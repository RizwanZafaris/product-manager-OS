#!/usr/bin/env python3
"""Agreement gate for the harness contract. Standard library only.

    python3 tools/check_manifest.py
    python3 tools/check_manifest.py --quiet
    python3 tools/check_manifest.py --root /path/to/repo

Proves that harness/MANIFEST.json and the router table in CLAUDE.md are two
faces of one contract: every router row has exactly one manifest entry, every
manifest entry names a real router row, the entries are in router order, all
three router columns agree with the entry that claims the row, every path in
skill, templates and reads resolves to a real file inside this tree, every tier
is one of the three tier names, every gate is 1 to 6, every stage is a real
stage name, every invariant id is defined in harness/INVARIANTS.md, every route
binds the four universal invariants, and no model id appears anywhere in the
manifest.

The join key is the router row's own "When the user asks for" cell, stored
verbatim in each entry as router_row. Matching is exact on the collapsed cell
text, so an edit to either face that the other did not follow fails the build
rather than drifting quietly.

All three columns are checked, not just the first. The Invoke column and the
Backing-templates column used to be free to change under a green check, which
made the check a claim about one third of the table. Now the parser is anchored
on the router heading, stops at the next heading, keeps backslash-escaped pipes
and pipes inside inline code inside their cell, and fails any row in that table
whose cell count is not three. A row can no longer hide a column, and a
three-column table elsewhere in the file is no longer read as routing.

stage and gate accept null, and only together. PLANNING artifacts are reviewed
on their own cadence rather than at a gate, and reference rows (glossary,
philosophy, domain and role cards) produce no artifact at all; inventing a stage
for them would be a fabricated field. null means no gate applies, never that a
gate was skipped.

Paths are read as untrusted strings. A path is refused when it is absolute, when
it climbs out with "..", when any component below the root is a symlink, or when
its resolved real path leaves the resolved root. Path.is_file() follows symlinks,
so a manifest path symlinked to a file outside the tree is a real file to a
naive existence check, and the desktop adapter inlines the text of what it
points at. The adapter refuses the same shapes at its own read sink, because
this checker is not always what runs first.

Limits, stated rather than hidden: this checks that the two faces agree and that
the paths exist, never that a route is the right route for the request, that a
tier assignment is sensible, or that a template is the one a reader needs. The
column checks compare the paths and the skill a cell names, not its prose, so a
cell can still describe the route badly in words no checker reads. Trigger
phrases are checked for shape and for uniqueness across routes, never for
faithfulness to the cell: they are deliberate paraphrases of it. The model-id
scan is a list of vendor-shaped patterns, so an unlisted vendor's id walks
straight through. Green means the contract is consistent, not that it is wise.
Structural validity is the first of the three checks in harness/INVARIANTS.md
and it is not a quality gate.

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
ROUTER_HEADING = "## Router"
ROUTER_HEADER = ("When the user asks for", "Invoke", "Backing templates")
SEPARATOR_RE = re.compile(r"^[\s:|-]+$")
INVARIANT_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|")

# Markdown link targets and inline code spans. A router cell names files those
# two ways and no other; prose is prose.
TOKEN_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)|`([^`]+)`")

# The four that bind every route, per the universal set in
# harness/INVARIANTS.md. A route adds to this list and never subtracts from it.
UNIVERSAL_INVARIANTS = ("content-is-data", "no-fabrication", "human-signs-gate",
                        "fail-closed")

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


def split_cells(line):
    """One pipe row split into its cells, escapes and code spans respected.

    A backslash-escaped pipe and a pipe inside an inline code span belong to the
    cell they sit in. Splitting on every pipe would read one such row as four
    cells, and a checker that skips rows it cannot parse is a checker a row can
    hide from. Cell text is returned verbatim, backslashes included, so the
    manifest's router_row stays a copy of what the file actually says.
    """
    cells, buf, escaped, in_code = [], [], False, False
    for char in line:
        if escaped:
            buf.append(char)
            escaped = False
        elif char == "\\":
            buf.append(char)
            escaped = True
        elif char == "`":
            buf.append(char)
            in_code = not in_code
        elif char == "|" and not in_code:
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    cells.append("".join(buf))
    if cells and not cells[0].strip():
        cells.pop(0)
    if cells and not cells[-1].strip():
        cells.pop()
    return [c.strip() for c in cells]


def router_table(text):
    """The router table's own lines, as (line number, raw line).

    Anchored on the router heading and stopped at the next heading, so a
    three-column table anywhere else in the file is not read as routing.
    Returns None when the heading is absent, which is a failure, not an
    empty table.
    """
    lines = text.split("\n")
    start = None
    for index, line in enumerate(lines):
        if line.strip() == ROUTER_HEADING:
            start = index + 1
            break
    if start is None:
        return None
    body = []
    for index in range(start, len(lines)):
        if lines[index].lstrip().startswith("#"):
            break
        body.append((index + 1, lines[index]))
    return body


def router_rows(text):
    """Every data row of the router table, as (line number, list of cells).

    A data row is any pipe row in the table that is neither the header nor the
    separator, whatever its cell count: a row with the wrong number of cells is
    returned so the caller can fail it rather than skip it. Counting rows this
    way means a new row added to CLAUDE.md is picked up here without anyone
    remembering to update a number.
    """
    body = router_table(text)
    if body is None:
        return None
    rows = []
    for line_no, line in body:
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cell_list = split_cells(stripped)
        if not cell_list:
            continue
        first = cell_list[0]
        if not first or SEPARATOR_RE.match(first) \
                or first == ROUTER_HEADER[0]:
            continue
        rows.append((line_no, cell_list))
    return rows


def path_tokens(cell):
    """The repository paths a router cell names, in the order it names them.

    A path arrives as a markdown link target or as an inline code span. A
    directory, an external URL, a bare anchor, and a placeholder carrying < or >
    are skipped: none of them names a file an entry could hold.
    """
    found = []
    for match in TOKEN_RE.finditer(cell):
        raw = (match.group(1) or match.group(2) or "").strip()
        if not raw.endswith(".md"):
            continue
        if "<" in raw or ">" in raw or raw.startswith("#") \
                or "://" in raw or raw.startswith("mailto:"):
            continue
        found.append(raw)
    return found


def path_refused(root, rel):
    """Why this path may not be read, or None when it is safe to read.

    Path.is_file() follows symlinks, so a manifest path symlinked to a file
    outside this tree is a real file to a naive existence check. Every component
    below the root is checked with no following, and the resolved real path has
    to stay inside the resolved root.
    """
    root = Path(root).resolve()
    if not isinstance(rel, str) or not rel:
        return "is not a path"
    if rel.startswith("/"):
        return ("names the absolute path %s. Paths are relative to the "
                "repository root" % rel)
    walked = root
    for part in Path(rel).parts:
        if part == "..":
            return "escapes the repository root with %s" % rel
        walked = walked / part
        if walked.is_symlink():
            return ("passes through the symlink %s. A symlink is refused "
                    "outright: is_file() follows it, and an adapter that "
                    "inlines file text would inline whatever it points at"
                    % walked.relative_to(root).as_posix())
    real = walked.resolve()
    if not real.is_relative_to(root):
        return ("resolves to %s, which is outside this tree" % real)
    if not real.is_file():
        return "names %s, which is not a file in this tree" % rel
    return None


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
    """Every path in skill, templates and reads is a real file inside the tree."""
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
                continue
            refused = path_refused(root, candidate)
            if refused:
                fail(line_no, "PATH", "%s: %s %s."
                     % (entry.get("id"), key, refused))


def named_by(entry, keys):
    """Every path this entry names under the given keys, plus their basenames."""
    paths = []
    for key in keys:
        value = entry.get(key)
        for rel in ([value] if isinstance(value, str) else (value or [])):
            if isinstance(rel, str) and rel:
                paths.append(rel)
    return set(paths), {Path(p).name for p in paths}


def check_invoke_column(entry, cell, line_no, fail):
    """The Invoke cell agrees with the entry's skill and reads.

    Two directions. Every SKILL.md the cell names has to be the skill the entry
    names, and a cell that names no skill has to sit against skill null: that
    biconditional is what stops the invoked procedure being repointed under a
    green check. Then every other file the cell names has to be one the entry
    reads, so the cell cannot send a reader to a file the route never opens.
    """
    entry_id = entry.get("id")
    skill = entry.get("skill")
    tokens = path_tokens(cell)
    named, names = named_by(entry, ("skill", "reads"))

    invoked = sorted({t for t in tokens if t.endswith("/SKILL.md")})
    expected = [skill] if isinstance(skill, str) and skill else []
    if invoked != sorted(expected):
        fail(line_no, "INVOKE", "%s: the Invoke cell names %s and the manifest "
             "names %s. The two faces have to name the same procedure; a route "
             "whose cell names no skill carries skill null."
             % (entry_id, ", ".join(invoked) or "no skill",
                ", ".join(expected) or "no skill"), ROUTER)

    if not tokens:
        fail(line_no, "INVOKE", "%s: the Invoke cell names no file at all. A "
             "row names the skill to follow or the files that are the procedure "
             "instead; prose alone routes nobody." % entry_id, ROUTER)

    for token in tokens:
        if token in named or Path(token).name in names:
            continue
        fail(line_no, "INVOKE", "%s: the Invoke cell names %s, which the entry "
             "neither follows as its skill nor lists under reads. Add it to "
             "reads or take it out of the cell." % (entry_id, token), ROUTER)


def check_templates_column(entry, cell, line_no, fail):
    """The Backing-templates cell agrees with the entry's templates and reads.

    A cell names a path in full, by basename beside a fuller sibling, or as a
    directory it does not enumerate. The first two are checked; a directory and
    a placeholder like products/<name>/STATE.md name no single file and are
    skipped, which is stated here rather than left for a reader to infer. A
    token under templates/ has to be one of the entry's own templates, because
    that column is where the artifact is declared, and reads is not the artifact.
    """
    entry_id = entry.get("id")
    tokens = path_tokens(cell)
    lands, land_names = named_by(entry, ("templates",))
    known, known_names = named_by(entry, ("templates", "reads"))

    for token in tokens:
        name = Path(token).name
        if token.startswith("templates/"):
            if token not in lands and name not in land_names:
                fail(line_no, "TEMPLATES", "%s: the Backing-templates cell "
                     "names %s, which is not in this entry's templates. The "
                     "cell and the entry have to agree on where the output "
                     "lands." % (entry_id, token), ROUTER)
        elif token not in known and name not in known_names:
            fail(line_no, "TEMPLATES", "%s: the Backing-templates cell names "
                 "%s, which the entry lists under neither templates nor reads."
                 % (entry_id, token), ROUTER)


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

    router_text = (root / ROUTER).read_text(encoding="utf-8")
    rows = router_rows(router_text)
    if rows is None:
        fail(1, "TABLE", "no %r heading in %s. The router table is found by its "
             "heading so that no other table in the file can be read as "
             "routing." % (ROUTER_HEADING, ROUTER), ROUTER)
        return sorted(problems)

    header = [cells for _, cells in
              ((n, split_cells(line.strip()))
               for n, line in router_table(router_text)
               if line.strip().startswith("|"))
              if cells and cells[0] == ROUTER_HEADER[0]]
    if not header:
        fail(1, "TABLE", "the router table has no %r header row."
             % ROUTER_HEADER[0], ROUTER)
    elif tuple(header[0]) != ROUTER_HEADER:
        fail(1, "TABLE", "the router table's columns are %s; this checker reads "
             "%s and compares all three against the manifest."
             % (", ".join(header[0]), ", ".join(ROUTER_HEADER)), ROUTER)

    misshapen = [(line_no, cells) for line_no, cells in rows if len(cells) != 3]
    for line_no, cells in misshapen:
        fail(line_no, "TABLE", "this router row has %d cell(s), not 3. Escape a "
             "pipe inside a cell as \\| or wrap it in backticks; a row with the "
             "wrong cell count is failed here rather than skipped, because a "
             "skipped row is a row that hides." % len(cells), ROUTER)
    rows = [(line_no, cells) for line_no, cells in rows if len(cells) == 3]

    known = invariant_ids((root / INVARIANTS).read_text(encoding="utf-8"))
    if not known:
        fail(1, "INVARIANT", "no invariant ids found; the rule table in %s must "
             "carry each id in backticks in its first cell." % INVARIANTS,
             INVARIANTS)
    for name in UNIVERSAL_INVARIANTS:
        if known and name not in known:
            fail(1, "INVARIANT", "%r is a universal invariant and is not "
                 "defined in the rule table. The universal set is not optional "
                 "metadata; it binds every route." % name, INVARIANTS)

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
    trigger_owner = {}
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
        else:
            normalized = [" ".join(t.lower().split()) for t in triggers]
            if len(set(normalized)) != len(normalized):
                fail(line_no, "TRIGGER", "%s: a trigger phrase is listed twice "
                     "in this entry." % entry_id)
            for phrase, original in zip(normalized, triggers):
                if phrase != original.strip().lower():
                    fail(line_no, "TRIGGER", "%s: the trigger %r carries "
                         "padding or doubled spaces. An adapter matches on the "
                         "phrase, so the phrase is stored collapsed."
                         % (entry_id, original))
                owner = trigger_owner.setdefault(phrase, entry_id)
                if owner != entry_id:
                    fail(line_no, "TRIGGER", "%s: the trigger %r is already "
                         "claimed by %s. One phrase cannot name two routes; an "
                         "adapter matching it would pick by table order, which "
                         "is not a routing decision anyone made."
                         % (entry_id, original, owner))
        binding = entry.get("invariants")
        if not isinstance(binding, list) or not binding:
            fail(line_no, "INVARIANT", "%s: invariants must name at least one "
                 "id from harness/INVARIANTS.md." % entry_id)
        else:
            for name in binding:
                if name not in known:
                    fail(line_no, "INVARIANT", "%s: %r is not defined in %s."
                         % (entry_id, name, INVARIANTS))
            for name in UNIVERSAL_INVARIANTS:
                if name not in binding:
                    fail(line_no, "INVARIANT", "%s: the universal invariant %r "
                         "is not listed. All four of %s bind every route and "
                         "are listed on every route, so an adapter reading one "
                         "entry sees them without having to know they are "
                         "global. Route-specific ids are additions to that set, "
                         "never replacements for it."
                         % (entry_id, name, ", ".join(UNIVERSAL_INVARIANTS)))

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
                 % (entry.get("id"), ROUTER_HEADER[0]))
        else:
            claims.setdefault(claimed, []).append(entry)

    by_cell = {}
    cells_of = {}
    for line_no, cells in rows:
        by_cell.setdefault(cells[0], []).append(line_no)
        cells_of.setdefault(cells[0], (line_no, cells))

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

    order = [cells[0] for _, cells in rows]
    claimed_order = [e.get("router_row") for e in entries]
    if sorted(order) == sorted(c for c in claimed_order if c in by_cell) \
            and order != claimed_order:
        fail(1, "ORDER", "the entries are not in router order. A reader "
             "comparing the two faces reads them side by side.")

    # Checks 7 and 8, column gates: the Invoke cell and the Backing-templates
    # cell, not just the first cell. Both are compared as projections, meaning
    # the files and the skill a cell names, against the entry that claims the
    # row. A rename or a repoint in either column now fails the build.
    for entry in entries:
        row = cells_of.get(entry.get("router_row"))
        if row is None:
            continue
        line_no, cells = row
        check_invoke_column(entry, cells[1], line_no, fail)
        check_templates_column(entry, cells[2], line_no, fail)

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
        print("%s: ok (8 checks, agrees with all three columns of %s)"
              % (MANIFEST, ROUTER))
    return 0


if __name__ == "__main__":
    sys.exit(main())
