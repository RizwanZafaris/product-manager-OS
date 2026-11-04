---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/architecture/solution-architecture.md", "templates/architecture/adr.md", "templates/definition/nfr.md"]
method: "knowledge/INDEX.md"
aliases: ["Green Software Assessment", "green-software-assessment"]
---
# Green Software Assessment

Based on the Software Carbon Intensity (SCI) specification from the Green Software Foundation, first published in 2021. Explained here in this repository's own words. The formula and the meaning of its four terms are the specification's; the boundary prompts, the decision table, the worked case and the trap are this repository's way of running it on a product.

## What it is for

Somebody asks what the product's carbon footprint is: a customer's procurement questionnaire, the sustainability lead, a board member. A total is the wrong number for a product team, because it rises with every customer won and so cannot tell a heavier design from a growing business. The SCI is a rate instead: emissions per functional unit, the one thing the product does for a customer, such as a document processed or an active user in a month. A rate moves when a design choice moves it, which is what makes it useful in a design review.

The specification also closes the cheapest exit. Offsets and market-based instruments, such as renewable energy certificates bought to cover consumption, do not reduce an SCI score. The score falls only when the software uses less energy, uses energy from a cleaner grid, or ties up less hardware. That is why this sheet sits beside the architecture set: the decisions that move the number are architecture and product decisions, mostly made before Gate 3.

## Run it when

- A customer's procurement questionnaire or tender asks for emissions per unit of service
- The [PESTLE scan](../strategy/pestle.md) environmental row has an act item: a reporting obligation, or a customer asking for its suppliers' figures
- Before Gate 3, while the choices that fix the energy profile are still open: region, model size, retention period, real time or batch
- An AI feature is about to move to a larger model, or a retention period is about to be extended "in case we need it"
- Once a year against last year's score per functional unit, so the trend is a fact and not a recollection

**Skip it when:** nobody inside or outside the company has asked for the number and no open design decision would change it, or what is wanted is the company's total footprint for a disclosure. A total for reporting is corporate greenhouse-gas accounting, owned by the sustainability or finance team under their own method; a per-unit score built here and pasted into a disclosure answers a different question and will be read as if it answered theirs.

## Inputs you need first

- Energy per component for one stated period: the cloud provider's energy or carbon reporting where it exists, otherwise average utilisation times rated power per instance type, from engineering
- Location-based grid carbon intensity for each region the software runs in, from a published grid-intensity source the team names and dates
- Embodied emissions per hardware type and its expected lifespan: a manufacturer's published product footprint where one exists, otherwise a named estimation dataset
- Volume of the functional unit over the same period, from the [metrics dictionary](../../templates/operate/metrics-dictionary.md)
- The open decisions from [solution architecture](../../templates/architecture/solution-architecture.md), the retention section of the [NFR](../../templates/definition/nfr.md), and, for AI features, the [eval spec](../../templates/ai/eval-spec.md)

## The worksheet

### Step 1: the formula and its four terms

**SCI = ((E × I) + M) per R**

| Term | What it is | Unit | Where the number comes from | Confidence (measured / estimated / assumed) |
|---|---|---|---|---|
| E | Energy consumed by the software inside the declared boundary, over the period | kWh | | |
| I | Location-based carbon intensity of the electricity, for the grid where the energy is consumed | grams CO2 equivalent per kWh | | |
| M | Embodied emissions: the share of the hardware's manufacturing and disposal emissions attributable to this software, over the period | grams CO2 equivalent | | |
| R | The functional unit the total is divided by | [per document, per user per month, per API call] | | |

**The embodied share, written out.** M = total embodied emissions of the hardware × (time this software reserves the hardware / the hardware's expected lifespan) × (resources this software reserves / the hardware's total resources). A server bought for this service alone, over a one-month period, carries one month of its lifespan; a server the service shares with three others of equal size carries a quarter of that.

### Step 2: the boundary

<!-- One row per component. "No data" is a reason to estimate and mark the row
     assumed, never a reason to exclude: the components nobody measures are the
     ones the score most needs, and an excluded row quietly flatters it. A row may
     be excluded only with a written reason a reviewer could disagree with. -->

| Component | In the boundary (yes / no) | E source | M source | Reason, if excluded |
|---|---|---|---|---|
| Application compute | | | | |
| Databases and storage, including backups | | | | |
| Network and data transfer | | | | |
| Model inference | | | | |
| Model training or fine-tuning, spread over the period it serves | | | | |
| Client devices, for the time they run the product | | | | |
| Build, test and deployment pipeline | | | | |
| Logging, monitoring and analytics | | | | |
| Idle and standby capacity | | | | |
| Third-party services called per unit | | | | |

### Step 3: the functional unit

<!-- R is something the product produces for a customer, and it stays fixed across
     every run you intend to compare. "Per server" is a unit of cost, not of value;
     "per active user" flatters a product whose heavy users do the most work. If R
     has to change, the old and new scores are not comparable, and the sheet says
     so in its header. -->

- Functional unit: [the unit, and why it is the thing customers pay for or use]
- Volume this period: [count, from the metrics dictionary]

### Step 4: the arithmetic

| Component | E (kWh) | I (g per kWh) | E × I (kg) | M (kg) | Total (kg) | Share of total | Confidence |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| **Sum** | | | | | | 100% | |

**SCI** = sum of totals / volume of R. State it with its unit and its period, and list the excluded components directly under it so nobody reads it without them.

### Step 5: the decisions that move it

<!-- One row per open decision. The "what it costs" column is mandatory: every
     reduction costs the user or the business something, and a row with that
     column empty has not been examined. Estimate each effect with the Step 4
     arithmetic, changing one input at a time. -->

| Decision | Term it moves | How to estimate the effect | What it costs the user or the business |
|---|---|---|---|
| Data retention: how long raw inputs and derived data are kept | E and M of storage, roughly in proportion to volume held | Volume held at steady state under the new period, divided by today's | Lost history; check the legal minimum in the NFR retention section first |
| Model size: a smaller or distilled model, or routing easy cases to one | E of inference, per request | Energy per request for each model, times the share of requests each would serve | Quality on the hard cases; the eval spec thresholds decide which cases may move |
| Batch instead of real time for work nobody waits for | M through higher utilisation, and I where work moves to cleaner hours | Hardware needed at the flattened peak, against today's | Latency the user sees; whether anyone actually waits for the result |
| Region: where the workload runs | I directly | Energy moved times the difference in grid intensity | Latency, data residency, price; a residency change reopens the privacy impact assessment |
| Payload and caching: work the product repeats or sends that nobody uses | E of network, compute and client devices | Bytes or calls removed per unit | Usually little; check freshness requirements |

## Reading the result

- **Compare rates, not totals.** An SCI that falls while the total rises is a business growing on a lighter design. An SCI that rises means some design got heavier per unit, whatever the total did.
- **One component above half the total.** That is the decision to examine first, before any row that is cheaper to talk about.
- **M large against E × I.** Hardware utilisation is the lever: idle capacity, oversized clusters, hardware replaced early. Cleaner electricity will not move this part of the score.
- **Most inputs marked assumed.** The score is an order of magnitude. It is good enough to rank the Step 5 decisions against each other and not good enough to claim a reduction of a few percent; publish it, if at all, with that label.

## ILLUSTRATIVE example

Invented. Driftwell is a fictional document-extraction API that reads scanned supplier invoices for small accounting firms. Every number below is ILLUSTRATIVE, including the grid intensities, the hardware footprints and the lifespans; none is a measurement of any real region, device or product. Period: one month. Functional unit: per 1,000 documents processed; volume 2,000,000 documents, so 2,000 units.

| Component | E (kWh) | I (g per kWh) | E × I (kg) | M (kg) | Total (kg) | Confidence |
|---|---|---|---|---|---|---|
| Inference, 4 dedicated GPU servers | 3,600 | 400 | 1,440.0 | 133.3 | 1,573.3 | E measured, M estimated |
| Application compute, 6 servers at half share | 900 | 400 | 360.0 | 75.0 | 435.0 | E measured, M estimated |
| Storage, page images kept 24 months | 1,200 | 400 | 480.0 | 90.0 | 570.0 | E estimated, M estimated |
| Network and data transfer | 150 | 400 | 60.0 | not estimated | 60.0 | E assumed |
| Build and test pipeline, shared runners | 80 | 400 | 32.0 | 4.0 | 36.0 | E estimated, M assumed |
| **Sum** | | | **2,372.0** | **302.3** | **2,674.3** | |

The inference M is 4 servers × 1,600 kg embodied each × (1 month / 48-month lifespan) × 1.0 share = 133.3 kg. The application M is 6 × 1,200 × (1 / 48) × 0.5 = 75.0 kg. **SCI = 2,674.3 kg / 2,000 = 1.34 kg per 1,000 documents**, excluding client devices (the firms' own scanners, outside the product) and network hardware [OPEN: embodied emissions for network equipment have no source yet; owner, platform engineering lead, before the next annual run].

| Decision | Change | Saving (kg per month) | Running total (kg) | SCI (kg per 1,000) | Cost |
|---|---|---|---|---|---|
| Baseline | | | 2,674.3 | 1.34 | |
| Retention | Page images kept 6 months instead of 24, extracted fields kept 7 years as now; storage held falls to a quarter, so E 1,200 to 300 kWh and M 90 to 22.5 kg | 360.0 + 67.5 = 427.5 | 2,246.8 | 1.12 | Firms lose the image after 6 months; contracts require 3, so allowed |
| Model routing | Small model on the 92% of pages it passes the eval thresholds for, at 40% of the large model's energy; handwritten pages stay on the large model. E = 3,600 × ((0.92 × 0.4) + 0.08) = 1,612.8 kWh | 1,987.2 × 0.4 = 794.9 | 1,451.9 | 0.73 | Two weeks of eval work; a second model to run and monitor |
| Batch | The 70% of documents uploaded as end-of-day batches move to an overnight window; the flattened peak needs 3 GPU servers, not 4, so inference M falls from 133.3 to 100.0 kg | 33.3 | 1,418.6 | 0.71 | Batch results arrive by 07:00, not within minutes; no firm in the batch group reads them before then |
| Region, not adopted | 60% of inference moved to a region at 120 g per kWh: 967.7 kWh × (400 minus 120) g | 271.0 | 1,147.6 | 0.57 | Breaks the residency term in 40% of contracts, and the rest need a privacy impact assessment; deferred |

The first three cut the SCI from 1.34 to 0.71 kg per 1,000 documents, about 47%, without touching a region. The released GPU server's idle energy is not counted in the batch row, a conservative omission. Notice where the saving came from: two of the three rows (retention and batch) were invisible in the cloud provider's dashboard, which reported compute energy only.

## The trap

Optimising the part that is measured. The cloud provider reports energy and carbon for compute, so the team cuts compute, reports the drop, and calls the product greener, while storage grows with an untouched retention period, the hardware sits idle at night, and the client and network rows were excluded for lack of data. The score on paper falls; the score with its boundary drawn honestly may not. The tell is in two places: a boundary table where every excluded row says "no data", and a decision list where every row touches a component marked measured. Fix it in Step 2: no exclusion for lack of data, only an estimate marked assumed, and at least one Step 5 row on a component the dashboard does not report. A related tell: a reduction claimed from a certificate purchase or a provider's renewable-matching claim. The specification does not let those reduce the score, so a reduction that rests on one has not happened.

## Feeds

- [Solution architecture](../../templates/architecture/solution-architecture.md): section 5 (what this commits us to), for the region, model and batch choices
- [ADR](../../templates/architecture/adr.md): one record per Step 5 decision taken, with the SCI before and after as its evidence
- [NFR](../../templates/definition/nfr.md): section 6 (data retention), where the retention decision lands as a stated period
- [Eval spec](../../templates/ai/eval-spec.md): the thresholds that decide which requests a smaller model may serve
- [Privacy impact assessment](../../templates/architecture/privacy-impact-assessment.md): reopened by any region change that moves personal data
- [PESTLE scan](../strategy/pestle.md): the environmental row, where a reporting obligation or a customer's request becomes an act item that this sheet answers
- [Tech debt assessment](tech-debt-assessment.md): idle and oversized capacity found here is often a compromise already carrying a cost
- DESIGN stage, feeds Gate 3
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
