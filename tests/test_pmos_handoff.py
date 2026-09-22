"""Tests for the handoff package builder."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from pmos.artifacts import build_manifest, check_manifest
from pmos.conductor import Conductor, EvidenceClass, Question, QuestionBank
from pmos.handoff import SECTIONS, build_handoff
from pmos.product import source_resolver
from pmos.store import Store

from test_pmos_artifacts import BLOCK_TEMPLATE, block
from test_pmos_conductor import gate_proof


BANKS = (
    QuestionBank("discover", "v1", (
        Question("discover.problem", "What is the problem statement?", EvidenceClass.OBSERVED_BEHAVIOR),
    ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),
    QuestionBank("define", "v1", (
        Question("define.scope", "What scope was approved?", EvidenceClass.OBSERVED_BEHAVIOR),
    ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),
    QuestionBank("design", "v1", (
        Question("design.interface", "What interface was decided?", EvidenceClass.OBSERVED_BEHAVIOR),
    ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),
)


def observed() -> dict[str, str]:
    return {"class": "observed_behavior", "source": "session replay", "date": "2026-09-03", "location": "replay/17"}


def sample_contract() -> dict[str, object]:
    return {
        "schema": 1,
        "banks": [
            {"id": "discover", "version": "v1", "questions": [], "gate": 1},
            {"id": "define", "version": "v1", "questions": [], "gate": 2},
            {"id": "design", "version": "v1", "questions": [], "gate": 3},
        ],
    }


# Which gate each of the nine sections is bound by. A real workspace's sections are
# artifacts of the phases that produced them, so the fixture stamps them that way: the
# three DISCOVER sections at gate 1, DEFINE at 2, DESIGN at 3. The fixture used to stamp
# every one with the literal `gate: None`, which put them in no manifest at all, and the
# positive assertions below then passed over artifacts nothing had bound.
SECTION_GATES = {title: 1 + index // 3 for index, title in enumerate(SECTIONS)}
BANK_OF_GATE = {1: "discover", 2: "define", 3: "design"}


class HandoffTests(unittest.TestCase):
    PRODUCT_ID = "payments"

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.store = Store(self.root / "runtime.sqlite")
        self.contract = sample_contract()
        self._write_baseline_workspace()
        # Wired the way pmos/product.py wires a real product. Without these two the
        # Conductor records an empty manifest for every approval, no artifact is ever
        # bound to a gate, and the whole class passes over evidence nothing holds.
        self.conductor = Conductor(self.store, self.PRODUCT_ID, BANKS,
                                  gate_source_verifier=self._gate_source_verifier,
                                  gate_manifest=self._gate_manifest,
                                  manifest_verifier=self._manifest_verifier)

    def _gate_manifest(self, bank_id: str) -> dict:
        gates = {"discover": 1, "define": 2, "design": 3}
        return build_manifest(self.root, gates[bank_id])

    def _manifest_verifier(self, manifest) -> dict:
        return check_manifest(self.root, manifest)

    def tearDown(self) -> None:
        self.store.close()
        self._tmp.cleanup()

    def _write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _section_body(self, modified: tuple[str, str] | None = None) -> str:
        body = []
        for index, title in enumerate(SECTIONS, 1):
            body.append(f"## {title}")
            if modified and modified[0] == title:
                body.append(modified[1])
            else:
                body.append(f"[{title}](sections/{index}.md)")
            body.append("")
        return "\n".join(body) + "\n"

    def _write_baseline_workspace(self) -> None:
        for index, title in enumerate(SECTIONS, 1):
            self._write(
                f"sections/{index}.md",
                block(
                    f"demo/sections/{index}",
                    "ALL STAGES",
                    SECTION_GATES[title],
                    "approved",
                    [],
                    "templates/sections.md",
                    "Body.\n",
                ),
            )
        self._write("gate-1.md", "approved proof source\n")
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(),
            ),
        )

    def _gate_hash(self) -> str:
        return hashlib.sha256((self.root / "gate-1.md").read_bytes()).hexdigest()

    def _gate_source_verifier(self, source: str, digest: str) -> bool:
        if source != "gate-1.md":
            return False
        return self._gate_hash() == digest

    def _approve(self, banks=("discover", "define", "design")) -> None:
        for bank_id in BANKS:
            if bank_id.id not in banks:
                break
            turn = self.conductor.next_turn()
            self.assertEqual((turn.status, turn.bank_id), ("question", bank_id.id))
            answered = self.conductor.submit_answer(
                turn.question.id, "It is documented.", observed(),
                expected_revision=turn.revision, turn_id=f"{bank_id.id}-answer")
            self.assertEqual(answered.status, "accepted")
            if bank_id.id in banks:
                proof = self.conductor.prove_gate(
                    bank_id.id, gate_proof(source="gate-1.md", source_hash=self._gate_hash()),
                    expected_revision=answered.revision, turn_id=f"{bank_id.id}-gate")
                self.assertIn(proof.status, {"advanced", "completed"})

    def _result(self) -> dict[str, object]:
        return build_handoff(self.conductor, self.contract, self.root)

    def test_development_ready_positive_case(self) -> None:
        self._approve()
        result = self._result()
        self.assertEqual(result["product_id"], self.PRODUCT_ID)
        self.assertTrue(result["development_ready"])
        self.assertIsNotNone(result["handoff"])
        self.assertEqual(result["source_revision"], self.store.head(self.PRODUCT_ID).token)
        for entry in result["approvals"]:
            self.assertEqual(entry["attestation"], "local")
            self.assertTrue(entry["approved"])

    def test_each_approval_carries_its_evidence_and_the_package_totals_them(self) -> None:
        self._approve()
        result = self._result()
        # observed() cites "session replay", free text this conductor has no resolver for.
        for entry in result["approvals"]:
            self.assertEqual(entry["evidence"],
                             {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 1})
        self.assertEqual(result["evidence"],
                         {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 3})
        # Reported, not gated: every answer is unverified and the package is still ready.
        self.assertTrue(result["development_ready"])

    def test_the_package_total_counts_every_bank_and_each_row_only_its_own(self) -> None:
        """The package total counts every bank's answers; each approvals row counts its own
        bank's. A BUILD answer given after Gate 3 is in the total and in no row."""
        build = QuestionBank("build", "v1", (
            Question("build.tests", "Which tests pass?", EvidenceClass.OBSERVED_BEHAVIOR),
        ), gate_prerequisites=("signed_by",), gate_approvers=("asha",))
        self.conductor = Conductor(self.store, "later", BANKS + (build,),
                                   gate_source_verifier=self._gate_source_verifier,
                                   gate_manifest=self._gate_manifest,
                                   manifest_verifier=self._manifest_verifier)
        self._approve()
        turn = self.conductor.next_turn()
        self.assertEqual((turn.status, turn.bank_id), ("question", "build"))
        answered = self.conductor.submit_answer(
            turn.question.id, "It is documented.", observed(),
            expected_revision=turn.revision, turn_id="build-answer")
        self.assertEqual(answered.status, "accepted")
        contract = dict(self.contract, banks=list(self.contract["banks"]) + [
            {"id": "build", "version": "v1", "questions": [], "gate": 4}])
        result = build_handoff(self.conductor, contract, self.root)
        self.assertEqual([item["bank_id"] for item in result["approvals"]],
                         ["discover", "define", "design"])
        for item in result["approvals"]:
            self.assertEqual(item["evidence"],
                             {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 1})
        self.assertEqual(result["evidence"],
                         {"quote_verified": 0, "source_verified": 0, "supplied_unverified": 4})

    def test_the_evidence_count_leaves_out_a_parked_answer(self) -> None:
        """A parked answer was filed as offered, not accepted, so it is no evidence at all.

        Counted as supplied_unverified it would report two answers behind a bank
        that accepted one.
        """
        banks = (QuestionBank("discover", "v1", (
            Question("discover.problem", "What is the problem statement?", EvidenceClass.OBSERVED_BEHAVIOR),
            Question("discover.person", "Who has the problem?", EvidenceClass.OBSERVED_BEHAVIOR),
        ), gate_prerequisites=("signed_by",), gate_approvers=("asha",)),) + BANKS[1:]
        conductor = Conductor(self.store, "parking", banks, source_resolver=source_resolver(self.root))
        turn = conductor.next_turn()
        cited = conductor.submit_answer(
            "discover.problem", "It is documented.",
            {"class": "observed_behavior", "source": "sections/1.md", "date": "2026-09-03",
             "location": "section 1"},
            expected_revision=turn.revision, turn_id="problem")
        self.assertEqual(cited.status, "accepted")
        for attempt in range(3):
            turn = conductor.next_turn()
            refused = conductor.submit_answer(
                "discover.person", "It is documented.",
                {"class": "observed_behavior", "source": "a hallway remark %d" % attempt},
                expected_revision=turn.revision, turn_id="person-%d" % attempt)
        self.assertEqual(refused.status, "parked")
        self.assertEqual(conductor.state()["banks"]["discover"]["parked"], ["discover.person"])
        result = build_handoff(conductor, self.contract, self.root)
        discover = next(item for item in result["approvals"] if item["bank_id"] == "discover")
        self.assertEqual(discover["evidence"],
                         {"quote_verified": 0, "source_verified": 1, "supplied_unverified": 0})
        self.assertEqual(result["evidence"],
                         {"quote_verified": 0, "source_verified": 1, "supplied_unverified": 0})

    def test_gap_line_marks_section_as_gap_and_not_ready(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("2. Vision and strategy", "- Gap: unresolved direction")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "2. Vision and strategy")
        self.assertEqual(section["status"], "gap")
        self.assertFalse(result["development_ready"])
        self.assertIn("Section 2. Vision and strategy has a gap", result["missing"])

    def test_broken_link_marks_section_as_broken(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("3. Outcomes and success measures", "[bad](missing.md)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "3. Outcomes and success measures")
        self.assertEqual(section["status"], "broken")
        self.assertFalse(result["development_ready"])
        self.assertIn("Section 3. Outcomes and success measures has broken link missing.md", result["missing"])

    def test_absolute_link_counts_as_broken(self) -> None:
        # An absolute link resolves outside the workspace, so it can never satisfy a section.
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "[outside](/etc/hosts)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(section["status"], "broken")
        self.assertFalse(section["links"][0]["exists"])
        self.assertFalse(result["development_ready"])

    def test_not_applicable_sections_remain_ready(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "- N/A because this section is not applicable")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(section["status"], "not_applicable")
        self.assertTrue(result["development_ready"])

    def test_link_to_a_file_without_an_artifact_block_is_not_ready(self) -> None:
        self._write("notes.txt", "TODO")
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "[notes](notes.txt)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(section["status"], "unbound")
        self.assertFalse(result["development_ready"])
        self.assertTrue(any("4. Scope and exclusions" in item for item in result["missing"]))

    def test_not_applicable_without_a_reason_is_not_ready(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "- N/A because")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(section["status"], "empty")
        self.assertFalse(result["development_ready"])
        self.assertTrue(any("4. Scope and exclusions" in item for item in result["missing"]))

    def test_an_unbound_link_beats_a_reasoned_exemption(self) -> None:
        # Linking a file claims the section applies, so a reason cannot exempt a section that
        # also points at a file carrying no artifact block.
        self._write("notes.txt", "TODO")
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(
                    ("4. Scope and exclusions", "[notes](notes.txt)\n- N/A because it does not apply")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(section["status"], "unbound")
        self.assertFalse(result["development_ready"])

    def test_design_gate_not_approved(self) -> None:
        self._approve(("discover", "define"))
        result = self._result()
        design = next(item for item in result["approvals"] if item["bank_id"] == "design")
        self.assertFalse(design["approved"])
        self.assertFalse(result["development_ready"])
        self.assertIn("Gate 3 is not approved", result["missing"])

    def test_discover_gate_becomes_stale(self) -> None:
        self._approve()
        (self.root / "gate-1.md").write_text("changed proof source\n", encoding="utf-8")
        result = self._result()
        discover = next(item for item in result["approvals"] if item["bank_id"] == "discover")
        self.assertTrue(discover["stale"])
        self.assertFalse(result["development_ready"])
        self.assertIn("Gate 1 approval is stale", result["missing"])

    def test_rewriting_a_bound_section_artifact_withdraws_readiness(self) -> None:
        """The binding this class exists to prove, and never proved before.

        Every section artifact used to be stamped with the literal `gate: None`,
        so no approval's manifest held any of them and this edit changed nothing
        a gate could notice.
        """
        self._approve()
        self.assertTrue(self._result()["development_ready"])
        bound = self.root / "sections" / "4.md"      # gate 2, by SECTION_GATES
        bound.write_text(bound.read_text(encoding="utf-8") + "\nRewritten after approval.\n",
                         encoding="utf-8")
        result = self._result()
        self.assertFalse(result["development_ready"])
        self.assertIn("Gate 2 approval is stale", result["missing"])

    def test_a_section_citing_a_later_gate_artifact_is_not_ready(self) -> None:
        """OPUS-1, reproduced and then refused.

        A file can carry an artifact block and still sit in no approval this
        handoff requires: build_manifest collects the artifacts whose declared
        gate equals the gate being approved, so a block naming gate 4 is bound
        by nothing, and rewriting it stales nothing. Before this check, such a
        citation read as "linked" and the package reported development ready
        over evidence that could change underneath it.
        """
        self._write("sections/later.md",
                    block("demo/sections/later", "ALL STAGES", 4, "approved", [],
                          "templates/sections.md", "Body.\n"))
        self._write("development-handoff.md", BLOCK_TEMPLATE.format(
            artifact_id="demo/development-handoff", phase="ALL STAGES", gate="null",
            status="approved", depends_on="[]", template="templates/development-handoff.md",
            body=self._section_body(("8. Interface and data contracts",
                                     "[later](sections/later.md)"))))
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"]
                       if item["title"] == "8. Interface and data contracts")
        self.assertEqual(section["status"], "unapproved")
        self.assertFalse(result["development_ready"])
        self.assertIn("Section 8. Interface and data contracts cites sections/later.md, "
                      "which declares gate 4 and is bound by no gate 1-3 approval",
                      result["missing"])
        # And the reason it matters: the citation is not held to anything.
        later = self.root / "sections" / "later.md"
        later.write_text(later.read_text(encoding="utf-8") + "\nRewritten.\n", encoding="utf-8")
        self.assertEqual([item["bank_id"] for item in self.conductor.stale_gates()], [])

    def test_no_development_handoff_is_not_ready(self) -> None:
        (self.root / "development-handoff.md").unlink()
        self._approve()
        result = self._result()
        self.assertIsNone(result["handoff"])
        self.assertFalse(result["development_ready"])
        self.assertIn("development-handoff.md artifact is missing", result["missing"])

    def test_directory_and_symlink_links_are_broken(self) -> None:
        (self.root / "my_directory").mkdir(parents=True, exist_ok=True)
        target_file = self.root / "sections" / "2.md"
        self.assertTrue(target_file.exists(), "Test precondition: sections/2.md must exist")
        (self.root / "live_symlink").symlink_to("sections/2.md")
        handoff_body = []
        for index, title in enumerate(SECTIONS, 1):
            handoff_body.append(f"## {title}")
            if title == "1. Problem":
                handoff_body.append("[problem](my_directory)")
            elif title == "2. Vision and strategy":
                handoff_body.append("[vision](live_symlink)")
            else:
                handoff_body.append(f"[{title}](sections/{index}.md)")
            handoff_body.append("")
        handoff_text = "\n".join(handoff_body) + "\n"
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=handoff_text,
            ),
        )
        self._approve()
        result = self._result()
        problem_section = next(item for item in result["sections"] if item["title"] == "1. Problem")
        self.assertEqual(problem_section["status"], "broken")
        vision_section = next(item for item in result["sections"] if item["title"] == "2. Vision and strategy")
        self.assertEqual(vision_section["status"], "broken")
        self.assertFalse(result["development_ready"])

    def test_real_file_inside_symlinked_directory_is_broken(self) -> None:
        self._write("real_dir/target.md", "Body.\n")
        (self.root / "symdir").symlink_to("real_dir", target_is_directory=True)
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("6. Evidence and decisions", "[via symlinked dir](symdir/target.md)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "6. Evidence and decisions")
        self.assertEqual(section["status"], "broken")
        self.assertFalse(section["links"][0]["exists"])
        self.assertFalse(result["development_ready"])

    def test_dotdot_across_symlinked_directory_is_broken(self) -> None:
        # A lexical ".." must not be able to cancel out a symlinked directory
        # component and slip past the symlink ban: "symdir/../file.md" must
        # not collapse to "file.md" before the walk ever notices "symdir".
        (self.root / "real_dir").mkdir(parents=True, exist_ok=True)
        (self.root / "symdir").symlink_to("real_dir", target_is_directory=True)
        self._write("file.md", "Body.\n")
        self.assertTrue((self.root / "file.md").exists(), "Test precondition: file.md must exist")
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("7. Dependencies", "[escape attempt](symdir/../file.md)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "7. Dependencies")
        self.assertEqual(section["status"], "broken")
        self.assertFalse(section["links"][0]["exists"])
        self.assertFalse(result["development_ready"])

    def test_relative_and_dotdot_links_inside_root_are_linked(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "[section one](sections/../sections/1.md)")),
            ),
        )
        self._approve()
        result = self._result()
        normal_section = next(item for item in result["sections"]
                              if item["title"] == "5. Requirements and acceptance criteria")
        self.assertEqual(normal_section["status"], "linked")
        self.assertTrue(normal_section["links"][0]["exists"])
        dotdot_section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertEqual(dotdot_section["status"], "linked")
        self.assertTrue(dotdot_section["links"][0]["exists"])
        self.assertTrue(result["development_ready"])

    def test_dotdot_link_to_a_file_without_an_artifact_block_resolves_but_is_unbound(self) -> None:
        # gate-1.md is an ordinary file: the path resolves inside the root, so it is not broken,
        # but nothing records a revision for it, so it cannot carry a section.
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("4. Scope and exclusions", "[gate proof](sections/../gate-1.md)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "4. Scope and exclusions")
        self.assertTrue(section["links"][0]["exists"])
        self.assertEqual(section["status"], "unbound")
        self.assertFalse(result["development_ready"])

    def test_dotdot_link_escaping_root_is_broken(self) -> None:
        self._write(
            "development-handoff.md",
            BLOCK_TEMPLATE.format(
                artifact_id="demo/development-handoff",
                phase="ALL STAGES",
                gate="null",
                status="approved",
                depends_on="[]",
                template="templates/architecture/development-handoff.md",
                body=self._section_body(("8. Interface and data contracts", "[outside](../outside.md)")),
            ),
        )
        self._approve()
        result = self._result()
        section = next(item for item in result["sections"] if item["title"] == "8. Interface and data contracts")
        self.assertEqual(section["status"], "broken")
        self.assertFalse(section["links"][0]["exists"])
        self.assertFalse(result["development_ready"])
