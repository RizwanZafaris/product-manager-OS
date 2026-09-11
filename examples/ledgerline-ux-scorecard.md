# UX Scorecard: Expense Copilot add-on, design-partner usability round

Fills [frameworks/design/ux-scorecard.md](../frameworks/design/ux-scorecard.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional product used across this repository, the design partners (N41) are invented firms, the participants, session times, ratings, SUS items and UMUX-LITE responses are ILLUSTRATIVE, built to show the six numbers and their arithmetic and not to be copied as a target or quoted as a benchmark. No number below is an external benchmark; the only external reference is the pooled SUS average named in the blank's "Reading the result" section, cited there with its own uncertainty. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-11-21 · **Round:** moderated, five finance reviewers (LD5, S-2 / N41), sessions 2026-11-17 to 2026-11-19, tasks T1 and T2 · **Facilitator:** Hana Sato · **Note-taker:** Kwame Boateng

Every number below either comes from the [journey data sheet](ledgerline-journey.md) (rows N1 to N94, cited by row) or the [design sheet](ledgerline-design-sheet.md) (rows LD5 to LD16); nothing contradicts either. The round was drawn from four of the six N41 design partners after phase 1 went live (N43) and before the EXP-1 pricing experiment opened (N56); no reviewer had yet seen the per-seat price screen in anger, since phase 1 billed no design partner (N42).

## What it is for

Four of the six design partners have been live on the add-on since 2026-11-10 (N41, N43). This worksheet is where the raw notes from a single moderated round, five reviewers, two tasks, become the six numbers a Gate 4 reviewer can check line by line, with every division written out. No earlier round of this product exists to compare against; the blank's rule is read against this product's own rounds, and this is round one.

## Run it when

- This round qualifies on the first two conditions: a round of moderated testing has just finished and the session notes need to become Gate 4 numbers, and the same scoring (same two tasks, same items) is what a before-and-after re-run on the pivot's usage meter (D7, DEP4) would need to be comparable.
- It also feeds the condition named in the blank's inputs: the happiness and task-success rows of [the HEART worksheet](../frameworks/metrics/heart-metrics.md) need a defined instrument behind them rather than a remembered impression.

**Skipped when** there is no defined task. The two tasks here each have a written success state (below), which is what makes all six numbers possible; run the same scoring on a free-play session and every figure would be arithmetic on noise.

## Inputs you need first

- A completed round from [the usability test plan](../templates/discovery/usability-test-plan.md): T1 and T2, five participants, and a written success state per task: T1, the filer reviews a drafted line item with a flagged field and confirms or corrects it (LEDGERLINE-S3); T2, the account admin activates the add-on and sees the billed per-seat charge before confirming (LEDGERLINE-S1).
- Raw session data per participant and task: whether the task was unassisted or assisted, the wall-clock time, the errors observed (recovered and unrecovered split), and the post-task ease rating.
- The raw ten-item SUS responses and the raw two-item UMUX-LITE responses for each participant, captured on the form, not a remembered summary.
- Assistive-technology status per participant: four reviewers filed without assistive technology, one each from Bramblewood Freight, Tessellate Consulting, Marlowe Field Services and Corrigan and Vale; the fifth, a second reviewer from Tessellate Consulting, used a screen reader (LD5). No non-English-locale participant was in this round; that segment row is recorded as "none in this round", which is a sample limit, not an absence of the risk.

## The worksheet

### 1. Task success

Reported unassisted and assisted separately, never merged: an assisted completion says the task is learnable with help, not that it succeeds unaided. n = 5 for T1, which sits at the blank's n of 5 floor and carries an adjusted Wald (Agresti-Coull) interval at the 95 percent level, z = 1.96, z^2 = 3.8416, z^2 / 2 = 1.9208. The screen-reader participant's result is reported as a raw fraction only, below the n = 5 floor.

| Task | Attempts (n) | Unassisted successes (x) | Success rate | 95% CI (adjusted Wald) |
|---|---|---|---|---|
| T1 | 5 | 4 | 80% (4 of 5) | [0.36, 0.98] |
| T2 | 5 | 5 | 100% (5 of 5) | not computed, ceiling result; see the trap below |

The screen-reader participant did not complete T1 unassisted, reported separately as 0 of 1 (LD8), never folded into the T1 row above: the participant could not locate the confidence flag with the screen reader, a failure field accuracy data (N21, N24) never surfaces. The arithmetic for T1 (LD7): `n' = 5 + 3.8416 = 8.8416`; `p' = (4 + 1.9208) / 8.8416 = 0.669`; `margin = 1.96 * sqrt(0.669 * 0.331 / 8.8416) = 0.310`; `interval = [0.359, 0.979]`, reported rounded to [0.36, 0.98].

### 2. Time on task and errors

The median, not the mean, across participants who completed the task (completion times are right-skewed; a slow outlier must not pull the figure up). Times below are session wall-clock from task prompt to the success state (LD9, LD10), ILLUSTRATIVE; they are not a re-measurement of N23, the internal median filing time, and are not claimed as its add-on replacement.

| Task | Median time on task | Errors (recovered) | Errors (unrecovered) |
|---|---|---|---|
| T1 | 74 s (sighted, n = 4) | 1 | 1 |
| T2 | 38 s (n = 5) | 1 | 0 |

T1's one recovered error was a sighted reviewer misreading a flagged amount as already corrected; the one unrecovered error is the screen-reader participant, who could not locate the confidence flag and abandoned the task rather than submit a wrong draft. T2's one recovered error was a reviewer opening the wrong settings tab first, then finding the correct one. Averaging recovered and unrecovered into one count would erase the difference between a participant who caught and fixed a mistake and one who could not fix it and stopped, which is why they are two columns.

### 3. Post-task ease

Asked immediately after each task, before debriefing, on a 7-point scale labelled 1 (Very difficult) to 7 (Very easy), item "Overall, this task was:". Median rating per task with n stated (LD11); no pass mark attached, because no external benchmark is attributed to this item and there is no earlier round of this product to compare it against.

| Task | n | Median ease rating (1 to 7) |
|---|---|---|
| T1 | 4 (sighted) | 5 |
| T2 | 5 | 6 |

T1's n is 4, not 5: the screen-reader participant's ease rating for an abandoned task is not folded into a sighted-task median, consistent with the segment rule below.

### 4. System Usability Scale (SUS)

Instrument: [Brooke's ten SUS items](https://digital.ahrq.gov/sites/default/files/docs/survey/systemusabilityscale%2528sus%2529_comp%255B1%255D.pdf), asked once per participant after the whole session and before debriefing, every item answered (a participant who cannot answer marks the centre point rather than skipping). Scored by Brooke's published procedure, odd items (1, 3, 5, 7, 9) contribute `scale position - 1` (0 to 4), even items (2, 4, 6, 8, 10) contribute `5 - scale position` (0 to 4), sum times 2.5, range 0 to 100. Individual item scores are not meaningful on their own, per Brooke; only the composite is reported.

| Respondent | Raw items (odd 1,3,5,7,9; even 2,4,6,8,10) | SUS score (0-100) |
|---|---|---|
| R1 | 4,2,4,2,4,2,4,1,4,2 | 77.5 |
| R2 | 3,3,4,2,3,2,3,3,3,2 | 60.0 |
| R3 (screen reader) | 2,4,2,4,1,4,2,5,2,5 | 17.5 |
| R4 | 4,2,3,2,4,1,4,2,3,2 | 72.5 |
| R5 | 3,2,4,3,3,2,4,2,4,3 | 65.0 |

**Mean SUS:** 58.5 · **n:** 5, reported with R3's 17.5 shown separately, never folded into a single mean that hides it (LD12, LD13).

Worked for R1 (odd items: 4, 4, 4, 4, 4, summing 20; even items: 2, 2, 2, 1, 2, summing 9): odd contributions `20 - 5 = 15`; even contributions `25 - 9 = 16`; sum `15 + 16 = 31`; `31 * 2.5 = 77.5`, matching the score logged above; the other four composites are the session log's figures under the same procedure. The mean is `(77.5 + 60.0 + 17.5 + 72.5 + 65.0) / 5 = 292.5 / 5 = 58.5`.

### 5. UMUX-LITE

Two items, quoted with attribution to the paper that is the instrument itself (Lewis, Utesch and Maher, 2013): "This system's capabilities meet my requirements" and "This system is easy to use.", each answered 1 (Strongly disagree) to 7 (Strongly agree). Raw score per respondent is `UMUX(1,3) = ((item1 - 1) + (item2 - 1)) * 100 / 12`, range 0 to 100, and the regression adjustment `UMUX-LITE = 0.65 * UMUX(1,3) + 22.9` (coefficients from the CHI 2013 paper, page 2101, computed on the authors' combined sample of n = 791) is applied, not optional, because the paper found raw two-item means run slightly below SUS means for the same system and comparing the unadjusted figure against a SUS number understates the product.

| Respondent | item1 | item2 | UMUX(1,3) | UMUX-LITE (adjusted) |
|---|---|---|---|---|
| R1 | 6 | 7 | 91.7 | 82.5 |
| R2 | 5 | 4 | 58.3 | 60.8 |
| R3 (screen reader) | 2 | 1 | 8.3 | 28.3 |
| R4 | 6 | 5 | 75.0 | 71.6 |
| R5 | 5 | 5 | 66.7 | 66.2 |

**Mean UMUX-LITE:** 61.9 · **n:** 5 (LD14, LD15)

Worked for R1: `UMUX(1,3) = ((6 - 1) + (7 - 1)) * 100 / 12 = (5 + 6) * 100 / 12 = 1100 / 12 = 91.7`; `UMUX-LITE = 0.65 * 91.7 + 22.9 = 59.6 + 22.9 = 82.5`. The mean of the five adjusted scores is `(82.5 + 60.8 + 28.3 + 71.6 + 66.2) / 5 = 309.4 / 5 = 61.9`.

## Reading the result

Read in the blank's order, task success first and satisfaction last, not in the order the data was collected. The observed numbers lead: T1 succeeds unassisted for 4 of 5 sighted reviewers, 80 percent, 95 percent adjusted-Wald interval [0.36, 0.98], which on its own reads like a workable rate; but the screen-reader participant's T1 result is a separate 0 of 1, reported as a raw fraction only, and that failure is what the 80 percent figure masks (LD16). T2 is a ceiling result, 5 of 5. Time on task (T1 median 74 s among sighted reviewers, T2 median 38 s) and the error split go next, still observed, with T1's one unrecovered error tied to the same screen-reader participant who could not locate the confidence flag. Satisfaction last: the SUS mean is 58.5 (n = 5) and the adjusted UMUX-LITE mean is 61.9 (n = 5), both below the SUS worksheet's cited pooled average of 68. The aesthetic-usability effect and the peak-end rule named in [the method card](../knowledge/design/ux-measurement.md) are exactly why satisfaction does not get to offset task success: the screen-reader participant's session (SUS 17.5, UMUX-LITE 28.3) sits far below the other four, and folding it into a single mean would have hidden the T1 failure rather than surfacing it.

Against a baseline, the blank's own honesty rule: the pooled SUS mean of 68, standard deviation about 12.5, across studies is a historical average, not a pass mark, and this document's method card does not hold a domain-matched baseline for finance filing software, so no such baseline is claimed here. So 58.5 is reported with its n = 5 and the statement that no domain-matched baseline was available, read as a signal to recheck T1's flagged-field pattern (LD16), not framed as a pass or fail on its own.

Segments carry their own rows, never folded in. Sighted reviewers (n = 4): T1 4 of 4 of the sighted attempts unassisted (4 of 5 overall once the screen-reader attempt is counted), median T1 time 74 s, one recovered error; SUS and UMUX-LITE means over R1, R2, R4 and R5 run higher than the pooled mean of 58.5 once R3 is set aside. The screen-reader participant (R3, n = 1, LD8): 0 of 1 unassisted on T1, one unrecovered error, SUS 17.5, adjusted UMUX-LITE 28.3. The pooled SUS of 58.5 is the one figure this round must not speak alone: it already sits below the historical average with the screen-reader segment folded in at n = 5, and reporting it without R3's separate row would understate how much of the gap is concentrated in a single failed session. n below 5 is honored where it bites: the screen-reader fraction (0 of 1) is reported as a raw count, no interval, no mean computed on the segment of one.

The one finding, in the blank's order, is not "SUS 58.5, needs work generally." It is: T1, reviewing a flagged field, is where the product fails the screen-reader segment outright while the sighted majority gets through it, and the satisfaction numbers, both below the historical pooled average even before R3 is isolated, are the signal to recheck the flagged-field pattern (LD16) rather than a verdict on the round as a whole.

## The trap

The trap the blank names is the single number in an exec update: "SUS was 58" spoken with no task success rate beside it and no n attached, or worse, T2's ceiling result quoted alone to imply the whole round passed. The fix is the order, every time: task success first, T1 4 of 5 (n = 5), 95 percent interval [0.36, 0.98], with the screen-reader participant's separate 0 of 1 named; then time and the error split, with the unrecovered one tied to its segment; then satisfaction last, each with its own n, SUS 58.5 (n = 5) and adjusted UMUX-LITE 61.9 (n = 5), with no baseline claimed and the R3 row separate. A scorecard that reports only the SUS and UMUX-LITE lines and calls it done has produced the trap, not the worksheet, and in this round it would have hidden the screen-reader failure entirely.

## Feeds

- [templates/discovery/usability-test-plan.md](../templates/discovery/usability-test-plan.md): this sheet's task success, time and error rows become the plan's success criteria and severity, sections 6 to 8
- [frameworks/metrics/heart-metrics.md](../frameworks/metrics/heart-metrics.md): the adjusted UMUX-LITE mean of 61.9 (n = 5) is the attitude instrument behind the happiness row; T1's 4 of 5 task success feeds the task-success row
- [templates/operate/metrics-dictionary.md](../templates/operate/metrics-dictionary.md): any of the six numbers tracked on an ongoing basis (for example post-task ease, or a SUS read run per re-test) gets its precise, checkable definition there
- BUILD, feeding Gate 4 (acceptance criteria met) in [os/STAGE-GATES.md](../os/STAGE-GATES.md); this round's T1 finding is the usability evidence the [design critique](ledgerline-design-critique.md) routed here (LD23)
- Method background: [knowledge/design/ux-measurement.md](../knowledge/design/ux-measurement.md)

## Exit gate, Gate 4: acceptance criteria met

Walk of this scorecard against the six numbers and the segment rule, signed by a named person.

- All six numbers present, with the arithmetic written out so a reviewer can check without re-running the session: task success (fraction, rate, adjusted-Wald interval per task), median time on task, the recovered and unrecovered error split, median post-task ease, per-respondent SUS with its mean, and per-respondent UMUX(1,3) with its adjusted mean. PASS.
- Every number traced: session-derived figures labelled ILLUSTRATIVE; assistive-technology segment tied to LD5 and LD8; no number contradicts the [journey data sheet](ledgerline-journey.md) or the [design sheet](ledgerline-design-sheet.md); N23 not re-quoted as this add-on's time figure. PASS.
- Segment rule honored: the screen-reader participant scored and reported as a separate row, no non-English-locale participant in this round recorded honestly as a sample limit, no interval or mean computed on the segment of one, raw counts only. PASS.
- Satisfaction numbers never used to offset a task-success rate; the SUS read against an honest "no domain-matched baseline on file," not 68 as a target. PASS.

Exit-gate walk verified and signed: **Maya Chen**, Product Manager, Expense Copilot, 2026-11-21 (n = 5, round 1; the flagged-field pattern this round surfaces routes into the next design critique or usability re-run).
