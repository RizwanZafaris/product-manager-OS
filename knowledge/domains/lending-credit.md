---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Lending and credit", "consumer lending", "credit decisioning", "BNPL", "lending-credit"]
---
# Lending and credit

Every decision this product makes is a regulated decision about a specific person: approve or decline, price the loan, set the limit, and each one carries fair-lending exposure the way a normal software decision never does. The underwriting model or policy is the product, and a wrong decision here is a legal liability before it is a business one. Affordability is a duty, not a UX nicety: buy now pay later products spent years presenting as not-credit while functioning as short-term credit, and regulators have been closing that gap. Adverse action matters as much as the decision itself: US law requires a specific, accurate reason for a decline, and a reason code chosen because it sounds plausible rather than because it reflects what the model actually weighted is a compliance failure even when the underlying decision was defensible. Collections is where the promise made at origination is actually tested, and it is the point where product design meets debt-collection law most directly: an automated reminder or dunning flow is a regulated communication, not a notification feature, and contact-frequency rules bind the roadmap whether or not the team designing it knows they exist.

## Questions a PM must ask

1. What decision does this model or policy actually make, approve, decline, price, or set a limit, and can the specific reason for one applicant's decline be reconstructed and stated to them?
2. Does the affordability check reflect capacity to repay this obligation on top of everything else the applicant already owes, or only capacity to make the first payment?
3. What data trains or drives the decision, and does it encode a proxy for a protected characteristic, a postcode standing in for class, a device type standing in for income, that would not survive a fair-lending review?
4. Is this product legally credit under the applicable regime regardless of how it is marketed, and does it carry the disclosures and affordability duties that follow from that?
5. What is the collections and default communication cadence, and does it comply with contact-frequency and channel rules rather than whatever cadence maximised recovery in a backtest?
6. Does the product furnish repayment performance to a credit bureau, and if not, has anyone weighed the consumer's credit-building cost against the operational convenience of staying silent?
7. What happens to a borrower who disputes a decision or a reported delinquency, and is there a human review path that is real rather than decorative?
8. For an SME borrower, whose personal guarantee or personal credit file is actually on the hook, and does the product make that as clear to the owner as it is to the underwriting model?

## Gatekeepers

- **The consumer credit regulator.** The US CFPB enforcing fair-lending and debt-collection communication rules, the UK FCA's Consumer Duty and its extension of affordability requirements into buy now pay later, or the equivalent national authority; each can order restitution and halt a product line outright.
- **Fair-lending and model risk review, internal or the regulator's.** Tests the decisioning model for disparate impact across protected classes, not only accuracy; a strong model score is not a defence to a disparate-impact finding.
- **Credit bureaus.** Set furnishing formats and dispute-handling obligations; a furnisher that cannot correct a disputed record within the mandated window is itself in violation, independent of whether the original decision was right.
- **The prudential regulator, for lenders funded by deposits or wholesale debt.** Cares about portfolio concentration and provisioning, which bounds how fast originations are actually allowed to grow.
- **Collections compliance and legal.** Owns contact-frequency, cease-and-desist handling, and channel rules under debt-collection law; a new nudge channel shipped without this sign-off is a regulatory exposure, not a growth win.
- **National usury and licensing regimes.** Interest-rate caps and lender-licensing requirements vary by US state and by country; a lending product operating "nationally" inside a federal system is usually operating under a patchwork it has to reflect rather than average over.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Approval rate | Growth and access | Rises by loosening underwriting into a loan vintage whose loss rate has not matured yet; always read approval and loss rate from the same cohort |
| Portfolio delinquency or default rate | Credit quality | A young book looks artificially healthy before most loans have reached their typical time to default; read it by vintage, never in aggregate |
| Adverse-action reason accuracy | Fair-lending compliance | A plausible-sounding reason that does not reflect what the model weighted passes a light audit and fails a real one |
| Approval-rate disparity by protected class or proxy | Fair lending | An aggregate disparity within tolerance can still hide a much larger one in a single product tier or geography the aggregate averages away |
| Time to funds, approval to money in account | Competitive speed | Measured from approval rather than application, it hides earlier funnel friction and rewards fast but shallow underwriting |
| Collections recovery rate | Unit economics | Improves short term through contact strategies that later draw complaints or breach frequency limits, borrowing against future legal exposure |
| Roll rate between delinquency buckets | Early warning | A stable ratio can coexist with a growing absolute number of delinquent borrowers on a growing book, and the ratio hides the headcount |
| Repeat use rate across BNPL merchants | Engagement | Reads as loyalty when it can equally mean a borrower stacking concurrent obligations across providers, none of whom individually see it |
| Credit bureau dispute rate | Data quality | A low rate can mean accurate furnishing, or it can mean borrowers do not know they have the right to dispute at all |
| Cost per dollar collected | Collections efficiency | Improves by shifting effort toward easy accounts and away from hardship cases that need forbearance, not more contact |

## Reading

- **The US Equal Credit Opportunity Act and Regulation B.** The clearest statement of what a specific, non-cosmetic adverse-action reason looks like, worth testing a decisioning product's explanations against even outside the US.
- **The US Fair Credit Reporting Act and the CFPB's Regulation F.** Govern bureau furnishing and disputes, and debt-collection communication frequency and channel rules.
- **The UK FCA's Consumer Duty and its extension of affordability and disclosure requirements to buy now pay later.** The clearest non-US example of a regulator closing the "this does not look like credit" gap (verify current implementation status before relying).
- **CFPB guidance on algorithmic and AI-driven credit decisions.** Read for the position that "the model decided" is not a defence to a vague adverse-action reason; see [modules/regulated/README.md](../../modules/regulated/README.md) when a model drives the decision.
- **State Bank of Pakistan's prudential regulation for consumer and SME financing, and its microfinance and digital lending guidance.** A non-US example of a central bank setting affordability and disclosure expectations directly on lenders (verify current specifics before relying).
- **FATF and national guidance on SME beneficial-ownership checks.** Relevant wherever the borrower is a company, since the person actually guaranteeing the debt has to be identified correctly, not just the entity.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays, since a credit decision is financial regulation and a model making it stacks the AI overlay on top of that), DESIGN-3 (where PII lives, since a credit file and its derived features are exactly the sensitive data class this question forces onto the data model), DELIVER-3 (known issues, since an unresolved fair-lending finding has to be listed and signed, not quietly shipped), and OPERATE-3 (did the drivers move, since an approval-rate headline needs its loss-rate driver examined in the same breath).

**Templates this bends:** [eval-spec](../../templates/ai/eval-spec.md) (subgroup and disparate-impact slices are the acceptance criteria for a decisioning model), [privacy-impact-assessment](../../templates/architecture/privacy-impact-assessment.md) (credit and affordability data is sensitive by default), [risk-register](../../templates/execution/risk-register.md) (fair-lending and collections-compliance risk as standing rows, not one-off entries), and [business-rules](../../templates/definition/business-rules.md) (adverse-action logic and affordability thresholds belong here as testable rules, not model internals).
