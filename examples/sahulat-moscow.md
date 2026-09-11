# MoSCoW prioritization: Sahulat Bill Pay

Fills [frameworks/prioritization/moscow.md](../frameworks/prioritization/moscow.md). Everything here is invented: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, chosen so that this worksheet agrees with the [Sahulat journey](sahulat-journey.md) and its [coverage sheet](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-05-20 · **Status:** Returned explicitly to Gate 2 for D5

## What it is for

This sheet negotiates the Sahulat Rel-1 scope against the fixed Gate 4 date of 2026-06-10. It runs MoSCoW, based on the ideas of Dai Clegg from his rapid application development work at Oracle, published in Case Method Fast-Track (1994) and later adopted by the DSDM method. Gate 4 is the fixed date because it is the agreed verification point for the release contract. The BUILD capacity is 28 engineer-weeks, of which 16 had been spent by 2026-05-20:

- 28 engineer-weeks total capacity, from N8.
- 16 engineer-weeks spent, from the sprint log.
- 28 - 16 = 12 engineer-weeks remaining.
- The remaining must slice is 7 engineer-weeks without Mehran Water.
- 7 / 12 = 0.5833, or 58 percent, under the 60 percent cap.
- Mehran Water needs 4 more engineer-weeks.
- With water, the must slice is 7 + 4 = 11 engineer-weeks.
- 11 / 12 = 0.9167, or 92 percent, over the 60 percent cap.

The balance-first work is a Should slice of 3 engineer-weeks. Cutting a Should does not reduce the Must slice, so it cannot rescue the water option on its own:

- The Must slice with water is 7 + 4 = 11 engineer-weeks, whether or not the balance-first Should slice ships.
- The Must cap is 60 percent of the 12 remaining engineer-weeks, which is 7.2 engineer-weeks.
- 11 is over 7.2 either way. Cutting the Should slice frees up total capacity, not Must effort.

Mehran Water therefore becomes Won't (this time), with D5's revisit condition: revisit when a new Mehran Water reference-validation test passes. The later Gate 4 record notes that the must slice overran by the resume half of AC-8, the one Gate 4 miss.

## Run it when

- The release date is fixed at 2026-06-10 by the Gate 4 verification point.
- The candidate list is larger than the 12 engineer-weeks remaining.
- The Gate 2 scope included Mehran Water as SAHULAT-S7, but 3 of 10 Mehran Water test bills failed reference validation on 2026-05-19.
- D5 requires the scope change to return explicitly to Gate 2 rather than being absorbed quietly into BUILD.
- The team needs a written Won't for Mehran Water so the 6 post-launch tickets asking for water bills do not re-open the release during this timebox.

**Skip it when:** the date is not fixed. That is not the case here. Gate 4's date is fixed at 2026-06-10.

## Inputs you need first

- **Fixed date:** Gate 4 on 2026-06-10.
- **Capacity:** N8 gives 4 engineers x 7 weeks = 28 engineer-weeks, plus 1 QA and the PM. The sprint log records 16 engineer-weeks spent by 2026-05-20, leaving 12.
- **Candidate effort:** the sprint log gives engineer-weeks per slice, not per-story sizes:
  - Remaining must slice: 7 engineer-weeks.
  - Balance-first slice, SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11: 3 engineer-weeks.
  - SAHULAT-S9: 1 engineer-week.
  - Unallocated contingency: 1 engineer-week.
  - Mehran Water reference fix: 4 engineer-weeks.
- **Release failure condition:** a Rel-1 requirement must be verified against the acceptance contract at Gate 4. The acceptance thresholds are N56, agreed at Gate 2 attempt 2. The Mehran Water validation (N58, 3 of 10 test bills failed on 2026-05-19) is the reason SAHULAT-S7 is killed by D5.
- **Decision owner:** Hira Baig owns the D5 scope decision. Zainab Qureshi owns the engineering estimate and the later AC-8 miss.
- **Source records:** [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

## The worksheet

### Step 1: the tests

| Label | Test question | Passes when |
|---|---|---|
| Must | If this is missing on 2026-06-10, do we ship? | No. It is required for the Rel-1 walking skeleton, safety path, or a bill-pay flow with no workable release-time alternative. |
| Should | What is the workaround for the first six weeks? | A workaround exists and is painful; dropping the item costs something measurable but not the release. |
| Could | What do we lose if this never ships? | Nothing measurable in the release contract. |
| Won't (this time) | Has the owner agreed in writing? | It is out of Rel-1, has a written revisit condition, and is not re-raised against the fixed date. |

### Step 2: classify

The effort column uses the sprint log's engineer-weeks per slice. It does not assign a size to an individual story.

| Item | Label | Test answer, why this label | Effort, engineer-weeks | Requested by | Agreed by |
|---|---|---|---:|---|---|
| Remaining Rel-1 must slice, including the lookup, payment, cash-in, Chenab Gas, dropped-session safety, duplicate protection and biller-posting paths | Must | Without this slice, the walking skeleton and the safety contract do not form a shippable Rel-1 release on 2026-06-10. | 7 | Hira Baig, product owner | Hira Baig |
| Balance-first slice, SAHULAT-S5, SAHULAT-S10 and SAHULAT-S11 | Should | Customers can still pay through the existing flow without saved references, the app flow or the reminder SMS. Dropping this slice is painful, but it does not fail the release. | 3 | Hira Baig, product owner | Hira Baig |
| Support lookup, SAHULAT-S9 | Should | The workaround is a slower support investigation. The payment can still complete without the first-call lookup. | 1 | Naveed Akhtar, customer support lead | Hira Baig |
| Unallocated contingency | Could | It is the first cut because it is not attached to a release requirement. Keeping it protects the fixed date if the timebox goes wrong. | 1 | Zainab Qureshi, engineering lead | Hira Baig |
| Mehran Water reference-validation fix, SAHULAT-S7 | Won't (this time) | 3 of 10 test bills failed reference validation on 2026-05-19. The Rel-1 release can ship without water, and adding the fix would make Musts exceed both the capacity and the 60 percent cap. Revisit when a new Mehran Water reference-validation test passes. | 4 | Hira Baig, product owner | Hira Baig, D5 |

The labels apply to slices, not to story-level estimates. SAHULAT-S7's identifier is spent and is not reused.

### Step 3: the cap check

Capacity remaining:

- 28 engineer-weeks total - 16 engineer-weeks spent = 12 engineer-weeks remaining.

Without Mehran Water:

| Label | Effort sum | Share of capacity | Cap | Pass? |
|---|---:|---:|---:|---|
| Must | 7 | 7 / 12 = 0.5833, or 58 percent | 60 percent | Yes |
| Should | 3 + 1 = 4 | 4 / 12 = 0.3333, or 33 percent | No separate cap | Yes |
| Could | 1 | 1 / 12 = 0.0833, or 8 percent | No separate cap | Yes |
| Total | 7 + 4 + 1 = 12 | 12 / 12 = 100 percent | At or under 100 percent | Yes |

With Mehran Water treated as a Must:

| Label | Effort sum | Share of capacity | Cap | Pass? |
|---|---:|---:|---:|---|
| Must | 7 + 4 = 11 | 11 / 12 = 0.9167, or 92 percent | 60 percent | No |
| Should | 3 + 1 = 4 | 4 / 12 = 0.3333, or 33 percent | No separate cap | No, because total scope is already 15 engineer-weeks |
| Could | 1 | 1 / 12 = 0.0833, or 8 percent | No separate cap | No, because total scope is already 16 engineer-weeks |
| Total | 11 + 4 + 1 = 16 | 16 / 12 = 1.3333, or 133 percent | At or under 100 percent | No |

The balance-first Should slice cannot save the water option:

- Must with water: 7 + 4 = 11 engineer-weeks. Cutting a Should slice does not reduce Must effort, so this figure does not change if the balance-first Should slice is cut.
- The Must cap is 60 percent of the 12 remaining engineer-weeks, which is 7.2 engineer-weeks.
- 11 is over the 7.2 engineer-week cap regardless of any Should or Could cut.
- Cutting the balance-first Should slice only reduces total candidate scope, from 16 to 13 engineer-weeks. It does nothing to the 11-engineer-week Must slice, which is the actual cap breach.

There are three valid moves when Musts exceed the cap: demote a Must, move the date, or add capacity that exists today. The date is fixed at 2026-06-10. No additional capacity exists in the N8 estimate. The evidence demotes Mehran Water to Won't (this time), rather than demoting the walking skeleton or moving Gate 4.

The must slice later overran by the resume half of AC-8. Gate 4 accepted that as its one miss on 2026-06-10. That later overrun confirms why the 60 percent contingency rule was needed, even though the initial no-water allocation was 58 percent.

### Step 4: the negotiation script

1. **"What happens on 2026-06-10 if this is missing?"**
   For the Rel-1 must slice, the walking skeleton or a safety path is incomplete, so the answer is that the release does not meet its agreed contract. For the balance-first slice and SAHULAT-S9, a workaround exists. For Mehran Water, the product can release with Ravi Power and Chenab Gas while water is excluded.

2. **"Which current Must comes out to make room?"**
   Adding Mehran Water would require 4 engineer-weeks. The current Must slice is 7 engineer-weeks, so water would make Musts 11 of 12, or 92 percent. No current Must can be removed without breaking the release contract.

3. **"What is the workaround for six weeks?"**
   For saved references, the app flow and the reminder SMS, customers can use the remaining Rel-1 lookup and pay flow without the balance-first additions. For support lookup, the support team can investigate through the existing operational path. For Mehran Water, customers can use another bill-payment route while the reference-validation problem is retested. The workaround is painful, but it does not make Gate 4 fail.

4. **"Shall we write it as a Won't for this release, with a revisit when a new Mehran Water reference-validation test passes?"**
   Yes. D5 records the explicit return to Gate 2, kills SAHULAT-S7, and keeps its identifier spent. The six tickets asking for water bills remain evidence for a later revisit, not a reason to break the 2026-06-10 timebox.

## Reading the result

Without Mehran Water, the plan uses all 12 remaining engineer-weeks:

- Musts: 7 / 12 = 58 percent, under the 60 percent cap.
- Shoulds: 4 / 12 = 33 percent.
- Could: 1 / 12 = 8 percent.
- Total: 12 / 12 = 100 percent.

The plan therefore holds only with the published cut order. The unallocated engineer-week is the first contingency cut, then the Should rows. The Must slice remains protected. It later overran by the resume half of AC-8, which Gate 4 recorded as its one miss.

With Mehran Water, the plan does not hold:

- Musts: 11 / 12 = 92 percent, over the 60 percent cap.
- Candidate scope: 16 / 12 = 133 percent, over remaining capacity.
- Cutting the 3 engineer-week balance-first Should slice does not change the Must slice: it stays at 11 / 12 = 92 percent, still over the cap, because cutting a Should reduces total scope, not Must effort.

Mehran Water is therefore a Won't (this time). The revisit condition is a new Mehran Water reference-validation test that passes. This is the scope decision behind D5 and the explicit return to Gate 2, not a quiet BUILD reclassification.

## ILLUSTRATIVE example

Sahulat's fixed Gate 4 date is 2026-06-10. Capacity remaining on 2026-05-20 is:

- 28 engineer-weeks total - 16 engineer-weeks spent = 12 engineer-weeks remaining.

The no-water plan is:

- Must slice: 7 engineer-weeks.
- Balance-first Should slice: 3 engineer-weeks.
- SAHULAT-S9 Should slice: 1 engineer-week.
- Unallocated contingency: 1 engineer-week.
- Total: 7 + 3 + 1 + 1 = 12 engineer-weeks.

The Must share is 7 / 12 = 58 percent, under the 60 percent cap.

Mehran Water needs 4 additional engineer-weeks:

- Must with water: 7 + 4 = 11 engineer-weeks.
- Must share with water: 11 / 12 = 92 percent.
- Candidate scope with water: 11 + 3 + 1 + 1 = 16 engineer-weeks.
- Capacity overrun: 16 - 12 = 4 engineer-weeks.

Removing the balance-first Should slice does not solve the cap breach:

- The Must slice with water stays at 7 + 4 = 11 engineer-weeks; cutting a Should does not reduce it.
- 11 / 12 = 92 percent.
- 92 percent is still above the 60 percent cap.

Mehran Water is written as Won't (this time), with a revisit when a new reference-validation test passes. SAHULAT-S7 is killed by D5 and its id is spent. The later Gate 4 miss is the resume half of AC-8, which overran the must slice after this worksheet was run.

## The trap

Treating the 3 engineer-week balance-first Should slice as a cut that helps the water option. It does not: cutting a Should reduces total scope, not Must effort, so the Must slice with water stays at 11 engineer-weeks, 92 percent of the 12 remaining, still above the 60 percent cap. It would also remove work tied to the balance-first hypothesis without making Mehran Water fit.

The other trap is treating the 4 engineer-week water fix as a small addition because the story is only one biller. The sprint log measures the slice, not the story label. The reference-validation fix consumes 4 of the 12 remaining engineer-weeks and changes the Must share from 58 percent to 92 percent.

The cap is what protects the fixed date when the must slice later overruns by the resume half of AC-8. Gate 4's accepted miss is evidence that the contingency was not decoration.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): N8, N54, N56, N58, D5, Gate 4 on 2026-06-10, SAHULAT-S7, AC-8 and the six post-launch water tickets.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): the MoSCoW slice figures from the sprint log, including the 7 engineer-week must slice, 3 engineer-week balance-first slice, 1 engineer-week SAHULAT-S9 slice, 1 unallocated engineer-week and 4 engineer-weeks for Mehran Water.
- Gate 2: the explicit return records the amended scope, the Won't decision and the spent SAHULAT-S7 identifier.
- Gate 4: the fixed date is 2026-06-10, and the resume half of AC-8 is recorded as the one miss.
- Decision D5: Mehran Water is removed from Rel-1 after the 3 of 10 reference-validation failures on 2026-05-19.

**Gate 2 return walk:** Hira Baig, Product Manager, signed the D5 scope return on 2026-05-21.
