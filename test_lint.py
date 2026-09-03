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
    return os_run_bytes({rel: text.encode("utf-8")
                         for rel, text in files.items()}, pins=pins)


def os_run_bytes(files, pins=None):
    """os_run, but the fixture is bytes, so a file can be invalid UTF-8."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, blob in files.items():
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
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


class WorkspaceExclusion(unittest.TestCase):
    """A user's filled draft in products/ must never fail the OS gate."""

    def test_user_workspace_draft_is_skipped(self):
        # The fixture is built in a temporary root, never under the live
        # repository. An earlier version of this test created and then removed
        # products/_gate_test in place, which deleted a real product folder of
        # that name. A gate that destroys a user's work to prove it protects it
        # is the failure this whole system exists to prevent.
        import lint, pathlib, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "products" / "_gate_test").mkdir(parents=True)
            (root / "products" / "_gate_test" / "draft.md").write_text(
                "[broken](nowhere.md) and TBD\n")
            (root / "products" / "README.md").write_text("# Workspaces\n")
            (root / "learn" / "products").mkdir(parents=True)
            (root / "learn" / "products" / "README.md").write_text("# Practice\n")
            names = [str(p) for p in lint.tracked_files(root)]
        self.assertFalse(any("_gate_test" in n for n in names))
        self.assertTrue(any(n.endswith("products/README.md") for n in names))
        self.assertTrue(
            any(n.endswith("learn/products/README.md") for n in names))


# The graph declaration, assembled from a dict so one test can vary one key.
# Passing None for a key drops it, which is how the missing-key case is built.
GRAPH_DEFAULTS = [("layer", "templates"), ("stage", "DEFINE"), ("gate", "2"),
                  ("feeds", "[]"), ("method", '""'),
                  ("aliases", '["The Thing"]')]
TEMPLATE_HEADER = "Stage: DEFINE, feeds Gate 2\nKnowledge: none\nSkill: manual\n"


def graph_fm(**over):
    """A frontmatter block carrying the six graph keys, minus any set to None."""
    pairs = [(k, over.get(k, v)) for k, v in GRAPH_DEFAULTS]
    return "---\n%s---\n" % "".join("%s: %s\n" % (k, v)
                                    for k, v in pairs if v is not None)


def header_for(stage, gate):
    """The three-line header a file with this declaration would carry.

    Built from the declaration rather than fixed, because the gate now checks
    that the two agree and a fixture that contradicts itself would be testing
    the contradiction rather than the rule under test. The contradiction has
    its own tests below, which write the header by hand.
    """
    clause = ", feeds Gate %s" % gate if str(gate).strip().isdigit() else ""
    return ("Stage: %s%s\nKnowledge: none\nSkill: manual\n"
            % (stage or "DEFINE", clause))


def template_file(**over):
    stage = over.get("stage", "DEFINE")
    gate = over.get("gate", "2")
    return (graph_fm(**over) + "# Thing\n\n"
            + header_for(stage, gate if gate is not None else ""))


class GraphDeclarationTests(unittest.TestCase):
    """Check 10. One failing fixture per rule, plus a clean baseline."""

    def test_a_complete_declaration_passes(self):
        codes, messages = os_run({"templates/thing.md": template_file()})
        self.assertEqual(set(), codes, messages)

    def test_the_template_header_is_still_found_under_the_declaration(self):
        codes, messages = os_run({"templates/thing.md": template_file()})
        self.assertNotIn("HEADER", codes, messages)

    def test_a_missing_key_is_flagged(self):
        codes, messages = os_run({"templates/thing.md": template_file(feeds=None)})
        self.assertIn("GRAPH", codes)
        self.assertIn("missing the feeds key", messages)

    def test_a_file_with_no_declaration_at_all_is_flagged(self):
        codes, messages = os_run(
            {"templates/thing.md": "# Thing\n\n" + TEMPLATE_HEADER})
        self.assertIn("GRAPH", codes)
        self.assertIn("no graph declaration", messages)

    def test_a_stage_outside_the_vocabulary_is_flagged(self):
        codes, messages = os_run(
            {"templates/thing.md": template_file(stage="REFINEMENT")})
        self.assertIn("GRAPH", codes)
        self.assertIn('stage "REFINEMENT" is not one of', messages)

    def test_every_declared_track_is_inside_the_vocabulary(self):
        for stage in ("DISCOVER", "OPERATE", "PLANNING", "AI OVERLAY",
                      "ALL STAGES"):
            codes, messages = os_run(
                {"templates/thing.md": template_file(stage=stage)})
            self.assertEqual(set(), codes, "%s: %s" % (stage, messages))

    def test_a_gate_outside_one_to_six_is_flagged(self):
        for value in ("0", "7", "two", '""'):
            codes, messages = os_run(
                {"templates/thing.md": template_file(gate=value)})
            self.assertIn("GRAPH", codes, value)
            self.assertIn("is not one of the gates", messages)

    def test_an_unresolvable_feeds_path_is_flagged(self):
        codes, messages = os_run(
            {"templates/thing.md": template_file(feeds='["templates/gone.md"]')})
        self.assertIn("GRAPH", codes)
        self.assertIn("feeds names templates/gone.md", messages)

    def test_a_feeds_path_that_resolves_is_not_flagged(self):
        codes, messages = os_run({
            "templates/thing.md": template_file(feeds='["templates/other.md"]'),
            "templates/other.md": template_file(aliases='["The Other"]'),
        })
        self.assertEqual(set(), codes, messages)

    def test_an_unresolvable_method_path_is_flagged(self):
        codes, messages = os_run(
            {"templates/thing.md": template_file(method='"knowledge/gone.md"')})
        self.assertIn("GRAPH", codes)
        self.assertIn("method names knowledge/gone.md", messages)

    def test_a_file_outside_the_six_layers_needs_no_declaration(self):
        codes, messages = os_run({"docs/note.md": "A plain note.\n"})
        self.assertEqual(set(), codes, messages)


class WikilinkTests(unittest.TestCase):
    """Check 11. Wikilinks are additive, so they resolve or they are noise."""

    def test_an_unresolvable_wikilink_is_flagged(self):
        codes, messages = os_run({"docs/note.md": "see [[nowhere/at-all.md]]\n"})
        self.assertIn("WIKILINK", codes)
        self.assertIn("nor a declared alias", messages)

    def test_a_wikilink_to_a_file_in_the_tree_resolves(self):
        codes, messages = os_run({"docs/note.md": "see [[docs/other.md]]\n",
                                  "docs/other.md": "Other.\n"})
        self.assertNotIn("WIKILINK", codes, messages)

    def test_a_wikilink_to_a_declared_alias_resolves(self):
        codes, messages = os_run({"docs/note.md": "see [[the thing]]\n",
                                  "templates/thing.md": template_file()})
        self.assertEqual(set(), codes, messages)

    def test_a_piped_or_anchored_wikilink_reads_only_the_target(self):
        codes, messages = os_run(
            {"docs/note.md": "[[docs/other.md#part|that part]]\n",
             "docs/other.md": "Other.\n"})
        self.assertNotIn("WIKILINK", codes, messages)

    def test_a_mermaid_subroutine_shape_is_not_read_as_a_wikilink(self):
        fenced = "```mermaid\nflowchart LR\n  svc --> q[[Async queue]]\n```\n"
        codes, messages = os_run({"docs/note.md": fenced})
        self.assertNotIn("WIKILINK", codes, messages)


class SkillDeclarationTests(unittest.TestCase):
    """The Task 2 decision: skills declare in a sidecar, not in frontmatter."""

    SKILL = "---\nname: x\ndescription: Use when testing.\n---\nBody.\n"
    SIDECAR = ("layer: skills\nstage: DEFINE\ngate: 2\nfeeds: []\n"
               'method: ""\naliases: ["Ex"]\n')

    def test_the_sanctioned_key_set_in_the_sidecar_passes(self):
        codes, messages = os_run({"skills/x/SKILL.md": self.SKILL,
                                  "skills/x/SKILL.graph.yml": self.SIDECAR})
        self.assertEqual(set(), codes, messages)

    def test_a_missing_sidecar_is_flagged(self):
        codes, messages = os_run({"skills/x/SKILL.md": self.SKILL})
        self.assertIn("GRAPH", codes)
        self.assertIn("SKILL.graph.yml", messages)

    def test_an_extra_key_in_the_sidecar_still_fails(self):
        codes, messages = os_run(
            {"skills/x/SKILL.md": self.SKILL,
             "skills/x/SKILL.graph.yml": self.SIDECAR + "owner: someone\n"})
        self.assertIn("GRAPH", codes)
        self.assertIn('carries "owner"', messages)

    def test_a_graph_key_in_the_skill_frontmatter_is_still_rejected(self):
        smuggled = ("---\nname: x\ndescription: Use when testing.\n"
                    "layer: skills\n---\nBody.\n")
        codes, messages = os_run(
            {"skills/x/SKILL.md": smuggled,
             "skills/x/SKILL.graph.yml": self.SIDECAR})
        self.assertIn("FRONTMATTER", codes)
        self.assertIn("exactly name and description", messages)

    def test_name_and_description_stay_legal_beside_the_graph_keys(self):
        agent = ("---\nname: an-agent\ndescription: Use when testing.\n"
                 "layer: agents\nstage: DESIGN\ngate: 3\nfeeds: []\n"
                 'method: ""\naliases: ["An agent"]\n---\n# An agent\n')
        codes, messages = os_run({"agents/an-agent.md": agent})
        self.assertEqual(set(), codes, messages)


class SecretGateTests(unittest.TestCase):
    """Check 9. Every fixture key is assembled from fragments, so this file
    never contains a credential-shaped literal, and the gate that now reads
    this file with no exemption stays green on it."""

    # Modern issuers put their own prefix in the token, which is what the gate
    # anchors on. Split before the payload so no line here matches a pattern.
    OPENAI_PROJECT = "sk-proj-" + "Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op"
    OPENAI_SERVICE = "sk-svcacct-" + "Qr1St2Uv3Wx4Yz5Ab6Cd7Ef"
    GITHUB_FINE = "github_pat_" + "11ABCDEFG0abcdefghij1234"
    JWT = ("eyJ" + "hbGciOiJIUzI1NiJ9" + "."
           + "eyJzdWIiOiIxMjMifQ" + "." + "dBjftJeZ4CVPmB92K27u")
    PEM = "-" * 5 + "BEGIN RSA PRIVATE KEY" + "-" * 5
    HOT_VALUE = "aB3dE6fG9hJ2" + "kL5mN8pQ1rS4tU7v"

    def test_modern_token_formats_are_caught(self):
        for label, value in (("OpenAI project key", self.OPENAI_PROJECT),
                             ("OpenAI service-account key",
                              self.OPENAI_SERVICE),
                             ("GitHub fine-grained token", self.GITHUB_FINE),
                             ("JSON web token", self.JWT),
                             ("private key block", self.PEM)):
            codes, messages = os_run({"docs/note.md": "key = %s\n" % value})
            self.assertIn("SECRET", codes, label)
            self.assertIn(label, messages)

    def test_an_aws_secret_access_key_value_is_caught(self):
        value = "aws_secret_access_key=" + "wJalrXUtnFEMI" + "K7MDENGbPxRfiCY" \
                + "EXAMPLEKEY12"
        codes, messages = os_run({"docs/note.md": value + "\n"})
        self.assertIn("SECRET", codes)
        self.assertIn("AWS secret access key value", messages)

    def test_a_high_entropy_value_under_a_credential_name_is_caught(self):
        codes, messages = os_run(
            {"docs/note.md": "session_token: %s\n" % self.HOT_VALUE})
        self.assertIn("SECRET", codes)
        self.assertIn("high-entropy value", messages)

    def test_prose_under_a_credential_name_is_not_caught(self):
        codes, messages = os_run(
            {"docs/note.md": "password: ask the security owner for it\n"
                             "token: the one the runbook names\n"})
        self.assertNotIn("SECRET", codes, messages)

    def test_a_base64_wrapped_token_is_caught(self):
        import base64
        wrapped = base64.b64encode(
            ("ghp_" + "abcdefghij0123456789").encode()).decode()
        codes, messages = os_run({"docs/note.md": "blob = %s\n" % wrapped})
        self.assertIn("SECRET", codes)
        self.assertIn("base64-encoded", messages)

    def test_a_token_split_across_a_line_break_is_caught(self):
        codes, messages = os_run({"docs/note.md": "key = AKIA\n" + "Z" * 16})
        self.assertIn("SECRET", codes)
        self.assertIn("line breaks are closed up", messages)

    def test_a_rule_bearing_file_is_not_exempt_from_the_secret_gate(self):
        fixture = {"docs/ARCHITECTURE.md": "example: %s\nOwner: TBD\n"
                                           % self.OPENAI_PROJECT}
        codes, messages = os_run(fixture)
        self.assertIn("SECRET", codes, messages)
        # Still exempt from the placeholder gate, which is the exemption that
        # exists for a reason: this file names the detector's own strings.
        self.assertNotIn("TBD", codes)

    def test_an_undecodable_file_fails_instead_of_being_skipped(self):
        codes, messages = os_run_bytes({"docs/note.md": b"head \xff\xfe tail"})
        self.assertIn("ENCODING", codes)
        self.assertIn("not valid UTF-8", messages)


class PathGateFenceTests(unittest.TestCase):
    """Check 8. The prompt body a user pastes lives inside a fenced block."""

    def test_a_repo_path_inside_a_fence_is_checked(self):
        fenced = ("Paste this:\n\n```\nRead templates/nowhere.md first.\n"
                  "```\n")
        codes, messages = os_run({"system/PROMPT.md": fenced})
        self.assertIn("PATH", codes)
        self.assertIn("templates/nowhere.md", messages)

    def test_a_manifest_line_resolves_names_against_its_directory(self):
        fenced = ("```\nlearn/         README.md, skills/tutor/SKILL.md\n"
                  "```\n")
        codes, messages = os_run(
            {"system/PROMPT.md": fenced,
             "learn/README.md": "# Learn\n",
             "learn/skills/tutor/SKILL.md":
                 "---\nname: tutor\ndescription: Use when learning.\n---\nX.\n"})
        self.assertNotIn("PATH", codes, messages)


class GraphTruthTests(unittest.TestCase):
    """Check 10. Legal keys are not the same claim as a true graph."""

    def test_a_layer_outside_the_directory_set_is_flagged(self):
        codes, messages = os_run({"templates/thing.md":
                                  template_file(layer="bananas")})
        self.assertIn("GRAPH", codes)
        self.assertIn('layer "bananas" is not a layer directory', messages)

    def test_a_layer_naming_another_directory_is_flagged(self):
        codes, messages = os_run({"templates/thing.md":
                                  template_file(layer="agents"),
                                  "agents/other.md": ""})
        self.assertIn("GRAPH", codes)
        self.assertIn("is not the directory this file lives in", messages)

    def test_a_declaration_contradicting_its_own_stage_header_is_flagged(self):
        contradicting = (graph_fm(stage="DEFINE", gate="6") + "# Thing\n\n"
                         + "Stage: DEFINE, feeds Gate 2\n"
                           "Knowledge: none\nSkill: manual\n")
        codes, messages = os_run({"templates/thing.md": contradicting})
        self.assertIn("GRAPH", codes)
        self.assertIn("its own Stage header names gate 2", messages)

    def test_a_stage_and_gate_the_gates_document_denies_are_flagged(self):
        silent = (graph_fm(stage="DEFINE", gate="6") + "# Thing\n\n"
                  + "Stage: DEFINE\nKnowledge: none\nSkill: manual\n")
        codes, messages = os_run({"templates/thing.md": silent})
        self.assertIn("GRAPH", codes)
        self.assertIn("gate 2 closing DEFINE", messages)

    def test_a_block_list_feeds_is_read_rather_than_skipped(self):
        block = ("---\nlayer: templates\nstage: DEFINE\ngate: 2\nfeeds:\n"
                 "  - templates/gone.md\nmethod: \"\"\naliases:\n"
                 "  - The Thing\n---\n# Thing\n\n" + TEMPLATE_HEADER)
        codes, messages = os_run({"templates/thing.md": block})
        self.assertIn("GRAPH", codes)
        self.assertIn("feeds names templates/gone.md", messages)

    def test_a_block_list_that_resolves_passes_and_declares_its_alias(self):
        block = ("---\nlayer: templates\nstage: DEFINE\ngate: 2\nfeeds:\n"
                 "  - templates/other.md\nmethod: \"\"\naliases:\n"
                 "  - The Thing\n---\n# Thing\n\n" + TEMPLATE_HEADER)
        codes, messages = os_run({
            "templates/thing.md": block,
            "templates/other.md": template_file(aliases='["The Other"]'),
            "docs/note.md": "see [[the thing]]\n"})
        self.assertEqual(set(), codes, messages)

    def test_a_gate_target_feeds_is_accepted(self):
        codes, messages = os_run({"templates/thing.md":
                                  template_file(feeds='["Gate 2"]')})
        self.assertEqual(set(), codes, messages)

    def test_a_feeds_gate_the_document_does_not_define_is_flagged(self):
        codes, messages = os_run({"templates/thing.md":
                                  template_file(feeds='["Gate 9"]')})
        self.assertIn("GRAPH", codes)
        self.assertIn("feeds names gate 9", messages)


class LinkTruthTests(unittest.TestCase):
    """Check 4 and check 11. Some target existing is not the target existing."""

    def test_a_qualified_wikilink_must_resolve_at_that_path(self):
        codes, messages = os_run({"docs/note.md": "see [[wrong/place/other.md]]\n",
                                  "docs/other.md": "Other.\n"})
        self.assertIn("WIKILINK", codes)
        self.assertIn("names neither a file at that path", messages)

    def test_an_ambiguous_bare_wikilink_is_flagged(self):
        codes, messages = os_run({"docs/note.md": "see [[other.md]]\n",
                                  "docs/other.md": "One.\n",
                                  "docs/sub/other.md": "Two.\n"})
        self.assertIn("WIKILINK", codes)
        self.assertIn("is ambiguous", messages)

    def test_a_unique_bare_wikilink_still_resolves(self):
        codes, messages = os_run({"docs/note.md": "see [[other.md]]\n",
                                  "docs/other.md": "One.\n"})
        self.assertNotIn("WIKILINK", codes, messages)

    def test_an_alias_holding_a_comma_stays_one_alias(self):
        files = {"templates/thing.md":
                 template_file(aliases='["Now, Next, Later"]'),
                 "docs/whole.md": "see [[Now, Next, Later]]\n"}
        codes, messages = os_run(files)
        self.assertEqual(set(), codes, messages)
        files["docs/part.md"] = "see [[Now]]\n"
        codes, messages = os_run(files)
        self.assertIn("WIKILINK", codes)
        self.assertIn("[[Now]]", messages)

    def test_a_duplicate_alias_is_reported(self):
        codes, messages = os_run({
            "templates/thing.md": template_file(aliases='["Shared"]'),
            "templates/other.md": template_file(aliases='["Shared"]')})
        self.assertIn("GRAPH", codes)
        self.assertIn("is already declared by", messages)

    def test_a_markdown_link_climbing_out_of_the_repository_is_flagged(self):
        codes, messages = os_run(
            {"docs/sub/note.md": "[out](../../../etc/hosts)\n"})
        self.assertIn("LINK", codes)
        self.assertIn("climbs out of the repository", messages)


class RegulatedPrdDepthTests(unittest.TestCase):
    """Check the PRD gate on a document that is shaped right and gutted."""

    JUNK_TABLE = ("| Note | Detail |\n|---|---|\n| Something | Anything |")

    def test_an_arbitrary_table_does_not_satisfy_section_0(self):
        gutted = MINIMAL.replace(
            "| Market | License condition | Regulator | Confirmed how | "
            "Confirmed date | Owner |\n|---|---|---|---|---|---|\n"
            "| UAE | No change to licensed activity | CBUAE | Memo REG-1 | "
            "2026-01-02 | Reg Lead |", self.JUNK_TABLE)
        codes, messages = run(gutted)
        self.assertIn("OVERLAY", codes)
        self.assertIn("section 0.1 has no table carrying the required columns",
                      messages)

    def test_a_register_with_a_header_and_no_rows_is_flagged(self):
        emptied = MINIMAL.replace(
            "| UAE | No change to licensed activity | CBUAE | Memo REG-1 | "
            "2026-01-02 | Reg Lead |\n", "")
        codes, messages = run(emptied)
        self.assertIn("OVERLAY", codes)
        self.assertIn("section 0.1 register has a header row and no entries",
                      messages)

    def test_an_eval_table_with_no_rows_is_flagged(self):
        emptied = MINIMAL.replace(
            "| 1 | Amount extracted | Exact-match accuracy | DS-A: 400 cases | "
            + THRESHOLD + " | Block | Ops Lead |\n", "")
        codes, messages = run(emptied)
        self.assertIn("EVAL", codes)
        self.assertIn("right columns and no rows", messages)

    def test_an_angle_bracket_field_is_not_an_answer_in_full_mode(self):
        unfilled = MINIMAL.replace("Reg Lead", "<owner>")
        codes, messages = run(unfilled)
        self.assertIn("OVERLAY", codes)
        self.assertIn("unfilled <angle-bracket> field", messages)
        # Template mode keeps its own bargain: an unfilled template is
        # supposed to be unfilled.
        self.assertEqual(set(), run(unfilled, template_mode=True)[0])

    def test_the_pinned_example_survives_the_stricter_gate(self):
        example = (REPO / "modules" / "regulated" / "examples"
                   / "dispute-summary" / "PRD.md")
        self.assertEqual([], lint.check(example)[0])


class IntegrityPinCoverageTests(unittest.TestCase):
    """Finding 20. Everything the repository calls verbatim is pinned."""

    VERBATIM = ("modules/regulated/templates/regulated-ai-prd-template.md",
                "modules/regulated/examples/dispute-summary/PRD.md",
                "modules/regulated/SKILL.md",
                "modules/regulated/lint.py",
                "modules/regulated/test_lint.py")

    def test_every_verbatim_regulated_file_is_pinned(self):
        for rel in self.VERBATIM:
            self.assertIn(rel, lint.PINNED_HASHES)

    def test_each_pin_matches_the_bytes_on_disk(self):
        import hashlib
        for rel, expected in lint.PINNED_HASHES.items():
            target = REPO / rel
            self.assertTrue(target.is_file(), rel)
            self.assertEqual(
                expected, hashlib.sha256(target.read_bytes()).hexdigest(), rel)


if __name__ == "__main__":
    unittest.main()
