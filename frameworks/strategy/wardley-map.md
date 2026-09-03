---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["frameworks/strategy/build-buy-partner.md", "templates/architecture/solution-architecture.md", "templates/architecture/integrations.md"]
method: "knowledge/INDEX.md"
aliases: ["Wardley map", "wardley-map"]
---
# Wardley map

Based on the ideas of Simon Wardley, from his mapping practice, developed from 2005 and published on his blog and in the open book Wardley Maps (2016 onward). Explained here in this repository's own words.

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
- **Every Movement cell says stable.** Nobody checked. Components do not hold still, so a column of stable means the vendor lists were not re-read this quarter; go and read them before the map is used to move money.
- **The Play column repeats one word.** All build is a team defending its scope. All rent is a team with no product of its own. Either way the map was filled to confirm a decision already taken.

## Climatic patterns: what the map does whether you act or not

Climate is the part of the landscape you do not get a vote on. These patterns are Simon Wardley's, from the same mapping practice (2005 onward), put here in our own words. They matter because they are what fills the Movement column in Part 2, and because they are the reason a map expires.

| Pattern | What it says | What it does to your map | The tell you ignored it |
|---|---|---|---|
| Everything evolves rightward | Competition, plus supply and demand, pushes every component toward the commodity end. Nothing drifts back left on its own. | Every row has a direction, so "stable" is a dated claim about the market, not a property of the component. | The Movement column is uniform and no vendor list carries a date. |
| Characteristics change as a thing industrializes | The left is uncertain, changing, and measured by what you learned. The right is defined, stable, priced, and measured by unit cost and volume. | A component that crossed into stage 3 or 4 needs different people, metrics, and cadence than the ones that built it at stage 2. | One cadence and one set of metrics across the whole chain, so the commodity work starves the genesis work or the reverse. |
| Efficiency enables innovation | When a component gets cheap and standard, things that were not economic on top of it become economic, and demand for the component rises rather than falls. | A commodity row is not the end of the story, it is the floor of the next map. Ask what you could build now that was priced out last year. | A rented utility is booked purely as a saving, and nothing new gets proposed above it. |
| You have no choice over evolution | The market sets the stage. Your only choice is how you respond to it. | The Stage column is evidence about the world; the Play column is the only place your preference belongs. | An argument about whether a component *should* be a commodity. |
| Past success breeds inertia | The more the current model earns, the harder the organization resists changing it, and the resistance is usually rational for the person voicing it. | Every retirement and every time-boxed build needs a named owner of the inertia: the sunk asset, the scarce skill, the vendor relationship, the revenue line, the reputation. | The map is agreed, nothing moves, and no document says who did not want it to. |

Fill one row for every component whose Movement column says shifting.

<!-- Inertia is somebody's real interest, not a bad attitude. Write it as an interest ("the team we would ask to retire the parser is the team that wrote it", "support revenue on the old integration") and the mitigation becomes a conversation with a named person instead of a change-management slide. -->

| Component shifting right | Pattern driving it | Evidence, dated | Cost of acting a year late | Inertia we will meet, and whose |
|---|---|---|---|---|
| | | | | |

## Doctrine: the practices you adopt whatever the map says

Doctrine is Wardley's term for the practices that pay off on any map, which is what separates them from plays: they are not re-argued each quarter. His second claim is the useful one, that adoption is roughly ordered, because the later practices do not hold without the earlier ones. A team that skips ahead buys the vocabulary and not the practice. Score each row 0 not practiced, 1 practiced by some people in some weeks, 2 practiced by default.

| Phase | Practice, in our words | You have it when | The cheap counterfeit | Score |
|---|---|---|---|---|
| 1. Stop the self-inflicted damage | Know who the user is and what they need, in their words | The need in Part 1 came from a transcript, not a workshop | A persona document with no source | |
| 1 | Use one shared language for the system | Two teams arguing can point at the same component and agree which one it is | A glossary nobody opens; four names for one service | |
| 1 | Remove duplication and bias | Somebody has looked for the same component built more than once under different names, and has the list | An architecture diagram that shows intent rather than what runs | |
| 1 | Use the method the stage earns | Stage 1 components get probes; stage 4 components get contracts and metrics | One planning ritual applied to every row | |
| 1 | Think small: small teams, small components, boundaries you can name | Each component in Part 2 has one owner who can describe its edge | A team whose scope is a department name | |
| 2. Become context aware | Map before you plan, then attack the map's own assumptions | The stage column has evidence in it before the plan is written | A map produced after the budget was set, to justify it | |
| 2 | Manage inertia openly | The inertia column above is filled with interests and names | "Change resistance" as a line in a risk register | |
| 2 | Separate aptitude from attitude | You staff by skill and by stage-appropriate temperament, and you say so out loud | Moving the person who built the genesis component onto its utility operation and calling it continuity | |
| 2 | Be transparent enough to be contested | An engineer outside the owning team can and does move a component's stage | A map only its author presents | |
| 3. Get better output for less | Optimize the flow of the whole chain, not one team's throughput | You can name the slowest handoff between two components | Per-team velocity, rising, with delivery unchanged | |
| 3 | Effectiveness before efficiency | You have killed at least one efficient build of something you should have rented | A tuned in-house component nobody needed | |
| 3 | Push decisions to whoever holds the context | The owner column in Part 2 can commit spend inside a known limit | An owner who can be blamed but cannot decide | |
| 4. Evolve continuously | There is no core: any component can be moved, retired, or handed to a vendor, including the one the company's identity is built on | The word "core" never appears as a reason on its own | "Strategic" used as an exemption from the decision rule | |
| 4 | Design for constant evolution | Every stage 1 or 2 build has a seam, a switch trigger, and a written replacement plan | A build with a review date and no trigger | |

**Decision rule.** Any phase 1 row scoring 0 gets fixed before this map is used to move budget or people. A map is only as honest as the practices that produced it, and a team without a shared language will faithfully encode its confusion into a diagram and then defend the diagram. Phase 3 and 4 gaps do not block the map; they go on the [product operating model assessment](../assessment/product-operating-model-assessment.md) as named weaknesses with dates.

## Gameplay: the plays the map makes available

Gameplay is the opposite of doctrine, and this is the part practitioners come for. Each play below is context-specific, available only when the map shows a particular condition, and each one has a counter, because the other players move too. They are not best practices, and a list of them is not a strategy. Two rules keep this section from becoming a menu: never run a play whose counter you cannot name, and never run one when its map condition is absent, since the play that wins on one map is the one that loses on another.

| Play, in our words | Map condition that makes it available | What it costs you | Counter-play to expect | The tell it was copied, not chosen |
|---|---|---|---|---|
| Open the component: publish the code, the spec, or the data | A stage 2 component you do not differentiate on, sitting underneath one you do | Maintenance, and the option of ever selling it | A better-resourced player forks it and out-distributes you; the standard settles where you did not choose | You opened the component you actually win on, because opening things looks generous |
| Land grab above a new commodity | Efficiency-enables-innovation just fired: something below you reached stage 4 and made a higher-order component economic | Left-side spend with no proof of demand yet | A fast follower with distribution enters at stage 3 once you have proven the need | No dated evidence that the component underneath actually moved |
| Fast follower | Someone else is paying for genesis in a space where your distribution or operations are genuinely better | The vocabulary and the ecosystem, both of which the first mover keeps | The first mover locks a standard or an ecosystem while you wait | Declared in a space where you have no distribution advantage either |
| Industrialize what your ecosystem proves | You run a utility that others build on, and you can see what they build | Trust, which is spent once and slowly | The ecosystem reads the pattern and builds somewhere else | No written rule about what you will not take from them |
| Buy time with a stopgap, then switch | Movement says shifting right inside four quarters and the interim spend is small | An interim thing to run and later unpick | Mostly internal: the stopgap quietly becomes the product | No dated switch trigger and no owner for it |
| Dispose of the liability | You own a component the market now sells at stage 3 or 4 | A political fight and a migration | Inertia, from the people who built it and are asked to end it | A retirement with a slide, no owner, and no date |
| Second-source a utility you depend on | A stage 4 component within two visibility ranks of the need, one vendor | An abstraction layer somebody has to keep honest | The vendor bundles or prices so the second source stops being worth running | An abstraction only one implementation ever ran through |
| Push your interface as the shared standard | You sit at stage 3 with an interface several buyers already integrate against | Your own freedom to change that interface | A larger player publishes a different one and yours becomes the legacy adapter | A standard proposed for an interface with exactly one implementer |
| Cross-subsidize: fund the left from the right | A stage 3 or 4 line with real margin, and a stage 1 or 2 bet nobody will fund | Resentment from the line paying, every planning round | A rival prices your margin component toward a utility and the subsidy evaporates | The transfer is invisible in the budget, so it dies in the first bad quarter |

Some plays are deception plays: talking down a rival's roadmap, distorting a signal, bundling to obscure a price. This repository does not stock them, and you will still meet them. The map is how you notice one being run on you, because it forces the question of which component the noise is about and what stage that component is actually at.

For each play you intend to run, fill one row and put it in the [decision log](../../templates/execution/decision-log.md).

| Play chosen | Component and rank it acts on | Map condition, with dated evidence | Counter we expect, and from whom | Abandon trigger, with date | Owner |
|---|---|---|---|---|---|
| | | | | | |

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. All figures ILLUSTRATIVE. User: a filer who travels a few times a quarter. Need: the report accepted the first time.

| Component | Rank | Stage | Evidence (invented) | Movement | Play |
|---|---|---|---|---|---|
| Category suggestion with the policy line shown | 1 | 2 custom | No vendor shows the policy line behind a draft; two offer post-hoc audit | Stable | Build; this is the differentiator |
| Draft-and-edit UI | 2 | 3 product | Form frameworks and component libraries abound | Stable | Buy the framework, build only the policy prompts |
| Receipt extraction | 3 | 4 commodity | Four metered APIs checked this quarter | Stable | Rent; do not extend the in-house parser |
| Category-to-policy mapping, learned from corrections | 2 | 2 custom | Specific to our policy; no vendor learns from reviewer corrections | Stable | Build; small, and it feeds rank 1 |
| Model inference | 4 | 4 commodity | Multiple providers, prices falling | Shifting | Rent behind an abstraction; wait on fine-tuning |
| Correction log and audit storage | 5 | 4 commodity | Managed databases | Stable | Rent |

Reading: two builds, both within two ranks of the need. The in-house receipt parser an engineer started before discovery is a stage 4 component; it stops at its current state and the extraction budget goes to a metered API, with the vendor-terms clause as the knock-out.

Climate, invented: the shifting row is model inference, driven by everything-evolves-rightward, with efficiency-enables-innovation directly behind it. Cheap inference is what makes the rank 1 component (a suggestion that shows the policy line) economic at all, so the saving is the budget for that build rather than a cut. Inertia named: the engineer who wrote the parser is the engineer the team would ask to retire it, so the retirement is owned by the engineering lead, not by that engineer.

Doctrine, invented: phase 1 all scores 2 except duplication, at 1, because nobody has yet checked whether the correction log and the audit store are the same component twice. That gets checked before the extraction budget moves.

Play, invented: dispose of the liability, acting on the receipt-extraction row. Condition: four metered APIs checked this quarter. Counter expected: inertia from inside, not from a rival. Abandon trigger: if the metered price for the expected monthly volume exceeds the parser's fully loaded run cost at the next quarterly review, the play stops and the row is re-scored. Owner: engineering lead.

## The decision it feeds

For every component in the value chain, one of four rulings, with an owner and a dated piece of vendor evidence behind it: build, buy, rent, or wait. Two further decisions fall out of the same table. Where the engineering budget moves this period, because spend sitting at stage 3 or 4 has already answered that question. And which play the team runs next, with its counter named and its abandon trigger dated, since a play missing either of those is a preference. The ruling nobody schedules is the one the map is best at forcing: retiring a component you built that the market now sells at stage 3 or 4, which stops being a loyalty question once the stage column carries evidence.

## The trap

Mapping by authorship. A component the team wrote gets placed at "custom" because it feels bespoke, while the market has already made it a commodity, and the map then defends a cost centre with a diagram. The tell is a stage 2 entry whose evidence column says "we built it" instead of a vendor count with a date. The stage is a fact about the market, not about your codebase. Fill the evidence column before the stage column, and have someone outside the team that built the component score it.

## Re-run trigger

**Re-run when any component's stage changes, and treat each of these as that change: a new vendor list for something you build, a rented component moving to metered pricing or being bundled into something else, a time-boxed build reaching its box, a vendor term or availability change on any rented row, a reorganization or budget cycle that reassigns owners. Absent any of those, re-run at every strategy refresh and before any build, buy, rent, or wait decision larger than the smallest thing you would ship without a map. A map older than two quarters is a historical document: read it for what moved, never for what to do next.**

The map is a snapshot of a landscape that evolves whether anyone looks at it or not, which is the whole content of the climatic patterns above. A map with no re-run date stops being a diagnosis and becomes an argument-ender, and the first thing it ends is the argument that the market has moved.

## Feeds

- [Build, buy, partner](build-buy-partner.md): the stage and movement columns are its first inputs
- [Solution architecture](../../templates/architecture/solution-architecture.md) and the [integrations register](../../templates/architecture/integrations.md): every buy or rent is a row
- [Product strategy](../../templates/planning/product-strategy.md): section 4 (sequencing), the retirements and time-boxed builds
- [Roadmap](../../templates/planning/roadmap.md): the Later column takes the wait rows with their trigger
- [Product operating model assessment](../assessment/product-operating-model-assessment.md): the doctrine scores are its inputs on team boundaries, decision rights, and learning, and phase 3 or 4 gaps land there rather than blocking the map
- [Strategy kernel](strategy-kernel.md): the map is the diagnosis, and a chosen play is a candidate guiding policy rather than a goal
- [Playing to Win](playing-to-win.md): run the "what would have to be true" test on the map condition behind a play, before the play is funded
- [Premortem worksheet](../execution/premortem-worksheet.md): run it on the chosen play with the counter-play written in as the first failure mode
- [Decision log](../../templates/execution/decision-log.md) and [ADR](../../templates/architecture/adr.md): one entry per play, carrying its map condition, its counter, and its abandon trigger
- [Now, Next, Later](../prioritization/now-next-later.md): wait rows and abandon triggers belong in Later with their trigger, never in Now with a date
- [Cynefin](../systems/cynefin.md): stage and domain are two readings of the same uncertainty, and a stage 1 component cannot honestly carry a dated commitment
- DESIGN stage, feeds Gate 3: architecture and risks reviewed
- Method background: [knowledge index](../../knowledge/INDEX.md), Wardley Mapping entry
