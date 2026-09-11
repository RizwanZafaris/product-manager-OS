# Capacity Plan: Harbourgate payments squad, Q4 2026

Fills [templates/planning/capacity-plan.md](../templates/planning/capacity-plan.md). Everything here is invented: Harbourgate is fictional, every person is fictional, and every number, date, rate and identifier is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Tomasz Wierzbicki, Engineering Lead · **Period:** Q4 2026 · **Date:** 2026-10-16 · **Status:** Approved
**Unit:** Engineer-days · **Linked roadmap:** Harbourgate Q4 2026 roadmap

## 1. The rules

- **The 80 percent rule.** Committed work is planned to no more than 80 percent of net available capacity. The other 20 percent absorbs interrupts, estimate error, and the standing demand nobody scheduled. When committed demand exceeds the line, an initiative moves to Next; the line does not move.
- **Ranges, not numbers.** Every initiative carries a low, likely, and high figure from the estimation sheet. The planning figure is the likely value, or the high value when confidence is low.
- **One unit.** This file uses engineer-days throughout.

## 2. Supply per team

The payments squad has 5 engineers across 13 weeks. Gross supply is 5 x 13 weeks x 5 engineer-days per week = 325 engineer-days. The deductions are 30 engineer-days of leave, 40 engineer-days of on-call and support, and 20 engineer-days of recurring load. The on-call and support deduction includes N54's 0.4 FTE legacy share through 2026-12-15. Net supply is 325 - 30 - 40 - 20 = 235 engineer-days. Plannable supply is 80 percent of 235 = 188 engineer-days. Source: HC32 and N54.

| Team | People | Weeks | Gross | Leave | On-call and support | Recurring load (hiring, onboarding, meetings) | Net | Plannable (80 percent of net) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Payments squad | 5 engineers | 13 | 325 | 30 | 40, including N54's 0.4 FTE legacy share to 2026-12-15 | 20 | 235 | 188 |

## 3. Demand per initiative

The low, likely and high figures are from HC33. The planning figure is the likely value, except for the Kestrel region failover rehearsal, which uses the high figure because confidence is low. The six initiative figures total 30 + 15 + 15 + 6 + 25 + 30 = 121 engineer-days.

| Initiative (roadmap ref) | Team | Low | Likely | High | Confidence | Planning figure | Missing work checked? | Order |
|---|---|---:|---:|---:|---|---:|---|---:|
| Legacy sunset decommission | Payments squad | 20 | 30 | 45 | Not stated | 30 | Yes, decommission steps and operational support included | 1 |
| Peak readiness and freeze support, N64 | Payments squad | 10 | 15 | 20 | Not stated | 15 | Yes, support for the 2026-11-13 to 2026-12-04 freeze included | 2 |
| DEP-4 support | Payments squad | 10 | 15 | 25 | Not stated | 15 | Yes, reporting migration support included | 3 |
| Tech debt payoff, TD-2 and TD-4, inside the HC34 budget | Payments squad | 6 | 6 | 10 | Not stated | 6 | Yes, the selected debt rows and decommission steps checked | 4 |
| Kestrel region failover rehearsal, N29 | Payments squad | 10 | 15 | 25 | Low | 25 | Yes, rehearsal and recovery work checked | 5 |
| Table-shape removal preparation, ADR-0002 | Payments squad | 20 | 30 | 45 | Not stated | 30 | Yes, preparation for DEP-4 and the 2027-03-31 removal date checked | 6 |

## 4. Standing demand

Standing demand totals 8 + 25 + 10 = 43 engineer-days. The 8 engineer-days of tech debt interest cover TD-1 to TD-4. TD-5 is finance's demand and is not included in the squad plan. Sources: HC33 and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

| Item | Team | Units per period | Source |
|---|---|---:|---|
| Tech debt interest, TD-1 to TD-4 | Payments squad | 8 engineer-days | HC33 and the tech debt register rows in the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md) |
| Support and defect fixing | Payments squad | 25 engineer-days | Q3 actual, HC33 |
| Platform, security, and compliance mandates, including DEP-7 evidence | Payments squad | 10 engineer-days | DEP-7 and HC33 |

## 5. The balance

Committed demand is standing demand plus the six initiatives:

- Standing demand: 43 engineer-days
- Initiatives: 30 + 15 + 15 + 6 + 25 + 30 = 121 engineer-days
- Committed demand: 43 + 121 = 164 engineer-days
- Utilization: 164 / 188 = 0.8723, rounded to 87 percent
- Remaining plannable capacity: 188 - 164 = 24 engineer-days

Nothing moves to Next.

| Team | Plannable | Standing demand | Initiatives above the line | Committed | Utilization | Over or under | Moves to Next |
|---|---:|---:|---|---:|---:|---|---|
| Payments squad | 188 | 43 | Legacy sunset decommission 30; peak readiness and freeze support 15; DEP-4 support 15; tech debt payoff 6; Kestrel region failover rehearsal 25; table-shape removal preparation 30 | 164 | 87 percent | Under by 24 engineer-days | Nothing |

## 6. Gaps and hiring

No capacity gap is identified. The plan has 24 engineer-days of remaining plannable capacity, and no work is moved to Next. No hire or borrowing decision is required for Q4 2026.

| Gap | Team | Units short | Option (hire / borrow / descope / defer) | Decision owner | Needed by | Scorecard |
|---|---|---|---|---|---|---|
| None identified | Payments squad | Not applicable | Retain the approved plan; no hire, borrow, descope or defer decision | Tomasz Wierzbicki | Not applicable | Not applicable |

## 7. Assumptions this plan rests on

The assumption that no sixth engineer is needed rests on the interpretation of the SPACE scores in HC48, rather than being a direct read from the data. HC48 provides scores where satisfaction and efficiency improved while activity rose, suggesting process bottlenecks rather than resource shortages. Based on this interpretation, the next cycle should buy flow, not capacity. This plan therefore carries the existing 5 engineers rather than adding a sixth.

| Assumption | If wrong | Tracked in |
|---|---|---|
| No sixth engineer is needed for the sunset and peak freeze, based on the interpretation of the SPACE scores in HC48 | The sunset or peak support work exceeds the 188 engineer-day plannable line, so the balance is revisited before committing additional work | [harbourgate-space-framework.md](harbourgate-space-framework.md) and this capacity plan |
| N54's 0.4 FTE legacy on-call share returns after the legacy path shutdown on 2026-12-15 | On-call and support demand remains higher than the 40 engineer-days deducted from gross supply, reducing available capacity for table-shape preparation and other Q4 work | R10 and this capacity plan |

---

## Exit gate (feeds the roadmap and Gate 2: requirements signed off)

- [x] One unit is used throughout
- [x] Every supply row subtracts leave, on-call, and recurring load before the 80 percent line is drawn
- [x] Every demand row carries low, likely, and high figures, and says whether missing work was checked
- [x] Standing demand includes debt interest and last period's support actual
- [x] No team is committed above its plannable figure; anything over the line is named and moved to Next
- [x] Every gap has an option, a decision owner, and a needed-by date
- [x] The roadmap's Now column matches what sits above the line here
- [x] The ILLUSTRATIVE rows have been deleted
- [x] Signed by Tomasz Wierzbicki, 2026-10-16
