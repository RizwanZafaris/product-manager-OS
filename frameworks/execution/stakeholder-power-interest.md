---
layer: frameworks
stage: DEFINE
gate: 2
feeds: ["templates/execution/stakeholder-map.md", "frameworks/execution/raci.md", "templates/execution/risk-register.md"]
method: "knowledge/high-output-management.md"
aliases: ["Stakeholder Power-Interest Grid", "stakeholder-power-interest"]
---
# Stakeholder Power-Interest Grid

Based on the ideas of Aubrey Mendelow, from his stakeholder mapping matrix as commonly cited (1991). Explained here in this repository's own words.

## What it is for

Sort the people who can affect the outcome by power (can they stop, fund, or reshape the work) and by interest (how much attention they pay right now), then choose an engagement mode per quadrant. The question it answers is where the PM's scarce engagement hours go, and which people must be met before a gate rather than discovered at it. Four modes: manage closely, keep satisfied, keep informed, monitor. The grid's value is the second quadrant, high power and low interest: the person who can stop the launch and is not paying attention until the week they do.

## Run it when

- Kickoff, and again before every gate, because both scores drift
- A decision stalls and nobody can name who is blocking it
- Entering a brownfield product with years of undocumented owners
- A sponsor changes, or a reorganisation moves a veto to a new desk

**Skip it when:** the initiative has one sponsor, one team, and one month. Write the sponsor's cadence in the one-pager and spend the afternoon on the work.

## Inputs you need first

- The candidate list: everyone who signed the last gate, budget owners, legal, security, support, operations, and whoever runs the system you integrate with
- Decision areas from the [RACI chart](raci.md), so power is scored against real decisions
- Each person's current concern in their own words, from conversations, not inferred from their title

## The worksheet

### Step 1: score

Power, 1 to 5: 1 no influence on this work; 2 can delay it; 3 can change its scope; 4 can stop it; 5 can stop it and move its budget. Interest, 1 to 5: 1 unaware; 2 aware, pays no attention; 3 attends when invited; 4 asks unprompted; 5 has an outcome of their own riding on it. Score from behaviour in the last 30 days, not from the org chart.

| Stakeholder (role) | Power | Evidence for the power score | Interest | Evidence for the interest score | Quadrant | Stance (sponsor / neutral / skeptic / opponent) |
|---|---|---|---|---|---|---|
| | | | | | | |

Quadrant rule: 4 or 5 is high on either axis. A 3 is treated as high, because over-engaging costs a meeting and under-engaging costs a veto.

### Step 2: the four modes

| Quadrant | Mode | What they get | Cadence floor | Relationship owner |
|---|---|---|---|---|
| High power, high interest | Manage closely | Co-ownership of decisions, early drafts, direct access | Every two weeks, plus before every gate | PM |
| High power, low interest | Keep satisfied | One-page summaries, no surprises, the single ask you need from them | Monthly, plus before any gate they sign | Sponsor, or the PM's manager |
| Low power, high interest | Keep informed | Working sessions, previews, credit for their evidence | Weekly channel update | PM or design lead |
| Low power, low interest | Monitor | The launch note | At launch | The comms owner |

### Step 3: the engagement plan

One row per person in the top two quadrants and per skeptic anywhere. This table is copied into the stakeholder map.

| Stakeholder | Quadrant | What they need to hear, in their terms | What you need from them | Who engages | By when | Movement target |
|---|---|---|---|---|---|---|
| | | | | | | [e.g. skeptic to neutral before Gate 3] |

## Reading the result

More than five people in "manage closely" means you are broadcasting, not managing; re-score honestly or find a co-owner. A high-power skeptic is engaged first, before any sponsor, because a sponsor's support is cheap to keep and a skeptic's veto is expensive to discover. The overlooked quadrant is low power and high interest: support staff, accounts-payable clerks, the people who will use the thing daily; they are the evidence base and the early-warning system, and keeping them informed costs a weekly note. Re-score at every gate. A sponsor whose interest fell from 5 to 2 between gates is a risk register row, not a relief.

## ILLUSTRATIVE example

Invented scores for Ledgerline's expense-report copilot before Gate 3, roles only.

| Stakeholder | Power | Interest | Quadrant | Stance |
|---|---|---|---|---|
| Chief financial officer | 5 | 2 | keep satisfied | neutral; wants audit safety, reads one page a month |
| Finance controller | 4 | 5 | manage closely | skeptic; fears auto-approval without evidence |
| Head of engineering | 4 | 3 | manage closely (3 treated as high) | sponsor |
| Security reviewer | 4 | 2 | keep satisfied; signs Gate 3 | neutral |
| Accounts-payable team lead | 2 | 5 | keep informed | sponsor; supplies the correction-rate evidence |
| Sales lead | 3 | 4 | manage closely | sponsor, with a habit of promising features |
| External auditors | 4 | 1 | keep satisfied, via the controller | unaware |

Engagement rows: the controller gets a working session on the sampling review before Gate 3, with the target of moving from skeptic to neutral; the security reviewer gets the retention design two weeks before the gate rather than at it; the auditors are reached only through the controller, with the evidence-retention note as the single ask.

## The trap

Scoring by title. The executive team fills the high-power row because they are executives, and the security reviewer at a middle grade is scored 2 because of where they sit. Then Gate 3 arrives and the reviewer, who signs it, has never seen the retention design. Power on this grid means power over this work, evidenced by what the person has stopped, funded, or changed in the last month; the evidence column is there to make a title-based score visibly empty. The companion failure is the one-time map: scored at kickoff, inherited at every gate, describing a company that has since reorganised.

## Feeds

- [Stakeholder map](../../templates/execution/stakeholder-map.md), section 1 (the scores) and section 3 (the engagement rows for the difficult quadrant)
- [RACI chart](raci.md): high-power stakeholders with no A or C cell are a finding for both sheets
- [Risk register](../../templates/execution/risk-register.md): sponsor drift and an unengaged veto-holder are risk rows
- [Program charter](../../templates/planning/program-charter.md), the governance section
- First required at [Gate 2: requirements signed off](../../os/STAGE-GATES.md), re-scored before every later gate
- Method background: [High Output Management](../../knowledge/high-output-management.md), the leverage argument behind spending engagement time where it moves the outcome
