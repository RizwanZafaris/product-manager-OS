---
layer: frameworks
stage: BUILD
gate: 4
feeds: ["templates/discovery/usability-test-plan.md", "frameworks/metrics/heart-metrics.md", "templates/operate/metrics-dictionary.md"]
method: "knowledge/design/ux-measurement.md"
aliases: ["UX Scorecard", "ux-scorecard"]
---
# UX Scorecard

Based on the ideas of John Brooke's System Usability Scale, from *Usability Evaluation in Industry* (1996); James R. Lewis, Brian S. Utesch and Deborah E. Maher's UMUX-LITE, from CHI 2013; and Alan Agresti and Brent A. Coull's adjusted Wald interval for a proportion, from *The American Statistician* (1998). Explained here in this repository's own words.

## What it is for

A round of usability testing produces six different numbers, and each one answers a different question. This worksheet is where they get scored, side by side, with the arithmetic written out so a second reviewer can check every figure without re-running the test. It produces: a task success rate with a confidence interval, a median time on task, an error count, a post-task ease rating, a System Usability Scale (SUS) score, and a UMUX-LITE score. Nothing here replaces [the usability test plan](../../templates/discovery/usability-test-plan.md), which decides what gets tested and with whom; this sheet is where the results of that plan get scored once the sessions are done.

## Run it when

- A round of moderated or unmoderated usability testing has just finished and the raw session notes need to become numbers a Gate 4 reviewer can check
- A before-and-after comparison is needed on a redesign, and the two rounds need to be scored the same way to be comparable at all
- A stakeholder wants a satisfaction number for an exec update, and the trap below needs a full scorecard standing behind whatever single figure is spoken aloud
- The happiness or task success rows in [the HEART worksheet](../../frameworks/metrics/heart-metrics.md) need a defined instrument rather than a guess

**Skip it when:** there are no defined tasks. Every number on this sheet either scores a task (success, time, errors, ease) or scores a session built around tasks (SUS, UMUX-LITE); with no defined task and no defined success state, there is nothing for any of the six numbers to be about, and running the arithmetic anyway produces figures that look precise and mean nothing.

## Inputs you need first

- A completed round from [the usability test plan](../../templates/discovery/usability-test-plan.md): tasks, participants, and each task's defined success state
- Raw session data: for each participant and task, whether it succeeded (unassisted or assisted), the time taken, the errors observed, and the post-task ease rating
- If a test-level questionnaire was run, the raw SUS or UMUX-LITE item responses for each participant, not a remembered summary
- The assistive-technology and right-to-left-locale status of each participant, so those segments can be scored and reported separately

## The worksheet

### 1. Task success

<!-- Report unassisted and assisted completions separately, never merged into
     one success count: an assisted completion says the task is learnable
     with help, not that it succeeds unaided. -->

**Success rate:** unassisted successes divided by attempts, per task. Report the fraction (for example, 7 of 10) and the percentage.

**Confidence interval (adjusted Wald / Agresti-Coull method, cited by title, not fetched; no DOI on file):** for x successes out of n attempts, at the 95 percent level (z = 1.96):

```
n' = n + z^2
p' = (x + z^2 / 2) / n'
margin = z * sqrt( p' * (1 - p') / n' )
interval = [p' - margin, p' + margin], clipped to [0, 1]
```

**n below 5: report the raw fraction only, no interval.** An interval computed on 3 or 4 attempts is arithmetic performed on a sample too small to support it; stating one invites false precision the round cannot back up.

| Task | Attempts (n) | Unassisted successes (x) | Success rate | 95% CI (adjusted Wald) |
|---|---|---|---|---|
| T1 | | | | |

### 2. Time on task and errors

**Time on task:** the median, not the mean, across participants who completed the task. Completion times are typically right-skewed, a few slow outliers pull a mean upward and make a product look worse than it read to most participants; the median is not moved by them.

**Errors:** count per task, recovered and unrecovered reported as separate columns. A recovered error the participant caught and fixed alone is a different finding from one that ended the task, and averaging them into one error count erases the difference.

| Task | Median time on task | Errors (recovered) | Errors (unrecovered) |
|---|---|---|---|
| T1 | | | |

### 3. Post-task ease

<!-- Ask immediately after each task, before debriefing, while the
     experience is still fresh. State the labels every time this item is
     used; no external benchmark number is attributed to it here, because
     the later MeasuringU naming and benchmark work for this style of item
     was not among the sources read for this sheet or its method card. -->

**Item, asked after every task:** "Overall, this task was:" on a 7-point scale, labeled 1 (Very difficult) to 7 (Very easy).

**Score:** the median rating per task, with n stated. No pass mark is attached to this number; read it against this product's own earlier rounds, never against a number recalled from somewhere else.

| Task | n | Median ease rating (1 to 7) |
|---|---|---|
| T1 | | |

### 4. System Usability Scale (SUS)

<!-- Ten items, alternating positive and negative tone, five-point agreement
     scale, asked once per participant after the whole session (not per
     task). The items themselves are linked to the primary source rather
     than reproduced here, per Brooke's own free-use-with-acknowledgement
     condition and this repository's one-quote-per-file limit, already
     spent below on UMUX-LITE. -->

**Instrument:** [Brooke's ten SUS items](https://digital.ahrq.gov/sites/default/files/docs/survey/systemusabilityscale%2528sus%2529_comp%255B1%255D.pdf), asked once per participant, immediately after the session and before debriefing. Every item gets a response; a participant who cannot answer one marks the scale's centre point rather than skipping it.

**Scoring, per respondent, standard, Brooke's own published procedure:**

```
Odd items (1, 3, 5, 7, 9):  contribution = scale position - 1   (range 0-4)
Even items (2, 4, 6, 8, 10): contribution = 5 - scale position   (range 0-4)
SUS score = sum of all ten contributions * 2.5                   (range 0-100)
```

Individual item scores are not meaningful on their own, per Brooke; report only the composite per respondent.

**Roll-up:** the mean SUS score across respondents, with n stated beside it.

| Respondent | SUS score (0-100) |
|---|---|
| P1 | |

**Mean SUS:** `<value>` · **n:** `<count>`

### 5. UMUX-LITE

<!-- Two items only, seven-point scale, asked once per participant. The raw
     two-item score needs a regression adjustment before it is placed next
     to a SUS number; skipping that step is the second distortion named in
     the method card's "How it lies" section. -->

**Items, quoted with attribution because the paper offers them as the instrument itself (Lewis, Utesch and Maher, 2013):** "This system's capabilities meet my requirements" and "This system is easy to use." Each answered on a 7-point scale from 1 (Strongly disagree) to 7 (Strongly agree).

**Raw score, per respondent:**

```
UMUX(1,3) = ( (item1 - 1) + (item2 - 1) ) * 100 / 12          (range 0-100)
```

**Regression adjustment, research evidence, coefficients from the fetched CHI 2013 paper, page 2101, computed on the authors' combined sample of n = 791:**

```
UMUX-LITE = 0.65 * UMUX(1,3) + 22.9
```

Applying this adjustment is not optional: the paper found raw UMUX-LITE means run slightly below SUS means for the same system, and comparing the unadjusted number against a SUS benchmark understates the product.

**Roll-up:** the mean adjusted UMUX-LITE score across respondents, with n stated beside it.

| Respondent | item1 | item2 | UMUX(1,3) | UMUX-LITE (adjusted) |
|---|---|---|---|---|
| P1 | | | | |

**Mean UMUX-LITE:** `<value>` · **n:** `<count>`

## Reading the result

Read the six numbers in this order, not alphabetically and not in the order they were collected: **task success first, satisfaction last.** A product can be rated pleasant to have used and still be genuinely hard to use, per the aesthetic-usability effect and the peak-end rule named in [the method card](../../knowledge/design/ux-measurement.md); task success, time on task and errors are observed, not remembered, and do not carry that bias. A high SUS or UMUX-LITE score does not offset a low task success rate; it explains why nobody in the room complained about it.

A SUS mean of 68 (standard deviation about 12.5) is the historical, pooled average across studies, standard, not a pass mark. Read this round's mean against a domain-matched baseline where one exists (a meta-analysis of digital health apps found a mean of 76.64, research evidence from Hyzy et al., 2022); with no domain baseline on file, report the number with its n and say plainly that no baseline was available, rather than implying 68 is a target this product should clear.

Report assistive-technology users and right-to-left-locale participants as their own rows or their own sub-table in every one of the six sections, never folded into the aggregate. An aggregate that looks healthy can be hiding a screen-reader flow that fails on every attempt; averaging across a segment that experiences a materially different product erases the one signal that would have caught it.

n below 5 on any of the six numbers: report the raw figures (fraction, median, count) and state the sample size plainly; do not compute or state a confidence interval, and treat a SUS or UMUX-LITE mean from fewer than 5 respondents as a pilot reading, not a scored round.

## ILLUSTRATIVE example

Invented, unrelated to any journey product in this repository: a delivery-status screen for a fictional last-mile courier app, "Bramwell Freight." Task: "find out whether today's delivery window has changed." 8 participants, one using a screen reader.

**Task success:** 6 of 8 unassisted successes. n = 8, x = 6. z = 1.96, z^2 = 3.8416.
`n' = 8 + 3.8416 = 11.8416`
`p' = (6 + 1.9208) / 11.8416 = 0.669`
`margin = 1.96 * sqrt(0.669 * 0.331 / 11.8416) = 1.96 * 0.1367 = 0.268`
`interval = [0.401, 0.937]`, reported as 75 percent (6 of 8), 95% CI [0.40, 0.94].

**Screen-reader segment (n = 1):** 0 of 1 succeeded unassisted. Reported as a raw fraction only, no interval: this is the one number in the round that the aggregate above does not show, and it is the one the team acts on first.

**Time on task:** median 48 seconds (sighted participants); the screen-reader participant abandoned the task at 4 minutes.

**Errors:** 2 recovered (misread the window as a delivery date), 1 unrecovered (the screen-reader participant, who could not locate the updated time at all).

**Post-task ease:** median 5 of 7 (sighted participants, n = 7).

**Mean SUS:** 71.5, n = 8.

**Mean UMUX-LITE:** raw UMUX(1,3) mean 68.2, adjusted: 0.65 * 68.2 + 22.9 = 67.2, n = 8.

Reading it: task success first. The aggregate 75 percent and the SUS of 71.5 would read as a comfortably passing round on their own. The screen-reader segment, reported separately per the rule above, shows a complete failure on the one task that mattered, which the aggregate hides. The scorecard's finding is not "71.5, ship it"; it is "sighted users found the change, one assistive-technology user could not find it at all, fix that before this round counts as passed."

## The trap

A single score in an exec update. "SUS was 71" or "UMUX-LITE came in at 67" spoken alone, with no task success rate beside it and no n attached, sounds like evidence and is a satisfaction number standing in for a question it cannot answer: whether people could actually do the thing. The fix is not a longer sentence, it is the order in the "Reading the result" section above, said in that order every time: task success first, with its n and interval or its raw fraction, then time and errors, then the satisfaction numbers last, each with its own n. A scorecard that reports only the last two rows and calls it done has produced the trap, not the worksheet.

## Feeds

- [Usability Test Plan](../../templates/discovery/usability-test-plan.md): sections 6 through 8 draw success criteria and severity from this sheet's task success, time and error rows
- [HEART metrics worksheet](../../frameworks/metrics/heart-metrics.md): this sheet's SUS or UMUX-LITE mean is the attitude instrument the happiness row requires; its task success rate feeds the task success row
- [Metrics Dictionary](../../templates/operate/metrics-dictionary.md): once a metric from this sheet is tracked on an ongoing basis, it gets a precise, checkable definition there
- BUILD, feeding [Gate 4: acceptance criteria met](../../os/STAGE-GATES.md)
- Method background: [UX Measurement](../../knowledge/design/ux-measurement.md)
