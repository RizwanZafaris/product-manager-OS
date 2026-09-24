#!/usr/bin/env python3
"""Tests for release-gate tools that no test executed. Run: python3 -m unittest tests/test_tools_gates.py

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
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
for _entry in (str(REPO), str(TOOLS)):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import ci_gate  # noqa: E402
import frontmatter_init  # noqa: E402
import pm_working_set  # noqa: E402
import prose_metrics  # noqa: E402
import readiness  # noqa: E402
import readiness_probe  # noqa: E402
import example_availability  # noqa: E402
import template_rubric  # noqa: E402
from tools.docs_contract import (check as check_docs,  # noqa: E402
                                 _example_families,
                                 check_commitment_probe_rule,
                                 check_declared_paths,
                                 check_duplicate_headings,
                                 check_evidence_contract,
                                 check_examples_inventory,
                                 check_executable_surface,
                                 check_gate_count,
                                 check_inventory,
                                 check_pricing_contract,
                                 check_readiness_claims,
                                 check_script_count,
                                 evidence_note_issues,
                                 main as docs_contract_main,
                                 PRICING_EXAMPLE,
                                 PRICING_EVIDENCE_COLUMN, PRICING_FLOOR_SECTION,
                                 PRICING_FLOOR_SOURCE, PRICING_TEMPLATE,
                                 README_READINESS, READINESS_CLAIMS)
from tools import exec_surface  # noqa: E402
from tools.graph import check_unique_ids, node_id  # noqa: E402
from tools.approval_gate import (CASES, EXAMPLE, EXECUTABLE_STATE,  # noqa: E402
                                 NOW, NULLIFIERS, OUTCOMES, PARAMS, POSITIVE,
                                 RECORD_FIELDS, RULES, RULE_TERMS, STATES,
                                 TEMPLATE, TERM_NAMES, Attempt,
                                 check as check_approvals, decide, revision)


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


class DuplicateHeadingGateTests(unittest.TestCase):
    """The heading a form carried twice, and the sibling rule that finds it.

    templates/discovery/discovery-synthesis.md opened its themes with two
    "### Theme 1" headings, one after the other, and every structural check
    walked past: the heading parses, the level does not jump, the link is not
    broken. A whole-file rule cannot be the answer, because a changelog writes
    "### Fixed" under every release on purpose. Siblings can, and these tests
    fail when that distinction stops being made in either direction.
    """

    DUPLICATE = ("### Theme 1: [name the theme in the customers' terms]\n"
                 "\n"
                 "### Theme 1: [name the theme in the customers' terms]\n")
    SINGLE = "### Theme 1: [name the theme in the customers' terms]\n"

    def findings(self, root):
        return [(item.path, item.line, item.message)
                for item in check_duplicate_headings(root)]

    def test_the_tree_as_it_stands_repeats_no_sibling_heading(self):
        self.assertEqual([], self.findings(REPO))

    def test_the_synthesis_template_with_its_duplicate_back_is_reported(self):
        """The audited defect, put back where the audit found it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "discovery" / "discovery-synthesis.md"
            text = document.read_text(encoding="utf-8")
            self.assertIn(self.SINGLE, text)
            document.write_text(text.replace(self.SINGLE, self.DUPLICATE, 1),
                                encoding="utf-8")
            reported = [(path, line) for path, line, _message in self.findings(root)]
            self.assertIn(("templates/discovery/discovery-synthesis.md", 66),
                          reported)
            message = dict(((path, line), message)
                           for path, line, message in self.findings(root))[
                               ("templates/discovery/discovery-synthesis.md", 66)]
            self.assertIn("line 64", message)

    def test_a_repeat_under_another_parent_is_not_a_duplicate(self):
        """The changelog shape: one "### Fixed" per release is not a defect,
        and a rule that cannot tell the two apart is not usable here."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## 0.2.0\n\n### Fixed\n\nsomething\n\n"
                "## 0.1.0\n\n### Fixed\n\nsomething else\n", encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0] == "note.md"])

    def test_a_repeat_under_one_parent_is_a_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## 0.2.0\n\n### Fixed\n\nsomething\n\n"
                "### Fixed\n\nsomething else\n", encoding="utf-8")
            self.assertEqual([("note.md", 9, "'Fixed' repeats the heading of "
                               "the same level and the same parent on line 5")],
                             [row for row in self.findings(root)
                              if row[0] == "note.md"])

    def test_a_heading_inside_an_html_comment_is_not_a_heading(self):
        """A guidance comment showing the filler what a repeated section looks
        like is an example of a heading, not two headings. This tree's
        templates are built out of such comments, so a check that reads them
        fails the tree it is meant to protect."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## Themes\n\n"
                "<!-- Write one block per theme, like this:\n"
                "### Theme n: [name]\n"
                "...\n"
                "### Theme n: [name]\n"
                "-->\n", encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0] == "note.md"])

    def test_a_real_duplicate_after_a_comment_is_still_reported(self):
        """The positive control for the line above: skipping comments must not
        skip what follows them."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n<!-- guidance\n### Theme n: [name]\n-->\n\n"
                "## Themes\n\n### Theme 1\n\n### Theme 1\n",
                encoding="utf-8")
            self.assertEqual([("note.md", 11, "'Theme 1' repeats the heading "
                               "of the same level and the same parent on line 9")],
                             [row for row in self.findings(root)
                              if row[0] == "note.md"])

    def test_a_repeat_spelled_with_a_closing_hash_sequence_is_reported(self):
        """CommonMark's other ATX spelling. A reviewer repeated a heading as
        "## Zed" and "## Zed ##" and the comparison, which kept the trailing
        hashes in the text, called them two different headings."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## Zed\n\nx\n\n## Zed ##\n\ny\n",
                encoding="utf-8")
            found = [row for row in self.findings(root) if row[0] == "note.md"]
            self.assertEqual(1, len(found), found)
            self.assertEqual(7, found[0][1])
            self.assertIn("on line 3", found[0][2])

    def test_a_repeated_setext_heading_is_reported(self):
        """The same reviewer's second spelling: a line of text underlined by
        "=" is a level-1 heading, and the reading took only ATX."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "Zed\n====\n\nx\n\nZed\n====\n\ny\n", encoding="utf-8")
            found = [row for row in self.findings(root) if row[0] == "note.md"]
            self.assertEqual(1, len(found), found)
            self.assertEqual(6, found[0][1])
            self.assertIn("on line 1", found[0][2])

    def test_a_dashed_setext_heading_is_read_as_level_two(self):
        """A "-" underline is level 2, so it repeats a sibling "## Zed" rather
        than a "# Zed"; without the level the two would never collide."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## Zed\n\nx\n\nZed\n---\n\ny\n",
                encoding="utf-8")
            found = [row for row in self.findings(root) if row[0] == "note.md"]
            self.assertEqual(1, len(found), found)
            self.assertEqual(7, found[0][1])

    def test_a_table_a_break_and_front_matter_are_not_setext_headings(self):
        """The positive control the widening owes: "-" also spells a table
        delimiter, a thematic break and the close of YAML front matter, and a
        reading that took those would report the tree it protects."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "---\ntitle: My Title\n---\n\n| a | b |\n|---|---|\n"
                "| c | d |\n\n---\n\n- item\n---\n\nparagraph\n",
                encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0] == "note.md"])

    def test_a_hash_inside_a_heading_is_not_a_closing_sequence(self):
        """The positive control for the other half: only a run of hashes with
        nothing after it is a closing sequence, so "## Hash # tag" keeps its
        hash and is a different heading from "## Hash"."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n## Hash # tag\n\nx\n\n## Hash\n\ny\n",
                encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0] == "note.md"])

    def test_a_heading_inside_a_fenced_block_is_not_a_heading(self):
        """A sample session that prints "## Stage" twice is output, not
        structure, and a check that cannot see a fence reports the sample."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "note.md").write_text(
                "# Note\n\n```\n## Stage\n## Stage\n```\n\n"
                "````\n```\n## Stage\n## Stage\n````\n", encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0] == "note.md"])


class DeclaredPathGateTests(unittest.TestCase):
    """The path a template declared and the tree never held.

    templates/ai/eval-spec.md sent a reader to
    "../architecture/ai-interaction-spec.md" from inside an HTML comment. That
    path is real from templates/definition/ and dead from templates/ai/, where
    it was written and where the file it means sits in the same directory. The
    link check above reads markdown links in five operator documents, so
    nothing in the tree resolved it.
    """

    WRONG = "../architecture/ai-interaction-spec.md"
    RIGHT = "./ai-interaction-spec.md"

    def findings(self, root):
        return [(item.path, item.line, item.message)
                for item in check_declared_paths(root)]

    def test_the_tree_as_it_stands_declares_no_dead_path(self):
        self.assertEqual([], self.findings(REPO))

    def test_the_eval_spec_comment_with_its_wrong_path_back_is_reported(self):
        """The audited defect, put back where the audit found it.

        The audit of 49ca7e8 read it at templates/ai/eval-spec.md:78. The line
        is computed here rather than pinned, because the section above it has
        since gained fields and a line number is not the defect.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "ai" / "eval-spec.md"
            text = document.read_text(encoding="utf-8")
            self.assertIn(self.RIGHT, text)
            broken = text.replace(self.RIGHT, self.WRONG, 1)
            document.write_text(broken, encoding="utf-8")
            line = broken.count("\n", 0, broken.index(self.WRONG)) + 1
            self.assertEqual(
                [("templates/ai/eval-spec.md", line,
                  "%r names no file in this tree" % self.WRONG)],
                self.findings(root))

    def test_a_path_real_from_another_template_is_still_read_from_this_one(self):
        """The defect class itself: the reference is not nonsense, it names a
        file that exists, at the depth it would have from somewhere else. A
        checker that resolved these against the repository root instead of
        against the file that wrote them would pass this one."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "ai" / "borrowed.md"
            document.write_text("# Borrowed\n\nSee ../os/STAGE-GATES.md.\n",
                                encoding="utf-8")
            self.assertTrue((root / "os" / "STAGE-GATES.md").is_file())
            self.assertEqual(
                [("templates/ai/borrowed.md", 3,
                  "'../os/STAGE-GATES.md' names no file in this tree")],
                [row for row in self.findings(root) if row[0].endswith("borrowed.md")])

    def test_a_reference_that_climbs_out_of_the_repository_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "ai" / "borrowed.md"
            document.write_text("# Borrowed\n\nSee ../../../secrets.md.\n",
                                encoding="utf-8")
            self.assertEqual(
                [("templates/ai/borrowed.md", 3,
                  "'../../../secrets.md' leaves the repository")],
                [row for row in self.findings(root) if row[0].endswith("borrowed.md")])

    def test_a_name_without_a_directory_is_not_read_as_a_path(self):
        """The stated limit, pinned so it is a decision and not a bug: a bare
        STATE.md in prose names a form, not a place."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "ai" / "borrowed.md"
            document.write_text("# Borrowed\n\nFill nowhere-near-here.md.\n",
                                encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0].endswith("borrowed.md")])


    def test_the_link_check_this_docstring_names_catches_what_it_says(self):
        """A stated limit may not lean on a mitigation that is not there. This
        check's docstring sends a reader to lint.py's LINK check for a markdown
        link whose target is missing, and an earlier wording claimed that
        covered the space form as well. It does not, and not because that gate
        is weak: CommonMark does not read an unbracketed destination containing
        a space as a link at all, so nothing renders it as one. The spelling
        that IS a link, with the destination in angle brackets, is read."""
        import lint  # noqa: PLC0415 -- the claim under test is lint's
        self.assertTrue(lint.LINK_RE.search("[a spec](./nope-xyz.md)"))
        self.assertTrue(lint.LINK_RE.search("[a spec](<./My Missing Spec.md>)"))
        self.assertIsNone(lint.LINK_RE.search("[a spec](./My Missing Spec.md)"))
        self.assertIn("CommonMark does not read",
                      check_declared_paths.__doc__)


class ExecutableSurfaceGateTests(unittest.TestCase):
    """SECURITY.md's inventory of tools/, held to the directory it describes.

    The file said "`tools/` holds eighteen scripts in all" while the directory
    held 27, and named tools/ext_ai_probe.py as the only script that calls out
    while tools/model_matrix.py had grown a urlopen of its own. Both sentences
    were true when they were typed. The inventory is generated now, and these
    tests fail when the generator stops reading the tree or the check stops
    reading the generator.
    """

    def test_the_generated_inventory_is_every_tracked_script_under_tools(self):
        """The closure proof the audit asked for: what the block counts is
        exactly what git tracks under tools/, not a list kept beside it."""
        # --others --exclude-standard as well as the index, so a script added
        # in the working tree and not yet staged counts: the inventory has to
        # describe the tree that is about to be committed, not the last one.
        tracked = subprocess.run(["git", "ls-files", "--cached", "--others",
                                  "--exclude-standard", "tools/"], cwd=REPO,
                                 capture_output=True, text=True, check=True,
                                 timeout=120).stdout.split()
        self.assertEqual(sorted(name for name in tracked if name.endswith(".py")),
                         ["tools/%s" % path.name
                          for path in exec_surface.scripts(REPO)])

    def test_the_committed_block_matches_the_tree(self):
        problem, _block = exec_surface.compare(REPO)
        self.assertIsNone(problem)
        self.assertEqual([], [item.as_dict()
                              for item in check_executable_surface(REPO)])

    def test_a_new_script_makes_the_committed_block_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text("x = 1\n", encoding="utf-8")
            messages = [item.message for item in check_executable_surface(root)]
            self.assertEqual(1, len(messages), messages)
            self.assertIn("does not match the tree", messages[0])

    def test_a_script_that_reaches_the_network_is_named_by_the_generator(self):
        """The second half of the defect: a count can be right while the list
        of exceptions is wrong."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text(
                "import urllib.request\n\n\ndef go():\n"
                "    return urllib.request.urlopen('https://example.invalid')\n",
                encoding="utf-8")
            block = exec_surface.render(root)
            self.assertIn("| `tools/invented.py` | no | yes |", block)

    def test_a_server_or_async_connection_is_named_too(self):
        """The first version of this generator read urllib, http.client and a
        socket, and a reviewer walked a script past it that spelled
        `import http.server` and `asyncio.open_connection`. It got no row, and
        the sentence over the table then said that script named no network
        primitive."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text(
                "import asyncio\nimport http.server\n\n\ndef go():\n"
                "    return asyncio.open_connection('h', 1)\n",
                encoding="utf-8")
            self.assertEqual((False, True),
                             exec_surface.facts(root / "tools" / "invented.py"))
            self.assertIn("| `tools/invented.py` | no | yes |",
                          exec_surface.render(root))

    def test_a_program_handed_to_a_subprocess_is_named_too(self):
        """The other half of the same gap: the call that leaves the machine is
        spelled as a string, not as an import."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text(
                "import subprocess\n\n\ndef go(url):\n"
                "    return subprocess.run(['curl', '-s', url], check=False)\n",
                encoding="utf-8")
            self.assertIn("| `tools/invented.py` | no | yes |",
                          exec_surface.render(root))

    def test_a_module_on_the_list_imported_by_name_is_named_too(self):
        """The second reviewer's walk-past. `import http.server` was read and
        `from http import server` was not, because only urllib had an
        ImportFrom case of its own -- while the block prints `http.server`,
        `http.client` and `xmlrpc.client` inside the list it claims against,
        so its disclaimer never covered these. This tree's own scripts spell
        `from X import Y` more than twenty times."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            script = root / "tools" / "invented.py"
            for source in ("from http import server\n",
                           "from http import client\n",
                           "from xmlrpc import client\n",
                           "from http.server import HTTPServer\n",
                           "from http import server as srv\n"):
                script.write_text(source, encoding="utf-8")
                self.assertEqual((False, True), exec_surface.facts(script),
                                 source)
            self.assertIn("| `tools/invented.py` | no | yes |",
                          exec_surface.render(root))

    def test_a_package_imported_alone_and_used_dotted_is_named_too(self):
        """The same hole one layer out: the import names only the package and
        the module on the list is spelled where it is used."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            script = root / "tools" / "invented.py"
            script.write_text("import http\n\n\ndef go():\n"
                              "    return http.server.HTTPServer(('', 0), None)\n",
                              encoding="utf-8")
            self.assertEqual((False, True), exec_surface.facts(script))
            self.assertIn("| `tools/invented.py` | no | yes |",
                          exec_surface.render(root))

    def test_a_module_beside_one_on_the_list_is_not_read(self):
        """The positive control the widening owes. urllib.parse is string
        handling and is deliberately off the list, tools/workspace.py imports
        it, and the suffix test is on a dot -- so "urllib.parse" is not
        "urllib.request" and an attribute rooted anywhere but a name is not a
        module at all."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            script = root / "tools" / "invented.py"
            for source in ("import urllib.parse\n\nX = urllib.parse.quote('a b')\n",
                           "from urllib import parse\n",
                           "import sslcheck\n",
                           "class C:\n    socket = 1\n\n\nX = C().socket\n"):
                script.write_text(source, encoding="utf-8")
                self.assertEqual((False, False), exec_surface.facts(script),
                                 source)

    def test_a_relative_import_is_not_a_network_module(self):
        """`from . import server` names tools/server.py, not the http
        package, and a reading that took the dotted join would say the tree's
        own sibling imports leave the machine."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            script = root / "tools" / "invented.py"
            script.write_text("from . import server\n", encoding="utf-8")
            self.assertEqual((False, False), exec_surface.facts(script))

    def test_the_block_names_the_spellings_its_reading_covers(self):
        """The claim and the code, pinned together: the block prints a list of
        modules, so it has to say that a module on it counts however the
        source spells the import, or a reader takes the list for a list of
        statements."""
        block = exec_surface.render(REPO)
        for spelling in ("`import http.server`", "`from http import server`",
                         "`from http.server import HTTPServer`"):
            self.assertIn(spelling, block)
        self.assertIn("counts however the source spells it", block)

    def test_the_word_curl_in_prose_is_not_a_call(self):
        """The positive control for the line above: only a string that IS the
        program counts, or every file that mentions one would carry a row."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text(
                '"""Explains why curl and ssh are not used here."""\n\n'
                "MESSAGE = 'run curl yourself'\n", encoding="utf-8")
            self.assertEqual((False, False),
                             exec_surface.facts(root / "tools" / "invented.py"))

    def test_the_block_prints_the_recognition_list_it_claims_against(self):
        """"Names no network primitive" is a statement about a fixed list, so
        the block has to print the list; without it the sentence reads as a
        claim about what a script can do."""
        block = exec_surface.render(REPO)
        self.assertIn("The network list this reading recognises, in full",
                      block)
        for name in ("http.server", "socketserver", "requests",
                     "open_connection", "curl"):
            self.assertIn("`%s`" % name, block)
        self.assertIn("not about what a script can do", block)

    def test_this_generator_does_not_classify_itself(self):
        """Its own constants name every module, call and program it looks for.
        Parsing rather than searching is what keeps them out, and a set literal
        inside frozenset(...) is what keeps the program names out."""
        self.assertEqual((False, False),
                         exec_surface.facts(TOOLS / "exec_surface.py"))

    def test_deleting_the_markers_fails_instead_of_passing(self):
        """Dropping the block is the cheapest way to drop the claim, so it has
        to be the loudest failure and not a silent pass."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            start = text.index(exec_surface.BEGIN)
            end = text.index(exec_surface.END) + len(exec_surface.END)
            document.write_text(text[:start] + text[end:], encoding="utf-8")
            messages = [item.message for item in check_executable_surface(root)]
            self.assertEqual(1, len(messages), messages)
            self.assertIn("no longer carries the executable-surface markers",
                          messages[0])

    def test_regenerating_a_stale_block_restores_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            document.write_text(
                document.read_text(encoding="utf-8").replace(
                    "`tools/` holds", "`tools/` allegedly holds", 1),
                encoding="utf-8")
            self.assertEqual(1, len(check_executable_surface(root)))
            self.assertEqual(0, quietly(exec_surface.main,
                                        ["--root", str(root)])[0])
            self.assertEqual([], check_executable_surface(root))


class ScriptCountGateTests(unittest.TestCase):
    """The script count where it is typed by hand, outside the generated block.

    Generating the inventory closed the sentence that carried the wrong number
    and left the page it sits on open. A reviewer re-typed "`tools/` holds
    eighteen scripts in all." into SECURITY.md's prose one line above the
    markers and every check stayed green, because the generator compares only
    what is between them. This is the gate-count technique applied to the
    second count on the same page.
    """

    STALE = "`tools/` holds eighteen scripts in all.\n\n"

    def findings(self, root):
        return [(item.path, item.line, item.message)
                for item in check_script_count(root)]

    def test_the_tree_as_it_stands_states_no_count_outside_the_block(self):
        self.assertEqual([], self.findings(REPO))

    def test_the_stale_sentence_re_typed_above_the_block_is_reported(self):
        """The bypass, exactly as the reviewer performed it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            document.write_text(
                text.replace(exec_surface.BEGIN, self.STALE + exec_surface.BEGIN, 1),
                encoding="utf-8")
            found = self.findings(root)
            self.assertEqual(1, len(found), found)
            self.assertIn("holds eighteen scripts", found[0][2])
            self.assertIn("tools/ holds %d script(s)"
                          % len(exec_surface.scripts(root)), found[0][2])

    def test_the_same_claim_below_the_block_is_reported_too(self):
        """The count does not become true by moving under the markers."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            document.write_text(
                text.replace(exec_surface.END, exec_surface.END + "\n\n" + self.STALE, 1),
                encoding="utf-8")
            self.assertEqual(1, len(self.findings(root)))

    def test_a_right_count_in_prose_passes_and_rots_loudly(self):
        """A hand-typed number is allowed while it is true, and reported the
        day the directory changes under it. That is the whole contract: a
        figure a reader cannot check is a figure nothing re-measures."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            total = len(exec_surface.scripts(root))
            sentence = "`tools/` holds %d scripts in all.\n\n" % total
            text = document.read_text(encoding="utf-8")
            document.write_text(
                text.replace(exec_surface.BEGIN, sentence + exec_surface.BEGIN, 1),
                encoding="utf-8")
            self.assertEqual([], self.findings(root))
            (root / "tools" / "invented.py").write_text("x = 1\n", encoding="utf-8")
            self.assertEqual(1, len(self.findings(root)))

    def test_a_stale_exception_count_in_the_prose_is_reported(self):
        """The other half of the same defect: the file named one script as the
        only one that leaves the machine while a second had grown a network
        call. That sentence sits in prose, above the generated table."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            self.assertIn("Two of them leave this path entirely", text)
            document.write_text(
                text.replace("Two of them leave this path entirely",
                             "One of them leave this path entirely", 1),
                encoding="utf-8")
            found = self.findings(root)
            self.assertEqual(1, len(found), found)
            self.assertIn("2 script(s) under tools/ name a network primitive",
                          found[0][2])

    def test_a_new_network_script_stales_that_sentence_too(self):
        """Not only a typo: adding a script that calls out makes the sentence
        wrong without anyone touching it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "tools" / "invented.py").write_text(
                "import http.server\n\n\ndef go():\n    return http.server\n",
                encoding="utf-8")
            messages = [row[2] for row in self.findings(root)]
            self.assertTrue(any("leave this path" in message
                                for message in messages), messages)

    def test_the_environment_only_count_is_read_as_well(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            self.assertIn("The other four scripts the table lists", text)
            document.write_text(
                text.replace("The other four scripts the table lists",
                             "The other five scripts the table lists", 1),
                encoding="utf-8")
            found = self.findings(root)
            self.assertEqual(1, len(found), found)
            self.assertIn("name an environment variable and no network "
                          "primitive", found[0][2])

    def test_the_stale_count_in_a_reworded_whole_directory_claim_is_reported(self):
        """The reviewer's second pass re-typed the same figure in two wordings
        the first shape did not read -- "contains" instead of "holds", and the
        directory named after the count instead of before it -- and both
        passed, on the same page and for the same reason as the original."""
        for sentence in ("`tools/` contains eighteen scripts.\n\n",
                         "There are 18 scripts under `tools/`.\n\n",
                         "18 scripts in `tools/` do the work.\n\n"):
            with tempfile.TemporaryDirectory() as tmp:
                root = copy_tree(tmp)
                document = root / "SECURITY.md"
                text = document.read_text(encoding="utf-8")
                document.write_text(
                    text.replace(exec_surface.BEGIN,
                                 sentence + exec_surface.BEGIN, 1),
                    encoding="utf-8")
                found = self.findings(root)
                self.assertEqual(1, len(found), (sentence, found))
                self.assertIn("tools/ holds %d script(s)"
                              % len(exec_surface.scripts(root)), found[0][2])

    def test_a_reworded_claim_that_is_right_passes(self):
        """The same contract as the wording above it: true today, reported the
        day the directory changes under it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            total = len(exec_surface.scripts(root))
            sentence = "`tools/` contains %d scripts.\n\n" % total
            text = document.read_text(encoding="utf-8")
            document.write_text(
                text.replace(exec_surface.BEGIN, sentence + exec_surface.BEGIN, 1),
                encoding="utf-8")
            self.assertEqual([], self.findings(root))
            (root / "tools" / "invented.py").write_text("x = 1\n",
                                                        encoding="utf-8")
            self.assertEqual(1, len(self.findings(root)))

    def test_a_count_of_a_named_subset_is_not_read(self):
        """The stated limit, pinned so it is a decision and not a bug:
        SECURITY.md's own "Six local scripts stay on this path" counts the six
        it then names, and holding it to the directory total would be wrong."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "SECURITY.md"
            text = document.read_text(encoding="utf-8")
            self.assertIn("Six local scripts stay on this path", text)
            document.write_text(
                text.replace("Six local scripts stay on this path",
                             "Six local scripts stay on this path, as do three "
                             "scripts named below", 1), encoding="utf-8")
            self.assertEqual([], self.findings(root))


class CommitmentProbeGateTests(unittest.TestCase):
    """The interview guide that bans the question it also requires.

    templates/discovery/interview-guide.md told its filler that no question
    may ask about the future, and required two lines later the Block E probe
    that asks what the participant would do next. The audit found it in the
    template. It was also in the template's filled example, in the mom-test
    framework worksheet, and in that worksheet's own filled example: six lines
    in four files, none of which any structural check read.
    """

    BANNED = ("- [x] No question asks about the idea, the future, or a price; "
              "every question asks about a specific past event or its cost\n")

    def findings(self, root):
        return [(item.path, item.line, item.message)
                for item in check_commitment_probe_rule(root)]

    def test_the_tree_as_it_stands_reconciles_every_guide_with_its_probe(self):
        self.assertEqual([], self.findings(REPO))

    def test_the_filled_example_with_its_pre_fix_line_back_is_reported(self):
        """The closure proof the finding states in its own words: the guide and
        its example agree. This is the example, with the line the audit read."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "examples" / "sahulat-interview-guide.md"
            text = document.read_text(encoding="utf-8")
            line = [number for number, raw
                    in enumerate(text.splitlines(), 1)
                    if raw.startswith("- [x] No question asks about the idea")]
            self.assertEqual(1, len(line))
            document.write_text(
                "\n".join(self.BANNED.rstrip("\n") if number == line[0] else raw
                          for number, raw
                          in enumerate(text.splitlines(), 1)) + "\n",
                encoding="utf-8")
            found = [row for row in self.findings(root)
                     if row[0] == "examples/sahulat-interview-guide.md"]
            self.assertEqual(1, len(found), found)
            self.assertEqual(line[0], found[0][1])
            self.assertIn("names no exemption", found[0][2])

    def test_the_framework_worksheet_rule_without_its_exemption_is_reported(self):
        """The same class one layer down, which no register record named and
        which shipped with the same contradiction."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = (root / "frameworks" / "discovery"
                        / "mom-test-interview-guide.md")
            text = document.read_text(encoding="utf-8")
            self.assertIn(", except in the closing commitment probe", text)
            document.write_text(
                text.replace(", except in the closing commitment probe", ""),
                encoding="utf-8")
            found = [row for row in self.findings(root)
                     if row[0].endswith("mom-test-interview-guide.md")]
            self.assertEqual(2, len(found), found)

    def test_the_ban_written_as_a_plain_bullet_is_reported(self):
        """The rule was read only on a table row or a checkbox item, so the
        same sentence one character shorter -- a plain bullet, or a numbered
        item -- stated the ban and named no exemption while the check stayed
        silent."""
        probe = ("| Close | What would you do next: try it, introduce us? "
                 "| commitment, not a compliment |\n")
        for rule in ("- Never ask what they would do in the future.\n",
                     "* Never ask what they would do in the future.\n",
                     "1. Never ask what they would do in the future.\n"):
            with tempfile.TemporaryDirectory() as tmp:
                root = copy_tree(tmp)
                document = root / "templates" / "discovery" / "invented.md"
                document.write_text("# Invented\n\n" + probe + "\n" + rule,
                                    encoding="utf-8")
                found = [row for row in self.findings(root)
                         if row[0].endswith("invented.md")]
                self.assertEqual(1, len(found), (rule, found))
                self.assertEqual(5, found[0][1])

    def test_a_rule_named_in_running_prose_is_not_read(self):
        """The stated limit, pinned so it is a decision and not a bug: the
        mom-test worksheet opens by summarising its own rules in a sentence
        ("not opinions about the future"), and a check that read paragraphs
        would demand an exemption clause from prose describing the rules."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "discovery" / "invented.md"
            document.write_text(
                "# Invented\n\n| Close | What would you do next? | commitment |"
                "\n\nThe rules ask about what happened, not the future.\n",
                encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0].endswith("invented.md")])

    def test_a_guide_that_asks_for_no_commitment_is_not_read(self):
        """The stated limit: the rule is read only where the probe is, so a
        questionnaire that bans the future and closes without a commitment ask
        is left alone."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "discovery" / "invented.md"
            document.write_text(
                "# Invented\n\n- [ ] No question asks about the future\n",
                encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0].endswith("invented.md")])

    def test_naming_the_exemption_is_what_clears_the_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            document = root / "templates" / "discovery" / "invented.md"
            probe = ("| Close | What would you do next: try it, introduce us? "
                     "| commitment, not a compliment |\n")
            document.write_text(
                "# Invented\n\n" + probe
                + "\n- [ ] No question asks about the future\n",
                encoding="utf-8")
            self.assertEqual(1, len([row for row in self.findings(root)
                                     if row[0].endswith("invented.md")]))
            document.write_text(
                "# Invented\n\n" + probe
                + "\n- [ ] No question asks about the future, except the "
                  "closing commitment probe\n", encoding="utf-8")
            self.assertEqual([], [row for row in self.findings(root)
                                  if row[0].endswith("invented.md")])


class GateCountGateTests(unittest.TestCase):
    """The other count nothing measured, for the same reason as the first.

    Three documents carried three numbers for one object and none was the
    object's: the README said 24 gates and 22 gates, the FAQ said twenty-one,
    and tools/ci_gate.py defined 25. Every one of them had been true once,
    which is how they survived: adding a gate is the moment they all go stale,
    and nothing re-read them. These tests fail if the check stops reading
    either the file or the documents.
    """

    def findings(self, root):
        return [(item.path, item.line, item.message) for item in check_gate_count(root)]

    def test_the_tree_as_it_stands_agrees_with_its_own_gate_file(self):
        self.assertEqual([], self.findings(REPO))

    def test_a_document_naming_the_wrong_count_beside_ci_gate_is_reported(self):
        total = len(ci_gate.GATES)
        stated = "%d gates as of this tree"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            readme = root / "README.md"
            text = readme.read_text(encoding="utf-8")
            self.assertIn(stated % total, text)
            readme.write_text(text.replace(stated % total, stated % (total - 1), 1),
                              encoding="utf-8")
            messages = [message for _path, _line, message in self.findings(root)]
            self.assertIn("this says '%d gates' and tools/ci_gate.py defines %d"
                          % (total - 1, total), messages)

    def test_adding_a_gate_makes_every_document_that_states_the_old_count_fail(self):
        """The direction the defect actually travels: the file grows, and the
        documents that were right yesterday are the ones that go wrong."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            gate_file = root / "tools" / "ci_gate.py"
            text = gate_file.read_text(encoding="utf-8")
            marker = '    Gate("readiness-local", ("python3", "tools/readiness.py", "--local"),\n'
            self.assertIn(marker, text)
            gate_file.write_text(
                text.replace(marker, '    Gate("invented", ("python3", "-c", "pass")),\n' + marker, 1),
                encoding="utf-8")
            paths = {path for path, _line, _message in self.findings(root)}
            self.assertEqual({"README.md", "docs/FAQ.md", "docs/ARCHITECTURE.md"},
                             paths)

    def test_restoring_twenty_two_on_either_architecture_line_is_reported(self):
        """docs/ARCHITECTURE.md said "twenty-two named gates" on the tree
        diagram's ci_gate.py line, which never names tools/, and "Its
        twenty-two gates" in prose, both while the file defined 25, and this
        check passed: it read digits only, and only in README.md and
        docs/FAQ.md. Putting either phrase back has to fail, naming its line."""
        total = len(ci_gate.GATES)
        # The words after each count, which do not move when the count does.
        for after, stated in ((" named gates in one pass", "twenty-two named gates"),
                              (" gates are the four checks above", "twenty-two gates")):
            with self.subTest(stated=stated), tempfile.TemporaryDirectory() as tmp:
                root = copy_tree(tmp)
                document = root / "docs" / "ARCHITECTURE.md"
                lines = document.read_text(encoding="utf-8").split("\n")
                hits = [number for number, line in enumerate(lines, 1)
                        if after in line]
                self.assertEqual(1, len(hits), after)
                line = lines[hits[0] - 1]
                end = line.index(after)
                start = line.rindex(" ", 0, end) + 1
                lines[hits[0] - 1] = line[:start] + "twenty-two" + line[end:]
                document.write_text("\n".join(lines), encoding="utf-8")
                self.assertEqual(
                    [("docs/ARCHITECTURE.md", hits[0],
                      "this says %r and tools/ci_gate.py defines %d"
                      % (stated, total))],
                    self.findings(root))

    def test_a_count_in_words_is_read_at_its_value(self):
        """"Twenty Six" is twenty-six, not six and not a miss, and "seventeen"
        is not "seven". A misread count fails a document that is right, or
        passes one that is wrong whenever the misreading happens to equal the
        total. A count opening a sentence is read like any other, and a line
        that names neither form of the file is not read."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "fixture"
            (root / "tools").mkdir(parents=True)
            (root / "tools" / "ci_gate.py").write_text(
                "GATES = (%s)\n" % ", ".join(["None"] * 26), encoding="utf-8")
            (root / "README.md").write_text(
                "`ci_gate.py` runs Twenty Six gates.\n"
                "`ci_gate.py` runs twenty-six named gates.\n"
                "`ci_gate.py` runs seventeen gates.\n"
                "`tools/ci_gate.py` runs 26 release gates.\n"
                "`tools/ci_gate.py` runs sixteen gates.\n"
                "The suite runs nine gates.\n"
                "See `ci_gate.py`. Twenty-five gates run there.\n",
                encoding="utf-8")
            self.assertEqual(
                [("README.md", 3, "this says 'seventeen gates' and "
                                  "tools/ci_gate.py defines 26"),
                 ("README.md", 5, "this says 'sixteen gates' and "
                                  "tools/ci_gate.py defines 26"),
                 ("README.md", 7, "this says 'Twenty-five gates' and "
                                  "tools/ci_gate.py defines 26")],
                self.findings(root))

    def test_a_tree_without_the_gate_file_makes_no_claim(self):
        """A fixture root is not a defect. The check reports nothing rather
        than holding documents to a number it could not measure."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bare"
            (root / "docs").mkdir(parents=True)
            (root / "README.md").write_text(
                "See `tools/ci_gate.py`, which runs 99 gates.\n", encoding="utf-8")
            self.assertEqual([], self.findings(root))


class ReadinessClaimGateTests(unittest.TestCase):
    """What a development-ready report leaves uncertified, which nothing checked.

    The quickstart's readiness section used to list what readiness requires
    and say nothing of what it does not, so a reader could take
    development_ready to mean the answers were evidenced. Three statements now
    say otherwise. Each seed below removes, rewords, moves, hides or
    contradicts them and runs the gate the way CI does, and a few check that
    what should pass does. The hedged-sentence seed matters most: it keeps the
    keywords and drops only the clause that makes the sentence a limit, and a
    rule that passed it would be a spelling test.
    """

    SOURCE = ("Whether an answer cites a workspace document, and whether a quotation it\n"
              "supplies was found there, is reported, as `quote_verified`,\n"
              "`source_verified` and `supplied_unverified` in `pmos status --json` at the\n"
              "top level and again per phase under `completed`, and under `evidence` in the\n"
              "handoff package and in `handoff/CONTEXT.md`, and is a condition of nothing.")
    EVIDENCED = ("It does not certify that every answer is evidenced:\n"
                 "a product whose every answer is `supplied_unverified` can be\n"
                 "development-ready.")
    ACTOR = ("It does not certify that a typed actor ID is\n"
             "authenticated: `pmos gate` records the ID it was given and stamps the\n"
             "approval a local attestation.")

    def gate(self, root):
        """Run tools/docs_contract.py --strict against root, as ci_gate does."""
        return quietly(docs_contract_main, ["--root", str(root), "--strict"])

    def seeded(self, tmp, old, new):
        root = copy_tree(tmp)
        path = root / "docs" / "RUNTIME-QUICKSTART.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(1, text.count(old), "the seed no longer matches the quickstart")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return root

    def assertNames(self, output, claim):
        self.assertIn("docs/RUNTIME-QUICKSTART.md", output)
        self.assertIn("no longer says that " + claim, output)

    def test_every_pin_ends_with_its_own_full_stop(self):
        """_as_sentence checks where a pin starts and not where it ends,
        which is sound only while each pin closes its own sentence."""
        for sentence in [s for _, s in READINESS_CLAIMS] + [README_READINESS]:
            with self.subTest(sentence=sentence[:30]):
                self.assertTrue(sentence.endswith("."))

    def test_the_tree_as_it_stands_makes_all_three_statements(self):
        self.assertEqual([], check_readiness_claims(REPO))

    def test_deleting_the_condition_of_nothing_sentence_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.SOURCE, ""))
        self.assertEqual(1, code)
        self.assertNames(output, "source verification is reported and is a "
                                 "condition of nothing")

    def test_deleting_the_evidence_non_certification_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.EVIDENCED, ""))
        self.assertEqual(1, code)
        self.assertNames(output, "a development-ready report does not certify "
                                 "that every answer is evidenced")

    def test_deleting_the_actor_non_certification_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, ""))
        self.assertEqual(1, code)
        self.assertNames(output, "a development-ready report does not certify "
                                 "that a typed actor id is authenticated")

    def test_the_hedged_sentence_that_keeps_the_keywords_still_fails(self):
        """Reported, and in the right places, and a condition of nothing no
        longer: the weaker sentence has to fail, or the rule checks spelling."""
        hedged = ("Source verification is reported in the handoff package and in "
                  "`pmos status --json`.")
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.SOURCE, hedged))
        self.assertEqual(1, code)
        self.assertNames(output, "source verification is reported and is a "
                                 "condition of nothing")
        self.assertNotIn("every answer is evidenced", output)

    def test_moving_the_statements_out_of_the_handoff_section_fails(self):
        """The section is the scope: the same words under another heading are
        not where a reader of the readiness conditions looks."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.seeded(tmp, "## Development handoff\n", "## Handoff notes\n")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertEqual(3, output.count("readiness-claim"))

    def test_an_inverted_condition_of_nothing_sentence_fails(self):
        """Every keyword the earlier rule asked for, and the claim reversed."""
        inverted = ("Whether an answer cites a workspace document is reported, and it is "
                    "no longer a condition of nothing: readiness now refuses a product "
                    "with any supplied_unverified answer.")
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.SOURCE, inverted))
        self.assertEqual(1, code)
        self.assertNames(output, "source verification is reported and is a "
                                 "condition of nothing")
        self.assertIn("makes source verification a condition of something", output)

    def test_an_affirmed_every_answer_is_evidenced_fails(self):
        inverted = "It does not certify anything it cannot see, and every answer is evidenced."
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.EVIDENCED, inverted))
        self.assertEqual(1, code)
        self.assertNames(output, "a development-ready report does not certify "
                                 "that every answer is evidenced")
        self.assertIn("says every answer is evidenced", output)

    def test_a_contradiction_added_beside_the_pinned_sentences_fails(self):
        """The three sentences intact and a fourth that takes them back."""
        added = self.ACTOR + " In practice every gate actor is authenticated."
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, added))
        self.assertEqual(1, code)
        self.assertNotIn("no longer says", output)
        self.assertIn("says an actor id is authenticated", output)

    def test_a_source_verification_floor_added_beside_them_fails(self):
        """The runtime has no min_source_verified floor, and only the pattern
        naming one catches this sentence."""
        added = self.ACTOR + " The runtime has a min_source_verified floor of one answer."
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, added))
        self.assertEqual(1, code)
        self.assertNotIn("no longer says", output)
        self.assertIn("describes a source-verification floor the runtime does not have",
                      output)

    def test_verification_made_a_condition_of_readiness_fails(self):
        """The condition-of pattern's first half, which needs no "no longer"."""
        added = self.ACTOR + " Source verification is a condition of readiness."
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, added))
        self.assertEqual(1, code)
        self.assertNotIn("no longer says", output)
        self.assertIn("makes source verification a condition of something", output)

    def test_a_sentence_that_agrees_with_the_pin_passes(self):
        """"A condition of nothing" said again beside the pins restates the
        claim, and is no contradiction of it."""
        added = self.ACTOR + " Evidence stays a condition of nothing."
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, added))
        self.assertEqual(0, code, output)

    def test_a_statement_moved_below_the_next_heading_fails(self):
        """The section ends at the next level-2 heading, so a pinned sentence
        moved under that heading is not in it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.seeded(tmp, self.ACTOR, "")
            path = root / "docs" / "RUNTIME-QUICKSTART.md"
            text = path.read_text(encoding="utf-8")
            after = "## Adopting revised question banks\n"
            self.assertEqual(1, text.count(after))
            path.write_text(text.replace(after, after + "\nMoved here. " + self.ACTOR + "\n"),
                            encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertNames(output, "a development-ready report does not certify "
                                 "that a typed actor id is authenticated")

    def test_a_heading_that_only_mentions_the_section_is_not_it(self):
        """The section starts at the line that is its heading. An H3 whose text
        contains "## Development handoff" is not that line."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / "docs" / "RUNTIME-QUICKSTART.md"
            text = path.read_text(encoding="utf-8")
            path.write_text("### Development handoff, in brief\n\n" + text, encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(0, code, output)

    def test_readiness_made_to_turn_on_evidence_fails(self):
        """Only the refuses, blocks or requires pattern catches these two."""
        for added in ("Readiness requires that every answer be source_verified.",
                      "pmos handoff refuses a product with supplied_unverified answers."):
            with self.subTest(added=added), tempfile.TemporaryDirectory() as tmp:
                code, output = self.gate(self.seeded(tmp, self.ACTOR,
                                                     self.ACTOR + " " + added))
                self.assertEqual(1, code)
                self.assertNotIn("no longer says", output)
                self.assertIn("makes readiness turn on how answers are evidenced", output)

    def test_a_pinned_sentence_prefixed_into_its_negation_fails(self):
        """The words of the pin intact inside a sentence that denies them. A
        substring test passed this; the pin has to stand as its own sentence."""
        denied = "It is false that " + self.SOURCE[0].lower() + self.SOURCE[1:]
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.SOURCE, denied))
        self.assertEqual(1, code)
        self.assertNames(output, "source verification is reported and is a "
                                 "condition of nothing")

    def test_a_pinned_sentence_negated_across_a_colon_or_semicolon_fails(self):
        """A colon or a semicolon does not end a sentence, so the pin after
        one sits inside the sentence that denies it."""
        for mark in (":", ";"):
            denied = "It is false%s %s%s" % (mark, self.ACTOR[0].lower(), self.ACTOR[1:])
            with self.subTest(mark=mark), tempfile.TemporaryDirectory() as tmp:
                code, output = self.gate(self.seeded(tmp, self.ACTOR, denied))
                self.assertEqual(1, code)
                self.assertNames(output, "a development-ready report does not "
                                         "certify that a typed actor id is authenticated")

    def test_the_readme_mirror_negated_across_a_colon_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            readme = root / "README.md"
            text = readme.read_text(encoding="utf-8")
            self.assertEqual(1, text.count("Readiness is structural:"))
            readme.write_text(text.replace("Readiness is structural:",
                                           "It is untrue: readiness is structural:"),
                              encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertIn("README.md no longer mirrors", output)

    def test_the_readme_mirror_prefixed_into_its_negation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            readme = root / "README.md"
            text = readme.read_text(encoding="utf-8")
            self.assertEqual(1, text.count("Readiness is structural:"))
            readme.write_text(text.replace("Readiness is structural:",
                                           "It is untrue that readiness is structural:"),
                              encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertIn("README.md no longer mirrors", output)

    def test_dropping_the_readme_mirror_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            readme = root / "README.md"
            text = readme.read_text(encoding="utf-8")
            start = text.index("Readiness is structural:")
            end = text.index("That is the mechanism", start)
            readme.write_text(text[:start] + text[end:], encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertIn("README.md no longer mirrors the quickstart's readiness limits", output)

    # A pin a reader cannot see states nothing. Each seed below puts pinned
    # text inside an HTML comment, which a renderer does not show, where the
    # text as written still reads as the pinned sentence.

    def hidden(self, tmp, first, last):
        """The tree with the quickstart's text from first through last commented out."""
        text = (REPO / "docs" / "RUNTIME-QUICKSTART.md").read_text(encoding="utf-8")
        start = text.index(first)
        end = text.index(last, start) + len(last)
        return self.seeded(tmp, text[start:end], "<!--\n" + text[start:end] + "\n-->")

    def assertAllThreeMissing(self, code, output):
        self.assertEqual(1, code)
        self.assertEqual(3, output.count("readiness-claim"))
        for name, _sentence in READINESS_CLAIMS:
            self.assertNames(output, name)

    def test_the_statements_hidden_in_a_comment_fail(self):
        """Both paragraphs commented out: in the text as written each pin
        still starts a sentence, and none of them renders."""
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.hidden(tmp, "Readiness is structural. Every",
                                                 "approval a local attestation."))
        self.assertAllThreeMissing(code, output)

    def test_the_heading_hidden_in_a_comment_fails(self):
        """Only the heading commented out: the three statements still render,
        under the section above it, and a heading that does not render is not
        the section, so none of them is found in it. The finding names line 1,
        as for a heading that is gone."""
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.hidden(tmp, "## Development handoff",
                                                 "## Development handoff"))
        self.assertAllThreeMissing(code, output)
        self.assertIn("docs/RUNTIME-QUICKSTART.md:1: error readiness-claim", output)

    def test_a_contradiction_inside_a_comment_still_fails(self):
        """The contradictions are looked for in the text as written, so a
        comment is no place to keep one: whoever reads the raw file, an agent
        included, reads it."""
        added = self.ACTOR + " <!-- In practice every gate actor is authenticated. -->"
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.ACTOR, added))
        self.assertEqual(1, code)
        self.assertNotIn("no longer says", output)
        self.assertIn("says an actor id is authenticated", output)

    def test_a_comment_left_open_hides_the_rest_of_the_file(self):
        """A comment that opens a line and never closes hides everything after
        it, so the statements below it are not stated."""
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, "Readiness is structural. Every",
                                                 "<!--\nReadiness is structural. Every"))
        self.assertAllThreeMissing(code, output)

    def test_a_comment_opened_in_code_joins_nothing(self):
        """A "<!--" in a code span renders as itself, so the words after it
        show, and here they deny the pin. Taking them for a comment must not
        join what is left into a sentence that satisfies the pin."""
        denied = "Done. `<!--` It is false that --> " + self.SOURCE
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.gate(self.seeded(tmp, self.SOURCE, denied))
        self.assertEqual(1, code)
        self.assertNames(output, "source verification is reported and is a "
                                 "condition of nothing")

    def test_comments_around_the_section_change_nothing_else(self):
        """A comment above the section and one below it: the statements
        between them still count, and a finding still names the heading's own
        line, because each comment keeps the line breaks it held."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.seeded(tmp, self.ACTOR, "")
            path = root / "docs" / "RUNTIME-QUICKSTART.md"
            text = path.read_text(encoding="utf-8")
            after = "## Adopting revised question banks"
            self.assertEqual(1, text.count(after))
            text = "<!--\nOne.\nTwo.\n-->\n" + text.replace(
                after, "<!-- a closing note -->\n\n" + after)
            path.write_text(text, encoding="utf-8")
            heading = text.split("\n").index("## Development handoff") + 1
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertEqual(1, output.count("readiness-claim"))
        self.assertIn("docs/RUNTIME-QUICKSTART.md:%d: error readiness-claim" % heading, output)
        self.assertNames(output, "a development-ready report does not certify "
                                 "that a typed actor id is authenticated")

    def test_the_readme_mirror_hidden_in_a_comment_fails(self):
        """The paragraph commented out, so the mirror still starts a sentence
        of the text as written, and does not render."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            readme = root / "README.md"
            text = readme.read_text(encoding="utf-8")
            start = text.index("A product is development-ready only once")
            last = "typed actor ID is authenticated."
            end = text.index(last, start) + len(last)
            readme.write_text(text[:start] + "<!-- " + text[start:end] + " -->" + text[end:],
                              encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code)
        self.assertIn("README.md no longer mirrors", output)


class ReadinessChangelogTests(unittest.TestCase):
    """The CHANGELOG entry for the Gate 5 report defect names what it must.

    This checks that the entry names the affected surfaces, the unaffected one,
    the origin and the no-change-to-approval scope. It cannot check that those
    statements are true: that is read against R1's diff by a reviewer.
    """

    def entry(self):
        text = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
        entries = [line for line in text.splitlines()
                   if line.startswith("- ") and "AI overlay: guardrails live, kill switch tested" in line]
        self.assertEqual(1, len(entries), "the Gate 5 report entry is missing or duplicated")
        return entries[0]

    def test_the_entry_names_every_surface_and_its_scope(self):
        entry = self.entry()
        for phrase in ("from 0.8.0", "`pmos status --json`", "`pmos_status`",
                       "The human `pmos status` view never showed it",
                       "nothing about what can be approved"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, entry)


class ProseMetricsTests(unittest.TestCase):
    """The whole-file prose measurement, and the quickstart held to it.

    The refusal paragraph in docs/RUNTIME-QUICKSTART.md was 341 words, measured
    over a line window. A window can be satisfied by moving the paragraph
    below it, so the bar is taken over every block in the file instead.
    """

    LIMIT = 120

    def test_the_quickstart_has_no_prose_block_over_the_limit(self):
        text = (REPO / "docs" / "RUNTIME-QUICKSTART.md").read_text(encoding="utf-8")
        line, words = prose_metrics.longest_prose_block(text)
        self.assertLessEqual(words, self.LIMIT,
                             "docs/RUNTIME-QUICKSTART.md:%d is a %d-word block" % (line, words))

    def test_a_long_block_moved_below_a_table_is_still_found(self):
        """The seed the acceptance names: a table where the paragraph was and
        the paragraph pushed past line 145. A line window misses it."""
        paragraph = " ".join(["word"] * 341) + "."
        text = ("| a | b |\n|---|---|\n| 1 | 2 |\n" + "\n" * 150
                + paragraph + "\n")
        line, words = prose_metrics.longest_prose_block(text)
        self.assertEqual((line, words), (154, 341))

    def test_one_trailing_list_line_does_not_hide_a_paragraph(self):
        """The bypass an earlier version had: any list-like line in a block made
        the whole block non-prose, so one '- ...' line hid 341 words."""
        paragraph = " ".join(["word"] * 341) + "."
        text = ("| a | b |\n|---|---|\n\n" + paragraph
                + "\n- In short: see the table above.\n")
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 341))

    def test_a_multi_line_comment_is_not_prose(self):
        filler = " ".join(["word"] * 200)
        text = "<!-- a note\n" + filler + "\n-->\nFive words of prose here.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 5))

    def half(self, count=102):
        return " ".join(["word"] * count)

    def test_a_wrapped_line_opening_with_a_number_other_than_one_stays_in_its_paragraph(self):
        """CommonMark lets only an ordered list starting at 1 interrupt a
        paragraph, so this renders as one 205-word paragraph."""
        text = self.half() + "\n2026. The runtime " + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 205))

    def test_a_wrapped_line_opening_with_a_pipe_stays_in_its_paragraph(self):
        """A "|" line with no delimiter row under it is not a table."""
        text = self.half() + "\n| are split " + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 205))

    def test_a_marker_indented_four_spaces_stays_in_its_paragraph(self):
        text = self.half() + "\n    - and " + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 204))

    def test_an_empty_first_item_stays_in_its_paragraph(self):
        """An empty list item cannot interrupt a paragraph either."""
        text = self.half() + "\n1. \n" + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 203))

    def test_a_delimiter_row_with_the_wrong_cell_count_is_not_a_table(self):
        """GFM makes a table only when header and delimiter agree on columns."""
        text = self.half() + "\n| a | b |\n|---|\n" + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 208))

    def test_prose_under_a_heading_that_ends_a_list_item_is_prose(self):
        """A heading interrupts a list item's lazy continuation, so what
        follows the heading is not absorbed into the item."""
        text = "- item\n# Heading\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_list_items_lazy_continuation_is_not_prose(self):
        text = "- item " + self.half(5) + "\n" + self.half(200) + "\nShort.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (0, 0))

    def test_a_table_ends_a_list_items_continuation(self):
        """The line after the table is measured, as the docstring's over-count
        note says, rather than folded back into the list item."""
        text = "- item\n| h |\n|---|\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 200))

    def test_what_does_interrupt_a_paragraph_still_ends_it(self):
        """The other side of the rules above: an ordered item at 1, a bullet,
        a heading, a quote, a comment and a real table each end the paragraph,
        and are not counted in it."""
        for opener in ("1. first " + self.half(), "- item " + self.half(),
                       "# Heading " + self.half(), "> quote " + self.half(),
                       "<!-- note " + self.half() + " -->",
                       "| h |\n|---|\n| %s |" % self.half()):
            with self.subTest(opener=opener[:10]):
                text = "Five words of prose here.\n" + opener + "\n"
                self.assertEqual(prose_metrics.longest_prose_block(text), (1, 5))

    # Each seed below hid a paragraph from an earlier version of the scanner:
    # a renderer shows the 200 words as a paragraph, and the ceiling check
    # measured fewer.

    def test_a_comment_after_a_list_item_ends_its_continuation(self):
        text = "- item\n<!-- c -->\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_thematic_break_is_not_a_list_item(self):
        """"* * *" and "- - -" match a bullet; they are rules, and the
        paragraph after one is prose."""
        for rule in ("* * *", "- - -", "_ _ _", "***"):
            with self.subTest(rule=rule):
                text = "intro line\n" + rule + "\n" + self.half(200) + "\n"
                self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_thematic_break_ends_a_paragraph_and_is_not_counted(self):
        text = "Five words of prose here.\n***\nFour more words here.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 5))

    def test_an_item_whose_text_is_a_rule_takes_no_continuation(self):
        text = "- ***\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_an_indented_rule_under_an_item_ends_its_continuation(self):
        text = "- item\n    ***\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_an_ordered_marker_has_at_most_nine_digits(self):
        """CommonMark caps an ordered marker at nine digits, so a line opening
        with a ten-digit number is prose, and the paragraph it opens is too."""
        text = "1234567890. x\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 202))

    def test_a_ten_digit_number_inside_a_quote_is_its_text(self):
        """The same cap inside a container: "> 1234567890. # h" is a quoted
        paragraph, so the line after it is its lazy continuation."""
        text = "> 1234567890. # h\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (0, 0))

    def test_an_empty_bullet_stays_in_its_paragraph(self):
        text = self.half() + "\n- \n" + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 203))

    def test_a_fence_closes_only_on_its_own_character(self):
        text = "```\ncode\n~~~\nstill code\n```\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (6, 200))

    def test_a_fence_closes_only_on_as_many_markers(self):
        text = "````\n```\ncode\n````\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (5, 200))

    def test_a_fence_line_with_an_info_string_does_not_close_one(self):
        text = "```\n```python\n```\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 200))

    def test_a_closing_fence_is_indented_at_most_three_spaces(self):
        """Four spaces in, the line is code, so the fence runs to the end."""
        text = "```\n    ```\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (0, 0))

    def test_backticks_with_a_backtick_after_them_open_no_fence(self):
        text = "``` a`b\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 202))

    def test_a_blank_line_does_not_end_a_comment(self):
        """A comment runs to its "-->", blank lines included. Ending it at the
        blank made the fence inside it open, and swallow what followed."""
        text = "<!--\n\n```\n-->\n" + self.half(200) + "\n```\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (5, 200))

    def test_a_table_ends_at_a_line_less_indented_than_its_header(self):
        """A table inside a list item ends with the item; the "|" line after
        it, at the margin, opens a paragraph."""
        text = "- a\n\n  | h |\n  |---|\n| row " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (5, 202))

    def test_an_item_indented_four_columns_takes_no_continuation(self):
        text = "    - x\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_a_deeply_indented_item_under_a_quote_ends_the_lazy_run(self):
        """markdown-it reads the 200 words as a paragraph, CommonMark as lazy
        text; the scanner takes the reading that counts them."""
        text = ">> x\n    - x\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_an_item_holding_indented_code_takes_no_continuation(self):
        for item in ("-     code", "-\t\tcode"):
            with self.subTest(item=item):
                text = item + "\n" + self.half(200) + "\n"
                self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_an_item_holding_a_link_definition_takes_no_continuation(self):
        text = "- [a]: /u\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_an_item_holding_a_table_row_takes_no_continuation(self):
        text = "- | a |\n  |---|\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 201))

    def test_an_empty_item_or_quote_takes_no_continuation(self):
        """An empty item or quote holds no paragraph, so the line after it
        opens one of its own."""
        for opener in ("-", "- ", ">", "1."):
            with self.subTest(opener=opener):
                text = opener + "\n" + self.half(200) + "\n"
                self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_an_item_holding_a_heading_takes_no_continuation(self):
        text = "- # h\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    # Each seed below is held by one reset in prose_blocks: take the reset out
    # and the scanner measures (0, 0) where a renderer shows the 200 words as
    # a paragraph.

    def test_a_fence_ends_a_list_items_continuation(self):
        """A fence at the margin ends the list, so the paragraph after the
        fence is not the item's lazy continuation."""
        text = "- item\n```\ncode\n```\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (5, 200))

    def test_a_blank_line_ends_a_table(self):
        """A "|" line after the blank opens a paragraph, not another row."""
        text = "| a |\n|---|\n| b |\n\n| " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (5, 201))

    def test_a_thematic_break_ends_a_list_items_continuation(self):
        text = "- item\n***\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_blank_line_ends_a_list_items_continuation(self):
        """Lazy continuation stops at a blank line. The quickstart has this
        shape: the readiness list, a blank line, then the paragraph that
        states what readiness leaves uncertified."""
        text = "- item\n\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_fence_ends_a_table(self):
        """The "|" line after the fence opens a paragraph, not another row."""
        text = "| a |\n|---|\n```\ncode\n```\n| " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (6, 201))

    def test_a_line_that_is_not_a_row_ends_a_table(self):
        """A heading ends the table, so the "|" line after it is a paragraph."""
        text = "| a |\n|---|\n# h\n| " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 201))

    # Each seed below is held by one alternative of a pattern above, or one
    # clause of a helper: take it out and the measure differs from what a
    # CommonMark renderer with GFM tables shows, often by losing the 200-word
    # paragraph.

    def test_a_tilde_fence_is_a_fence(self):
        """Its contents are code, not a list item whose lazy lines would take
        the paragraph after the closing fence."""
        text = "~~~\n- item\n~~~\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 200))

    def test_two_backticks_open_no_fence(self):
        """Two are a code span inside a paragraph; a fence takes three."""
        text = "``\n" + self.half(200) + "\n``\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 202))

    def test_a_rule_indented_four_spaces_does_not_end_a_paragraph(self):
        text = self.half(200) + "\n    ***\n" + self.half(100) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 301))

    def test_three_dashes_after_a_blank_line_are_a_rule(self):
        """After a blank line they are no setext underline but a rule, and the
        paragraph after the rule is measured on its own."""
        text = "Two words.\n\n---\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 200))

    def test_two_dashes_are_not_a_rule(self):
        text = "Two words.\n\n--\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 201))

    def test_a_rule_has_nothing_else_on_its_line(self):
        text = "Two words.\n\n***x " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 201))

    def test_seven_hashes_are_not_a_heading(self):
        """Text wherever they stand: opening a block, inside a paragraph, and
        on a list item's lazy line."""
        for text, expected in (("####### " + self.half(200) + "\n", (1, 201)),
                               (self.half() + "\n####### " + self.half(100) + "\n", (1, 203)),
                               ("- item\n####### " + self.half(200) + "\n", (0, 0))):
            with self.subTest(text=text[:12]):
                self.assertEqual(prose_metrics.longest_prose_block(text), expected)

    def test_a_hash_with_no_space_after_it_is_not_a_heading(self):
        for text, expected in (("#hashtag " + self.half(200) + "\n", (1, 201)),
                               (self.half() + "\n#hashtag " + self.half(100) + "\n", (1, 203)),
                               ("- item\n#hashtag " + self.half(200) + "\n", (0, 0))):
            with self.subTest(text=text[:12]):
                self.assertEqual(prose_metrics.longest_prose_block(text), expected)

    def test_a_dash_with_no_space_after_it_is_not_a_bullet(self):
        """"-->" opens a paragraph, and "--" on an item's lazy line is its
        text, not a sibling item."""
        for text, expected in (("--> " + self.half(200) + "\n", (1, 201)),
                               ("- item\n--\n" + self.half(200) + "\n", (0, 0))):
            with self.subTest(text=text[:8]):
                self.assertEqual(prose_metrics.longest_prose_block(text), expected)

    def test_a_number_with_no_space_after_its_dot_is_not_an_item(self):
        text = "2026.5 percent " + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 202))

    def test_an_ordered_item_holding_a_heading_takes_no_continuation(self):
        text = "- item\n1. # h\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_sibling_item_holding_a_heading_takes_no_continuation(self):
        text = "- item\n- # h\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (3, 200))

    def test_a_heading_in_an_item_in_a_quote_takes_no_continuation(self):
        """Every container marker is read, not only the first."""
        text = "> - # h\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_a_tab_before_a_marker_is_four_columns(self):
        """Four columns in, the line is indented code, not a list item whose
        lazy lines would take the paragraph after it."""
        text = "\t- item\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (2, 200))

    def test_a_row_indented_four_spaces_starts_no_table(self):
        """Inside a paragraph it is paragraph text, and so is the delimiter
        row under it."""
        text = self.half(200) + "\n    | h |\n|---|\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 204))

    def test_a_delimiter_row_indented_four_spaces_starts_no_table(self):
        text = "| starts " + self.half(200) + "\n    |---|\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 203))

    def test_a_delimiter_row_has_nothing_else_on_its_line(self):
        """"- item" begins like a delimiter row and is a list item, so the
        "|" line above it is a paragraph, not a table header."""
        text = "| " + self.half(200) + "\n- item\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 201))

    def test_outer_pipes_are_optional_on_either_row(self):
        """A header and a delimiter row that differ in their outer pipes still
        make a table, so the header is not prose. A delimiter row with no
        leading "|" is itself counted, one word here, as prose_blocks says."""
        for delimiter in ("---|---|", "|---|---"):
            with self.subTest(delimiter=delimiter):
                text = "| a | b |\n" + delimiter + "\n\nFive words of prose here.\n"
                self.assertEqual(prose_metrics.longest_prose_block(text), (4, 5))

    def test_an_escaped_pipe_does_not_split_a_cell(self):
        text = "| a \\| b | c |\n|---|---|\n\nFive words of prose here.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (4, 5))

    def test_a_fence_ends_the_paragraph_before_it(self):
        text = self.half(200) + "\n```\ncode\n```\nFive words of prose here.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 200))

    def test_a_table_ends_the_paragraph_before_it(self):
        """The line under the table, which prose_blocks counts as prose (its
        docstring says why), is a block of its own and does not rejoin the
        paragraph above the table."""
        text = self.half(200) + "\n| a |\n|---|\nFive more words here now.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 200))

    def test_a_heading_ends_the_paragraph_before_it(self):
        text = "Five words of prose here.\n# Heading\nFour more words here.\n"
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, 5))

    def test_a_one_line_comment_does_not_hide_the_line_after_it(self):
        """The indented fence on line 2 is something this does not read, so
        the whole file is measured as one block. Were the comment on line 1
        taken to run on, line 2 would be skipped, and the margin fence on
        line 4 would open a fence that hides the paragraph."""
        text = "<!-- c -->\n  ```\ncode\n```\n" + self.half(200) + "\n"
        self.assertEqual(prose_metrics.unmodelled_line(text), 2)
        self.assertEqual(prose_metrics.longest_prose_block(text), (1, len(text.split())))

    def test_what_it_does_not_read_is_measured_whole(self):
        """Each of these holds a paragraph the scanner, reading on, would miss:
        a fence or comment a list item or indent holds, or raw HTML. The file
        is then one block, and the ceiling fails."""
        for seed in ("  ```\n```\n", "  <!--\n```\n-->\n", "<div>\n```\n</div>\n\n",
                     "- ```\n   1. x\n", "> <!-- c\n> 1. x\n", "  ~~~\n~~~\n",
                     "  <div>\n```\n</div>\n\n", "- ~~~\n   1. x\n", "1. ```\n   1. x\n"):
            with self.subTest(seed=seed):
                text = seed + self.half(200) + "\n"
                self.assertEqual(prose_metrics.unmodelled_line(text), 1)
                self.assertEqual(prose_metrics.longest_prose_block(text),
                                 (1, len(text.split())))

    def test_a_margin_comment_and_fenced_html_are_read(self):
        """What the refusal above does not reach: a comment at the margin, and
        HTML or an indented fence line inside a fence or a comment."""
        for text in ("<!-- a note -->\nFive words of prose here.\n",
                     "```\n<div>\n    ```\n```\nFive words of prose here.\n",
                     "<!--\n<div>\n  ```\n-->\nFive words of prose here.\n"):
            with self.subTest(text=text[:12]):
                self.assertEqual(prose_metrics.unmodelled_line(text), 0)
                self.assertEqual(prose_metrics.longest_prose_block(text)[1], 5)

    def test_code_tables_lists_and_quotes_are_not_prose(self):
        filler = " ".join(["word"] * 200)
        text = "\n\n".join(["```", filler, "```", "| %s |\n|---|" % filler, "- " + filler,
                             "> " + filler, "# " + filler, "<!-- %s -->" % filler,
                             "Ten words of running prose, and nothing else, here now."])
        self.assertEqual(prose_metrics.longest_prose_block(text)[1], 10)


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
                    (self.CATALOG, "108 templates", "105 templates"),
                    ("README.md", "all 108 blanks", "all 105 blanks"),
                    ("docs/ARCHITECTURE.md", "all 108 templates",
                     "all 105 templates")):
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
            self.rewrite(catalog, "## definition (13 templates)",
                         "## definition (14 templates)", 1)
            self.assertEqual(
                sorted([(self.CATALOG, "the discovery section says 15 "
                         "template(s) and the directory holds 16"),
                        (self.CATALOG, "the definition section says 14 "
                         "template(s) and the directory holds 13")]),
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
            self.rewrite(root / "README.md", "all 108 blanks", "the blanks")
            self.rewrite(root / "docs" / "ARCHITECTURE.md",
                         "all 108 templates", "the templates")
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
            self.rewrite(root / "README.md", "all 108 blanks", "all 98 blanks")
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


class ExamplesInventoryGateTests(unittest.TestCase):
    """The examples index, counted against examples/ rather than against itself.

    Three of its four journey figures were stale and summed to its stale total,
    and the gate never opened the file. Each seed below passed silently before
    this check existed.
    """

    INDEX = "examples/README.md"
    COUNT = "the artifact map for the 58 files below"

    def findings(self, root):
        return [(item.path, item.line, item.message)
                for item in check_examples_inventory(root)]

    def rewrite(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertEqual(1, text.count(old), old)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def line_of(self, root, needle):
        lines = (root / self.INDEX).read_text(encoding="utf-8").splitlines()
        return next(number for number, raw in enumerate(lines, 1)
                    if needle in raw)

    def test_the_tree_as_it_stands_states_its_own_inventory(self):
        self.assertEqual([], self.findings(REPO))
        self.assertEqual([], [item for item in check_docs(REPO)
                              if item.path == self.INDEX])

    def test_a_section_count_off_by_one_is_reported_at_its_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, self.COUNT,
                         "the artifact map for the 57 files below")
            line = self.line_of(root, "57 files below")
            self.assertIn((self.INDEX, line, "the ledgerline section says "
                           "'57 files' and examples/ holds 58 ledgerline "
                           "artifact(s)"), self.findings(root))
            self.assertIn("examples-inventory",
                          {item.code for item in check_docs(root)
                           if item.severity == "error"})

    def test_a_new_file_with_its_row_and_a_stale_digit_is_reported(self):
        """The discriminating seed. The file is in the tree and in the table,
        so the orphan check is satisfied and the row count agrees with the
        tree: only the stated figure is stale, and a count read back from the
        document's own rows would pass it forever."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "examples" / "ledgerline-brand-new-thing.md").write_text(
                "# Brand new thing\n", encoding="utf-8")
            row = ("| [ledgerline-retrospective.md](ledgerline-retrospective.md)"
                   " |")
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            start = text.index(row)
            end = text.index("\n", start)
            index.write_text(text[:end] + "\n| [ledgerline-brand-new-thing.md]"
                             "(ledgerline-brand-new-thing.md) | None | None |"
                             + text[end:], encoding="utf-8")
            messages = [message for _path, _line, message
                        in self.findings(root)]
            self.assertNotIn("examples/ledgerline-brand-new-thing.md is in the "
                             "tree and not in the index", messages)
            self.assertIn("the ledgerline section says '58 files' and "
                          "examples/ holds 59 ledgerline artifact(s)", messages)
            self.assertIn("the summary row for ledgerline says 58 and "
                          "examples/ holds 59", messages)
            self.assertIn("the index says 170 artifacts in all and examples/ "
                          "holds 171", messages)

    def test_dropping_the_count_sentence_is_not_a_way_to_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX,
                         " It fills no template itself: it is the data sheet "
                         "and the artifact map for the 58 files below, apart "
                         "from the last 7 rows.", "")
            messages = [message for _path, _line, message
                        in self.findings(root)]
            self.assertTrue(any(message.startswith(
                "no operator document states the examples inventory for "
                "ledgerline") for message in messages), messages)

    def test_a_row_pointing_at_no_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX,
                         "| [example-brd.md](example-brd.md) |",
                         "| [does-not-exist.md](does-not-exist.md) | None | "
                         "None |\n| [example-brd.md](example-brd.md) |")
            line = self.line_of(root, "does-not-exist.md")
            self.assertIn((self.INDEX, line, "the index links does-not-exist.md"
                           ", which does not resolve"), self.findings(root))

    def test_a_file_the_index_never_links_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "examples" / "unlisted.md").write_text(
                "# Unlisted\n", encoding="utf-8")
            self.assertIn((self.INDEX, 1, "examples/unlisted.md is in the tree "
                           "and not in the index"), self.findings(root))

    def test_a_tree_with_no_examples_makes_no_inventory_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            shutil.rmtree(root / "examples")
            self.assertEqual([], self.findings(root))

    def row_line(self, text, name):
        prefix = "| [%s](%s) |" % (name, name)
        found = [raw for raw in text.splitlines() if raw.startswith(prefix)]
        self.assertEqual(1, len(found), name)
        return found[0]

    def swap_rows(self, root, first, second):
        index = root / self.INDEX
        text = index.read_text(encoding="utf-8")
        one, two = self.row_line(text, first), self.row_line(text, second)
        text = text.replace(one, "\0").replace(two, one).replace("\0", two)
        index.write_text(text, encoding="utf-8")

    def messages(self, root):
        return [message for _path, _line, message in self.findings(root)]

    def test_a_standalone_count_off_by_one_is_reported(self):
        """A section that names no journey is held to its rows, and only by
        the rows comparison: nothing else reads "the 16 files below"."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "Each of the 16 files below",
                         "Each of the 17 files below")
            line = self.line_of(root, "Each of the 17 files below")
            self.assertIn((self.INDEX, line, "the 'Standalone examples' "
                           "section says 17 file(s) and its table has 16 "
                           "row(s)"), self.findings(root))

    def test_dropping_the_total_is_not_a_way_to_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "the four hold 170 artifacts in "
                         "all, counted", "the four are counted")
            self.assertIn((self.INDEX, 1, "no operator document states the "
                           "examples inventory for the journeys' total. Its "
                           "section has to say \"the N files below\" and the "
                           "index \"N artifacts in all\", or the figure is "
                           "measured by nobody"), self.findings(root))

    def test_a_family_row_moved_into_another_section_is_reported(self):
        """The original stray-row defect with every count kept equal: a
        Ledgerline row in the standalone table and a standalone row in the
        Ledgerline table leave every row count and tree count unchanged."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.swap_rows(root, "ledgerline-business-case.md",
                           "example-brd.md")
            messages = self.messages(root)
            self.assertIn("the ledgerline section lists example-brd.md, which "
                          "is not a ledgerline artifact", messages)
            self.assertIn("the ledgerline section does not list "
                          "ledgerline-business-case.md", messages)

    def test_rows_swapped_between_two_families_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.swap_rows(root, "sahulat-decision-log.md",
                           "harbourgate-adr.md")
            messages = self.messages(root)
            self.assertIn("the sahulat section lists harbourgate-adr.md, "
                          "which is not a sahulat artifact", messages)
            self.assertIn("the harbourgate section does not list "
                          "harbourgate-adr.md", messages)

    def test_a_row_listed_twice_in_its_family_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            text = text.replace(self.row_line(text, "ledgerline-okrs.md"),
                                self.row_line(text,
                                              "ledgerline-positioning.md"))
            index.write_text(text, encoding="utf-8")
            messages = self.messages(root)
            self.assertIn("the ledgerline section lists "
                          "ledgerline-positioning.md more than once", messages)
            self.assertIn("the ledgerline section does not list "
                          "ledgerline-okrs.md", messages)

    def test_a_deleted_summary_row_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            row = self.row_line(text, "sahulat-journey.md")
            index.write_text(text.replace(row + "\n", ""), encoding="utf-8")
            self.assertIn("the summary table has 0 row(s) for sahulat and "
                          "needs one", self.messages(root))

    def test_the_lead_counts_are_held_to_their_sections(self):
        seeds = (
            ("16 standalone examples", "17 standalone examples",
             "the index says '17 standalone examples' and the 'Standalone "
             "examples' table has 16 row(s)"),
            ("41 single-file industry examples",
             "40 single-file industry examples",
             "the index says '40 single-file industry examples' and the "
             "'Industry examples' table has 41 row(s)"),
            ("and 4 journeys", "and 5 journeys",
             "the index says '5 journeys' and examples/ holds 4 journey(s)"),
        )
        for old, new, message in seeds:
            with self.subTest(new=new), tempfile.TemporaryDirectory() as tmp:
                root = copy_tree(tmp)
                self.rewrite(root / self.INDEX, old, new)
                self.assertIn((self.INDEX, 3, message), self.findings(root))

    def test_a_lead_count_whose_section_is_gone_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "## Industry examples\n",
                         "## Examples by industry\n")
            self.assertIn((self.INDEX, 3, "the index says '41 single-file "
                           "industry examples' and has no 'Industry examples' "
                           "section to count"), self.findings(root))

    def test_the_added_and_original_figures_are_held_to_the_tree(self):
        """The 38 / 30 / 38 figures were stale beside the family counts and
        nothing read them."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "the 38 artifacts added below the "
                         "original 13", "the 39 artifacts added below the "
                         "original 13")
            self.assertIn("the ledgerline section's 39 added, 13 original and "
                          "7 last rows make 59, and examples/ holds 58",
                          self.messages(root))
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "the 30 artifacts added below the "
                         "original 14", "the 31 artifacts added below the "
                         "original 13")
            messages = self.messages(root)
            # 31 + 13 still makes 44, so only the artifact map catches it.
            self.assertEqual(["the sahulat section says 'the original 13' and "
                              "its journey's artifact map lists 14"],
                             [m for m in messages if "sahulat" in m])

    def test_the_last_rows_figure_is_held_to_the_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "The last 7 Ledgerline rows",
                         "The last 8 Ledgerline rows")
            self.assertIn("the index gives [7, 8] figures for the last "
                          "ledgerline rows", self.messages(root))
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            self.assertEqual(3, text.count("last 7 "))
            index.write_text(text.replace("last 7 ", "last 8 "),
                             encoding="utf-8")
            messages = self.messages(root)
            self.assertIn("the index says the last 8 ledgerline rows are "
                          "outside the artifact map and cite neither the "
                          "journey nor its sheets, and 7 of them are",
                          messages)
            self.assertIn("the ledgerline section's 38 added, 13 original and "
                          "8 last rows make 59, and examples/ holds 58",
                          messages)

    JOURNEY = "examples/ledgerline-journey.md"
    TAIL_ROW = ("- [JTBD job map](ledgerline-jtbd-job-map.md) fills the job "
                "map worksheet.\n\n")

    def tail_messages(self, root, outside):
        return [message for message in self.messages(root)
                if message == "the index says the last 7 ledgerline rows are "
                "outside the artifact map and cite neither the journey nor "
                "its sheets, and %d of them are" % outside]

    def test_a_last_row_moved_into_the_artifact_map_is_reported(self):
        """The 'outside its artifact map' half of the last-rows clause. The
        moved row cites no journey, so only the map lookup can catch it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.JOURNEY, "## What this journey teaches",
                         self.TAIL_ROW + "## What this journey teaches")
            # One finding for each place the index states the figure.
            self.assertEqual(3, len(self.tail_messages(root, 6)))

    def test_the_artifact_map_runs_to_the_next_h2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            # A subheading inside the map keeps the map's links.
            self.rewrite(root / self.JOURNEY, "## What this journey teaches",
                         "### A later addition\n\n" + self.TAIL_ROW
                         + "## What this journey teaches")
            # One finding for each place the index states the figure.
            self.assertEqual(3, len(self.tail_messages(root, 6)))
        # A heading of the same name at another level is not the map.
        for heading in ("### Artifact map", "# Artifact map"):
            with self.subTest(heading=heading), \
                    tempfile.TemporaryDirectory() as tmp:
                root = copy_tree(tmp)
                self.rewrite(root / self.JOURNEY, "### Timeline",
                             heading + "\n\n" + self.TAIL_ROW
                             + "### Timeline")
                self.assertEqual([], [message
                                      for message in self.messages(root)
                                      if "ledgerline" in message])

    def test_the_last_rows_are_the_rows_at_the_foot_of_the_table(self):
        """The positional half of the last-rows clause: the K rows it names are
        the K rows at the foot of the family's table, not any K rows in it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            moved = self.row_line(text, "ledgerline-jtbd-job-map.md")
            first = self.row_line(text, "ledgerline-positioning.md")
            text = text.replace(moved + "\n", "")
            text = text.replace(first, moved + "\n" + first)
            index.write_text(text, encoding="utf-8")
            # A mapped row now sits in the last 7, so only 6 of them are
            # outside; one finding for each place the index states the figure.
            self.assertEqual(3, len(self.tail_messages(root, 6)))

    def test_a_tail_row_naming_no_file_is_reported_not_raised(self):
        """A row at the foot of the table that links no file is a finding. The
        tail filter reads only the family's own files, so the gate never opens
        a file the tree does not hold."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            last = self.row_line(text, "ledgerline-harness-routing-run.md")
            index.write_text(text.replace(
                last, last + "\n| [ledgerline-ghost.md](ledgerline-ghost.md) "
                "| x | y |"), encoding="utf-8")
            messages = self.messages(root)
            self.assertIn("the index links ledgerline-ghost.md, which does "
                          "not resolve", messages)
            self.assertEqual(3, len(self.tail_messages(root, 6)))

    def test_a_section_linking_two_journeys_indexes_neither(self):
        """A section says which family it indexes by linking exactly one
        journey. Linking two makes it no family's section, rather than the
        section of whichever journey a set happens to yield first."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "The last 7 rows sit outside",
                         "[sahulat-journey.md](sahulat-journey.md) is another "
                         "family. The last 7 rows sit outside")
            messages = self.messages(root)
            self.assertIn("no operator document states the examples "
                          "inventory for ledgerline. Its section has to say "
                          "\"the N files below\" and the index \"N artifacts "
                          "in all\", or the figure is measured by nobody",
                          messages)
            self.assertEqual([], [message for message in messages
                                  if "not a sahulat artifact" in message])
            # The unnamed 'last 7 rows' in that section names no family either.
            self.assertIn("'last 7 rows' names no journey family", messages)
            self.assertEqual([], [message for message in messages
                                  if "last 7 sahulat rows" in message])

    def test_a_last_rows_figure_on_no_family_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            self.rewrite(root / self.INDEX, "Read the examples before filling "
                         "the templates.", "Read the examples before filling "
                         "the templates, the last 2 widget rows first.")
            self.assertIn("'last 2 widget rows' names no journey family",
                          self.messages(root))

    def test_one_stale_figure_stated_twice_on_a_line_is_one_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            index = root / self.INDEX
            text = index.read_text(encoding="utf-8")
            line = next(raw for raw in text.splitlines()
                        if self.COUNT in raw)
            self.assertEqual(2, line.count("58 files"))
            index.write_text(text.replace(line, line.replace("58 files",
                                                             "57 files")),
                             encoding="utf-8")
            self.assertEqual(1, self.messages(root).count(
                "the ledgerline section says '57 files' and examples/ holds "
                "58 ledgerline artifact(s)"))

    def test_a_family_named_inside_another_is_counted_once(self):
        members = _example_families({
            "a-journey.md", "a-b-journey.md", "a-b-coverage-sheet.md",
            "a-b-thing.md", "a-other.md", "a-design-sheet.md"})
        self.assertEqual({"a": {"a-other.md"}, "a-b": {"a-b-thing.md"}},
                         members)

    def test_an_apple_double_file_is_not_an_example(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / "examples" / "._ledgerline-positioning.md").write_bytes(
                b"\x00\x05\x16\x07")
            self.assertEqual([], self.findings(root))

    def test_a_missing_index_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            (root / self.INDEX).unlink()
            self.assertEqual([(self.INDEX, 1, "the examples index is missing, "
                               "so nothing states the inventory it is the "
                               "front door for")], self.findings(root))


# Three filled evidence notes, one per kind, written as fixtures rather than
# shipped as examples: they exist to prove that an interview, a query result
# and a watched session can each pass the note contract on their own evidence.
# Everything in them is invented. Fennix Logistics is not a company.
INTERVIEW_NOTE = """# Evidence Note: P-1147 (ILLUSTRATIVE)

## Source

- **Name:** Payroll interview with Clara Morwen, payroll administrator, Fennix Logistics
- **Locator:** Interview P-1147, transcript section 3
- **Source date:** 2026-03-12
- **Type:** interview

## Claim

Payroll administrators retype an approved timesheet line when the legacy import writes an impossible start date.

**Evidence kind:** text quotation

**A. Text quotation** (interview, ticket, document, public page)

> "The system flags the row as approved even when the start date reads 02/30, so I have to retype the whole line."

- **Where in the source:** transcript section 3, 00:14:22 to 00:14:35

**Evidence class:** interview claim

## Weight

- **Confidence:** single-source
- **Agrees with:** E2, on the pattern rather than on this wording
- **Disagrees with:** none found
- **What this note cannot support:** how often this happens, or that the import is the only cause

## Ledger row

| E# | Claim | Evidence (quote, measure or observation) | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E1 | Administrators retype an approved line when the import writes an impossible start date | "The system flags the row as approved even when the start date reads 02/30, so I have to retype the whole line." | Interview P-1147, section 3 | 2026-03-12 | 2026-03-13 | single-source |
"""

METRIC_NOTE = """# Evidence Note: timesheet_edit_within_24h (ILLUSTRATIVE)

## Source

- **Name:** Warehouse query run by data operations, Fennix Logistics
- **Locator:** `timesheet_edit_within_24h.sql`, warehouse dataset march_2026
- **Source date:** 2026-03-31
- **Type:** metric export

## Claim

A small recurring share of approved timesheets is edited again within a day of approval.

**Evidence kind:** quantitative

**B. Quantitative** (metric export, dataset, query result)

- **Snapshot or query:** `timesheet_edit_within_24h.sql`, run 2026-04-01 against dataset march_2026
- **Filters:** approval status approved, edit timestamp within 24 hours of the approval timestamp, tenants flagged as test excluded
- **Denominator:** every timesheet approved in the period, 1,204 rows, counted the same way as the numerator
- **Period and timezone:** 2026-03-01 to 2026-03-31 inclusive, boundaries cut in UTC
- **Calculation:** 58 of 1,204 approved timesheets, deduplicated by timesheet ID so a row edited twice counts once

**Evidence class:** artifact

## Weight

- **Confidence:** single-source
- **Agrees with:** E1, on the pattern
- **Disagrees with:** none found
- **What this note cannot support:** whether the edits are corrections or mistakes

## Ledger row

| E# | Claim | Evidence (quote, measure or observation) | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E2 | A small recurring share of approved timesheets is edited again within a day | 58 of 1,204 approved timesheets edited within 24 hours, deduplicated by timesheet ID, March 2026 UTC | `timesheet_edit_within_24h.sql` | 2026-03-31 | 2026-04-01 | single-source |
"""

OBSERVATION_NOTE = """# Evidence Note: S-0922 (ILLUSTRATIVE)

## Source

- **Name:** Usability session with an approver, Fennix Logistics
- **Locator:** Session S-0922, recording `usab_0922.mp4`
- **Source date:** 2026-03-10
- **Type:** observation

## Claim

An approver clears a batch without opening any line detail.

**Evidence kind:** observation

**C. Observation** (watched behaviour, session recording, usability run)

- **Session or timecode:** S-0922, 00:04:10 to 00:07:45
- **What was observed:** the approver approved the batch from the summary screen and expanded no individual timesheet row
- **Context:** a batch view holding 14 pending items, reached from the daily approvals task

**Evidence class:** observed behavior

## Weight

- **Confidence:** single-source
- **Agrees with:** none found
- **Disagrees with:** none found
- **What this note cannot support:** that skipping line detail produces errors

## Ledger row

| E# | Claim | Evidence (quote, measure or observation) | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E3 | An approver clears a batch without opening any line detail | approved the batch from the summary screen and expanded no timesheet row, S-0922 at 00:04:10 to 00:07:45 | Session S-0922 | 2026-03-10 | 2026-03-11 | single-source |
"""


class EvidenceNoteContractTests(unittest.TestCase):
    """F12: an evidence note that is a count does not have to invent prose.

    The note's source types have always included metric exports, datasets and
    observations, while the claim block, the ledger row and the exit gate each
    demanded a verbatim quote. The three fixtures below are the closure proof:
    one interview, one query result and one watched session, each passing on
    the evidence it actually has. The mutations underneath are the old form,
    put back one piece at a time.
    """

    NOTES = {"text quotation": INTERVIEW_NOTE, "quantitative": METRIC_NOTE,
             "observation": OBSERVATION_NOTE}

    def issues(self, text, name="fixture.md"):
        return [(item.code, item.message)
                for item in evidence_note_issues(text, name, filled=True)]

    def docs_codes(self, root):
        return {item.code for item in check_docs(root) if item.severity == "error"}

    def test_the_tree_as_it_stands_meets_the_evidence_contract(self):
        self.assertEqual([], check_evidence_contract(REPO))

    def test_each_kind_passes_on_the_evidence_it_actually_has(self):
        for kind, note in self.NOTES.items():
            with self.subTest(kind=kind):
                self.assertEqual([], self.issues(note))

    def test_neither_the_measure_nor_the_observation_invents_a_quote(self):
        """The defect this finding names: prose written because a field asked
        for it. Neither fixture contains a quotation, and adding one is
        reported rather than accepted as evidence."""
        for kind in ("quantitative", "observation"):
            with self.subTest(kind=kind):
                note = self.NOTES[kind]
                self.assertNotIn('> "', note)
                forged = note.replace(
                    "**Evidence class:**",
                    '> "We edit those all the time."\n\n**Evidence class:**', 1)
                self.assertIn(("evidence-quote",
                               "a %s note quotes a sentence nobody said" % kind),
                              self.issues(forged))

    def test_an_interview_note_with_no_quote_is_still_reported(self):
        stripped = "\n".join(line for line in INTERVIEW_NOTE.splitlines()
                              if not line.startswith('> "'))
        self.assertIn(("evidence-quote",
                       "a text quotation note needs the sentence verbatim"),
                      self.issues(stripped))

    def test_a_missing_or_unanswered_field_is_reported_per_kind(self):
        cases = {
            "quantitative": ("- **Denominator:**", "Denominator"),
            "observation": ("- **Session or timecode:**", "Session or timecode"),
            "text quotation": ("- **Where in the source:**", "Where in the source"),
        }
        for kind, (line_start, label) in cases.items():
            note = self.NOTES[kind]
            dropped = "\n".join(line for line in note.splitlines()
                                 if not line.startswith(line_start))
            with self.subTest(kind=kind, mutation="dropped"):
                self.assertIn(("evidence-field",
                               "a %s note needs its '%s' field" % (kind, label)),
                              self.issues(dropped))
            blanked = "\n".join(
                (line_start + " [not yet answered]") if line.startswith(line_start)
                else line for line in note.splitlines())
            with self.subTest(kind=kind, mutation="left blank"):
                self.assertIn(("evidence-field",
                               "'%s' is still the blank instruction" % label),
                              self.issues(blanked))

    def test_an_undeclared_or_invented_kind_is_reported(self):
        self.assertIn(("evidence-kind",
                       "the claim block declares no '**Evidence kind:**'"),
                      self.issues(INTERVIEW_NOTE.replace(
                          "**Evidence kind:** text quotation", "")))
        self.assertTrue(any(code == "evidence-kind" and message.startswith("'vibes'")
                            for code, message in self.issues(
                                INTERVIEW_NOTE.replace("text quotation", "vibes", 1))))

    def test_a_template_that_demands_a_quote_of_every_note_is_reported(self):
        """The form as it stood at the audit: one quote block, no kinds."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / "templates" / "discovery" / "evidence-note.md"
            text = path.read_text(encoding="utf-8")
            start = text.index("**Evidence kind:**")
            end = text.index("**Evidence class:**")
            path.write_text(text[:start] + "**Verbatim quote:**\n\n"
                            + '> "[the load-bearing sentence]"\n\n'
                            + text[end:], encoding="utf-8")
            self.assertIn("evidence-kind", self.docs_codes(root))

    def test_a_ledger_column_that_only_takes_a_quote_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for name in ("templates/discovery/evidence-note.md",
                         "templates/execution/state.md",
                         "examples/sahulat-evidence-note.md"):
                path = root / name
                path.write_text(path.read_text(encoding="utf-8").replace(
                    "| E# | Claim | Evidence (quote, measure or observation) |",
                    "| E# | Claim | Verbatim quote |"), encoding="utf-8")
            codes = self.docs_codes(root)
            self.assertIn("evidence-ledger", codes)

    def test_a_state_ledger_that_drifts_from_the_note_row_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / "templates" / "execution" / "state.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "| E# | Claim | Evidence (quote, measure or observation) |",
                "| E# | Claim | Verbatim quote only |"), encoding="utf-8")
            self.assertIn(("templates/execution/state.md",
                           "the evidence ledger does not carry the note's row, "
                           "which is copied unchanged"),
                          [(item.path, item.message)
                           for item in check_evidence_contract(root)])

    def test_a_theme_that_must_carry_a_quote_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / "templates" / "discovery" / "discovery-synthesis.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "- **Load-bearing evidence:**", "- **Load-bearing quote:**"),
                encoding="utf-8")
            self.assertIn("evidence-kind", self.docs_codes(root))


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

    def test_a_spawned_gate_uses_sys_executable_not_literal_python3(self):
        captured = {}

        def fake_run(argv, **kwargs):
            captured["argv0"] = argv[0]
            return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

        with unittest.mock.patch.object(ci_gate.subprocess, "run", fake_run):
            ci_gate.run_gate(self.gate("pass"))
        self.assertEqual(sys.executable, captured["argv0"])
        self.assertNotEqual("python3", captured["argv0"])

    def test_main_refuses_to_run_under_python_older_than_3_11(self):
        with unittest.mock.patch.object(ci_gate.sys, "version_info",
                                        (3, 9, 6, "final", 0)):
            code, output = quietly(ci_gate.main, ["--manifest"])
        self.assertEqual(2, code)
        self.assertIn("Python 3.11+", output)
        self.assertIn("3.9", output)

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

    # F17: hidden_guidance_share, the informational metric added alongside
    # the seven scored dimensions above. These pin that it measures the
    # right thing, that it never moves "score", and that a section explains
    # itself the same way whether its guidance sits in a comment or in the
    # visible <details> convention docs/RENDERING.md documents.

    def test_hidden_guidance_counts_words_inside_html_comments_only(self):
        hidden, total, share = template_rubric.hidden_guidance(
            "a b c d <!-- e f g h --> i j")
        self.assertEqual(6, hidden)
        self.assertEqual(12, total)
        self.assertEqual(0.5, share)

    def test_hidden_guidance_share_is_zero_with_no_comments(self):
        hidden, total, share = template_rubric.hidden_guidance("a b c d")
        self.assertEqual((0, 4, 0.0), (hidden, total, share))

    def test_score_template_reports_hidden_guidance_alongside_the_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, STRONG_TEMPLATE)
        self.assertIn("hidden_guidance_share", report)
        self.assertIn("hidden_guidance_words", report)
        self.assertIn("total_words", report)
        self.assertGreater(report["hidden_guidance_words"], 0,
                            "STRONG_TEMPLATE's guidance still lives in "
                            "<!-- --> comments, so this must be nonzero")

    def test_a_visible_details_block_explains_a_section_like_a_comment_does(self):
        text = ("# X\n\nStage: DEFINE, feeds Gate 2\n\n## One\n"
                "<details open>\n<summary>Guidance</summary>\n\n"
                "What goes here, and what a bad answer looks like.\n\n"
                "</details>\n")
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, text)
        self.assertEqual(1, report["sections_explained"])
        self.assertEqual(1.0, report["marks"]["self_explaining"])

    def test_a_visible_details_block_is_not_counted_as_hidden(self):
        text = ("# X\n\n## One\n<details open>\n<summary>Guidance</summary>\n\n"
                "What goes here.\n\n</details>\n")
        with tempfile.TemporaryDirectory() as tmp:
            report = self.score(tmp, text)
        self.assertEqual(0, report["hidden_guidance_words"])
        self.assertEqual(0.0, report["hidden_guidance_share"])

    def test_migrating_a_section_from_comment_to_details_does_not_move_the_score(self):
        guidance = "What goes here, and a bad answer: a blank owner."
        skeleton = ("# X\n\nStage: DEFINE, feeds Gate 2\n\n## One\n%s\n"
                    "| a | b |\n|---|---|\n| [name] | [date] |\n\n"
                    "Read [the PRD](prd.md).\n\n## Exit gate\n- [ ] Done.\n")
        hidden_text = skeleton % ("<!-- %s -->" % guidance)
        visible_text = skeleton % (
            "<details open>\n<summary>Guidance</summary>\n\n%s\n\n</details>"
            % guidance)
        with tempfile.TemporaryDirectory() as tmp:
            before = self.score(tmp, hidden_text)
        with tempfile.TemporaryDirectory() as tmp:
            after = self.score(tmp, visible_text)
        self.assertEqual(before["score"], after["score"])
        self.assertEqual(before["marks"], after["marks"])
        self.assertGreater(before["hidden_guidance_share"], 0.0)
        self.assertEqual(0.0, after["hidden_guidance_share"])

    def test_highest_hidden_guidance_share_is_reported_and_ranked(self):
        # Almost entirely comment, so its hidden share is far above the
        # STRONG_TEMPLATE reference's, and both templates also appear in the
        # separate "weakest" (by score) table earlier in the same output, so
        # the ranking check below reads only the hidden-guidance section,
        # never the first occurrence of either path anywhere in the output.
        heavy_comment = " ".join(["word"] * 40)
        with tempfile.TemporaryDirectory() as tmp:
            root = self.tree(
                tmp, prd=STRONG_TEMPLATE,
                hider="# Hider\n\n## One\n<!-- %s -->\n" % heavy_comment)
            code, output = self.run_gate(root, "--hidden-top", "5")
        self.assertEqual(0, code, output)
        marker = "highest hidden-guidance share"
        self.assertIn(marker, output)
        section = output[output.index(marker):]
        hider_line = next(line for line in section.splitlines()
                          if "templates/definition/hider.md" in line)
        prd_line = next(line for line in section.splitlines()
                        if line.strip().startswith("templates/definition/prd.md"))
        self.assertLess(section.index(hider_line), section.index(prd_line),
                        "in the hidden-guidance ranking, the template hiding "
                        "a larger share of its words must rank above one "
                        "hiding a smaller share:\n%s" % section)

    # F21: worked_example must also credit a real completed example living
    # under examples/, not only the inline ILLUSTRATIVE_RE form, because 39
    # templates in the tree carry the first kind and none of the second and
    # were scoring as if they had no worked example at all.

    def _template_and_examples(self, tmp):
        root = Path(tmp)
        template = root / "templates" / "definition" / "subject.md"
        template.parent.mkdir(parents=True, exist_ok=True)
        examples = root / "examples"
        examples.mkdir(parents=True, exist_ok=True)
        return root, template, examples

    def test_a_linked_real_example_earns_worked_example_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, template, examples = self._template_and_examples(tmp)
            template.write_text(
                "# Subject\n\n"
                "Filled example: [worked](../../examples/worked.md)\n\n"
                "## One\n<!-- guidance -->\n", encoding="utf-8")
            (examples / "worked.md").write_text(
                "# Subject worked\n\n"
                "Fills [templates/definition/subject.md]"
                "(../templates/definition/subject.md). Everything here is "
                "invented.\n", encoding="utf-8")
            with unittest.mock.patch.object(template_rubric, "REPO", root):
                report = template_rubric.score_template(template)
        self.assertEqual(1.0, report["marks"]["worked_example"])

    def test_a_link_to_an_example_for_a_different_template_earns_no_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, template, examples = self._template_and_examples(tmp)
            template.write_text(
                "# Subject\n\n"
                "Filled example: [worked](../../examples/worked.md)\n\n"
                "## One\n<!-- guidance -->\n", encoding="utf-8")
            (examples / "worked.md").write_text(
                "# Other worked\n\n"
                "Fills [templates/definition/other.md]"
                "(../templates/definition/other.md). Everything here is "
                "invented.\n", encoding="utf-8")
            with unittest.mock.patch.object(template_rubric, "REPO", root):
                report = template_rubric.score_template(template)
        self.assertEqual(0.0, report["marks"]["worked_example"])

    def test_a_link_to_a_missing_example_earns_no_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, template, _examples = self._template_and_examples(tmp)
            template.write_text(
                "# Subject\n\n"
                "Filled example: [worked](../../examples/missing.md)\n\n"
                "## One\n<!-- guidance -->\n", encoding="utf-8")
            with unittest.mock.patch.object(template_rubric, "REPO", root):
                report = template_rubric.score_template(template)
        self.assertEqual(0.0, report["marks"]["worked_example"])


class TemplateBackpointerGateTests(unittest.TestCase):
    """tools/template_rubric.py --backpointers: the templates with no verified
    filled-example link are exactly the committed exception list.

    Four seeds, one for each weaker check this gate replaces. A floor on the
    count passes a new template with no pointer, because the count it floors
    does not move. A grep for "Filled example:" passes a line that links
    nothing. A check that the link resolves passes a link to a real example of
    another template. And with no gate at all, deleting a pointer fails
    nothing.
    """

    EXCUSED = "templates/definition/assumptions-register.md"

    def copy(self, tmp):
        """templates/ and examples/, which is all this gate reads."""
        root = Path(tmp).resolve() / "repo"
        for name in ("templates", "examples"):
            shutil.copytree(REPO / name, root / name,
                            ignore=shutil.ignore_patterns("._*"))
        return root

    def gate(self, root, exceptions=None):
        with contextlib.ExitStack() as stack:
            stack.enter_context(unittest.mock.patch.object(
                template_rubric, "REPO", root))
            stack.enter_context(unittest.mock.patch.object(
                template_rubric, "TEMPLATES", root / "templates"))
            if exceptions is not None:
                stack.enter_context(unittest.mock.patch.object(
                    template_rubric, "BACKPOINTER_EXCEPTIONS", exceptions))
            return quietly(template_rubric.main, ["--backpointers"])

    @staticmethod
    def block(output, heading):
        """The lines under the paragraph that opens with `heading`, up to the
        next blank line."""
        return output.split("\n" + heading, 1)[1].split("\n\n", 1)[0] \
            .splitlines()[1:]

    def unpointed(self, output):
        """Each template the gate lists as having no verified back-pointer,
        with what it says of it."""
        found = {}
        for line in self.block(output, "without a verified back-pointer."):
            if line.startswith("  templates/"):
                path, state = line[2:].split("  ", 1)
                found[path] = state
        return found

    def unexcused(self, *paths):
        """The listing expected when `paths` join the excused template."""
        expected = {self.EXCUSED: "on the exception list"}
        expected.update((path, "NOT ON THE EXCEPTION LIST") for path in paths)
        return expected

    @staticmethod
    def pointed(output):
        line = next(line for line in output.splitlines()
                    if "with a verified back-pointer    :" in line)
        return int(line.rsplit(":", 1)[1])

    def drop_pointers(self, template, replacement=()):
        lines = template.read_text(encoding="utf-8").split("\n")
        pointers = [number for number, line in enumerate(lines)
                    if line.startswith("Filled example:")]
        self.assertTrue(pointers, template.name)
        lines[pointers[0]:pointers[-1] + 1] = list(replacement)
        template.write_text("\n".join(lines), encoding="utf-8")

    def test_the_tree_as_it_stands_is_exactly_the_exception_list(self):
        code, output = quietly(template_rubric.main, ["--backpointers"])
        self.assertEqual(0, code, output)
        self.assertEqual(self.unexcused(), self.unpointed(output))

    def test_a_new_template_with_no_pointer_fails_naming_it(self):
        """The seed a floor cannot catch: the number of templates with a
        pointer is the same before and after, so a floor at today's figure
        passes the tree this gate fails."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            _code, before = self.gate(root)
            (root / "templates" / "definition" / "brand-new.md").write_text(
                "# Brand New\n\n## One\n", encoding="utf-8")
            code, after = self.gate(root)
        self.assertEqual(1, code, after)
        self.assertEqual(self.unexcused("templates/definition/brand-new.md"),
                         self.unpointed(after))
        self.assertEqual(self.pointed(before), self.pointed(after))

    def test_a_bare_filled_example_line_earns_nothing(self):
        """The seed a grep cannot catch: the words are on the page and no
        link is, so `grep -rL "Filled example:"` would not list the file."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            vision = root / "templates" / "planning" / "vision.md"
            self.drop_pointers(vision, ["Filled example: none yet"])
            self.assertIn("\nFilled example: none yet\n",
                          vision.read_text(encoding="utf-8"))
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertEqual(self.unexcused("templates/planning/vision.md"),
                         self.unpointed(output))

    def test_a_link_to_an_example_that_does_not_name_it_back_fails(self):
        """The seed worked_example_link() was written for: the link resolves
        to a real file under examples/, which fills a different template and
        so never names this one back."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            other = root / "examples" / "ledgerline-red-team-review.md"
            opening = "\n".join(other.read_text(encoding="utf-8")
                                .splitlines()[:5])
            self.assertNotIn("templates/ai/guardrails.md", opening)
            guardrails = root / "templates" / "ai" / "guardrails.md"
            text = guardrails.read_text(encoding="utf-8")
            old = "(../../examples/ledgerline-guardrails.md)"
            self.assertIn(old, text)
            guardrails.write_text(text.replace(
                old, "(../../examples/ledgerline-red-team-review.md)"),
                encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertEqual(self.unexcused("templates/ai/guardrails.md"),
                         self.unpointed(output))

    def test_deleting_one_of_the_added_pointers_fails_naming_its_template(self):
        """templates/execution/state.md: the phase index skips it as a journal
        rather than an artifact, so a pointer list built from the phase index
        would not have given it one."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.drop_pointers(root / "templates" / "execution" / "state.md")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertEqual(self.unexcused("templates/execution/state.md"),
                         self.unpointed(output))

    def test_an_entry_for_a_template_that_has_a_pointer_fails(self):
        exceptions = dict(template_rubric.BACKPOINTER_EXCEPTIONS)
        exceptions["templates/planning/vision.md"] = "It has none."
        code, output = self.gate(REPO, exceptions)
        self.assertEqual(1, code, output)
        self.assertIn("  templates/planning/vision.md has a verified "
                      "back-pointer to examples/", output)

    def test_an_entry_for_a_file_that_is_not_a_template_fails(self):
        exceptions = dict(template_rubric.BACKPOINTER_EXCEPTIONS)
        exceptions["templates/definition/no-such-template.md"] = "Nothing does."
        code, output = self.gate(REPO, exceptions)
        self.assertEqual(1, code, output)
        self.assertIn("  templates/definition/no-such-template.md is not a "
                      "template in this tree", output)

    def test_an_entry_fails_once_an_example_names_its_template_back(self):
        """The one reason an entry can give is that no example names its
        template back in its first five lines, and that stops being true the
        day one does, whether or not the template links it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            (root / "examples" / "assumptions-register-filled.md").write_text(
                "# Assumptions Register: Filled\n\nFills [%s](../%s). "
                "Invented.\n" % (self.EXCUSED, self.EXCUSED), encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("  %s is named back by "
                      "examples/assumptions-register-filled.md, so it has a "
                      "filled example to link" % self.EXCUSED, output)

    def test_every_entry_needs_a_one_line_reason(self):
        for reason in ("", "   ", "One line.\nAnd a second."):
            with self.subTest(reason=reason):
                code, output = self.gate(REPO, {self.EXCUSED: reason})
                self.assertEqual(1, code, output)
                self.assertIn("  %s has no one-line reason" % self.EXCUSED,
                              output)

    def test_every_template_several_examples_name_back_is_listed_with_all(self):
        """Which of several examples a template links is a reviewer's call the
        gate cannot make, so it lists each such template with every candidate
        and marks the linked ones, on a passing run too. The expectation is
        read from examples/ here, through the five opening lines every example
        declares its template in, so a listing that dropped a candidate or
        read another window disagrees with it."""
        code, output = quietly(template_rubric.main, ["--backpointers"])
        self.assertEqual(0, code, output)
        listed, current = {}, None
        for line in self.block(output, "named back by more than one file"):
            if line.startswith("  templates/"):
                current = listed.setdefault(line.strip(), {})
            else:
                current[line[6:]] = line[4] == "*"
        openings = {
            "examples/" + path.relative_to(REPO / "examples").as_posix():
                "\n".join(path.read_text(encoding="utf-8").splitlines()[:5])
            for path in sorted((REPO / "examples").rglob("*.md"))}
        expected = {}
        for template in sorted((REPO / "templates").rglob("*.md")):
            rel = template.relative_to(REPO).as_posix()
            named = [name for name, opening in openings.items()
                     if rel in opening]
            if template.name == "README.md" or len(named) < 2:
                continue
            linked = {line.split("(../../", 1)[1].split(")", 1)[0]
                      for line in template.read_text(encoding="utf-8").splitlines()
                      if line.startswith("Filled example: [")}
            expected[rel] = {name: name in linked for name in named}
        self.assertTrue(expected)
        self.assertEqual(expected, listed)

    def test_a_name_back_counts_on_the_fifth_line_and_not_the_sixth(self):
        """The window is what "names it back" means, pinned from both sides
        here, because every example in the tree names its template on its
        third line and so cannot tell a three-line window from an eight-line
        one."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            for line in (5, 6):
                rel = "templates/definition/boundary-%d.md" % line
                (root / rel).write_text(
                    "# Boundary\n\nFilled example: [boundary]"
                    "(../../examples/boundary-%d.md)\n" % line, encoding="utf-8")
                opening = (["# Boundary %d" % line] + ["filler"] * (line - 2)
                           + ["Fills %s." % rel])
                (root / "examples" / ("boundary-%d.md" % line)).write_text(
                    "\n".join(opening) + "\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertEqual(self.unexcused("templates/definition/boundary-6.md"),
                         self.unpointed(output))

    def test_every_candidate_listed_is_one_a_link_would_verify(self):
        """The listing and the link check read the same opening lines. If they
        differed, a file offered as a candidate could be refused as a link."""
        offered = 0
        for row in template_rubric.backpointer_rows():
            template = REPO / row["path"]
            up = "../" * (len(Path(row["path"]).parts) - 1)
            for candidate in row["candidates"]:
                offered += 1
                self.assertEqual(
                    [(REPO / candidate).resolve()],
                    template_rubric.linked_examples(
                        template, "[filled](%s%s)" % (up, candidate)),
                    "%s offers %s" % (row["path"], candidate))
        self.assertGreater(offered, 0)

    def test_a_file_under_examples_that_is_not_text_is_skipped(self):
        """Every file under examples/ is read for candidates, not only the
        ones a template links, so an image or a folder there must not stop
        the gate reading the rest."""
        for kind in ("an image", "a folder"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = self.copy(tmp)
                if kind == "an image":
                    (root / "examples" / "diagram.png").write_bytes(
                        b"\x89PNG\r\n\x1a\n\xff\xfe")
                else:
                    (root / "examples" / "images").mkdir()
                code, output = self.gate(root)
                self.assertEqual(0, code, output)


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


class ExampleAvailabilityGateTests(unittest.TestCase):
    """tools/example_availability.py --check: a domain card's statement about
    which of its templates have filled examples is generated from the declared
    relations, so it cannot survive them changing.

    F07 of the audit of 2026-09-23: seven cards denied examples the tree already
    carried (capital-markets said no filled failure-scenarios example existed
    anywhere while examples/harbourgate-failure-scenarios.md sat in the tree),
    and every gate passed, because nothing reads prose. Three seeds here, one
    per way the sentence went wrong: an example is added, an example is removed,
    and a card writes the claim by hand again.

    Four more hold shut the ways a card could leave the gate rather than pass
    it, each found by review of the first fix: dropping the anchor and the block,
    parking the claim inside a second copy of the generator's own markers,
    ending a repository-wide claim with a clause that merely mentions the domain,
    and declaring a template pack by linking its directory.

    Three more came out of the review after that, which broke the scoping test
    four ways with the same trick: a trailing clause of any shape, backticks
    round the template stem, and a closer written before its opener, which used
    to reach the operator as a traceback rather than a named reason.
    """

    CARD = "knowledge/domains/capital-markets.md"

    def copy(self, tmp):
        """examples/, knowledge/ and templates/, which is all this gate reads."""
        root = Path(tmp).resolve() / "repo"
        for name in ("examples", "knowledge", "templates"):
            shutil.copytree(REPO / name, root / name,
                            ignore=shutil.ignore_patterns("._*"))
        return root

    def gate(self, root):
        with unittest.mock.patch.object(example_availability, "ROOT", root):
            return quietly(example_availability.main, ["--check"])

    def generate(self, root):
        with unittest.mock.patch.object(example_availability, "ROOT", root):
            return quietly(example_availability.main, [])

    def test_the_tree_as_it_stands_is_fresh(self):
        code, output = quietly(example_availability.main, ["--check"])
        self.assertEqual(0, code, output)

    def test_adding_a_declared_example_stales_the_card_that_bends_it(self):
        """The seed a hand-written sentence cannot catch: a new filled example
        of a bent template lands and the card still says what it said."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            (root / "examples" / "domain-capital-markets-observability.md"
             ).write_text(
                "# Observability: Tallyhouse Markets\n\n"
                "Fills [templates/architecture/observability.md]"
                "(../templates/architecture/observability.md). Everything "
                "here is invented.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("stale: %s" % self.CARD, output)

    def test_removing_a_declared_example_stales_the_card_that_bends_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            (root / "examples" / "harbourgate-failure-scenarios.md").unlink()
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("stale: %s" % self.CARD, output)

    def test_a_hand_written_repository_wide_absence_claim_fails(self):
        """The seed regeneration alone cannot catch: the generated paragraph is
        fresh and the card's own prose says the opposite beside it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            card.write_text(card.read_text(encoding="utf-8") +
                            "\nNo filled failure-scenarios example exists "
                            "anywhere in the repository yet.\n",
                            encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("hand-written absence claim: %s" % self.CARD, output)

    def test_a_claim_scoped_to_one_domain_is_allowed(self):
        """Global existence and domain applicability are different statements:
        this gate refuses the first in prose and permits the second."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            card.write_text(card.read_text(encoding="utf-8") +
                            "\nfailure-scenarios has no filled example in the "
                            "repository yet for this domain.\n",
                            encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(0, code, output)

    def test_a_card_that_drops_the_anchor_and_the_block_is_not_excused(self):
        """The hole that made every other seed here optional: a card with no
        anchor and no block is regenerated by nothing, so it must fail rather
        than be counted fresh."""
        card = "knowledge/domains/travel-hospitality.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            path = root / card
            text = path.read_text(encoding="utf-8")
            start = text.index(example_availability.BEGIN)
            finish = text.index(example_availability.END) + len(example_availability.END)
            text = text[:start] + text[finish:]
            text = "".join(line for line in text.splitlines(keepends=True)
                           if not line.startswith(example_availability.ANCHOR))
            path.write_text(text, encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("no generated block: %s" % card, output)

    def test_a_second_generated_block_cannot_launder_an_absence_claim(self):
        """Only the first marker pair is regenerated, so a second pair is a
        place to park a false claim where nothing rewrites it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            card = root / self.CARD
            card.write_text(
                card.read_text(encoding="utf-8") + "\n" +
                example_availability.BEGIN + "\nNo filled failure-scenarios "
                "example exists anywhere in the repository.\n" +
                example_availability.END + "\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("no generated block: %s" % self.CARD, output)

    def test_the_prose_scan_reads_past_the_first_marker_pair(self):
        """The second lock on the same door as the test above: even if a card
        with two marker pairs reached the prose scan, only the first pair is
        dropped, because only the first pair is ever regenerated."""
        begin, end = example_availability.BEGIN, example_availability.END
        text = ("%s\nfresh generated prose\n%s\n\n%s\nNo filled "
                "failure-scenarios example exists anywhere in the repository.\n%s\n"
                % (begin, end, begin, end))
        self.assertEqual(
            ["No filled failure-scenarios example exists anywhere in the repository"],
            example_availability.handwritten_absence(text))

    def test_a_scoping_phrase_must_end_the_claim_it_scopes(self):
        """Mentioning the domain in a trailing clause does not make a
        repository-wide claim a claim about one domain."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            card.write_text(
                card.read_text(encoding="utf-8") +
                "\nNo filled failure-scenarios example exists in this "
                "repository, which matters most for this domain because the "
                "kill switch lives there.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("hand-written absence claim: %s" % self.CARD, output)

    def test_a_trailing_clause_cannot_scope_a_repository_wide_claim(self):
        """A sentence that merely ends in the scoping words has not scoped
        anything: each of these opens a new clause after a false
        repository-wide claim, and each is checked on its own so that no one
        of the four can pass inside a batch that fails for another."""
        variants = [
            "No filled failure-scenarios example exists in this repository, "
            "and none is planned for this domain.",
            "No filled failure-scenarios example exists in this repository, "
            "though the gap is felt most keenly for this domain.",
            "No filled failure-scenarios example exists in this repository; "
            "that gap is the one that hurts for this domain.",
            "No filled failure-scenarios example exists in this repository "
            "and none is planned for this domain.",
        ]
        for sentence in variants:
            with self.subTest(sentence=sentence):
                with tempfile.TemporaryDirectory() as tmp:
                    root = self.copy(tmp)
                    card = root / self.CARD
                    card.write_text(card.read_text(encoding="utf-8") +
                                    "\n" + sentence + "\n", encoding="utf-8")
                    code, output = self.gate(root)
                self.assertEqual(1, code, output)
                self.assertIn("hand-written absence claim: %s" % self.CARD,
                              output)

    def test_markdown_emphasis_does_not_hide_an_absence_claim(self):
        """Backticks round the template stem are a disguise, not a different
        sentence, and the generator's own wording of where is not a way out
        of a claim written by hand."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            card.write_text(card.read_text(encoding="utf-8") +
                            "\nNo filled `failure-scenarios` example exists "
                            "anywhere in this repository.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("hand-written absence claim: %s" % self.CARD, output)

    def test_a_closer_before_its_opener_is_named_not_a_traceback(self):
        """One of each marker in the wrong order is still a card with no
        readable block, so the gate names it rather than raising out of
        render()."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            text = card.read_text(encoding="utf-8")
            start = text.index(example_availability.BEGIN)
            finish = text.index(example_availability.END) + len(example_availability.END)
            text = text[:start] + text[finish:]
            card.write_text("%s\n%s\n%s\n" % (text, example_availability.END,
                                              example_availability.BEGIN),
                            encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("no generated block: %s" % self.CARD, output)
        self.assertIn("closer before its opener", output)

    def test_a_claim_moved_into_the_directory_readme_is_still_read(self):
        """The layer one file out: knowledge/domains/README.md carries no
        generated paragraph, so a claim parked there would be regenerated by
        nothing. It is read for claims like the cards beside it."""
        sidecar = "knowledge/domains/README.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            path = root / sidecar
            path.write_text(path.read_text(encoding="utf-8") +
                            "\nNo filled failure-scenarios example exists in "
                            "this repository.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("hand-written absence claim: %s" % sidecar, output)

    def test_a_claim_that_wraps_across_two_lines_is_still_one_claim(self):
        """A line break is not a disguise: the prose is read the way a reader
        reads it, not the way the file happens to be wrapped."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            card = root / self.CARD
            card.write_text(
                card.read_text(encoding="utf-8") +
                "\nNo filled failure-scenarios example exists in this\n"
                "repository.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("hand-written absence claim: %s" % self.CARD, output)

    def test_a_pack_link_counts_every_template_in_the_pack(self):
        """knowledge/domains/ai-products.md declares its pack by linking the
        directory, so a template landing in that directory is a template it
        bends and the card goes stale."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.copy(tmp)
            self.assertEqual(0, self.gate(root)[0])
            (root / "templates" / "ai" / "zz-illustrative-template.md").write_text(
                "# Illustrative\n\nInvented for a test.\n", encoding="utf-8")
            code, output = self.gate(root)
        self.assertEqual(1, code, output)
        self.assertIn("stale: knowledge/domains/ai-products.md", output)

    def test_the_release_suite_runs_this_gate(self):
        """A generator nothing invokes is a generator nothing checks."""
        argvs = [tuple(gate.argv) for gate in ci_gate.GATES]
        self.assertIn(("python3", "tools/example_availability.py", "--check"),
                      argvs)
# The roadmap commitment contract. F04 of the 2026-09-23 external audit: a
# roadmap row carried no stable id and no accountable owner, and the skill that
# drives the template asked for an 80 percent capacity line, quarterly entry and
# exit gates and a defence page that the template had no field for. The
# counterexamples live as documents under tests/fixtures/roadmap/ rather than as
# strings here, so each one can be read, and run through the gate by hand, as
# the thing a PM would actually have written.
ROADMAP_FIXTURES = REPO / "tests" / "fixtures" / "roadmap"

# Each row is one GUARD SITE: the fixture that breaks it, the message format
# string the site reports, and the edit that reverts that site ALONE. The
# reversion tests below apply each edit to a copy of tools/docs_contract.py and
# assert that the site's message stops being reported.
#
# Keyed by site rather than by issue code, because a code is not a guard. Five
# codes here are reported from two or three places, so a matrix keyed by code
# calls a code covered when one of its sites is pinned and leaves the others
# deletable with the suite green - which is what the external review of
# 2026-09-23 found for six sites, including the capacity arithmetic itself.
ROADMAP_REVERSIONS = (
    ("ownerless", "ownerless.md",
     "%s names no accountable owner",
     '            if _blank_cell(cell_at("owner")):',
     "            if False:"),
    ("two owners", "two-owners.md",
     "%s names more than one owner: accountability splits and nobody carries it",
     '            elif re.search(r",|;|/| and |&|\\+", owner):',
     "            elif False:"),
    ("over capacity", "over-capacity.md",
     "'%s' commits %s against a plannable %s: Now is over capacity and an "
     "initiative moves to Next",
     "        elif total > ceiling:",
     "        elif False:"),
    ("phantom reservation", "phantom-reservation.md",
     "'%s' declares %s reserved by Now and no record reserves anything on it",
     "        if team not in booked and declared:",
     "        if False:"),
    ("capacity arithmetic", "capacity-mismatch.md",
     "'%s' declares %s reserved by Now and its records reserve %s",
     "        if declared is None or abs(declared - total) > 1e-9:",
     "        if False:"),
    ("no plannable figure", "no-plannable.md",
     "'%s' states no plannable figure",
     '            issues.append(Issue("error", "roadmap-capacity-total", name, line_no,\n'
     '                                "\'%s\' states no plannable figure" % team))',
     '            issues.append(Issue("warning", "roadmap-ignored", name, line_no,\n'
     '                                "(reverted) %s" % team))'),
    ("two capacity rows for one team", "duplicate-capacity-row.md",
     "team '%s' has more than one capacity line row",
     "            if team in plannable:",
     "            if False:"),
    ("the wrong unit", "wrong-unit.md",
     "'%s' reserves in %s and its capacity line is in %s",
     "        if len(units) > 1 or (unit and units and unit not in units):",
     "        if False:"),
    ("unknown dependency", "unknown-dependency.md",
     "%s depends on %s, which has no row in the dependency index",
     "                    elif token not in governed:",
     "                    elif False:"),
    ("a dependency id that is not an id", "malformed-dependency.md",
     "%s cites '%s', which is not a dependency id",
     "                    if not IDENTIFIER.match(token):",
     "                    if False:"),
    ("the dependencies a reader sees", "dependency-mismatch.md",
     "%s publishes %s in Now and %s in its record: the table a reader sees and "
     "the record disagree",
     "            if published != recorded:",
     "            if False:"),
    # Rows that revert the finding rather than the branch: the code that follows
    # them reads the entry the guard just proved absent, so deleting the branch
    # would raise instead of passing, and an exception is not evidence that a
    # counterexample was allowed through.
    ("unknown team", "unknown-team.md",
     "%s reserves capacity on '%s', which has no capacity line row",
     '            issues.append(Issue("error", "roadmap-capacity-team", name, seen[0][1],\n'
     '                                "%s reserves capacity on \'%s\', which has no capacity "\n'
     '                                "line row" % (seen[0][0], team)))',
     '            issues.append(Issue("warning", "roadmap-ignored", name, seen[0][1],\n'
     '                                "(reverted) %s %s" % (seen[0][0], team)))'),
    ("missing record", "no-record.md",
     "%s is committed in Now with no initiative record",
     '                issues.append(Issue("error", "roadmap-record-missing", name, line_no,\n'
     '                                    "%s is committed in Now with no initiative record"\n'
     '                                    % identifier))',
     '                issues.append(Issue("warning", "roadmap-ignored", name, line_no,\n'
     '                                    "(reverted) %s" % identifier))'),
    ("a record field that is missing", "no-appetite.md",
     "%s's record has no '%s' field",
     '                    issues.append(Issue("error", "roadmap-record-field", name,\n'
     '                                        record["line"],\n'
     '                                        "%s\'s record has no \'%s\' field" % (identifier, key)))',
     '                    issues.append(Issue("warning", "roadmap-ignored", name,\n'
     '                                        record["line"],\n'
     '                                        "(reverted) %s %s" % (identifier, key)))'),
    ("a record field that is blank", "blank-appetite.md",
     "%s's '%s' is unfilled",
     "                elif _blank_cell(entry[1]):",
     "                elif False:"),
    ("commitment type", "shaped-in-now.md",
     "%s sits in Now, so its commitment type is 'committed', not '%s'",
     '            if commitment != "committed":',
     "            if False:"),
    ("owner mismatch", "owner-mismatch.md",
     "%s is owned by %s in Now and %s in its record",
     "            if record_owner and owner and record_owner != owner:",
     "            if False:"),
    ("reservation grammar", "bad-reservation.md",
     "%s's capacity reservation must read '<n> <unit> on <team>, reserved in "
     "[capacity plan](<link>)'",
     "            if entry is not None and not _blank_cell(entry[1]) and booking is None:",
     "            if False:"),
    ("the period with no gate", "no-gate.md",
     "%s targets '%s', which has no entry and exit gate",
     '                issues.append(Issue("error", "roadmap-quarterly-gate", name, line_no,\n'
     '                                    "%s targets \'%s\', which has no entry and exit gate"\n'
     '                                    % (identifier, period)))',
     '                issues.append(Issue("warning", "roadmap-ignored", name, line_no,\n'
     '                                    "(reverted) %s %s" % (identifier, period)))'),
    ("a gate row with a blank cell", "blank-gate.md",
     "the '%s' period has no %s",
     "                    if position >= len(gate_cells) or _blank_cell(gate_cells[position]):",
     "                    if False:"),
    ("two gate rows for one period", "duplicate-gate.md",
     "the '%s' period has more than one gate row",
     "            if period in gates:",
     "            if False:"),
    ("a row with no period at all", "no-period.md",
     "%s names no target period, so no entry and exit gate governs it",
     '            if _blank_cell(cell_at("target period")):',
     "            if False:"),
    ("defence page", "no-defence.md",
     "the defence page needs '%s'",
     '        if not re.search(r"^%s\\s*$" % re.escape(heading), defence, re.M):',
     "        if False:"),
    ("the defence page is a place, not a phrase", "defence-elsewhere.md",
     "the defence page needs '%s'",
     '    defence = "\\n".join(line for span in spans.get("Defence page") or ()\n'
     "                        for line in lines[span[0]:span[1]])",
     '    defence = "\\n".join(lines)'),
    ("headings hidden in a comment", "defence-in-a-comment.md",
     "the defence page needs '%s'",
     "    blanked = COMMENT_BLOCK.sub(lambda m: re.sub(r\"[^\\n]\", \" \", m.group(0)), text)",
     "    blanked = text"),
    ("missing section", "no-records-section.md",
     "a roadmap needs a '%s' section",
     "        if not _roadmap_sections(lines, label, level=REQUIRED_SECTION_LEVEL):",
     "        if False:"),
    ("the columns of every table", "dropped-columns.md",
     "the %s table needs a '%s' column",
     "                if found is None:",
     "                if False:"),
    ("no initiative id", "no-id.md",
     "a %s row needs a stable initiative id",
     "            if not IDENTIFIER.match(identifier):",
     "            if False:"),
    ("no outcome", "no-outcome.md",
     "%s names no outcome",
     '            if _blank_cell(cell_at("outcome")):',
     "            if False:"),
    ("the decision link", "no-decision-link.md",
     "%s's rejected options and override decision names no decision record to follow",
     "            if (decision is not None and not _blank_cell(decision[1])\n"
     "                    and not MD_LINK_TEXT.search(_bare(decision[1]))):",
     "            if False:"),
    ("two records for one initiative", "duplicate-record.md",
     "initiative %s has more than one record",
     "        if key in by_id:",
     "        if False and key in by_id:"),
    ("an HTML table is not a table this reads", "html-table.md",
     "the %s section holds an HTML table at line %d: this check reads markdown "
     "tables, so nothing reads that one",
     "                if HTML_TABLE.search(lines[index]):",
     "                if False:"),
    # The parser rows. Each fixture parks the SAME ownerless committed row in a
    # different legal markdown spelling, so each reversion below is a spelling
    # of the horizon table or its heading that a reader reads and this check
    # would stop reading.
    ("every table in a section", "second-table.md",
     "%s names no accountable owner",
     "            yield header_cells, rows\n            index = cursor\n            continue",
     "            yield header_cells, rows\n            return"),
    ("a blank line does not end the section", "blank-line-split.md",
     "%s names no accountable owner",
     "            yield header_cells, rows\n            index = cursor\n            continue",
     "            yield header_cells, rows\n"
     "            if cursor < end and not lines[cursor].strip():\n"
     "                return\n"
     "            index = cursor\n            continue"),
    ("a table without leading pipes", "pipeless-table.md",
     "%s names no accountable owner",
     '        if header and not header.startswith("#") and _is_table_delimiter(delimiter):',
     '        if header.startswith("|") and _is_table_delimiter(delimiter):'),
    ("a delimiter row with the wrong cell count", "ragged-table.md",
     "%s names no accountable owner",
     "            header_cells = _roadmap_cells(header)\n"
     "            rows, cursor = [], index + 2",
     "            header_cells = _roadmap_cells(header)\n"
     "            if len(_roadmap_cells(delimiter)) != len(header_cells):\n"
     "                index += 1\n"
     "                continue\n"
     "            rows, cursor = [], index + 2"),
    ("a row without leading pipes", "pipeless-row.md",
     "%s names no accountable owner",
     '    return bool(text and "|" in text and not BLOCK_START.match(text))',
     '    return text.startswith("|")'),
    ("every section with the heading", "second-now-section.md",
     "%s names no accountable owner",
     "    for span in sorted(found):",
     "    for span in sorted(found)[:1]:"),
    ("a heading in another case", "now-in-caps.md",
     "%s names no accountable owner",
     '    wanted = re.compile(r"%s\\b" % re.escape(section), re.I)',
     '    wanted = re.compile(r"%s\\b" % re.escape(section))'),
    ("a heading in bold", "now-in-bold.md",
     "%s names no accountable owner",
     '    return re.sub(r"[*_`]", "", MD_LINK_TEXT.sub(r"\\1", text)).strip()',
     "    return text.strip()"),
    ("a heading underlined instead of hashed", "now-underlined.md",
     "%s names no accountable owner",
     '        under = (re.match(r"^ {0,3}(=+|-+)\\s*$", lines[index + 1])\n'
     "                 if index + 1 < len(lines) else None)",
     "        under = None"),
    ("a heading at another level", "now-deeper-heading.md",
     "%s names no accountable owner",
     "        if level is not None and heading_level != level:",
     "        if heading_level != (2 if level is None else level):"),
)


def site_pattern(site):
    """The regex one guard site's messages match: its format string, filled in."""
    return re.compile("^%s$" % re.escape(site).replace("%s", ".*").replace("%d", ".*"))


def roadmap_issue_sites(source):
    """Every place tools/docs_contract.py reports a roadmap issue, by message.

    Read from the syntax tree rather than from the issue codes, because a code
    is not a place: this is what makes the matrix below a closed inventory.
    """
    sites = set()
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "Issue" and len(node.args) >= 5):
            continue
        code = node.args[1]
        if not (isinstance(code, ast.Constant)
                and str(code.value).startswith("roadmap-")):
            continue
        message = node.args[4]
        while isinstance(message, ast.BinOp) and isinstance(message.op, ast.Mod):
            message = message.left
        if isinstance(message, ast.Constant) and isinstance(message.value, str):
            sites.add(message.value)
        else:
            # A message this cannot read is still a site. Recorded rather than
            # skipped, so a guard written with an f-string cannot join the
            # check by being unreadable to its own inventory.
            sites.add("<message built at line %d>" % node.lineno)
    return sites


def roadmap_issues(name):
    """What tools/docs_contract.py reports for one fixture."""
    from tools.docs_contract import check_roadmap
    path = ROADMAP_FIXTURES / name
    return check_roadmap(name, path.read_text(encoding="utf-8"))


def roadmap_codes(name):
    """The issue codes reported for one fixture."""
    return {issue.code for issue in roadmap_issues(name)}


def roadmap_messages(name):
    """The issue messages reported for one fixture."""
    return [issue.message for issue in roadmap_issues(name)]


class RoadmapCommitmentGateTests(unittest.TestCase):
    """Each counterexample is refused, and the one that resolves is allowed.

    The positive control matters as much as the counterexamples: a check that
    refuses everything closes the finding on paper and makes the template
    unusable, which is the failure the audit calls weakening a claim to pass.
    """

    def test_a_committed_row_that_resolves_is_allowed(self):
        self.assertEqual(set(), roadmap_codes("committed.md"))

    def test_an_escaped_pipe_in_a_cell_does_not_shift_the_columns(self):
        """A second positive control. "\\|" renders as a pipe inside one cell;
        splitting on it would read the cell beside the one a reader sees."""
        self.assertEqual(set(), roadmap_codes("escaped-pipe.md"))

    def test_the_three_shipped_roadmaps_pass_the_contract(self):
        from tools.docs_contract import check_roadmaps
        self.assertEqual([], check_roadmaps(REPO))

    def test_an_ownerless_now_row_cannot_be_committed(self):
        self.assertIn("roadmap-owner", roadmap_codes("ownerless.md"))

    def test_a_now_row_owned_by_two_people_cannot_be_committed(self):
        self.assertIn("roadmap-owner", roadmap_codes("two-owners.md"))

    def test_an_over_capacity_now_cannot_be_committed(self):
        self.assertIn("roadmap-over-capacity", roadmap_codes("over-capacity.md"))

    def test_a_capacity_row_reserving_what_no_record_booked_is_refused(self):
        self.assertIn("roadmap-capacity-total", roadmap_codes("phantom-reservation.md"))

    def test_a_reservation_on_a_team_with_no_capacity_row_is_refused(self):
        self.assertIn("roadmap-capacity-team", roadmap_codes("unknown-team.md"))

    def test_a_dependency_nobody_governs_is_refused(self):
        self.assertIn("roadmap-dependency-record", roadmap_codes("unknown-dependency.md"))

    def test_a_now_row_with_no_initiative_record_is_refused(self):
        self.assertIn("roadmap-record-missing", roadmap_codes("no-record.md"))

    def test_a_record_missing_its_appetite_is_refused(self):
        self.assertIn("roadmap-record-field", roadmap_codes("no-appetite.md"))

    def test_a_now_row_whose_record_calls_itself_shaped_is_refused(self):
        self.assertIn("roadmap-commitment-type", roadmap_codes("shaped-in-now.md"))

    def test_a_row_and_its_record_naming_different_owners_is_refused(self):
        self.assertIn("roadmap-owner-mismatch", roadmap_codes("owner-mismatch.md"))

    def test_a_reservation_written_as_prose_is_refused(self):
        self.assertIn("roadmap-capacity-reservation", roadmap_codes("bad-reservation.md"))

    def test_a_now_period_with_no_entry_and_exit_gate_is_refused(self):
        self.assertIn("roadmap-quarterly-gate", roadmap_codes("no-gate.md"))

    def test_a_roadmap_without_a_defence_page_heading_is_refused(self):
        self.assertIn("roadmap-defence", roadmap_codes("no-defence.md"))

    def test_a_roadmap_with_no_initiative_records_section_is_refused(self):
        self.assertIn("roadmap-section", roadmap_codes("no-records-section.md"))

    def test_a_decision_field_with_no_record_to_follow_is_refused(self):
        self.assertIn("roadmap-decision-link", roadmap_codes("no-decision-link.md"))

    def test_a_now_row_that_names_no_outcome_is_refused(self):
        self.assertIn("roadmap-outcome", roadmap_codes("no-outcome.md"))

    def test_a_now_row_with_no_stable_id_is_refused(self):
        self.assertIn("roadmap-initiative-id", roadmap_codes("no-id.md"))

    def test_a_reservation_in_the_wrong_unit_is_refused(self):
        self.assertIn("roadmap-capacity-unit", roadmap_codes("wrong-unit.md"))

    def test_two_records_for_one_initiative_are_refused(self):
        self.assertIn("roadmap-record-duplicate", roadmap_codes("duplicate-record.md"))


class RoadmapTableParserTests(unittest.TestCase):
    """The trap the audit names: a parser that reads the first table under a
    heading, or stops at the first blank line, is itself the bypass. Every one
    of these fixtures hides an ownerless committed row where such a parser
    would never look."""

    def test_a_row_in_a_second_table_under_now_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("second-table.md"))

    def test_a_row_after_a_blank_line_between_two_tables_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("blank-line-split.md"))

    def test_a_row_under_a_second_now_heading_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("second-now-section.md"))

    def test_a_row_in_a_table_written_without_leading_pipes_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("pipeless-table.md"))

    def test_a_row_written_without_leading_pipes_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("pipeless-row.md"))

    def test_a_row_under_a_ragged_delimiter_row_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("ragged-table.md"))

    def test_cells_are_split_where_the_renderer_splits_them(self):
        from tools.docs_contract import _roadmap_cells
        self.assertEqual(["F-1", "A | B", "Ada"], _roadmap_cells(r"| F-1 | A \| B | Ada |"))
        self.assertEqual(["A", "B", "C"], _roadmap_cells("A | B | C"))

    def test_a_row_under_a_now_heading_in_capitals_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("now-in-caps.md"))

    def test_a_row_under_a_now_heading_in_bold_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("now-in-bold.md"))

    def test_a_row_under_an_underlined_now_heading_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("now-underlined.md"))

    def test_a_row_under_a_deeper_now_heading_is_read(self):
        self.assertIn("roadmap-owner", roadmap_codes("now-deeper-heading.md"))

    def test_a_horizon_row_written_as_an_html_table_is_reported(self):
        self.assertIn("roadmap-html-table", roadmap_codes("html-table.md"))

    def test_a_pipeless_table_yields_the_same_rows_as_a_piped_one(self):
        from tools.docs_contract import _roadmap_tables
        piped = ["| A | B |", "|---|---|", "| 1 | 2 |"]
        pipeless = ["A | B", "--- | ---", "1 | 2"]
        self.assertEqual(
            [(["A", "B"], [(3, ["1", "2"])])],
            [(header, rows) for header, rows in _roadmap_tables(piped, 0, 3)])
        self.assertEqual(
            [(["A", "B"], [(3, ["1", "2"])])],
            [(header, rows) for header, rows in _roadmap_tables(pipeless, 0, 3)])

    def test_a_thematic_break_and_a_frontmatter_fence_are_not_tables(self):
        from tools.docs_contract import _roadmap_tables
        lines = ["Some prose", "---", "more prose", "", "---", "key: value", "---"]
        self.assertEqual([], list(_roadmap_tables(lines, 0, len(lines))))

    def test_a_heading_is_matched_in_any_case_and_through_emphasis(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["## NOW (continued)", "a", "## **Now** again", "b",
                 "## Next", "c", "#### now once more", "d"]
        self.assertEqual([(1, 2), (3, 4), (7, 8)],
                         _roadmap_sections(lines, "Now"))

    def test_an_underlined_heading_is_a_heading(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["NOW (continued)", "---", "a", "", "## Next", "b"]
        self.assertEqual([(2, 4)], _roadmap_sections(lines, "Now"))

    def test_the_required_level_can_be_asked_for_on_its_own(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["#### Now (continued)", "a", "## Now", "b"]
        self.assertEqual([(1, 2), (3, 4)], _roadmap_sections(lines, "Now"))
        self.assertEqual([(3, 4)], _roadmap_sections(lines, "Now", level=2))

    def test_a_repeat_nested_under_its_own_section_is_read_once(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["## Now", "a", "### Now (continued)", "b", "## Next", "c"]
        self.assertEqual([(1, 4)], _roadmap_sections(lines, "Now"))

    def test_a_heading_that_exists_only_inside_a_comment_does_not_count(self):
        self.assertIn("roadmap-defence", roadmap_codes("defence-in-a-comment.md"))

    def test_a_second_table_that_drops_the_id_and_owner_columns_is_reported(self):
        codes = roadmap_codes("dropped-columns.md")
        self.assertIn("roadmap-columns", codes)

    def test_every_table_in_the_section_is_yielded(self):
        from tools.docs_contract import _roadmap_tables
        lines = ["| A | B |", "|---|---|", "| 1 | 2 |", "",
                 "prose between them", "",
                 "| C | D |", "|---|---|", "| 3 | 4 |"]
        found = list(_roadmap_tables(lines, 0, len(lines)))
        self.assertEqual([["A", "B"], ["C", "D"]], [header for header, _ in found])
        self.assertEqual([1, 1], [len(rows) for _, rows in found])

    def test_a_section_span_ends_at_the_next_heading_of_its_level(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["## Now", "", "a", "", "### Sub", "b", "", "## Next", "c"]
        self.assertEqual([(1, 7)], _roadmap_sections(lines, "Now"))

    def test_every_section_carrying_the_heading_is_returned(self):
        from tools.docs_contract import _roadmap_sections
        lines = ["## Now", "a", "## Next", "b", "## Now again", "c"]
        self.assertEqual([(1, 2), (5, 6)], _roadmap_sections(lines, "Now"))


class RoadmapContractWiringTests(unittest.TestCase):
    """The check has to run where the tree's document checks run, and it has to
    find every roadmap in the tree rather than a list of paths kept here."""

    def test_the_roadmap_check_runs_inside_the_docs_contract(self):
        source = (TOOLS / "docs_contract.py").read_text(encoding="utf-8")
        self.assertIn("issues.extend(check_roadmaps(root))", source)
        self.assertIn(("python3", "tools/docs_contract.py", "--strict"),
                      tuple(gate.argv for gate in ci_gate.GATES))

    def test_the_scan_finds_every_roadmap_document_in_the_tree(self):
        from tools.docs_contract import roadmap_documents
        found = {name for name, _ in roadmap_documents(REPO)}
        self.assertEqual({"templates/planning/roadmap.md",
                          "examples/expense-copilot-roadmap.md",
                          "examples/ledgerline-roadmap.md"}, found)

    def test_a_roadmap_added_anywhere_else_in_the_tree_is_found(self):
        from tools.docs_contract import roadmap_documents
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "os").mkdir()
            (root / "os" / "stray.md").write_text("# Roadmap: Stray\n", encoding="utf-8")
            (root / "os" / "other.markdown").write_text("# Roadmap: Other\n",
                                                        encoding="utf-8")
            (root / "tests" / "fixtures").mkdir(parents=True)
            (root / "tests" / "fixtures" / "counter.md").write_text(
                "# Roadmap: Counterexample\n", encoding="utf-8")
            self.assertEqual({"os/stray.md", "os/other.markdown"},
                             {name for name, _ in roadmap_documents(root)})

    def test_a_roadmap_that_was_retitled_is_still_found(self):
        """Discovery on the title alone is discovery a rename walks out of."""
        from tools.docs_contract import is_roadmap, roadmap_documents
        text = (ROADMAP_FIXTURES / "committed.md").read_text(encoding="utf-8")
        renamed = text.replace("# Roadmap: Fixture Product",
                               "# Product roadmap for the fixture", 1)
        self.assertNotIn("# Roadmap:", renamed)
        self.assertTrue(is_roadmap(renamed))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "os").mkdir()
            (root / "os" / "renamed.md").write_text(renamed, encoding="utf-8")
            self.assertEqual({"os/renamed.md"},
                             {name for name, _ in roadmap_documents(root)})

    def test_a_document_that_is_only_about_roadmaps_is_not_one(self):
        """The skill that writes roadmaps is not a roadmap, and neither is the
        framework page that explains the horizons."""
        from tools.docs_contract import is_roadmap
        for path in ("skills/roadmap-builder/SKILL.md",
                     "frameworks/prioritization/now-next-later.md",
                     "examples/ledgerline-now-next-later.md"):
            with self.subTest(document=path):
                self.assertFalse(is_roadmap((REPO / path).read_text(encoding="utf-8")))

    def test_the_template_carries_a_field_for_every_required_record_line(self):
        from tools.docs_contract import RECORD_FIELDS
        text = (REPO / "templates" / "planning" / "roadmap.md").read_text(encoding="utf-8")
        for key in RECORD_FIELDS:
            with self.subTest(field=key):
                self.assertRegex(text.lower(), r"(?m)^- \*\*%s" % re.escape(key))


class RoadmapReversionTests(unittest.TestCase):
    """The revert matrix, executed. Every guard site above is removed on its
    own in a copy of the tool, and the message that site reports must stop
    appearing for its counterexample. A guard that survives its own reversion
    was never the thing doing the work, and a site that no row reverts is a
    site that can be deleted with this suite green.
    """

    def run_reverted(self, old, new, fixture):
        """Run one fixture through a copy of the gate with one site removed.

        The patched source is written to a temporary directory and run as its
        own process rather than copied into a whole tree: tools/docs_contract.py
        imports nothing from this repository, and --roadmap reads the document
        by path, so forty tree copies would only make the matrix slow enough
        that it stopped being run.
        """
        source = (TOOLS / "docs_contract.py").read_text(encoding="utf-8")
        self.assertIn(old, source, "the reverted guard is not in the source")
        self.assertEqual(1, source.count(old),
                         "the reverted guard is not unique in the source")
        with tempfile.TemporaryDirectory() as tmp:
            patched = Path(tmp) / "docs_contract.py"
            patched.write_text(source.replace(old, new, 1), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(patched), "--json", "--roadmap",
                 str(ROADMAP_FIXTURES / fixture)],
                capture_output=True, text=True)
            self.assertEqual("", result.stderr, result.stderr)
            return {issue["message"] for issue in json.loads(result.stdout)}

    def test_every_guard_is_load_bearing_on_its_own(self):
        for label, fixture, site, old, new in ROADMAP_REVERSIONS:
            with self.subTest(guard=label):
                pattern = site_pattern(site)
                self.assertTrue(
                    any(pattern.match(message) for message in roadmap_messages(fixture)),
                    "%s: %s stopped reporting %r" % (label, fixture, site))
                after = self.run_reverted(old, new, fixture)
                self.assertFalse(
                    any(pattern.match(message) for message in after),
                    "%s: reverting this guard alone changed nothing, so it is "
                    "not what catches %s" % (label, fixture))

    def test_the_matrix_pins_every_guard_the_check_reports(self):
        reported = roadmap_issue_sites(
            (TOOLS / "docs_contract.py").read_text(encoding="utf-8"))
        pinned = {site for _label, _fixture, site, _old, _new in ROADMAP_REVERSIONS}
        self.assertEqual(set(), reported - pinned,
                         "guard sites with no reversion row: %s"
                         % sorted(reported - pinned))
        self.assertEqual(set(), pinned - reported,
                         "reversion rows for a guard the check no longer reports: %s"
                         % sorted(pinned - reported))
class ApprovalGateTests(unittest.TestCase):
    """F13. The human-approval template used to stop at trigger, timeout and
    logging: nothing bound the yes to the bytes the approver saw, so an edited
    payload, an expired approval, a revoked one and one already spent all
    executed like a fresh one, and a send whose outcome was never established
    could be retried into a second real send. The template now carries R1 to R6
    and NAC-1 to NAC-6; these tests are what stops that being prose. Each
    negative fixture must be refused for its own rule, both positive controls
    must execute, and the document check must fail when a rule, a record field
    or a negative criterion is dropped from the template."""

    def test_every_rule_has_a_negative_fixture_and_a_criterion(self):
        self.assertEqual({criterion for _id, _name, _reason, criterion in RULES},
                         set(CASES))
        self.assertEqual(len(RULES), 6)

    def test_each_negative_case_is_refused_for_its_own_rule(self):
        reason_of = {criterion: (rule, reason)
                     for rule, _name, reason, criterion in RULES}
        for criterion, (approval, attempt, allowed, reason) in CASES.items():
            with self.subTest(criterion=criterion):
                self.assertFalse(allowed, "a negative fixture must expect a refusal")
                verdict = decide(approval, attempt)
                self.assertFalse(verdict.allowed,
                                 "%s executed; it must be refused" % criterion)
                self.assertEqual(reason, verdict.reason)
                rule, expected = reason_of[criterion]
                self.assertEqual(expected, verdict.reason)
                self.assertEqual(rule, verdict.rule)

    def test_the_positive_controls_execute(self):
        # Without these a decide() that refused everything would satisfy all
        # six negative fixtures, which is the way this guard fails open.
        for name, (approval, attempt, allowed, reason) in POSITIVE.items():
            with self.subTest(control=name):
                self.assertTrue(allowed)
                verdict = decide(approval, attempt)
                self.assertTrue(verdict.allowed,
                                "%s was refused: %s" % (name, verdict.reason))
                self.assertEqual(reason, verdict.reason)

    def test_an_unknown_outcome_blocks_the_retry_until_it_is_reconciled(self):
        # R6 read as one pair: the same approval and the same parameters, with
        # and without the reconciliation. The refusal has to come from the
        # reconciliation and nothing else.
        approval, blocked, _allowed, _reason = CASES["NAC-6"]
        self.assertEqual("unreconciled", decide(approval, blocked).reason)
        reconciled = Attempt(blocked.parameters, blocked.execution_token,
                             blocked.at, prior_outcome="unknown",
                             reconciled=True)
        self.assertEqual("replay", decide(approval, reconciled).reason)

    def test_the_shipped_documents_carry_the_whole_contract(self):
        self.assertEqual([], check_approvals(REPO))

    def test_dropping_a_rule_a_field_or_a_criterion_fails_the_check(self):
        # Every rule and every negative criterion, in BOTH documents, and every
        # record field in the template. Erosion takes one row at a time, and
        # the row someone drops next will not be the one a review happened to
        # try: proving R5 is caught in the template says nothing about R2 in
        # the example. The loops are driven by RULES and RECORD_FIELDS, so a
        # rule or field added later is swept without anyone remembering to.
        removals = []
        for rule_id, name, _reason, criterion in RULES:
            for relative in (TEMPLATE, EXAMPLE):
                removals.append((relative, "**%s %s.**" % (rule_id, name),
                                 "rule %s" % rule_id))
                removals.append((relative, "| %s |" % criterion,
                                 "negative criterion %s" % criterion))
        for field_name in RECORD_FIELDS:
            removals.append((TEMPLATE, "| %s |" % field_name,
                             "%r is not stated" % field_name))
        removals.append((TEMPLATE, "| State |", "State row"))
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative, marker, expected in removals:
                with self.subTest(document=relative, marker=marker):
                    path = root / relative
                    text = path.read_text(encoding="utf-8")
                    self.assertEqual(1, text.count(marker),
                                     "%r is not a unique row in %s"
                                     % (marker, relative))
                    kept = [line for line in text.splitlines(True)
                            if marker not in line]
                    path.write_text("".join(kept), encoding="utf-8")
                    issues = check_approvals(root)
                    path.write_text(text, encoding="utf-8")
                    self.assertTrue(issues, "removing %r from %s was not caught"
                                    % (marker, relative))
                    self.assertTrue(any(expected in issue and relative in issue
                                        for issue in issues),
                                    "%s was reported as %r" % (expected, issues))
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")
    def test_dropping_a_state_from_the_vocabulary_fails_the_check(self):
        # Erosion, not deletion: the State row survives with one state quietly
        # gone, which is how an executor stops recognising "revoked". All seven
        # states, driven by STATES, because the one dropped next will not be
        # the one review happened to try.
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / TEMPLATE
            text = path.read_text(encoding="utf-8")
            rows = [line for line in text.splitlines(True)
                    if line.startswith("| State |")]
            self.assertEqual(1, len(rows), "the template has no single State row")
            row = rows[0]
            for state in STATES:
                with self.subTest(state=state):
                    eroded = row.replace(state, "", 1)
                    self.assertNotEqual(row, eroded)
                    path.write_text(text.replace(row, eroded, 1),
                                    encoding="utf-8")
                    issues = check_approvals(root)
                    path.write_text(text, encoding="utf-8")
                    self.assertTrue(any("%r is not in the State row" % state
                                        in issue for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")
    def test_the_record_fields_and_states_are_the_ones_the_template_names(self):
        text = (REPO / "templates" / "ai"
                / "human-approval-gates.md").read_text(encoding="utf-8")
        self.assertEqual(7, len(RECORD_FIELDS))
        for name in RECORD_FIELDS:
            self.assertIn("| %s |" % name, text)
        for state in STATES:
            self.assertIn(state, text)

    # --- the guards below had no fixture of their own until review said so ---
    # Each one exists because reverting that single guard, alone, produced no
    # test failure at all. Two of the five were fail-opens: a forged execution
    # token executed, and an approval carrying no authority scope executed.

    def test_a_forged_execution_token_is_refused(self):
        # R5's own sentence promises "the same approval ID or execution token".
        # Every fixture presented the right token, so the comparison could be
        # deleted and a bogus token would execute.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        forged = Attempt(attempt.parameters, "tok-FORGED", attempt.at)
        verdict = decide(approval, forged)
        self.assertFalse(verdict.allowed, "a forged token executed")
        self.assertEqual("replay", verdict.reason)
        self.assertEqual("R5", verdict.rule)

    def test_an_empty_authority_scope_is_not_a_blank_cheque(self):
        # An approval whose authority scope answers nothing authorises nothing.
        # The default was deliberate and had no fixture, so flipping it to
        # `return True` let it through silently.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        unscoped = replace(approval, authority_scope={})
        verdict = decide(unscoped, attempt)
        self.assertFalse(verdict.allowed, "an empty scope authorised the send")
        self.assertEqual("out-of-scope", verdict.reason)
        self.assertEqual("R2", verdict.rule)

    def test_a_superseded_approval_is_refused_as_superseded(self):
        # It failed closed either way, but as "not-approved" under a different
        # branch, so the state that R1 exists to produce was never exercised.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        verdict = decide(replace(approval, state="superseded"), attempt)
        self.assertFalse(verdict.allowed)
        self.assertEqual("superseded", verdict.reason)
        self.assertEqual("R1", verdict.rule)

    def test_an_unrecognised_prior_outcome_is_rejected(self):
        # The live defect this round found. prior_outcome was unvalidated while
        # the approval's state was enforced, so prior_outcome="Unknown" was
        # allowed=True: a capitalisation typo turned off R6 and half of R5,
        # which is exactly the silent non-firing F13 exists to close.
        for bad in ("Unknown", "UNKNOWN", "ok", "", "timeout"):
            with self.subTest(prior_outcome=bad):
                with self.assertRaises(ValueError):
                    Attempt(PARAMS, "tok-1", NOW, prior_outcome=bad)
        for good in OUTCOMES:
            with self.subTest(prior_outcome=good):
                Attempt(PARAMS, "tok-1", NOW, prior_outcome=good)

    def test_a_limit_on_something_unmeasurable_is_refused_not_raised(self):
        # A ceiling on a non-numeric parameter used to raise TypeError out of
        # decide(). An exception is not one of the documented refusal paths, so
        # a caller wrapping decide() in a try/except could read a crash as
        # anything it liked.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        for scope in ({"action": "send", "max_recipient": 500},
                      {"action": "send", "max_amount": "lots"}):
            with self.subTest(scope=scope):
                verdict = decide(replace(approval, authority_scope=scope),
                                 attempt)
                self.assertFalse(verdict.allowed)
                self.assertEqual("out-of-scope", verdict.reason)
                self.assertEqual("R2", verdict.rule)
        # A bool is an int in Python, so True < 500 and a scope ceiling would
        # pass an amount of True. The approval below is bound to exactly those
        # parameters, so R1 cannot be what refuses it: only the scope check is
        # left to catch it.
        booleans = {**PARAMS, "amount": True}
        bound = replace(approval, action_revision=revision(booleans))
        verdict = decide(bound, Attempt(booleans, attempt.execution_token,
                                        attempt.at))
        self.assertFalse(verdict.allowed, "an amount of True was authorised")
        self.assertEqual("out-of-scope", verdict.reason)
        self.assertEqual("R2", verdict.rule)

    def test_the_expiry_boundary_is_the_one_the_rule_states(self):
        # R3 says "past its expires-at", so the last moment of the window still
        # executes and the next one does not. Pinned so the boundary cannot
        # drift by a character without a test saying so.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        at_the_edge = Attempt(attempt.parameters, attempt.execution_token,
                              approval.expires_at)
        self.assertTrue(decide(approval, at_the_edge).allowed,
                        "the last moment of the window was refused")
        past_it = Attempt(attempt.parameters, attempt.execution_token,
                          approval.expires_at + 1)
        verdict = decide(approval, past_it)
        self.assertFalse(verdict.allowed)
        self.assertEqual("expired", verdict.reason)
        self.assertEqual("R3", verdict.rule)

    def test_a_missing_document_is_reported_not_passed(self):
        # Deleting the template is the cheapest way past a check that only
        # reads documents it finds. One copy, restored between subtests.
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in ("templates/ai/human-approval-gates.md",
                             "examples/ledgerline-human-approval-gates.md"):
                with self.subTest(document=relative):
                    path = root / relative
                    kept = path.read_text(encoding="utf-8")
                    path.unlink()
                    issues = check_approvals(root)
                    path.write_text(kept, encoding="utf-8")
                    self.assertIn("%s: missing" % relative, issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_a_field_named_only_in_prose_is_not_a_record_field(self):
        # _field_row is anchored to the table row on purpose. Weakening it to a
        # bare substring produced no failure, because each field name happens
        # to appear exactly once; this fixture makes the anchoring load-bearing
        # rather than lucky.
        template = "templates/ai/human-approval-gates.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / template
            text = path.read_text(encoding="utf-8")
            prosed = text.replace(
                "| Single-use execution token | [token",
                "The Single-use execution token is mentioned here. [token", 1)
            self.assertNotEqual(text, prosed)
            path.write_text(prosed, encoding="utf-8")
            issues = check_approvals(root)
            self.assertTrue(
                any("'Single-use execution token' is not stated" in issue
                    for issue in issues), issues)

    # --- hollowing the document out without deleting a heading ---------------

    def test_commenting_the_rules_out_fails_the_check(self):
        # The lines survive inside <!-- ... --> and still satisfy a line-
        # anchored regex, while the rendered document says nothing at all.
        template = "templates/ai/human-approval-gates.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / template
            text = path.read_text(encoding="utf-8")
            start = text.index("1. **R1 binding.**")
            end = text.index("## 6. Negative")
            hidden = text[:start] + "<!--\n" + text[start:end] + "\n-->\n" \
                + text[end:]
            path.write_text(hidden, encoding="utf-8")
            issues = check_approvals(root)
            self.assertTrue(issues, "commenting the rules out was not caught")
            self.assertTrue(any("rule R1" in issue for issue in issues), issues)

    def test_gutting_a_rule_sentence_under_its_heading_fails_the_check(self):
        # The heading stays, the sentence stops saying the rule. Structure
        # alone cannot see this, which is why RULE_TERMS exists. All six rules
        # in both documents: a term list that is load-bearing for R5 and R6 and
        # decorative for the other four is not a term list.
        neutral = " This is left to the team's discretion.\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in (TEMPLATE, EXAMPLE):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                for rule_id, name, _reason, _criterion in RULES:
                    with self.subTest(document=relative, rule=rule_id):
                        heading = "**%s %s.**" % (rule_id, name)
                        gutted = []
                        for line in text.splitlines(True):
                            if heading in line:
                                line = line[:line.index(heading)] + heading \
                                    + neutral
                            gutted.append(line)
                        self.assertNotEqual(text, "".join(gutted))
                        path.write_text("".join(gutted), encoding="utf-8")
                        issues = check_approvals(root)
                        path.write_text(text, encoding="utf-8")
                        self.assertTrue(
                            any("rule %s (%s) no longer says" % (rule_id, name)
                                in issue and relative in issue
                                for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")
    def test_marking_the_contract_historical_fails_the_check(self):
        # Every structural match still passes; the reader is simply told to
        # ignore the section. One sentence per phrase in NULLIFIERS, in both
        # documents, plus the HTML-comment form -- the scan reads the raw
        # bytes precisely so a comment cannot hide the notice.
        sentences = {
            r"no longer required": "These rules are no longer required.\n",
            r"no longer appl": "This contract no longer applies.\n",
            r"\bhistorical\b": "This section is historical.\n",
            r"\bdeprecated\b": "This section is deprecated.\n",
            r"\bobsolete\b": "This section is obsolete.\n",
            r"not enforced": "These rules are not enforced.\n",
            r"for reference only": "This section is for reference only.\n",
            r"informational only": "This section is informational only.\n",
            r"does not apply": "This section does not apply.\n",
        }
        # A phrase added to NULLIFIERS without a fixture here would be
        # untested, so the inventory is closed rather than sampled.
        self.assertEqual(set(NULLIFIERS), set(sentences))
        markers = list(sentences.values()) + [
            "<!-- HISTORICAL, NO LONGER REQUIRED -->\n"]
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in (TEMPLATE, EXAMPLE):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                head = text.index("## 5. Invalidation")
                for marker in markers:
                    with self.subTest(document=relative, marker=marker):
                        path.write_text(text[:head] + marker + text[head:],
                                        encoding="utf-8")
                        issues = check_approvals(root)
                        path.write_text(text, encoding="utf-8")
                        self.assertTrue(
                            any("marked dead" in issue and relative in issue
                                for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")
    def test_dropping_a_record_field_from_the_example_fails_the_check(self):
        # The same hole one layer out: the fields were checked in the template
        # and not in the filled copy that a reader actually copies from.
        example = "examples/ledgerline-human-approval-gates.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / example
            text = path.read_text(encoding="utf-8")
            for name in RECORD_FIELDS:
                with self.subTest(field=name):
                    marker = "| %s |" % name
                    self.assertIn(marker, text)
                    kept = [line for line in text.splitlines(True)
                            if not line.startswith(marker)]
                    path.write_text("".join(kept), encoding="utf-8")
                    issues = check_approvals(root)
                    path.write_text(text, encoding="utf-8")
                    self.assertTrue(
                        any("%r is not stated" % name in issue
                            and example in issue for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")


    # --- the guards review found with no fixture of their own ---------------
    # Each of the four below was reverted ALONE, by an independent reviewer,
    # with the whole suite still green. Three were fail-opens: a denied
    # approval executed, a completed action ran a second time, and an action
    # outside the approver's authority executed. The other two in this block
    # are the neighbours of those three, found by asking what the same mistake
    # one column over would look like.

    def test_a_denied_or_pending_approval_is_not_approved(self):
        # decide()'s catch-all for every state that is not "approved". Deleting
        # it is invisible unless a fixture reaches a state no earlier branch
        # claims, and pending and denied were reached by no fixture at all: on
        # the reverted tree a DENIED approval executed.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        for state in ("pending", "denied"):
            with self.subTest(state=state):
                verdict = decide(replace(approval, state=state), attempt)
                self.assertFalse(verdict.allowed,
                                 "a %s approval executed" % state)
                self.assertEqual("not-approved", verdict.reason)
                self.assertEqual("R1", verdict.rule)

    def test_the_expired_state_is_refused_as_expired_not_as_not_approved(self):
        # R3 is two halves: the clock, and the state the clock or an operator
        # already wrote. Every fixture used the clock, so the state half could
        # be deleted and the refusal would silently move to the catch-all with
        # the wrong reason and the wrong rule id -- the audit log would then
        # say "not-approved" about an approval that expired.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        inside_the_window = Attempt(attempt.parameters, attempt.execution_token,
                                    NOW)
        verdict = decide(replace(approval, state="expired"), inside_the_window)
        self.assertFalse(verdict.allowed, "an expired approval executed")
        self.assertEqual("expired", verdict.reason)
        self.assertEqual("R3", verdict.rule)

    def test_every_documented_state_gets_the_verdict_the_rules_state(self):
        # The state vocabulary is closed, so the verdicts are too: a state
        # added to STATES without a decision here fails this test rather than
        # inheriting whatever branch it happens to fall through to.
        expected = {
            "pending": (False, "not-approved", "R1"),
            "approved": (True, "executed", ""),
            "denied": (False, "not-approved", "R1"),
            "expired": (False, "expired", "R3"),
            "revoked": (False, "revoked", "R4"),
            "superseded": (False, "superseded", "R1"),
            "consumed": (False, "replay", "R5"),
        }
        self.assertEqual(set(STATES), set(expected))
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        allowed_states = [state for state, (ok, _r, _id) in expected.items()
                          if ok]
        self.assertEqual([EXECUTABLE_STATE], allowed_states,
                         "more than one state executes")
        for state, (ok, reason, rule) in expected.items():
            with self.subTest(state=state):
                verdict = decide(replace(approval, state=state), attempt)
                self.assertEqual(ok, verdict.allowed,
                                 "%s: %s" % (state, verdict.reason))
                self.assertEqual(reason, verdict.reason)
                self.assertEqual(rule, verdict.rule)

    def test_a_recorded_completion_is_a_replay_even_if_the_state_did_not_move(
            self):
        # R5 has two independent halves and NAC-5 sets both at once, so either
        # could be deleted with every test still green. This is the half the
        # module docstring's declared limit leans on: a caller that persists
        # the attempt's outcome but not the move to consumed still has replay
        # protection. On the reverted tree a completed send ran twice.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        self.assertEqual(EXECUTABLE_STATE, approval.state)
        replayed = Attempt(attempt.parameters, attempt.execution_token,
                           attempt.at, prior_outcome="done")
        verdict = decide(approval, replayed)
        self.assertFalse(verdict.allowed,
                         "a completed action ran a second time")
        self.assertEqual("replay", verdict.reason)
        self.assertEqual("R5", verdict.rule)

    def test_authority_scope_binds_the_action_not_only_its_ceilings(self):
        # NAC-2 moves the max_amount ceiling, so the branch that binds the
        # approver's authority to the action ITSELF had no fixture: on the
        # reverted tree an approval for a transfer executed against a scope
        # that only ever authorised a send. The approval is rebound to the
        # edited parameters first, so R1 cannot be what refuses it.
        approval, _attempt, _allowed, _reason = POSITIVE["clean"]
        for key, value in (("action", "transfer"), ("recipient", "acct-0001")):
            with self.subTest(parameter=key):
                parameters = dict(PARAMS, **{key: value})
                bound = replace(approval, action_revision=revision(parameters))
                verdict = decide(bound, Attempt(parameters, "tok-1", NOW))
                if key in approval.authority_scope:
                    self.assertFalse(verdict.allowed,
                                     "%s=%r executed outside the scope"
                                     % (key, value))
                    self.assertEqual("out-of-scope", verdict.reason)
                    self.assertEqual("R2", verdict.rule)
                else:
                    # The control: a parameter the scope says nothing about is
                    # not what R2 is for, so this one must still execute.
                    self.assertTrue(verdict.allowed,
                                    "%s=%r was refused as %s"
                                    % (key, value, verdict.reason))

    def test_an_unrecognised_approval_state_is_rejected(self):
        # The mirror of the prior-outcome check. Review found it uncovered and
        # called it cosmetic because every typo it tried failed closed, which
        # is true of the branch order as it stands today and is not a property
        # anything was holding in place. A state of "Revoked" is a revocation
        # that silently reads as not-approved; it should not construct at all.
        approval, _attempt, _allowed, _reason = POSITIVE["clean"]
        for bad in ("Revoked", "Approved", "consumedd", "", "approved ",
                    "REVOKED"):
            with self.subTest(state=bad):
                with self.assertRaises(ValueError):
                    replace(approval, state=bad)
        for good in STATES:
            with self.subTest(state=good):
                self.assertEqual(good, replace(approval, state=good).state)

    def test_the_action_revision_ignores_key_order_but_not_values(self):
        # The binding in R1 is a hash of the parameters, and the sort is what
        # makes it a hash of the parameters rather than of one serialisation of
        # them. Without the sort the same approved payload, rebuilt in another
        # order by any caller that round-trips it, is refused as superseded --
        # the failure that teaches a team to stop trusting the gate.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        reordered = {key: PARAMS[key] for key in reversed(list(PARAMS))}
        self.assertEqual(list(reversed(list(PARAMS))), list(reordered))
        self.assertEqual(revision(PARAMS), revision(reordered))
        verdict = decide(approval, Attempt(reordered, attempt.execution_token,
                                           attempt.at))
        self.assertTrue(verdict.allowed,
                        "the same payload in another key order was refused "
                        "as %s" % verdict.reason)
        edited = dict(PARAMS, amount=121)
        self.assertNotEqual(revision(PARAMS), revision(edited))
        verdict = decide(approval, Attempt(edited, attempt.execution_token,
                                           attempt.at))
        self.assertFalse(verdict.allowed, "an edited amount executed")
        self.assertEqual("superseded", verdict.reason)
        self.assertEqual("R1", verdict.rule)

    def test_the_term_and_outcome_inventories_are_the_ones_named_here(self):
        # The sweeps below are driven by RULE_TERMS and OUTCOMES, so a term or
        # an outcome deleted from the tool would simply stop being swept: an
        # inventory that certifies itself certifies nothing. Both are written
        # out here as well, so narrowing either one fails a test rather than
        # quietly narrowing the check.
        refuses = r"refus|never|must not|is not|does not|denied"
        self.assertEqual({
            "R1": (r"supersed", r"revision"),
            "R2": (r"executor", r"approver"),
            "R3": (r"expir", refuses),
            "R4": (r"revok", refuses),
            "R5": (r"second", refuses),
            "R6": (r"idempotency", r"retry", refuses),
        }, dict(RULE_TERMS))
        self.assertEqual((None, "done", "refused", "unknown"), tuple(OUTCOMES))

    def test_each_rule_term_is_load_bearing_on_its_own(self):
        # RULE_TERMS is the part of the check that reads what a rule still
        # says, and a term nothing exercises is decoration. Each term is
        # removed from the shipped sentence one at a time, in both documents,
        # leaving the heading and the rule's other terms in place: the check
        # has to name that term. Driven by RULE_TERMS, so a term added later
        # is swept with the rest.
        import re as _re                      # local: the module needs no more
        self.assertEqual({rule_id for rule_id, _n, _r, _c in RULES},
                         set(RULE_TERMS))
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in (TEMPLATE, EXAMPLE):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                for rule_id, name, _reason, _criterion in RULES:
                    heading = "**%s %s.**" % (rule_id, name)
                    for term in RULE_TERMS[rule_id]:
                        label = TERM_NAMES.get(term, repr(term))
                        with self.subTest(document=relative, rule=rule_id,
                                          term=label):
                            stripped = []
                            for line in text.splitlines(True):
                                if heading in line:
                                    head, sentence = line.split(heading, 1)
                                    sentence = _re.sub(term, "", sentence,
                                                       flags=_re.I)
                                    line = head + heading + sentence
                                stripped.append(line)
                            self.assertNotEqual(text, "".join(stripped),
                                                "%s %s was not in the sentence"
                                                % (rule_id, label))
                            path.write_text("".join(stripped),
                                            encoding="utf-8")
                            issues = check_approvals(root)
                            path.write_text(text, encoding="utf-8")
                            self.assertTrue(
                                any("rule %s (%s) no longer says" %
                                    (rule_id, name) in issue and label in issue
                                    and relative in issue for issue in issues),
                                issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    # --- a row somewhere else in the document is not that row ---------------
    # Structural matching on the whole file says only that the string exists
    # somewhere. Review showed that as a decoy row; the same hole is open to
    # anyone who moves a table instead of copying one, so each lookup is now
    # scoped to the section that owns it and these are what hold that.

    def test_a_row_outside_its_own_section_does_not_count(self):
        # Every rule, criterion and record field, in both documents, moved out
        # of its section to the end of the file. Nothing is deleted: the string
        # is still in the document, and the document is still wrong.
        moves = []
        for rule_id, name, _reason, criterion in RULES:
            moves.append(("**%s %s.**" % (rule_id, name), "rule %s" % rule_id))
            moves.append(("| %s |" % criterion,
                          "negative criterion %s" % criterion))
        for field_name in RECORD_FIELDS:
            moves.append(("| %s |" % field_name, "%r is not stated"
                          % field_name))
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in (TEMPLATE, EXAMPLE):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                for marker, expected in moves:
                    with self.subTest(document=relative, marker=marker):
                        lines = text.splitlines(True)
                        row = [line for line in lines if marker in line]
                        self.assertEqual(1, len(row), marker)
                        moved = [line for line in lines if marker not in line]
                        path.write_text("".join(moved) + "\n" + row[0],
                                        encoding="utf-8")
                        issues = check_approvals(root)
                        path.write_text(text, encoding="utf-8")
                        self.assertTrue(
                            any(expected in issue and relative in issue
                                for issue in issues),
                            "%s moved out of its section was not caught: %r"
                            % (marker, issues))
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_a_state_row_outside_section_four_is_not_the_state_row(self):
        # The row moved out of the record is not the record's row, and the
        # answer is that the record has no State row -- not that the vocabulary
        # was found somewhere else in the document.
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / TEMPLATE
            text = path.read_text(encoding="utf-8")
            rows = [line for line in text.splitlines(True)
                    if line.startswith("| State |")]
            self.assertEqual(1, len(rows))
            moved = [line for line in text.splitlines(True)
                     if not line.startswith("| State |")]
            path.write_text("".join(moved) + "\n" + rows[0], encoding="utf-8")
            issues = check_approvals(root)
            path.write_text(text, encoding="utf-8")
            self.assertTrue(any("the approval record has no State row" in issue
                                for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_a_missing_numbered_section_is_reported(self):
        # The scoping has to fail closed. A document that dropped the number
        # from a heading has no section 4, 5 or 6 to look in, and the answer to
        # that is a finding, not a search of the rest of the file.
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for relative in (TEMPLATE, EXAMPLE):
                path = root / relative
                text = path.read_text(encoding="utf-8")
                for number in (4, 5, 6):
                    with self.subTest(document=relative, section=number):
                        heading = [line for line in text.splitlines(True)
                                   if line.startswith("## %d." % number)]
                        self.assertEqual(1, len(heading))
                        unnumbered = heading[0].replace("## %d." % number,
                                                        "##", 1)
                        path.write_text(text.replace(heading[0], unnumbered, 1),
                                        encoding="utf-8")
                        issues = check_approvals(root)
                        path.write_text(text, encoding="utf-8")
                        self.assertTrue(
                            any("section %d is not there" % number in issue
                                and relative in issue for issue in issues),
                            issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_a_decoy_state_row_does_not_cover_a_gutted_one(self):
        # The vocabulary lookup used to take the first State row it found, so
        # a full decoy row above a gutted real one passed. Every State row in
        # section 4 has to carry the vocabulary now.
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            path = root / TEMPLATE
            text = path.read_text(encoding="utf-8")
            rows = [line for line in text.splitlines(True)
                    if line.startswith("| State |")]
            self.assertEqual(1, len(rows))
            for state in STATES:
                with self.subTest(state=state):
                    gutted = rows[0].replace(state, "", 1)
                    self.assertNotEqual(rows[0], gutted)
                    path.write_text(text.replace(rows[0], rows[0] + gutted, 1),
                                    encoding="utf-8")
                    issues = check_approvals(root)
                    path.write_text(text, encoding="utf-8")
                    self.assertTrue(any("%r is not in the State row" % state
                                        in issue for issue in issues), issues)
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_a_second_filled_copy_is_checked_too(self):
        # The next document kind: not this example, the one the second product
        # writes. A checker that names one file would never look at it, so the
        # examples are discovered rather than listed -- and the named example
        # stays required, so discovering others is not a way to lose it.
        second = "examples/northwind-human-approval-gates.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            good = (root / EXAMPLE).read_text(encoding="utf-8")
            (root / second).write_text(good, encoding="utf-8")
            self.assertEqual([], check_approvals(root),
                             "a compliant second copy was reported")
            for rule_id, name, _reason, criterion in RULES:
                with self.subTest(rule=rule_id):
                    heading = "**%s %s.**" % (rule_id, name)
                    kept = [line for line in good.splitlines(True)
                            if heading not in line]
                    (root / second).write_text("".join(kept), encoding="utf-8")
                    issues = check_approvals(root)
                    self.assertTrue(any("rule %s" % rule_id in issue
                                        and second in issue
                                        for issue in issues), issues)
            (root / second).write_text(good, encoding="utf-8")
            kept = (root / EXAMPLE)
            (root / EXAMPLE).unlink()
            self.assertIn("%s: missing" % EXAMPLE, check_approvals(root),
                          "the named example stopped being required")
            kept.write_text(good, encoding="utf-8")
            (root / second).unlink()
            self.assertEqual([], check_approvals(root),
                             "the copy was not restored")

    def test_an_unknown_outcome_outranks_every_other_refusal(self):
        # The order in decide() is a decision, not an accident: an attempt
        # whose outcome nobody established is not a fresh start, so it is
        # reported as unreconciled whatever else is wrong with the approval.
        # Reported as replay or revoked instead, a caller that treats those as
        # a duplicate no-op would retry a send that may already have landed.
        approval, attempt, _allowed, _reason = POSITIVE["clean"]
        for state in ("consumed", "revoked", "superseded", "expired"):
            with self.subTest(state=state):
                verdict = decide(replace(approval, state=state),
                                 Attempt(attempt.parameters,
                                         attempt.execution_token, attempt.at,
                                         prior_outcome="unknown"))
                self.assertFalse(verdict.allowed)
                self.assertEqual("unreconciled", verdict.reason)
                self.assertEqual("R6", verdict.rule)
class PricingContractGateTests(unittest.TestCase):
    """F16: the pricing blank decided a number and nothing about changing it.

    It had a value metric, tiers, a benchmark and discount rules, and no trial,
    overage, grandfathering, upgrade, downgrade, proration, refund or migration
    terms, no per-tier evidence or cost floor, and nowhere to say who moves when
    a price changes. Both pricing worksheets meanwhile told their reader to put
    the range in "the evidence column" of section 3, a column section 3 did not
    have. Each test below removes one part of the contract from a copy of the
    tree and asserts the check reports it; without them a later edit could take
    any of it back out and every gate in this repository would still pass.

    What these do not check: whether the fields are filled well. A change record
    whose cells all read "TBD" passes here, and Gate 5's signers are the ones who
    catch that. Nor do they check the example beyond its change record: the blank
    is what carries the requirement, and the example is read only for the thing
    the finding asked an example to prove.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = copy_tree(self.tmp.name)
        self.template = self.root / PRICING_TEMPLATE
        self.example = self.root / PRICING_EXAMPLE

    def edit(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, "the text this test mutates is no longer there")
        path.write_text(text.replace(old, new), encoding="utf-8")

    def codes(self):
        return [issue.message for issue in check_pricing_contract(self.root)]

    def test_the_tree_as_it_stands_carries_the_whole_contract(self):
        self.assertEqual(self.codes(), [])

    def test_a_tree_without_the_pricing_blank_makes_no_claim(self):
        self.template.unlink()
        self.assertEqual(check_pricing_contract(self.root), [])

    def test_dropping_the_evidence_column_the_worksheets_feed_is_reported(self):
        self.edit(self.template, " | %s |" % PRICING_EVIDENCE_COLUMN, " |")
        self.assertTrue(any(PRICING_EVIDENCE_COLUMN in message
                            for message in self.codes()))

    def test_renaming_the_column_in_a_worksheet_alone_is_reported(self):
        sheet = self.root / "frameworks" / "pricing" / "van-westendorp.md"
        self.edit(sheet, "%s column" % PRICING_EVIDENCE_COLUMN, "evidence column")
        self.assertTrue(any("no longer names" in message for message in self.codes()))

    def test_an_evidence_column_named_only_inside_a_comment_does_not_count(self):
        self.edit(self.template, "| %s |" % PRICING_EVIDENCE_COLUMN,
                  "|\n<!-- %s -->" % PRICING_EVIDENCE_COLUMN)
        self.assertTrue(any(PRICING_EVIDENCE_COLUMN in message
                            for message in self.codes()))

    def test_losing_a_standing_term_is_reported_by_name(self):
        self.edit(self.template, "| Grandfathering (an existing customer keeps an old price)",
                  "| Legacy pricing")
        self.assertIn("section 7 no longer asks for the Grandfathering term", self.codes())

    def test_losing_the_standing_terms_section_is_reported(self):
        self.edit(self.template, "## 7. Standing commercial terms", "## 7. Terms")
        self.assertTrue(any("Standing commercial terms" in message
                            for message in self.codes()))

    def test_dropping_the_migration_route_is_reported(self):
        self.edit(self.template, "[migration cutover plan](../delivery/migration-cutover-plan.md)",
                  "ask someone")
        self.assertTrue(any("migration-cutover-plan.md" in message
                            for message in self.codes()))

    def test_a_route_to_a_document_not_in_the_tree_is_reported(self):
        (self.root / "templates" / "delivery" / "support-runbook.md").unlink()
        self.assertTrue(any("which is not in this tree" in message
                            for message in self.codes()))

    def test_the_blank_losing_the_notice_and_the_reversal_is_reported(self):
        self.edit(self.template,
                  "| Notice: date and channel | Effective date "
                  "| Reversal: what undoes it, who decides, and by when ",
                  "| Effective date ")
        reported = " ".join(self.codes())
        self.assertIn("'Notice'", reported)
        self.assertIn("'Reversal'", reported)

    def test_the_filled_example_losing_the_reversal_is_reported(self):
        self.edit(self.example,
                  "| Reversal: what undoes it, who decides, and by when ", "| ")
        self.assertTrue(any("'Reversal'" in message for message in self.codes()))

    def test_the_example_is_read_as_well_as_the_blank(self):
        self.edit(self.example, "## 8. The change record", "## 8. What changed")
        self.assertEqual(self.codes(), [],
                         "an example with no change record section is not read; the "
                         "blank is what carries the requirement")
        self.edit(self.example, "## 8. What changed", "## 8. The change record")
        self.edit(self.example, "| Cohort |", "| Who |")
        self.assertTrue(any(issue.path == PRICING_EXAMPLE
                            for issue in check_pricing_contract(self.root)))

    def test_losing_the_per_tier_economic_floor_is_reported(self):
        """The same defect one heading over: unit economics feeds section 3a."""
        self.edit(self.template, PRICING_FLOOR_SECTION, "### 3a. Costs")
        self.assertTrue(any("per-tier economic floor" in message
                            for message in self.codes()))

    def test_the_floor_worksheet_dropping_the_section_it_feeds_is_reported(self):
        sheet = self.root / PRICING_FLOOR_SOURCE
        self.edit(sheet, "section 3a", "the tier table")
        self.assertTrue(any("no longer names the section it feeds" in message
                            for message in self.codes()))

    def test_the_whole_docs_contract_reports_it_too(self):
        self.edit(self.template, "| Proration (part-period charges when something changes mid-cycle)",
                  "| Part periods")
        self.assertTrue(any(issue.code == "pricing-contract"
                            for issue in check_docs(self.root)))


if __name__ == "__main__":
    unittest.main()
