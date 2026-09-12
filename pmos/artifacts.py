"""The runtime's reader for the artifact contract W3 stamps on working copies.

The wheel ships pmos/ but not tools/, so the runtime needs its own copy of the
frontmatter contract tools/workspace.py defines. The functions copied here
(parse_artifact, _parse_artifact_value, artifact_revision, not_an_artifact) and
the regular expressions and constants they use mirror that module exactly, so a
later task can make tools/workspace.py import them. scan, build_manifest and
check_manifest read a workspace tree without writing it.
"""
from __future__ import annotations

import hashlib
import json
import os
import re

from .store import ValidationError

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)

ARTIFACT_PHASES = ("DISCOVER", "DEFINE", "DESIGN", "BUILD", "DELIVER",
                   "OPERATE", "PLANNING", "AI OVERLAY", "ALL STAGES")
ARTIFACT_STATUSES = ("draft", "in-review", "approved", "superseded")
ARTIFACT_KEYS = ("artifact_id", "phase", "gate", "status", "depends_on",
                 "template")

ARTIFACT_FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$")


def parse_artifact(text):
    """The artifact frontmatter as a dict, or None when there is no artifact.

    Reads only the six ARTIFACT_KEYS, from lines of the form key: value.
    depends_on is a JSON array of strings, gate is an integer or null, and the
    others are plain strings. A value that does not parse is kept as its raw
    string, so a checker can report it rather than crash.
    """
    match = FRONTMATTER_RE.match(text or "")
    if not match:
        return None
    body = match.group(1)
    fields = {}
    for line in body.split("\n"):
        line = line.rstrip("\r")
        field = ARTIFACT_FIELD_RE.match(line)
        if not field:
            continue
        key, raw = field.group(1), field.group(2)
        if key not in ARTIFACT_KEYS:
            continue
        if key not in fields:
            fields[key] = _parse_artifact_value(key, raw)
    if "artifact_id" not in fields:
        return None
    return fields


def _parse_artifact_value(key, raw):
    if key == "depends_on":
        try:
            value = json.loads(raw)
        except (ValueError, TypeError):
            return raw
        if isinstance(value, list) and all(isinstance(item, str)
                                          for item in value):
            return value
        return raw
    if key == "gate":
        if raw == "null":
            return None
        try:
            return int(raw)
        except ValueError:
            return raw
    return raw


def not_an_artifact(inside):
    """True for a workspace file that never carries the artifact block.

    inside is the file's path relative to the workspace, in posix form. The
    root README.md and STATE.md, anything under gates/, the run log the runner
    writes beside a copy, and a report route's findings are records of the
    work rather than artifacts of it, so --stamp leaves them alone and the
    workspace gate does not ask them for the block.
    """
    return (inside in ("README.md", "STATE.md") or inside.startswith("gates/")
            or inside.endswith(".run-log.md") or inside.endswith("-report.md"))


def artifact_revision(text):
    """The sha256 hex digest of the body after the frontmatter block."""
    match = FRONTMATTER_RE.match(text or "")
    body = text[match.end():] if match else (text or "")
    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _relative_posix(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def scan(root):
    """Every artifact under root, as a dict from artifact_id to its record.

    Walks every *.md file under root in sorted order. .pmos/ at the root is not
    entered, and any path whose posix form relative to root is a record file
    (not_an_artifact) is skipped. A symlinked file is refused, as the gate
    verifier refuses one, and os.walk does not enter a symlinked directory.
    Files are read as UTF-8; one that does not decode is a ValidationError
    naming its relative path. The value for each artifact_id is {"path",
    "revision", "gate", "phase", "status", "depends_on"}: path is the posix
    form relative to root, revision is artifact_revision(text), gate is the
    parsed gate, phase and status are the parsed block's values when they are
    strings, else None, and depends_on is the parsed list when it is a list of
    strings, else []. Two files carrying the same artifact_id are a
    ValidationError naming the id and both paths.
    """
    found = {}
    for dirpath, dirnames, filenames in os.walk(root):
        if _relative_posix(dirpath, root) == ".":
            dirnames[:] = [name for name in dirnames if name != ".pmos"]
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = _relative_posix(full, root)
            if not_an_artifact(rel):
                continue
            if os.path.islink(full):
                # An approval must bind a file that lives in the workspace.
                raise ValidationError("%s is a symlink; an artifact must be a regular file in the "
                                      "workspace" % rel)
            try:
                with open(full, encoding="utf-8") as handle:
                    text = handle.read()
            except UnicodeDecodeError as exc:
                raise ValidationError("%s is not UTF-8 text" % rel) from exc
            parsed = parse_artifact(text)
            if not isinstance(parsed, dict) or not isinstance(parsed.get("artifact_id"), str):
                continue
            artifact_id = parsed["artifact_id"]
            depends_on = parsed.get("depends_on")
            if not (isinstance(depends_on, list)
                    and all(isinstance(item, str) for item in depends_on)):
                depends_on = []
            if artifact_id in found:
                raise ValidationError("artifact_id %s is carried by more than one file: %s and %s"
                                      % (artifact_id, found[artifact_id]["path"], rel))
            phase = parsed.get("phase")
            status = parsed.get("status")
            found[artifact_id] = {
                "path": rel,
                "revision": artifact_revision(text),
                "gate": parsed.get("gate"),
                "phase": phase if isinstance(phase, str) else None,
                "status": status if isinstance(status, str) else None,
                "depends_on": list(depends_on),
            }
    return found


def _entry(artifact_id, record):
    return {
        "id": artifact_id,
        "path": record["path"],
        "revision": record["revision"],
        "depends_on": list(record["depends_on"]),
    }


def build_manifest(root, gate):
    """The manifest for one gate: its artifacts and the dependencies they pull.

    From scan(root), the artifacts are the entries whose gate equals gate, each
    as {"id", "path", "revision", "depends_on"}, sorted by id. The dependencies
    are every id reachable through depends_on from those artifacts that is not
    itself one of them, in the same shape, sorted by id. An id that is reached
    but not in the scan is a ValidationError whose message is "<id> depends on
    <missing id> and the workspace does not have it yet", where <id> is the
    artifact that declares the missing one. A cycle ends the walk rather than
    looping. Returns {"artifacts": [...], "dependencies": [...]}; both lists are
    empty when no artifact names the gate.
    """
    found = scan(root)
    artifact_ids = sorted(aid for aid, record in found.items()
                          if record["gate"] == gate)
    artifact_set = set(artifact_ids)
    artifact_entries = [_entry(aid, found[aid]) for aid in artifact_ids]
    dependency_ids = set()
    for aid in artifact_ids:
        # Each step keeps the id that named the dependency, so a missing one is
        # reported against the file that declares it.
        stack = [(dep, aid) for dep in found[aid]["depends_on"]]
        visited = set()
        while stack:
            dep, parent = stack.pop()
            if dep in visited:
                continue
            visited.add(dep)
            if dep in artifact_set:
                continue
            if dep not in found:
                raise ValidationError(
                    "%s depends on %s and the workspace does not have it yet"
                    % (parent, dep))
            dependency_ids.add(dep)
            stack.extend((sub, dep) for sub in found[dep]["depends_on"]
                         if sub not in visited)
    dependency_entries = [_entry(did, found[did]) for did in sorted(dependency_ids)]
    return {"artifacts": artifact_entries, "dependencies": dependency_entries}


def check_manifest(root, manifest):
    """Compare a manifest to the workspace it was built from.

    Scans root again and returns {"changed": [...], "reconcile": [...]}. changed
    lists, sorted by id, every manifest entry (artifact or dependency) whose id
    is no longer in the scan or whose revision differs, as {"id", "path",
    "reviewed": the manifest's revision, "current": the current revision, or
    None when the id is gone}. reconcile lists, sorted, the ids of manifest
    artifacts that are not changed themselves but reach a changed id through
    the depends_on recorded in the manifest. A scan error is raised, never
    swallowed.
    """
    found = scan(root)
    by_id = {}
    for section in ("artifacts", "dependencies"):
        for entry in manifest.get(section, []):
            by_id[entry["id"]] = entry
    changed = []
    changed_ids = set()
    for aid, entry in sorted(by_id.items()):
        if aid not in found:
            changed.append({
                "id": aid,
                "path": entry["path"],
                "reviewed": entry["revision"],
                "current": None,
            })
            changed_ids.add(aid)
        elif found[aid]["revision"] != entry["revision"]:
            changed.append({
                "id": aid,
                "path": found[aid]["path"],
                "reviewed": entry["revision"],
                "current": found[aid]["revision"],
            })
            changed_ids.add(aid)
    reconcile = set()
    for entry in manifest.get("artifacts", []):
        aid = entry["id"]
        if aid in changed_ids:
            continue
        stack = list(entry["depends_on"])
        visited = set()
        while stack:
            dep = stack.pop()
            if dep in visited:
                continue
            visited.add(dep)
            if dep in changed_ids:
                reconcile.add(aid)
                break
            dep_entry = by_id.get(dep)
            if dep_entry is not None:
                stack.extend(sub for sub in dep_entry["depends_on"] if sub not in visited)
    return {"changed": changed, "reconcile": sorted(reconcile)}
