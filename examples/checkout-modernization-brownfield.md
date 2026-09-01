# Brownfield: modernizing a legacy checkout

Fictional company, fictional people, every number invented for illustration. See the [examples index](README.md).

The other two examples start at the beginning of the loop with a clean sheet. Most products are not clean sheets. This one shows the templates attached to a system that is already live, already load-bearing, and already carrying nine years of decisions nobody wrote down. It is a composite: the parts of each template that a brownfield product fills differently, with the compromises left in and one decision that was reversed in flight.

**Product:** Harbourgate, a mid-market retailer's checkout. Nine years old, three payment providers bolted on at different times, one of them through a wrapper written by a contractor who left in 2021. It takes real money every day, which is the whole difficulty.

**Owner:** Ife Adeyemi, Product Manager · **Entered the loop:** 2026-03-09 · **Current stage at time of writing:** BUILD

## Entering the loop mid-flight

There was no Gate 1 for Harbourgate and there never will be. The problem was not discovered; it was inherited. What the team did instead, in the first two weeks, was reconstruct the entry conditions the loop assumes:

- Filled [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md) against the existing system rather than a proposal. The problem statement: one order in nine that reaches the payment step never completes it, and the team cannot say which of the three providers is responsible because two of them log to different systems and one does not log declines at all.
- Skipped [templates/discovery/personas.md](../templates/discovery/personas.md) and marked it N/A because the customer base is known from six years of order data, and inventing archetypes would have added confidence without adding evidence. That skip is recorded in the discovery document, not left blank.
- Ran [templates/discovery/competitive-analysis.md](../templates/discovery/competitive-analysis.md) with the decision stated as "rebuild the payment layer in place, or route through a single provider and retire two integrations". The non-product alternative in the competitor set was "keep the current stack and only fix the logging", and it scored better on every axis except the one that mattered.
- Wrote a Gate 1 form anyway, in the [gates folder](../os/PRODUCT-WORKSPACE.md) of the product workspace, marked "reconstructed, not run" so no future reader mistakes it for evidence gathered before the fact.

**What that cost:** two weeks of a senior PM's time on a product that was already funded. The team decided it was worth it because the alternative was a DEFINE stage built on nobody's stated problem. That trade-off was argued twice and is written down rather than smoothed over.

## The definition stage on a live system

Weight chosen with [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md): full PRD, because three functions had to agree and money was moving. Two sections of [templates/definition/prd.md](../templates/definition/prd.md) behaved differently from the greenfield case:

**Background** could not link to discovery evidence, because there was none. It links instead to the reconstructed problem framing and says so in the first line. A reader who wants to know how confident to be gets that answer immediately.

**Out of scope** did the heavy lifting. On a brownfield product the interesting question is not what you are building, it is what you are refusing to touch while you are in there:

| # | Excluded | Why | Where it went |
|---|---|---|---|
| 1 | The contractor's provider wrapper | It works and nobody understands it. Touching it during a payment migration is two risks at once | Backlog, after the migration lands |
| 2 | Guest checkout redesign | Design has wanted it for two years and it is unrelated to the decline problem | Backlog, owned by design |
| 3 | The order-history page that reads from the payment tables | Coupling is real and known; the migration keeps the table shape so this stays untouched | Named as a constraint in the data model, not a task |

**The constraint nobody wanted to write:** the new payment path must keep writing the old table shape for at least two quarters, because reporting, finance reconciliation, and the order-history page all read it. The clean design does not do that. The team wrote the coupling into [templates/architecture/data-model.md](../templates/architecture/data-model.md) as a stated constraint with a removal date, rather than shipping a clean diagram that the code would immediately contradict.

## The decision that was reversed

Extracts from the product's [decision log](../templates/execution/decision-log.md), newest first. Both entries stand; the first was never edited.

### D-017: Migrate provider by provider, not by traffic percentage

- **Date:** 2026-05-21 · **Decider:** Ife Adeyemi
- **Context:** Two weeks into the ramp, the shadow-traffic approach from D-011 was producing declines we could not attribute. Running old and new paths against the same order meant two authorization attempts against the same card in some retry paths, and the fraud team saw the pattern before we did.
- **Options considered:** fix the retry logic and continue the percentage ramp; pause and migrate one provider at a time behind a per-provider flag; abandon the migration.
- **Decision and rationale:** One provider at a time. It is slower by roughly a month and it gives up the clean side-by-side comparison that D-011 was designed to produce. It also stops us doing something to customers' cards that we would struggle to defend. Given up: the comparison data, and the original launch date.
- **Reverses or is reversed by:** Reverses D-011.
- **Who was told:** Payments channel and the finance weekly, 2026-05-21. Fraud team told first, same day, before the channel post.

### D-011: Ramp the new payment path by traffic percentage, with shadow comparison

- **Date:** 2026-04-14 · **Decider:** Ife Adeyemi
- **Context:** The migration needs evidence that the new path is at least as good as the old one. A percentage ramp with shadow traffic gives a same-day comparison on identical order mixes.
- **Options considered:** percentage ramp with shadow comparison; provider-by-provider migration; a hard cutover on a low-volume weekend.
- **Decision and rationale:** Percentage ramp. The comparison data is worth the added complexity, and the rollback is a flag. Given up: simplicity, and one week of build time on the shadow harness.
- **Reverses or is reversed by:** Reversed by D-017.
- **Who was told:** Payments channel, 2026-04-15.

**Why this pair is in the examples folder.** The reversal is the point. D-011 was a reasonable decision made with the information available in April, and it was wrong by May. The system did its job in three ways: the options that lost were written down, so D-017 did not have to rediscover them; the reversal is a new entry rather than an edit, so the April reasoning survives; and the risk that killed it (retry paths hitting the same card twice) was already sitting in the risk register as a medium, raised by an engineer during the premortem and not weighted heavily enough at the time. The premortem found it. The gate did not stop it. That is a real outcome and it is left in.

## What the gates caught, and what they did not

| Gate | Outcome | Detail |
|---|---|---|
| Gate 1 | Reconstructed, not run | Marked as such. It is context, never cited as evidence |
| Gate 2 | Returned, then signed | Attempt 1 had no measurable criterion for "at least as good as the old path". Attempt 2 defined it against the decline rate per provider, with finance agreeing the baseline |
| Gate 3 | Passed, with a known miss | Nobody could name the owner of the contractor's wrapper. The gate recorded an owner for finding an owner, with a date, which is the honest version |
| Gate 4 | In progress at time of writing | The reversal in D-017 sent one acceptance criterion back to Gate 2 for re-signing, per rule 3 of the loop: backward is allowed, silent backward is not |

## What to copy from this example

1. **Reconstruct the entry conditions, and label the reconstruction.** A Gate 1 form filled in after the fact is useful context and is not evidence. Say which it is on the form itself.
2. **On a brownfield product, out-of-scope is the load-bearing section.** What you refuse to touch while you are in there is the decision that keeps the change shippable.
3. **Write the ugly coupling into the architecture document.** A clean diagram that the code contradicts is worse than an honest one with a removal date.
4. **Reverse decisions in public, with a new entry.** The April reasoning is not embarrassing; deleting it would be.
5. **Let the misses stand in the record.** A worked example where every gate passed on the first attempt teaches nobody anything they can use.
