---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Embedded finance", "Banking as a Service", "BaaS", "open banking", "embedded-finance-baas"]
---
# Embedded finance and banking as a service

The brand the end customer sees is rarely the regulated entity behind it. A sponsor bank, or a licensed e-money or payment institution, sits behind the brand, and the licence belongs to that sponsor, not to the product company shipping the roadmap. When the sponsor pulls it, the product stops, in full, regardless of how good the software is. That single structural fact bounds everything else here: your customer-facing team can design a beautiful onboarding flow, and the sponsor's risk appetite still decides whether it ships. Open banking, account-to-account data sharing and payment initiation, runs on regulator-mandated APIs in some markets and on privately negotiated or aggregator-mediated access in others, and a PM building "connect your bank" has to know which regime, if either, actually applies in each target market rather than assuming one global standard exists. Banking-as-a-service middleware itself became a live supervisory focus after program failures left end customers unable to reach their own funds when a partner bank or a middleware provider ran into trouble, a still-unfolding story rather than a settled one. Embedded lending and embedded payments inherit every duty covered in [lending-credit](lending-credit.md) and [payments-acquiring](payments-acquiring.md); "embedded" changes who stands in front of the customer, not which regulator's rules apply behind them.

## Questions a PM must ask

1. Which regulated entity actually holds the licence behind this feature, and does our contract with them cover the feature we are about to ship, or only the one we shipped last year?
2. If our sponsor bank or middleware provider failed tomorrow, what happens to a customer's funds and access, and have we actually modeled that rather than assumed the bank simply guarantees it?
3. For an open-banking data-sharing feature, is access happening through a regulator-mandated standard with its own consent and revocation rules, or through a privately negotiated arrangement with weaker guarantees?
4. Does the end customer know which entity is actually their bank of record for deposit-insurance and dispute purposes, or does the branding make that deliberately invisible?
5. When we embed a payment or lending feature inside another company's product, who owns the customer relationship for KYC, disputes, and complaints, and does the contract say so explicitly?
6. What data-sharing consent did the end customer actually give, for how long, for what scope, and can they revoke it as easily as they granted it?
7. What is the sponsor's or regulator's limit on this programme's volume or risk concentration, and who is monitoring against it in real time rather than discovering a breach after the fact?
8. If this feature is embedded lending or embedded payments, have we separately answered the full question set in [lending-credit](lending-credit.md) or [payments-acquiring](payments-acquiring.md), rather than assuming "embedded" made those duties smaller?

## Gatekeepers

- **The sponsor bank or licensed e-money institution behind the programme.** Holds the actual licence, approves the programme, sets risk and volume limits, and can suspend the whole offering; examiners now hold sponsors to a higher bar of ongoing oversight of their fintech partners than in the past.
- **The banking or payments regulator supervising that sponsor.** US federal banking regulators have tightened expectations on bank-fintech partnerships; the UK and EU authorise payment and e-money institutions directly under the post-PSD2 framework.
- **Open banking standard bodies, where they exist.** The UK's Open Banking regime, arising from a competition authority order, and the EU's technical standards on strong customer authentication and secure communication are the two most mature examples; their absence elsewhere means bilateral or aggregator-mediated access with weaker guarantees.
- **The distribution partner's own compliance and brand teams**, when finance is embedded into a non-financial product. They decide how much regulated-entity disclosure the brand will surface, and that negotiation shapes the interface as much as any regulator does.
- **Data aggregators or screen-scraping intermediaries**, where a regulated API is not used. A single point of failure for every embedded feature built on top of them, whose own terms of service, not a regulator, often decide what consent and revocation actually mean.
- **Deposit insurers and their pass-through rules.** Where end-customer funds sit in a pooled account at the sponsor, the insurer's pass-through rules decide whether individual customers are actually insured, and getting the bookkeeping wrong can void that coverage entirely.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Programme volume versus the sponsor's approved limit | Regulatory headroom | A monthly reading can hide a mid-month spike that breaches the limit and self-corrects before the next check |
| Data-sharing consent renewal rate | Genuine ongoing consent | A high rate can reflect a re-authentication flow designed to be hard to decline, not informed, freely given renewal |
| API uptime with the underlying bank or aggregator | Reliability of the whole embedded feature | Your own platform can report high uptime while the upstream connection it depends on fails intermittently, monitored as a separate system |
| Time to resolve a dispute across brand and licence-holder | Customer harm | Each party's own resolution metric can look fine while the customer bounces between two support queues with nobody owning the end-to-end clock |
| Sponsor audit findings, open and closed | Partnership health | Count alone hides severity; one open high-severity finding is a bigger risk than many closed low-severity ones |
| Embedded lending origination growth | Business growth | The lending-credit failure mode inherited wholesale; read it against vintage loss rates, never on its own |
| Share of customers who can name their actual bank of record | Transparency | Rarely measured at all, which is itself the finding; a near-zero answer means the disclosure was designed away |
| Revenue retained after sponsor and middleware fees | Unit economics | A healthy gross programme margin can still be thin or negative net once per-account and per-transaction fees apply at real volume |
| Consent scope creep, data accessed beyond original authorisation | Compliance and trust | Rarely tracked until an audit or complaint surfaces it, so its absence from a dashboard is not evidence it is not happening |
| Time to launch a new product line with the same sponsor | Platform velocity | A fast internal build time hides that the sponsor's own approval queue, not engineering, is usually the real constraint |

## Reading

- **The UK's Open Banking standard**, established through the Competition and Markets Authority's retail banking market investigation order, the clearest example of a regulator mandating the API rather than leaving account access to bilateral deals.
- **The EU's post-PSD2 framework on account information and payment initiation service providers.** The licensing categories embedded open-banking features actually fall into across Europe.
- **The US CFPB's personal financial data rights rulemaking under Section 1033 of the Dodd-Frank Act.** The US route toward an open-banking-style right, still maturing relative to the UK and EU (verify current implementation status before relying).
- **US federal banking regulators' guidance and enforcement on bank-fintech partnerships.** Read the pattern of findings, inadequate ongoing monitoring and unclear end-customer fund records, rather than any single case, and verify names and dates before relying.
- **State Bank of Pakistan's framework for electronic money institutions.** A non-US example of a central bank shaping who may hold end-customer float and on what terms an embedded payment feature may operate (verify current specifics before relying).
- **[modules/regulated/README.md](../../modules/regulated/README.md)**, read before assuming that embedding a feature shrinks the regulatory question; it usually only changes who stands between the product and the regulator.

**Conductor overlay:** this domain sharpens DESIGN-2 (integrations, since the sponsor and any middleware are the integration whose failure can end the whole programme), DEFINE-8 (overlays, since embedded finance puts a sponsor's regulator one contract away from the team shipping: the regulator half is a yes, and the regulated overlay fires only when a model is inside, per the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md)), DESIGN-3 (where PII lives, since open-banking data sharing widens what counts as sensitive data to months of transaction history obtained through a third party), and DELIVER-6 (regulated overlay drift, since sponsor terms or aggregator access terms can change between sign-off and launch).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (the sponsor and middleware named with owner and failure behavior), [privacy-impact-assessment](../../templates/architecture/privacy-impact-assessment.md) (data-sharing consent scope and revocation), [partner-integration-brief](../../templates/planning/partner-integration-brief.md) (the sponsor or middleware relationship is exactly the dependency this template exists to specify), and [risk-register](../../templates/execution/risk-register.md) (sponsor concentration and programme-suspension risk as standing entries).
