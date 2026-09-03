"""Contract tests for the standard-library PMOS operations seam."""

import threading
import unittest
from unittest.mock import patch

from pmos.operations import (
    AdoptionObserver,
    AnalyticsAdapter,
    ContractViolation,
    ConsentError,
    DataValidationError,
    DecisionRef,
    ExperimentRef,
    IdempotencyConflict,
    IssueTrackingAdapter,
    NotificationAdapter,
    OutboxError,
    OutboxStatus,
    QuoteRefused,
    ResearchStorageAdapter,
    SourceControlAdapter,
    TransactionalOutbox,
    validate_adapter,
)


class AdapterContractTests(unittest.TestCase):
    def test_all_five_in_memory_adapters_share_versioned_contract(self):
        adapters = (IssueTrackingAdapter(), SourceControlAdapter(),
                    AnalyticsAdapter(), ResearchStorageAdapter(), NotificationAdapter())
        contracts = [validate_adapter(adapter) for adapter in adapters]
        self.assertEqual({contract.contract_version for contract in contracts},
                         {"pmos.operations.contract.v1"})
        self.assertTrue(all(adapter.schema_version and adapter.capability_version
                            and adapter.capabilities for adapter in adapters))

    def test_bad_adapter_fails_closed(self):
        class Bad:
            contract = object()
        with self.assertRaises(ContractViolation):
            validate_adapter(Bad())


class OutboxTests(unittest.TestCase):
    def test_idempotency_conflict_retry_dead_letter_and_reconcile(self):
        outbox = TransactionalOutbox(backoff_base=2, backoff_cap=4)
        first = outbox.enqueue("issue.created", {"id": "1"},
                               idempotency_key="k", max_attempts=2)
        self.assertEqual(outbox.enqueue("issue.created", {"id": "1"},
                                        idempotency_key="k").id, first.id)
        with self.assertRaises(IdempotencyConflict):
            outbox.enqueue("issue.created", {"id": "2"}, idempotency_key="k")
        with self.assertRaises(IdempotencyConflict):
            outbox.enqueue("issue.deleted", {"id": "1"}, idempotency_key="k")
        retry = outbox.attempt(first.id, lambda payload: (_ for _ in ()).throw(TimeoutError()), now=0)
        self.assertEqual(retry.status, OutboxStatus.RETRY_WAIT)
        dead = outbox.attempt(first.id, lambda payload: (_ for _ in ()).throw(RuntimeError()), now=2)
        self.assertEqual(dead.status, OutboxStatus.DEAD_LETTER)
        delivered = outbox.enqueue("notice", {"id": "2"}, idempotency_key="n")
        delivered = outbox.attempt(delivered.id, lambda payload: "external-2", now=0)
        self.assertEqual(delivered.status, OutboxStatus.DELIVERED)
        self.assertEqual(outbox.reconcile({"n": "external-2"})[0].status,
                         OutboxStatus.ACKNOWLEDGED)

    def test_degraded_and_unavailable_modes_are_explicit(self):
        outbox = TransactionalOutbox(backoff_base=1, backoff_cap=2)
        queued = outbox.enqueue("notice", {"ok": True}, idempotency_key="d",
                                max_attempts=3, now=0)
        outbox.set_state("degraded", "dependency lag")
        degraded = outbox.attempt(queued.id, lambda payload: True, now=0)
        self.assertEqual(degraded.status, OutboxStatus.DEGRADED)
        self.assertEqual((degraded.attempts, degraded.next_attempt_at), (1, 1))
        outbox.set_state("unavailable", "dependency down")
        unavailable = outbox.attempt(queued.id, lambda payload: True, now=1)
        self.assertEqual(unavailable.status, OutboxStatus.UNAVAILABLE)
        self.assertEqual((unavailable.attempts, unavailable.next_attempt_at), (2, 3))
        self.assertEqual(outbox.dispatch(lambda payload: True, now=2), ())
        self.assertEqual(outbox.attempt(queued.id, lambda payload: True, now=3).status,
                         OutboxStatus.DEAD_LETTER)
        with self.assertRaises(DataValidationError):
            outbox.enqueue("secret", {"token": "never"}, idempotency_key="bad")

    def test_delivered_event_is_not_resent_and_sender_gets_idempotency_envelope(self):
        outbox = TransactionalOutbox()
        queued = outbox.enqueue("issue.created", {"id": "42"},
                                idempotency_key="issue-42")
        calls = []

        def sender(envelope):
            calls.append(envelope)
            return "remote-42"

        delivered = outbox.attempt(queued.id, sender, now=0)
        self.assertEqual(delivered.status, OutboxStatus.DELIVERED)
        self.assertEqual(calls, [{
            "event_type": "issue.created",
            "idempotency_key": "issue-42",
            "payload_hash": queued.payload_hash,
            "payload": {"id": "42"},
        }])
        self.assertEqual(outbox.dispatch(sender, now=1), ())
        self.assertEqual(outbox.attempt(queued.id, sender, now=2), delivered)
        self.assertEqual(len(calls), 1)

    def test_acknowledgement_requires_a_delivered_matching_record(self):
        outbox = TransactionalOutbox()
        queued = outbox.enqueue("notice", {"id": "1"}, idempotency_key="ack-1")
        with self.assertRaises(OutboxError):
            outbox.acknowledge(queued.id, external_id="unverified-remote", now=1)
        with self.assertRaises(OutboxError):
            outbox.reconcile({"ack-1": "unverified-remote"}, now=1)
        rejected = outbox.attempt(queued.id, lambda envelope: None, now=2)
        self.assertEqual(rejected.status, OutboxStatus.RETRY_WAIT)
        delivered = outbox.attempt(queued.id, lambda envelope: "verified-remote", now=3)
        self.assertEqual(delivered.status, OutboxStatus.DELIVERED)
        with self.assertRaises(OutboxError):
            outbox.acknowledge(delivered.id, now=3)
        with self.assertRaises(OutboxError):
            outbox.acknowledge(delivered.id, external_id="different-remote", now=3)
        acknowledged = outbox.acknowledge(delivered.id, external_id="verified-remote", now=3)
        self.assertEqual(acknowledged.status, OutboxStatus.ACKNOWLEDGED)
        self.assertEqual(acknowledged.external_id, "verified-remote")
        with self.assertRaises(OutboxError):
            outbox.acknowledge(delivered.id, external_id="different-remote", now=4)

    def test_sender_identity_secret_content_and_concurrent_attempts_fail_closed(self):
        outbox = TransactionalOutbox(backoff_base=0)
        with self.assertRaises(DataValidationError):
            outbox.enqueue("notice", {"nested": {"value": "sk-or-v1-" + "a" * 24}},
                           idempotency_key="secret-value")
        cyclic = {}
        cyclic["self"] = cyclic
        with self.assertRaises(DataValidationError):
            outbox.enqueue("notice", cyclic, idempotency_key="cyclic")

        queued = outbox.enqueue("notice", {"id": "1"}, idempotency_key="concurrent")
        entered, release, second_started = threading.Event(), threading.Event(), threading.Event()
        calls, outcomes = [], []

        def sender(_envelope):
            calls.append("send")
            entered.set()
            self.assertTrue(release.wait(1))
            return "remote-1"

        first = threading.Thread(target=lambda: outcomes.append(outbox.attempt(queued.id, sender, now=0)))
        second = threading.Thread(target=lambda: (second_started.set(), outcomes.append(
            outbox.attempt(queued.id, sender, now=0))))
        first.start()
        self.assertTrue(entered.wait(1))
        second.start()
        self.assertTrue(second_started.wait(1))
        release.set()
        first.join(1)
        second.join(1)
        self.assertFalse(first.is_alive())
        self.assertFalse(second.is_alive())
        self.assertEqual(calls, ["send"])
        self.assertEqual({item.status for item in outcomes}, {OutboxStatus.DELIVERED})


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.analytics = AnalyticsAdapter()
        self.kwargs = dict(metric_id="activation", value=2.0, unit="users",
                            definition="users who finish setup", source="warehouse",
                            observed_at=90, freshness_seconds=20,
                            lineage_hash="a" * 64)

    def test_metric_freshness_future_and_lineage(self):
        self.assertEqual(self.analytics.ingest_metric(self.kwargs, now=100).value, 2.0)
        for changes in ({"observed_at": 101}, {"observed_at": 1},
                        {"lineage_hash": "unproven"}, {"source": "unknown"}):
            bad = dict(self.kwargs, **changes)
            with self.assertRaises(DataValidationError):
                self.analytics.ingest_metric(bad, now=100)

    def test_experiment_outcome_links_typed_experiment_and_decision(self):
        outcome = self.analytics.record_experiment_outcome(
            ExperimentRef("exp-1"), DecisionRef("decision-1"), {"result": "persist"},
            recorded_at=100)
        self.assertEqual(outcome.experiment.type, "experiment")
        with self.assertRaises(TypeError):
            outcome.result["result"] = "mutated"
        self.assertEqual(self.analytics.outcomes[0].result["result"], "persist")
        with self.assertRaises(DataValidationError):
            self.analytics.record_experiment_outcome(
                {"id": "exp-1", "type": "decision"}, DecisionRef("decision-1"), {"ok": 1})


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.research = ResearchStorageAdapter(retention_seconds=10,
                                                clock=lambda: 100)

    def test_consent_recruit_retention_redaction_deletion_and_quote_refusal(self):
        with self.assertRaises(ConsentError):
            self.research.recruit("p1")
        self.research.record_consent("p1", {"interview", "quote"}, "consent-v2",
                                     granted_at=90, expires_at=110)
        self.assertEqual(self.research.recruit("p1", now=95), "enrolled")
        evidence = self.research.store_evidence("p1", "verbatim evidence", captured_at=96,
                                                lineage_hash="b" * 64)
        self.assertEqual(self.research.quote_evidence(evidence.id, now=100),
                         "verbatim evidence")
        self.assertTrue(self.research.redact_evidence(evidence.id).redacted)
        with self.assertRaises(QuoteRefused):
            self.research.quote_evidence(evidence.id, now=100)
        # Retention and deletion both produce a tombstone and no readable content.
        self.assertEqual(self.research.purge_expired(now=100), 0)
        self.assertEqual(self.research.delete_participant("p1", deleted_at=101), 1)
        self.assertIsNone(self.research.get_evidence(evidence.id, now=101))

    def test_quote_needs_explicit_quote_scope_and_retention(self):
        self.research.record_consent("p2", {"interview"}, "v1", granted_at=90,
                                     expires_at=200)
        self.research.recruit("p2", now=95)
        evidence = self.research.store_evidence("p2", "text", captured_at=96,
                                                retention_until=100, lineage_hash="c" * 64)
        with self.assertRaises(QuoteRefused):
            self.research.quote_evidence(evidence.id, now=99)
        self.assertIsNone(self.research.get_evidence(evidence.id, now=100))

    def test_future_research_capture_and_pre_capture_reads_fail_closed(self):
        self.research.record_consent("p3", {"interview", "quote"}, "v1",
                                     granted_at=90, expires_at=200)
        self.research.recruit("p3", now=95)
        with self.assertRaises(DataValidationError):
            self.research.store_evidence("p3", "future", captured_at=101,
                                         lineage_hash="d" * 64)
        evidence = self.research.store_evidence("p3", "present", captured_at=99,
                                                lineage_hash="e" * 64)
        self.assertIsNone(self.research.get_evidence(evidence.id, now=98))
        with self.assertRaises(QuoteRefused):
            self.research.quote_evidence(evidence.id, now=98)

    def test_expired_consent_blocks_storage_reads_before_retention_expiry(self):
        self.research.record_consent("p4", {"interview", "quote"}, "v1",
                                     granted_at=90, expires_at=99)
        self.research.recruit("p4", now=95)
        evidence = self.research.store_evidence(
            "p4", "retained but inaccessible", captured_at=96,
            retention_until=105, lineage_hash="f" * 64)
        self.assertIsNone(self.research.get_evidence(evidence.id, now=99))
        with self.assertRaises(QuoteRefused):
            self.research.quote_evidence(evidence.id, now=99)

    def test_public_evidence_view_hides_expired_and_withdrawn_content(self):
        clock = [100.0]
        research = ResearchStorageAdapter(retention_seconds=100,
                                          clock=lambda: clock[0])
        research.record_consent("expiring", {"interview"}, "v1", expires_at=110)
        research.recruit("expiring")
        expiring = research.store_evidence(
            "expiring", "must not survive consent expiry", lineage_hash="a" * 64)
        self.assertEqual([item.id for item in research.evidence], [expiring.id])
        clock[0] = 110
        self.assertIsNone(research.get_evidence(expiring.id))
        self.assertEqual(research.evidence, ())

        research.record_consent("withdrawn", {"interview"}, "v1", expires_at=200)
        research.recruit("withdrawn")
        withdrawn = research.store_evidence(
            "withdrawn", "must not survive withdrawal", lineage_hash="b" * 64)
        self.assertEqual([item.id for item in research.evidence], [withdrawn.id])
        research.withdraw_consent("withdrawn")
        self.assertIsNone(research.get_evidence(withdrawn.id))
        self.assertEqual(research.evidence, ())

    def test_consent_scope_timestamps_and_secret_evidence_fail_closed(self):
        with self.assertRaises(ConsentError):
            self.research.record_consent("bad", {True}, "v1", granted_at=90)
        with self.assertRaises(DataValidationError):
            self.research.record_consent("bad", {"interview"}, "v1", granted_at=float("nan"))
        self.research.record_consent("p5", {"interview"}, "v1", granted_at=90)
        self.research.recruit("p5", now=95)
        with self.assertRaises(DataValidationError):
            self.research.store_evidence("p5", "sk-or-v1-" + "b" * 24,
                                         captured_at=96, lineage_hash="a" * 64)


class AdoptionTests(unittest.TestCase):
    def test_observation_requires_consent_and_does_not_claim_external_adoption(self):
        observer = AdoptionObserver(clock=lambda: 100)
        with self.assertRaises(ConsentError):
            observer.observe(channel="pilot", outcome="used", consent=False)
        item = observer.observe(channel="pilot", outcome="used", consent=True,
                                observed_at=99, accessibility_issue=True,
                                accessibility_notes="keyboard navigation")
        self.assertEqual(item.evidence_status, "observation_only")
        self.assertFalse(item.external_adoption_evidence)
        self.assertEqual(item.accessibility_notes, "keyboard navigation")

    def test_consent_and_accessibility_flags_require_exact_booleans(self):
        observer = AdoptionObserver(clock=lambda: 100)
        for value in (1, "true", None):
            with self.assertRaises(ConsentError):
                observer.observe(channel="pilot", outcome="used", consent=value)
        for value in (1, "false", None):
            with self.assertRaises(DataValidationError):
                observer.observe(channel="pilot", outcome="used", consent=True,
                                 accessibility_issue=value)
        with self.assertRaises(DataValidationError):
            observer.observe(channel="pilot", outcome="used", consent=True,
                             observed_at=float("inf"))


class OperationsBoundaryTests(unittest.TestCase):
    def test_issue_updates_allow_only_valid_mutable_fields(self):
        issues = IssueTrackingAdapter()
        issue = issues.create_issue("Initial", labels=("triage",))
        with self.assertRaises(DataValidationError):
            issues.update_issue(issue["id"], expected_revision=1, id="replacement")
        with self.assertRaises(DataValidationError):
            issues.update_issue(issue["id"], expected_revision=1, revision=9)
        with self.assertRaises(DataValidationError):
            issues.update_issue(issue["id"], expected_revision=True, status="closed")
        with self.assertRaises(DataValidationError):
            issues.update_issue(issue["id"], expected_revision=1, status="done")
        updated = issues.update_issue(issue["id"], expected_revision=1, status="closed")
        self.assertEqual((updated["id"], updated["revision"], updated["status"]),
                         (issue["id"], 2, "closed"))

    def test_bounded_in_memory_adapters_reject_oversized_record_sets(self):
        with patch("pmos.operations.MAX_IN_MEMORY_RECORDS", 1):
            issues = IssueTrackingAdapter()
            issues.create_issue("one")
            with self.assertRaises(DataValidationError):
                issues.create_issue("two")

            notifications = NotificationAdapter()
            notifications.queue_notification("user", "one")
            with self.assertRaises(DataValidationError):
                notifications.queue_notification("user", "two")

            outbox = TransactionalOutbox()
            outbox.enqueue("notice", {"id": "1"}, idempotency_key="one")
            with self.assertRaises(DataValidationError):
                outbox.enqueue("notice", {"id": "2"}, idempotency_key="two")

            adoption = AdoptionObserver(clock=lambda: 100)
            adoption.observe(channel="pilot", outcome="one", consent=True)
            with self.assertRaises(DataValidationError):
                adoption.observe(channel="pilot", outcome="two", consent=True)

            analytics = AnalyticsAdapter()
            observation = dict(metric_id="metric", value=1, unit="users", definition="defined",
                               source="warehouse", observed_at=90, freshness_seconds=20,
                               lineage_hash="d" * 64)
            analytics.ingest_metric(observation, now=100)
            with self.assertRaises(DataValidationError):
                analytics.ingest_metric(observation, now=100)

            research = ResearchStorageAdapter(clock=lambda: 100)
            research.record_consent("one", {"interview"}, "v1", granted_at=90)
            with self.assertRaises(DataValidationError):
                research.record_consent("two", {"interview"}, "v1", granted_at=90)

            source = SourceControlAdapter()
            with self.assertRaises(DataValidationError):
                source.create_branch("feature")


if __name__ == "__main__":
    unittest.main(verbosity=2)
