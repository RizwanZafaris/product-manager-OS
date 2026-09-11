# Design Critique: Expense Copilot, Activation and Charge-Confirmation Screen

Fills [frameworks/design/design-critique.md](../frameworks/design/design-critique.md) and cites the [design sheet](ledgerline-design-sheet.md) (LD19 to LD23) as the data source. Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional product used across this repository, the people are fictional roles or invented names, the screen and every comment and figure are ILLUSTRATIVE, built to show the worksheet and the phrasing rule and not to be copied as a result. The critique ran against the activation and charge-confirmation screen (LEDGERLINE-S1) the day after positioning was signed, so nothing below reports a price outcome or an EXP result; those stay with the [journey](ledgerline-journey.md) and the [design sheet](ledgerline-design-sheet.md). See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Facilitator:** Priya Nair (rotating) · **Held:** 2026-10-31 · **Stage at the time:** DEFINE, feeding [Gate 2: requirements signed off](../os/STAGE-GATES.md). Note: The screen (LEDGERLINE-S1) was a pre-build Figma prototype at the time of this critique, staged at DEFINE, which justifies the Gate 2 feed; this framing is distinct from the screen's later BUILD-stage ship date of 2026-11-19.

## What it is for

A design critique exists to improve a piece of work, not to approve it. NN/g names this as one of two distinct meetings: a critique gathers feedback against agreed objectives, while a design review evaluates a design and can end in a go decision (Gibbons, 2016). This sheet runs the critique half. The approval half, when the team is ready for it, is a separate event recorded in the [design review record](../templates/architecture/design-review-record.md), never this sheet.

NN/g sets three conditions for a critique to work: a clear scope, design objectives agreed before the room fills, and conversation instead of commands (Gibbons, 2016). Without agreed objectives, feedback becomes a vote on taste. This sheet exists to force the first two conditions onto paper before anyone opens a comment on the design.

## Run it when

- A design has a shape worth reacting to (a flow, a wireframe, a prototype, a build) and the objectives it must serve are already written down somewhere, most often the [design brief](../templates/definition/design-brief.md); here, as a local deviation, the objectives are substituted from the positioning document signed the day before (LD20).
- The team wants structured feedback from more than one person before committing further design or engineering time.
- A decision needs input from people outside the room who are not present to approve it themselves.

**Skip it when:** the change is a one-screen bug fix with no objective in dispute. Run it in code review instead and save the room for work where the objective, not just the pixel, is still open.

## Inputs you need first

- The scope: which screen, flow, or state is in the room, and which is explicitly out.
- The objectives, pasted in verbatim from the positioning document (LD20), signed 2026-10-30, not re-derived from memory in the room.
- Three or four questions the presenter has written in advance to focus the conversation (Berkun, 2003); an open "what do you think" invites forty minutes of scattered reaction.
- The roster: a presenter, three to seven critiquers, a facilitator, and a note-taker.

## The worksheet

### 1. Scope and objectives

| Screen, flow, or state in scope | Objective it must serve | Source |
|---|---|---|
| The add-on activation screen and the charge-confirmation step (LEDGERLINE-S1), as a Figma prototype, pre-build | The admin sees the exact charge before confirming, never after | positioning document (LD20), signed 2026-10-30 |
| The same screen, read against the platform it activates on | The screen reads as an add-on to the platform the account already runs, not a new vendor | positioning document (LD20), signed 2026-10-30 |

**Out of scope this session:** the drafted-line-item screen (LEDGERLINE-S3), brought to a later session; the per-seat price itself and the value-metric choice, settled at D3; the billing-system seat meter, DEP1, owned separately.

### 2. The presenter's questions

1. Does the charge-confirmation step show the exact per-seat charge before the admin confirms, with nothing that reads as a charge appearing only after activation?
2. Does the screen read as something the account already runs, given it activates on the existing Business-plan login, or does it read as a separate product the admin has to be sold on again?
3. Does the flow hold up at the narrow, kiosk-equivalent mobile width some accounts use for admin tasks, or does the charge figure become hard to read there?

### 3. Roles

| Role | Who | Job |
|---|---|---|
| Presenter | the product designer, LD-P1 | Frames the scope and objectives, asks the prepared questions, does not defend every comment in the room |
| Critiquers (3 to 7) | Maya Chen, P1, product manager; Tomas Lindqvist, P5, head of product marketing; Ruth Adeyemi, P6, VP sales; Hana Sato, P8, head of customer success (4) | React to the objectives, not to personal preference |
| Facilitator (rotates session to session) | Priya Nair, P2, engineering lead | Keeps the room on scope, enforces the phrasing rule, runs the parking lot |
| Note-taker | Kwame Boateng, P7, data analyst | Fills the outcome log live, so nothing is reconstructed from memory afterward |

### 4. Mode

- **Round robin:** each critiquer speaks in turn on each screen in scope, so a quiet voice is not crowded out by a loud one.
- **Quotas:** each critiquer owes a fixed number of comments (for example, two strengths and two concerns) before the floor opens, so the session does not end on a single dominant thread.

Mode used this session: round robin, four critiquers plus the presenter.

### 5. Phase bar

| Stage the design is in | What the room may react to |
|---|---|
| DISCOVER, DEFINE | Goals and flows: does this solve the problem, does the flow match the job to be done |
| BUILD | States and fidelity only: empty, error, loading, and edge states against the design system, not the underlying flow decision already made at DEFINE |

The work is in DEFINE, the day after positioning was signed, so the room reacts to whether the flow itself serves the two pasted objectives, not yet to build-stage state fidelity; that pass is a later session's job once the screen is built.

### 6. Phrasing rule

Every comment in the room follows this order and no other:

1. **Observation.** What is actually on screen or in the flow, stated plainly.
2. **Objective affected.** Which pasted objective from section 1 this observation bears on.
3. **Question.** What the presenter should consider, phrased as a question, never as an instruction.

"Make the button blue" is a command and is out of order. "The charge figure sits below the fold at the narrow width tested (observation), which works against the charge-before-confirming objective (objective), so what happens if the figure moves above the confirm action (question)" is in order.

### 7. Parking lot

| Item raised | Why it is parked | Owner | Where it goes next |
|---|---|---|---|
| A seats-versus-filers breakdown on the activation screen, so the admin sees both counts before confirming | Out of scope: neither pasted objective covers a second breakdown view, and it is a new screen, not a state of this one | Maya Chen, P1 | Logged as LEDGERLINE-S4 on 2026-12-17, from the win-loss interviews (WL-01, WL-04) |
| Icon color for the confidence indicator on the confirmation step | Out of scope: no pasted objective covers icon color, and the confidence indicator itself belongs to the drafted-line-item screen (LEDGERLINE-S3), out of scope this session | the product designer, LD-P1 | Parking lot; revisit if LEDGERLINE-S3 reaches its own critique |
| Icon color contrast against the platform's existing palette | Out of scope: escalated to the design-system lead (LD-P2); relates to the library gaps logged at LD2 or the token coverage at LD3, but no specific LD row covers a palette contrast rule | Priya Nair, P2 | Design-system gap log |

### 8. Outcome log

| Comment | Objective it ties to | Status (accepted / rejected with reason / needs evidence) | If needs evidence: test it routes to |
|---|---|---|---|
| C1: The charge-confirmation step displays the exact per-seat charge clearly before the admin confirms (observation), which satisfies the charge-before-confirming objective (objective), so does the combined display of rate and count obscure the exact charge at a glance, or does it serve the objective best as is (question)? | Charge before confirming, never after (row 1) | Accepted, in scope: a fidelity and layout question inside the product designer's authority | (n/a) |
| C2: The confirm action and the charge figure sit in the same viewport at desktop width, but the flow has not been checked at the narrow, kiosk-equivalent mobile width some accounts use for admin tasks (observation), against the charge-before-confirming objective (objective), so does the figure stay legible and above the fold at that width (question)? | Charge before confirming, never after (row 1) | Needs evidence | Usability test: the 2026-11-17 to 2026-11-19 round (LD5 to LD16), reviewing the charge-confirmation task at the tested width, owner Hana Sato |
| C3: The charge-confirmation copy states the monthly total but does not restate that the charge is billed on the same invoice as the Business plan (observation), against the charge-before-confirming objective, since an admin might read "monthly total" as a separate bill (objective), so what if the copy named the existing invoice explicitly (question)? | Charge before confirming, never after (row 1) | Accepted, in scope: a copy change inside the product designer's authority | (n/a) |
| C4: The activation screen opens from inside the account's existing Business-plan settings, with no separate login or account creation step (observation), which is exactly the reads-as-an-add-on objective (objective), so does the entry point need a stronger visual tie to the settings area it opens from (question)? | Reads as an add-on to the existing platform, not a new vendor (row 2) | Accepted, in scope: a visual-hierarchy change inside the product designer's authority | (n/a) |
| C5: The screen's header names the add-on by its own product name without referencing "Ledgerline" or "Business plan" anywhere on the step (observation), against the reads-as-an-add-on objective (objective), so should the header carry the platform name alongside the add-on name (question)? | Reads as an add-on to the existing platform, not a new vendor (row 2) | Accepted, in scope: a copy and header change inside the product designer's authority | (n/a) |
| C6: The confirmation screen's visual style (typography, spacing, button shape) matches the rest of the Business-plan settings pages exactly, with no new component introduced (observation), which supports the reads-as-an-add-on objective directly (objective), so is there anything on the screen that still reads as a separate product (question)? | Reads as an add-on to the existing platform, not a new vendor (row 2) | Accepted, in scope: confirms the objective is already met; no change needed, logged as accepted with no action | (n/a) |
| C7: An admin filling this out at a kiosk-style shared terminal cannot see whether the account already has other seats activated elsewhere, so a seats-versus-filers breakdown before confirming would let them check that first (observation)? | (no pasted objective covers a second breakdown view; scoped to this screen's two objectives only) | Parked, out of scope: logged as a new screen rather than a change to this one | LEDGERLINE-S4, logged 2026-12-17 |
| C8: The confidence indicator icon planned for the drafted-line-item screen (LEDGERLINE-S3) uses the same amber as this screen's warning state, which could read as unrelated warnings once both screens ship (observation)? | (no pasted objective covers LEDGERLINE-S3, out of scope this session) | Rejected with reason: LEDGERLINE-S3 is explicitly out of scope this session and is brought to its own later critique | Parking lot; revisit at LEDGERLINE-S3's own session |
| C9: The confirm button's green does not match the platform's existing primary-action color exactly, a few shades brighter (observation)? | (no pasted objective covers color-token accuracy) | Rejected with reason: a design-system token question, not a flow objective this session pasted in | Design-system gap log, not this outcome log |

**Arithmetic:** comments tied to a pasted objective, divided by all comments logged. All nine comments (C1 to C9) were logged; six (C1 to C6) tied to a pasted objective from section 1, three (C7, C8, C9) did not: 6 / 9 = 67 percent. Treat a share under half as a warning sign, not a benchmark; at 67 percent, the room was working from agreed objectives.

## Reading the result

The outcome log is the artifact this session produces: a set of accepted changes, rejected suggestions with their reason recorded, and open items routed to a test. None of it is an approval. A design that came out of a critique with every comment accepted still has to clear its own [design review record](../templates/architecture/design-review-record.md) before it proceeds, because a critique is evidence for that review, not a substitute for it. Carry the accepted rows into the [decision log](../templates/execution/decision-log.md) so the rework has a paper trail distinct from the sign-off it is waiting on.

A parking lot that fills up faster than the outcome log is a signal the scope in section 1 was wrong, not that the room wandered; fix the scope before the next session rather than tightening facilitation around a scope nobody agreed to.

Outcome: five accepted rows (C1, C3, C4, C5, C6) go to the decision log for the next design pass, and to the [design review record](../templates/architecture/design-review-record.md) once landed; one accepted-and-routed row (C2) goes to the 2026-11-17 to 2026-11-19 usability round rather than a new test built just for this question, since that round already covered the charge-confirmation task (LD5 to LD16); one item (C7) is not rejected but logged as its own screen, LEDGERLINE-S4, rather than a change here; two rejected rows (C8, C9) have their reason on the page and route to the parking lot or the design-system gap log rather than reopening the session. Nobody in the room approved the screen to ship: that belongs to the design review record once the accepted changes land and the C2 evidence is read from the usability round.

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

The PM sitting in a critique at pixel altitude: reacting to color, spacing, and copy instead of the objectives the design has to serve, and then, worse, treating the room's agreement as the approval to proceed. A critique produces feedback; it does not produce a go decision, and a PM who lets a critique's warm consensus stand in for a signed [design review record](../templates/architecture/design-review-record.md) has skipped a gate without anyone noticing it was skipped.

The trap here, on the very first customer-facing screen of the add-on, is that the room drifts toward pricing questions the value metric had not yet settled (D3 was still three days away). C7's seats-versus-filers breakdown could easily have pulled the room into a pricing argument; the facilitator instead routed it to a new screen rather than reopening the value-metric question, so the session stayed on the two pasted objectives. A PM who let this DEFINE-stage critique wander into per-seat-versus-per-usage debate would have pre-empted D3 without anyone noticing it was skipped.

## Feeds

- [Positioning document](ledgerline-positioning.md): LD20 supplies the two objectives pasted into section 1 of this sheet, signed the day before this session
- [Decision log](../templates/execution/decision-log.md): the accepted rows of the outcome log (C1, C3, C4, C5, C6, and the routing of C2)
- [UX scorecard](ledgerline-ux-scorecard.md): where C2's needs-evidence question is answered, inside the 2026-11-17 to 2026-11-19 round's charge-confirmation task (T2)
- [Design review record](../templates/architecture/design-review-record.md): the separate approval event this sheet never performs
- DEFINE, feeding [Gate 2: requirements signed off](../os/STAGE-GATES.md)
