#!/usr/bin/env python3
"""Generator for docs/GRAPH.md, the artifact-to-gate graph. Standard library only.

    python3 tools/graph.py            # write docs/GRAPH.md
    python3 tools/graph.py --check    # exit 1 when the committed file is stale

The contract, stated so a reader never has to infer it:

Inputs are two declarations that already exist in the tree, so the graph is a
reading of the repository rather than a second copy of it. First, the YAML
frontmatter "feeds" key on files under os/, knowledge/, frameworks/, templates/,
skills/, and agents/: each value is either a gate reference ("Gate 4") or a path
to another file in the tree. A SKILL.md is the one exception to where that key
lives: it declares in a SKILL.graph.yml sidecar beside it, because the Agent
Skills format validates SKILL.md frontmatter against a closed attribute list and
a graph key there breaks the skill in runtimes that enforce it. Second, the
three-line Stage/Knowledge/Skill header
that every template carries, whose Stage line names the stage the artifact serves
and the gates it feeds. Gate numbers, gate titles, and which stage each gate
closes are read from os/STAGE-GATES.md, never hardcoded here.

Output is one Mermaid flowchart with one subgraph per stage, each gate sitting in
the stage it closes. A node is emitted only when it carries at least one edge, and
an edge is emitted only where a feeds key or a Stage header declares one, because
a diagram of 200 plus files with an edge per pair is a picture of nothing.

Two properties the build depends on. The output is deterministic: every collection
is sorted before it is rendered, so regenerating an unchanged tree produces a
byte-identical file and CI can diff it. And the frontmatter pass is optional per
file: files with no frontmatter contribute whatever their template header declares
and are counted in the run report, so this script is correct on a tree where the
frontmatter is half landed.

Limits, stated rather than hidden. The frontmatter parser handles the shapes this
repository uses, a top-level "key: value" and a block sequence of "- item" under
one, and ignores nested mappings and anchors; it is not a YAML implementation and
does not pretend to be. Gate numbers are harvested from a Stage line only after
the word "feeds", so "after Gate 2 signed a baseline" is not read as an edge; a
Stage line with no "feeds" at all is harvested whole, which is how the file that
IS a gate still reaches its gate. A feeds value that resolves to nothing is
counted and listed in the output rather than guessed at. Nothing here validates
that a declared relationship is a sensible one: the graph shows what the tree
claims, and a wrong claim renders as a wrong arrow.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = "docs/GRAPH.md"
GATES_FILE = "os/STAGE-GATES.md"
SKILL_SIDECAR = "SKILL.graph.yml"

# One walker for the gate and the graph, so the two can never disagree about what
# is in the tree. lint.py is the owner; this is a caller.
sys.path.insert(0, str(ROOT))
try:
    from lint import tracked_files
except ImportError:  # pragma: no cover
    print("cannot import tracked_files from lint.py at the repo root",
          file=sys.stderr)
    raise

# Layers whose files can declare a feeds relationship. Everything else in the
# tree is prose about the system rather than a node in it.
SCAN_DIRS = ("agents", "frameworks", "knowledge", "os", "skills", "templates")

# Ordered, because the diagram reads top to bottom in loop order and the two
# tracks come after the six stages they run across.
STAGE_ORDER = ["DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER", "OPERATE",
               "PLANNING", "AI OVERLAY", "ALL STAGES"]
STAGE_TITLES = {"PLANNING": "PLANNING track",
                "AI OVERLAY": "AI overlay track",
                "ALL STAGES": "ALL STAGES, cross cutting"}
DEFAULT_STAGE = "ALL STAGES"

# Case-sensitive on purpose: the stage tokens are written in capitals in every
# header, and a case-blind match would read the word "design" in a sentence about
# design work as a stage declaration.
CASED_TOKENS = ["DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER", "OPERATE",
                "PLANNING"]
LOOSE_TOKENS = [("ai overlay", "AI OVERLAY"), ("all stages", "ALL STAGES"),
                ("any stage", "ALL STAGES"), ("every stage", "ALL STAGES")]

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_ITEM_RE = re.compile(r"^\s*-\s+(.*)$")
FM_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
STAGE_LINE_RE = re.compile(r"^\**Stage:\**\s*(.+)$")
FEEDS_SPLIT_RE = re.compile(r"\bfeeds?\b", re.I)
GATE_REF_RE = re.compile(r"\bGates?\s+((?:\d\s*(?:,|and|to)\s*)*\d)")
GATE_HEADING_RE = re.compile(r"^##\s+Gate\s+(\d):\s+(.+?)\s*$")
GATE_FLOW_RE = re.compile(r"^Closes\s+([A-Z]+)\.\s*(?:Feeds|Loops back to)\s+"
                          r"([A-Z]+)\.")
HEADER_SCAN_LINES = 8

# Mermaid edge shapes. A gate arrow is the spine, an artifact arrow is a handoff
# between two documents, and the thick arrow is the loop between gates.
FEEDS_GATE = "-->"
FEEDS_FILE = "-.->"
GATE_TO_GATE = "==>"
EDGE_KINDS = [(FEEDS_GATE, "an artifact feeds a gate"),
              (FEEDS_FILE, "an artifact feeds another artifact"),
              (GATE_TO_GATE, "a gate opens the next stage")]


def read(path):
    """Text of one file, or None when it is not readable as UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def split_inline(value):
    """Split a scalar or an inline list into stripped, unquoted values."""
    text = value.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    parts = [p.strip().strip("'\"") for p in text.split(",")]
    return [p for p in parts if p]


def frontmatter(raw):
    """Parse a leading YAML block into {key: [values]}, or None when absent."""
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return None
    data, key = {}, None
    for line in match.group(1).split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
        item = FM_ITEM_RE.match(line)
        if item and key:
            data[key].append(item.group(1).strip().strip("'\""))
            continue
        field = FM_FIELD_RE.match(line)
        if field:
            key = field.group(1).lower()
            data[key] = split_inline(field.group(2))
    return data


def declared_frontmatter(path, raw):
    """The declaration this file makes to the graph, wherever it keeps it.

    A SKILL.md keeps the two-key Agent Skills contract in its own frontmatter
    and its graph keys in a SKILL.graph.yml sidecar beside it, because a
    runtime that validates SKILL.md frontmatter against a closed attribute list
    rejects the file outright on an unknown key. Read both and merge, sidecar
    winning, so a skill is a node here without being a broken skill there.
    """
    data = frontmatter(raw)
    if path.name != "SKILL.md":
        return data
    text = read(path.parent / SKILL_SIDECAR)
    if text is None:
        return data
    merged = dict(data or {})
    merged.update(frontmatter("---\n%s\n---\n" % text.strip("\n")) or {})
    return merged


def gates_in(text):
    """Gate numbers a piece of text declares as fed.

    Only the part after the first "feeds" or "feed" counts, so a Stage line that
    mentions a gate as history rather than as a destination does not become an
    edge. A line with no such word is read whole, which is the case for the one
    template that is a gate rather than an input to one.
    """
    halves = FEEDS_SPLIT_RE.split(text, 1)
    scope = halves[1] if len(halves) > 1 else text
    found = set()
    for match in GATE_REF_RE.finditer(scope):
        found.update(int(d) for d in re.findall(r"\d", match.group(1)))
    return found


def stage_in(text):
    """The stage a Stage line names, or None. Earliest token wins.

    "BUILD into DELIVER" is primarily a BUILD artifact, and reading the earliest
    token gives that answer without a second rule.
    """
    hits = []
    for token in CASED_TOKENS:
        at = text.find(token)
        if at != -1:
            hits.append((at, token))
    lowered = text.lower()
    for token, stage in LOOSE_TOKENS:
        at = lowered.find(token)
        if at != -1:
            hits.append((at, stage))
    return min(hits)[1] if hits else None


def stage_header(raw):
    """The Stage line from a three-line template header, or None.

    The window starts under any frontmatter. The graph declaration sits above
    the header, and counting from byte zero would push the header out of range
    on every file that carries one.
    """
    match = FRONTMATTER_RE.match(raw)
    raw = raw[match.end():] if match else raw
    for line in raw.split("\n")[:HEADER_SCAN_LINES]:
        match = STAGE_LINE_RE.match(line.strip())
        if match:
            return match.group(1).strip()
    return None


def read_gates(root):
    """Gate number to (title, closes stage, feeds stage), from STAGE-GATES.md."""
    raw = read(root / GATES_FILE)
    if raw is None:
        return {}
    gates, current = {}, None
    for line in raw.split("\n"):
        heading = GATE_HEADING_RE.match(line)
        if heading:
            current = int(heading.group(1))
            gates[current] = [heading.group(2), DEFAULT_STAGE, None]
            continue
        flow = GATE_FLOW_RE.match(line.strip())
        if flow and current is not None:
            gates[current][1] = flow.group(1)
            gates[current][2] = flow.group(2)
    return {n: tuple(v) for n, v in gates.items()}


def node_id(rel):
    """A Mermaid-safe id for a path. Letters, digits, and underscores only."""
    return "n_" + re.sub(r"[^0-9A-Za-z]", "_", rel)


def label_for(rel):
    """A short label: the last two path parts, with the extension dropped.

    A directory's own file (SKILL.md, README.md) is named by its directory, since
    twenty nodes labeled SKILL would be twenty nodes labeled nothing.
    """
    parts = rel.split("/")
    stem = parts[-1][:-3] if parts[-1].endswith(".md") else parts[-1]
    chain = parts[:-1] if stem in ("SKILL", "README") else parts[:-1] + [stem]
    return "/".join(chain[-2:]) if chain else stem


def clean_label(text):
    """Text safe inside a quoted Mermaid label."""
    return re.sub(r"\s+", " ", text.replace('"', "'").replace("|", "/")).strip()


def resolve(value, rel, tree):
    """What one feeds value points at: [("gate", n)], [("file", rel)], or []."""
    if re.search(r"\bgates?\b", value, re.I):
        return [("gate", n) for n in sorted(gates_in(value))]
    target = value.split("#")[0].strip().strip("`")
    if not target or target.startswith(("http://", "https://", "mailto:", "/")):
        return []
    if target in tree:
        return [("file", target)]
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
    return [("file", joined)] if joined in tree else []


def collect(root):
    """Walk the tree once and return everything the renderer needs.

    The return value is a dict rather than a tuple because seven positional
    values at a call site is a puzzle for the next reader.
    """
    gates = read_gates(root)
    files = [p for p in tracked_files(root)
             if p.suffix == ".md"
             and p.relative_to(root).as_posix().split("/")[0] in SCAN_DIRS
             and not p.relative_to(root).as_posix().startswith("modules/")]
    rels = [p.relative_to(root).as_posix() for p in files]
    tree = set(rels)

    stages, declared, unresolved = {}, {}, []
    with_fm, without_fm, with_feeds = [], [], []
    for path, rel in sorted(zip(files, rels), key=lambda pair: pair[1]):
        raw = read(path)
        if raw is None:
            continue
        data = declared_frontmatter(path, raw)
        (with_fm if data is not None else without_fm).append(rel)
        header = stage_header(raw)

        stage = None
        if data and data.get("stage"):
            stage = stage_in(data["stage"][0].upper())
        if stage is None and header:
            stage = stage_in(header)
        stages[rel] = stage or DEFAULT_STAGE

        targets = []
        if header:
            targets.extend(("gate", n) for n in sorted(gates_in(header)))
        feeds = (data or {}).get("feeds", [])
        if feeds:
            with_feeds.append(rel)
        for value in feeds:
            hits = resolve(value, rel, tree)
            if hits:
                targets.extend(hits)
            else:
                unresolved.append((rel, value))
        declared[rel] = sorted(set(targets))

    return {"gates": gates, "stages": stages, "declared": declared,
            "with_fm": sorted(with_fm), "without_fm": sorted(without_fm),
            "with_feeds": sorted(with_feeds),
            "unresolved": sorted(set(unresolved)), "scanned": len(rels)}


def build(data):
    """Turn declarations into (nodes by stage, sorted edges)."""
    gates, stages, declared = data["gates"], data["stages"], data["declared"]
    gate_id = {n: "G%d" % n for n in gates}

    edges, live = set(), set()
    for rel in sorted(declared):
        for kind, target in declared[rel]:
            if kind == "gate" and target in gate_id:
                edges.add((FEEDS_GATE, node_id(rel), gate_id[target]))
                live.add(rel)
            elif kind == "file" and target in stages and target != rel:
                edges.add((FEEDS_FILE, node_id(rel), node_id(target)))
                live.update((rel, target))
    for number in sorted(gates):
        nxt = next((n for n in sorted(gates)
                    if gates[n][1] == gates[number][2]), None)
        if nxt is not None and nxt != number:
            edges.add((GATE_TO_GATE, gate_id[number], gate_id[nxt]))

    nodes = {stage: [] for stage in STAGE_ORDER}
    for number in sorted(gates):
        title, closes, _ = gates[number]
        stage = closes if closes in nodes else DEFAULT_STAGE
        nodes[stage].append((gate_id[number],
                             clean_label("Gate %d: %s" % (number, title)),
                             True))
    for rel in sorted(live):
        stage = stages[rel] if stages[rel] in nodes else DEFAULT_STAGE
        nodes[stage].append((node_id(rel), clean_label(label_for(rel)), False))
    for stage in nodes:
        nodes[stage].sort()

    order = {shape: i for i, (shape, _) in enumerate(EDGE_KINDS)}
    return nodes, sorted(edges, key=lambda e: (order[e[0]], e[1], e[2]))


def mermaid(nodes, edges):
    """Render the flowchart. One subgraph per stage, edges after the subgraphs."""
    out = ["```mermaid", "flowchart LR"]
    for stage in STAGE_ORDER:
        if not nodes[stage]:
            continue
        title = STAGE_TITLES.get(stage, stage)
        out.append('  subgraph s_%s["%s"]' % (re.sub(r"[^0-9A-Za-z]", "_", stage),
                                              title))
        out.append("    direction LR")
        for ident, label, _ in nodes[stage]:
            out.append('    %s["%s"]' % (ident, label))
        out.append("  end")
    for shape, src, dst in edges:
        out.append("  %s %s %s" % (src, shape, dst))
    gate_ids = sorted(i for stage in nodes for i, _, is_gate in nodes[stage]
                      if is_gate)
    if gate_ids:
        out.append("  classDef gate stroke-width:3px")
        out.append("  class %s gate" % ",".join(gate_ids))
    out.append("```")
    return "\n".join(out)


def render(data):
    """The whole of docs/GRAPH.md as one string."""
    nodes, edges = build(data)
    node_count = sum(len(v) for v in nodes.values())
    artifacts = node_count - sum(1 for stage in nodes
                                 for _, _, is_gate in nodes[stage] if is_gate)
    lines = [
        "<!-- Generated by tools/graph.py. Never hand-edit this file: edit the "
        "declarations in the tree and regenerate. -->",
        "",
        "# Artifact and gate graph",
        "",
        "**Generated by `tools/graph.py`. Never hand-edit this file.** Run "
        "`python3 tools/graph.py` to rebuild it and commit the result; "
        "`python3 tools/graph.py --check` regenerates in memory and fails the "
        "build when the committed copy is stale.",
        "",
        "Two declarations already in the tree produce everything below: the "
        "frontmatter `feeds` key, and the Stage line of the three-line header "
        "every template in [templates/](../templates/README.md) carries. Gate "
        "numbers, gate titles, and the stage each gate closes are read from "
        "[os/STAGE-GATES.md](../os/STAGE-GATES.md). Nothing is asserted here "
        "that is not written somewhere else first, which is the only reason a "
        "generated map is worth keeping: it cannot drift from the files it "
        "describes without the check flag noticing.",
        "",
        "## How to read it",
        "",
        "One subgraph per stage of the loop in "
        "[os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md), plus the two tracks "
        "that run across every stage. Each gate sits inside the stage it "
        "closes. A file appears only when it declares at least one "
        "relationship, so a node missing from the diagram is a file that has "
        "not said what it feeds yet, not a file outside the system.",
        "",
        "| Arrow | Meaning |",
        "|---|---|",
    ]
    for shape, meaning in EDGE_KINDS:
        lines.append("| `%s` | %s |" % (shape, meaning))
    lines += [
        "",
        "## What this run read",
        "",
        "| Measure | Count |",
        "|---|---|",
        "| Files scanned in the six declaring layers | %d |" % data["scanned"],
        "| Files carrying frontmatter of any shape | %d |" % len(data["with_fm"]),
        "| Files with no frontmatter yet | %d |" % len(data["without_fm"]),
        "| Files declaring a `feeds` key | %d |" % len(data["with_feeds"]),
        "| Nodes in the diagram | %d |" % node_count,
        "| Artifact nodes | %d |" % artifacts,
        "| Edges in the diagram | %d |" % len(edges),
        "| Feeds values that resolved to nothing | %d |"
        % len(data["unresolved"]),
        "",
        "A file with no frontmatter is not an error, and a file with "
        "frontmatter has not necessarily declared a feed: every SKILL.md and "
        "agent file carries a name and a description already. The `feeds` pass "
        "lands file by file, and until it reaches a file, that file still "
        "contributes whatever its Stage header declares.",
        "",
        "## The graph",
        "",
        mermaid(nodes, edges),
        "",
        "## Coverage by stage",
        "",
        "| Stage | Gates | Artifacts with a declared relationship |",
        "|---|---|---|",
    ]
    for stage in STAGE_ORDER:
        if not nodes[stage]:
            continue
        gate_names = sorted(label.split(":")[0] for _, label, is_gate
                            in nodes[stage] if is_gate)
        count = sum(1 for _, _, is_gate in nodes[stage] if not is_gate)
        lines.append("| %s | %s | %d |"
                     % (STAGE_TITLES.get(stage, stage),
                        ", ".join(gate_names) or "none", count))
    if data["unresolved"]:
        lines += [
            "",
            "## Feeds values that resolved to nothing",
            "",
            "Each row is a `feeds` value that names neither a gate nor a file "
            "in the tree. Fix the declaration in the source file; this page "
            "regenerates.",
            "",
            "| File | Value |",
            "|---|---|",
        ]
        for rel, value in data["unresolved"]:
            lines.append("| `%s` | `%s` |" % (rel, clean_label(value)))
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="regenerate in memory and fail when the committed "
                             "docs/GRAPH.md is stale")
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="repository root (defaults to this script's repo)")
    args = parser.parse_args(argv)

    data = collect(args.root)
    text = render(data)
    target = args.root / OUTPUT

    if args.check:
        current = read(target)
        if current is None:
            print("%s is missing. Run: python3 tools/graph.py" % OUTPUT,
                  file=sys.stderr)
            return 1
        if current != text:
            print("%s is stale: it does not match what tools/graph.py "
                  "generates from the tree. Run: python3 tools/graph.py, then "
                  "commit the result." % OUTPUT, file=sys.stderr)
            return 1
        print("%s: ok (up to date, %d files scanned)"
              % (OUTPUT, data["scanned"]))
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    nodes, edges = build(data)
    print("%s: written" % OUTPUT)
    print("  files scanned: %d (%d with frontmatter, %d without, %d declaring "
          "a feeds key)" % (data["scanned"], len(data["with_fm"]),
                            len(data["without_fm"]), len(data["with_feeds"])))
    print("  nodes: %d, edges: %d, unresolved feeds values: %d"
          % (sum(len(v) for v in nodes.values()), len(edges),
             len(data["unresolved"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
