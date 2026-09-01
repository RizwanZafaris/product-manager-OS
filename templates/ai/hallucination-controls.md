# Hallucination Controls: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 4 (acceptance criteria met) and Gate 6 (outcomes verified)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- A model asserts with equal confidence whether it knows or not. These controls
     decide, in writing, what the system is allowed to state, what it must ground,
     and what it does when it does not know. "The model is usually right" is an
     observation, not a control. -->

**Feature:** [one sentence]
**Controls owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Grounding sources

<!-- What the system is allowed to state facts FROM. Anything not traceable to a row
     here falls under the abstain policy. -->

| Source | Content it grounds | Freshness guarantee | Access path |
|---|---|---|---|
| [e.g. orders database] | [order status, amounts, dates] | [live query] | [read-only API] |
| [e.g. help-center corpus] | [policy answers] | [re-indexed weekly] | [retrieval index vX] |
| [add] | | | |

## 2. Abstain policy

- When the system cannot ground a claim, it: [says what, exactly; write the user-facing wording]
- Fields the system must never fill by generation when the source is silent: monetary amounts, names and identifiers, dates and reference numbers, legal or regulatory statements, [add]
- Absence beats fabrication: an empty field with "not found in [source]" is the correct output, and the eval set contains cases that reward it: [eval case IDs]

## 3. Verifier step

<!-- The check that runs between generation and the user. Can be a rule, a second
     model call, or a human, but it must be named and testable. -->

- Verifier: [rules engine / second-pass model check / human review queue]
- What it checks: [claims against sources, numbers against fields, citations resolve]
- On failure: [strip the claim / regenerate once / route to human / fail closed]
- Latency budget for the verifier: [n ms]
- Owner: [name] · Test: [test ID]

## 4. Monitored error taxonomy

<!-- You cannot reduce what you do not count. Each error class gets a detection method
     and a rate someone reads on a cadence. -->

| Error class | Example | Detection | Rate reviewed by, cadence |
|---|---|---|---|
| Fabricated entity | [invented order number] | [ID validated against source] | [name, weekly] |
| Wrong number | [correct field, wrong value] | [sampled human audit] | [name, weekly] |
| Unsupported claim | [assertion with no grounding row] | [verifier log] | [name, weekly] |
| Stale fact | [true last month, false now] | [source freshness check] | [name, monthly] |
| [add] | | | |

## Worked micro-example

A support assistant is asked for a refund amount the retrieval step did not return. Wrong output: a plausible number. Correct output per this document: "I could not find the refund amount for this order; here is where to check", logged as an abstain, counted in the weekly rate. The abstain is a success case, and the eval set says so.

## Exit gate

- [ ] Every fact class the system outputs traces to a grounding source row
- [ ] The abstain wording is written here, not left to the model
- [ ] The verifier has an owner, a failure behavior, and a test that can fail
- [ ] Every error class has a detection method and a named reader on a cadence
