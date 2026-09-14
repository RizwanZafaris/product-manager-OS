# Scale envelope for full-state domain snapshots

## Scope

`PMOSDomain` (in [pmos/domain.py](../pmos/domain.py)) is a standalone
governance aggregate: organizations, products, initiatives, gates,
approvals, evidence, comments and its own append-only audit trail. Every
mutation re-serializes the *entire* aggregate to one canonical JSON document
and, when a `Store` is attached, commits that whole document as one
versioned snapshot. This page is the published scale envelope audit finding
F34 asked for: measured figures, the hard limit and what happens at it, and
what to do as a product grows. The figures below are measurements from one
machine on one day, not a guarantee for every machine or every shape of
data.

`PMOSDomain` is a separate aggregate from the interview `Conductor` that
`pmos/cli.py` builds for every `pmos` command. Nothing in `pmos/cli.py`
constructs a `PMOSDomain`; it is a governance aggregate a host embeds
directly (see [pmos/usecases.py](../pmos/usecases.py) for worked examples),
not something the shipped `pmos` command line ever touches today. The two
aggregates persist to different paths in the same `Store` and cannot share a
product id (each checks that a loaded snapshot's file set is exactly its
own). Read this page as being about the embedded `PMOSDomain` API, not about
the `pmos` command line.

## The hard limit

`MAX_SNAPSHOT_BYTES` in [pmos/domain.py](../pmos/domain.py) is 16 MiB
(16 x 1024 x 1024 = 16,777,216 bytes). It bounds the canonical JSON encoding
of the whole aggregate: every table (organizations, products, initiatives,
opportunities, experiments, releases, decisions, risks, approvals,
dependencies, portfolio allocations, evidence, metrics, users, memberships,
assignments, comments, mentions), every gate proof, and the complete audit
event history, one entry per mutation ever made. The audit history is not
pruned or summarized: F34's evidence specifically named it as a size driver,
and this benchmark confirms it grows in lockstep with everything else the
aggregate does.

The limit is enforced in two places, both inside `_encode_state`, which the
transactional-mutation wrapper calls on every mutation:

- Before a durable mutation is persisted, once the mutation has run in
  memory: if the new state's canonical encoding exceeds `MAX_SNAPSHOT_BYTES`,
  `PersistenceError("domain snapshot exceeds the safe size limit")` is
  raised. The wrapper catches this, restores the domain's in-memory state
  from the pre-mutation checkpoint, restores the prior store head, and
  re-raises. The mutation has no durable effect; nothing is lost.
- At the start of every mutation (durable or in-memory only), the *current*
  state is re-encoded as a rollback checkpoint. If the domain is already
  over the limit at that point, the same error is raised before the new
  mutation body even runs.

A `PMOSDomain` used without a `Store` (a pure in-memory aggregate) skips the
first check on persist, since there is nothing to persist. It can cross
`MAX_SNAPSHOT_BYTES` on one mutation without that mutation failing; the
*next* mutation then fails at the checkpoint step, because the state it
would checkpoint is already over the limit. Either way, no mutation is ever
left half-applied, and no prior state is ever lost: the acceptance
criterion for F34 ("hitting the limit is actionable and preserves prior
state") already held before this slice; this slice adds the benchmark, this
page, and an early warning before that point.

There is no archive or export command for `PMOSDomain` itself. R15 shipped
`pmos export` for the Conductor state a `pmos` command line actually drives
(see `docs/RUNTIME-QUICKSTART.md`'s Export section); it is a separate
aggregate from `PMOSDomain`, as noted in [Scope](#scope) above, so exporting
a `PMOSDomain` still means backing up the store first (see
[Backup and recovery](#backup-and-recovery) below) and then reducing what
future mutations add (see
[Guidance as a product grows](#guidance-as-a-product-grows)).

## The early warning

Once a snapshot reaches 80% of `MAX_SNAPSHOT_BYTES`
(`SNAPSHOT_WARNING_BYTES`, about 13.4 MiB), two things happen on every
subsequent successful mutation:

- `PMOSDomain.scale_warning` (a read-only property) returns a small mapping
  with `size_bytes`, `limit_bytes`, `percent_of_limit`, and a `message`
  naming the size, the limit, and the next action, the same wording as
  below. It is `None` under the threshold. It reflects the domain's current
  in-memory state, so it is accurate immediately after any mutation, with or
  without a `Store` attached.
- For a durable aggregate, the same structure rides along in that commit's
  own metadata under the `"scale_warning"` key, so a later reader (backup
  tooling, an export command, a future status surface) can see that a given
  commit was near the limit without re-reading and re-encoding the whole
  snapshot.

The message is deliberately plain, for example:

> domain snapshot is 13500000 bytes, 80% of the 16777216 byte
> MAX_SNAPSHOT_BYTES limit; archive old audit history or export the product
> soon; see docs/SCALE.md for measured figures and options

The export half of that message is aspirational until R15 ships; today the
action is to read this page and plan ahead. Nothing enforces the warning by
itself and nothing before the hard limit blocks a mutation.

The warning lives in [pmos/domain.py](../pmos/domain.py) because that is the
module that carries `MAX_SNAPSHOT_BYTES`. `pmos/cli.py` still does not build
a `PMOSDomain` (see [Scope](#scope) above), so this `scale_warning` is not
what `pmos status` surfaces; a host embedding `PMOSDomain` directly can check
it after any mutation right now. R15 added the CLI-facing counterpart for
the aggregate `pmos/cli.py` does drive: `Conductor.scale_warning` in
[pmos/conductor.py](../pmos/conductor.py), bounded by the Conductor's own,
much smaller, `MAX_STATE_BYTES` (1 MiB, not this page's 16 MiB
`MAX_SNAPSHOT_BYTES`). `pmos status` reports it as `capacity_warning`; see
`docs/RUNTIME-QUICKSTART.md`'s Export section for both the warning and the
`pmos export` command it names as the next action.

## Measured figures

Measured with [tools/bench_scale.py](../tools/bench_scale.py) (a full run,
not `--quick`) on:

| | |
|---|---|
| Machine | Apple M4 Pro, 24 GiB RAM |
| Platform | macOS-26.6.2-arm64-arm-64bit |
| Python | 3.12.13 |
| Commit | ec8da5c (R12's own changes were uncommitted at measurement time, per this slice's setup instructions) |
| Date | 2026-09-14T20:24:44Z |

### Mutation, backup and recovery (the `PMOSDomain` construct)

One `PMOSDomain` per tier, backed by a real SQLite `Store`, padded with real
`create_evidence` and `comment` calls to the target percentage of
`MAX_SNAPSHOT_BYTES`. "Mutation" times only `complete_gate` on a freshly
created initiative; setup (the initiative and its one evidence item) is not
timed. "Backup" and "recover" time `Store.backup` and `Store.restore` on the
SQLite database holding that tier's snapshot.

| Tier | Snapshot bytes | Artifacts | Audit events | Gate commit p50 / p95 (ms) | Backup p50 / p95 (ms) | Recover p50 / p95 (ms) | Warning fired |
|---|---|---|---|---|---|---|---|
| 25% | 4,219,230 (25.2%) | 15 | 30 | 101.7 / 122.0 | 455.8 / 614.7 | 466.7 / 711.2 | no |
| 50% | 8,413,534 (50.2%) | 29 | 54 | 205.3 / 276.1 | 917.4 / 1012.6 | 862.9 / 1141.1 | no |
| 75% | 12,607,884 (75.2%) | 43 | 78 | 296.4 / 321.0 | 1348.7 / 1535.8 | 1347.1 / 3391.4 | no |
| 95% | 15,963,397 (95.2%) | 54 | 97 | 386.7 / 440.5 | 8229.9 / 13916.2 | 9438.4 / 15098.3 | yes |

Two things stand out. Gate commit latency grows roughly linearly with
snapshot size, which is expected: every mutation re-encodes the whole
aggregate twice (a rollback checkpoint, then the persisted state) and
re-checks every stored invariant. Backup and recovery do not grow linearly;
they are cheap under half the limit and become an order of magnitude more
expensive near it on this machine. Budget for that jump rather than
extrapolating linearly from a small product's numbers.

### Status (the `Conductor` construct)

`Conductor.next_turn` and `pmos.phases.phase_report` are Conductor
operations, not `PMOSDomain` operations (see [Scope](#scope) above), so they
are measured on a separate `Conductor` workspace per tier, with banks,
answered questions and gate-manifest artifact counts scaled by the same
tier fraction against `Conductor`'s own state limit
(`MAX_STATE_BYTES` in [pmos/conductor.py](../pmos/conductor.py), 1 MiB, a
different and much smaller number than `MAX_SNAPSHOT_BYTES`).

| Tier | Banks | Answers | Manifest artifacts | Conductor state bytes | next_turn p50 / p95 (ms) | phase_report p50 / p95 (ms) |
|---|---|---|---|---|---|---|
| 25% | 2 | 10 | 16 | 9,675 | 0.24 / 0.79 | 1.64 / 2.66 |
| 50% | 3 | 30 | 45 | 25,759 | 0.44 / 0.50 | 1.87 / 2.05 |
| 75% | 4 | 60 | 88 | 49,413 | 0.79 / 0.93 | 3.24 / 3.51 |
| 95% | 6 | 114 | 168 | 92,435 | 1.48 / 1.56 | 5.82 / 6.08 |

Conductor state stays two to three orders of magnitude smaller than a
`PMOSDomain` snapshot at every tier, so status latency stays under a few
milliseconds throughout this range; it is not the bottleneck F34 is about.

## Guidance as a product grows

**Below the 80% warning.** Nothing to do. Mutation latency grows with
snapshot size but stays workable through this whole range on ordinary
hardware.

**Past the 80% warning, under the hard limit.** `scale_warning` starts
returning a structured warning after every mutation (see
[The early warning](#the-early-warning)). Back up the store now, while
backup is still cheap (see the measured figures above). The single most
effective lever available today, before R15's export command ships, is to
prefer digest-only evidence for large source material: call
`create_evidence(..., content="", content_hash=<sha256>, ...)` with a host
`evidence_verifier` configured, so the large document lives outside the
snapshot and only its hash is stored inline. Free-text `content` and
`comment` bodies are what this benchmark used to reach each tier's target
size efficiently; they are the fastest way to grow a snapshot, and the
audit trail grows by one event on every mutation regardless, so fewer,
larger mutations do not avoid history growth, only content-size growth.

**At the hard limit.** Mutations that would grow the encoded snapshot past
`MAX_SNAPSHOT_BYTES` are refused with `PersistenceError`; see
[The hard limit](#the-hard-limit). Nothing is lost and no partial write
happens. Until R15 ships an export path, the only way to keep working is to
stop growing this aggregate: start a new product/initiative split across
more than one `PMOSDomain` (a different `storage_id` in the same `Store`),
or reduce future mutations to metadata-only changes that do not add
evidence or comment content.

## Backup and recovery

`Store.backup(destination)` uses SQLite's own backup API; `Store.restore(backup,
destination)` copies it to a new or existing database path. Both are
available at any time regardless of `PMOSDomain`'s size, since they operate
on the SQLite file, not on the decoded aggregate. Run a backup on a regular
cadence rather than only once a product approaches the limit: the measured
figures above show backup and recovery growing much faster than linearly in
the last quarter of the range, so a backup taken at 95% costs roughly 20
times what the same operation costs at 25% on this machine.

## Reproducing these numbers

```
python3.12 tools/bench_scale.py            # full run: real percentages of MAX_SNAPSHOT_BYTES, ~3 minutes on the machine above
python3.12 tools/bench_scale.py --quick    # small fixed ceiling, a handful of repetitions, seconds; exercises the same code paths, not scale figures
```

Both print one JSON object: per-tier snapshot bytes, artifact and history
counts, and p50/p95 latency for mutation, status, backup and recovery, plus
the machine, Python version, commit and timestamp the run was measured
against. `--quick` numbers are not scale figures and must never be copied
into the tables above; only a full run's numbers belong here. The tool uses
a fixed default seed, so a full run's synthetic content is the same from
run to run; wall-clock timings still vary with the machine and its load.
The tool is not part of any CI gate; it is a manual instrument for
re-measuring this page when the aggregate's shape changes materially.
