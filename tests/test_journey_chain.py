#!/usr/bin/env python3
"""Tests for the two journey record generators, and for what other documents say about them.

    python3 -m unittest test_journey_chain

tools/journey_chain.py answers every Gate 1 to 3 question from the documents
it copies into its workspace, the expense copilot's and the Ledgerline journey
sheet, and its record says what pmos checked and what the generator checked. tools/journey_record.py drives all six banks on a fictional product and
reads its evidence columns from the runtime. Every defect below is seeded
somewhere disposable: a scratch copy of the files the chain generator reads, run
as a subprocess, a workspace built into a temporary directory, or a function
patched for one test. Nothing here writes to the repository.
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
for _entry in (str(REPO), str(REPO / "tools")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import journey_chain  # noqa: E402
import journey_record  # noqa: E402
import workspace  # noqa: E402
from pmos.banks import load_contract  # noqa: E402
from pmos.cli import main as pmos_main  # noqa: E402

RECORD = REPO / "examples" / "journey-chain.md"
RUN_RECORD = REPO / "examples" / "journey-run.md"
# Written out rather than read from the generator, so the generator cannot widen its own
# exception list and still pass: these are the questions whose lands_in names no document
# the expense copilot chain wrote, measured against the workspace it builds. The ceiling is
# this set, seven, not the two first planned: DISCOVER-8's lands_in names only the STATE.md
# position block, which is not an artifact, and DESIGN-2, DESIGN-6, DESIGN-7 and DESIGN-8
# name an integrations document, an observability plan, the AI overlay's agent architecture
# and guardrails, and a design review record, five documents no expense copilot example fills.
EXPECTED_FALLBACKS = {"DISCOVER-8", "DEFINE-7", "DEFINE-9", "DESIGN-2", "DESIGN-6", "DESIGN-7",
                      "DESIGN-8"}
# The questions answered under a stronger evidence class than they ask for, because no
# clause of the section they cite records a yes from anyone it names.
EXPECTED_STRONGER = {"DEFINE-6", "DESIGN-2", "DESIGN-5"}
FALLBACK_PREFIX = "lands_in target absent, cited "
LANDS_IN_MD = re.compile(r"`([^`]+\.md)`")
# Everyone the expense copilot documents name.
CAST = ("Maya Chen", "Priya Nair", "Daniel Okafor")


def scratch_copy(where: Path) -> Path:
    """A copy of what the generator reads: the runtime, the tools, the templates and
    frameworks it stamps from, and the documents it copies."""
    repo = where / "repo"
    repo.mkdir()
    shutil.copy2(REPO / "lint.py", repo / "lint.py")
    for name in ("pmos", "tools", "templates", "frameworks"):
        shutil.copytree(REPO / name, repo / name,
                        ignore=shutil.ignore_patterns("__pycache__", "._*"))
    (repo / "examples").mkdir()
    for path in sorted((REPO / "examples").glob("expense-copilot-*.md")):
        shutil.copy2(path, repo / "examples" / path.name)
    shutil.copy2(REPO / "examples" / "ledgerline-journey.md",
                 repo / "examples" / "ledgerline-journey.md")
    return repo


def run_chain(repo: Path, out: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "tools" / "journey_chain.py"),
                           "--out", str(out)],
                          cwd=repo, capture_output=True, text=True, timeout=300)


def record_rows():
    """Question id to (evidence class cell, cited cell, section) from the answer table."""
    rows = {}
    for line in RECORD.read_text(encoding="utf-8").split("\n"):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.fullmatch(r"(?:DISCOVER|DEFINE|DESIGN)-\d+", cells[0]):
            rows[cells[0]] = (cells[1], cells[2], cells[3])
    return rows


def gates_column(text: str, title: str) -> dict:
    """Bank id to the integer in one titled column of a record's Gates table."""
    lines = text.split("\n")
    header = next(line for line in lines if line.startswith("| Gate | Bank |"))
    index = [cell.strip() for cell in header.strip().strip("|").split("|")].index(title)
    column = {}
    for line in lines:
        if re.match(r"\| [1-6] \| ", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            column[cells[1]] = int(cells[index])
    return column


def built_workspace(where: Path) -> Path:
    journey_chain.build_workspace(where)
    return where


class JourneyChainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract()
        cls.questions = {question["id"]: question
                         for bank in cls.contract["banks"] if bank["id"] in journey_chain.GATE_OF
                         for question in bank["questions"]}

    # ------------------------------ the declarations ------------------------------

    def test_an_example_that_declares_nothing_stops_the_run_and_names_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            (repo / "examples" / "expense-copilot-stray.md").write_text(
                "# Stray notes\n\nNotes on templates/definition/prd.md, filling nothing.\n",
                encoding="utf-8")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertNotEqual(done.returncode, 0)
            self.assertIn("expense-copilot-stray.md declares nothing to fill", done.stderr)
            self.assertFalse(out.exists())

    def test_only_the_first_eight_lines_declare_what_an_example_fills(self):
        """The rule tools/phase_index.py reads: a declaration further down is body text."""
        declaration = "Fills [templates/definition/prd.md](../templates/definition/prd.md)."
        self.assertEqual(journey_chain.declared_fill("\n" * 7 + declaration),
                         "templates/definition/prd.md")
        self.assertIsNone(journey_chain.declared_fill("\n" * 8 + declaration))

    def test_the_declared_template_decides_even_when_the_body_mentions_another_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            prd = repo / "examples" / "expense-copilot-prd.md"
            lines = prd.read_text(encoding="utf-8").split("\n")
            lines.insert(1, "Drafted once templates/discovery/problem-framing.md had closed.")
            edited = "\n".join(lines)
            prd.write_text(edited, encoding="utf-8")
            # The seed is the case the old rule got wrong: the first template path in the body.
            self.assertEqual(re.search(r"templates/[a-z]+/[a-z0-9-]+\.md", edited).group(0),
                             "templates/discovery/problem-framing.md")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertEqual(done.returncode, 0, done.stderr)
            record = out.read_text(encoding="utf-8")
            self.assertIn("| expense-copilot-prd.md | templates/definition/prd.md | "
                          "definition/prd.md |", record)
            # Nothing the record reports depends on that line, so it is the committed record.
            self.assertEqual(record, RECORD.read_text(encoding="utf-8"))

    def test_a_frameworks_declaration_is_stamped_where_its_stage_puts_it(self):
        """frameworks/ has no workspace folder of its own: the destination is read from the
        declared file's stage, DESIGN for the risk matrix, and an example carries no stage."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            shutil.copy2(REPO / "examples" / "example-risk-matrix.md",
                         repo / "examples" / "expense-copilot-risk-matrix.md")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("| expense-copilot-risk-matrix.md | frameworks/execution/risk-matrix.md "
                          "| architecture/risk-matrix.md |", out.read_text(encoding="utf-8"))

    def test_an_example_declaring_a_file_that_does_not_exist_stops_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            (repo / "examples" / "expense-copilot-stray.md").write_text(
                "# Stray\n\nFills [templates/definition/never-written.md]"
                "(../templates/definition/never-written.md).\n", encoding="utf-8")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertNotEqual(done.returncode, 0)
            self.assertIn("expense-copilot-stray.md declares it fills "
                          "templates/definition/never-written.md, which is not a file", done.stderr)
            self.assertFalse(out.exists())

    def test_two_examples_on_one_workspace_path_stop_the_run_naming_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            shutil.copy2(repo / "examples" / "expense-copilot-prd.md",
                         repo / "examples" / "expense-copilot-prd-copy.md")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertNotEqual(done.returncode, 0)
            for name in ("expense-copilot-prd.md", "expense-copilot-prd-copy.md",
                         "definition/prd.md"):
                self.assertIn(name, done.stderr)
            self.assertFalse(out.exists())

    # ------------------------------ the answers ------------------------------

    def test_a_quote_edited_out_of_its_document_stops_the_run_naming_the_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            framing = repo / "examples" / "expense-copilot-problem-framing.md"
            quote = journey_chain.ANSWERS["DISCOVER-1"]["quote"]
            text = framing.read_text(encoding="utf-8")
            self.assertIn(quote, text)
            framing.write_text(text.replace(quote, "Filers"), encoding="utf-8")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertNotEqual(done.returncode, 0)
            self.assertIn("DISCOVER-1: the quoted span is not in section", done.stderr)
            self.assertFalse(out.exists())

    def test_a_quote_found_only_outside_its_section_is_refused(self):
        """The quote is looked for in the section the answer names, not anywhere in the file."""
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            framing = root / "discovery" / "problem-framing.md"
            entry = journey_chain.ANSWERS["DISCOVER-1"]
            text = framing.read_text(encoding="utf-8")
            self.assertEqual(text.count(entry["quote"]), 1)
            # Cut from section 6, where the answer says it is, and set under section 3.
            moved = text.replace(entry["quote"], "Filers").replace(
                "## 3. Problem statement\n", "## 3. Problem statement\n\n%s.\n" % entry["quote"])
            framing.write_text(moved, encoding="utf-8")
            self.assertIn(entry["quote"], moved)
            with self.assertRaises(SystemExit) as caught:
                journey_chain.evidence_for(self.questions["DISCOVER-1"],
                                           "discovery/problem-framing.md", root)
            self.assertIn("DISCOVER-1: the quoted span is not in section "
                          "'6. Who feels it and how often'", str(caught.exception))

    def test_an_answer_cut_from_its_document_is_refused(self):
        """Otherwise the quote check could be met by cutting answer and quote from one span."""
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            entry = journey_chain.ANSWERS["DISCOVER-6"]
            with mock.patch.dict(journey_chain.ANSWERS,
                                 {"DISCOVER-6": dict(entry, answer=entry["quote"])}):
                with self.assertRaises(SystemExit) as caught:
                    journey_chain.evidence_for(self.questions["DISCOVER-6"],
                                               "discovery/discovery-document.md", root)
            self.assertIn("DISCOVER-6: the answer is a verbatim slice of "
                          "discovery/discovery-document.md", str(caught.exception))

    def test_a_question_with_no_written_answer_stops_the_run_naming_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_copy(Path(tmp))
            path = repo / "pmos" / "question_banks.json"
            contract = json.loads(path.read_text(encoding="utf-8"))
            define = next(bank for bank in contract["banks"] if bank["id"] == "define")
            define["questions"].append(dict(define["questions"][-1], id="DEFINE-13",
                                            handle="one question too many"))
            path.write_text(json.dumps(contract), encoding="utf-8")
            out = Path(tmp) / "record.md"
            done = run_chain(repo, out)
            self.assertNotEqual(done.returncode, 0)
            self.assertIn("DEFINE-13: no answer is written for it", done.stderr)
            self.assertFalse(out.exists())

    def test_an_answer_for_a_question_no_bank_asks_stops_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            with mock.patch.dict(journey_chain.ANSWERS,
                                 {"DEFINE-99": dict(journey_chain.ANSWERS["DEFINE-1"])}):
                with self.assertRaises(SystemExit) as caught:
                    journey_chain.plan_answers(root, self.contract)
            self.assertIn("answers DEFINE-99, which no Gate 1 to 3 bank asks", str(caught.exception))

    def test_a_question_whose_lands_in_the_workspace_lacks_needs_a_named_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            # The shipped case: DEFINE-7's register was never written, so it cites its fallback.
            cited, fallback = journey_chain.cite(self.questions["DEFINE-7"], root)
            self.assertEqual((cited, fallback), ("definition/prd.md", True))
            # A question with no lands_in document and no fallback is refused by id.
            with self.assertRaises(SystemExit) as caught:
                journey_chain.cite({"id": "DEFINE-13",
                                    "lands_in": "`definition/never-written.md` and STATE.md."}, root)
            self.assertIn("DEFINE-13", str(caught.exception))
            self.assertIn("definition/never-written.md", str(caught.exception))
            self.assertIn("it has no fallback", str(caught.exception))
            # A named fallback the workspace does not hold is no document to cite either.
            with mock.patch.dict(journey_chain.FALLBACKS, {"DEFINE-7": "definition/missing.md"}):
                with self.assertRaises(SystemExit) as caught:
                    journey_chain.cite(self.questions["DEFINE-7"], root)
            self.assertIn("DEFINE-7", str(caught.exception))
            self.assertIn("its fallback definition/missing.md is not in it either",
                          str(caught.exception))
            # A fallback outlives its reason only until the lands_in document appears.
            (root / "definition" / "assumptions-register.md").write_text("# Register\n",
                                                                           encoding="utf-8")
            with self.assertRaises(SystemExit) as caught:
                journey_chain.cite(self.questions["DEFINE-7"], root)
            self.assertIn("DEFINE-7", str(caught.exception))
            self.assertIn("stale", str(caught.exception))

    def test_a_repointed_source_is_refused_here_and_by_pmos(self):
        """pmos checks that a quote occurs in the file it cites; this generator checks that it
        sits in the section the answer names, which pmos does not read."""
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            question = self.questions["DISCOVER-1"]
            entry = journey_chain.ANSWERS["DISCOVER-1"]
            # A stamped artifact whose header names this answer's person with its date on one
            # line, so the interview claim check alone would pass it.
            elsewhere = "planning/product-strategy.md"
            text = (root / elsewhere).read_text(encoding="utf-8")
            self.assertIsNone(journey_chain.claim_problem("interview_claim", entry, text))
            self.assertNotIn(entry["quote"], text)
            with self.assertRaises(SystemExit) as caught:
                journey_chain.evidence_for(question, elsewhere, root)
            self.assertIn("DISCOVER-1: %s has no section headed" % elsewhere, str(caught.exception))
            evidence = journey_chain.evidence_for(question, "discovery/problem-framing.md", root)
            self.cli(["init", "--path", str(root), "--product-id", "repointed"])
            # Repointed at a file that lacks the quote, pmos refuses it too.
            refused = self.submit(root, "DISCOVER-1", entry["answer"], dict(evidence, source=elsewhere),
                                  "repointed")
            self.assertEqual(refused["outcome"]["status"], "challenge")
            self.assertIn("quote does not occur in %s" % elsewhere, refused["outcome"]["message"])
            # A quote that is in the cited file, but outside the section the answer names, is
            # refused here and accepted by pmos, which records it quote_verified.
            framing = root / "discovery" / "problem-framing.md"
            moved = framing.read_text(encoding="utf-8").replace(entry["quote"], "Filers").replace(
                "## 3. Problem statement\n", "## 3. Problem statement\n\n%s.\n" % entry["quote"])
            framing.write_text(moved, encoding="utf-8")
            with self.assertRaises(SystemExit):
                journey_chain.evidence_for(question, "discovery/problem-framing.md", root)
            accepted = self.submit(root, "DISCOVER-1", entry["answer"], evidence, "outside-its-section")
            self.assertEqual(accepted["outcome"]["status"], "accepted")
            after = self.cli(["status", "--path", str(root), "--product-id", "repointed"])
            self.assertEqual((after["quote_verified"], after["source_verified"], after["supplied_unverified"]),
                             (1, 0, 0))

    @staticmethod
    def cli(argv):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            pmos_main(argv + ["--json"])
        return json.loads(output.getvalue())

    def submit(self, root, question_id, answer, evidence, turn_id):
        status = self.cli(["status", "--path", str(root), "--product-id", "repointed"])
        self.assertEqual(status["question"]["id"], question_id)
        return self.cli(["answer", "--path", str(root), "--product-id", "repointed",
                         "--question-id", question_id, "--answer", answer,
                         "--evidence", json.dumps(evidence),
                         "--expected-revision", status["revision_token"], "--turn-id", turn_id])

    # ------------------------------ the evidence classes ------------------------------

    def test_an_interview_claim_needs_its_person_and_date_on_one_line_of_the_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            text = (root / "discovery" / "problem-framing.md").read_text(encoding="utf-8")
        entry = journey_chain.ANSWERS["DISCOVER-1"]
        self.assertIsNone(journey_chain.claim_problem("interview_claim", entry, text))
        # Priya Nair is named in section 7 and 2026-08-13 in the header, never on one line:
        # found separately, the two would not say who said it when.
        self.assertIn("Priya Nair", text)
        self.assertIn(entry["date"], text)
        for person, date in (("Hana Sato", entry["date"]),
                             (entry["person"], "2026-01-01"),
                             ("Priya Nair", entry["date"])):
            with self.subTest(person=person, date=date):
                self.assertEqual(
                    journey_chain.claim_problem("interview_claim",
                                                dict(entry, person=person, date=date), text),
                    "no line of it names %s together with %s" % (person, date))
        self.assertEqual(journey_chain.claim_problem(
            "interview_claim", {"quote": entry["quote"], "person": entry["person"]}, text),
            "the answer names no date")
        self.assertEqual(journey_chain.claim_problem(
            "interview_claim", {"quote": entry["quote"]}, text),
            "the answer names no person and no date")

    def test_a_named_commitment_needs_a_clause_in_which_that_person_says_yes(self):
        okafor = "Daniel Okafor"
        # One for each word of assent, from lines the expense copilot documents carry or could.
        for quote in ("Approved at Gate 2 by the business sponsor: Daniel Okafor, 2026-08-28",
                      "baseline and method agreed with Daniel Okafor, finance lead, 2026-08-12",
                      "Read and acknowledged by Daniel Okafor, business sponsor, on 2026-08-28",
                      "Daniel Okafor committed the finance join to 2026-10-09",
                      "signed by Maya Chen, Priya Nair and Daniel Okafor (V8)",
                      # the control for the negated sentence below: the same words, unnegated
                      "Daniel Okafor approved the list in writing"):
            with self.subTest(quote=quote):
                self.assertTrue(journey_chain.records_yes(quote, okafor))
        for quote in (
                # a yes from somebody else
                "Approved at Gate 2 by the product owner: Maya Chen, 2026-08-28",
                # the person, and no yes at all
                "All four rows escalate to the same person, Daniel Okafor.",
                # a table row: the yes is in one cell, the person in another
                "committed; delivered 2026-10-09 | Daniel Okafor, finance lead and sponsor",
                # one sentence records a yes, the next names the person
                "The list was approved. Daniel Okafor chairs the review.",
                # the same across a semicolon, and across a table cell
                "Daniel Okafor chairs the review; the list was approved",
                "approved | Daniel Okafor, finance lead",
                # a yes the person withheld
                "Daniel Okafor has not approved the list",
                "Daniel Okafor has not yet approved the list",
                "Daniel Okafor never agreed to the list",
                "No acknowledged reading by Daniel Okafor is on file",
                # a negation anywhere earlier in the clause, not only in the two words before
                "Daniel Okafor has not, in writing, approved the list",
                "Daniel Okafor hasn't approved the list",
                "Daniel Okafor hasn\u2019t, as of today, signed the list"):
            with self.subTest(quote=quote):
                self.assertFalse(journey_chain.records_yes(quote, okafor))

    def test_a_named_commitment_its_document_never_records_is_refused(self):
        """As this generator first filed them: three answers citing documents that name a
        person, filed as that person's commitment though no clause records one."""
        seeds = (("DEFINE-6", "definition/prd.md", "Daniel Okafor"),
                 ("DESIGN-2", "execution/dependency-register.md", "Daniel Okafor"),
                 ("DESIGN-5", "execution/dependency-register.md", "Priya Nair"))
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            for question_id, cited, person in seeds:
                question = self.questions[question_id]
                self.assertEqual(question["evidence_class"], "named_commitment")
                filed = {key: value for key, value in journey_chain.ANSWERS[question_id].items()
                         if key != "class"}
                filed["person"] = person
                self.assertIn(person, (root / cited).read_text(encoding="utf-8"))
                with self.subTest(question=question_id):
                    with mock.patch.dict(journey_chain.ANSWERS, {question_id: filed}):
                        with self.assertRaises(SystemExit) as caught:
                            journey_chain.evidence_for(question, cited, root)
                    message = str(caught.exception)
                    for part in (question_id, "named_commitment", cited, person):
                        self.assertIn(part, message)
            # The same question passes once its section records the sponsor's yes.
            prd = root / "definition" / "prd.md"
            yes = "Read and acknowledged by Daniel Okafor, business sponsor, on 2026-08-28"
            prd.write_text(prd.read_text(encoding="utf-8").replace(
                "## Out of scope\n", "## Out of scope\n\n%s.\n" % yes), encoding="utf-8")
            filed = {key: value for key, value in journey_chain.ANSWERS["DEFINE-6"].items()
                     if key != "class"}
            filed.update(person="Daniel Okafor", quote=yes)
            with mock.patch.dict(journey_chain.ANSWERS, {"DEFINE-6": filed}):
                evidence = journey_chain.evidence_for(self.questions["DEFINE-6"],
                                                      "definition/prd.md", root)
            self.assertEqual((evidence["class"], evidence["person"], evidence["quote"]),
                             ("named_commitment", "Daniel Okafor", yes))

    def test_the_answers_above_their_class_cite_sections_with_no_yes_in_them(self):
        """Why DEFINE-6, DESIGN-2 and DESIGN-5 are artifact evidence: if their sections gain a
        yes from a person they name, this fails, and each can be a named commitment again."""
        rows = record_rows()
        stronger = {question_id for question_id, (klass, _cited, _section) in rows.items()
                    if "(asks " in klass}
        self.assertEqual(stronger, EXPECTED_STRONGER)
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            for question_id in sorted(EXPECTED_STRONGER):
                klass, cited, section = rows[question_id]
                with self.subTest(question=question_id):
                    self.assertEqual(klass, "artifact (asks named_commitment)")
                    self.assertNotIn("person", journey_chain.ANSWERS[question_id])
                    path = cited[len(FALLBACK_PREFIX):] if cited.startswith(FALLBACK_PREFIX) else cited
                    body = journey_chain.section_body((root / path).read_text(encoding="utf-8"),
                                                      section)
                    # DEFINE-6's Out of scope names nobody; the register names two of the cast.
                    for person in CAST:
                        self.assertFalse(any(journey_chain.records_yes(line, person)
                                             for line in body.split("\n")), person)

    def test_no_answer_is_a_slice_of_the_document_it_cites_and_every_quote_is(self):
        rows = record_rows()
        self.assertEqual(sorted(rows), sorted(self.questions))
        with tempfile.TemporaryDirectory() as tmp:
            root = built_workspace(Path(tmp))
            for question_id, (_klass, cited, section) in rows.items():
                with self.subTest(question=question_id):
                    path = cited[len(FALLBACK_PREFIX):] if cited.startswith(FALLBACK_PREFIX) else cited
                    text = (root / path).read_text(encoding="utf-8")
                    entry = journey_chain.ANSWERS[question_id]
                    self.assertNotIn(entry["answer"], text)
                    self.assertIn(entry["quote"], text)
                    self.assertEqual(entry["section"], section)

    def test_only_the_named_questions_fall_back_and_every_other_cites_its_lands_in(self):
        rows = record_rows()
        fallbacks = {question_id for question_id, (_klass, cited, _section) in rows.items()
                     if cited.startswith(FALLBACK_PREFIX)}
        self.assertEqual(fallbacks, EXPECTED_FALLBACKS)
        for question_id, (_klass, cited, _section) in rows.items():
            if question_id in fallbacks:
                continue
            with self.subTest(question=question_id):
                self.assertIn(cited, LANDS_IN_MD.findall(self.questions[question_id]["lands_in"]))

    # ------------------------------ the record ------------------------------

    def test_the_record_splits_the_evidence_and_says_what_each_column_checks(self):
        record = RECORD.read_text(encoding="utf-8")
        header = next(line for line in record.split("\n") if line.startswith("| Gate | Bank |"))
        for title in ("pmos quote_verified", "pmos source_verified", "pmos supplied_unverified",
                      "Quote found in the section its answer names (checked by "
                      "tools/journey_chain.py, not by pmos)", "Artifacts bound to the approval"):
            self.assertIn(title, header)
        self.assertNotIn("Evidence citing a workspace file", record)
        per_gate = {"discover": 9, "define": 12, "design": 8}
        self.assertEqual(gates_column(record, "Questions answered"), per_gate)
        # Every answer quotes its document, and pmos found every quote in the file cited.
        self.assertEqual(gates_column(record, "pmos quote_verified"), per_gate)
        # pmos reads the cited file now, where it used to read nothing inside it.
        self.assertNotIn("reads nothing inside that file", record)
        self.assertIn("the section column equals the answered column by construction", record)
        self.assertIn("29 quote_verified, 0 source_verified, 0 supplied_unverified", record)
        self.assertEqual(len(record_rows()), 29)

    def test_the_record_reads_its_evidence_bound_columns_and_handoff_line_from_the_runtime(self):
        """The committed record reads 9/12/8 quote_verified because every answer quotes its
        document. A generator that printed those figures without asking the runtime would write
        the same record, so only a run whose evidence and workspace differ tells the two apart:
        here Gate 1's answers quote nothing, Gate 3's cite an interview id, and one more Gate 1
        artifact is stamped into the workspace before the gates are proved."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copied = journey_chain.build_workspace(root)
            plan = journey_chain.plan_answers(root, self.contract)
            for question_id, (cited, fallback, evidence) in list(plan.items()):
                if question_id.startswith("DISCOVER-"):
                    evidence = {key: value for key, value in evidence.items() if key != "quote"}
                elif question_id.startswith("DESIGN-"):
                    evidence = {key: value for key, value in evidence.items() if key != "quote"}
                    evidence["source"] = "interview-001"
                plan[question_id] = (cited, fallback, evidence)
            guide = root / "discovery" / "interview-guide.md"
            guide.write_text(workspace.stamp_artifact("# Interview guide\n",
                                                      "templates/discovery/interview-guide.md",
                                                      journey_chain.SLUG), encoding="utf-8")
            gates, answers, before = journey_chain.drive_gates(root, plan)
            after, stale = journey_chain.staleness(root, before)
            record = journey_chain.generate_markdown(copied, gates, answers, before, after, stale)
        self.assertEqual(gates_column(record, "pmos quote_verified"),
                         {"discover": 0, "define": 12, "design": 0})
        self.assertEqual(gates_column(record, "pmos source_verified"),
                         {"discover": 9, "define": 0, "design": 0})
        self.assertEqual(gates_column(record, "pmos supplied_unverified"),
                         {"discover": 0, "define": 0, "design": 8})
        self.assertEqual(gates_column(record, "Artifacts bound to the approval"),
                         {"discover": 4, "define": 5, "design": 6})
        self.assertIn("Evidence the package reports, every bank counted: 12 quote_verified, "
                      "9 source_verified, 8 supplied_unverified.", record)
        self.assertIn("pmos recorded 12 of the 29 answers here quote_verified.", record)


class JourneyRunRecordTests(unittest.TestCase):
    """tools/journey_record.py, and the documents that count or cite the two records."""

    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract()

    def test_the_run_record_reads_its_evidence_columns_from_the_runtime(self):
        """The committed record reads every answer supplied_unverified and no artifact bound,
        because its answers cite an interview id and its workspace holds no artifact. A
        generator that printed those figures without asking the runtime would write the same
        record, so only a run whose evidence differs can tell the two apart: here DEFINE's
        answers quote a workspace file, DISCOVER's and DESIGN's cite one without quoting, and
        one artifact names Gate 1."""
        real_answer, real_bank = journey_record.answer, journey_record.process_bank

        def answer(folder, evidence, token, turn_id, question_id):
            # gate-probe.txt is written into the workspace before the first question, and
            # notes.md before the first DEFINE question. BUILD to OPERATE keep the interview id.
            if question_id.startswith("DEFINE-"):
                evidence = dict(evidence, source="notes.md", quote="the payout batch fails every Monday")
            elif question_id.startswith(("DISCOVER-", "DESIGN-")):
                evidence = dict(evidence, source="gate-probe.txt")
            return real_answer(folder, evidence, token, turn_id, question_id)

        def process_bank(folder, prefix):
            if prefix == "discover":
                target = Path(folder, "discovery", "problem-framing.md")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(workspace.stamp_artifact(
                    "# Problem framing\n", "templates/discovery/problem-framing.md", "checkout"),
                    encoding="utf-8")
            if prefix == "define":
                Path(folder, "notes.md").write_text("Mina said the payout batch fails every Monday.\n",
                                                    encoding="utf-8")
            return real_bank(folder, prefix)

        with mock.patch.object(journey_record, "answer", answer), \
                mock.patch.object(journey_record, "process_bank", process_bank):
            text = journey_record.generate_record_text()
        per_bank = {bank["id"]: len(bank["questions"]) for bank in self.contract["banks"]}

        def only(*bank_ids):
            return {bank_id: count if bank_id in bank_ids else 0 for bank_id, count in per_bank.items()}

        self.assertEqual(gates_column(text, "pmos quote_verified"), only("define"))
        self.assertEqual(gates_column(text, "pmos source_verified"), only("discover", "design"))
        self.assertEqual(gates_column(text, "pmos supplied_unverified"),
                         only("build", "deliver", "operate"))
        self.assertEqual(gates_column(text, "Artifacts bound to the approval"),
                         {bank_id: int(bank_id == "discover") for bank_id in per_bank})
        total = sum(per_bank.values())
        citing = sum(only("discover", "define", "design").values())
        result = next(line for line in text.split("\n") if line.startswith("The runtime ended"))
        self.assertIn("%d of the %d cite a file pmos found inside the workspace, and 1 of the 6 "
                      "approvals bound a workspace artifact" % (citing, total), result)
        self.assertIn("[journey-chain.md](journey-chain.md)", result)

    def test_the_documents_that_count_the_journeys_use_the_contract_s_counts(self):
        total = sum(len(bank["questions"]) for bank in self.contract["banks"])
        early = sum(len(bank["questions"]) for bank in self.contract["banks"] if bank["gate"] <= 3)
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"command line answering (\d+) questions", readme), [str(total)])
        index = (REPO / "examples" / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"answering all (\d+) questions", index), [str(total)])
        self.assertEqual(re.findall(r"every one of the (\d+) questions in Gates 1 to 3", index),
                         [str(early)])
        result = next(line for line in RUN_RECORD.read_text(encoding="utf-8").split("\n")
                      if line.startswith("The runtime ended"))
        self.assertIn("with %d answers accepted" % total, result)

    def test_stage_gates_cites_for_artifact_binding_the_record_that_shows_it(self):
        text = (REPO / "os" / "STAGE-GATES.md").read_text(encoding="utf-8")
        worth = text.split("\n## What a gate is worth\n", 1)[1].split("\n## ", 1)[0]
        binding = [sentence for sentence in re.split(r"(?<=\.) ", worth)
                   if "artifact-revision binding" in sentence]
        self.assertEqual(len(binding), 1, binding)
        self.assertEqual(re.findall(r"\(\.\./examples/([a-z-]+\.md)\)", binding[0]),
                         ["journey-chain.md"])
        # The two records bear that out: the chain's approvals bind artifacts, the run's bind
        # none, which the same paragraph says of the run.
        chain = gates_column(RECORD.read_text(encoding="utf-8"), "Artifacts bound to the approval")
        run = gates_column(RUN_RECORD.read_text(encoding="utf-8"), "Artifacts bound to the approval")
        self.assertTrue(all(chain.values()), chain)
        self.assertEqual(set(run.values()), {0})
        self.assertIn("that run carries no workspace artifacts, so none of its approvals binds one",
                      worth)
        # And Gate 2's inputs name the ids the Conductor asks for the planning set by.
        define = next(bank for bank in self.contract["banks"] if bank["id"] == "define")
        planning = [question["id"] for question in define["questions"]
                    if any(path.startswith("planning/")
                           for path in LANDS_IN_MD.findall(question["lands_in"]))]
        gate_two = text.split("\n## Gate 2:", 1)[1].split("\n## ", 1)[0]
        self.assertIn("as %s to %s" % (planning[0], planning[-1]), gate_two)


if __name__ == "__main__":
    unittest.main()
