# Lean Canvas: Paceboard shift handoff

Fills [frameworks/strategy/lean-canvas.md](../frameworks/strategy/lean-canvas.md). Everything here is invented: Paceboard is a fictional company, Shiftboard is its fictional product, and Maya Chen, Luis Ortega, and Priya Nair are fictional people. Every claim and figure is ILLUSTRATIVE, included to show how to rank an early bet rather than to describe a real business.

**Owner:** Maya Chen, product manager · **Date:** 2026-09-01 · **Stage:** PLANNING

A fictional context block: Paceboard is considering Shiftboard, a pre-revenue tool for shift-based teams. Maya Chen is the product manager, Luis Ortega is the designer, and Priya Nair is the operations partner. The product does not have paying customers, committed customers, or an operating model yet.

## What it is for

This canvas records Paceboard's bet before Shiftboard exists. It separates the problems worth testing from the solution, revenue, and advantage claims that are still assumptions.

The worksheet is appropriate because Shiftboard is pre-revenue and pre-customer. It is not a description of Paceboard's existing business.

## Run it when

- Before Shiftboard exists and before a business model can be modeled
- While the team is deciding whether shift handoffs are a problem worth solving
- Before building the whole product, so the largest unknown is visible
- When the problem, solution, or proposed early adopter changes

**Skip it when:** the business already has paying customers and an operating model. Use the [business model canvas](../frameworks/strategy/business-model-canvas.md) at that point.

## Inputs you need first

- A candidate problem statement for shift-based operations teams
- Existing observations about how teams record and pass on shift information
- A rough first solution
- No finance model, because price and cost are not real yet

## The worksheet

### Part 1: problem, alternatives, solution

| # | Top problem, in the customer's words | What they use instead today | Solution feature that beats it | Evidence, or "assumption" |
|---|---|---|---|---|
| 1 | “The next shift cannot tell what changed without asking the person who left.” | A shared spreadsheet, chat messages, and a verbal handoff | A handoff timeline that highlights changes since the last shift | assumption |
| 2 | “Important exceptions disappear inside a long stream of routine updates.” | A pinned chat message or a note on a printed checklist | An exception view that separates unresolved issues from completed work | assumption |
| 3 | “I do not know whether the incoming shift actually saw the handoff.” | A verbal confirmation or no confirmation | A read receipt with an acknowledgement request for unresolved items | assumption |

### Part 2: the rest of the canvas

| Block | Prompt | Answer | Confidence (high / med / low) |
|---|---|---|---|
| Customer segments | Who feels problems 1 to 3 worst, and the early adopters within them | Operations leads at shift-based teams with frequent handoffs. Early adopters are managers who already maintain a shared handoff document and have tried to make staff use it consistently. | low |
| Unique value proposition | One sentence a skeptical customer would repeat back correctly | “The next shift sees what changed and what still needs attention, without chasing the person who left.” | low |
| Channels | How the segment above hears about this and tries it | Direct conversations with operations leads, a short live demonstration using a fictional handoff, and a candidate operations software marketplace. These channels are untested. | low |
| Revenue streams | What gets paid, by whom, on what basis, if anything yet | No revenue yet. A monthly fee per active team is an assumption. Current revenue arithmetic is 0 paid teams x an untested price = 0 revenue. | low |
| Cost structure | The two or three costs that scale with usage or headcount | Product development headcount, message storage and notification usage, and customer support. Usage cost would be active teams x messages and notifications per team, but no usage rate is real yet. | low |
| Key metrics | The two or three numbers that would tell you, within a month, whether the bet is working | Handoff acknowledgement rate = acknowledged handoffs / published handoffs. Unresolved-item completion rate = completed unresolved items / unresolved items created. Repeat-use rate = teams publishing a second handoff / teams publishing a first handoff. These are proposed measures, not observed results. | low |

### Part 3: the unfair advantage filter

| Candidate advantage | Passes the filter? | Why, specifically, a funded rival could not buy or copy it fast |
|---|---|---|
| A correction history showing which handoff details repeatedly become unresolved items | No, none yet | A rival could build a similar history feature. It could become an advantage only if Paceboard accumulates a distinctive, permissioned dataset before a rival has comparable usage. |

**Decision rule:** none passes the filter at this stage. The honest answer is “none yet, price and speed only.” The correction history is a candidate to revisit after committed customers exist, not an advantage to claim now.

## Reading the result

- Every problem row says “assumption,” so this is a research task, not a build task.
- The next action is five interviews with shift managers before touching channels or revenue.
- The segment can be built as a list, but its severity and early-adopter signal are not yet evidenced.
- The unfair advantage box is honestly empty. Paceboard should not call a feature, a team, or an early start an unfair advantage.
- If the canvas later holds steady across updates with paying or committed customers, Paceboard should graduate to the [business model canvas](../frameworks/strategy/business-model-canvas.md).

## ILLUSTRATIVE example

Paceboard is a fictional pre-revenue company considering Shiftboard, a fictional shift handoff product. Maya Chen, Luis Ortega, and Priya Nair have written the canvas before building it.

The first problem is lost context between shifts, with spreadsheets, chat, and verbal handoffs as the alternatives. The second is that exceptions disappear among routine updates, with pinned messages and printed checklists as the alternatives. The third is uncertainty about whether the incoming shift saw the handoff, with verbal confirmation or no confirmation as the alternatives. All three are assumptions because no interview evidence has been recorded.

The proposed solution is a change-focused handoff timeline, an exception view, and acknowledgement requests. The proposed segment is shift-based operations teams, with managers who already maintain a handoff document as early adopters. The proposed value proposition is: “The next shift sees what changed and what still needs attention, without chasing the person who left.” Channels and revenue are untested. Current revenue is 0 paid teams x an untested price = 0. No candidate unfair advantage passes the filter.

## The trap

The risk is filling Shiftboard's canvas as if it were already a business. A polished subscription price, a named marketplace, and a claimed data advantage would make the page look complete while hiding that every problem, channel, revenue, and advantage claim is untested.

The tell is the absence of the word “assumption.” Here, all three problem rows say “assumption,” and the next action is five interviews. The canvas is useful because it shows what must be learned before Paceboard builds.

## Feeds

- [Business model canvas](../frameworks/strategy/business-model-canvas.md): the canvas to graduate into once revenue and channels are real, not guessed
- [Value proposition canvas](../frameworks/strategy/value-proposition-canvas.md): sharpens the problem and value proposition boxes with ranked jobs, pains, and gains
- [Assumptions register](../templates/definition/assumptions-register.md): records every low-confidence assumption with a validation method and date
- [Vision](../templates/planning/vision.md): section 2 can take the segment and early-adopter description
- [Product strategy](../templates/planning/product-strategy.md): section 1 can use a problem row once it carries evidence
- PLANNING track, ahead of Gate 1
- Method background: [knowledge index](../knowledge/INDEX.md), Lean Startup entry
