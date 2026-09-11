# Tech Debt Register: Quay

Fills [templates/execution/tech-debt-register.md](../templates/execution/tech-debt-register.md). Everything here is invented: Harbourgate and Quay are fictional, every person is fictional, and every number, date, rate and amount is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Bea Lindqvist · **Engineering lead:** Tomasz Wierzbicki · **Last reviewed:** 2026-10-16 · **Cadence:** every planning cycle · **Unit:** engineer-days per quarter

## 1. How interest is counted

- **Interest sources counted here:** workaround time, change slowdown, incidents, manual operations and onboarding
- **Measured from:** the Quay debt rows and capacity-demand evidence in the [Harbourgate journey](harbourgate-journey.md) and [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), including N62, N65, HC33, HC34 and HC35

## 2. The register

| # | Item (a fact about the system) | Where | Taken on when, why, and where recorded | Interest (engineer-days per quarter) | Principal (engineer-days, low to high) | Ratio (interest / likely principal) | Trend (growing / flat / shrinking) | Owner | Status |
|---|---|---|---|---:|---|---:|---|---|---|
| TD-1 | Quay writes the legacy table shape as well as its own rows | Quay data model and reporting boundary | 2026-04-08, deliberate and prudent, ADR-0002 | 3 | 6 to 18, likely 10 | 3 / 10 = 0.3 | flat | Bea Lindqvist | Accepted by Tomasz Wierzbicki, removal 2027-03-31 after DEP-4 |
| TD-2 | Legacy adapter code and the Marlowe and Tidewater credentials are still deployed after their flags were removed | Quay legacy adapter and provider credentials | 2026-08-03 and 2026-08-31, retained during the provider drain | 2 | 3 to 8, likely 5 | 2 / 5 = 0.4 | flat | Bea Lindqvist | Bundled with the sunset, 2026-12-15 |
| TD-3 | 1.5% of Kestrel declines still classify as “other” and are triaged by hand | Quay decline event stream | 2026-08-14, after the reason-class mapping fix, N62 | 2 | 2 to 6, likely 4 | 2 / 4 = 0.5 | flat | Bea Lindqvist | Bundled with the next decline-stream change |
| TD-4 | The settlement-file-absent alert and reconciliation are still configured for three providers’ drops | Quay settlement ingestion and reconciliation | 2026-07-09, after A3, while the three-provider sunset remains in progress | 1 | 1 to 2, likely 1 | 1 / 1 = 1.0 | flat | Bea Lindqvist | Paid in Q4 inside the sunset decommission steps |
| TD-5 | Legacy-authorised refunds after 2026-11-15 go through provider portals by hand under BR-009 | Finance operations and provider portals | 2026-10-14, D-024, because portal-only refunds remain needed during wind-down | 6 finance-analyst days in Q4 | none: portal-only by contract | not computed | shrinking | Priya Raman | Accepted by Priya Raman, revisit 2027-06-15 |

## 3. Payoff rule and budget

- **Order:** highest ratio first. An item with a ratio above 1 pays for itself inside a quarter and does not wait for a convenient moment.
- **Bundling:** an item whose code an initiative is about to touch is paid inside that initiative, and the initiative's estimate says so.
- **Budget this quarter:** 10 engineer-days, agreed in the capacity plan, HC34, and not borrowed against.
- **Exception:** an item with a ratio above 1 that is not in the payoff plan needs a name in section 5 by the next review.

## 4. Payoff plan

| Register # | Quarter | Engineer-days budgeted | Bundled with (initiative touching the same code, or "standalone") | Done when (the verification) | Status |
|---|---|---:|---|---|---|
| TD-2 | Q4 2026 | 5 | Legacy sunset decommission | The legacy adapter and the Marlowe and Tidewater credentials are removed as part of the legacy path shutdown and contract end on 2026-12-15 | Scheduled |
| TD-4 | Q4 2026 | 1 | Legacy sunset decommission | The three-provider settlement-file and reconciliation configuration is removed without preventing the remaining Quay and Kestrel close | Scheduled |

**Payoff arithmetic:** 5 engineer-days for TD-2 + 1 engineer-day for TD-4 = 6 engineer-days planned for tech debt payoff. The remaining Q4 debt budget is 10 - 6 = 4 engineer-days.

TD-1 is accepted rather than paid in Q4. TD-3 remains bundled with the next decline-stream change. TD-5 is finance-analyst work, not engineering demand, and is accepted by Priya Raman.

## 5. Accepted debt

| Register # | Accepted by (name, role) | Rationale in one sentence | Revisit when | Date |
|---|---|---|---|---|
| TD-1 | Tomasz Wierzbicki, Engineering Lead | Quay keeps the legacy table shape so reporting, finance reconciliation and the order-history page continue to read unchanged rows while DEP-4 migrates reporting away from it. | DEP-4 lands on 2027-02-27; removal remains 2027-03-31 under ADR-0002 | 2026-10-16 |
| TD-5 | Priya Raman, Head of Finance Operations | Finance must retain portal-only refunds for legacy-authorised orders after 2026-11-15 while the provider wind-down access remains available. | 2027-06-15, when portal wind-down access ends under N52 | 2026-10-16 |

## 6. Interest total

- **Open items:** 5 · **Interest total this quarter:** 3 + 2 + 2 + 1 = 8 engineer-days for TD-1 to TD-4, plus 6 finance-analyst days for TD-5 · **Debt budget:** 10 engineer-days · **Copied to capacity plan on:** 2026-10-16

The engineering interest total is 3 + 2 + 2 + 1 = 8 engineer-days per quarter. The 8 engineer-day figure is the standing demand carried by the Q4 capacity plan, HC33. TD-5 stays outside the squad's engineering plan.

## 7. Retired

| Register # | Paid off on | Interest saved per quarter | Estimated principal | Actual principal | What we learned about the estimate |
|---|---|---:|---:|---:|---|
| TD-3, prior reason-class mapping issue | 2026-08-14 | 3 engineer-days | 4 engineer-days | 5 engineer-days | The mapping change cost 5 engineer-days rather than the estimated 4; the residual 1.5% “other” classification remains as TD-3 |

---

## Exit gate (feeds Gate 3: architecture and risks reviewed)

Done when every box is honestly ticked. The register goes to [Gate 3](../os/STAGE-GATES.md) with the architecture set, and its interest total goes to the capacity plan.

- [x] Every item is a verifiable fact about the system, not a preference
- [x] Every item has an interest figure in engineer-days per quarter, measured or labeled ILLUSTRATIVE with a date to measure (TD-5 is carried in finance-analyst days, not engineering capacity)
- [ ] Every principal is a range, not a single number. TD-5 is explicitly portal-only by contract, so no engineering principal is computed.
- [x] Every item with a ratio above 1 is in the payoff plan or accepted by name in section 5
- [x] The interest total appears in the capacity plan's standing demand, as 8 engineer-days for TD-1 to TD-4
- [x] The debt budget is the figure agreed in the capacity plan, 10 engineer-days
- [x] Retired items record actual against estimated principal
- [x] The ILLUSTRATIVE row has been deleted
- [x] Signed by Bea Lindqvist, 2026-10-16
