# Porter's five forces

Based on the ideas of Michael E. Porter, from "How Competitive Forces Shape Strategy", Harvard Business Review (1979). Explained here in this repository's own words.

## What it is for

Profit in a market is squeezed by five pressures: rivalry among the players already there, the threat of new entrants, the threat of substitutes, the bargaining power of buyers, and the bargaining power of suppliers. Score them for your segment and the job you serve, not for the industry on a slide, and two things fall out. The two strongest forces tell you what the strategy must neutralize. And each force implies something specific for pricing and for the roadmap, which is where product managers usually stop reading Porter too early. This sheet scores the forces and makes you write the implication and the owner in the same row.

## Run it when

- Before a pricing or packaging decision, to know which force will discount your list price
- When a strategy names a segment and nobody has asked who holds the power there
- When a supplier (a platform, a model provider, a data source) changes terms and the team is surprised
- When leadership asks whether an internal tool could be sold, before the market is sized
- Every year, because the entrant force can go from weak to strong in one technology cycle

**Skip it when:** you have not chosen a segment. The forces differ by segment; scored for "the software market", every force lands at 3 and the sheet says nothing.

## Inputs you need first

- The segment and job, from the [product strategy](../../templates/planning/product-strategy.md) section 2 or the discovery document
- Competitive analysis, sections 3 to 5: the named rivals and the non-product alternatives
- Supplier facts: platform terms, model provider pricing, data licences, from the [integrations register](../../templates/architecture/integrations.md)
- Buyer concentration: how many customers make up most of the revenue, from finance

## The worksheet

<!-- Score 1 to 5 for the pressure the force puts on our margin in this segment: 1 weak, 3 moderate, 5 strong. The driving questions are prompts, not a checklist; answer with dated evidence. The two implication columns are mandatory for any force scored 4 or 5. -->

| Force | Driving questions | Score 1 to 5 | Evidence | Implication for pricing | Implication for roadmap | Owner |
|---|---|---|---|---|---|---|
| Rivalry among existing competitors | How many rivals, how alike, how fast do they match features, do they compete on price | | | | | |
| Threat of new entrants | What does entry cost, what do incumbents hold that entrants cannot, how fast could a new team ship a credible copy | | | | | |
| Threat of substitutes | What does the customer do instead (spreadsheet, bundled module, nothing), what does that cost them, when does it stop being good enough | | | | | |
| Bargaining power of buyers | How concentrated are buyers, how low are their switching costs, can they build it themselves, do they see prices transparently | | | | | |
| Bargaining power of suppliers | How many suppliers per component, what does switching cost, can a supplier move into our product | | | | | |

**Implication guide, when a force scores 4 or 5.** Rivalry: price drifts to parity, so the roadmap needs a dimension rivals cannot match and pricing needs a value metric they do not use. Entrants: build switching costs early and win distribution before the copy ships. Substitutes: price against the substitute's total cost, including the labour it hides, and beat it on the job rather than on features. Buyers: expect discounting, tier by delivered value, integrate deeply enough that leaving is a project. Suppliers: abstract the supplier behind an interface, keep a second source live, put pass-through clauses in contracts.

**Decision rule.** Rank the forces by score. The top two are the strategy's problem; each must have a named response in the roadmap or the pricing sheet within the period. A force at 4 or 5 with empty implication columns is an unfinished sheet, not an accepted risk.

## Reading the result

- **Substitutes or buyers lead.** A value problem: the product has not yet beaten the spreadsheet on the job. Feed the [value proposition canvas](value-proposition-canvas.md) before touching price.
- **Suppliers lead.** A dependency problem: a platform or model provider can take the margin. Feed the integrations register and the [build, buy, partner](build-buy-partner.md) sheet for that component.
- **Entrants or rivalry lead.** A defensibility problem: run the [Seven Powers audit](seven-powers-audit.md) and expect the honest answer to be "none yet".
- **Everything scores 3.** Segment not chosen; see Skip it when.

## ILLUSTRATIVE example

Invented. Ledgerline's leadership asked whether the internal expense copilot could be sold to other mid-market firms; the forces are scored for that segment, mid-market finance teams on a common finance system.

| Force | Score | Evidence (invented) | Pricing implication | Roadmap implication |
|---|---|---|---|---|
| Substitutes | 4 | Buyers already run a form plus email, and the finance system's module comes "free" with the licence | Price against reviewer hours per close, not per seat | Beat the bundled module on first-submission approval, the job, not on feature count |
| Suppliers | 4 | The finance system controls API access; two model providers with volatile terms | Pass-through clause for inference cost | Provider abstraction; a second finance system to keep leverage |
| New entrants | 4 | A small team can wrap a model and ship receipt drafting in a quarter | Do not price as if the product were rare | The policy mapping learned from corrections is the only switching cost on offer; build it first |
| Buyer power | 3 | Many buyers, but each compares against the bundled module's zero price | Tier by active filers | Deep policy-field integration |
| Rivalry | 3 | Several vendors, mostly competing on breadth | Room to hold list price for a year | Watch quarterly |

Top two: substitutes and suppliers. Reading: an unattractive market for a newcomer with no power. The productization business case has to show a pricing story framed on close time and a supplier abstraction, or recommend staying internal.

## The trap

Scoring the industry instead of the segment. Buyer power gets a low score because "there are thousands of mid-market firms", while the buyer that matters is the finance system's marketplace team, which decides whether those firms ever see the product. Or entrants score low because last year's sheet said so, in a year when a new model API made a credible copy a quarter's work. Score the forces for a named segment, on a dated sheet, and rescore the entrant row every time the underlying technology drops in price.

## Feeds

- [Competitive analysis](../../templates/discovery/competitive-analysis.md): section 5 (axes that can move the decision) and section 6 (so what)
- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 4 (competitive benchmark) and the section 2 failure mode accepted
- [Product strategy](../../templates/planning/product-strategy.md): section 1 (diagnosis) and section 6 (key risks)
- [Business case](../../templates/planning/business-case.md): the market-attractiveness paragraph under its options
- [Risk register](../../templates/execution/risk-register.md): every force at 4 or 5 without a funded response
- PLANNING track and DISCOVER, ahead of Gate 1
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
