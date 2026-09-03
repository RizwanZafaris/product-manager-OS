---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/execution/risk-register.md", "templates/operate/post-launch-review.md", "templates/execution/dependency-register.md"]
method: "knowledge/INDEX.md"
aliases: ["Premortem Worksheet", "premortem-worksheet"]
---
# Premortem Worksheet

Based on the ideas of Gary Klein, from "Performing a Project Premortem", Harvard Business Review (2007). Explained here in this repository's own words.

This is the form the [program-premortem skill](../../skills/program-premortem/SKILL.md) drives. The skill brings the twelve failure modes and the interview; this worksheet is the paper the session fills in. Run the skill when you want the modes checked against a plan; run the worksheet alone when you have a room and an hour.

## What it is for

Prospective hindsight. Told that a project has already failed, people produce more causes, and more specific ones, than when asked what might go wrong, because certainty removes the social cost of pessimism. The worksheet captures the failure headline, the causes by category, the votes, and the mitigations with owners, and it ends with one committed sentence naming the most likely cause. The decision it improves is which risks get owners before the plan is signed rather than after it fails.

## Run it when

- Before Gate 3, as the risk half of "architecture and risks reviewed"
- Before kickoff of anything with three or more teams or an external dependency
- Before a cutover, migration, or regulated go-live
- When status has been green for six weeks and instinct disagrees

**Skip it when:** the plan does not exist yet. A premortem on an intention produces causes like "we lost focus", which nobody can own. Write the plan, then kill it on paper.

## Inputs you need first

- The plan: the roadmap row, the charter, the PRD, or the cutover runbook
- The [risk register](../../templates/execution/risk-register.md) and [dependency register](../../templates/execution/dependency-register.md) as they stand
- The people who will do the work, plus one outsider who will not
- Sixty minutes, and a facilitator who is not the sponsor

## The worksheet

### Step 1: the failure headline

| Field | Answer |
|---|---|
| Date of failure | [six months out, or launch plus one quarter] |
| Headline, past tense, one sentence | [what a colleague would say happened] |

The tense is the method. "Might fail" invites rebuttal; "failed" invites explanation.

### Step 2: causes

Three minutes of silent writing, then round robin, one cause per person per turn until the room is empty. No discussion, no rebuttal.

| # | Cause (past tense, specific: what happened, when, who noticed first) | Category | Author's role | Already on the register? (row number or no) |
|---|---|---|---|---|
| | | | | |

Categories match the register: value, usability, feasibility, viability, delivery, security, plus people and external.

### Step 3: votes

Each person has three likelihood votes and one unrecoverable vote, for the cause the team could least recover from. Score = likelihood votes + 2 x unrecoverable votes.

| Cause # | Likelihood votes | Unrecoverable votes | Score |
|---|---|---|---|
| | | | |

### Step 4: mitigations

Every cause scoring 3 or more, and every cause with an unrecoverable vote regardless of score.

| Cause # | Smallest intervention (one artifact, rule, or meeting change) | Owner (one name) | By when | Early warning signal | Register row |
|---|---|---|---|---|---|
| | | | | | |

### Step 5: the sentence

"It is [date] and the initiative failed. The most likely cause, given the table above, was [one cause]."

Facilitation rules: the outsider's causes are read first; the sponsor speaks last and votes last; "that won't happen" is out of order until step 4; no names in cause cells.

## Reading the result

A top cause already on the register with a mitigation is confirmation; a top cause absent from the register is the finding, and the register was the thing being tested. Half the causes in one category is a structural gap: all delivery means the plan is a date list, all viability means nobody has checked the business case. A cause with many likelihood votes and no unrecoverable vote is a schedule risk and gets a date; a cause with an unrecoverable vote and few likelihood votes still gets an owner, by the same logic as the impact-5 line in the [risk matrix](risk-matrix.md). Votes spread evenly across ten causes mean the room hedged; ask for the sentence anyway, and let the silence do its work.

## ILLUSTRATIVE example

Invented session for Ledgerline's expense-report copilot before rollout wave 3, which extends the copilot to all 4,000 employees. Seven people, one outsider from the support team.

Headline: "It is six months from now, and finance switched the copilot to draft-only after the auditors questioned first-pass approvals."

| # | Cause | Category | Register? |
|---|---|---|---|
| 1 | Managers approved copilot drafts without reading them; accounts-payable corrections doubled in month two | viability | no |
| 2 | The receipt mailbox connector hit provider rate limits at month end | delivery | row 1 |
| 3 | Policy rules encoded in March were stale by June because policy changes had no owner | delivery | no |
| 4 | Inference cost rose with volume and finance froze the budget | viability | no |
| 5 | Support had no runbook for "the copilot misread my receipt" tickets | delivery | no |
| 6 | The engineer who tuned the thresholds left | people | row 4 |
| 7 | Security review found receipts retained past the policy period | security | no |
| 8 | Sales sold the copilot to an account running a different expense system | external | no |

Votes: cause 1 scored 11 (five likelihood, three unrecoverable); causes 3 and 7 scored 6; cause 2 scored 4; cause 4 scored 3. Mitigations: cause 1, a sampling review of one in ten approvals by accounts payable with a public correction-rate guardrail, owned by the finance controller before wave 3, early signal corrections above 3 percent; cause 3, a RACI row making the controller accountable for policy rules with a monthly review, owned by the copilot PM; cause 7, a retention rule in the data model signed by the security reviewer before Gate 3. Five new register rows. The sentence: "The most likely cause was managers rubber-stamping drafts, which turned a time saving into an audit finding."

## The trap

The premortem that turns back into a brainstorm. The facilitator lets "might" into the room, causes arrive as categories ("integration risk") instead of events with dates, the sponsor speaks second and explains why each cause is handled, votes spread evenly, and the sentence hedges across three causes. Nothing lands on the register, and the session is remembered as having been done. The tells are visible on the page: no past tense in the cause column, no cause scoring above 4, and a sentence with an "or" in it.

## Feeds

- [Risk register](../../templates/execution/risk-register.md), section 2, one row per mitigated cause, with the session date in the register header's premortem field
- [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md), whose checklist asks that a premortem ran and the register absorbed it
- [Post-launch review](../../templates/operate/post-launch-review.md), section 5, where the causes are reconciled against what arrived
- [Dependency register](../../templates/execution/dependency-register.md), for causes that are another team's date
- The [program-premortem skill](../../skills/program-premortem/SKILL.md), which drives this form and adds the twelve failure modes
- Method background: [premortem entry in the knowledge index](../../knowledge/INDEX.md)
