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
"""
from __future__ import annotations

import argparse
import datetime as _dt
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--template", action="store_true",
                        help="structure-only mode for an unfilled template")
    parser.add_argument("--no-stale-fail", action="store_true",
                        help="report a stale as-of date as a notice rather than a "
                             "failure. For forks that accept the staleness")
    args = parser.parse_args(argv)

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
