# RACI

Based on responsibility charting, a management practice from the 1970s with no single documented originator, later codified as the responsibility assignment matrix in the Project Management Institute's PMBOK Guide (1996 onward). Explained here in this repository's own words.

## What it is for

For each decision area or deliverable, who does the work (Responsible), who answers for the outcome (Accountable, exactly one), who is asked before the decision (Consulted, two-way), and who is told after it (Informed, one-way). The question it answers is the one that costs a meeting every time it is asked without a chart: who actually decides this. The decision it improves is every later decision, because the chart removes the moment where six people discover that none of them owns the call.

## Run it when

- Writing a program charter, or kicking off anything with three or more teams
- A decision has stalled twice and each time a different person was "waiting on" someone else
- Defining the handoffs between agents and humans in an agent team
- After a reorganisation, when the old chart names roles that no longer exist

**Skip it when:** one team of five sits in one room shipping one thing. The chart would take a morning and everyone already knows; write the owner's name in the one-pager instead.

## Inputs you need first

- The list of decision areas and deliverables, from the program charter, PRD section 4, and the [stakeholder map](../../templates/execution/stakeholder-map.md) section 2
- The people, by role, from the stakeholder map section 1
- The escalation ladder from the [dependency register](../../templates/execution/dependency-register.md), for what happens when an A is missing

## The worksheet

### Step 1: the chart

| Decision area or deliverable | R: does the work (one or more) | A: answers for it (exactly one name) | C: asked before, and can change it (at most three) | I: told after | Forum and cadence where A decides |
|---|---|---|---|---|---|
| Scope changes | | | | | |
| Budget | | | | | |
| Launch go or no-go | | | | | |
| Priority order | | | | | |
| [add areas] | | | | | |

Letter rules. R does the work and may be several people; at least one per row. A is one named person who can say no to the R's work and is the person the sponsor calls; A may also be R. C is consulted before the decision and the consultation is two-way: a C who cannot change the outcome is an I. I hears afterwards and has no vote. A blank cell is allowed and means "nobody", which is a finding to record, not a gap to hide.

### Step 2: the checks

| Check | Rule | Fail signal | Fix |
|---|---|---|---|
| One A per row | Exactly one name | Zero, or two names, or a team name | The two A's shared manager picks one; a team becomes its lead |
| A is a person | A name, never a committee | "Steering committee" | Name the chair |
| C load | At most three per row | Five C's on a row | Move the rest to I; a decision with five consultees is made by attrition |
| A load | No person is A on more than a stated number of rows (write the number here: [n]) | One name in every A cell | Delegate, or accept that this person is the bottleneck and plan around it |
| R exists | At least one R per row | An A with nobody doing the work | The row is a wish; assign or delete |
| Forum exists | Every A has a calendar slot where they decide | "As needed" | Put it on the calendar or accept the delay |
| Signed | Every A has agreed to their row in writing | Silence taken as consent | Ask; an A who never agreed is not accountable, they are surprised |

Decision rule: a row failing two or more checks goes back to the sponsor before the charter is signed. A chart with more than a quarter of its rows failing is not a chart, it is a symptom; run the stakeholder power-interest grid to find out why nobody wants to own the decisions.

## Reading the result

Read the columns, not just the rows. One name in most A cells is a bottleneck that will set the program's pace. A row with many C's and one R is a decision that will be re-litigated after it is made. An A who is never R is normal for an executive; an R who is A on everything is a hero, and heroes go on leave. A column of I's for a function that can block launch (legal, security, support) means the chart has already made a mistake. Everyone consulted and no one accountable is the classic failure: a chart that grants every stakeholder a veto and nobody a decision.

## ILLUSTRATIVE example

Invented chart for Ledgerline's expense-report copilot rollout, roles only.

| Decision area | R | A | C | I | Forum |
|---|---|---|---|---|---|
| Expense policy rules encoded in the copilot | policy analyst | finance controller | PM, legal counsel | engineering lead, support lead | monthly policy review |
| Model threshold and prompt changes | ML engineer | copilot PM | finance controller, security reviewer | support lead | weekly product review |
| Launch go or no-go per rollout wave | release manager | head of product | customer success lead, finance controller | sales lead | wave readiness review, 48 hours before each wave |
| Receipt data retention period | data engineer | security reviewer | legal counsel | PM | quarterly security review |
| Customer-facing comms | product marketer | copilot PM | support lead | sales lead | launch comms review |
| Inference spend | copilot PM | VP product | finance business partner | engineering lead | monthly budget review |

Two checks failed in the first draft: the policy row had "finance team" as A, fixed to the controller; the model row had both the PM and the controller as A, fixed by making the controller C with a stated right to block threshold changes that touch policy, which is what a C is for.

## The trap

The chart the PM wrote alone. It is drafted in an afternoon, circulated, and silence is taken as agreement. At the first contested decision, the named A says they never agreed to own it, and the chart, which was supposed to end that argument, starts it. The signed check exists because of this. The related failure is C as a courtesy: people listed as consulted who hear about the decision afterwards, then object, and are right to, because "consulted" was a promise the chart made and nobody kept.

## Feeds

- [Stakeholder map](../../templates/execution/stakeholder-map.md), section 2, decision areas, which carries the chart between gates
- [Program charter](../../templates/planning/program-charter.md), the governance section
- [Agent team protocol](../../agents/TEAM.md), for the human gate owner and handoff packets
- [Decision log](../../templates/execution/decision-log.md): every entry names the A who made it
- First required at [Gate 2: requirements signed off](../../os/STAGE-GATES.md), reviewed at every gate after
- Method background: [triad decision rights](../../knowledge/roles/triad-decision-rights.md), the default split the chart starts from
