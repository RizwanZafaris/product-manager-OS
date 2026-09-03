---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/product-strategy.md", "templates/planning/vision.md", "templates/execution/risk-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Strategy kernel", "strategy-kernel"]
---
# Strategy kernel

Based on the ideas of Richard Rumelt, from Good Strategy Bad Strategy (2011). Explained here in this repository's own words.

## What it is for

Most documents called "strategy" are goals with adjectives. The kernel is the test that tells them apart. A strategy has three parts that depend on each other: a diagnosis that names the one obstacle that matters (the crux), a guiding policy that says how you will get past it, and coherent actions that spend real resources on the policy and on nothing else. Run this worksheet to find out whether the strategy you hold is one, and if not, which part is missing. It improves one decision: whether the product strategy is fit to fund a roadmap.

## Run it when

- Before the [product strategy](../../templates/planning/product-strategy.md) is signed for a period
- When a roadmap review keeps ending in "everything is a priority"
- When a strategy document reads well and nobody can say what it rules out
- When leadership hands down a target ("halve the tickets") and calls it a strategy

**Skip it when:** discovery has not run and there is no evidence to diagnose. The kernel scores a claim about the situation; with an empty [discovery document](../../templates/discovery/discovery-document.md), you will spend the week writing fiction in three parts.

## Inputs you need first

- Evidence about the struggle: filled evidence notes and the discovery document
- The competitive or alternative fact base: [competitive analysis](../../templates/discovery/competitive-analysis.md), section 6, including the do-nothing and buy-a-tool options
- Capacity and constraints: what the team can actually staff this period
- The draft strategy or goals document under test, if one exists

## The worksheet

### Part 1: the diagnosis

<!-- Facts, each with a link. The crux is the one obstacle that, if beaten, makes the rest tractable. A diagnosis with no surprising fact in it is a summary of the org chart. -->

| Claim about the situation | Evidence (linked) | Confidence (high / med / low) |
|---|---|---|
| [what is going on, in one sentence] | | |
| [the second fact] | | |

- **The crux:** [one obstacle, stated so that a reader could disagree with it]
- **What the diagnosis excludes:** [the popular explanation it rejects, and why]
- **What changed:** [why last period's strategy is not automatically this one]

### Part 2: the guiding policy

| Field | Answer |
|---|---|
| The policy | [how we get past the crux, in one or two sentences] |
| What it refuses | [named moves a reasonable rival might make that we will not] |
| The advantage it leans on | [an asset, a position, a capability, or "none yet: speed only"] |

### Part 3: coherent actions

<!-- Three to five. Each one consumes budget or people this period. -->

| # | Action | The policy clause it follows from | What it consumes | Leans on or conflicts with | Owner |
|---|---|---|---|---|---|
| 1 | | | | [another action, or "none"] | |
| 2 | | | | | |

### Part 4: the kernel test

Score each check PASS or FAIL. No partial credit.

| # | Check | Pass or fail | Note |
|---|---|---|---|
| K1 | The diagnosis names a crux, not a goal ("fewer bounces" is a goal) | | |
| K2 | At least one claim in the diagnosis would surprise a new hire | | |
| K3 | The policy refuses something a reasonable rival could do instead | | |
| K4 | Every action traces to a clause of the policy | | |
| K5 | No two actions compete for the same people or contradict each other | | |
| K6 | Resources concentrate: no action is funded "a little" to keep everyone happy | | |
| K7 | No sentence would survive with a competitor's name swapped in | | |

**Decision rule:** seven passes and the strategy is fit to file. A fail in K1 or K2 sends you back to discovery; a fail in K3 means you hold a goal, not a policy; a fail in K4 to K6 means you hold a wish list with a strategy stapled to the front.

## Reading the result

- **All pass.** File the parts into the product strategy template: Part 1 into section 1, Part 2 into section 3, Part 3 into section 4. Attach this sheet as evidence.
- **K1 or K2 fail.** The diagnosis is a description. Return to discovery; the crux usually turns up in the cost-of-inaction work in [problem framing](../../templates/discovery/problem-framing.md).
- **K3 fail.** The policy is an aspiration. Ask what you would refuse to do under it, and write the refusal into the policy.
- **K4 to K6 fail.** The actions are the existing roadmap. Cut the ones that do not trace, and expect that to be most of them.
- **K7 fail alone.** An editing problem. Cut the sentence.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot, the internal tool its own filers and finance reviewers use; no real figures.

| Part | Fill |
|---|---|
| Diagnosis | Expense tickets tripled after a travel agency switch; about a third of reports bounce at review, mostly on category mismatches against a policy the filer has never read; reviewers spend their pass on mechanical checks. Evidence: twelve interviews, finance system baseline. |
| Crux | Policy knowledge and receipt data sit on the wrong side of the submit button, so two people do clerical work in sequence and neither is good at it. Excludes: "the form is bad" and "filers need training". |
| Guiding policy | Move the clerical work to the machine and keep the judgment with the people, on both sides of submit. Refuses auto-submission, a parallel "better form" project, and any vendor whose terms allow training on our data. |
| Coherent actions | 1. Draft from the receipt with the policy line shown. 2. Confidence flags in the reviewer view. 3. Admin correction loop. 4. Measure first-submission approval from week one. 5. Close the vendor-terms clause before Gate 5. |
| Kernel test | K1 to K7 pass. K5 was the near miss: a month-end reminder nudge wanted the same engineer as action 2 and traced to no policy clause, so it was cut. |

The full fill lives in [examples/ledgerline-strategy-kernel.md](../../examples/ledgerline-strategy-kernel.md).

## The trap

The retrofitted diagnosis. A tired team already has a roadmap, so it writes Part 3 first, composes a Part 2 that permits it, then a Part 1 that justifies Part 2. The sheet passes every check on paper. The tell is K2: nothing in the diagnosis would surprise anyone, and the crux is a restatement of the flagship feature ("filers need AI-drafted reports"). A real diagnosis is written before the actions and usually kills one of them. If the sheet killed nothing, it tested nothing.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 1 (diagnosis), section 3 (how we win), section 4 (sequencing)
- [Vision](../../templates/planning/vision.md): section 5 (non-goals) takes the refusals from Part 2
- [Risk register](../../templates/execution/risk-register.md): each low-confidence diagnosis claim becomes a row
- PLANNING track; the signed strategy is the input to every [roadmap](../../templates/planning/roadmap.md) and [OKR](../../templates/planning/okrs.md) cycle
- Companion worksheet: [Playing to Win](playing-to-win.md), which turns the policy into testable conditions
- Method background: [knowledge index](../../knowledge/INDEX.md), strategy kernel entry
