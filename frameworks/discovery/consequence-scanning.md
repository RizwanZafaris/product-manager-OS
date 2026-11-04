---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/problem-framing.md", "templates/ai/responsible-ai-impact-assessment.md", "templates/execution/risk-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Consequence scanning", "consequence-scanning"]
---
# Consequence scanning

Based on Consequence Scanning, published by Doteveryone, the UK responsible-technology think tank, as "Consequence Scanning: an agile practice for responsible innovators" (2019). Explained here in this repository's own words. The likelihood and impact scoring in step 3 is this repository's addition, taken from the [risk matrix](../execution/risk-matrix.md), and should not be read as part of Doteveryone's method.

## What it is for

A team planning a feature lists what it intends to happen. This sheet makes it list what else will happen: the effects on people outside the room, the uses nobody designed for, the second-order changes that show up months later. It asks three questions in order. What are the intended and unintended consequences of this feature? Which of them are positive, worth building toward on purpose? Which are negative, and worth reducing? Then it sorts every consequence by how much control the team has over it: act on what you control, influence what you can shape but not decide, and monitor what sits outside your reach. The output is a short list of design changes, owners and watch signals, not a values statement.

## Run it when

- A new product or a feature with a new audience, a new kind of data, or a new way for one person to affect another enters DISCOVER
- Before the [responsible AI impact assessment](../../templates/ai/responsible-ai-impact-assessment.md) is filled for a model feature, to populate its affected-groups and harms sections
- A feature is about to scale past the audience it was tested on: a new market, a public launch after a closed beta
- Each significant iteration of the same feature, rerun in under an hour against the previous sheet

**Skip it when:** the change is a reversible adjustment to an existing flow that adds no new audience, no new data and no new way for one person to reach another, such as a copy change or a reordered settings page. A decision-log line covers it, and a scan run on every small change teaches the team to treat the scan as paperwork.

## Inputs you need first

- One sentence of what the feature does and for whom, from the [problem framing](../../templates/discovery/problem-framing.md) draft
- The people in the room: the building team plus at least one person who is not on it, ideally support or someone who talks to customers every week
- Any evidence of how people already use comparable features: support tickets, research notes, competitor incident reports
- A timebox: 60 to 90 minutes for a first scan, 30 for a rerun

## The worksheet

### Step 1: list consequences, intended and unintended

Write each consequence as a change in someone's life or behaviour, naming who: "members without smartphones stop borrowing" rather than "accessibility concern". Five prompts widen the list past the obvious, and each one is asked out loud:

1. Who is affected and never opens the product?
2. What does someone who wants to cause harm do with this?
3. What happens when it is wrong, slow, or unavailable?
4. What happens at ten times and a hundred times today's usage?
5. What does it change about people's habits after six months?

### Step 2: tag each consequence

Tag every row with three things: intended or unintended; positive or negative for the group named; and the group affected. A consequence can be positive for one group and negative for another; write it twice.

### Step 3: score likelihood and impact

Likelihood within the next twelve months, at the planned usage: 1 no plausible path; 2 plausible, not yet seen anywhere; 3 seen in comparable products; 4 seen in this product's own testing, beta or support queue; 5 already happening.

Impact on the group named, positive or negative, worst credible case for negatives: 1 barely noticed; 2 noticeable, easily absorbed; 3 changes what people do, or costs them real time or money; 4 serious effect on safety, livelihood, or a group's access to something they need; 5 irreversible harm, or physical danger.

**Arithmetic:** score = likelihood x impact, from 1 to 25. **The impact-5 rule:** any negative consequence with impact 5 is treated as score 25 for sorting, whatever its likelihood, because multiplying a rare catastrophe by its low likelihood ranks it below a likely nuisance.

### Step 4: sort by control, then decide

**Act:** the team can change it through the design, the scope, the defaults or the launch plan. **Influence:** the team can shape it but someone else decides: a partner, a platform, another team, a policy owner. **Monitor:** outside the team's reach; the team can only watch for it and respond.

| # | Consequence (who, and what changes) | Intended? | Positive or negative | Group | L | I | Score (L x I) | Act / influence / monitor | Decision | Owner | Signal to watch |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

**Decision rule, applied row by row:**

- Negative, act, score 10 or more (or impact 5): a change to the plan this iteration, with an owner and a date
- Negative, influence, score 10 or more: a named owner and a dated conversation with the person who decides
- Negative, monitor, any score: a signal, a threshold that triggers a response, and an owner; a monitor row without a signal is deleted, not kept
- Negative, score under 10 and not impact 5: recorded, revisited at the next scan
- Positive, act, score 10 or more: written into the problem framing as a success signal, so it is measured rather than hoped for

## Reading the result

- **Every consequence is intended and positive.** The session did not happen; the room restated the pitch. Rerun it with someone from outside the team asking the five prompts.
- **Nothing sits in act.** The team has put every negative outside its own control. Ask of each influence and monitor row what the team could change to make it less likely; most have at least one design lever.
- **The scan changed nothing in the plan.** Count the negative act rows scoring 10 or more and the plan changes they produced. Zero changes from one or more such rows means the scan was performed, not used.
- **Monitor rows with no signal.** These are worries, not monitoring. Each one gets a signal and a threshold or is removed.
- **A cluster of negatives on one group.** If three or more negative rows name the same group, that group belongs in section 2 of the responsible AI impact assessment, or in the personas, with someone from it consulted.

## ILLUSTRATIVE example

Invented. Mossgate Commons, a fictional neighbourhood tool-lending library run as a members' app, plans a public map showing which members hold which tools. Scan run 2026-10-14, 75 minutes, six people including the volunteer who runs the phone line. All scores are ILLUSTRATIVE.

| # | Consequence | Intended? | Positive or negative | Group | L | I | Score | Sort | Decision | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Members borrow a tool instead of buying one | Intended | Positive | Members | 4 | 3 | 12 | Act | Success signal: loans per active member per month | Bea Tregarthen, coordinator |
| C2 | The map shows which homes hold valuable tools, and a burglar uses it | Unintended | Negative | Lenders and their households | 2 | 5 | 10, sorted as 25 | Act | Map shows areas of roughly 500 metres, never addresses; exact address shared only after a loan is confirmed; before the map ships, 2026-11-20 | Jun Mirren, volunteer app lead |
| C3 | Members without smartphones lose access as loans move into the app | Unintended | Negative | Older and offline members | 3 | 3 | 9 | Act | Under 10, recorded; the phone line stays, revisit at next scan | Bea Tregarthen |
| C4 | A scraper copies the map into a dataset of who owns what | Unintended | Negative | Lenders | 3 | 4 | 12 | Act | Map visible only when signed in, rate-limited per account; before the map ships, 2026-11-20 | Jun Mirren |
| C5 | Lenders feel obliged to lend to neighbours they would rather not | Unintended | Negative | Lenders | 3 | 2 | 6 | Act | Under 10, recorded; a "not available" toggle that needs no reason is cheap, added anyway | Jun Mirren |
| C6 | The local hardware shop loses tool-hire income | Unintended | Negative | A business that is not a member | 2 | 3 | 6 | Influence | Under 10, recorded; offer the shop a listing as a lender | Bea Tregarthen |
| C7 | Home insurers refuse claims for tools lent to strangers | Unintended | Negative | Lenders | 2 | 3 | 6 | Monitor | Signal: any member report of a refused claim; the first report triggers a review | Bea Tregarthen |

The arithmetic for C2: 2 x 5 = 10, and the impact-5 rule sorts it as 25, the top of the list, ahead of C1 and C4 at 12. That ordering is the point of the rule: the burglary path ties for the least likely row on the sheet and is the one that changed the design most, from a pin per home to an area per neighbourhood. Two negative act rows at 10 or more, C2 and C4, produced two plan changes, so the scan was used. C3 sits just under the line, and the room chose to record it rather than act; the phone-line volunteer's objection is noted on the sheet, because the next scan should test whether the score was too low.

## The trap

The room scores its own blind spots low. Consequences for people who are not in the room, offline users, bystanders, a neighbouring business, get impact 2 because nobody present has felt them, while consequences for the team's own metrics get careful attention. The tell: every row naming a group not represented in the room scores impact 2 or less, and the basis for those scores is somebody's guess. The fix is structural rather than moral: bring one person who talks to that group every week, or mark those rows "not consulted" and carry them into the [responsible AI impact assessment](../../templates/ai/responsible-ai-impact-assessment.md) section 2 as open fields with an owner. A scan whose unintended negatives all landed in monitor is the other version of the same trap: the team found the problems and placed every one outside its own reach.

## Feeds

- [Problem framing](../../templates/discovery/problem-framing.md): positive act rows become success signals, and the decisions that narrow scope become the out-of-scope line
- [Responsible AI impact assessment](../../templates/ai/responsible-ai-impact-assessment.md): affected groups into section 2, negative rows into section 3 with their scores rescored on that template's severity scale
- [Risk register](../../templates/execution/risk-register.md): negative act and influence rows scoring 10 or more, with the same owner
- [Trust and safety harm model](../../templates/delivery/trust-safety-harm-model.md): any row a bad actor drives becomes a vector in its section 3
- Companion sheet: the [premortem worksheet](../execution/premortem-worksheet.md) asks how the project fails; this sheet asks who the project affects when it succeeds
- DISCOVER stage, feeds Gate 1; reruns feed Gate 3 through the impact assessment
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
