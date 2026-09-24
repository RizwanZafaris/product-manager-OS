#!/usr/bin/env python3
"""Tests for the tree's contract gates. Run: python3 -m unittest tests/test_contract_gates.py

tools/check_manifest.py and tools/check_workspace_contract.py had no tests of
their own, and in each one the check that had quietly stopped working was the
one nothing else covered: the manifest's model-id pattern required a digit, so
the primary production ids of the three vendors it names walked through, and the
workspace contract compared two callers of one shared map, which cannot see a
change to the map itself.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.check_manifest import MODEL_PATTERNS, check_manifest

REPO = Path(__file__).resolve().parent.parent

# harness/ is deletable by design, and both gates report ok on a tree without
# it: check_manifest has no manifest to read and check_workspace_contract has
# no runner to compare against. Tests that seed a manifest defect have nothing
# to seed it into on such a tree, so they skip rather than fail on a fixture.
HAS_HARNESS = (REPO / "harness").is_dir()
NEEDS_HARNESS = unittest.skipUnless(
    HAS_HARNESS, "harness/ is not in this tree, so there is no manifest to "
                 "mutate; the gate itself reports ok here.")

# One real production id per pattern, keyed by the label the gate reports. These
# are ids a contributor would actually paste into a note, which is the property
# that makes the table evidence rather than a restatement of the patterns.
VENDOR_IDS = {
    "an OmniRoute auto tier model string": ("auto/cheap", "auto/coding",
                                            "auto/reasoning"),
    "an OpenAI gpt model id": ("gpt-4o", "gpt-5", "gpt4"),
    "an OpenAI reasoning model id": ("o3-mini", "o1-preview", "o4-pro"),
    "an Anthropic claude model id": ("claude-3-5-sonnet", "claude-opus-4"),
    "an Anthropic model family name": ("sonnet", "opus", "haiku"),
    "a Google gemini model id": ("gemini-2-flash", "gemini-1.5-pro"),
    "a Llama model id": ("llama-3", "llama3"),
    "a Mistral model id": ("mistral-7b", "mistral-large"),
    "a third-party model id": ("deepseek-chat", "deepseek-reasoner",
                               "deepseek-v3", "qwen-max", "qwen-plus",
                               "qwen-turbo", "qwen3-max", "grok-beta",
                               "grok-4"),
}

# A vendor name is not a model id. A gate that fired on these would be routed
# around rather than fixed.
NOT_MODEL_IDS = ("grok the tier doctrine", "grokking the router table",
                 "deepseek is a vendor", "the qwen family")


def copy_tree(tmp):
    """This repository, copied, so a mutation never touches the real one."""
    root = Path(tmp) / "repo"
    shutil.copytree(REPO, root, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                  "*.pyc"))
    return root


class ModelIdGateTests(unittest.TestCase):
    """Check 1 of the manifest gate: no model id anywhere in the manifest."""

    def test_every_pattern_catches_that_vendors_production_ids(self):
        by_label = {label: pattern for pattern, label in MODEL_PATTERNS}
        self.assertEqual(len(by_label), len(MODEL_PATTERNS))
        self.assertEqual(set(by_label), set(VENDOR_IDS))
        for label, ids in VENDOR_IDS.items():
            for model_id in ids:
                with self.subTest(label=label, model_id=model_id):
                    self.assertIsNotNone(
                        re.search(by_label[label], model_id, re.I),
                        "%s is %s and the gate does not see it"
                        % (model_id, label))

    def test_a_vendor_name_in_prose_is_not_read_as_a_model_id(self):
        for text in NOT_MODEL_IDS:
            with self.subTest(text=text):
                hits = [label for pattern, label in MODEL_PATTERNS
                        if re.search(pattern, text, re.I)]
                self.assertEqual([], hits, text)

    @NEEDS_HARNESS
    def test_a_non_numeric_model_id_in_the_manifest_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.assertEqual([], check_manifest(root))
            manifest = root / "harness" / "MANIFEST.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["tier_note"] += " Route this one to deepseek-chat."
            manifest.write_text(json.dumps(data, indent=2) + "\n",
                                encoding="utf-8")
            problems = check_manifest(root)
            self.assertIn("MODEL", {code for _, _, code, _ in problems},
                          problems)


class WorkspaceContractGateTests(unittest.TestCase):
    """The canonical destinations the rest of the tree addresses by name."""

    MOVE = ('"templates/execution/state.md": "STATE.md",',
            '"templates/execution/state.md": "execution/STATE.md",')

    def run_gate(self, root):
        return subprocess.run(
            [sys.executable, str(root / "tools" / "check_workspace_contract.py")],
            capture_output=True, text=True, timeout=300)

    def move_state(self, root):
        module = root / "tools" / "workspace.py"
        text = module.read_text(encoding="utf-8")
        self.assertIn(self.MOVE[0], text)
        module.write_text(text.replace(*self.MOVE), encoding="utf-8")

    def test_moving_the_state_file_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.assertEqual(0, self.run_gate(root).returncode)
            self.move_state(root)
            moved = self.run_gate(root)
            self.assertEqual(1, moved.returncode, moved.stdout + moved.stderr)
            self.assertIn("products/contract-check/STATE.md", moved.stdout)

    def test_moving_the_state_file_fails_with_the_harness_deleted_too(self):
        """harness/ is deletable by design, and deleting it removes both the
        runner this gate compares against and the harness suite that pins
        STATE.md at the workspace root. The canonical table is what is left."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            # ignore_errors so the test still means something on a tree
            # that already has no harness/: the state it puts the copy
            # in is the state that matters, not the removal.
            shutil.rmtree(root / "harness", ignore_errors=True)
            clean = self.run_gate(root)
            self.assertEqual(0, clean.returncode, clean.stdout + clean.stderr)
            self.move_state(root)
            moved = self.run_gate(root)
            self.assertEqual(1, moved.returncode, moved.stdout + moved.stderr)
            self.assertIn("products/contract-check/STATE.md", moved.stdout)


# --- F03: one severity dictionary across the DELIVER set -------------------
# The QA ladder said a core flow broken with no workaround was S2; the UAT
# plan said an unfinishable job was S1 and a workaround was S2. The same
# defect therefore blocked or shipped depending on which document the reader
# had open. The ladder is now canonical; the UAT plan, the support runbook and
# the release-readiness record carry crosswalks onto its ids.
#
# The first review of this fix failed on perimeter: the guard read templates/
# and left the shipped examples, a second table under the same heading, a
# renamed column and a fourth scale in the same folder all unguarded. The
# document sets below are globs, not a list, so a new example is scanned the
# day it lands, and the floors keep an existing one from being renamed out of
# the scan.

TEMPLATES = REPO / "templates" / "delivery"
EXAMPLES = REPO / "examples"


def doc_set(template_name, example_glob, floor):
    """Every shipped document of one kind: the template plus its examples."""
    docs = [TEMPLATES / template_name] + sorted(EXAMPLES.glob(example_glob))
    assert len(docs) >= floor, (
        "%s: found %d documents, inventory floor is %d; a document was renamed "
        "or deleted out of the severity scan" % (template_name, len(docs), floor))
    for doc in docs:
        assert doc.is_file(), "missing severity-covered document: %s" % doc
    return docs


# Floors are the shipped counts at the time of the fix. They are a ratchet: a
# new example raises the real count and still passes, renaming one out of the
# glob does not.
LADDER_DOCS = lambda: doc_set("testing-strategy.md", "*testing-strategy*.md", 2)
CROSSWALK_DOCS = lambda: doc_set("uat-plan.md", "*uat-plan*.md", 2)
SUPPORT_DOCS = lambda: doc_set("support-runbook.md", "*support-runbook*.md", 2)
RELEASE_DOCS = lambda: doc_set("release-readiness.md", "*release-readiness*.md", 4)

LADDER_DOC = TEMPLATES / "testing-strategy.md"
CROSSWALK_DOC = TEMPLATES / "uat-plan.md"
RELEASE_DOC = TEMPLATES / "release-readiness.md"
SUPPORT_DOC = TEMPLATES / "support-runbook.md"

LADDER_HEADING = "## 6. Defect severity ladder (canonical)"
LADDER_HEADER = ["Severity", "Definition", "Release rule"]
CROSSWALK_HEADING = "## 5. Defect handling during UAT"
CROSSWALK_HEADER = ["Canonical severity", "What it looks like in UAT",
                    "Action inside the UAT window",
                    "Release rule (from the canonical ladder)"]
SUPPORT_HEADING = "## 4. Escalation"
SUPPORT_HEADER = ["Canonical severity", "What it looks like on a support call",
                  "Escalate to (name)", "How (channel, pager)",
                  "Expected first response", "What to include"]
DECISION_HEADING = "### What each Severity cell means for the release"
DECISION_HEADER = ["Severity cell",
                   "May the release proceed while this row is open?"]
SEVERITIES = ("S1", "S2", "S3", "S4")
NOT_A_DEFECT = "not a defect"
FIXTURES = REPO / "tests" / "fixtures" / "severity-crosswalk.json"

# A document outside the covered set may not import the canonical ids, and no
# document anywhere may revive the old support scale. "Sev 1" was the fourth
# vocabulary the first review found sitting in the same folder as the fix.
FOREIGN_SCALE = re.compile(r"\bSev ?\d")
GUIDANCE_TREES = ("templates", "examples", "frameworks", "knowledge", "skills")

# Inside a covered document the perimeter is tighter than the tree-wide one
# above: no other spelling of a severity may appear at all, in prose or in a
# table cell. "Sev-1" and "Severity 1" are outside FOREIGN_SCALE on purpose,
# because templates/architecture/design-review-record.md legitimately scores
# usability findings "severity 3 or 4" on a different axis, and that document
# is not covered here.
FOREIGN_SEVERITY = re.compile(
    r"\b(?:sev|severity)[ \-]?\d"
    r"|\bseverity\s+(?:one|two|three|four)\b"
    r"|\bseverity\s+(?:low|medium|high|critical|minor|major|blocker|trivial|cosmetic)\b"
    r"|\b(?:low|medium|high|critical)[ \-]severity\b", re.I)

# The second review's second bypass: every guard in this class parses tables,
# so a contradicting definition written in prose beside the table defeated all
# of them. These two read the prose. They are narrow by construction, and what
# they do not reach is stated in honest_limits, in the ladder itself and in the
# CHANGELOG rather than left silent: they fire on a definition ATTACHED TO A
# CANONICAL ID, in either word order, and prose that defines a defect class
# without naming an id is not reached by them.
PROSE_DEFINES = re.compile(
    r"\bS[1-4]\b(?:\s+(?:row|rows|defect|defects|issue|issues|item|items|"
    r"bug|bugs|case|cases))?\s+(?:means|mean|is defined as|are defined as|"
    r"is when|are when|stands for|signifies|denotes|refers to|covers|is for|"
    r"are for|is anything|are anything|is any|are any|applies to|apply to|"
    r"is the one|are the ones|is used for|are used for|is reserved for|"
    r"are reserved for|is where|are where|is a|are a|is an|are an|is the|"
    r"are the)\b", re.I)
PROSE_ASSIGNS = re.compile(
    r"\b(?:means|mean|counts as|count as|is treated as|are treated as|"
    r"is classified as|are classified as|is defined as|is recorded as|"
    r"is anything|is any|is when)\s+(?:an? )?S[1-4]\b", re.I)
# The same redefinition with the id at the end and the subject in between:
# "we treat an unfinishable job as S1". The verb list is deliberately short --
# a classifying verb, not a reporting one -- so that "accepted as S4" about one
# named row, which cites the ladder, is not mistaken for a definition of it.
PROSE_TREATS = re.compile(
    r"\b(?:treats?|treated|defines?|defined|classif(?:y|ies|ied)|counts?|"
    r"counted|regards?|regarded)\b[^.|]{0,60}?\bas (?:an? )?S[1-4]\b", re.I)


def fixture():
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


def uncommented(lines):
    """Markdown lines with HTML comment blocks dropped, single and multi line."""
    out, inside = [], False
    for line in lines:
        stripped = line.strip()
        if inside:
            if "-->" in stripped:
                inside = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                inside = True
            continue
        out.append(line)
    return out


def cut(line):
    return [c.strip().strip("*").strip() for c in line.split("|")[1:-1]]


def is_delimiter(line):
    cells = [c.strip() for c in line.split("|")[1:-1]]
    return bool(cells) and all(c and set(c) <= set("-:") for c in cells)


def tables_in(lines):
    """Every pipe table in a list of markdown lines, as (header, body rows)."""
    rows = [l.strip() for l in uncommented(lines) if l.strip()]
    found, i = [], 0
    while i < len(rows) - 1:
        if rows[i].startswith("|") and is_delimiter(rows[i + 1]):
            body, j = [], i + 2
            while j < len(rows) and rows[j].startswith("|"):
                body.append(cut(rows[j]))
                j += 1
            found.append((cut(rows[i]), body))
            i = j
            continue
        i += 1
    return found


def all_tables(text):
    return tables_in(text.splitlines())


def every_table(text):
    """all_tables plus the tables parked inside HTML comments. tables_in drops
    comments because the shipped templates narrate the removed scale in them;
    a whole severity table commented out is still a severity table the person
    filling the template reads, so the second-scale rule reads these too."""
    seen, out = [], tables_in([l for l in text.splitlines()
                               if not l.strip().startswith("<!--")
                               and not l.strip().startswith("-->")])
    for table in all_tables(text) + out:
        if table not in seen:
            seen.append(table)
    return seen


def section_lines(text, heading):
    """The lines under `heading`, up to the next heading of any level."""
    lines = text.splitlines()
    assert heading in lines, "heading not found: %s" % heading
    out = []
    for line in lines[lines.index(heading) + 1:]:
        if line.startswith("#"):
            break
        out.append(line)
    return out


def tables_under(text, heading):
    """EVERY table under `heading`. The first review added a second, contra-
    dicting severity table under the UAT heading and nothing failed, because
    only the first table was ever read."""
    return tables_in(section_lines(text, heading))


def table_under(text, heading):
    tables = tables_under(text, heading)
    assert len(tables) == 1, (
        "expected exactly one table under %s, found %d" % (heading, len(tables)))
    return tables[0]


def blocking_class(release_rule):
    """always / conditional / never, read off a canonical-ladder release rule."""
    rule = release_rule.strip().lower()
    if rule.startswith("always blocks"):
        return "always"
    if rule.startswith("blocks unless"):
        return "conditional"
    if rule.startswith("ships"):
        return "never"
    raise AssertionError("unrecognised release rule: %r" % release_rule)


def decision_class(answer):
    """always / conditional / never, read off the release-readiness decision
    table. Deliberately a different vocabulary from the ladder's, so this leg
    of the closure proof reads release-readiness and cannot recompute the
    ladder's answer."""
    text = answer.strip().lower()
    if text.startswith("no"):
        return "always"
    if text.startswith("only if"):
        return "conditional"
    if text.startswith("yes"):
        return "never"
    raise AssertionError("unrecognised release-readiness answer: %r" % answer)


def outcome(kind, approver_recorded):
    """blocks / ships for one defect under one blocking class."""
    if kind == "always":
        return "blocks"
    if kind == "never":
        return "ships"
    return "ships" if approver_recorded else "blocks"


def only_row(rows, cell_index, keywords, where):
    """The one row whose cell contains every keyword. Ambiguity is a failure."""
    hits = [r for r in rows
            if all(k.lower() in r[cell_index].lower() for k in keywords)]
    assert len(hits) == 1, (
        "%s: %r matched %d rows, expected exactly one" % (where, keywords, len(hits)))
    return hits[0]


def severity_columns(header):
    """Indices of every column this document calls a severity."""
    return [i for i, cell in enumerate(header) if "severity" in cell.lower()]


def id_columns(header, rows):
    """Indices of every column that IS a severity scale whatever it is called.
    The header word is not enough: the review's next shape was a table headed
    '| # | Class | Meaning |' whose second column held the canonical ids, which
    no name-based scan reaches. Every filled cell a canonical id, and at least
    one, is a column of severities however the column is titled."""
    # DISCLOSED LIMIT, measured 2026-09-23 in throwaway copies of all ten
    # covered documents. Requiring EVERY filled cell to be canonical keeps an
    # ordinary column that merely mentions an id from being read as a scale,
    # and the price is that one non-id row hides the column from this helper.
    # A second definition table therefore escapes the whole rule when three
    # things hold at once: its ids sit in a column other than the first, one
    # filled cell of that column is not a canonical id (a decoy row such as
    # "(other)"), and no header cell contains the word "severity". Appended to
    # each of the ten covered documents in its own copy, such a table is 10 of
    # 10 GREEN, so this reaches every covered kind, not only some. What still
    # fails: the same table with every row canonical (10 of 10 RED), the same
    # table with its ids in the first column, decoy included, which the
    # first-column rule in the test below catches (10 of 10 RED), a blank cell
    # as the decoy, which is skipped rather than counted (RED), and any column
    # the table calls Severity, which the cell scan and the meaning rule
    # catch whatever its rows say (RED). Widening `all(` to `any(` is the
    # known fix; it is a change to what the gate demands and is not taken here.
    out = []
    for i in range(len(header)):
        cells = [r[i].strip().upper() for r in rows if len(r) > i and r[i].strip()]
        if cells and all(c in SEVERITIES for c in cells):
            out.append(i)
    return out


class SeverityCrosswalkTests(unittest.TestCase):
    """F03, 2026-09-23 360 audit. QA and UAT used incompatible severity
    meanings with no crosswalk, so copying a defect between the two documents
    changed whether it blocked the release. One dictionary now lives in the
    testing strategy; the UAT plan, the support runbook and the release-
    readiness record may only reword it beside one of its ids. These tests
    fail if that stops being true, in the templates or in the examples."""

    # -- the dictionary itself ------------------------------------------

    def read_ladder(self, doc):
        header, rows = table_under(doc.read_text(encoding="utf-8"), LADDER_HEADING)
        self.assertEqual(LADDER_HEADER, header, "%s: not a severity ladder" % doc.name)
        self.assertEqual(list(SEVERITIES), [r[0] for r in rows],
                         "%s: the ladder ids changed" % doc.name)
        return {r[0]: {"definition": r[1], "rule": r[2]} for r in rows}, rows

    def read_crosswalk(self, doc):
        header, rows = table_under(doc.read_text(encoding="utf-8"), CROSSWALK_HEADING)
        self.assertEqual(CROSSWALK_HEADER, header,
                         "%s: the UAT section 5 table is not a crosswalk onto "
                         "the canonical ids" % doc.name)
        self.assertEqual(list(SEVERITIES), [r[0] for r in rows],
                         "%s: the UAT crosswalk does not cover the four ids" % doc.name)
        return {r[0]: {"uat": r[1], "action": r[2], "rule": r[3]} for r in rows}, rows

    def test_every_shipped_ladder_states_the_same_canonical_dictionary(self):
        """The examples are the records the audit's closure proof names. The
        first review restored the pre-fix example ladder with the whole suite
        green, because only templates/ was read."""
        canonical, _ = self.read_ladder(LADDER_DOC)
        for sev in SEVERITIES:
            blocking_class(canonical[sev]["rule"])
        for doc in LADDER_DOCS():
            ladder, _ = self.read_ladder(doc)
            self.assertEqual(canonical, ladder,
                             "%s states a different severity dictionary from "
                             "the canonical ladder" % doc.name)

    def test_every_uat_plan_reworders_the_ladder_and_does_not_redefine_it(self):
        canonical, _ = self.read_ladder(LADDER_DOC)
        for doc in CROSSWALK_DOCS():
            text = doc.read_text(encoding="utf-8")
            cross, _ = self.read_crosswalk(doc)
            for sev in SEVERITIES:
                self.assertEqual(canonical[sev]["rule"], cross[sev]["rule"],
                                 "%s states a different release rule for %s"
                                 % (doc.name, sev))
            self.assertRegex(
                text,
                r"The canonical ladder is \[testing strategy\]"
                r"\([^)]*testing-strategy\.md\) section 6",
                "%s does not point at the canonical ladder" % doc.name)

    def test_every_support_runbook_escalation_table_is_a_crosswalk(self):
        """The fourth vocabulary. Section 4 used to tell the reader to paste
        an org Sev 1 / Sev 2 / Sev 3 scale in, while section 5 was fed known-
        issues rows carrying S1 to S4 from the readiness document."""
        canonical, _ = self.read_ladder(LADDER_DOC)
        for doc in SUPPORT_DOCS():
            text = doc.read_text(encoding="utf-8")
            header, rows = table_under(text, SUPPORT_HEADING)
            self.assertEqual(SUPPORT_HEADER, header,
                             "%s: section 4 is not a crosswalk onto the "
                             "canonical ids" % doc.name)
            self.assertEqual(list(SEVERITIES), [r[0] for r in rows],
                             "%s: section 4 does not cover the four ids" % doc.name)
            self.assertRegex(
                text,
                r"The canonical ladder is \[testing strategy\]"
                r"\([^)]*testing-strategy\.md\) section 6",
                "%s does not point at the canonical ladder" % doc.name)
        self.assertEqual(sorted(canonical), sorted(SEVERITIES))

    def test_no_guidance_document_revives_the_old_support_scale(self):
        """Every tree that tells a reader what to write. CHANGELOG.md is not
        one of them: it records that the scale was removed, in those words,
        and a history that cannot name what it removed is worse than useless.
        Nothing under these five trees may reintroduce it."""
        offenders = []
        for tree in GUIDANCE_TREES:
            for doc in sorted((REPO / tree).glob("**/*.md")):
                hit = FOREIGN_SCALE.search(doc.read_text(encoding="utf-8"))
                if hit:
                    offenders.append("%s: %r" % (doc.relative_to(REPO), hit.group(0)))
        self.assertEqual([], offenders,
                         "a Sev N scale is back in the guidance trees: %s" % offenders)
        self.assertEqual(5, len(GUIDANCE_TREES))
        for tree in GUIDANCE_TREES:
            self.assertTrue((REPO / tree).is_dir(), "missing tree: %s" % tree)

    # -- no second scale anywhere in a covered document ------------------

    def covered(self):
        return LADDER_DOCS() + CROSSWALK_DOCS() + SUPPORT_DOCS() + RELEASE_DOCS()

    def allowed_cells(self):
        classes = fixture()["gap_classes"]
        return ({s.lower() for s in SEVERITIES}
                | {"%s: %s" % (NOT_A_DEFECT, c) for c in classes}
                | {"%s: [gap class]" % NOT_A_DEFECT, ""})

    def test_every_severity_column_in_a_covered_document_holds_a_canonical_value(self):
        """Scans by the Severity column itself, not by a pair of exact header
        strings. The first review hid a table from the old scan by renaming a
        neighbouring column, and put 'medium' back in a shipped example."""
        allowed = self.allowed_cells()
        seen = 0
        for doc in self.covered():
            for header, rows in all_tables(doc.read_text(encoding="utf-8")):
                for column in severity_columns(header):
                    for row in rows:
                        if len(row) <= column:
                            continue
                        cell = row[column].strip()
                        seen += 1
                        self.assertIn(cell.lower(), allowed,
                                      "%s: severity %r is not in the canonical "
                                      "dictionary" % (doc.name, cell))
        self.assertGreaterEqual(seen, 30, "the severity columns were not found")

    # Each covered document kind has exactly one table it is allowed to key by
    # the canonical ids, and which one depends on the kind. Only the release-
    # readiness TEMPLATE carries a decision table; its examples carry none.
    OWN_TABLE = (("ladder", LADDER_DOCS, LADDER_HEADING),
                 ("crosswalk", CROSSWALK_DOCS, CROSSWALK_HEADING),
                 ("support", SUPPORT_DOCS, SUPPORT_HEADING),
                 ("release", RELEASE_DOCS, DECISION_HEADING))

    # A column name that pairs a severity with what it MEANS, or with when it
    # blocks, is a definition table however its rows are keyed.
    MEANING_WORDS = ("mean", "definition", "define", "looks like", "description",
                     "describes", "criteria", "stands for", "covers",
                     "when to use", "what it is", "applies", "scope",
                     "release rule")

    def own_tables(self, doc):
        """The one table this document's kind may key by the canonical ids."""
        for _, docs, heading in self.OWN_TABLE:
            if doc in docs():
                try:
                    return tables_under(doc.read_text(encoding="utf-8"), heading)
                except AssertionError:
                    # The heading is absent. Every release-readiness example is
                    # in this case legitimately; a covered document that has
                    # lost its canonical heading fails in the tests above, and
                    # here its canonical table stops being exempt, which is the
                    # safe direction.
                    return []
        raise AssertionError("%s is in no covered kind" % doc.name)

    def test_no_covered_document_carries_a_second_severity_definition_table(self):
        """The third review's blocking bypass. This rule used to iterate the
        UAT plans alone, so a contradicting '| Severity | Definition | Release
        rule |' table appended to templates/delivery/testing-strategy.md, the
        file that holds the single dictionary, left every test green. It now
        walks every covered document and exempts only that document's own
        canonical table.

        A second table may still CITE a severity, in a register of accepted
        exceptions for instance, and the cell scan holds those cells to the
        canonical set. What it may not do is DEFINE one, and a definition table
        is either keyed by the id or pairs a severity column with a meaning."""
        walked = exempted = 0
        for doc in self.covered():
            walked += 1
            own = self.own_tables(doc)
            for header, rows in every_table(doc.read_text(encoding="utf-8")):
                if (header, rows) in own:
                    exempted += 1
                    continue
                first = {r[0].strip().upper() for r in rows if r}
                self.assertFalse(first & set(SEVERITIES),
                                 "%s: a second table is keyed by the canonical "
                                 "ids, so it defines a severity rather than "
                                 "citing one: %s" % (doc.name, header))
                # This assertion has a disclosed limit, stated in full at
                # id_columns: a column other than the first whose ids are
                # broken by one non-canonical row is not seen here, and the
                # rules either side of this one do not see it either.
                stray = set(id_columns(header, rows)) - set(severity_columns(header))
                self.assertEqual(
                    set(), stray,
                    "%s: a column this table does not call a severity holds the "
                    "canonical ids, which is a second scale under another name: "
                    "%s" % (doc.name, [header[i] for i in sorted(stray)]))
                if not severity_columns(header):
                    continue
                meaning = [c for c in header
                           if any(w in c.lower() for w in self.MEANING_WORDS)]
                self.assertEqual([], meaning,
                                 "%s: a second table pairs a severity with a "
                                 "meaning or a release rule, which is a second "
                                 "scale: %s" % (doc.name, header))
        self.assertGreaterEqual(walked, 10, "the covered set shrank")
        # Ten documents, and every one but the four release-readiness examples
        # carries a canonical table: two ladders, two crosswalks, two support
        # crosswalks and the release-readiness template's decision table.
        self.assertEqual(7, exempted,
                         "a covered document lost its canonical table, or "
                         "gained a second one that was exempted")

    def test_no_covered_document_defines_a_severity_in_prose(self):
        """The third review's second blocking bypass: every other guard here
        parses tables, so 'For the sponsor's purposes S1 means a tester cannot
        complete a scoped job at all' sat in the UAT template, three lines under
        a sentence these tests pin saying severity is not redefined there, with
        everything green. That sentence is the audit's own wording.

        Two nets, both narrow. A definition verb attached to a canonical id, in
        either word order, is a redefinition. Any severity vocabulary that is
        not S1 to S4 -- Sev 1, Severity 1, 'severity Low', 'Low severity' -- may
        not appear in a covered document at all, in prose or in a cell."""
        offenders, foreign, lines_read = [], [], 0
        for doc in self.covered():
            # Every line, including fenced blocks and HTML comments. A reader
            # filling a template reads its comments, so a definition parked in
            # one is a definition. This is why the surviving comments in the
            # UAT plan and the support runbook narrate the removed scale
            # without restating it.
            for line in doc.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                lines_read += 1
                where = "%s: %%r in %%r" % doc.name
                hit = FOREIGN_SEVERITY.search(line)
                if hit:
                    foreign.append(where % (hit.group(0), stripped[:90]))
                if stripped.startswith("|"):
                    continue
                for pattern in (PROSE_DEFINES, PROSE_ASSIGNS, PROSE_TREATS):
                    hit = pattern.search(line)
                    if hit:
                        offenders.append(where % (hit.group(0), stripped[:90]))
        self.assertEqual([], offenders,
                         "a covered document defines a severity in prose "
                         "instead of citing the canonical ladder: %s" % offenders)
        self.assertEqual([], foreign,
                         "a covered document uses a severity vocabulary that is "
                         "not S1 to S4: %s" % foreign)
        # 1263 lines across the ten documents today. The floor is a ratchet
        # close under that: trimming a paragraph passes, gutting a document so
        # the scan has nothing to read does not.
        self.assertGreaterEqual(lines_read, 1100,
                                "the prose scan read too little to be reading "
                                "the covered documents")

    def test_each_release_readiness_record_keeps_a_severity_bearing_table(self):
        """Renaming the Severity column itself is the last way out of the scan
        above, so every shipped record must still have one."""
        for doc in RELEASE_DOCS():
            tables = [h for h, _ in all_tables(doc.read_text(encoding="utf-8"))
                      if severity_columns(h) and any("issue" in c.lower() for c in h)]
            self.assertTrue(tables,
                            "%s: no known-issues table with a Severity column"
                            % doc.name)

    # -- the release-readiness leg, read from release-readiness ----------

    def decision_table(self):
        header, rows = table_under(RELEASE_DOC.read_text(encoding="utf-8"),
                                   DECISION_HEADING)
        self.assertEqual(DECISION_HEADER, header,
                         "the release decision table changed shape")
        table = {r[0]: r[1] for r in rows}
        self.assertEqual(list(SEVERITIES) + ["%s: [gap class]" % NOT_A_DEFECT],
                         [r[0] for r in rows],
                         "the release decision table does not cover every "
                         "severity cell value")
        return table

    def test_the_release_decision_table_is_classifiable(self):
        table = self.decision_table()
        for key, answer in table.items():
            decision_class(answer)
        self.assertEqual("always", decision_class(table["S1"]))
        self.assertEqual("conditional", decision_class(table["S2"]))

    def test_the_three_synthetic_defects_block_the_same_way_in_every_document(self):
        """The closure proof for F03. Each defect is resolved to a severity id
        twice, once through the engineering definition and once through the UAT
        business wording, and the release outcome is then read three times: off
        the ladder's release rule, off the UAT crosswalk's, and off the release-
        readiness decision table, which is a separate table in a separate
        document with its own vocabulary. All three must agree with the
        fixture, in the template set and in every shipped example."""
        decisions = self.decision_table()
        defects = fixture()["defects"]
        self.assertEqual(3, len(defects))
        ladders = LADDER_DOCS()
        crosswalks = CROSSWALK_DOCS()
        self.assertEqual(len(ladders), len(crosswalks),
                         "a testing strategy or a UAT plan has no counterpart")
        for ladder_doc, cross_doc in zip(ladders, crosswalks):
            _, ladder_rows = self.read_ladder(ladder_doc)
            _, cross_rows = self.read_crosswalk(cross_doc)
            where = "%s / %s" % (ladder_doc.name, cross_doc.name)
            for defect in defects:
                approved = defect["approver_recorded"]
                qa_row = only_row(ladder_rows, 1, defect["qa_keywords"],
                                  "%s, %s through the QA ladder" % (where, defect["id"]))
                uat_row = only_row(cross_rows, 1, defect["uat_keywords"],
                                   "%s, %s through the UAT crosswalk" % (where, defect["id"]))
                self.assertEqual(defect["canonical"], qa_row[0],
                                 "%s, %s: the engineering definition resolves to %s"
                                 % (where, defect["id"], qa_row[0]))
                self.assertEqual(defect["canonical"], uat_row[0],
                                 "%s, %s: the UAT wording resolves to %s, not %s"
                                 % (where, defect["id"], uat_row[0], defect["canonical"]))
                qa_outcome = outcome(blocking_class(qa_row[2]), approved)
                uat_outcome = outcome(blocking_class(uat_row[3]), approved)
                release_outcome = outcome(
                    decision_class(decisions[defect["canonical"]]), approved)
                self.assertEqual(
                    [defect["expected_outcome"]] * 3,
                    [qa_outcome, uat_outcome, release_outcome],
                    "%s, %s: testing strategy says %s, UAT says %s, release "
                    "readiness says %s" % (where, defect["id"], qa_outcome,
                                           uat_outcome, release_outcome))

    def test_no_shipped_known_issues_row_ships_open_against_the_decision_table(self):
        """The exit-gate lines are the operative enforcement in that document,
        so the records are checked against them, not only the words checked
        against the file."""
        classes = fixture()["gap_classes"]
        evidence = fixture()["gap_class_evidence"]
        self.assertEqual(sorted(classes), sorted(evidence),
                         "a gap class has no evidence words")
        checked = 0
        for doc in RELEASE_DOCS():
            for header, rows in all_tables(doc.read_text(encoding="utf-8")):
                columns = severity_columns(header)
                if not columns or not any("issue" in c.lower() for c in header):
                    continue
                column = columns[0]
                issue = [i for i, c in enumerate(header) if "issue" in c.lower()][0]
                why = [i for i, c in enumerate(header)
                       if "acceptable" in c.lower() or "why" in c.lower()]
                for row in rows:
                    if len(row) <= max(column, issue):
                        continue
                    cell, story = row[column].strip().lower(), row[issue].lower()
                    if not cell:
                        # A wholly blank row is the template's unfilled one. A
                        # row that names an issue and leaves the severity blank
                        # is a defect with no id, which is the hole this fix
                        # exists to close, so it fails here rather than being
                        # skipped alongside the placeholder.
                        self.assertFalse(
                            any(c.strip() for c in row),
                            "%s: a known-issues row carries no severity: %s"
                            % (doc.name, row[issue][:60]))
                        continue
                    checked += 1
                    self.assertNotEqual("s1", cell,
                                        "%s: an S1 row may not ship open: %s"
                                        % (doc.name, row[issue][:60]))
                    if cell == "s2":
                        reason = row[why[0]].lower() if why else ""
                        self.assertTrue(
                            "condition" in reason or "accepted by" in reason
                            or "approved by" in reason,
                            "%s: an S2 row records no approver and is not "
                            "written as a condition: %s"
                            % (doc.name, row[issue][:60]))
                    if cell.startswith(NOT_A_DEFECT):
                        self.assertTrue(cell.startswith(NOT_A_DEFECT + ": "),
                                        "%s: a not-a-defect row names no gap "
                                        "class: %r" % (doc.name, row[column]))
                        gap = cell.split(": ", 1)[1]
                        self.assertIn(gap, classes,
                                      "%s: %r is not one of the four gap "
                                      "classes" % (doc.name, gap))
                        self.assertTrue(
                            any(word in story for word in evidence[gap]),
                            "%s: the row claims %r but its Issue cell shows no "
                            "gap, so a defect is being relabelled out of the "
                            "ladder: %s" % (doc.name, gap, row[issue][:80]))
        self.assertGreaterEqual(checked, 12, "the known-issues rows were not found")

    # -- the documents may not claim more than the tests enforce ---------

    def test_release_readiness_states_the_rules_these_tests_enforce(self):
        release = RELEASE_DOC.read_text(encoding="utf-8")
        for claim in (
            "The Severity cell takes one canonical ID from the "
            "[testing strategy](testing-strategy.md) severity ladder",
            "`not a defect: untested path`",
            "`not a defect: missing runbook`",
            "`not a defect: unstaffed support`",
            "`not a defect: external approval pending`",
            "An S1 row, or an S2 row with no named approver recorded "
            "against it, is a condition and may not ship open",
            "- [ ] Every Severity cell is a canonical id from the testing "
            "strategy ladder, or `not a defect:` followed by one of the four "
            "gap classes named in section 3",
            "- [ ] No known-issues row is S1, and every S2 row names the "
            "approver who accepted it and why, or it has moved to a condition",
            "| Severity invented at the meeting |",
        ):
            self.assertIn(claim, release,
                          "release-readiness no longer states: %s" % claim[:60])

    def test_the_ladder_claims_exactly_the_documents_that_are_covered(self):
        """The first review found the fix asserting 'no other document in this
        product's DELIVER set defines a severity of its own' while the support
        runbook, same folder, defined one. The claim now names its documents,
        and the test reads the same four kinds the scan reads."""
        for doc in LADDER_DOCS():
            text = doc.read_text(encoding="utf-8")
            self.assertIn("single defect-severity dictionary for four documents",
                          text, "%s: the dictionary claim changed" % doc.name)
            for link in ("uat-plan.md", "release-readiness.md", "support-runbook.md"):
                self.assertRegex(text, r"\]\([^)]*%s\)" % re.escape(link),
                                 "%s: the dictionary claim does not name %s"
                                 % (doc.name, link))
            self.assertIn("What it does not reach is prose that defines a "
                          "defect class without naming an ID", text,
                          "%s: the ladder no longer states the limit of the "
                          "checks, which is the one thing review has to carry"
                          % doc.name)
            self.assertIn("when one attaches a definition to an ID in prose",
                          text,
                          "%s: the ladder no longer states that prose is read"
                          % doc.name)
            self.assertIn("none of the other three covered documents, the UAT "
                          "plan, the release-readiness checklist and the "
                          "support runbook, defines a defect severity of its "
                          "own", text,
                          "%s: the exit gate no longer names the covered set"
                          % doc.name)
        # The claim names three documents besides the ladder. The scan walks
        # three document kinds besides the ladder. doc_set() raises if any kind
        # lost a document, so walking the set here pins the sentence to the
        # files the other tests read rather than to a list kept beside it.
        covered = [CROSSWALK_DOCS(), SUPPORT_DOCS(), RELEASE_DOCS()]
        self.assertEqual(3, len(covered))
        for kind in covered:
            self.assertTrue(kind, "a covered document kind is empty")
        self.assertGreaterEqual(len(self.covered()), 10,
                                "the covered set shrank below its inventory")
# --------------------------------------------------------------------------
# F09: the PRD's own lineage and change-impact contract.
# --------------------------------------------------------------------------

PRD = REPO / "templates" / "definition" / "prd.md"

# The trace the audit's closure proof names, hop by hop: objective, the evidence
# it stands on, the capability that serves it, the story, the acceptance
# criterion, the test, and the release decision that criterion gates. Each entry
# is one of the PRD's tables and the columns that carry those hops, written out
# here rather than read off the template, so a renamed or dropped column fails
# instead of quietly shrinking what this test walks.
TRACE_COLUMNS = {
    "objectives": ("Evidence", "Metric ID"),
    "stories": ("Acceptance criteria ID", "Verified by (test ID, filled at BUILD)"),
    "scope": ("Objective it serves", "Story it serves", "Release slice"),
    "slices": ("Capabilities", "Depends on", "Dependency register ID"),
    "launch": ("Covers (slice or objective)", "Verified by (artifact or test ID)"),
    "companions": ("Applies (Yes / No)", "Why"),
    "signoff": ("Revision signed",),
    "changes": ("What changed (rows by ID)", "CR", "Approvals re-taken",
                "Approvals unaffected"),
}
# The cell that identifies each of those tables, so a table is found by what it
# is rather than by where it sits: sections move, headers do not.
TABLE_KEYS = {
    "objectives": "Objective",
    "stories": "Story",
    "scope": "Capability",
    "slices": "Slice",
    "launch": "Criterion",
    "companions": "Open this",
    "signoff": "Role",
    "changes": "Version",
}

# One filled PRD, ILLUSTRATIVE throughout and invented for this test. Values are
# keyed by column name, never by position, so the fixture is rendered through
# whatever header the shipped template carries: a column the template drops is a
# hop this fixture can no longer supply, which is the failure this test is for.
FIXTURE = {
    "objectives": [
        {"#": "O1", "Objective": "Field reps submit an expense report without retyping it",
         "Evidence": "E7", "Metric": "median submission time", "Metric ID": "M-004",
         "Baseline": "14 min", "Target": "7 min", "Metric owner": "Priya Nair",
         "Measured where": "report_submitted event"}],
    "stories": [
        {"#": "US1", "Story": "As a field rep, I want the receipt read for me, so that I do not retype it.",
         "Persona": "field rep", "Priority (must / should / later)": "must",
         "Acceptance criteria ID": "AC-1",
         "Verified by (test ID, filled at BUILD)": "TC-101"}],
    "scope": [
        {"#": "F1", "Capability": "Receipt extraction",
         "What it does, in one sentence": "Reads amount, date and merchant from a photographed receipt.",
         "Objective it serves": "O1", "Story it serves": "US1",
         "Release slice": "S1", "Detail": "FR-001"}],
    "slices": [
        {"Slice": "S1", "What it delivers": "Extraction behind a pilot flag",
         "Capabilities": "F1", "Depends on": "none",
         "Dependency register ID": "n/a", "Planned release": "Now row 1"}],
    "launch": [
        {"#": "L1", "Criterion": "All \"must\" stories pass their acceptance criteria",
         "Covers (slice or objective)": "S1",
         "Verified by (artifact or test ID)": "TC-101", "Owner": "Maya Chen"}],
    "companions": [
        {"Trigger, if this is true of your product": "It processes personal data",
         "Open this": "privacy-impact-assessment.md", "Stage": "DESIGN",
         "Applies (Yes / No)": "Yes", "Why": "Receipts carry names and card tails"},
        {"Trigger, if this is true of your product": "It touches what customers pay for",
         "Open this": "pricing-packaging.md", "Stage": "PLANNING",
         "Applies (Yes / No)": "No", "Why": "No tier or price changes in this slice"}],
    "signoff": [
        {"Role": "Product owner", "Name": "Maya Chen", "Date": "2026-04-02",
         "Revision signed": "v1.1", "What they are signing": "Scope"},
        {"Role": "Engineering lead", "Name": "Daniel Okafor", "Date": "2026-03-10",
         "Revision signed": "v1.0", "What they are signing": "Feasibility"}],
    "changes": [
        {"Version": "v1.1", "Date": "2026-04-02",
         "What changed (rows by ID)": "O1, AC-1", "CR": "CR-4",
         "Approvals re-taken": "Product owner",
         "Approvals unaffected": "Engineering lead: no build change"}],
}
FIXTURE_BASELINE = "v1.0"


def md_tables(text):
    """Every markdown table in a document, as a list of (headers, rows-of-dicts)."""
    found, lines = [], text.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("|") or i + 1 >= len(lines):
            continue
        if not re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lines[i + 1].strip()):
            continue
        headers = [c.strip() for c in line.strip().strip("|").split("|")]
        rows = []
        for body in lines[i + 2:]:
            if not body.startswith("|"):
                break
            cells = [c.strip() for c in body.strip().strip("|").split("|")]
            rows.append(dict(zip(headers, cells)))
        found.append((headers, rows))
    return found


def prd_table(text, key):
    """The one table in a document whose header carries TABLE_KEYS[key]."""
    wanted = TABLE_KEYS[key]
    hits = [t for t in md_tables(text) if wanted in t[0]]
    return hits[0] if len(hits) == 1 else None


def render_fixture(template_text, fixture=None, baseline=FIXTURE_BASELINE):
    """The fixture, written out through the shipped template's own headers.

    Cells the fixture does not name are rendered empty, so a template that grows
    a column stays renderable; a template that drops one loses the value the
    trace below needs, which is the point.
    """
    fixture = FIXTURE if fixture is None else fixture
    out = ["# Trace fixture (ILLUSTRATIVE, invented for this test)",
           "", "**Baseline:** %s" % baseline, ""]
    for key in TABLE_KEYS:
        headers = prd_table(template_text, key)[0]
        out.append("| " + " | ".join(headers) + " |")
        out.append("|" + "---|" * len(headers))
        for row in fixture[key]:
            out.append("| " + " | ".join(row.get(h, "") for h in headers) + " |")
        out.append("")
    return "\n".join(out)


def resolve_trace(filled):
    """Walk O1 to the release decision, returning the hops that resolved.

    Every hop reads a cell by column name and looks the value up in the table it
    points at. A missing column, an empty cell or an id that names no row stops
    the walk, and the caller sees how far it got.
    """
    hops, cell = [], lambda row, name: (row or {}).get(name, "").strip()
    tables = {key: prd_table(filled, key) for key in TABLE_KEYS}
    if any(t is None for t in tables.values()):
        return hops
    find = lambda key, col, value: next(
        (r for r in tables[key][1] if cell(r, col) == value), None)

    objective = find("objectives", "#", "O1")
    for column, label in (("Evidence", "evidence"), ("Metric ID", "metric")):
        if not cell(objective, column):
            return hops
        hops.append("O1 -> %s %s" % (label, cell(objective, column)))

    capability = next((r for r in tables["scope"][1]
                       if cell(r, "Objective it serves") == "O1"), None)
    if not capability:
        return hops
    hops.append("O1 -> %s" % cell(capability, "#"))

    story = find("stories", "#", cell(capability, "Story it serves"))
    if not story:
        return hops
    hops.append("%s -> %s" % (cell(capability, "#"), cell(story, "#")))

    criterion = cell(story, "Acceptance criteria ID")
    test = cell(story, "Verified by (test ID, filled at BUILD)")
    if not criterion or not test:
        return hops
    hops.append("%s -> %s" % (cell(story, "#"), criterion))
    hops.append("%s -> %s" % (criterion, test))

    slice_row = find("slices", "Slice", cell(capability, "Release slice"))
    if not slice_row or not cell(slice_row, "Depends on"):
        return hops
    hops.append("%s -> %s" % (cell(capability, "#"), cell(slice_row, "Slice")))

    decision = next((r for r in tables["launch"][1]
                     if cell(r, "Covers (slice or objective)") == cell(slice_row, "Slice")
                     and cell(r, "Verified by (artifact or test ID)") == test), None)
    if not decision:
        return hops
    hops.append("%s -> %s" % (test, cell(decision, "#")))
    return hops


FULL_TRACE = ["O1 -> evidence E7", "O1 -> metric M-004", "O1 -> F1", "F1 -> US1",
              "US1 -> AC-1", "AC-1 -> TC-101", "F1 -> S1", "TC-101 -> L1"]


class PrdLineageTraceTests(unittest.TestCase):
    """F09: the PRD carries the lineage and the change impact itself.

    The audit's closure proof is a reviewer tracing O1 to the release decision
    without guessing, and a change naming the approvals it affects. Both are
    checked here against one filled fixture rendered through the shipped
    template's own headers, so the trace cannot pass on a template that no
    longer asks for the columns it walks.

    Named limits, three. The cited IDs are not resolved into the documents that
    define them: E7 is not looked up in ../discovery/evidence-note.md, M-004 not
    in ../operate/metrics-dictionary.md, TC-101 not in the frd.md matrix, so this
    proves the chain is expressible and internally consistent, not that its far
    ends exist. Nothing here reads a real product's PRD. And no gate rejects a
    filled PRD that leaves the new cells blank; on the default path the exit-gate
    checklist and the humans who sign Gate 2 are what enforce them, exactly as
    with every other field in this template.
    """

    @classmethod
    def setUpClass(cls):
        cls.template = PRD.read_text(encoding="utf-8")

    def test_the_template_asks_for_every_column_the_trace_walks(self):
        for key, columns in TRACE_COLUMNS.items():
            table = prd_table(self.template, key)
            self.assertIsNotNone(table, "no single %s table in the PRD template" % key)
            for column in columns:
                with self.subTest(table=key, column=column):
                    self.assertIn(column, table[0])

    def test_the_template_names_a_baseline_and_a_change_reference(self):
        for phrase in ("**Baseline:**", "**Changes since baseline:**",
                       "change-request.md"):
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase in self.template,
                                "the PRD template does not name %s" % phrase)

    def test_the_filled_fixture_resolves_every_hop_to_the_release_decision(self):
        self.assertEqual(FULL_TRACE, resolve_trace(render_fixture(self.template)))

    def test_a_broken_hop_stops_the_walk_rather_than_passing(self):
        """The walk has teeth: emptying one cell truncates the trace."""
        for key, column, stops_after in (("objectives", "Evidence", 0),
                                         ("scope", "Objective it serves", 2),
                                         ("stories", "Verified by (test ID, filled at BUILD)", 4),
                                         ("slices", "Depends on", 6)):
            with self.subTest(column=column):
                broken = {k: [dict(r) for r in rows] for k, rows in FIXTURE.items()}
                broken[key][0][column] = ""
                hops = resolve_trace(render_fixture(self.template, broken))
                self.assertEqual(FULL_TRACE[:stops_after], hops)

    def test_a_change_names_the_approvals_it_re_took_and_the_ones_it_did_not(self):
        filled = render_fixture(self.template)
        roles = {r["Role"] for r in prd_table(filled, "signoff")[1]}
        ids = ({r["#"] for r in prd_table(filled, "objectives")[1]}
               | {r["Acceptance criteria ID"] for r in prd_table(filled, "stories")[1]})
        for change in prd_table(filled, "changes")[1]:
            with self.subTest(version=change["Version"]):
                self.assertTrue(change["CR"].startswith("CR-"), change["CR"])
                changed = {v.strip() for v in change["What changed (rows by ID)"].split(",")}
                self.assertTrue(changed <= ids, "change names rows this PRD has not: %s"
                                % sorted(changed - ids))
                retaken = {v.strip() for v in change["Approvals re-taken"].split(",")}
                unaffected = {v.split(":")[0].strip()
                              for v in change["Approvals unaffected"].split(",")}
                self.assertTrue(retaken <= roles, sorted(retaken - roles))
                self.assertEqual(roles, retaken | unaffected,
                                 "every signer is either re-taken or explained")
                for role in unaffected:
                    self.assertIn(":", change["Approvals unaffected"],
                                  "%s is unaffected with no reason" % role)

    def test_a_signature_older_than_a_change_names_the_older_revision(self):
        """The revision column is what stops a signature outliving its bytes."""
        filled = render_fixture(self.template)
        signed = {r["Role"]: r["Revision signed"] for r in prd_table(filled, "signoff")[1]}
        change = prd_table(filled, "changes")[1][0]
        retaken = {v.strip() for v in change["Approvals re-taken"].split(",")}
        for role, revision in signed.items():
            with self.subTest(role=role):
                self.assertEqual(revision == change["Version"], role in retaken)
        self.assertIn(FIXTURE_BASELINE, set(signed.values()))

    def test_every_companion_row_is_answered_yes_or_no_with_a_reason(self):
        for row in prd_table(render_fixture(self.template), "companions")[1]:
            with self.subTest(trigger=row["Open this"]):
                self.assertIn(row["Applies (Yes / No)"], ("Yes", "No"))
                self.assertTrue(row["Why"])

    def test_the_shipped_companion_table_leaves_both_cells_for_the_filler(self):
        """Blank in the template, mandatory in the exit gate: the template must
        not answer the applicability question on the reader's behalf."""
        headers, rows = prd_table(self.template, "companions")
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(trigger=row["Open this"]):
                self.assertEqual("", row["Applies (Yes / No)"])
                self.assertEqual("", row["Why"])

    def test_the_exit_gate_checks_each_new_contract(self):
        gate = self.template.split("## Exit gate")[-1]
        for phrase in ("evidence ID and a metric-dictionary ID",
                       "an objective, and a release slice",
                       "names its dependencies",
                       "names what it covers and what verifies it",
                       "answered Yes or No with a reason",
                       "the revision each signed",
                       "the approvals it re-took"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, gate)


if __name__ == "__main__":
    unittest.main()
