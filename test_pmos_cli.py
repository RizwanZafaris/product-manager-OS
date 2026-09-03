import json
import hashlib
import os
import signal
import subprocess
import sys
import threading
import unittest
import shutil
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pmos.cli import _local_gate_verifier, _paths, main
from pmos.migrations import (create_legacy_fixture, migrate_workspace, recover_workspace,
                              rollback_workspace, MigrationError)
from pmos.store import Store
import pmos.migrations as migrations


class CliTests(unittest.TestCase):
    def test_init_status_verify_human_and_json(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            self.assertEqual(main(["--json", "status", "--path", folder]), 0)
            self.assertEqual(main(["verify", "--path", folder, "--json"]), 0)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                self.assertEqual(store.head("checkout").revision, 0)

    def test_user_supplied_evidence_flow_rejects_invalid_and_stale_submissions(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(main(["init", "--path", folder, "--product-id", "checkout"]), 0)
            invalid = {"class": "observed_behavior", "source": "real interview"}
            self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                   "--question-id", "first-outcome", "--answer", "A real outcome",
                                   "--evidence", json.dumps(invalid), "--expected-revision", "0:-",
                                   "--turn-id", "invalid-v1", "--json"]), 1)
            valid = {"class": "observed_behavior", "source": "interview-001",
                     "date": "2026-09-04", "location": "customer-call"}
            # The invalid attempt advanced the durable revision; using the old
            # token must fail closed rather than overwrite the challenge.
            self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                   "--question-id", "first-outcome", "--answer", "A real outcome",
                                   "--evidence", json.dumps(valid), "--expected-revision", "0:-",
                                   "--turn-id", "stale-v1", "--json"]), 1)
            with Store(Path(folder) / ".pmos/runtime.sqlite") as store:
                current = store.head("checkout").token
            answer_output = StringIO()
            with redirect_stdout(answer_output):
                self.assertEqual(main(["answer", "--path", folder, "--product-id", "checkout",
                                       "--question-id", "first-outcome", "--answer", "A real outcome",
                                       "--evidence", json.dumps(valid), "--expected-revision", current,
                                       "--turn-id", "valid-v1", "--json"]), 0)
            accepted = json.loads(answer_output.getvalue())
            next_revision = accepted["outcome"]["revision"]
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
                                       "--bank-id", "onboarding", "--evidence",
                                       json.dumps(gate_evidence),
                                       "--expected-revision", next_revision,
                                       "--turn-id", "gate-v1", "--json"]), 0)
            gated = json.loads(gate_output.getvalue())
            self.assertTrue(gated["outcome"]["completed"])

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
                self.assertEqual(store.head("checkout").revision, 0)

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
                self.assertEqual(store.head("checkout").revision, 0)
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
                    cwd=str(Path(__file__).parent), shell=False,
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
                cwd=str(Path(__file__).parent), shell=False,
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
                self.assertEqual(store.head("checkout").revision, 0)

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
                Path(__file__).parent, package_copy,
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
