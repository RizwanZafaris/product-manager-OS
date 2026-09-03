# Metrics Review: [product or feature name]

**Stage:** OPERATE (this file feeds [Gate 6: outcomes verified, learn or sunset](../../os/STAGE-GATES.md))
**Knowledge:** [north star metric](../../knowledge/north-star-metric.md)
**Skill:** [product-review](../../skills/product-review/SKILL.md); the [analyst agent](../../agents/analyst-agent.md) prepares the numbers

<!-- This is the review the loop exists for: did the outcome move, and what do we do
     about it? Run it on a fixed cadence after launch, not "when we get around to it".
     The metric structure follows the north star model, one value metric fed by input
     metrics, based on the ideas popularized by Sean Ellis and by Amplitude's
     framework; the knowledge card linked above covers the vanity-metric trap.

     Honesty rule: a number without a confidence note is a rumor. Say how sure you
     are of the data before you argue about what it means. -->

**Owner:** [name] · **Review window:** [YYYY-MM-DD] to [YYYY-MM-DD] · **Cadence:** [e.g. every 4 weeks]
**Linked OKR sheet:** [../planning/okrs.md copy for this product]

## 1. Outcome vs target, per key result

<!-- Copy each key result from the OKR sheet. Do not invent new ones here; if the KRs
     were wrong, that is a finding for section 4. The italic row shows a completed entry. -->

| Key result | Baseline | Target | Actual this window | Delta | Data confidence (high / medium / low, why) |
|---|---|---|---|---|---|
| | | | | | |
| *first-submission approval rate* | *62%* | *80%* | *71%* | *+9 pts, short of target* | *high, finance system of record* |

## 2. Input metric movement

<!-- Input metrics explain the outcome row above. If an input moved and the outcome
     did not, the causal story in the strategy is wrong somewhere. Say so. -->

| Input metric | Prior window | This window | Expected to drive | Did it? |
|---|---|---|---|---|
| | | | [which KR] | yes / no / unclear |

## 3. Counter-metrics and guardrails

<!-- What we refuse to sacrifice for the headline. A win that trashed a guardrail is
     not a win. -->

| Guardrail metric | Threshold | This window | Breached? |
|---|---|---|---|
| | | | yes / no |

## 4. What we predicted vs what happened

<!-- The retro section. Pull the load-bearing assumptions from
     ../definition/assumptions-register.md and grade them. This table is where the
     team actually learns; skipping it turns the review into a scoreboard. -->

| Assumption or prediction at launch | What actually happened | Held / Broke | What we change because of it |
|---|---|---|---|
| | | | |

- The most surprising thing in the data this window: [one sentence]
- What we will stop doing, based on the above: [one item, or "nothing, and here is why"]

## 5. Decision

<!-- One of three words, with a named decider. "Keep watching" is only legal with a
     date on it, otherwise it is sunset denial. -->

- **Decision:** PERSIST / PIVOT / SUNSET
  - Persist: outcomes are moving toward target; continue and set the next review date
  - Pivot: the problem is real but this approach is not working; name what changes and take it back to DISCOVER
  - Sunset: the outcome is not worth the ongoing cost; name the wind-down owner and date
- Decider: [name] · Date: [YYYY-MM-DD]
- If persist: next review date: [YYYY-MM-DD]
- If pivot: what changes, and the new discovery document: [link to the new ../discovery/discovery-document.md copy]
- If sunset: wind-down owner, user migration plan, and shutdown date: [name, plan, date]

## Exit gate

Gate 6 is satisfied when:

- [ ] Every KR row has an actual and a data-confidence note
- [ ] Input metrics are mapped to the KRs they were supposed to drive, with an honest "did it?"
- [ ] Guardrail metrics are reported, including breaches
- [ ] Section 4 grades real launch assumptions, not retrofitted ones
- [ ] The decision is one of the three words, with a named decider and the follow-through fields filled

Signed: [name], [role], [YYYY-MM-DD]
