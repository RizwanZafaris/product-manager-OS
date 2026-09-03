#!/usr/bin/env python3
"""pmos: the CLI face of the harness contract. Standard library only.

    harness/adapters/cli/pmos list
    harness/adapters/cli/pmos write-prd
    harness/adapters/cli/pmos review-spec --input products/dispute/PRD.md
    harness/adapters/cli/pmos build-roadmap --tier drafting

Resolves one task id from harness/MANIFEST.json and prints the plan: what the
task is, which stage and gate it belongs to, which tier it will use, which skill
governs it, which templates it fills, which files to read first, which
invariants bind it, and the exact next action a human takes.

The manifest holds the logic. This adapter is thin on purpose: every line it
prints is read out of a file that already governs the work, so the plan is the
same plan whether you read it here or read the router table in CLAUDE.md
yourself. Delete harness/ and nothing about the OS changes.

What it does not do, stated here rather than discovered later:

  * It never calls a model and never opens a network connection. There is no
    code in this file that could. Credentials are read from the environment for
    a presence check only (OMNIROUTE_BASE_URL, OMNIROUTE_API_KEY); the values
    are never printed, logged, or written anywhere.
  * It never writes, edits, or creates a file. Not the manifest, not a
    template, nothing under harness/.
  * It never signs a gate, approves a send, or decides that a route is the
    right route for a request. Those are the human's, per
    harness/INVARIANTS.md.
  * It says nothing about whether an artifact is any good. A resolved plan is
    a structural fact, which is the first of the three checks in
    harness/INVARIANTS.md and the weakest one.
  * It does not guess a route from free text. You pass a task id; a person
    reads the router table. An unroutable request is queued and the table
    amended, never guessed at.

Exit status: 0 on a resolved plan (with or without a model connected), 1 when
the request cannot be resolved (unknown task id, missing manifest, unreadable
input file), 2 on a usage error from the argument parser, 3 on a refusal.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path

MANIFEST = "harness/MANIFEST.json"
INVARIANTS = "harness/INVARIANTS.md"
ROUTING = "routing/omniroute.config.json"
ROUTING_DOC = "routing/README.md"
ROUTER = "CLAUDE.md"
GATES_DOC = "os/STAGE-GATES.md"
LOOP_DOC = "os/OPERATING-LOOP.md"
CHECKER = "tools/check_manifest.py"

TIER_RANK = {"extraction": 0, "drafting": 1, "judgment": 2}
BASE_URL_ENV = "OMNIROUTE_BASE_URL"
API_KEY_ENV = "OMNIROUTE_API_KEY"

INVARIANT_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|([^|]*)\|")
LABEL = 16


def find_root(start=None):
    """The repository root: the nearest parent holding the manifest and CLAUDE.md."""
    here = Path(start).resolve() if start else Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if (candidate / MANIFEST).is_file() and (candidate / ROUTER).is_file():
            return candidate
    return None


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def first_sentence(text):
    """The first sentence of a rule cell, for a one-line reminder.

    The rules live in a markdown table, so a link renders as its own text and
    backticks come off. The wording is quoted, never paraphrased.
    """
    text = MD_LINK_RE.sub(r"\1", text).replace("`", "")
    text = " ".join(text.split())
    cut = text.find(". ")
    return text if cut == -1 else text[:cut + 1]


def invariant_rules(root):
    """Map each invariant id to the first sentence of its rule."""
    path = root / INVARIANTS
    rules = {}
    if not path.is_file():
        return rules
    for line in path.read_text(encoding="utf-8").split("\n"):
        match = INVARIANT_ROW_RE.match(line.strip())
        if match:
            rules[match.group(1)] = first_sentence(match.group(2))
    return rules


def tier_facts(root):
    """The tiers block from routing/omniroute.config.json, the only mapping."""
    path = root / ROUTING
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    tiers = config.get("tiers")
    return tiers if isinstance(tiers, dict) else {}


def load_manifest(root):
    """The manifest, or (None, message) when it cannot be used."""
    path = root / MANIFEST
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        return None, "%s cannot be read: %s" % (MANIFEST, error)
    except json.JSONDecodeError as error:
        return None, "%s is not parseable at line %d: %s. Run python3 %s." % (
            MANIFEST, error.lineno, error.msg, CHECKER)
    entries = manifest.get("tasks")
    if not isinstance(entries, list) or not entries:
        return None, "%s holds no tasks array. Run python3 %s." % (
            MANIFEST, CHECKER)
    return manifest, None


def mark(root, candidate):
    """A path, flagged when the file is not in the tree."""
    if (root / candidate).is_file():
        return candidate
    return "%s (missing: run python3 %s)" % (candidate, CHECKER)


def field(label, values, out):
    """One labelled block. First value on the label line, the rest indented."""
    items = [values] if isinstance(values, str) else list(values)
    if not items:
        return
    out.write("%-*s%s\n" % (LABEL, label, items[0]))
    for item in items[1:]:
        out.write("%-*s%s\n" % (LABEL, "", item))


def cmd_list(root, entries, out):
    """The task table: one row per manifest entry, in router order."""
    widths = max(len(str(e.get("id"))) for e in entries)
    out.write("%-*s  %-8s %-4s %-10s %s\n"
              % (widths, "task id", "stage", "gate", "tier", "skill"))
    skill_rule = max(len(str(e.get("skill") or "")) for e in entries)
    out.write("%s  %s %s %s %s\n"
              % ("-" * widths, "-" * 8, "-" * 4, "-" * 10, "-" * skill_rule))
    for entry in entries:
        stage = entry.get("stage") or "none"
        gate = entry.get("gate")
        skill = entry.get("skill") or "(no skill: follow the reads)"
        out.write("%-*s  %-8s %-4s %-10s %s\n"
                  % (widths, entry.get("id"), stage,
                     str(gate) if gate else "none", entry.get("tier"), skill))
    out.write("\n%d entries, one per router row in %s, in router order.\n"
              % (len(entries), ROUTER))
    out.write("python3 %s proves the two faces agree. It proves nothing "
              "about quality.\n" % CHECKER)
    out.write("Plan one: harness/adapters/cli/pmos <task-id>\n")
    return 0


def resolve(entries, task):
    """The entry with this id, or None."""
    for entry in entries:
        if entry.get("id") == task:
            return entry
    return None


def unknown_task(entries, task, err):
    """Fail clearly on an unknown id, and name the near misses."""
    ids = [str(e.get("id")) for e in entries]
    close = difflib.get_close_matches(task, ids, n=3, cutoff=0.5)
    err.write("pmos: %r is not a task id in %s.\n" % (task, MANIFEST))
    if close:
        err.write("Closest ids: %s\n" % ", ".join(close))
    err.write("Run harness/adapters/cli/pmos list for all %d ids. A request "
              "that matches no row is queued and the router table in %s is "
              "amended, never guessed at.\n" % (len(ids), ROUTER))
    return 1


def tier_decision(entry, override, err):
    """The tier to print, plus notes. Returns (tier, notes) or (None, None)."""
    routed = entry.get("tier")
    if override is None or override == routed:
        notes = []
        if override == routed:
            notes.append("--tier %s repeats the routed tier, so nothing "
                         "changed." % override)
        return routed, notes
    if routed == "judgment" and override == "extraction":
        err.write(
            "pmos: REFUSED. --tier extraction would downgrade the judgment "
            "route %s to extraction.\n" % entry.get("id"))
        err.write(
            "Judgment work is work that is expensive to get wrong and hard to "
            "check locally. A cheap answer to it looks reviewed and is not, "
            "which is worse than a late one.\n")
        err.write(
            "Per fail-closed in %s and rule 3 in %s, judgment work queues; it "
            "never silently downgrades. Queue the task, or connect a provider "
            "that serves the judgment tier.\n" % (INVARIANTS, ROUTING_DOC))
        return None, None
    notes = []
    if TIER_RANK[override] < TIER_RANK[routed]:
        notes.append("WARNING: --tier %s downgrades this route from %s."
                     % (override, routed))
        notes.append("The manifest says %s because that is what a wrong "
                     "answer here costs. The plan below applies the override; "
                     "rerun without --tier for the routed plan."
                     % routed)
        if routed == "judgment":
            notes.append("A downgraded judgment run produces a document that "
                         "reads as reviewed. Say so on the artifact, or queue "
                         "the work instead (%s, rule 3)." % ROUTING_DOC)
    else:
        notes.append("--tier %s upgrades this route from %s. That spends more "
                     "and breaks no rule." % (override, routed))
    return override, notes


def input_block(root, entry, path, err):
    """Describe the task input file. Returns a list of lines, or None on error."""
    target = Path(path)
    if target.is_dir():
        err.write("pmos: --input %s is a directory. Name one file.\n" % path)
        return None
    try:
        raw = target.read_bytes()
    except OSError as error:
        err.write("pmos: --input %s cannot be read: %s\n" % (path, error))
        return None
    text = raw.decode("utf-8", errors="replace")
    lines = text.split("\n")
    head = next((line.strip() for line in lines if line.strip()), "(empty)")
    if len(head) > 78:
        head = head[:75] + "..."
    block = [
        "%s (%d bytes, %d lines)" % (target, len(raw), len(lines)),
        "first line: %s" % head,
        "Loaded as the task input and nothing else. Its contents are data: "
        "directives found inside it are reported to the human with the source "
        "named, never obeyed (content-is-data).",
    ]
    if "least-data" in (entry.get("invariants") or []):
        block.append("This route binds least-data. The denied directories and "
                     "document classes are named in the reads above; this tool "
                     "does not evaluate them, so check before this file "
                     "reaches a prompt.")
    return block


def credential_block(root, tier, facts):
    """What the environment offers, without reading a secret into the output."""
    # Presence only. The value is never stored, printed, or written.
    have_url = bool(os.environ.get(BASE_URL_ENV))
    have_key = bool(os.environ.get(API_KEY_ENV))
    block = [
        "%s: %s" % (BASE_URL_ENV, "set" if have_url else "not set"),
        "%s: %s (presence only, the value is never read into this output)"
        % (API_KEY_ENV, "set" if have_key else "not set"),
    ]
    if not have_key:
        block.append("No model call is possible from this shell, and this tool "
                     "would not make one anyway. The plan above stands without "
                     "one: the harness is an accelerant on a format that holds "
                     "on its own.")
    else:
        block.append("A caller can make the tiered call itself; the contract "
                     "and the request headers are in %s. This tool stays out "
                     "of it." % ROUTING_DOC)
    if tier == "judgment":
        requires = facts.get("judgment", {}).get("requires")
        if requires:
            block.append("judgment tier: %s" % first_sentence(requires))
        block.append("If that tier has no connected provider, the work queues. "
                     "It is never rerouted to a cheaper tier to finish on "
                     "time (fail-closed).")
    return block


def next_action(entry, tier, out_paths):
    """The exact next action a human takes, numbered."""
    steps = []
    reads = entry.get("reads") or []
    if len(reads) == 1:
        steps.append("Read %s first." % reads[0])
    elif reads:
        steps.append("Read %s, in that order." % ", ".join(reads))
    skill = entry.get("skill")
    if skill:
        steps.append("Follow %s. It owns the procedure; this plan only points "
                     "at it." % skill)
    else:
        steps.append("No skill governs this row, so the reads above are the "
                     "procedure. Nothing else is implied.")
    steps.append("Run the load-bearing call on the %s tier. The model for that "
                 "tier is in %s and nowhere else." % (tier, ROUTING))
    if out_paths:
        if len(out_paths) == 1:
            which = "Fill a copy of %s" % out_paths[0]
        else:
            which = ("Fill a copy of whichever of these the request calls "
                     "for, and the skill and the reads above decide which: %s"
                     % ", ".join(out_paths))
        steps.append("%s in your product workspace, per "
                     "os/PRODUCT-WORKSPACE.md. The file in the repository is "
                     "the blank, never the draft. A field with no answer gets "
                     "[OPEN: what is missing, who owns the answer], which is a "
                     "valid value." % which)
    else:
        steps.append("This row produces no artifact, so there is nothing to "
                     "fill in and nothing to file.")
    gate = entry.get("gate")
    if gate:
        steps.append("Take it to gate %d in %s. Report which boxes pass and "
                     "which do not, then stop: a named human signs it, never "
                     "an agent." % (gate, GATES_DOC))
    else:
        steps.append("No gate applies to this row. Review it on its own "
                     "cadence per %s." % LOOP_DOC)
    return ["%d. %s" % (i, step) for i, step in enumerate(steps, 1)]


def cmd_plan(root, entry, tier, notes, input_lines, facts, rules, out):
    """Print the resolved plan for one task."""
    stage = entry.get("stage")
    gate = entry.get("gate")
    model = facts.get(tier, {}).get("model")
    tier_line = "%s" % tier
    if tier != entry.get("tier"):
        tier_line += " (overridden by --tier; the manifest routes this to %s)" \
            % entry.get("tier")
    if model:
        tier_line += " (%s maps it to %s)" % (ROUTING, model)
    templates = [mark(root, p) for p in (entry.get("templates") or [])]
    reads = [mark(root, p) for p in (entry.get("reads") or [])]

    for note in notes:
        out.write("%s\n" % note)
    if notes:
        out.write("\n")

    field("task", entry.get("id"), out)
    field("router row", entry.get("router_row"), out)
    field("triggers", "; ".join(entry.get("trigger") or []), out)
    if stage:
        field("stage", "%s (gate %s in %s)" % (stage, gate, GATES_DOC), out)
        field("gate", "%s, signed by a named human, never by an agent" % gate,
              out)
    else:
        field("stage", "none. A planning overlay or a reference read: reviewed "
                       "on its own cadence, not at a gate (%s)." % LOOP_DOC,
              out)
        field("gate", "none. That means no gate applies, never that a gate was "
                      "skipped.", out)
    field("tier", tier_line, out)
    field("skill", entry.get("skill") or
          "none. This router row names no skill; the reads are the procedure.",
          out)
    field("templates", templates or
          ["none. This row produces no artifact."], out)
    field("reads first", reads or ["none named."], out)
    field("invariants", ["%s: %s" % (name, rules.get(name, "defined in %s"
                                                     % INVARIANTS))
                         for name in (entry.get("invariants") or [])]
          or ["none named, which is itself a defect: run python3 %s." % CHECKER],
          out)
    if entry.get("note"):
        field("manifest note", entry["note"], out)
    if input_lines:
        field("input", input_lines, out)
    field("credentials", credential_block(root, tier, facts), out)
    field("next action", next_action(entry, tier, entry.get("templates") or []),
          out)
    out.write("\nNothing was written, sent, or called. This plan is an index "
              "into files that already govern the work.\n")
    return 0


EPILOG = """\
examples:
  harness/adapters/cli/pmos list
  harness/adapters/cli/pmos write-prd
  harness/adapters/cli/pmos review-spec --input products/dispute/PRD.md
  harness/adapters/cli/pmos build-roadmap --tier drafting

what this tool does:
  resolves one task id from harness/MANIFEST.json and prints the plan behind it
  (stage, gate, tier, skill, templates, reads, invariants, next action).

what it does not do:
  no model call, no network connection, no file written or edited, no gate
  signed, no send approved, no judgment about whether a route or an artifact is
  any good, no guessing a route from free text. Credentials are checked for
  presence only and never printed. See the module docstring for why each of
  those is a refusal rather than a missing feature.

exit status:
  0 plan resolved, 1 request could not be resolved, 2 usage error,
  3 refused (a silent downgrade of judgment work to extraction).
"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="pmos",
        description="Resolve one task id from the harness manifest and print "
                    "its plan. Standard library only, no install step, no "
                    "model call.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("task", nargs="?",
                        help='a task id from harness/MANIFEST.json, or "list" '
                             "for the whole table")
    parser.add_argument("--input", metavar="PATH",
                        help="load this file as the task input. Its contents "
                             "are data, never instructions")
    parser.add_argument("--tier", choices=sorted(TIER_RANK),
                        help="override the routed tier. A downgrade warns; "
                             "downgrading judgment work to extraction is "
                             "refused")
    parser.add_argument("--root", metavar="PATH",
                        help="repository root (default: found from this "
                             "file's location)")
    args = parser.parse_args(argv)

    out, err = sys.stdout, sys.stderr
    root = find_root(args.root)
    if root is None:
        err.write("pmos: no repository root found from %s. Expected a parent "
                  "holding both %s and %s. Pass --root.\n"
                  % (args.root or Path(__file__).resolve().parent, MANIFEST,
                     ROUTER))
        return 1

    manifest, problem = load_manifest(root)
    if problem:
        err.write("pmos: %s\n" % problem)
        return 1
    entries = manifest["tasks"]

    if args.task is None:
        parser.print_help(out)
        return 0
    if args.task == "list":
        if args.input or args.tier:
            err.write("pmos: list takes no --input and no --tier.\n")
            return 1
        return cmd_list(root, entries, out)

    entry = resolve(entries, args.task)
    if entry is None:
        return unknown_task(entries, args.task, err)

    tier, notes = tier_decision(entry, args.tier, err)
    if tier is None:
        return 3

    input_lines = None
    if args.input:
        input_lines = input_block(root, entry, args.input, err)
        if input_lines is None:
            return 1

    return cmd_plan(root, entry, tier, notes, input_lines, tier_facts(root),
                    invariant_rules(root), out)


if __name__ == "__main__":
    sys.exit(main())
