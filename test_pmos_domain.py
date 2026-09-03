import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from pmos.domain import (
    AllocationError,
    ApprovalError,
    BootstrapError,
    ENTITY_TYPES,
    LifecycleStage,
    PMOSDomain,
    PermissionDenied,
    PersistenceError,
    RelationError,
    RevisionConflict,
    SNAPSHOT_PATH,
    TransitionError,
    ValidationError,
)
from pmos.store import Store


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


class DomainTest(unittest.TestCase):
    def setUp(self):
        self.d = PMOSDomain()
        self.org, self.product, self.owner, self.owner_membership = self.d.bootstrap_workspace(
            "Acme", "Ledger", "Owner"
        )
        self.actor = self.owner.id

    def test_lifecycle_e2e_and_independent_stages(self):
        i = self.d.create_initiative(self.product.id, "Fees", actor_id=self.actor)
        stages = [
            LifecycleStage.DEFINE,
            LifecycleStage.DESIGN,
            LifecycleStage.BUILD,
            LifecycleStage.DELIVER,
            LifecycleStage.OPERATE,
            LifecycleStage.RETIRED,
        ]
        for target in stages:
            evidence = self.d.create_evidence(
                i.id,
                f"{i.stage.value} review",
                f"{i.stage.value}-evidence",
                actor_id=self.actor,
            )
            i = self.d.complete_gate(
                i.id, i.stage, evidence_ids=[evidence.id], actor_id=self.actor,
                expected_revision=i.revision,
            )
            i = self.d.transition_initiative(
                i.id, target, expected_revision=i.revision, actor_id=self.actor
            )
        self.assertTrue(i.retired)
        other = [
            self.d.create_initiative(self.product.id, str(n), actor_id=self.actor)
            for n in range(4)
        ]
        self.assertEqual({x.stage for x in other}, {LifecycleStage.DISCOVER})

    def test_blocked_transition_and_cas(self):
        i = self.d.create_initiative(self.product.id, "A", actor_id=self.actor)
        research = self.d.create_evidence(
            i.id, "Research", "customer evidence", actor_id=self.actor
        )
        self.d.set_gate_requirements(
            i.id, i.stage, [research.id], actor_id=self.actor
        )
        with self.assertRaises(TransitionError):
            self.d.transition_initiative(
                i.id, LifecycleStage.DEFINE, expected_revision=i.revision, actor_id=self.actor
            )
        with self.assertRaises(TransitionError):
            self.d.complete_gate(i.id, i.stage, actor_id=self.actor,
                                expected_revision=i.revision)
        i = self.d.complete_gate(
            i.id, i.stage, prerequisites=[research.id], actor_id=self.actor,
            expected_revision=i.revision,
        )
        current = self.d.transition_initiative(
            i.id, LifecycleStage.DEFINE, expected_revision=i.revision, actor_id=self.actor
        )
        with self.assertRaises(RevisionConflict):
            self.d.update(
                "initiative", i.id, expected_revision=i.revision, name="stale", actor_id=self.actor
            )
        self.assertEqual(current.revision, 2)

    def test_transition_requires_current_stage_gate_not_old_assertions(self):
        initiative = self.d.create_initiative(self.product.id, "No bypass", actor_id=self.actor)
        discover_evidence = self.d.create_evidence(
            initiative.id, "Discover", "discovery complete", actor_id=self.actor
        )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DISCOVER,
            evidence_ids=[discover_evidence.id],
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        initiative = self.d.transition_initiative(
            initiative.id, LifecycleStage.DEFINE,
            expected_revision=initiative.revision, actor_id=self.actor,
        )
        with self.assertRaises(TransitionError):
            self.d.transition_initiative(
                initiative.id, LifecycleStage.DESIGN,
                expected_revision=initiative.revision,
                prerequisites=[discover_evidence.id], actor_id=self.actor,
            )
        self.assertEqual(self.d.get(initiative.id, "initiative").stage, LifecycleStage.DEFINE)
        define_evidence = self.d.create_evidence(
            initiative.id, "Define", "definition complete", actor_id=self.actor
        )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DEFINE,
            evidence_ids=[define_evidence.id],
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        advanced = self.d.transition_initiative(
            initiative.id, LifecycleStage.DESIGN,
            expected_revision=initiative.revision, actor_id=self.actor,
        )
        self.assertEqual(advanced.stage, LifecycleStage.DESIGN)

    def test_traceability_is_typed_and_non_dangling(self):
        i = self.d.create_initiative(self.product.id, "A", actor_id=self.actor)
        decision = self.d.create_decision(i.id, "Ship", actor_id=self.actor)
        risk = self.d.create_risk(i.id, "Fraud", actor_id=self.actor)
        evidence = self.d.create_evidence(i.id, "Review", "sample", actor_id=self.actor)
        metric = self.d.create_metric(i.id, "approval", actor_id=self.actor)
        experiment = self.d.create_experiment(i.id, "Holdout", actor_id=self.actor)
        release = self.d.create_release(i.id, "v1", actor_id=self.actor)
        self.d.link(decision.id, risk.id, "informs", actor_id=self.actor)
        self.d.link(risk.id, evidence.id, "supports", actor_id=self.actor)
        self.d.link(evidence.id, metric.id, "measures", actor_id=self.actor)
        self.d.link(metric.id, experiment.id, "validates", actor_id=self.actor)
        self.d.link(experiment.id, release.id, "ships", actor_id=self.actor)
        with self.assertRaises(RelationError):
            self.d.link(decision.id, decision.id, "informs", actor_id=self.actor)

    def test_rbac_and_collaboration(self):
        viewer = self.d.create_user("Viewer", actor_id=self.actor)
        pm = self.d.create_user("PM", actor_id=self.actor)
        self.d.add_membership(self.product.id, viewer.id, "viewer", actor_id=self.actor)
        self.d.add_membership(self.product.id, pm.id, "pm", actor_id=self.actor)
        i = self.d.create_initiative(self.product.id, "A", actor_id=self.actor)
        with self.assertRaises(PermissionDenied):
            self.d.assign(i.id, viewer.id, actor_id=viewer.id)
        with self.assertRaises(PermissionDenied):
            self.d.complete_gate(i.id, i.stage, actor_id=viewer.id,
                                 expected_revision=i.revision)
        comment = self.d.add_comment(i.id, "hello", actor_id=viewer.id)
        mention = self.d.mention(i.id, pm.id, actor_id=viewer.id, comment_id=comment.id)
        self.assertEqual(mention.mentioned_user_id, pm.id)

    def test_reserved_system_actor_and_unguarded_writes_are_rejected(self):
        initiative = self.d.create_initiative(self.product.id, "Guarded", actor_id=self.actor)
        decision = self.d.create_decision(initiative.id, "D", actor_id=self.actor)
        risk = self.d.create_risk(initiative.id, "R", actor_id=self.actor)
        attempts = (
            lambda: self.d.create_initiative(self.product.id, "missing actor"),
            lambda: self.d.create_initiative(self.product.id, "magic actor", actor_id="system"),
            lambda: self.d.create_decision(initiative.id, "missing actor"),
            lambda: self.d.link(decision.id, risk.id, "informs"),
            lambda: self.d.set_capacity(self.product.id, "Q1", 1),
        )
        for attempt in attempts:
            with self.subTest(attempt=attempt):
                with self.assertRaises(PermissionDenied):
                    attempt()
        self.assertEqual(len(self.d.list_entities("initiative")), 1)
        with self.assertRaises(BootstrapError):
            self.d.bootstrap_workspace("Again", "Again", "Again")

    def test_new_product_atomically_grants_creator_ownership(self):
        organization = self.d.create_organization("Second org", actor_id=self.actor)
        product = self.d.create_product(organization.id, "Second", actor_id=self.actor)
        self.assertTrue(self.d.authorize(product.id, self.actor, "admin"))
        initiative = self.d.create_initiative(product.id, "Works", actor_id=self.actor)
        self.assertEqual(initiative.product_id, product.id)
        memberships = [
            value for value in self.d.list_entities("membership")
            if value.product_id == product.id and value.user_id == self.actor
        ]
        self.assertEqual([value.role for value in memberships], ["owner"])

    def test_cross_product_reads_and_dependencies_respect_authority_boundary(self):
        viewer = self.d.create_user("Viewer", actor_id=self.actor)
        self.d.add_membership(self.product.id, viewer.id, "viewer", actor_id=self.actor)
        visible = self.d.create_initiative(self.product.id, "Visible", actor_id=self.actor)
        organization = self.d.create_organization("Other org", actor_id=self.actor)
        other_product = self.d.create_product(organization.id, "Other", actor_id=self.actor)
        hidden = self.d.create_initiative(other_product.id, "Hidden", actor_id=self.actor)

        self.assertEqual(
            [item.id for item in self.d.list_entities("initiative", actor_id=viewer.id)],
            [visible.id],
        )
        self.assertEqual(self.d.get(visible.id, actor_id=viewer.id).id, visible.id)
        with self.assertRaises(PermissionDenied):
            self.d.get(hidden.id, actor_id=viewer.id)
        with self.assertRaises(PermissionDenied):
            self.d.rollup(other_product.id, actor_id=viewer.id)
        with self.assertRaises(AllocationError):
            self.d.add_dependency(visible.id, hidden.id, actor_id=self.actor)

    def test_generic_create_and_update_cannot_bypass_governance(self):
        initiative = self.d.create_initiative(self.product.id, "Guarded", actor_id=self.actor)
        with self.assertRaises(ValidationError):
            self.d.create_initiative(
                self.product.id, "Jump", actor_id=self.actor, stage=LifecycleStage.BUILD
            )
        with self.assertRaises(TransitionError):
            self.d.update(
                "initiative", initiative.id, expected_revision=initiative.revision,
                actor_id=self.actor, stage=LifecycleStage.BUILD,
            )
        evidence = self.d.create_evidence(
            initiative.id, "Evidence", "fact", actor_id=self.actor
        )
        approval = self.d.request_approval(
            initiative.id, evidence_ids=[evidence.id], actor_id=self.actor
        )
        with self.assertRaises(ApprovalError):
            self.d.update(
                "approval", approval.id, expected_revision=approval.revision,
                actor_id=self.actor, status="approved",
            )
        self.assertEqual(self.d.get(initiative.id).stage, LifecycleStage.DISCOVER)
        self.assertEqual(self.d.get(approval.id).status, "requested")

    def test_approval_requires_independent_approver_and_persists_requester(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "approval.db")
            store = Store(path)
            domain = PMOSDomain(store, storage_id="approval-os")
            _org, product, owner, _membership = domain.bootstrap_workspace(
                "Bank", "Payments", "Maker", regulated=True
            )
            initiative = domain.create_initiative(product.id, "KYC", actor_id=owner.id)
            evidence = domain.create_evidence(
                initiative.id, "Control", "pass", actor_id=owner.id
            )
            request = domain.request_approval(
                initiative.id, evidence_ids=[evidence.id],
                policy_version="policy-1", actor_id=owner.id,
            )
            with self.assertRaises(ApprovalError):
                domain.approve(
                    request.id, approver_id=owner.id, evidence_ids=[evidence.id]
                )
            checker = domain.create_user("Checker", actor_id=owner.id)
            domain.add_membership(product.id, checker.id, "approver", actor_id=owner.id)
            approved = domain.approve(
                request.id, approver_id=checker.id, evidence_ids=[evidence.id]
            )
            self.assertEqual(approved.requester_id, owner.id)
            self.assertEqual(approved.approver_id, checker.id)
            store.close()

            reopened_store = Store(path)
            reopened = PMOSDomain(reopened_store, storage_id="approval-os")
            restored = reopened.get(request.id, "approval", actor_id=checker.id)
            self.assertEqual(restored.requester_id, owner.id)
            self.assertEqual(restored.approver_id, checker.id)
            reopened_store.close()

    def test_regulated_approval_drift_revoke_and_reapprove(self):
        regulated = self.d.create_product(
            self.org.id, "Bank", regulated=True, actor_id=self.actor
        )
        i = self.d.create_initiative(regulated.id, "KYC", actor_id=self.actor)
        approver = self.d.create_user("Approver", actor_id=self.actor)
        self.d.add_membership(regulated.id, approver.id, "approver", actor_id=self.actor)
        ev = self.d.create_evidence(i.id, "Control", "v1", actor_id=self.actor)
        approval = self.d.request_approval(
            i.id, evidence_ids=[ev.id], policy_version="p1",
            actor_id=self.actor, regulated=False,
        )
        approved = self.d.approve(
            approval.id, approver_id=approver.id, evidence_ids=[ev.id], timestamp=100
        )
        self.assertEqual(approved.status, "approved")
        self.d.update(
            "evidence", ev.id, expected_revision=ev.revision,
            content="v2", actor_id=self.actor,
        )
        self.assertEqual(self.d.get(approval.id).status, "invalidated")
        with self.assertRaises(ApprovalError):
            self.d.approve(approval.id, approver_id=approver.id)
        self.d.revoke_approval(approval.id, actor_id=approver.id)
        fresh = self.d.request_approval(
            i.id, evidence_ids=[ev.id], policy_version="p1", actor_id=self.actor
        )
        self.assertEqual(
            self.d.approve(fresh.id, approver_id=approver.id, evidence_ids=[ev.id]).status,
            "approved",
        )

    def test_gate_rejects_labels_cross_initiative_evidence_and_hash_drift(self):
        initiative = self.d.create_initiative(
            self.product.id, "Evidence-bound", actor_id=self.actor
        )
        other = self.d.create_initiative(
            self.product.id, "Other", actor_id=self.actor
        )
        evidence = self.d.create_evidence(
            initiative.id, "Research", "v1", actor_id=self.actor
        )
        foreign = self.d.create_evidence(
            other.id, "Foreign", "not applicable", actor_id=self.actor
        )

        with self.assertRaises(TransitionError):
            self.d.set_gate_requirements(
                initiative.id,
                LifecycleStage.DISCOVER,
                ["approved-by-regulatory"],
                actor_id=self.actor,
            )
        with self.assertRaises(TransitionError):
            initiative = self.d.complete_gate(
                initiative.id,
                LifecycleStage.DISCOVER,
                prerequisites=["evidence-hash:abc"],
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )
        with self.assertRaises(TransitionError):
            self.d.complete_gate(
                initiative.id,
                LifecycleStage.DISCOVER,
                evidence_ids=[foreign.id],
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )
        with self.assertRaises(TransitionError):
            self.d.complete_gate(
                initiative.id,
                LifecycleStage.DISCOVER,
                evidence_ids=[["not", "an", "id"]],
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )

        self.d.set_gate_requirements(
            initiative.id,
            LifecycleStage.DISCOVER,
            [evidence.id],
            actor_id=self.actor,
        )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DISCOVER,
            evidence_ids=[evidence.id],
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        proof = self.d.gate_proof(
            initiative.id, LifecycleStage.DISCOVER, actor_id=self.actor
        )
        self.assertEqual(proof.evidence_bindings, ((evidence.id, evidence.content_hash),))

        updated = self.d.update(
            "evidence",
            evidence.id,
            expected_revision=evidence.revision,
            content="v2",
            actor_id=self.actor,
        )
        self.assertEqual(self.d.completed_gates(initiative.id), ())
        with self.assertRaises(TransitionError):
            self.d.transition_initiative(
                initiative.id,
                LifecycleStage.DEFINE,
                expected_revision=initiative.revision,
                actor_id=self.actor,
            )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DISCOVER,
            evidence_ids=[updated.id],
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        rebound = self.d.gate_proof(initiative.id, LifecycleStage.DISCOVER)
        self.assertEqual(rebound.evidence_bindings, ((updated.id, updated.content_hash),))

    def test_digest_only_evidence_requires_external_verification(self):
        initiative = self.d.create_initiative(self.product.id, "Evidence contract", actor_id=self.actor)
        forged_hash = "0" * 64
        with self.assertRaises(ValidationError):
            self.d.create_evidence(
                initiative.id, "Unverifiable", content="", content_hash=forged_hash,
                actor_id=self.actor,
            )

        verified = PMOSDomain(evidence_verifier=lambda digest: digest == forged_hash)
        _org, product, owner, _membership = verified.bootstrap_workspace(
            "External Org", "External Product", "External Owner")
        external_initiative = verified.create_initiative(product.id, "External", actor_id=owner.id)
        evidence = verified.create_evidence(
            external_initiative.id, "External record", content="", content_hash=forged_hash,
            actor_id=owner.id,
        )
        completed = verified.complete_gate(
            external_initiative.id, LifecycleStage.DISCOVER,
            evidence_ids=[evidence.id], actor_id=owner.id,
            expected_revision=external_initiative.revision,
        )
        self.assertEqual(completed.revision, external_initiative.revision + 1)

    def test_gate_completion_is_revisioned_and_concurrent_proof_conflicts(self):
        initiative = self.d.create_initiative(self.product.id, "CAS gate", actor_id=self.actor)
        evidence = self.d.create_evidence(initiative.id, "Proof", "observed", actor_id=self.actor)
        first = self.d.complete_gate(
            initiative.id, LifecycleStage.DISCOVER, evidence_ids=[evidence.id],
            actor_id=self.actor, expected_revision=initiative.revision,
        )
        self.assertEqual(first.revision, initiative.revision + 1)
        with self.assertRaises(RevisionConflict):
            self.d.complete_gate(
                initiative.id, LifecycleStage.DISCOVER, evidence_ids=[evidence.id],
                actor_id=self.actor, expected_revision=initiative.revision,
            )

    def test_regulated_checkpoint_requires_current_independent_bound_approval(self):
        regulated = self.d.create_product(
            self.org.id, "Regulated", regulated=True, actor_id=self.actor
        )
        initiative = self.d.create_initiative(
            regulated.id, "KYC", actor_id=self.actor
        )
        checker = self.d.create_user("Checker", actor_id=self.actor)
        self.d.add_membership(
            regulated.id, checker.id, "approver", actor_id=self.actor
        )

        # Low-risk discovery/definition still require explicit evidence, but
        # the policy checkpoint begins before implementation (DESIGN -> BUILD).
        for target in (LifecycleStage.DEFINE, LifecycleStage.DESIGN):
            evidence = self.d.create_evidence(
                initiative.id,
                f"{initiative.stage.value} evidence",
                f"{initiative.stage.value} complete",
                actor_id=self.actor,
            )
            initiative = self.d.complete_gate(
                initiative.id,
                initiative.stage,
                evidence_ids=[evidence.id],
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )
            initiative = self.d.transition_initiative(
                initiative.id,
                target,
                expected_revision=initiative.revision,
                actor_id=self.actor,
            )

        design_evidence = self.d.create_evidence(
            initiative.id, "Design controls", "controls pass", actor_id=self.actor
        )
        with self.assertRaises(ApprovalError):
            self.d.complete_gate(
                initiative.id,
                LifecycleStage.DESIGN,
                evidence_ids=[design_evidence.id],
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )

        request = self.d.request_approval(
            initiative.id,
            evidence_ids=[design_evidence.id],
            policy_version="policy-2026-09",
            actor_id=self.actor,
        )
        with self.assertRaises(ApprovalError):
            self.d.approve(
                request.id,
                approver_id=self.actor,
                evidence_ids=[design_evidence.id],
            )
        self.d.approve(
            request.id,
            approver_id=checker.id,
            evidence_ids=[design_evidence.id],
        )
        unrelated = self.d.create_evidence(
            initiative.id, "Unreviewed", "not approved", actor_id=self.actor
        )
        with self.assertRaises(ApprovalError):
            self.d.complete_gate(
                initiative.id,
                LifecycleStage.DESIGN,
                evidence_ids=[design_evidence.id, unrelated.id],
                approval_id=request.id,
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DESIGN,
            evidence_ids=[design_evidence.id],
            approval_id=request.id,
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        proof = self.d.gate_proof(initiative.id, LifecycleStage.DESIGN)
        self.assertEqual(proof.approval_id, request.id)
        self.assertEqual(proof.policy_version, "policy-2026-09")

        self.d.revoke_approval(
            request.id, actor_id=checker.id, reason="control withdrawn"
        )
        self.assertNotIn("design:complete", self.d.completed_gates(initiative.id))
        with self.assertRaises(TransitionError):
            self.d.transition_initiative(
                initiative.id,
                LifecycleStage.BUILD,
                expected_revision=initiative.revision,
                actor_id=self.actor,
            )

        replacement = self.d.request_approval(
            initiative.id,
            evidence_ids=[design_evidence.id],
            policy_version="policy-2026-09",
            actor_id=self.actor,
        )
        self.d.approve(
            replacement.id,
            approver_id=checker.id,
            evidence_ids=[design_evidence.id],
        )
        initiative = self.d.complete_gate(
            initiative.id,
            LifecycleStage.DESIGN,
            evidence_ids=[design_evidence.id],
            approval_id=replacement.id,
            actor_id=self.actor,
            expected_revision=initiative.revision,
        )
        initiative = self.d.transition_initiative(
            initiative.id,
            LifecycleStage.BUILD,
            expected_revision=initiative.revision,
            actor_id=self.actor,
        )
        build_evidence = self.d.create_evidence(
            initiative.id, "Build controls", "build verified", actor_id=self.actor
        )
        with self.assertRaises(ApprovalError):
            self.d.complete_gate(
                initiative.id,
                LifecycleStage.BUILD,
                evidence_ids=[build_evidence.id],
                approval_id=replacement.id,
                actor_id=self.actor,
                expected_revision=initiative.revision,
            )

    def test_audit_export_redacts_evidence_and_collaboration_content(self):
        initiative = self.d.create_initiative(
            self.product.id, "Confidential", actor_id=self.actor
        )
        evidence = self.d.create_evidence(
            initiative.id,
            "Interview",
            "customer-confidential-v1",
            actor_id=self.actor,
        )
        self.d.comment(
            initiative.id, "private-review-comment", actor_id=self.actor
        )
        updated = self.d.update(
            "evidence",
            evidence.id,
            expected_revision=evidence.revision,
            content="customer-confidential-v2",
            actor_id=self.actor,
        )
        exported = self.d.export_audit()
        self.assertTrue(self.d.verify_audit_export(exported))
        self.assertNotIn("customer-confidential-v1", exported)
        self.assertNotIn("customer-confidential-v2", exported)
        self.assertNotIn("private-review-comment", exported)
        self.assertIn(updated.content_hash, exported)

    def test_capacity_priority_sequence_dependencies_and_audit(self):
        a = self.d.create_initiative(self.product.id, "A", actor_id=self.actor)
        b = self.d.create_initiative(self.product.id, "B", actor_id=self.actor)
        c = self.d.create_initiative(self.product.id, "C", actor_id=self.actor)
        self.d.set_capacity(self.product.id, "Q1", 5, actor_id=self.actor)
        self.d.allocate_capacity(a.id, "Q1", 3, actor_id=self.actor)
        with self.assertRaises(AllocationError):
            self.d.allocate_capacity(b.id, "Q1", 3, actor_id=self.actor)
        self.d.allocate_capacity(b.id, "Q1", 2, actor_id=self.actor)
        self.d.score_initiative(a.id, 9, actor_id=self.actor)
        self.d.sequence_initiative(a.id, 1, period="Q1", actor_id=self.actor)
        self.d.add_dependency(a.id, b.id, actor_id=self.actor)
        self.d.add_dependency(b.id, c.id, actor_id=self.actor)
        with self.assertRaises(AllocationError):
            self.d.add_dependency(c.id, a.id, actor_id=self.actor)
        exported = self.d.export_audit()
        self.assertTrue(self.d.verify_audit_export(exported))
        tampered = json.loads(exported)
        tampered["events"][0]["action"] = "tampered"
        self.assertFalse(self.d.verify_audit_export(tampered))

    def test_full_aggregate_round_trip_rehydrates_every_state_family(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "domain.db")
            store = Store(path)
            domain = PMOSDomain(store, storage_id="complete-os")
            _org, product, owner, _membership = domain.bootstrap_workspace(
                "Complete", "Payments", "Owner", regulated=True
            )
            actor = owner.id
            initiative = domain.create_initiative(
                product.id, "KYC", description="regulated flow", actor_id=actor
            )
            dependency_target = domain.create_initiative(product.id, "Platform", actor_id=actor)
            domain.create_opportunity(initiative.id, "Reduce abandonment", actor_id=actor)
            experiment = domain.create_experiment(
                initiative.id, "Holdout", hypothesis="conversion rises", actor_id=actor
            )
            release = domain.create_release(
                initiative.id, "Launch", version_label="1.0", actor_id=actor
            )
            decision = domain.create_decision(
                initiative.id, "Ship", outcome="approved", actor_id=actor
            )
            risk = domain.create_risk(initiative.id, "Fraud", severity="high", actor_id=actor)
            evidence = domain.create_evidence(
                initiative.id, "Control test", "passed", actor_id=actor
            )
            metric = domain.create_metric(
                initiative.id, "conversion", target=0.8, unit="ratio", actor_id=actor
            )
            teammate = domain.create_user("Teammate", actor_id=actor)
            approver = domain.create_user("Approver", actor_id=actor)
            domain.add_membership(product.id, teammate.id, "contributor", actor_id=actor)
            domain.add_membership(product.id, approver.id, "approver", actor_id=actor)
            domain.assign(initiative.id, teammate.id, actor_id=actor, role="designer")
            comment = domain.comment(initiative.id, "review", actor_id=teammate.id)
            domain.mention(
                initiative.id, approver.id, actor_id=teammate.id, comment_id=comment.id
            )
            approval = domain.request_approval(
                initiative.id, evidence_ids=[evidence.id],
                policy_version="policy-1", actor_id=actor,
            )
            domain.approve(approval.id, approver_id=approver.id, evidence_ids=[evidence.id])
            domain.link(decision.id, risk.id, "informs", actor_id=actor)
            domain.link(risk.id, evidence.id, "supports", actor_id=actor)
            domain.link(evidence.id, metric.id, "measures", actor_id=actor)
            domain.link(metric.id, experiment.id, "validates", actor_id=actor)
            domain.link(experiment.id, release.id, "ships", actor_id=actor)
            domain.set_gate_requirements(
                initiative.id, LifecycleStage.DISCOVER, [evidence.id], actor_id=actor
            )
            domain.complete_gate(
                initiative.id, LifecycleStage.DISCOVER,
                evidence_ids=[evidence.id], approval_id=approval.id, actor_id=actor,
                expected_revision=initiative.revision,
            )
            domain.set_capacity(product.id, "Q1", 5, actor_id=actor)
            domain.allocate_capacity(initiative.id, "Q1", 3, actor_id=actor)
            domain.score_initiative(initiative.id, 9, actor_id=actor)
            domain.sequence_initiative(initiative.id, 1, period="Q1", actor_id=actor)
            domain.add_dependency(initiative.id, dependency_target.id, actor_id=actor)
            expected_digest = domain.state_digest
            expected_audit = domain.export_audit()
            expected_head = domain.storage_revision
            store.close()

            reopened_store = Store(path)
            reopened = PMOSDomain.open(reopened_store, storage_id="complete-os")
            self.assertEqual(reopened.state_digest, expected_digest)
            self.assertEqual(reopened.export_audit(), expected_audit)
            self.assertEqual(reopened.storage_revision, expected_head)
            self.assertTrue(reopened.verify_audit_export(reopened.export_audit()))
            for entity_type in ENTITY_TYPES:
                self.assertGreater(len(reopened.list_entities(entity_type)), 0, entity_type)
            self.assertEqual(
                reopened.completed_gates(initiative.id), ("discover:complete",)
            )
            restored_proof = reopened.gate_proof(
                initiative.id, LifecycleStage.DISCOVER, actor_id=actor
            )
            self.assertEqual(restored_proof.evidence_bindings, ((evidence.id, evidence.content_hash),))
            self.assertEqual(restored_proof.approval_id, approval.id)
            self.assertEqual(restored_proof.policy_version, "policy-1")
            self.assertEqual(len(reopened.relation_history()), 5)
            self.assertEqual(reopened.rollup(product.id, "Q1")["capacity"], 3.0)
            self.assertTrue(reopened.authorize(product.id, teammate.id, "edit"))
            loaded = reopened.get(initiative.id, "initiative")
            advanced = reopened.transition_initiative(
                initiative.id, LifecycleStage.DEFINE,
                expected_revision=loaded.revision, actor_id=actor,
            )
            self.assertEqual(advanced.stage, LifecycleStage.DEFINE)
            reopened_store.close()

    def test_two_instances_conflict_rolls_back_then_refresh_retry_preserves_both(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "domain.db")
            first_store = Store(path)
            first = PMOSDomain(first_store, storage_id="shared")
            _org, product, owner, _membership = first.bootstrap_workspace(
                "Acme", "Ledger", "Owner"
            )
            second_store = Store(path)
            second = PMOSDomain(second_store, storage_id="shared")
            stale_digest = second.state_digest

            first.create_initiative(product.id, "First", actor_id=owner.id)
            with self.assertRaisesRegex(RevisionConflict, "refresh before retry"):
                second.create_initiative(product.id, "Second", actor_id=owner.id)
            self.assertEqual(second.state_digest, stale_digest)
            self.assertEqual(len(second.list_entities("initiative")), 0)

            second.refresh()
            second.create_initiative(product.id, "Second", actor_id=owner.id)
            first.refresh()
            self.assertEqual(
                [item.name for item in first.list_entities("initiative")], ["First", "Second"]
            )
            self.assertEqual(first.state_digest, second.state_digest)
            first_store.close()
            second_store.close()

            final_store = Store(path)
            final = PMOSDomain(final_store, storage_id="shared")
            self.assertEqual(
                [item.name for item in final.list_entities("initiative")], ["First", "Second"]
            )
            final_store.close()

    def test_tampered_hash_and_unknown_schema_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "domain.db")
            store = Store(path)
            valid = PMOSDomain(store, storage_id="tampered")
            valid.bootstrap_workspace("Acme", "Ledger", "Owner")
            original = json.loads(store.read_file("tampered", SNAPSHOT_PATH))
            original["state"]["tables"]["organization"][0]["name"] = "altered"
            result = store.commit(
                "tampered", {SNAPSHOT_PATH: canonical(original)},
                expected_revision=store.head("tampered"), metadata={"test": "semantic tamper"},
            )
            self.assertTrue(result.committed)
            with self.assertRaisesRegex(PersistenceError, "hash mismatch"):
                PMOSDomain(store, storage_id="tampered")

            store.create_product("unknown-schema")
            unknown = {
                "format": "pmos.domain.snapshot/v999",
                "schema_version": "pmos.domain.v999",
                "state": {},
                "state_hash": hashlib.sha256(canonical({})).hexdigest(),
            }
            result = store.commit(
                "unknown-schema", {SNAPSHOT_PATH: canonical(unknown)},
                expected_revision=store.head("unknown-schema"),
                metadata={"test": "future schema"},
            )
            self.assertTrue(result.committed)
            with self.assertRaisesRegex(PersistenceError, "unsupported"):
                PMOSDomain(store, storage_id="unknown-schema")
            store.close()

    def test_every_public_mutator_is_transactional(self):
        primary_mutators = {
            "bootstrap_workspace", "create_organization", "create_product",
            "create_initiative", "create_opportunity", "create_experiment",
            "create_release", "create_decision", "create_risk", "create_evidence",
            "create_metric", "update", "complete_gate", "set_gate_requirements",
            "transition_initiative", "retire_initiative", "create_user",
            "add_membership", "assign", "comment", "mention", "link",
            "request_approval", "approve", "revoke_approval", "score_initiative",
            "set_capacity", "allocate_capacity", "sequence_initiative", "add_dependency",
        }
        for name in sorted(primary_mutators):
            with self.subTest(name=name):
                self.assertTrue(
                    hasattr(getattr(PMOSDomain, name), "__wrapped__"),
                    f"{name} must participate in atomic snapshot persistence",
                )


if __name__ == "__main__":
    unittest.main()
