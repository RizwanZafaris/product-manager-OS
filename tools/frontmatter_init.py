#!/usr/bin/env python3
"""Derive the graph frontmatter across the six declaring layers. Stdlib only.

    python3 tools/frontmatter_init.py            # write the missing keys
    python3 tools/frontmatter_init.py --dry-run  # report only, change nothing

Every file under os/, knowledge/, frameworks/, templates/, skills/, and agents/
carries six keys that the graph and lint check 10 read:

    layer    the top directory the file lives in
    stage    the stage or cross-cutting track the file serves
    gate     the gate this file is first required at, 1 to 6
    feeds    up to three downstream artifacts, repo-root-relative paths
    method   the knowledge card that governs the file, or "" when none does
    aliases  the names a reader is likely to write in a wikilink

Nothing here is invented. Every value is read off a declaration the tree already
carries: the three-line Stage/Knowledge/Skill header on templates, the "## Feeds"
and "## Used by" and "## Files this skill drives" and "## Hand off to" sections,
the gate table in a stage map, and the H1 title. Where a file declares nothing,
the field lands empty ("" or []) rather than guessed at, because a wrong feeds
path fails the gate and a wrong method sends a reader to the wrong book.

Two properties this script is built around.

It never clobbers. An existing frontmatter block is kept line for line, and only
the keys it is missing are appended before its closing fence. A human who edits a
derived value keeps that edit through every later run, which is the whole point:
the script is a first pass, not an owner.

It is idempotent. A second run over an unchanged tree finds every key present and
writes nothing, so the script can go in a hook or a CI step without producing a
diff of its own.

Limits, stated rather than hidden. SKILL.md files do NOT get these keys in their
frontmatter: the Agent Skills format validates SKILL.md frontmatter against a
closed attribute list, so an unknown key there is a load error in some runtimes.
Their declaration lives in a SKILL.graph.yml sidecar beside the SKILL.md, same
six keys, same rules. The feeds list is capped at three targets, taken in the
order the source section declares them, because these lists are written most
important first and a graph carrying every declared pair is a picture of nothing.
Aliases are made unique across the tree by first claim in sorted path order, so
one alias resolves to one file. And nothing here checks that a declaration is
sensible: lint check 10 checks that the paths resolve, and a resolvable arrow
pointing at the wrong file is still a wrong arrow.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# One walker for the gate, the graph, and this script, so the three can never
# disagree about what is in the tree. lint.py is the owner; this is a caller.
sys.path.insert(0, str(ROOT))
try:
    from lint import tracked_files
except ImportError:  # pragma: no cover
    print("cannot import tracked_files from lint.py at the repo root",
          file=sys.stderr)
    raise

LAYERS = ("agents", "frameworks", "knowledge", "os", "skills", "templates")
KEYS = ("layer", "stage", "gate", "feeds", "method", "aliases")
SIDECAR = "SKILL.graph.yml"

STAGES = ("DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER", "OPERATE")
TRACKS = ("PLANNING", "AI OVERLAY", "ALL STAGES")
STAGE_GATE = {name: number for number, name in enumerate(STAGES, 1)}
GATE_STAGE = {number: name for name, number in STAGE_GATE.items()}
DEFAULT_STAGE = "ALL STAGES"

MAX_FEEDS = 3
MAX_ALIASES = 3
HEADER_SCAN_LINES = 8

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):")
STAGE_LINE_RE = re.compile(r"^\**Stage:\**\s*(.+)$")
KNOWLEDGE_LINE_RE = re.compile(r"^\**Knowledge:\**\s*(.+)$")
GATE_REF_RE = re.compile(r"\bGates?\s+((?:[1-6]\s*(?:,|and|or|to)\s*)*[1-6])")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BARE_PATH_RE = re.compile(r"((?:\.\./)+[A-Za-z0-9._/-]+\.md)")
HEADING_RE = re.compile(r"^(#{2,3})\s+(\S.*)$")
TITLE_RE = re.compile(r"^#\s+(\S.*)$")
PLACEHOLDER_RE = re.compile(r"\[[^\]]*\]|<[^>]*>")

# Case-sensitive for the six stages and PLANNING, because the words are written
# in capitals in every header and a case-blind match reads the ordinary English
# word "design" in a sentence about design work as a stage declaration.
LOOSE_TOKENS = (("ai overlay", "AI OVERLAY"), ("all stages", "ALL STAGES"),
                ("any stage", "ALL STAGES"), ("every stage", "ALL STAGES"))

# Read in this order; the first section a file carries is the one that speaks
# for it. Each is an existing convention in the tree, not a new one. "## Exit
# gate" is deliberately absent: it names a gate, which is the gate key's job,
# and the artifacts it happens to link are reviewers rather than outputs.
FEED_SECTIONS = ("## Feeds", "## Where the output lands", "## Used by",
                 "## Files this skill drives", "## Hand off to",
                 "## Where this sits in the loop", "## Where to go")

# Which layers a layer is allowed to feed. The tree flows one way: a knowledge
# card informs a worksheet, a worksheet lands in a template, a template answers
# to a gate. Without this, a "## Feeds" bullet naming the card behind a method
# renders as a template feeding its own source, and the graph reads backwards.
DOWNSTREAM = {"knowledge": {"frameworks", "templates", "skills"},
              "frameworks": {"frameworks", "templates"},
              "templates": {"templates"},
              "skills": {"skills", "templates"},
              "agents": {"agents", "templates"},
              "os": {"os", "skills", "templates"}}

# Never a feeds target. The first two are the gate and the loop themselves, and
# that relationship is the gate key. A README or an INDEX is a directory's
# rendered face, not an artifact anything hands work to.
NOT_A_TARGET = ("os/STAGE-GATES.md", "os/OPERATING-LOOP.md")
NOT_A_TARGET_NAMES = ("README.md", "INDEX.md")

# Sections that name the gate a file answers to, when no Stage header does.
GATE_SECTIONS = ("## Exit gate", "## The gate this stage ends at", "## Feeds",
                 "## Where it sits in the loop", "## Where this sits in the loop",
                 "## Hand off to")

# Sections that name the stage a file serves, when no Stage header does.
STAGE_SECTIONS = ("## Where it sits in the loop", "## Where this sits in the loop",
                  "## Feeds", "## The gate this stage ends at")


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def split_frontmatter(raw):
    """Return (frontmatter body or None, the rest of the file)."""
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return None, raw
    return match.group(1), raw[match.end():]


def frontmatter_keys(block):
    """Top-level keys of a frontmatter block, in declaration order."""
    keys = []
    for line in block.split("\n"):
        if not line.strip() or line.startswith((" ", "\t", "-", "#")):
            continue
        match = FM_KEY_RE.match(line)
        if match:
            keys.append(match.group(1).lower())
    return keys


def headings(body):
    """{heading line: (start, end)} over the body's lines, ## and ### only."""
    lines = body.split("\n")
    heads = [(i, m.group(1), m.group(0).strip())
             for i, m in ((i, HEADING_RE.match(ln)) for i, ln in enumerate(lines))
             if m]
    spans = {}
    for position, (index, hashes, text) in enumerate(heads):
        end = next((j for j, deeper, _ in heads[position + 1:]
                    if len(deeper) <= len(hashes)), len(lines))
        spans.setdefault(text, (index, end))
    return lines, spans


def section_text(lines, spans, wanted):
    """The text under the first of `wanted` headings this file carries."""
    for name in wanted:
        for heading, (start, end) in spans.items():
            if heading.lower().startswith(name.lower()):
                return "\n".join(lines[start:end])
    return ""


def header_line(body, pattern):
    """A three-line-header field from the top of the body, or None."""
    for line in body.split("\n")[:HEADER_SCAN_LINES]:
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip()
    return None


def stage_in(text):
    """The stage a piece of text names, earliest token wins, or None."""
    hits = []
    for token in STAGES + ("PLANNING",):
        at = text.find(token)
        if at != -1:
            hits.append((at, token))
    lowered = text.lower()
    for token, stage in LOOSE_TOKENS:
        at = lowered.find(token)
        if at != -1:
            hits.append((at, stage))
    return min(hits)[1] if hits else None


def gates_in(text, after_feeds=False):
    """Gate numbers a piece of text names, in the order it names them.

    Order, not sorted order, because the first gate a declaration names is the
    one it is about: "feeds Gate 4, which checks every change since Gate 2"
    is a statement about Gate 4, and sorting it hands back Gate 2.

    With after_feeds, only the part following the first "feeds" counts, so a
    Stage line that mentions a gate as history rather than as a destination is
    not read as a declaration. A line with no such word is read whole.
    """
    scope = text
    if after_feeds:
        halves = re.split(r"\bfeeds?\b", text, 1, flags=re.I)
        scope = halves[1] if len(halves) > 1 else text
    found = []
    for match in GATE_REF_RE.finditer(scope):
        for digit in re.findall(r"[1-6]", match.group(1)):
            if int(digit) not in found:
                found.append(int(digit))
    return found


def link_targets(text):
    """Every link-shaped and bare relative path in a piece of text, in order."""
    out = []
    for match in MD_LINK_RE.finditer(text):
        out.append(match.group(1))
    for match in BARE_PATH_RE.finditer(MD_LINK_RE.sub(" ", text)):
        out.append(match.group(1))
    return out


def resolve(target, rel, tree):
    """A link target as a repo-root-relative path in the tree, or None."""
    target = target.split("#")[0].strip().strip("`")
    if not target or target.startswith(("http://", "https://", "mailto:", "/")):
        return None
    if target in tree:
        return target
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
    return joined if joined in tree else None


def first_sentence(text):
    """The opening sentence, which is where a description declares its stage.

    Agent and skill descriptions follow one shape: what this is, then a "Use
    when" clause full of incidental mentions. "relitigated during BUILD" in a
    trigger clause is not a stage declaration, and reading the whole field
    would file a DEFINE-stage reviewer under BUILD.
    """
    return re.split(r"(?<=[a-z])\.\s", text, 1)[0]


def gate_hint(rel, lines, spans, description):
    """The first gate a file's own prose names, or None."""
    found = gates_in(section_text(lines, spans, GATE_SECTIONS))
    if not found and rel.split("/")[0] in ("agents", "skills"):
        found = gates_in(description)
    return found[0] if found else None


def derive_stage(rel, body, lines, spans, description):
    """The stage this file serves, from what the file already declares.

    Order of authority: the template header says it outright; a stage map is
    named for its stage; an agent or skill description names the stage it is
    for; a "where it sits in the loop" section says it in prose; and a file
    that names only a gate is placed in the stage that gate closes.
    """
    header = header_line(body, STAGE_LINE_RE)
    if header:
        found = stage_in(header)
        if found:
            return found
    parts = rel.split("/")
    if parts[:2] == ["os", "maps"]:
        named = parts[2][:-3].upper()
        if named in STAGES:
            return named
    if parts[0] in ("agents", "skills") and description:
        found = stage_in(first_sentence(description))
        if found:
            return found
    found = stage_in(section_text(lines, spans, STAGE_SECTIONS))
    if found:
        return found
    hint = gate_hint(rel, lines, spans, description)
    return GATE_STAGE[hint] if hint in GATE_STAGE else DEFAULT_STAGE


def derive_gate(rel, body, lines, spans, stage, description):
    """The gate this file answers to, 1 to 6.

    A template header that names the gate it feeds wins, because that is the
    file stating its own destination and it is occasionally not the gate that
    closes its stage. Otherwise a file in one of the six stages answers to that
    stage's gate, and a cross-cutting file answers to the earliest gate its own
    prose says reads it. Gate 1 is the floor: everything is on the table by the
    first gate at the latest.
    """
    header = header_line(body, STAGE_LINE_RE)
    if header:
        found = gates_in(header, after_feeds=True)
        if found:
            return found[0]
    if stage in STAGE_GATE:
        return STAGE_GATE[stage]
    hint = gate_hint(rel, lines, spans, description)
    return hint if hint else 1


def derive_method(rel, body, lines, spans, tree):
    """The knowledge card that governs this file, or "" when none does.

    Each layer has one place where it names its method, and only that place is
    read. A knowledge card is itself the method and never points at another.
    """
    layer = rel.split("/")[0]
    if layer == "knowledge":
        return ""
    if layer == "templates":
        source = header_line(body, KNOWLEDGE_LINE_RE) or ""
    elif layer == "frameworks":
        source = "\n".join(ln for ln in body.split("\n")
                           if "Method background" in ln)
        # Several worksheets say outright that no card covers their method and
        # then name the nearest neighbour. The nearest neighbour is not the
        # governing method, and this field stays empty rather than pointing at
        # the wrong book.
        if re.search(r"\bno\b[^.;]*\bcard\b", source, re.I):
            return ""
    elif layer == "skills":
        source = section_text(lines, spans, ("## Files this skill drives",))
    else:
        return ""
    for target in link_targets(source):
        hit = resolve(target, rel, tree)
        if hit and hit.startswith("knowledge/"):
            return hit
    return ""


def is_target(hit, rel):
    """True when `hit` is a legitimate downstream artifact of `rel`."""
    if hit == rel or hit in NOT_A_TARGET:
        return False
    if hit.split("/")[-1] in NOT_A_TARGET_NAMES:
        return False
    return hit.split("/")[0] in DOWNSTREAM.get(rel.split("/")[0], set())


def derive_feeds(rel, body, lines, spans, tree):
    """Up to three downstream artifacts this file declares, in its own order."""
    inline = "\n".join(ln for ln in body.split("\n")
                       if re.match(r"^\**Feeds:\**", ln.strip()))
    source = inline or section_text(lines, spans, FEED_SECTIONS)
    out = []
    for target in link_targets(source):
        hit = resolve(target, rel, tree)
        if hit and is_target(hit, rel) and hit not in out:
            out.append(hit)
        if len(out) == MAX_FEEDS:
            break
    return out


def title_of(body):
    """The H1 title as a lookup name, or "".

    Everything after the first colon is dropped: an H1 in this tree is a name
    followed by either a fill-in field or a subtitle, and neither is a name a
    reader would type into a wikilink.
    """
    for line in body.split("\n")[:HEADER_SCAN_LINES + 4]:
        match = TITLE_RE.match(line)
        if match:
            title = match.group(1).strip()
            head = title.split(":")[0].strip()
            if len(head) >= 3:
                title = head
            title = PLACEHOLDER_RE.sub("", title)
            return re.sub(r"\s+", " ", title).strip(" :,.")
    return ""


def acronym(text):
    words = [w for w in re.findall(r"[A-Za-z]+", text) if len(w) > 2]
    return "".join(w[0] for w in words).upper()


def derive_aliases(rel, body, existing_name):
    """The names a reader is likely to write in a wikilink to this file."""
    stem = rel.split("/")[-1][:-3]
    title = title_of(body)
    out = []
    if stem.isalpha() and len(stem) <= 4 and acronym(title) == stem.upper():
        out.append(stem.upper())
    if title:
        out.append(title)
    if existing_name:
        out.append(existing_name)
    elif stem not in ("README", "INDEX", "SKILL", "TEAM"):
        out.append(stem)
    seen, unique = set(), []
    for alias in out:
        if alias and alias.lower() not in seen:
            seen.add(alias.lower())
            unique.append(alias)
    return unique[:MAX_ALIASES]


def quote(text):
    """A double-quoted YAML scalar. The tree contains no quotes to escape."""
    return '"%s"' % text.replace('"', "'")


def render(values, keys):
    """The frontmatter lines for `keys`, in the declared key order."""
    lines = []
    for key in keys:
        value = values[key]
        if key == "gate":
            lines.append("gate: %d" % value)
        elif key in ("feeds", "aliases"):
            lines.append("%s: [%s]"
                         % (key, ", ".join(quote(v) for v in value)))
        elif key in ("layer", "stage"):
            # Plain scalars: one word, or two capitalized ones. Quoting a
            # controlled vocabulary adds noise and hides a typo in it.
            lines.append("%s: %s" % (key, value))
        else:
            lines.append("%s: %s" % (key, quote(value)))
    return lines


def collect(root):
    """Derive the six keys for every file in the six declaring layers."""
    files = [p for p in tracked_files(root)
             if p.suffix == ".md"
             and p.relative_to(root).as_posix().split("/")[0] in LAYERS
             and not p.relative_to(root).as_posix().startswith("modules/")]
    rels = sorted(p.relative_to(root).as_posix() for p in files)
    tree = set(rels)

    # An alias is claimed by exactly one file, first claim winning, so that a
    # wikilink written by name lands somewhere definite. README.md is read
    # before INDEX.md in the same directory because convention 10 makes the
    # README the directory's face and the INDEX a two-line pointer to it.
    claimed, out = {}, {}
    for rel in sorted(rels, key=lambda r: (posixpath.dirname(r),
                                           r.endswith("/INDEX.md"), r)):
        raw = read(root / rel)
        if raw is None:
            continue
        block, body = split_frontmatter(raw)
        existing = frontmatter_keys(block) if block is not None else []
        lines, spans = headings(body)
        name, description = "", ""
        for line in (block or "").split("\n"):
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("'\"")
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip()

        stage = derive_stage(rel, body, lines, spans, description)
        gate = derive_gate(rel, body, lines, spans, stage, description)
        aliases = []
        for alias in derive_aliases(rel, body, name):
            if claimed.setdefault(alias.lower(), rel) == rel:
                aliases.append(alias)
        out[rel] = {
            "layer": rel.split("/")[0],
            "stage": stage,
            "gate": gate,
            "feeds": derive_feeds(rel, body, lines, spans, tree),
            "method": derive_method(rel, body, lines, spans, tree),
            "aliases": aliases,
            "_existing": existing,
            "_has_block": block is not None,
        }
    return out


def apply(root, values, dry_run=False):
    """Write the missing keys. Returns (created, extended, untouched, sidecars)."""
    created = extended = untouched = sidecars = 0
    for rel in sorted(values):
        derived = values[rel]
        path = root / rel
        if path.name == "SKILL.md":
            target, own = path.parent / SIDECAR, None
            raw = read(target)
            block = raw if raw is not None else None
            existing = frontmatter_keys(block) if block is not None else []
        else:
            target = path
            own = read(path)
            block, body = split_frontmatter(own)
            existing = derived["_existing"]

        missing = [k for k in KEYS if k not in existing]
        if not missing:
            untouched += 1
            continue
        added = render(derived, missing)

        if target.name == SIDECAR:
            text = "\n".join((block.rstrip("\n").split("\n") if block else [])
                             + added) + "\n"
            sidecars += 1
        elif block is None:
            text = "---\n" + "\n".join(added) + "\n---\n" + own
            created += 1
        else:
            text = ("---\n" + block.rstrip("\n") + "\n" + "\n".join(added)
                    + "\n---\n" + body)
            extended += 1
        if not dry_run:
            target.write_text(text, encoding="utf-8")
    return created, extended, untouched, sidecars


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change and write nothing")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)

    values = collect(args.root)
    created, extended, untouched, sidecars = apply(args.root, values,
                                                   dry_run=args.dry_run)
    empty_feeds = sum(1 for v in values.values() if not v["feeds"])
    empty_method = sum(1 for v in values.values() if not v["method"])
    print("%s%d files in the six layers"
          % ("dry run: " if args.dry_run else "", len(values)))
    print("  frontmatter created: %d, extended: %d, already complete: %d, "
          "sidecars written: %d" % (created, extended, untouched, sidecars))
    print("  files with no declared feeds: %d, with no governing method: %d"
          % (empty_feeds, empty_method))
    for stage in STAGES + TRACKS:
        count = sum(1 for v in values.values() if v["stage"] == stage)
        if count:
            print("  stage %s: %d" % (stage, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
