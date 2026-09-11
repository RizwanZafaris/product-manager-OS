# Growth Plan: Expense Copilot Add-on

Fills [templates/planning/growth-plan.md](../templates/planning/growth-plan.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count and dollar figure is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so it can be checked against the documents this plan follows. See the [examples index](README.md).

**Owner:** Maya Chen, product manager · **Period:** the growth cycle opening 2026-12-22, EXP-2 kill date 2027-02-12 · **Last updated:** 2026-12-22
**Linked metrics review:** [ledgerline-metrics-review.md](ledgerline-metrics-review.md) (2026-12-21, PIVOT on packaging, D6) · **Linked OKR sheet:** [ledgerline-okrs.md](ledgerline-okrs.md) (scored 2026-12-21)

## 1. Where the metric tree stands

Numbers are carried from the metrics review for its window, 2026-11-23 to 2026-12-18, not re-derived here.

| Metric | Role | Current | Trend over window | Source system |
|---|---|---|---|---|
| M-001, copilot-drafted reports approved on first submission per month, across customer accounts | North star | 422 (N65) | No prior-window figure for M-001 itself; the review judges the mechanism steady from M-003 and M-006 holding near their Phase 1 figures (metrics review section 2), not from a dated M-001 comparison | Product analytics joined to platform approval events |
| M-002, accounts with the add-on active (paid or design partner) at week end | Input | 79 = 73 paid + 6 design partners (N64); true figure 79 to 82 per G-1's up-to-3-account undercount | Target 180; actual 79; KR1 scored 0.44 (N70) | Billing |
| M-003, share of eligible reports drafted, pooled across active add-on accounts | Input | 47%, 555 of 1,180 (N65) | Target 50% (N72); held near Phase 1's 54%, though the cause of the drop from 54% to 47% is open (Kwame Boateng, per-account split due before EXP-2 exposure on 2027-01-11, metrics review section 2), not attributed to the wider account base | Product analytics |
| M-006, first-submission approval rate on drafted reports, pooled across active add-on accounts | Input | 76% (N65) | Target 78% (N71); held near target while M-002 missed by more than half | Reviewer approval events |
| M-007, offer-to-paid conversion within 14 days of first exposure | Diagnostic; EXP-1 target | Control 2.4%, anchored 2.9%, pooled 2.7% (N61) | Both arms under the 4.0% kill line (N57); the leak this plan exists to fix | Billing joined to exposure events |
| M-011, add-on MRR | Diagnostic; KR4 | $15,906 (N68) | Target $30,000; actual $15,906; KR4 scored 0.53 (N73) | Billing |

**The tree:** M-002 gates the population; within active accounts, M-001 = M-003 x M-006 applied to eligible reports. This window: 555 = 47% of 1,180 eligible reports (M-003); 422 = 76% of 555 drafted reports (M-006) = M-001 (N65).

## 2. The next growth bet

- **Input metric chosen:** M-002, accounts with the add-on active, moved through M-007, offer-to-paid conversion within 14 days
- **Why this one:** M-006 sat at 76% against a 78% target, so the product itself is not the ceiling on M-002; the win-loss and advisory-board evidence names the price as the cause; the funnel leaks at every step (section 3), where M-007 pooled at 2.7% against a 6.0% ship bar (N57, N61). That is the input with the most headroom relative to what the product already delivers, and it is the only input the pivot decision (D6) reopened. The one measured reference point for an add-on's conversion at Ledgerline is the prior Bills Automation add-on, 4.1% of exposed accounts paid within 14 days (N39); EXP-1's 2.7% sat below it, and EXP-2's 6.0% bar is a decision threshold set by the pre-declared ship rule (N57), not a second observed rate.
- **What the last metrics review said about it:** "Only the one input tied to the price, M-007, missed by more than half." (metrics review, 2026-12-21)
- **Decision:** D7, EXP-2 is the next bet, decided 2026-12-22 by Maya Chen with Isabel Ferreira; Isabel Ferreira approves the $2.40 offer price to about 2,818 to 2,821 accounts.
- **Targets for the next cycle:** none are set here. M-002 and add-on MRR have no next-cycle target in this plan, consistent with the [OKR sheet](ledgerline-okrs.md)'s end-of-period line, which records that this plan sets EXP-2's 6.0% bar on M-007 and names M-002 as the bet, and that it does not itself set targets for the next OKR cycle. Open: Maya Chen and Isabel Ferreira set a next-cycle M-002 target (a delta from 79 accounts at 2026-12-18, N64) and a usage-MRR target (a delta from $15,906, N68) at the next OKR cycle. Open: the metrics dictionary's M-011 formula (seats x per-seat price) cannot compute MRR under a per-report price; it needs a new id or a version suffix before a usage-MRR target can be carried against it.

## 3. The loop or channel behind the metric

- **Mechanism:** an S-1 account is exposed to the add-on offer inside the Expenses settings page, opens the offer, reaches the price step, and an account admin activates and pays. The loop is a single-touch conversion funnel, not a referral loop; nothing here feeds a second account's exposure.
- **Where it leaks today:** at every step, not sharply at one. Of 2,748 exposed accounts: exposed to opened, 1,044 of 2,748 = 38% (62% lost); opened to price step, 302 of 1,044 = 29% (71% lost); price step to paid, 73 of 302 = 24% (76% lost) (N60, N61). As a share of exposed accounts the price-step drop (11% of exposed reaching it, down to 2.7% paying, about 8 points) is the smallest of the three in absolute terms; the price step is the worst single step, not a cliff. The price is named as the cause because the win-loss and advisory-board evidence below names it directly, not because the funnel shape singles it out; the control arm's activation page already shows the $6-per-seat price at the "opened the offer" step (LEDGERLINE-S1), before an account ever reaches the price step, so some of the opened-to-price-step loss (71%) may be price-driven too. EXP-2's read should report every step rate, not only the end-to-end conversion.
- **Evidence:** EXP-1's funnel counts (N60, N61) from product analytics joined to exposure events; six win-loss interviews WL-01 to WL-06 (N76, N77), where four of six named the seat-priced total as an obstacle: seats billed for people who never file, a total above the plan, or a total above the buyer's own budget, and both wins had filers at 70% or more of seats; the advisory board's first session (EV-AB01, N78), where six of eight members said seat pricing penalises accounts with few filers and five of eight asked for a per-report price, about two weeks before EXP-1's kill (2026-12-02 to 2026-12-18, 16 days), and three weeks before the metrics review ratified it.

## 4. The cheapest experiment

<!-- The design's success event is defined explicitly against M-007 (offer-to-paid
     conversion), not against product activation alone, so the 6.0% bar is meant
     to carry the same meaning it did when EXP-1 failed it. Whether the
     measurement window itself, first exposure to payment or first exposure to
     first invoice, stays as declared is still open; see the note on billing
     timing below the table. -->

| Hypothesis (must be falsifiable) | Design | Cost (people-days + spend) | Duration | Success threshold | Owner |
|---|---|---|---|---|---|
| A usage price of $2.40 per drafted report (N89), billed monthly in arrears with no seat charge and no minimum, converts at least 6.0% of exposed accounts within 14 days, because it removes the objections that surfaced across the win-loss batch: seats billed for people who never file (WL-01, WL-04, the latter asking unprompted for a per-filer or per-report number), an add-on priced above the plan (WL-06, $228 against the $149 plan), and a seat total above its own budget (WL-05, whose $330 total landed above its own budget for a small finance tool, unprompted). The per-report price answers the second objection with a monthly cost that reads as a fraction of the plan and of Cinderwick's seat price rather than a multiple of either (N90, N13, N27) | EXP-2: single-arm re-offer to up to 2,827 S-1 accounts not currently paying (2,675 exposed non-converters plus 152 never exposed), less the up to 3 accounts G-1 shows activated through manual invoice lines in the EXP-1 window and the six design partners already active, for a population of about 2,818 to 2,821 accounts; success is M-007 measured on this population, 6.0% or more reaching paid status within 14 days of exposure, per N91 | 1 person-month, about $10,000, for the usage meter DEP4/ADR-008 (N87); no new spend beyond that for engineering, though the offer page needs a rewrite for the new price and the LEDGERLINE-S6 running-cost display is new UI, not reused from EXP-1 | Exposure from 2027-01-11 once DEP4 lands by 2027-01-08, closing by 2027-01-29 so every account's 14-day window closes inside the review period; analysis date 2027-02-12, or kill at that date if not analysed sooner (N91, N92) | 6.0%, the same bar EXP-1 failed against, on purpose, so the pivot cannot be declared a success by lowering the line; 4.0% to 6.0% iterates rather than ships or kills, owner Maya Chen with Tomas Lindqvist, as EXP-1's brief did | Maya Chen |

- **Billing timing note:** "billed monthly in arrears" means the usage event (a drafted report an account is charged for) and the invoice date are not the same day; most of the 14-day window will close before an account's first month-end invoice posts. M-007's paid_event is joined to `billing.paid_event`. Open: Maya Chen with the billing lead confirms before 2027-01-11 whether a mid-cycle usage charge can post and be paid inside 14 days, or whether M-007's window needs to run from first exposure to first invoice rather than first exposure to payment for this experiment; either way, "activated with no payment" does not count toward the 6.0%. If the window changes to first exposure to first invoice, that is a changed measure of M-007 for this experiment, not a silent substitution, and will be registered as M-007 v2 in the metrics dictionary's change log before EXP-2's analysis date.
- **Worth, before cost:** at the 6.0% success threshold, about 169 of about 2,820 exposed accounts (2,820 x 6.0%) would convert. At the median S-1 account's 7 reports filed a month (N33) and $2.40 per drafted report, the monthly bill per converted account ranges from about $7.90 at the observed 47% drafted share (N65, M-003) to about $16.80 if every filed report were drafted; across 169 converted accounts that is about $1,335 to $2,839 a month, roughly $16,000 to $34,000 a year. N90 now carries this same median-account range rather than the mean of 11 reports a month it used before the 2026-12-22 data-sheet correction.
- **Cheaper alternative considered:** a manual-invoice usage pilot on a small sample, extending the mechanism G-1 already used for 3 legacy accounts, was considered and not chosen; it does not exercise the billing-scale path DEP4 delivers or protect the 14-day measurement clock the way an automated meter does, and EXP-2 needs both before a wider re-offer.
- **Population and precision:** at n = about 2,818 to 2,821 (2,827 less the design-partner and G-1 exclusions named in the Design cell above) and an assumed true rate near 6.0%, the standard error is about 0.45 points. 95% of S-1 (2,675 of 2,827) already declined the seat offer once; this is a single-arm re-offer to mostly prior decliners with no holdout, run across January, so a result cannot be cleanly separated from re-exposure effects or seasonality. No holdout: the 6.0% bar is absolute rather than a lift over a control, every non-paying S-1 account gets the re-offer, and because 95% of the population already declined once, the design is biased against success rather than toward it.
- **Buyer-facing cost:** the median account's usage price is about $7.90 to $16.80 a month (see Worth, above), the range set by the 47% observed drafted share (N65, M-003) up to every filed report being drafted, against a $149-a-month plan, about 5% to 11% of it (N27), and against Cinderwick's $8-per-seat benchmark. The data sheet's N90 row was corrected 2026-12-22 to this same median-account figure (7 reports a month, N33), replacing the earlier mean-based $26 figure. No buyer has been asked this specific number: 5 of 8 advisory board members asked for a per-report price in the abstract (N78), and 0 of 6 design-partner interviews asked any price (N40); willingness to pay at $2.40 is unvalidated.
- **What ships:** LEDGERLINE-S6, "as an account admin, I am billed per drafted report in arrears and can see the running count and the month's cost so far," is the story EXP-2 depends on.
- **Open:** EXP-2 experiment brief, owner Maya Chen, due before 2027-01-11 exposure start, per the template's routing of each experiment through [experiment-designer](../skills/experiment-designer/SKILL.md); not yet written or linked here.

## 5. Counter-metric

| Metric | Damage it detects | Threshold that stops the experiment | Source system |
|---|---|---|---|
| M-009, model cost per drafted report | A usage price that outruns the cost it is meant to cover | Hard stop at $1.05 (N92), unchanged from the OKR cycle's M-009 ceiling (N74); this does not, on its own, protect the N49 60% margin floor at the $2.40 price, which binds at $0.96 per report (2.40 x 0.40). Measured cost is $0.93 (N67, the window figure, not the $0.92 derived at the quoted rate in N11), about 61% margin, roughly 3 cents of headroom before the floor is breached. Written trigger: a margin review is called by Daniel Okafor the first week M-009 exceeds $0.96, ahead of the $1.05 hard stop; see R6 and DEP2, since a vendor volume re-quote at customer scale is the risk that moves this number | Vendor invoice over drafted count |
| M-006, first-submission approval rate on drafted reports | A conversion push that trades product quality for a lower price story | Must not fall below 70% (N92) | Reviewer approval events |
| M-010, support tickets per 100 add-on accounts per week | A new billing model that confuses account admins into support load | Must not exceed 8 per week (N92) | Support system |

## 6. Kill condition

- **Ends at:** conversion under 4.0% at the analysis date, or 2027-02-12, whichever comes first (N92)
- **Who decides:** Maya Chen (N92)
- **Decision lands in:** [decision log](../templates/execution/decision-log.md) entry, plus a ledger row below
- **Next metrics review:** the EXP-2 analysis date, 2027-02-12

## Experiment ledger

| # | Experiment | Dates | Result (number vs threshold) | Decision (scale / iterate / kill) | Logged at |
|---|---|---|---|---|---|
| 1 | EXP-1, per-seat price at $6 a seat per month, plain and anchored against the N7 reviewer-cost anchor | Exposure 2026-11-23 to 2026-12-04; analysis 2026-12-18 (N56) | Control 2.4%, anchored 2.9%, pooled 2.7%, both arms under the 4.0% kill line, the 0.5-point gap inside a standard error of about 0.6 points (N61) | Kill, executed by Maya Chen 2026-12-18 per the pre-declared rule (N57, N62); ratified as D6 on 2026-12-21 | Decision log D6, 2026-12-21 (metrics review) |
| 2 | EXP-2, usage price at $2.40 per drafted report, no seat charge | Exposure planned from 2027-01-11; analysis or kill by 2027-02-12 (N91, N92) | Open: not yet run | Open: not yet run | This plan, 2026-12-22 |

## How this plan fails

| Failure mode | What it looks like | The rule that stops it, as applied here |
|---|---|---|
| Tactics with no loop | A calendar of activities, and no mechanism by which one feeds the next | Section 3 names a single-touch exposure-to-paid funnel, explicitly not a referral loop, and says so rather than implying one |
| No counter-metric | Signups rise, and so do churn and support load, and the plan reports growth | Section 5's three thresholds, M-009 with an explicit break-even at $0.96, M-006 at 70%, M-010 at 8 a week |
| Channels chosen by fashion | Budget moves to whichever channel is discussed most this quarter | The channel here is fixed, the existing single-touch offer page; the bet is the price on it, chosen from win-loss and advisory-board evidence (section 3), not from discussion volume |
| No kill condition | A channel underperforms all quarter because stopping feels premature | Section 6: under 4.0% or 2027-02-12, whichever comes first, decided by Maya Chen, with an explicit 4.0-6.0% iterate band (section 4) so a mid-range result has a named owner and does not default to either extreme |
| Targets with no baseline | A committed lift with no documented starting number | This plan sets no next-cycle M-002 or MRR target itself, and section 2 records that as an open item rather than leaving it implied by the OKR sheet; when set, both will be deltas from the dated baselines already on this page, 79 accounts and $15,906 at 2026-12-18 (N64, N68) |

### The rejected option: iterate the anchor copy

At the 2026-12-21 metrics review, iterating EXP-1's anchor copy was argued and rejected, because both arms sat under the 4.0% kill line, not between the 4.0% to 6.0% iterate band the brief pre-declared (N57); there was no live arm left to iterate on. Persisting with discounts was also argued and rejected, because N48 forbids any discount beyond the two already agreed, annual prepay and the design-partner rate, without Isabel Ferreira and a decision-log entry, and a discount does not fix a value-metric mismatch. A two-price test for EXP-2 at $1.60 and $2.40 was argued at this plan's own signing and rejected: $1.60 sits under the N49 60% margin floor at the $0.92 derived at the quoted rate (N11), so it was never a price the margin rule would have let ship (D7).

## Exit gate

This plan is fit to run when:

- [x] The bet is a single input metric, and the tree linking it to the north star is written in section 1. M-002 is the chosen input, and section 1's table plus its tree line trace M-002 through M-003 and M-006 to M-001, with M-007 as the diagnostic the bet moves.
- [x] The mechanism behind the metric is named, with the leak located and evidenced. Section 3 names the single-touch exposure-to-paid funnel and reports the leak at every step, with the price step named as the worst single step on win-loss and advisory-board evidence, not on funnel shape alone.
- [x] The hypothesis can fail, with a numeric success threshold agreed before the experiment starts. EXP-2's threshold is 6.0% within 14 days, measured against M-007 (paid, not product activation), pre-declared 2026-12-22, the same bar EXP-1 failed against, with an iterate band at 4.0-6.0% and a kill under 4.0%. Open: whether M-007's window runs from exposure to payment or exposure to first invoice for this experiment (see the billing timing note in section 4); the 6.0% bar itself is unchanged either way.
- [x] Cost and duration are stated, and the experiment is the cheapest that could plausibly move the metric. One person-month for the usage meter (N87), plus the LEDGERLINE-S6 billing display; section 4 states the worth at the 6.0% bar and names the cheaper alternative considered and rejected.
- [x] A counter-metric is named with a stopping threshold and a source system. Section 5 carries M-009, M-006 and M-010, each with a threshold and a source system; M-009's row also states the margin floor's actual break-even.
- [x] The kill condition names a date or a threshold and a decider, before the start. Section 6: under 4.0% or 2027-02-12, whichever comes first, decided by Maya Chen (N92); exposure closes 2027-01-29 so every account's window falls inside the period.
- [x] Every finished experiment has a ledger row and a decision-log entry, failures included. EXP-1's ledger row records the kill, logged at the decision log's D6 entry; EXP-2's row is open because it has not run.

Signed: Maya Chen, product manager, 2026-12-22. Isabel Ferreira, Chief Product Officer, co-decider on D7 and approver of the $2.40 offer price, 2026-12-22.
