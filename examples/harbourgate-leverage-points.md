# Harbourgate Leverage Points

Fills [frameworks/systems/leverage-points.md](../frameworks/systems/leverage-points.md).

Everything here is invented: Harbourgate, checkout-pay, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen so that this worksheet reconciles with the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-03-20 · **Product:** Harbourgate checkout-pay · **Source:** [HC55 in the coverage sheet](harbourgate-coverage-sheet.md) · **Anchor:** [Harbourgate journey](harbourgate-journey.md)

## What it is for

Harbourgate's checkout-pay team shipped six changes between 2025-07 and 2025-12. Five were parameter or buffer tuning at rungs 12 to 11. The metric remained a system problem, not only a parameter problem. This worksheet places each change and each candidate intervention on Meadows' twelve rungs, then separates the strongest intervention the team can make alone from the stronger interventions that need one named person's yes.

The practical finding is that the single decline event stream for fraud, finance and support is a rung 6 information flow. The team can reach it at authority 3, so it goes in Now ahead of parameter work. The rule and structural changes that the team cannot reach alone each receive one named person and one ask.

Based on the ideas of Donella Meadows, from her paper "Leverage Points: Places to Intervene in a System" (1999). The L, A and altitude arithmetic is this repository's own local heuristic, not a scoring system proposed by Meadows.

## Run it when

- A metric has stayed flat while checkout-pay has continued to ship changes
- The planning slate is mostly thresholds, retries, copy, capacity or other parameter work
- A behaviour keeps returning after a parameter change, such as unattributed declines or the same cascade
- A sponsor asks why delivered changes have not changed the payment outcome

**Skip it when:** the system is not running yet, or during an active payment incident where the immediate fix is the priority. Harbourgate is already running, so this reconstructed exercise is applicable.

## Inputs you need first

- The six checkout-pay changes shipped between 2025-07 and 2025-12, from [HC55](harbourgate-coverage-sheet.md)
- The observed payment problem and outcome measures, including the entry decline visibility and Gate 6 decline event stream, from [harbourgate-journey.md](harbourgate-journey.md)
- The existing payment loop, including the cascade and the unattributed-declines loop, from [HC54](harbourgate-coverage-sheet.md)
- The people and authority needed to change rules, integrations and provider decisions, from the Harbourgate cast and [HC55](harbourgate-coverage-sheet.md)
- The resulting artefacts for the selected intervention, including S8, AC-4, R2, BR-001 and D-010, from [harbourgate-journey.md](harbourgate-journey.md) and [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md)

## The worksheet

### Step 1: the twelve rungs

| Rung r | Meadows' place, in our words | What it looks like in a product | Our instance | Who can change it |
|---|---|---|---|---|
| 12 | Numbers: the constants somebody set once | Thresholds, limits, prices, timeouts, retry counts, headcount, copy and its timing | Cascade retry delay shortened; wrapper restart moved to nightly; decline message copy rewritten | The checkout-pay team, within its remit |
| 11 | Buffers: the size of a stabilizing stock against the flows through it | Queue depth, credit balance, review capacity, slack in the release train | Extra instances for 2025-11-28; peak-week double on-call | The checkout-pay team, within its remit |
| 10 | Stock and flow structure: the plumbing and where paths cross | The route a record actually takes, the hand-off nodes, the integration topology | Route through one provider and retire two integrations | Rohan Iyer, for the provider and budget decision |
| 9 | Delays: how long a signal takes relative to how fast the system moves | Charge to draft, submit to approval, correction to retrain, ship to measured effect | No separate rung 9 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 8 | Balancing loops: the strength of a correction against the error it must catch | Sampling audits, alerts, rate limits, anything whose job is to pull the system back | No separate rung 8 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 7 | Reinforcing loops: the gain on the loops that compound, good and bad | Invite loops, correction-data loops, and the vicious ones nobody designed | No separate rung 7 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 6 | Information flows: who can see what, and who cannot | Showing a consequence to the person who caused it. The strongest rung a product team routinely owns outright | Marlowe monthly statements imported to a finance spreadsheet; proposed single decline event stream for fraud, finance and support, which became S8 and AC-4 | The team can build the single decline event stream; authority 3 |
| 5 | Rules: incentives, permissions, constraints, penalties | Policy configuration, override rights, contract terms, what the team is measured on | Named owner for every integration; retire the cascade rule, which became BR-001 when Marlowe's cohort reached 100% on 2026-07-20 | Tomasz Wierzbicki for the integration-ownership ask; Saoirse Whelan for the cascade-retirement ask |
| 4 | Self-organization: the power to add or change structure | Admin-authored rules, learning from corrections, APIs and plug-ins. You trade control for adaptation | No separate rung 4 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 3 | Goals: what the system is actually for | The objective the rules and incentives serve when nobody is watching | No separate rung 3 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 2 | Paradigms: the shared assumption the goals grew out of | The unexamined belief about who owes what to whom | No separate rung 2 instance is recorded in HC55 | No instance is evidenced in this sheet |
| 1 | The power to hold a paradigm loosely | Running the exercise in which the artifact your product manages stops existing | No separate rung 1 instance is recorded in HC55 | No instance is evidenced in this sheet |

The rung numbers are an ordering, not a measurement. A difference of two rungs is treated as a tie when the authority and the actual system change do not separate the candidates.

### Step 2: the arithmetic

This worksheet uses:

- **Leverage L = 13 minus r**
- **Authority A = 3** when the team can act inside its own remit
- **Authority A = 2** when one named person's yes is needed
- **Authority A = 1** when several functions, a board, a contract or a market change is involved
- **Altitude = L x A**

| Rung r | L arithmetic | L | Authority case | A | Altitude arithmetic | Altitude |
|---|---:|---:|---|---:|---:|---:|
| 12 | 13 - 12 | 1 | Team can change it | 3 | 1 x 3 | 3 |
| 11 | 13 - 11 | 2 | Team can change it | 3 | 2 x 3 | 6 |
| 10 | 13 - 10 | 3 | One named person's yes | 1 | 3 x 1 | 3 |
| 9 | 13 - 9 | 4 | No instance scored |  |  |  |
| 8 | 13 - 8 | 5 | No instance scored |  |  |  |
| 7 | 13 - 7 | 6 | No instance scored |  |  |  |
| 6 | 13 - 6 | 7 | Team can change it | 3 | 7 x 3 | 21 |
| 5 | 13 - 5 | 8 | One named person's yes | 2 | 8 x 2 | 16 |
| 4 | 13 - 4 | 9 | No instance scored |  |  |  |
| 3 | 13 - 3 | 10 | No instance scored |  |  |  |
| 2 | 13 - 2 | 11 | No instance scored |  |  |  |
| 1 | 13 - 1 | 12 | No instance scored |  |  |  |

The candidate authority and altitude values are those in HC55. They are local sorting values for this quarter, not values assigned by Meadows.

### Step 3: the effort audit

| Shipped item, last two quarters | Rung r | L = 13 minus r | Who approved it |
|---|---:|---:|---|
| Cascade retry delay shortened | 12 | 13 - 12 = 1 | Approval name not recorded in HC55 |
| Wrapper restart moved to nightly | 12 | 13 - 12 = 1 | Approval name not recorded in HC55 |
| Extra instances for 2025-11-28 | 11 | 13 - 11 = 2 | Approval name not recorded in HC55 |
| Decline message copy rewritten | 12 | 13 - 12 = 1 | Approval name not recorded in HC55 |
| Peak-week double on-call | 11 | 13 - 11 = 2 | Approval name not recorded in HC55 |
| Marlowe monthly statements imported to a finance spreadsheet | 6 | 13 - 6 = 7 | Finance is the named destination; approval name not recorded in HC55 |

There were six shipped items. Five were at rungs 12 to 10:

**P = items at rungs 12 to 10 / all items**

**P = 5 / 6 = 0.833...**

The parameter share is therefore **P = 5 of 6**, as recorded in HC55. The five parameter or buffer items were the three rung 12 items and the two rung 11 items. Their approver names are not recorded in HC55. The one item above rung 9 was the rung 6 finance spreadsheet, and its destination was finance.

The audit shows that five of six changes were tuning at the weakest end of the supplied instances. The next slate therefore puts the reachable rung 6 information flow ahead of further parameter work.

### Step 4: the intervention slate

| Candidate intervention | Rung r | Why that rung: the loop, rule, or flow it changes | L | A | Altitude | Reachable this quarter | If not, the one person to ask |
|---|---:|---|---:|---:|---:|---|---|
| Tune the cascade retry | 12 | Changes a retry delay, a constant in the cascade loop | 13 - 12 = 1 | 3 | 1 x 3 = 3 | yes |  |
| Fix the logging only | 6 | Makes decline information available, but does not change the wider ownership or routing rule | 13 - 6 = 7 | 1 | 7 x 1 = 7 | no | No single approver: fraud, finance and support would each need to sign off separately, the several-functions case for an A of 1 |
| One decline stream for fraud, finance and support | 6 | Changes the information flow so each decline carries provider, reason class and trace id; this became S8 and AC-4 | 13 - 6 = 7 | 3 | 7 x 3 = 21 | yes |  |
| A named owner for every integration | 5 | Changes the integration-ownership rule, rather than only changing an integration parameter | 13 - 5 = 8 | 2 | 8 x 2 = 16 | no | Tomasz Wierzbicki, ask him to name an owner for every integration; answered by R2's caretaker on 2026-04-24 |
| Retire the cascade rule | 5 | Changes the payment rule that retries a Kestrel decline through Marlowe; the rule became BR-001 when Marlowe's cohort reached 100% on 2026-07-20 | 13 - 5 = 8 | 2 | 8 x 2 = 16 | no | Saoirse Whelan, ask her to retire the cascade and accept the one-retry rule; answered by BR-001 when Marlowe's cohort reached 100% on 2026-07-20 |
| Route through one provider and retire two | 10 | Changes the stock and flow structure and integration topology, routing every card payment through one provider | 13 - 10 = 3 | 1 | 3 x 1 = 3 | no | Rohan Iyer, ask for the provider and budget decision; answered by D-010 |

The slate has one reachable candidate at the highest reachable rung:

- **Now:** one decline stream for fraud, finance and support, rung 6, authority 3, altitude 21. This became **S8** and **AC-4**.
- **Parameter work:** tune the cascade retry, rung 12, authority 3, altitude 3. It does not displace the rung 6 information-flow work.
- **Escalations:** the three rows the team cannot reach alone each name one person and one ask. The isolated logging row is not promoted over the single shared stream because it needs separate sign-off from fraud, finance and support rather than one named person's yes.

The strong unreachable rows convert to exactly one decision ask each:

1. **Tomasz Wierzbicki:** name an owner for every integration. The ask was answered by R2's caretaker on 2026-04-24.
2. **Saoirse Whelan:** retire the cascade rule and accept the replacement rule. The ask was answered by BR-001 when Marlowe's cohort reached 100% on 2026-07-20.
3. **Rohan Iyer:** approve routing through one provider and retiring two integrations. The ask was answered by D-010.

## Reading the result

- **A row with L of 7 or more at A of 3.** The single decline event stream is the find: L = 7, A = 3, altitude = 21. It is an information flow, and it became S8 and AC-4. It enters Now ahead of the rung 12 cascade retry tune. N20 is the number the information flow was missing: 0% of Marlowe declines carried provider and reason class at entry, against 100% of all declines at Gate 6, once the stream existed.
- **Every strong row sits at A of 1 or 2.** The named-owner rule, cascade retirement and one-provider routing all require an escalation. They are not backlog-only items: each has one person and one ask.
- **The sheet contains nothing above rung 10.** Harbourgate does contain a rung 6 information-flow candidate and a rung 5 rule candidate. The sheet is therefore not limited to knobs.
- **P near 1 for two quarters running with a flat metric.** This audit records P = 5 of 6 for the supplied period. A second period is not supplied, so no two-period conclusion is made.
- **A high-L intervention shipped and made things worse.** Direction still needs review. The cascade rule was the rule to retire because it produced double authorisations in the later journey, and BR-001 replaced it with one retry using a different method rather than automatic resubmission of the same card.
- **Did the escalated rungs actually reduce the load the parameter tuning kept absorbing.** N22 is the check: on-call pages for the payment path fell from 11 in March 2026 to 4 in September 2026, after the decline stream, the cascade retirement and the integration-ownership ask had all landed. A parameter-only program would not be expected to move that number; a rung 5 and rung 6 program is.

## ILLUSTRATIVE example

This is the filled Harbourgate example. All figures, dates and identifiers below are ILLUSTRATIVE.

The effort audit covers six checkout-pay changes from 2025-07 to 2025-12. Five were at rungs 12 to 10, giving:

**P = 5 / 6 = 0.833...**

The five tuning changes were the shortened cascade retry delay, the nightly wrapper restart, extra instances for 2025-11-28, rewritten decline copy and peak-week double on-call. The sixth change, importing Marlowe monthly statements to a finance spreadsheet, was at rung 6.

| Candidate | Rung | Why that rung | L | A | Altitude |
|---|---:|---|---:|---:|---:|
| Tune the cascade retry | 12 | Changes a retry delay | 1 | 3 | 3 |
| Fix the logging only | 6 | Makes decline information visible without changing the wider rule or topology | 7 | 1 | 7 |
| One decline stream for fraud, finance and support | 6 | Gives the relevant functions one provider, reason-class and trace-id stream; became S8 and AC-4 | 7 | 3 | 21 |
| A named owner for every integration | 5 | Changes the integration-ownership rule | 8 | 2 | 16 |
| Retire the cascade rule | 5 | Changes the rule that retried Kestrel declines through Marlowe; became BR-001 | 8 | 2 | 16 |
| Route through one provider and retire two | 10 | Changes the integration topology and payment path | 3 | 1 | 3 |

Reading: the single decline stream scores 21, against 3 for the cascade retry tune, and the team can reach it without approval outside its remit. It therefore goes in Now. The named-owner rule and cascade retirement both score 16, but each requires one named person's yes. Routing through one provider has a higher rung than parameter tuning but an authority of 1, so its altitude is 3 and it becomes an escalation to Rohan Iyer rather than a team-owned Now item.

The three escalation asks were answered in the journey:

- R2's caretaker was named on 2026-04-24 after the ask to Tomasz Wierzbicki.
- BR-001 answered the ask to Saoirse Whelan when Marlowe's cohort reached 100% on 2026-07-20.
- D-010 answered the ask to Rohan Iyer for one-provider routing.

## The decision it feeds

The decision is to put the single decline event stream for fraud, finance and support in Now, ahead of the cascade retry tune and other parameter work of similar cost.

The second decision is to escalate, rather than backlog, the three strong rows that the team cannot reach alone:

- integration ownership to Tomasz Wierzbicki
- cascade retirement to Saoirse Whelan
- one-provider routing to Rohan Iyer

## Where the output lands

The reachable single decline stream landed in the product change represented by **S8** and **AC-4**.

The integration-ownership ask landed in **R2**, closed when Bea Lindqvist became caretaker on 2026-04-24.

The cascade-retirement ask landed in **BR-001**, which replaced the retired **BR-008** when Marlowe's cohort reached 100% on 2026-07-20.

The one-provider routing ask landed in **D-010**, the decision to build on Kestrel as the single card partner for web, app and kiosk.

## Re-run trigger

Re-run at the start of the next planning period, and when the owner of an integration, rule or provider decision changes. Re-run immediately if a new decline loop appears, if a provider is added or retired, or if a parameter change leaves the payment-step outcome flat.

Authority scores describe the current Harbourgate organisation. They should not be carried forward after a reorganisation, a new sponsor or a changed provider contract.

## The trap: when this method misleads you

Rung inflation remains the main trap. A logging change is only a rung 6 information flow if it makes a consequence visible to someone who could act on it. The shared decline stream qualifies because it gives fraud, finance and support provider, reason class and trace id data, and became S8 and AC-4. A copy rewrite remains rung 12.

The second trap is authority theater. The team cannot turn a rung 5 rule change into A of 3 by describing it as configuration. The named-owner rule and cascade retirement each need one person's yes, so they remain A of 2 and name Tomasz Wierzbicki and Saoirse Whelan.

The third trap is sorting on altitude alone. The one-provider routing row has rung 10 and L of 3, but authority 1 gives altitude 3. It is structurally important and commercially consequential, but it is not reachable by the team alone. Read L and A together.

The final caution is Meadows' own: a high-leverage intervention can be pushed in the wrong direction. The cascade was intended to recover declines, but its later double-authorisation behaviour meant the rule needed to be retired and replaced by BR-001, not merely tuned.

## Feeds

- [S8 and AC-4 in the Harbourgate journey](harbourgate-journey.md): the single decline stream and its acceptance criterion
- [R2 and BR-001 in the Harbourgate journey](harbourgate-journey.md): the named-owner and cascade-rule outcomes
- [D-010 in the Harbourgate coverage sheet](harbourgate-coverage-sheet.md): the one-provider decision
- [HC55 in the Harbourgate coverage sheet](harbourgate-coverage-sheet.md): the effort audit, rung assignments, authority scores and altitudes
- [Roadmap](../templates/planning/roadmap.md): the reachable rung 6 intervention enters Now, with its rung recorded
- [Product strategy](../templates/planning/product-strategy.md): the effort audit is evidence for or against the current sequence
- [Decision memo](../templates/planning/decision-memo.md): the strong unreachable rows become named asks rather than backlog tickets
- [Metrics review](../templates/operate/metrics-review.md): the high-altitude intervention is checked against observed payment outcomes
- [OKRs](../templates/planning/okrs.md): a key result that only a rung 12 change could reach is treated as a target, not an outcome
- Method background: Donella Meadows, "Leverage Points: Places to Intervene in a System" (1999), explained in this repository's own words
- OPERATE and the planning turn into DEFINE, reviewed at [Gate 6: outcomes verified](../os/STAGE-GATES.md)
