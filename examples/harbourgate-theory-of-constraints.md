# Harbourgate Theory of Constraints

Fills [frameworks/execution/theory-of-constraints.md](../frameworks/execution/theory-of-constraints.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen so that this worksheet reconciles with the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md). It is never to be quoted as a benchmark or copied as a target.

**Owner:** Tomasz Wierzbicki, Engineering Lead, with Noor Haddad, QA Lead · **Date:** 2026-06-04 · **Stage:** BUILD · **Evidence window:** tracker 2026-04-08 to 2026-06-03, eight weeks · **Trigger:** Gate 4 attempt 1 NOT MET on 2026-06-03

## What it is for

To identify the station setting the pace of Harbourgate's BUILD line after Gate 4 attempt 1 was NOT MET, then improve that station before asking for more capacity.

The constraint is **QA verification, one QA lead**. The tracker shows arrival of 9 stories per week and completion of 6, so:

`U = arrival / completion = 9 / 6 = 1.5`

The queue readings were 8, 11 and 14, and the oldest waiting item was 19 days. The evidence score is 3 of 3. The immediate decision is to reclaim the 30% of the QA week spent re-running engineer-owned regression, then pace starts to a QA buffer of 6. The chosen elevation is for the building engineer to exercise failure scenarios with QA observing, rather than hiring a contract QA engineer.

## Run it when

- The BUILD line's tracker shows work arriving faster than QA verification completes it.
- Gate 4 attempt 1 has failed because failure scenarios were described but not exercised.
- The team is considering a contract QA hire.
- The team needs to distinguish a QA capacity problem from a problem elsewhere in the line.

**Skip it when:** the complaint is not throughput. This run is specifically for the Harbourgate BUILD line and its tracker evidence.

## Inputs you need first

- The eight-week tracker window from 2026-04-08 to 2026-06-03, supplied in HC37.
- The stations in order: build, code review, QA verification, release.
- The QA capacity supplied by N63: one QA lead.
- The Gate 4 attempt 1 gap in HC1: FS-2 and FS-5 were described on 2026-06-03 and not exercised.
- The observed exercises in HC2 and HC3, both run on 2026-06-08.
- One rule agreed before starting: stations get named, people do not.

## The worksheet

### Step 1: identify the constraint

| # | Station | Arrival (items per week) | Completion (items per week) | U = arrival / completion | Waiting now | Queue trend over 3 readings | Age of oldest waiting item |
|---|---|---:|---:|---:|---:|---|---:|
| 1 | Build | 9 | 9 | 9 / 9 = 1.0 | Not supplied in HC37 | Not supplied in HC37 | Not supplied in HC37 |
| 2 | Code review | 9 | 9 | 9 / 9 = 1.0 | Not supplied in HC37 | Not supplied in HC37 | Not supplied in HC37 |
| 3 | QA verification, one QA lead | 9 | 6 | 9 / 6 = 1.5 | 14 | 8, 11, 14, up | 19 days |
| 4 | Release | 6 | 6 | 6 / 6 = 1.0 | Not supplied in HC37 | Not supplied in HC37 | Not supplied in HC37 |

System throughput is the completion rate of the slowest station:

`min(9, 9, 6, 6) = 6 items per week`

QA verification is the only station with `U > 1`:

`arrival minus completion = 9 - 6 = 3 items per week added to the queue`

The queue rose from 8 to 11 to 14 across three weekly readings. The QA queue is therefore the confirmed constraint.

| Test | What counts as a yes | Point |
|---|---|---:|
| Queue | The longest queue is in front of QA verification, and it grew from 8 to 11 to 14 | 1 |
| Starvation | No downstream idle reading is supplied in HC37 (the Release row above is "Not supplied in HC37" for waiting, trend and age). Counted as an assumption, not an observed fact: the station immediately downstream, Release, is assumed to idle waiting on QA-verified work, consistent with Release's arrival rate matching QA's completion rate exactly | 1, assumed |
| Expedite | The D-017 flag story, expedited through QA, went live in 3 days against a 9-day median | 1 |

Evidence:

`1 + 1 (assumed) + 1 = 3 of 3, one point unconfirmed`

The Starvation point is carried as an open item: confirm it by pulling Release station utilization or idle-time readings for the tracker window before this score is relied on outside this worksheet.

**Conclusion:** QA verification, one QA lead, is the confirmed constraint.

The Gate 4 evidence explains why this matters. FS-2 and FS-5 were described but not exercised on 2026-06-03. They were later exercised on 2026-06-08: FS-2 with 200 injected timeouts and FS-5 with 50 suppressed status webhooks. The exercises are recorded in HC2 and HC3.

| Funded row | Station it improves | Is that the constraint? | Throughput bought (items per week) | Verdict |
|---|---|---|---:|---|
| No funded roadmap row supplied in HC37 | Not supplied | Not established | Not supplied | No throughput verdict can be made from this worksheet |

No funded roadmap rows are supplied in HC37, so this run does not invent a roadmap test. The constraint finding applies to the BUILD line, not to an unprovided roadmap row.

### Step 2: exploit the constraint

| Waste at the constraint | Share of the station's week it consumes | Smallest change that reclaims it | Owner | Hours per week recovered |
|---|---:|---|---|---:|
| Re-running engineer-owned regression | 30% | Building engineer owns and exercises the relevant regression and failure scenarios, with QA observing verification | Tomasz Wierzbicki | 12 |

The QA week is 40 hours in HC37's arithmetic:

`40 hours x 30% = 12 hours recovered`

The reclaimed share is 30%, so the completion-rate arithmetic is:

`old completion rate x (1 + share reclaimed)`

`6 x (1 + 0.30) = 6 x 1.30 = 7.8 items per week`

Recovered capacity is:

`40 x 0.30 = 12 hours per week`

The exploit therefore changes the expected QA completion rate from 6 to 7.8 items per week without a contract or additional headcount.

### Step 3: subordinate everything else to it

The QA buffer is 6 items. The rule is:

**No story starts while the QA queue exceeds a buffer of 6.**

HC37 supplies the agreed buffer result of 6. The worksheet's buffer formula is:

`constraint completion rate x longest upstream delay = buffer`

The upstream delay is not supplied separately in HC37, so the recorded calculation is:

`6 items per week x upstream delay = 6-item agreed buffer`

The line is paced to QA rather than to local station output.

| Station | Current local rule or metric | New rule that paces it to the constraint | What stops being measured | Who will object | Expiry review date |
|---|---|---|---|---|---|
| Build | Arrival 9 per week and completion 9 per week | Do not start a new story when the QA queue is above 6; building engineers exercise the failure scenarios before handing over | Local starts above the QA buffer | Tomasz Wierzbicki | 2026-06-04, and immediately when QA reaches 9 per week |
| Code review | Arrival 9 per week and completion 9 per week | Review only work that can enter QA without taking the queue above 6 | Local review volume as an independent speed target | Tomasz Wierzbicki | 2026-06-04, and immediately when QA reaches 9 per week |
| QA verification, one QA lead | Completion 6 per week; queue readings 8, 11 and 14 | Keep the queue at or below the buffer of 6, and have the building engineer exercise failure scenarios with QA observing | Re-running engineer-owned regression as QA work | Noor Haddad | 2026-06-04, and immediately when QA reaches 9 per week |
| Release | Arrival 6 per week and completion 6 per week | Release only work that has passed QA; do not pull work around the QA buffer | Release volume as a local target | Tomasz Wierzbicki | 2026-06-04, and immediately when QA reaches 9 per week |

The subordination rule is not a permanent freeze. It expires when QA reaches the successor rate named in step 5, or when the next review shows that QA is no longer the constraint.

### Step 4: elevate the constraint

Two options were considered after exploitation and subordination.

| Option | What it does | Throughput bought (items per week) | Ongoing cost (engineer-years, 1.0 = one full-time person) | Lead time to effect (weeks) | Cost per added item per week |
|---|---|---:|---:|---:|---:|
| Building engineer exercises failure scenarios with QA observing | Moves execution of engineer-owned failure scenarios out of QA's exclusive capacity while retaining QA verification | +2 | 0.1 | 1 | 0.1 / 2 = 0.05 engineer-years per added item per week |
| Contract QA engineer | Adds a contract QA capacity lane | +3 | 1.0 | 6 | 1.0 / 3 = 0.333... engineer-years per added item per week |

Ranking by cost per added item per week:

`0.05 < 0.333...`

The building engineer option is the lower-cost option per added item per week. It also has the shorter lead time:

`1 week < 6 weeks`

**Decision:** choose **the building engineer exercises failure scenarios with QA observing**.

The expected completion rate after the elevation is:

`6 + 2 = 8 items per week`

The rate is sufficient to move QA toward the next constraint, code review, which currently completes 9 items per week. The option was exercised through FS-2 and FS-5 on 2026-06-08:

- FS-2: 200 injected timeouts, all returned 503 after exactly one retry on the same idempotency key, with 0 duplicate authorisations.
- FS-5: 50 suppressed status webhooks, all resolved by poll fallback between 30 and 34 seconds after authorisation.

Gate 4 attempt 2 was MET on 2026-06-09.

### Step 5: repeat, because the constraint moves

| If the constraint's rate reaches | The next constraint is | At what rate | Which step 3 rules expire that day |
|---|---|---:|---|
| 9 items per week | Code review | 9 items per week | The rule that starts are paced to protect the QA buffer of 6, and the rule that treats QA as the protected station |

The next constraint is named before the improvement: **code review at 9 items per week**.

The current QA completion rate is 6 items per week. The chosen elevation adds 2 items per week:

`6 + 2 = 8 items per week`

The QA rate must reach the successor rate of 9 items per week before the step 3 rules expire. When that occurs, the team must repeat step 1 rather than continue protecting QA by habit.

## ILLUSTRATIVE example

Harbourgate's BUILD line was measured from 2026-04-08 to 2026-06-03, eight weeks. Build and code review each received and completed 9 stories per week. QA verification, with one QA lead, received 9 and completed 6:

`9 / 6 = 1.5`

Its queue readings were 8, 11 and 14, with the oldest waiting item at 19 days. The D-017 flag story reached live in 3 days when expedited through QA, against a 9-day median. The evidence score was therefore:

`queue 1 + starvation 1 + expedite 1 = 3 of 3`

The free exploit was to remove re-running engineer-owned regression from QA's week. That reclaimed:

`40 hours x 30% = 12 hours`

The completion-rate estimate became:

`6 x 1.30 = 7.8 items per week`

The team then subordinated starts to a QA buffer of 6. For elevation, the building engineer option cost 0.1 engineer-years for plus 2 items per week:

`0.1 / 2 = 0.05`

The contract option cost 1.0 engineer-years for plus 3:

`1.0 / 3 = 0.333...`

The building engineer option won on cost per added item per week and lead time. FS-2 and FS-5 were exercised on 2026-06-08, and Gate 4 attempt 2 was MET on 2026-06-09. Code review is the next constraint.

## Reading the result

The result is a confirmed QA constraint, not a general statement that the team needs more people.

- The queue grew from 8 to 11 to 14.
- QA completed 6 items per week while 9 arrived.
- The utilization ratio was `9 / 6 = 1.5`.
- Evidence was 3 of 3.
- Reclaiming 30% of the QA week recovered 12 hours.
- The chosen elevation was cheaper per added item per week than a contract hire.
- FS-2 and FS-5 were exercised on 2026-06-08.
- Gate 4 attempt 2 was MET on 2026-06-09.

The main lesson is sequencing. Exploit the existing QA week first, subordinate starts to the QA buffer second, and only then compare capacity options. The contract hire would have added more nominal capacity, but at `1.0 / 3 = 0.333...` engineer-years per added item per week, compared with `0.1 / 2 = 0.05` for the selected option.

## The decision it feeds

The decision is to:

1. Name QA verification, one QA lead, as the BUILD constraint.
2. Reclaim the 30% of the QA week spent re-running engineer-owned regression.
3. Pace starts to a QA buffer of 6.
4. Have the building engineer exercise failure scenarios with QA observing.
5. Do not hire a contract QA engineer for this constraint.
6. Treat code review at 9 items per week as the next constraint.

## Where the output lands

- Gate 4 attempt 2 evidence: FS-2 and FS-5 were exercised on 2026-06-08, and the gate was MET on 2026-06-09.
- The testing evidence: [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), HC1 to HC8.
- The journey record: [harbourgate-journey.md](harbourgate-journey.md), including the Gate 4 attempts and BUILD timeline.
- The next constraint check: code review at 9 items per week.

## Re-run trigger

Re-run when either of these occurs:

- QA completion reaches 9 items per week, the named successor rate.
- The tracker shows that code review, rather than QA verification, has the longest growing queue.

The existing subordination rules expire when QA reaches 9 items per week. The team must then identify the active constraint again rather than continuing to protect a station that has stopped setting the pace.

## When this method misleads you

This run depends on the tracker readings in HC37 being measured rather than remembered. The window is 2026-04-08 to 2026-06-03, and the queue readings are 8, 11 and 14. If those readings are later found to be batch updates rather than stage transitions, the queue evidence must be rechecked.

The worksheet also does not establish a funded roadmap-row verdict because HC37 supplies no funded roadmap rows. It names the BUILD constraint and records the throughput arithmetic, but it does not claim that any particular roadmap item should be kept, re-aimed or parked.

Finally, the QA rule must expire when the constraint moves. A buffer of 6 is a subordination rule for the current QA constraint, not a permanent release policy.

## Feeds

- [harbourgate-journey.md](harbourgate-journey.md), the Harbourgate journey and canonical data sheet
- [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), HC1 to HC8 and HC37
- Gate 4 attempt 1, NOT MET on 2026-06-03
- FS-2 and FS-5 exercises on 2026-06-08
- Gate 4 attempt 2, MET on 2026-06-09

**Exit-gate walk:** Tomasz Wierzbicki confirms that QA verification was identified as the constraint with evidence 3 of 3, the 30% reclaim was calculated as 12 hours per week, starts were subordinated to a buffer of 6, the building engineer option was selected at `0.05` engineer-years per added item per week against `0.333...` for the contract option, FS-2 and FS-5 were exercised on 2026-06-08, and code review at 9 items per week was named as the next constraint. **Signed:** Tomasz Wierzbicki and Noor Haddad, 2026-06-04.
