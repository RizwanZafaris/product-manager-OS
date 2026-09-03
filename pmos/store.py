"""Local, durable transaction primitives for Product Manager OS.

``Store`` deliberately treats SQLite as an authoritative *local* transaction
domain.  WAL helps readers and writers on one filesystem; it is not a
distributed database and this module makes no shared-network SQLite claim.

The implementation has no dependencies outside the Python standard library.
It stores document snapshots, work proposals, a leased work queue, and scoped
memory streams.  Public mutators return small dataclasses so a caller has to
handle a stale compare-and-swap or a lease fence explicitly.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import re
import secrets
import sqlite3
import stat
import threading
import time
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Optional, Union


PACK_FORMAT = "pmos.commit-pack/v1"
MAX_PACK_BYTES = 16 * 1024 * 1024
MAX_PACK_FILES = 4096
MAX_PATH_BYTES = 1024


class StoreError(Exception):
    """Base class for safe, expected storage errors."""


class ValidationError(StoreError):
    """Input is malformed or exceeds a deliberate safety bound."""


class IntegrityError(StoreError):
    """Stored data failed a checksum, hash chain, or invariant."""


class NotFoundError(StoreError):
    """A requested product, commit, job, or memory record does not exist."""


def _database_path(database: Union[str, os.PathLike[str]], *, require_exists: bool = False) -> Path:
    """Return a local SQLite path without permitting unsafe final-node traversal.

    ``:memory:`` is SQLite's documented in-memory database spelling and has no
    filesystem target to validate. Every other Store database is a local
    regular file, whether it already exists or will be created by SQLite.
    """
    if os.fspath(database) == ":memory:":
        return Path(":memory:")
    path = Path(database)
    lexical = path if path.is_absolute() else Path.cwd() / path
    # macOS exposes normal temporary paths through /var and /tmp symlinks.
    # Inspect the caller's lexical components for user-controlled links, then
    # traverse one consistent physical path descriptor-by-descriptor.
    lexical_cursor = Path(lexical.anchor)
    for index, component in enumerate(lexical.parts[1:-1], start=1):
        lexical_cursor = lexical_cursor / component
        try:
            metadata = lexical_cursor.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            raise ValidationError("cannot inspect database parent: %s" % path.parent) from exc
        if stat.S_ISLNK(metadata.st_mode) and not (index == 1 and component in {"tmp", "var"}):
            raise ValidationError("database parent must not be a symlink: %s" % lexical_cursor)
    absolute = lexical.resolve()
    parts = absolute.parts
    anchor = Path(absolute.anchor)
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(str(anchor), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                             getattr(os, "O_NOFOLLOW", 0))
        for component in parts[1:-1]:
            try:
                next_descriptor = os.open(component, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                                          getattr(os, "O_NOFOLLOW", 0), dir_fd=descriptor)
            except FileNotFoundError:
                if require_exists:
                    raise ValidationError("database parent is missing: %s" % path.parent)
                os.mkdir(component, 0o700, dir_fd=descriptor)
                next_descriptor = os.open(component, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                                          getattr(os, "O_NOFOLLOW", 0), dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
    except ValidationError:
        raise
    except OSError as exc:
        raise ValidationError("database parent contains an unsafe component: %s" % path.parent) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        if require_exists:
            raise ValidationError("database source is missing: %s" % path)
    except OSError as exc:
        raise ValidationError("cannot inspect database path: %s" % path) from exc
    else:
        if stat.S_ISLNK(metadata.st_mode):
            raise ValidationError("database path must not be a symlink: %s" % path)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValidationError("database path must be a regular file: %s" % path)
    # Keep all later opens on this one physical spelling.  Returning the
    # lexical input here would make a second pathname traversal (and reopen a
    # mutable ancestor) after the descriptor validation above.
    return absolute


def _open_database_guards(path: Path) -> tuple[int, int]:
    """Pin the descriptor-walked parent and SQLite node without following links."""
    parent_fd: Optional[int] = None
    target_fd: Optional[int] = None
    success = False
    try:
        if not path.is_absolute():
            raise ValidationError("database path must be absolute after validation")
        parent_fd = os.open(path.anchor, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                            getattr(os, "O_NOFOLLOW", 0))
        for component in path.parts[1:-1]:
            next_parent = os.open(component, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                                  getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = next_parent
        flags = os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
        try:
            target_fd = os.open(path.name, flags, dir_fd=parent_fd)
        except FileNotFoundError:
            target_fd = os.open(path.name, flags | os.O_CREAT | os.O_EXCL, 0o600,
                                dir_fd=parent_fd)
        metadata = os.fstat(target_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValidationError("database path must be a regular file: %s" % path)
        success = True
        return parent_fd, target_fd
    except ValidationError:
        raise
    except OSError as exc:
        raise ValidationError("cannot safely open database path: %s" % path) from exc
    finally:
        if not success:
            if target_fd is not None:
                os.close(target_fd)
            if parent_fd is not None:
                os.close(parent_fd)


def _assert_guarded_database_path(path: Path, parent_fd: int, target_fd: int) -> None:
    """Require ``path`` to still name the directory and file held by the guards."""
    expected_parent = os.fstat(parent_fd)
    expected_file = os.fstat(target_fd)
    try:
        current_parent = os.stat(path.parent, follow_symlinks=False)
        current_file = os.stat(path, follow_symlinks=False)
    except OSError as exc:
        raise IntegrityError("database path changed while open") from exc
    if (not stat.S_ISDIR(current_parent.st_mode) or
            current_parent.st_dev != expected_parent.st_dev or
            current_parent.st_ino != expected_parent.st_ino or
            not stat.S_ISREG(current_file.st_mode) or
            current_file.st_dev != expected_file.st_dev or
            current_file.st_ino != expected_file.st_ino):
        raise IntegrityError("database path changed while open")


class QueueStatus(str, Enum):
    QUEUED = "queued"
    LEASED = "leased"
    RETRY_WAIT = "retry_wait"
    CANCEL_REQUESTED = "cancel_requested"
    CANCELLED = "cancelled"
    SUCCEEDED = "succeeded"
    CONFLICTED = "conflicted"
    DEAD_LETTER = "dead_letter"


class MemoryClass(str, Enum):
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    EVIDENCE = "evidence"


@dataclass(frozen=True)
class ProductHead:
    product_id: str
    revision: int
    commit_hash: Optional[str]

    @property
    def token(self) -> str:
        return "%d:%s" % (self.revision, self.commit_hash or "-")


@dataclass(frozen=True)
class PreparedCommit:
    product_id: str
    commit_hash: str
    expected_revision: str
    parent_hash: Optional[str]
    snapshot_hash: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class Conflict:
    code: str
    expected_revision: Optional[str]
    current: ProductHead
    message: str


@dataclass(frozen=True)
class PublishResult:
    status: str
    head: Optional[ProductHead] = None
    conflict: Optional[Conflict] = None
    commit_hash: Optional[str] = None

    @property
    def committed(self) -> bool:
        return self.status == "committed"


@dataclass(frozen=True)
class Snapshot:
    product_id: str
    head: ProductHead
    files: Mapping[str, bytes]


@dataclass(frozen=True)
class ImportResult:
    status: str
    prepared: Optional[PreparedCommit] = None
    publish: Optional[PublishResult] = None
    conflict: Optional[Conflict] = None


@dataclass(frozen=True)
class QueueResult:
    status: str
    job_id: str
    conflict: Optional[str] = None


@dataclass(frozen=True)
class Job:
    job_id: str
    idempotency_key: str
    payload_hash: str
    payload: bytes
    status: QueueStatus
    priority: int
    available_at: float
    due_at: Optional[float]
    deadline: Optional[float]
    attempts: int
    max_attempts: int
    lease_token: Optional[str]
    lease_generation: int
    lease_until: Optional[float]
    result: Optional[bytes]
    error: Optional[str]


@dataclass(frozen=True)
class Lease:
    job: Job
    owner: str
    token: str
    generation: int


@dataclass(frozen=True)
class LeaseResult:
    status: str
    job: Optional[Job] = None
    reason: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.status == "ok"


@dataclass(frozen=True)
class MemoryRecord:
    scope: str
    task_id: Optional[str]
    memory_class: MemoryClass
    key: str
    value: bytes
    event_hash: str
    reviewed: bool
    tombstoned: bool
    created_at: float


@dataclass(frozen=True)
class VerificationReport:
    ok: bool
    errors: tuple[str, ...]


def canonical_json(value: Any) -> bytes:
    """The one JSON encoding used for hashes, packs, and structured payloads."""
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValidationError("value is not canonical JSON") from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_relative_path(path: Union[str, os.PathLike[str]]) -> str:
    """Return a portable stored path; storage paths never denote filesystem links."""
    try:
        value = os.fspath(path)
    except TypeError as exc:
        raise ValidationError("path must be a non-empty NUL-free string") from exc
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValidationError("path must be a non-empty NUL-free string")
    if len(value.encode("utf-8")) > MAX_PATH_BYTES or "\\" in value:
        raise ValidationError("path is too long or not portable")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or value.startswith("/"):
        raise ValidationError("absolute paths are not allowed")
    parts = []
    for part in candidate.parts:
        if part in ("", "."):
            continue
        if part == "..":
            raise ValidationError("parent paths are not allowed")
        parts.append(part)
    if not parts:
        raise ValidationError("path must name a file")
    return "/".join(parts)


def _as_bytes(value: Union[bytes, bytearray, memoryview, str, Any]) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    return canonical_json(value)


def _now(now: Optional[float] = None) -> float:
    return time.time() if now is None else float(now)


def _event_hash(previous: Optional[str], body: Mapping[str, Any]) -> str:
    return sha256(canonical_json({"previous": previous or "", "body": body}))


def _serialized(method: Any) -> Any:
    """Serialize all use of one sqlite3 connection across caller threads."""
    @wraps(method)
    def guarded(self: "Store", *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            self._assert_database_guard()
            return method(self, *args, **kwargs)
    return guarded


_SCHEMA = """
CREATE TABLE IF NOT EXISTS blobs (
    hash TEXT PRIMARY KEY CHECK(length(hash)=64),
    size INTEGER NOT NULL CHECK(size >= 0),
    data BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS product_heads (
    product_id TEXT PRIMARY KEY REFERENCES products(product_id),
    revision INTEGER NOT NULL DEFAULT 0 CHECK(revision >= 0),
    commit_hash TEXT
);
CREATE TABLE IF NOT EXISTS commits (
    commit_hash TEXT PRIMARY KEY CHECK(length(commit_hash)=64),
    product_id TEXT NOT NULL REFERENCES products(product_id),
    parent_hash TEXT,
    snapshot_hash TEXT NOT NULL CHECK(length(snapshot_hash)=64),
    metadata_json BLOB NOT NULL,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS commit_entries (
    commit_hash TEXT NOT NULL REFERENCES commits(commit_hash),
    path TEXT NOT NULL,
    blob_hash TEXT NOT NULL REFERENCES blobs(hash),
    PRIMARY KEY(commit_hash, path)
);
CREATE TABLE IF NOT EXISTS prepared_commits (
    commit_hash TEXT PRIMARY KEY REFERENCES commits(commit_hash),
    expected_revision TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('prepared','published')),
    prepared_at REAL NOT NULL,
    published_at REAL
);
CREATE TABLE IF NOT EXISTS product_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL REFERENCES products(product_id),
    kind TEXT NOT NULL,
    payload_json BLOB NOT NULL,
    previous_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE CHECK(length(event_hash)=64),
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS product_events_stream ON product_events(product_id, event_id);

CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    payload_hash TEXT NOT NULL REFERENCES blobs(hash),
    payload_encoding TEXT NOT NULL,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 0,
    available_at REAL NOT NULL,
    due_at REAL,
    deadline REAL,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3 CHECK(max_attempts > 0),
    lease_token TEXT,
    lease_generation INTEGER NOT NULL DEFAULT 0,
    lease_owner TEXT,
    lease_until REAL,
    result_hash TEXT REFERENCES blobs(hash),
    error TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS jobs_ready ON jobs(status, available_at, priority DESC);

CREATE TABLE IF NOT EXISTS memory_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT NOT NULL CHECK(scope IN ('os','task')),
    task_key TEXT NOT NULL,
    memory_class TEXT NOT NULL,
    memory_key TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('put','tombstone','promote')),
    payload_hash TEXT REFERENCES blobs(hash),
    reviewed INTEGER NOT NULL DEFAULT 0 CHECK(reviewed IN (0,1)),
    metadata_json BLOB NOT NULL,
    previous_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE CHECK(length(event_hash)=64),
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS memory_events_stream
    ON memory_events(scope, task_key, event_id);
CREATE TABLE IF NOT EXISTS memory_projection (
    scope TEXT NOT NULL,
    task_key TEXT NOT NULL,
    memory_class TEXT NOT NULL,
    memory_key TEXT NOT NULL,
    payload_hash TEXT,
    event_hash TEXT NOT NULL,
    reviewed INTEGER NOT NULL,
    tombstoned INTEGER NOT NULL,
    created_at REAL NOT NULL,
    PRIMARY KEY(scope, task_key, memory_class, memory_key)
);
"""

_QUEUE_EVENT_SCHEMA = """
CREATE TABLE IF NOT EXISTS job_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL REFERENCES jobs(job_id),
    kind TEXT NOT NULL,
    state_json BLOB NOT NULL,
    previous_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE CHECK(length(event_hash)=64),
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS job_events_stream ON job_events(job_id, event_id);
"""

MIGRATIONS = ((1, _SCHEMA), (2, _QUEUE_EVENT_SCHEMA))

_JOB_EVENT_KINDS = frozenset({
    "migrated_snapshot", "enqueued", "lease_expired", "cancel_expired",
    "cancelled_before_lease", "deadline_elapsed", "leased", "heartbeat",
    "heartbeat_deadline_elapsed", "cancelled_on_success", "succeeded",
    "conflicted", "failed", "cancel_requested", "cancelled",
})
_ACTIVE_QUEUE_STATES = frozenset({
    QueueStatus.LEASED.value, QueueStatus.CANCEL_REQUESTED.value,
})
_TERMINAL_QUEUE_STATES = frozenset({
    QueueStatus.CANCELLED.value, QueueStatus.SUCCEEDED.value,
    QueueStatus.CONFLICTED.value, QueueStatus.DEAD_LETTER.value,
})
_JOB_STATE_KEYS = frozenset({
    "job_id", "idempotency_key", "payload_hash", "payload_encoding", "status",
    "priority", "available_at", "due_at", "deadline", "attempts", "max_attempts",
    "lease_token_hash", "lease_generation", "lease_owner", "lease_until",
    "result_hash", "error", "created_at", "updated_at",
})
_JOB_IMMUTABLE_KEYS = frozenset({
    "job_id", "idempotency_key", "payload_hash", "payload_encoding", "priority",
    "due_at", "deadline", "max_attempts", "created_at",
})
_QUEUE_TRANSITIONS = {
    QueueStatus.QUEUED.value: frozenset({
        QueueStatus.LEASED.value, QueueStatus.CANCELLED.value,
        QueueStatus.DEAD_LETTER.value,
    }),
    QueueStatus.RETRY_WAIT.value: frozenset({
        QueueStatus.LEASED.value, QueueStatus.CANCELLED.value,
        QueueStatus.DEAD_LETTER.value,
    }),
    QueueStatus.LEASED.value: frozenset({
        QueueStatus.LEASED.value, QueueStatus.CANCEL_REQUESTED.value,
        QueueStatus.RETRY_WAIT.value, QueueStatus.DEAD_LETTER.value,
        QueueStatus.SUCCEEDED.value, QueueStatus.CONFLICTED.value,
    }),
    QueueStatus.CANCEL_REQUESTED.value: frozenset({QueueStatus.CANCELLED.value}),
    QueueStatus.CANCELLED.value: frozenset(),
    QueueStatus.SUCCEEDED.value: frozenset(),
    QueueStatus.CONFLICTED.value: frozenset(),
    QueueStatus.DEAD_LETTER.value: frozenset(),
}


class Store:
    """A SQLite-backed local transaction domain.

    A Store is safe for concurrent local processes through ``BEGIN IMMEDIATE``
    and SQLite's locking.  It must not be placed on a shared/network database
    filesystem and used as though it were a multi-host consensus service.

    Queue delivery is *at least once*.  A successful ``succeed`` transition is
    exactly one committed local result, but a lease holder may have already
    made an external call before it crashes, so external effects are never
    claimed to be exactly once.
    """

    def __init__(self, database: Union[str, os.PathLike[str]],
                 fault_injector: Optional[Any] = None) -> None:
        self.database = _database_path(database)
        self._fault_injector = fault_injector
        self._lock = threading.RLock()
        self._database_parent_fd: Optional[int] = None
        self._database_fd: Optional[int] = None
        self._conn: Optional[sqlite3.Connection] = None
        try:
            if os.fspath(database) == ":memory:":
                self._conn = sqlite3.connect(str(self.database), timeout=5.0,
                                             isolation_level=None, check_same_thread=False)
            else:
                self._database_parent_fd, self._database_fd = _open_database_guards(self.database)
                self._conn = sqlite3.connect(self.database.as_uri() + "?mode=rw", uri=True, timeout=5.0,
                                             isolation_level=None, check_same_thread=False)
                self._assert_database_guard()
            self._conn.row_factory = sqlite3.Row
            self._configure()
            self._assert_database_guard()
            self._migrate()
            self._assert_database_guard()
        except BaseException:
            self.close()
            raise

    def _assert_database_guard(self) -> None:
        if self.database == Path(":memory:"):
            return
        if self._database_parent_fd is None or self._database_fd is None:
            raise IntegrityError("database guard is unavailable")
        _assert_guarded_database_path(
            self.database, self._database_parent_fd, self._database_fd,
        )

    def _configure(self) -> None:
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._conn.execute("PRAGMA trusted_schema=OFF")

    def close(self) -> None:
        with self._lock:
            if self._conn is not None:
                self._conn.close()
                self._conn = None  # type: ignore[assignment]
            for attribute in ("_database_fd", "_database_parent_fd"):
                descriptor = getattr(self, attribute, None)
                if descriptor is not None:
                    os.close(descriptor)
                    setattr(self, attribute, None)

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _migrate(self) -> None:
        conn = self._conn
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations "
                         "(version INTEGER PRIMARY KEY, checksum TEXT NOT NULL, applied_at REAL NOT NULL)")
            seen = {int(row["version"]): row["checksum"] for row in
                    conn.execute("SELECT version, checksum FROM schema_migrations")}
            for version, script in MIGRATIONS:
                checksum = sha256(script.encode("utf-8"))
                if version in seen:
                    if seen[version] != checksum:
                        raise IntegrityError("migration checksum mismatch for version %s" % version)
                    continue
                statements = [statement.strip() for statement in script.split(";") if statement.strip()]
                for statement in statements:
                    conn.execute(statement)
                if version == 2:
                    # Version 1 databases can already contain work. Bind each
                    # existing row once at the explicit upgrade boundary; a
                    # missing event after that point is corruption, not a cue
                    # to silently bless the row again on reopen.
                    self._backfill_job_events()
                conn.execute("INSERT INTO schema_migrations(version, checksum, applied_at) VALUES(?,?,?)",
                             (version, checksum, _now()))
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _begin(self) -> None:
        self._conn.execute("BEGIN IMMEDIATE")

    def _fault(self, point: str) -> None:
        """Invoke an explicit test/fault hook at a transaction boundary.

        Production callers leave this unset. Crash probes use it to kill a
        real child after SQLite has performed a precise subset of the work.
        """
        if self._fault_injector is not None:
            self._fault_injector(point)

    def _put_blob(self, data: bytes) -> str:
        digest = sha256(data)
        existing = self._conn.execute("SELECT size, data FROM blobs WHERE hash=?", (digest,)).fetchone()
        if existing is None:
            self._conn.execute("INSERT INTO blobs(hash,size,data) VALUES(?,?,?)", (digest, len(data), data))
        elif int(existing["size"]) != len(data) or bytes(existing["data"]) != data:
            raise IntegrityError("content-addressed blob collision")
        return digest

    def _blob(self, digest: str) -> bytes:
        row = self._conn.execute("SELECT data FROM blobs WHERE hash=?", (digest,)).fetchone()
        if row is None:
            raise IntegrityError("referenced blob is missing")
        value = bytes(row["data"])
        if sha256(value) != digest:
            raise IntegrityError("blob hash mismatch")
        return value

    @staticmethod
    def _valid_identifier(value: str, label: str) -> str:
        if not isinstance(value, str) or not value.strip() or "\x00" in value or len(value) > 512:
            raise ValidationError("%s must be a bounded non-empty string" % label)
        return value

    @_serialized
    def create_product(self, product_id: str) -> ProductHead:
        product_id = self._valid_identifier(product_id, "product_id")
        self._begin()
        try:
            row = self._conn.execute("SELECT product_id FROM products WHERE product_id=?", (product_id,)).fetchone()
            if row is None:
                now = _now()
                self._conn.execute("INSERT INTO products(product_id,created_at) VALUES(?,?)", (product_id, now))
                self._conn.execute("INSERT INTO product_heads(product_id,revision,commit_hash) VALUES(?,0,NULL)",
                                   (product_id,))
                self._append_product_event(product_id, "product_created", {"product_id": product_id}, now)
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        return self.head(product_id)

    @_serialized
    def head(self, product_id: str) -> ProductHead:
        row = self._conn.execute("SELECT product_id, revision, commit_hash FROM product_heads WHERE product_id=?",
                                 (product_id,)).fetchone()
        if row is None:
            raise NotFoundError("product not found: %s" % product_id)
        head = ProductHead(str(row["product_id"]), int(row["revision"]), row["commit_hash"])
        if head.revision == 0 and head.commit_hash is not None:
            raise IntegrityError("revision-zero product head must not reference a commit")
        if head.revision > 0 and head.commit_hash is None:
            raise IntegrityError("nonzero product head is missing its commit")
        if head.commit_hash is not None:
            commit = self._conn.execute(
                "SELECT c.product_id,p.state FROM commits c "
                "LEFT JOIN prepared_commits p ON p.commit_hash=c.commit_hash "
                "WHERE c.commit_hash=?", (head.commit_hash,)).fetchone()
            if (commit is None or commit["product_id"] != head.product_id or
                    commit["state"] != "published"):
                raise IntegrityError("product head does not reference its own published commit")
        return head

    get_head = head

    def _coerce_expected(self, expected: Optional[Union[str, int, ProductHead]]) -> Optional[str]:
        if expected is None:
            return None
        if isinstance(expected, ProductHead):
            return expected.token
        if isinstance(expected, int):
            return "%d:*" % expected
        if isinstance(expected, str) and ":" in expected:
            return expected
        raise ValidationError("expected revision must be a head token or ProductHead")

    @staticmethod
    def _matches_expected(expected: str, current: ProductHead) -> bool:
        if expected == current.token:
            return True
        # Integer callers get a revision-only token.  ProductHead.token is the
        # stronger form and is the one serialized into freshly prepared work.
        return expected == "%d:*" % current.revision

    def _assert_product(self, product_id: str) -> ProductHead:
        return self.head(product_id)

    @_serialized
    def prepare_commit(self, product_id: str, files: Mapping[Union[str, os.PathLike[str]], Any],
                       expected_revision: Optional[Union[str, int, ProductHead]] = None,
                       metadata: Optional[Mapping[str, Any]] = None) -> PreparedCommit:
        """Durably prepare a complete snapshot without changing a product head."""
        if not isinstance(files, Mapping):
            raise ValidationError("files must be a mapping of relative paths to content")
        normalized: dict[str, bytes] = {}
        for path, content in files.items():
            key = normalize_relative_path(path)
            if key in normalized:
                raise ValidationError("duplicate normalized path: %s" % key)
            normalized[key] = _as_bytes(content)
        meta = dict(metadata or {})
        meta_bytes = canonical_json(meta)
        expected = self._coerce_expected(expected_revision)
        self._begin()
        try:
            head = self._assert_product(product_id)
            if expected is None:
                expected = head.token
            entries = []
            for path in sorted(normalized):
                digest = self._put_blob(normalized[path])
                entries.append({"path": path, "blob_hash": digest, "size": len(normalized[path])})
            snapshot_hash = sha256(canonical_json(entries))
            body = {"product_id": product_id, "parent_hash": head.commit_hash,
                    "snapshot_hash": snapshot_hash, "metadata": meta,
                    "entries": entries}
            commit_hash = sha256(canonical_json(body))
            existing = self._conn.execute("SELECT product_id FROM commits WHERE commit_hash=?", (commit_hash,)).fetchone()
            if existing is None:
                now = _now()
                self._conn.execute("INSERT INTO commits(commit_hash,product_id,parent_hash,snapshot_hash,metadata_json,created_at) "
                                   "VALUES(?,?,?,?,?,?)",
                                   (commit_hash, product_id, head.commit_hash, snapshot_hash, meta_bytes, now))
                self._conn.executemany("INSERT INTO commit_entries(commit_hash,path,blob_hash) VALUES(?,?,?)",
                                       [(commit_hash, item["path"], item["blob_hash"]) for item in entries])
                self._conn.execute("INSERT INTO prepared_commits(commit_hash,expected_revision,state,prepared_at) VALUES(?,?, 'prepared', ?)",
                                   (commit_hash, expected, now))
                self._append_product_event(product_id, "commit_prepared",
                                           {"commit_hash": commit_hash, "expected_revision": expected}, now)
            self._fault("prepare.before_commit")
            self._conn.commit()
            self._fault("prepare.after_commit")
        except Exception:
            self._conn.rollback()
            raise
        return PreparedCommit(product_id, commit_hash, expected, head.commit_hash, snapshot_hash,
                              tuple(sorted(normalized)))

    prepare_snapshot = prepare_commit

    def _append_product_event(self, product_id: str, kind: str, payload: Mapping[str, Any], now: float) -> str:
        previous = self._conn.execute("SELECT event_hash FROM product_events WHERE product_id=? ORDER BY event_id DESC LIMIT 1",
                                      (product_id,)).fetchone()
        prior = previous["event_hash"] if previous else None
        body = {"product_id": product_id, "kind": kind, "payload": payload, "created_at": now}
        event_hash = _event_hash(prior, body)
        self._conn.execute("INSERT INTO product_events(product_id,kind,payload_json,previous_hash,event_hash,created_at) "
                           "VALUES(?,?,?,?,?,?)", (product_id, kind, canonical_json(payload), prior, event_hash, now))
        return event_hash

    @_serialized
    def publish(self, prepared: Union[PreparedCommit, str],
                expected_revision: Optional[Union[str, int, ProductHead]] = None) -> PublishResult:
        """Publish a prepared commit with a local ``BEGIN IMMEDIATE`` CAS."""
        commit_hash = prepared.commit_hash if isinstance(prepared, PreparedCommit) else str(prepared)
        requested = self._coerce_expected(expected_revision)
        self._begin()
        try:
            row = self._conn.execute("SELECT c.product_id,c.parent_hash,p.state,p.expected_revision "
                                     "FROM commits c JOIN prepared_commits p ON c.commit_hash=p.commit_hash "
                                     "WHERE c.commit_hash=?", (commit_hash,)).fetchone()
            if row is None:
                raise NotFoundError("prepared commit not found")
            product_id = str(row["product_id"])
            current = self.head(product_id)
            expected = requested or str(row["expected_revision"])
            if row["state"] == "published":
                if current.commit_hash == commit_hash:
                    self._conn.commit()
                    return PublishResult("committed", current, commit_hash=commit_hash)
                conflict = Conflict("already_published", expected, current, "prepared commit was published on another head")
                self._conn.commit()
                return PublishResult("conflict", conflict=conflict, commit_hash=commit_hash)
            if not self._matches_expected(expected, current):
                conflict = Conflict("stale_revision", expected, current, "expected head revision is stale")
                self._conn.commit()
                return PublishResult("conflict", conflict=conflict, commit_hash=commit_hash)
            if row["parent_hash"] != current.commit_hash:
                conflict = Conflict("lineage_conflict", expected, current, "proposal parent does not match current head")
                self._conn.commit()
                return PublishResult("conflict", conflict=conflict, commit_hash=commit_hash)
            now = _now()
            next_head = ProductHead(product_id, current.revision + 1, commit_hash)
            self._conn.execute("UPDATE product_heads SET revision=?,commit_hash=? WHERE product_id=?",
                               (next_head.revision, commit_hash, product_id))
            self._conn.execute("UPDATE prepared_commits SET state='published',published_at=? WHERE commit_hash=?",
                               (now, commit_hash))
            self._append_product_event(product_id, "head_published",
                                       {"commit_hash": commit_hash, "previous": current.token,
                                        "current": next_head.token}, now)
            self._fault("publish.before_commit")
            self._conn.commit()
            self._fault("publish.after_commit")
            return PublishResult("committed", next_head, commit_hash=commit_hash)
        except Exception:
            self._conn.rollback()
            raise

    publish_commit = publish

    @_serialized
    def commit(self, product_id: str, files: Mapping[Union[str, os.PathLike[str]], Any],
               expected_revision: Optional[Union[str, int, ProductHead]] = None,
               metadata: Optional[Mapping[str, Any]] = None) -> PublishResult:
        prepared = self.prepare_commit(product_id, files, expected_revision, metadata)
        return self.publish(prepared, expected_revision)

    commit_snapshot = commit

    @_serialized
    def read_snapshot(self, product_id: str, revision: Optional[Union[str, int, ProductHead]] = None) -> Snapshot:
        """Read head and all entries inside one reader snapshot transaction."""
        self._conn.execute("BEGIN")
        try:
            head = self.head(product_id)
            wanted = self._coerce_expected(revision)
            if wanted is not None and wanted != head.token:
                raise NotFoundError("requested revision is not the current head")
            files: dict[str, bytes] = {}
            if head.commit_hash:
                rows = self._conn.execute("SELECT path,blob_hash FROM commit_entries WHERE commit_hash=? ORDER BY path",
                                          (head.commit_hash,)).fetchall()
                for row in rows:
                    files[str(row["path"])] = self._blob(str(row["blob_hash"]))
            self._conn.commit()
            return Snapshot(product_id, head, files)
        except Exception:
            self._conn.rollback()
            raise

    snapshot = read_snapshot

    @_serialized
    def read_file(self, product_id: str, path: Union[str, os.PathLike[str]]) -> bytes:
        snap = self.read_snapshot(product_id)
        normalized = normalize_relative_path(path)
        try:
            return snap.files[normalized]
        except KeyError as exc:
            raise NotFoundError("file not found in product snapshot") from exc

    @_serialized
    def export_commit_pack(self, prepared: Union[PreparedCommit, str], *, max_bytes: int = MAX_PACK_BYTES,
                           max_files: int = MAX_PACK_FILES) -> bytes:
        """Export a canonical, self-validating full-snapshot proposal."""
        commit_hash = prepared.commit_hash if isinstance(prepared, PreparedCommit) else str(prepared)
        row = self._conn.execute("SELECT c.product_id,c.parent_hash,c.snapshot_hash,c.metadata_json,p.expected_revision "
                                 "FROM commits c JOIN prepared_commits p ON p.commit_hash=c.commit_hash "
                                 "WHERE c.commit_hash=?", (commit_hash,)).fetchone()
        if row is None:
            raise NotFoundError("prepared commit not found")
        entries = self._conn.execute("SELECT path,blob_hash FROM commit_entries WHERE commit_hash=? ORDER BY path",
                                     (commit_hash,)).fetchall()
        if len(entries) > max_files:
            raise ValidationError("commit exceeds pack file limit")
        files = []
        for entry in entries:
            data = self._blob(str(entry["blob_hash"]))
            files.append({"path": str(entry["path"]), "blob_hash": str(entry["blob_hash"]),
                          "size": len(data), "data_b64": base64.b64encode(data).decode("ascii")})
        core = {"format": PACK_FORMAT, "commit": {"hash": commit_hash,
                "product_id": str(row["product_id"]), "parent_hash": row["parent_hash"],
                "snapshot_hash": str(row["snapshot_hash"]),
                "metadata": json.loads(bytes(row["metadata_json"]).decode("utf-8"))},
                "expected_revision": str(row["expected_revision"]), "files": files}
        pack = dict(core)
        pack["pack_hash"] = sha256(canonical_json(core))
        encoded = canonical_json(pack)
        if len(encoded) > max_bytes:
            raise ValidationError("commit exceeds pack byte limit")
        return encoded

    export_pack = export_commit_pack

    def _decode_pack(self, pack: Union[bytes, bytearray, str], *, max_bytes: int, max_files: int) -> tuple[dict[str, Any], list[tuple[str, bytes, str]]]:
        raw = pack.encode("utf-8") if isinstance(pack, str) else bytes(pack)
        if not raw or len(raw) > max_bytes:
            raise ValidationError("pack is empty or exceeds byte limit")
        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("pack is not valid UTF-8 JSON") from exc
        if not isinstance(decoded, dict) or decoded.get("format") != PACK_FORMAT:
            raise ValidationError("unsupported commit pack")
        if set(decoded) != {"format", "commit", "expected_revision", "files", "pack_hash"}:
            raise ValidationError("pack contains unknown or missing fields")
        claimed = decoded.get("pack_hash")
        core = {key: decoded[key] for key in ("format", "commit", "expected_revision", "files") if key in decoded}
        if not isinstance(claimed, str) or sha256(canonical_json(core)) != claimed:
            raise IntegrityError("commit pack hash mismatch")
        commit = decoded.get("commit")
        files = decoded.get("files")
        if not isinstance(commit, dict) or not isinstance(files, list) or len(files) > max_files:
            raise ValidationError("pack has invalid commit or file set")
        product_id = self._valid_identifier(commit.get("product_id"), "product_id")
        if not isinstance(commit.get("hash"), str) or not isinstance(commit.get("snapshot_hash"), str):
            raise ValidationError("pack is missing commit hashes")
        if commit.get("parent_hash") is not None and not isinstance(commit["parent_hash"], str):
            raise ValidationError("pack has invalid parent hash")
        if not isinstance(commit.get("metadata"), dict):
            raise ValidationError("pack metadata must be an object")
        if not isinstance(decoded.get("expected_revision"), str):
            raise ValidationError("pack expected revision is invalid")
        parsed: list[tuple[str, bytes, str]] = []
        seen = set()
        entries = []
        for item in files:
            if not isinstance(item, dict):
                raise ValidationError("pack file record is invalid")
            path = normalize_relative_path(item.get("path"))
            if path in seen:
                raise ValidationError("pack contains duplicate normalized path")
            seen.add(path)
            digest = item.get("blob_hash")
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValidationError("pack blob hash is invalid")
            try:
                data = base64.b64decode(item.get("data_b64", ""), validate=True)
            except (ValueError, TypeError) as exc:
                raise ValidationError("pack blob is not base64") from exc
            if item.get("size") != len(data) or sha256(data) != digest:
                raise IntegrityError("pack blob size or hash mismatch")
            parsed.append((path, data, digest))
            entries.append({"path": path, "blob_hash": digest, "size": len(data)})
        if sha256(canonical_json(entries)) != commit["snapshot_hash"]:
            raise IntegrityError("pack snapshot hash mismatch")
        body = {"product_id": product_id, "parent_hash": commit.get("parent_hash"),
                "snapshot_hash": commit["snapshot_hash"], "metadata": commit["metadata"], "entries": entries}
        if sha256(canonical_json(body)) != commit["hash"]:
            raise IntegrityError("pack commit lineage hash mismatch")
        return decoded, parsed

    @_serialized
    def import_commit_pack(self, pack: Union[bytes, bytearray, str],
                           expected_revision: Optional[Union[str, int, ProductHead]] = None,
                           *, max_bytes: int = MAX_PACK_BYTES,
                           max_files: int = MAX_PACK_FILES) -> ImportResult:
        """Validate and store immutable proposal content, then attempt local CAS publish."""
        decoded, parsed = self._decode_pack(pack, max_bytes=max_bytes, max_files=max_files)
        commit = decoded["commit"]
        product_id = commit["product_id"]
        wanted = self._coerce_expected(expected_revision) or decoded["expected_revision"]
        self._begin()
        try:
            exists = self._conn.execute("SELECT product_id FROM products WHERE product_id=?", (product_id,)).fetchone()
            if exists is None:
                now = _now()
                self._conn.execute("INSERT INTO products(product_id,created_at) VALUES(?,?)", (product_id, now))
                self._conn.execute("INSERT INTO product_heads(product_id,revision,commit_hash) VALUES(?,0,NULL)", (product_id,))
                self._append_product_event(product_id, "product_created", {"product_id": product_id}, now)
            existing = self._conn.execute("SELECT product_id FROM commits WHERE commit_hash=?", (commit["hash"],)).fetchone()
            if existing is None:
                for _path, data, _digest in parsed:
                    self._put_blob(data)
                now = _now()
                self._conn.execute("INSERT INTO commits(commit_hash,product_id,parent_hash,snapshot_hash,metadata_json,created_at) VALUES(?,?,?,?,?,?)",
                                   (commit["hash"], product_id, commit.get("parent_hash"), commit["snapshot_hash"],
                                    canonical_json(commit["metadata"]), now))
                self._conn.executemany("INSERT INTO commit_entries(commit_hash,path,blob_hash) VALUES(?,?,?)",
                                       [(commit["hash"], path, digest) for path, _data, digest in parsed])
                self._conn.execute("INSERT INTO prepared_commits(commit_hash,expected_revision,state,prepared_at) VALUES(?,?, 'prepared', ?)",
                                   (commit["hash"], wanted, now))
                self._append_product_event(product_id, "commit_imported",
                                           {"commit_hash": commit["hash"], "expected_revision": wanted}, now)
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        prepared = PreparedCommit(product_id, commit["hash"], wanted, commit.get("parent_hash"),
                                  commit["snapshot_hash"], tuple(path for path, _data, _digest in parsed))
        published = self.publish(prepared, wanted)
        if published.committed:
            return ImportResult("committed", prepared, published)
        return ImportResult("conflict", prepared, published, published.conflict)

    import_pack = import_commit_pack

    # -------------------------- durable work queue --------------------------
    @staticmethod
    def _job_state(row: sqlite3.Row) -> Mapping[str, Any]:
        """Return the complete canonical queue projection for integrity events.

        Lease credentials are represented only by a one-way digest in the
        append-only history. The live token remains in ``jobs`` only while a
        lease is active, and verification compares its digest.
        """
        token = row["lease_token"]
        token_hash = sha256(str(token).encode("utf-8")) if token is not None else None
        return {
            "job_id": str(row["job_id"]),
            "idempotency_key": str(row["idempotency_key"]),
            "payload_hash": str(row["payload_hash"]),
            "payload_encoding": str(row["payload_encoding"]),
            "status": str(row["status"]),
            "priority": int(row["priority"]),
            "available_at": float(row["available_at"]),
            "due_at": None if row["due_at"] is None else float(row["due_at"]),
            "deadline": None if row["deadline"] is None else float(row["deadline"]),
            "attempts": int(row["attempts"]),
            "max_attempts": int(row["max_attempts"]),
            "lease_token_hash": token_hash,
            "lease_generation": int(row["lease_generation"]),
            "lease_owner": None if row["lease_owner"] is None else str(row["lease_owner"]),
            "lease_until": None if row["lease_until"] is None else float(row["lease_until"]),
            "result_hash": None if row["result_hash"] is None else str(row["result_hash"]),
            "error": None if row["error"] is None else str(row["error"]),
            "created_at": float(row["created_at"]),
            "updated_at": float(row["updated_at"]),
        }

    def _append_job_event(self, job_id: str, kind: str, created_at: float) -> str:
        if kind not in _JOB_EVENT_KINDS:
            raise IntegrityError("unknown queue event kind")
        row = self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        if row is None:
            raise IntegrityError("queue event references a missing job")
        previous_row = self._conn.execute(
            "SELECT event_hash FROM job_events WHERE job_id=? ORDER BY event_id DESC LIMIT 1",
            (job_id,),
        ).fetchone()
        previous = str(previous_row["event_hash"]) if previous_row is not None else None
        state = self._job_state(row)
        body = {"job_id": job_id, "kind": kind, "state": state,
                "created_at": float(created_at)}
        digest = _event_hash(previous, body)
        self._conn.execute(
            "INSERT INTO job_events(job_id,kind,state_json,previous_hash,event_hash,created_at) "
            "VALUES(?,?,?,?,?,?)",
            (job_id, kind, canonical_json(state), previous, digest, float(created_at)),
        )
        return digest

    def _backfill_job_events(self) -> None:
        rows = self._conn.execute(
            "SELECT j.* FROM jobs j LEFT JOIN job_events e ON e.job_id=j.job_id "
            "WHERE e.job_id IS NULL ORDER BY j.created_at,j.job_id"
        ).fetchall()
        for row in rows:
            self._append_job_event(
                str(row["job_id"]), "migrated_snapshot", float(row["updated_at"]))

    def _assert_queue_verified(self) -> None:
        blob_rows = {str(row["hash"]): row for row in self._conn.execute(
            "SELECT hash,size,data FROM blobs")}
        errors: list[str] = []
        self._verify_jobs(blob_rows, errors)
        if errors:
            raise IntegrityError("; ".join(errors))

    @_serialized
    def enqueue(self, payload: Any, *, idempotency_key: Optional[str] = None, priority: int = 0,
                available_at: Optional[float] = None, due_at: Optional[float] = None,
                deadline: Optional[float] = None, max_attempts: int = 3) -> QueueResult:
        data = _as_bytes(payload)
        payload_hash = sha256(data)
        key = idempotency_key or payload_hash
        self._valid_identifier(key, "idempotency_key")
        if max_attempts < 1:
            raise ValidationError("max_attempts must be positive")
        now = _now()
        if deadline is not None and float(deadline) < now:
            raise ValidationError("deadline is already elapsed")
        self._begin()
        try:
            self._assert_queue_verified()
            row = self._conn.execute("SELECT job_id,payload_hash FROM jobs WHERE idempotency_key=?", (key,)).fetchone()
            if row is not None:
                self._conn.commit()
                if row["payload_hash"] == payload_hash:
                    return QueueResult("deduplicated", str(row["job_id"]))
                return QueueResult("conflict", str(row["job_id"]), "idempotency key has a different full-SHA payload")
            digest = self._put_blob(data)
            job_id = secrets.token_hex(16)
            self._conn.execute("INSERT INTO jobs(job_id,idempotency_key,payload_hash,payload_encoding,status,priority,available_at,due_at,deadline,attempts,max_attempts,created_at,updated_at) "
                               "VALUES(?,?,?,?,?,?,?,?,?,0,?,?,?)",
                               (job_id, key, digest, "json" if not isinstance(payload, (bytes, bytearray, memoryview, str)) else "bytes",
                                QueueStatus.QUEUED.value, int(priority), now if available_at is None else float(available_at),
                                None if due_at is None else float(due_at), None if deadline is None else float(deadline),
                                int(max_attempts), now, now))
            self._append_job_event(job_id, "enqueued", now)
            self._fault("enqueue.before_commit")
            self._conn.commit()
            self._fault("enqueue.after_commit")
            return QueueResult("queued", job_id)
        except Exception:
            self._conn.rollback()
            raise

    enqueue_job = enqueue

    def _job_from_row(self, row: sqlite3.Row) -> Job:
        result = self._blob(str(row["result_hash"])) if row["result_hash"] else None
        return Job(str(row["job_id"]), str(row["idempotency_key"]), str(row["payload_hash"]),
                   self._blob(str(row["payload_hash"])), QueueStatus(str(row["status"])), int(row["priority"]),
                   float(row["available_at"]), row["due_at"], row["deadline"], int(row["attempts"]),
                   int(row["max_attempts"]), row["lease_token"], int(row["lease_generation"]),
                   row["lease_until"], result, row["error"])

    @_serialized
    def get_job(self, job_id: str) -> Job:
        self._assert_queue_verified()
        row = self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        if row is None:
            raise NotFoundError("job not found")
        return self._job_from_row(row)

    @_serialized
    def list_jobs(self, status: Optional[Union[QueueStatus, str]] = None) -> tuple[Job, ...]:
        self._assert_queue_verified()
        if status is None:
            rows = self._conn.execute("SELECT * FROM jobs ORDER BY created_at,job_id").fetchall()
        else:
            rows = self._conn.execute("SELECT * FROM jobs WHERE status=? ORDER BY created_at,job_id",
                                      (str(status.value if isinstance(status, QueueStatus) else status),)).fetchall()
        return tuple(self._job_from_row(row) for row in rows)

    def _recover_expired_locked(self, now: float) -> int:
        rows = self._conn.execute("SELECT job_id,attempts,max_attempts,status FROM jobs WHERE status IN ('leased','cancel_requested') "
                                 "AND lease_until IS NOT NULL AND lease_until <= ?", (now,)).fetchall()
        for row in rows:
            if row["status"] == QueueStatus.CANCEL_REQUESTED.value:
                status, error = QueueStatus.CANCELLED.value, "cancelled after lease expiration"
            elif int(row["attempts"]) >= int(row["max_attempts"]):
                status, error = QueueStatus.DEAD_LETTER.value, "lease expired after retry budget"
            else:
                status, error = QueueStatus.RETRY_WAIT.value, "lease expired"
            self._conn.execute("UPDATE jobs SET status=?,available_at=?,lease_token=NULL,lease_owner=NULL,lease_until=NULL,error=?,updated_at=? WHERE job_id=?",
                               (status, now, error, now, row["job_id"]))
            self._append_job_event(
                str(row["job_id"]),
                "cancel_expired" if status == QueueStatus.CANCELLED.value else "lease_expired",
                now,
            )
        return len(rows)

    @_serialized
    def recover_expired_leases(self, now: Optional[float] = None) -> int:
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            count = self._recover_expired_locked(stamp)
            self._conn.commit()
            return count
        except Exception:
            self._conn.rollback()
            raise

    recover_leases = recover_expired_leases

    @_serialized
    def lease_next(self, owner: str, *, lease_seconds: float = 30.0, now: Optional[float] = None) -> Optional[Lease]:
        self._valid_identifier(owner, "owner")
        if not math.isfinite(float(lease_seconds)) or lease_seconds <= 0:
            raise ValidationError("lease_seconds must be positive")
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            self._recover_expired_locked(stamp)
            cancelling = self._conn.execute(
                "SELECT job_id FROM jobs WHERE status='cancel_requested' ORDER BY job_id"
            ).fetchall()
            for cancelling_row in cancelling:
                cancelling_id = str(cancelling_row["job_id"])
                self._conn.execute(
                    "UPDATE jobs SET status='cancelled',lease_token=NULL,lease_owner=NULL,"
                    "lease_until=NULL,updated_at=?,error='cancelled before lease' WHERE job_id=?",
                    (stamp, cancelling_id),
                )
                self._append_job_event(cancelling_id, "cancelled_before_lease", stamp)
            elapsed = self._conn.execute(
                "SELECT job_id FROM jobs WHERE status IN ('queued','retry_wait') "
                "AND deadline IS NOT NULL AND deadline <= ? ORDER BY job_id", (stamp,)
            ).fetchall()
            for elapsed_row in elapsed:
                elapsed_id = str(elapsed_row["job_id"])
                self._conn.execute(
                    "UPDATE jobs SET status='dead_letter',updated_at=?,error='deadline elapsed' "
                    "WHERE job_id=?", (stamp, elapsed_id),
                )
                self._append_job_event(elapsed_id, "deadline_elapsed", stamp)
            row = self._conn.execute("SELECT * FROM jobs WHERE status IN ('queued','retry_wait') AND available_at <= ? "
                                     "AND (deadline IS NULL OR deadline > ?) ORDER BY priority DESC, "
                                     "CASE WHEN due_at IS NULL THEN 1 ELSE 0 END, due_at, available_at,created_at,job_id LIMIT 1",
                                     (stamp, stamp)).fetchone()
            if row is None:
                self._conn.commit()
                return None
            token = secrets.token_urlsafe(24)
            generation = int(row["lease_generation"]) + 1
            until = stamp + float(lease_seconds)
            self._conn.execute("UPDATE jobs SET status='leased',attempts=attempts+1,lease_token=?,lease_generation=?,lease_owner=?,lease_until=?,updated_at=?,error=NULL WHERE job_id=?",
                               (token, generation, owner, until, stamp, row["job_id"]))
            self._append_job_event(str(row["job_id"]), "leased", stamp)
            new_row = self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (row["job_id"],)).fetchone()
            self._conn.commit()
            return Lease(self._job_from_row(new_row), owner, token, generation)
        except Exception:
            self._conn.rollback()
            raise

    lease = lease_next

    def _fenced_job(self, job_id: str, token: str, generation: int, stamp: float) -> Optional[sqlite3.Row]:
        return self._conn.execute("SELECT * FROM jobs WHERE job_id=? AND lease_token=? AND lease_generation=? "
                                  "AND status IN ('leased','cancel_requested') AND lease_until > ? "
                                  "AND (deadline IS NULL OR deadline > ?)",
                                  (job_id, token, generation, stamp, stamp)).fetchone()

    @_serialized
    def heartbeat(self, job_id: str, token: str, generation: int, *, lease_seconds: float = 30.0,
                  now: Optional[float] = None) -> LeaseResult:
        if not math.isfinite(float(lease_seconds)) or lease_seconds <= 0:
            raise ValidationError("lease_seconds must be positive")
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            self._recover_expired_locked(stamp)
            row = self._fenced_job(job_id, token, generation, stamp)
            if row is None or row["status"] != QueueStatus.LEASED.value:
                self._conn.commit()
                return LeaseResult("fenced", reason="lease token or generation is stale")
            if row["deadline"] is not None and float(row["deadline"]) <= stamp:
                self._conn.execute("UPDATE jobs SET status='dead_letter',lease_token=NULL,lease_owner=NULL,lease_until=NULL,error='deadline elapsed',updated_at=? WHERE job_id=?",
                                   (stamp, job_id))
                self._append_job_event(job_id, "heartbeat_deadline_elapsed", stamp)
                self._conn.commit()
                return LeaseResult("deadline", reason="deadline elapsed")
            self._conn.execute("UPDATE jobs SET lease_until=?,updated_at=? WHERE job_id=?", (stamp + lease_seconds, stamp, job_id))
            self._append_job_event(job_id, "heartbeat", stamp)
            result = self._job_from_row(self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone())
            self._conn.commit()
            return LeaseResult("ok", result)
        except Exception:
            self._conn.rollback()
            raise

    @_serialized
    def succeed(self, job_id: str, token: str, generation: int, result: Any, *, now: Optional[float] = None) -> LeaseResult:
        data = _as_bytes(result)
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            self._recover_expired_locked(stamp)
            row = self._fenced_job(job_id, token, generation, stamp)
            if row is None:
                self._conn.commit()
                return LeaseResult("fenced", reason="lease token or generation is stale")
            if row["status"] == QueueStatus.CANCEL_REQUESTED.value:
                self._conn.execute("UPDATE jobs SET status='cancelled',lease_token=NULL,lease_owner=NULL,lease_until=NULL,error='cancelled while leased',updated_at=? WHERE job_id=?",
                                   (stamp, job_id))
                self._append_job_event(job_id, "cancelled_on_success", stamp)
                self._conn.commit()
                return LeaseResult("cancelled", reason="cancellation was requested")
            digest = self._put_blob(data)
            self._conn.execute("UPDATE jobs SET status='succeeded',result_hash=?,lease_token=NULL,lease_owner=NULL,lease_until=NULL,updated_at=?,error=NULL "
                               "WHERE job_id=?", (digest, stamp, job_id))
            self._append_job_event(job_id, "succeeded", stamp)
            result_job = self._job_from_row(self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone())
            self._conn.commit()
            return LeaseResult("ok", result_job)
        except Exception:
            self._conn.rollback()
            raise

    complete = succeed

    @_serialized
    def mark_conflicted(self, job_id: str, token: str, generation: int, reason: str,
                        *, now: Optional[float] = None) -> LeaseResult:
        """Finish a fenced lease as conflicted when its precondition changed."""
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            self._recover_expired_locked(stamp)
            row = self._fenced_job(job_id, token, generation, stamp)
            if row is None:
                self._conn.commit()
                return LeaseResult("fenced", reason="lease token or generation is stale")
            self._conn.execute("UPDATE jobs SET status='conflicted',lease_token=NULL,lease_owner=NULL,lease_until=NULL,error=?,updated_at=? WHERE job_id=?",
                               (str(reason)[:2048], stamp, job_id))
            self._append_job_event(job_id, "conflicted", stamp)
            result = self._job_from_row(self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone())
            self._conn.commit()
            return LeaseResult("ok", result)
        except Exception:
            self._conn.rollback()
            raise

    conflict = mark_conflicted

    @_serialized
    def fail(self, job_id: str, token: str, generation: int, error: str, *, retryable: bool = True,
             backoff_base: float = 1.0, now: Optional[float] = None) -> LeaseResult:
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            self._recover_expired_locked(stamp)
            row = self._fenced_job(job_id, token, generation, stamp)
            if row is None:
                self._conn.commit()
                return LeaseResult("fenced", reason="lease token or generation is stale")
            if row["status"] == QueueStatus.CANCEL_REQUESTED.value:
                target = QueueStatus.CANCELLED
            elif not retryable or int(row["attempts"]) >= int(row["max_attempts"]):
                target = QueueStatus.DEAD_LETTER
            else:
                target = QueueStatus.RETRY_WAIT
            available = stamp + max(0.0, float(backoff_base)) * (2 ** max(0, int(row["attempts"]) - 1))
            self._conn.execute("UPDATE jobs SET status=?,available_at=?,lease_token=NULL,lease_owner=NULL,lease_until=NULL,error=?,updated_at=? WHERE job_id=?",
                               (target.value, available if target is QueueStatus.RETRY_WAIT else stamp, str(error)[:2048], stamp, job_id))
            self._append_job_event(job_id, "failed", stamp)
            result = self._job_from_row(self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone())
            self._conn.commit()
            return LeaseResult("ok", result)
        except Exception:
            self._conn.rollback()
            raise

    retry = fail

    @_serialized
    def cancel(self, job_id: str, *, now: Optional[float] = None) -> LeaseResult:
        stamp = _now(now)
        self._begin()
        try:
            self._assert_queue_verified()
            row = self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            if row is None:
                raise NotFoundError("job not found")
            status = QueueStatus(str(row["status"]))
            if status in (QueueStatus.SUCCEEDED, QueueStatus.CANCELLED, QueueStatus.DEAD_LETTER, QueueStatus.CONFLICTED):
                self._conn.commit()
                return LeaseResult("terminal", self._job_from_row(row))
            if status is QueueStatus.LEASED:
                self._conn.execute("UPDATE jobs SET status='cancel_requested',updated_at=? WHERE job_id=?", (stamp, job_id))
                self._append_job_event(job_id, "cancel_requested", stamp)
                response = "cancel_requested"
            else:
                self._conn.execute(
                    "UPDATE jobs SET status='cancelled',lease_token=NULL,lease_owner=NULL,"
                    "lease_until=NULL,updated_at=?,error='cancelled before execution' WHERE job_id=?",
                    (stamp, job_id),
                )
                self._append_job_event(job_id, "cancelled", stamp)
                response = "cancelled"
            job = self._job_from_row(self._conn.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone())
            self._conn.commit()
            return LeaseResult(response, job)
        except Exception:
            self._conn.rollback()
            raise

    # ------------------------------ memory streams ------------------------------
    @staticmethod
    def _memory_scope(scope: str, task_id: Optional[str]) -> tuple[str, str, Optional[str]]:
        if scope not in ("os", "task"):
            raise ValidationError("memory scope must be 'os' or 'task'")
        if scope == "os":
            if task_id is not None:
                raise ValidationError("OS memory cannot be assigned to a task")
            return scope, "", None
        if task_id is None:
            raise ValidationError("task memory requires a task_id")
        if not isinstance(task_id, str) or not task_id or "\x00" in task_id or len(task_id) > 512:
            raise ValidationError("task_id is invalid")
        return scope, task_id, task_id

    def _append_memory(self, scope: str, task_key: str, memory_class: Union[MemoryClass, str], key: str,
                       action: str, value: Optional[bytes], reviewed: bool, metadata: Mapping[str, Any], now: float) -> MemoryRecord:
        klass = MemoryClass(memory_class)
        self._valid_identifier(key, "memory key")
        payload_hash = self._put_blob(value) if value is not None else None
        previous = self._conn.execute("SELECT event_hash FROM memory_events WHERE scope=? AND task_key=? ORDER BY event_id DESC LIMIT 1",
                                      (scope, task_key)).fetchone()
        prior = previous["event_hash"] if previous else None
        body = {"scope": scope, "task_key": task_key, "memory_class": klass.value, "memory_key": key,
                "action": action, "payload_hash": payload_hash, "reviewed": bool(reviewed),
                "metadata": metadata, "created_at": now}
        event_hash = _event_hash(prior, body)
        self._conn.execute("INSERT INTO memory_events(scope,task_key,memory_class,memory_key,action,payload_hash,reviewed,metadata_json,previous_hash,event_hash,created_at) "
                           "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                           (scope, task_key, klass.value, key, action, payload_hash, int(reviewed), canonical_json(dict(metadata)),
                            prior, event_hash, now))
        tombstoned = action == "tombstone"
        self._conn.execute("INSERT INTO memory_projection(scope,task_key,memory_class,memory_key,payload_hash,event_hash,reviewed,tombstoned,created_at) "
                           "VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(scope,task_key,memory_class,memory_key) DO UPDATE SET "
                           "payload_hash=excluded.payload_hash,event_hash=excluded.event_hash,reviewed=excluded.reviewed,tombstoned=excluded.tombstoned,created_at=excluded.created_at",
                           (scope, task_key, klass.value, key, payload_hash, event_hash, int(reviewed), int(tombstoned), now))
        return MemoryRecord(scope, task_key or None, klass, key, value or b"", event_hash, bool(reviewed), tombstoned, now)

    @_serialized
    def append_memory(self, scope: str, memory_class: Union[MemoryClass, str], key: str, value: Any, *,
                      task_id: Optional[str] = None, reviewed: bool = False,
                      metadata: Optional[Mapping[str, Any]] = None) -> MemoryRecord:
        scope, task_key, _ = self._memory_scope(scope, task_id)
        self._assert_memory_verified()
        self._begin()
        try:
            record = self._append_memory(scope, task_key, memory_class, key, "put", _as_bytes(value), reviewed,
                                         metadata or {}, _now())
            self._fault("memory.before_commit")
            self._conn.commit()
            self._fault("memory.after_commit")
            return record
        except Exception:
            self._conn.rollback()
            raise

    remember = append_memory

    @_serialized
    def retrieve_memory(self, *, scope: str = "task", task_id: Optional[str] = None,
                        memory_class: Optional[Union[MemoryClass, str]] = None,
                        include_tombstones: bool = False) -> tuple[MemoryRecord, ...]:
        scope, task_key, _ = self._memory_scope(scope, task_id)
        self._assert_memory_verified()
        conditions = ["p.scope=?", "p.task_key=?"]
        parameters: list[Any] = [scope, task_key]
        if memory_class is not None:
            conditions.append("p.memory_class=?")
            parameters.append(MemoryClass(memory_class).value)
        if not include_tombstones:
            conditions.append("p.tombstoned=0")
        rows = self._conn.execute("SELECT p.*,b.data FROM memory_projection p LEFT JOIN blobs b ON b.hash=p.payload_hash WHERE " +
                                 " AND ".join(conditions) + " ORDER BY p.created_at,p.memory_key", parameters).fetchall()
        return tuple(MemoryRecord(scope, task_key or None, MemoryClass(str(row["memory_class"])), str(row["memory_key"]),
                                  bytes(row["data"] or b""), str(row["event_hash"]), bool(row["reviewed"]),
                                  bool(row["tombstoned"]), float(row["created_at"])) for row in rows)

    @_serialized
    def retrieve_task_memory(self, task_id: str, *, include_os: bool = False,
                             memory_class: Optional[Union[MemoryClass, str]] = None) -> tuple[MemoryRecord, ...]:
        # The only cross-stream composition is explicit and never exposes another task.
        records = list(self.retrieve_memory(scope="task", task_id=task_id, memory_class=memory_class))
        if include_os:
            records.extend(self.retrieve_memory(scope="os", memory_class=memory_class))
        return tuple(records)

    @_serialized
    def promote_to_os(self, task_id: str, memory_class: Union[MemoryClass, str], key: str, *,
                      reviewed_by: str, expected_source_event_hash: Optional[str] = None) -> MemoryRecord:
        self._valid_identifier(reviewed_by, "reviewed_by")
        scope, task_key, _ = self._memory_scope("task", task_id)
        memory_value = MemoryClass(memory_class).value
        self._begin()
        try:
            self._assert_memory_verified()
            selected = self._conn.execute(
                "SELECT p.*,b.data FROM memory_projection p LEFT JOIN blobs b ON b.hash=p.payload_hash "
                "WHERE p.scope=? AND p.task_key=? AND p.memory_class=? AND p.memory_key=?",
                (scope, task_key, memory_value, key)).fetchone()
            if selected is None or bool(selected["tombstoned"]):
                raise NotFoundError("task memory record not found")
            source_hash = str(selected["event_hash"])
            if expected_source_event_hash is not None and expected_source_event_hash != source_hash:
                raise ValidationError("task memory source changed before promotion")
            record = self._append_memory("os", "", memory_class, key, "promote", bytes(selected["data"] or b""), True,
                                         {"source_task_id": task_id, "source_event_hash": source_hash,
                                          "reviewed_by": reviewed_by}, _now())
            self._conn.commit()
            return record
        except Exception:
            self._conn.rollback()
            raise

    promote_memory = promote_to_os

    @_serialized
    def tombstone_memory(self, scope: str, memory_class: Union[MemoryClass, str], key: str, *,
                         task_id: Optional[str] = None, reason: str = "retention") -> MemoryRecord:
        scope, task_key, _ = self._memory_scope(scope, task_id)
        self._assert_memory_verified()
        self._begin()
        try:
            record = self._append_memory(scope, task_key, memory_class, key, "tombstone", None, False,
                                         {"reason": str(reason)[:1024]}, _now())
            self._conn.commit()
            return record
        except Exception:
            self._conn.rollback()
            raise

    retain_tombstone = tombstone_memory

    @_serialized
    def rebuild_memory_projection(self) -> int:
        """Recreate materialized memory only from append-only event history."""
        self._assert_memory_verified(compare_projection=False)
        self._begin()
        try:
            self._conn.execute("DELETE FROM memory_projection")
            rows = self._conn.execute("SELECT * FROM memory_events ORDER BY event_id").fetchall()
            count = 0
            for row in rows:
                tombstoned = row["action"] == "tombstone"
                self._conn.execute("INSERT INTO memory_projection(scope,task_key,memory_class,memory_key,payload_hash,event_hash,reviewed,tombstoned,created_at) VALUES(?,?,?,?,?,?,?,?,?) "
                                   "ON CONFLICT(scope,task_key,memory_class,memory_key) DO UPDATE SET payload_hash=excluded.payload_hash,event_hash=excluded.event_hash,reviewed=excluded.reviewed,tombstoned=excluded.tombstoned,created_at=excluded.created_at",
                                   (row["scope"], row["task_key"], row["memory_class"], row["memory_key"], row["payload_hash"],
                                    row["event_hash"], row["reviewed"], int(tombstoned), row["created_at"]))
                count += 1
            self._conn.commit()
            return count
        except Exception:
            self._conn.rollback()
            raise

    rebuild_memory = rebuild_memory_projection

    # ------------------------------- verification -------------------------------
    def _verify_chain(self, table: str, keys: Iterable[tuple[Any, ...]], errors: list[str]) -> None:
        for key in keys:
            where = "product_id=?" if table == "product_events" else "scope=? AND task_key=?"
            rows = self._conn.execute("SELECT * FROM %s WHERE %s ORDER BY event_id" % (table, where), key).fetchall()
            previous = None
            for row in rows:
                try:
                    if table == "product_events":
                        payload = json.loads(bytes(row["payload_json"]).decode("utf-8"))
                        body = {"product_id": row["product_id"], "kind": row["kind"], "payload": payload,
                                "created_at": row["created_at"]}
                    else:
                        metadata = json.loads(bytes(row["metadata_json"]).decode("utf-8"))
                        body = {"scope": row["scope"], "task_key": row["task_key"], "memory_class": row["memory_class"],
                                "memory_key": row["memory_key"], "action": row["action"], "payload_hash": row["payload_hash"],
                                "reviewed": bool(row["reviewed"]), "metadata": metadata, "created_at": row["created_at"]}
                    if row["previous_hash"] != previous or row["event_hash"] != _event_hash(previous, body):
                        errors.append("%s hash chain mismatch" % table)
                        break
                    previous = row["event_hash"]
                except Exception:
                    errors.append("%s invalid event payload" % table)
                    break

    def _verify_memory(
        self,
        blob_rows: Mapping[str, sqlite3.Row],
        errors: list[str],
        *,
        compare_projection: bool = True,
    ) -> None:
        self._verify_chain(
            "memory_events",
            [(row["scope"], row["task_key"]) for row in self._conn.execute(
                "SELECT DISTINCT scope,task_key FROM memory_events")],
            errors,
        )
        expected_projection: dict[tuple[str, str, str, str], tuple[Any, ...]] = {}
        referenced_hashes: set[str] = set()
        for event in self._conn.execute("SELECT * FROM memory_events ORDER BY event_id"):
            key = (str(event["scope"]), str(event["task_key"]),
                   str(event["memory_class"]), str(event["memory_key"]))
            action = str(event["action"])
            payload_hash = event["payload_hash"]
            if key[0] == "os" and key[1] != "":
                errors.append("OS memory event has a task key")
            if key[0] == "task" and not key[1]:
                errors.append("task memory event lacks a task key")
            try:
                MemoryClass(key[2])
            except ValueError:
                errors.append("memory event class is invalid")
            if action == "tombstone":
                if payload_hash is not None:
                    errors.append("memory tombstone retains a payload")
            elif payload_hash is None or str(payload_hash) not in blob_rows:
                errors.append("memory event payload is missing")
            else:
                referenced_hashes.add(str(payload_hash))
            expected_projection[key] = (
                payload_hash, event["event_hash"], int(event["reviewed"]),
                int(action == "tombstone"), event["created_at"])
        for digest in referenced_hashes:
            row = blob_rows[digest]
            data = bytes(row["data"])
            if int(row["size"]) != len(data) or sha256(data) != digest:
                errors.append("memory payload blob integrity mismatch: %s" % digest)
        if not compare_projection:
            return
        actual_projection = {
            (str(row["scope"]), str(row["task_key"]), str(row["memory_class"]),
             str(row["memory_key"])):
            (row["payload_hash"], row["event_hash"], int(row["reviewed"]),
             int(row["tombstoned"]), row["created_at"])
            for row in self._conn.execute("SELECT * FROM memory_projection")
        }
        if actual_projection != expected_projection:
            errors.append("memory projection does not match replayed event history")

    def _assert_memory_verified(self, *, compare_projection: bool = True) -> None:
        blob_rows = {str(row["hash"]): row for row in self._conn.execute(
            "SELECT hash,size,data FROM blobs")}
        errors: list[str] = []
        self._verify_memory(
            blob_rows, errors, compare_projection=compare_projection)
        if errors:
            raise IntegrityError("; ".join(errors))

    @staticmethod
    def _queue_state_errors(state: Any, blob_hashes: set[str]) -> tuple[str, ...]:
        found: list[str] = []
        if not isinstance(state, dict) or set(state) != _JOB_STATE_KEYS:
            return ("queue state has unknown or missing fields",)
        status = state.get("status")
        if status not in _QUEUE_TRANSITIONS:
            found.append("queue status is invalid")
        for key in ("job_id", "idempotency_key"):
            value = state.get(key)
            if (not isinstance(value, str) or not value or "\x00" in value
                    or len(value) > 512):
                found.append("queue %s is invalid" % key)
        for key in ("payload_hash", "result_hash", "lease_token_hash"):
            value = state.get(key)
            if value is not None and (not isinstance(value, str)
                                      or re.fullmatch(r"[0-9a-f]{64}", value) is None):
                found.append("queue %s is invalid" % key)
        if state.get("payload_hash") not in blob_hashes:
            found.append("queue payload blob is missing")
        result_hash = state.get("result_hash")
        if result_hash is not None and result_hash not in blob_hashes:
            found.append("queue result blob is missing")
        if state.get("payload_encoding") not in {"json", "bytes"}:
            found.append("queue payload encoding is invalid")
        for key in ("priority", "attempts", "max_attempts", "lease_generation"):
            if not isinstance(state.get(key), int) or isinstance(state.get(key), bool):
                found.append("queue %s is not an integer" % key)
        attempts = state.get("attempts")
        maximum = state.get("max_attempts")
        generation = state.get("lease_generation")
        if (isinstance(attempts, int) and isinstance(maximum, int)
                and (attempts < 0 or maximum < 1 or attempts > maximum)):
            found.append("queue attempt count is invalid")
        if (isinstance(attempts, int) and isinstance(generation, int)
                and (generation < 0 or generation != attempts)):
            found.append("queue lease generation does not match attempts")
        for key in ("available_at", "created_at", "updated_at"):
            value = state.get(key)
            if (not isinstance(value, (int, float)) or isinstance(value, bool)
                    or not math.isfinite(float(value))):
                found.append("queue %s is not finite" % key)
        for key in ("due_at", "deadline", "lease_until"):
            value = state.get(key)
            if value is not None and (not isinstance(value, (int, float))
                                      or isinstance(value, bool)
                                      or not math.isfinite(float(value))):
                found.append("queue %s is not finite" % key)
        active = status in _ACTIVE_QUEUE_STATES
        lease_values = (state.get("lease_token_hash"), state.get("lease_owner"),
                        state.get("lease_until"))
        if active:
            owner = state.get("lease_owner")
            if (any(value is None for value in lease_values)
                    or not isinstance(owner, str) or not owner or len(owner) > 512
                    or not isinstance(attempts, int) or attempts < 1):
                found.append("active queue lease is incomplete")
        elif any(value is not None for value in lease_values):
            found.append("inactive queue state retains lease material")
        if status == QueueStatus.QUEUED.value and attempts != 0:
            found.append("queued job has already been attempted")
        if status == QueueStatus.SUCCEEDED.value:
            if result_hash is None:
                found.append("succeeded job has no result")
        elif result_hash is not None:
            found.append("non-succeeded job retains a result")
        error = state.get("error")
        if error is not None and (not isinstance(error, str) or len(error) > 2048):
            found.append("queue error is invalid")
        return tuple(found)

    def _verify_jobs(self, blob_rows: Mapping[str, sqlite3.Row], errors: list[str]) -> None:
        jobs = {str(row["job_id"]): row for row in self._conn.execute(
            "SELECT * FROM jobs ORDER BY created_at,job_id")}
        event_jobs = {str(row["job_id"]) for row in self._conn.execute(
            "SELECT DISTINCT job_id FROM job_events")}
        for missing in sorted(event_jobs - set(jobs)):
            errors.append("queue event references missing job: %s" % missing)
        for job_id, row in jobs.items():
            try:
                actual = self._job_state(row)
            except Exception:
                errors.append("queue row is malformed: %s" % job_id)
                continue
            for problem in self._queue_state_errors(actual, set(blob_rows)):
                errors.append("%s: %s" % (problem, job_id))
            events = self._conn.execute(
                "SELECT * FROM job_events WHERE job_id=? ORDER BY event_id", (job_id,)
            ).fetchall()
            if not events:
                errors.append("queue job has no integrity event: %s" % job_id)
                continue
            previous_hash: Optional[str] = None
            previous_state: Optional[Mapping[str, Any]] = None
            latest: Optional[Mapping[str, Any]] = None
            for index, event in enumerate(events):
                try:
                    raw_state = bytes(event["state_json"])
                    state = json.loads(raw_state.decode("utf-8"))
                    if canonical_json(state) != raw_state:
                        raise ValueError("queue state is not canonical JSON")
                    if event["kind"] not in _JOB_EVENT_KINDS:
                        raise ValueError("unknown queue event kind")
                    if not isinstance(event["created_at"], (int, float)) or not math.isfinite(
                            float(event["created_at"])):
                        raise ValueError("queue event timestamp is invalid")
                    if not isinstance(state, dict) or state.get("job_id") != job_id:
                        raise ValueError("queue event job does not match")
                    body = {"job_id": job_id, "kind": event["kind"], "state": state,
                            "created_at": float(event["created_at"])}
                    if (event["previous_hash"] != previous_hash
                            or event["event_hash"] != _event_hash(previous_hash, body)):
                        raise ValueError("queue event hash chain mismatch")
                    state_problems = self._queue_state_errors(state, set(blob_rows))
                    if state_problems:
                        raise ValueError(state_problems[0])
                    if float(event["created_at"]) != float(state["updated_at"]):
                        raise ValueError("queue event timestamp does not match its state")
                    if index == 0:
                        if event["kind"] not in {"enqueued", "migrated_snapshot"}:
                            raise ValueError("queue history has no creation event")
                        if event["kind"] == "enqueued" and (
                                state["status"] != QueueStatus.QUEUED.value
                                or state["attempts"] != 0):
                            raise ValueError("queue creation event has invalid state")
                    elif previous_state is not None:
                        if any(state[key] != previous_state[key]
                               for key in _JOB_IMMUTABLE_KEYS):
                            raise ValueError("immutable queue identity changed")
                        if state["status"] not in _QUEUE_TRANSITIONS[previous_state["status"]]:
                            raise ValueError("illegal queue status transition")
                        if state["status"] == QueueStatus.LEASED.value:
                            increment = 0 if previous_state["status"] == QueueStatus.LEASED.value else 1
                            if (state["attempts"] != previous_state["attempts"] + increment
                                    or state["lease_generation"] !=
                                    previous_state["lease_generation"] + increment):
                                raise ValueError("queue lease counters changed illegally")
                        elif (state["attempts"] != previous_state["attempts"]
                              or state["lease_generation"] != previous_state["lease_generation"]):
                            raise ValueError("queue counters changed outside a lease")
                    previous_hash = str(event["event_hash"])
                    previous_state = state
                    latest = state
                except Exception as exc:
                    errors.append("queue event history invalid for %s: %s" % (job_id, exc))
                    latest = None
                    break
            if latest is not None and latest != actual:
                errors.append("queue projection does not match event history: %s" % job_id)

    @_serialized
    def verify(self) -> VerificationReport:
        errors: list[str] = []
        quick = self._conn.execute("PRAGMA quick_check").fetchall()
        if any(str(row[0]).lower() != "ok" for row in quick):
            errors.append("sqlite quick_check failed")
        if self._conn.execute("PRAGMA foreign_key_check").fetchone() is not None:
            errors.append("foreign key check failed")
        blob_rows = {str(row["hash"]): row for row in self._conn.execute(
            "SELECT hash,size,data FROM blobs")}
        for row in blob_rows.values():
            data = bytes(row["data"])
            if int(row["size"]) != len(data):
                errors.append("blob size mismatch: %s" % row["hash"])
            if sha256(data) != row["hash"]:
                errors.append("blob hash mismatch: %s" % row["hash"])
        self._verify_jobs(blob_rows, errors)
        products = {str(row["product_id"]) for row in
                    self._conn.execute("SELECT product_id FROM products")}
        self._verify_chain("product_events", [(item,) for item in sorted(products)], errors)
        self._verify_memory(blob_rows, errors)
        commit_rows = {str(row["commit_hash"]): row for row in self._conn.execute(
            "SELECT commit_hash,product_id,parent_hash,snapshot_hash,metadata_json FROM commits")}
        prepared_rows = {str(row["commit_hash"]): row for row in self._conn.execute(
            "SELECT commit_hash,expected_revision,state,prepared_at,published_at "
            "FROM prepared_commits")}
        for commit_hash, commit in commit_rows.items():
            prepared = prepared_rows.get(commit_hash)
            if prepared is None:
                errors.append("commit lacks a prepared/published state: %s" % commit_hash)
            else:
                expected = str(prepared["expected_revision"])
                if not re.match(r"^\d+:(?:-|\*|[0-9a-f]{64})$", expected):
                    errors.append("prepared commit has invalid expected revision: %s" % commit_hash)
                if ((prepared["state"] == "published") !=
                        (prepared["published_at"] is not None)):
                    errors.append("prepared commit publication timestamp mismatch: %s" % commit_hash)
            if str(commit["product_id"]) not in products:
                errors.append("commit references unknown product: %s" % commit_hash)
            parent = commit["parent_hash"]
            if parent is not None:
                parent_row = commit_rows.get(str(parent))
                if parent_row is None or parent_row["product_id"] != commit["product_id"]:
                    errors.append("commit parent is missing or cross-product: %s" % commit_hash)
            entries = self._conn.execute(
                "SELECT e.path,e.blob_hash,b.size,b.data FROM commit_entries e "
                "LEFT JOIN blobs b ON b.hash=e.blob_hash "
                "WHERE e.commit_hash=? ORDER BY e.path", (commit_hash,)).fetchall()
            body = []
            for item in entries:
                try:
                    normalized = normalize_relative_path(str(item["path"]))
                    if normalized != item["path"]:
                        raise ValidationError("path is not normalized")
                except ValidationError:
                    errors.append("commit entry path invalid: %s" % commit_hash)
                if item["data"] is None or item["size"] is None:
                    errors.append("commit entry blob is missing: %s" % commit_hash)
                    continue
                data = bytes(item["data"])
                if int(item["size"]) != len(data) or sha256(data) != item["blob_hash"]:
                    errors.append("commit entry blob integrity mismatch: %s" % commit_hash)
                body.append({"path": item["path"], "blob_hash": item["blob_hash"],
                             "size": int(item["size"])})
            if sha256(canonical_json(body)) != commit["snapshot_hash"]:
                errors.append("commit snapshot mismatch: %s" % commit_hash)
                continue
            try:
                raw_metadata = bytes(commit["metadata_json"])
                metadata = json.loads(raw_metadata.decode("utf-8"))
                if not isinstance(metadata, dict) or canonical_json(metadata) != raw_metadata:
                    raise ValueError("metadata is not a canonical object")
                commit_body = {"product_id": commit["product_id"],
                               "parent_hash": commit["parent_hash"],
                               "snapshot_hash": commit["snapshot_hash"],
                               "metadata": metadata, "entries": body}
                if sha256(canonical_json(commit_body)) != commit_hash:
                    errors.append("commit lineage hash mismatch: %s" % commit_hash)
            except Exception:
                errors.append("commit metadata invalid: %s" % commit_hash)

        if set(prepared_rows) - set(commit_rows):
            errors.append("prepared state references a missing commit")

        canonical_commits: set[str] = set()
        for row in self._conn.execute(
                "SELECT product_id,revision,commit_hash FROM product_heads"):
            product_id = str(row["product_id"])
            revision = int(row["revision"])
            current = row["commit_hash"]
            if product_id not in products:
                errors.append("head references unknown product: %s" % product_id)
                continue
            if (revision == 0) != (current is None):
                errors.append("product head revision/commit mismatch: %s" % product_id)
                continue
            chain: list[str] = []
            seen: set[str] = set()
            while current is not None:
                commit_hash = str(current)
                if commit_hash in seen:
                    errors.append("commit lineage cycle: %s" % product_id)
                    break
                seen.add(commit_hash)
                commit = commit_rows.get(commit_hash)
                prepared = prepared_rows.get(commit_hash)
                if commit is None:
                    errors.append("product head lineage has missing commit: %s" % product_id)
                    break
                if commit["product_id"] != product_id:
                    errors.append("product head lineage crosses products: %s" % product_id)
                    break
                if prepared is None or prepared["state"] != "published":
                    errors.append("product head lineage includes unpublished commit: %s" % product_id)
                    break
                chain.append(commit_hash)
                current = commit["parent_hash"]
            if len(chain) != revision:
                errors.append("product head revision does not equal lineage depth: %s" % product_id)
            canonical_commits.update(chain)
            events = self._conn.execute(
                "SELECT kind,payload_json FROM product_events WHERE product_id=? "
                "ORDER BY event_id", (product_id,)).fetchall()
            created = [event for event in events if event["kind"] == "product_created"]
            published = [event for event in events if event["kind"] == "head_published"]
            if len(created) != 1 or not events or events[0]["kind"] != "product_created":
                errors.append("product event stream lacks one leading creation: %s" % product_id)
            try:
                event_hashes = [json.loads(bytes(event["payload_json"]).decode("utf-8"))[
                    "commit_hash"] for event in published]
                if event_hashes != list(reversed(chain)):
                    errors.append("published event history does not match product head: %s" % product_id)
            except Exception:
                errors.append("published event payload is invalid: %s" % product_id)
        published_commits = {commit_hash for commit_hash, row in prepared_rows.items()
                             if row["state"] == "published"}
        if published_commits != canonical_commits:
            errors.append("published commit set does not match canonical product lineages")
        return VerificationReport(not errors, tuple(errors))

    @_serialized
    def assert_verified(self) -> None:
        report = self.verify()
        if not report.ok:
            raise IntegrityError("; ".join(report.errors))

    @_serialized
    def backup(self, destination: Union[str, os.PathLike[str]]) -> Path:
        """Make a consistent SQLite backup using SQLite's backup API."""
        target = _database_path(destination)
        if target == Path(":memory:"):
            raise ValidationError("backup destination must be a filesystem path")
        parent_fd: Optional[int] = None
        target_fd: Optional[int] = None
        destination_conn: Optional[sqlite3.Connection] = None
        try:
            parent_fd, target_fd = _open_database_guards(target)
            if (self._database_fd is not None and
                    os.fstat(self._database_fd).st_dev == os.fstat(target_fd).st_dev and
                    os.fstat(self._database_fd).st_ino == os.fstat(target_fd).st_ino):
                raise ValidationError("backup destination must differ from the source database")
            destination_conn = sqlite3.connect(
                target.as_uri() + "?mode=rw", uri=True, timeout=5.0,
                isolation_level=None, check_same_thread=False,
            )
            _assert_guarded_database_path(target, parent_fd, target_fd)
            self._conn.backup(destination_conn)
            _assert_guarded_database_path(target, parent_fd, target_fd)
        finally:
            if destination_conn is not None:
                destination_conn.close()
            if target_fd is not None:
                os.close(target_fd)
            if parent_fd is not None:
                os.close(parent_fd)
        return target

    @classmethod
    def restore(cls, backup: Union[str, os.PathLike[str]], destination: Union[str, os.PathLike[str]]) -> "Store":
        """Copy a SQLite backup to a new or existing local database path."""
        source_path = _database_path(backup, require_exists=True)
        target_path = _database_path(destination)
        if source_path == Path(":memory:") or target_path == Path(":memory:"):
            raise ValidationError("restore paths must name filesystem databases")
        source_parent_fd: Optional[int] = None
        source_fd: Optional[int] = None
        target_parent_fd: Optional[int] = None
        target_fd: Optional[int] = None
        source: Optional[sqlite3.Connection] = None
        target: Optional[sqlite3.Connection] = None
        try:
            source_parent_fd, source_fd = _open_database_guards(source_path)
            target_parent_fd, target_fd = _open_database_guards(target_path)
            if (os.fstat(source_fd).st_dev == os.fstat(target_fd).st_dev and
                    os.fstat(source_fd).st_ino == os.fstat(target_fd).st_ino):
                raise ValidationError("restore destination must differ from the backup")
            source = sqlite3.connect(
                source_path.as_uri() + "?mode=rw", uri=True, timeout=5.0,
                isolation_level=None, check_same_thread=False,
            )
            target = sqlite3.connect(
                target_path.as_uri() + "?mode=rw", uri=True, timeout=5.0,
                isolation_level=None, check_same_thread=False,
            )
            _assert_guarded_database_path(source_path, source_parent_fd, source_fd)
            _assert_guarded_database_path(target_path, target_parent_fd, target_fd)
            source.backup(target)
            _assert_guarded_database_path(source_path, source_parent_fd, source_fd)
            _assert_guarded_database_path(target_path, target_parent_fd, target_fd)
        finally:
            if target is not None:
                target.close()
            if source is not None:
                source.close()
            for descriptor in (target_fd, target_parent_fd, source_fd, source_parent_fd):
                if descriptor is not None:
                    os.close(descriptor)
        return cls(target_path)


PMOSStore = Store
