# Business Requirements Document: Northstar Inventory Forecasting

Fills [templates/definition/brd.md](../templates/definition/brd.md). Everything here is invented: Northstar Foods is a fictional mid-size packaged-food company, Inventory Forecasting is a fictional initiative, the people are fictional, and every number and date is ILLUSTRATIVE.

**Owner:** Mara Chen · **Sponsor:** Daniel Ortiz, chief financial officer
**Date:** 2027-01-18 · **Status:** Signed off · **Version:** 1

## 1. Business objectives

| # | Objective | Company objective or OKR it serves | Metric | Baseline | Target | By when |
|---|---|---|---|---|---|---|
| BO1 | Reduce the time planners spend preparing the monthly demand and replenishment plan | Company objective: make operations more predictable while protecting gross margin; Operations OKR O1 | Planner hours spent per monthly planning cycle | 320 hours per cycle, measured by Operations in Q4 2026 | 160 hours per cycle | 2027-06-30 |
| BO2 | Reduce avoidable expedited freight caused by late or inaccurate replenishment decisions | Company objective: make operations more predictable while protecting gross margin; Operations OKR O2 | Monthly expedited freight spend | $48,000 per month, measured by Finance in Q4 2026 | $36,000 per month | 2027-06-30 |

## 2. Background and problem

Northstar Foods plans production and replenishment across its packaged-snack portfolio using spreadsheets assembled from separate sales, inventory and supplier reports. Planners spend 320 hours per monthly cycle reconciling those inputs, and the resulting plan still leaves the business exposed to late changes and avoidable expedited freight. The framed problem is documented in a problem framing (not included in this standalone excerpt; see the [problem framing template](../templates/discovery/problem-framing.md)), including the cost of inaction: if Northstar does nothing, the company continues spending about $48,000 per month on expedited freight while planning capacity remains tied up in reconciliation. This initiative funds a business capability, not a commitment to a particular forecasting model or user interface.

## 3. Scope

### In scope

| # | Capability or change, in business terms | Serves objective |
|---|---|---|
| S1 | Consolidate approved sales, inventory and supplier lead-time inputs into one planning view | BO1 |
| S2 | Produce a weekly demand and replenishment forecast for the initial packaged-snack portfolio | BO1, BO2 |
| S3 | Flag projected stockouts, excess inventory and supplier lead-time exceptions for planner review | BO2 |
| S4 | Give planners an exportable recommendation and an audit trail showing the inputs and overrides used in each planning cycle | BO1 |
| S5 | Train the supply planning team and establish an operating owner for forecast review and exception handling | BO1, BO2 |

### Out of scope

| # | Explicitly excluded | Why | Revisit when |
|---|---|---|---|
| X1 | Automatic purchase-order submission to suppliers | The first release must support planner review and preserve purchasing controls | Revisit after two completed monthly planning cycles meet the success measures |
| X2 | Forecasting for international markets | The initial business case covers Northstar's domestic packaged-snack operation only | Revisit when the sponsor approves a separate international business case |
| X3 | Replacement of the enterprise resource planning system | ERP replacement is a separate technology program with different funding and governance | Revisit through the annual technology portfolio review |
| X4 | Consumer demand forecasting for new products with no sales history | There is not yet an agreed method for validating those forecasts | Revisit after Finance and Operations approve a validation method |

## 4. Stakeholders

| Name | Function | Stake in this initiative | Decision rights (approves / consulted / informed) |
|---|---|---|---|
| Daniel Ortiz | Chief financial officer | Controls the funding requested by this document and expects the return calculation to be auditable | Approves final funding and Gate 2 sign-off |
| Mara Chen | Product and operations systems lead | Owns the business requirements and delivery coordination | Consulted on scope and requirements; informed on funding |
| Priya Nair | Vice president, supply chain | Owns the planning process and the operational outcome | Consulted on objectives, scope and acceptance |
| Leon Brooks | Director, demand planning | Owns planner adoption and the operating process after launch | Consulted on workflow and success measurement |
| Sofia Alvarez | Finance business partner | Reviews the financial method and validates actual savings | Approves the calculation method; consulted on results |
| Ethan Cole | Chief information security officer | Reviews data access, retention and platform controls | Consulted on constraints and launch readiness |
| Jules Martin | Procurement director | Owns supplier and purchasing process boundaries | Informed on scope; consulted on future purchase-order integration |

## 5. Constraints

| Constraint | Type (budget / deadline / regulatory / platform / people) | Hard or soft | Source |
|---|---|---|---|
| Total build funding must remain within the approved estimate range of $200,000 to $280,000 | Budget | Hard | Daniel Ortiz, CFO funding review, 2027-01-18 |
| The first operating review must occur by 2027-06-30 so the initiative can be evaluated against the Operations OKRs | Deadline | Hard | Operations OKRs O1 and O2 |
| The initiative must use Northstar's existing identity, data warehouse and approved cloud account | Platform | Hard | Ethan Cole, information security review, 2027-01-12 |
| Planners must remain accountable for accepting or rejecting recommendations | People | Hard | Priya Nair and Leon Brooks, requirements review, 2027-01-15 |
| No production data may be copied into an unapproved external forecasting service | Regulatory | Hard | Ethan Cole, data handling standard, 2027-01-12 |
| The initial release should not require more than one planner training session per operating region | People | Soft | Leon Brooks, planning team workshop, 2027-01-15 |

## 6. Financial case

- **Cost to build:** $200,000 to $280,000, with a planning estimate of $240,000, produced by Mara Chen with Engineering and Finance input.
- **Cost to run:** $4,000 per month once live, or $48,000 per year.
- **Expected return:** The calculation uses avoided planner effort plus avoided expedited freight. Planner effort savings are 160 hours per monthly cycle multiplied by $45 per hour multiplied by 12 months, which equals $86,400 per year. Expected expedited freight reduction is $12,000 per month multiplied by 12 months, which equals $144,000 per year. Gross annual benefit is therefore $86,400 plus $144,000, or $230,400. After annual run cost of $48,000, expected net annual benefit is $182,400.
- **Payback horizon:** At the planning estimate, $240,000 divided by $182,400 equals 1.316 years. 1.316 years multiplied by 12 months equals 15.8 months, so the expected payback is about 16 months after the start of live operation.
- **Sensitivity:** The case breaks if the initiative saves materially fewer than 160 planner hours per monthly cycle. At 80 hours saved per cycle, the planner benefit is 80 multiplied by $45 multiplied by 12, or $43,200 per year. Combined with the expected $144,000 freight reduction, gross annual benefit would be $187,200. After $48,000 annual run cost, net annual benefit would be $139,200, extending payback on the $240,000 planning estimate to $240,000 divided by $139,200 multiplied by 12, or about 20.7 months. The 160-hour savings assumption is carried into the assumptions-register excerpt below, A1.

**Assumptions register excerpt** (fills [assumptions-register.md](../templates/definition/assumptions-register.md)):

| ID | Assumption | Category | Confidence | Impact if wrong | Validation method | Validate by | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| A1 | The initiative saves planners 160 hours per monthly cycle | Behavior | Medium | High, this is the sensitivity in Section 6 above | Compare planner hours logged per cycle before and after rollout against the Operations Q4 2026 time measure baseline | 2027-07-31 | Leon Brooks | OPEN |

**Finance partner who agreed the calculation method:** Sofia Alvarez, finance business partner, 2027-01-18

## 7. Success measurement

- **Who measures:** Sofia Alvarez, with Leon Brooks supplying operating data · **Where:** Northstar Operations and Finance monthly performance report
- **Review cadence after launch:** Finance and Supply Chain review BO1 and BO2 monthly for the first three months after launch, then quarterly. The first formal review is due by 2027-06-30.
- **Sunset trigger:** If the initiative does not reduce planner effort to 160 hours per monthly cycle and expedited freight to $36,000 per month by 2027-06-30, and the sponsor does not approve a written recovery plan, Northstar will stop further investment and return the process to the existing planning method.

## 8. Sponsor sign-off

- **I confirm the objectives, scope, constraints, and financial case above, and I fund the DEFINE and DESIGN stages.**
- **Sponsor:** Daniel Ortiz · **Signature or approval record:** Northstar funding decision record, approved in the CFO portfolio review · **Date:** 2027-01-18

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every objective traces to a stated company objective or OKR
- [x] Every objective has metric, baseline, and target, or a named owner and date for the missing number
- [x] Out of scope is populated, with reasons
- [x] Exactly one stakeholder holds final approval
- [x] Financial case method agreed with a named finance partner, or labeled ILLUSTRATIVE with an owner and date
- [x] The sensitivity assumption appears in [assumptions-register.md](../templates/definition/assumptions-register.md), as the A1 excerpt in Section 6, above
- [x] Sponsor sign-off recorded with a date

Signed at Gate 2: Daniel Ortiz, chief financial officer, 2027-01-18
