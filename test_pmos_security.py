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

    # Every credential below is assembled from fragments, so this file carries
    # no credential-shaped literal of its own and stays clean under the two
    # gates that read it.
    AWS_ID = "AKIA" + "ABCDEFGHIJKLMNOP"
    AWS_TEMP_ID = "ASIA" + "ABCDEFGHIJKLMNOP"
    GITHUB_TOKEN = "ghp_" + "abcdefghij0123456789"
    ANTHROPIC_KEY = "sk-ant-" + "abcdefghijklmnopqrstuvwx"
    OPENAI_KEY = "sk-" + "abcdefghijklmnopqrstuvwx"
    PEM_HEADER = "-" * 5 + "BEGIN RSA PRIVATE KEY" + "-" * 5
    ASSIGNED_VALUE = "Ab3" + "cdefghijklmnopqrstuvwxyz"

    def test_every_credential_detector_has_a_fixture_that_names_it(self):
        """One synthetic credential per detector, asserted against the detector
        that should catch it. The suite used to supply an OpenRouter key alone
        and to assert on the file path only, so five of the six patterns could
        be deleted or narrowed with every test still green."""
        cases = {
            "aws-id.py": ('ID = "%s"\n' % self.AWS_ID,
                          "credential-shaped aws value"),
            "aws-temp-id.py": ('ID = "%s"\n' % self.AWS_TEMP_ID,
                               "credential-shaped aws value"),
            "github.py": ('T = "%s"\n' % self.GITHUB_TOKEN,
                          "credential-shaped github value"),
            "anthropic.py": ('K = "%s"\n' % self.ANTHROPIC_KEY,
                             "credential-shaped anthropic value"),
            "openai.py": ('K = "%s"\n' % self.OPENAI_KEY,
                          "credential-shaped openai value"),
            "private-key.md": "%s\n" % self.PEM_HEADER,
            "assignment.py": ('api_key = "%s"\n' % self.ASSIGNED_VALUE,
                              "credential-shaped assignment"),
        }
        cases["private-key.md"] = (cases["private-key.md"],
                                   "credential-shaped private-key value")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            self.assertEqual(scan(root), [])
            for name, (body, message) in cases.items():
                with self.subTest(name=name):
                    path = root / name
                    write(path, body)
                    findings = scan(root)
                    self.assertTrue(
                        any(item.path == name and item.code == "committed-secret"
                            and item.message == message for item in findings),
                        findings)
                    path.unlink()

    def test_a_test_named_file_is_not_exempt_from_the_source_scan(self):
        """The AST pass skipped every file whose name began with test_, so a
        shell, an eval or a pickle could be committed there and run by CI with
        the gate green. The same hole covered any helper that happened to carry
        the prefix. A naming convention is not a safety property."""
        cases = {
            "test_shell.py": ("import subprocess\n"
                              "subprocess.run(['x'], shell=True)\n", "unsafe-shell"),
            "test_eval.py": ("eval('1 + 1')\n", "unsafe-execution"),
            "test_pickle.py": ("from pickle import loads\nloads(b'x')\n",
                               "unsafe-pickle"),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            for name, (body, code) in cases.items():
                with self.subTest(name=name):
                    path = root / name
                    write(path, body)
                    findings = scan(root)
                    self.assertTrue(
                        any(item.path == name and item.code == code
                            for item in findings), findings)
                    path.unlink()

    def test_shell_and_process_replacement_primitives_are_rejected(self):
        """getoutput and getstatusoutput take no shell= keyword to inspect and
        always run the command through /bin/sh -c, and the exec and spawn
        family hands the process an argument vector the caller controls. Both
        passed the gate while subprocess.run(shell=True) beside them failed."""
        cases = {
            "getoutput.py": "import subprocess\nsubprocess.getoutput('git ' + a)\n",
            "getstatusoutput.py": ("import subprocess\n"
                                   "subprocess.getstatusoutput('git ' + a)\n"),
            "execv.py": "import os\nos.execv('/bin/sh', ['sh', '-c', a])\n",
            "spawnv.py": ("import os\n"
                          "os.spawnv(os.P_WAIT, '/bin/sh', ['sh', '-c', a])\n"),
            "posix-spawn.py": ("import os\n"
                               "os.posix_spawn('/bin/sh', ['sh', '-c', a], os.environ)\n"),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            for name, body in cases.items():
                with self.subTest(name=name):
                    path = root / name
                    write(path, body)
                    findings = scan(root)
                    self.assertTrue(
                        any(item.path == name and item.code == "unsafe-execution"
                            for item in findings), findings)
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

    def test_a_lost_boundary_is_reported_against_the_document_that_lost_it(self):
        """Every phrase used to be tested against the five key documents
        concatenated and reported against docs/THREAT-MODEL.md whatever was
        missing. Dropping the whole evidence boundary from another document was
        invisible, and a real miss named a file that was not at fault."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            self.assertFalse([item for item in check(root)
                              if item.severity == "error"])
            write(root / "docs" / "ACCESSIBILITY.md",
                  "# Accessibility\n\nNothing about evidence at all.\n")
            issues = [item for item in check(root)
                      if item.code == "evidence-boundary"]
            self.assertTrue(issues)
            self.assertEqual({"docs/ACCESSIBILITY.md"},
                             {item.path for item in issues})

    def test_a_boundary_another_document_still_carries_is_not_masked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secure_fixture(root)
            model = root / "docs" / "THREAT-MODEL.md"
            write(model, model.read_text(encoding="utf-8")
                  .replace("a live sandbox", "a live environment"))
            issues = [item for item in check(root)
                      if item.code == "evidence-boundary"]
            self.assertEqual(
                [("docs/THREAT-MODEL.md",
                  "missing explicit boundary: live sandbox")],
                [(item.path, item.message) for item in issues])

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
