"""The small, dependency-free Product Manager OS command line interface."""

from __future__ import annotations

import argparse
import json
import shlex
import sqlite3
import stat
import sys
from pathlib import Path
from typing import Any, Sequence

from .banks import CONTRACT_PATH, LEGACY_ONBOARDING, parse_contract, shipped_banks
from .conductor import TurnOutcome
from .migrations import migrate_workspace, recover_workspace, rollback_workspace
from .product import PIN_PATH, local_gate_verifier, pinned_contract, product_banks, product_conductor, source_resolver
from .release import build_provenance, verify_provenance
from .store import NotFoundError, Store, StoreError, ValidationError

# The old private names stay for existing callers.
_pinned_contract = pinned_contract
_product_banks = product_banks
_product_conductor = product_conductor
_local_gate_verifier = local_gate_verifier
_cli_source_resolver = source_resolver


def _emit(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, sort_keys=True, ensure_ascii=False))
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list, tuple)):
                print("%s: %s" % (key, json.dumps(item, sort_keys=True, ensure_ascii=False)))
            else:
                print("%s: %s" % (key, item))
    else:
        print(value)


def _error(exc: Exception, as_json: bool) -> int:
    value = {"ok": False, "error": str(exc),
             "hint": "Check the path, run `pmos status`, or use `pmos init --help`."}
    _emit(value, as_json)
    return 2


def _outcome_dict(outcome: TurnOutcome) -> dict[str, Any]:
    """Serialize a conductor outcome without treating model/customer claims as facts."""
    question = None
    if outcome.question is not None:
        question = {"id": outcome.question.id, "prompt": outcome.question.prompt,
                    "evidence_class": outcome.question.required_evidence.value}
    return {"status": outcome.status, "revision": outcome.revision,
            "bank_id": outcome.bank_id, "question": question,
            "message": outcome.message, "challenge_count": outcome.challenge_count,
            "accepted": outcome.accepted, "completed": outcome.completed,
            "conflict_revision": outcome.conflict_revision}


def _paths(path: str | Path) -> tuple[Path, Path]:
    root = Path(path).expanduser().resolve()
    runtime_dir = root / ".pmos"
    try:
        metadata = runtime_dir.lstat()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise ValidationError("cannot inspect the PM OS runtime directory") from exc
    else:
        if stat.S_ISLNK(metadata.st_mode):
            raise ValidationError("PM OS runtime directory must not be a symlink")
        if not stat.S_ISDIR(metadata.st_mode):
            raise ValidationError("PM OS runtime path is not a directory")
    database = runtime_dir / "runtime.sqlite"
    try:
        metadata = database.lstat()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise ValidationError("cannot inspect the PM OS runtime database") from exc
    else:
        if stat.S_ISLNK(metadata.st_mode):
            raise ValidationError("PM OS runtime database must not be a symlink")
        if not stat.S_ISREG(metadata.st_mode):
            raise ValidationError("PM OS runtime database must be a regular file")
    return root, database


def _run_new_user(root: Path, product_id: str) -> dict[str, Any]:
    _root, database = _paths(root)
    # The shipped contract is read and checked before the product exists, so a
    # broken install fails init without leaving a product that has no pin.
    raw = CONTRACT_PATH.read_bytes()
    parse_contract(raw)
    with Store(database) as store:
        head = store.create_product(product_id)
        published = store.commit(product_id, {PIN_PATH: raw}, expected_revision=head,
                                 metadata={"reason": "pin the question bank contract"})
        if not published.committed:
            raise StoreError("could not pin the question bank contract")
        conductor = _product_conductor(store, root, product_id)
        pending = conductor.next_turn(expected_revision=published.head)
        if pending.status != "question" or pending.question is None:
            raise StoreError("onboarding did not produce a deterministic first question")
        verified = store.verify()
        if not verified.ok:
            raise StoreError("runtime verification failed: " + "; ".join(verified.errors))
        return {"ok": True, "status": "initialized", "product_id": product_id,
                "root": str(root), "database": str(database),
                "onboarding": {"status": pending.status, "revision": pending.revision,
                                "question": pending.question.prompt,
                                "question_id": pending.question.id,
                                "evidence_class": pending.question.required_evidence.value,
                                "next": "submit a real answer with `pmos answer`"},
                "verification": {"ok": verified.ok, "errors": list(verified.errors)}}


def _init(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.path).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    root, database = _paths(root)
    database.parent.mkdir(parents=True, exist_ok=True)
    # Re-check after creation so a pre-existing unsafe path never becomes a
    # runtime write target. The migration commands enforce the same boundary
    # through their descriptor-relative destination lock.
    root, database = _paths(root)
    product_id = args.product_id or root.name + "-product"
    if database.exists():
        try:
            with Store(database) as store:
                store.head(product_id)
            raise ValidationError("runtime already contains product %r; use status or choose --product-id" % product_id)
        except NotFoundError:
            pass
    return _run_new_user(root, product_id)


def _status(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("PM OS is not initialized at %s; run `pmos init --path %s`" % (root, root))
    with Store(database) as store:
        product_id = args.product_id
        if not product_id:
            # Store intentionally keeps its durable public surface small; the
            # CLI's read-only status selector may inspect the product index to
            # choose the sole/first product deterministically.
            row = store._conn.execute("SELECT product_id FROM products ORDER BY product_id LIMIT 1").fetchone()
            product_id = str(row[0]) if row else None
        if not product_id:
            raise ValidationError("runtime contains no product; run `pmos init --product-id <id>`")
        head = store.head(product_id)
        report = store.verify()
        snapshot = store.read_snapshot(product_id)
        result = {"ok": report.ok, "status": "ready" if report.ok else "corrupt",
                  "root": str(root), "database": str(database), "product_id": product_id,
                  "revision": head.revision, "commit_hash": head.commit_hash,
                  # The exact value to pass as --expected-revision: composing
                  # <revision>:<commit_hash> by hand gives 0:None at revision 0.
                  "revision_token": head.token,
                  "file_count": len(snapshot.files), "errors": list(report.errors)}
        if report.ok:
            try:
                result.update(_interview_status(store, root, product_id, head.token))
            except (ValidationError, StoreError) as exc:
                result["interview_error"] = str(exc)
        return result


def _interview_status(store: Store, root: Path, product_id: str, token: str) -> dict[str, Any]:
    """Where the interview stands and the one next safe command, so status alone lets a user resume.

    Position and staleness come from the Conductor itself (next_turn re-checks every gate proof), so status can
    never disagree with what answer, reopen and gate would do. Commands are shell-quoted and carry the current
    revision token; only the answer, reason, evidence and turn id are left as placeholders.
    """
    banks = _product_banks(store, product_id)
    conductor = _product_conductor(store, root, product_id)
    position = conductor.next_turn()
    state = conductor.state()

    def command(name: str, *parts: str) -> str:
        return " ".join(["pmos", name, "--path", shlex.quote(str(root)), "--product-id", shlex.quote(product_id),
                         *parts, "--expected-revision", shlex.quote(token), "--turn-id", "'<new turn id>'"])

    parked, verified, unverified = [], 0, 0
    for bank in banks:
        bank_state = state["banks"].get(bank.id, {})
        for question_id in bank_state.get("parked", []):
            parked.append({"bank_id": bank.id, "question_id": question_id,
                           "reopen": command("reopen", "--question-id", shlex.quote(question_id),
                                             "--reason", "'<why you are reopening it>'")})
        for record in bank_state.get("answers", {}).values():
            if record.get("parked"):
                continue
            # An answer stored before evidence verification carries no label: it was never checked.
            if record.get("verification") == "source_verified":
                verified += 1
            else:
                unverified += 1
    stale_banks: list[dict[str, Any]] = []
    if position.status == "stale":
        stale_gates = conductor.stale_gates()
        if stale_gates and stale_gates[0]["bank_id"] == position.bank_id:
            for entry in stale_gates:
                bank_id = entry["bank_id"]
                stale_banks.append({
                    "bank_id": bank_id,
                    "message": entry["message"],
                    "changed": entry["changed"],
                    "reconcile": entry["reconcile"],
                    "gate": command("gate", "--bank-id", shlex.quote(bank_id),
                                    "--evidence", "'<gate evidence json>'"),
                })
        else:
            stale_banks.append({"bank_id": position.bank_id, "message": position.message,
                                "changed": [], "reconcile": [],
                                "gate": command("gate", "--bank-id", shlex.quote(position.bank_id),
                                                "--evidence", "'<gate evidence json>'")})
    question = None
    if position.question is not None:
        question = {"id": position.question.id, "prompt": position.question.prompt,
                    "evidence_class": position.question.required_evidence.value}
    if stale_banks:
        next_command = stale_banks[0]["gate"]
    elif position.status == "question" and question is not None:
        next_command = command("answer", "--question-id", shlex.quote(question["id"]),
                               "--answer", "'<your answer>'", "--evidence", "'<evidence json>'")
    elif parked:
        next_command = parked[0]["reopen"]
    elif position.status == "blocked" and position.bank_id:
        next_command = command("gate", "--bank-id", shlex.quote(position.bank_id),
                               "--evidence", "'<gate evidence json>'")
    else:
        next_command = None
    pinned = {bank.id: bank.version for bank in banks}
    try:
        shipped: dict[str, str] | None = {bank.id: bank.version for bank in shipped_banks()}
    except ValidationError:
        shipped = None
    current = pinned == shipped
    # _product_banks returns LEGACY_ONBOARDING itself only when the product has no pin.
    if banks is LEGACY_ONBOARDING:
        message = "This product started before the question bank contract and keeps the one-question onboarding bank."
    elif not current:
        message = ("This product keeps the question banks it started with; the shipped contract differs, "
                   "and moving a product to it is not supported yet.")
    else:
        message = "This product runs the shipped question banks."
    approvals: list[dict[str, Any]] = []
    for bank in banks:
        if bank.id not in state["gates"]:
            continue
        record = state["gates"][bank.id]
        proof = record.get("proof", {})
        manifest = record.get("manifest")
        if manifest is None:
            artifacts = None
            dependencies = None
        else:
            artifacts = [item["id"] for item in manifest.get("artifacts", [])]
            dependencies = [item["id"] for item in manifest.get("dependencies", [])]
        superseded = len(state.get("superseded_gates", {}).get(bank.id, []))
        approvals.append({
            "bank_id": bank.id,
            "attestation": record.get("attestation", "local"),
            "actor_id": proof.get("actor_id"),
            "approved_at": proof.get("approved_at"),
            "artifacts": artifacts,
            "dependencies": dependencies,
            "superseded": superseded,
        })
    rejections: list[dict[str, Any]] = []
    for bank in banks:
        # The Conductor validates a rejection record on load: it always has its proof, manifest and rejected_at.
        for record in state.get("gate_rejections", {}).get(bank.id, []):
            rejections.append({
                "bank_id": bank.id,
                "actor_id": record["proof"]["actor_id"],
                "rejected_at": record["rejected_at"],
                "artifacts": [item["id"] for item in record["manifest"]["artifacts"]],
            })
    return {"interview": position.status, "interview_message": position.message,
            "current_bank_id": position.bank_id, "question": question,
            "parked": parked, "stale_banks": stale_banks,
            "source_verified": verified, "supplied_unverified": unverified,
            "next": next_command,
            "approvals": approvals,
            "rejections": rejections,
            "question_banks": {"pinned": pinned, "shipped": shipped,
                               "current": current, "message": message}}


def _verify(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("runtime is missing at %s; run `pmos init --path %s`" % (database, root))
    with Store(database) as store:
        report = store.verify()
        result = {"ok": report.ok, "database": str(database), "errors": list(report.errors)}
    if args.provenance:
        provenance = verify_provenance(root, args.provenance)
        result["provenance"] = {"ok": provenance.ok, "errors": list(provenance.errors)}
        result["ok"] = result["ok"] and provenance.ok
        result["errors"].extend(provenance.errors)
    return result


def _evidence(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValidationError("--evidence must be valid JSON object") from exc
    if not isinstance(value, dict):
        raise ValidationError("--evidence must be a JSON object")
    return value


def _answer(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("runtime is missing; run `pmos init --path %s`" % root)
    with Store(database) as store:
        conductor = _product_conductor(store, root, args.product_id)
        outcome = conductor.submit_answer(args.question_id, args.answer, _evidence(args.evidence),
                                          expected_revision=args.expected_revision, turn_id=args.turn_id)
        result = {"ok": outcome.accepted, "product_id": args.product_id,
                  "outcome": _outcome_dict(outcome)}
        if not outcome.accepted:
            result["error"] = "answer was not accepted; supply the requested evidence and current revision"
        return result


def _reopen(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("runtime is missing; run `pmos init --path %s`" % root)
    with Store(database) as store:
        conductor = _product_conductor(store, root, args.product_id)
        outcome = conductor.reopen(args.question_id, expected_revision=args.expected_revision,
                                    turn_id=args.turn_id, reason=args.reason)
        result = {"ok": outcome.status == "reopened", "product_id": args.product_id,
                  "outcome": _outcome_dict(outcome)}
        if not result["ok"]:
            result["error"] = "reopen was not accepted; provide the current revision and a new turn id"
        return result


def _gate(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("runtime is missing; run `pmos init --path %s`" % root)
    with Store(database) as store:
        conductor = _product_conductor(store, root, args.product_id)
        outcome = conductor.prove_gate(args.bank_id, _evidence(args.evidence),
                                       expected_revision=args.expected_revision, turn_id=args.turn_id)
        return _gate_result(outcome, args.product_id)


def _gate_result(outcome: TurnOutcome, product_id: str) -> dict[str, Any]:
    # A gate that moves the interview to the next bank is a success even though the interview is not complete.
    ok = outcome.status in ("advanced", "completed")
    result = {"ok": ok, "product_id": product_id, "outcome": _outcome_dict(outcome)}
    if outcome.status == "stale":
        # A re-proof can be recorded while another approval is still stale:
        # name it, and never report completion.
        result["error"] = outcome.message
    elif outcome.status == "rejected":
        result["rejection_recorded"] = True
        result["error"] = outcome.message
    elif not ok:
        if outcome.message:
            result["error"] = "gate proof was not accepted: " + outcome.message
        else:
            result["error"] = "gate proof was not accepted; provide a real source and current revision"
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pmos", description="Product Manager OS local runtime")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit machine-readable JSON")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("init", "initialize a deterministic local PM OS"),
                            ("new-user", "run the deterministic new-user onboarding flow"),
                            ("status", "show runtime health and current head"),
                            ("verify", "verify runtime integrity and optional provenance")):
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("--path", default=".", help="workspace root (default: current directory)")
        sub.add_argument("--json", action="store_true", dest="json_command")
        if name in {"init", "new-user", "status"}:
            sub.add_argument("--product-id", help="stable product identifier")
        if name == "status":
            # Product selection is optional; without it status selects the
            # only/first product deterministically.
            pass
        if name in {"init", "new-user"}:
            sub.add_argument("--force", action="store_true",
                             help="accepted for compatibility; an existing product is always refused")
        if name == "verify":
            sub.add_argument("--provenance", help="provenance manifest to verify")
    for name, help_text in (("answer", "submit a caller-supplied answer and evidence"),
                            ("reopen", "reopen a parked question so it can be answered with fresh evidence"),
                            ("gate", "submit caller-supplied gate proof")):
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("--path", default=".")
        sub.add_argument("--product-id", required=True)
        sub.add_argument("--expected-revision", required=True,
                         help="head token returned by init/status/previous outcome")
        sub.add_argument("--turn-id", required=True, help="unique idempotency key for this submission")
        if name != "reopen":
            sub.add_argument("--evidence", required=True, help="JSON object containing caller-supplied evidence")
        sub.add_argument("--json", action="store_true", dest="json_command")
        if name == "answer":
            sub.add_argument("--question-id", required=True)
            sub.add_argument("--answer", required=True)
        elif name == "reopen":
            sub.add_argument("--question-id", required=True)
            sub.add_argument("--reason", required=True)
        else:
            sub.add_argument("--bank-id", required=True)
    migrate = commands.add_parser("migrate", help="migrate a legacy workspace with a dry-run option")
    migrate.add_argument("source")
    migrate.add_argument("--destination")
    migrate.add_argument("--product-id")
    migrate.add_argument("--dry-run", action="store_true")
    migrate.add_argument("--json", action="store_true", dest="json_command")
    rollback = commands.add_parser("rollback", help="restore the last migration backup")
    rollback.add_argument("destination", nargs="?", default=".")
    rollback.add_argument("--json", action="store_true", dest="json_command")
    recover = commands.add_parser("recover", help="recover a migration interrupted during activation")
    recover.add_argument("destination", nargs="?", default=".")
    recover.add_argument("--json", action="store_true", dest="json_command")
    release = commands.add_parser("provenance", help="write a release provenance manifest")
    release.add_argument("--path", default=".")
    release.add_argument("--output")
    release.add_argument("--json", action="store_true", dest="json_command")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    as_json = bool(getattr(args, "json_output", False) or getattr(args, "json_command", False))
    try:
        if args.command in {"init", "new-user"}:
            result = _init(args)
        elif args.command == "status":
            result = _status(args)
        elif args.command == "verify":
            result = _verify(args)
        elif args.command == "answer":
            result = _answer(args)
        elif args.command == "reopen":
            result = _reopen(args)
        elif args.command == "gate":
            result = _gate(args)
        elif args.command == "migrate":
            result = migrate_workspace(args.source, args.destination, product_id=args.product_id,
                                       dry_run=args.dry_run).as_dict()
            result["ok"] = result["status"] in {"planned", "migrated"}
        elif args.command == "rollback":
            result = rollback_workspace(args.destination).as_dict()
            result["ok"] = result["status"] == "rolled_back"
        elif args.command == "recover":
            result = recover_workspace(args.destination).as_dict()
            result["ok"] = result["status"] in {"recovered", "aborted", "rolled_back"}
        elif args.command == "provenance":
            output = args.output or str(Path(args.path).resolve() / "docs/release/provenance.json")
            result = build_provenance(args.path, output=output)
            result = {"ok": True, "output": output, **result}
        else:  # pragma: no cover
            raise ValidationError("unknown command")
        _emit(result, as_json)
        return 0 if result.get("ok", True) else 1
    except (OSError, sqlite3.DatabaseError, StoreError, ValueError, RuntimeError) as exc:
        return _error(exc, as_json)


if __name__ == "__main__":
    raise SystemExit(main())
