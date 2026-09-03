---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/product-strategy.md", "templates/planning/vision.md", "templates/execution/risk-register.md"]
method: "knowledge/INDEX.md"
aliases: ["PESTLE scan", "pestle"]
---
# PESTLE scan

Based on the ideas of Francis J. Aguilar, whose ETPS scan in Scanning the Business Environment (1967) is the root of the widely used PESTLE variant (political, economic, social, technological, legal, environmental). Explained here in this repository's own words.

## What it is for

The world outside the product changes on its own schedule: a regulation gets an effective date, a model provider halves its price, a travel budget freezes. A PESTLE scan is a structured walk through six categories of external change with one purpose: find the changes that will touch this product in the next four quarters and give each one a response and an owner. It is not a research report. The "so what" column is the product; the other columns exist to keep it honest.

## Run it when

- At a strategy or vision refresh, to fill the "why now" and "what changed" lines with dated facts
- Before entering a new market or geography, where the legal and political rows are usually the whole story
- When a regulation, a platform policy, or a vendor's terms have surprised the team once already
- Twice a year, on a calendar, so the scan happens before the surprise rather than after

**Skip it when:** the horizon is shorter than a quarter. A scan is for changes that need a planned response; for a change landing next month, open the [risk register](../../templates/execution/risk-register.md) and write the row.

## Inputs you need first

- The users, markets, and geographies in scope, from the product strategy section 2
- The last scan, if one exists, so movement is visible
- The compliance owner's watch list, where the [regulated module](../../modules/regulated/README.md) applies
- Supplier and platform terms, from the integrations register

## The worksheet

<!-- One row per specific change, not per category. A category with nothing material gets one row saying so, with the date scanned, so the next reader knows it was looked at. Direction: helps / hurts / mixed. Likelihood: high, medium, low that the change lands within four quarters. Response: act (a roadmap or plan item with an owner), watch (a named signal and a re-check date), ignore (recorded so nobody re-raises it). -->

| Category | Specific change (dated, sourced) | Direction | Horizon (quarters) | Likelihood | So what for this product in the next four quarters | Response | Owner | Feeds |
|---|---|---|---|---|---|---|---|---|
| Political | | | | | | | | |
| Economic | | | | | | | | |
| Social | | | | | | | | |
| Technological | | | | | | | | |
| Legal | | | | | | | | |
| Environmental | | | | | | | | |

**Prompts per category.** Political: procurement rules, public budgets, trade and sanctions lists touching your users or vendors. Economic: interest rates, hiring or travel freezes, budget cycles. Social: work patterns, expectations about automation, trust in machine suggestions. Technological: model and infrastructure price curves, platform API changes, the tooling new entrants get for free. Legal: privacy, data residency, tax rules, employment law, accessibility mandates, each with its effective date. Environmental: reporting obligations, carbon accounting in your users' processes, physical risk to operations.

**Decision rule.** Every "act" row has an owner and lands in a named document within two weeks of the scan. Every "watch" row has a signal someone will actually see and a re-check date. A legal row with a known effective date inside four quarters is "act" by definition; it cannot be "watch". A scan with no "act" rows is either a stable half-year or an unfinished scan; say which.

## Reading the result

- **One or two act rows, mostly legal or technological.** Normal. Route them to the roadmap and the risk register and close the scan.
- **A legal row with an effective date and no roadmap item.** Fix this first; it is the single most expensive miss a scan can produce.
- **Every row is "watch".** The scan avoided decisions. Ask of each watch row: what would make us act, and when would we know?
- **Rows about the whole economy with no product-specific so what.** Cut them. A scan is judged by its so-what column, not its breadth.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot; every change below is fictional and dated to a fictional scan.

| Category | Change | Horizon | Likelihood | So what | Response |
|---|---|---|---|---|---|
| Legal | A proposed rule in one country Ledgerline's staff travel to would require digital receipts to carry a structured tax field from a stated date next year | 3 | High | Extraction must emit the field or every report from that country bounces at review | Act: roadmap item, compliance owner |
| Technological | Two model providers cut inference prices in the last two quarters; one changed its retention terms | 1 to 2 | High | Unit cost falls; the vendor-terms clause must be re-checked per provider | Act: re-review terms before Gate 5, engineering lead |
| Economic | A travel freeze is expected next quarter | 1 | Medium | Report volume drops, so the adoption metric needs a per-report denominator, not a count | Act: metric definition, PM |
| Social | Hybrid work shifts spend from travel to home-office items | 4 | Medium | The category-to-policy mapping needs categories the policy does not yet name | Watch: policy diffs each quarter, finance lead |
| Political | Nothing material this scan | | | | Recorded, dated |
| Environmental | The sustainability lead may ask for travel emissions per expense line | 4 or later | Low | A category tag, not a product | Watch: a second ask triggers a one-pager |

## The trap

The scan that is a news digest. Someone spends two days collecting headlines, each category gets five bullets, and the so-what column reads "monitor" all the way down. Six months later the legal change with an effective date in the scan lands with no roadmap item, and the postmortem finds it, dated, in the scan. The specific failure is the empty response column, and the specific fix is the rule above: a known effective date is "act", and "watch" needs a signal and a date. Judge the scan by the two rows that changed a plan, not by the forty that did not.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 1, the "what changed recently" line, and section 6 (key risks)
- [Vision](../../templates/planning/vision.md): section 3, why now, takes the dated shifts
- [Risk register](../../templates/execution/risk-register.md) and [assumptions register](../../templates/definition/assumptions-register.md): act and watch rows
- [Compliance impact assessment](../../templates/operate/compliance-impact-assessment.md): the legal rows
- PLANNING track; the [SWOT](swot-tows.md) external boxes draw from this scan
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
