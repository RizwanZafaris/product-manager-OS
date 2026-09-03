# The Harness

This directory is an adapter over a document system. It takes three things the OS already states in prose, and makes them executable instead of advisory:

| Stated in prose | Made executable here |
|---|---|
| The router table in [../CLAUDE.md](../CLAUDE.md): which request goes to which skill, template, and read | [MANIFEST.json](MANIFEST.json), one entry per router row, addressed by a stable id |
| The tier doctrine in [../routing/README.md](../routing/README.md): how expensive a model the work deserves | [tiers.md](tiers.md) as a decision you can run, [runner.py](runner.py) as the call that honors it |
| The seven rules an agent must not break | [INVARIANTS.md](INVARIANTS.md), with every route naming the ids that bind it |

Nothing here decides anything on its own. An entry is an index into a file that already governs the work. [../tools/check_manifest.py](../tools/check_manifest.py) proves the manifest and the router table agree row for row, and fails the build when they drift.

## What the harness is not

It is not a runtime dependency. The OS is a set of documents: templates you fill, skills you follow, gates a person signs. All of that works with a text editor and a pencil, and it worked that way before this directory existed.

The harness must never become the product. The moment a template can only be filled through an adapter, or a gate can only be walked by a tool, the system has stopped being readable and started being a program you have to trust. The test for that failure is below, and you should run it.

## The deletability guarantee

`rm -rf harness/` leaves a working document system, and every shipping gate still passes with the directory removed.

Proved, not asserted. The repository was copied to a scratch directory, `harness/` was deleted in the copy, and all four gates were run there:

```
$ tar --exclude='.git' --exclude='__pycache__' -cf - . | (cd /private/tmp/deltest && tar -xf -)
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
Ran 47 tests in 0.795s
OK

$ python3 tools/graph.py --check
docs/GRAPH.md: ok (up to date, 256 files scanned)
exit 0
```

No exceptions, and no defect report attached. That is a change from the first run of this proof, and it is worth recording rather than quietly replacing. The guarantee used to hold for every file the harness owns and be violated by one file that documents it: `examples/ledgerline-harness-routing-run.md` carried three relative links into `harness/`, so deleting the directory failed the link gate and the one test that asserts the tree ships clean.

The rule that came out of that, and the one to apply to anything written from here: **a file outside this directory names a harness path in plain text, never as a link.** The example now writes `harness/runner.py`, `harness/MANIFEST.json`, and `harness/tiers.md` in backticks, and the module map in [../README.md](../README.md) names `harness/` the same way and says so in the row itself. A backticked path still tells a reader where to look and costs nothing on deletion. A link is a dependency, and the link gate is right to treat it as one.

Re-run the proof whenever a file outside this directory starts talking about the harness. It is four commands against a scratch copy, and it is the only thing standing between a stated property and a wish.

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

There is no harness database, no cache of runs, no state file under this directory. That is deliberate. A private store would break the one property that makes this system auditable: you can read everything that happened with a text editor.

| What | Where it lives |
|---|---|
| Run state and position in the loop | `products/<name>/STATE.md`, per [../os/PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md) |
| Accepted answers and the evidence ledger | The same STATE.md, append only |
| Artifacts | Filled copies of the templates the route names, inside the product workspace |
| Gate attempts | `products/<name>/gates/`, one file per attempt |
| Logs | Beside the artifact they describe, in the same stage folder, never here |

Logs are the one exception to "the harness writes nothing", and they are written next to the artifact rather than into this directory, so a document and the record of how it was produced travel together.

## Credentials

Two environment variables, `OMNIROUTE_BASE_URL` and `OMNIROUTE_API_KEY`, resolved at call time by whatever makes the call. They are never written into this repository, never printed, and never logged. An adapter may report whether a variable is set; it never reports a value. [../routing/omniroute.config.json](../routing/omniroute.config.json) names the variables and holds no key. A literal credential anywhere in the tree is a defect, and check 9 of `lint.py` scans for common key shapes, this directory included.

## Adding a task type

The router table is the source of truth and the manifest follows it. In this order:

1. **Add the router row** to the table in [../CLAUDE.md](../CLAUDE.md): what the user asks for, what to invoke, the backing templates. If no skill fits, say so in the row and name the file to read instead.
2. **Add the manifest entry** to `tasks` in [MANIFEST.json](MANIFEST.json), in the same position the row holds. Copy the row's first cell verbatim into `router_row`; that string is the join key. Fill `id`, `trigger`, `stage`, `gate`, `tier`, `skill`, `templates`, `reads`, `invariants`. Use `null` for a skill the row does not name, and `null` for both `stage` and `gate` when the output is not gated. Never invent a stage to fill a field.
3. **Run the agreement gate**: `python3 tools/check_manifest.py`. It fails on a missing path, an absolute path, a model id, a bad tier, an unknown invariant id, a dropped entry, and wrong order.
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
