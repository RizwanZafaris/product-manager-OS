# Heuristic Evaluation: Harbourgate guest checkout redesign prototype

Fills [frameworks/design/heuristic-evaluation.md](../frameworks/design/heuristic-evaluation.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay, Kestrel, Marlowe and Tidewater are fictional, the evaluators and the prototype are fictional, and every finding, date and count is ILLUSTRATIVE, chosen to show the procedure and the arithmetic and never to be quoted as a benchmark or copied as a target. The guest checkout redesign is the seed's deferred design item: it sits out of scope on the Quay migration (the out-of-scope table in [harbourgate-journey.md](harbourgate-journey.md)), and this evaluation is design work on that deferred item, run against a prototype, after the Gate 6 PERSIST of 2026-10-14. See the [examples index](README.md).

**Owner:** Ines Castellanos, Design Lead · **Panel passes:** 2026-11-03 to 2026-11-04 · **Consolidated and scored:** 2026-11-05 · **Prototype link:** ILLUSTRATIVE, internal design-tool file, not a public URL · **Panel:** 3 evaluators working independently (E1, E2, E3), consolidated with Ines Castellanos present · **Method:** [Usability Heuristics](../knowledge/design/usability-heuristics.md)

## What it is for

### 1. Scope

**Product or flow:** `Guest checkout, web store (the deferred guest checkout redesign, out of scope for the Quay migration per the seed's out-of-scope table)` · **Screens in scope:** `SCR1 Basket review, SCR2 Sign-in or continue as guest, SCR3 Email and contact details, SCR4 Delivery address, SCR5 Payment method, SCR6 Order confirmation` · **Build or prototype link:** `ILLUSTRATIVE, internal design-tool file`

| Task | Screens it touches | In scope |
|---|---|---|
| T1 A returning customer completes a purchase as a guest | SCR1, SCR2, SCR3, SCR4, SCR5, SCR6 | yes |
| T2 A first-time customer pays with a new card and recovers from one decline | SCR5 | yes |
| T3 A kiosk customer collects an out-of-stock size for home delivery, paying on the PIN pad | SCR5 | no: kiosks sit outside the web accessibility standard (HC12) and the payment surface is the terminal SDK flow, not the web payment screen |
| T4 A customer checks where an already-placed order is | none (the order-history page, also out of scope) | no: outside this redesign's scope |
| T5 A customer recovers a cart abandoned in a different browser | SCR1 (re-entry) | no: no prototype for the recovery link exists |

The convention for this worksheet is 3 to 5 tasks; three of the five candidate tasks fell out on scope, so the evaluation ran on the two that survived. Section 6's evaluator-effect caveat grows when the task list shrinks: fewer tasks, more unseen problems.

## Run it when

### 2. Evaluators

Three evaluators, working independently, no shared screen and no discussion until every pass was submitted (Nielsen and Molich 1990; Moran and Gordon 2023). Ines Castellanos owns consolidation and read her own notes only after the three passes were in. Ines Castellanos's walkthrough of T2 in section 5 was walked outside the three-evaluator panel, as a separate pass, and is not counted among the panel's three independent passes.

| Evaluator | Role or background | Pass completed (date) |
|---|---|---|
| E1 | Senior product designer outside the Harbourgate design team, walked the prototype on 2026-11-03 and submitted the same day | 2026-11-03 |
| E2 | Accessibility specialist (the walk's WCAG lens; Harbourgate digital accessibility standard v4, HC12), walked on 2026-11-04 and submitted the same day | 2026-11-04 |
| E3 | Support agent with three months on the payment queue, walked as a first-time guest on 2026-11-04 and submitted on 2026-11-04 | 2026-11-04 |

A fourth evaluator, the guest checkout redesign's own designer, was excluded: a designer inspecting their own screen is one pass on someone else's work, not an independent one. No AI pass was run; had one been, section 6 makes its status plain: one evaluator, run faster.

## Inputs you need first

### 3. Findings grid

One row per evaluator per finding. Heuristic names come from Nielsen's 1994 revision, and two from Shneiderman's eight golden rules (error prevention and undo) where they name the violated expectation better than Nielsen's list does; the ISO 9241-110 column lists the nearest interaction principle, in the exact seven-name vocabulary of the [Usability Heuristics](../knowledge/design/usability-heuristics.md) crosswalk, for vocabulary only and is never a compliance claim. Severity is the same 1 to 4 scale as the [usability test plan](../templates/discovery/usability-test-plan.md) section 6 (4 blocker, 3 major, 2 minor, 1 cosmetic), never the wording from NN/g's own scale.

| Evaluator | Screen | Element | Heuristic (name) | ISO 9241-110 principle | What happened | Evidence (screenshot id or step) | Severity (1 to 4) |
|---|---|---|---|---|---|---|---|
| E1 | SCR2 | "Continue as guest" | Recognition rather than recall | Self-descriptiveness | "Continue as guest" is visually weaker than the sign-in card, so the guest path is not recognised; the guest customer has to recall that checking out without an account is possible at all | step 1 | 3 |
| E2 | SCR5 | Card-entry fields | Visibility of system status | Self-descriptiveness | The step-up challenge appears (BR-005, card-not-present over GBP 250) with no progress cue naming the GBP 250 threshold | step 3 | 2 |
| E3 | SCR5 | Card-entry fields | Visibility of system status | Self-descriptiveness | A decline flashes then is replaced; the one-retry offer with a different method (BR-001) is not visible on the decline | step 3 | 3 |
| E1 | SCR3 | Email field | Match between system and the real world | Suitability for the user's tasks | "Billing email" uses a payment-provider term the customer does not; it is the only place on the flow where a provider word is shown | step 1 | 2 |
| E2 | SCR4 | Address line 2 | Match between system and the real world | Suitability for the user's tasks | "Flat number or name" is Harbourgate phrasing; a customer with a house number hesitates and skips a line they needed | step 1 | 2 |
| E3 | SCR4 | "Save this address" checkbox | Recognition rather than recall | Self-descriptiveness | No hint that saving this address requires an account, so the guest either wastes a step or abandons the address | step 2 | 1 |
| E1 | SCR5 | Submit-payment button | Consistency and standards | Conformity with user expectations | The submit button is styled identically to disabled buttons elsewhere on the web store, so a customer who has submitted waits for confirmation the button does not show | step 4 | 2 |
| E2 | SCR3 | Inline error, invalid email | Help users recognise, diagnose and recover from errors | Use error robustness | "Email format is invalid" names the field but not what the correct format looks like | step 3 | 1 |
| E3 | SCR4 | Inline error, empty postcode | Help users recognise, diagnose and recover from errors | Use error robustness | "Required field missing" names no field; on a form with several optional lines the customer cannot tell which one was empty | step 4 | 2 |
| E1 | SCR1 | Quantity stepper | User control and freedom | Controllability | The stepper has no upper bound shown; the customer cannot see whether the basket holds the quantity they set | step 1 | 2 |
| E1 | SCR6 | "Track your order" | Recognition rather than recall | Self-descriptiveness | The link lands on an account-only tracking page, which the guest cannot use | step 2 | 2 |
| E2 | SCR6 | "Track your order" | Recognition rather than recall | Self-descriptiveness | The confirmation page never explains that tracking is account-only | step 2 | 2 |
| E2 | SCR6 | Confirmation email, order id | Help and documentation | Learnability | The order id's format (an eight-digit string) is never shown, so the customer does not know what to write down | step 2 | 1 |
| E3 | SCR6 | "Create an account" card | Match between system and the real world | Suitability for the user's tasks | The post-purchase account prompt sits above the confirmation and reads as a required next step | step 3 | 1 |
| E1 | SCR1 | "Guest checkout" entry button | Aesthetic and minimalist design | No clean match | The basket page stacks four actions and the guest entry sits below the fold on a phone | step 1 | 2 |
| E3 | SCR2 | Sign-in card | Consistency and standards | Conformity with user expectations | The sign-in card and the guest card use the same border and the same type, and only the word inside tells them apart | step 1 | 1 |

## The worksheet

### 4. Consolidation arithmetic

Deduped by the rule: same screen, same element, same violated expectation. F11 and F12 match all three (SCR6, the "Track your order" link, the violated expectation "a link I can actually follow") and consolidate. E3's finding on SCR5 and the accessibility finding AX-1 are the same control, but AX-1 is the violated expectation "a screen-reader user hears it at all", a different violated expectation from "a sighted user sees what to do next", so E3's finding is a row of its own and AX-1 is not entered here: it is a pre-existing finding already on the guest-checkout backlog, owned by Ines Castellanos.

Consolidated severity is the median of the independent severities; with three finders (odd count) it is the middle value, and no even-count tie-break was needed. Counts are 1 when one evaluator alone reported it, 2 when a matching pair reported it (F11), and 3 when all three did. Panel N = 3.

| Finding | Screen | Element | Consolidated severity | Count found (of 3 evaluators) |
|---|---|---|---|---|
| F1: guest path not recognisable on the sign-in or guest screen | SCR2 | "Continue as guest" | 3 | 1 |
| F2: decline shown with no retry-with-different-method path | SCR5 | Card-entry fields | 3 | 1 |
| F3: step-up challenge with no progress or threshold cue | SCR5 | Card-entry fields | 2 | 1 |
| F4: "Billing email" provider jargon | SCR3 | Email field | 2 | 1 |
| F5: "Flat number or name" label | SCR4 | Address line 2 | 2 | 1 |
| F6: save-address hint absent | SCR4 | "Save this address" checkbox | 1 | 1 |
| F7: submit button matches disabled-button style | SCR5 | Submit-payment button | 2 | 1 |
| F8: inline error, invalid email, no example format | SCR3 | Inline error | 1 | 1 |
| F9: inline error, empty postcode, no named field | SCR4 | Inline error | 2 | 1 |
| F10: quantity stepper upper bound not shown | SCR1 | Quantity stepper | 2 | 1 |
| F11: order tracking link lands account-only, unexplained | SCR6 | "Track your order" | 2 | 2 |
| F12: order-id format not shown in confirmation | SCR6 | Confirmation email order id | 1 | 1 |
| F13: account prompt reads as a required next step | SCR6 | "Create an account" card | 1 | 1 |
| F14: guest entry below the fold on phone | SCR1 | "Guest checkout" entry | 2 | 1 |
| F15: sign-in and guest cards visually identical | SCR2 | Sign-in card | 1 | 1 |

Median arithmetic shown for the two consolidated rows:

- F1 (E1, 3): median of {3} = 3, count 1 of 3.
- F2 (E3, 3): median of {3} = 3, count 1 of 3.
- F11 (E1 and E2, 2 and 2): median of {2, 2} = 2 (even count, higher of the two middle values, both 2), count 2 of 3.
- F12 (E2, 1): median of {1} = 1, count 1 of 3.

The rest are single-finder rows: consolidated severity equals the single independent severity.

### 5. Task-based variant: cognitive walkthrough

Run on T2 alongside the general pass, because T2 is exactly the first-encounter question the method answers (and not T3: kiosks and the terminal flow are out of scope, and this variant is skipped for expert users on a familiar flow). Ines Castellanos walked this pass outside the three-evaluator panel.

**User profile:** a first-time guest paying with a new card that will be declined once
**Task:** T2, "pay with a new card after one decline, without an account"
**Correct action sequence (what an expert would take):** S1, review basket, continue as guest; S2, choose "Continue as guest"; S3, enter contact details; S4, enter delivery address; S5, enter new card details and submit (the system invokes step-up above GBP 250 per BR-005); S5, on the decline, read the reason class, choose the one-retry offer with a different method per BR-001 (the same card is never resubmitted automatically per AC-5), submit; S5, on success, proceed to SCR6.

The four questions are the practitioner form, Wharton, Rieman, Lewis and Polson (1994); the gulf mapping is after Norman's gulfs of execution and evaluation ([Interaction Design Principles](../knowledge/design/interaction-design-principles.md)).

| Step | Would they try to achieve the right effect (gulf of execution: intent to action)? | Would they notice the correct action is available (gulf of execution: action to interface)? | Would they connect the action to their goal (gulf of execution: mapping the action to the goal)? | Would the feedback show progress toward the goal (gulf of evaluation)? | Success or failure story | Severity (1 to 4) |
|---|---|---|---|---|---|---|
| S1 | Yes | Yes | Yes | Yes | Success | 1 |
| S2 | Yes | No: the guest option is not recognisable (F1) | No: the customer cannot map "continue as guest" to "check out without an account" | Yes | Failure: two no answers; same cause as F1, so the walkthrough confirms F1 and adds no new cause | 3 |
| S3 | Yes | Yes | Yes | Yes | Success | 1 |
| S4 | Yes | Yes | Yes | Yes | Success | 1 |
| S5a (first submit) | Yes | Yes | Yes | No: step-up appears with no progress cue (F3) | Failure: one no answer | 2 |
| S5b (decline) | No: the customer does not know they may retry | Yes: a submit button is present, but it looks disabled (F7) and is not labelled "try a different card" (F2) | No: the decline message does not name the card or say a different method is wanted (F2) | No: the decline flashes, then a retry appears that the customer did not request | Failure: three no answers | 3 |
| S5c (retry submit) | Yes | No: same disabled-style button | Yes | Yes | Failure: one no answer, same cause as F7 | 2 |
| S6 | Yes | No: the order id is not shown; tracking is account-only (F11, F12) | No: the account prompt reads as required (F13) | Yes | Failure: two no answers | 2 |

**Arithmetic.** Failure stories, counting "no" answers across the four questions, per step: S1 0, S2 2, S3 0, S4 0, S5a 1, S5b 3, S5c 1, S6 2. Total no answers = 0 + 2 + 0 + 0 + 1 + 3 + 1 + 2 = 9, of 32 answers across the eight steps. Steps with at least one failure story = S2, S5a, S5b, S5c, S6, that is 5 of 8 = 0.63 (62.5%). The failures are concentrated in two steps, S5a to S5b and S5c (five of the nine no answers land in the decline-and-retry segment), which names one specific redesign target, the decline and retry flow on SCR5, rather than a pattern to recheck against gulf of execution: action to interface. The S5c "no" shares its cause with F7, and the S2 "no"s share their cause with F1, so no new finding is created; the walkthrough confirms F1, F2, F3 and F7 as task-level blockers on the path T2.

### 6. Coverage caveat

In Nielsen and Molich's four 1990 experiments, single evaluators working alone caught only 20 to 51 percent of the usability problems actually present in the interfaces they reviewed (evidence class: research evidence). This applies to the cognitive walkthrough as much as to the general pass: the evaluator effect, average agreement between any two evaluators looking at the same system ranged from 5 to 65 percent across heuristic evaluation, cognitive walkthrough and think-aloud testing alike (Hertzum and Jacobsen, 2001; evidence class: research evidence), is a property of usability evaluation methods generally, not of inspection alone and not of any one list. An AI pass, run once against a screenshot or a prototype, is one evaluator's judgment running faster than a person's; pool it with the panel's other independent passes in section 3 or 4, never report it as coverage equal to a 3 to 5 person panel. Applied to this pass: three evaluators on two in-scope tasks produced sixteen individual findings, consolidated into fifteen distinct issues, and most of them are single-finder, which is the evaluator effect showing itself: a count of 1 here means only one evaluator's independent judgment supports it so far, not that the problem is weak or confirmed.

## Reading the result

Every consolidated severity 3 or 4 finding goes to the next moderated usability round, whatever its count, scoped by the [usability test plan](../templates/discovery/usability-test-plan.md). Inspection never closes a severity 3 or 4: severity 3 and 4 sit in the [Design Review Record](../templates/architecture/design-review-record.md) section 3 as an inspection-class row "open, routed to usability test" until a user session confirms the fix or the problem's absence, in parallel with a [risk register](../templates/execution/risk-register.md) row with a named owner while the test is pending. A finding with count 1, whatever its severity, gets the same routing: one evaluator caught it, and section 6's evidence cuts both ways, since a single evaluator catches only a minority of what is actually present. A count of 1 may mean a real problem the rest of the panel missed, or it may mean nobody else could confirm it; that unresolved uncertainty, not a presumption in either direction, is why it goes to a usability round rather than being called fixed or dismissed. Severity 1 and 2 findings with count 2 or higher are strong enough to fix directly, no test needed.

- **F1 and F2, severity 3, count 1 each:** routed to the next moderated round on the guest checkout (a usability test plan to be written), and, in parallel, tracked as a design backlog and design-debt item outside the risk register, under Ines Castellanos, on the deferred redesign, since the journey's own R11 (associates stop using kiosks after the "pay at the till" fallback) is a registered usability risk on a different surface and this is a web-side finding. Count 1 does not soften either routing: one evaluator caught it, and the evidence does not say whether that means the other two missed something real or nobody else could confirm it.
- **F11, severity 2, count 2:** corroborated twice, minor; fix directly.
- **F3, F4, F5, F6, F7, F8, F9, F10, F12, F13, F14, F15, all severity 1 or 2, count 1:** routed to the next moderated usability round on the guest checkout (a usability test plan to be written). A count of 1 does not require a test on a severity 1 or 2; it simply means the rest of the panel did not report it, and the fix does not depend on whether they missed it.

The cognitive walkthrough's finding on S5b is F2 itself, not a new finding; the walkthrough's contribution is to show F2 as a task blocker on T2, not merely a screen-level principle break.

## ILLUSTRATIVE example

Invented, a guest checkout prototype for a fictional mid-market retailer (this file itself), panel of 3 evaluators, two in-scope tasks, fifteen consolidated findings (from sixteen individual), the arithmetic above.

| Finding | Screen | Element | Consolidated severity | Count found (of 3) |
|---|---|---|---|---|
| F1: guest path not recognisable | SCR2 | "Continue as guest" | 3 | 1 |
| F2: decline with no retry-with-different-method path | SCR5 | Card-entry fields | 3 | 1 |
| F11: tracking link account-only, unexplained | SCR6 | "Track your order" | 2 | 2 |

F1 and F2, severity 3, go to the next moderated usability round (a usability test plan to be written for the guest checkout) and, in parallel, to the design backlog and design-debt item outside the risk register under Ines Castellanos; each count 1 is routed on the same rule as a count 3. F11, severity 2 with count 2, is fixed directly.

## The trap

An expert review recorded as user evidence at Gate 3 or 4. A heuristic pass, however well run, is trained judgment applied by people who already know how the product is supposed to work; it substitutes for a data-gathering method, it does not become one by being written up carefully. The tell is a Design Review Record or a Gate 4 readiness note that cites this worksheet's findings as if they showed real users succeeding at real tasks. They show where a screen predictably breaks a general principle, nothing about whether the specific people who will use this specific product can get their specific job done. That claim needs the [usability test plan](../templates/discovery/usability-test-plan.md), run with real participants, cited by name. Here the trap takes a local shape: the deferred guest checkout redesign is an out-of-scope item on the Quay migration, and its findings must not be read into the migration's user evidence (the UAT, HC11, which says 4 of 4 testers would use the new path, was a finance and operations UAT, not a customer guest-checkout round).

## Feeds

- [Design Review Record](../templates/architecture/design-review-record.md): every consolidated finding from section 4 and every failure story from section 5 is the screen-level evidence the record carries to Gate 3 on the deferred guest checkout redesign.
- [Usability Test Plan](../templates/discovery/usability-test-plan.md): F1 and F2 scope what the next moderated round on the guest checkout must probe, and the plan's own section 6 severity scale is the scale this worksheet reuses.
- Design backlog and design-debt tracking: F1 and F2 are tracked as design backlog and design-debt items outside the risk register, under Ines Castellanos, on the deferred redesign, while the usability round they were routed to is still pending; the journey's usability row R11 is a registered usability risk on a different surface, not the web-side neighbour of this class of finding.
- DESIGN stage, feeding [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md).
- Method background: [Usability Heuristics](../knowledge/design/usability-heuristics.md).
