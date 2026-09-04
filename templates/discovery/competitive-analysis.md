---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/jobs-to-be-done.md"
aliases: ["Competitive Analysis", "competitive-analysis"]
---
# Competitive Analysis: [market or decision short name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Jobs to be done](../../knowledge/jobs-to-be-done.md)
Skill: [competitive-intel](../../skills/competitive-intel/SKILL.md)

<!-- Fill section 1 first, and stop if you cannot. A competitive analysis that does
     not name the decision it informs is a scrapbook: hours of screenshots, a
     feature grid nobody reads, and no decision changed. Section 1 is the only
     mandatory section in this file.

     Fill these three fields first, in this order: the decision in section 1, the
     job in section 2, and the so-what in section 6. Everything between them is
     evidence for those three.

     Delete any section you do not need. An empty section is worse than no
     section. Write "N/A because <reason>" where a section genuinely does not
     apply to this decision.

     Based on the ideas in Jobs to be Done, per Clayton Christensen, Tony Ulwick,
     and Bob Moesta: the competition is whatever the customer currently hires to
     make the same progress. That is often a spreadsheet, an agency, or doing
     nothing, and those belong in the table below alongside the named vendors. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Refresh by:** [YYYY-MM-DD, or "one-off for this decision"]

## 1. The decision this informs (mandatory)

- **Decision:** [the specific choice this analysis feeds, e.g. "whether to build our own payout rails or route through a provider for the Q1 launch"]
- **Decided by:** [name] · **Needed by:** [YYYY-MM-DD]
- **What would change the decision:** [the finding that flips it; write this before you research, so the research cannot quietly become confirmation]
- **Where the decision gets recorded:** [decision-log.md](../execution/decision-log.md)

<!-- If you cannot fill the first bullet with one concrete decision and a name,
     stop. Do the work when the decision exists. -->

## 2. The job and the current alternatives

<!-- Start from the job, not the vendor list. A competitor set assembled from
     the vendors you already know about will miss the alternative most users
     actually chose, which is frequently a spreadsheet, an internal script, or
     leaving the problem unsolved. -->


- **The job:** [what the customer is trying to get done, stated without naming any product]
- **What they hire today:** [the incumbent, the spreadsheet, the manual process, the nothing]

## 3. Competitor set

<!-- Five rows at most. A grid of fifteen vendors is a signal that section 1 is
     empty. Include at least one non-product alternative (manual process, in-house
     build, or doing nothing), because that is usually the real incumbent. -->

| # | Who | What they are for, in their words | Who they serve | Why they are in this set |
|---|---|---|---|---|
| C1 | | | | |
| C2 | | | | |
| C3 | doing nothing / the manual workaround | | | |

## 4. Evidence per competitor

<!-- Every claim carries a source and a date, because competitive facts rot faster
     than any other kind. "Their onboarding takes two weeks" is worthless without
     "signed up 2026-08-14, timed it". Secondhand claims from a sales deck are
     labeled as such, never laundered into fact. -->

| # | Claim | Source (used it / docs / pricing page / customer said / analyst) | Date checked | Confidence (high / medium / low) |
|---|---|---|---|---|
| | | | | |

## 5. Comparison on the axes that matter to the decision

<!-- Choose three to five axes that could actually change the decision in section 1.
     Do not compare on feature checklists. If an axis cannot move the decision, it
     does not earn a column. -->

| Axis (why it matters to the decision) | Us today | C1 | C2 | C3 |
|---|---|---|---|---|
| [axis 1] | | | | |
| [axis 2] | | | | |
| [axis 3] | | | | |

## 6. So what

<!-- The section that makes the rest worth writing. It commits to something:
     what changes in the plan, what does not, and what would have to be true
     for that to be wrong. An analysis whose conclusion is that the landscape
     is interesting has not finished. -->


- **What this says about the decision:** [two or three sentences, committed, not balanced]
- **Where we are genuinely behind, and whether it matters to this decision:** [honest, one or two lines]
- **What we will not copy, and why:** [the feature everyone will ask for after reading this]
- **Open questions that would change the answer:** [each with an owner and a date]

## 7. Worked micro-example (illustrative, invented; delete once real content exists)

<!-- Shows the evidence standard: a dated source per claim, and a named
     decision at the end. Delete it once real content exists. -->


> **Decision:** Whether the first release of a receipt-scanning feature ships our own extraction or a vendor's, decided by the product lead by the end of the month.
> **What would change it:** A vendor priced under our per-receipt cost ceiling that also allows an on-premises deployment for our regulated customers.
> **The job:** A field rep wants a filed expense to be accepted the first time, without typing.
> **What they hire today:** The phone camera plus manual entry, and for two of our largest accounts, an outsourced processing team.
> **So what:** Vendor A clears the accuracy axis and fails the residency axis, which is the axis with a contract behind it, so the first release routes through Vendor B and the residency question goes to legal with a date.

---

## 8. How this analysis fails

<!-- Every row produces a document that looks thorough and changes nothing.
     The last is the one that costs most, because the alternative most
     products actually lose to is not a competitor. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Feature checklist | Rows of features with ticks, no weighting, no user impact | Compare on the job the user is hiring for, not on counts |
| Cherry-picked set | Only the direct rivals appear, and not the tools users really consider | Include at least one non-obvious substitute per segment |
| Undated claims | "Market leader", or a screenshot with no source and no date | Every claim carries a source and the date it was retrieved |
| No decision attached | A long document ending in "more research needed" | Section 1 names the decision. If none, do not write this document |
| Copying their roadmap | The plan mirrors a rival's recent launches rather than your own thesis | Prioritise against your differentiation, not their shipping log |
| Ignoring the real alternative | A spreadsheet, a manual process, or doing nothing is never scored | Score the status quo as a first-class competitor. It usually wins |

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Checkable by someone who did not do the research. -->


- [ ] Section 1 names one decision, one decider, and one date
- [ ] The finding that would flip the decision was written before the research started
- [ ] The competitor set includes at least one non-product alternative
- [ ] Every claim carries a source and a date checked, with secondhand claims labeled
- [ ] Comparison axes are the ones that can move this decision, not a feature checklist
- [ ] The so-what section commits to a reading rather than listing both sides
- [ ] The analysis is linked from the decision log entry it fed
