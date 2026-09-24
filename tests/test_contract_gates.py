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


# --------------------------------------------------------------------------
# F09: the PRD's own lineage and change-impact contract.
# --------------------------------------------------------------------------

PRD = REPO / "templates" / "definition" / "prd.md"

# The trace the audit's closure proof names, hop by hop: objective, the evidence
# it stands on, the capability that serves it, the story, the acceptance
# criterion, the test, and the release decision that criterion gates. Each entry
# is one of the PRD's tables and the columns that carry those hops, written out
# here rather than read off the template, so a renamed or dropped column fails
# instead of quietly shrinking what this test walks.
TRACE_COLUMNS = {
    "objectives": ("Evidence", "Metric ID"),
    "stories": ("Acceptance criteria ID", "Verified by (test ID, filled at BUILD)"),
    "scope": ("Objective it serves", "Story it serves", "Release slice"),
    "slices": ("Capabilities", "Depends on", "Dependency register ID"),
    "launch": ("Covers (slice or objective)", "Verified by (artifact or test ID)"),
    "companions": ("Applies (Yes / No)", "Why"),
    "signoff": ("Revision signed",),
    "changes": ("What changed (rows by ID)", "CR", "Approvals re-taken",
                "Approvals unaffected"),
}
# The cell that identifies each of those tables, so a table is found by what it
# is rather than by where it sits: sections move, headers do not.
TABLE_KEYS = {
    "objectives": "Objective",
    "stories": "Story",
    "scope": "Capability",
    "slices": "Slice",
    "launch": "Criterion",
    "companions": "Open this",
    "signoff": "Role",
    "changes": "Version",
}

# One filled PRD, ILLUSTRATIVE throughout and invented for this test. Values are
# keyed by column name, never by position, so the fixture is rendered through
# whatever header the shipped template carries: a column the template drops is a
# hop this fixture can no longer supply, which is the failure this test is for.
FIXTURE = {
    "objectives": [
        {"#": "O1", "Objective": "Field reps submit an expense report without retyping it",
         "Evidence": "E7", "Metric": "median submission time", "Metric ID": "M-004",
         "Baseline": "14 min", "Target": "7 min", "Metric owner": "Priya Nair",
         "Measured where": "report_submitted event"}],
    "stories": [
        {"#": "US1", "Story": "As a field rep, I want the receipt read for me, so that I do not retype it.",
         "Persona": "field rep", "Priority (must / should / later)": "must",
         "Acceptance criteria ID": "AC-1",
         "Verified by (test ID, filled at BUILD)": "TC-101"}],
    "scope": [
        {"#": "F1", "Capability": "Receipt extraction",
         "What it does, in one sentence": "Reads amount, date and merchant from a photographed receipt.",
         "Objective it serves": "O1", "Story it serves": "US1",
         "Release slice": "S1", "Detail": "FR-001"}],
    "slices": [
        {"Slice": "S1", "What it delivers": "Extraction behind a pilot flag",
         "Capabilities": "F1", "Depends on": "none",
         "Dependency register ID": "n/a", "Planned release": "Now row 1"}],
    "launch": [
        {"#": "L1", "Criterion": "All \"must\" stories pass their acceptance criteria",
         "Covers (slice or objective)": "S1",
         "Verified by (artifact or test ID)": "TC-101", "Owner": "Maya Chen"}],
    "companions": [
        {"Trigger, if this is true of your product": "It processes personal data",
         "Open this": "privacy-impact-assessment.md", "Stage": "DESIGN",
         "Applies (Yes / No)": "Yes", "Why": "Receipts carry names and card tails"},
        {"Trigger, if this is true of your product": "It touches what customers pay for",
         "Open this": "pricing-packaging.md", "Stage": "PLANNING",
         "Applies (Yes / No)": "No", "Why": "No tier or price changes in this slice"}],
    "signoff": [
        {"Role": "Product owner", "Name": "Maya Chen", "Date": "2026-04-02",
         "Revision signed": "v1.1", "What they are signing": "Scope"},
        {"Role": "Engineering lead", "Name": "Daniel Okafor", "Date": "2026-03-10",
         "Revision signed": "v1.0", "What they are signing": "Feasibility"}],
    "changes": [
        {"Version": "v1.1", "Date": "2026-04-02",
         "What changed (rows by ID)": "O1, AC-1", "CR": "CR-4",
         "Approvals re-taken": "Product owner",
         "Approvals unaffected": "Engineering lead: no build change"}],
}
FIXTURE_BASELINE = "v1.0"


def md_tables(text):
    """Every markdown table in a document, as a list of (headers, rows-of-dicts)."""
    found, lines = [], text.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("|") or i + 1 >= len(lines):
            continue
        if not re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lines[i + 1].strip()):
            continue
        headers = [c.strip() for c in line.strip().strip("|").split("|")]
        rows = []
        for body in lines[i + 2:]:
            if not body.startswith("|"):
                break
            cells = [c.strip() for c in body.strip().strip("|").split("|")]
            rows.append(dict(zip(headers, cells)))
        found.append((headers, rows))
    return found


def prd_table(text, key):
    """The one table in a document whose header carries TABLE_KEYS[key]."""
    wanted = TABLE_KEYS[key]
    hits = [t for t in md_tables(text) if wanted in t[0]]
    return hits[0] if len(hits) == 1 else None


def render_fixture(template_text, fixture=None, baseline=FIXTURE_BASELINE):
    """The fixture, written out through the shipped template's own headers.

    Cells the fixture does not name are rendered empty, so a template that grows
    a column stays renderable; a template that drops one loses the value the
    trace below needs, which is the point.
    """
    fixture = FIXTURE if fixture is None else fixture
    out = ["# Trace fixture (ILLUSTRATIVE, invented for this test)",
           "", "**Baseline:** %s" % baseline, ""]
    for key in TABLE_KEYS:
        headers = prd_table(template_text, key)[0]
        out.append("| " + " | ".join(headers) + " |")
        out.append("|" + "---|" * len(headers))
        for row in fixture[key]:
            out.append("| " + " | ".join(row.get(h, "") for h in headers) + " |")
        out.append("")
    return "\n".join(out)


def resolve_trace(filled):
    """Walk O1 to the release decision, returning the hops that resolved.

    Every hop reads a cell by column name and looks the value up in the table it
    points at. A missing column, an empty cell or an id that names no row stops
    the walk, and the caller sees how far it got.
    """
    hops, cell = [], lambda row, name: (row or {}).get(name, "").strip()
    tables = {key: prd_table(filled, key) for key in TABLE_KEYS}
    if any(t is None for t in tables.values()):
        return hops
    find = lambda key, col, value: next(
        (r for r in tables[key][1] if cell(r, col) == value), None)

    objective = find("objectives", "#", "O1")
    for column, label in (("Evidence", "evidence"), ("Metric ID", "metric")):
        if not cell(objective, column):
            return hops
        hops.append("O1 -> %s %s" % (label, cell(objective, column)))

    capability = next((r for r in tables["scope"][1]
                       if cell(r, "Objective it serves") == "O1"), None)
    if not capability:
        return hops
    hops.append("O1 -> %s" % cell(capability, "#"))

    story = find("stories", "#", cell(capability, "Story it serves"))
    if not story:
        return hops
    hops.append("%s -> %s" % (cell(capability, "#"), cell(story, "#")))

    criterion = cell(story, "Acceptance criteria ID")
    test = cell(story, "Verified by (test ID, filled at BUILD)")
    if not criterion or not test:
        return hops
    hops.append("%s -> %s" % (cell(story, "#"), criterion))
    hops.append("%s -> %s" % (criterion, test))

    slice_row = find("slices", "Slice", cell(capability, "Release slice"))
    if not slice_row or not cell(slice_row, "Depends on"):
        return hops
    hops.append("%s -> %s" % (cell(capability, "#"), cell(slice_row, "Slice")))

    decision = next((r for r in tables["launch"][1]
                     if cell(r, "Covers (slice or objective)") == cell(slice_row, "Slice")
                     and cell(r, "Verified by (artifact or test ID)") == test), None)
    if not decision:
        return hops
    hops.append("%s -> %s" % (test, cell(decision, "#")))
    return hops


FULL_TRACE = ["O1 -> evidence E7", "O1 -> metric M-004", "O1 -> F1", "F1 -> US1",
              "US1 -> AC-1", "AC-1 -> TC-101", "F1 -> S1", "TC-101 -> L1"]


class PrdLineageTraceTests(unittest.TestCase):
    """F09: the PRD carries the lineage and the change impact itself.

    The audit's closure proof is a reviewer tracing O1 to the release decision
    without guessing, and a change naming the approvals it affects. Both are
    checked here against one filled fixture rendered through the shipped
    template's own headers, so the trace cannot pass on a template that no
    longer asks for the columns it walks.

    Named limits, three. The cited IDs are not resolved into the documents that
    define them: E7 is not looked up in ../discovery/evidence-note.md, M-004 not
    in ../operate/metrics-dictionary.md, TC-101 not in the frd.md matrix, so this
    proves the chain is expressible and internally consistent, not that its far
    ends exist. Nothing here reads a real product's PRD. And no gate rejects a
    filled PRD that leaves the new cells blank; on the default path the exit-gate
    checklist and the humans who sign Gate 2 are what enforce them, exactly as
    with every other field in this template.
    """

    @classmethod
    def setUpClass(cls):
        cls.template = PRD.read_text(encoding="utf-8")

    def test_the_template_asks_for_every_column_the_trace_walks(self):
        for key, columns in TRACE_COLUMNS.items():
            table = prd_table(self.template, key)
            self.assertIsNotNone(table, "no single %s table in the PRD template" % key)
            for column in columns:
                with self.subTest(table=key, column=column):
                    self.assertIn(column, table[0])

    def test_the_template_names_a_baseline_and_a_change_reference(self):
        for phrase in ("**Baseline:**", "**Changes since baseline:**",
                       "change-request.md"):
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase in self.template,
                                "the PRD template does not name %s" % phrase)

    def test_the_filled_fixture_resolves_every_hop_to_the_release_decision(self):
        self.assertEqual(FULL_TRACE, resolve_trace(render_fixture(self.template)))

    def test_a_broken_hop_stops_the_walk_rather_than_passing(self):
        """The walk has teeth: emptying one cell truncates the trace."""
        for key, column, stops_after in (("objectives", "Evidence", 0),
                                         ("scope", "Objective it serves", 2),
                                         ("stories", "Verified by (test ID, filled at BUILD)", 4),
                                         ("slices", "Depends on", 6)):
            with self.subTest(column=column):
                broken = {k: [dict(r) for r in rows] for k, rows in FIXTURE.items()}
                broken[key][0][column] = ""
                hops = resolve_trace(render_fixture(self.template, broken))
                self.assertEqual(FULL_TRACE[:stops_after], hops)

    def test_a_change_names_the_approvals_it_re_took_and_the_ones_it_did_not(self):
        filled = render_fixture(self.template)
        roles = {r["Role"] for r in prd_table(filled, "signoff")[1]}
        ids = ({r["#"] for r in prd_table(filled, "objectives")[1]}
               | {r["Acceptance criteria ID"] for r in prd_table(filled, "stories")[1]})
        for change in prd_table(filled, "changes")[1]:
            with self.subTest(version=change["Version"]):
                self.assertTrue(change["CR"].startswith("CR-"), change["CR"])
                changed = {v.strip() for v in change["What changed (rows by ID)"].split(",")}
                self.assertTrue(changed <= ids, "change names rows this PRD has not: %s"
                                % sorted(changed - ids))
                retaken = {v.strip() for v in change["Approvals re-taken"].split(",")}
                unaffected = {v.split(":")[0].strip()
                              for v in change["Approvals unaffected"].split(",")}
                self.assertTrue(retaken <= roles, sorted(retaken - roles))
                self.assertEqual(roles, retaken | unaffected,
                                 "every signer is either re-taken or explained")
                for role in unaffected:
                    self.assertIn(":", change["Approvals unaffected"],
                                  "%s is unaffected with no reason" % role)

    def test_a_signature_older_than_a_change_names_the_older_revision(self):
        """The revision column is what stops a signature outliving its bytes."""
        filled = render_fixture(self.template)
        signed = {r["Role"]: r["Revision signed"] for r in prd_table(filled, "signoff")[1]}
        change = prd_table(filled, "changes")[1][0]
        retaken = {v.strip() for v in change["Approvals re-taken"].split(",")}
        for role, revision in signed.items():
            with self.subTest(role=role):
                self.assertEqual(revision == change["Version"], role in retaken)
        self.assertIn(FIXTURE_BASELINE, set(signed.values()))

    def test_every_companion_row_is_answered_yes_or_no_with_a_reason(self):
        for row in prd_table(render_fixture(self.template), "companions")[1]:
            with self.subTest(trigger=row["Open this"]):
                self.assertIn(row["Applies (Yes / No)"], ("Yes", "No"))
                self.assertTrue(row["Why"])

    def test_the_shipped_companion_table_leaves_both_cells_for_the_filler(self):
        """Blank in the template, mandatory in the exit gate: the template must
        not answer the applicability question on the reader's behalf."""
        headers, rows = prd_table(self.template, "companions")
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(trigger=row["Open this"]):
                self.assertEqual("", row["Applies (Yes / No)"])
                self.assertEqual("", row["Why"])

    def test_the_exit_gate_checks_each_new_contract(self):
        gate = self.template.split("## Exit gate")[-1]
        for phrase in ("evidence ID and a metric-dictionary ID",
                       "an objective, and a release slice",
                       "names its dependencies",
                       "names what it covers and what verifies it",
                       "answered Yes or No with a reason",
                       "the revision each signed",
                       "the approvals it re-took"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, gate)


if __name__ == "__main__":
    unittest.main()
