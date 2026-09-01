# Eval Spec: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 4 (acceptance criteria met) and Gate 5 (release readiness)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- An eval spec turns "the model should do X well" into something that can block a
     release. A requirement without a labeled dataset, a numeric threshold, and a named
     owner is a hope with a bullet point. Fill every field or write "N/A because
     [reason]". For products under a financial or data regulator, the stricter version
     of this table lives in ../../modules/regulated/README.md and wins on overlap. -->

**Feature:** [one sentence: what the model does, for whom]
**Model and version pinned:** [provider, model, exact version string]
**Spec owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Scenario set

<!-- Scenarios are the behaviors that matter, before you think about metrics. Include
     the ugly ones: adversarial input, out-of-scope requests, ambiguous cases. A
     scenario set that is all happy path measures nothing you will be paged about. -->

| # | Scenario | Why it matters | Source (real tickets, interviews, synthetic) |
|---|---|---|---|
| 1 | [e.g. user pastes a full email thread and asks for next steps] | [core use] | [support tickets Q3] |
| 2 | [e.g. input contains an instruction addressed to the model] | [injection surface] | [synthetic, red team] |
| 3 | [add rows until the ugly cases are covered] | | |

## 2. Golden dataset

- Location (repo path or system, access-controlled): [where]
- Size: [n labeled cases; 30 to 50 is a workable v1 floor, fewer is a demo]
- Labeling method and who labeled: [method, names]
- Versioned alongside the model version: [yes or no]
- Refresh cadence, and who adds production failures back in: [cadence, name]

## 3. Metrics and thresholds

<!-- Every threshold is either labeled ILLUSTRATIVE or cites the agreement that set it,
     as "per [agreement] dated YYYY-MM-DD". An unlabeled number gets quoted back at you. -->

| Metric | Definition (exact, computable) | Threshold | Status | Below threshold | Owner |
|---|---|---|---|---|---|
| [e.g. extraction accuracy] | [exact-match on labeled fields] | [e.g. 0.90, ILLUSTRATIVE] | ILLUSTRATIVE / per [agreement] | block release | [name] |
| [e.g. false-refusal rate] | [refusals on in-scope cases / in-scope cases] | [e.g. under 5%, ILLUSTRATIVE] | ILLUSTRATIVE / per [agreement] | [action] | [name] |
| [add] | | | | | |

## 4. Release gate

- Evals run at: [CI / pre-release / production sampling, and the sample rate]
- What blocks: [which rows above are hard gates vs monitored]
- Model or prompt upgrade policy: any change to the pinned model or prompt version re-runs the full set before it ships; [name] owns the re-run
- Where results are recorded (dated, retrievable): [location]

## Worked micro-example

One filled row, to show the shape: metric "merchant-name extraction accuracy", defined as exact match against the labeled field, dataset `evals/merchant-names-v2` (140 cases, labeled by two ops agents with disagreements adjudicated), threshold 0.92 ILLUSTRATIVE, below threshold block release, owner J. Doe. The row is boring. That is the point; boring rows are runnable.

## Exit gate

- [ ] Every scenario in section 1 has at least one dataset case covering it
- [ ] Every metric row has a definition, a numeric threshold, a status label, a below-threshold action, and a named owner
- [ ] The dataset location, size, and labeling method are stated, not implied
- [ ] Someone is named for feeding production failures back into the dataset
- [ ] The upgrade re-run rule is written and owned
