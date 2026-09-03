---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/product-strategy.md", "templates/planning/vision.md", "templates/definition/assumptions-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Playing to Win cascade", "playing-to-win"]
---
# Playing to Win cascade

Based on the ideas of A.G. Lafley and Roger L. Martin, from Playing to Win: How Strategy Really Works (2013). Explained here in this repository's own words.

## What it is for

Strategy is five choices that constrain each other: what winning means, where you will play, how you will win there, what capabilities that demands, and what management systems keep those capabilities sharp. The cascade forces each choice to follow from the one above it, so a where-to-play that lists every segment or a how-to-win that names no capability shows up as a broken link. The second half, reverse engineering, is the part teams skip: for each serious option, write down what would have to be true for it to be the right choice, then test the condition you believe least. It improves one decision: which option to fund, and which condition to test before the money moves.

## Run it when

- Two or three credible options are on the table and the room is choosing by seniority
- The product strategy names bets but nobody can say what capability each bet requires
- After the [strategy kernel](strategy-kernel.md) passes and the policy needs turning into testable conditions
- When a new leader asks "what is our strategy" and the answer is a roadmap

**Skip it when:** there is one option and no budget to test anything. The cascade earns its cost by comparing options and surfacing conditions; with a single forced move, write the conditions straight into the [assumptions register](../../templates/definition/assumptions-register.md) and get on with it.

## Inputs you need first

- A diagnosis and crux from the strategy kernel worksheet
- User evidence: [personas](../../templates/discovery/personas.md) and the discovery document
- The alternatives fact base: competitive analysis, sections 3 to 6, including buy and do-nothing
- An honest capability inventory from the engineering lead: what the team can do today

## The worksheet

### Part 1: the cascade, per option

<!-- One column per option. A choice that refuses nothing is not a choice. Where to play names user, scope, and channel; how to win is one of two things, lower cost or a difference the user prefers, never both. -->

| Choice | Option A | Option B | What each refuses |
|---|---|---|---|
| Winning aspiration (what winning looks like for the user, not a number) | | | |
| Where to play (user, scope, geography, channel) | | | |
| How to win (why the chosen user picks this over the alternative) | | | |
| Capabilities required (three to five things we must do better than the alternative) | | | |
| Management systems (measures, rituals, and structures that keep the capabilities sharp) | | | |

**Coherence check:** read each column top to bottom. If the how-to-win could be stated without the where-to-play, the where-to-play is decoration. If a required capability is not in the inventory and has no build plan, the option is a wish.

### Part 2: what would have to be true

<!-- Written by the person who likes the option least. Categories: user (they would value this), company (we could do it at acceptable cost), alternative (the vendor or incumbent would not respond), channel (it reaches them). At least one condition per category. -->

| Option | Condition that would have to be true | Category | Confidence (high / med / low) | Cheapest test | Owner | By |
|---|---|---|---|---|---|---|
| A | | | | | | |
| A | | | | | | |
| B | | | | | | |

**Decision rule:** an option dies when any condition is known to be false. Among survivors, rank by the count of low-confidence conditions; test the lowest-confidence condition of the leading option first, before any build money moves. Fund an option only when every low-confidence condition has a test with a date, and file each condition as an assumptions register row.

## Reading the result

- **One option survives with every condition high or medium.** Fund it. Copy the cascade into the product strategy and the conditions into the register.
- **Two survive.** Do not average them. Run the two cheapest low-confidence tests and reconvene with results, not opinions.
- **None survive.** The diagnosis was wrong or the options were too narrow. Return to the kernel; do not soften a false condition into "medium".
- **An option survives only because a condition was never written.** Someone liked it too much. Reassign Part 2 to the skeptic and rerun.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot, the internal tool; the two options the finance lead and the PM argued.

| Choice | Option A: build the copilot | Option B: buy a vendor expense tool and mandate it |
|---|---|---|
| Winning aspiration | Reports accepted first time, with the filer still the author | Expense administration off the finance team's desk |
| Where to play | Filers who travel one to four times a quarter, and the three reviewers; not assistants filing for others | Every employee, all expense types, from day one |
| How to win | The draft carries the policy line, so category mismatches stop before submit | Breadth: cards, mileage, per diem in one package |
| Capabilities | Extraction on the receipt formats we see; category-to-policy mapping; a correction loop | Vendor management; a rollout and training program |
| Management systems | Weekly first-submission approval review; eval thresholds per the eval spec | Licence review; a mandate enforced by finance |

Conditions for Option A: filers accept a draft they must review rather than wanting auto-submit (user, medium; test: pilot with eight filers); extraction on crumpled and foreign-language receipts clears the eval threshold (company, low; test: run the eval set before Gate 2); no vendor offers policy-line drafting at lower total cost inside two quarters (alternative, medium; test: three vendor demos, timed). Option B died on one condition: a vendor whose terms forbid training on Ledgerline data, at a licence cost below the build, was tested and not found.

## The trap

Advocacy dressed as conditions. The option's sponsor writes Part 2, lists four conditions they already believe, scores them all high, and skips the one they suspect is false. The cascade then "proves" the option. The tell: no condition in the alternative category, and no row scored low. A sheet with no low-confidence row was written by a believer. Hand Part 2 to the person who argued for the other option, and require one condition per category before anyone scores anything.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 2 (where to play), section 3 (how we win), section 4 (sequencing takes the test order)
- [Vision](../../templates/planning/vision.md): section 2 (who this is for) and section 5 (non-goals) take the refusals
- [Assumptions register](../../templates/definition/assumptions-register.md): section 1, one row per condition
- PLANNING track; the funded option is what the [roadmap](../../templates/planning/roadmap.md) Next column may contain
- Method background: [knowledge index](../../knowledge/INDEX.md), Playing to Win entry
