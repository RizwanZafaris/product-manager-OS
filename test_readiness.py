"""Adversarial regression tests for the readiness evaluator and registry.

These tests use temporary JSON documents and mocks.  They deliberately never
write a scorecard into the checkout and never allow a verifier subprocess to
run while testing rubric validation.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


REPO = Path(__file__).resolve().parent
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import readiness  # noqa: E402
from readiness_registry import Step  # noqa: E402


def valid_spec(*, verifier="os-tree", criterion_id="C-1", task=None):
    criterion = {
        "id": criterion_id,
        "title": "A criterion",
        "points": 100,
    }
    if verifier is not None:
        criterion["verifier"] = verifier
    else:
        criterion.update({"task": task or "T-1", "blocker": "not built"})
    return {
        "schema": 2,
        "title": "Test rubric",
        "note": "Temporary rubric",
        "categories": [{
            "id": "cat",
            "title": "Category",
            "points": 100,
            "criteria": [criterion],
        }],
    }


def valid_ledger(*, owns=("C-1",), task_id="T-1"):
    return {
        "schema": 2,
        "title": "Test ledger",
        "note": "Temporary ledger",
        "tasks": [{
            "id": task_id,
            "title": "A task",
            "status": "green",
            "owns": list(owns),
            "owns_hard_gates": [],
            "depends_on": [],
            "risk": "low",
            "outcome": "A test outcome",
            "scope": ["bounded fixture"],
            "non_goals": ["network calls"],
            "acceptance": "The fixed verifier passes.",
            "owned_files": ["test_readiness.py"],
            "failure_cases": ["verifier fails"],
            "executor_capabilities": ["deterministic-test"],
            "reviewer_capabilities": ["adversarial-review"],
            "acceptance_verifiers": ["os-tree"],
            "evidence_paths": ["test_readiness.py"],
            "attempt_count": 1,
            "last_failure_class": "none",
            "next_action": "monitor",
        }],
    }


class RubricValidationTests(unittest.TestCase):
    def assert_validation_error(self, spec, ledger, expected):
        errors = readiness.validate(spec, ledger)
        self.assertTrue(
            any(expected in error for error in errors),
            "expected %r in %r" % (expected, errors),
        )

    def score_temporary_rubric(self, spec, ledger, *, run_verifier=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            criteria = root / "criteria.json"
            tasks = root / "task-ledger.json"
            criteria.write_text(json.dumps(spec), encoding="utf-8")
            tasks.write_text(json.dumps(ledger), encoding="utf-8")
            verifier_patch = (patch.object(readiness, "run_verifier",
                                            run_verifier)
                              if run_verifier is not None else nullcontext())
            with patch.object(readiness, "CRITERIA", criteria), \
                    patch.object(readiness, "TASKS", tasks), verifier_patch:
                return readiness.score()

    def test_legacy_verify_shell_string_is_rejected_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "marker"
            spec = valid_spec()
            spec["categories"][0]["criteria"][0].pop("verifier")
            spec["categories"][0]["criteria"][0]["verify"] = (
                "python3 -c \"open(%r, 'w').write('executed')\"" % marker
            )
            run = Mock(side_effect=AssertionError("must not run"))
            report = self.score_temporary_rubric(spec, valid_ledger(),
                                                 run_verifier=run)
            self.assertTrue(any("unknown fields" in error
                                for error in report["rubric_errors"]))
            run.assert_not_called()
            self.assertFalse(marker.exists())

    def test_unknown_verifier_id_is_rejected_without_execution(self):
        spec = valid_spec(verifier="python3 -c 'touch marker'")
        run = Mock(side_effect=AssertionError("must not run"))
        report = self.score_temporary_rubric(spec, valid_ledger(),
                                             run_verifier=run)
        self.assertTrue(any("unknown verifier" in error
                            for error in report["rubric_errors"]))
        run.assert_not_called()

    def test_marker_file_injection_in_json_is_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "marker"
            spec = valid_spec(verifier="__import__('os').system('touch %s')"
                              % marker)
            report = self.score_temporary_rubric(spec, valid_ledger())
            self.assertTrue(report["rubric_errors"])
            self.assertFalse(marker.exists())

    def test_duplicate_criterion_ids_fail(self):
        spec = valid_spec()
        criteria = spec["categories"][0]["criteria"]
        criteria[0]["points"] = 50
        criteria.append({
            "id": "C-1",
            "title": "Another criterion",
            "points": 50,
            "verifier": "os-tree",
        })
        self.assert_validation_error(spec, valid_ledger(),
                                     "duplicate criterion id C-1")

    def test_category_criteria_sum_mismatch_fails(self):
        spec = valid_spec()
        spec["categories"][0]["criteria"][0]["points"] = 99
        self.assert_validation_error(spec, valid_ledger(),
                                     "allocates 100 points but its criteria sum to 99")

    def test_non_100_total_fails(self):
        spec = valid_spec()
        spec["categories"][0]["points"] = 99
        spec["categories"][0]["criteria"][0]["points"] = 99
        self.assert_validation_error(spec, valid_ledger(),
                                     "exactly 100 points")

    def test_unknown_fields_fail_at_each_rubric_level(self):
        cases = []
        spec = valid_spec()
        spec["unexpected"] = True
        cases.append((spec, valid_ledger(), "unknown top-level fields"))

        spec = valid_spec()
        spec["categories"][0]["unexpected"] = True
        cases.append((spec, valid_ledger(), "unknown fields"))

        spec = valid_spec()
        spec["categories"][0]["criteria"][0]["unexpected"] = True
        cases.append((spec, valid_ledger(), "unknown fields"))

        spec = valid_spec()
        ledger = valid_ledger()
        ledger["tasks"][0]["unexpected"] = True
        cases.append((spec, ledger, "unknown fields"))

        for candidate, ledger, expected in cases:
            with self.subTest(expected=expected):
                self.assert_validation_error(candidate, ledger, expected)

    def test_unknown_criterion_owned_by_task_fails(self):
        self.assert_validation_error(
            valid_spec(),
            valid_ledger(owns=("C-1", "C-unknown")),
            "owns unknown criterion C-unknown",
        )

    def test_criterion_naming_unknown_task_fails(self):
        spec = valid_spec(verifier=None, task="T-missing")
        self.assert_validation_error(spec, valid_ledger(),
                                     "names unknown task T-missing")

    def test_missing_task_ownership_fails(self):
        spec = valid_spec(verifier=None)
        self.assert_validation_error(spec, valid_ledger(owns=()),
                                     "does not declare ownership of C-1")

    def test_task_owning_nothing_fails(self):
        self.assert_validation_error(valid_spec(), valid_ledger(owns=()),
                                     "owns neither criteria nor hard gates")

    def test_legacy_task_ledger_schema_is_rejected(self):
        ledger = valid_ledger()
        ledger["schema"] = 1
        self.assert_validation_error(valid_spec(), ledger,
                                     "task ledger schema must be 2")

    def test_task_dependency_cycle_is_rejected(self):
        ledger = valid_ledger()
        ledger["tasks"][0]["depends_on"] = ["T-2"]
        second = dict(ledger["tasks"][0])
        second.update({"id": "T-2", "owns": [],
                       "owns_hard_gates": ["local_review_record_complete"],
                       "depends_on": ["T-1"]})
        ledger["tasks"].append(second)
        self.assert_validation_error(valid_spec(), ledger,
                                     "dependency graph contains a cycle")

    def test_external_policy_cannot_self_attest(self):
        policy = json.loads(readiness.EXTERNAL_GATES.read_text(
            encoding="utf-8"))
        policy["gates"][0]["status"] = "verified"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "external.json"
            path.write_text(json.dumps(policy), encoding="utf-8")
            _rows, errors = readiness.external_requirements(path)
        self.assertTrue(any("cannot self-attest" in error
                            for error in errors))


class VerifierExecutionTests(unittest.TestCase):
    def run_mocked(self, output, *, tests=("pkg.Case.test_expected",),
                   exit_code=0):
        registry = {"fixture": (Step(("python3", "-c", "ignored"),
                                      tests=tests),)}
        completed = SimpleNamespace(returncode=exit_code, stdout=output,
                                    stderr="")
        with patch.object(readiness, "REGISTRY", registry), \
                patch.object(readiness.subprocess, "run",
                             return_value=completed) as run:
            passed, _seconds, rows = readiness.run_verifier("fixture")
        return passed, rows[0], run

    def test_run_verifier_uses_argv_and_shell_false(self):
        completed = SimpleNamespace(returncode=0, stdout="ok", stderr="")
        step = Step(("python3", "tools/check.py", "--name", "value"))
        with patch.object(readiness, "REGISTRY", {"fixture": (step,)}), \
                patch.object(readiness.subprocess, "run",
                             return_value=completed) as run:
            passed, _seconds, _rows = readiness.run_verifier("fixture")
        self.assertTrue(passed)
        argv = run.call_args.args[0]
        self.assertIsInstance(argv, list)
        self.assertEqual(argv, [sys.executable, "tools/check.py", "--name",
                                "value"])
        self.assertIs(run.call_args.kwargs["shell"], False)

    def test_zero_test_evidence_fails(self):
        passed, row, _run = self.run_mocked("Ran 0 tests in 0.001s\nOK")
        self.assertFalse(passed)
        self.assertIn("expected 1 exact tests", row["evidence_error"])

    def test_missing_test_id_evidence_fails(self):
        output = "test_other (pkg.Case) ... ok\n\nRan 1 test in 0.001s\nOK"
        passed, row, _run = self.run_mocked(output)
        self.assertFalse(passed)
        self.assertIn("missing exact test evidence", row["evidence_error"])

    def test_skip_evidence_fails(self):
        output = ("test_expected (pkg.Case) ... skipped 'not ready'\n\n"
                  "Ran 1 test in 0.001s\nOK (skipped=1)")
        passed, row, _run = self.run_mocked(output)
        self.assertFalse(passed)
        self.assertIn("forbidden", row["evidence_error"])

    def test_expected_failure_evidence_fails(self):
        output = ("test_expected (pkg.Case) ... expected failure\n\n"
                  "Ran 1 test in 0.001s\nOK (expected failures=1)")
        passed, row, _run = self.run_mocked(output)
        self.assertFalse(passed)
        self.assertIn("forbidden", row["evidence_error"])

    def test_wrong_test_count_evidence_fails(self):
        tests = ("pkg.Case.test_expected", "pkg.Case.test_second")
        output = "test_expected (pkg.Case) ... ok\n\nRan 1 test in 0.001s\nOK"
        passed, row, _run = self.run_mocked(output, tests=tests)
        self.assertFalse(passed)
        self.assertIn("expected 2 exact tests", row["evidence_error"])


class VerdictAndOutputTests(unittest.TestCase):
    def test_category_verdict_is_diagnostic_and_never_complete(self):
        spec = valid_spec(verifier="fixture")
        ledger = valid_ledger()

        def fake_git(*args):
            return "" if args and args[0] == "status" else "d" * 40

        with tempfile.TemporaryDirectory() as directory:
            criteria = Path(directory) / "criteria.json"
            tasks = Path(directory) / "task-ledger.json"
            criteria.write_text(json.dumps(spec), encoding="utf-8")
            tasks.write_text(json.dumps(ledger), encoding="utf-8")
            with patch.object(readiness, "CRITERIA", criteria), \
                    patch.object(readiness, "TASKS", tasks), \
                    patch.object(readiness, "REGISTRY", {"fixture": (Step(("true",)),)}), \
                    patch.object(readiness, "run_verifier",
                                 return_value=(True, 0.0, [])), \
                patch.object(readiness, "git", side_effect=fake_git), \
                patch.object(readiness.subprocess, "run",
                             return_value=SimpleNamespace(returncode=0,
                                                          stdout="", stderr="")):
                report = readiness.score("cat")

        self.assertEqual(report["scope"], "category-diagnostic")
        self.assertTrue(report["verdict"].startswith("CATEGORY DIAGNOSTIC:"))
        self.assertFalse(report["complete_readiness"])

    def test_local_100_still_reports_external_readiness_as_blocked(self):
        spec = valid_spec(verifier="fixture")
        ledger = valid_ledger()
        ledger["tasks"][0]["acceptance_verifiers"] = ["fixture"]

        def fake_git(*args):
            return "" if args and args[0] == "status" else "d" * 40

        with tempfile.TemporaryDirectory() as directory:
            criteria = Path(directory) / "criteria.json"
            tasks = Path(directory) / "task-ledger.json"
            criteria.write_text(json.dumps(spec), encoding="utf-8")
            tasks.write_text(json.dumps(ledger), encoding="utf-8")
            with patch.object(readiness, "CRITERIA", criteria), \
                    patch.object(readiness, "TASKS", tasks), \
                    patch.object(readiness, "REGISTRY", {
                        "fixture": (Step(("true",)),)}), \
                    patch.object(readiness, "LOCAL_HARD_GATE_VERIFIERS", {
                        "fixture_gate": ("fixture",)}), \
                    patch.object(readiness, "run_verifier",
                                 return_value=(True, 0.0, [])), \
                    patch.object(readiness, "git", side_effect=fake_git):
                report = readiness.score()

        self.assertTrue(report["local_engineering_readiness"])
        self.assertFalse(report["external_readiness"])
        self.assertFalse(report["complete_readiness"])
        self.assertIn("LOCAL ENGINEERING READINESS 100/100",
                      report["verdict"])

    def test_non_point_bearing_hard_gate_is_executed_and_can_be_green(self):
        spec = valid_spec(verifier="fixture")
        ledger = valid_ledger()
        ledger["tasks"][0]["acceptance_verifiers"] = ["fixture"]
        calls = []

        def fake_git(*args):
            return "" if args and args[0] == "status" else "d" * 40

        def fake_verifier(verifier_id):
            calls.append(verifier_id)
            return True, 0.0, []

        with tempfile.TemporaryDirectory() as directory:
            criteria = Path(directory) / "criteria.json"
            tasks = Path(directory) / "task-ledger.json"
            criteria.write_text(json.dumps(spec), encoding="utf-8")
            tasks.write_text(json.dumps(ledger), encoding="utf-8")
            with patch.object(readiness, "CRITERIA", criteria), \
                    patch.object(readiness, "TASKS", tasks), \
                    patch.object(readiness, "REGISTRY", {
                        "fixture": (Step(("true",)),),
                        "hidden-hard-gate": (Step(("true",)),),
                    }), \
                    patch.object(readiness, "LOCAL_HARD_GATE_VERIFIERS", {
                        "hidden_gate": ("hidden-hard-gate",),
                    }), \
                    patch.object(readiness, "run_verifier",
                                 side_effect=fake_verifier), \
                    patch.object(readiness, "git", side_effect=fake_git):
                report = readiness.score()

        self.assertEqual(calls, ["fixture", "hidden-hard-gate"])
        self.assertTrue(report["hard_gates"]["hidden_gate"])
        self.assertTrue(report["local_engineering_readiness"])

    def test_git_failure_never_looks_like_a_clean_exact_tree(self):
        spec = valid_spec(verifier="fixture")
        ledger = valid_ledger()
        ledger["tasks"][0]["acceptance_verifiers"] = ["fixture"]

        with tempfile.TemporaryDirectory() as directory:
            criteria = Path(directory) / "criteria.json"
            tasks = Path(directory) / "task-ledger.json"
            criteria.write_text(json.dumps(spec), encoding="utf-8")
            tasks.write_text(json.dumps(ledger), encoding="utf-8")
            with patch.object(readiness, "CRITERIA", criteria), \
                    patch.object(readiness, "TASKS", tasks), \
                    patch.object(readiness, "REGISTRY", {
                        "fixture": (Step(("true",)),),
                    }), \
                    patch.object(readiness, "LOCAL_HARD_GATE_VERIFIERS", {
                        "fixture_gate": ("fixture",),
                    }), \
                    patch.object(readiness, "run_verifier",
                                 return_value=(True, 0.0, [])), \
                    patch.object(readiness, "git", return_value=None):
                report = readiness.score()

        self.assertFalse(report["tree"]["git_available"])
        self.assertFalse(report["hard_gates"]["tree_clean_and_stable"])
        self.assertFalse(report["local_engineering_readiness"])

    def test_output_path_rejects_unignored_repository_path(self):
        with self.assertRaises(readiness.ReadinessError):
            readiness.output_path(REPO / "test_readiness-scorecard.json")

    def test_output_path_permits_external_temp_path(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "scorecard.json"
            self.assertEqual(readiness.output_path(candidate), candidate.resolve())


if __name__ == "__main__":
    unittest.main()
