---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Islamic finance", "Shariah-compliant finance", "Takaful", "islamic-finance"]
---
# Islamic finance

This product cannot charge interest (riba), cannot deal in excessive uncertainty (gharar), and cannot resemble gambling (maysir), so a feature that would be a simple interest-bearing loan or a conventional insurance policy elsewhere has to be rebuilt as a trade, a lease, or a partnership producing a similar outcome through a different legal form. The Shariah board reviews and approves the contract structure before anything is built, not after; it can send back something that already works technically because the legal form, not the economic effect, is what compliance means here.

The second distinctive fact is that a ruling from one board does not travel. A structure approved in Malaysia can be rejected by a board in Pakistan or the Gulf, because schools of jurisprudence and board composition differ by market, so "Shariah-compliant" is a separate approval to win in every market entered, not one global standard satisfied once. The third is that the claim is a matter of faith for the customer, not only a technical certification, so a product formally approved but widely seen as a riba workaround, a criticism leveled at some tawarruq-based structures, carries a reputational cost no compliance sign-off captures.

## Questions a PM must ask

1. Which contract structure does this feature use, Murabaha, Ijara, Diminishing Musharaka, Mudaraba, and does the flow genuinely follow its steps, or skip one for speed? Skipping the ownership-transfer step in a Murabaha sale to close faster is the shortcut a Shariah audit exists to catch.
2. Has this specific product, not just its contract type, been approved by the Shariah board governing this market? A generic Murabaha approval does not cover a new fee structure or asset class.
3. Is a change to pricing, fees, or the underlying asset one the board must re-approve? Treating a Shariah-approved product like a feature that can be A/B tested without re-review is the most common process failure here.
4. Where does incidental non-compliant income go, such as conventional interest earned briefly on float while funds transit? It must be identified and donated to charity, with someone owning the calculation and evidence.
5. For a takaful product, is the operator's fee wakala, a fixed agency fee, or mudaraba, a share of profit, and does the surplus mechanism return money to participants or quietly retain it? The fee model, not the pooling concept, is what a Shariah board scrutinizes most.
6. Does the disclosed profit rate match what is actually realized, or is it smoothed through a profit-equalization reserve? A stable-looking return can be smoothing, not performance.
7. If this product also touches a conventional financial regulator's rules, has [the regulated module](../../modules/regulated/README.md) been checked alongside the Shariah approval? The two gates do not substitute for each other.
8. Can this approval be undone or amended quickly, or does a material change require a fresh fatwa cycle measured in months? Reversibility here has a religious-governance answer, not only a technical one.

## Gatekeepers

- **The Shariah Supervisory Board, at the bank or product level.** Reviews and approves every product's contract structure before launch, not only its marketing copy, and can force a rebuild of something that already works because its legal form fails, not its economics.
- **A centralized Shariah Advisory Council, where one exists.** Bank Negara Malaysia's Council issues rulings binding on every Islamic institution in Malaysia under the Islamic Financial Services Act 2013; without a centralized council, expect the opposite instead, two banks offering differently structured "Islamic" products for the same need.
- **The central bank's Islamic banking supervision department.** Runs a separate Islamic banking license or window authorization, and in some markets applies prudential rules referencing IFSB standards. The State Bank of Pakistan's Shariah Governance Framework layers a central-bank board on top of each institution's own.
- **AAOIFI, where its standards are mandated or merely referenced.** Mandatory in Bahrain and some other jurisdictions, advisory elsewhere; even where advisory, an examiner or a sophisticated customer will ask why a product departs from its standard for that contract type.
- **Public and scholarly opinion.** A product technically approved but widely perceived as a conventional-finance workaround carries reputational risk no compliance sign-off resolves, because the customer's objection is to the substance, not the paperwork.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Profit-sharing ratio realized versus disclosed | Whether the account performs as promised | The bank's discretion over a profit-equalization reserve can smooth the realized number away from true underlying performance |
| Shariah non-compliant income identified and purified | Cleanliness of the income stream | A low figure can mean genuine cleanliness or an under-resourced purification process that simply is not looking closely |
| Takaful surplus distributed versus retained | Whether participants benefit from a good claims year | Retention framed as prudent reserving can function like conventional insurer profit-taking under a different name |
| Financing-to-deposit ratio within an Islamic window | Balance-sheet health of the Islamic business line | Can be flattered by resource-sharing with a conventional parent bank in ways that would not survive standing alone |
| Shariah board approval cycle time | Governance responsiveness | A fast cycle looks efficient and can also mean a board rubber-stamping structures designed to mimic conventional products as closely as legal |
| Rate of new products with a conventional-equivalent profile | How much genuine structural innovation is happening | Not necessarily wrong, but exactly the pattern AAOIFI's stricter standards exist to scrutinize |
| Customer complaints citing Shariah-compliance doubt | Trust in the faith-based claim itself | Low volume can reflect genuine trust or simply that doubtful customers have nowhere specific to raise it |
| Wakala fee as a share of takaful contributions | Operator's revenue model transparency | A fee presented as modest can still leave little in the pool for genuine surplus once claims and reserves are deducted |
| Cross-border product reuse rate | Efficiency of scaling a structure across markets | A structure reused without a fresh local board approval is a compliance gap, not an efficiency win |
| Account attrition after a profit-rate reset | Whether disclosed profit-sharing terms hold up in practice | Attrition concentrated right after a reset usually means the prior rate was smoothed higher than the account could sustain |

## Reading

- **AAOIFI's Shariah Standards.** Read the standard for the specific contract type being built, Murabaha, Ijara, or Diminishing Musharaka, before designing the flow, not after a working prototype exists.
- **The IFSB's prudential and risk-management standards.** The closest equivalent to Basel-style capital and disclosure expectations, layered on top of Shariah compliance rather than replacing it.
- **Bank Negara Malaysia's Islamic Financial Services Act 2013 and its Shariah Advisory Council rulings.** Read as the centralized-authority model, and contrast it with the bank-by-bank board system common elsewhere.
- **The State Bank of Pakistan's Shariah Governance Framework for Islamic Banking Institutions.** Read for the bank-level board plus central-bank oversight model. Pakistan's Federal Shariat Court ruled in 2022 that interest should be eliminated from banking, a decision now under appeal, live and contested rather than settled (verify current status before relying).
- **A published comparison of wakala versus mudaraba operator remuneration in takaful, from an IFSB or AAOIFI source.** Read for why the operator's fee structure, not the pooling concept, is what a Shariah board actually scrutinizes.

**Conductor overlay:** this domain sharpens DEFINE-3 (a contract-structure change after launch may need a fresh fatwa cycle measured in months, not a flag), DEFINE-8 (the overlay question extends to whether a Shariah board governs this market alongside any financial or AI regulator), DESIGN-1 (the rejected alternative is usually the conventional-equivalent structure, rejected on legal form, not economics), and OPERATE-8 (the counter-metric behind a smooth profit rate usually sits in the profit-equalization reserve).

**Templates this bends:** [business-rules](../../templates/definition/business-rules.md) (the contract structure is the business rule, and its Shariah sign-off belongs recorded beside it), [decision-log](../../templates/execution/decision-log.md) (a board approval or rejection is a decision worth logging with its reasoning attached), [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (a Shariah gate runs parallel to a legal and privacy sign-off, not instead of one), and [personas](../../templates/discovery/personas.md) (a customer choosing Islamic finance for faith and one choosing it for price are different personas, and conflating them misreads the complaint rate).
