---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Remittances", "cross-border remittances", "remittance corridor", "money transfer operator"]
---
# Remittances

A remittance has two ends, and they are not symmetric. The sender abroad chose your app; the receiver at home did not, and judges the product entirely by whether cash or wallet funds actually arrive at a place they can reach, not by anything on a screen. A corridor, the licensed path between one sending country and one receiving one, is the real unit of this business: cost, speed, and regulatory friction vary so widely by corridor that a single global average number describes nothing real. Every corridor bundles four things that can each fail independently: a licence to send in the origin country, a licence or exemption to pay out in the destination country, an FX spread that is usually the largest and least visible part of the price, and a payout network of agents or wallets whose local cash liquidity is an operational fact, not a digital one. Any of the four can close on you: a correspondent bank can end the relationship that lets the money settle across borders long before any regulator asks you to stop, a pattern well documented in higher-risk corridors and known in the industry as de-risking.

## Questions a PM must ask

1. Who experiences a delay, the sender who already paid, or the receiver waiting for cash, and can either of them actually reach a human when something goes wrong?
2. What is the total cost to the sender including the FX margin, not only the disclosed fee? A fee-only comparison misleads wherever the spread carries most of the real margin.
3. What happens to the receiver's money if the specific payout agent they are standing in front of has no cash on hand today?
4. Which entity is licensed to send in the origin country, and which is licensed or exempted to pay out in the destination one, and do the two licences actually cover this exact corridor?
5. Is beneficiary information travelling with the payment the way FATF Recommendation 16 expects, or only checked at the front end and dropped somewhere in transit?
6. Where does sanctions and politically exposed person screening actually happen, at send, at payout, or both, and what happens to a transfer that is held mid-flight?
7. Does the disclosed delivery time match reality in this specific corridor, given local payout hours, holidays, and agent liquidity, or is it a global average dressed up as a promise?
8. If the correspondent bank or payout partner behind this corridor ends the relationship, what is the fallback, and how much real notice does the product actually get before it happens?

## Gatekeepers

- **Money transmitter regulators in every jurisdiction touched.** A state-by-state licensing regime in the US, authorisation as a payment institution under the UK and EU frameworks, and in Pakistan the State Bank's licensing and supervision of exchange companies and authorised remittance channels.
- **Correspondent and settlement banks.** They can end the account a remittance business depends on for cross-border settlement on commercial notice, not regulatory notice, and that termination is often the true cause of a corridor going dark.
- **Sanctions and PEP screening, owned by compliance.** Every transfer is screened before or during payout, and a held transfer is a compliance decision, not a system bug, which the product needs a way to communicate without disclosing what compliance forbids explaining.
- **The payout network itself.** Whether an owned network or a partner, a mobile money operator such as Kenya's M-Pesa, or a cash agent network, it controls the last mile no amount of app polish can digitise away, including agent float and identity checks at cash-out.
- **Receiving-country central banks.** Many, the State Bank of Pakistan among them, regulate how inbound remittances must settle, for example requiring payout in local currency through licensed channels, which bounds what "instant payout" can actually mean.
- **FATF, via Recommendation 16.** Not a regulator itself, but the standard-setter whose wire transfer rule national regulators convert into binding originator and beneficiary information requirements.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Total cost as a share of the transfer, fee plus FX margin | True cost to the sender | Reporting the fee alone hides the FX spread, which is exactly why the World Bank tracks cost this way rather than by fee |
| Time to payout, initiation to funds available | Speed | Measured as a system timestamp rather than receiver-experienced availability, which depends on agent hours and liquidity, not message delivery |
| First-time payout success rate | Reliability | Retries and manual interventions can be excluded from the denominator, making a fragile corridor look smooth |
| Corridor coverage, countries and currencies reached | Reach | A corridor can be technically covered while actual payout liquidity or agent density is thin across most of it |
| Sanctions screening false-positive rate | Screening quality | Driving it toward zero usually means the matching threshold was loosened, which is a sanctions risk dressed as a UX win |
| Complaint rate per thousand transfers | Service quality | The receiver, who has no relationship with the sending app, has no channel to complain into, so receiver-side failure is structurally undercounted |
| Payout point liquidity or uptime | Last-mile reliability | A digital "transfer complete" status can be true while the cash point is empty, and the two systems rarely reconcile with each other |
| Compliance hold rate and duration | Control friction versus experience | A falling hold rate can mean better screening, or a quietly loosened control, and the two look identical on a dashboard |
| Active corridor count year over year | Growth | A corridor lost to de-risking and a new one opened elsewhere can net to the same number while trust in the lost corridor is gone |
| FX rate offered versus the mid-market rate at that moment | Pricing transparency | Quoting against a stale mid-market snapshot flatters the disclosed margin against the rate a sender could actually get elsewhere right then |

## Reading

- **The World Bank's Remittance Prices Worldwide database.** The standard corridor-level cost dataset, and the reason a "low fee" claim needs a same-corridor comparison before it means anything.
- **UN Sustainable Development Goal target 10.c.** The international policy benchmark, remittance costs below three percent, that regulators and NGOs use to judge pricing.
- **FATF Recommendation 16**, the wire transfer rule, sets the baseline for what originator and beneficiary information must travel with a cross-border transfer.
- **The State Bank of Pakistan's regulatory framework for exchange companies and home remittance channels.** A non-US example of a receiving-country regulator shaping payout currency and channel requirements (verify current specifics before relying).
- **FATF and World Bank reporting on correspondent banking de-risking.** Documents why remittance corridors, especially to higher-risk geographies, can lose banking access even when the remittance business itself is fully compliant.
- **Kenya's M-Pesa** as the canonical mobile money payout rail, useful for understanding how a wallet-based payout changes last-mile economics against a cash agent network.
- **A note on screening models:** where sanctions or fraud screening runs on a machine learning model rather than list matching alone, treat the model itself as the case in [modules/regulated/README.md](../../modules/regulated/README.md).

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person, since the receiver, not the paying sender, usually experiences the failure), DESIGN-2 (integrations, because every correspondent bank and payout partner needs an owner and a failure behavior, de-risking included), DEFINE-8 (overlays, since money moving across borders makes the regulator half a yes, which leaves the model half to decide whether the regulated overlay fires, per the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md)), and OPERATE-4 (cost to run, where held-transfer support volume is the operational load that matters).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (every correspondent and payout partner needs a named failure behavior), [personas](../../templates/discovery/personas.md) (sender and receiver as two distinct, unequally powerful personas), [pricing-packaging](../../templates/planning/pricing-packaging.md) (fee and FX margin have to be modeled and disclosed as one price, not two), and [failure-scenarios](../../templates/delivery/failure-scenarios.md) (a compliance hold and an illiquid payout agent are named scenarios, not edge cases discovered in production).
