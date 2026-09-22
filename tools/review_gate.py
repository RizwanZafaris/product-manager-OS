#!/usr/bin/env python3
"""Validate an exact-tree local review record without authenticating identity.

Reviewer identity and organizational independence require an external trust
domain and remain an external readiness gate.  This local check proves only
record shape, content binding, and finding disposition; it must never be
described as cryptographic or human-identity attestation.

A record that passes is well-formed and current. It is not evidence that a
review took place: a model can run --record over its own work, and the one
mechanical guard against that cannot fire here (see GUARD_LIMITS). Nor does
a plain gate run prove the recorded commands were ever run: it re-checks the
record against itself, and a record written by hand rather than by --record
can be self-consistent. ``--reexecute`` re-runs every recorded command and is
the only mode that tests the record against the tree.
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
    # products/ is where this repository tells every user to put their own
    # workspaces, and .gitignore keeps it out of the tree. It was not in this
    # set, so a reviewer with any local product digested a tree no clean
    # checkout has: the record then passed on that machine and failed in CI,
    # with nothing in the failure naming the cause. Found by exactly that,
    # on 2026-09-21. The tracked-file guard below still applies, so a
    # force-added file under products/ keeps it in the digest.
    "products",
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
# A recorded evidence command is re-run at record time, and the longest one
# this repository records is a full ci_gate.py sweep, which takes about four
# minutes. The ceiling is the same one readiness_registry.py gives its
# slowest probe, so a reviewer cannot hit a limit here that the repository's
# own verifiers do not hit.
EVIDENCE_TIMEOUT_SECONDS = 1800
# How much of a command's output the record keeps. A gate sweep prints tens of
# kilobytes; storing all of it would bury the review in the artefact meant to
# carry it. The window is centred on the matched text, so what is kept still
# shows the claim being met.
EVIDENCE_OUTPUT_LIMIT = 4096
# How much of a mismatching output a refusal prints. The head and the tail are
# both shown: a gate sweep prints its verdict ("release gates: N/M passed") on
# its last line, and a refusal cut from the front would hide exactly that.
REFUSAL_HEAD = 300
REFUSAL_TAIL = 500
# Where a reviewer transcript must live. Any path in the tree used to be
# accepted, so README.md or the change's own source could be named as "the
# reviewer's output" and hash correctly. A dedicated directory does not prove
# who wrote the file; it does make the claim "this is the transcript" one that
# a file was put there to make, rather than one any file already satisfies.
# Nothing here asks git whether the file is committed: the digest walks the
# filesystem, so an untracked file is accepted locally. A clean checkout that
# lacks it digests differently, so such a record is stale there.
TRANSCRIPT_DIR = "docs/readiness/review-transcripts/"
# Evidence is an ALLOWLIST: a recorded command must be one this repository
# itself defines as a check -- the argv of a gate in tools/ci_gate.py's GATES,
# or an exact entry in ci_gate.EVIDENCE_COMMANDS beside it -- split with shlex
# and compared as a whole, so an extra or different argument is refused. It
# replaced a denylist of shells and command runners. That list could not be
# finished: ``sh -c 'python3 lint.py --os; echo 26/26 passed'`` was refused,
# and the same chain came back behind ``find -exec`` and a git ``!`` alias.
# Re-running such a command proves it reproduces its output, never that it is
# the check it names, because the echo really does print the result.
#
# What the allowlist guarantees, and no more: the recorded command is one of
# those checks, written as the repository writes it, and it is run the way
# ci_gate.py runs it (its cwd, ci_gate's environment, ``python3`` replaced by
# the interpreter running this tool). It does not guarantee the output came
# from the recorded tree. A check can be run against a tree that differs from
# the one recorded -- a hand-written record can carry output from anywhere --
# and the tree-digest comparison is what covers that; --reexecute re-runs the
# check on the tree as it is now. The checks are themselves files in the
# tree, so a change that edits a check changes what that check proves; the
# digest covers that edit, and nothing here judges it. The interpreter running
# this tool, and the machine, are trusted: whoever runs the tool controls both.
# Printed by --record and by the gate itself. Both facts were true before and
# stated nowhere, which is the same defect this repository scores P0 in its own
# documents: a claim the code does not support. The phrase "identity not
# authenticated" reads narrower than it is, so what the guard cannot do is
# printed next to it rather than left for a reader to infer from the source.
# The author count is measured on every run rather than written in here: this
# repository's older history does carry a model as a commit author, outside the
# window recent_authors() reads, so a fixed sentence saying the window holds
# only the owner would be one history rewrite away from false.
GUARD_LIMITS = (
    "the self-attestation refusal compares the reviewer string to the %s",
    "git reports for this tree's last 40 commits. Any other name passes it",
    "unconditionally, so unless a model's name is among those it cannot fire",
    "on a model name in this repository.",
    "independent_implementation is set true by this tool. It is not elicited",
    "from the reviewer, and nothing here verifies it.",
)


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


def _read_attestation(path, root):
    """Read the canonical attestation record, refusing to follow a symlink
    anywhere on the path -- the file itself, or any directory above it.

    ``Path.read_text``, and a bare ``os.open(str(path), O_NOFOLLOW)`` alike,
    follow a symlink at every path component except the final one --
    ``O_NOFOLLOW`` only refuses when the leaf itself is a symlink. The writer
    had exactly this gap and was fixed for it (commit 2c3485f): a symlinked
    ``docs`` or ``docs/readiness`` sent a write wherever it pointed while
    ``record_review`` still reported success. The reader kept the
    leaf-only version, so a symlinked ``docs`` or ``docs/readiness`` holding
    an otherwise well-formed, digest-matching attestation would validate
    cleanly even though the file actually read was never inside the reviewed
    tree the digest is supposed to bind it to -- the writer refuses that
    layout outright, but the gate would read and accept it.

    Fixed the same way the writer was: ``path`` is required to resolve to a
    real descendant of ``root`` with no ``..`` or ``.`` component (mirroring
    ``_write_attestation``'s containment check, so ``--attestation`` cannot
    point outside the tree at all, symlink or not), and the file is then
    read through ``_read_relative`` -- a component-by-component walk from a
    descriptor on ``root`` with ``dir_fd``-relative opens and ``O_NOFOLLOW``
    throughout, so a symlink at any parent, or at the leaf, makes the open
    fail instead of resolving it. Fails closed with a plain ``OSError`` in
    every case; there is no fallback to pathname resolution.
    """
    path = Path(path)
    root = Path(root)
    try:
        relative = path.relative_to(root)
    except ValueError:
        raise OSError(
            "attestation path %s is not inside root %s; refusing to read "
            "it through pathname joining" % (path, root))
    parts = relative.parts
    if not parts:
        raise OSError("attestation path %s is the root itself" % (path,))
    if any(component in ("..", ".") for component in parts):
        # Same reasoning as _write_attestation's identical check: relative_to
        # is a string comparison of path segments, not a filesystem
        # resolution, so a literal ".." segment survives it. Refusing it here
        # keeps every component the walk below opens a real, named child of
        # the descriptor already held.
        raise OSError(
            "attestation path %s contains a relative path component "
            "('..' or '.'); refusing to walk it through the reviewed tree"
            % (path,))
    if not _dir_fd_operations_supported():
        raise OSError(
            "this platform lacks the dir_fd-relative filesystem operations "
            "(O_NOFOLLOW/O_DIRECTORY) the attestation read path needs to "
            "refuse a parent-directory symlink; refusing to fall back to "
            "pathname resolution instead")
    root_fd = os.open(str(root), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        payload = _read_relative(root_fd, relative)
    finally:
        os.close(root_fd)
    return payload.decode("utf-8")


def _dir_fd_operations_supported():
    """Whether this platform can do every dir_fd-relative call the safe
    attestation write needs, so the caller can refuse outright instead of
    quietly falling back to pathname resolution.

    ``os.replace`` is checked via ``os.rename``: both wrap the same
    ``renameat(2)`` on POSIX, but ``os.supports_dir_fd`` is only ever
    populated for the name ``rename`` was registered under, so probing
    ``os.replace`` directly under-reports support that is actually there.
    """
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        return False
    required = (os.open, os.stat, os.mkdir, os.rename, os.unlink)
    return all(function in os.supports_dir_fd for function in required)


def _replace_regular_file(dir_fd, name, contents):
    """Atomically write ``contents`` to ``name`` inside ``dir_fd``.

    Refuses before writing anything if ``name`` already exists as anything
    other than a plain regular file -- a symlink included, which is the leaf
    case commit a419774 closed and this keeps closed under the dir_fd
    rewrite. The new content lands in a sibling temporary name first and is
    moved onto ``name`` with ``os.replace(..., dir_fd=...)``: a rename inside
    one directory, which POSIX guarantees is atomic, so nothing ever reads a
    half-written attestation.
    """
    try:
        existing = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        existing = None
    if existing is not None and not stat.S_ISREG(existing.st_mode):
        raise OSError("attestation path %r is not a regular file" % (name,))

    tmp_name = ".%s.tmp-%d" % (name, os.getpid())
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(tmp_name, flags, 0o644, dir_fd=dir_fd)
    try:
        os.write(fd, contents.encode("utf-8"))
    finally:
        os.close(fd)
    try:
        os.replace(tmp_name, name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
    except BaseException:
        try:
            os.unlink(tmp_name, dir_fd=dir_fd)
        except OSError:
            pass
        raise


def _write_attestation(path, contents, root):
    """Write the attestation record, refusing to write through a symlink
    anywhere on the path -- the file itself, or any directory above it.

    The leaf was closed first (commit a419774): opening the final file with
    ``O_NOFOLLOW`` refuses if that last name is itself a symlink. But every
    *parent* directory was still reached by pathname -- ``os.makedirs`` to
    create a missing one, a plain ``os.open(str(path), ...)`` to reach the
    file inside it -- and pathname resolution follows a symlink at any
    component that is not the final one. Replacing ``docs`` or
    ``docs/readiness`` itself with a symlink therefore sent the write
    wherever that symlink pointed, inside the tree or outside it, while
    ``record_review`` went on to report success.

    Fixed by walking every parent component one at a time from a descriptor
    on ``root``, using ``dir_fd``-relative opens with ``O_NOFOLLOW``
    throughout: a missing component is created with
    ``os.mkdir(component, dir_fd=...)``, which can only ever create a
    directory inside the descriptor already held open, never through a
    symlink planted at an earlier component; an existing component is
    refused unless ``os.stat(..., follow_symlinks=False)`` says it is
    positively a directory, which also refuses a symlink that happens to
    point at one.

    ``root`` is required, not defaulted. It used to be optional, with a
    fallback branch for a caller that omitted it: that branch reached the
    parent directory by plain pathname (``os.makedirs`` plus a bare
    ``os.open(str(path), ...)``), which is exactly the unguarded resolution
    this function exists to avoid -- the round-2 bug all over again, just
    reachable through this helper's own default instead of through
    ``record_review``. No production caller ever omitted ``root``; only the
    direct unit test on this helper did, and that test now passes it
    explicitly instead of exercising a fallback nothing else used.

    Refuses outright, rather than falling back to pathname calls, on a
    platform lacking the O_NOFOLLOW/O_DIRECTORY flags or the dir_fd support
    this depends on.
    """
    if not _dir_fd_operations_supported():
        raise OSError(
            "this platform lacks the dir_fd-relative filesystem operations "
            "(O_NOFOLLOW/O_DIRECTORY plus os.supports_dir_fd coverage for "
            "open, stat, mkdir and rename) the attestation write path needs "
            "to refuse a parent-directory symlink; refusing to fall back to "
            "pathname resolution instead")

    path = Path(path)
    dir_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

    root = Path(root)
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        raise OSError(
            "attestation path %s is not inside root %s; refusing to write "
            "it through pathname joining" % (path, root))
    if not parts:
        raise OSError("attestation path %s is the root itself" % (path,))
    if any(component in ("..", ".") for component in parts):
        # ``relative_to`` is a string comparison of path segments; it does
        # not resolve ``..`` the way the filesystem does. A literal ``..``
        # segment survives it -- ``root / ".." / "outside" / "x.json"`` is a
        # valid child of ``root`` by that comparison alone -- and the walk
        # below would then genuinely open ``..`` with ``dir_fd=parent_fd``:
        # that entry always exists, is always a directory, and is never a
        # symlink, so none of the checks in the loop catch it. Refusing any
        # ``..`` or ``.`` component here, before the walk starts, is what
        # keeps every component the loop opens a real, named child of the
        # descriptor already held -- which is the guarantee the walk exists
        # to provide in the first place.
        raise OSError(
            "attestation path %s contains a relative path component "
            "('..' or '.'); refusing to walk it through the reviewed tree"
            % (path,))

    parent_fd = os.open(str(root), dir_flags)
    try:
        for component in parts[:-1]:
            try:
                info = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                os.mkdir(component, dir_fd=parent_fd)
                info = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
            if not stat.S_ISDIR(info.st_mode):
                raise OSError(
                    "attestation path component %r is not a plain directory "
                    "(refusing: a symlink or other non-directory here could "
                    "redirect the write outside the reviewed tree)" %
                    (component,))
            child_fd = os.open(component, dir_flags, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = child_fd
        _replace_regular_file(parent_fd, parts[-1], contents)
    finally:
        os.close(parent_fd)


def _ci_gate():
    """tools/ci_gate.py, the module beside this one that defines the checks."""
    tools = str(Path(__file__).resolve().parent)
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import ci_gate
    return ci_gate


def evidence_allowlist():
    """Every command evidence may name: {argv tuple: (cwd, timeout)}.

    Read from the tools/ci_gate.py beside this file: each gate's argv with
    that gate's cwd and timeout, then each exact entry of EVIDENCE_COMMANDS.
    """
    ci_gate = _ci_gate()
    forms = {}
    for gate in ci_gate.GATES:
        forms.setdefault(tuple(gate.argv), (gate.cwd, gate.timeout))
    for argv in ci_gate.EVIDENCE_COMMANDS:
        forms.setdefault(tuple(argv), (".", EVIDENCE_TIMEOUT_SECONDS))
    return forms


def evidence_form(command):
    """``(argv, cwd, timeout)`` for an evidence command, or raise OSError.

    Refuses a command that does not parse, and one whose argv is not exactly
    an entry of evidence_allowlist(). Shared by the record, the re-execution
    and the validator, so a plain gate run rejects a stored command that
    --record would have refused to run.
    """
    import shlex
    try:
        argv = shlex.split(command)
    except ValueError as error:
        raise OSError("it could not be parsed: %s" % (error,))
    form = evidence_allowlist().get(tuple(argv))
    if form is None:
        raise OSError(
            "it is not a check this repository defines. Evidence may name "
            "only the argv of a gate in tools/ci_gate.py GATES (python3 "
            "tools/ci_gate.py --manifest lists them) or an entry of "
            "ci_gate.EVIDENCE_COMMANDS, exactly as written there, with no "
            "other arguments")
    return argv, form[0], form[1]


def run_evidence(command, root):
    """Run one recorded evidence command in the reviewed tree.

    Returns its combined output and exit code; raises OSError when the
    command was refused by evidence_form, or could not be run to completion.

    The command must be on the allowlist (evidence_form; the comment
    beside TRANSCRIPT_DIR says what that does and does not guarantee). It is
    split with shlex and run as ONE
    program, never through a shell, the way ci_gate.py runs a gate: in that
    gate's cwd, with ci_gate's environment and PYTHONPATH pointing at the
    reviewed tree's tests/, and with ``python3`` replaced by the interpreter
    running this tool.

    What remains true, and is stated rather than hidden: the output is what
    the check printed on the tree it ran in. Whether that tree is the one the
    record pins is the digest comparison's job, not this function's.

    stderr is folded into stdout because that is what the reviewer read. A
    command whose telling line goes to stderr (git's fatals, unittest's
    summary) would otherwise be unquotable as evidence.
    """
    import subprocess
    argv, cwd, timeout = evidence_form(command)
    if argv[0] == "python3":
        argv = [sys.executable] + argv[1:]
    env = _ci_gate().environment()
    env["PYTHONPATH"] = str(Path(root) / "tests")
    try:
        done = subprocess.run(argv, cwd=str(Path(root) / cwd), shell=False,
                              env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise OSError("it did not finish within %d seconds" % timeout)
    except (OSError, subprocess.SubprocessError) as error:
        raise OSError("%s" % (error,))
    return _as_bytes(done.stdout).decode("utf-8", "replace"), done.returncode


def evidence_excerpt(output, result, limit=EVIDENCE_OUTPUT_LIMIT):
    """``output``, shortened around ``result`` and with the cut named in place.

    The whole output is kept when it is small, which is the ordinary case. A
    longer one is kept as a window that contains the matched text
    contiguously, so the validator's later substring re-check reads the
    excerpt exactly as it read the full output -- an excerpt that could break
    the match would turn a true record into a gate failure nobody could
    explain. The elision is written into the text rather than left implicit,
    because a reader must not mistake a window for everything the command
    said.
    """
    limit = max(limit, len(result))
    if len(output) <= limit:
        return output
    index = max(output.find(result), 0)
    end = min(len(output), max(0, index - (limit - len(result)) // 2) + limit)
    start = max(0, end - limit)
    excerpt = output[start:end]
    if start:
        excerpt = "[... %d characters elided ...]\n" % start + excerpt
    if end < len(output):
        excerpt += "\n[... %d characters elided ...]" % (len(output) - end)
    return excerpt


def refusal_display(output, head=REFUSAL_HEAD, tail=REFUSAL_TAIL):
    """What a refusal prints of a command's output: its head and its tail."""
    output = output.strip()
    if not output:
        return "(nothing)"
    if len(output) <= head + tail:
        return output
    return "%s\n[... %d characters elided ...]\n%s" % (
        output[:head], len(output) - head - tail, output[-tail:])


def parse_evidence(raw):
    """Split one --evidence value into (command, expected exit, result).

    ``COMMAND|RESULT`` expects the command to exit 0. ``COMMAND|exit=N|RESULT``
    records a command expected to exit N, which is how a red run a reviewer
    deliberately quotes (a gate sweep with CI-6 still red, a refusal) is
    recorded honestly. The exit code used to be stored and never compared, so
    ``ci_gate.py|passed`` was accepted on a red tree because "24/25 passed"
    contains "passed". Returns None when the value is malformed.
    """
    command, separator, rest = raw.partition("|")
    command, rest = command.strip(), rest.strip()
    expected = 0
    match = re.match(r"exit=(-?\d+)\|", rest)
    if match:
        expected = int(match.group(1))
        rest = rest[match.end():].strip()
    if not separator or not command or not rest:
        return None
    return command, expected, rest


def transcript_path_error(path):
    """Why ``path`` cannot name a reviewer transcript, or None."""
    # A ".." segment needs no check of its own: membership is decided
    # against the digest's rows, which hold normalised paths only, so
    # "review-transcripts/../README.md" is never found there.
    if not path.startswith(TRANSCRIPT_DIR):
        return ("reviewer transcript %s is not under %s: a transcript is a "
                "file put there to be one, not any file already in the tree"
                % (path, TRANSCRIPT_DIR))
    return None


def print_guard_limits(authors, indent="  "):
    """Say, in the tool's own output, what the tool does not prove."""
    if authors is None:
        counted = "author names and emails (unreadable just now)"
    else:
        counted = "%d author name(s) and email(s)" % len(authors)
    print(indent + "limits   : " + GUARD_LIMITS[0] % counted)
    for line in GUARD_LIMITS[1:]:
        print(indent + "           " + line)


def _transcript_errors(document, rows):
    """Check the reviewer's own output is in the tree the record binds to.

    The digest proves what was read. It said nothing about what the reviewer
    then wrote, so the record's verdict and findings were the only trace of
    the review itself and both were typed by whoever ran the tool. Requiring
    a transcript inside the tree puts the reviewer's output inside the
    digest: the file cannot be swapped after the fact without staling the
    record, and the record names which file it was. Whether git tracks it is
    not checked; see TRANSCRIPT_DIR.

    Membership is decided against the inventory ``tree_digest`` already
    built, not against git or the filesystem. That is the stronger test and
    the cheaper one: a path in those rows is by construction part of the
    reviewed tree and already carries the hash to compare, so a transcript
    that validates here is one whose bytes the digest covers.
    """
    path = document.get("reviewer_transcript")
    recorded = document.get("reviewer_transcript_sha256")
    if not isinstance(path, str) or not path.strip():
        return ["reviewer transcript path is missing"]
    if not isinstance(recorded, str) or not HEX64.match(recorded):
        return ["reviewer transcript digest is malformed"]
    misplaced = transcript_path_error(path)
    if misplaced:
        return [misplaced]
    row = next((r for r in rows
                if r["path"] == path and r["kind"] == "file"), None)
    if row is None:
        return ["reviewer transcript %s is not a file in the reviewed tree"
                % path]
    if row["sha256"] != recorded:
        return ["reviewer transcript %s does not hash to the value the record "
                "carries" % path]
    return []


def _evidence_errors(evidence):
    """Check each evidence item against the output recorded beside it.

    Evidence used to be free text of any shape: the writer took whatever was
    typed and the gate checked only that the list was non-empty, so a command
    nobody ran and a result nobody saw passed identically to a real one. The
    writer now re-runs each command and stores what it printed, which leaves
    this function two things to re-check on every later run of the gate --
    that each command is one --record would run (evidence_form), and that
    the result the record claims still appears in the output the record
    carries.

    Be precise about what that proves: internal consistency, and nothing
    more. It catches an edit to one half of an item -- a result changed
    without its output. It does NOT catch an edit to both halves, and it
    cannot tell a record --record wrote from one typed by hand: a
    hand-written item whose result appears in its own invented output passes
    here. It does not re-execute anything. ``reexecution_errors`` does, and
    is what tests the record against the tree; it runs only under
    ``--reexecute`` because a recorded gate sweep takes minutes.
    """
    if not isinstance(evidence, list):
        return []
    fields = {"command", "result", "output", "exit_code"}
    errors = []
    for index, item in enumerate(evidence, 1):
        if not isinstance(item, dict) or set(item) != fields:
            errors.append("review evidence item %d does not use the closed "
                          "evidence schema (command, result, output, "
                          "exit_code)" % index)
            continue
        command, result, output = (item.get("command"), item.get("result"),
                                   item.get("output"))
        label = "review evidence %d (%s)" % (
            index, command if isinstance(command, str) and command.strip()
            else "unnamed command")
        if not isinstance(command, str) or not command.strip():
            errors.append("%s: command is missing" % label)
        if not isinstance(result, str) or not result.strip():
            errors.append("%s: recorded result is empty" % label)
        if not isinstance(output, str):
            errors.append("%s: recorded output is missing" % label)
        if isinstance(item.get("exit_code"), bool) or not isinstance(
                item.get("exit_code"), int):
            errors.append("%s: recorded exit code is not an integer" % label)
        if isinstance(command, str) and command.strip():
            try:
                evidence_form(command)
            except OSError as error:
                errors.append("%s: --record would refuse to run it: %s"
                              % (label, error))
        if (isinstance(result, str) and result.strip() and
                isinstance(output, str) and result not in output):
            errors.append("%s: the recorded result does not appear in the "
                          "output recorded for that command" % label)
    return errors


def reexecution_errors(document, root=REPO):
    """Re-run every recorded evidence command and compare it to the record.

    This is the check a hand-written record cannot pass by being consistent
    with itself: the command must still run in this tree, exit with the code
    the record stores, and print the recorded result. It is opt-in
    (``--reexecute``) and ci_gate.py does not use it, because a recorded
    ci_gate.py sweep re-run from inside ci_gate.py would take minutes on
    every gate run. A plain gate run therefore does not re-execute anything.
    """
    errors = []
    evidence = document.get("evidence") if isinstance(document, dict) else None
    for index, item in enumerate(evidence or [], 1):
        if not isinstance(item, dict) or not isinstance(
                item.get("command"), str):
            continue
        label = "review evidence %d (%s)" % (index, item["command"])
        try:
            output, exit_code = run_evidence(item["command"], root)
        except OSError as error:
            errors.append("%s: re-run failed: %s" % (label, error))
            continue
        if exit_code != item.get("exit_code"):
            errors.append("%s: re-run exited %d, the record says %r"
                          % (label, exit_code, item.get("exit_code")))
        result = item.get("result")
        if isinstance(result, str) and result not in output:
            errors.append("%s: re-run output does not contain the recorded "
                          "result" % label)
    return errors


def validate_attestation(document, root=REPO):
    errors = []
    fields = {
        "schema", "reviewer_id", "reviewer_kind",
        "independent_implementation", "identity_assurance", "reviewed_at",
        "reviewed_tree_sha256", "reviewer_transcript",
        "reviewer_transcript_sha256", "scope", "evidence", "findings",
        "verdict",
    }
    if not isinstance(document, dict):
        return ["review attestation does not use the closed schema"]
    if set(document) != fields:
        # Naming the difference, rather than only the fact of it, is what
        # makes a record written against an older schema legible. The two
        # transcript fields were added after records already existed; a bare
        # "does not use the closed schema" on such a record reads as
        # corruption and sends a reader to the source to find out otherwise.
        detail = []
        missing = sorted(fields - set(document))
        unexpected = sorted(set(document) - fields)
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected " + ", ".join(unexpected))
        return ["review attestation does not use the closed schema (%s)"
                % "; ".join(detail)]
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
    actual, rows = tree_digest(root)
    if not isinstance(claimed, str) or not HEX64.match(claimed):
        errors.append("reviewed tree digest is malformed")
    elif claimed != actual:
        errors.append("review is stale: repository tree digest changed")
    errors.extend(_transcript_errors(document, rows))
    for field in ("scope", "evidence", "findings"):
        if not isinstance(document.get(field), list):
            errors.append("review %s must be a list" % field)
    if not document.get("scope"):
        errors.append("review scope cannot be empty")
    if not document.get("evidence"):
        errors.append("review evidence cannot be empty")
    if not document.get("findings"):
        # A review that found nothing is a legitimate outcome, but it is a
        # claim somebody makes, not a field nobody filled. Recording it as an
        # explicit P3 accepted finding is the difference between the two, and
        # the record printed "findings : 0" for both until this fired.
        errors.append("review findings cannot be empty: a review that found "
                      "nothing records that as an explicit P3 accepted "
                      "finding")
    errors.extend(_evidence_errors(document.get("evidence")))
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
    the recent history. That refusal is weaker than it sounds and
    print_guard_limits() says so in the tool's own output: it matches names,
    and nothing makes a model's name one of the commit authors it reads.

    What this can enforce at record time, it does. Every --evidence command
    must be a check the repository defines (evidence_allowlist: a gate's
    argv or an EVIDENCE_COMMANDS entry, exactly), and is run here, as one
    program with no shell, and refused unless it exits with the expected
    code and prints the recorded result; the output and exit code are
    stored. That holds for records this function writes. The gate cannot
    tell such a record from one typed by hand, so a plain gate run proves
    only that the record is consistent with itself and names allowlisted
    commands; ``--reexecute`` is what re-runs the commands against the tree.
    --finding is required, so "found nothing" is a claim somebody made; and
    --transcript must already be a file under TRANSCRIPT_DIR inside the tree,
    so that file is bound to the digest as the reviewer's output. Nothing
    here checks that git tracks it, or who wrote it.
    """
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
    if not args.finding:
        print("record: --finding is required. A review that found nothing "
              "says so on the record:")
        print("        --finding \"P3|accepted|no defect found|<what you "
              "read to conclude that>\"")
        print("        An empty findings list is indistinguishable from a "
              "field nobody filled.")
        return 2
    transcript = (args.transcript or "").strip()
    if not transcript:
        print("record: --transcript is required. Put the reviewer's own "
              "output under %s in this tree and name it here, relative to "
              "the repository root." % TRANSCRIPT_DIR)
        print("        The digest binds the record to what was read; this "
              "binds it to what the reviewer said about it.")
        return 2
    misplaced = transcript_path_error(transcript)
    if misplaced:
        print("record: REFUSED. " + misplaced)
        return 2
    # An early answer for a mistyped path, before any evidence command runs,
    # so a typo cannot cost a gate sweep. The row lookup after the digest is
    # what decides membership.
    if not (root / transcript).is_file():
        print("record: REFUSED. --transcript %r does not exist under %s."
              % (transcript, root))
        return 2

    findings = []
    for index, raw in enumerate(args.finding, 1):
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

    # Parse every evidence string before running any of them. A typo in the
    # last one should not cost the four minutes the first one takes.
    requested = []
    for raw in args.evidence:
        parsed = parse_evidence(raw)
        if parsed is None:
            print("record: --evidence must be COMMAND|RESULT or "
                  "COMMAND|exit=N|RESULT with both sides filled, got %r" % raw)
            print("        The command is re-run here and RESULT must appear "
                  "in its output, so an empty RESULT asserts nothing.")
            print("        A shell pipeline cannot be recorded: the first "
                  "'|' separates the command from the result.")
            return 2
        requested.append(parsed)

    executed = []
    for command, expected, result in requested:
        print("record: re-running %s" % command)
        try:
            output, exit_code = run_evidence(command, root)
        except OSError as error:
            print("record: REFUSED. evidence command %r could not be run: %s"
                  % (command, error))
            return 2
        if result not in output:
            print("record: REFUSED. evidence command %r ran and exited %d, "
                  "but the result you recorded is not in its output."
                  % (command, exit_code))
            print("        you recorded : %s" % result)
            print("        it printed   : %s" % refusal_display(output))
            return 2
        if exit_code != expected:
            print("record: REFUSED. evidence command %r exited %d; the "
                  "evidence expects %d." % (command, exit_code, expected))
            print("        A result that appears in a failing run's output "
                  "is not evidence the run passed.")
            print("        To quote a run you know fails, write "
                  "COMMAND|exit=%d|RESULT." % exit_code)
            print("        it printed   : %s" % refusal_display(output))
            return 2
        executed.append({
            "command": command, "result": result,
            "output": evidence_excerpt(output, result), "exit_code": exit_code,
        })

    # Digest the tree only now. An evidence command can touch the tree it
    # runs in, and a digest taken before it ran would pin the record to a
    # tree that no longer exists by the time the record is written -- stale
    # the moment it lands, for a reason nothing in its own output names.
    digest, rows = tree_digest(root)
    transcript_row = next((r for r in rows if r["path"] == transcript and
                           r["kind"] == "file"), None)
    if transcript_row is None:
        print("record: REFUSED. --transcript %r is not a file in the "
              "reviewed tree." % transcript)
        print("        Give a path relative to the repository root: a "
              "transcript outside the tree is not bound to the digest this "
              "record pins.")
        return 2

    document = {
        "schema": 1,
        "reviewer_id": reviewer,
        "reviewer_kind": args.reviewer_kind,
        "independent_implementation": True,
        "identity_assurance": "unauthenticated-local-claim",
        "reviewed_at": _dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "reviewed_tree_sha256": digest,
        "reviewer_transcript": transcript,
        "reviewer_transcript_sha256": transcript_row["sha256"],
        "scope": list(args.scope),
        "evidence": executed,
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
        _write_attestation(path, json.dumps(document, indent=2) + "\n", root)
    except OSError as error:
        print("record: REFUSED. %s" % error)
        return 2
    print("recorded review of %d files at %s" % (len(rows), digest[:12]))
    print("  reviewer : %s (%s, identity not authenticated)"
          % (reviewer, args.reviewer_kind))
    print("  transcript: %s (%s)"
          % (transcript, transcript_row["sha256"][:12]))
    print("  evidence : %d command(s) run here; a plain gate run re-checks "
          "the record against itself, --reexecute re-runs them"
          % len(executed))
    print("  verdict  : %s" % args.verdict)
    print("  findings : %d" % len(findings))
    print("  written  : %s" % path)
    print_guard_limits(authors)
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
                        help="a check you ran and text from its output. "
                             "Repeatable, at least one. COMMAND must be the "
                             "argv of a gate in tools/ci_gate.py (see its "
                             "--manifest) or an entry of its EVIDENCE_COMMANDS, "
                             "exactly; anything else is refused. It is re-run "
                             "in this tree as ci_gate.py runs it, with no "
                             "shell, and refused unless it exits 0 (or N, "
                             "written COMMAND|exit=N|RESULT) and RESULT "
                             "appears in what it prints")
    parser.add_argument("--finding", action="append",
                        metavar="SEVERITY|STATUS|SUMMARY|EVIDENCE",
                        help="a finding. Repeatable, at least one. A review "
                             "that found nothing records P3|accepted|...")
    parser.add_argument("--transcript", metavar="PATH",
                        help="the reviewer's own output, a file under "
                             + TRANSCRIPT_DIR + " in this tree, as a path "
                             "relative to the repository root. Commit it with "
                             "the record: a clean checkout without it "
                             "digests differently. Required")
    parser.add_argument("--reexecute", action="store_true",
                        help="also re-run every recorded evidence command and "
                             "fail unless each exits as recorded and prints "
                             "its recorded result. A plain run does not")
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
        document = json.loads(_read_attestation(path, REPO))
    except (OSError, json.JSONDecodeError) as error:
        print("independent review unavailable: %s" % error)
        return 1
    errors = validate_attestation(document, REPO)
    if args.reexecute and not errors:
        errors = reexecution_errors(document, REPO)
    for error in errors:
        print("review gate: " + error)
    if errors:
        return 1
    print("local review record: exact tree accepted; no unresolved P0/P1; "
          "reviewer identity is not authenticated and remains an external gate")
    if args.reexecute:
        print("  evidence : every recorded command re-run here and matched")
    else:
        print("  evidence : checked against the record itself, not re-run; "
              "--reexecute re-runs it")
    print_guard_limits(recent_authors(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
