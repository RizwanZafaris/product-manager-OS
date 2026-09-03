#!/usr/bin/env python3
"""Agreement gate for the harness contract. Standard library only.

    python3 tools/check_manifest.py
    python3 tools/check_manifest.py --quiet
    python3 tools/check_manifest.py --root /path/to/repo

Proves that harness/MANIFEST.json and the router table in CLAUDE.md are two
faces of one contract: every router row has exactly one manifest entry, every
manifest entry names a real router row, the entries are in router order, every
path in skill, templates and reads resolves to a file that exists, every tier is
one of the three tier names, every gate is 1 to 6, every stage is a real stage
name, every invariant id is defined in harness/INVARIANTS.md, and no model id
appears anywhere in the manifest.

The join key is the router row's own "When the user asks for" cell, stored
verbatim in each entry as router_row. Matching is exact on the collapsed cell
text, so an edit to either face that the other did not follow fails the build
rather than drifting quietly.

stage and gate accept null, and only together. PLANNING artifacts are reviewed
on their own cadence rather than at a gate, and reference rows (glossary,
philosophy, domain and role cards) produce no artifact at all; inventing a stage
for them would be a fabricated field. null means no gate applies, never that a
gate was skipped.

Limits, stated rather than hidden: this checks that the two faces agree and that
the paths exist, never that a route is the right route for the request, that a
tier assignment is sensible, or that a template is the one a reader needs. The
model-id scan is a list of vendor-shaped patterns, so an unlisted vendor's id
walks straight through. Green means the contract is consistent, not that it is
wise. Structural validity is the first of the three checks in
harness/INVARIANTS.md and it is not a quality gate.

Exit status is 1 on any problem, so CI can depend on it. Run it after any edit
to CLAUDE.md, harness/MANIFEST.json, or harness/INVARIANTS.md, alongside
python3 lint.py --os.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HARNESS = "harness"
MANIFEST = "harness/MANIFEST.json"
INVARIANTS = "harness/INVARIANTS.md"
ROUTER = "CLAUDE.md"

STAGES = ("DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER", "OPERATE")
TIERS = ("extraction", "drafting", "judgment")
GATES = (1, 2, 3, 4, 5, 6)

PATH_KEYS = ("skill", "templates", "reads")
REQUIRED_KEYS = ("id", "router_row", "trigger", "stage", "gate", "tier",
                 "skill", "templates", "reads", "invariants")

ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
ROUTER_HEADER = "When the user asks for"
SEPARATOR_RE = re.compile(r"^[\s:|-]+$")
INVARIANT_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|")

# The tier-to-model mapping belongs in routing/omniroute.config.json and
# nowhere else. A model id in the manifest puts the indirection one layer too
# low: the contract would then change every time a provider changed, and two
# files would disagree about which model answered. Vendor-shaped, deliberately:
# a detector's rules have to be legible to whoever reviews the detector.
MODEL_PATTERNS = [
    (r"auto/(?:cheap|coding|reasoning)", "an OmniRoute auto tier model string"),
    (r"\bgpt-?[0-9]", "an OpenAI gpt model id"),
    (r"\bo[134]-(?:mini|preview|pro)\b", "an OpenAI reasoning model id"),
    (r"\bclaude-[0-9a-z]", "an Anthropic claude model id"),
    (r"\b(?:sonnet|opus|haiku)\b", "an Anthropic model family name"),
    (r"\bgemini-[0-9a-z]", "a Google gemini model id"),
    (r"\bllama-?[0-9]", "a Llama model id"),
    (r"\bmistral-[0-9a-z]", "a Mistral model id"),
    (r"\b(?:qwen|deepseek|grok)-?[0-9]", "a third-party model id"),
]


def router_rows(text):
    """Every data row of the router table, as (line number, first cell).

    A router row is a three-cell pipe row that is neither the header nor the
    separator. Counting rows this way means a new row added to CLAUDE.md is
    picked up here without anyone remembering to update a number.
    """
    rows = []
    for line_no, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cell_list = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cell_list) != 3:
            continue
        first = cell_list[0]
        if not first or SEPARATOR_RE.match(first) or first == ROUTER_HEADER:
            continue
        rows.append((line_no, first))
    return rows


def invariant_ids(text):
    """Ids defined in the seven-rule table in harness/INVARIANTS.md."""
    found = []
    for line in text.split("\n"):
        match = INVARIANT_ROW_RE.match(line.strip())
        if match:
            found.append(match.group(1))
    return found


def entry_lines(raw):
    """Map each entry id to the line its "id" key sits on, for the messages."""
    lines = {}
    for line_no, line in enumerate(raw.split("\n"), 1):
        match = re.search(r'"id"\s*:\s*"([^"]+)"', line)
        if match and match.group(1) not in lines:
            lines[match.group(1)] = line_no
    return lines


def walk_strings(node, trail="tasks"):
    """Yield (json path, string) for every string anywhere under node."""
    if isinstance(node, str):
        yield trail, node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, "%s.%s" % (trail, key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, "%s[%d]" % (trail, index))


def check_paths(entry, root, line_no, fail):
    """Every path in skill, templates and reads resolves to a real file."""
    for key in PATH_KEYS:
        value = entry.get(key)
        if value is None:
            continue
        candidates = [value] if isinstance(value, str) else value
        if not isinstance(candidates, list):
            fail(line_no, "SHAPE", "%s: %s must be a list or null."
                 % (entry.get("id"), key))
            continue
        for candidate in candidates:
            if not isinstance(candidate, str) or not candidate:
                fail(line_no, "SHAPE", "%s: %s holds a non-string path."
                     % (entry.get("id"), key))
            elif candidate.startswith("/"):
                fail(line_no, "PATH", "%s: %s names the absolute path %s. "
                     "Paths are relative to the repository root."
                     % (entry.get("id"), key, candidate))
            elif ".." in Path(candidate).parts:
                fail(line_no, "PATH", "%s: %s escapes the repository root "
                     "with %s." % (entry.get("id"), key, candidate))
            elif not (root / candidate).is_file():
                fail(line_no, "PATH", "%s: %s names %s, which is not a file "
                     "in this tree." % (entry.get("id"), key, candidate))


def check_manifest(root):
    """Returns sorted (file, line, code, message) tuples. Empty means green."""
    root = Path(root)
    problems = []

    def fail(line_no, code, message, where=MANIFEST):
        problems.append((where, line_no, code, message))

    for needed in (MANIFEST, INVARIANTS, ROUTER):
        if not (root / needed).is_file():
            fail(1, "MISSING", "%s is not in this tree; the harness contract "
                 "cannot be checked without it." % needed, needed)
    if problems:
        return sorted(problems)

    raw = (root / MANIFEST).read_text(encoding="utf-8")
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as error:
        fail(error.lineno, "JSON", "%s is not parseable: %s"
             % (MANIFEST, error.msg))
        return sorted(problems)

    rows = router_rows((root / ROUTER).read_text(encoding="utf-8"))
    known = invariant_ids((root / INVARIANTS).read_text(encoding="utf-8"))
    if not known:
        fail(1, "INVARIANT", "no invariant ids found; the seven-rule table "
             "must carry each id in backticks in its first cell.", INVARIANTS)

    entries = manifest.get("tasks")
    if not isinstance(entries, list) or not entries:
        fail(1, "SHAPE", "tasks must be a non-empty array of entries.")
        return sorted(problems)

    at = entry_lines(raw)
    line_of = lambda e: at.get(e.get("id"), 1)  # noqa: E731

    # Check 1, model gate: the whole file, keys and values alike.
    for trail, text in walk_strings(manifest, "manifest"):
        for pattern, label in MODEL_PATTERNS:
            match = re.search(pattern, text, re.I)
            if match:
                fail(1, "MODEL", "%s contains %r, which reads as %s. Tier "
                     "names only here; the mapping lives in "
                     "routing/omniroute.config.json."
                     % (trail, match.group(0), label))

    # Check 2, shape gate: required keys, ids, triggers, invariant ids.
    seen_ids = set()
    for entry in entries:
        line_no = line_of(entry)
        entry_id = entry.get("id")
        for key in REQUIRED_KEYS:
            if key not in entry:
                fail(line_no, "SHAPE", "%s is missing the required key %s."
                     % (entry_id or "an entry", key))
        if not isinstance(entry_id, str) or not ID_RE.match(entry_id or ""):
            fail(line_no, "ID", "%r is not a kebab-case id." % (entry_id,))
        elif entry_id in seen_ids:
            fail(line_no, "ID", "%s is used by more than one entry; an "
                 "adapter addresses a route by id." % entry_id)
        else:
            seen_ids.add(entry_id)
        triggers = entry.get("trigger")
        if not isinstance(triggers, list) or not triggers or not all(
                isinstance(t, str) and t.strip() for t in triggers):
            fail(line_no, "TRIGGER", "%s: trigger must be a non-empty list of "
                 "phrases lifted from the router row." % entry_id)
        binding = entry.get("invariants")
        if not isinstance(binding, list) or not binding:
            fail(line_no, "INVARIANT", "%s: invariants must name at least one "
                 "id from harness/INVARIANTS.md." % entry_id)
        else:
            for name in binding:
                if name not in known:
                    fail(line_no, "INVARIANT", "%s: %r is not defined in %s."
                         % (entry_id, name, INVARIANTS))

    # Check 3, tier gate: a tier name, never a model.
    for entry in entries:
        if entry.get("tier") not in TIERS:
            fail(line_of(entry), "TIER", "%s: tier is %r; it must be one of "
                 "%s." % (entry.get("id"), entry.get("tier"), ", ".join(TIERS)))

    # Check 4, stage and gate gate: real names, real numbers, null together.
    for entry in entries:
        line_no = line_of(entry)
        stage, gate = entry.get("stage"), entry.get("gate")
        if stage is not None and stage not in STAGES:
            fail(line_no, "STAGE", "%s: stage is %r; it must be one of %s, or "
                 "null." % (entry.get("id"), stage, ", ".join(STAGES)))
        if gate is not None and (isinstance(gate, bool) or gate not in GATES):
            fail(line_no, "GATE", "%s: gate is %r; it must be 1 to 6, or null."
                 % (entry.get("id"), gate))
        if (stage is None) != (gate is None):
            fail(line_no, "GATE", "%s: stage and gate are null only together. "
                 "A stage without its gate hides which checklist applies; a "
                 "gate without its stage names a checklist nothing feeds."
                 % entry.get("id"))

    # Check 5, path gate: every named file exists.
    for entry in entries:
        check_paths(entry, root, line_of(entry), fail)

    # Check 6, agreement gate: row to entry, entry to row, and the order.
    claims = {}
    for entry in entries:
        claimed = entry.get("router_row")
        if not isinstance(claimed, str) or not claimed.strip():
            fail(line_of(entry), "ROW", "%s: router_row must quote the router "
                 "row's own %r cell verbatim."
                 % (entry.get("id"), ROUTER_HEADER))
        else:
            claims.setdefault(claimed, []).append(entry)

    by_cell = {}
    for line_no, cell in rows:
        by_cell.setdefault(cell, []).append(line_no)

    for cell, line_numbers in sorted(by_cell.items()):
        if cell not in claims:
            fail(line_numbers[0], "ROW", "router row %r has no manifest entry. "
                 "Every row gets one, including the rows that need no skill: "
                 "give it skill null and the reads it names." % cell, ROUTER)

    for claimed, owners in sorted(claims.items()):
        if claimed not in by_cell:
            fail(line_of(owners[0]), "ROW", "%s claims router row %r, which is "
                 "not in the table in %s. Fix the manifest, never the router "
                 "table." % (owners[0].get("id"), claimed, ROUTER))
        if len(owners) > 1:
            fail(line_of(owners[1]), "ROW", "router row %r is claimed by %s. "
                 "One entry per row." % (claimed,
                                         ", ".join(o.get("id") for o in owners)))

    if len(entries) != len(rows):
        fail(1, "COUNT", "%d manifest entries against %d router rows in %s. "
             "The two faces have to agree row for row."
             % (len(entries), len(rows), ROUTER))

    order = [cell for _, cell in rows]
    claimed_order = [e.get("router_row") for e in entries]
    if sorted(order) == sorted(c for c in claimed_order if c in by_cell) \
            and order != claimed_order:
        fail(1, "ORDER", "the entries are not in router order. A reader "
             "comparing the two faces reads them side by side.")

    return sorted(problems)


def harness_present(root):
    """True when the harness directory exists.

    False means somebody deleted it, which is a supported end state: the
    harness is an adapter over a document system, not a runtime dependency.
    A tree with no harness/ has nothing to check and this gate reports ok.
    A harness/ that exists but is missing MANIFEST.json or INVARIANTS.md is
    a broken contract, not a deletion, and still fails.
    """
    return (Path(root) / HARNESS).is_dir()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=".", type=Path,
                        help="repository root (default: the current directory)")
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing on success, for CI")
    args = parser.parse_args(argv)

    if not harness_present(args.root):
        if not args.quiet:
            print("%s/: absent, nothing to check. The harness is deletable, "
                  "so this gate reports ok instead of failing. A %s/ that "
                  "exists without MANIFEST.json or INVARIANTS.md is a broken "
                  "contract and still fails." % (HARNESS, HARNESS))
        return 0

    problems = check_manifest(args.root)
    for where, line_no, code, message in problems:
        print("%s:%d: %s %s" % (where, line_no, code, message))
    if problems:
        print("\n%d problem(s). The manifest and the router table do not "
              "agree, which is the point of having a checker."
              % len(problems), file=sys.stderr)
        return 1
    if not args.quiet:
        print("%s: ok (6 checks, agrees with %s)" % (MANIFEST, ROUTER))
    return 0


if __name__ == "__main__":
    sys.exit(main())
