# Weighted decision matrix

Based on the ideas of Stuart Pugh, from his concept selection method (1981) and Total Design (1991), with criteria weights in the manner of multi-attribute decision analysis (Keeney and Raiffa, 1976); the impact versus effort 2x2 is a common pattern with no single originator. Explained here in this repository's own words.

## What it is for

Choosing one option from a few (a vendor, an architecture, a market, a pricing model) against criteria that matter unequally. The matrix makes the weights explicit before the options are scored, so the argument happens where it belongs, on what matters, rather than on which option someone already prefers. It produces a weighted total per option, a margin, and, through the sensitivity check, an honest statement of whether the decision is robust or a judgment call dressed as arithmetic.

## Run it when

- Two to five mutually exclusive options and three to eight criteria, with facts available per option.
- The disagreement is about priorities ("cost matters more than control") rather than about facts.
- The decision is a one-way door or a heavy two-way door on the [decision doors](decision-doors.md) sheet and deserves a written case.

**Skip it when:** one criterion decides it. If only one option can meet the date, or one fails a legal test, the matrix is theatre with a spreadsheet; write the one-line decision in the log and move on.

## Inputs you need first

- The options, described to the same depth; a thin option always loses to a detailed one.
- Criteria drawn from the problem statement, the [NFRs](../../templates/definition/nfr.md), and the [product strategy](../../templates/planning/product-strategy.md), not from what the favorite option is good at.
- A fact per option per criterion, with its source, or a marked gap in the [assumptions register](../../templates/definition/assumptions-register.md).
- The single decider, per [triad decision rights](../../knowledge/roles/triad-decision-rights.md).

## The worksheet

### Step 1: criteria and weights, before any option is scored

| Criterion | What a 5 looks like | What a 1 looks like | Weight (1 to 5) | Why this weight |
|---|---|---|---|---|
| [criterion] | [observable] | [observable] | [n] | [one sentence] |

<!-- The decider sets the weights and dates the sheet before scoring starts. Weights changed after scoring are logged as a new sheet, never edited in place. -->

### Step 2: score and multiply

Score each option 1 to 5 per criterion against the anchors above. Weighted = weight x score. Total = sum of weighted scores.

| Criterion | Weight | A score | A weighted | B score | B weighted | C score | C weighted |
|---|---|---|---|---|---|---|---|
| [criterion] | [w] | [1 to 5] | [w x s] | | | | |
| **Total** | | | [sum] | | [sum] | | [sum] |

Margin = (winner total minus runner-up total) / winner total. Under 10 percent is a tie.

### Step 3: sensitivity check

Change one thing at a time and re-total. If the winner changes in any row, the decision hinges on that weight or score, and the memo must say so.

| Change | New totals | Winner changes? | What it tells you |
|---|---|---|---|
| Swap the two highest weights | | | Whether the ordering of priorities decides it |
| Set the most contested weight to 1 | | | Whether one stakeholder's criterion decides it |
| Drop the criterion the winner scores best on | | | Whether the winner is a one-trick option |
| Lower the least-evidenced score by 1 | | | Whether the decision rests on a guess |

### The two-minute version: impact versus effort

For a quick sort of a small list, before any of the above is worth its cost. Split each axis at the median of the set, not at an absolute, so every quadrant can hold something.

| | Effort below the median | Effort above the median |
|---|---|---|
| Impact above the median (against the period's metric) | Do now | Plan and size; graduate to the [RICE sheet](rice-scoring-sheet.md) |
| Impact below the median | Fill-ins, for idle weeks | Do not do; write down why |

## Reading the result

The winner is the highest total that survives the sensitivity rows. Report three things: the winner, the margin, and the weight the decision hinges on. A tie or a sensitive result is not a failure of the method; it is the finding. Settle it by fetching the one fact that would move the contested score, or, if that fact cannot be had in time, by the decider's judgment stated as judgment in the [decision log](../../templates/execution/decision-log.md), with the losing options recorded.

## ILLUSTRATIVE example

Ledgerline chooses how to extract receipt fields for the expense-report copilot. Options: A, the general-purpose model vendor's document API; B, a specialist OCR vendor plus in-house classification; C, an in-house model. Every score invented.

| Criterion | Weight | A | A wtd | B | B wtd | C | C wtd |
|---|---|---|---|---|---|---|---|
| Accuracy on the pilot receipt set | 5 | 4 | 20 | 4 | 20 | 2 | 10 |
| Time to first release | 4 | 5 | 20 | 3 | 12 | 1 | 4 |
| Data-handling terms (retention, training on our data) | 5 | 3 | 15 | 4 | 20 | 5 | 25 |
| Cost per report at scale | 3 | 3 | 9 | 4 | 12 | 2 | 6 |
| Control over the roadmap | 2 | 2 | 4 | 3 | 6 | 5 | 10 |
| **Total** | | | 68 | | 70 | | 55 |

B leads A by 2 of 70, about 3 percent: a tie. Sensitivity: setting the data-handling weight to 1 gives A 56 and B 54, so the decision hinges entirely on data-handling terms, which are also the least-evidenced score on the sheet. The finding is not "B wins"; it is "get both vendors' data terms in writing before deciding," logged with a date.

## The trap

Reverse engineering. The team scores the options first, sees that the favorite lost, and adjusts weights until it wins; the sheet then arrives at the review as proof. The tell is a weights column with no "why," dated after the scores. The sensitivity check is the defence, and it is the first thing a tired team skips, because it can only make the answer less certain. A matrix presented without its sensitivity rows is a press release with a total at the bottom.

## Feeds

- [Decision log](../../templates/execution/decision-log.md): the entry, with the options that lost and the weight it hinged on
- [Decision memo](../../templates/planning/decision-memo.md), driven by the [decision-memo skill](../../skills/decision-memo/SKILL.md), for one-way doors
- [ADR](../../templates/architecture/adr.md) when the choice is structural, feeding [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
- [Assumptions register](../../templates/definition/assumptions-register.md): every score that rests on a guess
- How much process the choice deserves: [decision doors](decision-doors.md); the same mechanism for sourcing choices: [build, buy, partner](../strategy/build-buy-partner.md)
- Method background: no card yet; the attribution line above names the sources, and the [knowledge index](../../knowledge/INDEX.md) holds the neighbouring methods
