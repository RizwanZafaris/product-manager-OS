#!/usr/bin/env python3
"""Review gate for regulated AI PRDs. Standard library only.

    python3 lint.py my-feature-prd.md
    python3 lint.py --template templates/regulated-ai-prd-template.md

Both modes: required sections, a parseable, non-future and non-stale as-of date,
review-gate checkboxes present, no banned metric strings, no em dashes, no
TBD/TODO/FIXME. PRD mode only (--template skips these, because an unfilled
template is supposed to be unfilled): every section 0 cell and "key: value" field
is answered, and every section 1 eval row carries a metric, dataset, numeric
threshold, below-threshold action, and owner, with the threshold either labeled
ILLUSTRATIVE or citing a dated agreement.

Limits, stated rather than hidden: a section 0 bullet with no colon is not read
as a field; gate boxes are checked for presence, never for being ticked, because
only a human can honestly tick one; the banned-metric list is a specific set of
literal strings, so a spelled-out variant walks straight through; and nothing
here tells a real citation from a confident sentence. Green means the document is
complete, not that it is true.

Two scans are deliberately wider than the rest. Dashes are checked on the raw
text, before code fences and HTML comments are blanked, because a template's
comments are read by the person filling it in. Banned metric strings are checked
line by line and then again over the text with its line breaks closed up, so a
string broken across a line break is still caught; the reported line is where the
match starts.

An as-of date older than STALE_AFTER_DAYS fails the gate, which is what makes the
repository's re-verification promise something CI enforces rather than something
a README asserts. A fork that wants the old advisory behavior runs the gate with
--no-stale-fail.

OS tree mode (python3 lint.py --os, run from the repo root) runs eleven checks
over the whole Product Manager OS tree rather than one PRD: character and
banned-metric gates over every .md and .json outside modules/regulated/, a
placeholder gate that accepts angle-bracket fill-in fields as the one sanctioned
placeholder form, a link gate that resolves every relative link and rejects
absolute local paths, a header gate for the three-line Stage/Knowledge/Skill
block on every template, a frontmatter gate for SKILL.md files, a sha256
integrity gate over the two byte-exact regulated files, a path gate for repo
paths named in system/ prompts, a secret gate, a graph gate over the six-key
declaration every file in the six declaring layers carries, and a wikilink gate
that resolves every [[target]] to a file or a declared alias.
modules/regulated/ is governed by its own verbatim lint.py and is exempt from
tree mode except for the integrity gate, which is the point.
docs/ARCHITECTURE.md and this file name the detector's own rule strings, so the
placeholder, secret, and wikilink gates skip them: a detector's rules have to be
legible, and the wikilink spec has to be able to write [[target]] in prose.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import posixpath
import re
import sys
from pathlib import Path

STALE_AFTER_DAYS = 180

# Deliberately blunt: these strings must not appear in this repository in any
# context, so the check does not try to be clever about surrounding words.
BANNED_METRICS = [
    (r"\$\s?14\s?m\b", "$14M"),
    (r"\b14(\.0)?\s?(%|percent)", "14%"),
    (r"\b22(\.0)?\s?(%|percent)", "22%"),
    (r"\b97(\.0)?\s?(%|percent)", "97%"),
    (r"\b99\.95", "99.95"),
    (r"\b120\s?k\b", "120K"),
    (r"\b120,000\b", "120,000"),
]

# Escapes, so the file that bans these characters does not contain one. The
# metric patterns above stay readable: a detector's rules have to be legible to
# whoever reviews the detector.
DASHES = {"\u2014": "em dash", "\u2013": "en dash",
          "\u2015": "horizontal bar", "\u2212": "minus sign"}

# (heading pattern, a word the heading must contain, human name)
REQUIRED_SECTIONS = [
    (r"^##\s*0\.", "overlay", "## 0. Regulated overlay"),
    (r"^###\s*0\.1\b", None, "### 0.1 Regulatory precondition register"),
    (r"^###\s*0\.2\b", None, "### 0.2 Scheme-rule constraints"),
    (r"^###\s*0\.3\b", None, "### 0.3 Data residency and model-vendor terms"),
    (r"^###\s*0\.4\b", None, "### 0.4 Financial-crime touchpoints"),
    (r"^###\s*0\.5\b", None, "### 0.5 Customer-communication conduct"),
    (r"^###\s*0\.6\b", None, "### 0.6 The metric that survives an audit"),
    (r"^##\s*1\.", "acceptance", "## 1. Acceptance criteria"),
    (r"^##\s*2\.", "edge", "## 2. Edge cases"),
    (r"^###\s*MUST REFUSE", None, "### MUST REFUSE"),
    (r"^###\s*MUST ESCALATE", None, "### MUST ESCALATE"),
    (r"^###\s*MUST NEVER INVENT", None, "### MUST NEVER INVENT"),
    (r"^##\s*3\.", "determin", "## 3. Non-determinism clause"),
    (r"^##\s*4\.", "guardrail", "## 4. Guardrails"),
    (r"^##\s*5\.", "operations", "## 5. Operations page"),
    (r"^##\s*6\.", "review gate", "## 6. Review gate"),
    (r"^##\s*7\.", "gaps", "## 7. GAPS"),
]

EVAL_COLUMNS = {"metric": ("metric",), "dataset": ("eval set", "dataset"),
                "threshold": ("threshold",), "below-threshold action": ("below",),
                "owner": ("owner",)}

# A threshold nobody has agreed to is a placeholder with a number attached, and an
# unlabeled number gets quoted back at you as a benchmark. One of these two has to
# be true of every shipped threshold: it says ILLUSTRATIVE, or it names the
# agreement and the date that agreement was reached.
ILLUSTRATIVE_RE = re.compile(r"illustrative", re.I)
AGREED_RE = re.compile(r"\b(?:per|agreed)\b[^|]*?\bdated\s+\d{4}-\d{2}-\d{2}", re.I)

AS_OF_RE = re.compile(r"as of[:\s]*\**\s*(\d{4}-\d{2}-\d{2})", re.I)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]")
FIELD_RE = re.compile(r"^\s*[-*]\s+(.+?):\s*(.*)$")
BARE_NA_RE = re.compile(r"^(n/?a|not applicable|none|nil|unknown)\.?$", re.I)
SEPARATOR_RE = re.compile(r"^\|?[\s:|-]+\|?$")


def mask(text):
    """Blank HTML comments and fenced code, preserving line numbers."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))  # noqa: E731
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"^```.*?^```", blank, text, flags=re.S | re.M)
    return text.split("\n")


def collapse(lines):
    """Return the text with every line break closed up, plus a line per char.

    A banned string split over a line break ("99." then "95" on the next line)
    reads as two innocent fragments line by line and as the banned string here.
    Whitespace inside a line is left alone, so the patterns keep their word
    boundaries and the only new adjacency is the one at each line join.
    """
    chars, origin = [], []
    for line_no, line in enumerate(lines, 1):
        for char in line.strip():
            chars.append(char)
            origin.append(line_no)
    return "".join(chars), origin


def cells(line):
    body = line.strip().strip("|")
    return [c.strip() for c in body.split("|")]


def tables(lines, start, end):
    """Yield (header_cells, [(line_no, row_cells), ...]) for tables in a span."""
    i = start
    while i < end:
        nxt = lines[i + 1].strip() if i + 1 < end else ""
        if lines[i].strip().startswith("|") and SEPARATOR_RE.match(nxt) and "-" in nxt:
            header, rows, j = cells(lines[i]), [], i + 2
            while j < end and lines[j].strip().startswith("|"):
                rows.append((j + 1, cells(lines[j])))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def unanswered(value):
    """Return why a cell or field value is not a real answer, or None."""
    text = MD_LINK_RE.sub(r"\1", value).strip()
    if not text or text in {"-", "--", "?", "??", "???"}:
        return "is blank"
    if BARE_NA_RE.match(text):
        return 'says "%s" with no reason. Write "N/A because <reason>"' % text
    if re.search(r"\[[^\]]*\]", CHECKBOX_RE.sub("", text)):
        return "still holds a [placeholder]"
    return None


def headings(lines):
    """Return [(index, hashes, text)] and {heading text: (start, end)}."""
    heads = [(i, m.group(1), lines[i]) for i, m in
             ((i, re.match(r"^(#{2,3})\s+\S", ln)) for i, ln in enumerate(lines)) if m]
    spans = {}
    for pos, (i, hashes, text) in enumerate(heads):
        end = next((j for j, h2, _ in heads[pos + 1:] if len(h2) <= len(hashes)),
                   len(lines))
        spans.setdefault(text.strip(), (i, end))
    return heads, spans


def span_for(spans, pattern):
    return next((s for h, s in spans.items() if re.match(pattern, h)), None)


def check(path, template_mode=False, stale_fatal=True):
    """Return (sorted failures, sorted non-fatal notices) as (line, code, msg)."""
    raw = Path(path).read_text(encoding="utf-8")
    lines = mask(raw)
    text = "\n".join(lines)
    problems, notices = [], []
    fail = lambda n, c, m: problems.append((n, c, m))  # noqa: E731

    # Before mask(), on purpose: a dash inside a code fence or an HTML comment is
    # still a dash the reader sees, and the template's comments are instructions.
    for i, line in enumerate(raw.split("\n"), 1):
        for char, name in DASHES.items():
            if char in line:
                fail(i, "DASH", "contains an %s. Use a comma or a colon." % name)

    # Line by line, then again over the closed-up text, so that a banned string
    # broken across a line break is caught too. Reported once per line and label.
    seen = set()

    def banned(line_no, label):
        if (line_no, label) not in seen:
            seen.add((line_no, label))
            fail(line_no, "BANNED", "contains the banned metric string %s." % label)

    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"\b(TBD|TODO|FIXME|XXX)\b", line, re.I):
            fail(i, "TBD", '"%s" is a deferred decision, not an answer.' % m.group(1))
        for pattern, label in BANNED_METRICS:
            if re.search(pattern, line, re.I):
                banned(i, label)

    collapsed, origin = collapse(lines)
    for pattern, label in BANNED_METRICS:
        for m in re.finditer(pattern, collapsed, re.I):
            banned(origin[m.start()], label)

    heads, spans = headings(lines)
    titles = [t for _, _, t in heads]
    for pattern, keyword, label in REQUIRED_SECTIONS:
        hit = next((t for t in titles if re.match(pattern, t.strip(), re.I)), None)
        if hit is None:
            fail(1, "SECTION", "required section is missing: %s" % label)
        elif keyword and keyword not in hit.lower():
            fail(titles.index(hit) + 1, "SECTION",
                 'heading "%s" does not mention "%s".' % (hit.strip(), keyword))

    m = AS_OF_RE.search(text)
    if not m:
        fail(1, "ASOF", 'no as-of date found. Add "Regulatory references verified '
                        'as of: YYYY-MM-DD" to the header.')
    else:
        line_no, today = text[:m.start()].count("\n") + 1, _dt.date.today()
        try:
            when = _dt.date.fromisoformat(m.group(1))
        except ValueError:
            fail(line_no, "ASOF", "as-of date %s does not parse." % m.group(1))
        else:
            if when > today:
                fail(line_no, "ASOF", "as-of date %s is in the future." % when)
            elif (today - when).days > STALE_AFTER_DAYS:
                stale = (line_no, "STALE", "as-of date %s is over %d days old. "
                         "Re-verify every citation against primary text and move "
                         "the date, or run with --no-stale-fail."
                         % (when, STALE_AFTER_DAYS))
                (problems if stale_fatal else notices).append(stale)

    gate = span_for(spans, r"^##\s*6\.")
    if gate and not any(CHECKBOX_RE.match(lines[i]) for i in range(*gate)):
        fail(gate[0] + 1, "GATE", "review gate has no checkboxes.")

    if template_mode:
        return sorted(problems), sorted(notices)

    overlay = span_for(spans, r"^##\s*0\.")
    if overlay:
        rows_seen = False
        for header, rows in tables(lines, *overlay):
            for line_no, row in rows:
                rows_seen = True
                for idx, value in enumerate(row):
                    why = unanswered(value)
                    if why:
                        name = header[idx] if idx < len(header) else "column %d" % (idx + 1)
                        fail(line_no, "OVERLAY",
                             'section 0 field "%s" %s.' % (name.strip()[:58], why))
        for i in range(*overlay):
            fm = FIELD_RE.match(lines[i])
            if fm and not CHECKBOX_RE.match(lines[i]):
                why = unanswered(fm.group(2))
                if why:
                    fail(i + 1, "OVERLAY",
                         'section 0 field "%s" %s.' % (fm.group(1).strip()[:58], why))
        if not rows_seen:
            fail(overlay[0] + 1, "OVERLAY", "section 0 has no completed table rows.")

    accept = span_for(spans, r"^##\s*1\.")
    if accept:
        found = False
        for header, rows in tables(lines, *accept):
            lower = [h.lower() for h in header]
            index = {key: next((i for i, h in enumerate(lower)
                                if any(k in h for k in keys)), None)
                     for key, keys in EVAL_COLUMNS.items()}
            if any(v is None for v in index.values()):
                continue
            found = True
            for line_no, row in rows:
                for key, idx in index.items():
                    value = row[idx] if idx < len(row) else ""
                    why = unanswered(value)
                    if why:
                        fail(line_no, "EVAL", "eval row %s has no %s (it %s)."
                             % (row[0] or "?", key, why))
                    elif key == "threshold":
                        if not re.search(r"\d", value):
                            fail(line_no, "EVAL", "eval row %s threshold %r has no "
                                 "number in it." % (row[0] or "?", value))
                        elif not (ILLUSTRATIVE_RE.search(value)
                                  or AGREED_RE.search(value)):
                            fail(line_no, "LABEL", "eval row %s threshold %r is "
                                 "neither labeled ILLUSTRATIVE nor traced to an "
                                 'agreement. Write the number as "<n> '
                                 '(ILLUSTRATIVE)" until it is agreed, or cite it '
                                 'as "per <agreement> dated YYYY-MM-DD".'
                                 % (row[0] or "?", value))
        if not found:
            fail(accept[0] + 1, "EVAL", "section 1 has no eval table with metric, "
                 "eval set or dataset, threshold, below-threshold action, and "
                 "owner columns.")

    return sorted(problems), sorted(notices)


# ---------------------------------------------------------------------------
# OS tree mode. Everything below is additive; the PRD gate above is unchanged.
# ---------------------------------------------------------------------------

# sha256 of the two byte-exact regulated files, recorded at copy time from
# the source repo, github.com/RizwanZafaris/regulated-ai-prd. Any drift fails
# the build; fixes go to the source repo first and are re-copied here, never
# edited here.
PINNED_HASHES = {
    "modules/regulated/templates/regulated-ai-prd-template.md":
        "5bec8839d75c71800263bf8d7e3e3b9cf0014f9521beb1b2a4a8ce9da616ad5d",
    "modules/regulated/examples/dispute-summary/PRD.md":
        "7427e8995e2941e3878f20a68196ab26d29d9c19322749cf4a1d2b2771c3aa07",
}

# Anchored, not bare prefixes: a bare "sk-" would false-positive on every
# mention of risk-register.md across the tree.
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"\bsk-[A-Za-z0-9]{20,}", "API key (sk-)"),
    (r"\bghp_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"BEGIN [A-Z ]*PRIVATE KEY", "private key block"),
]

# Files that legitimately spell out the detector's own rule strings.
RULE_BEARING = {"docs/ARCHITECTURE.md", "lint.py", "test_lint.py"}

PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b", re.I)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
REPO_PATH_RE = re.compile(
    r"\b((?:os|templates|knowledge|skills|agents|system|routing|modules|"
    r"examples|docs)/[A-Za-z0-9._/\-]*[A-Za-z0-9])")
HEADER_KEYS = ("Stage:", "Knowledge:", "Skill:")
HEADER_WINDOW = 8

# The six layers that declare themselves to the graph, and the key set every
# file in them carries. Written by tools/frontmatter_init.py, read by
# tools/graph.py, and checked here.
GRAPH_LAYERS = ("agents", "frameworks", "knowledge", "os", "skills",
                "templates")
GRAPH_KEYS = ("layer", "stage", "gate", "feeds", "method", "aliases")

# A SKILL.md declares in a sidecar, never in its own frontmatter. The Agent
# Skills format validates SKILL.md frontmatter against a closed attribute list
# (name, description, license, metadata, compatibility), and a runtime that
# enforces it rejects the file outright on an unknown key. Check 6 keeps the
# two-key contract on the SKILL.md; check 10 reads the sidecar beside it.
SKILL_SIDECAR = "SKILL.graph.yml"

# name and description predate the graph on every agent file and are the Agent
# Skills contract everywhere else. Any other key outside GRAPH_KEYS fails.
GRAPH_COMPANIONS = ("name", "description")

# The six stages of the loop, plus the three cross-cutting tracks the loop and
# the graph already name. A file that serves the PLANNING track must be able to
# say so: forcing it to claim one of the six would be a wrong answer, and a
# wrong stage is worse than a missing one.
STAGE_VOCABULARY = ("DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER",
                    "OPERATE", "PLANNING", "AI OVERLAY", "ALL STAGES")

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")


def fields(block):
    """Top-level "key: value" pairs of a YAML block, values left as text.

    Not a YAML implementation: indented lines and block sequences are skipped,
    because the declaration this gate reads uses neither.
    """
    out = {}
    for line in block.split("\n"):
        if not line.strip() or line.startswith((" ", "\t", "-", "#")):
            continue
        match = FM_FIELD_RE.match(line)
        if match:
            out[match.group(1).lower()] = match.group(2).strip()
    return out


def values_of(text):
    """A declaration value as a list: an inline list, or a lone scalar."""
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    parts = [p.strip().strip("'\"") for p in text.split(",")]
    return [p for p in parts if p]


def declaration(path, raw):
    """One file's graph declaration as (fields or None, where it should be)."""
    if path.name == "SKILL.md":
        sidecar = path.parent / SKILL_SIDECAR
        if not sidecar.is_file():
            return None, SKILL_SIDECAR
        try:
            return fields(sidecar.read_text(encoding="utf-8")), SKILL_SIDECAR
        except (UnicodeDecodeError, OSError):
            return None, SKILL_SIDECAR
    match = FRONTMATTER_RE.match(raw)
    return (fields(match.group(1)) if match else None), "frontmatter"


def points_at(value, rp, tree):
    """A declared path as a file in the tree, or None."""
    target = value.split("#")[0].strip().strip("`")
    if not target or target.startswith(("http://", "https://", "mailto:", "/")):
        return None
    if target in tree:
        return target
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(rp), target))
    return joined if joined in tree else None


def wikilink_lands(target, tree, aliases):
    """True when [[target]] names a file in the tree or a declared alias."""
    if target in tree or target + ".md" in tree:
        return True
    if target.lower() in aliases:
        return True
    tail = target.split("/")[-1]
    return any(p.split("/")[-1] in (tail, tail + ".md") for p in tree)


def tracked_files(root):
    """Every file in the tree except VCS internals, caches, and user workspaces.

    products/ and learn/products/ hold a user's own filled drafts (gitignored);
    the gate judges the shipped system, never someone's work in progress. The
    two workspace README.md files stay in scope because they ship with the repo.
    """
    skip = {".git", "__pycache__", ".venv", "node_modules"}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (skip & set(path.parts)) \
                and not path.name.startswith("._"):
            rel = path.relative_to(root).parts
            in_workspace = (rel[:1] == ("products",) and rel[1:] != ("README.md",)) \
                or (rel[:2] == ("learn", "products") and rel[2:] != ("README.md",))
            if in_workspace:
                continue
            yield path


def in_angle_field(line, start):
    """True when position start sits inside an <angle-bracket> fill-in field."""
    left = line.rfind("<", 0, start)
    return left != -1 and line.find(">", left) > start


def os_check(root, pins=None):
    """Whole-tree gate. Returns sorted (relpath, line, code, message) tuples."""
    root = Path(root)
    pins = PINNED_HASHES if pins is None else pins
    problems = []
    fail = lambda p, n, c, m: problems.append((str(p), n, c, m))  # noqa: E731

    all_files = list(tracked_files(root))
    rel = {p: p.relative_to(root).as_posix() for p in all_files}
    tree = set(rel.values())

    # Check 7, integrity gate: runs first and inside modules/regulated/,
    # which is otherwise exempt from tree mode.
    import hashlib
    for pinned, expected in sorted(pins.items()):
        target = root / pinned
        if not target.is_file():
            fail(pinned, 1, "INTEGRITY", "pinned byte-exact file is missing.")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            fail(pinned, 1, "INTEGRITY", "content drifted from the pinned "
                 "sha256. Fix the source repo and re-copy; never edit here.")

    # Checks 10 and 11 read declarations rather than one file's own text, so
    # the declarations are gathered before the per-file pass: a wikilink in one
    # file resolves against an alias declared in another, and an alias is
    # claimed by exactly one file, whichever sorts first.
    decls, aliases = {}, {}
    for path in all_files:
        rp = rel[path]
        if path.suffix != ".md" or rp.startswith("modules/") \
                or rp.split("/")[0] not in GRAPH_LAYERS:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        block, source = declaration(path, raw)
        decls[rp] = (block, source)
        for alias in values_of((block or {}).get("aliases", "")):
            aliases.setdefault(alias.lower(), rp)

    for path in all_files:
        rp = rel[path]
        if rp.startswith("modules/regulated/"):
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        raw_lines = raw.split("\n")
        lines = mask(raw) if path.suffix == ".md" else raw_lines
        is_doc = path.suffix in (".md", ".json")

        # Check 9, secret gate: every readable file.
        if rp not in RULE_BEARING:
            for i, line in enumerate(raw_lines, 1):
                for pattern, label in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        fail(rp, i, "SECRET",
                             "matches the %s pattern." % label)

        if not is_doc:
            continue

        # Check 1, character gate: raw text, same reasoning as the PRD gate.
        for i, line in enumerate(raw_lines, 1):
            for char, name in DASHES.items():
                if char in line:
                    fail(rp, i, "DASH",
                         "contains an %s. Use a comma or a colon." % name)

        # Check 2, metric gate: masked lines plus the closed-up text.
        seen = set()
        for i, line in enumerate(lines, 1):
            for pattern, label in BANNED_METRICS:
                if re.search(pattern, line, re.I) and (i, label) not in seen:
                    seen.add((i, label))
                    fail(rp, i, "BANNED",
                         "contains the banned metric string %s." % label)
        collapsed, origin = collapse(lines)
        for pattern, label in BANNED_METRICS:
            for m in re.finditer(pattern, collapsed, re.I):
                key = (origin[m.start()], label)
                if key not in seen:
                    seen.add(key)
                    fail(rp, key[0], "BANNED",
                         "contains the banned metric string %s." % label)

        # Check 3, placeholder gate: angle-bracket fields are sanctioned.
        if rp not in RULE_BEARING:
            for i, line in enumerate(lines, 1):
                for m in PLACEHOLDER_RE.finditer(line):
                    if not in_angle_field(line, m.start()):
                        fail(rp, i, "TBD", '"%s" is a deferred decision, '
                             "not an answer." % m.group(1))

        # Check 4, link gate: markdown files only.
        if path.suffix == ".md":
            for i, line in enumerate(lines, 1):
                for m in LINK_RE.finditer(line):
                    target = m.group(1).split("#")[0]
                    if not target or target.startswith(
                            ("http://", "https://", "mailto:")):
                        continue
                    if target.startswith("/"):
                        fail(rp, i, "LINK",
                             "absolute local path %s in a link." % target)
                    elif not (path.parent / target).resolve().exists():
                        fail(rp, i, "LINK",
                             "relative link %s does not resolve." % target)

        # Check 5, header gate: three-line Stage/Knowledge/Skill block. The
        # window starts under any frontmatter, because the graph declaration
        # sits above the header and would otherwise push it out of range. The
        # header is still the first thing a reader of the document sees.
        if rp.startswith("templates/"):
            match = FRONTMATTER_RE.match(raw)
            start = raw[:match.end()].count("\n") if match else 0
            top = "\n".join(lines[start:start + HEADER_WINDOW])
            for key in HEADER_KEYS:
                if key not in top:
                    fail(rp, 1, "HEADER",
                         "template header is missing the %s line." % key)

        # Check 6, frontmatter gate: exactly name and description.
        if path.name == "SKILL.md":
            fm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
            keys = [ln.split(":")[0].strip() for ln in
                    (fm.group(1).split("\n") if fm else [])
                    if ln.strip() and not ln.startswith((" ", "\t"))]
            if keys != ["name", "description"]:
                fail(rp, 1, "FRONTMATTER", "SKILL.md frontmatter must be "
                     "exactly name and description; found %s." % (keys or "none"))
            elif fm and "use when" not in fm.group(1).lower():
                fail(rp, 1, "FRONTMATTER",
                     'description has no explicit "Use when" clause.')

        # Check 8, path gate: repo paths named in system/ prompts must exist.
        if rp.startswith("system/"):
            for i, line in enumerate(lines, 1):
                for m in REPO_PATH_RE.finditer(line):
                    named = m.group(1)
                    if named not in tree and not any(
                            t.startswith(named + "/") for t in tree):
                        fail(rp, i, "PATH",
                             "names repo path %s, which does not exist." % named)

        # Check 10, graph gate: the declaration every file in the six layers
        # carries. A missing key is a hole in the graph; a stage outside the
        # vocabulary or a feeds path that resolves to nothing is worse, because
        # it renders as a confident arrow pointing at the wrong place.
        if rp in decls:
            block, source = decls[rp]
            if block is None:
                fail(rp, 1, "GRAPH", "has no graph declaration. Put the keys "
                     "%s in its %s, or run tools/frontmatter_init.py."
                     % (", ".join(GRAPH_KEYS), source))
            else:
                for key in GRAPH_KEYS:
                    if key not in block:
                        fail(rp, 1, "GRAPH",
                             "%s is missing the %s key." % (source, key))
                for key in sorted(k for k in block
                                  if k not in GRAPH_KEYS + GRAPH_COMPANIONS):
                    fail(rp, 1, "GRAPH", '%s carries "%s", which is not one of '
                         "%s." % (source, key,
                                  ", ".join(GRAPH_KEYS + GRAPH_COMPANIONS)))
                stage = block.get("stage", "").strip().strip("'\"")
                if "stage" in block and stage not in STAGE_VOCABULARY:
                    fail(rp, 1, "GRAPH", 'stage "%s" is not one of %s.'
                         % (stage, ", ".join(STAGE_VOCABULARY)))
                gate = block.get("gate", "").strip().strip("'\"")
                if "gate" in block and not (gate.isdigit()
                                            and 1 <= int(gate) <= 6):
                    fail(rp, 1, "GRAPH", 'gate "%s" is not an integer 1 to 6.'
                         % gate)
                for value in values_of(block.get("feeds", "")):
                    if points_at(value, rp, tree) is None:
                        fail(rp, 1, "GRAPH", "feeds names %s, which is not a "
                             "file in the tree." % value)
                for value in values_of(block.get("method", "")):
                    if points_at(value, rp, tree) is None:
                        fail(rp, 1, "GRAPH", "method names %s, which is not a "
                             "file in the tree." % value)

        # Check 11, wikilink gate: additive Obsidian links, every layer. A
        # relative markdown link is what GitHub renders and check 4 owns those;
        # a wikilink is what the vault graph reads, and an unresolved one is an
        # edge the graph silently drops.
        if path.suffix == ".md" and rp not in RULE_BEARING:
            for i, line in enumerate(lines, 1):
                for m in WIKILINK_RE.finditer(line):
                    target = m.group(1).split("|")[0].split("#")[0].strip()
                    if target and not wikilink_lands(target, tree, aliases):
                        fail(rp, i, "WIKILINK", "wikilink [[%s]] names neither "
                             "a file in the tree nor a declared alias." % target)

    return sorted(problems)


def run_os_mode(root):
    problems = os_check(root)
    for rp, line_no, code, message in problems:
        print("%s:%d: %s %s" % (rp, line_no, code, message))
    if problems:
        print("\n%d problem(s). The gate failed, which is the point of having "
              "one." % len(problems), file=sys.stderr)
        return 1
    print("%s: ok (OS tree mode, %d checks)" % (root, 11))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--template", action="store_true",
                        help="structure-only mode for an unfilled template")
    parser.add_argument("--os", dest="os_mode", action="store_true",
                        help="whole-tree OS gate, run from the repo root")
    parser.add_argument("--no-stale-fail", action="store_true",
                        help="report a stale as-of date as a notice rather than a "
                             "failure. For forks that accept the staleness")
    args = parser.parse_args(argv)

    if args.os_mode:
        return run_os_mode(args.files[0] if args.files else Path("."))
    if not args.files:
        parser.error("give at least one file, or use --os")

    total = 0
    for path in args.files:
        if not path.is_file():
            print("%s: cannot read file" % path, file=sys.stderr)
            total += 1
            continue
        problems, notices = check(path, template_mode=args.template,
                                  stale_fatal=not args.no_stale_fail)
        for line_no, code, message in problems:
            print("%s:%d: %s %s" % (path, line_no, code, message))
        for line_no, code, message in notices:
            print("%s:%d: %s %s (not a failure)" % (path, line_no, code, message))
        if not problems:
            print("%s: ok (%s mode)" % (path, "template" if args.template else "PRD"))
        total += len(problems)
    if total:
        print("\n%d problem(s). The gate failed, which is the point of having one."
              % total, file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
