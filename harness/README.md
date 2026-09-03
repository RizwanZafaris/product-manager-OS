# The Harness

This directory is a legacy route adapter over a document system. It takes three things the OS already states in prose, and makes them executable instead of advisory. The durable local runtime now lives separately in `pmos/`; this harness remains useful for route-manifest compatibility and adapter checks, but its state-free limits are not limits of `pmos/`.

| Stated in prose | Made executable here |
|---|---|
| The router table in [../CLAUDE.md](../CLAUDE.md): which request goes to which skill, template, and read | [MANIFEST.json](MANIFEST.json), one entry per router row, addressed by a stable id |
| The tier doctrine in [../routing/README.md](../routing/README.md): how expensive a model the work deserves | [tiers.md](tiers.md) as a decision you can run, [runner.py](runner.py) as the call that honors it |
| The seven rules an agent must not break | [INVARIANTS.md](INVARIANTS.md), with every route naming the ids that bind it, and the four that bind every route always listed first on all 41 |

Nothing here decides anything on its own. An entry is an index into a file that already governs the work. [../tools/check_manifest.py](../tools/check_manifest.py) runs eight checks and proves the manifest and the router table agree, row for row and across all three of the table's columns, and fails the build when they drift. Column agreement is the half that used to be assumed: the skill a router row names has to be that entry's own skill, and a template named in a row has to be one the entry declares, so a row can no longer point somewhere the manifest does not.

## Maturity, stated separately from the document system's

The document layers and this directory are not at the same level of
readiness, and a single version number across both hides that. So it is
written here instead.

The templates, the knowledge cards, the frameworks and the gates are the
mature part. They work with a text editor, they have no runtime, and the
failure mode of a mistake in them is a document that argues badly, which a
reader can see and fix.

This directory is the legacy adapter part. It is a real runner with real
tests, and as of the audit it closed in this release, it agrees with the
initializer about where every artifact lands, rewrites the links in a copy
it places, distinguishes the four kinds of route rather than treating all
forty-one as document producers, rolls a failed multi-file commit back,
and serializes journal writes under a lock. Those are the things that were
wrong and are now right, and each one has a regression test that fails
against the behaviour it replaced.

What this directory is still not, stated so nobody has to discover it in production:

| Not this | Why not, concretely |
|---|---|
| The `pmos` job queue | A deferred legacy route records a job and exits; it does not run the Store's leased queue, retry state, fencing, or cancellation lifecycle. |
| A cross-machine team system | The harness lock is local filesystem coordination. Use `pmos.domain` and a persistence integration for local team/approval/portfolio policy; neither substitute for a distributed service. |
| External governance evidence | A legacy document gate is still a human workflow. `pmos` can hash local evidence and invalidate changed approvals, but neither layer can self-attest external human, regulatory, or release approval. |
| A portfolio engine | STATE.md is one document workspace. The local domain runtime models initiatives, dependencies, and capacity separately; it is not a hosted portfolio product. |
| Release reproducibility by itself | The legacy route does not create a complete run record. `pmos` can produce local provenance and deterministic state evidence, but a published artifact and exact hosted CI remain external gates. |

Use the harness for document-route compatibility and drafting with a person reading the output. Use `pmos` when the local operation needs durable queue, memory, policy, approval, portfolio, recovery, or provenance semantics. Neither is permission to use output as external regulatory evidence or to claim a hosted team system.

## What the harness is not

It is not a runtime dependency. The OS is a set of documents: templates you fill, skills you follow, gates a person signs. All of that works with a text editor and a pencil, and it worked that way before this directory existed.

The harness must never become the product. The moment a template can only be filled through an adapter, or a gate can only be walked by a tool, the system has stopped being readable and started being a program you have to trust. The test for that failure is below, and you should run it.

## The deletability guarantee

`rm -rf harness/` leaves a working document system, and all four shipping gates now pass on the deleted tree. The guarantee was earned rather than inherited: the same proof failed earlier on the same day, for a reason this section names, and both runs are kept below. A record of a property that once failed and was then fixed is worth more than a clean claim, because it tells you what breaks it.

### The run that failed

The repository was copied to a scratch directory, `harness/` was deleted in the copy, and all four gates were run there on 2026-09-03:

```
$ tar --exclude='.git' --exclude='__pycache__' -cf - . | (cd /private/tmp/deltest && tar -xf -)
$ cd /private/tmp/deltest && rm -rf harness

$ python3 lint.py --os
2 problem(s). The gate failed, which is the point of having one.
AGENTS.md:11: LINK relative link harness/INVARIANTS.md does not resolve.
AGENTS.md:18: LINK relative link harness/MANIFEST.json does not resolve.
exit 1

$ python3 tools/check_manifest.py
harness/: absent, nothing to check. The harness is deletable, so this gate
reports ok instead of failing. A harness/ that exists without MANIFEST.json
or INVARIANTS.md is a broken contract and still fails.
exit 0

$ python3 test_lint.py
Ran 78 tests in 1.793s
FAILED (failures=1)
  test_the_real_tree_passes_the_shipping_gate: the two links above

$ python3 tools/graph.py --check
docs/GRAPH.md: ok (up to date, 256 files scanned)
exit 0
```

Nothing under `harness/` caused that. `AGENTS.md` named two harness paths as markdown links, at its lines 11 and 18, so deleting the directory left two dangling links and the link gate reported them. One file outside this directory was enough to break the property for the whole tree.

### What changed between the two runs

Those two references in `AGENTS.md` are backticked paths now instead of links, and that file says why in the same paragraph. No gate was relaxed, no check was exempted, and no file under `harness/` moved. That is the whole delta.

### The run that passes

Same procedure, same scratch directory, re-run on 2026-09-03 after that edit:

```
$ tar --exclude='.git' --exclude='__pycache__' --exclude='.pytest_cache' -cf - . | (cd /private/tmp/deltest && tar -xf -)
$ cd /private/tmp/deltest && rm -rf harness

$ python3 lint.py --os
.: ok (OS tree mode, 11 checks)
exit 0

$ python3 tools/check_manifest.py
harness/: absent, nothing to check. The harness is deletable, so this gate
reports ok instead of failing. A harness/ that exists without MANIFEST.json
or INVARIANTS.md is a broken contract and still fails.
exit 0

$ python3 test_lint.py
Ran 108 tests in 1.944s
OK

$ python3 tools/graph.py --check
docs/GRAPH.md: ok (up to date, 256 files scanned)
exit 0
```

What that does and does not mean. The document system was untouched across both runs: every template still fills, every skill still reads as a procedure, every gate is still signed by a person, and nothing under `harness/` was ever a source of truth. What broke the first time was the gate, and it broke in exactly the way this section has broken before, when a file outside the directory started naming a harness path as a link.

The rule, and it is the whole guarantee: **a file outside this directory names a harness path in plain text, in backticks, never as a link.** `examples/ledgerline-harness-routing-run.md` follows it, the module map in [../README.md](../README.md) follows it and says so in the row itself, and `AGENTS.md` follows it now. A backticked path still tells a reader where to look and costs nothing on deletion. A link is a dependency, and the link gate is right to treat it as one.

Re-run the proof whenever a file outside this directory starts talking about the harness. It is four commands against a scratch copy, and it is the only thing standing between a stated property and a wish. Nothing enforces the backtick rule except attention, attention has now failed it twice, and that is the argument for running the proof rather than trusting the sentence above it.

One wiring change was needed to earn the guarantee. `tools/check_manifest.py` used to report two missing files and exit 1 on a tree with no harness, which would have failed CI for doing the supported thing. It now reports ok when `harness/` is absent, and still fails when `harness/` exists without its contract files. Deletion and a broken contract are different events and the checker now tells them apart.

## Three checks, and why a green gate is not a good document

A harness makes one mistake easy: believing that a green checker means a good document. The belief is more dangerous here than in a repository with no checker, because now there is a number to point at. Keep these three separate and run them in this order.

| Check | What it proves | What it cannot see |
|---|---|---|
| `python3 lint.py --os`, plus [../tools/check_manifest.py](../tools/check_manifest.py) | The tree is structurally valid: sections present, links resolve, no banned strings, no secrets, manifest and router table agree | Whether a single sentence in it is true, testable, or worth writing |
| [../skills/spec-review/SKILL.md](../skills/spec-review/SKILL.md) | The prose is testable: every requirement has a condition, an expected result, and a threshold a test could report as failing | Whether the requirement is the right one to build |
| The human gate in [../os/STAGE-GATES.md](../os/STAGE-GATES.md) | The thinking is sound, and a named person accepts the consequences | Nothing. It is the last check, which is why a person owns it |

A structurally perfect, logically empty document passes the first and must fail the other two. "The system should feel trustworthy" clears every check the linter has. It carries no unit, so spec review blocks it. It commits nobody to anything, so the gate refuses it. A structural gate is not a quality gate, and the harness is the layer most likely to confuse the two, because the harness is the layer that prints "ok".

## The harness stores nothing of its own

There is no harness database, no cache of runs, no state file under this directory. That is deliberate for this legacy adapter. It does not mean the OS has no runtime state: `pmos.Store` keeps transactional local state in a workspace's `.pmos/runtime.sqlite`, with integrity verification, full snapshots, backup/restore, a leased queue, and scoped memory streams.

| What | Where it lives |
|---|---|
| Run state and position in the loop | `products/<name>/STATE.md`, per [../os/PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md) |
| Accepted answers and the evidence ledger | The same STATE.md, append only |
| Artifacts | Filled copies of the templates the route names, inside the product workspace |
| Gate attempts | `products/<name>/gates/`, one file per attempt |
| Logs | Beside the artifact they describe, in the same stage folder, never here |

Logs are the one exception to "the harness writes nothing", and they are written next to the artifact rather than into this directory, so a document and the record of how it was produced travel together. The local runtime has a different, explicit storage contract; see [../docs/RUNTIME-QUICKSTART.md](../docs/RUNTIME-QUICKSTART.md).

## Credentials

The legacy harness uses `OMNIROUTE_BASE_URL` and the config's API-key variable (`OMNIROUTE_API_KEY` unless a deployment changes it), resolved at call time. The local OpenRouter adapter separately uses `OPENROUTER_API_KEY` (or a configured environment-variable name), also only at call time. Keys are never written into this repository or the local Store. An adapter may report whether a variable is set; it never reports a value. [../routing/omniroute.config.json](../routing/omniroute.config.json) names variables and holds no key. A literal credential anywhere in the tree is a defect, and the security gate scans for credential shapes with no file exempted, this directory included.

Never printed and never logged is enforced in one place rather than promised at each sink. `runner.py` resolves the credential once and registers that exact value with a single redactor used by standard output, the run log, the artifact's face, and the journal row; masking is longest-first and has no length floor, because a short credential is still a credential. Printed URLs drop userinfo and mask query values, and a failed call records a sanitized status descriptor rather than the gateway's own response body, so a hostile or noisy gateway cannot write its text into your files. The full picture, including the write boundary, is in [../SECURITY.md](../SECURITY.md).

## Adding a task type

The router table is the source of truth and the manifest follows it. In this order:

1. **Add the router row** to the table in [../CLAUDE.md](../CLAUDE.md): what the user asks for, what to invoke, the backing templates. If no skill fits, say so in the row and name the file to read instead.
2. **Add the manifest entry** to `tasks` in [MANIFEST.json](MANIFEST.json), in the same position the row holds. Copy the row's first cell verbatim into `router_row`; that string is the join key. Fill `id`, `trigger`, `stage`, `gate`, `tier`, `skill`, `templates`, `reads`, `invariants`. Use `null` for a skill the row does not name, and `null` for both `stage` and `gate` when the output is not gated. Never invent a stage to fill a field.
3. **Run the agreement gate**: `python3 tools/check_manifest.py`. It fails on a missing path, an absolute path or one that climbs or passes through a symlink, a model id where a tier name belongs, a bad tier, stage, or gate, an unknown invariant id, an entry that omits one of the four universal ids, a dropped entry, and wrong order. It also reads the router table itself: a row that does not hold exactly three cells fails rather than being skipped, a trigger phrase claimed twice fails, and the Invoke and Backing-templates cells have to name this entry's own skill and templates.
4. **Regenerate the generated adapter**: `python3 harness/adapters/claude-code/generate.py`, then `--check` to confirm no drift.
5. **Re-run the adapter selftest**: `python3 harness/adapters/desktop/selftest.py`.
6. **Run the shipping gate**: `python3 lint.py --os`.

If a request matches no row, the work is queued and the table is amended. It is never guessed at. A guessed route sets a precedent nobody reviewed, and the next request of that shape inherits it.

## How the three adapters stay in sync

One manifest, three faces. Two read it at run time and one is generated from it, so none of them holds a second copy of the routing.

```
             ../CLAUDE.md  (router table, what a person reads)
                   |
                   |  tools/check_manifest.py proves these two agree
                   v
             MANIFEST.json  (41 entries, one per row, in router order)
                   |
      +------------+------------+
      |            |            |
   read at      read at     generated
   run time     run time    from it
      |            |            |
   adapters/    adapters/    adapters/
     cli        desktop      claude-code
```

| Adapter | How it uses the manifest | Kept honest by |
|---|---|---|
| [adapters/cli](adapters/cli/pmos.py) | Reads MANIFEST.json on every invocation. Nothing is generated, so it cannot drift | `check_manifest.py`, plus its own unresolvable-request exit code |
| [adapters/desktop](adapters/desktop/README.md) | Builds its tool list from the manifest at server start, one tool per entry, in router order | `adapters/desktop/selftest.py`, which asserts count, order, uniqueness, and schema shape |
| [adapters/claude-code](adapters/claude-code/README.md) | Generated files: one command per entry, written by `generate.py` | `generate.py --check`, which exits 1 on a hand-edit, a deleted file, or an invented command |

Add a route and all three change from one edit to the manifest. Two of them need no build step at all; the third needs one command and has a checker that catches you forgetting it.

## What this layer refuses

| Owned here | Not owned here |
|---|---|
| The route ids, and that each names the invariants that bind it | The gate contents, which stay in [../os/STAGE-GATES.md](../os/STAGE-GATES.md) |
| Turning the tier doctrine into a call that sends the right headers | The tier to model mapping, which is [../routing/omniroute.config.json](../routing/omniroute.config.json) and nowhere else |
| Proving the manifest and the router table agree | Whether the routed work is any good. See the three checks above |
| Halting and queueing when a rule would otherwise break | The channel the queue is read in. That is the adapter's |

No adapter signs a gate, sends anything, or judges quality. It resolves a request into a plan, names the files, prints the rules, and stops. A person does the rest, which is the whole design.
