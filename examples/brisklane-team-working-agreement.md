# Team Working Agreement: Brisklane dispatch team, winter 2026 to 2027

Fills [templates/execution/team-working-agreement.md](../templates/execution/team-working-agreement.md). Everything here is invented for this standalone example: Brisklane is a fictional maker of route-planning and dispatch software for small courier firms, the dispatch team and its people are invented, and every hour, count and date is ILLUSTRATIVE, not drawn from any real company. The clock offsets are the real standard-time offsets for the three cities named, as they stand after the autumn 2026 changes. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**Team:** Dispatch (the screens courier dispatchers use to assign and re-route jobs) · **Agreed:** 2026-11-09 · **Review by:** 2027-02-08 · **Status:** Agreed

## 1. Who this binds, and when they can talk

| Seat | Name | Location and UTC offset now | Working hours, local | Working hours, UTC | Local holidays the others do not share |
|---|---|---|---|---|---|
| Product | Ines Carvalho | Lisbon, UTC+0 | 09:00 to 17:30 | 09:00 to 17:30 | Portugal's national holidays, per the company holiday calendar |
| Design | Marcus Doyle | Toronto, UTC-5 | 08:00 to 16:30 | 13:00 to 21:30 | Ontario's statutory holidays, per the company holiday calendar |
| Engineering | Aditi Kulkarni | Pune, UTC+5:30, no daylight saving | 10:00 to 18:30; Tuesday and Thursday 11:30 to 20:00 | 04:30 to 13:00; Tuesday and Thursday 06:00 to 14:30 | Maharashtra's holiday list, per the company holiday calendar |

Overlap arithmetic, overlap = max(0, earliest end in UTC - latest start in UTC):

- Three-way, Monday, Wednesday, Friday: latest start 13:00 (Marcus), earliest end 13:00 (Aditi), so max(0, 13:00 - 13:00) = 0 hours.
- Three-way, Tuesday and Thursday: latest start 13:00 (Marcus), earliest end 14:30 (Aditi), so 1.5 hours, 13:00 to 14:30 UTC. That is 13:00 in Lisbon, 08:00 in Toronto and 18:30 in Pune.
- Product and design: 13:00 to 17:30 UTC, 4.5 hours every day.
- Product and engineering: 09:00 to 13:00 UTC, 4 hours; 5.5 hours on Tuesday and Thursday.
- Design and engineering: 0 hours on Monday, Wednesday and Friday; 1.5 hours on Tuesday and Thursday.

Next clock change to recompute at: 2027-03-14 (Toronto moves to UTC-4), then 2027-03-28 (Lisbon moves to UTC+1). Pune does not change.
The overlap window is for: decisions that need live talk, step 3 disputes, design and engineering pairing · It is never used for: status

[OPEN: Joy Santos joins as QA lead on 2027-01-11 from Manila, UTC+8, working 01:00 to 10:00 UTC. She has one hour a day with Ines, four to five and a half with Aditi, and none with Marcus at all. Whether test charters get design review async-only, or someone flexes, has to be decided before she starts. Owner: Aditi Kulkarni, by 2027-01-18, when this agreement is re-run for four seats.]

## 2. Decision rights

Model this team runs: first voice per risk, the table in the triad decision rights card, because the three of us share 3 live hours a week and deciding everything jointly needs more live time than that.

| Question | First voice | The other seats' part | Our adjustment, if any |
|---|---|---|---|
| Is it valuable, will they choose it | Product | Design and engineering bring evidence that tests the belief | None |
| Can users succeed with it | Design | Product keeps it tied to the outcome; engineering flags feasibility limits | Product may not overrule design on the route-confirmation step without a test with at least three dispatchers |
| Can we build and run it | Engineering | Product and design say what may degrade and what must not | None |
| Scope and sequence within the area | Product, after hearing both | Dissent recorded, then commitment | None |
| A change that raises map-routing spend by more than 10 percent a month | Engineering | Product signs when the cause is a feature rather than load | Added for this team: routing spend is the team's largest running cost |

Any one of us may decide alone, and tell the others in writing the same day: dispatcher-facing copy, a component choice inside the design system, a refactor with no user-visible change, an internal admin screen.
Needs all three: removing or reordering a step in job assignment, any change to how a route is shown as confirmed, a commitment made to a named customer.

## 3. Async-first defaults

- **Written decisions.** A decision made in a call does not exist until it is in the team decision log, written by its first voice within one working day. Anyone who was absent may reopen it within two working days with new evidence; after that it stands until its reopen trigger fires.
- **Proposals.** A change that needs more than one seat starts as a written proposal with a decide-by date at least three working days out. Silence by that date means consent. We chose consent because with three time zones, "no decision" would stall every proposal sent on a Friday.
- **Handoffs across time zones.** Aditi's day ends first. She writes three lines in the team thread, what moved, what is blocked, what Ines or Marcus need, before she signs off. Marcus writes the same for Aditi's morning.
- **Meeting-free blocks.** Wednesday all day, in each person's local time, and Monday and Friday mornings until 12:00 local. Exceptions: production incidents only.
- **Missed meetings.** Trio syncs and planning are recorded and summarized in writing by whoever ran them, within four working hours.

| Channel | Use it for | Expected first response | Not for |
|---|---|---|---|
| Document comments | Proposals, specs, design review | 2 working days | Anything urgent |
| Team thread | Questions that block today's work | 4 of the recipient's working hours | Decisions, which go to the decision log |
| Direct message | Quick checks, personal matters | 4 working hours | Anything the others need to find later |
| Call or page | Production incidents, per engineering's on-call rota | 15 minutes, per the rota; the PM is not on it | Anything that can wait a working day |

Response times are counted in the recipient's working hours, never the sender's.

## 4. Rituals and cadence

| Ritual | The one output it produces | Cadence | Sync or async | Who | Where the output lands | Cancelled when |
|---|---|---|---|---|---|---|
| Trio sync | This week's decisions that need live talk | Tuesday and Thursday, 13:00 to 13:45 UTC | Sync | All three | Team decision log | Nothing is on the agenda doc by 10:00 UTC that day |
| Customer contact | One insight or assumption test a week | Weekly, one dispatcher interview on Tuesday or Thursday, 14:30 to 17:30 UTC, inside the product and design overlap and clear of Marcus's meeting-free mornings | Sync for Ines and Marcus, async for Aditi | Ines, Marcus; Aditi watches the recording within 2 working days | Team opportunity solution tree | Never; a skipped week is made up the next |
| Product review | Decisions from the WIP walk | Thursday, inside 13:45 to 14:30 UTC; the team's slot is 20 minutes | Sync | All three, with the head of product | Team decision log | The org cancels it |
| Planning | The next cycle's commitments | First Tuesday of the month, 12:00 to 14:00 UTC, in place of that day's trio sync | Sync | All three | Roadmap and capacity plan | Never |
| Retrospective | Two or three owned actions | Second and fourth Tuesday of the month: board open 48 hours, then 30 minutes in the trio sync slot | Async, then sync | All three | Retrospective copy | Never |
| Design critique | Design changes agreed before handoff | Weekly | Async only: recorded walkthrough, comments within 2 working days | Marcus runs it; Ines and Aditi comment | The design file's comments, decisions to the log | No design change that week |
| Status | The weekly written status | Friday, by each person's end of day | Async, never a meeting | Each writes their part; Ines compiles it on Monday | Team status report | Never |

Planning at 12:00 UTC is 07:00 in Toronto: Marcus flexes for it, so the flexing does not all fall on Aditi, who works late on Tuesday and Thursday every week. Waiver, agreed 2026-11-09: design critique is async only, because design and engineering share no live time three days a week. It is re-examined at the 2027-02-08 review against one question, whether any design change reached engineering without critique comments from Aditi.

## 5. How disagreement escalates

1. **Restate it as a falsifiable disagreement**, in writing, within 2 working days of it surfacing: which of the four risks is contested, and what evidence would settle it.
2. **Buy the evidence at the smallest price**, timeboxed to 5 working days: a dispatcher test, a spike, a data pull.
3. **If the evidence cannot arrive in time, the first voice decides.** The decision log records the call, the dissent and the trigger that reopens it.
4. **Still stuck, or outside the trio's rights:** a six-part brief per the [escalation skill](../skills/escalation/SKILL.md), sent to rung 2: Tomasz Wrona, head of product; Rhea Osei, VP engineering; Hana Morimoto, design director. They answer within 3 business days.

Disagree and commit, as this team means it: the seat that lost says so once, in the decision log entry, then designs or builds the decided option as if it were its own, and raises it again only when the reopen trigger fires.

## 6. Review

Review on 2027-02-08, and early when any of these happens: a seat changes hands; someone joins from a time zone that changes section 1's overlap, which Joy Santos's start on 2027-01-11 already triggers; a sync ritual is skipped three times running; a dispute reaches step 4; a response-time expectation is missed often enough that someone has stopped relying on it.

[OPEN: the 2027-03-14 and 2027-03-28 clock changes widen the Tuesday and Thursday window. Worked ahead: Marcus starts at 12:00 UTC from 2027-03-14, so the three-way window becomes 12:00 to 14:30 UTC, 2.5 hours, and Aditi's late shift could end an hour earlier. Owner: Ines Carvalho, to propose the change in writing by 2027-03-08.]

## Exit gate

Done when every box is honestly ticked. This file declares no gate; it is re-read at each gate the team reaches.

- [x] All three seats, and any extended members, are named with local and UTC hours, and the overlap arithmetic is shown for the three together and for each pair (the QA lead joining in January is an open item, not yet a row)
- [x] The next clock change to recompute at is dated (2027-03-14)
- [x] The decision model is named with its reason, and the decision table is adapted for this team (route-confirmation test rule, routing-spend row)
- [x] The reversible calls one seat may make alone, and the one-way doors that need all three, are listed
- [x] Every default in section 3 holds a number or a named choice, including what silence means (consent, with the reason)
- [x] Every channel has an expected first response, counted in the recipient's working hours
- [x] Every ritual names the one output it produces and where it lands, and every sync ritual fits the overlap window or names who flexes (planning: Marcus; Tuesday and Thursday: Aditi; critique waived to async)
- [x] The escalation path carries time limits and names the rung-2 managers
- [x] A review date is set, no more than one quarter out (2027-02-08)
- [x] The three names are in the stakeholder map, and adopting this agreement is a decision log entry (D-017)

Signed: Ines Carvalho, product manager, 2026-11-09 · Marcus Doyle, design lead, 2026-11-09 · Aditi Kulkarni, engineering lead, 2026-11-09
