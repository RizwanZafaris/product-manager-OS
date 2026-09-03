"""A deterministic, durable, one-question-at-a-time PM Conductor.

The conductor intentionally contains no model call or inference.  A caller
supplies versioned question banks and evidence records; this module enforces
the interview protocol and persists its state through :class:`pmos.store.Store`.
The Store's product-head token is the optimistic-concurrency revision.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping, Optional, Sequence

from .store import NotFoundError, ProductHead, Store, ValidationError, canonical_json


STATE_PATH = ".pmos/conductor/state.json"
STATE_VERSION = "pmos.conductor.v2"
MAX_BANKS = 32
MAX_QUESTIONS_PER_BANK = 128
MAX_PROMPT_CHARS = 2048
MAX_ANSWER_CHARS = 8192
MAX_TEXT_CHARS = 2048
MAX_TURN_ID_CHARS = 160
# Durable idempotency retention window; older keys are safely evicted.
MAX_TURN_RESULTS = 1024
MAX_STATE_BYTES = 1024 * 1024
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,127}$")
_BANNED_OPENERS = ("everyone", "obviously", "we believe", "users want", "growing fast")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class EvidenceClass(str, Enum):
    OBSERVED_BEHAVIOR = "observed_behavior"
    ARTIFACT = "artifact"
    NAMED_COMMITMENT = "named_commitment"
    INTERVIEW_CLAIM = "interview_claim"
    TEAM_BELIEF = "team_belief"


@dataclass(frozen=True)
class Question:
    """A stable question definition.  ``id`` must never be recycled."""

    id: str
    prompt: str
    evidence_class: EvidenceClass | str

    def __post_init__(self) -> None:
        _identifier(self.id, "question id")
        _bounded_text(self.prompt, "prompt", MAX_PROMPT_CHARS)
        EvidenceClass(self.evidence_class)

    @property
    def required_evidence(self) -> EvidenceClass:
        return EvidenceClass(self.evidence_class)


@dataclass(frozen=True)
class QuestionBank:
    """Immutable bank definition pinned by its ID, version, and definition hash."""

    id: str
    version: str
    questions: Sequence[Question]
    gate_prerequisites: Sequence[str] = ()
    gate_approvers: Sequence[str] = ()

    def __post_init__(self) -> None:
        _identifier(self.id, "bank id")
        _identifier(self.version, "bank version")
        try:
            questions = tuple(self.questions)
            prerequisites = tuple(self.gate_prerequisites)
            approver_values = tuple(self.gate_approvers)
        except TypeError as exc:
            raise ValidationError("question bank sequences must be iterable") from exc
        if not questions or len(questions) > MAX_QUESTIONS_PER_BANK:
            raise ValidationError("question bank must contain 1 to %d questions" % MAX_QUESTIONS_PER_BANK)
        ids = [question.id for question in questions]
        if len(ids) != len(set(ids)):
            raise ValidationError("question IDs must be unique within a bank")
        for prerequisite in prerequisites:
            _identifier(prerequisite, "gate prerequisite")
        approvers = tuple(_identifier(item, "gate approver")
                          for item in approver_values)
        if len(approvers) != len(set(approvers)):
            raise ValidationError("gate approvers must be unique")
        object.__setattr__(self, "questions", questions)
        object.__setattr__(self, "gate_prerequisites", prerequisites)
        object.__setattr__(self, "gate_approvers", approvers)

    @property
    def definition_hash(self) -> str:
        body = {
            "id": self.id,
            "version": self.version,
            "questions": [{"id": q.id, "prompt": q.prompt, "evidence_class": q.required_evidence.value}
                          for q in self.questions],
            "gate_prerequisites": list(self.gate_prerequisites),
            "gate_approvers": list(self.gate_approvers),
        }
        return hashlib.sha256(canonical_json(body)).hexdigest()


@dataclass(frozen=True)
class TurnOutcome:
    """A serializable result; consumers should branch on ``status`` explicitly."""

    status: str
    revision: Optional[str]
    bank_id: Optional[str] = None
    question: Optional[Question] = None
    message: str = ""
    challenge_count: int = 0
    accepted: bool = False
    completed: bool = False
    conflict_revision: Optional[str] = None


class Conductor:
    """Persist a product's interview in a Store snapshot.

    Question banks are ordered stages.  Completing a bank is not enough to
    open the next one: ``prove_gate`` must record all declared prerequisites.
    This is deliberately separate from question answers so an answer cannot
    masquerade as a gate sign-off or external evidence. Turn idempotency
    records are retained in a bounded 1024-result window. Once an old record
    is evicted, replay is no longer guaranteed to return its original result;
    the current cursor, gate, and expected-revision checks still apply, so an
    evicted retry cannot bypass the protocol.
    """

    def __init__(self, store: Store, product_id: str, banks: Sequence[QuestionBank], *,
                 gate_source_verifier: Optional[Callable[[str, str], bool]] = None) -> None:
        if not isinstance(store, Store):
            raise ValidationError("store must be a Store")
        _identifier(product_id, "product id")
        if not banks or len(banks) > MAX_BANKS:
            raise ValidationError("conductor must have 1 to %d banks" % MAX_BANKS)
        normalized = tuple(_coerce_bank(bank) for bank in banks)
        bank_ids = [bank.id for bank in normalized]
        if len(bank_ids) != len(set(bank_ids)):
            raise ValidationError("bank IDs must be unique")
        self.store = store
        self.product_id = product_id
        self.banks = normalized
        self._by_id = {bank.id: bank for bank in normalized}
        if gate_source_verifier is not None and not callable(gate_source_verifier):
            raise ValidationError("gate_source_verifier must be callable")
        self._gate_source_verifier = gate_source_verifier
        try:
            self.store.head(product_id)
        except NotFoundError:
            self.store.create_product(product_id)

    # ------------------------------ public turns ------------------------------
    def next_turn(self, *, expected_revision: Optional[str | int | ProductHead] = None) -> TurnOutcome:
        """Return exactly one pending question, a blocked result, or completion."""
        snapshot, state = self._load()
        conflict = self._expected_conflict(expected_revision, snapshot.head)
        if conflict:
            return conflict
        return self._position(snapshot.head.token, state)

    next_question = next_turn

    def submit_answer(self, question_id: str, answer: str, evidence: Mapping[str, Any], *,
                      expected_revision: str | int | ProductHead, turn_id: str) -> TurnOutcome:
        """Accept or challenge the currently offered question, atomically.

        Invalid evidence consumes one of at most two challenges.  The third
        invalid submission is blocked and leaves the cursor unchanged.
        """
        _identifier(question_id, "question id")
        _identifier(turn_id, "turn id", MAX_TURN_ID_CHARS)
        request_hash = _request_hash("answer", {
            "question_id": question_id, "answer": answer,
            "evidence": _evidence_mapping(evidence),
        })
        snapshot, state = self._load()
        duplicate = self._duplicate(state, turn_id, request_hash, snapshot.head.token)
        if duplicate is not None:
            return duplicate
        conflict = self._expected_conflict(expected_revision, snapshot.head)
        if conflict:
            return conflict
        position = self._position(snapshot.head.token, state)
        if position.status != "question":
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked" if position.status == "blocked" else position.status, snapshot.head.token,
                bank_id=position.bank_id, message=position.message, completed=position.completed))
        if position.question is None or position.question.id != question_id:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "conflict", snapshot.head.token, bank_id=position.bank_id,
                message="answer does not match the current question", conflict_revision=snapshot.head.token))
        question = position.question
        valid, reason, normalized_evidence = self._validate_answer(question, answer, evidence)
        bank_state = state["banks"][position.bank_id]
        if not valid:
            previous = int(bank_state["challenges"].get(question.id, 0))
            count = min(2, previous + 1)
            bank_state["challenges"][question.id] = count
            if count >= 2:
                bank_state["parked"].append(question.id)
                outcome = TurnOutcome("blocked", snapshot.head.token, bank_id=position.bank_id,
                                      question=question, message="question parked after two challenges: " + reason,
                                      challenge_count=count)
            else:
                outcome = TurnOutcome("challenge", snapshot.head.token, bank_id=position.bank_id,
                                      question=question, message=reason, challenge_count=count)
            return self._record(snapshot, state, turn_id, request_hash, outcome)
        bank_state["answers"][question.id] = {
            "answer": answer,
            "evidence": normalized_evidence,
            "evidence_class": question.required_evidence.value,
        }
        bank_state["cursor"] += 1
        outcome = TurnOutcome("accepted", snapshot.head.token, bank_id=position.bank_id, question=question,
                              message="answer accepted", accepted=True)
        return self._record(snapshot, state, turn_id, request_hash, outcome)

    answer = submit_answer

    def prove_gate(self, bank_id: str, evidence: Mapping[str, Any], *, expected_revision: str | int | ProductHead,
                   turn_id: str) -> TurnOutcome:
        """Record independently checkable proof needed to leave a completed bank."""
        _identifier(bank_id, "bank id")
        _identifier(turn_id, "turn id", MAX_TURN_ID_CHARS)
        if bank_id not in self._by_id:
            raise ValidationError("unknown bank")
        supplied = _evidence_mapping(evidence)
        request_hash = _request_hash("gate", {"bank_id": bank_id,
                                                "evidence": supplied})
        snapshot, state = self._load()
        duplicate = self._duplicate(state, turn_id, request_hash, snapshot.head.token)
        if duplicate is not None:
            return duplicate
        conflict = self._expected_conflict(expected_revision, snapshot.head)
        if conflict:
            return conflict
        index = int(state["current_bank"])
        if index >= len(self.banks) or self.banks[index].id != bank_id:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id, message="only the current completed bank may be gated"))
        bank = self._by_id[bank_id]
        bank_state = state["banks"][bank_id]
        if bank_state["cursor"] != len(bank.questions) or bank_state["parked"]:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id, message="all questions must be accepted before gate proof"))
        required_fields = {"source", "source_sha256", "actor_id", "requester_id",
                           "decision", "approved_at", *bank.gate_prerequisites}
        if set(supplied) != required_fields:
            missing_or_unknown = sorted(required_fields.symmetric_difference(supplied))
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate proof schema mismatch: " + ", ".join(missing_or_unknown)))
        missing = [name for name in required_fields if not _truthy_text(supplied.get(name))]
        if missing:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="unproven gate prerequisites: " + ", ".join(missing)))
        try:
            actor_id = _identifier(supplied["actor_id"], "gate actor")
            requester_id = _identifier(supplied["requester_id"], "gate requester")
        except ValidationError as exc:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id, message=str(exc)))
        if actor_id == requester_id:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate approval requires a different maker and checker"))
        if actor_id not in bank.gate_approvers:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate actor is not authorized by the pinned question bank"))
        if supplied["decision"] != "approved" or not _UTC.match(supplied["approved_at"]):
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate decision or UTC approval timestamp is invalid"))
        if not _HEX64.match(supplied["source_sha256"]):
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate source hash is invalid"))
        if self._gate_source_verifier is None:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate source verifier is not configured"))
        try:
            verified = self._gate_source_verifier(supplied["source"],
                                                  supplied["source_sha256"])
        except Exception:
            verified = False
        if verified is not True:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate source could not be verified"))
        if "signed_by" in supplied and supplied["signed_by"] != actor_id:
            return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
                "blocked", snapshot.head.token, bank_id=bank_id,
                message="gate signer does not match the authorized actor"))
        proof = dict(supplied)
        state["gates"][bank_id] = {
            "proof": proof,
            "proof_sha256": hashlib.sha256(canonical_json(proof)).hexdigest(),
        }
        state["current_bank"] += 1
        status = "completed" if state["current_bank"] == len(self.banks) else "advanced"
        return self._record(snapshot, state, turn_id, request_hash, TurnOutcome(
            status, snapshot.head.token, bank_id=bank_id, message="gate proof recorded", completed=status == "completed"))

    complete_gate = prove_gate

    def state(self) -> Mapping[str, Any]:
        """Return a defensive JSON-compatible copy of persisted conductor state."""
        _snapshot, state = self._load()
        return json.loads(canonical_json(state).decode("utf-8"))

    # ------------------------------ persistence ------------------------------
    def _load(self) -> tuple[Any, dict[str, Any]]:
        snapshot = self.store.read_snapshot(self.product_id)
        raw = snapshot.files.get(STATE_PATH)
        if raw is None:
            return snapshot, self._new_state()
        if len(raw) > MAX_STATE_BYTES:
            raise ValidationError("conductor state exceeds safety bound")
        try:
            state = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("conductor state is not valid UTF-8 JSON") from exc
        self._validate_state(state)
        return snapshot, state

    def _new_state(self) -> dict[str, Any]:
        return {
            "schema": STATE_VERSION,
            "current_bank": 0,
            "banks": {bank.id: {"version": bank.version, "definition_hash": bank.definition_hash,
                                  "cursor": 0, "answers": {}, "challenges": {}, "parked": []}
                      for bank in self.banks},
            "gates": {}, "turn_results": {},
        }

    def _validate_state(self, state: Any) -> None:
        if not isinstance(state, dict) or state.get("schema") != STATE_VERSION:
            raise ValidationError("unsupported conductor state")
        if set(state) != {"schema", "current_bank", "banks", "gates", "turn_results"}:
            raise ValidationError("conductor state has unknown or missing fields")
        if not isinstance(state["current_bank"], int) or not 0 <= state["current_bank"] <= len(self.banks):
            raise ValidationError("conductor state has invalid cursor")
        if not isinstance(state["banks"], dict) or set(state["banks"]) != set(self._by_id):
            raise ValidationError("conductor bank set does not match persisted state")
        for bank in self.banks:
            saved = state["banks"][bank.id]
            if not isinstance(saved, dict) or saved.get("version") != bank.version or saved.get("definition_hash") != bank.definition_hash:
                raise ValidationError("question bank definition changed; create a new bank version")
            if not isinstance(saved.get("cursor"), int) or not 0 <= saved["cursor"] <= len(bank.questions):
                raise ValidationError("conductor bank cursor is invalid")
            if not isinstance(saved.get("answers"), dict) or not isinstance(saved.get("challenges"), dict) or not isinstance(saved.get("parked"), list):
                raise ValidationError("conductor bank state is invalid")
            question_ids = {question.id for question in bank.questions}
            if (not set(saved["answers"]).issubset(question_ids) or
                    not set(saved["challenges"]).issubset(question_ids) or
                    not set(saved["parked"]).issubset(question_ids) or
                    len(saved["parked"]) != len(set(saved["parked"]))):
                raise ValidationError("conductor bank has unknown question state")
            expected_answer_ids = {question.id for question in bank.questions[:saved["cursor"]]}
            if set(saved["answers"]) != expected_answer_ids:
                raise ValidationError("conductor answers do not match the durable cursor")
            for question_id, count in saved["challenges"].items():
                if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 2:
                    raise ValidationError("conductor challenge count is invalid")
                if question_id in saved["parked"] and count != 2:
                    raise ValidationError("parked question lacks two challenges")
        if not isinstance(state["gates"], dict) or not isinstance(state["turn_results"], dict):
            raise ValidationError("conductor state is invalid")
        completed_ids = {bank.id for bank in self.banks[:state["current_bank"]]}
        if set(state["gates"]) != completed_ids:
            raise ValidationError("conductor gates do not match the durable bank cursor")
        for bank in self.banks[:state["current_bank"]]:
            saved = state["banks"][bank.id]
            if saved["cursor"] != len(bank.questions) or saved["parked"]:
                raise ValidationError("gated bank is not complete")
        for bank_id, gate in state["gates"].items():
            if not isinstance(gate, dict) or set(gate) != {"proof", "proof_sha256"} or \
                    not isinstance(gate["proof"], dict):
                raise ValidationError("stored gate proof is malformed")
            actual = hashlib.sha256(canonical_json(gate["proof"])).hexdigest()
            if gate.get("proof_sha256") != actual:
                raise ValidationError("stored gate proof hash does not match")
            bank = self._by_id[bank_id]
            base = {"source", "source_sha256", "actor_id", "requester_id",
                    "decision", "approved_at", *bank.gate_prerequisites}
            if set(gate["proof"]) != base or gate["proof"].get("actor_id") not in bank.gate_approvers:
                raise ValidationError("stored gate proof violates its pinned policy")
        if len(state["turn_results"]) > MAX_TURN_RESULTS:
            raise ValidationError("conductor idempotency record limit exceeded")
        for turn_id, record in state["turn_results"].items():
            _identifier(turn_id, "stored turn id", MAX_TURN_ID_CHARS)
            if not isinstance(record, dict) or set(record) != {"request_sha256", "outcome"} or \
                    not isinstance(record.get("request_sha256"), str) or \
                    not _HEX64.match(record["request_sha256"]):
                raise ValidationError("stored idempotency record is malformed")
            _outcome_from_data(record["outcome"])

    def _record(self, snapshot: Any, state: dict[str, Any], turn_id: str,
                request_hash: str, outcome: TurnOutcome) -> TurnOutcome:
        state["turn_results"][turn_id] = {
            "request_sha256": request_hash,
            "outcome": _outcome_data(outcome),
        }
        # Evict oldest logical commits before publishing. The order is
        # derived from the pre-commit store revision embedded in each outcome,
        # rather than dict insertion order (canonical JSON sorts object keys).
        while len(state["turn_results"]) > MAX_TURN_RESULTS:
            self._evict_oldest_turn_result(state)
        encoded = canonical_json(state)
        while len(encoded) > MAX_STATE_BYTES and len(state["turn_results"]) > 1:
            self._evict_oldest_turn_result(state)
            encoded = canonical_json(state)
        if len(encoded) > MAX_STATE_BYTES:
            del state["turn_results"][turn_id]
            return TurnOutcome("blocked", snapshot.head.token, message="conductor state exceeds safety bound")
        files = dict(snapshot.files)
        files[STATE_PATH] = encoded
        committed = self.store.commit(self.product_id, files, expected_revision=snapshot.head,
                                      metadata={"kind": "pmos.conductor.turn", "turn_id": turn_id})
        if not committed.committed:
            return TurnOutcome("conflict", snapshot.head.token, message="store revision changed", conflict_revision=committed.conflict.current.token if committed.conflict else None)
        return TurnOutcome(outcome.status, committed.head.token, bank_id=outcome.bank_id,
                           question=outcome.question, message=outcome.message,
                           challenge_count=outcome.challenge_count, accepted=outcome.accepted,
                           completed=outcome.completed, conflict_revision=outcome.conflict_revision)

    @staticmethod
    def _turn_result_order(record: Mapping[str, Any], turn_id: str) -> tuple[int, str, str]:
        """Return a durable best-effort age key for a turn result."""
        outcome = record.get("outcome")
        revision = outcome.get("revision") if isinstance(outcome, Mapping) else None
        prefix = revision.split(":", 1)[0] if isinstance(revision, str) else ""
        try:
            sequence = int(prefix)
        except (TypeError, ValueError):
            sequence = -1
        return sequence, str(revision or ""), turn_id

    def _evict_oldest_turn_result(self, state: dict[str, Any]) -> None:
        if not state["turn_results"]:
            return
        oldest = min(
            state["turn_results"].items(),
            key=lambda item: self._turn_result_order(item[1], item[0]),
        )[0]
        del state["turn_results"][oldest]

    def _duplicate(self, state: Mapping[str, Any], turn_id: str,
                   request_hash: str, current_revision: str) -> Optional[TurnOutcome]:
        record = state["turn_results"].get(turn_id)
        if record is None:
            return None
        if record["request_sha256"] != request_hash:
            return TurnOutcome(
                "conflict", current_revision,
                message="turn id was already used for a different request",
                conflict_revision=current_revision)
        outcome = _outcome_from_data(record["outcome"])
        # The state snapshot records the pre-commit token because the Store
        # determines the commit hash.  A replay observes the current durable
        # head, while preserving the original logical result.
        return TurnOutcome(outcome.status, current_revision, bank_id=outcome.bank_id,
                           question=outcome.question, message=outcome.message,
                           challenge_count=outcome.challenge_count, accepted=outcome.accepted,
                           completed=outcome.completed, conflict_revision=outcome.conflict_revision)

    def _expected_conflict(self, expected: Optional[str | int | ProductHead], head: ProductHead) -> Optional[TurnOutcome]:
        if expected is None:
            return None
        if isinstance(expected, ProductHead):
            matches = expected.token == head.token
        elif isinstance(expected, int):
            matches = expected == head.revision
        else:
            matches = isinstance(expected, str) and expected == head.token
        if not matches:
            return TurnOutcome("conflict", head.token, message="expected revision is stale", conflict_revision=head.token)
        return None

    def _position(self, revision: str, state: Mapping[str, Any]) -> TurnOutcome:
        index = int(state["current_bank"])
        if index >= len(self.banks):
            return TurnOutcome("completed", revision, message="all banks and gates are complete", completed=True)
        bank = self.banks[index]
        saved = state["banks"][bank.id]
        if saved["parked"]:
            return TurnOutcome("blocked", revision, bank_id=bank.id,
                               message="a question is parked after two challenges")
        cursor = int(saved["cursor"])
        if cursor == len(bank.questions):
            return TurnOutcome("blocked", revision, bank_id=bank.id,
                               message="answers are complete; gate prerequisites still require proof")
        return TurnOutcome("question", revision, bank_id=bank.id, question=bank.questions[cursor])

    def _validate_answer(self, question: Question, answer: str, evidence: Mapping[str, Any]) -> tuple[bool, str, dict[str, str]]:
        try:
            _bounded_text(answer, "answer", MAX_ANSWER_CHARS)
            normal = _evidence_mapping(evidence)
        except ValidationError as exc:
            return False, str(exc), {}
        lowered = answer.strip().lower()
        if question.required_evidence is not EvidenceClass.TEAM_BELIEF and any(lowered.startswith(item) for item in _BANNED_OPENERS):
            return False, "answer starts with a banned unsupported generalization", normal
        evidence_class = normal.get("class")
        if evidence_class != question.required_evidence.value:
            return False, "evidence class must be " + question.required_evidence.value, normal
        required: dict[EvidenceClass, tuple[str, ...]] = {
            EvidenceClass.OBSERVED_BEHAVIOR: ("source", "date", "location"),
            EvidenceClass.ARTIFACT: ("source", "location"),
            EvidenceClass.NAMED_COMMITMENT: ("person", "source"),
            EvidenceClass.INTERVIEW_CLAIM: ("person", "source", "date"),
            EvidenceClass.TEAM_BELIEF: ("source",),
        }
        missing = [field for field in required[question.required_evidence] if not _truthy_text(normal.get(field))]
        if missing:
            return False, "missing evidence fields: " + ", ".join(missing), normal
        return True, "", normal


def _coerce_bank(value: QuestionBank) -> QuestionBank:
    if not isinstance(value, QuestionBank):
        raise ValidationError("banks must contain QuestionBank values")
    return value


def _identifier(value: Any, label: str, maximum: int = 128) -> str:
    if not isinstance(value, str) or len(value) > maximum or not _ID.match(value):
        raise ValidationError("%s must be a bounded stable identifier" % label)
    return value


def _bounded_text(value: Any, label: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value or len(value) > maximum:
        raise ValidationError("%s must be a bounded non-empty string" % label)
    return value


def _truthy_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence_mapping(value: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(value, Mapping) or len(value) > 16:
        raise ValidationError("evidence must be a small mapping")
    normal: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not _ID.match(key) or not isinstance(item, str) or "\x00" in item or len(item) > MAX_TEXT_CHARS:
            raise ValidationError("evidence contains an invalid field")
        normal[key] = item.strip()
    return normal


def _request_hash(operation: str, payload: Mapping[str, Any]) -> str:
    """Bind an idempotency key to one semantic request, never just an outcome."""
    return hashlib.sha256(canonical_json({
        "operation": operation,
        "payload": payload,
    })).hexdigest()


def _outcome_data(outcome: TurnOutcome) -> dict[str, Any]:
    data = asdict(outcome)
    question = data.get("question")
    if question is not None:
        data["question"] = {"id": question["id"], "prompt": question["prompt"], "evidence_class": EvidenceClass(question["evidence_class"]).value}
    return data


def _outcome_from_data(data: Any) -> TurnOutcome:
    fields = {"status", "revision", "bank_id", "question", "message",
              "challenge_count", "accepted", "completed", "conflict_revision"}
    if not isinstance(data, dict) or set(data) != fields:
        raise ValidationError("stored turn result is invalid")
    copied = dict(data)
    question = copied.get("question")
    if question is not None:
        if not isinstance(question, dict) or set(question) != {
                "id", "prompt", "evidence_class"}:
            raise ValidationError("stored turn question is invalid")
        copied["question"] = Question(question["id"], question["prompt"], question["evidence_class"])
    try:
        outcome = TurnOutcome(**copied)
    except (TypeError, ValueError) as exc:
        raise ValidationError("stored turn result is invalid") from exc
    if (outcome.status not in {"question", "challenge", "blocked", "accepted",
                              "advanced", "completed", "conflict"} or
            not isinstance(outcome.challenge_count, int) or
            isinstance(outcome.challenge_count, bool) or
            outcome.challenge_count < 0 or outcome.challenge_count > 2 or
            not isinstance(outcome.accepted, bool) or
            not isinstance(outcome.completed, bool)):
        raise ValidationError("stored turn result values are invalid")
    return outcome
