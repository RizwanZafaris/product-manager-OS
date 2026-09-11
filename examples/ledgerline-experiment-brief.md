# Experiment Brief: EXP-1, Per-seat Pricing Offer

Fills [templates/operate/experiment-brief.md](../templates/operate/experiment-brief.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count and dollar figure is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so it can be checked against the documents this brief follows and precedes. See the [examples index](README.md).

**Owner:** Maya Chen, product manager · **Status:** decided · **Last updated:** 2026-12-22, appended after the growth plan (D7) to record the EXP-2 carry-forward population (N91) and the exit gate's link to the next bet

## 1. Hypothesis

- **We believe that** anchoring the $6-per-seat (N46) add-on price against a reviewer-cost figure (Ledgerline's own N7 estimate: 30 reviewer-hours a month, about $1,800), shown on the activation page alongside the plain offer
- **will move** M-007, offer-to-paid conversion within 14 days of first exposure, raising the anchored arm to at least 6.0% and above the plain arm by at least the 2.5-point minimum detectable effect (N55)
- **because** a buyer reads a monthly charge against a labour bill they already carry, not against a per-seat abstraction, so naming the labour bill should make the price legible as a saving rather than a new line item
- **Evidence this is worth testing:** 9 of 31 lost Business-plan deals in Q3 named receipt capture as the reason, 7 of those to the vendor Cinderwick (N37); five of six design-partner finance leads said they would pay "something" for the add-on but none of the six was asked a price (N40); the positioning document's D2 finding that a free feature cannot be positioned against an $8-a-seat vendor without announcing the value is zero. This evidence supports selling an add-on; none of it tests the anchor mechanism specifically. Zero of six design partners were asked a price (N40), and the anchor figure is Ledgerline's own internal estimate (N7), not evidence from a buyer.

D3 (2026-11-03) rejected per drafted report (no usage meter existed yet, DEP4) and per active filer (no definition of "active filer" was agreed) as the add-on's value metric, and set plan seats at $6 per seat per month instead, because billing already held each account's plan seat count and sales forecasts in seats; the add-on seat meter still had to be built (DEP1, N86). This brief tests how the seat price is presented, not which metric it should be.

## 2. Target metric and guardrail

| Field | Answer |
|---|---|
| Target metric | M-007, offer-to-paid conversion within 14 days of first exposure, share of exposed S-1 accounts |
| Tree link | M-007 is a diagnostic input to M-002, accounts with the add-on active, which is the input the north star metric M-001 (copilot-drafted reports approved on first submission, across customer accounts) depends on for account volume, per the metrics dictionary lineage |
| Baseline | 4.1%, a proxy measured on the prior add-on, Bills Automation (launched 2026-03-02), conversion of exposed accounts paid within 14 days (N39); it is a different product, so it is a proxy, not this add-on's own history. The control arm came in at 2.4%, 1.7 points under this proxy, so the proxy overstated this add-on's plain-offer conversion (see the decided outcome in section 5) |
| Minimum detectable effect we care about | 2.5 percentage points, a lift from the 4.1% baseline to at least 6.6% (N55) |
| Guardrail metric and floor | M-006, first-submission approval rate on drafted reports, must stay at or above 70% (N58) across converted accounts, the 73 paid accounts; M-008, reviewer-caught extraction errors per 100 drafted reports, must stay under 3 per 100 drafted reports (N58; the brief applies the same converted-accounts scope); M-010, support tickets per 100 add-on accounts per week, should not exceed 8 (N74). N65 and N67, the measured figures used in the decided outcome below, are reported across all 79 active add-on accounts, including the six S-2 design partners who were never exposed to EXP-1; no converted-only cut exists on the data sheet, so the check against this floor is approximate, not the pre-declared scope itself |

Note on the window: this brief's own predeclared clock (section 4, N56) always measured 14 days from each account's own first exposure, never from a page view. The 2026-12-19 change log entry (see [metrics dictionary, section 6](ledgerline-metrics-dictionary.md)) is a precision clarification (336 hours from first exposure) of the window already agreed on 2026-11-04 and pre-declared here; no value changed.

Note on the ship bar versus the sizing: 6.0% in section 5's ship rule is a business-viability bar, not itself the effect this experiment was sized to detect. Detecting a lift to exactly 6.0% (1.9 points above the 4.1% baseline) at two-sided 5%, 80% power needs roughly 2,080 accounts per arm by the same two-proportion method N55 used, more than the roughly 1,270 to 1,450 accounts per arm this experiment carried. This is a known limitation of this experiment's sizing against its own ship bar, not a condition the pre-declared Ship rule (N57) itself carries: clearing 6.0% without the full 2.5-point margin over control is a bar crossed without the statistical power to call it a supported difference, a gap the EXP-2 proposal in section 5 is meant to close.

Guardrails are checked continuously during exposure, not only at the analysis date: per the [GTM plan](ledgerline-gtm-plan.md)'s section 5 M-008 stop row, drafting pauses for the affected account or language (owner Priya Nair) if M-008 reaches 3 or more per 100 drafted reports before 2026-12-18; the N94 offer-page swap belongs to the GTM plan's EXP-1 kill-rule row, not to that stop condition.

## 3. Variants

| Variant | What the user experiences | Allocation |
|---|---|---|
| Control (S-3) | An S-1 account admin opens the in-app offer banner, on the add-on activation page in Expenses settings (LEDGERLINE-S1), and sees the plain offer: $6 per plan seat per month, no comparison line | 1,450 accounts by design (N54); 1,371 reached (N59) |
| A, anchored (S-4) | The same in-app offer banner, with one added line comparing the monthly charge to what the account's reviewers spend today on mechanical checks, using Ledgerline's own internal figure: 30 reviewer-hours a month across three reviewers, about $1,800 a month at a $60 hourly rate (estimate, N7, at an assumed rate, N6), as the stated comparison. No source on file records the banner's exact copy, so this describes what it compared, not a verbatim line. | 1,450 accounts by design (N54); 1,377 reached (N59) |

Assignment is by account id, split evenly within S-1, the 2,900 Business accounts active in Expenses with 10 or more reports last quarter (N32, N54). The anchor line quotes Ledgerline's own reviewer-cost figure rather than each buyer's own; that choice is not argued as a variant here because Ledgerline's own reviewer-cost figure (N7) was the comparison available at pricing sign-off (D3). WL-01 also objected to the figure itself, calling it Ledgerline's own number rather than the buyer's; with both arms under the kill line, the experiment cannot separate that objection from the seat-scaling cause named in the decided outcome below, and D6 did not act on it as a separate finding.

## 4. Sample size and duration

| Field | Answer |
|---|---|
| Sample needed | About 1,270 accounts per arm: two-proportion z-test, baseline 4.1% against a detectable 6.6% (4.1 plus the 2.5-point minimum detectable effect), two-sided alpha 0.05, 80% power, computed by Kwame Boateng and recorded as N55 |
| Expected duration | 12-day exposure window, plus a 14-day conversion window measured per account from its own first exposure, so accounts exposed on the last day are still being watched after exposure closes |
| Start / end dates | Exposure 2026-11-23 to 2026-12-04; per-account conversion window 14 days from first exposure; analysis 2026-12-18 (N56) |
| Unit of assignment | Account. Billing, seats and the offer itself are all account-level, and S-1's median account has 34 plan seats and 11 filers (N34), so a seat- or filer-level split would let one account see both variants |

Of the 2,900 designed exposures, 2,748 were actually reached during the window, 1,371 in control and 1,377 in the anchored arm (N59); the 152 accounts not reached carry forward into EXP-2's re-offer population rather than being re-run here (N91).

## 5. Decision rule

| Outcome | Rule (N57, pre-declared 2026-11-05) | Action | Owner |
|---|---|---|---|
| Ship | Anchored arm converts at 6.0% or better, guardrails intact (M-006 and M-008 per N58) | Switch the control arm (S-3) and any S-1 accounts not yet exposed to the anchored offer, then open phase 3 | Maya Chen |
| Iterate | Either arm converts between 4.0% and 6.0% | Revise the anchor's wording or the offer's placement on the activation page, and re-test before phase 3 opens | Maya Chen with Tomas Lindqvist |
| Kill | Both arms under 4.0%, or a guardrail is breached | Hold phase 3, reopen the pricing and packaging document's section 1 (value metric), and write the learning into the next metrics review | Maya Chen with Isabel Ferreira |

M-010 (at most 8 per 100 add-on accounts per week, N74) is monitored alongside M-006 and M-008 during exposure but is not one of N57's or N58's pre-declared ship conditions.

**Proposed for EXP-2, 2026-12-22 (not yet pre-declared, not part of N57):** tightening the decision rule for the next experiment by requiring the anchored arm to clear control by the full 2.5-point minimum detectable effect (N55) on Ship, narrowing "either arm" to the arm under test on Iterate and Kill, and adding M-010 as a Ship-row guardrail. The 2,080-per-arm power observation below is the reason this refinement is proposed; it is a limitation of this experiment's sizing, not a rule this experiment was run against. None of this refinement changes EXP-1's own decided outcome: both arms fell under 4.0% and every guardrail held, so the result is KILL under N57's wording as pre-declared.

**Decided on 2026-12-18:** Control converted at 33 of 1,371, 2.4%; anchored converted at 40 of 1,377, 2.9%; pooled 73 of 2,748, 2.7% (N61). Both arms sat under the 4.0% kill line, and the 0.5-point gap between arms sat inside a standard error of about 0.6 points, so it is not read as a real difference. The funnel behind that number shows where accounts left: of the 2,748 exposed, 1,044 (38%) opened the offer, 302 (11%) reached the price step, and 73 (2.7%) paid (N60): 62% of exposed accounts never opened the offer, and 93% of those who opened it did not pay. Guardrails held: M-006 pooled at 76% across active add-on accounts in the review window, above the 70% floor, M-008 at 2.4 errors per 100 drafted reports, under the 3 ceiling, and M-010 at 5.1 support tickets per 100 add-on accounts per week, under the 8 ceiling (N65, N67, N58, N74). The kill rule fired on the target metric alone; the product held. Executed by Maya Chen on 2026-12-18 per the pre-declared rule (N57, N62), and ratified as decision D6 at the [metrics review, section 5](ledgerline-metrics-review.md), on 2026-12-21, which recorded PIVOT on packaging rather than a product pivot, per the [journey timeline](ledgerline-journey.md).

The mechanism named in section 1 failed mainly because buyers do not read an add-on charge against labour cost when the charge scales with seats that do not file, so no anchor could make $204 a month, the median account's 34 seats at $6 (N47), read as a saving against a $149 plan. Four of six win-loss interviews named the seat-priced total as an obstacle: seats billed for non-filers, a total above the plan, or a total above the buyer's own budget (N77); only WL-01, Redfern Heating and Air, named the reviewer-cost anchor directly, calling 30 reviewer-hours a month "a big company's problem" against a reviewer who does the work alone on a Friday. The advisory board named the same seat problem and asked for a per-report price at its session on 2026-12-02 (N78), five days before the first win-loss interview. That is why D6 reopened the value metric (D3) instead of iterating the anchor copy, an option D6 rejected because both arms were under the kill line.

## How this experiment fails

| Failure mode | What it looks like | The rule that stops it, as applied here |
|---|---|---|
| A variant, not a hypothesis | The brief names the change but not the behaviour it predicts | Section 1's "because" clause names the reviewer-cost mechanism, not just the anchored-banner variant, before launch |
| Peeking and stopping early | Checking daily and calling it the first time it looks significant | M-007 is computed once, on 2026-12-18; the T-7 funnel tile is visible only to Kwame Boateng, the analyst, until then (dashboard spec, section 3). The OKR sheet's 2026-12-14 check-in records exposure only and leaves M-007 unread, so no conversion figure was reported before the analysis date |
| Never powered | A detectable effect picked to suit the schedule, then "no effect" reported | The 2.5-point minimum detectable effect was computed from the 4.1% baseline and the traffic on 2026-11-05, before any account was exposed (N55) |
| No guardrails | The primary metric improves while something else quietly gets worse | M-006, M-008 and M-010 floors were checked at the 2026-12-18 analysis and all held (N65, N67, N74), and drafting would have paused for the affected account or language had M-008 reached 3 per 100 before the analysis date (section 2) |
| No decision rule | "We will look at the numbers and discuss" | Section 5's ship, iterate and kill rules and owners were written on 2026-11-05, before exposure opened |
| The loser ships anyway | The variant underperformed and was merged regardless | Both arms fell under the kill line, so phase 3 was held rather than entered, per section 5's Kill row |

## Exit gate

This brief is fit to launch when:

- [x] The hypothesis names a mechanism, not just a direction. Section 1's "because" clause names the reviewer-cost anchor mechanism, and that mechanism, not just the offer copy, is what the decided outcome later found to be the main problem.
- [x] Exactly one target metric is named, tied to the north star tree, with a dated baseline. M-007 is the sole target metric, linked to M-002 and M-001 in section 2, with the 4.1% baseline dated to the prior add-on's 2026-03-02 launch (N39).
- [x] A guardrail exists with a numeric floor and a stop behavior. Section 2 carries M-006 (at least 70%), M-008 (under 3 per 100), and M-010 (at most 8 per 100 add-on accounts per week), all checked at the decided outcome.
- [x] Sample size and duration were computed before launch, arithmetic shown. Section 4 shows the two-proportion sizing to about 1,270 accounts per arm and the 12-day exposure plus 14-day conversion window, computed by Kwame Boateng on 2026-11-05 (N55).
- [x] All three decision outcomes have pre-committed rules, actions, and owners. Section 5's table names an owner for ship, iterate and kill before any account was exposed.
- [x] The kill outcome ends in a written learning, not a quiet burial. The decided-on note names the mechanism defect, and it is carried forward into D6 and the growth plan's next bet rather than dropped.

Signed: Maya Chen, product manager, 2026-11-05
