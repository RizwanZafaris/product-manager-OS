# Design Brief: Wrenfield Scheduler, Self-Schedule Widget

Fills [templates/definition/design-brief.md](../templates/definition/design-brief.md). Everything here is invented and standalone: Wrenfield Health is a fictional scheduling SaaS sold to outpatient clinics, Naomi Castellanos, Priya Anand and Marcus Oyelaran are fictional people who do not appear in any other example in this repository, and every number, name and date is ILLUSTRATIVE. This brief exists to show the design-brief template filled on its own, without a PRD, personas file or problem-framing document behind it; links below point at the relevant blank templates rather than at sibling artifacts that were never written for this scenario. See the [examples index](README.md).

**Product owner:** Naomi Castellanos · **Design lead:** Priya Anand · **Engineering counterpart:** Marcus Oyelaran · **Date:** 2026-06-15 · **Status:** Agreed
**Links:** PRD not written for this standalone brief · [problem framing template](../templates/discovery/problem-framing.md) · [personas template](../templates/discovery/personas.md)

## 1. The problem

Renata Silva, a returning patient at a Wrenfield clinic, needs to book a routine follow-up visit and today can only do it by calling the front desk during business hours, waiting on hold, and negotiating a slot verbally with a coordinator who is reading the same calendar Renata could see herself. Across the 340 clinics on Wrenfield Scheduler, 70 percent of routine follow-up bookings still arrive by phone rather than through any self-service surface, because none exists (E1, clinic ops interview log, 2026-05-02). A front-desk coordinator at Alder Family Medicine put it directly: "Half my calls are someone who already knows they want a six-week checkup. I'm just typing what they tell me into the same screen they could type into themselves" (E2, INT-011, 2026-05-06). No solution guess is implied by this problem statement; the widget described in section 6 is one candidate, not a settled answer.

## 2. Users

| User (persona link) | Primary or secondary | Job to be done | Current workaround | What better means, in their words | Evidence |
|---|---|---|---|---|---|
| Renata Silva, returning patient booking a routine follow-up | primary | Get a follow-up slot onto her calendar without losing ten minutes to hold music | Calls during business hours, waits on hold, negotiates a time verbally | "I want to do this the way I book a haircut: pick a time and get a text back" (E3, INT-014, 2026-05-08) | INT-014 |
| Front-desk coordinator, e.g. the Alder Family Medicine role quoted above | secondary | Keep the day's calendar accurate without re-typing what the patient already knows | Answers the phone, reads availability aloud, types the patient's stated choice into Wrenfield Scheduler | "Anything that gets the easy bookings off my phone line means I can actually help the person standing in front of me" (E2, INT-011, 2026-05-06) | INT-011 |

## 3. Constraints

| Constraint | Type (platform / design system / accessibility / localization / legal / brand / technical / time) | Hard or soft | Source |
|---|---|---|---|
| Uses the Meridian design system's components unless a gap is logged | design system | soft | Priya Anand, design lead |
| Meets WCAG 2.2 Level AA (W3C Recommendation, 5 October 2023), with evidence in the accessibility checklist | accessibility | hard | Wrenfield's signed clinic data-processing addendum, section 9 |
| Renders as an embedded widget inside clinic-owned WordPress and Squarespace sites, correct down to a 320px viewport | technical | hard | Marcus Oyelaran, engineering counterpart |
| English and Spanish copy at launch; no other locale before phase 2 | localization | hard | Naomi Castellanos, product owner, per the FY26 clinic mix (62 percent of the 340 clinics report Spanish as a common patient-facing language) |
| No patient name, date of birth or visit reason may appear in the widget's URL or in any query parameter the embedding site's own analytics can read, per HIPAA, the Health Insurance Portability and Accountability Act of 1996 | legal | hard | Wrenfield's compliance counsel review, 2026-05-28 |
| Widget's default palette must re-theme to a clinic's brand colors using Meridian's existing token set, no new component tree per clinic | brand | soft | Priya Anand, design lead |
| Design must be agreed in time for engineering to ship ahead of Wrenfield Connect, the company's annual clinic conference, 2026-09-22 | time | soft | Naomi Castellanos, product owner |

## 4. Success

| Outcome | Metric (PRD reference) | Target (ILLUSTRATIVE until agreed) | Pre-launch test (usability test, prototype study, experiment) | Test date |
|---|---|---|---|---|
| Fewer routine follow-ups booked by phone | Phone-booked share of routine follow-up bookings, no PRD written for this standalone brief; owned by Naomi Castellanos | Fall from 70 percent (1,260 of an average clinic's 1,800 quarterly routine follow-up bookings) to 40 percent (720 of 1,800) within 90 days of launch, freeing roughly 36 staff-hours per clinic per quarter (84 hours today at 4 minutes a call, down to 48) | [usability-test-plan.md](../templates/discovery/usability-test-plan.md) copy, five patients completing a mock booking end to end | 2026-08-04 |
| Patients who start the widget finish it, rather than abandoning to the phone | Self-schedule completion rate (guardrail) | Must not fall below 80 percent of started sessions | Same prototype study as above, timed and screen-recorded | 2026-08-04 |

## 5. Out of scope

| Excluded | Why | Where it went (backlog / never / another brief) |
|---|---|---|
| New-patient intake booking | Needs an insurance-verification step this widget's data model was not built to hold; a different, larger problem | backlog, phase 2 |
| Rescheduling or cancelling an existing booking through the widget | Rel-1 targets the easy case first, per the design lead's fidelity rule in section 6; reschedule doubles the state machine the prototype study would need to test | backlog, phase 2 |
| Searching across multiple providers at one clinic | Most routine follow-ups return to the same provider the patient already saw; provider search is a distinct job, not a variant of this one | backlog, phase 2 |
| SMS appointment reminders | Already owned by Wrenfield's existing notifications system; this brief only needs that system to fire on a booking this widget creates | another brief: notifications system, not touched here |

## 6. Deliverables

| Deliverable | Fidelity (sketch / wireframe / prototype / final) | Decision it informs | Due | Reviewers (roles) |
|---|---|---|---|---|
| Booking flow sketches, three variants of the date and time picker | sketch | Whether the picker reads as a calendar grid, a list of slot chips, or a two-step day-then-time flow | 2026-06-29 | product owner, engineering counterpart |
| Wireframes for the chosen flow, patient-facing and coordinator-facing confirmation screen | wireframe | Screen count and what each screen must load before it is usable at 320px | 2026-07-13 | product owner, engineering counterpart, front-desk coordinator (Alder Family Medicine) |
| Clickable prototype for the usability test | prototype | Whether the flow clears the 80 percent completion guardrail before any code ships | 2026-07-27 | design lead, product owner |
| Final visual design with redlines and Meridian token mapping | final | Exact spacing, states and token names for the engineering handoff | 2026-08-17 | engineering counterpart |
| Accessibility annotations against WCAG 2.2 AA, feeding the accessibility checklist | final | What the [accessibility checklist](../templates/architecture/accessibility-checklist.md) records as evidence at Gate 2 | 2026-08-17 | design lead, engineering counterpart |

## 7. Review dates

| Review | Date | Attendees (roles) | Decision expected | Input needed by |
|---|---|---|---|---|
| Problem and direction | 2026-06-22 | product owner, design lead, engineering counterpart, front-desk coordinator (Alder Family Medicine) | Which of the three sketch variants in section 6 moves to wireframe | 2026-06-19 |
| Solution | 2026-07-20 | product owner, design lead, engineering counterpart | Whether the prototype is ready for the 2026-07-27 usability test as built, or needs a revision pass first | 2026-07-17 |
| Handoff to engineering | 2026-08-19 | design lead, engineering counterpart | Final visual design and accessibility annotations accepted as build-ready | 2026-08-17 |

## 8. Open questions

| Question | Owner | Needed by | Blocks (section or deliverable) |
|---|---|---|---|
| Does the 320px minimum need to hold inside a WordPress theme's own narrow sidebar layout, or only full-width embeds? | Marcus Oyelaran | 2026-06-22 | Wireframes (section 6, due 2026-07-13) |
| Will clinics accept a shared default palette for the first four weeks, or does every clinic need its brand colors live at launch? | Naomi Castellanos | 2026-07-06 | Final visual design (section 6, due 2026-08-17) |

---

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The agreed brief travels with the PRD to [Gate 2](../os/STAGE-GATES.md), and its deliverables become the design inputs to the DESIGN stage.

- [x] The problem is stated without a solution, and any solution guess is labeled as one: section 1 names the widget in section 6 as one candidate, not a settled answer, and states no solution itself
- [x] The primary user has a job, a workaround, and evidence; "all users" appears nowhere: Renata Silva, INT-014
- [x] Every constraint is labeled hard or soft with a source: seven rows, section 3
- [x] Success metrics reference the PRD, and a pre-launch test is named with a date: no PRD exists for this standalone brief, and both rows in section 4 say so plainly rather than inventing one; both name a prototype study and a date
- [x] Out of scope is written with reasons: four rows, section 5
- [x] Every deliverable names the decision it informs, a due date, and reviewers: five rows, section 6
- [x] Review dates are on calendars, with attendees confirmed: three rows, section 7, confirmed at the 2026-06-15 sign-off below
- [x] The accessibility row names the level and where its evidence will live: WCAG 2.2 Level AA, section 3, evidence into the accessibility checklist per section 6
- [x] Signed by the product owner and the design lead, Naomi Castellanos and Priya Anand, 2026-06-15
