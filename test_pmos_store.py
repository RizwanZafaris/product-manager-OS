"""Executable contract for the local PM OS managed runtime."""

from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from pmos.store import (
    MemoryClass,
    QueueStatus,
    Store,
    ValidationError,
    IntegrityError,
    NotFoundError,
    canonical_json,
    sha256,
)


class StoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.path = Path(self.temp.name) / "runtime.sqlite"
        self.store = Store(self.path)

    def tearDown(self) -> None:
        self.store.close()
        self.temp.cleanup()

    def test_pragmas_and_atomic_full_snapshot_commit(self) -> None:
        self.assertEqual(self.store._conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)
        self.assertEqual(self.store._conn.execute("PRAGMA synchronous").fetchone()[0], 2)  # FULL
        self.assertEqual(self.store._conn.execute("PRAGMA trusted_schema").fetchone()[0], 0)
        self.store.create_product("ledger")
        first = self.store.commit("ledger", {"docs/a.md": "one", "docs/b.md": "two"})
        self.assertTrue(first.committed)
        old = self.store.read_snapshot("ledger")
        proposal = self.store.prepare_commit("ledger", {"docs/a.md": "changed"}, old.head)
        # An unpublished full snapshot is durable but never visible to readers.
        self.assertEqual(self.store.read_snapshot("ledger").files, old.files)
        self.assertTrue(self.store.publish(proposal).committed)
        self.assertEqual(self.store.read_snapshot("ledger").files, {"docs/a.md": b"changed"})
        self.assertTrue(self.store.verify().ok)

    def test_stale_compare_and_swap_is_an_explicit_conflict(self) -> None:
        self.store.create_product("p")
        base = self.store.head("p")
        a = self.store.prepare_commit("p", {"a": "a"}, base)
        b = self.store.prepare_commit("p", {"b": "b"}, base)
        self.assertTrue(self.store.publish(a).committed)
        stale = self.store.publish(b)
        self.assertEqual(stale.status, "conflict")
        self.assertEqual(stale.conflict.code, "stale_revision")
        self.assertEqual(self.store.read_snapshot("p").files, {"a": b"a"})

    def test_concurrent_local_writers_and_reader_snapshot(self) -> None:
        self.store.create_product("p")
        base = self.store.head("p")
        proposals = [self.store.prepare_commit("p", {"a": "one"}, base),
                     self.store.prepare_commit("p", {"b": "two"}, base)]
        barrier = threading.Barrier(3)
        results = []

        def writer(proposal):
            other = Store(self.path)
            try:
                barrier.wait()
                results.append(other.publish(proposal.commit_hash))
            finally:
                other.close()

        threads = [threading.Thread(target=writer, args=(proposal,)) for proposal in proposals]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(item.status for item in results), ["committed", "conflict"])
        # A reader sees one immutable commit, never a half-assembled map.
        snap = self.store.read_snapshot("p")
        self.assertIn(snap.files, ({"a": b"one"}, {"b": b"two"}))

    def test_one_store_instance_serializes_concurrent_callers(self) -> None:
        barrier = threading.Barrier(9)
        results = []
        failures = []

        def enqueue(index):
            try:
                barrier.wait()
                results.append(self.store.enqueue(
                    {"index": index}, idempotency_key="thread-%d" % index))
            except Exception as exc:  # captured for an explicit assertion below
                failures.append(exc)

        threads = [threading.Thread(target=enqueue, args=(index,))
                   for index in range(8)]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()
        self.assertEqual(failures, [])
        self.assertEqual(len(results), 8)
        self.assertEqual(len(self.store.list_jobs()), 8)
        self.assertTrue(self.store.verify().ok)

    def test_reopen_prepared_and_published_crash_boundaries(self) -> None:
        self.store.create_product("p")
        proposal = self.store.prepare_commit("p", {"state.md": "prepared"})
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(self.store.read_snapshot("p").files, {})
        self.assertTrue(self.store.publish(proposal.commit_hash).committed)
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(self.store.read_snapshot("p").files, {"state.md": b"prepared"})
        self.assertTrue(self.store.verify().ok)

    def test_process_kill_commit_boundaries_are_atomic(self) -> None:
        probe = Path(__file__).resolve().parent / "tools" / "runtime_crash_probe.py"
        expectations = {
            "prepare.before_commit": (0, 0),
            "prepare.after_commit": (0, 1),
            "publish.before_commit": (0, 1),
            "publish.after_commit": (1, 1),
            "enqueue.before_commit": (0, 0),
            "enqueue.after_commit": (1, 0),
            "memory.before_commit": (0, 0),
            "memory.after_commit": (1, 0),
        }
        for point, (visible, prepared_count) in expectations.items():
            with self.subTest(point=point), TemporaryDirectory() as folder:
                database = Path(folder) / "crash.sqlite"
                completed = subprocess.run(
                    [sys.executable, str(probe), str(database), point],
                    cwd=str(Path(__file__).resolve().parent), shell=False,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    timeout=20)
                self.assertEqual(completed.returncode, -signal.SIGKILL,
                                 msg=completed.stdout + completed.stderr)
                reopened = Store(database)
                try:
                    operation = point.split(".", 1)[0]
                    if operation in ("prepare", "publish"):
                        self.assertEqual(reopened.head("crash-product").revision,
                                         visible)
                        count = reopened._conn.execute(
                            "SELECT count(*) FROM prepared_commits").fetchone()[0]
                        self.assertEqual(count, prepared_count)
                        expected_files = ({"state.md": b"published payload"}
                                          if visible else {})
                        self.assertEqual(
                            reopened.read_snapshot("crash-product").files,
                            expected_files)
                    elif operation == "enqueue":
                        self.assertEqual(len(reopened.list_jobs()), visible)
                    else:
                        self.assertEqual(len(reopened.retrieve_task_memory(
                            "crash-task")), visible)
                    self.assertTrue(reopened.verify().ok)
                finally:
                    reopened.close()

    def test_cross_store_commit_pack_and_stale_conflict(self) -> None:
        self.store.create_product("p")
        base = self.store.prepare_commit("p", {"v": "base"})
        base_pack = self.store.export_pack(base)
        self.assertTrue(self.store.publish(base).committed)
        other = Store(Path(self.temp.name) / "other.sqlite")
        self.addCleanup(other.close)
        self.assertEqual(other.import_pack(base_pack).status, "committed")
        proposal = self.store.prepare_commit("p", {"v": "source"}, self.store.head("p"))
        pack = self.store.export_pack(proposal)
        self.assertTrue(other.commit("p", {"v": "target"}, other.head("p")).committed)
        imported = other.import_pack(pack)
        self.assertEqual(imported.status, "conflict")
        self.assertEqual(imported.conflict.code, "stale_revision")
        self.assertEqual(other.read_snapshot("p").files, {"v": b"target"})

    def test_pack_rejects_corruption_and_traversal(self) -> None:
        self.store.create_product("p")
        prepared = self.store.prepare_commit("p", {"safe/path": "data"})
        raw = self.store.export_pack(prepared)
        corrupted = raw[:-1] + (b" " if raw[-1:] != b" " else b"!")
        with self.assertRaises((ValidationError, IntegrityError)):
            self.store.import_pack(corrupted)
        decoded = json.loads(raw)
        decoded["files"][0]["path"] = "../escape"
        core = {key: decoded[key] for key in ("format", "commit", "expected_revision", "files")}
        decoded["pack_hash"] = sha256(canonical_json(core))
        with self.assertRaises(ValidationError):
            self.store.import_pack(canonical_json(decoded))
        for path in ("/absolute", "../parent", "a/../../b", "nul\x00name"):
            with self.assertRaises(ValidationError):
                self.store.prepare_commit("p", {path: "x"})

    def test_queue_dedup_fencing_heartbeat_retry_cancel_and_deadletter(self) -> None:
        first = self.store.enqueue({"task": 1}, idempotency_key="same", available_at=0)
        self.assertEqual(self.store.enqueue({"task": 1}, idempotency_key="same").status, "deduplicated")
        self.assertEqual(self.store.enqueue({"task": 2}, idempotency_key="same").status, "conflict")
        lease = self.store.lease_next("worker", now=1, lease_seconds=5)
        self.assertIsNotNone(lease)
        self.assertEqual(self.store.heartbeat(first.job_id, lease.token, lease.generation + 1, now=2).status, "fenced")
        self.assertTrue(self.store.heartbeat(first.job_id, lease.token, lease.generation, now=2).ok)
        retry = self.store.fail(first.job_id, lease.token, lease.generation, "transient", backoff_base=0, now=3)
        self.assertEqual(retry.job.status, QueueStatus.RETRY_WAIT)
        again = self.store.lease_next("worker", now=3)
        self.assertGreater(again.generation, lease.generation)
        self.assertEqual(self.store.cancel(first.job_id, now=4).status, "cancel_requested")
        self.assertEqual(self.store.succeed(first.job_id, again.token, again.generation, "late", now=4).status, "cancelled")
        dead = self.store.enqueue("bad", idempotency_key="dead", available_at=0, max_attempts=2)
        l1 = self.store.lease_next("worker", now=10)
        self.assertEqual(l1.job.job_id, dead.job_id)
        self.store.fail(dead.job_id, l1.token, l1.generation, "retry", backoff_base=0, now=10)
        l2 = self.store.lease_next("worker", now=10)
        self.store.fail(dead.job_id, l2.token, l2.generation, "last", backoff_base=0, now=10)
        self.assertEqual(self.store.get_job(dead.job_id).status, QueueStatus.DEAD_LETTER)

    def test_queue_recovers_expired_leases_and_commits_one_result(self) -> None:
        queued = self.store.enqueue("payload", idempotency_key="recover", available_at=0)
        lease = self.store.lease_next("owner", now=10, lease_seconds=1)
        self.assertEqual(lease.job.job_id, queued.job_id)
        self.assertEqual(self.store.recover_expired_leases(now=12), 1)
        newer = self.store.lease_next("other", now=12)
        self.assertEqual(self.store.succeed(queued.job_id, lease.token, lease.generation, "old", now=12).status, "fenced")
        self.assertTrue(self.store.succeed(queued.job_id, newer.token, newer.generation, "new", now=12).ok)
        self.assertEqual(self.store.get_job(queued.job_id).result, b"new")
        self.assertEqual(self.store.succeed(queued.job_id, newer.token, newer.generation, "again", now=13).status, "fenced")

    def test_queue_projection_and_event_tampering_fail_before_dispatch(self) -> None:
        safe = self.store.enqueue({"action": "safe"}, idempotency_key="safe", available_at=0)
        evil = self.store.enqueue({"action": "evil"}, idempotency_key="evil", available_at=0)
        safe_hash = self.store._conn.execute(
            "SELECT payload_hash FROM jobs WHERE job_id=?", (safe.job_id,)
        ).fetchone()[0]
        evil_hash = self.store._conn.execute(
            "SELECT payload_hash FROM jobs WHERE job_id=?", (evil.job_id,)
        ).fetchone()[0]
        self.store._conn.execute(
            "UPDATE jobs SET payload_hash=? WHERE job_id=?", (evil_hash, safe.job_id)
        )
        self.assertFalse(self.store.verify().ok)
        with self.assertRaises(IntegrityError):
            self.store.lease_next("worker", now=1)

        self.store._conn.execute(
            "UPDATE jobs SET payload_hash=? WHERE job_id=?", (safe_hash, safe.job_id)
        )
        self.assertTrue(self.store.verify().ok)
        self.store._conn.execute(
            "UPDATE jobs SET status='succeeded',lease_token='forged',attempts=0 "
            "WHERE job_id=?", (safe.job_id,)
        )
        self.assertFalse(self.store.verify().ok)
        with self.assertRaises(IntegrityError):
            self.store.get_job(safe.job_id)

        self.store._conn.execute(
            "UPDATE job_events SET event_hash=? WHERE job_id=? AND event_id=("
            "SELECT MIN(event_id) FROM job_events WHERE job_id=?)",
            ("0" * 64, evil.job_id, evil.job_id),
        )
        self.assertFalse(self.store.verify().ok)

    def test_queue_integrity_migration_backfills_once_but_never_reblesses_deletion(self) -> None:
        legacy_path = Path(self.temp.name) / "legacy-v1.sqlite"
        with Store(legacy_path) as legacy:
            queued = legacy.enqueue({"action": "existing"}, idempotency_key="existing")
        raw = sqlite3.connect(legacy_path)
        try:
            raw.execute("DROP TABLE job_events")
            raw.execute("DELETE FROM schema_migrations WHERE version=2")
            raw.commit()
        finally:
            raw.close()

        with Store(legacy_path) as upgraded:
            self.assertTrue(upgraded.verify().ok)
            self.assertEqual(upgraded.get_job(queued.job_id).payload,
                             b'{"action":"existing"}')
            upgraded._conn.execute("DELETE FROM job_events WHERE job_id=?", (queued.job_id,))
        with Store(legacy_path) as reopened:
            self.assertFalse(reopened.verify().ok)
            with self.assertRaises(IntegrityError):
                reopened.get_job(queued.job_id)

    def test_task_memory_isolation_classes_promotion_rebuild_and_tamper(self) -> None:
        for memory_class in MemoryClass:
            self.store.append_memory("task", memory_class, memory_class.value, {"class": memory_class.value}, task_id="task-a")
        self.store.append_memory("task", MemoryClass.WORKING, "secret", "b", task_id="task-b")
        a = self.store.retrieve_task_memory("task-a")
        self.assertEqual({record.memory_class for record in a}, set(MemoryClass))
        self.assertNotIn("secret", {record.key for record in a})
        promoted = self.store.promote_to_os("task-a", MemoryClass.SEMANTIC, "semantic", reviewed_by="reviewer")
        self.assertTrue(promoted.reviewed)
        self.assertEqual(len(self.store.retrieve_memory(scope="os")), 1)
        self.store.tombstone_memory("task", MemoryClass.WORKING, "working", task_id="task-a")
        self.store._conn.execute("DELETE FROM memory_projection")
        self.store.rebuild_memory_projection()
        self.assertNotIn("working", {record.key for record in self.store.retrieve_task_memory("task-a")})
        self.assertTrue(self.store.verify().ok)
        self.store._conn.execute("UPDATE memory_events SET event_hash=? WHERE event_id=(SELECT MIN(event_id) FROM memory_events)",
                                 ("0" * 64,))
        self.assertFalse(self.store.verify().ok)

    def test_memory_projection_drift_fails_verification_and_rebuild_repairs(self) -> None:
        self.store.append_memory(
            "task", MemoryClass.EVIDENCE, "source", "verified",
            task_id="projection-task")
        self.store._conn.execute(
            "UPDATE memory_projection SET payload_hash=NULL "
            "WHERE task_key='projection-task'")
        report = self.store.verify()
        self.assertFalse(report.ok)
        self.assertTrue(any("projection" in error for error in report.errors))
        with self.assertRaises(IntegrityError):
            self.store.retrieve_task_memory("projection-task")
        self.store.rebuild_memory_projection()
        self.assertTrue(self.store.verify().ok)
        self.assertEqual(
            self.store.retrieve_task_memory("projection-task")[0].value,
            b"verified")
        payload_hash = self.store._conn.execute(
            "SELECT payload_hash FROM memory_projection WHERE task_key='projection-task'"
        ).fetchone()[0]
        self.store._conn.execute(
            "UPDATE blobs SET data=? WHERE hash=?", (b"altered", payload_hash)
        )
        with self.assertRaises(IntegrityError):
            self.store.retrieve_task_memory("projection-task")

    def test_backup_restore_and_verify(self) -> None:
        self.store.create_product("p")
        self.assertTrue(self.store.commit("p", {"doc": "durable"}).committed)
        self.store.append_memory("task", MemoryClass.EVIDENCE, "source", "citation", task_id="t")
        backup = self.store.backup(Path(self.temp.name) / "backup.sqlite")
        restored = Store.restore(backup, Path(self.temp.name) / "restored.sqlite")
        self.addCleanup(restored.close)
        self.assertEqual(restored.read_snapshot("p").files, {"doc": b"durable"})
        self.assertEqual(restored.retrieve_task_memory("t")[0].value, b"citation")
        self.assertTrue(restored.verify().ok)

    def test_expired_leases_cannot_heartbeat_or_finish_without_recovery_call(self) -> None:
        queued = self.store.enqueue({"job": "expiry"}, idempotency_key="expiry-direct", available_at=0)
        lease = self.store.lease_next("worker", lease_seconds=1, now=100)
        self.assertIsNotNone(lease)
        expired = self.store.succeed(queued.job_id, lease.token, lease.generation, "late", now=102)
        self.assertEqual(expired.status, "fenced")
        self.assertEqual(self.store.get_job(queued.job_id).status, QueueStatus.RETRY_WAIT)
        lease = self.store.lease_next("worker", lease_seconds=1, now=103)
        self.assertIsNotNone(lease)
        with self.assertRaises(ValidationError):
            self.store.heartbeat(queued.job_id, lease.token, lease.generation, lease_seconds=-1, now=103)
        with self.assertRaises(ValidationError):
            self.store.heartbeat(queued.job_id, lease.token, lease.generation, lease_seconds=float("nan"), now=103)
        self.assertTrue(self.store.verify().ok)

    def test_database_backup_and_restore_reject_symlink_or_special_targets(self) -> None:
        external = Path(self.temp.name) / "external.sqlite"
        with Store(external) as outside:
            outside.create_product("external")
        alias = Path(self.temp.name) / "alias.sqlite"
        alias.symlink_to(external)
        with self.assertRaisesRegex(ValidationError, "must not be a symlink"):
            Store(alias)
        with self.assertRaisesRegex(ValidationError, "must not be a symlink"):
            self.store.backup(alias)
        with self.assertRaisesRegex(ValidationError, "must not be a symlink"):
            Store.restore(alias, Path(self.temp.name) / "restored.sqlite")
        parent_alias = Path(self.temp.name) / "alias-directory"
        parent_alias.symlink_to(Path(self.temp.name), target_is_directory=True)
        with self.assertRaisesRegex(ValidationError, "parent must not be a symlink"):
            Store(parent_alias / "nested.sqlite")
        with self.assertRaisesRegex(ValidationError, "parent must not be a symlink"):
            self.store.backup(parent_alias / "backup.sqlite")
        directory = Path(self.temp.name) / "not-a-database"
        directory.mkdir()
        with self.assertRaisesRegex(ValidationError, "must be a regular file"):
            Store(directory)

    def test_backup_and_restore_connect_boundaries_reject_parent_swaps(self) -> None:
        import pmos.store as store_module

        self.store.create_product("authoritative")
        real_connect = store_module.sqlite3.connect

        backup_parent = Path(self.temp.name) / "backup-safe"
        backup_parent.mkdir()
        backup_target = backup_parent / "copy.sqlite"
        backup_staged = Path(self.temp.name) / "backup-staged"
        backup_outside = Path(self.temp.name) / "backup-outside"
        backup_outside.mkdir()
        external_backup = backup_outside / "copy.sqlite"
        with Store(external_backup) as external:
            external.create_product("external-backup")
        backup_swapped = False

        def swap_backup_parent(*args, **kwargs):
            nonlocal backup_swapped
            if not backup_swapped:
                backup_parent.rename(backup_staged)
                backup_parent.symlink_to(backup_outside, target_is_directory=True)
                backup_swapped = True
            return real_connect(*args, **kwargs)

        with patch.object(store_module.sqlite3, "connect", side_effect=swap_backup_parent):
            with self.assertRaises(IntegrityError):
                self.store.backup(backup_target)
        with Store(external_backup) as external:
            self.assertEqual(external.head("external-backup").product_id, "external-backup")
            with self.assertRaises(NotFoundError):
                external.head("authoritative")

        source_backup = self.store.backup(Path(self.temp.name) / "source-backup.sqlite")
        restore_parent = Path(self.temp.name) / "restore-safe"
        restore_parent.mkdir()
        restore_target = restore_parent / "restored.sqlite"
        restore_target_uri = restore_target.resolve().as_uri() + "?mode=rw"
        restore_staged = Path(self.temp.name) / "restore-staged"
        restore_outside = Path(self.temp.name) / "restore-outside"
        restore_outside.mkdir()
        external_restore = restore_outside / "restored.sqlite"
        with Store(external_restore) as external:
            external.create_product("external-restore")
        restore_swapped = False

        def swap_restore_parent(*args, **kwargs):
            nonlocal restore_swapped
            if args and args[0] == restore_target_uri and not restore_swapped:
                restore_parent.rename(restore_staged)
                restore_parent.symlink_to(restore_outside, target_is_directory=True)
                restore_swapped = True
            return real_connect(*args, **kwargs)

        with patch.object(store_module.sqlite3, "connect", side_effect=swap_restore_parent):
            with self.assertRaises(IntegrityError):
                Store.restore(source_backup, restore_target)
        with Store(external_restore) as external:
            self.assertEqual(external.head("external-restore").product_id, "external-restore")
            with self.assertRaises(NotFoundError):
                external.head("authoritative")

    def test_connect_boundary_parent_swap_never_creates_or_uses_external_database(self) -> None:
        parent = Path(self.temp.name) / "guarded"
        parent.mkdir()
        database = parent / "runtime.sqlite"
        outside = Path(self.temp.name) / "outside"
        staged = Path(self.temp.name) / "staged"
        import pmos.store as store_module
        real_connect = store_module.sqlite3.connect

        def swap_then_connect(*args, **kwargs):
            parent.rename(staged)
            outside.mkdir()
            parent.symlink_to(outside, target_is_directory=True)
            return real_connect(*args, **kwargs)

        with patch.object(store_module.sqlite3, "connect", side_effect=swap_then_connect):
            with self.assertRaises(Exception):
                Store(database)
        self.assertFalse((outside / "runtime.sqlite").exists())

        # If an attacker pre-populates the replacement path, post-connect
        # identity validation still fails before Store configuration or SQL.
        parent2 = Path(self.temp.name) / "guarded-existing"
        parent2.mkdir()
        database2 = parent2 / "runtime.sqlite"
        outside2 = Path(self.temp.name) / "outside-existing"
        outside2.mkdir()
        staged2 = Path(self.temp.name) / "staged-existing"
        external = outside2 / "runtime.sqlite"
        with Store(external) as seeded:
            seeded.create_product("external")
        def swap_existing_then_connect(*args, **kwargs):
            parent2.rename(staged2)
            parent2.symlink_to(outside2, target_is_directory=True)
            return real_connect(*args, **kwargs)
        with patch.object(store_module.sqlite3, "connect", side_effect=swap_existing_then_connect):
            with self.assertRaises(IntegrityError):
                Store(database2)
        with Store(external) as seeded:
            self.assertEqual(seeded.head("external").product_id, "external")

    def test_nonfinal_ancestor_swap_cannot_redirect_guard_open(self) -> None:
        safe = Path(self.temp.name) / "safe"
        nested = safe / "nested"
        nested.mkdir(parents=True)
        database = nested / "runtime.sqlite"
        outside = Path(self.temp.name) / "outside"
        (outside / "nested").mkdir(parents=True)
        staged = Path(self.temp.name) / "staged-safe"
        import pmos.store as store_module
        real_path = store_module._database_path
        real_open = store_module.os.open
        validated = False
        swapped = False

        def arm_after_validation(*args, **kwargs):
            nonlocal validated
            value = real_path(*args, **kwargs)
            validated = True
            return value

        def swap_ancestor(name, *args, **kwargs):
            nonlocal swapped
            if validated and name == "safe" and not swapped:
                safe.rename(staged)
                safe.symlink_to(outside, target_is_directory=True)
                swapped = True
            return real_open(name, *args, **kwargs)

        with patch.object(store_module, "_database_path", side_effect=arm_after_validation), \
                patch.object(store_module.os, "open", side_effect=swap_ancestor):
            with self.assertRaises(ValidationError):
                Store(database)
        self.assertTrue(swapped)
        self.assertFalse((outside / "nested" / "runtime.sqlite").exists())
        self.assertFalse((staged / "nested" / "runtime.sqlite").exists())

    def test_relative_and_uri_metacharacter_database_names_are_literal(self) -> None:
        original = Path.cwd()
        folder = Path(self.temp.name) / "relative-workdir"
        folder.mkdir()
        try:
            os.chdir(folder)
            with Store("runtime?#%.sqlite") as store:
                self.assertTrue(store.database.is_absolute())
                store.create_product("literal-name")
            self.assertTrue((folder / "runtime?#%.sqlite").is_file())
            self.assertFalse((folder / "runtime").exists())
        finally:
            os.chdir(original)

    def test_post_initialization_database_parent_swap_fails_before_operation(self) -> None:
        parent = Path(self.temp.name) / "live-guard"
        parent.mkdir()
        database = parent / "runtime.sqlite"
        guarded = Store(database)
        self.addCleanup(guarded.close)
        guarded.create_product("safe")
        staged = Path(self.temp.name) / "staged-live-guard"
        outside = Path(self.temp.name) / "outside-live-guard"
        parent.rename(staged)
        outside.mkdir()
        parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(IntegrityError):
            guarded.head("safe")

    def test_forged_missing_or_cross_product_head_fails_closed(self) -> None:
        self.store.create_product("p-one")
        one = self.store.commit("p-one", {"one": "1"})
        self.store.create_product("p-two")
        two = self.store.commit("p-two", {"two": "2"})
        self.assertTrue(one.committed and two.committed)
        self.store._conn.execute(
            "UPDATE product_heads SET commit_hash=? WHERE product_id='p-one'",
            ("0" * 64,))
        with self.assertRaises(IntegrityError):
            self.store.head("p-one")
        with self.assertRaises(IntegrityError):
            self.store.read_snapshot("p-one")
        self.assertFalse(self.store.verify().ok)
        self.store._conn.execute(
            "UPDATE product_heads SET commit_hash=? WHERE product_id='p-one'",
            (two.commit_hash,))
        with self.assertRaises(IntegrityError):
            self.store.head("p-one")
        self.assertFalse(self.store.verify().ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
