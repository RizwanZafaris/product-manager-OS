"""Release provenance and tamper-evident artifact manifests.

The release format is intentionally boring JSON.  It records hashes and
metadata only; file contents, environment variables, and credentials never
enter a provenance document.  A verifier can therefore run offline and fail
closed when a file is missing, changed, or unexpectedly added.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional


PROVENANCE_FORMAT = "pmos.release-provenance/v3"
PROVENANCE_SCHEMA = "pmos.release.v3"
DEFAULT_PROVENANCE = Path("docs/release/provenance.json")
_SECRET_NAME_PARTS = (".env", ".pem", ".key", ".p12", ".pfx", "credentials", "secret")
_SKIP_DIRS = {".git", ".pmos", "__pycache__", ".mypy_cache", ".pytest_cache", ".tox", ".venv", "venv"}
_MAX_INVENTORY_ENTRIES = 16384
_MAX_INVENTORY_DEPTH = 64
_MAX_INVENTORY_BYTES = 256 * 1024 * 1024


class ProvenanceError(ValueError):
    """The manifest or release root is malformed."""


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    errors: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.ok


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _regular_file_digest(path: Path) -> tuple[str, int]:
    """Hash one stable regular file without following a swapped symlink."""
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ProvenanceError("release file hashing requires no-follow support")
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ProvenanceError("release path is not a regular file: %s" % path)
        digest = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size):
            raise ProvenanceError("release file changed while hashing: %s" % path)
        pathname = os.stat(path, follow_symlinks=False)
        if (not stat.S_ISREG(pathname.st_mode) or pathname.st_dev != before.st_dev or
                pathname.st_ino != before.st_ino):
            raise ProvenanceError("release path changed while hashing: %s" % path)
        return digest.hexdigest(), int(before.st_size)
    except ProvenanceError:
        raise
    except OSError as exc:
        raise ProvenanceError("cannot safely read release file: %s" % path) from exc
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass


def _sha256(path: Path) -> str:
    """Return a stable no-follow digest for callers needing only the hash."""
    return _regular_file_digest(path)[0]


def _regular_file_digest_at(root_fd: int, relative: str) -> tuple[str, int]:
    """Hash a regular release file through pinned no-follow directory fds."""
    parts = Path(relative).parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ProvenanceError("unsafe release path: %s" % relative)
    descriptors: list[int] = []
    try:
        current = os.dup(root_fd)
        descriptors.append(current)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        for component in parts[:-1]:
            current = os.open(component, flags | getattr(os, "O_DIRECTORY", 0), dir_fd=current)
            descriptors.append(current)
        file_fd = os.open(parts[-1], flags, dir_fd=current)
        descriptors.append(file_fd)
        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise ProvenanceError("release path is not a regular file: %s" % relative)
        digest = hashlib.sha256()
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(file_fd)
        current_name = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size or not stat.S_ISREG(current_name.st_mode) or
                current_name.st_dev != before.st_dev or current_name.st_ino != before.st_ino):
            raise ProvenanceError("release path changed while hashing: %s" % relative)
        return digest.hexdigest(), int(before.st_size)
    except ProvenanceError:
        raise
    except OSError as exc:
        raise ProvenanceError("cannot safely read release file: %s" % relative) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _root_fd(root: Path) -> int:
    try:
        return os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                       getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise ProvenanceError("cannot open release root safely: %s" % root) from exc


def _secret_path(relative: str) -> bool:
    lowered = relative.lower()
    name = Path(relative).name.lower()
    return name.startswith(".env") or any(part in lowered for part in _SECRET_NAME_PARTS)


def _category(relative: str) -> str:
    path = Path(relative)
    if relative.startswith("skills/") or path.name == "SKILL.md":
        return "skills"
    if (relative.startswith((".claude/", ".github/", "routing/")) or
            path.name in {"AGENTS.md", "CLAUDE.md", "pyproject.toml", "pmos_build_backend.py", "setup.cfg", "tox.ini"} or
            path.suffix.lower() in {".json", ".yaml", ".yml", ".toml", ".cfg", ".ini"}):
        return "config"
    return "artifacts"


def _git_output(root: Path, argv: list[str]) -> Optional[str]:
    try:
        completed = subprocess.run(
            ["git", *argv], cwd=str(root), shell=False,
            check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout


def _git_identity(root: Path, excluded: set[str]) -> tuple[Optional[str], Optional[bool]]:
    """Return a commit only when *root* is the repository root, plus cleanliness.

    A parent repository is not a provenance authority for an arbitrary nested
    directory.  The output manifest itself may be excluded, but no other
    tracked, staged, or untracked change is ignored.
    """
    top = _git_output(root, ["rev-parse", "--show-toplevel"])
    if top is None or Path(top.strip()).resolve() != root:
        return None, None
    raw_commit = _git_output(root, ["rev-parse", "HEAD"])
    if raw_commit is None:
        return None, None
    commit = raw_commit.strip().lower()
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        return None, None
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=str(root), shell=False, check=True, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return commit, None
    dirty = False
    for record in completed.stdout.split(b"\0"):
        if not record:
            continue
        # Porcelain v1 -z uses two status bytes, a space, then an unquoted path.
        try:
            relative = record[3:].decode("utf-8")
        except UnicodeDecodeError:
            dirty = True
            break
        if relative not in excluded:
            dirty = True
            break
    return commit, not dirty


def _open_relative_directory(root_fd: int, parts: list[str]) -> int:
    descriptor = os.dup(root_fd)
    try:
        for component in parts:
            next_descriptor = os.open(
                component, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                getattr(os, "O_NOFOLLOW", 0), dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _safe_symlink_target_at(root_fd: int, directory_fd: int, name: str, relative: str,
                            metadata: os.stat_result, excluded: set[str]) -> bytes:
    """Read and resolve one relative link from pinned descriptors only."""
    try:
        target = os.readlink(name, dir_fd=directory_fd)
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        current_target = os.readlink(name, dir_fd=directory_fd)
    except OSError as exc:
        raise ProvenanceError("cannot read release symlink: %s" % relative) from exc
    if (not stat.S_ISLNK(current.st_mode) or current.st_dev != metadata.st_dev or
            current.st_ino != metadata.st_ino or current_target != target):
        raise ProvenanceError("release symlink changed while reading: %s" % relative)
    if not target or Path(target).is_absolute() or "\x00" in target:
        raise ProvenanceError("release symlink has an unsafe target: %s" % relative)

    # Resolve chained, relative links under the pinned root.  This deliberately
    # rejects absolute or root-escaping targets and never asks the pathname
    # resolver to traverse a mutable parent directory.
    resolved = list(Path(relative).parts[:-1])
    pending = list(Path(target).parts)
    links = 0
    final_metadata: Optional[os.stat_result] = None
    while pending:
        component = pending.pop(0)
        if component in ("", "."):
            continue
        if component == "..":
            if not resolved:
                raise ProvenanceError("release symlink escapes the release root: %s" % relative)
            resolved.pop()
            continue
        parent_fd = _open_relative_directory(root_fd, resolved)
        try:
            candidate = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
            if stat.S_ISLNK(candidate.st_mode):
                links += 1
                if links > 32:
                    raise ProvenanceError("release symlink chain is too deep: %s" % relative)
                nested = os.readlink(component, dir_fd=parent_fd)
                if not nested or Path(nested).is_absolute() or "\x00" in nested:
                    raise ProvenanceError("release symlink has an unsafe target: %s" % relative)
                pending = list(Path(nested).parts) + pending
                continue
            if pending and not stat.S_ISDIR(candidate.st_mode):
                raise ProvenanceError("release symlink target is missing: %s" % relative)
            resolved.append(component)
            final_metadata = candidate
        except FileNotFoundError as exc:
            raise ProvenanceError("release symlink target is missing: %s" % relative) from exc
        finally:
            os.close(parent_fd)
    if not resolved or final_metadata is None:
        raise ProvenanceError("release symlink target is missing: %s" % relative)
    relative_target = "/".join(resolved)
    if relative_target in excluded or resolved[0] in _SKIP_DIRS:
        raise ProvenanceError(
            "release symlink targets excluded or unrecorded state: %s" % relative)
    return target.encode("utf-8")


def _safe_symlink_target(root: Path, path: Path, excluded: set[str]) -> bytes:
    """Compatibility wrapper for callers with a pathname, pinned internally."""
    relative = path.relative_to(root).as_posix()
    root_fd = _root_fd(root)
    try:
        parts = list(Path(relative).parts)
        parent_fd = _open_relative_directory(root_fd, parts[:-1])
        try:
            metadata = os.stat(parts[-1], dir_fd=parent_fd, follow_symlinks=False)
            return _safe_symlink_target_at(root_fd, parent_fd, parts[-1], relative,
                                           metadata, excluded)
        finally:
            os.close(parent_fd)
    finally:
        os.close(root_fd)


def _digest_file_at(directory_fd: int, name: str, relative: str,
                    metadata: os.stat_result) -> tuple[str, int]:
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                             dir_fd=directory_fd)
        before = os.fstat(descriptor)
        if (not stat.S_ISREG(before.st_mode) or before.st_dev != metadata.st_dev or
                before.st_ino != metadata.st_ino):
            raise ProvenanceError("release path changed while hashing: %s" % relative)
        digest = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size or not stat.S_ISREG(current.st_mode) or
                current.st_dev != before.st_dev or current.st_ino != before.st_ino):
            raise ProvenanceError("release path changed while hashing: %s" % relative)
        return digest.hexdigest(), int(before.st_size)
    except OSError as exc:
        raise ProvenanceError("cannot safely read release file: %s" % relative) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _inventory(root: Path, excluded: set[str]) -> list[tuple[str, str, str, int]]:
    """Snapshot a release tree through one pinned, no-follow descriptor tree."""
    result: list[tuple[str, str, str, int]] = []
    entries = 0
    total_bytes = 0
    root_fd = _root_fd(root)
    root_identity = os.fstat(root_fd)
    try:
        def visit(directory_fd: int, prefix: str, depth: int) -> None:
            nonlocal entries, total_bytes
            if depth > _MAX_INVENTORY_DEPTH:
                raise ProvenanceError("release tree exceeds directory depth limit")
            for name in sorted(os.listdir(directory_fd)):
                if not prefix and name in _SKIP_DIRS:
                    continue
                relative = (prefix + "/" + name).strip("/")
                if relative in excluded:
                    continue
                entries += 1
                if entries > _MAX_INVENTORY_ENTRIES:
                    raise ProvenanceError("release tree exceeds inventory entry limit")
                metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if stat.S_ISDIR(metadata.st_mode):
                    child = os.open(name, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                                    getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
                    try:
                        visit(child, relative, depth + 1)
                    finally:
                        os.close(child)
                elif stat.S_ISLNK(metadata.st_mode):
                    payload = _safe_symlink_target_at(root_fd, directory_fd, name, relative,
                                                      metadata, excluded)
                    total_bytes += len(payload)
                    result.append((relative, "symlink", hashlib.sha256(payload).hexdigest(),
                                   len(payload)))
                elif stat.S_ISREG(metadata.st_mode):
                    digest, size = _digest_file_at(directory_fd, name, relative, metadata)
                    total_bytes += size
                    result.append((relative, "file", digest, size))
                else:
                    raise ProvenanceError("release tree contains an unsupported special file: %s" % relative)
                if total_bytes > _MAX_INVENTORY_BYTES:
                    raise ProvenanceError("release tree exceeds byte limit")
        visit(root_fd, "", 0)
        current = os.stat(root, follow_symlinks=False)
        if current.st_dev != root_identity.st_dev or current.st_ino != root_identity.st_ino:
            raise ProvenanceError("release root changed while inventorying")
    except OSError as exc:
        raise ProvenanceError("cannot safely inventory release tree") from exc
    finally:
        os.close(root_fd)
    return result


def _files(root: Path, excluded: set[str]) -> list[tuple[str, Path, str]]:
    """Compatibility inventory view for callers that need only names and kinds."""
    return [(relative, root / relative, kind)
            for relative, kind, _digest, _size in _inventory(root, excluded)]


def _tree_hash(files: Mapping[str, Mapping[str, Any]]) -> str:
    return hashlib.sha256(_canonical({key: files[key] for key in sorted(files)})).hexdigest()


def build_provenance(root: str | os.PathLike[str], *, output: str | os.PathLike[str] | None = None,
                     source_commit: Optional[str] = None) -> dict[str, Any]:
    """Build a manifest for *root* without recording file contents or secrets."""
    base = Path(root).expanduser().resolve()
    if not base.is_dir():
        raise ProvenanceError("release root is not a directory: %s" % base)
    target = Path(output).expanduser().resolve() if output else (base / DEFAULT_PROVENANCE)
    output_parent_fd: Optional[int] = None
    if output is not None:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            output_parent_fd = os.open(target.parent, os.O_RDONLY |
                                       getattr(os, "O_DIRECTORY", 0) |
                                       getattr(os, "O_NOFOLLOW", 0))
        except OSError as exc:
            raise ProvenanceError("cannot open provenance output parent safely") from exc
    excluded = {target.relative_to(base).as_posix()} if target.is_relative_to(base) else set()
    if target.is_relative_to(base) and _secret_path(target.relative_to(base).as_posix()):
        raise ProvenanceError("provenance output cannot use a secret-like path")
    entries: dict[str, dict[str, Any]] = {}
    counts = {"artifacts": 0, "config": 0, "skills": 0}
    for relative, kind, digest, size in _inventory(base, excluded):
        if _secret_path(relative):
            raise ProvenanceError(
                "release tree contains a secret-like path: %s" % relative)
        category = _category(relative)
        entry = {"category": category, "kind": kind,
                 "sha256": digest, "size": size}
        entries[relative] = entry
        counts[category] += 1
    discovered_commit, clean = _git_identity(base, excluded)
    if source_commit is not None and (clean is not True or
                                      source_commit.lower() != discovered_commit):
        raise ProvenanceError(
            "source_commit overrides are accepted only for the clean, current Git HEAD")
    source_state = ("git-clean" if clean is True else
                    "git-dirty" if clean is False else "not-a-git-root")
    manifest: dict[str, Any] = {
        "format": PROVENANCE_FORMAT,
        "schema": PROVENANCE_SCHEMA,
        # A dirty tree is deliberately not attributed to HEAD: the file hashes
        # still identify it, while source_commit remains an honest null.
        "source_commit": discovered_commit if clean is True else None,
        "source_state": source_state,
        "files": {key: entries[key] for key in sorted(entries)},
        "counts": counts,
    }
    if output is not None:
        try:
            manifest["provenance_path"] = target.relative_to(base).as_posix()
        except ValueError:
            pass
    manifest["tree_sha256"] = _tree_hash(manifest["files"])
    if output is not None:
        descriptor: Optional[int] = None
        temporary_name = target.name + ".tmp-%s" % secrets.token_hex(16)
        try:
            descriptor = os.open(temporary_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                                 getattr(os, "O_NOFOLLOW", 0), 0o600,
                                 dir_fd=output_parent_fd)
            payload = _canonical(manifest) + b"\n"
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            if descriptor is not None:
                os.close(descriptor)
        try:
            os.replace(temporary_name, target.name, src_dir_fd=output_parent_fd,
                       dst_dir_fd=output_parent_fd)
            os.fsync(output_parent_fd)
        finally:
            os.close(output_parent_fd)
    return manifest


def _load_manifest(manifest: Mapping[str, Any] | str | os.PathLike[str]) -> Mapping[str, Any]:
    if isinstance(manifest, Mapping):
        return manifest
    path = Path(manifest)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProvenanceError("cannot read provenance manifest") from exc
    if not isinstance(value, Mapping):
        raise ProvenanceError("provenance manifest must be an object")
    return value


def verify_provenance(root: str | os.PathLike[str], manifest: Mapping[str, Any] | str | os.PathLike[str]) -> VerificationResult:
    """Verify a manifest against the current release tree."""
    errors: list[str] = []
    manifest_path: Optional[Path] = None
    if not isinstance(manifest, Mapping):
        manifest_path = Path(manifest).expanduser().resolve()
    try:
        value = _load_manifest(manifest)
    except ProvenanceError as exc:
        return VerificationResult(False, (str(exc),))
    if value.get("format") != PROVENANCE_FORMAT:
        errors.append("unsupported provenance format")
    if value.get("schema") != PROVENANCE_SCHEMA:
        errors.append("unsupported provenance schema")
    allowed_fields = {"format", "schema", "source_commit", "source_state",
                      "files", "counts", "tree_sha256", "provenance_path"}
    required_fields = allowed_fields - {"provenance_path"}
    if set(value) - allowed_fields or not required_fields.issubset(value):
        errors.append("provenance manifest does not use the closed schema")
    files = value.get("files")
    if not isinstance(files, Mapping):
        return VerificationResult(False, tuple(errors + ["files must be an object"]))
    root_path = Path(root).expanduser().resolve()
    output_path: Optional[str] = None
    if manifest_path is not None:
        try:
            output_path = manifest_path.relative_to(root_path).as_posix()
        except ValueError:
            output_path = None
        claimed = value.get("provenance_path")
        if claimed is not None and claimed != output_path:
            errors.append("provenance path does not match the loaded manifest path")
    elif "provenance_path" in value:
        errors.append("mapping manifest cannot choose a provenance exclusion")
    expected: dict[str, Mapping[str, Any]] = {}
    for relative, entry in files.items():
        if not isinstance(relative, str) or not isinstance(entry, Mapping):
            errors.append("malformed file entry")
            continue
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts or not relative or "\\" in relative:
            errors.append("unsafe manifest path: %s" % relative)
            continue
        if set(entry) != {"category", "kind", "sha256", "size"}:
            errors.append("malformed file entry fields: %s" % relative)
            continue
        if (not isinstance(entry.get("sha256"), str) or
                len(entry["sha256"]) != 64 or
                any(ch not in "0123456789abcdef" for ch in entry["sha256"])):
            errors.append("malformed file hash: %s" % relative)
            continue
        if not isinstance(entry.get("size"), int) or isinstance(entry.get("size"), bool) or \
                entry["size"] < 0:
            errors.append("malformed file size: %s" % relative)
            continue
        if _secret_path(relative):
            errors.append("secret-like path must not be recorded: %s" % relative)
            continue
        if entry.get("kind") not in {"file", "symlink"}:
            errors.append("malformed file kind: %s" % relative)
            continue
        expected[relative] = entry
    try:
        scanned = _inventory(root_path, {output_path} if output_path else set())
    except ProvenanceError as exc:
        return VerificationResult(False, tuple(errors + [str(exc)]))
    actual_inventory = {relative: (kind, digest, size)
                        for relative, kind, digest, size in scanned}
    secret_paths = sorted(relative for relative in actual_inventory
                          if _secret_path(relative))
    errors.extend("secret-like path present in release tree: %s" % relative
                  for relative in secret_paths)
    actual_paths = set(actual_inventory)
    unexpected = sorted(actual_paths - set(expected))
    errors.extend("unrecorded file: %s" % relative for relative in unexpected)
    for relative, entry in expected.items():
        observed = actual_inventory.get(relative)
        if observed is None:
            errors.append("missing or unsafe file: %s" % relative)
            continue
        kind, actual, actual_size = observed
        if kind != entry.get("kind"):
            errors.append("missing or changed symlink: %s" % relative)
            continue
        if actual != entry.get("sha256"):
            errors.append("hash mismatch: %s" % relative)
        if actual_size != entry.get("size"):
            errors.append("size mismatch: %s" % relative)
        if entry.get("category") != _category(relative):
            errors.append("category mismatch: %s" % relative)
    if value.get("tree_sha256") != _tree_hash(expected):
        errors.append("tree hash mismatch")
    counts = value.get("counts")
    if isinstance(counts, Mapping):
        actual_counts = {kind: sum(1 for entry in expected.values() if entry.get("category") == kind)
                         for kind in ("artifacts", "config", "skills")}
        if dict(counts) != actual_counts:
            errors.append("category counts mismatch")
    else:
        errors.append("counts must be an object")

    state = value.get("source_state")
    claimed_commit = value.get("source_commit")
    discovered_commit, clean = _git_identity(root_path, {output_path} if output_path else set())
    if state == "git-clean":
        if (not isinstance(claimed_commit, str) or len(claimed_commit) != 40 or
                any(ch not in "0123456789abcdef" for ch in claimed_commit)):
            errors.append("clean Git provenance needs a valid source commit")
        elif clean is not True or discovered_commit != claimed_commit:
            errors.append("source commit is not bound to the clean current Git HEAD")
    elif state == "git-dirty":
        if claimed_commit is not None:
            errors.append("dirty Git provenance must not claim a source commit")
        if clean is not False:
            errors.append("source state no longer matches a dirty Git tree")
    elif state == "not-a-git-root":
        if claimed_commit is not None:
            errors.append("non-Git provenance must not claim a source commit")
        if clean is not None:
            errors.append("source state falsely claims the root is not Git")
    else:
        errors.append("source state is invalid")
    return VerificationResult(not errors, tuple(errors))


__all__ = ["DEFAULT_PROVENANCE", "PROVENANCE_FORMAT", "PROVENANCE_SCHEMA",
           "ProvenanceError", "VerificationResult", "build_provenance", "verify_provenance"]
