#!/usr/bin/env python3
"""Review gate for regulated AI PRDs. Standard library only.

    python3 lint.py my-feature-prd.md
    python3 lint.py --template templates/regulated-ai-prd-template.md

Both modes: required sections, a parseable, non-future and non-stale as-of date,
review-gate checkboxes present, no banned metric strings, no em dashes, no
TBD/TODO/FIXME. PRD mode only (--template skips these, because an unfilled
template is supposed to be unfilled): every section 0 cell and "key: value" field
is answered, in the sense that it holds neither a [placeholder] nor an unfilled
<angle-bracket> field; sections 0.1 and 0.2 each carry a table with their
required columns and at least one entry, so a gutted document cannot satisfy
section 0 with any table that happens to have a row; and the section 1 eval
table carries at least one row, each with a metric, dataset, numeric threshold,
below-threshold action, and owner, with the threshold either labeled
ILLUSTRATIVE or citing a dated agreement.

Limits, stated rather than hidden: a section 0 bullet with no colon is not read
as a field; gate boxes are checked for presence, never for being ticked, because
only a human can honestly tick one; the banned-metric list is a specific set of
literal strings, so a spelled-out variant walks straight through; a required
column is matched by a keyword in its header, so a renamed column with the same
word in it passes; and nothing here tells a real citation from a confident
sentence. Green means the document is complete, not that it is true.

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
placeholder form, a link gate that resolves every relative link against the
tracked tree and rejects absolute local paths and any link that climbs out of
the repository, a header gate for the three-line Stage/Knowledge/Skill block on
every template, a frontmatter gate for SKILL.md files, a sha256 integrity gate
over every regulated file this repository calls verbatim, a path gate for repo
paths named in system/ prompts, a secret gate, a graph gate over the six-key
declaration every file in the six declaring layers carries, and a wikilink gate
that resolves every [[target]] to a file or a declared alias.
modules/regulated/ is governed by its own verbatim lint.py and is exempt from
tree mode except for the integrity gate, which is the point.

Four of those checks are wider than they read. The secret gate runs on every
readable file with no exemption, line by line and again over the closed-up text,
and a file that is not valid UTF-8 fails rather than being skipped, because a
file no check could read is a file no check has cleared. The path gate reads the
raw lines of system/ prompts, fences included, since the prompt body a user
pastes lives inside a fence; a name in a manifest line is resolved against the
directory that line names as well as against the repository root. The graph gate
checks the declaration against the truth it claims: layer is the directory the
file lives in, gate is a gate os/STAGE-GATES.md defines, and stage and gate
agree with the file's own Stage header and with the gate that document says
closes that stage. The wikilink gate resolves a qualified target exactly and
accepts a bare name only while it is unique in the tree.

docs/ARCHITECTURE.md and this file name the detector's own rule strings, so the
placeholder and wikilink gates skip them: a detector's rules have to be legible,
and the wikilink spec has to be able to write [[target]] in prose. The secret
gate exempts nothing. A real key inside a document about the secret gate is
still a real key, so the patterns here are written not to match their own source
text instead.

Workspace mode:

    python3 lint.py --workspace products/my-product

products/ and learn/products/ are excluded from Git and from tree mode, and both
exclusions stay: a half-filled draft must never fail the repository's build. The
cost of that, until this mode existed, was that a user's work was checked by
nothing at all. This is the opt-in. It runs the five content checks over one
workspace directory and exits non-zero on failure: links, secrets, placeholders,
dashes, and banned metric strings. Every file under the directory is read, and
the workspace is not required to be under products/.

What it deliberately does not run: the template header block, SKILL.md
frontmatter, graph declarations, wikilink resolution, the system/ path gate, the
integrity pins, manifest agreement, and the whole PRD gate (required sections,
as-of date, eval table). A filled artifact is not a template and not a layer
file, so those checks would report the document for being what it is supposed to
be. Links may point back into the repository: the containment boundary is the
repository root, not the workspace, so ../../os/STAGE-GATES.md resolves and
../../../etc/hosts still fails.

JSON mode:

    python3 lint.py --json-syntax

Parses every tracked .json file and reports the file, line, and column of each
syntax error. CI ran no JSON parser before this, so a corrupt
routing/omniroute.config.json or harness/MANIFEST.json passed the build: every
other check reads those files as text, and text is what a broken JSON file still
is. Tree mode is untouched and still runs eleven checks; this is a separate step
so the eleven keep their meaning.
"""
from __future__ import annotations

import argparse
import base64
import collections
import datetime as _dt
import hashlib
import json
import math
import posixpath
import re
import sys
import urllib.parse
from pathlib import Path

STALE_AFTER_DAYS = 180

# The numbers the worked example uses. A filled document that still carries
# them is carrying the example's answers rather than its own, which is the
# failure this list catches.
#
# Deliberately blunt inside this repository, where none of them can be true of
# anything: the check does not try to be clever about surrounding words.
#
# Not blunt in a product workspace, where they can be. A real product can have
# a 14% baseline, and rejecting a sourced one taught the operator that the way
# to pass the gate is to round the number, which is worse than the thing being
# prevented. In workspace mode the same literal is judged on whether it carries
# provenance: a number with a source beside it is evidence, and a bare one is
# still the example's answer wearing this product's clothes. See SOURCED_RE.
BANNED_METRICS = [
    (r"\$\s?14\s?m\b", "$14M"),
    (r"\b14(\.0)?\s?(%|percent)", "14%"),
    (r"\b22(\.0)?\s?(%|percent)", "22%"),
    (r"\b97(\.0)?\s?(%|percent)", "97%"),
    (r"\b99\.95", "99.95"),
    (r"\b120\s?k\b", "120K"),
    (r"\b120,000\b", "120,000"),
]

# What makes a number evidence rather than a leftover. Any of: a URL, an
# explicit evidence-ledger reference like [E3], a bracketed source or citation
# note, or the word "source" with something after it. The test is deliberately
# generous, because the check it gates is a heuristic and the cost of a false
# accusation here is an operator who edits a true number to get past a gate.
SOURCED_RE = re.compile(
    r"https?://"
    r"|\[E\d+\]"
    r"|\bsources?\s*[:=]"
    r"|\bcitation\s*[:=]"
    r"|\bper\s+[A-Z]"
    r"|\bmeasured\s+(?:by|at|on|in|from|against)\b"
    r"|\bbaseline\s+from\b",
    re.I)


def sourced_near(lines, index):
    """Whether the number on this line carries provenance.

    The line itself, and the line under it, because a markdown table puts the
    figure in one cell and its source in another on the same row, while a
    prose paragraph often puts the citation on the following line.
    """
    window = lines[max(0, index - 1):index + 2]
    return any(SOURCED_RE.search(line) for line in window)


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
TICKED_RE = re.compile(r"^\s*[-*]\s*\[[xX]\]")

# The status line the regulated template puts at the top. Matched only when it
# names Approved on its own, so the template's own "Draft / In review /
# Approved" menu of choices is not read as a claim of approval.
APPROVED_RE = re.compile(r"^\*\*Status:\*\*\s*Approved\b", re.M)
FIELD_RE = re.compile(r"^\s*[-*]\s+(.+?):\s*(.*)$")
BARE_NA_RE = re.compile(r"^(n/?a|not applicable|none|nil|unknown)\.?$", re.I)
SEPARATOR_RE = re.compile(r"^\|?[\s:|-]+\|?$")

# An unfilled fill-in field, the template's own placeholder form. Legal in a
# template, never in a document that claims to be finished, which is why this
# only bites in full-document mode. The leading character class keeps "<= 5"
# and a closing HTML tag out of it.
ANGLE_FIELD_RE = re.compile(r"<[A-Za-z0-9][^<>]*>")

# The two section 0 registers carry a fixed column set, so a document cannot
# satisfy section 0 with any table that happens to have a row in it. Each entry
# is (heading pattern, name, column groups); a group is satisfied when some
# header cell contains one of its keywords.
SECTION0_TABLES = (
    (r"^###\s*0\.1\b", "0.1",
     (("market",), ("license", "approval", "notification"), ("regulator",),
      ("confirmed",), ("owner",))),
    (r"^###\s*0\.2\b", "0.2",
     (("rule area", "rule"), ("reference",), ("version",), ("watch",))),
)


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
    stripped = CHECKBOX_RE.sub("", text)
    if re.search(r"\[[^\]]*\]", stripped):
        return "still holds a [placeholder]"
    if ANGLE_FIELD_RE.search(stripped):
        return "still holds an unfilled <angle-bracket> field"
    return None


def matches_schema(header, schema):
    """True when this table header carries every required column group."""
    lower = [h.lower() for h in header]
    return all(any(any(word in cell for word in group) for cell in lower)
               for group in schema)


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

    # The gate used to be satisfied by the presence of checkbox text, never by
    # its state, so a document could carry nine unticked boxes and pass. An
    # unticked box is not itself a defect: the worked example ships with one
    # unticked and a paragraph saying why, which is the discipline working.
    #
    # What is a defect is a document that calls itself Approved while the
    # evidence for that approval is still unticked. That is the one case where
    # the tally can be judged rather than merely reported, so it is the one
    # case that fails.
    if gate:
        boxes = [i for i in range(*gate) if CHECKBOX_RE.match(lines[i])]
        unticked = [i for i in boxes if not TICKED_RE.match(lines[i])]
        approved = APPROVED_RE.search("\n".join(lines))
        if unticked and approved:
            for i in unticked:
                fail(i + 1, "GATE",
                     "this document's status is Approved and this review-gate "
                     "box is not ticked: %s. A gate nobody can fail is a "
                     "ceremony. Either tick it with the evidence behind it, or "
                     "set the status back to In review."
                     % lines[i].strip()[:120])
        elif unticked:
            notices.append(
                (gate[0] + 1, "GATE",
                 "review gate: %d of %d box(es) still unticked. Not a failure "
                 "while the status is not Approved. This gate is discipline "
                 "rather than control: nothing here can stop a person ticking "
                 "a box the evidence does not support."
                 % (len(unticked), len(boxes))))

    overlay = span_for(spans, r"^##\s*0\.")
    if overlay:
        for header, rows in tables(lines, *overlay):
            for line_no, row in rows:
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
        # The register tables, by schema rather than by shape: a table with the
        # right columns and no rows is an empty register, and a table with rows
        # and the wrong columns is a different document.
        for pattern, name, schema in SECTION0_TABLES:
            sub = span_for(spans, pattern)
            if sub is None:
                continue  # the required-section check above already said so
            matched = [rows for header, rows in tables(lines, *sub)
                       if matches_schema(header, schema)]
            columns = ", ".join(group[0] for group in schema)
            if not matched:
                fail(sub[0] + 1, "OVERLAY", "section %s has no table carrying "
                     "the required columns (%s)." % (name, columns))
            elif not any(matched):
                fail(sub[0] + 1, "OVERLAY", "section %s register has a header "
                     "row and no entries." % name)

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
            if not rows:
                fail(accept[0] + 1, "EVAL", "section 1 eval table has the right "
                     "columns and no rows. One eval row per requirement, or the "
                     "table is a promise.")
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

# sha256 of every regulated file this repository calls a verbatim copy, taken
# from the current bytes of the copy in this tree. The module README names five:
# two byte-exact documents carrying verified citations, and the three runnable
# files (SKILL.md, lint.py, test_lint.py) that let the module's own gate run
# from its directory. Any drift fails the build; fixes go to the source repo,
# github.com/RizwanZafaris/regulated-ai-prd, and are re-copied here, never
# edited here. modules/regulated/README.md is deliberately absent: it describes
# this repository's policy and is local, not a copy.
PINNED_HASHES = {
    "modules/regulated/templates/regulated-ai-prd-template.md":
        "5bec8839d75c71800263bf8d7e3e3b9cf0014f9521beb1b2a4a8ce9da616ad5d",
    "modules/regulated/examples/dispute-summary/PRD.md":
        "7427e8995e2941e3878f20a68196ab26d29d9c19322749cf4a1d2b2771c3aa07",
    "modules/regulated/SKILL.md":
        "5152a98223260a98002752d0f48b3ede72931d574d0df683247d5ac6854636ad",
    "modules/regulated/lint.py":
        "17bb3e21c83df56651c7026633a96d3968c3a9df9c78a54c4fdcd4d591c2f854",
    "modules/regulated/test_lint.py":
        "e7efed32a43e69e86eebd8bd76636d648a034c591231607c05c1f93d60be405e",
}

# Anchored, not bare prefixes: a bare "sk-" would false-positive on every
# mention of risk-register.md across the tree. The modern issuers put their own
# prefix in the token, which is what makes anchoring affordable. None of these
# patterns matches its own source text, which is why this file needs no
# exemption from the check it defines.
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"\bASIA[0-9A-Z]{16}", "AWS temporary access key id"),
    (r"\bsk-proj-[A-Za-z0-9_\-]{16,}", "OpenAI project key"),
    (r"\bsk-svcacct-[A-Za-z0-9_\-]{16,}", "OpenAI service-account key"),
    (r"\bsk-ant-[A-Za-z0-9_\-]{16,}", "Anthropic API key"),
    (r"\bsk-[A-Za-z0-9]{20,}", "API key (sk-)"),
    (r"\bgithub_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained token"),
    (r"\bgh[pousr]_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"\bxox[abprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    (r"\bAIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}",
     "JSON web token"),
    (r"-{5}BEGIN [A-Z ]*PRIVATE KEY-{5}", "private key block"),
    (r"(?i)\baws[_\- ]?secret[_\- ]?access[_\- ]?key\b\W{0,4}[A-Za-z0-9/+]{40}",
     "AWS secret access key value"),
]

# The shape that catches the key no issuer prefixed: a credential-shaped name,
# an assignment, and a value with too much entropy to be a word. Length, three
# character classes, and the entropy floor together are what keep this off
# prose; a 24-character English phrase does not clear 3.6 bits per character.
SECRET_NAME_RE = re.compile(
    r"(?i)(?:^|[^A-Za-z0-9])[A-Za-z0-9]{0,20}[_\-]?"
    r"(?:api[_\-]?key|secret[_\-]?key|client[_\-]?secret|secret|token|"
    r"password|passwd|credential|access[_\-]?key|bearer)\b"
    r"\s*(?:[:=]|=>)\s*[\"']?([A-Za-z0-9+/=_\-]{24,})")
ENTROPY_FLOOR = 3.6
BASE64_RUN_RE = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")

# Files that legitimately spell out the detector's own rule strings. This is an
# exemption from the placeholder and wikilink gates only: those files name
# banned strings as detector patterns and have to write [[target]] in prose.
# The secret gate exempts nothing, because a real key in a document about the
# secret gate is still a real key.
RULE_BEARING = {"docs/ARCHITECTURE.md", "lint.py", "test_lint.py"}

PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b", re.I)

# An inline link destination in every spelling CommonMark allows: bare, wrapped
# in angle brackets, followed by a title, and percent-encoded. The old pattern
# read one of those and silently matched nothing for the rest, so a link with a
# space or a title in it was not a broken link the gate reported, it was a link
# the gate never saw. The empty destination is allowed to match, because []()
# resolves to nothing and is handled below rather than skipped by the regex.
LINK_RE = re.compile(
    r"\]\(\s*(<[^<>\n]*>|[^\s()]*)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?\s*\)")

# The reference spellings: [text][label] and the collapsed [label][]. The two
# bracket groups must touch, so "- [ ] [UAT](uat-plan.md)" stays a checkbox
# beside an inline link rather than becoming a reference to a label named " ".
# The definition line gives a label its destination, and that destination is
# checked exactly like an inline one.
REF_USE_RE = re.compile(r"\[([^\[\]]*)\]\[([^\[\]]*)\](?!\()")
REF_DEF_RE = re.compile(
    r"^ {0,3}\[([^\[\]]+)\]:\s*(<[^<>]*>|\S+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^()]*\)))?\s*$")

ATX_RE = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HTML_ANCHOR_RE = re.compile(
    r"<a\s[^>]*?\b(?:name|id)\s*=\s*[\"']([^\"']+)[\"']", re.I)
REPO_PATH_RE = re.compile(
    r"\b((?:os|templates|knowledge|skills|agents|system|routing|modules|"
    r"examples|docs)/[A-Za-z0-9._/\-]*[A-Za-z0-9])")
HEADER_KEYS = ("Stage:", "Knowledge:", "Skill:")
HEADER_WINDOW = 8

# A manifest line in a system prompt: a directory, whitespace, then the files
# it holds, named relative to it.
MANIFEST_PREFIX_RE = re.compile(
    r"^(?:>\s*)?([A-Za-z0-9._\-]+(?:/[A-Za-z0-9._\-]+)*/)\s{2,}\S")

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

# Read from os/STAGE-GATES.md when it is there, so the gate set and the
# stage-to-gate mapping come from the document that defines them rather than
# from a constant that can drift away from it. These are the fallback for a
# tree that has no STAGE-GATES.md, which is how the unit fixtures run.
GATE_NUMBERS = (1, 2, 3, 4, 5, 6)
STAGE_CLOSED_BY = {"DISCOVER": 1, "DEFINE": 2, "DESIGN": 3, "BUILD": 4,
                   "DELIVER": 5, "OPERATE": 6}
GATE_HEADING_RE = re.compile(r"^##\s*Gate\s+(\d+)\b", re.M)
CLOSES_RE = re.compile(r"^Closes\s+([A-Z][A-Z ]*?)\.", re.M)

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
FM_ITEM_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")

# The Stage line of the file's own three-line header, which is the claim a
# reader believes. The declaration has to agree with it.
STAGE_HEADER_RE = re.compile(r"^\s*Stage:\s*(.*)$")
GATE_MENTION_RE = re.compile(r"\bgates?\b((?:\s*(?:and|or|to|,)?\s*\d+)+)", re.I)
HEADER_SCAN_LINES = 12


def fields(block):
    """Top-level keys of a YAML block, values as text, block lists folded in.

    Not a YAML implementation, but not blind to one either: a key whose value
    sits on the following lines as a block sequence is folded into the inline
    form, because the two spellings mean the same thing and a gate that reads
    only one of them can be evaded by choosing the other.
    """
    out, key = {}, None
    for line in block.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = FM_ITEM_RE.match(line)
        if item and key and not FM_FIELD_RE.match(line):
            out[key] = flow_list(out.get(key, ""), item.group(1))
            continue
        match = FM_FIELD_RE.match(line)
        if match and not line.startswith((" ", "\t")):
            key = match.group(1).lower()
            out[key] = match.group(2).strip()
        elif not line.startswith((" ", "\t")):
            key = None
    return out


def flow_list(current, item):
    """Append one block-sequence item to a value, as an inline YAML list."""
    items = values_of(current) if current.strip() else []
    items.append(item.strip().strip("'\""))
    return "[%s]" % ", ".join('"%s"' % v.replace('"', '\\"') for v in items)


def values_of(text):
    """A declaration value as a list: an inline list, or a lone scalar.

    Quote-aware, because an alias is allowed to contain a comma. Splitting
    "Now, Next, Later roadmap" on commas invents three aliases that resolve
    nothing and, worse, collide with real ones.
    """
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    parts, current, quote, escape = [], [], None, False
    for char in text:
        if escape:
            current.append(char)
            escape = False
        elif char == "\\" and quote == '"':
            escape = True
        elif quote:
            if char == quote:
                quote = None
            else:
                current.append(char)
        elif char in "'\"":
            quote = char
        elif char == ",":
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


def gate_contract(root):
    """(gate numbers, {stage: closing gate}) as os/STAGE-GATES.md states them."""
    try:
        raw = (Path(root) / "os" / "STAGE-GATES.md").read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return set(GATE_NUMBERS), dict(STAGE_CLOSED_BY)
    numbers = [int(n) for n in GATE_HEADING_RE.findall(raw)]
    closes = {}
    for match in GATE_HEADING_RE.finditer(raw):
        tail = raw[match.end():]
        stage = CLOSES_RE.search(tail[:tail.find("\n## ") if "\n## " in tail
                                      else len(tail)])
        if stage:
            closes[stage.group(1).strip()] = int(match.group(1))
    if not numbers:
        return set(GATE_NUMBERS), dict(STAGE_CLOSED_BY)
    return set(numbers), closes or dict(STAGE_CLOSED_BY)


def stage_header(raw):
    """The Stage: line of the file's own header block, or None."""
    match = FRONTMATTER_RE.match(raw)
    body = raw[match.end():] if match else raw
    for line in body.split("\n")[:HEADER_SCAN_LINES]:
        found = STAGE_HEADER_RE.match(line)
        if found:
            return found.group(1)
    return None


def stages_named(line):
    """Vocabulary stages the header line names, in vocabulary order."""
    return [s for s in STAGE_VOCABULARY
            if re.search(r"\b%s\b" % s.replace(" ", r"\s+"), line)]


def gates_named(line):
    """Gate numbers the header line names."""
    found = set()
    for match in GATE_MENTION_RE.finditer(line):
        found.update(int(n) for n in re.findall(r"\d+", match.group(1)))
    return found


def entropy(text):
    """Shannon entropy of a string, in bits per character."""
    if not text:
        return 0.0
    counts = collections.Counter(text).values()
    return -sum((n / len(text)) * math.log2(n / len(text)) for n in counts)


def secret_hits(line):
    """Every secret-shaped string on one line, as labels."""
    labels = []
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, line):
            labels.append(label)
    for match in SECRET_NAME_RE.finditer(line):
        value = match.group(1)
        classes = sum(bool(re.search(p, value))
                      for p in ("[a-z]", "[A-Z]", "[0-9]"))
        if classes >= 2 and entropy(value) >= ENTROPY_FLOOR:
            labels.append("high-entropy value assigned to a "
                          "credential-shaped name")
    for match in BASE64_RUN_RE.finditer(line):
        run = match.group(0)
        try:
            decoded = base64.b64decode(
                run + "=" * (-len(run) % 4), validate=True).decode("utf-8",
                                                                   "replace")
        except ValueError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, decoded):
                labels.append("base64-encoded " + label)
    return labels


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


def wikilink_lands(target, tree, aliases, basenames):
    """Why [[target]] does not land, or None when it does.

    A qualified target resolves exactly. Proving that some file of that
    basename exists somewhere is not proving that the named one does, and it
    is how [[wrong/place/target.md]] used to pass. A bare name is allowed
    because a vault link is written that way, but only while it is unambiguous:
    two files of that name and the link means whichever the reader guesses.
    """
    if target.lower() in aliases:
        return None
    if "/" in target:
        if target in tree or target + ".md" in tree:
            return None
        return ("names neither a file at that path nor a declared alias")
    hits = basenames.get(target, []) + basenames.get(target + ".md", [])
    if not hits:
        return "names neither a file in the tree nor a declared alias"
    if len(set(hits)) > 1:
        return ("is ambiguous: %s files are named that (%s). Qualify it with "
                "its path" % (len(set(hits)), ", ".join(sorted(set(hits))[:3])))
    return None


# Directories the walker never enters: VCS internals, and the scratch
# directories .gitignore already keeps out of the repository. .pytest_cache is
# why this is a named set rather than the four it used to be: it holds its own
# README.md, so the wikilink gate's count of files named README.md came out at
# 23 on a machine where pytest had run and lower on one where it had not. A gate
# whose view of the tree depends on local scratch is not a gate.
#
# .obsidian is deliberately NOT in this set. It is the committed vault config,
# it ships with the repository, and it is content the gate is supposed to judge.
# That is also why this is a list of directory names and never a rule about a
# leading dot: the dot says nothing about whether Git tracks the directory.
SCRATCH_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def tracked_files(root):
    """Every file in the tree except VCS internals, scratch, and workspaces.

    products/ and learn/products/ hold a user's own filled drafts (gitignored);
    the gate judges the shipped system, never someone's work in progress. The
    two workspace README.md files stay in scope because they ship with the repo.
    """
    skip = SCRATCH_DIRS
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (skip & set(path.parts)) \
                and not path.name.startswith("._"):
            rel = path.relative_to(root).parts
            in_workspace = (rel[:1] == ("products",) and rel[1:] != ("README.md",)) \
                or (rel[:2] == ("learn", "products") and rel[2:] != ("README.md",))
            if in_workspace:
                continue
            yield path


def in_tree(target, tree):
    """True when a named path is a tracked file or a tracked directory."""
    return target in tree or any(t.startswith(target + "/") for t in tree)


def in_angle_field(line, start):
    """True when position start sits inside an <angle-bracket> fill-in field."""
    left = line.rfind("<", 0, start)
    return left != -1 and line.find(">", left) > start


def slug(heading):
    """A heading as the anchor GitHub gives it.

    Lowercased, markup and punctuation dropped, inner whitespace hyphenated.
    Not every renderer agrees on the edges, so the gate only ever uses this to
    say that an anchor names no heading in the file it points at, which is the
    failure worth reporting.
    """
    text = MD_LINK_RE.sub(r"\1", heading)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\s\-]", "", text)
    return re.sub(r"\s+", "-", text)


def anchors_of(lines):
    """Every anchor a markdown file offers: heading slugs and explicit names.

    Repeated headings take the -1, -2 suffixes the renderers add, so a link to
    the second "## Owner" resolves the way the reader's browser resolves it.
    """
    found, counts = set(), collections.Counter()
    for line in lines:
        match = ATX_RE.match(line)
        if match:
            base = slug(match.group(2))
            if base:
                found.add(base if not counts[base]
                          else "%s-%d" % (base, counts[base]))
                counts[base] += 1
        for explicit in HTML_ANCHOR_RE.finditer(line):
            found.add(explicit.group(1))
    return found


def destination(dest):
    """A raw link destination as (path, anchor), unwrapped and unescaped.

    <angle brackets> come off, because they are the only way to write a
    destination with a space in it, and %20 comes out, because the file on disk
    is named with the space rather than with the escape.
    """
    text = dest.strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    if text.startswith(("http://", "https://", "mailto:")):
        return None, None
    path, _, anchor = text.partition("#")
    return urllib.parse.unquote(path).strip(), urllib.parse.unquote(anchor).strip()


def target_problems(path, line_no, dest, inside, lines, tree=None, cache=None):
    """Why one link destination does not land, as (line, code, message) rows."""
    out = []
    target, anchor = destination(dest)
    if target is None:
        return out
    if not target:
        # A same-file anchor. The path half is this file, so only the anchor
        # can be wrong, and an anchor nobody wrote is a link nobody can follow.
        if anchor and anchor not in anchors_of(lines):
            out.append((line_no, "LINK", "anchor #%s names no heading in this "
                        "file." % anchor))
        return out
    if target.startswith("/"):
        return [(line_no, "LINK", "absolute local path %s in a link." % target)]
    landing = (path.parent / target).resolve()
    if not landing.is_relative_to(inside):
        return [(line_no, "LINK", "link %s climbs out of the repository, to %s."
                 % (target, landing))]
    if not landing.exists():
        return [(line_no, "LINK", "relative link %s does not resolve." % target)]
    if tree is not None and landing.is_file() and \
            landing.relative_to(inside).as_posix() not in tree:
        return [(line_no, "LINK", "link %s resolves to %s, which is not a file "
                 "this gate tracks."
                 % (target, landing.relative_to(inside).as_posix()))]
    if anchor and landing.is_file() and landing.suffix == ".md":
        if cache is None:
            cache = {}
        if landing not in cache:
            try:
                cache[landing] = anchors_of(mask(
                    landing.read_text(encoding="utf-8")))
            except (UnicodeDecodeError, OSError):
                cache[landing] = None
        known = cache[landing]
        if known is not None and anchor not in known:
            out.append((line_no, "LINK", "link %s names anchor #%s, which is no "
                        "heading in %s." % (target, anchor, target)))
    return out


def link_problems(path, lines, inside, tree=None, cache=None):
    """Every link in one markdown file that does not land, as failure rows.

    Inline links, reference definitions, and reference uses, because a reader
    follows all three and the gate used to read only the first. A definition is
    checked once, where it is written, rather than once per use of its label.
    """
    out, defs = [], {}
    for i, line in enumerate(lines, 1):
        found = REF_DEF_RE.match(line)
        if found:
            defs[found.group(1).strip().lower()] = (i, found.group(2))
    for i, line in enumerate(lines, 1):
        for match in LINK_RE.finditer(line):
            out.extend(target_problems(path, i, match.group(1), inside, lines,
                                       tree, cache))
        for match in REF_USE_RE.finditer(line):
            label = (match.group(2).strip() or match.group(1).strip())
            if label and label.lower() not in defs:
                out.append((i, "LINK", "reference-style link [%s] has no [%s]: "
                            "definition in this file." % (label, label)))
    for _, (i, dest) in sorted(defs.items()):
        out.extend(target_problems(path, i, dest, inside, lines, tree, cache))
    return out


def os_check(root, pins=None):
    """Whole-tree gate. Returns sorted (relpath, line, code, message) tuples."""
    root = Path(root)
    pins = PINNED_HASHES if pins is None else pins
    problems = []
    fail = lambda p, n, c, m: problems.append((str(p), n, c, m))  # noqa: E731

    all_files = list(tracked_files(root))
    rel = {p: p.relative_to(root).as_posix() for p in all_files}
    tree = set(rel.values())
    inside = root.resolve()
    anchor_cache = {}
    basenames = collections.defaultdict(list)
    for target in tree:
        basenames[target.split("/")[-1]].append(target)
    layers = {part for part in (t.split("/")[0] for t in tree)
              if part in GRAPH_LAYERS}
    gate_numbers, stage_closed_by = gate_contract(root)

    # Check 7, integrity gate: runs first and inside modules/regulated/,
    # which is otherwise exempt from tree mode.
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
            owner = aliases.setdefault(alias.lower(), rp)
            if owner != rp:
                fail(rp, 1, "GRAPH", 'alias "%s" is already declared by %s. '
                     "One alias, one file, or a wikilink resolves to whichever "
                     "sorts first." % (alias, owner))

    for path in all_files:
        rp = rel[path]
        if rp.startswith("modules/regulated/"):
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(rp, 1, "ENCODING", "is not valid UTF-8, so not one check "
                 "below could read it. A file the gate cannot read is a file "
                 "the gate has not cleared, which is why this fails rather "
                 "than skips.")
            continue
        except OSError:
            fail(rp, 1, "ENCODING", "could not be read from disk, so no check "
                 "below ran against it.")
            continue
        raw_lines = raw.split("\n")
        lines = mask(raw) if path.suffix == ".md" else raw_lines
        is_doc = path.suffix in (".md", ".json")

        # Check 9, secret gate: every readable file, with no file-level
        # exemption. The closed-up text is scanned as well, so a token broken
        # across a line break is caught the way a split metric string is.
        seen_secrets = set()
        for i, line in enumerate(raw_lines, 1):
            for label in secret_hits(line):
                if (i, label) not in seen_secrets:
                    seen_secrets.add((i, label))
                    fail(rp, i, "SECRET", "matches the %s pattern." % label)
        joined, origin = collapse(raw_lines)
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, joined):
                key = (origin[m.start()], label)
                if key not in seen_secrets:
                    seen_secrets.add(key)
                    fail(rp, key[0], "SECRET", "matches the %s pattern once "
                         "the line breaks are closed up." % label)

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

        # Check 4, link gate: markdown files only. The rules are unchanged and
        # the parser under them reads the spellings it used to skip, so a link
        # with a title, a space, or an anchor is now judged rather than missed.
        if path.suffix == ".md":
            for i, code, message in link_problems(path, lines, inside, tree,
                                                  anchor_cache):
                fail(rp, i, code, message)

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
        # Raw lines, not masked ones: the prompt body a user pastes lives
        # inside a fenced block, so masking the fences hid the only text this
        # check exists to read. The manifest inside that fence lists a
        # directory and then its contents, so a name is resolved against the
        # directory prefix in force as well as against the repository root.
        if rp.startswith("system/"):
            prefix = ""
            for i, line in enumerate(raw_lines, 1):
                head = MANIFEST_PREFIX_RE.match(line)
                if head and in_tree(head.group(1).rstrip("/"), tree):
                    prefix = head.group(1)
                elif line.strip() and not line.startswith((" ", "\t")):
                    prefix = ""
                for m in REPO_PATH_RE.finditer(line):
                    named = m.group(1)
                    if in_tree(named, tree) or (prefix and
                                                in_tree(prefix + named, tree)):
                        continue
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
                layer = block.get("layer", "").strip().strip("'\"")
                own = rp.split("/")[0]
                if "layer" in block and layer not in layers:
                    fail(rp, 1, "GRAPH", 'layer "%s" is not a layer directory '
                         "in this tree (%s)."
                         % (layer, ", ".join(sorted(layers))))
                elif "layer" in block and layer != own:
                    fail(rp, 1, "GRAPH", 'layer "%s" is not the directory this '
                         'file lives in, which is "%s".' % (layer, own))
                stage = block.get("stage", "").strip().strip("'\"")
                if "stage" in block and stage not in STAGE_VOCABULARY:
                    fail(rp, 1, "GRAPH", 'stage "%s" is not one of %s.'
                         % (stage, ", ".join(STAGE_VOCABULARY)))
                gate = block.get("gate", "").strip().strip("'\"")
                if "gate" in block and not (gate.isdigit()
                                            and int(gate) in gate_numbers):
                    fail(rp, 1, "GRAPH", 'gate "%s" is not one of the gates '
                         "os/STAGE-GATES.md defines (%s)."
                         % (gate, ", ".join(str(n)
                                            for n in sorted(gate_numbers))))
                # The declaration against the file's own three-line header,
                # and against the gate the stage closes. A declaration that
                # contradicts the sentence under it renders a confident arrow
                # nobody in the room agrees with.
                header = stage_header(raw)
                header_stages = stages_named(header) if header else []
                header_gates = gates_named(header) if header else set()
                if header_stages and stage and stage not in header_stages:
                    fail(rp, 1, "GRAPH", 'declares stage "%s" while its own '
                         "Stage header says %s."
                         % (stage, ", ".join(header_stages)))
                if header_gates and gate.isdigit() \
                        and int(gate) not in header_gates:
                    fail(rp, 1, "GRAPH", 'declares gate %s while its own Stage '
                         "header names gate %s."
                         % (gate, ", ".join(str(n) for n in
                                            sorted(header_gates))))
                elif not header_gates and gate.isdigit() \
                        and stage in stage_closed_by \
                        and int(gate) != stage_closed_by[stage]:
                    fail(rp, 1, "GRAPH", "declares stage %s with gate %s, but "
                         "os/STAGE-GATES.md has gate %d closing %s. Name the "
                         "gate in the Stage header if the artifact really "
                         "lands at a later one."
                         % (stage, gate, stage_closed_by[stage], stage))
                for key in ("feeds", "method"):
                    for value in values_of(block.get(key, "")):
                        targets = gates_named(value)
                        if re.search(r"\bgates?\b", value, re.I):
                            # tools/graph.py renders this as a gate arrow, so
                            # the gate gate accepts it and checks the number.
                            stray = sorted(targets - gate_numbers)
                            if not targets:
                                fail(rp, 1, "GRAPH", "%s names %r, which reads "
                                     "as a gate and names no gate number."
                                     % (key, value))
                            elif stray:
                                fail(rp, 1, "GRAPH", "%s names gate %s, which "
                                     "os/STAGE-GATES.md does not define."
                                     % (key, ", ".join(str(n) for n in stray)))
                        elif points_at(value, rp, tree) is None:
                            fail(rp, 1, "GRAPH", "%s names %s, which is not a "
                                 "file in the tree." % (key, value))

        # Check 11, wikilink gate: additive Obsidian links, every layer. A
        # relative markdown link is what GitHub renders and check 4 owns those;
        # a wikilink is what the vault graph reads, and an unresolved one is an
        # edge the graph silently drops.
        if path.suffix == ".md" and rp not in RULE_BEARING:
            for i, line in enumerate(lines, 1):
                for m in WIKILINK_RE.finditer(line):
                    target = m.group(1).split("|")[0].split("#")[0].strip()
                    why = wikilink_lands(target, tree, aliases,
                                         basenames) if target else None
                    if why:
                        fail(rp, i, "WIKILINK",
                             "wikilink [[%s]] %s." % (target, why))

    return sorted(problems)


# ---------------------------------------------------------------------------
# Workspace mode and JSON mode. Both are additive; tree mode is unchanged and
# still runs its eleven checks.
# ---------------------------------------------------------------------------

# Named here so the mode can print what it ran, and so a reader can see the
# list is short on purpose. The checks tree mode runs and this one does not are
# the ones that judge a file for being a template, a layer file, or a shipped
# part of the repository. A user's draft is none of those.
WORKSPACE_CHECKS = ("links", "secrets", "placeholders", "dashes",
                    "banned metric strings")


def workspace_files(workspace):
    """Every file under one workspace, minus VCS internals and caches."""
    skip = {".git", "__pycache__", ".venv", "node_modules"}
    for path in sorted(Path(workspace).rglob("*")):
        if path.is_file() and not (skip & set(path.parts)) \
                and not path.name.startswith("._"):
            yield path


def workspace_check(workspace, root=None):
    """Content gate over one user workspace. Returns sorted 4-tuples.

    The workspace is gitignored and invisible to tree mode by design, so this
    is the only check it gets and it is opt-in. Links resolve against the
    repository root rather than the workspace, because a filled artifact links
    back to the templates and the gates it came from.
    """
    workspace = Path(workspace).resolve()
    root = Path(root).resolve() if root is not None else Path.cwd().resolve()
    if not workspace.is_relative_to(root):
        root = workspace
    problems = []
    fail = lambda p, n, c, m: problems.append((str(p), n, c, m))  # noqa: E731
    anchor_cache = {}

    for path in workspace_files(workspace):
        rp = path.relative_to(root).as_posix()
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(rp, 1, "ENCODING", "is not valid UTF-8, so not one check "
                 "below could read it.")
            continue
        except OSError:
            fail(rp, 1, "ENCODING", "could not be read from disk, so no check "
                 "below ran against it.")
            continue
        raw_lines = raw.split("\n")
        lines = mask(raw) if path.suffix == ".md" else raw_lines

        seen_secrets = set()
        for i, line in enumerate(raw_lines, 1):
            for label in secret_hits(line):
                if (i, label) not in seen_secrets:
                    seen_secrets.add((i, label))
                    fail(rp, i, "SECRET", "matches the %s pattern." % label)
        joined, origin = collapse(raw_lines)
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, joined):
                key = (origin[m.start()], label)
                if key not in seen_secrets:
                    seen_secrets.add(key)
                    fail(rp, key[0], "SECRET", "matches the %s pattern once "
                         "the line breaks are closed up." % label)

        if path.suffix not in (".md", ".json"):
            continue

        for i, line in enumerate(raw_lines, 1):
            for char, name in DASHES.items():
                if char in line:
                    fail(rp, i, "DASH",
                         "contains an %s. Use a comma or a colon." % name)

        seen = set()

        def banned_here(line_no, label):
            """One finding, unless the figure on that line carries a source."""
            if (line_no, label) in seen:
                return
            seen.add((line_no, label))
            if sourced_near(lines, line_no - 1):
                return
            fail(rp, line_no, "BANNED",
                 "contains %s with no source beside it. In your own workspace "
                 "this is only banned when it is unsourced: it is one of the "
                 "worked example's numbers, so a bare copy of it reads as the "
                 "example's answer rather than yours. Cite where it came from "
                 "on the same line or the next one, or replace it with your "
                 "own figure. Do not round it to get past this." % label)

        for i, line in enumerate(lines, 1):
            for pattern, label in BANNED_METRICS:
                if re.search(pattern, line, re.I):
                    banned_here(i, label)
        collapsed, origin = collapse(lines)
        for pattern, label in BANNED_METRICS:
            for m in re.finditer(pattern, collapsed, re.I):
                banned_here(origin[m.start()], label)

        for i, line in enumerate(lines, 1):
            for m in PLACEHOLDER_RE.finditer(line):
                if not in_angle_field(line, m.start()):
                    fail(rp, i, "TBD", '"%s" is a deferred decision, not an '
                         "answer." % m.group(1))

        if path.suffix == ".md":
            for i, code, message in link_problems(path, lines,
                                                  root, None, anchor_cache):
                fail(rp, i, code, message)

    return sorted(problems)


def json_problems(root):
    """Every tracked .json file that does not parse, as sorted 4-tuples."""
    problems = []
    for path in tracked_files(Path(root)):
        if path.suffix != ".json":
            continue
        rp = path.relative_to(Path(root)).as_posix()
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            problems.append((rp, 1, "JSON", "is not valid UTF-8, so it is not "
                             "JSON either."))
        except OSError:
            problems.append((rp, 1, "JSON", "could not be read from disk."))
        except json.JSONDecodeError as broken:
            problems.append((rp, broken.lineno, "JSON",
                             "does not parse: %s at column %d."
                             % (broken.msg, broken.colno)))
    return sorted(problems)


def report(problems, ok_line):
    """Print failure rows, or the ok line. Returns the exit status."""
    for rp, line_no, code, message in problems:
        print("%s:%d: %s %s" % (rp, line_no, code, message))
    if problems:
        print("\n%d problem(s). The gate failed, which is the point of having "
              "one." % len(problems), file=sys.stderr)
        return 1
    print(ok_line)
    return 0


def run_workspace_mode(target, root=None):
    target = Path(target)
    if not target.is_dir():
        print("%s: not a directory. Workspace mode checks one workspace, for "
              "example products/my-product." % target, file=sys.stderr)
        return 1
    files = list(workspace_files(target))
    if not files:
        print("%s: no files to check." % target)
        return 0
    return report(workspace_check(target, root),
                  "%s: ok (workspace mode, %d file%s, %s)"
                  % (target, len(files), "" if len(files) == 1 else "s",
                     ", ".join(WORKSPACE_CHECKS)))


def run_json_mode(root):
    return report(json_problems(root),
                  "%s: ok (every tracked .json file parses)" % root)


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
    parser.add_argument("--workspace", metavar="DIR",
                        help="content gate over one product workspace, for "
                             "example products/my-product. Links, secrets, "
                             "placeholders, dashes, banned metric strings")
    parser.add_argument("--json-syntax", dest="json_mode", action="store_true",
                        help="parse every tracked .json file and report each "
                             "syntax error")
    parser.add_argument("--no-stale-fail", action="store_true",
                        help="report a stale as-of date as a notice rather than a "
                             "failure. For forks that accept the staleness")
    args = parser.parse_args(argv)

    if args.os_mode:
        return run_os_mode(args.files[0] if args.files else Path("."))
    if args.workspace:
        return run_workspace_mode(args.workspace,
                                  args.files[0] if args.files else None)
    if args.json_mode:
        return run_json_mode(args.files[0] if args.files else Path("."))
    if not args.files:
        parser.error("give at least one file, or use --os, --workspace, or "
                     "--json-syntax")

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
