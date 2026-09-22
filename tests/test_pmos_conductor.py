"""Executable contract for the persistent deterministic Conductor."""

from __future__ import annotations

import os
import hashlib
import stat
import threading
import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.conductor import (EXCERPT_STEMS, MIN_EXCERPT_WORDS, STATE_PATH, Conductor, EvidenceClass, Question,
                            QuestionBank, TurnOutcome, canonical_json, evidence_counts)
import pmos.product as product_module
from pmos.product import document_reader, local_gate_verifier, product_conductor, source_resolver
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
        # The refusal names the class's whole field list, not only what is absent: that list
        # lives in pmos/conductor.py and in no document the quickstart reaches, so a reader
        # who saw one field name had to open the source to learn what it sat beside.
        self.assertEqual(
            (refused.status, refused.message),
            ("challenge",
             "missing evidence fields: date (observed_behavior evidence needs source, date, location)"))
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

    def test_recorded_gate_proof_returns_accepted_true(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=first.revision, turn_id="turn-1")
        second = conductor.next_turn()
        conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                expected_revision=second.revision, turn_id="turn-2")
        blocked = conductor.next_turn()
        self.assertEqual(blocked.status, "blocked")
        outcome = conductor.prove_gate("discover", gate_proof(),
                                       expected_revision=blocked.revision, turn_id="gate-1")
        self.assertEqual(outcome.status, "advanced")
        self.assertTrue(outcome.accepted)
        self.assertEqual(outcome.message, "gate proof recorded")
        store.close()

    def test_unauthorized_actor_message_names_pinned_approvers(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=first.revision, turn_id="turn-1")
        second = conductor.next_turn()
        conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                expected_revision=second.revision, turn_id="turn-2")
        blocked = conductor.next_turn()
        self.assertEqual(blocked.status, "blocked")
        unauth_proof = dict(gate_proof(), actor_id="unknown-actor")
        outcome = conductor.prove_gate("discover", unauth_proof,
                                       expected_revision=blocked.revision, turn_id="gate-unauth")
        self.assertEqual(outcome.status, "blocked")
        self.assertIn("gate actor is not authorized by the pinned question bank; its approvers are: asha", outcome.message)
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
        self.assertIn("manifest", archived)
        self.assertIn("manifest_sha256", archived)
        self.assertEqual(archived["attestation"], "local")
        self.assertEqual(archived["reason"], "superseded after proof changed")
        self.assertRegex(archived["superseded_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        conductor.store.close()

    def _manifested(self, *, changed=None, reconcile=None, manifest=None):
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        fixed_manifest = manifest if manifest is not None else {"artifacts": [], "dependencies": []}
        result = {"changed": changed or [], "reconcile": reconcile or []}

        def manifest_builder(bank_id):
            return fixed_manifest

        def manifest_checker(manifest):
            self.assertEqual(manifest, fixed_manifest)
            return result

        return store, Conductor(store, "payments", BANKS,
                                gate_source_verifier=verifier,
                                gate_manifest=manifest_builder,
                                manifest_verifier=manifest_checker), result

    def _gate_two_answers(self, conductor: Conductor) -> TurnOutcome:
        turn = conductor.next_turn()
        conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                expected_revision=turn.revision, turn_id="m-a1")
        turn = conductor.next_turn()
        conductor.submit_answer("discover.cost", "The export reports the weekly cost.", artifact(),
                                expected_revision=turn.revision, turn_id="m-a2")
        return conductor.next_turn()

    def test_approved_gate_stores_manifest_hash_and_local_attestation(self) -> None:
        store, conductor, _ = self._manifested(manifest={"artifacts": [
            {"id": "spec", "path": "spec.md", "revision": "rev-1234567890abcdef", "depends_on": []}],
            "dependencies": []})
        turn = self._gate_two_answers(conductor)
        approved = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="m-g1")
        self.assertEqual(approved.status, "advanced")
        gate = conductor.state()["gates"]["discover"]
        self.assertEqual(set(gate), {"proof", "proof_sha256", "manifest", "manifest_sha256", "attestation", "contract_sha256"})
        self.assertEqual(gate["manifest"]["artifacts"][0]["id"], "spec")
        self.assertEqual(gate["manifest_sha256"], hashlib.sha256(canonical_json(gate["manifest"])).hexdigest())
        self.assertEqual(gate["attestation"], "local")
        reloaded = Conductor(store, "payments", BANKS, gate_source_verifier=lambda *a: True)
        self.assertEqual(reloaded.state()["gates"]["discover"]["manifest_sha256"], gate["manifest_sha256"])
        store.close()

    def test_manifest_change_makes_next_turn_stale(self) -> None:
        store, conductor, result = self._manifested(changed=[
            {"id": "spec", "reviewed": "rev-aaaabbbbccccdddd", "current": "rev-eeeeffff111122223"}],
            reconcile=["dep-1"])
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="mc-g1")
        stale = conductor.next_turn()
        self.assertEqual(stale.status, "stale")
        self.assertEqual(stale.bank_id, "discover")
        self.assertIn("spec (reviewed rev-aaaa, now rev-eeee)", stale.message)
        self.assertIn("needs reconciliation: dep-1", stale.message)
        self.assertTrue(stale.message.endswith("; prove the gate again"))
        store.close()

    def test_manifest_change_with_missing_revision_reports_missing(self) -> None:
        store, conductor, result = self._manifested(changed=[
            {"id": "spec", "reviewed": "rev-aaaabbbbccccdddd", "current": None}])
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="miss-g1")
        stale = conductor.next_turn()
        self.assertEqual(stale.status, "stale")
        self.assertIn("spec (reviewed rev-aaaa, now missing)", stale.message)
        store.close()

    def _content_aware_conductor(self, current: dict[str, str]):
        # Like pmos/artifacts.py: the builder binds each artifact's revision when the gate is proved, and the
        # verifier reports the entries whose recorded revision no longer matches, plus the approved artifacts
        # that depend on one of them.
        def entry(aid, depends_on):
            return {"id": aid, "path": aid + ".md", "revision": current[aid], "depends_on": depends_on}

        def build(bank_id):
            if bank_id == "discover":
                return {"artifacts": [entry("spec", [])], "dependencies": []}
            return {"artifacts": [entry("prd", ["spec"])], "dependencies": [entry("spec", [])]}

        def check(manifest):
            entries = list(manifest["artifacts"]) + list(manifest["dependencies"])
            changed = [{"id": e["id"], "path": e["path"], "reviewed": e["revision"],
                        "current": current.get(e["id"])}
                       for e in entries if current.get(e["id"]) != e["revision"]]
            changed_ids = {c["id"] for c in changed}
            reconcile = sorted(e["id"] for e in manifest["artifacts"]
                               if e["id"] not in changed_ids
                               and any(dep in changed_ids for dep in e["depends_on"]))
            return {"changed": changed, "reconcile": reconcile}

        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        return store, Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                                gate_manifest=build, manifest_verifier=check)

    def _gate_both_banks(self, conductor: Conductor) -> TurnOutcome:
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="gb-g1")
        turn = conductor.next_turn()
        self.assertEqual(turn.question.id, "define.sponsor")
        conductor.submit_answer("define.sponsor", "Mina committed.", commitment(),
                                expected_revision=turn.revision, turn_id="gb-d1")
        turn = conductor.next_turn()
        conductor.prove_gate("define", gate_proof(), expected_revision=turn.revision, turn_id="gb-g2")
        return conductor.next_turn()

    def test_stale_gates_lists_every_affected_approval(self) -> None:
        current = {"spec": "a" * 64, "prd": "c" * 64}
        store, conductor = self._content_aware_conductor(current)
        self._gate_both_banks(conductor)
        self.assertEqual(conductor.stale_gates(), [])
        current["spec"] = "b" * 64
        gates = conductor.stale_gates()
        self.assertEqual([g["bank_id"] for g in gates], ["discover", "define"])
        for gate in gates:
            self.assertEqual(gate["changed"], [{"id": "spec", "path": "spec.md",
                                                "reviewed": "a" * 64, "current": "b" * 64}])
            self.assertEqual(gate["reconcile"], ["prd"] if gate["bank_id"] == "define" else [])
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        self.assertEqual(stale.message, conductor.stale_gates()[0]["message"])
        # Re-proving discover binds the changed spec, but define's approval still binds the old one, so the
        # re-proof is recorded and the interview stays stale on define.
        reproved = conductor.prove_gate("discover", gate_proof(), expected_revision=stale.revision,
                                        turn_id="sg-reprove")
        self.assertEqual((reproved.status, reproved.bank_id), ("stale", "define"))
        self.assertTrue(reproved.message.startswith("gate proof for discover recorded again; "
                                                    "approved artifacts for define changed: spec"), reproved.message)
        self.assertEqual(conductor.state()["gates"]["discover"]["manifest"]["artifacts"][0]["revision"], "b" * 64)
        remaining = conductor.stale_gates()
        self.assertEqual([g["bank_id"] for g in remaining], ["define"])
        self.assertEqual(remaining[0]["reconcile"], ["prd"])
        store.close()

    def test_stale_gates_empty_when_unchanged_and_without_verifier(self) -> None:
        current = {"spec": "a" * 64, "prd": "c" * 64}
        store, conductor = self._content_aware_conductor(current)
        self._gate_both_banks(conductor)
        self.assertEqual(conductor.stale_gates(), [])
        current["spec"] = "b" * 64
        store.close()
        bare = Store(self.path)
        bare_conductor = Conductor(bare, "payments", BANKS)
        self.assertEqual(bare_conductor.stale_gates(), [])
        bare.close()

    def test_manifest_verifier_validation_error_message(self) -> None:
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH

        def checker(manifest):
            raise ValidationError("x.md is a symlink")

        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                              gate_manifest=lambda bank_id: {"artifacts": [], "dependencies": []},
                              manifest_verifier=checker)
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="ve-g1")
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        self.assertEqual(stale.message, "approved artifacts for discover could not be checked: x.md is a symlink")
        store.close()

    def test_manifest_verifier_runtime_error_message(self) -> None:
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH

        def checker(manifest):
            raise RuntimeError("boom")

        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                              gate_manifest=lambda bank_id: {"artifacts": [], "dependencies": []},
                              manifest_verifier=checker)
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="re-g1")
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        self.assertEqual(stale.message, "approved artifacts for discover could not be checked; prove the gate again")
        store.close()

    def test_reproving_keeps_superseded_manifest_and_question_position(self) -> None:
        # A stub workspace that behaves like pmos/artifacts.py: the builder binds each artifact's current
        # revision, and the verifier reports the entries whose recorded revision no longer matches.
        current = {"spec": "a" * 64}

        def build(bank_id):
            return {"artifacts": [{"id": aid, "path": aid + ".md", "revision": rev, "depends_on": []}
                                  for aid, rev in sorted(current.items())], "dependencies": []}

        def check(manifest):
            changed = [{"id": entry["id"], "path": entry["path"], "reviewed": entry["revision"],
                        "current": current.get(entry["id"])}
                       for entry in manifest["artifacts"] if current.get(entry["id"]) != entry["revision"]]
            return {"changed": changed, "reconcile": []}

        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                              gate_manifest=build, manifest_verifier=check)
        turn = self._gate_two_answers(conductor)
        first = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="re-g1")
        self.assertEqual(first.status, "advanced")
        self.assertEqual(conductor.next_turn().question.id, "define.sponsor")
        current["spec"] = "b" * 64  # an approved artifact changes, so its gate is stale
        stale = conductor.next_turn()
        self.assertEqual((stale.status, stale.bank_id), ("stale", "discover"))
        self.assertIn("spec (reviewed aaaaaaaa, now bbbbbbbb)", stale.message)
        reproved = conductor.prove_gate("discover", gate_proof(), expected_revision=stale.revision,
                                        turn_id="re-g1-again")
        self.assertEqual(reproved.status, "advanced")
        state = conductor.state()
        self.assertEqual(state["gates"]["discover"]["manifest"]["artifacts"][0]["revision"], "b" * 64)
        (archived,) = state["superseded_gates"]["discover"]
        self.assertEqual(archived["manifest"]["artifacts"][0]["revision"], "a" * 64)
        self.assertEqual(set(archived), {"proof", "proof_sha256", "manifest", "manifest_sha256",
                                         "attestation", "contract_sha256", "reason", "superseded_at"})
        self.assertEqual(state["current_bank"], 1)
        self.assertEqual(conductor.next_turn().question.id, "define.sponsor")
        store.close()

    def test_rejection_is_recorded_and_does_not_advance(self) -> None:
        store, conductor, _ = self._manifested()
        turn = self._gate_two_answers(conductor)
        self.assertEqual(conductor.state()["current_bank"], 0)
        rejected = conductor.prove_gate("discover", dict(gate_proof(), decision="rejected"),
                                        expected_revision=turn.revision, turn_id="rj-g1")
        self.assertEqual(rejected.status, "rejected")
        self.assertEqual(rejected.bank_id, "discover")
        self.assertIn("gate rejected by asha", rejected.message)
        self.assertEqual(conductor.state()["current_bank"], 0)
        self.assertNotIn("discover", conductor.state()["gates"])
        rejections = conductor.state()["gate_rejections"]["discover"]
        (one,) = rejections
        self.assertEqual(set(one), {"proof", "proof_sha256", "manifest", "manifest_sha256",
                                   "attestation", "rejected_at"})
        self.assertEqual(one["proof"]["decision"], "rejected")
        self.assertEqual(one["attestation"], "local")
        self.assertRegex(one["rejected_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        approved = conductor.prove_gate("discover", gate_proof(),
                                        expected_revision=rejected.revision, turn_id="rj-g2")
        self.assertEqual(approved.status, "advanced")
        self.assertEqual(conductor.state()["current_bank"], 1)
        store.close()

    def test_builder_validation_error_blocks_and_records_no_gate(self) -> None:
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH

        def builder(bank_id):
            raise ValidationError("manifest service is down")

        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                              gate_manifest=builder)
        turn = self._gate_two_answers(conductor)
        blocked = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="bv-g1")
        self.assertEqual(blocked.status, "blocked")
        self.assertEqual(blocked.message, "manifest service is down")
        self.assertNotIn("discover", conductor.state().get("gates", {}))
        self.assertNotIn("discover", conductor.state().get("gate_rejections", {}))
        store.close()

    def test_malformed_manifest_blocks_gate(self) -> None:
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                              gate_manifest=lambda bank_id: {"artifacts": "nope", "dependencies": []})
        turn = self._gate_two_answers(conductor)
        blocked = conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="mm-g1")
        self.assertEqual(blocked.status, "blocked")
        self.assertIn("manifest", blocked.message)
        store.close()

    def test_old_two_key_gate_record_still_loads(self) -> None:
        # A product that passed a gate before manifests holds {proof, proof_sha256} only; it must still load.
        store = Store(self.path)
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        conductor = Conductor(store, "payments", BANKS, gate_source_verifier=verifier)
        turn = self._gate_two_answers(conductor)
        conductor.prove_gate("discover", gate_proof(), expected_revision=turn.revision, turn_id="ok-g1")
        snapshot = store.read_snapshot("payments")
        state = json.loads(snapshot.files[STATE_PATH])
        proof = state["gates"]["discover"]["proof"]
        state["gates"]["discover"] = {"proof": proof,
                                      "proof_sha256": hashlib.sha256(canonical_json(proof)).hexdigest()}
        files = dict(snapshot.files)
        files[STATE_PATH] = canonical_json(state)
        self.assertTrue(store.commit("payments", files, expected_revision=snapshot.head,
                                     metadata={"reason": "a gate recorded before manifests"}).committed)
        loaded = Conductor(store, "payments", BANKS, gate_source_verifier=verifier,
                           manifest_verifier=lambda manifest: self.fail("an old record has no manifest"))
        self.assertEqual(set(loaded.state()["gates"]["discover"]), {"proof", "proof_sha256"})
        self.assertEqual(loaded.next_turn().question.id, "define.sponsor")
        store.close()

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
                 "03/09/2026": "challenge", "2026-13-01": "challenge",
                 "2099-01-01": "challenge",
                 "2099-01-01T00:00:00Z": "challenge"}
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
        store = Store(Path(self.temp.name) / "dates-future.sqlite")
        conductor = Conductor(store, "payments", BANKS)
        turn = conductor.next_turn()
        future = (datetime.now(timezone.utc) + timedelta(days=4000)).strftime("%Y-%m-%dT%H:%M:%SZ")
        result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                         dict(observed(), date=future),
                                         expected_revision=turn.revision, turn_id="date-future-dt")
        self.assertEqual(result.status, "challenge")
        self.assertEqual(result.message, "evidence date is in the future")
        store.close()
        store = Store(Path(self.temp.name) / "dates-future-day.sqlite")
        conductor = Conductor(store, "payments", BANKS)
        turn = conductor.next_turn()
        result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                         dict(observed(), date="2099-01-01"),
                                         expected_revision=turn.revision, turn_id="date-future-day")
        self.assertEqual(result.status, "challenge")
        self.assertEqual(result.message, "evidence date is in the future")
        store.close()
        store = Store(Path(self.temp.name) / "dates-future-hour.sqlite")
        conductor = Conductor(store, "payments", BANKS)
        turn = conductor.next_turn()
        future_hour = (datetime.now(timezone.utc) + timedelta(days=2)).strftime("%Y-%m-%d %H")
        result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                         dict(observed(), date=future_hour),
                                         expected_revision=turn.revision, turn_id="date-future-hour")
        self.assertEqual(result.status, "challenge")
        self.assertEqual(result.message, "evidence date is in the future")
        store.close()
        store = Store(Path(self.temp.name) / "dates-past-hour.sqlite")
        conductor = Conductor(store, "payments", BANKS)
        turn = conductor.next_turn()
        past_hour = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d %H")
        result = conductor.submit_answer("discover.person", "Mina exported the failures.",
                                         dict(observed(), date=past_hour),
                                         expected_revision=turn.revision, turn_id="date-past-hour")
        self.assertEqual(result.status, "accepted")
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


# The interview notes a quotation is checked against. The sentence is wrapped
# across two lines with a doubled space, the way a pasted transcript arrives.
INTERVIEW = ("# Interview with Asha, 3 September\n\n"
             "Asha said: \"We re-key every failed payout batch by hand,\n"
             "  and it takes the  whole of Monday morning.\"\n")
GENUINE = "We re-key every failed payout batch by hand, and it takes the whole of Monday morning."
FABRICATED = "THIS SENTENCE IS NOWHERE IN THE FILE"


class QuotationTest(unittest.TestCase):
    """A supplied quotation is checked against its document, or the answer is refused."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name, "workspace")
        (self.root / "notes").mkdir(parents=True)
        (self.root / "notes" / "interview.md").write_text(INTERVIEW, encoding="utf-8")
        self.stores: list[Store] = []

    def tearDown(self) -> None:
        for store in self.stores:
            store.close()
        self.temp.cleanup()

    def store(self, name: str) -> Store:
        store = Store(Path(self.temp.name) / (name + ".sqlite"))
        self.stores.append(store)
        return store

    def conductor(self, name: str = "runtime", *, reader: bool = True,
                  banks=BANKS) -> Conductor:
        return Conductor(self.store(name), "payments", banks,
                         gate_source_verifier=local_gate_verifier(self.root),
                         source_resolver=source_resolver(self.root),
                         document_reader=document_reader(self.root) if reader else None)

    def submit(self, conductor: Conductor, evidence: dict, turn_id: str) -> TurnOutcome:
        turn = conductor.next_turn()
        return conductor.submit_answer("discover.person", "Mina exported the failures.", evidence,
                                       expected_revision=turn.revision, turn_id=turn_id)

    def quoted(self, value: str, *, field: str = "quote", source: str = "notes/interview.md") -> dict:
        return dict(observed(), source=source, **{field: value})

    def saved(self, conductor: Conductor) -> dict:
        return conductor.state()["banks"]["discover"]["answers"]["discover.person"]

    def test_a_quote_found_in_the_cited_file_is_accepted_and_recorded_quote_verified(self) -> None:
        conductor = self.conductor()
        result = self.submit(conductor, self.quoted(GENUINE), "genuine")
        self.assertEqual(result.status, "accepted")
        self.assertEqual(self.saved(conductor)["verification"], "quote_verified")
        self.assertEqual(self.saved(conductor)["evidence"]["quote"], GENUINE)

    def test_a_quote_absent_from_the_cited_file_is_refused_naming_the_file_and_the_quote(self) -> None:
        conductor = self.conductor()
        result = self.submit(conductor, self.quoted(FABRICATED), "fabricated")
        self.assertEqual(result.status, "challenge")
        self.assertIn("notes/interview.md", result.message)
        self.assertIn(FABRICATED, result.message)
        self.assertNotIn("discover.person", conductor.state()["banks"]["discover"]["answers"])

    def test_a_one_character_edit_to_a_passing_quote_is_refused(self) -> None:
        # The seeded defect: the passing quote with "Monday" misspelt. A check
        # that only looked for overlap, or compared case-insensitively on a
        # prefix, would let this through.
        edited = GENUINE.replace("Monday", "Munday")
        self.assertNotEqual(edited, GENUINE)
        conductor = self.conductor()
        result = self.submit(conductor, self.quoted(edited), "one-char")
        self.assertEqual(result.status, "challenge")
        self.assertIn("Munday", result.message)

    def test_excerpt_and_quotation_are_checked_exactly_like_quote(self) -> None:
        self.assertEqual(EXCERPT_STEMS, ("quote", "quotation", "excerpt", "verbatim"))
        for field in ("quote", "excerpt", "quotation"):
            with self.subTest(field=field):
                refused = self.submit(self.conductor("bad-" + field), self.quoted(FABRICATED, field=field),
                                      "bad-" + field)
                self.assertEqual(refused.status, "challenge")
                self.assertIn(field + " does not occur in notes/interview.md", refused.message)
                good = self.conductor("good-" + field)
                accepted = self.submit(good, self.quoted(GENUINE, field=field), "good-" + field)
                self.assertEqual(accepted.status, "accepted")
                self.assertEqual(self.saved(good)["verification"], "quote_verified")

    def test_a_differently_spelled_excerpt_key_is_checked_like_quote(self) -> None:
        # The bypass a literal field list left open: `Quote` or `quote_text`
        # carrying an invented sentence was stored beside source_verified.
        spellings = ("Quote", "QUOTE", "quote_text", "QuotedText", "sourceQuote", "Excerpt-1",
                     "verbatim", "verbatimQuote", "Quotation", "q.u.o.t.e", "ex-cerpt", "ex:cerpt")
        for index, field in enumerate(spellings):
            with self.subTest(field=field):
                refused = self.submit(self.conductor("spelt-bad-%d" % index),
                                      self.quoted(FABRICATED, field=field), "spelt-bad-%d" % index)
                self.assertEqual(refused.status, "challenge")
                self.assertIn(field + " does not occur in notes/interview.md", refused.message)
                good = self.conductor("spelt-good-%d" % index)
                accepted = self.submit(good, self.quoted(GENUINE, field=field), "spelt-good-%d" % index)
                self.assertEqual(accepted.status, "accepted")
                self.assertEqual(self.saved(good)["verification"], "quote_verified")

    def test_a_key_that_names_no_excerpt_is_not_checked(self) -> None:
        # The stated edge of the rule, pinned so the prose cannot drift past it:
        # a key without one of the EXCERPT_STEMS words is stored as supplied and
        # the answer keeps the label its source earned. `quota` is not `quote`.
        for index, field in enumerate(("said", "quota", "note")):
            with self.subTest(field=field):
                conductor = self.conductor("unchecked-%d" % index)
                result = self.submit(conductor, self.quoted(FABRICATED, field=field), "unchecked-%d" % index)
                self.assertEqual(result.status, "accepted")
                self.assertEqual(self.saved(conductor)["verification"], "source_verified")

    def test_a_blank_excerpt_field_is_not_a_quotation(self) -> None:
        # Evidence values are stripped, so `"quote": "  "` quotes nothing: it is
        # not checked and not refused, and the answer keeps its source's label.
        conductor = self.conductor()
        result = self.submit(conductor, self.quoted("   "), "blank")
        self.assertEqual(result.status, "accepted", result.message)
        self.assertEqual(self.saved(conductor)["verification"], "source_verified")

    def test_a_quotation_shorter_than_the_minimum_is_refused(self) -> None:
        # "e" occurs in the interview notes, and in nearly every document; it
        # must not earn quote_verified. The minimum counts words after the
        # whitespace collapse, and a quotation at the minimum is checked normally.
        self.assertEqual(MIN_EXCERPT_WORDS, 3)
        for index, (quote, expected) in enumerate((("e", "challenge"), ("payout batch", "challenge"),
                                                   ("every failed\n  payout", "accepted"))):
            with self.subTest(quote=quote):
                self.assertIn(" ".join(quote.split()), " ".join(INTERVIEW.split()))
                conductor = self.conductor("short-%d" % index)
                result = self.submit(conductor, self.quoted(quote), "short-%d" % index)
                self.assertEqual(result.status, expected)
                if expected == "challenge":
                    self.assertIn("quote is too short to check", result.message)
                else:
                    self.assertEqual(self.saved(conductor)["verification"], "quote_verified")

    def test_a_reader_that_raises_or_returns_no_text_refuses_the_quote(self) -> None:
        # A reader failure is a refusal, never a pass: a reader that raises, or
        # hands back something that is not text, leaves the quote unchecked.
        def raises(source: str) -> str:
            raise OSError("disk went away")
        readers = {"raises": raises, "none": lambda source: None,
                   "bytes": lambda source: INTERVIEW.encode("utf-8")}
        for name, reader in readers.items():
            with self.subTest(reader=name):
                conductor = Conductor(self.store("reader-" + name), "payments", BANKS,
                                      source_resolver=source_resolver(self.root), document_reader=reader)
                result = self.submit(conductor, self.quoted(GENUINE), "reader-" + name)
                self.assertEqual(result.status, "challenge")
                self.assertIn("could not be read to check the quotation", result.message)

    def test_a_document_reader_that_is_not_callable_is_refused_at_construction(self) -> None:
        with self.assertRaisesRegex(ValidationError, "document_reader must be callable"):
            Conductor(self.store("not-callable"), "payments", BANKS, document_reader="notes/interview.md")

    def test_the_document_reader_refuses_everything_outside_a_plain_workspace_file(self) -> None:
        # Each bound of the shared walk, pinned on the reader and on the gate
        # verifier, which read through the same helper.
        # Resolved, so no symlinked system directory (/var on macOS) on the way
        # refuses it for another reason and hides a missing absolute-path check.
        outside = Path(self.temp.name).resolve() / "outside.md"
        outside.write_text(INTERVIEW, encoding="utf-8")
        (self.root / ".pmos").mkdir()
        (self.root / ".pmos" / "notes.md").write_text(INTERVIEW, encoding="utf-8")
        (self.root / "back\\slash.md").write_text(INTERVIEW, encoding="utf-8")
        (self.root / "linked-dir").symlink_to(self.root / "notes", target_is_directory=True)
        (self.root / "notes" / "linked.md").symlink_to(self.root / "notes" / "interview.md")
        digest = hashlib.sha256(INTERVIEW.encode("utf-8")).hexdigest()
        read, verify = document_reader(self.root), local_gate_verifier(self.root)
        self.assertEqual(read("notes/interview.md"), INTERVIEW)
        self.assertTrue(verify("notes/interview.md", digest))
        refused = {
            "absolute": str(outside),
            "parent": "../outside.md",
            "pmos": ".pmos/notes.md",
            "backslash": "back\\slash.md",
            "symlinked directory": "linked-dir/interview.md",
            "symlinked file": "notes/linked.md",
            "directory": "notes",
            "empty": "",
        }
        for name, source in refused.items():
            with self.subTest(case=name):
                self.assertIsNone(read(source))
                self.assertFalse(verify(source, digest))
        self.assertIsNone(read(123))

    def test_the_gate_verifier_treats_an_unusable_expected_hash_as_a_mismatch(self) -> None:
        # compare_digest raises TypeError on a non-str hash or a non-ASCII str;
        # a direct library call must get False, not the exception.
        verify = local_gate_verifier(self.root)
        digest = hashlib.sha256(INTERVIEW.encode("utf-8")).hexdigest()
        self.assertTrue(verify("notes/interview.md", digest))
        for name, expected in {"none": None, "int": 7, "bytes": digest.encode("ascii"),
                               "non-ascii": "\u00e9" * 64}.items():
            with self.subTest(expected=name):
                self.assertIs(verify("notes/interview.md", expected), False)

    def test_a_file_that_is_not_regular_is_refused(self) -> None:
        # The regular-file check, pinned by a file that reports itself as a
        # character device: everything else about it would read normally.
        digest = hashlib.sha256(INTERVIEW.encode("utf-8")).hexdigest()
        read, verify = document_reader(self.root), local_gate_verifier(self.root)
        real_fstat = os.fstat

        def device(descriptor: int) -> os.stat_result:
            fields = list(real_fstat(descriptor))[:10]
            fields[0] = stat.S_IFCHR | 0o644
            return os.stat_result(fields)
        with patch.object(product_module.os, "fstat", device):
            self.assertIsNone(read("notes/interview.md"))
            self.assertFalse(verify("notes/interview.md", digest))

    def test_a_named_pipe_at_the_cited_path_is_refused_without_blocking(self) -> None:
        # Opening a FIFO for reading blocks until a writer appears; a planted
        # pipe must not hang `pmos answer` or `pmos gate`.
        if not hasattr(os, "mkfifo"):
            self.skipTest("no named pipes on this platform")
        pipe = self.root / "notes" / "pipe.md"
        os.mkfifo(pipe)
        results: dict[str, object] = {}

        def attempt() -> None:
            results["read"] = document_reader(self.root)("notes/pipe.md")
            results["verify"] = local_gate_verifier(self.root)("notes/pipe.md", "0" * 64)
        worker = threading.Thread(target=attempt, daemon=True)
        worker.start()
        worker.join(5)
        if worker.is_alive():
            for _ in range(2):  # release each blocked open before failing
                try:
                    os.close(os.open(pipe, os.O_WRONLY | os.O_NONBLOCK))
                except OSError:
                    pass
                worker.join(1)
            self.fail("opening a named pipe blocked")
        self.assertEqual(results, {"read": None, "verify": False})

    def test_the_size_ceiling_holds_on_open_and_during_the_read(self) -> None:
        # The ceiling is checked twice: on the size the file reports when it is
        # opened, and again on the bytes actually read, for a file that grows
        # after it was opened. Both are pinned for the reader and the verifier.
        digest = hashlib.sha256(INTERVIEW.encode("utf-8")).hexdigest()
        size = len(INTERVIEW.encode("utf-8"))
        read, verify = document_reader(self.root), local_gate_verifier(self.root)
        self.assertEqual(product_module.MAX_WORKSPACE_FILE_BYTES, 16 * 1024 * 1024)
        with patch.object(product_module, "MAX_WORKSPACE_FILE_BYTES", size):
            self.assertEqual(read("notes/interview.md"), INTERVIEW)
            self.assertTrue(verify("notes/interview.md", digest))
        with patch.object(product_module, "MAX_WORKSPACE_FILE_BYTES", size - 1):
            self.assertIsNone(read("notes/interview.md"))
            self.assertFalse(verify("notes/interview.md", digest))
            real_fstat = os.fstat

            def understated(descriptor: int) -> os.stat_result:
                fields = list(real_fstat(descriptor))[:10]
                fields[6] = 1
                return os.stat_result(fields)
            # Refused on the reported size alone, before a single byte is read.
            reads: list[int] = []
            real_read = os.read

            def counting(descriptor: int, length: int) -> bytes:
                reads.append(length)
                return real_read(descriptor, length)
            with patch.object(product_module.os, "read", counting):
                self.assertIsNone(read("notes/interview.md"))
                self.assertFalse(verify("notes/interview.md", digest))
            self.assertEqual(reads, [])
            # The file claims one byte on open, so only the read-time count can stop it.
            with patch.object(product_module.os, "fstat", understated):
                self.assertIsNone(read("notes/interview.md"))
                self.assertFalse(verify("notes/interview.md", digest))

    def test_a_legacy_product_gets_the_document_reader_too(self) -> None:
        # product_conductor has two branches; a product made before the pin runs
        # the legacy bank, and without the reader there every quote is refused.
        store = self.store("legacy")
        store.create_product("legacy")
        conductor = product_conductor(store, self.root, "legacy")
        turn = conductor.next_turn()
        self.assertEqual(turn.status, "question")
        result = conductor.submit_answer(turn.question.id, "Mina exported the failures.", self.quoted(GENUINE),
                                         expected_revision=turn.revision, turn_id="legacy-quote")
        self.assertEqual(result.status, "accepted", result.message)
        bank = conductor.state()["banks"][turn.bank_id]
        self.assertEqual(bank["answers"][turn.question.id]["verification"], "quote_verified")

    def test_evidence_counts_partitions_accepted_answers_and_skips_parked_ones(self) -> None:
        state = {"banks": {
            "discover": {"answers": {
                "a": {"verification": "quote_verified"},
                "b": {"verification": "source_verified"},
                "c": {"verification": "supplied_unverified"},
                "d": {},
                "e": {"verification": "failed_validation", "parked": True},
                "f": {"verification": "quote_verified", "parked": True},
            }},
            "define": {"answers": {"g": {"verification": "quote_verified"}}},
        }}
        self.assertEqual(evidence_counts(state, BANKS),
                         {"quote_verified": 2, "source_verified": 1, "supplied_unverified": 2})

    def test_every_excerpt_field_supplied_must_check_out(self) -> None:
        # One genuine field cannot carry a fabricated one past the check.
        conductor = self.conductor()
        evidence = dict(self.quoted(GENUINE), excerpt=FABRICATED)
        result = self.submit(conductor, evidence, "mixed")
        self.assertEqual(result.status, "challenge")
        self.assertIn("excerpt does not occur", result.message)

    def test_an_excerpt_against_a_source_that_is_not_a_document_is_refused(self) -> None:
        for index, source in enumerate(("Asha interview transcript round two", "INT-0042",
                                        "https://example.com/transcripts/asha")):
            with self.subTest(source=source):
                self.assertIsNone(source_resolver(self.root)(source))
                conductor = self.conductor("uncitable-%d" % index)
                result = self.submit(conductor, self.quoted(GENUINE, source=source), "uncitable-%d" % index)
                self.assertEqual(result.status, "challenge")
                self.assertIn("a quotation can only be recorded against a citable document", result.message)
                self.assertIn(repr(source), result.message)

    def test_whitespace_and_line_wrap_are_ignored_but_case_and_punctuation_are_not(self) -> None:
        # The stated normalization: every run of whitespace, line breaks
        # included, compares as one space on both sides. Nothing else is folded.
        cases = {
            GENUINE: "accepted",
            "  We re-key every failed payout batch\nby hand,\tand it takes the whole of Monday morning.  ":
                "accepted",
            GENUINE.lower(): "challenge",
            GENUINE.replace("hand,", "hand"): "challenge",
            GENUINE.replace("re-key", "rekey"): "challenge",
        }
        for index, (quote, expected) in enumerate(cases.items()):
            with self.subTest(quote=quote):
                result = self.submit(self.conductor("ws-%d" % index), self.quoted(quote), "ws-%d" % index)
                self.assertEqual(result.status, expected)

    def test_a_document_the_reader_cannot_open_refuses_the_quote(self) -> None:
        # A path the resolver finds but the reader refuses (a symlink inside the
        # workspace, or bytes that are not UTF-8) is not a pass by default.
        (self.root / "notes" / "linked.md").symlink_to(self.root / "notes" / "interview.md")
        (self.root / "notes" / "binary.md").write_bytes(b"\xff\xfe not text")
        for index, source in enumerate(("notes/linked.md", "notes/binary.md")):
            with self.subTest(source=source):
                self.assertIs(source_resolver(self.root)(source), True)
                self.assertIsNone(document_reader(self.root)(source))
                result = self.submit(self.conductor("unreadable-%d" % index),
                                     self.quoted(GENUINE, source=source), "unreadable-%d" % index)
                self.assertEqual(result.status, "challenge")
                self.assertIn("could not be read to check the quotation", result.message)

    def test_a_conductor_without_a_document_reader_refuses_excerpt_bearing_evidence(self) -> None:
        for index, source in enumerate(("notes/interview.md", "Asha interview transcript round two")):
            with self.subTest(source=source):
                conductor = self.conductor("no-reader-%d" % index, reader=False)
                result = self.submit(conductor, self.quoted(GENUINE, source=source), "no-reader-%d" % index)
                self.assertEqual(result.status, "challenge")
                self.assertIn("no document reader configured", result.message)

    def test_an_answer_without_an_excerpt_is_byte_identical_with_or_without_the_reader(self) -> None:
        # Without the reader is how every Conductor was built before quotations
        # were checked, so equal bytes here is "unchanged from today".
        expected = {"notes/interview.md": "source_verified",
                    "Asha interview transcript round two": "supplied_unverified"}
        for index, (source, label) in enumerate(expected.items()):
            with self.subTest(source=source):
                states, outcomes = [], []
                for reader in (False, True):
                    conductor = self.conductor("plain-%d-%s" % (index, reader), reader=reader)
                    outcome = self.submit(conductor, dict(observed(), source=source), "plain")
                    outcomes.append((outcome.status, outcome.message, outcome.revision))
                    states.append(conductor.store.read_snapshot("payments").files[STATE_PATH])
                self.assertEqual(outcomes[0], outcomes[1])
                self.assertEqual(states[0], states[1])
                self.assertEqual(json.loads(states[1])["banks"]["discover"]["answers"]["discover.person"], {
                    "answer": "Mina exported the failures.",
                    "evidence": dict(observed(), source=source),
                    "evidence_class": "observed_behavior",
                    "verification": label,
                })

    def test_the_conductor_module_has_no_filesystem_access(self) -> None:
        # The layering the document reader exists for: nothing else enforces it,
        # and importing pathlib here to read the file directly would look like
        # a working shortcut.
        import ast
        import pmos.conductor as module
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        banned = {"pathlib", "os", "io", "shutil", "tempfile", "glob"}
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found += [alias.name for alias in node.names if alias.name.split(".")[0] in banned]
            elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in banned:
                found.append(node.module)
            elif isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
                if name in {"open", "read_text", "read_bytes"}:
                    found.append(name + "()")
        self.assertEqual(found, [])

    # ---- what each new refusal does to the store and to the challenge budget ----
    # Pinned per refusal because docs/RUNTIME-QUICKSTART.md states which refusals
    # advance the revision; the table built on that claim needs a test per row.

    def assert_challenge_recorded(self, conductor: Conductor, evidence: dict, turn_id: str) -> TurnOutcome:
        before = conductor.next_turn().revision
        result = self.submit(conductor, evidence, turn_id)
        state = conductor.state()
        self.assertEqual((result.status, result.challenge_count), ("challenge", 1))
        self.assertNotEqual(result.revision, before)
        self.assertEqual(conductor.next_turn().revision, result.revision)
        self.assertIn(turn_id, state["turn_results"])
        self.assertEqual(state["banks"]["discover"]["challenges"], {"discover.person": 1})
        (event,) = state["banks"]["discover"]["rejected"]["discover.person"]
        self.assertEqual((event["event"], event["reason"]), ("challenged", result.message))
        self.assertEqual(state["banks"]["discover"]["cursor"], 0)
        return result

    def test_refusal_quote_mismatch_writes_a_turn_and_spends_a_challenge(self) -> None:
        self.assert_challenge_recorded(self.conductor(), self.quoted(FABRICATED), "mismatch")

    def test_refusal_uncitable_source_writes_a_turn_and_spends_a_challenge(self) -> None:
        self.assert_challenge_recorded(self.conductor(), self.quoted(GENUINE, source="INT-0042"), "uncitable")

    def test_refusal_no_document_reader_writes_a_turn_and_spends_a_challenge(self) -> None:
        self.assert_challenge_recorded(self.conductor(reader=False), self.quoted(GENUINE), "no-reader")

    def test_refusal_unreadable_document_writes_a_turn_and_spends_a_challenge(self) -> None:
        (self.root / "notes" / "binary.md").write_bytes(b"\xff\xfe")
        self.assert_challenge_recorded(self.conductor(), self.quoted(GENUINE, source="notes/binary.md"),
                                       "unreadable")

    def test_refusal_too_short_writes_a_turn_and_spends_a_challenge(self) -> None:
        self.assert_challenge_recorded(self.conductor(), self.quoted("payout batch"), "too-short")

    def test_a_third_refusal_of_each_new_kind_parks_the_question(self) -> None:
        (self.root / "notes" / "binary.md").write_bytes(b"\xff\xfe")
        kinds = {
            "mismatch": (True, lambda n: self.quoted("%s %d" % (FABRICATED, n))),
            "uncitable": (True, lambda n: self.quoted(GENUINE, source="INT-%04d" % n)),
            "unreadable": (True, lambda n: self.quoted(GENUINE + " %d" % n, source="notes/binary.md")),
            "too short": (True, lambda n: self.quoted("batch %d" % n)),
            "no reader": (False, lambda n: self.quoted(GENUINE + " %d" % n)),
        }
        for index, (kind, (reader, evidence)) in enumerate(kinds.items()):
            with self.subTest(kind=kind):
                conductor = self.conductor("park-%d" % index, reader=reader)
                statuses = [self.submit(conductor, evidence(attempt), "park-%d" % attempt)
                            for attempt in range(3)]
                self.assertEqual([(item.status, item.challenge_count) for item in statuses],
                                 [("challenge", 1), ("challenge", 2), ("parked", 2)])
                state = conductor.state()
                bank = state["banks"]["discover"]
                self.assertEqual((bank["parked"], bank["cursor"]), (["discover.person"], 1))
                self.assertEqual(bank["answers"]["discover.person"]["verification"], "failed_validation")
                # A parked answer is filed as offered, not accepted, so no report counts it.
                self.assertEqual(evidence_counts(state, BANKS),
                                 {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 0})

    # ---- gate proofs ----
    QUOTING_BANKS = (
        QuestionBank("discover", "v1", (
            Question("discover.person", "Who did the behavior?", EvidenceClass.OBSERVED_BEHAVIOR),
        ), gate_prerequisites=("signed_by", "quote"), gate_approvers=("asha",)),
    )

    def gated(self, name: str) -> tuple[Conductor, str]:
        conductor = self.conductor(name, banks=self.QUOTING_BANKS)
        accepted = self.submit(conductor, observed(), "person")
        self.assertEqual(accepted.status, "accepted")
        (self.root / "gate-1.md").write_text(INTERVIEW, encoding="utf-8")
        return conductor, accepted.revision

    def gate_evidence(self, quote: str) -> dict:
        return dict(gate_proof(source="gate-1.md",
                               source_hash=hashlib.sha256(INTERVIEW.encode("utf-8")).hexdigest()),
                    quote=quote)

    def test_a_gate_proof_whose_excerpt_is_not_in_the_gate_source_is_refused(self) -> None:
        conductor, revision = self.gated("gate-bad")
        before = conductor.state()
        result = conductor.prove_gate("discover", self.gate_evidence(FABRICATED),
                                      expected_revision=revision, turn_id="gate-bad")
        self.assertEqual(result.status, "blocked")
        self.assertIn("quote does not occur in gate-1.md", result.message)
        self.assertIn(FABRICATED, result.message)
        after = conductor.state()
        # A blocked gate writes its turn and advances the revision, records no
        # approval, moves no bank, and has no challenge budget to spend.
        self.assertNotEqual(result.revision, revision)
        self.assertIn("gate-bad", after["turn_results"])
        self.assertEqual((after["gates"], after["current_bank"]), ({}, before["current_bank"]))
        self.assertEqual(after["banks"]["discover"]["challenges"], {})

    def test_a_gate_proof_whose_excerpt_is_in_the_gate_source_is_recorded(self) -> None:
        conductor, revision = self.gated("gate-good")
        result = conductor.prove_gate("discover", self.gate_evidence(GENUINE),
                                      expected_revision=revision, turn_id="gate-good")
        self.assertEqual(result.status, "completed")
        self.assertEqual(conductor.state()["gates"]["discover"]["proof"]["quote"], GENUINE)

    def test_a_gate_proof_excerpt_needs_a_document_reader(self) -> None:
        conductor = Conductor(self.store("gate-no-reader"), "payments", self.QUOTING_BANKS,
                              gate_source_verifier=local_gate_verifier(self.root),
                              source_resolver=source_resolver(self.root))
        accepted = self.submit(conductor, observed(), "person")
        (self.root / "gate-1.md").write_text(INTERVIEW, encoding="utf-8")
        result = conductor.prove_gate("discover", self.gate_evidence(GENUINE),
                                      expected_revision=accepted.revision, turn_id="gate-no-reader")
        self.assertEqual(result.status, "blocked")
        self.assertIn("no document reader configured", result.message)


QUICKSTART = Path(__file__).resolve().parent.parent / "docs" / "RUNTIME-QUICKSTART.md"
TABLE_HEADER = "| Refusal | Store revision advances | Why |"
# The seven refusals the paragraph this table replaced named, and the
# quotation refusal the excerpt check added beside them, committed here rather
# than read from the table, so a row can be neither dropped nor invented
# without this set being edited in the same change where a reviewer sees it.
REFUSALS_NAMED = frozenset({
    "insufficient evidence",
    "an answer to a question other than the one offered",
    "an unknown question ID",
    "an unverifiable gate source",
    "a stale expected revision",
    "a reused turn ID",
    "a request refused before the conductor reads it",
    "a quotation that is not in the cited document or cannot be checked",
})


def refusal_table(text: str) -> dict[str, bool]:
    """The quickstart's refusal table, as refusal -> does the revision advance."""
    lines = text.splitlines()
    start = lines.index(TABLE_HEADER) + 2
    rows: dict[str, bool] = {}
    for raw in lines[start:]:
        if not raw.startswith("|"):
            break
        refusal, advances = [cell.strip() for cell in raw.strip("|").split("|")][:2]
        if advances not in ("yes", "no"):
            raise AssertionError("row %r says %r, not yes or no" % (refusal, advances))
        rows[refusal] = advances == "yes"
    return rows


class RefusalTableTest(unittest.TestCase):
    """docs/RUNTIME-QUICKSTART.md's refusal table, driven through a real Conductor.

    The table replaced a paragraph that stated the same seven facts as running
    prose, which nothing checked. Every row is a claim about store behaviour,
    so a row that is wrong makes the document falser than the paragraph was.
    Each sub-case also checks the outcome it got back, so a driver that stopped
    reaching its refusal fails here rather than passing on a revision that
    simply never moved.
    """

    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "runtime.sqlite")
        self.stores = [self.store]
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        self.conductor = Conductor(self.store, "payments", BANKS, gate_source_verifier=verifier)

    def tearDown(self) -> None:
        for store in self.stores:
            store.close()
        self.temp.cleanup()

    def quotation_refusals(self) -> list[tuple[bool, bool, object]]:
        """The five ways the excerpt check refuses, each on a fresh store."""
        root = Path(self.temp.name, "workspace")
        (root / "notes").mkdir(parents=True)
        (root / "notes" / "interview.md").write_text(INTERVIEW, encoding="utf-8")
        (root / "notes" / "latin1.md").write_bytes(b"caf\xe9 notes, not UTF-8 text\n")
        cases = (
            ("absent", True, "notes/interview.md", FABRICATED, "does not occur in"),
            ("short", True, "notes/interview.md", "Monday morning", "too short to check"),
            ("uncitable", True, "Asha interview", GENUINE, "can only be recorded against a citable"),
            ("unreadable", True, "notes/latin1.md", GENUINE, "could not be read to check"),
            ("no-reader", False, "notes/interview.md", GENUINE, "no document reader configured"),
        )
        results = []
        for name, reader, source, quote, reason in cases:
            self.store = Store(Path(self.temp.name) / (name + ".sqlite"))
            self.stores.append(self.store)
            conductor = Conductor(self.store, "payments", BANKS,
                                  source_resolver=source_resolver(root),
                                  document_reader=document_reader(root) if reader else None)
            evidence = dict(observed(), source=source, quote=quote)
            results.append(self.moved(
                lambda: conductor.submit_answer("discover.person", "Mina exported the failures.",
                                                evidence, expected_revision=self.token(),
                                                turn_id=name),
                lambda result, reason=reason: (isinstance(result, TurnOutcome)
                                               and result.status == "challenge"
                                               and reason in result.message)))
        return results

    def token(self) -> str:
        return self.store.head("payments").token

    def moved(self, action, expect) -> tuple[bool, bool, object]:
        """(did the revision move, was the outcome the one expected, the outcome)."""
        before = self.store.head("payments").revision
        try:
            result = action()
        except ValidationError as exc:
            result = exc
        return self.store.head("payments").revision != before, expect(result), result

    @staticmethod
    def outcome(status: str, message: str | None = None):
        return lambda result: (isinstance(result, TurnOutcome) and result.status == status
                               and (message is None or result.message == message))

    @staticmethod
    def raised(result) -> bool:
        return isinstance(result, ValidationError)

    def drive(self, refusal: str) -> list[tuple[bool, bool, object]]:
        if refusal == "a quotation that is not in the cited document or cannot be checked":
            return self.quotation_refusals()
        conductor, token = self.conductor, self.token
        first = conductor.next_turn()
        mismatch = self.outcome("conflict", "answer does not match the current question")
        if refusal == "insufficient evidence":
            return [self.moved(lambda: conductor.submit_answer(
                "discover.person", "A hunch.", {"class": "team_belief", "source": "hunch"},
                expected_revision=token(), turn_id="weak"), self.outcome("challenge"))]
        if refusal == "an answer to a question other than the one offered":
            return [self.moved(lambda: conductor.submit_answer(
                "discover.cost", "Support exported 41.", artifact(),
                expected_revision=token(), turn_id="ahead"), mismatch)]
        if refusal == "an unknown question ID":
            return [self.moved(lambda: conductor.submit_answer(
                "discover.nowhere", "An answer.", observed(),
                expected_revision=token(), turn_id="nowhere"), mismatch)]
        person = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=first.revision, turn_id="person")
        self.assertEqual(person.status, "accepted")
        if refusal == "an unverifiable gate source":
            conductor.submit_answer("discover.cost", "Support exported 41.", artifact(),
                                    expected_revision=token(), turn_id="cost")
            return [self.moved(lambda: conductor.prove_gate(
                "discover", gate_proof(source="forged.md"), expected_revision=token(), turn_id="gate"),
                self.outcome("blocked", "gate source could not be verified"))]
        if refusal == "a stale expected revision":
            return [self.moved(lambda: conductor.submit_answer(
                "discover.cost", "Support exported 41.", artifact(),
                expected_revision=first.revision, turn_id="late"),
                self.outcome("conflict", "expected revision is stale"))]
        if refusal == "a reused turn ID":
            # Both halves of the row: the identical replay returns the original
            # result, and a different payload under the same ID is a conflict.
            return [
                self.moved(lambda: conductor.submit_answer(
                    "discover.person", "Mina exported the failures.", observed(),
                    expected_revision=token(), turn_id="person"), self.outcome("accepted")),
                self.moved(lambda: conductor.submit_answer(
                    "discover.cost", "Something else.", artifact(),
                    expected_revision=token(), turn_id="person"), self.outcome("conflict")),
            ]
        if refusal == "a request refused before the conductor reads it":
            return [
                self.moved(lambda: conductor.submit_answer(
                    "", "An answer.", observed(), expected_revision=token(), turn_id="bad-id"),
                    self.raised),
                self.moved(lambda: conductor.submit_answer(
                    "discover.cost", "An answer.", "not an object",
                    expected_revision=token(), turn_id="bad-evidence"), self.raised),
                self.moved(lambda: conductor.prove_gate(
                    "nosuchbank", gate_proof(), expected_revision=token(), turn_id="bad-bank"),
                    self.raised),
            ]
        raise AssertionError("no driver for the refusal %r" % refusal)

    def test_the_table_names_exactly_the_refusals_the_paragraph_did(self) -> None:
        self.assertEqual(REFUSALS_NAMED, set(refusal_table(QUICKSTART.read_text(encoding="utf-8"))))

    def test_every_row_is_true_of_the_store_revision(self) -> None:
        for refusal, advances in refusal_table(QUICKSTART.read_text(encoding="utf-8")).items():
            with self.subTest(refusal=refusal):
                self.tearDown()
                self.setUp()
                cases = self.drive(refusal)
                for moved, expected, result in cases:
                    self.assertTrue(expected, "%r did not produce its refusal: %r" % (refusal, result))
                    self.assertEqual(advances, moved,
                                     "the table says the revision %s after %r, and it %s"
                                     % ("advances" if advances else "stays",
                                        refusal, "moved" if moved else "stayed"))


def quickstart_bullet(text: str, key: str) -> str:
    """The quickstart's Phase status bullet that opens with `key`, flattened."""
    lines = text.splitlines()
    opener = "- `%s`" % key
    start = next(index for index, raw in enumerate(lines) if raw.startswith(opener))
    body = [lines[start]]
    for raw in lines[start + 1:]:
        if not raw.startswith("  "):
            break
        body.append(raw)
    return " ".join(" ".join(body).split())


class PhaseStatusDocTest(unittest.TestCase):
    """The quickstart's `outcomes` and `missing` bullets, against a real report.

    The bullets name the keys a reader of `pmos status --json` will look for
    and say that a Gate 5 line citing BUILD-5 reads Gate 4's answer. Here the
    bullets are held to their wording, and the report a freshly initialised
    product produces is held to the keys they name, to `answered_in` naming
    the gate-4 bank for BUILD-5, and to the `carried` marker. Nothing is
    answered on a fresh product, so `met` turning true on a carried answer is
    not exercised here; tests/test_pmos_phases.py drives that (a carried
    answer met, a parked one unmet).
    """

    def status(self, *flags: str) -> str:
        import contextlib
        import io
        from pmos.cli import main
        with TemporaryDirectory() as folder:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["init", "--path", folder, "--product-id", "demo"]), 0)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main(["status", "--path", folder, "--product-id", "demo", *flags])
        return out.getvalue()

    def report(self) -> dict:
        return json.loads(self.status("--json"))

    def test_human_mode_prints_the_table_and_not_the_phases_list(self) -> None:
        """The paragraph once said human mode printed `phases` as JSON; 0.8.0
        dropped it from human output, and the paragraph now says so."""
        text = " ".join(QUICKSTART.read_text(encoding="utf-8").split())
        self.assertIn("In human mode `status` does not print `phases` itself", text)
        human = self.status().splitlines()
        self.assertFalse([line for line in human if line.startswith("phases:")])
        self.assertEqual(6, len([line for line in human if line.startswith("Gate ")]))
        self.assertTrue([line for line in human if "no question stands behind" in line])
        self.assertTrue([line for line in human if "carried from build" in line])

    def test_the_bullets_name_the_keys_and_the_cross_bank_read(self) -> None:
        text = QUICKSTART.read_text(encoding="utf-8")
        outcomes = quickstart_bullet(text, "outcomes")
        missing = quickstart_bullet(text, "missing")
        for phrase in ("read from the bank that owns it", "`BUILD-5`", "Gate 4",
                       "`answered_in`", "`carried`", '`["build"]`'):
            with self.subTest(bullet="outcomes", phrase=phrase):
                self.assertIn(phrase, outcomes)
        for phrase in ("`gate_lines`", "`unknown_gate_lines`", "`met` is `null`"):
            with self.subTest(bullet="missing", phrase=phrase):
                self.assertIn(phrase, missing)

    def test_the_report_has_what_the_bullets_describe(self) -> None:
        phases = self.report()["phases"]
        gate_of = {phase["bank_id"]: phase["gate"] for phase in phases}
        for phase in phases:
            with self.subTest(bank=phase["bank_id"]):
                self.assertIn("gate_lines", phase["missing"])
                self.assertEqual(
                    phase["missing"]["unknown_gate_lines"],
                    [row["line"] for row in phase["outcomes"] if row["met"] is None])
                for row in phase["outcomes"]:
                    self.assertEqual(row["carried"], sorted(
                        {bank for bank in row["answered_in"].values() if bank != phase["bank_id"]}))
        deliver = [phase for phase in phases if phase["gate"] == 5][0]
        cites = [row for row in deliver["outcomes"] if "BUILD-5" in row["questions"]]
        self.assertEqual(1, len(cites), "the Gate 5 line citing BUILD-5 is gone")
        row = cites[0]
        self.assertEqual(4, gate_of[row["answered_in"]["BUILD-5"]])
        # Unanswered on a fresh product, and still marked: the marker names the
        # owning bank, not an answer that was carried.
        self.assertFalse(row["met"])
        self.assertEqual(["build"], row["carried"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
