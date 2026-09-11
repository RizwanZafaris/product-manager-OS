# Harbourgate SPACE Framework: squad capacity and flow

Fills [frameworks/metrics/space-framework.md](../frameworks/metrics/space-framework.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and identifier is ILLUSTRATIVE, taken from the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md). It is not a benchmark or a target.

**Owner:** Tomasz Wierzbicki, Engineering Lead · **Date:** 2026-10-12 · **Product:** Harbourgate checkout · **Stage:** OPERATE

## What it is for

This worksheet answers Tomasz Wierzbicki's question on 2026-10-12:

> "can the squad carry the sunset and the peak freeze without a sixth engineer?"

The answer must be team-level, not an individual productivity ranking. The slate covers satisfaction and well being, performance, activity, communication and collaboration, and efficiency and flow. It combines a repeated pulse with telemetry so that no single activity measure is treated as productivity.

The method follows Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, and Jenna Butler, from "The SPACE of Developer Productivity" (ACM Queue 19(1), 2021), from [knowledge/INDEX.md](../knowledge/INDEX.md) and the [SPACE framework](../frameworks/metrics/space-framework.md).

## Run it when

- A leader asks whether the Harbourgate payments squad can carry the legacy sunset and the peak freeze.
- The capacity decision could be mistaken for a request for another engineer.
- The team needs a balanced read across human experience, outcomes, activity, communication and flow.
- A productivity claim needs evidence before it changes the staffing assumption.

**Skip it when:** the constraint is already known and named in daily work. This sheet is not a substitute for fixing a known queue or approver bottleneck.

## Inputs you need first

- The question in the asker's words and the decision it changes.
- A repeated pulse with stable wording. The satisfaction question was, "I can sustain this pace", with 4 of 7 agreeing in June 2026 and 6 of 7 agreeing in September 2026.
- The Gate 6 outcome and change failure evidence for Quay.
- Deployment telemetry from the build and release system.
- Review latency telemetry.
- Payment-path page counts and the legacy on-call share.
- The team shape: 5 engineers, 1 QA lead and 1 PM, from N63 in the [Harbourgate journey](harbourgate-journey.md).
- The comparison period for the capacity plan, the baseline window 2026-09-01 to 2026-09-30, from HC48 in the [coverage sheet](harbourgate-coverage-sheet.md). Note that no metric on this slate is measured against that window; the telemetry figures are measured over the Gate 6 comparison window, 2026-09-08 to 2026-10-05, from N67.
- The peak change freeze constraint from N64, 2026-11-13 to 2026-12-04. This slate does not measure it; it is a target and its satisfaction is assumed from the freeze and rollback provisions, not evidenced here.

## The worksheet

### The five dimensions

| Dimension | What it measures | Instrument used here | What it cannot see |
|---|---|---|---|
| Satisfaction and well being | Whether the squad can sustain the pace | Repeated pulse, same wording in June 2026 and September 2026 | Output, quality or flow by itself |
| Performance | Whether shipped changes hold up in production | Change failure rate, read beside N18 | The human cost of getting there |
| Activity | Counts of output | Production deployments per week | Value, quality or whether the work was needed |
| Communication and collaboration | How work and knowledge move | Review requested to merged latency | Whether review produced a sound decision |
| Efficiency and flow | Interruptions and flow burden | On-call pages for the payment path (N22) and legacy on-call share (N54), as an alert-volume and borrowed-capacity proxy for flow, not a flow measurement | Whether the faster flow produced valuable work |

### Step 1: frame the question and the level

| The question in the asker's words | What they will do with the answer | Level: individual, team, or system | Period and baseline window | Will any row reach a performance review or a cross-person comparison? |
|---|---|---|---|---|
| "can the squad carry the sunset and the peak freeze without a sixth engineer?" | Use the read as the Q4 capacity plan's section 7 assumption, deciding whether the next cycle buys capacity or buys flow | team | 2026-09-01 to 2026-09-30 is the comparison period for the capacity plan (HC48). The telemetry window is the Gate 6 comparison window, 2026-09-08 to 2026-10-05 (N67). The peak change freeze (N64, 2026-11-13 to 2026-12-04) is assumed satisfied by the freeze and rollback provisions and is not measured on this slate. | no |

No row reaches a performance review or a cross-person comparison. The answer is about the squad's operating conditions, not a ranking of the 5 engineers.

### Step 2: the slate

| Dimension | Metric (numerator / denominator, period) | Level | Perceptual or telemetric | Owner (one name) | Baseline (date) | How it rises while the work gets worse | Guardrail that catches that |
|---|---|---|---|---|---|---|---|
| Satisfaction and well being | Share agreeing with "I can sustain this pace": 4 of 7 in June 2026 and 6 of 7 in September 2026, repeated pulse | team | perceptual | Tomasz Wierzbicki | 2026-09-30, with the June 2026 pulse as the earlier comparison | The pulse is sent after an easy period, or people agree because they feel pressure to support the plan | Keep the wording fixed, repeat the pulse, and read it beside performance, activity and efficiency |
| Performance | Change failure rate = remedial deployments / production deployments: 1 / 17 = 5.9% in the Gate 6 comparison window (2026-09-08 to 2026-10-05), read beside N18's decline rates of Kestrel connector 6.5%, former Marlowe cohort 8.7% and kiosks 3.0% of attempts | team | telemetric | Bea Lindqvist | 2026-10-05, with the previous window at 2 / 12 = 16.7% | The squad makes fewer, larger releases, or avoids changes that would reveal failures | Read change failure rate beside deployment count and N18, and keep the no-customer-impact incident check |
| Activity | Production deployments per week = 17 deployments / 4 weeks = 4.25 deployments per week, Gate 6 comparison window (2026-09-08 to 2026-10-05) | team | telemetric | Bea Lindqvist | 2026-10-05 | One change is split into several deployments, or low-value work is shipped to raise the count | Read only beside the performance and satisfaction rows |
| Communication and collaboration | Median time from review requested to merged, 0.6 days, Gate 6 comparison window (2026-09-08 to 2026-10-05); no prior reading exists | team | telemetric | Tomasz Wierzbicki | No prior reading. Instrumentation task dated 2026-10-12 | Reviews are merged quickly with little scrutiny, or work avoids review | Establish and retain a pre-September comparison at the next run, with review depth and change failure rate read together |
| Efficiency and flow | On-call pages for the payment path (N22) fell from 11 in March 2026 to 4 in September 2026, so 11 - 4 = 7 fewer pages; legacy on-call share (N54) is 0.4 FTE through the sunset. This is an alert-volume and borrowed-capacity proxy for flow, not a flow measurement | team | telemetric | Bea Lindqvist | 2026-09-30, with March 2026 as the earlier page baseline | Pages fall because alerts are suppressed, or flow improves only by borrowing 0.4 FTE of on-call capacity from the squad | Check the on-call tool for pages, retain alert coverage, and remove the legacy share after 2026-12-15 rather than treating it as free capacity |

The communication row scores 1 because it has no prior reading before the next run establishes one. Tomasz Wierzbicki owns the dated instrumentation task from 2026-10-12. The row remains visible and is not treated as covered until a baseline exists.

### Step 3: the coverage arithmetic

Scores:

- Satisfaction and well being = 2
- Performance = 2
- Activity = 2
- Communication and collaboration = 1
- Efficiency and flow = 2

Coverage total:

`2 + 2 + 2 + 1 + 2 = 9 of 10`

Let D be the count of dimensions scoring 2:

`D = 4`

| Check | Arithmetic | Pass condition | Result |
|---|---|---|---|
| Three dimensions, minimum | `D = 4` dimensions scoring 2 | D is 3 or more | Pass, 4 is greater than or equal to 3 |
| Something was asked, not only logged | Satisfaction is 1 perceptual row among the 4 dimensions scoring 2 | 1 or more | Pass, 1 is greater than or equal to 1 |
| Activity is not carrying the slate | `D - 1 = 4 - 1 = 3` | 2 or more | Pass, 3 is greater than or equal to 2 |
| Every row is gameable on paper | 4 rows scoring 2 have both a gaming move and a guardrail, so `4 / 4 = 1` | equals 1 | Pass |
| No row is a ranking | Individual-level rows appearing in any cross-person comparison = 0 | 0 | Pass |

The slate is quotable at team level:

- Total coverage: `9 of 10`
- D: `4`
- Perceptual rows among D: `1`
- Activity-independent dimensions among D: `3`
- Gameable covered rows: `4 / 4 = 1`
- Individual or cross-person comparison rows: `0`

Communication remains a score of 1 and becomes an instrumentation task, not a caveat to hide in the result.

## Reading the result

The rows are read in pairs rather than one at a time.

| What you see | What it means | The action it implies |
|---|---|---|
| Activity up, performance better | Deployments increased from 12 in the previous window to 17 in the Gate 6 comparison window, while change failure rate moved from `2 / 12 = 16.7%` to `1 / 17 = 5.9%` | Do not use activity growth as evidence for a sixth engineer. Preserve the release flow and its guardrails |
| Activity up, satisfaction up | Deployments are 4.25 per week in the Gate 6 comparison window, and the pulse moved from 4 of 7 agreeing in June 2026 to 6 of 7 in September 2026 | The higher activity is not currently showing a satisfaction cost. Re-run the pulse rather than assuming the result will persist |
| Efficiency better, communication incomplete | On-call pages fell from 11 in March 2026 to 4 in September 2026, while review latency is 0.6 days with no prior baseline | Keep the proxy reading, but instrument communication before making a stronger claim. Note this is an alert-volume proxy, not a flow measurement |
| Performance better, activity up | `1 / 17 = 5.9%` change failure rate in the Gate 6 window accompanies 4.25 deployments per week | The squad is shipping more often with fewer remedial deployments in the comparison window. Do not turn this into an individual target |
| Efficiency burden remains | The legacy path still consumes 0.4 FTE of on-call share | Buy flow by removing the legacy burden through the planned sunset, not capacity by adding a sixth engineer |
| Satisfaction up, other rows not all complete | The pulse improved from 4 of 7 to 6 of 7, but communication has no prior baseline | Treat the pulse as one positive signal, not proof that every dimension improved |

The combined read is:

- Satisfaction improved from 4 of 7 to 6 of 7.
- Activity is 17 deployments over the Gate 6 comparison window (2026-09-08 to 2026-10-05), which is `17 / 4 = 4.25 deployments per week`.
- Performance improved from `2 / 12 = 16.7%` remedial deployments to `1 / 17 = 5.9%`.
- On-call pages for the payment path fell by `11 - 4 = 7`.
- The legacy path still consumes 0.4 FTE of on-call share.
- Communication is not yet comparable because the 0.6-day review latency has no prior baseline.

The answer to Tomasz Wierzbicki's question is no: the evidence does not support adding a sixth engineer for this decision. The next cycle should buy flow, specifically by removing the legacy on-call burden and protecting the existing release and review flow. This lands as the Q4 capacity plan's section 7 assumption. No row reaches a cross-person comparison. The peak change freeze (N64) is assumed satisfied by the change-freeze and rollback provisions and is not measured on this slate, so this read does not speak to it directly.

Any dimension scoring 1 names its own next task. Here, communication and collaboration requires dated instrumentation owned by Tomasz Wierzbicki, beginning from the 2026-10-12 decision record and establishing a pre-September comparison before the next planning read.

**Re-run trigger:** re-run this slate at the start of the next planning period, feeding the Q4 capacity plan's next cycle, or sooner if the squad changes shape (a joiner, a leaver, a split, a new manager), or once the legacy path's 0.4 FTE on-call share (N54) disappears after the 2026-12-15 sunset. A baseline measured against the current five-engineer, legacy-carrying shape describes a team that will no longer exist once the sunset lands.

## ILLUSTRATIVE example

This Harbourgate example uses the five-dimension slate in HC48. All figures are ILLUSTRATIVE and are sourced from N18, N22, N54, N63, HC47 and HC48 in the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md).

The ask was made by Tomasz Wierzbicki on 2026-10-12. The level was team. The capacity-plan comparison period was 2026-09-01 to 2026-09-30 (HC48); the telemetry window for change failure rate, deployments and review latency is the Gate 6 comparison window, 2026-09-08 to 2026-10-05 (N67). The squad has 5 engineers, 1 QA lead and 1 PM.

| Dimension | Metric (ILLUSTRATIVE) | Instrument | Owner | Baseline (ILLUSTRATIVE) | Gaming move | Guardrail |
|---|---|---|---|---|---|---|
| Satisfaction and well being | "I can sustain this pace": 4 of 7 in June 2026 and 6 of 7 in September 2026 | perceptual pulse | Tomasz Wierzbicki | 2026-09-30, compared with June 2026 | Send the pulse after an easy period | Fixed wording and repeated send, read with telemetry |
| Performance | Remedial deployments / production deployments: `1 / 17 = 5.9%`, beside N18, Gate 6 comparison window | build and release system | Bea Lindqvist | 2026-10-05 | Make fewer, larger releases | Read with deployment count and N18 |
| Activity | `17 / 4 = 4.25` production deployments per week, Gate 6 comparison window | build and release system | Bea Lindqvist | 2026-10-05 | Split one change into several deployments | Read only with performance and satisfaction |
| Communication and collaboration | Median review requested to merged: 0.6 days, Gate 6 comparison window; no prior reading | build and release system | Tomasz Wierzbicki | No prior reading | Merge quickly without review depth | Instrument a baseline and read with change failure rate |
| Efficiency and flow | On-call pages (N22): 11 in March 2026 and 4 in September 2026, `11 - 4 = 7` fewer; legacy on-call share (N54): 0.4 FTE. Alert-volume and borrowed-capacity proxy, not a flow measurement | on-call tool and engineering estimate | Bea Lindqvist | 2026-09-30 | Suppress pages or treat legacy work as free capacity | Retain alert coverage and remove the legacy share at sunset |

Coverage arithmetic reuses the figures from Step 3: `9 of 10`, with `D = 4`.

The four fully instrumented dimensions are satisfaction and well being, performance, activity, and efficiency and flow. Communication is the one incomplete dimension because its review-latency baseline is missing. The slate passes every check because:

- `D = 4`, so the minimum-three check passes.
- Perceptual rows among D = `1`, so the human-input check passes.
- Activity-independent dimensions = `4 - 1 = 3`, so activity is not carrying the slate.
- Gameable covered rows = `4 / 4 = 1`.
- Individual-level or cross-person comparison rows = `0`.

The decision is to buy flow, not capacity. The Q4 capacity plan carries that as its section 7 assumption. The peak change freeze (N64) is assumed satisfied and is not measured on this slate.

## The trap

The trap would be carrying 4.25 deployments per week onto a dashboard as proof that the squad needs more engineers. That would turn activity into a target and erase the other four dimensions.

The current evidence does not support that reading. The activity row rose while change failure rate improved from `2 / 12 = 16.7%` to `1 / 17 = 5.9%`, and the satisfaction pulse improved from 4 of 7 to 6 of 7. On-call pages fell from 11 to 4. The remaining burden is the 0.4 FTE legacy on-call share, which is a flow problem connected to the sunset.

The communication row is also a warning. A median review latency of 0.6 days looks precise, but without a prior baseline before September it cannot show whether communication improved or merely changed. It scores 1, stays visible, and becomes a dated instrumentation task.

The slate must not be used to rank the 5 engineers. No row is individual-level, and no result reaches a performance review or a cross-person comparison. The question is whether the team can carry the work, not which person is productive.

## Feeds

- [harbourgate-journey.md](harbourgate-journey.md), N18, N22, N54, N63 and N64, for the payment outcome, pages, legacy on-call share, team shape and peak freeze target.
- [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), HC47 and HC48, for the DORA comparison and the SPACE slate.
- Q4 capacity plan, section 7, where the read lands as the assumption that the next cycle buys flow, not capacity.
- Metrics dictionary, where the five slate rows become named metrics.
- Metrics review, where the guardrails are read beside the metrics they guard.
- Gate 6, where the outcome evidence supports the operating decision.
