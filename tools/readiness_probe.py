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
    done = subprocess.run(command, cwd=str(cwd or REPO), shell=isinstance(
        command, str), capture_output=True, text=True)
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
        if not source.is_file():
            continue
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source), str(target))
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

    if ws.LINK_RE is not lint.LINK_RE:
        say("the rewriter and the gate use different link patterns")
        return 1

    cases = [
        ("](../../GLOSSARY.md)", "plain inline"),
        ("](<../../GLOSSARY.md>)", "angle-bracket destination"),
        ('](../../GLOSSARY.md "A title")', "inline with a title"),
        ("](../../GLOSSARY.md#a-heading)", "anchor preserved"),
    ]
    failed = []
    for text, label in cases:
        out, rewrites, _skipped = ws.rewrite_links(
            text, "templates/discovery", "products/p/discovery", "p")
        if not rewrites:
            failed.append("%s: not seen by the rewriter" % label)
            continue
        if "../../../GLOSSARY.md" not in out:
            failed.append("%s: rewrote to %r" % (label, out))
        if text.endswith("#a-heading)") and "#a-heading" not in out:
            failed.append("%s: anchor was dropped" % label)
    for note in failed:
        say("  " + note)
    say("link grammar: %d of %d spellings handled by one pattern"
        % (len(cases) - len(failed), len(cases)))
    return 0 if not failed else 1


def probe_compile_all():
    code, out = run("git ls-files '*.py' | xargs python3 -m py_compile")
    say("every tracked Python file compiles" if code == 0 else out.strip()[-800:])
    return code


def probe_full_suite():
    """Root, harness and regulated suites, with the counts printed."""
    total, failed = 0, 0
    for label, command, cwd in (
            ("root", ["python3", "-m", "unittest", "test_lint", "-v"], REPO),
            ("harness", ["python3", "-m", "unittest", "discover", "-s",
                         "harness", "-p", "test_*.py", "-v"], REPO),
            ("regulated", ["python3", "-m", "unittest", "test_lint", "-v"],
             REPO / "modules" / "regulated")):
        code, out = run(command, cwd=cwd)
        match = re.search(r"^Ran (\d+) tests?", out, re.M)
        ran = int(match.group(1)) if match else 0
        skipped = len(re.findall(r"\.\.\. skipped", out))
        total += ran
        if code != 0 or skipped:
            failed += 1
            say("%s: %d test(s), %d skipped, exit %d" % (label, ran, skipped,
                                                         code))
        else:
            say("%s: %d test(s), 0 skipped, ok" % (label, ran))
    say("total: %d test executions" % total)
    return 0 if failed == 0 else 1


def probe_ci_covers_runtime():
    """CI must run the shipped runtime, not only read the documents."""
    workflow = REPO / ".github" / "workflows" / "lint.yml"
    if not workflow.is_file():
        say("no workflow file")
        return 1
    text = workflow.read_text(encoding="utf-8")
    required = {
        "compiles every tracked .py": "py_compile",
        "runs the harness suite": "discover -s harness",
        "checks the Claude Code adapter": "generate.py --check",
        "runs the desktop self-test": "selftest.py",
        "initializes a real workspace": "init_product.py",
        "lints that workspace": "lint.py --workspace",
        "proves the workspace contract": "check_workspace_contract.py",
        "proves the harness is deletable": "rm -rf harness",
    }
    missing = [label for label, needle in required.items()
               if needle not in text]
    for label in missing:
        say("  CI does not: " + label)
    say("CI runtime coverage: %d of %d"
        % (len(required) - len(missing), len(required)))
    return 0 if not missing else 1


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
    """Prove the gates fail when the defect is reintroduced.

    A gate that has never been shown to fail is a gate nobody has tested. Each
    mutation is applied to a throwaway copy of the tree, never to this one.
    """
    import tempfile

    mutations = [
        ("a syntax error in the runtime",
         "harness/runner.py", lambda t: t + "\ndef broken(:\n",
         ["python3", "-m", "py_compile", "harness/runner.py"]),
        ("a route losing its kind",
         "harness/MANIFEST.json",
         lambda t: t.replace('"kind": "interactive",', "", 1),
         ["python3", "tools/check_manifest.py", "--quiet"]),
        ("a gate criterion removed",
         "modules/regulated/examples/dispute-summary/PRD.md",
         lambda t: t.replace("## 6. Review gate: sign-off requires",
                             "## 6. Notes", 1),
         ["python3", "lint.py",
          "modules/regulated/examples/dispute-summary/PRD.md"]),
        ("evidence unticked while Approved",
         "modules/regulated/examples/dispute-summary/PRD.md",
         lambda t: t.replace("**Status:** In review", "**Status:** Approved", 1),
         ["python3", "lint.py",
          "modules/regulated/examples/dispute-summary/PRD.md"]),
    ]

    caught, missed = 0, []
    with tempfile.TemporaryDirectory() as tmp:
        base = tracked_tree(Path(tmp) / "tree")
        for label, rel, mutate, command in mutations:
            target = base / rel
            original = target.read_text(encoding="utf-8")
            target.write_text(mutate(original), encoding="utf-8")
            code, _out = run(command, cwd=base)
            target.write_text(original, encoding="utf-8")
            for stale in base.rglob("__pycache__"):
                shutil.rmtree(stale, ignore_errors=True)
            if code == 0:
                missed.append(label)
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
