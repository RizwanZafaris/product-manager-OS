#!/usr/bin/env python3.12
"""Scale benchmark for full-state domain snapshots (audit F34, slice R12).

Builds synthetic products in a temporary directory at four documented size
tiers (25, 50, 75 and 95 percent of ``pmos.domain.MAX_SNAPSHOT_BYTES``) and
measures, through the real pmos APIs:

  * mutation   -- a gate commit (``PMOSDomain.complete_gate``) on a
                  ``PMOSDomain`` whose durable snapshot has been padded, via
                  real ``create_evidence``/``comment`` calls, to the tier's
                  target byte size;
  * status     -- ``Conductor.next_turn`` and ``pmos.phases.phase_report`` on
                  a separately built ``Conductor`` workspace, sized by answer
                  count (history length) and gate-manifest artifact count
                  scaled by the same tier fraction;
  * backup and recovery -- ``Store.backup`` and ``Store.restore`` on the
                  domain's own SQLite-backed store (the one holding the large
                  snapshot).

Two constructs are used because ``PMOSDomain`` (governed by
MAX_SNAPSHOT_BYTES, 16 MiB) and ``Conductor`` (governed by its own, much
smaller MAX_STATE_BYTES, 1 MiB) are independent aggregates in this codebase;
neither is reachable from the other, and the CLI in pmos/cli.py only ever
builds a Conductor. See docs/SCALE.md for the full writeup of this split and
what each number means.

Deterministic: every random choice is drawn from ``random.Random(seed)``, and
--seed defaults to a fixed constant, so two runs with the same seed produce
the same synthetic content (byte-for-byte content, not wall-clock timings).

--quick trades size and repetition count for speed so this can run inside a
test: it targets a small fixed byte ceiling instead of the real 16 MiB limit
and uses far fewer repetitions. Quick-mode numbers are not scale figures and
must never be copied into docs/SCALE.md; only a full run's numbers may be.

This tool is intentionally not wired into any CI gate (see the acceptance
list in the R12 task) -- it is a manual/occasional instrument, not a check
that blocks a merge on a latency regression.

Standard library only. No network call, no model call.
"""

from __future__ import annotations

import argparse
import json
import platform
import random
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pmos.conductor import Conductor, EvidenceClass, Question, QuestionBank  # noqa: E402
from pmos.domain import (  # noqa: E402
    LifecycleStage,
    MAX_SNAPSHOT_BYTES,
    PMOSDomain,
    SNAPSHOT_PATH,
)
from pmos.phases import phase_report  # noqa: E402
from pmos.store import Store  # noqa: E402

DEFAULT_SEED = 20260912
TIERS = (0.25, 0.50, 0.75, 0.95)

# ---------------------------------------------------------------------------
# Tunables. "full" targets the real MAX_SNAPSHOT_BYTES; "quick" targets a
# small fixed ceiling purely to exercise the same code paths fast.
# ---------------------------------------------------------------------------


class _Config:
    def __init__(self, quick: bool) -> None:
        self.quick = quick
        if quick:
            self.domain_limit_bytes = 65_536
            self.domain_chunk_bytes = 8_000
            self.domain_baseline_max = 4
            self.mutation_reps = 3
            self.status_reps = 3
            self.backup_reps = 2
            self.conductor_banks_max = 2
            self.conductor_questions_max = 3
            self.conductor_artifacts_max = 3
        else:
            self.domain_limit_bytes = MAX_SNAPSHOT_BYTES
            self.domain_chunk_bytes = 1_000_000
            self.domain_baseline_max = 40
            self.mutation_reps = 11
            self.status_reps = 21
            self.backup_reps = 5
            self.conductor_banks_max = 6
            self.conductor_questions_max = 20
            self.conductor_artifacts_max = 30


# ---------------------------------------------------------------------------
# Small helpers: percentiles and timing.
# ---------------------------------------------------------------------------


def _percentile(samples: list[float], pct: float) -> float:
    """Linear-interpolation percentile; works for any non-empty sample list."""
    if not samples:
        return 0.0
    ordered = sorted(samples)
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    fraction = rank - low
    return ordered[low] + (ordered[high] - ordered[low]) * fraction


def _summarize(samples: list[float]) -> dict[str, Any]:
    return {
        "count": len(samples),
        "p50_ms": round(_percentile(samples, 50) * 1000, 3),
        "p95_ms": round(_percentile(samples, 95) * 1000, 3),
        "min_ms": round(min(samples) * 1000, 3) if samples else 0.0,
        "max_ms": round(max(samples) * 1000, 3) if samples else 0.0,
    }


def _time_calls(fn: Callable[[], Any], reps: int) -> list[float]:
    samples = []
    for _ in range(reps):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return samples


_PADDING_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789 "


def _padding_text(rng: random.Random, length: int) -> str:
    # rng.choices() (bulk) rather than a per-character rng.choice() loop:
    # full mode generates tens of millions of characters across all tiers.
    return "".join(rng.choices(_PADDING_ALPHABET, k=length))


# ---------------------------------------------------------------------------
# The domain (mutation + snapshot-bytes sizing + backup/recovery) construct.
# ---------------------------------------------------------------------------


def _build_domain_tier(tmp_path: Path, tier: float, cfg: _Config, rng: random.Random) -> dict[str, Any]:
    db_path = tmp_path / ("domain-%d.sqlite3" % int(tier * 1000))
    store = Store(db_path)
    domain = PMOSDomain(store, storage_id="bench-domain")
    _org, product, owner, _membership = domain.bootstrap_workspace(
        "Bench Org", "Bench Product", "Bench Owner"
    )
    initiative = domain.create_initiative(product.id, "Scale bench initiative", actor_id=owner.id)

    target_bytes = max(1, int(cfg.domain_limit_bytes * tier))
    baseline_count = max(1, round(cfg.domain_baseline_max * tier))
    artifact_count = 0

    # A realistic shape first: small evidence and comments.
    for i in range(baseline_count):
        domain.create_evidence(
            initiative.id, "Observed behavior %d" % i,
            _padding_text(rng, 200), actor_id=owner.id,
        )
        artifact_count += 1
        domain.comment(initiative.id, _padding_text(rng, 120), actor_id=owner.id)

    # Then large padding entries to reach the target byte size efficiently
    # (few, large mutations rather than many small ones -- each mutation
    # re-encodes the *entire* state, so call count dominates wall time).
    snapshot = store.read_snapshot("bench-domain")
    current_bytes = len(snapshot.files[SNAPSHOT_PATH])
    while current_bytes < target_bytes:
        remaining = target_bytes - current_bytes
        chunk = min(cfg.domain_chunk_bytes, max(64, remaining))
        domain.create_evidence(
            initiative.id, "Padding evidence %d" % artifact_count,
            _padding_text(rng, chunk), actor_id=owner.id,
        )
        artifact_count += 1
        snapshot = store.read_snapshot("bench-domain")
        current_bytes = len(snapshot.files[SNAPSHOT_PATH])

    history_length = len(domain.history)
    scale_warning = domain.scale_warning

    # Mutation: a gate commit through the real pmos API. Setup (a fresh
    # initiative plus its one evidence item) happens outside the timed
    # window; only complete_gate() itself is timed.
    mutation_samples: list[float] = []
    for i in range(cfg.mutation_reps):
        gate_initiative = domain.create_initiative(
            product.id, "Gate bench %d" % i, actor_id=owner.id
        )
        evidence = domain.create_evidence(
            gate_initiative.id, "Gate evidence", "ok", actor_id=owner.id
        )
        start = time.perf_counter()
        domain.complete_gate(
            gate_initiative.id, LifecycleStage.DISCOVER,
            evidence_ids=[evidence.id], actor_id=owner.id,
            expected_revision=gate_initiative.revision,
        )
        mutation_samples.append(time.perf_counter() - start)

    final_snapshot = store.read_snapshot("bench-domain")
    final_bytes = len(final_snapshot.files[SNAPSHOT_PATH])

    # Backup and recovery on the store that holds this large snapshot.
    backup_samples: list[float] = []
    recover_samples: list[float] = []
    for i in range(cfg.backup_reps):
        backup_path = tmp_path / ("domain-%d-backup-%d.sqlite3" % (int(tier * 1000), i))
        start = time.perf_counter()
        store.backup(backup_path)
        backup_samples.append(time.perf_counter() - start)

        restore_path = tmp_path / ("domain-%d-restore-%d.sqlite3" % (int(tier * 1000), i))
        start = time.perf_counter()
        restored = Store.restore(backup_path, restore_path)
        recover_samples.append(time.perf_counter() - start)
        restored.close()

    store.close()

    return {
        "tier": tier,
        "target_bytes": target_bytes,
        "snapshot_bytes": final_bytes,
        "percent_of_max_snapshot_bytes": round(100 * final_bytes / MAX_SNAPSHOT_BYTES, 2),
        "artifact_count": artifact_count,
        "history_length": history_length,
        "scale_warning_present": scale_warning is not None,
        "scale_warning": scale_warning,
        "mutation_gate_commit_ms": _summarize(mutation_samples),
        "backup_ms": _summarize(backup_samples),
        "recover_ms": _summarize(recover_samples),
    }


# ---------------------------------------------------------------------------
# The Conductor (status: next_turn + phase_report) construct.
# ---------------------------------------------------------------------------


def _build_conductor_tier(tmp_path: Path, tier: float, cfg: _Config) -> dict[str, Any]:
    db_path = tmp_path / ("conductor-%d.sqlite3" % int(tier * 1000))
    store = Store(db_path)

    bank_count = max(1, round(cfg.conductor_banks_max * tier))
    questions_per_bank = max(1, round(cfg.conductor_questions_max * tier))
    artifacts_per_gate = max(1, round(cfg.conductor_artifacts_max * tier))

    banks = []
    for b in range(bank_count):
        questions = tuple(
            Question(
                "bank%d-q%d" % (b, q),
                "Synthetic bench question %d for bank %d?" % (q, b),
                EvidenceClass.TEAM_BELIEF,
            )
            for q in range(questions_per_bank)
        )
        banks.append(QuestionBank("bank-%d" % b, "v1", questions, gate_approvers=("approver-1",)))

    def gate_manifest(bank_id: str) -> dict[str, Any]:
        return {
            "artifacts": [
                {"id": "%s-art-%d" % (bank_id, i), "path": "%s/art-%d.md" % (bank_id, i),
                 "revision": "r1", "depends_on": []}
                for i in range(artifacts_per_gate)
            ],
            "dependencies": [],
        }

    conductor = Conductor(
        store, "bench-conductor", banks,
        gate_source_verifier=lambda _source, _digest: True,
        gate_manifest=gate_manifest,
    )

    turn_counter = 0
    history_length = 0
    for bank in banks:
        for question in bank.questions:
            position = conductor.next_turn()
            outcome = conductor.submit_answer(
                question.id, "Deterministic synthetic bench answer.",
                {"class": "team_belief", "source": "bench-fixture"},
                expected_revision=position.revision, turn_id="answer-%d" % turn_counter,
            )
            turn_counter += 1
            if not outcome.accepted:
                raise RuntimeError("bench setup: answer was not accepted: %s" % outcome.message)
            history_length += 1
        position = conductor.next_turn()
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        proof = {
            "source": "bench-source", "source_sha256": "0" * 64,
            "actor_id": "approver-1", "requester_id": "requester-1",
            "decision": "approved", "approved_at": now,
        }
        outcome = conductor.prove_gate(
            bank.id, proof, expected_revision=position.revision, turn_id="gate-%d" % turn_counter,
        )
        turn_counter += 1
        if outcome.status not in ("advanced", "completed"):
            raise RuntimeError("bench setup: gate proof was not accepted: %s" % outcome.message)

    root = tmp_path / ("conductor-%d-root" % int(tier * 1000))
    root.mkdir(exist_ok=True)

    next_turn_samples = _time_calls(lambda: conductor.next_turn(), cfg.status_reps)
    phase_report_samples = _time_calls(lambda: phase_report(conductor, None, root), cfg.status_reps)

    conductor_state_bytes = len(store.read_snapshot("bench-conductor").files[".pmos/conductor/state.json"])
    store.close()

    return {
        "tier": tier,
        "bank_count": bank_count,
        "questions_per_bank": questions_per_bank,
        "artifact_count": bank_count * artifacts_per_gate,
        "history_length": history_length,
        "conductor_state_bytes": conductor_state_bytes,
        "next_turn_ms": _summarize(next_turn_samples),
        "phase_report_ms": _summarize(phase_report_samples),
    }


# ---------------------------------------------------------------------------
# Orchestration.
# ---------------------------------------------------------------------------


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(_REPO_ROOT), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def run(quick: bool, seed: int) -> dict[str, Any]:
    cfg = _Config(quick)
    rng = random.Random(seed)
    domain_results = []
    conductor_results = []
    with tempfile.TemporaryDirectory(prefix="pmos-bench-scale-") as tmp:
        tmp_path = Path(tmp)
        for tier in TIERS:
            domain_results.append(_build_domain_tier(tmp_path, tier, cfg, rng))
            conductor_results.append(_build_conductor_tier(tmp_path, tier, cfg))

    return {
        "tool": "tools/bench_scale.py",
        "purpose": "R12 / audit finding F34: scale envelope for full-state domain snapshots",
        "quick": quick,
        "seed": seed,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "commit": _git_commit(),
        "max_snapshot_bytes": MAX_SNAPSHOT_BYTES,
        "domain_limit_bytes_used": cfg.domain_limit_bytes,
        "note": (
            "quick mode targets a small fixed byte ceiling, not the real "
            "MAX_SNAPSHOT_BYTES; only a full (non --quick) run's numbers "
            "belong in docs/SCALE.md."
        ) if quick else (
            "full run: domain tiers target real percentages of "
            "MAX_SNAPSHOT_BYTES; conductor tiers scale answer/artifact "
            "counts by the same tier fraction against Conductor's own, "
            "much smaller MAX_STATE_BYTES."
        ),
        "domain": domain_results,
        "conductor": conductor_results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true",
                        help="small fixed byte ceiling and few repetitions; fast enough for a test")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="seed for deterministic synthetic content (default: %(default)s)")
    args = parser.parse_args(argv)
    result = run(quick=args.quick, seed=args.seed)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
