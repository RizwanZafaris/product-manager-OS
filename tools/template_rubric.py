#!/usr/bin/env python3
"""Score every template against the flagship bar, derived from prd.md.

    python3 tools/template_rubric.py
    python3 tools/template_rubric.py --json docs/readiness/template-rubric.json
    python3 tools/template_rubric.py --min 70          # gate mode: fail below

Standard library only, like every other script in this tree.

Why this exists. "Every template should be as good as the PRD" is a real
instruction and an unmeasurable one, so this file turns it into a score a
command produces. The bar is not invented here: it is read off
templates/definition/prd.md, which is the document the rest of the tree is
being held to, and every dimension below is something that document does and
the median template does not.

What flagship is NOT. It is not length. A decision log is legitimately shorter
than a PRD and padding it would make it worse, so nothing here rewards lines
for their own sake. Depth is scored against the template's own section count,
which is a measure of whether each section was actually written out or merely
named.

The seven dimensions, and what each one catches:

1. self-explaining   Every section carries a guidance comment saying what goes
                     in it and what a bad answer looks like. The PRD has one
                     per section. A template whose sections are bare headings
                     is a form, and a form teaches nobody.
2. worked example    At least one filled example, marked ILLUSTRATIVE so it can
                     never be mistaken for real evidence. Without one, the
                     first user invents the format and the second disagrees.
3. exit gate         Names the gate it feeds and what must be true to pass. A
                     document that does not know where it goes cannot be
                     checked by anyone downstream.
4. fillable          Has fill-in fields. A template with none is prose.
5. structured        Uses a table wherever it enumerates, because a list of
                     rows with no columns is where owners and dates go missing.
6. traceable         Links or ID-references sibling artifacts. The stack works
                     only if a criterion can name the story it verifies.
7. failure-aware     Names the trap, the failure mode, or what a bad answer
                     looks like. This is the dimension that separates this
                     tree's templates from a generic template pack, and it is
                     the one most often missing.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "templates"
REFERENCE = TEMPLATES / "definition" / "prd.md"

H2_RE = re.compile(r"^##\s+\S", re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TABLE_ROW_RE = re.compile(r"^\|", re.M)
# A fill-in field, in either convention this tree sanctions. lint.py accepts
# both [square] and <angle> fields, and the first version of this rubric
# counted only the first, so a template written entirely in angle fields
# scored near zero on fillable. It also counted the visible text of a markdown
# link as a field, because [knowledge index](...) matches a bare square
# pattern. Both errors are corrected here: a square field is one NOT followed
# by an opening parenthesis, and angle fields count too.
FIELD_RE = re.compile(r"\[[a-z][^\]]{2,}\](?!\()|<[A-Za-z0-9][^<>]{2,}>")
LINK_RE = re.compile(r"\]\(\s*(?:<[^<>\n]*>|[^\s()]*)")
# Two conventions exist in this tree for marking a filled example, and the
# first version of this rubric recognised only one. That produced false
# negatives: dependency-register.md carries a fully worked row and says "the
# example row shows the precision expected", and was scored as having no
# example at all. Measured across the tree: 46 files use the ILLUSTRATIVE
# convention, 14 use different wording, 38 genuinely have none. Recognising
# both is the honest instrument; making the tree use one of them is a separate
# and worthwhile fix.
ILLUSTRATIVE_RE = re.compile(
    r"illustrative|worked (micro-)?example|the example row|example row shows"
    r"|delete (?:it|the example|this row)|sample row", re.I)
EXIT_GATE_RE = re.compile(r"^##\s*Exit gate", re.M | re.I)
# The vocabulary this tree uses when it tells you how a thing goes wrong.
FAILURE_RE = re.compile(
    r"\btrap\b|\bfails?\b|failure mode|bad answer|goes wrong|how it lies|"
    r"skip it when|do not\b|never\b|is not a\b|red flag|smell\b",
    re.I)

WEIGHTS = {
    "self_explaining": 25,
    "failure_aware": 20,
    "worked_example": 15,
    "exit_gate": 15,
    "structured": 10,
    "traceable": 10,
    "fillable": 5,
}


def sections_with_guidance(text):
    """How many h2 sections are followed by a guidance comment before the next.

    Measured per section rather than by counting comments anywhere, because a
    template can carry one long preamble comment and leave twelve sections
    unexplained, and that is the shape this dimension exists to catch.
    """
    parts = re.split(r"(?m)^##\s+", text)
    if len(parts) < 2:
        return 0, 0
    bodies = parts[1:]
    explained = sum(1 for body in bodies if "<!--" in body)
    return explained, len(bodies)


def score_template(path):
    # Accept a relative path from the command line as well as an absolute one.
    path = Path(path)
    if not path.is_absolute():
        path = (REPO / path).resolve()
    text = path.read_text(encoding="utf-8")
    stripped = COMMENT_RE.sub("", text)
    explained, total_sections = sections_with_guidance(text)
    lines = len(text.splitlines())

    marks = {}
    # 1. Every section explains itself.
    marks["self_explaining"] = (explained / total_sections) if total_sections else 0.0
    # 2. A worked example, marked so it cannot be mistaken for evidence.
    marks["worked_example"] = 1.0 if ILLUSTRATIVE_RE.search(text) else 0.0
    # 3. An exit gate that names where the output goes.
    marks["exit_gate"] = 1.0 if EXIT_GATE_RE.search(text) else 0.0
    # 4. Fields to fill. Saturates quickly: ten is plenty to prove the point.
    fields = len(FIELD_RE.findall(stripped))
    marks["fillable"] = min(fields / 10.0, 1.0)
    # 5. Tables where it enumerates. Six rows is a real table.
    rows = len(TABLE_ROW_RE.findall(stripped))
    marks["structured"] = min(rows / 6.0, 1.0)
    # 6. References its siblings. Four links is a document wired into a stack.
    links = len(LINK_RE.findall(stripped))
    marks["traceable"] = min(links / 4.0, 1.0)
    # 7. Says how it goes wrong. Scaled per section, because one warning in a
    #    sixteen-section document is not a failure-aware document.
    warnings = len(FAILURE_RE.findall(text))
    marks["failure_aware"] = min(warnings / max(total_sections, 4), 1.0)

    score = sum(WEIGHTS[k] * v for k, v in marks.items())
    return {
        "path": path.relative_to(REPO).as_posix(),
        "lines": lines,
        "sections": total_sections,
        "sections_explained": explained,
        "fields": fields,
        "table_rows": rows,
        "links": links,
        "warnings": warnings,
        "marks": {k: round(v, 3) for k, v in marks.items()},
        "score": round(score, 1),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", metavar="PATH",
                        help="write the machine-readable report here")
    parser.add_argument("--min", type=float,
                        help="exit 1 if any template scores below this")
    parser.add_argument("--top", type=int, default=25,
                        help="how many of the weakest to print (default 25)")
    parser.add_argument("--path", help="score one file and stop")
    args = parser.parse_args(argv)

    if args.path:
        report = score_template(Path(args.path))
        print(json.dumps(report, indent=2))
        return 0

    reference = score_template(REFERENCE)
    scored = sorted(
        (score_template(p) for p in sorted(TEMPLATES.rglob("*.md"))
         if p.name != "README.md"),
        key=lambda r: r["score"])

    values = [r["score"] for r in scored]
    print("flagship rubric, bar read off %s"
          % REFERENCE.relative_to(REPO).as_posix())
    print("  reference score : %.1f  (%d lines, %d sections, %d explained)"
          % (reference["score"], reference["lines"], reference["sections"],
             reference["sections_explained"]))
    print("  templates       : %d" % len(scored))
    print("  median score    : %.1f" % statistics.median(values))
    print("  mean score      : %.1f" % statistics.mean(values))
    for threshold in (90, 75, 60):
        print("  at or above %-3d : %d" % (threshold,
                                           sum(1 for v in values if v >= threshold)))
    print("")
    print("weakest %d:" % min(args.top, len(scored)))
    print("  %-52s %6s %6s %5s %s" % ("template", "score", "lines", "sec",
                                      "biggest gap"))
    for row in scored[:args.top]:
        worst = min(row["marks"], key=lambda k: row["marks"][k] * WEIGHTS[k]
                    if row["marks"][k] < 1 else 99)
        print("  %-52s %6.1f %6d %5d %s"
              % (row["path"], row["score"], row["lines"], row["sections"],
                 worst.replace("_", " ")))

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "schema": 1,
            "reference": reference,
            "weights": WEIGHTS,
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "templates": scored,
        }, indent=2) + "\n", encoding="utf-8")
        print("")
        # An output path outside the repository is a legitimate thing to
        # ask for, and relative_to raises on one. Report what was written.
        try:
            shown = out.relative_to(REPO).as_posix()
        except ValueError:
            shown = str(out)
        print("written to %s" % shown)

    if args.min is not None:
        below = [r for r in scored if r["score"] < args.min]
        print("")
        if below:
            print("%d template(s) below the %.0f bar. The weakest is %s at %.1f."
                  % (len(below), args.min, below[0]["path"], below[0]["score"]))
            return 1
        print("every template is at or above %.0f." % args.min)
    return 0


if __name__ == "__main__":
    sys.exit(main())
