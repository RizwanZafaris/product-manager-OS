# Acquisition Integration Plan: Calderbank acquires Tinsmith

Fills [templates/planning/acquisition-integration-plan.md](../templates/planning/acquisition-integration-plan.md). Everything here is invented for this standalone example: Calderbank is a fictional accounts-payable automation company, Tinsmith a fictional supplier-onboarding company it acquired, and Halvorsen Freight a fictional Tinsmith customer. Every number, name, date, contract term and quotation is ILLUSTRATIVE, not drawn from any real company or deal. See the [examples index](README.md).

**Owner:** Ana Kovač, Chief Product Officer, Calderbank · **Deal sponsor:** Rafael Osei, Chief Revenue Officer · **Acquired-side product lead:** Lior Ben-Ami, Head of Product, Tinsmith · **Integration lead:** Dev Pillai
**Close date (day 1):** 2026-09-01 · **Day 100:** 2026-12-09 · **Last updated:** 2026-10-27 (day 57)

## 1. The deal thesis, restated as testable product hypotheses

- Thesis as approved: "Tinsmith's supplier portal removes the supplier-data errors behind most of our invoice exceptions, its 1,100 customers are a ready cross-sell base for Calderbank AP, and retiring Tinsmith Pay and its separate hosting pays for the integration."
- Source: Calderbank board paper BP-2026-07 and its business case, both in the corporate development workspace, not tracked in this repository; the case was built on the [business case template](../templates/planning/business-case.md)
- Counterfactual: the May [build, buy, partner, or wait](../frameworks/strategy/build-buy-partner.md) run scored building a supplier portal at 18 months with no customer base, and a partnership with Tinsmith as giving the portal without the cross-sell base or the team

| # | Thesis claim | Kind | Hypothesis | Threshold and date | Kill signal | Owner |
|---|---|---|---|---|---|---|
| H1 | "a ready cross-sell base" | Cross-sell revenue | We believe offering Calderbank AP to Tinsmith customers with more than 200 suppliers will convert, measured by AP contracts signed in the Tinsmith base | 88 accounts, 8% of 1,100, by 2027-09-01 | Fewer than 10 qualified opportunities by day 120 (2026-12-29) | Rafael Osei |
| H2 | "removes the supplier-data errors behind most of our invoice exceptions" | Capability | We believe supplier self-onboarding through the portal will cut exceptions for joint customers, measured by exceptions as a share of invoices processed | From 6.0% to 4.0% within 90 days of enablement, on the first 10 joint customers | Less than 0.5 points of improvement after 90 days | Lior Ben-Ami |
| H3 | "pays for the integration" | Cost removed | We believe retiring Tinsmith Pay and Tinsmith's hosting removes run cost, measured by annualized run cost | $900,000 a year saved by 2027-12-01 | Fewer than 60% of Pay customers migrated by 2027-03-01 | Joon Park, Calderbank Payments PM |
| H4 | Not in the quoted thesis; in the board paper's appendix | The team | We believe the five engineers who built Tinsmith's supplier-matching engine stay, measured by retention | 4 of 5 at month 12 | Two leave before month 6 | Ana Kovač |

"Most of our invoice exceptions" was not testable as written: the board paper cites no share. H2 tests the part that can be measured, and the claim's "most" is recorded here as unsupported.

## 2. Product and customer overlap map

| Our product line | Their product line | Overlap | Same buyer and segment | Shared customers |
|---|---|---|---|---|
| Calderbank AP (invoice capture and approval) | Tinsmith Portal (supplier onboarding) | Adjacent | Yes | 130, Tinsmith revenue $1.2M |
| Calderbank Payments | Tinsmith Pay (supplier payments through a partner bank) | Same job | Yes | 41 of Pay's 142 customers |
| None | Tinsmith Forms API (supplier forms embedded by software companies) | None | No | 0 |

| Segment | Their customers | Ours | Both | Terms that matter |
|---|---|---|---|---|
| Mid-market finance teams | 1,040, $7.1M | 2,400, $61M | 130 | 210 Tinsmith customers have prices locked to 2028; 12 hold a termination right on change of control |
| Software companies (Forms API) | 60, $0.8M | 0 | 0 | None material |

Matching rule used: email domain plus billing-entity tax ID, extract of 2026-09-18, run by Dev Pillai in revenue operations. Matching on company name alone had found 171 shared customers; 41 of those were different legal entities with similar names.

## 3. Integrate, keep separate, or sunset: one decision per product line

| Product line | Decision | Hypothesis it serves | What would reverse it | Decider | Decision date | Next document |
|---|---|---|---|---|---|---|
| Tinsmith Portal | Integrate | H1, H2 | The H2 kill signal: integration then stops at sign-on and billing, and the portal is kept separate | Ana Kovač | 2026-09-29 | Roadmap rows R-31 to R-34 |
| Tinsmith Pay | Sunset | H3 | Calderbank Payments cannot serve the customers who pay suppliers in currencies it does not support by 2027-06-30 | Ana Kovač | 2026-09-29 | A filled [sunset plan](../templates/operate/sunset-eol-plan.md), due 2026-11-21 |
| Tinsmith Forms API | Keep separate | None. Kept because it is profitable, its buyer is outside our segment, and its team of three needs nothing from ours | Its team cannot be retained, or it starts to need Calderbank engineering time | Ana Kovač | 2026-09-29 | Decision memo DM-12, review at day 180 |

- Sunset announcements: Tinsmith Pay was to be announced on day 45, 2026-10-15. It slipped to 2026-11-24 [OPEN: 31 Pay customers pay suppliers in four currencies Calderbank Payments does not support; owner Joon Park, decision on adding the currencies or extending Pay for those 31 customers due 2026-11-14]. A holding statement went to all 142 Pay customers on 2026-10-15: no change to Tinsmith Pay before 2027-06-30, and at least six months' notice of any change, which is the notice their contracts require.

## 4. Customer commitments inherited

| Customer or segment | Commitment | Where it is written | Due | Disposition | Owner |
|---|---|---|---|---|---|
| Halvorsen Freight | SAML single sign-on for the portal | Order form addendum, clause 4 | 2027-03-31 | Keep: delivered by the day-60 sign-on milestone | Lior Ben-Ami |
| 210 early customers | Price locked until their 2028 renewal | Early-adopter clause in their order forms | 2028 renewals | Honour | Rosa Ilić, finance partner |
| 95 EU customers | Processing inside the EU | Their data processing agreements | Ongoing | Keep: Calderbank's EU region only; no migration out of the EU | Kwame Asante, data protection officer |
| 12 customers, $640,000 a year | May terminate within 60 days of change-of-control notice | Master agreements, change-of-control clause | Window closed 2026-10-31 | Retention call with each by day 14: 11 stayed, 1 terminated ($38,000 a year) | Beatrice Nkem |
| Tinsmith Pay customers | 99.9% monthly availability | Pay service-level schedule | Until retirement | Honour, then retire | Mateo Silva |

## 5. Technical and data integration risks

| Area | Their current state | Ours | Integration risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|---|
| Identity and sign-on | Own passwords plus one social sign-in | SAML and OIDC | Wrong account linking for the 130 shared customers | Medium | High | Link only on verified domain plus admin confirmation | Wen Zhao |
| Billing and entitlements | Separate billing system | Calderbank billing | Double billing during transition | Medium | Medium | Tinsmith billing stays until each customer's renewal | Rosa Ilić |
| Shared data entities | Supplier records, own matching engine | Supplier records in AP | Duplicate suppliers when portal data reaches AP | High | High | Tinsmith's engine becomes the matcher; AP reads its output | Yusuf Demir |
| Data residency and permitted use | EU and US hosting | EU and US regions | Using Tinsmith customers' supplier data inside Calderbank AP | Medium | High | [OPEN: Tinsmith's terms permit processing "to provide the Services"; whether that covers showing a customer's supplier records inside Calderbank AP needs counsel's reading; owner Kwame Asante, by 2026-11-20. No portal data moves into AP before then] | Kwame Asante |
| Security posture and open findings | Two medium findings from diligence | | Findings inherited into our audit scope | High | Medium | Both fixed by 2026-11-30 | Mateo Silva |
| Infrastructure and hosting | A different cloud provider | Our provider | Two platforms to run and pay for | Certain | Medium | No migration before day 180; H3 counts the saving only after it | Wen Zhao |
| Third-party and open-source licences | One copyleft component in Forms API, flagged in diligence | | Obligations if Forms API code is reused in our products | Low | Medium | Forms API stays separate; legal review by 2026-11-15 | Hamid Farouk, counsel |
| Regulated partner held by the target | Pay runs through a partner bank agreement | Calderbank Payments has its own | Any change to Pay needs the bank's consent | Certain | High | [reg-gap-check](../skills/reg-gap-check/SKILL.md) run before the Pay sunset plan is filed | Joon Park |
| Systems only one person understands | Pay's bank integration (Mateo Silva); the matching engine (two engineers) | | Knowledge leaves with the person | Medium | High | Section 7 transfer dates | Ana Kovač |

## 6. The first 100 days

| By | Milestone | Owner | Status |
|---|---|---|---|
| Day 1, 2026-09-01 | A joint letter to every customer names one support contact per product; support routing unchanged; customer-facing changes to Tinsmith products frozen for 30 days except security fixes | Ana Kovač | Done |
| Day 30, 2026-09-30 | Overlap map built from matched data; one decision per product line in the decision log; a retention conversation held with each person in section 7 | Ana Kovač | Done |
| Day 30, 2026-09-30 | Commitments register complete from contracts and order forms | Hamid Farouk | Done 2026-10-04, four days late: 300 order forms read by hand, with no clause search available |
| Day 60, 2026-10-30 | Calderbank sign-on live for the portal; first 10 joint customers enabled for H2 with their baselines recorded; 12 Calderbank account executives certified on the portal | Lior Ben-Ami | In progress: sign-on live 2026-10-22; 7 of 10 joint customers enabled |
| Day 60, 2026-10-30 | Tinsmith Pay sunset announced | Joon Park | Slipped to 2026-11-24; see section 3 |
| Day 100, 2026-12-09 | Combined roadmap published; the matching engine's design written down and one change to it shipped by a Calderbank engineer; H1 leading read taken | Ana Kovač | Planned |

## 7. Retention of key people

| Person and role | Why they matter | Retention terms | Their stated concern | Relationship owner | Flight signal to watch | Second person, and transfer date |
|---|---|---|---|---|---|---|
| Mateo Silva, Tinsmith CTO | Built the hosting and the partner-bank integration behind Pay | 18-month bonus, half paid at month 9 | Wants to report to Calderbank's CTO, not to a VP | Ana Kovač | Stops attending the architecture review | Wen Zhao, paired since 2026-09-14; Pay runbooks handed over by 2026-12-15 |
| Yusuf Demir and Clara Holm, matching engineers | The only two people who understand the matching engine (H2, H4) | Equity refresh vesting over 24 months | That the engine will be rewritten into Calderbank's stack and their work discarded | Lior Ben-Ami | Asking to move off the engine | Priit Kask: design document by 2026-11-30, one shipped change by day 100 |
| Beatrice Nkem, Tinsmith head of customer success | Holds the relationships with the 12 change-of-control accounts and the Pay customers | 12-month bonus | Her team being folded into Calderbank's success team under a new manager | Ana Kovač | Declining the Pay customer calls | Account plans for the top 50 accounts in the CRM by 2026-11-15 |
| Oskar Lind, Forms API lead | Runs Forms API with two others | None | That keep separate means sunset later | Ana Kovač | Asking about transfers | Told the keep-separate decision in writing on 2026-09-29; review at day 180 |

The other three matching engineers have standard retention terms and are tracked as a group under H4.

## 8. Metrics that would show the thesis was wrong

| Hypothesis | Leading signal | Lagging signal | Threshold that means wrong | Review date | Who calls it |
|---|---|---|---|---|---|
| H1 | Qualified AP opportunities in the Tinsmith base: 15 by day 100, 25 by day 120 | AP contracts signed in the Tinsmith base, 88 by 2027-09-01 | Fewer than 10 qualified by day 120 | 2026-12-29 | Rafael Osei |
| H2 | Exceptions as a share of invoices for the first 10 joint customers, 90 days after enablement | Support tickets per 1,000 invoices for joint customers at month 12 | Less than 0.5 points of improvement at 90 days | 2027-02-01 | Lior Ben-Ami |
| H3 | Share of Pay customers migrated, 60% by 2027-03-01 | Annualized run-cost saving at month 15 | Under 60% at month 6, or under $600,000 at month 15 | 2027-03-01 | Joon Park |
| H4 | Matching engineers still here at month 6, 5 of 5 | 4 of 5 at month 12 | Two leave before month 6 | 2027-03-01 | Ana Kovač |

| Guardrail | Baseline at close | Threshold | Owner |
|---|---|---|---|
| Acquired-customer churn | 1.1% of Tinsmith logos a month, six months before close | Above 2.0% in any month | Beatrice Nkem |
| Acquired-team voluntary attrition | 0 leavers in the quarter before close, team of 38 | More than 3 leavers in the first six months | Ana Kovač |
| Share of Calderbank engineering capacity spent on integration | Planned 15% | Above 25% for two consecutive months | Sunita Rao, VP Engineering |

Readings so far: Tinsmith logo churn was 1.4% in September and 1.9% in October, close to the threshold, with the change-of-control termination inside October's figure. Integration took 18% of engineering capacity in September and 23% in October. Both are on the agenda for the day-60 review; neither has crossed its line. All figures ILLUSTRATIVE.

## 9. How this plan fails

| Failure | The tell | What to do |
|---|---|---|
| Sunset by rumour | Pay customers asked support about a shutdown in the first two weeks, before any decision | The 2026-10-15 holding statement, with a date and a notice period, while the currency question stays open |
| Integration eats the core roadmap | October's capacity reading at 23%, two points under the line | Read monthly beside the [capacity plan](../templates/planning/capacity-plan.md); a second month above 25% pauses roadmap rows R-33 and R-34 |
| Key people leave at the vest date | Mateo Silva's first bonus payment falls at month 9, 2027-06-01 | Pay runbooks transferred by 2026-12-15, six months before the payment |

## Exit gate

This plan is ready to run when:

- [x] The thesis is quoted as approved, with its source, and every claim in it is a hypothesis with a metric, a threshold, a date, a kill signal and an owner, or is marked as untestable (the "most of our invoice exceptions" share is marked unsupported)
- [x] The overlap map comes from matched data, and the matching rule and extract date are written down
- [x] Every acquired product line has one decision, integrate, keep separate or sunset, with the hypothesis it serves, what would reverse it, a decider and a date (Forms API serves no hypothesis, and says so)
- [x] Every sunset decision names its filled sunset plan, or the date that plan is due (Tinsmith Pay, due 2026-11-21)
- [x] Inherited commitments were read from contracts and order forms, and each has a disposition and an owner
- [ ] Data residency and permitted use were checked against the acquired company's own customer terms before any migration was scheduled (residency checked; permitted use open with counsel until 2026-11-20, and no portal data moves until then)
- [x] Every first-100-days milestone is a checkable condition with an owner, and slipped milestones show their new date and reason
- [x] Every key person is named, with their own stated concern and a second person who will hold their knowledge
- [x] Every hypothesis has a leading signal readable by day 180 and a named person who calls it wrong, and the three guardrails have baselines

Signed: Ana Kovač, Chief Product Officer, 2026-10-27, with the permitted-use and currency questions open and owned
