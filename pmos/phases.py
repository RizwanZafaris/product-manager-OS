"""Query shared phase state for each product bank.

This module reads conductor and contract data to answer, for every phase of a
product, what the phase must show, what is done, what is missing, the next step,
who approves it, and what blocks progress, without writing any files.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .artifacts import scan
from .conductor import Conductor

_LANDS_IN_MD_RE = re.compile(r"`([^`]+\.md)`")


def approval_summary(bank_id: str, state: dict[str, Any]) -> dict[str, Any] | None:
    """The recorded gate approval for one bank, or None without one.

    Reads state["gates"][bank_id]: the proof's actor_id and approved_at, the
    attestation the record carries (or "local" when it has none), the ids the
    approved manifest names in "artifacts" and "dependencies" (None for both
    when the record has no manifest), and how many times this bank's approval
    has since been superseded.
    """
    record = state["gates"].get(bank_id)
    if not record:
        return None
    proof = record["proof"]
    manifest = record.get("manifest")
    if manifest is not None:
        artifact_ids = [entry["id"] for entry in manifest.get("artifacts", [])]
        dependency_ids = [entry["id"] for entry in manifest.get("dependencies", [])]
    else:
        artifact_ids = None
        dependency_ids = None
    return {
        "bank_id": bank_id,
        "attestation": record.get("attestation", "local"),
        "actor_id": proof.get("actor_id"),
        "approved_at": proof.get("approved_at"),
        "artifacts": artifact_ids,
        "dependencies": dependency_ids,
        "superseded": len(state.get("superseded_gates", {}).get(bank_id, [])),
    }


def rejection_summaries(bank_id: str, state: dict[str, Any]) -> list[dict[str, Any]]:
    """One entry per recorded gate rejection for this bank, in stored order.

    Each rejection carries its own manifest, so the artifacts it named are
    reported even when the bank's approval (if any) was never touched.
    """
    records = state.get("gate_rejections", {}).get(bank_id, [])
    summaries = []
    for record in records:
        proof = record["proof"]
        manifest = record.get("manifest", {})
        summaries.append({
            "bank_id": bank_id,
            "actor_id": proof.get("actor_id"),
            "rejected_at": record.get("rejected_at"),
            "artifacts": [entry["id"] for entry in manifest.get("artifacts", [])],
        })
    return summaries


def _named_documents(contract_bank: dict[str, Any] | None, root: Path) -> list[dict[str, Any]]:
    """The distinct `*.md` paths a contract bank's questions land in.

    Collected from every question's "lands_in" text, in first-seen order.
    present is True when the named path is a regular file under root.
    """
    if contract_bank is None:
        return []
    seen: set[str] = set()
    paths: list[str] = []
    for question in contract_bank.get("questions", []):
        for path in _LANDS_IN_MD_RE.findall(question.get("lands_in", "") or ""):
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return [{"path": path, "present": (root / path).is_file()} for path in paths]


def _manifest_revisions(gate_record: dict[str, Any] | None) -> dict[str, str]:
    """id to revision, from a gate record's manifest artifacts and dependencies."""
    if not gate_record:
        return {}
    manifest = gate_record.get("manifest")
    if not manifest:
        return {}
    revisions: dict[str, str] = {}
    for section in ("artifacts", "dependencies"):
        for entry in manifest.get(section, []):
            revisions[entry["id"]] = entry["revision"]
    return revisions


def phase_report(conductor: Conductor, contract: dict | None, root: Path) -> list[dict[str, Any]]:
    state = conductor.state()
    position = conductor.next_turn()
    stale = conductor.stale_gates()
    scanned = scan(root)

    bank_index = state["current_bank"]
    bank_map = {
        bank["id"]: bank for bank in contract["banks"]
    } if contract is not None else {}
    signoffs = contract.get("signoffs", {}) if contract is not None and isinstance(contract, dict) else {}
    stale_map = {entry["bank_id"]: entry for entry in stale if isinstance(entry, dict)}
    stale_ids = set(stale_map)

    # Which bank owns each question id. A gate_rendering row may cite a question from an
    # earlier bank: the shipped DELIVER row "AI overlay: guardrails live, kill switch tested"
    # cites BUILD-5 and BUILD-6. Looked up in the citing bank's own answers, as this did
    # before, those ids are never found and the row reports met=false forever while the gate
    # reports approved. Every shipped id is globally unique, so a flat map is exact.
    owner_of: dict[str, str] = {}
    for owning in conductor.banks:
        for question in owning.questions:
            owner_of.setdefault(question.id, owning.id)

    result: list[dict[str, Any]] = []
    for index, bank in enumerate(conductor.banks):
        bank_state = state["banks"][bank.id]
        contract_bank = bank_map.get(bank.id)

        contract_questions = []
        if contract_bank is not None:
            contract_questions = [question for question in contract_bank.get("gate_rendering", [])]
        phase = contract_bank.get("stage", bank.id.upper()) if contract_bank is not None else bank.id.upper()
        gate = contract_bank.get("gate") if contract_bank is not None else None

        answers = bank_state["answers"]
        answer_order = [question.id for question in bank.questions]
        accepted = [
            question_id for question_id in answer_order
            if isinstance(answers.get(question_id), dict) and not answers.get(question_id).get("parked")
        ]
        complete_with_source = sum(1 for question_id in accepted
                                   if answers[question_id].get("verification") == "source_verified")
        complete_without_source = len(accepted) - complete_with_source

        def _answer_for(question_id: str):
            owner = owner_of.get(question_id)
            if owner is None:
                return None
            return state["banks"][owner]["answers"].get(question_id)

        outcomes = []
        for row in contract_questions:
            questions = row.get("questions", [])
            if not questions:
                met = None
                answered_in = {}
            else:
                met = all(
                    isinstance(_answer_for(question_id), dict)
                    and not _answer_for(question_id).get("parked")
                    for question_id in questions
                )
                answered_in = {question_id: owner_of[question_id]
                               for question_id in questions if question_id in owner_of}
            # A row satisfied wholly or partly by another bank's answer is marked. The
            # runtime holds no re-verification fact: it knows BUILD-5 was answered once, at
            # Gate 4, and the row's own evidence text asks for it "re-verified against the
            # release candidate". Reporting met=true with no marker would turn a visible
            # false negative into an invisible false positive, which is the worse of the two.
            carried = sorted({owner for question_id, owner in answered_in.items()
                              if owner != bank.id})
            outcomes.append({
                "line": row["line"],
                "evidenced_by": row.get("evidenced_by"),
                "questions": questions,
                "met": met,
                "answered_in": answered_in,
                "carried": carried,
            })

        if bank.id in stale_ids:
            phase_state = "stale"
        elif bank.id in state["gates"]:
            phase_state = "approved"
        elif index == bank_index:
            if bank_state["parked"]:
                phase_state = "blocked"
            elif all(
                    isinstance(answers.get(question_id), dict) and not answers.get(question_id).get("parked")
                    for question_id in answer_order
            ) and not bank_state.get("reopened"):
                phase_state = "awaiting_approval"
            else:
                phase_state = "in_progress"
        else:
            phase_state = "not_started"

        if bank_state["parked"]:
            first_parked = bank_state["parked"][0]
        else:
            first_parked = None

        if index == bank_index and position.status == "stale":
            next_action = None
        elif stale_map:
            if bank.id in stale_ids:
                next_action = {"action": "gate", "bank_id": bank.id, "question_id": None}
            else:
                next_action = None
        elif bank.id == position.bank_id:
            if position.status == "question":
                next_action = {"action": "answer", "bank_id": bank.id,
                               "question_id": position.question.id if position.question else None}
            elif position.status == "blocked" and first_parked is not None:
                next_action = {"action": "reopen", "bank_id": bank.id, "question_id": first_parked}
            elif position.status == "blocked":
                next_action = {"action": "gate", "bank_id": bank.id, "question_id": None}
            else:
                next_action = None
        else:
            next_action = None

        if index == bank_index and position.status == "stale":
            blocking_reason = "the approval for %s no longer holds; prove it again first" % position.bank_id
        elif phase_state == "stale":
            blocking_reason = stale_map[bank.id]["message"]
        elif phase_state == "approved":
            blocking_reason = None
        elif index == bank_index:
            if phase_state == "awaiting_approval":
                blocking_reason = "waits for Gate %s approval" % gate
            elif phase_state == "blocked" and first_parked is not None:
                blocking_reason = position.message
            else:
                blocking_reason = None
        else:
            if index == 0:
                blocking_reason = None
            else:
                previous = bank_map.get(conductor.banks[index - 1].id, {})
                blocking_reason = "waits for Gate %s (%s)" % (previous.get("gate"), previous.get("stage"))

        stale_entry = stale_map.get(bank.id)
        missing = {
            "questions": [question_id for question_id in answer_order
                          if question_id not in answers],
            "parked": list(bank_state["parked"]),
            "gate_lines": [outcome["line"] for outcome in outcomes if outcome["met"] is False],
            # Rows the contract renders with no question behind them: a human signature the
            # runtime cannot see. They were in neither list, so nothing named them at all.
            "unknown_gate_lines": [outcome["line"] for outcome in outcomes
                                   if outcome["met"] is None],
            "changed": list(stale_entry["changed"]) if stale_entry else [],
            "reconcile": list(stale_entry["reconcile"]) if stale_entry else [],
        }

        if gate is not None:
            manifest_revisions = _manifest_revisions(state["gates"].get(bank.id))
            documents = [
                {
                    "id": artifact_id,
                    "path": scanned[artifact_id]["path"],
                    "phase": scanned[artifact_id]["phase"],
                    "status": scanned[artifact_id]["status"],
                    "revision": scanned[artifact_id]["revision"],
                    "approved_revision": manifest_revisions.get(artifact_id),
                }
                for artifact_id in sorted(
                    artifact_id for artifact_id, record in scanned.items() if record["gate"] == gate)
            ]
        else:
            documents = []

        result.append({
            "phase": phase,
            "bank_id": bank.id,
            "gate": gate,
            "state": phase_state,
            "outcomes": outcomes,
            "completed": {
                "questions": accepted,
                "source_verified": complete_with_source,
                "supplied_unverified": complete_without_source,
            },
            "missing": missing,
            "next_action": next_action,
            "required_approver": {
                "runtime": list(bank.gate_approvers),
                "attestation": "local",
                "signoff_roles": signoffs.get(str(gate)) if bank.gate_approvers is not None and gate is not None else None,
            },
            "blocking_reason": blocking_reason,
            "documents": documents,
            "named_documents": _named_documents(contract_bank, root),
            "approval": approval_summary(bank.id, state),
            "rejections": rejection_summaries(bank.id, state),
        })
    return result
