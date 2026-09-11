# WSJF and Cost of Delay: Ledgerline Add-on Short List

Fills [frameworks/prioritization/wsjf-cost-of-delay.md](../frameworks/prioritization/wsjf-cost-of-delay.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its backlog and every score are fiction built to show the worksheet method, not to suggest a benchmark or target.

**Owner:** Maya Chen, Product Manager · **Scored with:** Priya Nair, Engineering Lead · **Date:** 2026-12-23

## What it is for

This worksheet sequences Ledgerline's add-on short list after the 2026-12-23 backlog triage. It orders work that is already in scope, rather than deciding whether the add-on should exist.

The short list uses WSJF, weighted shortest job first. Cost of delay is the sum of value, time criticality, and risk reduction or opportunity enablement. WSJF divides that sum by duration in weeks of team time.

The meter, BL-01, leads on time criticality because DEP4, the usage meter, is needed before EXP-2 can open. German extraction, BL-02, remains near the bottom while R3 is open and EVAL-3 is below its 90% threshold.

## Run it when

- A ranked list has survived earlier product decisions and needs a delivery sequence.
- Several add-on backlog items compete for the same Q1 2027 capacity.
- Work has different levels of urgency, enablement value and duration.
- A large item may produce a better sequence if it is split into a thinner slice.

**Skip it when:** the question is whether an item should be built at all. This sheet assumes the scored short list is eligible for sequencing. BL-06 and BL-08 are not scored because the triage record leaves them parked or not yet on the short list.

## Inputs you need first

- The add-on backlog register, including BL-01 to BL-08, from the 2026-12-23 triage.
- Duration in weeks of team time for each scored item.
- The delivery dependency and experiment context, including DEP4 and EXP-2.
- Open risks and dictionary gaps, including R3, G-1, G-2 and G-3.
- The short-list scores in the supplementary data sheet, LC42 and LC43, which records the scoring by Maya Chen with Priya Nair.
- The price-hold context for the 73 paid accounts, N93, where it affects enablement value for BL-07.

See the [journey data sheet](ledgerline-journey.md) and its [coverage sheet](ledgerline-coverage-sheet.md).

## The worksheet

### Step 1: score cost of delay, one column at a time

Cost of delay uses the relative scale 1, 2, 3, 5, 8, 13, 20. The team scored every item in one component before moving to the next component.

| Component | Question it answers | Column scoring notes |
|---|---|---|
| User or business value | How much does this move the period's metric or a customer's outcome, relative to the others? | BL-01 scores 13 because the running cost and per-drafted-report billing are needed for EXP-2. BL-05 scores 8 because it addresses a customer filer problem. BL-03 scores 1 because it improves measurement coverage rather than the core customer outcome. |
| Time criticality | How fast does the value decay? Is there a fixed date after which it is worth much less? Does waiting change what has to be built? | BL-01 scores 20 because DEP4 is needed before EXP-2 can open. The other scored items are 1 or 2. BL-02 scores 2 while German extraction remains below the EVAL-3 threshold. |
| Risk reduction or opportunity enablement | What risk does this retire, or what future work does it unlock, that the others do not? | BL-04 scores 5 because it closes the G-2 draft-id gap. BL-02 scores 5 because it addresses R3 and G-3. BL-01 scores 8 because it enables EXP-2. |

The column order was:

1. User or business value across BL-01, BL-03, BL-04, BL-07, BL-02 and BL-05.
2. Time criticality across the same six items.
3. Risk reduction or opportunity enablement across the same six items.
4. Duration was then recorded in weeks of team time.

The scores are relative to this sheet only. They are not compared with the RICE scores or with another team's scale.

### Step 2: divide by duration

For every row:

**CoD = value + time criticality + risk or enablement**

**WSJF = CoD / duration**

| # | Item | Value | Time criticality | Risk or enablement | CoD (sum) | Duration | Arithmetic | WSJF |
|---|---|---:|---:|---:|---:|---:|---|---:|
| 1 | BL-01, bill per drafted report and show the running cost, DEP4 and LEDGERLINE-S6 | 13 | 20 | 8 | 41 | 4 weeks | 13 + 20 + 8 = 41; 41 / 4 | 10.25 |
| 2 | BL-03, fix the G-1 legacy annual-invoice activation-event gap | 1 | 1 | 3 | 5 | 1 week | 1 + 1 + 3 = 5; 5 / 1 | 5.0 |
| 3 | BL-04, fix the G-2 classic-approvals events with no draft id | 3 | 1 | 5 | 9 | 3 weeks | 3 + 1 + 5 = 9; 9 / 3 | 3.0 |
| 4 | BL-07, create a path to move the 73 held accounts to a successor price | 5 | 1 | 3 | 9 | 4 weeks | 5 + 1 + 3 = 9; 9 / 4 | 2.25 |
| 5 | BL-02, improve German-language receipt extraction, R3 and G-3 | 5 | 2 | 5 | 12 | 6 weeks | 5 + 2 + 5 = 12; 12 / 6 | 2.0 |
| 6 | BL-05, warn the filer about the top pre-submit bounce cause | 8 | 2 | 1 | 11 | 8 weeks | 8 + 2 + 1 = 11; 11 / 8 | 1.4 |

**Sequence before the split:**

1. BL-01, 10.25
2. BL-03, 5.0
3. BL-04, 3.0
4. BL-07, 2.25
5. BL-02, 2.0
6. BL-05, 1.4

BL-06 and BL-08 are left off the short list because the triage record marks BL-06 parked to 2027-02-12 and leaves BL-08 not yet on the short list. No WSJF arithmetic is assigned to either item.

### Step 3: the split test

BL-05 is the largest scored item at 8 weeks. The thinnest useful slice is to warn the filer about the single top bounce cause before submission, rather than build the full pre-submit check.

Value reduced because full pre-submit check addresses multiple causes; slice addresses only the top one.

| Large item | Slice | Slice CoD | Slice duration | Slice WSJF |
|---|---|---:|---:|---:|
| BL-05, pre-submit check | Warn the filer about the single top bounce cause only | 8 | 3 weeks | 5 + 2 + 1 = 8; 8 / 3 = 2.7 |

The slice changes the order:

1. BL-01, 10.25
2. BL-03, 5.0
3. BL-04, 3.0
4. BL-05 slice, 2.7
5. BL-07, 2.25
6. BL-02, 2.0
7. The rest of BL-05, after the slice

The split moves the one-cause pre-submit check above migration tooling, BL-07. It does not move the full BL-05 item above BL-07.

## The relative-scale warning

The scores mean nothing outside this sheet. A 13 here is not a 13 on another team's sheet, and the WSJF values must not be compared or added across teams or quarters.

The scale compresses extremes. It is a sequencing aid, not a claim that BL-01 is a measurable multiple of BL-03. Duration is expressed in weeks of team time for every scored item, so the denominator is consistent across the sheet.

When value can be stated as money per week with a real duration, that arithmetic can replace the relative scale. This sheet does not replace the recorded relative scores in LC42 or LC43.

## Reading the result

The sequence after the split is:

1. **BL-01**, the usage meter, WSJF 10.25. Its time criticality is 20 because DEP4 blocks EXP-2.
2. **BL-03**, the G-1 activation-event fix, WSJF 5.0.
3. **BL-04**, the G-2 draft-id fix, WSJF 3.0.
4. **BL-05 slice**, the single-cause pre-submit warning, WSJF 2.7.
5. **BL-07**, the successor-price path for the 73 held accounts, WSJF 2.25.
6. **BL-02**, German extraction, WSJF 2.0.
7. **The rest of BL-05**, WSJF 1.4 at its full 8-week duration.

BL-02 remains near the bottom until its evaluation clears. EVAL-3 contains 300 labeled receipts, and its field accuracy is 71% against the 90% eval threshold. The Q1 planning record uses 90% as the promotion signal for German-language extraction.

BL-01 is first because it enables EXP-2, whose planned exposure cannot start before DEP4 lands. BL-03 and BL-04 follow because they close known measurement gaps, G-1 and G-2. BL-07 matters for the 73 held accounts and their 12-month price hold, but it does not unblock EXP-2. The one-cause BL-05 slice beats BL-07 because its 3-week duration is shorter than BL-07's 4 weeks.

Re-score if a duration changes, DEP4 moves, the EXP-2 date moves, the R3 evaluation clears, or the 73-account price-hold decision changes.

## ILLUSTRATIVE example

Ledgerline's fictional add-on short list was scored on 2026-12-23. The figures below are ILLUSTRATIVE and come from LC42 and LC43 of the [coverage sheet](ledgerline-coverage-sheet.md).

| # | Item | Value | Time | Risk | CoD | Duration | Arithmetic | WSJF |
|---|---|---:|---:|---:|---:|---:|---|---:|
| 1 | BL-01, drafted-report meter for EXP-2 | 13 | 20 | 8 | 41 | 4 | 13 + 20 + 8 = 41; 41 / 4 | 10.25 |
| 2 | BL-03, legacy annual-invoice activation event | 1 | 1 | 3 | 5 | 1 | 1 + 1 + 3 = 5; 5 / 1 | 5.0 |
| 3 | BL-04, classic-approvals draft-id coverage | 3 | 1 | 5 | 9 | 3 | 3 + 1 + 5 = 9; 9 / 3 | 3.0 |
| 4 | BL-07, successor-price path for held accounts | 5 | 1 | 3 | 9 | 4 | 5 + 1 + 3 = 9; 9 / 4 | 2.25 |
| 5 | BL-02, German-language extraction | 5 | 2 | 5 | 12 | 6 | 5 + 2 + 5 = 12; 12 / 6 | 2.0 |
| 6 | BL-05, full pre-submit check | 8 | 2 | 1 | 11 | 8 | 8 + 2 + 1 = 11; 11 / 8 | 1.4 |

The split test changes the fourth row:

| Large item | Slice | CoD | Duration | WSJF |
|---|---|---:|---:|---:|
| BL-05 | Warn the filer about the single top bounce cause only | 5 + 2 + 1 = 8 | 3 weeks | 8 / 3 = 2.7 |

The resulting order is BL-01, BL-03, BL-04, the BL-05 slice, BL-07, BL-02, then the rest of BL-05.

## The trap

The first trap is scoring by item instead of by column. If the BL-01 sponsor gives it 20 for value, time criticality and risk, then another sponsor can do the same for BL-02. CoD becomes a record of who argued most strongly rather than a relative comparison. Maya Chen and Priya Nair avoided that by scoring the whole value column, then the whole time-criticality column, then the whole risk or enablement column.

The second trap is treating duration as a lever to game. BL-05 has a CoD of 11, but its 8-week duration produces:

**11 / 8 = 1.4**

The slice has a CoD of 8 and a 3-week duration, producing:

**8 / 3 = 2.7**

That result is useful only because the slice is a real thinner delivery unit, not because its duration was reduced to improve the score.

The third trap is ignoring dependencies. BL-01 would not lead on time criticality without DEP4 and EXP-2. Its score of 20 records that the value decays through a blocked experiment, rather than treating the meter as ordinary backlog cleanup.

## Feeds

- [ledgerline-journey.md](ledgerline-journey.md): DEP4, EXP-2, G-1 to G-3, R3, N93 and the shared identifiers.
- [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): LC40, LC42 and LC43, including the backlog triage, the column scores, the durations and the split arithmetic.
- [Ledgerline backlog example](ledgerline-backlog.md): the add-on queue, intake state and active-item context.
- [Now, Next, Later example](ledgerline-now-next-later.md): the Q1 2027 consequence of this sequence.
- [Growth plan example](ledgerline-growth-plan.md): EXP-2, which BL-01 enables.
- The sequencing step of the roadmap builder, on the PLANNING track of the operating loop.
- Method background: based on the ideas of Donald Reinertsen, from The Principles of Product Development Flow (2009), in the form popularized by the Scaled Agile Framework. See also the WSJF entry in the [knowledge index](../knowledge/INDEX.md).
