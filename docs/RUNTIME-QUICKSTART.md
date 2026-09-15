# PMOS runtime quickstart

Product Manager OS is usable as a document tree, and its optional local
runtime is standard-library Python.  It does not require an API key, a hosted
service, or a model.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --no-index .
pmos init --path ./products/my-product --product-id checkout
pmos status --path ./products/my-product
pmos verify --path ./products/my-product
```

For a release-style packaging check, use a normal isolated PEP 517 build:
`python -m pip wheel --no-index --no-deps --wheel-dir /tmp/pmos-wheels .`.
The project uses a repository-local, standard-library PEP 517 backend, so no
runtime dependencies are downloaded or required.

`init` creates `.pmos/runtime.sqlite`, creates the product through the public
Store API, pins the shipped question bank contract into the product, and
renders `DISCOVER-1`, the first question of the `DISCOVER` bank, through the
public Conductor API.  It never invents a customer answer or gate proof. Add
`--json` before or after the command for automation:

```bash
pmos --json status --path ./products/my-product
```

Continue only with evidence you actually collected. The revision token and
question ID come from `init`/`status`, and `status` also prints a `next` line
with the one command to run next: the answer, the reopen command for a parked
question, or the gate command for a bank ready for approval or whose approval
went stale. A bank is ready for its gate once every question in it is
answered, and `pmos status` names the next question each time. The evidence
fields are checked by the conductor:

```bash
pmos answer --path ./products/my-product --product-id checkout \
  --question-id DISCOVER-1 --answer "<your observed outcome>" \
  --evidence '{"class":"observed_behavior","source":"<interview or artifact>","date":"<YYYY-MM-DD>","location":"<where observed>"}' \
  --expected-revision '<revision_token from pmos status>' --turn-id answer-001 --json

pmos reopen --path ./products/my-product --product-id checkout \
  --question-id DISCOVER-1 --reason "<why you are reopening this parked question>" \
  --expected-revision '<revision_token from pmos status>' --turn-id reopen-001 --json

pmos gate --path ./products/my-product --product-id checkout --bank-id discover \
  --evidence '{"source":"approval/discover.txt","source_sha256":"<sha256-of-that-file>","actor_id":"local-reviewer","requester_id":"local-operator","decision":"approved","approved_at":"<UTC-YYYY-MM-DDTHH:MM:SSZ>"}' \
  --expected-revision '<revision_token from pmos status>' --turn-id gate-001 --json
```

A refusal never records a gate approval, and the answer it refused is not
accepted. Most refusals are still committed as a turn record, so the store
revision advances: insufficient evidence, an answer to any question other
than the one offered (an unknown question ID included), and an unverifiable
gate source each write a record and move the revision on. A stale expected
revision and a reused turn ID leave the revision where it was, and so does a
request refused before the conductor reads it: a question ID that is not well
formed, evidence that is not a JSON object, or a bank ID that does not exist.
Replaying a turn ID with the identical request returns its original result.
Read the next revision from `pmos status`, which prints `revision_token`
(the exact token to pass as `--expected-revision`; a product made by `init`
is already at revision 1 because `init` commits the pinned contract, and
`pmos status` always prints the exact token), or, for a refusal that wrote a
record, from that refusal's own `revision` field. After a refusal that wrote
a record, the revision `answer` returned is stale and retrying with it is
refused as a
conflict; `pmos status` is current either way.
A third refused submission, after two challenges, parks it: the answer is
filed as offered and marked parked, the cursor moves on, and the bank's
remaining questions can still be answered. The bank's gate proof is refused
while any of its answers is parked. To recover, reopen the parked question
with its question ID, a reason, the current revision, and a new turn ID, then
answer it with fresh evidence, because evidence identical to a refused
submission is refused afterwards.
Replace every angle-bracket value with a real, traceable source; the source
must be a regular, non-symlink file inside the workspace (but outside
`.pmos/`) and its digest must match. The pinned banks name `local-reviewer`
as the gate approver and reject self-approval where requester and reviewer
are the same. Placeholders are intentionally not accepted as evidence by the
runtime.

When `pmos gate` records an approval, it also records a manifest: every file
in the workspace whose artifact block names that bank's gate (DISCOVER is
gate 1, and so on to OPERATE, gate 6), each with its path and revision (the
SHA-256 of its body after the block), plus the artifacts they depend on. A
gate whose artifacts depend on one the workspace does not have yet is
refused, and the error names it. Every later command checks each approval's
source file and manifest again, and an edited or deleted artifact makes that
approval stale. `pmos status` then lists every stale bank under
`stale_banks`, earliest first, each with `changed` (the artifact, its
reviewed and its current revision) and `reconcile` (the approved artifacts
that depend on a changed one), and `next` is the gate command for the
earliest. Proving a stale bank again records the current revisions, keeps
the earlier approval as superseded history and moves nothing else; another
bank whose approval still binds the old revision stays stale until it is
approved again. A gate submitted with `"decision":"rejected"` is recorded,
reported with `rejection_recorded` and listed under `rejections` in status,
and it never advances the interview. Every approval is labelled a local
attestation (`approvals` in status), because actor IDs are typed, not
authenticated.

## Phase status

`pmos status` also reports `phases`: one entry per question bank, DISCOVER
through OPERATE, in stage order, built by the same read-only query an adapter
can call on its own, such as the desktop adapter's `pmos_status` tool (see
`docs/COMPATIBILITY.md`'s execution-host matrix and
`harness/adapters/desktop/README.md`). In human mode the line
prints as JSON, the same as every other list `status` already prints; add
`--json` for the whole document. Each entry carries:

- `phase` (the stage name, for example `DISCOVER`), `bank_id` (the bank's
  internal id, for example `discover`), and `gate` (the gate number that
  bank's approval satisfies).
- `state`, one of `approved`, `stale`, `awaiting_approval`, `blocked` (a
  parked answer), `in_progress`, or `not_started`.
- `outcomes`: each Gate checklist line from the pinned contract, with the
  question IDs that evidence it and `met` (`true` once every one of those
  questions is answered and unparked, `false` while any is missing or
  parked, `null` for a line no question can evidence, such as a human
  sign-off the Conductor only reports the presence of).
- `documents` and `named_documents`: `documents` lists the workspace
  artifacts whose artifact block names this gate, each with its `id`, `path`,
  `phase`, its current status and revision from `scan()`, and, once the gate
  is approved, the revision the approval binds; `named_documents` lists the
  workspace paths the bank's own questions land in, each with `present`
  (`true` when that path is a regular file in the workspace).
- `completed`: the accepted question IDs for this bank (`questions`), split
  into `source_verified` and `supplied_unverified` counts.
- `missing`: unanswered question IDs, parked question IDs, and unmet Gate
  lines; for a stale bank it also carries `changed` (the artifacts that no
  longer match the approved revision) and `reconcile` (the approved
  artifacts that depend on one of those changed artifacts), both empty for
  a bank that is not stale.
- `next_action`: the one step that moves this phase forward, as data rather
  than shell syntax, for example `{"action": "answer", "bank_id": "discover",
  "question_id": "DISCOVER-1"}`, or `null` when this phase has nothing to do
  right now. `action` is `answer`, `reopen`, or `gate`; the CLI turns this
  into the shell command `status` already prints under `next`, and an
  adapter renders its own form from the same data.
- `required_approver`: `runtime` (the pinned bank's approver IDs, the same
  ones a `pmos gate` submission is checked against), `attestation` (always
  `local`), and `signoff_roles` (the human roles named in that gate's
  sign-off table in `os/STAGE-GATES.md`, compiled into the contract; `null`
  for a product pinned before that compilation existed).
- `blocking_reason`: why this phase cannot move right now, for example
  "waits for Gate 1 approval" or the Conductor's message for a stale or
  parked bank, or `null` when nothing is blocking it.
- `approval` and `rejections`: the same per-bank approval and rejection
  summaries `status` already reports at the top level, repeated here beside
  the phase they belong to.

Building `phases` can itself run into a malformed workspace, for example a
symlinked artifact under an artifact block `scan()` refuses to follow. That
never hides the rest of `status`: `phases` comes back as an empty list and
the top-level result carries `phases_error` naming what went wrong, instead
of `status` failing outright.

## The file-to-runtime boundary

F01: Markdown and the runtime are one system with one authority for each
field, not two copies that can quietly disagree.

- **File-owned:** a workspace artifact's body and its authored frontmatter
  fields (`artifact_id`, `phase`, `status`, `depends_on`, `template`). You
  edit these directly, in any editor, with no runtime call.
- **Runtime-owned:** gate approvals, the artifact revisions they bind, and
  interview answers. These change only through `pmos answer`, `pmos reopen`,
  and `pmos gate`; no direct file edit changes them.
- **Stable IDs and the revision rule.** `artifact_id` is the identity that
  survives a rename; `pmos/artifacts.py`'s `artifact_revision()` is the
  SHA-256 of an artifact's body after its frontmatter block, computed fresh
  every time, never typed by hand. A gate approval binds the revisions of
  every artifact whose block names that gate, plus everything they depend on,
  in one manifest (see `pmos gate` above).
- **A direct edit becomes a pending proposal, not an accepted change.**
  Editing an approved artifact's body changes its revision. That alone does
  not revise the approval: the runtime still holds the revision it bound, so
  `pmos status` marks the bank `stale` and `pmos reconcile` lists the edit as
  pending. The edit is accepted only by re-proving the affected gate with
  `pmos gate`, which records the new revisions and keeps the superseded
  approval as history (see `## Reconcile` below).
- **What export does and does not do.** `pmos export` writes the runtime's
  side of a product, portably: interview answers, every gate approval with
  the manifest it bound, and the stale gates, versioned and human-indexed.
  It is an archive/read path, not an import path: nothing in this slice
  reads an export back into a runtime.
- **The Obsidian UI round trip is deferred.** A control-station UI that lets
  someone accept a proposal or prove a gate from inside Obsidian is owner-
  deferred and out of scope here. `pmos reconcile` and `pmos export` are the
  CLI/agent half of the boundary; the file half (artifact frontmatter and
  body) already round-trips through any editor, Obsidian included, today.

## Reconcile: pending proposals and conflicts

`pmos reconcile` is read-only: it never commits to the store and never edits
a workspace file. It compares the workspace to the runtime's bound approvals
and reports two things.

```bash
pmos reconcile --path ./products/my-product --product-id checkout --json
```

**Pending proposals.** Each workspace artifact whose current body differs
from the revision the runtime's latest approval bound for it, sorted by id:
its `id`, `path`, `accepted_revision`, `current_revision`, `stales_gates`
(every bank whose approval no longer verifies because of it),
`reconcile_dependents` (other approved artifacts that depend on it and so
also need reconciliation), and `next_action`, one `{"bank_id", "command"}`
entry per staled bank naming the `pmos gate` re-proof that accepts the
edit. `pmos gate` is the only accepted way to clear a pending proposal;
reconcile itself changes nothing.

**Conflicts**, named explicitly rather than surfaced as a stack trace: a
bound artifact that is missing (`missing_artifact`), a bound id that now
belongs to a different file because the file's own `artifact_id` field
changed (`artifact_id_changed`), two files sharing one id
(`duplicate_id`), and a symlinked or unreadable artifact
(`symlinked_artifact` / `unreadable_artifact`). `scan()` stops at the first
workspace-wide problem it finds, so a duplicate id or a symlinked/unreadable
file reports as one conflict per call; fix it and reconcile again to see the
next.

`reconcile` reuses `pmos/artifacts.py`'s `check_manifest()` through
`Conductor.stale_gates()`, the exact comparison `pmos status` and `pmos gate`
already run; it does not invent a second approval path. A clean workspace
returns empty `pending` and `conflicts` lists and exits 0.

## Export: portable archive

```bash
pmos export --path ./products/my-product --product-id checkout --out ./archive/checkout-2026-09-15 --json
```

`pmos export` is read-only on the store: it only reads the current snapshot
and writes two local files under `--out` (created if missing):

- `export.json`: a versioned (`pmos.export.v1`) package with the schema
  version, product id, source revision, interview answers, every gate
  approval with the manifest it bound and its attestation (always `local`
  today), and the stale gates.
- `EXPORT.md`: a short human index of the same package, in the style of
  `handoff/CONTEXT.md`.

This is F34's archive/export path: the lever `docs/SCALE.md` names for
staying ahead of a growing snapshot. **It is not an import path.** Reading an
export back into a runtime is out of scope for this slice; nothing consumes
`export.json` as input.

`pmos export` refuses to overwrite an existing `export.json` unless `--force`
is given, so a scripted backup cadence never silently clobbers an earlier
archive:

```bash
pmos export --path ./products/my-product --product-id checkout --out ./archive/checkout-2026-09-15 --force
```

**The capacity warning.** Once the Conductor's own durable state (bounded by
`MAX_STATE_BYTES`, 1 MiB, in `pmos/conductor.py`) reaches 80% of that limit,
`pmos status` adds a `capacity_warning` field naming the current size, the
limit, and the next action: `pmos export`. Below the threshold the field is
`null`. This is the CLI-facing counterpart to `PMOSDomain.scale_warning`
documented in `docs/SCALE.md`, for the much smaller limit a `pmos` command
line user actually meets.

## Development handoff

At Gate 3, DESIGN hands a development-ready package to engineering. Fill
`templates/architecture/development-handoff.md` with links to the workspace
artifacts that carry each section's detail, then check it with:

```bash
pmos handoff --path ./products/my-product --product-id checkout --json
```

This writes two files under the workspace every time it runs, whether or not
the product is development-ready: `handoff/context-index.json`, the full
package as data, and `handoff/CONTEXT.md`, a short Markdown index of the same
data using relative links only, so the gaps are visible either way. It exits
0 when the product is development-ready and 1 when it is not; it never
modifies accepted history.

A product is development-ready only when every one of these holds at once:

- Gates 1 to 3 are approved and none of them is stale.
- The `development-handoff.md` artifact exists, with its artifact block.
- Every required section (problem; vision and strategy; outcomes and success
  measures; scope and exclusions; requirements and acceptance criteria;
  evidence and decisions; dependencies; interface and data contracts;
  unresolved risks and constraints) links at least one workspace artifact,
  or carries an `N/A because` line.
- Every linked artifact actually resolves in the workspace.

A `Gap:` line, an empty section, or a link that does not resolve blocks the
designation, and `handoff/CONTEXT.md` names which. Run on a freshly
initialized product with none of this done yet (a product named `demo` here,
to show real output), `pmos handoff --json` returned:

```json
{"context": "handoff/CONTEXT.md", "development_ready": false, "index": "handoff/context-index.json", "missing": ["development-handoff.md artifact is missing", "Gate 1 is not approved", "Gate 2 is not approved", "Gate 3 is not approved", "Section 1. Problem is missing", "Section 2. Vision and strategy is missing", "Section 3. Outcomes and success measures is missing", "Section 4. Scope and exclusions is missing", "Section 5. Requirements and acceptance criteria is missing", "Section 6. Evidence and decisions is missing", "Section 7. Dependencies is missing", "Section 8. Interface and data contracts is missing", "Section 9. Unresolved risks and constraints is missing"], "ok": false, "product_id": "demo"}
```

As with every gate approval, `development_ready` reflects local attestation,
never authenticated team approval: the package records who ran each gate and
when, and that the attestation is `local`, but it does not and cannot confirm
that actor's identity.

An answer may carry the evidence class its question asks for or a stronger
one, observed behavior being the strongest. A product keeps the contract it
started with, and `pmos status` shows its pinned and shipped bank versions
under `question_banks`. Moving a product to a newer contract is not
supported yet. A product created before the contract, or by `pmos migrate`,
keeps the one-question onboarding bank.

The runtime retains the most recent 1,024 Conductor turn records as an
idempotency window. Replaying a retained turn ID returns its original result
or a payload conflict; once a record is evicted, the request is evaluated
against the current cursor and expected revision instead of being replayed.
This bounds durable memory without allowing an old retry to bypass the current
protocol. Domain digest-only evidence follows the same fail-closed rule: use
content-backed evidence, or configure a trusted external verifier for the
digest before creating or completing a gate.

For an older file workspace, inspect before changing anything:

```bash
pmos migrate ./legacy-workspace --destination ./products/my-product --dry-run
pmos migrate ./legacy-workspace --destination ./products/my-product --product-id checkout
pmos recover ./products/my-product
pmos rollback ./products/my-product
```

Migration builds and verifies a new database beside the active runtime, makes
a SQLite backup of an existing runtime, and activates the new database with a
single filesystem replace. A durable activation journal is written before the
replace. If a process dies after replacement, `recover` verifies the journal's
hash and SQLite invariants, then finalizes the migration; if verification fails
it restores a verified backup or quarantines the unverified runtime. Rollback
uses the same two-phase journal: a process death after rollback replacement is
recovered only when the restored runtime exactly matches its recorded hash and
SQLite invariants. Recovery is idempotent and never overwrites a runtime whose
hash is not the pinned migration or rollback state. If a normal injected fault
occurs after migration replacement, the old runtime is restored synchronously
and the journal records `aborted`. `rollback` uses the recorded backup and
verifies it before activation.

`migrate`, `recover`, and `rollback` take the same destination-scoped local
advisory lock for their whole lifecycle. A concurrent lifecycle operation waits
briefly, then fails with an actionable busy error; retry it after the active
operation completes. The retained `.pmos/migration.lock` file is not a stale
lock marker: its operating-system lock is released automatically if the process
exits or crashes, so do not delete it to "unlock" a workspace.
The lifecycle also binds the lock to the original `.pmos` directory identity;
if that directory is replaced or symlinked during migration, recovery, or
rollback, the operation is refused rather than reading or writing runtime,
journal, backup, or manifest state through the replacement path. Existing
control files must be regular files, never symlinks.

The local SQLite runtime is pinned to its opened parent directory and database
inode for the Store lifetime. A pathname replacement is rejected before PM OS
performs another serialized operation. This is a same-host filesystem boundary,
not a claim of distributed or hostile-kernel storage safety.

Migration is bounded to 4,096 regular files, 16 MiB per file, 64 MiB total, and
1,024 UTF-8 path bytes. Planned files are reopened by descriptor-relative
component traversal with no-follow flags and their device, inode, and size are
checked again before and after reading; a symlink swap or file replacement is
rejected rather than imported.

Create and verify release provenance offline:

```bash
pmos provenance --path . --output docs/release/provenance.json
pmos verify --path . --provenance docs/release/provenance.json
```

The provenance file contains categories, sizes, SHA-256 hashes, schema, and a
Git source commit when available.  It contains no file contents or secrets.
Tampering, missing files, and unrecorded files fail verification.

The runtime is intentionally local and transactional.  Queue delivery is at
least once, external integrations need their adapter and outbox contracts,
and a green local verification does not substitute for human gate approval or
external CI and regulatory evidence.

Runtime skills are loaded only when the closed, shipped manifest at
`skills/runtime-manifest.json` matches every `contract.json`, `SKILL.graph.yml`,
`SKILL.md`, and template hash.  Missing, unknown, extra, symlinked, or
path-escaping assets fail closed.  Editing a skill's self-declared hashes or
risk metadata cannot approve a change; the trusted manifest must be regenerated
by the release process. The wheel includes those same manifest-bound assets,
so `SkillRegistry().load()` works from an installed distribution without the
source checkout; the isolated packaging test verifies all seven load.
