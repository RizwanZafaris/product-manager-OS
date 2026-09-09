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

``tools/review_gate.py`` keeps its own tracked-aware rule and does not import
this module, because its exclusion additionally has to stay safe for a
tracked file that happens to be named like a sidecar without necessarily
carrying the AppleDouble magic (a name-only ``is_excluded_sidecar`` check
guarded by tracked-ness). Its docstrings at lines ~100-200 and ~320 explain
why that check is name-only and tracked-aware rather than magic-byte-based.
Both copies apply to disjoint problems -- reproducible review digests here,
loader crashes and mis-listings everywhere else -- and a test in
``test_pmos_invariants.py`` pins that the two never disagree about a name
that both could apply to.
"""

from __future__ import annotations

import stat
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


__all__ = [
    "APPLEDOUBLE_MAGIC",
    "APPLEDOUBLE_PREFIX",
    "is_appledouble_sidecar",
    "is_appledouble_sidecar_path",
    "without_appledouble_sidecars",
]
