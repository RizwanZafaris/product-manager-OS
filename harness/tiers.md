# Tiers: the routing decision, as a procedure

The doctrine lives in [routing/README.md](../routing/README.md) and the config that binds it is [routing/omniroute.config.json](../routing/omniroute.config.json). This file is neither. It is the same doctrine turned into a decision you can execute at the end of a long day, when you have a task in front of you and no appetite for a principle.

Three tiers. You pick one by answering one question about the output, not about the task.

## The one question

**If this output is wrong, what catches it, and when?**

That is the whole rule. Everything below is scaffolding for people who do not believe it yet.

- Something mechanical catches it, right now: a checker, a diff, a template field list, your own eyes in ten seconds. That is **extraction**.
- A human catches it, in review, before anyone acts on it. That is **drafting**.
- Nothing catches it until someone has already relied on it. That is **judgment**.

Notice what the question does not ask. It does not ask how hard the task feels, how long the input is, or how clever the output needs to sound. Feel is a bad proxy and it is biased toward the expensive tier every single time.

## The procedure

Run these in order and stop at the first yes.

1. **Is the answer checkable against the input?** Could you, or a script, hold the output next to the source and say yes or no without needing an opinion? Pull fields from a document, normalize a backlog, tag sources, convert a format, check a draft against a template's field list. Yes: **extraction**. Stop.
2. **Is the output a first draft of a structured artifact that a named human will review before it counts?** Fill one template from supplied evidence, write an ADR, produce a diagram as code, restructure a document without changing its claims. Yes: **drafting**. Stop.
3. **Will a person act on this, or sign it, without an independent check?** A prioritization call, a premortem, a red team pass, a regulatory gap check, a gate review, anything going out under someone's own name. Yes: **judgment**. Stop.
4. **Still unsure?** Then the task is more than one task. Go to the section on chains below. Do not resolve your uncertainty by picking judgment.

## The three tiers, and the tell for each misroute

| Tier | Config name | The test it passes | The tell you routed here wrongly |
|---|---|---|---|
| extraction | `auto/cheap` | A wrong answer is caught mechanically, before anyone relies on it | Your reviewer keeps rewriting the substance rather than the wording. You are asking a lookup tier to weigh things |
| drafting | `auto/coding` | A wrong answer is caught by a human in review, and review is actually happening | Reviews come back clean every time. Either the work was extraction, or nobody is really reading it |
| judgment | `auto/reasoning:pro` | A wrong answer survives until someone acts on it | Your monthly spend is judgment-heavy and your queue holds extraction work. You routed by feel |

## Chains split by tier

A task that spans tiers runs as separate calls, one per tier. Not one call on the judgment tier because the judgment tier is the smartest.

Extract, then draft, then judge, is three calls with three inputs. It is not a more expensive version of one call; it is a different thing. One judgment-tier call does all three at the top price and then hides which step introduced the error when the output turns out wrong. You get a document you cannot debug.

The worked example in [agents/hermes-agent.md](../agents/hermes-agent.md) shows the split on a real request: extract the source into a record, draft from the record plus the canonical facts, then judge the draft because a person will send it. Three calls, three tiers, one queue entry.

**The tell that you failed to split:** you cannot say which call produced a given sentence. If the answer to "where did this number come from" is "the model", the chain was never split.

## Judgment work queues, it never downgrades

This is rule 3 of the doctrine and the one people break under deadline pressure.

When the judgment tier is capped, down, or untrustworthy, judgment work **waits**. It does not quietly move to a cheaper tier. A premortem rerouted to the cheap tier produces a document that looks reviewed and is not, and that is strictly worse than a late one: the lateness is visible and the fake review is not.

The config sets this as `limits.onCapReached: halt-tier-and-queue`. [runner.py](runner.py) enforces it, and queues judgment work when any of these hold:

| Condition | Why it queues |
|---|---|
| The judgment tier has no executable target | Nothing to run. The gateway answers `Combo has no executable targets` |
| Its concrete model is the same concrete model a cheaper tier resolved to | The tier name promised something the gateway cannot deliver. Running here is the silent downgrade, wearing a judgment label |
| No operator has named the resolved model judgment-grade | The config requires a provider serving a pro reasoning model. No program can read "pro" off a model id, so a person names the model, through `OMNIROUTE_JUDGMENT_MODELS` or a pinned `fixedFallback.combos.judgment`. With nobody having named it, the checker is unavailable, and fail-closed means deny, not skip |
| `fixedFallback` is on and the model is not in its judgment combo | The deployment asked to know exactly which model signs its artifacts. Honor that |
| The answering model is not the model that was certified | The response header naming the model came back with a different id, or with no id at all. The run did not happen on the model the artifact would claim, so there is nothing to write. It queues without trying the next link in the chain, because a gateway that reroutes one named model reroutes the next one too |
| The daily spend cap is reached | Read from the variable `limits.dailySpendCapUsdEnv` names, with spend to date from `OMNIROUTE_DAILY_SPEND_USD`, and checked before the probe so a capped run spends nothing. At or over the cap the work queues and that is terminal |
| A cap is set and no meter reports spend | An unavailable checker. Fail-closed answers that by queueing, never by running and hoping |
| A call's reservation would pass the daily or task cap | Every call first reserves the most it could bill in the shared ledger at its tier's price ceiling, across processes, so two runs cannot both take the last allowance |
| An earlier call's cost is unknown | Its full reservation stays charged, and new reservations in its scopes queue until someone reconciles it with the billed amount: `python3 -m pmos.spend status` lists them, and `python3 -m pmos.spend reconcile <key> <usd> <evidence>` clears one |
| A cap is in force and the tier has no price ceiling | The most the call could bill is unknown, so nothing can be reserved; set `tiers.<tier>.priceCeilingUsdPerMTok` |

The spend rows apply to every tier, not only judgment. The gateway's daily figure can include calls the ledger already recorded, so the same spend may be counted twice; that errs toward stopping early, never toward overspending.

## Reading what the ledger actually spent

`python3 -m pmos.spend status` lists open and unresolved reservations, but it does not summarize what happened. For that, `python3 tools/usage_report.py` reads the same ledger and reports usage grouped by operation, resolved model and provider, task id, and cache disposition, with a denominator of completed calls over attempted calls and a separate count of quality failures (a completed call whose reply was not usable) in every group. Pass `--ledger PATH` for a ledger other than the default, `--json` for one JSON object instead of text, and `--task-suite FILE` to overlay a fixed set of tasks the report should cover, including any task that runs on a subscription tier the ledger never sees.

Every row also carries a cost certainty, taken straight from the reservation's own state so the ledger and the report can never disagree about the words:

| State | Cost certainty label | What it means |
|---|---|---|
| `settled` | billed | The call finished and a real cost came back |
| `open` | reserved worst case, not yet settled | The call has not settled yet; this is the most it could cost, not what it did cost |
| `unknown` | unknown | The call finished with no reported cost; the full reservation stays charged until someone reconciles it |

A tier billed through a subscription rather than a per-call price never opens a spend session at all (`transport_call` in `harness/runner.py` skips the ledger when no cap is in force), so the ledger has no rows for it. The report never turns that absence into a $0.00 figure: a `--task-suite` entry marked `"metered": false` shows its cost as the literal string `unavailable`, and its completed/success facts come only from what the suite file states.

`python3 tools/usage_report.py --compare BEFORE AFTER` diffs two snapshots, each a ledger file or a JSON report this tool already wrote. No token or cost savings claim is valid from this output unless both sides were built against the same `--task-suite`: the compare output says `fixed_suite_match: true` only when both sides name exactly the same fixed set of tasks, `false` when they cover different work, and reports it as unavailable when either side carries no task suite at all. A delta printed under any other condition describes different work, not a saving.

There is one sanctioned way to run judgment work on a cheaper model, and it is loud: set `tiers.judgment.keylessFallback.enabled` to true in the config. It is off by default. Every artifact produced under it carries the line `judgment tier: degraded, reviewed by a person before use` on its face, because an artifact that does not say it was degraded will be read as one that was not.

## A tier name is not a model

`auto/cheap` is a promise about which models may answer. It is not proof that one is connected, and it is not proof that the model behind it is the model you had in mind last month.

Two habits follow, and both are cheap:

1. **Probe before a run that matters.** `python3 harness/runner.py --probe` prints the concrete model that answered each tier. On a fresh install all three tier names commonly resolve to one free model, which means your carefully tiered pipeline is one model wearing three hats.
2. **Record the concrete model on the artifact.** Not the tier name. Six weeks later, "produced on the judgment tier" tells a reader nothing they can verify, and "produced by model X, provider Y, cache MISS" tells them everything.

The same point has a sharp edge for fallback: build a fallback chain on **resolved concrete model ids**, never on tier names. A chain of three tier names that all resolve to one model retries that one model three times and calls it resilience.

**Certifying at probe time proves nothing on its own.** If the probe resolves a concrete id and the real call then sends the tier alias again, the gateway is free to answer from a cheaper model and the artifact still carries the certified id. So the runner does both halves. Every request it makes, the task call and every condense chunk on the retry path, targets the concrete id it certified. Every response is held to it: the model header has to come back naming that same id, and a different id or a missing header queues the work instead of writing a document. This is fail-closed and it has a cost worth knowing before you meet it: a gateway that decorates or namespaces the id, or that omits the header, will refuse every run rather than mislabel one. The same applies to the terminal-event rule below. Both are deliberate, and both name the gateway as the thing to fix in the message they print.

## What the runner refuses to write

Tier discipline decides who answers. These decide whether the answer is allowed to become a file, and every one of them is a refusal rather than a warning.

| Refusal | The failure it exists for |
|---|---|
| A reply with no text, no terminal event, or a `finish_reason` other than `stop` | A truncated document looks finished. That is the whole problem: the reader cannot see the sentence that never arrived |
| A document whose headings, table columns, or table rows do not match the template it was meant to fill | The second check, and the one that does not trust the gateway. A table that comes back as a bare header, or a document ending mid-row, fails here even when the stream said it finished |
| An existing artifact or log, unless you pass `--update` | A rerun over finished work is usually a mistake, and the cheap version of that mistake is a refusal with a flag named in it |
| A `--product` value that is not a plain slug landing directly under `products/` | Checked before any model call, so a run that could not land safely never spends one |
| A route with more than one template and no `--template` | Picking the first silently turns a request for one document into another. Exit non-zero and list the choices |
| Condensing the template on a large input | Only evidence is condensed. A condensed template is a different form with different fields, and the extraction tier is exempt from condensing altogether because copying text exactly is the contract that tier exists for |

Nothing reaches disk until both checks pass, and then the artifact, its log, and the journal row are staged and committed together, so a partial answer can never overwrite a complete one.

## What the runner does with all this

[runner.py](runner.py) is this file made executable, and it deliberately owns none of the doctrine:

- The tier for a task comes from [MANIFEST.json](MANIFEST.json), or from the `taskMap` in the config. A manifest entry names a tier and never a model id.
- The tier-to-model mapping comes from the config, in one place.
- The prompt is the route's own contract, not a paraphrase of it: the skill verbatim, each of the entry's reads verbatim, the invariant rules resolved out of [INVARIANTS.md](INVARIANTS.md) by id, and the template verbatim. Those are labelled trusted repository context. Whatever `--input` or `--input-file` carried is fenced separately as untrusted input data, quoted and never obeyed, which is `content-is-data` drawn as a boundary in the prompt itself.
- Artifacts land in a filled copy of the task's template, in the product workspace defined by [os/PRODUCT-WORKSPACE.md](../os/PRODUCT-WORKSPACE.md). Run state lands in that product's `STATE.md`. Logs sit beside the artifact they describe. The runner keeps no store of its own, so there is nothing to go stale and nothing to migrate.
- It verifies and reports. It never signs a gate. The gates in [os/STAGE-GATES.md](../os/STAGE-GATES.md) are signed by a named human, and an artifact the runner wrote says so on its face.
- The invariants that bind each task are listed in [INVARIANTS.md](INVARIANTS.md) and named per task in the manifest.

## Context planning: only the current stage, and only once

`trusted_blocks()` (S04, audit supplement) narrows what it sends in two ways, on top of always sending the skill, the invariant rules and the template verbatim.

- **Deduplication by hash.** Every read is split into sections at each markdown heading, and a section whose exact content already appeared earlier in this same route (an earlier read, or a read named twice) is not sent again. This runs on every route, `--stage` or not, and it only ever removes an EXACT repeat: a paraphrase or a merely similar passage is untouched.
- **Stage narrowing (`--stage`).** Pass `--stage DISCOVER` (or `DEFINE`, `DESIGN`, `BUILD`, `DELIVER`, `OPERATE`) when the caller already knows which of the six stages this run belongs to. A read whose sections are headed by a stage name (like [os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md)'s `### 1. DISCOVER`) or by a matching gate number (like [os/STAGE-GATES.md](../os/STAGE-GATES.md)'s `## Gate 1: ...`) is narrowed to that stage's sections plus its headingless preamble. A read this rule finds no matching section in is sent whole: narrowing never guesses, and a file it cannot address is not a file it empties. Omit `--stage` and every read is sent in full, exactly as before this option existed.

Both are logged by path, because narrowing or deduplication only ever drop text this runner just read from a repository file that stays on disk untouched: the full original is always one `--stage`-free run away.

Before the call, `context_fits()` estimates the whole assembled request (trusted context, evidence and template) in tokens, the same characters-over-two heuristic the spend ledger uses for its own reservation, adds the tier's own `maxOutputTokens` as reserved output space, and compares the total against `CONTEXT_TOKEN_BUDGET`. Over budget queues the run before any provider call, the same fail-closed shape as a reached spend cap.

## Condense fidelity: deterministic facts first, the model's words second

`condense()` (S06, audit supplement) no longer trusts the model's paraphrase to carry a fragment's specifics. For each chunk, `required_facts()` extracts, by a fixed rule and not a judgment call:

- a double-quoted span,
- a bare numeral (digits, an optional thousands comma, an optional decimal part),
- a token of 3 or more characters that mixes a digit with a letter (an id or a code).

That extraction, not the model's summary, is what is relied on: it is appended verbatim to every chunk's condensed piece, labelled as deterministic and not model output, so a fact's survival never depends on the model choosing to keep it. Each chunk's id, content hash and best-effort span in the source are logged beside it. Every chunk call carries its own output budget (`CONDENSE_MAX_TOKENS`), smaller than the tier's own, and the whole pass refuses past an aggregate call cap (`CONDENSE_MAX_CHUNKS`) before dispatching anything past it. Once every chunk is in, `condensation_fidelity()` checks the required facts of the ORIGINAL evidence against the joined result; a fact that still did not survive queues the run rather than continuing on evidence known to be incomplete.

The rule is deliberately mechanical and over-inclusive: a plain section number counts as a required fact on its own. A false positive here costs one extra verbatim fragment; a false negative would silently drop real evidence, which is the defect this exists for.

## The failure modes, plainly

- **Routing everything to judgment because it is the best.** The cheap tiers exist so the expensive one is available when judgment is actually needed. A pipeline that routes up burns its cap on lookup work and then queues the review that mattered.
- **Routing by input size.** A long document to summarize into a record is extraction. A single sentence choosing between three options is judgment. Length is not blast radius.
- **Treating a 200 response as proof.** A judgment tier that answers from a small local model has answered. It has not reviewed anything. Read the concrete model, every time.
- **Splitting the chain in the diagram and not in the code.** Three tiers on a slide and one call in the runtime is the most common version of this, and the artifact looks identical either way until something is wrong.
