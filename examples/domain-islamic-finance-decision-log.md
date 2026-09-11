# Decision Log: Nakhla Wallet Shariah-Compliant Financing

Fills [templates/execution/decision-log.md](../templates/execution/decision-log.md). Everything here is invented: Nakhla Wallet is a fictional Shariah-compliant digital wallet, its people are fictional, and every number, date, fee and identifier is ILLUSTRATIVE. See the [examples index](README.md).

**Initiative:** Commodity Murabaha consumer financing · **Log owner:** Layla Haddad, product manager · **Started:** 2026-04-06
**Entries:** 4 · **Open reversals:** 1 · **Last entry:** 2026-06-15

## 1. Index

| ID | Decision, in one line | Date | Decider | Type | Status |
|---|---|---|---|---|---|
| D-SF-04 | Show "profit rate," never "interest," in all customer copy | 2026-06-15 | Layla Haddad, product manager | naming | holding |
| D-SF-03 | Shariah board rejects the fee-on-delay structure for Murabaha financing | 2026-05-11 | Sheikh Omar Farouk, Shariah board chair | pricing | holding |
| D-SF-02 | Wallet takes ownership of the commodity before selling it to the customer | 2026-04-28 | Youssef Karim, head of product | sequencing | holding |
| D-SF-01 | Select commodity Murabaha over a conventional-equivalent financing structure | 2026-04-06 | Youssef Karim, head of product | scope | reversed by D-SF-02 |

## 2. When to log, and when not to

| Log it | Do not log it |
|---|---|
| Two or more people debated it for over ten minutes | It was never in question |
| Anyone could reasonably reopen it in three months | It is a task, and the tracker already holds it |
| It closed off an option that cost something to give up | It restates something already decided; link the original instead |
| A new joiner would otherwise ask "why is it like this?" | It changes system structure, which belongs in an [ADR](../templates/architecture/adr.md) |
| It was decided under time pressure or with thin evidence | It is a preference nobody will act on |

**Log within a day of deciding.** A rationale reconstructed a week later is a rationalisation: the reasons that get written down are the ones that survived, not the ones that operated.

## 3. Decisions

### D-SF-04: Show "profit rate," never "interest"

- **Date:** 2026-06-15 · **Decider:** Layla Haddad, product manager
- **Type:** naming
- **Context:** The marketing copy for the Murabaha financing feature described the cost as an "interest rate" in early drafts, because the number looks identical to a conventional rate. The Shariah board flagged this as a mislabeling risk: the legal form is a sale at a deferred price, and calling the markup "interest" invites both customer confusion and a perception of riba. The board had already rejected the original fee structure in D-SF-03 on 2026-05-11 and replaced it with a fixed charitable donation; this entry ensures the language matches the approved structure.
- **Options considered:** use "interest rate" because customers understand it; use "profit rate" with a footnote explaining the Murabaha structure; use a neutral "financing cost" with no rate disclosed.
- **Decision and rationale:** Use "profit rate" in all customer-facing copy. The term accurately describes the bank's markup on a sale, not a charge for the use of money over time. A "financing cost" label was rejected because it obscures the disclosed rate, which the board wants visible and comparable. Given up: some customers may find "profit rate" unfamiliar, and the support team will need a short script explaining the difference. The board's approval of the revised late-fee structure in D-SF-03 was conditional on this language change, so the decision also closes a board condition rather than standing alone.
- **Evidence it rested on:** Shariah board meeting minutes, 2026-06-15; AAOIFI Shariah Standard No. 8 on Murabaha (verify current edition and applicability with counsel); the marketing copy review log, 2026-06-10.
- **What would change our mind:** a board ruling in a new market requiring different terminology, or a regulator requiring a specific disclosure label; either would be a new entry, not an edit to this one.
- **Reverses or is reversed by:** none
- **Who was told:** product channel and marketing weekly, 2026-06-15

### D-SF-03: Shariah board rejects the fee-on-delay structure for Murabaha financing

- **Date:** 2026-05-11 · **Decider:** Sheikh Omar Farouk, Shariah board chair
- **Type:** pricing
- **Context:** The proposed late-payment fee on deferred Murabaha instalments was sized to match the conventional product's penalty-interest rate of 2% per month on the overdue amount (ILLUSTRATIVE). The Shariah board reviewed the structure at its 2026-05-11 sitting and rejected it. A fee that scales with lateness functions as disguised riba regardless of its label, because it charges more for more time, which is the definition of interest. The board approved a fixed, cost-recovery-only late fee instead, donated to charity if it exceeds actual recovery cost.
- **Options considered:** a late fee sized to match the conventional penalty rate; a fixed late fee set at the actual administrative cost of chasing an overdue instalment; no late fee at all.
- **Decision and rationale:** A fixed charitable donation set at the actual recovery cost, not at the conventional penalty rate. AAOIFI Shariah Standard No. 8 on Murabaha governs this contract type; the board applied its rule that a late-payment charge must not be a source of profit and must not scale with the overdue period (verify the current text and its applicability in this jurisdiction with counsel). The fixed fee recovers the administrative cost of a reminder call and a letter, currently estimated at PKR 200 per overdue instalment (ILLUSTRATIVE), and any amount collected above that cost goes to the charity fund. Given up: the revenue the conventional-scaled fee would have produced, which the finance model had counted as PKR 1.2 million a year at a 3% overdue rate (ILLUSTRATIVE); and the simplicity of one fee number that scales, replaced by a fixed fee plus a separate charity-accounting line.
- **Evidence it rested on:** Shariah board meeting minutes, 2026-05-11; AAOIFI Shariah Standard No. 8 on Murabaha (verify); the product finance model, version 4, 2026-05-05.
- **What would change our mind:** a board ruling permitting a different late-fee basis, or a regulator requiring a specific late-fee disclosure; both would be a new entry with a fresh board sitting, not an edit to this one.
- **Reverses or is reversed by:** none
- **Who was told:** product channel, finance weekly, and the Shariah board secretary, 2026-05-12

### D-SF-02: Wallet takes ownership of the commodity before selling it to the customer

- **Date:** 2026-04-28 · **Decider:** Youssef Karim, head of product
- **Type:** sequencing
- **Context:** In commodity Murabaha, the bank must own the commodity before selling it to the customer at a deferred price. The engineering and operations teams proposed a flow where the wallet's platform matches the customer to a broker and books the sale almost simultaneously, skipping a deliberate ownership step to cut latency and cost. The Shariah board's advisory note of 2026-04-21 warned that skipping the ownership-transfer step is the shortcut a Shariah audit exists to catch, citing the risk that the sale becomes a financing transaction rather than a trade.
- **Options considered:** the simultaneous match-and-sell flow the engineering team proposed; a deliberate ownership step where the wallet holds the commodity for a recorded interval before selling; a fully manual ownership process run by the treasury desk.
- **Decision and rationale:** A deliberate ownership step, recorded in the wallet's ledger within the platform flow, before the deferred-price sale. The simultaneous flow was rejected because it collapses the sale into a mere exchange of cash, which is the form the board is protecting. A fully manual process was rejected because it does not scale past the pilot. Given up: about four seconds of flow latency and an estimated PKR 6 per transaction in additional operational cost (ILLUSTRATIVE) for the ownership recording step. The ownership step is now an explicit business rule, BR-SF-12, and its absence would fail the Shariah audit.
- **Evidence it rested on:** Shariah board advisory note, 2026-04-21; product flow diagram, versions 3 and 4, 2026-04-25; the commodity broker's delivery confirmation API documentation (verify current API terms with the broker).
- **What would change our mind:** a board ruling that a centralised fungible commodity pool satisfies the ownership requirement without a per-transaction step, or a fall in ownership-step latency and cost that removes the trade-off entirely.
- **Reverses or is reversed by:** reverses D-SF-01
- **Who was told:** product channel, engineering weekly, treasury weekly, 2026-04-29

### D-SF-01: Select commodity Murabaha over a conventional-equivalent financing structure

- **Date:** 2026-04-06 · **Decider:** Youssef Karim, head of product
- **Type:** scope
- **Context:** At the start of the initiative the team debated whether to build the financing feature on a conventional interest-bearing product and obtain a Shariah approval for a compliant wrapper, or to build the contract structure as a genuine trade from day one. The conventional-equivalent approach would have shipped faster because the underlying product already existed. The Shariah board's preliminary guidance of 2026-04-01 warned that a conventional product in an Islamic wrapper is precisely the tawarruq-based structure that carries the reputational cost the domain card describes.
- **Options considered:** a conventional interest-bearing product with a Shariah-compliant wrapper; a genuine commodity Murabaha trade structure built from first principles; delay the feature until a board-approved structure could be designed.
- **Decision and rationale:** A genuine commodity Murabaha trade structure, built from first principles. The wrapper approach was rejected because it fails the legal-form test the board applies, even if the economics are equivalent, and the reputational risk of a widely-criticized tawarruq workaround is not one a compliance sign-off resolves. Delaying the feature was rejected because the market window was real. Given up: roughly eight weeks of development time and an estimated PKR 8 million in additional build cost (ILLUSTRATIVE). This decision was later superseded by circumstance when the ownership-step design in D-SF-02 made clear the original sequencing assumption (that the trade could be simulated) did not hold.
- **Evidence it rested on:** Shariah board preliminary guidance, 2026-04-01; product discovery interviews, 2026-04-02 and 2026-04-02; the [islamic-finance domain card](../knowledge/domains/islamic-finance.md).
- **What would change our mind:** a board ruling that a specific wrapper structure is acceptable in this market, or a shift in the competitive landscape that makes the eight-week delay unaffordable.
- **Reverses or is reversed by:** reversed by D-SF-02
- **Who was told:** product channel, board chair's office, 2026-04-07

## 4. How this log fails

| Failure mode | What it looks like | The rule |
|---|---|---|
| Winners only | Every entry lists what was chosen and no option that lost | An entry with no losing option is a announcement, not a decision. Reject it at review |
| Committee as decider | "The team decided", or three names in the decider field | Exactly one name. A group can agree; only a person can be asked why |
| Edited history | An old entry now describes what the team currently believes | Entries are immutable. A change of mind is a new id that names the old one |
| Rationale is the outcome | "We chose A because A was better" | The rationale names the trade: what A cost, and why that cost was acceptable |
| Silent staleness | Entries from two strategies ago, all still marked holding | Review status at every gate. Mark superseded by circumstance rather than leaving it |
| Log kept by one person | Entries stop when that person is on leave | The owner is named, and the review is on a recurring agenda, not in someone's memory |
| Nobody was told | A correct decision that half the team acts against | "Who was told" is a required field, and blank means the decision has not landed yet |

## 5. Gate review

| Gate | Reviewed on | Entries still holding | Marked superseded | New reversals |
|---|---|---|---|---|
| 1 | 2026-07-10 | 3 | 0 | 0 |

## Exit gate

- [x] Every entry has a matching index row, and every index row has an entry
- [x] Every entry has exactly one decider, by name
- [x] Every entry lists the options that lost, not only the winner
- [x] Every rationale names what was given up, not only what was gained
- [x] Every entry records the evidence it rested on, or says plainly that it was judgment
- [x] Every entry names what would change our mind
- [x] No entry has been edited into a different decision; reversals are new ids
- [x] Entry dates are within a day or two of the decisions they record
- [x] Status has been reviewed at the most recent gate, and stale entries are marked superseded rather than left holding
- [x] Structural technology decisions are in [ADRs](../templates/architecture/adr.md), linked rather than duplicated here
- [x] The worked example above has been removed

Signed: Layla Haddad, product manager, 2026-07-10
</output>
