"""Build a product's Conductor for every client (the CLI, the use cases and the
adapters) from the product's pinned question bank contract and its workspace root.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import stat
from pathlib import Path
from typing import Any

from .artifacts import build_manifest, check_manifest
from .banks import LEGACY_ONBOARDING, banks_from_contract, parse_contract
from .conductor import Conductor, QuestionBank
from .store import Store, ValidationError

# The path in a product's Store snapshot where its question bank contract is
# pinned, beside the Conductor's own state.
PIN_PATH = ".pmos/conductor/banks.json"


def pinned_contract(store: Store, product_id: str) -> dict[str, Any] | None:
    """The product's pinned question bank contract, or None when it has no pin."""
    files = store.read_snapshot(product_id).files
    if PIN_PATH in files:
        return parse_contract(files[PIN_PATH])
    return None


def product_banks(store: Store, product_id: str) -> tuple[QuestionBank, ...]:
    """The banks a product runs: its pinned contract, or LEGACY_ONBOARDING itself.

    A product keeps the banks it started with, so a repository update never
    strands it mid-interview. A product created before the pin keeps the
    legacy onboarding bank.
    """
    contract = pinned_contract(store, product_id)
    if contract is None:
        return LEGACY_ONBOARDING
    return banks_from_contract(contract)


def product_conductor(store: Store, root: Path, product_id: str) -> Conductor:
    """The Conductor every CLI command builds for a product, bound to its workspace.

    A product with a pinned contract gets the gate manifest builder and verifier:
    each approval records the revisions of the workspace artifacts whose block
    names that bank's gate, with their dependencies, and every later turn checks
    them again. A product that started before the pin runs the legacy onboarding
    bank, which has no gate number, so it runs without them.

    Both shapes get the document reader: a supplied quotation is checkable only
    against text, and the Conductor has no filesystem access of its own.
    """
    contract = pinned_contract(store, product_id)
    if contract is None:
        return Conductor(store, product_id, LEGACY_ONBOARDING,
                         gate_source_verifier=local_gate_verifier(root),
                         source_resolver=source_resolver(root),
                         document_reader=document_reader(root))
    # banks_from_contract validates every entry first, so a malformed contract
    # raises ValidationError here rather than a KeyError below.
    banks = banks_from_contract(contract)
    gates: dict[str, int] = {}
    for entry in contract["banks"]:
        gate = entry.get("gate")
        if not isinstance(gate, int) or isinstance(gate, bool):
            raise ValidationError("question bank contract is malformed: bank %s has no gate number" % entry["id"])
        gates[entry["id"]] = gate

    def gate_manifest(bank_id: str) -> dict[str, Any]:
        if bank_id not in gates:
            raise ValidationError("bank %s has no gate in the pinned contract" % bank_id)
        return build_manifest(root, gates[bank_id])

    def manifest_verifier(manifest: Any) -> dict[str, Any]:
        return check_manifest(root, manifest)

    return Conductor(store, product_id, banks, gate_source_verifier=local_gate_verifier(root),
                     source_resolver=source_resolver(root),
                     document_reader=document_reader(root),
                     gate_manifest=gate_manifest, manifest_verifier=manifest_verifier)


# The ceiling on any workspace file the runtime reads whole: a proof artifact it
# hashes, or a document it checks a quotation against.
MAX_WORKSPACE_FILE_BYTES = 16 * 1024 * 1024


def _with_bounded_file(resolved_root: Path, source: str, use):
    """Return ``use(file_descriptor)`` for a workspace-relative file, or None.

    None means one of three things: the source is not a bounded, non-symlink
    regular file below the root, so ``use`` was never called; ``use`` itself
    returned None (both callers do once a read passes the ceiling); or ``use``
    raised OSError, ValueError or TypeError. Each path component is opened relative
    to the one before it with ``O_NOFOLLOW``, so a symlink planted anywhere
    along the way is refused; resolving the whole path first and checking the
    result afterwards would have followed it already.
    """
    relative = Path(source)
    if (relative.is_absolute() or not relative.parts or ".." in relative.parts or
            relative.parts[0] == ".pmos" or "\\" in source):
        return None
    opened: list[int] = []
    try:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | \
            getattr(os, "O_NOFOLLOW", 0)
        # O_NONBLOCK so a named pipe planted at the cited path opens at once and
        # is refused by the regular-file check below, instead of blocking the
        # open until something writes to it. A regular file ignores the flag.
        file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        current = os.open(resolved_root, directory_flags)
        opened.append(current)
        for component in relative.parts[:-1]:
            current = os.open(component, directory_flags, dir_fd=current)
            opened.append(current)
        file_fd = os.open(relative.parts[-1], file_flags, dir_fd=current)
        opened.append(file_fd)
        metadata = os.fstat(file_fd)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_WORKSPACE_FILE_BYTES:
            return None
        return use(file_fd)
    except (OSError, ValueError, TypeError):
        return None
    finally:
        for descriptor in reversed(opened):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _read_bounded(file_fd: int) -> bytes | None:
    """The whole file, or None once it grows past the ceiling mid-read."""
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = os.read(file_fd, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > MAX_WORKSPACE_FILE_BYTES:
            return None
        chunks.append(chunk)


def local_gate_verifier(root: Path):
    """Verify a bounded, non-symlink proof artifact below the workspace root."""
    resolved_root = root.resolve()

    def digest_of(file_fd: int) -> str | None:
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                return digest.hexdigest()
            total += len(chunk)
            if total > MAX_WORKSPACE_FILE_BYTES:
                return None
            digest.update(chunk)

    def verify(source: str, expected_hash: str) -> bool:
        actual = _with_bounded_file(resolved_root, source, digest_of)
        if actual is None:
            return False
        try:
            return hmac.compare_digest(actual, expected_hash)
        except TypeError:
            # An expected hash that is not a str, or a str with non-ASCII
            # characters, is a mismatch, not a crash in the caller.
            return False

    return verify


def document_reader(root: Path):
    """Read a cited workspace document so a supplied quotation can be checked.

    The Conductor holds no filesystem access by construction, and
    ``source_resolver`` answers only True/False/None, so a quotation could
    never be compared with the document it claims to come from without a
    second injected callable that hands back the text. Returns the decoded
    text, or None when the source is not a readable UTF-8 workspace document,
    which the Conductor turns into a refusal rather than a pass.
    """
    resolved_root = root.resolve()

    def read(source: str) -> str | None:
        if not isinstance(source, str):
            return None
        raw = _with_bounded_file(resolved_root, source, _read_bounded)
        if raw is None:
            return None
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            # A binary or mis-encoded file is not a document a quotation can be
            # checked against, and guessing an encoding would invent the text.
            return None

    return read


def _looks_like_local_path(source: str) -> bool:
    """Heuristic: does ``source`` look like a workspace-relative path?"""
    if not source:
        return False
    if "\\" in source:
        return True
    if source.startswith(("./", ".\\", "~", "../", "..\\")):
        return True
    if source in {".", "..", "~"}:
        return True
    if "/" in source:
        return True
    # A bare name with a file extension ("notes.md"). Free text such as
    # "Q3 review v1.2" has spaces or a numeric suffix and stays free text.
    if not re.search(r"\s", source) and re.search(r"\.[A-Za-z][A-Za-z0-9]{0,11}$", source):
        return True
    return False


def source_resolver(root: Path):
    """Resolve a caller-supplied source the way the gate verifier bounds it.

    Returns True when the source is a regular file that exists below the
    workspace root, False when it looks like a local path but is missing or
    escapes the root, and None when it does not look like a local path at all
    (free text or an interview id), so the conductor records it as supplied
    unverified instead of refusing the answer.
    """
    resolved_root = root.resolve()

    def resolve(source: str):
        if not isinstance(source, str) or not source:
            return None
        if "://" in source:
            return None
        if not _looks_like_local_path(source):
            return None
        relative = Path(source)
        if relative.is_absolute() or ".." in relative.parts or relative.parts and relative.parts[0] == ".pmos":
            return False
        try:
            candidate = (resolved_root / relative).resolve(strict=False)
        except (OSError, ValueError):
            return False
        try:
            candidate.relative_to(resolved_root)
        except ValueError:
            return False
        return candidate.is_file()

    return resolve
