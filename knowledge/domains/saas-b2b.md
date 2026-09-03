---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["B2B SaaS", "saas-b2b"]
---
# B2B SaaS

Selling software to companies means the person who feels the pain, the person who signs the contract, and the person who can veto the deal are usually three different people, and your product has to satisfy all of them in different documents. The economics are subscription economics: what you spend to land a customer against what that customer's revenue does after landing, which is why net revenue retention and CAC payback, not signups, are the numbers a board reads first.

## Questions a PM must ask

1. Who is the user, who is the economic buyer, and who is the blocker, by name and role in a real target account? A roadmap built for the user alone dies in procurement; one built for the buyer alone dies in adoption.
2. What does the security and procurement gauntlet require before a contract can sign: SOC 2 Type II, ISO 27001, a data processing agreement, a vendor risk questionnaire, insurance certificates? Each missing artifact is weeks of stall per deal.
3. What drives expansion: seats, usage, or tier upgrades? The answer decides the packaging, the pricing page, and half the roadmap, and it should be a decision, not an accident.
4. What is CAC payback in months, funded from gross margin, and is it inside the range the sales motion can afford? A payback period the business cannot finance turns growth into a countdown.
5. Which enterprise features are actually gate requirements in disguise: SSO, SCIM provisioning, audit logs, role-based access, data residency? IT admins do not adopt; they permit.
6. Is the motion product-led, sales-assisted, or both, and does the product's first-hour experience match the claim? A PLG label on a product that needs a demo call is a leaky funnel with better branding.
7. What happens when the champion leaves the account? Renewal risk concentrated in one advocate is a metric nobody tracks until the quarter it detonates.
8. What would migration away from us cost the customer, honestly? Switching cost you did not design is switching cost you do not have.

## Gatekeepers

- **Procurement and vendor risk.** Security questionnaires, DPAs, subprocessor lists, insurance, and legal redlines on the MSA; a deal is not late, it is queued behind artifacts you have or lack.
- **IT and security admins.** SSO, SCIM, audit logs, and access controls are their entry price; without them you sell to teams and get evicted by the platform review.
- **Data protection regimes.** GDPR and its cousins bind where customer data lives and which subprocessors touch it; residency asks arrive mid-deal and land on the architecture.
- **Existing system owners.** The tools you integrate with (CRM, ERP, identity) have admins whose change windows and API terms pace your rollout.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Net revenue retention (NRR) | Whether the installed base grows without new sales | Blends expansion and churn; a strong NRR can hide a logo-churn problem eating future expansion |
| Gross revenue retention (GRR) | Churn with the flattery removed | None, which is why boards ask for it second and trust it first |
| CAC payback (months, gross-margin basis) | Whether the growth engine finances itself | Excluding sales overhead or using revenue instead of gross margin flatters it badly |
| Logo churn vs revenue churn | Whether you are losing customers or just small ones | Averaging the two answers a question nobody asked |
| Time to first value | Whether the promise survives onboarding | Instrumented from contract, not from first login, or it misses the stall |
| Pipeline blocked on security review | The procurement tax, made visible | Nobody logs it unless the PM asks; ask |

## Reading

- **David Skok's SaaS metrics essays** (forEntrepreneurs, from 2010, maintained since). The canonical derivation of why churn compounds against growth, why negative net churn is the strongest force in the model, and what CAC payback range a sales motion can sustain. When someone quotes a SaaS benchmark at you, this is usually where it came from; read the original so you know the assumptions.
- **[Crossing the Chasm](../crossing-the-chasm.md)** applies with full force here: the procurement gauntlet is the mainstream buyer's reference-demand made bureaucratic. The card one level up covers it.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: you must name three), DEFINE-2 (the audience includes procurement and the admin), DESIGN-2 (integrations: identity and provisioning are entry criteria), and OPERATE-5 (the next bet is usually an NRR driver).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (security, audit, and residency targets become contract-driven, with the buyer's compliance calendar as the deadline) and [gtm-plan](../../templates/planning/gtm-plan.md) (the first cohort is an account profile, and the channel evidence includes a procurement path).
