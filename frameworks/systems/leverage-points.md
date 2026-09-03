---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/planning/roadmap.md", "templates/planning/product-strategy.md", "templates/planning/decision-memo.md"]
method: ""
aliases: ["Leverage Points", "leverage-points"]
---
# Leverage Points

Based on the ideas of Donella Meadows, from her paper "Leverage Points: Places to Intervene in a System" (1999). Explained here in this repository's own words.

## What it is for

The quarterly review where the team shipped eleven things, every one of them a threshold raised, a limit relaxed, a nudge retimed, and the metric has not moved. Meadows' argument is that places to intervene in a system are not equally powerful, and she ranked twelve of them, weakest at the numbers and strongest at the frame the whole system was designed inside. This worksheet does three things with that ranking: it places each candidate intervention on the rung it actually occupies, it audits which rungs last quarter's effort landed on, and it separates the strong moves the team can make alone from the strong moves that need one named person's yes. The practical point it forces into the open is uncomfortable: product teams spend nearly all their effort at the weakest end, tuning parameters, because a parameter is the easiest thing in the world to get approved. Nobody blocks a threshold change. Everybody blocks a rule change, so the rule change never gets proposed, and the backlog fills with knobs.

## Run it when

- A metric has been flat for two review cycles while the team shipped steadily and on time
- At the start of planning, before the backlog is scored, because [RICE](../prioritization/rice-scoring-sheet.md) ranks items at whatever altitude they arrive at and never asks whether the whole list is knobs
- A behavior keeps coming back after every fix (rubber-stamped approvals, reopened tickets, the same escalation each month), which means the loop producing it is untouched
- A sponsor asks why a fully delivered roadmap changed nothing in the business

**Skip it when:** the system is not running yet. Before first release there are no loops, no delays, and no rules anyone has felt, so every rung above the parameters is speculation dressed as insight; run [assumption mapping](../discovery/assumption-mapping.md) instead. Skip it mid-incident too, where the fix is the fix.

## Inputs you need first

- Everything shipped in the last two quarters, from the [roadmap](../../templates/planning/roadmap.md) change log, as a plain list
- The goal the system is actually run against, which is the one the incentives serve, not the one on the slide. [Product strategy](../../templates/planning/product-strategy.md) sections 1b and 3 hold the claimed version
- At least one loop drawn concretely, from [growth loops](../metrics/growth-loops.md) or the [north star input tree](../metrics/north-star-input-tree.md), so that "feedback loop" names a specific circuit rather than a gesture
- Who is allowed to change what: the [RACI](../execution/raci.md) and the [power-interest grid](../execution/stakeholder-power-interest.md) supply the authority column, and without it the sheet becomes a wish list

## The worksheet

### Step 1: the twelve rungs

<!-- Fill the last two columns for your own system. Leave a row blank if your product genuinely has no instance of it; a blank row at rung 7 or 8 is a finding, not a gap in the paperwork. -->

| Rung r | Meadows' place, in our words | What it looks like in a product | Our instance | Who can change it |
|---|---|---|---|---|
| 12 | Numbers: the constants somebody set once | Thresholds, limits, prices, timeouts, retry counts, headcount, copy and its timing | | |
| 11 | Buffers: the size of a stabilizing stock against the flows through it | Queue depth, credit balance, review capacity, slack in the release train | | |
| 10 | Stock and flow structure: the plumbing and where paths cross | The route a record actually takes, the hand-off nodes, the integration topology | | |
| 9 | Delays: how long a signal takes relative to how fast the system moves | Charge to draft, submit to approval, correction to retrain, ship to measured effect | | |
| 8 | Balancing loops: the strength of a correction against the error it must catch | Sampling audits, alerts, rate limits, anything whose job is to pull the system back | | |
| 7 | Reinforcing loops: the gain on the loops that compound, good and bad | Invite loops, correction-data loops, and the vicious ones nobody designed | | |
| 6 | Information flows: who can see what, and who cannot | Showing a consequence to the person who caused it. The strongest rung a product team routinely owns outright | | |
| 5 | Rules: incentives, permissions, constraints, penalties | Policy configuration, override rights, contract terms, what the team is measured on | | |
| 4 | Self-organization: the power to add or change structure | Admin-authored rules, learning from corrections, APIs and plug-ins. You trade control for adaptation | | |
| 3 | Goals: what the system is actually for | The objective the rules and incentives serve when nobody is watching | | |
| 2 | Paradigms: the shared assumption the goals grew out of | The unexamined belief about who owes what to whom | | |
| 1 | The power to hold a paradigm loosely | Running the exercise in which the artifact your product manages stops existing | | |

The rung numbers are an ordering, not a measurement. Rung 6 is not twice rung 12; it means only that information flows have beaten parameter tuning often enough for Meadows to rank them above it. Treat a two-rung difference as a tie.

### Step 2: the arithmetic

This scoring arithmetic, L, A, and altitude, is this repository's own invention, not Meadows'. Her paper ranks the twelve rungs; it assigns no numbers to them and proposes no authority scale. Treat L, A, and altitude as a local heuristic for sorting a worksheet, not as a figure Meadows would sign.

Leverage L = 13 minus r, so rung 12 gives L of 1 and rung 1 gives L of 12.

Authority A, scored against this quarter and this org chart: 3 the team can do it inside its own remit, no approval outside the triad; 2 one named person's yes; 1 several functions, a board, a contract renegotiation, or a market change. An A of 1 or 2 must name the person or the event, or it is scored one point higher.

Altitude = L x A, from 1 to 36.

The authority scale is deliberately three points wide. The rung is the judgment that carries the sheet, and it is already an ordinal borrowed from someone else's list; bolting a five-point authority scale onto it invites an hour of argument about whether the controller is a 3 or a 4 when the honest answer is to go and ask her. Never sum altitude down the sheet, and never average it. The product sorts rows inside a band; it does not rank a paradigm against a delay.

### Step 3: the effort audit

| Shipped item, last two quarters | Rung r | L = 13 minus r | Who approved it |
|---|---|---|---|
| | | | |

Parameter share P = (items at rungs 12 to 10) divided by (all items). Record P, and record who approved the parameter items against who approved anything above rung 9.

Two structural rules, neither of which is a benchmark: if the strategy names a differentiator and nothing shipped above rung 9 supports it, the roadmap is not executing the strategy, whatever the delivery report says. And if P was near 1 last quarter and is near 1 again, the team has a maintenance plan with a roadmap's title page. There is no correct value of P to hit, and any number quoted as an industry norm here would be invented; compare P against your own previous quarter and against what the strategy claims.

### Step 4: the intervention slate

| Candidate intervention | Rung r | Why that rung: the loop, rule, or flow it changes | L | A | Altitude | Reachable this quarter | If not, the one person to ask |
|---|---|---|---|---|---|---|---|
| | | | | | | [yes / no] | [role] |

**Decision rule:** take the highest rung you can reach at A of 3 and put it in the Now column ahead of any parameter work of similar cost. Cap parameter work rather than banning it, because a badly set threshold really does break a product. Every row with L of 7 or more and A below 3 converts into exactly one [decision memo](../../templates/planning/decision-memo.md) naming one person and one ask; filed as a backlog ticket it will sit there for a year, because no backlog grooming session has ever changed a rule.

## Reading the result

- **A row with L of 7 or more at A of 3.** This is the find, and it is usually an information flow. Ship it this quarter and say out loud which parameter item it displaced.
- **Every strong row sits at A of 1 or 2.** The constraint is not the roadmap, it is the mandate. That is a finding to carry upward, not a reason to go quiet; write the memo, and ship the best reachable row while it waits.
- **The sheet contains nothing above rung 10.** The team is listing knobs because it has not drawn its loops. Stop and draw one, then come back.
- **P near 1 for two quarters running with a flat metric.** The altitude is the diagnosis. Further tuning will not rescue it.
- **A high-L intervention shipped and made things worse.** Check direction before you check altitude. Meadows' own warning was that leverage points are counterintuitive and that people who find one frequently push it the wrong way, which is what a strong intervention with a sign error looks like.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. All figures below are ILLUSTRATIVE.

Effort audit: 11 items shipped over two quarters (ILLUSTRATIVE), 9 of them at rungs 12 to 10, so P = 0.82 (ILLUSTRATIVE). Every one of the nine was approved inside the team. The two above rung 9 both needed the finance controller, and one of them was cut for time.

| Candidate | Rung | Why that rung | L | A | Altitude |
|---|---|---|---|---|---|
| Raise the auto-approval confidence threshold | 12 | A constant, set once, changeable in config | 1 | 3 | 3 |
| Draft the report the day the charge posts, not at month end | 9 | Shortens the delay between the act and the consequence | 4 | 3 | 12 |
| Show each manager the correction rate on the reports they approved last month | 6 | Puts the consequence in front of the person who caused it, closing a loop that was open | 7 | 3 | 21 |
| Route out-of-policy lines to the policy owner instead of the filer's manager | 5 | Changes who is permitted to decide, which is a rule, not a routing tweak | 8 | 2 | 16 |
| Sample and re-audit approved reports weekly | 8 | Strengthens the balancing loop against rubber-stamping | 5 | 3 | 15 |
| Restate the system's goal from close-the-books speed to policy-clean spend with a fast reimbursement promise | 3 | Changes what the rules and incentives are for | 10 | 1 | 10 |

Reading: the manager correction-rate view scores 21 against the threshold tune at 3, and both cost about a sprint (ILLUSTRATIVE), so the sprint goes to the correction-rate view. The rule change at altitude 16 becomes one memo to the finance controller, not a ticket. The goal restatement at rung 3 scores 10 only because authority is 1, and that is the pair the product multiplication hides: it is the most powerful move on the sheet and the least reachable, so it belongs in the strategy conversation rather than the quarter. Rung 2 sits underneath all of it as the unexamined belief that filing an expense report is a chore the employee owes the company; the rung 1 exercise, which nobody is funding this year, asks what remains of the product if policy is enforced at card authorization and no report is ever filed.

## The decision it feeds

Which interventions enter the Now column of next quarter's roadmap, and at what altitude the quarter's largest bet sits. Second, and more often the useful one: whether a given item stays a backlog ticket or becomes an escalation with one named person on it, which is the difference between a rule that changes and a rule that gets discussed.

## Where the output lands

The slate's reachable rows land in the [roadmap](../../templates/planning/roadmap.md), Now and Next columns, each carrying its rung so the altitude survives contact with the planning meeting. The unreachable strong rows land in a [decision memo](../../templates/planning/decision-memo.md), section 1 (the decision) and section 3 (options), one memo per row.

## Re-run trigger

Re-run at the start of each planning period, and immediately when the org changes shape: a reorg, a new sponsor, a merged team, or a rule changing owner. Authority scores are facts about the current org chart and expire with it, so a slate more than one planning period old is telling you what used to be out of reach.

## The trap: when this method misleads you

Rung inflation. Every team wants its work to be high altitude, so a copy change gets filed as an information flow and a threshold gets called a rule change, and the sheet certifies exactly the parameter work it was built to expose. The mechanical test is in the "why that rung" column: name the loop, the rule text, or the person who now sees something they could not see before. If nothing changes hands, no rule text is edited, and no loop gains or loses strength, it is a number at rung 12 no matter what it is called.

The second failure is authority theater, scoring A of 1 on everything strong so the slate can be all parameters with a clear conscience. An A of 1 that cannot name the person or the market event is a 2, and the memo gets written.

The third is the multiplication itself, which hides the tail exactly as it does in the [risk matrix](../execution/risk-matrix.md): a rung 2 paradigm shift at A of 1 scores 12 and ties a delay fix at A of 3, so read L and A as a pair and never sort on altitude alone. Underneath all three sits Meadows' own caution, which this sheet cannot enforce: the ranking came out of a specific frustration with people tuning numbers, she treated it as provisional rather than settled, and a team that recites the twelve rungs while never drawing its own loops has swapped one ritual for another.

## Feeds

- [Roadmap](../../templates/planning/roadmap.md): Now and Next take the reachable rows, with the rung recorded
- [Product strategy](../../templates/planning/product-strategy.md), section 4 (sequencing): the effort audit is evidence for or against the current sequence
- [Decision memo](../../templates/planning/decision-memo.md) and the [decision log](../../templates/execution/decision-log.md): one memo per strong unreachable row, its outcome logged
- [Metrics review](../../templates/operate/metrics-review.md), section 4 (predicted versus observed): a high-altitude intervention that moved nothing belongs here before it is repeated
- [OKRs](../../templates/planning/okrs.md): a key result that only a rung 12 change could reach is a target, not an outcome
- [Growth loops](../metrics/growth-loops.md) and [five whys and fishbone](../execution/five-whys-fishbone.md) supply the loops and causes this sheet ranks; [impact mapping](../prioritization/impact-mapping.md) names the actor whose behavior a rung 6 or rung 5 move is meant to change
- OPERATE and the planning turn into DEFINE, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- The [roadmap builder](../../skills/roadmap-builder/SKILL.md) and [strategy critic](../../skills/strategy-critic/SKILL.md) skills read the slate
- Method background: no knowledge card covers systems thinking, so Meadows' paper is the reference; [High Output Management](../../knowledge/high-output-management.md) carries the nearest idea in the [knowledge index](../../knowledge/INDEX.md), managerial leverage
