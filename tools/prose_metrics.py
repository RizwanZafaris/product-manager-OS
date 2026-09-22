#!/usr/bin/env python3
"""Measure the running prose in a Markdown file, whole-file rather than by line window.

A word count taken over a line range moves the moment anything above it is
edited, so it can be satisfied by pushing the long paragraph further down the
file instead of shortening it.  Every reading here is taken over the whole
document, which a rewrite cannot dodge.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# A fence opener this models: at the left margin, three or more backticks or
# tildes. A backtick fence's info string may not itself hold a backtick.
FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})(.*)$")
THEMATIC_BREAK = re.compile(r"^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$")
# A line that opens a heading, a list item, a blockquote or an HTML comment, at
# the start of a block. Such a line is not running prose. Table rows are
# recognised separately, by their delimiter row, because a line that merely
# starts with "|" is not a table.
NOT_PROSE = re.compile(r"^(\s*(#{1,6}(\s|$)|[-*+]([ \t]|$)|>|\d{1,9}[.)]([ \t]|$))|<!--)")
# The openers CommonMark lets interrupt a paragraph already running: indented
# at most three spaces, a bullet only with content, and an ordered item only
# when it starts at 1 and has content. Any other such line inside a paragraph
# is a continuation line of that paragraph.
INTERRUPTS = re.compile(r"^ {0,3}(#{1,6}(\s|$)|[-*+][ \t]+\S|>|1[.)][ \t]+\S)|^<!--")
# A list-item or blockquote marker, at any indent.
CONTAINER = re.compile(r"^[ \t]*([-*+]|\d{1,9}[.)])(?=[ \t]|$)|^[ \t]*>")
# What, after a container marker or on a lazy line, starts something other
# than a paragraph: a heading, raw HTML or a comment, a table row, or a link
# reference definition, which markdown-it reads as a block of its own. (A
# fence is not listed: one at the margin is opened before this is asked, and
# any other is refused by UNMODELLED.)
NOT_A_PARAGRAPH = re.compile(r"^(#{1,6}(\s|$)|<|\||\[[^\]]*\]:)")
# What this does not model, outside a fence or a comment: a fence or comment
# opener that is indented or follows a list or quote marker, which the item or
# quote then holds until a line outside it ends both, and a line that may open
# a raw HTML block, whose text renders.
UNMODELLED = re.compile(r"^[ \t]+(`{3}|~{3}|<!--)|^[ \t]*<(?!!--)[A-Za-z/?!]"
                        r"|^[ \t]*(([-*+]|\d{1,9}[.)])[ \t]+|>[ \t]*)+(`{3}|~{3}|<)")
TABLE_ROW = re.compile(r"^ {0,3}\|")
DELIMITER_ROW = re.compile(r"^ {0,3}\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def indent(line: str) -> int:
    """Leading columns, a tab counting as four."""
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip(" "))


def cells(row: str) -> int:
    """How many cells a "|" row has, the way GFM counts them."""
    inner = row.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") else inner
    return len(re.split(r"(?<!\\)\|", inner))


def starts_table(row: str, following: str) -> bool:
    """A header row: GFM needs a delimiter row under it with as many cells."""
    return bool(TABLE_ROW.match(row) and DELIMITER_ROW.match(following)
                and cells(row) == cells(following))


def opens_fence(line: str):
    """The fence marker when the line opens a fenced code block, else None."""
    match = FENCE_OPEN.match(line)
    if not match or (match.group(1)[0] == "`" and "`" in match.group(2)):
        return None
    return match.group(1)


def closes_fence(line: str, marker: str) -> bool:
    """The same character, at least as many of it, and nothing after."""
    return bool(re.match(r"^ {0,3}%s{%d,}[ \t]*$" % (re.escape(marker[0]), len(marker)),
                         line))


def leaves_a_paragraph_open(line: str) -> bool:
    """Whether a list-item or blockquote line ends inside a paragraph.

    Only an open paragraph takes lazy continuation lines, so this decides
    whether the lines after it are folded into the item. When in doubt it
    answers False, which counts the following lines as prose. Its callers
    ask only about a line indented at most three columns, so a leading tab
    never reaches it.
    """
    rest = line
    while True:
        match = CONTAINER.match(rest)
        if not match:
            break
        rest = rest[match.end():]
        gap = rest[:len(rest) - len(rest.lstrip(" \t"))]
        if "\t" in gap or len(gap) >= 4:
            return False  # indented code, or nothing, inside the item or quote
        rest = rest.lstrip(" \t")
    body = rest.strip()
    return bool(body) and not THEMATIC_BREAK.match(body) \
        and not NOT_A_PARAGRAPH.match(body)


SENTENCE_END = re.compile(r"[.!?](?:[\"')\]]+)?(?:\s|$)")


def unmodelled_line(text: str) -> int:
    """The first line prose_blocks cannot read, or 0 when it reads them all."""
    marker = None
    in_comment = False
    for number, raw in enumerate(text.splitlines(), 1):
        if marker is not None:
            marker = None if closes_fence(raw, marker) else marker
        elif in_comment:
            in_comment = "-->" not in raw
        elif UNMODELLED.match(raw):
            return number
        elif raw.startswith("<!--"):
            in_comment = "-->" not in raw
        else:
            marker = opens_fence(raw)
    return 0


def prose_blocks(text: str) -> list[tuple[int, str]]:
    """Every run of running prose, as (first line, text).

    A run is a stretch of consecutive non-blank lines none of which is
    structure. Structure is a fenced code block, a table (a "|" row followed
    by a delimiter row with as many cells, and the "|" rows that follow it
    with no blank line between, up to a line less indented than its header),
    a heading, a thematic break, a list item, a blockquote, or an HTML
    comment (through the line holding "-->"), plus the lazy continuation
    lines a list item or blockquote takes after it before the next blank
    line, since Markdown renders those as part of the item or the quote. Only
    an item or quote that ends in a paragraph takes them (see
    leaves_a_paragraph_open), and a line that could start another block ends
    them, so the prose after a heading, a comment, a fence or a thematic
    break under a list item is prose.

    Structure is excluded line by line, not block by block. A paragraph that
    one list line follows is still a paragraph of the length it has: a ceiling
    check that dropped the whole block would let a single trailing "- ..."
    line hide a paragraph of any length. Inside a running paragraph only the
    lines CommonMark lets interrupt one end it (see INTERRUPTS), so a wrapped
    line that happens to begin "2026. " or "| " stays in its paragraph.

    This is not a Markdown parser, and it does not track list nesting. It
    reads fences and comments only at the left margin. A document holding
    anything it does not read is returned whole, as one block from line 1, so
    a ceiling it is held to fails rather than passes on a guess: a fence or
    comment line that is indented or follows a list or quote marker, which
    the item or quote would hold until a line outside it ends both, and a
    line that may open a raw HTML block, whose text renders (see UNMODELLED
    and unmodelled_line). Elsewhere, where its reading is known to depart
    from CommonMark it counts more as prose, not less: a line straight after
    a table with no blank line between (GFM may render it as one more row), a
    paragraph a setext underline turns into a heading, an indented code
    block, a table without a leading "|", a table whose delimiter row has no
    leading "|" (from that row on), a list item's later paragraphs, the lazy
    continuation of a nested item after a blank line or of an item or quote
    line indented four or more columns, a "|" line an item or quote would
    take as lazy text, and what follows an item whose text is a table row or
    a link reference definition are all counted as prose. ProseMetricsTests in
    tests/test_tools_gates.py holds an example of each reading above. Those
    are examples, not a proof: no test shows that every guard here is needed,
    nor that no other input is under-counted.
    """
    if unmodelled_line(text):
        return [(1, text)]
    lines = text.splitlines()
    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start = 0
    absorbing = False
    in_comment = False
    table_indent = None  # the header's indent while a table is open
    fence = None  # the marker of the open fenced code block

    def close() -> None:
        nonlocal current
        if current:
            blocks.append((start, "\n".join(current)))
            current = []

    for number, raw in enumerate(lines, 1):
        if fence is not None:
            if closes_fence(raw, fence):
                fence = None
            continue
        if in_comment:
            in_comment = "-->" not in raw
            continue
        if not raw.strip():
            close()
            absorbing = False
            table_indent = None
            continue
        opened = opens_fence(raw)
        if opened:
            close()
            fence = opened
            absorbing = False
            table_indent = None
            continue
        following = lines[number] if number < len(lines) else ""
        if (table_indent is not None and TABLE_ROW.match(raw)
                and indent(raw) >= table_indent):
            continue  # a body row
        table_indent = None
        if starts_table(raw, following):
            close()
            table_indent = indent(raw)
            absorbing = False
            continue
        if THEMATIC_BREAK.match(raw):
            close()
            absorbing = False
            continue
        if absorbing:
            if CONTAINER.match(raw) or THEMATIC_BREAK.match(raw.lstrip(" \t")):
                # A sibling or nested item, or a quote: its text is not prose,
                # and it takes lazy lines only if it too ends in a paragraph.
                # Four or more columns in, renderers disagree on whether the
                # line nests or continues, so what follows is counted.
                absorbing = indent(raw) <= 3 and leaves_a_paragraph_open(raw)
                continue
            if not NOT_A_PARAGRAPH.match(raw.lstrip(" \t")):
                continue  # a lazy continuation line
            absorbing = False  # could start another block: read it afresh
        opens = INTERRUPTS.match(raw) if current else NOT_PROSE.match(raw)
        if opens:
            close()
            if raw.startswith("<!--"):
                in_comment = "-->" not in raw
            elif indent(raw) <= 3 and CONTAINER.match(raw):
                absorbing = leaves_a_paragraph_open(raw)
            continue
        if not current:
            start = number
        current.append(raw)
    close()
    return blocks


def longest_prose_block(text: str) -> tuple[int, int]:
    """The line and word count of the longest prose block, or (0, 0)."""
    measured = [(len(body.split()), line) for line, body in prose_blocks(text)]
    if not measured:
        return 0, 0
    words, line = max(measured)
    return line, words


def mean_sentence_words(text: str) -> float:
    """Mean words per sentence across the prose blocks, 0.0 when there are none."""
    words = 0
    sentences = 0
    for _line, body in prose_blocks(text):
        flat = " ".join(body.split())
        words += len(flat.split())
        sentences += max(1, len(SENTENCE_END.findall(flat)))
    return round(words / sentences, 1) if sentences else 0.0


def measure(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    line, words = longest_prose_block(text)
    return {"path": str(path), "longest_prose_block_line": line,
            "longest_prose_block_words": words,
            "unmodelled_line": unmodelled_line(text),
            "mean_sentence_words": mean_sentence_words(text),
            "prose_blocks": len(prose_blocks(text))}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    results = [measure(path) for path in args.paths]
    if args.json:
        print(json.dumps(results, sort_keys=True))
    else:
        for result in results:
            print("%s: longest prose block %d words at line %d, mean sentence "
                  "%.1f words" % (result["path"],
                                  result["longest_prose_block_words"],
                                  result["longest_prose_block_line"],
                                  result["mean_sentence_words"]))
            if result["unmodelled_line"]:
                print("  line %d is not something this reads, so the whole file "
                      "was measured as one block" % result["unmodelled_line"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
