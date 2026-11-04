# Trust and Safety Harm Model: Lanternway neighbourhood resale, second-city launch

Fills [templates/delivery/trust-safety-harm-model.md](../templates/delivery/trust-safety-harm-model.md). Everything here is invented for this standalone example: Lanternway is a fictional neighbourhood resale marketplace in the UK for furniture, tools, bikes and children's gear, Plover Pay is a fictional licensed payment partner, the people are invented, and every volume, rate, time target, date and identifier is ILLUSTRATIVE, not drawn from any real marketplace or incident. No statement here says what any law requires; obligations are recorded by Lanternway's legal owner in its compliance impact assessment. See the [examples index](README.md).

Lanternway runs in one city today with about 46,000 monthly active users (ILLUSTRATIVE). This release opens a second city and adds neighbourhood groups, the product's first surface where one person's post reaches many people at once. Buyers pay cash on collection or through Plover Pay's checkout; Lanternway never holds funds, and the partner's obligations are recorded in the compliance impact assessment, not here. Gate 5 is planned for 2026-11-06.

**Surfaces in scope:** listings, seller profiles and ratings, buyer and seller chat, reviews, neighbourhood groups (new in this release)
**Markets:** UK; legal obligations recorded in the Lanternway compliance impact assessment by Marisol Ekdahl, Legal Counsel, on 2026-10-12
**Owner:** Tobias Renwick, Trust and Safety Lead · **Reviewed with:** Precious Abara, Support Lead; Marisol Ekdahl, Legal Counsel · **Date:** 2026-10-30

## 1. Actors

| Actor | Type (bad actor / victim / bystander) | What they want, or stand to lose | How they reach the surface | Account needed to be harmed? |
|---|---|---|---|---|
| Payment scammers sending fake payment screenshots or off-platform links | Bad actor, financially motivated | A buyer's money, or a seller's goods | Fresh accounts, chat | Yes, the victim has one |
| Sellers of stolen tools and bikes | Bad actor, financially motivated | Cash for stolen goods | Listings | No: the owner of the goods |
| Harassers after a sale | Bad actor, personally motivated | Continued contact, sometimes at the other person's home | Chat, the collection address | No: household members |
| Rating rings | Bad actor, organised | Inflated ratings that sell more | Reviews between linked accounts | Yes, the misled buyer |
| Sellers of prohibited goods (bladed items, recalled child car seats) | Bad actor, opportunistic or financially motivated | A sale | Listings | No: the child in the car seat |
| Group raiders | Bad actor, organised or personally motivated | Flooding a group, or targeting one member | Group posts | Yes |
| Buyers and sellers | Victim | Money, goods, safety at collection | Every surface | Yes |
| Owners of stolen goods | Bystander | Their property | They find it listed | No |
| Household members at a collection address | Bystander | Safety, and the privacy of the address | The address a seller shares for collection | No |
| People pictured in listing photos | Bystander | Privacy | Faces or family photos in the background of a listing | No |

## 2. Severity tiers

All targets are ILLUSTRATIVE, set by Tobias Renwick on 2026-09-15.

| Tier | What qualifies | Example | First-action target (p90) | Who may act | Automated action alone allowed? |
|---|---|---|---|---|---|
| T1 | Threat of violence, someone in danger at a collection, child sexual exploitation | "I know where you live" after a refund dispute | 1 hour | On-call trust and safety rota of four, 24 hours | No: an automated hold is allowed, a person confirms |
| T2 | Payment scam, stolen goods, targeted harassment, home address exposed, recalled child safety products | A buyer is sent a payment link to a look-alike site | 12 hours | T2 reviewers | Holding a message, yes; suspending an account, no |
| T3 | Misdescribed items, spam, fake reviews | A "solid oak" table that is veneer | 72 hours | T3 reviewers | Removing exact-duplicate spam, yes |
| T4 | Wrong category, duplicate listings | A bike listed under furniture | 7 days | Automated, sampled weekly | Yes |

## 3. Abuse vectors and controls

| ID | Vector | Actor, victim | Tier | Prevent | Detect | Respond | Control owner | Evidence the control works |
|---|---|---|---|---|---|---|---|---|
| TS-1 | Off-platform payment link or fake payment screenshot in chat | Scammer, buyer or seller | T2 | Warning before a link or phone number is sent in the first three messages of a chat; "Paid" status shown only from Plover Pay, and sellers told to wait for it | Link-pattern classifier, precision 0.81 on 400 labelled messages (2026-09-18); report on every message | Hold the message, warn the recipient, restrict the sender pending review, statement of reasons | Dara Quennell, Trust and Safety PM | Red-team pass on the warning, 2026-10-08; classifier precision from the dated set |
| TS-2 | Stolen tools and bikes listed | Seller of stolen goods, owner | T2 | New sellers limited to 3 listings a week in tools and bikes for their first 30 days; optional frame or serial number field shown to buyers | Image reuse matched against other listings; reports from owners | Remove the listing, preserve listing and account data for a police request handled by Legal, ban on a second confirmed case | Tobias Renwick | Assumed for owners without an account, because their report route is not built: gap G1 |
| TS-3 | Harassment after a sale | Harasser, buyer or seller and their household | T2, or T1 on a threat or a visit | Addresses never appear on profiles and are shared in chat only by the seller's choice; chat closes 14 days after a completed sale unless both reopen it | Block and report; repeat-contact signal for the same pair after closure | Block, restrict, suspend; T1 escalation on a threat or a visit | Tobias Renwick | Chat closure passed UAT, 2026-10-21 |
| TS-4 | Unsafe collection meeting | Bad actor, buyer or seller | T1 | Suggested public collection points (libraries, supermarket car parks) in the listing flow; "share my collection" with a contact | Report categories "I felt unsafe" and "I was threatened" route to the T1 queue | Restrict the reported account at once, show emergency guidance to the reporter, police liaison by the on-call lead | Tobias Renwick | T1 routing tested 2026-10-21; collection points chosen in 0.29 of city-1 collections |
| TS-5 | Prohibited items: bladed items, recalled child car seats | Seller, buyer and child | T2 | Prohibited-items list shown at listing; the car-seat category requires the model name and shows a recall-check link | Keyword and image classifier at listing, recall 0.88 on 250 labelled prohibited listings (2026-09-30); reports | Remove, warn, ban on repeat | Dara Quennell | Classifier recall from the dated set |
| TS-6 | Rating rings | Ring, buyers | T3 | A review is possible only after a sale completed in the app | Reciprocal-review graph among accounts sharing devices or payment instruments | Remove the reviews, reset the ratings, restrict the accounts | Dara Quennell | Assumed: the graph signal is not tuned, gap G2 |
| TS-7 | Raid on a neighbourhood group | Raiders, group members | T2 | New accounts cannot post in groups for 7 days; group admins can switch on post approval | Report velocity, 10 reports on one post inside 30 minutes | Auto-hide the post above the threshold, slow mode for the group, review | Tobias Renwick | Tabletop exercise, 2026-10-24; also row FS-6 in the Lanternway failure scenarios |
| TS-8 | Taken-over account messaging buyers | Attacker, buyers | T2 | Controls are in the security architecture threat walk, not repeated here | New device plus a change of payout details | Lock the account, notify counterparties in open chats, restore | Security Lead | Per the security architecture review, 2026-10-02 |

## 4. Reporting and appeals flow

- Report entry points: on every listing, profile, message, group post and review, in two taps · Reporting without an account: designed for owners of stolen goods and household members, not built; gap G1 carries an interim route
- Report categories, each mapped to a tier: unsafe or threatened (T1); scam or payment, stolen item, harassment, prohibited item (T2); misleading listing, fake review, spam (T3); other (T3 unless a reviewer re-tiers it)

| Step | Who or what acts | Time target | What the person is told |
|---|---|---|---|
| Report received | System | Immediate | T1 categories: "Thanks. Safety reports are reviewed first. If you are in danger now, call 999." Others: "Thanks. We will tell you what we decide." |
| Triage and routing | Category plus signals, to the T1, T2 or T3 queue | Under 1 minute | Nothing further |
| Decision | Reviewer for the tier | Per section 2 | Nothing until the outcome |
| Notice to the person actioned | Reviewer, from a template | At decision | Statement of reasons: the rule, what was found, the action, and the appeal button |
| Outcome to the reporter | System | At decision | That action was or was not taken, without the other account's sanction detail |
| Appeal | A senior T2 reviewer who did not make the first decision | 72 hours; appeals open for 14 days | The outcome, and that it is final |
| Referral outside the company | On-call trust and safety lead for T1; Legal for police data requests | T1 inside the hour | Where it is safe, that a referral was made |

## 5. Moderation operating model and queues

Volumes are the city-1 daily average plus the second-city forecast (ILLUSTRATIVE). Buffer 30 percent, covering breaks, training, double review and absence (ILLUSTRATIVE). Reviewer hours per day = items per day x share needing a human x handle time / 60.

| Queue | Tiers and vectors routed here | Hours covered | Items per day | Share needing a human | Handle time (minutes) | Reviewer hours per day | Staffed hours at 30 percent buffer | Staffed hours at 10x volume | First-action target p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| Urgent | T1, any vector | 24 hours, on-call rota | 6 | 1.0 | 20 | 2.0 | 2.6 | 26.0 | 20 minutes / 1 hour |
| Standard | T2: TS-1, 2, 3, 5, 7, 8 | 08:00 to midnight | 140 | 0.70 | 6 | 9.8 | 12.7 | 127.4 | 3 hours / 12 hours |
| Low | T3 and T4: TS-6, misleading listings, spam | 09:00 to 17:00 weekdays | 420 | 0.40 | 2.5 | 7.0 | 9.1 | 91.0 | 24 hours / 72 hours |

The standard queue worked through: 140 x 0.70 x 6 / 60 = 9.8 hours, x 1.3 = 12.7 staffed hours. At ten times the volume: 1,400 x 0.70 x 6 / 60 = 98 hours, x 1.3 = 127.4, about 17 reviewers on 7.5-hour shifts for that queue alone. Linear hiring is not the plan at that scale; gap G4 holds the automation plan.

- Surge plan, when the oldest standard item passes 8 hours or depth passes 150: page the on-call trust and safety lead, extend the TS-1 warning to every message with a link, and pause the low queue
- Decision quality: 5 percent of standard decisions double-reviewed each week, agreement target 0.90; the policy text is owned by Tobias Renwick
- Reviewer wellbeing: urgent-queue reviewers rotate after two hours, and the employee support service is offered to every reviewer

## 6. Transparency and metrics

| Metric | Definition (computable) | Cut by | Target | Owner | Published externally? |
|---|---|---|---|---|---|
| Prevalence | Violating listing and group-post views / all such views, from 1,000 randomly sampled views labelled each week; reported with a 95 percent Wilson interval | Surface, category | Below 0.010 (ILLUSTRATIVE), judged on a four-week pooled sample | Dara Quennell | Yes, twice yearly |
| Time to first action | Report or detection timestamp to first action timestamp; p50 and p90 | Tier | Per section 2 | Tobias Renwick | Yes |
| Proactive rate | Items actioned before any user report / all items actioned | Vector | 0.50 by the end of Q2 2027 (ILLUSTRATIVE) | Dara Quennell | Yes |
| Appeal overturn rate | Appeals reversed / appeals decided | Tier, reviewer | Below 0.10 (ILLUSTRATIVE) | Tobias Renwick | Yes |
| Repeat-offender rate | Actioned accounts actioned again within 90 days / actioned accounts | Vector | Falling quarter on quarter | Dara Quennell | No |
| Counter-metric | Blocks / thousand chats | City | Not above the city-1 baseline after launch | Precious Abara | No |

Latest city-1 reading, week of 2026-10-19 (ILLUSTRATIVE): prevalence 9 of 1,000 sampled views, 0.009, with a 95 percent interval of 0.005 to 0.017; urgent p90 52 minutes; standard p90 9.5 hours; low p90 61 hours; proactive rate 0.38; appeal overturn rate 11 of 64, 0.17. The prevalence interval's upper bound is above the target, so one week cannot show the target is met, which is why the target is judged on the pooled sample. The overturn rate is above target: most reversals were TS-1 restrictions on sellers who had pasted their own shop's link, and the reviewer guidance was rewritten on 2026-10-28.

- External transparency: a twice-yearly transparency note with actions by category and tier, time to first action p50 and p90 by tier, appeals and overturns, and prevalence with its interval; signed by Tobias Renwick and Marisol Ekdahl
- What a user can see about actions on their own account: an account standing page listing each action, its reason and the appeal button

## 7. How this model fails while looking complete

Three of the template's failure rows were found in review of this file.

| Failure | The tell | What to do |
|---|---|---|
| Only users can report | The first draft had no entry point for an owner of stolen goods without an account | Designed a logged-out route; until it is built, support's contact form takes these reports (gap G1) |
| Staffed for launch day | The first draft of section 5 had no 10x column | The arithmetic shows 127.4 staffed hours a day for the standard queue at ten times; gap G4 |
| The tier set by the typical case | Harassment after a sale sat in T3 because most cases are rude messages | Re-tiered to T2, and to T1 on a threat or a visit |

## 8. Gaps carried to launch

| Gap | Vector ID | Ship with it open? Why | Owner | Close-by date |
|---|---|---|---|---|
| G1: logged-out reporting for owners of stolen goods and household members is designed, not built | TS-2, TS-3 | Yes, on condition that support's contact form accepts these reports with a T2 tag and routes them within 4 hours in the meantime | Dara Quennell | 2026-12-15 |
| G2: the rating-ring signal is not tuned, so TS-6 detection is assumed | TS-6 | Yes: T3, misleading but low loss | Dara Quennell | 2027-01-31 |
| G3: overnight urgent cover is one person from a rota of four, with no second person behind them | TS-3, TS-4 | Accepted as a waiver by Wren Penhallow, VP Product, for the first eight weeks of the second city, decision-log D-31, because the trust and safety lead owns the rota and should not waive its own gap; a fifth rota member starts 2027-01-05 | Tobias Renwick | 2027-01-05 |
| G4: no automation plan for the standard queue at ten times today's volume | All T2 | Yes: launch volume is far below that line | Dara Quennell | 2027-01-31 |

## Exit gate

This document passes when:

- [x] Section 1 names bad actors by kind, victims on both sides, and at least one bystander who needs no account to be harmed (owners of stolen goods, household members, people pictured)
- [x] Every vector has a tier set on its worst credible outcome, and every T1 and T2 vector has a prevent control, not only detection
- [x] Every control has evidence that it works, or an "assumed" that appears as a section 8 gap with an owner and a date (TS-2 as G1, TS-6 as G2)
- [x] The reporting flow works for a person with no account, or says why not (not built; G1 names the interim route)
- [x] Every flow step states what the person is told, and appeals go to a different reviewer
- [x] Section 5 shows the staffing arithmetic at today's volume and at ten times, with the buffer written as a number
- [x] Prevalence and time to first action are defined, cut by tier, and owned
- [x] Every vector that could flood a queue or take a surface down has a matching row in failure-scenarios.md (TS-7 as FS-6)
- [x] No T1 vector ships with an open gap unless the gap row names who accepted it and why (G3, accepted by Wren Penhallow, D-31)

Signed: Tobias Renwick, Trust and Safety Lead, 2026-10-30
