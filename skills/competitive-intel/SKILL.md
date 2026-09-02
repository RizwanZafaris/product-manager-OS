---
name: competitive-intel
description: Produce a sourced competitor teardown (offer, pricing, positioning, gaps) where every claim carries a URL and a date, landing in the competitive analysis and positioning templates. Use when a build, buy, pricing, or positioning decision needs to know what the alternatives actually do, when a competitor move has the team reacting on rumor, or when win-loss keeps naming the same rival. Takes the decision, the job, and a candidate set; returns the evidence table, a teardown per competitor, the structural read, and a committed so-what.
---

# Competitive Intel: a teardown that changes one decision

Competitive work fails as a scrapbook: fifteen logos in a feature grid, pricing copied from a page nobody dated, a sales deck's claims laundered into fact, and positioning that starts from the leader's category. This skill starts from the decision, sources every claim, and ends with a reading someone signs.

## Files this skill drives

- [../../templates/discovery/competitive-analysis.md](../../templates/discovery/competitive-analysis.md), every section, section 1 first
- [../../templates/planning/positioning.md](../../templates/planning/positioning.md), sections 1, 2, and 5
- [../../templates/discovery/evidence-note.md](../../templates/discovery/evidence-note.md), one per load-bearing source
- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where the decision lands
- Worksheets: [../../frameworks/strategy/positioning-canvas.md](../../frameworks/strategy/positioning-canvas.md) (Dunford, Obviously Awesome, 2019), [../../frameworks/strategy/porters-five-forces.md](../../frameworks/strategy/porters-five-forces.md) (Porter, Harvard Business Review, 1979), [../../frameworks/strategy/seven-powers-audit.md](../../frameworks/strategy/seven-powers-audit.md) (Helmer, 7 Powers, 2016)
- Method background: the Obviously Awesome and 7 Powers entries in [../../knowledge/INDEX.md](../../knowledge/INDEX.md), [../../knowledge/jobs-to-be-done.md](../../knowledge/jobs-to-be-done.md), [../../knowledge/roles/pmm-boundary.md](../../knowledge/roles/pmm-boundary.md) on who owns the category call

## When to use

- A build, buy, or partner decision, a price, or a positioning refresh needs to know what the alternatives do
- A competitor shipped, repriced, or was acquired, and the roadmap is being rewritten from a headline
- Before Gate 1, when the "what they hire today" row of the discovery set is empty
- The win-loss review names the same rival three quarters running

## Inputs

The decision, its decider, its needed-by date, and the finding that would flip it. The job, stated without naming any product, from the JTBD spec or the discovery document. A candidate set. Access: a trial account or budget for one, win-loss and sales notes, the current positioning if any.

Ask for what is missing. No decision: stop; the analysis template makes section 1 mandatory for this reason. No job: ask what the customer does today when the product is absent, the spreadsheet and the nothing included. Then write down what the team already believes about each competitor, so the research cannot quietly become confirmation.

## Workflow

### 1. Fix the decision and the set

Write the decision, the decider, the date, and the flip finding before opening a single competitor page. Choose the set: five entries at most, at least one of them a non-product alternative (manual process, in-house build, doing nothing), because that is usually the real incumbent. Decision rule: an entry that could not change the decision in section 1 leaves the set.

### 2. Plan the sources by strength

Per competitor, in order of strength: use it yourself (trial, sandbox, demo); their documentation, pricing page, changelog, terms; public filings, job postings, partner directories; what customers said in win-loss and sales notes; analyst or sales-deck claims, last and labeled. Every claim in the table carries a URL a reader could open, the date checked, its source class, and a confidence. Decision rule: no URL and date, no entry. Secondhand claims are marked in the row itself.

### 3. Tear down each competitor on five rows

Offer: what it does and for whom, in their words, quoted. Pricing: the unit they charge by, list price, what is gated to which tier, a dated capture of the page. Positioning: the category they claim, who they name as the alternative, the segment they court. Gaps: what they cannot do, evidenced by documentation, a test, or a customer statement; the absence of a marketing page is not evidence of absence. Direction: hiring, release cadence, partnerships, each with a date.

### 4. Read the structure, not just the rivals

Run the five forces at the level of the market the decision lives in: rivalry, entrants, substitutes, buyer power, supplier power, one line each with its implication for price and roadmap. Then run the 7 Powers audit on the product and on the strongest rival: for each power, is there a benefit, and is there a barrier. Decision rule: a benefit with no barrier is a feature, and features get copied; write "none" for the power rather than a hopeful adjective.

### 5. Compare on the decision axes, then position in order

Choose three to five axes that could move the decision and fill section 5 of the analysis template. Feature checklists do not earn a column. Then fill the positioning canvas in Dunford's order: competitive alternatives, unique attributes, value with proof, best-fit segment, market category last. Never from a tagline backward. Positioning sections 1 and 2 fill from the teardown, section 5 from the canvas; sections 3 and 4 need discovery evidence and stay marked unproven without it.

### 6. Commit and date the shelf life

Write the so-what: what this says about the decision, in two or three committed sentences; where we are behind and whether it matters here; what we will not copy and why; open questions with an owner and a date. Log the decision with a link to the analysis, and set a refresh-by date on the header. Competitive facts rot faster than any other evidence, and an undated teardown is a rumor with tables.

## Output format

1. Decision block: decision, decider, needed by, flip finding, what the team believed going in
2. Competitor set table, five rows at most, one non-product alternative
3. Evidence table: | # | Competitor | Claim | URL | Date checked | Source class | Secondhand? | Confidence |
4. Teardown per competitor: offer, pricing, positioning, gaps, direction
5. Structure: five forces, one line and one implication each; 7 Powers verdict for us and for the strongest rival
6. Comparison on the decision axes, the so-what, the decision log entry, the refresh-by date

## Failure modes this skill guards against

- The fifteen-logo grid with no decision behind it
- Claims from a sales deck or an analyst summary laundered into fact
- Prices without a date, quoted a year later
- Positioning chosen from the leader's category instead of from what customers do today
- A roadmap rewritten because a rival shipped something, without asking whether the cohort cares
- Comparing against the named rival while the actual incumbent is a spreadsheet
- Naming a "power" that has a benefit and no barrier

## Exit gate

The analysis feeds Gate 1 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) and the positioning doc the GTM plan is built on. Do not report it done until every claim carries a URL and a date, the so-what commits to a reading, the decision log entry links the analysis, and the refresh-by date is on the header.
