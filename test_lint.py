#!/usr/bin/env python3
"""Tests for the PRD review gate. Run: python3 -m unittest test_lint.py -v"""
import datetime as dt
import tempfile
import unittest
from pathlib import Path

import lint

REPO = Path(__file__).resolve().parent

# The banned metric strings and the em dash are assembled from fragments rather
# than written out: this repository must not contain them as literals anywhere,
# including in the tests for the checker that detects them.
BANNED_MONEY = "$" + "14" + "M"
BANNED_UPTIME = "99." + "95"
EM_DASH = chr(0x2014)

# Computed rather than written down, because a stale as-of date now fails the
# gate and a hard-coded date would turn these tests red on a future Tuesday.
FRESH_AS_OF = (dt.date.today() - dt.timedelta(days=5)).isoformat()
STALE_AS_OF = (dt.date.today()
               - dt.timedelta(days=lint.STALE_AFTER_DAYS + 5)).isoformat()

COST = "- Cost per call target: 0.04 USD"
THRESHOLD = "99.0 percent (ILLUSTRATIVE)"

# A lint fixture, not a model PRD. Only sections 0 and 1 are fill-checked,
# so the other sections carry headings and little else.
MINIMAL = """# PRD: Test feature
**Regulatory references verified as of:** """ + FRESH_AS_OF + """
## 0. Regulated overlay
### 0.1 Regulatory precondition register
| Market | License condition | Regulator | Confirmed how | Confirmed date | Owner |
|---|---|---|---|---|---|
| UAE | No change to licensed activity | CBUAE | Memo REG-1 | 2026-01-02 | Reg Lead |
### 0.2 Scheme-rule constraints
| Rule area touched | Reference | Version pinned at spec time | Who watches for drift |
|---|---|---|---|
| Disputes | Register SR-1 | Edition recorded in SR-1 | Rules Analyst |
### 0.3 Data residency and model-vendor terms
- Data classes in the flow: case text, stored and processed in region
### 0.4 Financial-crime touchpoints
- Screening points in the flow: at intake, which locks the case to financial crime
### 0.5 Customer-communication conduct
- Regulated communication in any market: no, the output is internal only
### 0.6 The metric that survives an audit
- Headline success metric: median analyst handling time per case
## 1. Acceptance criteria
| # | Requirement | Metric | Eval set or dataset | Pass threshold | Below | Failing-case owner |
|---|---|---|---|---|---|---|
| 1 | Amount extracted | Exact-match accuracy | DS-A: 400 cases | """ + THRESHOLD + """ | Block | Ops Lead |
## 2. Edge cases
### MUST REFUSE
- Non-card dispute: no draft, banner shown
### MUST ESCALATE
- Screening signal: routes to the Financial Crime duty officer
### MUST NEVER INVENT
- monetary amounts: emit UNKNOWN
## 3. Non-determinism clause
- Acceptable variation: wording and sentence order
## 4. Guardrails
- Kill switch: manual, flag off in 5 minutes, owned by the Eng Manager
## 5. Operations page
""" + COST + """
## 6. Review gate
- [x] Section 0 complete for every in-scope market
## 7. GAPS
- 1 No Arabic eval set: medium blast radius, Product Lead, 2026-03-01
"""


def run(text, template_mode=False, stale_fatal=True):
    """Lint a string; return (set of failure codes, joined failure messages)."""
    return _lint(text, template_mode, stale_fatal)[0]


def _lint(text, template_mode=False, stale_fatal=True):
    """Lint a string; return ((codes, messages), (notice codes, notices))."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "prd.md"
        path.write_text(text, encoding="utf-8")
        problems, notices = lint.check(path, template_mode=template_mode,
                                       stale_fatal=stale_fatal)
    pair = lambda found: ({c for _, c, _ in found},  # noqa: E731
                          " ".join(m for _, _, m in found))
    return pair(problems), pair(notices)


class ReviewGateTests(unittest.TestCase):

    def test_a_complete_prd_passes(self):
        codes, messages = run(MINIMAL)
        self.assertEqual(set(), codes, messages)

    def test_missing_required_section_is_flagged(self):
        codes, messages = run(MINIMAL.replace("## 3. Non-determinism clause",
                                             "## 3b. Notes on variation"))
        self.assertIn("SECTION", codes)
        self.assertIn("Non-determinism", messages)

    def test_unanswered_overlay_fields_are_flagged(self):
        codes, messages = run(MINIMAL.replace("Memo REG-1", "")
                              .replace("Reg Lead", "[name]")
                              .replace("Edition recorded in SR-1", "N/A"))
        self.assertIn("OVERLAY", codes)
        self.assertIn("is blank", messages)
        self.assertIn("[placeholder]", messages)
        self.assertIn("with no reason", messages)

    def test_incomplete_eval_row_is_flagged(self):
        codes, messages = run(MINIMAL.replace("99.0 percent", "high")
                              .replace("| Block |", "|  |")
                              .replace("| Ops Lead |", "|  |"))
        self.assertIn("EVAL", codes)
        self.assertIn("has no owner", messages)
        self.assertIn("has no below-threshold action", messages)
        self.assertIn("has no number in it", messages)

    def test_an_unlabeled_threshold_is_flagged(self):
        codes, messages = run(MINIMAL.replace(THRESHOLD, "99.0 percent"))
        self.assertIn("LABEL", codes)
        self.assertIn("neither labeled ILLUSTRATIVE nor traced", messages)

    def test_a_threshold_traced_to_a_dated_agreement_is_not_flagged(self):
        agreed = "99.0 percent per memo DATA-1 dated 2026-01-19"
        codes, messages = run(MINIMAL.replace(THRESHOLD, agreed))
        self.assertNotIn("LABEL", codes)
        self.assertEqual(set(), codes, messages)

    def test_a_banned_metric_split_across_two_lines_is_caught(self):
        split = COST + "\n- Availability last quarter: 99.\n95 percent measured"
        codes, messages = run(MINIMAL.replace(COST, split))
        self.assertIn("BANNED", codes)
        self.assertIn(BANNED_UPTIME, messages)

    def test_dashes_are_caught_inside_code_fences_and_comments(self):
        fenced = "```\nrun the gate %s carefully\n```\n" % EM_DASH + COST
        self.assertIn("DASH", run(MINIMAL.replace(COST, fenced))[0])
        commented = "<!-- fill this in %s per market -->\n" % EM_DASH + COST
        self.assertIn("DASH", run(MINIMAL.replace(COST, commented))[0])

    def test_banned_metrics_and_em_dashes_are_flagged(self):
        codes, messages = run(MINIMAL.replace(COST, "%s, saving %s a year %s at %s"
                                              % (COST, BANNED_MONEY, EM_DASH,
                                                 BANNED_UPTIME)))
        self.assertIn("BANNED", codes)
        self.assertIn("DASH", codes)
        self.assertIn(BANNED_MONEY, messages)
        self.assertIn(BANNED_UPTIME, messages)

    def test_as_of_date_must_exist_and_not_be_in_the_future(self):
        missing, _ = run(MINIMAL.replace("as of:** " + FRESH_AS_OF, "date:** unknown"))
        self.assertIn("ASOF", missing)
        future, messages = run(MINIMAL.replace(FRESH_AS_OF, "2999-01-01"))
        self.assertIn("ASOF", future)
        self.assertIn("in the future", messages)

    def test_a_stale_as_of_date_fails_unless_the_escape_hatch_is_used(self):
        stale = MINIMAL.replace(FRESH_AS_OF, STALE_AS_OF)
        codes, messages = run(stale)
        self.assertIn("STALE", codes)
        self.assertIn("Re-verify every citation", messages)
        waived, notices = _lint(stale, stale_fatal=False)
        self.assertNotIn("STALE", waived[0])
        self.assertIn("STALE", notices[0])

    def test_deferred_decisions_flagged_but_not_inside_comments(self):
        codes, _ = run(MINIMAL.replace(COST, "- Cost per call target: TBD"))
        self.assertIn("TBD", codes)
        clean, _ = run(MINIMAL.replace(COST, "<!-- TODO: revisit -->\n" + COST))
        self.assertNotIn("TBD", clean)

    def test_template_mode_skips_fill_checks_but_keeps_the_rest(self):
        unfilled = MINIMAL.replace("Memo REG-1", "").replace("Reg Lead", "[name]")
        self.assertIn("OVERLAY", run(unfilled)[0])
        self.assertEqual(set(), run(unfilled, template_mode=True)[0])
        dashed = unfilled.replace("## 7. GAPS", "## 7. GAPS %s short list" % EM_DASH)
        self.assertIn("DASH", run(dashed, template_mode=True)[0])

    def test_shipped_template_and_example_pass_their_own_gate(self):
        template = (REPO / "modules" / "regulated" / "templates"
                    / "regulated-ai-prd-template.md")
        example = (REPO / "modules" / "regulated" / "examples"
                   / "dispute-summary" / "PRD.md")
        self.assertEqual([], lint.check(template, template_mode=True)[0])
        self.assertEqual([], lint.check(example)[0])
        # The template is an unfilled PRD, so the full gate must reject it.
        self.assertNotEqual([], lint.check(template)[0])


def os_run(files, pins=None):
    """Run the OS tree gate over a synthetic tree; return (codes, messages)."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, text in files.items():
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        problems = lint.os_check(root, pins={} if pins is None else pins)
    return ({code for _, _, code, _ in problems},
            " ".join(message for _, _, _, message in problems))


class OsTreeGateTests(unittest.TestCase):
    """One failing fixture per tree-mode gate, plus a clean baseline."""

    CLEAN = "A clean note that violates nothing.\n"

    def test_a_clean_tree_passes(self):
        codes, messages = os_run({"docs/note.md": self.CLEAN})
        self.assertEqual(set(), codes, messages)

    def test_character_gate_catches_a_dash(self):
        codes, _ = os_run({"docs/note.md": "left %s right\n" % EM_DASH})
        self.assertIn("DASH", codes)

    def test_metric_gate_catches_a_banned_literal(self):
        codes, messages = os_run(
            {"docs/note.md": "saving %s a year\n" % BANNED_MONEY})
        self.assertIn("BANNED", codes)
        self.assertIn(BANNED_MONEY, messages)

    def test_placeholder_gate_allows_only_angle_fields(self):
        codes, _ = os_run({"docs/note.md": "Owner: TBD\n"})
        self.assertIn("TBD", codes)
        clean, _ = os_run({"docs/note.md": "Owner: <TBD until Gate 1>\n"})
        self.assertNotIn("TBD", clean)

    def test_link_gate_catches_broken_and_absolute_links(self):
        codes, _ = os_run(
            {"docs/note.md": "[gone](missing.md) [abs](/etc/hosts)\n"})
        self.assertIn("LINK", codes)

    def test_header_gate_requires_the_three_line_block(self):
        codes, _ = os_run({"templates/thing.md": self.CLEAN})
        self.assertIn("HEADER", codes)
        headed = ("Stage: discovery, feeds Gate 1\n"
                  "Knowledge: none\nSkill: manual\n" + self.CLEAN)
        clean, messages = os_run({"templates/thing.md": headed})
        self.assertNotIn("HEADER", clean, messages)

    def test_frontmatter_gate_requires_exactly_name_and_description(self):
        bad = "---\nname: x\ndescription: Use when testing.\nextra: y\n---\n"
        codes, _ = os_run({"skills/x/SKILL.md": bad})
        self.assertIn("FRONTMATTER", codes)
        good = "---\nname: x\ndescription: Use when testing.\n---\nBody.\n"
        clean, messages = os_run({"skills/x/SKILL.md": good})
        self.assertNotIn("FRONTMATTER", clean, messages)

    def test_integrity_gate_catches_missing_and_drifted_pins(self):
        import hashlib
        expected = hashlib.sha256(b"the pinned bytes").hexdigest()
        pins = {"modules/regulated/pinned.md": expected}
        missing, _ = os_run({"docs/note.md": self.CLEAN}, pins=pins)
        self.assertIn("INTEGRITY", missing)
        drifted, _ = os_run(
            {"modules/regulated/pinned.md": "different bytes\n"}, pins=pins)
        self.assertIn("INTEGRITY", drifted)
        clean, messages = os_run(
            {"modules/regulated/pinned.md": "the pinned bytes"}, pins=pins)
        self.assertNotIn("INTEGRITY", clean, messages)

    def test_path_gate_requires_named_system_paths_to_exist(self):
        codes, _ = os_run(
            {"system/PROMPT.md": "Ask for templates/nowhere.md by path.\n"})
        self.assertIn("PATH", codes)
        clean, messages = os_run(
            {"system/PROMPT.md": "Ask for templates/real.md by path.\n",
             "templates/real.md": ("Stage: discovery, feeds Gate 1\n"
                                   "Knowledge: none\nSkill: manual\n")})
        self.assertNotIn("PATH", clean, messages)

    def test_secret_gate_catches_a_key_shaped_string(self):
        fake_key = "AKIA" + "A" * 16  # assembled so this file stays clean
        codes, messages = os_run({"docs/note.md": "key = %s\n" % fake_key})
        self.assertIn("SECRET", codes)
        self.assertIn("AWS access key", messages)

    def test_the_real_tree_passes_the_shipping_gate(self):
        self.assertEqual([], lint.os_check(REPO))


if __name__ == "__main__":
    unittest.main()


class WorkspaceExclusion(unittest.TestCase):
    """A user's filled draft in products/ must never fail the OS gate."""

    def test_user_workspace_draft_is_skipped(self):
        import lint, pathlib, shutil
        ws = pathlib.Path("products/_gate_test")
        ws.mkdir(parents=True, exist_ok=True)
        try:
            (ws / "draft.md").write_text("[broken](nowhere.md) and TBD\n")
            names = [str(p) for p in lint.tracked_files(pathlib.Path("."))]
            self.assertFalse(any("_gate_test" in n for n in names))
            self.assertTrue(any(n.endswith("learn/products/README.md") for n in names))
        finally:
            shutil.rmtree(ws)
