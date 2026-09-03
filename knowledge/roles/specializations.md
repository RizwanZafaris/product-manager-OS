---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["PM Specializations", "specializations"]
---
# PM Specializations

The [ladder](ladder.md) describes altitude; specialization describes terrain. Same rungs, same gate discipline, different problems and different documents. Seven shapes recur across the industry, described below with what each owns, decides, and produces, its success measure, and the specific way it goes wrong. Titles vary by company even more here than on the ladder, so map by the work, not the badge.

One rule holds across all seven: specialization narrows the problems, never the accountability. A Growth PM who disclaims responsibility for retention quality, or a Platform PM who disclaims usability because the users are engineers, has traded the job for a fraction of it.

## Core PM

The default shape and the reference point for the other six: one product area, all six stages of the [operating loop](../../os/OPERATING-LOOP.md), all four risks of [empowered product teams](../cagan-product-teams.md).

- **Decides:** scope, priority, and document weight within the area; gate recommendations.
- **Documents:** produces the [discovery](../../templates/discovery/discovery-document.md) to [metrics review](../../templates/operate/metrics-review.md) chain; consumes strategy and OKRs.
- **Success measure:** the outcome named at Gate 1, verified at Gate 6.
- **Failure mode:** shapelessness. Without a deliberate terrain, a core PM drifts to wherever the loudest stakeholder points.

## Product Owner

The role Scrum defines: order the backlog, accept the work, be available to the team. Marty Cagan's position, argued across the SVPG essays, is that carving this off as a separate junior job is an anti-pattern: it splits the person who decides from the person who saw the evidence, and produces a backlog administrator with no mandate to say no. This repository takes the same side: PO is a set of responsibilities a PM carries into delivery, not a separate career.

The counter-reality: large Scrum and SAFe organizations staff the split anyway, and holding the PO title is not a character flaw. If that is your seat, the card's advice is to do the PM job from it.

- **Decides:** backlog order, sprint-level acceptance, clarifications the team needs today.
- **Documents:** produces [acceptance criteria](../../templates/definition/acceptance-criteria.md), user stories, and [business rules](../../templates/definition/business-rules.md); consumes the [PRD](../../templates/definition/prd.md) and [FRD](../../templates/definition/frd.md).
- **Success measure:** the team is never blocked on a product answer, and accepted work matches written criteria.
- **Failure mode:** proxy management: relaying decisions made elsewhere at increasing speed and decreasing fidelity. The escape is to start producing discovery evidence nobody asked for, which is how POs become PMs.

## Technical PM

A PM whose users or buyers are engineers: APIs, developer tools, infrastructure sold or consumed as product. One title collision to defuse immediately: Technical Program Manager is a different job (cross-team delivery orchestration) that shares the acronym; this entry covers the product role.

- **Decides:** API surface and contract shape jointly with architects, versioning and deprecation policy, which integrations are supported versus tolerated.
- **Documents:** produces [API contracts](../../templates/architecture/api-contract.md), [NFRs](../../templates/definition/nfr.md), and [integration registers](../../templates/architecture/integrations.md); consumes [system design](../../templates/architecture/system-design.md) and [ADRs](../../templates/architecture/adr.md) as primary reading, not appendices.
- **Success measure:** adoption by builders and time-to-first-successful-call; reliability against the written NFR targets.
- **Failure mode:** fluency without judgment: knowing the system well enough to defend every constraint and forgetting to represent the user who meets it. Documentation debt is the visible symptom.

## Growth PM

Owns a metric, not a surface: activation, retention, monetization, or the loop that connects them. Works in experiment portfolios where most bets lose. The craft descends from Sean Ellis's growth practice and the loops-over-funnels framing argued by Brian Balfour and Casey Winters; the [north star metric](../north-star-metric.md) card and the AARRR entry in the [knowledge index](../README.md) carry the underlying models.

- **Decides:** the experiment portfolio and its kill thresholds, which input metric is the current bet, when a result is real versus noise.
- **Documents:** produces experiment briefs and the [growth plan](../../templates/planning/growth-plan.md); consumes the [metrics review](../../templates/operate/metrics-review.md) and instrumentation specs.
- **Success measure:** input metrics moved with the counter-metric honored. A growth win that degrades the counter-metric is a loss booked in a different quarter.
- **Failure mode:** local maxima and dark patterns: optimizing the step in front of you until the product is a funnel wearing a product costume. The kill condition in the growth plan template exists because of this failure.

## Platform PM

Runs an internal platform as a product where the customers are the company's own teams, and captive customers make every signal a liar.

- **Decides:** what the paved road includes, migration timelines and deprecation dates, which team requests are roadmap and which are tickets.
- **Documents:** produces [system design](../../templates/architecture/system-design.md) input, [API contracts](../../templates/architecture/api-contract.md), and a [dependency register](../../templates/execution/dependency-register.md) that is actually governed; consumes every consuming team's roadmap.
- **Success measure:** voluntary adoption, or where adoption is mandated, migration completed on the published date with support load falling afterward. Mandated adoption is not product-market fit and must never be reported as if it were.
- **Failure mode:** building for the architecture review instead of the internal user. The platform is elegant, the paved road is empty, and product teams keep their own duct tape because the duct tape ships.

## Data PM

Owns data products: pipelines, metrics layers, instrumentation standards, the datasets other teams build on. The user is anyone who makes a decision from the data, which is everyone.

- **Decides:** schema contracts and their change policy, data quality thresholds and who is paged on breach, what gets instrumented as standard versus per-team.
- **Documents:** produces the [data model](../../templates/architecture/data-model.md) and [observability spec](../../templates/architecture/observability.md); consumes the [compliance impact assessment](../../templates/operate/compliance-impact-assessment.md), because data products inherit every regulation their inputs touch.
- **Success measure:** trust: decisions are made from the governed dataset instead of private spreadsheets, and metric disputes end by citation instead of meeting.
- **Failure mode:** the dashboard factory. Output is measured in charts shipped; nobody can name a decision any chart changed. The fix is the same evidence discipline the discovery templates enforce, pointed inward.

## AI PM

Owns a product with a model inside, which adds a risk class the other six shapes do not carry: the product is probabilistic, and its failures are discovered rather than designed. In this repository the terrain is concrete: the AI overlay activates, and the [templates/ai/](../../templates/ai/eval-spec.md) pack becomes required reading rather than optional.

- **Decides:** eval thresholds and what blocks ship, guardrail scope, where a human approval gate is non-negotiable, the acceptable failure taxonomy and its monitoring.
- **Documents:** produces the [eval spec](../../templates/ai/eval-spec.md), [guardrails](../../templates/ai/guardrails.md), [human approval gates](../../templates/ai/human-approval-gates.md), and [red team review](../../templates/ai/red-team-review.md); consumes everything a core PM consumes, plus incident reports as a first-class evidence source. Under a financial or data regulator, the [reg-gap-check skill](../../skills/reg-gap-check/SKILL.md) routes to the regulated overlay.
- **Success measure:** product outcomes and eval pass rates and contained failures, jointly. Any one alone is a partial grade.
- **Failure mode:** demo-driven development: the demo works, the eval spec is a stub, and the failure taxonomy is written after the incident. The eval-spec template blocks ship on failure precisely because this failure mode is the default.

## Sources

- Marty Cagan, SVPG essays and Inspired (2017): the product owner split as anti-pattern, and the four-risk accountability every specialization keeps. See [empowered product teams](../cagan-product-teams.md).
- Sean Ellis, and Brian Balfour and Casey Winters' writing on growth loops: the Growth PM shape, in this repo via the [north star metric](../north-star-metric.md) card and the AARRR index entry.
- Ken Schwaber and Jeff Sutherland, the Scrum Guide: the Product Owner responsibilities paraphrased above.
- This repository's own AI overlay ([templates/ai/](../../templates/ai/eval-spec.md)): the AI PM terrain, stated as templates rather than theory.
