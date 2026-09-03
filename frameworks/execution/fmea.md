---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/execution/risk-register.md", "templates/operate/operational-readiness-review.md", "templates/definition/nfr.md"]
method: "knowledge/INDEX.md"
aliases: ["Failure Modes and Effects Analysis", "fmea"]
---
# Failure Modes and Effects Analysis

Based on the US military standard MIL-P-1629 (1949), adopted by NASA for the Apollo programme and by Ford from the late 1970s. Explained here in this repository's own words.

## What it is for

Walking a system step by step and asking, at each step, how it can fail, what that failure does to somebody, why it happens, and what would catch it. The [risk matrix](risk-matrix.md) scores risks the team already named; the [premortem](premortem-worksheet.md) invents causes for one big failure. FMEA is the third shape: it enumerates failure modes function by function, so the ones nobody thought to name get written down anyway. It resolves the design review where an engineer says "that edge case is handled" and nobody can say by what, and the launch meeting where a control is described but never traced to the failure it is supposed to catch.

**The decision it feeds:** for each failure path, whether it ships as designed, ships with a named control, or sends the design back before [Gate 3](../../os/STAGE-GATES.md) and [Gate 5](../../os/STAGE-GATES.md). A severity-5 row is a design decision, not a mitigation decision, and this sheet is what forces that distinction into the open.

## Run it when

- Before Gate 3, on any flow that moves money, touches personal data, or writes to a system of record
- Before Gate 5, on the failure paths a new integration or a new model introduces
- After the second incident with the same shape, when [five whys](five-whys-fishbone.md) has produced a cause and you want to know where else that cause lives
- Before handing a service to an on-call rotation that did not build it

**Skip it when:** the design is not settled. FMEA on a sketch produces failure modes for functions that will not exist, and the sheet is then wrong in a way that reads as thorough. Also skip it for a flow with one step and no downstream consumer, where the failure mode and the effect are the same sentence.

## Inputs you need first

- The flow as steps or functions, from the design brief, the sequence diagram, or the runbook
- The effects the business actually cares about, from the [NFR](../../templates/definition/nfr.md) and the [acceptance criteria](../../templates/definition/acceptance-criteria.md)
- The existing controls: validations, alerts, reconciliations, reviews. Name them, do not assume them
- The incident history for this system and its neighbours, from [incident postmortems](../../templates/operate/incident-postmortem.md)
- The engineer who built each step, the person who supports it, and ninety minutes

## The worksheet

### Step 1: the three scales

Severity, the worst credible effect of this failure mode on a user, a customer, or the business:

| S | Meaning |
|---|---|
| 1 | Cosmetic. Somebody notices and nothing changes |
| 2 | One person loses time or redoes work. No external effect |
| 3 | A team absorbs manual rework, or a customer complains and is made whole |
| 4 | A commitment is missed, a period close slips, or a customer escalates formally |
| 5 | Money moves wrongly, a contract or regulation is breached, or personal data leaks |

Occurrence, how often this cause produces this failure mode within the initiative's horizon:

| O | Meaning |
|---|---|
| 1 | No precedent here or in systems like it |
| 2 | Has happened to teams like ours, not to us |
| 3 | Has happened to us in the last two years |
| 4 | Happens in a normal month, or a precondition is already true |
| 5 | Happens most weeks and is treated as normal |

Detection, and note the inversion: a **low** number is good, because it means something catches the failure early.

| D | Meaning |
|---|---|
| 1 | An automatic control blocks the failure before it leaves the system, every time |
| 2 | An automatic check flags it and a human must clear the flag before it proceeds |
| 3 | A routine human review would probably catch it before it reaches anyone outside |
| 4 | Found downstream: at the close, in a reconciliation, or in an audit |
| 5 | Nothing looks for it. You learn from a complaint, or you never learn |

The classic automotive form scores each of these 1 to 10. Five points is enough here, and deliberately coarse: a ten-point scale invites an argument about a 6 versus a 7 that no software team can settle with evidence, and the ranking below does not use the product anyway, so the extra resolution buys nothing. Anchor descriptions are what make two scorers agree, not extra numbers.

### Step 2: how the rows get ranked, and the method that is deprecated

Risk priority number, **RPN = S x O x D**, range 1 to 125.

Ranking by RPN alone is now discouraged by current AIAG and IEC guidance, and this repository treats it as the deprecated method. The reason is arithmetic: equal products carry unequal severities. A severity-5 failure at occurrence 2 and detection 3 and a severity-2 failure at occurrence 5 and detection 3 both score 30, and the multiplication has erased the only difference that matters. Sorting by RPN then hands the team a queue where a contract breach and an untidy line item sit side by side.

What to do instead, in this order:

1. **Screen on severity first.** Read every severity-5 row before any other row, whatever its product. Then every severity-4 row.
2. **Assign an action priority from the table below,** which treats a high-severity item as actionable regardless of its product.
3. **Keep the RPN column, and use it only within one action-priority band,** as a tiebreak for sequencing work you have already decided to do.

| S | Condition on O and D | Action priority |
|---|---|---|
| 5 | any O, any D | High |
| 4 | O of 3 or more, or D of 4 or more | High |
| 4 | O of 2 or less and D of 3 or less | Medium |
| 3 | O of 4 or more, or (O of 3 and D of 4 or more) | High |
| 3 | O of 3 and D of 3 or less, or O of 2 or less and D of 4 or more | Medium |
| 3 | O of 2 or less and D of 3 or less | Low |
| 2 | O of 4 or more and D of 4 or more | Medium |
| 2 | anything else | Low |
| 1 | any O, any D | Low |

What each band obliges:

| Action priority | Obligation |
|---|---|
| High | An action with an owner and a date before the gate, or a written reason for accepting it, signed by the sponsor |
| Medium | An action with an owner, or a recorded acceptance in the [risk register](../../templates/execution/risk-register.md)'s accepted section |
| Low | Action optional. Record that you looked and chose not to act |

### Step 3: the analysis sheet

<!-- One row per failure mode, not per step: a step with three ways to fail gets three rows. Write the failure mode as what the system does, and the effect as what a person outside the team experiences. If the effect cell needs the word "potentially", you have not found the effect yet. -->

| # | Step or function | Failure mode (what the system does) | Effect (on whom, and what they lose) | S | Cause (why it does that) | O | Current control, named | D | RPN (deprecated, tiebreak only) | Action priority |
|---|---|---|---|---|---|---|---|---|---|---|
| | [step] | [failure mode] | [effect] | [1 to 5] | [cause] | [1 to 5] | [control, or "none"] | [1 to 5] | [S x O x D] | [High / Medium / Low] |

### Step 4: the action sheet

Every High row, and every Medium row the team chooses to act on.

<!-- Prevention changes the cause, so it moves O. Detection changes what catches it, so it moves D. Only a design change that shrinks the effect moves S. Write which of the three you are doing; a list where every action is a new alert will not reduce how often the failure happens. -->

| # | Action | Type (prevent / detect / reduce the effect) | Owner (one role) | By when | S after | O after | D after | Action priority after | Register row |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## ILLUSTRATIVE example

Invented analysis for Ledgerline's expense-report copilot, on the submit-and-code flow, before Gate 3 of rollout wave 3. Every number below is ILLUSTRATIVE.

| # | Step | Failure mode | Effect | S | Cause | O | Control | D | RPN | AP |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Assign the expense to a cost code | Codes a personal expense as client-billable | The client is invoiced for a cost their contract excludes; credit note and a contract conversation | 5 | Merchant category maps to a billable code with no client-context check | 2 | Billing reviews the batch before invoicing | 3 | 30 | High |
| 2 | Extract the amount from a receipt image | Reads the pre-tip subtotal as the total | The employee is reimbursed short and files a correction | 2 | Split-line restaurant receipts carry two totals in one block | 5 | The employee sees the figure at submission | 3 | 30 | Low |
| 3 | Poll the receipt mailbox | Stops polling and reports no error | Reports are submitted with no receipts attached; the period close slips | 4 | The provider's rate limit returns an empty page with a success status | 3 | None. The volume drop looks plausible | 4 | 48 | High |
| 4 | Retain receipt images | Keeps images past the retention period | A reportable finding at the next privacy audit | 5 | No deletion job; retention exists only in a policy document | 3 | None | 5 | 75 | High |
| 5 | Apply the policy rule table | Applies a rule that a policy change superseded | Non-compliant claims are approved and finance reverses them by hand | 3 | No owner for the rule table, so it is edited when somebody remembers | 4 | A quarterly spot check by finance | 4 | 48 | High |
| 6 | Render the merchant name on the report line | Truncates a long merchant name | The line looks untidy. Nobody is blocked | 1 | Fixed column width in the report view | 4 | Visible on screen | 2 | 8 | Low |

Rows 1 and 2 are the deprecation in miniature: both score 30, and one of them invoices a client for something their contract excludes. Under an RPN sort, row 1 would rank below row 5 and level with a tip-rounding annoyance. Severity screening puts it first.

Actions on the High rows:

| # | Action | Type | Owner | By when | S | O | D | AP after |
|---|---|---|---|---|---|---|---|---|
| 1 | The copilot may propose a billable code but cannot apply one; a human picks the client. The worst outcome becomes an internal re-code | reduce the effect | copilot PM | before wave 3 | 2 | 2 | 2 | Low |
| 3 | Treat an empty page with a success status as an error, add backoff, and alert on zero receipts for thirty minutes in business hours | prevent and detect | engineering lead | before wave 3 | 4 | 1 | 1 | Medium |
| 4 | Retention field in the data model plus a scheduled deletion job, signed off by the security reviewer | prevent | engineering lead | before Gate 3 | 5 | 1 | 2 | High |
| 5 | Name the finance controller accountable for the rule table in the RACI, with a monthly review and a change hook from the policy owner | prevent | copilot PM | before wave 3 | 3 | 2 | 3 | Low |

Row 4 is the instructive one. The action removes almost all of the occurrence and most of the blindness, and the band does not move, because a leak is still a leak. It stays on the Gate 3 agenda with the sponsor's signature next to it. Row 3 shows the other lesson: the alert alone would have left the band where it was, and only fixing the cause moved it.

## Reading the result

Read the severity-5 rows as a list of design decisions and take them to the design review, not to the risk register. Then count High rows against the weeks left; more High rows than the team can act on before the gate means the scope is wrong, and that is a conversation with the sponsor rather than a longer sheet.

Three patterns are worth looking for on the page. A control column full of phrases like "the user will notice" is not a control column; it is a customer doing your quality assurance, and every one of those rows is really a detection-5. An action sheet where every action is prevent-free, all alerts and reviews, will show occurrence unchanged in the after columns, and the failure will keep happening on the same cadence with a faster notification. And a cluster of failure modes sharing one cause is a structural finding: fix the cause once rather than the six modes separately, and run [five whys](five-whys-fishbone.md) on it.

## Where the output lands

Carry the High rows into the [risk register](../../templates/execution/risk-register.md) with their triggers, section 2 for the owned ones and section 3 for the accepted ones, so the two documents do not diverge. Where a row's action is a new operational check, it also belongs in the [operational readiness review](../../templates/operate/operational-readiness-review.md), sections 2 and 6, or the check exists on this sheet and nowhere the on-call can see it. A detection control that needs a number becomes a target with an owner in the [NFR](../../templates/definition/nfr.md). The severity-5 rows reach [Gate 3 and Gate 5](../../os/STAGE-GATES.md) by name, with the design decision on each recorded there.

## Re-run trigger

Re-run when the flow gains or loses a step, when a new integration or model version enters it, and after any incident whose failure mode is not already a row on the sheet. Between those, revisit the occurrence column at the start of each planning period, because occurrence is the column that rots: a cause that was rare last quarter may now happen in a normal month, and nothing in the sheet notices on its own.

## The trap

The sheet that becomes an inventory. A team enumerates two hundred failure modes at one row per field validation, scores them in an afternoon, and produces a document nobody reads twice. The tells are visible: effects written as restatements of the failure mode, severity clustered at 3, "monitoring" as the control on half the rows, and no design change anywhere in the action sheet. It also misleads by construction in two specific conditions. First, single-point analysis: FMEA looks at one failure mode at a time, so a pair of individually harmless failures that are catastrophic together will not appear on any row, and the sheet will read as clean. Second, invented occurrence: with no incident history and no telemetry, the occurrence column is a group's collective guess wearing a number, and the action priority table will then rank confidently on the softest input on the page. Write the basis for each occurrence score next to it, or state on the sheet that occurrence is unevidenced and the ranking is provisional.

## Feeds

- [Risk register](../../templates/execution/risk-register.md), section 2 for every High row with its owner and trigger, section 3 for the accepted ones
- [Gate 3 and Gate 5](../../os/STAGE-GATES.md), where severity-5 rows appear by name and the design decision on each is recorded
- [Operational readiness review](../../templates/operate/operational-readiness-review.md), sections 2 and 6, for the detection controls this sheet created
- [NFR](../../templates/definition/nfr.md), where a detection control that needs a number becomes a target with an owner
- [Post-launch review](../../templates/operate/post-launch-review.md), where the failure modes that actually arrived are reconciled against the sheet
- [Risk matrix](risk-matrix.md) for scoring the rows that turn out to be initiative-level risks, and the [premortem worksheet](premortem-worksheet.md) for the failure this sheet is too granular to see
- The [launch-readiness skill](../../skills/launch-readiness/SKILL.md) and the [reg-gap-check skill](../../skills/reg-gap-check/SKILL.md), both of which ask what catches a given failure
- Method background: [knowledge index](../../knowledge/INDEX.md)
