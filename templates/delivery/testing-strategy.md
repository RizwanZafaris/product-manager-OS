---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Testing Strategy", "testing-strategy"]
---
# Testing Strategy: [product or feature name]

**Stage:** DELIVER (feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [acceptance agent](../../agents/acceptance-agent.md)

<!-- Fill every field, or write "N/A because <reason>". A blank field is a decision
     deferred to whoever finds it blank.

     This document is the argument for why Gate 5 can trust the build. It is written
     once per product or major feature, before testing starts, and it is the file the
     release-readiness checklist points back to. If a test level is not in this
     document, nobody is accountable for running it. -->

**Owner:** [name] · **Engineering counterpart:** [name] · **Status:** Draft / Agreed
**Version:** [n] · **Date:** [YYYY-MM-DD]

## 1. Scope

- In scope for testing: [areas, flows, integrations]
- Out of scope, and why that is safe: [area plus reason, or "nothing"]
- Linked requirements: [../definition/prd.md copy for this product] · [../definition/acceptance-criteria.md copy]

## 2. Test levels

<!-- Every level gets an owner and a blocking rule. A level marked non-blocking is a
     deliberate risk acceptance, not a default. Delete rows that truly do not apply
     and say why in the scope section. The italic row shows a completed entry.
     The four UI component sub-levels come from named, rendered UI states
     carrying the acceptance criteria, per
     [knowledge/design/component-driven-development.md](../../knowledge/design/component-driven-development.md);
     their state list is the single one in
     [ui-state-inventory.md](../definition/ui-state-inventory.md), never
     restated here. A visual baseline is accepted by a role that is not the
     component's author, and the acceptance is traced to a decision-log entry,
     not to a click on "approve" in a tool with no record. -->

| Level | What it proves | Owner | Where it runs | Maintenance cost | Blocks release? |
|---|---|---|---|---|---|
| Unit | | | | | |
| Integration | | | | | |
| Contract (API) | | | | | |
| End to end | | | | | |
| Performance and load | | | | | |
| Security | | | | | |
| Accessibility | | | | | |
| UI component: render (mounts without error, against every state in the UI state inventory) | | | | low, cheap to keep green | |
| UI component: interaction (a named user action produces its stated outcome) | | | | medium | |
| UI component: accessibility (role, name, and state exposed per state) | | | | medium | |
| UI component: visual (a screenshot diff against an accepted baseline) | | | | high, baselines rot fast; accepted only by a non-author role, traced to [decision-log.md](../execution/decision-log.md) | |
| Model evals (AI features, see [eval spec](../ai/eval-spec.md)) | | | | | |
| *Example: Contract (API)* | *provider and consumer schemas still agree* | *A. Rivera* | *CI, every merge* | *low* | *yes* |

## 3. Coverage targets

<!-- A coverage number is a smoke alarm, not proof of quality. Targets are numbers
     with owners, never adjectives like "high" or "adequate". -->

| Area | Target | Current | Owner |
|---|---|---|---|
| [critical path modules] | [n%] | [n%] | [name] |
| [new code in this release] | [n%] | [n%] | [name] |

## 4. Environments

| Environment | Purpose | Data policy | Refresh cadence | Who has access |
|---|---|---|---|---|
| [dev] | | [synthetic only] | | |
| [staging] | | [no production personal data] | | |
| [production] | | [real data, monitored] | | |

<!-- Production personal data never leaves production. If a test needs realistic data,
     the answer is synthetic or anonymized data, and the anonymization has an owner. -->

## 5. Entry and exit criteria

**Testing starts when:**
- [ ] Acceptance criteria are signed (Gate 4 input, see [../definition/acceptance-criteria.md](../definition/acceptance-criteria.md))
- [ ] The environment above is up and seeded
- [ ] [add product-specific entry conditions]

**Testing ends when:**
- [ ] Every blocking level in section 2 has run and passed
- [ ] Open defects are within the ladder rules in section 6
- [ ] The [edge-case register](edge-cases.md) has no unresolved rows
- [ ] Results are recorded where the release-readiness reviewer can find them: [location]

## 6. Defect severity ladder

| Severity | Definition | Release rule |
|---|---|---|
| S1 | Data loss, security breach, or the product unusable | Always blocks |
| S2 | A core flow broken with no workaround | Blocks unless the sign-off names who accepted it and why |
| S3 | Broken with a workaround, or a non-core flow | Ships with a fix date and an owner |
| S4 | Cosmetic | Ships, tracked |

## Exit gate

This document passes when:

- [ ] Every test level has an owner and an explicit blocking rule
- [ ] Coverage targets are numbers with owners, not adjectives
- [ ] Entry and exit criteria could be applied by someone who just joined the team
- [ ] The environment table states the data policy for each environment
- [ ] The severity ladder says exactly what blocks release

Signed: [name], [role], [YYYY-MM-DD]
