# Wardley map

Based on the ideas of Simon Wardley, from his mapping practice published on his blog and in the open book Wardley Maps (2005 onward). Explained here in this repository's own words.

## What it is for

A map answers a question a roadmap cannot: for each component in the value chain, should you build it, buy it, rent it as a utility, or wait? Two axes do the work. The vertical axis is visibility to the user: the need at the top, the components that serve it beneath, down to storage and compute. The horizontal axis is evolution: genesis (novel, uncertain), custom-built (bespoke, expert-made), product (off the shelf, feature competition), commodity (standard, priced like a utility). Components move rightward over time whether you like it or not. Build on the left where you differentiate, buy on the right where you do not: that is the whole discipline, and the map makes each component's position an argument you can check instead of a feeling.

## Run it when

- Before a [build, buy, partner](build-buy-partner.md) decision on any component, so the evolution stage is on the table
- When the engineering budget is spread across components nobody can rank by user visibility
- When a component you built is now sold by three vendors as an API
- At a strategy refresh, to see which component is about to change stage

**Skip it when:** the product is a single feature on someone else's platform with two components. A map of two boxes is a sentence; write it in the [solution architecture](../../templates/architecture/solution-architecture.md) and move on.

## Inputs you need first

- The user need, in the user's words, from the discovery document or the [JTBD spec](../../templates/discovery/jtbd-spec.md)
- The component inventory: the system design or solution architecture, or a whiteboard hour with the engineering lead
- Vendor facts: which components are available as products or utilities, with dates checked
- Current spend per component, people and licences, from the engineering lead

## The worksheet

### Part 1: the anchor

| Field | Answer |
|---|---|
| User | [who, precisely] |
| Need | [the outcome they want, in their words] |

### Part 2: the components

<!-- Stage cues. 1 genesis: nobody agrees what it is, few instances, high failure rate. 2 custom: bespoke builds, experts required, no two alike. 3 product: several vendors compete on features, buyers compare. 4 commodity: standardized, price-competed, often an API you meter. Visibility rank 1 is closest to the user. -->

| Component | Serves (parent component or the need) | Visibility rank | Stage 1 to 4 | Evidence for the stage (vendor count, dated) | Movement (stable / shifting right within four quarters) | Play | Owner |
|---|---|---|---|---|---|---|---|
| | | | | | | [build / buy / rent / wait] | |

**Decision rule.** Build only at stage 1 or 2, and only when the component sits within two visibility ranks of the need and is part of how you win. Buy at stage 3. Rent at stage 4 and never build there. Wait when the component is shifting right within four quarters and the interim spend is small: pay for the stopgap, do not build what is about to become a utility. A component you built that now sits at stage 3 or 4 is a cost centre with a story; plan its replacement.

### Part 3: the sketch

<!-- Optional. Rank down the page, stage across it. Two rows shown. -->

```
                genesis     custom          product       commodity
need            [user need]
rank 1                      [policy line]
rank 2                                      [draft UI]
rank 3                                                    [extraction API]
```

## Reading the result

- **Most spend sits at stage 3 or 4.** The team is building what it could buy. Move the budget left, to the stage 1 and 2 components closest to the need.
- **Nothing sits at stage 1 or 2.** The product has no component of its own; the strategy's "how we win" line needs a rewrite or a plan.
- **A left-side component is shifting right fast.** Time-box the build, design for replacement, and record the switch trigger in the [decision log](../../templates/execution/decision-log.md).
- **Engineering and product disagree on a stage.** Good; that argument is the map's product. Settle it with vendor evidence, not seniority.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. User: a filer who travels a few times a quarter. Need: the report accepted the first time.

| Component | Rank | Stage | Evidence (invented) | Movement | Play |
|---|---|---|---|---|---|
| Category suggestion with the policy line shown | 1 | 2 custom | No vendor shows the policy line behind a draft; two offer post-hoc audit | Stable | Build; this is the differentiator |
| Draft-and-edit UI | 2 | 3 product | Form frameworks and component libraries abound | Stable | Buy the framework, build only the policy prompts |
| Receipt extraction | 3 | 4 commodity | Four metered APIs checked this quarter | Stable | Rent; do not extend the in-house parser |
| Category-to-policy mapping, learned from corrections | 2 | 2 custom | Specific to our policy; no vendor learns from reviewer corrections | Stable | Build; small, and it feeds rank 1 |
| Model inference | 4 | 4 commodity | Multiple providers, prices falling | Shifting | Rent behind an abstraction; wait on fine-tuning |
| Correction log and audit storage | 5 | 4 commodity | Managed databases | Stable | Rent |

Reading: two builds, both within two ranks of the need. The in-house receipt parser an engineer started before discovery is a stage 4 component; it stops at its current state and the extraction budget goes to a metered API, with the vendor-terms clause as the knock-out.

## The trap

Mapping by authorship. A component the team wrote gets placed at "custom" because it feels bespoke, while the market has already made it a commodity, and the map then defends a cost centre with a diagram. The tell is a stage 2 entry whose evidence column says "we built it" instead of a vendor count with a date. The stage is a fact about the market, not about your codebase. Fill the evidence column before the stage column, and have someone outside the team that built the component score it.

## Feeds

- [Build, buy, partner](build-buy-partner.md): the stage and movement columns are its first inputs
- [Solution architecture](../../templates/architecture/solution-architecture.md) and the [integrations register](../../templates/architecture/integrations.md): every buy or rent is a row
- [Product strategy](../../templates/planning/product-strategy.md): section 4 (sequencing), the retirements and time-boxed builds
- [Roadmap](../../templates/planning/roadmap.md): the Later column takes the wait rows with their trigger
- DESIGN stage, feeds Gate 3: architecture and risks reviewed
- Method background: [knowledge index](../../knowledge/INDEX.md), Wardley Mapping entry
