import json
import shlex
import hashlib
import os
import signal
import subprocess
import sys
import threading
import unittest
import shutil
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pmos.cli import (_cli_source_resolver, _gate_result, _local_gate_verifier, _paths,
                      _product_conductor, _unsupported_platform_reason, main, PIN_PATH,
                      UNSUPPORTED_PLATFORM_EXIT_CODE)
from pmos.banks import CONTRACT_PATH
from pmos.conductor import STATE_PATH, TurnOutcome
from pmos.migrations import (create_legacy_fixture, migrate_workspace, recover_workspace,
                              rollback_workspace, MigrationError)
from pmos.store import Store, ValidationError
from pmos.artifacts import artifact_revision
import pmos.migrations as migrations


class CliTests(unittest.TestCase):
    def test_init_status_verify_human_and_json(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.assertEqual(main(["--json", "status", "--path", folder]), 0)
            self.assertEqual(main(["verify", "--path", folder, "--json"]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("checkout").revision, 1)
                self.assertIn(PIN_PATH, store.read_snapshot("checkout").files)

    def status(self, folder: str) -> dict:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--json", "status", "--path", folder, "--product-id", "checkout"]), 0)
        return json.loads(output.getvalue())

    def human_status(self, folder: str) -> str:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["status", "--path", folder, "--product-id", "checkout"]), 0)
        return output.getvalue()

    def answer(self, folder: str, evidence: dict, token: str, turn_id: str,
               question_id: str = "DISCOVER-1") -> dict:
        output = StringIO()
        with redirect_stdout(output):
            main(["answer", "--path", folder, "--product-id", "checkout", "--question-id", question_id,
                  "--answer", "A real outcome", "--evidence", json.dumps(evidence),
                  "--expected-revision", token, "--turn-id", turn_id, "--json"])
        return json.loads(output.getvalue())

    def answer_bank(self, folder: str, prefix: str) -> dict:
        for _ in range(20):
            status = self.status(folder)
            if status["interview"] != "question":
                return status
            question_id = status["question"]["id"]
            result = self.answer(folder, {"class": "observed_behavior", "source": "interview-001",
                                          "date": "2026-09-04", "location": "customer-call"},
                                 status["revision_token"], prefix + "-" + question_id,
                                 question_id=question_id)
            self.assertEqual(result["outcome"]["status"], "accepted")
        self.fail("the bank did not finish")

    def test_status_human_output_leads_with_where_you_are_and_what_to_open(self):
        # The payload always carried this; it was buried in a one-line JSON dump of phases.
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["status", "--path", folder, "--product-id", "checkout"]), 0)
            text = output.getvalue()
            self.assertIn("Where you are: Gate 1, DISCOVER, question DISCOVER-1 of", text)
            self.assertIn("Do this next: pmos answer", text)
            self.assertIn("Open next: discovery/problem-framing.md", text)
            self.assertIn("Gate 6", text)
            # the wall of JSON the summary replaces is gone from human output
            self.assertNotIn("\"named_documents\"", text)

    def test_status_json_output_still_carries_phases(self):
        # --json is a machine contract: the human summary must not touch it.
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--json", "status", "--path", folder, "--product-id", "checkout"]), 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(len(payload["phases"]), 6)
            self.assertNotIn("Where you are", output.getvalue())

    def test_status_alone_resumes_the_interview_after_init(self):
        with TemporaryDirectory() as parent:
            folder = str(Path(parent) / "work space")
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.status(folder)
            # init commits the pinned contract, so the product starts at revision 1, not 0:-.
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                self.assertEqual(status["revision_token"], store.head("checkout").token)
            self.assertEqual((status["interview"], status["question"]["id"]), ("question", "DISCOVER-1"))
            self.assertIn("--expected-revision " + shlex.quote(status["revision_token"]), status["next"])
            self.assertIn(shlex.quote(str(Path(folder).resolve())), status["next"])
            human = self.human_status(folder)
            for value in (status["revision_token"], status["question"]["id"], status["next"]):
                self.assertIn(value, human)
            result = self.answer(folder, {"class": "observed_behavior", "source": "interview-001",
                                          "date": "2026-09-04", "location": "customer-call"},
                                 status["revision_token"], "answer-001")
            self.assertEqual(result["outcome"]["status"], "accepted")

    def pin(self, folder: str, raw: bytes) -> None:
        with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
            snapshot = store.read_snapshot("checkout")
            files = dict(snapshot.files)
            files[PIN_PATH] = raw
            result = store.commit("checkout", files, expected_revision=snapshot.head,
                                  metadata={"reason": "test pin"})
            self.assertTrue(result.committed)

    def test_a_product_without_a_pin_keeps_the_legacy_bank(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            # init pins now, so a product created through the Store alone stands for one made before the pin.
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                store.create_product("legacy")
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--json", "status", "--path", folder, "--product-id", "legacy"]), 0)
            status = json.loads(output.getvalue())
            self.assertEqual(status["question"]["id"], "first-outcome")
            self.assertEqual(status["question_banks"]["pinned"], {"onboarding": "v1"})
            self.assertEqual(set(status["question_banks"]["shipped"]),
                             {"discover", "define", "design", "build", "deliver", "operate"})
            self.assertFalse(status["question_banks"]["current"])
            self.assertIn("before the question bank contract", status["question_banks"]["message"])

    def test_a_pinned_product_runs_the_pinned_banks(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.status(folder)
            self.assertEqual(status["current_bank_id"], "discover")
            self.assertEqual(status["question"]["id"], "DISCOVER-1")
            self.assertEqual(status["question_banks"]["pinned"], status["question_banks"]["shipped"])
            self.assertEqual(len(status["question_banks"]["pinned"]), 6)
            self.assertTrue(status["question_banks"]["current"])
            evidence = {"class": "observed_behavior", "source": "session replay",
                        "date": "2026-09-03", "location": "replay/17"}
            output = StringIO()
            with redirect_stdout(output):
                rc = main(["answer", "--path", folder, "--product-id", "checkout",
                           "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                           "--evidence", json.dumps(evidence),
                           "--expected-revision", status["revision_token"],
                           "--turn-id", "answer-001", "--json"])
            self.assertEqual(rc, 0)
            result = json.loads(output.getvalue())
            self.assertTrue(result["ok"])
            status = self.status(folder)
            self.assertEqual(status["question"]["id"], "DISCOVER-2")

    def test_a_pin_that_differs_from_the_shipped_contract_is_kept(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            contract = json.loads(CONTRACT_PATH.read_bytes())
            contract["banks"][0]["version"] = "c0000000000000000"
            contract["banks"][0]["questions"][0]["ask"] = "Who has this problem, by name?"
            self.pin(folder, json.dumps(contract).encode("utf-8"))
            status = self.status(folder)
            self.assertEqual(status["question_banks"]["pinned"]["discover"], "c0000000000000000")
            self.assertFalse(status["question_banks"]["current"])
            # the pin is still kept; the difference is that status now names the way out
            self.assertIn("adopt it with `pmos repin`", status["question_banks"]["message"])
            self.assertEqual(status["question"]["prompt"], "Who has this problem, by name?")

    def test_repin_adopts_the_shipped_contract_and_stales_the_changed_bank(self):
        # A product pinned to older questions can now adopt the shipped ones. Answers survive;
        # the bank whose questions changed must prove its gate again, through the same staleness
        # path a changed proof source takes.
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            contract = json.loads(CONTRACT_PATH.read_bytes())
            contract["banks"][0]["version"] = "c0000000000000000"
            contract["banks"][0]["questions"][0]["ask"] = "Who has this problem, by name?"
            self.pin(folder, json.dumps(contract).encode("utf-8"))
            status = self.answer_bank(folder, "discover")
            proof_bytes = b"discover"
            Path(folder, "gate-discover.txt").write_bytes(proof_bytes)
            evidence = {"source": "gate-discover.txt", "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                        "actor_id": "local-reviewer", "requester_id": "local-operator",
                        "decision": "approved", "approved_at": "2026-09-04T00:00:00Z"}
            output = StringIO()
            with redirect_stdout(output):
                rc = main(["gate", "--path", folder, "--product-id", "checkout", "--bank-id", "discover",
                           "--evidence", json.dumps(evidence), "--expected-revision", status["revision_token"],
                           "--turn-id", "gate-discover", "--json"])
            self.assertEqual(rc, 0, output.getvalue())
            self.assertEqual(self.status(folder)["stale_banks"], [])

            preview = StringIO()
            with redirect_stdout(preview):
                self.assertEqual(main(["--json", "repin", "--path", folder, "--product-id", "checkout",
                                       "--dry-run"]), 0)
            planned = json.loads(preview.getvalue())
            self.assertEqual([entry["bank_id"] for entry in planned["changed"]], ["discover"])
            self.assertEqual(planned["changed"][0]["modified"], ["DISCOVER-1"])
            self.assertEqual(planned["gates_to_prove_again"], ["discover"])
            # a preview writes nothing
            self.assertEqual(self.status(folder)["question_banks"]["pinned"]["discover"], "c0000000000000000")
            self.assertEqual(self.status(folder)["stale_banks"], [])

            applied = StringIO()
            with redirect_stdout(applied):
                self.assertEqual(main(["--json", "repin", "--path", folder, "--product-id", "checkout"]), 0)
            done = json.loads(applied.getvalue())
            self.assertTrue(done["ok"])
            after = self.status(folder)
            self.assertEqual(after["question_banks"]["pinned"], after["question_banks"]["shipped"])
            self.assertTrue(after["question_banks"]["current"])
            self.assertEqual([item["bank_id"] for item in after["stale_banks"]], ["discover"])
            self.assertIn("changed since this gate was approved", after["stale_banks"][0]["message"])
            # the answers are still there: the bank is not back at its first question
            self.assertEqual(after["source_verified"] + after["supplied_unverified"], 9)

    def test_a_corrupt_pin_is_reported_rather_than_raised(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.pin(folder, b"{")
            status = self.status(folder)
            self.assertIn("not valid JSON", status["interview_error"])
            evidence = {"class": "observed_behavior", "source": "session replay",
                        "date": "2026-09-03", "location": "replay/17"}
            output = StringIO()
            with redirect_stdout(output):
                rc = main(["answer", "--path", folder, "--product-id", "checkout",
                           "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                           "--evidence", json.dumps(evidence),
                           "--expected-revision", status["revision_token"],
                           "--turn-id", "answer-001", "--json"])
            self.assertEqual(rc, 2)
            result = json.loads(output.getvalue())
            self.assertFalse(result["ok"])
            self.assertIn("not valid JSON", result["error"])

    def test_status_shows_a_parked_question_with_its_reopen_command(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            token = self.status(folder)["revision_token"]
            for label in ("bad1", "bad2", "bad3"):
                token = self.answer(folder, {"class": "observed_behavior", "source": "real interview"},
                                    token, label)["outcome"]["revision"]
            # Parking DISCOVER-1 moves the cursor on; the reopen is next once the rest of the bank is answered.
            status = self.answer_bank(folder, "rest")
            (parked,) = status["parked"]
            self.assertEqual(parked["question_id"], "DISCOVER-1")
            self.assertEqual(status["next"], parked["reopen"])
            for part in ("pmos reopen --path", "--product-id checkout", "--question-id DISCOVER-1",
                         "--expected-revision %s" % status["revision_token"], "--turn-id '<new turn id>'"):
                self.assertIn(part, parked["reopen"])
            self.assertIn(parked["reopen"], self.human_status(folder))

    def test_status_counts_a_verified_answer_and_names_the_gate(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            Path(folder, "notes").mkdir()
            Path(folder, "notes", "call.md").write_text("customer call notes\n", encoding="utf-8")
            result = self.answer(folder, {"class": "observed_behavior", "source": "notes/call.md",
                                          "date": "2026-09-04", "location": "customer-call"},
                                 self.status(folder)["revision_token"], "answer-verified")
            self.assertEqual(result["outcome"]["status"], "accepted")
            status = self.answer_bank(folder, "rest")
            self.assertEqual((status["source_verified"], status["supplied_unverified"]), (1, 8))
            self.assertEqual(status["interview"], "blocked")
            self.assertIn("pmos gate", status["next"])
            self.assertIn("--bank-id discover", status["next"])

    def test_status_reports_a_stale_gate_with_the_command_that_proves_it_again(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.assertEqual(status["supplied_unverified"], 9)
            proof = Path(folder, "onboarding-approval.txt")
            proof.write_bytes(b"reviewed onboarding evidence\n")
            gate = {"source": "onboarding-approval.txt", "source_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
                    "actor_id": "local-reviewer", "requester_id": "local-operator", "decision": "approved",
                    "approved_at": "2026-09-04T00:00:00Z"}
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["gate", "--path", folder, "--product-id", "checkout", "--bank-id", "discover",
                                       "--evidence", json.dumps(gate), "--expected-revision",
                                       status["revision_token"], "--turn-id", "gate-1", "--json"]), 0)
            after = self.status(folder)
            self.assertEqual((after["interview"], after["current_bank_id"]), ("question", "define"))
            proof.write_bytes(b"changed after approval\n")
            status = self.status(folder)
            self.assertEqual(status["interview"], "stale")
            (stale,) = status["stale_banks"]
            self.assertEqual(stale["bank_id"], "discover")
            # The approval source changed, not an artifact, so there is nothing to reconcile.
            self.assertEqual((stale["changed"], stale["reconcile"]), ([], []))
            self.assertEqual(status["next"], stale["gate"])
            self.assertIn("pmos gate", stale["gate"])

    def test_status_phases_report_tracks_discover_through_approval_and_staleness(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            contract = json.loads(CONTRACT_PATH.read_bytes())
            status = self.status(folder)
            phases = status["phases"]
            self.assertEqual([phase["bank_id"] for phase in phases],
                             ["discover", "define", "design", "build", "deliver", "operate"])
            discover = phases[0]
            self.assertEqual(discover["state"], "in_progress")
            self.assertEqual(discover["next_action"],
                             {"action": "answer", "bank_id": "discover", "question_id": "DISCOVER-1"})
            self.assertEqual(discover["required_approver"],
                             {"runtime": ["local-reviewer"], "attestation": "local",
                              "signoff_roles": contract["signoffs"]["1"]})
            for phase in phases[1:]:
                self.assertEqual(phase["state"], "not_started")
                self.assertIsNone(phase["next_action"])

            status = self.answer_bank(folder, "a")
            phases = {phase["bank_id"]: phase for phase in status["phases"]}
            self.assertEqual(phases["discover"]["state"], "awaiting_approval")
            self.assertEqual(phases["discover"]["next_action"],
                             {"action": "gate", "bank_id": "discover", "question_id": None})

            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            after = self.status(folder)
            phases = {phase["bank_id"]: phase for phase in after["phases"]}
            self.assertEqual(phases["discover"]["state"], "approved")
            self.assertIsNone(phases["discover"]["next_action"])
            self.assertEqual(phases["define"]["state"], "in_progress")

            proof = Path(folder, "onboarding-approval.txt")
            proof.write_bytes(b"changed after approval\n")
            stale = self.status(folder)
            phases = {phase["bank_id"]: phase for phase in stale["phases"]}
            self.assertEqual(phases["discover"]["state"], "stale")
            self.assertEqual(phases["discover"]["next_action"],
                             {"action": "gate", "bank_id": "discover", "question_id": None})
            self.assertEqual(phases["define"]["blocking_reason"],
                             "the approval for discover no longer holds; prove it again first")

    def test_status_phases_after_a_rejected_gate_leaves_discover_awaiting_approval(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "rejected")
            self.assertEqual(parsed["outcome"]["status"], "rejected")
            after = self.status(folder)
            discover = next(phase for phase in after["phases"] if phase["bank_id"] == "discover")
            self.assertEqual(discover["state"], "awaiting_approval")
            self.assertEqual(discover["next_action"],
                             {"action": "gate", "bank_id": "discover", "question_id": None})

    def test_status_phases_use_the_pinned_signoff_roles_not_the_shipped_ones(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            contract = json.loads(CONTRACT_PATH.read_bytes())
            shipped_roles = contract["signoffs"]["1"]
            contract["signoffs"]["1"] = ["A pinned-only approver"]
            self.pin(folder, json.dumps(contract).encode("utf-8"))
            status = self.status(folder)
            discover = status["phases"][0]
            self.assertEqual(discover["bank_id"], "discover")
            self.assertEqual(discover["required_approver"]["signoff_roles"], ["A pinned-only approver"])
            self.assertNotEqual(discover["required_approver"]["signoff_roles"], shipped_roles)

    def test_status_reports_a_phases_error_without_hiding_the_rest_of_status(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            baseline = self.status(folder)
            with patch("pmos.cli.phase_report",
                      side_effect=ValidationError("x.md is a symlink and was refused")):
                status = self.status(folder)
            self.assertEqual(status["phases"], [])
            self.assertEqual(status["phases_error"], "x.md is a symlink and was refused")
            self.assertEqual(status["interview"], "question")
            self.assertIsNotNone(status["next"])
            self.assertEqual(status["question"]["id"], "DISCOVER-1")
            self.assertIn("pinned", status["question_banks"])
            # phases_error is the only key the error adds: every other status key a
            # normal call returns is still present when phase_report raises.
            self.assertEqual(set(status) - {"phases_error"}, set(baseline))

    def test_status_reports_a_phases_error_for_a_real_symlinked_artifact(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            baseline = self.status(folder)
            target = self.write_artifact(folder, "discovery/problem-framing.md",
                                         "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                         "templates/discovery/problem-framing.md", "A real outcome")
            link = Path(folder, "discovery/problem-framing-link.md")
            os.symlink(target, link)
            status = self.status(folder)
            self.assertEqual(status["phases"], [])
            self.assertIn("discovery/problem-framing-link.md", status["phases_error"])
            self.assertIn("symlink", status["phases_error"])
            # The rest of status, the interview included, is untouched by the
            # scan failure: the real symlink does not make an earlier status
            # step fail, so every key but phases_error matches the baseline.
            self.assertEqual(set(status) - {"phases_error"}, set(baseline))
            self.assertEqual(status["interview"], baseline["interview"])
            self.assertEqual(status["question"], baseline["question"])
            self.assertIn("pinned", status["question_banks"])

    def test_an_answer_citing_a_missing_local_file_is_refused(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            result = self.answer(folder, {"class": "observed_behavior", "source": "notes/does-not-exist.txt",
                                          "date": "2026-09-04", "location": "customer-call"},
                                 self.status(folder)["revision_token"], "missing-1")
            self.assertEqual((result["ok"], result["outcome"]["status"]), (False, "challenge"))
            self.assertIn("could not be resolved", result["outcome"]["message"])

    def test_the_source_resolver_leaves_free_text_unchecked(self):
        with TemporaryDirectory() as folder:
            resolve = _cli_source_resolver(Path(folder))
            Path(folder, "notes.md").write_text("x", encoding="utf-8")
            self.assertIs(resolve("notes.md"), True)
            self.assertIs(resolve("notes/missing.md"), False)
            self.assertIs(resolve("../outside.md"), False)
            self.assertIsNone(resolve("real interview"))
            self.assertIsNone(resolve("Q3 review v1.2"))
            self.assertIsNone(resolve("interview-001"))

    def test_a_gate_result_never_reports_completion_while_another_gate_is_stale(self):
        outcome = TurnOutcome("stale", "3:abc", bank_id="define",
                              message="gate proof for discover recorded again; gate proof gate-2.md for define "
                                      "no longer verifies (changed or missing); prove the gate again")
        result = _gate_result(outcome, "checkout")
        self.assertEqual((result["ok"], result["outcome"]["completed"]), (False, False))
        self.assertEqual(result["error"], outcome.message)

    def test_a_gate_that_moves_to_the_next_bank_is_ok_but_not_complete(self):
        advanced = TurnOutcome("advanced", "5:abc", bank_id="discover",
                               message="gate proof recorded")
        advanced_result = _gate_result(advanced, "checkout")
        self.assertEqual((advanced_result["ok"], advanced_result["outcome"]["completed"]), (True, False))
        self.assertNotIn("error", advanced_result)

        completed = TurnOutcome("completed", "6:abc", bank_id="operate",
                                message="gate proof recorded", completed=True)
        completed_result = _gate_result(completed, "checkout")
        self.assertEqual((completed_result["ok"], completed_result["outcome"]["completed"]), (True, True))
        self.assertNotIn("error", completed_result)

        blocked = TurnOutcome("blocked", "5:abc", bank_id="discover",
                              message="gate source could not be verified")
        blocked_result = _gate_result(blocked, "checkout")
        self.assertEqual((blocked_result["ok"], blocked_result["outcome"]["completed"]), (False, False))
        self.assertEqual(
            blocked_result["error"],
            "gate proof was not accepted: gate source could not be verified",
        )

    def write_artifact(self, folder: str, rel_path: str, artifact_id: str, phase: str,
                       gate: int, depends_on: list, template: str, body: str) -> Path:
        path = Path(folder, rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        block = (
            "---\n"
            "artifact_id: %s\n"
            "phase: %s\n"
            "gate: %d\n"
            "status: draft\n"
            "depends_on: %s\n"
            "template: %s\n"
            "---\n"
            "%s\n"
        ) % (artifact_id, phase, gate, json.dumps(depends_on), template, body)
        path.write_text(block, encoding="utf-8")
        return path

    def gate(self, folder: str, token: str, turn_id: str, decision: str,
             bank_id: str = "discover") -> tuple[int, dict]:
        proof = Path(folder, "onboarding-approval.txt")
        proof.write_bytes(b"reviewed onboarding evidence\n")
        evidence = {"source": "onboarding-approval.txt",
                    "source_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
                    "actor_id": "local-reviewer", "requester_id": "local-operator", "decision": decision,
                    "approved_at": "2026-09-04T00:00:00Z"}
        output = StringIO()
        with redirect_stdout(output):
            rc = main(["gate", "--path", folder, "--product-id", "checkout", "--bank-id", bank_id,
                       "--evidence", json.dumps(evidence), "--expected-revision", token,
                       "--turn-id", turn_id, "--json"])
        return rc, json.loads(output.getvalue())

    def conductor_state(self, folder: str):
        with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
            return _product_conductor(store, Path(folder).resolve(), "checkout").state()

    def handoff(self, folder: str) -> tuple[int, dict]:
        output = StringIO()
        with redirect_stdout(output):
            rc = main(["--json", "handoff", "--path", folder, "--product-id", "checkout"])
        return rc, json.loads(output.getvalue())

    def reconcile(self, folder: str) -> dict:
        output = StringIO()
        with redirect_stdout(output):
            main(["--json", "reconcile", "--path", folder, "--product-id", "checkout"])
        return json.loads(output.getvalue())

    def export(self, folder: str, out_dir: str, force: bool = False) -> tuple[int, dict]:
        args = ["--json", "export", "--path", folder, "--product-id", "checkout", "--out", out_dir]
        if force:
            args.append("--force")
        output = StringIO()
        with redirect_stdout(output):
            rc = main(args)
        return rc, json.loads(output.getvalue())

    def head(self, folder: str):
        with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
            return store.head("checkout")

    def test_an_approved_gate_binds_the_manifest_to_the_workspace(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            path = self.write_artifact(folder, "discovery/problem-framing.md",
                                       "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                       "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            gate = self.conductor_state(folder)["gates"]["discover"]
            self.assertEqual(gate["manifest"], {
                "artifacts": [{"id": "checkout/discovery/problem-framing",
                               "path": "discovery/problem-framing.md",
                               "revision": artifact_revision(path.read_text(encoding="utf-8")),
                               "depends_on": []}],
                "dependencies": []})
            self.assertEqual(gate["attestation"], "local")

    def test_a_gate_whose_manifest_names_a_missing_dependency_is_not_accepted(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1,
                                ["checkout/discovery/missing"], "templates/discovery/problem-framing.md",
                                "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual(rc, 1)
            self.assertFalse(parsed["ok"])
            self.assertIn("depends on checkout/discovery/missing and the workspace does not have it yet",
                          parsed["error"])

    def test_a_rejected_gate_is_recorded_and_keeps_the_bank_blocked(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "rejected")
            self.assertEqual(rc, 1)
            self.assertFalse(parsed["ok"])
            self.assertTrue(parsed["rejection_recorded"])
            self.assertEqual(parsed["outcome"]["status"], "rejected")
            state = self.conductor_state(folder)
            (rejection,) = state["gate_rejections"]["discover"]
            self.assertEqual(rejection["manifest"]["artifacts"][0]["id"], "checkout/discovery/problem-framing")
            self.assertNotIn("discover", state["gates"])
            after = self.status(folder)
            self.assertEqual(after["interview"], "blocked")
            self.assertEqual(after["current_bank_id"], "discover")

    def test_status_lists_the_approvals_with_their_artifacts(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            after = self.status(folder)
            self.assertEqual(after["approvals"], [{
                "bank_id": "discover", "attestation": "local", "actor_id": "local-reviewer",
                "approved_at": "2026-09-04T00:00:00Z", "artifacts": ["checkout/discovery/problem-framing"],
                "dependencies": [], "superseded": 0}])
            self.assertEqual(after["rejections"], [])

    def test_status_names_the_changed_artifact_of_a_stale_approval(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            path = self.write_artifact(folder, "discovery/problem-framing.md",
                                       "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                       "templates/discovery/problem-framing.md", "A real outcome")
            reviewed = artifact_revision(path.read_text(encoding="utf-8"))
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A changed outcome")
            current = artifact_revision(path.read_text(encoding="utf-8"))
            self.assertNotEqual(reviewed, current)
            after = self.status(folder)
            self.assertEqual(after["interview"], "stale")
            (stale,) = after["stale_banks"]
            self.assertEqual(stale["bank_id"], "discover")
            self.assertEqual(stale["changed"], [{"id": "checkout/discovery/problem-framing",
                                                 "path": "discovery/problem-framing.md",
                                                 "reviewed": reviewed, "current": current}])
            self.assertEqual(stale["reconcile"], [])
            self.assertEqual(after["next"], stale["gate"])

    def test_status_keeps_a_rejection_after_the_approval_that_follows_it(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "rejected")
            self.assertEqual((rc, parsed["ok"]), (1, False))
            rc, parsed = self.gate(folder, self.status(folder)["revision_token"], "gate-2", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            after = self.status(folder)
            (rejection,) = after["rejections"]
            self.assertEqual((rejection["bank_id"], rejection["actor_id"], rejection["artifacts"]),
                             ("discover", "local-reviewer", ["checkout/discovery/problem-framing"]))
            self.assertRegex(rejection["rejected_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
            self.assertEqual([approval["bank_id"] for approval in after["approvals"]], ["discover"])

    def test_revision_bound_approvals_hold_through_the_cli(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            # (1) discover advances.
            status = self.answer_bank(folder, "a")
            problem_path = self.write_artifact(folder, "discovery/problem-framing.md",
                                               "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                               "templates/discovery/problem-framing.md", "A real outcome")
            problem_before = artifact_revision(problem_path.read_text(encoding="utf-8"))
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual(rc, 0)
            self.assertEqual(parsed["outcome"]["status"], "advanced")
            # (2) define artifacts in place.
            self.write_artifact(folder, "planning/vision.md", "checkout/planning/vision", "PLANNING", 2,
                                ["checkout/discovery/problem-framing"], "templates/planning/vision.md",
                                "A vision")
            self.write_artifact(folder, "definition/prd.md", "checkout/definition/prd", "DEFINE", 2,
                                ["checkout/planning/vision"], "templates/definition/prd.md",
                                "A product brief")
            status = self.answer_bank(folder, "b")
            # (3) rejection blocks advancement.
            rc, parsed = self.gate(folder, status["revision_token"], "gate-2", "rejected",
                                   bank_id="define")
            self.assertEqual(rc, 1)
            self.assertEqual(parsed["ok"], False)
            self.assertEqual(parsed["rejection_recorded"], True)
            status = self.status(folder)
            self.assertEqual(status["interview"], "blocked")
            self.assertEqual(status["current_bank_id"], "define")
            self.assertEqual(len(status["rejections"]), 1)
            self.assertEqual(status["rejections"][0]["bank_id"], "define")
            self.assertEqual([a["bank_id"] for a in status["approvals"]], ["discover"])
            # (4) approval advances to design question.
            rc, parsed = self.gate(folder, status["revision_token"], "gate-3", "approved",
                                   bank_id="define")
            self.assertEqual(rc, 0)
            self.assertEqual(parsed["outcome"]["status"], "advanced")
            status = self.status(folder)
            self.assertEqual([a["bank_id"] for a in status["approvals"]], ["discover", "define"])
            define_approval = [a for a in status["approvals"] if a["bank_id"] == "define"][0]
            self.assertEqual(define_approval["artifacts"],
                             ["checkout/definition/prd", "checkout/planning/vision"])
            self.assertEqual(define_approval["dependencies"], ["checkout/discovery/problem-framing"])
            self.assertEqual(status["interview"], "question")
            self.assertEqual(status["current_bank_id"], "design")
            question_id = status["question"]["id"]
            # (5) upstream change stales dependents and requires reconciliation.
            problem_path = self.write_artifact(folder, "discovery/problem-framing.md",
                                               "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                               "templates/discovery/problem-framing.md", "A changed outcome")
            problem_after = artifact_revision(problem_path.read_text(encoding="utf-8"))
            self.assertNotEqual(problem_before, problem_after)
            status = self.status(folder)
            self.assertEqual(status["interview"], "stale")
            self.assertEqual([s["bank_id"] for s in status["stale_banks"]], ["discover", "define"])
            for stale in status["stale_banks"]:
                self.assertEqual([c["id"] for c in stale["changed"]],
                                 ["checkout/discovery/problem-framing"])
            discover_stale = [s for s in status["stale_banks"] if s["bank_id"] == "discover"][0]
            define_stale = [s for s in status["stale_banks"] if s["bank_id"] == "define"][0]
            self.assertEqual(discover_stale["reconcile"], [])
            self.assertEqual(define_stale["reconcile"],
                             ["checkout/definition/prd", "checkout/planning/vision"])
            self.assertEqual(status["next"], status["stale_banks"][0]["gate"])
            # (6) re-approving one bank clears only that bank.
            rc, parsed = self.gate(folder, status["revision_token"], "gate-4", "approved",
                                   bank_id="discover")
            self.assertEqual(rc, 1)
            self.assertEqual(parsed["ok"], False)
            self.assertEqual(parsed["outcome"]["status"], "stale")
            self.assertEqual(parsed["outcome"]["bank_id"], "define")
            status = self.status(folder)
            self.assertEqual([s["bank_id"] for s in status["stale_banks"]], ["define"])
            discover_approval = [a for a in status["approvals"] if a["bank_id"] == "discover"][0]
            self.assertEqual(discover_approval["superseded"], 1)
            # (7) re-approving define clears it without moving the interview on.
            rc, parsed = self.gate(folder, status["revision_token"], "gate-5", "approved",
                                   bank_id="define")
            self.assertEqual(rc, 0)
            self.assertEqual(parsed["ok"], True)
            status = self.status(folder)
            self.assertEqual(status["interview"], "question")
            self.assertEqual(status["question"]["id"], question_id)
            self.assertEqual(status["stale_banks"], [])
            for bank in ("discover", "define"):
                approval = [a for a in status["approvals"] if a["bank_id"] == bank][0]
                self.assertEqual(approval["superseded"], 1)
            self.assertEqual(len(status["rejections"]), 1)
            self.assertEqual(status["rejections"][0]["bank_id"], "define")
            # (8) the history survives a reopen.
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                state = _product_conductor(store, Path(folder).resolve(), "checkout").state()
            superseded_discover = state["superseded_gates"]["discover"]
            self.assertEqual(len(superseded_discover), 1)
            superseded_record = superseded_discover[0]
            superseded_bindings = {
                binding["id"]: binding for binding in superseded_record["manifest"]["artifacts"]
            }
            self.assertEqual(superseded_bindings["checkout/discovery/problem-framing"]["revision"],
                             problem_before)
            current_discover_bindings = {
                binding["id"]: binding for binding in state["gates"]["discover"]["manifest"]["artifacts"]
            }
            self.assertEqual(
                current_discover_bindings["checkout/discovery/problem-framing"]["revision"],
                problem_after)
            self.assertEqual(len(state["gate_rejections"]["define"]), 1)

    def test_a_rejected_gate_result_carries_the_message(self):
        outcome = TurnOutcome("rejected", "5:abc", bank_id="discover",
                              message="gate rejected by local-reviewer; the bank stays open until its current revisions are approved")
        result = _gate_result(outcome, "checkout")
        self.assertFalse(result["ok"])
        self.assertTrue(result["rejection_recorded"])
        self.assertEqual(result["error"], outcome.message)

    def test_a_blank_workspace_reaches_completed_through_the_cli_alone(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            for bank_id in ("discover", "define", "design", "build", "deliver", "operate"):
                status = self.answer_bank(folder, bank_id)
                self.assertEqual(status["interview"], "blocked")
                self.assertEqual(status["current_bank_id"], bank_id)
                proof_name = "gate-" + bank_id + ".txt"
                proof_bytes = bank_id.encode()
                Path(folder, proof_name).write_bytes(proof_bytes)
                evidence = {
                    "source": proof_name,
                    "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                    "actor_id": "local-reviewer",
                    "requester_id": "local-operator",
                    "decision": "approved",
                    "approved_at": "2026-09-04T00:00:00Z",
                }
                output = StringIO()
                with redirect_stdout(output):
                    rc = main(["gate", "--path", folder, "--product-id", "checkout",
                               "--bank-id", bank_id, "--evidence", json.dumps(evidence),
                               "--expected-revision", status["revision_token"],
                               "--turn-id", "gate-" + bank_id, "--json"])
                self.assertEqual(rc, 0)
                result = json.loads(output.getvalue())
                self.assertTrue(result["ok"])
                if bank_id == "operate":
                    self.assertEqual(result["outcome"]["status"], "completed")
                else:
                    self.assertEqual(result["outcome"]["status"], "advanced")
            final = self.status(folder)
            self.assertEqual(final["interview"], "completed")
            self.assertEqual(final["source_verified"] + final["supplied_unverified"], 54)

    def test_a_stale_gate_can_be_proved_again_through_the_cli(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            proof = Path(folder, "onboarding-approval.txt")

            def gate(data: bytes, turn_id: str, token: str) -> dict:
                proof.write_bytes(data)
                evidence = {"source": "onboarding-approval.txt", "source_sha256": hashlib.sha256(data).hexdigest(),
                            "actor_id": "local-reviewer", "requester_id": "local-operator", "decision": "approved",
                            "approved_at": "2026-09-04T00:00:00Z"}
                output = StringIO()
                with redirect_stdout(output):
                    main(["gate", "--path", folder, "--product-id", "checkout", "--bank-id", "discover",
                          "--evidence", json.dumps(evidence), "--expected-revision", token,
                          "--turn-id", turn_id, "--json"])
                return json.loads(output.getvalue())

            self.assertTrue(gate(b"reviewed onboarding evidence\n", "gate-1", status["revision_token"])["ok"])
            proof.write_bytes(b"changed after approval\n")
            stale = self.status(folder)
            self.assertEqual(stale["interview"], "stale")
            again = gate(b"re-reviewed onboarding evidence\n", "gate-2", stale["revision_token"])
            # Re-proving DISCOVER moves the interview on again; five banks are still to come.
            self.assertEqual((again["ok"], again["outcome"]["status"]), (True, "advanced"))
            self.assertEqual(self.status(folder)["interview"], "question")

    def test_gitignore_covers_pmos_runtime_and_sqlite_sidecars(self):
        """F07: .gitignore must ignore .pmos/ at any depth and SQLite sidecar
        files anywhere, so a routine git add never stages private answers or
        database state."""
        if shutil.which("git") is None:
            self.skipTest("git is not installed")
        repo_root = Path(__file__).resolve().parent.parent
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=str(repo_root), capture_output=True, check=True,
            )
        except (subprocess.CalledProcessError, OSError):
            self.skipTest("not a git work tree")
        ignored = [
            "my-product/.pmos/runtime.sqlite",
            ".pmos/runtime.sqlite",
            "a/b/.pmos/runtime.sqlite-wal",
            "products/demo/.pmos/runtime.sqlite",
            "x/runtime.sqlite-shm",
        ]
        for path in ignored:
            result = subprocess.run(
                ["git", "check-ignore", path],
                cwd=str(repo_root), capture_output=True,
            )
            self.assertEqual(result.returncode, 0,
                             "expected %s to be ignored" % path)
        result = subprocess.run(
            ["git", "check-ignore", "pmos/cli.py"],
            cwd=str(repo_root), capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0,
                            "expected pmos/cli.py to not be ignored")

    def test_force_never_lets_init_overwrite_an_existing_product(self):
        """--force's help once promised the opposite of what it did: an
        existing product was always refused without --force, and --force's
        only real effect was to skip that refusal. It must always refuse."""
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            output = StringIO()
            with redirect_stdout(output):
                code = main(["init", "--path", folder, "--product-id", "checkout",
                            "--force", "--json"])
            self.assertEqual(code, 2)
            self.assertIn("already contains product", json.loads(output.getvalue())["error"])

    def test_force_after_an_accepted_answer_still_refuses_clearly(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                current = store.head("checkout").token
            valid = {"class": "observed_behavior", "source": "interview-001",
                     "date": "2026-09-04", "location": "customer-call"}
            self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                   "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                   "--evidence", json.dumps(valid), "--expected-revision", current,
                                   "--turn-id", "v1", "--json"]), 0)
            output = StringIO()
            with redirect_stdout(output):
                code = main(["init", "--path", folder, "--product-id", "checkout",
                            "--force", "--json"])
            self.assertEqual(code, 2)
            self.assertIn("already contains product", json.loads(output.getvalue())["error"])

    def test_a_new_product_id_still_initializes_in_an_existing_runtime(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.assertEqual(main(["init", "--path", folder, "--product-id", "billing"]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("billing").revision, 1)

    def test_user_supplied_evidence_flow_rejects_invalid_and_stale_submissions(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                initial = store.head("checkout").token
            invalid = {"class": "observed_behavior", "source": "real interview"}
            self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                   "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                   "--evidence", json.dumps(invalid), "--expected-revision", initial,
                                   "--turn-id", "invalid-v1", "--json"]), 1)
            valid = {"class": "observed_behavior", "source": "interview-001",
                     "date": "2026-09-04", "location": "customer-call"}
            # The invalid attempt advanced the durable revision; using the old
            # token must fail closed rather than overwrite the challenge.
            self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                   "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                   "--evidence", json.dumps(valid), "--expected-revision", initial,
                                   "--turn-id", "stale-v1", "--json"]), 1)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                current = store.head("checkout").token
            answer_output = StringIO()
            with redirect_stdout(answer_output):
                self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                       "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                       "--evidence", json.dumps(valid), "--expected-revision", current,
                                       "--turn-id", "valid-v1", "--json"]), 0)
            self.assertEqual(json.loads(answer_output.getvalue())["outcome"]["status"], "accepted")
            status = self.answer_bank(folder, "flow")
            proof_bytes = b"reviewed onboarding evidence\n"
            Path(folder, "onboarding-approval.txt").write_bytes(proof_bytes)
            gate_evidence = {
                "source": "onboarding-approval.txt",
                "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
                "actor_id": "local-reviewer",
                "requester_id": "local-operator",
                "decision": "approved",
                "approved_at": "2026-09-04T00:00:00Z",
            }
            gate_output = StringIO()
            with redirect_stdout(gate_output):
                self.assertEqual(main(["gate", "--path", folder, "--product-id", "checkout",
                                       "--bank-id", "discover", "--evidence",
                                       json.dumps(gate_evidence),
                                       "--expected-revision", status["revision_token"],
                                       "--turn-id", "gate-v1", "--json"]), 0)
            gated = json.loads(gate_output.getvalue())
            # A gate that moves the interview on is ok without completing it.
            self.assertEqual((gated["outcome"]["status"], gated["outcome"]["completed"]), ("advanced", False))

    def test_reopen_parked_question_then_answer_with_fresh_evidence(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)

            def token() -> str:
                # The current revision token, taken from `pmos status`, which
                # now prints a ready-made revision_token field so a caller never
                # composes <revision>:<commit_hash> by hand (F11).
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(main(["--json", "status", "--path", folder, "--product-id", "checkout"]), 0)
                return json.loads(output.getvalue())["revision_token"]

            invalid = {"class": "observed_behavior", "source": "real interview"}
            for label in ("bad1", "bad2", "bad3"):
                self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                       "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                       "--evidence", json.dumps(invalid),
                                       "--expected-revision", token(), "--turn-id", label, "--json"]), 1)
            reopen_args = ["reopen", "--path", folder, "--product-id", "checkout",
                           "--question-id", "DISCOVER-1", "--reason", "found the call recording",
                           "--expected-revision", token(), "--turn-id", "reopen-1", "--json"]
            reopen_output = StringIO()
            with redirect_stdout(reopen_output):
                self.assertEqual(main(reopen_args), 0)
            reopened = json.loads(reopen_output.getvalue())
            self.assertEqual((reopened["ok"], reopened["outcome"]["status"]), (True, "reopened"))
            self.assertEqual(reopened["outcome"]["question"]["id"], "DISCOVER-1")
            valid = {"class": "observed_behavior", "source": "interview-001",
                     "date": "2026-09-04", "location": "customer-call"}
            answer_output = StringIO()
            with redirect_stdout(answer_output):
                self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                       "--question-id", "DISCOVER-1", "--answer", "A real outcome",
                                       "--evidence", json.dumps(valid),
                                       "--expected-revision", reopened["outcome"]["revision"],
                                       "--turn-id", "good-after-reopen", "--json"]), 0)
            self.assertEqual(json.loads(answer_output.getvalue())["outcome"]["status"], "accepted")
            # Replaying the reopen turn returns its recorded outcome; only the
            # revision differs, because a replay reports the current head.
            replay_output = StringIO()
            with redirect_stdout(replay_output):
                self.assertEqual(main(reopen_args), 0)
            replayed = json.loads(replay_output.getvalue())["outcome"]
            self.assertEqual({key: value for key, value in replayed.items() if key != "revision"},
                             {key: value for key, value in reopened["outcome"].items() if key != "revision"})
            # A new reopen still carrying the parked-time revision is stale now.
            stale_output = StringIO()
            with redirect_stdout(stale_output):
                self.assertEqual(main(reopen_args[:-3] + ["--turn-id", "reopen-stale", "--json"]), 1)
            self.assertEqual(json.loads(stale_output.getvalue())["outcome"]["status"], "conflict")

    def test_export_out_existing_file_is_rejected_cleanly(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as out_parent:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            out_file = Path(out_parent) / "archive-file"
            out_file.write_text("nope", encoding="utf-8")
            rc, result = self.export(folder, str(out_file))
            self.assertEqual(rc, 2)
            self.assertIn("--out", result["error"])
            self.assertNotIn("Errno", result["error"])

    def test_answer_refusal_hint_names_answer_help(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.status(folder)
            answer_args = [
                "answer", "--path", folder, "--product-id", "checkout",
                "--question-id", "DISCOVER-1", "--answer", "x",
                "--evidence", "{not-json",
                "--expected-revision", status["revision_token"],
                "--turn-id", "answer-bad-evidence", "--json",
            ]
            output = StringIO()
            with redirect_stdout(output):
                rc = main(answer_args)
            self.assertEqual(rc, 2)
            payload = json.loads(output.getvalue())
            self.assertFalse(payload["ok"])
            self.assertIn("pmos answer --help", payload["hint"])

    def test_actionable_missing_runtime_error_is_json(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["status", "--path", folder, "--json"]), 2)
            runtime = Path(folder) / ".pmos/runtime.sqlite"
            runtime.parent.mkdir()
            runtime.write_bytes(b"not sqlite")
            self.assertEqual(main(["verify", "--path", folder, "--json"]), 2)

    def test_runtime_directory_symlink_never_escapes_workspace(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            root = Path(folder) / "workspace"
            root.mkdir()
            target = Path(outside)
            (root / ".pmos").symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(Exception, "runtime directory must not be a symlink"):
                _paths(root)
            self.assertEqual(main([
                "init", "--path", str(root), "--product-id", "checkout", "--json",
            ]), 2)
            self.assertFalse((target / "runtime.sqlite").exists())

    def test_runtime_database_symlink_never_escapes_workspace(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            root = Path(folder) / "workspace"
            root.mkdir()
            runtime = root / ".pmos"
            runtime.mkdir()
            external = Path(outside) / "runtime.sqlite"
            with Store(external) as store:
                store.create_product("outside")
            (runtime / "runtime.sqlite").symlink_to(external)
            with self.assertRaisesRegex(Exception, "runtime database must not be a symlink"):
                _paths(root)
            self.assertEqual(main([
                "status", "--path", str(root), "--product-id", "outside", "--json",
            ]), 2)

    def test_gate_source_verifier_rejects_escape_symlink_and_hash_drift(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            root = Path(folder)
            proof = root / "evidence" / "approval.txt"
            proof.parent.mkdir()
            proof.write_bytes(b"approved\n")
            digest = hashlib.sha256(proof.read_bytes()).hexdigest()
            verify = _local_gate_verifier(root)
            self.assertTrue(verify("evidence/approval.txt", digest))
            self.assertFalse(verify("evidence/approval.txt", "0" * 64))
            external = Path(outside) / "external.txt"
            external.write_bytes(b"approved\n")
            self.assertFalse(verify(str(external), digest))
            self.assertFalse(verify("../external.txt", digest))
            link = root / "evidence" / "link.txt"
            link.symlink_to(external)
            self.assertFalse(verify("evidence/link.txt", digest))

    def test_migration_dry_run_backup_atomic_activation_and_rollback(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            destination = root / "product"
            legacy = root / "legacy"
            self.assertEqual(main(["init", "--path", str(destination), "--product-id", "checkout"]), 0)
            create_legacy_fixture(legacy)
            planned = migrate_workspace(legacy, destination, product_id="checkout", dry_run=True)
            self.assertTrue(planned.ok)
            self.assertFalse((destination / ".pmos/migration.json").exists())
            migrated = migrate_workspace(legacy, destination, product_id="checkout")
            self.assertTrue(migrated.ok)
            self.assertIsNotNone(migrated.backup)
            with Store(destination / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.read_file("checkout", "STATE.md").splitlines()[0], b"# Legacy state")
            restored = rollback_workspace(destination)
            self.assertTrue(restored.ok)
            with Store(destination / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("checkout").revision, 1)

            fresh = root / "fresh"
            create_legacy_fixture(fresh)
            with self.assertRaises(MigrationError):
                migrate_workspace(fresh, fresh, fault_injector=lambda point:
                                  (_ for _ in ()).throw(RuntimeError("after activate"))
                                  if point == "after_activate" else None)
            self.assertFalse((fresh / ".pmos/runtime.sqlite").exists())
            fresh_journal = json.loads((fresh / ".pmos/migration-journal.json").read_text(encoding="utf-8"))
            self.assertEqual(fresh_journal["state"], "aborted")
            self.assertEqual(fresh_journal["recovery_action"], "quarantined_runtime")

            def fail(point):
                if point == "before_activate":
                    raise RuntimeError("injected activation failure")

            with self.assertRaises(MigrationError):
                migrate_workspace(legacy, destination, product_id="checkout", fault_injector=fail)
            with Store(destination / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("checkout").revision, 1)
            existing_journal = json.loads((destination / ".pmos/migration-journal.json").read_text(encoding="utf-8"))
            self.assertEqual(existing_journal["state"], "prepared")

    def test_destination_migration_lock_rejects_overlapping_activation_and_preserves_manifest_hash(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / "legacy"
            destination = root / "product"
            create_legacy_fixture(legacy)
            reached_activation = threading.Event()
            release_activation = threading.Event()
            first_result = []
            first_error = []

            def pause_before_activation(point):
                if point == "before_activate":
                    reached_activation.set()
                    if not release_activation.wait(3):
                        raise RuntimeError("test did not release migration lock")

            def first_migration():
                try:
                    first_result.append(migrate_workspace(
                        legacy, destination, product_id="checkout", fault_injector=pause_before_activation))
                except Exception as exc:  # pragma: no cover - asserted below
                    first_error.append(exc)

            worker = threading.Thread(target=first_migration)
            worker.start()
            self.assertTrue(reached_activation.wait(3), "first migration never acquired the destination lock")
            try:
                with patch.object(migrations, "MIGRATION_LOCK_TIMEOUT_SECONDS", 0.1):
                    with self.assertRaisesRegex(MigrationError, "destination is busy"):
                        migrate_workspace(legacy, destination, product_id="checkout")
            finally:
                release_activation.set()
            worker.join(3)
            self.assertFalse(worker.is_alive(), "first migration did not finish")
            self.assertEqual(first_error, [])
            self.assertEqual(len(first_result), 1)
            self.assertEqual(first_result[0].status, "migrated")
            runtime = destination / ".pmos/runtime.sqlite"
            manifest = json.loads((destination / ".pmos/migration.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["activated_sha256"], hashlib.sha256(runtime.read_bytes()).hexdigest())

    def test_destination_migration_lock_rejects_symlink_lock_file(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            root = Path(folder)
            legacy = root / "legacy"
            destination = root / "product"
            create_legacy_fixture(legacy)
            lock = destination / ".pmos/migration.lock"
            lock.parent.mkdir(parents=True)
            external = Path(outside) / "not-a-lock"
            external.write_bytes(b"unchanged\n")
            lock.symlink_to(external)
            with self.assertRaisesRegex(MigrationError, "safe destination migration lock"):
                migrate_workspace(legacy, destination, product_id="checkout")
            self.assertEqual(external.read_bytes(), b"unchanged\n")

    def test_destination_migration_lock_rejects_runtime_directory_swap(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = create_legacy_fixture(root / "legacy")
            destination = root / "product"
            outside = root / "outside"

            def swap_runtime_directory(point):
                if point != "before_activate":
                    return
                runtime_dir = destination / ".pmos"
                staged = root / "staged-pmos"
                runtime_dir.rename(staged)
                temporary = next(path for path in staged.glob("runtime.sqlite.migration-*")
                                 if not path.name.endswith(("-wal", "-shm")))
                outside.mkdir()
                runtime_dir.symlink_to(outside, target_is_directory=True)
                temporary.rename(outside / temporary.name)

            with self.assertRaisesRegex(MigrationError, "runtime directory changed while locked"):
                migrate_workspace(legacy, destination, product_id="checkout",
                                  fault_injector=swap_runtime_directory)
            self.assertTrue((destination / ".pmos").is_symlink())
            self.assertFalse((outside / "runtime.sqlite").exists())
            self.assertFalse((outside / "migration.json").exists())

    def test_destination_migration_lock_rejects_whole_destination_swap(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = create_legacy_fixture(root / "legacy")
            destination = root / "product"
            staged = root / "staged-product"
            replacement = root / "replacement"

            def swap_destination(point):
                if point == "before_activate":
                    destination.rename(staged)
                    replacement.mkdir()
                    destination.symlink_to(replacement, target_is_directory=True)

            with self.assertRaisesRegex(MigrationError, "destination changed while locked"):
                migrate_workspace(legacy, destination, product_id="checkout",
                                  fault_injector=swap_destination)
            self.assertFalse((replacement / ".pmos/runtime.sqlite").exists())

    def test_recovery_rejects_symlinked_migration_journal(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = create_legacy_fixture(root / "legacy")
            destination = root / "product"
            migrate_workspace(legacy, destination, product_id="checkout")
            journal = destination / ".pmos/migration-journal.json"
            external = root / "external-journal.json"
            external.write_bytes(journal.read_bytes())
            original_external = external.read_bytes()
            journal.unlink()
            journal.symlink_to(external)
            with self.assertRaisesRegex(MigrationError, "migration journal is not a safe regular file"):
                recover_workspace(destination)
            self.assertTrue(journal.is_symlink())
            self.assertEqual(external.read_bytes(), original_external)

    def test_recovery_rejects_migration_journal_swapped_during_read(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = create_legacy_fixture(root / "legacy")
            destination = root / "product"
            migrate_workspace(legacy, destination, product_id="checkout")
            journal = destination / ".pmos/migration-journal.json"
            original = journal.with_name("original-journal.json")
            external = root / "external-journal.json"
            external.write_bytes(journal.read_bytes())
            external_before = external.read_bytes()
            real_open = os.open
            swapped = False

            def swap_before_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if (not swapped and
                        os.fspath(path).endswith("/.pmos/migration-journal.json")):
                    journal.rename(original)
                    journal.symlink_to(external)
                    swapped = True
                return real_open(path, flags, *args, **kwargs)

            with patch.object(migrations.os, "open", side_effect=swap_before_open):
                with self.assertRaisesRegex(MigrationError, "migration journal is missing or invalid"):
                    recover_workspace(destination)
            self.assertTrue(swapped)
            self.assertTrue(journal.is_symlink())
            self.assertEqual(external.read_bytes(), external_before)

    def test_atomic_json_completes_a_write_split_into_short_chunks(self):
        """os.write() may write fewer bytes than given without raising;
        _atomic_json must keep writing until every byte lands rather than
        trust one call."""
        real_write = migrations.os.write

        def short_write(descriptor, payload):
            return real_write(descriptor, payload[:7])

        with TemporaryDirectory() as folder:
            target = Path(folder) / "migration-journal.json"
            value = {"state": "recovery_required", "note": "x" * 200}
            with patch.object(migrations.os, "write", side_effect=short_write):
                migrations._atomic_json(target, value)
            self.assertEqual(migrations._read_json(target), value)

    def test_atomic_json_leaves_the_previous_journal_untouched_on_failure(self):
        """A short write followed by a real failure (disk full) must not
        replace a valid control file with truncated JSON, and must not
        leave a temporary behind that blocks the next attempt."""
        real_write = migrations.os.write

        with TemporaryDirectory() as folder:
            target = Path(folder) / "migration-journal.json"
            first = {"state": "in_progress", "note": "original"}
            migrations._atomic_json(target, first)
            original_bytes = target.read_bytes()

            calls = []

            def short_then_fail(descriptor, payload):
                calls.append(payload)
                if len(calls) == 1:
                    return real_write(descriptor, payload[:8])
                raise OSError(28, "No space left on device")

            second = {"state": "aborted", "note": "y" * 200}
            with patch.object(migrations.os, "write", side_effect=short_then_fail):
                with self.assertRaises(OSError):
                    migrations._atomic_json(target, second)

            self.assertEqual(target.read_bytes(), original_bytes,
                             "a failed write replaced the previous valid journal")
            leftovers = [item.name for item in target.parent.iterdir()
                        if ".tmp-" in item.name]
            self.assertEqual([], leftovers, "a failed write left a temporary behind")
            self.assertEqual(migrations._read_json(target), first)

            # The failed attempt must not block the very next one.
            migrations._atomic_json(target, second)
            self.assertEqual(migrations._read_json(target), second)

    def test_rollback_rejects_runtime_directory_swap_and_symlinked_manifest(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = create_legacy_fixture(root / "legacy")
            destination = root / "product"
            self.assertEqual(main(["init", "--path", str(destination),
                                   "--product-id", "checkout"]), 0)
            migrate_workspace(legacy, destination, product_id="checkout")
            manifest = destination / ".pmos/migration.json"
            external_manifest = root / "external-manifest.json"
            external_manifest.write_bytes(manifest.read_bytes())
            manifest.unlink()
            manifest.symlink_to(external_manifest)
            with self.assertRaisesRegex(MigrationError, "migration manifest is not a safe regular file"):
                rollback_workspace(destination)
            manifest.unlink()
            manifest.write_bytes(external_manifest.read_bytes())

            outside = root / "outside"

            def swap_runtime_directory(point):
                if point != "before_activate":
                    return
                runtime_dir = destination / ".pmos"
                staged = root / "staged-pmos"
                runtime_dir.rename(staged)
                temporary = next(path for path in staged.glob("runtime.sqlite.rollback-*")
                                 if not path.name.endswith(("-wal", "-shm")))
                outside.mkdir()
                runtime_dir.symlink_to(outside, target_is_directory=True)
                (staged / "runtime.sqlite").rename(outside / "runtime.sqlite")
                temporary.rename(outside / temporary.name)

            with self.assertRaisesRegex(MigrationError, "runtime directory changed while locked"):
                rollback_workspace(destination, fault_injector=swap_runtime_directory)
            self.assertFalse((outside / "migration.json").exists())

    def test_recover_finalizes_sigkill_after_replace_existing_and_fresh(self):
        script = (
            "import os,signal,sys\n"
            "from pmos.migrations import migrate_workspace\n"
            "def kill(point):\n"
            "    if point in ('after_replace','after_activate'): os.kill(os.getpid(), signal.SIGKILL)\n"
            "migrate_workspace(sys.argv[1], sys.argv[2], product_id=sys.argv[3], fault_injector=kill)"
        )
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / "legacy"
            create_legacy_fixture(legacy)
            existing = root / "existing"
            self.assertEqual(main(["init", "--path", str(existing), "--product-id", "checkout"]), 0)
            for source, destination, product_id in ((legacy, existing, "checkout"),
                                                     (legacy, root / "fresh", "fresh")):
                completed = subprocess.run(
                    [sys.executable, "-c", script, str(source), str(destination), product_id],
                    cwd=str(Path(__file__).resolve().parent.parent), shell=False,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
                self.assertEqual(completed.returncode, -signal.SIGKILL,
                                 completed.stdout + completed.stderr)
                self.assertFalse((destination / ".pmos/migration.json").exists())
                self.assertTrue((destination / ".pmos/migration-journal.json").exists())
                recovery_output = StringIO()
                with redirect_stdout(recovery_output):
                    self.assertEqual(main(["recover", str(destination), "--json"]), 0)
                self.assertEqual(json.loads(recovery_output.getvalue())["status"], "recovered")
                self.assertTrue((destination / ".pmos/migration.json").exists())
                # Recovery is idempotent and should not create a second state.
                self.assertEqual(recover_workspace(destination).status, "recovered")
                with Store(destination / ".pmos/runtime.sqlite") as store:
                    self.assertEqual(store.read_file(product_id, "STATE.md").splitlines()[0], b"# Legacy state")

    def test_recover_finalizes_sigkill_after_rollback_activation(self):
        script = (
            "import os,signal,sys\n"
            "from pmos.migrations import rollback_workspace\n"
            "def kill(point):\n"
            "    if point == 'after_activate': os.kill(os.getpid(), signal.SIGKILL)\n"
            "rollback_workspace(sys.argv[1], fault_injector=kill)"
        )
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / "legacy"
            destination = root / "product"
            create_legacy_fixture(legacy)
            self.assertEqual(main(["init", "--path", str(destination), "--product-id", "checkout"]), 0)
            migrate_workspace(legacy, destination, product_id="checkout")
            runtime = destination / ".pmos/runtime.sqlite"
            migrated_hash = hashlib.sha256(runtime.read_bytes()).hexdigest()
            completed = subprocess.run(
                [sys.executable, "-c", script, str(destination)],
                cwd=str(Path(__file__).resolve().parent.parent), shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            self.assertEqual(completed.returncode, -signal.SIGKILL,
                             completed.stdout + completed.stderr)
            pending = json.loads((destination / ".pmos/migration-journal.json").read_text(encoding="utf-8"))
            self.assertEqual(pending["state"], "rollback_prepared")
            self.assertEqual(pending["rollback_from_sha256"], migrated_hash)
            # Recovery must close the replacement instead of incorrectly
            # accepting the preceding finalized migration state.
            recovery_output = StringIO()
            with redirect_stdout(recovery_output):
                self.assertEqual(main(["recover", str(destination), "--json"]), 0)
            recovered = json.loads(recovery_output.getvalue())
            self.assertEqual(recovered["status"], "rolled_back")
            self.assertTrue(recovered["ok"])
            manifest = json.loads((destination / ".pmos/migration.json").read_text(encoding="utf-8"))
            restored_hash = hashlib.sha256(runtime.read_bytes()).hexdigest()
            self.assertEqual(manifest["status"], "rolled_back")
            self.assertEqual(manifest["activated_sha256"], restored_hash)
            self.assertEqual(manifest["rollback_from_sha256"], migrated_hash)
            self.assertEqual(recover_workspace(destination).status, "rolled_back")
            self.assertEqual(rollback_workspace(destination).status, "rolled_back")
            with Store(runtime) as store:
                self.assertEqual(store.head("checkout").revision, 1)

    def test_planned_file_symlink_swap_and_migration_limits_fail_closed(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            root = Path(folder)
            legacy = root / "legacy"
            create_legacy_fixture(legacy)
            plan = migrations.plan_workspace(legacy, root / "destination", product_id="safe")
            external = Path(outside) / "hosts"
            external.write_bytes(b"do not import\n")
            target = legacy / "STATE.md"
            target.unlink()
            target.symlink_to(external)
            with self.assertRaises(MigrationError):
                migrate_workspace(legacy, root / "destination", product_id="safe", plan=plan)

            bounded = root / "bounded"
            bounded.mkdir()
            (bounded / "large.txt").write_bytes(b"12345")
            with patch.object(migrations, "MAX_FILE_BYTES", 4):
                with self.assertRaises(MigrationError):
                    migrations.plan_workspace(bounded)

            many = root / "many"
            many.mkdir()
            for index in range(3):
                (many / ("file-%d.txt" % index)).write_text("x", encoding="utf-8")
            with patch.object(migrations, "MAX_MIGRATION_FILES", 2):
                with self.assertRaises(MigrationError):
                    migrations.plan_workspace(many)

    def test_recovery_and_rollback_refuse_unknown_active_runtime(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / "legacy"
            destination = root / "product"
            create_legacy_fixture(legacy)
            self.assertEqual(main(["init", "--path", str(destination),
                                   "--product-id", "checkout"]), 0)
            migrate_workspace(legacy, destination, product_id="checkout")
            runtime = destination / ".pmos/runtime.sqlite"
            with Store(runtime) as store:
                snapshot = store.read_snapshot("checkout")
                changed = dict(snapshot.files)
                changed["post-migration.txt"] = b"newer operator state\n"
                store.commit("checkout", changed, expected_revision=snapshot.head.revision)
                expected_revision = snapshot.head.revision + 1

            with self.assertRaises(MigrationError):
                rollback_workspace(destination)
            # A finalized migration journal is not sufficient evidence on its
            # own: recovery must notice a later active runtime rather than
            # returning a false green "already finalized" result.
            with self.assertRaises(MigrationError):
                recover_workspace(destination)
            with Store(runtime) as store:
                self.assertEqual(store.head("checkout").revision, expected_revision)

            journal_path = destination / ".pmos/migration-journal.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["state"] = "prepared"
            journal_path.write_text(json.dumps(journal), encoding="utf-8")
            with self.assertRaises(MigrationError):
                recover_workspace(destination)
            with Store(runtime) as store:
                self.assertEqual(store.head("checkout").revision, expected_revision)

    def test_isolated_install_imports_console_script(self):
        interpreter = sys.executable if sys.version_info >= (3, 11) else shutil.which("python3.11")
        if not interpreter:
            self.fail("Python >=3.11 is required for the isolated install contract")
        with TemporaryDirectory() as folder:
            folder_path = Path(folder)
            target = folder_path / "target"
            target.mkdir()
            package_copy = folder_path / "package"
            wheelhouse = folder_path / "wheelhouse"
            wheelhouse.mkdir()
            shutil.copytree(
                Path(__file__).resolve().parent.parent, package_copy,
                ignore=shutil.ignore_patterns(
                    ".git", "build", "*.egg-info", "__pycache__", ".pytest_cache", ".venv"))
            # Exercise the real isolated PEP 517 path with no package index.
            # The repository-local backend has no build dependencies, so this
            # must work in a clean interpreter rather than relying on a cache.
            built = subprocess.run(
                [interpreter, "-m", "pip", "wheel", "--no-index", "--no-deps",
                 "--wheel-dir", str(wheelhouse), str(package_copy)],
                cwd=str(package_copy), shell=False, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, timeout=60)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            wheels = sorted(wheelhouse.glob("product_manager_os-*.whl"))
            self.assertEqual(len(wheels), 1, built.stdout + built.stderr)
            completed = subprocess.run(
                [interpreter, "-m", "pip", "install", "--no-index", "--no-deps",
                 "--target", str(target), str(wheels[0])],
                cwd=str(package_copy), shell=False, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, timeout=60)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            env = dict(os.environ)
            env["PYTHONPATH"] = str(target)
            result = subprocess.run([interpreter, "-m", "pmos.cli", "--help"],
                                    env=env, shell=False, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Product Manager OS", result.stdout)
            skills = subprocess.run(
                [interpreter, "-c",
                 "from pmos.skills import SkillRegistry; "
                 "r=SkillRegistry(); print(','.join(r.load()))"],
                cwd=str(folder_path), env=env, shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, timeout=20)
            self.assertEqual(skills.returncode, 0, skills.stderr)
            self.assertEqual(len(skills.stdout.strip().split(",")), 7)
            banks = subprocess.run(
                [interpreter, "-c",
                 "from pmos.banks import shipped_banks; "
                 "print(','.join(bank.id for bank in shipped_banks()))"],
                cwd=str(folder_path), env=env, shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, timeout=20)
            self.assertEqual(banks.returncode, 0, banks.stderr)
            self.assertEqual(banks.stdout.strip(),
                             "discover,define,design,build,deliver,operate")

    def test_handoff_right_after_init_is_not_ready_but_still_writes_both_files(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            token = self.status(folder)["revision_token"]
            rc, result = self.handoff(folder)
            self.assertEqual(rc, 1)
            self.assertFalse(result["ok"])
            self.assertFalse(result["development_ready"])
            self.assertTrue(any("development-handoff.md" in reason for reason in result["missing"]))
            index_path = Path(folder, "handoff/context-index.json")
            context_path = Path(folder, "handoff/CONTEXT.md")
            self.assertTrue(index_path.is_file())
            self.assertTrue(context_path.is_file())
            index = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual(index["source_revision"], token)

    def test_handoff_context_md_names_local_attestation_only_after_an_approval(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.handoff(folder)
            before = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("Development-ready: no", before)
            self.assertNotIn("local attestation", before)

            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))

            self.handoff(folder)
            after = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("Development-ready: no", after)
            self.assertIn("Gate 1", after)
            self.assertIn("local attestation", after)

    def test_handoff_changes_no_store_revision(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            before = self.status(folder)["revision_token"]
            rc, result = self.handoff(folder)
            self.assertEqual(rc, 1)
            after = self.status(folder)["revision_token"]
            self.assertEqual(before, after)

    def test_handoff_context_md_rewrites_a_section_link_relative_to_the_handoff_folder(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            design_path = Path(folder, "design/api-contract.md")
            design_path.parent.mkdir(parents=True, exist_ok=True)
            design_path.write_text("# API contract\n", encoding="utf-8")
            self.write_artifact(folder, "development-handoff.md", "checkout/development-handoff",
                                "ALL STAGES", 1, [], "templates/architecture/development-handoff.md",
                                "## 1. Problem\n[API contract](design/api-contract.md)\n")
            self.handoff(folder)
            context = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            # The link target sits at root/design/api-contract.md, one level
            # below root; from root/handoff/ that is reached by stepping up
            # first, so the rendered link must carry the brief's '../' prefix
            # rather than the root-relative 'design/api-contract.md'.
            self.assertIn("../design/api-contract.md", context)
            self.assertNotIn("(design/api-contract.md)", context)

    def test_handoff_symlinked_handoff_directory_never_escapes_workspace(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            target = Path(outside)
            Path(folder, "handoff").symlink_to(target, target_is_directory=True)
            self.assertEqual(main(["handoff", "--path", folder, "--product-id", "checkout", "--json"]), 2)
            self.assertFalse((target / "context-index.json").exists())
            self.assertFalse((target / "CONTEXT.md").exists())

    def test_handoff_symlinked_context_index_never_escapes_workspace(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            handoff_dir = Path(folder, "handoff")
            handoff_dir.mkdir()
            external = Path(outside, "context-index.json")
            external.write_text("untouched\n", encoding="utf-8")
            (handoff_dir / "context-index.json").symlink_to(external)
            self.assertEqual(main(["handoff", "--path", folder, "--product-id", "checkout", "--json"]), 2)
            self.assertEqual(external.read_text(encoding="utf-8"), "untouched\n")

    def test_unsupported_platform_fails_fast_with_one_line_message_and_exit_code(self):
        # F33: an unsupported platform must refuse before any command runs, with
        # one clear stderr line and a documented exit code -- never a raw
        # OSError/NotImplementedError from inside a dir_fd-relative call.
        with TemporaryDirectory() as folder:
            root = Path(folder) / "workspace"
            out, err = StringIO(), StringIO()
            with patch("pmos.cli._unsupported_platform_reason",
                      return_value="dir_fd-relative filesystem operations (os.supports_dir_fd)"):
                with redirect_stdout(out), redirect_stderr(err):
                    code = main(["init", "--path", str(root), "--product-id", "checkout"])
            self.assertEqual(code, UNSUPPORTED_PLATFORM_EXIT_CODE)
            self.assertEqual(code, 3)
            self.assertEqual(
                err.getvalue(),
                "pmos: unsupported platform, missing dir_fd-relative filesystem "
                "operations (os.supports_dir_fd); see docs/COMPATIBILITY.md\n")
            self.assertEqual(out.getvalue(), "")
            # The gate ran before `init` touched the filesystem at all: init's
            # first action is creating --path, and that never happened.
            self.assertFalse(root.exists())

    def test_unsupported_platform_emits_one_line_json_when_requested(self):
        with TemporaryDirectory() as folder:
            out, err = StringIO(), StringIO()
            with patch("pmos.cli._unsupported_platform_reason",
                      return_value="a working sqlite3 module"):
                with redirect_stdout(out), redirect_stderr(err):
                    code = main(["--json", "status", "--path", folder])
            self.assertEqual(code, UNSUPPORTED_PLATFORM_EXIT_CODE)
            self.assertEqual(err.getvalue(), "")
            payload = out.getvalue()
            self.assertEqual(payload.count("\n"), 1)
            self.assertEqual(
                json.loads(payload),
                {"ok": False,
                 "error": "pmos: unsupported platform, missing a working sqlite3 "
                          "module; see docs/COMPATIBILITY.md"})

    def test_supported_platform_takes_the_normal_path(self):
        # The real, unpatched probe must pass on the interpreter running this
        # suite (every CI and local platform this repository claims to run on).
        self.assertIsNone(_unsupported_platform_reason())
        # And explicitly patched to "supported", ordinary dispatch is unchanged.
        with TemporaryDirectory() as folder:
            with patch("pmos.cli._unsupported_platform_reason", return_value=None):
                self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
                self.assertEqual(main(["--json", "status", "--path", folder]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("checkout").revision, 1)


    # ------------------------------ reconcile (F01) ------------------------------

    def test_reconcile_on_a_freshly_initialized_product_has_nothing_pending(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            head_before = self.head(folder)
            report = self.reconcile(folder)
            head_after = self.head(folder)
            self.assertEqual(head_before, head_after)
            self.assertEqual(report["schema"], "pmos.reconcile.v1")
            self.assertTrue(report["read_only"])
            self.assertEqual((report["pending"], report["conflicts"], report["ok"]), ([], [], True))

    def test_reconcile_shows_a_pending_proposal_and_re_proving_clears_it(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            path = self.write_artifact(folder, "discovery/problem-framing.md",
                                       "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                       "templates/discovery/problem-framing.md", "A real outcome")
            reviewed = artifact_revision(path.read_text(encoding="utf-8"))
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            clean = self.reconcile(folder)
            self.assertEqual((clean["pending"], clean["conflicts"], clean["ok"]), ([], [], True))
            # A direct edit outside `pmos answer`/`pmos gate` is a pending
            # proposal, not an accepted change; reconcile writes nothing.
            head_before = self.head(folder)
            path = self.write_artifact(folder, "discovery/problem-framing.md",
                                       "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                       "templates/discovery/problem-framing.md", "A changed outcome")
            current = artifact_revision(path.read_text(encoding="utf-8"))
            report = self.reconcile(folder)
            head_after = self.head(folder)
            self.assertEqual(head_before, head_after)
            self.assertTrue(report["read_only"])
            self.assertFalse(report["ok"])
            self.assertEqual(report["conflicts"], [])
            (pending,) = report["pending"]
            self.assertEqual(pending["id"], "checkout/discovery/problem-framing")
            self.assertEqual(pending["path"], "discovery/problem-framing.md")
            self.assertEqual(pending["accepted_revision"], reviewed)
            self.assertEqual(pending["current_revision"], current)
            self.assertEqual(pending["stales_gates"], ["discover"])
            self.assertEqual(pending["reconcile_dependents"], [])
            (action,) = pending["next_action"]
            self.assertEqual(action["bank_id"], "discover")
            self.assertIn("pmos gate", action["command"])
            self.assertIn("--bank-id discover", action["command"])
            # Accepting the proposal happens only by re-proving the gate
            # through the existing shared command, never through reconcile.
            status = self.status(folder)
            rc, parsed = self.gate(folder, status["revision_token"], "gate-2", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            cleared = self.reconcile(folder)
            self.assertEqual((cleared["pending"], cleared["conflicts"], cleared["ok"]), ([], [], True))

    def test_reconcile_names_dependents_that_need_reconciliation(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual(rc, 0)
            self.write_artifact(folder, "planning/vision.md", "checkout/planning/vision", "PLANNING", 2,
                                ["checkout/discovery/problem-framing"], "templates/planning/vision.md",
                                "A vision")
            self.write_artifact(folder, "definition/prd.md", "checkout/definition/prd", "DEFINE", 2,
                                ["checkout/planning/vision"], "templates/definition/prd.md",
                                "A product brief")
            status = self.answer_bank(folder, "b")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-2", "approved", bank_id="define")
            self.assertEqual(rc, 0)
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A changed outcome")
            report = self.reconcile(folder)
            (pending,) = report["pending"]
            self.assertEqual(pending["id"], "checkout/discovery/problem-framing")
            self.assertEqual(pending["stales_gates"], ["discover", "define"])
            self.assertEqual(pending["reconcile_dependents"],
                             ["checkout/definition/prd", "checkout/planning/vision"])
            self.assertEqual({action["bank_id"] for action in pending["next_action"]},
                             {"discover", "define"})

    def test_reconcile_reports_a_missing_bound_artifact_as_a_conflict(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            path = self.write_artifact(folder, "discovery/problem-framing.md",
                                       "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                       "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            path.unlink()
            report = self.reconcile(folder)
            self.assertEqual(report["pending"], [])
            self.assertFalse(report["ok"])
            (conflict,) = report["conflicts"]
            self.assertEqual(conflict["kind"], "missing_artifact")
            self.assertEqual(conflict["id"], "checkout/discovery/problem-framing")
            self.assertEqual(conflict["path"], "discovery/problem-framing.md")

    def test_reconcile_reports_an_artifact_whose_id_changed_as_a_conflict(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual((rc, parsed["ok"]), (0, True))
            # The same file, but its own artifact_id field was edited: the id
            # the approval bound no longer resolves to any file at all.
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing-renamed", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            report = self.reconcile(folder)
            self.assertEqual(report["pending"], [])
            self.assertFalse(report["ok"])
            (conflict,) = report["conflicts"]
            self.assertEqual(conflict["kind"], "artifact_id_changed")
            self.assertEqual(conflict["bound_id"], "checkout/discovery/problem-framing")
            self.assertEqual(conflict["current_id"], "checkout/discovery/problem-framing-renamed")
            self.assertEqual(conflict["path"], "discovery/problem-framing.md")

    def test_reconcile_reports_two_artifacts_sharing_one_id_as_a_conflict(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.write_artifact(folder, "discovery/one.md", "checkout/discovery/dup", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "First")
            self.write_artifact(folder, "discovery/two.md", "checkout/discovery/dup", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "Second")
            report = self.reconcile(folder)
            self.assertEqual(report["pending"], [])
            self.assertFalse(report["ok"])
            (conflict,) = report["conflicts"]
            self.assertEqual(conflict["kind"], "duplicate_id")
            self.assertIn("checkout/discovery/dup", conflict["message"])

    def test_reconcile_reports_a_symlinked_artifact_as_a_conflict(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            target = self.write_artifact(folder, "discovery/problem-framing.md",
                                         "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                         "templates/discovery/problem-framing.md", "A real outcome")
            link = Path(folder, "discovery/problem-framing-link.md")
            os.symlink(target, link)
            report = self.reconcile(folder)
            self.assertEqual(report["pending"], [])
            self.assertFalse(report["ok"])
            (conflict,) = report["conflicts"]
            self.assertEqual(conflict["kind"], "symlinked_artifact")
            self.assertIn("symlink", conflict["message"])

    def test_reconcile_reports_an_unreadable_artifact_as_a_conflict(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            bad_dir = Path(folder, "discovery")
            bad_dir.mkdir(parents=True, exist_ok=True)
            (bad_dir / "bad.md").write_bytes(b"\xff\xfe not valid utf-8 \x00")
            report = self.reconcile(folder)
            self.assertEqual(report["pending"], [])
            self.assertFalse(report["ok"])
            (conflict,) = report["conflicts"]
            self.assertEqual(conflict["kind"], "unreadable_artifact")

    # ------------------------------ export (F34) ------------------------------

    def test_export_writes_a_portable_package_and_a_readable_index(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as out_parent:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.answer_bank(folder, "a")
            self.write_artifact(folder, "discovery/problem-framing.md",
                                "checkout/discovery/problem-framing", "DISCOVER", 1, [],
                                "templates/discovery/problem-framing.md", "A real outcome")
            rc, parsed = self.gate(folder, status["revision_token"], "gate-1", "approved")
            self.assertEqual(rc, 0)
            out_dir = str(Path(out_parent) / "archive")
            head_before = self.head(folder)
            rc, result = self.export(folder, out_dir)
            head_after = self.head(folder)
            self.assertEqual(rc, 0)
            # export is read-only on the store: only local files are written.
            self.assertEqual(head_before, head_after)
            self.assertTrue(result["ok"])
            self.assertEqual(result["source_revision"], head_after.token)
            package = json.loads(Path(out_dir, "export.json").read_text(encoding="utf-8"))
            self.assertEqual(package["schema"], "pmos.export.v1")
            self.assertEqual(package["product_id"], "checkout")
            self.assertEqual(package["source_revision"], head_after.token)
            (approval,) = package["approvals"]
            self.assertEqual(approval["bank_id"], "discover")
            self.assertEqual(approval["attestation"], "local")
            self.assertEqual(approval["manifest"]["artifacts"][0]["id"],
                             "checkout/discovery/problem-framing")
            self.assertIn("not an import", package["note"])
            self.assertTrue(package["interview"]["banks"]["discover"]["answers"])
            index = Path(out_dir, "EXPORT.md").read_text(encoding="utf-8")
            self.assertIn("Product: checkout", index)
            self.assertIn("not an import path", index)
            self.assertIn("discover", index)

    def test_export_refuses_to_overwrite_without_force_then_succeeds_with_it(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as out_parent:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            out_dir = str(Path(out_parent) / "archive")
            rc, result = self.export(folder, out_dir)
            self.assertEqual(rc, 0)
            first = Path(out_dir, "export.json").read_text(encoding="utf-8")
            rc, result = self.export(folder, out_dir)
            self.assertNotEqual(rc, 0)
            self.assertIn("--force", result["error"])
            self.assertEqual(Path(out_dir, "export.json").read_text(encoding="utf-8"), first)
            rc, result = self.export(folder, out_dir, force=True)
            self.assertEqual(rc, 0)
            self.assertTrue(result["ok"])

    # ------------------------------ capacity warning (F34) ------------------------------

    def test_status_capacity_warning_is_none_under_the_threshold(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            status = self.status(folder)
            self.assertIsNone(status["capacity_warning"])

    def test_status_reports_a_capacity_warning_past_80_percent_of_max_state_bytes(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.answer_bank(folder, "a")
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                raw = store.read_snapshot("checkout").files[STATE_PATH]
            size = len(raw)
            # 85% of a patched-small MAX_STATE_BYTES: over the 80% warning
            # threshold, under the hard bound _load() enforces.
            patched_max = int(size / 0.85)
            with patch("pmos.conductor.MAX_STATE_BYTES", patched_max):
                status = self.status(folder)
            warning = status["capacity_warning"]
            self.assertIsNotNone(warning)
            self.assertEqual(warning["size_bytes"], size)
            self.assertEqual(warning["limit_bytes"], patched_max)
            self.assertGreaterEqual(warning["percent_of_limit"], 80.0)
            self.assertIn("MAX_STATE_BYTES", warning["message"])
            self.assertIn("pmos export", warning["message"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
