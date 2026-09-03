#!/usr/bin/env python3
"""Measure local PM OS readiness from fixed, executable evidence.

    python3 tools/readiness.py
    python3 tools/readiness.py --output /tmp/pmos-scorecard.json
    python3 tools/readiness.py --category workspace

The rubric allocates points but never contains executable commands. Every
verifier id resolves through readiness_registry to argv-only steps. Filtered
unit-test evidence is accepted only when every exact test id runs, the count
is positive and exact, and there are no skips or expected failures.

The default is stdout only. A generated scorecard must be explicitly written
outside the repository or to an ignored path; a committed "current" scorecard
would become stale in the commit that records it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from readiness_registry import REGISTRY

REPO = Path(__file__).resolve().parent.parent
CRITERIA = REPO / "docs" / "readiness" / "criteria.json"
TASKS = REPO / "docs" / "readiness" / "task-ledger.json"
EXTERNAL_GATES = REPO / "docs" / "readiness" / "external-gates.json"
REGISTRY_FILE = Path(__file__).with_name("readiness_registry.py")
EXTERNAL = "EXTERNAL:"

TASK_REQUIRED_FIELDS = frozenset({
    "id", "title", "status", "owns", "owns_hard_gates", "depends_on",
    "risk", "outcome", "scope", "non_goals", "acceptance",
    "owned_files", "failure_cases", "executor_capabilities",
    "reviewer_capabilities", "acceptance_verifiers", "evidence_paths",
    "attempt_count", "last_failure_class", "next_action",
})
TASK_STATUSES = frozenset({"planned", "running", "blocked", "green"})
TASK_RISKS = frozenset({"low", "medium", "high", "critical"})
OWNABLE_HARD_GATES = frozenset({"local_review_record_complete"})

# These are local engineering gates. External evidence is deliberately
# reported in a separate lane and can never be manufactured by a local test.
LOCAL_HARD_GATE_VERIFIERS = {
    "thirteen_use_cases_green": ("usecase-matrix",),
    "routes_executable": ("manifest-contract", "harness-route-behavior"),
    "ci_parity_green": ("ci-runtime",),
    "process_fault_suite_green": ("store-crash-recovery",),
    "links_green": ("workspace-links", "workspace-drift", "link-grammar"),
    "security_green": ("secret-boundaries", "security-policy"),
    "local_review_record_complete": ("independent-review",),
    "documentation_claims_match": ("docs-contract",),
}


class ReadinessError(Exception):
    """The evaluator cannot safely or meaningfully produce a verdict."""


def say(*parts):
    print(" ".join(str(p) for p in parts))


def git(*args):
    done = subprocess.run(["git", *args], cwd=str(REPO), shell=False,
                          capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def clean_env():
    """Minimal deterministic child environment with credentials removed."""
    allowed = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR", "TEMP",
               "TMP", "SYSTEMROOT")
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    return env


def validate(spec, ledger):
    """Return every rubric/ledger defect; execute nothing when nonempty."""
    errors = []
    top_fields = {"schema", "title", "note", "categories"}
    category_fields = {"id", "title", "points", "criteria"}
    criterion_fields = {"id", "title", "points", "verifier", "task",
                        "blocker"}
    unknown = set(spec) - top_fields
    if unknown:
        errors.append("criteria has unknown top-level fields: %s" %
                      ", ".join(sorted(unknown)))
    if spec.get("schema") != 2:
        errors.append("criteria schema must be 2")
    categories = spec.get("categories")
    if not isinstance(categories, list) or not categories:
        errors.append("criteria categories must be a nonempty list")
        categories = []

    category_ids, criterion_ids = set(), set()
    criterion_by_id = {}
    total = 0
    for category in categories:
        if not isinstance(category, dict):
            errors.append("each category must be an object")
            continue
        extra = set(category) - category_fields
        if extra:
            errors.append("category %r has unknown fields: %s" %
                          (category.get("id"), ", ".join(sorted(extra))))
        cid = category.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append("every category needs a nonempty string id")
        elif cid in category_ids:
            errors.append("duplicate category id %s" % cid)
        category_ids.add(cid)
        points = category.get("points")
        if not isinstance(points, int) or isinstance(points, bool) or points <= 0:
            errors.append("category %s points must be a positive integer" % cid)
            points = 0
        rows = category.get("criteria")
        if not isinstance(rows, list) or not rows:
            errors.append("category %s criteria must be a nonempty list" % cid)
            rows = []
        subtotal = 0
        for criterion in rows:
            if not isinstance(criterion, dict):
                errors.append("category %s contains a non-object criterion" % cid)
                continue
            extra = set(criterion) - criterion_fields
            if extra:
                errors.append("criterion %r has unknown fields: %s" %
                              (criterion.get("id"), ", ".join(sorted(extra))))
            rid = criterion.get("id")
            if not isinstance(rid, str) or not rid:
                errors.append("every criterion needs a nonempty string id")
                continue
            if rid in criterion_ids:
                errors.append("duplicate criterion id %s" % rid)
            criterion_ids.add(rid)
            criterion_by_id[rid] = criterion
            value = criterion.get("points")
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append("criterion %s points must be a positive integer" % rid)
                value = 0
            subtotal += value
            verifier = criterion.get("verifier")
            task = criterion.get("task")
            blocker = criterion.get("blocker")
            if verifier:
                if task is not None or blocker is not None:
                    errors.append("criterion %s mixes a verifier with task/blocker" %
                                  rid)
                if verifier not in REGISTRY:
                    errors.append("criterion %s names unknown verifier %r" %
                                  (rid, verifier))
            else:
                if not isinstance(task, str) or not task:
                    errors.append("unbuilt criterion %s needs a task" % rid)
                if not isinstance(blocker, str) or not blocker:
                    errors.append("unbuilt criterion %s needs a blocker" % rid)
        if subtotal != points:
            errors.append("category %s allocates %d points but its criteria sum "
                          "to %d" % (cid, points, subtotal))
        total += points
    if total != 100:
        errors.append("criteria must allocate exactly 100 points, got %d" % total)

    ledger_fields = {"schema", "title", "note", "baseline", "tasks"}
    task_fields = {
        "id", "title", "status", "owns", "owns_hard_gates",
        "depends_on", "risk", "estimate_weeks", "outcome", "scope",
        "non_goals", "acceptance", "note", "evidence", "blocked_by",
        "owned_files", "failure_cases", "executor_capabilities",
        "reviewer_capabilities", "acceptance_verifiers", "evidence_paths",
        "attempt_count", "last_failure_class", "next_action",
    }
    extra = set(ledger) - ledger_fields
    if extra:
        errors.append("task ledger has unknown fields: %s" %
                      ", ".join(sorted(extra)))
    if ledger.get("schema") != 2:
        errors.append("task ledger schema must be 2")
    tasks = ledger.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("task ledger tasks must be a nonempty list")
        tasks = []
    task_ids, owners, hard_owners, dependencies = set(), {}, {}, {}
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("task ledger contains a non-object task")
            continue
        extra = set(task) - task_fields
        if extra:
            errors.append("task %r has unknown fields: %s" %
                          (task.get("id"), ", ".join(sorted(extra))))
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            errors.append("every task needs a nonempty string id")
            continue
        if task_id in task_ids:
            errors.append("duplicate task id %s" % task_id)
        task_ids.add(task_id)
        missing = TASK_REQUIRED_FIELDS - set(task)
        if missing:
            errors.append("task %s misses required fields: %s" %
                          (task_id, ", ".join(sorted(missing))))
        if task.get("status") not in TASK_STATUSES:
            errors.append("task %s has invalid status" % task_id)
        if task.get("risk") not in TASK_RISKS:
            errors.append("task %s has invalid risk" % task_id)
        if not isinstance(task.get("attempt_count"), int) or \
                isinstance(task.get("attempt_count"), bool) or \
                task.get("attempt_count", -1) < 0:
            errors.append("task %s attempt_count must be a nonnegative integer" %
                          task_id)
        for field in ("scope", "non_goals", "owned_files", "failure_cases",
                      "executor_capabilities", "reviewer_capabilities",
                      "acceptance_verifiers", "evidence_paths"):
            if not isinstance(task.get(field), list):
                errors.append("task %s field %s must be a list" %
                              (task_id, field))
        deps = task.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append("task %s depends_on must be a list" % task_id)
            deps = []
        dependencies[task_id] = deps
        owned = task.get("owns", [])
        hard = task.get("owns_hard_gates", [])
        if not isinstance(owned, list) or not isinstance(hard, list):
            errors.append("task %s ownership fields must be lists" % task_id)
            continue
        if not owned and not hard:
            errors.append("task %s owns neither criteria nor hard gates" % task_id)
        for rid in owned:
            if rid not in criterion_ids:
                errors.append("task %s owns unknown criterion %s" % (task_id, rid))
            owners.setdefault(rid, []).append(task_id)
        for gate in hard:
            if gate not in OWNABLE_HARD_GATES:
                errors.append("task %s owns unknown hard gate %s" %
                              (task_id, gate))
            hard_owners.setdefault(gate, []).append(task_id)
        for verifier in task.get("acceptance_verifiers", []):
            if verifier not in REGISTRY:
                errors.append("task %s names unknown acceptance verifier %s" %
                              (task_id, verifier))
        for field in ("owned_files", "evidence_paths"):
            for raw_path in task.get(field, []):
                if (not isinstance(raw_path, str) or not raw_path or
                        Path(raw_path).is_absolute() or
                        ".." in Path(raw_path).parts):
                    errors.append("task %s has unsafe %s entry %r" %
                                  (task_id, field, raw_path))
    for rid, criterion in criterion_by_id.items():
        task_id = criterion.get("task")
        if task_id:
            if task_id not in task_ids:
                errors.append("criterion %s names unknown task %s" % (rid, task_id))
            if task_id not in owners.get(rid, []):
                errors.append("task %s does not declare ownership of %s" %
                              (task_id, rid))
        declared = owners.get(rid, [])
        if len(declared) != 1:
            errors.append("criterion %s must have exactly one task owner, got %d" %
                          (rid, len(declared)))
    for gate, declared in hard_owners.items():
        if len(declared) != 1:
            errors.append("hard gate %s must have exactly one task owner" % gate)
    for task_id, deps in dependencies.items():
        for dependency in deps:
            if dependency not in task_ids:
                errors.append("task %s depends on unknown task %s" %
                              (task_id, dependency))
            if dependency == task_id:
                errors.append("task %s cannot depend on itself" % task_id)

    # A cycle makes the ledger impossible to execute. Unknown nodes were
    # already reported and are ignored here so the diagnostic stays precise.
    visiting, visited = set(), set()

    def visit(task_id):
        if task_id in visiting:
            errors.append("task dependency graph contains a cycle at %s" %
                          task_id)
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in dependencies.get(task_id, []):
            if dependency in task_ids:
                visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in sorted(task_ids):
        visit(task_id)
    return errors


def external_requirements(path=EXTERNAL_GATES):
    """Load closed-schema external gates without treating claims as proof."""
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [], ["external gate policy is unreadable: %s" % error]
    errors = []
    if set(document) != {"schema", "title", "note", "gates"}:
        errors.append("external gate policy fields are not the closed schema")
    if document.get("schema") != 1:
        errors.append("external gate policy schema must be 1")
    gates = document.get("gates")
    if not isinstance(gates, list) or not gates:
        return [], errors + ["external gates must be a nonempty list"]
    expected = {
        "EXT-CI", "EXT-AI", "EXT-INTEGRATIONS", "EXT-USER",
        "EXT-TEAM", "EXT-REGULATORY", "EXT-RELEASE",
    }
    seen, rows = set(), []
    fields = {"id", "title", "status", "evidence_required", "owner_action"}
    for gate in gates:
        if not isinstance(gate, dict) or set(gate) != fields:
            errors.append("each external gate must use the closed gate schema")
            continue
        gate_id = gate.get("id")
        if gate_id in seen:
            errors.append("duplicate external gate %s" % gate_id)
        seen.add(gate_id)
        if gate.get("status") != "required":
            errors.append(
                "external gate %s cannot self-attest; status must be required" %
                gate_id)
        evidence = gate.get("evidence_required")
        if not isinstance(evidence, list) or not evidence or not all(
                isinstance(item, str) and item for item in evidence):
            errors.append("external gate %s needs explicit evidence" % gate_id)
        if not isinstance(gate.get("owner_action"), str) or not \
                gate.get("owner_action"):
            errors.append("external gate %s needs an owner action" % gate_id)
        rows.append(dict(gate))
    if seen != expected:
        errors.append("external gate set mismatch: expected %s" %
                      ", ".join(sorted(expected)))
    return rows, errors


def run_verifier(verifier_id):
    """Run fixed argv steps and return a structured all-or-nothing result."""
    started = time.monotonic()
    rows, passed = [], True
    for step in REGISTRY[verifier_id]:
        argv = list(step.argv)
        if argv and argv[0] == "python3":
            argv[0] = sys.executable
        step_started = time.monotonic()
        try:
            done = subprocess.run(
                argv, cwd=str(REPO), shell=False, capture_output=True,
                text=True, timeout=step.timeout, env=clean_env())
            code = done.returncode
            output = ((done.stdout or "") + (done.stderr or "")).strip()
        except subprocess.TimeoutExpired as error:
            code = None
            output = "timed out after %s seconds" % step.timeout
            if error.stdout:
                output += "\n" + str(error.stdout)[-400:]
        tests_run = None
        evidence_error = None
        if step.tests:
            found = re.search(r"^Ran (\d+) tests?", output, re.M)
            tests_run = int(found.group(1)) if found else 0
            missing = [test_id for test_id in step.tests
                       if test_id.rsplit(".", 1)[-1] not in output]
            forbidden = ("skipped=", "expected failures=",
                         "unexpected successes=")
            if tests_run != len(step.tests):
                evidence_error = "expected %d exact tests; runner reported %d" % (
                    len(step.tests), tests_run)
            elif missing:
                evidence_error = "missing exact test evidence: %s" % \
                    ", ".join(missing)
            elif any(token in output for token in forbidden):
                evidence_error = "skipped/expected-failure evidence is forbidden"
        ok = code == 0 and evidence_error is None
        passed = passed and ok
        rows.append({
            "argv": argv,
            "exit_code": code,
            "seconds": round(time.monotonic() - step_started, 3),
            "expected_test_ids": list(step.tests),
            "tests_run": tests_run,
            "evidence_error": evidence_error,
            "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
            "output_tail": output[-800:] if not ok else "",
        })
        if not ok:
            break
    return passed, round(time.monotonic() - started, 3), rows


def score(selected=None):
    before_head = git("rev-parse", "HEAD")
    before_status = git("status", "--porcelain=v1", "--untracked-files=all")
    spec = json.loads(CRITERIA.read_text(encoding="utf-8"))
    ledger = json.loads(TASKS.read_text(encoding="utf-8"))
    integrity_errors = validate(spec, ledger)
    external_gates, external_errors = external_requirements()
    integrity_errors.extend(external_errors)
    known_categories = {row.get("id") for row in spec.get("categories", [])
                        if isinstance(row, dict)}
    if selected and selected not in known_categories:
        integrity_errors.append("unknown category %r" % selected)

    report = {
        "schema": 2,
        "scope": "category-diagnostic" if selected else "local-readiness",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "evaluated_commit": before_head or "",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD") or "",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "evidence_digests": {
            "criteria": digest(CRITERIA),
            "task_ledger": digest(TASKS),
            "external_gate_policy": digest(EXTERNAL_GATES),
            "verifier_registry": digest(REGISTRY_FILE),
            "workflow": digest(REPO / ".github" / "workflows" / "lint.yml"),
        },
        "rubric_errors": integrity_errors,
        "categories": [],
        "earned": 0,
        "possible": 0,
        "verified_criteria": 0,
        "failed_criteria": 0,
        "unbuilt_criteria": 0,
        "external_blockers": [row["id"] for row in external_gates],
        "external_gates": [dict(row, verified=False)
                           for row in external_gates],
        "open_tasks": [],
    }

    verifier_results = {}

    def verified(verifier_id):
        if verifier_id not in verifier_results:
            verifier_results[verifier_id] = run_verifier(verifier_id)
        return verifier_results[verifier_id]

    if not integrity_errors:
        for category in spec["categories"]:
            if selected and category["id"] != selected:
                continue
            block = {"id": category["id"], "title": category["title"],
                     "points": category["points"], "earned": 0,
                     "criteria": []}
            say("")
            say("== %s (%d points)" % (category["title"], category["points"]))
            for criterion in category["criteria"]:
                entry = {"id": criterion["id"], "title": criterion["title"],
                         "points": criterion["points"]}
                verifier = criterion.get("verifier")
                if verifier:
                    passed, seconds, steps = verified(verifier)
                    entry.update({"verifier": verifier, "seconds": seconds,
                                  "steps": steps,
                                  "status": "green" if passed else "failing",
                                  "earned": criterion["points"] if passed else 0})
                    counter = "verified_criteria" if passed else "failed_criteria"
                    report[counter] += 1
                    say("  [%s] %-6s %2d/%-2d  %s  (%.1fs)" %
                        ("PASS" if passed else "FAIL", criterion["id"],
                         entry["earned"], criterion["points"],
                         criterion["title"][:66], seconds))
                    if not passed:
                        failed = steps[-1]
                        detail = failed["evidence_error"]
                        if not detail:
                            tail = failed["output_tail"].splitlines()
                            detail = tail[-1] if tail else "no output"
                        say("           exit %s: %s" %
                            (failed["exit_code"], detail))
                else:
                    blocker = criterion["blocker"]
                    external = blocker.startswith(EXTERNAL)
                    entry.update({"status": "external-blocker" if external
                                  else "unbuilt", "earned": 0,
                                  "task": criterion["task"],
                                  "blocker": blocker})
                    report["unbuilt_criteria"] += 1
                    report["open_tasks"].append(criterion["task"])
                    # Rubric blockers are local implementation defects. True
                    # external requirements live in external-gates.json.
                    say("  [%s] %-6s  0/%-2d  %s" %
                        ("EXT " if external else "TODO", criterion["id"],
                         criterion["points"], criterion["title"][:66]))
                block["earned"] += entry["earned"]
                block["criteria"].append(entry)
            block["shortfall"] = block["points"] - block["earned"]
            report["categories"].append(block)
            report["earned"] += block["earned"]
            report["possible"] += block["points"]
    elif not selected:
        report["possible"] = 100

    # A hard gate is a release requirement even when it deliberately carries
    # no rubric points. Execute every such verifier explicitly; checking only
    # whether a point-bearing criterion happened to populate the cache made
    # otherwise-green local readiness impossible to reach.
    if not selected and not integrity_errors:
        for verifier_ids in LOCAL_HARD_GATE_VERIFIERS.values():
            for verifier_id in verifier_ids:
                verified(verifier_id)

    report["open_tasks"] = sorted(set(report["open_tasks"]))
    report["external_blockers"] = sorted(set(report["external_blockers"]))
    after_head = git("rev-parse", "HEAD")
    after_status = git("status", "--porcelain=v1", "--untracked-files=all")
    git_available = bool(
        isinstance(before_head, str) and
        re.fullmatch(r"[0-9a-fA-F]{40}", before_head) and
        isinstance(after_head, str) and
        re.fullmatch(r"[0-9a-fA-F]{40}", after_head) and
        isinstance(before_status, str) and isinstance(after_status, str)
    )
    stable = bool(git_available and before_head == after_head and
                  before_status == after_status)
    clean = bool(git_available and before_status == "" and after_status == "")
    report["tree"] = {
        "before_head": before_head,
        "after_head": after_head,
        "git_available": git_available,
        "before_clean": bool(git_available and before_status == ""),
        "after_clean": bool(git_available and after_status == ""),
        "stable_during_evaluation": stable,
    }
    local_hard_gates = {
        "rubric_integrity_green": not integrity_errors,
        "task_ledger_buildable": ledger.get("schema") == 2 and
        not integrity_errors,
        "all_tasks_green": bool(ledger.get("tasks")) and all(
            task.get("status") == "green"
            for task in ledger.get("tasks", [])
            if isinstance(task, dict)),
        "every_verifiable_criterion_passes": report["failed_criteria"] == 0,
        "no_unbuilt_criteria": report["unbuilt_criteria"] == 0,
        "tree_clean_and_stable": clean and stable,
    }
    for gate_name, verifier_ids in LOCAL_HARD_GATE_VERIFIERS.items():
        local_hard_gates[gate_name] = all(
            verifier_id in verifier_results and
            verifier_results[verifier_id][0]
            for verifier_id in verifier_ids)
    report["hard_gates"] = local_hard_gates
    all_local_green = all(local_hard_gates.values())
    local_complete = (not selected and all_local_green and
                      report["earned"] == 100 and
                      report["possible"] == 100)
    external_complete = not report["external_blockers"]
    complete = local_complete and external_complete
    report["all_hard_gates_green"] = all_local_green
    report["local_engineering_readiness"] = local_complete
    report["external_readiness"] = external_complete
    report["complete_readiness"] = complete
    if selected:
        report["verdict"] = "CATEGORY DIAGNOSTIC: %s %d/%d" % (
            selected, report["earned"], report["possible"])
    elif complete:
        report["verdict"] = (
            "COMPLETE PM OS READINESS: 100/100 — ALL HARD GATES GREEN")
    elif local_complete:
        report["verdict"] = (
            "COMPLETE PM OS READINESS: NOT 100/100 — BLOCKED "
            "(LOCAL ENGINEERING READINESS 100/100)")
    else:
        report["verdict"] = (
            "COMPLETE PM OS READINESS: NOT 100/100 — WORK REMAINS")
    return report


def output_path(value):
    path = Path(value).expanduser().resolve()
    try:
        path.relative_to(REPO.resolve())
    except ValueError:
        return path
    ignored = subprocess.run(["git", "check-ignore", "-q", str(path)],
                             cwd=str(REPO), shell=False).returncode == 0
    if not ignored:
        raise ReadinessError(
            "scorecard output inside the repository must be ignored; use an "
            "external path or add a dedicated ignored artifact directory")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output", "--json", dest="output", metavar="PATH",
                        help="write JSON to an external or ignored path")
    parser.add_argument("--category", help="diagnose one category only")
    parser.add_argument(
        "--local", action="store_true",
        help="exit on the local 100-point engineering gate; still report all external requirements")
    parser.add_argument("--no-write", action="store_true",
                        help="deprecated compatibility flag; stdout is default")
    args = parser.parse_args(argv)
    if args.no_write and args.output:
        parser.error("--no-write and --output are mutually exclusive")

    report = score(args.category)
    say("")
    say("=" * 72)
    say("SCORE: %d / %d" % (report["earned"], report["possible"]))
    if report["rubric_errors"]:
        say("  rubric/evaluator integrity errors:")
        for error in report["rubric_errors"]:
            say("   -", error)
    say("  passing evidence : %d criteria" % report["verified_criteria"])
    say("  failing          : %d criteria" % report["failed_criteria"])
    say("  not built        : %d criteria" % report["unbuilt_criteria"])
    say("  external blockers: %s" %
        (", ".join(report["external_blockers"]) or "none"))
    for name, ok in report["hard_gates"].items():
        say("  hard gate %-40s %s" % (name, "GREEN" if ok else "NOT GREEN"))
    say("")
    say(report["verdict"])
    say("  measured on %s with Python %s" %
        (report["evaluated_commit"][:12] or "unknown", report["python"]))
    if report["external_blockers"]:
        say("  external evidence remains required; local tests cannot self-attest it")

    if args.output:
        try:
            out = output_path(args.output)
        except ReadinessError as error:
            say("  scorecard not written:", error)
            return 2
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        say("  scorecard written to", out)
    if args.category:
        return 0 if (not report["rubric_errors"] and
                     report["failed_criteria"] == 0) else 1
    if args.local:
        return 0 if report["local_engineering_readiness"] else 1
    return 0 if report["complete_readiness"] else 1


if __name__ == "__main__":
    sys.exit(main())
