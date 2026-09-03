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

## Exit gate

This review is done when:

- [ ] Every target in section 2 is quoted from a Gate 5 era document
- [ ] Worked and did-not lists both have entries with evidence, covering product and process
- [ ] The premortem table has a row for every arrived failure, predicted or not
- [ ] Every follow-up has left this file for an owned destination
- [ ] The recurring [metrics review](metrics-review.md) cadence is scheduled, with its first date set

Signed: [name], [role], [YYYY-MM-DD]
