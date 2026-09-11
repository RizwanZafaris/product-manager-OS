---
layer: frameworks
stage: DEFINE
gate: 2
feeds: ["templates/definition/design-brief.md", "templates/execution/decision-log.md", "templates/architecture/design-review-record.md"]
method: "knowledge/design/pm-design-collaboration.md"
aliases: ["Design Critique", "design-critique"]
---
# Design Critique

Based on the ideas of Sarah Gibbons at Nielsen Norman Group (2016) and Scott Berkun (2003). Explained here in this repository's own words.

## What it is for

A design critique exists to improve a piece of work, not to approve it. NN/g names this as one of two distinct meetings: a critique gathers feedback against agreed objectives, while a design review evaluates a design and can end in a go decision (Gibbons, 2016). This sheet runs the critique half. The approval half, when the team is ready for it, is a separate event recorded in the [design review record](../../templates/architecture/design-review-record.md), never this sheet.

NN/g sets three conditions for a critique to work: a clear scope, design objectives agreed before the room fills, and conversation instead of commands (Gibbons, 2016). Without agreed objectives, feedback becomes a vote on taste. This sheet exists to force the first two conditions onto paper before anyone opens a comment on the design.

## Run it when

- A design has a shape worth reacting to (a flow, a wireframe, a prototype, a build) and the objectives it must serve are already written down somewhere, most often the [design brief](../../templates/definition/design-brief.md).
- The team wants structured feedback from more than one person before committing further design or engineering time.
- A decision needs input from people outside the room who are not present to approve it themselves.

**Skip it when:** the change is a one-screen bug fix with no objective in dispute. Run it in code review instead and save the room for work where the objective, not just the pixel, is still open.

## Inputs you need first

- The scope: which screen, flow, or state is in the room, and which is explicitly out.
- The objectives, pasted in verbatim from the [design brief](../../templates/definition/design-brief.md) section 4, not re-derived from memory in the room.
- Three or four questions the presenter has written in advance to focus the conversation (Berkun, 2003); an open "what do you think" invites forty minutes of scattered reaction.
- The roster: a presenter, three to seven critiquers, a facilitator, and a note-taker.

## The worksheet

### 1. Scope and objectives

<!-- Paste the objective rows from the design brief (section 4, Success) or the
     PRD requirement they trace to. A critique with no pasted objective is a
     critique about taste. -->

| Screen, flow, or state in scope | Objective it must serve | Source |
|---|---|---|
| | | [design brief](../../templates/definition/design-brief.md) section 4 |

**Out of scope this session:** [name what the room will not react to, so a critiquer does not spend the room's time on a screen nobody brought]

### 2. The presenter's questions

<!-- 3 to 4 questions, written before the room convenes (Berkun, 2003). A
     question is a real question, not a request for reassurance: "does the
     error state read as urgent enough" beats "does this look okay". -->

1.
2.
3.
4. [optional]

### 3. Roles

| Role | Who | Job |
|---|---|---|
| Presenter | | Frames the scope and objectives, asks the prepared questions, does not defend every comment in the room |
| Critiquers (3 to 7) | | React to the objectives, not to personal preference |
| Facilitator (rotates session to session) | | Keeps the room on scope, enforces the phrasing rule, runs the parking lot |
| Note-taker | | Fills the outcome log live, so nothing is reconstructed from memory afterward |

### 4. Mode

<!-- Pick one before the room starts. -->

- **Round robin:** each critiquer speaks in turn on each screen in scope, so a quiet voice is not crowded out by a loud one.
- **Quotas:** each critiquer owes a fixed number of comments (for example, two strengths and two concerns) before the floor opens, so the session does not end on a single dominant thread.

Mode used this session: [round robin / quotas]

### 5. Phase bar

<!-- Berkun's point that the critique bar should widen early and narrow late
     (Berkun, 2003), mapped onto this repository's stages. -->

| Stage the design is in | What the room may react to |
|---|---|
| DISCOVER, DEFINE | Goals and flows: does this solve the problem, does the flow match the job to be done |
| DESIGN | Screens and interactions against the pasted objectives: layout, states, copy and accessibility of the flow already decided at DEFINE |
| BUILD | States and fidelity only: empty, error, loading, and edge states against the design system, not the underlying flow decision already made at DEFINE |

Reacting to a DEFINE-level question (should this flow exist at all) once the work is in BUILD is a scope break; the facilitator routes it to the parking lot and, if it holds up, back to a new design brief revision rather than reopening this session.

### 6. Phrasing rule

Every comment in the room follows this order and no other:

1. **Observation.** What is actually on screen or in the flow, stated plainly.
2. **Objective affected.** Which pasted objective from section 1 this observation bears on.
3. **Question.** What the presenter should consider, phrased as a question, never as an instruction.

"Make the button blue" is a command and is out of order. "The confirm action reads as low priority next to the cancel action (observation), which works against the objective of a fast completion path (objective), so what happens if confirm carries more visual weight (question)" is in order.

### 7. Parking lot

<!-- Anything raised that is out of scope, a new objective, or a question the
     room cannot resolve in the room. -->

| Item raised | Why it is parked | Owner | Where it goes next |
|---|---|---|---|
| | | | |

### 8. Outcome log

<!-- One row per distinct piece of feedback. Every row closes with a status;
     "still discussing" is not a valid close. This log feeds the decision log,
     not the design review record: a critique never signs an approval. -->

| Comment | Objective it ties to | Status (accepted / rejected with reason / needs evidence) | If needs evidence: test it routes to |
|---|---|---|---|
| | | | |

**Arithmetic:** comments tied to a pasted objective, divided by all comments logged. Treat a share under half as a warning sign, not a benchmark: it means the room was not actually working from agreed objectives, whatever section 1 says on paper; stop and re-scope before the next session rather than trusting the room's judgment on an unagreed target.

## Reading the result

The outcome log is the artifact this session produces: a set of accepted changes, rejected suggestions with their reason recorded, and open items routed to a test. None of it is an approval. A design that came out of a critique with every comment accepted still has to clear its own [design review record](../../templates/architecture/design-review-record.md) before it proceeds, because a critique is evidence for that review, not a substitute for it. Carry the accepted rows into the [decision log](../../templates/execution/decision-log.md) so the rework has a paper trail distinct from the sign-off it is waiting on.

A parking lot that fills up faster than the outcome log is a signal the scope in section 1 was wrong, not that the room wandered; fix the scope before the next session rather than tightening facilitation around a scope nobody agreed to.

## ILLUSTRATIVE example

Invented, for a fictional team-scheduling app's shift-swap screen. Numbers below are illustrative only.

**Scope:** the shift-swap confirmation screen, mobile. **Objective:** a worker can request a swap and see its status in under 30 seconds (paste-in from the fictional brief). Out of scope: the manager-approval screen, brought to a later session.

**Questions:** (1) Does the confirmation state make it obvious the swap is only requested, not final? (2) Does the status indicator read correctly to a worker who has not opened the app in a week? (3) Is the decline path as visible as the accept path?

**Mode:** round robin, five critiquers plus the presenter.

| Comment | Objective it ties to | Status | Routes to |
|---|---|---|---|
| The "Pending" label sits below the fold on a small screen | Status visible in under 30 seconds | Accepted | |
| Decline uses the same button weight as accept | Decline path as visible as accept | Accepted | |
| Icon color for "Pending" reads as an error state to some users | Status visible in under 30 seconds | Needs evidence | Usability test, next round |
| Swap history should show on this screen too | (no pasted objective covers this) | Rejected, out of scope this session | Parking lot, candidate for a new brief section |

Objective-tied share: 3 of 4 comments (75 percent), so the room stayed close to its objectives.

Outcome: three accepted changes go to the decision log for the next build pass; one goes to a usability test before it is decided; nobody in the room approved the screen to ship, because that decision belongs to the design review record once the accepted changes land and the test result is in.

## The trap

The PM sitting in a critique at pixel altitude: reacting to color, spacing, and copy instead of the objectives the design has to serve, and then, worse, treating the room's agreement as the approval to proceed. A critique produces feedback; it does not produce a go decision, and a PM who lets a critique's warm consensus stand in for a signed [design review record](../../templates/architecture/design-review-record.md) has skipped a gate without anyone noticing it was skipped.

## Feeds

- [Design brief](../../templates/definition/design-brief.md): section 1 and section 4 supply the objectives pasted into section 1 of this sheet; a critique held before the brief exists is a critique with nothing to check comments against
- [Decision log](../../templates/execution/decision-log.md): the accepted rows of the outcome log
- [Design review record](../../templates/architecture/design-review-record.md): the separate approval event this sheet never performs
- DEFINE, feeding [Gate 2: requirements signed off](../../os/STAGE-GATES.md); this sheet always logs to Gate 2, even for a critique run against a BUILD-stage screen (section 5's phase bar limits what the room may react to at BUILD, not which gate the outcome log feeds), its outcome carried forward rather than re-scoped
- Worked fill: [Ledgerline design critique example](../../examples/ledgerline-design-critique.md)
- Method background: [PM and design collaboration](../../knowledge/design/pm-design-collaboration.md)
