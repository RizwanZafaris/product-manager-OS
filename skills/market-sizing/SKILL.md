---
name: market-sizing
description: Size a market top-down and bottom-up as TAM, SAM, and SOM, reconcile the two within a stated tolerance, and register every input as an assumption with a source or a test. Use when a business case, a where-to-play choice, a board question, or a Gate 1 cost-of-inaction calculation needs a market number that survives the question "where did that come from". Takes a segment definition, a unit, a price with its source, and count sources; returns both sizings, the reconciliation, a sensitivity range, and the assumption rows.
---

# Market Sizing: two methods that must agree, and every input on the record

A market size fails when it is one number from an analyst headline, a small share of a large figure, and a spreadsheet nobody can reopen. The business case then rests on it, the board quotes it, and the first real customer count proves it wrong. This skill runs the sizing twice, from the top and from the bottom, forces the two to reconcile, and files every input where a reviewer can attack it.

## Files this skill drives

- [../../frameworks/strategy/market-sizing.md](../../frameworks/strategy/market-sizing.md), the worksheet and its reconciliation table
- [../../templates/definition/assumptions-register.md](../../templates/definition/assumptions-register.md), one row per input that is not a sourced fact
- [../../templates/planning/business-case.md](../../templates/planning/business-case.md), where SOM lands in the benefits as a range with its assumption IDs beside it
- [../../templates/discovery/evidence-note.md](../../templates/discovery/evidence-note.md), one per external figure, with the URL and the definition the source used
- [../../templates/planning/product-strategy.md](../../templates/planning/product-strategy.md), where SAM per segment informs where to play
- [../../templates/planning/gtm-plan.md](../../templates/planning/gtm-plan.md), whose first cohort must be a countable subset of SOM
- Method background: [../../knowledge/crossing-the-chasm.md](../../knowledge/crossing-the-chasm.md) (Moore, 1991) on why the beachhead, not the market, is the number that matters first

## When to use

- A business case or funding ask needs a market number in its benefits section
- A where-to-play choice between segments in the product strategy
- A board or executive asks "how big is this", and the honest answer is not yet written down
- Pricing or packaging work needs a volume estimate per tier
- Gate 1's cost of inaction depends on how many people carry the problem

## Inputs

The segment, described precisely enough to count, from section 4 of the positioning template or the discovery document. The unit the market is counted in (companies, seats, transactions), and the unit the product charges by. A price or price range with its source: the price list, pilot invoices, or a labeled assumption. Count sources: public statistics with URLs, internal data (CRM, billing, product analytics), a directory or register a list could be built from. For SOM, the reach and capacity constraints: channel reach from the GTM plan, onboarding and sales capacity from the owners of those teams.

Ask for what is missing. Never fill a count from memory. A figure with no public source is an assumption row with a validation method, not a cell in the table. If the segment cannot be described well enough to count, stop and finish positioning section 4 first.

## Workflow

### 1. Define the market in one sentence

The job, the segment, the geography, the period (a year), the unit. Write it at the top of the worksheet. Decision rule: if two people would count different things from this sentence, it is not done.

### 2. Size top-down

Start from the largest sourced population and apply filters in sequence: the share in the segment, the share with the trigger that makes the job urgent, the share reachable with the product and channels as they exist. TAM is the population times the unit price per year; SAM is TAM after the reachability filter; SOM is SAM after the capacity filter for the planning horizon. Every filter is a row with a value, a source URL and date or an assumption ID, and a confidence.

### 3. Size bottom-up

Count from the unit up: the number of target accounts from a list you could actually build, times units per account from a sample of real accounts, times price per unit per year. For SOM, the accounts the channel can reach and the team can onboard in the horizon, from the capacity owners. Each factor is a row with the same columns as step 2. Where a sample was used, state its size and how it was drawn.

### 4. Reconcile, do not average

Put the two sizings side by side. State the tolerance from the worksheet before comparing. If they disagree beyond it, find the input that explains the gap: usually a definition mismatch (the public figure counts a broader segment) or a price mismatch (list versus invoiced). Adjust the input with the weaker source and record why. Decision rule: the reconciliation names the gap driver or the sizing is not done; a midpoint between two disagreeing methods is a number with no method.

### 5. Show the range

Take the two least certain inputs, set each to its plausible low and high, and report low, base, and high for SOM. The output is a range with the two drivers named, never a point. Then register every input that is not a sourced fact in the assumptions register: confidence, impact, the cheapest test (count a sample of accounts, check a pilot invoice, run one pricing survey), a validate-by date, an owner. Low-confidence, high-impact inputs get tests scheduled, not caveats.

### 6. Land the numbers where they are used

The business case takes SOM as the range with the assumption IDs beside it. The product strategy takes SAM per segment. The GTM plan's first cohort must be a subset of SOM that a list could be built for this week. Write one paragraph of defense: what would have to be true for the high case, and the single observation that would collapse the base case.

## Output format

1. Market definition sentence, with the unit
2. Top-down table: | Step | Population or filter | Value | Source (URL, date) or AS-id | Confidence |
3. Bottom-up table: | Factor | Value | Source or AS-id | Confidence |
4. Reconciliation: | Method | TAM | SAM | SOM |, the stated tolerance, and the named gap driver
5. Sensitivity: low, base, high for SOM, with the two inputs that drive the spread
6. Assumption rows, and the defense paragraph naming where each number lands

## Failure modes this skill guards against

- A TAM lifted from an analyst headline without the definition that produced it
- SOM as a small share of a huge number, with no capacity behind the share
- Averaging top-down and bottom-up instead of finding why they differ
- Mixing units, companies in one row and seats in the next
- Counting the whole population when only the segment with the trigger buys
- Pricing at list when the pilot invoices say otherwise
- A point estimate where the decision needs a range
- Assumptions that live in the spreadsheet instead of the register
- A real figure with no URL, which this repository's rules forbid outright

## Exit gate

The sizing feeds Gate 1's cost-of-inaction line in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) and the business case behind the roadmap. Do not report it done until every input has a source or an assumption ID, the reconciliation names its gap driver, and the range with its two drivers is what the business case carries.
