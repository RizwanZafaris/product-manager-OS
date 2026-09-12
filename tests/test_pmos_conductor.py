"""Executable contract for the persistent deterministic Conductor."""

from __future__ import annotations

import os
import hashlib
import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.conductor import Conductor, EvidenceClass, Question, QuestionBank, TurnOutcome
from pmos.store import Store, ValidationError
from pmos.banks import LEGACY_ONBOARDING, banks_from_contract, load_contract, shipped_banks


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
               source: str = "gate-1.md", source_hash: str = GATE_HASH,
               approved_at: str = "2026-09-03T00:00:00Z") -> dict[str, str]:
    return {"source": source, "source_sha256": source_hash,
            "actor_id": actor, "requester_id": requester,
            "decision": "approved", "approved_at": approved_at,
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

    def cost_offered(self, conductor: Conductor) -> TurnOutcome:
        """Answer discover.person, so that discover.cost is the question offered."""
        first = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=first.revision, turn_id="person")
        offered = conductor.next_turn()
        self.assertEqual((offered.status, offered.question.id), ("question", "discover.cost"))
        return offered

    def test_evidence_stronger_than_the_question_asks_is_accepted(self) -> None:
        store, conductor = self.opening()
        offered = self.cost_offered(conductor)
        accepted = conductor.submit_answer("discover.cost", "Support exported 41 failed payouts.", observed(),
                                           expected_revision=offered.revision, turn_id="cost-observed")
        self.assertEqual(accepted.status, "accepted")
        record = conductor.state()["banks"]["discover"]["answers"]["discover.cost"]
        # The record names the question's minimum; its evidence keeps the class supplied.
        self.assertEqual((record["evidence_class"], record["evidence"]["class"]),
                         ("artifact", "observed_behavior"))
        self.assertEqual(conductor.next_turn().status, "blocked")
        store.close()

    def test_evidence_weaker_than_the_question_asks_is_refused_and_the_question_stays(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        refused = conductor.submit_answer("discover.person", "Mina exported the failures.", artifact(),
                                          expected_revision=first.revision, turn_id="person-artifact")
        self.assertEqual((refused.status, refused.message),
                         ("challenge", "evidence class must be observed_behavior or stronger"))
        self.assertEqual(conductor.next_turn().question.id, "discover.person")
        store.close()

    def test_the_fields_checked_are_those_of_the_class_supplied(self) -> None:
        store, conductor = self.opening()
        offered = self.cost_offered(conductor)
        undated = observed()
        del undated["date"]
        refused = conductor.submit_answer("discover.cost", "Support exported 41 failed payouts.", undated,
                                          expected_revision=offered.revision, turn_id="cost-undated")
        self.assertEqual((refused.status, refused.message), ("challenge", "missing evidence fields: date"))
        store.close()

    def test_an_unknown_or_missing_evidence_class_is_refused(self) -> None:
        store, conductor = self.opening()
        revision = self.cost_offered(conductor).revision
        unknown = dict(artifact(), **{"class": "rumor"})
        missing = {key: value for key, value in artifact().items() if key != "class"}
        for label, evidence in (("unknown", unknown), ("missing", missing)):
            with self.subTest(label=label):
                refused = conductor.submit_answer("discover.cost", "Support exported 41 failed payouts.", evidence,
                                                  expected_revision=revision, turn_id="cost-" + label)
                self.assertEqual((refused.status, refused.message),
                                 ("challenge", "evidence class must be artifact or stronger"))
                revision = refused.revision
        store.close()

    def test_the_shipped_contract_loads_six_banks_in_loop_order(self) -> None:
        contract = load_contract()
        self.assertEqual((contract["schema"], len(contract["banks"])), (1, 6))
        banks = shipped_banks()
        self.assertEqual([bank.id for bank in banks],
                         ["discover", "define", "design", "build", "deliver", "operate"])
        self.assertEqual([bank.version for bank in banks],
                         [bank["version"] for bank in contract["banks"]])
        first = banks[0].questions[0]
        self.assertEqual((first.id, first.prompt), ("DISCOVER-1", contract["banks"][0]["questions"][0]["ask"]))
        for bank in banks:
            self.assertEqual(bank.gate_approvers, ("local-reviewer",))
            for question in bank.questions:
                self.assertIsInstance(question.required_evidence, EvidenceClass)

    def test_shipped_definition_hashes_are_stable(self) -> None:
        self.assertEqual([bank.definition_hash for bank in shipped_banks()],
                         [bank.definition_hash for bank in shipped_banks()])

    def test_the_legacy_onboarding_bank_keeps_its_definition_hash(self) -> None:
        # The hash of the one bank pmos/cli.py builds today. Saved state pins it,
        # so a product that started on that bank would be refused on any other.
        self.assertEqual(LEGACY_ONBOARDING[0].definition_hash,
                         "06f90a11b758a58ac0d2c0f2022deb8244c1009a73a4139a6f528a73b5958dfa")

    def test_a_contract_file_that_cannot_be_used_is_a_validation_error(self) -> None:
        good = load_contract()
        payloads = {
            "missing": None,
            "not UTF-8": b"\xff\xfe",
            "not JSON": b"{",
            "not an object": b"[]",
            "schema 2": json.dumps(dict(good, schema=2)).encode("utf-8"),
            "no banks": json.dumps(dict(good, banks=[])).encode("utf-8"),
        }
        with TemporaryDirectory() as temp:
            for label, payload in payloads.items():
                with self.subTest(label=label):
                    path = Path(temp) / (label.replace(" ", "-") + ".json")
                    if payload is not None:
                        path.write_bytes(payload)
                    with self.assertRaises(ValidationError):
                        load_contract(path)

    def test_a_malformed_bank_is_a_validation_error(self) -> None:
        bank = load_contract()["banks"][0]
        question = bank["questions"][0]
        broken = {
            "no version": {key: value for key, value in bank.items() if key != "version"},
            "questions that are not a list": dict(bank, questions=7),
            "an unknown evidence class": dict(bank, questions=[dict(question, evidence_class="rumor")]),
            "an empty ask": dict(bank, questions=[dict(question, ask="")]),
        }
        for label, value in broken.items():
            with self.subTest(label=label):
                with self.assertRaises(ValidationError):
                    banks_from_contract({"schema": 1, "banks": [value]})

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
        env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent))))
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
        self.assertEqual(conductor.next_turn().question.id, "discover.person")
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 0)
        two = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                      expected_revision=one.revision, turn_id="bad-2")
        self.assertEqual((two.status, two.challenge_count), ("challenge", 2))
        self.assertEqual(conductor.next_turn().question.id, "discover.person")
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 0)
        three = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                        expected_revision=two.revision, turn_id="bad-3")
        self.assertEqual((three.status, three.challenge_count), ("parked", 2))
        # The cap holds: a parked question is no longer the offered question.
        four = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                       expected_revision=three.revision, turn_id="bad-4")
        self.assertEqual(four.status, "conflict")
        self.assertEqual(conductor.state()["banks"]["discover"]["challenges"]["discover.person"], 2)
        store.close()

    def test_park_is_preceded_by_exactly_two_challenges(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        invalid = {"class": "observed_behavior", "source": "heard it"}
        revision = turn.revision
        statuses = []
        for index in range(3):
            outcome = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                              expected_revision=revision, turn_id="cap-%d" % index)
            statuses.append((outcome.status, outcome.challenge_count))
            revision = outcome.revision
        self.assertEqual(statuses, [("challenge", 1), ("challenge", 2), ("parked", 2)])
        store.close()

    def test_parked_question_advances_the_cursor_and_only_blocks_the_gate(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        invalid = {"class": "observed_behavior", "source": "heard it"}
        one = conductor.submit_answer("discover.person", "Mina mentioned it once.", invalid,
                                      expected_revision=turn.revision, turn_id="park-1")
        self.assertEqual((one.status, one.challenge_count), ("challenge", 1))
        two = conductor.submit_answer("discover.person", "Still only hearsay.", invalid,
                                      expected_revision=one.revision, turn_id="park-2")
        self.assertEqual((two.status, two.challenge_count), ("challenge", 2))
        three = conductor.submit_answer("discover.person", "Still only hearsay.", invalid,
                                        expected_revision=two.revision, turn_id="park-3")
        self.assertEqual((three.status, three.challenge_count), ("parked", 2))
        offered = conductor.next_turn()
        self.assertEqual((offered.status, offered.question.id), ("question", "discover.cost"))
        accepted = conductor.submit_answer("discover.cost", "The export reports the weekly cost.",
                                           artifact(), expected_revision=offered.revision,
                                           turn_id="park-4")
        self.assertEqual(accepted.status, "accepted")
        saved = conductor.state()["banks"]["discover"]
        self.assertEqual((saved["cursor"], saved["parked"]), (2, ["discover.person"]))
        self.assertTrue(saved["answers"]["discover.person"]["parked"])
        self.assertEqual(saved["answers"]["discover.person"]["answer"], "Still only hearsay.")
        refused = conductor.prove_gate("discover", gate_proof(),
                                       expected_revision=accepted.revision, turn_id="park-gate")
        self.assertEqual(refused.status, "blocked")
        self.assertEqual(conductor.state()["gates"], {})
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

    def test_prove_gate_rejects_invalid_and_future_timestamps(self) -> None:
        store, conductor = self.opening()
        current = conductor.next_turn()
        a1 = conductor.submit_answer("discover.person", "Mina exported it.", observed(),
                                     expected_revision=current.revision, turn_id="ts-a1")
        current = conductor.next_turn()
        a2 = conductor.submit_answer("discover.cost", "Cost is in export.", artifact(),
                                     expected_revision=current.revision, turn_id="ts-a2")
        revision = a2.revision
        future = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        past = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        invalid_cases = [
            ("2026-99-99T99:99:99Z", "ts-impossible"),
            ("2026-02-30T10:00:00Z", "ts-feb30"),
            ("2026-09-03T00:00:00", "ts-no-tz"),
            ("2026-09-03T00:00:00+05:00", "ts-offset"),
            (future, "ts-future"),
        ]
        for approved_at, turn_id in invalid_cases:
            result = conductor.prove_gate("discover", gate_proof(approved_at=approved_at),
                                          expected_revision=revision, turn_id=turn_id)
            self.assertEqual(result.status, "blocked", approved_at)
            self.assertFalse(result.completed)
            revision = result.revision
        self.assertEqual(conductor.state()["gates"], {})
        self.assertEqual(conductor.state()["current_bank"], 0)
        valid = conductor.prove_gate("discover", gate_proof(approved_at=past),
                                    expected_revision=revision, turn_id="ts-valid")
        self.assertEqual(valid.status, "advanced")
        self.assertIn("discover", conductor.state()["gates"])
        store.close()

    def gated_discover(self) -> tuple[Conductor, Path]:
        """Gate the first bank against a real proof file, checked by hash the way the CLI checks it."""
        root = Path(self.temp.name)
        proof = root / "gate-1.md"
        proof.write_bytes(GATE_BYTES)

        def verifier(source: str, digest: str) -> bool:
            path = root / source
            return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest

        conductor = Conductor(Store(self.path), "payments", BANKS, gate_source_verifier=verifier)
        turn = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=turn.revision, turn_id="f06-a1")
        turn = conductor.next_turn()
        conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                expected_revision=turn.revision, turn_id="f06-a2")
        turn = conductor.next_turn()
        gated = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="f06-g1")
        self.assertEqual(gated.status, "advanced")
        return conductor, proof

    def test_changed_gate_proof_makes_the_bank_stale(self) -> None:
        conductor, proof = self.gated_discover()
        self.assertEqual(conductor.next_turn().question.id, "define.sponsor")
        proof.write_bytes(b"changed after approval\n")
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        self.assertIn("gate-1.md", stale.message)
        conductor.store.close()

    def test_removed_gate_proof_makes_the_bank_stale(self) -> None:
        conductor, proof = self.gated_discover()
        proof.unlink()
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        conductor.store.close()

    def test_answers_are_refused_while_an_approval_is_stale(self) -> None:
        conductor, proof = self.gated_discover()
        proof.write_bytes(b"changed after approval\n")
        turn = conductor.next_turn()
        refused = conductor.submit_answer("define.sponsor", "Mina approved scope.", commitment(),
                                          expected_revision=turn.revision, turn_id="f06-a3")
        self.assertEqual((refused.status, refused.bank_id), ("stale", "discover"))
        self.assertEqual(conductor.state()["banks"]["define"]["answers"], {})
        conductor.store.close()

    def test_a_later_bank_cannot_be_gated_on_a_stale_approval(self) -> None:
        conductor, proof = self.gated_discover()
        turn = conductor.next_turn()
        accepted = conductor.submit_answer("define.sponsor", "Mina approved scope.", commitment(),
                                           expected_revision=turn.revision, turn_id="f06-a3")
        self.assertEqual(accepted.status, "accepted")
        second = Path(self.temp.name) / "gate-2.md"
        second.write_bytes(b"define approval\n")
        proof.write_bytes(b"changed after approval\n")
        turn = conductor.next_turn()
        refused = conductor.prove_gate("define", gate_proof(source="gate-2.md",
                                                            source_hash=hashlib.sha256(b"define approval\n").hexdigest()),
                                       expected_revision=turn.revision, turn_id="f06-g2")
        self.assertEqual((refused.status, refused.bank_id), ("stale", "discover"))
        state = conductor.state()
        self.assertEqual(state["current_bank"], 1)
        self.assertNotIn("define", state["gates"])
        conductor.store.close()

    def test_reproving_a_stale_bank_restores_it_and_keeps_the_superseded_approval(self) -> None:
        conductor, proof = self.gated_discover()
        proof.write_bytes(b"revised approval\n")
        turn = conductor.next_turn()
        self.assertEqual(turn.status, "stale")
        malformed = conductor.prove_gate("discover", {"source": "gate-1.md"},
                                         expected_revision=turn.revision, turn_id="f06-bad")
        self.assertEqual(malformed.status, "blocked")
        self.assertNotIn("superseded_gates", conductor.state())
        new_hash = hashlib.sha256(b"revised approval\n").hexdigest()
        turn = conductor.next_turn()
        reproved = conductor.prove_gate("discover", gate_proof(source_hash=new_hash),
                                        expected_revision=turn.revision, turn_id="f06-g1-again")
        self.assertEqual(reproved.status, "advanced")
        self.assertEqual(conductor.next_turn().question.id, "define.sponsor")
        state = conductor.state()
        self.assertEqual(state["current_bank"], 1)
        self.assertEqual(state["gates"]["discover"]["proof"]["source_sha256"], new_hash)
        (archived,) = state["superseded_gates"]["discover"]
        self.assertEqual(archived["proof"]["source_sha256"], GATE_HASH)
        self.assertEqual(archived["reason"], "superseded after proof changed")
        self.assertRegex(archived["superseded_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        conductor.store.close()

    def test_an_unchanged_proof_stays_completed(self) -> None:
        conductor, proof = self.gated_discover()
        turn = conductor.next_turn()
        conductor.submit_answer("define.sponsor", "Mina approved scope.", commitment(),
                                expected_revision=turn.revision, turn_id="f06-a3")
        turn = conductor.next_turn()
        done = conductor.prove_gate("define", gate_proof(), expected_revision=turn.revision, turn_id="f06-g2")
        self.assertEqual(done.status, "completed")
        self.assertEqual(conductor.next_turn().status, "completed")
        self.assertNotIn("superseded_gates", conductor.state())
        conductor.store.close()

    def test_without_a_verifier_recorded_proof_is_not_rechecked(self) -> None:
        conductor, proof = self.gated_discover()
        conductor.store.close()
        proof.write_bytes(b"changed after approval\n")
        store = Store(self.path)
        unverified = Conductor(store, "payments", BANKS)
        self.assertEqual(unverified.next_turn().question.id, "define.sponsor")
        store.close()

    def test_a_replayed_gate_turn_returns_its_recorded_outcome_while_stale(self) -> None:
        conductor, proof = self.gated_discover()
        proof.write_bytes(b"changed after approval\n")
        turn = conductor.next_turn()
        replay = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="f06-g1")
        self.assertEqual(replay.status, "advanced")
        self.assertNotIn("superseded_gates", conductor.state())
        conductor.store.close()

    def park(self, conductor: Conductor, revision: str, prefix: str) -> TurnOutcome:
        """Three insufficient answers to discover.person: challenge, challenge, parked."""
        invalid = {"class": "observed_behavior", "source": "heard it"}
        outcome = None
        for index in range(3):
            outcome = conductor.submit_answer("discover.person", "Still vague.", invalid,
                                              expected_revision=revision, turn_id="%s-%d" % (prefix, index))
            revision = outcome.revision
        self.assertEqual(outcome.status, "parked")
        return outcome

    def test_a_reopened_question_recovers_and_the_bank_reaches_its_gate(self) -> None:
        store, conductor = self.opening()
        parked = self.park(conductor, conductor.next_turn().revision, "recover")
        self.assertEqual(conductor.next_turn().question.id, "discover.cost")
        reopened = conductor.reopen("discover.person", expected_revision=parked.revision,
                                    turn_id="recover-reopen", reason="found the recording")
        self.assertEqual((reopened.status, reopened.question.id), ("reopened", "discover.person"))
        self.assertEqual(conductor.next_turn().question.id, "discover.person")
        accepted = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                           expected_revision=reopened.revision, turn_id="recover-good-1")
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(conductor.state()["banks"]["discover"]["cursor"], 1)
        turn = conductor.next_turn()
        self.assertEqual(turn.question.id, "discover.cost")
        accepted = conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                           expected_revision=turn.revision, turn_id="recover-good-2")
        gate = conductor.prove_gate("discover", gate_proof(), expected_revision=accepted.revision,
                                    turn_id="recover-gate")
        self.assertEqual(gate.status, "advanced")
        store.close()
        store, reloaded = self.opening()
        self.assertEqual(reloaded.next_turn().question.id, "define.sponsor")
        self.assertEqual(reloaded.state()["banks"]["discover"]["reopened"], [])
        store.close()

    def test_replaying_a_reopen_changes_nothing_twice(self) -> None:
        store, conductor = self.opening()
        parked = self.park(conductor, conductor.next_turn().revision, "idem")
        first = conductor.reopen("discover.person", expected_revision=parked.revision,
                                 turn_id="idem-reopen", reason="found the recording")
        replay = conductor.reopen("discover.person", expected_revision=first.revision,
                                  turn_id="idem-reopen", reason="found the recording")
        self.assertEqual((replay.status, replay.revision), (first.status, first.revision))
        events = conductor.state()["banks"]["discover"]["rejected"]["discover.person"]
        self.assertEqual([event["event"] for event in events].count("reopened"), 1)
        store.close()

    def test_a_reopen_with_a_stale_revision_conflicts(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        self.park(conductor, first.revision, "stale-rev")
        conflict = conductor.reopen("discover.person", expected_revision=first.revision,
                                    turn_id="stale-rev-reopen", reason="found the recording")
        self.assertEqual(conflict.status, "conflict")
        self.assertIn("discover.person", conductor.state()["banks"]["discover"]["parked"])
        store.close()

    def test_rejected_evidence_is_refused_after_a_reopen(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        for index in range(3):
            turn = conductor.submit_answer("discover.person", "Everyone needs it.", observed(),
                                           expected_revision=turn.revision, turn_id="fresh-%d" % index)
        self.assertEqual(turn.status, "parked")
        reopened = conductor.reopen("discover.person", expected_revision=turn.revision,
                                    turn_id="fresh-reopen", reason="rewrite the answer")
        same = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                       expected_revision=reopened.revision, turn_id="fresh-same")
        self.assertEqual(same.status, "challenge")
        self.assertIn("already rejected", same.message)
        different = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                            dict(observed(), location="replay/18"),
                                            expected_revision=same.revision, turn_id="fresh-new")
        self.assertEqual(different.status, "accepted")
        store.close()

    def test_only_a_parked_question_in_the_current_bank_can_be_reopened(self) -> None:
        store, conductor = self.opening()
        blocked = conductor.reopen("discover.person", expected_revision=conductor.next_turn().revision,
                                   turn_id="not-parked", reason="nothing to reopen")
        self.assertEqual(blocked.status, "blocked")
        self.assertIn("only a parked question", blocked.message)
        store.close()

    def test_the_rejected_history_is_kept_in_order(self) -> None:
        store, conductor = self.opening()
        parked = self.park(conductor, conductor.next_turn().revision, "hist")
        conductor.reopen("discover.person", expected_revision=parked.revision,
                         turn_id="hist-reopen", reason="found the recording")
        events = conductor.state()["banks"]["discover"]["rejected"]["discover.person"]
        self.assertEqual([event["event"] for event in events], ["challenged", "challenged", "parked", "reopened"])
        self.assertEqual(events[-1]["reason"], "found the recording")
        store.close()

    def test_a_reopen_is_refused_while_an_earlier_approval_is_stale(self) -> None:
        conductor, proof = self.gated_discover()
        turn = conductor.next_turn()
        invalid = {"class": "named_commitment", "source": "approval email"}
        for index in range(3):
            turn = conductor.submit_answer("define.sponsor", "Mina approved scope.", invalid,
                                           expected_revision=turn.revision, turn_id="stale-park-%d" % index)
        self.assertEqual(turn.status, "parked")
        proof.write_bytes(b"changed after approval\n")
        refused = conductor.reopen("define.sponsor", expected_revision=conductor.next_turn().revision,
                                   turn_id="stale-reopen", reason="found the email")
        self.assertEqual((refused.status, refused.bank_id), ("stale", "discover"))
        self.assertIn("define.sponsor", conductor.state()["banks"]["define"]["parked"])
        conductor.store.close()

    def test_the_fourth_reopen_of_one_question_is_blocked(self) -> None:
        store, conductor = self.opening()
        turn = self.park(conductor, conductor.next_turn().revision, "limit-0")
        statuses = []
        for cycle in range(1, 5):
            turn = conductor.reopen("discover.person", expected_revision=turn.revision,
                                    turn_id="limit-reopen-%d" % cycle, reason="another look")
            statuses.append(turn.status)
            if turn.status == "reopened":
                turn = self.park(conductor, turn.revision, "limit-%d" % cycle)
        self.assertEqual(statuses, ["reopened", "reopened", "reopened", "blocked"])
        self.assertIn("reopen limit", turn.message)
        store.close()

    def test_a_state_saved_before_reopen_existed_still_loads(self) -> None:
        store, conductor = self.opening()
        parked = self.park(conductor, conductor.next_turn().revision, "legacy")
        saved = json.loads(json.dumps(conductor.state()))
        for bank_state in saved["banks"].values():
            bank_state.pop("reopened", None)
            bank_state.pop("rejected", None)
        conductor._validate_state(saved)
        self.assertEqual(parked.status, "parked")
        store.close()

    def gated_both(self) -> tuple[Conductor, Path, Path]:
        """Gate discover and define, each against its own real proof file."""
        conductor, first = self.gated_discover()
        second = Path(self.temp.name) / "gate-2.md"
        second.write_bytes(b"define approval\n")
        turn = conductor.next_turn()
        conductor.submit_answer("define.sponsor", "Mina approved scope.", commitment(),
                                expected_revision=turn.revision, turn_id="f06-a3")
        turn = conductor.next_turn()
        done = conductor.prove_gate("define", gate_proof(source="gate-2.md",
                                                         source_hash=hashlib.sha256(second.read_bytes()).hexdigest()),
                                    expected_revision=turn.revision, turn_id="f06-g2")
        self.assertEqual(done.status, "completed")
        return conductor, first, second

    def test_reproving_one_of_two_stale_gates_does_not_complete_the_interview(self) -> None:
        conductor, first, second = self.gated_both()
        first.write_bytes(b"revised discover approval\n")
        second.write_bytes(b"revised define approval\n")
        self.assertEqual(conductor.next_turn().bank_id, "discover")
        reproved = conductor.prove_gate("discover", gate_proof(source_hash=hashlib.sha256(first.read_bytes()).hexdigest()),
                                        expected_revision=conductor.next_turn().revision, turn_id="f06-g1-again")
        self.assertEqual((reproved.status, reproved.bank_id, reproved.completed), ("stale", "define", False))
        self.assertIn("recorded again", reproved.message)
        position = conductor.next_turn()
        self.assertEqual((position.status, position.bank_id), ("stale", "define"))
        conductor.store.close()
        # The recorded re-proof and the remaining stale gate survive a restart.
        root = Path(self.temp.name)

        def verifier(source: str, digest: str) -> bool:
            path = root / source
            return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest

        resumed = Conductor(Store(self.path), "payments", BANKS, gate_source_verifier=verifier)
        position = resumed.next_turn()
        self.assertEqual((position.status, position.bank_id), ("stale", "define"))
        done = resumed.prove_gate("define", gate_proof(source="gate-2.md",
                                                       source_hash=hashlib.sha256(second.read_bytes()).hexdigest()),
                                  expected_revision=position.revision, turn_id="f06-g2-again")
        self.assertEqual((done.status, done.completed), ("completed", True))
        self.assertEqual(resumed.next_turn().status, "completed")
        superseded = resumed.state()["superseded_gates"]
        self.assertEqual((len(superseded["discover"]), len(superseded["define"])), (1, 1))
        resumed.store.close()

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

    def test_invalid_date_is_refused(self) -> None:
        store, conductor = self.opening()
        turn = conductor.next_turn()
        bad = {"class": "observed_behavior", "source": "session replay",
               "date": "banana", "location": "replay/17"}
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", bad,
                                         expected_revision=turn.revision, turn_id="bad-date")
        self.assertEqual(result.status, "challenge")
        store.close()

    def test_missing_local_source_refused_when_resolver_set(self) -> None:
        store = Store(self.path)
        conductor = Conductor(store, "payments", BANKS, source_resolver=lambda source: False)
        turn = conductor.next_turn()
        evidence = {"class": "observed_behavior", "source": "does-not-exist.txt",
                    "date": "2026-09-03", "location": "replay/17"}
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", evidence,
                                         expected_revision=turn.revision, turn_id="missing-src")
        self.assertEqual(result.status, "challenge")
        store.close()

    def test_https_source_accepted_as_supplied_unverified(self) -> None:
        store = Store(self.path)
        consulted: list[str] = []
        conductor = Conductor(store, "payments", BANKS,
                              source_resolver=lambda source: consulted.append(source) or False)
        turn = conductor.next_turn()
        evidence = {"class": "observed_behavior", "source": "https://example.com/replay.log",
                    "date": "2026-09-03", "location": "replay/17"}
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", evidence,
                                         expected_revision=turn.revision, turn_id="https-src")
        self.assertEqual(result.status, "accepted")
        saved = conductor.state()["banks"]["discover"]["answers"]["discover.person"]
        self.assertEqual(saved["verification"], "supplied_unverified")
        self.assertEqual(consulted, [])
        store.close()

    def test_resolvable_local_source_recorded_as_source_verified(self) -> None:
        store = Store(self.path)
        conductor = Conductor(store, "payments", BANKS,
                              source_resolver=lambda source: source == "does-not-exist.txt")
        turn = conductor.next_turn()
        evidence = {"class": "observed_behavior", "source": "does-not-exist.txt",
                    "date": "2026-09-03", "location": "replay/17"}
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", evidence,
                                         expected_revision=turn.revision, turn_id="local-src")
        self.assertEqual(result.status, "accepted")
        saved = conductor.state()["banks"]["discover"]["answers"]["discover.person"]
        self.assertEqual(saved["verification"], "source_verified")
        store.close()

    def test_no_resolver_still_behaves_as_before_apart_from_date_check(self) -> None:
        store = Store(self.path)
        conductor = Conductor(store, "payments", BANKS)
        turn = conductor.next_turn()
        evidence = {"class": "observed_behavior", "source": "does-not-exist.txt",
                    "date": "2026-09-03", "location": "replay/17"}
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", evidence,
                                         expected_revision=turn.revision, turn_id="no-resolver")
        self.assertEqual(result.status, "accepted")
        saved = conductor.state()["banks"]["discover"]["answers"]["discover.person"]
        self.assertEqual(saved["verification"], "supplied_unverified")
        store.close()

    def test_iso_dates_and_datetimes_parse_and_malformed_dates_refuse(self) -> None:
        cases = {"2026-09-03": "accepted", "2026-09-03T10:00:00Z": "accepted",
                 "2026-09-03T10:00:00+05:00": "accepted", "2026-02-30": "challenge",
                 "03/09/2026": "challenge", "2026-13-01": "challenge"}
        for index, (date, expected) in enumerate(cases.items()):
            with self.subTest(date=date):
                store = Store(Path(self.temp.name) / ("dates-%d.sqlite" % index))
                conductor = Conductor(store, "payments", BANKS)
                turn = conductor.next_turn()
                result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                                 dict(observed(), date=date),
                                                 expected_revision=turn.revision, turn_id="date-%d" % index)
                self.assertEqual(result.status, expected)
                store.close()

    def test_malformed_optional_date_refuses_any_evidence_class(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=first.revision, turn_id="person")
        second = conductor.next_turn()
        result = conductor.submit_answer("discover.cost", "Support exported 41 failed payouts.",
                                         dict(artifact(), date="banana"),
                                         expected_revision=second.revision, turn_id="cost-bad-date")
        self.assertEqual(result.status, "challenge")
        self.assertIn("date", result.message)
        store.close()

    def test_every_non_web_source_goes_to_the_resolver(self) -> None:
        for index, source in enumerate(("C:\\notes\\replay.txt", "notes:replay", "file:///tmp/replay.txt")):
            with self.subTest(source=source):
                consulted: list[str] = []
                store = Store(Path(self.temp.name) / ("sources-%d.sqlite" % index))
                conductor = Conductor(store, "payments", BANKS,
                                      source_resolver=lambda value: consulted.append(value) or False)
                turn = conductor.next_turn()
                result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                                 dict(observed(), source=source),
                                                 expected_revision=turn.revision, turn_id="source-%d" % index)
                self.assertEqual(result.status, "challenge")
                self.assertEqual(consulted, [source])
                store.close()

    def test_resolver_that_cannot_check_a_source_leaves_it_unverified(self) -> None:
        store = Store(self.path)
        conductor = Conductor(store, "payments", BANKS, source_resolver=lambda source: None)
        turn = conductor.next_turn()
        result = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=turn.revision, turn_id="unchecked")
        self.assertEqual(result.status, "accepted")
        saved = conductor.state()["banks"]["discover"]["answers"]["discover.person"]
        self.assertEqual(saved["verification"], "supplied_unverified")
        store.close()

    def test_resolver_error_or_non_boolean_answer_refuses(self) -> None:
        def broken(source: str) -> bool:
            raise OSError("disk unavailable")
        for index, resolver in enumerate((broken, lambda source: "yes", lambda source: 1)):
            with self.subTest(index=index):
                store = Store(Path(self.temp.name) / ("resolver-%d.sqlite" % index))
                conductor = Conductor(store, "payments", BANKS, source_resolver=resolver)
                turn = conductor.next_turn()
                result = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                                 expected_revision=turn.revision, turn_id="broken-%d" % index)
                self.assertEqual(result.status, "challenge")
                store.close()

    def test_parked_answer_is_labelled_failed_validation(self) -> None:
        store, conductor = self.opening()
        bad = dict(observed(), date="banana")
        statuses = []
        for attempt in range(3):
            turn = conductor.next_turn()
            statuses.append(conductor.submit_answer("discover.person", "Mina exported the failures.", bad,
                                                    expected_revision=turn.revision,
                                                    turn_id="park-%d" % attempt).status)
        self.assertEqual(statuses, ["challenge", "challenge", "parked"])
        saved = conductor.state()["banks"]["discover"]["answers"]["discover.person"]
        self.assertEqual(saved["verification"], "failed_validation")
        store.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
