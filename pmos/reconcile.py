"""Read-only comparison of a workspace against the runtime's bound approvals.

F01: the artifact body and its authored frontmatter are file-owned; approvals,
the revisions they bind, and interview answers are runtime-owned. A workspace
edit made outside `pmos answer`/`pmos gate` never becomes part of the approved
record by itself; it becomes a pending proposal, visible here, until the
affected gate is proved again with `pmos gate`.

This module never writes to the Store or the workspace. It reads
pmos/artifacts.py's scan() and, through pmos/conductor.py's stale_gates(),
the same check_manifest()-backed comparison `pmos status` and `pmos gate`
already use, so reconcile can never disagree with them about what is stale.
It does not invent a second approval path: accepting a pending proposal still
happens by re-proving the gate with `pmos gate`, which each entry below
names.
"""
from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any

from .artifacts import scan
from .product import product_conductor
from .store import Store, ValidationError

SCHEMA = "pmos.reconcile.v1"


def _scan_conflict(exc: ValidationError) -> dict[str, Any]:
    """Classify a scan() failure into one of the conflict kinds reconcile names."""
    message = str(exc)
    if "is a symlink" in message:
        kind = "symlinked_artifact"
    elif "is not UTF-8 text" in message:
        kind = "unreadable_artifact"
    elif "carried by more than one file" in message:
        kind = "duplicate_id"
    else:
        kind = "workspace_scan_error"
    return {"kind": kind, "message": message}


def _diagnose_missing(root: Path, scanned: dict[str, Any], artifact_id: str, path: str) -> dict[str, Any]:
    """A manifest-bound id no longer found by scan(): the file is gone, or the
    same path now carries a different artifact_id."""
    candidate = root / path
    try:
        is_file = candidate.is_file() and not candidate.is_symlink()
    except OSError:
        is_file = False
    if not is_file:
        return {"kind": "missing_artifact", "id": artifact_id, "path": path,
                "message": "%s (%s) is bound by an approval but is no longer a file in the workspace"
                          % (artifact_id, path)}
    found_id = None
    for other_id, record in scanned.items():
        if record["path"] == path:
            found_id = other_id
            break
    if found_id:
        message = ("%s now carries artifact_id %s, not the bound id %s that approval recorded"
                   % (path, found_id, artifact_id))
    else:
        message = ("%s no longer carries an artifact block; the bound artifact_id %s is gone"
                   % (path, artifact_id))
    return {"kind": "artifact_id_changed", "bound_id": artifact_id, "current_id": found_id,
            "path": path, "message": message}


def _gate_command(root: Path, product_id: str, bank_id: str, token: str) -> str:
    return " ".join(["pmos", "gate", "--path", shlex.quote(str(root)), "--product-id", shlex.quote(product_id),
                     "--bank-id", shlex.quote(bank_id), "--evidence", "'<gate evidence json>'",
                     "--expected-revision", shlex.quote(token), "--turn-id", "'<new turn id>'"])


def reconcile_report(store: Store, root: Path, product_id: str) -> dict[str, Any]:
    """Compare the workspace to the runtime's bound approvals. Writes nothing.

    Returns {"schema", "read_only": True, "product_id", "revision_token",
    "pending", "conflicts", "message"}.

    "pending" lists every workspace artifact whose current body differs from
    the revision the latest approval bound for it, sorted by id, each as
    {"id", "path", "accepted_revision", "current_revision", "stales_gates",
    "reconcile_dependents", "next_action"}: "stales_gates" is every bank
    whose approval no longer verifies because of this artifact,
    "reconcile_dependents" is every other approved artifact that depends on
    it and so also needs reconciliation, and "next_action" is one {"bank_id",
    "command"} entry per staled bank, naming the `pmos gate` re-proof that
    accepts the edit.

    "conflicts" names, one entry per problem found: a bound artifact that is
    missing ("missing_artifact"), a bound id that now belongs to a different
    file ("artifact_id_changed"), two files sharing one id
    ("duplicate_id"), or a symlinked or unreadable artifact
    ("symlinked_artifact" / "unreadable_artifact"). scan() aborts on the
    first workspace-wide problem it finds (a duplicate id or a symlinked or
    unreadable file), so only one such conflict is reported per call; fixing
    it and reconciling again surfaces the next.
    """
    head = store.head(product_id)
    conflicts: list[dict[str, Any]] = []
    try:
        scanned = scan(root)
        scan_ok = True
    except ValidationError as exc:
        scanned = {}
        scan_ok = False
        conflicts.append(_scan_conflict(exc))

    pending: list[dict[str, Any]] = []
    if scan_ok:
        conductor = product_conductor(store, root, product_id)
        stale = conductor.stale_gates()
        by_id: dict[str, dict[str, Any]] = {}
        for entry in stale:
            bank_id = entry["bank_id"]
            for item in entry["changed"]:
                artifact_id = item["id"]
                if item["current"] is None:
                    conflicts.append(_diagnose_missing(root, scanned, artifact_id, item["path"]))
                    continue
                record = by_id.setdefault(artifact_id, {
                    "id": artifact_id, "path": item["path"],
                    "accepted_revision": item["reviewed"], "current_revision": item["current"],
                    "stales_gates": [], "reconcile_dependents": [],
                })
                if bank_id not in record["stales_gates"]:
                    record["stales_gates"].append(bank_id)
                for dependent in entry["reconcile"]:
                    if dependent not in record["reconcile_dependents"]:
                        record["reconcile_dependents"].append(dependent)
        for record in by_id.values():
            record["reconcile_dependents"].sort()
            record["next_action"] = [
                {"bank_id": bank_id, "command": _gate_command(root, product_id, bank_id, head.token)}
                for bank_id in record["stales_gates"]
            ]
        pending = sorted(by_id.values(), key=lambda r: r["id"])
        # The same missing/changed id can be named once per bank it stales
        # (a dependency bound in more than one manifest); report it once.
        seen: set[tuple[Any, ...]] = set()
        deduped: list[dict[str, Any]] = []
        for conflict in conflicts:
            key = (conflict.get("kind"), conflict.get("id"), conflict.get("path"), conflict.get("bound_id"))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(conflict)
        conflicts = deduped

    message = "reconcile is read-only; it changed no state"
    if not scan_ok:
        message += "; the workspace scan itself could not complete, see conflicts"
    return {
        "schema": SCHEMA,
        "read_only": True,
        "product_id": product_id,
        "revision_token": head.token,
        "pending": pending,
        "conflicts": conflicts,
        "message": message,
    }
