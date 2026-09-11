import json
import os
import re
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pmos.release as release
import pmos_build_backend
from pmos.release import ProvenanceError, build_provenance, verify_provenance
from pmos import __version__


def _lowest_free_descriptor() -> int:
    """Return the lowest unused descriptor number; it rises when fds leak."""
    descriptor = os.open(os.devnull, os.O_RDONLY)
    os.close(descriptor)
    return descriptor


class ReleaseProvenanceTests(unittest.TestCase):
    def test_package_metadata_versions_are_identical(self):
        root = Path(__file__).parent
        pyproject = re.search(r'^version\s*=\s*"([^"]+)"',
                              (root / "pyproject.toml").read_text(encoding="utf-8"), re.M)
        self.assertIsNotNone(pyproject)
        self.assertEqual(pyproject.group(1), "0.8.0")
        self.assertEqual(pyproject.group(1), __version__)
        self.assertEqual(pyproject.group(1), pmos_build_backend._project()["version"])

    def test_hashes_categories_and_detects_tampering(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "templates").mkdir()
            (root / "skills/demo").mkdir(parents=True)
            (root / "routing").mkdir()
            (root / "templates/PRD.md").write_text("# PRD\n", encoding="utf-8")
            (root / "skills/demo/SKILL.md").write_text("# Skill\n", encoding="utf-8")
            (root / "routing/config.json").write_text("{}\n", encoding="utf-8")
            manifest = build_provenance(root)
            self.assertEqual(manifest["schema"], "pmos.release.v3")
            self.assertEqual(manifest["source_state"], "not-a-git-root")
            self.assertIsNone(manifest["source_commit"])
            self.assertEqual(set(manifest["counts"]), {"artifacts", "config", "skills"})
            self.assertTrue(verify_provenance(root, manifest).ok)
            forged_tree = json.loads(json.dumps(manifest))
            forged_tree["tree_sha256"] = "0" * 64
            forged_result = verify_provenance(root, forged_tree)
            self.assertFalse(forged_result.ok)
            self.assertIn("tree hash mismatch", forged_result.errors)
            (root / "templates/PRD.md").write_text("tampered\n", encoding="utf-8")
            self.assertFalse(verify_provenance(root, manifest).ok)

    def test_mapping_manifest_cannot_exclude_a_self_chosen_file(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "artifact.txt").write_text("safe\n", encoding="utf-8")
            manifest = build_provenance(root)
            (root / "forged.json").write_text("unrecorded\n", encoding="utf-8")
            forged = json.loads(json.dumps(manifest))
            forged["provenance_path"] = "forged.json"
            result = verify_provenance(root, forged)
            self.assertFalse(result.ok)
            self.assertIn("mapping manifest cannot choose a provenance exclusion", result.errors)

    def test_nested_runtime_named_directories_are_not_excluded(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("venv", ".pmos", ".tox"):
                path = root / "pmos" / name
                path.mkdir(parents=True, exist_ok=True)
                (path / "critical.py").write_text(name, encoding="utf-8")
            manifest = build_provenance(root)
            for name in ("venv", ".pmos", ".tox"):
                self.assertIn("pmos/%s/critical.py" % name, manifest["files"])
            self.assertTrue(verify_provenance(root, manifest).ok)

    def test_safe_symlink_round_trip_and_worktree_git_file_are_supported(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "artifact.txt").write_text("safe\n", encoding="utf-8")
            (root / "alias.txt").symlink_to("artifact.txt")
            # Linked Git worktrees contain this control file. It is metadata,
            # not a release artifact, and must be treated like a .git folder.
            (root / ".git").write_text("gitdir: /outside/control/path\n",
                                        encoding="utf-8")
            manifest = build_provenance(root)
            self.assertNotIn(".git", manifest["files"])
            self.assertEqual(manifest["files"]["alias.txt"]["kind"], "symlink")
            self.assertTrue(verify_provenance(root, manifest).ok)

            (root / "alias.txt").unlink()
            (root / "alias.txt").symlink_to("missing.txt")
            result = verify_provenance(root, manifest)
            self.assertFalse(result.ok)
            self.assertTrue(any("target is missing" in error
                                for error in result.errors))

    def test_regular_file_symlink_swap_during_hashing_fails_closed(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as outside_folder:
            root = Path(folder)
            victim = root / "victim.txt"
            victim.write_text("local\n", encoding="utf-8")
            external = Path(outside_folder) / "external.txt"
            external.write_text("external\n", encoding="utf-8")
            original_read = release.os.read
            swapped = False

            def swap_after_open(descriptor, size):
                nonlocal swapped
                chunk = original_read(descriptor, size)
                if chunk and not swapped:
                    victim.unlink()
                    victim.symlink_to(external)
                    swapped = True
                return chunk

            with patch.object(release.os, "read", side_effect=swap_after_open):
                with self.assertRaisesRegex(ProvenanceError, "release path changed while hashing"):
                    build_provenance(root)

    def test_nested_directory_replacement_during_inventory_fails_closed(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            nested = root / "nested"
            nested.mkdir()
            (nested / "proof.txt").write_text("safe", encoding="utf-8")
            outside = root / "outside"
            staged = root / "staged"
            real_open = release.os.open
            swapped = False

            def swap_nested(name, *args, **kwargs):
                nonlocal swapped
                if name == "nested" and not swapped:
                    nested.rename(staged)
                    outside.mkdir()
                    nested.symlink_to(outside, target_is_directory=True)
                    swapped = True
                return real_open(name, *args, **kwargs)

            with patch.object(release.os, "open", side_effect=swap_nested):
                with self.assertRaisesRegex(ProvenanceError, "cannot safely inventory"):
                    build_provenance(root)
            self.assertTrue(swapped)

    def test_symlink_replacement_during_inventory_fails_closed(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "proof.txt").write_text("safe", encoding="utf-8")
            alias = root / "alias.txt"
            alias.symlink_to("proof.txt")
            outside = root / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            real_readlink = release.os.readlink
            swapped = False

            def swap_link(name, *args, **kwargs):
                nonlocal swapped
                target = real_readlink(name, *args, **kwargs)
                if name == "alias.txt" and not swapped:
                    alias.unlink()
                    alias.symlink_to(outside)
                    swapped = True
                return target

            with patch.object(release.os, "readlink", side_effect=swap_link):
                with self.assertRaisesRegex(ProvenanceError, "symlink changed"):
                    build_provenance(root)
            self.assertTrue(swapped)

    def test_file_replaced_between_stat_and_open_fails_closed(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            victim = root / "artifact.txt"
            victim.write_text("original\n", encoding="utf-8")
            replacement = root / "replacement.txt"
            real_open = release.os.open
            swapped = False

            def swap_before_open(name, *args, **kwargs):
                nonlocal swapped
                if name == "artifact.txt" and not swapped:
                    swapped = True
                    replacement.write_text("substituted\n", encoding="utf-8")
                    replacement.replace(victim)
                return real_open(name, *args, **kwargs)

            with patch.object(release.os, "open", side_effect=swap_before_open):
                with self.assertRaisesRegex(ProvenanceError,
                                            "release path changed while hashing"):
                    build_provenance(root)
            self.assertTrue(swapped)

    def test_failed_build_does_not_leak_the_output_directory_descriptor(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            (root / ".env.example").write_text("KEY=\n", encoding="utf-8")
            output = root / release.DEFAULT_PROVENANCE
            with self.assertRaises(ProvenanceError):
                build_provenance(root, output=output)
            baseline = _lowest_free_descriptor()
            for _ in range(40):
                with self.assertRaises(ProvenanceError):
                    build_provenance(root, output=output)
            self.assertEqual(_lowest_free_descriptor(), baseline)

    def test_failed_provenance_write_leaves_no_temporary_in_the_tree(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            output = root / release.DEFAULT_PROVENANCE
            baseline = _lowest_free_descriptor()

            def refuse_write(descriptor, payload):
                raise OSError("disk full")

            with patch.object(release.os, "write", side_effect=refuse_write):
                with self.assertRaises(OSError):
                    build_provenance(root, output=output)
            self.assertEqual(sorted(item.name for item in output.parent.iterdir()), [])
            self.assertEqual(_lowest_free_descriptor(), baseline)

    def test_a_short_write_followed_by_a_real_failure_leaves_no_trace(self):
        """os.write() may write fewer bytes than asked without raising. A
        single unchecked call could publish a manifest truncated mid-object
        on the byte count where a later real failure (disk full) lands."""
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            output = root / release.DEFAULT_PROVENANCE
            baseline = _lowest_free_descriptor()
            real_write = release.os.write
            calls = []

            def short_then_fail(descriptor, payload):
                calls.append(payload)
                if len(calls) == 1:
                    return real_write(descriptor, payload[:8])
                raise OSError("disk full")

            with patch.object(release.os, "write", side_effect=short_then_fail):
                with self.assertRaises(OSError):
                    build_provenance(root, output=output)
            self.assertEqual(sorted(item.name for item in output.parent.iterdir()), [])
            self.assertEqual(_lowest_free_descriptor(), baseline)

    def test_a_complete_write_in_several_chunks_still_publishes_valid_json(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            output = root / release.DEFAULT_PROVENANCE
            real_write = release.os.write

            def chunked_write(descriptor, payload):
                return real_write(descriptor, payload[:16])

            with patch.object(release.os, "write", side_effect=chunked_write):
                manifest = build_provenance(root, output=output)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), manifest)
            self.assertTrue(verify_provenance(root, output).ok)

    def test_manifest_built_without_output_records_an_existing_provenance_file(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            default = release.DEFAULT_PROVENANCE.as_posix()
            written = build_provenance(root, output=root / release.DEFAULT_PROVENANCE)
            self.assertEqual(written["provenance_path"], default)
            self.assertNotIn(default, written["files"])
            manifest = build_provenance(root)
            self.assertNotIn("provenance_path", manifest)
            self.assertIn(default, manifest["files"])
            self.assertTrue(verify_provenance(root, manifest).ok)

    def test_output_is_json_without_content_or_secret(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            output = root / "docs/provenance.json"
            manifest = build_provenance(root, output=output)
            raw = output.read_text(encoding="utf-8")
            self.assertEqual(json.loads(raw), manifest)
            self.assertNotIn("safe", raw)
            self.assertTrue(verify_provenance(root, output).ok)

    def test_output_parent_swap_cannot_redirect_provenance_write(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            docs = root / "docs"
            docs.mkdir()
            outside = root / "outside"
            staged = root / "staged-docs"

            def swap_parent(*_args):
                docs.rename(staged)
                outside.mkdir()
                docs.symlink_to(outside, target_is_directory=True)
                return None, None

            with patch.object(release, "_git_identity", side_effect=swap_parent):
                build_provenance(root, output=docs / "provenance.json")
            self.assertFalse((outside / "provenance.json").exists())
            self.assertTrue((staged / "provenance.json").exists())

    def test_source_commit_is_bound_to_clean_current_git_head(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "release@test.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Release Test"],
                           cwd=root, check=True)
            (root / "artifact.txt").write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "add", "artifact.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                                  text=True, stdout=subprocess.PIPE).stdout.strip()
            manifest = build_provenance(root)
            self.assertEqual(manifest["source_state"], "git-clean")
            self.assertEqual(manifest["source_commit"], head)
            self.assertTrue(verify_provenance(root, manifest).ok)
            forged = json.loads(json.dumps(manifest))
            forged["source_commit"] = "0" * 40
            self.assertFalse(verify_provenance(root, forged).ok)
            with self.assertRaises(ProvenanceError):
                build_provenance(root, source_commit="0" * 40)

    def test_dirty_tree_is_never_attributed_to_head(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "release@test.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Release Test"],
                           cwd=root, check=True)
            (root / "tracked.txt").write_text("clean\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            (root / "tracked.txt").write_text("dirty\n", encoding="utf-8")
            manifest = build_provenance(root)
            self.assertEqual(manifest["source_state"], "git-dirty")
            self.assertIsNone(manifest["source_commit"])
            self.assertTrue(verify_provenance(root, manifest).ok)
            forged = json.loads(json.dumps(manifest))
            forged["source_state"] = "git-clean"
            forged["source_commit"] = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True,
                stdout=subprocess.PIPE).stdout.strip()
            self.assertFalse(verify_provenance(root, forged).ok)

    def test_untracked_default_provenance_file_does_not_dirty_a_library_call(self):
        # A library caller of build_provenance(root) (no `output`) should see
        # the tree as clean, and get a real source_commit, when the only
        # untracked file sitting in the tree is a default-path provenance
        # manifest written by a prior call. That manifest is excluded from
        # this call's own inventory already (it is recorded as an existing
        # file, per test_manifest_built_without_output_records_an_existing_
        # provenance_file); git identity must exclude it the same way, or
        # its own presence marks the tree dirty and hides source_commit.
        with TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "release@test.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Release Test"],
                           cwd=root, check=True)
            (root / "tracked.txt").write_text("clean\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                                  text=True, stdout=subprocess.PIPE).stdout.strip()
            # Writes the default-path manifest to disk, untracked, exactly as
            # a prior release step would leave it.
            written = build_provenance(root, output=root / release.DEFAULT_PROVENANCE)
            self.assertTrue(verify_provenance(root, root / release.DEFAULT_PROVENANCE).ok)
            manifest = build_provenance(root)
            self.assertEqual(manifest["source_state"], "git-clean")
            self.assertEqual(manifest["source_commit"], head)
            self.assertEqual(written["source_state"], "git-clean")
            self.assertEqual(written["source_commit"], head)

    def test_secret_like_path_blocks_build_and_cannot_hide_from_verification(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "release@test.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Release Test"],
                           cwd=root, check=True)
            (root / "artifact.txt").write_text("safe\n", encoding="utf-8")
            subprocess.run(["git", "add", "artifact.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "safe fixture"], cwd=root, check=True)
            safe_manifest = build_provenance(root)

            (root / ".env.production").write_text("not-a-real-secret\n", encoding="utf-8")
            subprocess.run(["git", "add", ".env.production"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "unsafe fixture"], cwd=root, check=True)
            with self.assertRaises(ProvenanceError):
                build_provenance(root)
            result = verify_provenance(root, safe_manifest)
            self.assertFalse(result.ok)
            self.assertTrue(any("secret-like path present" in error
                                for error in result.errors))

            (root / ".env.production").unlink()
            (root / ".env.production").symlink_to("artifact.txt")
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "unsafe symlink fixture"],
                           cwd=root, check=True)
            with self.assertRaises(ProvenanceError):
                build_provenance(root)
            symlink_result = verify_provenance(root, safe_manifest)
            self.assertFalse(symlink_result.ok)
            self.assertTrue(any("secret-like path present" in error
                                for error in symlink_result.errors))

            (root / ".env.production").unlink()
            subprocess.run(["git", "add", "-u", ".env.production"], cwd=root, check=True)
            (root / ".pmos").mkdir()
            (root / ".pmos/runtime-secret.txt").write_text(
                "mutable excluded state\n", encoding="utf-8")
            (root / "exported-artifact.txt").symlink_to(".pmos/runtime-secret.txt")
            subprocess.run(["git", "add", "exported-artifact.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "excluded target fixture"],
                           cwd=root, check=True)
            with self.assertRaises(ProvenanceError):
                build_provenance(root)
            excluded_result = verify_provenance(root, safe_manifest)
            self.assertFalse(excluded_result.ok)
            self.assertTrue(any("excluded or unrecorded state" in error
                                for error in excluded_result.errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
