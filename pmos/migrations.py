"""Offline migration and recovery helpers for legacy PMOS workspaces.

Migration is a two-phase operation: build and verify a new SQLite snapshot in
an adjacent temporary file, then atomically activate it.  An existing runtime
is backed up first.  A deliberate fault injector is provided for tests and
operational drills; normal callers leave it unset.
"""

from __future__ import annotations

import json
import hashlib
import hmac
import os
import re
import secrets
import stat
import errno
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

from .release import _canonical
from .store import Store, ValidationError, sha256


RUNTIME_RELATIVE = Path(".pmos/runtime.sqlite")
MANIFEST_RELATIVE = Path(".pmos/migration.json")
JOURNAL_RELATIVE = Path(".pmos/migration-journal.json")
LOCK_RELATIVE = Path(".pmos/migration.lock")
_EXCLUDED_DIRS = {".git", ".pmos", "__pycache__", ".pytest_cache"}
_IDENTIFIER = re.compile(r"[^A-Za-z0-9_.:-]+")
MAX_MIGRATION_FILES = 4096
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_PATH_BYTES = 1024
MAX_CONTROL_BYTES = 1024 * 1024
MIGRATION_LOCK_TIMEOUT_SECONDS = 5.0
MIGRATION_LOCK_POLL_SECONDS = 0.05

try:
    import fcntl
except ImportError:  # pragma: no cover - PMOS supports macOS and Linux.
    fcntl = None


_THREAD_LOCKS_GUARD = threading.Lock()
_THREAD_LOCKS: dict[str, threading.Lock] = {}


class MigrationError(RuntimeError):
    """Migration could not be prepared or activated safely."""


class _DestinationLock:
    """Destination-scoped, thread- and process-safe advisory migration lock.

    The lock file is intentionally retained. ``flock`` releases its advisory
    lock on close or process death, while retaining the inode prevents a
    cleanup race where a second operation locks a replacement file.
    """

    def __init__(self, destination: Path) -> None:
        self.destination = destination
        self._thread_lock: Optional[threading.Lock] = None
        self._destination_fd: Optional[int] = None
        self._pmos_fd: Optional[int] = None
        self._lock_fd: Optional[int] = None

    def __enter__(self) -> "_DestinationLock":
        if fcntl is None:
            raise MigrationError("destination migration locking is unavailable on this platform")
        deadline = time.monotonic() + MIGRATION_LOCK_TIMEOUT_SECONDS
        key = str(self.destination)
        with _THREAD_LOCKS_GUARD:
            self._thread_lock = _THREAD_LOCKS.setdefault(key, threading.Lock())
        if not self._thread_lock.acquire(timeout=max(0.0, deadline - time.monotonic())):
            raise MigrationError(
                "destination is busy with another migration, recovery, or rollback; try again shortly"
            )
        try:
            self.destination.mkdir(parents=True, exist_ok=True)
            self._destination_fd = os.open(str(self.destination), _open_flags(True))
            try:
                os.mkdir(".pmos", 0o700, dir_fd=self._destination_fd)
            except FileExistsError:
                pass
            self._pmos_fd = os.open(".pmos", _open_flags(True), dir_fd=self._destination_fd)
            pmos_stat = os.fstat(self._pmos_fd)
            if not stat.S_ISDIR(pmos_stat.st_mode):
                raise MigrationError("migration lock directory is not a safe directory")
            self._lock_fd = os.open(
                LOCK_RELATIVE.name,
                os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=self._pmos_fd,
            )
            lock_stat = os.fstat(self._lock_fd)
            if not stat.S_ISREG(lock_stat.st_mode) or lock_stat.st_nlink != 1:
                raise MigrationError("migration lock is not a safe regular file")
            while True:
                try:
                    fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return self
                except OSError as exc:
                    if exc.errno not in (errno.EACCES, errno.EAGAIN):
                        raise MigrationError("cannot acquire destination migration lock: %s" % exc) from exc
                    if time.monotonic() >= deadline:
                        raise MigrationError(
                            "destination is busy with another migration, recovery, or rollback; try again shortly"
                        ) from exc
                    time.sleep(min(MIGRATION_LOCK_POLL_SECONDS, max(0.0, deadline - time.monotonic())))
        except MigrationError:
            self.__exit__(None, None, None)
            raise
        except OSError as exc:
            self.__exit__(None, None, None)
            raise MigrationError("cannot create or open a safe destination migration lock: %s" % exc) from exc
        except Exception:
            self.__exit__(None, None, None)
            raise

    def assert_runtime_directory(self) -> None:
        """Refuse lifecycle writes if the locked ``.pmos`` directory was swapped."""
        if self._destination_fd is None or self._pmos_fd is None:
            raise MigrationError("destination migration lock is not active")
        expected_destination = os.fstat(self._destination_fd)
        try:
            current_destination = os.stat(self.destination, follow_symlinks=False)
        except OSError as exc:
            raise MigrationError("migration destination changed while locked") from exc
        if (not stat.S_ISDIR(current_destination.st_mode) or
                current_destination.st_dev != expected_destination.st_dev or
                current_destination.st_ino != expected_destination.st_ino):
            raise MigrationError("migration destination changed while locked")
        expected = os.fstat(self._pmos_fd)
        try:
            current = os.stat(".pmos", dir_fd=self._destination_fd, follow_symlinks=False)
        except OSError as exc:
            raise MigrationError("migration runtime directory changed while locked") from exc
        if (not stat.S_ISDIR(current.st_mode) or current.st_dev != expected.st_dev or
                current.st_ino != expected.st_ino):
            raise MigrationError("migration runtime directory changed while locked")

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._lock_fd is not None:
            try:
                if fcntl is not None:
                    fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(self._lock_fd)
                self._lock_fd = None
        for attribute in ("_pmos_fd", "_destination_fd"):
            descriptor = getattr(self, attribute)
            if descriptor is not None:
                os.close(descriptor)
                setattr(self, attribute, None)
        if self._thread_lock is not None:
            self._thread_lock.release()
            self._thread_lock = None


@dataclass(frozen=True)
class FilePlan:
    """A planned regular file identity, used to close the plan/read TOCTOU."""

    path: str
    device: int
    inode: int
    size: int

    def as_dict(self) -> dict[str, Any]:
        return {"path": self.path, "device": self.device,
                "inode": self.inode, "size": self.size}


@dataclass(frozen=True)
class MigrationPlan:
    source: str
    destination: str
    product_id: str
    files: tuple[str, ...]
    file_count: int
    total_bytes: int
    file_specs: tuple[FilePlan, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {"source": self.source, "destination": self.destination,
                "product_id": self.product_id, "files": list(self.files),
                "file_count": self.file_count, "total_bytes": self.total_bytes,
                "file_specs": [item.as_dict() for item in self.file_specs]}


@dataclass(frozen=True)
class MigrationResult:
    status: str
    dry_run: bool
    plan: MigrationPlan
    runtime: str
    backup: Optional[str] = None
    manifest: Optional[str] = None
    message: str = ""

    @property
    def ok(self) -> bool:
        return self.status in {"planned", "migrated", "rolled_back", "recovered", "aborted"}

    def as_dict(self) -> dict[str, Any]:
        return {"status": self.status, "dry_run": self.dry_run,
                "plan": self.plan.as_dict(), "runtime": self.runtime,
                "backup": self.backup, "manifest": self.manifest, "message": self.message}


def _fault(injector: Any, point: str) -> None:
    if injector is not None:
        injector(point)


def _product_id(source: Path, requested: Optional[str]) -> str:
    value = requested or (source.name + "-product")
    value = _IDENTIFIER.sub("-", value).strip("-")[:200]
    if not value:
        raise ValidationError("product_id must contain at least one safe character")
    return value


def _workspace_files(source: Path) -> list[FilePlan]:
    """List regular files and freeze their identity before migration."""
    result: list[FilePlan] = []
    for current, dirs, names in os.walk(source, topdown=True, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in _EXCLUDED_DIRS and
                         not Path(current, name).is_symlink())
        for name in sorted(names):
            path = Path(current, name)
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            if not relative or "\x00" in relative or "\\" in relative or ".." in Path(relative).parts:
                raise MigrationError("unsafe source path: %s" % relative)
            if len(relative.encode("utf-8")) > MAX_PATH_BYTES:
                raise MigrationError("path exceeds migration limit: %s" % relative)
            metadata = path.stat()
            if not stat.S_ISREG(metadata.st_mode):
                continue
            if metadata.st_size > MAX_FILE_BYTES:
                raise MigrationError("file exceeds migration limit: %s" % relative)
            result.append(FilePlan(relative, int(metadata.st_dev), int(metadata.st_ino), int(metadata.st_size)))
    if len(result) > MAX_MIGRATION_FILES:
        raise MigrationError("workspace exceeds %d-file migration limit" % MAX_MIGRATION_FILES)
    total = sum(item.size for item in result)
    if total > MAX_TOTAL_BYTES:
        raise MigrationError("workspace exceeds %d-byte migration limit" % MAX_TOTAL_BYTES)
    return result


def _open_flags(directory: bool) -> int:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    if directory:
        flags |= getattr(os, "O_DIRECTORY", 0)
    return flags


def _read_planned_file(source: Path, item: FilePlan) -> bytes:
    """Read a planned file via descriptor-relative O_NOFOLLOW traversal."""
    components = Path(item.path).parts
    if not components or any(part in ("", ".", "..") for part in components):
        raise MigrationError("unsafe planned path: %s" % item.path)
    descriptors: list[int] = []
    try:
        current = os.open(str(source), _open_flags(True))
        descriptors.append(current)
        for component in components[:-1]:
            current = os.open(component, _open_flags(True), dir_fd=current)
            descriptors.append(current)
        file_fd = os.open(components[-1], _open_flags(False), dir_fd=current)
        descriptors.append(file_fd)
        before = os.fstat(file_fd)
        if (not stat.S_ISREG(before.st_mode) or int(before.st_dev) != item.device or
                int(before.st_ino) != item.inode or int(before.st_size) != item.size or
                before.st_size > MAX_FILE_BYTES):
            raise MigrationError("planned file changed identity or size: %s" % item.path)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_fd, min(1024 * 1024, MAX_FILE_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise MigrationError("file exceeds migration limit: %s" % item.path)
            chunks.append(chunk)
        after = os.fstat(file_fd)
        if (int(after.st_dev) != item.device or int(after.st_ino) != item.inode or
                int(after.st_size) != item.size or total != item.size):
            raise MigrationError("planned file changed while reading: %s" % item.path)
        return b"".join(chunks)
    except OSError as exc:
        raise MigrationError("cannot safely read planned file %s: %s" % (item.path, exc)) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def plan_workspace(source: str | os.PathLike[str], destination: str | os.PathLike[str] | None = None,
                   *, product_id: Optional[str] = None) -> MigrationPlan:
    source_path = Path(source).expanduser().resolve()
    if not source_path.is_dir():
        raise MigrationError("legacy workspace is not a directory: %s" % source_path)
    destination_path = Path(destination).expanduser().resolve() if destination else source_path
    files = _workspace_files(source_path)
    # A destination nested in the source can contain generated files; never
    # migrate the destination runtime or temporary migration files themselves.
    dest_prefix = None
    try:
        dest_prefix = destination_path.relative_to(source_path).as_posix().rstrip("/") + "/"
    except ValueError:
        pass
    selected = [item for item in files
                if item.path != RUNTIME_RELATIVE.as_posix() and
                item.path != MANIFEST_RELATIVE.as_posix() and
                item.path != JOURNAL_RELATIVE.as_posix() and
                not (dest_prefix and item.path.startswith(dest_prefix))]
    if len(selected) > MAX_MIGRATION_FILES:
        raise MigrationError("workspace exceeds %d-file migration limit" % MAX_MIGRATION_FILES)
    total = sum(item.size for item in selected)
    if total > MAX_TOTAL_BYTES:
        raise MigrationError("workspace exceeds %d-byte migration limit" % MAX_TOTAL_BYTES)
    return MigrationPlan(str(source_path), str(destination_path), _product_id(source_path, product_id),
                         tuple(item.path for item in selected), len(selected), total, tuple(selected))


def _assert_lifecycle_file(path: Path, label: str, *, lifecycle_lock: Optional[_DestinationLock] = None,
                           allow_missing: bool = False) -> None:
    """Bind lifecycle control files to the original locked runtime directory."""
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        if not allow_missing:
            raise MigrationError("%s is missing: %s" % (label, path))
    except OSError as exc:
        raise MigrationError("cannot inspect %s: %s" % (label, path)) from exc
    else:
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise MigrationError("%s is not a safe regular file: %s" % (label, path))
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()


def _atomic_json(path: Path, value: Mapping[str, Any], *,
                 lifecycle_lock: Optional[_DestinationLock] = None) -> None:
    _assert_lifecycle_file(path, "migration control file", lifecycle_lock=lifecycle_lock,
                           allow_missing=True)
    temporary = path.with_name(path.name + ".tmp-%s" % os.getpid())
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, "O_NOFOLLOW", 0), 0o600)
        os.write(descriptor, _canonical(value) + b"\n")
        os.fsync(descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    os.replace(temporary, path)
    try:
        directory_fd = os.open(str(path.parent), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        # The file itself is durable; some platforms do not permit directory
        # fsync. Do not turn a successful activation into a false failure.
        pass


def _file_digest(path: Path, *, lifecycle_lock: Optional[_DestinationLock] = None,
                 label: str = "runtime database") -> str:
    _assert_lifecycle_file(path, label, lifecycle_lock=lifecycle_lock)
    digest = hashlib.sha256()
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise MigrationError("%s is not a safe regular file: %s" % (label, path))
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size):
            raise MigrationError("%s changed while hashing: %s" % (label, path))
    except MigrationError:
        raise
    except OSError as exc:
        raise MigrationError("cannot read %s: %s" % (label, path)) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    return digest.hexdigest()


def _journal_plan(plan: MigrationPlan) -> dict[str, Any]:
    return {"source": plan.source, "destination": plan.destination,
            "product_id": plan.product_id,
            "files": [item.as_dict() for item in plan.file_specs],
            "file_count": plan.file_count, "total_bytes": plan.total_bytes}


def _plan_from_journal(journal: Mapping[str, Any]) -> MigrationPlan:
    raw_files = journal.get("files", [])
    if not isinstance(raw_files, list) or len(raw_files) > MAX_MIGRATION_FILES:
        raise MigrationError("migration journal has invalid file plan")
    specs: list[FilePlan] = []
    for raw in raw_files:
        if not isinstance(raw, Mapping):
            raise MigrationError("migration journal has malformed file identity")
        try:
            item = FilePlan(str(raw["path"]), int(raw["device"]), int(raw["inode"]), int(raw["size"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise MigrationError("migration journal has malformed file identity") from exc
        item_path = Path(item.path)
        if (not item.path or item_path.is_absolute() or ".." in item_path.parts or
                "\\" in item.path or "\x00" in item.path or
                len(item.path.encode("utf-8")) > MAX_PATH_BYTES or item.size < 0 or
                item.size > MAX_FILE_BYTES or item.device < 0 or item.inode < 0):
            raise MigrationError("migration journal exceeds file limits")
        specs.append(item)
    return MigrationPlan(str(journal.get("source", "")), str(journal.get("destination", "")),
                         _product_id(Path(str(journal.get("source", "workspace"))),
                                     str(journal.get("product_id", "migrated-product"))),
                         tuple(item.path for item in specs), len(specs), sum(item.size for item in specs),
                         tuple(specs))


def _read_control_json(path: Path, label: str, *,
                       lifecycle_lock: Optional[_DestinationLock] = None) -> dict[str, Any]:
    """Read one bounded control document through a stable no-follow descriptor."""
    _assert_lifecycle_file(path, label, lifecycle_lock=lifecycle_lock)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise MigrationError("safe migration control reads require no-follow support")
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
        before = os.fstat(descriptor)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                before.st_size > MAX_CONTROL_BYTES):
            raise MigrationError("%s is not a bounded private regular file" % label)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_CONTROL_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_CONTROL_BYTES:
                raise MigrationError("%s exceeds the control-file size limit" % label)
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size or total != before.st_size):
            raise MigrationError("%s changed while being read" % label)
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        pathname = os.stat(path, follow_symlinks=False)
        if (not stat.S_ISREG(pathname.st_mode) or pathname.st_dev != before.st_dev or
                pathname.st_ino != before.st_ino):
            raise MigrationError("%s path changed while being read" % label)
        value = json.loads(b"".join(chunks).decode("utf-8"))
    except MigrationError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MigrationError("%s is missing or invalid" % label) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if not isinstance(value, dict):
        raise MigrationError("%s must be an object" % label)
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    return value


def _read_json(path: Path, *, lifecycle_lock: Optional[_DestinationLock] = None) -> dict[str, Any]:
    return _read_control_json(path, "migration journal", lifecycle_lock=lifecycle_lock)


def _manifest_from_journal(journal: Mapping[str, Any], runtime: Path) -> dict[str, Any]:
    return {"format": "pmos.migration/v1", "source": journal["source"],
            "destination": journal["destination"], "product_id": journal["product_id"],
            "runtime": RUNTIME_RELATIVE.as_posix(), "backup": journal.get("backup"),
            "previous_runtime": bool(journal.get("previous_runtime")),
            "activated_sha256": journal.get("new_runtime_sha256"),
            "created_at": journal.get("created_at", time.time()),
            "recovered": bool(journal.get("recovered", False))}


def _valid_sha256(value: Any, label: str) -> str:
    if (not isinstance(value, str) or len(value) != 64 or
            any(character not in "0123456789abcdef" for character in value)):
        raise MigrationError("%s has no valid SHA-256 hash" % label)
    return value


def _read_manifest(path: Path, *, lifecycle_lock: Optional[_DestinationLock] = None) -> dict[str, Any]:
    manifest = _read_control_json(
        path, "migration manifest", lifecycle_lock=lifecycle_lock)
    if manifest.get("format") != "pmos.migration/v1":
        raise MigrationError("unsupported migration manifest")
    return manifest


def _assert_runtime_hash(runtime: Path, expected_hash: str, label: str, *,
                         lifecycle_lock: Optional[_DestinationLock] = None) -> None:
    """Check both byte identity and SQLite invariants before declaring a state durable."""
    expected = _valid_sha256(expected_hash, label)
    if not runtime.is_file() or runtime.is_symlink():
        raise MigrationError("%s is missing or is not a regular file" % label)
    if not hmac.compare_digest(_file_digest(runtime, lifecycle_lock=lifecycle_lock, label=label), expected):
        raise MigrationError("%s does not match its recorded hash" % label)
    try:
        with Store(runtime) as active:
            active.assert_verified()
    except Exception as exc:
        raise MigrationError("%s does not satisfy SQLite invariants" % label) from exc


def _rolled_back_manifest(manifest: Mapping[str, Any], *, previous_hash: str,
                          restored_hash: str, recovered: bool = False) -> dict[str, Any]:
    """Return a manifest whose active hash names the restored runtime.

    ``activated_sha256`` names the file that is currently active.  Retaining
    the migration hash separately lets recovery distinguish a completed
    rollback from an unrecorded replacement without weakening stale-state
    refusal.
    """
    updated = dict(manifest)
    updated["migrated_runtime_sha256"] = previous_hash
    updated["activated_sha256"] = restored_hash
    updated["rollback_from_sha256"] = previous_hash
    updated["rollback_runtime_sha256"] = restored_hash
    updated["rolled_back_at"] = time.time()
    updated["status"] = "rolled_back"
    if recovered:
        updated["rollback_recovered"] = True
    return updated


def _mark_journal(path: Path, journal: Mapping[str, Any], state: str, *,
                  lifecycle_lock: Optional[_DestinationLock] = None, **extra: Any) -> dict[str, Any]:
    updated = dict(journal)
    updated.update(extra)
    updated["state"] = state
    _atomic_json(path, updated, lifecycle_lock=lifecycle_lock)
    return updated


def _quarantine(path: Path, *, lifecycle_lock: Optional[_DestinationLock] = None,
                label: str = "runtime database") -> Optional[Path]:
    try:
        _assert_lifecycle_file(path, label, lifecycle_lock=lifecycle_lock)
    except MigrationError as exc:
        if "is missing:" in str(exc):
            return None
        raise
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    if not path.exists():
        return None
    target = path.with_name(path.name + ".quarantine-%s" % secrets.token_hex(6))
    os.replace(path, target)
    return target


def _discard_temporary(path: Path, *, lifecycle_lock: Optional[_DestinationLock] = None,
                       label: str = "migration temporary") -> None:
    """Remove only a still-bound regular temporary file after a failed transition."""
    try:
        _assert_lifecycle_file(path, label, lifecycle_lock=lifecycle_lock, allow_missing=True)
    except MigrationError:
        return
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def _restore_backup(runtime: Path, backup: Path, *,
                    lifecycle_lock: Optional[_DestinationLock] = None) -> None:
    _assert_lifecycle_file(backup, "migration backup", lifecycle_lock=lifecycle_lock)
    _assert_lifecycle_file(runtime, "runtime database", lifecycle_lock=lifecycle_lock,
                           allow_missing=True)
    recovery = runtime.with_name(runtime.name + ".recovery-%s" % secrets.token_hex(6))
    try:
        with Store.restore(backup, recovery) as restored:
            restored.assert_verified()
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        os.replace(recovery, runtime)
    finally:
        if recovery.exists():
            recovery.unlink()


def _migrate_workspace_locked(source: str | os.PathLike[str], destination: str | os.PathLike[str] | None = None,
                              *, product_id: Optional[str] = None, dry_run: bool = False,
                              fault_injector: Any = None, plan: Optional[MigrationPlan] = None,
                              lifecycle_lock: Optional[_DestinationLock] = None) -> MigrationResult:
    """Migrate a legacy file tree into a verified PMOS runtime database."""
    if plan is None:
        plan = plan_workspace(source, destination, product_id=product_id)
    else:
        source_check = str(Path(source).expanduser().resolve())
        destination_check = str(Path(destination).expanduser().resolve()) if destination else source_check
        if plan.source != source_check or plan.destination != destination_check:
            raise MigrationError("supplied migration plan does not match source or destination")
        if plan.file_count != len(plan.file_specs) or tuple(plan.files) != tuple(item.path for item in plan.file_specs):
            raise MigrationError("supplied migration plan has no complete file identities")
    runtime = Path(plan.destination) / RUNTIME_RELATIVE
    manifest_path = Path(plan.destination) / MANIFEST_RELATIVE
    if dry_run:
        return MigrationResult("planned", True, plan, str(runtime), message="dry-run: no files changed")
    Path(plan.destination).mkdir(parents=True, exist_ok=True)
    if lifecycle_lock is not None:
        lifecycle_lock.assert_runtime_directory()
    backup_path: Optional[Path] = None
    had_runtime = runtime.exists()
    if had_runtime:
        backup_path = runtime.parent / ("backup-%d.sqlite" % int(time.time() * 1000000))
    temporary = runtime.with_name(runtime.name + ".migration-%s" % secrets.token_hex(8))
    activated = False
    journal_path = Path(plan.destination) / JOURNAL_RELATIVE
    journal: Optional[dict[str, Any]] = None
    try:
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        with Store(temporary) as target:
            target.create_product(plan.product_id)
            _fault(fault_injector, "before_read")
            files: dict[str, bytes] = {}
            total_read = 0
            for item in plan.file_specs:
                content = _read_planned_file(Path(plan.source), item)
                total_read += len(content)
                if total_read > MAX_TOTAL_BYTES:
                    raise MigrationError("workspace exceeds %d-byte migration limit" % MAX_TOTAL_BYTES)
                files[item.path] = content
            target.commit(plan.product_id, files, expected_revision=0,
                          metadata={"migration": "legacy-workspace/v1", "source": plan.source,
                                    "file_count": plan.file_count})
            target.assert_verified()
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        new_runtime_sha256 = _file_digest(temporary, lifecycle_lock=lifecycle_lock,
                                          label="migration temporary")
        _fault(fault_injector, "before_backup")
        if backup_path is not None:
            if lifecycle_lock is not None:
                lifecycle_lock.assert_runtime_directory()
            with Store(runtime) as existing:
                existing.assert_verified()
                existing.backup(backup_path)
        _fault(fault_injector, "after_backup")
        journal = {"format": "pmos.migration-journal/v1", "state": "prepared",
                   "source": plan.source, "destination": plan.destination,
                   "product_id": plan.product_id, "runtime": RUNTIME_RELATIVE.as_posix(),
                   "temporary": temporary.name, "backup": backup_path.name if backup_path else None,
                   "previous_runtime": had_runtime,
                   "previous_runtime_sha256": _file_digest(
                       runtime, lifecycle_lock=lifecycle_lock) if had_runtime else None,
                   "new_runtime_sha256": new_runtime_sha256,
                   "plan": _journal_plan(plan), "created_at": time.time()}
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        _atomic_json(journal_path, journal, lifecycle_lock=lifecycle_lock)
        _fault(fault_injector, "before_activate")
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        os.replace(temporary, runtime)
        activated = True
        _fault(fault_injector, "after_replace")
        _fault(fault_injector, "after_activate")
        manifest = _manifest_from_journal(journal, runtime)
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        _atomic_json(manifest_path, manifest, lifecycle_lock=lifecycle_lock)
        if lifecycle_lock is not None:
            lifecycle_lock.assert_runtime_directory()
        _mark_journal(journal_path, journal, "finalized", lifecycle_lock=lifecycle_lock,
                      finalized_at=time.time())
        return MigrationResult("migrated", False, plan, str(runtime),
                               str(backup_path) if backup_path else None,
                               str(manifest_path), "migration activated and verified")
    except Exception as exc:
        _discard_temporary(temporary, lifecycle_lock=lifecycle_lock)
        # A fault after os.replace must not leave a new runtime claiming to
        # be active without its migration manifest. Restore the old backup
        # when one exists; otherwise quarantine the newly-created runtime.
        if activated and runtime.exists():
            try:
                if backup_path is not None and backup_path.exists():
                    _restore_backup(runtime, backup_path, lifecycle_lock=lifecycle_lock)
                    if journal is not None:
                        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                                      recovery_action="restored_backup",
                                      error=str(exc), aborted_at=time.time())
                else:
                    quarantined = _quarantine(runtime, lifecycle_lock=lifecycle_lock)
                    if journal is not None:
                        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                                      recovery_action="quarantined_runtime",
                                      quarantined=str(quarantined) if quarantined else None,
                                      error=str(exc), aborted_at=time.time())
            except Exception as recovery_exc:
                if journal is not None:
                    _mark_journal(journal_path, journal, "recovery_required", lifecycle_lock=lifecycle_lock,
                                  error=str(exc),
                                  recovery_error=str(recovery_exc), recovery_required_at=time.time())
                raise MigrationError("migration activation failed and requires recovery: %s" % recovery_exc) from exc
        raise MigrationError("migration was not activated: %s" % exc) from exc


def migrate_workspace(source: str | os.PathLike[str], destination: str | os.PathLike[str] | None = None,
                      *, product_id: Optional[str] = None, dry_run: bool = False,
                      fault_injector: Any = None, plan: Optional[MigrationPlan] = None) -> MigrationResult:
    """Migrate a legacy workspace while holding the destination lifecycle lock."""
    if plan is None:
        plan = plan_workspace(source, destination, product_id=product_id)
    else:
        source_check = str(Path(source).expanduser().resolve())
        destination_check = str(Path(destination).expanduser().resolve()) if destination else source_check
        if plan.source != source_check or plan.destination != destination_check:
            raise MigrationError("supplied migration plan does not match source or destination")
        if plan.file_count != len(plan.file_specs) or tuple(plan.files) != tuple(item.path for item in plan.file_specs):
            raise MigrationError("supplied migration plan has no complete file identities")
    if dry_run:
        runtime = Path(plan.destination) / RUNTIME_RELATIVE
        return MigrationResult("planned", True, plan, str(runtime), message="dry-run: no files changed")
    with _DestinationLock(Path(plan.destination)) as lifecycle_lock:
        return _migrate_workspace_locked(source, destination, product_id=product_id,
                                         dry_run=False, fault_injector=fault_injector, plan=plan,
                                         lifecycle_lock=lifecycle_lock)


def _recover_workspace_locked(destination: str | os.PathLike[str], *,
                              lifecycle_lock: Optional[_DestinationLock] = None) -> MigrationResult:
    """Finish or abort a migration interrupted after activation.

    Recovery is idempotent. A verified runtime matching the journal's new
    hash is finalized into the normal manifest; an old runtime matching the
    journal is safely aborted. Any other state is restored from a verified
    backup or quarantined, and the journal records the resulting action.
    """
    destination_path = Path(destination).expanduser().resolve()
    journal_path = destination_path / JOURNAL_RELATIVE
    journal = _read_json(journal_path, lifecycle_lock=lifecycle_lock)
    if journal.get("format") != "pmos.migration-journal/v1":
        raise MigrationError("unsupported migration journal")
    state = journal.get("state")
    plan_data = journal.get("plan")
    if isinstance(plan_data, Mapping):
        merged = dict(plan_data)
        merged.setdefault("source", journal.get("source", ""))
        merged.setdefault("destination", journal.get("destination", str(destination_path)))
        merged.setdefault("product_id", journal.get("product_id", "migrated-product"))
        plan = _plan_from_journal(merged)
    else:
        plan = _plan_from_journal(journal)
    runtime = destination_path / RUNTIME_RELATIVE
    manifest_path = destination_path / MANIFEST_RELATIVE
    backup_name = journal.get("backup")
    backup = runtime.parent / backup_name if isinstance(backup_name, str) and Path(backup_name).name == backup_name else None
    new_hash = _valid_sha256(journal.get("new_runtime_sha256"), "migration journal")
    if state == "finalized":
        # A finalized journal is not by itself proof that its runtime is still
        # active.  In particular, a rollback can replace the runtime between
        # journal finalization and its own manifest update.  Never report that
        # state as recovered unless both the current bytes and SQLite
        # invariants still match the finalized migration record.
        _assert_runtime_hash(runtime, new_hash, "finalized migration runtime",
                             lifecycle_lock=lifecycle_lock)
        manifest = _read_manifest(manifest_path, lifecycle_lock=lifecycle_lock)
        if manifest.get("status") == "rolled_back" or not hmac.compare_digest(
                _valid_sha256(manifest.get("activated_sha256"), "migration manifest"), new_hash):
            raise MigrationError("finalized migration manifest does not describe the active runtime")
        return MigrationResult("recovered", False, plan, str(runtime),
                               str(backup) if backup else None, str(manifest_path),
                               "migration was already finalized and verified")
    if state == "aborted":
        return MigrationResult("aborted", False, plan, str(runtime),
                               str(backup) if backup else None, str(manifest_path),
                               "migration was already aborted")
    if state == "rollback_finalized":
        restored_hash = _valid_sha256(journal.get("rollback_runtime_sha256"), "rollback journal")
        previous_hash = _valid_sha256(journal.get("rollback_from_sha256"), "rollback journal")
        if not hmac.compare_digest(previous_hash, new_hash):
            raise MigrationError("rollback journal does not bind to the finalized migration runtime")
        _assert_runtime_hash(runtime, restored_hash, "finalized rollback runtime",
                             lifecycle_lock=lifecycle_lock)
        manifest = _read_manifest(manifest_path, lifecycle_lock=lifecycle_lock)
        if (manifest.get("status") != "rolled_back" or
                not hmac.compare_digest(_valid_sha256(manifest.get("activated_sha256"), "migration manifest"), restored_hash) or
                not hmac.compare_digest(_valid_sha256(manifest.get("rollback_from_sha256"), "migration manifest"), previous_hash) or
                not hmac.compare_digest(_valid_sha256(manifest.get("rollback_runtime_sha256"), "migration manifest"), restored_hash)):
            raise MigrationError("finalized rollback manifest does not describe the active runtime")
        return MigrationResult("rolled_back", False, plan, str(runtime),
                               str(backup) if backup else None, str(manifest_path),
                               "rollback was already finalized and verified")
    if state in {"rollback_prepared", "rollback_recovery_required"}:
        previous_hash = _valid_sha256(journal.get("rollback_from_sha256"), "rollback journal")
        restored_hash = _valid_sha256(journal.get("rollback_runtime_sha256"), "rollback journal")
        if not hmac.compare_digest(previous_hash, new_hash):
            raise MigrationError("rollback journal does not bind to the finalized migration runtime")
        current_hash = (_file_digest(runtime, lifecycle_lock=lifecycle_lock)
                        if runtime.is_file() and not runtime.is_symlink() else None)
        if current_hash == restored_hash:
            # The replace happened, but the process died before either the
            # manifest or journal could close the transition.  Both are now
            # rebuilt from the pinned pair of hashes.
            _assert_runtime_hash(runtime, restored_hash, "prepared rollback runtime",
                                 lifecycle_lock=lifecycle_lock)
            manifest = _read_manifest(manifest_path, lifecycle_lock=lifecycle_lock)
            if (manifest.get("status") == "rolled_back" and
                    hmac.compare_digest(_valid_sha256(manifest.get("activated_sha256"), "migration manifest"), restored_hash)):
                updated_manifest = manifest
            else:
                if not hmac.compare_digest(_valid_sha256(manifest.get("activated_sha256"), "migration manifest"), previous_hash):
                    raise MigrationError("rollback manifest does not describe the migration being recovered")
                updated_manifest = _rolled_back_manifest(manifest, previous_hash=previous_hash,
                                                         restored_hash=restored_hash, recovered=True)
                _atomic_json(manifest_path, updated_manifest, lifecycle_lock=lifecycle_lock)
            _mark_journal(journal_path, journal, "rollback_finalized", lifecycle_lock=lifecycle_lock,
                          rollback_recovered=True,
                          rollback_finalized_at=time.time(), recovery_action="finalized_rollback")
            return MigrationResult("rolled_back", False, plan, str(runtime),
                                   str(backup) if backup else None, str(manifest_path),
                                   "verified restored runtime and finalized rollback")
        if current_hash == previous_hash:
            # The rollback journal was written but activation never occurred.
            # Preserve the original migration journal and make a later retry
            # possible; this is not permission to overwrite any other state.
            _assert_runtime_hash(runtime, previous_hash, "pre-rollback migration runtime",
                                 lifecycle_lock=lifecycle_lock)
            _mark_journal(journal_path, journal, "finalized", lifecycle_lock=lifecycle_lock,
                          rollback_aborted=True,
                          rollback_aborted_at=time.time(), recovery_action="rollback_not_activated")
            return MigrationResult("recovered", False, plan, str(runtime),
                                   str(backup) if backup else None, str(manifest_path),
                                   "rollback did not activate; migration remains active")
        _mark_journal(journal_path, journal, "rollback_recovery_required", lifecycle_lock=lifecycle_lock,
                      recovery_error="active runtime does not match the rollback's old or restored hash",
                      recovery_required_at=time.time())
        raise MigrationError(
            "active runtime changed during rollback; recovery refused to overwrite or quarantine it"
        )
    if state not in {"prepared", "recovery_required"}:
        raise MigrationError("migration journal has unknown state")
    temporary_name = journal.get("temporary")
    temporary = runtime.parent / temporary_name if isinstance(temporary_name, str) and Path(temporary_name).name == temporary_name else None
    old_hash = journal.get("previous_runtime_sha256")
    current_hash = (_file_digest(runtime, lifecycle_lock=lifecycle_lock)
                    if runtime.is_file() and not runtime.is_symlink() else None)
    expected_new_invalid = False
    if current_hash == new_hash and runtime.is_file():
        try:
            with Store(runtime) as active:
                active.assert_verified()
            manifest = _manifest_from_journal(journal, runtime)
            manifest["recovered"] = True
            _atomic_json(manifest_path, manifest, lifecycle_lock=lifecycle_lock)
            if temporary is not None and temporary.exists():
                _quarantine(temporary, lifecycle_lock=lifecycle_lock, label="migration temporary")
            updated = _mark_journal(journal_path, journal, "finalized", lifecycle_lock=lifecycle_lock,
                                     recovered=True,
                                     recovered_at=time.time(), recovery_action="finalized_new_runtime")
            return MigrationResult("recovered", False, plan, str(runtime),
                                   str(backup) if backup else None, str(manifest_path),
                                   "verified active runtime and finalized migration")
        except Exception as exc:
            # A runtime with the expected bytes but a broken SQLite invariant
            # must not be declared complete; fall through to backup restore.
            journal = _mark_journal(journal_path, journal, "recovery_required", lifecycle_lock=lifecycle_lock,
                                    recovery_error=str(exc), recovery_required_at=time.time())
            expected_new_invalid = True
    if current_hash == old_hash and runtime.is_file():
        if temporary is not None and temporary.exists():
            _quarantine(temporary, lifecycle_lock=lifecycle_lock, label="migration temporary")
        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                      recovery_action="old_runtime_still_active",
                      recovered_at=time.time())
        return MigrationResult("aborted", False, plan, str(runtime),
                               str(backup) if backup else None, str(manifest_path),
                               "old runtime remained active; migration aborted")
    if backup is not None and backup.is_file() and (current_hash is None or expected_new_invalid):
        _restore_backup(runtime, backup, lifecycle_lock=lifecycle_lock)
        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                      recovery_action="restored_backup",
                      recovered_at=time.time())
        if temporary is not None and temporary.exists():
            _quarantine(temporary, lifecycle_lock=lifecycle_lock, label="migration temporary")
        return MigrationResult("aborted", False, plan, str(runtime), str(backup),
                               str(manifest_path), "restored verified backup; migration aborted")
    if current_hash is not None and current_hash not in {new_hash, old_hash}:
        _mark_journal(
            journal_path, journal, "recovery_required", lifecycle_lock=lifecycle_lock,
            recovery_error="active runtime does not match the journal's old or new hash",
            recovery_required_at=time.time(),
        )
        raise MigrationError(
            "active runtime changed after the migration journal was written; "
            "recovery refused to overwrite or quarantine it"
        )
    if runtime.exists():
        quarantined = _quarantine(runtime, lifecycle_lock=lifecycle_lock)
        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                      recovery_action="quarantined_runtime",
                      quarantined=str(quarantined) if quarantined else None, recovered_at=time.time())
    elif temporary is not None and temporary.exists():
        _quarantine(temporary, lifecycle_lock=lifecycle_lock, label="migration temporary")
        _mark_journal(journal_path, journal, "aborted", lifecycle_lock=lifecycle_lock,
                      recovery_action="quarantined_unactivated_runtime",
                      recovered_at=time.time())
    else:
        _mark_journal(journal_path, journal, "recovery_required", lifecycle_lock=lifecycle_lock,
                      recovery_error="neither active runtime nor backup is available",
                      recovery_required_at=time.time())
        raise MigrationError("migration recovery has no verifiable runtime or backup")
    return MigrationResult("aborted", False, plan, str(runtime),
                           str(backup) if backup else None, str(manifest_path),
                           "quarantined unverified runtime; migration aborted")


def recover_workspace(destination: str | os.PathLike[str]) -> MigrationResult:
    """Recover a destination while holding the migration lifecycle lock."""
    destination_path = Path(destination).expanduser().resolve()
    with _DestinationLock(destination_path) as lifecycle_lock:
        return _recover_workspace_locked(destination_path, lifecycle_lock=lifecycle_lock)


def _rollback_workspace_locked(destination: str | os.PathLike[str], *, fault_injector: Any = None,
                               lifecycle_lock: Optional[_DestinationLock] = None) -> MigrationResult:
    """Restore the backup recorded by the most recent migration atomically."""
    destination_path = Path(destination).expanduser().resolve()
    manifest_path = destination_path / MANIFEST_RELATIVE
    journal_path = destination_path / JOURNAL_RELATIVE
    runtime = destination_path / RUNTIME_RELATIVE
    manifest = _read_manifest(manifest_path, lifecycle_lock=lifecycle_lock)
    activated_hash = _valid_sha256(manifest.get("activated_sha256"), "migration manifest")
    if manifest.get("status") == "rolled_back":
        # A completed rollback is idempotent only while the exact restored
        # runtime remains active.  A later operator write is never discarded.
        restored_hash = _valid_sha256(manifest.get("rollback_runtime_sha256"), "rollback manifest")
        _assert_runtime_hash(runtime, restored_hash, "rolled-back runtime",
                             lifecycle_lock=lifecycle_lock)
        plan = MigrationPlan(str(manifest.get("source", destination_path)), str(destination_path),
                             str(manifest.get("product_id", "migrated-product")), (), 0, 0)
        backup_name = manifest.get("backup")
        backup = runtime.parent / backup_name if isinstance(backup_name, str) and Path(backup_name).name == backup_name else None
        return MigrationResult("rolled_back", False, plan, str(runtime),
                               str(backup) if backup else None, str(manifest_path),
                               "rollback was already completed and verified")
    if not runtime.is_file() or runtime.is_symlink():
        raise MigrationError("active runtime is missing or is not a regular file")
    current_hash = _file_digest(runtime, lifecycle_lock=lifecycle_lock)
    if not hmac.compare_digest(current_hash, activated_hash):
        raise MigrationError(
            "active runtime changed since migration; rollback refused to discard newer state"
        )
    journal = _read_json(journal_path, lifecycle_lock=lifecycle_lock)
    if journal.get("format") != "pmos.migration-journal/v1":
        raise MigrationError("unsupported migration journal")
    if journal.get("state") != "finalized":
        raise MigrationError("migration lifecycle requires recovery before rollback")
    migration_hash = _valid_sha256(journal.get("new_runtime_sha256"), "migration journal")
    if not hmac.compare_digest(migration_hash, current_hash):
        raise MigrationError("migration journal does not bind to the active runtime")
    backup_name = manifest.get("backup")
    if not isinstance(backup_name, str) or Path(backup_name).name != backup_name:
        raise MigrationError("migration has no safe rollback backup")
    backup = runtime.parent / backup_name
    _assert_lifecycle_file(backup, "rollback backup", lifecycle_lock=lifecycle_lock)
    plan = MigrationPlan(str(manifest.get("source", destination_path)), str(destination_path),
                         str(manifest.get("product_id", "migrated-product")), (), 0, 0)
    temporary = runtime.with_name(runtime.name + ".rollback-%s" % os.getpid())
    try:
        _fault(fault_injector, "before_restore")
        with Store.restore(backup, temporary) as restored:
            restored.assert_verified()
        restored_hash = _file_digest(temporary, lifecycle_lock=lifecycle_lock,
                                     label="rollback temporary")
        journal = _mark_journal(
            journal_path, journal, "rollback_prepared", lifecycle_lock=lifecycle_lock,
            rollback_from_sha256=current_hash,
            rollback_runtime_sha256=restored_hash, rollback_prepared_at=time.time(),
        )
        _fault(fault_injector, "before_activate")
        if (not runtime.is_file() or runtime.is_symlink()
                or not hmac.compare_digest(_file_digest(runtime, lifecycle_lock=lifecycle_lock), current_hash)):
            raise MigrationError(
                "active runtime changed while rollback was being prepared; rollback refused"
            )
        os.replace(temporary, runtime)
        _fault(fault_injector, "after_activate")
        updated = _rolled_back_manifest(manifest, previous_hash=current_hash,
                                        restored_hash=restored_hash)
        _atomic_json(manifest_path, updated, lifecycle_lock=lifecycle_lock)
        _mark_journal(journal_path, journal, "rollback_finalized", lifecycle_lock=lifecycle_lock,
                      rollback_finalized_at=time.time())
        return MigrationResult("rolled_back", False, plan, str(runtime), str(backup),
                               str(manifest_path), "previous runtime restored and verified")
    except Exception as exc:
        _discard_temporary(temporary, lifecycle_lock=lifecycle_lock, label="rollback temporary")
        raise MigrationError("rollback was not activated: %s" % exc) from exc


def rollback_workspace(destination: str | os.PathLike[str], *, fault_injector: Any = None) -> MigrationResult:
    """Restore the recorded backup while holding the migration lifecycle lock."""
    destination_path = Path(destination).expanduser().resolve()
    with _DestinationLock(destination_path) as lifecycle_lock:
        return _rollback_workspace_locked(destination_path, fault_injector=fault_injector,
                                          lifecycle_lock=lifecycle_lock)


def create_legacy_fixture(root: str | os.PathLike[str], *, product_id: str = "legacy-product") -> Path:
    """Create a tiny deterministic legacy tree for tests and demonstrations."""
    path = Path(root).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    (path / "STATE.md").write_text("# Legacy state\n\nProduct: %s\n" % product_id, encoding="utf-8")
    (path / "README.md").write_text("# Legacy workspace\n\nMigrate this workspace with `pmos migrate`.\n",
                                    encoding="utf-8")
    return path


__all__ = ["JOURNAL_RELATIVE", "LOCK_RELATIVE", "MANIFEST_RELATIVE", "RUNTIME_RELATIVE",
           "MAX_CONTROL_BYTES", "MAX_FILE_BYTES", "MAX_MIGRATION_FILES", "MAX_PATH_BYTES", "MAX_TOTAL_BYTES",
           "FilePlan", "MigrationError", "MigrationPlan", "MigrationResult",
           "create_legacy_fixture", "migrate_workspace", "plan_workspace",
           "recover_workspace", "rollback_workspace"]
