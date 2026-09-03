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


if __name__ == "__main__":
    unittest.main(verbosity=2)
