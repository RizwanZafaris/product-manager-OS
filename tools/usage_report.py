#!/usr/bin/env python3
"""Usage and cost report over the shared spend ledger (audit finding S08).

    python3 tools/usage_report.py
    python3 tools/usage_report.py --ledger /path/to/spend.sqlite
    python3 tools/usage_report.py --json
    python3 tools/usage_report.py --task-suite suite.json
    python3 tools/usage_report.py --compare before.sqlite after.sqlite
    python3 tools/usage_report.py --compare before.json after.json --json

Standard library only, like every other script in this tree.

## What this reads

The spend ledger (``pmos/spend.py``) is the only source of truth this script
reads. Every reservation it records may carry: operation (what kind of call
this was, for example a task dispatch, a probe, a retry, a summary or a
review), task_id (which finding or task the call served), context_version
(which context or handoff bundle produced the call), resolved_model,
provider, cache_disposition, and success. Every field is optional, and a
reservation written before these fields existed reads back with them as
``None``: this script reports that as "(unspecified)" or "(unreported)" in a
grouping key, never silently drops the row and never guesses a value.

## Cost certainty

Every reservation is exactly one of three states, and this script never
blurs them into one number:

- billed: the call finished and a real cost came back.
- reserved worst case, not yet settled: the call has not settled yet, so
  this is the most it could have cost, not what it did cost.
- unknown: the call finished but its provider never reported a cost; the
  reservation's full worst case stays charged until someone reconciles it
  with ``python3 -m pmos.spend reconcile``.

A row that reports only "billed" totals and silently ignores open or unknown
reservations understates spend. This script always shows all three, labeled,
never netted into one figure.

## Denominators and quality failures

Every table in this report carries a denominator, completed of attempted,
where attempted is every reservation (or every fixed-suite task) counted and
completed is the subset that actually settled or resolved as unknown (as
opposed to a reservation that was made and never settled, which is real
in-flight or abandoned work, not zero work). Quality failures are the subset
of completed calls whose reply was not usable (settle's ``success=False``),
counted separately from cost, because a cheaper call that failed more often
is not a saving.

## Unavailable usage

Some tiers bill through a subscription rather than a per-call price, and the
harness never opens a spend session for them (see harness/runner.py,
transport_call: ``_SPEND is None`` skips the ledger entirely). The ledger
therefore has no rows for that usage at all, and this script never invents a
$0.00 figure for it. A ``--task-suite`` file can declare such a task
explicitly with ``"metered": false``; this report then shows its cost as the
literal string "unavailable", never as a number, and takes its completed and
success facts (which the ledger cannot see) from whatever the suite file
states, also "unavailable" when the suite does not say.

## Comparing a fixed task suite

No token or cost savings claim is valid without comparing the same fixed set
of tasks before and after a change; a smaller total spend over a different or
partial task set proves nothing. ``--compare BEFORE AFTER`` builds a report
for each side (a ledger sqlite file, or a JSON report this tool already
wrote with ``--json``) and diffs their "suite_coverage" tables when both
sides were built against the same ``--task-suite``. When the two sides name
different task ids, or either side has no suite_coverage at all, the compare
output says so plainly (``fixed_suite_match: false`` or ``null``) instead of
printing a delta that looks like a savings claim.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from pmos.spend import SpendLedger, cost_certainty, default_path  # noqa: E402

UNAVAILABLE = "unavailable"
UNSPECIFIED = "(unspecified)"
UNREPORTED = "(unreported)"
UNRESOLVED = "(unresolved)"
SQLITE_MAGIC = b"SQLite format 3\x00"


# --------------------------------------------------------------- reading in

def load_reservations(ledger_path: Path) -> List[Dict[str, Any]]:
    """Every reservation in the ledger at ``ledger_path``, oldest first.

    Returns an empty list, and never creates the file, when nothing exists
    at ``ledger_path`` yet: an absent ledger reports no usage, which is
    different from a ledger that recorded zero-cost usage.
    """
    path = Path(ledger_path)
    if not path.exists():
        return []
    ledger = SpendLedger(path)
    try:
        return ledger.reservations()
    finally:
        ledger.close()


def load_task_suite(path: Optional[Path]) -> List[Dict[str, Any]]:
    """Parse a fixed representative task suite file.

    Each entry is an object with a required ``task_id`` and optional
    ``operation``, ``metered`` (default true), ``completed``, ``success``
    and ``label``. ``completed`` and ``success`` matter only for a
    ``metered: false`` entry: the ledger has no rows for unmetered usage, so
    those two facts, when known at all, have to come from the suite file
    itself rather than from a guess.
    """
    if path is None:
        return []
    text = Path(path).read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("%s is not valid JSON: %s" % (path, exc)) from exc
    if not isinstance(payload, list):
        raise ValueError("%s must be a JSON array of task entries" % path)
    entries: List[Dict[str, Any]] = []
    seen_ids = set()
    for index, raw in enumerate(payload):
        if not isinstance(raw, dict) or not raw.get("task_id"):
            raise ValueError(
                "%s entry %d has no task_id" % (path, index))
        task_id = str(raw["task_id"])
        if task_id in seen_ids:
            raise ValueError(
                "%s names task_id %s more than once" % (path, task_id))
        seen_ids.add(task_id)
        entries.append({
            "task_id": task_id,
            "operation": raw.get("operation"),
            "metered": bool(raw.get("metered", True)),
            "completed": raw.get("completed"),
            "success": raw.get("success"),
            "label": raw.get("label"),
        })
    return entries


# ------------------------------------------------------------- summarizing

def _completed(record: Mapping[str, Any]) -> bool:
    """A reservation is completed once it settled, billed or unknown.

    An 'open' reservation was made and never settled: real attempted work,
    not yet completed work, and never counted as completed.
    """
    return record["state"] in ("settled", "unknown")


def summarize(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """One denominators-and-totals row over a group of reservations."""
    attempted = len(records)
    completed_records = [r for r in records if _completed(r)]
    completed = len(completed_records)
    quality_failures = sum(1 for r in completed_records if r["success"] is False)
    success_unreported = sum(1 for r in completed_records if r["success"] is None)
    billed_usd = sum(r["charged_usd"] or 0.0 for r in records
                     if r["state"] == "settled")
    reserved_worst_case_usd = sum(r["reserved_usd"] for r in records
                                  if r["state"] == "open")
    unresolved_worst_case_usd = sum(r["charged_usd"] or 0.0 for r in records
                                    if r["state"] == "unknown")
    certainty_counts = collections.Counter(
        cost_certainty(r["state"]) for r in records)
    return {
        "attempted": attempted,
        "completed": completed,
        "open": attempted - completed,
        "denominator": "%d/%d" % (completed, attempted),
        "quality_failures": quality_failures,
        "success_unreported": success_unreported,
        "billed_usd": round(billed_usd, 6),
        "reserved_worst_case_usd": round(reserved_worst_case_usd, 6),
        "unresolved_worst_case_usd": round(unresolved_worst_case_usd, 6),
        "cost_certainty_counts": dict(certainty_counts),
    }


def _group(records: Sequence[Mapping[str, Any]],
           key_fn) -> Dict[str, Dict[str, Any]]:
    buckets: Dict[str, List[Mapping[str, Any]]] = collections.defaultdict(list)
    for record in records:
        buckets[key_fn(record)].append(record)
    return {key: summarize(rows) for key, rows in sorted(buckets.items())}


def _model_provider_key(record: Mapping[str, Any]) -> str:
    model = record.get("resolved_model") or UNRESOLVED
    provider = record.get("provider") or "(unknown provider)"
    return "%s @ %s" % (model, provider)


def build_sections(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Every grouping this report publishes, plus one overall row."""
    return {
        "overall": summarize(records),
        "by_operation": _group(
            records, lambda r: r.get("operation") or UNSPECIFIED),
        "by_model_provider": _group(records, _model_provider_key),
        "by_task": _group(
            records, lambda r: r.get("task_id") or UNSPECIFIED),
        "by_cache_disposition": _group(
            records, lambda r: r.get("cache_disposition") or UNREPORTED),
        "by_cost_certainty": _group(
            records, lambda r: cost_certainty(r["state"])),
    }


# --------------------------------------------------- fixed task suite rows

def _suite_row_metered(task_id: str,
                       records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    task_records = [r for r in records if r.get("task_id") == task_id]
    if not task_records:
        return {
            "attempted": 1,
            "completed": False,
            "success": None,
            "billed_usd": UNAVAILABLE,
            "cost_certainty": UNAVAILABLE,
        }
    completed_records = [r for r in task_records if _completed(r)]
    completed = bool(completed_records)
    if any(r["success"] is False for r in completed_records):
        success: Optional[bool] = False
    elif any(r["success"] is True for r in completed_records):
        success = True
    else:
        success = None
    billed = sum(r["charged_usd"] or 0.0 for r in task_records
                 if r["state"] == "settled")
    states = {r["state"] for r in task_records}
    if "unknown" in states:
        certainty = cost_certainty("unknown")
    elif states == {"settled"}:
        certainty = cost_certainty("settled")
    elif "open" in states:
        certainty = cost_certainty("open")
    else:
        certainty = UNAVAILABLE
    return {
        "attempted": 1,
        "completed": completed,
        "success": success,
        "billed_usd": round(billed, 6),
        "cost_certainty": certainty,
    }


def _suite_row_unmetered(entry: Mapping[str, Any]) -> Dict[str, Any]:
    # Subscription usage never opens a spend session (harness/runner.py,
    # transport_call: _SPEND is None skips the ledger), so the ledger has
    # nothing to say about it. Cost is unavailable by construction, not
    # looked up, and completed/success come only from what the suite file
    # itself was told, never inferred.
    return {
        "attempted": 1,
        "completed": entry.get("completed"),
        "success": entry.get("success"),
        "billed_usd": UNAVAILABLE,
        "cost_certainty": UNAVAILABLE,
    }


def suite_coverage(suite: Sequence[Mapping[str, Any]],
                   records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Completed-of-attempted denominators over the fixed task suite.

    One row per suite entry: a metered entry's completed, success and cost
    come from the ledger; an unmetered entry's cost is always the literal
    string "unavailable", and its completed/success come from the suite
    file, "unavailable" too when the file does not say.
    """
    rows: Dict[str, Any] = {}
    for entry in suite:
        task_id = entry["task_id"]
        if entry["metered"]:
            row = _suite_row_metered(task_id, records)
        else:
            row = _suite_row_unmetered(entry)
        row["operation"] = entry.get("operation")
        row["metered"] = entry["metered"]
        row["label"] = entry.get("label")
        rows[task_id] = row
    attempted = len(rows)
    completed = sum(1 for row in rows.values() if row["completed"] is True)
    quality_failures = sum(1 for row in rows.values()
                           if row["success"] is False)
    unavailable = sum(1 for row in rows.values()
                      if row["billed_usd"] == UNAVAILABLE)
    return {
        "tasks": rows,
        "attempted": attempted,
        "completed": completed,
        "denominator": "%d/%d" % (completed, attempted),
        "quality_failures": quality_failures,
        "unavailable_cost_tasks": unavailable,
    }


# ------------------------------------------------------------- the report

def build_report(ledger_path: Path,
                 task_suite: Optional[Sequence[Mapping[str, Any]]] = None
                 ) -> Dict[str, Any]:
    records = load_reservations(ledger_path)
    report: Dict[str, Any] = {
        "ledger": str(ledger_path),
        "sections": build_sections(records),
    }
    if task_suite:
        report["suite_coverage"] = suite_coverage(task_suite, records)
    else:
        report["suite_coverage"] = None
    return report


# ------------------------------------------------------------------ compare

def _looks_like_sqlite(path: Path) -> bool:
    try:
        with open(path, "rb") as handle:
            head = handle.read(len(SQLITE_MAGIC))
    except OSError:
        return False
    return head == SQLITE_MAGIC


def load_snapshot(spec: str,
                  task_suite: Optional[Sequence[Mapping[str, Any]]]
                  ) -> Dict[str, Any]:
    """One side of ``--compare``: a ledger file or a saved JSON report."""
    path = Path(spec)
    if not path.exists():
        raise ValueError("no such ledger or report file: %s" % spec)
    if _looks_like_sqlite(path):
        return build_report(path, task_suite)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(
            "%s is neither a spend ledger nor a JSON report: %s"
            % (spec, exc)) from exc
    if not isinstance(payload, dict) or "sections" not in payload:
        raise ValueError("%s is valid JSON but not a usage report" % spec)
    return payload


def _numeric_delta(before: Mapping[str, Any], after: Mapping[str, Any],
                   field: str) -> Optional[float]:
    b, a = before.get(field), after.get(field)
    if isinstance(b, (int, float)) and isinstance(a, (int, float)):
        return round(a - b, 6)
    return None


_DELTA_FIELDS = ("attempted", "completed", "quality_failures", "billed_usd",
                 "reserved_worst_case_usd", "unresolved_worst_case_usd")


def _diff_summaries(before: Mapping[str, Any],
                    after: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "before": before,
        "after": after,
        "delta": {field: _numeric_delta(before, after, field)
                 for field in _DELTA_FIELDS},
    }


def _diff_section(before: Mapping[str, Any],
                  after: Mapping[str, Any]) -> Dict[str, Any]:
    keys = sorted(set(before) | set(after))
    empty = summarize([])
    return {key: _diff_summaries(before.get(key, empty), after.get(key, empty))
           for key in keys}


def compare_reports(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Diff two reports, and say plainly when they do not share a fixed suite.

    A savings claim over billed_usd or attempted/completed counts is only as
    good as the guarantee that both sides ran the same fixed task suite.
    ``fixed_suite_match`` is true only when both sides carry suite_coverage
    and name exactly the same task ids; otherwise it is false (both present,
    different tasks) or null (one or both sides built with no task suite at
    all), and the delta numbers must not be read as a savings claim.
    """
    before_suite = before.get("suite_coverage")
    after_suite = after.get("suite_coverage")
    if before_suite is None or after_suite is None:
        fixed_suite_match: Optional[bool] = None
    else:
        fixed_suite_match = (set(before_suite["tasks"]) ==
                             set(after_suite["tasks"]))
    result: Dict[str, Any] = {
        "fixed_suite_match": fixed_suite_match,
        "overall": _diff_summaries(before["sections"]["overall"],
                                   after["sections"]["overall"]),
        "by_operation": _diff_section(before["sections"]["by_operation"],
                                      after["sections"]["by_operation"]),
        "by_model_provider": _diff_section(
            before["sections"]["by_model_provider"],
            after["sections"]["by_model_provider"]),
        "by_task": _diff_section(before["sections"]["by_task"],
                                 after["sections"]["by_task"]),
    }
    if before_suite is not None and after_suite is not None:
        result["suite_coverage"] = {
            "before": before_suite,
            "after": after_suite,
            "completed_delta": after_suite["completed"] - before_suite["completed"],
            "quality_failures_delta": (after_suite["quality_failures"] -
                                       before_suite["quality_failures"]),
        }
    return result


# --------------------------------------------------------------- rendering

def _render_summary_line(indent: str, key: str, row: Mapping[str, Any]) -> str:
    return ("%s%s: %s completed of attempted, quality_failures=%d, "
            "billed_usd=%.6f, reserved_worst_case_usd=%.6f, "
            "unresolved_worst_case_usd=%.6f"
            % (indent, key, row["denominator"], row["quality_failures"],
               row["billed_usd"], row["reserved_worst_case_usd"],
               row["unresolved_worst_case_usd"]))


def render_text(report: Mapping[str, Any]) -> str:
    lines = ["ledger: %s" % report["ledger"]]
    lines.append(_render_summary_line("overall ", "totals",
                                      report["sections"]["overall"]))
    for section_name in ("by_operation", "by_model_provider", "by_task",
                        "by_cache_disposition", "by_cost_certainty"):
        section = report["sections"][section_name]
        lines.append("%s:" % section_name)
        if not section:
            lines.append("  (no reservations)")
            continue
        for key, row in section.items():
            lines.append(_render_summary_line("  ", key, row))
    coverage = report.get("suite_coverage")
    if coverage is None:
        lines.append("suite_coverage: no --task-suite was given")
    else:
        lines.append("suite_coverage: %s completed of attempted, "
                     "quality_failures=%d, unavailable_cost_tasks=%d"
                     % (coverage["denominator"], coverage["quality_failures"],
                        coverage["unavailable_cost_tasks"]))
        for task_id, row in sorted(coverage["tasks"].items()):
            lines.append(
                "  %s: metered=%s completed=%s success=%s billed_usd=%s "
                "cost_certainty=%s"
                % (task_id, row["metered"], row["completed"], row["success"],
                   row["billed_usd"], row["cost_certainty"]))
    return "\n".join(lines)


def render_compare_text(before_spec: str, after_spec: str,
                        diff: Mapping[str, Any]) -> str:
    lines = ["compare: before=%s after=%s" % (before_spec, after_spec)]
    match = diff["fixed_suite_match"]
    if match is True:
        lines.append("fixed_suite_match: true, the delta below is a valid "
                     "before/after comparison on one fixed task suite")
    elif match is False:
        lines.append("fixed_suite_match: false, before and after named "
                     "different tasks; the delta below is NOT a savings "
                     "claim, it compares different work")
    else:
        lines.append("fixed_suite_match: unavailable, run both sides with "
                     "the same --task-suite before reading any delta as a "
                     "savings claim")
    overall = diff["overall"]
    lines.append("overall delta: attempted=%s completed=%s "
                 "quality_failures=%s billed_usd=%s "
                 "reserved_worst_case_usd=%s unresolved_worst_case_usd=%s"
                 % tuple(overall["delta"][field] for field in _DELTA_FIELDS))
    if "suite_coverage" in diff:
        lines.append("suite_coverage delta: completed=%+d quality_failures=%+d"
                     % (diff["suite_coverage"]["completed_delta"],
                        diff["suite_coverage"]["quality_failures_delta"]))
    return "\n".join(lines)


# ------------------------------------------------------------------- main

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tools/usage_report.py",
        description="Usage and cost report over the shared spend ledger.",
    )
    parser.add_argument("--ledger", default=str(default_path()),
                        help="path to the spend ledger (default: %(default)s)")
    parser.add_argument("--task-suite", type=Path, default=None,
                        help="JSON file naming the fixed representative "
                             "task suite")
    parser.add_argument("--json", action="store_true",
                        help="print one JSON object instead of text")
    parser.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"),
                        default=None,
                        help="two ledger files or saved JSON reports to "
                             "diff, each read with --task-suite when given")
    args = parser.parse_args(argv)

    try:
        task_suite = load_task_suite(args.task_suite)
    except ValueError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2

    if args.compare is not None:
        before_spec, after_spec = args.compare
        try:
            before = load_snapshot(before_spec, task_suite or None)
            after = load_snapshot(after_spec, task_suite or None)
        except ValueError as exc:
            sys.stderr.write("%s\n" % exc)
            return 2
        diff = compare_reports(before, after)
        if args.json:
            print(json.dumps({"before": before, "after": after,
                              "compare": diff}, sort_keys=True))
        else:
            print(render_compare_text(before_spec, after_spec, diff))
        return 0

    report = build_report(Path(args.ledger), task_suite or None)
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
