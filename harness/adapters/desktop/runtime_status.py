#!/usr/bin/env python3
"""A read only MCP tool reporting one product's runtime phase status.

Standard library plus the repository's own pmos package, imported from the
repository root by path the way harness/runner.py does it, so this module
works under tools/ci_gate.py's minimal environment (no PYTHONPATH to the repo
root there). It imports no MCP SDK: server.py is the only place that talks to
the SDK, and this module has to be importable, and callable, with or without
it installed.

status() answers the same question `pmos status --json` answers about a
product's phase report, and nothing more: it opens the product's Store the
way pmos status does, builds the Conductor for that product, and asks
pmos.phases.phase_report for its phases. It never creates a product, never
migrates a workspace, and never writes to the Store; reading the runtime
database does apply its own schema migrations if the database predates them,
exactly as opening it for `pmos status` already does, because that happens
inside Store itself and not because this module asks for it.

On a missing runtime, an unknown product, or a bad argument, status() returns
{"ok": false, "error": <message>} and never raises. It always closes the
Store it opens, on every path through the function.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

# harness/adapters/desktop/runtime_status.py, so the repository root is three
# directories up. Inserted ahead of anything already on sys.path so a repo
# checked out somewhere that also has a "pmos" importable elsewhere still
# resolves to this tree's own package.
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pmos.cli import _paths  # noqa: E402
from pmos.phases import phase_report  # noqa: E402
from pmos.product import pinned_contract, product_conductor  # noqa: E402
from pmos.store import NotFoundError, Store, StoreError, ValidationError  # noqa: E402

TOOL = {
    "name": "pmos_status",
    "description": (
        "Reads one product's runtime phase status: for every question bank, "
        "its phase state, what outcomes are met and what is missing, the one "
        "next action, who must approve its gate, and the documents that gate "
        "names. It opens the PM OS runtime read only, the same way `pmos "
        "status` does, and never creates a product, never migrates a "
        "workspace, and never writes anything to the runtime. It runs no "
        "model call, sends nothing, and signs no gate."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": ("The workspace folder where PM OS is "
                                 "initialized, the same --path a pmos CLI "
                                 "command takes."),
            },
            "product_id": {
                "type": "string",
                "description": ("The product whose phase status to read, "
                                 "the same --product-id a pmos CLI command "
                                 "takes."),
            },
        },
        "required": ["path", "product_id"],
        "additionalProperties": False,
    },
}


def _validated_arguments(arguments: Any) -> tuple[str, str]:
    """path and product_id from arguments, or a ValidationError naming why not."""
    if not isinstance(arguments, dict):
        raise ValidationError("arguments must be a JSON object")
    extra = sorted(set(arguments) - {"path", "product_id"})
    if extra:
        raise ValidationError("arguments carry unknown field(s): %s" % ", ".join(extra))
    path = arguments.get("path")
    product_id = arguments.get("product_id")
    if not isinstance(path, str) or not path.strip():
        raise ValidationError("path must be a non-empty string")
    if not isinstance(product_id, str) or not product_id.strip():
        raise ValidationError("product_id must be a non-empty string")
    return path, product_id


def status(arguments: dict) -> dict[str, Any]:
    """{"ok": true, "product_id", "revision_token", "phases"} for one product.

    Mirrors the phases half of `pmos status --json`: the same missing-runtime
    error when the workspace has never been initialized, the same Store and
    Conductor construction, and the same fallback to an empty phases list
    plus a phases_error string when building the Conductor from the pinned
    contract, or phase_report itself, raises ValidationError (a malformed
    pinned contract, or, for example, a symlinked artifact under the
    workspace).

    A missing runtime, an unknown product_id, or a malformed arguments value
    all come back as {"ok": false, "error": <message>}; this function never
    raises. The Store it opens is always closed before it returns, on every
    path, success or failure.
    """
    store: Store | None = None
    try:
        path, product_id = _validated_arguments(arguments)
        root, database = _paths(path)
        if not database.exists():
            raise ValidationError(
                "PM OS is not initialized at %s; run `pmos init --path %s`" % (root, root))
        store = Store(database)
        head = store.head(product_id)
        phases_error = None
        try:
            conductor = product_conductor(store, root, product_id)
            phases = phase_report(conductor, pinned_contract(store, product_id), root)
        except ValidationError as exc:
            phases = []
            phases_error = str(exc)
        result: dict[str, Any] = {"ok": True, "product_id": product_id,
                                   "revision_token": head.token, "phases": phases}
        if phases_error is not None:
            result["phases_error"] = phases_error
        return result
    except (OSError, sqlite3.DatabaseError, StoreError, ValueError, RuntimeError) as exc:
        return {"ok": False, "error": str(exc)}
    finally:
        if store is not None:
            store.close()


# NotFoundError is re-exported for callers that want to recognize the
# "unknown product" case by type rather than by message text.
__all__ = ["TOOL", "status", "NotFoundError"]
