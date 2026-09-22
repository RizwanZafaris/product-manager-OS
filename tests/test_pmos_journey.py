"""The runtime half of the W9h fictional journey test.

Every approval, actor, date and piece of evidence below is fictional: it is
invented for this test alone, lives only inside the temporary workspace this
test creates and destroys, and proves nothing about any real product,
sponsor or reviewer. No assertion here should be read as a claim about a real
gate approval.

This module drives the whole journey, from the understood problem (Gate 1)
through a development-ready handoff (Gate 3), through pmos.cli.main only: no
Store, Conductor or other internal object is touched directly. A temporary
workspace holds one product, id "ledgerline", and every working copy this
test writes carries its own artifact block and a body whose first line is
literally "FICTIONAL TEST DATA".

The static half of W9h checks the real example files under examples/: every
number, date and id there is a claim about the fiction this repository has
already committed to in expense-copilot-journey.md and ledgerline-journey.md,
never invented fresh by a test. It was added by W9f, once the fourteenth
step, the development handoff, existed to check.
"""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.cli import main
from pmos.handoff import SECTIONS as HANDOFF_SECTIONS

PRODUCT_ID = "ledgerline"

# The runtime's only authorized gate approver (pmos/banks.py LOCAL_APPROVERS).
# "requester_id" carries this test's fictional sponsor instead: the conductor
# requires the approving actor and the requesting actor to differ, so the
# fictional identity goes on the field that is free to carry one.
_LOCAL_APPROVER = "local-reviewer"
_FICTIONAL_SPONSOR = "fictional-sponsor"

# ------------------------------ static half ------------------------------
#
# The fourteen-step internal-v1 chain W9-DESIGN decision 4 lays out: the
# template each step fills, the example that fills it, and the date that
# step's own artifact carries (its Date, Last updated, Last entry or Last
# reviewed field; Prepared for the handoff). decision-log.md's date is its
# Last entry, not its earlier Started field: Started reaches back to Gate 1,
# but this step sits between the data model and API contract before it and
# the two registers after it, and Last entry is where it actually sits in
# the chain. Every date here is ILLUSTRATIVE and traces to
# expense-copilot-journey.md's V-rows.
REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"

JOURNEY_STEPS = (
    ("templates/discovery/problem-framing.md",
     "expense-copilot-problem-framing.md", "2026-08-13"),
    ("templates/discovery/discovery-document.md",
     "expense-copilot-discovery.md", "2026-08-14"),
    ("templates/planning/vision.md",
     "expense-copilot-vision.md", "2026-08-18"),
    ("templates/planning/product-strategy.md",
     "expense-copilot-product-strategy.md", "2026-08-21"),
    ("templates/planning/roadmap.md",
     "expense-copilot-roadmap.md", "2026-08-25"),
    ("templates/definition/prd.md",
     "expense-copilot-prd.md", "2026-08-28"),
    ("templates/definition/acceptance-criteria.md",
     "expense-copilot-acceptance-criteria.md", "2026-08-28"),
    ("templates/architecture/adr.md",
     "expense-copilot-adr.md", "2026-09-03"),
    ("templates/architecture/data-model.md",
     "expense-copilot-data-model.md", "2026-09-05"),
    ("templates/architecture/api-contract.md",
     "expense-copilot-api-contract.md", "2026-09-05"),
    ("templates/execution/decision-log.md",
     "expense-copilot-decision-log.md", "2026-09-08"),
    ("templates/execution/dependency-register.md",
     "expense-copilot-dependency-register.md", "2026-09-08"),
    ("templates/execution/risk-register.md",
     "expense-copilot-risk-register.md", "2026-09-08"),
    ("templates/architecture/development-handoff.md",
     "expense-copilot-development-handoff.md", "2026-09-10"),
)

# Every step above except the discovery document and the PRD, which already
# existed before W9 and only had their company name corrected (W9a). The
# figure-reuse check applies to these twelve: the ones this journey actually
# wrote.
NEW_EXAMPLES = tuple(example for _template, example, _date in JOURNEY_STEPS
                     if example not in ("expense-copilot-discovery.md",
                                        "expense-copilot-prd.md"))

JOURNEY_FILE = "expense-copilot-journey.md"
DATA_SHEETS = (JOURNEY_FILE, "ledgerline-journey.md")

# An example names the template it fills in one of these two phrasings, the
# same pair tools/phase_index.py's own FILLS tuple recognizes.
FILLS_PHRASES = ("Fills [", "Produced with [")

# Standard protocol and format constants a filled artifact may cite without
# tracing them to either data sheet: they name a wire format or a standard,
# not a fact about Ledgerline. expense-copilot-api-contract.md's error table
# cites HTTP status codes; expense-copilot-data-model.md's data dictionary
# cites the two ISO standards its currency and timestamp fields follow.
STANDARD_NUMERALS = frozenset((
    "200", "400", "401", "403", "404", "409", "422", "429", "500",
    "4217", "8601",
))

_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\n]+)\)")
_SECTION_RE = re.compile(r"^##\s*(\d\.\s+.*)$")
_NUMERAL_RE = re.compile(r"\d+")
_THOUSANDS_COMMA_RE = re.compile(r"(?<=\d),(?=\d)")


def _link_targets(text):
    """Every link target in text, external links and bare anchors dropped.

    Mirrors pmos/handoff.py's own _link_target: an angle-bracketed target is
    unwrapped, a target followed by a title is cut at the first space, and
    an in-page anchor is stripped from whatever remains.
    """
    for line in text.split("\n"):
        for match in _LINK_RE.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1].strip()
            if " " in target:
                target = target.split(" ", 1)[0]
            target = target.split("#", 1)[0]
            if not target or target.startswith("#"):
                continue
            if target.lower().startswith(("http:", "https:", "mailto:")):
                continue
            yield target


def _numerals(text):
    """Every maximal run of digits in text, thousands commas ignored.

    "40,000" and "40000" both read as the numerals "40" and "000": a comma
    between two digits is a grouping mark, not a boundary, so it is removed
    before runs are collected. This keeps the check agreeing with itself
    however a figure happens to be punctuated in the file that carries it.
    """
    return set(_NUMERAL_RE.findall(_THOUSANDS_COMMA_RE.sub("", text)))


class JourneyRuntimeTests(unittest.TestCase):
    """Gate 1 to a development-ready Gate 3 handoff, driven by pmos.cli.main."""

    # ------------------------------ CLI helpers ------------------------------

    def run_cli(self, argv: list) -> tuple:
        """Run pmos.cli.main(argv) and return (exit code, parsed JSON)."""
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(list(argv) + ["--json"])
        return code, json.loads(buffer.getvalue())

    def status(self, folder: str) -> dict:
        code, result = self.run_cli(["status", "--path", folder, "--product-id", PRODUCT_ID])
        self.assertEqual(code, 0, result)
        return result

    def answer_bank(self, folder: str, prefix: str, source: str | None = None,
                    quote: str | None = None) -> dict:
        """Answer every open question of the current bank with fictional evidence.

        The evidence class is always observed_behavior: it is the strongest
        rung on the conductor's evidence ladder, so it satisfies every
        question regardless of that question's own required class. Without
        a source the evidence names a visibly fictional one that is never a
        real file, so it is recorded as supplied rather than verified; that
        is fine, since acceptance never requires verification. With one, it
        names that workspace file, which pmos records as source_verified,
        or, when a quote from that file comes with it, as quote_verified.
        """
        for _ in range(20):
            status = self.status(folder)
            if status["interview"] != "question":
                return status
            question_id = status["question"]["id"]
            evidence = {"class": "observed_behavior",
                        "source": source or "fictional-test-evidence-" + question_id.lower(),
                        "date": "2026-08-13", "location": "fictional-test-interview"}
            if quote:
                evidence["quote"] = quote
            code, result = self.run_cli([
                "answer", "--path", folder, "--product-id", PRODUCT_ID,
                "--question-id", question_id,
                "--answer", "FICTIONAL TEST DATA: a fictional answer for " + question_id,
                "--evidence", json.dumps(evidence),
                "--expected-revision", status["revision_token"],
                "--turn-id", prefix + "-" + question_id])
            self.assertEqual((code, result["outcome"]["status"]), (0, "accepted"), result)
        self.fail("the %s bank did not finish answering" % prefix)

    def write_working_copy(self, folder: str, rel_path: str, artifact_id: str, phase: str,
                           gate: int, depends_on: list, template: str, body: str) -> Path:
        """Write a minimal working copy carrying its artifact block.

        Modeled on the write_artifact helper in
        tests/test_pmos_cli.py::CliTests (see
        test_revision_bound_approvals_hold_through_the_cli), kept local here
        so this module never imports from another test module.
        """
        path = Path(folder, rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        block = (
            "---\n"
            "artifact_id: %s\n"
            "phase: %s\n"
            "gate: %d\n"
            "status: draft\n"
            "depends_on: %s\n"
            "template: %s\n"
            "---\n"
            "%s\n"
        ) % (artifact_id, phase, gate, json.dumps(depends_on), template, body)
        path.write_text(block, encoding="utf-8")
        return path

    def approve_gate(self, folder: str, token: str, turn_id: str, bank_id: str) -> tuple:
        """Approve bank_id's gate with a real local proof file and fictional names.

        The proof file's content visibly names it as fictional test data; its
        hash is real, because the runtime's gate verifier checks the bytes on
        disk, but what those bytes say is invented for this test alone. Each
        bank gets its own proof file, never rewritten afterward: the
        conductor re-verifies every approved gate's proof source on every
        later turn, so reusing one file across gates would stale the earlier
        approval as soon as a later one overwrote it.
        """
        proof_name = "fictional-gate-approval-%s.txt" % bank_id
        proof_path = Path(folder, proof_name)
        proof_bytes = ("FICTIONAL TEST DATA: %s requested a fictional approval of the %s "
                      "gate for this test only.\n" % (_FICTIONAL_SPONSOR, bank_id)).encode("utf-8")
        proof_path.write_bytes(proof_bytes)
        evidence = {
            "source": proof_name,
            "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
            "actor_id": _LOCAL_APPROVER,
            "requester_id": _FICTIONAL_SPONSOR,
            "decision": "approved",
            "approved_at": "2026-09-04T00:00:00Z",
        }
        return self.run_cli(["gate", "--path", folder, "--product-id", PRODUCT_ID,
                             "--bank-id", bank_id, "--evidence", json.dumps(evidence),
                             "--expected-revision", token, "--turn-id", turn_id])

    def handoff(self, folder: str) -> tuple:
        return self.run_cli(["handoff", "--path", folder, "--product-id", PRODUCT_ID])

    def drive_to_gate_three(self, folder: str, sources: dict, quotes: dict | None = None) -> None:
        """Steps 1 to 3: init, write the working copies, answer and approve Gates 1 to 3.

        sources maps each bank to the evidence source its answers name: a
        workspace file, or free text, or None for the fictional default.
        quotes maps a bank to words its answers quote from that source.
        """
        quotes = quotes or {}
        # 1. pmos init.
        code, result = self.run_cli(["init", "--path", folder, "--product-id", PRODUCT_ID])
        self.assertEqual((code, result["ok"]), (0, True), result)

        # 2. Gate 1: problem framing, answered and approved by a fictional sponsor.
        self.write_working_copy(
            folder, "discovery/problem-framing.md", "ledgerline/discovery/problem-framing",
            "DISCOVER", 1, [], "templates/discovery/problem-framing.md",
            "FICTIONAL TEST DATA\nA minimal fictional problem framing, invented for this test.\n")
        status = self.answer_bank(folder, "discover", sources.get("discover"), quotes.get("discover"))
        code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-1", "discover")
        self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

        # 2. Gate 2: vision, product strategy, roadmap and PRD, each depending
        # on the artifact before it, all answered and approved together.
        self.write_working_copy(
            folder, "planning/vision.md", "ledgerline/planning/vision", "DEFINE", 2,
            ["ledgerline/discovery/problem-framing"], "templates/planning/vision.md",
            "FICTIONAL TEST DATA\nA minimal fictional vision, invented for this test.\n")
        self.write_working_copy(
            folder, "planning/product-strategy.md", "ledgerline/planning/product-strategy",
            "DEFINE", 2, ["ledgerline/planning/vision"], "templates/planning/product-strategy.md",
            "FICTIONAL TEST DATA\nA minimal fictional product strategy, invented for this test.\n")
        self.write_working_copy(
            folder, "planning/roadmap.md", "ledgerline/planning/roadmap", "DEFINE", 2,
            ["ledgerline/planning/product-strategy"], "templates/planning/roadmap.md",
            "FICTIONAL TEST DATA\nA minimal fictional roadmap, invented for this test.\n")
        self.write_working_copy(
            folder, "definition/prd.md", "ledgerline/definition/prd", "DEFINE", 2,
            ["ledgerline/planning/roadmap"], "templates/definition/prd.md",
            "FICTIONAL TEST DATA\nA minimal fictional PRD, invented for this test.\n")
        status = self.answer_bank(folder, "define", sources.get("define"), quotes.get("define"))
        code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-2", "define")
        self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

        # 2. Gate 3: a data model, an API contract and the development handoff
        # itself, which fills all nine sections (requirement 3 below).
        self.write_working_copy(
            folder, "architecture/data-model.md", "ledgerline/architecture/data-model",
            "DESIGN", 3, ["ledgerline/definition/prd"], "templates/architecture/data-model.md",
            "FICTIONAL TEST DATA\nA minimal fictional data model, invented for this test.\n")
        self.write_working_copy(
            folder, "architecture/api-contract.md", "ledgerline/architecture/api-contract",
            "DESIGN", 3, ["ledgerline/architecture/data-model"],
            "templates/architecture/api-contract.md",
            "FICTIONAL TEST DATA\nA minimal fictional API contract, invented for this test.\n")
        handoff_body = "\n".join([
            "FICTIONAL TEST DATA",
            "A minimal fictional development handoff, invented for this test.",
            "",
            "## 1. Problem",
            "",
            "Link: [problem framing](../discovery/problem-framing.md)",
            "",
            "## 2. Vision and strategy",
            "",
            "Link: [vision](../planning/vision.md)",
            "Link: [product strategy](../planning/product-strategy.md)",
            "",
            "## 3. Outcomes and success measures",
            "",
            "Link: [roadmap](../planning/roadmap.md)",
            "",
            "## 4. Scope and exclusions",
            "",
            "Link: [PRD](../definition/prd.md)",
            "",
            "## 5. Requirements and acceptance criteria",
            "",
            "Link: [PRD](../definition/prd.md)",
            "",
            "## 6. Evidence and decisions",
            "",
            "Link: [product strategy](../planning/product-strategy.md)",
            "",
            "## 7. Dependencies",
            "",
            "Link: [roadmap](../planning/roadmap.md)",
            "",
            "## 8. Interface and data contracts",
            "",
            "Link: [data model](data-model.md)",
            "Link: [API contract](api-contract.md)",
            "",
            "## 9. Unresolved risks and constraints",
            "",
            "Link: [API contract](api-contract.md)",
        ])
        self.write_working_copy(
            folder, "architecture/development-handoff.md",
            "ledgerline/architecture/development-handoff", "DESIGN", 3,
            ["ledgerline/architecture/api-contract"],
            "templates/architecture/development-handoff.md", handoff_body)
        status = self.answer_bank(folder, "design", sources.get("design"), quotes.get("design"))
        code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-3", "design")
        self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

    # --------------------------------- the tests ---------------------------------

    def test_the_journey_reaches_a_development_ready_handoff_then_a_gate_one_edit_stales_it(self):
        with TemporaryDirectory() as folder:
            # Each bank's answers cite a working copy that exists when they are given, and
            # Gate 1's also quote it, so the three banks' evidence reads differently.
            self.drive_to_gate_three(folder, {"discover": "discovery/problem-framing.md",
                                              "define": "definition/prd.md",
                                              "design": "architecture/data-model.md"},
                                     {"discover": "A minimal fictional problem framing"})

            # 4. pmos handoff now reports a development-ready package.
            code, package = self.handoff(folder)
            self.assertEqual(code, 0, package)
            self.assertTrue(package["development_ready"], package)
            self.assertEqual(package["missing"], [])
            self.assertEqual(package["evidence"],
                             {"quote_verified": 9, "source_verified": 20, "supplied_unverified": 0})
            self.assertEqual(package["evidence_by_gate"], {
                "1": {"quote_verified": 9, "source_verified": 0, "supplied_unverified": 0},
                "2": {"quote_verified": 0, "source_verified": 12, "supplied_unverified": 0},
                "3": {"quote_verified": 0, "source_verified": 8, "supplied_unverified": 0}})

            status = self.status(folder)
            index = json.loads(Path(folder, "handoff/context-index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["source_revision"], status["revision_token"])

            context = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("Development-ready: yes", context)
            lines = context.split("\n")
            figure = lines[lines.index("Development-ready: yes") + 1]
            self.assertIn("29 of 29", figure)
            # One line per gate, each with that gate's own figures: a line dropped, or one
            # gate's figures printed for another, fails here.
            self.assertEqual(self.gate_evidence_lines(context), [
                "- Gate 1 (discover): 9 quote_verified, 0 source_verified, 0 supplied_unverified",
                "- Gate 2 (define): 0 quote_verified, 12 source_verified, 0 supplied_unverified",
                "- Gate 3 (design): 0 quote_verified, 8 source_verified, 0 supplied_unverified"])
            for gate_number, bank_id in ((1, "discover"), (2, "define"), (3, "design")):
                self.assertIn("Gate %d (%s)" % (gate_number, bank_id), context)
            self.assertEqual(context.count("local attestation"), 3)

            # 5. Editing the Gate 1 working copy stales its approval.
            self.write_working_copy(
                folder, "discovery/problem-framing.md", "ledgerline/discovery/problem-framing",
                "DISCOVER", 1, [], "templates/discovery/problem-framing.md",
                "FICTIONAL TEST DATA\nA changed fictional problem framing, invented for this test.\n")
            code, package = self.handoff(folder)
            self.assertEqual(code, 1, package)
            self.assertFalse(package["development_ready"], package)
            self.assertIn("Gate 1 approval is stale", package["missing"])

            status = self.status(folder)
            self.assertIn("discover", [stale["bank_id"] for stale in status["stale_banks"]])

    def test_a_handoff_whose_answers_cite_no_workspace_file_is_still_development_ready(self):
        """Verification is reported and gates nothing: the same journey, every answer
        citing an interview id instead of a file, reaches the same verdict."""
        with TemporaryDirectory() as folder:
            self.drive_to_gate_three(folder, dict.fromkeys(("discover", "define", "design"),
                                                           "interview-001"))
            code, package = self.handoff(folder)
            self.assertEqual(code, 0, package)
            self.assertTrue(package["development_ready"], package)
            self.assertEqual(package["missing"], [])
            self.assertEqual(package["evidence"],
                             {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 29})
            context = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            lines = context.split("\n")
            self.assertIn("0 of 29", lines[lines.index("Development-ready: yes") + 1])
            self.assertEqual(self.gate_evidence_lines(context), [
                "- Gate 1 (discover): 0 quote_verified, 0 source_verified, 9 supplied_unverified",
                "- Gate 2 (define): 0 quote_verified, 0 source_verified, 12 supplied_unverified",
                "- Gate 3 (design): 0 quote_verified, 0 source_verified, 8 supplied_unverified"])

    @staticmethod
    def gate_evidence_lines(context: str) -> list:
        """The per-gate lines of CONTEXT.md's Evidence section, in order."""
        section = context.split("\n## Evidence\n", 1)[1].split("\n## ", 1)[0]
        return [line for line in section.split("\n") if line.startswith("- Gate ")]

    # ------------------------------ static half ------------------------------
    #
    # These five checks read the real files under examples/ rather than a
    # temporary workspace. Nothing here is fictional test data; these are
    # claims about the repository's own committed fiction, checked against
    # itself.

    def test_static_each_step_example_exists_and_names_its_template(self):
        """W9-DESIGN decision 7: each journey step's example exists and
        names its template on its third line."""
        for template_rel, example_rel, _date in JOURNEY_STEPS:
            path = EXAMPLES / example_rel
            self.assertTrue(path.is_file(), "%s does not exist" % path)
            lines = path.read_text(encoding="utf-8").split("\n")
            self.assertGreaterEqual(len(lines), 3,
                                    "%s has fewer than three lines" % example_rel)
            third_line = lines[2]
            needles = ["%s%s]" % (phrase, template_rel) for phrase in FILLS_PHRASES]
            self.assertTrue(
                any(needle in third_line for needle in needles),
                "%s's third line does not name %s: %r"
                % (example_rel, template_rel, third_line))

    def test_static_every_relative_link_in_the_journey_files_resolves(self):
        """W9-DESIGN decision 7: every relative link in the journey's files
        resolves. A link counts only if it names a real, non-symlink file
        inside the workspace, the same rule pmos/handoff.py applies to a
        development handoff's own links."""
        files = (JOURNEY_FILE,) + tuple(example for _t, example, _d in JOURNEY_STEPS)
        repo_resolved = REPO.resolve()
        for rel in files:
            path = EXAMPLES / rel
            text = path.read_text(encoding="utf-8")
            for target in _link_targets(text):
                candidate = (EXAMPLES / target).resolve()
                try:
                    candidate.relative_to(repo_resolved)
                except ValueError:
                    self.fail("%s links %s, which resolves outside the repository"
                             % (rel, target))
                self.assertTrue(
                    candidate.is_file() and not candidate.is_symlink(),
                    "%s links %s, which does not resolve to a real, non-symlink file"
                    % (rel, target))

    def test_static_dates_increase_along_the_chain(self):
        """W9-DESIGN decision 7: dates increase along the chain.

        Several steps share a date: vision, product strategy and roadmap are
        each drafted on their own day but all approved at the same Gate 2
        sitting as the PRD and the acceptance criteria (2026-08-28), and the
        data model, the API contract, the two registers and the decision
        log's own last entry cluster on 2026-09-05 and 2026-09-08. "Increase"
        is read as never going backward, not as a strict inequality: a tie
        is two artifacts from the same sitting, not a chain out of order.
        """
        previous_date, previous_example = None, None
        for _template, example, date_str in JOURNEY_STEPS:
            year, month, day = (int(part) for part in date_str.split("-"))
            current_date = date(year, month, day)
            if previous_date is not None:
                self.assertLessEqual(
                    previous_date, current_date,
                    "%s (%s) is dated before %s (%s)"
                    % (example, date_str, previous_example, previous_date.isoformat()))
            previous_date, previous_example = current_date, example

    def test_static_handoff_sections_link_an_existing_journey_file_with_no_gap_lines(self):
        """W9-DESIGN decision 7: each of the handoff example's nine sections
        links an existing journey file, and none has a Gap: line.

        Sections are read by their own heading boundaries here, not by
        pmos/handoff.py's parser, which (by design, per templates/architecture
        /development-handoff.md's own comment) reads everything after
        section 9's heading, the Development-ready check included, as
        section 9. That quirk matters for how the file is written; it is not
        what this check is verifying, which is the file's own authored
        structure, section by section.
        """
        path = EXAMPLES / "expense-copilot-development-handoff.md"
        lines = path.read_text(encoding="utf-8").split("\n")
        boundaries = [index for index, line in enumerate(lines) if line.startswith("## ")]
        boundaries.append(len(lines))

        sections = {}
        for start, end in zip(boundaries, boundaries[1:]):
            match = _SECTION_RE.match(lines[start].strip())
            if match:
                sections[match.group(1).strip()] = lines[start + 1:end]

        repo_resolved = REPO.resolve()
        for title in HANDOFF_SECTIONS:
            self.assertIn(title, sections,
                          "expense-copilot-development-handoff.md has no ## %s heading" % title)
            body = sections[title]
            has_resolving_link = False
            for line in body:
                stripped = line.lstrip()
                if stripped.startswith("- "):
                    stripped = stripped[2:].lstrip()
                self.assertFalse(
                    stripped.startswith("Gap:"),
                    "expense-copilot-development-handoff.md section %s carries a Gap: line"
                    % title)
                for target in _link_targets(line):
                    candidate = (EXAMPLES / target).resolve()
                    try:
                        candidate.relative_to(repo_resolved)
                    except ValueError:
                        continue
                    if candidate.is_file() and not candidate.is_symlink():
                        has_resolving_link = True
            self.assertTrue(
                has_resolving_link,
                "expense-copilot-development-handoff.md section %s links no existing journey file"
                % title)

    def test_static_every_numeral_in_the_new_files_appears_on_one_of_the_two_data_sheets(self):
        """W9-DESIGN decision 7: every numeral in the new files appears in
        one of the two data sheets (a figure-reuse check).

        STANDARD_NUMERALS carries the small, fixed set of protocol and
        format constants (HTTP status codes, ISO standard numbers) that name
        a standard rather than a fact about Ledgerline, so they are exempt.
        Everything else in the twelve files this journey actually wrote must
        appear, digit run for digit run, somewhere in
        expense-copilot-journey.md or ledgerline-journey.md.
        """
        sheet_text = "".join((EXAMPLES / rel).read_text(encoding="utf-8")
                             for rel in DATA_SHEETS)
        sheet_numerals = _numerals(sheet_text) | STANDARD_NUMERALS
        for rel in NEW_EXAMPLES:
            text = (EXAMPLES / rel).read_text(encoding="utf-8")
            offending = sorted(_numerals(text) - sheet_numerals)
            self.assertEqual(
                offending, [],
                "%s carries numerals not on either data sheet: %s" % (rel, offending))


if __name__ == "__main__":
    unittest.main()
