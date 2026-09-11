# Backlog: Ledgerline Expense Copilot

Fills [templates/execution/backlog.md](../templates/execution/backlog.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, and every backlog item, score, date and identifier are fiction carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Maya Chen · **Refinement cadence:** backlog triage · **Last triaged:** 2026-12-23
**Tracker of record:** this file · **Size cap:** 12 active items

## 1. Intake: what is allowed in

| Intake source | Who raises it | What it must carry before it enters | Where it goes if incomplete |
|---|---|---|---|
| Customer support | Support lead | Ticket volume, severity, sample tickets, affected segment | Back to support with the missing field named |
| Sales | Account executive or sales operations | Account, contract value, close date, what the deal is blocked on | Stays in the CRM. A deal blocker is not a backlog item until it is a product problem |
| Engineering and tech debt | Engineering lead | Systems affected, user-visible impact, rough effort | Stays in the engineering wiki until user impact is stated |
| Leadership request | The executive or a named delegate | The strategic goal it serves, a success metric, a deadline if real | Leadership queue, visibly unranked, rather than silently at the top |
| Product discovery | Product manager or designer | Hypothesis, target user, expected outcome, evidence so far | Ideas bin, not the ranked backlog |

This queue is the Ledgerline add-on backlog after D6. It is separate from the internal RICE backlog. The register and its ranking use the facts in [ledgerline-journey.md](ledgerline-journey.md) and [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md).

## 2. The register

| ID | Item (the problem, not the solution) | Source | Requester | Raised | Rank | Size | State | Linked story or PRD |
|---|---|---|---|---|---|---|---|---|
| BL-01 | The add-on cannot bill per drafted report or show the account's running cost | DEP4, LEDGERLINE-S6 | Maya Chen | 2026-12-21 | WSJF 10.25 | 4 weeks | committed | LEDGERLINE-S6 |
| BL-02 | German-language receipts extract below the required threshold | R3, G-3 | Priya Nair | 2026-11-23 | WSJF 2.0 | 6 weeks | blocked on EVAL-3 | EVAL-3 |
| BL-03 | Legacy annual-invoice accounts emit no activation event | G-1 | Kwame Boateng | 2026-12-19 | WSJF 5.0 | 1 week | refined | G-1 |
| BL-04 | Classic-approvals events carry no draft id | G-2 | Kwame Boateng | 2026-11-13 | WSJF 3.0 | 3 weeks | candidate | G-2 |
| BL-05 | Customer filers learn of a policy breach only at review | Support tickets, N38 | Hana Sato | 2026-11-30 | WSJF 1.4 | 8 weeks | candidate |  |
| BL-06 | Admins cannot see billed seats against filers before activating | LEDGERLINE-S4 | Hana Sato | 2026-12-17 | unranked |  | parked to 2027-02-12 | LEDGERLINE-S4 |
| BL-07 | The 73 held accounts have no path to a successor price | N93, R8 | Isabel Ferreira | 2026-12-22 | WSJF 2.25 | 4 weeks | candidate | R8 |
| BL-08 | Customer filers must photograph one receipt at a time | Customer feedback | Marcus Webb | 2026-11-06 | unranked |  | candidate |  |

**States, fixed vocabulary:** `candidate` (in the queue), `refined` (understood and sized), `committed` (in a release slice), `blocked` (named blocker), `parked` (deliberately deferred with a revisit date), `dead` (see section 5).

## 3. Ranking

**Method in use:** WSJF and cost of delay · **Last re-ranked:** 2026-12-23 · **Changed method?** No. Any future change is recorded in [decision-log.md](../templates/execution/decision-log.md).

WSJF is calculated as:

**(value + time criticality + risk or enablement) / duration in weeks**

| Order | ID | Value | Time criticality | Risk or enablement | Cost of delay arithmetic | Duration | WSJF |
|---|---|---:|---:|---:|---|---:|---:|
| 1 | BL-01 | 13 | 20 | 8 | 13 + 20 + 8 = 41 | 4 | 41 / 4 = 10.25 |
| 2 | BL-03 | 1 | 1 | 3 | 1 + 1 + 3 = 5 | 1 | 5 / 1 = 5.0 |
| 3 | BL-04 | 3 | 1 | 5 | 3 + 1 + 5 = 9 | 3 | 9 / 3 = 3.0 |
| 4 | BL-07 | 5 | 1 | 3 | 5 + 1 + 3 = 9 | 4 | 9 / 4 = 2.25 |
| 5 | BL-02 | 5 | 2 | 5 | 5 + 2 + 5 = 12 | 6 | 12 / 6 = 2.0 |
| 6 | BL-05 | 8 | 2 | 1 | 8 + 2 + 1 = 11 | 8 | 11 / 8 = 1.4 |

BL-06 and BL-08 are left off the short list because BL-06 is parked and BL-08 is not yet on the short list.

The pre-submit check is the BL-05 slice that warns the filer about the single top bounce cause:

**(5 + 2 + 1) / 3 = 8 / 3 = 2.7**

That slice ranks above BL-07. The resulting short-list order is BL-01, BL-03, BL-04, the BL-05 slice, BL-07, BL-02, then the remainder of BL-05.

| Method | Use it when | Sheet |
|---|---|---|
| RICE | Comparable items, and you want the arithmetic visible | [rice-scoring-sheet](../frameworks/prioritization/rice-scoring-sheet.md) |
| MoSCoW | One release scope, negotiating what ships | [moscow](../frameworks/prioritization/moscow.md) |
| WSJF and cost of delay | Sequencing where waiting has a measurable price | [wsjf-cost-of-delay](../frameworks/prioritization/wsjf-cost-of-delay.md) |
| Weighted decision matrix | Several criteria that are not all commensurable | [weighted-decision-matrix](../frameworks/prioritization/weighted-decision-matrix.md) |
| Now, next, later | Communicating outward, where dates would be read as promises | [now-next-later](../frameworks/prioritization/now-next-later.md) |

## 4. Health check

| Failure mode | What it looks like | The rule | This period |
|---|---|---|---|
| Infinite growth | The register passes the size cap and triage quietly stops | Cap at 12 active items. Overflow goes to the ideas bin, not to the bottom of the list | 8 active, within the cap |
| Zombie items | Carried without an owner, never scheduled | An item with no requester for 90 days is archived and the last owner is told | No requesterless active items |
| Duplicates | The same problem filed under multiple titles | Search before entry, and link rather than re-file. Merge on sight and keep the older id | No duplicate active items identified |
| No requester | An anonymous row nobody can explain | Requester and use case are mandatory at intake, per section 1 | 8 of 8 active items have requesters |
| Priority inflation | Everything arrives marked highest | Each source gets at most one top-priority item per cycle. The rest are stack-ranked against each other | WSJF order has one first item |
| Stale context | The item cites a plan, cycle or metric that no longer exists | An item with no update in 180 days is re-validated against the current strategy or killed when its context is no longer current | No stale-context item identified |

**Numbers to record each period:** active items 8 · added 4 · killed 1 · median age 14.5 days · oldest item 47 days

Added against killed:

**4 added - 1 killed = 3 net items**

The oldest item is BL-08 at 47 days. The active item ages are 1, 2, 4, 6, 23, 30, 40 and 47 days, producing a median age of 14.5 days.

## 5. Kill policy

- Untouched for 6 months with no deferral date: archive, and tell the last known owner.
- The requester has left and nobody claimed it within 30 days: kill, and log the removal.
- Duplicated by, or superseded by, something already shipped: close it, link the successor, remove within a week.
- It belongs to another team or product: redirect it to that owner and do not keep a local copy.
- It has been carried through 3 planning cycles without being ranked into one: it is not a candidate, whatever anyone says in the meeting.

| ID | Item | Killed on | Why | Who was told |
|---|---|---|---|---|
| BL-09 | Revise the anchored offer copy | 2026-12-21 | Both EXP-1 arms sat under the kill line, so the iterate path was rejected under D6 | Tomas Lindqvist |
| BL-10 | A ten-report free allowance | 2026-11-03 | Rejected under D2 because the accounts that need the product most would exhaust it | Marcus Webb |

BL-09 and BL-10 are dead, their ids are spent, and neither remains in the active register.

## Exit gate (feeds Gate 4: acceptance criteria met)

- [x] Every active item names a problem, not a solution, and carries a requester and a date raised
- [x] Intake sources each have a stated destination for incomplete requests
- [x] One ranking method is named, and any change of method has a decision-log entry
- [x] The health check has been run this period and the six numbers are recorded
- [x] Added against killed has been computed, not estimated: 4 - 1 = 3
- [x] The register is inside its size cap: 8 active items against a cap of 12
- [x] No item has been carried through planning cycles without being ranked into one
- [x] Killed items are in the dead table with their ids spent and the reason written
- [x] The committed item links to a story id: BL-01 links to LEDGERLINE-S6
- [x] The worked example has been removed

Signed at the backlog exit gate, 2026-12-23: Maya Chen, Product Manager.
