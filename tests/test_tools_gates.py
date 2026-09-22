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
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
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
import template_rubric  # noqa: E402
from tools.docs_contract import (check as check_docs,  # noqa: E402
                                 _example_families,
                                 check_examples_inventory, check_gate_count,
                                 check_inventory, check_readiness_claims,
                                 main as docs_contract_main, README_READINESS,
                                 READINESS_CLAIMS)
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


if __name__ == "__main__":
    unittest.main()
