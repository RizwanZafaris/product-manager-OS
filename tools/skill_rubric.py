#!/usr/bin/env python3
"""Score prose skills against the contract skills themselves already use.

    python3 tools/skill_rubric.py
    python3 tools/skill_rubric.py --min 6
    python3 tools/skill_rubric.py --json docs/readiness/skill-rubric.json

Standard library only, like every other script in this tree.

Why this is not tools/template_rubric.py. A template is a form somebody fills
in, so it is judged on whether each section explains itself, carries a worked
example, and names how the document goes wrong. A skill is a procedure
somebody follows. Demanding a filled worked example in all of them would have
been the same mistake the template rubric already caught once with
templates/execution/state.md: the score improves and the file gets worse.

The bar is read off the skills, not invented. Counting sections across the
thirty-five prose skills in this tree produced a clear shared vocabulary, and
the seven below are what the strongest of them carry:

    28/35  Files this skill drives
    28/35  When to use
    28/35  Exit gate
    27/35  Workflow
    24/35  Output format
    22/35  Inputs
    18/35  Failure modes this skill guards against

That last one matters. Skills already have their own convention for naming how
the work goes wrong, and it is a named section rather than a table bolted on.
Eighteen of thirty-five carry it, which is the single largest gap in the layer
and the one worth closing first.

What is deliberately out of scope. skills/runtime/ holds a different artifact
entirely: short machine-facing entries whose contract lives in contract.json
and SKILL.graph.yml beside them, validated by pmos/skills.py against a schema
and a mandatory-asset list. They carry none of the seven sections because they
are not prose procedures, and scoring them here would report a real thing as
broken while a stricter check already passes on it.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"

# The contract, in the order a reader meets it.
SECTIONS = (
    "Files this skill drives",
    "When to use",
    "Inputs",
    "Workflow",
    "Output format",
    "Failure modes this skill guards against",
    "Exit gate",
)

# Headings that carry a contract element under a different name. These are
# recognised rather than renamed, because in every case here the local name is
# more informative than the generic one: "The method: six passes, in order"
# tells a reader how many passes there are and that order matters, which
# "Workflow" does not. Forcing the rename would score better and read worse,
# which is the failure this whole family of rubrics keeps having to avoid.
#
# They are reported as aliases rather than silently accepted, so the naming
# inconsistency stays visible to anyone who wants to settle it.
ALIASES = {
    "Workflow": ("The method: six passes, in order", "The walk", "The method"),
    "Output format": ("Output shape",),
    "Inputs": ("Inputs and preconditions",),
}


# Not prose skills. Their contract is machine-readable and lives beside them,
# and pmos/skills.py validates it against a schema and a mandatory-asset list.
EXEMPT_PREFIXES = ("skills/runtime/",)

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
# Skills number their workflow with h3 headings, "### 1. Fix the decision",
# not with list items. The first version of this file counted list items only
# and reported well-formed skills as having zero steps. Both forms count.
NUMBERED_STEP_RE = re.compile(r"^###\s*\d+\.\s+\S|^\s*\d+\.\s+\S", re.M)
LINK_RE = re.compile(r"\]\(\s*(?:<[^<>\n]*>|[^\s()]*)")


def is_exempt(rel):
    return any(rel.startswith(prefix) for prefix in EXEMPT_PREFIXES)


def score_skill(path):
    rel = Path(path).resolve().relative_to(REPO.resolve()).as_posix()
    text = Path(path).read_text(encoding="utf-8")
    headings = [h.strip() for h in HEADING_RE.findall(text)]
    def found(section):
        if section in headings:
            return section
        for alias in ALIASES.get(section, ()):
            if alias in headings:
                return alias
        return None

    resolved = {s: found(s) for s in SECTIONS}
    present = [s for s in SECTIONS if resolved[s]]
    missing = [s for s in SECTIONS if not resolved[s]]
    aliased = {s: resolved[s] for s in SECTIONS
               if resolved[s] and resolved[s] != s}

    body = {}
    parts = re.split(r"(?m)^##\s+", text)
    for chunk in parts[1:]:
        name = chunk.split("\n", 1)[0].strip()
        body[name] = chunk

    # Two checks beyond presence, because a section that exists and says
    # nothing is the failure a heading count cannot see.
    workflow = body.get(resolved.get("Workflow") or "Workflow", "")
    numbered = len(NUMBERED_STEP_RE.findall(workflow))
    # A skill's exit gate is prose that names the conditions under which the
    # work is not done, not a checkbox list. Counting "- [ ]" here reported
    # every skill in the tree as hollow, which was a fact about this file
    # rather than about the skills. What is measured instead is whether the
    # gate says anything: a gate of one sentence that names no condition is
    # the failure worth catching.
    gate = body.get(resolved.get("Exit gate") or "Exit gate", "")
    gate_boxes = gate.count("- [ ]")
    gate_words = len(gate.split())
    failures = body.get(
        resolved.get("Failure modes this skill guards against")
        or "Failure modes this skill guards against", "")
    failure_items = len(re.findall(r"^\s*[-*]\s+\*\*", failures, re.M)) or \
        len(re.findall(r"^\s*[-*]\s+\S", failures, re.M))
    links = len(LINK_RE.findall(text))

    return {
        "path": rel,
        "sections_present": len(present),
        "missing": missing,
        "aliased": aliased,
        "workflow_steps": numbered,
        "exit_gate_boxes": gate_boxes,
        "exit_gate_words": gate_words,
        "failure_modes": failure_items,
        "links": links,
        "lines": len(text.splitlines()),
    }


def say(*parts):
    print(" ".join(str(p) for p in parts))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--min", type=int, metavar="N",
                        help="exit 1 if any prose skill carries fewer than N "
                             "of the seven sections")
    parser.add_argument("--json", metavar="PATH")
    parser.add_argument("--path", help="score one skill and stop")
    args = parser.parse_args(argv)

    if args.path:
        print(json.dumps(score_skill(args.path), indent=2))
        return 0

    everything = [score_skill(p) for p in sorted(SKILLS.rglob("SKILL.md"))]
    exempt = [r for r in everything if is_exempt(r["path"])]
    scored = sorted((r for r in everything if not is_exempt(r["path"])),
                    key=lambda r: (r["sections_present"], r["path"]))

    counts = [r["sections_present"] for r in scored]
    say("skill rubric, contract read off the skills themselves")
    say("  prose skills scored : %d" % len(scored))
    say("  exempt              : %d (skills/runtime/, machine contracts "
        "validated by pmos/skills.py)" % len(exempt))
    say("  carrying all seven  : %d" % sum(1 for c in counts if c == 7))
    say("  median sections     : %.1f of 7" % statistics.median(counts))
    say("")
    say("  the seven, and how many prose skills carry each:")
    for section in SECTIONS:
        have = sum(1 for r in scored if section not in r["missing"])
        say("    %-44s %d/%d" % (section, have, len(scored)))

    alias_users = [r for r in scored if r.get("aliased")]
    if alias_users:
        say("")
        say("  %d skill(s) carry a section under a different heading:"
            % len(alias_users))
        for row in alias_users:
            for canonical, actual in row["aliased"].items():
                say("    %-38s %s -> %s"
                    % (row["path"].replace("skills/", "").replace(
                        "/SKILL.md", ""), canonical, actual))

    weak = [r for r in scored if r["sections_present"] < 7]
    if weak:
        say("")
        say("  %d skill(s) below the full contract:" % len(weak))
        for row in weak:
            say("    %d/7  %-38s missing: %s"
                % (row["sections_present"],
                   row["path"].replace("skills/", "").replace("/SKILL.md", ""),
                   ", ".join(row["missing"])[:60]))

    # A section can be present and empty. These are the two that matter most.
    hollow = [r for r in scored
              if ("Workflow" not in r["missing"] and r["workflow_steps"] < 3)
              or ("Exit gate" not in r["missing"] and r["exit_gate_words"] < 25)]
    if hollow:
        say("")
        say("  %d skill(s) with a section that is present and thin:" % len(hollow))
        for row in hollow:
            say("    %-38s workflow steps %d, exit-gate words %d"
                % (row["path"].replace("skills/", "").replace("/SKILL.md", ""),
                   row["workflow_steps"], row["exit_gate_words"]))

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {"schema": 1, "sections": list(SECTIONS),
             "skills": scored, "exempt": [r["path"] for r in exempt]},
            indent=2) + "\n", encoding="utf-8")
        say("")
        try:
            say("  written to %s" % out.relative_to(REPO).as_posix())
        except ValueError:
            say("  written to %s" % out)

    if args.min is not None:
        below = [r for r in scored if r["sections_present"] < args.min]
        say("")
        if below:
            say("%d prose skill(s) carry fewer than %d of the seven sections."
                % (len(below), args.min))
            return 1
        say("every prose skill carries at least %d of the seven." % args.min)
    return 0


if __name__ == "__main__":
    sys.exit(main())
