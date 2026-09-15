# Coverage: domain cards and role rungs

F26 in the 2026-09-12 audit named the gap this file closes: the knowledge
layer advertises 47 domain cards and a role ladder of 8 rungs plus 7
specializations, and a catalog that size can imply a confidence the tree has
not earned. This file says, per card and per rung or specialization, exactly
what kind of evidence exists for it and what does not, so breadth and
validation are never read as the same claim.

## What the four columns mean

- **Reference.** The card or rung exists as a knowledge document: named
  gatekeepers, metrics and how they lie for a domain card; scope, decision
  rights and failure modes for a role rung or specialization. Every row in
  this file is "yes" here, because every one of the 47 cards and 15
  rungs/specializations is at minimum a reference document.
- **Worked example.** A filled artifact in `examples/` demonstrates the card
  or rung on an invented company, so a reader can see the domain's or role's
  distinguishing content applied rather than only described.
- **Expert-reviewed.** An outside practitioner in that domain or at that rung
  reviewed the card and their review is recorded in this repository.
- **Field-tested.** The card or rung's guidance was used on a real, non-
  fictional product and the outcome is recorded in this repository.

**Expert-reviewed and field-tested read "none recorded" for every row in
this file**, because no file anywhere in this tree records an outside
practitioner's review or a real deployment for any domain card or role rung.
That is a statement about what this repository holds, not a claim that no
domain card has ever been read by a practitioner; absence of a record is
read as absence of evidence here, per this file's own rule, not as a
judgment on the card's quality.

## How this was generated

Computed from the tree at commit `558e37c`, by a small script that lists
`knowledge/domains/*.md` (excluding `README.md` and `INDEX.md`) for the 47
domain ids, matches each `examples/domain-<id>-<artifact>.md` file to its
domain by longest-prefix match, and reads the `## N. Title` headings of
`knowledge/roles/ladder.md` and the `## Title` headings of
`knowledge/roles/specializations.md` for the 8 rungs and 7 specializations.
The script is in the PR handoff; reproduce its counts directly with:

```bash
python3 -c "
import os
ids = sorted(f[:-3] for f in os.listdir('knowledge/domains')
             if f.endswith('.md') and f not in ('README.md', 'INDEX.md'))
examples = sorted(f for f in os.listdir('examples')
                   if f.startswith('domain-') and f.endswith('.md'))
matched = set()
for ef in examples:
    rest = ef[:-3][len('domain-'):]
    cands = [d for d in ids if rest == d or rest.startswith(d + '-')]
    if cands:
        matched.add(max(cands, key=len))
print(len(ids), 'domain cards,', len(matched), 'with a worked example')
"
```

That prints `47 domain cards, 41 with a worked example` on this tree. The
"no rung and no specialization has a worked example yet" line in
[CHANGELOG.md](../CHANGELOG.md) is the source for every "none recorded"
worked-example cell in the role table below; this file trusts that dated,
first-party disclosure rather than re-deriving it, since there is no
`examples/role-*` naming convention to scan for.

## Domain cards (47)

41 of the 47 have at least one worked example under `examples/`. The other
six, `ai-products`, `fintech`, `mobile-money-wallets`, `payments-acquiring`,
`retail-in-store` and `saas-b2b`, are reference-only: their content exists
and their worked example, if any is added later, will be a new row in this
table, not a retroactive change to this one. `fintech` is deliberately a
pointer card (see [README.md](../README.md)), so it routes a model-bearing
financial product to the regulated module and the fourteen financial-services
cards rather than carrying its own worked example.

| Domain card | Reference | Worked example | Expert-reviewed | Field-tested |
|---|---|---|---|---|
| [Aerospace and defence](../knowledge/domains/aerospace-defence.md) | yes | [domain-aerospace-defence-analytics-instrumentation-spec.md](../examples/domain-aerospace-defence-analytics-instrumentation-spec.md) | none recorded | none recorded |
| [Agritech](../knowledge/domains/agritech.md) | yes | [domain-agritech-business-case.md](../examples/domain-agritech-business-case.md) | none recorded | none recorded |
| [AI products](../knowledge/domains/ai-products.md) | yes | none recorded | none recorded | none recorded |
| [Automotive and mobility](../knowledge/domains/automotive-mobility.md) | yes | [domain-automotive-mobility-risk-register.md](../examples/domain-automotive-mobility-risk-register.md) | none recorded | none recorded |
| [Capital markets](../knowledge/domains/capital-markets.md) | yes | [domain-capital-markets-nfr.md](../examples/domain-capital-markets-nfr.md) | none recorded | none recorded |
| [Card issuing](../knowledge/domains/card-issuing.md) | yes | [domain-card-issuing-risk-register.md](../examples/domain-card-issuing-risk-register.md) | none recorded | none recorded |
| [Construction and AEC](../knowledge/domains/construction-aec.md) | yes | [domain-construction-aec-business-rules.md](../examples/domain-construction-aec-business-rules.md) | none recorded | none recorded |
| [Consumer social](../knowledge/domains/consumer-social.md) | yes | [domain-consumer-social-failure-scenarios.md](../examples/domain-consumer-social-failure-scenarios.md) | none recorded | none recorded |
| [Core banking](../knowledge/domains/core-banking.md) | yes | [domain-core-banking-sla-slo-definition.md](../examples/domain-core-banking-sla-slo-definition.md) | none recorded | none recorded |
| [Crypto and digital assets](../knowledge/domains/crypto-digital-assets.md) | yes | [domain-crypto-digital-assets-nfr.md](../examples/domain-crypto-digital-assets-nfr.md) | none recorded | none recorded |
| [Cybersecurity and GRC](../knowledge/domains/cybersecurity-grc.md) | yes | [domain-cybersecurity-grc-nfr.md](../examples/domain-cybersecurity-grc-nfr.md) | none recorded | none recorded |
| [Developer tools, APIs and platforms](../knowledge/domains/devtools-api.md) | yes | [domain-devtools-api-nfr.md](../examples/domain-devtools-api-nfr.md) | none recorded | none recorded |
| [Ecommerce](../knowledge/domains/ecommerce.md) | yes | [domain-ecommerce-metrics-review.md](../examples/domain-ecommerce-metrics-review.md) | none recorded | none recorded |
| [Edtech](../knowledge/domains/edtech.md) | yes | [domain-edtech-compliance-impact-assessment.md](../examples/domain-edtech-compliance-impact-assessment.md) | none recorded | none recorded |
| [Embedded finance and banking as a service](../knowledge/domains/embedded-finance-baas.md) | yes | [domain-embedded-finance-baas-integrations.md](../examples/domain-embedded-finance-baas-integrations.md) | none recorded | none recorded |
| [Energy and utilities](../knowledge/domains/energy-utilities.md) | yes | [domain-energy-utilities-sla-slo-definition.md](../examples/domain-energy-utilities-sla-slo-definition.md) | none recorded | none recorded |
| [ERP and enterprise finance](../knowledge/domains/erp.md) | yes | [domain-erp-nfr.md](../examples/domain-erp-nfr.md) | none recorded | none recorded |
| [Fintech](../knowledge/domains/fintech.md) | yes | none recorded | none recorded | none recorded |
| [Food delivery and quick commerce](../knowledge/domains/food-delivery-quick-commerce.md) | yes | [domain-food-delivery-quick-commerce-risk-register.md](../examples/domain-food-delivery-quick-commerce-risk-register.md) | none recorded | none recorded |
| [Gaming](../knowledge/domains/gaming.md) | yes | [domain-gaming-release-readiness.md](../examples/domain-gaming-release-readiness.md) | none recorded | none recorded |
| [Hardware and IoT](../knowledge/domains/hardware-iot.md) | yes | [domain-hardware-iot-nfr.md](../examples/domain-hardware-iot-nfr.md) | none recorded | none recorded |
| [Healthtech](../knowledge/domains/healthtech.md) | yes | [domain-healthtech-compliance-impact-assessment.md](../examples/domain-healthtech-compliance-impact-assessment.md) | none recorded | none recorded |
| [HR technology](../knowledge/domains/hr-tech.md) | yes | [domain-hr-tech-eval-spec.md](../examples/domain-hr-tech-eval-spec.md) | none recorded | none recorded |
| [Insurance](../knowledge/domains/insurance.md) | yes | [domain-insurance-business-rules.md](../examples/domain-insurance-business-rules.md) | none recorded | none recorded |
| [Islamic finance](../knowledge/domains/islamic-finance.md) | yes | [domain-islamic-finance-decision-log.md](../examples/domain-islamic-finance-decision-log.md) | none recorded | none recorded |
| [Legaltech](../knowledge/domains/legaltech.md) | yes | [domain-legaltech-data-model.md](../examples/domain-legaltech-data-model.md) | none recorded | none recorded |
| [Lending and credit](../knowledge/domains/lending-credit.md) | yes | [domain-lending-credit-risk-register.md](../examples/domain-lending-credit-risk-register.md) | none recorded | none recorded |
| [Logistics](../knowledge/domains/logistics.md) | yes | [domain-logistics-failure-scenarios.md](../examples/domain-logistics-failure-scenarios.md) | none recorded | none recorded |
| [Manufacturing and industrial](../knowledge/domains/manufacturing-industrial.md) | yes | [domain-manufacturing-industrial-nfr.md](../examples/domain-manufacturing-industrial-nfr.md) | none recorded | none recorded |
| [Marketplaces](../knowledge/domains/marketplaces.md) | yes | [domain-marketplaces-north-star-metric.md](../examples/domain-marketplaces-north-star-metric.md) | none recorded | none recorded |
| [Marketing and advertising technology](../knowledge/domains/martech-adtech.md) | yes | [domain-martech-adtech-metrics-dictionary.md](../examples/domain-martech-adtech-metrics-dictionary.md) | none recorded | none recorded |
| [Media and publishing](../knowledge/domains/media-publishing.md) | yes | [domain-media-publishing-business-rules.md](../examples/domain-media-publishing-business-rules.md) | none recorded | none recorded |
| [Mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) | yes | none recorded | none recorded | none recorded |
| [Payments acquiring](../knowledge/domains/payments-acquiring.md) | yes | none recorded | none recorded | none recorded |
| [Pharma and life sciences](../knowledge/domains/pharma-life-sciences.md) | yes | [domain-pharma-life-sciences-eval-spec.md](../examples/domain-pharma-life-sciences-eval-spec.md) | none recorded | none recorded |
| [Proptech and real estate](../knowledge/domains/proptech-real-estate.md) | yes | [domain-proptech-real-estate-data-model.md](../examples/domain-proptech-real-estate-data-model.md) | none recorded | none recorded |
| [Public sector and GovTech](../knowledge/domains/public-sector-govtech.md) | yes | [domain-public-sector-govtech-release-readiness.md](../examples/domain-public-sector-govtech-release-readiness.md) | none recorded | none recorded |
| [Regtech, AML and KYC](../knowledge/domains/regtech-aml-kyc.md) | yes | [domain-regtech-aml-kyc-business-rules.md](../examples/domain-regtech-aml-kyc-business-rules.md) | none recorded | none recorded |
| [Remittances](../knowledge/domains/remittances.md) | yes | [domain-remittances-failure-scenarios.md](../examples/domain-remittances-failure-scenarios.md) | none recorded | none recorded |
| [Retail (in-store)](../knowledge/domains/retail-in-store.md) | yes | none recorded | none recorded | none recorded |
| [B2B SaaS](../knowledge/domains/saas-b2b.md) | yes | none recorded | none recorded | none recorded |
| [Sports betting and iGaming](../knowledge/domains/sports-betting-igaming.md) | yes | [domain-sports-betting-igaming-metrics-dictionary.md](../examples/domain-sports-betting-igaming-metrics-dictionary.md) | none recorded | none recorded |
| [Streaming and OTT](../knowledge/domains/streaming-ott.md) | yes | [domain-streaming-ott-dependency-register.md](../examples/domain-streaming-ott-dependency-register.md) | none recorded | none recorded |
| [Telecom](../knowledge/domains/telecom.md) | yes | [domain-telecom-nfr.md](../examples/domain-telecom-nfr.md) | none recorded | none recorded |
| [Transaction banking](../knowledge/domains/transaction-banking.md) | yes | [domain-transaction-banking-failure-scenarios.md](../examples/domain-transaction-banking-failure-scenarios.md) | none recorded | none recorded |
| [Travel and hospitality](../knowledge/domains/travel-hospitality.md) | yes | [domain-travel-hospitality-failure-scenarios.md](../examples/domain-travel-hospitality-failure-scenarios.md) | none recorded | none recorded |
| [Wealth and investing](../knowledge/domains/wealth-investing.md) | yes | [domain-wealth-investing-business-rules.md](../examples/domain-wealth-investing-business-rules.md) | none recorded | none recorded |

## Role ladder (8 rungs)

None of the eight rungs has a worked example: [knowledge/roles/ladder.md](../knowledge/roles/ladder.md)
is reference content, each rung stating what it owns, decides and how it
fails, without a fictional company walking that rung end to end.

| Role rung | Reference | Worked example | Expert-reviewed | Field-tested |
|---|---|---|---|---|
| Associate Product Manager | yes | none recorded | none recorded | none recorded |
| Product Manager | yes | none recorded | none recorded | none recorded |
| Senior Product Manager | yes | none recorded | none recorded | none recorded |
| Principal Product Manager (IC track) | yes | none recorded | none recorded | none recorded |
| Group Product Manager (management track) | yes | none recorded | none recorded | none recorded |
| Director of Product | yes | none recorded | none recorded | none recorded |
| VP of Product | yes | none recorded | none recorded | none recorded |
| Chief Product Officer | yes | none recorded | none recorded | none recorded |

## Specializations (7)

Same status as the ladder: [knowledge/roles/specializations.md](../knowledge/roles/specializations.md)
distinguishes each specialization from its neighbours by what it owns and
what it does not produce, with no worked example yet.

| Specialization | Reference | Worked example | Expert-reviewed | Field-tested |
|---|---|---|---|---|
| Core PM | yes | none recorded | none recorded | none recorded |
| Product Owner | yes | none recorded | none recorded | none recorded |
| Technical PM | yes | none recorded | none recorded | none recorded |
| Growth PM | yes | none recorded | none recorded | none recorded |
| Platform PM | yes | none recorded | none recorded | none recorded |
| Data PM | yes | none recorded | none recorded | none recorded |
| AI PM | yes | none recorded | none recorded | none recorded |

## What this does and does not license

This matrix is reference inventory, not a roadmap. Per the finding's own
fix text, role and domain journeys get added only when a real pilot exposes
a need for one, not to raise a coverage count in this table. A domain
card's worked example is one invented company applying that domain's
distinguishing content to one template; it is evidence the card's content is
usable, not evidence the card is correct for every company in that
industry, and it is never expert review or field use, the two columns nothing
here currently satisfies.
