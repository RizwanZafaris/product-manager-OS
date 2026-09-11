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

    def test_a_wrong_section_heading_is_reported_when_the_total_still_adds_up(self):
        """Two headings wrong in opposite directions leave the total, every
        link and the front door all correct, so no other reading can see
        them. Only the heading counted against its own directory does, and
        the stale-total test above cannot show that, because it also moves
        the total."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            catalog = root / self.CATALOG
            self.rewrite(catalog, "## discovery (16 templates)",
                         "## discovery (15 templates)", 1)
            self.rewrite(catalog, "## definition (11 templates)",
                         "## definition (12 templates)", 1)
            self.assertEqual(
                sorted([(self.CATALOG, "the discovery section says 15 "
                         "template(s) and the directory holds 16"),
                        (self.CATALOG, "the definition section says 12 "
                         "template(s) and the directory holds 11")]),
                sorted(self.findings(root)))

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


class ReadinessProbeCiWiringTests(unittest.TestCase):
    """probe_ci_covers_runtime: the workflow runs the canonical suite, and the
    suite carries every gate the readiness rubric counts on."""

    WORKFLOW = REPO / ".github" / "workflows" / "lint.yml"
    INVOCATION = "        run: python3 tools/ci_gate.py"

    def probe(self, workflow, gate_ids):
        manifest = json.dumps({"schema": 1,
                               "gates": [{"id": gate} for gate in gate_ids]})
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / ".github" / "workflows" / "lint.yml"
            target.parent.mkdir(parents=True)
            target.write_text(workflow, encoding="utf-8")
            with unittest.mock.patch.object(readiness_probe, "REPO", root), \
                    unittest.mock.patch.object(readiness_probe, "run",
                                               return_value=(0, manifest)):
                return quietly(readiness_probe.probe_ci_covers_runtime)

    def real(self):
        return (self.WORKFLOW.read_text(encoding="utf-8"),
                [gate.gate_id for gate in ci_gate.GATES])

    def test_the_shipped_workflow_and_suite_pass(self):
        code, output = self.probe(*self.real())
        self.assertEqual(0, code, output)

    def test_a_suite_missing_a_required_gate_fails(self):
        workflow, gates = self.real()
        self.assertIn("security-policy", gates)
        code, output = self.probe(
            workflow, [gate for gate in gates if gate != "security-policy"])
        self.assertEqual(1, code, output)
        self.assertIn("misses gate ids: security-policy", output)

    def test_a_commented_out_invocation_fails(self):
        workflow, gates = self.real()
        self.assertIn(self.INVOCATION, workflow)
        code, output = self.probe(
            workflow.replace(self.INVOCATION,
                             "        # run: python3 tools/ci_gate.py"), gates)
        self.assertEqual(1, code, output)
        self.assertIn("no active exact invocation", output)

    def test_a_step_allowed_to_fail_fails_the_wiring(self):
        workflow, gates = self.real()
        code, output = self.probe(
            workflow.replace(self.INVOCATION, self.INVOCATION
                             + "\n        continue-on-error: true", 1), gates)
        self.assertEqual(1, code, output)
        self.assertIn("continue-on-error", output)


class CiGateVerdictTests(unittest.TestCase):
    """tools/ci_gate.py decides pass or fail from what a gate printed as well
    as how it exited. These are the readings a passing exit code cannot hide."""

    def gate(self, script, **options):
        return ci_gate.Gate("fixture", ("python3", "-c", script), **options)

    def test_a_clean_test_run_passes_and_is_counted(self):
        row = ci_gate.run_gate(self.gate(
            "print('Ran 3 tests in 0.010s'); print(); print('OK')",
            expects_tests=True))
        self.assertTrue(row["passed"], row)
        self.assertEqual(3, row["tests"])

    def test_a_nonzero_exit_fails(self):
        row = ci_gate.run_gate(self.gate("import sys; sys.exit(3)"))
        self.assertFalse(row["passed"])
        self.assertIn("exit 3", row["reasons"])

    def test_zero_tests_fails_even_on_a_clean_exit(self):
        for script in ("print('Ran 0 tests in 0.000s'); print('OK')",
                       "print('OK')"):
            with self.subTest(script=script):
                row = ci_gate.run_gate(self.gate(script, expects_tests=True))
                self.assertFalse(row["passed"], row)
                self.assertIn("zero tests", row["reasons"])

    def test_a_skipped_test_is_not_a_pass(self):
        for tail in ("OK (skipped=1)", "OK (expected failures=1)",
                     "OK (unexpected successes=1)"):
            with self.subTest(tail=tail):
                row = ci_gate.run_gate(self.gate(
                    "print('Ran 4 tests in 0.100s'); print(%r)" % tail,
                    expects_tests=True))
                self.assertFalse(row["passed"], row)
                self.assertIn("non-passing test disposition", row["reasons"])

    def test_missing_required_output_fails_on_a_clean_exit(self):
        row = ci_gate.run_gate(self.gate(
            "print('frontmatter created: 1, extended: 0')",
            required_output="created: 0, extended: 0"))
        self.assertFalse(row["passed"])
        self.assertIn("required output missing", row["reasons"])

    def test_a_gate_that_runs_past_its_timeout_fails(self):
        row = ci_gate.run_gate(self.gate("import time; time.sleep(30)",
                                         timeout=1))
        self.assertFalse(row["passed"])
        self.assertIsNone(row["exit_code"])

    def test_an_unknown_gate_id_is_refused(self):
        code, output = quietly(ci_gate.main, ["--gate", "no-such-gate"])
        self.assertEqual(2, code)
        self.assertIn("unknown gate", output)

    def test_one_failing_gate_fails_the_suite_and_no_gates_is_no_pass(self):
        passing = self.gate("pass")
        failing = ci_gate.Gate("broken", ("python3", "-c",
                                          "import sys; sys.exit(1)"))
        for gates, expected in (((passing,), 0), ((passing, failing), 1),
                                ((), 1)):
            with self.subTest(gates=[gate.gate_id for gate in gates]):
                with unittest.mock.patch.object(ci_gate, "GATES", gates):
                    code, _output = quietly(ci_gate.main, [])
                self.assertEqual(expected, code)


class FrontmatterInitGateTests(unittest.TestCase):
    """The frontmatter gate is tools/frontmatter_init.py --dry-run plus one
    required line of output. These hold the script to what that line means."""

    TARGET = "templates/definition/one-pager.md"

    @classmethod
    def setUpClass(cls):
        cls.required = next(gate.required_output for gate in ci_gate.GATES
                            if gate.gate_id == "frontmatter")

    def dry_run(self, root):
        return quietly(frontmatter_init.main, ["--dry-run", "--root",
                                               str(root)])

    def edit(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def method_line(self, path):
        return next(line for line in path.read_text(encoding="utf-8")
                    .splitlines() if line.startswith("method:"))

    def test_this_tree_reports_nothing_to_write(self):
        code, output = self.dry_run(REPO)
        self.assertEqual(0, code)
        self.assertIn(self.required, output)

    def test_a_missing_key_is_reported_and_the_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            target = root / self.TARGET
            self.edit(target, self.method_line(target) + "\n", "")
            before = target.read_bytes()
            _code, output = self.dry_run(root)
            self.assertIn("extended: 1", output)
            self.assertNotIn(self.required, output)
            self.assertEqual(before, target.read_bytes())

    def test_a_write_restores_the_key_and_keeps_a_human_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            target = root / self.TARGET
            method = self.method_line(target)
            self.edit(target, method + "\n", "")
            self.edit(target, 'aliases: ["One-Pager"]',
                      'aliases: ["One-Pager", "a hand-written alias"]')
            quietly(frontmatter_init.main, ["--root", str(root)])
            text = target.read_text(encoding="utf-8")
            self.assertIn(method, text.splitlines())
            self.assertIn('aliases: ["One-Pager", "a hand-written alias"]',
                          text, "a derived value a human edited was replaced")
            _code, output = self.dry_run(root)
            self.assertIn(self.required, output,
                          "a second run over the written tree is not clean")

    def test_a_file_with_no_frontmatter_is_reported_as_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            target = root / self.TARGET
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            target.write_text(text.split("\n---\n", 1)[1], encoding="utf-8")
            _code, output = self.dry_run(root)
            self.assertIn("created: 1", output)
            self.assertNotIn(self.required, output)


class GraphFreshnessGateTests(unittest.TestCase):
    """docs/GRAPH.md is generated, and --check is all that keeps it true.

    That gate regenerates from the tree and compares bytes, so it does see a
    generator change: both sides move and the committed file stops matching.
    What it cannot see is the part of the generator that never reaches the
    output. check_unique_ids is exactly that part, and short-circuiting it
    merges two files into one diagram node with every gate still green, which
    is why it is read here directly rather than through the diagram.
    """

    def graph(self, root, *arguments):
        return subprocess.run(
            [sys.executable, str(root / "tools" / "graph.py"),
             "--root", str(root), *arguments], capture_output=True, text=True,
            timeout=120)

    def test_the_committed_graph_matches_this_tree(self):
        done = self.graph(REPO, "--check")
        self.assertEqual(0, done.returncode, done.stdout + done.stderr)

    def test_a_file_leaving_the_tree_makes_the_committed_graph_stale(self):
        """The graph is a reading of the repository. A committed file that no
        longer describes the tree is the whole failure this gate exists for."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.assertEqual(0, self.graph(root, "--check").returncode)
            (root / "templates" / "discovery" / "personas.md").unlink()
            stale = self.graph(root, "--check")
            self.assertEqual(1, stale.returncode, stale.stdout)
            self.assertIn("is stale", stale.stderr)

    def test_an_edited_graph_file_is_stale_against_the_same_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            target = root / "docs" / "GRAPH.md"
            target.write_bytes(target.read_bytes() + b"\n")
            stale = self.graph(root, "--check")
            self.assertEqual(1, stale.returncode, stale.stdout)
            self.assertIn("is stale", stale.stderr)

    def test_a_missing_graph_is_reported_and_not_quietly_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "docs" / "GRAPH.md").unlink()
            missing = self.graph(root, "--check")
            self.assertEqual(1, missing.returncode, missing.stdout)
            self.assertIn("is missing", missing.stderr)
            self.assertFalse((root / "docs" / "GRAPH.md").exists(),
                             "--check reports; it does not repair")

    def test_two_paths_that_sanitize_alike_keep_distinct_node_ids(self):
        # Every byte outside [0-9A-Za-z] collapses to "_", so these two differ
        # only in the character that collapses. The hash suffix is keyed on the
        # untouched path, which is the part that carries the difference.
        self.assertNotEqual(node_id("os/collision-a.md"),
                            node_id("os/collision_a.md"))
        check_unique_ids(["os/collision-a.md", "os/collision_a.md"])

    def test_a_real_id_collision_stops_the_build(self):
        with unittest.mock.patch("tools.graph.node_id",
                                 side_effect=lambda rel: "n_same"):
            with self.assertRaises(SystemExit) as stopped:
                check_unique_ids(["os/one.md", "os/two.md"])
        self.assertIn("node id collision", str(stopped.exception))


STRONG_TEMPLATE = """# Strong

Stage: DEFINE, feeds Gate 2

## Problem
<!-- What goes here, and what a bad answer looks like: one that never names a user. -->
| Field | Value |
|---|---|
| [owner name] | [target date] |
| [metric name] | [baseline value] |
| [risk one] | [mitigation one] |
| [risk two] | [mitigation two] |

Read with [the PRD](../definition/prd.md), [the one-pager](one-pager.md),
[the OKRs](okrs.md) and [the roadmap](roadmap.md).

## Worked example
<!-- ILLUSTRATIVE only. The trap: an example copied as evidence fails the gate. -->
ILLUSTRATIVE: [field alpha] and [field beta] filled for a fictional product.

## Exit gate
<!-- Do not pass this gate on an unsigned box; a bad answer is a blank owner. -->
- [ ] A named human signed.
"""

WEAK_TEMPLATE = "# Weak\n\n## One\n\n## Two\n\n## Three\n"


class TemplateRubricGateTests(unittest.TestCase):
    """tools/template_rubric.py: the flagship bar and its --min gate mode."""

    def tree(self, tmp, **files):
        root = Path(tmp)
        for name, text in files.items():
            path = root / "templates" / "definition" / (name + ".md")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return root

    def score(self, tmp, text):
        root = self.tree(tmp, subject=text)
        with unittest.mock.patch.object(template_rubric, "REPO", root):
            return template_rubric.score_template(
                root / "templates" / "definition" / "subject.md")

    def run_gate(self, root, *argv):
        with unittest.mock.patch.object(template_rubric, "REPO", root), \
                unittest.mock.patch.object(template_rubric, "TEMPLATES",
                                           root / "templates"), \
                unittest.mock.patch.object(template_rubric, "REFERENCE",
                                           root / "templates" / "definition"
                                           / "prd.md"):
            return quietly(template_rubric.main, list(argv))

    def test_the_weights_are_a_hundred_points(self):
        self.assertEqual(100, sum(template_rubric.WEIGHTS.values()))

    def test_a_template_that_does_what_the_reference_does_scores_full_marks(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, STRONG_TEMPLATE)
        self.assertEqual(100.0, report["score"], report["marks"])

    def test_named_sections_with_no_guidance_score_as_a_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, WEAK_TEMPLATE)
        self.assertEqual(0.0, report["marks"]["self_explaining"])
        self.assertLess(report["score"], 20)

    def test_one_preamble_comment_does_not_explain_every_section(self):
        text = "# Form\n<!-- one long preamble -->\n\n## One\n\n## Two\n"
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, text)
        self.assertEqual(0, report["sections_explained"])
        self.assertEqual(0.0, report["marks"]["self_explaining"])

    def test_link_text_is_not_a_fill_in_field(self):
        text = ("# Links\n\n## One\n<!-- guidance -->\n[the knowledge index]"
                "(../../knowledge/INDEX.md) and [the PRD](prd.md)\n")
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, text)
        self.assertEqual(0, report["fields"])
        self.assertEqual(2, report["links"])

    def test_the_min_gate_fails_on_a_weak_template_and_passes_without_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.tree(tmp, prd=STRONG_TEMPLATE, strong=STRONG_TEMPLATE,
                             weak=WEAK_TEMPLATE)
            code, output = self.run_gate(root, "--min", "70")
            self.assertEqual(1, code, output)
            self.assertIn("templates/definition/weak.md", output)
            (root / "templates" / "definition" / "weak.md").unlink()
            code, output = self.run_gate(root, "--min", "70")
            self.assertEqual(0, code, output)

    def test_an_exempt_file_keeps_its_row_and_leaves_the_statistics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.tree(tmp, prd=STRONG_TEMPLATE, weak=WEAK_TEMPLATE)
            exempt = {"templates/definition/weak.md": "Not a fill-in template."}
            with unittest.mock.patch.object(template_rubric, "EXEMPT", exempt):
                code, output = self.run_gate(root, "--min", "70")
            self.assertEqual(0, code, output)
            self.assertIn("exempt from this rubric, with the reason:", output)
            self.assertIn("templates/definition/weak.md", output)


class PmWorkingSetGateTests(unittest.TestCase):
    """tools/pm_working_set.py: the documents written weekly, held to the bar."""

    PRD = "templates/definition/prd.md"

    def gate(self, working_set, score=None):
        patches = [unittest.mock.patch.object(pm_working_set, "WORKING_SET",
                                              working_set)]
        if score is not None:
            patches.append(unittest.mock.patch.object(
                pm_working_set, "score_template",
                return_value={"score": score, "marks": {}}))
        with contextlib.ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            return quietly(pm_working_set.main, ["--min", "75"])

    def test_every_document_in_the_set_names_a_template_this_tree_ships(self):
        for name, _cadence, rel in pm_working_set.WORKING_SET:
            with self.subTest(document=name):
                self.assertIsNotNone(rel)
                self.assertTrue((REPO / rel).is_file(), rel)

    def test_a_document_with_no_template_fails_the_gate(self):
        code, output = self.gate([
            ("Ghost document", "weekly", "templates/none/ghost.md"),
            ("PRD or spec", "per feature", self.PRD)])
        self.assertEqual(1, code, output)
        self.assertIn("have no template at all", output)

    def test_a_document_below_the_bar_fails_and_one_above_passes(self):
        working_set = [("PRD or spec", "per feature", self.PRD)]
        code, output = self.gate(working_set, score=60.0)
        self.assertEqual(1, code, output)
        self.assertIn("below the 75 bar", output)
        code, output = self.gate(working_set, score=95.0)
        self.assertEqual(0, code, output)


class ReadinessCategoryExitTests(unittest.TestCase):
    """tools/readiness.py --category exits on its own verdict.

    Criterion CI-3 pins this through two fresh-tree mutants, which means only a
    full readiness run notices a regression. These read the same branch in the
    fast suite, against a stubbed report, so the diagnostic a maintainer runs
    on one category before a release cannot read green over a failing
    criterion.
    """

    def report(self, **changes):
        report = {"earned": 10, "possible": 10, "rubric_errors": [],
                  "verified_criteria": 1, "failed_criteria": 0,
                  "unbuilt_criteria": 0, "external_blockers": [],
                  "hard_gates": {}, "verdict": "CATEGORY DIAGNOSTIC: fixture",
                  "evaluated_commit": "d" * 40, "python": "3",
                  "local_engineering_readiness": False,
                  "complete_readiness": False}
        report.update(changes)
        return report

    def category(self, report, name="workspace"):
        with unittest.mock.patch.object(readiness, "score",
                                        return_value=report) as scored:
            code, _output = quietly(readiness.main, ["--category", name])
        scored.assert_called_once_with(name)
        return code

    def test_a_failing_criterion_fails_the_category_run(self):
        self.assertEqual(1, self.category(self.report(failed_criteria=1,
                                                      earned=5)))

    def test_a_rubric_error_fails_the_category_run(self):
        self.assertEqual(1, self.category(self.report(
            rubric_errors=["unknown verifier"])))

    def test_a_clean_category_passes_without_claiming_readiness(self):
        self.assertEqual(0, self.category(self.report()))


if __name__ == "__main__":
    unittest.main()
