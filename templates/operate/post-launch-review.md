---
layer: templates
stage: OPERATE
gate: 6
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Post-Launch Review", "post-launch-review"]
---
# Post-Launch Review: [launch name]

**Stage:** OPERATE (feeds [Gate 6: outcomes verified, learn or sunset](../../os/STAGE-GATES.md)); an event review, run once per launch. The recurring instrument is [metrics-review.md](metrics-review.md)
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [product-review](../../skills/product-review/SKILL.md)

<!-- Two review templates live in this directory and they answer different
     questions. The metrics review runs on a cadence forever and asks "is the
     outcome moving?". This one runs once, [2 to 6] weeks after a specific launch,
     and asks "did this launch do what we said at Gate 5, and what did shipping it
     teach us?". Running it later than six weeks means the people who remember why
     decisions were made have moved on to the next thing.

     Section 5 is the bookend to the premortem (Gary Klein's exercise, indexed in
     the knowledge layer) run before Gate 3: the premortem predicted failures in
     advance, and this review checks which ones arrived. A team that never
     reconciles the two is guessing twice. -->

**Owner:** [name] · **Launch date:** [YYYY-MM-DD] · **Review date:** [YYYY-MM-DD]
**Inputs:** [release-readiness copy] · [gtm-plan copy] · [launch dashboard link]

## 1. Launch facts

<!-- Facts first and separately, because the argument that follows depends
     on them and they are the part people misremember. Dates, scope actually
     shipped, and the target as it was written before launch, not as it is
     remembered now. -->


- What shipped, one sentence: [sentence]
- The one launch metric from the GTM plan: [metric] · Stop condition set then: [condition]
- Rollout shape as it actually happened: [including anything staged, delayed, or rolled back]

## 2. Goal vs actual

<!-- Targets are the ones written at Gate 5, quoted, not remembered. Retrofitted
     targets make every launch a success and every review worthless. -->

| Metric | Target at Gate 5 (quoted from doc) | Actual at review | Delta | Data confidence |
|---|---|---|---|---|
| | | | | |

## 3. What worked, what did not

<!-- Both lists cover the product AND the process of shipping it. Each item names
     its evidence; an item without evidence is a mood. -->

- Worked: [item, evidence]
- Did not: [item, evidence]
- Would do differently next launch: [one item, specific enough to actually do]

## 4. Customer feedback

<!-- Quote verbatim, and count. A review that paraphrases feedback into
     agreement with the team's existing view is the most common way a launch
     teaches nothing. Include the complaint nobody wants to read. -->


| Source (tickets / interviews / reviews / sales) | Theme | Count | One verbatim quote |
|---|---|---|---|
| | | | |

- The feedback we expected but did not get: [what, and what that might mean]

## 5. Premortem reconciliation

<!-- Pull the failure modes from the premortem run before Gate 3. Three columns of
     honesty: predicted and arrived, predicted and did not, arrived unpredicted. -->

| Failure mode | Predicted? | Arrived? | What we change because of it |
|---|---|---|---|
| | yes / no | yes / no | |

## 6. Follow-ups

<!-- Every row lands in a living document or a tracker, not in this file. This
     review closes; its outputs move out. -->

| Item | Lands in (linked doc or ticket) | Owner | Date |
|---|---|---|---|
| | | | |

## How this review fails

<!-- Each row produces a review that happened and changed nothing. The first
     two are the same failure in different clothes: a review that cannot
     record a miss is a ceremony, and a target that moves after the result is
     known is a way of never recording one. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Only the wins are reviewed | Every section reports something that went well | Name at least one thing that came in under its target, or the review is not finished |
| The target moved after the fact | "What we really wanted was a smaller number", said afterwards | The target and the definition of success are locked before launch and quoted here unchanged |
| Everything is attributed to the launch | Any movement in the period is credited to the release | State what the metric would plausibly have done anyway, and say how confident you are |
| Nothing is decided | The document ends in thanks and a list of observations | Close with named owners, dated actions, and a date to re-check |
| Held too late to remember | Six weeks after launch, and nobody can recall what shipped | Hold it within about two weeks of the launch window closing |
| Blame lands on a person | The review names who missed rather than what allowed the miss | Name the step in the process that permitted it, and the change to that step |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- A review that records a miss and produces a decision, which is the shape
     the rows above are asking for. Delete once real content exists. -->

| Target, as written before launch | Actual | Verdict |
|---|---|---|
| *Median filing time under 3 minutes* | *2m 55s* | *met* |
| *First-time acceptance rate up by a fifth* | *up by about a twentieth* | ***missed*** |
| *Manual entry fallback under one in ten submissions* | *one in four* | ***missed, and worse than the pre-launch rate*** |

*What we would have seen anyway: filing time was already falling before launch as the pilot cohort learned the old form. Perhaps a third of that gain is not ours.*

*Cause, as far as we know: extraction fails on low-light photographs more often than the labelled test set predicted, because the test set was photographed indoors. We did not know this and did not test for it.*

*Decisions: S. Kaur rebuilds the test set from real submitted photographs by 20 July. Second market launch holds until the fallback rate is under one in ten, decided by R. Ali. Re-review 14 August.*

The second and third rows are why the review was worth holding. A version that reported only the first row would have been accurate, celebratory, and would have sent the team into a second market with a defect it had not found.

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


This review is done when:

- [ ] Every target in section 2 is quoted from a Gate 5 era document
- [ ] Worked and did-not lists both have entries with evidence, covering product and process
- [ ] The premortem table has a row for every arrived failure, predicted or not
- [ ] Every follow-up has left this file for an owned destination
- [ ] The recurring [metrics review](metrics-review.md) cadence is scheduled, with its first date set

Signed: [name], [role], [YYYY-MM-DD]
