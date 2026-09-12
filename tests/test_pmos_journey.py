"""The runtime half of the W9h fictional journey test.

Every approval, actor, date and piece of evidence below is fictional: it is
invented for this test alone, lives only inside the temporary workspace this
test creates and destroys, and proves nothing about any real product,
sponsor or reviewer. No assertion here should be read as a claim about a real
gate approval.

This module drives the whole journey, from the understood problem (Gate 1)
through a development-ready handoff (Gate 3), through pmos.cli.main only: no
Store, Conductor or other internal object is touched directly. A temporary
workspace holds one product, id "ledgerline", and every working copy this
test writes carries its own artifact block and a body whose first line is
literally "FICTIONAL TEST DATA".

The static half of W9h, which checks the real example files under
examples/, is added to this module by a later task; this module holds only
the runtime TestCase.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.cli import main

PRODUCT_ID = "ledgerline"

# The runtime's only authorized gate approver (pmos/banks.py LOCAL_APPROVERS).
# "requester_id" carries this test's fictional sponsor instead: the conductor
# requires the approving actor and the requesting actor to differ, so the
# fictional identity goes on the field that is free to carry one.
_LOCAL_APPROVER = "local-reviewer"
_FICTIONAL_SPONSOR = "fictional-sponsor"


class JourneyRuntimeTests(unittest.TestCase):
    """Gate 1 to a development-ready Gate 3 handoff, driven by pmos.cli.main."""

    # ------------------------------ CLI helpers ------------------------------

    def run_cli(self, argv: list) -> tuple:
        """Run pmos.cli.main(argv) and return (exit code, parsed JSON)."""
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(list(argv) + ["--json"])
        return code, json.loads(buffer.getvalue())

    def status(self, folder: str) -> dict:
        code, result = self.run_cli(["status", "--path", folder, "--product-id", PRODUCT_ID])
        self.assertEqual(code, 0, result)
        return result

    def answer_bank(self, folder: str, prefix: str) -> dict:
        """Answer every open question of the current bank with fictional evidence.

        The evidence class is always observed_behavior: it is the strongest
        rung on the conductor's evidence ladder, so it satisfies every
        question regardless of that question's own required class. The
        source named in the evidence is visibly fictional and never a real
        file, so it is recorded as supplied rather than verified; that is
        fine, since acceptance never requires verification.
        """
        for _ in range(20):
            status = self.status(folder)
            if status["interview"] != "question":
                return status
            question_id = status["question"]["id"]
            evidence = {"class": "observed_behavior",
                        "source": "fictional-test-evidence-" + question_id.lower(),
                        "date": "2026-08-13", "location": "fictional-test-interview"}
            code, result = self.run_cli([
                "answer", "--path", folder, "--product-id", PRODUCT_ID,
                "--question-id", question_id,
                "--answer", "FICTIONAL TEST DATA: a fictional answer for " + question_id,
                "--evidence", json.dumps(evidence),
                "--expected-revision", status["revision_token"],
                "--turn-id", prefix + "-" + question_id])
            self.assertEqual((code, result["outcome"]["status"]), (0, "accepted"), result)
        self.fail("the %s bank did not finish answering" % prefix)

    def write_working_copy(self, folder: str, rel_path: str, artifact_id: str, phase: str,
                           gate: int, depends_on: list, template: str, body: str) -> Path:
        """Write a minimal working copy carrying its artifact block.

        Modeled on the write_artifact helper in
        tests/test_pmos_cli.py::CliTests (see
        test_revision_bound_approvals_hold_through_the_cli), kept local here
        so this module never imports from another test module.
        """
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

    def approve_gate(self, folder: str, token: str, turn_id: str, bank_id: str) -> tuple:
        """Approve bank_id's gate with a real local proof file and fictional names.

        The proof file's content visibly names it as fictional test data; its
        hash is real, because the runtime's gate verifier checks the bytes on
        disk, but what those bytes say is invented for this test alone. Each
        bank gets its own proof file, never rewritten afterward: the
        conductor re-verifies every approved gate's proof source on every
        later turn, so reusing one file across gates would stale the earlier
        approval as soon as a later one overwrote it.
        """
        proof_name = "fictional-gate-approval-%s.txt" % bank_id
        proof_path = Path(folder, proof_name)
        proof_bytes = ("FICTIONAL TEST DATA: %s requested a fictional approval of the %s "
                      "gate for this test only.\n" % (_FICTIONAL_SPONSOR, bank_id)).encode("utf-8")
        proof_path.write_bytes(proof_bytes)
        evidence = {
            "source": proof_name,
            "source_sha256": hashlib.sha256(proof_bytes).hexdigest(),
            "actor_id": _LOCAL_APPROVER,
            "requester_id": _FICTIONAL_SPONSOR,
            "decision": "approved",
            "approved_at": "2026-09-04T00:00:00Z",
        }
        return self.run_cli(["gate", "--path", folder, "--product-id", PRODUCT_ID,
                             "--bank-id", bank_id, "--evidence", json.dumps(evidence),
                             "--expected-revision", token, "--turn-id", turn_id])

    def handoff(self, folder: str) -> tuple:
        return self.run_cli(["handoff", "--path", folder, "--product-id", PRODUCT_ID])

    # --------------------------------- the test ---------------------------------

    def test_the_journey_reaches_a_development_ready_handoff_then_a_gate_one_edit_stales_it(self):
        with TemporaryDirectory() as folder:
            # 1. pmos init.
            code, result = self.run_cli(["init", "--path", folder, "--product-id", PRODUCT_ID])
            self.assertEqual((code, result["ok"]), (0, True), result)

            # 2. Gate 1: problem framing, answered and approved by a fictional sponsor.
            self.write_working_copy(
                folder, "discovery/problem-framing.md", "ledgerline/discovery/problem-framing",
                "DISCOVER", 1, [], "templates/discovery/problem-framing.md",
                "FICTIONAL TEST DATA\nA minimal fictional problem framing, invented for this test.\n")
            status = self.answer_bank(folder, "discover")
            code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-1", "discover")
            self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

            # 2. Gate 2: vision, product strategy, roadmap and PRD, each depending
            # on the artifact before it, all answered and approved together.
            self.write_working_copy(
                folder, "planning/vision.md", "ledgerline/planning/vision", "DEFINE", 2,
                ["ledgerline/discovery/problem-framing"], "templates/planning/vision.md",
                "FICTIONAL TEST DATA\nA minimal fictional vision, invented for this test.\n")
            self.write_working_copy(
                folder, "planning/product-strategy.md", "ledgerline/planning/product-strategy",
                "DEFINE", 2, ["ledgerline/planning/vision"], "templates/planning/product-strategy.md",
                "FICTIONAL TEST DATA\nA minimal fictional product strategy, invented for this test.\n")
            self.write_working_copy(
                folder, "planning/roadmap.md", "ledgerline/planning/roadmap", "DEFINE", 2,
                ["ledgerline/planning/product-strategy"], "templates/planning/roadmap.md",
                "FICTIONAL TEST DATA\nA minimal fictional roadmap, invented for this test.\n")
            self.write_working_copy(
                folder, "definition/prd.md", "ledgerline/definition/prd", "DEFINE", 2,
                ["ledgerline/planning/roadmap"], "templates/definition/prd.md",
                "FICTIONAL TEST DATA\nA minimal fictional PRD, invented for this test.\n")
            status = self.answer_bank(folder, "define")
            code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-2", "define")
            self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

            # 2. Gate 3: a data model, an API contract and the development handoff
            # itself, which fills all nine sections (requirement 3 below).
            self.write_working_copy(
                folder, "architecture/data-model.md", "ledgerline/architecture/data-model",
                "DESIGN", 3, ["ledgerline/definition/prd"], "templates/architecture/data-model.md",
                "FICTIONAL TEST DATA\nA minimal fictional data model, invented for this test.\n")
            self.write_working_copy(
                folder, "architecture/api-contract.md", "ledgerline/architecture/api-contract",
                "DESIGN", 3, ["ledgerline/architecture/data-model"],
                "templates/architecture/api-contract.md",
                "FICTIONAL TEST DATA\nA minimal fictional API contract, invented for this test.\n")
            handoff_body = "\n".join([
                "FICTIONAL TEST DATA",
                "A minimal fictional development handoff, invented for this test.",
                "",
                "## 1. Problem",
                "",
                "Link: [problem framing](../discovery/problem-framing.md)",
                "",
                "## 2. Vision and strategy",
                "",
                "Link: [vision](../planning/vision.md)",
                "Link: [product strategy](../planning/product-strategy.md)",
                "",
                "## 3. Outcomes and success measures",
                "",
                "Link: [roadmap](../planning/roadmap.md)",
                "",
                "## 4. Scope and exclusions",
                "",
                "Link: [PRD](../definition/prd.md)",
                "",
                "## 5. Requirements and acceptance criteria",
                "",
                "Link: [PRD](../definition/prd.md)",
                "",
                "## 6. Evidence and decisions",
                "",
                "Link: [product strategy](../planning/product-strategy.md)",
                "",
                "## 7. Dependencies",
                "",
                "Link: [roadmap](../planning/roadmap.md)",
                "",
                "## 8. Interface and data contracts",
                "",
                "Link: [data model](data-model.md)",
                "Link: [API contract](api-contract.md)",
                "",
                "## 9. Unresolved risks and constraints",
                "",
                "Link: [API contract](api-contract.md)",
            ])
            self.write_working_copy(
                folder, "architecture/development-handoff.md",
                "ledgerline/architecture/development-handoff", "DESIGN", 3,
                ["ledgerline/architecture/api-contract"],
                "templates/architecture/development-handoff.md", handoff_body)
            status = self.answer_bank(folder, "design")
            code, result = self.approve_gate(folder, status["revision_token"], "journey-gate-3", "design")
            self.assertEqual((code, result["outcome"]["status"]), (0, "advanced"), result)

            # 4. pmos handoff now reports a development-ready package.
            code, package = self.handoff(folder)
            self.assertEqual(code, 0, package)
            self.assertTrue(package["development_ready"], package)
            self.assertEqual(package["missing"], [])

            status = self.status(folder)
            index = json.loads(Path(folder, "handoff/context-index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["source_revision"], status["revision_token"])

            context = Path(folder, "handoff/CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("Development-ready: yes", context)
            for gate_number, bank_id in ((1, "discover"), (2, "define"), (3, "design")):
                self.assertIn("Gate %d (%s)" % (gate_number, bank_id), context)
            self.assertEqual(context.count("local attestation"), 3)

            # 5. Editing the Gate 1 working copy stales its approval.
            self.write_working_copy(
                folder, "discovery/problem-framing.md", "ledgerline/discovery/problem-framing",
                "DISCOVER", 1, [], "templates/discovery/problem-framing.md",
                "FICTIONAL TEST DATA\nA changed fictional problem framing, invented for this test.\n")
            code, package = self.handoff(folder)
            self.assertEqual(code, 1, package)
            self.assertFalse(package["development_ready"], package)
            self.assertIn("Gate 1 approval is stale", package["missing"])

            status = self.status(folder)
            self.assertIn("discover", [stale["bank_id"] for stale in status["stale_banks"]])


if __name__ == "__main__":
    unittest.main()
