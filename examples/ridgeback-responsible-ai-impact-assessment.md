# Responsible AI Impact Assessment: Ridgeback Trails conditions brief

Fills [templates/ai/responsible-ai-impact-assessment.md](../templates/ai/responsible-ai-impact-assessment.md). Everything here is invented for this standalone example: Ridgeback Trails is a fictional hiking app offered in the UK, the people are invented, the land managers and rescue teams are unnamed composites, and every count, rate, score, date and identifier is ILLUSTRATIVE, not drawn from any real app, trail or incident. See the [examples index](README.md).

**Feature:** For each trail, a model summarises the community trip reports from the last 14 days into a conditions brief of three to five lines (ice and snow, flooded fords, path damage, closures and diversions, livestock), shown on the trail page before a hike.
**Model and version assessed:** `model-r-2026-09-01` (ILLUSTRATIVE), the same string as the conditions-brief eval spec and model card
**Assessment owner:** Imogen Thwaite, Product Lead, Trail Pages · **Date:** 2026-10-27 · **Next review:** 2027-01-27, or any trigger in section 7
**Regulator applicability, recorded by Rhys Pemberton, Legal Counsel, on 2026-10-09:** no financial or data regulator applies to the conditions brief in the sense os/STAGE-GATES.md uses, so the regulated module does not fire. The feature handles no money and no special-category data. Ordinary personal-data duties for accounts and trip-report locations are handled in the Ridgeback privacy impact assessment. The app is offered in the UK only, so no EU AI Act classification was made; section 7 makes one a precondition of any EU market.

Gate 3 for the conditions brief is planned for 2026-11-03. The brief has run in a closed prototype beta with 410 users since 2026-08-18 (ILLUSTRATIVE), which is where several bases below come from.

## 1. Intended use and out-of-scope use

- What the feature does, for whom, in what situation: it helps a walker who is deciding whether to do a trail, and what to bring, by summarising what other walkers reported recently. It supplements official forecasts, land-manager notices and the walker's own judgement; it replaces none of them.
- What the output decides or informs: it informs the walker's go or no-go and kit decision. No person reviews each brief before it is shown; about 2,400 briefs are regenerated per day (ILLUSTRATIVE).

| Foreseeable use | In scope? | What the product does about it | Where we learned it is foreseeable |
|---|---|---|---|
| Planning a lowland walk: what to expect underfoot | Yes | Nothing extra | Beta feedback |
| Using the brief as the only safety check for a winter mountain route | No | On upland and mountain trails from November to March, the official mountain forecast link and the land manager's notices sit above the brief, and the brief opens "Not a safety check" | Beta support tickets T-3312 and T-3390; consequence scan row C2 |
| Reading a brief for a trail with one or two recent reports | No | After the section 4 result, no brief is generated below 3 reports in 14 days; the raw reports are shown with their dates under "Few recent reports" | Section 4 |
| A walking-club leader deciding for a group from the brief | No | Nothing built beyond the report count and dates; recorded as part of H6 | Consequence scan row C5 |
| A mountain rescue team reading briefs to judge where a missing walker went | No | Nothing built; the outreach letter to rescue teams says briefs are summaries of user reports, not observations | Conversation with one team's volunteer coordinator, 2026-10-02 |

## 2. Affected groups, including people who never use it

| Group | User or non-user | How the output reaches them | What they can do about it today | Consulted? How, how many, when |
|---|---|---|---|---|
| Walkers who read the brief | User | Trail page | Flag the brief; open the raw reports | In-app survey, 410 beta users, September 2026 |
| Companions walking with a user | Non-user | Through the user's decision | Nothing inside the product | Not consulted |
| Trip-report authors | User | Their words are summarised | Flag "This misrepresents my report" | Interviews with 8 frequent authors, September 2026 |
| Welsh-language report authors and readers | User | Their reports may be summarised less completely | Same flag as above | Not consulted separately; see the open field in section 4 |
| Volunteer mountain rescue teams | Non-user | Call-outs rise if briefs under-warn | Nothing | One conversation with one team's volunteer coordinator, 2026-10-02 |
| Land managers and estate rangers | Non-user | Closures shown or missed; over-warning cuts visits | Land-manager portal for official notices | Call with 3 land managers, 2026-09-24 |
| Cafes, guides and car parks near trailheads | Non-user | Footfall falls if briefs over-warn | Nothing | Not consulted |

[OPEN: rescue-team consultation is one conversation with one coordinator; owner Imogen Thwaite, to present the brief and this assessment at the regional rescue teams' meeting by 2026-12-01.]

## 3. Harms by severity and likelihood

Scales as defined in the template. Score = severity x likelihood; severity 5 sorts to the top band whatever its score.

| # | Harm, and its type | Group affected | Severity | Basis | Likelihood | Basis | Score | Mitigation, as a design change where possible | Owner | Residual score |
|---|---|---|---|---|---|---|---|---|---|---|
| H1 | Brief omits a hazard present in its source reports, and a walker goes onto an upland route unprepared (safety) | Walkers, companions, rescue teams | 5 | Serious injury on a mountain route is the worst credible case | 2 | Not seen in the beta; the path exists, since hazard recall is below 1.0 in section 4 | 10, top band by severity 5 | Official forecast and notices above the brief on upland trails; hazards listed first; recall floor per segment with a stop condition; no brief below 3 reports | Imogen Thwaite | 5 x 1 = 5, still top band by severity 5 |
| H2 | Brief states a hazard no report mentions, so walkers avoid a safe trail and learn to ignore warnings (quality of service) | Walkers, nearby businesses | 3 | Lost trust makes later true warnings less effective | 3 | 9 invented hazard lines in 300 briefs in the eval | 9 | Every hazard line links to the report it came from; a line with no source is dropped by the verifier before display | Kwame Osei-Lindqvist, ML Lead | 3 x 2 = 6 |
| H3 | Trails with few reports get worse briefs (quality of service) | Walkers on rural and less popular trails | 4 | The omission harm in H1, concentrated on one group | 4 | Seen in this product's own eval, section 4 | 16 | No brief below 3 reports in 14 days; raw reports shown instead | Imogen Thwaite | 4 x 2 = 8 |
| H4 | Welsh-language reports summarised less completely (quality of service) | Welsh-language authors and readers | 3 | Hazards from those reports reach fewer readers | 3 | 4 of 17 Welsh hazards missed in section 4, too few to read as a rate | 9 | Open: more labelled cases first, then decide | Ffion Maddox, Content Lead | Not scored until measured |
| H5 | A paraphrase reveals when a solo author was on a trail, such as "a walker on her own at 6am" (privacy) | Trip-report authors | 3 | Exposes a pattern of someone's movements | 2 | Two such paraphrases found in beta spot checks | 6 | Output filter strips times, ages, genders and group sizes; author names never appear in briefs | Kwame Osei-Lindqvist | 3 x 1 = 3 |
| H6 | Walkers stop reading raw reports and official forecasts (over-reliance) | Walkers, companions | 4 | Over-reliance turns any H1 miss into an injury path | 3 | Beta: the raw-report open rate fell from 0.41 to 0.18 after briefs appeared | 12 | Report count and newest and oldest dates shown; "Not a safety check" line; official forecast link on upland trails | Imogen Thwaite | 4 x 3 = 12, accepted: the design levers available are weak, so it is monitored in section 7 |
| H7 | Brief keeps a closure that has been lifted, and a trail and its trailhead businesses lose visits (allocation) | Land managers, nearby businesses | 2 | Lost income, recoverable | 3 | One stale closure in the beta | 6 | Portal notices override briefs within an hour; closures are shown verbatim from the portal, never written by the model | Imogen Thwaite | 2 x 2 = 4 |

H1, H3 and H6 are in the Ridgeback risk register as R-21, R-22 and R-23, with the same owners.

## 4. Fairness checks by segment

- Labelled set: `evals/brief-hazards-v2`, 300 briefs holding 612 hazards, labelled by two contract rangers between 2026-10-06 and 2026-10-10 · Floor below which a segment is a count, not a rate: 20 hazards, matching the eval spec
- Measure, written before the run: hazard recall = hazards in the source reports that appear in the brief / hazards in the source reports. Gap = miss-rate ratio = (1 minus the segment's recall) / (1 minus the reference segment's recall). A segment fails if its ratio is above 1.5 or its recall is below 0.90 (both ILLUSTRATIVE thresholds, set by Imogen Thwaite and Kwame Osei-Lindqvist on 2026-10-01).

| Segment | How membership is known | n (hazards) | Measure and formula | Result | Reference segment result | Gap | Fails at | Verdict |
|---|---|---|---|---|---|---|---|---|
| 10 or more reports in 14 days | Report count from the trail database | 290 | Hazard recall, miss-rate ratio | 0.952 (276 of 290) | Reference | 1.00 | | Pass |
| 3 to 9 reports | Report count | 232 | Same | 0.931 (216 of 232) | 0.952 | 1.43 | Ratio above 1.5, or recall below 0.90 | Pass |
| 1 or 2 reports | Report count | 90 | Same | 0.844 (76 of 90) | 0.952 | 3.22 | Same | Fail |
| Upland and mountain trails | Trail grade from the trail database | 340 | Same | 0.918 (312 of 340) | 0.941, lowland | 1.40 | Same | Pass |
| Lowland trails | Trail grade | 272 | Same | 0.941 (256 of 272) | Reference | 1.00 | | Pass |
| Welsh-language source reports | Language detected on the report, checked by a Welsh-speaking labeller | 17 | Same | 13 of 17 | | | | Count only |

The aggregate is 568 of 612 hazards, a recall of 0.928, which passes the floor. Only the split shows that trails with one or two reports fail it: the miss-rate ratio is (1 minus 0.844) / (1 minus 0.952) = 0.156 / 0.048 = 3.22. The design change in H3 followed from this row: no brief is generated below 3 reports, so that segment now receives raw reports and no generated text.

[OPEN: Welsh-language recall cannot be read at 13 of 17 hazards; owner Ffion Maddox, Content Lead, target 40 labelled Welsh hazards by 2026-12-15, then this row is re-run and H4 is scored.]

## 5. Transparency to users

| What is disclosed | Where and when it is shown | Who sees it (users, and any non-user it reaches) | Spec reference |
|---|---|---|---|
| That a model produced the output | Label above every brief: "AI summary of 7 trip reports" (count varies) | Every reader of the trail page | Conditions-brief interaction spec section 1 |
| What the output is based on | "Newest report 2 days ago, oldest 11 days ago" under the label; every hazard line links to its report | Every reader | Interaction spec section 3 |
| Known limits, from model-card.md section 2 | "It can miss things. Not a safety check."; on upland trails the official forecast link sits above the brief | Every reader | Model card section 2 |
| How to reach a person, and how to report a problem | "Something wrong?" link under each brief opens the flag form; land managers use their portal | Readers; land managers through the portal | Interaction spec section 5 |

## 6. Human oversight and appeal

- Reviewed by a person before it has an effect: no individual brief. Gate 1 in the conditions-brief human approval gates holds any brief that would state a closure the land-manager portal does not hold, and routes it to the content desk instead of showing it.
- Not reviewed before effect, and why that is acceptable: the briefs themselves, at about 2,400 a day. The compensating controls are the source-link verifier (H2), the no-brief rule below 3 reports (H3), official notices above the brief on upland trails (H1), and the weekly sampled recall in section 7.
- Overrides feed back into the eval set: yes. Every upheld flag becomes a labelled case in `brief-hazards` at the weekly review, owned by Kwame Osei-Lindqvist.

| Output that affects a person | Who can contest it | Entry point | Decided by (not the first decider) | Time target | What the person is told | Recorded where |
|---|---|---|---|---|---|---|
| A brief that summarises an author's report | The report's author | "This misrepresents my report", on the report and on the brief | Content desk moderator; the weekly sampling is done by the contract rangers, a different group | 48 hours | Email: brief regenerated, line removed, or kept, with the reason | Flag log |
| A brief that shows or misses a closure | The land manager | Land-manager portal | Official notices override automatically; wording disputes go to the Content Lead | 1 hour for notices, 24 hours for wording | Portal message | Portal log |
| A walker's report that a brief was wrong | Any walker | "Something wrong?" link | Content desk moderator | 72 hours | In-app note | Flag log, then the eval set |

## 7. Monitoring and the stop condition

| Signal | Definition (computable) | Cadence | Owner | Alert at |
|---|---|---|---|---|
| Sampled hazard recall | Section 4 formula, on 60 briefs a week stratified by report-density band and trail grade, labelled by the contract rangers | Weekly | Kwame Osei-Lindqvist | Below 0.92 in any segment |
| Invented-hazard rate | Hazard lines with no supporting report / all hazard lines, same sample | Weekly | Kwame Osei-Lindqvist | Above 0.02 |
| Flag rate | Flags / thousand brief views | Daily | Ffion Maddox | Above 2.0 |
| Raw-report open rate, upland trails | Sessions opening at least one raw report / sessions viewing a brief | Weekly | Imogen Thwaite | Below 0.15 |
| Incident link | Any rescue-team contact, user report or press enquiry linking an incident to a brief | As it arrives | On-call product lead | Any |

- **Stop condition:** (1) a confirmed case where a brief omitted a hazard that was in its source reports, on a trail where a user or a rescue team reports an injury or a call-out, stops briefs on all upland and mountain trails; (2) sampled hazard recall below 0.90 in any segment for two consecutive weeks stops briefs for that segment
- **Who can call it, alone:** the on-call product lead, the Content Lead, or the assessment owner. The Content Lead owns no growth target; the trail-page weekly active users target sits with the assessment owner. · **What stopping does:** turns off briefs per segment through the kill switch in the conditions-brief guardrails section 4 · **Time to stopped:** 10 minutes, tested in staging on 2026-10-22
- **What users see while stopped:** the raw reports with their dates, under "Summary paused"
- **Who decides a restart, on what evidence:** the assessment owner and the ML Lead together, after a written root-cause note and a section 4 re-run that passes
- **Re-assessment triggers:** a new market (Ireland is on the 2027 roadmap, and as an EU market it needs the legal owner's EU AI Act classification before anything else); Gaelic-language reports; photos added to briefs; any model or prompt change, re-run through model selection and the eval spec

## 8. How this assessment fails

Three of the template's failure rows were caught in drafts of this file.

| Failure | The tell | What to do |
|---|---|---|
| Only users are listed | The first draft of section 2 had three rows, all users | The consequence scan on 2026-09-29 added companions, rescue teams and trailhead businesses |
| Fairness read from the aggregate | The first draft reported 0.928 overall and passed | The density split found the failing segment, and the no-brief rule followed |
| A stop condition nobody will call | The first draft named only the assessment owner, who owns the growth target | The Content Lead and the on-call product lead were added, each able to call it alone |

## Exit gate

This document passes when:

- [x] The header records who made the regulator-applicability call and when, and the answer is that none applies (Rhys Pemberton, 2026-10-09)
- [x] Section 1 lists foreseeable out-of-scope uses with their source, each with a control or a stated reason for none
- [x] Section 2 has at least one non-user row, and the consulted column is filled for every row, "not consulted" included (four non-user rows; rescue-team consultation is an open field)
- [ ] Every harm in section 3 has a severity and a likelihood with a basis, a type, an owner and a residual score (not yet: H4 has no residual score until the Welsh-language cases exist; owner Ffion Maddox, due 2026-12-15. Gate 3 is asked to accept this as an open item, not to treat the box as passed)
- [x] Every row scoring 10 or more, and every severity 5 row, appears in the risk register (R-21 to R-23)
- [x] At least one mitigation is a design change, not a disclaimer (the no-brief rule, the source-link verifier, verbatim closures)
- [x] Every fairness check names its segments, how membership is known, n, the measure's formula and the failing threshold, written before the run (thresholds set 2026-10-01; labelling 2026-10-06 to 2026-10-10)
- [x] Segments below the floor are written as "x of n" and carry an open field with an owner (Welsh-language, 13 of 17)
- [x] Section 6 names an appeal decider who is not the first decider, with a time target, or says N/A with the reason
- [x] The stop condition is observable, at least one role able to call it alone does not own the growth target, and the switch it uses has a test date (2026-10-22)

Signed: Imogen Thwaite, Product Lead, Trail Pages, 2026-10-27
