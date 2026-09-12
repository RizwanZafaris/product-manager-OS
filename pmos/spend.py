"""Shared persistent spend ledger for Product Manager OS.

The ledger is OS state, not harness state. It records reservations made
before a billable call and settles them once the real cost is known, so that
two workers sharing a cap cannot both spend its last allowance and a crash
after dispatch never refunds an unknown charge.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Mapping, Optional, Sequence


class BudgetExceeded(Exception):
    """Raised when a reservation would breach a configured cap."""


class UnresolvedCharge(BudgetExceeded):
    """Raised when an unresolved (unknown) charge blocks a new reservation."""


_MAX_STR_LEN = 200


def default_path() -> Path:
    """Return the ledger path.

    Honours ``PMOS_SPEND_LEDGER`` when set and non-empty; otherwise uses a
    path under the user's cache directory. The returned path is never inside
    this repository.
    """
    env = os.environ.get("PMOS_SPEND_LEDGER")
    if env and env.strip():
        return Path(env)
    return Path.home() / ".cache" / "pmos" / "spend.sqlite"


def day_scope(now: Optional[_dt.datetime] = None) -> str:
    """Return the canonical daily scope string, for example ``day:2026-09-12``."""
    if now is None:
        now = _dt.datetime.now(_dt.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=_dt.timezone.utc)
    return "day:" + now.astimezone(_dt.timezone.utc).date().isoformat()


def _validate_amount(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError("%s must not be a bool" % name)
    if not isinstance(value, (int, float)):
        raise ValueError("%s must be a number" % name)
    converted = float(value)
    if math.isnan(converted) or math.isinf(converted):
        raise ValueError("%s must be finite" % name)
    if converted < 0:
        raise ValueError("%s must be nonnegative" % name)
    return converted


def _validate_text(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError("%s must be a string" % name)
    if not value:
        raise ValueError("%s must be non-empty" % name)
    if len(value) > _MAX_STR_LEN:
        raise ValueError("%s too long" % name)
    if "\x00" in value:
        raise ValueError("%s must not contain NUL" % name)
    return value


def _validate_scopes(limits: Mapping[str, object]) -> dict[str, float]:
    if not isinstance(limits, Mapping):
        raise ValueError("limits must be a mapping")
    if not limits:
        raise ValueError("limits must name at least one scope")
    result: dict[str, float] = {}
    for scope, cap in limits.items():
        scope_text = _validate_text(scope, "scope")
        result[scope_text] = _validate_amount(cap, "cap")
    return result


def _validate_external(
    external: Optional[Mapping[str, object]]
) -> dict[str, float]:
    if external is None:
        return {}
    if not isinstance(external, Mapping):
        raise ValueError("external must be a mapping")
    result: dict[str, float] = {}
    for scope, amount in external.items():
        scope_text = _validate_text(scope, "external scope")
        result[scope_text] = _validate_amount(amount, "external amount")
    return result


class SpendLedger:
    """A sqlite3-backed persistent spend ledger."""

    def __init__(self, path: str | os.PathLike[str]):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(
            str(self._path),
            isolation_level=None,
            timeout=30.0,
        )
        self._conn.execute("PRAGMA busy_timeout=30000")
        self._create_schema()

    def _create_schema(self) -> None:
        conn = self._conn
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS reservations ("
                "key TEXT PRIMARY KEY,"
                "reserved_usd REAL NOT NULL,"
                "charged_usd REAL,"
                "state TEXT NOT NULL CHECK (state IN ('open','settled','unknown')),"
                "created_at REAL NOT NULL,"
                "note TEXT NOT NULL DEFAULT ''"
                ")"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS reservation_scopes ("
                "key TEXT NOT NULL,"
                "scope TEXT NOT NULL,"
                "PRIMARY KEY (key, scope)"
                ")"
            )
            # Every reservation reads its scopes' rows; the primary key leads
            # with key, so without this each scope lookup scans the table.
            conn.execute(
                "CREATE INDEX IF NOT EXISTS reservation_scopes_by_scope "
                "ON reservation_scopes (scope)"
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SpendLedger":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def _execute(
        self,
        sql: str,
        params: Sequence[object] = (),
    ) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def _check_existing_key(self, key: str) -> None:
        row = self._execute(
            "SELECT 1 FROM reservations WHERE key = ?", (key,)
        ).fetchone()
        if row is not None:
            raise ValueError("reservation key already used: %s" % key)

    def _check_unresolved(self, scopes: Sequence[str]) -> None:
        # One join per scope: an IN list with a placeholder per reservation
        # would pass SQLite's host-parameter limit on a long-lived scope, and
        # the refusal names the scope the unknown charge actually shares.
        for scope in scopes:
            row = self._execute(
                "SELECT r.key FROM reservations AS r "
                "INNER JOIN reservation_scopes AS s ON s.key = r.key "
                "WHERE s.scope = ? AND r.state = 'unknown' "
                "ORDER BY r.created_at ASC LIMIT 1",
                (scope,),
            ).fetchone()
            if row is not None:
                raise UnresolvedCharge(
                    "unresolved charge %s blocks scope %s" % (row[0], scope)
                )

    def _committed_for_scope(self, scope: str) -> float:
        rows = self._execute(
            "SELECT r.key, r.state, r.reserved_usd, r.charged_usd "
            "FROM reservations AS r "
            "INNER JOIN reservation_scopes AS s ON s.key = r.key "
            "WHERE s.scope = ?",
            (scope,),
        ).fetchall()
        total = 0.0
        for _key, state, reserved_usd, charged_usd in rows:
            if state == "open":
                total += float(reserved_usd)
            else:
                total += float(charged_usd) if charged_usd is not None else 0.0
        return total

    def committed(self, scope: str) -> float:
        """Return the committed spend for a scope."""
        scope_text = _validate_text(scope, "scope")
        return self._committed_for_scope(scope_text)

    def unresolved(self) -> list[str]:
        """Return keys in the 'unknown' state, oldest first."""
        rows = self._execute(
            "SELECT key FROM reservations WHERE state = 'unknown' ORDER BY created_at ASC"
        ).fetchall()
        return [row[0] for row in rows]

    def reserve(
        self,
        key: str,
        max_usd: object,
        limits: Mapping[str, object],
        external: Optional[Mapping[str, object]] = None,
    ) -> None:
        """Reserve ``max_usd`` against the named scopes.

        Raises :class:`UnresolvedCharge` if any reservation sharing one of the
        scopes is in the 'unknown' state, or :class:`BudgetExceeded` if the
        committed spend plus ``max_usd`` plus any external spend would breach a
        cap. A refusal records nothing. A reused key raises ``ValueError``.
        """
        key_text = _validate_text(key, "key")
        amount = _validate_amount(max_usd, "max_usd")
        scopes = _validate_scopes(limits)
        external_spend = _validate_external(external)
        conn = self._conn
        conn.execute("BEGIN IMMEDIATE")
        try:
            self._check_existing_key(key_text)
            self._check_unresolved(list(scopes.keys()))
            for scope, cap in scopes.items():
                committed = self._committed_for_scope(scope)
                extra = external_spend.get(scope, 0.0)
                if committed + extra + amount > cap:
                    raise BudgetExceeded(
                        "scope %s cap %s exceeded: %s committed + %s external + %s "
                        "reserved"
                        % (scope, cap, committed, extra, amount)
                    )
            created_at = time.time()
            self._execute(
                "INSERT INTO reservations (key, reserved_usd, state, created_at) "
                "VALUES (?, ?, 'open', ?)",
                (key_text, amount, created_at),
            )
            for scope in scopes:
                self._execute(
                    "INSERT INTO reservation_scopes (key, scope) VALUES (?, ?)",
                    (key_text, scope),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _fetch_reservation(self, key: str) -> tuple[float, str, Optional[float], str]:
        row = self._execute(
            "SELECT reserved_usd, state, charged_usd, note FROM reservations WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            raise KeyError(key)
        return float(row[0]), str(row[1]), row[2], str(row[3])

    def settle(self, key: str, actual_usd: object) -> None:
        """Settle a reservation with a real cost.

        ``actual_usd`` ``None`` marks the reservation 'unknown' and charges the
        full reservation amount, never refunding it until :meth:`reconcile`.
        A finite nonnegative amount settles it, even above the reservation.
        """
        key_text = _validate_text(key, "key")
        if actual_usd is None:
            amount: Optional[float] = None
        else:
            amount = _validate_amount(actual_usd, "actual_usd")
        conn = self._conn
        conn.execute("BEGIN IMMEDIATE")
        try:
            reserved_usd, state, _charged_usd, _note = self._fetch_reservation(key_text)
            if state != "open":
                raise ValueError("reservation %s is not open" % key_text)
            if amount is None:
                self._execute(
                    "UPDATE reservations SET state = 'unknown', charged_usd = ?, "
                    "note = ? WHERE key = ?",
                    (reserved_usd, "cost unknown; pending reconciliation", key_text),
                )
            else:
                note = ""
                if amount > reserved_usd:
                    note = "charged above reservation"
                self._execute(
                    "UPDATE reservations SET state = 'settled', charged_usd = ?, "
                    "note = ? WHERE key = ?",
                    (amount, note, key_text),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def reconcile(
        self,
        key: str,
        actual_usd: object,
        evidence: Optional[str] = None,
    ) -> None:
        """Reconcile an 'unknown' reservation with a finite nonnegative cost.

        When ``evidence`` is given it is validated with the text rules and
        recorded in the note as ``reconciled: `` followed by the evidence.
        """
        key_text = _validate_text(key, "key")
        amount = _validate_amount(actual_usd, "actual_usd")
        if evidence is None:
            note = "reconciled after an unknown cost"
        else:
            note = "reconciled: " + _validate_text(evidence, "evidence")
        conn = self._conn
        conn.execute("BEGIN IMMEDIATE")
        try:
            _reserved_usd, state, _charged_usd, _note = self._fetch_reservation(key_text)
            if state != "unknown":
                raise ValueError("reservation %s is not unknown" % key_text)
            self._execute(
                "UPDATE reservations SET state = 'settled', charged_usd = ?, "
                "note = ? WHERE key = ?",
                (amount, note, key_text),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def reservations(self, state: Optional[str] = None) -> list[dict[str, object]]:
        """Return reservations, oldest first, optionally filtered by ``state``.

        Each entry is a dict with key, reserved_usd, charged_usd, state,
        created_at, note and a sorted list of scopes.
        """
        if state is not None and state not in ("open", "settled", "unknown"):
            raise ValueError("unknown reservation state: %s" % state)
        if state is None:
            rows = self._execute(
                "SELECT key, reserved_usd, charged_usd, state, created_at, note "
                "FROM reservations ORDER BY created_at ASC, key ASC"
            ).fetchall()
        else:
            rows = self._execute(
                "SELECT key, reserved_usd, charged_usd, state, created_at, note "
                "FROM reservations WHERE state = ? "
                "ORDER BY created_at ASC, key ASC",
                (state,),
            ).fetchall()
        result: list[dict[str, object]] = []
        for key, reserved_usd, charged_usd, row_state, created_at, note in rows:
            scopes = self._execute(
                "SELECT scope FROM reservation_scopes WHERE key = ? ORDER BY scope ASC",
                (key,),
            ).fetchall()
            result.append(
                {
                    "key": str(key),
                    "reserved_usd": float(reserved_usd),
                    "charged_usd": (
                        float(charged_usd) if charged_usd is not None else None
                    ),
                    "state": str(row_state),
                    "created_at": float(created_at),
                    "note": str(note),
                    "scopes": [str(row[0]) for row in scopes],
                }
            )
        return result


def _format_created(value: float) -> str:
    return _dt.datetime.fromtimestamp(
        value, _dt.timezone.utc
    ).isoformat()


def _print_reservation(prefix: str, entry: Mapping[str, object]) -> None:
    print(
        "%s %s reserved=%s scopes=%s created=%s"
        % (
            prefix,
            entry["key"],
            entry["reserved_usd"],
            ",".join(entry["scopes"]),
            _format_created(float(entry["created_at"])),
        )
    )


def _cmd_status(ledger: SpendLedger, path: Path, as_json: bool) -> int:
    unresolved = ledger.reservations("unknown")
    open_entries = ledger.reservations("open")
    if as_json:
        print(
            json.dumps(
                {
                    "path": str(path),
                    "unresolved": unresolved,
                    "open": open_entries,
                }
            )
        )
        return 0
    print("ledger: %s" % path)
    for entry in unresolved:
        _print_reservation("unknown", entry)
    for entry in open_entries:
        _print_reservation("open", entry)
    print("unresolved: %d" % len(unresolved))
    print("open: %d" % len(open_entries))
    return 0


def _cmd_reconcile(args: argparse.Namespace) -> int:
    path = Path(args.ledger)
    evidence = " ".join(args.evidence)
    if len(evidence) < 10:
        sys.stderr.write("evidence must be at least 10 characters\n")
        return 2
    if not path.exists():
        # Reconciling against a ledger that does not exist would create an
        # empty one and then fail on the missing key; refuse it plainly.
        sys.stderr.write("no ledger exists at %s\n" % path)
        return 2
    ledger: Optional[SpendLedger] = None
    try:
        # Parsed inside the try: a NaN, a negative or a non-number is an
        # operator error with exit status 2, never a traceback.
        amount = _validate_amount(float(args.usd), "usd")
        ledger = SpendLedger(path)
        ledger.reconcile(args.key, amount, evidence)
    except (ValueError, KeyError) as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    finally:
        if ledger is not None:
            ledger.close()
    print("reconciled %s %s" % (args.key, amount))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the operator command line and return an exit status."""
    parser = argparse.ArgumentParser(
        prog="pmos.spend",
        description="Inspect and reconcile the shared spend ledger.",
    )
    parser.add_argument(
        "--ledger",
        default=str(default_path()),
        help="path to the spend ledger (default: %(default)s)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    status_parser = subparsers.add_parser(
        "status", help="show unresolved and open reservations"
    )
    status_parser.add_argument(
        "--json", action="store_true", help="print one JSON object"
    )
    reconcile_parser = subparsers.add_parser(
        "reconcile", help="reconcile an unknown reservation with evidence"
    )
    reconcile_parser.add_argument("key", help="reservation key")
    reconcile_parser.add_argument("usd", help="actual cost in USD")
    reconcile_parser.add_argument(
        "evidence", nargs="+", help="evidence words for the reconciliation"
    )
    args = parser.parse_args(argv)
    path = Path(args.ledger)
    if args.command == "status":
        if not path.exists():
            print("no ledger exists at %s" % path)
            return 0
        ledger = SpendLedger(path)
        try:
            return _cmd_status(ledger, path, args.json)
        finally:
            ledger.close()
    return _cmd_reconcile(args)


if __name__ == '__main__':
    sys.exit(main())
