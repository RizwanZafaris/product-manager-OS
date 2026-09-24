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


class OnePagerCostAndStopTests(unittest.TestCase):
    """The one-pager's failure table demands that costs, risks and a kill
    criterion appear on the same page, and that success carries one date.

    Until F10 the demand had nowhere to land: the fillable structure carried no
    appetite or cost field, no stop threshold and caller, no reversal line, and
    the metric table had a target with no date beside it. A failure table that
    asks for something the form cannot hold teaches the reader to skip it, and
    nothing in the tree noticed. The template half of this class is the
    contract; the example half is the proof that the fields can be answered,
    because a field nobody has filled once is a heading, not a contract.

    The limit, named rather than left silent: this reads the shipped template
    and the one worked example, and nothing in this tree reads a user's filled
    copy of either. An appetite with no number, a stop row with no caller and a
    blank review date all still reach Gate 2, where the humans who sign it are
    the check, exactly as the template's own "What checks this" paragraph says.
    """

    TEMPLATE = "templates/definition/one-pager.md"
    EXAMPLE = "examples/sahulat-one-pager.md"
    SECTION = "## 8. Cost, stop and reversal"
    STOP_HEADER = ("| # | We stop, cut scope or roll back if | Threshold | "
                   "Checked when | Who calls it |")

    def read(self, relative_path):
        return (REPO / relative_path).read_text(encoding="utf-8")

    def starts_with(self, text, prefix):
        return [line for line in text.splitlines() if line.startswith(prefix)]

    def metric_header(self, text, where):
        header = self.starts_with(text, "| Metric |")
        self.assertTrue(header, "%s has no metric table to date" % where)
        return header[0]

    def test_the_template_carries_the_fields_its_failure_table_demands(self):
        text = self.read(self.TEMPLATE)
        self.assertIn(self.SECTION, text,
                      "nowhere on the page to record cost, stopping or reversal")
        self.assertTrue(self.starts_with(text, "**Appetite:**"),
                        "no field for what the sponsor agreed to spend")
        self.assertTrue(self.starts_with(text, "**Reversal:**"),
                        "no field for how this is turned off, or what cannot be undone")
        self.assertIn(self.STOP_HEADER, text,
                      "no row holding a stop threshold and the person who calls it")

    def test_the_metric_table_carries_the_date_the_failure_table_demands(self):
        header = self.metric_header(self.read(self.TEMPLATE), self.TEMPLATE)
        self.assertIn("Review date", header,
                      "a target with no date cannot fail, and the failure table "
                      "asks for one metric, one target number, one date")

    def test_the_exit_gate_checks_the_new_fields(self):
        checklist = self.starts_with(self.read(self.TEMPLATE), "- [ ] ")
        for phrase, missing in (
                ("appetite", "the appetite and its review date"),
                ("date it is read", "the date each metric row is read"),
                ("reversal line", "the stop caller and what cannot be undone")):
            self.assertTrue(any(phrase in line for line in checklist),
                            "the exit gate does not check %s, so a page that "
                            "leaves it blank still passes" % missing)

    def test_the_filled_example_answers_every_new_field(self):
        text = self.read(self.EXAMPLE)
        self.assertIn(self.SECTION, text, "the worked example skips section 8")
        self.assertTrue(self.starts_with(text, "**Appetite:**"),
                        "the worked example never answers what this costs")
        self.assertTrue(self.starts_with(text, "**Reversal:**"),
                        "the worked example never answers how this is reversed")
        self.assertIn("Review date", self.metric_header(text, self.EXAMPLE),
                      "the worked example's metrics carry no date they are read")
        stop_rows = [line for line in text.splitlines()
                     if re.match(r"\|\s*S\d+\s*\|", line)]
        self.assertGreaterEqual(
            len(stop_rows), 2,
            "the worked example fills fewer than two stop rows, so the field is "
            "demonstrated by its header alone")


if __name__ == "__main__":
    unittest.main()
