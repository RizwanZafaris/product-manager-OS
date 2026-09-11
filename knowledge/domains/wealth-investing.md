---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Wealth management", "Retail brokerage", "Robo-advice", "wealth-investing"]
---
# Wealth and investing

This product recommends what to do with somebody else's money, and the fee you earn and the outcome the client needs are not automatically the same thing. Every other domain sells something for money; this one is trusted with the money itself, and the loop has to show the recommendation served the client before it shows anything else. A brokerage that executes orders, a robo-adviser allocating a model portfolio, and an asset manager running a fund sit on one spectrum: how much discretion you take over someone's money, and how squarely the law puts the client's interest ahead of your revenue.

The second distinctive fact: "advice" versus "execution" is a regulatory line, not a marketing choice. The moment a product recommends rather than merely executes, a duty attaches, suitability, appropriateness, or a best-interest standard depending on jurisdiction, and it attaches to the interaction, not to the app store listing's wording. A savings nudge can become investment advice the moment it recommends a specific fund. Where an algorithm chooses the allocation, the questions below sit on top of [the regulated module](../../modules/regulated/README.md) rather than replacing it.

## Questions a PM must ask

1. Does this feature give a recommendation, or only take an instruction? The line decides whether a suitability duty attaches, and a feature that quietly crosses it, a "recommended for you" fund list, inherits the duty without anyone deciding to take it on.
2. What does the client's risk profile and objective actually say, and when was it last confirmed? A model portfolio built on a two-year-old questionnaire is being run against a person who may not exist anymore.
3. Who holds the client's assets, and how are they segregated from the firm's own money? Custody failure is the domain's worst outcome, and a clean app is no evidence the money behind it is safe.
4. What is the all-in cost to the client, including anything the firm earns from routing the order rather than from the client? A fee schedule and the real cost are different documents until proven otherwise.
5. Can the client reach a human when the algorithm's answer feels wrong to them? A robo-adviser with no override path is a suitability duty with nobody to discharge it.
6. What happens to the model portfolio during a market shock the backtest never saw? Rebalancing logic tested only in calm markets is untested.
7. Which license covers this activity here, and does it cover advice, execution, or both? A broker-dealer license and an investment-adviser license are not the same permission, and a launch plan assuming one covers the other stalls at the regulator.
8. If the statement and the model's internal record disagree, which is the client's legal record, and how fast can support produce it? A dispute here is a regulatory complaint waiting to be filed, not a support ticket.

## Gatekeepers

- **The suitability or best-interest compliance officer.** Approves the risk questionnaire and the advice model, and any retuning of either; a re-tuned recommendation algorithm is a compliance change, not just a release.
- **The securities regulator that licenses the activity.** The SEC and FINRA for US broker-dealers under Regulation Best Interest, the FCA for UK firms under the Consumer Duty, the SECP for brokers and asset managers in Pakistan, SEBI for investment advisers in India. Each can suspend the license the product depends on.
- **The custodian or clearing firm.** Holds the client's assets and enforces segregation rules, the FCA's CASS sourcebook, the US Customer Protection Rule; a custody failure here is the client's money, not a data breach.
- **The exchange or venue, through the best-execution duty.** MiFID II Article 27 requires "all sufficient steps" toward the best result on price, cost, speed, and likelihood of execution; FINRA Rule 5310 asks for "reasonable diligence" to the same end.
- **The investor-protection scheme, where one exists.** SIPC in the US covers up to $500,000 per client, of which $250,000 can be cash; it insures against the firm's failure, not the market falling, and conflating the two is the trap.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Assets under management (AUM) | Scale of the business | Grows with market appreciation the firm did nothing to earn, and one large client leaving looks like a hundred small ones leaving |
| Net new assets | Whether clients are choosing you, market moves aside | Counts a bonus-driven transfer the same as a considered decision, identical the quarter the client leaves |
| Cost to serve versus revenue yield | Whether a segment is worth serving at its price | A profitable-looking segment can be subsidized by a captive one cross-funding another client's low fee |
| Suitability override or exception rate | Whether risk profiling is actually gating trades | Near zero looks clean and usually means the gate is decorative; an engaged advice process produces exceptions |
| Portfolio drift from target allocation | Whether the model is doing what it promised | Measured firm-wide, it hides accounts nobody has rebalanced in a year inside an average that looks fine |
| Trading or portfolio turnover | Activity, and for a fee-per-trade model, revenue | High turnover in a fee-per-trade account is a conflict of interest wearing the costume of engagement |
| Payment for order flow as a share of revenue | Dependence on a routing-based revenue source | Can rise while execution quality falls, paid for by different parties for different things |
| Complaint and suitability-breach rate | Whether the advice model is serving clients | Falls when complaints become harder to file, not when advice improves; read it beside the channel's friction |
| Client risk-tolerance re-confirmation rate | Whether the profile behind every recommendation is current | A high onboarding completion rate says nothing about whether anyone was asked again five years later |
| Time to liquidate and disburse | Whether a client can actually get their money out | Measured only for the median request, while the tail, disputed and frozen accounts, is where the damage sits |

## Reading

- **MiFID II, Directive 2014/65/EU, Article 27 on best execution.** Read the "all sufficient steps" wording directly; it is a process obligation, which is why a best-execution policy document exists as a named artifact in EU firms.
- **SEC Regulation Best Interest, effective 30 June 2020.** Read Form CRS alongside the rule: the disclosure a retail client receives is often the more useful document for a PM than the rule text.
- **FCA Consumer Duty, PS22/9, in force for open products from 31 July 2023 (verify the closed-book date before relying, since it followed a year later).** Read it for the outcomes it names, avoiding foreseeable harm and enabling clients to pursue their objectives, rather than as a checklist.
- **SEC actions against Wealthfront Advisers LLC and Hedgeable, Inc., December 2018.** The first enforcement actions against robo-advisers, over misleading statements about tax-loss harvesting and undisclosed conflicts (verify the exact figures before relying).
- **SEBI (Investment Advisers) Regulations, 2013, India.** Read for a fiduciary standard separating advice from distribution, a structural answer to the conflict Reg BI and the Consumer Duty address differently.

**Conductor overlay:** this domain sharpens DISCOVER-1 (the person is the account holder, not the household, and their stated goal may not match their actual risk capacity), DEFINE-5 (a requirement fails here as a suitability breach or a bad fill, not a bug ticket), DESIGN-6 (seeing an advice model misbehave means watching portfolio drift and concentration, not just error rates), and OPERATE-8 (the counter-metric behind a rising AUM or turnover number is almost always a conflict of interest).

**Templates this bends:** [business-rules](../../templates/definition/business-rules.md) (the suitability and appropriateness logic is a business rule with a named owner, not an algorithm detail), [nfr](../../templates/definition/nfr.md) (best execution and custody segregation become hard non-functional requirements with a regulator behind them), [personas](../../templates/discovery/personas.md) (risk tolerance and time horizon belong in the persona, not a separate onboarding form), and [release-readiness](../../templates/delivery/release-readiness.md) (a new instrument or model change needs suitability sign-off in the readiness table, not just a QA pass).

**Filled in this repo:** [domain-wealth-investing-business-rules.md](../../examples/domain-wealth-investing-business-rules.md) fills the [business-rules](../../templates/definition/business-rules.md) template directly for this domain, for Ashford Wealth: the BR-014 rule blocking new discretionary recommendations when a risk questionnaire is older than 24 months, a best-execution venue review, a concentration limit for discretionary portfolios, an appropriateness test for complex products under UK COBS 10 and MiFID II, the US Regulation Best Interest care obligation, and employee personal-dealing surveillance, with the execution-only carve-out stated explicitly and compliance holding change control. For the other three bent templates, [harbourgate-nfr.md](../../examples/harbourgate-nfr.md), [sahulat-personas.md](../../examples/sahulat-personas.md) and [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md) remain the nearest reading for the dated-revision-log, evidence-based-persona, and prior-NO-GO shapes, though none carries a suitability or best-execution fact.

**Worked example (ILLUSTRATIVE):** A suitability business rule, in the shape of `templates/definition/business-rules.md` section 1. Every name and ID below is invented.

| ID | Rule statement (WHEN ... THEN ...) | Trigger point | Source of truth | Business owner | Exceptions | Enforced by | Test traceability |
|---|---|---|---|---|---|---|---|
| BR-014 | WHEN a client's risk questionnaire is more than 24 months old THEN block any new discretionary trade recommendation until it is reconfirmed | Order entry, before a recommendation is generated | Suitability policy v4, held by the Best-Interest Compliance Officer | Farah Siddiqui, Best-Interest Compliance Officer | Execution-only orders the client initiates unprompted are not blocked, since no recommendation attaches to them | REG-BI-11 | AC-22 |

A generic business rule names a trigger and an owner; this one adds a staleness clock the regulator, not the product team, effectively sets, and an exception carved out precisely at the line where advice stops and execution starts.
