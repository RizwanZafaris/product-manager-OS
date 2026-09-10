#!/usr/bin/env python3
"""Tests for release-gate tools that no test executed. Run: python3 -m unittest test_tools_gates

The audit of 2026-09-04 traced every root and harness test and found gate
modules under tools/ that ran zero lines, so an edit short-circuiting a check in
any of them produced no failing test: the only thing that would have noticed was
the gate, and the gate now agreed with its own weakened code. Each class below
pins the part of one tool that would go vacuous first, and each is written so it
fails when that check stops checking.

Two readings here are new rather than covered. The template inventory in
tools/docs_contract.py is the only check in the tree that counts the templates,
so nothing but a seeded defect shows that it counts them correctly. And the
mutation anchors in tools/readiness_probe.py are read statically, so a store or
workspace edit that moves an anchored line is reported by the fast suite rather
than by an 1800 second probe reporting itself as not caught.

tools/runtime_crash_probe.py is not tested here, and on purpose: it only ever
runs as a child process, and test_pmos_store asserts that the child dies by
SIGKILL at every one of its eight fault points, so a probe that stopped
crashing already fails a test. A trace of the parent process cannot see that,
which is why it read as zero coverage.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

REPO = Path(__file__).resolve().parent
TOOLS = REPO / "tools"
for _entry in (str(REPO), str(TOOLS)):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import ci_gate  # noqa: E402
import frontmatter_init  # noqa: E402
import pm_working_set  # noqa: E402
import readiness  # noqa: E402
import readiness_probe  # noqa: E402
import template_rubric  # noqa: E402
from tools.docs_contract import check as check_docs, check_inventory  # noqa: E402
from tools.graph import check_unique_ids, node_id  # noqa: E402


def copy_tree(tmp):
    """This repository, copied, so a mutation never touches the real one."""
    root = Path(tmp) / "repo"
    shutil.copytree(REPO, root, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                  "*.pyc", "._*"))
    return root


def quietly(function, *args, **kwargs):
    """Call a tool's entry point and return (result, what it printed)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        result = function(*args, **kwargs)
    return result, out.getvalue()


def mutation_table():
    """probe_mutation_checks' mutants, read from the source rather than run.

    The list is a literal, so it can be read without building eighteen fresh
    trees. If it ever stops being one, this raises rather than returning an
    empty table that every test below would pass against.
    """
    source = (TOOLS / "readiness_probe.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef) \
                and node.name == "probe_mutation_checks":
            for statement in node.body:
                if isinstance(statement, ast.Assign) \
                        and len(statement.targets) == 1 \
                        and getattr(statement.targets[0], "id", None) \
                        == "mutations":
                    return ast.literal_eval(statement.value)
    raise AssertionError("probe_mutation_checks no longer assigns a literal "
                         "mutations list, so its anchors cannot be read")


class TemplateInventoryGateTests(unittest.TestCase):
    """The count nothing measured, now measured against the tree.

    A stale figure survived in five files at once. The catalog's per-directory
    headings summed exactly to the number the front door claimed, so checking
    the arithmetic reassured a reader instead of alerting one, and the only
    reading that separates the two is a count taken from the directories.
    """

    CATALOG = "templates/README.md"

    def findings(self, root):
        return [(item.path, item.message) for item in check_inventory(root)]

    def rewrite(self, path, old, new, count=-1):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, path.name)
        path.write_text(text.replace(old, new, count) if count >= 0
                        else text.replace(old, new), encoding="utf-8")

    def test_the_tree_as_it_stands_states_its_own_inventory(self):
        self.assertEqual([], self.findings(REPO))

    def test_a_template_the_catalog_never_listed_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "templates" / "discovery" / "unlisted.md").write_text(
                "# Unlisted\n", encoding="utf-8")
            messages = [message for _path, message in self.findings(root)]
            self.assertIn("templates/discovery/unlisted.md is in the tree and "
                          "not in the catalog", messages)

    def test_a_self_consistent_stale_total_is_reported_everywhere_it_sits(self):
        """The shape the defect actually shipped in: the headings, the catalog
        total and the front door all agreeing on a number the tree does not."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            catalog = root / self.CATALOG
            self.rewrite(catalog, "(16 templates)", "(15 templates)", 1)
            self.rewrite(catalog, "(11 templates)", "(10 templates)", 1)
            for name, before, after in (
                    (self.CATALOG, "100 templates", "98 templates"),
                    ("README.md", "all 100 blanks", "all 98 blanks"),
                    ("docs/ARCHITECTURE.md", "all 100 templates",
                     "all 98 templates")):
                self.rewrite(root / name, before, after)
            reported = {path for path, _message in self.findings(root)}
            self.assertEqual({self.CATALOG, "README.md",
                              "docs/ARCHITECTURE.md"}, reported)

    def test_a_catalog_row_pointing_at_no_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.CATALOG, "discovery/personas.md",
                         "discovery/personae.md")
            messages = [message for _path, message in self.findings(root)]
            self.assertIn("the catalog lists templates/discovery/personae.md, "
                          "which is not in the tree", messages)

    def test_dropping_the_claim_is_not_a_way_to_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / "README.md", "all 100 blanks", "the blanks")
            self.rewrite(root / "docs" / "ARCHITECTURE.md",
                         "all 100 templates", "the templates")
            messages = [message for _path, message in self.findings(root)]
            self.assertTrue(any(message.startswith("no operator document "
                                                   "states the template "
                                                   "inventory")
                                for message in messages), messages)

    def test_the_gate_itself_fails_on_a_stale_total(self):
        """check_inventory passing proves nothing until the gate runs it. The
        documentation contract reported green on the stale figure for as long
        as it did because no reading of the count was wired into it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.assertEqual([], [item for item in check_docs(root)
                                  if item.severity == "error"])
            self.rewrite(root / "README.md", "all 100 blanks", "all 98 blanks")
            codes = {item.code for item in check_docs(root)
                     if item.severity == "error"}
            self.assertIn("inventory-count", codes)

    def test_a_tree_with_no_templates_makes_no_inventory_claim(self):
        """This gate also runs against fixture roots, which have no catalog to
        be wrong about. Silence there is the correct reading, not a hole."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            shutil.rmtree(root / "templates")
            self.assertEqual([], self.findings(root))


class ReadinessProbeMutationAnchorTests(unittest.TestCase):
    """Criterion CI-3's mutants, checked for the one way they fail silently.

    Each mutant replaces an anchor that has to occur exactly once in its file.
    When a later edit moves an anchored line the count goes to zero, and the
    probe reports that mutant as not caught: CI-3 goes red for a reason that
    has nothing to do with the gate it names, and only after a full fresh-tree
    run. The store's cancel handling was rewritten on exactly the line after
    the queue-integrity anchor, which is how that happened once already.
    """

    QUEUE = "queue integrity check bypassed before dispatch"
    CHECK = "            self._assert_queue_verified()\n"

    def test_every_anchor_matches_its_target_exactly_once(self):
        anchored = [row for row in mutation_table() if "rel" in row]
        self.assertTrue(anchored)
        for row in anchored:
            with self.subTest(label=row["label"]):
                text = (REPO / row["rel"]).read_text(encoding="utf-8")
                self.assertEqual(1, text.count(row["old"]),
                                 "the anchor for %r matches %d time(s) in %s"
                                 % (row["label"], text.count(row["old"]),
                                    row["rel"]))
                self.assertNotEqual(row["old"], row["new"])

    def test_the_table_keeps_every_mutant_and_names_each_once(self):
        table = mutation_table()
        labels = [row["label"] for row in table]
        self.assertEqual(len(labels), len(set(labels)))
        self.assertGreaterEqual(len(table), 18, "a mutant was dropped from "
                                "the table rather than re-anchored")
        for row in table:
            with self.subTest(label=row["label"]):
                self.assertTrue(row.get("argv"))
                self.assertTrue(row.get("diagnostic"))

    def test_the_queue_mutant_removes_only_the_check_and_only_in_lease_next(self):
        """Whatever text anchors it, the mutant has to take the queue check
        out of the dispatch path and change nothing else. The same two opening
        lines also start recovery and heartbeat, so an anchor that drifted
        into one of those would still match once and prove nothing about
        dispatch."""
        row = next(row for row in mutation_table()
                   if row["label"] == self.QUEUE)
        self.assertEqual(row["old"].replace(self.CHECK, "", 1), row["new"],
                         "the mutant removes the queue check and nothing else")
        text = (REPO / row["rel"]).read_text(encoding="utf-8")
        start = text.index("    def lease_next(")
        end = text.find("\n    def ", start + 1)
        at = text.find(row["old"])
        self.assertTrue(start < at < end,
                        "the anchor sits outside lease_next, the dispatch path")


if __name__ == "__main__":
    unittest.main()
