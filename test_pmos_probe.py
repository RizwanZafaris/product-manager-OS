"""Regressions for the EXT-AI probe and the skill rubric.

These sit at the public CLI boundary -- ``ext_ai_probe.main(argv)`` and
``skill_rubric.main(argv)`` -- because that is the surface an operator and CI
actually invoke, and every defect covered here reported success through it.

No network is reachable from these tests: the provider transport is patched to
raise if it is ever entered, and each run asserts it was not.
"""

from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ext_ai_probe as probe  # noqa: E402
import skill_rubric  # noqa: E402
from pmos.openrouter import OpenRouterProvider, OpenRouterResponse  # noqa: E402
from pmos.routing import ModelSpec  # noqa: E402

FREE = ModelSpec(provider="openrouter", model="test/mock-free", free=True,
                 available=True, certified=False, context_window=8192,
                 cost_per_1k_tokens=0.0,
                 privacy_classes=frozenset({"public"}))
PAID = ModelSpec(provider="openrouter", model="test/mock-paid", free=False,
                 available=True, certified=False, context_window=8192,
                 cost_per_1k_tokens=0.000001,
                 privacy_classes=frozenset({"public"}))


def run_probe(args, spec=FREE, complete=None, omni=None):
    """Invoke the probe CLI with discovery and evidence-writing captured."""
    captured = {}

    def discover(report, args):
        report["catalog"] = {"discovered": 1, "free_models": [spec.model],
                             "free_only": True, "certified_models": []}
        return [spec]

    with contextlib.ExitStack() as stack:
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        stack.enter_context(patch.object(probe, "credential_present",
                                         return_value=True))
        stack.enter_context(patch.object(probe, "discover", side_effect=discover))
        stack.enter_context(patch.object(
            probe, "write", side_effect=lambda r, o: captured.update(r)))
        network = stack.enter_context(
            patch.object(OpenRouterProvider, "_json_request",
                         side_effect=AssertionError("network prohibited")))
        adapter = None
        if complete is not None:
            adapter = stack.enter_context(
                patch.object(OpenRouterProvider, "complete", **complete))
        if omni is not None:
            stack.enter_context(patch.object(
                probe, "omniroute_models",
                return_value=["openrouter/test/free:free"]))
            adapter = stack.enter_context(
                patch.object(probe, "omniroute_chat", **omni))
        code = probe.main(args)
        assert network.call_count == 0, "a test opened the network path"
    return code, captured, adapter


def answer(output="a real nonempty answer", model=FREE.model, cost=0.0):
    return OpenRouterResponse(output=output, input_tokens=10, output_tokens=20,
                              total_tokens=30, actual_model=model, cost_usd=cost)


class DispatchAccountingTests(unittest.TestCase):
    """A cap counts dispatch attempts, not the ones that happened to work.

    Counting successes let a failing adapter be re-entered once per case: the
    audit observed four attempts under ``--max-calls 1``. A cap that loosens
    exactly when calls start failing is the opposite of a cap.
    """

    def test_failed_attempts_count_against_the_cap(self):
        code, report, adapter = run_probe(
            ["--max-calls", "1"],
            complete={"side_effect": RuntimeError("upstream refused")})
        self.assertEqual(adapter.call_count, 1)
        self.assertEqual(len(report["calls"]), 1)
        self.assertNotEqual(code, 0)

    def test_failed_attempts_count_against_the_cap_via_omniroute(self):
        code, _report, adapter = run_probe(
            ["--via", "omniroute", "--max-calls", "1"],
            omni={"return_value": {"error": "mock_provider_failure"}})
        self.assertEqual(adapter.call_count, 1)
        self.assertNotEqual(code, 0)

    def test_a_run_with_errors_does_not_report_success(self):
        code, report, _ = run_probe(
            ["--max-calls", "3"],
            complete={"side_effect": RuntimeError("upstream refused")})
        self.assertGreater(report["totals"]["errors"], 0)
        self.assertNotEqual(code, 0)

    def test_a_clean_run_still_reports_success(self):
        """The failing exit code must be caused by failure, not by running."""
        code, report, _ = run_probe(["--max-calls", "1"],
                                    complete={"return_value": answer()})
        self.assertEqual(report["totals"]["errors"], 0)
        self.assertEqual(code, 0)


class AdapterContractTests(unittest.TestCase):
    """The probe must speak the adapter's actual contract.

    ``OpenRouterProvider.complete`` takes a model-ID string and returns a
    ProviderResponse carrying ``output``, ``input_tokens`` and
    ``output_tokens``. The probe passed a ModelSpec and read ``.text``,
    ``.prompt_tokens`` and ``.completion_tokens``, so every call raised
    OpenRouterMalformedResponse, and when a response was forced in it recorded
    zero characters and null usage for an answer that had both.
    """

    def test_the_adapter_is_given_a_model_id_string(self):
        _code, _report, adapter = run_probe(["--max-calls", "1"],
                                            complete={"return_value": answer()})
        model_argument = adapter.call_args[0][0]
        self.assertIsInstance(model_argument, str)
        self.assertEqual(model_argument, FREE.model)

    def test_response_text_and_usage_are_read_from_the_real_fields(self):
        text = "a real nonempty answer"
        _code, report, _ = run_probe(
            ["--max-calls", "1"], complete={"return_value": answer(output=text)})
        call = report["calls"][0]
        self.assertEqual(call["response_chars"], len(text))
        self.assertEqual(call["prompt_tokens"], 10)
        self.assertEqual(call["completion_tokens"], 20)
        self.assertEqual(call["resolved_model"], FREE.model)


class ProvenanceTests(unittest.TestCase):
    """Evidence without a resolved model is not evidence of a model call."""

    def test_a_missing_resolved_model_is_recorded_as_a_failure(self):
        _code, report, _ = run_probe(
            ["--max-calls", "1"], complete={"return_value": answer(model=None)})
        self.assertTrue(report["calls"][0].get("error"),
                        "a call with no resolved model must not be recorded clean")

    def test_a_missing_resolved_model_fails_the_run(self):
        code, _report, _ = run_probe(
            ["--max-calls", "1"], complete={"return_value": answer(model=None)})
        self.assertNotEqual(code, 0)

    def test_omniroute_missing_resolved_model_is_recorded_as_a_failure(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--max-calls", "1"],
            omni={"return_value": {"text": "answer", "resolved_model": None}})
        self.assertTrue(report["calls"][0].get("error"))
        self.assertNotEqual(code, 0)


class BudgetTests(unittest.TestCase):
    """A ceiling only ever compared after the fact is not a ceiling."""

    def test_a_provider_overcharge_halts_the_run_instead_of_repeating(self):
        """What is actually enforceable when price is only known afterwards.

        Cost arrives with the response, so no design can hold total spend under
        the ceiling when a provider bills more than it advertised. What it can
        do is reserve against the advertised price, detect the discrepancy on
        reconciliation, stop, and fail. The audit saw the opposite: six cases
        ran, $3.00 was billed against a $0.01 ceiling, and the run exited 0.
        """
        code, report, adapter = run_probe(
            ["--allow-paid", "--budget-usd", "0.01", "--model", PAID.model,
             "--max-calls", "6"],
            spec=PAID,
            complete={"return_value": answer(model=PAID.model, cost=0.75)})
        self.assertEqual(adapter.call_count, 1, "the breach must stop the run")
        self.assertAlmostEqual(report["totals"]["cost_usd"], 0.75, places=6)
        self.assertTrue(report["totals"].get("budget_breach"))
        self.assertNotEqual(code, 0)

    def test_a_call_whose_advertised_price_exceeds_the_ceiling_is_never_sent(self):
        """Reservation happens before dispatch, using the advertised price."""
        dear = ModelSpec(provider="openrouter", model="test/mock-dear", free=False,
                         available=True, certified=False, context_window=8192,
                         cost_per_1k_tokens=10.0,
                         privacy_classes=frozenset({"public"}))
        code, report, adapter = run_probe(
            ["--allow-paid", "--budget-usd", "0.01", "--model", dear.model,
             "--max-calls", "6"],
            spec=dear,
            complete={"return_value": answer(model=dear.model, cost=10.0)})
        self.assertEqual(adapter.call_count, 0)
        self.assertEqual(report["totals"]["cost_usd"], 0.0)
        self.assertNotEqual(code, 0)

    def test_the_run_stops_once_the_ceiling_is_known_to_be_reached(self):
        _code, _report, adapter = run_probe(
            ["--allow-paid", "--budget-usd", "0.01", "--model", PAID.model,
             "--max-calls", "6"],
            spec=PAID,
            complete={"return_value": answer(model=PAID.model, cost=0.75)})
        self.assertLessEqual(adapter.call_count, 1)

    def test_a_run_inside_its_budget_completes(self):
        code, report, _ = run_probe(
            ["--allow-paid", "--budget-usd", "1.00", "--model", PAID.model,
             "--max-calls", "1"],
            spec=PAID,
            complete={"return_value": answer(model=PAID.model, cost=0.10)})
        self.assertEqual(code, 0)
        self.assertAlmostEqual(report["totals"]["cost_usd"], 0.10, places=6)


class DiscoveryOnlyTests(unittest.TestCase):
    """``--discover-only`` must not generate, by any transport."""

    def test_discovery_only_makes_no_generation_via_omniroute(self):
        code, _report, adapter = run_probe(
            ["--via", "omniroute", "--discover-only", "--max-calls", "1"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(adapter.call_count, 0)
        self.assertEqual(code, 0)

    def test_discovery_only_makes_no_generation_on_the_direct_path(self):
        code, _report, adapter = run_probe(
            ["--discover-only", "--max-calls", "1"],
            complete={"return_value": answer()})
        self.assertEqual(adapter.call_count, 0)
        self.assertEqual(code, 0)


class SkillRubricTests(unittest.TestCase):
    """A heading is not a procedure.

    The rubric counted sections present, so a skill carrying all seven required
    headings and nothing underneath them scored a pass. That made the rubric an
    autocomplete check rather than a quality gate.
    """

    def _install(self, root, body):
        skills = root / "skills"
        skills.mkdir(exist_ok=True)
        doc = skills / "SKILL.md"
        doc.write_text(body, encoding="utf-8")
        return skills, doc

    def test_seven_empty_headings_do_not_pass(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            body = "# Empty procedure\n\n" + "\n\n".join(
                "## " + heading for heading in skill_rubric.SECTIONS)
            skills, doc = self._install(root, body)
            with patch.object(skill_rubric, "REPO", root), \
                 patch.object(skill_rubric, "SKILLS", skills):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = skill_rubric.main(["--min", "7"])
                score = skill_rubric.score_skill(doc)
            self.assertEqual(score["workflow_steps"], 0)
            self.assertNotEqual(code, 0,
                                "empty headings must not satisfy the rubric")

    def test_a_real_shipped_skill_still_passes(self):
        """The rubric must reject emptiness, not content it merely dislikes."""
        source = Path(__file__).resolve().parent / "skills"
        candidates = sorted(source.glob("*/SKILL.md"))
        self.assertTrue(candidates, "repository ships no skills to compare against")
        with TemporaryDirectory() as directory:
            root = Path(directory)
            body = candidates[0].read_text(encoding="utf-8")
            skills, doc = self._install(root, body)
            with patch.object(skill_rubric, "REPO", root), \
                 patch.object(skill_rubric, "SKILLS", skills):
                score = skill_rubric.score_skill(doc)
            self.assertGreater(score["workflow_steps"], 0)


if __name__ == "__main__":
    unittest.main()


class ZeroBudgetTests(unittest.TestCase):
    """Zero is a ceiling, not an absence of one.

    The guard read ``if budget``, so a budget of $0.00 -- the default, and the
    value a free-only run declares -- skipped reservation and breach checks
    entirely. An independent reviewer dispatched twice and billed $1.50 against
    it with budget_breach false and exit 0. Unexpected billing can explain the
    first charge; it cannot explain the second dispatch or a successful exit.
    """

    def test_a_zero_budget_stops_after_the_first_unexpected_charge(self):
        code, report, adapter = run_probe(
            ["--max-calls", "2"], complete={"return_value": answer(cost=0.75)})
        self.assertEqual(adapter.call_count, 1, "the second dispatch must not happen")
        self.assertTrue(report["totals"]["budget_breach"])
        self.assertNotEqual(code, 0)

    def test_a_free_run_that_costs_nothing_still_succeeds(self):
        code, report, _ = run_probe(["--max-calls", "1"],
                                    complete={"return_value": answer(cost=0.0)})
        self.assertEqual(code, 0)
        self.assertFalse(report["totals"]["budget_breach"])

    def test_unbounded_spend_is_opt_in_and_never_the_default(self):
        code, report, adapter = run_probe(
            ["--max-calls", "2", "--allow-paid", "--unbounded-budget"],
            complete={"return_value": answer(cost=0.75)})
        self.assertEqual(adapter.call_count, 2)
        self.assertFalse(report["totals"]["budget_breach"])
        self.assertEqual(code, 0)


class UnknownCostTests(unittest.TestCase):
    """Absent authoritative cost is UNKNOWN, never zero."""

    def test_a_missing_cost_is_not_recorded_as_zero(self):
        _code, report, _ = run_probe(["--max-calls", "1"],
                                     complete={"return_value": answer(cost=None)})
        call = report["calls"][0]
        self.assertIsNone(call["cost_usd"])
        self.assertEqual(call.get("cost_status"), "UNKNOWN")

    def test_a_missing_cost_fails_the_run(self):
        code, _report, _ = run_probe(["--max-calls", "1"],
                                     complete={"return_value": answer(cost=None)})
        self.assertNotEqual(code, 0)

    def test_a_nonsense_cost_is_rejected_rather_than_summed(self):
        for bad in (float("nan"), float("inf"), -1.0):
            with self.subTest(cost=bad):
                code, report, _ = run_probe(
                    ["--max-calls", "1"],
                    complete={"return_value": answer(cost=bad)})
                self.assertTrue(report["calls"][0].get("error"))
                self.assertNotEqual(code, 0)


class GatewayEligibilityTests(unittest.TestCase):
    """The gateway must not invent eligibility or price.

    The OmniRoute path took ``args.model`` on trust, built a ModelSpec with
    free=True regardless, and recorded cost 0.0. A reviewer pinned
    ``vendor/paid-model`` against a catalog advertising only a free test model,
    got one dispatch, exit 0 and a reported cost of $0.00 for a $2 call.
    """

    def test_a_model_outside_the_discovered_catalog_is_refused(self):
        code, _report, adapter = run_probe(
            ["--via", "omniroute", "--model", "vendor/paid-model",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "vendor/paid-model",
                                   "cost_usd": 2}})
        self.assertEqual(adapter.call_count, 0)
        self.assertNotEqual(code, 0)

    def test_a_catalog_model_is_still_allowed(self):
        """Membership admits the call; cost evidence is a separate requirement.

        Updated when absent gateway cost became UNKNOWN. This case previously
        passed with no cost at all, which only worked because absence was
        being read as $0.00 -- the very defect R2 reported. It now supplies a
        cost, so it tests admission rather than the fabricated zero.
        """
        code, _report, adapter = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer", "cost_usd": 0.0,
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(adapter.call_count, 1)
        self.assertEqual(code, 0)

    def test_a_catalog_model_without_cost_evidence_is_admitted_but_fails(self):
        """Admission and evidence are distinct: it dispatches, then fails."""
        code, report, adapter = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(adapter.call_count, 1)
        self.assertEqual(report["calls"][0]["cost_status"], "UNKNOWN")
        self.assertNotEqual(code, 0)

    def test_a_resolved_model_other_than_the_pinned_one_is_an_error(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "something/else"}})
        self.assertTrue(report["calls"][0].get("error"))
        self.assertNotEqual(code, 0)

    def test_a_reported_gateway_cost_is_carried_not_zeroed(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "openrouter/test/free:free",
                                   "cost_usd": 2}})
        self.assertEqual(report["calls"][0]["cost_usd"], 2)
        self.assertTrue(report["totals"]["budget_breach"])
        self.assertNotEqual(code, 0)


class ExecutionLimitTests(unittest.TestCase):
    """A run that dispatched nothing has not produced generation evidence."""

    def test_a_zero_call_cap_is_not_a_successful_generation_run(self):
        code, _report, adapter = run_probe(
            ["--via", "omniroute", "--max-calls", "0"],
            omni={"return_value": {"text": "answer",
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(adapter.call_count, 0)
        self.assertNotEqual(code, 0)

    def test_a_zero_call_cap_fails_on_the_direct_path_too(self):
        code, _report, adapter = run_probe(
            ["--max-calls", "0"], complete={"return_value": answer()})
        self.assertEqual(adapter.call_count, 0)
        self.assertNotEqual(code, 0)

    def test_refusal_cases_are_still_evaluated_once_the_cap_is_reached(self):
        """Refusals cost nothing, and they are the evidence the gate exists for."""
        _code, report, _ = run_probe(["--max-calls", "1"],
                                     complete={"return_value": answer()})
        refusal_ids = {r["case"] for r in report["policy_results"]
                       if not r["eligible"]}
        self.assertIn("architecture-refusal-check", refusal_ids)
        self.assertIn("regulatory-refusal-check", refusal_ids)


class ProbeConfigurationTests(unittest.TestCase):
    """Contract details the audit's happy-path cases never exercised."""

    def test_a_custom_credential_variable_reaches_the_adapter(self):
        seen = {}
        real_init = OpenRouterProvider.__init__

        def record(self, *args, **kwargs):
            seen["api_key_env"] = kwargs.get("api_key_env")
            return real_init(self, *args, **kwargs)

        with patch.object(OpenRouterProvider, "__init__", record):
            run_probe(["--max-calls", "1", "--env", "CUSTOM_KEY_VAR"],
                      complete={"return_value": answer()})
        self.assertEqual(seen.get("api_key_env"), "CUSTOM_KEY_VAR")

    def test_the_gateway_subprocess_has_a_finite_timeout(self):
        import subprocess as sp
        seen = {}

        def record(argv, **kwargs):
            seen.update(kwargs)
            return sp.CompletedProcess(argv, 0, stdout="ok", stderr="")

        with patch.object(probe.subprocess, "run", side_effect=record):
            probe.omniroute_chat("openrouter/test/free:free", "hello")
        self.assertIsNotNone(seen.get("timeout"))
        self.assertGreater(seen["timeout"], 0)

    def test_the_cost_reservation_bound_is_not_below_the_byte_length(self):
        """len(prompt)//4 under-counts; a token is never more than a byte."""

        class Args:
            max_output_tokens = 1

        prompt = "x" * 400
        reserved = probe.reserve_cost_usd(PAID, prompt, Args())
        floor = PAID.cost_per_1k_tokens * len(prompt.encode("utf-8")) / 1000.0
        self.assertGreaterEqual(reserved, floor)


class CanonicalCoverageTests(unittest.TestCase):
    """A regression suite CI does not run is not coverage."""

    def test_this_module_is_registered_in_the_canonical_gate(self):
        import ci_gate
        argv = [a for gate in ci_gate.GATES for a in gate.argv]
        self.assertIn("test_pmos_probe", argv)


class CrossTransportCostAndIdentityTests(unittest.TestCase):
    """One behaviour matrix, applied to both transports.

    Each defect below was found on one transport after the other had been
    fixed, which is the tell that they were being fixed case by case rather
    than as a contract. These assert the contract on both.
    """

    # -- missing cost ----------------------------------------------------
    def test_gateway_omitting_cost_entirely_is_unknown_not_zero(self):
        """The real omniroute_chat never returns cost_usd, so this is the
        ordinary production shape, not an exotic adapter."""
        code, report, adapter = run_probe(
            ["--via", "omniroute", "--max-calls", "2"],
            omni={"return_value": {"text": "ok",
                                   "resolved_model": "openrouter/test/free:free"}})
        call = report["calls"][0]
        self.assertEqual(call.get("cost_status"), "UNKNOWN")
        self.assertIsNone(call.get("cost_usd"))
        self.assertEqual(adapter.call_count, 1, "unknown cost must stop the run")
        self.assertNotEqual(code, 0)

    def test_direct_omitting_cost_is_unknown_not_zero(self):
        code, report, adapter = run_probe(
            ["--max-calls", "2"], complete={"return_value": answer(cost=None)})
        self.assertEqual(report["calls"][0].get("cost_status"), "UNKNOWN")
        self.assertEqual(adapter.call_count, 1)
        self.assertNotEqual(code, 0)

    # -- unknown cost halts ----------------------------------------------
    def test_gateway_explicit_null_cost_halts_before_a_second_dispatch(self):
        code, report, adapter = run_probe(
            ["--via", "omniroute", "--max-calls", "2"],
            omni={"return_value": {"text": "ok", "cost_usd": None,
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(adapter.call_count, 1)
        self.assertNotEqual(code, 0)

    def test_aggregate_cost_reports_uncertainty_rather_than_zero(self):
        _code, report, _ = run_probe(
            ["--via", "omniroute", "--max-calls", "2"],
            omni={"return_value": {"text": "ok",
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertTrue(report["totals"].get("cost_unknown"),
                        "an aggregate of unknowns must not read as $0.00")

    # -- model identity --------------------------------------------------
    def test_direct_rejects_a_substituted_model(self):
        code, report, _ = run_probe(
            ["--max-calls", "1"],
            complete={"return_value": answer(model="unapproved/model")})
        self.assertTrue(report["calls"][0].get("error"))
        self.assertNotEqual(code, 0)

    def test_gateway_rejects_a_substituted_model(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "ok", "cost_usd": 0.0,
                                   "resolved_model": "unapproved/model"}})
        self.assertTrue(report["calls"][0].get("error"))
        self.assertNotEqual(code, 0)

    def test_the_authorised_model_is_still_accepted_on_both_transports(self):
        code, _report, _ = run_probe(
            ["--max-calls", "1"],
            complete={"return_value": answer(model=FREE.model, cost=0.0)})
        self.assertEqual(code, 0)
        code, _report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "ok", "cost_usd": 0.0,
                                   "resolved_model": "openrouter/test/free:free"}})
        self.assertEqual(code, 0)

    # -- a known charge survives a provenance error ----------------------
    def test_a_known_charge_is_kept_when_provenance_fails(self):
        _code, report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "ok", "cost_usd": 0.5,
                                   "resolved_model": None}})
        call = report["calls"][0]
        self.assertTrue(call.get("error"))
        self.assertEqual(call.get("cost_usd"), 0.5,
                         "billing data must not be discarded with the result")


class DiscoveryBoundaryTests(unittest.TestCase):
    """The discovery boundary was mocked away in every existing test."""

    def test_discovery_passes_the_custom_credential_variable(self):
        seen = []
        import pmos.openrouter as openrouter_module
        real_init = openrouter_module.OpenRouterProvider.__init__

        def spy(self, *args, **kwargs):
            seen.append(kwargs.get("api_key_env"))
            return real_init(self, *args, **kwargs)

        class Args:
            env = "CUSTOM_KEY_VAR"
            free_only = True
            model = None
            certified_only = False

        with patch.object(openrouter_module.OpenRouterProvider, "__init__", spy):
            try:
                probe.discover({"catalog": {}}, Args())
            except Exception:            # noqa: BLE001 - transport is absent
                pass
        self.assertTrue(seen, "discovery never constructed a provider")
        self.assertIn("CUSTOM_KEY_VAR", seen)

    def test_gateway_discovery_has_a_finite_timeout(self):
        import subprocess as sp
        seen = {}

        def record(argv, **kwargs):
            seen.update(kwargs)
            return sp.CompletedProcess(argv, 0, stdout="", stderr="")

        with patch.object(probe.subprocess, "run", side_effect=record):
            probe.omniroute_models(free_only=True)
        self.assertIsNotNone(seen.get("timeout"))
        self.assertGreater(seen["timeout"], 0)


# --------------------------------------------------------------------------
# Shared acceptance matrix
#
# Every defect closed so far was found on one transport after the other had
# already been fixed, which is the tell that they were being repaired case by
# case rather than as a contract. This table states the contract once and runs
# it against both transports, so a fix to one cannot silently drift from the
# other.
# --------------------------------------------------------------------------

CATALOG_MODEL = "openrouter/test/free:free"


def _direct(case):
    """Run one matrix row through the direct adapter."""
    argv = ["--max-calls", "2"] + list(case.get("argv", []))
    if case.get("raises"):
        return run_probe(argv, complete={"side_effect": case["raises"]})
    return run_probe(argv, complete={"return_value": answer(
        output=case.get("output", "a real answer"),
        model=case.get("model", FREE.model),
        cost=case.get("cost", None) if "cost" not in case
        else case["cost"])})


def _gateway(case):
    """Run the same row through the OmniRoute gateway."""
    argv = ["--via", "omniroute", "--model", CATALOG_MODEL,
            "--max-calls", "2"] + list(case.get("argv", []))
    if case.get("raises"):
        return run_probe(argv, omni={"side_effect": case["raises"]})
    result = {"text": case.get("output", "a real answer"),
              "resolved_model": (CATALOG_MODEL if case.get("model", "keep") == "keep"
                                 else case.get("model"))}
    if "cost" in case:
        result["cost_usd"] = case["cost"]
    return run_probe(argv, omni={"return_value": result})


MATRIX = (
    {"id": "clean-free-call", "cost": 0.0,
     "expect_ok": True, "max_dispatches": 2},
    {"id": "cost-missing", "expect_ok": False, "max_dispatches": 1,
     "cost_status": "UNKNOWN"},
    {"id": "cost-null", "cost": None, "expect_ok": False, "max_dispatches": 1,
     "cost_status": "UNKNOWN"},
    {"id": "cost-negative", "cost": -1.0, "expect_ok": False,
     "max_dispatches": 1, "cost_status": "INVALID"},
    {"id": "cost-nan", "cost": float("nan"), "expect_ok": False,
     "max_dispatches": 1, "cost_status": "INVALID"},
    {"id": "cost-infinite", "cost": float("inf"), "expect_ok": False,
     "max_dispatches": 1, "cost_status": "INVALID"},
    {"id": "overcharge-on-zero-budget", "cost": 0.75, "expect_ok": False,
     "max_dispatches": 1},
    {"id": "model-substituted", "cost": 0.0, "model": "unapproved/model",
     "expect_ok": False, "max_dispatches": 1},
    {"id": "model-missing", "cost": 0.0, "model": None, "expect_ok": False,
     "max_dispatches": 1},
    {"id": "provider-raises", "raises": RuntimeError("upstream refused"),
     "expect_ok": False, "max_dispatches": 1},
    {"id": "empty-output", "cost": 0.0, "output": "", "expect_ok": False,
     "max_dispatches": 1},
)


class SharedAcceptanceMatrixTests(unittest.TestCase):
    """One contract, asserted identically on the direct and gateway paths."""

    def _assert_row(self, case, code, report, adapter, transport):
        label = "%s/%s" % (case["id"], transport)
        if case["expect_ok"]:
            self.assertEqual(code, 0, "%s should succeed" % label)
        else:
            self.assertNotEqual(code, 0, "%s must not report success" % label)
        self.assertLessEqual(adapter.call_count, case["max_dispatches"],
                             "%s dispatched too many times" % label)
        if case.get("cost_status") and report.get("calls"):
            self.assertEqual(report["calls"][0].get("cost_status"),
                             case["cost_status"], label)

    def test_the_matrix_holds_on_the_direct_transport(self):
        for case in MATRIX:
            with self.subTest(case=case["id"]):
                code, report, adapter = _direct(case)
                self._assert_row(case, code, report, adapter, "direct")

    def test_the_matrix_holds_on_the_gateway_transport(self):
        for case in MATRIX:
            with self.subTest(case=case["id"]):
                code, report, adapter = _gateway(case)
                self._assert_row(case, code, report, adapter, "gateway")

    def test_both_transports_agree_on_every_row(self):
        """Parity itself is the assertion: same input class, same verdict."""
        for case in MATRIX:
            with self.subTest(case=case["id"]):
                direct_code = _direct(case)[0]
                gateway_code = _gateway(case)[0]
                self.assertEqual(bool(direct_code), bool(gateway_code),
                                 "%s: direct exit %s but gateway exit %s"
                                 % (case["id"], direct_code, gateway_code))


class DiscoveryParsingBoundaryTests(unittest.TestCase):
    """The discovery parser itself, not a mock standing in for it.

    Every existing test replaced omniroute_models wholesale, so its own
    failure handling was never exercised. These drive the real function and
    only fake the subprocess it shells out to.
    """

    def _models(self, returncode=0, stdout="", stderr="", free_only=True,
                raises=None):
        import subprocess as sp

        def fake(argv, **kwargs):
            if raises is not None:
                raise raises
            return sp.CompletedProcess(argv, returncode, stdout=stdout,
                                       stderr=stderr)

        with patch.object(probe.subprocess, "run", side_effect=fake):
            return probe.omniroute_models(free_only=free_only)

    def test_a_failed_simulation_is_not_an_inventory(self):
        """Exit 1 stdout was parsed as a catalog, and the catalog gates dispatch."""
        self.assertIsNone(self._models(
            returncode=1, stdout="openrouter/vendor/ghost:free\n",
            stderr="fatal: gateway down"))

    def test_a_discovery_timeout_fails_safely_rather_than_crashing(self):
        import subprocess as sp
        self.assertIsNone(self._models(
            raises=sp.TimeoutExpired(["omniroute"], 120)))

    def test_a_missing_gateway_binary_fails_safely(self):
        self.assertIsNone(self._models(raises=OSError("no such executable")))

    def test_a_truncated_model_id_is_discarded_not_repaired(self):
        """The CLI elides long ids; the marker is evidence, not noise."""
        self.assertEqual(self._models(
            stdout="| openrouter/nvidia/nemotron-3.5-lig… |\n",
            free_only=False), [])

    def test_an_ordinary_catalog_line_still_parses(self):
        self.assertEqual(
            self._models(stdout="| 1 | openrouter | openrouter/test/model:free |\n"),
            ["openrouter/test/model:free"])

    def test_free_only_filters_priced_models(self):
        models = self._models(
            stdout="openrouter/a/paid-model\nopenrouter/b/free-model:free\n")
        self.assertEqual(models, ["openrouter/b/free-model:free"])


class GatewayResponseParsingTests(unittest.TestCase):
    """omniroute_chat's own footer parsing, driven for real."""

    def _chat(self, stdout="", stderr="", returncode=0, raises=None):
        import subprocess as sp

        def fake(argv, **kwargs):
            if raises is not None:
                raise raises
            return sp.CompletedProcess(argv, returncode, stdout=stdout,
                                       stderr=stderr)

        with patch.object(probe.subprocess, "run", side_effect=fake):
            return probe.omniroute_chat("openrouter/test/free:free", "hello")

    def test_the_resolved_model_is_read_from_the_footer(self):
        result = self._chat(stdout="the answer\n",
                            stderr="[openrouter/test/free:free · 812ms · 44 tok]\n")
        self.assertEqual(result["resolved_model"], "openrouter/test/free:free")
        self.assertEqual(result["total_tokens"], 44)
        self.assertEqual(result["text"], "the answer")

    def test_a_coloured_footer_still_parses(self):
        coloured = ("\x1b[36m[openrouter/test/free:free · 5ms · 7 tok]"
                    "\x1b[0m\n")
        result = self._chat(stdout="the answer\n", stderr=coloured)
        self.assertEqual(result["resolved_model"], "openrouter/test/free:free")

    def test_a_nonzero_exit_is_an_error_not_an_answer(self):
        result = self._chat(returncode=3, stderr="boom")
        self.assertTrue(result.get("error"))

    def test_a_timeout_is_reported_rather_than_raised(self):
        import subprocess as sp
        result = self._chat(raises=sp.TimeoutExpired(["omniroute"], 120))
        self.assertEqual(result.get("error"), "omniroute_timeout")

    def test_a_missing_footer_yields_no_resolved_model(self):
        result = self._chat(stdout="an answer with no provenance footer\n")
        self.assertIsNone(result.get("resolved_model"))
