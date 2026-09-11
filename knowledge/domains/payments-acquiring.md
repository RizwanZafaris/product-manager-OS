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

**Filled in this repo:** the best-covered sector in the repository, between two journeys tagged with this card:
- [harbourgate-journey.md](../../examples/harbourgate-journey.md) is the index for a fictional retailer replacing a nine-year checkout payment layer across three providers; start here, it carries this card's own sector tag alongside retail in-store and ecommerce and names which provider (Kestrel, Marlowe, Tidewater) is the merchant of record's actual liability at each point.
- [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) fills the integrations template this card bends directly: an eleven-row register with an owner, a status, and a retirement date per acquiring provider, exactly the "who owns the failure behavior" shape this card's Questions section asks for.
- [harbourgate-nfr.md](../../examples/harbourgate-nfr.md) shows a Gate 2 non-functional-requirements document returned once for lacking a measurable "at least as good as the old path," then re-signed; read it for how a PCI-scoping and authorisation-latency requirement gets written so a spec-review pass cannot wave it through unmeasured.
- [sahulat-opportunity-assessment.md](../../examples/sahulat-opportunity-assessment.md) carries this card's tag alongside [mobile money and wallets](mobile-money-wallets.md); read it for the acquiring-adjacent version of this card's questions when the rail underneath is a wallet's own cash network rather than a card scheme.
- [ledgerline-pricing-packaging.md](../../examples/ledgerline-pricing-packaging.md) fills the pricing-packaging template this card bends, but only near: Ledgerline is B2B SaaS tier design, useful for the transparency-versus-margin discipline, but it never has to show a merchant an interchange-plus breakdown against a blended-rate competitor.
- [harbourgate-failure-scenarios.md](../../examples/harbourgate-failure-scenarios.md) fills the failure-scenarios template this card bends: read it for the reconciliation-gap detection and recovery-owner shape this card's post-authorisation question asks for.

**Worked example (ILLUSTRATIVE):** a failure-scenarios row this card's post-authorisation question would add, for the fictional Quay payment service from the Harbourgate examples, none of it real:

| ID | Scenario | Blast radius | Detection | Recovery | Data loss risk |
|---|---|---|---|---|---|
| FS-9 | network authorises the transaction, but the order-fulfilment service fails before the order is created (ILLUSTRATIVE) | affected customers see a completed charge, no order confirmation, and no visible way to tell whether it will arrive or not | reconciliation job comparing authorised-transaction count to created-order count, alerting above a 0.1% gap over 15 minutes; a customer report before then is the honest fallback | auto-void the authorisation if unconfirmed after 10 minutes, or auto-create the order from the authorisation record if fulfilment recovers first, whichever resolves first; owner: payments on-call; target 15 minutes to first customer-visible state | none for funds (authorisation only, not captured), but order intent can be lost if the reconciliation job itself lags |

This is the scenario a generic "payment service down" row never names: the network's own authorisation succeeded, so nothing in the payment path looks broken, and the actual failure is a chargeback and a support ticket waiting to happen thirty days later unless the reconciliation gap is caught within minutes, not discovered at month-end close.
