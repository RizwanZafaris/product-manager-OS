---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/torres-continuous-discovery.md"
aliases: ["Discovery Document", "discovery-document"]
---
# Discovery Document: [product or initiative name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Continuous discovery](../../knowledge/torres-continuous-discovery.md)
Skill: [feedback-synthesis](../../skills/feedback-synthesis/SKILL.md)

<!-- The one-page record of why this work exists. Fill it before anyone writes a
     requirement, a design, or a line of code. If you cannot fill it, that is the
     finding: you have a solution looking for a problem.

     Based on the ideas in Continuous Discovery Habits by Teresa Torres: discovery
     is a weekly habit that keeps decisions tied to real customer contact, not a
     phase that ends. This document is the durable snapshot of where that contact
     has led you so far.

     Rules for filling it in:
     - Every claim of pain needs a source: an interview ID, a support ticket, a
       metric. "Everyone knows" is not a source.
     - Write "unknown" where you do not know. An honest unknown becomes a research
       question; a confident guess becomes a dead roadmap item.
     - Square brackets mark fill-in fields. Replace the whole bracket. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Decided

## 1. Trigger

[What put this on the table: a customer signal, a metric movement, a strategic bet, a competitor move, an executive request. One or two sentences. Name the actual event, with a date.]

<!-- "Leadership wants it" is a real trigger; write it down honestly. A discovery
     document that hides its trigger hides its bias. -->

## 2. Target user

- **Who, specifically:** [segment, role, or archetype; link the persona file if one exists: ../discovery/personas.md]
- **How many of them:** [count or estimate, with the source of the estimate]
- **How we reached them so far:** [interviews held, tickets read, analytics reviewed; give counts and IDs]
- **Markets, jurisdictions, and locales in scope:** [the countries or regions this pass covers, the languages and currencies involved, and any regulator or scheme with a claim on it; write "one market: [name]" if that is the honest answer]

<!-- The jurisdiction line is asked here, at the front, because it changes what
     the rest of the loop demands. A second market brings its own rules, its own
     payment or identity rails, and often its own regulator, and finding that out
     at Gate 5 is the expensive way. If a financial or data regulator applies to
     any market listed AND the product contains an AI or machine-learning
     feature, the regulated overlay activates at Gate 2: see
     ../../os/STAGE-GATES.md for the rule, which governs, and
     ../../modules/regulated/README.md for the module. A regulated product with
     no model in it does not activate it. Full analysis lives in
     ../operate/compliance-impact-assessment.md, not here. -->


## 3. The pain

[Describe the problem in the user's terms, not the product's terms. What are they trying to get done, where does it break, what does the workaround cost them today? Two to five sentences.]

**Evidence:**

| # | Evidence item | Type (interview / ticket / metric / observation) | Source or ID | Date |
|---|---|---|---|---|
| 1 | [what was seen or said, in your words] | [type] | [ID or link] | [date] |
| 2 | | | | |
| 3 | | | | |

<!-- Three or more independent items before Gate 1. One loud customer is an
     anecdote. Anecdotes start discovery; they do not finish it. -->

## 4. Hypothesis

> We believe that [building or changing X] for [target user] will [change in user behavior or outcome], and we will know because [observable signal] moves from [baseline] to [target] within [period].

<!-- One sentence, falsifiable, with a number at each end. If you cannot state the
     baseline, your first task is measurement, not building. -->

## 5. Success signal

- **Leading signal (weeks):** [metric or behavior that moves first, and the threshold that means "keep going"]
- **Lagging signal (months):** [the outcome that justifies the investment]
- **Kill signal:** [the observation that would tell you to stop; write it now, while you are still neutral]

## 6. What we are NOT doing

[Adjacent problems, segments, or solutions deliberately out of scope for this pass, and one line each on why. This section prevents scope creep from re-litigating settled ground.]

## 7. Go or no-go

- **Decision:** GO / NO-GO / MORE DISCOVERY
- **Decided by:** [name] · **Date:** [YYYY-MM-DD]
- **Rationale:** [two or three sentences: which evidence carried the decision]
- **If GO:** the next artifact is [problem-framing.md](problem-framing.md), then the DEFINE stage.
- **If MORE DISCOVERY:** the open questions go into [user-research-plan.md](user-research-plan.md) with a revisit date: [date]

---

### Worked micro-example (illustrative, invented)

> **Trigger:** Support logged 41 tickets in March tagged "expense report rejected", up from 12 in February.
> **Target user:** Field sales reps who file expenses weekly from a phone, roughly 800 across three regions per the HR headcount export.
> **Pain:** Reps photograph receipts at day's end, half the photos fail validation, and resubmission takes two days, so reps batch a month at a time and finance closes late.
> **Hypothesis:** We believe that validating receipt photos at capture time for field reps will cut failed submissions, and we will know because first-pass acceptance moves from 55% to 80% (both numbers illustrative) within one quarter.
> **Kill signal:** Reps who see the validation prompt still submit failing photos at the same rate after two weeks.

---

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Check honestly. An unchecked box here is a reason to stay in DISCOVER, not a
     formality to tick. Gate 1 itself lives in os/STAGE-GATES.md. -->

- [ ] Trigger is named, with a date, including any political trigger
- [ ] Target user is specific enough that a stranger could find five of them
- [ ] Markets and jurisdictions are named, and the regulated-overlay question is answered either way
- [ ] Three or more independent evidence items, each with a source ID
- [ ] Hypothesis is falsifiable and carries a baseline and a target
- [ ] A kill signal is written down
- [ ] The go or no-go decision has a name and a date on it
