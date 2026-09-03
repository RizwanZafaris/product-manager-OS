"""Executable product-manager OS readiness use cases.

The matrix in this module is deliberately a small integration harness rather
than a documentation checklist.  Every row invokes one or more public PMOS
APIs and returns an inspectable outcome.  A host can run the matrix in CI or
from an onboarding command without needing a network service or model secret.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from collections import Counter
from contextlib import redirect_stdout
from dataclasses import dataclass, field, replace
from io import StringIO
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping

from .cli import main as cli_main
from .conductor import Conductor, EvidenceClass, Question, QuestionBank
from .domain import (
    ApprovalError,
    LifecycleStage,
    PMOSDomain,
    RevisionConflict,
)
from .hooks import decide
from .migrations import create_legacy_fixture, migrate_workspace
from .operations import (
    AnalyticsAdapter,
    DecisionRef,
    ExperimentRef,
    IssueTrackingAdapter,
    ResearchStorageAdapter,
    SourceControlAdapter,
    TransactionalOutbox,
)
from .routing import (
    ModelRouter,
    ModelSpec,
    ProviderResponse,
    RouteStatus,
    RoutingRequest,
)
from .store import QueueStatus, Store
from .skills import SkillRegistry


USE_CASE_IDS = (
    "solo_manual",
    "ai_drafting",
    "concurrent_team",
    "portfolio",
    "regulated",
    "automation",
    "analytics_experiments",
    "research",
    "integrations",
    "migration",
    "disaster_recovery",
    "security",
    "new_user",
)


@dataclass(frozen=True)
class UseCaseResult:
    """One executed matrix row with contract-checked observed evidence.

    ``passed`` is deliberately a computed property.  A row cannot set it to
    ``True`` or provide three assertion strings as a substitute for executing
    its declared predicates.
    """

    use_case_id: str
    assertions: tuple[str, ...]
    evidence: Mapping[str, Any]
    _execution: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({}), repr=False)

    @property
    def passed(self) -> bool:
        return not _result_errors(self)


@dataclass(frozen=True)
class _EvidenceExpectation:
    predicate: Callable[[Any], bool]
    description: str


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 512


def _true(value: Any) -> bool:
    return value is True


def _nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _at_least(minimum: int) -> Callable[[Any], bool]:
    return lambda value: (_nonnegative_int(value) and value >= minimum)


def _equals(expected: Any) -> Callable[[Any], bool]:
    return lambda value: value == expected


def _one_of(*values: str) -> Callable[[Any], bool]:
    return lambda value: value in values


_CASE_ASSERTIONS: Mapping[str, tuple[str, ...]] = {
    "solo_manual": ("created product and initiative", "completed discover gate",
                    "transitioned to define", "evidence remains addressable"),
    "ai_drafting": ("routed a bounded draft", "persisted draft as a decision",
                    "retained model provenance"),
    "concurrent_team": ("assigned work", "recorded comment and mention",
                        "rejected stale revision"),
    "portfolio": ("allocated within each product capacity", "scored initiatives",
                  "sequenced work", "rolled up two products without flattening initiatives"),
    "regulated": ("blocked checkpoint without independent approval",
                  "bound approved evidence and policy to the design gate",
                  "transitioned only after the proof was current",
                  "invalidated approval and gate proof on evidence drift"),
    "automation": ("enqueued idempotent work", "leased with a fence",
                   "recorded terminal success"),
    "analytics_experiments": ("accepted fresh lineaged metric",
                              "linked experiment outcome to decision",
                              "retained typed references"),
    "research": ("required consent before recruitment", "stored lineaged evidence",
                 "redacted evidence before reuse"),
    "integrations": ("created issue through adapter contract",
                     "recorded source-control commit", "delivered idempotent outbox event",
                     "kept external side effect behind an in-process idempotency record"),
    "migration": ("planned a real legacy migration", "activated the public migration API",
                  "reopened and verified the migrated runtime"),
    "disaster_recovery": ("created verified backup", "restored database",
                          "verified restored content and chains"),
    "security": ("blocked secret material", "blocked out-of-bound write",
                 "required approval for external mutation"),
    "new_user": ("initialized and completed the CLI onboarding gate",
                 "reopened Store, Conductor, and durable domain state",
                 "validated a runtime skill contract and hook boundary",
                 "delivered and exactly acknowledged an operation outbox record"),
}


_CASE_EVIDENCE: Mapping[str, Mapping[str, _EvidenceExpectation]] = {
    "solo_manual": {
        "product_id": _EvidenceExpectation(_identifier, "a product ID"),
        "initiative_id": _EvidenceExpectation(_identifier, "an initiative ID"),
        "evidence_id": _EvidenceExpectation(_identifier, "an evidence ID"),
        "trace_count": _EvidenceExpectation(_nonnegative_int, "a nonnegative trace count"),
        "stage": _EvidenceExpectation(_equals("define"), "the DEFINE stage"),
    },
    "ai_drafting": {
        "model": _EvidenceExpectation(_equals("deterministic-draft"), "the routed model"),
        "decision_id": _EvidenceExpectation(_identifier, "a persisted decision ID"),
        "product_id": _EvidenceExpectation(_identifier, "a product ID"),
    },
    "concurrent_team": {
        "assignment_id": _EvidenceExpectation(_identifier, "an assignment ID"),
        "mention_id": _EvidenceExpectation(_identifier, "a mention ID"),
    },
    "portfolio": {
        "allocated_capacity": _EvidenceExpectation(_equals(9.0), "nine units of capacity"),
        "initiative_count": _EvidenceExpectation(_equals(3), "three initiatives"),
        "product_count": _EvidenceExpectation(_equals(2), "two products"),
    },
    "regulated": {
        "product_id": _EvidenceExpectation(_identifier, "a regulated product ID"),
        "blocked_without_approval": _EvidenceExpectation(_true, "an observed approval block"),
        "stage": _EvidenceExpectation(_equals("build"), "the BUILD stage"),
        "changed_evidence_revision": _EvidenceExpectation(_at_least(1), "a changed evidence revision"),
        "approval_status": _EvidenceExpectation(_equals("invalidated"), "an invalidated approval"),
    },
    "automation": {
        "job_id": _EvidenceExpectation(_identifier, "a queue job ID"),
        "status": _EvidenceExpectation(_equals(QueueStatus.SUCCEEDED.value), "a succeeded job"),
    },
    "analytics_experiments": {
        "metric_id": _EvidenceExpectation(_equals("activation"), "the activation metric"),
        "experiment_id": _EvidenceExpectation(_identifier, "an experiment ID"),
        "decision_id": _EvidenceExpectation(_identifier, "a decision ID"),
    },
    "research": {
        "evidence_id": _EvidenceExpectation(_identifier, "research evidence ID"),
        "redacted": _EvidenceExpectation(_true, "a recorded redaction"),
    },
    "integrations": {
        "issue_id": _EvidenceExpectation(_identifier, "an issue ID"),
        "branch": _EvidenceExpectation(_equals("feature/onboarding"), "the expected branch"),
        "external_id": _EvidenceExpectation(_equals("external-event-1"), "a sender external ID"),
        "outbox_status": _EvidenceExpectation(_equals("acknowledged"), "an exact acknowledgement"),
    },
    "migration": {
        "status": _EvidenceExpectation(_equals("migrated"), "a migrated runtime"),
        "backup_created": _EvidenceExpectation(_true, "a migration backup"),
        "runtime_verified": _EvidenceExpectation(_true, "a verified reopened runtime"),
        "migrated_revision": _EvidenceExpectation(_equals(1), "the migrated revision"),
        "migrated_file_count": _EvidenceExpectation(_at_least(2), "migrated legacy files"),
    },
    "disaster_recovery": {
        "revision": _EvidenceExpectation(_equals(1), "a restored durable revision"),
        "verified": _EvidenceExpectation(_true, "a verified restored store"),
    },
    "security": {
        "secret_action": _EvidenceExpectation(_equals("deny"), "secret denial"),
        "outside_action": _EvidenceExpectation(_equals("deny"), "path denial"),
        "external_action": _EvidenceExpectation(_equals("ask"), "external approval"),
    },
    "new_user": {
        "cli_initialized": _EvidenceExpectation(_true, "successful CLI initialization"),
        "cli_completed": _EvidenceExpectation(_true, "a completed CLI gate"),
        "store_verified": _EvidenceExpectation(_true, "a verified Store reopen"),
        "conductor_completed": _EvidenceExpectation(_true, "a durable conductor completion"),
        "domain_reopened": _EvidenceExpectation(_true, "a durable domain reopen"),
        "hook_action": _EvidenceExpectation(_equals("allow"), "an allowed transition hook"),
        "skill_contract_count": _EvidenceExpectation(_at_least(1), "at least one verified skill"),
        "operations_status": _EvidenceExpectation(_equals("acknowledged"), "an acknowledged outbox delivery"),
    },
}

# These calls are observed by the runner, outside the implementation being
# evaluated. They intentionally name public seams rather than every internal
# helper, so refactors remain possible while a constant-result replacement
# cannot masquerade as an integration run.
_EXECUTION_REQUIREMENTS: Mapping[str, Mapping[str, int]] = {
    "solo_manual": {
        "pmos.domain.PMOSDomain.create_evidence": 1,
        "pmos.domain.PMOSDomain.complete_gate": 1,
        "pmos.domain.PMOSDomain.transition_initiative": 1,
        "pmos.domain.PMOSDomain.traces": 1,
    },
    "ai_drafting": {
        "pmos.routing.ModelRouter.route": 1,
        "pmos.domain.PMOSDomain.create_decision": 1,
    },
    "concurrent_team": {
        "pmos.domain.PMOSDomain.assign": 1,
        "pmos.domain.PMOSDomain.comment": 1,
        "pmos.domain.PMOSDomain.mention": 1,
        "pmos.domain.PMOSDomain.update": 2,
    },
    "portfolio": {
        "pmos.domain.PMOSDomain.allocate_capacity": 3,
        "pmos.domain.PMOSDomain.score_initiative": 3,
        "pmos.domain.PMOSDomain.rollup": 2,
    },
    "regulated": {
        "pmos.domain.PMOSDomain.request_approval": 1,
        "pmos.domain.PMOSDomain.approve": 1,
        "pmos.domain.PMOSDomain.complete_gate": 4,
        "pmos.domain.PMOSDomain.transition_initiative": 3,
    },
    "automation": {
        "pmos.store.Store.enqueue": 1,
        "pmos.store.Store.lease_next": 1,
        "pmos.store.Store.succeed": 1,
    },
    "analytics_experiments": {
        "pmos.operations.AnalyticsAdapter.ingest_metric": 1,
        "pmos.operations.AnalyticsAdapter.record_experiment_outcome": 1,
    },
    "research": {
        "pmos.operations.ResearchStorageAdapter.record_consent": 1,
        "pmos.operations.ResearchStorageAdapter.store_evidence": 1,
        "pmos.operations.ResearchStorageAdapter.quote_evidence": 1,
        "pmos.operations.ResearchStorageAdapter.redact_evidence": 1,
    },
    "integrations": {
        "pmos.operations.IssueTrackingAdapter.create_issue": 1,
        "pmos.operations.SourceControlAdapter.record_commit": 1,
        "pmos.operations.TransactionalOutbox.attempt": 1,
        "pmos.operations.TransactionalOutbox.acknowledge": 1,
    },
    "migration": {
        "pmos.migrations.create_legacy_fixture": 1,
        "pmos.migrations.migrate_workspace": 2,
        "pmos.store.Store.backup": 1,
        "pmos.store.Store.read_snapshot": 1,
    },
    "disaster_recovery": {
        "pmos.store.Store.backup": 1,
        "pmos.store.Store.restore": 1,
        "pmos.store.Store.assert_verified": 1,
        "pmos.store.Store.read_file": 1,
    },
    "security": {"pmos.hooks.decide": 3},
    "new_user": {
        "pmos.cli.main": 3,
        "pmos.conductor.Conductor.next_turn": 1,
        "pmos.domain.PMOSDomain.open": 2,
        "pmos.skills.SkillRegistry.load": 1,
        "pmos.operations.TransactionalOutbox.acknowledge": 1,
    },
}


def _result_errors(result: Any, *, require_execution: bool = True) -> tuple[str, ...]:
    """Validate results outside each case implementation; no self-attestation."""
    if type(result) is not UseCaseResult:
        return ("case did not return a UseCaseResult",)
    expected_assertions = _CASE_ASSERTIONS.get(result.use_case_id)
    expected_evidence = _CASE_EVIDENCE.get(result.use_case_id)
    if expected_assertions is None or expected_evidence is None:
        return ("unknown use-case result ID",)
    errors: list[str] = []
    if result.assertions != expected_assertions:
        errors.append("assertion contract does not match the registered use case")
    if not isinstance(result.evidence, Mapping) or set(result.evidence) != set(expected_evidence):
        errors.append("evidence keys do not match the registered use case")
        return tuple(errors)
    for key, expectation in expected_evidence.items():
        try:
            valid = expectation.predicate(result.evidence[key])
        except Exception:
            valid = False
        if valid is not True:
            errors.append("%s did not provide %s" % (key, expectation.description))
    if require_execution:
        if not isinstance(result._execution, Mapping):
            errors.append("execution proof is malformed")
        else:
            for call, minimum in _EXECUTION_REQUIREMENTS[result.use_case_id].items():
                count = result._execution.get(call)
                if (not isinstance(count, int) or isinstance(count, bool) or
                        count < minimum):
                    errors.append("required execution seam was not observed: %s" % call)
    return tuple(errors)


def _observed(case_id: str, **evidence: Any) -> UseCaseResult:
    """Build a result only after the typed matrix contract has observed it."""
    result = UseCaseResult(case_id, _CASE_ASSERTIONS.get(case_id, ()),
                           MappingProxyType(dict(evidence)))
    errors = _result_errors(result, require_execution=False)
    if errors:
        raise AssertionError("use-case evidence contract failed: " + "; ".join(errors))
    return result


def _result(*_args: Any, **_kwargs: Any) -> UseCaseResult:
    """Reject the legacy self-attested result factory rather than preserve it."""
    raise AssertionError("use cases must return contract-checked observed evidence via _observed")


class _DeterministicProvider:
    """A local provider implementation for deterministic, offline routing."""

    available = True

    def complete(self, model: str, prompt: str, **_: Any) -> ProviderResponse:
        # The router treats the adapter-reported identity as a trust boundary;
        # report the requested local model rather than rely on a fallback.
        return ProviderResponse("Draft: " + prompt.strip(), total_tokens=4,
                                actual_model=model)


def _domain() -> tuple[PMOSDomain, Any, Any, str]:
    domain = PMOSDomain()
    _org, product, owner, _membership = domain.bootstrap_workspace(
        "Readiness Org", "PM OS", "Readiness Owner")
    initiative = domain.create_initiative(
        product.id, "Core workflow", actor_id=owner.id)
    return domain, product, initiative, owner.id


def solo_manual() -> UseCaseResult:
    domain, product, initiative, actor = _domain()
    evidence = domain.create_evidence(
        initiative.id, "manual observation", "customer completed setup",
        actor_id=actor)
    initiative = domain.complete_gate(
        initiative.id, LifecycleStage.DISCOVER,
        evidence_ids=[evidence.id], actor_id=actor,
        expected_revision=initiative.revision)
    progressed = domain.transition_initiative(initiative.id, LifecycleStage.DEFINE,
                                              expected_revision=initiative.revision,
                                              actor_id=actor)
    links = domain.traces(evidence.id, actor_id=actor)
    return _observed("solo_manual", product_id=product.id, initiative_id=progressed.id,
                     evidence_id=evidence.id, trace_count=len(links), stage=progressed.stage.value)


def ai_drafting() -> UseCaseResult:
    domain, product, initiative, actor = _domain()
    router = ModelRouter(
        [ModelSpec("local", "deterministic-draft", capabilities={"text"},
                   context_window=2048, priority=0)],
        {"local": _DeterministicProvider()},
    )
    decision = router.route(RoutingRequest(prompt="Draft an outcome statement", task="draft",
                                           capabilities={"text"}))
    if decision.status is not RouteStatus.ROUTED or not decision.output:
        raise AssertionError("AI drafting route did not produce an output")
    created = domain.create_decision(
        initiative.id, "Drafted outcome", outcome=decision.output,
        actor_id=actor)
    return _observed("ai_drafting", model=decision.model, decision_id=created.id,
                     product_id=product.id)


def concurrent_team() -> UseCaseResult:
    domain, product, initiative, owner = _domain()
    pm = domain.create_user("PM", actor_id=owner)
    designer = domain.create_user("Designer", actor_id=owner)
    domain.add_membership(product.id, pm.id, "pm", actor_id=owner)
    domain.add_membership(product.id, designer.id, "contributor", actor_id=owner)
    assignment = domain.assign(initiative.id, designer.id, actor_id=pm.id)
    comment = domain.comment(initiative.id, "Please review the evidence", actor_id=pm.id)
    mention = domain.mention(initiative.id, designer.id, actor_id=pm.id, comment_id=comment.id)
    original_revision = initiative.revision
    domain.update("initiative", initiative.id, expected_revision=original_revision,
                  actor_id=pm.id, name="reviewed workflow")
    try:
        domain.update("initiative", initiative.id, expected_revision=original_revision,
                      actor_id=pm.id, name="stale write")
    except RevisionConflict:
        # A real concurrent edit must advance the revision before the stale
        # writer is rejected; exercise that path explicitly.
        pass
    else:
        raise AssertionError("stale concurrent write was accepted")
    return _observed("concurrent_team", assignment_id=assignment.id, mention_id=mention.id)


def portfolio() -> UseCaseResult:
    domain, product, _, actor = _domain()
    first = domain.create_initiative(product.id, "Growth", actor_id=actor)
    second = domain.create_initiative(product.id, "Reliability", actor_id=actor)
    domain.set_capacity(product.id, "Q1", 5, actor_id=actor)
    domain.allocate_capacity(first.id, "Q1", 3, actor_id=actor)
    domain.allocate_capacity(second.id, "Q1", 2, actor_id=actor)
    domain.score_initiative(first.id, 9, actor_id=actor)
    domain.score_initiative(second.id, 7, actor_id=actor)
    domain.sequence_initiative(first.id, 1, period="Q1", actor_id=actor)
    rollup = domain.rollup(product.id, "Q1", actor_id=actor)
    if rollup.get("capacity") != 5:
        raise AssertionError("portfolio rollup lost allocated capacity")

    second_product = domain.create_product(
        product.organization_id, "Platform", actor_id=actor)
    platform = domain.create_initiative(
        second_product.id, "Shared services", actor_id=actor)
    domain.set_capacity(second_product.id, "Q1", 4, actor_id=actor)
    domain.allocate_capacity(platform.id, "Q1", 4, actor_id=actor)
    domain.score_initiative(platform.id, 8, actor_id=actor)
    domain.sequence_initiative(platform.id, 1, period="Q1", actor_id=actor)
    portfolio_rollup = domain.rollup(period="Q1", actor_id=actor)
    visible_products = domain.list_entities("product", actor_id=actor)
    if (portfolio_rollup.get("capacity") != 9
            or portfolio_rollup.get("initiative_count") != 3
            or len(visible_products) != 2):
        raise AssertionError("multi-product portfolio rollup is incomplete")
    return _observed("portfolio", allocated_capacity=float(portfolio_rollup["capacity"]),
                     initiative_count=portfolio_rollup["initiative_count"],
                     product_count=len(visible_products))


def regulated() -> UseCaseResult:
    domain = PMOSDomain()
    _org, product, owner, _membership = domain.bootstrap_workspace(
        "Regulated Org", "Payments", "Product owner", regulated=True)
    initiative = domain.create_initiative(product.id, "KYC", actor_id=owner.id)
    approver = domain.create_user("Control owner", actor_id=owner.id)
    domain.add_membership(
        product.id, approver.id, "approver", actor_id=owner.id)
    for target in (LifecycleStage.DEFINE, LifecycleStage.DESIGN):
        stage_evidence = domain.create_evidence(
            initiative.id, "%s evidence" % initiative.stage.value,
            "%s complete" % initiative.stage.value, actor_id=owner.id)
        initiative = domain.complete_gate(
            initiative.id, initiative.stage, evidence_ids=[stage_evidence.id],
            actor_id=owner.id, expected_revision=initiative.revision)
        initiative = domain.transition_initiative(
            initiative.id, target, expected_revision=initiative.revision,
            actor_id=owner.id)

    evidence = domain.create_evidence(
        initiative.id, "design control test", "control-v1", actor_id=owner.id)
    try:
        domain.complete_gate(
            initiative.id, LifecycleStage.DESIGN,
            evidence_ids=[evidence.id], actor_id=owner.id,
            expected_revision=initiative.revision)
    except ApprovalError:
        blocked_without_approval = True
    else:
        raise AssertionError("regulated design gate accepted no approval")
    approval = domain.request_approval(
        initiative.id, evidence_ids=[evidence.id], policy_version="policy-v1",
        actor_id=owner.id)
    approved = domain.approve(approval.id, approver_id=approver.id, evidence_ids=[evidence.id])
    initiative = domain.complete_gate(
        initiative.id, LifecycleStage.DESIGN, evidence_ids=[evidence.id],
        approval_id=approved.id, actor_id=owner.id,
        expected_revision=initiative.revision)
    progressed = domain.transition_initiative(
        initiative.id, LifecycleStage.BUILD,
        expected_revision=initiative.revision, actor_id=owner.id)
    changed = domain.update("evidence", evidence.id, expected_revision=evidence.revision,
                            content="control-v2", actor_id=owner.id)
    invalidated = domain.get(approved.id, actor_id=owner.id)
    if invalidated.status != "invalidated":
        raise AssertionError("approval remained valid after evidence drift")
    return _observed("regulated", product_id=product.id,
                     blocked_without_approval=blocked_without_approval,
                     stage=progressed.stage.value,
                     changed_evidence_revision=changed.revision,
                     approval_status=invalidated.status)


def automation() -> UseCaseResult:
    with tempfile.TemporaryDirectory(prefix="pmos-usecase-") as directory:
        with Store(Path(directory) / "queue.sqlite") as store:
            store.create_product("automation-product")
            queued = store.enqueue({"action": "refresh_metrics"}, idempotency_key="refresh-1",
                                   available_at=0)
            lease = store.lease_next("worker-1", now=10)
            if lease is None or lease.job.job_id != queued.job_id:
                raise AssertionError("queued work was not leased")
            completed = store.succeed(lease.job.job_id, lease.token, lease.generation,
                                      {"refreshed": True}, now=11)
            if not completed.ok or completed.job is None or completed.job.status is not QueueStatus.SUCCEEDED:
                raise AssertionError("automation result was not durably completed")
            job_id = completed.job.job_id
    return _observed("automation", job_id=job_id, status=QueueStatus.SUCCEEDED.value)


def analytics_experiments() -> UseCaseResult:
    analytics = AnalyticsAdapter()
    observation = analytics.ingest_metric({
        "metric_id": "activation", "value": 0.42, "unit": "ratio",
        "definition": "users completing setup", "source": "warehouse",
        "observed_at": 90, "freshness_seconds": 20,
        "lineage_hash": hashlib.sha256(b"warehouse-query-v1").hexdigest(),
    }, now=100)
    outcome = analytics.record_experiment_outcome(ExperimentRef("experiment-1"),
                                                  DecisionRef("decision-1"),
                                                  {"result": "ship"}, recorded_at=100)
    return _observed("analytics_experiments", metric_id=observation.metric_id,
                     experiment_id=outcome.experiment.id, decision_id=outcome.decision.id)


def research() -> UseCaseResult:
    research_store = ResearchStorageAdapter(retention_seconds=20, clock=lambda: 100)
    research_store.record_consent("participant-1", {"interview", "quote"}, "consent-v1",
                                  granted_at=90, expires_at=200)
    research_store.recruit("participant-1", now=95)
    evidence = research_store.store_evidence("participant-1", "observed behavior", captured_at=96,
                                             lineage_hash="a" * 64)
    if research_store.quote_evidence(evidence.id, now=100) != "observed behavior":
        raise AssertionError("consented evidence could not be quoted")
    redacted = research_store.redact_evidence(evidence.id)
    if not redacted.redacted:
        raise AssertionError("research redaction was not recorded")
    return _observed("research", evidence_id=evidence.id, redacted=redacted.redacted)


def integrations() -> UseCaseResult:
    issues = IssueTrackingAdapter()
    source = SourceControlAdapter()
    issue = issues.create_issue("Implement onboarding", description="first-run path")
    branch = source.create_branch("feature/onboarding")
    commit = source.record_commit(branch["name"], "Add onboarding", tree_hash="b" * 64)
    outbox = TransactionalOutbox()
    event = outbox.enqueue("issue.created", {"issue_id": issue["id"], "commit": commit["id"]},
                           idempotency_key="integration-1")
    delivered = outbox.attempt(event.id, lambda payload: "external-event-1", now=0)
    if not delivered.external_id:
        raise AssertionError("integration outbox did not deliver")
    acknowledged = outbox.acknowledge(delivered.id, external_id=delivered.external_id, now=1)
    return _observed("integrations", issue_id=issue["id"], branch=branch["name"],
                     external_id=delivered.external_id, outbox_status=acknowledged.status.value)


def migration() -> UseCaseResult:
    with tempfile.TemporaryDirectory(prefix="pmos-migration-") as directory:
        root = Path(directory)
        legacy = create_legacy_fixture(root / "legacy", product_id="migration-product")
        destination = root / "destination"
        runtime = destination / ".pmos/runtime.sqlite"
        # Seed a real runtime so the migration must create and retain a backup
        # rather than only importing a convenient in-memory commit pack.
        with Store(runtime) as existing:
            existing.create_product("migration-product")
        planned = migrate_workspace(legacy, destination, product_id="migration-product", dry_run=True)
        if planned.status != "planned" or not planned.dry_run or planned.plan.file_count < 2:
            raise AssertionError("migration dry run did not create a bounded legacy plan")
        migrated = migrate_workspace(legacy, destination, product_id="migration-product")
        if migrated.status != "migrated" or not migrated.backup:
            raise AssertionError("public migration API did not activate with a backup")
        with Store(runtime) as reopened:
            reopened.assert_verified()
            snapshot = reopened.read_snapshot("migration-product")
            if snapshot.files.get("STATE.md", b"").splitlines()[:1] != [b"# Legacy state"]:
                raise AssertionError("migrated runtime did not retain legacy state")
            revision = snapshot.head.revision
            file_count = len(snapshot.files)
    return _observed("migration", status=migrated.status, backup_created=migrated.backup is not None,
                     runtime_verified=True, migrated_revision=revision,
                     migrated_file_count=file_count)


def disaster_recovery() -> UseCaseResult:
    with tempfile.TemporaryDirectory(prefix="pmos-recovery-") as directory:
        root = Path(directory)
        backup = root / "backup.sqlite"
        with Store(root / "live.sqlite") as live:
            live.create_product("recovery-product")
            live.commit("recovery-product", {"state.json": "durable"}, expected_revision=0)
            live.backup(backup)
        with Store.restore(backup, root / "restored.sqlite") as restored:
            restored.assert_verified()
            if restored.read_file("recovery-product", "state.json") != b"durable":
                raise AssertionError("restored state differs from durable state")
            revision = restored.head("recovery-product").revision
    return _observed("disaster_recovery", revision=revision, verified=True)


def security() -> UseCaseResult:
    secret = decide("PreToolUse", {"tool_name": "Bash", "tool_input": {
        "command": "python -c 'print(1)'", "token": "sk-or-v1-" + "x" * 32}}, repo_root=".")
    outside = decide("PreToolUse", {"tool_name": "Write", "tool_input": {
        "file_path": "/tmp/not-project.txt"}}, repo_root=".")
    external = decide("PreToolUse", {"tool_name": "Bash", "tool_input": {
        "command": "git push origin main"}}, repo_root=".")
    if secret.action != "deny" or outside.action != "deny" or external.action != "ask":
        raise AssertionError("security hooks did not fail closed")
    return _observed("security", secret_action=secret.action,
                     outside_action=outside.action, external_action=external.action)


def new_user() -> UseCaseResult:
    """Exercise the public runtime boundary as one durable golden slice.

    This deliberately crosses CLI -> Store -> Conductor, opens an independent
    durable Domain in the same Store, validates a packaged skill, checks a
    runtime hook, and completes an exact-ID outbox acknowledgement. It is not
    a hosted-provider or human-approval attestation.
    """
    with tempfile.TemporaryDirectory(prefix="pmos-new-user-") as directory:
        root = Path(directory)
        product_id = "onboarding-product"

        def cli_json(arguments: list[str]) -> Mapping[str, Any]:
            stream = StringIO()
            with redirect_stdout(stream):
                exit_code = cli_main(["--json", *arguments])
            try:
                payload = json.loads(stream.getvalue())
            except json.JSONDecodeError as exc:
                raise AssertionError("CLI did not return JSON evidence") from exc
            if exit_code != 0 or payload.get("ok") is not True:
                raise AssertionError("CLI boundary did not report successful execution")
            return payload

        initialized = cli_json(["init", "--path", str(root), "--product-id", product_id])
        initial_revision = initialized["onboarding"]["revision"]
        answer = cli_json([
            "answer", "--path", str(root), "--product-id", product_id,
            "--question-id", "first-outcome", "--answer", "A customer completes setup.",
            "--evidence", json.dumps({"class": "observed_behavior", "source": "session-1",
                                        "date": "2026-09-04", "location": "research/1"}),
            "--expected-revision", initial_revision, "--turn-id", "golden-answer-1",
        ])
        proof = root / "onboarding-proof.txt"
        proof_bytes = b"independent onboarding approval\n"
        proof.write_bytes(proof_bytes)
        gated = cli_json([
            "gate", "--path", str(root), "--product-id", product_id,
            "--bank-id", "onboarding",
            "--evidence", json.dumps({
                "source": proof.name, "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                "actor_id": "local-reviewer", "requester_id": "local-operator",
                "decision": "approved", "approved_at": "2026-09-04T00:00:00Z",
            }),
            "--expected-revision", answer["outcome"]["revision"], "--turn-id", "golden-gate-1",
        ])
        runtime = root / ".pmos/runtime.sqlite"
        with Store(runtime) as store:
            store.assert_verified()
            onboarding = Conductor(store, product_id, (
                QuestionBank("onboarding", "v1", (
                    Question("first-outcome", "What outcome should the first product user achieve?",
                             EvidenceClass.OBSERVED_BEHAVIOR),
                ), gate_approvers=("local-reviewer",)),
            ))
            if onboarding.next_turn().status != "completed":
                raise AssertionError("CLI conductor state did not survive Store reopen")

            domain = PMOSDomain.open(store, storage_id="golden-domain")
            _organization, product, owner, _membership = domain.bootstrap_workspace(
                "Golden Org", "Golden Product", "Golden Owner")
            initiative = domain.create_initiative(product.id, "First workflow", actor_id=owner.id)
            evidence = domain.create_evidence(initiative.id, "Observed setup", "completed",
                                              actor_id=owner.id)
            domain.complete_gate(initiative.id, LifecycleStage.DISCOVER,
                                 evidence_ids=[evidence.id], actor_id=owner.id,
                                 expected_revision=initiative.revision)
            hook = decide("before_transition", {
                "actor_id": owner.id, "expected_revision": 1,
                "gate_evidence_hashes": [evidence.content_hash],
            }, repo_root=root)
            if hook.action != "allow":
                raise AssertionError("runtime transition hook rejected valid durable evidence")

            contracts = SkillRegistry().load()
            if "lifecycle-conductor" not in contracts:
                raise AssertionError("trusted lifecycle skill was not available")

            issue = IssueTrackingAdapter().create_issue("Finish onboarding")
            outbox = TransactionalOutbox()
            queued = outbox.enqueue("issue.created", {"issue_id": issue["id"]},
                                    idempotency_key="golden-issue-1")
            delivered = outbox.attempt(queued.id, lambda _event: "golden-external-1", now=0)
            acknowledged = outbox.acknowledge(delivered.id, external_id="golden-external-1", now=1)
            if acknowledged.status.value != "acknowledged":
                raise AssertionError("operation delivery was not exactly acknowledged")

        with Store(runtime) as reopened_store:
            reopened_store.assert_verified()
            reopened_domain = PMOSDomain.open(reopened_store, storage_id="golden-domain")
            if reopened_domain.get(initiative.id, actor_id=owner.id).id != initiative.id:
                raise AssertionError("durable domain state did not survive Store reopen")
            domain_reopened = True
            store_verified = reopened_store.verify().ok
    return _observed("new_user", cli_initialized=initialized["ok"] is True,
                     cli_completed=gated["outcome"]["completed"] is True,
                     store_verified=store_verified, conductor_completed=True,
                     domain_reopened=domain_reopened, hook_action=hook.action,
                     skill_contract_count=len(contracts), operations_status=acknowledged.status.value)


_IMPLEMENTATIONS: Mapping[str, Callable[[], UseCaseResult]] = {
    "solo_manual": solo_manual,
    "ai_drafting": ai_drafting,
    "concurrent_team": concurrent_team,
    "portfolio": portfolio,
    "regulated": regulated,
    "automation": automation,
    "analytics_experiments": analytics_experiments,
    "research": research,
    "integrations": integrations,
    "migration": migration,
    "disaster_recovery": disaster_recovery,
    "security": security,
    "new_user": new_user,
}


def validate_registry() -> tuple[str, ...]:
    """Prove the executable registry is exactly the mandatory matrix."""
    registered = tuple(_IMPLEMENTATIONS)
    if registered != USE_CASE_IDS or set(registered) != set(USE_CASE_IDS):
        raise AssertionError("use-case registry does not cover exactly the mandatory IDs")
    if any(not callable(_IMPLEMENTATIONS[case_id]) for case_id in USE_CASE_IDS):
        raise AssertionError("use-case registry contains a non-executable row")
    return registered


def run_use_case(use_case_id: str) -> UseCaseResult:
    validate_registry()
    try:
        implementation = _IMPLEMENTATIONS[use_case_id]
    except KeyError as exc:
        raise ValueError("unknown use-case ID: %s" % use_case_id) from exc
    calls: Counter[str] = Counter()
    previous_profile = sys.getprofile()

    def observe(frame: Any, event: str, arg: Any) -> None:
        if previous_profile is not None:
            previous_profile(frame, event, arg)
        if event != "call":
            return
        module = frame.f_globals.get("__name__", "")
        if not isinstance(module, str) or not module.startswith("pmos."):
            return
        name = frame.f_code.co_name
        # Store's serialized wrapper preserves the public function metadata,
        # but the executing code object is the wrapper. Resolve the closed-over
        # method without retaining caller arguments or other frame content.
        method = frame.f_locals.get("method") if name == "guarded" else None
        if callable(method) and isinstance(getattr(method, "__qualname__", None), str):
            name = method.__qualname__
        else:
            owner = frame.f_locals.get("self")
            if owner is not None and type(owner).__module__ == module:
                name = type(owner).__qualname__ + "." + name
            else:
                owner_type = frame.f_locals.get("cls")
                if isinstance(owner_type, type) and owner_type.__module__ == module:
                    name = owner_type.__qualname__ + "." + name
        calls[module + "." + name] += 1

    sys.setprofile(observe)
    try:
        result = implementation()
    finally:
        sys.setprofile(previous_profile)
    if type(result) is UseCaseResult:
        result = replace(result, _execution=MappingProxyType(dict(calls)))
    if result.use_case_id != use_case_id:
        raise AssertionError("use-case returned an ID different from its registered row")
    errors = _result_errors(result)
    if errors:
        raise AssertionError("use-case did not satisfy its observed-evidence contract: " + "; ".join(errors))
    return result


def run_all() -> tuple[UseCaseResult, ...]:
    """Run every mandatory row, preserving registry order."""
    return tuple(run_use_case(case_id) for case_id in validate_registry())


__all__ = [
    "USE_CASE_IDS", "UseCaseResult", "validate_registry", "run_use_case", "run_all",
    "solo_manual", "ai_drafting", "concurrent_team", "portfolio", "regulated",
    "automation", "analytics_experiments", "research", "integrations", "migration",
    "disaster_recovery", "security", "new_user",
]
