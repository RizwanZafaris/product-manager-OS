---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/problem-framing.md", "templates/execution/decision-log.md", "frameworks/prioritization/now-next-later.md"]
method: "knowledge/INDEX.md"
aliases: ["Cynefin"]
---
# Cynefin

Based on the sense-making framework Cynthia Kurtz and Dave Snowden set out in the IBM Systems Journal (2003), and popularized by Snowden with Mary Boone in Harvard Business Review (November 2007). Explained here in this repository's own words.

The domain names used below are the current ones. The 2003 paper called the five known, knowable, complex, chaotic, and disorder, and the renaming happened later, so a citation to that paper will not carry the vocabulary on this page.

## What it is for

Deciding which method the problem in front of you can even support, before anyone runs one. Cynefin sorts a situation by what is knowable about cause and effect: **clear** (a rule exists and holds), **complicated** (no rule, but analysis or expertise will settle it), **complex** (the same action gives different outcomes and the pattern only reads in hindsight), **chaotic** (no discernible cause and effect, and harm is accruing now), and **confused** (the people in the room are each acting from a different domain and none of them knows it). Each domain has one action mode that works and several that produce confident nonsense. The meeting this ends is the one where a staff engineer wants an analysis, a designer wants a sprint, and a director wants a date, and all three are right about a different part of the problem. A clear-domain problem does not need a design sprint. A chaotic-domain problem must not wait for a roadmap.

## Run it when

- The team has argued for two sessions about which method to use, rather than about the answer.
- A sponsor is asking for a dated commitment on work whose outcome nobody can predict.
- An incident recurs after the runbook closed it, which means the problem was never clear.
- At every stage transition in the [operating loop](../../os/OPERATING-LOOP.md), because the domain shifts as evidence lands.

**Skip it when:** the work is a known change to a known system with a written procedure and a bored owner. You are already in the clear domain, you knew it before you read this, and scoring it is a meeting you owe nobody.

## Inputs you need first

- The problem written as a symptom or a decision, not a topic: "managers approve drafts without reading them," not "approvals."
- Two or three people who must act on the answer, scoring independently. One scorer produces one person's habit.
- The clock: what harm accrues, to whom, per week of study.
- What has already been tried, with outcomes. Repeat actions with different results are the strongest single signal.
- The [problem framing](../../templates/discovery/problem-framing.md) sheet if one exists, sections 1 to 3.

## The worksheet

### Step 1: state the problem and its clock

| Field | Entry |
|---|---|
| Problem, as a symptom or a decision | [one sentence] |
| Who must act | [role, not a name] |
| Harm per week of study | [what gets worse, and for whom] |
| Tried already, with outcome | [action, result, date] |

### Step 2: score the two axes, independently, then compare

<!-- Each scorer fills this alone before anyone speaks. Scores are 0 to 3 on both
     axes. Four steps, not ten: the only thing this output selects is which of five
     procedures applies, so a finer scale buys a 6.5 that maps to no procedure and
     invites the team to average its way out of a real disagreement. -->

**Axis K, cause and effect:**

| K | Meaning | Test |
|---|---|---|
| 3 | Known | A written rule exists and has held every time this year. Anyone trained applies it. |
| 2 | Knowable | No rule written, but a qualified expert with data that exists or can be gathered would settle it. |
| 1 | Only knowable afterwards | The same action has produced different outcomes. The pattern makes sense in retrospect and does not predict forward. |
| 0 | Absent | Nobody can say what is driving what right now. |

**Axis T, time available before you must act:**

| T | Meaning |
|---|---|
| 3 | No clock. A quarter of study costs nothing. |
| 2 | A quarter of runway. |
| 1 | Weeks. The situation moves while you study it. |
| 0 | Now. Harm accrues hourly and the ground shifts under the analysis. |

### Step 3: the arithmetic

There is no total and no average. The domain is read off K, and T can only make it worse.

| Rule | Domain |
|---|---|
| K = 3 | Clear |
| K = 2 | Complicated |
| K = 1 | Complex |
| K = 0 | Chaotic |
| Override: T = 0 and K of 2 or below | Chaotic, until you buy the clock back and re-score |
| Override: two scorers differ on K by 2 or more | Confused |

**Do not average K.** Two scorers at 3 and 1 average to 2, which sends the team to hire an expert for a problem one of them believes is emergent and the other believes is routine. That gap is the finding, not noise to be smoothed.

### Step 4: split the problem, because it is never one domain

<!-- Most real problems are three domains wearing one name. Split until each part
     scores cleanly, then run the mode each part earns. -->

| Part of the problem | K | T | Domain | Action mode | Instrument to run | Owner |
|---|---|---|---|---|---|---|
| | | | | | | |

### Step 5: the response table

| Domain | Action mode | What good looks like | Instruments that apply here | Actively harmful here |
|---|---|---|---|---|
| Clear | Sense, categorize, respond | The rule is written down, delegated, and audited by sample | [Business rules](../../templates/definition/business-rules.md), [acceptance criteria](../../templates/definition/acceptance-criteria.md), [support runbook](../../templates/delivery/support-runbook.md), [RACI](../execution/raci.md) | [Design sprint](../discovery/design-sprint-runbook.md) and [assumption mapping](../discovery/assumption-mapping.md): a week spent rediscovering a written rule |
| Complicated | Sense, analyze, respond | One expert analysis, a decision recorded, a range not a point | [Five whys and fishbone](../execution/five-whys-fishbone.md), [weighted decision matrix](../prioritization/weighted-decision-matrix.md), [build, buy, partner](../strategy/build-buy-partner.md), [estimation sheet](../execution/estimation-sheet.md), [ADR](../../templates/architecture/adr.md) | Probing for something the vendor's documentation already answers; treating the expert's answer as final once the system starts behaving differently |
| Complex | Probe, sense, respond | Several small safe-to-fail probes in parallel, each with a pass criterion fixed beforehand | [Assumption mapping](../discovery/assumption-mapping.md), [experiment brief](../../templates/operate/experiment-brief.md), [design sprint](../discovery/design-sprint-runbook.md), [Mom Test guide](../discovery/mom-test-interview-guide.md), [Now, Next, Later](../prioritization/now-next-later.md) | [RICE](../prioritization/rice-scoring-sheet.md) and [MoSCoW](../prioritization/moscow.md) against a fixed date: real arithmetic on invented reach; a dated [roadmap](../../templates/planning/roadmap.md) commitment in place of a probe |
| Chaotic | Act, sense, respond | Someone acts inside the hour to stop the bleeding, then the domain is re-scored | [Escalation](../../skills/escalation/SKILL.md), [failure scenarios](../../templates/delivery/failure-scenarios.md), [customer comms](../../templates/delivery/customer-comms.md), then [incident postmortem](../../templates/operate/incident-postmortem.md) | Any prioritization sheet, any gate review, any discovery round. Consensus-seeking is the specific failure: it costs the hour you had |
| Confused | Split and re-score | The parts are separated and each is scored on its own | Step 4 above, then this table again | Deciding anything. Every participant is applying the mode that fits their own domain and defending it as method |

## Reading the result

- **Clear.** Write the rule, delegate it, and sample the output. The risk is complacency: a clear process that stops working slides straight into chaos, because nobody was watching the rule, only following it.
- **Complicated.** Buy expertise, timebox the analysis, and record the decision with its basis. A range beats a point, and the estimation sheet's reference class beats a confident single number.
- **Complex.** Stop asking for the answer and start asking what the cheapest probe is. Multiple parallel probes, each cheap enough to fail without a postmortem. Commit to a cadence, never to a scope.
- **Chaotic.** Act. Any action that increases order is better than the right action taken tomorrow. Then re-score within the day, because chaos is a transit, not an address.
- **Confused.** The most common and least reported outcome. Split further.

Patterns worth naming: if every part scores complicated, the team is treating its own preference for analysis as a property of the world. If every part scores complex, someone is using emergence as a reason to avoid a commitment they could honestly make. If the same part scores clear one quarter and chaotic the next, the rule was never audited.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Two scorers, a product manager and an engineering lead. All scores ILLUSTRATIVE.

| Part | K | T | Domain | Mode | What we ran |
|---|---|---|---|---|---|
| VAT rate applied to a receipt from a country already in the policy table | 3, 3 | 3 | Clear | Categorize | A business rule and a sampled monthly audit; no discovery |
| Extraction latency triples in the last three days of the month | 2, 2 | 2 | Complicated | Analyze | Fishbone with the platform engineer, one week, then an ADR on the queue change |
| Managers approve drafted reports without reading them | 1, 1 | 2 | Complex | Probe | Three parallel probes: a reviewer sampling prompt, a confidence badge, a delayed submit. Pass criteria fixed beforehand |
| The extraction vendor suspended the account with 400 reports mid-flight | 0, 0 | 0 | Chaotic | Act | Failover to manual entry within the hour, filers told the same day, postmortem the next |
| "Copilot adoption is bad" | 3, 1 | 2 | Confused | Split | The engineering lead read a known onboarding defect, the product manager read unexplained abandonment. Both were present. Split into two parts and re-scored |

The last row is the sheet earning its cost. Averaging 3 and 1 to a 2 would have bought a fortnight of analysis on the half of the problem that was already fixable and none on the half that needed probes.

## The decision it feeds

What the team spends its next two weeks on, and whether a dated commitment can honestly be made at all. Concretely: a runbook entry and a rule, or one timeboxed expert analysis, or a set of parallel probes with no promised scope, or an incident response starting now. It also settles who decides, since the clear and complicated parts delegate cleanly and the complex parts cannot be delegated to an expert who does not exist.

## Where the output lands

- [Problem framing](../../templates/discovery/problem-framing.md), section 7 (constraints on any resolution) and section 8 (decision requested): the domain call is a constraint on what a resolution can promise.
- [Decision log](../../templates/execution/decision-log.md): one entry per domain call, with the date, both scores, and the disagreement if there was one.

## Re-run trigger

**Re-run when the answer to the K question changes: a probe settles what was unknowable, a clear process fails in a way its runbook cannot close, an expert analysis returns without an answer, or the system changes shape (a vendor, a regulation, a reorganization, a tenfold change in volume). Absent any of those, re-run at every stage transition and at the start of each planning period.**

A domain call with no re-run trigger becomes a label the team defends. The whole point of the framework is that problems move, and mostly they move because you acted.

## When this method misleads you

The framework is a sense-making aid, not a classifier, and it fails in three specific ways. First, retrospective coherence: after a complex problem resolves, the causal chain looks obvious, so the team scores the next one complicated and buys an analysis that cannot work. Second, domain preference dressed as diagnosis: an analytical organization scores everything a 2 and a founder-led one scores everything a 1, and because both scores are single-digit and quick, neither gets challenged. Independent scoring by people with different jobs is the only cheap defence. Third, chaos by choice: a team that likes acting scores T as 0 to skip the analysis, when the truth is that a week of study was available and nobody wanted to sit through it. Ask what specifically gets worse in that week, name it, and the T score usually rises. And if a single scorer fills this sheet alone, it produces a confident domain, a matching instrument, and no information at all: it will return the domain that scorer already preferred, with a table attached.

## Feeds

- [Problem framing](../../templates/discovery/problem-framing.md) and the [decision log](../../templates/execution/decision-log.md), as above
- [Now, Next, Later](../prioritization/now-next-later.md): complex parts belong in Next or Later with a probe, never in Now with a date
- [Experiment brief](../../templates/operate/experiment-brief.md) and [assumption mapping](../discovery/assumption-mapping.md) for every complex part; the [experiment-designer skill](../../skills/experiment-designer/SKILL.md) when a probe outgrows a card
- [Decision doors](../prioritization/decision-doors.md): the domain sets how much process the decision deserves, and reversibility sets the rest
- [Risk matrix](../execution/risk-matrix.md): a complex part scored with a confident likelihood is the misuse that sheet's own trap describes
- [Gate 1: problem worth solving](../../os/STAGE-GATES.md) and Gate 3, whose checklists assume the problem has been framed well enough to name a method
- [Iceberg model](iceberg-model.md): the companion diagnostic. Cynefin says which method the problem can support; the iceberg says which layer of the system the problem lives in
- Method background: [knowledge index](../../knowledge/INDEX.md)
