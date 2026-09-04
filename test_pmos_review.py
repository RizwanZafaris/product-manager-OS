"""Tests for exact-tree independent review evidence."""

from __future__ import annotations

import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

TOOLS = Path(__file__).resolve().parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import review_gate
from review_gate import tree_digest, validate_attestation  # noqa: E402


def attestation(root, **changes):
    digest, _rows = tree_digest(root)
    document = {
        "schema": 1,
        "reviewer_id": "independent-test-reviewer",
        "reviewer_kind": "independent-agent",
        "independent_implementation": True,
        "identity_assurance": "unauthenticated-local-claim",
        "reviewed_at": "2026-09-03T00:00:00Z",
        "reviewed_tree_sha256": digest,
        "scope": ["runtime", "tests", "gates"],
        "evidence": [{"command": "tests", "result": "pass"}],
        "findings": [],
        "verdict": "accepted",
    }
    document.update(changes)
    return document


class IndependentReviewGateTests(unittest.TestCase):
    def test_exact_tree_review_passes_and_any_content_change_stales_it(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / "assets").mkdir()
            linked = root / "linked-assets"
            linked.symlink_to("assets", target_is_directory=True)
            document = attestation(root)
            self.assertEqual(validate_attestation(document, root), [])
            _digest, rows = tree_digest(root)
            self.assertIn(("linked-assets", "symlink"),
                          {(row["path"], row["kind"]) for row in rows})
            (root / "runtime.py").write_text("SAFE = False\n", encoding="utf-8")
            self.assertTrue(any("stale" in error for error in
                                validate_attestation(document, root)))

    def test_nested_build_or_dist_named_source_is_part_of_exact_tree(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "pmos" / "build" / "critical.py"
            source.parent.mkdir(parents=True)
            source.write_text("SAFE = True\n", encoding="utf-8")
            first, first_rows = tree_digest(root)
            source.write_text("SAFE = False\n", encoding="utf-8")
            second, second_rows = tree_digest(root)
            self.assertNotEqual(first, second)
            self.assertIn("pmos/build/critical.py", {row["path"] for row in first_rows})
            self.assertIn("pmos/build/critical.py", {row["path"] for row in second_rows})

    def test_parent_swap_uses_pinned_review_tree_descriptor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "assets"
            nested.mkdir()
            (nested / "proof.txt").write_text("safe", encoding="utf-8")
            outside = root / "outside"
            staged = root / "staged-assets"
            real_read = review_gate.os.read
            swapped = False

            def swap_after_open(descriptor, size):
                nonlocal swapped
                chunk = real_read(descriptor, size)
                if chunk and not swapped:
                    nested.rename(staged)
                    outside.mkdir()
                    nested.symlink_to(outside, target_is_directory=True)
                    swapped = True
                return chunk

            with patch.object(review_gate.os, "read", side_effect=swap_after_open):
                _digest, rows = tree_digest(root)
            self.assertTrue(swapped)
            self.assertIn("assets/proof.txt", {row["path"] for row in rows})
            self.assertFalse((outside / "proof.txt").exists())

    def test_nested_directory_replacement_during_inventory_fails_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "assets"
            nested.mkdir()
            (nested / "proof.txt").write_text("safe", encoding="utf-8")
            outside = root / "outside"
            staged = root / "staged"
            real_open = review_gate.os.open
            swapped = False

            def swap_nested(name, *args, **kwargs):
                nonlocal swapped
                if name == "assets" and not swapped:
                    nested.rename(staged)
                    outside.mkdir()
                    nested.symlink_to(outside, target_is_directory=True)
                    swapped = True
                return real_open(name, *args, **kwargs)

            with patch.object(review_gate.os, "open", side_effect=swap_nested):
                with self.assertRaisesRegex(OSError, "Too many levels|No such file|Not a directory"):
                    tree_digest(root)
            self.assertTrue(swapped)

    def test_symlink_replacement_during_inventory_fails_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "proof.txt").write_text("safe", encoding="utf-8")
            alias = root / "alias.txt"
            alias.symlink_to("proof.txt")
            outside = root / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            real_readlink = review_gate.os.readlink
            swapped = False

            def swap_link(name, *args, **kwargs):
                nonlocal swapped
                target = real_readlink(name, *args, **kwargs)
                if name == "alias.txt" and not swapped:
                    alias.unlink()
                    alias.symlink_to(outside)
                    swapped = True
                return target

            with patch.object(review_gate.os, "readlink", side_effect=swap_link):
                with self.assertRaisesRegex(OSError, "review symlink changed"):
                    tree_digest(root)
            self.assertTrue(swapped)

    def test_whole_root_swap_fails_closed(self):
        with TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "tree"
            root.mkdir()
            (root / "proof.txt").write_text("safe", encoding="utf-8")
            staged = parent / "staged"
            real_read = review_gate.os.read
            swapped = False

            def swap_after_open(descriptor, size):
                nonlocal swapped
                chunk = real_read(descriptor, size)
                if chunk and not swapped:
                    root.rename(staged)
                    root.mkdir()
                    swapped = True
                return chunk

            with patch.object(review_gate.os, "read", side_effect=swap_after_open):
                with self.assertRaisesRegex(OSError, "review root changed"):
                    tree_digest(root)
            self.assertTrue(swapped)

    def test_unresolved_high_priority_finding_fails(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_text("a", encoding="utf-8")
            finding = {"id": "R-1", "severity": "P1", "status": "open",
                       "summary": "unsafe", "evidence": "test"}
            errors = validate_attestation(
                attestation(root, findings=[finding]), root)
            self.assertTrue(any("unresolved P1" in error for error in errors))

    def test_review_cannot_be_self_declared_or_use_unknown_fields(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_text("a", encoding="utf-8")
            self.assertTrue(validate_attestation(
                attestation(root, reviewer_id="root"), root))
            malformed = attestation(root)
            malformed["trust_me"] = True
            self.assertEqual(validate_attestation(malformed, root),
                             ["review attestation does not use the closed schema"])

    def test_local_record_cannot_claim_authenticated_reviewer_identity(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_text("a", encoding="utf-8")
            errors = validate_attestation(
                attestation(root, identity_assurance="authenticated"), root)
            self.assertTrue(any("unauthenticated" in error for error in errors))



class RecordReviewTests(unittest.TestCase):
    """The gate had no way to close it except hand-writing JSON.

    That is why these exist. A gate that can only be validated and never
    recorded stays red, red becomes the normal state, and the check stops
    carrying information: three pull requests were merged with this one red
    before --record was added. The tests below cover the two properties that
    matter, which are that it produces a record the validator accepts, and
    that it refuses to let the person who wrote the tree close the gate on it.
    """

    def _args(self, root, **over):
        import argparse
        # The canonical path matters: tree_digest deliberately excludes
        # docs/readiness/independent-review.json from its own hash, so a
        # record written there does not invalidate itself. Writing anywhere
        # else inside the tree would, which is what the first version of this
        # test did and is why it failed.
        canonical = root / review_gate.ATTESTATION
        canonical.parent.mkdir(parents=True, exist_ok=True)
        fields = dict(
            record=True, attestation=str(canonical),
            reviewer="A. Reviewer", reviewer_kind="human",
            scope=["templates/"], evidence=["python3 tools/ci_gate.py|17/18"],
            finding=None, verdict="accepted", digest=False)
        fields.update(over)
        return argparse.Namespace(**fields)

    def test_a_recorded_review_validates(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            code = review_gate.record_review(self._args(root), root)
            self.assertEqual(0, code)
            document = json.loads(
                (root / review_gate.ATTESTATION).read_text(encoding="utf-8"))
            self.assertEqual([], validate_attestation(document, root))

    def test_it_records_the_digest_of_the_tree_it_saw(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            review_gate.record_review(self._args(root), root)
            document = json.loads(
                (root / review_gate.ATTESTATION).read_text(encoding="utf-8"))
            expected, _rows = tree_digest(root)
            self.assertEqual(expected, document["reviewed_tree_sha256"])

            # And a later change makes that record stale, which is the whole
            # point of binding the review to a digest.
            (root / "b.md").write_text("added later\n", encoding="utf-8")
            self.assertIn("stale", " ".join(
                validate_attestation(document, root)))

    def test_it_refuses_to_let_an_author_attest_their_own_tree(self):
        """The single integrity property. Everything else here is ergonomics."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            with patch.object(review_gate, "recent_authors",
                              return_value={"the author"}):
                code = review_gate.record_review(
                    self._args(root, reviewer="The Author"), root)
            self.assertEqual(2, code)
            self.assertFalse((root / review_gate.ATTESTATION).exists(),
                             "a refused self-attestation still wrote a record")

    def test_it_refuses_a_review_that_ran_nothing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            code = review_gate.record_review(
                self._args(root, evidence=None), root)
            self.assertEqual(2, code)
            self.assertFalse((root / review_gate.ATTESTATION).exists())

    def test_it_refuses_a_review_with_no_stated_scope(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            code = review_gate.record_review(self._args(root, scope=None), root)
            self.assertEqual(2, code)

    def test_findings_are_recorded_with_ids_and_survive_validation(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            code = review_gate.record_review(self._args(
                root,
                finding=["P2|accepted|Tables are becoming uniform|read 25"]),
                root)
            self.assertEqual(0, code)
            document = json.loads(
                (root / review_gate.ATTESTATION).read_text(encoding="utf-8"))
            self.assertEqual(1, len(document["findings"]))
            self.assertEqual("R1", document["findings"][0]["id"])
            self.assertEqual([], validate_attestation(document, root))

    def test_a_malformed_finding_is_refused_rather_than_guessed(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            code = review_gate.record_review(
                self._args(root, finding=["just a sentence"]), root)
            self.assertEqual(2, code)

    def test_identity_is_never_claimed_as_authenticated(self):
        """The tool records a claim. It must never dress it as proof."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            review_gate.record_review(self._args(root), root)
            document = json.loads(
                (root / review_gate.ATTESTATION).read_text(encoding="utf-8"))
            self.assertEqual("unauthenticated-local-claim",
                             document["identity_assurance"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
