"""Query shared phase state for each product bank.

This module reads conductor and contract data to answer, for every phase of a
product, what the phase must show, what is done, what is missing, the next step,
who approves it, and what blocks progress, without writing any files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .conductor import Conductor


def phase_report(conductor: Conductor, contract: dict | None, root: Path) -> list[dict[str, Any]]:
    state = conductor.state()
    position = conductor.next_turn()
    stale = conductor.stale_gates()

    bank_index = state["current_bank"]
    bank_map = {
        bank["id"]: bank for bank in contract["banks"]
    } if contract is not None else {}
    signoffs = contract.get("signoffs", {}) if contract is not None and isinstance(contract, dict) else {}
    stale_map = {entry["bank_id"]: entry for entry in stale if isinstance(entry, dict)}
    stale_ids = set(stale_map)

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

        outcomes = []
        for row in contract_questions:
            questions = row.get("questions", [])
            if not questions:
                met = None
            else:
                met = all(
                    isinstance(answers.get(question_id), dict) and not answers.get(question_id).get("parked")
                    for question_id in questions
                )
            outcomes.append({
                "line": row["line"],
                "evidenced_by": row.get("evidenced_by"),
                "questions": questions,
                "met": met,
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

        missing = {
            "questions": [question_id for question_id in answer_order
                          if question_id not in answers],
            "parked": list(bank_state["parked"]),
            "gate_lines": [outcome["line"] for outcome in outcomes if outcome["met"] is False],
        }

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
        })
    return result
