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
import re
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

# A gate's section ends at the next '## ' heading of any kind. The shipped file has
# no box under a non-gate heading today, so a parser that ran each gate to the
# next '## Gate' heading counts it the same; this text is what tells the two apart.
# Gate 1's later lines use the other spellings lint.py's CHECKBOX_RE accepts, which
# the shipped file does not use either, so only this text tells a parser that
# counts '- [ ] ' alone from one that counts every box.
SYNTHETIC_CHECKLISTS = (
    "- [ ] a box before any gate belongs to none\n\n"
    "## Gate 1: one\n\n"
    "- [ ] first line of gate one\n"
    "- [ ] second line of gate one\n\n"
    "### A subsection does not end its gate\n\n"
    "- [ ] third line of gate one\n"
    "- [x] a ticked line of gate one\n"
    "* [ ] a starred line of gate one\n"
    "  - [ ] an indented line of gate one\n\n"
    "## Gate 2: two\n\n"
    "- [ ] the only line of gate two\n\n"
    "## What a gate is worth\n\n"
    "- [ ] a box under a heading that is not a gate belongs to none\n"
)

PLANNING_QUESTIONS = {"DEFINE-10": "planning/vision.md",
                      "DEFINE-11": "planning/product-strategy.md",
                      "DEFINE-12": "planning/roadmap.md"}

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

    def test_parse_checklists_counts_lines_per_gate(self):
        self.assertEqual(question_banks.parse_checklists(SYNTHETIC_CHECKLISTS), {
            1: ["first line of gate one", "second line of gate one",
                "third line of gate one", "a ticked line of gate one",
                "a starred line of gate one", "an indented line of gate one"],
            2: ["the only line of gate two"],
        })
        # Every box the fixture spells is one lint.py counts as a checkbox, so the
        # compiler and the linter agree on what a checklist line is.
        import lint
        boxes = [line for line in SYNTHETIC_CHECKLISTS.split("\n") if "[ ]" in line or "[x]" in line]
        self.assertEqual(len(boxes), 9)
        for line in boxes:
            self.assertTrue(lint.CHECKBOX_RE.match(line), line)
        shipped = question_banks.parse_checklists(
            question_banks.STAGE_GATES.read_text(encoding="utf-8"))
        self.assertEqual({gate: len(lines) for gate, lines in shipped.items()},
                         {1: 8, 2: 11, 3: 9, 4: 6, 5: 8, 6: 8})

    def test_a_rendering_table_that_misses_a_checklist_line_is_a_bank_error(self):
        bank = self._parse()  # SYNTHETIC feeds Gate 9 and renders two rows
        three = question_banks.parse_checklists(
            "## Gate 9: test\n- [ ] one\n- [ ] two\n- [ ] three\n")
        with self.assertRaisesRegex(
                question_banks.BankError,
                "has 3 checklist lines but .* has 2 rows") as caught:
            question_banks.check_checklist_coverage(bank, three)
        self.assertIn("Gate 9", str(caught.exception))
        self.assertIn("skills/conductor/questions/test.md", str(caught.exception))
        # Equal counts pass: the check compares rows with lines, nothing else.
        question_banks.check_checklist_coverage(bank, question_banks.parse_checklists(
            "## Gate 9: test\n- [ ] one\n- [ ] two\n"))
        with self.assertRaisesRegex(question_banks.BankError, "has no Gate 9 checklist"):
            question_banks.check_checklist_coverage(bank, {})

    def test_the_define_bank_before_the_planning_questions_fails_the_coverage_check(self):
        """The red state this check was written against, rebuilt so it stays provable.

        Before DEFINE-10 to DEFINE-12 the bank rendered eight rows for Gate 2's
        eleven lines and compiled cleanly. That bank is rebuilt here from the
        shipped file by removing the three entries and their rows, and the
        real --check and write modes are run over it with the other five banks
        and the real os/STAGE-GATES.md.
        """
        text = (question_banks.SOURCE_DIR / "define.md").read_text(encoding="utf-8")
        kept, skipping = [], False
        for line in text.split("\n"):
            if line.startswith("### "):
                skipping = any(line.startswith("### %s:" % question_id)
                               for question_id in PLANNING_QUESTIONS)
            elif line.startswith("## "):
                skipping = False
            if skipping or (line.startswith("|") and any(
                    re.search(r"\b%s\b" % question_id, line) for question_id in PLANNING_QUESTIONS)):
                continue
            kept.append(line)
        before = question_banks.parse_bank("define", "\n".join(kept))
        self.assertEqual([question["id"] for question in before["questions"]],
                         ["DEFINE-%d" % number for number in range(1, 10)])
        self.assertEqual(len(before["gate_rendering"]), 8)
        expected = (r"Gate 2 in os/STAGE-GATES\.md has 11 checklist lines but .*"
                    r"skills/conductor/questions/define\.md has 8 rows")
        checklists = question_banks.parse_checklists(
            question_banks.STAGE_GATES.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(question_banks.BankError, expected):
            question_banks.check_checklist_coverage(before, checklists)

        source_dir, output = question_banks.SOURCE_DIR, question_banks.OUTPUT
        with tempfile.TemporaryDirectory() as tmp:
            rebuilt = Path(tmp) / "questions"
            rebuilt.mkdir()
            for stage in question_banks.ORDER:
                (rebuilt / ("%s.md" % stage)).write_bytes(
                    (source_dir / ("%s.md" % stage)).read_bytes())
            (rebuilt / "define.md").write_text("\n".join(kept), encoding="utf-8")
            committed = output.read_bytes()
            question_banks.SOURCE_DIR = rebuilt
            question_banks.OUTPUT = Path(tmp) / "question_banks.json"
            question_banks.OUTPUT.write_bytes(committed)
            try:
                for argv in (["--check"], []):
                    errors = io.StringIO()
                    with contextlib.redirect_stdout(io.StringIO()), \
                            contextlib.redirect_stderr(errors):
                        code = question_banks.main(argv)
                    self.assertEqual(code, 1, argv)
                    self.assertRegex(errors.getvalue(), expected)
                    self.assertEqual(question_banks.OUTPUT.read_bytes(), committed, argv)
            finally:
                question_banks.SOURCE_DIR, question_banks.OUTPUT = source_dir, output

    def test_the_define_bank_asks_for_the_planning_set(self):
        define = next(bank for bank in self.contract["banks"] if bank["id"] == "define")
        landing = {question["id"]: re.findall(r"`([^`]+\.md)`", question["lands_in"])
                   for question in define["questions"]}
        for question_id, path in PLANNING_QUESTIONS.items():
            self.assertEqual(landing[question_id][0], path, question_id)
        self.assertEqual({question_id for question_id, paths in landing.items()
                          if any(path.startswith("planning/") for path in paths)},
                         set(PLANNING_QUESTIONS))
        # Appended after DEFINE-9, never inserted: a resumed journey points at an ID.
        self.assertEqual([question["id"] for question in define["questions"]][-3:],
                         list(PLANNING_QUESTIONS))
        self.assertEqual([row["questions"] for row in define["gate_rendering"][:3]],
                         [[question_id] for question_id in PLANNING_QUESTIONS])
        self.assertEqual((len(define["questions"]), len(define["gate_rendering"])), (12, 11))
        # Each approver set is the one os/STAGE-GATES.md names for that document, and
        # each entry takes a one-pager that carries it, which Gate 2 allows at that weight.
        approvers = {"DEFINE-10": ("business sponsor",),
                     "DEFINE-11": ("product owner", "business sponsor"),
                     "DEFINE-12": ("product owner", "engineering lead")}
        for question_id, roles in approvers.items():
            accept = self.questions[question_id]["accept_when"]
            for role in roles:
                self.assertIn(role, accept, question_id)
            self.assertIn("one-pager", accept, question_id)
            self.assertEqual(self.questions[question_id]["evidence_rung"], 2, question_id)

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
