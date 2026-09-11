# Retrospective: Ledgerline Expense Copilot launch cycle

Fills [templates/execution/retrospective.md](../templates/execution/retrospective.md). Everything here is invented: Ledgerline is a fictional company, the Expense Copilot is a fictional product, the people are fictional, and every number and date is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md). See the [examples index](README.md).

**Owner:** Hana Sato, head of customer success · **Date:** 2026-12-23 · **Status:** Actions open; cycle closed with a PIVOT on packaging

**Facilitator:** Hana Sato, not the team lead · **Scribe:** Kwame Boateng · **Cycle:** 2026-11-02 to 2026-12-22 · **Held on:** 2026-12-23 · **Attendees:** 8 of 9 invited, roles across product, engineering, finance, product marketing, data, sales and customer success · **Format:** timeline

## 1. Format choice

| Format | Pick it when |
|---|---|
| Start, stop, continue | The team wants actions fast and the cycle was ordinary |
| 4Ls (liked, learned, lacked, longed for) | Morale is the question, or a new team is forming |
| Sailboat (wind, anchors, rocks, island) | The team has a shared goal and needs to name what drags on it |
| Timeline | The cycle was long or eventful and memories disagree about what happened when |

**Chosen:** Timeline, because the cycle moved from the D3 value-metric decision through phase 1, EXP-1, the DPA decision, and the D6 packaging pivot, so the mechanism clause needed to be examined in sequence rather than as a single outcome.

## 2. Facts first

| Date | What happened | Source |
|---|---|---|
| 2026-11-03 | D3 set the value metric at $6 per plan seat per month, with the north star mismatch accepted in writing | [ledgerline-journey.md](ledgerline-journey.md), D3 |
| 2026-11-05 | 14 account executives were briefed before customer exposure | [ledgerline-journey.md](ledgerline-journey.md), N84 |
| 2026-11-09 to 2026-11-10 | Phase 1 start slipped 1 day because the internal review ran on 2026-11-09; Maya Chen accepted the slip | [ledgerline-journey.md](ledgerline-journey.md), N85 |
| 2026-11-10 to 2026-11-22 | Phase 1 ran for six design partners: 412 eligible reports, 224 drafted, and 173 approved first time | [ledgerline-journey.md](ledgerline-journey.md), N43 to N44 |
| 2026-11-23 | Four of six partners met the phase 1 condition; Oakhurst Dental Partners was not evaluable on 11 reports and Wrenfield Labs recorded 61% approval on 33 drafted reports, mostly German-language receipts | [ledgerline-journey.md](ledgerline-journey.md), N45 |
| 2026-11-23 to 2026-12-04 | EXP-1 exposure ran across the control and anchored per-seat offers, with a 14-day conversion window per account | [ledgerline-journey.md](ledgerline-journey.md), N56 |
| 2026-12-03 | D5 accepted the model vendor's standard subprocessor terms in the customer DPA, with 30-day prompt retention and the existing no-training clause | [ledgerline-journey.md](ledgerline-journey.md), D5 |
| 2026-12-18 | EXP-1 recorded 33 of 1,371 control accounts paid, 40 of 1,377 anchored accounts paid, and 73 of 2,748 accounts paid in total; the difference was inside a standard error of about 0.6 points | [ledgerline-journey.md](ledgerline-journey.md), N61 |
| 2026-12-18 | Maya Chen executed the EXP-1 KILL rule | [ledgerline-journey.md](ledgerline-journey.md), N62 |
| 2026-12-21 | D6 killed the per-seat price, pivoted packaging to a usage metric, held phase 3, withdrew the one-pager pricing section, and switched the offer page to the alternate wording | [ledgerline-journey.md](ledgerline-journey.md), D6 and N94 |

- Planned versus delivered: 6 design partners entered phase 1; 4 of 6 met the exit condition. The arithmetic is 4 / 6, with Oakhurst not evaluable and Wrenfield below the condition.
- Gate outcome this cycle, if any: D6 returned a PIVOT on packaging. EXP-1 was KILL under the pre-declared rule because both arms were under 4.0%.
- Defects found after "done": 1 observed launch quality issue, Wrenfield's German-language receipt result at 61% approval on 33 drafted reports. Interrupts absorbed: 1 day of schedule slip at phase 1 start.

## 3. The board

| Column | Item | Raised by (role) | Votes |
|---|---|---|---|
| Timeline, before launch | The value metric was chosen by what billing could meter | Product | 7 |
| Timeline, before launch | No row compared the add-on with the customer's own plan price | Product marketing | 6 |
| Timeline, offer design | The anchor quoted our own reviewer cost, not the buyer's | Data | 5 |
| Timeline, customer exposure | A live deal found the DPA subprocessor gap, not a checklist | Sales | 4 |
| Timeline, measurement | The funnel tile stayed locked and nobody argued the result | Engineering | 3 |
| Timeline, rollout control | The rollback wording existed before it was needed | Customer success | 3 |

## 4. Themes and root causes

| Theme | Evidence from the board | Root cause (inside our authority) | Keep or change |
|---|---|---|---|
| We selected a billable unit before proving that it represented customer value | The value metric was chosen by what billing could meter, with 7 votes; the customer plan-price comparison was absent, with 6 votes | The pricing review treated billing feasibility as the leading constraint and did not require a benchmark row for the customer's own plan price before signing D3 | Change |
| The mechanism clause was asserted, not tested with the buyer's reference point | The anchor used our own reviewer cost, with 5 votes; EXP-1 converted 33 of 1,371 control accounts and 40 of 1,377 anchored accounts, while the difference sat inside a standard error of about 0.6 points | The experiment brief did not require evidence that the buyer compared the price to the same labour cost or to the customer's own plan price | Change |
| Operational readiness was discovered in the field instead of fully checked before exposure | The DPA subprocessor gap was found through a live deal, with 4 votes; D5 later accepted the standard terms | The launch checklist did not make the customer DPA subprocessor clause an explicit pre-exposure dependency for every customer-facing path | Change |
| The team protected decision quality when the result arrived | The funnel tile stayed locked, with 3 votes; the rollback wording existed before it was needed, with 3 votes; Maya Chen executed the KILL on 2026-12-18 and D6 followed on 2026-12-21 | The brief, dashboard and GTM plan had pre-declared analysis access, decision rules and rollback wording | Keep |

## 5. Actions

| Action | Owner | Due | Verification | Status |
|---|---|---|---|---|
| Stop signing a price unless the pricing document contains a benchmark row for the customer's own plan price and the proposed value metric. Reopen the D3 pricing logic before the usage re-offer. | Isabel Ferreira | 2027-01-08 | The re-signed pricing document contains the benchmark row and records the comparison before EXP-2 exposure opens on 2027-01-11 | Open |
| Build the drafted-report usage meter and the account-level running cost view. Do not reuse the seat-metering work as the value meter. | Priya Nair with the billing lead | 2027-01-08 | DEP4 is delivered, LEDGERLINE-S6 is testable, and an account can see the running count and month's cost before EXP-2 exposure | Open |
| Add a mechanism check to every experiment brief: name the buyer's comparison point, cite the evidence that the buyer uses it, and test that mechanism separately from the conversion result. | Maya Chen with Kwame Boateng | 2027-01-11 | The EXP-2 brief records the buyer comparison point and its evidence before the single-arm exposure begins | Open |

## 6. Previous retro's actions

| Action from last retro | Done (yes / no) | Effect observed | If carried over, what changes |
|---|---|---|---|
| Brief the account executives before any customer sees the add-on | Yes | 14 account executives were briefed on 2026-11-05 before customer exposure | Not carried over |
| Draft the rollback message before each launch phase opens | Yes | The rollback wording was drafted on 2026-11-06 and used when the offer page switched on 2026-12-21 | Not carried over |

## 7. Health of the retro itself

- Did the quieter voices speak, and how does the facilitator know: Yes. The board included six role-raised items, including engineering and customer success observations that were not the highest-vote groups.
- Attendance against the team: 8 of 9 invited.
- Duration: 75 minutes, against the 90-minute box.
- One thing to change about the next retro: Put the buyer's price benchmark on the facts board before discussing any pricing mechanism.

---

## Exit gate (feeds the next cycle's plan and Gate 6: outcomes verified)

Done when every box is honestly ticked. Actions go to the team's tracker; actions that change how the team works also go to [decision-log.md](../templates/execution/decision-log.md); the three-sentence lesson goes to the [Gate 6](../os/STAGE-GATES.md) form when the cycle closes a stage.

- [x] Facts were on the board before opinions
- [x] One format was chosen and the reason is written
- [x] Every theme has a root cause inside the team's authority
- [x] Two to four actions, each with an owner, a date, and a verification
- [x] At least one action stops something
- [x] The previous retro's actions were reviewed with their observed effect
- [x] No item names a person as a cause
- [x] Actions are in the tracker, and the ones that change working agreements are in the decision log
- [x] Signed by the facilitator, Hana Sato, 2026-12-23
