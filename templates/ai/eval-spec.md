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

## 0. Trace source and error analysis

<!-- Before metrics, read the failures. This block restates, in this repository's own
     words, the error-analysis-first discipline argued by Hamel Husain, Shreya
     Shankar, and Eugene Yan, and echoed in Anthropic's guidance on building evals:
     open-code real traces first, let the failure taxonomy fall out of the reading,
     and only then decide what to measure. An eval built metric-first measures what
     was easy to compute; an eval built from read traces measures what actually goes
     wrong. -->

- Traces read: [n production or support traces, open-coded by hand; 50 to 100 is a workable v1, labeled ILLUSTRATIVE]
- Who read them: [names, at least one being the spec owner]
- Where the coded traces live: [location]

| Failure cluster (from the traces, not from imagination) | Frequency in the read set | Example trace ID |
|---|---|---|
| [e.g. wrong entity picked when the input names two] | [n of the read set] | [id] |
| [add a row per cluster found] | | |

Every scenario in section 1 either names the cluster it covers or is labeled
"synthetic": a case the traces have not produced yet but the team can argue for,
such as an injection attack. A scenario set with no cluster-backed rows was written
before anyone read the data.

## 1. Scenario set

<!-- Scenarios are the behaviors that matter, before you think about metrics. Include
     the ugly ones: adversarial input, out-of-scope requests, ambiguous cases. A
     scenario set that is all happy path measures nothing you will be paged about. -->

| # | Scenario | Why it matters | Source (cluster # from section 0, or "synthetic") |
|---|---|---|---|
| 1 | [e.g. user pastes a full email thread and asks for next steps] | [core use] | [cluster 1] |
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
     as "per [agreement] dated YYYY-MM-DD". An unlabeled number gets quoted back at you.

     Grader type is a required column. Code graders (exact match, schema check) are
     cheap and trustworthy. Human graders are the reference. A model grader is itself
     a model: before any model-graded row may gate a release, its judgments must be
     validated against a held-out set of human labels, reporting precision, recall,
     and false-accept rate. An unvalidated model grader gating a release is one model
     vouching for another. -->

### 3a. Capability suite

<!-- Deliberately hard cases at the edge of what the feature can do. A healthy
     capability suite scores well below a perfect pass rate; if everything passes,
     the suite has stopped telling you where the frontier is, so add harder cases.
     Capability rows inform the release decision; they rarely hard-block it. -->

| Metric | Definition (exact, computable) | Grader (code / human / model) | Threshold | Status | Below threshold | Owner |
|---|---|---|---|---|---|---|
| [e.g. multi-document synthesis quality] | [rubric score on held-out hard set] | [model, validated per note above] | [e.g. 0.60, ILLUSTRATIVE] | ILLUSTRATIVE / per [agreement] | [investigate, not block] | [name] |
| [add] | | | | | | |

### 3b. Regression suite

<!-- Cases the product already handles and must never lose. This suite runs in CI on
     every prompt or model change and its pass rate sits at or near perfect; any drop
     is a regression, and a regression blocks. Failed capability cases graduate here
     once the team fixes them. -->

| Metric | Definition (exact, computable) | Grader (code / human / model) | Threshold | Status | Below threshold | Owner |
|---|---|---|---|---|---|---|
| [e.g. extraction accuracy] | [exact-match on labeled fields] | [code] | [e.g. 0.90, ILLUSTRATIVE] | ILLUSTRATIVE / per [agreement] | block release | [name] |
| [e.g. false-refusal rate] | [refusals on in-scope cases / in-scope cases] | [human] | [e.g. under 5%, ILLUSTRATIVE] | ILLUSTRATIVE / per [agreement] | [action] | [name] |
| [add] | | | | | | |

## 4. Release gate

- Evals run at: [CI / pre-release / production sampling, and the sample rate]
- What blocks: [which rows above are hard gates vs monitored]
- Model or prompt upgrade policy: any change to the pinned model or prompt version re-runs the full set before it ships; [name] owns the re-run
- Where results are recorded (dated, retrievable): [location]

## Worked micro-example

One filled row, to show the shape: metric "merchant-name extraction accuracy", defined as exact match against the labeled field, dataset `evals/merchant-names-v2` (140 cases, labeled by two ops agents with disagreements adjudicated), grader code, threshold 0.92 ILLUSTRATIVE, below threshold block release, owner J. Doe. The row is boring. That is the point; boring rows are runnable.

### Worked micro-example, agentic feature

For a feature that takes actions (files a ticket, updates a record, sends a draft),
grade the world, not the transcript: metric "ticket actually created", defined as
the ticket existing in the tracker with the required fields after the run, checked
by a code grader querying the tracker API. A transcript that says "I have created
the ticket" is the model reporting on itself, and self-report is exactly what fails
silently.

State which reliability question each threshold answers. Pass@k asks "can it do
this at all?": success counted if any of k attempts succeeds, the right frame for a
capability row. Pass^k asks "does it do this every time?": success only if all k
attempts succeed, the right frame for a regression row on an action users trigger
repeatedly, because a step that usually works compounds into a workflow that
regularly fails. Write "pass@k" or "pass^k" into the definition cell so the two are
never averaged into one flattering number.

## Exit gate

- [ ] Section 0 names how many traces were read, by whom, and the clusters found
- [ ] Every scenario in section 1 maps to a section 0 cluster or is labeled synthetic
- [ ] Metrics are split into a capability suite and a CI-gated regression suite, and only regression rows hard-block by default
- [ ] Every metric row has a definition, a grader type, a numeric threshold, a status label, a below-threshold action, and a named owner
- [ ] Every model-graded row that gates a release cites its validation against held-out human labels: precision, recall, and false-accept rate
- [ ] Agentic checks verify external state, and each definition states pass@k or pass^k
- [ ] The dataset location, size, and labeling method are stated, not implied
- [ ] Someone is named for feeding production failures back into the dataset
- [ ] The upgrade re-run rule is written and owned
