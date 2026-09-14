#!/usr/bin/env python3
"""Generator for docs/PHASE-INDEX.md, the phase index. Standard library only.

    python3 tools/phase_index.py            # write docs/PHASE-INDEX.md
    python3 tools/phase_index.py --check    # exit 1 when the committed file is stale

The index is a reading of declarations already in the tree, never a second copy:
a framework's feeds frontmatter names the templates it feeds; an example names
the template it fills on its third line; a template's stage and gate are read
the way the workspace stamps a copy of it; tools/workspace.py resolves where the
working copy lands, its artifact ID and what it depends on; and
os/STAGE-GATES.md holds the gate titles. IDs and paths are shown for a product
named ledgerline, the example product of os/PRODUCT-WORKSPACE.md.

It fails, and writes nothing, when a feed or an example names a template that
does not exist, or when a step of the journey has lost its last framework or its
last filled example. Every other gap is shown in the index rather than failed on.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "PHASE-INDEX.md"
SLUG = "ledgerline"
JOURNEY = (
    "templates/discovery/problem-framing.md",
    "templates/planning/vision.md",
    "templates/planning/product-strategy.md",
    "templates/planning/roadmap.md",
    "templates/definition/prd.md",
    "templates/architecture/development-handoff.md",
)
WEIGHTS = {"templates/definition/prd.md":
           ("templates/definition/one-pager.md",
            "templates/definition/brd.md")}
# An example names the template it fills in one of these two phrasings.
FILLS = ("Fills [templates/", "Produced with [templates/")

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import graph  # noqa: E402
import workspace  # noqa: E402
import init_product  # noqa: E402
from lint import tracked_files  # noqa: E402


def _read_text(path):
    """Read one file as text, or None when it is missing."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return None


def _link(rel):
    """A relative Markdown link from docs/ to a repo-relative file, by name."""
    return "[%s](../%s)" % (Path(rel).name, rel)


def _name_link(rel):
    """A Markdown link by file name without .md, relative from docs/."""
    return "[%s](../%s)" % (Path(rel).stem, rel)


def _shown(path):
    """A path as the messages show it: repo-relative when it is in the repo."""
    try:
        return Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def collect():
    """Read the tree's declarations into a dict for render() and problems()."""
    templates = {}
    for rel in init_product.every_shipped_template():
        if Path(rel).name == "README.md":
            continue
        text = _read_text(ROOT / rel)
        if text is None:
            continue
        # Stamped the way init_product stamps a copy, so the phase includes the
        # folder fallback for a template that declares no stage.
        artifact = workspace.parse_artifact(
            workspace.stamp_artifact(text, rel, SLUG))
        if artifact is None:  # STATE.md: a journal, not an artifact
            continue
        templates[rel] = {
            "phase": artifact.get("phase"),
            "gate": artifact.get("gate"),
            "artifact_id": artifact.get("artifact_id"),
            "depends_on": artifact.get("depends_on") or [],
            "destination": workspace.destination_for(rel, SLUG, text),
        }

    # tracked_files yields absolute paths; everything below compares
    # repo-relative ones.
    tracked = sorted(path.relative_to(ROOT).as_posix()
                     for path in tracked_files(ROOT))
    fed_by = {rel: [] for rel in templates}
    filled_by = {rel: [] for rel in templates}
    broken = set()

    # A framework lives one folder down; frameworks/README.md and INDEX.md are
    # indexes of them, not frameworks.
    for fw_rel in tracked:
        if not (fw_rel.startswith("frameworks/") and fw_rel.endswith(".md")
                and fw_rel.count("/") >= 2):
            continue
        fm = graph.frontmatter(_read_text(ROOT / fw_rel) or "")
        for named in (fm or {}).get("feeds", []):
            if not named.startswith("templates/"):
                continue
            if named in templates:
                fed_by[named].append(fw_rel)
            elif not (ROOT / named).is_file():
                broken.add((fw_rel, named))

    for ex_rel in tracked:
        if not (ex_rel.startswith("examples/") and ex_rel.endswith(".md")):
            continue
        head = "\n".join((_read_text(ROOT / ex_rel) or "").split("\n")[:8])
        for needle in FILLS:
            pos = head.find(needle)
            if pos < 0:
                continue
            end = head.find("]", pos + len(needle))
            if end < 0:
                continue
            named = "templates/" + head[pos + len(needle):end]
            if named in templates:
                filled_by[named].append(ex_rel)
            elif not (ROOT / named).is_file():
                broken.add((ex_rel, named))

    return {
        "templates": templates,
        "fed_by": {rel: sorted(found) for rel, found in fed_by.items()},
        "filled_by": {rel: sorted(found) for rel, found in filled_by.items()},
        "broken": sorted(broken),
        "gates": graph.read_gates(ROOT),
    }


def problems(index):
    """Every reason not to write the index, as sorted strings."""
    found = ["%s names %s, which is not a file" % pair
             for pair in index["broken"]]
    for rel in JOURNEY:
        if rel not in index["templates"]:
            found.append("the journey names %s, which is not a template" % rel)
            continue
        if not index["fed_by"].get(rel):
            found.append("journey step %s has no framework feeding it" % rel)
        if not index["filled_by"].get(rel):
            found.append("journey step %s has no filled example" % rel)
    return sorted(found)


def _gate_label(index, stage, gate):
    """'DEFINE, Gate 2: <title>', or the bare stage when it names no gate."""
    info = index["gates"].get(gate) if isinstance(gate, int) else None
    return "%s, Gate %d: %s" % (stage, gate, info[0]) if info else stage


def _cells(index, rel):
    """The frameworks, examples, working copy and dependency cells of a row."""
    row = index["templates"][rel]
    frameworks = index["fed_by"].get(rel) or []
    examples = index["filled_by"].get(rel) or []
    return {
        "frameworks": (", ".join(_name_link(f) for f in frameworks)
                       or "no framework feeds this template"),
        "examples": (", ".join(_name_link(e) for e in examples)
                     or "no filled example yet"),
        "copy": "`%s`, `%s`" % (row["destination"], row["artifact_id"]),
        "depends": ", ".join("`%s`" % d for d in row["depends_on"]) or "none",
    }


def render(index):
    """The index as deterministic Markdown with LF line ends."""
    templates = index["templates"]
    lines = [
        "<!-- Generated by tools/phase_index.py. Never hand-edit this file: "
        "edit the declarations in the tree and regenerate. -->",
        "",
        "# Phase index",
        "",
        "**Generated by `tools/phase_index.py`. Never hand-edit this file.** "
        "Rebuild it with `python3 tools/phase_index.py` and check it with "
        "`python3 tools/phase_index.py --check`.",
        "",
        "Every row is read from declarations already in the tree: a "
        "framework's `feeds` frontmatter, the template an example names on "
        "its third line, the template's own stage and gate, "
        "`tools/workspace.py` for where the working copy lands, its artifact "
        "ID and what it depends on, and `os/STAGE-GATES.md` for the gate "
        "titles. IDs and paths are shown for a product named ledgerline.",
        "",
        "## The journey",
        "",
        "| Step | Phase and gate | Depends on | Frameworks | Template | "
        "Filled example | Working copy |",
        "|---|---|---|---|---|---|---|",
    ]
    for step, rel in enumerate(JOURNEY, 1):
        if rel not in templates:
            lines.append("| %d | missing | | | %s | | |" % (step, rel))
            continue
        row, cells = templates[rel], _cells(index, rel)
        lines.append("| %d | %s | %s | %s | %s | %s | %s |" % (
            step, _gate_label(index, row["phase"], row["gate"]),
            cells["depends"], cells["frameworks"], _link(rel),
            cells["examples"], cells["copy"]))
    lighter, heavier = WEIGHTS["templates/definition/prd.md"]
    lines += ["", "The PRD's lighter weight is %s and its heavier weight is %s."
              % (_link(lighter), _link(heavier))]

    closes = {}
    for number, (title, stage, _feeds) in sorted(index["gates"].items()):
        closes.setdefault(stage, []).append((number, title))
    for stage in graph.STAGE_ORDER:
        members = sorted(rel for rel, row in templates.items()
                         if row["phase"] == stage)
        if not members:
            continue
        lines += ["", "## %s" % graph.STAGE_TITLES.get(stage, stage), ""]
        for number, title in closes.get(stage, []):
            lines.append("Ends at Gate %d: %s." % (number, title))
        if closes.get(stage):
            lines.append("")
        lines += ["| Template | Frameworks | Filled examples | Working copy | "
                  "Depends on |", "|---|---|---|---|---|"]
        for rel in members:
            cells = _cells(index, rel)
            lines.append("| %s | %s | %s | %s | %s |" % (
                _link(rel), cells["frameworks"], cells["examples"],
                cells["copy"], cells["depends"]))
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="regenerate in memory and fail when the committed "
                             "docs/PHASE-INDEX.md is stale")
    args = parser.parse_args(argv)

    index = collect()
    found = problems(index)
    if found:
        for problem in found:
            print("phase index: %s" % problem, file=sys.stderr)
        return 1
    payload = render(index).encode("utf-8")  # explicit LF, never translated
    shown = _shown(OUTPUT)

    if args.check:
        try:
            current = OUTPUT.read_bytes()
        except OSError:
            print("%s is missing. Run: python3 tools/phase_index.py" % shown,
                  file=sys.stderr)
            return 1
        if current != payload:
            print("%s is stale: it does not match what tools/phase_index.py "
                  "generates from the tree (byte comparison, so a stray CRLF "
                  "counts as stale too). Run: python3 tools/phase_index.py, "
                  "then commit the result." % shown, file=sys.stderr)
            return 1
        print("%s: ok (up to date)" % shown)
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(payload)
    print("%s: written" % shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
