---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Mobile money", "Mobile wallets", "Branchless banking", "mobile-money-wallets"]
---
# Mobile money and wallets

The interface for this product is often not a smartphone screen but a USSD menu, dialed as a short code over the GSM signaling channel, or simply a shopkeeper behind a counter who is the interface entirely. The agent is not a channel bolted onto the product; the agent's cash float on a given morning is as much a part of the product's real uptime as the app's server logs, and no backend engineering fixes an agent who ran out of cash.

The second distinctive fact: the stated mission, financial inclusion, and the product truth are in tension. Success is how much of daily life moves onto the ledger and stays there, not how many wallets a sign-up promotion registered. A wallet mostly used to cash out immediately after every deposit is a remittance pass-through wearing an inclusion story, not the thing the mission describes.

The third is that regulation here typically follows the product rather than preceding it. Kenya's M-Pesa launched through Safaricom in 2007 and ran for years under a central-bank no-objection arrangement before a dedicated e-money framework caught up to it (verify the exact regulatory milestones before relying); a product assuming law arrives first is reading this domain backward.

## Questions a PM must ask

1. Who exactly is this for: a feature-phone user with no data plan, a smartphone user who prefers USSD out of habit, or an agent acting on a customer's behalf? Designing for a smartphone persona in a USSD-majority market builds the wrong product well.
2. What did that person's cash workaround cost before this product existed, in time or a trip to pay a bill or send money home? Informal does not mean free; pricing it makes the product's value legible.
3. Does a low-value account get simplified due diligence, or is full KYC imposed on everyone regardless of risk? FATF's own guidance on financial inclusion endorses tiered, risk-based due diligence; ignoring it excludes the population the product claims to serve.
4. Is the agent network exclusive to this provider, or can the same shopkeeper serve a competitor too? Exclusive agency has historically been a barrier regulators pushed against, since it caps liquidity at the point of cash-in and cash-out.
5. What happens when a USSD session times out mid-transaction? A smartphone app can retry silently; a dropped USSD session can leave a customer unsure whether their money moved at all.
6. Does this wallet interoperate with the national instant-payment scheme or other wallets, or only work inside its own closed network? Interoperability, not registrations, is what makes it useful outside its own ecosystem.
7. How is the pooled customer-funds trust account reconciled against individual wallet balances, and how often? A mismatch here is every customer's money at once, found by an auditor rather than a dashboard.
8. What is the plan for a SIM swap or a lost device, given the phone number is often the entire identity credential? A recovery process built for biometrics does not transfer to a shared feature phone.

## Gatekeepers

- **The central bank's payment systems and e-money licensing function.** The State Bank of Pakistan's EMI Regulations and Branchless Banking Regulations for non-bank issuers and agent-based models, and the Central Bank of Kenya's oversight of e-money issuance under its national payment system framework. Decides who may hold pooled customer funds at all.
- **The mobile network operator, where the wallet is telco-led.** Controls the USSD short code, SIM registration data, and often the agent network itself; a telco can reprice or throttle USSD access to a wallet competing with its own product, with no regulatory process behind that decision.
- **The national instant-payment scheme operator.** Pakistan's Raast and India's UPI, run by NPCI, set the interoperability rules a wallet must implement to reach accounts outside its own network; staying outside the scheme caps a wallet's usefulness no matter how good its own engineering is.
- **Super-agents and agent-network managers.** The layer between the provider and the shopkeeper, setting commission and float-replenishment logistics that decide whether an agent has cash on hand on a given day, the product's real-world availability.
- **The financial intelligence unit applying tiered due diligence.** Decides how much simplified KYC a low-value tier may use before stepping up to full verification, directly setting onboarding friction and the addressable unbanked population.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Registered wallets | Headline reach | Vastly overstates usage; a one-time cash-out during a sign-up promotion counts the same as a wallet used every week |
| 30-day active wallets | Real, ongoing usage | The number providers are most reluctant to report, precisely because it is usually far smaller than registrations |
| Cash-in/cash-out volume | Liquidity moving through the agent network | Mostly cash-out right after cash-in is a remittance pass-through, not money staying digital, the actual point of the inclusion story |
| Agent density per population | Physical accessibility | Averages hide urban clustering; the rural areas the mission targets are often the thinnest served and the average never shows it |
| USSD session success rate | Reliability of the primary interface for many users | Measured server-side, it misses the session timeouts and dropped calls the subscriber experiences at the network's edge |
| Off-net or interoperable transaction share | Whether the wallet functions beyond its own closed network | A low share can be reported as engagement when it is really a captive customer with no way to pay someone on another network |
| Float and trust-account reconciliation accuracy | Whether pooled funds match individual balances | Usually invisible until an agent cannot honor a cash-out and the customer finds the discrepancy before the provider's own systems do |
| Agent commission as a share of transaction value | Sustainability of the agent network's economics | A thin commission looks efficient for the provider while quietly pushing agents to ration service or refuse small transactions |
| KYC tier distribution | Whether tiered due diligence works as designed | Nearly everyone on the lowest tier can mean good inclusion design or unmonitored laundering exposure; the number alone cannot say which |
| Average transaction value | Product usage pattern | A falling average can mean inclusion of smaller customers or a shrinking base doing fewer big transactions; the wallet-count trend beside it says which |

## Reading

- **GSMA's Mobile Money guidelines and its State of the Industry material.** Read for the interoperability and consumer-protection framing GSMA pushes providers toward, not for any figure to quote elsewhere.
- **The Central Bank of Kenya's regulatory path for M-Pesa, from a no-objection arrangement toward formal e-money regulation (verify the specific instrument and year before relying).** Read for how regulation followed a working product rather than preceding it, the reverse order from a bank launch.
- **The State Bank of Pakistan's EMI Regulations and Branchless Banking Regulations.** Read for the tiered-account and agent-banking rules underneath wallets like Easypaisa and JazzCash, and the structure Raast now layers interoperability on top of.
- **FATF guidance on AML/CFT measures and financial inclusion.** Read for the risk-based, tiered-CDD justification that lets a low-value wallet use simplified due diligence without breaching AML law.
- **NPCI's documentation of India's UPI.** Read as the contrasting model: bank-account interoperability designed in from the start, rather than wallet interoperability retrofitted onto a closed network years later.

**Conductor overlay:** this domain sharpens DISCOVER-1 (the person is often unbanked and reachable only through USSD or an agent, not the researcher's own channels), DISCOVER-3 (an informal, cash-based workaround is not a free one, and pricing it is evidence this domain most often skips), DESIGN-2 (the agent network and the national switch are integrations with an SLA, not a partnership), and OPERATE-2 (active wallets against registered wallets is this domain's clearest number-versus-number gap).

**Templates this bends:** [personas](../../templates/discovery/personas.md) (the agent is a persona alongside the wallet holder), [journey-map](../../templates/discovery/journey-map.md) (a cash-in or cash-out journey includes a human agent step no screenshot can show), [integrations](../../templates/architecture/integrations.md) (the agent network's float logistics and the national switch both need an owner and an SLA), and [north-star-metric](../../templates/planning/north-star-metric.md) (active, on-ledger balance belongs at the root, not registration counts).

**Filled in this repo:** this is the one sector with a filled journey built for it. Sahulat Bill Pay is a fictional mobile-money wallet in Pakistan, carrying this card's own sector tag:
- [sahulat-journey.md](../../examples/sahulat-journey.md) is the index and data sheet for the whole Sahulat journey; start here for the shared facts (the agent network, the KYC tiers, the cash-out pattern) every other Sahulat artifact reconciles against.
- [sahulat-personas.md](../../examples/sahulat-personas.md) fills the personas template this card bends, and already carries the agent as a named persona alongside the wallet holder, exactly the substitution this card's questions ask for.
- [sahulat-north-star-metric.md](../../examples/sahulat-north-star-metric.md) fills the north-star-metric template this card bends; read it for a metric built on active, on-ledger balance rather than a registration count.
- [sahulat-opportunity-assessment.md](../../examples/sahulat-opportunity-assessment.md) carries this card's own sector tag and the [payments acquiring](payments-acquiring.md) tag together; read it for how the ten discovery questions get answered when cash-workaround cost and tiered KYC are live constraints, not afterthoughts.
- [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) fills the integrations template this card bends, but only near: Harbourgate is a retailer's payment-provider register, useful for the owner-plus-SLA pattern, but its rows are card acquirers, not an agent network's float logistics or a national instant-payment switch.
- [sahulat-journey-map.md](../../examples/sahulat-journey-map.md) fills the journey-map template this card bends directly: Shazia's five-stage bill-pay journey, including the branch-or-shop trip this card's agent-network point is about, and a backstage note naming the exact reconciliation gap between the branch/shop till and the biller's system that the [payments acquiring](payments-acquiring.md) card's post-authorisation question also raises.

**Worked example (ILLUSTRATIVE):** a journey-map stage this card's agent-persona and USSD-timeout questions would add, for the fictional wallet holder persona from sahulat-personas.md, none of it real:

| | Stage 2: Cash-in at the agent |
|---|---|
| **User actions** | Hands the agent 2,000 rupees and their phone number; waits while the agent keys the deposit into the agent app |
| **Touchpoints and tools** | Agent's smartphone app (not the customer's own phone); customer's feature phone receives an SMS confirmation only, no USSD prompt at this step |
| **Thoughts** | "Did that actually go through, or do I need to ask him to check again?" |
| **Emotion (high / neutral / low)** | Low, session INT-011 (ILLUSTRATIVE): agent app froze mid-transaction and the customer left without a confirmation SMS, unsure if the deposit posted |
| **Pain and friction** | The customer has no direct visibility into the transaction; if the agent's session times out silently, there is no receipt independent of what the agent chooses to say |
| **Moments of truth** | Customer decides whether to trust this agent again, or walk to a competing agent's shop next time, a decision made on this one interaction, not on the app's uptime dashboard |

**Backstage note:** the agent's float balance at the moment of this transaction decides whether the cash-in even completes; a backend that is fully up produces this exact failure mode when the agent ran out of float, which is why the fix here is a float-replenishment SLA, not a retry button.
