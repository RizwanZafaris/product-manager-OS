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
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
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


# The commercial half of a pricing decision, which the blank carried nowhere and
# two worksheets promised anyway. The pricing template decided the number and
# stopped: no trial, overage, upgrade, downgrade, proration, refund or
# grandfathering terms, no per-tier evidence or cost floor, and no record of who
# moves when a price changes. The worksheets said they fed "the evidence column"
# of section 3, and section 3 had five columns, none of them evidence.
#
# Four things are read here, and only these four. The blank's own section 3
# table has to carry the column both pricing worksheets send their reading to,
# under the name they use, so neither side can be renamed alone; section 3a and
# the unit economics sheet are pinned to each other the same way, because that
# sheet now sends its cost to serve and its margin there. Section 7 has to ask
# every standing term. And section 8 has to ask, and the filled example has to
# answer, the things a price change is not a decision without. Everything is
# read with the HTML comments taken out (see _shown), because guidance a reader
# never sees is not a field anyone fills.
#
# Stated limits. This counts headings and column names; it does not read what is
# written under them, so a section 8 row whose cells are all "TBD" passes here and
# is caught by the person who signs Gate 5. Only the one filled example declared
# below is read: another example filling this template is not found automatically,
# because the declaration line is the only thing in the tree that says which
# template an example fills, and a check that guessed would report the wrong file.
# And that example is read for its change record only, because the change record is
# what the finding asked an example to prove; an example that dropped its section 3a
# or its section 7 is not reported here, only a blank that dropped them.
# A tree without the pricing template makes no claim and is not checked, the same
# posture the inventory and gate-count checks take toward fixture roots.
PRICING_TEMPLATE = "templates/planning/pricing-packaging.md"
PRICING_EXAMPLE = "examples/ledgerline-pricing-packaging.md"
# The name of the column in the template's section 3 tier table, and the words
# each worksheet uses to send its reading there. Pinned in one place so renaming
# the column in the template alone, or in a worksheet alone, is a failure rather
# than a silent promise of a place that does not exist.
PRICING_EVIDENCE_COLUMN = "Price evidence"
PRICING_EVIDENCE_SOURCES = ("frameworks/pricing/van-westendorp.md",
                            "frameworks/pricing/gabor-granger.md")
# The standing terms section 7 has to ask about. The list is the commercial
# contract a buyer is owed between price changes; a term missing from the blank
# is a term invented at the first ticket.
PRICING_TERMS = ("Trial", "Overage", "Upgrade mid-term", "Downgrade mid-term",
                 "Proration", "Refunds and credits", "Grandfathering")
# What a price change has to say, in the template's section 8 and in the filled
# example, before it is a decision rather than a number: who moves, what they
# pay now, what they pay after, the notice, the effective date, the reversal and
# the evidence. Matched as the opening words of a column heading, so a heading
# may say more but not less.
PRICING_CHANGE_FIELDS = ("Cohort", "Count", "Pays now", "Pays after", "Notice",
                         "Effective date", "Reversal", "Evidence")
# The heading of each section this check reads, and the templates section 9 has
# to route to. A route whose file is not in the tree is a dead end, so each is
# checked to exist.
PRICING_SECTIONS = ("## 7. Standing commercial terms", "## 8. The change record",
                    "## 9. Commercial-change checklist")
# The per-tier economic floor, and the worksheet that feeds it. The unit economics
# sheet sends its cost to serve and its contribution margin to section 3a of the
# pricing blank; deleting that section leaves the worksheet promising a place that
# does not exist, which is the defect this whole check was written for, one heading
# over. Pinned on both sides so neither can be removed or renamed alone.
PRICING_FLOOR_SECTION = "### 3a. Economic floor per tier"
PRICING_FLOOR_SOURCE = "frameworks/metrics/unit-economics.md"
PRICING_ROUTES = ("templates/definition/business-rules.md",
                  "templates/delivery/launch-comms-plan.md",
                  "templates/delivery/customer-comms.md",
                  "templates/delivery/migration-cutover-plan.md",
                  "templates/execution/change-request.md",
                  "templates/delivery/support-runbook.md",
                  "templates/execution/decision-log.md")


def _table_headings(lines: list, start: int, end: int) -> list:
    """Every cell of every table header row between two line indexes.

    A header row is a line of pipe-separated cells whose next line is the
    delimiter row. Cells are returned stripped of their markdown emphasis, since
    the example marks illustrative rows with asterisks.
    """
    cells = []
    for index in range(start, min(end, len(lines)) - 1):
        raw, below = lines[index].strip(), lines[index + 1].strip()
        if not raw.startswith("|") or not below.startswith("|"):
            continue
        if not re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", below):
            continue
        cells.extend(cell.strip().strip("*").strip() for cell in raw.strip("|").split("|"))
    return cells


def check_pricing_contract(root: Path) -> list[Issue]:
    """The pricing blank's commercial contract, and the example that has to answer it."""
    issues: list[Issue] = []
    template = root / PRICING_TEMPLATE
    if not template.is_file():
        return issues
    text = _shown(template.read_text(encoding="utf-8"))
    lines = text.splitlines()
    tiers = _section(lines, "## 3. Tiers and packaging")
    if tiers == (0, 0):
        issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, 1,
                            "section 3 (tiers and packaging) is gone, so the column "
                            "the pricing worksheets feed has nowhere to be"))
    elif PRICING_EVIDENCE_COLUMN not in _table_headings(lines, *tiers):
        issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, tiers[0],
                            "section 3's tier table has no %r column; both pricing "
                            "worksheets say they feed one" % PRICING_EVIDENCE_COLUMN))
    for source in PRICING_EVIDENCE_SOURCES:
        sheet = root / source
        if not sheet.is_file():
            issues.append(Issue("error", "pricing-contract", source, 1,
                                "pricing worksheet is missing"))
        elif PRICING_EVIDENCE_COLUMN not in _shown(sheet.read_text(encoding="utf-8")):
            issues.append(Issue("error", "pricing-contract", source, 1,
                                "this worksheet feeds the pricing template but no "
                                "longer names the %r column it feeds"
                                % PRICING_EVIDENCE_COLUMN))
    for heading in PRICING_SECTIONS:
        if _section(lines, heading) == (0, 0):
            issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, 1,
                                "the pricing blank has lost %r" % heading))
    if _section(lines, PRICING_FLOOR_SECTION) == (0, 0):
        issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, 1,
                            "the pricing blank has lost the per-tier economic floor "
                            "that the unit economics worksheet feeds"))
    floor = root / PRICING_FLOOR_SOURCE
    if not floor.is_file():
        issues.append(Issue("error", "pricing-contract", PRICING_FLOOR_SOURCE, 1,
                            "unit economics worksheet is missing"))
    elif "section 3a" not in _shown(floor.read_text(encoding="utf-8")):
        issues.append(Issue("error", "pricing-contract", PRICING_FLOOR_SOURCE, 1,
                            "this worksheet feeds the pricing template's per-tier "
                            "floor but no longer names the section it feeds"))
    terms = _section(lines, PRICING_SECTIONS[0])
    if terms != (0, 0):
        asked = " ".join(_table_headings(lines, *terms)) + "\n" \
            + "\n".join(lines[terms[0]:terms[1]])
        for term in PRICING_TERMS:
            if term not in asked:
                issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, terms[0],
                                    "section 7 no longer asks for the %s term" % term))
    routes = _section(lines, PRICING_SECTIONS[2])
    if routes != (0, 0):
        routed = "\n".join(lines[routes[0]:routes[1]])
        for target in PRICING_ROUTES:
            if Path(target).name not in routed:
                issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, routes[0],
                                    "section 9 no longer routes the change to %s" % target))
            elif not (root / target).is_file():
                issues.append(Issue("error", "pricing-contract", PRICING_TEMPLATE, routes[0],
                                    "section 9 routes the change to %s, which is not "
                                    "in this tree" % target))
    for name in (PRICING_TEMPLATE, PRICING_EXAMPLE):
        path = root / name
        if not path.is_file():
            issues.append(Issue("error", "pricing-contract", name, 1,
                                "the pricing %s is missing"
                                % ("blank" if name == PRICING_TEMPLATE else "example")))
            continue
        body = _shown(path.read_text(encoding="utf-8")).splitlines()
        record = _section(body, PRICING_SECTIONS[1])
        if record == (0, 0):
            continue
        headings = _table_headings(body, *record)
        for field in PRICING_CHANGE_FIELDS:
            if not any(cell.startswith(field) for cell in headings):
                issues.append(Issue("error", "pricing-contract", name, record[0],
                                    "the change record no longer asks who moves, what "
                                    "they pay, the notice, the effective date, the "
                                    "reversal and the evidence: %r is gone" % field))
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
    issues.extend(check_inventory(root))
    issues.extend(check_gate_count(root))
    issues.extend(check_examples_inventory(root))
    issues.extend(check_readiness_claims(root))
    issues.extend(check_pricing_contract(root))
    return sorted(issues, key=lambda item: (item.severity, item.path, item.line,
                                             item.code, item.message))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
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
