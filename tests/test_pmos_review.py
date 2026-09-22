"""Tests for exact-tree independent review evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import subprocess

import review_gate
from review_gate import tree_digest, validate_attestation  # noqa: E402


def git_repo(root, ignore="._*\n"):
    """A real git repository, because tracked-ness is the thing under test."""
    def run(*args):
        return subprocess.run(('git',) + args, cwd=str(root), capture_output=True,
                              text=True, timeout=30)
    run('init', '-q')
    run('config', 'user.email', 'test@example.invalid')
    run('config', 'user.name', 'Review Fixture')
    (root / '.gitignore').write_text(ignore, encoding='utf-8')
    run('add', '.gitignore')
    return run


# The production transcript directory sits under docs/readiness/, and many
# classes here replace docs/ or docs/readiness/ with a symlink to prove the
# record and the gate refuse to follow it. A transcript under docs/ would then
# be refused first, and those tests would pass for the wrong reason. So the
# module runs with the directory moved to the tree's top level; the one test
# that needs the production value reads PRODUCTION_TRANSCRIPT_DIR.
PRODUCTION_TRANSCRIPT_DIR = review_gate.TRANSCRIPT_DIR
TEST_TRANSCRIPT_DIR = "review-transcripts/"
TRANSCRIPT = TEST_TRANSCRIPT_DIR + "reviewer-transcript.md"
_transcript_dir_patch = patch.object(review_gate, "TRANSCRIPT_DIR",
                                     TEST_TRANSCRIPT_DIR)


# Evidence may name only a check tools/ci_gate.py defines, and none of those
# can run in a temporary tree of three files. The classes here that test
# every other guard (the exit code, the result match, the excerpt, the
# transcript, the digest) therefore run with an allowlist that admits any
# command, from the tree root, with the default ceiling. The allowlist itself
# is tested by ReviewEvidenceAllowlistTests, which restores the real one.
REAL_EVIDENCE_ALLOWLIST = review_gate.evidence_allowlist


class _AnyFixtureCommand(dict):
    def get(self, key, default=None):
        return (".", review_gate.EVIDENCE_TIMEOUT_SECONDS)


_allowlist_patch = patch.object(review_gate, "evidence_allowlist",
                                lambda: _AnyFixtureCommand())


def setUpModule():
    _transcript_dir_patch.start()
    _allowlist_patch.start()


def tearDownModule():
    _allowlist_patch.stop()
    _transcript_dir_patch.stop()


def write_transcript(root, name="a.md", text="reviewer said: fine\n"):
    path = Path(root) / TEST_TRANSCRIPT_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return TEST_TRANSCRIPT_DIR + name


def attestation(root, **changes):
    # The transcript is written before the digest is taken because the record
    # requires it to be inside the tree it binds to; writing it afterwards
    # would stale every fixture built on this.
    transcript = Path(root) / TRANSCRIPT
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_text("reviewer output\n", encoding="utf-8")
    digest, _rows = tree_digest(root)
    document = {
        "schema": 1,
        "reviewer_id": "independent-test-reviewer",
        "reviewer_kind": "independent-agent",
        "independent_implementation": True,
        "identity_assurance": "unauthenticated-local-claim",
        "reviewed_at": "2026-09-03T00:00:00Z",
        "reviewed_tree_sha256": digest,
        "reviewer_transcript": TRANSCRIPT,
        "reviewer_transcript_sha256": hashlib.sha256(
            transcript.read_bytes()).hexdigest(),
        "scope": ["runtime", "tests", "gates"],
        "evidence": [{"command": "python3 -m unittest", "result": "OK",
                      "output": "Ran 3 tests in 0.01s\n\nOK\n",
                      "exit_code": 0}],
        "findings": [{"id": "R1", "severity": "P3", "status": "accepted",
                      "summary": "no defect found",
                      "evidence": "read the whole tree"}],
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

    def test_a_root_level_force_added_file_under_dist_is_reviewed(self):
        """The same bypass, one directory shallower: a root ROOT_SKIP_DIRS
        name (dist/, build/, .readiness/) must not exclude a file git
        actually tracks beneath it, the same way the nested case above and
        the ._ exclusion are protected."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            policy = root / "dist" / "policy.json"
            policy.parent.mkdir()
            policy.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "-f", "dist/policy.json")
            run("commit", "-qm", "init")
            self.assertIn("dist/policy.json", run("ls-files").stdout.split())
            first, first_rows = tree_digest(root)
            self.assertIn("dist/policy.json", {row["path"] for row in first_rows})
            policy.write_text('{"approved": true}\n', encoding="utf-8")
            second, _second_rows = tree_digest(root)
            self.assertNotEqual(first, second)

    def test_an_untracked_dist_directory_is_still_skipped(self):
        """The root-skip exclusion still applies when git tracks nothing
        beneath it, so an ordinary build scratch directory is not hashed."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            clean, _rows = tree_digest(root)
            scratch = root / "dist" / "untracked.json"
            scratch.parent.mkdir()
            scratch.write_text("{}\n", encoding="utf-8")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("dist/untracked.json", {row["path"] for row in rows})

    def test_a_local_product_workspace_does_not_move_the_recorded_tree(self):
        """products/ is where this repository tells every user to work, and it
        is gitignored, so a reviewer with one digested a tree no clean checkout
        has. The record then passed on that machine and failed in CI, naming
        only "1 criteria failing". That happened on 2026-09-21."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            clean, _rows = tree_digest(root)
            workspace = root / "products" / "acme" / "discovery"
            workspace.mkdir(parents=True)
            (workspace / "problem-framing.md").write_text("# Problem\n", encoding="utf-8")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("products/acme/discovery/problem-framing.md",
                             {row["path"] for row in rows})

    def test_a_tracked_file_under_products_is_still_hashed(self):
        """The skip is by name only while git carries nothing beneath it, the
        same guard every other root-skip directory gets: a force-added file
        there must still move the digest it is pinned to."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / ".gitignore").write_text("/products/\n", encoding="utf-8")
            tracked = root / "products" / "policy.json"
            tracked.parent.mkdir()
            tracked.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "app.py", ".gitignore")
            run("add", "-f", "products/policy.json")
            run("commit", "-qm", "init")
            first, first_rows = tree_digest(root)
            self.assertIn("products/policy.json", {row["path"] for row in first_rows})
            tracked.write_text('{"approved": true}\n', encoding="utf-8")
            second, _second_rows = tree_digest(root)
            self.assertNotEqual(first, second)

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
                             ["review attestation does not use the closed "
                              "schema (unexpected trust_me)"])

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


class TrackedMetadataNameTests(unittest.TestCase):
    """A filename that resembles metadata must not exempt tracked content.

    The AppleDouble exclusion shipped in 0b2a466 matched any name beginning
    "._" outright, and its commit message claimed git could not track such a
    file. That claim was wrong: `git add -f` overrides .gitignore, so a tracked
    ._policy.json was force-added, omitted from the reviewed inventory, and its
    contents could be flipped from {"approved": false} to {"approved": true}
    without changing the digest a recorded review is pinned to.

    The rule is therefore tracked-aware: git decides what is reviewable, and a
    name only excuses a file from review when git is not carrying it.
    """

    def test_a_force_added_dot_underscore_file_is_reviewed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            policy = root / "._policy.json"
            policy.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "-f", "._policy.json")
            run("add", "app.py")
            run("commit", "-qm", "init")
            self.assertIn("._policy.json", run("ls-files").stdout.split())
            _digest, rows = tree_digest(root)
            self.assertIn("._policy.json", {row["path"] for row in rows})

    def test_editing_a_tracked_dot_underscore_file_stales_the_review(self):
        """The exact bypass: flipping a tracked approval flag must be caught."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            policy = root / "._policy.json"
            policy.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "-f", "._policy.json")
            run("commit", "-qm", "init")
            document = attestation(root)
            self.assertEqual(validate_attestation(document, root), [])
            policy.write_text('{"approved": true}\n', encoding="utf-8")
            self.assertTrue(any("stale" in error for error in
                                validate_attestation(document, root)))

    def test_an_untracked_sidecar_is_still_excluded(self):
        """Reproducibility across filesystems must survive the tighter rule."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            clean, _rows = tree_digest(root)
            (root / "._app.py").write_bytes(b"\x00\x05\x16\x07AppleDouble")
            (root / ".DS_Store").write_bytes(b"\x00\x00\x00\x01Bud1")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("._app.py", {row["path"] for row in rows})

    def test_a_tracked_nested_dot_underscore_file_is_reviewed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            package = root / "pmos"
            package.mkdir()
            nested = package / "._rules.json"
            nested.write_text('{"allow": false}\n', encoding="utf-8")
            run("add", "-f", "pmos/._rules.json")
            run("commit", "-qm", "init")
            first, rows = tree_digest(root)
            self.assertIn("pmos/._rules.json", {row["path"] for row in rows})
            nested.write_text('{"allow": true}\n', encoding="utf-8")
            self.assertNotEqual(first, tree_digest(root)[0])

    def test_a_tracked_dot_underscore_symlink_is_reviewed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "real.py").write_text("SAFE = True\n", encoding="utf-8")
            link = root / "._link"
            link.symlink_to("real.py")
            run("add", "-f", "._link")
            run("add", "real.py")
            run("commit", "-qm", "init")
            _digest, rows = tree_digest(root)
            entry = {(r["path"], r["kind"]) for r in rows}
            self.assertIn(("._link", "symlink"), entry)

    def test_a_tracked_pyc_is_reviewed_but_an_untracked_one_is_not(self):
        """The same bypass class applies to the compiled-artifact exclusion."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root, ignore="*.pyc\n")
            blob = root / "vendored.pyc"
            blob.write_bytes(b"\x00payload-one")
            run("add", "-f", "vendored.pyc")
            run("commit", "-qm", "init")
            first, rows = tree_digest(root)
            self.assertIn("vendored.pyc", {row["path"] for row in rows})
            blob.write_bytes(b"\x00payload-two")
            self.assertNotEqual(first, tree_digest(root)[0])
            (root / "scratch.pyc").write_bytes(b"\x00untracked")
            self.assertNotIn("scratch.pyc",
                             {r["path"] for r in tree_digest(root)[1]})

    def test_ordinary_tracked_source_changes_still_stale_the_review(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            source = root / "app.py"
            source.write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            document = attestation(root)
            self.assertEqual(validate_attestation(document, root), [])
            source.write_text("SAFE = False\n", encoding="utf-8")
            self.assertTrue(any("stale" in error for error in
                                validate_attestation(document, root)))

    def test_it_fails_closed_when_the_git_index_cannot_be_read(self):
        """An unreadable index must never be treated as 'nothing is tracked'."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            # A metadata-shaped entry is what forces the tracked-ness question.
            (root / "._policy.json").write_text('{"approved": true}\n',
                                                encoding="utf-8")
            with patch.object(review_gate, "_git",
                              side_effect=OSError("git unavailable")):
                with self.assertRaises(OSError):
                    tree_digest(root)

    def test_a_plain_directory_that_is_not_a_repository_still_works(self):
        """Tests and ad-hoc trees are not git repositories; excluding is safe there."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            clean, _rows = tree_digest(root)
            (root / "._app.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            self.assertEqual(clean, tree_digest(root)[0])


class TrackedFilenameByteFidelityTests(unittest.TestCase):
    """A CR byte inside a tracked filename must not vanish from the review.

    ``_git`` ran ``subprocess.run`` with ``text=True``. Universal-newline
    translation rewrites a bare CR to LF inside decoded output, including
    inside the NUL-delimited byte stream ``git ls-files -z`` prints. A
    tracked filename that itself contains a literal CR byte therefore comes
    back from ``tracked_paths`` spelled with an LF instead, the tracked-set
    lookup for the real on-disk name misses, and a metadata-shaped file git
    is genuinely carrying is silently excluded from the digest a recorded
    review is pinned to.
    """

    def test_a_tracked_filename_with_a_bare_cr_byte_is_reviewed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            name = "._policy\r.json"
            policy = root / name
            policy.write_bytes(b'{"approved": false}\n')
            run("add", "-f", name)
            run("commit", "-qm", "init")

            raw = subprocess.run(["git", "ls-files", "-z"], cwd=str(root),
                                 capture_output=True, timeout=30)
            self.assertIn(b"._policy\r.json\x00", raw.stdout,
                         "fixture setup did not track the exact CR filename")

            _digest, rows = tree_digest(root)
            self.assertIn(name, {row["path"] for row in rows})

            policy.write_bytes(b'{"approved": true}\n')
            self.assertNotEqual(_digest, tree_digest(root)[0])


class GitDiscoveryFailureFailsClosedTests(unittest.TestCase):
    """A nonzero rev-parse exit is not proof there is no repository to protect.

    ``tracked_paths`` treated any nonzero ``rev-parse --is-inside-work-tree``
    exit as "not a work tree" and returned ``None``, which lets every
    metadata-shaped file be excluded on the theory that there is no tracked
    content to lose. But git also exits nonzero for reasons that have
    nothing to do with whether a repository exists here -- dubious
    ownership, permissions, a broken config -- and those must not be treated
    as an empty tracked set.
    """

    def test_a_dubious_ownership_style_failure_raises_instead_of_excluding(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            policy = root / "._policy.json"
            policy.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "-f", "._policy.json")
            run("add", "app.py")
            run("commit", "-qm", "init")

            real_git = review_gate._git

            def dubious_ownership(target_root, *args):
                if args[:1] == ("rev-parse",):
                    return subprocess.CompletedProcess(
                        args=("git",) + args, returncode=128, stdout="",
                        stderr="fatal: detected dubious ownership in repository at "
                              + str(target_root))
                return real_git(target_root, *args)

            with patch.object(review_gate, "_git", side_effect=dubious_ownership):
                with self.assertRaises(OSError):
                    tree_digest(root)


class GitDiscoveryConservatismTests(unittest.TestCase):
    """Only git's own "no repository" statement may authorise an exclusion.

    The dubious-ownership case is one instance of a general rule. Recognition
    has to be positive: an exit whose reason is unrecognised -- a permission
    failure, a broken object store, or git speaking a language this pattern
    does not match -- must fail closed rather than be read as "nothing is
    tracked here".
    """

    def _repo_with_tracked_sidecar(self, root):
        run = git_repo(root)
        (root / "._policy.json").write_text('{"approved": false}\n',
                                            encoding="utf-8")
        run("add", "-f", "._policy.json")
        run("commit", "-qm", "init")
        return run

    def _rev_parse_failure(self, root, stderr, returncode=128):
        real_git = review_gate._git

        def failing(target_root, *args):
            if args[:1] == ("rev-parse",):
                return subprocess.CompletedProcess(
                    args=("git",) + args, returncode=returncode,
                    stdout="", stderr=stderr)
            return real_git(target_root, *args)
        return failing

    def test_an_unrecognised_failure_reason_raises(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._repo_with_tracked_sidecar(root)
            failing = self._rev_parse_failure(
                root, "fatal: could not read Permission denied")
            with patch.object(review_gate, "_git", side_effect=failing):
                with self.assertRaises(OSError):
                    tree_digest(root)

    def test_a_localised_git_message_fails_closed_rather_than_excluding(self):
        """A translated fatal message is unrecognised, so it must not pass."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._repo_with_tracked_sidecar(root)
            failing = self._rev_parse_failure(
                root, "fatal: ce n'est pas un depot git")
            with patch.object(review_gate, "_git", side_effect=failing):
                with self.assertRaises(OSError):
                    tree_digest(root)

    def test_a_real_missing_repository_is_still_recognised(self):
        """The positive path must keep working against real git output."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / "._runtime.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            digest, rows = tree_digest(root)
            self.assertNotIn("._runtime.py", {row["path"] for row in rows})
            self.assertTrue(digest)


class DamagedRepositoryTests(unittest.TestCase):
    """A repository git cannot read is not an absence of a repository.

    Renaming .git/objects away makes `rev-parse --is-inside-work-tree` answer
    with the identical "fatal: not a git repository" line a plain directory
    produces. Matching that wording therefore excluded a tracked file from a
    damaged repository and left the digest unmoved when it was edited. Real
    git, no mocked discovery.
    """

    def _repo(self, root):
        run = git_repo(root)
        (root / "._policy.json").write_text('{"approved": false}\n',
                                            encoding="utf-8")
        run("add", "-f", "._policy.json")
        run("commit", "-qm", "init")
        return run

    def test_an_unreadable_object_store_fails_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._repo(root)
            os.rename(root / ".git" / "objects",
                      root / ".git" / "objects-unavailable")
            with self.assertRaises(OSError):
                tree_digest(root)

    def test_a_repository_missing_its_head_fails_closed(self):
        """Verified: a missing HEAD or refs/ produces the same fatal wording.

        A missing .git/config does NOT -- git exits 0 and carries on with
        defaults -- so it is deliberately not used here.
        """
        for damaged in ("HEAD", "refs"):
            with self.subTest(damaged=damaged):
                with TemporaryDirectory() as directory:
                    root = Path(directory)
                    self._repo(root)
                    os.rename(root / ".git" / damaged,
                              root / ".git" / (damaged + "-gone"))
                    with self.assertRaises(OSError):
                        tree_digest(root)

    def test_a_plain_directory_is_still_not_a_repository(self):
        """The ordinary standalone-directory path must keep working."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / "._runtime.py").write_bytes(b"\x00\x05\x16\x07sidecar")
            digest, rows = tree_digest(root)
            self.assertNotIn("._runtime.py", {row["path"] for row in rows})
            self.assertTrue(digest)

    def test_a_worktree_gitdir_pointer_counts_as_control_metadata(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime.py").write_text("SAFE = True\n", encoding="utf-8")
            (root / ".git").write_text("gitdir: /nowhere/.git/worktrees/x\n",
                                       encoding="utf-8")
            self.assertTrue(review_gate.git_control_present(root))


class RootSkipDirectoryTrackedContentTests(unittest.TestCase):
    """A root scratch directory name must not excuse tracked content either.

    ROOT_SKIP_DIRS (.readiness, build, dist, venv, .tox, and *.egg-info) was
    skipped by name before tracked_set() was ever consulted, the same defect
    class the ._ exclusion was fixed for. `git add -f` overrides .gitignore,
    so a tracked file can sit inside one of these directories and change
    content without moving the digest a recorded review is pinned to.
    """

    def test_a_force_added_root_dist_file_is_reviewed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "dist").mkdir()
            policy = root / "dist" / "policy.json"
            policy.write_text('{"approved": false}\n', encoding="utf-8")
            run("add", "-f", "dist/policy.json")
            run("commit", "-qm", "init")
            self.assertIn("dist/policy.json", run("ls-files").stdout.split())
            first, rows = tree_digest(root)
            self.assertIn("dist/policy.json", {row["path"] for row in rows})
            policy.write_text('{"approved": true}\n', encoding="utf-8")
            self.assertNotEqual(first, tree_digest(root)[0])

    def test_an_untracked_root_dist_directory_is_still_excluded(self):
        """Reproducibility for ordinary build output must survive the tighter rule."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = git_repo(root)
            (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
            run("add", "app.py")
            run("commit", "-qm", "init")
            clean, _rows = tree_digest(root)
            (root / "dist").mkdir()
            (root / "dist" / "wheel.whl").write_bytes(b"not tracked")
            dirty, rows = tree_digest(root)
            self.assertEqual(clean, dirty)
            self.assertNotIn("dist/wheel.whl", {row["path"] for row in rows})


class RecentAuthorsUnreadableHistoryTests(unittest.TestCase):
    """recent_authors must not fail open when git history cannot be read.

    It used to return an empty set on any git failure, so record_review could
    proceed with an arbitrary reviewer identity whenever author history could
    not be inspected -- the self-attestation defense failed open exactly when
    it mattered. "git told us nothing" and "git tracks nothing" must not
    collapse into the same answer, the same distinction tracked_paths() makes
    for the reviewed tree itself.
    """

    def _repo_with_unreadable_history(self, root):
        run = git_repo(root)
        (root / "app.py").write_text("SAFE = True\n", encoding="utf-8")
        run("add", "app.py")
        run("commit", "-qm", "init")
        os.rename(root / ".git" / "objects", root / ".git" / "objects-unavailable")
        return run

    def test_recent_authors_returns_none_for_a_damaged_object_store(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._repo_with_unreadable_history(root)
            self.assertIsNone(review_gate.recent_authors(root))

    def test_recent_authors_is_still_empty_for_a_repository_with_no_commits(self):
        """The positive, real cases must keep returning an empty set."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            git_repo(root)
            self.assertEqual(set(), review_gate.recent_authors(root))

    def test_recent_authors_is_still_empty_outside_any_repository(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(set(), review_gate.recent_authors(root))


class ReadinessRecordCommitFieldTests(unittest.TestCase):
    """A readiness record's commit field must never pre-fill a literal SHA.

    EXT-USER-session-script.md once pre-filled "Commit under test" with a
    commit that was already 61 commits behind HEAD by the time a session ran
    the script, so an observer filling in the block as written would certify
    stale code. The fix is the same one EXT-TEAM-review-brief.md's "Commit
    reviewed" field already used: instruct the observer to run
    `git rev-parse HEAD` themselves rather than reading a value off the page.
    This guards every docs/readiness/*.md file against the same mistake
    recurring, not just the one file it was found in.
    """

    COMMIT_FIELD_RE = re.compile(
        r"^(Commit under test|Commit reviewed)\s*:\s*[`\"']?([0-9a-f]{7,40})\b",
        re.MULTILINE)

    def test_no_readiness_doc_pre_fills_a_literal_commit_sha(self):
        readiness_dir = Path(__file__).resolve().parent.parent / "docs" / "readiness"
        offenders = []
        for path in sorted(readiness_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for match in self.COMMIT_FIELD_RE.finditer(text):
                offenders.append("%s: %r" % (path.name, match.group(0)))
        self.assertEqual([], offenders,
                         "a readiness record pre-fills a commit SHA that "
                         "will go stale rather than asking for "
                         "`git rev-parse HEAD` at session time")

    def test_the_pattern_itself_catches_a_pre_filled_sha(self):
        """The regex must actually fire, not just pass vacuously above."""
        sample = "Commit under test     : ba286db0121e613f5c1a6a6d3bdfa3cc6bee2c27\n"
        self.assertTrue(self.COMMIT_FIELD_RE.search(sample))
        backticked = "Commit under test: `ba286db`\n"
        self.assertTrue(self.COMMIT_FIELD_RE.search(backticked))
        quoted = 'Commit reviewed: "ba286db0121e613f5c1a6a6d3bdfa3cc6bee2c27"\n'
        self.assertTrue(self.COMMIT_FIELD_RE.search(quoted))
        safe = "Commit under test     : (output of git rev-parse HEAD)\n"
        self.assertFalse(self.COMMIT_FIELD_RE.search(safe))


class AttestationSymlinkTests(unittest.TestCase):
    """A symlink at the canonical attestation path must never be followed.

    ``tree_digest`` deliberately excludes ``docs/readiness/independent-review.json``
    from the hash a review is bound to -- it is the record, not reviewed
    content -- so a symlink planted at exactly that path is invisible to the
    digest that is supposed to catch tampering. Reading or writing through it
    with a symlink-following API (``Path.read_text`` / ``Path.write_text``)
    would let an attacker substitute an attestation written for a different
    tree, or clobber an arbitrary file the symlink points at, without either
    ever showing up as a stale digest.
    """

    def test_record_review_refuses_to_write_through_a_symlink(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-target-%d" % os.getpid())
            outside.write_text("do not touch\n", encoding="utf-8")
            try:
                canonical = root / review_gate.ATTESTATION
                canonical.parent.mkdir(parents=True, exist_ok=True)
                canonical.symlink_to(outside)

                import argparse
                args = argparse.Namespace(
                    record=True, attestation=str(canonical),
                    reviewer="A. Reviewer", reviewer_kind="human",
                    scope=["templates/"],
                    evidence=["python3 tools/ci_gate.py|17/18"],
                    finding=None, verdict="accepted", digest=False)
                code = review_gate.record_review(args, root)

                self.assertEqual(2, code)
                self.assertEqual(
                    "do not touch\n", outside.read_text(encoding="utf-8"),
                    "a refused record write still clobbered the symlink target")
                self.assertTrue(
                    canonical.is_symlink(),
                    "the refusal should leave the symlink in place, not replace it")
            finally:
                outside.unlink(missing_ok=True)

    def test_validation_flow_refuses_to_read_through_a_symlink(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-planted-%d" % os.getpid())
            outside.write_text(json.dumps(attestation(root)), encoding="utf-8")
            try:
                canonical = root / review_gate.ATTESTATION
                canonical.parent.mkdir(parents=True, exist_ok=True)
                canonical.symlink_to(outside)

                # main() resolves --attestation against, and validates
                # against, the module-level REPO; patch it to this tmp tree
                # (now that _read_attestation requires an in-root path) so
                # the read path is exercised end to end without touching the
                # real repository tree.
                with patch.object(review_gate, "REPO", root):
                    code = review_gate.main(["--attestation", str(canonical)])

                self.assertEqual(1, code)
            finally:
                outside.unlink(missing_ok=True)

    def test_write_attestation_helper_rejects_a_symlink_directly(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / ("attn-helper-target-%d" % os.getpid())
            outside.write_text("do not touch\n", encoding="utf-8")
            try:
                canonical = root / "independent-review.json"
                canonical.symlink_to(outside)
                with self.assertRaises(OSError):
                    review_gate._write_attestation(canonical, "{}\n", root)
                self.assertEqual("do not touch\n", outside.read_text(encoding="utf-8"))
            finally:
                outside.unlink(missing_ok=True)

    def test_write_attestation_helper_requires_root(self):
        """root used to be optional, with a fallback that reached the parent
        directory by plain pathname resolution -- the round-2 bug again,
        just reachable through this helper's own default. Finding P3-1: make
        it required so that fallback cannot exist to reintroduce."""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "independent-review.json"
            with self.assertRaises(TypeError):
                review_gate._write_attestation(path, "{}\n")

    def test_read_attestation_helper_rejects_a_symlink_directly(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / ("attn-helper-source-%d" % os.getpid())
            outside.write_text("{}\n", encoding="utf-8")
            try:
                canonical = root / "independent-review.json"
                canonical.symlink_to(outside)
                with self.assertRaises(OSError):
                    review_gate._read_attestation(canonical, root)
            finally:
                outside.unlink(missing_ok=True)


class AttestationParentSymlinkTests(unittest.TestCase):
    """A symlink at a *parent directory* of the attestation path must never
    be followed either, and record_review must never create one.

    Round 2 of the same finding: the leaf-level fix above (commit a419774)
    closed the case where ``docs/readiness/independent-review.json`` is
    itself a symlink. But ``_write_attestation`` still reached that file by
    walking ``docs`` and ``docs/readiness`` as plain pathname components --
    ``os.makedirs`` to create a missing one, a bare ``os.open(str(path))`` to
    write the file inside it -- and pathname resolution follows a symlink at
    any component that is not the final one. Replacing ``docs`` (or
    ``docs/readiness``) with a symlink to a directory outside the reviewed
    tree therefore sent the write there instead, with ``record_review``
    still reporting success. This class is that traversal, one directory
    shallower each time, plus the two ordinary-tree cases the fix must not
    break: recording still works in a clean tree, and a missing
    ``docs/readiness/`` is still created (safely) when absent.
    """

    def _args(self, root, attestation, **over):
        import argparse
        fields = dict(
            record=True, attestation=str(attestation),
            reviewer="A. Reviewer", reviewer_kind="human",
            scope=["templates/"], evidence=["echo 17 of 18 passed|17 of 18"],
            finding=["P3|accepted|no defect found|read templates/"],
            transcript=write_transcript(root), verdict="accepted",
            digest=False)
        fields.update(over)
        return argparse.Namespace(**fields)

    def test_refuses_when_docs_is_a_symlink_to_outside_the_tree(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-parent-docs-%d" % os.getpid())
            outside.mkdir()
            try:
                canonical = root / review_gate.ATTESTATION
                (root / "docs").symlink_to(outside, target_is_directory=True)

                code = review_gate.record_review(
                    self._args(root, canonical), root)

                self.assertEqual(2, code)
                self.assertEqual(
                    [], list(outside.rglob("*")),
                    "the refused write reached the directory the docs/ "
                    "symlink pointed at")
                self.assertFalse(
                    (root / "docs" / "readiness").exists(),
                    "record_review must not resolve through the docs/ "
                    "symlink to fabricate a readiness/ directory beyond it")
            finally:
                import shutil
                shutil.rmtree(outside, ignore_errors=True)

    def test_refuses_when_docs_readiness_is_a_symlink_to_outside_the_tree(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            (root / "docs").mkdir()
            outside = root.parent / ("attn-parent-readiness-%d" % os.getpid())
            outside.mkdir()
            try:
                canonical = root / review_gate.ATTESTATION
                (root / "docs" / "readiness").symlink_to(
                    outside, target_is_directory=True)

                code = review_gate.record_review(
                    self._args(root, canonical), root)

                self.assertEqual(2, code)
                self.assertEqual(
                    [], list(outside.rglob("*")),
                    "the refused write reached the directory the "
                    "docs/readiness/ symlink pointed at")
            finally:
                import shutil
                shutil.rmtree(outside, ignore_errors=True)

    def test_refuses_when_the_attestation_file_itself_is_a_symlink(self):
        """The leaf case, kept alongside the parent-traversal cases above so
        this class stands on its own as the round-2 regression set."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-parent-leaf-%d" % os.getpid())
            outside.write_text("do not touch\n", encoding="utf-8")
            try:
                canonical = root / review_gate.ATTESTATION
                canonical.parent.mkdir(parents=True, exist_ok=True)
                canonical.symlink_to(outside)

                code = review_gate.record_review(
                    self._args(root, canonical), root)

                self.assertEqual(2, code)
                self.assertEqual(
                    "do not touch\n", outside.read_text(encoding="utf-8"))
                self.assertTrue(canonical.is_symlink())
            finally:
                outside.unlink(missing_ok=True)

    def test_still_records_normally_and_creates_missing_readiness_dir(self):
        """The ordinary case the fix must not break: no docs/readiness/ yet,
        nothing malicious anywhere, a plain first recording."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            canonical = root / review_gate.ATTESTATION
            self.assertFalse((root / "docs").exists())

            code = review_gate.record_review(
                self._args(root, canonical), root)

            self.assertEqual(0, code)
            self.assertTrue((root / "docs" / "readiness").is_dir())
            self.assertFalse((root / "docs" / "readiness").is_symlink())
            document = json.loads(canonical.read_text(encoding="utf-8"))
            self.assertEqual([], validate_attestation(document, root))

    def test_refuses_a_dot_dot_component_in_the_attestation_path(self):
        """Round 2's own gap, found by the adversarial verifier against the
        walk above: ``path.relative_to(root)`` is a string comparison of
        path segments, not a filesystem resolution. A literal ``..``
        segment survives it -- ``root / ".." / "escape.json"`` reads as a
        child of ``root`` by that comparison alone -- and the walk then
        genuinely opens ``..`` with ``dir_fd=parent_fd``: that entry always
        exists, is always a directory, and is never a symlink, so none of
        the walk's existing checks catch it. This is exactly the gap the
        containment check's own error message ("not inside root; refusing")
        was supposed to close."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")

            code = review_gate.record_review(
                self._args(root, "../escape-dotdot.json"), root)

            self.assertEqual(2, code)
            self.assertFalse((root.parent / "escape-dotdot.json").exists())
            self.assertFalse((root / "escape-dotdot.json").exists())

    def test_refuses_an_embedded_dot_dot_component_in_the_attestation_path(self):
        """Same gap, reached through an existing directory rather than as
        the leading component -- ``docs/../../outside/escape.json`` walks
        into the real ``docs/`` first, then back out through the ``..``
        entries exactly as above."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            (root / "docs").mkdir()

            code = review_gate.record_review(
                self._args(root, "docs/../../outside/escape2.json"), root)

            self.assertEqual(2, code)
            self.assertFalse((root.parent / "outside").exists())
            self.assertFalse((root / "outside").exists())


class AttestationReadPathTests(unittest.TestCase):
    """The read side (``_read_attestation``, exercised through ``main()``)
    needs the same parent-directory protection the write side already has.

    Commit 2c3485f fixed ``_write_attestation`` for a symlinked ``docs`` or
    ``docs/readiness``: pathname resolution follows a symlink at any
    component that is not the final one, so a symlink at either parent
    directory sent a write wherever it pointed while ``record_review``
    still reported success. ``_read_attestation`` had the identical bug on
    the read side -- ``O_NOFOLLOW`` on a bare ``os.open(str(path), ...)``
    only refuses a symlink at the *final* component -- so a symlinked
    ``docs`` or ``docs/readiness`` holding an otherwise well-formed,
    digest-matching attestation validated cleanly even though the file
    actually read was never inside the reviewed tree: the writer refused
    that layout, but the gate would read and accept it. Every test here
    patches the module-level ``REPO`` to a throwaway tree so the real
    repository is never touched, and proves the case fails against the
    pre-fix reader (a plain ``os.open`` with leaf-only ``O_NOFOLLOW``) before
    proving it is refused by the fixed one.
    """

    def test_refuses_when_docs_is_a_symlink_to_outside_the_tree(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-read-docs-%d" % os.getpid())
            (outside / "readiness").mkdir(parents=True)
            try:
                (root / "docs").symlink_to(outside, target_is_directory=True)
                # A well-formed attestation, digest-matching root, planted
                # exactly where the docs/ symlink resolves it to.
                (outside / "readiness" / "independent-review.json").write_text(
                    json.dumps(attestation(root)), encoding="utf-8")

                with patch.object(review_gate, "REPO", root):
                    code = review_gate.main([])

                self.assertEqual(
                    1, code,
                    "a symlinked docs/ let the gate read and accept an "
                    "attestation living outside the reviewed tree")
            finally:
                import shutil
                shutil.rmtree(outside, ignore_errors=True)

    def test_refuses_when_docs_readiness_is_a_symlink_to_outside_the_tree(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            (root / "docs").mkdir()
            outside = root.parent / ("attn-read-readiness-%d" % os.getpid())
            outside.mkdir()
            try:
                (root / "docs" / "readiness").symlink_to(
                    outside, target_is_directory=True)
                (outside / "independent-review.json").write_text(
                    json.dumps(attestation(root)), encoding="utf-8")

                with patch.object(review_gate, "REPO", root):
                    code = review_gate.main([])

                self.assertEqual(
                    1, code,
                    "a symlinked docs/readiness/ let the gate read and "
                    "accept an attestation living outside the reviewed tree")
            finally:
                import shutil
                shutil.rmtree(outside, ignore_errors=True)

    def test_a_normal_attestation_still_validates(self):
        """The ordinary case the fix must not break: a real docs/readiness/,
        a well-formed attestation sitting where it belongs, read and
        accepted through main() exactly as before."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            canonical = root / review_gate.ATTESTATION
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(json.dumps(attestation(root)), encoding="utf-8")

            with patch.object(review_gate, "REPO", root):
                code = review_gate.main([])

            self.assertEqual(0, code)

    def test_refuses_a_dot_dot_component_in_the_attestation_argument(self):
        """Confirms the earlier finding stays fixed on the read path too:
        ``docs/../../outside/escape.json`` walks into the real ``docs/``
        first, then back out through literal ``..`` entries, which a plain
        ``os.open(str(path), ...)`` resolves like any other pathname."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            (root / "docs").mkdir()
            outside_dir = root.parent / "outside"
            outside_dir.mkdir()
            try:
                (outside_dir / "escape.json").write_text(
                    json.dumps(attestation(root)), encoding="utf-8")

                with patch.object(review_gate, "REPO", root):
                    code = review_gate.main(
                        ["--attestation", "docs/../../outside/escape.json"])

                self.assertEqual(
                    1, code,
                    "a '..' component in --attestation let the gate read "
                    "and accept an attestation living outside the reviewed "
                    "tree")
            finally:
                import shutil
                shutil.rmtree(outside_dir, ignore_errors=True)

    def test_refuses_an_absolute_attestation_argument_outside_root(self):
        """No symlink and no ``..`` at all here -- just a plain absolute
        path outside the tree, holding a well-formed, digest-matching
        attestation. Before the containment check this validated cleanly,
        because an absolute --attestation is used as-is and nothing then
        checked it was actually inside the reviewed tree."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            outside = root.parent / ("attn-read-outside-%d" % os.getpid())
            outside.write_text(json.dumps(attestation(root)), encoding="utf-8")
            try:
                with patch.object(review_gate, "REPO", root):
                    code = review_gate.main(["--attestation", str(outside)])

                self.assertEqual(
                    1, code,
                    "an absolute --attestation path outside root was read "
                    "and accepted instead of refused")
            finally:
                outside.unlink(missing_ok=True)


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
            scope=["templates/"], evidence=["echo 17 of 18 passed|17 of 18"],
            finding=["P3|accepted|no defect found|read templates/"],
            transcript=write_transcript(root), verdict="accepted",
            digest=False)
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

    def test_it_refuses_to_record_when_history_cannot_be_inspected(self):
        """recent_authors() must fail closed: an unreadable history must
        refuse the recording rather than be treated as an empty author set
        (which would let a self-attestation through by accident)."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = git_repo(root)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            run("add", "a.md")
            run("commit", "-qm", "init")
            (root / ".git" / "HEAD").write_text("garbage\n", encoding="utf-8")
            self.assertIsNone(review_gate.recent_authors(root))
            code = review_gate.record_review(self._args(root), root)
            self.assertEqual(2, code)
            self.assertFalse((root / review_gate.ATTESTATION).exists(),
                             "a review whose history could not be read still wrote a record")

    def test_it_refuses_to_record_when_recent_authors_returns_none(self):
        """The fail-open case: a reviewer git cannot vouch for must not slip through."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("content\n", encoding="utf-8")
            with patch.object(review_gate, "recent_authors", return_value=None):
                code = review_gate.record_review(
                    self._args(root, reviewer="Alice"), root)
            self.assertEqual(2, code)
            self.assertFalse((root / review_gate.ATTESTATION).exists(),
                             "a refused record was written despite unreadable history")

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



PY = shlex.quote(sys.executable)


class ReviewRecordCarriesEvidenceTests(unittest.TestCase):
    """A record must carry what was run, not what was typed.

    Every case here was accepted before. One command -- no model consulted,
    an evidence command never run, zero findings -- wrote a record the gate
    passed: `--evidence "python3 tools/ci_gate.py|26/26 passed"` on a tree
    that was not 26/26, and "findings : 0". validate_attestation checked only
    that evidence was a non-empty list, so an edited result, a result nobody
    saw and a real one were indistinguishable, and the schema had no field
    that could bind the reviewer's own output to the tree.

    These prove the half that is checkable. The other half -- that a model
    outside the authoring session actually read the change -- no command in
    this repository can distinguish from a typed record, and the last case
    here pins the tool to saying so.
    """

    def _args(self, root, **over):
        import argparse
        canonical = root / review_gate.ATTESTATION
        canonical.parent.mkdir(parents=True, exist_ok=True)
        (root / "a.md").write_text("content\n", encoding="utf-8")
        transcript = write_transcript(root, "transcript.md")
        fields = dict(
            record=True, attestation=str(canonical),
            reviewer="A. Reviewer", reviewer_kind="independent-agent",
            scope=["a.md"],
            evidence=["echo 24 of 25 passed|24 of 25",
                      "echo lint clean|lint clean"],
            finding=["P3|accepted|no defect found|read a.md"],
            transcript=transcript, verdict="accepted", digest=False)
        fields.update(over)
        return argparse.Namespace(**fields)

    def _record(self, root, **over):
        import contextlib
        import io
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = review_gate.record_review(self._args(root, **over), root)
        return code, out.getvalue()

    def _gate(self, root):
        import contextlib
        import io
        out = io.StringIO()
        with patch.object(review_gate, "REPO", root), \
                contextlib.redirect_stdout(out):
            code = review_gate.main([])
        return code, out.getvalue()

    def test_a_result_the_command_did_not_print_is_refused(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(
                root, evidence=["echo 24 of 25 passed|26/26 passed"])
            self.assertEqual(2, code, out)
            self.assertIn("'echo 24 of 25 passed'", out)
            self.assertIn("you recorded : 26/26 passed", out)
            self.assertIn("it printed   : 24 of 25 passed", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists(),
                             "a refused fabrication still wrote a record")

    def test_a_record_with_no_findings_is_refused(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, finding=None)
            self.assertEqual(2, code, out)
            self.assertIn("--finding is required", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists())
            # And the gate refuses one written by hand, since the tool is not
            # the only way a record reaches the tree.
            document = attestation(root, findings=[])
            self.assertTrue(any("findings cannot be empty" in error for error
                                in validate_attestation(document, root)))

    def test_a_missing_or_mis_hashed_transcript_fails_the_gate(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            # A second committed file in the transcript directory, present
            # before the digest, so repointing at it is a hash mismatch and
            # not a staleness.
            other = write_transcript(root, "other.md", "a different file\n")
            self.assertEqual(0, self._record(root)[0])
            record = root / review_gate.ATTESTATION
            good = json.loads(record.read_text(encoding="utf-8"))
            self.assertEqual([], validate_attestation(good, root))

            # The record edited, the tree untouched. The attestation file is
            # outside its own digest, so staleness cannot see either of these;
            # only the transcript check does, which is why it exists.
            repointed = dict(good, reviewer_transcript=other)
            self.assertEqual(
                ["reviewer transcript %s does not hash to the value the "
                 "record carries" % other],
                validate_attestation(repointed, root))
            digit = good["reviewer_transcript_sha256"]
            rehashed = dict(good, reviewer_transcript_sha256=(
                "1" if digit[0] == "0" else "0") + digit[1:])
            self.assertEqual(
                ["reviewer transcript %stranscript.md does not hash to the "
                 "value the record carries" % TEST_TRANSCRIPT_DIR],
                validate_attestation(rehashed, root))

            (root / TEST_TRANSCRIPT_DIR / "transcript.md").unlink()
            errors = validate_attestation(good, root)
            self.assertIn("reviewer transcript %stranscript.md is not a file "
                          "in the reviewed tree" % TEST_TRANSCRIPT_DIR, errors)
            code, out = self._gate(root)
            self.assertEqual(1, code)
            self.assertIn("transcript.md is not a file in the reviewed tree",
                          out)

    def test_a_one_character_edit_to_a_recorded_result_fails_naming_the_item(self):
        """The mandatory seeded defect, through the gate's own entry point."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(0, self._record(root)[0])
            self.assertEqual(0, self._gate(root)[0])
            record = root / review_gate.ATTESTATION
            document = json.loads(record.read_text(encoding="utf-8"))
            self.assertEqual("lint clean", document["evidence"][1]["result"])
            document["evidence"][1]["result"] = "lint clear"
            record.write_text(json.dumps(document, indent=2) + "\n",
                              encoding="utf-8")
            code, out = self._gate(root)
            self.assertEqual(1, code, out)
            self.assertIn("review evidence 2 (echo lint clean): the recorded "
                          "result does not appear in the output recorded for "
                          "that command", out)
            self.assertNotIn("review evidence 1", out)

    def test_what_is_stored_is_what_the_command_printed_and_how_it_exited(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=[
                "%s -c \"import sys; sys.stderr.write('to-stderr\\n'); "
                "sys.exit(3)\"|exit=3|to-stderr" % PY])
            self.assertEqual(0, code, out)
            item = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))["evidence"][0]
            self.assertEqual("to-stderr\n", item["output"])
            self.assertEqual(3, item["exit_code"])

    def test_a_long_output_is_kept_as_a_window_that_still_holds_the_result(self):
        output = "x" * 10000 + "MATCH" + "y" * 10000
        excerpt = review_gate.evidence_excerpt(output, "MATCH", limit=100)
        self.assertIn("MATCH", excerpt)
        self.assertLess(len(excerpt), 200)
        self.assertIn("characters elided", excerpt)
        self.assertEqual("short", review_gate.evidence_excerpt("short", "sh"))

    def test_the_tool_states_what_its_guard_cannot_prove(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, recorded = self._record(root)
            self.assertEqual(0, code)
            gate_code, gated = self._gate(root)
            self.assertEqual(0, gate_code)
            self.assertIn("identity not authenticated", recorded)
            self.assertIn("identity is not authenticated", gated)
            for out in (recorded, gated):
                flat = " ".join(out.split())
                self.assertIn("compares the reviewer string to the", flat)
                self.assertIn("git reports for this tree's last 40 commits",
                              flat)
                self.assertIn("cannot fire on a model name in this repository",
                              flat)
                self.assertIn("independent_implementation is set true by this "
                              "tool. It is not elicited from the reviewer",
                              flat)


class ReviewRecordBypassTests(unittest.TestCase):
    """Each way the first hardening could still be sidestepped, closed.

    An independent check of that hardening wrote records the gate accepted
    anyway: an evidence command chained with ``; echo 26/26 passed``, a
    command that exited 2 accepted because its output contained the result,
    a hand-written record whose result and output agreed, and README.md named
    as the reviewer transcript. It also found guards nothing pinned. Every
    test here fails when the guard it names is reverted.

    The fixture helpers are shared with ReviewRecordCarriesEvidenceTests
    by reference rather than by inheritance, so that class's cases run once.
    """

    _args = ReviewRecordCarriesEvidenceTests._args
    _record = ReviewRecordCarriesEvidenceTests._record
    _gate = ReviewRecordCarriesEvidenceTests._gate

    def test_a_command_cannot_chain_a_second_program_to_print_its_result(self):
        # Guard: run_evidence splits with shlex and runs no shell.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=[
                "%s -c pass; echo 26/26 passed|26/26 passed" % PY])
            self.assertEqual(2, code, out)
            self.assertIn("the result you recorded is not in its output", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists())

    def test_an_unparseable_command_is_refused_not_crashed_on(self):
        # Guard: shlex's ValueError becomes a named refusal.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=["echo 'unclosed|x"])
            self.assertEqual(2, code, out)
            self.assertIn("could not be parsed", out)

    def test_a_failing_command_is_refused_even_when_its_output_matches(self):
        # Guard: the exit code must be the expected one (0 unless declared).
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            failing = ("%s -c \"print('release gates: 24/25 passed'); "
                       "raise SystemExit(1)\"" % PY)
            code, out = self._record(root, evidence=[failing + "|passed"])
            self.assertEqual(2, code, out)
            self.assertIn("exited 1; the evidence expects 0", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists())
            # Declared, the same red run is recordable, and says it was red.
            code, out = self._record(root, evidence=[
                failing + "|exit=1|release gates: 24/25 passed"])
            self.assertEqual(0, code, out)
            item = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))["evidence"][0]
            self.assertEqual(1, item["exit_code"])
            self.assertEqual("release gates: 24/25 passed", item["result"])

    def test_a_refusal_shows_the_end_of_a_long_output(self):
        # Guard: refusal_display keeps the tail, where a sweep's verdict is.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=[
                "%s -c \"print('[PASS] x' * 400); "
                "print('release gates: 24/25 passed')\"|26/26 passed" % PY])
            self.assertEqual(2, code, out)
            self.assertIn("release gates: 24/25 passed", out)
            self.assertIn("characters elided", out)

    def test_a_transcript_outside_the_transcript_directory_is_refused(self):
        # Guard: transcript_path_error, on both the record and the gate.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("readme\n", encoding="utf-8")
            code, out = self._record(root, transcript="README.md")
            self.assertEqual(2, code, out)
            self.assertIn("is not under %s" % TEST_TRANSCRIPT_DIR, out)
            dotted = TEST_TRANSCRIPT_DIR + "../README.md"
            code, out = self._record(root, transcript=dotted)
            self.assertEqual(2, code, out)

            self.assertEqual(0, self._record(root)[0])
            good = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))
            readme = hashlib.sha256(b"readme\n").hexdigest()
            forged = dict(good, reviewer_transcript="README.md",
                          reviewer_transcript_sha256=readme)
            self.assertEqual(
                ["reviewer transcript README.md is not under %s: a transcript "
                 "is a file put there to be one, not any file already in the "
                 "tree" % TEST_TRANSCRIPT_DIR],
                validate_attestation(forged, root))

    def test_the_production_transcript_directory_is_under_docs_readiness(self):
        self.assertEqual("docs/readiness/review-transcripts/",
                         PRODUCTION_TRANSCRIPT_DIR)

    def test_a_missing_transcript_is_refused_before_any_command_runs(self):
        # Guard: the early is_file() refusal in record_review.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "ran.txt"
            code, out = self._record(
                root, transcript=TEST_TRANSCRIPT_DIR + "absent.md",
                evidence=["%s -c \"open('ran.txt', 'w').write('x'); "
                          "print('ran')\"|ran" % PY])
            self.assertEqual(2, code, out)
            self.assertIn("does not exist", out)
            self.assertFalse(marker.exists(),
                             "an evidence command ran before a missing "
                             "transcript was refused")

    def test_a_command_that_writes_into_the_tree_does_not_stale_the_record(self):
        # Guard: record_review digests the tree after the evidence runs.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=[
                "%s -c \"open('made.txt', 'w').write('x'); print('made')\"|made"
                % PY])
            self.assertEqual(0, code, out)
            self.assertTrue((root / "made.txt").exists())
            document = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))
            self.assertEqual([], validate_attestation(document, root))

    def test_record_refuses_each_missing_input(self):
        # Guards: --transcript required, empty RESULT refused, a program that
        # cannot be started refused.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, transcript="  ")
            self.assertEqual(2, code, out)
            self.assertIn("--transcript is required", out)
            code, out = self._record(root, evidence=["echo ok|  "])
            self.assertEqual(2, code, out)
            self.assertIn("with both sides filled", out)
            code, out = self._record(root, evidence=["echo ok|exit=0|"])
            self.assertEqual(2, code, out)
            self.assertIn("with both sides filled", out)
            code, out = self._record(
                root, evidence=["no-such-program-r8 --x|anything"])
            self.assertEqual(2, code, out)
            self.assertIn("could not be run", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists())

    def test_a_transcript_removed_by_an_evidence_command_is_refused(self):
        # Guard: the row lookup after the digest, which is what decides.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            gone = TEST_TRANSCRIPT_DIR + "transcript.md"
            code, out = self._record(root, evidence=[
                "%s -c \"import os; os.remove('%s'); print('gone')\"|gone"
                % (PY, gone)])
            self.assertEqual(2, code, out)
            self.assertIn("is not a file in the reviewed tree", out)
            self.assertFalse((root / review_gate.ATTESTATION).exists())

    def test_the_validator_rejects_a_missing_or_malformed_transcript_field(self):
        # Guards: the path and digest shape checks in _transcript_errors.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                ["reviewer transcript path is missing"],
                validate_attestation(attestation(root, reviewer_transcript=""),
                                     root))
            self.assertEqual(
                ["reviewer transcript digest is malformed"],
                validate_attestation(
                    attestation(root, reviewer_transcript_sha256="abc"), root))
            unshaped = attestation(root)
            del unshaped["reviewer_transcript"]
            self.assertEqual(
                ["review attestation does not use the closed schema "
                 "(missing reviewer_transcript)"],
                validate_attestation(unshaped, root))

    def _item_errors(self, **changes):
        item = {"command": "echo ok", "result": "ok", "output": "ok\n",
                "exit_code": 0}
        item.update(changes)
        return review_gate._evidence_errors([item])

    def test_the_validator_rejects_each_malformed_evidence_field(self):
        # Guards: each field check in _evidence_errors.
        self.assertEqual([], self._item_errors())
        self.assertEqual(
            ["review evidence 1 (unnamed command): command is missing"],
            self._item_errors(command="   "))
        self.assertEqual(
            ["review evidence 1 (echo ok): recorded output is missing"],
            self._item_errors(output=None))
        self.assertEqual(
            ["review evidence 1 (echo ok): recorded result is empty"],
            self._item_errors(result=" "))
        for bad in ("0", False, None):
            self.assertEqual(
                ["review evidence 1 (echo ok): recorded exit code is not an "
                 "integer"], self._item_errors(exit_code=bad), repr(bad))
        self.assertIn("does not use the closed evidence schema",
                      review_gate._evidence_errors([{"command": "x"}])[0])

    def test_reexecute_rejects_a_hand_written_self_consistent_record(self):
        # Guard: reexecution_errors, reached through main(["--reexecute"]).
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(0, self._record(root)[0])
            record = root / review_gate.ATTESTATION
            document = json.loads(record.read_text(encoding="utf-8"))
            self.assertEqual(0, self._gate_args(root, ["--reexecute"])[0])
            # Never run, and consistent with itself: a plain gate run accepts
            # it, which is the limit the docstrings now state.
            document["evidence"][0] = {
                "command": "%s -c \"print('release gates: 24/25 passed')\""
                           % PY,
                "result": "release gates: 26/26 passed",
                "output": "release gates: 26/26 passed\n", "exit_code": 0}
            record.write_text(json.dumps(document, indent=2) + "\n",
                              encoding="utf-8")
            code, out = self._gate(root)
            self.assertEqual(0, code, out)
            self.assertIn("not re-run; --reexecute re-runs it", out)
            code, out = self._gate_args(root, ["--reexecute"])
            self.assertEqual(1, code, out)
            self.assertIn("review evidence 1 (", out)
            self.assertIn("re-run output does not contain the recorded result",
                          out)
            # An exit code edited on its own is caught the same way.
            document["evidence"][0] = dict(
                json.loads(record.read_text(encoding="utf-8"))["evidence"][0],
                command="echo 24 of 25 passed", result="24 of 25",
                output="24 of 25 passed\n", exit_code=5)
            record.write_text(json.dumps(document, indent=2) + "\n",
                              encoding="utf-8")
            code, out = self._gate_args(root, ["--reexecute"])
            self.assertEqual(1, code, out)
            self.assertIn("re-run exited 0, the record says 5", out)

    def _gate_args(self, root, argv):
        import contextlib
        import io
        out = io.StringIO()
        with patch.object(review_gate, "REPO", root), \
                contextlib.redirect_stdout(out):
            code = review_gate.main(argv)
        return code, out.getvalue()

    def test_reexecute_reports_a_command_that_cannot_be_started(self):
        # Guard: reexecution_errors' OSError catch. Without it a recorded
        # program missing from this machine crashes --reexecute.
        with TemporaryDirectory() as tmp:
            document = {"evidence": [
                {"command": "no-such-program-r8 --x", "result": "x",
                 "output": "x\n", "exit_code": 0}]}
            errors = review_gate.reexecution_errors(document, Path(tmp))
            self.assertEqual(1, len(errors), errors)
            self.assertTrue(errors[0].startswith(
                "review evidence 1 (no-such-program-r8 --x): re-run failed: "),
                errors[0])

    def test_a_command_runs_the_way_ci_gate_runs_its_gate(self):
        # Guards: run_evidence uses the form's cwd, ci_gate's environment
        # with PYTHONPATH at the reviewed tree's tests/, and the running
        # interpreter for "python3", as ci_gate.run_gate does.
        probe = ("python3 -c \"import os, sys; print(sys.executable); "
                 "print(os.getcwd()); print(os.environ.get('PYTHONPATH')); "
                 "print(os.environ.get('R8_LEAK'))\"")
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sub").mkdir()
            form = {tuple(shlex.split(probe)): ("sub", 60)}
            with patch.object(review_gate, "evidence_allowlist",
                              lambda: form), \
                    patch.dict(os.environ, {"R8_LEAK": "leaked"}):
                output, code = review_gate.run_evidence(probe, root)
            self.assertEqual(0, code, output)
            executable, cwd, pythonpath, leak = output.splitlines()
            self.assertEqual(os.path.realpath(sys.executable),
                             os.path.realpath(executable))
            self.assertEqual(os.path.realpath(root / "sub"),
                             os.path.realpath(cwd))
            self.assertEqual(str(root / "tests"), pythonpath)
            self.assertEqual("None", leak)

    def test_a_command_is_stopped_at_its_forms_timeout(self):
        # Guard: run_evidence passes the form's timeout, not a fixed ceiling.
        command = "python3 -c \"import time; time.sleep(4)\""
        form = {tuple(shlex.split(command)): (".", 1)}
        with TemporaryDirectory() as tmp, \
                patch.object(review_gate, "evidence_allowlist", lambda: form):
            with self.assertRaises(OSError) as caught:
                review_gate.run_evidence(command, Path(tmp))
        self.assertEqual("it did not finish within 1 seconds",
                         str(caught.exception))

    def test_record_stores_a_window_that_holds_a_late_result(self):
        # Guard: record_review stores evidence_excerpt(output, result), not
        # the raw output and not a head cut that drops the matched text.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = self._record(root, evidence=[
                "%s -c \"print('x' * 9000); print('LATE-RESULT')\"|LATE-RESULT"
                % PY])
            self.assertEqual(0, code, out)
            item = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))["evidence"][0]
            self.assertIn("LATE-RESULT", item["output"])
            self.assertTrue(item["output"].startswith("[... "),
                            item["output"][:60])
            self.assertLess(len(item["output"]),
                            review_gate.EVIDENCE_OUTPUT_LIMIT + 100)
            self.assertEqual([], validate_attestation(json.loads(
                (root / review_gate.ATTESTATION).read_text(encoding="utf-8")),
                root))

    def test_each_elision_marker_names_its_own_cut(self):
        # Guards: the leading and the trailing marker in evidence_excerpt,
        # each present exactly when that side was cut.
        output = "x" * 10000 + "MATCH" + "y" * 10000
        excerpt = review_gate.evidence_excerpt(output, "MATCH", limit=100)
        self.assertEqual("[... 9953 characters elided ...]\n"
                         + output[9953:10053]
                         + "\n[... 9952 characters elided ...]", excerpt)
        head = review_gate.evidence_excerpt("MATCH" + "y" * 500, "MATCH",
                                            limit=100)
        self.assertEqual("MATCH" + "y" * 95
                         + "\n[... 405 characters elided ...]", head)
        tail = review_gate.evidence_excerpt("x" * 500 + "MATCH", "MATCH",
                                            limit=100)
        self.assertEqual("[... 405 characters elided ...]\n"
                         + "x" * 95 + "MATCH", tail)


class ReviewEvidenceAllowlistTests(unittest.TestCase):
    """Evidence may name only a check this repository defines.

    Three rounds tried a denylist of command runners, and each round an
    unlisted one restored the chain: ``sh -c 'python3 lint.py --os; echo
    26/26 passed'`` was accepted by --record, the plain gate and
    --reexecute, and after sh was listed the same chain came back behind
    ``find -exec`` and a git ``!`` alias. Re-running such a command cannot
    expose it, because echo really prints the result. These tests run with
    the real allowlist, read from tools/ci_gate.py, and each fails when that
    allowlist is reverted.
    """

    _args = ReviewRecordCarriesEvidenceTests._args
    _record = ReviewRecordCarriesEvidenceTests._record
    _item_errors = ReviewRecordBypassTests._item_errors
    _gate_args = ReviewRecordBypassTests._gate_args

    PROBE = "sh -c 'python3 lint.py --os; echo 26/26 passed'"

    def setUp(self):
        real = patch.object(review_gate, "evidence_allowlist",
                            REAL_EVIDENCE_ALLOWLIST)
        real.start()
        self.addCleanup(real.stop)

    def test_the_probe_and_every_other_wrapper_are_refused_at_record(self):
        # Guard: evidence_form's allowlist lookup, reached through
        # run_evidence at record time. Nothing may run: the last command
        # would write ran.txt if it did.
        wrappers = (
            self.PROBE,
            "find . -maxdepth 0 -exec sh -c "
            "'python3 lint.py --os; echo 26/26 passed' ;",
            "git -c 'alias.x=!echo 26/26 passed' x",
            "echo 26/26 passed",
            "python3 -c \"open('ran.txt', 'w'); print('26/26 passed')\"",
        )
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for command in wrappers:
                code, out = self._record(
                    root, evidence=[command + "|26/26 passed"])
                self.assertEqual(2, code, out)
                self.assertIn("it is not a check this repository defines", out)
                self.assertIn("tools/ci_gate.py", out)
                self.assertIn("EVIDENCE_COMMANDS", out)
                self.assertFalse((root / review_gate.ATTESTATION).exists(),
                                 command)
            self.assertFalse((root / "ran.txt").exists())

    def test_extra_or_changed_arguments_are_refused_unless_in_the_form(self):
        # Guard: the lookup is on the whole argv, not on the program.
        for command in ("python3 lint.py --os --verbose",
                        "python3 lint.py",
                        "python3.11 lint.py --os",
                        "python3 lint.py --os; echo 26/26 passed",
                        "python3 tools/ci_gate.py --gate os-tree --gate compile",
                        "python3 tools/ci_gate.py --gate no-such-gate",
                        "python3 tools/ci_gate.py --manifest"):
            with self.assertRaises(OSError, msg=command) as caught:
                review_gate.evidence_form(command)
            self.assertIn("not a check this repository defines",
                          str(caught.exception))
        # Arguments that are part of an allowlisted form are accepted, and
        # quoting or spacing that splits to the same argv is the same form.
        self.assertEqual(["python3", "tools/ci_gate.py", "--gate", "os-tree"],
                         review_gate.evidence_form(
                             "python3 tools/ci_gate.py --gate os-tree")[0])
        self.assertEqual(["python3", "lint.py", "--os"],
                         review_gate.evidence_form("'python3' lint.py   --os")[0])

    def test_every_gate_argv_is_accepted_with_that_gates_cwd_and_timeout(self):
        # Guards: evidence_allowlist reads GATES, keeps each gate's cwd and
        # timeout, and adds EVIDENCE_COMMANDS; and that list is exactly the
        # full sweep plus the sweep narrowed to one gate, so an entry added
        # there (an echo, a shell) turns this red.
        import ci_gate
        for gate in ci_gate.GATES:
            self.assertEqual(
                (list(gate.argv), gate.cwd, gate.timeout),
                review_gate.evidence_form(shlex.join(gate.argv)), gate.gate_id)
        self.assertEqual(
            {("python3", "tools/ci_gate.py")} |
            {("python3", "tools/ci_gate.py", "--gate", gate.gate_id)
             for gate in ci_gate.GATES},
            set(ci_gate.EVIDENCE_COMMANDS))
        for argv in ci_gate.EVIDENCE_COMMANDS:
            self.assertEqual(
                (list(argv), ".", review_gate.EVIDENCE_TIMEOUT_SECONDS),
                review_gate.evidence_form(shlex.join(argv)))
        self.assertIn(("python3", "-m", "unittest", "test_lint", "-v"),
                      {tuple(g.argv) for g in ci_gate.GATES
                       if g.cwd == "modules/regulated"})

    def test_a_real_gate_command_is_accepted_by_record_gate_and_reexecute(self):
        # The positive case, end to end, on a copy of this repository: the
        # json-syntax gate's own argv is recorded, the plain gate accepts
        # the record, and --reexecute re-runs it and matches.
        import shutil
        repo = Path(review_gate.REPO)
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "tree"
            shutil.copytree(repo, root, symlinks=True,
                            ignore=shutil.ignore_patterns(
                                "__pycache__", "products", "._*", ".DS_Store"))
            code, out = self._record(root, evidence=[
                "python3 lint.py --json-syntax|every tracked .json file "
                "parses"])
            self.assertEqual(0, code, out)
            item = json.loads((root / review_gate.ATTESTATION).read_text(
                encoding="utf-8"))["evidence"][0]
            self.assertEqual("python3 lint.py --json-syntax", item["command"])
            self.assertEqual(0, item["exit_code"])
            code, out = self._gate_args(root, [])
            self.assertEqual(0, code, out)
            self.assertIn("exact tree accepted", out)
            code, out = self._gate_args(root, ["--reexecute"])
            self.assertEqual(0, code, out)
            self.assertIn("every recorded command re-run here and matched",
                          out)

    def test_the_plain_gate_rejects_a_stored_command_record_would_refuse(self):
        # Guard: the evidence_form call in _evidence_errors. A hand-written
        # record is the only way such a command reaches the tree.
        errors = self._item_errors(command=self.PROBE)
        self.assertEqual(1, len(errors), errors)
        self.assertTrue(errors[0].startswith(
            "review evidence 1 (%s): --record would refuse to run it: it is "
            "not a check this repository defines" % self.PROBE), errors[0])
        self.assertEqual([], self._item_errors(command="python3 lint.py --os"))
        errors = self._item_errors(command="python3 lint.py --os 'x")
        self.assertEqual(1, len(errors), errors)
        self.assertIn("--record would refuse to run it: it could not be "
                      "parsed", errors[0])

    def test_reexecute_refuses_a_stored_command_that_is_not_allowlisted(self):
        # Guard: reexecution_errors reaches evidence_form through
        # run_evidence, so --reexecute never runs the probe.
        with TemporaryDirectory() as tmp:
            document = {"evidence": [
                {"command": self.PROBE, "result": "26/26 passed",
                 "output": "26/26 passed\n", "exit_code": 0}]}
            errors = review_gate.reexecution_errors(document, Path(tmp))
        self.assertEqual(1, len(errors), errors)
        self.assertTrue(errors[0].startswith(
            "review evidence 1 (%s): re-run failed: it is not a check this "
            "repository defines" % self.PROBE), errors[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
