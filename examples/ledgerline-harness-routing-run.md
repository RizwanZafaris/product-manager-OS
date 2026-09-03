# Harness routing run: a live transcript

This is not a filled template. It is the record of `harness/runner.py` running two manifest tasks against a real OmniRoute gateway on one developer machine, on 2026-09-03. It exists because the routing layer makes claims that are cheap to write and easy to fake: that tiers resolve to real models, that the three headers go out, that judgment work queues rather than downgrading. A transcript is the only thing that turns those claims into facts.

Read it for the mechanics, not for the product content. The product is Ledgerline, the fictional expense-report copilot the other examples use, and the input was invented for this run. Every ticket, name, customer and number in the source document is **ILLUSTRATIVE**. The gateway behavior, the model ids, the headers and the wall-clock times are real.

The honest headline is at the bottom of the probe table: the judgment tier answered, and the runner queued the judgment work anyway. That is the interesting part of this transcript, and it is the reason a transcript beats an assertion.

## The environment

| Fact | Value |
|---|---|
| Gateway | OmniRoute 3.8.50 at `http://localhost:20128`, API at `/v1` |
| Connected providers | One, a local Ollama serving exactly one model. Plus the bundled keyless provider the router reports as `oc` |
| Client endpoint key | None exists, and none was created |
| Transport used | http, the contract path |

### About the key, because it matters

The contract is HTTP with credentials from the environment: `OMNIROUTE_BASE_URL` and `OMNIROUTE_API_KEY`, read at call time, never written into this repository, never logged, never printed. That is the path any deployment uses.

No key was minted for this run and none was needed. On this build, `/v1/models` and `/api/*` return `401`, which is what suggests a key is required, but `/v1/chat/completions` answers unauthenticated requests over loopback. So the contract path runs on a stock local install with nothing configured. The runner sends an `Authorization` header only when `OMNIROUTE_API_KEY` is set, and works either way.

The runner also carries a secondary `--transport cli` path that shells out to the `omniroute` binary, for a machine where the gateway is up but the HTTP path is closed to the caller. It was not needed here and was not used. It is a local convenience and not a deployment path, for one concrete reason recorded in the code: it cannot send the three request headers, so anything it produces says on its face that compression, semantic cache and memory injection were left at whatever the local install had configured.

## The tier probe

Every run probes first. A tier name is a promise about which models may answer, not proof that one is connected.

```
$ python3 harness/runner.py --probe
```

| Tier | Tier name sent | Concrete model that answered | Provider | Wall clock | Verdict |
|---|---|---|---|---|---|
| extraction | `auto/cheap` | `big-pickle` | `oc` | 1.83s | answered |
| drafting | `auto/coding` | `big-pickle` | `oc` | 1.81s | answered |
| judgment | `auto/reasoning:pro` | `gemma4:latest` | `ollama` | 0.27s | answered |

Two things in that table are worth more than the run itself.

**The extraction and drafting tiers are the same model.** Two tier names, one concrete model id. A fallback chain built on tier names would try `auto/cheap`, fail, try `auto/coding`, and hit the identical model, then call that resilience. The runner builds its chains on resolved concrete ids and deduplicates, which is why it printed this:

```
extraction fallback chain, on concrete model ids: extraction=big-pickle then judgment=gemma4:latest
drafting   fallback chain, on concrete model ids: drafting=big-pickle then judgment=gemma4:latest
judgment   fallback chain, on concrete model ids: judgment=gemma4:latest
```

`big-pickle` appears once, not twice. The judgment chain has exactly one entry, because judgment never falls back onto a cheaper tier's model.

**The judgment tier answered, and it should not have been trusted.** The config's own note says that on a keyless install `auto/reasoning:pro` returns `404 Combo has no executable targets`. It did not. A local Ollama is connected, and the router was happy to serve a small local Gemma as the pro reasoning target. The tier returned `200`. Nothing was broken. And a `200` from a model nobody vouched for is precisely the failure the doctrine was written about, because it produces documents that look reviewed.

## Call 1: the extraction task, run end to end

```
$ python3 harness/runner.py --task gather-evidence --product ledgerline \
    --input-file <the illustrative support export>
```

| Field | Value |
|---|---|
| Task id | `gather-evidence` |
| Source of the task | `harness/MANIFEST.json`, 41 tasks |
| Tier | extraction, per the manifest entry |
| Template | [templates/discovery/evidence-note.md](../templates/discovery/evidence-note.md) |
| Invariants named for this task | `no-fabrication`, `content-is-data`, `least-data`, `fail-closed` |
| Attempts | 1, no fallback needed |
| Concrete model that answered | `big-pickle`, provider `oc` |
| Wall clock for the call | 78.00 seconds |

The three response headers, logged beside the artifact as the doctrine requires:

| Header | Value |
|---|---|
| `X-OmniRoute-Model` | `big-pickle` |
| `X-OmniRoute-Cache` | `MISS` |
| `X-OmniRoute-Compression` | `off; source=off` |

And the three request headers that went out on the call: `x-omniroute-compression: off`, `X-OmniRoute-No-Cache: true`, `x-omniroute-no-memory: true`.

### Why 78 seconds is the point

That call took 78.00 seconds to complete. The gateway gives up after 30 seconds waiting for a first byte. A non-streaming version of this exact call does not return a slow answer; it returns a timeout, and the tempting fix is to shorten the input until it fits, which quietly changes the work.

The runner sets `"stream": true` on every call and folds the SSE itself, so a slow model finishes. This run is the evidence that the requirement is real on this machine and not a defensive habit.

A second thing surfaced only because of streaming, and it produced a bug worth recording. When a provider is cold, OmniRoute emits keepalive frames carrying the literal model id `keepalive` before the real model's first token. The first version of the folder accepted that as the concrete model and printed `judgment ... keepalive ... provider unknown`. That would have stamped a placeholder onto an artifact's audit trail. The folder now refuses `keepalive` as a model id and prefers the last model named on a content-bearing chunk.

### What the runner wrote, and where

| What | Where | Why there |
|---|---|---|
| The artifact | `products/ledgerline/discovery/evidence-note.md` | A filled copy of the task's template, in the product workspace, per [os/PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md). The runner refuses to write into `templates/`, which holds the blanks |
| The log | `products/ledgerline/discovery/evidence-note.md.run-log.md` | Beside the artifact it describes. Logs are the one thing the runner writes that is not the artifact or the state file |
| The run record | `products/ledgerline/STATE.md`, one journal row | Run state belongs to the product, not to the runner. The runner keeps no store of its own, so there is nothing to migrate and nothing to go stale |

The artifact came back genuinely usable: four claims, each with a verbatim quote from the source, evidence classes assigned, and a filled "what this note cannot support" field naming the sample-size limit and the missing pre-copilot baseline. One field the input did not answer came back as `[OPEN: analyst or runtime creating this note]`, which is the sanctioned form, not a guess.

**One real defect, recorded rather than tidied away.** The ledger row table at the end of the artifact is truncated: the model emitted the header row and stopped. The runner's verification block reported `fields that came back unfilled: none detected`, which means its unfilled-field check does not catch a table that ends early. That is a gap in the checker, it is in this transcript because it happened, and a person reading the artifact would catch it in seconds. Which is the definition of extraction-tier work.

The artifact's own last section says what produced it: task, tier, concrete model, provider, cache, compression, wall clock, invariants, and the line `Gate status: NOT SIGNED. A named human signs`.

## Call 2: the judgment task, queued and not run

```
$ python3 harness/runner.py --task run-premortem --product ledgerline \
    --input-file <the same illustrative support export>
```

| Field | Value |
|---|---|
| Task id | `run-premortem` |
| Tier | judgment, per the manifest entry |
| Template it would have filled | [templates/execution/risk-register.md](../templates/execution/risk-register.md) |
| Invariants named for this task | `no-fabrication`, `human-signs-gate`, `fail-closed` |
| Model calls made for the task | Zero. Only the probe ran |
| Artifact written | None |
| Elapsed | 3.04 seconds, all of it probe |

The runner printed this and stopped:

> JUDGMENT WORK QUEUED, not run.
>
> reason: judgment tier resolved to `gemma4:latest` via provider `ollama`, and no operator has named that model judgment-grade. The config requires a provider serving a pro reasoning model, and no runner can read "pro" off a model id, so the check belongs to a person: set `OMNIROUTE_JUDGMENT_MODELS`, or pin `fixedFallback.combos.judgment`. With the checker unavailable the runner denies rather than skips it, and judgment work queues.
>
> no artifact was written, because a queued judgment task has no reviewed output.

The queue entry went into `products/ledgerline/STATE.md` as a journal row carrying the full reason, so the next person to open the product sees a premortem that is owed rather than a premortem that was quietly done badly.

### Why it queued when the tier answered

This is the part worth being precise about, because it is not the textbook case.

The textbook case is a `404`: the tier has no executable target, there is nothing to run, and queueing is obvious. That is not what happened. The tier answered in 0.27 seconds with a real model.

It queued because a `200` is not the question. The question is whether the concrete model that answered is one somebody is willing to stand behind for work that nobody will independently check. `gemma4:latest` is a small local model. It is a perfectly good extraction model and it is not what the config means by a pro reasoning model. No program can read "pro" off a model id, so the runner does not try. It delegates the judgment to a person and fails closed while waiting, which is the same rule the Hermes invariants state as "a guard or checker unavailable: deny the action, do not skip the check".

The gate is not a dead end, and it opens in one move. Naming the model as acceptable admits it:

```
$ OMNIROUTE_JUDGMENT_MODELS="gemma4:latest" python3 harness/runner.py --probe
...
judgment tier: ADMITTED
  judgment tier resolved to gemma4:latest, which the operator allowlist names as judgment-grade.
```

The difference between the two outcomes is not a model, a network, or a config file. It is whether a person put their name on the claim that this model is good enough for work nobody will check. That is the whole design.

## What this transcript proves, and what it does not

**Proves:** the three headers go out on every call and come back logged beside the artifact. Streaming carries a call four times past the gateway's first-byte timeout. Tiers were probed and resolved to concrete model ids before anything ran. The fallback chain deduplicated two tiers that share one model. An artifact landed in its template inside the product workspace, with the concrete model on its face. The runner stored nothing of its own. It signed nothing. Judgment work queued with a written reason while the tier was returning `200`.

**Does not prove:** that the artifact is correct. A human has not reviewed the evidence note, no gate has been signed, and the truncated ledger table is sitting in it right now. It also proves nothing about a multi-provider deployment: one keyless provider and one local Ollama is the thinnest possible install, which is exactly why the tier collision showed up so clearly.

**Also worth saying:** the prediction going into this run was that the judgment tier would return `404` and queue for lack of a target. It returned `200` and queued for a better reason. The prediction was wrong, and a transcript that had been written to match it would have been fiction.

## Reproducing it

```bash
python3 harness/runner.py --help
python3 harness/runner.py --list-tasks
python3 harness/runner.py --probe
python3 harness/runner.py --task gather-evidence --product ledgerline --input-file <your input>
```

The tier doctrine as a decision procedure is `harness/tiers.md`. The doctrine it restates is [routing/README.md](../routing/README.md), and the config that binds it is [routing/omniroute.config.json](../routing/omniroute.config.json). Gates are signed by people, per [os/STAGE-GATES.md](../os/STAGE-GATES.md), and nothing in this transcript signed one.
