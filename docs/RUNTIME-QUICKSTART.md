# PMOS runtime quickstart

Product Manager OS is usable as a document tree, and its optional local
runtime is standard-library Python.  It does not require an API key, a hosted
service, or a model.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --no-index .
pmos init --path ./my-product --product-id checkout
pmos status --path ./my-product
pmos verify --path ./my-product
```

For a release-style packaging check, use a normal isolated PEP 517 build:
`python -m pip wheel --no-index --no-deps --wheel-dir /tmp/pmos-wheels .`.
The project uses a repository-local, standard-library PEP 517 backend, so no
runtime dependencies are downloaded or required.

`init` creates `.pmos/runtime.sqlite`, creates the product through the public
Store API, and renders a deterministic first onboarding question through the
public Conductor API.  It never invents a customer answer or gate proof. Add
`--json` before or after the command for automation:

```bash
pmos --json status --path ./my-product
```

Continue only with evidence you actually collected. The revision and question
ID come from `init`/`status`; the evidence fields are checked by the conductor:

```bash
pmos answer --path ./my-product --product-id checkout \
  --question-id first-outcome --answer "<your observed outcome>" \
  --evidence '{"class":"observed_behavior","source":"<interview or artifact>","date":"<YYYY-MM-DD>","location":"<where observed>"}' \
  --expected-revision 0:- --turn-id answer-001 --json

pmos gate --path ./my-product --product-id checkout --bank-id onboarding \
  --evidence '{"source":"approval/onboarding.txt","source_sha256":"<sha256-of-that-file>","actor_id":"local-reviewer","requester_id":"local-operator","decision":"approved","approved_at":"<UTC-YYYY-MM-DDTHH:MM:SSZ>"}' \
  --expected-revision '<revision returned by answer>' --turn-id gate-001 --json
```

Insufficient evidence, a stale revision, a repeated turn ID, or an unknown
question is rejected and leaves the prior state intact. Replace every angle-
bracket value with a real, traceable source; the source must be a regular,
non-symlink file inside the workspace (but outside `.pmos/`) and its digest
must match. The pinned onboarding policy requires `local-reviewer` and rejects
self-approval where requester and reviewer are the same. Placeholders are intentionally not
accepted as evidence by the runtime.

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
pmos migrate ./legacy-workspace --destination ./my-product --dry-run
pmos migrate ./legacy-workspace --destination ./my-product --product-id checkout
pmos recover ./my-product
pmos rollback ./my-product
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
