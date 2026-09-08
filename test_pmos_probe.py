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
