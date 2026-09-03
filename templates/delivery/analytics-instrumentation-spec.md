# Analytics Instrumentation Spec: [product or feature name]

**Stage:** DELIVER (feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md)), but write it before BUILD starts
**Knowledge:** [north star metric](../../knowledge/north-star-metric.md)
**Skill:** [metrics-tree](../../skills/metrics-tree/SKILL.md)

<!-- The PRD names success metrics. This file is the only thing that makes them
     measurable. Every metric is computed from events, and events only exist if
     someone specified them before the code was written. A spec written after build
     means launch week reports nothing, the metrics review runs on anecdotes, and
     the Gate 6 decision is a vote instead of a reading.

     Gate note: this file lives in delivery/ because Gate 5 checks it, but it is
     written during DESIGN and handed to engineering with the build ticket. The
     one rule that carries the document: every metric in section 1 traces to at
     least one event in section 2, and every event in section 2 serves at least
     one metric in section 1. Untraceable events are cost; untraceable metrics
     are fiction. -->

**Owner:** [name] · **Engineering counterpart:** [name] · **Last updated:** [YYYY-MM-DD]
**PRD:** [link to the filled ../definition/prd.md copy] · **Analytics platform:** [tool name]

## 1. Metrics this spec serves

<!-- Copy the metrics from the PRD success section and the OKR sheet. Do not invent
     new ones here. The italic row shows a completed entry. -->

| Metric | Defined in | Computed from (events below) | Reported where |
|---|---|---|---|
| | [PRD section / OKR sheet] | | [dashboard, section 5] |
| *reports submitted without edit* | *PRD section 4* | *report_submitted where edit_count = 0* | *launch dashboard, tile 2* |

## 2. Event taxonomy

<!-- Naming convention first, then the events. Pick one convention and never break
     it; a warehouse with three naming styles is three warehouses.
     Convention for this product: [e.g. object_action, snake_case, past tense]. -->

| Event name | Fires when (exact trigger) | Properties (from section 3) | Required for launch | Owner |
|---|---|---|---|---|
| | | | yes / no | |
| *report_submitted* | *user taps Submit and the API returns 2xx* | *report_id, edit_count, source* | *yes* | *[name]* |

## 3. Property dictionary

<!-- One row per property, defined once, reused across events. PII class feeds the
     data model's classification; see ../architecture/data-model.md. Anything
     marked PII needs a named reason to exist in analytics at all. -->

| Property | Type | Allowed values or format | PII class (none / pseudonymous / direct) | Notes |
|---|---|---|---|---|
| | | | | |

## 4. Identity and platforms

- User identifier in events: [field, and where it is set]
- Anonymous-to-known stitching: [how, or "not needed because <reason>"]
- Platforms covered: [web / iOS / Android / backend] · Gaps: [platform not covered, and why that is acceptable]
- Environment separation: [how staging events are kept out of production data]

## 5. QA plan

<!-- Instrumentation is code and it ships with bugs like any other code. An event
     nobody verified is an event that fires twice, or never, or with nulls. -->

- Verification method: [e.g. debug view walkthrough per event, automated event tests]
- Environment: [where] · Verifier: [name] · Verify by: [YYYY-MM-DD, before Gate 5]
- [ ] Every event marked required in section 2 was seen firing with correct properties
- [ ] Every metric in section 1 was computed once from staging data and the number was sane
- Known instrumentation gaps shipping anyway: [list with owner and fix date, or "none"]

## 6. Dashboards and consumers

| Dashboard | Link | Primary audience | Owner | Exists before launch |
|---|---|---|---|---|
| | | | | yes / no |

## Exit gate

This spec is done when:

- [ ] Every PRD success metric traces to named events, and every event serves a named metric
- [ ] Every property has a type and a PII class
- [ ] The QA plan has a named verifier and a date before Gate 5
- [ ] The launch dashboard exists and reads from these events, not from a manual export

Signed: [name], [role], [YYYY-MM-DD]
