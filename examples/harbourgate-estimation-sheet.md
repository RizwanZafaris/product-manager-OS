# Harbourgate Estimation Sheet: ADR-0004

Fills [frameworks/execution/estimation-sheet.md](../frameworks/execution/estimation-sheet.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE. See the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Tomasz Wierzbicki · **With:** Bea Lindqvist · **Date:** 2026-06-18

## What it is for

This sheet estimates ADR-0004, dual-path settlement reconciliation for Harbourgate. It uses t-shirt sizing, story points, a three-point estimate and a reference-class check. The estimate is a range, with the planning and external commitment figures stated separately.

## Run it when

- ADR-0004 is being sized after D-021 reshaped the plan
- The cutover plan needs the reconciliation work in engineer-weeks
- The team needs a commitment that includes the finance close runbook and rehearsals

## Inputs you need first

- Scope: ADR-0004, matching settlement on either reference while both paths drain
- Measured velocity for the last six two-week sprints: low 21, median 26, high 30 points
- Three-point components in engineer-weeks, from HC31
- A reference class, with fewer than five reference projects available
- Dependency register item DEP-3, the finance daily-close runbook

## The worksheet

### Step 1: t-shirt size for triage

ADR-0004 is M because the expected work is in the three to six engineer-week band. No named past project of the same size is available in the Harbourgate reference set.

| Item | Size | Past item of the same size it was compared to |
|---|---|---|
| ADR-0004, dual-path reconciliation | M | No named comparison project available |

### Step 2: story points, one team only

The story is 21 points. Velocity is measured, not negotiated, from the last six two-week sprints.

| Story | Points | Reference story compared to | Velocity per sprint, last six: low / median / high | Sprints needed: points / high, points / median, points / low |
|---|---:|---|---|---|
| ADR-0004, matching on either reference, straddle classification, rehearsals and AC-8 tests | 21 | No named reference story available | 21 / 26 / 30 points | 21 / 30 = 0.7, 21 / 26 = 0.8, 21 / 21 = 1 sprint |

### Step 3: three-point (PERT)

All values are engineer-weeks. P was set from the failure case in which settlement lines remain unmatched and the dual-path work also needs the finance close and rehearsal coverage.

| Component | O | M | P | E | SD |
|---|---:|---:|---:|---:|---:|
| Matching on either reference | 1 | 1.5 | 3 | (1 + 4 x 1.5 + 3) / 6 = 10 / 6 = 1.7 | (3 - 1) / 6 = 0.3 |
| Straddle classification | 0.5 | 1 | 2 | (0.5 + 4 x 1 + 2) / 6 = 6.5 / 6 = 1.1 | (2 - 0.5) / 6 = 1.5 / 6 = 0.25 |
| Rehearsal fixtures and AC-8 tests | 0.5 | 1 | 2 | (0.5 + 4 x 1 + 2) / 6 = 6.5 / 6 = 1.1 | (2 - 0.5) / 6 = 1.5 / 6 = 0.25 |
| Total | | | | 1.667 + 1.083 + 1.083 = 3.8 | √(0.3² + 0.25² + 0.25²) = 0.5 |

The total is summed from the unrounded per-component values before they are rounded to 1.7 and 1.1 above; adding the rounded figures shown in the table (1.7 + 1.1 + 1.1) gives 3.9, a rounding artifact, not the 3.8 carried forward. Total expected effort is 3.8 engineer-weeks. The defensible date-equivalent estimate is:

`E + 2 SD = 3.8 + (2 x 0.5) = 4.8 engineer-weeks`

### Step 4: reference class

Fewer than five reference projects are available, so no stable outside-view ratio can be calculated. The range is widened by hand rather than presenting a weak ratio as precise.

| Reference class (past projects like this one) | Count | Actual / estimate at P50 | Actual / estimate at P80 | Source |
|---|---:|---|---|---|
| Dual-path payment reconciliation with settlement drain | Fewer than five | Not stable enough to calculate | Not stable enough to calculate | HC31 in the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md) |

Inside-view total: 3.8 engineer-weeks.

Outside-view treatment: because the reference class has fewer than five projects, the estimate is widened by hand to 3 to 6 engineer-weeks. The planning figure is 4 engineer-weeks and the external commitment is 5 engineer-weeks.

### Step 5: missing work

| Work the stories did not price | Included / excluded / not applicable because | Weeks if excluded |
|---|---|---|
| Compliance or security review | Not applicable because ADR-0004 prices reconciliation implementation and its delivery evidence | Not applicable |
| Operational readiness and runbooks | Included: DEP-3, the finance daily-close runbook updated for dual-path reconciliation | Not applicable |
| Data migration | Not applicable because the work matches settlement records and does not migrate data | Not applicable |
| Instrumentation | Included in the reconciliation checks and AC-8 tests | Not applicable |
| Customer comms and training | Not applicable because this is an internal reconciliation change | Not applicable |
| Rollback and rehearsal | Included: rehearsal fixtures, AC-8 tests and the rehearsals named in HC31 | Not applicable |
| Accessibility | Not applicable because the work changes reconciliation processing, not a customer-facing surface | Not applicable |

## The only output

3 to 6 engineer-weeks, planned at 4, committed at 5.

The actual lands at about 4 engineer-weeks, as recorded in N43, and ADR-0004 was built by 2026-07-03.

## Reading the result

The story-point result is 0.7 to 1 sprint from the measured velocity of 21, 26 and 30 points. The three-point result is 3.8 engineer-weeks, with a standard deviation of 0.5 and E plus 2 SD of 4.8 engineer-weeks.

The reference-class check cannot provide a stable ratio because fewer than five reference projects are available. The wider hand-set range therefore wins over a single inside-view number. The finance close runbook, DEP-3, and the rehearsals are explicitly included so the estimate covers the delivery work exposed by D-021.

## ILLUSTRATIVE example

This Harbourgate example sizes ADR-0004 after D-021 reshaped the plan on 2026-06-18. Tomasz Wierzbicki worked with Bea Lindqvist. The work was sized M at 21 points, against measured velocity of 21, 26 and 30 points, and the three-point estimate was E 3.8 and SD 0.5 engineer-weeks. The output was widened to 3 to 6 engineer-weeks, planned at 4 and committed at 5. Actual effort was about 4 engineer-weeks, and the work was built by 2026-07-03.

## The trap

The trap is quoting the 3.8 engineer-week expected value as the commitment. It excludes the uncertainty represented by the pessimistic cases, the finance close runbook and the rehearsals unless those are named in scope.

A second trap is treating fewer than five reference projects as a reliable ratio. Here, the reference class is admitted as insufficient, so the range is widened by hand and the external commitment is 5 rather than the expected value of 3.8.

## Feeds

- [Harbourgate journey](harbourgate-journey.md), for ADR-0004, D-021, DEP-3, AC-8 and N43
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), for HC30 and HC31
- The migration cutover plan, for the reconciliation work and rehearsal coverage
- The capacity plan, for the demand in engineer-weeks
- ADR-0004, the decision this estimate prices
