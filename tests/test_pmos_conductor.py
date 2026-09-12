"""Executable contract for the persistent deterministic Conductor."""

from __future__ import annotations

import os
import hashlib
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
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
