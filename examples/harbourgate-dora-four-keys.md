# DORA Four Keys: Harbourgate Quay at Gate 6

Fills [frameworks/metrics/dora-four-keys.md](../frameworks/metrics/dora-four-keys.md). Everything here is invented: Harbourgate, Quay and every person are fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen to reconcile with the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-10-16 · **Product:** Quay · **Window:** 2026-09-07 to 2026-10-05 · **Comparison:** 2026-08-11 to 2026-09-07

## What it is for

This sheet compares Quay with itself across the Gate 6 review window, using the four weeks before it as the previous period. It measures deployment frequency, lead time for changes, change failure rate and time to restore service.

The comparison is against the previous period, not against another team and not against a named DORA performance band. The Gate 6 window had higher deployment frequency, shorter lead time and a lower change failure rate. Neither window had an incident with customer impact.

The result is a total score of plus 3. The decomposition shows release approval as the largest lead-time stage. Counter-metrics are reported beside each key, including the measures that are not available in HC47.

## Run it when

- At Gate 6, to check whether the delivery system improved after the migration and drain
- Before reviewing the peak change freeze while R10 remains open
- When the team needs evidence for a delivery-system decision rather than a general impression of speed
- After a change to how the team ships, so the next window has a comparable before

**Skip it when:** the service ships on somebody else's calendar. That is not the case for Quay in this review. The build and release system supplied the deployment and lead-time evidence, and incident records supplied the stability evidence.

## Inputs you need first

- Production deployment records for Quay
- Commit and release timestamps joined to those deployments
- Remedial deployment records
- Incident records for the review window and the previous window
- A previous period for comparison
- The Gate 6 window definition from N67
- The supporting operational evidence in HC24 and HC47

The source data is the [Harbourgate journey](harbourgate-journey.md), especially N22, N64, N67 and R10, and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), especially HC24 and HC47.

## The worksheet

### Step 1: agree the four definitions before anyone reads a number

| Key | Clock starts | Clock stops | Counting rule | Source system | Value this period | Same figure last period |
|---|---|---|---|---|---|---|
| Deployment frequency | Not applicable, it is a count | Not applicable | One promotion of one artifact to production counts once, whatever it contains | Build and release system | 17 deployments / 4 weeks = 4.25 per week | 12 deployments / 4 weeks = 3.0 per week |
| Lead time for changes | First commit on the branch | The change is serving production traffic | Report the median and the 85th percentile | Build and release system | Median 2.2 days; 85th percentile 5.0 days | Median 3.1 days; 85th percentile 7.4 days |
| Change failure rate | Not applicable, it is a ratio | Not applicable | A deployment failed if it needed a remedial deployment | Build and release system | 1 remedial deployment / 17 deployments x 100 = 5.9% | 2 remedial deployments / 12 deployments x 100 = 16.7% |
| Time to restore service | Impact began, using the agreed impact rule | Service restored, not root cause found | Report the median and the worst case | Incident records | No incident with customer impact, so no restore duration | No incident with customer impact, so no restore duration |

The arithmetic:

- Deployment frequency = production deployments in the window / weeks in the window
- This period = 17 / 4 = 4.25 per week
- Previous period = 12 / 4 = 3.0 per week
- Lead time for one change = time serving production minus time of first commit
- This period reports a median of 2.2 days and an 85th percentile of 5.0 days
- Previous period reports a median of 3.1 days and an 85th percentile of 7.4 days
- Change failure rate = deployments needing a remedial deployment / all production deployments x 100
- This period = 1 / 17 x 100 = 5.882..., reported as 5.9%
- Previous period = 2 / 12 x 100 = 16.666..., reported as 16.7%
- Time to restore for one incident = time restored minus time impact began
- Neither window contains an incident with customer impact, so there is no restore duration to calculate

### Step 2: score the direction of travel

The 20% noise band and its floors are the local heuristic described in the worksheet, not part of the delivery-performance research of Nicole Forsgren, Jez Humble and Gene Kim. The score is against Quay's own previous period.

For deployment frequency, the previous value is 3.0 per week. Its 20% noise band is:

- 3.0 x 20% = 0.6 deployments per week
- The frequency floor is one deployment per week
- Noise band used = one deployment per week
- Change = 4.25 - 3.0 = 1.25 deployments per week
- 1.25 is outside the one-deployment noise band, so the score is plus 1

For lead time, the previous median is 3.1 days. Its 20% noise band is:

- 3.1 x 20% = 0.62 days
- Change = 3.1 - 2.2 = 0.9 days shorter
- 0.9 is outside the 0.62-day noise band, so the score is plus 1

For change failure rate, the previous value is 16.7%. Its 20% noise band is:

- 16.7% x 20% = 3.34 percentage points
- Change = 16.7% - 5.9% = 10.8 percentage points lower
- 10.8 percentage points is outside the 3.34-point noise band, so the score is plus 1

For time to restore, neither period has an incident with customer impact. There is no median duration to compare, so the score is 0, unchanged.

| Key | Previous | This period | Change | Noise band | Score (minus 1, 0, plus 1) |
|---|---|---|---|---|---|
| Deployment frequency | 3.0 per week | 4.25 per week | 4.25 - 3.0 = 1.25 per week higher | 20% of 3.0 = 0.6, floored at one deployment per week | plus 1 |
| Lead time, median | 3.1 days | 2.2 days | 3.1 - 2.2 = 0.9 days shorter | 3.1 x 20% = 0.62 days | plus 1 |
| Change failure rate | 2 of 12 = 16.7% | 1 of 17 = 5.9% | 16.7% - 5.9% = 10.8 percentage points lower | 16.7% x 20% = 3.34 percentage points | plus 1 |
| Time to restore, median | No incident with customer impact | No incident with customer impact | No duration in either period | No duration to score | 0 |
| | | | | **Total: 1 + 1 + 1 + 0** | **plus 3** |

The scores describe direction, not performance quality. The stability result is read alongside the counts: one remedial deployment out of 17 this period, compared with two out of 12 previously. The absence of an incident with customer impact is not converted into an invented restore time.

### Step 3: decompose the worst key

The largest lead-time stage is release approval. The median stages sum exactly to the reported median:

- 0.4 + 0.6 + 0.1 + 0.9 + 0.2 = 2.2 days

The share arithmetic is:

- First commit to review requested = 0.4 / 2.2 x 100 = 18.181..., reported as 18.2%
- Review requested to merged = 0.6 / 2.2 x 100 = 27.272..., reported as 27.3%
- Merged to build and tests done = 0.1 / 2.2 x 100 = 4.545..., reported as 4.5%
- Tests done to release approved = 0.9 / 2.2 x 100 = 40.909..., reported as 40.9%
- Approved to serving production = 0.2 / 2.2 x 100 = 9.090..., reported as 9.1%
- Total share = 18.2% + 27.3% + 4.5% + 40.9% + 9.1% = 100.0%, allowing for rounding

| Stage (lead time) | Median time | Share of lead time | Who is waiting | Fix candidate |
|---|---:|---:|---|---|
| First commit to review requested | 0.4 days | 0.4 / 2.2 = 18.2% | The change author, before review is requested | Keep the review request close to the first commit |
| Review requested to merged | 0.6 days | 0.6 / 2.2 = 27.3% | The change author, waiting for review | Inspect review queue ageing beside the lead-time metric |
| Merged to build and tests done | 0.1 days | 0.1 / 2.2 = 4.5% | The merged change, waiting for verification | No immediate change indicated by this decomposition |
| Tests done to release approved | 0.9 days | 0.9 / 2.2 = 40.9% | The tested change, waiting for release approval | Review the approval queue and approval policy before changing the freeze |
| Approved to serving production | 0.2 days | 0.2 / 2.2 = 9.1% | The approved change, waiting for promotion | No immediate change indicated by this decomposition |
| **Total** | **0.4 + 0.6 + 0.1 + 0.9 + 0.2 = 2.2 days** | **100.0%** | | |

The release-approval stage is the largest stage at 0.9 days, or 40.9% of the median. The evidence supports examining that queue. It does not support removing the peak change freeze while R10 is open.

For time to restore, the same detect, page, diagnose, remediate and confirm decomposition cannot be run for either window because neither window contains an incident with customer impact.

### Step 4: one counter-metric per key

| Key | How it moves without improving | Counter-metric reported beside it | Owner |
|---|---|---|---|
| Deployment frequency | Empty deployments, or one artifact split into several promotions, can raise the count without adding customer-visible change | Share of deployments carrying no customer-visible change was not reported in HC47, so the 4.25 per week figure is not treated as proof of customer value | Bea Lindqvist |
| Lead time for changes | The branch can be cut late, or work can wait before the first commit, leaving the measured clock unchanged | Age of the oldest open change, timed from when work started, was not reported in HC47; the stage decomposition instead reports the 0.9-day release-approval wait | Tomasz Wierzbicki |
| Change failure rate | Incidents can go unrecorded, or a failure can be relabelled as a planned follow-up | Remedial deployments from the build and release system: 1 of 17 this period, 2 of 12 previously. The incident record reports no incident with customer impact in either window | Bea Lindqvist |
| Time to restore service | The clock can start at declaration rather than at impact | Time from first customer report to declaration was not reported because neither window has an incident with customer impact | Callum Fraser |

The four September pages were closed without customer impact, and no incident record was opened on the payment path between 2026-08-11 and 2026-10-05. They are reported as operational context, not as restore-time observations.

## How to read the result

Throughput improved and the measured stability key also improved:

- Deployment frequency moved from 3.0 to 4.25 per week
- Median lead time moved from 3.1 to 2.2 days
- Change failure rate moved from 16.7% to 5.9%
- Neither period had an incident with customer impact

The total of plus 3 is therefore useful as a summary, but it is not a grade. The decomposition supplies the more actionable finding: tests completed after 0.1 days, while release approval took 0.9 days, the largest stage in the 2.2-day median.

The counter-metrics limit the interpretation. The share of deployments carrying no customer-visible change and the age of the oldest open change were not reported in HC47. The frequency and lead-time improvements should therefore be read as delivery-system movement, not as proof that customer value increased or that all waiting time fell.

The four September pages were closed without customer impact, as recorded in HC24. There is no time-to-restore comparison because neither window contains an incident with customer impact.

No DORA performance band is quoted. This sheet uses a self-comparison only. The 20% scoring rule is a local heuristic authored in the worksheet, not a threshold specified by Forsgren, Humble and Kim.

## ILLUSTRATIVE example

Quay is Harbourgate's payment service. The previous window was 2026-08-11 to 2026-09-07, and the Gate 6 window was 2026-09-07 to 2026-10-05.

| Key | Previous | This period | Noise band | Score |
|---|---|---|---|---|
| Deployment frequency | 12 deployments / 4 weeks = 3.0 per week | 17 deployments / 4 weeks = 4.25 per week | 20% of 3.0 = 0.6, floored at one deployment per week | plus 1 |
| Lead time, median | 3.1 days | 2.2 days | 3.1 x 20% = 0.62 days | plus 1 |
| Lead time, 85th percentile | 7.4 days | 5.0 days | Reported, not scored | |
| Change failure rate | 2 of 12 = 16.7% | 1 of 17 = 5.9% | 16.7% x 20% = 3.34 percentage points | plus 1 |
| Time to restore, median | No incident with customer impact | No incident with customer impact | No duration to score | 0 |

Total: 1 + 1 + 1 + 0 = plus 3.

Decomposition of the 2.2-day median lead time:

- First commit to review requested: 0.4 days
- Review requested to merged: 0.6 days
- Merged to build and tests done: 0.1 days
- Tests done to release approved: 0.9 days
- Approved to serving production: 0.2 days
- Total: 0.4 + 0.6 + 0.1 + 0.9 + 0.2 = 2.2 days

Release approval is 0.9 / 2.2 x 100 = 40.9% of the median, the largest stage.

The counter-metric evidence is deliberately incomplete where the source is incomplete. Remedial deployment counts are available and show 1 of 17 this period. The share of deployments carrying no customer-visible change, the age of the oldest open change and time from first customer report to declaration are not reported in HC47. The four September pages were closed without customer impact, and no incident with customer impact occurred in either window.

## The decision it feeds

Keep the peak change freeze exactly as written in N64 while R10 is open:

> 2026-11-13 to 2026-12-04: no Quay or flag changes except rollbacks.

The DORA result does not justify weakening that decision. Delivery throughput and stability improved, but R10 remains open because peak trading lands inside the drain and a rollback would need providers whose contracts are under notice. The release-approval decomposition is a candidate for later flow work, not a reason to change the freeze.

The review also records the follow-up:

- Keep N64 unchanged
- Keep the legacy path warm to 2026-12-15 as the mitigation for R10
- Review the release-approval queue after the freeze
- Add the missing counter-metric readings before treating the frequency or lead-time movement as customer-value evidence

## Where the output lands

- The Gate 6 metrics review, where the movement is read against the expected outcome
- The peak change freeze decision under N64, with R10 retained as open
- The delivery-system work queue, with release approval recorded as the largest lead-time stage
- The operational review for Quay, with HC24 and HC47 as the evidence for the window

## Re-run trigger

Re-run at the next planning-period review, and again after a change to how Quay ships, including a new approval step, a test-suite rebuild, a branching change, a team split or a change to the on-call group.

The next run should preserve the same definitions and report the missing counter-metrics where the build and release system can supply them.

## When this method misleads you

The four keys describe a delivery system, not a team leaderboard and not customer value. Splitting one artifact into several promotions can raise frequency. Starting the lead-time clock late can make lead time appear shorter. Unrecorded incidents can reduce change failure rate. Starting a restore clock at declaration can reduce time to restore.

The service boundary also matters. These figures describe Quay, not Harbourgate's whole checkout, all payment providers or every product surface.

The Gate 6 window contains 17 deployments, so the denominator is visible beside the 5.9% rate. The previous window contains 12 deployments, so its 16.7% rate is also reported with its count. The absence of an incident with customer impact is useful evidence, but it is not a restore-time measurement.

Finally, the four keys do not measure whether shoppers completed payment, whether payment data was correctly reconciled or whether the migration reduced customer harm. Those outcomes remain in the Harbourgate metrics, including N18, N19, HC20 and HC24.

## Feeds

- [Harbourgate journey](harbourgate-journey.md), the canonical product data sheet and identifier register
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), HC24 and HC47 for the Gate 6 operational and DORA evidence
- Gate 6 review, 2026-10-14, where Quay was recorded as PERSIST
- N64, the peak change freeze retained exactly as written
- R10, the open risk that keeps the freeze in place
- The Gate 6 metrics review, where the plus 3 total is read with its decomposition and counter-metrics

Gate 6 exit-gate walk: I checked the window definition, deployment arithmetic, lead-time arithmetic, change-failure arithmetic, incident evidence, decomposition total, counter-metric gaps and the decision against N64 and R10. The peak change freeze remains unchanged.

**Signed:** Ife Adeyemi, Product Manager · **Date:** 2026-10-16
