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



class AppleDoubleSidecarTests(unittest.TestCase):
    """The reviewed tree must not depend on the filesystem it is checked out on.

    macOS writes AppleDouble sidecars (``._name``) beside every entry when a
    repository lives on exFAT, FAT or SMB, which is exactly what happens when
    the maintainer keeps this repository on an external drive. Those sidecars
    are OS-generated metadata, are already ignored by .gitignore, and can never
    reach a hosted checkout. Hashing them made the digest recorded on such a
    workspace permanently unable to match the digest CI computes for the same
    commit, so a review recorded there could never validate.
    """

    def test_appledouble_sidecar_does_not_change_the_reviewed_digest(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            clean, _rows = tree_digest(root)
            (root / "._runtime.py").write_bytes(
                b"\x00\x05\x16\x07AppleDouble resource fork")
            (root / "._agents").write_bytes(b"\x00\x05\x16\x07dir sidecar")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("._runtime.py", {row["path"] for row in rows})
            self.assertNotIn("._agents", {row["path"] for row in rows})

    def test_nested_appledouble_sidecars_are_excluded_too(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "pmos"
            package.mkdir()
            (package / "store.py").write_text("SAFE = True\n", encoding="utf-8")
            clean, _rows = tree_digest(root)
            (package / "._store.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("pmos/._store.py", {row["path"] for row in rows})

    def test_a_recorded_review_survives_sidecars_appearing_afterwards(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            document = attestation(root)
            self.assertEqual(validate_attestation(document, root), [])
            (root / "._runtime.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            self.assertEqual(validate_attestation(document, root), [])

    def test_real_source_changes_still_stale_the_review_on_such_a_workspace(self):
        """Excluding sidecars must not blunt the gate's actual job."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / "._runtime.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            document = attestation(root)
            self.assertEqual(validate_attestation(document, root), [])
            (root / "runtime.py").write_text("SAFE = False\n", encoding="utf-8")
            self.assertTrue(any("stale" in error for error in
                                validate_attestation(document, root)))

    def test_a_dotfile_that_is_not_a_sidecar_is_still_reviewed(self):
        """Only the ``._`` AppleDouble prefix is excluded, not dotfiles at large."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env.example").write_text("KEY=\n", encoding="utf-8")
            first, rows = tree_digest(root)
            self.assertIn(".env.example", {row["path"] for row in rows})
            (root / ".env.example").write_text("KEY=changed\n", encoding="utf-8")
            second, _rows = tree_digest(root)
            self.assertNotEqual(first, second)


class WorktreeGitLinkTests(unittest.TestCase):
    """A review recorded from a git worktree must validate in a plain clone.

    ``git worktree add`` writes ``.git`` as a regular *file* holding an
    absolute ``gitdir:`` path that is unique to that worktree, where a normal
    clone has ``.git`` as a directory. The root skip list only skipped the
    directory form, so the file form was hashed and every worktree produced a
    different digest for the very same commit -- silently, and in the one
    workflow the contributing guide asks for.
    """

    def test_a_gitdir_link_file_is_excluded_like_the_git_directory(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            clean, _rows = tree_digest(root)
            (root / ".git").write_text(
                "gitdir: /somewhere/.git/worktrees/task-branch\n", encoding="utf-8")
            linked, rows = tree_digest(root)
            self.assertEqual(clean, linked)
            self.assertNotIn(".git", {row["path"] for row in rows})

    def test_two_worktrees_of_one_commit_agree_with_a_plain_clone(self):
        """The same content must hash the same from any checkout shape."""
        digests = []
        for gitlink in (None,
                        "gitdir: /a/.git/worktrees/one\n",
                        "gitdir: /b/very/different/path/.git/worktrees/two\n"):
            with TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
                if gitlink is None:
                    (root / ".git").mkdir()
                    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n",
                                                        encoding="utf-8")
                else:
                    (root / ".git").write_text(gitlink, encoding="utf-8")
                digests.append(tree_digest(root)[0])
        self.assertEqual(len(set(digests)), 1, digests)

    def test_a_nested_git_link_file_is_still_reviewed(self):
        """Only the repository root's .git is excluded, not any file so named."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "vendor"
            nested.mkdir()
            (nested / ".git").write_text("gitdir: /elsewhere\n", encoding="utf-8")
            first, rows = tree_digest(root)
            self.assertIn("vendor/.git", {row["path"] for row in rows})
            (nested / ".git").write_text("gitdir: /changed\n", encoding="utf-8")
            self.assertNotEqual(first, tree_digest(root)[0])


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
