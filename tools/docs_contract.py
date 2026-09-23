#!/usr/bin/env python3
"""Check operator-document accessibility and evidence-boundary claims."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


KEY_DOCS = ("README.md", "SECURITY.md", "docs/THREAT-MODEL.md",
            "docs/ACCESSIBILITY.md", "docs/ARCHITECTURE.md")
AMBIGUOUS = frozenset({"here", "this", "this link", "link", "more", "read more",
                       "click here", "details"})
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# CommonMark spells one heading two ways, and both had to be read before a
# repeat of one could be seen. ATX: the closing sequence "## Zed ##" is a
# decoration on the heading "Zed", so it is stripped rather than compared --
# a reviewer repeated a heading in that spelling and the comparison called
# "Zed ##" a different heading. The sequence is one or more hashes preceded
# by whitespace and followed by nothing else, so "## Hash # tag" keeps its
# hash and "## C# ##" is "C#".
HEADING = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+)?\s*$")
# Setext: a line of text underlined by "=" (level 1) or "-" (level 2). The
# other heading spelling, and the other half of the same evasion.
SETEXT = re.compile(r"^ {0,3}(=+|-+)\s*$")
# A previous line that a setext underline may NOT be reading. "-" carries
# three other meanings in this tree -- a thematic break, a list bullet and
# the closing fence of YAML front matter -- and a setext heading underlines a
# paragraph, never a heading, a table row, a block quote, a list item, an HTML
# block or an indented code block (four spaces or more). Every ambiguous shape
# is left unread rather than guessed at: a "---" after a blank line stays a
# thematic break, "| a | b |" over "|---|" stays a table, and the line under a
# code sample stays sample output.
NOT_SETEXT_TEXT = re.compile(
    r"^(?: {4,}|(?: {0,3}(?:[-*+>|<]|#{1,6}\s|\d+[.)]\s|=+\s*$)))")
FALSE_LIVE = re.compile(r"(?i)\b(?:100\s*/\s*100|all external gates are green|"
                        r"live sandbox verified|provider certified|regulatory certified|"
                        r"user validated)\b")
REQUIRED_BOUNDARIES = ("local evidence", "external evidence", "does not prove",
                       "live sandbox", "provider", "user", "regulatory")
# Which document has to carry each boundary phrase. The check used to test every
# phrase against the five key documents concatenated and then report the miss
# against docs/THREAT-MODEL.md whatever was actually missing, so six of the seven
# clauses could not fail while any one document still carried the words, and the
# one that could fail named a file that was not necessarily at fault. The threat
# model and the accessibility statement are the two documents that state the
# boundary; README.md has its own readme-boundary check below, and SECURITY.md
# and docs/ARCHITECTURE.md are not boundary statements.
BOUNDARY_OWNERS = {
    "docs/THREAT-MODEL.md": REQUIRED_BOUNDARIES,
    "docs/ACCESSIBILITY.md": tuple(phrase for phrase in REQUIRED_BOUNDARIES
                                   if phrase != "does not prove"),
}
REQUIRED_PATHS = ("pmos/cli.py", "pmos/domain.py", "pmos/store.py", "pmos/hooks.py",
                  "pmos/openrouter.py")

# The template inventory, which nothing measured. A stale figure survived in
# five files at once because the catalog's per-directory headings were
# self-consistently wrong: they summed to the number the front door claimed, so
# a reader who checked the arithmetic was reassured rather than alerted. The
# only reading that can catch that is a count taken from the tree.
TEMPLATES_DIR = "templates"
CATALOG = "templates/README.md"
# "## discovery (16 templates)": one heading per directory under templates/.
CATALOG_SECTION = re.compile(r"^##\s+([A-Za-z0-9_.-]+)\s+\((\d+)\s+templates?\)\s*$")
# Any count of templates or blanks. Inside the catalog every one of these is
# either a section heading, checked against that directory, or the whole total.
COUNT = re.compile(r"\b(\d+)\s+(?:templates?|blanks?)\b", re.I)
# An inventory claim in an operator document, as opposed to a count of some
# subset of the templates. "all 100 templates" and "all 100 blanks" say the
# figure covers the whole tree; "the 55 templates that name the knowledge
# index" counts something else and is not read here. That is a stated limit:
# a subset figure in these documents is checked by a reader, not by this gate.
INVENTORY = re.compile(r"\ball\s+(\d+)\s+(?:templates?|blanks?)\b", re.I)
# Where the front-door inventory claim lives. CHANGELOG.md is deliberately not
# in this set: it records what was true on the day of an entry, so its older
# figures are correct history and would fail a check against today's tree.
INVENTORY_DOCS = ("README.md", "docs/ARCHITECTURE.md")

# The gate count, measured from tools/ci_gate.py rather than trusted. A
# document naming a number of gates on the same line as ci_gate.py is making a
# claim about this tree, so it is read; a number on any other line is not,
# which is the same stated limit the inventory check carries. CHANGELOG.md is
# excluded for the reason given above: its older figures are correct history.
#
# Unlike the other counts in this file, this one is read in words as well as
# digits, up to ninety-nine, with "release" or "named" allowed before "gates".
# A larger figure in words is misread by its last words ("one hundred
# twenty-six gates" reads as 26); no document here writes one.
# docs/ARCHITECTURE.md said "twenty-two named gates" and "Its twenty-two gates"
# beside ci_gate.py while the file defined 25, and a check that read digits
# alone, in README.md and docs/FAQ.md alone, passed both.
_UNITS = ("zero one two three four five six seven eight nine ten eleven twelve "
          "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
NUMBER_WORDS = dict({word: value for value, word in enumerate(_UNITS)},
                    **{word: 10 * value for value, word in enumerate(_TENS, 2)})
GATE_COUNT = re.compile(
    r"\b(\d+|(?:%s)(?:[-\s](?:%s))?|%s)\s+(?:(?:release|named)\s+)?gates\b"
    % ("|".join(_TENS), "|".join(_UNITS[1:10]), "|".join(_UNITS)), re.I)
GATE_COUNT_DOCS = ("README.md", "docs/FAQ.md", "docs/ARCHITECTURE.md")
CI_GATE = "tools/ci_gate.py"
SECURITY = "SECURITY.md"

# How many scripts tools/ holds, stated in prose rather than inside the block
# the generator writes. The count in SECURITY.md was typed by hand until
# tools/exec_surface.py took it over, and a reviewer put the stale sentence
# back one line ABOVE the generated markers, where every check walked past it.
# A whole-directory claim is what is read, in either of two shapes: a verb and
# a number ("holds N scripts", "all N scripts", "contains N scripts") or a
# number and a scope ("N scripts in all", "in total", "altogether", "under
# `tools/`", "in `tools/`"). The second reviewer re-typed the stale figure in
# two wordings the first shape alone did not read -- "`tools/` contains
# eighteen scripts." and "There are 18 scripts under `tools/`." -- and both
# passed, so the scope half was added.
# A count of a named subset is still not read, which is why SECURITY.md's own
# "Six local scripts stay on this path" is left alone, the same stated limit
# INVENTORY carries above; the cost of naming the directory in the second shape
# is that a subset claim that also names it ("six local scripts in `tools/`")
# would be read as a whole-directory claim, and no sentence in this tree is
# written that way.
SCRIPT_COUNT = re.compile(
    r"\b(?:holds|all|contains)\s+(\d+|(?:%s)(?:[-\s](?:%s))?|%s)\s+scripts\b"
    r"|\b(\d+|(?:%s)(?:[-\s](?:%s))?|%s)\s+scripts\s+"
    r"(?:in\s+all|in\s+total|altogether|"
    r"(?:in|under)\s+`?%s/?`?)\b"
    % ("|".join(_TENS), "|".join(_UNITS[1:10]), "|".join(_UNITS),
       "|".join(_TENS), "|".join(_UNITS[1:10]), "|".join(_UNITS),
       "tools"), re.I)

# The interview-guide contradiction, as three readings of one line. A guide
# states its question rules as checklist items or table rows; the ban is on
# asking about the future, or on a question containing "would"; the closing
# commitment probe asks exactly that and the same guides require it. A line
# that states the ban without naming the exemption is the defect.
# The two figures SECURITY.md's prose derives from the generated table above
# it: how many scripts leave the manual path, and how many of the rest read an
# environment variable without leaving it. Both said something different before
# the table was generated, and both are a reader's summary of rows nobody can
# be asked to count. Sentence-specific on purpose, the way the gate count is
# tied to a line naming ci_gate.py: a rewording drops the reading, and the
# check says only what the sentence it matches says.
LEAVE_CLAIM = re.compile(
    r"\b(\d+|(?:%s)(?:[-\s](?:%s))?|%s)\s+of them leave this path\b"
    % ("|".join(_TENS), "|".join(_UNITS[1:10]), "|".join(_UNITS)), re.I)
ENV_ONLY_CLAIM = re.compile(
    r"\bother\s+(\d+|(?:%s)(?:[-\s](?:%s))?|%s)\s+scripts the table lists\b"
    % ("|".join(_TENS), "|".join(_UNITS[1:10]), "|".join(_UNITS)), re.I)

COMMITMENT = re.compile(r"\bcommitment\b", re.I)
WOULD = re.compile(r"\bwould\b", re.I)
QUESTION_BAN = re.compile(r"\bthe future\b|contains \"would\"|"
                          r"\bmight do later\b", re.I)
EXEMPTION = re.compile(r"\bexempt\w*\b|\bexcept\b", re.I)
# The shapes a guide states a question rule in: a table row, or a list item
# under any marker, with or without a checkbox. It was ("|", "- [") until a
# reviewer wrote the ban as a plain bullet -- "- Never ask what they would do
# in the future." -- which is the same rule one character shorter and was not
# read. A rule written as a running sentence is still not read, and that is a
# stated limit rather than an oversight: the mom-test worksheet opens by
# summarising its own rules in prose ("not opinions about the future"), and a
# check that read paragraphs would demand an exemption clause from a
# sentence that is describing the rules rather than stating one.
RULE_LINE = re.compile(r"^(?:\||[-*+]\s|\d+[.)]\s)")
GUIDE_DIRS = ("templates", "examples", "frameworks")

# Two editorial defects that every structural check in this tree walked past,
# because each one is well-formed: the heading parses, the path is spelled like
# a path. templates/discovery/discovery-synthesis.md carried "### Theme 1: [name
# the theme in the customers' terms]" twice in a row, so whoever filled the form
# saw two Theme 1 sections; templates/ai/eval-spec.md sent a reader to
# "../architecture/ai-interaction-spec.md" from inside an HTML comment, and the
# file it meant sits beside it in templates/ai/. Neither the link check above
# (five operator documents, markdown links only, comments included but nothing
# outside a link) nor the heading-order check (levels, not text) could see
# either one.
#
# A fenced block, so a heading-shaped line inside one is not read as a heading.
# CommonMark: three or more backticks or tildes, indented at most three spaces,
# closed by at least as many of the same character on a line of its own.
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*(.*)$")
# An explicit relative path reference: a token that begins "./" or "../" and
# ends in a suffix this tree actually commits. Written that way it is a claim
# about where this repository keeps a file, wherever it appears -- in a link
# target, in prose, or inside an HTML comment, which is where the eval-spec one
# hid. A bare "STATE.md" is not read: in these documents a name without a
# directory is usually the name of a form, not a path to one.
# The trailing lookaheads let a sentence end on a path -- "see ../x.md." is a
# reference and a full stop, not a reference to "x.md." -- while still refusing
# to cut a longer name in half: a dot followed by a letter or digit continues
# the token, so "../x.md.bak" matches nothing rather than matching "../x.md".
DECLARED_PATH = re.compile(
    r"(?<![\w./-])(\.{1,2}/[A-Za-z0-9._/-]*[A-Za-z0-9_-]"
    r"\.(?:md|py|json|ya?ml|toml|txt|sh))(?![A-Za-z0-9_/-])(?!\.[A-Za-z0-9])")
# Where a declared path is read. templates/ is the layer whose paths are a
# contract: a blank tells the person filling it which other file to open, and a
# wrong answer there is wrong in every copy made from it. This is a stated
# limit, not a claim that nothing else declares a path: examples/ carries
# inherited comments whose relative paths resolved from the template's
# directory and not from examples/, and those are left to the finding that owns
# the examples layer.
DECLARED_PATH_DIR = "templates"

# The examples inventory, which failed the same way the template inventory did:
# three of four journey counts were stale and summed to the stale total, so the
# arithmetic agreed with itself. A family is any examples/<family>-journey.md in
# the tree, and its artifacts are its other files less the two supplementary
# sheets. The rule is taken from the tree, not from a list kept here, because a
# list of files to leave out can be edited until it reproduces whatever the
# index already says. Only the index is read: CHANGELOG.md and the release notes
# carry the older figures as history, for the reason given above.
EXAMPLES_DIR = "examples"
EXAMPLES_INDEX = "examples/README.md"
JOURNEY = "-journey.md"
SUPPLEMENTARY = ("-coverage-sheet.md", "-design-sheet.md")
# "the artifact map for the 58 files below": how a section states its count.
# Numerals only, the limit the template inventory states.
SECTION_COUNT = re.compile(r"\b(\d+)\s+files\s+below\b")
# Any other "N files" in a family section restates that family's figure.
FILES_COUNT = re.compile(r"\b(\d+)\s+files\b")
EXAMPLES_TOTAL = re.compile(r"\b(\d+)\s+artifacts\s+in\s+all\b")
# "| [ledgerline-journey.md](ledgerline-journey.md) | 58 |": the summary table.
JOURNEY_ROW = re.compile(r"^\|\s*\[[^\]]*\]\(([^)\s]+" + re.escape(JOURNEY)
                         + r")\)\s*\|\s*(\d+)\s*\|")
# The lead sentence's counts of the sections that are not journeys, each held
# to the rows of the section named here, and its count of journeys, held to
# the tree. A figure written in words is not read, the limit stated above.
LEAD_COUNTS = (
    (re.compile(r"\b(\d+)\s+standalone\s+examples\b"), "Standalone examples"),
    (re.compile(r"\b(\d+)\s+single-file\s+industry\s+examples\b"),
     "Industry examples"),
)
JOURNEY_COUNT = re.compile(r"\b(\d+)\s+journeys\b")
# "the 38 artifacts added below the original 13": the original figure is the
# journey's own "## Artifact map", and the two with any "last N rows" figure
# have to add up to the family's count.
ADDED = re.compile(r"\b(\d+)\s+artifacts\s+added\s+below\s+the\s+original\s+"
                   r"(\d+)\b")
# "the last 7 rows" or "the last 7 Ledgerline rows": rows at the foot of a
# family's table that are outside its artifact map and cite neither its
# journey nor its sheets. The family is the word before "rows" when there is
# one, and otherwise the section's own.
LAST_ROWS = re.compile(r"\blast\s+(\d+)\s+(?:([A-Za-z][A-Za-z-]*)\s+)?rows\b")
ARTIFACT_MAP = "Artifact map"

# What a development-ready report does and does not certify, stated where a
# reader of the handoff section meets it. Three claims, each pinned as one
# exact sentence (compared with backticks dropped, case folded and whitespace
# collapsed) and checked on its own, so deleting one names the one deleted.
# A pin counts only where it stands as a sentence of its own: at the start of
# the section or after a ".", "!" or "?" and a space, so wording prefixed into
# the same sentence ("It is false that ...", "It is false: ...") does not
# satisfy it. And it counts only outside an HTML comment: the section,
# heading included, is found and read with every comment taken out (see
# COMMENT and _shown), so a pin inside one does not count. Other raw HTML is
# read as text, so a pin hidden some other way, in an attribute or in an
# element a browser does not display, still counts. That is a stated limit,
# checked by a reviewer.
# Exact, because a rule built from keywords passes a sentence that keeps the
# keywords and inverts the claim: "is no longer a condition of nothing" and
# "does not certify anything it cannot see, and every answer is evidenced"
# both carried every phrase an earlier version of this rule asked for.
# Rewording a pinned sentence therefore means editing it here too, in the
# same change, where a reviewer sees both.
QUICKSTART = "docs/RUNTIME-QUICKSTART.md"
QUICKSTART_READINESS = "## Development handoff"
READINESS_CLAIMS = (
    ("source verification is reported and is a condition of nothing",
     "whether an answer cites a workspace document, and whether a quotation it "
     "supplies was found there, is reported, as quote_verified, source_verified and "
     "supplied_unverified in pmos status --json at the top level and again per phase "
     "under completed, and under evidence in the handoff package and in "
     "handoff/context.md, and is a condition of nothing."),
    ("a development-ready report does not certify that every answer is evidenced",
     "it does not certify that every answer is evidenced: a product whose every "
     "answer is supplied_unverified can be development-ready."),
    ("a development-ready report does not certify that a typed actor id is authenticated",
     "it does not certify that a typed actor id is authenticated: pmos gate records "
     "the id it was given and stamps the approval a local attestation."),
)
# The same three facts in one line where README.md describes readiness.
README_READINESS = (
    "readiness is structural: how many answers cite a workspace document is reported "
    "by pmos status --json and is a condition of nothing, so a development-ready "
    "report does not certify that every answer is evidenced, nor that any typed "
    "actor id is authenticated.")
# Pinning the three sentences does not stop a fourth, added beside them, that
# says the opposite. These are the contradictions of those three claims this
# rule can recognise, checked sentence by sentence over the rest of the
# section as written, comments included, once the pinned sentences are taken
# out. It is a list, not an understanding of English: a contradiction worded
# some other way passes.
READINESS_CONTRADICTIONS = (
    (re.compile(r"\bevery answer is evidenced\b"),
     "says every answer is evidenced"),
    (re.compile(r"\b(?:is|are) authenticated\b"),
     "says an actor id is authenticated"),
    (re.compile(r"\bcondition of (?!nothing)|\bno longer a condition\b"),
     "makes source verification a condition of something"),
    (re.compile(r"\bmin_source_verified\b"),
     "describes a source-verification floor the runtime does not have"),
    (re.compile(r"\b(?:refuses?|blocks?|requires?)\b.*\b(?:source_verified|"
                r"supplied_unverified|unverified|evidenced)\b"),
     "makes readiness turn on how answers are evidenced"),
)
SENTENCE = re.compile(r"(?<=[.!?:;])\s+")
# An HTML comment, which a renderer does not show: "<!--" through the next
# "-->", or through the end of the file when none follows, as a comment that
# opens a line hides the rest of the document. This is not code-aware: a
# "<!--" in a code span or block is taken for a comment too, and the words
# after it for hidden. That errs one way only. Each comment is replaced by a
# mark (see _shown), so the text on either side of one is never joined, and
# reading too much as a comment can stop a pin counting but never make one
# count. A pin straight after a comment does not count either.
COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.S)


def _flat(text: str) -> str:
    return " ".join(text.replace("`", "").lower().split())


def _shown(text: str) -> str:
    """text with its HTML comments (see COMMENT) taken out, and nothing else.

    Each comment becomes a mark and the line breaks it held: the mark keeps
    the words on either side of it apart, and the line breaks keep every line
    at the number it has in the file, so a finding names its true line and the
    text as written can be read over the same lines.
    """
    return COMMENT.sub(lambda found: "\0" + "\n" * found.group(0).count("\n"), text)


def _as_sentence(sentence: str) -> "re.Pattern[str]":
    """A pinned sentence, matched only where it starts a sentence.

    Where it ends needs no check: every pin ends with its own full stop.
    """
    return re.compile(r"(?:^|(?<=[.!?] ))" + re.escape(sentence))


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    line: int
    message: str

    def as_dict(self):
        return {"severity": self.severity, "code": self.code, "path": self.path,
                "line": self.line, "message": self.message}


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _local_target(root: Path, source: Path, raw: str) -> bool:
    target = raw.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith("#") or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return True
    target = target.split("#", 1)[0]
    candidate = (source.parent / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    return candidate.exists()


def _template_blanks(root: Path) -> dict:
    """Every blank under templates/, keyed by the directory that holds it.

    templates/README.md is the catalog rather than a blank, so it is not
    counted; anything at the top level of templates/ is in the same position
    and is excluded the same way.
    """
    base = root / TEMPLATES_DIR
    grouped: dict = {}
    for path in sorted(base.rglob("*.md")):
        relative = path.relative_to(base)
        if len(relative.parts) < 2 or relative.name.startswith("._"):
            continue
        grouped.setdefault(relative.parts[0], set()).add(relative.as_posix())
    return grouped


def _catalog_sections(text: str) -> dict:
    """Each catalog section: its line, its declared count, its linked blanks.

    A link that climbs out of templates/ is context the section cites, not a
    row of the catalog, so only targets inside the directory are collected.
    """
    sections: dict = {}
    current = None
    for number, raw in enumerate(text.splitlines(), 1):
        match = CATALOG_SECTION.match(raw)
        if match:
            current = match.group(1)
            sections[current] = [number, int(match.group(2)), set()]
            continue
        if raw.startswith("## "):
            current = None
        if current is None:
            continue
        for link in LINK.finditer(raw):
            target = link.group(2).strip().split("#", 1)[0].strip("<>")
            if target.endswith(".md") and not target.startswith(("../", "/")) \
                    and "://" not in target:
                sections[current][2].add(target)
    return sections


def check_inventory(root: Path) -> list[Issue]:
    """The template count, taken from the tree and compared with what is said.

    Three readings, in order of how far a wrong number travels: the catalog's
    per-directory headings and link tables against the directories themselves,
    every other count in the catalog against the total, and the front-door
    inventory figures against the same total. A tree with no templates/ makes
    no inventory claim and is not checked; this file is run against fixture
    roots as well as this repository.

    What this does not read: a spelled-out number ("Eight directories"), and a
    figure that counts some subset of the templates rather than all of them.
    """
    issues: list[Issue] = []
    if not (root / TEMPLATES_DIR).is_dir():
        return issues
    grouped = _template_blanks(root)
    total = sum(len(names) for names in grouped.values())

    catalog = root / CATALOG
    if not catalog.is_file():
        issues.append(Issue("error", "missing-doc", CATALOG, 1,
                            "the template catalog is missing, so nothing "
                            "states the inventory it is the front door for"))
        return issues
    text = catalog.read_text(encoding="utf-8")
    sections = _catalog_sections(text)

    for name in sorted(set(grouped) - set(sections)):
        issues.append(Issue("error", "inventory-count", CATALOG, 1,
                            "templates/%s holds %d blank(s) and the catalog "
                            "has no section for it" % (name, len(grouped[name]))))
    for name in sorted(set(sections) - set(grouped)):
        issues.append(Issue("error", "inventory-count", CATALOG,
                            sections[name][0],
                            "the catalog has a section for templates/%s, which "
                            "holds no blanks" % name))
    for name in sorted(set(sections) & set(grouped)):
        line, declared, linked = sections[name]
        actual = grouped[name]
        if declared != len(actual):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "the %s section says %d template(s) and the "
                                "directory holds %d"
                                % (name, declared, len(actual))))
        for missing in sorted(actual - linked):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "templates/%s is in the tree and not in the "
                                "catalog" % missing))
        for absent in sorted(linked - actual):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "the catalog lists templates/%s, which is not "
                                "in the tree" % absent))

    for number, raw in enumerate(text.splitlines(), 1):
        if CATALOG_SECTION.match(raw):
            continue
        for match in COUNT.finditer(raw):
            if int(match.group(1)) != total:
                issues.append(Issue("error", "inventory-count", CATALOG, number,
                                    "the catalog says %r and templates/ holds "
                                    "%d blank(s)" % (match.group(0), total)))

    claims = 0
    for name in INVENTORY_DOCS:
        path = root / name
        if not path.is_file():
            continue
        document = path.read_text(encoding="utf-8")
        for match in INVENTORY.finditer(document):
            claims += 1
            if int(match.group(1)) != total:
                issues.append(Issue("error", "inventory-count", name,
                                    _line(document, match.start()),
                                    "this says %r and templates/ holds %d "
                                    "blank(s)" % (match.group(0), total)))
    if not claims:
        issues.append(Issue("error", "inventory-count", INVENTORY_DOCS[0], 1,
                            "no operator document states the template "
                            "inventory. One of %s has to carry it as \"all N "
                            "templates\" or \"all N blanks\", or the figure "
                            "the front door shows a reader is measured by "
                            "nobody" % ", ".join(INVENTORY_DOCS)))
    return issues


def _gate_total(root: Path):
    """How many gates tools/ci_gate.py defines, read from its GATES tuple.

    Parsed, not imported: importing runs the module, and this file is run
    against fixture roots that need not carry a working runtime. A tree with
    no ci_gate.py, or one whose GATES is not a literal tuple, returns None and
    makes no claim, rather than guessing a number the documents are then held
    to.
    """
    source = root / CI_GATE
    if not source.is_file():
        return None
    try:
        tree = ast.parse(source.read_text(encoding="utf-8"))
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (isinstance(target, ast.Name) and target.id == "GATES"
                    and isinstance(node.value, (ast.Tuple, ast.List))):
                return len(node.value.elts)
    return None


def _stated_count(figure: str) -> int:
    """A figure GATE_COUNT matched, "26", "twenty-six" or "Twenty Six", as a number."""
    if figure.isdigit():
        return int(figure)
    return sum(NUMBER_WORDS[word] for word in re.split(r"[-\s]+", figure.lower()))


def check_gate_count(root: Path) -> list[Issue]:
    """Gate counts stated beside ci_gate.py, against what that file defines.

    This exists because three documents carried three different numbers for
    one object, none of them the number the file held: the README said 24 and
    22, the FAQ said twenty-one, and tools/ci_gate.py defined 25. A figure a
    reader cannot check is a figure nothing re-measures when gates are added.

    A count is read in digits or in words up to ninety-nine, on any line that
    names ci_gate.py with or without its tools/ directory. A larger number
    written in words is not read.
    """
    issues: list[Issue] = []
    total = _gate_total(root)
    if total is None:
        return issues
    # The bare file name counts as naming it: docs/ARCHITECTURE.md's tree
    # diagram states the count on the line listing ci_gate.py under tools/,
    # where the full path never appears.
    named = Path(CI_GATE).name
    for name in GATE_COUNT_DOCS:
        path = root / name
        if not path.is_file():
            continue
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if named not in raw:
                continue
            for match in GATE_COUNT.finditer(raw):
                if _stated_count(match.group(1)) != total:
                    issues.append(Issue("error", "gate-count", name, number,
                                        "this says %r and %s defines %d"
                                        % (match.group(0), CI_GATE, total)))
    return issues


def _markdown(root: Path, base: Path):
    """Every markdown file under base, in a stable order, skipping the hidden.

    A path segment that starts with "." is tooling rather than documentation,
    and a name that starts with "._" is an exFAT resource fork: this tree is
    edited from a drive that writes them beside every file, and reading one as
    a document reports findings against a file nobody can see.
    """
    if not base.is_dir():
        return []
    out = []
    for path in sorted(base.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts) \
                or path.name.startswith("._"):
            continue
        out.append((path, relative.as_posix()))
    return out


def _headings(text: str):
    """(line number, level, text) for every heading, fenced blocks left out.

    The fence state is tracked rather than the fences removed, so a line keeps
    the number it has in the file and a finding names that number.

    An HTML comment is skipped for the same reason a fenced block is: this
    tree's templates are built out of guidance comments, and a comment that
    shows the filler what a repeated section looks like ("### Theme n: [name]",
    twice, inside one comment) is an example of a heading and not a heading.
    Nothing this tree ships puts a real heading inside a comment. The comment
    state is tracked line by line, so a comment that opens and closes on one
    line hides only that line.

    Both of CommonMark's heading spellings are read: ATX ("## Zed", with or
    without a closing "##") and setext (a line of text underlined by "=" or
    "-"). A reviewer repeated a heading in each of those two spellings and the
    reading, which took only bare ATX, saw one heading where the file had two.
    YAML front matter is skipped whole, because its closing "---" underlines
    the last line of the block and is not a heading.

    What the setext reading does not do: it takes the LAST line above the
    underline as the heading text, where CommonMark takes the whole paragraph,
    and it reads no underline whose line above is ambiguous (see
    NOT_SETEXT_TEXT). Both keep the widening from inventing a heading where the
    file has a table, a list or a thematic break.
    """
    lines = text.splitlines()
    out, fence, comment = [], None, False
    start = 1
    if lines and lines[0].strip() == "---":
        closing = next((number for number, raw in enumerate(lines[1:], 2)
                        if raw.strip() in ("---", "...")), None)
        start = (closing + 1) if closing else len(lines) + 1
    previous = None
    for number, raw in enumerate(lines, 1):
        if number < start:
            continue
        if comment:
            comment = "-->" not in raw
            previous = None
            continue
        if "<!--" in raw and "-->" not in raw.split("<!--", 1)[1]:
            comment = True
            previous = None
            continue
        found = FENCE.match(raw)
        if found:
            marker = found.group(1)
            if fence is None:
                fence = marker
            # A closing fence is the same character, at least as long, and
            # carries no info string; anything else opens nothing and closes
            # nothing while a fence is open.
            elif marker[0] == fence[0] and len(marker) >= len(fence) \
                    and not found.group(2).strip():
                fence = None
            previous = None
            continue
        if fence is not None:
            continue
        heading = HEADING.match(raw)
        if heading:
            out.append((number, len(heading.group(1)), heading.group(2)))
            previous = None
            continue
        underline = SETEXT.match(raw)
        if underline and previous is not None:
            level = 1 if underline.group(1)[0] == "=" else 2
            out.append((previous[0], level, previous[1]))
            previous = None
            continue
        stripped = raw.strip()
        previous = None if not stripped or NOT_SETEXT_TEXT.match(raw) \
            else (number, stripped)
    return out


def check_duplicate_headings(root: Path) -> list[Issue]:
    """A heading that repeats one of its own siblings, in any markdown file.

    Siblings, not the whole file: a changelog writes "### Fixed" under every
    release heading and each of those is a different section, while two of them
    under one release are one section written twice. The same shape covers a
    persona sheet that repeats "#### Snapshot" under each persona. What the
    rule cannot excuse is the defect it was written for, two "### Theme 1"
    headings with the same parent and nothing between them.

    Text is compared with its case and its runs of whitespace flattened, so
    "### Theme 1" and "###  theme 1" are the same heading. What this does not
    read: two sibling headings that differ by a word while naming the same
    thing, which is a reader's finding and not a checker's.
    """
    issues: list[Issue] = []
    for path, name in _markdown(root, root):
        seen: dict = {}
        stack: list = []
        for number, level, text in _headings(path.read_text(encoding="utf-8")):
            flat = " ".join(text.split()).lower()
            while stack and stack[-1][0] >= level:
                stack.pop()
            key = (tuple(parent for _, parent in stack), level, flat)
            first = seen.get(key)
            if first is None:
                seen[key] = number
            else:
                issues.append(Issue("error", "duplicate-heading", name, number,
                                    "%r repeats the heading of the same level "
                                    "and the same parent on line %d"
                                    % (text, first)))
            stack.append((level, flat))
    return issues


def check_declared_paths(root: Path) -> list[Issue]:
    """Every explicit relative path a template declares, against the tree.

    Read from the directory of the file that names it, which is the only way
    the defect shows: "../architecture/ai-interaction-spec.md" is a real path
    from templates/definition/ and a dead one from templates/ai/, where it was
    written. A reference that climbs out of the repository is reported for the
    same reason a missing one is: neither is a path a reader can follow here.

    What this does not read, each one a stated limit and not an oversight: a
    reference without a leading "./" or "../" (see DECLARED_PATH), so
    "architecture/nope.md" written as bare prose passes; a reference whose
    suffix is outside the committed list in DECLARED_PATH, so "../x.csv"
    passes; a reference containing a space, since the pattern stops at one and
    a sentence is not a path; a directory reference; and any file outside
    templates/ (see DECLARED_PATH_DIR). A reviewer walked each of the first
    three past this check deliberately, and a second reviewer walked all three
    past it again. Widening any of them trades a class of miss for a class of
    false positive across the 982 live references under templates/, which is a
    change that owes its own fixtures.

    What the other gate does and does not add, measured rather than assumed: a
    WELL-FORMED markdown link whose target is missing is caught by lint.py's
    LINK check, so "[a spec](./nope-xyz.md)" is reported there. The space form
    is not, and not because that check is weak: CommonMark does not read
    "[a spec](./My Missing Spec.md)" as a link at all, because an unbracketed
    destination cannot contain a space, so nothing renders it as one either.
    The spelling that IS a link, "[a spec](<./My Missing Spec.md>)", is read by
    lint.py and reported. An earlier version of this docstring said the LINK
    check caught the space form; it does not, and saying so claimed coverage
    this tree does not have.
    """
    issues: list[Issue] = []
    resolved = root.resolve()
    for path, name in _markdown(root, root / DECLARED_PATH_DIR):
        text = path.read_text(encoding="utf-8")
        for found in DECLARED_PATH.finditer(text):
            reference = found.group(1)
            target = (path.parent / reference).resolve()
            try:
                target.relative_to(resolved)
            except ValueError:
                issues.append(Issue("error", "declared-path", name,
                                    _line(text, found.start()),
                                    "%r leaves the repository" % reference))
                continue
            if not target.is_file():
                issues.append(Issue("error", "declared-path", name,
                                    _line(text, found.start()),
                                    "%r names no file in this tree" % reference))
    return issues


def check_script_count(root: Path) -> list[Issue]:
    """The number of scripts under tools/, stated in SECURITY.md's prose.

    The count is taken from tools/ and compared with what the file says, in
    digits or in words up to ninety-nine, the same way the gate count is read.

    It exists because the block above it was not enough. SECURITY.md said
    "`tools/` holds eighteen scripts in all" while the directory held 27; the
    sentence became a generated block between two markers, and a reviewer then
    re-typed the stale one into the prose a line ABOVE those markers, where the
    generator's own comparison does not look and every check stayed green. A
    count a reader cannot check is a count nothing re-measures, wherever on the
    page it sits.

    Only SECURITY.md is read, and only outside the generated markers: inside
    them, tools/exec_surface.py re-renders the text and check_executable_surface
    compares it. A tree with no tools/ makes no claim and is not checked.

    Two figures the prose derives from the generated table are read as well,
    because a stale exception list is the other half of the defect this file
    was fixed for: how many scripts leave the manual path, against the rows the
    table marks as naming a network primitive, and how many of the rest read an
    environment variable without leaving, against the rows marked that way.
    Both are matched on the sentence that states them, the way the gate count
    is matched on a line naming ci_gate.py, so rewording the sentence drops the
    reading rather than failing the build.

    What this does not read: a count of any other named subset of the scripts,
    such as this file's own "Six local scripts stay on this path"; a count of
    scripts in any other document; and a number written in words above
    ninety-nine.
    """
    issues: list[Issue] = []
    try:
        try:
            from tools import exec_surface
        except ImportError:
            import exec_surface  # type: ignore[no-redef]
    except ImportError:
        return [Issue("error", "script-count", SECURITY, 1,
                      "tools/exec_surface.py could not be imported, so the "
                      "script count in prose was not checked")]
    found = [exec_surface.facts(path) for path in exec_surface.scripts(root)]
    total = len(found)
    if not total:
        return issues
    leaving = sum(1 for _environment, network in found if network)
    environment_only = sum(1 for environment, network in found
                           if environment and not network)
    path = root / SECURITY
    if not path.is_file():
        return issues
    inside = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if exec_surface.BEGIN in raw:
            inside = True
            continue
        if exec_surface.END in raw:
            inside = False
            continue
        if inside:
            continue
        for match in SCRIPT_COUNT.finditer(raw):
            figure = match.group(1) or match.group(2)
            if _stated_count(figure) != total:
                issues.append(Issue("error", "script-count", SECURITY, number,
                                    "this says %r and tools/ holds %d script(s)"
                                    % (match.group(0), total)))
        for pattern, measured, what in (
                (LEAVE_CLAIM, leaving, "name a network primitive"),
                (ENV_ONLY_CLAIM, environment_only,
                 "name an environment variable and no network primitive")):
            for match in pattern.finditer(raw):
                if _stated_count(match.group(1)) != measured:
                    issues.append(Issue(
                        "error", "script-count", SECURITY, number,
                        "this says %r and %d script(s) under tools/ %s"
                        % (match.group(0), measured, what)))
    return issues


def check_commitment_probe_rule(root: Path) -> list[Issue]:
    """An interview guide whose question rule bans the question it also asks.

    Every markdown file under templates/, examples/ and frameworks/ is read.
    A file that carries a line naming a commitment in words that use "would"
    is taken to ask a closing commitment probe; in such a file, every table row
    and every list item -- under any bullet or number, with or without a
    checkbox -- that bans asking about the future, or bans a question
    containing "would", has to name the exemption, and one that does not is
    reported.

    It exists because an external audit found templates/discovery/
    interview-guide.md banning future questions on one line while requiring,
    two lines later, the Block E probe that asks the participant what they
    would do next. Correcting the template left the same contradiction in three
    further files: the template's own filled example, the mom-test framework
    worksheet, and that worksheet's filled example. Six lines in four files
    carried it and no structural check saw any of them, because every one of
    those lines parses and reads well on its own.

    What this does not read: a ban written as a running sentence rather than as
    a row or a list item (see RULE_LINE), because this tree's worksheets
    summarise their own rules in prose and a check that read paragraphs would
    demand an exemption clause from a sentence that is describing the rules;
    the rule is matched as text, so a ban worded some other way is not
    seen; a guide that asks the probe without any line naming
    a commitment is not read at all; a line naming a commitment for some other
    reason can make a file eligible, and the cost of that breadth is one more
    line that has to say "except the closing commitment probe"; and the check
    asks only whether the exemption is named, never whether the guide's
    questions obey it, which is a reader's finding and not a checker's.
    """
    issues: list[Issue] = []
    for directory in GUIDE_DIRS:
        for path, name in _markdown(root, root / directory):
            lines = path.read_text(encoding="utf-8").splitlines()
            probe = None
            for number, raw in enumerate(lines, 1):
                if COMMITMENT.search(raw) and WOULD.search(raw):
                    probe = number
            if probe is None:
                continue
            for number, raw in enumerate(lines, 1):
                if not RULE_LINE.match(raw.strip()):
                    continue
                if QUESTION_BAN.search(raw) and not EXEMPTION.search(raw):
                    issues.append(Issue(
                        "error", "commitment-probe", name, number,
                        "this rules out the question the closing commitment "
                        "probe asks, and names no exemption, while line %d of "
                        "the same file asks for a commitment in words that use "
                        "\"would\"" % probe))
    return issues


def check_executable_surface(root: Path) -> list[Issue]:
    """SECURITY.md's inventory of tools/, against what tools/ holds.

    The third count in this file that nothing measured, and the one with the
    longest reach: SECURITY.md told a reader how many scripts the tree runs and
    which of them leave the machine. It said eighteen while the directory held
    27, and it named one script as the only one that calls out while a second
    had grown a network call. The block is generated by tools/exec_surface.py;
    this check re-renders it from the tree and reports the committed copy when
    it differs, so the gate that already runs this file also fails on a stale
    or deleted inventory.

    What this does not read: what a script does with an environment variable or
    a socket, which is prose beside the block and a reviewer's finding. A tree
    with no tools/ makes no claim and is not checked.
    """
    try:
        try:
            from tools import exec_surface
        except ImportError:
            import exec_surface  # type: ignore[no-redef]
    except ImportError:
        return [Issue("error", "executable-surface", SECURITY, 1,
                      "tools/exec_surface.py could not be imported, so the "
                      "executable-surface inventory was not checked")]
    problem, _block = exec_surface.compare(root)
    if problem is None:
        return []
    return [Issue("error", "executable-surface", SECURITY, 1,
                  "%s. Run: python3 tools/exec_surface.py" % problem)]


def _example_families(names) -> dict:
    """Each journey family's artifacts, by the rule stated above.

    A file goes to the longest family prefix it carries, so a family whose name
    begins with another family's name does not have its files counted twice.
    """
    families = sorted((name[:-len(JOURNEY)] for name in names
                       if name.endswith(JOURNEY)), key=len, reverse=True)
    excluded = {family + suffix for family in families
                for suffix in (JOURNEY,) + SUPPLEMENTARY}
    members = {family: set() for family in families}
    for name in names:
        if name in excluded:
            continue
        for family in families:
            if name.startswith(family + "-"):
                members[family].add(name)
                break
    return members


def _index_sections(text: str) -> list:
    """Each heading's section: heading, line, count claims, rows, journeys.

    A row is a table line whose first cell links a file beside the index,
    which leaves out header rows and a row that only cites a template. Each
    row is kept as (line, file). The journeys are the ones the section's prose
    links, which is how a section says which family it indexes.
    """
    sections = []
    current = {"heading": "(top)", "line": 1, "claims": [], "rows": [],
               "journeys": set()}
    sections.append(current)
    for number, raw in enumerate(text.splitlines(), 1):
        heading = HEADING.match(raw)
        if heading:
            current = {"heading": heading.group(2), "line": number,
                       "claims": [], "rows": [], "journeys": set()}
            sections.append(current)
            continue
        for match in SECTION_COUNT.finditer(raw):
            current["claims"].append((number, int(match.group(1))))
        cells = raw.split("|")
        if raw.startswith("|") and len(cells) > 2:
            first = [link.group(2).strip() for link in LINK.finditer(cells[1])
                     if link.group(2).strip().endswith(".md")
                     and "/" not in link.group(2)]
            if first:
                current["rows"].append((number, first[0]))
        if not raw.startswith("|"):
            for link in LINK.finditer(raw):
                if link.group(2).endswith(JOURNEY):
                    current["journeys"].add(link.group(2)[:-len(JOURNEY)])
    return sections


def _artifact_map(base: Path, family: str) -> set:
    """The family's files linked from its journey's own "## Artifact map".

    The section runs from that H2 heading to the next H1 or H2, so a
    subheading inside it keeps its links, and a deeper "### Artifact map"
    elsewhere in the journey is not the map.
    """
    journey = base / (family + JOURNEY)
    found, inside = set(), False
    for raw in journey.read_text(encoding="utf-8").splitlines():
        heading = HEADING.match(raw)
        if heading:
            if len(heading.group(1)) <= 2:
                inside = len(heading.group(1)) == 2 and \
                    heading.group(2) == ARTIFACT_MAP
            continue
        if inside:
            for link in LINK.finditer(raw):
                target = link.group(2).strip().split("#", 1)[0]
                if target.startswith(family + "-"):
                    found.add(target)
    return found


def _cites_its_journey(base: Path, name: str, family: str) -> bool:
    text = (base / name).read_text(encoding="utf-8")
    return any(family + suffix in text for suffix in (JOURNEY,) + SUPPLEMENTARY)


def check_examples_inventory(root: Path) -> list[Issue]:
    """The examples index against examples/ itself.

    What is checked, all against the tree rather than against the index:
    - every file in the directory is linked from the index, and every link
      in the index resolves;
    - every "the N files below" equals the rows of its section's table;
    - a section whose prose links exactly one journey is that family's
      section: its rows have to be exactly that family's files, once each,
      and every "N files" in it has to equal the family's count from the tree;
    - every family has one summary-table row, and its figure equals the tree;
    - "N artifacts in all" equals the tree's total, and the lead sentence's
      standalone, industry and journey counts equal their sections' rows and
      the number of journeys;
    - "N artifacts added below the original M": M equals the family files the
      journey's own "## Artifact map" links, and N + M plus any "last K rows"
      figure equals the family's count;
    - "the last K rows" are K rows at the foot of the family's table that are
      outside its artifact map and cite neither its journey nor its sheets.
    Checking a figure against its own rows alone would pass forever on a file
    added with its row and a stale digit; the tree is the only reading that
    moves when the directory does. A figure written in words is not read, and
    neither is a subset figure such as "the last ten": both are stated limits,
    checked by a reader.
    """
    issues: list[Issue] = []
    base = root / EXAMPLES_DIR
    if not base.is_dir():
        return issues
    index = root / EXAMPLES_INDEX
    if not index.is_file():
        issues.append(Issue("error", "missing-doc", EXAMPLES_INDEX, 1,
                            "the examples index is missing, so nothing states "
                            "the inventory it is the front door for"))
        return issues
    names = {path.name for path in base.glob("*.md")
             if path.name != "README.md" and not path.name.startswith("._")}
    members = _example_families(names)
    families = {family: len(files) for family, files in members.items()}
    text = index.read_text(encoding="utf-8")
    lines = text.splitlines()

    def report(number, message):
        issues.append(Issue("error", "examples-inventory", EXAMPLES_INDEX,
                            number, message))

    linked = set()
    for match in LINK.finditer(text):
        target = match.group(2).strip().split("#", 1)[0].strip("<>")
        linked.add(target)
        if not _local_target(root, index, match.group(2)):
            issues.append(Issue("error", "broken-local-link", EXAMPLES_INDEX,
                                _line(text, match.start()),
                                "the index links %s, which does not resolve"
                                % match.group(2)))
    for name in sorted(names - linked):
        report(1, "examples/%s is in the tree and not in the index" % name)

    sections = _index_sections(text)
    by_heading = {section["heading"]: section for section in sections}
    stated, section_of = set(), {}
    for section in sections:
        heading, rows = section["heading"], section["rows"]
        for number, declared in section["claims"]:
            if declared != len(rows):
                report(number, "the %r section says %d file(s) and its table "
                       "has %d row(s)" % (heading, declared, len(rows)))
        journeys = section["journeys"]
        family = next(iter(journeys)) if len(journeys) == 1 else None
        if not section["claims"] or family not in families:
            continue
        stated.add(family)
        section_of[family] = section
        files = [name for _number, name in rows]
        for name in sorted(set(files) - members[family]):
            report(next(number for number, row in rows if row == name),
                   "the %s section lists %s, which is not a %s artifact"
                   % (family, name, family))
        for name in sorted(members[family] - set(files)):
            report(section["line"], "the %s section does not list %s"
                   % (family, name))
        for name in sorted({name for name in files if files.count(name) > 1}):
            report(section["line"], "the %s section lists %s more than once"
                   % (family, name))
        actual = families[family]
        end = rows[-1][0] if rows else section["claims"][-1][0]
        for number in range(section["line"], end + 1):
            for match in FILES_COUNT.finditer(lines[number - 1]):
                if int(match.group(1)) != actual:
                    report(number, "the %s section says %r and examples/ holds "
                           "%d %s artifact(s)" % (family, match.group(0),
                                                  actual, family))

    summarised = {}
    for number, raw in enumerate(lines, 1):
        row = JOURNEY_ROW.match(raw)
        if row and row.group(1)[:-len(JOURNEY)] in families:
            family = row.group(1)[:-len(JOURNEY)]
            summarised.setdefault(family, []).append(number)
            if int(row.group(2)) != families[family]:
                report(number, "the summary row for %s says %s and examples/ "
                       "holds %d" % (family, row.group(2), families[family]))
    for family in sorted(families):
        if len(summarised.get(family, ())) != 1:
            report(1, "the summary table has %d row(s) for %s and needs one"
                   % (len(summarised.get(family, ())), family))

    total = sum(families.values())
    totals = [(_line(text, match.start()), int(match.group(1)))
              for match in EXAMPLES_TOTAL.finditer(text)]
    for number, declared in totals:
        if declared != total:
            report(number, "the index says %d artifacts in all and examples/ "
                   "holds %d" % (declared, total))
    for pattern, heading in LEAD_COUNTS:
        for match in pattern.finditer(text):
            number = _line(text, match.start())
            section = by_heading.get(heading)
            if section is None:
                report(number, "the index says %r and has no %r section to "
                       "count" % (match.group(0), heading))
            elif int(match.group(1)) != len(section["rows"]):
                report(number, "the index says %r and the %r table has %d "
                       "row(s)" % (match.group(0), heading,
                                   len(section["rows"])))
    for match in JOURNEY_COUNT.finditer(text):
        if int(match.group(1)) != len(families):
            report(_line(text, match.start()), "the index says %r and "
                   "examples/ holds %d journey(s)" % (match.group(0),
                                                      len(families)))

    # "the last K rows", read wherever it is stated, then held to the table.
    last = {}
    for section in sections:
        start = section["line"]
        end = (sections[sections.index(section) + 1]["line"] - 1
               if section is not sections[-1] else len(lines))
        journeys = section["journeys"]
        own = next(iter(journeys)) if len(journeys) == 1 else None
        for number in range(start, end + 1):
            for match in LAST_ROWS.finditer(lines[number - 1]):
                named = (match.group(2) or "").lower() or own
                if named not in families:
                    report(number, "%r names no journey family"
                           % match.group(0))
                    continue
                last.setdefault(named, []).append((number, int(match.group(1))))
    for family, claims in sorted(last.items()):
        figures = {figure for _number, figure in claims}
        if len(figures) > 1:
            report(claims[0][0], "the index gives %s figures for the last "
                   "%s rows" % (sorted(figures), family))
            continue
        section = section_of.get(family)
        if section is None:
            continue
        mapped = _artifact_map(base, family)
        for number, figure in claims:
            tail = section["rows"][-figure:] if figure else []
            outside = [name for _row, name in tail
                       if name in members[family] and name not in mapped
                       and not _cites_its_journey(base, name, family)]
            # A figure above the row count needs no clause of its own: the
            # tail is then every row, so fewer than the figure are outside.
            if len(outside) != figure:
                report(number, "the index says the last %d %s rows are "
                       "outside the artifact map and cite neither the journey "
                       "nor its sheets, and %d of them are"
                       % (figure, family, len(outside)))
    for family, section in sorted(section_of.items()):
        end = section["rows"][-1][0] if section["rows"] else section["line"]
        mapped = None
        for number in range(section["line"], end + 1):
            for match in ADDED.finditer(lines[number - 1]):
                added, original = int(match.group(1)), int(match.group(2))
                mapped = _artifact_map(base, family) if mapped is None else mapped
                if original != len(mapped):
                    report(number, "the %s section says 'the original %d' and "
                           "its journey's artifact map lists %d"
                           % (family, original, len(mapped)))
                tail = next(iter({f for _n, f in last.get(family, [])}), 0)
                if added + original + tail != families[family]:
                    report(number, "the %s section's %d added, %d original "
                           "and %d last rows make %d, and examples/ holds %d"
                           % (family, added, original, tail,
                              added + original + tail, families[family]))

    # Removing a count is otherwise a way to make every clause above true,
    # the route the template inventory's own front-door check had to close.
    missing = sorted(set(families) - stated)
    if missing or (families and not totals):
        report(1, "no operator document states the examples inventory for %s. "
               "Its section has to say \"the N files below\" and the index "
               "\"N artifacts in all\", or the figure is measured by nobody"
               % (", ".join(missing) or "the journeys' total"))
    # Two figures on one line read the same way give one finding, not two.
    return list(dict.fromkeys(issues))


def _section(lines: list, heading: str):
    """Where a level-2 section lies in lines, up to the next one.

    The number of its heading line, which is also the index of the line after
    it, and the index of the next line that starts with "## ", or len(lines);
    (0, 0) when no line is the heading.
    """
    for index, raw in enumerate(lines):
        if raw.strip() == heading:
            end = next((later for later in range(index + 1, len(lines))
                        if lines[later].startswith("## ")), len(lines))
            return index + 1, end
    return 0, 0


def check_readiness_claims(root: Path) -> list[Issue]:
    """The three statements of what readiness leaves uncertified, and README's mirror.

    A tree with no quickstart makes no claim and is not checked, the same
    posture the inventory and gate-count checks take toward fixture roots.
    A quickstart that has lost the handoff section fails every claim, since
    moving the heading is otherwise a way to drop all three at once. The
    section and its pins are looked for with the comments taken out (see
    _shown), so a heading or a pin inside a comment does not count, and the
    contradictions over the same lines as written. README.md's mirror is
    looked for with its comments taken out the same way.
    """
    path = root / QUICKSTART
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    written, shown = text.split("\n"), _shown(text).split("\n")
    line, end = _section(shown, QUICKSTART_READINESS)
    flat = _flat("\n".join(written[line:end]))
    visible = _flat("\n".join(shown[line:end]))
    issues: list[Issue] = []
    spans = []
    for name, sentence in READINESS_CLAIMS:
        pinned = _as_sentence(sentence)
        found = pinned.search(flat)
        if found:
            spans.append(found.span())
        if pinned.search(visible):
            continue
        issues.append(Issue("error", "readiness-claim", QUICKSTART, line or 1,
                            "the %r section no longer says that %s (pinned in "
                            "tools/docs_contract.py as: %r)"
                            % (QUICKSTART_READINESS[3:], name, sentence)))
    rest, cursor = [], 0
    for begin, end in sorted(spans):
        rest.append(flat[cursor:begin])
        cursor = end
    rest.append(flat[cursor:])
    for sentence in SENTENCE.split(" ".join(rest)):
        for pattern, what in READINESS_CONTRADICTIONS:
            if pattern.search(sentence):
                issues.append(Issue("error", "readiness-contradiction", QUICKSTART,
                                    line or 1,
                                    "the %r section %s: %r"
                                    % (QUICKSTART_READINESS[3:], what, sentence)))
    readme = root / "README.md"
    if readme.is_file() and not _as_sentence(README_READINESS).search(
            _flat(_shown(readme.read_text(encoding="utf-8")))):
        issues.append(Issue("error", "readiness-claim", "README.md", 1,
                            "README.md no longer mirrors the quickstart's readiness "
                            "limits (pinned in tools/docs_contract.py as: %r)"
                            % README_READINESS))
    return issues


# --- The roadmap commitment contract --------------------------------------
# A roadmap row used to be a line of prose: no stable id, no accountable owner,
# and nothing that tied a Now row to the capacity it spends or the decision that
# chose it. The skill that drives the template asks for the 80 percent capacity
# line, quarterly entry and exit gates and a defence page, and the template had
# no field for any of them, so a filled roadmap could not retain the decisions
# its own skill requires. These checks read the roadmap the way a reviewer does:
# every committed row resolves to one owner, one outcome, one capacity
# reservation and dependencies somebody is governing, and a roadmap that
# reserves more than the plannable figure is over capacity whatever it claims.
#
# The independent review of 2026-09-23 refused the first version of these
# checks for reading one spelling of the document: a second Now table written
# without leading pipes, and a second "## NOW" heading, both of which GitHub
# renders exactly like the spellings the parser did read, parked an ownerless
# committed row where nothing looked. So the rule here is the reader's rule:
# whatever GFM renders as a horizon table, under whatever renders as a Now
# heading, is a row this check reads - pipes or no pipes, any case, any
# heading level, hashed or underlined, emphasis or none. Where the two could
# still disagree, the check refuses rather than reads on: a raw HTML table in
# a section it parses is reported, not ignored.
#
# Scope: every document in the tree that carries the roadmap title, or the Now
# and initiative records sections a roadmap from this template carries, wherever
# it sits. tests/ is skipped, and only tests/: it holds the counterexample
# fixtures these checks are tested against, and a roadmap that ships is not in
# the test tree. products/ and learn/products/ are a user's own workspace, which
# no gate in this repository judges.
# The title a roadmap made from this template carries, in any case and
# through emphasis marks. The colon has to follow the word: "# Roadmap
# Builder: ..." is the skill that writes roadmaps, not a roadmap.
ROADMAP_TITLE = re.compile(r"^#\s+[*_`]{0,3}\s*Roadmap\b\s*:\s*\S", re.M | re.I)
ROADMAP_SKIP = ("tests", "products", ".git", "__pycache__", ".venv",
                "node_modules", ".pytest_cache")
# "R-1", "BL-01", "EXP-2", "DEP4". A letter, then letters or digits, then a
# number, with the hyphen optional because both spellings are already in use in
# this tree's own worked examples.
IDENTIFIER = re.compile(r"^[A-Z][A-Z0-9]*-?\d{1,4}$")
# Which section carries what. Each is (heading pattern, human name).
# Which section carries what. A name, not a heading pattern: the heading is
# matched on its rendered text, so "## NOW", "## **Now**" and a setext "Now"
# underlined with dashes are the same section as "## Now". A roadmap must still
# carry each one as a level-2 heading; the rows under every other spelling are
# read too, because an unread row is a row anyone can park.
ROADMAP_SECTIONS = ("Now", "Next", "Initiative records", "Capacity line",
                    "Dependency index", "Quarterly gates", "Defence page")
REQUIRED_SECTION_LEVEL = 2
# Column groups every Now and Next table must carry, checked per table rather
# than once per section: a second table under the heading that drops the id
# column would otherwise be a place to park a row the check cannot read.
ROADMAP_COLUMNS = (
    ("id", ("id",)),
    ("owner", ("owner",)),
    ("outcome", ("outcome",)),
    ("target period", ("period",)),
    ("confidence", ("confidence",)),
    ("dependencies", ("dependenc",)),
    ("status", ("status",)),
)
# The fields one initiative record carries. The key is the label lowercased and
# cut at the first bracket, so "Outcome (objective ref)" keys as "outcome".
RECORD_FIELDS = ("id", "owner", "outcome", "strategy or okr ref",
                 "evidence ref", "appetite", "dependency ids", "score sheet",
                 "capacity reservation", "commitment type", "entry rule",
                 "exit rule", "rejected options and override decision")
RECORD_LINE = re.compile(r"^\s*[-*]\s+\*\*(?P<label>[^*]+?)\s*:\s*\*\*\s*(?P<value>.*?)\s*$")
# "40 person-days on extraction squad, reserved in [capacity plan](capacity-plan.md)".
RESERVATION = re.compile(
    r"^(?P<size>\d+(?:\.\d+)?)\s+(?P<unit>[A-Za-z][A-Za-z-]*)\s+on\s+"
    r"(?P<team>[^,]+?)\s*,\s*reserved\s+in\s+\[[^\]]+\]\([^)\s]+\)$", re.I)
DEFENCE_HEADINGS = ("### Highest-scored items not funded",
                    "### Funded despite a lower score",
                    "### What would change this sequence")
# "DEP-1", "DEP4": the ids a dependency index governs, picked out of a cell
# that is otherwise free prose in every shipped roadmap in this tree.
DEPENDENCY_TOKEN = re.compile(r"\bDEP[A-Z0-9]*-?\d{1,4}\b")
EMPHASIS_EDGE = re.compile(r"^[*_]{1,3}|[*_]{1,3}$")
MD_LINK_TEXT = re.compile(r"\[([^\]]*)\]\([^)\s]*\)")
BRACKET_ONLY = re.compile(r"^(?:\[[^\]]*\]|<[^>]*>)$")
BLANK_ANSWERS = frozenset({"", "-", "--", "?", "??", "n/a", "na", "tbd", "todo",
                           "none yet", "unknown"})
TABLE_SEPARATOR = re.compile(r"^\|?[\s:|-]+\|?$")
# A raw HTML table renders to a reader and is not a markdown table, so no
# check below reads a row written inside one.
HTML_TABLE = re.compile(r"<table\b", re.I)
TABLE_SECTIONS = ("Now", "Next", "Capacity line", "Dependency index",
                  "Quarterly gates")
# Where GFM ends a table: a heading, a quote, a list item or a fence.
BLOCK_START = re.compile(r"^(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s|```|~~~)")


# A pipe inside a cell is written "\\|" and renders as a pipe. Splitting on it
# would put the check's columns out of step with the reader's, which is a way
# to show an empty Owner and have this check read the cell beside it.
CELL_SPLIT = re.compile(r"(?<!\\)\|")


def _roadmap_cells(line: str) -> list:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if CELL_SPLIT.search(text) and text.endswith("|"):
        text = text[:-1]
    return [cell.strip().replace("\\|", "|") for cell in CELL_SPLIT.split(text)]


def _is_table_delimiter(line: str) -> bool:
    text = line.strip()
    return bool("|" in text and "-" in text and TABLE_SEPARATOR.match(text))


def _is_table_row(line: str) -> bool:
    """A body row: a pipe, and not the start of some other block.

    The pipe is what a multi-column row cannot be written without, in either
    spelling; the block starts are where GFM itself ends the table.
    """
    text = line.strip()
    return bool(text and "|" in text and not BLOCK_START.match(text))


def _roadmap_tables(lines: list, start: int, end: int):
    """Yield (header_cells, [(line_no, cells)]) for EVERY table in a span.

    Every table, because a section can hold more than one and a check that
    reads the first is a check anyone can walk around by adding a second. The
    walk continues to the end of the span after a table finishes, so a blank
    line between two tables, or prose between them, hides nothing.

    A table is recognised by its DELIMITER row, not by a leading pipe on the
    header. GFM makes the leading and trailing pipe optional, so

        ID | Theme | Owner
        --- | --- | ---
        F-7 | Shadow |

    renders as a table to every reader, and a parser that requires the pipe
    reads nothing there at all: not a malformed table, no table. The delimiter
    must carry a pipe, which is what separates it from a thematic break or a
    frontmatter fence. A header and a delimiter whose cell counts disagree are
    read as a table anyway: GFM renders those lines as a paragraph rather than
    a table, and a committed row nobody reads is the whole of this finding.
    """
    index = start
    while index < end:
        header = lines[index].strip()
        delimiter = lines[index + 1].strip() if index + 1 < end else ""
        if header and not header.startswith("#") and _is_table_delimiter(delimiter):
            header_cells = _roadmap_cells(header)
            rows, cursor = [], index + 2
            while cursor < end and _is_table_row(lines[cursor]):
                rows.append((cursor + 1, _roadmap_cells(lines[cursor])))
                cursor += 1
            yield header_cells, rows
            index = cursor
            continue
        index += 1


def _heading_text(text: str) -> str:
    """A heading as a reader sees it: links flattened, emphasis marks dropped."""
    return re.sub(r"[*_`]", "", MD_LINK_TEXT.sub(r"\1", text)).strip()


def _heading_lines(lines: list) -> list:
    """(index, level, rendered text, first content line) for every heading.

    Setext headings are here because "NOW (continued)" underlined with dashes
    renders as an h2 exactly like "## NOW (continued)" does, and a scanner that
    reads one spelling is a scanner anyone can walk around with the other.
    """
    heads = []
    index = 0
    while index < len(lines):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.*?)\s*$", lines[index])
        if match:
            heads.append((index, len(match.group(1)),
                          _heading_text(re.sub(r"\s+#+$", "", match.group(2))),
                          index + 1))
            index += 1
            continue
        text = lines[index].strip()
        under = (re.match(r"^ {0,3}(=+|-+)\s*$", lines[index + 1])
                 if index + 1 < len(lines) else None)
        if (under and re.search(r"\w", text) and "|" not in text
                and not BLOCK_START.match(text)):
            heads.append((index, 1 if under.group(1)[0] == "=" else 2,
                          _heading_text(text), index + 2))
            index += 2
            continue
        index += 1
    return heads


def _roadmap_spans(lines: list) -> dict:
    """{heading line: (first content line, line the next same-or-higher heading starts)}."""
    heads = _heading_lines(lines)
    spans = {}
    for position, (index, level, _text, start) in enumerate(heads):
        end = len(lines)
        for later, later_level, _later_text, _later_start in heads[position + 1:]:
            if later_level <= level:
                end = later
                break
        spans[index] = (start, end)
    return spans


def _roadmap_sections(lines: list, section: str, level=None) -> list:
    """Every span whose heading names this section, in any case, at any level.

    Every one, because a document with two "## Now" headings is the same bypass
    as a section with two tables: reading one of them is an invitation to put
    the row that would fail under the other. In any case and at any level for
    the same reason one step out - "## NOW (continued)" and "#### Now
    (continued)" render as headings a reader reads as Now, so rows under them
    are rows this check has to read. A span wholly inside another span of the
    same name is dropped, so a repeat nested under its own section is read once
    rather than counted twice.
    """
    spans = _roadmap_spans(lines)
    wanted = re.compile(r"%s\b" % re.escape(section), re.I)
    found = []
    for index, heading_level, text, _start in _heading_lines(lines):
        if level is not None and heading_level != level:
            continue
        if wanted.match(text):
            found.append(spans[index])
    kept = []
    for span in sorted(found):
        if any(span[0] >= outer[0] and span[1] <= outer[1] for outer in kept):
            continue
        kept.append(span)
    return kept


# HTML comments are blanked line for line before any of this is read. The
# guidance in a template is written in them, and a heading or a table row that
# only exists inside one is not in the document a reader sees.
COMMENT_BLOCK = re.compile(r"<!--.*?(?:-->|\Z)", re.S)


FRONTMATTER = re.compile(r"\A---\n.*?\n---(?=\n|\Z)", re.S)


def _roadmap_lines(text: str) -> list:
    blanked = COMMENT_BLOCK.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    # YAML frontmatter is not a paragraph, and its closing fence is not the
    # underline of a setext heading; blanked in place so line numbers hold.
    blanked = FRONTMATTER.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), blanked)
    return blanked.split("\n")


def _bare(cell: str) -> str:
    """The cell with only its outermost emphasis marks removed.

    Edge-anchored, so a link target that contains an underscore survives; the
    reservation grammar below is matched against this rather than against the
    link-flattened text, because the link is part of what it requires.
    """
    return EMPHASIS_EDGE.sub("", EMPHASIS_EDGE.sub("", cell.strip())).strip()


def _plain(cell: str) -> str:
    return MD_LINK_TEXT.sub(r"\1", _bare(cell)).strip()


def _blank_cell(cell: str) -> bool:
    if BRACKET_ONLY.match(_bare(cell)):
        return True
    return _plain(cell).lower() in BLANK_ANSWERS


def _blank_row(cells: list) -> bool:
    return all(_blank_cell(cell) for cell in cells)


def _roadmap_all_tables(lines: list, spans):
    """Every table in every span that carries the heading."""
    for span in spans or ():
        for table in _roadmap_tables(lines, *span):
            yield table


def _roadmap_records(lines: list, spans) -> list:
    """Return one dict per initiative record in the records sections.

    A record opens on its ID field and runs until the next ID field or the next
    heading, so records are read whether they are separated by a blank line, a
    paragraph or a sub-heading.
    """
    records, current = [], None
    for span in spans or ():
        current = None
        for index in range(span[0], span[1]):
            line = lines[index]
            if line.startswith("#"):
                current = None
                continue
            match = RECORD_LINE.match(line)
            if not match:
                continue
            key = match.group("label").split("(")[0].strip().lower()
            if key == "id":
                current = {"line": index + 1, "fields": {}}
                records.append(current)
            if current is None:
                continue
            current["fields"].setdefault(key, (index + 1, match.group("value")))
    return records


def _number(cell: str):
    text = _plain(cell).replace(",", "")
    match = re.match(r"^(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


def check_roadmap(name: str, text: str) -> list:
    """The commitment contract for one roadmap document."""
    issues: list[Issue] = []
    lines = _roadmap_lines(text)
    spans = {}
    for label in ROADMAP_SECTIONS:
        spans[label] = _roadmap_sections(lines, label)
        if not _roadmap_sections(lines, label, level=REQUIRED_SECTION_LEVEL):
            issues.append(Issue("error", "roadmap-section", name, 1,
                                "a roadmap needs a '%s' section" % label))
    # Scoped to the defence page's own span. Searched across the document,
    # these three satisfy the check from anywhere - from under "Parked and
    # killed", say - which is a defence page nobody wrote.
    defence = "\n".join(line for span in spans.get("Defence page") or ()
                        for line in lines[span[0]:span[1]])
    for heading in DEFENCE_HEADINGS:
        if not re.search(r"^%s\s*$" % re.escape(heading), defence, re.M):
            issues.append(Issue("error", "roadmap-defence", name, 1,
                                "the defence page needs '%s'" % heading))

    for label in TABLE_SECTIONS:
        for span in spans.get(label) or ():
            for index in range(span[0], span[1]):
                if HTML_TABLE.search(lines[index]):
                    issues.append(Issue("error", "roadmap-html-table", name, index + 1,
                                        "the %s section holds an HTML table at line %d: "
                                        "this check reads markdown tables, so nothing "
                                        "reads that one" % (label, index + 1)))

    # Horizon tables: the columns, then the rows.
    horizon_rows = {"Now": [], "Next": []}
    for label in ("Now", "Next"):
        for header, rows in _roadmap_all_tables(lines, spans.get(label)):
            lowered = [cell.lower() for cell in header]
            column = {}
            for name_of, words in ROADMAP_COLUMNS:
                found = None
                for position, cell in enumerate(lowered):
                    if name_of == "id":
                        if cell == "id":
                            found = position
                            break
                        continue
                    if any(word in cell for word in words):
                        found = position
                        break
                if found is None:
                    issues.append(Issue(
                        "error", "roadmap-columns", name, rows[0][0] - 2 if rows else 1,
                        "the %s table needs a '%s' column" % (label, name_of)))
                else:
                    column[name_of] = found
            for line_no, cells in rows:
                if _blank_row(cells):
                    continue
                horizon_rows[label].append((line_no, cells, column))

    # Dependency ids somebody is governing.
    governed = set()
    for _header, rows in _roadmap_all_tables(lines, spans.get("Dependency index")):
        for _line_no, cells in rows:
            if cells and not _blank_row(cells):
                governed.add(_plain(cells[0]).upper())

    # The quarterly gates, by period.
    gates = {}
    for _header, rows in _roadmap_all_tables(lines, spans.get("Quarterly gates")):
        for line_no, cells in rows:
            if _blank_row(cells) or len(cells) < 3:
                continue
            period = _plain(cells[0]).lower()
            if period in gates:
                issues.append(Issue("error", "roadmap-quarterly-gate", name, line_no,
                                    "the '%s' period has more than one gate row" % period))
                continue
            gates[period] = (line_no, cells)

    records = _roadmap_records(lines, spans.get("Initiative records"))
    by_id = {}
    for record in records:
        field = record["fields"].get("id")
        if field is None or _blank_cell(field[1]):
            continue
        key = _plain(field[1]).upper()
        if key in by_id:
            issues.append(Issue("error", "roadmap-record-duplicate", name,
                                record["line"],
                                "initiative %s has more than one record" % key))
            continue
        by_id[key] = record

    reservations = []
    for label in ("Now", "Next"):
        for line_no, cells, column in horizon_rows[label]:
            def cell_at(which):
                position = column.get(which)
                return cells[position] if position is not None and position < len(cells) else ""
            identifier = _plain(cell_at("id")).upper()
            if not IDENTIFIER.match(identifier):
                issues.append(Issue("error", "roadmap-initiative-id", name, line_no,
                                    "a %s row needs a stable initiative id" % label))
                continue
            owner = _plain(cell_at("owner"))
            if _blank_cell(cell_at("owner")):
                issues.append(Issue("error", "roadmap-owner", name, line_no,
                                    "%s names no accountable owner" % identifier))
            elif re.search(r",|;|/| and |&|\+", owner):
                issues.append(Issue("error", "roadmap-owner", name, line_no,
                                    "%s names more than one owner: accountability "
                                    "splits and nobody carries it" % identifier))
            if label != "Now":
                continue
            if _blank_cell(cell_at("outcome")):
                issues.append(Issue("error", "roadmap-outcome", name, line_no,
                                    "%s names no outcome" % identifier))
            record = by_id.get(identifier)
            if record is None:
                issues.append(Issue("error", "roadmap-record-missing", name, line_no,
                                    "%s is committed in Now with no initiative record"
                                    % identifier))
                continue
            fields = record["fields"]
            for key in RECORD_FIELDS:
                entry = fields.get(key)
                if entry is None:
                    issues.append(Issue("error", "roadmap-record-field", name,
                                        record["line"],
                                        "%s's record has no '%s' field" % (identifier, key)))
                elif _blank_cell(entry[1]):
                    issues.append(Issue("error", "roadmap-record-field", name, entry[0],
                                        "%s's '%s' is unfilled" % (identifier, key)))
            record_owner = _plain(fields.get("owner", (0, ""))[1])
            if record_owner and owner and record_owner != owner:
                issues.append(Issue("error", "roadmap-owner-mismatch", name, record["line"],
                                    "%s is owned by %s in Now and %s in its record"
                                    % (identifier, owner, record_owner)))
            commitment = _plain(fields.get("commitment type", (0, ""))[1]).lower()
            if commitment != "committed":
                issues.append(Issue("error", "roadmap-commitment-type", name, record["line"],
                                    "%s sits in Now, so its commitment type is "
                                    "'committed', not '%s'" % (identifier, commitment or "unset")))
            raw = _plain(fields.get("dependency ids", (0, ""))[1])
            if raw and raw.lower() not in {"none", "none.", "no dependencies"}:
                for token in re.split(r"[,;]\s*", raw):
                    token = token.strip().rstrip(".").upper()
                    if not token:
                        continue
                    if not IDENTIFIER.match(token):
                        issues.append(Issue("error", "roadmap-dependency-record", name,
                                            record["line"],
                                            "%s cites '%s', which is not a dependency id"
                                            % (identifier, token)))
                    elif token not in governed:
                        issues.append(Issue("error", "roadmap-dependency-record", name,
                                            record["line"],
                                            "%s depends on %s, which has no row in the "
                                            "dependency index" % (identifier, token)))
            # The table is what a reader sees; the record is what this check
            # reads. A row that publishes DEP-404 while its record says none is
            # two documents in one file.
            published = set(DEPENDENCY_TOKEN.findall(
                _plain(cell_at("dependencies")).upper()))
            recorded = set(DEPENDENCY_TOKEN.findall(raw.upper()))
            if published != recorded:
                issues.append(Issue("error", "roadmap-dependency-mismatch", name, line_no,
                                    "%s publishes %s in Now and %s in its record: the "
                                    "table a reader sees and the record disagree"
                                    % (identifier, _id_list(published), _id_list(recorded))))
            entry = fields.get("capacity reservation")
            booking = RESERVATION.match(_bare(entry[1])) if entry else None
            if entry is not None and not _blank_cell(entry[1]) and booking is None:
                issues.append(Issue("error", "roadmap-capacity-reservation", name, entry[0],
                                    "%s's capacity reservation must read '<n> <unit> on "
                                    "<team>, reserved in [capacity plan](<link>)'" % identifier))
            elif booking is not None:
                reservations.append((identifier, record["line"], float(booking.group("size")),
                                     booking.group("unit").lower(),
                                     booking.group("team").strip().lower()))
            # The decision that chose this over what it beat has to be a link,
            # not a sentence: "we considered the alternatives" is what every
            # roadmap says, and it is the one field a reviewer follows.
            decision = fields.get("rejected options and override decision")
            if (decision is not None and not _blank_cell(decision[1])
                    and not MD_LINK_TEXT.search(_bare(decision[1]))):
                issues.append(Issue("error", "roadmap-decision-link", name, decision[0],
                                    "%s's rejected options and override decision names "
                                    "no decision record to follow" % identifier))
            period = _plain(cell_at("target period")).lower()
            if _blank_cell(cell_at("target period")):
                # Without this an empty cell short-circuits both gate checks,
                # so the row no gate governs is the row that says nothing.
                issues.append(Issue("error", "roadmap-quarterly-gate", name, line_no,
                                    "%s names no target period, so no entry and exit "
                                    "gate governs it" % identifier))
            elif period not in gates:
                issues.append(Issue("error", "roadmap-quarterly-gate", name, line_no,
                                    "%s targets '%s', which has no entry and exit gate"
                                    % (identifier, period)))
            elif period:
                gate_line, gate_cells = gates[period]
                for position, what in ((1, "entry gate"), (2, "exit gate")):
                    if position >= len(gate_cells) or _blank_cell(gate_cells[position]):
                        issues.append(Issue("error", "roadmap-quarterly-gate", name, gate_line,
                                            "the '%s' period has no %s" % (period, what)))

    # The capacity line: what Now reserved, against what the teams can carry.
    booked = {}
    for identifier, line_no, size, unit, team in reservations:
        total, units, lines_seen = booked.setdefault(team, [0.0, set(), []])
        booked[team] = [total + size, units | {unit}, lines_seen + [(identifier, line_no)]]
    plannable = {}
    for _header, rows in _roadmap_all_tables(lines, spans.get("Capacity line")):
        for line_no, cells in rows:
            if _blank_row(cells) or len(cells) < 5:
                continue
            team = _plain(cells[0]).lower()
            if team in plannable:
                issues.append(Issue("error", "roadmap-capacity-team", name, line_no,
                                    "team '%s' has more than one capacity line row"
                                    % team))
                continue
            plannable[team] = (line_no, _number(cells[2]),
                               _plain(cells[3]).lower(), _number(cells[4]))
    for team, (total, units, seen) in sorted(booked.items()):
        if team not in plannable:
            issues.append(Issue("error", "roadmap-capacity-team", name, seen[0][1],
                                "%s reserves capacity on '%s', which has no capacity "
                                "line row" % (seen[0][0], team)))
            continue
        line_no, ceiling, unit, declared = plannable[team]
        if len(units) > 1 or (unit and units and unit not in units):
            issues.append(Issue("error", "roadmap-capacity-unit", name, line_no,
                                "'%s' reserves in %s and its capacity line is in %s"
                                % (team, ", ".join(sorted(units)), unit or "no unit")))
        if declared is None or abs(declared - total) > 1e-9:
            issues.append(Issue("error", "roadmap-capacity-total", name, line_no,
                                "'%s' declares %s reserved by Now and its records reserve %s"
                                % (team, "nothing" if declared is None else _trim(declared),
                                   _trim(total))))
        if ceiling is None:
            issues.append(Issue("error", "roadmap-capacity-total", name, line_no,
                                "'%s' states no plannable figure" % team))
        elif total > ceiling:
            issues.append(Issue("error", "roadmap-over-capacity", name, line_no,
                                "'%s' commits %s against a plannable %s: Now is over "
                                "capacity and an initiative moves to Next"
                                % (team, _trim(total), _trim(ceiling))))
    # A capacity row can also declare a reservation no record made. Without
    # this the arithmetic is only checked from the records inward, and a
    # capacity line could carry any figure at all for a team Now never booked.
    for team, (line_no, _ceiling, _unit, declared) in sorted(plannable.items()):
        if team not in booked and declared:
            issues.append(Issue("error", "roadmap-capacity-total", name, line_no,
                                "'%s' declares %s reserved by Now and no record "
                                "reserves anything on it" % (team, _trim(declared))))
    return issues


def _id_list(ids) -> str:
    return ", ".join(sorted(ids)) if ids else "nothing"


def _trim(value: float) -> str:
    return ("%f" % value).rstrip("0").rstrip(".")


def is_roadmap(text: str) -> bool:
    """A roadmap by its title, or by the sections only a roadmap carries.

    Discovery on the title alone is discovery a retitled copy walks out of:
    "# Product roadmap for X" is the same document with the same commitments.
    A document that carries both a Now section and an initiative records
    section is that document whatever its first line says.
    """
    if ROADMAP_TITLE.search(text):
        return True
    lines = _roadmap_lines(text)
    return bool(_roadmap_sections(lines, "Initiative records",
                                  level=REQUIRED_SECTION_LEVEL)
                and _roadmap_sections(lines, "Now", level=REQUIRED_SECTION_LEVEL))


def roadmap_documents(root: Path) -> list:
    """Every shipped document this tree governs as a roadmap."""
    found = []
    # Both spellings of the extension a markdown document is written with.
    for path in sorted(list(root.rglob("*.md")) + list(root.rglob("*.markdown"))):
        parts = set(path.relative_to(root).parts[:-1])
        if parts & set(ROADMAP_SKIP):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if is_roadmap(text):
            found.append((path.relative_to(root).as_posix(), text))
    return found


def check_roadmaps(root: Path) -> list:
    issues: list[Issue] = []
    for name, text in roadmap_documents(root):
        issues.extend(check_roadmap(name, text))
    return issues


def check(root: Path) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    lowered = {}
    for name in KEY_DOCS:
        path = root / name
        if not path.exists():
            issues.append(Issue("error", "missing-doc", name, 1,
                                "required operator document is missing"))
            continue
        text = path.read_text(encoding="utf-8")
        lowered[name] = text.lower()
        previous = 0
        for number, raw in enumerate(text.splitlines(), 1):
            heading = HEADING.match(raw)
            if heading:
                level = len(heading.group(1))
                if previous and level > previous + 1:
                    issues.append(Issue("error", "heading-order", name, number,
                                        "heading level jumps from H%d to H%d" % (previous, level)))
                previous = level
        for match in IMAGE.finditer(text):
            if not match.group(1).strip():
                issues.append(Issue("error", "image-alt", name, _line(text, match.start()),
                                    "images need non-empty alternative text"))
        for match in LINK.finditer(text):
            label, target = match.groups()
            line = _line(text, match.start())
            if label.strip().lower() in AMBIGUOUS:
                issues.append(Issue("error", "ambiguous-link", name, line,
                                    "link text must describe its destination"))
            if not _local_target(root, path, target):
                issues.append(Issue("error", "broken-local-link", name, line,
                                    "local link does not resolve inside the repository"))
        for match in FALSE_LIVE.finditer(text):
            issues.append(Issue("error", "overclaim", name, _line(text, match.start()),
                                "operator docs must not claim unverified external evidence"))
    for name, phrases in BOUNDARY_OWNERS.items():
        text = lowered.get(name)
        if text is None:
            continue
        for phrase in phrases:
            if phrase not in text:
                issues.append(Issue("error", "evidence-boundary", name, 1,
                                    "missing explicit boundary: %s" % phrase))
    for name in REQUIRED_PATHS:
        if not (root / name).is_file():
            issues.append(Issue("error", "missing-runtime-path", name, 1,
                                "documented CLI/API runtime path is absent"))
    readme = root / "README.md"
    if readme.exists() and "local evidence is not external evidence" not in readme.read_text(encoding="utf-8").lower():
        issues.append(Issue("warning", "readme-boundary", "README.md", 1,
                            "add: 'Local evidence is not external evidence.'"))
    issues.extend(check_duplicate_headings(root))
    issues.extend(check_executable_surface(root))
    issues.extend(check_script_count(root))
    issues.extend(check_commitment_probe_rule(root))
    issues.extend(check_declared_paths(root))
    issues.extend(check_inventory(root))
    issues.extend(check_gate_count(root))
    issues.extend(check_examples_inventory(root))
    issues.extend(check_readiness_claims(root))
    issues.extend(check_roadmaps(root))
    return sorted(issues, key=lambda item: (item.severity, item.path, item.line,
                                             item.code, item.message))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--json", action="store_true")
    # One roadmap document, by path, so the counterexample fixtures under
    # tests/ can be run through the same code the tree-wide gate runs.
    parser.add_argument("--roadmap", type=Path, action="append", default=[],
                        metavar="PATH", help="check only these roadmap documents")
    args = parser.parse_args(argv)
    if args.roadmap:
        issues = []
        for path in args.roadmap:
            issues.extend(check_roadmap(path.as_posix(),
                                        path.read_text(encoding="utf-8")))
        issues.sort(key=lambda item: (item.severity, item.path, item.line,
                                      item.code, item.message))
    else:
        issues = check(args.root)
    if args.json:
        print(json.dumps([issue.as_dict() for issue in issues], sort_keys=True))
    else:
        for issue in issues:
            print("%s:%d: %s %s: %s" % (issue.path, issue.line, issue.severity,
                                           issue.code, issue.message))
        print("docs contract: %d error(s), %d warning(s)" %
              (sum(issue.severity == "error" for issue in issues),
               sum(issue.severity == "warning" for issue in issues)))
    return 1 if any(item.severity == "error" or args.strict for item in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
