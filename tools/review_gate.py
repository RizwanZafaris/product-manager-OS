#!/usr/bin/env python3
"""Validate an exact-tree local review record without authenticating identity.

Reviewer identity and organizational independence require an external trust
domain and remain an external readiness gate.  This local check proves only
record shape, content binding, and finding disposition; it must never be
described as cryptographic or human-identity attestation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATTESTATION = Path("docs/readiness/independent-review.json")
ROOT_SKIP_DIRS = frozenset({
    ".git", ".readiness", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".tox", ".venv", "venv", "build", "dist",
})
NESTED_CACHE_DIRS = frozenset({"__pycache__", ".pytest_cache", ".mypy_cache"})
SKIP_NAMES = frozenset({".DS_Store"})
APPLEDOUBLE_PREFIX = "._"
GIT_CONTROL_NAME = ".git"
BUILD_ARTIFACT_SUFFIXES = (".pyc", ".pyo")
GIT_TIMEOUT_SECONDS = 30
HEX64 = re.compile(r"^[0-9a-f]{64}$")
# Git's own wording when it has positively determined there is no repository
# here at all (a plain directory, or one whose parents were all searched and
# none carried a .git). This is deliberately narrow: dubious ownership,
# permission failures, and config errors are nonzero exits too, but none of
# them say this, and none of them mean "nothing is tracked here".
NOT_A_GIT_REPOSITORY = re.compile(rb"not a git repository", re.IGNORECASE)
# Git's wording for a repository that positively exists but has no commits
# yet. There is no history to check for self-attestation there either, so it
# is treated the same as "no repository": an empty author set, not a fail.
NO_COMMITS_YET = re.compile(rb"does not have any commits yet", re.IGNORECASE)
MAX_TREE_ENTRIES = 16384
MAX_TREE_DEPTH = 64
MAX_TREE_BYTES = 256 * 1024 * 1024


def _as_bytes(value):
    """Coerce ``_git`` output to bytes regardless of how it arrived.

    Real ``_git`` calls always return ``bytes`` (see below). A caller that
    substitutes its own ``subprocess.CompletedProcess`` -- a test simulating
    a git failure it cannot literally reproduce, such as a specific fatal
    exit -- may hand back plain ``str`` fields instead. Both must be handled
    the same way, so tracked-ness logic is not accidentally re-coupled to one
    output type.
    """
    if isinstance(value, bytes):
        return value
    if value is None:
        return b""
    return value.encode("utf-8", "surrogateescape")


def _git(root, *args):
    """Run git in ``root`` and return its result with UNDECODED byte output.

    Raises OSError when git cannot be executed at all. Output is deliberately
    left as bytes rather than captured with ``text=True``: universal-newline
    translation rewrites a bare CR byte to LF, and a git-tracked *filename*
    can itself contain a literal CR. That rewrite made the path string this
    function returned for such a file disagree with the real on-disk name by
    one byte, the tracked-set lookup for it missed, and the file was silently
    excluded from the reviewed tree. Callers decode at the point of use:
    ordinary text output (``rev-parse``) is plain ASCII and safe to decode
    directly; path output (``ls-files -z``) must be decoded with filesystem
    semantics (``os.fsdecode``), never with newline translation.
    """
    import subprocess
    try:
        return subprocess.run(("git",) + args, cwd=str(root), capture_output=True,
                              timeout=GIT_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as error:
        raise OSError("review tree could not consult git: %s" % (error,))


def git_control_present(root):
    """Whether git control metadata exists at ``root`` or above it.

    Answers the only question that matters when git refuses to talk: is there
    a repository here whose absence of an answer should be fatal? A ``.git``
    entry -- the directory a clone carries, or the ``gitdir:`` pointer file a
    worktree or submodule carries -- is that evidence, and GIT_DIR names it
    explicitly when the environment overrides discovery.

    Ancestors count, because a subdirectory of a repository is still inside
    one, which is exactly the case git's own discovery walks.
    """
    override = os.environ.get("GIT_DIR")
    if override and Path(override).exists():
        return True
    current = Path(root).resolve()
    for candidate in (current, *current.parents):
        if (candidate / GIT_CONTROL_NAME).exists():
            return True
    return False


def tracked_paths(root):
    """Every path git tracks under ``root``, or None outside a work tree.

    Tracked-ness, not the filename, decides what the review covers. This exists
    because the previous rule excluded any name beginning ``._`` outright, on
    the stated but false premise that git cannot carry such a file. ``git add
    -f`` overrides .gitignore, so a tracked ``._policy.json`` was force-added,
    omitted from the reviewed inventory, and could have its contents flipped
    without moving the digest a recorded review is pinned to.

    Fails closed. If ``root`` is a work tree whose index cannot be read, this
    raises rather than reporting an empty set, because "git told us nothing"
    and "git tracks nothing" must never collapse into the same answer -- the
    first would silently exclude every metadata-named file in the tree.

    Returns None when ``root`` is not a work tree at all. There is no tracked
    content to protect there, so the filesystem-metadata exclusion applies on
    its own; this is the case for temporary directories and ad-hoc trees.

    A nonzero ``rev-parse`` exit is not by itself proof of that. Git also
    exits nonzero for dubious ownership, permission failures, and a broken
    config -- none of which mean there is no tracked content here, and all of
    which previously fell into this same "return None" path, letting every
    metadata-shaped file be excluded because git could not be consulted. Only
    git's own positive statement that no repository exists is trusted; any
    other failure to inspect raises instead of guessing.
    """
    probe = _git(root, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0:
        stderr = _as_bytes(probe.stderr)
        # git's wording cannot carry this decision on its own. A repository
        # whose object store has been renamed away answers a rev-parse with
        # the very same "fatal: not a git repository" line as a plain
        # directory, so trusting the message excluded a tracked file from a
        # damaged repository and left its digest unmoved when it was edited.
        # Control metadata on disk is the fact; the message is only
        # corroboration.
        if git_control_present(root):
            raise OSError(
                "review tree at %s carries git control metadata but git could "
                "not inspect it (rev-parse exited %d: %s); refusing to treat "
                "an unreadable repository as an empty tracked set" %
                (root, probe.returncode,
                 stderr.decode("utf-8", "replace").strip()))
        if NOT_A_GIT_REPOSITORY.search(stderr) is not None:
            return None
        raise OSError(
            "review tree could not determine whether %s is a git work tree "
            "(git rev-parse exited %d: %s); refusing to treat an inspection "
            "failure as an empty tracked set" %
            (root, probe.returncode, stderr.decode("utf-8", "replace").strip()))
    if _as_bytes(probe.stdout).strip() != b"true":
        return None
    listing = _git(root, "ls-files", "-z")
    if listing.returncode != 0:
        raise OSError("review tree is a git work tree whose index could not be "
                      "read; refusing to treat that as an empty tracked set")
    return frozenset(os.fsdecode(entry)
                     for entry in _as_bytes(listing.stdout).split(b"\0") if entry)


def is_excluded_sidecar(name):
    """True for a name that *looks* like OS-generated or build metadata.

    A name alone is never sufficient to exclude anything; callers must also
    confirm the path is untracked. See :func:`is_reviewable_artifact`.
    """
    return (name in SKIP_NAMES or name.startswith(APPLEDOUBLE_PREFIX) or
            name.endswith(BUILD_ARTIFACT_SUFFIXES))


def is_reviewable_artifact(relative, name, tracked):
    """Whether an entry belongs in the reviewed tree.

    macOS writes an AppleDouble sidecar (``._name``) beside every entry on a
    filesystem without native extended-attribute support -- exFAT, FAT and SMB,
    which is what an external drive gives you. Hashing those made the digest
    depend on which filesystem the checkout sat on, so a review recorded on
    such a workspace could never match the digest CI computes for the same
    commit. Excluding them is the same judgement already made for .DS_Store.

    But the exclusion is only safe for content git is not carrying. Anything
    tracked is reviewed no matter what it is called, which keeps both
    properties at once: an untracked sidecar cannot break reproducibility, and
    a metadata-shaped filename cannot smuggle tracked content past a reviewer.
    """
    if not is_excluded_sidecar(name):
        return True
    if tracked is not None and relative in tracked:
        return True
    return False


def _read_relative(root_fd, relative):
    parts = Path(relative).parts
    descriptors = []
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
            raise OSError("not a regular file")
        payload = b"".join(iter(lambda: os.read(file_fd, 65536), b""))
        current_name = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
        if current_name.st_dev != before.st_dev or current_name.st_ino != before.st_ino:
            raise OSError("path changed")
        return payload
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _read_entry(directory_fd, name, metadata):
    """Read a regular entry from the descriptor that enumerated it."""
    descriptor = None
    try:
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                             dir_fd=directory_fd)
        before = os.fstat(descriptor)
        if (not stat.S_ISREG(before.st_mode) or before.st_dev != metadata.st_dev or
                before.st_ino != metadata.st_ino):
            raise OSError("review file changed")
        payload = b"".join(iter(lambda: os.read(descriptor, 65536), b""))
        after = os.fstat(descriptor)
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if (before.st_dev != after.st_dev or before.st_ino != after.st_ino or
                before.st_size != after.st_size or not stat.S_ISREG(current.st_mode) or
                current.st_dev != before.st_dev or current.st_ino != before.st_ino):
            raise OSError("review file changed")
        return payload
    finally:
        if descriptor is not None:
            os.close(descriptor)


def tree_digest(root=REPO):
    """Hash paths, file kinds and bytes, excluding only review/ephemera."""
    root = Path(root).resolve()
    tracked_cache = []
    rows = []
    entries = 0
    total_bytes = 0
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                      getattr(os, "O_NOFOLLOW", 0))
    root_identity = os.fstat(root_fd)
    try:
        def tracked_set():
            """Consult git only if something metadata-shaped actually turns up.

            Deferring the call keeps the subprocess out of the walk for trees
            that contain no such entry. That matters for correctness, not only
            speed: the race-detection tests patch os.read globally and act on
            the first non-empty read, and an eager `git ls-files` would consume
            that read from its own pipe before the inventory ever began.
            """
            if not tracked_cache:
                tracked_cache.append(tracked_paths(root))
            return tracked_cache[0]

        def add(relative, kind, payload):
            nonlocal entries, total_bytes
            entries += 1
            total_bytes += len(payload)
            if entries > MAX_TREE_ENTRIES:
                raise OSError("review tree exceeds entry limit")
            if total_bytes > MAX_TREE_BYTES:
                raise OSError("review tree exceeds byte limit")
            rows.append({
                "path": relative,
                "kind": kind,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size": len(payload),
            })

        def visit(directory_fd, prefix, depth):
            nonlocal entries
            if depth > MAX_TREE_DEPTH:
                raise OSError("review tree exceeds directory depth limit")
            for name in sorted(os.listdir(directory_fd)):
                relative = (prefix + "/" + name).strip("/")
                at_root = not prefix
                metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if at_root and name == GIT_CONTROL_NAME:
                    # A plain clone carries .git as a directory; `git worktree
                    # add` and submodule checkouts carry it as a regular file
                    # holding an absolute "gitdir:" pointer unique to that
                    # checkout. Skipping only the directory form made every
                    # worktree hash differently from the clone CI builds, so a
                    # review recorded in a task worktree could never validate.
                    # Neither form is reviewable content.
                    continue
                if stat.S_ISDIR(metadata.st_mode):
                    if not at_root and name in NESTED_CACHE_DIRS:
                        continue
                    if at_root and (name in ROOT_SKIP_DIRS or name.endswith(".egg-info")):
                        # A root-level scratch directory is skipped by name
                        # only while git carries nothing beneath it. `git add
                        # -f` can force-track a file inside `dist/` or
                        # `build/` past .gitignore, and skipping the whole
                        # directory by name let such a file change content
                        # without moving the digest a recorded review is
                        # pinned to -- the same defect class the ._ exclusion
                        # above was fixed for. tracked_set() is None outside
                        # a git work tree, which keeps the old behaviour
                        # there: nothing tracked to protect, so the name-only
                        # exclusion is safe.
                        tracked = tracked_set()
                        tracked_beneath = tracked is not None and any(
                            p == name or p.startswith(name + "/")
                            for p in tracked)
                        if not tracked_beneath:
                            continue
                    entries += 1
                    if entries > MAX_TREE_ENTRIES:
                        raise OSError("review tree exceeds entry limit")
                    child = os.open(name, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                                    getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
                    try:
                        visit(child, relative, depth + 1)
                    finally:
                        os.close(child)
                    continue
                if relative == ATTESTATION.as_posix():
                    continue
                if (is_excluded_sidecar(name) and
                        not is_reviewable_artifact(relative, name, tracked_set())):
                    continue
                if stat.S_ISLNK(metadata.st_mode):
                    target = os.readlink(name, dir_fd=directory_fd)
                    current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    current_target = os.readlink(name, dir_fd=directory_fd)
                    if (not stat.S_ISLNK(current.st_mode) or current.st_dev != metadata.st_dev or
                            current.st_ino != metadata.st_ino or current_target != target):
                        raise OSError("review symlink changed")
                    add(relative, "symlink", target.encode("utf-8"))
                elif stat.S_ISREG(metadata.st_mode):
                    add(relative, "file", _read_entry(directory_fd, name, metadata))
                else:
                    raise OSError("review tree contains an unsupported special file")

        visit(root_fd, "", 0)
    finally:
        current_root = os.stat(root, follow_symlinks=False)
        os.close(root_fd)
    if (not stat.S_ISDIR(current_root.st_mode) or current_root.st_dev != root_identity.st_dev or
            current_root.st_ino != root_identity.st_ino):
        raise OSError("review root changed while inventorying")
    rows.sort(key=lambda row: row["path"])
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest(), tuple(rows)


def _read_attestation(path):
    """Read the canonical attestation record, refusing to follow a symlink.

    ``Path.read_text`` follows symlinks like any other ``open(2)`` call. The
    attestation path is a well-known, fixed location
    (``docs/readiness/independent-review.json``) that ``tree_digest`` itself
    deliberately excludes from the hash it binds a review to -- so a symlink
    planted at that exact path is never caught by the reviewed-tree digest
    either. Reading through it would validate whatever file the symlink
    pointed to, inside the repository or outside it, as though it were the
    record written to this path, defeating the point of pinning a review to
    an exact file. ``O_NOFOLLOW`` on the open refuses that outright: if the
    final path component is a symlink, the open fails instead of resolving
    it.
    """
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise OSError("attestation path %s is not a regular file" % path)
        payload = b"".join(iter(lambda: os.read(fd, 65536), b""))
        return payload.decode("utf-8")
    finally:
        os.close(fd)


def _write_attestation(path, contents):
    """Write the attestation record, refusing to write through a symlink.

    ``Path.write_text`` follows symlinks the same way ``read_text`` does. If
    the canonical attestation path had been replaced with a symlink -- to
    another file inside the tracked tree, or to something outside the
    repository entirely -- an unguarded write would silently overwrite
    whatever that symlink pointed to instead of the attestation file itself,
    while ``record_review`` went on to report success. ``O_NOFOLLOW`` on the
    open refuses to resolve a symlink at that path; ``O_CREAT`` still creates
    an ordinary new file when nothing exists there yet, because there is
    nothing to follow in that case.
    """
    directory = os.path.dirname(str(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags, 0o644)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise OSError("attestation path %s is not a regular file" % path)
        os.write(fd, contents.encode("utf-8"))
    finally:
        os.close(fd)


def validate_attestation(document, root=REPO):
    errors = []
    fields = {
        "schema", "reviewer_id", "reviewer_kind",
        "independent_implementation", "identity_assurance", "reviewed_at",
        "reviewed_tree_sha256", "scope", "evidence", "findings",
        "verdict",
    }
    if not isinstance(document, dict) or set(document) != fields:
        return ["review attestation does not use the closed schema"]
    if document.get("schema") != 1:
        errors.append("review schema must be 1")
    reviewer = document.get("reviewer_id")
    if not isinstance(reviewer, str) or not reviewer or reviewer == "root":
        errors.append("reviewer identity is missing or not independent")
    if document.get("reviewer_kind") not in ("independent-agent", "human"):
        errors.append("reviewer kind must be independent-agent or human")
    if document.get("independent_implementation") is not True:
        errors.append("reviewer must attest they implemented none of the reviewed tree")
    if document.get("identity_assurance") != "unauthenticated-local-claim":
        errors.append("local review identity must be labelled unauthenticated")
    if not isinstance(document.get("reviewed_at"), str) or not re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
            document.get("reviewed_at", "")):
        errors.append("reviewed_at must be an explicit UTC timestamp")
    claimed = document.get("reviewed_tree_sha256")
    actual, _rows = tree_digest(root)
    if not isinstance(claimed, str) or not HEX64.match(claimed):
        errors.append("reviewed tree digest is malformed")
    elif claimed != actual:
        errors.append("review is stale: repository tree digest changed")
    for field in ("scope", "evidence", "findings"):
        if not isinstance(document.get(field), list):
            errors.append("review %s must be a list" % field)
    if not document.get("scope"):
        errors.append("review scope cannot be empty")
    if not document.get("evidence"):
        errors.append("review evidence cannot be empty")
    finding_fields = {"id", "severity", "status", "summary", "evidence"}
    finding_ids = set()
    for finding in document.get("findings", []):
        if not isinstance(finding, dict) or set(finding) != finding_fields:
            errors.append("each finding must use the closed finding schema")
            continue
        if finding.get("id") in finding_ids:
            errors.append("duplicate review finding id")
        finding_ids.add(finding.get("id"))
        severity = finding.get("severity")
        status = finding.get("status")
        if severity not in ("P0", "P1", "P2", "P3"):
            errors.append("review finding severity is invalid")
        if status not in ("open", "resolved", "accepted"):
            errors.append("review finding status is invalid")
        if severity in ("P0", "P1") and status != "resolved":
            errors.append("review has unresolved %s finding %s" %
                          (severity, finding.get("id")))
    if document.get("verdict") != "accepted":
        errors.append("independent review verdict is not accepted")
    return errors


def recent_authors(root, limit=40):
    """Names and emails that authored the recent history of this tree.

    Used to refuse a self-attestation. This is a weak check and is meant to
    be: it catches the obvious case where the person recording the review is
    the person who wrote the commits, and it cannot catch a reviewer who uses
    a different name. Independence is asserted by a human either way; this
    only removes the easiest way to assert it falsely by accident.

    Returns None when git control metadata is present but the history could
    not be read (a corrupted repository, an unreadable object store, a
    missing HEAD). This used to return an empty set on any failure, which let
    the self-attestation refusal fail open: a reviewer whose name matched an
    author of a history git could not read was recorded anyway, because
    "git told us nothing" and "there is no history to check" collapsed into
    the same answer. That is the same distinction tracked_paths() makes for
    the reviewed tree itself, and record_review() below refuses outright
    rather than guess when this returns None. An empty set is still correct,
    not a failure, for a tree with no git control metadata at all and for a
    repository that positively has no commits yet -- both have no history to
    protect.
    """
    import subprocess
    try:
        done = subprocess.run(
            ["git", "log", "--format=%an%n%ae", "-%d" % int(limit)],
            cwd=str(root), capture_output=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None if git_control_present(root) else set()
    if done.returncode != 0:
        stderr = _as_bytes(done.stderr)
        if NO_COMMITS_YET.search(stderr) is not None:
            return set()
        # Control-metadata presence decides before the message does, the
        # same order tracked_paths() above uses and for the same reason: a
        # damaged repository (for instance a HEAD file overwritten with
        # garbage) makes git print the identical "fatal: not a git
        # repository" line a plain directory gets, so trusting the message
        # here first would let a self-attestation through on a tree that
        # very much has commit history git merely could not read.
        if git_control_present(root):
            return None
        if NOT_A_GIT_REPOSITORY.search(stderr) is not None:
            return set()
        return None
    stdout = _as_bytes(done.stdout).decode("utf-8", "replace")
    return {line.strip().lower() for line in stdout.splitlines() if line.strip()}


def record_review(args, root=REPO):
    """Write a review record for the tree as it stands right now.

    This exists because the gate was closable only by hand-writing JSON with
    a correct schema and a correct digest, and a gate nobody can close is a
    gate everybody learns to ignore. Three pull requests were merged with this
    check red before it was added.

    It records; it does not vouch. identity_assurance stays
    unauthenticated-local-claim, because nothing here authenticates anyone,
    and the tool refuses outright when the reviewer name matches an author of
    the recent history. That refusal is the one integrity property worth
    having: the person who wrote the code must not be able to close the gate
    on it by running a command.
    """
    digest, rows = tree_digest(root)
    reviewer = (args.reviewer or "").strip()
    if not reviewer or reviewer.lower() == "root":
        print("record: --reviewer must name the person who did the review")
        return 2

    authors = recent_authors(root)
    if authors is None:
        print("record: REFUSED. this tree's commit history could not be "
              "inspected, so a self-attestation by %r cannot be ruled out."
              % reviewer)
        print("        The self-attestation refusal only protects when git "
              "can be read; it does not stand in for it.")
        return 2
    if reviewer.lower() in authors:
        print("record: REFUSED. %r authored commits in this tree's recent "
              "history, so recording this review would be a self-attestation."
              % reviewer)
        print("        The point of this gate is that somebody who did not "
              "write the change has read it.")
        print("        If you genuinely did not implement any of it and the "
              "name simply matches, use the name you review under.")
        return 2

    if not args.scope:
        print("record: --scope is required. Say what you actually reviewed, "
              "so a later reader knows what this covers.")
        return 2
    if not args.evidence:
        print("record: --evidence is required. Name at least one command you "
              "ran. A review that ran nothing is a reading.")
        return 2

    findings = []
    for index, raw in enumerate(args.finding or [], 1):
        parts = raw.split("|")
        if len(parts) != 4:
            print("record: --finding must be "
                  "SEVERITY|STATUS|SUMMARY|EVIDENCE, got %r" % raw)
            return 2
        severity, status, summary, evidence = (p.strip() for p in parts)
        findings.append({
            "id": "R%d" % index, "severity": severity, "status": status,
            "summary": summary, "evidence": evidence,
        })

    document = {
        "schema": 1,
        "reviewer_id": reviewer,
        "reviewer_kind": args.reviewer_kind,
        "independent_implementation": True,
        "identity_assurance": "unauthenticated-local-claim",
        "reviewed_at": _dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "reviewed_tree_sha256": digest,
        "scope": list(args.scope),
        "evidence": [{"command": c, "result": r} for c, r in
                     (e.split("|", 1) + [""] if "|" not in e else e.split("|", 1)
                      for e in args.evidence)],
        "findings": findings,
        "verdict": args.verdict,
    }

    errors = validate_attestation(document, root)
    if errors:
        print("record: the record this would write does not validate:")
        for error in errors:
            print("  " + error)
        return 1

    path = Path(args.attestation)
    if not path.is_absolute():
        path = root / path
    try:
        _write_attestation(path, json.dumps(document, indent=2) + "\n")
    except OSError as error:
        print("record: REFUSED. %s" % error)
        return 2
    print("recorded review of %d files at %s" % (len(rows), digest[:12]))
    print("  reviewer : %s (%s, identity not authenticated)"
          % (reviewer, args.reviewer_kind))
    print("  verdict  : %s" % args.verdict)
    print("  findings : %d" % len(findings))
    print("  written  : %s" % path)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--digest", action="store_true",
                        help="print the current reviewable tree digest")
    parser.add_argument("--attestation", default=str(ATTESTATION))
    parser.add_argument("--record", action="store_true",
                        help="record a review of the tree as it stands now. "
                             "Refuses if the reviewer authored recent history")
    parser.add_argument("--reviewer", help="who did the review")
    parser.add_argument("--reviewer-kind", default="human",
                        choices=("human", "independent-agent"))
    parser.add_argument("--scope", action="append", metavar="WHAT",
                        help="what was reviewed. Repeatable, at least one")
    parser.add_argument("--evidence", action="append", metavar="COMMAND|RESULT",
                        help="a command you ran and what it returned. "
                             "Repeatable, at least one")
    parser.add_argument("--finding", action="append",
                        metavar="SEVERITY|STATUS|SUMMARY|EVIDENCE",
                        help="a finding. Repeatable. Omit if none")
    # The validator accepts exactly one verdict, so the CLI offers exactly one
    # rather than letting a reviewer type "rejected", write nothing, and learn
    # why at the end. A rejection is recorded by not recording: the gate stays
    # red, which is what a rejection means.
    parser.add_argument("--verdict", default="accepted",
                        choices=("accepted",),
                        help="only 'accepted' is recordable. A rejection is "
                             "expressed by leaving the gate red, and by saying "
                             "so wherever the change is being discussed")
    args = parser.parse_args(argv)
    if args.record:
        return record_review(args)
    if args.digest:
        digest, rows = tree_digest(REPO)
        print(json.dumps({"files": len(rows), "sha256": digest}, sort_keys=True))
        return 0
    path = Path(args.attestation)
    if not path.is_absolute():
        path = REPO / path
    try:
        document = json.loads(_read_attestation(path))
    except (OSError, json.JSONDecodeError) as error:
        print("independent review unavailable: %s" % error)
        return 1
    errors = validate_attestation(document, REPO)
    for error in errors:
        print("review gate: " + error)
    if errors:
        return 1
    print("local review record: exact tree accepted; no unresolved P0/P1; "
          "reviewer identity is not authenticated and remains an external gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
