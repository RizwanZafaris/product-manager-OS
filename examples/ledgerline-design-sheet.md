# Ledgerline Design Sheet: the data behind the experience-design examples

Fills no template. This file extends [ledgerline-journey.md](ledgerline-journey.md) and never contradicts it: every row, id, person, date and decision on the journey's data sheet stands exactly as written there, and this sheet only adds rows beside them, prefixed LD. It is the supplementary data sheet for the experience-design examples that fill a design-layer worksheet or template on the Expense Copilot story. Everything here is ILLUSTRATIVE and invented: every count, score, date and screen described below is fiction built so that these files and the journey's thirteen can be checked against each other. No figure is a benchmark, a target to copy, or a claim about any real usability round, survey instrument or design system. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2027-01-20 · **Extends:** the [journey data sheet](ledgerline-journey.md), rows N1 to N94 and every id in its shared-identifier section

## Rules for every design file

- **The journey wins.** Where this sheet and [ledgerline-journey.md](ledgerline-journey.md) could be read two ways, the journey's reading holds. No design file moves a journey date, owner, outcome, score or gate attempt, and no N row is restated here with a different value.
- **Two sources of numbers, nothing else.** A design file cites journey rows by their own ids (N32, D6, LEDGERLINE-S1) and this sheet's rows by LD id. A number found in neither is wrong, or this sheet is; the sheet is corrected first and the file second, the rule the journey states for itself.
- **The journey's firmness words.** Every LD row carries one of measured, estimate, target or assumption for quantities, or decided for choices, or date for calendar facts. A derived row shows its arithmetic and takes the firmness of its weakest input.
- **Nothing on the journey sheet moves.** Design files dated after the journey closed on 2026-12-22 extend it and change nothing it records. EXP-2's result is left open on purpose, exactly as the coverage sheet for this journey leaves it open: no design file reports an EXP-2 conversion figure or a successor price for the 73 held accounts (N93), because the journey does not know them.

## Cast additions

Two people are added, by role only, matching the journey's own convention for the legal lead and the billing lead. Neither is named, because the journey's cast table names nobody in either role.

| Id | Person (fictional) | Role | Appears in |
|---|---|---|---|
| LD-P1 | the product designer | Designs the screens LEDGERLINE-S1 through S5 carry; presents at the design critique; co-signs the design review record | Design critique, design review record, choice-symmetry audit |
| LD-P2 | the design-system lead | Owns the shared component library (LD1) and its inventory; reviews design-system conformance | Design-system audit, design review record |

Every other person in a design file is a named member of the journey's cast: Maya Chen, Tomas Lindqvist, Kwame Boateng, Hana Sato, Isabel Ferreira, Priya Nair, Daniel Okafor, Ruth Adeyemi or Marcus Webb, exactly as [the journey](ledgerline-journey.md) lists them. A design file needing a person neither the journey nor this sheet names uses a role, the way the journey itself falls back to "the legal lead" and "the billing lead."

## Reconciliation notes

- **The six design partners.** Bramblewood Freight, Tessellate Consulting, Marlowe Field Services, Corrigan and Vale, Oakhurst Dental Partners and Wrenfield Labs are the N41 design partners and nobody else; a design file drawing usability or critique participants from customer accounts draws from this list, or from the N36 best-fit segment by role ("a finance reviewer at a design-partner account"), never from an invented company.
- **The 73 seat-price accounts.** N93 holds them at $6 a seat for 12 months pending EXP-2. A design file may show the activation screen these accounts saw (LEDGERLINE-S1, priced per seat) without implying a successor price exists; none is recorded anywhere in this story.
- **D6 and D7.** D6 (2026-12-21) killed the per-seat price and pivoted packaging; D7 (2026-12-22) set the usage re-offer at $2.40 per drafted report. A design file dated after 2026-12-22 may show screens built for the usage price; one dated before it may not, on pain of contradicting the journey's own timeline.
- **$2.40 per drafted report** is N89, proposed, not yet tested; EXP-2 opens 2027-01-11 per N91. No design file states a conversion result for it.
- **The offer-page wording, N94.** "Copilot pricing is under review; existing activations are unchanged," drafted 2026-11-06, switched live 2026-12-21. A design file dated in that window shows whichever wording the date requires.
- **The heart-metrics baseline is a different instrument from SUS, and the two are never compared.** LD18 below is a single in-app rating (HEART's Happiness dimension, one question, one 5-point scale, answered by filers after submitting a report). It was read on a different population, on a different day, against a different question, from the SUS and UMUX-LITE rows in this sheet (LD9 to LD13), which were asked of design-partner finance reviewers in a moderated round. No design file states that the two numbers agree, disagree, or can be added together; they answer different questions and sit in different sections.
- **The shared component library is a sheet fact.** The journey is silent on it: no N row, no S row, no D row mentions a design system. LD1 through LD4 below are invented here, for this lane, and are never attributed to the journey.

## Data rows (every value ILLUSTRATIVE)

A number not on this sheet or on the journey's sheet does not appear in any design file.

### The shared component library (new to this lane)

| Id | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| LD1 | Shared component library | "Ledgerline UI," one library, versioned, shared across the Starter, Business and Enterprise surfaces and the add-on; the copilot's screens draw from it rather than shipping one-off components | design-system lead's library register | measured |
| LD2 | Library inventory at 2027-01-18 | 41 components published stable; 6 in trial; 2 deprecated with a removal date of 2027-04-01; 3 logged gaps (no confirmation-with-charge pattern, no confidence-flag chip, no per-seat-versus-per-usage price toggle) before the copilot shipped its own one-off versions of all three | library register, design-system lead | measured |
| LD3 | Token coverage on the copilot's screens | 94% of styled properties reference a library token; the 6% not tokenized are the three gap components at LD2 | design-system lead's audit, 2027-01-10 | measured |
| LD4 | One-off components the copilot shipped ahead of the library | the charge-confirmation step (LEDGERLINE-S1), the confidence-flag chip (LEDGERLINE-S3), and the per-seat price row later reused, unchanged, for the per-report price row proposed under D7; none formally promoted into LD1 as of this sheet's date | design-system lead's gap log | measured |

### Usability round, design-partner finance reviewers, 2026-11-17 to 2026-11-19

Feeds a [UX scorecard](../frameworks/design/ux-scorecard.md) example. Participants are finance reviewers at four of the six N41 design partners, drawn after phase 1 went live (N43) and before the EXP-1 pricing experiment opened (N56); none had yet seen the per-seat price screen in anger, since phase 1 billed no design partner (N42).

| Id | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| LD5 | Round dates and roster | 2026-11-17 to 2026-11-19, moderated, one hour each; 5 finance reviewers: one each from Bramblewood Freight, Tessellate Consulting, Marlowe Field Services and Corrigan and Vale, plus one screen-reader user from Tessellate Consulting's second reviewer; facilitator Hana Sato; note-taker Kwame Boateng | usability test plan, session log | measured |
| LD6 | Task T1: review a drafted line item with a flagged field and confirm or correct it (LEDGERLINE-S3) | 5 attempts, 4 unassisted successes; the screen-reader participant did not complete unassisted | session log | measured |
| LD7 | Task T1 confidence interval | n = 5 below the n = 5 threshold where the worksheet still computes an interval (adjusted Wald, z = 1.96): n' = 5 + 3.8416 = 8.8416; p' = (4 + 1.9208) / 8.8416 = 0.669; margin = 1.96 x sqrt(0.669 x 0.331 / 8.8416) = 0.310; interval [0.359, 0.979], reported as 80 percent (4 of 5), 95% CI [0.36, 0.98] | derived from LD6, adjusted Wald per the worksheet's own method | measured |
| LD8 | Task T1, screen-reader segment | 0 of 1 succeeded unassisted; reported as a raw fraction only, per the worksheet's rule below n = 5; the participant could not locate the confidence flag with the screen reader, which field accuracy data (N21, N24) never surfaces | session log | measured |
| LD9 | Task T2: activate the add-on and see the per-seat charge before confirming (LEDGERLINE-S1) | 5 of 5 unassisted successes; median time on task 38 seconds; 1 recovered error (one reviewer opened the wrong settings tab first) | session log | measured |
| LD10 | Time on task and errors, T1 | median 74 seconds (sighted participants, n = 4); 1 recovered error (misread a flagged amount as already corrected), 1 unrecovered (the screen-reader participant) | session log | measured |
| LD11 | Post-task ease, 1 to 7 | T1: median 5 of 7, n = 4 (sighted). T2: median 6 of 7, n = 5 | session log | measured |
| LD12 | SUS raw item responses, per respondent (odd items 1,3,5,7,9 and even items 2,4,6,8,10, 1 to 5 agreement) | R1: 4,2,4,2,4,2,4,1,4,2 -> SUS 77.5. R2: 3,3,4,2,3,2,3,3,3,2 -> SUS 60.0. R3 (screen reader): 2,4,2,4,1,4,2,5,2,5 -> SUS 17.5. R4: 4,2,3,2,4,1,4,2,3,2 -> SUS 72.5. R5: 3,2,4,3,3,2,4,2,4,3 -> SUS 65.0 | SUS questionnaire, scored per the worksheet's published procedure | measured |
| LD13 | Mean SUS | (77.5 + 60.0 + 17.5 + 72.5 + 65.0) / 5 = 58.5, n = 5; reported with the screen-reader respondent's 17.5 shown separately, never folded into a single mean that hides it | derived from LD12 | measured |
| LD14 | UMUX-LITE raw items, per respondent (item1, item2, 1 to 7 agreement) | R1: 6,7. R2: 5,4. R3: 2,1. R4: 6,5. R5: 5,5 | UMUX-LITE questionnaire | measured |
| LD15 | UMUX-LITE scoring | UMUX(1,3) per respondent = ((item1-1)+(item2-1))*100/12: R1 91.7, R2 58.3, R3 8.3, R4 75.0, R5 66.7. Adjusted (0.65x+22.9): R1 82.5, R2 60.8, R3 28.3, R4 71.6, R5 66.2. Mean adjusted UMUX-LITE 61.9, n = 5 | derived from LD14 per the worksheet's regression adjustment | measured |
| LD16 | Reading the round | task success first: T1 at 80 percent (4 of 5) masks a screen-reader failure reported separately at 0 of 1 (LD8); satisfaction last: mean SUS 58.5 and mean UMUX-LITE 61.9 sit below the SUS worksheet's cited pooled average of 68, read as a signal to recheck T1's flagged-field pattern, not as a pass or fail on their own | derived from LD7, LD8, LD13, LD15, per the worksheet's reading order | estimate |

### HEART happiness reading, in-app, 2026-12-01 to 2026-12-15 (a separate instrument)

| Id | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| LD17 | Instrument | one in-app question, asked once per filer after a drafted report is submitted: "How satisfied are you with the drafting experience on this report," 5-point scale, top-2-box reported | in-app survey, product analytics | measured |
| LD18 | Happiness baseline, 2026-12-01 to 2026-12-15 | 58 percent top-2-box across 214 responses from active add-on accounts (N64); never stated alongside or averaged with LD13's mean SUS of 58.5, a numeric coincidence between two different instruments on two different scales | in-app survey, product analytics | measured |

### Design critique, activation and charge-confirmation screen, 2026-10-31

Feeds a [design critique](../frameworks/design/design-critique.md) example. Held the day after positioning was signed (2026-10-30), against the objectives the positioning document had just set for the add-on's first customer-facing screen.

| Id | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| LD19 | Scope and roster | In scope: the add-on activation screen and the charge-confirmation step (LEDGERLINE-S1) as a Figma prototype, pre-build. Out of scope: the drafted-line-item screen (LEDGERLINE-S3), brought to a later session. Presenter: the product designer (LD-P1). Critiquers: Maya Chen, Tomas Lindqvist, Ruth Adeyemi, Hana Sato (4). Facilitator: Priya Nair. Note-taker: Kwame Boateng | critique session log | measured |
| LD20 | Objectives pasted in (from the positioning document, signed 2026-10-30) | O1: the admin sees the exact charge before confirming, never after (supports the margin rule at D2). O2: the screen reads as an add-on to the platform the account already runs, not a new vendor | positioning document section 4 | measured |
| LD21 | Outcome log, comment counts | 9 comments logged: 6 tied to O1 or O2, 3 not tied to either pasted objective (2 about icon color, 1 requesting a seats-versus-filers breakdown that became LEDGERLINE-S4 on 2026-12-17, outside this session's scope) | critique outcome log | measured |
| LD22 | Objective-tied share | 6 of 9 = 67 percent, above the worksheet's own reading of "most teams find under half a working signal," read as the room staying close to its objectives | derived from LD21 per the worksheet's arithmetic | measured |
| LD23 | Accepted changes carried to the decision log | 5 of 6 objective-tied comments accepted outright; 1 needs evidence (whether the charge figure reads clearly at the kiosk-equivalent mobile width) and routes to the usability round of 2026-11-17 (LD5 to LD16), which is how T2's mobile framing in that round traces back to this session | critique outcome log; decision log | measured |

### Choice-symmetry audit, activation and the 2026-12-21 offer-page swap

Feeds a [choice-symmetry audit](../frameworks/design/choice-symmetry-audit.md) example. Reads the accept path (N46's per-seat activation, shipped 2026-11-19 as LEDGERLINE-S1) and the corresponding exit path, and separately the offer-page wording change N94 made on the pivot date.

| Id | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| LD24 | Steps to accept, per-seat activation (LEDGERLINE-S1, live 2026-11-19 to 2026-12-21) | 3 steps: open Expenses settings, review the per-seat charge screen, confirm | product screens, reviewed by the product designer | measured |
| LD25 | Steps to cancel the same activation | 3 steps: open Expenses settings, open the add-on panel, confirm cancellation; no retention prompt, no required reason field | product screens | measured |
| LD26 | Symmetry reading for LD24 and LD25 | symmetric at 3 steps each with no added friction on exit, which is the finding the audit's own arithmetic is built to surface when a product adds a confirmation step or a retention offer only on the way out | derived from LD24, LD25 | measured |
| LD27 | Offer-page wording, before and after D6 | before 2026-12-21: the per-seat price and the $204-a-month median figure for a 34-seat account (N47) shown on the same screen as the accept button, 1 step to see the price, 1 step to accept. After 2026-12-21 (N94): the price is not shown at all; the screen reads "Copilot pricing is under review; existing activations are unchanged," with no accept button for a new price, 0 steps to accept, because there is nothing to accept | product screens; GTM plan section 5 | measured |
| LD28 | Reading LD27 | the asymmetry the D6 swap introduced is not between accepting and declining a single offer; it is between the two dates: an admin visiting before 2026-12-21 could see a price and act on it, and one visiting after cannot see any price at all, which the audit logs as a withdrawn-offer state rather than a choice-symmetry defect | derived from LD27, D6, N94 | estimate |

## New identifiers

Every id below is new, is unused on the journey sheet or the read-only coverage sheet for this story, and is spelled the same way in every design file. The journey's own ids (P1 to P9, LEDGERLINE-S1 to S6, R1 to R6, D1 to D7, DEP1 to DEP5, ADR-007, ADR-008, M-001 to M-012, S-1 to S-6, G-1 to G-3, N1 to N94) keep their meaning unchanged.

**Prefix.** LD, for Ledgerline Design. Checked against the journey's identifier tables and against every id the coverage sheet for this story claims (LC is that sheet's prefix there; HC is the journey-adjacent prefix the same sheet uses for its own rows; neither collides with LD).

**People.** LD-P1 the product designer, LD-P2 the design-system lead, both above.

**Data rows.** LD1 to LD28, above.

## Artifact map of the design files

| File | Fills | Stage and gate | What it decides, and which rows it uses |
|---|---|---|---|
| [ledgerline-ux-scorecard.md](ledgerline-ux-scorecard.md) | frameworks/design/ux-scorecard.md | BUILD, feeds Gate 4 | Scores the 2026-11-17 usability round task by task and satisfaction-instrument by instrument, reporting the screen-reader segment separately at every step per the worksheet's own rule. Uses LD5 to LD16, N21, N24, N41, LEDGERLINE-S1, S3; facilitator Hana Sato, scored by Kwame Boateng |
| [ledgerline-design-critique.md](ledgerline-design-critique.md) | frameworks/design/design-critique.md | DEFINE, feeds Gate 2 | Runs the 2026-10-31 critique on the activation and charge-confirmation screen against the two objectives the positioning document set the day before, logs 9 comments with their objective-tied share, and routes one open item into the usability round rather than approving the screen. Uses LD19 to LD23, D2, LEDGERLINE-S1; presenter the product designer, facilitator Priya Nair |
| [ledgerline-choice-symmetry-audit.md](ledgerline-choice-symmetry-audit.md) | frameworks/design/choice-symmetry-audit.md | BUILD and DELIVER, feeds Gate 4 and Gate 5 | Audits the accept and cancel steps on the per-seat activation as symmetric, then reads the 2026-12-21 offer-page swap as a withdrawn-offer state rather than a choice-symmetry defect, keeping the two findings in separate sections so the pivot is not mistaken for a dark pattern. Uses LD24 to LD28, N46, N47, N94, D6, LEDGERLINE-S1 |
| [ledgerline-design-system-audit.md](ledgerline-design-system-audit.md) | frameworks/design/design-system-audit.md | DESIGN, feeds Gate 3 | Audits the copilot's three screens against the shared component library, reports 94 percent token coverage and zero deviation rate with three snowflakes, and routes two unreasoned one-offs to the tech-debt register. Uses LD1 to LD4, LEDGERLINE-S1, S3, S5; owned by the design-system lead (LD-P2) |

The design-system inventory (LD1 to LD4) and the HEART happiness reading (LD17, LD18) are sheet facts; LD17 and LD18 stand as a record that the two satisfaction instruments on this story were never run on the same population or averaged together.
