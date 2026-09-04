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
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_TREE_ENTRIES = 16384
MAX_TREE_DEPTH = 64
MAX_TREE_BYTES = 256 * 1024 * 1024


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
    rows = []
    entries = 0
    total_bytes = 0
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                      getattr(os, "O_NOFOLLOW", 0))
    root_identity = os.fstat(root_fd)
    try:
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
                if stat.S_ISDIR(metadata.st_mode):
                    if ((at_root and (name in ROOT_SKIP_DIRS or name.endswith(".egg-info"))) or
                            (not at_root and name in NESTED_CACHE_DIRS)):
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
                if (relative == ATTESTATION.as_posix() or name in SKIP_NAMES or
                        name.endswith((".pyc", ".pyo"))):
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
    """
    import subprocess
    try:
        done = subprocess.run(
            ["git", "log", "--format=%an%n%ae", "-%d" % int(limit)],
            cwd=str(root), capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return set()
    if done.returncode != 0:
        return set()
    return {line.strip().lower() for line in done.stdout.splitlines()
            if line.strip()}


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
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
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
        document = json.loads(path.read_text(encoding="utf-8"))
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
