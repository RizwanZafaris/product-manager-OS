#!/usr/bin/env python3
"""Prove the runner and the initializer place a template in the same file.

    python3 tools/check_workspace_contract.py
    python3 tools/check_workspace_contract.py --quiet

Standard library only, like every other script in this tree.

Why this exists as its own check. The two writers into a product workspace,
`tools/init_product.py` and `harness/runner.py`, each used to answer "where
does this go" on its own. They agreed on most templates and disagreed on
thirteen. One of the disagreements was STATE.md: the runner filed it under
`execution/state.md` while every skill, prompt and adapter addresses it at the
workspace root, so a run could leave a second state file and a later resume
could read the wrong one. Nothing in the tree failed while that was true,
because nothing in the tree had ever asked the two of them the same question.

They now share `tools/workspace.py`, which is what makes the disagreement
impossible rather than merely absent. This script is the proof that the sharing
is still in place: it walks every template the manifest routes to and asserts
the two callers return the same path for each.

`harness/` is deletable by design, so a tree without it has no runner to
disagree with anything. That is a pass, reported as a skip, exactly as
`tools/check_manifest.py` treats the same case.

The two-caller comparison cannot see a change to the shared map itself: both
callers read it, so they agree on the new answer and the check stays green
while the artifact moves. On the shipped tree `harness/test_runner.py` catches
that, and on a tree with `harness/` deleted that suite is gone too. So this
script also asserts the destinations that skills, prompts and adapters address
by name against `CANONICAL_DESTINATIONS` below, and it runs that table on both
paths, deleted harness included.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "harness" / "MANIFEST.json"
SLUG = "contract-check"

# The destinations the rest of the tree addresses by name rather than by
# computing them. STATE.md is the one that matters: os/CONDUCTOR.md's resume
# protocol, every skill and every adapter look for it at the workspace root, so
# moving it leaves a resume reading a file that is not there.
CANONICAL_DESTINATIONS = {
    "templates/execution/state.md": "products/%s/STATE.md",
    "modules/regulated/templates/regulated-ai-prd-template.md":
        "products/%s/definition/ai/regulated-ai-prd.md",
}


def say(*parts):
    print(" ".join(str(p) for p in parts))


def named_templates():
    """Every template the manifest routes any task to."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    found = set()
    for task in manifest.get("tasks") or []:
        found.update(task.get("templates") or [])
    return sorted(found)


def canonical_problems(workspace, quiet):
    """Report every canonical destination the shared map no longer produces."""
    problems = 0
    for rel, shape in sorted(CANONICAL_DESTINATIONS.items()):
        expected = shape % SLUG
        path = REPO / rel
        if not path.is_file():
            say("MISSING  %s is addressed by name and does not exist." % rel)
            problems += 1
            continue
        try:
            got = workspace.destination_for(rel, SLUG,
                                            path.read_text(encoding="utf-8"))
        except workspace.WorkspaceError as error:
            say("REFUSED  %s has no computable destination: %s" % (rel, error))
            problems += 1
            continue
        if got != expected:
            say("MOVED    %s" % rel)
            say("           addressed by name at: %s" % expected)
            say("           computed:             %s" % got)
            problems += 1
        elif not quiet:
            say("  ok  %-52s -> %s" % (rel, got))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--quiet", action="store_true",
                        help="print only failures and the one-line verdict")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(REPO / "tools"))
    import workspace                                        # noqa: E402

    fixed = canonical_problems(workspace, args.quiet)

    if not (REPO / "harness").is_dir() or not MANIFEST.is_file():
        if fixed:
            say("")
            say("workspace contract: %d canonical destination(s) moved. There "
                "is no harness/ in this tree, so the runner disagrees with "
                "nothing, but the paths the rest of the tree addresses by name "
                "still have to be the paths the initializer writes." % fixed)
            return 1
        say("workspace contract: ok (%d canonical destination(s)). The "
            "two-writer comparison is skipped, this tree has no harness/. The "
            "harness is deletable by design and an absent runner disagrees "
            "with nothing." % len(CANONICAL_DESTINATIONS))
        return 0

    sys.path.insert(0, str(REPO / "harness"))
    import runner                                           # noqa: E402

    templates = named_templates()
    if not templates:
        say("workspace contract: the manifest names no templates, so there is "
            "nothing to check. That is itself suspicious.")
        return 1

    disagreed, refused, missing = [], [], []
    for rel in templates:
        path = REPO / rel
        if not path.is_file():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8")
        try:
            canonical = workspace.destination_for(rel, SLUG, text)
        except workspace.WorkspaceError as error:
            refused.append((rel, str(error)))
            continue
        try:
            got = runner.artifact_path(SLUG, path).relative_to(
                REPO).as_posix()
        except Exception as error:                          # noqa: BLE001
            refused.append((rel, str(error)))
            continue
        if got != canonical:
            disagreed.append((rel, canonical, got))
        elif not args.quiet:
            say("  ok  %-52s -> %s" % (rel, canonical))

    problems = fixed
    for rel in missing:
        say("MISSING  %s is routed to by the manifest and does not exist."
            % rel)
        problems += 1
    for rel, why in refused:
        say("REFUSED  %s has no computable destination: %s" % (rel, why))
        problems += 1
    for rel, canonical, got in disagreed:
        say("DIFFERS  %s" % rel)
        say("           initializer: %s" % canonical)
        say("           runner:      %s" % got)
        problems += 1

    if problems:
        say("")
        say("workspace contract: %d problem(s) across %d template(s). The two "
            "writers into a product workspace do not agree on where a filled "
            "artifact goes, which is how a workspace ends up with two state "
            "files and a resume that reads the wrong one."
            % (problems, len(templates)))
        return 1
    say("workspace contract: ok (%d templates, one destination each, %d of "
        "them addressed by name)" % (len(templates),
                                     len(CANONICAL_DESTINATIONS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
