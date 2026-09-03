"""Adversarial tests for the PM OS local security and documentation gates."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pmos.domain import ApprovalError, PMOSDomain
from pmos.hooks import claude_output, decide
from pmos.store import Store, ValidationError
from tools.docs_contract import check
from tools.security_gate import scan


REPO = Path(__file__).resolve().parent


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def secure_fixture(root: Path) -> None:
    write(root / "pyproject.toml", "[project]\ndependencies = []\n")
    write(root / "pmos" / "cli.py", "def main():\n    return 0\n")
    for name in ("domain.py", "store.py", "hooks.py", "openrouter.py"):
        write(root / "pmos" / name, "# local runtime\n")
    write(root / "README.md", "# PM OS\n\nLocal evidence is not external evidence.\n")
    write(root / "SECURITY.md", "# Security\n\n[Threat model](docs/THREAT-MODEL.md)\n")
    write(root / "docs" / "ARCHITECTURE.md", "# Architecture\n\n[Security guide](../SECURITY.md)\n")
    write(root / "docs" / "ACCESSIBILITY.md", """# Accessibility

## Boundaries

Local evidence is not external evidence. A live sandbox, provider, user, and
regulatory claim requires independent evidence.
""")
    write(root / "docs" / "THREAT-MODEL.md", """# Threat Model

## Boundary

Local evidence is not external evidence. It does not prove a live sandbox,
provider, user, or regulatory claim.

## Dependency surface and exception inventory

The dependency surface is empty. The exception inventory is empty.
""")


class SecurityGateFixtureTests(unittest.TestCase):
    def test_clean_fixture_passes_and_each_static_violation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            self.assertEqual(scan(root), [])
            cases = {
                "secret.py": 'TOKEN = "' + "sk-or-v1-" + 'abcdefghijklmnopqrstuvwx"\n',
                "shell.py": 'import subprocess\nsubprocess.run(["x"], shell=True)\n',
                "dynamic.py": 'eval("1 + 1")\n',
                "pickle.py": 'import pickle\n',
                "escape.py": 'open("../outside", "w")\n',
            }
            for name, body in cases.items():
                with self.subTest(name=name):
                    path = root / name
                    write(path, body)
                    findings = scan(root)
                    self.assertTrue(any(item.path == name for item in findings), findings)
                    path.unlink()

    def test_threat_model_and_dependency_exceptions_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            (root / "docs" / "THREAT-MODEL.md").write_text("# Threat\n", encoding="utf-8")
            codes = {item.code for item in scan(root)}
            self.assertIn("threat-model", codes)
            write(root / "requirements.txt", "unsafe-package==1\n")
            self.assertIn("dependency-surface", {item.code for item in scan(root)})

    def test_aliases_import_from_dynamic_dispatch_and_nonliteral_shell_fail_closed(self):
        """The source gate must see the primitive, not just one spelling of it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            cases = {
                "subprocess-alias.py": (
                    "import subprocess as sp\nsp.run(['x'], shell=bool(1))\n",
                    "unsafe-shell",
                ),
                "subprocess-from.py": (
                    "from subprocess import Popen as launch\nlaunch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-assignment.py": (
                    "import subprocess\nlaunch = subprocess.run\nlaunch(['x'], shell='maybe')\n",
                    "unsafe-shell",
                ),
                "subprocess-expanded-shell.py": (
                    "import subprocess\nsubprocess.run(['x'], **{'shell': True})\n",
                    "unsafe-shell",
                ),
                "subprocess-popen-positional-shell.py": (
                    "import subprocess\nsubprocess.Popen(['x'], -1, None, None, None, None, None, True, True)\n",
                    "unsafe-shell",
                ),
                "subprocess-dynamic-import.py": (
                    "getattr(__import__('subprocess'), 'run')(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-subscript-dispatch.py": (
                    "import subprocess\nsubprocess.__dict__['run'](['x'], shell=True)\n",
                    "unsafe-dynamic-dispatch",
                ),
                "subprocess-vars-subscript-dispatch.py": (
                    "import subprocess\ntable = vars(subprocess)\n"
                    "launch = table['run']\nlaunch(['x'], shell=True)\n",
                    "unsafe-dynamic-dispatch",
                ),
                "subprocess-conditional-overwrite.py": (
                    "import subprocess\nlaunch = subprocess.run\nif maybe:\n"
                    "    launch = harmless\nlaunch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-while-overwrite.py": (
                    "import subprocess\nlaunch = subprocess.run\nwhile maybe:\n"
                    "    launch = harmless\nlaunch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-for-overwrite.py": (
                    "import subprocess\nlaunch = subprocess.run\nfor item in items:\n"
                    "    launch = harmless\nlaunch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-match-overwrite.py": (
                    "import subprocess\nlaunch = subprocess.run\nmatch state:\n"
                    "    case 'safe':\n        launch = harmless\n"
                    "launch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-match-guard-alias.py": (
                    "import subprocess\nlaunch = harmless\nmatch state:\n"
                    "    case _ if (launch := subprocess.run):\n        pass\n"
                    "launch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-ifexp-alias.py": (
                    "import subprocess\nlaunch = harmless if maybe else subprocess.run\n"
                    "launch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-class-attribute-alias.py": (
                    "import subprocess\nclass Launcher:\n"
                    "    run = subprocess.run\nLauncher.run(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-class-attribute-conditional.py": (
                    "import subprocess\nclass Launcher:\n    pass\n"
                    "Launcher.run = harmless\nif maybe:\n"
                    "    Launcher.run = subprocess.run\nLauncher.run(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "subprocess-tuple-alias.py": (
                    "import subprocess\nlaunch, harmless = subprocess.run, print\n"
                    "launch(['x'], shell=True)\n",
                    "unsafe-shell",
                ),
                "os-alias.py": (
                    "import os as operating\noperating.system('x')\n",
                    "unsafe-execution",
                ),
                "os-from.py": (
                    "from os import popen as launch\nlaunch('x')\n",
                    "unsafe-execution",
                ),
                "builtins-getattr.py": (
                    "import builtins\ngetattr(builtins, 'eval')('1 + 1')\n",
                    "unsafe-execution",
                ),
                "builtins-from.py": (
                    "from builtins import exec as execute\nexecute('pass')\n",
                    "unsafe-execution",
                ),
                "dynamic-dispatch.py": (
                    "import builtins\nname = 'eval'\ngetattr(builtins, name)\n",
                    "unsafe-dynamic-dispatch",
                ),
                "pickle-from.py": (
                    "from pickle import loads as deserialize\ndeserialize(b'payload')\n",
                    "unsafe-pickle",
                ),
            }
            for name, (body, code) in cases.items():
                with self.subTest(name=name):
                    write(root / name, body)
                    findings = scan(root)
                    self.assertTrue(any(item.path == name and item.code == code
                                        for item in findings), findings)
                    (root / name).unlink()

            write(root / "literal-false.py", "import subprocess\n"
                  "subprocess.Popen(['x'], -1, None, None, None, None, None, True, False)\n")
            self.assertFalse([item for item in scan(root) if item.path == "literal-false.py"])


class DocumentationContractFixtureTests(unittest.TestCase):
    def test_clean_fixture_passes_and_readme_warning_is_actionable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            self.assertFalse([item for item in check(root) if item.severity == "error"])
            (root / "README.md").write_text("# PM OS\n", encoding="utf-8")
            warnings = check(root)
            self.assertTrue(any(item.code == "readme-boundary" for item in warnings))

    def test_mutations_prove_heading_alt_link_boundary_and_claim_failures(self):
        mutations = {
            "heading": ("docs/ACCESSIBILITY.md", "# Accessibility\n\n### Skipped\n", "heading-order"),
            "alt": ("docs/ACCESSIBILITY.md", "# Accessibility\n\n![](x.png)\n", "image-alt"),
            "link": ("docs/ACCESSIBILITY.md", "# Accessibility\n\n[click here](missing.md)\n", "ambiguous-link"),
            "claim": ("docs/ACCESSIBILITY.md", "# Accessibility\n\nProvider certified\n", "overclaim"),
        }
        for label, (name, text, code) in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                secure_fixture(root)
                write(root / name, text)
                self.assertIn(code, {item.code for item in check(root)})


class PublicRuntimeAdversarialTests(unittest.TestCase):
    def test_untrusted_prompt_cannot_authorize_tool_and_secret_never_leaks(self):
        secret = "sk-or-v1-" + "a" * 32
        denied = decide("PreToolUse", {
            "tool_name": "Bash", "tool_input": {"command": "git push",
                                                   "instruction_origin": "untrusted"},
            "session_id": "case-1"})
        self.assertEqual(denied.action, "deny")
        secret_denied = decide("PreToolUse", {
            "tool_name": "Write", "tool_input": {"file_path": "x.md", "content": secret}})
        rendered = json.dumps(claude_output("PreToolUse", secret_denied), sort_keys=True)
        self.assertEqual(secret_denied.action, "deny")
        self.assertNotIn(secret, json.dumps(secret_denied.audit, sort_keys=True))
        self.assertNotIn(secret, rendered)

    def test_store_rejects_traversal_before_persistence(self):
        with tempfile.TemporaryDirectory() as tmp, Store(Path(tmp) / "pmos.db") as store:
            product = store.create_product("product")
            with self.assertRaises(ValidationError):
                store.prepare_commit(product.product_id, {"../escape.md": "no"},
                                     expected_revision=product)
            self.assertEqual(store.read_snapshot(product.product_id).files, {})

    def test_audit_tamper_and_regulated_approval_drift_fail_closed(self):
        domain = PMOSDomain()
        _organization, product, owner, _membership = domain.bootstrap_workspace(
            "Acme", "Bank", "Owner", regulated=True)
        initiative = domain.create_initiative(
            product.id, "KYC", actor_id=owner.id)
        approver = domain.create_user("Approver", actor_id=owner.id)
        domain.add_membership(
            product.id, approver.id, "approver", actor_id=owner.id)
        evidence = domain.create_evidence(
            initiative.id, "Control", "v1", actor_id=owner.id)
        approval = domain.request_approval(initiative.id, evidence_ids=[evidence.id],
                                           policy_version="policy-1",
                                           actor_id=owner.id)
        domain.approve(approval.id, approver_id=approver.id, evidence_ids=[evidence.id])
        exported = json.loads(domain.export_audit())
        exported["events"][0]["action"] = "forged"
        self.assertFalse(domain.verify_audit_export(exported))
        domain.update("evidence", evidence.id, expected_revision=evidence.revision,
                      content="changed", actor_id=owner.id)
        self.assertEqual(domain.get(approval.id, actor_id=owner.id).status,
                         "invalidated")
        with self.assertRaises(ApprovalError):
            domain.approve(approval.id, approver_id=approver.id, evidence_ids=[evidence.id])


if __name__ == "__main__":
    unittest.main()
