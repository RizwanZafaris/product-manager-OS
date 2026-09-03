#!/usr/bin/env python3
"""One probe per readiness criterion that needs more than a single command.

    python3 tools/readiness_probe.py <probe>
    python3 tools/readiness_probe.py --list

Standard library only, like every other script in this tree.

Each probe exits 0 only when the property actually holds on this checkout,
and prints what it measured either way. A probe never repairs anything and
never writes inside the repository except under a temporary product workspace
it removes afterwards, so running the scorecard cannot improve the score it is
measuring.

The probes that mutate a workspace do it under a slug containing this process
id, so two scorecard runs cannot collide and a crashed run leaves a directory
named after a dead process rather than corrupting a real product.
"""

from __future__ import annotations

import json
import os
import posixpath
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO))

PROBE_SLUG = "readiness-probe-%d" % os.getpid()


def say(*parts):
    print(" ".join(str(p) for p in parts))


def run(command, cwd=None):
    """One subprocess. Returns (exit code, combined output)."""
    if isinstance(command, str):
        raise TypeError("probe commands must be argv sequences, never shell text")
    argv = list(command)
    if argv and argv[0] == "python3":
        argv[0] = sys.executable
    done = subprocess.run(argv, cwd=str(cwd or REPO), shell=False,
                          capture_output=True, text=True)
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def remove_workspace(slug):
    path = REPO / "products" / slug
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)


def tracked_tree(destination):
    """A copy of this repository holding exactly the tracked files.

    Not a filtered copytree. The first version of this ignored products/
    wholesale and so dropped products/README.md, which is tracked and which
    six files under learn/ link to, and the probe then reported a deletability
    failure that was its own. What CI checks out is the tracked set, so that is
    what a probe measuring CI's behaviour has to build.
    """
    destination = Path(destination)
    code, out = run(["git", "ls-files", "-z"])
    if code != 0:
        raise RuntimeError("git ls-files failed: %s" % out.strip()[:200])
    for rel in out.split("\0"):
        if not rel:
            continue
        source = REPO / rel
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            raw_target = os.readlink(source)
            if Path(raw_target).is_absolute():
                raise RuntimeError("tracked symlink has an absolute target: %s" % rel)
            try:
                (source.parent / raw_target).resolve().relative_to(REPO)
            except ValueError as exc:
                raise RuntimeError("tracked symlink escapes repository: %s" % rel) from exc
            os.symlink(raw_target, target)
        elif source.is_file():
            shutil.copy2(str(source), str(target), follow_symlinks=False)
        else:
            raise RuntimeError("tracked entry is neither a file nor a safe symlink: %s" % rel)
    return destination


# ------------------------------------------------------------------ probes

def probe_workspace_lifecycle():
    """Create a workspace, install every shipped template, verify it."""
    remove_workspace(PROBE_SLUG)
    try:
        for step in (["python3", "tools/init_product.py", PROBE_SLUG],
                     ["python3", "tools/init_product.py", PROBE_SLUG,
                      "--add-all"],
                     ["python3", "tools/init_product.py", PROBE_SLUG,
                      "--check"]):
            code, out = run(step)
            if code != 0:
                say("FAILED at: %s" % " ".join(step))
                say(out.strip()[-1500:])
                return 1
        installed = len(list((REPO / "products" / PROBE_SLUG).rglob("*.md")))
        shipped = len(list((REPO / "templates").rglob("*.md")))
        say("workspace lifecycle: created, %d document(s) installed from %d "
            "shipped templates, every link re-resolved." % (installed, shipped))
        return 0 if installed >= shipped else 1
    finally:
        remove_workspace(PROBE_SLUG)


def probe_workspace_links():
    """A fully installed workspace has zero broken links."""
    remove_workspace(PROBE_SLUG)
    try:
        run(["python3", "tools/init_product.py", PROBE_SLUG])
        run(["python3", "tools/init_product.py", PROBE_SLUG, "--add-all"])
        code, out = run(["python3", "lint.py", "--workspace",
                         "products/%s" % PROBE_SLUG])
        say(out.strip().splitlines()[-1] if out.strip() else "no output")
        return code
    finally:
        remove_workspace(PROBE_SLUG)


def probe_workspace_drift():
    """No link points at a blank template when a filled copy exists.

    The check the link gate cannot make: a link into templates/ resolves, so
    it is not broken, and it is still the wrong file once this workspace holds
    its own copy of that template. Measured before the settle pass existed:
    181 links across 41 files.
    """
    import workspace as ws

    remove_workspace(PROBE_SLUG)
    try:
        run(["python3", "tools/init_product.py", PROBE_SLUG])
        run(["python3", "tools/init_product.py", PROBE_SLUG, "--add-all"])
        drifted, files = 0, set()
        root = REPO / "products" / PROBE_SLUG
        for path in sorted(root.rglob("*.md")):
            here = posixpath.dirname(path.relative_to(REPO).as_posix())
            _text, rewrites, _skipped = ws.rewrite_links(
                path.read_text(encoding="utf-8"), here, here, PROBE_SLUG)
            if rewrites:
                drifted += len(rewrites)
                files.add(path.name)
        say("semantic source-template drift: %d link(s) across %d file(s)"
            % (drifted, len(files)))
        if drifted:
            for name in sorted(files)[:10]:
                say("  " + name)
        return 0 if drifted == 0 else 1
    finally:
        remove_workspace(PROBE_SLUG)


def probe_link_grammar():
    """The rewriter and the gate read the same link grammar."""
    import lint
    import workspace as ws

    if (ws.LINK_RE is not lint.LINK_RE or
            ws.REF_DEF_RE is not lint.REF_DEF_RE):
        say("the rewriter and the gate use different link patterns")
        return 1

    cases = [
        ("](../../GLOSSARY.md)", "](../../../GLOSSARY.md)",
         "plain inline"),
        ("](<../../GLOSSARY.md>)", "](<../../../GLOSSARY.md>)",
         "angle-bracket destination"),
        ('](../../GLOSSARY.md "A title")',
         '](../../../GLOSSARY.md "A title")',
         "inline title preserved verbatim"),
        ("](../../GLOSSARY.md 'A title')",
         "](../../../GLOSSARY.md 'A title')",
         "single-quoted title preserved verbatim"),
        ("](../../GLOSSARY.md (A title))",
         "](../../../GLOSSARY.md (A title))",
         "parenthesized title preserved verbatim"),
        ("](../../GLOSSARY.md#a-heading)",
         "](../../../GLOSSARY.md#a-heading)", "anchor preserved"),
        ('](../../GLOSSARY.md#a-heading "A title")',
         '](../../../GLOSSARY.md#a-heading "A title")',
         "anchor and title preserved together"),
        ('[read][glossary]\n[glossary][]\n'
         '[glossary]: ../../GLOSSARY.md "A title"',
         '[read][glossary]\n[glossary][]\n'
         '[glossary]: ../../../GLOSSARY.md "A title"',
         "full/collapsed reference uses and definition"),
        ("](../../%47LOSSARY.md)", "](../../../GLOSSARY.md)",
         "percent-encoded destination resolved"),
    ]
    failed = []
    for source, expected, label in cases:
        out, rewrites, _skipped = ws.rewrite_links(
            source, "templates/discovery", "products/p/discovery", "p")
        if not rewrites:
            failed.append("%s: not seen by the rewriter" % label)
            continue
        if out != expected:
            failed.append("%s: expected %r, got %r" %
                          (label, expected, out))
    for untouched in ("](https://example.com/path)", "](mailto:a@example.com)",
                      "](#same-document)"):
        out, rewrites, skipped = ws.rewrite_links(
            untouched, "templates/discovery", "products/p/discovery", "p")
        if out != untouched or rewrites or skipped:
            failed.append("external/mail/same-document link changed: %r" %
                          untouched)

    remove_workspace(PROBE_SLUG)
    try:
        source = REPO / "products" / PROBE_SLUG / "source"
        destination = REPO / "products" / PROBE_SLUG / "destination"
        source.mkdir(parents=True)
        destination.mkdir(parents=True)
        (source / "A File.md").write_text("# A file\n", encoding="utf-8")
        out, rewrites, skipped = ws.rewrite_links(
            "](<A File.md>)", source.relative_to(REPO).as_posix(),
            destination.relative_to(REPO).as_posix(), PROBE_SLUG)
        expected = "](<../source/A File.md>)"
        if out != expected or not rewrites or skipped:
            failed.append("angle-bracket space target: expected %r, got %r" %
                          (expected, out))
    finally:
        remove_workspace(PROBE_SLUG)

    for note in failed:
        say("  " + note)
    total = len(cases) + 4
    say("link grammar: %d of %d spellings handled by one pattern"
        % (total - len(failed), total))
    return 0 if not failed else 1


def probe_compile_all():
    """Compile every tracked Python file without a shell or source pycache."""
    import tempfile

    code, out = run(["git", "ls-files", "-z", "--", "*.py"])
    if code != 0:
        say(out.strip()[-800:])
        return code
    files = [rel for rel in out.split("\0") if rel]
    if not files:
        say("git reported zero tracked Python files")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        for number, rel in enumerate(files):
            try:
                py_compile.compile(
                    str(REPO / rel),
                    cfile=str(Path(tmp) / ("%05d.pyc" % number)),
                    doraise=True)
            except py_compile.PyCompileError as error:
                say(str(error)[-800:])
                return 1
    say("every tracked Python file compiles (%d file(s))" % len(files))
    return 0


def probe_full_suite():
    """Root, harness and regulated suites, with the counts printed."""
    required_root = (
        "test_lint.py", "test_readiness.py", "test_pmos_routing.py",
        "test_pmos_store.py", "test_pmos_domain.py",
        "test_pmos_operations.py", "test_pmos_hooks.py",
        "test_pmos_usecases.py", "test_pmos_conductor.py",
        "test_pmos_skills.py", "test_pmos_cli.py",
        "test_pmos_release.py", "test_pmos_security.py",
        "test_pmos_review.py",
    )
    missing = [name for name in required_root if not (REPO / name).is_file()]
    if missing:
        say("required root test modules missing: %s" % ", ".join(missing))
        return 1
    root_modules = [Path(name).stem for name in required_root]
    total, failed = 0, 0
    for label, command, cwd in (
            ("root", ["python3", "-m", "unittest", *root_modules, "-v"],
             REPO),
            ("harness", ["python3", "-m", "unittest", "discover", "-s",
                         "harness", "-p", "test_*.py", "-v"], REPO),
            ("regulated", ["python3", "-m", "unittest", "test_lint", "-v"],
             REPO / "modules" / "regulated")):
        code, out = run(command, cwd=cwd)
        match = re.search(r"^Ran (\d+) tests?", out, re.M)
        ran = int(match.group(1)) if match else 0
        skipped = len(re.findall(r"\.\.\. skipped", out))
        nonpassing = any(token in out for token in
                         ("expected failures=", "unexpected successes="))
        total += ran
        if code != 0 or skipped or ran == 0 or nonpassing:
            failed += 1
            say("%s: %d test(s), %d skipped, exit %d" % (label, ran, skipped,
                                                         code))
        else:
            say("%s: %d test(s), 0 skipped, ok" % (label, ran))
    say("total: %d test executions" % total)
    return 0 if failed == 0 else 1


def probe_ci_covers_runtime():
    """CI must actively invoke the canonical, code-owned release suite."""
    workflow = REPO / ".github" / "workflows" / "lint.yml"
    if not workflow.is_file():
        say("no workflow file")
        return 1
    # Comments are deliberately excluded. A prose claim that CI runs a command
    # is not an executable workflow step.
    lines = [line.strip() for line in workflow.read_text(
        encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    problems = []
    if "run: python3 tools/ci_gate.py" not in lines:
        problems.append("no active exact invocation of tools/ci_gate.py")
    if any(line.startswith("continue-on-error:") and
           line.split(":", 1)[1].strip().lower() not in ("false", "${{ false }}")
           for line in lines):
        problems.append("workflow permits continue-on-error")
    if any(line.startswith("if:") and line.split(":", 1)[1].strip().lower()
           in ("false", "${{ false }}") for line in lines):
        problems.append("workflow contains a statically disabled step or job")
    for version in ('"3.11"', '"3.13"'):
        if version not in "\n".join(lines):
            problems.append("required Python %s is absent" % version.strip('"'))

    code, output = run(["python3", "tools/ci_gate.py", "--manifest"])
    try:
        manifest = json.loads(output) if code == 0 else {}
    except json.JSONDecodeError:
        manifest = {}
    gate_ids = {row.get("id") for row in manifest.get("gates", [])
                if isinstance(row, dict)}
    required = {
        "compile", "root-tests", "harness-tests", "regulated-tests",
        "claude-adapter", "desktop-adapter", "workspace-lifecycle",
        "workspace-links", "workspace-contract", "regulated-example",
        "os-tree", "json-syntax", "graph-freshness", "manifest-contract",
        "frontmatter", "security-policy", "docs-contract",
        "readiness-local",
    }
    missing = sorted(required - gate_ids)
    if missing:
        problems.append("canonical suite misses gate ids: %s" %
                        ", ".join(missing))
    for problem in problems:
        say("  " + problem)
    say("CI wiring: canonical invocation %s; %d/%d required gate ids" %
        ("active" if "run: python3 tools/ci_gate.py" in lines else "missing",
         len(required) - len(missing), len(required)))
    return 0 if not problems else 1


def probe_deletable_harness():
    """The tree gate passes with harness/ removed."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        clone = tracked_tree(Path(tmp) / "tree")
        shutil.rmtree(clone / "harness", ignore_errors=True)
        for step in (["python3", "lint.py", "--os"],
                     ["python3", "tools/check_manifest.py", "--quiet"],
                     ["python3", "tools/check_workspace_contract.py",
                      "--quiet"],
                     ["python3", "-m", "unittest", "test_lint"]):
            code, out = run(step, cwd=clone)
            if code != 0:
                say("with harness/ deleted, this failed: %s"
                    % " ".join(step))
                say(out.strip()[-900:])
                return 1
    say("the harness is deletable: tree gate, manifest, contract and root "
        "suite all pass without it")
    return 0


def probe_mutation_checks():
    """Prove each named gate fails for the defect its criterion claims.

    Every mutant gets a fresh tracked tree. Its targeted verifier must pass
    before mutation, the anchor must occur exactly once, and the mutated check
    must fail with the intended diagnostic. An unrelated red build earns no
    mutation evidence.
    """
    import tempfile

    mutations = [
        {
            "label": "runtime syntax error",
            "rel": "harness/runner.py", "old": "\nif __name__ == \"__main__\":",
            "new": "\ndef mutation_broken(:\n\nif __name__ == \"__main__\":",
            "argv": ["python3", "-m", "py_compile", "harness/runner.py"],
            "diagnostic": "SyntaxError",
        },
        {
            "label": "canonical STATE path drift",
            "rel": "tools/workspace.py",
            "old": '"templates/execution/state.md": "STATE.md",',
            "new": '"templates/execution/state.md": "execution/STATE.md",',
            "argv": ["python3", "-m", "unittest",
                     "harness.test_runner.AuditRegressionTests."
                     "test_state_lands_at_the_workspace_root", "-v"],
            "diagnostic": "products/p/STATE.md",
        },
        {
            "label": "semantic link repointed to blank template",
            "rel": "tools/workspace.py",
            "old": "if local and (REPO / local).exists():",
            "new": "if False and local and (REPO / local).exists():",
            "argv": ["python3", "-m", "unittest",
                     "harness.test_runner.AuditRegressionTests."
                     "test_a_link_prefers_the_workspace_copy_over_the_blank_template", "-v"],
            "diagnostic": "AssertionError",
        },
        {
            "label": "inline title discarded",
            "rel": "tools/workspace.py",
            "old": "return replace_capture(match, group, wrap_target(rebuilt, angled))",
            "new": 'return "](%s)" % wrap_target(rebuilt, angled)',
            "argv": ["python3", "tools/readiness_probe.py", "link-grammar"],
            "diagnostic": "inline title preserved",
        },
        {
            "label": "reference definition left unrelocated",
            "rel": "tools/workspace.py",
            "old": "stripped = REF_DEF_RE.sub(replace_reference, stripped)",
            "new": "stripped = stripped",
            "argv": ["python3", "tools/readiness_probe.py", "link-grammar"],
            "diagnostic": "full/collapsed reference",
        },
        {
            "label": "active canonical CI invocation commented out",
            "rel": ".github/workflows/lint.yml",
            "old": "        run: python3 tools/ci_gate.py",
            "new": "        # run: python3 tools/ci_gate.py",
            "argv": ["python3", "tools/readiness_probe.py",
                     "ci-covers-runtime"],
            "diagnostic": "no active exact invocation",
        },
        {
            "label": "route loses its executable kind",
            "rel": "harness/MANIFEST.json",
            "old": ('"id": "conduct-product-journey",\n'
                    '      "router_row": "\\"start\\", \\"start a product\\", or any wish to be interviewed through the loop",\n'
                    '      "trigger": ["start", "start a product", "interview me through the loop"],\n'
                    '      "stage": "DISCOVER",\n'
                    '      "gate": 1,\n'
                    '      "tier": "judgment",\n'
                    '      "kind": "interactive",'),
            "new": ('"id": "conduct-product-journey",\n'
                    '      "router_row": "\\"start\\", \\"start a product\\", or any wish to be interviewed through the loop",\n'
                    '      "trigger": ["start", "start a product", "interview me through the loop"],\n'
                    '      "stage": "DISCOVER",\n'
                    '      "gate": 1,\n'
                    '      "tier": "judgment",'),
            "argv": ["python3", "tools/check_manifest.py", "--quiet"],
            "diagnostic": "kind",
        },
        {
            "label": "mandatory regulated gate section removed",
            "rel": "modules/regulated/examples/dispute-summary/PRD.md",
            "old": "## 6. Review gate: sign-off requires",
            "new": "## 6. Notes",
            "argv": ["python3", "lint.py",
                     "modules/regulated/examples/dispute-summary/PRD.md"],
            "diagnostic": "does not mention",
        },
        {
            "label": "approved evidence becomes incomplete",
            "rel": "modules/regulated/examples/dispute-summary/PRD.md",
            "old": "**Status:** In review", "new": "**Status:** Approved",
            "argv": ["python3", "lint.py",
                     "modules/regulated/examples/dispute-summary/PRD.md"],
            "diagnostic": "status is Approved",
        },
        {
            "label": "exact unit-test evidence becomes an empty selection",
            "rel": "tools/readiness_registry.py",
            "old": "test_pmos_security.PublicRuntimeAdversarialTests.test_untrusted_prompt_cannot_authorize_tool_and_secret_never_leaks",
            "new": "test_pmos_security.PublicRuntimeAdversarialTests.test_does_not_exist",
            "argv": ["python3", "tools/readiness.py", "--category",
                     "governance"],
            "diagnostic": "governance 10/15",
        },
        {
            "label": "data rubric attempts arbitrary verifier command",
            "rel": "docs/readiness/criteria.json",
            "old": '"verifier": "workspace-contract"',
            "new": '"verifier": "false || true"',
            "argv": ["python3", "tools/readiness.py", "--category",
                     "workspace"],
            "diagnostic": "unknown verifier",
        },
        {
            "label": "queue integrity check bypassed before dispatch",
            "rel": "pmos/store.py",
            "old": ("            self._assert_queue_verified()\n"
                    "            self._recover_expired_locked(stamp)\n"
                    "            cancelling = self._conn.execute("),
            "new": ("            self._recover_expired_locked(stamp)\n"
                    "            cancelling = self._conn.execute("),
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_store.py", "-v"],
            "diagnostic": "IntegrityError",
        },
        {
            "label": "memory projection verification bypassed",
            "rel": "pmos/store.py",
            "old": "        scope, task_key, _ = self._memory_scope(scope, task_id)\n        self._assert_memory_verified()\n        conditions = [\"p.scope=?\", \"p.task_key=?\"]",
            "new": "        scope, task_key, _ = self._memory_scope(scope, task_id)\n        conditions = [\"p.scope=?\", \"p.task_key=?\"]",
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_store.py", "-v"],
            "diagnostic": "IntegrityError",
        },
        {
            "label": "approval evidence drift accepted",
            "rel": "pmos/domain.py",
            "old": ('        if entity_type == "evidence" and getattr(old, "content_hash", None) != getattr(obj, "content_hash", None):'),
            "new": ('        if False and entity_type == "evidence" and getattr(old, "content_hash", None) != getattr(obj, "content_hash", None):'),
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_domain.py", "-v"],
            "diagnostic": "active approval refers to changed or missing evidence",
        },
        {
            "label": "release tree hash verification bypassed",
            "rel": "pmos/release.py",
            "old": "    if value.get(\"tree_sha256\") != _tree_hash(expected):\n        errors.append(\"tree hash mismatch\")",
            "new": "    if False and value.get(\"tree_sha256\") != _tree_hash(expected):\n        errors.append(\"tree hash mismatch\")",
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_release.py", "-v"],
            "diagnostic": "AssertionError",
        },
        {
            "label": "OpenRouter redirect response accepted",
            "rel": "pmos/openrouter.py",
            "old": "                if final_url is not None and _origin(final_url) != _origin(self.config.base_url):\n                    raise OpenRouterRedirectError()",
            "new": "                if False and final_url is not None and _origin(final_url) != _origin(self.config.base_url):\n                    raise OpenRouterRedirectError()",
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_skills.py", "-v"],
            "diagnostic": "AssertionError",
        },
        {
            "label": "hook actor boundary bypassed",
            "rel": "pmos/hooks.py",
            "old": ('        if not _nonempty_text(payload.get("actor_id")):\n'
                    '            return result("deny", "transition needs a nonempty actor identifier")'),
            "new": ('        if False and not _nonempty_text(payload.get("actor_id")):\n'
                    '            return result("deny", "transition needs a nonempty actor identifier")'),
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_hooks.py", "-v"],
            "diagnostic": "AssertionError",
        },
        {
            "label": "trusted skill hash verification bypassed",
            "rel": "pmos/skills.py",
            "old": ('                if hashlib.sha256(snapshot).hexdigest() != _manifest_hash(assets[asset_name]):\n'
                    '                    raise SkillContractError("trusted asset hash drift for %s/%s" % (skill_id, asset_name))'),
            "new": ('                if False and hashlib.sha256(snapshot).hexdigest() != _manifest_hash(assets[asset_name]):\n'
                    '                    raise SkillContractError("trusted asset hash drift for %s/%s" % (skill_id, asset_name))'),
            "argv": ["python3", "-m", "unittest", "discover", "-s", ".",
                     "-p", "test_pmos_skills.py", "-v"],
            "diagnostic": "AssertionError",
        },
    ]

    caught, missed = 0, []
    for number, mutation in enumerate(mutations):
        with tempfile.TemporaryDirectory() as tmp:
            base = tracked_tree(Path(tmp) / ("tree-%02d" % number))
            command = mutation["argv"]
            before, baseline = run(command, cwd=base)
            if before != 0:
                missed.append("%s (baseline failed: %s)" %
                              (mutation["label"], baseline.strip()[-180:]))
                continue
            target = base / mutation["rel"]
            original = target.read_text(encoding="utf-8")
            count = original.count(mutation["old"])
            if count != 1:
                missed.append("%s (mutation anchor count %d, expected 1)" %
                              (mutation["label"], count))
                continue
            target.write_text(original.replace(
                mutation["old"], mutation["new"], 1), encoding="utf-8")
            code, output = run(command, cwd=base)
            if code == 0:
                missed.append("%s (targeted gate stayed green)" %
                              mutation["label"])
            elif mutation["diagnostic"].lower() not in output.lower():
                missed.append("%s (wrong diagnostic: %s)" %
                              (mutation["label"], output.strip()[-180:]))
            else:
                caught += 1
    for label in missed:
        say("  NOT caught: " + label)
    say("mutation checks: %d of %d defects caught by the gates"
        % (caught, len(mutations)))
    return 0 if not missed else 1


def probe_golden_path():
    """The documented quickstart, executed as written."""
    remove_workspace(PROBE_SLUG)
    try:
        steps = [
            ["python3", "tools/init_product.py", PROBE_SLUG],
            ["python3", "tools/init_product.py", PROBE_SLUG, "--add",
             "templates/discovery/discovery-document.md"],
            ["python3", "tools/init_product.py", PROBE_SLUG, "--check"],
            ["python3", "lint.py", "--workspace", "products/%s" % PROBE_SLUG],
        ]
        for step in steps:
            code, out = run(step)
            if code != 0:
                say("golden path broke at: %s" % " ".join(step))
                say(out.strip()[-900:])
                return 1
        root = REPO / "products" / PROBE_SLUG
        for expected in ("STATE.md", "discovery/discovery-document.md"):
            if not (root / expected).is_file():
                say("golden path did not produce %s" % expected)
                return 1
        say("golden path: workspace created, STATE.md seeded, a discovery "
            "document installed with resolving links, workspace gate green")
        return 0
    finally:
        remove_workspace(PROBE_SLUG)


PROBES = {name[len("probe_"):].replace("_", "-"): value
          for name, value in sorted(globals().items())
          if name.startswith("probe_")}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("--list", "-l", "-h", "--help"):
        say("probes:")
        for name in sorted(PROBES):
            say("  " + name)
        return 0 if argv and argv[0] == "--list" else 2
    name = argv[0]
    if name not in PROBES:
        say("unknown probe %r. Run --list." % name)
        return 2
    try:
        return PROBES[name]()
    except Exception as error:                              # noqa: BLE001
        say("probe %s raised: %s: %s"
            % (name, type(error).__name__, error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
