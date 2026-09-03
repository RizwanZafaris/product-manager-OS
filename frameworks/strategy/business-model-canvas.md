---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/business-case.md", "templates/planning/pricing-packaging.md", "templates/definition/assumptions-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Business model canvas", "business-model-canvas"]
---
# Business model canvas

Based on the ideas of Alexander Osterwalder and Yves Pigneur, from Business Model Generation (2010). Explained here in this repository's own words.

## What it is for

A business model is the logic by which a product turns value delivered into money kept. The canvas lays that logic out in nine blocks on one page: who you serve, what you offer them, how it reaches them, what relationship you keep, how you earn, what you must own, what you must do, who you rely on, and what it all costs. The page is not the output. The output is two consistency checks that a filled canvas makes possible: whether revenue covers the cost structure at the scale you plan for, and whether each value proposition is written for a segment that actually appears in the segment block. A canvas that passes both is a model; one that fails either is a hope with nine headings.

## Run it when

- Before the [business case](../../templates/planning/business-case.md), so the cost and revenue logic exists before the arithmetic
- When pricing is being set and nobody has written down the cost to serve one customer
- When a partnership or channel changes the economics and the strategy has not caught up
- When an internal tool is proposed for sale and the question is whether it closes as a business

**Skip it when:** the product has no paying customer and one team. Use the [lean canvas](lean-canvas.md); its blocks are built for hypotheses, and this one is built for a business that already runs or is being modelled as one.

## Inputs you need first

- Segment and value evidence: discovery document, personas, and the [value proposition canvas](value-proposition-canvas.md) if run
- Price and value metric from the [pricing and packaging](../../templates/planning/pricing-packaging.md) sheet
- Cost facts from engineering and finance: inference, infrastructure, support, sales, per customer where possible
- Channel evidence: what has actually brought customers so far, or the honest word "none"

## The worksheet

### Part 1: the nine blocks

<!-- One line of answer per block, with evidence and confidence. Where a block holds a guess, say so; guesses go to the assumptions register. -->

| Block | Prompt | Answer | Evidence | Confidence (high / med / low) |
|---|---|---|---|---|
| Customer segments | Who pays, who uses, and which segment we build for first | | | |
| Value propositions | What problem we solve per segment, in the customer's words | | | |
| Channels | How each segment hears about us, buys, and gets onboarded | | | |
| Customer relationships | Self-serve, assisted, or managed, per segment, and what that costs | | | |
| Revenue streams | What each segment pays for, by which value metric, how often | | | |
| Key resources | The assets the model cannot run without: data, integrations, people, licences | | | |
| Key activities | The two or three things we must do well every week | | | |
| Key partnerships | Who supplies or distributes something we will not build, and why they want to | | | |
| Cost structure | The largest costs, fixed and variable, and which block drives each | | | |

### Part 2: consistency check A, revenue covers cost

<!-- Per customer, per year, at the scale the strategy assumes. Every number is ILLUSTRATIVE until finance agrees the method. -->

| Line | Value | Source |
|---|---|---|
| Revenue per customer per year | | |
| Variable cost to serve per customer per year (inference, support, infrastructure) | | |
| Contribution per customer (revenue minus cost to serve) | | |
| Cost to acquire one customer | | |
| Fixed cost per year (team, tooling) | | |
| Break-even customer count (fixed cost divided by contribution) | | |
| Customer count the strategy assumes at the end of the horizon | | |

**Rule:** contribution must be positive, and the assumed count must pass break-even inside the planning horizon. Otherwise the model does not close, and no narrative fixes that.

### Part 3: consistency check B, proposition matches segment

| Segment (from the segment block) | Value proposition written for it | Channel that reaches it | Revenue stream it pays |
|---|---|---|---|
| | | | |

**Rule:** every segment has a row with all four cells filled, and every value proposition appears in exactly one segment's row. A proposition with no segment is a feature; a segment with no proposition is a wish.

## Reading the result

- **Both checks pass.** Copy the model into the business case; the canvas is its appendix.
- **Check A fails on contribution.** The value metric or the cost to serve is wrong. Go to the pricing sheet before adding customers; more customers at negative contribution is a faster way to lose money.
- **Check A fails on break-even.** A scale problem. Either the channel block cannot deliver the count or the fixed cost is too high for the horizon; the strategy's sequencing section has to say which.
- **Check B fails.** The segment block was written to make the check pass ("finance teams of all sizes"). Split it until each row is specific enough to name a buyer.

## ILLUSTRATIVE example

Invented. Ledgerline modelled what its internal expense copilot would look like as a product sold to other mid-market firms. All numbers are fictional and exist only to show the arithmetic.

Segments: mid-market finance teams (buyer) and their filers (users). Value: reports accepted the first time; reviewer hours back. Channels: the finance system's marketplace, then direct sales. Relationships: assisted onboarding to encode the policy, then self-serve. Revenue: a monthly fee per active filer. Key resources: the finance system integration and the policy mapping method. Key activities: extraction quality, policy encoding. Partners: the finance system vendor, a model provider. Costs: inference, integration maintenance, a two-person sales effort.

| Line | ILLUSTRATIVE value |
|---|---|
| Revenue per customer per year | 24,000 |
| Cost to serve per customer per year | 6,000 |
| Contribution | 18,000 |
| Cost to acquire | 9,000 |
| Fixed cost per year | 1,800,000 |
| Break-even count | 100 customers |
| Assumed count at end of year three | 140 customers |

Check A passes with little room: a doubling of inference cost pushes break-even to 150 customers and the plan needs a price change. That sensitivity goes to the assumptions register and the business case. Check B passes only after "finance teams" was split into the buyer and the filer, with the filer's proposition (one sitting, no bounce) reaching them through the buyer's rollout, not a channel of its own.

## The trap

The canvas as an org chart. The team fills the blocks with what exists today (every vendor under partners, "subscription" under revenue, the whole team under key resources) and skips the checks because the page looks complete. The specific failure is a revenue block with no value metric: "subscription" says how often money arrives, not what the customer pays for, so check A cannot run and nobody notices it did not. Write the value metric into the revenue block first, then run check A before the page is shown to anyone.

## Feeds

- [Business case](../../templates/planning/business-case.md): the cost and revenue logic behind its options and sensitivities
- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 1 (value metric) and section 2 (pricing model)
- [Assumptions register](../../templates/definition/assumptions-register.md): every low-confidence block and the check A sensitivity
- [Product strategy](../../templates/planning/product-strategy.md): section 2 segments and section 3 differentiation must match the canvas
- PLANNING track, ahead of Gate 1 for a new product line
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
