#!/usr/bin/env python3
"""The three surfaces that carry versions here, and what an addition does to each.

F06, external 360 audit of 2026-09-23: README.md held two rules that could not
both be true. One reserved "changing what a gate demands" for a major version;
the next allowed a minor release to add a required template section, after which
a document filled against the older shape fails the current gate. The tree keeps
three separately versioned things and the two rules were talking about two of
them:

* the package version, ``version`` in ``pyproject.toml`` and the tag cut from it;
* the document schema, the templates together with the checks that read a filled
  document, chiefly ``REQUIRED_SECTIONS`` in ``lint.py``. A filled document
  carries no record of the shape it was filled against, so it is checked by
  today's checker. An added required section is breaking here;
* the runtime bank contract, ``pmos/question_banks.json``. A product pins the
  banks it started with and the Conductor refuses to open it against different
  ones, so a shipped addition reaches no existing product until ``pmos repin``.
  An added question is not breaking for a product already in flight.

These tests drive one already approved fixture on each surface through an
addition no check requires and an addition a check does require, so the outcomes
README.md and CHANGELOG.md state are read out of the runtime rather than
asserted. VersioningStatementsAgree fails if either document stops stating them.
"""
from __future__ import annotations

import hashlib
import json
import unittest
import unittest.mock
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import lint
from test_lint import MINIMAL, run

from pmos.banks import CONTRACT_PATH
from pmos.cli import PIN_PATH, main
from pmos.conductor import STATE_PATH, bank_fingerprint
from pmos.store import Store

REPO = Path(__file__).resolve().parent.parent
PRODUCT = "checkout"

# A section a later release adds to the regulated PRD template. The two tests
# below differ only in whether a check lists it, which is the whole distinction
# between an optional and a mandatory addition on this surface.
ADDED_SECTION_PATTERN = (r"^##\s*8\.", "rollback", "## 8. Rollback plan")
ADDED_SECTION_TEXT = ("## 8. Rollback plan\n"
                      "- Reversal: flag off in 5 minutes, owned by the Eng Manager\n")


class DocumentSchemaAdditions(unittest.TestCase):
    """The document schema is checked as it stands today, not as it stood when
    the document was filled. MINIMAL stands for a document approved before
    section 8 existed."""

    def test_an_added_section_no_check_requires_leaves_an_old_filled_document_passing(self):
        codes, messages = run(MINIMAL)
        self.assertEqual(codes, set(), messages)

    def test_an_added_section_a_check_requires_fails_the_same_old_filled_document(self):
        with unittest.mock.patch.object(
                lint, "REQUIRED_SECTIONS", list(lint.REQUIRED_SECTIONS) + [ADDED_SECTION_PATTERN]):
            codes, messages = run(MINIMAL)
        self.assertIn("SECTION", codes)
        self.assertIn("## 8. Rollback plan", messages)

    def test_the_migration_is_to_add_the_section_to_the_document(self):
        migrated = MINIMAL + ADDED_SECTION_TEXT
        with unittest.mock.patch.object(
                lint, "REQUIRED_SECTIONS", list(lint.REQUIRED_SECTIONS) + [ADDED_SECTION_PATTERN]):
            codes, messages = run(migrated)
        self.assertEqual(codes, set(), messages)

    def test_nothing_in_a_filled_document_records_the_shape_it_was_filled_against(self):
        """Why the check above is the whole story: there is no schema version to
        pin a filled document to, so a checker change reaches every document."""
        self.assertNotIn("schema_version", MINIMAL.lower())
        self.assertFalse(hasattr(lint, "SCHEMA_VERSION"))


def _run_json(argv: list[str]) -> tuple[int, dict]:
    output = StringIO()
    with redirect_stdout(output):
        code = main(argv)
    return code, json.loads(output.getvalue())


def _status(folder: str) -> dict:
    code, payload = _run_json(["--json", "status", "--path", folder, "--product-id", PRODUCT])
    assert code == 0, payload
    return payload


def _pin(folder: str, contract: dict) -> None:
    raw = json.dumps(contract).encode("utf-8")
    with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
        snapshot = store.read_snapshot(PRODUCT)
        files = dict(snapshot.files)
        files[PIN_PATH] = raw
        result = store.commit(PRODUCT, files, expected_revision=snapshot.head,
                              metadata={"reason": "versioning contract fixture"})
        assert result.committed


def _answer_bank(folder: str, prefix: str) -> dict:
    """Answer every question of the bank now open, and return the status after."""
    for _ in range(20):
        status = _status(folder)
        if status["interview"] != "question":
            return status
        question_id = status["question"]["id"]
        evidence = {"class": "observed_behavior", "source": "interview-001",
                    "date": "2026-09-04", "location": "customer-call"}
        code, result = _run_json(
            ["answer", "--path", folder, "--product-id", PRODUCT, "--question-id", question_id,
             "--answer", "A real outcome", "--evidence", json.dumps(evidence),
             "--expected-revision", status["revision_token"], "--turn-id", prefix + "-" + question_id,
             "--json"])
        assert code == 0 and result["outcome"]["status"] == "accepted", result
    raise AssertionError("the bank did not finish")


def _gate(folder: str, token: str, turn_id: str, bank_id: str) -> tuple[int, dict]:
    proof = Path(folder, "gate-approval.txt")
    proof.write_bytes(b"reviewed gate evidence\n")
    evidence = {"source": "gate-approval.txt",
                "source_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
                "actor_id": "local-reviewer", "requester_id": "local-operator",
                "decision": "approved", "approved_at": "2026-09-04T00:00:00Z"}
    return _run_json(["gate", "--path", folder, "--product-id", PRODUCT, "--bank-id", bank_id,
                      "--evidence", json.dumps(evidence), "--expected-revision", token,
                      "--turn-id", turn_id, "--json"])


def _repin(folder: str, *extra: str) -> tuple[int, dict]:
    return _run_json(["--json", "repin", "--path", folder, "--product-id", PRODUCT, *extra])


def _conductor_state(folder: str) -> dict:
    with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
        return json.loads(store.read_snapshot(PRODUCT).files[STATE_PATH])


def _contract_without(bank_id: str, question_ids: tuple[str, ...]) -> dict:
    """The shipped contract as it stood before those questions were appended."""
    contract = json.loads(CONTRACT_PATH.read_bytes())
    bank = next(item for item in contract["banks"] if item["id"] == bank_id)
    bank["questions"] = [q for q in bank["questions"] if q["id"] not in question_ids]
    bank["version"] = "c0000000000000000"
    return contract


class RuntimeBankContractAdditions(unittest.TestCase):
    """The same already approved fixture, an approved Gate 1, under an addition
    to a bank it has not approved and an addition to the bank it has."""

    def approved_gate_one(self, folder: str, contract: dict) -> dict:
        """A product pinned to an older contract with DISCOVER approved."""
        self.assertEqual(main(["init", "--path", folder, "--product-id", PRODUCT]), 0)
        _pin(folder, contract)
        status = _answer_bank(folder, "discover")
        code, result = _gate(folder, status["revision_token"], "gate-discover", "discover")
        self.assertEqual(code, 0, result)
        after = _status(folder)
        self.assertEqual(after["stale_banks"], [])
        self.assertFalse(after["question_banks"]["current"])
        return after

    def test_an_addition_to_a_bank_the_product_has_not_approved_is_adopted_and_stales_no_gate(self):
        # The optional arm: DEFINE-10 to DEFINE-12 land in a bank this product
        # has not gated, so repin takes them and the Gate 1 approval is untouched.
        with TemporaryDirectory() as folder:
            before = self.approved_gate_one(folder, _contract_without(
                "define", ("DEFINE-10", "DEFINE-11", "DEFINE-12")))
            self.assertIn("adopt it with `pmos repin`", before["question_banks"]["message"])

            code, planned = _repin(folder, "--dry-run")
            self.assertEqual(code, 0, planned)
            self.assertEqual([entry["bank_id"] for entry in planned["changed"]], ["define"])
            self.assertEqual(planned["changed"][0]["added"], ["DEFINE-10", "DEFINE-11", "DEFINE-12"])
            self.assertEqual(planned["gates_to_prove_again"], [])  # no approval on define, so nothing to re-prove

            code, done = _repin(folder)
            self.assertEqual(code, 0, done)
            after = _status(folder)
            self.assertTrue(after["question_banks"]["current"])
            self.assertEqual(after["stale_banks"], [])
            # The Gate 1 approval survived, and every DISCOVER answer is still stored.
            self.assertIn("discover", _conductor_state(folder)["gates"])
            self.assertEqual(after["source_verified"] + after["supplied_unverified"]
                             + after.get("quote_verified", 0), 9)
            self.assertEqual((after["interview"], after["question"]["id"]), ("question", "DEFINE-1"))

    def test_an_addition_to_a_bank_the_product_has_approved_is_refused_and_the_approval_holds(self):
        # The required arm: the question lands in the bank this product gated, so
        # adopting it would leave an approved bank with a question still to ask,
        # which the Conductor refuses to open. Repin refuses first and writes nothing.
        with TemporaryDirectory() as folder:
            before = self.approved_gate_one(folder, _contract_without("discover", ("DISCOVER-9",)))
            self.assertIn("refuses", before["question_banks"]["message"])
            self.assertNotIn("adopt it with", before["question_banks"]["message"])

            for dry_run in (["--dry-run"], []):
                code, refused = _repin(folder, *dry_run)
                self.assertEqual(code, 2, refused)
                self.assertIn("discover: DISCOVER-9", refused["error"])
                self.assertIn("keeps the banks it started with", refused["error"])

            after = _status(folder)
            self.assertEqual(after["revision_token"], before["revision_token"])
            self.assertEqual(after["question_banks"]["pinned"]["discover"], "c0000000000000000")
            self.assertEqual(after["stale_banks"], [])
            self.assertIn("discover", _conductor_state(folder)["gates"])
            # The product keeps working on the contract it pinned.
            self.assertEqual((after["interview"], after["question"]["id"]), ("question", "DEFINE-1"))

    def test_a_reworded_question_in_an_approved_bank_stales_that_gate_until_it_is_proved_again(self):
        # The reapproval path. No question is added or removed, so repin adopts;
        # the approval recorded the hash of the questions it was given, so the
        # gate reports stale until it is proved again.
        with TemporaryDirectory() as folder:
            contract = json.loads(CONTRACT_PATH.read_bytes())
            discover = next(item for item in contract["banks"] if item["id"] == "discover")
            discover["questions"][0]["ask"] = "Who has this problem, by name?"
            discover["version"] = "c0000000000000000"
            self.approved_gate_one(folder, contract)

            code, done = _repin(folder)
            self.assertEqual(code, 0, done)
            self.assertEqual(done["gates_to_prove_again"], ["discover"])
            after = _status(folder)
            self.assertEqual([item["bank_id"] for item in after["stale_banks"]], ["discover"])
            self.assertIn("changed since this gate was approved", after["stale_banks"][0]["message"])

            code, proved = _gate(folder, after["revision_token"], "gate-discover-again", "discover")
            self.assertEqual(code, 0, proved)
            cleared = _status(folder)
            self.assertEqual(cleared["stale_banks"], [])
            # The approval that stopped verifying is kept, not deleted.
            state = _conductor_state(folder)
            self.assertEqual(len(state["superseded_gates"]["discover"]), 1)
            self.assertIn("superseded_at", state["superseded_gates"]["discover"][0])

    def test_an_approval_records_the_hash_of_the_questions_its_bank_asked(self):
        """What makes the staleness above possible, and what README.md calls the
        stored question hash. A gate recorded before contract pinning has none."""
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", PRODUCT]), 0)
            status = _answer_bank(folder, "discover")
            code, result = _gate(folder, status["revision_token"], "gate-discover", "discover")
            self.assertEqual(code, 0, result)
            record = _conductor_state(folder)["gates"]["discover"]
            from pmos.banks import shipped_banks
            shipped = next(bank for bank in shipped_banks() if bank.id == "discover")
            self.assertEqual(record["contract_sha256"], bank_fingerprint(shipped))


class VersioningStatementsAgree(unittest.TestCase):
    """README.md and CHANGELOG.md must keep stating the outcomes above. Reword
    either one and this class fails, which is the point: the prose is the
    deliverable of F06 and nothing else guards it."""

    README = (REPO / "README.md").read_text(encoding="utf-8")
    CHANGELOG = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")

    def section(self) -> str:
        body = self.README.split("## Versioning and stability", 1)[1]
        return body.split("\n## ", 1)[0]

    def test_the_readme_names_the_three_surfaces_and_where_each_one_lives(self):
        section = self.section()
        for phrase in ("package version", "`pyproject.toml`",
                       "document schema", "`REQUIRED_SECTIONS` in `lint.py`",
                       "runtime bank contract", "`pmos/question_banks.json`"):
            self.assertIn(phrase, section, "README versioning section no longer names: %s" % phrase)

    def test_the_readme_states_both_addition_outcomes(self):
        section = self.section()
        self.assertIn("an added mandatory section is a breaking change", section.lower())
        self.assertIn("an added mandatory question is not a breaking change", section.lower())
        self.assertIn("pmos repin", section)
        self.assertIn("reapproval", section.lower())

    def test_the_readme_no_longer_reserves_every_gate_change_for_a_major_version(self):
        """The sentence F06 reported: it promised for all three surfaces at once."""
        self.assertNotIn("changing what a gate demands is a breaking change", self.section().lower())

    def test_the_surfaces_the_readme_names_are_real(self):
        self.assertIn('version = "', (REPO / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertTrue(lint.REQUIRED_SECTIONS)
        contract = json.loads((REPO / "pmos" / "question_banks.json").read_bytes())
        self.assertTrue(all("version" in bank for bank in contract["banks"]))

    def test_the_changelog_carries_the_dated_correction_on_both_rules(self):
        head = self.CHANGELOG.split("## Unreleased", 1)[0]
        major = next(line for line in head.split("\n") if line.startswith("- **MAJOR**"))
        minor = next(line for line in head.split("\n") if line.startswith("- **MINOR**"))
        self.assertIn("Corrected 2026-09-23", major)
        self.assertIn("document schema", major)
        self.assertIn("Corrected 2026-09-23", minor)
        self.assertIn("pmos repin", minor)

    def test_the_changelog_entry_names_this_module_and_both_outcomes(self):
        unreleased = self.CHANGELOG.split("## Unreleased", 1)[1].split("\n## ", 1)[0]
        self.assertIn("tests/test_versioning_contract.py", unreleased)
        self.assertIn("breaking on the document schema and is not breaking for a product already pinned",
                      unreleased)


if __name__ == "__main__":
    unittest.main()
