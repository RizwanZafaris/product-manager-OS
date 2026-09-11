# UX Writing Guide: Sahulat Bill Pay

Fills [templates/definition/ux-writing-guide.md](../templates/definition/ux-writing-guide.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, the people are fiction, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Product owner:** Hira Baig · **Content design lead:** Hira Baig (the only PM; she also owns content at this artifact weight) · **Date:** 2026-03-13 · **Status:** Agreed at Gate 2 attempt 2, 2026-03-25; annotated after Gate 4 (2026-06-10) and the post-launch review (2026-08-21), annotations marked as such
**Links:** [design brief](sahulat-one-pager.md) · [personas](sahulat-personas.md) · [accessibility checklist](../templates/architecture/accessibility-checklist.md) · [localisation and RTL checklist](../templates/architecture/localisation-rtl-checklist.md)

## 1. Who we write for

| Persona (link) | What they are trying to do | Reading context | Channel (in-product, email, push, SMS, support script) |
|---|---|---|---|
| P1 Shazia ([personas](sahulat-personas.md)) | Look up her Ravi Power bill by the reference on the paper, pay it, and hold proof before the due date | USSD menu, feature phone, no screen scroll; reads one line at a time under time pressure near a counter; will not return to re-read | in-product (USSD text), SMS confirmation, status SMS after a dropped session |
| P2 Rafiq ([personas](sahulat-personas.md)) | Answer "did my customer's bill go through" at the counter without sending them away again | Agent handset, queue of customers behind him; skims, does not read every word; needs a yes/no and a number, not a sentence | agent-handset confirmation, support script, float top-up hotline |
| Support agent on Naveed Akhtar's team | Look up a payment by reference and tell the caller whether money moved | Call centre console, reading aloud while the customer listens; needs plain words that survive being spoken | support script, SMS resend |
| First-time applicant (not a persona; listed for completeness) | Complete a form they have never seen before, under time pressure | Full attention, first pass; will not return to re-read | in-product |

## 2. Voice principles

| Principle | Do (product's own words) | Don't (product's own words) |
|---|---|---|
| Plain over formal | "Pay PKR 2,400 now." | "Please proceed with the settlement of your outstanding utility obligation." |
| Specific over reassuring | "Bill paid. Reference 78421. Sent to Ravi Power within 30 minutes." | "Your transaction was successful. Thank you for using Sahulat." |
| Name the rule, not the feeling | "You can pay up to PKR 25,000 a month. Your tier limit is reached." (AC-13) | "We are sorry, but something went wrong." |
| Short enough for one USSD line | "Not enough balance. Cash in at an agent." | "The amount you wish to pay exceeds the available funds in your wallet. Please visit an authorised agent to add more funds." |

## 3. Message patterns

### 3.1 Error

Say what happened and how to fix it, in plain, positive language, next to the field it belongs to (standard; GOV.UK Design System, error-message component). Never use an error message for something the user cannot fix, such as ineligibility or a service outage; send them to a page that explains the problem and what to do next instead (standard; same source). Avoid technical jargon and words that blame the user, "forbidden," "illegal," "you forgot"; avoid "please," because it implies a choice, and "sorry," because it does not help fix the problem (standard; same source).

| Situation | Message pattern | Example (ILLUSTRATIVE) |
|---|---|---|
| Field left empty | An instruction: "Enter [what is missing]" | "Enter your Ravi Power reference number" |
| Unknown reference (AC-2) | A description naming the rule | "Reference not found. Check the number printed on your bill." |
| Insufficient balance (AC-4) | State the gap and the fix | "PKR 1,200 short. Cash in at an agent, then dial again." |
| Tier-limit refusal (AC-13) | Name the limit and what to do next | "Monthly limit PKR 25,000 reached. Visit a Sahulat agent to raise your tier." |
| The user cannot fix the problem (outage, aggregator down) | Route to an explanation, not an inline error | Open: link the problem page Sahulat uses. Owner: Hira Baig. Date: before Rel-2 scope freeze. |

### 3.2 Empty

State what would normally be here, then give a direct path into the task that would fill it (standard; Carbon Design System, empty-states pattern; Nielsen Norman Group, "Designing Empty States in Complex Applications"). Distinguish a first-use empty state from the result of a user's own filter or search, from an error state; each needs a different sentence, because "nothing here yet" and "nothing matches" are not the same fact.

**This product's decision:** First-use empty (no saved references): "No bills saved yet. Dial *123* to look up your first bill." Search-with-no-results (a reference entered that returns nothing): "No bill found for that number. Check the digits on your paper bill." These two sentences are never swapped; a customer who has looked up three bills and typed a fourth reference gets the second, not the first.

### 3.3 Success

Confirm what happened, in the past tense, without inviting a second look for reassurance the action already succeeded.

**This product's decision:** "Bill paid. PKR 2,400 sent to Ravi Power. Reference 78421. You will get an SMS within 60 seconds." (AC-3, N56.) No "Thank you," no "Your satisfaction matters," no prompt to check the ledger again. The SMS carries the same reference so the customer holds proof on paper (or in the SMS log) without needing the app open.

### 3.4 Confirmation

Use a confirmation step only before an action with serious consequences, destroying work, an irreversible charge, or anything that cannot be undone (standard; Nielsen Norman Group, "Confirmation Dialogs Can Prevent User Errors, If Not Overused"). Prefer undo to confirmation wherever the action can be reversed after the fact. A generic "Are you sure?" on a reversible action trains people to click through it, which removes the protection on the one action later that actually needed it.

**This product's decision:** One confirmation, on USSD, before the debit call fires: "Pay PKR 2,400 to Ravi Power? Press 1 to confirm, 2 to cancel." (ADR-2's phase boundary.) No confirmation on lookup, no confirmation on saving a reference, no confirmation on opting out of reminders (AC-12). The duplicate-payment block (AC-10) makes a second identical attempt impossible without a new reference, so the confirmation step protects against the wrong biller or the wrong amount, not against paying twice.

### 3.5 Notification, by persistence

State how long a message stays on screen as a product decision, not a default (standard; Carbon Design System, notification pattern): an inline notification stays until the user dismisses it or the underlying state resolves; a toast without an action can clear itself; a toast or banner carrying an action stays until the user acts or dismisses it. Use a page-level banner sparingly. There is evidence people miss banners placed outside the content they are reading, so information belonging to the current task goes in the main content, not a banner above it (standard; GOV.UK Design System, notification-banner component).

| Message type | Persistence | This product's rule |
|---|---|---|
| Inline (next to a field or row) | Until dismissed or resolved | USSD has no persistent inline layer; every inline message is the single response line and disappears when the next keypress arrives. The confirmation SMS is the durable record. |
| Toast, no action | Can clear on its own | Not applicable on USSD. On the app (SAHULAT-S10), a success toast clears after 8 seconds; it carries no action. |
| Toast or banner with an action | Until acted on or dismissed | Not applicable on USSD. On the app, a tier-limit banner (AC-13) persists until the customer visits an agent or raises tier; it names the limit in the banner text itself. |
| Status SMS after a dropped session | Delivered within 2 minutes of the drop (N56, AC-7/AC-8); no further SMS if the customer dials again and resumes | "Session ended. Money did not move. Dial again to resume." or "Session ended. PKR 2,400 paid. Reference 78421." Exactly one of these two, never both, never neither. |

### 3.6 Form validation timing

State this product's decision once here, and link it from every form so no screen re-derives it. Validating inline, field by field, rather than only on submit, measured higher task success and fewer errors, plus 31% higher satisfaction, 42% shorter completion time and 47% fewer eye fixations, in a small usability study across six form variants (research evidence, one study; Wroblewski, "Inline Validation in Web Forms," tested with Etre). Treat the finding as a reason to default to inline validation, not as a number this product can cite as its own; a product that validates differently should say why and where.

**This product's decision:** Hybrid, dictated by channel. USSD (the majority surface) validates on submit per step: the customer enters a reference, presses send, and receives either the bill or an error; there is no keystroke-by-keystroke feedback on a feature-phone keypad. The app (SAHULAT-S10) validates the reference format inline as the customer types, because the app has a cursor and a keyboard. Owner: Hira Baig, agreed 2026-03-13. Zainab Qureshi confirmed the USSD constraint on 2026-03-13: Falak Telecom's gateway delivers the whole string on send, not character by character.

## 4. Banned and preferred words

Seeded from the GOV.UK Design System error-message component (adapt under licence: Open Government Licence v3.0, Crown copyright; this section contains public sector information adapted from the GOV.UK Design System under the Open Government Licence v3.0, https://design-system.service.gov.uk/components/error-message/). Add product-specific rows below the seed; never delete a seed row, only add "unless" exceptions this product has actually decided.

| Banned | Why | Prefer instead |
|---|---|---|
| forbidden, illegal, prohibited | Blames the user for a system decision | State what to do instead |
| you forgot | Assumes carelessness the product cannot know | "Enter [field]" |
| please | Implies the action is optional | Remove it; state the instruction plainly |
| sorry | Does not help the user fix the problem | Remove it; lead with the fix |
| valid, invalid | Adds nothing a specific rule does not already say | Name the actual rule broken |
| error 0x0000000643, unspecified error, and other technical codes | Meaningless to the reader | Plain-English description of what happened |
| utilize | Longer than the plain word, no added meaning | use |
| "transaction" | Too abstract for a woman holding a paper bill at a counter | "bill payment" or "payment" |
| "initiate", "execute", "process" | Agency language; the customer pays, the system does not act on her behalf | "pay", "send" |
| "your request has been received" | Says nothing about whether money moved, which is the only question after a dropped session (E4, INT-007) | "Money did not move" or "PKR [amount] paid" |
| "kindly" | Regional politeness filler that adds length on a 160-character SMS segment and implies optionality | Remove it; state the instruction |
| "network issue", "system busy" | Names no cause the customer can act on | "BillBridge is slow. Try again in 5 minutes." or route to the problem page |

## 5. Terminology glossary

One term, one meaning, used the same way on every screen, in every message, and in support scripts. A second term for the same concept is a silent bug: a user who has learned one word does not recognise the other.

| Term | Meaning in this product | Never use instead |
|---|---|---|
| Reference number | The 10-to-14 digit number printed on the paper bill, keyed into USSD to look up the amount owed | Consumer number, account number, subscriber ID (these appear on some bills beside the reference and caused UF-1 in the usability round: 2 of 5 customers entered the consumer number instead) |
| Bill payment | A completed transfer from a Sahulat wallet to a biller through BillBridge | Transaction, remittance, settlement |
| Wallet balance | Money sitting in the Sahulat account, spendable within 30 seconds of a cash-in (N56) | Account, fund, stash |
| Agent | A licensed Sahulat point-of-service operator who performs cash-ins and cash-outs at a counter | Shopkeeper, dealer, retailer (these describe the shop, not the person doing the service) |
| Cash-in | Adding money to the wallet at an agent counter | Deposit, top-up, load (top-up implies airtime) |
| Tier | The KYC level attached to a wallet, which sets the monthly payment limit checked by AC-13 | Level, grade, class |
| Status SMS | The message sent within 2 minutes of a dropped USSD session telling the customer whether money moved (N56) | Alert, notification, update |

## 6. Numbers, money, dates and time

Never hand-encode a locale's number, date or currency format. Read it from the platform's Unicode CLDR-backed formatting library (ICU or equivalent) at run time (standard; Unicode CLDR project, https://cldr.unicode.org/index); a hand-built table drifts out of date the day CLDR next publishes and silently mis-formats a market this product has not tested. The localisation and RTL checklist (../templates/architecture/localisation-rtl-checklist.md) carries the structural walk this rule feeds.

| Element | Rule | Evidence class |
|---|---|---|
| Decimal and thousands separators | Read from CLDR per locale; never assume comma-decimal or period-decimal. In en-PK the grouping separator is a comma and the decimal separator is a period: "PKR 2,400". | standard (Unicode CLDR) |
| Calendar | Read from CLDR per locale; never assume Gregorian. Bill due dates come from BillBridge as Gregorian; display follows the device locale. | standard (Unicode CLDR) |
| Currency display | Read symbol, placement and rounding from CLDR per locale. PKR is always written with the unit before the amount: "PKR 2,400", never "Rs. 2,400" or "2,400 Rs". | standard (Unicode CLDR) |
| Date order and separators | Read from CLDR per locale; never assume day-month-year. Due dates in USSD responses use DD-MM-YYYY: "Due 05-09-2026". | standard (Unicode CLDR) |
| Relative time ("2 hours ago") | Open: cutoff before switching to an absolute date. Owner: Hira Baig. Needed by: Rel-2 scope freeze. | product decision |

## 7. Languages and scripts

This section names the operating facts; the walk that proves them lives in the localisation and RTL checklist (../templates/architecture/localisation-rtl-checklist.md).

| Field | Value |
|---|---|
| Source language this guide is written in | English (en-PK). All USSD menus, SMS templates, support scripts and acceptance criteria are authored in English; Urdu (ur-PK) is the target translation language for the second pass. |
| Translation workflow | Open: vendor or in-house process for ur-PK. Owner: Hira Baig. Needed by: Rel-2 scope freeze. |
| Reviewer per shipped language | English: Hira Baig (author and reviewer are the same person at this artifact weight; flagged as a risk in the accessibility checklist walk). Urdu: Open, name required before any Urdu string ships. |
| Channel encoding budgets (SMS segment length, push character limit, email subject limit) | SMS: 160 characters per segment on Falak Telecom's gateway (N40's contract governs cost, not length; segment count drives PKR 1.2 x segments). Push: not shipped in Rel-1. Email: not shipped in Rel-1. USSD response: 182 GSM-7 characters is the 3GPP standard's theoretical maximum per page (TS 23.038 and TS 23.090); Falak Telecom's gateway contract enforces less, 160 characters per menu page (corrected 2026-09-26, see the change log; the design sheet's SD9 and the content and microcopy audit's channel arithmetic confirm 160 as the actual contracted line). |

## 8. Accessible copy

The evidence column and the walk itself belong to the accessibility checklist (../templates/architecture/accessibility-checklist.md); this section states the content-level rules that checklist verifies.

- Link text makes sense read on its own, out of the sentence around it; never "click here" or "read more" with no named destination. On USSD there are no links; the rule applies to the app flow (SAHULAT-S10) and to any future web portal.
- Every image that carries meaning has alternative text stating that meaning; a decorative image is marked so a screen reader skips it. USSD has no images. The app's biller logos carry the biller name in alt text; a logo alone is never the only label.
- No instruction is given by colour or position alone ("the button on the right," "the red one"); pair it with a name or a label a screen reader also announces. USSD uses numeric keys only: "Press 1 to confirm, 2 to cancel." The app pairs every colour-coded state with a word: "Paid" not just green, "Failed" not just red.
- Every input has a visible label; a placeholder is never the only label, because it disappears the moment the user starts typing. On USSD the prompt IS the label: "Enter reference:" appears before the input line. On the app, the field label sits above the input and survives focus.

## 9. Change log

| Date | Change | Owner |
|---|---|---|
| 2026-03-13 | Guide created, first draft | Hira Baig |
| 2026-03-25 | Agreed at Gate 2 attempt 2; voice principles locked, message patterns signed | Hira Baig |
| 2026-06-10 | Annotation after Gate 4: AC-8 resume half accepted as the one miss; the status-SMS pattern in section 3.5 is unchanged (it describes the intended behaviour; the resume-on-redial half of AC-8 deferred to Rel-2 means the "dial again to resume" branch is not yet live) | Hira Baig |
| 2026-08-21 | Annotation after the post-launch review: 61 DUP-PAY tickets in week 1 (N47) despite AC-10 holding zero confirmed second debits; the ticket volume traced to customers calling support because the status SMS had not arrived within 2 minutes on some sessions (timeout spike, N67), not to a wording failure. Section 3.5's persistence rule is unchanged; the operational fix was the timeout patch shipped 2026-07-14, not a copy change. | Hira Baig |
| 2026-09-26 | Correction: section 7's USSD response budget restated as 160 GSM-7 characters, Falak Telecom's actual enforced page limit, not the 182-character 3GPP theoretical maximum this row previously quoted; the content and microcopy audit's channel arithmetic (2026-09-24 to 2026-09-26) is what caught the gap between the standard's ceiling and the gateway's contract | Hira Baig |

---

## How this guide fails while looking complete

A voice-principles table filled with adjectives no competitor would ever disagree with, "friendly," "clear," "helpful," is not a decision; it is decoration, and a writer under deadline learns nothing from it that they did not already believe. The tell is a message-pattern section that restates the seed rows without a single product-specific "this product's decision" line filled in: a guide that never commits to inline-versus-submit validation, a banner persistence rule, or a reading-context table has not yet been used on a real screen. The other failure is silent drift: a glossary term that a new feature quietly renames without updating this file, so two words now mean the same thing in different parts of the product and support cannot tell users which one to trust.

In Sahulat's case the third failure mode is channel blindness: writing a voice guide for the smartphone app and shipping 94 percent of payments on USSD (CN28: 56,300 of 61,500 lookups were USSD in FW-1). A principle like "confirm what happened, in the past tense" is trivially satisfied by a 160-character SMS but requires deliberate truncation logic on a 160-character USSD response line (Falak Telecom's enforced page budget, not the 182-character 3GPP theoretical maximum). This guide's section 2's fourth principle exists because that arithmetic forced it.

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The agreed guide travels with the [design brief](sahulat-one-pager.md) to [Gate 2](../os/STAGE-GATES.md), and its message patterns become the standard [spec-review](../skills/spec-review/SKILL.md) checks every new screen against.

- [x] Section 1 names a real reading context per persona, not "all users": Shazia reads one USSD line at a time at a counter; Rafiq skims an agent handset with a queue behind him; a support agent reads aloud while the caller listens.
- [x] At most 4 voice principles, each with a do and a don't in the product's own words, none copied from a vendor voice guide. Four principles, all four with product-specific examples drawn from AC-3, AC-13, and the USSD character budget.
- [x] Every message pattern in section 3 that this product ships has its own "this product's decision" line filled in, not left on the seed default. Sections 3.2 through 3.6 each carry a decision line; 3.1's last row is Open (the problem page URL), owned by Hira Baig.
- [x] The banned and preferred words table keeps every seed row and its Open Government Licence attribution intact. All six seed rows present; five product additions below them.
- [x] Every glossary term has exactly one meaning and at least one "never use instead" entry. Seven terms, seven "never use" entries.
- [x] Section 6 points to CLDR at run time; no hand-encoded locale table appears in this file. Rules stated; formats read from ICU at run time.
- [ ] Section 7 names a reviewer for every shipped language. English: named (Hira Baig, with the author-equals-reviewer flag). Urdu: Open, name required before any Urdu string ships. Not yet closed; Urdu is not shipped in Rel-1, so this box remains unticked at Gate 2 and must close before any ur-PK string reaches production.
- [x] Section 8's rules are checked against the accessibility checklist's evidence, not asserted here alone. Each bullet maps to a checklist item; the USSD-specific constraints (numeric keys, no images, prompt-as-label) are verified in the checklist's walk.
- [x] Signed by the product owner and the content design lead, Hira Baig, 2026-03-25.
