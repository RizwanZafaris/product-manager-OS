---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Crypto", "Digital assets", "VASP", "crypto-digital-assets"]
---
# Crypto and digital assets

The ledger this product writes to is public, irreversible, and not yours: a mis-sent transaction is usually gone, which makes key management the core of the product rather than a backend detail. The custodial-versus-non-custodial choice is the business model in miniature: custody is easier for the user and puts you in the position every major collapse in this industry has failed at, while self-custody pushes an unforgiving failure mode, a lost seed phrase, an irreversible send, onto a customer who never signed up to be their own bank.

The second distinctive fact is jurisdictional patchwork by design: the same token can be a security, a commodity, or an unregulated instrument depending on where the holder sits, and regulators are still actively deciding which. A license built for one classification does not travel with a token across a border, and "regulation by enforcement" has been a live pattern here, not a hypothetical. The third is that a private counterparty, not a regulator, often stops you first: a banking partner can exit a crypto relationship unilaterally on its own risk appetite, taking your fiat on-ramp with it overnight.

## Questions a PM must ask

1. Is this product custodial or non-custodial for this specific flow, and does the customer actually understand which? A "your keys, your coins" line beside a custodial hot wallet is a claim that will not survive a support ticket.
2. What license or registration covers this activity here: a VASP or CASP authorization, a money transmitter license, a specific virtual-asset law? The activity needing a license is defined by what the product does, not by what you call it.
3. What share of customer assets sits in cold storage versus hot wallets, and what is the actual process for moving between them? A firm-wide percentage can hide one badly overexposed hot wallet.
4. Does this transfer trigger the FATF travel rule, and can you actually exchange originator and beneficiary information with the receiving VASP? A wallet address alone is not compliance once a transfer crosses the threshold that applies.
5. What happens to withdrawals when compliance needs to review an account? A median SLA hides the tail of accounts frozen indefinitely, which is where customer trust actually breaks.
6. If asked for proof of reserves, what would the attestation prove, assets held, liabilities owed, or only the first? A reserves snapshot with no liabilities figure proves solvency of nothing.
7. Has the smart contract this product relies on been audited, and by whom? Code that moves money is a live financial instrument the moment it deploys.
8. What is the plan if your banking partner exits the relationship on days of notice? A single-bank fiat rail is a single point of failure no blockchain redundancy fixes.

## Gatekeepers

- **The licensing regulator for the activity.** MiCA's CASP authorization in the EU (stablecoin rules from mid-2024, the general licensing regime from the end of that year, verify exact dates), Singapore's MAS under the Payment Services Act, Japan's FSA registration built after the Mt. Gox and Coincheck incidents, Dubai's VARA, and New York's BitLicense (23 NYCRR Part 200). Different names, the same function: no license, no legal fiat rail.
- **The banking or payments partner.** Not a regulator, and more decisive day to day than one: a bank can debank a crypto customer on its own AML risk appetite, a decision that routinely arrives with no hearing.
- **The FATF travel-rule counterparty network.** Recommendation 16 requires originator and beneficiary information to travel with a transfer above a threshold; without an interoperable way to exchange it, many firms simply block withdrawals to unknown wallets rather than risk non-compliance.
- **Sanctions enforcement, including against addresses and code.** OFAC's designation of the Tornado Cash smart contract addresses on 8 August 2022 showed that code, not only a person or entity, can become a sanctioned target overnight; the Fifth Circuit held in Van Loon v. Department of the Treasury, 26 November 2024, that the immutable contracts were not property that could be designated, and OFAC removed Tornado Cash from the list on 21 March 2025. Both halves are the lesson: the designation landed on every product in the ecosystem the same day, and its reversal took over two years of litigation.
- **The proof-of-reserves auditor or attestor.** An attestation under agreed-upon procedures is not a full audit; it proves assets exist, not that liabilities are covered, and naming that difference to users is the real job.
- **The smart-contract auditor, for any DeFi-adjacent feature.** An unaudited contract handling customer funds is a live financial product regardless of how it is labeled internally.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Proof-of-reserves ratio | Assets held versus customer liabilities | Can be satisfied by borrowing assets briefly right before the snapshot, a documented criticism of point-in-time attestations |
| Share of assets in cold storage | Custody risk exposure | A healthy firm-wide average can coexist with one hot wallet dangerously overexposed on any given day |
| Travel-rule message match rate | Compliance coverage on transfers | Measured only against trusted partner VASPs, silently excluding the harder counterparties routed around instead |
| Withdrawal processing time | Whether customers can actually get their funds | The median looks fine while a tail of accounts sits frozen pending review, which is what matters to those customers |
| Sanctioned-address screening hit rate | AML screening effectiveness | Inflated by low match thresholds that also raise false negatives, the failures nobody sees until an examiner finds them |
| Stablecoin peg deviation | Confidence in the peg mechanism | Looks stable measured only in calm markets, and says nothing about redemption-queue risk under stress, exactly what mattered for TerraUSD in May 2022 |
| On-chain versus off-chain transaction mix | How much activity actually settles on the public ledger | A high off-chain share can mean efficient netting or an IOU ledger wearing a blockchain's branding |
| Chargeback and fraud rate on card on-ramps | Fraud exposure at the fiat entry point | Card-network chargeback windows outlast the irreversible crypto send on the other side of the same transaction |
| Key-recovery success rate | Whether customers who lose access can get it back | A high rate for a custodial product can mean the product is not meaningfully non-custodial at all |
| Time from listing to delisting under investigation | Token risk management | A fast delisting looks responsible and can also mean there was never a real due-diligence process before listing it |

## Reading

- **FATF's guidance for a risk-based approach to virtual assets and VASPs.** The primary text behind the travel rule, Recommendation 16; read it before any vendor's compliance summary.
- **MiCA, Regulation (EU) 2023/1114.** Read Title III on asset-referenced and e-money tokens and Title V on crypto-asset service providers; the phased application dates matter more than the passage date.
- **FinCEN's 2013 guidance (FIN-2013-G001) on virtual currency administrators and exchangers as money services businesses.** The foundational US reading connecting crypto activity to the Bank Secrecy Act framework.
- **New York's BitLicense, 23 NYCRR Part 200.** Finalised in June 2015, the first dedicated state-level virtual-currency licensing regime in the US, still the reference point competitors measure their own burden against.
- **SEC v. Coinbase, Inc., filed 6 June 2023 in the Southern District of New York.** Read for the theory of the case rather than any outcome, since which tokens are securities remains genuinely unsettled.
- **Public reporting on the FTX collapse, filed for Chapter 11 bankruptcy on 11 November 2022.** Read for the custody-commingling failure that made proof of reserves a customer expectation afterward.

**Conductor overlay:** this domain sharpens DESIGN-3 (private keys and identity data are both PII questions with a residency answer, not just a security one), DESIGN-6 (seeing the system misbehave means watching peg deviation and reserve ratios in real time, not waiting for a quarterly attestation), DELIVER-10 (the stop condition is usually a withdrawal halt, the crypto-specific circuit breaker), and OPERATE-8 (the counter-metric behind a healthy-looking reserves ratio is the liabilities figure nobody published beside it).

**Templates this bends:** [security-architecture](../../templates/architecture/security-architecture.md) (the custody and key-management model is the architecture, not an appendix to it), [nfr](../../templates/definition/nfr.md) (withdrawal SLA and cold-storage thresholds are hard requirements with a trust consequence attached), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (an exchange hack, a chain reorganization, and a stablecoin depeg are named scenarios, not generic outage rows), and [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (travel-rule data sharing across a border is a privacy assessment as much as an AML one).

**Filled in this repo:** [domain-crypto-digital-assets-nfr.md](../../examples/domain-crypto-digital-assets-nfr.md) fills the [nfr](../../templates/definition/nfr.md) template directly for this domain, for Northbank Digital: withdrawal latency per asset with an executive escalation path, a hot-wallet share cap with cold-storage reconciliation and reserve-attestation cadence, a signing-quorum requirement, and travel-rule data sent before settlement above the FATF Recommendation 16 threshold, because a slow withdrawal or a thin cold-storage margin is exactly what becomes a run once it is noticed. For the other three bent templates, [harbourgate-security-architecture.md](../../examples/harbourgate-security-architecture.md), [harbourgate-failure-scenarios.md](../../examples/harbourgate-failure-scenarios.md) and [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) remain the nearest reading, for the trust-boundary table, a payments outage set, and the cross-border transfer table, though none carries a custody, chain-reorganization, or stablecoin-depeg scenario.

**Worked example (ILLUSTRATIVE):** two filled NFR rows for a fictional exchange, Northbank Digital, showing how the sector turns a generic availability requirement into a custody-and-trust requirement.

| Requirement | Target | Measured how | Verified by |
|---|---|---|---|
| Withdrawal processing time, standard queue | 95% of withdrawals confirmed on-chain within 4 hours; anything held past 24 hours auto-escalates to a named compliance reviewer instead of sitting in the queue | Withdrawal-request timestamp to on-chain broadcast timestamp, per request | Withdrawal-latency dashboard, owner Head of Treasury |
| Cold storage share of customer assets | No less than 95% of customer asset value in cold storage at every daily snapshot; any breach pages the CISO within 15 minutes | Daily snapshot comparing hot and cold wallet balances | Custody attestation log |

A generic NFR would stop at "withdrawals should be fast" and "funds should be safe." The sector fact forcing a number and an escalation path onto both rows is that a slow withdrawal and a thin cold-storage margin are the two events that turn into a bank run the moment either one is noticed publicly.
