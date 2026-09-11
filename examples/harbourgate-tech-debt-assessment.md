# Tech Debt Assessment: Harbourgate checkout-pay

Fills [frameworks/assessment/tech-debt-assessment.md](../frameworks/assessment/tech-debt-assessment.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every figure is ILLUSTRATIVE, taken from the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-04-08 · **Status:** Feeds ADR-0003 and Gate 3

## What it is for

This assessment prices the known compromises in checkout-pay before the architecture decision and Gate 3. Tomasz Wierzbicki and Bea Lindqvist assessed five candidate rows on 2026-04-08.

The assessment separates two ideas:

- Cunningham's debt metaphor decides whether a compromise is debt at all. The row must be verifiable, must create measurable recurring cost, and must have a known better shape.
- Fowler's quadrant describes what else must change when the principal is paid. It distinguishes deliberate from inadvertent choices and prudent from reckless choices.

The assessment finds five debt rows with total interest of 33 engineer-days per quarter. Three rows are bundled into Quay:

1. Marlowe's missing decline logs
2. The BR-008 cascade rule
3. The Marlowe path carrying the card number through Harbourgate servers

The undocumented and unowned wrapper is retired by ADR-0003 because of its risk, even though its ratio is only 0.2. The direct table-shape coupling is accepted by Tomasz Wierzbicki, recorded in ADR-0002, and carried by DEP-4.

The wrapper's plain-text logs fail the Cunningham test because no measurable recurring time cost was established. They are excluded from this sheet and routed to R8 from F1.

## Run it when

This assessment ran before Gate 3 on 2026-04-08 because engineering needed a priced view of the compromises entering the architecture decision.

It should be re-run:

- At the start of the next planning cycle
- When a postmortem, slipped estimate, or security finding names an area already assessed
- When Quay's table-shape coupling is reviewed against DEP-4
- When ADR-0003 or ADR-0002 reaches its removal or review condition

It is not used to turn every disliked implementation detail into debt. A row remains only when the Cunningham test is passed and the recurring interest can be evidenced.

## Inputs you need first

- The checkout-pay repository and wrapper history
- The ADR set, especially ADR-0002 and ADR-0003
- Finding F1 and risk R8
- The HC49 assessment data in the [coverage sheet](harbourgate-coverage-sheet.md)
- The current capacity-plan debt budget, which is 10 engineer-days in HC34
- The initiative option to build Quay as a separate payment service

## The worksheet

### Step 1: the Cunningham test, which decides what is on the sheet at all

All three questions were run against each candidate. The five rows below passed all three questions. F1 did not pass the measurable-interest question and is therefore not a debt row.

| Candidate | Is it a fact a new engineer could verify in an afternoon | Does it cost measurable time every quarter it stands | Does the team now know what the right shape is | Result and destination |
|---|---|---|---|---|
| The wrapper is undocumented and unowned since 2021 | Yes. The wrapper was written by a contractor who left in 2021, and no engineer could change it safely until 2026-04-24 | Yes. HC49 records 6 engineer-days per quarter of interest | Yes. ADR-0003 defines the replacement shape, a Quay service routing every card payment through Kestrel | Debt row 1 |
| Marlowe logs no declines | Yes. Marlowe logs no declines, while the other providers use different systems | Yes. HC49 records 8 engineer-days per quarter of interest | Yes. Quay's shared decline stream provides provider and reason data | Debt row 2 |
| BR-008 retries Kestrel declines through Marlowe without a shared idempotency key | Yes. BR-008 is the 2019 cascade rule | Yes. HC49 records 3 engineer-days per quarter of interest | Yes. BR-001 replaces it with one retry using a different method, and BR-008 is retired | Debt row 3 |
| The Marlowe path carries the card number through Harbourgate servers, with 7 systems in PCI DSS assessment scope | Yes. N55 records 7 systems at entry, and I-5 records the card number in transit | Yes. HC49 records 12 engineer-days per quarter of interest | Yes. Quay uses Kestrel hosted fields so no card number reaches a Harbourgate server | Debt row 4 |
| Reporting, reconciliation and the order-history page read the payment tables directly | Yes. I-10 reads the legacy table shape, and ADR-0002 records the constraint | Yes. HC49 records 4 engineer-days per quarter of interest | Yes. Quay continues writing the legacy shape while DEP-4 moves reporting away from it | Debt row 5 |
| F1, wrapper logs hold the masked PAN and cardholder name in plain text | Yes. The finding is verifiable | No measurable recurring time cost was established | The remediation is known, but the Cunningham test stops at the missing interest basis | Not a debt row. Routed to R8 in the risk register |

### Step 2: the Fowler quadrant, which decides what else has to change

| Row | Quadrant | What happened | What paying the principal buys | Second action required |
|---|---|---|---|---|
| The wrapper is undocumented and unowned since 2021 | IR, inadvertent and reckless | The wrapper's ownership and shape were lost after the contractor left, and nobody had a safe change path | Retiring the wrapper removes the unowned integration surface | Name a caretaker during the transition, then retire the wrapper through ADR-0003. Bea Lindqvist became caretaker on 2026-04-24, closing R2 |
| Marlowe logs no declines | DR, deliberate and reckless | The integration was accepted without a complete decline event stream | Quay's decline stream supplies the missing provider and reason information | Change the integration design so every decline is emitted with provider and reason class |
| BR-008 retries Kestrel declines through Marlowe without a shared idempotency key | DR, deliberate and reckless | The cascade was chosen to recover declines, without protecting the authorisation path from duplicate attempts | Retiring BR-008 removes the cascade and its double-authorisation exposure | Change the retry rule to BR-001 and do not resubmit the same card automatically |
| The Marlowe path carries the card number through Harbourgate servers | DP, deliberate and prudent | The path was knowingly introduced as part of the Marlowe integration | Quay and Kestrel hosted fields reduce the Harbourgate card-data path and the PCI DSS scope from 7 systems at entry toward 3 after sunset | Keep the hosted-fields boundary and record the scope change with the PCI DSS owner |
| Reporting, reconciliation and the order-history page read the payment tables directly | DP, deliberate and prudent | The legacy table shape was retained knowingly so existing consumers would continue to work | Paying the principal eventually removes the coupling and the old table shape | Keep the compatibility shape under ADR-0002, and move reporting off it through DEP-4 |

### Step 3: the arithmetic

Interest is recorded in engineer-days per quarter. The five rows sum as follows:

```text
6 + 8 + 3 + 12 + 4 = 33 engineer-days per quarter
```

Likely principal is the middle value in each HC49 range. The ratio is:

```text
interest / likely principal
```

Payback is:

```text
likely principal / interest
```

The ratios and payback estimates are:

| Row | Interest | Principal, low to likely to high | Ratio arithmetic | Ratio, to one decimal | Payback arithmetic | Payback |
|---|---:|---|---|---:|---|---:|
| Wrapper | 6 | 15 to 25 to 40 | 6 / 25 = 0.24 | 0.2 | 25 / 6 = 4.166... | 4.2 quarters |
| Marlowe missing declines | 8 | 10 to 15 to 25 | 8 / 15 = 0.533... | 0.5 | 15 / 8 = 1.875 | 1.9 quarters |
| BR-008 cascade | 3 | 5 to 8 to 12 | 3 / 8 = 0.375 | 0.4 | 8 / 3 = 2.666... | 2.7 quarters |
| Card number crossing Harbourgate servers | 12 | 20 to 30 to 50 | 12 / 30 = 0.4 | 0.4 | 30 / 12 = 2.5 | 2.5 quarters |
| Table-shape coupling | 4 | 30 to 45 to 70 | 4 / 45 = 0.088... | 0.1 | 45 / 4 = 11.25 | 11.3 quarters |

The ratio does not decide the wrapper row. Its 0.2 ratio understates the security and ownership risk represented by R2. ADR-0003 retires it because the replacement architecture removes the unowned wrapper, not because the ratio reaches the scheduling threshold.

The assessment has 5 open rows and 33 engineer-days per quarter of interest. Against the 10 engineer-day debt budget in HC34:

```text
33 - 10 = 23 engineer-days per quarter above the budget
```

This difference is standing demand that the capacity plan must account for. It is not a reason to pretend that the wrapper, the missing decline stream, the cascade, or the card-data path have no cost.

### Step 4: the sheet

| # | Item, as a verifiable fact | Where | Quadrant | Recorded in | Interest (team-days per quarter) | Teams paying | Basis for interest | Principal, low to likely to high | Basis for principal | Ratio | Trend | Second action, from step 2 | Owner | Decision, signed |
|---:|---|---|---|---|---:|---|---|---|---|---:|---|---|---|---|
| 1 | The wrapper is undocumented and unowned since 2021 | Tidewater integration, I-7 | IR | ADR-0003 | 6 | Payments squad | HC49, estimate | 15 to 25 to 40 engineer-days | HC49, estimate | 0.2 | growing | Name a caretaker during transition, then retire the wrapper | Bea Lindqvist during transition, Tomasz Wierzbicki for the architecture decision | Retire through ADR-0003, signed by Tomasz Wierzbicki |
| 2 | Marlowe logs no declines | Marlowe integration, I-5 | DR | ADR-0003 | 8 | Payments squad, finance and support users of the decline information | HC49, estimate | 10 to 15 to 25 engineer-days | HC49, estimate | 0.5 | growing | Create one decline stream with provider and reason class | Bea Lindqvist | Bundle into Quay, signed by Tomasz Wierzbicki |
| 3 | BR-008 retries Kestrel declines through Marlowe without a shared idempotency key | BR-008 | DR | ADR-0003 | 3 | Payments squad and fraud operations | HC49, estimate | 5 to 8 to 12 engineer-days | HC49, estimate | 0.4 | growing | Replace the cascade with BR-001 and prohibit automatic resubmission of the same card | Tomasz Wierzbicki | Bundle into Quay, signed by Tomasz Wierzbicki |
| 4 | The Marlowe path carries the card number through Harbourgate servers, with 7 systems in PCI DSS assessment scope | I-5, N55 | DP | ADR-0003 | 12 | Payments squad and Information Security | HC49, estimate | 20 to 30 to 50 engineer-days | HC49, estimate | 0.4 | flat | Keep the hosted-fields boundary and re-assess PCI DSS scope | Hamid Qureshi | Bundle into Quay, signed by Tomasz Wierzbicki |
| 5 | Reporting, reconciliation and the order-history page read the payment tables directly | I-10, ADR-0002 | DP | ADR-0002 | 4 | Payments squad, finance, data engineering and order-history consumers | HC49, estimate | 30 to 45 to 70 engineer-days | HC49, estimate | 0.1 | flat | Keep the compatibility shape, then move reporting through DEP-4 | Tomasz Wierzbicki | Accept by name, signed by Tomasz Wierzbicki. Revisit when DEP-4 lands, removal date 2027-03-31 |

**Totals to carry**

| Measure | Arithmetic | Result |
|---|---|---:|
| Open rows | Count of rows 1 to 5 | 5 |
| Interest total | 6 + 8 + 3 + 12 + 4 | 33 engineer-days per quarter |
| Debt budget this cycle | HC34 | 10 engineer-days |
| Difference | 33 - 10 | 23 engineer-days per quarter above budget |

The wrapper's plain-text logs are not in the open-row total:

```text
F1: measurable interest not established, therefore 0 debt rows added
F1 destination: R8
```

## ILLUSTRATIVE example

This is an ILLUSTRATIVE Harbourgate example, using the five HC49 rows rather than invented comparison rows.

| # | Item (ILLUSTRATIVE) | Quadrant | Interest | Likely principal | Ratio | Trend | Decision |
|---:|---|---|---:|---:|---:|---|---|
| 1 | The wrapper is undocumented and unowned since 2021 | IR | 6 | 25 | 0.2 | growing | Retire through ADR-0003 |
| 2 | Marlowe logs no declines | DR | 8 | 15 | 0.5 | growing | Bundle into Quay |
| 3 | BR-008 retries Kestrel declines through Marlowe without a shared idempotency key | DR | 3 | 8 | 0.4 | growing | Bundle into Quay |
| 4 | The Marlowe path carries the card number through Harbourgate servers | DP | 12 | 30 | 0.4 | flat | Bundle into Quay |
| 5 | Reporting, reconciliation and the order-history page read the payment tables directly | DP | 4 | 45 | 0.1 | flat | Accept by name, ADR-0002 and DEP-4 |

The total is:

```text
6 + 8 + 3 + 12 + 4 = 33 engineer-days per quarter
```

The three rows bundled into Quay are rows 2, 3 and 4. The wrapper is also retired by ADR-0003, but it is not counted as one of those three bundled rows because its decision is driven by the ownership and security risk shown by R2.

The table-shape row is accepted because its likely principal is 45 engineer-days and its ratio is only 0.1:

```text
4 / 45 = 0.088... = 0.1
```

Acceptance is not deletion. Tomasz Wierzbicki signs the acceptance, ADR-0002 keeps the old shape until 2027-03-31, and DEP-4 tracks the move of reporting away from it.

## How to read the result

The highest ratio among the five rows is the missing decline stream:

```text
8 / 15 = 0.5
```

The cascade and card-data rows both have a 0.4 ratio. The wrapper's ratio is 0.2, but ADR-0003 retires it because an unowned payment wrapper is a risk item, not merely a slow piece of code.

The 33 engineer-days per quarter of interest is greater than the 10 engineer-day debt budget by 23 engineer-days per quarter. The capacity plan therefore carries more standing demand than the ring-fenced budget covers.

The quadrant mix is also a finding:

- Two rows are DR, the missing decline logs and BR-008. Their second actions change the integration and commitment choices that created the shortcuts.
- Two rows are DP, the card-data path and the table-shape coupling. They were deliberate compatibility or boundary decisions.
- One row is IR, the wrapper. Its main lesson is ownership, not only refactoring.

F1 is kept separate from the debt score. The wrapper logs holding the masked PAN and cardholder name in plain text are a security finding that became R8. No measurable recurring time cost was established, so adding it to the debt total would make the total look more complete while weakening the Cunningham test.

## The decision it feeds

ADR-0003 should route every card payment through Kestrel from Quay and retire the Marlowe and Tidewater integrations.

The assessment supports that decision in four ways:

1. It prices the recurring cost of the current payment path at 33 engineer-days per quarter.
2. It identifies the three rows that Quay can bundle into the replacement work: missing decline logs, BR-008, and the card-data path.
3. It shows why the wrapper is retired despite its 0.2 ratio: R2 is an ownership and operational-risk item.
4. It names the table-shape coupling as an accepted compromise rather than hiding it in a clean architecture diagram.

The table-shape decision becomes ADR-0002 and DEP-4. The accepted row has a named owner, a revisit condition, and a removal date of 2027-03-31.

## Where the output lands

- ADR-0003, which records the Kestrel route, the retirement of Marlowe and Tidewater, and the wrapper risk
- ADR-0002, which records the accepted legacy table shape and its removal date
- DEP-4, which tracks reporting's move away from the legacy table shape
- R8, which receives F1 because the plain-text wrapper logs failed the measurable-interest part of the Cunningham test
- The capacity plan, which carries 33 engineer-days per quarter of interest against the 10 engineer-day budget
- Gate 3, where the architecture set is reviewed with each compromise numbered and owned

The source values are recorded in the [Harbourgate journey](harbourgate-journey.md) and [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), especially HC49, N55, F1 and R8.

## Re-run trigger

Re-run at the start of the next planning cycle.

Re-run earlier if:

- A security finding names the wrapper, its logs, or the card-data path
- A postmortem or slipped estimate names Marlowe, BR-008, the table shape, or the Quay compatibility path
- DEP-4 changes status
- ADR-0002 reaches its review condition
- The replacement architecture changes the Kestrel boundary or the shared decline stream

When a row cannot produce a measurable interest basis at the next review, do not silently retain its number. Reclassify it as a risk, an architecture question, or a preference.

## When this method misleads you

The wrapper illustrates the first failure mode. Its ratio is 0.2, but that ratio understates the importance of an unowned integration. The decision to retire it comes from R2 and ADR-0003, not from the ratio alone.

The second failure mode is shared cost. Marlowe's missing declines affect the payments squad, finance and support users, so the teams-paying column must not be reduced to the code-owning team.

The third failure mode is treating all findings as debt. F1 is real and important, but it has no measured recurring time cost in HC49. It goes to R8 instead of inflating the debt total.

The fourth failure mode is confusing deliberate compatibility with accidental neglect. The table shape is a deliberate decision recorded in ADR-0002. It is accepted by name and assigned to DEP-4, rather than described as an undocumented mess.

The fifth failure mode is using the ratio as a substitute for architecture judgment. The three Quay bundles are not selected only because their ratios are higher than the table-shape row. They are selected because the replacement architecture opens the same code and removes three related compromises together.

## Feeds

- ADR-0003, the decision to route every card payment through Kestrel from Quay
- ADR-0002, the accepted legacy table shape and its removal date
- DEP-4, reporting's migration away from the legacy table shape
- R8, the register entry created from F1
- The capacity plan, with 33 engineer-days per quarter of interest against a 10 engineer-day debt budget
- Gate 3, where the architecture and its known compromises are reviewed
- [Harbourgate journey](harbourgate-journey.md), the canonical product data sheet
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), especially HC49, N55, F1 and R8
- [Tech debt assessment worksheet](../frameworks/assessment/tech-debt-assessment.md), the blank filled by this example

### Pre-Gate-3 readiness walk (this assessment's own check, not the Gate 3 record)

| Readiness question | Evidence | Result |
|---|---|---|
| Does every known compromise have a verifiable fact | Five debt rows have facts, locations and sources in HC49; F1 is separately recorded | Pass |
| Does every debt row have an interest basis and principal range | Rows 1 to 5 show HC49 interest and low, likely and high principal values | Pass |
| Are the recurring costs reconciled | 6 + 8 + 3 + 12 + 4 = 33 engineer-days per quarter | Pass |
| Is the debt budget comparison visible | 33 - 10 = 23 engineer-days per quarter above the budget | Pass |
| Does every row have an owner and a decision | Rows are assigned to Tomasz Wierzbicki, Bea Lindqvist or Hamid Qureshi, with bundle, retire or accept decisions | Pass |
| Are excluded findings routed somewhere | F1 fails the measurable-interest test and is routed to R8 | Pass |
| Is the accepted table-shape coupling recorded | ADR-0002 and DEP-4 carry the acceptance, review condition and removal date | Pass |

**Readiness check:** this assessment is READY TO FEED GATE 3. It is an internal input, not the gate's own outcome: the journey's Gate attempts table records Gate 3 itself as held on 2026-04-10, REVIEWED AND ACCEPTED WITH THE WRAPPER-OWNER MISS (Tomasz Wierzbicki to name an owner by 2026-04-24).

**Signed:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-04-08
