---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/positioning.md", "frameworks/strategy/value-proposition-canvas.md", "templates/planning/gtm-plan.md"]
method: "knowledge/INDEX.md"
aliases: ["Positioning canvas", "positioning-canvas"]
---
# Positioning canvas

Based on the ideas of April Dunford, from Obviously Awesome: How to Nail Product Positioning so Customers Get It, Buy It, Love It (2019). Explained here in this repository's own words.

## What it is for

Most positioning starts from a tagline and works backward to justify it. Dunford's method runs the other direction, in a fixed order: name what the customer would use if you vanished, find what you have that those alternatives lack, translate each attribute into value with proof, find the customers for whom that value is urgent rather than nice, and only then choose the market category, the frame that makes the value obvious with no explanation needed. Skip a step, or take them out of order, and the category does the work the earlier steps were meant to do, usually by borrowing a competitor's frame. This worksheet enforces the order; the [positioning template](../../templates/planning/positioning.md) is where the answer gets written up for a reader who was not in the room.

## Run it when

- A product, feature, or tier needs a positioning statement and none exists, or the existing one reads like a tagline with reasons attached afterward
- Sales keeps comparing you to the wrong alternative, or the right one but the wrong attribute
- A rebrand, a new segment, or a repositioning is on the table and the last exercise cannot be found or defended
- Before [pricing and packaging](../../templates/planning/pricing-packaging.md), since price is read against the category you claim

**Skip it when:** the [value proposition canvas](value-proposition-canvas.md) has not been run and no evidenced pains or gains exist for any segment. Positioning without evidenced value is five confident guesses in the right order, which reads better than the wrong order but is no more true.

## Inputs you need first

- The current alternatives customers actually use, from the discovery document or [competitive analysis](../../templates/discovery/competitive-analysis.md)
- Evidenced value: the [value proposition canvas](value-proposition-canvas.md), if run, or interview evidence notes
- A segment candidate list, from [personas](../../templates/discovery/personas.md) or the discovery document
- The existing tagline or pitch, if one exists, set aside and not read again until Part 5

## The worksheet

<!-- Fill Parts 1 to 5 strictly in order. Do not open a part until the one before it has real entries with evidence, not placeholders; a canvas filled out of order is the trap this sheet exists to catch. -->

### Part 1: competitive alternatives

| Alternative (what they actually do without us) | Why it is good enough today | Evidence |
|---|---|---|
| | | |
| | | |
| | | |

**Gate:** at least three named alternatives, none of them "the market" or "nothing," each with linked evidence or marked assumption.

### Part 2: unique attributes

| Attribute (a fact about us, not a benefit) | Which Part 1 alternatives lack it | Evidence they lack it |
|---|---|---|
| | | |
| | | |

**Gate:** every attribute names at least one alternative that lacks it, by evidence, not by assertion.

### Part 3: value, with proof

| Attribute (from Part 2) | Value it creates for the customer | Proof (measured result, named outcome, or "unproven") |
|---|---|---|
| | | |
| | | |

**Gate:** no row moves forward on "unproven" alone if a test exists this week; unproven rows may proceed to Part 4 but must stay marked.

### Part 4: best-fit segments

| Candidate segment | Which Part 3 values they rank urgent, not nice | Signal (trigger, threshold, or regulation that makes it urgent) | Rank |
|---|---|---|---|
| | | | |
| | | | |

**Decision rule:** rank by how many Part 3 rows a segment treats as urgent, weighted toward the values with proof over the values marked unproven. The top-ranked segment is the best fit; it does not have to be the largest segment.

### Part 5: market category

| Field | Answer |
|---|---|
| Category chosen | [the mental shelf the Part 4 segment already has] |
| What it makes them assume, before you say a word | [pricing shape, must-have features, expected rivals] |
| Assumptions the category creates that we do not meet | [named now, so sales meets them prepared] |
| Categories considered and rejected | [category: the reason] |

**The swap test:** read the value row for each Part 3 attribute with the leading Part 1 alternative's name swapped in for ours. A sentence that still reads true failed: the value was not unique, it was assumed. Send it back to Part 2, not to Part 5.

## Reading the result

- **All five parts pass their gates in order.** Copy the sequence into the positioning template; this sheet is the evidence trail behind it.
- **The category was chosen before Part 4 finished, or a tagline drove Part 1's alternative list.** Positioning built backward. Start over from Part 1 with the tagline set aside; do not patch Part 5.
- **Part 2 is empty, or every attribute is shared with an alternative.** No unique attribute exists yet, so no category choice can be honest; that is a product finding, not a wordsmithing one, and it belongs in the roadmap before a deck.
- **Two segments tie in Part 4.** Do not position for both. The [GTM plan](../../templates/planning/gtm-plan.md) needs one beachhead; pick the segment with more proved, not unproven, Part 3 rows.

## ILLUSTRATIVE example

Invented, Ledgerline's expense copilot, positioned as a product sold to other mid-market finance teams.

Part 1: a spreadsheet plus a policy document (free, pain lands on the filer); the finance system's bundled module (already paid for, weak on policy checks); a full expense-management vendor (broad, priced for enterprise). Part 2: the draft shows the policy line before submit; none of the three check policy before review. Part 3: that attribute creates first-submission approval without a second pass, proof from a six-filer pilot's approval rate against filers' own prior reports. Part 4: mid-market finance teams on that shared system, close week as the trigger, rank 1; enterprise teams, rank 2, since the full vendor already covers them adequately. Part 5: category chosen, "expense drafting," narrower than "expense management," since the module and the full vendor already own that wider shelf and its price expectations; the narrower category signals a point tool priced per filer, the assumption the pitch has to meet.

Swap test: "the full vendor's draft shows the policy line before submit" reads false; the attribute holds.

## The trap

Writing Part 5 first: an exec already has a category in mind, and Parts 1 through 4 get filled to support it, alternatives narrowed to make the category look uncontested, attributes picked because they sound impressive rather than because a named alternative lacks them. The tell: a Part 1 with fewer than three alternatives, or a Part 4 segment with no signal filled in, both signs the parts were reverse-engineered from a sentence already finished before the sheet was opened. The fix is mechanical: set the tagline aside before Part 1 starts, and do not let one sitting produce Parts 1 to 4 and Part 5 together; a day between breaks the anchor.

## Feeds

- [Positioning](../../templates/planning/positioning.md): sections 1 to 5, in the same order
- [Value proposition canvas](value-proposition-canvas.md): Part 3 (value) draws on its evidenced relievers and gain creators
- [GTM plan](../../templates/planning/gtm-plan.md): the best-fit segment as the beachhead
- [Pricing and packaging](../../templates/planning/pricing-packaging.md): the category chosen sets the pricing shape a buyer expects
- [Sales enablement one-pager](../../templates/delivery/sales-enablement-one-pager.md): the alternatives and proof rows, directly
- PLANNING track, ahead of the GTM plan
- Method background: [knowledge index](../../knowledge/INDEX.md), Obviously Awesome positioning entry
