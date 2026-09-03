"""Deterministic, policy-first domain primitives for Product Manager OS.

``PMOSDomain`` remains useful as a standalone in-memory aggregate.  When a
``pmos.store.Store`` is supplied, however, every public mutation is committed
as one versioned, content-addressed full snapshot and published with the
store's compare-and-swap head.  A stale writer is rolled back locally and must
explicitly refresh before retrying; it can never silently overwrite a peer.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
from dataclasses import MISSING, asdict, dataclass, field, fields, replace
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple, TypeVar

from .store import (
    IntegrityError as StoreIntegrityError,
    ProductHead,
    Store,
    StoreError,
)

SCHEMA_VERSION = "pmos.domain.v2"
SNAPSHOT_FORMAT = "pmos.domain.snapshot/v2"
SNAPSHOT_PATH = "domain/state.json"
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024
_HEX_DIGITS = frozenset("0123456789abcdef")


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in _HEX_DIGITS for character in value)
    )


class DomainError(Exception):
    """Base class for expected domain failures."""


class NotFound(DomainError):
    pass


class ValidationError(DomainError):
    pass


class AuthorizationError(DomainError):
    pass


class PermissionDenied(AuthorizationError):
    pass


class RevisionConflict(DomainError):
    pass


class PersistenceError(DomainError):
    """Durable state could not be verified, decoded, or published safely."""


class BootstrapError(AuthorizationError):
    """The one-time authority bootstrap was invalid or already completed."""


class TransitionError(DomainError):
    pass


class RelationError(DomainError):
    pass


class ApprovalError(DomainError):
    pass


class AllocationError(DomainError):
    pass


class LifecycleStage(str, Enum):
    DISCOVER = "discover"
    DEFINE = "define"
    DESIGN = "design"
    BUILD = "build"
    DELIVER = "deliver"
    OPERATE = "operate"
    RETIRED = "retired"


STAGES = tuple(LifecycleStage)
TRANSITIONS = {
    LifecycleStage.DISCOVER: (LifecycleStage.DEFINE,),
    LifecycleStage.DEFINE: (LifecycleStage.DESIGN,),
    LifecycleStage.DESIGN: (LifecycleStage.BUILD,),
    LifecycleStage.BUILD: (LifecycleStage.DELIVER,),
    LifecycleStage.DELIVER: (LifecycleStage.OPERATE,),
    LifecycleStage.OPERATE: (LifecycleStage.RETIRED,),
    LifecycleStage.RETIRED: (),
}

# These transitions commit implementation, release, live operation, or
# decommissioning. A regulated product requires a stage-bound independent
# approval before the corresponding gate can be completed.
REGULATED_APPROVAL_STAGES = frozenset(
    {
        LifecycleStage.DESIGN,
        LifecycleStage.BUILD,
        LifecycleStage.DELIVER,
        LifecycleStage.OPERATE,
    }
)


@dataclass(frozen=True)
class Entity:
    id: str
    schema_version: str = SCHEMA_VERSION
    revision: int = 0
    created_at: int = 0
    updated_at: int = 0

    @property
    def version(self) -> str:
        return self.schema_version

    @property
    def schema(self) -> str:
        return self.schema_version

    @property
    def entity_type(self) -> str:
        name = self.__class__.__name__
        return "portfolio_allocation" if name == "PortfolioAllocation" else "".join(("_" + c.lower() if c.isupper() else c) for c in name).lstrip("_")

    @property
    def kind(self) -> str:
        return self.entity_type


@dataclass(frozen=True)
class Organization(Entity):
    name: str = ""


@dataclass(frozen=True)
class Product(Entity):
    organization_id: str = ""
    name: str = ""
    regulated: bool = False


@dataclass(frozen=True)
class Initiative(Entity):
    product_id: str = ""
    name: str = ""
    description: str = ""
    stage: LifecycleStage = LifecycleStage.DISCOVER
    retired: bool = False

    @property
    def lifecycle_stage(self) -> LifecycleStage:
        return self.stage

    @property
    def current_stage(self) -> LifecycleStage:
        return self.stage


@dataclass(frozen=True)
class Opportunity(Entity):
    initiative_id: str = ""
    title: str = ""
    description: str = ""


@dataclass(frozen=True)
class Experiment(Entity):
    initiative_id: str = ""
    name: str = ""
    hypothesis: str = ""
    status: str = "planned"


@dataclass(frozen=True)
class Release(Entity):
    initiative_id: str = ""
    name: str = ""
    version_label: str = ""
    status: str = "planned"


@dataclass(frozen=True)
class Decision(Entity):
    initiative_id: str = ""
    title: str = ""
    outcome: str = ""


@dataclass(frozen=True)
class Risk(Entity):
    initiative_id: str = ""
    title: str = ""
    severity: str = "medium"
    status: str = "open"


@dataclass(frozen=True)
class Evidence(Entity):
    initiative_id: str = ""
    title: str = ""
    content_hash: str = ""
    content: str = ""

    @property
    def hash(self) -> str:
        return self.content_hash


@dataclass(frozen=True)
class Metric(Entity):
    initiative_id: str = ""
    name: str = ""
    target: Optional[float] = None
    unit: str = ""


@dataclass(frozen=True)
class Approval(Entity):
    initiative_id: str = ""
    stage: LifecycleStage = LifecycleStage.DISCOVER
    requester_id: str = ""
    approver_id: str = ""
    policy_version: str = ""
    evidence_hashes: Tuple[str, ...] = ()
    status: str = "requested"
    approved_at: Optional[int] = None
    revoked_at: Optional[int] = None
    reason: str = ""

    @property
    def evidence_hash(self) -> str:
        return self.evidence_hashes[0] if self.evidence_hashes else ""

    @property
    def is_valid(self) -> bool:
        return self.status == "approved"


@dataclass(frozen=True)
class Dependency(Entity):
    initiative_id: str = ""
    depends_on_id: str = ""
    relationship: str = "blocks"


@dataclass(frozen=True)
class PortfolioAllocation(Entity):
    product_id: str = ""
    initiative_id: str = ""
    period: str = ""
    capacity: float = 0.0
    score: float = 0.0
    sequence: int = 0


@dataclass(frozen=True)
class Membership(Entity):
    product_id: str = ""
    user_id: str = ""
    role: str = "viewer"


@dataclass(frozen=True)
class User(Entity):
    name: str = ""


@dataclass(frozen=True)
class Assignment(Entity):
    initiative_id: str = ""
    assignee_id: str = ""
    role: str = "owner"


@dataclass(frozen=True)
class Comment(Entity):
    initiative_id: str = ""
    author_id: str = ""
    body: str = ""


@dataclass(frozen=True)
class Mention(Entity):
    initiative_id: str = ""
    author_id: str = ""
    mentioned_user_id: str = ""
    comment_id: Optional[str] = None


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    timestamp: int
    action: str
    entity_type: str
    entity_id: str
    actor_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    previous_hash: str = ""
    event_hash: str = ""
    schema_version: str = SCHEMA_VERSION

    @property
    def hash(self) -> str:
        return self.event_hash


@dataclass(frozen=True)
class GateProof:
    initiative_id: str
    stage: LifecycleStage
    evidence_bindings: Tuple[Tuple[str, str], ...]
    actor_id: str
    completed_at: int
    approval_id: Optional[str] = None
    policy_version: str = ""


ENTITY_TYPES = {
    "organization": Organization,
    "product": Product,
    "initiative": Initiative,
    "opportunity": Opportunity,
    "experiment": Experiment,
    "release": Release,
    "decision": Decision,
    "risk": Risk,
    "approval": Approval,
    "dependency": Dependency,
    "portfolio_allocation": PortfolioAllocation,
    "evidence": Evidence,
    "metric": Metric,
    "user": User,
    "membership": Membership,
    "assignment": Assignment,
    "comment": Comment,
    "mention": Mention,
}

TRACE_RELATION_NAMES = frozenset(
    {"supports", "informs", "mitigates", "measures", "validates", "ships", "traces_to", "depends_on"}
)
TRACE_TARGETS = {
    "decision": frozenset({"risk", "evidence", "metric", "experiment", "release"}),
    "risk": frozenset({"evidence", "metric"}),
    "evidence": frozenset({"metric", "experiment", "release"}),
    "metric": frozenset({"experiment", "release"}),
    "experiment": frozenset({"release"}),
    "release": frozenset({"metric"}),
}
RESERVED_ACTOR_IDS = frozenset({"system", "bootstrap", "internal"})
IMMUTABLE_UPDATE_FIELDS = {
    "product": frozenset({"organization_id", "regulated"}),
    "initiative": frozenset({"product_id", "stage", "retired"}),
    "opportunity": frozenset({"initiative_id"}),
    "experiment": frozenset({"initiative_id"}),
    "release": frozenset({"initiative_id"}),
    "decision": frozenset({"initiative_id"}),
    "risk": frozenset({"initiative_id"}),
    "evidence": frozenset({"initiative_id"}),
    "metric": frozenset({"initiative_id"}),
    "dependency": frozenset({"initiative_id", "depends_on_id"}),
    "portfolio_allocation": frozenset({"product_id", "initiative_id", "period"}),
    "membership": frozenset({"product_id", "user_id"}),
    "assignment": frozenset({"initiative_id", "assignee_id"}),
    "comment": frozenset({"initiative_id", "author_id"}),
    "mention": frozenset({"initiative_id", "author_id", "mentioned_user_id", "comment_id"}),
}


def _canonical(value: Any) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValidationError("domain values must be canonical JSON") from exc


def _stage(value: LifecycleStage | str) -> LifecycleStage:
    if isinstance(value, LifecycleStage):
        return value
    try:
        return LifecycleStage(value.lower())
    except (AttributeError, ValueError):
        raise ValidationError(f"unknown lifecycle stage: {value}")


_Result = TypeVar("_Result")


def _transactional(method: Callable[..., _Result]) -> Callable[..., _Result]:
    """Make one public domain command an atomic in-memory/store mutation."""

    @wraps(method)
    def guarded(self: "PMOSDomain", *args: Any, **kwargs: Any) -> _Result:
        return self._run_mutation(method, *args, **kwargs)

    return guarded


class PMOSDomain:
    """A deterministic aggregate implementing PM OS governance invariants.

    ``actor_id`` is an authorization input from a trusted host, not an
    authentication mechanism.  The host must authenticate identities before
    calling commands and must enforce tenant/read isolation around the
    unscoped ``get``/``list`` inspection APIs.  This aggregate enforces stored
    roles, write policy, integrity, and concurrency; it does not issue or
    verify login credentials. Unscoped ``history``, ``audit_history``,
    ``export_audit``, ``relation_history``, and gate-inspection calls are also
    trusted-host operations; request paths must use actor-scoped alternatives.
    """

    schema_version = SCHEMA_VERSION

    def __init__(self, store: Optional[Store] = None, *, storage_id: str = "pmos-domain",
                 evidence_verifier: Optional[Callable[[str], bool]] = None) -> None:
        if evidence_verifier is not None and not callable(evidence_verifier):
            raise ValidationError("evidence_verifier must be callable")
        self._store = store
        self._storage_id = storage_id
        # A verifier is deliberately supplied by the trusted host. It proves
        # that a digest-only Evidence record exists in an external system; it
        # is never inferred from a caller-supplied boolean or digest.
        self._evidence_verifier = evidence_verifier
        self._store_head: Optional[ProductHead] = None
        self._mutation_depth = 0
        self._initialize_empty_state()
        if store is not None:
            try:
                self._store_head = store.create_product(storage_id)
                self._load_from_store()
            except PersistenceError:
                raise
            except (StoreError, OSError) as exc:
                raise PersistenceError("durable domain could not be opened safely") from exc

    @classmethod
    def open(cls, store: Store, *, storage_id: str = "pmos-domain",
             evidence_verifier: Optional[Callable[[str], bool]] = None) -> "PMOSDomain":
        """Open or create a durable aggregate in ``store``."""
        return cls(store, storage_id=storage_id, evidence_verifier=evidence_verifier)

    def _initialize_empty_state(self) -> None:
        self._clock = 0
        self._next_id = 1
        self._tables: Dict[str, Dict[str, Entity]] = {name: {} for name in ENTITY_TYPES}
        self._gates: Dict[tuple[str, LifecycleStage], GateProof] = {}
        self._gate_requirements: Dict[tuple[str, LifecycleStage], set[str]] = {}
        self._relations: list[tuple[str, str, str]] = []
        self._assignments: Dict[str, Assignment] = {}
        self._comments: Dict[str, Comment] = {}
        self._mentions: Dict[str, Mention] = {}
        self._capacity: Dict[tuple[str, str], float] = {}
        self._audit: list[AuditEvent] = []

    @property
    def storage_head(self) -> Optional[ProductHead]:
        """The exact durable head this instance has loaded, or ``None`` in memory mode."""
        return self._store_head

    @property
    def storage_revision(self) -> Optional[str]:
        return self._store_head.token if self._store_head is not None else None

    @property
    def state_digest(self) -> str:
        """Hash of the complete canonical aggregate state (not a mutable pointer)."""
        core = self._state_core()
        return hashlib.sha256(_canonical(core).encode("utf-8")).hexdigest()

    def _state_core(self) -> Mapping[str, Any]:
        return {
            "clock": self._clock,
            "next_id": self._next_id,
            "tables": {
                typ: [asdict(table[key]) for key in sorted(table)]
                for typ, table in sorted(self._tables.items())
            },
            "gates": [
                asdict(proof)
                for _key, proof in sorted(
                    self._gates.items(), key=lambda item: (item[0][0], item[0][1].value)
                )
            ],
            "gate_requirements": [
                {
                    "initiative_id": initiative_id,
                    "stage": stage.value,
                    "requirements": sorted(requirements),
                }
                for (initiative_id, stage), requirements in sorted(
                    self._gate_requirements.items(), key=lambda item: (item[0][0], item[0][1].value)
                )
            ],
            "relations": [list(edge) for edge in self._relations],
            "capacity": [
                {"product_id": product_id, "period": period, "capacity": capacity}
                for (product_id, period), capacity in sorted(self._capacity.items())
            ],
            "audit": [asdict(event) for event in self._audit],
        }

    def _encode_state(self) -> bytes:
        self._assert_invariants()
        core = self._state_core()
        document = {
            "format": SNAPSHOT_FORMAT,
            "schema_version": SCHEMA_VERSION,
            "state": core,
            "state_hash": hashlib.sha256(_canonical(core).encode("utf-8")).hexdigest(),
        }
        encoded = _canonical(document).encode("utf-8")
        if len(encoded) > MAX_SNAPSHOT_BYTES:
            raise PersistenceError("domain snapshot exceeds the safe size limit")
        return encoded

    @staticmethod
    def _strict_json(encoded: bytes) -> Mapping[str, Any]:
        if not isinstance(encoded, bytes) or not encoded or len(encoded) > MAX_SNAPSHOT_BYTES:
            raise PersistenceError("domain snapshot is empty or exceeds the safe size limit")

        def object_without_duplicates(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate JSON member")
                result[key] = value
            return result

        try:
            document = json.loads(
                encoded.decode("utf-8"),
                object_pairs_hook=object_without_duplicates,
                parse_constant=lambda _value: (_ for _ in ()).throw(ValueError("non-finite number")),
            )
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise PersistenceError("domain snapshot is not strict JSON") from exc
        if not isinstance(document, dict):
            raise PersistenceError("domain snapshot root must be an object")
        try:
            canonical = _canonical(document).encode("utf-8")
        except ValidationError as exc:
            raise PersistenceError("domain snapshot is not canonical JSON") from exc
        if canonical != encoded:
            raise PersistenceError("domain snapshot is not in canonical form")
        return document

    @staticmethod
    def _decode_entity(typ: str, raw: Any) -> Entity:
        if not isinstance(raw, dict):
            raise PersistenceError(f"{typ} entry must be an object")
        cls = ENTITY_TYPES[typ]
        expected = {item.name for item in fields(cls)}
        if set(raw) != expected:
            raise PersistenceError(f"{typ} entry has an unknown or missing field")
        values = dict(raw)
        if typ in {"initiative", "approval"}:
            try:
                values["stage"] = LifecycleStage(values["stage"])
            except (TypeError, ValueError) as exc:
                raise PersistenceError(f"{typ} has an unknown lifecycle stage") from exc
        if typ == "approval":
            if not isinstance(values["evidence_hashes"], list):
                raise PersistenceError("approval evidence hashes must be a list")
            values["evidence_hashes"] = tuple(values["evidence_hashes"])
        try:
            return cls(**values)
        except (TypeError, ValueError) as exc:
            raise PersistenceError(f"{typ} entry is invalid") from exc

    @classmethod
    def _decode_state(cls, encoded: bytes) -> "PMOSDomain":
        document = cls._strict_json(encoded)
        if set(document) != {"format", "schema_version", "state", "state_hash"}:
            raise PersistenceError("domain snapshot envelope is not a closed schema")
        if document["format"] != SNAPSHOT_FORMAT or document["schema_version"] != SCHEMA_VERSION:
            raise PersistenceError("unsupported domain snapshot schema")
        state = document["state"]
        if not isinstance(state, dict) or set(state) != {
            "clock", "next_id", "tables", "gates", "gate_requirements", "relations", "capacity", "audit"
        }:
            raise PersistenceError("domain state is not a closed schema")
        digest = hashlib.sha256(_canonical(state).encode("utf-8")).hexdigest()
        if not isinstance(document["state_hash"], str) or not hmac.compare_digest(document["state_hash"], digest):
            raise PersistenceError("domain state hash mismatch")
        if (not isinstance(state["clock"], int) or isinstance(state["clock"], bool)
                or not isinstance(state["next_id"], int) or isinstance(state["next_id"], bool)):
            raise PersistenceError("domain clock and ID cursor must be integers")
        tables = state["tables"]
        if not isinstance(tables, dict) or set(tables) != set(ENTITY_TYPES):
            raise PersistenceError("domain entity tables are missing or unknown")

        candidate = object.__new__(cls)
        candidate._store = None
        candidate._storage_id = "validation"
        candidate._store_head = None
        candidate._mutation_depth = 0
        candidate._clock = state["clock"]
        candidate._next_id = state["next_id"]
        candidate._tables = {name: {} for name in ENTITY_TYPES}
        for typ in sorted(ENTITY_TYPES):
            entries = tables[typ]
            if not isinstance(entries, list):
                raise PersistenceError(f"{typ} table must be a list")
            for raw in entries:
                entity = cls._decode_entity(typ, raw)
                if entity.id in candidate._tables[typ]:
                    raise PersistenceError(f"duplicate {typ} identifier")
                candidate._tables[typ][entity.id] = entity

        gates = state["gates"]
        if not isinstance(gates, list):
            raise PersistenceError("gates must be a list")
        candidate._gates = {}
        proof_fields = {item.name for item in fields(GateProof)}
        for raw in gates:
            if not isinstance(raw, dict) or set(raw) != proof_fields:
                raise PersistenceError("gate entry is invalid")
            values = dict(raw)
            try:
                values["stage"] = LifecycleStage(values["stage"])
            except (TypeError, ValueError) as exc:
                raise PersistenceError("gate stage is unknown") from exc
            bindings = values["evidence_bindings"]
            if (
                not isinstance(bindings, list)
                or any(
                    not isinstance(binding, list)
                    or len(binding) != 2
                    or any(not isinstance(part, str) for part in binding)
                    for binding in bindings
                )
            ):
                raise PersistenceError("gate evidence bindings are invalid")
            values["evidence_bindings"] = tuple((binding[0], binding[1]) for binding in bindings)
            try:
                proof = GateProof(**values)
            except (TypeError, ValueError) as exc:
                raise PersistenceError("gate proof is invalid") from exc
            key = (proof.initiative_id, proof.stage)
            if key in candidate._gates:
                raise PersistenceError("gate proof is duplicated")
            candidate._gates[key] = proof

        requirements = state["gate_requirements"]
        if not isinstance(requirements, list):
            raise PersistenceError("gate requirements must be a list")
        candidate._gate_requirements = {}
        for entry in requirements:
            if not isinstance(entry, dict) or set(entry) != {"initiative_id", "stage", "requirements"}:
                raise PersistenceError("gate requirement entry is invalid")
            values = entry["requirements"]
            if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
                raise PersistenceError("gate requirements must contain strings")
            try:
                key = (entry["initiative_id"], LifecycleStage(entry["stage"]))
            except (TypeError, ValueError) as exc:
                raise PersistenceError("gate requirement stage is unknown") from exc
            if not isinstance(key[0], str) or key in candidate._gate_requirements or values != sorted(set(values)):
                raise PersistenceError("gate requirement key or values are invalid")
            candidate._gate_requirements[key] = set(values)

        relations = state["relations"]
        if not isinstance(relations, list):
            raise PersistenceError("relations must be a list")
        candidate._relations = []
        for edge in relations:
            if not isinstance(edge, list) or len(edge) != 3 or any(not isinstance(v, str) for v in edge):
                raise PersistenceError("relation entry is invalid")
            candidate._relations.append((edge[0], edge[1], edge[2]))

        capacity = state["capacity"]
        if not isinstance(capacity, list):
            raise PersistenceError("capacity must be a list")
        candidate._capacity = {}
        for entry in capacity:
            if not isinstance(entry, dict) or set(entry) != {"product_id", "period", "capacity"}:
                raise PersistenceError("capacity entry is invalid")
            key = (entry["product_id"], entry["period"])
            if any(not isinstance(v, str) for v in key) or key in candidate._capacity:
                raise PersistenceError("capacity key is invalid or duplicated")
            candidate._capacity[key] = entry["capacity"]

        audit = state["audit"]
        if not isinstance(audit, list):
            raise PersistenceError("audit must be a list")
        candidate._audit = []
        audit_fields = {item.name for item in fields(AuditEvent)}
        for raw in audit:
            if not isinstance(raw, dict) or set(raw) != audit_fields or not isinstance(raw.get("payload"), dict):
                raise PersistenceError("audit event is invalid")
            try:
                candidate._audit.append(AuditEvent(**dict(raw)))
            except (TypeError, ValueError) as exc:
                raise PersistenceError("audit event is invalid") from exc

        candidate._assignments = dict(candidate._tables["assignment"])
        candidate._comments = dict(candidate._tables["comment"])
        candidate._mentions = dict(candidate._tables["mention"])
        candidate._assert_invariants()
        return candidate

    def _adopt_state(self, candidate: "PMOSDomain") -> None:
        self._clock = candidate._clock
        self._next_id = candidate._next_id
        self._tables = candidate._tables
        self._gates = candidate._gates
        self._gate_requirements = candidate._gate_requirements
        self._relations = candidate._relations
        self._assignments = candidate._assignments
        self._comments = candidate._comments
        self._mentions = candidate._mentions
        self._capacity = candidate._capacity
        self._audit = candidate._audit

    def _load_from_store(self) -> None:
        if self._store is None:
            return
        try:
            report = self._store.verify()
            if not report.ok:
                raise PersistenceError("durable store integrity verification failed")
            snapshot = self._store.read_snapshot(self._storage_id)
            if snapshot.head.commit_hash is None:
                if snapshot.files:
                    raise PersistenceError("uncommitted durable domain contains files")
                candidate = object.__new__(PMOSDomain)
                candidate._store = None
                candidate._storage_id = "validation"
                candidate._store_head = None
                candidate._mutation_depth = 0
                candidate._initialize_empty_state()
            else:
                if set(snapshot.files) != {SNAPSHOT_PATH}:
                    raise PersistenceError("durable domain snapshot has an unexpected file set")
                candidate = self._decode_state(snapshot.files[SNAPSHOT_PATH])
            self._adopt_state(candidate)
            self._store_head = snapshot.head
        except PersistenceError:
            raise
        except (StoreIntegrityError, StoreError, OSError) as exc:
            raise PersistenceError("durable domain snapshot failed integrity verification") from exc

    def refresh(self) -> "PMOSDomain":
        """Replace local state with the latest verified head before an explicit retry."""
        if self._store is None:
            return self
        checkpoint = self._encode_state()
        prior_head = self._store_head
        try:
            self._load_from_store()
        except Exception:
            self._adopt_state(self._decode_state(checkpoint))
            self._store_head = prior_head
            raise
        return self

    def _persist_state(self) -> None:
        if self._store is None:
            return
        if self._store_head is None:
            raise PersistenceError("durable domain has no loaded head")
        encoded = self._encode_state()
        digest = self.state_digest
        try:
            result = self._store.commit(
                self._storage_id,
                {SNAPSHOT_PATH: encoded},
                expected_revision=self._store_head,
                metadata={"format": SNAPSHOT_FORMAT, "schema_version": SCHEMA_VERSION, "state_hash": digest},
            )
        except StoreError as exc:
            raise PersistenceError("durable domain commit failed safely") from exc
        if not result.committed or result.head is None:
            conflict = result.conflict
            current = conflict.current.token if conflict is not None else "unknown"
            raise RevisionConflict(
                f"durable domain expected {self._store_head.token}, current {current}; refresh before retry"
            )
        self._store_head = result.head

    def _run_mutation(self, method: Callable[..., _Result], *args: Any, **kwargs: Any) -> _Result:
        outermost = self._mutation_depth == 0
        checkpoint = self._encode_state() if outermost else b""
        prior_head = self._store_head
        self._mutation_depth += 1
        try:
            result = method(self, *args, **kwargs)
            if outermost:
                self._assert_invariants()
                self._persist_state()
            return result
        except Exception:
            if outermost:
                self._adopt_state(self._decode_state(checkpoint))
                self._store_head = prior_head
            raise
        finally:
            self._mutation_depth -= 1

    def _assert_invariants(self) -> None:
        if not isinstance(self._clock, int) or isinstance(self._clock, bool) or self._clock < 0:
            raise PersistenceError("domain clock is invalid")
        if not isinstance(self._next_id, int) or isinstance(self._next_id, bool) or self._next_id < 1:
            raise PersistenceError("domain ID cursor is invalid")
        if set(self._tables) != set(ENTITY_TYPES):
            raise PersistenceError("domain entity table set is invalid")

        auto_id_max = 0
        entity_by_id: dict[str, tuple[str, Entity]] = {}
        max_timestamp = 0
        for typ, table in self._tables.items():
            if not isinstance(table, dict):
                raise PersistenceError("domain entity table is invalid")
            for key, entity in table.items():
                if not isinstance(entity, ENTITY_TYPES[typ]) or key != entity.id:
                    raise PersistenceError(f"{typ} table contains an invalid entity")
                self._validate_entity(entity)
                if entity.id in entity_by_id:
                    raise PersistenceError("domain entity identifiers must be globally unique")
                entity_by_id[entity.id] = (typ, entity)
                max_timestamp = max(max_timestamp, entity.created_at, entity.updated_at)
                prefix, separator, suffix = entity.id.rpartition("-")
                if separator and len(prefix) == 3 and suffix.isdigit():
                    auto_id_max = max(auto_id_max, int(suffix))
        if self._next_id <= auto_id_max:
            raise PersistenceError("domain ID cursor would reuse an existing identifier")

        organizations = self._tables["organization"]
        products = self._tables["product"]
        initiatives = self._tables["initiative"]
        users = self._tables["user"]
        for product in products.values():
            if product.organization_id not in organizations:
                raise PersistenceError("product refers to a missing organization")
        for initiative in initiatives.values():
            if initiative.product_id not in products:
                raise PersistenceError("initiative refers to a missing product")
            if initiative.retired != (initiative.stage == LifecycleStage.RETIRED):
                raise PersistenceError("initiative retirement state conflicts with lifecycle stage")
        initiative_children = {
            "opportunity", "experiment", "release", "decision", "risk", "evidence", "metric", "approval",
            "dependency", "portfolio_allocation", "assignment", "comment", "mention",
        }
        for typ in initiative_children:
            for entity in self._tables[typ].values():
                if entity.initiative_id not in initiatives:
                    raise PersistenceError(f"{typ} refers to a missing initiative")
        for membership in self._tables["membership"].values():
            if membership.product_id not in products or membership.user_id not in users:
                raise PersistenceError("membership has a dangling reference")
            if membership.role not in {"admin", "owner", "pm", "contributor", "viewer", "approver", "auditor"}:
                raise PersistenceError("membership role is unknown")
        membership_keys = [
            (membership.product_id, membership.user_id)
            for membership in self._tables["membership"].values()
        ]
        if len(membership_keys) != len(set(membership_keys)):
            raise PersistenceError("product membership is duplicated")
        member_pairs = set(membership_keys)
        for product_id in products:
            if not any(
                membership.product_id == product_id and membership.role in {"admin", "owner"}
                for membership in self._tables["membership"].values()
            ):
                raise PersistenceError("every product must retain an owner or administrator")
        for assignment in self._tables["assignment"].values():
            initiative = initiatives[assignment.initiative_id]
            if assignment.assignee_id not in users or (initiative.product_id, assignment.assignee_id) not in member_pairs:
                raise PersistenceError("assignment has a dangling assignee")
        for comment in self._tables["comment"].values():
            initiative = initiatives[comment.initiative_id]
            if comment.author_id not in users or (initiative.product_id, comment.author_id) not in member_pairs:
                raise PersistenceError("comment has a dangling author")
        for mention in self._tables["mention"].values():
            initiative = initiatives[mention.initiative_id]
            if (
                mention.author_id not in users
                or mention.mentioned_user_id not in users
                or (initiative.product_id, mention.author_id) not in member_pairs
                or (initiative.product_id, mention.mentioned_user_id) not in member_pairs
            ):
                raise PersistenceError("mention has a dangling user")
            if mention.comment_id is not None:
                comment = self._tables["comment"].get(mention.comment_id)
                if comment is None or comment.initiative_id != mention.initiative_id:
                    raise PersistenceError("mention has a dangling or cross-initiative comment")
        for dependency in self._tables["dependency"].values():
            if dependency.depends_on_id not in initiatives:
                raise PersistenceError("dependency has a dangling target")
            if initiatives[dependency.initiative_id].product_id != initiatives[dependency.depends_on_id].product_id:
                raise PersistenceError("dependency crosses product authority boundaries")
        for allocation in self._tables["portfolio_allocation"].values():
            initiative = initiatives[allocation.initiative_id]
            if allocation.product_id != initiative.product_id:
                raise PersistenceError("allocation product does not match its initiative")
            if allocation.capacity < 0 or allocation.sequence < 0:
                raise PersistenceError("allocation capacity or sequence is invalid")
        allocation_keys = [
            (allocation.initiative_id, allocation.period)
            for allocation in self._tables["portfolio_allocation"].values()
        ]
        if len(allocation_keys) != len(set(allocation_keys)):
            raise PersistenceError("portfolio allocation is duplicated for a period")
        for approval in self._tables["approval"].values():
            product_id = initiatives[approval.initiative_id].product_id
            if approval.requester_id not in users or (product_id, approval.requester_id) not in member_pairs:
                raise PersistenceError("approval has a dangling requester")
            if approval.approver_id and (
                approval.approver_id not in users
                or (product_id, approval.approver_id) not in member_pairs
            ):
                raise PersistenceError("approval has a dangling approver")
            if approval.approver_id and approval.approver_id == approval.requester_id:
                raise PersistenceError("approval violates separation of duties")
            if approval.status not in {"requested", "approved", "revoked", "invalidated"}:
                raise PersistenceError("approval status is unknown")
            if approval.status == "approved" and (not approval.approver_id or approval.approved_at is None):
                raise PersistenceError("approved approval lacks authority or timestamp")
            if approval.status in {"requested", "approved"}:
                available = {
                    evidence.content_hash for evidence in self._tables["evidence"].values()
                    if evidence.initiative_id == approval.initiative_id
                }
                if any(digest not in available for digest in approval.evidence_hashes):
                    raise PersistenceError("active approval refers to changed or missing evidence")
            if products[product_id].regulated and (not approval.policy_version or not approval.evidence_hashes):
                raise PersistenceError("regulated approval lacks policy or evidence")
        for evidence in self._tables["evidence"].values():
            if not _is_sha256(evidence.content_hash):
                raise PersistenceError("evidence content hash is invalid")
            if evidence.content and hashlib.sha256(evidence.content.encode("utf-8")).hexdigest() != evidence.content_hash:
                raise PersistenceError("evidence content hash mismatch")

        for (initiative_id, stage), proof in self._gates.items():
            if (
                initiative_id not in initiatives
                or not isinstance(stage, LifecycleStage)
                or not isinstance(proof, GateProof)
                or proof.initiative_id != initiative_id
                or proof.stage != stage
                or not isinstance(proof.actor_id, str)
                or proof.actor_id not in users
                or not isinstance(proof.completed_at, int)
                or isinstance(proof.completed_at, bool)
                or proof.completed_at < 0
            ):
                raise PersistenceError("gate proof identity or authority is invalid")
            max_timestamp = max(max_timestamp, proof.completed_at)
            if not proof.evidence_bindings or tuple(sorted(proof.evidence_bindings)) != proof.evidence_bindings:
                raise PersistenceError("gate proof requires sorted evidence bindings")
            evidence_ids = [binding[0] for binding in proof.evidence_bindings]
            if len(evidence_ids) != len(set(evidence_ids)):
                raise PersistenceError("gate proof repeats evidence")
            for evidence_id, digest in proof.evidence_bindings:
                evidence = self._tables["evidence"].get(evidence_id)
                if (
                    evidence is None
                    or evidence.initiative_id != initiative_id
                    or evidence.content_hash != digest
                    or len(digest) != 64
                ):
                    raise PersistenceError("gate proof evidence is missing, changed, or cross-initiative")
            product = products[initiatives[initiative_id].product_id]
            if (product.id, proof.actor_id) not in member_pairs:
                raise PersistenceError("gate proof actor lacks product membership")
            approval = self._tables["approval"].get(proof.approval_id) if proof.approval_id else None
            if approval is not None:
                if (
                    approval.initiative_id != initiative_id
                    or approval.stage != stage
                    or approval.status != "approved"
                    or approval.requester_id == approval.approver_id
                    or approval.policy_version != proof.policy_version
                    or sorted(approval.evidence_hashes) != sorted(binding[1] for binding in proof.evidence_bindings)
                ):
                    raise PersistenceError("gate proof approval is stale or does not match its evidence and policy")
            elif proof.approval_id is not None or proof.policy_version:
                raise PersistenceError("gate proof approval reference is invalid")
            if product.regulated and stage in REGULATED_APPROVAL_STAGES and approval is None:
                raise PersistenceError("regulated checkpoint lacks an approved gate proof")
        for (initiative_id, stage), values in self._gate_requirements.items():
            if initiative_id not in initiatives or not isinstance(stage, LifecycleStage):
                raise PersistenceError("gate requirement refers to missing state")
            if not isinstance(values, set) or any(not isinstance(item, str) or not item for item in values):
                raise PersistenceError("gate requirement values are invalid")
            for evidence_id in values:
                evidence = self._tables["evidence"].get(evidence_id)
                if evidence is None or evidence.initiative_id != initiative_id:
                    raise PersistenceError("gate requirement is not an evidence reference for its initiative")

        if len(self._relations) != len(set(self._relations)):
            raise PersistenceError("duplicate trace relation")
        for source_id, target_id, relation in self._relations:
            source_info = entity_by_id.get(source_id)
            target_info = entity_by_id.get(target_id)
            if source_info is None or target_info is None:
                raise PersistenceError("trace relation has a dangling endpoint")
            if relation not in TRACE_RELATION_NAMES or target_info[0] not in TRACE_TARGETS.get(source_info[0], ()):
                raise PersistenceError("trace relation violates the typed graph")
            if getattr(source_info[1], "initiative_id", None) != getattr(target_info[1], "initiative_id", None):
                raise PersistenceError("trace relation crosses initiatives")

        for (product_id, period), value in self._capacity.items():
            if product_id not in products or not isinstance(period, str) or not self._finite_number(value) or value < 0:
                raise PersistenceError("capacity limit is invalid")
            used = sum(
                allocation.capacity for allocation in self._tables["portfolio_allocation"].values()
                if allocation.product_id == product_id and allocation.period == period
            )
            if used > value:
                raise PersistenceError("capacity allocations exceed the configured limit")

        graph: dict[str, set[str]] = {}
        for dependency in self._tables["dependency"].values():
            graph.setdefault(dependency.initiative_id, set()).add(dependency.depends_on_id)

        def cycle(node: str, visiting: set[str], visited: set[str]) -> bool:
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            for child in graph.get(node, set()):
                if cycle(child, visiting, visited):
                    return True
            visiting.remove(node)
            visited.add(node)
            return False

        visited: set[str] = set()
        if any(cycle(node, set(), visited) for node in graph):
            raise PersistenceError("dependency graph contains a cycle")

        if self._assignments != self._tables["assignment"] or self._comments != self._tables["comment"] or self._mentions != self._tables["mention"]:
            raise PersistenceError("collaboration projection does not match entity state")
        exported = {"schema_version": SCHEMA_VERSION, "events": [asdict(event) for event in self._audit]}
        if not self.verify_audit_export(exported):
            raise PersistenceError("audit chain failed verification")
        if self._audit:
            for event in self._audit:
                if (
                    not isinstance(event.sequence, int)
                    or isinstance(event.sequence, bool)
                    or not isinstance(event.timestamp, int)
                    or isinstance(event.timestamp, bool)
                    or event.timestamp < 0
                    or not isinstance(event.action, str)
                    or not event.action
                    or not isinstance(event.entity_type, str)
                    or not isinstance(event.entity_id, str)
                    or not isinstance(event.actor_id, str)
                    or not event.actor_id
                    or event.schema_version != SCHEMA_VERSION
                ):
                    raise PersistenceError("audit event fields are invalid")
                if event.actor_id != "bootstrap" and event.actor_id not in users:
                    raise PersistenceError("audit event actor is not a known authority")
            max_timestamp = max(max_timestamp, max(event.timestamp for event in self._audit))
        if self._clock < max_timestamp:
            raise PersistenceError("domain clock precedes stored state")

    @staticmethod
    def _finite_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))

    @classmethod
    def _validate_entity(cls, entity: Entity) -> None:
        for item in fields(entity):
            value = getattr(entity, item.name)
            if item.name == "id":
                if not isinstance(value, str) or not value or "\x00" in value or len(value) > 512:
                    raise PersistenceError("entity identifier is invalid")
            elif item.name == "schema_version":
                if value != SCHEMA_VERSION:
                    raise PersistenceError("entity schema version is unknown")
            elif item.name in {"revision", "created_at", "updated_at"}:
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    raise PersistenceError(f"entity {item.name} is invalid")
            elif item.name == "stage":
                if not isinstance(value, LifecycleStage):
                    raise PersistenceError("initiative lifecycle stage is invalid")
            elif item.name == "evidence_hashes":
                if not isinstance(value, tuple) or any(not _is_sha256(part) for part in value):
                    raise PersistenceError("approval evidence hashes are invalid")
            elif item.name in {"approved_at", "revoked_at"}:
                if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                    raise PersistenceError("approval timestamp is invalid")
            elif item.name == "comment_id":
                if value is not None and not isinstance(value, str):
                    raise PersistenceError("mention comment identifier is invalid")
            elif item.name == "target":
                if value is not None and not cls._finite_number(value):
                    raise PersistenceError("metric target is invalid")
            elif item.default is not MISSING and isinstance(item.default, str):
                if not isinstance(value, str) or "\x00" in value:
                    raise PersistenceError(f"entity field {item.name} must be a string")
            elif item.default is not MISSING and isinstance(item.default, bool):
                if not isinstance(value, bool):
                    raise PersistenceError(f"entity field {item.name} must be a boolean")
            elif item.default is not MISSING and isinstance(item.default, int):
                if not isinstance(value, int) or isinstance(value, bool):
                    raise PersistenceError(f"entity field {item.name} must be an integer")
            elif item.default is not MISSING and isinstance(item.default, float):
                if not cls._finite_number(value):
                    raise PersistenceError(f"entity field {item.name} must be finite")

    @property
    def history(self) -> Tuple[AuditEvent, ...]:
        """Trusted-host full audit stream; request paths should use ``history_for_actor``."""
        # Return copies so callers cannot mutate the append-only log through a
        # frozen event's (necessarily plain-dict) payload.
        return tuple(replace(event, payload=dict(event.payload)) for event in self._audit)

    @property
    def audit_history(self) -> Tuple[AuditEvent, ...]:
        return self.history

    def history_for_actor(self, product_id: str, *, actor_id: str) -> Tuple[AuditEvent, ...]:
        """Return one product's audit stream only to its audit-authorized users."""
        self._require_product_action(product_id, actor_id, "audit")
        entity_ids = {product_id}
        entity_ids.update(
            entity.id for entity in self._tables["initiative"].values()
            if entity.product_id == product_id
        )
        initiative_ids = set(entity_ids)
        for typ, table in self._tables.items():
            if typ in {"organization", "product", "initiative", "user"}:
                continue
            for entity in table.values():
                if getattr(entity, "product_id", None) == product_id or getattr(entity, "initiative_id", None) in initiative_ids:
                    entity_ids.add(entity.id)
        return tuple(
            replace(event, payload=dict(event.payload))
            for event in self._audit
            if event.entity_id in entity_ids
        )

    @_transactional
    def bootstrap_workspace(
        self,
        organization_name: str,
        product_name: str,
        owner_name: str,
        *,
        regulated: bool = False,
    ) -> tuple[Organization, Product, User, Membership]:
        """Create the first authority boundary exactly once.

        Bootstrap is intentionally a single atomic command instead of a magic
        public ``system`` actor.  After it succeeds every mutation must name a
        real user whose stored membership authorizes the operation.
        """
        if self._audit or any(self._tables[name] for name in ENTITY_TYPES):
            raise BootstrapError("workspace bootstrap is allowed only for a completely empty domain")
        organization = self._create("organization", "bootstrap", name=organization_name)
        product = self._create(
            "product",
            "bootstrap",
            organization_id=organization.id,
            name=product_name,
            regulated=regulated,
        )
        owner = self._create("user", "bootstrap", name=owner_name)
        membership = self._create(
            "membership",
            "bootstrap",
            product_id=product.id,
            user_id=owner.id,
            role="owner",
        )
        return organization, product, owner, membership

    bootstrap = bootstrap_workspace

    def _public_actor(self, actor_id: Optional[str]) -> str:
        if (
            not isinstance(actor_id, str)
            or not actor_id
            or actor_id != actor_id.strip()
            or actor_id.lower() in RESERVED_ACTOR_IDS
        ):
            raise PermissionDenied("a non-reserved authenticated user actor is required")
        self._require("user", actor_id)
        return actor_id

    def _require_os_admin(self, actor_id: Optional[str]) -> str:
        actor = self._public_actor(actor_id)
        if not any(
            membership.user_id == actor and membership.role in {"admin", "owner"}
            for membership in self._tables["membership"].values()
        ):
            raise PermissionDenied(f"{actor} is not an OS owner or administrator")
        return actor

    def _require_product_action(self, product_id: str, actor_id: Optional[str], action: str) -> str:
        self._require("product", product_id)
        actor = self._public_actor(actor_id)
        if not self.authorize(product_id, actor, action):
            raise PermissionDenied(f"{actor} cannot {action} product {product_id}")
        return actor

    def _entity_product_id(self, typ: str, entity: Entity) -> Optional[str]:
        if typ == "product":
            return entity.id
        if typ == "membership":
            return entity.product_id  # type: ignore[attr-defined]
        if typ == "initiative":
            return entity.product_id  # type: ignore[attr-defined]
        initiative_id = getattr(entity, "initiative_id", None)
        if initiative_id:
            return self._require("initiative", initiative_id).product_id  # type: ignore[attr-defined]
        return None

    def _authorize_entity_mutation(self, typ: str, entity: Entity, actor_id: Optional[str]) -> str:
        product_id = self._entity_product_id(typ, entity)
        if product_id is None:
            return self._require_os_admin(actor_id)
        action = "admin" if typ in {"membership", "product"} else "edit"
        return self._require_product_action(product_id, actor_id, action)

    def _authorize_entity_read(self, typ: str, entity: Entity, actor_id: Optional[str]) -> str:
        actor = self._public_actor(actor_id)
        if typ == "user" and entity.id == actor:
            return actor
        product_id = self._entity_product_id(typ, entity)
        if product_id is None:
            return self._require_os_admin(actor)
        if not self.authorize(product_id, actor, "view"):
            raise PermissionDenied(f"{actor} cannot view {typ} {entity.id}")
        return actor

    @staticmethod
    def _creation_extras(kwargs: Mapping[str, Any]) -> dict[str, Any]:
        unknown = set(kwargs) - {"id", "timestamp"}
        if unknown:
            raise ValidationError(f"caller cannot set creation state fields: {sorted(unknown)}")
        return dict(kwargs)

    def _id(self, kind: str) -> str:
        result = f"{kind[:3]}-{self._next_id:06d}"
        self._next_id += 1
        return result

    def _tick(self, timestamp: Optional[int] = None) -> int:
        if timestamp is None:
            self._clock += 1
        else:
            if timestamp < self._clock:
                raise ValidationError("timestamps must be monotonic")
            self._clock = timestamp
        return self._clock

    def _record(self, action: str, typ: str, entity_id: str, actor_id: str, payload: Any = None, timestamp: Optional[int] = None) -> AuditEvent:
        if not isinstance(actor_id, str) or not actor_id:
            raise ValidationError("audit actor must be a non-empty string")
        now = self._tick(timestamp)
        previous = self._audit[-1].event_hash if self._audit else "0" * 64
        body = {"sequence": len(self._audit) + 1, "timestamp": now, "action": action, "entity_type": typ, "entity_id": entity_id, "actor_id": actor_id, "payload": payload or {}, "previous_hash": previous, "schema_version": SCHEMA_VERSION}
        digest = hashlib.sha256(_canonical(body).encode()).hexdigest()
        event = AuditEvent(event_hash=digest, **body)
        self._audit.append(event)
        return event

    def _table(self, typ: str) -> Dict[str, Entity]:
        try:
            return self._tables[typ]
        except KeyError:
            raise ValidationError(f"unknown entity type: {typ}")

    def get(
        self,
        entity_id: str,
        entity_type: Optional[str] = None,
        *,
        actor_id: Optional[str] = None,
    ) -> Entity:
        """Read one entity.

        Omitting ``actor_id`` is a trusted-host/internal inspection operation.
        Untrusted request paths must supply their authenticated actor so stored
        product membership is enforced.
        """
        tables = [self._table(entity_type)] if entity_type else self._tables.values()
        for typ, table in (
            ((entity_type, tables[0]),) if entity_type else self._tables.items()
        ):
            if entity_id in table:
                entity = table[entity_id]
                if actor_id is not None:
                    self._authorize_entity_read(str(typ), entity, actor_id)
                return entity
        raise NotFound(entity_id)

    get_entity = get

    def list_entities(
        self, entity_type: str, *, actor_id: Optional[str] = None
    ) -> Tuple[Entity, ...]:
        """List a table; actor-scoped calls return only visible product data."""
        values = tuple(self._table(entity_type).values())
        if actor_id is None:
            return values
        actor = self._public_actor(actor_id)
        if entity_type in {"organization", "user"}:
            self._require_os_admin(actor)
            return values
        visible: list[Entity] = []
        for entity in values:
            try:
                self._authorize_entity_read(entity_type, entity, actor)
            except PermissionDenied:
                continue
            visible.append(entity)
        return tuple(visible)

    def _require(self, typ: str, entity_id: str) -> Entity:
        try:
            return self._table(typ)[entity_id]
        except KeyError:
            raise NotFound(f"{typ}:{entity_id}")

    def _create(self, typ: str, actor_id: str, timestamp: Optional[int] = None, **kwargs: Any) -> Entity:
        cls = ENTITY_TYPES[typ]
        controlled = {"schema_version", "revision", "created_at", "updated_at"}.intersection(kwargs)
        if controlled:
            raise ValidationError(f"caller cannot set controlled fields: {sorted(controlled)}")
        entity_id = kwargs.pop("id", None) or self._id(typ)
        if typ == "user" and isinstance(entity_id, str) and entity_id.lower() in RESERVED_ACTOR_IDS:
            raise ValidationError("user identifier is reserved")
        if any(entity_id in table for table in self._tables.values()):
            raise ValidationError(f"duplicate domain entity id: {entity_id}")
        if isinstance(entity_id, str):
            prefix, separator, suffix = entity_id.rpartition("-")
            if separator and len(prefix) == 3 and suffix.isdigit():
                self._next_id = max(self._next_id, int(suffix) + 1)
        now = self._tick(timestamp)
        obj = cls(id=entity_id, created_at=now, updated_at=now, **kwargs)
        self._table(typ)[entity_id] = obj
        entity_document = asdict(obj)
        # Audit records prove exactly which entity revision changed without
        # duplicating customer, research, comment, or strategy content.
        audit_payload = {
            "entity_revision": obj.revision,
            "entity_hash": hashlib.sha256(_canonical(entity_document).encode("utf-8")).hexdigest(),
        }
        if typ == "evidence":
            audit_payload["content_hash"] = obj.content_hash  # type: ignore[attr-defined]
            audit_payload["content_redacted"] = True
        self._record("create", typ, entity_id, actor_id, audit_payload, timestamp=now)
        return obj

    @_transactional
    def create_organization(self, name: str, *, actor_id: Optional[str] = None, **kwargs: Any) -> Organization:
        actor = self._require_os_admin(actor_id)
        return self._create("organization", actor, name=name, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_product(self, organization_id: str, name: str, *, regulated: bool = False, actor_id: Optional[str] = None, **kwargs: Any) -> Product:
        self._require("organization", organization_id)
        actor = self._require_os_admin(actor_id)
        product = self._create("product", actor, organization_id=organization_id, name=name, regulated=regulated, **self._creation_extras(kwargs))
        self._create("membership", actor, product_id=product.id, user_id=actor, role="owner")
        return product  # type: ignore[return-value]

    @_transactional
    def create_initiative(self, product_id: str, name: str, *, description: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Initiative:
        actor = self._require_product_action(product_id, actor_id, "edit")
        result = self._create("initiative", actor, product_id=product_id, name=name, description=description, **self._creation_extras(kwargs))
        return result  # type: ignore[return-value]

    @_transactional
    def create_opportunity(self, initiative_id: str, title: str, *, description: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Opportunity:
        self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        return self._create("opportunity", actor, initiative_id=initiative_id, title=title, description=description, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_experiment(self, initiative_id: str, name: str, *, hypothesis: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Experiment:
        self._allowed(initiative_id, actor_id, "experiment")
        actor = self._public_actor(actor_id)
        return self._create("experiment", actor, initiative_id=initiative_id, name=name, hypothesis=hypothesis, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_release(self, initiative_id: str, name: str, *, version_label: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Release:
        self._allowed(initiative_id, actor_id, "release")
        actor = self._public_actor(actor_id)
        return self._create("release", actor, initiative_id=initiative_id, name=name, version_label=version_label, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_decision(self, initiative_id: str, title: str, *, outcome: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Decision:
        self._allowed(initiative_id, actor_id, "decision")
        actor = self._public_actor(actor_id)
        return self._create("decision", actor, initiative_id=initiative_id, title=title, outcome=outcome, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_risk(self, initiative_id: str, title: str, *, severity: str = "medium", actor_id: Optional[str] = None, **kwargs: Any) -> Risk:
        self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        return self._create("risk", actor, initiative_id=initiative_id, title=title, severity=severity, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def create_evidence(self, initiative_id: str, title: str, content: str = "", *, content_hash: Optional[str] = None, actor_id: Optional[str] = None, **kwargs: Any) -> Evidence:
        """Create content-backed evidence or a host-verified digest-only record.

        Digest-only records are accepted only when ``evidence_verifier`` was
        supplied by the trusted host and returns the literal ``True`` for the
        digest. The same verifier is called again when a gate binds the record.
        """
        self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        if not isinstance(content, str):
            raise ValidationError("evidence content must be text")
        digest = content_hash or hashlib.sha256(content.encode()).hexdigest()
        if not _is_sha256(digest):
            raise ValidationError("content hash must be a lowercase SHA-256 digest")
        if content_hash and content and digest != hashlib.sha256(content.encode()).hexdigest():
            raise ValidationError("content hash does not match content")
        if not content and not self._verify_external_evidence(digest):
            raise ValidationError(
                "blank evidence requires a trusted external verifier for its content hash"
            )
        return self._create("evidence", actor, initiative_id=initiative_id, title=title, content=content, content_hash=digest, **self._creation_extras(kwargs))  # type: ignore[return-value]

    def _verify_external_evidence(self, digest: str) -> bool:
        """Fail closed unless the trusted host verifies a digest externally."""
        verifier = self._evidence_verifier
        if verifier is None:
            return False
        try:
            return verifier(digest) is True
        except Exception:
            return False

    @_transactional
    def create_metric(self, initiative_id: str, name: str, *, target: Optional[float] = None, unit: str = "", actor_id: Optional[str] = None, **kwargs: Any) -> Metric:
        self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        return self._create("metric", actor, initiative_id=initiative_id, name=name, target=target, unit=unit, **self._creation_extras(kwargs))  # type: ignore[return-value]

    # Short aliases are useful to storage adapters and keep callers terse.
    organization = create_organization
    product = create_product
    initiative = create_initiative
    opportunity = create_opportunity
    experiment = create_experiment
    release = create_release
    decision = create_decision
    risk = create_risk
    evidence = create_evidence
    metric = create_metric

    @_transactional
    def update(self, entity_type: str, entity_id: str, *, expected_revision: int, actor_id: Optional[str] = None, timestamp: Optional[int] = None, **changes: Any) -> Entity:
        old = self._require(entity_type, entity_id)
        actor = self._authorize_entity_mutation(entity_type, old, actor_id)
        if old.revision != expected_revision:
            raise RevisionConflict(f"{entity_type}:{entity_id} expected revision {expected_revision}, current {old.revision}")
        if entity_type == "approval":
            raise ApprovalError("approval state can change only through approval commands")
        immutable = IMMUTABLE_UPDATE_FIELDS.get(entity_type, frozenset()).intersection(changes)
        if entity_type == "initiative" and {"stage", "retired"}.intersection(immutable):
            raise TransitionError("initiative lifecycle can change only through transition commands")
        if immutable:
            raise ValidationError(f"entity scope fields are immutable: {sorted(immutable)}")
        if entity_type == "membership" and "role" in changes:
            role = changes["role"]
            if role not in {"admin", "owner", "pm", "contributor", "viewer", "approver", "auditor"}:
                raise ValidationError(f"unknown role: {role}")
            if old.role in {"admin", "owner"} and role not in {"admin", "owner"}:  # type: ignore[attr-defined]
                authorities = [
                    membership for membership in self._tables["membership"].values()
                    if membership.product_id == old.product_id  # type: ignore[attr-defined]
                    and membership.role in {"admin", "owner"}
                ]
                if len(authorities) == 1 and authorities[0].id == old.id:
                    raise PermissionDenied("cannot demote the product's final owner or administrator")
        allowed = {f.name for f in old.__dataclass_fields__.values()} - {"id", "schema_version", "revision", "created_at", "updated_at"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValidationError(f"unknown fields: {sorted(unknown)}")
        if entity_type == "evidence" and "content" in changes:
            if not isinstance(changes["content"], str):
                raise ValidationError("evidence content must be text")
            if "content_hash" not in changes:
                changes["content_hash"] = hashlib.sha256(changes["content"].encode()).hexdigest()
        if entity_type == "evidence" and "content_hash" in changes:
            digest = changes["content_hash"]
            content = changes.get("content", old.content)  # type: ignore[attr-defined]
            if not _is_sha256(digest):
                raise ValidationError("content hash must be a lowercase SHA-256 digest")
            if content and digest != hashlib.sha256(content.encode()).hexdigest():
                raise ValidationError("content hash does not match content")
            if not content and not self._verify_external_evidence(digest):
                raise ValidationError(
                    "blank evidence requires a trusted external verifier for its content hash"
                )
        now = self._tick(timestamp)
        obj = replace(old, **changes, revision=old.revision + 1, updated_at=now)
        self._table(entity_type)[entity_id] = obj
        if entity_type == "assignment": self._assignments[entity_id] = obj  # type: ignore[assignment]
        if entity_type == "comment": self._comments[entity_id] = obj  # type: ignore[assignment]
        if entity_type == "mention": self._mentions[entity_id] = obj  # type: ignore[assignment]
        audit_payload = {
            "changed_fields": sorted(changes),
            "revision": obj.revision,
            "entity_hash": hashlib.sha256(_canonical(asdict(obj)).encode("utf-8")).hexdigest(),
        }
        if entity_type == "evidence" and "content" in changes:
            audit_payload["content_hash"] = obj.content_hash  # type: ignore[attr-defined]
            audit_payload["content_redacted"] = True
        self._record("update", entity_type, entity_id, actor, audit_payload, timestamp=now)
        if entity_type == "evidence" and getattr(old, "content_hash", None) != getattr(obj, "content_hash", None):
            # Approval captures hashes, never a mutable evidence pointer.  A
            # changed hash therefore invalidates every affected approval.
            for aid, approval in tuple(self._tables["approval"].items()):
                if getattr(old, "content_hash", None) in approval.evidence_hashes and approval.status in {"requested", "approved"}:
                    invalid = replace(approval, status="invalidated", revision=approval.revision + 1, updated_at=now, reason="evidence changed")
                    self._tables["approval"][aid] = invalid
                    self._record("approval_invalidated", "approval", aid, actor, {"evidence_id": entity_id}, timestamp=now)
            self._invalidate_gate_proofs(
                lambda proof: any(evidence_id == entity_id for evidence_id, _digest in proof.evidence_bindings),
                actor_id=actor,
                reason="bound evidence changed",
                timestamp=now,
            )
        return obj

    def _evidence_bindings(
        self,
        initiative_id: str,
        evidence_ids: Iterable[str],
        *,
        require_one: bool,
    ) -> Tuple[Tuple[str, str], ...]:
        raw_identifiers = tuple(evidence_ids)
        if any(not isinstance(evidence_id, str) or not evidence_id for evidence_id in raw_identifiers):
            raise TransitionError("gate evidence references must be non-empty Evidence IDs")
        identifiers = tuple(dict.fromkeys(raw_identifiers))
        if require_one and not identifiers:
            raise TransitionError("gate completion requires at least one Evidence ID")
        bindings = []
        for evidence_id in identifiers:
            try:
                evidence = self._require("evidence", evidence_id)
            except NotFound as exc:
                raise TransitionError(f"gate evidence does not exist: {evidence_id}") from exc
            if evidence.initiative_id != initiative_id:
                raise TransitionError("gate evidence belongs to another initiative")
            if not _is_sha256(evidence.content_hash):
                raise TransitionError("gate evidence content hash is invalid")
            if evidence.content and hashlib.sha256(evidence.content.encode("utf-8")).hexdigest() != evidence.content_hash:
                raise TransitionError("gate evidence content hash is invalid")
            if not evidence.content and not self._verify_external_evidence(evidence.content_hash):
                raise TransitionError(
                    "blank gate evidence requires trusted external verification"
                )
            bindings.append((evidence.id, evidence.content_hash))
        return tuple(sorted(bindings))

    def _approval_for_gate(
        self,
        initiative: Initiative,
        stage: LifecycleStage,
        bindings: Tuple[Tuple[str, str], ...],
        approval_id: Optional[str],
        *,
        required: bool,
    ) -> Optional[Approval]:
        if approval_id is None:
            if required:
                raise ApprovalError(
                    f"regulated {stage.value} checkpoint requires an independently approved Approval ID"
                )
            return None
        try:
            approval = self._require("approval", approval_id)
        except NotFound as exc:
            raise ApprovalError("gate approval does not exist") from exc
        if approval.initiative_id != initiative.id or approval.stage != stage:
            raise ApprovalError("gate approval belongs to another initiative or lifecycle stage")
        if approval.status != "approved" or approval.approved_at is None:
            raise ApprovalError("gate approval is not currently approved")
        if not approval.requester_id or approval.requester_id == approval.approver_id:
            raise ApprovalError("gate approval does not satisfy maker-checker separation")
        if not approval.policy_version:
            raise ApprovalError("gate approval has no policy version")
        if sorted(approval.evidence_hashes) != sorted(digest for _evidence_id, digest in bindings):
            raise ApprovalError("gate approval evidence does not match the gate evidence")
        return approval

    def _invalidate_gate_proofs(
        self,
        predicate: Callable[[GateProof], bool],
        *,
        actor_id: str,
        reason: str,
        timestamp: Optional[int] = None,
    ) -> None:
        for key, proof in tuple(self._gates.items()):
            if not predicate(proof):
                continue
            del self._gates[key]
            self._record(
                "gate_invalidated",
                "initiative",
                proof.initiative_id,
                actor_id,
                {"stage": proof.stage.value, "reason": reason},
                timestamp=timestamp,
            )

    @_transactional
    def complete_gate(
        self,
        initiative_id: str,
        stage: LifecycleStage | str,
        *,
        evidence_ids: Sequence[str] = (),
        prerequisites: Iterable[str] = (),
        approval_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        expected_revision: int,
    ) -> Initiative:
        """Complete the current stage with immutable Evidence ID/hash bindings.

        ``prerequisites`` remains as a compatibility alias, but its members are
        interpreted only as Evidence IDs. Arbitrary labels never become facts.
        """
        init = self._allowed(initiative_id, actor_id, "transition")
        actor = self._public_actor(actor_id)
        stage = _stage(stage)
        if init.revision != expected_revision:
            raise RevisionConflict(f"initiative:{initiative_id} expected revision {expected_revision}, current {init.revision}")
        if stage != init.stage:
            raise TransitionError(f"gate belongs to current stage {init.stage.value}, not {stage.value}")
        supplied = tuple(evidence_ids) + tuple(prerequisites)
        bindings = self._evidence_bindings(initiative_id, supplied, require_one=True)
        supplied_ids = {evidence_id for evidence_id, _digest in bindings}
        required_evidence = self._gate_requirements.get((initiative_id, stage), set())
        if not required_evidence.issubset(supplied_ids):
            raise TransitionError("required gate Evidence IDs are not all supplied")
        product = self._require("product", init.product_id)
        approval = self._approval_for_gate(
            init,
            stage,
            bindings,
            approval_id,
            required=product.regulated and stage in REGULATED_APPROVAL_STAGES,
        )
        payload = {
            "stage": stage.value,
            "revision": init.revision + 1,
            "evidence": [
                {"evidence_id": evidence_id, "content_hash": digest}
                for evidence_id, digest in bindings
            ],
            "approval_id": approval.id if approval is not None else None,
            "policy_version": approval.policy_version if approval is not None else "",
        }
        event = self._record("gate_completed", "initiative", initiative_id, actor, payload)
        self._gates[(initiative_id, stage)] = GateProof(
            initiative_id=initiative_id,
            stage=stage,
            evidence_bindings=bindings,
            actor_id=actor,
            completed_at=event.timestamp,
            approval_id=approval.id if approval is not None else None,
            policy_version=approval.policy_version if approval is not None else "",
        )
        updated = replace(init, revision=init.revision + 1, updated_at=event.timestamp)
        self._tables["initiative"][initiative_id] = updated
        return updated

    @_transactional
    def set_gate_requirements(self, initiative_id: str, stage: LifecycleStage | str, requirements: Iterable[str], *, actor_id: Optional[str] = None) -> Tuple[str, ...]:
        self._allowed(initiative_id, actor_id, "transition")
        actor = self._public_actor(actor_id)
        stage = _stage(stage)
        bindings = self._evidence_bindings(initiative_id, requirements, require_one=False)
        values = {evidence_id for evidence_id, _digest in bindings}
        self._gate_requirements[(initiative_id, stage)] = values
        current = self._gates.get((initiative_id, stage))
        if current is not None and not values.issubset(
            {evidence_id for evidence_id, _digest in current.evidence_bindings}
        ):
            self._invalidate_gate_proofs(
                lambda proof: proof.initiative_id == initiative_id and proof.stage == stage,
                actor_id=actor,
                reason="gate requirements changed",
            )
        self._record(
            "gate_requirements_set",
            "initiative",
            initiative_id,
            actor,
            {
                "stage": stage.value,
                "evidence": [
                    {"evidence_id": evidence_id, "content_hash": digest}
                    for evidence_id, digest in bindings
                ],
            },
        )
        return tuple(sorted(values))

    configure_gate = set_gate_requirements

    satisfy_gate = complete_gate
    pass_gate = complete_gate

    @_transactional
    def transition_initiative(self, initiative_id: str, target: LifecycleStage | str, *, expected_revision: int, actor_id: Optional[str] = None, prerequisites: Iterable[str] = (), timestamp: Optional[int] = None) -> Initiative:
        current = self._allowed(initiative_id, actor_id, "transition")
        actor = self._public_actor(actor_id)
        target = _stage(target)
        if current.revision != expected_revision:
            raise RevisionConflict(f"initiative:{initiative_id} expected revision {expected_revision}, current {current.revision}")
        if target not in TRANSITIONS[current.stage]:
            raise TransitionError(f"transition {current.stage.value}->{target.value} is not allowed")
        proof = self._gates.get((initiative_id, current.stage))
        if proof is None:
            raise TransitionError(f"missing evidence-backed {current.stage.value} gate proof")
        bound_ids = {evidence_id for evidence_id, _digest in proof.evidence_bindings}
        asserted = set(prerequisites)
        if asserted and not asserted.issubset(bound_ids):
            raise TransitionError("asserted prerequisites are not bound Evidence IDs")
        required = self._gate_requirements.get((initiative_id, current.stage), set())
        if not required.issubset(bound_ids):
            raise TransitionError("configured gate Evidence IDs are not bound")
        product = self._require("product", current.product_id)
        self._approval_for_gate(
            current,
            current.stage,
            proof.evidence_bindings,
            proof.approval_id,
            required=product.regulated and current.stage in REGULATED_APPROVAL_STAGES,
        )
        now = self._tick(timestamp)
        updated = replace(current, stage=target, retired=target == LifecycleStage.RETIRED, revision=current.revision + 1, updated_at=now)
        self._tables["initiative"][initiative_id] = updated
        self._record("transition", "initiative", initiative_id, actor, {"from": current.stage.value, "to": target.value, "revision": updated.revision}, timestamp=now)
        return updated

    advance_initiative = transition_initiative
    advance = transition_initiative
    transition = transition_initiative

    @_transactional
    def retire_initiative(self, initiative_id: str, *, expected_revision: int, actor_id: Optional[str] = None, timestamp: Optional[int] = None) -> Initiative:
        return self.transition_initiative(initiative_id, LifecycleStage.RETIRED, expected_revision=expected_revision, actor_id=actor_id, timestamp=timestamp)

    @_transactional
    def create_user(self, name: str, *, actor_id: Optional[str] = None, **kwargs: Any) -> User:
        actor = self._require_os_admin(actor_id)
        return self._create("user", actor, name=name, **self._creation_extras(kwargs))  # type: ignore[return-value]

    @_transactional
    def add_membership(self, product_id: str, user_id: str, role: str, *, actor_id: Optional[str] = None, **kwargs: Any) -> Membership:
        self._require("product", product_id); self._require("user", user_id)
        actor = self._require_product_action(product_id, actor_id, "admin")
        role = role.lower()
        if role not in {"admin", "owner", "pm", "contributor", "viewer", "approver", "auditor"}:
            raise ValidationError(f"unknown role: {role}")
        for m in self._tables["membership"].values():
            if m.product_id == product_id and m.user_id == user_id:
                return self.update("membership", m.id, expected_revision=m.revision, actor_id=actor, role=role)  # type: ignore[return-value]
        return self._create("membership", actor, product_id=product_id, user_id=user_id, role=role, **self._creation_extras(kwargs))  # type: ignore[return-value]

    grant_role = add_membership
    add_product_membership = add_membership

    def _role(self, product_id: str, user_id: str) -> Optional[str]:
        roles = [m.role for m in self._tables["membership"].values() if m.product_id == product_id and m.user_id == user_id]
        return max(roles, key=lambda x: {"viewer": 0, "auditor": 1, "contributor": 2, "pm": 3, "approver": 3, "owner": 4, "admin": 5}.get(x, -1)) if roles else None

    def authorize(self, product_id: str, user_id: str, action: str) -> bool:
        role = self._role(product_id, user_id)
        if role is None:
            return False
        if action in {"view", "comment", "mention"}:
            return True
        if action in {"assign", "edit", "transition", "decision", "experiment", "release"}:
            return role in {"admin", "owner", "pm", "contributor"}
        if action in {"approve", "revoke_approval"}:
            return role in {"admin", "owner", "approver"}
        if action == "audit":
            return role in {"admin", "owner", "auditor"}
        return role in {"admin", "owner"}

    check_permission = authorize

    def _allowed(self, initiative_id: str, actor_id: Optional[str], action: str) -> Initiative:
        init = self._require("initiative", initiative_id)
        actor = self._public_actor(actor_id)
        if not self.authorize(init.product_id, actor, action):
            raise PermissionDenied(f"{actor} cannot {action} initiative {initiative_id}")
        return init

    @_transactional
    def assign(self, initiative_id: str, assignee_id: str, *, actor_id: Optional[str] = None, role: str = "owner", **kwargs: Any) -> Assignment:
        init = self._allowed(initiative_id, actor_id, "assign")
        actor = self._public_actor(actor_id)
        self._require("user", assignee_id)
        if not self.authorize(init.product_id, assignee_id, "view") and assignee_id != "system":
            raise PermissionDenied("assignee is not a product member")
        result = self._create("assignment", actor, initiative_id=initiative_id, assignee_id=assignee_id, role=role, **self._creation_extras(kwargs))
        self._assignments[result.id] = result
        return result  # type: ignore[return-value]

    assignment = assign

    @_transactional
    def comment(self, initiative_id: str, body: str, *, actor_id: str, **kwargs: Any) -> Comment:
        self._allowed(initiative_id, actor_id, "comment")
        actor = self._public_actor(actor_id)
        result = self._create("comment", actor, initiative_id=initiative_id, author_id=actor, body=body, **self._creation_extras(kwargs))
        self._comments[result.id] = result
        return result  # type: ignore[return-value]

    add_comment = comment

    @_transactional
    def mention(self, initiative_id: str, mentioned_user_id: str, *, actor_id: str, comment_id: Optional[str] = None, **kwargs: Any) -> Mention:
        init = self._allowed(initiative_id, actor_id, "mention")
        actor = self._public_actor(actor_id)
        self._require("user", mentioned_user_id)
        if not self.authorize(init.product_id, mentioned_user_id, "view"):
            raise PermissionDenied("mentioned user is not a product member")
        if comment_id is not None:
            c = self._require("comment", comment_id)
            if c.initiative_id != initiative_id:
                raise ValidationError("comment belongs to another initiative")
        result = self._create("mention", actor, initiative_id=initiative_id, author_id=actor, mentioned_user_id=mentioned_user_id, comment_id=comment_id, **self._creation_extras(kwargs))
        self._mentions[result.id] = result
        return result  # type: ignore[return-value]

    add_mention = mention

    @_transactional
    def link(self, source_id: str, target_id: str, relation: str, *, actor_id: Optional[str] = None) -> tuple[str, str, str]:
        source = self.get(source_id); target = self.get(target_id)
        st = next(k for k, cls in ENTITY_TYPES.items() if isinstance(source, cls)); tt = next(k for k, cls in ENTITY_TYPES.items() if isinstance(target, cls))
        if relation not in TRACE_RELATION_NAMES:
            raise RelationError(f"unknown relation: {relation}")
        if tt not in TRACE_TARGETS.get(st, ()):
            raise RelationError(f"invalid typed relation {st} -[{relation}]-> {tt}")
        si = getattr(source, "initiative_id", None); ti = getattr(target, "initiative_id", None)
        if si != ti:
            raise RelationError("traceability entities must belong to the same initiative")
        self._allowed(si, actor_id, "edit")
        actor = self._public_actor(actor_id)
        edge = (source_id, target_id, relation)
        if edge not in self._relations:
            self._relations.append(edge)
            self._record("link", st, source_id, actor, {"target_id": target_id, "relation": relation})
        return edge

    add_trace = link
    link_trace = link
    add_relation = link
    add_traceability = link

    def traces(self, entity_id: str, *, actor_id: Optional[str] = None) -> Tuple[tuple[str, str, str], ...]:
        self.get(entity_id, actor_id=actor_id)
        return tuple(e for e in self._relations if e[0] == entity_id or e[1] == entity_id)

    @_transactional
    def request_approval(self, initiative_id: str, *, evidence_ids: Sequence[str] = (), policy_version: str = "", regulated: Optional[bool] = None, actor_id: Optional[str] = None, **kwargs: Any) -> Approval:
        init = self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        product = self._require("product", init.product_id)
        # A caller may opt into stronger handling, never downgrade a product's
        # stored regulatory classification for one request.
        is_regulated = product.regulated or regulated is True
        hashes = []
        for eid in evidence_ids:
            ev = self._require("evidence", eid)
            if ev.initiative_id != initiative_id:
                raise ApprovalError("evidence belongs to another initiative")
            hashes.append(ev.content_hash)
        if is_regulated and (not policy_version or not hashes):
            raise ApprovalError("regulated approval requires policy version and evidence hashes")
        result = self._create("approval", actor, initiative_id=initiative_id, stage=init.stage, requester_id=actor, approver_id="", policy_version=policy_version, evidence_hashes=tuple(hashes), **self._creation_extras(kwargs))
        return result  # type: ignore[return-value]

    create_approval = request_approval

    @_transactional
    def approve(self, approval_id: str, *, approver_id: str, timestamp: Optional[int] = None, evidence_ids: Sequence[str] = (), policy_version: Optional[str] = None) -> Approval:
        approval = self._require("approval", approval_id)
        init = self._allowed(approval.initiative_id, approver_id, "approve")
        product = self._require("product", init.product_id)
        if approver_id == approval.requester_id:
            raise ApprovalError("requester and approver must be different users")
        if approval.status != "requested":
            raise ApprovalError("only a pending approval request can be approved")
        if approval.stage != init.stage:
            raise ApprovalError("approval request belongs to an earlier lifecycle stage")
        if product.regulated and (not approver_id or not approval.policy_version or not approval.evidence_hashes):
            raise ApprovalError("regulated approval requires authority, timestamp, evidence hashes, and policy version")
        if policy_version is not None and policy_version != approval.policy_version:
            raise ApprovalError("policy version mismatch")
        ids = tuple(evidence_ids)
        if ids:
            current_evidence = tuple(self._require("evidence", eid) for eid in ids)
            if any(evidence.initiative_id != approval.initiative_id for evidence in current_evidence):
                raise ApprovalError("evidence belongs to another initiative")
            current_hashes = tuple(evidence.content_hash for evidence in current_evidence)
        else:
            available = {
                evidence.content_hash for evidence in self._tables["evidence"].values()
                if evidence.initiative_id == approval.initiative_id
            }
            if any(digest not in available for digest in approval.evidence_hashes):
                raise ApprovalError("evidence changed; approval must be re-requested")
            current_hashes = approval.evidence_hashes
        if tuple(current_hashes) != tuple(approval.evidence_hashes):
            raise ApprovalError("evidence changed; approval must be re-requested")
        now = self._tick(timestamp)
        result = replace(approval, approver_id=approver_id, status="approved", approved_at=now, revision=approval.revision + 1, updated_at=now)
        self._tables["approval"][approval_id] = result
        self._record("approve", "approval", approval_id, approver_id, {"evidence_hashes": result.evidence_hashes, "policy_version": result.policy_version}, timestamp=now)
        return result

    @_transactional
    def revoke_approval(self, approval_id: str, *, actor_id: str, reason: str = "", timestamp: Optional[int] = None) -> Approval:
        approval = self._require("approval", approval_id)
        init = self._allowed(approval.initiative_id, actor_id, "revoke_approval")
        now = self._tick(timestamp)
        result = replace(approval, status="revoked", revoked_at=now, reason=reason, revision=approval.revision + 1, updated_at=now)
        self._tables["approval"][approval_id] = result
        self._record("revoke_approval", "approval", approval_id, actor_id, {"reason": reason}, timestamp=now)
        self._invalidate_gate_proofs(
            lambda proof: proof.approval_id == approval_id,
            actor_id=actor_id,
            reason="bound approval revoked",
            timestamp=now,
        )
        return result

    revoke = revoke_approval

    @_transactional
    def score_initiative(self, initiative_id: str, score: float, *, actor_id: Optional[str] = None, expected_revision: Optional[int] = None) -> PortfolioAllocation:
        init = self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        if not self._finite_number(score):
            raise AllocationError("score must be a finite number")
        existing = next((a for a in self._tables["portfolio_allocation"].values() if a.initiative_id == initiative_id), None)
        if existing:
            if expected_revision is None: expected_revision = existing.revision
            return self.update("portfolio_allocation", existing.id, expected_revision=expected_revision, actor_id=actor, score=float(score))  # type: ignore[return-value]
        product = self._require("product", init.product_id)
        return self._create("portfolio_allocation", actor, product_id=product.id, initiative_id=initiative_id, score=float(score))  # type: ignore[return-value]

    set_priority = score_initiative
    set_score = score_initiative

    @_transactional
    def set_capacity(self, product_id: str, period: str, capacity: float, *, actor_id: Optional[str] = None) -> float:
        actor = self._require_product_action(product_id, actor_id, "edit")
        if not self._finite_number(capacity) or capacity < 0:
            raise AllocationError("capacity must be a finite non-negative number")
        self._capacity[(product_id, period)] = float(capacity)
        self._record("set_capacity", "product", product_id, actor, {"period": period, "capacity": capacity})
        return float(capacity)

    @_transactional
    def allocate_capacity(self, initiative_id: str, period: str, capacity: float, *, actor_id: Optional[str] = None, expected_revision: Optional[int] = None) -> PortfolioAllocation:
        init = self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        if not self._finite_number(capacity) or capacity < 0:
            raise AllocationError("allocation must be a finite non-negative number")
        limit = self._capacity.get((init.product_id, period))
        allocated = sum(a.capacity for a in self._tables["portfolio_allocation"].values() if a.product_id == init.product_id and a.period == period and a.initiative_id != initiative_id)
        if limit is not None and allocated + capacity > limit:
            raise AllocationError(f"capacity over-allocation: {allocated + capacity} > {limit}")
        old = next((a for a in self._tables["portfolio_allocation"].values() if a.initiative_id == initiative_id and a.period == period), None)
        if old:
            if expected_revision is None: expected_revision = old.revision
            return self.update("portfolio_allocation", old.id, expected_revision=expected_revision, actor_id=actor, capacity=float(capacity))  # type: ignore[return-value]
        return self._create("portfolio_allocation", actor, product_id=init.product_id, initiative_id=initiative_id, period=period, capacity=float(capacity))  # type: ignore[return-value]

    allocate = allocate_capacity

    @_transactional
    def sequence_initiative(self, initiative_id: str, sequence: int, *, actor_id: Optional[str] = None, period: str = "", expected_revision: Optional[int] = None) -> PortfolioAllocation:
        init = self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise AllocationError("sequence must be a non-negative integer")
        old = next((a for a in self._tables["portfolio_allocation"].values() if a.initiative_id == initiative_id and a.period == period), None)
        if old:
            if expected_revision is None: expected_revision = old.revision
            return self.update("portfolio_allocation", old.id, expected_revision=expected_revision, actor_id=actor, sequence=int(sequence))  # type: ignore[return-value]
        return self._create("portfolio_allocation", actor, product_id=init.product_id, initiative_id=initiative_id, period=period, sequence=int(sequence))  # type: ignore[return-value]

    sequence = sequence_initiative

    @_transactional
    def add_dependency(self, initiative_id: str, depends_on_id: str, *, actor_id: Optional[str] = None, relationship: str = "blocks", **kwargs: Any) -> Dependency:
        left = self._allowed(initiative_id, actor_id, "edit")
        actor = self._public_actor(actor_id)
        right = self._require("initiative", depends_on_id)
        if initiative_id == depends_on_id:
            raise AllocationError("dependency cycle")
        if left.product_id != right.product_id:
            raise AllocationError("cross-product dependencies require an explicit portfolio relation")
        graph: Dict[str, set[str]] = {}
        for d in self._tables["dependency"].values(): graph.setdefault(d.initiative_id, set()).add(d.depends_on_id)
        graph.setdefault(initiative_id, set()).add(depends_on_id)
        def reaches(start: str, wanted: str, seen: set[str]) -> bool:
            if start == wanted: return True
            if start in seen: return False
            seen.add(start)
            return any(reaches(n, wanted, seen) for n in graph.get(start, ()))
        if reaches(depends_on_id, initiative_id, set()):
            raise AllocationError("dependency cycle")
        return self._create("dependency", actor, initiative_id=initiative_id, depends_on_id=depends_on_id, relationship=relationship, **self._creation_extras(kwargs))  # type: ignore[return-value]

    add_dependency_edge = add_dependency

    def rollup(
        self,
        product_id: Optional[str] = None,
        period: Optional[str] = None,
        *,
        actor_id: Optional[str] = None,
    ) -> Mapping[str, Any]:
        if product_id is not None:
            self._require("product", product_id)
        actor: Optional[str] = None
        if actor_id is not None:
            actor = self._public_actor(actor_id)
            if product_id is not None and not self.authorize(product_id, actor, "view"):
                raise PermissionDenied(f"{actor} cannot view product {product_id}")
        def visible(candidate_product_id: str) -> bool:
            return actor is None or self.authorize(candidate_product_id, actor, "view")
        allocs = [
            allocation for allocation in self._tables["portfolio_allocation"].values()
            if (product_id is None or allocation.product_id == product_id)
            and (period is None or allocation.period == period)
            and visible(allocation.product_id)
        ]
        dependencies = [
            dependency for dependency in self._tables["dependency"].values()
            if (product_id is None or self._require("initiative", dependency.initiative_id).product_id == product_id)
            and visible(self._require("initiative", dependency.initiative_id).product_id)
        ]
        return {
            "product_id": product_id,
            "period": period,
            "initiative_count": len({allocation.initiative_id for allocation in allocs}),
            "capacity": sum(allocation.capacity for allocation in allocs),
            "score": sum(allocation.score for allocation in allocs),
            "sequence": [
                allocation.initiative_id
                for allocation in sorted(allocs, key=lambda value: (value.sequence, value.initiative_id))
            ],
            "dependencies": len(dependencies),
        }

    portfolio_rollup = rollup
    product_rollup = rollup
    dependency_rollup = rollup

    def entity_history(self, entity_id: str, *, actor_id: Optional[str] = None) -> Tuple[AuditEvent, ...]:
        self.get(entity_id, actor_id=actor_id)
        return tuple(event for event in self.history if event.entity_id == entity_id)

    def export_audit(self) -> str:
        """Export the redacted full audit chain for trusted-host administration."""
        events = [asdict(e) for e in self._audit]
        return _canonical({"schema_version": SCHEMA_VERSION, "events": events})

    audit_export = export_audit

    @staticmethod
    def verify_audit_export(exported: str | Mapping[str, Any]) -> bool:
        try:
            doc = json.loads(exported) if isinstance(exported, str) else dict(exported)
            if doc.get("schema_version") != SCHEMA_VERSION: return False
            previous = "0" * 64
            events = doc["events"]
            for index, event in enumerate(events, 1):
                if event["sequence"] != index or event["previous_hash"] != previous: return False
                body = {k: event[k] for k in ("sequence", "timestamp", "action", "entity_type", "entity_id", "actor_id", "payload", "previous_hash", "schema_version")}
                digest = hashlib.sha256(_canonical(body).encode()).hexdigest()
                if digest != event["event_hash"]: return False
                previous = digest
            return True
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, ValidationError):
            return False

    verify_audit = verify_audit_export

    def relation_history(self, *, actor_id: Optional[str] = None) -> Tuple[tuple[str, str, str], ...]:
        if actor_id is None:
            return tuple(self._relations)
        actor = self._public_actor(actor_id)
        visible = []
        for edge in self._relations:
            try:
                self.get(edge[0], actor_id=actor)
            except PermissionDenied:
                continue
            visible.append(edge)
        return tuple(visible)

    def gate_history(self, initiative_id: str, *, actor_id: Optional[str] = None) -> Tuple[AuditEvent, ...]:
        self.get(initiative_id, "initiative", actor_id=actor_id)
        return tuple(event for event in self.history if event.entity_type == "initiative" and event.entity_id == initiative_id and event.action in {"gate_completed", "gate_invalidated", "transition"})

    def gate_proof(
        self,
        initiative_id: str,
        stage: LifecycleStage | str,
        *,
        actor_id: Optional[str] = None,
    ) -> GateProof:
        """Return the immutable evidence/approval binding for one completed gate."""
        self.get(initiative_id, "initiative", actor_id=actor_id)
        stage = _stage(stage)
        try:
            return self._gates[(initiative_id, stage)]
        except KeyError as exc:
            raise NotFound(f"gate:{initiative_id}:{stage.value}") from exc

    def completed_gates(self, initiative_id: str, *, actor_id: Optional[str] = None) -> Tuple[str, ...]:
        self.get(initiative_id, "initiative", actor_id=actor_id)
        return tuple(
            sorted(
                f"{stage.value}:complete"
                for stored_initiative, stage in self._gates
                if stored_initiative == initiative_id
            )
        )


# Friendly names for callers that call the aggregate ``Domain`` or ``Store``.
Domain = PMOSDomain
DomainStore = PMOSDomain
StaleRevision = RevisionConflict
ConflictError = RevisionConflict

__all__ = [
    "SCHEMA_VERSION", "SNAPSHOT_FORMAT", "SNAPSHOT_PATH", "LifecycleStage", "STAGES", "TRANSITIONS", "REGULATED_APPROVAL_STAGES", "ENTITY_TYPES", "Entity",
    "Organization", "Product", "Initiative", "Opportunity", "Experiment", "Release", "Decision", "Risk", "Approval", "Dependency", "PortfolioAllocation", "Evidence", "Metric", "User", "Membership", "Assignment", "Comment", "Mention", "AuditEvent", "GateProof", "PMOSDomain", "Domain", "DomainStore", "DomainError", "NotFound", "ValidationError", "AuthorizationError", "PermissionDenied", "RevisionConflict", "StaleRevision", "ConflictError", "TransitionError", "RelationError", "ApprovalError", "AllocationError",
    "PersistenceError", "BootstrapError",
]
