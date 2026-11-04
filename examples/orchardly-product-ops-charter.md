# Product Ops Charter: Orchardly product group

Fills [templates/execution/product-ops-charter.md](../templates/execution/product-ops-charter.md). Everything here is invented for this standalone example: Orchardly is a fictional procurement and supplier-ordering platform for restaurant groups, its teams and people are invented, and every count, amount and date is ILLUSTRATIVE, not drawn from any real company. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**Function lead:** Elsa Marangoni · **Reports to:** Imogen Harrow, head of product · **Chartered:** 2026-10-20 · **Review by:** 2027-04-19 · **Status:** Chartered
**People:** 2 (Elsa Marangoni, lead; Kofi Boakye, analyst) · **Tool budget:** GBP 48,000 a year, pending approval (see the open items) · **Product teams served:** 8, with 9 PMs

## 1. The problems this function exists to own

The assessment dimensions are from the [product operating model assessment](../frameworks/assessment/product-operating-model-assessment.md) the product leadership team scored on 2026-09-30, where dimension 4 (risk retired before commitment) and dimension 7 (outcome accounting) both scored 1.

| # | Problem area | The symptom, observed and dated | Assessment dimension it weakens | Cost of leaving it, in one line |
|---|---|---|---|---|
| 1 | Tooling | Tooling audit, 2026-09-14: eight teams on five feedback and roadmap tools with no shared tags, and 23 paid seats held by people who had left | None directly | About GBP 9,000 a year in idle seats, and no way to count a request across teams |
| 2 | Insights and feedback pipeline | Support logged 1,140 product-tagged tickets in Q3 2026; a 200-ticket sample read on 2026-10-05 found 61 percent reached no product team. The supplier catalogue team learned of its most common complaint from a lost-deal note on 2026-08-27 | 4, risk retired before commitment | Teams commit a quarter before the cheapest evidence reaches them |
| 3 | Process and rituals | The weekly product review's pre-read went out 48 hours ahead in 3 of 12 weeks in Q3 | 7, outcome accounting | The review slides into a demo, and decisions get made on polish |
| 4 | Launch coordination | On 2026-09-08 two launches emailed the same restaurant groups the same morning; support learned of one from customers | None directly | Customers confused, support blindsided, one launch's metric polluted by the other |
| 5 | Data and metrics hygiene | "Active buyer" has three definitions across four dashboards; on 2026-10-01 the board update and the growth review disagreed by about 900 buyers | 7, outcome accounting | Two numbers for one question, and no decision until someone reconciles them by hand |

## 2. What it owns

| Area | What it owns | Done when (observable) | Related artifact |
|---|---|---|---|
| Tooling | Selection, administration, licences, access and retirement of the product toolset | One feedback tool and one roadmap tool across all eight teams by 2027-02-01, and no seat held by a leaver for more than 30 days | Tool inventory, kept by Kofi Boakye |
| Insights and feedback pipeline | Intake from support, sales and research; tagging; routing to the owning team; a monthly synthesis per team | Every product-tagged ticket routed to an owning team, and each team receives its synthesis by the fifth working day of the month | [feedback program](../templates/operate/feedback-program.md) |
| Process and rituals | The shared template set, the planning calendar, the product review's logistics and its 48-hour pre-read | Pre-read out 48 hours ahead in at least 10 of 12 weeks; one template set, versioned | [decision log](../templates/execution/decision-log.md) |
| Launch coordination | The launch calendar, orchestrating readiness checks, timing customer emails across teams | One calendar every team and support reads, and no two customer emails to the same segment on one day without a logged decision | [release readiness](../templates/delivery/release-readiness.md), [launch comms plan](../templates/delivery/launch-comms-plan.md) |
| Data and metrics hygiene | Custody of the metrics dictionary, versioned definition changes, the dashboard inventory and its retirements | Every metric in the board update and the product review has a current dictionary entry | [metrics dictionary](../templates/operate/metrics-dictionary.md), [dashboard spec](../templates/operate/dashboard-spec.md) |

## 3. What it explicitly does not own

| Not owned | Who owns it | Where the line sits |
|---|---|---|
| What to build, and in what order | Each product team's PM | Product ops brings the evidence; the team decides |
| The roadmap's content | Imogen Harrow and the PMs | Product ops runs the calendar the roadmap is reviewed on |
| Any go or no-go | The decider named in each release readiness copy | Product ops runs the checklist and never holds the vote |
| Research studies | Mei Takeda, research lead | Product ops runs intake and the research repository; Mei's team designs and runs studies |
| Pipelines, warehouses, instrumentation code | Arjun Bhatt, data engineering lead | Product ops owns definitions; data engineering owns the plumbing |
| Messaging and positioning | Clara Jensen, product marketing lead | Product ops supplies the launch calendar |
| Managing or appraising PMs | Imogen Harrow | Product ops reviews no one's performance |
| Replying to customers about feature requests, asked of product ops by Nikolai Sorensen, VP sales, on 2026-10-06 | The account executive, with the owning PM's answer | Declined in writing on 2026-10-09. Product ops routes the request and tells the account executive which PM owns it; it never promises a feature or a date |

## 4. Customers

| Customer | What they get | What they must give | Channel |
|---|---|---|---|
| Product managers (9) | Routed feedback and a monthly synthesis, tool access, the launch calendar, the template set | An owner name for every feedback tag in their area; launch dates at least 10 working days ahead | Request form in the product-ops channel |
| Design and engineering leads | The launch calendar and the readiness checklist, run for them | Readiness status per launch, five working days before the date | Request form |
| Product leadership | A pre-read that arrives on time; a monthly metric consistency report | A decision within 5 working days on any request that fits no area in section 2 | Weekly one-on-one between Elsa and Imogen |
| Support, sales and customer success | One intake path, and a reply naming the team that owns each item | Tickets and lost-deal notes in the intake format | Intake form inside the support tool |

## 5. Service levels

| Service | How to request it | Response | Fulfilment | Measured how | A breach goes to |
|---|---|---|---|---|---|
| Tool access or licence | Request form | 1 working day | 3 working days | Form timestamps, read monthly | Elsa Marangoni, then Imogen Harrow |
| Feedback item routed to its owning team | Automatic from intake | Automatic acknowledgment | 5 working days from intake | Routing timestamps in the feedback tool, read weekly | The owning PM's lead |
| Metric definition change | Request form | 2 working days | Logged and versioned before any dashboard changes, within 10 working days | Monthly diff of dashboards against the dictionary | Arjun Bhatt and Imogen Harrow jointly |
| Launch added to the calendar | Calendar form | 1 working day | 2 working days | Launches that reached the calendar fewer than 10 working days ahead, counted monthly | Elsa Marangoni |
| Change to a shared template or ritual | Proposal in the template set | 2 working days | Published with 10 working days' notice | Changes with notice over all changes, per quarter | Imogen Harrow |

## 6. How its value is measured

| Indicator | Baseline, dated | Target by the review date | Counterweight | Source |
|---|---|---|---|---|
| PM hours a week on operational admin | 6.5 hours, survey of 2026-10-12, 8 of 9 PMs answering | 4.0 hours | PM satisfaction with the service, 1 to 5 (no baseline yet, see the open items) | Quarterly time survey |
| Feedback items routed to an owner within 5 working days | Time to route was not recorded before; 39 percent of the 200-ticket sample reached any team at all, 2026-10-05 | 85 percent | Share later re-routed as misfiled, below 10 percent | Feedback tool routing log |
| Launches with readiness complete five working days before the date | 2 of 7 launches in Q3 2026 | At least 6 of every 7 | Launch steps added this quarter, none net | Launch calendar |
| Reported metrics with a current dictionary entry | 11 of 34, inventory of 2026-10-15 | 30 of 34 | Dashboards retired against dashboards added; 0 retired in Q3 | Dashboard inventory |

Retired this quarter: planned, the Monday launch-sync meeting, replaced by the launch calendar by 2026-12-14; and the shared intake spreadsheet, once the feedback tool routes automatically.
If the indicators have not moved by the review date: Imogen Harrow decides between re-scoping to the areas that moved, re-staffing, or winding the function down, and records the decision in the product group's decision log.

Open items:

- [OPEN: PM satisfaction cannot have a baseline before the service exists. The first reading is taken on 2027-01-18 and its target set then. Owner: Elsa Marangoni.]
- [OPEN: the GBP 48,000 tool budget awaits finance approval. Until it lands, the tooling area in section 2 cannot buy the shared feedback tool, and its 2027-02-01 date is at risk. Owner: Imogen Harrow, due 2026-11-30.]

## Exit gate

Done when every box is honestly ticked. This file declares no gate; the function it charters serves every stage.

- [x] Every problem in section 1 has a dated symptom and, where one applies, the assessment dimension it weakens
- [x] Every area in section 2 has a "done when" someone outside the function could check
- [x] Section 3 names an owner and a handoff line for every excluded area, including at least one request the function has already been offered and declined (feature-request replies, declined 2026-10-09)
- [x] Every customer in section 4 has what they get and what they must give
- [x] Every service level has a response, a fulfilment, a measurement method and a breach path
- [x] Every indicator in section 6 has a dated baseline taken before the function started, a target and a counterweight, or an open item saying why the baseline cannot exist yet (PM satisfaction, open until 2027-01-18)
- [x] The retirement rule and the consequence of no movement are written, with who decides
- [x] A review date is set, no more than two quarters out (2027-04-19)

Signed: Elsa Marangoni, product operations lead, 2026-10-20 · Imogen Harrow, head of product, 2026-10-20
