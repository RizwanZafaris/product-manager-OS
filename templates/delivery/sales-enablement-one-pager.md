---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: ""
aliases: ["Sales Enablement One-Pager", "sales-enablement-one-pager"]
---
# Sales Enablement One-Pager: [product or feature name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md)
Knowledge: [Positioning canvas worksheet](../../frameworks/strategy/positioning-canvas.md)
Skill: [pmm-agent](../../agents/pmm-agent.md)

> **Delete any section you do not need.** A feature with no pricing change and no new buyer needs sections 1, 3, and 4 only. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- A derived document. Everything here comes from ../planning/positioning.md
     (alternatives, attributes, value, segment, category), ../planning/gtm-plan.md
     (beachhead and launch sequence), ../planning/pricing-packaging.md (price),
     and the sales row of launch-comms-plan.md (when the field hears). If this
     page says anything those do not, one of them is wrong, and it is usually
     this one. It fits on one page because a rep reads it between calls. Fill
     section 1 and the proof table first; a claim without proof does not go on
     the page. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Derived from:** [positioning.md version and date] · **Valid until:** [YYYY-MM-DD, or the next pricing change]

## 1. Who it is for

<!-- From positioning.md section 4. Precise enough that a rep can disqualify in
     one question. -->

| Field | Answer |
|---|---|
| Best-fit buyer | [role, company shape, in one line] |
| Trigger events that make them care now | [two or three observable events] |
| One question that qualifies them | [the question, and the answer that means yes] |
| Who this is NOT for, and what to offer them instead | [segments, with the honest alternative] |

## 2. Pains and the alternative

<!-- In the customer's words, with the evidence note behind each. A pain the rep
     cannot say out loud to a customer is not a pain, it is a slide. -->

| Pain, as the customer says it | What they do today instead | What that costs them | Evidence (interview or evidence-note id) |
|---|---|---|---|
| | | | |

## 3. What it does, with proof

<!-- One row per claim. Proof is a measured result, a named reference customer
     who has consented, or a demo the rep can run live. Unproven claims stay on
     this page only as "unproven" and never reach a customer. -->

| Claim, in one sentence | Proof | Status |
|---|---|---|
| | | proven / unproven |

**The one sentence a rep should say first:** [from positioning.md: the value that is urgent for the best-fit segment]

## 4. Objections

<!-- Collected from real calls and win-loss reviews, hardest first. The "do not
     say" column exists because the tempting answer is usually the one that
     creates a support ticket or a legal question later. The italic row is an
     invented example on the expense copilot. -->

| Objection | Honest answer | Proof or pointer | Do not say |
|---|---|---|---|
| | | | |
| *"Does it read our receipts correctly?"* | *it proposes fields with a confidence flag; the submitter confirms before anything is filed* | *demo step 3; findings in the filled usability-test-plan.md* | *"it is always right"* |

## 5. Pricing pointer

<!-- No numbers on this page. Prices change; the page does not get reprinted.
     Point to the source and name who may quote. -->

- Tier or package this sits in: [name, from pricing-packaging.md]
- Value metric it is priced on: [seats, submissions, entities]
- Where the current price list lives: [link or document id]
- Who may quote, and discount authority: [role, limit, escalation for exceptions]
- What is NOT included and costs extra: [list, so it is never a surprise on the invoice]

## 6. Demo path

<!-- The shortest path that shows the value in section 3, in the order the buyer
     cares about. Name what to avoid: the feature that looks impressive and
     raises an objection you cannot yet answer. -->

| Step | What to show | What to say | What to avoid | Time |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Demo environment and data:** [link, who resets it, which invented company it uses]

## 7. Where to send people

- Product questions during a deal: [name, channel]
- Security and privacy questionnaires: [owner; the filled ../architecture/privacy-impact-assessment.md and security-architecture.md are the sources]
- Feature requests from prospects: [intake route, feeding ../operate/feedback-program.md]
- Lost deals: [win-loss review owner; every loss gets a row in ../operate/win-loss-review.md]

## Exit gate (feeds Gate 5: release readiness green)

A signed page satisfies the sales line in section 4 of [launch-comms-plan.md](launch-comms-plan.md) and the field-readiness checkbox at [Gate 5](../../os/STAGE-GATES.md).

- [ ] Every line traces to positioning.md, gtm-plan.md, pricing-packaging.md, or the launch comms plan; nothing is invented here
- [ ] Every claim carries proof or is marked unproven, and unproven claims are absent from the demo path
- [ ] Every objection has an honest answer and a "do not say"
- [ ] The pricing section holds pointers and authority, no numbers
- [ ] A rep has read it and could disqualify a prospect with the section 1 question
- [ ] Signed by [name], [date]
