#!/usr/bin/env python3
"""Tests for tools/phase_index.py, the generator of docs/PHASE-INDEX.md.

    python3 -m unittest test_phase_index

The index is how a phase reaches its frameworks, its template, a filled example
and the working copy it produces, so the rules that fail it are pinned here: a
reference to a template that does not exist, and a journey step that lost its
last framework or its last example. Every other gap is one the index shows. The
tests read the real tree; the one that writes points OUTPUT at a temporary file.
"""
from __future__ import annotations

import contextlib
import copy
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

import phase_index  # noqa: E402


class PhaseIndexTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.index = phase_index.collect()
        cls.text = phase_index.render(cls.index)

    def _copy(self):
        return copy.deepcopy(self.index)

    def _main(self, argv):
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return phase_index.main(argv)

    def test_render_is_deterministic(self):
        self.assertEqual(phase_index.render(phase_index.collect()), self.text)

    def test_this_tree_has_no_problems(self):
        self.assertEqual(phase_index.problems(self.index), [])

    def test_a_journey_step_without_an_example_is_a_problem(self):
        index = self._copy()
        index["filled_by"]["templates/planning/vision.md"] = []
        self.assertIn("journey step templates/planning/vision.md has no "
                      "filled example", phase_index.problems(index))

    def test_a_journey_step_without_a_framework_is_a_problem(self):
        index = self._copy()
        index["fed_by"]["templates/discovery/problem-framing.md"] = []
        self.assertIn("journey step templates/discovery/problem-framing.md "
                      "has no framework feeding it",
                      phase_index.problems(index))

    def test_a_reference_to_a_missing_template_is_a_problem(self):
        index = self._copy()
        index["broken"] = [("examples/fake.md", "templates/does-not-exist.md")]
        self.assertIn("examples/fake.md names templates/does-not-exist.md, "
                      "which is not a file", phase_index.problems(index))

    def test_the_journey_lists_its_steps_in_order(self):
        journey = self.text.split("## The journey", 1)[1].split("\n## ", 1)[0]
        rows = [line for line in journey.splitlines()
                if re.match(r"\| \d+ \|", line)]
        self.assertEqual(len(rows), len(phase_index.JOURNEY))
        for row, rel in zip(rows, phase_index.JOURNEY):
            self.assertIn("(../%s)" % rel, row)

    def test_the_vision_row_names_its_gate_dependency_and_id(self):
        row = next(line for line in self.text.splitlines()
                   if line.startswith("| 2 |"))
        self.assertIn("(../templates/planning/vision.md)", row)
        self.assertIn("DEFINE, Gate 2:", row)
        self.assertIn("`ledgerline/discovery/problem-framing`", row)
        self.assertIn("`ledgerline/planning/vision`", row)

    def test_every_template_sits_in_exactly_one_stage_table(self):
        stages = self.text.split("## The journey", 1)[1].split("\n## ", 1)[1]
        for rel in self.index["templates"]:
            self.assertEqual(
                stages.count("| [%s](../%s) |" % (Path(rel).name, rel)), 1, rel)

    def test_the_regulated_prd_sits_in_the_ai_overlay_track(self):
        rel = "modules/regulated/templates/regulated-ai-prd-template.md"
        self.assertEqual(self.index["templates"][rel]["phase"], "AI OVERLAY")

    def test_the_index_states_no_template_count(self):
        # tools/docs_contract.py polices every "N templates" claim in the tree.
        self.assertIsNone(re.search(r"\b\d+\s+(?:templates?|blanks?)\b",
                                    self.text, re.I))

    def test_check_fails_when_missing_or_stale_and_passes_once_written(self):
        original = phase_index.OUTPUT
        with tempfile.TemporaryDirectory() as tmp:
            phase_index.OUTPUT = Path(tmp) / "PHASE-INDEX.md"
            try:
                self.assertEqual(self._main(["--check"]), 1)
                phase_index.OUTPUT.write_text("stale\n", encoding="utf-8")
                self.assertEqual(self._main(["--check"]), 1)
                self.assertEqual(self._main([]), 0)
                self.assertEqual(self._main(["--check"]), 0)
            finally:
                phase_index.OUTPUT = original


if __name__ == "__main__":
    unittest.main()
