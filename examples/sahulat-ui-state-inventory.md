# UI State Inventory: Sahulat Bill Pay, the second-pass agent-assisted screens

Fills [templates/definition/ui-state-inventory.md](../templates/definition/ui-state-inventory.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan run by a fictional licensed electronic-money institution, the people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, chosen so that this file agrees with the canonical data sheet in [sahulat-journey.md](sahulat-journey.md) and not to describe any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-10-05 · **Status:** Draft

## 1. Scope

| Field | Value |
|---|---|
| Screens or components in scope | USSD menu script v0.4, agent-initiated payment (14 screens, [sahulat-design-sheet.md](sahulat-design-sheet.md) SD4); the agent-handset app confirmation screen (3 strings, SD7); the status and confirmation SMS templates (9 templates, SD6) |
| Declared viewports | USSD is character-based over Falak Telecom's gateway, no visual viewport applies; the agent-handset app is declared for the pilot district's sampled devices, smallest screen 5.0 inch (SD10, SD11), the only device size this pass tested. No tablet or desktop viewport is claimed |
| Declared themes | Only the agent-handset app's existing Latin body face against Noto Sans Arabic for Urdu nastaliq glyphs was tested (SD10). No light and dark theme split is recorded on the design sheet; a separate dark-theme pass is [OPEN: Anum Siddiqui] |
| Declared locales | SMS templates: en-PK and Roman Urdu over GSM-7; ur-PK (RTL) over UCS-2 for the one string SD11 identifies as fitting only in UCS-2 (SD1, SD2). Agent-handset app: Urdu nastaliq glyphs tested on the confirmation screen (SD10). USSD menu: the menu is character-based over the gateway; no GSM-7/UCS-2 SMS encoding budget applies to USSD strings themselves (SD1 defines budgets for SMS segments); Urdu-script strings carried on the USSD menu were character-counted (SD8, SD9) and pseudo-localised on paper (SD12) but not device-tested for encoding behavior as SMS templates were. The localisation and RTL checklist [sahulat-localisation-rtl-checklist.md](sahulat-localisation-rtl-checklist.md) declares en-PK and ur-PK in scope for the agent handset. No other locale ships in this pass |
| Design brief this inventory fills deliverables for | [OPEN: scope is drawn instead from the design sprint's D9 decision and sprint questions SQ1 and SQ2, drafted into menu script v0.4 by Anum Siddiqui, owner Hira Baig, per [sahulat-design-sheet.md](sahulat-design-sheet.md)] |

Two of the template's default state groups are deleted for this scope, and said here rather than dropped silently. Empty is deleted: none of the three surfaces (a character-based USSD menu, an SMS template, a single confirmation screen) presents a list that can be empty. Form is deleted: no surface in scope collects more than one field at a time, so there is no multi-field submit to fail as a group; AC-2's bad-reference case is a single-field error and is carried under Error, field below. The template's Offline group is not given its own row: on this feature-phone flow a dropped USSD session is the only offline-adjacent signal the design sheet records, and it is already the dropped-after-debit and dropped-before-debit rows below (AC-7, AC-8); inventing a second, distinct "offline" state with no data behind it would be the fabrication this artifact exists to prevent. The template's Permission denied group is kept, but reassigned: Sahulat has no role-based access control surfaced anywhere in the journey or the design sheet, so the honest fit for that group is AC-13's KYC-tier refusal, a payment blocked by what the wallet is allowed to do rather than by who is looking, and it is filed there instead of left as an invented row.

## 2. The inventory

| State group | State | AC id | Story name | Test data or mock | Test type | Copy source | Recovery action | Owner | Story permalink (build id) |
|---|---|---|---|---|---|---|---|---|---|
| Default | Entry screen | [OPEN: AC id, Hira Baig] | USSD/Entry/Default | Falak Telecom short code dialed, no prior state | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Default | Biller choice | [OPEN: AC id, Hira Baig] | USSD/BillerChoice/Default | 3 billers listed (Ravi Power, Chenab Gas, Mehran Water removed per D5) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Default | Reference entry | AC-1 | USSD/ReferenceEntry/Default | a valid Ravi Power reference in BillBridge's test catalogue | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Success | Bill found | AC-1 | USSD/BillFound/Success | lookup at or under 8 seconds p95 (N56) | render, interaction | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Error, field | Bill not found | AC-2 | USSD/BillNotFound/ErrorField | a reference absent from BillBridge's 160-biller catalogue (N37) | render, a11y | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | "reference not found, check the number on your bill" | | |
| Default | Confirm amount | AC-3 | USSD/ConfirmAmount/Default | a looked-up bill and a wallet funded at or above the amount | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Default | Agent PIN-free confirm, AS-3 path | [OPEN: AC id, Hira Baig] | USSD/AgentPinFreeConfirm/Default | agent keys the bill, customer confirms on her own phone, no PIN shared (AS-3) | render, interaction | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Default | Agent PIN-entered confirm, fallback path | [OPEN: AC id, Hira Baig] | USSD/AgentPinEnteredConfirm/Default | agent keys the bill, customer's PIN entered on the agent's handset (E6) | render, interaction | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Loading | Initial, processing | AC-3 | USSD/Processing/LoadingInitial | debit request pending, within Falak Telecom's 180-second session ceiling (N66) | render | n/a | n/a | | |
| Success | Payment success | AC-3 | USSD/Success/Success | debit posted, SMS confirmation within 60 seconds (N56) | render, visual | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Error, dropped after debit | Session drops after the debit posts | AC-7 | USSD/DroppedAfterDebit/Error | idempotency key (ADR-2) written, session forced to drop after the debit call, within N66's 180-second ceiling | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | status SMS within 2 minutes confirms the payment went through (N56); no action needed | | |
| Error, dropped before debit | Session drops before the debit posts | AC-8 | USSD/DroppedBeforeDebitResume/Error | idempotency key written, debit not yet posted, session forced to drop, second dial from the same MSISDN | render, interaction | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | status SMS within 2 minutes says nothing was charged (N56); dial again to resume the same bill at the same amount | | |
| Error, duplicate | Already-paid block | AC-10 | USSD/AlreadyPaidBlock/Error | one completed payment, the identical reference and month replayed inside the 24-hour window (ADR-2, N56) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | "already paid on [date], reference [x]"; blocked 24 hours, no second debit | | |
| Error, permission denied (KYC tier) | Tier-limit refusal | AC-13 | USSD/TierLimitRefusal/Error | a lowest-tier wallet, a bill above that tier's limit | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | decline names the tier's limit in rupees; the rupee figure itself is Open, owner Amna Rasheed (routed, section 5) | | |
| Default | Agent handset, payment keyed | [OPEN: AC id, Hira Baig] | AgentApp/PaymentKeyed/Default | agent keys a bill on his handset for a customer at the counter (SD7) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Success | Agent handset, customer confirmed on her own phone | [OPEN: AC id, Hira Baig] | AgentApp/CustomerConfirmed/Success | AS-3 path, confirmation on the customer's own phone, AS-3 still an unverified assumption (test, not true), confirmation received on the customer's own phone (SD7) | render, interaction, a11y | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Error, abandoned | Agent handset, customer declined to confirm | [OPEN: AC id, Hira Baig] | AgentApp/CustomerDeclined/Error | customer does not confirm the keyed payment within the session (SD7); a non-confirmation is an abandonment of the session, not a field error | render, interaction | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | agent re-keys or asks the customer to confirm again | | |
| Success | SMS, payment confirmation | AC-3 | SMS/PaymentConfirmation/Success | SMS carrying the payment reference, within 60 seconds (N56) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Error, field | SMS, insufficient balance | AC-4 | SMS/InsufficientBalance/ErrorField | a wallet funded below the bill amount | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | states the shortfall to the rupee, offers a cash-in prompt | | |
| Error, dropped after debit | SMS, dropped-after-debit status | AC-7 | SMS/DroppedAfterDebitStatus/Error | forced drop after the debit call, status SMS after a dropped session within 2 minutes (N56) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a, payment already went through | | |
| Error, dropped before debit | SMS, dropped-before-debit resume prompt | AC-8 | SMS/DroppedBeforeDebitResumePrompt/Error | forced drop before the debit call, status SMS after a dropped session within 2 minutes (N56); rewritten by Naveed Akhtar after SD13's ambiguity finding | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | dial again to check; money may have moved (SD13's rewrite) | | |
| Error, duplicate | SMS, duplicate blocked | AC-10 | SMS/DuplicateBlocked/Error | identical reference and month replayed inside the 24-hour window | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a, payment already recorded | | |
| Error, permission denied (KYC tier) | SMS, tier-limit refusal | AC-13 | SMS/TierLimitRefusal/Error | a lowest-tier wallet attempting a bill above that tier's limit | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | names the tier's limit; rupee figure Open, owner Amna Rasheed | | |
| Success | SMS, agent-keyed confirmation to the customer's own phone | [OPEN: AC id, Hira Baig] | SMS/AgentKeyedConfirmation/Success | AS-3 path, new for pass 2 (SD6) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | n/a | | |
| Error, system | SMS, float-hotline escalation to the agent | [OPEN: AC id, Hira Baig] | SMS/FloatHotlineEscalation/Error | R1, agent float runs out on a bill-peak day; new for pass 2 (SD6) | render | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | agent calls the float top-up hotline (Gate 5 condition, owner Tariq Sohail) | | |
| Default | SMS, reminder three days before due date | AC-12 | SMS/Reminder/Default | carried in the template set (SD6) but unused while S11 stays balance-first and out of scope for the agent-assisted flow | n/a, out of scope this pass | [sahulat-ux-writing-guide.md](sahulat-ux-writing-guide.md) | STOP reply suppresses further reminders for that reference | | |
| Overflow | Screens flagged in the pseudo-localisation walk | [OPEN: AC id, Hira Baig] | USSD/Overflow/PseudoLocalisationExpansion | every string expanded 40 percent per SD12's walk; 2 of 14 screens (agent PIN-free confirm, dropped-before-debit resume) were expanded and then shortened | render | [sahulat-content-microcopy-audit.md](sahulat-content-microcopy-audit.md) | shortened before the usability round (SD12); closed | Anum Siddiqui | |
| Locale | Urdu script, RTL, UCS-2 | [OPEN: AC id, Hira Baig] | AgentApp/RTL-Urdu | Noto Sans Arabic tested against the app's Latin body face on 5 sampled devices (SD10); line height 1.8x for Urdu against 1.4x for Latin body copy (SD11) | render, a11y, visual | [sahulat-localisation-rtl-checklist.md](sahulat-localisation-rtl-checklist.md) | n/a | | |
| Viewport | Agent handset, 5.0-inch smallest sampled screen | [OPEN: AC id, Hira Baig] | AgentApp/Viewport-5in | 5 of the pilot district's devices sampled from N6's 600-agent cohort (SD10) | visual | n/a | n/a | | |

## 3. Coverage arithmetic

| Ratio | Count | Total | Result |
|---|---|---|---|
| Rows with an AC id / all rows | 17 | 29 | 59% |
| Rows with a story permalink at Gate 4 / all rows | 0 | 29 | 0% |

The second ratio is 0 percent for a real reason, not an oversight: pass 2 has not reached BUILD, and [sahulat-design-sheet.md](sahulat-design-sheet.md) is explicit that no pass-2 gate outcome is asserted before the journey or the coverage sheet records one. A 0 percent permalink ratio at this point in the pass is the honest reading, not a gap to explain away.

The first ratio counts every row in section 2 above (29 rows), including those marked out of scope or closed. A row is counted as having an AC id if its "AC id" column contains a specific AC identifier (e.g., AC-1), not if it contains an [OPEN] placeholder. 17 rows carry such an identifier.

## 4. Visual-baseline acceptances

No visual-baseline acceptance has occurred yet. USSD and SMS carry no pixel baseline at all, being character-based; the only surface with a pixel baseline is the agent-handset app's confirmation screen, and SD10's typeface test and SD11's line-height test are pre-BUILD design decisions, not accepted changes against a shipped baseline. This table stays empty until BUILD produces a first baseline to accept or reject changes against.

| Date | State (row above) | What changed | Decision-log entry | Accepted by (non-author role) |
|---|---|---|---|---|
| | | | | |

## 5. Findings routed

| Finding | Row (state) | Severity | Routed to (backlog item, risk register row) | Owner | Fix by |
|---|---|---|---|---|---|
| AC-13's KYC-tier rupee limit has no figure, so both tier-limit rows above cannot carry a numeric threshold in their copy | USSD/TierLimitRefusal/Error, SMS/TierLimitRefusal/Error | High | [sahulat-acceptance-criteria.md](sahulat-acceptance-criteria.md) AC-13, DEP-3's memo | Amna Rasheed | [OPEN] |
| The float-hotline escalation (R1, agent float runs out) has an SMS to the agent (SD6) but no agent-handset screen state showing the agent that a cash-in cannot post for lack of float | SMS/FloatHotlineEscalation/Error | Medium | `sahulat-state-diagram.md` (design sheet artifact map; not yet a link) | Anum Siddiqui | [OPEN, before pass-2 DESIGN closes] |
| SAHULAT-S4, the agent seeing a confirmation on his own handset for a payment he did not key, remains "not covered" per the acceptance criteria's own gap table and has no row above | Agent-handset states, section 2 | Medium | [sahulat-acceptance-criteria.md](sahulat-acceptance-criteria.md), gap table, SAHULAT-S4 | Hira Baig | [OPEN, D8's next-pass scope] |
| Two screens were flagged in the pseudo-localisation walk and shortened before the usability round | USSD/Overflow/PseudoLocalisationExpansion | Low, closed | [sahulat-content-microcopy-audit.md](sahulat-content-microcopy-audit.md) | Anum Siddiqui | 2026-09-20 (closed) |

## How this artifact fails while looking complete

Pass 1's own history names the failure mode most worth checking here. AC-8's resume-on-next-dial half was written as a row, not skipped, at Gate 2; it was accepted as a listed miss at Gate 4 because no story permalink ever backed it, and the gap fed 61 duplicate-payment tickets and the M3 breach in launch week (N47, D7). A table with a row for every state and a permalink for none of them is not thoroughness, it is exactly that shape again, which is why section 3's 0 percent permalink ratio above is stated in full rather than rounded away or left for a reader to notice on their own.

The second risk this pass carries is scope drift on locale. SD10 and SD11 test Urdu RTL rendering only on the agent-handset app's confirmation screen; the USSD menu and the SMS templates carry Urdu-script strings (SD1, SD2, SD6) but were never device-tested for rendering the way the app screen was, only character-counted (SD8, SD9) and pseudo-localised on paper (SD12). A reader skimming this file could assume the "Locale" row above proves RTL correctness across all three surfaces; it proves it for one of them, and section 1 says so, but the distinction is easy to lose once the row exists.

## Sibling artifacts

- [Sahulat acceptance criteria](sahulat-acceptance-criteria.md), which supplies the AC ids this file's rows trace to, and the two tier-limit rows and AS-3-path rows this file sends back as [OPEN: AC id] candidates
- [Sahulat UX writing guide](sahulat-ux-writing-guide.md), which owns the copy for every state whose Copy source column points at it, including the status-SMS pattern this file's dropped-session rows both use
- [Sahulat localisation and RTL checklist](sahulat-localisation-rtl-checklist.md), which walks the Urdu RTL evidence this file's Locale row only summarises
- [Sahulat content and microcopy audit](sahulat-content-microcopy-audit.md), which owns the character-budget and pseudo-localisation evidence behind this file's Overflow row
- [Sahulat design sheet](sahulat-design-sheet.md), the source for every SD id this file cites and the artifact map this file's screens and strings are drawn from
- [Component spec](../templates/architecture/component-spec.md), which would link here for the state list and add only implementation detail; no filled Sahulat example exists for it yet
- [Design review record](../templates/architecture/design-review-record.md), which would link here rather than re-listing states as review checklist items; no filled Sahulat example exists for it yet
- [Testing strategy](../templates/delivery/testing-strategy.md), which this inventory would feed with the test type column once a filled Sahulat example exists
- [Edge cases](../templates/delivery/edge-cases.md), which holds behavioral edges rather than which visual state renders; no filled Sahulat example exists for it yet

## Exit gate (feeds Gate 2: Requirements signed off)

Done when every box is honestly ticked. This inventory travels with the pass-2 design brief, once one is filed (section 1), toward [Gate 2](../os/STAGE-GATES.md); the story permalink column completes in BUILD and is checked at [Gate 4](../os/STAGE-GATES.md). No pass-2 gate attempt is scheduled yet, matching [sahulat-design-sheet.md](sahulat-design-sheet.md)'s reconciliation note that no pass-2 gate outcome is asserted before the journey records one; this walk is this document's own completeness check, not a claim that Gate 2 has convened.

- [x] Section 1 declares every screen or component, viewport, theme, and locale this inventory claims to cover, and no row claims more. Two groups (Empty, Form) are deleted with reasons; Offline is folded into the dropped-session rows rather than invented separately; Permission denied is reassigned to AC-13's KYC-tier refusal rather than invented
- [x] Empty and error each carry a row per distinct cause, not one collapsed row. Error splits into field, dropped-after-debit, dropped-before-debit, duplicate, permission denied (KYC tier), system and abandoned, seven distinct causes across 12 error rows; Empty is deleted, not collapsed, per section 1
- [x] Every row has a state, a test type, and a recovery action or an explicit "n/a"
- [x] No downstream artifact in the sibling list above re-enumerates this file's states; each links here instead
- [x] The coverage arithmetic in section 3 is recounted from this file's own rows, not carried over from a previous count
- [ ] Every accepted visual-baseline change in section 4 is accepted by someone other than its author. No baseline exists yet; section 4 is empty until BUILD produces a first one, so this box cannot honestly be ticked before then
- [x] Every finding in section 5 has an owner and a routed destination
- [x] Signed by Hira Baig, 2026-10-05
