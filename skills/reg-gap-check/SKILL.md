---
name: reg-gap-check
description: Regulatory gap analysis for payments and fintech product specs. Use when a PM has a PRD, feature spec, or roadmap item touching money movement, cards, wallets, lending, crypto or customer data, and needs to know what a regulator, scheme, or compliance reviewer will challenge before building. Outputs a severity-ranked gap table with owners and evidence needed. Routes verified regulatory citations through the regulated module and never invents regulator text.
---

# Regulatory Gap Check: find the challenge before the regulator does

Most payments product work dies in review, not in build. The PM ships a spec, then legal, compliance, the scheme, or the central bank asks the question nobody wrote down, and the roadmap slips a quarter. This skill runs the challenge in advance.

## Files this skill drives

- [../../modules/regulated/README.md](../../modules/regulated/README.md), which explains when the regulated overlay activates and names the canonical source
- [../../modules/regulated/templates/regulated-ai-prd-template.md](../../modules/regulated/templates/regulated-ai-prd-template.md), the byte-exact template whose section 0 and Appendix A hold the repository's only verified regulatory citations
- [../../modules/regulated/SKILL.md](../../modules/regulated/SKILL.md), the authoring procedure for a regulated AI PRD
- Findings land in [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md) and, where an assessment is warranted, trigger [../../templates/operate/compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md)

## The citation rule, before anything else

This skill maps gaps; it does not write regulation. The only regulator text this repository vouches for lives inside `modules/regulated/`, where every citation carries the date it was verified against primary text. When a gap touches an instrument covered there, cite it by pointing into the module. When a gap touches any other regime, name the domain and say "verify against the [market] regime" with the evidence type that would close it. Never reconstruct a rule, a section number, a threshold, or a quotation from memory: an invented citation is worse than a named unknown, because it gets believed.

## When to use

- Before a PRD for any money-touching feature goes to engineering
- Before a market-entry or corridor decision is committed to a roadmap
- When inheriting a product and needing to know where the regulatory debt sits

## Inputs

The spec or PRD text, plus (ask if missing): target markets, customer type (consumer, merchant, both), money-flow direction (pay-in, payout, stored value, cross-border), card involvement (acquiring, issuing, tokenized credentials), data residency posture.

## The eleven domains checked

1. **Licensing and perimeter**: does this feature change what license the activity needs? Stored value, holding funds, FX conversion, payment initiation, and crypto each move the perimeter. Flag any feature that quietly crosses from "technical service" to "regulated activity."
2. **AML / CFT**: screening, transaction monitoring coverage for the NEW flow, threshold and reporting duties, whether the risk assessment was updated for this feature.
3. **KYC / KYB and onboarding**: does the feature admit a new customer class the current onboarding tiers were not designed for? Tiered-approval fit, beneficial ownership.
4. **Sanctions**: list screening at the right point in the NEW flow, not just at onboarding; cross-border legs re-screened per hop.
5. **Card scheme rules**: if cards touch it: acquiring vs issuing obligations, credential storage class, tokenization requirements, chargeback and dispute duties, MIT/CIT classification for any stored-credential or recurring flow. Scheme rulebooks are licensed documents; cite the reference and version, never paste or reconstruct the text.
6. **Data protection and residency**: what personal data the feature creates, where it is stored and processed, cross-border transfer basis, retention. Payments data often carries residency duties the app database was not designed for.
7. **PCI-DSS scope**: does the feature EXPAND scope (new place PAN or credentials flow)? Scope expansion found late is one of the most expensive review failures.
8. **Strong authentication**: SCA / 3DS obligations and exemptions for the flow, step-up triggers, and what the fallback is when authentication fails.
9. **Consumer protection and disclosure**: fees shown before commitment, FX margin disclosure, refund and complaint paths, marketing claims the product cannot evidence.
10. **Operational resilience and outsourcing**: new critical vendor in the flow? Regulator notification, exit plan, uptime and incident duties that now apply to the vendor's leg.
11. **Emerging regimes where relevant**: payment token / stablecoin rules, open banking consent models, instant payment scheme mandates, e-invoicing. Checked against the TARGET market's regime, not a generic one; ask which market before assuming.

## Workflow

1. Classify the feature: money flow, parties, markets, card involvement, data created.
2. If the feature contains an AI or agentic component in a regulated market, stop and route the PRD itself through [../../modules/regulated/SKILL.md](../../modules/regulated/SKILL.md) first; this skill then runs over the result as the second pass.
3. Run all eleven domains. For each, produce PASS (spec addresses it), GAP (silent), or CONFLICT (spec contradicts a known obligation).
4. For every GAP and CONFLICT: state the specific challenge a reviewer would raise, in one sentence, the way they would say it.
5. Rank by severity: BLOCKER (cannot ship in a market), MAJOR (ships but creates licensing or audit exposure), MINOR (fixable in copy or config).
6. Name the evidence that closes each gap (a legal opinion, a scheme doc, a DPIA, a scope assessment) and the natural owner. Carry BLOCKER and MAJOR rows into the risk register.

## Output format

| # | Domain | Finding | Severity | The challenge as a reviewer would phrase it | Evidence to close | Owner |
|---|---|---|---|---|---|---|

Close with the three questions the PM should ask their compliance team THIS WEEK, the ones whose answers change the build.

## Honesty rule

This skill maps gaps; it does not give legal advice. Where a regime is market-specific and unstated, say "verify against [market] regime" rather than inventing the rule. Where the regulated module covers the instrument, point there; its citations carry verification dates and this skill's prose does not.

## Exit gate

This skill's output feeds Gate 2 and Gate 5 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md). Do not report the check done until every domain has a verdict, every BLOCKER and MAJOR has an owner and named closing evidence, and the three compliance questions are written.
