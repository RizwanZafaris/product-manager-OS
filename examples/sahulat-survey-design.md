# Survey Design: SV-1, Agent-App Bill-Pay Census

Fills [templates/discovery/survey-design.md](../templates/discovery/survey-design.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, carried from the [Sahulat journey](sahulat-journey.md) data sheet and the [coverage sheet](sahulat-coverage-sheet.md) it extends, never invented fresh here. See the [examples index](README.md).

**Owner:** Hira Baig · **Date:** 2026-09-11 · **Status:** Analyzed; designed 2026-09-11, piloted 2026-09-15, fielded 2026-09-16 to 2026-09-22, tabulated 2026-09-28 (CN21, CN22, CN24)

## 1. Goal and decision

| Field | Value |
|---|---|
| Research question | How many of Sahulat's agents already perform a bill payment for a customer, and how often, in a stated recent window |
| Decision this informs | Bilal Hasan's agent commission schedule v8, adding the bill-pay line (N39, DEP-4 v8, due 2026-09-30); the schedule pays agents PKR 5 per assisted bill only if assisting is already common practice, not a fringe behaviour the pilot invented |
| Result that would change the decision | Agreed before fielding, 2026-09-11: if fewer than 25 percent of respondents report an assisted payment in the last seven days, the pivot premise itself reopens with Faisal Mirza before Bilal Hasan prices a line item for it (CN23). At or above 25 percent, commission-schedule work proceeds on the assumption D8 already made (D9, dated 2026-09-18, postdates this survey and does not bear on the commission-schedule decision it feeds) |
| Why a survey and not five more interviews | INT-015 to INT-020, the six pass-2 Mom Test sessions, already show assisting is not rare (CN16: 11, 6, 9, 14, 2, 8 assisted payments each in the last seven days), but six agents cannot say how common that is across 3,200. The commission schedule prices a behaviour by volume; volume needs a count across the population, not six more stories |

## 2. Sample

| Field | Value |
|---|---|
| Population described | Sahulat's 3,200 active agents (N5), the group whose commission schedule this survey feeds |
| Sampling frame | The agent-app roster: agents whose agent app is installed and who received the push. This is narrower than N5's full 3,200. The coverage sheet does not carry a separate count of agents without the app or with a dormant install, so the exact frame size is Open: Tariq Sohail. What is known is the response count against N5 itself (CN21: 734 of 3,200, 23 percent), which is a lower bound on the frame's true reach, not a true response rate against the frame |
| Sampling method | Census of the reachable frame, not a random draw: every agent who opens the app in the field window sees the survey, an access filter that is the exposure mechanism rather than part of the frame. This over-represents agents who use the app often, which likely skews toward agents already comfortable keying a transaction on it, the same skill the assisted-payment behaviour in Q1 and Q2 requires. A frame limited to app users may over-count assisting relative to the full 3,200, including agents who rarely open the app at all |
| Target responses | 500, with at least 150 from the Lahore pilot district (CN20). 500 was set so the district cut in section 6 would not be read off fewer than a hundred and fifty respondents per side, and because the RQ's 25 percent threshold (CN23) needs enough respondents that a few percentage points either way do not flip the decision on sampling noise alone |
| Segments that must be readable on their own | Lahore pilot district (where the float top-up hotline has been live since 2026-07-17) against everywhere else. The two districts have carried different operational conditions since launch, so a single pooled number could hide a real difference in how often assisting happens |
| Incentive | PKR 100 airtime per complete (CN20), the same mechanism the coverage sheet uses for SV-2 (CN36). It is enough to be worth a minute's typing, not so large that an agent who never assists a customer will invent one to collect it; there is no independent check inside SV-1 on that risk, flagged again in section 4 |
| Field window | Pilot 2026-09-15; field 2026-09-16 to 2026-09-22; one reminder push 2026-09-19 (CN20) |

## 3. Question bank

District (Lahore pilot against elsewhere) is not asked. The agent-app account record already carries each respondent's counter district, and CN21's 188-against-546 split is read from that field at tabulation, not self-reported; asking it again would only add a chance for a typo to break the segment cut.

| # | Question text, as the respondent sees it | Type | Answer options (balanced, exhaustive, one "none of these") | Serves (RQ or segment cut) | Required |
|---|---|---|---|---|---|
| Q1 | In the last 7 days, did you help a customer complete an electricity or gas bill payment at your counter, whether you keyed it or the customer did on their own phone? | Single choice | Yes / No | RQ1 | Yes |
| Q2 | In the last 7 days, how many bill payments did you help a customer complete? | Open numeric, whole number | Numeric entry, 0 to 99; shown only if Q1 is Yes | RQ1 | Yes if Q1 is Yes |
| Q3 | How important is it to you that you can confirm a customer's bill has posted before she leaves your counter? | Rating scale, 1 to 10 | 1 (not important) to 10 (critical) | Segment cut, opportunity scoring (OUT-1) | Yes |
| Q4 | How important is it to you that you do not run out of float on a day when many bills are due? | Rating scale, 1 to 10 | 1 (not important) to 10 (critical) | Segment cut, opportunity scoring (OUT-2) | Yes |
| Q5 | How important is it to you that a customer never disputes a payment you keyed for her? | Rating scale, 1 to 10 | 1 (not important) to 10 (critical) | Segment cut, opportunity scoring (OUT-3) | Yes |
| Q6 | How important is it to you that you can hand the customer proof she accepts, quickly? | Rating scale, 1 to 10 | 1 (not important) to 10 (critical) | Segment cut, opportunity scoring (OUT-4) | Yes |
| Q7 | How important is it to you that helping with a customer's bill does not eat into unpaid time at your counter? | Rating scale, 1 to 10 | 1 (not important) to 10 (critical) | Segment cut, opportunity scoring (OUT-5) | Yes |
| Q8 | How satisfied are you today with how quickly you can confirm a customer's bill has posted? | Rating scale, 1 to 10 | 1 (not satisfied) to 10 (completely satisfied) | Segment cut, opportunity scoring (OUT-1) | Yes |
| Q9 | How satisfied are you today with how often you have float on a bill-peak day? | Rating scale, 1 to 10 | 1 (not satisfied) to 10 (completely satisfied) | Segment cut, opportunity scoring (OUT-2) | Yes |
| Q10 | How satisfied are you today with how rarely a customer disputes a payment you keyed? | Rating scale, 1 to 10 | 1 (not satisfied) to 10 (completely satisfied) | Segment cut, opportunity scoring (OUT-3) | Yes |
| Q11 | How satisfied are you today with how quickly you can hand the customer proof she accepts? | Rating scale, 1 to 10 | 1 (not satisfied) to 10 (completely satisfied) | Segment cut, opportunity scoring (OUT-4) | Yes |
| Q12 | How satisfied are you today with how much unpaid time a customer's bill costs you? | Rating scale, 1 to 10 | 1 (not satisfied) to 10 (completely satisfied) | Segment cut, opportunity scoring (OUT-5) | Yes |
| Q13 | Anything about handling a customer's bill at your counter you want Sahulat to know? | Open text | Free text, none of these not offered since the field is voluntary | Segment cut, opportunity scoring (open coding) | No |

**Screening question and routing:** No respondent is screened out at intake; the survey fields as a census to the whole reachable frame from section 2. Q1 routes: a No skips Q2 and moves straight to Q3, because Q3 to Q12 ask what any agent wants handled better, assisting today or not.

**Estimated completion time:** Open: not logged from the 5-agent pilot on 2026-09-15. The pilot confirmed the survey completed end to end on the agent app and did not time it; a repeat of this survey should capture this figure before fielding, not after.

## 4. Bias checks

Run 2026-09-11 by Sara Lodhi, who did not write the questions.

| Check | Passes when | Result |
|---|---|---|
| Leading wording | No question suggests its answer or names the product's virtue | Pass. Q1 asks about the behaviour plainly; none of Q3 to Q12 names Sahulat, the pivot, or the proposed PKR 5 line |
| Double-barreled | Each question asks one thing | Pass. Each of Q3 to Q12 states one outcome, in the direction-plus-measure-plus-object-plus-context form the [opportunity scoring](../frameworks/discovery/opportunity-scoring.md) worksheet requires, so no rating question can be read two ways |
| Acquiescence | Agree or disagree scales are balanced with reversed items, or replaced by specific choices | Pass by replacement. Q3 to Q12 use importance and satisfaction ratings on a stated 1-to-10 scale, not an agree-disagree pattern, so there is nothing to reverse |
| Order effects | Attitude questions come after behavior; options rotated where order could steer | Fix, applied before the pilot. Behaviour (Q1, Q2) already precedes the rating block. Sara Lodhi's review flagged that Q3 to Q12 asked the five outcomes in the same fixed order (OUT-1 to OUT-5) to every respondent, risking a primacy effect on whichever outcome lands first; Hira Baig added device-side randomization of the five outcome pairs (each importance question kept immediately before its own satisfaction question) before the pilot fielded |
| Recall period | Every "how often" names a period the respondent can remember | Pass. Q1 and Q2 both name the last 7 days, the same seven-day lookback the Mom Test sessions used (CN14's sessions ran 2026-09-10 to 2026-09-12 and CN16 reports each agent's last-seven-days count, the same length and question wording, not the same calendar dates), so the two data sources are comparable |
| Social desirability | No question makes one answer the respectable one | Open, not fully resolved. Section 7 tells respondents this survey feeds the commission schedule, which is exactly the incentive that could inflate Q2: an agent who wants to be paid for assisting has a reason to round the count up. Nothing inside SV-1 checks this independently. The closest external check is N45, Usman Javed's two-day field observation at twelve counters on 2026-08-11 and 2026-08-12 (41 of 53 observed bill payments were agent-assisted), but that is an August sample from twelve counters, not a check on this survey's respondents or window. Open: Sara Lodhi, whether Q2's self-reports track N45's observed rate once both exist for the same period |
| Coverage | Every likely answer has an option; "other" has a text box | Pass. Q1 is an exhaustive Yes or No; Q13 is the open catch-all for anything the rating scale cannot hold |
| Length | Completion time from the pilot is under [agreed minutes] | Open. No agreed-minutes figure was set before the pilot, and the pilot did not log completion time (section 3); this check cannot be marked Pass or Fail from what exists |
| Frame bias | Section 2 states who the frame leaves out and how that bends the result | Pass. Section 2 states the frame is narrower than N5's 3,200 and names the direction of the bias: an app-using frame likely over-represents agents already comfortable keying a transaction |

## 5. Pilot

- Pilot respondents: 5 agents from the app-holding roster, fielded 2026-09-15 (CN20)
- Watched for: completion time, the drop-off question, questions answered "other" more than expected, free text that reveals a missing option
- Changes made after the pilot: Open: Hira Baig. The order-effects fix in section 4 was made on 2026-09-11, ahead of the pilot, from Sara Lodhi's bias-check review, not from a pilot finding. Whatever the 5-agent pilot itself surfaced was not preserved as a numbered row in the coverage sheet; if this survey is repeated, the pilot's findings should be logged here rather than left to memory

## 6. Analysis plan

| RQ | Questions | Cut by (segment) | Statistic (share, mean, distribution, Kano class, PMF share) | Threshold agreed in advance | Action at each result |
|---|---|---|---|---|---|
| RQ1 | Q1, Q2 | Lahore pilot district against elsewhere | Share answering Yes to Q1; mean and median of Q2 among Yes respondents | Below 25 percent reporting a Q1 Yes reopens the pivot premise with Faisal Mirza (CN23) | At or above 25 percent: the pivot premise stands, commission-schedule v8 work continues on Bilal Hasan's track toward the 2026-09-30 date. Below 25 percent: pause commission-schedule pricing and take the result to Faisal Mirza before DEP-4 v8 is drafted further |
| Segment cut | Q3 to Q12 | Lahore pilot district against elsewhere | Mean importance and mean satisfaction per outcome (OUT-1 to OUT-5); opportunity score = importance + max(importance minus satisfaction, 0), per the [opportunity scoring](../frameworks/discovery/opportunity-scoring.md) worksheet, based on Tony Ulwick's Outcome-Driven Innovation method | No pass or fail threshold; this block ranks where agents are underserved rather than gating a decision | Feeds a separate opportunity-scoring pass over the OUT-1 to OUT-5 outcomes; not a gate on the commission-schedule decision itself |

- Open text handling: Q13 coded by Hira Baig using the [feedback-synthesis](../skills/feedback-synthesis/SKILL.md) skill; codes agreed before reading the first response
- Minimum responses before any segment is reported: 150, the same floor section 2 set for the Lahore cut, so a small-sample segment result is never read as a finding
- Where results are filed: this section, once fielding closes, and forward into the opportunity-scoring pass over Q3 to Q12

**Results, recorded 2026-09-22 to 2026-09-28.** Fielding closed at 734 responses, 23 percent of the 3,200-agent frame: 188 from the Lahore pilot district, 546 elsewhere (CN21). Of those, 426 (58 percent) answered Q1 Yes, well clear of the 25 percent floor set in advance, so the pivot premise was not reopened and Bilal Hasan's commission-schedule v8 work continued toward its 2026-09-30 date. Among Yes respondents, the median Q2 answer was 9 assisted payments in the last seven days (CN22). The Q3-to-Q12 ratings were tabulated by Sara Lodhi on 2026-09-28 and handed to the opportunity-scoring pass (CN24): unpaid counter time (OUT-5) scored highest at 15.8, ahead of proof-handing (OUT-4) at 14.3 and float (OUT-2) at 14.0, with dispute risk (OUT-3) lowest at 8.9. The social-desirability question left open in section 4 was not closed: CN22's 58 percent and N45's field-observed 41 of 53 (77 percent) are not the same period or the same measurement, so they do not confirm or contradict each other, and that comparison remains Open with Sara Lodhi.

## 7. Distribution, consent, and data handling

- Channel and who sends: in-app push through the agent app; sent by Sara Lodhi's team on Hira Baig's behalf, with the reminder on 2026-09-19
- What respondents are told: the survey is short, feeds how Sahulat supports agents at the counter, is not anonymous (the response is tied to the agent's own account so it can be cut by district), and is used by the product team and Bilal Hasan's finance team only
- Personal data collected: the agent's own app account identifier (needed to attach district and to prevent a second submission) and the self-reported answers; no customer data is collected or asked for. Whether this needs its own privacy-impact assessment or is covered by the agent app's existing one is Open: Amna Rasheed
- Raw data location, access, and deletion date: the agent-app survey export, readable by Sara Lodhi and Hira Baig only; deleted 2026-12-21, 90 days after the field window closed, a retention date set at design time rather than carried from an existing policy

## Exit gate (feeds Gate 1: problem worth solving)

Results enter the pass-2 discovery-synthesis pass as a source and, for the OUT-1 to OUT-5 block, the opportunity-scoring tabulation, toward [Gate 1](../os/STAGE-GATES.md) of the second pass, which the [coverage sheet](sahulat-coverage-sheet.md) notes is not yet scheduled.

- [x] One research question, one decision, and the result that would change it are written before fielding. Section 1: RQ1, the commission-schedule v8 decision, and the CN23 threshold
- [x] The frame's gaps and the sampling bias are stated, and the target count carries its reasoning. Section 2 names the app-only frame as narrower than N5 and states the direction of the resulting bias; the 500-response target carries the segment-floor reasoning behind it
- [x] Every question serves an RQ or a segment cut, and every bias check has a result. Section 3's table and section 4's table both carry one in every row, including the two left Open rather than Pass
- [x] The analysis plan names thresholds agreed with the decision owner before the first response. Section 6, RQ1 row, cites CN23, agreed 2026-09-11 before the 2026-09-16 field open
- [ ] A pilot ran and its changes are logged. The pilot ran (section 5, CN20); its findings were not preserved as a logged change, only the order-effects fix made ahead of it, so this box stays open for the next run
- [x] Consent wording and data handling are stated, with a deletion date. Section 7 states both; the PIA question is separately Open with Amna Rasheed and does not block this box
- [x] Signed by Hira Baig, 2026-09-11

Signed: Hira Baig, Product Manager, 2026-09-11.
