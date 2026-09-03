"""Executable integration coverage for the mandatory PM OS use-case matrix."""

import unittest
from unittest.mock import patch

import pmos.usecases as usecases
from pmos.usecases import USE_CASE_IDS, UseCaseResult, run_all, run_use_case, validate_registry


class UseCaseMatrixTests(unittest.TestCase):
    def test_registry_is_exactly_the_mandatory_thirteen(self):
        expected = (
            "solo_manual", "ai_drafting", "concurrent_team", "portfolio", "regulated",
            "automation", "analytics_experiments", "research", "integrations", "migration",
            "disaster_recovery", "security", "new_user",
        )
        self.assertEqual(USE_CASE_IDS, expected)
        self.assertEqual(validate_registry(), expected)

    def test_every_registered_case_executes_and_returns_behavioral_evidence(self):
        results = run_all()
        self.assertEqual(tuple(result.use_case_id for result in results), USE_CASE_IDS)
        self.assertEqual(len(results), 13)
        for result in results:
            self.assertTrue(result.passed, result.use_case_id)
            self.assertGreaterEqual(len(result.assertions), 3, result.use_case_id)
            self.assertTrue(result.evidence, result.use_case_id)
            self.assertTrue(result._execution, result.use_case_id)

    def test_unknown_case_is_rejected(self):
        with self.assertRaises(ValueError):
            run_use_case("not-a-real-use-case")

    def test_self_attested_or_always_passing_stub_cannot_satisfy_matrix(self):
        """The registry verifies observed evidence independently of ``passed``.

        This is deliberately a mutation-style regression: the historic result
        factory accepted arbitrary text plus ``passed=True``.  A replacement
        implementation cannot restore that bypass by returning an object whose
        own ``passed`` property unconditionally claims success.
        """
        with self.assertRaisesRegex(AssertionError, "contract-checked"):
            usecases._result("solo_manual", "a", "b", "c", x=1)

        class AlwaysPassingResult(UseCaseResult):
            @property
            def passed(self):  # type: ignore[override]
                return True

        forged = AlwaysPassingResult(
            "solo_manual", usecases._CASE_ASSERTIONS["solo_manual"], {})
        self.assertTrue(forged.passed)
        replacement = dict(usecases._IMPLEMENTATIONS)
        replacement["solo_manual"] = lambda: forged
        with patch.object(usecases, "_IMPLEMENTATIONS", replacement):
            with self.assertRaisesRegex(AssertionError, "observed-evidence contract"):
                usecases.run_use_case("solo_manual")

        # A structurally perfect constant is still not behavioral evidence.
        # Mutate every implementation independently to return the exact values
        # its typed predicate accepts, while calling no PMOS API; the external
        # execution observer must reject all thirteen replacements.
        conforming = {
            "solo_manual": dict(product_id="fake", initiative_id="fake",
                                evidence_id="fake", trace_count=0, stage="define"),
            "ai_drafting": dict(model="deterministic-draft", decision_id="fake",
                                product_id="fake"),
            "concurrent_team": dict(assignment_id="fake", mention_id="fake"),
            "portfolio": dict(allocated_capacity=9.0, initiative_count=3,
                              product_count=2),
            "regulated": dict(product_id="fake", blocked_without_approval=True,
                              stage="build", changed_evidence_revision=1,
                              approval_status="invalidated"),
            "automation": dict(job_id="fake", status="succeeded"),
            "analytics_experiments": dict(metric_id="activation",
                                          experiment_id="fake", decision_id="fake"),
            "research": dict(evidence_id="fake", redacted=True),
            "integrations": dict(issue_id="fake", branch="feature/onboarding",
                                 external_id="external-event-1",
                                 outbox_status="acknowledged"),
            "migration": dict(status="migrated", backup_created=True,
                              runtime_verified=True, migrated_revision=1,
                              migrated_file_count=2),
            "disaster_recovery": dict(revision=1, verified=True),
            "security": dict(secret_action="deny", outside_action="deny",
                             external_action="ask"),
            "new_user": dict(cli_initialized=True, cli_completed=True,
                             store_verified=True, conductor_completed=True,
                             domain_reopened=True, hook_action="allow",
                             skill_contract_count=1,
                             operations_status="acknowledged"),
        }
        for case_id, evidence in conforming.items():
            with self.subTest(conforming_constant_stub=case_id):
                constant = dict(usecases._IMPLEMENTATIONS)
                constant[case_id] = (
                    lambda case_id=case_id, evidence=evidence:
                    usecases._observed(case_id, **evidence))
                with patch.object(usecases, "_IMPLEMENTATIONS", constant):
                    with self.assertRaisesRegex(AssertionError, "execution seam"):
                        usecases.run_use_case(case_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
