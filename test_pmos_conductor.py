"""Executable contract for the persistent deterministic Conductor."""

from __future__ import annotations

import os
import hashlib
import subprocess
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.conductor import Conductor, EvidenceClass, Question, QuestionBank
from pmos.store import Store


BANKS = (
    QuestionBank("discover", "v1", (
        Question("discover.person", "Who did the behavior?", EvidenceClass.OBSERVED_BEHAVIOR),
        Question("discover.cost", "What artifact records the cost?", EvidenceClass.ARTIFACT),
    ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),
    QuestionBank("define", "v1", (
        Question("define.sponsor", "Who committed in writing?", EvidenceClass.NAMED_COMMITMENT),
    ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),
)


def observed() -> dict[str, str]:
    return {"class": "observed_behavior", "source": "session replay", "date": "2026-09-03", "location": "replay/17"}


def artifact() -> dict[str, str]:
    return {"class": "artifact", "source": "support export", "location": "exports/cost.csv"}


def commitment() -> dict[str, str]:
    return {"class": "named_commitment", "person": "Mina", "source": "approval email"}


GATE_BYTES = b"independent gate evidence\n"
GATE_HASH = hashlib.sha256(GATE_BYTES).hexdigest()


def gate_proof(*, actor: str = "asha", requester: str = "mina",
               source: str = "gate-1.md", source_hash: str = GATE_HASH) -> dict[str, str]:
    return {"source": source, "source_sha256": source_hash,
            "actor_id": actor, "requester_id": requester,
            "decision": "approved", "approved_at": "2026-09-03T00:00:00Z",
            "signed_by": actor}


class ConductorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.path = Path(self.temp.name) / "runtime.sqlite"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def opening(self) -> tuple[Store, Conductor]:
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        return store, Conductor(store, "payments", BANKS,
                                gate_source_verifier=verifier)

    def test_three_turns_survive_reopen_and_subprocess_exit(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        self.assertEqual(first.status, "question")
        accepted = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                           expected_revision=first.revision, turn_id="turn-1")
        self.assertEqual(accepted.status, "accepted")
        store.close()

        store, conductor = self.opening()  # separate Conductor/Store opening two
        second = conductor.next_turn()
        self.assertEqual(second.question.id, "discover.cost")
        accepted = conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                           expected_revision=second.revision, turn_id="turn-2")
        self.assertEqual(accepted.status, "accepted")
        store.close()

        # A separate process opens the DB and exits immediately after observing
        # the durable cursor: no in-memory object participates in recovery.
        script = "from pmos.store import Store; from pmos.conductor import Conductor; from test_pmos_conductor import BANKS; import sys; s=Store(sys.argv[1]); c=Conductor(s,'payments',BANKS); assert c.next_turn().status == 'blocked'"
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).parent))
        subprocess.run([sys.executable, "-c", script, str(self.path)], check=True, env=env)

        store, conductor = self.opening()  # separate opening three
        blocked = conductor.next_turn()
        self.assertEqual(blocked.status, "blocked")
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 2)
        gated = conductor.prove_gate("discover", gate_proof(),
                                     expected_revision=blocked.revision, turn_id="gate-1")
        self.assertEqual(gated.status, "advanced")
        third = conductor.next_turn()
        self.assertEqual(third.question.id, "define.sponsor")
        self.assertEqual(conductor.submit_answer("define.sponsor", "Mina approved scope.", commitment(),
                                                 expected_revision=third.revision, turn_id="turn-3").status, "accepted")
        store.close()

    def test_invalid_does_not_advance_and_challenge_is_capped(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        invalid = {"class": "observed_behavior", "source": "heard it"}
        one = conductor.submit_answer("discover.person", "Everyone needs it.", invalid,
                                      expected_revision=turn.revision, turn_id="bad-1")
        self.assertEqual((one.status, one.challenge_count), ("challenge", 1))
        two = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                      expected_revision=one.revision, turn_id="bad-2")
        self.assertEqual((two.status, two.challenge_count), ("blocked", 2))
        self.assertEqual(conductor.next_turn().status, "blocked")
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 0)
        store.close()

    def test_duplicate_turn_and_stale_revision_are_explicit(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        first = conductor.submit_answer("discover.person", "Mina exported it.", observed(),
                                        expected_revision=turn.revision, turn_id="same-turn")
        duplicate = conductor.submit_answer("discover.person", "different payload", observed(),
                                            expected_revision=turn.revision, turn_id="same-turn")
        self.assertEqual(duplicate.status, "conflict")
        self.assertIn("different request", duplicate.message)
        self.assertEqual(duplicate.revision, first.revision)
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 1)
        stale = conductor.submit_answer("discover.cost", "file", artifact(),
                                        expected_revision=turn.revision, turn_id="stale")
        self.assertEqual(stale.status, "conflict")
        self.assertEqual(conductor.next_turn().question.id, "discover.cost")
        store.close()

    def test_completion_requires_answers_and_each_gate(self) -> None:
        store, conductor = self.opening()
        initial = conductor.next_turn()
        early = conductor.prove_gate("discover", gate_proof(),
                                     expected_revision=initial.revision, turn_id="early-gate")
        self.assertEqual(early.status, "blocked")
        current = conductor.next_turn()
        a1 = conductor.submit_answer("discover.person", "Mina exported it.", observed(), expected_revision=current.revision, turn_id="a1")
        current = conductor.next_turn()
        a2 = conductor.submit_answer("discover.cost", "Cost is in export.", artifact(), expected_revision=current.revision, turn_id="a2")
        missing_proof = gate_proof()
        del missing_proof["signed_by"]
        missing = conductor.prove_gate("discover", missing_proof, expected_revision=a2.revision, turn_id="missing")
        self.assertEqual(missing.status, "blocked")
        self.assertEqual(conductor.prove_gate("discover", gate_proof(), expected_revision=missing.revision, turn_id="ok-gate").status, "advanced")
        current = conductor.next_turn()
        answer = conductor.submit_answer("define.sponsor", "Mina signed.", commitment(), expected_revision=current.revision, turn_id="d1")
        self.assertEqual(conductor.next_turn().status, "blocked")
        done = conductor.prove_gate("define", gate_proof(), expected_revision=answer.revision, turn_id="done")
        self.assertEqual(done.status, "completed")
        self.assertTrue(conductor.next_turn().completed)
        store.close()

    def test_gate_proof_requires_authority_independence_and_verified_hash(self) -> None:
        store, conductor = self.opening()
        current = conductor.next_turn()
        one = conductor.submit_answer("discover.person", "Mina exported it.", observed(),
                                      expected_revision=current.revision, turn_id="proof-a1")
        current = conductor.next_turn()
        two = conductor.submit_answer("discover.cost", "Cost is in export.", artifact(),
                                      expected_revision=current.revision, turn_id="proof-a2")
        same_actor = conductor.prove_gate("discover", gate_proof(requester="asha"),
                                          expected_revision=two.revision, turn_id="same-actor")
        self.assertEqual(same_actor.status, "blocked")
        unauthorized = conductor.prove_gate("discover", gate_proof(actor="mallory"),
                                             expected_revision=same_actor.revision,
                                             turn_id="unauthorized")
        self.assertEqual(unauthorized.status, "blocked")
        tampered = conductor.prove_gate("discover", gate_proof(source_hash="0" * 64),
                                       expected_revision=unauthorized.revision,
                                       turn_id="tampered-proof")
        self.assertEqual(tampered.status, "blocked")
        accepted = conductor.prove_gate("discover", gate_proof(),
                                       expected_revision=tampered.revision,
                                       turn_id="verified-proof")
        self.assertEqual(accepted.status, "advanced")
        persisted = conductor.state()["gates"]["discover"]
        self.assertEqual(persisted["proof"]["source_sha256"], GATE_HASH)
        self.assertEqual(len(persisted["proof_sha256"]), 64)
        store.close()

    def test_question_bank_freezes_all_sequences(self) -> None:
        questions = [Question("q", "What happened?", EvidenceClass.OBSERVED_BEHAVIOR)]
        prerequisites = ["signed_by"]
        approvers = ["asha"]
        bank = QuestionBank("frozen", "v1", questions, prerequisites, approvers)
        questions.append(Question("later", "Should not appear.", EvidenceClass.ARTIFACT))
        prerequisites.append("forged")
        approvers.append("mallory")
        self.assertIsInstance(bank.questions, tuple)
        self.assertIsInstance(bank.gate_prerequisites, tuple)
        self.assertIsInstance(bank.gate_approvers, tuple)
        self.assertEqual(tuple(q.id for q in bank.questions), ("q",))
        self.assertEqual(bank.gate_prerequisites, ("signed_by",))
        self.assertEqual(bank.gate_approvers, ("asha",))

    def test_evicted_turn_is_state_checked_and_window_does_not_permanently_block(self) -> None:
        store, conductor = self.opening()
        with patch("pmos.conductor.MAX_TURN_RESULTS", 2):
            turn = conductor.next_turn()
            first = conductor.submit_answer(
                "wrong.question", "Mina exported it.", observed(),
                expected_revision=turn.revision, turn_id="window-1")
            self.assertEqual(first.status, "conflict")
            second = conductor.submit_answer(
                "wrong.question", "Mina exported it.", observed(),
                expected_revision=first.revision, turn_id="window-2")
            self.assertEqual(second.status, "conflict")
            third = conductor.submit_answer(
                "wrong.question", "Mina exported it.", observed(),
                expected_revision=second.revision, turn_id="window-3")
            self.assertEqual(third.status, "conflict")
            self.assertNotIn("window-1", conductor.state()["turn_results"])
            self.assertIn("window-2", conductor.state()["turn_results"])
            replay = conductor.submit_answer(
                "wrong.question", "different", observed(),
                expected_revision=third.revision, turn_id="window-2")
            self.assertEqual(replay.status, "conflict")
            self.assertIn("different request", replay.message)
        store.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
