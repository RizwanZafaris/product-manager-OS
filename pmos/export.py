"""Build a portable, versioned export of a product's Conductor state.

F34: PMOSDomain's separate 16 MiB MAX_SNAPSHOT_BYTES envelope is documented in
docs/SCALE.md, which promised this slice's archive/export path for the
runtime a `pmos` command line actually drives -- the Conductor state
pmos/conductor.py bounds at the much smaller MAX_STATE_BYTES. This module
reads one product's interview answers, its recorded gate approvals (each
with the manifest it bound and its local attestation), and its stale gates,
and returns them as one JSON-serializable package.

It is read-only on the Store: nothing here commits a mutation. It is not an
import path -- reading a `pmos export` package back into a runtime is out of
scope for this slice, and the rendered index says so.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SCHEMA = "pmos.export.v1"


def build_export(conductor: Any, root: Any) -> dict[str, Any]:
    """The export package for one product, read from its Conductor only.

    conductor.state() and conductor.stale_gates() only read the Store's
    current snapshot; nothing here writes to it. root is accepted for
    parity with the other workspace-reading builders (pmos/handoff.py) and
    is not currently read directly: every fact here already comes through
    the Conductor's own state and gate manifests.
    """
    state = conductor.state()
    stale = conductor.stale_gates()
    head = conductor.store.head(conductor.product_id)

    banks: dict[str, Any] = {}
    for bank in conductor.banks:
        saved = state["banks"][bank.id]
        banks[bank.id] = {
            "version": saved["version"],
            "cursor": saved["cursor"],
            "answers": dict(saved["answers"]),
            "parked": list(saved["parked"]),
            "reopened": list(saved.get("reopened", [])),
        }

    approvals = []
    for bank in conductor.banks:
        record = state["gates"].get(bank.id)
        if record is None:
            continue
        approvals.append({
            "bank_id": bank.id,
            "attestation": record.get("attestation", "local"),
            "proof": dict(record["proof"]),
            "manifest": record.get("manifest"),
            "superseded": len(state.get("superseded_gates", {}).get(bank.id, [])),
        })

    return {
        "schema": SCHEMA,
        "product_id": conductor.product_id,
        "source_revision": head.token,
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "interview": {"current_bank": state["current_bank"], "banks": banks},
        "approvals": approvals,
        "stale_gates": stale,
        "note": ("This is an archive/export snapshot for portability, not an import path; "
                "reading it back into a runtime is out of scope for this slice."),
    }


def render_export_markdown(package: dict[str, Any]) -> str:
    """A short human index of the export package, like handoff's CONTEXT.md."""
    lines = ["# Product export", "",
             "Product: %s" % package["product_id"],
             "Source revision: %s" % package["source_revision"],
             "Exported at: %s" % package["exported_at"],
             "", "This is an archive/export snapshot, not an import path.",
             "Reading it back into a runtime is out of scope for this slice.",
             "", "## Approvals", ""]
    if package["approvals"]:
        for item in package["approvals"]:
            proof = item["proof"]
            detail = "approved by %s at %s; %s attestation" % (
                proof.get("actor_id"), proof.get("approved_at"), item["attestation"])
            if item["superseded"]:
                detail += "; %d superseded" % item["superseded"]
            lines.append("- %s: %s" % (item["bank_id"], detail))
    else:
        lines.append("- (none)")
    lines.extend(["", "## Stale gates", ""])
    if package["stale_gates"]:
        for entry in package["stale_gates"]:
            lines.append("- %s: %s" % (entry["bank_id"], entry["message"]))
    else:
        lines.append("- (none)")
    lines.extend(["", "## Interview", ""])
    banks = package["interview"]["banks"]
    for bank_id, saved in banks.items():
        lines.append("- %s: %d answered, %d parked" % (
            bank_id, len(saved["answers"]), len(saved["parked"])))
    lines.append("")
    return "\n".join(lines)
