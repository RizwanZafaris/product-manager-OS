---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Insurance", "P&C", "Insurtech", "insurance"]
---
# Insurance

An insurance product sells a promise to pay in the future, conditional on an event nobody wants to happen, and the loop exists to price that promise correctly, then honor it when the event occurs. The distinctive fact is that the two moments testing the product, underwriting a risk correctly and paying a claim fairly, are separated by months or years, so a bad underwriting decision does not surface until a customer's worst day, when it is far more expensive to fix.

The second distinctive fact is distribution: most policies reach the customer through an agent, broker, or managing general agent standing between insurer and buyer, and embedded insurance, a policy sold inside someone else's checkout, adds a partner who is not licensed to give insurance advice and rarely thinks of themselves as selling insurance at all. Reserve adequacy is the quiet discipline underneath it: an insurer that underprices today looks fine until claims development proves it wrong, years later, past any quarterly review. Where a model scores an applicant or triages a claim, these questions sit on top of [the regulated module](../../modules/regulated/README.md).

## Questions a PM must ask

1. Who is the policyholder, who is the claimant, and are they the same person? A third-party liability claim means the person your product judges may never have agreed to your terms of service.
2. Is the rate filed with a regulator, and does this market require prior approval before a change goes live, or only notice after? Shipping a price on a "file and use" assumption in a "prior approval" jurisdiction is a compliance failure disguised as a pricing experiment.
3. What data does underwriting use, and is any of it a protected category this market restricts, such as genetic or health information? A model that proxies for a restricted category is not made lawful by never asking for it directly.
4. What does the claims process look like from first notice of loss to payment, and where does a wrongful denial get caught before it becomes a pattern? One bad denial is a customer problem; a pattern is a market-conduct exam.
5. Who is the reinsurer, and what does the treaty exclude? A feature that seems ready to ship can be quietly uninsurable until the treaty is amended, a decision your team does not control.
6. Is the distributor licensed for what they are actually selling? An embedded-insurance partner integrated for speed may be giving advice they have no license to give.
7. What is the reserve basis for this product line, and who is the appointed actuary who certifies it? A product growing faster than its reserving discipline is a liability the balance sheet has not admitted yet.
8. Is this a takaful product, and has the Shariah board approved the pooling and surplus structure? See [islamic-finance](islamic-finance.md); a conventional feature copied into a takaful product usually fails on structure, not economics.

## Gatekeepers

- **The insurance regulator and its rate-filing regime.** US state Departments of Insurance under prior-approval or file-and-use rules can block a rate before it reaches a customer; the SECP under Pakistan's Insurance Ordinance, 2000, requires policy forms and rating bases to be filed and can prohibit their use; IRDAI in India moved most life, general and health products to use-and-file in 2022 and 2023, so the default there is filing after launch with prior approval kept for reserved categories, and the power to require modification or withdrawal of a product survives either way. The EU is the counter-example: Solvency II, Article 21, bars member states from requiring prior approval or systematic notification of policy conditions and premium scales, so the national competent authority's gate there is solvency and conduct supervision after the fact, not a rate filing before launch.
- **The Appointed Actuary or Chief Actuary.** Certifies that claim reserves, including incurred-but-not-reported claims, are adequate; a named, personal sign-off, not a committee decision that disappears into minutes.
- **Claims-conduct enforcement.** Built on the pattern set by the NAIC's Model Unfair Claims Settlement Practices Act in the US and equivalent conduct rules elsewhere; a systematic pattern of wrongful denial is where regulators start asking for your claims-triage logic.
- **The reinsurer.** Large or novel risks are ceded under a treaty with its own exclusions and audit rights; the reinsurer can effectively veto a product feature by declining to cover it.
- **Distribution and producer licensing bodies.** Agent and broker licensing regimes, and in the EU the Insurance Distribution Directive's product oversight and governance duties, decide who may sell what and what they must disclose about commission.
- **The Shariah board, for a takaful line.** Reviews the contribution pool, the operator's fee model, and the surplus-distribution mechanism before launch; see [islamic-finance](islamic-finance.md).

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Loss ratio | Claims paid against premium earned | A low ratio this year can be next year's adverse reserve development in disguise, not real profitability |
| Combined ratio | Underwriting profitability including expenses | Sits under the break-even line while investment income quietly does the profitable work underwriting never did |
| Claims cycle time, first notice to payment | Speed of the claims process | Improves by fast-tracking simple claims and shunting complex ones to a slow review queue the average never shows |
| Claims denial rate | Underwriting discipline at the claims stage | Alone it cannot separate fraud prevention from wrongful denial; read it beside the appeal overturn rate |
| Appeal overturn rate | Whether denials were correct in the first place | A low volume of appeals is often unequal access to appeal, not evidence the original decisions were right |
| Policy renewal or retention rate | Customer satisfaction and pricing competitiveness | Can be propped up by auto-renewal without repricing a customer whose risk changed, building adverse selection the metric never flags |
| Straight-through issuance rate | Underwriting automation | Rises by referring hard risks to a slower manual queue, moving friction out of the metric rather than out of the customer's experience |
| Fraud model hit rate and false-positive rate | Effectiveness of fraud detection | A hit rate alone rewards flagging everything; pair it with investigator time spent clearing genuine claims wrongly flagged |
| Reserve development, favorable or adverse | Whether past pricing was right | Reported a year or more later, punishing or rewarding decisions nobody making today's price will still answer for |
| Satisfaction score at claims | Experience during the moment that matters most | Collected mostly from customers whose claims were approved quickly, excluding the disputed and delayed cases |

## Reading

- **Solvency II, Directive 2009/138/EC.** Read the three-pillar structure, capital requirements, governance, disclosure, and the ORSA requirement directly; the clearest statement of why reserving and governance are one discipline.
- **The IAIS Insurance Core Principles.** The global baseline a national regulator's own rulebook usually maps back to; useful for orienting in a market whose rules you do not yet know well.
- **The NAIC's Model Unfair Claims Settlement Practices Act.** Adopted with variation state by state in the US; read it for the pattern even outside the US, since the same conduct categories recur everywhere.
- **The EU Insurance Distribution Directive, (EU) 2016/97.** Read for product oversight and governance duties and commission-disclosure rules reaching embedded-insurance partners as much as traditional brokers.
- **The US Genetic Information Nondiscrimination Act (GINA).** A narrow, specific restriction worth reading precisely because it is narrow: one protected category carved out by name rather than by a general fairness principle.
- **SECP's Insurance Ordinance, 2000, and Pakistan's takaful rules (verify the current citation and year before relying).** Read for a market where conventional and takaful insurance are licensed under one regulator but different structural rules.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the policyholder and the claimant separately, since a product built for the buyer can still fail the person it pays out to), DEFINE-5 (a requirement fails here as a wrongful denial or an unfiled rate, categories a generic bug tracker has no field for), DESIGN-3 (health and claims data retention has a named regulatory period, not a default), and OPERATE-8 (the counter-metric behind a falling denial rate or a rising retention rate usually sits in appeal-overturn or reserve-development numbers, reported later).

**Templates this bends:** [business-rules](../../templates/definition/business-rules.md) (underwriting eligibility and claims-adjudication logic are literally the business rules, versioned like code), [nfr](../../templates/definition/nfr.md) (claims cycle time and reserve-reporting cadence are regulatory requirements, not target SLAs), [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (a rate change or a new underwriting data source triggers this before it triggers a release), and [personas](../../templates/discovery/personas.md) (claimant and policyholder need separate persona treatment even when they share a name on the policy).

**Filled in this repo:** [domain-insurance-business-rules.md](../../examples/domain-insurance-business-rules.md) fills the [business-rules](../../templates/definition/business-rules.md) template directly for this domain, for Cobalt Assurance: the BR-INS-04 fast-track triage rule, a fraud-indicator referral to the special investigations unit, a total-loss threshold, claim acknowledgement and decision time limits under state unfair-claims-settlement-practices acts, versioned underwriting eligibility tied to its rate-filing reference, held by the Chief Claims Officer, with actuarial and compliance sign-off required for any threshold change. For the other three bent templates, [harbourgate-nfr.md](../../examples/harbourgate-nfr.md), [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) and [sahulat-personas.md](../../examples/sahulat-personas.md) remain the nearest reading for revision-log discipline, an update-note pattern, and a two-person opposed-interest split, though none carries a claims-cycle figure, a rate-filing question, or a claimant persona.

**Worked example (ILLUSTRATIVE):** a business-rules row for a fictional motor-claims triage feature, in the register shape [harbourgate-business-rules.md](../../examples/harbourgate-business-rules.md) uses for payment declines.

| Field | Value |
|---|---|
| ID | BR-INS-04 |
| Rule statement | WHEN a first-notice-of-loss claim's estimated value is below USD 2,500 AND the policy is within its first 90 days of no prior claims THEN route to fast-track adjudication, else route to a licensed human adjuster |
| Trigger point | Claims intake, on FNOL submission |
| Source of truth | Claims-handling manual v4, held by the Chief Claims Officer |
| Business owner | Chief Claims Officer, not engineering |
| Exceptions | None on the USD 2,500 threshold. A policy already flagged for a prior denial in the last 12 months is excluded from fast-track regardless of value, and routes to a human adjuster |
| Regulatory tie-in | A pattern of fast-track denials above this threshold is exactly what a market-conduct exam under the market's unfair-claims-practices rule would sample; changing the cutoff without re-documenting the rationale is the kind of undocumented change that turns one bad denial into a pattern, so it needs more than a product sign-off |
| Enforced by | FR-CLM-12 |
| Test traceability | AC-CLM-03: appeal-overturn rate on fast-track denials tracked separately from the manual-review appeal-overturn rate, since a rising fast-track figure is the signal the card's gatekeepers watch for |
