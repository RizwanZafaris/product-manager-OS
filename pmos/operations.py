"""Safe, deterministic operations and integration primitives for PMOS.

This module is deliberately a standard-library-only seam.  The adapters are
in-memory doubles with explicit contracts; they do not make network calls,
execute commands, or retain credentials.  A host may replace an adapter after
validating the same contract and schema/capability versions.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import threading
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Optional


CONTRACT_VERSION = "pmos.operations.contract.v1"
SCHEMA_VERSION = "pmos.operations.schema.v1"
CAPABILITY_VERSION = "pmos.operations.capabilities.v1"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_KEYS = frozenset({
    "password", "secret", "token", "credential", "credentials",
    "api_key", "apikey", "access_key", "private_key", "shell_command",
    "command", "commands",
})
_SECRET_VALUE_PATTERNS = (
    re.compile(r"\bsk-or-v1-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*"
               r"[\"']?[A-Za-z0-9_+/=-]{20,}"),
)
MAX_TEXT_CHARS = 16 * 1024
MAX_IDENTIFIER_CHARS = 512
MAX_COLLECTION_ITEMS = 256
MAX_PAYLOAD_DEPTH = 8
MAX_CANONICAL_PAYLOAD_BYTES = 64 * 1024
MAX_IN_MEMORY_RECORDS = 4096
_ISSUE_STATUSES = frozenset({"open", "in_progress", "blocked", "closed"})


class OperationsError(Exception):
    """Base class for expected, safe operations failures."""


class ContractViolation(OperationsError):
    pass


class IdempotencyConflict(OperationsError):
    pass


class OutboxError(OperationsError):
    pass


class DataValidationError(OperationsError):
    pass


class ConsentError(OperationsError):
    pass


class RetentionError(OperationsError):
    pass


class QuoteRefused(ConsentError):
    pass


# Conventional aliases keep the boundary pleasant to consume alongside
# ``pmos.store`` and ``pmos.domain`` without creating a second error taxonomy.
ValidationError = DataValidationError
AdapterContractError = ContractViolation
OutboxConflict = IdempotencyConflict


class AdapterState(str, Enum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class OutboxStatus(str, Enum):
    QUEUED = "queued"
    RETRY_WAIT = "retry_wait"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    DEAD_LETTER = "dead_letter"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class AdapterContract:
    name: str
    contract_version: str = CONTRACT_VERSION
    schema_version: str = SCHEMA_VERSION
    capability_version: str = CAPABILITY_VERSION
    capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ContractViolation("adapter contract needs a name")
        caps = tuple(sorted(set(str(item) for item in self.capabilities)))
        object.__setattr__(self, "capabilities", caps)


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise DataValidationError("payload is not canonical JSON") from exc


def payload_hash(value: Any) -> str:
    _assert_safe(value)
    return hashlib.sha256(_canonical(value)).hexdigest()


def _text(value: Any, label: str, *, allow_empty: bool = False,
          maximum: int = MAX_TEXT_CHARS) -> str:
    if (not isinstance(value, str) or "\x00" in value or len(value) > maximum or
            (not allow_empty and not value.strip())):
        raise DataValidationError("%s must be a bounded %sstring" % (
            label, "possibly empty " if allow_empty else "non-empty "))
    return value


def _assert_safe(value: Any, *, key: str = "", depth: int = 0) -> None:
    """Reject credentials, commands, unbounded, and noncanonical payloads."""
    if depth > MAX_PAYLOAD_DEPTH:
        raise DataValidationError("payload nesting exceeds the safe bound")
    normalized_key = key.lower().replace("-", "_")
    if (normalized_key in _FORBIDDEN_KEYS or normalized_key.endswith("_token") or
            normalized_key in {"authorization", "headers", "auth_header"}):
        raise DataValidationError("credentials and shell commands are not storable")
    if isinstance(value, Mapping):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise DataValidationError("payload mapping exceeds the safe bound")
        for item_key, item_value in value.items():
            if not isinstance(item_key, str):
                raise DataValidationError("payload keys must be strings")
            _text(item_key, "payload key", maximum=MAX_IDENTIFIER_CHARS)
            _assert_safe(item_value, key=item_key, depth=depth + 1)
    elif isinstance(value, (list, tuple)):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise DataValidationError("payload collection exceeds the safe bound")
        for item in value:
            _assert_safe(item, depth=depth + 1)
    elif isinstance(value, str):
        _text(value, "payload value", allow_empty=True)
        if any(pattern.search(value) for pattern in _SECRET_VALUE_PATTERNS):
            raise DataValidationError("credentials and shell commands are not storable")
    elif value is not None and not isinstance(value, (bool, int, float)):
        raise DataValidationError("payload values must be JSON primitives, mappings, or sequences")
    elif isinstance(value, float) and not math.isfinite(value):
        raise DataValidationError("payload numbers must be finite")
    if depth == 0 and len(_canonical(value)) > MAX_CANONICAL_PAYLOAD_BYTES:
        raise DataValidationError("canonical payload exceeds the safe bound")


def _copy(value: Any) -> Any:
    return copy.deepcopy(value)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _now(value: Optional[float]) -> float:
    current = time.time() if value is None else _timestamp(value)
    if not math.isfinite(current):
        raise DataValidationError("timestamp must be finite")
    return current


def _reserve_record(current_count: int, label: str) -> None:
    if current_count >= MAX_IN_MEMORY_RECORDS:
        raise DataValidationError("%s exceeds the in-memory record limit" % label)


def _timestamp(value: Any) -> float:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise DataValidationError("timestamp is not ISO-8601") from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.timestamp()
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        return float(value)
    raise DataValidationError("timestamp must be numeric or ISO-8601")


class BaseAdapter:
    """Common surface shared by every deterministic adapter."""

    contract: AdapterContract

    def __init__(self, contract: AdapterContract) -> None:
        self.contract = contract
        self.state = AdapterState.AVAILABLE
        self.state_reason = ""

    @property
    def schema_version(self) -> str:
        return self.contract.schema_version

    @property
    def capability_version(self) -> str:
        return self.contract.capability_version

    @property
    def capabilities(self) -> tuple[str, ...]:
        return self.contract.capabilities

    def health(self) -> Mapping[str, str]:
        return {"state": self.state.value, "reason": self.state_reason}

    def set_state(self, state: AdapterState | str, reason: str = "") -> None:
        try:
            self.state = AdapterState(state)
        except (TypeError, ValueError) as exc:
            raise DataValidationError("unknown adapter state") from exc
        reason_text = _text(reason, "adapter state reason", allow_empty=True)
        _assert_safe({"reason": reason_text})
        self.state_reason = reason_text

    def _require_available(self) -> None:
        if self.state is AdapterState.UNAVAILABLE:
            raise OutboxError("adapter is unavailable")


def validate_adapter(adapter: Any, *, expected_name: Optional[str] = None) -> AdapterContract:
    """Validate a versioned adapter before it is installed in a host.

    Validation is intentionally strict: a similarly named object is not a
    contract.  ``BaseAdapter`` subclasses can be tested with this function,
    while a bad adapter fails closed with ``ContractViolation``.
    """
    contract = getattr(adapter, "contract", None)
    if not isinstance(contract, AdapterContract):
        raise ContractViolation("adapter has no AdapterContract")
    if expected_name is not None and contract.name != expected_name:
        raise ContractViolation("unexpected adapter kind")
    if contract.contract_version != CONTRACT_VERSION:
        raise ContractViolation("unsupported contract version")
    if contract.schema_version != SCHEMA_VERSION:
        raise ContractViolation("unsupported schema version")
    if contract.capability_version != CAPABILITY_VERSION:
        raise ContractViolation("unsupported capability version")
    if not isinstance(contract.capabilities, tuple):
        raise ContractViolation("capabilities must be immutable")
    for name in ("health", "set_state"):
        if not callable(getattr(adapter, name, None)):
            raise ContractViolation("adapter is missing %s" % name)
    return contract


class IssueTrackingAdapter(BaseAdapter):
    def __init__(self) -> None:
        super().__init__(AdapterContract(
            "issue_tracking", capabilities=("issue.create", "issue.read", "issue.update")))
        self._issues: dict[str, dict[str, Any]] = {}
        self._sequence = 0

    @staticmethod
    def _issue_fields(title: Any, description: Any, labels: Any, status: Any = "open") -> dict[str, Any]:
        title_text = _text(title, "issue title")
        description_text = _text(description, "issue description", allow_empty=True)
        if isinstance(labels, str):
            raise DataValidationError("issue labels must be a collection of strings")
        try:
            normalized_labels = tuple(sorted({_text(item, "issue label", maximum=256)
                                              for item in labels}))
        except TypeError as exc:
            raise DataValidationError("issue labels must be a collection of strings") from exc
        if len(normalized_labels) > MAX_COLLECTION_ITEMS:
            raise DataValidationError("issue labels exceed the safe bound")
        if not isinstance(status, str) or status not in _ISSUE_STATUSES:
            raise DataValidationError("issue status is invalid")
        fields = {"title": title_text, "description": description_text,
                  "labels": normalized_labels, "status": status}
        _assert_safe(fields)
        return fields

    def create_issue(self, title: str, *, description: str = "", labels: Iterable[str] = ()) -> Mapping[str, Any]:
        self._require_available()
        fields = self._issue_fields(title, description, labels)
        _reserve_record(len(self._issues), "issues")
        self._sequence += 1
        issue = {"id": "issue-%06d" % self._sequence, **fields, "revision": 1}
        _assert_safe(issue)
        self._issues[issue["id"]] = issue
        return _copy(issue)

    create = create_issue

    def get_issue(self, issue_id: str) -> Optional[Mapping[str, Any]]:
        item = self._issues.get(issue_id)
        return _copy(item) if item else None

    def update_issue(self, issue_id: str, *, expected_revision: int, **changes: Any) -> Mapping[str, Any]:
        self._require_available()
        item = self._issues.get(issue_id)
        if item is None:
            raise DataValidationError("issue not found")
        if (not isinstance(expected_revision, int) or isinstance(expected_revision, bool) or
                expected_revision < 1):
            raise DataValidationError("issue revision must be a positive integer")
        if item["revision"] != expected_revision:
            raise IdempotencyConflict("issue revision conflict")
        allowed = {"title", "description", "labels", "status"}
        if not changes or set(changes) - allowed:
            raise DataValidationError("issue updates may change only title, description, labels, or status")
        updated_fields = self._issue_fields(
            changes.get("title", item["title"]),
            changes.get("description", item["description"]),
            changes.get("labels", item["labels"]),
            changes.get("status", item["status"]),
        )
        changed = dict(item)
        changed.update(updated_fields)
        changed["revision"] += 1
        _assert_safe(changed)
        self._issues[issue_id] = changed
        return _copy(changed)

    def list_issues(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(_copy(self._issues[key]) for key in sorted(self._issues))


class SourceControlAdapter(BaseAdapter):
    def __init__(self) -> None:
        super().__init__(AdapterContract(
            "source_control", capabilities=("branch.create", "commit.record", "commit.read")))
        self._branches: dict[str, str] = {"main": "0" * 40}
        self._commits: dict[str, dict[str, Any]] = {}

    def create_branch(self, name: str, *, from_commit: str = "0" * 40) -> Mapping[str, str]:
        self._require_available()
        if (not _text(name, "branch name", maximum=256) or name in self._branches or
                not _valid_commit(from_commit)):
            raise DataValidationError("invalid or duplicate branch")
        _assert_safe({"branch": name, "from_commit": from_commit})
        _reserve_record(len(self._branches) + len(self._commits), "source-control records")
        self._branches[name] = from_commit
        return {"name": name, "head": from_commit}

    def record_commit(self, branch: str, message: str, *, tree_hash: str) -> Mapping[str, str]:
        self._require_available()
        if (not isinstance(branch, str) or branch not in self._branches or
                not _text(message, "commit message") or not _valid_hash(tree_hash)):
            raise DataValidationError("invalid commit input")
        _reserve_record(len(self._branches) + len(self._commits), "source-control records")
        parent = self._branches[branch]
        commit = hashlib.sha1(_canonical({"branch": branch, "message": message,
                                          "parent": parent, "tree": tree_hash})).hexdigest()
        record = {"id": commit, "branch": branch, "message": message,
                  "parent": parent, "tree_hash": tree_hash}
        _assert_safe(record)
        self._commits[commit] = record
        self._branches[branch] = commit
        return _copy(record)

    commit = record_commit

    def get_commit(self, commit_id: str) -> Optional[Mapping[str, Any]]:
        item = self._commits.get(commit_id)
        return _copy(item) if item else None


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_HEX64.fullmatch(value))


def _valid_commit(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{40}", value))


@dataclass(frozen=True)
class MetricObservation:
    metric_id: str
    value: float
    unit: str
    definition: str
    source: str
    observed_at: float
    freshness_seconds: float
    lineage_hash: str
    experiment_id: Optional[str] = None
    decision_id: Optional[str] = None


@dataclass(frozen=True)
class ExperimentRef:
    id: str
    type: str = "experiment"


@dataclass(frozen=True)
class DecisionRef:
    id: str
    type: str = "decision"


@dataclass(frozen=True)
class ExperimentOutcome:
    experiment: ExperimentRef
    decision: DecisionRef
    result: Mapping[str, Any]
    recorded_at: float

    @property
    def experiment_id(self) -> str:
        return self.experiment.id

    @property
    def decision_id(self) -> str:
        return self.decision.id

    @property
    def experiment_type(self) -> str:
        return self.experiment.type

    @property
    def decision_type(self) -> str:
        return self.decision.type


class AnalyticsAdapter(BaseAdapter):
    def __init__(self) -> None:
        super().__init__(AdapterContract(
            "analytics", capabilities=("metric.ingest", "experiment.outcome")))
        self._metrics: list[MetricObservation] = []
        self._outcomes: list[ExperimentOutcome] = []

    def ingest_metric(self, observation: MetricObservation | Mapping[str, Any] | None = None, *,
                      now: Optional[float] = None, **fields: Any) -> MetricObservation:
        if observation is None:
            observation = fields
        elif fields:
            raise DataValidationError("metric fields cannot accompany an observation")
        raw = dict(observation) if isinstance(observation, Mapping) else observation
        if isinstance(raw, dict):
            try:
                raw = MetricObservation(**raw)
            except TypeError as exc:
                raise DataValidationError("metric schema is incomplete") from exc
        if not isinstance(raw, MetricObservation):
            raise DataValidationError("metric observation has an invalid type")
        try:
            raw = replace(raw, observed_at=_timestamp(raw.observed_at),
                          freshness_seconds=float(raw.freshness_seconds))
        except (TypeError, ValueError) as exc:
            raise DataValidationError("metric timestamp or freshness is invalid") from exc
        metric_id = _text(raw.metric_id, "metric id", maximum=MAX_IDENTIFIER_CHARS)
        unit = _text(raw.unit, "metric unit", maximum=256)
        definition = _text(raw.definition, "metric definition")
        source = _text(raw.source, "metric source", maximum=MAX_IDENTIFIER_CHARS)
        if source.lower() in {"unknown", "unproven", "synthetic"}:
            raise DataValidationError("metric source is unproven")
        if not isinstance(raw.value, (int, float)) or isinstance(raw.value, bool) or not math.isfinite(raw.value):
            raise DataValidationError("metric value must be finite")
        if raw.freshness_seconds <= 0 or not math.isfinite(raw.freshness_seconds):
            raise DataValidationError("freshness must be positive")
        if not _valid_hash(raw.lineage_hash):
            raise DataValidationError("metric lineage hash is required")
        current = _now(now)
        if raw.observed_at > current:
            raise DataValidationError("future metric observations are rejected")
        if current - raw.observed_at > raw.freshness_seconds:
            raise DataValidationError("stale metric observation")
        raw = replace(raw, metric_id=metric_id, unit=unit, definition=definition,
                      source=source)
        _assert_safe({
            "metric_id": raw.metric_id, "value": raw.value, "unit": raw.unit,
            "definition": raw.definition, "source": raw.source,
            "observed_at": raw.observed_at, "freshness_seconds": raw.freshness_seconds,
            "lineage_hash": raw.lineage_hash, "experiment_id": raw.experiment_id,
            "decision_id": raw.decision_id,
        })
        self._require_available()
        _reserve_record(len(self._metrics) + len(self._outcomes), "analytics records")
        self._metrics.append(raw)
        return raw

    ingest = ingest_metric

    def record_experiment_outcome(self, experiment: ExperimentRef | Mapping[str, Any] | str | None = None,
                                  decision: DecisionRef | Mapping[str, Any] | str | None = None,
                                  result: Optional[Mapping[str, Any]] = None, *,
                                  experiment_id: Optional[str] = None,
                                  decision_id: Optional[str] = None,
                                  recorded_at: Optional[float] = None) -> ExperimentOutcome:
        if experiment is None:
            experiment = experiment_id
        if decision is None:
            decision = decision_id
        if result is None:
            raise DataValidationError("experiment result is required")
        exp = _typed_ref(experiment, ExperimentRef, "experiment")
        dec = _typed_ref(decision, DecisionRef, "decision")
        if not isinstance(result, Mapping) or not result:
            raise DataValidationError("experiment result is required")
        _assert_safe(result)
        stamp = _now(recorded_at)
        if stamp > time.time():
            raise DataValidationError("experiment outcome timestamp cannot be in the future")
        self._require_available()
        _reserve_record(len(self._metrics) + len(self._outcomes), "analytics records")
        outcome = ExperimentOutcome(exp, dec, _freeze(_copy(dict(result))), stamp)
        self._outcomes.append(outcome)
        return outcome

    @property
    def metrics(self) -> tuple[MetricObservation, ...]:
        return tuple(self._metrics)

    @property
    def outcomes(self) -> tuple[ExperimentOutcome, ...]:
        return tuple(self._outcomes)


def _typed_ref(value: Any, cls: Any, expected: str) -> Any:
    if isinstance(value, cls):
        ref = value
    elif isinstance(value, Mapping):
        try:
            ref = cls(id=value["id"], type=value.get("type", expected))
        except (KeyError, TypeError) as exc:
            raise DataValidationError("typed reference is incomplete") from exc
    elif isinstance(value, str):
        ref = cls(value)
    else:
        raise DataValidationError("typed reference is required")
    if (not isinstance(ref.type, str) or ref.type != expected):
        raise DataValidationError("reference type does not match")
    _text(ref.id, "%s id" % expected, maximum=MAX_IDENTIFIER_CHARS)
    return ref


@dataclass(frozen=True)
class ParticipantConsent:
    participant_id: str
    scope: frozenset[str]
    version: str
    granted_at: float
    expires_at: Optional[float] = None
    withdrawn_at: Optional[float] = None

    @property
    def active(self) -> bool:
        return self.withdrawn_at is None

    @property
    def consent_scope(self) -> frozenset[str]:
        return self.scope

    @property
    def consent_version(self) -> str:
        return self.version


@dataclass(frozen=True)
class ResearchEvidence:
    id: str
    participant_id: str
    content: str
    scope: str
    captured_at: float
    lineage_hash: str
    retention_until: Optional[float]
    redacted: bool = False
    tombstone: bool = False

    @property
    def evidence_lineage_hash(self) -> str:
        return self.lineage_hash

    @property
    def deleted(self) -> bool:
        return self.tombstone


class ResearchStorageAdapter(BaseAdapter):
    STATUSES = frozenset({"recruiting", "enrolled", "paused", "withdrawn", "completed", "rejected"})

    def __init__(self, *, retention_seconds: float = 86400.0, clock: Optional[Callable[[], float]] = None) -> None:
        super().__init__(AdapterContract(
            "research_storage", capabilities=("consent.record", "participant.recruit",
                                                "evidence.store", "evidence.redact", "participant.delete",
                                                "quote.read")))
        if (not isinstance(retention_seconds, (int, float)) or isinstance(retention_seconds, bool) or
                not math.isfinite(retention_seconds) or retention_seconds <= 0):
            raise DataValidationError("retention must be positive")
        self.retention_seconds = float(retention_seconds)
        self._clock = clock or time.time
        self._consents: dict[str, ParticipantConsent] = {}
        self._statuses: dict[str, str] = {}
        self._evidence: dict[str, ResearchEvidence] = {}
        self._sequence = 0

    def record_consent(self, participant_id: str, scope: Iterable[str], version: str,
                       *, granted_at: Optional[float] = None, expires_at: Optional[float] = None) -> ParticipantConsent:
        try:
            values = (scope,) if isinstance(scope, str) else tuple(scope)
        except TypeError as exc:
            raise ConsentError("consent scope must be a collection of strings") from exc
        if len(values) > MAX_COLLECTION_ITEMS:
            raise ConsentError("consent scope exceeds the safe bound")
        try:
            scopes = frozenset(_text(item, "consent scope", maximum=256) for item in values)
            participant = _text(participant_id, "participant id", maximum=MAX_IDENTIFIER_CHARS)
            consent_version = _text(version, "consent version", maximum=256)
        except DataValidationError as exc:
            raise ConsentError("participant, consent scope, and version are required") from exc
        current = _now(self._clock() if granted_at is None else granted_at)
        wall_clock = _now(self._clock())
        expiry = _timestamp(expires_at) if expires_at is not None else None
        if not scopes:
            raise ConsentError("participant, consent scope, and version are required")
        if current > wall_clock:
            raise ConsentError("consent timestamp cannot be in the future")
        if expiry is not None and expiry <= current:
            raise ConsentError("consent expiry must follow grant")
        _assert_safe({"participant_id": participant, "scope": tuple(sorted(scopes)),
                      "version": consent_version, "granted_at": current, "expires_at": expiry})
        if participant not in self._consents:
            _reserve_record(len(self._consents) + len(self._evidence), "research records")
        consent = ParticipantConsent(participant, scopes, consent_version, current, expiry)
        self._consents[participant] = consent
        self._statuses.setdefault(participant, "recruiting")
        return consent

    # Alias useful to hosts that call this operation grant_consent.
    grant_consent = record_consent

    def withdraw_consent(self, participant_id: str, *, withdrawn_at: Optional[float] = None) -> int:
        """Withdraw consent and tombstone linked evidence immediately."""
        return self.delete_participant(participant_id, deleted_at=withdrawn_at)

    def set_recruiting_status(self, participant_id: str, status: str) -> str:
        participant = _text(participant_id, "participant id", maximum=MAX_IDENTIFIER_CHARS)
        if not isinstance(status, str) or status not in self.STATUSES:
            raise DataValidationError("unknown recruiting status")
        if participant not in self._consents:
            raise ConsentError("consent is required before recruiting")
        self._statuses[participant] = status
        return status

    set_status = set_recruiting_status

    def recruit(self, participant_id: str, *, required_scope: str = "interview", now: Optional[float] = None) -> str:
        current = _now(now if now is not None else self._clock())
        participant = _text(participant_id, "participant id", maximum=MAX_IDENTIFIER_CHARS)
        required = _text(required_scope, "required consent scope", maximum=256)
        consent = self._consents.get(participant)
        if consent is None or not consent.active or required not in consent.scope:
            raise ConsentError("active consent does not cover recruitment scope")
        if consent.expires_at is not None and current >= consent.expires_at:
            raise ConsentError("consent has expired")
        if self._statuses.get(participant) != "recruiting":
            raise ConsentError("participant is not recruiting")
        self._statuses[participant] = "enrolled"
        return "enrolled"

    def store_evidence(self, participant_id: str, content: str, *, scope: str = "interview",
                       captured_at: Optional[float] = None, lineage_hash: Optional[str] = None,
                       retention_until: Optional[float] = None) -> ResearchEvidence:
        wall_clock = _timestamp(self._clock())
        current = wall_clock if captured_at is None else _timestamp(captured_at)
        if current > wall_clock:
            raise DataValidationError("evidence capture timestamp cannot be in the future")
        participant = _text(participant_id, "participant id", maximum=MAX_IDENTIFIER_CHARS)
        evidence_scope = _text(scope, "evidence scope", maximum=256)
        consent = self._active_consent(participant, evidence_scope, current)
        if self._statuses.get(participant) != "enrolled":
            raise ConsentError("participant must be enrolled")
        evidence_content = _text(content, "evidence content")
        evidence_hash = lineage_hash
        if not _valid_hash(evidence_hash):
            raise DataValidationError("evidence lineage hash is required")
        expiry = (_timestamp(retention_until) if retention_until is not None
                  else current + self.retention_seconds)
        if expiry <= current:
            raise RetentionError("evidence retention has expired")
        _assert_safe({"participant_id": participant, "content": evidence_content,
                      "scope": evidence_scope, "captured_at": current,
                      "lineage_hash": evidence_hash, "retention_until": expiry})
        _reserve_record(len(self._consents) + len(self._evidence), "research records")
        self._sequence += 1
        item = ResearchEvidence("evidence-%06d" % self._sequence, participant, evidence_content,
                                evidence_scope, current, evidence_hash, expiry)
        self._evidence[item.id] = item
        return item

    save_evidence = store_evidence

    def _active_consent(self, participant_id: str, scope: str, current: float) -> ParticipantConsent:
        consent = self._consents.get(participant_id)
        if consent is None or not consent.active or scope not in consent.scope:
            raise ConsentError("active consent does not cover evidence scope")
        if consent.expires_at is not None and current >= consent.expires_at:
            raise RetentionError("consent has expired")
        return consent

    def redact_evidence(self, evidence_id: str, *, replacement: str = "[REDACTED]") -> ResearchEvidence:
        item = self._evidence.get(evidence_id)
        if item is None or item.tombstone:
            raise DataValidationError("evidence is unavailable")
        replacement_text = _text(replacement, "redaction replacement")
        _assert_safe({"replacement": replacement_text})
        changed = replace(item, content=replacement_text, redacted=True)
        self._evidence[evidence_id] = changed
        return changed

    redact = redact_evidence

    def delete_participant(self, participant_id: str, *, deleted_at: Optional[float] = None) -> int:
        participant = _text(participant_id, "participant id", maximum=MAX_IDENTIFIER_CHARS)
        if participant not in self._consents:
            raise DataValidationError("participant not found")
        current = _now(deleted_at if deleted_at is not None else self._clock())
        consent = self._consents[participant]
        self._consents[participant] = replace(consent, withdrawn_at=current)
        self._statuses[participant] = "withdrawn"
        count = 0
        for key, item in tuple(self._evidence.items()):
            if item.participant_id == participant and not item.tombstone:
                self._evidence[key] = replace(item, content="", tombstone=True)
                count += 1
        return count

    delete = delete_participant

    def purge_expired(self, *, now: Optional[float] = None) -> int:
        current = _now(now if now is not None else self._clock())
        count = 0
        for key, item in tuple(self._evidence.items()):
            if item.retention_until is not None and current >= item.retention_until and not item.tombstone:
                self._evidence[key] = replace(item, content="", tombstone=True)
                count += 1
        return count

    def get_evidence(self, evidence_id: str, *, now: Optional[float] = None) -> Optional[ResearchEvidence]:
        item = self._evidence.get(evidence_id)
        current = _timestamp(now if now is not None else self._clock())
        # A caller cannot retrieve or quote an observation before its capture
        # instant, even if a damaged/imported backing store contains one.
        if item is not None and item.captured_at > current:
            return None
        if item is not None:
            consent = self._consents.get(item.participant_id)
            if (consent is None or not consent.active or item.scope not in consent.scope
                    or (consent.expires_at is not None and current >= consent.expires_at)):
                return None
        if item is not None and item.retention_until is not None and current >= item.retention_until:
            self.purge_expired(now=current)
            item = self._evidence.get(evidence_id)
        return item if item is not None and not item.tombstone else None

    def quote_evidence(self, evidence_id: str, *, now: Optional[float] = None) -> str:
        item = self.get_evidence(evidence_id, now=now)
        if item is None or item.redacted:
            raise QuoteRefused("quote refused for missing, expired, deleted, or redacted evidence")
        current = _now(now if now is not None else self._clock())
        try:
            self._active_consent(item.participant_id, "quote", current)
        except (ConsentError, RetentionError) as exc:
            # A caller requesting a quote must not learn or bypass a consent
            # failure by inspecting a lower-level storage error.
            raise QuoteRefused("quote scope or consent is not active") from exc
        return item.content

    quote = quote_evidence

    @property
    def evidence(self) -> tuple[ResearchEvidence, ...]:
        # The convenience view is a retrieval API, not an administrative
        # backing-store escape hatch. Keep consent expiry, withdrawal,
        # pre-capture, and retention checks identical to ``get_evidence`` so
        # callers cannot recover content simply by enumerating this property.
        current = _timestamp(self._clock())
        return tuple(
            item for evidence_id in sorted(self._evidence)
            if (item := self.get_evidence(evidence_id, now=current)) is not None
        )


@dataclass(frozen=True)
class Notification:
    id: str
    recipient: str
    message: str
    channel: str
    sent: bool = False


class NotificationAdapter(BaseAdapter):
    def __init__(self) -> None:
        super().__init__(AdapterContract(
            "notifications", capabilities=("notification.queue", "notification.ack")))
        self._notifications: dict[str, Notification] = {}
        self._sequence = 0

    def queue_notification(self, recipient: str, message: str, *, channel: str = "in_app") -> Notification:
        self._require_available()
        recipient_text = _text(recipient, "notification recipient", maximum=MAX_IDENTIFIER_CHARS)
        message_text = _text(message, "notification message")
        channel_text = _text(channel, "notification channel", maximum=256)
        _assert_safe({"recipient": recipient_text, "message": message_text, "channel": channel_text})
        _reserve_record(len(self._notifications), "notifications")
        self._sequence += 1
        item = Notification("notification-%06d" % self._sequence, recipient_text, message_text, channel_text)
        self._notifications[item.id] = item
        return item

    send = queue_notification

    def acknowledge(self, notification_id: str) -> Notification:
        item = self._notifications.get(notification_id)
        if item is None:
            raise DataValidationError("notification not found")
        changed = replace(item, sent=True)
        self._notifications[notification_id] = changed
        return changed


@dataclass(frozen=True)
class OutboxRecord:
    id: str
    event_type: str
    idempotency_key: str
    payload: Mapping[str, Any]
    payload_hash: str
    status: OutboxStatus = OutboxStatus.QUEUED
    attempts: int = 0
    max_attempts: int = 3
    next_attempt_at: float = 0.0
    last_error: Optional[str] = None
    acknowledged_at: Optional[float] = None
    external_id: Optional[str] = None

    @property
    def acknowledged(self) -> bool:
        return self.status is OutboxStatus.ACKNOWLEDGED

    @property
    def hash(self) -> str:
        return self.payload_hash

    @property
    def due_at(self) -> float:
        return self.next_attempt_at


class TransactionalOutbox:
    """A bounded, idempotent in-memory transactional outbox.

    A production transaction can persist the returned immutable record in the
    same transaction as its domain write.  Senders receive a canonical
    envelope carrying the immutable idempotency key and payload hash. A
    delivered-but-unacknowledged event is never dispatched automatically a
    second time; reconciliation must query the remote system by that key.
    This class intentionally stores only canonical payloads and hashes, never
    commands, headers, or secrets.
    """
    MAX_ATTEMPTS = 8

    def __init__(self, *, backoff_base: float = 1.0, backoff_cap: float = 60.0) -> None:
        if (not isinstance(backoff_base, (int, float)) or isinstance(backoff_base, bool) or
                not isinstance(backoff_cap, (int, float)) or isinstance(backoff_cap, bool) or
                not math.isfinite(backoff_base) or not math.isfinite(backoff_cap) or
                backoff_base < 0 or backoff_cap < backoff_base):
            raise DataValidationError("invalid retry bounds")
        self.backoff_base = float(backoff_base)
        self.backoff_cap = float(backoff_cap)
        self._records: dict[str, OutboxRecord] = {}
        self._keys: dict[str, str] = {}
        self._sequence = 0
        self.state = AdapterState.AVAILABLE
        self.state_reason = ""
        # Hold this through sender execution. It deliberately gives this
        # in-memory adapter at-most-one *local* attempt per record; remote
        # exactly-once still needs a durable idempotency-aware sender.
        self._lock = threading.RLock()

    @property
    def records(self) -> tuple[OutboxRecord, ...]:
        with self._lock:
            return tuple(self._records.values())

    def set_state(self, state: AdapterState | str, reason: str = "") -> None:
        try:
            normalized = AdapterState(state)
        except (TypeError, ValueError) as exc:
            raise DataValidationError("unknown adapter state") from exc
        with self._lock:
            self.state = normalized
            reason_text = _text(reason, "adapter state reason", allow_empty=True)
            _assert_safe({"reason": reason_text})
            self.state_reason = reason_text

    def enqueue(self, event_type: str, payload: Mapping[str, Any], *, idempotency_key: str,
                max_attempts: int = 3, now: float = 0.0) -> OutboxRecord:
        if not isinstance(payload, Mapping):
            raise OutboxError("event type, idempotency key, and mapping payload are required")
        try:
            event = _text(event_type, "outbox event type", maximum=256)
            key = _text(idempotency_key, "outbox idempotency key", maximum=MAX_IDENTIFIER_CHARS)
        except DataValidationError as exc:
            raise OutboxError("event type, idempotency key, and mapping payload are required") from exc
        if (not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or
                not 1 <= max_attempts <= self.MAX_ATTEMPTS):
            raise OutboxError("retry bound is outside the safe limit")
        _assert_safe(payload)
        _assert_safe({"event_type": event, "idempotency_key": key})
        frozen = _freeze(dict(payload))
        digest = payload_hash(_thaw(frozen))
        current = _now(now)
        with self._lock:
            existing_id = self._keys.get(key)
            if existing_id is not None:
                existing = self._records[existing_id]
                if existing.event_type != event or existing.payload_hash != digest:
                    raise IdempotencyConflict("idempotency key has a different event or payload")
                return existing
            _reserve_record(len(self._records), "outbox records")
            self._sequence += 1
            record_id = "outbox-%06d" % self._sequence
            record = OutboxRecord(record_id, event, key, frozen, digest,
                                  OutboxStatus.QUEUED, 0, max_attempts, current)
            self._records[record_id] = record
            self._keys[key] = record_id
            return record

    publish = enqueue

    def _replace(self, record: OutboxRecord, **changes: Any) -> OutboxRecord:
        changed = replace(record, **changes)
        self._records[record.id] = changed
        return changed

    def _delivery_failure(self, record: OutboxRecord, *, attempts: int, current: float,
                          error: str, status: OutboxStatus = OutboxStatus.RETRY_WAIT) -> OutboxRecord:
        if attempts >= record.max_attempts:
            return self._replace(record, attempts=attempts, status=OutboxStatus.DEAD_LETTER,
                                 next_attempt_at=current, last_error=error)
        delay = min(self.backoff_cap, self.backoff_base * (2 ** (attempts - 1)))
        return self._replace(record, attempts=attempts, status=status,
                             next_attempt_at=current + delay, last_error=error)

    def attempt(self, record_id: str, sender: Callable[[Mapping[str, Any]], Any], *, now: Optional[float] = None) -> OutboxRecord:
        record_key = _text(record_id, "outbox record id", maximum=MAX_IDENTIFIER_CHARS)
        current = _now(now)
        with self._lock:
            record = self._records.get(record_key)
            if record is None:
                raise OutboxError("outbox record not found")
            if record.status in (OutboxStatus.DELIVERED, OutboxStatus.ACKNOWLEDGED,
                                 OutboxStatus.DEAD_LETTER):
                return record
            if current < record.next_attempt_at:
                return record
            if self.state in (AdapterState.UNAVAILABLE, AdapterState.DEGRADED):
                label = (OutboxStatus.UNAVAILABLE if self.state is AdapterState.UNAVAILABLE
                         else OutboxStatus.DEGRADED)
                return self._delivery_failure(
                    record, attempts=record.attempts + 1, current=current,
                    error="adapter_%s" % self.state.value, status=label,
                )
            attempts = record.attempts + 1
            envelope = {
                "event_type": record.event_type,
                "idempotency_key": record.idempotency_key,
                "payload_hash": record.payload_hash,
                "payload": _thaw(record.payload),
            }
            try:
                result = sender(envelope)
                external_id = _text(result, "sender external id", maximum=MAX_IDENTIFIER_CHARS)
                _assert_safe({"external_id": external_id})
            except Exception as exc:  # adapter boundaries expose only a safe category
                return self._delivery_failure(
                    record, attempts=attempts, current=current,
                    error=("invalid_external_id" if isinstance(exc, DataValidationError)
                           else type(exc).__name__),
                )
            return self._replace(record, attempts=attempts, status=OutboxStatus.DELIVERED,
                                 external_id=external_id, last_error=None)

    deliver = attempt

    def dispatch(self, sender: Callable[[Mapping[str, Any]], Any], *, now: Optional[float] = None,
                 limit: int = 100) -> tuple[OutboxRecord, ...]:
        """Attempt at most ``limit`` due records; the bound is deliberate."""
        if limit < 1 or limit > 1000:
            raise OutboxError("dispatch limit is outside the safe bound")
        current = _now(now)
        retryable = {OutboxStatus.QUEUED, OutboxStatus.RETRY_WAIT,
                     OutboxStatus.DEGRADED, OutboxStatus.UNAVAILABLE}
        with self._lock:
            candidates = [item for item in self._records.values()
                          if item.status in retryable and item.next_attempt_at <= current]
        return tuple(self.attempt(item.id, sender, now=current)
                     for item in candidates[:limit])

    process = dispatch

    def acknowledge(self, record_id: str, *, external_id: Optional[str] = None,
                    now: Optional[float] = None) -> OutboxRecord:
        record_key = _text(record_id, "outbox record id", maximum=MAX_IDENTIFIER_CHARS)
        try:
            delivered_id = _text(external_id, "delivered external id", maximum=MAX_IDENTIFIER_CHARS)
        except DataValidationError as exc:
            raise OutboxError("acknowledgement needs the exact delivered external id") from exc
        with self._lock:
            record = self._records.get(record_key)
            if record is None:
                raise OutboxError("outbox record not found")
            if record.status is OutboxStatus.ACKNOWLEDGED:
                if record.external_id != delivered_id:
                    raise OutboxError("external acknowledgement does not reconcile")
                return record
            if record.status is not OutboxStatus.DELIVERED:
                raise OutboxError("only a delivered record can be acknowledged")
            if record.external_id != delivered_id:
                raise OutboxError("external acknowledgement does not reconcile")
            return self._replace(record, status=OutboxStatus.ACKNOWLEDGED,
                                 acknowledged_at=_now(now if now is not None else time.time()))

    def reconcile(self, acknowledgements: Mapping[str, str], *, now: Optional[float] = None) -> tuple[OutboxRecord, ...]:
        if not isinstance(acknowledgements, Mapping):
            raise OutboxError("reconciliation requires record/key to delivered-id mappings")
        if len(acknowledgements) > MAX_COLLECTION_ITEMS:
            raise OutboxError("reconciliation batch exceeds the safe bound")
        items = tuple(acknowledgements.items())
        changed = []
        with self._lock:
            for key, external in items:
                lookup = _text(key, "reconciliation record/key", maximum=MAX_IDENTIFIER_CHARS)
                record_id = lookup if lookup in self._records else self._keys.get(lookup)
                if record_id is None:
                    continue
                changed.append(self.acknowledge(record_id, external_id=external, now=now))
        return tuple(changed)

    def dead_letters(self) -> tuple[OutboxRecord, ...]:
        with self._lock:
            return tuple(item for item in self._records.values()
                         if item.status is OutboxStatus.DEAD_LETTER)


@dataclass(frozen=True)
class AdoptionObservation:
    id: str
    observed_at: float
    channel: str
    outcome: str
    consent: bool
    accessibility_issue: bool = False
    accessibility_notes: str = ""
    evidence_status: str = "observation_only"
    external_adoption_evidence: bool = False


class AdoptionObserver:
    """Records consented feedback observations, never external adoption proof."""
    def __init__(self, *, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock = clock or time.time
        self._observations: list[AdoptionObservation] = []
        self._sequence = 0

    def observe(self, *, channel: str, outcome: str, consent: bool,
                observed_at: Optional[float] = None, accessibility_issue: bool = False,
                accessibility_notes: str = "") -> AdoptionObservation:
        if consent is not True:
            raise ConsentError("feedback/adoption observation requires consent")
        if not isinstance(accessibility_issue, bool):
            raise DataValidationError("accessibility issue flag must be an exact boolean")
        channel_text = _text(channel, "observation channel", maximum=256)
        outcome_text = _text(outcome, "observation outcome")
        notes_text = _text(accessibility_notes, "accessibility notes", allow_empty=True)
        current = _now(observed_at if observed_at is not None else self._clock())
        if current > _now(self._clock()):
            raise DataValidationError("observation timestamp cannot be in the future")
        if accessibility_issue and not notes_text:
            raise DataValidationError("accessibility issue needs notes")
        _assert_safe({"channel": channel_text, "outcome": outcome_text,
                      "consent": consent, "accessibility_issue": accessibility_issue,
                      "accessibility_notes": notes_text, "observed_at": current})
        _reserve_record(len(self._observations), "adoption observations")
        self._sequence += 1
        item = AdoptionObservation("adoption-%06d" % self._sequence, current, channel_text, outcome_text,
                                   True, accessibility_issue, notes_text)
        self._observations.append(item)
        return item

    record_feedback = observe
    record_observation = observe
    observe_adoption = observe

    @property
    def observations(self) -> tuple[AdoptionObservation, ...]:
        return tuple(self._observations)


# Friendly names used by integrations and test harnesses.
IssueTrackerAdapter = IssueTrackingAdapter
Adapter = BaseAdapter
SourceControl = SourceControlAdapter
Analytics = AnalyticsAdapter
ResearchStore = ResearchStorageAdapter
Notifications = NotificationAdapter
Outbox = TransactionalOutbox
FeedbackObserver = AdoptionObserver
MetricIngestion = AnalyticsAdapter


__all__ = [name for name in globals() if not name.startswith("_")]
