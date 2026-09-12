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


if __name__ == "__main__":
    unittest.main()
