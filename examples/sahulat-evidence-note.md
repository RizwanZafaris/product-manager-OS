# Evidence Note: INT-004, C-04, 2026-02-02

Fills [templates/discovery/evidence-note.md](../templates/discovery/evidence-note.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, the people are fiction, and every number, quote and date is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Note ID:** E1 · **Author:** Hira Baig · **Retrieved:** 2026-02-03

## Source

- **Name:** Interview session INT-004, participant code C-04 (customer), held by Hira Baig with Usman Javed taking notes
- **Locator:** `products/sahulat-bill-pay/discover/interview-notes/INT-004.md`, section 8; the same note is published as [sahulat-interview-notes.md](sahulat-interview-notes.md)
- **Source date:** 2026-02-02
- **Type:** interview

## Claim

A weekend due date turns into a surcharge because the physical payment channel that exists on the due date is closed or charges a fee, and neither removes the fine.

**Evidence kind:** text quotation

**A. Text quotation** (interview, ticket, document, public page)

> "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill."

- **Where in the source:** INT-004 section 8, at timestamp 02:10 in the session recording

**Evidence class:** interview claim (a real person said it, cited by source and date; timestamp 02:10 within the session recording)

## Weight

- **Confidence:** single-source. This wording stands alone; T5 corroborates the pattern through its other two sessions (INT-005 and INT-008), not through INT-004 itself, so agreement on the theme does not verify this specific quote
- **Agrees with:** none found as an independent source carrying this exact wording. Theme T5 ("weekend and after-hours due dates produce surcharges", sessions INT-004, 005, 008) and N24 (3 of 8 customers whose most recent due date fell on a Saturday or Sunday) point the same direction but do not restate this sentence, so they corroborate the pattern without verifying this quote
- **Disagrees with:** none found
- **What this note cannot support:** that a digital rail fixes the surcharge. C-04 did not say the problem is the absence of a phone option; she named three concrete facts (shut branch, PKR 50 shop charge, fine posted anyway). Whether BillBridge's posting SLA (N36, quoted, posts to the biller within 30 minutes seven days a week) would have removed the fine for her is our inference, carried as risk R3 and untested at the review, not something this quote proves

## Ledger row

Copy this row, filled, into the evidence ledger in the product's STATE.md:

| E# | Claim | Evidence (quote, measure or observation) | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E1 | Weekend due dates produce a surcharge because the open channel charges a fee and the fine posts anyway | "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." | INT-004, interview notes section 8, 02:10 | 2026-02-02 | 2026-02-03 | single-source |

## How an evidence note fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Paraphrase presented as a quote | Quotation marks around a tidied version of what was said | Quotation marks are reserved for verbatim text. Paraphrase goes outside them, always |
| A quote invented for a count or a behaviour | A sentence in quotation marks under a metric export or a watched session, because the form asked for a quote | A count is recorded as a measure and a behaviour as an observation. Neither field accepts words nobody said |
| No source or no date | "Research shows", with nothing attached | Author or speaker, document or session, and the date. A note without them cannot be checked |
| Only what we already believed | Sources selected because they agreed, and the disagreement went unrecorded | Record what contradicts the position too. Finding no counter-evidence is itself a finding |
| Context stripped | A sentence lifted from a paragraph that qualifies or reverses it | Carry enough surrounding text that the meaning survives the extraction |
| Confidence asserted | "A reliable source", with nothing behind the adjective | Use the classes in Weight above: verified, single-source, contested, unverified |

*Note what is outside the quotation marks. C-04 did not say validation or a rail caused anything, and did not say other customers face the same thing. Both are our reading, and both are why the confidence is single-source rather than verified.*

## Exit gate

- [x] The evidence kind is declared, and the block that matches it is the one that is filled. This note declares kind text quotation and fills block A; blocks B and C are deleted
- [x] A text quotation carries the sentence verbatim, and everything outside the quotation marks is marked as inference. The quote is carried unchanged from INT-004 section 8 at 02:10; the claim line and the "cannot support" line are labelled as ours
- [x] A quantitative note carries its snapshot or query, filters, denominator, period and timezone, and calculation, and someone else could run it and land on the same figure. This does not apply here, because this note is a text quotation; were it quantitative, the query as run, its filters, its denominator, its period with timezone and its calculation would all be required
- [x] An observation carries its session or timecode and its context, and is written in plain words rather than as words in quotation marks that nobody said. This does not apply here, because this note is a text quotation; were it an observation, the session and timecode and the surrounding context would be required, written in plain words
- [x] Source, source date and retrieval date are all present and locatable by someone else. Session INT-004, dated 2026-02-02, filed at the path above and published as [sahulat-interview-notes.md](sahulat-interview-notes.md); retrieved 2026-02-03
- [x] The confidence class is one of the four in Weight, and the reason for it is stated. Single-source: this wording stands alone, and T5 and N24 corroborate the pattern without restating the sentence
- [x] Contradicting evidence was looked for, and either recorded or explicitly reported as absent. None found against this quote; the absence is recorded in Weight rather than left silent
- [x] The ledger row is filled and ready to copy into the product's STATE.md. It matches E1 in the [journey identifier table](sahulat-journey.md) exactly
- [x] The worked example above has been removed
