#!/usr/bin/env python3
"""Check the documents a product manager actually builds, against the bar.

    python3 tools/pm_working_set.py
    python3 tools/pm_working_set.py --min 75      # gate mode
    python3 tools/pm_working_set.py --json docs/readiness/pm-working-set.json

Standard library only, like every other script in this tree.

Why this file exists, separately from tools/template_rubric.py. The rubric
scores all ninety-eight templates equally, and they are not equal. A sunset
plan is written once in a product's life; a decision log is written every
week. A tree whose median score is respectable can still be weak in exactly
the documents a person touches on a Tuesday, and that is the failure this
check is built to catch.

Where the list comes from. It is the convergent set across five independent
practitioner sources on what a product manager writes, keeping only what
appeared in three or more of them, with cadence taken from practitioner
reports rather than from a framework. It is deliberately not the whole
templates directory and it is deliberately not this repository's own opinion
of what matters, because a repository grading its own priorities proves
nothing.

The cadence column is the point. It is what turns "this template is weak" into
"this template is weak and it is written every week", which is a different
sentence and a different priority.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

from template_rubric import score_template                 # noqa: E402

# (document, how often a PM touches it, template path or None)
#
# "None" is not a gap in the list. It is a gap in the tree, and it is reported
# as one, because the two documents most frequently updated by practitioners
# were the two this repository had no template for.
WORKING_SET = [
    ("Product roadmap", "biweekly", "templates/planning/roadmap.md"),
    ("PRD or spec", "per feature", "templates/definition/prd.md"),
    ("User stories", "very often", "templates/definition/user-stories.md"),
    ("Backlog", "very often", "templates/execution/backlog.md"),
    ("Acceptance criteria", "per story",
     "templates/definition/acceptance-criteria.md"),
    ("One-pager or proposal", "per idea", "templates/definition/one-pager.md"),
    ("Business case", "per bet", "templates/planning/business-case.md"),
    ("OKRs", "quarterly", "templates/planning/okrs.md"),
    ("Product strategy", "annual", "templates/planning/product-strategy.md"),
    ("Vision", "rare", "templates/planning/vision.md"),
    ("Personas", "per segment", "templates/discovery/personas.md"),
    ("Competitive analysis", "frequent",
     "templates/discovery/competitive-analysis.md"),
    ("Customer journey map", "per feature",
     "templates/discovery/journey-map.md"),
    ("Release readiness", "per release",
     "templates/delivery/release-readiness.md"),
    ("Release notes", "every few weeks", "templates/delivery/release-notes.md"),
    ("GTM plan", "per launch", "templates/planning/gtm-plan.md"),
    ("Stakeholder update", "weekly", "templates/planning/exec-update.md"),
    ("Post-launch review", "per launch",
     "templates/operate/post-launch-review.md"),
    ("Risk register", "weekly", "templates/execution/risk-register.md"),
    ("Decision log", "continuous", "templates/execution/decision-log.md"),
    ("Experiment brief", "per test", "templates/operate/experiment-brief.md"),
    ("Metrics review", "monthly", "templates/operate/metrics-review.md"),
]

# How often a document is written, as a rough weight. A weak template that is
# written continuously costs more than a weak one written once a year, and the
# shortfall total below is weighted by this so the ranking matches the cost.
CADENCE_WEIGHT = {
    "continuous": 5, "very often": 5, "weekly": 4, "biweekly": 3,
    "per story": 3, "per feature": 3, "frequent": 3, "monthly": 2,
    "per test": 2, "per release": 2, "per launch": 2, "every few weeks": 2,
    "per idea": 2, "per bet": 1, "per segment": 1, "quarterly": 1,
    "annual": 1, "rare": 1,
}


def say(*parts):
    print(" ".join(str(p) for p in parts))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--min", type=float,
                        help="exit 1 if any document in the set scores below")
    parser.add_argument("--json", metavar="PATH",
                        help="write the machine-readable report here")
    args = parser.parse_args(argv)

    rows, missing = [], []
    for name, cadence, rel in WORKING_SET:
        if rel is None or not (REPO / rel).is_file():
            missing.append({"document": name, "cadence": cadence,
                            "template": rel, "status": "no template"})
            continue
        scored = score_template(REPO / rel)
        rows.append({"document": name, "cadence": cadence, "template": rel,
                     "score": scored["score"],
                     "weight": CADENCE_WEIGHT.get(cadence, 1),
                     "marks": scored["marks"]})

    say("the PM working set: what a product manager builds in normal conditions")
    say("")
    say("  %-24s %-16s %6s  %s" % ("document", "cadence", "score", "template"))
    say("  " + "-" * 86)
    for row in sorted(rows, key=lambda r: (-r["weight"], r["score"])):
        flag = "" if row["score"] >= 90 else (
            "  weak" if row["score"] < 75 else "  below flagship")
        say("  %-24s %-16s %6.1f  %s%s"
            % (row["document"], row["cadence"], row["score"], row["template"],
               flag))
    for gap in missing:
        say("  %-24s %-16s %6s  NO TEMPLATE"
            % (gap["document"], gap["cadence"], "--"))

    scores = [r["score"] for r in rows]
    # Weighted shortfall: how far the set is from flagship, counting the
    # documents a person writes often more heavily than the ones they do not.
    shortfall = sum((100 - r["score"]) * r["weight"] for r in rows)
    say("")
    say("  documents in the set : %d" % len(WORKING_SET))
    say("  with a template      : %d" % len(rows))
    say("  missing entirely     : %d%s"
        % (len(missing),
           "  (" + ", ".join(g["document"] for g in missing) + ")"
           if missing else ""))
    say("  median score         : %.1f" % statistics.median(scores))
    say("  at or above 90       : %d" % sum(1 for s in scores if s >= 90))
    say("  below 75             : %d" % sum(1 for s in scores if s < 75))
    say("  weighted shortfall   : %d  (lower is better; weighted by cadence)"
        % shortfall)

    worst = sorted(rows, key=lambda r: -((100 - r["score"]) * r["weight"]))[:5]
    say("")
    say("  costliest to leave weak, by cadence times shortfall:")
    for row in worst:
        say("    %-24s %-16s %5.1f  (weight %d)"
            % (row["document"], row["cadence"], row["score"], row["weight"]))

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "schema": 1, "documents": rows, "missing": missing,
            "median": statistics.median(scores),
            "weighted_shortfall": shortfall,
        }, indent=2) + "\n", encoding="utf-8")
        say("")
        try:
            say("  written to %s" % out.relative_to(REPO).as_posix())
        except ValueError:
            say("  written to %s" % out)

    if args.min is not None:
        below = [r for r in rows if r["score"] < args.min]
        say("")
        if missing:
            say("%d document(s) in the working set have no template at all."
                % len(missing))
            return 1
        if below:
            say("%d document(s) below the %.0f bar, weakest %s at %.1f."
                % (len(below), args.min,
                   min(below, key=lambda r: r["score"])["document"],
                   min(r["score"] for r in below)))
            return 1
        say("every document in the working set is at or above %.0f." % args.min)
    return 0


if __name__ == "__main__":
    sys.exit(main())
