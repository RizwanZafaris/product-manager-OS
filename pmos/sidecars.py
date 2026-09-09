"""Positive recognition of macOS AppleDouble sidecar files.

The defect this closes. macOS writes an AppleDouble sidecar (``._name``)
beside every entry on a filesystem without native extended-attribute
support -- exFAT, FAT and SMB, which is what an external drive gives you. A
checkout that lives on such a volume carries hundreds of these, none tracked
by git, and every loader in this repository that enumerates a directory with
``rglob``, ``glob`` or ``iterdir`` and then reads what it finds chokes on
one: the sidecar's body is the binary AppleDouble container format, not
UTF-8 text, and it is not the JSON, Markdown or Python the loader expected
either. Hosted CI runs on Linux and never sees the problem; a maintainer
whose checkout sits on exFAT sees it on nearly every command.

The fix is deliberately narrow. A name is never enough on its own -- a
tracked file that happens to be named ``._policy.json`` is real content, not
metadata, as ``tools/review_gate.py`` already established for the git-aware
digest. This module makes the same judgement for the parts of the codebase
that have no git dependency to lean on (``pmos/`` is dependency-free by
policy, and ``tools/`` may import it because it already imports ``pmos``).
Rather than trusting the tracked-set the way ``review_gate`` does, it trusts
the AppleDouble file format itself: a sidecar carries a fixed 4-byte magic
number at the start of its body, and it only ever exists beside the real
file it shadows. Recognition is positive on both counts, so nothing is
excused by name alone.

A path is an AppleDouble sidecar only if ALL of the following hold:

- its name starts with ``._``;
- it is a regular file -- not a symlink, not a directory;
- its first 4 bytes are the AppleDouble magic ``00 05 16 07``;
- a sibling entry named ``name`` with the ``._`` prefix removed exists in
  the same directory.

Anything that fails any one of those checks is not excused: a directory
named ``._foo``, a plain file that merely starts with ``._`` but carries no
magic header, or a sidecar with no sibling all get the unmodified behaviour
of whatever inspects them (crash, error, or listing) that they would have
gotten before this module existed.

Format alone turned out not to be enough either. The independent review of
this module force-added a genuine AppleDouble file beside its sibling and
the predicate excused it, because git was carrying it and nothing here had
asked. ``SidecarFilter`` below adds the half ``tools/review_gate.py`` already
had: a file git tracks is content whatever its bytes look like and is never
excused; only in a tree git does not know is the format the whole rule.
``review_gate`` keeps its own copy of the tracked-set logic because its
exclusion is name-only under tracked-ness; a test in
``test_pmos_invariants.py`` pins that the two never disagree about a name
that both could apply to.
"""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

APPLEDOUBLE_MAGIC = b"\x00\x05\x16\x07"
APPLEDOUBLE_PREFIX = "._"


def is_appledouble_sidecar(directory, name):
    """True only if ``name`` inside ``directory`` is a real AppleDouble sidecar.

    ``directory`` may be any path-like object; ``name`` is the bare entry
    name (no separators). All four conditions in the module docstring must
    hold; any I/O failure while checking is treated as "not a sidecar" so a
    vanished or unreadable entry falls back to whatever the caller would
    otherwise have done with it.
    """
    if not name.startswith(APPLEDOUBLE_PREFIX) or len(name) <= len(APPLEDOUBLE_PREFIX):
        return False
    directory = Path(directory)
    candidate = directory / name
    try:
        info = candidate.lstat()
    except OSError:
        return False
    if not stat.S_ISREG(info.st_mode):
        return False
    try:
        with open(candidate, "rb") as handle:
            header = handle.read(len(APPLEDOUBLE_MAGIC))
    except OSError:
        return False
    if header != APPLEDOUBLE_MAGIC:
        return False
    sibling = directory / name[len(APPLEDOUBLE_PREFIX):]
    try:
        sibling.lstat()
    except OSError:
        return False
    return True


def is_appledouble_sidecar_path(path):
    """Convenience wrapper: ``is_appledouble_sidecar`` from one ``Path``."""
    path = Path(path)
    return is_appledouble_sidecar(path.parent, path.name)


def without_appledouble_sidecars(paths):
    """Filter an iterable of ``Path`` objects, dropping real sidecars only.

    Every other entry -- directories named ``._foo``, tracked or untracked
    files that merely look like sidecars, real files with ordinary names --
    passes through unchanged.
    """
    for path in paths:
        path = Path(path)
        if not is_appledouble_sidecar(path.parent, path.name):
            yield path



GIT_CONTROL_NAME = ".git"
GIT_TIMEOUT_SECONDS = 30


class SidecarInspectionError(OSError):
    """A git work tree is present but could not be consulted.

    Raised instead of guessing, because "git told us nothing" and "git tracks
    nothing here" must never collapse into the same answer: the first would
    let every sidecar-shaped file be excused, tracked or not.
    """


def git_control_present(root):
    """Whether git control metadata exists at ``root`` or above it.

    A ``.git`` entry, the directory a clone carries or the ``gitdir:`` pointer
    file a worktree carries, is the evidence; ``GIT_DIR`` names it explicitly
    when the environment overrides discovery. Ancestors count, because a
    subdirectory of a repository is still inside one.
    """
    override = os.environ.get("GIT_DIR")
    if override and Path(override).exists():
        return True
    current = Path(root).resolve()
    for candidate in (current, *current.parents):
        if (candidate / GIT_CONTROL_NAME).exists():
            return True
    return False


def _git(root, *args):
    try:
        return subprocess.run(("git",) + args, cwd=str(root), capture_output=True,
                              timeout=GIT_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as error:
        raise SidecarInspectionError(
            "sidecar filter could not consult git in %s: %s" % (root, error))


def tracked_paths(root):
    """Paths git tracks under ``root``, relative to it; None outside a work tree.

    The same judgement ``tools/review_gate.py`` makes for the reviewed digest,
    carried here so the loaders can make it too. An independent review of
    the first sidecar fix force-added ``._real.md`` with genuine AppleDouble
    bytes beside ``real.md``, and the positive-recognition predicate excused
    it: git was carrying the file, and the loaders never looked. Tracked-ness
    is the fact that settles it. A file git carries is content whatever its
    bytes look like, and is never excused; a file git does not carry, in a
    tree git does not know, is judged by its format alone.

    Fails closed. When control metadata is present but git cannot answer (a
    damaged repository, a permission failure, a missing binary), this raises
    rather than returning an empty set, for the reason on the exception.
    Returns None only when there is no repository here at all, which is the
    case for temporary directories, ad-hoc trees and packaged installs.
    """
    root = Path(root)
    if not git_control_present(root):
        return None
    probe = _git(root, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0:
        raise SidecarInspectionError(
            "%s carries git control metadata but git could not inspect it "
            "(rev-parse exited %d: %s); refusing to treat an unreadable "
            "repository as an empty tracked set" %
            (root, probe.returncode,
             (probe.stderr or b"").decode("utf-8", "replace").strip()))
    if (probe.stdout or b"").strip() != b"true":
        return None
    listing = _git(root, "ls-files", "-z")
    if listing.returncode != 0:
        raise SidecarInspectionError(
            "%s is inside a git work tree whose index could not be read; "
            "refusing to treat that as an empty tracked set" % root)
    # Bytes, decoded with filesystem semantics: a tracked name can carry a
    # bare CR, and text-mode newline translation would rewrite it.
    return frozenset(os.fsdecode(entry)
                     for entry in (listing.stdout or b"").split(b"\0") if entry)


class SidecarFilter:
    """The complete rule: AppleDouble by format, and not carried by git.

    Construct one per walk root. Construction consults git once (or not at
    all outside a repository); ``excused`` then answers per path with no
    further process spawns. ``is_appledouble_sidecar`` alone is only the
    format half of this rule and is kept for callers that have no root.
    """

    def __init__(self, root):
        self.root = Path(root)
        self._resolved = self.root.resolve()
        self.tracked = tracked_paths(self.root)

    def excused(self, path):
        path = Path(path)
        if not is_appledouble_sidecar(path.parent, path.name):
            return False
        try:
            relative = path.resolve().relative_to(self._resolved).as_posix()
        except (OSError, ValueError):
            # Outside the root this filter was built for, or gone. The fourth
            # review round handed a genuine sidecar from another directory to
            # a filter built on a directory git did not know, and it was
            # excused because the root check came after the no-repository
            # shortcut. A filter answers for its root and nothing else.
            return False
        if self.tracked is None:
            return True
        return relative not in self.tracked


__all__ = [
    "APPLEDOUBLE_MAGIC",
    "APPLEDOUBLE_PREFIX",
    "SidecarFilter",
    "SidecarInspectionError",
    "git_control_present",
    "tracked_paths",
    "is_appledouble_sidecar",
    "is_appledouble_sidecar_path",
    "without_appledouble_sidecars",
]
