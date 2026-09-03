# Risk Matrix

Based on the probability and impact matrix as codified in the US military system-safety standard MIL-STD-882 (1969) and later in the risk management standard ISO 31000 (2009). Explained here in this repository's own words.

## What it is for

Scoring risks on likelihood and impact with scales defined tightly enough that two people score the same risk the same way, then drawing the appetite lines that say which scores demand action. The question it answers is which ten of forty risks deserve the team's attention this week. The [risk register](../../templates/execution/risk-register.md) defaults to a 3 by 3 on purpose, because a fine scale invents precision; this 5 by 5 is for the register that has grown past fifteen open rows and has six of them tied at the top with no way to order them. Whichever scale you use, write it in the register's section 1 so the two documents agree.

## Run it when

- The register has more open rows than the weekly review can walk
- Before Gate 3, when the premortem has added rows and the top band needs owners
- A sponsor asks which risks they should personally hear about
- Two reviewers keep scoring the same risk two bands apart

**Skip it when:** the register has under ten rows. The 3 by 3 in the register already ranks them, and a 5 by 5 debate about whether a risk is a 3 or a 4 costs more than the ranking is worth.

## Inputs you need first

- The register rows, each written as an event that could happen
- The initiative's horizon, because likelihood is scored within it
- The sponsor's stated appetite: the score above which they must be told, and the categories where they accept less
- The [premortem](premortem-worksheet.md) output, which supplies the rows the plan did not think of

## The worksheet

### Step 1: the scales

Likelihood within the horizon: 1 rare, no precedent in this team's history; 2 unlikely, has happened to teams like ours, not to us; 3 possible, has happened to us in the last two years; 4 likely, has happened to us in the last year, or early signs are already visible; 5 almost certain, a precondition is already true.

Impact, worst credible outcome, highest of the three dimensions (time, customers, commitments): 1 minor, under a week of one team's time and no customer notices; 2 moderate, a sprint slips or a few customers notice, nothing breached; 3 significant, a milestone slips by more than a month, or a customer commitment is breached, or a compliance finding; 4 major, a gate cannot pass this quarter, or revenue or a regulatory deadline is at risk; 5 severe, the initiative fails or the company faces a reportable incident.

Score = L x I, from 1 to 25.

| Likelihood, then impact | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 5 | 5 | 10 | 15 | 20 | 25 |
| 4 | 4 | 8 | 12 | 16 | 20 |
| 3 | 3 | 6 | 9 | 12 | 15 |
| 2 | 2 | 4 | 6 | 8 | 10 |
| 1 | 1 | 2 | 3 | 4 | 5 |

### Step 2: the bands and appetite lines

| Band | Score | What it requires | Review |
|---|---|---|---|
| Low | 1 to 4 | Accept, signed by name in the register | Quarterly |
| Medium | 5 to 9 | A mitigation plan with a date | Monthly |
| High | 10 to 15 | A named owner, a trigger, and an active mitigation | Weekly |
| Critical | 16 to 25 | All of the above, plus escalation to the sponsor and a line on the next gate's agenda | Weekly, and at every status report |

Appetite lines, set by the sponsor and written here: any risk with impact 5 sits in the top band regardless of likelihood, because multiplication flattens tails; the sponsor is told personally above [score]; security and compliance rows move up one band. The rule for the top band: a named owner and a trigger, where a trigger is an observable signal that the risk is starting to happen, not the date of the next review.

### Step 3: the scoring sheet

| # | Risk (event) | Category | L | Basis for L | I | Basis for I | Score | Band after appetite | Owner | Trigger | Response (mitigate / accept / transfer / avoid) | Review date |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | |

The basis columns are the method. A score without a basis is a feeling, and two feelings will disagree next week.

## Reading the result

More than a fifth of the rows in the top two bands means the plan is wrong, not the register; take it back to DESIGN. Nothing above 9 means the register is decoration or the team has stopped imagining; run the premortem. Score the residual after mitigation as a second number, so the register shows what the mitigation buys. Watch movement: a score that rises two reviews running is the one to escalate, whatever its absolute value. A trigger that has fired and a risk that is still "open" is an incident wearing a risk's clothes.

## ILLUSTRATIVE example

Invented rows for Ledgerline's expense-report copilot before Gate 3.

| # | Risk | L | I | Score | Band | Owner | Trigger |
|---|---|---|---|---|---|---|---|
| 1 | Receipt mailbox connector is rate-limited by the email provider at month end | 4 (happened in wave 1) | 3 | 12 | high | engineering lead | connector error rate above 2 percent for 15 minutes |
| 2 | Auditors reject copilot-drafted reports as insufficient evidence | 2 | 5 | 10 | critical, by the impact-5 line | finance controller | any audit query naming the copilot |
| 3 | Inference cost per report exceeds the budgeted rate | 3 | 2 | 6 | medium | copilot PM | cost per report above $0.40 for two weeks |
| 4 | The engineer who tuned the category thresholds leaves | 2 | 3 | 6 | medium | engineering manager | notice given, or a second job posting in that skill |
| 5 | Managers approve copilot drafts without reading them | 4 | 4 | 16 | critical | head of product | post-approval corrections above 3 percent of approved reports |

Row 2 shows the appetite line doing its work: a 10 would sit in the high band, but an impact of 5 puts it in critical with sponsor visibility. Row 5 gets a sampling review as its mitigation and is on the Gate 3 agenda.

## The trap

Multiplication hides the tail. A rare catastrophe scores 5 and sits below a likely nuisance at 6, and the weekly review spends its time on the nuisance. The impact-5 line exists because of this, and the other half of the fix is scoring impact on the worst credible outcome rather than the average one. Teams that argue for ten minutes about a 3 versus a 4 usually have no basis column; fill it, and the argument becomes a question about evidence.

## Feeds

- [Risk register](../../templates/execution/risk-register.md), section 1 (the scale you used) and section 2 (the rows, with the top band's owners and triggers)
- [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md), whose checklist asks that every high-scoring risk has a named owner and a review date
- [Premortem worksheet](premortem-worksheet.md), which feeds rows in; the [escalation skill](../../skills/escalation/SKILL.md), which takes critical rows out
- [Status report](../../templates/execution/status-report.md), where critical rows appear every week
- Method background: [Cagan's four risks](../../knowledge/cagan-product-teams.md) for the category column, and the [program-premortem skill](../../skills/program-premortem/SKILL.md)
