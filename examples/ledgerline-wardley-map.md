# Wardley map: Ledgerline Expense Copilot

Fills [frameworks/strategy/wardley-map.md](../frameworks/strategy/wardley-map.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, vendors, counts, scores and costs are fictional and must not be treated as benchmarks.

**Owner:** Priya Nair, Engineering Lead, with Maya Chen, Product Manager · **Date:** 2026-12-22 · **Status:** Draft map for the build, buy, partner sheet after D6

The source data is the [journey data sheet](ledgerline-journey.md) and the supplementary [coverage sheet](ledgerline-coverage-sheet.md). The new vendor counts and doctrine scores come from LC13.

## What it is for

This map answers the build, buy, partner question for the Ledgerline add-on after D6 changed the value metric from plan seats to drafted reports.

The chain starts with the customer's need for a drafted expense line that shows the account's own policy line. It then separates the components that Ledgerline should build from the components it should rent or retire:

- Build the policy-matched draft because the account's own policy line beside the draft is the differentiating experience.
- Build a small drafted-report counter because the usage meter is the new value metric and ADR-008 proposes a product-side counter billed in arrears.
- Rent receipt extraction from metered APIs because three document-extraction APIs were checked and all are metered.
- Ask procurement for a second source through DEP2 because the extraction utility is rented and vendor concentration remains a dependency.
- Dispose of the add-on's seat entitlement after the 12-month holds end, because seat pricing was killed by D6 and the 73 paid accounts hold that price for 12 months under N93.
- Name the billing team that built the $15,000 seat meter as the inertia, rather than treating the retirement as an abstract change-management issue.

## Run it when

- Before the build, buy, partner sheet for the drafted-report meter, as required on 2026-12-22.
- When D6 changes the value metric from plan seats to drafted reports.
- When deciding whether extraction should remain an in-house capability or become a rented utility.
- When planning the retirement of seat entitlement after the 12-month holds end.
- When DEP2's volume re-quote or vendor availability changes the extraction decision.

**Skip it when:** the question is only whether an existing billing integration can be wired to a single feature. This map is needed here because the value chain contains a differentiating policy match, a new usage meter, a rented extraction utility, and a legacy seat entitlement.

## Inputs you need first

- **User need:** a filer gets a drafted line item with the matched policy line from the account's own policy, from LEDGERLINE-S2 and the customer-policy evidence in LC13.
- **Component inventory:** the policy-matched draft, the drafted-report counter, receipt extraction and seat entitlement.
- **Vendor facts:** three document-extraction APIs checked on 2026-12-18, all metered; three metered-billing vendors checked on 2026-12-18.
- **Current spend:** the seat meter used 1.5 person-months and $15,000, and that work is not reused by the usage model, per N86. The drafted-report meter needs 1 person-month and $10,000, per N87.
- **Decision context:** D6 killed the per-seat price on 2026-12-21. ADR-007 records the existing seat-based entitlement and charge. ADR-008, proposed on 2026-12-22, proposes the drafted-report meter.
- **Open dependency:** DEP2 is the model vendor volume re-quote at customer scale. DEP4 is the usage meter needed by 2027-01-08.

## The worksheet

### Part 1: the anchor

| Field | Answer |
|---|---|
| User | A filer at a customer account using the Ledgerline Expenses add-on |
| Need | Photograph or forward a receipt and get a drafted line item with the matched policy line from the user's own company policy |
| Source | LEDGERLINE-S2, LC13, N65 |

### Part 2: the components

| Component | Serves (parent component or the need) | Visibility rank | Stage 1 to 4 | Evidence for the stage (vendor count, dated) | Movement (stable / shifting right within four quarters) | Play | Owner |
|---|---|---:|---:|---|---|---|---|
| Policy-matched draft | The user's need | 1 | 2, custom | No Business-plan rival shows the account's own policy line beside a draft, based on EV-C02 and EV-C03; checked for this map on 2026-12-22 | Stable for this map; re-score if the vendor landscape changes | Build | Priya Nair |
| Drafted-report counter | Policy-matched draft and billing charge | 2 | 2, custom | ADR-008 proposes a product-side drafted-report counter; no vendor count is recorded in LC13; the component is specific to the new value metric. The stage 2 rating is a placeholder pending a vendor scan of product-side usage-metering options, and that scan is an open dependency of this map | Shifting right as usage metering becomes a standard billing capability | Build | Priya Nair |
| Seat entitlement | Existing add-on charge and entitlement | 2 | 3, product | Three metered-billing vendors checked on 2026-12-18; the stage 3 reading is Priya Nair's judgement drawn from that LC13 vendor count. The stage 3 reading rests on the billing and metering infrastructure that computes the seat charge, not on the entitlement logic itself, which is Ledgerline's own legacy code sitting in the charge path and is a disposition candidate alongside the billing work | Shifting right within four quarters, with retirement after the 12-month holds end | Dispose of the liability | Billing team |
| Receipt extraction | Policy-matched draft | 3 | 4, commodity | Three document-extraction APIs checked on 2026-12-18, all metered | Stable for this map, with DEP2 as the second-source question | Rent | Priya Nair with procurement |
| Billing-system invoice run | Drafted-report counter | 3 | 3, product | The proposed counter posts a monthly count into the billing system's invoice run; three metered-billing vendors checked on 2026-12-18 | Shifting right as usage billing becomes more standardized | Buy the billing capability, build the product counter | Billing lead with Priya Nair |

**Decision rule applied.**

- The policy-matched draft is stage 2, within one visibility rank of the need, and is part of how Ledgerline wins. Build it.
- The drafted-report counter is stage 2, within two visibility ranks of the need, and is required by the new value metric. Build it. The stage 2 rating is a placeholder pending a vendor scan of product-side usage-metering options, which is an open dependency.
- Receipt extraction is stage 4. Rent it and do not extend an in-house parser.
- Seat entitlement is stage 3 on the strength of the metered-billing market that supports the charge, and the entitlement logic inside it is legacy internal code rather than a purchased product; D6 has invalidated its value metric. Dispose of the liability after the N93 holds end.
- The billing-system invoice run is not the differentiating component. Use the existing billing capability while building the small product-side counter.

### Part 3: the sketch

```text
                         genesis       custom             product             commodity
need                     [drafted line with the account's policy line]

rank 1                                  [policy-matched draft]

rank 2                                  [drafted-report counter] [seat entitlement]

rank 3                                                    [billing invoice run] [receipt extraction]
```

The map's key movement is from seat entitlement to drafted-report usage. D6 changed the value metric. The product-side counter is the smallest new component that lets the product follow that metric without rebuilding the rented extraction utility.

## Reading the result

- **Most spend sits at stage 3 or 4:** the $15,000 seat-metering build is now a liability because the value metric it serves was killed by D6. Receipt extraction belongs at stage 4 and should be rented.
- **Stage 2 remains close to the need:** the policy-matched draft is the differentiating component. The drafted-report counter is also close to the need because it makes the new usage value visible and billable, though its stage 2 rating is a placeholder pending a vendor scan.
- **A left-side component is shifting right:** the drafted-report counter is a small custom component with a replacement seam at the billing-system interface. The switch trigger is D6's change of value metric, already fired on 2026-12-21.
- **The seat entitlement row is a retirement decision:** the billing team built the $15,000 meter and has a legitimate interest in preserving that work. The map therefore names the team and the 12-month hold as part of the plan.
- **DEP2 remains material:** three extraction APIs were checked, but the customer-scale re-quote is still open. The rented row must not be treated as settled until procurement answers the volume question.

## Climatic patterns: what the map does whether you act or not

| Pattern | What it says | What it does to your map | The tell you ignored it |
|---|---|---|---|
| Everything evolves rightward | Competition, supply and demand push components toward the commodity end. | The policy-matched draft may attract product competition, the usage meter may become a billing utility, and extraction is already commodity. | Treating the stage 2 draft or the stage 3 seat entitlement as permanently custom without checking the market. |
| Characteristics change as a thing industrializes | Uncertain components need learning, while standardized components need contracts, metrics and volume management. | The policy match needs product and engineering learning. Extraction needs API contracts, cost monitoring and a second-source decision. | Applying the same development method and metrics to policy matching and metered extraction. |
| Efficiency enables innovation | Cheap standardized components enable new higher-order components. | Rented extraction creates room to build the policy-matched draft and the usage experience above it. | Treating the extraction saving only as a budget cut instead of funding the higher-order draft. |
| You have no choice over evolution | The market sets the stage; the response is the strategic choice. | The stage 4 extraction row is rented even though Ledgerline previously built related capability. The stage 3 seat entitlement is retired after its hold. | Calling the seat meter strategic merely because Ledgerline paid to build it. |
| Past success breeds inertia | The current model creates rational resistance to change. | The billing team that built the $15,000 seat meter is named as the inertia owner. The mitigation is a transition from seat entitlement to the drafted-report counter after N93. | Recording only "billing resistance" without naming the team whose work is being retired. |

Fill one row for every component whose Movement column says shifting.

| Component shifting right | Pattern driving it | Evidence, dated | Cost of acting a year late | Inertia we will meet, and whose |
|---|---|---|---|---|
| Drafted-report counter | Everything evolves rightward, and characteristics change as the component industrializes | ADR-008 proposes a product-side counter on 2026-12-22; the new value metric is drafted reports after D6 on 2026-12-21 | The add-on remains tied to the seat metric that D6 killed, while the 73 paid accounts remain on the 12-month hold | The billing team may prefer the existing seat entitlement because it built the meter using 1.5 person-months and $15,000, N86 |
| Seat entitlement | Everything evolves rightward, and past success breeds inertia | Three metered-billing vendors checked on 2026-12-18; N93 holds the 73 paid accounts at $6 per seat for 12 months | The $15,000 seat-metering investment remains in the charge path after the value metric has changed, and the add-on cannot move cleanly to drafted-report billing | The billing team that built the seat meter, with the sunk 1.5 person-months and $15,000, N86 |
| Billing-system invoice run | Characteristics change as a thing industrializes | Three metered-billing vendors checked on 2026-12-18; ADR-008 proposes monthly drafted-report billing in arrears | The product counter has no stable billing seam for EXP-2, which DEP4 must deliver by 2027-01-08 | The billing lead, whose existing integration is organized around seat entitlement rather than drafted-report usage |

## Doctrine: the practices you adopt whatever the map says

Doctrine is applied here as Wardley's term for practices that should hold across maps. LC13 scores only the phase 1 rows for this map. No phase 1 row scores 0, so the map can be used to move the drafted-report meter and extraction spend. Later-phase doctrine is not scored in LC13 and is not treated as evidence of practice.

| Phase | Practice, in our words | You have it when | The cheap counterfeit | Score |
|---|---|---|---|---:|
| 1. Stop the self-inflicted damage | Know who the user is and what they need, in their words | The need is anchored to LEDGERLINE-S2 and the customer's policy line | A persona document with no source | 1 |
| 1 | Use one shared language for the system | The policy-matched draft, seat entitlement and drafted-report counter are named consistently across the map and ADRs | A glossary nobody opens | 2 |
| 1 | Remove duplication and bias | The map identifies that seat entitlement and the proposed usage meter both compute entitlement | An architecture diagram that shows intent rather than what runs | 1 |
| 1 | Use the method the stage earns | Stage 2 components are built with explicit seams, while stage 4 extraction is rented and metered | One planning ritual for every row | 2 |
| 1 | Think small: small teams, small components, boundaries you can name | Each map row has a named owner and the drafted-report counter has a boundary at the billing invoice interface | A team whose scope is a department name | 2 |
| 2. Become context aware | Map before you plan, then attack the map's own assumptions | The vendor counts and stage evidence are recorded before the build, buy, partner decision | A map produced after the budget was set | Not scored in LC13 |
| 2 | Manage inertia openly | The billing team's interest in preserving the seat meter is named | "Change resistance" in a risk register | Not scored in LC13 |
| 2 | Separate aptitude from attitude | Product and engineering skills are matched to the policy draft, while billing operates the invoice seam | Moving the seat-meter author into utility operations without a plan | Not scored in LC13 |
| 2 | Be transparent enough to be contested | An engineer outside the billing team can challenge the stage evidence and the retirement plan | A map only its author presents | Not scored in LC13 |
| 3. Get better output for less | Optimize the flow of the whole chain, not one team's throughput | Extraction, policy matching, counter and billing are read as one value chain | Per-team velocity with delivery unchanged | Not scored in LC13 |
| 3 | Effectiveness before efficiency | The team stops extending seat metering and funds the value metric that D6 selected | A tuned in-house component nobody needs | Not scored in LC13 |
| 3 | Push decisions to whoever holds the context | Priya Nair owns the component boundary and Maya Chen owns the product decision | An owner who can be blamed but cannot decide | Not scored in LC13 |
| 4. Evolve continuously | Any component can be moved, retired or handed to a vendor | Seat entitlement is eligible for retirement despite the $15,000 build | "Core" used as an exemption | Not scored in LC13 |
| 4 | Design for constant evolution | The drafted-report counter has a billing seam and D6 is its switch trigger | A build with only a review date | Not scored in LC13 |

**Decision rule.** No phase 1 row scores 0. The map can therefore be used to move budget toward the policy-matched draft and drafted-report counter, and away from extending seat entitlement or receipt extraction. Phase 2 to 4 gaps are unscored rather than silently treated as complete.

## Gameplay: the plays the map makes available

| Play, in our words | Map condition that makes it available | What it costs you | Counter-play to expect | The tell it was copied, not chosen |
|---|---|---|---|---|
| Open the component: publish the code, the spec, or the data | A stage 2 component sits below a component Ledgerline wins on, but the map does not select this play for the current decision | Maintenance and loss of future differentiation | A better-resourced player forks and distributes it | Opening the policy-matched draft itself, even though it is the differentiating component |
| Land grab above a new commodity | Extraction is stage 4 and makes the policy-matched draft economic | Left-side spend without a new demand proof | A fast follower enters once the policy-matched draft is proven | No evidence that extraction is actually stage 4 |
| Fast follower | A rival pays for genesis while Ledgerline has better distribution or operations | Ecosystem and vocabulary controlled by the first mover | The first mover locks the standard | Claiming a distribution advantage that is not evidenced |
| Industrialize what your ecosystem proves | The product-side meter and policy experience reveal what customer accounts need from usage billing | Trust and the risk of taking value from the ecosystem | The ecosystem builds elsewhere | No rule for what Ledgerline will not take from customers |
| Buy time with a stopgap, then switch | A component is shifting right within four quarters and interim spend is small | A stopgap that must later be unpicked | The stopgap quietly becomes the product | No switch trigger or owner |
| Dispose of the liability | Three metered-billing vendors checked on 2026-12-18 support stage 3 for the billing and metering infrastructure, D6 killed the seat value metric, and N93 holds the 73 paid accounts for 12 months | A political fight and migration work | The billing team's attachment to the $15,000 meter | Retirement without the billing team, N93 or a date |
| Second-source a utility you depend on | Receipt extraction is stage 4, rented, and vendor concentration is a live question under DEP2 | An abstraction layer and vendor comparison work | The primary vendor bundles or reprices the service | An abstraction with only one implementation |
| Push your interface as the shared standard | The drafted-report counter needs a stable product-to-billing interface | Freedom to change the interface is reduced | The billing platform publishes another interface | A standard with one implementer and no consumer |
| Cross-subsidize: fund the left from the right | The rented extraction utility and billing capability may create efficiency for the policy-matched draft | Resentment from the line paying | A rival reduces the margin component | The transfer is invisible in the budget |

Some plays are deception plays, such as distorting a rival's roadmap or bundling to hide a price. They are not selected here. The map instead makes the market movement and the internal inertia visible.

For each play you intend to run, fill one row and put it in the [decision log](../templates/execution/decision-log.md).

| Play chosen | Component and rank it acts on | Map condition, with dated evidence | Counter we expect, and from whom | Abandon trigger, with date | Owner |
|---|---|---|---|---|---|
| Rent the utility and second-source it | Receipt extraction, rank 3 | Three document-extraction APIs checked on 2026-12-18, all metered; DEP2 is the open volume re-quote | The primary model vendor may bundle or reprice at customer scale; procurement owns the question | Abandon the rented utility play if DEP2 shows the metered API cannot support the customer-scale margin decision; date is not supplied because procurement owns the date | Priya Nair with procurement |
| Dispose of the liability | Seat entitlement, rank 2 | D6 killed the per-seat value metric on 2026-12-21; N93 holds 73 paid accounts at $6 per seat for 12 months | The billing team that built the $15,000 meter may defend continued use of the existing entitlement | Abandon the retirement only if the 12-month holds cannot be honored or if the migration decision memo due 2027-10-01 identifies a contractual blocker | Priya Nair with the billing lead |
| Build the drafted-report counter | Drafted-report counter, rank 2 | ADR-008 was proposed on 2026-12-22; DEP4 is needed by 2027-01-08; N87 estimates 1 person-month and $10,000 | The billing platform may require a different posting interface, or the existing seat meter may be defended as sufficient | Abandon this implementation if D6 is reversed and the value metric returns to seats; D6 is the re-run trigger | Priya Nair |

## ILLUSTRATIVE example

This is the Ledgerline example, not a benchmark.

The map has one differentiating stage 2 component, the policy-matched draft, and one enabling stage 2 component, the drafted-report counter, whose stage 2 rating is a placeholder pending a vendor scan of product-side usage-metering options. Receipt extraction is stage 4 because three document-extraction APIs were checked on 2026-12-18 and all are metered. Seat entitlement is stage 3 on the strength of the three metered-billing vendors checked on the same date that support the charge, a stage 3 reading that is Priya Nair's judgement drawn from the LC13 vendor count, while the entitlement logic inside it remains Ledgerline's own legacy code sitting in the charge path; D6 has already made that component a liability for the add-on.

The map therefore directs the team to build the policy-matched draft and the small counter, rent extraction, ask DEP2's second-source question, and retire seat entitlement after the N93 holds end. The billing team's 1.5 person-month and $15,000 seat-metering investment is inertia, not evidence that the component should remain.

Doctrine phase 1 scores are 1, 2, 1, 2 and 2. The shared language and named boundaries are present, but the user-need and duplication practices are only partly practiced. No phase 1 row scores 0.

The selected plays are to rent and second-source extraction, dispose of the seat-metering liability, and build the drafted-report counter. The re-run trigger is D6's change of value metric, with a further re-run required if DEP2 changes the extraction landscape, DEP4 changes the usage-meter boundary, or the 12-month holds reach their migration decision.

## The decision it feeds

This map feeds the [build, buy, partner sheet](../frameworks/strategy/build-buy-partner.md).

| Component | Ruling | Why |
|---|---|---|
| Policy-matched draft | Build | Stage 2, rank 1, and no Business-plan rival shows the account's own policy line beside a draft |
| Drafted-report counter | Build | Stage 2, rank 2, and required by the drafted-report value metric selected after D6 |
| Receipt extraction | Rent | Stage 4, with three metered APIs checked on 2026-12-18 |
| Extraction vendor depth | Second-source question | DEP2 remains open and procurement owns the volume re-quote |
| Seat entitlement | Dispose of the liability | D6 killed the seat metric; N93 holds the 73 paid accounts for 12 months |
| Billing-system invoice run | Buy or use existing capability | It is not the differentiator; the product-side counter should post into the billing run |

The budget moves to the drafted-report counter: N87 records 1 person-month and $10,000, needed by 2027-01-08. The $15,000 seat-metering work in N86 is not reused by the usage model. The map does not move extraction budget into another in-house parser.

## The trap

Mapping by authorship.

Ledgerline built the seat meter, so the billing team can reasonably describe it as custom work. That is not its current market stage. LC13 records three metered-billing vendors checked on 2026-12-18, and the stage 3 reading is Priya Nair's judgement drawn from that vendor count, supporting stage 3 for the billing and metering infrastructure the charge rests on, while the entitlement logic itself is Ledgerline's own legacy code inside that charge path. D6 then changed the value metric away from seats, and N93 limits the existing price to 12 months for the 73 paid accounts.

The opposite trap is mapping the policy-matched draft as a commodity because extraction is a commodity. LC13 says no Business-plan rival shows the account's own policy line beside a draft. The policy match therefore remains the stage 2 component closest to the need.

## Re-run trigger

**Re-run when D6's change of value metric changes the component map, and treat each of these as confirmation that the map must be checked: a new extraction vendor list, a DEP2 volume re-quote, a change in the drafted-report meter boundary under DEP4, the 12-month holds reaching their migration decision, a vendor term or availability change, or a decision to reverse D6.**

D6 changed the value metric on 2026-12-21, so this map is already a re-run of the earlier seat-based assumption. The next planned implementation dependency is DEP4, needed by 2027-01-08. The 73 paid accounts have 12-month price holds under N93, and the migration decision memo is due 2027-10-01.

A future map must re-score:

- The policy-matched draft if a vendor begins showing the account's own policy line beside its draft.
- Receipt extraction if DEP2 changes the metered price, vendor count or second-source case.
- The drafted-report counter if the billing platform changes its usage capability.
- Seat entitlement when the N93 holds reach their migration decision.

**Signed for the map walk:** Priya Nair, Engineering Lead, with Maya Chen, Product Manager, 2026-12-22.

## Feeds

- [Build, buy, partner](../frameworks/strategy/build-buy-partner.md): stage, movement and play decisions for the drafted-report counter
- [Solution architecture](../templates/architecture/solution-architecture.md) and the [integrations register](../templates/architecture/integrations.md): the rented extraction API and billing interface
- [Product strategy](../templates/planning/product-strategy.md): the policy-matched draft, drafted-report meter and seat-entitlement retirement
- [Roadmap](../templates/planning/roadmap.md): the usage meter and EXP-2 dependency
- [Product operating model assessment](../frameworks/assessment/product-operating-model-assessment.md): the unscored phase 2 to 4 doctrine gaps
- [Strategy kernel](../frameworks/strategy/strategy-kernel.md): the diagnosis and the chosen plays
- [Playing to Win](../frameworks/strategy/playing-to-win.md): the conditions behind the rented extraction and drafted-report meter plays
- [Premortem worksheet](../frameworks/execution/premortem-worksheet.md): the counter-play from the billing team and the extraction vendor
- [Decision log](../templates/execution/decision-log.md) and [ADR](../templates/architecture/adr.md): the plays, D6 and ADR-008
- [Now, Next, Later](../frameworks/prioritization/now-next-later.md): the drafted-report meter and its trigger
- [Cynefin](../frameworks/systems/cynefin.md): uncertainty around the stage 2 policy-matched draft
- DESIGN stage, feeds Gate 3: architecture and risks reviewed
- Method background: [knowledge index](../knowledge/INDEX.md), Wardley Mapping entry
