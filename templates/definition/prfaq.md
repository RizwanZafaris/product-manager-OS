---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/amazon-pr-faq.md"
aliases: ["PR/FAQ", "prfaq"]
---
# PR/FAQ: [product or feature name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Amazon PR/FAQ](../../knowledge/amazon-pr-faq.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md)

<!-- The working-backwards method as practiced at Amazon, described by Colin Bryar
     and Bill Carr in Working Backwards and restated here in this repository's own
     words: write the launch press release and the hard-question FAQ before the
     product exists, so the argument about whether this is worth building happens on
     one page instead of in a codebase.

     The knowledge card names the trap: a PR/FAQ written to sell a decision already
     made. The defense is the internal FAQ, which must contain the questions the
     authors hope nobody asks. A PR/FAQ whose internal FAQ has no uncomfortable
     entries has not been reviewed, it has been admired.

     Weight guidance: this sits beside the [PRD](prd.md) as a DEFINE artifact, best
     for new products and bets where the customer story is the contested part. It
     does not replace the PRD; a green-lit PR/FAQ feeds one. Keep the press release
     to one page. Plain language throughout: if a sentence would embarrass you in an
     actual press release, it does not belong in this one. -->

**Owner:** [name] · **Last updated:** [YYYY-MM-DD] · **Status:** [draft / reviewed / green-lit / parked]

## 1. Press release

<!-- Dated the day of the imagined launch. Customer's problem first, product second.
     Every claim in it must be one the team is prepared to make true. -->

- **Headline:** [what shipped, for whom, in one line a journalist would keep]
- **Subheading:** [the customer and the benefit, one sentence]
- **Location and imagined date:** [city, YYYY-MM-DD of the future launch]

[Opening paragraph: what launched and the problem it removes, four sentences maximum.]

[Problem paragraph: the customer's situation today, in their terms. What they do now, what it costs them.]

[Solution paragraph: how the product removes that cost. Capabilities in plain words, no internal jargon.]

> "[Customer quote: a named, plausible customer describing the progress they made. Write what you hope a real customer will say, and treat it as a commitment.]"

[How to get started: the first step a customer takes, in one paragraph.]

## 2. External FAQ

<!-- The questions customers and press will actually ask: price, availability, data,
     migration, what happens to the old thing. Honest answers only; an evasive
     answer here is a requirement you have not written yet. -->

| Question | Answer |
|---|---|
| [How much does it cost?] | |
| [Who can use it at launch?] | |
| [What happens to my existing data / workflow?] | |
| | |

## 3. Internal FAQ

<!-- The hard questions, on the record. Sizing, why-us, what must be true, what we
     kill to fund this, the failure modes. Each answer cites evidence or admits it is
     a judgment call. This section is where the green-light decision actually lives. -->

| Question | Answer, with evidence or an honest "judgment call" |
|---|---|
| [How big is this, and how do we know?] | |
| [Why are we the right team to build it?] | |
| [What must be true for the launch story above to happen?] | |
| [What are we choosing not to do to fund this?] | |
| [What is the most likely way this fails?] | |
| | |

## 4. Availability

| Field | Answer |
|---|---|
| Imagined launch window | [period, not a promise] |
| Launch scope | [segments, regions, platforms at day one] |
| Explicitly not at launch | [deferred scope, so day-one reviews are honest] |

## Exit gate

This PR/FAQ is fit for a green-light review when:

- [ ] The press release fits one page and leads with the customer's problem
- [ ] The customer quote describes progress a real customer could plausibly claim
- [ ] Every external FAQ answer is honest enough to publish as written
- [ ] The internal FAQ contains at least two questions the authors would rather not answer
- [ ] Every internal answer cites evidence or is marked a judgment call
- [ ] A reviewer who read only this document could argue against the product, which means it gave them the material to

Signed: [name], [role], [YYYY-MM-DD]
