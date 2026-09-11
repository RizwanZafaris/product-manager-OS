# Sales Enablement One-Pager: Expense Copilot Add-on

Fills [templates/delivery/sales-enablement-one-pager.md](../templates/delivery/sales-enablement-one-pager.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, Cinderwick is a fictional competitor, and every count, dollar figure and date is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so this page can be checked against the documents it derives from. See the [examples index](README.md).

**Owner:** Tomas Lindqvist, head of product marketing · **Date:** 2026-11-06 · **Status:** Approved 2026-11-06; section 1's Enterprise note added 2026-11-23 once R4 opened, closed 2026-12-03 by D5; section 3's proof row updated 2026-11-23 once phase 1 closed (N44); section 3's demo step 3 added 2026-11-13 once LEDGERLINE-S5 shipped; section 4's Cinderwick do-not-say updated 2026-12-03 once R4 closed (R4, D5); section 4 row 1's do-not-say updated 2026-12-17 once the win-loss review was signed; section 7's feature-request routing updated 2026-11-10 once the advisory board was chartered, and its forum names updated again 2026-12-22 to match the feedback program's corrected charter; section 7's lost-deals line updated 2026-12-17 once the win-loss review was signed; section 4 row 1 and section 5 marked withdrawn 2026-12-21 per D6, after the per-seat price failed its own kill rule
**Derived from:** [positioning.md](ledgerline-positioning.md), signed 2026-10-30 · [pricing-packaging.md](ledgerline-pricing-packaging.md), signed 2026-11-03, section 1 reopened 2026-12-21 · [gtm-plan.md](ledgerline-gtm-plan.md), signed 2026-11-06 · **Valid until:** the next pricing change. That arrived 2026-12-21 (D6); section 5 and section 4 row 1 are withdrawn, not reprinted, until pricing-packaging.md section 1 is re-signed

## 1. Who it is for

| Field | Answer |
|---|---|
| Best-fit buyer | Account admin with billing authority on a Business-plan account in segment S-5: first-submission approval under 75%, five or more filers (N36) |
| Trigger events that make them care now | The account is shopping receipt-capture vendors and has already looked at Cinderwick; a finance lead mentions keeping a spreadsheet alongside the Expenses form |
| One question that qualifies them | "What's your team's first-submission approval rate on expense reports, and roughly how many people file them?" Yes if approval is under 75%, roughly one bounce in every four reports, and five or more people file, which is where S-5 is drawn (N36) |
| Who this is NOT for, and what to offer them instead | Starter-plan accounts: no reviewer workflow exists to draft into, out of scope (N30); no upgrade path is defined in v1, Open: Isabel Ferreira owns whether one is built. Enterprise accounts (S-6, 310 accounts, N31): sold bespoke through the Enterprise motion; **(added 2026-11-23, when R4 opened; closed 2026-12-03 by D5)** two Enterprise prospects were nonetheless quoted from this add-on's list price while held on a DPA subprocessor question, and closing that gap is not this page's problem to solve (N79) |

## 2. Pains and the alternative

All figures ILLUSTRATIVE, drawn from the six design-partner interviews (EV-C01 to EV-C06, N40, 2026-10-19 to 2026-10-28), the platform data pull (EV-C07, N32 to N38), and the Q3 support-ticket pull (EV-C09, N38). No interview transcript in this workspace carries a verbatim buyer quote, so this table paraphrases rather than invents one.

| Pain, paraphrased from what the customer describes (no verbatim quote exists in this workspace, see the note above) | What they do today instead | What that costs them | Evidence |
|---|---|---|---|
| A report bounces back for a wrong category or a missing field, and the filer has to resubmit | Type receipt data straight into the Expenses form, no draft | Median first-submission approval of 66% across S-1, the design partners' own Q3 baseline at 64% before any product touched it; internally, a bounce costs about 30 minutes across the filer and the reviewer combined, an estimate from the internal build's own cost model, not yet measured at a customer account (N14); internally, median filing time was 25 minutes before the copilot (N5) and 12 minutes from first receipt to submit with it (N23), both on Ledgerline's own reports, not a customer account | EV-C07 (N32, N33, N35, N44); EV-C01 to EV-C06 (N40, 6 of 6 named bounces) |
| Finance keeps a shadow spreadsheet because the Expenses form has no place for the account's own policy | Maintain a shared spreadsheet alongside the form | Manual double entry, and whatever the sheet's owner remembers to update | EV-C01 to EV-C06 (N40, 4 of 6 keep one today) |
| Trialled a separate receipt-capture tool that doesn't feed the approval flow (2 of 6) | Trialled Cinderwick, a seat-priced vendor at $8 per seat per month, quoted (N13) | A separate login, a separate vendor contract, and the drafted result still has to be moved back into the Expenses form by hand | EV-C01 to EV-C06 (N40, 2 of 6 had trialled Cinderwick); Q3 win-loss batch (N37, EV-C08, 7 of the 9 lost deals that named receipt capture chose Cinderwick) |
| Reviewers spend mechanical time on category and receipt problems instead of judgment calls | Nothing; it's absorbed as review overhead | 610 support tickets tagged category or receipt in Q3 alone | EV-C09 (N38) |

## 3. What it does, with proof

| Claim, in one sentence | Proof | Status |
|---|---|---|
| Drafts the line item, with matched receipt and category, inside the same Expenses workflow the account already approves reports through | Demo step 1; LEDGERLINE-S2 | unproven at signing (2026-11-06); proven by live demo for the six design partners from 2026-11-10 (LEDGERLINE-S2) |
| Matches drafted fields to the account's own written policy, not a generic category list | Demo step 1; positioning.md section 2, attribute 2 | unproven at signing (2026-11-06); proven by live demo from 2026-11-10 (LEDGERLINE-S2) |
| Flags each drafted field with the model's confidence, so the reviewer spends judgment where it's needed | Demo step 2; LEDGERLINE-S3 | unproven at signing (2026-11-06); proven by live demo from 2026-11-10 (LEDGERLINE-S3) |
| Saves the filer time on each report | Internally, a target of 15 minutes per drafted report, about $13.75 at the internal filer rate (N15); this is a target, not evidence, and not yet measured at a customer account | unproven |
| Fewer bounces means the reviewer stops re-checking what the filer was already told | Unproven at signing (2026-11-06): no customer measurement exists yet; to be judged against S-1's 66% baseline (N35) and the design partners' own Q3 baseline of 64% (N44). **Updated 2026-11-23:** phase 1 closed at 224 of 412 eligible reports drafted (54%) and 173 of those approved first time (77%), against that same 64% baseline (N44), and 4 of 6 partners met the phase 1 exit condition (N45) | unproven at signing; proven for the six design partners as of 2026-11-23 (N44, N45) |

**The one sentence a rep should say first:** It drafts the line item from the receipt, matched to your policy, inside the Expenses approval flow you already use. No new login, no new vendor.

## 4. Objections

| Objection | Honest answer | Proof or pointer | Do not say |
|---|---|---|---|
| "You'll bill us for every seat, even people who barely file" | **Withdrawn 2026-12-21 per D6, alongside section 5: the price this answer priced against failed its EXP-1 kill rule.** Yes, it is priced per plan seat, the seat count on your account, not per filer or per report; see the pricing pointer in section 5 for the current price. Do not quote a price until pricing-packaging.md section 1 is re-signed | pricing-packaging.md section 1 (D3, reopened 2026-12-21 per D6); pricing pointer, section 5 below | "It's basically free once you count the time it saves." This is the exact framing EXP-1 tested against the reviewer's hourly cost, and the framing the win-loss review later found had lost deals; do not lean on it (win-loss review signed 2026-12-17, added to this row that date) |
| "Why isn't this included in the Business plan?" | No, it carries a real per-report model cost that the flat plan price does not, so it needs its own revenue line. A free bundle was considered and rejected on margin (D2); we do not have a date for when, or whether, that changes | pricing-packaging.md section 2 (D2, N50, N51) | "It'll probably be free later." "We can throw it in." Neither is a decision anyone has made |
| "We already have Cinderwick, why switch?" | Fair. If Cinderwick already does the extraction, the difference is that this activates on the account you already run: no second login, no second vendor contract. Whether it also avoids a second security review depends on your own DPA; whether our model provider is covered as a subprocessor under your DPA is an open item with the legal lead (positioning.md section 2, attribute 3), so route the questionnaire there. **Updated 2026-12-03 (D5, DEP3):** the customer DPA now names the model vendor as a subprocessor, on the model vendor's standard terms with 30-day prompt retention and the existing no-training clause | Demo step 1; positioning.md section 2, attribute 3 (N13) | "No security review needed." Two Enterprise prospects were held on exactly this subprocessor question until D5 closed it on 2026-12-03 (R4, added to this row that date); do not promise a smaller account will skip the same check |
| "Does it read our receipts correctly?" | It proposes fields with a confidence flag; the filer confirms every field before submitting, and the reviewer sees each field's confidence flag. Internally, reviewers caught extraction errors on about 2.1 of every 100 drafted reports (N24) | Demo step 2; internal metrics review, N24 | "It is always right" |
| "What about receipts that aren't in English?" | Honestly, not yet reliable. Foreign-language receipts are an open risk (R3); do not promise it for an account whose filers submit non-English receipts | R3 in the journey's shared risks; do not demo a non-English receipt | "It handles any language" |
| "Why trust an AI category guess over our own spreadsheet?" | It matches drafted fields against the account's own written policy, which a spreadsheet only does if someone maintains it by hand every time the policy changes | Demo step 1; positioning.md section 2, attribute 2 | "AI is smarter than a spreadsheet." The comparison isn't intelligence, it's that the spreadsheet has no policy engine behind it |

## 5. Pricing pointer

**Withdrawn 2026-12-21 per D6.** The per-seat price this section pointed to failed its own pre-declared kill rule (EXP-1: pooled conversion 2.7%, both arms under the 4.0% floor) and pricing-packaging.md section 1 is reopened. Do not quote a price on this add-on until a replacement pointer is signed; route pricing questions to Isabel Ferreira. What follows is the pointer as it stood from 2026-11-06 to 2026-12-21, kept for the record rather than deleted, and it carries no numbers:

- Tier or package this sits in: the single Copilot add-on tier (pricing-packaging.md section 3)
- Value metric it is priced on: plan seats, per pricing-packaging.md section 1 (D3); that value metric is exactly what D6 reopened
- Where the current price list lives: pricing-packaging.md, section 3
- Who may quote, and discount authority: account executives quote from the current price list in pricing-packaging.md, section 3; Ruth Adeyemi for prepay; Isabel Ferreira for anything else. No standing discount without Isabel Ferreira's sign-off outside the two rules on file: annual prepay, approved by Ruth Adeyemi, and the design-partner rate, approved by Isabel Ferreira, offer expires to new partners 2026-12-31 (N48; expiry date per N42)
- What is NOT included and costs extra: no upgrade tier exists; Enterprise accounts (S-6) are sales-led but two Enterprise prospects were nonetheless quoted from this list (N79), a gap withdrawn along with the two quotes on 2026-12-21 (N88)

## 6. Demo path

| Step | What to show | What to say | What to avoid | Time |
|---|---|---|---|---|
| 1 | A filer photographs or forwards one clear, English-language receipt and the drafted line item appears, matched to the account's own policy category (LEDGERLINE-S2) | "This drafts the line item from the receipt, matched to your policy, inside the same Expenses form you already file through" | Photographing several receipts in one shot; v1 reads one receipt per item, a PRD trade-off, not a rough edge to smooth over live. A normal multi-receipt report, each receipt captured separately, is fine to show | 2 min |
| 2 | The reviewer opens the drafted report and sees each field's confidence flag (LEDGERLINE-S3) | "Reviewers only spend judgment where the confidence flag tells them to" | A receipt in a language other than English; foreign-language extraction is an open risk (R3), not a demo strength | 2 min |
| 3 | The account-level approval-rate tile (LEDGERLINE-S5, shipped 2026-11-13) **(step added 2026-11-13, when the tile shipped)** | "This is the number your account's own approval rate tracks once you activate. From 2026-11-13 the tile also shows the rate before and after activation for accounts with data" | Quoting a specific target percentage as a guarantee; no customer-level target exists on this page. Do not cite the phase 1 partners' drafted-report count (N44) here: that figure was measured through 2026-11-22, after this tile shipped, and belongs to section 3's proof row, not this script | 1 min |

**Demo environment and data:** Larchfield Logistics, the standing demo account, live from 2026-11-10 when phase 1 opened (no separate build date or link recorded in this workspace); the sales engineer resets it before each session.

## 7. Where to send people

- Product questions during a deal: Maya Chen, product manager, via the launch team channel
- Security and privacy questionnaires: the legal lead. Open: no filled privacy or security architecture document for this add-on exists in this workspace as the source; route the questionnaire to the legal lead directly until one is written
- Feature requests from prospects: write an evidence note that feeds the regular feedback-synthesis pass ([feedback-program.md](ledgerline-feedback-program.md) owns the intake). **(added 2026-11-10, when the advisory board was chartered; forum names updated 2026-12-22 to match the feedback program's corrected charter)** The Ledgerline Expenses Advisory Board, chartered in feedback-program.md section 5 with Hana Sato as owner, informs the pricing and packaging review through its own paying-account panel; it is not the intake for a prospect's feature request
- Lost deals: Hana Sato owns win-loss; every loss gets a row in [win-loss-review.md](ledgerline-win-loss-review.md). **(updated 2026-12-17, when the win-loss batch was signed)** That instrument later found the seat-count pattern this page's first objection answers

## Exit gate (feeds Gate 5: release readiness green)

A signed page satisfies the sales line in gtm-plan.md's phase 1 comms row and the field-readiness checkbox at [Gate 5](../os/STAGE-GATES.md).

- [x] Every line traces to positioning.md, gtm-plan.md, pricing-packaging.md, or the launch comms named in gtm-plan.md; nothing is invented here. Sections 1 to 3 trace to the signed positioning and pricing documents. Section 4's N24 figure traces to the internal metrics review, not a customer document, and is named as such where it is used; the same is true of N14 and N15 in section 2, sourced from the internal business case
- [x] Every claim carries proof or is marked unproven, and unproven claims are absent from the demo path. Section 3's two unproven rows, filing-time saved and the bounce-reduction claim, are not demoed; the drafting, policy-match and confidence-flag claims appear in section 6 steps 1 and 2, alongside step 3, which shows the account-level approval-rate tile (LEDGERLINE-S5) without claiming the bounce-reduction rate moves
- [x] Every objection has an honest answer and a "do not say." Section 4, six rows
- [x] The pricing section holds pointers and authority and no price for this add-on; no other section on the page quotes this add-on's price. Section 5 held no numbers from 2026-11-06 and still holds none now that it is withdrawn; section 4 row 1's objection answer no longer carries the $6-a-seat or 34-seat figures either, and points to section 5 instead. The only price quoted anywhere on the page is the competitor's, Cinderwick's $8 per seat per month in section 2 row 3 (N13), which is not this add-on's price
- [x] A rep has read it and could disqualify a prospect with the section 1 question. Marcus Webb, mid-market account executive, read the draft on 2026-11-05 to 2026-11-06 and fed section 4's objections from his own calls
- [x] Signed by Tomas Lindqvist, head of product marketing, 2026-11-06

This page's own record against itself: it was approved before phase 1 opened, updated in place once phase 1 gave section 3 a real proof point (2026-11-23), and had section 5 (and section 4's first objection answer) withdrawn the day the price they pointed to was killed (2026-12-21), rather than left up with a number that no longer held. The rest of the page stands. Reps working this segment after 2026-12-21 need pricing-packaging.md's reopened section 1 and a new pricing pointer, not this page's old section 5.

Related: the [journey index](ledgerline-journey.md) for the full cast, data sheet and timeline.
