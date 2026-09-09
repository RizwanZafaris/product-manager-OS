---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Payments and acquiring", "merchant acquiring", "payment service provider", "PSP", "payments-acquiring"]
---
# Payments acquiring

Acquiring runs on a four-party model: the cardholder, the issuer, the acquirer, and the card network, with a payment service provider or gateway often sitting on top of the acquirer and a merchant underneath all of it. The first thing a PM here has to know is which of those parties the product actually is, because liability for fraud and chargebacks attaches to a specific party by network rule, not to whoever built the checkout screen. The essence of the business shows up in two numbers merchants actually feel: authorisation rate is what they lose over today, at the point of sale, and chargebacks and scheme fines are what they lose over months later, long after the transaction felt finished. Interchange, the fee a network sets and routes to the issuer, is not something an acquirer or PSP controls, though it flows through their pricing; blended pricing hides it from the merchant, interchange-plus pricing exposes it. PCI DSS applies to anyone who stores, processes, or transmits card data, and every product decision to reduce that scope, tokenisation, a hosted field, a redirect, has a direct and permanent compliance cost consequence.

## Questions a PM must ask

1. In this flow, are we the merchant of record, the PSP, the gateway, or the acquirer, and does our contract and our actual liability match which one we are?
2. Who absorbs a chargeback when it happens, is it passed to the merchant, absorbed by the platform, or contested, and does the product show the merchant the deadline they are already on the clock for?
3. Does this feature touch the raw card number, or does it stay inside a PCI-scoped boundary already reduced by tokenisation or a hosted field? Every "just capture the card number here" request re-expands that scope.
4. Is this transaction card-present or card-not-present, and does the fraud and liability model the design assumes actually match which one it is?
5. What is the true cost stack to the merchant, interchange, scheme fees, acquirer markup, and any PSP markup on top, and is it shown to them in a form they can compare against a competitor?
6. What happens when a payment is approved by the network but fulfilment fails afterward, and does the refund route back through the same rail on the same timeline the customer expects?
7. Which card networks and local payment methods does this checkout actually support in the merchant's real market, or does "we support cards" quietly mean the two networks that were easiest to integrate?
8. What evidence does a merchant need to win a dispute in this category, and does the product capture it, delivery confirmation, a signed receipt, a matching device fingerprint, at the time of the transaction rather than after the dispute lands?

## Gatekeepers

- **The card networks**, Visa, Mastercard, and regional or domestic schemes. Set interchange, chargeback rules and deadlines, and merchant category codes, and can fine an acquirer, who passes the fine and the underlying risk down to the merchant or PSP.
- **The acquiring bank.** Underwrites the merchant, carries settlement risk between authorisation and funding, and can freeze funds or terminate the relationship outright on a fraud or chargeback pattern.
- **The PCI Security Standards Council, via PCI DSS.** Not a regulator, but contractually mandated by every network and acquirer; an unencrypted card-data breach is a security failure and a contractual one at once.
- **National payment services regulators.** Strong customer authentication requirements under the EU and UK's post-PSD2 framework, state money-transmitter regimes in the US depending on structure, and Pakistan's State Bank licensing payment system operators and payment service providers directly.
- **The acquirer's or network's risk and underwriting desk.** Sets merchant category code, processing limits, and reserve requirements; a product that lets a merchant quietly change what they sell invites exactly the fraud pattern this desk exists to catch.
- **Interchange and scheme-fee regulators, where they exist.** The EU's Interchange Fee Regulation caps certain consumer card interchange (verify current cap levels before relying), the clearest example of a jurisdiction capping a fee an acquirer's own pricing model assumes is fixed.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Authorisation approval rate | Checkout conversion health | Rises by routing risky-looking transactions to a more lenient acquirer, which raises fraud loss the metric never sees |
| Chargeback ratio | Dispute exposure | Networks judge it against transaction count, so inflating small, low-risk volume elsewhere quietly dilutes a bad ratio |
| Fraud loss as a share of volume | Risk control | Falls when legitimate transactions are declined more aggressively, trading fraud loss for lost sales the P&L records under a different line |
| Blended processing cost | Unit economics | Hides that one high-interchange card type, a premium or a commercial card, is quietly the least profitable segment being served |
| Time to settlement, authorisation to payout | Merchant cash flow | A headline "next day" figure can exclude a rolling reserve held against newer or riskier merchants |
| Dispute win rate | Evidence and process quality | A merchant who stops contesting low-value disputes because it is not worth the effort looks identical to one who is simply losing more |
| PCI scope, systems in assessment | Compliance cost and breach surface | A "compliant" status says nothing about whether scope quietly grew as new features started touching card data |
| Checkout conversion rate | UX health | Improves by skipping step-up authentication a regulator or network actually requires, borrowing against future chargeback and liability exposure |
| Refund cycle time | Customer trust | A fast "refund initiated" status can precede a slow actual return of funds to the customer's statement, and the two get conflated |
| Merchant onboarding time | Growth | Improves by underwriting faster and lighter, which is exactly the shortcut that produces the fraud-prone book risk has to clean up later |

## Reading

- **PCI DSS**, from the PCI Security Standards Council. Read the scoping guidance before any feature that could touch a card number, not the headline requirements list.
- **Visa and Mastercard's public chargeback and dispute rulebooks.** Read the reason codes and time limits for the merchant's actual category, not a generic summary of "how disputes work."
- **The EMV chip liability shift for card-present counterfeit fraud.** The reference case for how a network rule reallocated fraud liability between issuers and merchants (verify current category-specific dates before relying).
- **The EU's strong customer authentication regime under the post-PSD2 framework.** The clearest example of a checkout-level control mandated by regulation rather than by scheme rule, so "just remove the extra step" is not always the product's call.
- **State Bank of Pakistan's Payment Systems and Electronic Fund Transfers framework.** A non-US example of a central bank directly licensing payment system operators and payment service providers rather than leaving oversight to card-network contracts alone (verify current specifics before relying).
- **A note on fraud scoring:** where authorisation or risk decisions run on a machine learning model rather than static rules, treat the model as the AI in finance case in [modules/regulated/README.md](../../modules/regulated/README.md).

**Conductor overlay:** this domain sharpens DEFINE-5 (how requirements fail, since "handle chargebacks" is not testable but a deadline and an evidence requirement is), DESIGN-2 (integrations, since the acquirer, gateway, and network each need an owner and a failure behavior), DISCOVER-1 (name the person, since merchant, cardholder, and issuer each carry a different stake in the same transaction), and OPERATE-8 (the counter-metric, since an approval-rate experiment needs a fraud-loss counter-metric in the same window).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (acquirer, gateway, and network each get an owner, SLA, and failure behavior), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (a chargeback deadline and a post-authorisation fulfilment failure are named scenarios), [dashboard-spec](../../templates/operate/dashboard-spec.md) (approval rate and fraud loss belong on one dashboard so neither moves unseen), and [pricing-packaging](../../templates/planning/pricing-packaging.md) (interchange-plus versus blended pricing is a transparency decision, not only a margin one).
