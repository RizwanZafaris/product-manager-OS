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

TOOLS = Path(__file__).resolve().parent.parent / "tools"
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
                probe, "gateway_catalog",
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
        source = Path(__file__).resolve().parent.parent / "skills"
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

    def test_the_gateway_may_answer_with_the_provider_spelling(self):
        """openrouter/<id> pinned, <id> answered: one model, two hops' spellings."""
        code, report, adapter = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer", "cost_usd": 0.0,
                                   "resolved_model": "test/free:free"}})
        self.assertEqual(adapter.call_count, 1)
        self.assertFalse(report["calls"][0].get("error"))
        self.assertEqual(code, 0)

    def test_dropping_the_free_suffix_is_still_a_substitution(self):
        """The paid twin of a free model is a different model."""
        code, report, _ = run_probe(
            ["--via", "omniroute", "--model", "openrouter/test/free:free",
             "--max-calls", "1"],
            omni={"return_value": {"text": "answer", "cost_usd": 0.0,
                                   "resolved_model": "test/free"}})
        self.assertEqual(report["calls"][0].get("error"), "resolved_model_mismatch")
        self.assertNotEqual(code, 0)

    def test_same_gateway_model_accepts_exactly_two_spellings(self):
        same = probe.same_gateway_model
        self.assertTrue(same("openrouter/v/m:free", "openrouter/v/m:free"))
        self.assertTrue(same("openrouter/v/m:free", "v/m:free"))
        self.assertFalse(same("openrouter/v/m:free", "v/m"))
        self.assertFalse(same("openrouter/v/m:free", "other/v/m:free"))
        self.assertFalse(same("openrouter/v/m:free", ""))
        self.assertFalse(same("openrouter/v/m:free", None))
        self.assertFalse(same("v/m:free", "openrouter/v/m:free"))

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


class ProvenanceErrorsStillBillTests(unittest.TestCase):
    """The run loop's aggregate must carry a charge the gateway reported even
    when the answer it bought was refused as evidence. Found by the third
    independent review round: cache hit, compression and identity conflict
    each aggregated to $0.00 with cost_unknown false against a 0.75 charge.
    """

    def _run(self, omni_result):
        return run_probe(["--via", "omniroute", "--max-calls", "2"],
                         omni={"return_value": omni_result})

    def test_a_cache_replay_with_a_charge_breaches_a_zero_budget(self):
        code, report, adapter = self._run(
            {"error": "cached_response", "error_detail": "replayed",
             "cost_usd": 0.75, "cost_source": "gateway header"})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["cost_usd"], 0.75)
        self.assertEqual(report["calls"][0]["cost_basis"], "gateway header")
        self.assertEqual(report["totals"]["cost_usd"], 0.75)
        self.assertTrue(report["totals"]["budget_breach"])
        self.assertEqual(adapter.call_count, 1, "a breach must stop the run")

    def test_a_substituted_model_with_a_charge_is_still_billed(self):
        code, report, adapter = self._run(
            {"text": "answer", "resolved_model": "other/model",
             "cost_usd": 0.75, "cost_source": "provider usage.cost"})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["error"], "resolved_model_mismatch")
        self.assertEqual(report["calls"][0]["cost_usd"], 0.75)
        self.assertEqual(report["totals"]["cost_usd"], 0.75)
        self.assertTrue(report["totals"]["budget_breach"])

    def test_a_missing_resolved_model_with_a_charge_is_still_billed(self):
        code, report, _ = self._run(
            {"text": "answer", "cost_usd": 0.75, "cost_source": "gateway header"})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["error"], "missing_resolved_model")
        self.assertEqual(report["totals"]["cost_usd"], 0.75)
        self.assertTrue(report["totals"]["budget_breach"])


class BodyCostTypingReachesTheRunLoopTests(unittest.TestCase):
    """The end-to-end shape of the fourth round's P1: a provider body cost
    of "0" (string) or True must fail the run as INVALID, never pass as OK."""

    def _gateway(self, cost):
        return run_probe(["--via", "omniroute", "--max-calls", "2"],
                         omni={"return_value": {
                             "text": "answer", "cost_usd": cost,
                             "cost_source": "provider usage.cost",
                             "resolved_model": "openrouter/test/free:free"}})

    def test_a_numeric_string_body_cost_is_invalid_not_ok(self):
        code, report, adapter = self._gateway("0")
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["cost_status"], "INVALID")
        self.assertEqual(adapter.call_count, 1)

    def test_a_bool_body_cost_is_invalid_not_a_dollar(self):
        code, report, _ = self._gateway(True)
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["cost_status"], "INVALID")
        self.assertNotEqual(report["totals"]["cost_usd"], 1.0)


class ErrorsWithoutBillingAreUnknownTests(unittest.TestCase):
    """Fourth review round, P2: an errored call the gateway said nothing
    about aggregated as cost_usd 0.0 with cost_unknown false. Silence about
    money is not $0.00, on either transport."""

    def test_a_gateway_error_with_no_cost_makes_the_aggregate_unknown(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--max-calls", "2"],
            omni={"return_value": {"error": "cached_response",
                                   "error_detail": "replayed"}})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["cost_status"], "UNKNOWN")
        self.assertTrue(report["totals"]["cost_unknown"])

    def test_a_direct_adapter_exception_makes_the_aggregate_unknown(self):
        code, report, _ = run_probe(
            ["--max-calls", "2"],
            complete={"side_effect": RuntimeError("upstream refused")})
        self.assertNotEqual(code, 0)
        self.assertEqual(report["calls"][0]["cost_status"], "UNKNOWN")
        self.assertTrue(report["totals"]["cost_unknown"])

    def test_a_refusal_before_any_request_is_not_an_unknown_charge(self):
        code, report, _ = run_probe(
            ["--via", "omniroute", "--max-calls", "1"],
            omni={"return_value": {"error": "omniroute_not_local",
                                   "error_detail": "must be loopback"}})
        self.assertNotEqual(code, 0)
        self.assertFalse(report["totals"]["cost_unknown"])


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

    def test_the_gateway_call_has_a_finite_timeout(self):
        seen = {}

        def record(request, timeout=None):
            seen["timeout"] = timeout
            return _GatewayResponse(b'{"model": "test/free:free", "choices": []}')

        probe.omniroute_chat("openrouter/test/free:free", "hello", urlopen=record,
                             environ={})
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
        """A gateway answer carrying neither a provider cost nor a cost header
        yields no cost_usd at all; that absence must read as UNKNOWN."""
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
        seen = {}

        def record(self, path, **kwargs):
            seen.update(kwargs)
            return {"data": []}

        with patch.object(OpenRouterProvider, "_json_request", record):
            probe.gateway_catalog(free_only=True)
        self.assertIsNotNone(seen.get("timeout_seconds"))
        self.assertGreater(seen["timeout_seconds"], 0)

    def test_gateway_discovery_reads_no_credential(self):
        """The catalog is public. Discovery must not need, read or send a key.

        Asserted at the transport, not one layer up. A first version of this
        test faked ``_json_request`` and passed while the real adapter still
        resolved a credential inside that very method and refused keyless
        discovery outright -- the fake had hidden the defect it was written to
        catch. Here the real request path runs and only the socket is faked.
        """
        seen = {}

        class Response:
            status = 200

            def read(self, n=-1):
                return b'{"data": []}'

            def geturl(self):
                return "https://openrouter.ai/api/v1/models"

            def close(self):
                pass

        def transport(request, timeout=None):
            seen["headers"] = {k.lower(): v for k, v in request.header_items()}
            seen["url"] = request.full_url
            return Response()

        provider = OpenRouterProvider(urlopen=transport)
        with patch.dict(probe.os.environ, {"OPENROUTER_API_KEY": "must-not-be-read"}), \
                patch.object(OpenRouterProvider, "_credential",
                             side_effect=AssertionError("discovery read a credential")), \
                patch.object(probe, "OpenRouterProvider", return_value=provider,
                             create=True), \
                patch("pmos.openrouter.OpenRouterProvider", return_value=provider):
            self.assertEqual(probe.gateway_catalog(free_only=True), [])
        self.assertNotIn("authorization", seen["headers"])
        self.assertTrue(seen["url"].endswith("/api/v1/models"))

    def test_anonymous_mode_is_refused_for_generation(self):
        """Anonymous is a catalog-only privilege; a keyless chat is not attempted."""
        from pmos.openrouter import OpenRouterAuthError
        calls = []
        provider = OpenRouterProvider(urlopen=lambda *a, **k: calls.append(a))
        with self.assertRaises(OpenRouterAuthError):
            provider._json_request("/api/v1/chat/completions", method="POST",
                                   payload={}, anonymous=True)
        self.assertEqual(calls, [])

    def test_default_discovery_still_requires_the_credential(self):
        """The direct transport's contract is unchanged: no key, no discovery."""
        from pmos.openrouter import OpenRouterAuthMissing
        calls = []
        provider = OpenRouterProvider(urlopen=lambda *a, **k: calls.append(a),
                                      environ={})
        with self.assertRaises(OpenRouterAuthMissing):
            provider.discover(free_only=True)
        self.assertEqual(calls, [])


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


class DiscoveryCatalogBoundaryTests(unittest.TestCase):
    """The gateway catalog itself, not a mock standing in for it.

    Replaces the tests that drove the `omniroute simulate` parser, which was
    retired on 2026-09-09: the router's dry run prints the `auto` combo's
    fallback table whatever model is pinned, so it could not confirm a pinned
    id and, on the day it was replaced, listed a model OpenRouter had withdrawn
    from the free tier while surfacing none that was free. These drive the real
    function and fake only the HTTP boundary beneath the adapter, which is the
    same boundary every other test in this file already prohibits.
    """

    def _catalog(self, payload=None, free_only=True, raises=None):
        def fake(self, path, **kwargs):
            if raises is not None:
                raise raises
            return payload

        with patch.object(OpenRouterProvider, "_json_request", fake):
            return probe.gateway_catalog(free_only=free_only)

    @staticmethod
    def _entry(model, prompt="0", completion="0"):
        return {"id": model, "context_length": 4096,
                "pricing": {"prompt": prompt, "completion": completion},
                "supported_parameters": [], "architecture": {}}

    def test_a_transport_error_is_not_an_inventory(self):
        """An unreadable catalog must read as unknown, never as empty."""
        from pmos.openrouter import OpenRouterError
        self.assertIsNone(self._catalog(raises=OpenRouterError()))

    def test_a_discovery_timeout_fails_safely_rather_than_crashing(self):
        self.assertIsNone(self._catalog(raises=TimeoutError("catalog timed out")))

    def test_an_unreachable_provider_fails_safely(self):
        self.assertIsNone(self._catalog(raises=OSError("network unreachable")))

    def test_a_malformed_catalog_is_not_an_inventory(self):
        """A body that is not a catalog is unknown, not empty."""
        self.assertIsNone(self._catalog(payload={"data": "not a list"}))
        self.assertIsNone(self._catalog(payload={"data": [{"no": "id"}]}))

    def test_a_priceless_row_is_never_free(self):
        """A row without prices is dropped; it is not evidence of anything.

        The provider's own catalog carries five meta-router rows priced "-1",
        and a row with no price at all is the same case: it cannot be selected,
        cannot be called free, and cannot invalidate the priced rows beside it.
        """
        self.assertEqual(self._catalog(payload={"data": [
            {"id": "vendor/priceless", "context_length": 1, "pricing": {},
             "supported_parameters": [], "architecture": {}},
            self._entry("openrouter/auto", prompt="-1", completion="-1"),
        ]}), [])

    def test_free_is_decided_by_the_provider_price_not_the_name(self):
        """A ':free' suffix on a priced model is a name; the price decides."""
        models = self._catalog(payload={"data": [
            self._entry("a/looks-free:free", prompt="0.000001", completion="0"),
            self._entry("b/is-free"),
        ]})
        self.assertEqual(models, ["openrouter/b/is-free"])

    def test_free_only_off_keeps_priced_models(self):
        models = self._catalog(payload={"data": [
            self._entry("a/paid", prompt="0.001", completion="0.002"),
            self._entry("b/free"),
        ]}, free_only=False)
        self.assertEqual(models, ["openrouter/a/paid", "openrouter/b/free"])

    def test_an_empty_catalog_is_empty_not_failed(self):
        """Distinct from failure: the provider answered and prices nothing at zero."""
        self.assertEqual(self._catalog(payload={"data": []}), [])

    def test_catalog_ids_carry_the_gateway_prefix(self):
        """The gateway is asked for openrouter/<id>; membership must match it."""
        self.assertEqual(self._catalog(payload={"data": [self._entry("v/m:free")]}),
                         ["openrouter/v/m:free"])


class _GatewayResponse:
    """A minimal stand-in for what urlopen returns from the loopback gateway."""

    def __init__(self, body=b"", headers=None, status=200):
        self._body = body
        self.headers = dict(headers or {})
        self.status = status

    def read(self, n=-1):
        return self._body if n is None or n < 0 else self._body[:n]

    def close(self):
        pass


def _ok_body(model="test/free:free", text="the answer", usage=None):
    import json as _json
    payload = {"model": model,
               "choices": [{"message": {"role": "assistant", "content": text}}],
               "usage": usage if usage is not None else
               {"prompt_tokens": 20, "completion_tokens": 24, "total_tokens": 44}}
    return _json.dumps(payload).encode("utf-8")


class GatewayHttpBoundaryTests(unittest.TestCase):
    """omniroute_chat over the loopback HTTP API, driven for real.

    Replaces the footer-parsing tests retired on 2026-09-09 with the CLI path
    they covered. Only the socket is faked; headers, body parsing, provenance
    checks and cost sourcing are the real code.
    """

    def _chat(self, body=None, headers=None, raises=None, environ=None,
              model="openrouter/test/free:free"):
        seen = {}

        def fake(request, timeout=None):
            seen["request"] = request
            seen["headers"] = {k.lower(): v for k, v in request.header_items()}
            seen["body"] = request.data
            if raises is not None:
                raise raises
            return _GatewayResponse(body if body is not None else _ok_body(),
                                    headers or {})

        result = probe.omniroute_chat(model, "hello", urlopen=fake,
                                      environ={} if environ is None else environ)
        return result, seen

    def test_doctrine_headers_are_sent_on_every_call(self):
        """routing/README.md: compression off, no cache, no memory, every time."""
        _result, seen = self._chat()
        self.assertEqual(seen["headers"].get("x-omniroute-compression"), "off")
        self.assertEqual(seen["headers"].get("x-omniroute-no-cache"), "true")
        self.assertEqual(seen["headers"].get("x-omniroute-no-memory"), "true")

    def test_the_request_is_pinned_and_asks_for_usage(self):
        import json as _json
        _result, seen = self._chat()
        sent = _json.loads(seen["body"])
        self.assertEqual(sent["model"], "openrouter/test/free:free")
        self.assertEqual(sent["usage"], {"include": True})
        self.assertGreater(sent["max_tokens"], 0)
        self.assertFalse(sent.get("stream"))

    def test_the_resolved_model_is_read_from_the_body(self):
        result, _ = self._chat(body=_ok_body(model="test/free:free"))
        self.assertEqual(result["resolved_model"], "test/free:free")
        self.assertEqual(result["total_tokens"], 44)
        self.assertEqual(result["text"], "the answer")

    def test_body_and_header_must_name_the_same_model(self):
        result, _ = self._chat(body=_ok_body(model="test/free:free"),
                               headers={"X-OmniRoute-Model": "other/model"})
        self.assertEqual(result.get("error"), "resolved_model_conflict")

    def test_a_cache_replay_is_not_evidence(self):
        result, _ = self._chat(headers={"X-OmniRoute-Cache": "HIT"})
        self.assertEqual(result.get("error"), "cached_response")
        result, _ = self._chat(headers={"X-OmniRoute-Cache-Hit": "true"})
        self.assertEqual(result.get("error"), "cached_response")

    def test_a_compressed_prompt_is_not_evidence(self):
        result, _ = self._chat(headers={"X-OmniRoute-Compression": "on; ratio=0.6"})
        self.assertEqual(result.get("error"), "compressed_prompt")
        result, _ = self._chat(headers={"X-OmniRoute-Compression": "off; source=request-header"})
        self.assertFalse(result.get("error"))

    def test_provider_cost_is_preferred_over_the_gateway_header(self):
        result, _ = self._chat(
            body=_ok_body(usage={"prompt_tokens": 1, "completion_tokens": 1,
                                 "total_tokens": 2, "cost": 0.0}),
            headers={"X-OmniRoute-Response-Cost": "0.5"})
        self.assertEqual(result["cost_usd"], 0.0)
        self.assertIn("provider", result["cost_source"])

    def test_the_gateway_cost_header_is_carried_and_labelled(self):
        result, _ = self._chat(headers={"X-OmniRoute-Response-Cost": "0.0000000000"})
        self.assertEqual(result["cost_usd"], 0.0)
        self.assertIn("gateway", result["cost_source"])

    def test_no_cost_anywhere_means_no_cost_key(self):
        result, _ = self._chat()
        self.assertNotIn("cost_usd", result)

    def test_an_unparseable_cost_header_is_not_a_cost(self):
        result, _ = self._chat(headers={"X-OmniRoute-Response-Cost": "n/a"})
        self.assertNotIn("cost_usd", result)

    def test_an_http_error_is_an_error_not_an_answer(self):
        import urllib.error
        err = urllib.error.HTTPError("http://localhost:20128/v1/chat/completions",
                                     404, "Not Found", {},
                                     io.BytesIO(b'{"error": {"message": "gone"}}'))
        result, _ = self._chat(raises=err)
        self.assertEqual(result.get("error"), "omniroute_http_404")
        self.assertEqual(result.get("error_detail"), "gone")

    def test_a_timeout_is_reported_rather_than_raised(self):
        import socket
        result, _ = self._chat(raises=socket.timeout("timed out"))
        self.assertEqual(result.get("error"), "omniroute_timeout")

    def test_a_refused_connection_is_unavailable(self):
        import urllib.error
        result, _ = self._chat(raises=urllib.error.URLError(OSError(61, "refused")))
        self.assertEqual(result.get("error"), "omniroute_unavailable")

    def test_a_non_json_body_is_malformed(self):
        result, _ = self._chat(body=b"<html>oops</html>")
        self.assertEqual(result.get("error"), "omniroute_malformed_response")

    def test_an_error_body_is_an_error(self):
        result, _ = self._chat(body=b'{"error": {"message": "cooling down"}}')
        self.assertEqual(result.get("error"), "omniroute_error")

    def test_an_oversize_body_is_refused(self):
        result, _ = self._chat(body=b"x" * (probe.GATEWAY_MAX_RESPONSE_BYTES + 1))
        self.assertEqual(result.get("error"), "omniroute_response_too_large")

    def test_a_missing_model_yields_no_resolved_model(self):
        result, _ = self._chat(body=b'{"choices": [{"message": {"content": "x"}}]}')
        self.assertIsNone(result.get("resolved_model"))

    # -- billing survives every judgement about the answer ------------------
    # Third review round: a body carrying usage.cost 0.75 with a cache hit,
    # then with compression on, then with a body/header model disagreement,
    # was refused as evidence each time and each time returned before the
    # cost was read, so the run aggregated $0.00 against a reported charge.

    def test_a_reported_charge_survives_a_cache_replay_error(self):
        result, _ = self._chat(
            body=_ok_body(usage={"prompt_tokens": 1, "completion_tokens": 1,
                                 "total_tokens": 2, "cost": 0.75}),
            headers={"X-OmniRoute-Cache": "HIT"})
        self.assertEqual(result.get("error"), "cached_response")
        self.assertEqual(result.get("cost_usd"), 0.75)

    def test_a_reported_charge_survives_a_compression_error(self):
        result, _ = self._chat(headers={"X-OmniRoute-Compression": "on",
                                        "X-OmniRoute-Response-Cost": "0.75"})
        self.assertEqual(result.get("error"), "compressed_prompt")
        self.assertEqual(result.get("cost_usd"), 0.75)
        self.assertIn("gateway", result.get("cost_source", ""))

    def test_a_reported_charge_survives_a_model_conflict(self):
        result, _ = self._chat(body=_ok_body(model="test/free:free"),
                               headers={"X-OmniRoute-Model": "other/model",
                                        "X-OmniRoute-Response-Cost": "0.75"})
        self.assertEqual(result.get("error"), "resolved_model_conflict")
        self.assertEqual(result.get("cost_usd"), 0.75)

    def test_a_reported_charge_survives_an_error_body(self):
        result, _ = self._chat(body=b'{"error": {"message": "cooling down"}}',
                               headers={"X-OmniRoute-Response-Cost": "0.25"})
        self.assertEqual(result.get("error"), "omniroute_error")
        self.assertEqual(result.get("cost_usd"), 0.25)

    def test_a_reported_charge_survives_an_http_error(self):
        import urllib.error
        from email.message import Message
        hdrs = Message(); hdrs["X-OmniRoute-Response-Cost"] = "0.5"
        err = urllib.error.HTTPError("http://localhost:20128/v1/chat/completions",
                                     402, "Payment Required", hdrs,
                                     io.BytesIO(b'{"error": {"message": "billed"}}'))
        result, _ = self._chat(raises=err)
        self.assertEqual(result.get("error"), "omniroute_http_402")
        self.assertEqual(result.get("cost_usd"), 0.5)

    def test_a_string_body_cost_is_handed_on_untyped_for_usable_cost_to_judge(self):
        """Fourth review round, P1: "0" in the body became 0.0 before
        usable_cost could call a numeric string INVALID, so a value the
        contract rejects passed as OK. The helper no longer types the body."""
        result, _ = self._chat(body=_ok_body(usage={"prompt_tokens": 1,
                                                    "completion_tokens": 1,
                                                    "total_tokens": 2,
                                                    "cost": "0"}))
        self.assertEqual(result.get("cost_usd"), "0")
        self.assertEqual(probe.usable_cost(result["cost_usd"])[1], "INVALID")

    def test_a_bool_body_cost_is_handed_on_untyped_too(self):
        result, _ = self._chat(body=_ok_body(usage={"prompt_tokens": 1,
                                                    "completion_tokens": 1,
                                                    "total_tokens": 2,
                                                    "cost": True}))
        self.assertIs(result.get("cost_usd"), True)
        self.assertEqual(probe.usable_cost(result["cost_usd"])[1], "INVALID")

    def test_no_charge_reported_means_no_cost_key_on_errors_too(self):
        result, _ = self._chat(headers={"X-OmniRoute-Cache": "HIT"})
        self.assertEqual(result.get("error"), "cached_response")
        self.assertNotIn("cost_usd", result)

    def test_a_remote_gateway_is_refused_before_any_call(self):
        calls = []
        result = probe.omniroute_chat(
            "openrouter/test/free:free", "hello",
            urlopen=lambda *a, **k: calls.append(a),
            environ={"OMNIROUTE_BASE_URL": "https://gateway.example.com/v1"})
        self.assertEqual(result.get("error"), "omniroute_not_local")
        self.assertEqual(calls, [])

    def test_the_gateway_key_is_sent_but_a_provider_key_is_never_read(self):
        _result, seen = self._chat(environ={"OMNIROUTE_API_KEY": "gw-key",
                                            "OPENROUTER_API_KEY": "provider-key"})
        self.assertEqual(seen["headers"].get("authorization"), "Bearer gw-key")
        self.assertNotIn(b"provider-key", seen["body"])
        for value in seen["headers"].values():
            self.assertNotIn("provider-key", value)
