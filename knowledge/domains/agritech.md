---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Agritech", "AgTech", "precision agriculture", "farm management", "agritech"]
---
# Agritech

Most software domains assume a smartphone, a bank account, and a title deed. Agritech, sold at any scale, cannot assume any of the three: a majority of the world's farms are smallholdings, often without registered land title, working with feature phones and patchy connectivity, in markets where a bad season is not a business risk but a subsistence risk. The distinctive fact of this domain is that the farmer using the product and the customer paying for it are frequently different people again, an input company, a lender, a cooperative, or a buyer, which means the product has to serve someone with almost no power to reject a bad design.

The second distinctive fact is that weather is an uncontrolled variable sitting on top of every metric you will ever report. A good rainfall year makes a mediocre product look transformative, and a bad one makes a good product look like it failed, so any yield, adoption, or repayment claim needs a comparison to what would have happened anyway.

## Questions a PM must ask

1. What does a farmer do today without this product, and what does that workaround actually cost in time, money, or risk? A workaround such as walking to a market town to sell grain is the baseline every value claim has to beat.
2. What does the product assume about land title, identity documents, or collateral, and what happens to the farmer who has none of them? Where land tenure is informal, a product built around a title deed excludes the smallholders it claims to serve.
3. What does the product assume about connectivity and device: a smartphone with data, a feature phone with SMS or USSD, or nothing reliable at all? Designing for the smartphone-and-broadband case first is designing for the minority.
4. Whose money moves through this product, over what rail, and what happens when that rail's operator changes its terms? In most emerging markets the payment rail is a telco's mobile-money system, not yours, and its rules set your ceiling.
5. Is a yield, income, or repayment claim adjusted for weather, or does a good season simply get credited to the product? Without a comparison group or a normal-year baseline, the claim is a correlation wearing causation's clothes.
6. Who is the trusted intermediary who actually drives adoption: an extension agent, a cooperative, an input dealer? Smallholder adoption usually runs through a person the farmer already trusts, not through an app store.
7. What input is this product recommending or selling, and is it registered for use in the country the farmer is in? A marketplace listing an unregistered pesticide or uncertified seed has created a legal and safety problem, not a sales one.
8. What happens to a farmer's credit standing or access if the model behind a lending or input-advance decision is wrong for their specific plot? A regional model applied to one smallholding can be confidently, and consequentially, wrong.

## Gatekeepers

- **The national input regulator.** Pesticide and seed registration regimes, echoed internationally by frameworks such as the EU's plant-protection-product rules or the OECD Seed Schemes, decide which inputs a marketplace may legally list at all.
- **Land administration and tenure authorities.** Where land records are incomplete, documented by the FAO's own tenure guidance, a product assuming a title deed as collateral or identity anchor will fail on exactly the smallholders it claims to serve.
- **Mobile network operators and mobile-money schemes.** The payment rail underneath most emerging-market agritech, commonly a telco-run mobile-money system, is owned by someone else, and its API terms and agent-network reach set the ceiling on what the product can move.
- **Commodity exchanges or warehouse-receipt authorities, where one exists.** A structure such as a national commodity exchange substitutes a graded, warehoused receipt for a land title as bankable collateral, and only works inside that exchange's own grading and settlement rules.
- **Equipment and data-interoperability standards.** Compliance with an interoperability standard for farm equipment decides whether the product can read a tractor or implement's own data at all, regardless of what the farmer wants to share.
- **Agricultural extension services and cooperatives.** In many smallholder markets, a government extension agent or a cooperative, not the farmer alone, is the trusted party who decides whether a new tool gets adopted.
- **Carbon-credit or sustainability-claim verifiers.** Where the product monetizes a carbon or sustainability claim, a registry's verification standard, and its credibility, gates whether that claim can be sold at all.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Active farmer retention through a full season | Genuine adoption versus a promotion spike | A single-season signup surge after a subsidy looks identical to real adoption until the next planting season arrives |
| Yield uplift attributed to the product | Product impact on output | Weather is the dominant variable in any single season; without a control group, a good rainfall year gets credited to the app |
| Input-marketplace GMV | Commercial traction | Pre-season, credit-driven purchases can be returned, left unused, or diverted, and GMV recognized at order time overstates real uptake |
| Credit repayment rate (embedded agri-finance) | Portfolio health | A rescheduled or rolled-over loan can be counted as current, hiding real default risk until one bad season hits everyone at once |
| Connectivity / reachability coverage | Addressable market | Reachable by SMS is not reachable with a working handset and airtime, and tower-based coverage maps overstate usable connectivity |
| Extension-advice adoption rate | Behavior change on the ground | An agent recording advice delivered is not a farmer changing a practice, and self-reported adoption is easy to inflate |
| Time to payout (output marketplaces, contract farming) | Cash-flow benefit to the farmer | A fast payout to a cooperative or aggregator is not a fast payout to the individual farmer; last-mile disbursement is where delay actually hurts |
| Women farmers reached, or any named underserved segment | Inclusion | Registered under a household account controlled by a male relative is not the same as reached, a known distortion in rural digital-inclusion metrics |
| Carbon credits issued or verified | Sustainability revenue | Issuance is not additionality; a credit can be issued under a registry's methodology and still not represent carbon that would not have been sequestered anyway |

## Reading

- **FAO's Voluntary Guidelines on the Responsible Governance of Tenure**, 2012, the reference for why land-based collateral and identity assumptions break down for smallholders, and what a more careful design looks like instead.
- **ISO 11783 (ISOBUS)**, the interoperability standard deciding whether your software can read a farm's own equipment data, regardless of the farmer's wishes.
- **The EU's plant-protection-products regulation**, Regulation (EC) No 1107/2009, a working example of how an input-approval regime gates an agri-marketplace's listings even outside the EU.
- **The OECD Seed Schemes**, an international seed-certification framework relevant to any marketplace selling seed across borders.
- **The Ethiopia Commodity Exchange**, established 2008, a real, working substitute for land-title collateral, built around graded, warehoused output rather than a paper deed.
- **M-Pesa**, launched in Kenya in 2007, the canonical mobile-money rail most smallholder-facing marketplaces and lenders in emerging markets are built on top of, not around.
- **Copernicus and the Sentinel satellites**, the EU's Earth-observation programme and a major open source of the remote-sensing data behind yield and weather products, worth knowing before licensing a commercial alternative.

**Conductor overlay:** this domain sharpens DISCOVER-3 (the workaround cost is the honest baseline, whether that is a market-town trip or an informal moneylender), DEFINE-7 (name the assumptions about smartphones, literacy, and land title explicitly, since the default case in this domain is the exception elsewhere), DESIGN-2 (integrations are the mobile-money rail and the equipment's own data standard, neither of which you control), and OPERATE-8 (the counter-metric to any yield or income claim is what the weather alone would have done).

**Templates this bends:** [problem-framing](../../templates/discovery/problem-framing.md) (the workaround a smallholder already uses becomes the comparison baseline), [integrations](../../templates/architecture/integrations.md) (mobile-money rails and equipment data standards as gatekept dependencies), [personas](../../templates/discovery/personas.md) (connectivity, literacy, and land-tenure realities as persona attributes, not footnotes), and [business-case](../../templates/planning/business-case.md) (a weather-adjusted baseline before any yield or income benefit is claimed).

**Filled in this repo:** [domain-agritech-business-case.md](../../examples/domain-agritech-business-case.md) fills the [business-case](../../templates/planning/business-case.md) template directly for this domain: a weather-adjusted yield-gap benefit row, a below-normal-rain sensitivity, and an options table with a costed do-nothing baseline, built the way question 5 above asks for. For the other bent templates, the nearest example is still outside agritech: the [Sahulat journey](../../examples/sahulat-journey.md) and its artifacts, a fictional mobile-money wallet in Pakistan reached mostly through USSD on feature phones through an agent network, is the closest structural cousin because the [mobile-money-wallets](mobile-money-wallets.md) card it uses shares this card's two hardest constraints: a trusted human intermediary (Sahulat's shopkeeper agent, this domain's extension agent or cooperative) who actually drives adoption, and a payment rail the product does not own. Read [sahulat-personas.md](../../examples/sahulat-personas.md) for how a feature-phone, low-literacy persona is written as a first-class attribute rather than an edge case, and [sahulat-problem-framing.md](../../examples/sahulat-problem-framing.md) for a workaround-cost baseline (the cash trip to an agent) built the same way question 1 above asks for. Sahulat is only near: it carries no weather variable, no land-tenure question, and no input-registration gatekeeper, the three facts that make agritech its own card rather than a relabelled mobile-money one.

**Worked example (ILLUSTRATIVE):** a slice of a [business-case](../../templates/planning/business-case.md) benefit row, weather-adjusted per question 5 above, in the style of [harbourgate-nfr.md](../../examples/harbourgate-nfr.md)'s numbered, sourced rows.

| Benefit claimed | Raw figure | Weather adjustment | Adjusted figure | Source |
|---|---|---|---|---|
| Maize yield uplift, pilot cohort, 2026 season | +34% vs. prior-season self-report (N1) | 2026 was a wetter-than-normal season regionally; a control group of 40 non-pilot farms in the same district, tracked by the same agronomist, saw +21% over the same period with no product access (N2) | +13 percentage points attributable to the product (N1 minus N2), not +34 | Field agronomist log, 2026 harvest; district rainfall index for the comparison window |

This is the pattern question 5 names: the raw +34% is what a good rainfall year alone would have produced credited to the app; only the gap against a same-season, same-district control group is a defensible product claim, and it is the smaller, less impressive number.
