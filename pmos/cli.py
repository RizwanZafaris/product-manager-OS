"""The small, dependency-free Product Manager OS command line interface."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sqlite3
import stat
import sys
from pathlib import Path
from typing import Any, Sequence

from .conductor import Conductor, EvidenceClass, Question, QuestionBank, TurnOutcome
from .migrations import migrate_workspace, recover_workspace, rollback_workspace
from .release import build_provenance, verify_provenance
from .store import NotFoundError, Store, StoreError, ValidationError


def _banks() -> tuple[QuestionBank, ...]:
    return (QuestionBank(
        "onboarding", "v1", (Question(
            "first-outcome", "What outcome should the first product user achieve?",
            EvidenceClass.OBSERVED_BEHAVIOR),),
        gate_approvers=("local-reviewer",)),)


def _local_gate_verifier(root: Path):
    """Verify a bounded, non-symlink proof artifact below the workspace root."""
    resolved_root = root.resolve()

    def verify(source: str, expected_hash: str) -> bool:
        relative = Path(source)
        if (relative.is_absolute() or not relative.parts or ".." in relative.parts or
                relative.parts[0] == ".pmos" or "\\" in source):
            return False
        opened: list[int] = []
        try:
            directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | \
                getattr(os, "O_NOFOLLOW", 0)
            file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            current = os.open(resolved_root, directory_flags)
            opened.append(current)
            for component in relative.parts[:-1]:
                current = os.open(component, directory_flags, dir_fd=current)
                opened.append(current)
            file_fd = os.open(relative.parts[-1], file_flags, dir_fd=current)
            opened.append(file_fd)
            metadata = os.fstat(file_fd)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 16 * 1024 * 1024:
                return False
            digest = hashlib.sha256()
            total = 0
            while True:
                chunk = os.read(file_fd, 1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > 16 * 1024 * 1024:
                    return False
                digest.update(chunk)
            return hmac.compare_digest(digest.hexdigest(), expected_hash)
        except (OSError, ValueError, TypeError):
            return False
        finally:
            for descriptor in reversed(opened):
                try:
                    os.close(descriptor)
                except OSError:
                    pass

    return verify


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
    with Store(database) as store:
        store.create_product(product_id)
        conductor = Conductor(store, product_id, _banks())
        pending = conductor.next_turn(expected_revision=0)
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
    if database.exists() and not args.force:
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
            raise ValidationError("runtime contains no product; run `pmos init --force`")
        head = store.head(product_id)
        report = store.verify()
        snapshot = store.read_snapshot(product_id)
        return {"ok": report.ok, "status": "ready" if report.ok else "corrupt",
                "root": str(root), "database": str(database), "product_id": product_id,
                "revision": head.revision, "commit_hash": head.commit_hash,
                "file_count": len(snapshot.files), "errors": list(report.errors)}


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
        conductor = Conductor(store, args.product_id, _banks(),
                              gate_source_verifier=_local_gate_verifier(root))
        outcome = conductor.submit_answer(args.question_id, args.answer, _evidence(args.evidence),
                                          expected_revision=args.expected_revision, turn_id=args.turn_id)
        result = {"ok": outcome.accepted, "product_id": args.product_id,
                  "outcome": _outcome_dict(outcome)}
        if not outcome.accepted:
            result["error"] = "answer was not accepted; supply the requested evidence and current revision"
        return result


def _gate(args: argparse.Namespace) -> dict[str, Any]:
    root, database = _paths(args.path)
    if not database.exists():
        raise ValidationError("runtime is missing; run `pmos init --path %s`" % root)
    with Store(database) as store:
        conductor = Conductor(store, args.product_id, _banks(),
                              gate_source_verifier=_local_gate_verifier(root))
        outcome = conductor.prove_gate(args.bank_id, _evidence(args.evidence),
                                       expected_revision=args.expected_revision, turn_id=args.turn_id)
        result = {"ok": outcome.completed, "product_id": args.product_id,
                  "outcome": _outcome_dict(outcome)}
        if not outcome.completed:
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
            sub.add_argument("--force", action="store_true", help="allow an existing runtime when product is absent")
        if name == "verify":
            sub.add_argument("--provenance", help="provenance manifest to verify")
    for name, help_text in (("answer", "submit a caller-supplied answer and evidence"),
                            ("gate", "submit caller-supplied gate proof")):
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("--path", default=".")
        sub.add_argument("--product-id", required=True)
        sub.add_argument("--expected-revision", required=True,
                         help="head token returned by init/status/previous outcome")
        sub.add_argument("--turn-id", required=True, help="unique idempotency key for this submission")
        sub.add_argument("--evidence", required=True, help="JSON object containing caller-supplied evidence")
        sub.add_argument("--json", action="store_true", dest="json_command")
        if name == "answer":
            sub.add_argument("--question-id", required=True)
            sub.add_argument("--answer", required=True)
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
