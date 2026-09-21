"""Shared phase reporting over Conductor state and a pinned contract."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import unittest

from pmos.artifacts import artifact_revision, build_manifest, check_manifest
from pmos.conductor import Conductor
from pmos.phases import phase_report
from pmos.store import Store

from test_pmos_conductor import BANKS, GATE_HASH, artifact, commitment, gate_proof, observed


_PROBLEM_FRAMING_BLOCK = """---
artifact_id: discovery/problem-framing
phase: DISCOVER
gate: 1
status: draft
depends_on: []
template: templates/discovery/problem-framing.md
---
{body}
"""


def problem_framing_text(body: str) -> str:
    return _PROBLEM_FRAMING_BLOCK.format(body=body)


class PhaseReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.path = Path(self.temp.name) / "runtime.sqlite"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def opening(self) -> tuple[Store, Conductor]:
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        resolver = lambda source: source in ("session replay", "support export", "approval email")
        store = Store(self.path)
        conductor = Conductor(
            store,
            "payments",
            BANKS,
            gate_source_verifier=verifier,
            source_resolver=resolver,
        )
        return store, conductor

    def opening_with_switchable_verifier(self, switch: dict[str, bool]) -> tuple[Store, Conductor]:
        def verifier(source: str, digest: str) -> bool:
            return bool(switch.get("enabled", False)) and source == "gate-1.md" and digest == GATE_HASH
        resolver = lambda source: source in ("session replay", "support export", "approval email")
        store = Store(self.path)
        conductor = Conductor(
            store,
            "payments",
            BANKS,
            gate_source_verifier=verifier,
            source_resolver=resolver,
        )
        return store, conductor

    def opening_with_workspace(self, root: Path) -> tuple[Store, Conductor]:
        verifier = lambda source, digest: source == "gate-1.md" and digest == GATE_HASH
        resolver = lambda source: source in ("session replay", "support export", "approval email")
        gate_of = {"discover": 1, "define": 2}
        store = Store(self.path)
        conductor = Conductor(
            store,
            "payments",
            BANKS,
            gate_source_verifier=verifier,
            source_resolver=resolver,
            gate_manifest=lambda bank_id: build_manifest(root, gate_of[bank_id]),
            manifest_verifier=lambda manifest: check_manifest(root, manifest),
        )
        return store, conductor

    WORKSPACE_CONTRACT = {
        "banks": [
            {
                "id": "discover",
                "stage": "DISCOVER",
                "gate": 1,
                "gate_rendering": [
                    {
                        "line": "The person is named",
                        "evidenced_by": "discover.person",
                        "questions": ["discover.person"],
                    },
                    {
                        "line": "The cost is exported",
                        "evidenced_by": "discover.cost",
                        "questions": ["discover.cost"],
                    },
                ],
                "questions": [
                    {
                        "id": "discover.person",
                        "lands_in": "`discovery/problem-framing.md` section 6 and "
                                    "`discovery/personas.md` evidence block.",
                    },
                ],
            },
            {
                "id": "define",
                "stage": "DEFINE",
                "gate": 2,
                "gate_rendering": [
                    {
                        "line": "The sponsor is named",
                        "evidenced_by": "define.sponsor",
                        "questions": ["define.sponsor"],
                    }
                ],
            },
        ],
        "signoffs": {"1": ["Product owner"], "2": ["Sponsor"]},
    }

    CONTRACT = {
        "banks": [
            {
                "id": "discover",
                "stage": "DISCOVER",
                "gate": 1,
                "gate_rendering": [
                    {
                        "line": "The person is named",
                        "evidenced_by": "discover.person",
                        "questions": ["discover.person"],
                    },
                    {
                        "line": "The cost is exported",
                        "evidenced_by": "discover.cost",
                        "questions": ["discover.cost"],
                    },
                ],
            },
            {
                "id": "define",
                "stage": "DEFINE",
                "gate": 2,
                "gate_rendering": [
                    {
                        "line": "The sponsor is named",
                        "evidenced_by": "define.sponsor",
                        "questions": ["define.sponsor"],
                    }
                ],
            },
        ],
        "signoffs": {"1": ["Product owner"], "2": ["Sponsor"]},
    }

    def test_fresh_product_report(self) -> None:
        store, conductor = self.opening()
        report = phase_report(conductor, self.CONTRACT, self.path)
        discover, define = report

        self.assertEqual(discover["state"], "in_progress")
        self.assertEqual(discover["next_action"], {
            "action": "answer",
            "bank_id": "discover",
            "question_id": "discover.person",
        })
        self.assertEqual(discover["missing"]["questions"], ["discover.person", "discover.cost"])
        self.assertEqual(discover["missing"]["gate_lines"], [
            "The person is named", "The cost is exported",
        ])
        self.assertEqual(discover["outcomes"], [
            {
                "line": "The person is named",
                "evidenced_by": "discover.person",
                "questions": ["discover.person"],
                "met": False,
                "answered_in": {"discover.person": "discover"},
                "carried": [],
            },
            {
                "line": "The cost is exported",
                "evidenced_by": "discover.cost",
                "questions": ["discover.cost"],
                "met": False,
                "answered_in": {"discover.cost": "discover"},
                "carried": [],
            },
        ])
        self.assertEqual(discover["completed"], {
            "questions": [],
            "source_verified": 0,
            "quote_verified": 0,
            "supplied_unverified": 0,
        })

        self.assertEqual(define["state"], "not_started")
        self.assertEqual(define["blocking_reason"], "waits for Gate 1 (DISCOVER)")
        self.assertEqual(define["required_approver"], {
            "runtime": ["asha"],
            "attestation": "local",
            "signoff_roles": ["Sponsor"],
        })
        store.close()

    def cross_bank_contract(self) -> dict:
        """The shipped contract's shape: a later bank's gate line citing an earlier
        bank's question. One real row does this, the DELIVER line "AI overlay:
        guardrails live, kill switch tested", which cites BUILD-5 and BUILD-6."""
        contract = copy.deepcopy(self.CONTRACT)
        for bank in contract["banks"]:
            if bank["id"] == "define":
                bank["gate_rendering"].append({
                    "line": "The person survived into DEFINE",
                    "evidenced_by": "discover.person, re-read at Gate 2",
                    "questions": ["define.sponsor", "discover.person"],
                })
        return contract

    def test_a_line_citing_an_earlier_banks_question_is_met_and_says_where_from(self) -> None:
        """The defect: the id was looked up in the citing bank's own answers, where it
        never appears, so the row read unmet forever while the gate read approved."""
        store, conductor = self.opening()
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                        expected_revision=second.revision, turn_id="cost")
        fourth = conductor.prove_gate("discover", gate_proof(), expected_revision=third.revision,
                                      turn_id="gate-1")
        fifth = conductor.submit_answer("define.sponsor", "Dana signed the brief.", observed(),
                                        expected_revision=fourth.revision, turn_id="sponsor")
        self.assertEqual(fifth.status, "accepted")

        report = phase_report(conductor, self.cross_bank_contract(), self.path)
        define = [phase for phase in report if phase["bank_id"] == "define"][0]
        carried = [row for row in define["outcomes"]
                   if row["line"] == "The person survived into DEFINE"][0]
        self.assertTrue(carried["met"])
        self.assertEqual(carried["answered_in"],
                         {"define.sponsor": "define", "discover.person": "discover"})
        # The marker is the whole point: the runtime knows discover.person was answered
        # once, at Gate 1. It holds no fact that anyone re-read it at Gate 2, which is what
        # this row's own evidence text asks for. Reporting met=true silently would turn a
        # visible false negative into an invisible false positive.
        self.assertEqual(carried["carried"], ["discover"])
        self.assertNotIn("The person survived into DEFINE", define["missing"]["gate_lines"])
        # A row satisfied inside its own bank carries no marker, so the marker cannot be
        # something every row gets.
        own = [row for row in define["outcomes"] if row["line"] == "The sponsor is named"][0]
        self.assertEqual(own["carried"], [])
        store.close()

    def test_a_carried_line_is_unmet_while_the_earlier_answer_is_parked(self) -> None:
        """Foreign ids are evaluated, not waved through: the lookup has to find the
        answer AND find it unparked."""
        store, conductor = self.opening()
        # A refusal that writes a record advances the store, so the revision the refusal
        # itself returns is already stale; retrying with it is a conflict, not a challenge.
        # Read the current revision back each time, the way `pmos status` does.
        for index in range(3):
            refused = conductor.submit_answer(
                "discover.person", "Mina exported the failures.",
                {"class": "observed_behavior", "source": "a source this fixture cannot resolve",
                 "date": "2026-09-04", "location": "customer-call"},
                expected_revision=conductor.next_turn().revision, turn_id="park-%d" % index)
        self.assertEqual(refused.status, "parked")

        report = phase_report(conductor, self.cross_bank_contract(), self.path)
        define = [phase for phase in report if phase["bank_id"] == "define"][0]
        carried = [row for row in define["outcomes"]
                   if row["line"] == "The person survived into DEFINE"][0]
        self.assertFalse(carried["met"])
        self.assertIn("The person survived into DEFINE", define["missing"]["gate_lines"])
        store.close()

    def test_a_line_citing_an_id_no_bank_defines_stays_unmet(self) -> None:
        store, conductor = self.opening()
        contract = copy.deepcopy(self.CONTRACT)
        for bank in contract["banks"]:
            if bank["id"] == "define":
                bank["gate_rendering"].append({
                    "line": "A line with a typo behind it",
                    "evidenced_by": "define.spnosor",
                    "questions": ["define.spnosor"],
                })
        report = phase_report(conductor, contract, self.path)
        define = [phase for phase in report if phase["bank_id"] == "define"][0]
        typo = [row for row in define["outcomes"]
                if row["line"] == "A line with a typo behind it"][0]
        self.assertFalse(typo["met"])
        self.assertEqual(typo["answered_in"], {})
        store.close()

    def test_a_line_with_no_question_behind_it_is_unknown_and_not_unmet(self) -> None:
        """Four shipped rows are human signatures with no question behind them. They
        were in neither list, so the report named them nowhere at all."""
        store, conductor = self.opening()
        contract = copy.deepcopy(self.CONTRACT)
        for bank in contract["banks"]:
            if bank["id"] == "discover":
                bank["gate_rendering"].append({
                    "line": "Go or no-go recorded with rationale",
                    "evidenced_by": "a human signature",
                    "questions": [],
                })
        report = phase_report(conductor, contract, self.path)
        discover = [phase for phase in report if phase["bank_id"] == "discover"][0]
        self.assertEqual(discover["missing"]["unknown_gate_lines"],
                         ["Go or no-go recorded with rationale"])
        self.assertNotIn("Go or no-go recorded with rationale",
                         discover["missing"]["gate_lines"])
        store.close()

    def test_fully_answered_bank_is_awaiting_approval(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                        expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                       expected_revision=second.revision, turn_id="cost")
        self.assertEqual((second.status, third.status), ("accepted", "accepted"))

        report = phase_report(conductor, self.CONTRACT, self.path)
        discover, define = report

        self.assertEqual(discover["state"], "awaiting_approval")
        self.assertEqual(discover["next_action"], {"action": "gate", "bank_id": "discover", "question_id": None})
        self.assertEqual(discover["blocking_reason"], "waits for Gate 1 approval")
        self.assertEqual(discover["outcomes"], [
            {"line": "The person is named", "evidenced_by": "discover.person", "questions": ["discover.person"], "met": True, "answered_in": {"discover.person": "discover"}, "carried": []},
            {"line": "The cost is exported", "evidenced_by": "discover.cost", "questions": ["discover.cost"], "met": True, "answered_in": {"discover.cost": "discover"}, "carried": []},
        ])
        self.assertEqual(discover["completed"], {
            "questions": ["discover.person", "discover.cost"],
            "source_verified": 2,
            "quote_verified": 0,
            "supplied_unverified": 0,
        })
        self.assertEqual(define["state"], "not_started")

        store.close()

    def test_gated_bank_is_approved(self) -> None:
        store, conductor = self.opening()
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                        expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                       expected_revision=second.revision, turn_id="cost")
        blocked = conductor.next_turn()
        self.assertEqual(blocked.status, "blocked")
        conductor.prove_gate("discover", gate_proof(), expected_revision=blocked.revision, turn_id="gate-1")

        report = phase_report(conductor, self.CONTRACT, self.path)
        discover, define = report

        self.assertEqual(discover["state"], "approved")
        self.assertIsNone(discover["blocking_reason"])
        self.assertIsNone(discover["next_action"])
        self.assertEqual(define["state"], "in_progress")
        self.assertEqual(define["next_action"], {
            "action": "answer",
            "bank_id": "define",
            "question_id": "define.sponsor",
        })
        store.close()

    def test_required_approver_signoff_lookup(self) -> None:
        store, conductor = self.opening()
        report = phase_report(conductor, self.CONTRACT, self.path)
        self.assertEqual(report[0]["required_approver"], {
            "runtime": ["asha"],
            "attestation": "local",
            "signoff_roles": ["Product owner"],
        })

        no_signoff = {key: value for key, value in self.CONTRACT.items() if key != "signoffs"}
        contractless = phase_report(conductor, no_signoff, self.path)[0]
        self.assertIsNone(contractless["required_approver"]["signoff_roles"])
        store.close()

    def test_contract_none_uses_bank_id(self) -> None:
        store, conductor = self.opening()
        report = phase_report(conductor, None, self.path)
        discover = report[0]

        self.assertEqual(discover["phase"], "DISCOVER")
        self.assertIsNone(discover["gate"])
        self.assertEqual(discover["outcomes"], [])
        self.assertEqual(discover["required_approver"], {
            "runtime": ["asha"],
            "attestation": "local",
            "signoff_roles": None,
        })
        store.close()

    def test_stale_gate_blocks_current_bank_reason(self) -> None:
        switch = {"enabled": True}
        store, conductor = self.opening_with_switchable_verifier(switch)
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                        expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                       expected_revision=second.revision, turn_id="cost")
        blocked = conductor.next_turn()
        self.assertEqual(blocked.status, "blocked")
        gated = conductor.prove_gate("discover", gate_proof(),
                                     expected_revision=blocked.revision, turn_id="gate-1")
        self.assertTrue(gated.status in ("advanced", "completed"))
        define = conductor.next_turn()
        self.assertEqual(define.question.id, "define.sponsor")
        switch["enabled"] = False

        report = phase_report(conductor, self.CONTRACT, self.path)
        discover, define_report = report
        stale = conductor.stale_gates()
        self.assertEqual(discover["state"], "stale")
        self.assertEqual(discover["next_action"], {"action": "gate", "bank_id": "discover", "question_id": None})
        self.assertEqual(discover["blocking_reason"], stale[0]["message"])
        self.assertEqual(define_report["state"], "in_progress")
        self.assertIsNone(define_report["next_action"])
        self.assertEqual(
            define_report["blocking_reason"],
            "the approval for discover no longer holds; prove it again first",
        )
        store.close()

    def test_contract_with_only_late_bank_includes_missing_discover_phase(self) -> None:
        store, conductor = self.opening()
        contract = {
            "banks": [
                {
                    "id": "define",
                    "stage": "DEFINE",
                    "gate": 2,
                    "gate_rendering": [
                        {
                            "line": "The sponsor is named",
                            "evidenced_by": "define.sponsor",
                            "questions": ["define.sponsor"],
                        },
                    ],
                }
            ],
            "signoffs": {"2": ["Sponsor"]},
        }
        report = phase_report(conductor, contract, self.path)

        discover, define = report
        self.assertEqual(discover["phase"], "DISCOVER")
        self.assertIsNone(discover["gate"])
        self.assertEqual(discover["outcomes"], [])
        self.assertEqual(define["phase"], "DEFINE")
        self.assertEqual(define["gate"], 2)
        self.assertEqual(define["outcomes"], [
            {
                "line": "The sponsor is named",
                "evidenced_by": "define.sponsor",
                "questions": ["define.sponsor"],
                "met": False,
                "answered_in": {"define.sponsor": "define"},
                "carried": [],
            }
        ])
        store.close()

    def test_documents_and_named_documents_before_the_gate(self) -> None:
        workspace = Path(self.temp.name) / "workspace"
        (workspace / "discovery").mkdir(parents=True)
        text = problem_framing_text("Problem body.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(text, encoding="utf-8")

        store, conductor = self.opening_with_workspace(workspace)
        report = phase_report(conductor, self.WORKSPACE_CONTRACT, workspace)
        discover = report[0]

        self.assertEqual(discover["documents"], [{
            "id": "discovery/problem-framing",
            "path": "discovery/problem-framing.md",
            "phase": "DISCOVER",
            "status": "draft",
            "revision": artifact_revision(text),
            "approved_revision": None,
        }])
        self.assertEqual(discover["named_documents"], [
            {"path": "discovery/problem-framing.md", "present": True},
            {"path": "discovery/personas.md", "present": False},
        ])
        self.assertIsNone(discover["approval"])
        self.assertEqual(discover["rejections"], [])
        store.close()

    def test_approval_names_the_artifact_after_the_gate(self) -> None:
        workspace = Path(self.temp.name) / "workspace"
        (workspace / "discovery").mkdir(parents=True)
        text = problem_framing_text("Problem body.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(text, encoding="utf-8")

        store, conductor = self.opening_with_workspace(workspace)
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                        expected_revision=second.revision, turn_id="cost")
        blocked = conductor.next_turn()
        gated = conductor.prove_gate("discover", gate_proof(),
                                     expected_revision=blocked.revision, turn_id="gate-1")
        self.assertIn(gated.status, ("advanced", "completed"))

        report = phase_report(conductor, self.WORKSPACE_CONTRACT, workspace)
        discover = report[0]

        self.assertEqual(discover["documents"][0]["approved_revision"], artifact_revision(text))
        self.assertIsNotNone(discover["approval"])
        self.assertIn("discovery/problem-framing", discover["approval"]["artifacts"])
        store.close()

    def test_stale_discover_names_the_changed_artifact_after_an_edit(self) -> None:
        workspace = Path(self.temp.name) / "workspace"
        (workspace / "discovery").mkdir(parents=True)
        text = problem_framing_text("Problem body.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(text, encoding="utf-8")

        store, conductor = self.opening_with_workspace(workspace)
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                        expected_revision=second.revision, turn_id="cost")
        blocked = conductor.next_turn()
        conductor.prove_gate("discover", gate_proof(),
                             expected_revision=blocked.revision, turn_id="gate-1")

        edited = problem_framing_text("Problem body, edited.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(edited, encoding="utf-8")

        report = phase_report(conductor, self.WORKSPACE_CONTRACT, workspace)
        discover = report[0]

        self.assertEqual(discover["state"], "stale")
        self.assertEqual(discover["missing"]["changed"], [{
            "id": "discovery/problem-framing",
            "path": "discovery/problem-framing.md",
            "reviewed": artifact_revision(text),
            "current": artifact_revision(edited),
        }])
        self.assertEqual(discover["missing"]["reconcile"], [])
        store.close()

    def test_rejections_name_the_artifact_after_a_rejected_gate_submission(self) -> None:
        workspace = Path(self.temp.name) / "workspace"
        (workspace / "discovery").mkdir(parents=True)
        text = problem_framing_text("Problem body.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(text, encoding="utf-8")

        store, conductor = self.opening_with_workspace(workspace)
        first = conductor.next_turn()
        second = conductor.submit_answer("discover.person", "Mina exported the failures.", observed(),
                                         expected_revision=first.revision, turn_id="person")
        third = conductor.submit_answer("discover.cost", "The export runs every Friday.", artifact(),
                                        expected_revision=second.revision, turn_id="cost")
        blocked = conductor.next_turn()
        conductor.prove_gate("discover", gate_proof(),
                             expected_revision=blocked.revision, turn_id="gate-1")

        edited = problem_framing_text("Problem body, edited.\n")
        (workspace / "discovery" / "problem-framing.md").write_text(edited, encoding="utf-8")

        stale_turn = conductor.next_turn()
        self.assertEqual(stale_turn.status, "stale")
        rejected_proof = gate_proof()
        rejected_proof["decision"] = "rejected"
        rejected = conductor.prove_gate("discover", rejected_proof,
                                        expected_revision=stale_turn.revision, turn_id="gate-1-rejected")
        self.assertEqual(rejected.status, "rejected")

        report = phase_report(conductor, self.WORKSPACE_CONTRACT, workspace)
        discover = report[0]

        self.assertEqual(len(discover["rejections"]), 1)
        self.assertIn("discovery/problem-framing", discover["rejections"][0]["artifacts"])
        store.close()


if __name__ == "__main__":
    unittest.main()
