---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["frameworks/strategy/business-model-canvas.md", "frameworks/strategy/value-proposition-canvas.md", "templates/definition/assumptions-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Lean canvas", "lean-canvas"]
---
# Lean canvas

Based on the ideas of Ash Maurya, from Running Lean (2012), adapting Alexander Osterwalder's business model canvas for a business that does not exist yet. Explained here in this repository's own words.

## What it is for

A business model canvas describes a business; a lean canvas describes a bet. Maurya swapped four of Osterwalder's nine blocks (key partners, key activities, key resources, customer relationships) for four built to expose a startup's biggest unknowns: the top three problems, the alternatives customers use today, an unfair advantage, and the metrics that would tell you the bet is working. The page still has nine boxes and takes the same twenty minutes to fill, but it reads differently: a stack of unproven claims ranked by how much breaks if each is wrong, not a description of a business already running. It improves one decision: which assumption to test this week, and with what.

## Run it when

- Before a product exists and before a business model can be modeled: pre-revenue, pre-customer bets
- A new initiative is being scoped and the team wants its assumptions written down before anyone writes code
- The business model canvas's revenue, channel, or relationship blocks would be pure guesses, because there is no running business yet to describe
- A top problem, the solution, or the unfair advantage line changes; rewrite the canvas rather than patch it, since it is a hypothesis, not a record

**Skip it when:** the business already has paying customers and an operating model. Use the [business model canvas](business-model-canvas.md); its blocks (channels, relationships, partnerships) describe operations a hypothesis-stage bet does not have yet, and filling them from guesses buries the one thing this stage needs, a ranked list of what remains unproven.

## Inputs you need first

- A candidate problem statement and who has it, from the discovery document or [problem framing](../../templates/discovery/problem-framing.md)
- Any interviews already run: evidence notes on what people do about this problem today
- A first cut at the solution, however rough
- Nothing from finance: this canvas runs before a price or a cost is real

## The worksheet

### Part 1: problem, alternatives, solution

<!-- Exactly three problems, ranked. A problem row with "nothing" in the alternative column has not been interviewed; people always do something, even if it is enduring the pain. -->

| # | Top problem, in the customer's words | What they use instead today | Solution feature that beats it | Evidence, or "assumption" |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Part 2: the rest of the canvas

| Block | Prompt | Answer | Confidence (high / med / low) |
|---|---|---|---|
| Customer segments | Who feels problems 1 to 3 worst, and the early adopters within them | | |
| Unique value proposition | One sentence a skeptical customer would repeat back correctly | | |
| Channels | How the segment above hears about this and tries it | | |
| Revenue streams | What gets paid, by whom, on what basis, if anything yet | | |
| Cost structure | The two or three costs that scale with usage or headcount | | |
| Key metrics | The two or three numbers that would tell you, within a month, whether the bet is working | | |

### Part 3: the unfair advantage filter

<!-- An unfair advantage is something a well-funded competitor cannot buy or copy quickly. Being first, working hard, a feature copyable in a sprint, paid marketing, and a strong team with no lock-in are not one on their own. -->

| Candidate advantage | Passes the filter? | Why, specifically, a funded rival could not buy or copy it fast |
|---|---|---|
| | | |

**Decision rule:** most canvases pass nothing here at this stage, and "none yet" is the honest, common answer. A candidate passes only when the why-not column names a specific mechanism, not a head start.

## Reading the result

- **All three problem rows carry real evidence, and the segment is one you could build a list of.** Move to testing the solution against those three problems; do not build the whole canvas at once.
- **Every problem row says "assumption."** This is a research task, not a build task. Get five interviews before touching channels or revenue.
- **The unfair advantage box is honestly empty.** Write "none yet, price and speed only," and revisit it once you have any committed customers; do not force an answer to fill the box.
- **The canvas holds steady across two updates with paying or committed customers.** That stability is the signal to graduate to the [business model canvas](business-model-canvas.md), since channels and relationships can now be described from what happened, not guessed.

## ILLUSTRATIVE example

Invented. Before Ledgerline's expense copilot had any user outside the company, its product team floated selling a standalone version, at the earliest hypothesis stage.

Problems: filers resubmit reports rejected on category mismatches (alternative: argue with the reviewer, or eat the delay; assumption); reviewers spend a pass on mechanical checks instead of judgment (alternative: overtime during close week; assumption); finance gets no early signal a report will bounce (alternative: finds out at review; assumption). Solution: a draft showing the policy line before submit. Segment: mid-market finance teams on a shared finance system; early adopters, teams that already tried a policy document and gave up making filers read it. UVP: "reports that pass review the first time, because the policy check happens before submit, not after." Channels: untested; candidate is the finance system's own marketplace. Revenue: a monthly fee per active filer, an assumption. Cost structure: inference and one support engineer. Key metrics: first-submission approval rate, reviewer hours per close. Unfair advantage: none passes the filter yet; the candidate is the correction log, if it accumulates before a rival's does.

## The trap

The canvas filled to look like a pitch slide instead of a risk map. Every box gets a confident one-liner, revenue reads like a clean subscription story, and the unfair-advantage box names the team instead of staying honestly blank. The tell: a canvas with no cell marked "assumption," though no interview has run since the last version. The whole value of a lean canvas is ranking guesses so you know which to kill first; a page with no guesses marked as guesses has hidden the one thing it exists to show, and will be believed exactly as far as it looks finished.

## Feeds

- [Business model canvas](business-model-canvas.md): the canvas to graduate into once revenue and channels are real, not guessed
- [Value proposition canvas](value-proposition-canvas.md): sharpens the problem and UVP boxes with ranked jobs, pains, and gains before the one-line UVP gets written
- [Assumptions register](../../templates/definition/assumptions-register.md): every box marked "assumption," confidence low, with a validation method and date
- [Vision](../../templates/planning/vision.md): section 2 (who this is for) takes the segment and early-adopter description
- [Product strategy](../../templates/planning/product-strategy.md): section 1, once the problem row carries evidence rather than assumption
- PLANNING track, ahead of Gate 1
- Method background: [knowledge index](../../knowledge/INDEX.md), Lean Startup entry
