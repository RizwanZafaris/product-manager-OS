---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/architecture/component-spec.md", "templates/execution/tech-debt-register.md", "templates/planning/program-charter.md"]
method: "knowledge/design/design-systems-and-tokens.md"
aliases: ["Design System Audit", "design-system-audit"]
---
# Design System Audit

Based on the ideas of Brad Frost's interface inventory technique, the U.S. Web Design System maturity model (General Services Administration, CC0 1.0), the GOV.UK Design System's component lifecycle statuses (Government Digital Service, Open Government Licence v3.0), Ben Callahan and Sparkbox's design system maturity model, Nathan Curtis's team models for scaling a design system, Tomas Hirsch's design system adoption metric work at Mews, and Karen VanHouten's design system failure research. Explained here in this repository's own words.

## What it is for

A design system is not a fact about the organization, it is a claim that needs checking screen by screen. This worksheet audits how much of one product's shipped or built interface actually comes from the shared system, how mature that system is on two independent ladders, whether the governance that keeps a system alive is in place, and which of five well documented failure patterns is already visible. Where no system exists yet, or the mandate to keep the current one is not fixed, the same worksheet scores candidate foundations so the choice is made on evidence rather than on whoever demoed last. Its rows feed three places: a deviation becomes a tech-debt-register item or a component-spec proposal, and the finished picture becomes the design-system dependency the program charter needs to name.

## Run it when

- A Gate 3 design review needs an evidence-backed answer to "how much of this is really the system" instead of an impression from whoever built the newest screen
- The team is about to adopt, replace, or build a design system foundation and needs to compare candidates on more than visual taste
- A tech-debt conversation keeps citing "design system drift" with no inventory behind the phrase
- A design system has been running for a while and nobody has written down who owns what, how a component gets proposed, or how one gets retired

**Skip it when:** one product team owns its own interface with no shared library across products. There is nothing to audit adoption against, and steps 1 through 5 collapse to "we built what we built." Step 6 (choosing a foundation) can still run on its own the first time that team picks a component library to build on.

## Inputs you need first

- The screens or the build in scope, reachable the same way for every reviewer
- The design system's own documentation, if one exists: its component list, current version, and token names
- The name of whoever can answer the five governance questions in step 4 with more than a guess
- For step 6 only: the shortlist of candidate foundations and, for each, a link to its published licence file

## The worksheet

### 1. Interface inventory per screen

<!-- After Brad Frost's interface inventory technique, paraphrased. Screenshot
     every screen in scope, then tag every distinct UI element on it with
     exactly one of the three tags below. Do this before any arithmetic: the
     inventory is the raw material section 2 counts, and a tag decided while
     also computing coverage tends to drift toward whichever answer the
     counter wants. -->

| Screen | Element | Tag | System component (name and version), if applicable | Notes |
|---|---|---|---|---|
| | | system component / snowflake / deviation | | |

- **System component:** this element is the shared system's component, used as published, at the version named.
- **Snowflake:** this element is deliberately product-owned. Not every one-off is a problem; a payment amount ticker or a fraud-hold banner may have no reason to live in a shared system. Write the reason down beside it.
- **Deviation:** this element started as a system component and was detached, overridden, or hand-modified, or it duplicates a system component in the product's own code instead of importing it.

### 2. Arithmetic

<!-- Three counts, each with the distortion it carries (after Hirsch, Mews
     engineering, 2025) and the action it is meant to trigger. Compute all
     three from the same inventory pass; a coverage number produced from a
     different sample than the deviation count is not comparable to it. -->

**Coverage** = system-component instances divided by all instances on the inventoried screens.
*Distortion:* container components (cards, layout shells, page frames) dominate visual area while being a small share of instances, so a coverage number read from a screenshot overstates real usage; count instances, not pixels. Component complexity is not equal either, a badge and a datepicker count the same instance but are not the same adoption story. Pages are dynamic, so a dropdown, a modal, or an empty state that only appears on interaction is easy to miss in a single static pass; note which states were and were not inventoried.
*Action:* coverage below the team's own bar is a training and friction problem, not yet a debt problem. Route it to whoever owns onboarding to the system, not straight to the tech-debt register.

**Deviation rate** = deviation instances divided by all instances.
*Distortion:* one screen with a hand-modified component repeated fifty times is not fifty separate design decisions, it is one decision copied fifty times. Count distinct deviation decisions alongside raw instance counts, or a single copy-pasted override will read as a systemic adoption failure.
*Action:* each distinct deviation becomes a row in the [tech debt register](../../templates/execution/tech-debt-register.md) (Item: the deviation, stated as a fact about the system; Interest: the team-days it costs each quarter to keep diverging) or, where the deviation reveals a real gap the system should close, a proposal into the [component spec](../../templates/architecture/component-spec.md) process instead of a debt line.

**Deprecated instances** = instances of a system component the system itself has marked deprecated, whatever the reason.
*Distortion:* a component can be deprecated in the system's documentation weeks or months before any consuming product notices, so a low deprecated-instance count can mean either a clean product or a stale inventory pass. Check the pass date against the system's own changelog before reading a zero as good news.
*Action:* each deprecated instance gets a migration ticket with the system's stated replacement, sequenced against the deprecation route named in step 4.

### 3. Maturity

<!-- Two independent ladders. The first asks how deeply the CONSUMING
     product has adopted the system; the second asks how far along the
     system ITSELF has grown as a product. A team can score high on one and
     low on the other, and both readings matter. -->

**Adoption ladder** (after the U.S. Web Design System maturity model, General Services Administration, CC0 1.0). Score the product's adoption at each of the three levels, 0 (not started) to 2 (fully in place):

| Level | What it asks | Score (0 to 2) |
|---|---|---|
| Principles | Does the team's design and build process actually apply the system's stated design principles as an evaluative lens, not just cite them? | |
| Guidance | Do the product's components follow the system's published UX guidance, whether or not the product uses the system's own code? | |
| Code | Does the product use the system's design tokens and component code directly, with overrides kept to the settings the system exposes for that purpose? | |

A product can score 2 on Guidance while scoring 0 on Code: it rebuilt every component from scratch but followed the system's rules doing it. That is a real, if expensive, form of adoption, and the ladder is built to let the audit say so rather than force one blended number.

**System maturity stage** (after Ben Callahan and Sparkbox's design system maturity model). Name the one stage that best fits the system today, not the product's use of it:

| Stage | What is happening |
|---|---|
| 1: Building version one | The system is pre-first-release or just past it; component set, tooling, and technology choices are still being made |
| 2: Growing adoption | A first version exists; the work is persuading and teaching more internal teams to use it |
| 3: Surviving the teenage years | The system is part of daily work; the open questions are enforcing standards without killing creativity, prioritizing growth, and proving return on investment |
| 4: Evolving a healthy product | The system runs with the governance, sustainability planning, and communication strategy of a mature product |

### 4. Governance

<!-- Five questions, scored 0 to 2, each answered against the method card's
     Governance section rather than re-explained here. Do not restate what
     a team model, a lifecycle status, or a deprecation route is; that
     explanation lives once, in knowledge/design/design-systems-and-tokens.md
     (Governance section), and a second copy here would only drift out of
     sync with it. -->

See [knowledge/design/design-systems-and-tokens.md](../../knowledge/design/design-systems-and-tokens.md), Governance section, for what each row means before scoring it.

| Governance item | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Team model named (after Nathan Curtis, EightShapes: solitary, centralized, or federated) | No named model; whoever last touched the code decides | A model exists but nobody outside the system team could name it | Named, written down, and known by the teams that consume the system | |
| Contribution path exists and is known (after the GOV.UK Design System's contribution criteria) | No path; requests happen in hallway conversations | A path exists but consuming teams do not know it is there | Published, used, and consuming teams can point to it | |
| Lifecycle statuses in use (after the GOV.UK Design System's component lifecycle statuses) | No status is ever shown; every component looks equally settled | Statuses exist informally, in a changelog or a Slack channel, not on the component itself | Statuses are visible at the point of use, the way GOV.UK's trial tag sits on the component's own guidance page | |
| Issue split in use (after Brad Frost's bug, discrepancy, feature, recipe split) | Every report lands in one undifferentiated backlog | The team distinguishes types informally, not in the tracker | The tracker itself splits bug, visual discrepancy, system feature request, and product-owned recipe, and routes each differently | |
| Deprecation route with a warning-only phase | Deprecated means removed, with no notice | A deprecation is announced but nothing in the product surfaces it before removal | A warning-only phase exists first: consumers see the deprecation at build or design time and keep working while they migrate | |

### 5. VanHouten failure-pattern diagnostic

<!-- After Karen VanHouten's "Why Design Systems Fail" (2023), paraphrased.
     Five patterns from her practitioner experience. Mark each present,
     partly present, or absent, with the one sentence of evidence that
     justifies the mark; a mark with no evidence sentence is a guess,
     not a finding. -->

| Pattern | What it looks like | Present / partly / absent | Evidence |
|---|---|---|---|
| No shared, contextual purpose | "Improve the UX of our products" stands in for a purpose nobody can act on; no answer to why this org, why now | | |
| Overbuilding, or scaling too early | The system tried to cover every case for every team (scaling vertically) before proving the smallest shared set works for one team (scaling horizontally) | | |
| Inability to decide and move | Foundational choices (color, type, a component's first shape) stay open for months because every decision is treated as equally weighty | | |
| Lack of clear ownership and dedicated resources | The system's champion maintains it as an unstaffed side project on top of another full-time role | | |
| Lack of cultural alignment | Teams comply with the system on paper while quietly building around it, because nobody outside the system team was brought into why it exists | | |

Two or more patterns marked present is the threshold this worksheet uses to say the system's problem is organizational, not a missing component: no amount of new components fixes a purpose nobody agreed on or a champion with no budget.

### 6. Choosing a foundation

<!-- Run this step only when there is a real choice to make: adopting an
     external foundation, replacing the current one, or building from
     scratch versus buying in. Skip it when the organization mandates a
     specific system with no alternative on the table; scoring a choice
     nobody is free to make wastes the review's time. -->

**Skip it when:** the organization has already mandated a specific design system foundation and no alternative is under consideration.

Score each candidate 0 to 2 on each dimension. The licence question is a veto, not a score: a licence that fails it removes the candidate regardless of every other total.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Ownership model | No named owning team or role | An informal or part-time owner | A named team with budget and a stated team model |
| Published conformance report and known gaps | No report; gaps only found by hitting them | A report exists but is stale or incomplete | A current, published conformance report naming known gaps explicitly |
| Theming and dark mode mechanism | Hardcoded values, no mechanism | A mechanism exists but requires touching component internals | A documented, semantic-tier token mechanism, theme swap requires no component change |
| RTL, including overlays | Not supported, or supported only for base layout | Base layout mirrors correctly; overlays (menus, tooltips, modals) do not | Full mirroring including overlay positioning and icon direction |
| Design tool parity and who maintains it | No design-tool library, or one nobody maintains | A design-tool library exists but drifts from the code library, unowned | A maintained design-tool library kept in sync with code, with a named owner |
| Last release | No release in over a year, or version history not visible | Released within the last year, irregular cadence | Released within the last quarter, on a stated cadence |
| Licence (veto question, see [knowledge/design/ui-dependency-licensing.md](../../knowledge/design/ui-dependency-licensing.md)) | Licence fails the organization's own dependency policy, or no licence file is found | Licence passes with a caveat or a required action (attribution, notice-keeping) the team must actually do | Licence passes cleanly against the organization's dependency policy |

A candidate that scores 0 on the licence row is out regardless of its total on the other six dimensions; write down why in the register this step feeds, so the elimination is not re-litigated next quarter.

## Reading the result

Coverage, deviation rate, and deprecated-instance counts from step 2 are a snapshot, not a target; read them beside the maturity stage from step 3, because a system at stage 1 or 2 is supposed to have low coverage; it does not yet have enough surface area for high coverage to be possible. A governance score under half in step 4 predicts that step 2's numbers will not hold: without a named team model, a known contribution path, and visible lifecycle statuses, deviations accumulate faster than they get fixed regardless of how much engineering effort goes into components this quarter. Two or more patterns marked present in step 5 outrank a good step 2 number: an organizational failure pattern will erode good adoption numbers within a year if it is not addressed directly, usually by fixing purpose and ownership rather than by shipping more components. Step 6's output, when it runs, is a single recommended foundation plus the eliminated candidates and why, which becomes the [component spec](../../templates/architecture/component-spec.md) starting point and the design-system dependency row the [program charter](../../templates/planning/program-charter.md) names in its scope and out-of-scope tables.

## ILLUSTRATIVE example

Invented, for a mid-market expense-management product's receipt-capture and approval flow, three screens in scope: capture, review queue, and approval detail. Design system: an internal library at version 4.2, adopted eighteen months ago.

**Step 1 to 2 (abbreviated):** 61 total tagged instances across the three screens. 44 system components (name and version recorded per row, omitted here), 9 snowflakes (a currency-conversion ticker and a fraud-hold banner, both reasoned as product-specific), 8 deviations (a detached button variant reused six times across the review queue, counted as one distinct deviation decision, plus two one-off overrides). Coverage = 44 / 61 = 72 percent by instance count, read with the container-area caveat since the approval-detail screen's card shell is one of the 44 and dominates the screenshot. Deviation rate = 8 / 61 = 13 percent by instance, one distinct decision. Deprecated instances: 3, all one deprecated date-range picker still shipping on the review queue; the system's changelog shows it was deprecated four months before this pass, so the count is real, not stale.

**Step 3:** Adoption ladder: Principles 2 (the team cites the system's principles in design reviews), Guidance 1 (guidance followed on two of three screens; the fraud-hold banner ignores the system's alert-color guidance on purpose), Code 2 (tokens and components used directly, overrides limited to settings the system exposes). System maturity stage: 3, surviving the teenage years (daily use, an open debate this quarter about whether to fork the button component for a partner-branded surface).

**Step 4:** Team model named, centralized, publicly documented: 2. Contribution path exists and is known: 1 (a path exists in the system's own repo, but the product team learned about it from this audit, not from onboarding). Lifecycle statuses in use: 0 (nothing in the system's documentation marks anything trial or stable; the deprecated date-range picker was announced only in a changelog entry). Issue split in use: 1 (bugs and feature requests share one backlog; visual discrepancies get filed as bugs). Deprecation route with a warning-only phase: 1 (the changelog entry functioned as a warning, but nothing in the product's own build surfaced it, which is how three deprecated instances still ship). Governance total: 5 of 10.

**Step 5:** No shared, contextual purpose: absent (the system's charter document states a specific purpose, "cut new-screen build time by half," tied to a measured baseline). Overbuilding or scaling too early: absent (the system started with one product and expanded to three over eighteen months, matching the horizontal-before-vertical sequence). Inability to decide and move: partly present (the button-fork debate has been open six weeks with no decision cadence set). Lack of clear ownership: absent (a two-person team owns the system full time). Lack of cultural alignment: partly present (the fraud-hold banner's deliberate guidance break was never brought back to the system team, so the system team does not know their guidance is being knowingly overridden). One pattern present, two partly present: below this worksheet's two-pattern threshold, but the two partly-present patterns point at the same root, an undersized decision cadence, worth a fix before it compounds.

**Reading:** the 72 percent coverage number looks healthy for a stage-3 system, and the governance total at 5 of 10 is the more actionable finding: lifecycle statuses and a known contribution path would likely have caught the deprecated date-range picker before three instances shipped. The button-fork decision (step 5) is routed to a decision deadline rather than another round of debate. Outcome recorded: the fraud-hold banner's snowflake status is confirmed as deliberate and logged; the eight deviation instances become one tech-debt-register row (the detached button variant, principal estimated at two team-days) and one component-spec proposal (should the system add a variant instead of the product overriding it).

## The trap

Coverage as a quality KPI. A high coverage number says the product used a lot of the system's components; it says nothing about whether those components were the right ones, wired correctly, or serving users well. A team under pressure to raise coverage can do it by wrapping every element in a system container regardless of fit, which raises the number while making nothing better, and a team with a genuinely well-designed snowflake-heavy product can score low coverage while being exactly right for its users. Read coverage next to the reasoned snowflake list from step 1 and the maturity stage from step 3, never alone, and never as a target set before the audit that ran to hit it.

## Feeds

- [Component spec](../../templates/architecture/component-spec.md): deviations that reveal a real system gap, and the recommended foundation from step 6, become proposals
- [Tech debt register](../../templates/execution/tech-debt-register.md): each distinct deviation decision from step 2 that is not routed to a component-spec proposal becomes a register row, its interest figure drawn from the workaround and rework time it costs each quarter
- [Program charter](../../templates/planning/program-charter.md): the audit's outcome (which foundation, current coverage and governance scores) is the design-system dependency this program names in its scope and out-of-scope tables
- DESIGN stage, feeding [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
- Method background: [Design systems and tokens](../../knowledge/design/design-systems-and-tokens.md)

Where this worksheet paraphrases GOV.UK Design System content (the lifecycle-status and contribution-criteria rows in step 4), that content is reused under the Open Government Licence v3.0: "Contains public sector information licensed under the Open Government Licence v3.0." No Crown mark or GOV.UK branding is reproduced, and no endorsement by the Government Digital Service is implied.
