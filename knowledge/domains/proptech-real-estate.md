---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Proptech", "real estate technology", "property technology", "proptech-real-estate"]
---
# Proptech and real estate

This domain runs two loops that rarely share a codebase and never share a regulator: the discovery loop of search, leads, and showings, and the transaction loop of financing and conveyancing that moves title and money. A feature that speeds up search can slow the transaction if it produces leads that title and lending cannot process at the same rate. The second distinctive fact: "neutral" fields rarely are. Address, zip code, name, and photo correlate tightly with race, national origin, and familial status, and fair-housing law does not require intent, only effect. Outside the US MLS and title-insurance model, the transaction loop looks different again: across most of continental Europe a civil-law notary, not an escrow company, is the instrument that clears title, and software built around the American closing process breaks quietly the first time it meets one.

## Questions a PM must ask

1. Is this a search or lead feature, a financing or closing feature, or a tenancy or property-management feature? Each loop has different gatekeepers and different money changing hands.
2. Which fields does the ranking, targeting, or screening model use, and do any correlate with a protected class such as race, national origin, or familial status? Since Inclusive Communities (2015), effect is enough; intent is not required.
3. Are we a broker of record, a technology vendor to brokers, or a lender or servicer? The answer decides which license, fiduciary duty, and regulator attaches, regardless of how the company describes itself.
4. For a valuation or pricing feature: when the automated estimate is badly wrong on a specific address, who absorbs the error? Zillow's own iBuying arm found out the answer is whoever guaranteed the price.
5. For a mortgage or disclosure feature: does the timeline respect the Loan Estimate and Closing Disclosure delivery windows, and what happens to the clock when a term changes late? TRID's timing is not a UX preference.
6. For a tenant-facing feature: what data feeds a screening decision, and can an applicant see why they were declined? Criteria drawn from eviction or criminal records carry disparate-impact exposure independent of any algorithm.
7. Who actually clears title in this market: a title company, a closing attorney, or a notary? The closing mechanism is jurisdiction-specific and does not transplant across borders.
8. What is the local liquidity? Real estate is intensely local; a product tuned to one metro's inventory can be unusable three counties over, let alone in another country's tenure system.

## Gatekeepers

- **State or provincial real estate licensing boards.** License brokers and agents, discipline misrepresentation and undisclosed dual agency, and increasingly govern how buyer-broker compensation must be disclosed, following the 2024 NAR commission-lawsuit settlement (verify current effective date and terms before relying).
- **HUD and the Fair Housing Act, with DOJ backing.** Bar discrimination in the sale, rental, or advertising of housing on race, color, religion, sex, national origin, familial status, and disability. Disparate-impact claims are cognizable per Texas Dept. of Housing & Community Affairs v. Inclusive Communities Project (2015). HUD's 2019 charge against Facebook over housing-ad targeting, later settled with changes to how housing ads may be delivered, is the canonical algorithmic case (verify exact settlement terms and date before relying).
- **The CFPB.** Administers RESPA's anti-kickback rules on referral fees, and TRID's disclosure timing; also led an interagency rulemaking on quality-control standards for automated valuation models in mortgage lending (verify current status and effective date before relying).
- **MLS rules and the operating association (NAR in the US).** Not a government regulator, but a private rulebook deciding what a listing is, when it must be shared under the Clear Cooperation Policy, and now how buyer-broker compensation may be displayed; violating it can get a product delisted regardless of what the law allows.
- **Title insurers, closing attorneys, or, in most civil-law jurisdictions, the notary.** The instrument that actually clears title and disburses funds. Across France, Germany, and much of continental Europe a licensed notary, not an escrow company, must certify the transfer.
- **State and local landlord-tenant regulators.** Govern security-deposit trust accounting, habitability, and eviction procedure for property-management products; rules are set locally and rarely generalize.
- **Anti-money-laundering supervisors.** Real estate is a recognized laundering channel; in the UK, estate agency businesses carry AML supervision under the Money Laundering Regulations, and many markets require source-of-funds checks above a threshold (verify your market's threshold before relying).

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Days on market | Listing velocity and pricing accuracy | A relist resets the clock; an average hides listings quietly withdrawn and reposted to look fresh |
| Listing-to-close conversion rate | Whether leads become closed transactions | Counts contingent or financing-pending contracts as wins before title or financing cleared |
| Automated valuation accuracy (median error) | Whether the pricing model can be trusted | A tight median hides a fat tail of misses on exactly the homes the business is exposed on when it guarantees the price |
| Cost per qualified lead | Agent or brokerage acquisition efficiency | "Qualified" is self-defined; loosen it and the number improves while sales drowns in unworkable leads |
| Time to close (mortgage) | Financing throughput | Rate-lock extensions and TRID re-disclosure loops get absorbed as "in process" rather than counted as delay |
| Fair-housing complaint rate | Discrimination exposure the company already sees | A low count measures who complained, not who was silently filtered out by a screening rule |
| Occupancy rate (property management) | Portfolio health | Rises if management tolerates below-market rent to avoid vacancy, or defers maintenance-driven turns |
| Rent collection rate | Cash-flow health | A near-perfect rate during a grace period can mask arrears that land on the ledger all at once when it ends |
| Tenant-screening denial rate, by criterion | Where the applicant funnel narrows | An aggregate rate looks neutral while one criterion denies one group disproportionately |
| Commission or fee payout time | Agent cash cycle | Improves by pushing disputed payouts into a later period instead of resolving them |

## Reading

- **The Fair Housing Act (1968) and HUD's implementing regulations.** Read the seven protected classes and the definition of familial status directly; most teams can name three from memory and miss the rest.
- **Texas Dept. of Housing & Community Affairs v. Inclusive Communities Project (2015).** The Supreme Court held disparate-impact claims cognizable under the Fair Housing Act; a facially neutral rule is judged by its effect, not its intent.
- **HUD's 2019 charge against Facebook over housing-ad targeting**, and the resulting change to how housing, employment, and credit ads may be delivered (verify exact settlement terms and date before relying).
- **CFPB's TILA-RESPA Integrated Disclosure (TRID) rule**, effective October 2015. Read the Loan Estimate and Closing Disclosure timing directly before assuming a disclosure-flow change is cosmetic.
- **Reporting on Zillow Offers' November 2021 shutdown.** The clearest public case of an automated-valuation product meeting real inventory risk once the company started buying homes at its own estimate.
- **UK Estate Agents Act 1979 and the Consumer, Estate Agents and Redress Act 2007.** A non-US model worth reading for contrast: agents must join a redress scheme and are separately supervised for anti-money-laundering compliance, with no MLS-equivalent system underneath.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: the applicant or tenant a screening tool filters is not the broker or landlord who bought the software), DESIGN-2 (integrations: MLS, title or notary, and lending systems you do not control and cannot get an SLA from), DESIGN-3 (where address, name, and photo fields live and what they proxy for, not only where PII sits), and DELIVER-4 (the first cohort is a metro market, because liquidity and law are both local).

**Templates this bends:** [personas](../../templates/discovery/personas.md) (landlord, tenant, applicant, and agent are four people with different leverage), [data-model](../../templates/architecture/data-model.md) (mark which fields proxy for a protected class, not only which are PII), [integrations](../../templates/architecture/integrations.md) (MLS, title or notary, and loan-origination systems as third-party dependencies with someone else's SLA), [gtm-plan](../../templates/planning/gtm-plan.md) (the first cohort is a metro, not a country), and [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (fair-housing and AVM quality-control rows alongside privacy rows).
