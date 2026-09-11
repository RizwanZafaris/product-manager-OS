# Worked Examples

Eleven standalone examples and three journeys. Two of the standalone examples take one fictional product, an expense-report copilot at a fictional mid-market software company, through the front half of the [operating loop](../os/OPERATING-LOOP.md). The third takes the templates in the other direction: onto a product that was already live, already messy, and already carrying nine years of undocumented decisions. The fourth is a transcript rather than a filled template: the Conductor interviewing a PM, shown at the two moments interviews earn their keep, a vague answer challenged into evidence and a stage advance refused with the gate checklist as the reason. The eleventh is the record of a real routing run, the only file here produced by a model call rather than written by hand. The remaining six fill a framework worksheet or a planning template on the same copilot; the section after the table says why they exist. The [three journeys](#the-three-journeys) are larger: each is one data sheet and an artifact map, plus the filled artifacts the map indexes, thirteen for Ledgerline, fourteen for Sahulat and sixteen for Harbourgate, forty-three in all, cross-checked against each other and against their data sheet. Read them before filling the templates: a template shows the questions, an example shows what an answer that survives a gate review looks like, including the places where the honest answer is a gap with an owner.

Everything in these examples is invented. The company, the people, the interview counts, and every number are fiction built to illustrate the format. Nothing here is evidence about any real product, and none of the figures are targets to copy.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [expense-copilot-discovery.md](expense-copilot-discovery.md) | [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md) | DISCOVER, taken to Gate 1 |
| [expense-copilot-prd.md](expense-copilot-prd.md) | [templates/definition/prd.md](../templates/definition/prd.md) | DEFINE, taken to Gate 2 |
| [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md) | Extracts from problem framing, competitive analysis, PRD, data model, and the decision log | Entered mid-flight, currently at Gate 4 |
| [conductor-transcript.md](conductor-transcript.md) | [templates/execution/state.md](../templates/execution/state.md), plus the Gate 1 checklist from [os/STAGE-GATES.md](../os/STAGE-GATES.md) | DISCOVER into DEFINE, refused once at Gate 1 |
| [ledgerline-jtbd-job-map.md](ledgerline-jtbd-job-map.md) | [frameworks/discovery/jtbd-job-map.md](../frameworks/discovery/jtbd-job-map.md) | DISCOVER, feeds Gate 1 |
| [ledgerline-business-case.md](ledgerline-business-case.md) | [templates/planning/business-case.md](../templates/planning/business-case.md) | DISCOVER and the PLANNING track, feeds Gate 1 and the roadmap |
| [ledgerline-kano-survey.md](ledgerline-kano-survey.md) | [frameworks/discovery/kano-survey.md](../frameworks/discovery/kano-survey.md) | DEFINE, feeds Gate 2 through the PRD scope table |
| [ledgerline-strategy-kernel.md](ledgerline-strategy-kernel.md) | [frameworks/strategy/strategy-kernel.md](../frameworks/strategy/strategy-kernel.md) | PLANNING track, feeds the product strategy |
| [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md) | [frameworks/prioritization/rice-scoring-sheet.md](../frameworks/prioritization/rice-scoring-sheet.md) | PLANNING track, feeds the roadmap |
| [ledgerline-north-star-tree.md](ledgerline-north-star-tree.md) | [frameworks/metrics/north-star-input-tree.md](../frameworks/metrics/north-star-input-tree.md) | PLANNING track, feeds the north star sheet and the OKRs |
| [ledgerline-harness-routing-run.md](ledgerline-harness-routing-run.md) | Fills no template. A live run record from `harness/runner.py`, kept because the routing layer's claims are cheap to write and easy to fake | DISCOVER evidence, plus one judgment task the runner queued rather than downgraded |

The brownfield example exists because clean examples teach the easy case. It shows a reconstructed Gate 1 labeled as reconstructed, an out-of-scope table doing the load-bearing work, a coupling the team wrote into the architecture rather than designing around, and one decision that was made in April and reversed in May, with both log entries kept.

## The three journeys

Each journey is one file holding the story, a data sheet every artifact draws its numbers and ids from, and an artifact map giving each artifact's brief: what it decides and which data-sheet rows it may not contradict. Every artifact fills one template, keeps that template's H2 structure, walks its exit gate at the bottom, and links back to its journey. The tables below index them in the order each journey's own artifact map lists them.

### Ledgerline: pricing and selling the expense copilot

[ledgerline-journey.md](ledgerline-journey.md) takes the same invented company from pricing and packaging through a killed pricing experiment to the post-pivot growth plan, PLANNING through OPERATE. It fills no template itself: it is the data sheet and the artifact map for the thirteen files below.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [ledgerline-positioning.md](ledgerline-positioning.md) | [templates/planning/positioning.md](../templates/planning/positioning.md) | PLANNING track, feeds the GTM plan |
| [ledgerline-pricing-packaging.md](ledgerline-pricing-packaging.md) | [templates/planning/pricing-packaging.md](../templates/planning/pricing-packaging.md) | PLANNING track, feeds Gate 5 readiness |
| [ledgerline-growth-plan.md](ledgerline-growth-plan.md) | [templates/planning/growth-plan.md](../templates/planning/growth-plan.md) | OPERATE, feeds Gate 6 |
| [ledgerline-gtm-plan.md](ledgerline-gtm-plan.md) | [templates/planning/gtm-plan.md](../templates/planning/gtm-plan.md) | DELIVER, feeds Gate 5 |
| [ledgerline-okrs.md](ledgerline-okrs.md) | [templates/planning/okrs.md](../templates/planning/okrs.md) | PLANNING track, scored into Gate 6 |
| [ledgerline-experiment-brief.md](ledgerline-experiment-brief.md) | [templates/operate/experiment-brief.md](../templates/operate/experiment-brief.md) | OPERATE, feeds Gate 6 |
| [ledgerline-metrics-dictionary.md](ledgerline-metrics-dictionary.md) | [templates/operate/metrics-dictionary.md](../templates/operate/metrics-dictionary.md) | OPERATE, feeds Gate 6; written before the instrumentation |
| [ledgerline-dashboard-spec.md](ledgerline-dashboard-spec.md) | [templates/operate/dashboard-spec.md](../templates/operate/dashboard-spec.md) | OPERATE, feeds Gate 6; specified before launch day |
| [ledgerline-metrics-review.md](ledgerline-metrics-review.md) | [templates/operate/metrics-review.md](../templates/operate/metrics-review.md) | OPERATE, feeds Gate 6 |
| [ledgerline-sales-enablement-one-pager.md](ledgerline-sales-enablement-one-pager.md) | [templates/delivery/sales-enablement-one-pager.md](../templates/delivery/sales-enablement-one-pager.md) | DELIVER, feeds Gate 5 |
| [ledgerline-win-loss-review.md](ledgerline-win-loss-review.md) | [templates/operate/win-loss-review.md](../templates/operate/win-loss-review.md) | OPERATE, feeds Gate 6 |
| [ledgerline-feedback-program.md](ledgerline-feedback-program.md) | [templates/operate/feedback-program.md](../templates/operate/feedback-program.md) | OPERATE, feeds Gate 6; intake feeds DISCOVER |
| [ledgerline-status-report.md](ledgerline-status-report.md) | [templates/execution/status-report.md](../templates/execution/status-report.md) | BUILD and DELIVER, weekly; feeds Gate 4 and Gate 5 |

### Sahulat: a solo PM from zero to one

[sahulat-journey.md](sahulat-journey.md) follows a fictional mobile-money wallet's bill-pay feature from DISCOVER to a Gate 6 PIVOT, run by one product manager. It fills no template itself: it is the data sheet and the artifact map for the fourteen files below.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [sahulat-user-research-plan.md](sahulat-user-research-plan.md) | [templates/discovery/user-research-plan.md](../templates/discovery/user-research-plan.md) | DISCOVER, feeds Gate 1 |
| [sahulat-interview-guide.md](sahulat-interview-guide.md) | [templates/discovery/interview-guide.md](../templates/discovery/interview-guide.md) | DISCOVER, feeds Gate 1 |
| [sahulat-interview-notes.md](sahulat-interview-notes.md) | [templates/discovery/interview-notes.md](../templates/discovery/interview-notes.md) | DISCOVER, feeds Gate 1 |
| [sahulat-personas.md](sahulat-personas.md) | [templates/discovery/personas.md](../templates/discovery/personas.md) | DISCOVER, feeds Gate 1 |
| [sahulat-problem-framing.md](sahulat-problem-framing.md) | [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md) | DISCOVER, feeds Gate 1 |
| [sahulat-opportunity-assessment.md](sahulat-opportunity-assessment.md) | [templates/discovery/opportunity-assessment.md](../templates/discovery/opportunity-assessment.md) | DISCOVER, feeds Gate 1 |
| [sahulat-one-pager.md](sahulat-one-pager.md) | [templates/definition/one-pager.md](../templates/definition/one-pager.md) | DEFINE, feeds Gate 2 |
| [sahulat-acceptance-criteria.md](sahulat-acceptance-criteria.md) | [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md) | DEFINE, feeds Gate 2, verified at Gate 4 |
| [sahulat-user-stories.md](sahulat-user-stories.md) | [templates/definition/user-stories.md](../templates/definition/user-stories.md) | DEFINE, feeds Gate 2, worked through BUILD |
| [sahulat-vision.md](sahulat-vision.md) | [templates/planning/vision.md](../templates/planning/vision.md) | PLANNING track, feeds every stage |
| [sahulat-north-star-metric.md](sahulat-north-star-metric.md) | [templates/planning/north-star-metric.md](../templates/planning/north-star-metric.md) | PLANNING track, scored at Gate 6 |
| [sahulat-decision-log.md](sahulat-decision-log.md) | [templates/execution/decision-log.md](../templates/execution/decision-log.md) | All stages, reviewed at every gate |
| [sahulat-launch-comms-plan.md](sahulat-launch-comms-plan.md) | [templates/delivery/launch-comms-plan.md](../templates/delivery/launch-comms-plan.md) | DELIVER, feeds Gate 5 |
| [sahulat-post-launch-review.md](sahulat-post-launch-review.md) | [templates/operate/post-launch-review.md](../templates/operate/post-launch-review.md) | OPERATE, feeds Gate 6 |

### Harbourgate: modernising a regulated brownfield checkout

[harbourgate-journey.md](harbourgate-journey.md) completes [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md), from Gate 4 through Gate 6 PERSIST and the retirement of the legacy payment layer. It fills no template itself: it is the data sheet and the artifact map for the sixteen files below.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [harbourgate-adr.md](harbourgate-adr.md) | [templates/architecture/adr.md](../templates/architecture/adr.md) | DESIGN, feeds Gate 3 |
| [harbourgate-system-design.md](harbourgate-system-design.md) | [templates/architecture/system-design.md](../templates/architecture/system-design.md) | DESIGN, feeds Gate 3 |
| [harbourgate-api-contract.md](harbourgate-api-contract.md) | [templates/architecture/api-contract.md](../templates/architecture/api-contract.md) | DESIGN, feeds Gate 3 |
| [harbourgate-integrations.md](harbourgate-integrations.md) | [templates/architecture/integrations.md](../templates/architecture/integrations.md) | DESIGN, feeds Gate 3 |
| [harbourgate-security-architecture.md](harbourgate-security-architecture.md) | [templates/architecture/security-architecture.md](../templates/architecture/security-architecture.md) | DESIGN, feeds Gate 3 |
| [harbourgate-observability.md](harbourgate-observability.md) | [templates/architecture/observability.md](../templates/architecture/observability.md) | DESIGN, feeds Gate 3; re-checked at Gate 5 |
| [harbourgate-nfr.md](harbourgate-nfr.md) | [templates/definition/nfr.md](../templates/definition/nfr.md) | DEFINE, feeds Gate 2 |
| [harbourgate-business-rules.md](harbourgate-business-rules.md) | [templates/definition/business-rules.md](../templates/definition/business-rules.md) | DEFINE, feeds Gate 2; amended through DELIVER |
| [harbourgate-dependency-register.md](harbourgate-dependency-register.md) | [templates/execution/dependency-register.md](../templates/execution/dependency-register.md) | DESIGN, feeds Gate 3; reviewed weekly through DELIVER |
| [harbourgate-stakeholder-map.md](harbourgate-stakeholder-map.md) | [templates/execution/stakeholder-map.md](../templates/execution/stakeholder-map.md) | DISCOVER through OPERATE, first required at Gate 2 |
| [harbourgate-risk-register.md](harbourgate-risk-register.md) | [templates/execution/risk-register.md](../templates/execution/risk-register.md) | DESIGN, feeds Gate 3; reviewed weekly |
| [harbourgate-migration-cutover-plan.md](harbourgate-migration-cutover-plan.md) | [templates/delivery/migration-cutover-plan.md](../templates/delivery/migration-cutover-plan.md) | DELIVER, feeds Gate 5 |
| [harbourgate-release-readiness.md](harbourgate-release-readiness.md) | [templates/delivery/release-readiness.md](../templates/delivery/release-readiness.md) | DELIVER, this file is Gate 5 (attempt 2) |
| [harbourgate-incident-postmortem.md](harbourgate-incident-postmortem.md) | [templates/operate/incident-postmortem.md](../templates/operate/incident-postmortem.md) | OPERATE event review, written in DELIVER, feeds Gate 6 |
| [harbourgate-sunset-eol-plan.md](harbourgate-sunset-eol-plan.md) | [templates/operate/sunset-eol-plan.md](../templates/operate/sunset-eol-plan.md) | OPERATE, executes the consequence of Gate 6 |
| [harbourgate-compliance-impact-assessment.md](harbourgate-compliance-impact-assessment.md) | [templates/operate/compliance-impact-assessment.md](../templates/operate/compliance-impact-assessment.md) | DEFINE and DELIVER, feeds Gate 2 and Gate 5; re-verified at sunset |

## Why the framework examples exist

A worksheet shows the form. An example shows a filled form: the declarations made before any scoring, the arithmetic done on the page where a reader can check it, the decision rule applied at the point where it actually bites (a Kano tie-break, a RICE row that scores low against the declared goal and is still worth building, a payback that fails at half the assumed adoption), and the cells left open with an owner because the invented team had no evidence for them. The six share one product and one set of invented facts, so a figure in the business case traces to the discovery document and a backlog row in the RICE sheet to a Kano class. A naming note: these six call the company Ledgerline, the repository's standard name for the invented company, and refer to people by role; the earlier pair calls the same company Fernwood Software and gives its people names. Same product, same interviews, same figures. The later Ledgerline journey and its thirteen artifacts depart from the by-role convention and name a cast: Maya Chen (product manager), Priya Nair (engineering lead), Daniel Okafor (finance lead), Isabel Ferreira (chief product officer), Tomas Lindqvist (head of product marketing), Ruth Adeyemi (VP sales), Kwame Boateng (data analyst), Hana Sato (head of customer success), and Marcus Webb (account executive); the journey's own "The people" section is the source for all nine.

## How these were produced

The first three follow Method 1 from the README: the template was copied unchanged, every field was filled by hand, and the exit gate at the bottom was walked box by box. No AI runtime was involved, which is the point; the documents stand on their own. The conductor transcript is the deliberate exception: it illustrates an interactive runtime driving the interview, and every STATE.md excerpt in it was produced by the rules the transcript itself demonstrates. The PRD cross-references the discovery document the way a real Gate 2 artifact cites its Gate 1 evidence, and because the product contains a model, it points into the AI overlay under [templates/ai/](../templates/ai/eval-spec.md) for the parts a conventional PRD cannot carry. The six framework examples were filled the same way as the first three: worksheet copied, every input invented and labeled ILLUSTRATIVE, the arithmetic done by hand, and any cell without evidence marked open with an owner rather than filled by guesswork.

The 43 journey artifacts were produced the same way, journey by journey: each artifact was filled by hand from its journey's data sheet, reviewed on its own, and then the whole journey had a cross-artifact pass that reconciled figures one artifact carried differently from another or from the data sheet. The last such consistency pass on each journey was not recorded clean, per [CHANGELOG.md](../CHANGELOG.md), so where two artifacts still disagree, the journey's own data sheet is the authority, not either artifact's wording.

## The regulated worked example

A third, fully worked example exists for teams under a financial regulator: the dispute-summary PRD inside the regulated module, at `modules/regulated/examples/dispute-summary/PRD.md`. It is a byte-exact copy from its canonical source repository and is never edited here; the module's own README states the policy.
