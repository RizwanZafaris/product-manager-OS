#!/usr/bin/env python3
"""Tests for tools/question_banks.py, the Conductor's question bank compiler.

    python3 -m unittest test_question_banks

The six Markdown banks in skills/conductor/questions/ are the authored source of
the Conductor's interview; the compiler turns them into the one versioned
contract the pmos package ships, pmos/question_banks.json. Most tests read the
real tree. The format rules are pinned on a small synthetic bank, and the one
test that writes points OUTPUT at a temporary file.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
for _entry in (str(REPO), str(REPO / "tools")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import question_banks  # noqa: E402

SYNTHETIC = (
    "# TEST bank\n\n"
    "Stage: TEST, feeds Gate 9 (a test gate) in x.\n"
    "Header prose goes here.\n\n"
    "### TEST-1: first handle\n\n"
    "Ask: What is the first question?\n"
    "Wrong costs: Something breaks.\n"
    "Evidence class: 1 or 2, an artifact or better.\n"
    "Cross-examine when: the answer hedges. Move: force one.\n"
    "Accept when: it is answered.\n"
    "Lands in: `a.md`, and STATE.md accepted answers.\n\n"
    "### TEST-2: second handle\n\n"
    "Ask: What is the second question?\n"
    "Evidence class: 5, a judgment the user owns.\n"
    "Accept when: it is answered.\n"
    "Lands in: `b.md`, and STATE.md accepted answers.\n\n"
    "## Forced pair\n\n"
    "On \"advance anyway\": TEST-2, then TEST-1.\n\n"
    "## Gate 9 rendering\n\n"
    "| Gate 9 checklist line | Evidenced by |\n"
    "|---|---|\n"
    "| The first line | TEST-1 |\n"
    "| Signed by a human | The signed gate attestation |\n"
)

SYNTHETIC_SIGNOFFS = (
    "preamble\n\n"
    "## Gate 1: discovery\n\n"
    "| Checklist | Status |\n"
    "|---|---|\n"
    "| smoke test | pass |\n"
    "\n"
    "| Sign-off | Name | Date |\n"
    "| Product owner | Priya | 2026 |\n"
    "| Sponsor or lead who can stop this | Sam | 2026 |\n\n"
    "## Gate 2: define\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Product owner | Dee | 2026 |\n"
    "| Partner | Ian | 2026 |\n\n"
    "## Gate 3: design\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Reviewer | Raj | 2026 |\n"
    "| Support | Nia | 2026 |\n\n"
    "## Gate 4: build\n\n"
    "| Checklist | Status |\n"
    "|---|---|\n"
    "| build item | done |\n"
    "\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Reviewer | Tom | 2026 |\n\n"
    "## Gate 5: deliver\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Ops | Uma | 2026 |\n"
    "| QA | Will | 2026 |\n\n"
    "## Gate 6: operate\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Ops | Uma | 2026 |\n"
    "\n"
    "## Appendix\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Ignore this | Person | 2026 |\n"
)

SYNTHETIC_SIGNOFFS_MISSING = (
    "## Gate 1: one\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Owner | A | 2026 |\n\n"
    "## Gate 2: two\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Owner | B | 2026 |\n\n"
    "## Gate 3: three\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Owner | C | 2026 |\n\n"
    "## Gate 4: four\n\n"
    "| Checklist | Status |\n"
    "|---|---|\n"
    "| step | pass |\n\n"
    "## Gate 5: five\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Owner | E | 2026 |\n\n"
    "## Gate 6: six\n\n"
    "| Sign-off | Name | Date |\n"
    "|---|---|---|\n"
    "| Owner | F | 2026 |\n"
)


class QuestionBankCompileTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contract = question_banks.compile_contract()
        cls.questions = {question["id"]: question
                         for bank in cls.contract["banks"]
                         for question in bank["questions"]}

    def _parse(self, text=SYNTHETIC):
        return question_banks.parse_bank("test", text)

    def _main(self, argv):
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return question_banks.main(argv)

    def test_the_committed_contract_is_fresh(self):
        self.assertEqual(question_banks.OUTPUT.read_bytes(),
                         question_banks.render(self.contract).encode("utf-8"))

    def test_the_banks_come_in_loop_order_with_gates_one_to_six(self):
        banks = self.contract["banks"]
        self.assertEqual([bank["id"] for bank in banks],
                         list(question_banks.ORDER))
        self.assertEqual([bank["gate"] for bank in banks], [1, 2, 3, 4, 5, 6])

    def test_every_entry_has_a_rung_and_its_class(self):
        for question in self.questions.values():
            self.assertIn(question["evidence_rung"], range(1, 6))
            self.assertEqual(
                question["evidence_class"],
                question_banks.RUNG_CLASSES[question["evidence_rung"]])

    def test_one_or_two_reads_as_the_weaker_rung(self):
        self.assertEqual(self.questions["DISCOVER-2"]["evidence_rung"], 2)
        self.assertEqual(self.questions["DISCOVER-7"]["evidence_rung"], 2)
        self.assertEqual(self._parse()["questions"][0]["evidence_rung"], 2)

    def test_every_field_of_an_entry_is_carried(self):
        build_1 = self.questions["BUILD-1"]
        self.assertTrue(build_1["cross_examine"].startswith(
            "the answer is a coverage figure"))
        self.assertTrue(build_1["wrong_costs"])
        self.assertIn("delivery/testing-strategy.md", build_1["lands_in"])
        self.assertIsNone(build_1["options"])
        self.assertTrue(self.questions["DEFINE-1"]["options"])

    def test_entry_numbers_strictly_increase(self):
        for bank in self.contract["banks"]:
            numbers = [int(q["id"].rsplit("-", 1)[1])
                       for q in bank["questions"]]
            self.assertTrue(all(a < b for a, b in zip(numbers, numbers[1:])),
                            bank["id"])

    def test_each_forced_pair_names_two_entries_of_its_bank(self):
        for bank in self.contract["banks"]:
            own = {question["id"] for question in bank["questions"]}
            self.assertEqual(len(bank["forced_pair"]), 2, bank["id"])
            self.assertTrue(set(bank["forced_pair"]) <= own, bank["id"])

    def test_gate_rendering_keeps_the_body_rows_only(self):
        self.assertEqual(self._parse()["gate_rendering"], [
            {"line": "The first line", "evidenced_by": "TEST-1",
             "questions": ["TEST-1"]},
            {"line": "Signed by a human",
             "evidenced_by": "The signed gate attestation",
             "questions": []},
        ])
        for bank in self.contract["banks"]:
            for row in bank["gate_rendering"]:
                self.assertTrue(row["line"] and row["evidenced_by"], row)
                self.assertNotIn("checklist line", row["line"])
                self.assertTrue(set(row["questions"]) <= set(self.questions),
                                row)

    def test_a_broken_format_rule_is_a_bank_error(self):
        broken = {
            "no rung": SYNTHETIC.replace("5, a judgment", "a judgment"),
            "a rung out of range": SYNTHETIC.replace("5, a judgment",
                                                     "7, a judgment"),
            "no Accept when": SYNTHETIC.replace(
                "Accept when: it is answered.\nLands in: `b.md`",
                "Lands in: `b.md`"),
            "a repeated field": SYNTHETIC.replace(
                "Ask: What is the second question?\n",
                "Ask: What is the second question?\nAsk: Again?\n"),
            "numbers that do not increase": SYNTHETIC.replace(
                "### TEST-2:", "### TEST-1:"),
            "a forced pair of one": SYNTHETIC.replace(
                "TEST-2, then TEST-1", "TEST-2 alone"),
            "another stage's heading": SYNTHETIC.replace(
                "### TEST-2:", "### OTHER-2:"),
            "no rendering rows": SYNTHETIC.replace(
                "| The first line | TEST-1 |\n"
                "| Signed by a human | The signed gate attestation |\n", ""),
        }
        for label, text in broken.items():
            with self.subTest(label=label):
                self.assertNotEqual(text, SYNTHETIC)
                with self.assertRaises(question_banks.BankError):
                    self._parse(text)

    def test_the_version_follows_the_contract_not_the_prose(self):
        version = question_banks.bank_version(self._parse())
        self.assertNotEqual(version, question_banks.bank_version(self._parse(
            SYNTHETIC.replace("What is the first question?",
                              "What is the other question?"))))
        self.assertEqual(version, question_banks.bank_version(self._parse(
            SYNTHETIC.replace("Header prose goes here.",
                              "Different prose."))))

    def test_parse_signoffs_extracts_roles_and_ignores_other_tables(self):
        self.assertEqual(question_banks.parse_signoffs(SYNTHETIC_SIGNOFFS), {
            "1": ["Product owner", "Sponsor or lead who can stop this"],
            "2": ["Product owner", "Partner"],
            "3": ["Reviewer", "Support"],
            "4": ["Reviewer"],
            "5": ["Ops", "QA"],
            "6": ["Ops"],
        })

    def test_parse_signoffs_fails_when_a_gate_is_missing_a_signoff_table(self):
        with self.assertRaisesRegex(
            question_banks.BankError,
            "os/STAGE-GATES.md: Gate 4 has no sign-off table"):
            question_banks.parse_signoffs(SYNTHETIC_SIGNOFFS_MISSING)

    def test_parse_signoffs_treats_adjacent_gate_headings_as_a_section_end(self):
        text = (
            "## Gate 1: one\n"
            "## Gate 2: two\n"
            "| Sign-off | Name | Date |\n"
            "|---|---|---|\n"
            "| Name 2 | Sam | 2026 |\n"
            "\n"
            "## Gate 3: three\n"
            "| Sign-off | Name | Date |\n"
            "|---|---|---|\n"
            "| Name 3 | Tom | 2026 |\n"
            "\n"
            "## Gate 4: four\n"
            "| Sign-off | Name | Date |\n"
            "|---|---|---|\n"
            "| Name 4 | Uma | 2026 |\n"
            "\n"
            "## Gate 5: five\n"
            "| Sign-off | Name | Date |\n"
            "|---|---|---|\n"
            "| Name 5 | Viv | 2026 |\n"
            "\n"
            "## Gate 6: six\n"
            "| Sign-off | Name | Date |\n"
            "|---|---|---|\n"
            "| Name 6 | Wen | 2026 |\n"
        )
        with self.assertRaisesRegex(
            question_banks.BankError,
            "os/STAGE-GATES.md: Gate 1 has no sign-off table"):
            question_banks.parse_signoffs(text)

    def test_the_committed_contract_has_complete_signoffs(self):
        self.assertEqual(
            set(self.contract["signoffs"].keys()),
            {"1", "2", "3", "4", "5", "6"})
        self.assertEqual(self.contract["signoffs"]["1"],
                         ["Product owner",
                          "Sponsor or lead who can stop this"])
        for roles in self.contract["signoffs"].values():
            self.assertIsInstance(roles, list)
            self.assertTrue(roles)
            self.assertTrue(all(isinstance(role, str) for role in roles))

    def test_check_fails_when_missing_or_stale_and_passes_once_written(self):
        original = question_banks.OUTPUT
        with tempfile.TemporaryDirectory() as tmp:
            question_banks.OUTPUT = Path(tmp) / "question_banks.json"
            try:
                self.assertEqual(self._main(["--check"]), 1)
                question_banks.OUTPUT.write_text("stale\n", encoding="utf-8")
                self.assertEqual(self._main(["--check"]), 1)
                self.assertEqual(self._main([]), 0)
                self.assertEqual(self._main(["--check"]), 0)
            finally:
                question_banks.OUTPUT = original


if __name__ == "__main__":
    unittest.main()
