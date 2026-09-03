#!/usr/bin/env python3
"""Compute the Complete PM OS readiness score by running the evidence.

    python3 tools/readiness.py
    python3 tools/readiness.py --json docs/readiness/scorecard.json
    python3 tools/readiness.py --category harness

Standard library only, like every other script in this tree.

The rule this file exists to enforce: a point is earned by a command that
exits 0 on this checkout, and by nothing else. A criterion in
docs/readiness/criteria.json either carries a verify command or it does not.
If it does, this script runs it and the exit code decides. If it does not, the
criterion scores zero and prints the task that would build it and the reason
it is not built. There is no status field a person can edit to raise the
score, no partial credit, and no credit for a document describing a
capability.

Every run records the commit it scored, whether the working tree was clean,
the interpreter, and the wall clock of each check, because a score without the
tree it was measured on is a number somebody typed.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CRITERIA = REPO / "docs" / "readiness" / "criteria.json"
DEFAULT_OUT = REPO / "docs" / "readiness" / "scorecard.json"

# A blocker whose text starts with this needs authority, credentials, money or
# a service this repository cannot provide for itself. It is reported apart
# from ordinary unbuilt work, because the two need different decisions.
EXTERNAL = "EXTERNAL:"


def say(*parts):
    print(" ".join(str(p) for p in parts))


def git(*args):
    done = subprocess.run(["git", *args], cwd=str(REPO), capture_output=True,
                          text=True)
    return done.stdout.strip() if done.returncode == 0 else ""


def run_verify(command, timeout=900):
    """Run one verify command. Returns (passed, exit code, seconds, tail)."""
    started = time.monotonic()
    try:
        done = subprocess.run(command, cwd=str(REPO), shell=True,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, None, time.monotonic() - started, "timed out"
    seconds = time.monotonic() - started
    output = ((done.stdout or "") + (done.stderr or "")).strip()
    return done.returncode == 0, done.returncode, seconds, output[-400:]


def score(selected=None):
    spec = json.loads(CRITERIA.read_text(encoding="utf-8"))
    dirty = bool(git("status", "--porcelain"))
    report = {
        "schema": 1,
        "generated": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "working_tree": "dirty" if dirty else "clean",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "categories": [],
        "earned": 0,
        "possible": 0,
        "verified_criteria": 0,
        "failed_criteria": 0,
        "unbuilt_criteria": 0,
        "external_blockers": [],
        "open_tasks": [],
    }

    for category in spec["categories"]:
        if selected and category["id"] != selected:
            continue
        block = {"id": category["id"], "title": category["title"],
                 "points": category["points"], "earned": 0, "criteria": []}
        say("")
        say("== %s (%d points)" % (category["title"], category["points"]))
        for criterion in category["criteria"]:
            entry = {"id": criterion["id"], "title": criterion["title"],
                     "points": criterion["points"]}
            command = criterion.get("verify")
            if command:
                passed, code, seconds, tail = run_verify(command)
                entry.update({"verify": command, "exit_code": code,
                              "seconds": round(seconds, 2),
                              "status": "green" if passed else "failing",
                              "earned": criterion["points"] if passed else 0})
                if not passed:
                    entry["output_tail"] = tail
                    report["failed_criteria"] += 1
                else:
                    report["verified_criteria"] += 1
                say("  [%s] %-6s %2d/%-2d  %s  (%.1fs)"
                    % ("PASS" if passed else "FAIL", criterion["id"],
                       entry["earned"], criterion["points"],
                       criterion["title"][:66], seconds))
                if not passed:
                    say("           exit %s: %s" % (code, tail.splitlines()[-1]
                                                    if tail else "no output"))
            else:
                blocker = criterion.get("blocker", "not implemented")
                external = blocker.startswith(EXTERNAL)
                entry.update({"status": "external-blocker" if external
                              else "unbuilt",
                              "earned": 0,
                              "task": criterion.get("task"),
                              "blocker": blocker})
                report["unbuilt_criteria"] += 1
                if external:
                    report["external_blockers"].append(criterion["id"])
                if criterion.get("task"):
                    report["open_tasks"].append(criterion["task"])
                say("  [%s] %-6s  0/%-2d  %s"
                    % ("EXT " if external else "TODO", criterion["id"],
                       criterion["points"], criterion["title"][:66]))
                say("           %s %s" % (criterion.get("task") or "-",
                                          blocker[:110]))
            block["earned"] += entry["earned"]
            block["criteria"].append(entry)
        block["shortfall"] = block["points"] - block["earned"]
        say("  -- %s: %d/%d" % (category["id"], block["earned"],
                                block["points"]))
        report["categories"].append(block)
        report["earned"] += block["earned"]
        report["possible"] += block["points"]

    report["open_tasks"] = sorted(set(report["open_tasks"]))

    # Hard gates override the number. Each one is a fact about this run, not a
    # judgment, so it is computed rather than asserted.
    report["hard_gates"] = {
        "every_verifiable_criterion_passes": report["failed_criteria"] == 0,
        "no_unbuilt_criteria": report["unbuilt_criteria"] == 0,
        "no_external_blockers": not report["external_blockers"],
        "working_tree_clean": not dirty,
    }
    report["all_hard_gates_green"] = all(report["hard_gates"].values())
    report["verdict"] = (
        "COMPLETE PM OS READINESS: %d/%d — ALL HARD GATES GREEN"
        % (report["earned"], report["possible"])
        if report["all_hard_gates_green"] and
        report["earned"] == report["possible"] else
        "COMPLETE PM OS READINESS: NOT %d/%d — %s"
        % (report["possible"],
           report["possible"],
           "BLOCKED" if report["external_blockers"] and
           report["failed_criteria"] == 0 and
           report["unbuilt_criteria"] == len(report["external_blockers"])
           else "WORK REMAINS"))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", metavar="PATH", default=str(DEFAULT_OUT),
                        help="where to write the machine-readable scorecard")
    parser.add_argument("--category", help="score one category and stop")
    parser.add_argument("--no-write", action="store_true",
                        help="print the score and write no file")
    args = parser.parse_args(argv)

    report = score(args.category)

    say("")
    say("=" * 72)
    say("SCORE: %d / %d" % (report["earned"], report["possible"]))
    say("  verified by a passing command : %d criteria"
        % report["verified_criteria"])
    say("  failing                       : %d criteria"
        % report["failed_criteria"])
    say("  not built                     : %d criteria"
        % report["unbuilt_criteria"])
    say("  external blockers             : %s"
        % (", ".join(report["external_blockers"]) or "none"))
    say("  open tasks                    : %s"
        % (", ".join(report["open_tasks"]) or "none"))
    say("")
    for name, ok in report["hard_gates"].items():
        say("  hard gate %-38s %s" % (name, "GREEN" if ok else "NOT GREEN"))
    say("")
    say(report["verdict"])
    say("  measured on %s (%s tree) with Python %s"
        % (report["commit"][:12] or "unknown", report["working_tree"],
           report["python"]))

    if not args.no_write and not args.category:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        say("  scorecard written to %s"
            % out.relative_to(REPO) if out.is_relative_to(REPO) else out)
    return 0 if report["all_hard_gates_green"] else 1


if __name__ == "__main__":
    sys.exit(main())
