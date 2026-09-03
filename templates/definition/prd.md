---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/cagan-product-teams.md"
aliases: ["PRD", "Product Requirements Document"]
---
# Product Requirements Document: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Cagan on product teams](../../knowledge/cagan-product-teams.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md); [ai-prd](../../skills/ai-prd/SKILL.md) when a model produces the output

> **Sections 0 to 13 are the spine. Section 13 pulls in the rest.** Fill the spine for
> every product. Then use the companion table in section 13 to pull in only the
> documents this product actually needs, rather than growing this one until nobody
> reads it. Most of the length below is guidance in HTML comments, which you strip
> when you publish; a filled PRD is far shorter than this blank.
>
> **Delete what does not apply.** An empty heading is worse than no heading: it reads
> as an unanswered question and it teaches readers to skim. Delete it, or write
> "N/A because <reason>". Never leave a heading standing over white space.
>
> **Is a full PRD the right weight?** A change one squad ships in a few sprints belongs
> in [one-pager.md](one-pager.md); a sprint of work behind a flag belongs in a ticket
> with acceptance criteria attached. [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md)
> decides in three questions. Pick the weight before you write a word.

<!-- The general-purpose PRD for this OS. It states what the product does, how you
     will know it worked, and what would make you stop. The why-fund-it case lives
     in brd.md; the how-it-is-built lives in the architecture templates; the
     function-by-function detail lives in frd.md.

     Fill four fields first, in this order: the objectives table in section 2, the
     out-of-scope table in section 7, the kill criteria in section 9, and the four
     risks in section 10. A PRD with those four answered is already useful; the rest
     is detail. Note that out-of-scope comes before scope on purpose. Exclusions are
     cheap to argue about now and expensive to argue about in week six.

     Based on the ideas of Marty Cagan, from Inspired (2008): a spec is only as good as
     its answers to the four risks: will they use it (value), can they use it
     (usability), can we build it (feasibility), does it work for the business
     (viability). Section 10 forces each risk to a named answer with its strongest
     counter-evidence attached.

     Two overlays extend this document:
     - Product contains a model: add the AI overlay, starting with
       ../ai/eval-spec.md, because acceptance criteria for model behavior are eval
       sets, not sentences. Stop and use ../../skills/ai-prd/SKILL.md instead.
     - Product contains an AI or machine-learning feature AND a financial or
       data regulator applies to it: the regulated module governs; see
       ../../modules/regulated/README.md and use its template as shipped,
       unmodified. Both halves are required, and ../../os/STAGE-GATES.md holds
       the rule and what a regulated product with no model brings instead. -->

**Owner:** [name] · **Engineering lead:** [name] · **Design lead:** [name]
**Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved · **Version:** [n]
**Who implements this:** [a human engineering team / a model, which routes this document to [ai-prd](../../skills/ai-prd/SKILL.md)]
**Links:** [BRD](brd.md) · [problem framing](../discovery/problem-framing.md) · [FRD](frd.md) · [assumptions](assumptions-register.md)

<!-- "Who implements this" is not a formality. A human reader resolves an ambiguous
     sentence with judgment and asks you at standup. A model resolves it with a guess
     you never see. If the answer is "a model", the acceptance criteria in this
     document have to be executable, and that is a different skill. -->

## 0. The one read

<!-- Write this last, put it first, keep it under 150 words. Assume most of your
     readers will read this section and skim the rest. This section is what they
     get, so it has to be true on its own. If it
     cannot be written honestly in 150 words, the product is not yet understood.

     Five sentences, in this order: the problem and who has it; what ships; the one
     number that says it worked; the one thing this deliberately does not do; the
     condition under which we stop. -->

**Problem:** [who has it, and what it costs them today]
**What ships:** [one sentence, in user terms, not component terms]
**Success looks like:** [the single number from section 2 that settles it]
**Deliberately not doing:** [the exclusion most likely to be assumed in]
**We stop if:** [the first row of section 9]

## 1. Background

[Three to six sentences: the problem, who has it, and the evidence weight behind it.
Link, do not restate; the discovery file is the source of truth. End with the
hypothesis this product tests, copied from the discovery document.]

<!-- If this section is being written from memory rather than from a discovery file,
     stop. A PRD written instead of the discovery work, rather than after it, is the
     most common and most expensive failure in this whole system. Go and do the
     DISCOVER stage. -->

## 2. Objectives

| # | Objective | Metric | Baseline | Target | Metric owner | Measured where |
|---|---|---|---|---|---|---|
| O1 | | | | | | |
| O2 | | | | | | |

<!-- Objectives are outcomes in user or business terms, never "ship X". A target
     nobody has agreed with the metric owner is labeled ILLUSTRATIVE until agreed,
     and an ILLUSTRATIVE target cannot pass Gate 2.

     Fill this table before section 4. A feature list with no objective above it is
     a wish list with row numbers. -->

## 3. Users and stories

**Primary persona:** [link to a persona block in ../discovery/personas.md]

| # | Story | Persona | Priority (must / should / later) | Acceptance criteria ID |
|---|---|---|---|---|
| US1 | As a [persona], I want [action], so that [outcome]. | | must | AC-[n] in [acceptance-criteria.md](acceptance-criteria.md) |
| US2 | | | | |

<!-- Every "must" story needs an acceptance criteria ID before Gate 2. A must
     without testable acceptance is a hope, not a requirement. The IDs here (US1,
     US2) are quoted by the FRD, the test plan, and the release readiness pack, so
     they never get renumbered once this document is circulated. -->

## 4. Functional scope

| # | Capability | What it does, in one sentence | Story it serves | Detail |
|---|---|---|---|---|
| F1 | | | US[n] | FR-[n] in [frd.md](frd.md) |

<!-- This table is the contract of record for WHAT ships. The FRD decomposes each
     row; if the two disagree, this table wins and the FRD gets fixed. Scope creep
     almost always enters through the FRD, never through here, which is why the
     precedence rule is written down. -->

## 5. Non-functional summary

[One paragraph naming the binding non-functional constraints. The latency,
availability, scale, security, accessibility, and retention targets live in nfr.md
with numbers and owners. Name here only the ones that shape scope, for example
"must work offline in the field".]

Full register: [nfr.md](nfr.md) · Accessibility: [accessibility-checklist.md](../architecture/accessibility-checklist.md)

## 6. Success metrics and instrumentation

| Metric | Type (leading / lagging / guardrail) | Instrumented where | Owner | Reviewed when |
|---|---|---|---|---|
| | | | | |

<!-- A guardrail metric is one this product must NOT damage: support ticket volume,
     page load elsewhere, refund rate, churn in the segment you did not target.
     Every launch needs at least one, and it is the metric that tells you whether
     the win was real or borrowed from somewhere else in the system.

     If the instrumentation does not exist yet, building it is functional scope: add
     the row to section 4 and write the event spec in
     ../delivery/analytics-instrumentation-spec.md. A metric with no instrumented
     source is a metric you will argue about in the review instead of reading. -->

## 7. Out of scope

| # | Excluded | Why | Where it went (backlog / never / other team) |
|---|---|---|---|
| X1 | | | |

<!-- Fill this before section 4. Two reasons.

     The first is old: exclusions are cheap to argue about now and expensive in week
     six, and the argument you avoid here happens later at ten times the cost.

     The second is new. When a model implements the spec, an unstated exclusion is
     not a gap the reader notices and asks about; it is an invitation. Anything you
     did not exclude is something an implementer may attempt. That turns this table
     from a scope note into a boundary.

     Include the exclusions people will assume in, not just the ones somebody
     proposed. "No bulk import" belongs here even if nobody asked for bulk import. -->

## 8. Launch criteria

| # | Criterion | Verified by (artifact or test) | Owner |
|---|---|---|---|
| L1 | All "must" stories pass their acceptance criteria | [acceptance-criteria.md](acceptance-criteria.md) | |
| L2 | Non-functional targets met or waived by their owner | [nfr.md](nfr.md) | |
| L3 | [rollback tested / support briefed / docs live / add your own] | | |

<!-- The conditions under which this ships. These become Gate 4 and Gate 5 inputs;
     the delivery templates verify them. Anything unmeasurable here will be argued
     about in the launch meeting, so make every row checkable by a named person. -->

## 9. Kill criteria

| # | We stop or roll back if | Threshold | Checked when | Who calls it |
|---|---|---|---|---|
| K1 | [the leading metric does not move] | [number, with the unit and the baseline it is measured against] | [date or milestone] | [name] |
| K2 | [the guardrail metric degrades] | | | |
| K3 | [the enabling assumption busts] | [the row ID in [assumptions-register.md](assumptions-register.md) moves to BUSTED] | | |

<!-- Read this before deciding you do not need it.

     Every product document names the conditions for shipping. Almost none names the
     conditions for stopping, and the result is predictable: nobody pulls the plug,
     because nobody ever agreed what would justify it. The team then argues about
     sunk cost instead of about evidence, and the argument is won by whoever is most
     senior or most tired.

     A kill criterion written before launch is an argument you have while everyone is
     still calm. Three rules make it real:

     - A threshold, not a mood. "Adoption is disappointing" is not a criterion.
       "Weekly active use in the pilot cohort below 200 accounts at day 60"
       (ILLUSTRATIVE, invented for this example) is.
     - A check point, not a vigil. Name the date or the milestone when someone looks.
       A criterion nobody is scheduled to check is not a criterion.
     - A named caller. The person who is allowed to say stop, in advance, in writing.
       Usually the same human who signs Gate 2.

     Stopping is not the only outcome. A criterion can trigger a rollback, a scope
     cut, a pivot to the second option in the decision memo, or an extension with a
     new threshold. Say which, per row.

     If a criterion fires and the team continues anyway, that is a legitimate
     decision, and it goes in ../execution/decision-log.md with the reasoning. What
     is not legitimate is having no criterion to fire. -->

## 10. Four risks, answered

| Risk | Answer, with evidence | Strongest evidence against | Confidence (high / medium / low) |
|---|---|---|---|
| Value: will they use it | | | |
| Usability: can they use it | | | |
| Feasibility: can we build it | | | |
| Viability: does it work for the business | | | |

<!-- The counter-evidence column is not optional and it is not rhetorical. Write the
     single strongest fact, quote, or number that argues against your answer. If you
     cannot find one, write "none found, and here is where I looked" and name the
     sources. A risk row with an empty counter-evidence cell has not been thought
     about; it has been asserted.

     Low confidence is a legal answer. It routes the risk into
     assumptions-register.md with a validation method and a date, and it usually
     means the honest next step is a prototype or a test rather than more document.
     An empty cell is not a legal answer. -->

## 11. Assumptions

| # | The guess this plan is standing on | Impact if wrong | Register ID | Validate by | Owner |
|---|---|---|---|---|---|
| A1 | | | [row ID in assumptions-register.md, for example AS-004] | [YYYY-MM-DD] | |

<!-- The short index only. The full register, with confidence, validation method and
     status, is assumptions-register.md. The Register ID column carries that file's
     own row ID so the two never drift; markdown cannot deep-link a table row, so
     cite the ID rather than trying to link it.

     What belongs here: the load-bearing guesses. Not every assumption, only the ones
     that, if false, change what ships or whether it ships at all. If an assumption
     appears in section 9 as a kill criterion, it belongs here too.

     Every row carries a validate-by date. An assumption with no date is a belief,
     and beliefs do not expire on their own. -->

## 12. Open questions

| # | Question | Blocks (section or story) | Owner | Needed by |
|---|---|---|---|---|
| Q1 | | | | |

<!-- Cap this table. Five open questions at Gate 2 is a document with honest gaps;
     twenty is a document that has become a graveyard, and nobody reads a graveyard.
     If the list is longer than five, the extras are not open questions: they are
     either decisions nobody has made (route them to
     ../planning/decision-memo.md) or scope nobody has cut (route them to
     section 7).

     Every row needs an owner and a date. A question with neither is a note. -->

## 13. Companion documents

<!-- The spine above is what every product fills. This table is how the rest of the
     system reaches this document. Read the triggers, tick the ones that are true,
     and open those templates. Leave the untriggered rows as they are; they are the
     record of what you considered and did not need.

     The pattern of a short mandatory core plus a menu pulled in by product type is
     borrowed from the BMAD-METHOD project's PRD template, applied here to the
     templates this repository already ships. -->

| Trigger, if this is true of your product | Open this | Stage |
|---|---|---|
| Users can lose data, money, or work if this misbehaves | [failure-scenarios.md](../delivery/failure-scenarios.md) | DELIVER |
| The behavior at the boundaries is not obvious from the stories | [edge-cases.md](../delivery/edge-cases.md) | BUILD into DELIVER |
| Any metric in section 6 is not already instrumented | [analytics-instrumentation-spec.md](../delivery/analytics-instrumentation-spec.md) | DELIVER |
| A support or success team will field questions about this | [support-runbook.md](../delivery/support-runbook.md) | DELIVER |
| Existing users or existing data have to move | [migration-cutover-plan.md](../delivery/migration-cutover-plan.md) | DELIVER |
| This replaces something people currently rely on | [sunset-eol-plan.md](../operate/sunset-eol-plan.md) | OPERATE |
| Anyone outside the team has to be told it shipped | [launch-comms-plan.md](../delivery/launch-comms-plan.md) | DELIVER |
| It touches what customers pay for, or what tier they are on | [pricing-packaging.md](../planning/pricing-packaging.md) | PLANNING |
| It processes personal data | [privacy-impact-assessment.md](../architecture/privacy-impact-assessment.md) | DESIGN |
| A regulator, licence condition, or scheme rule is in scope | [reg-gap-check](../../skills/reg-gap-check/SKILL.md) and `modules/regulated/` | DEFINE and DELIVER |
| Anyone will use this with a screen reader, a keyboard only, or at low vision | [accessibility-checklist.md](../architecture/accessibility-checklist.md) | DESIGN |
| An availability or latency promise is made to anyone outside the team | [sla-slo-definition.md](../delivery/sla-slo-definition.md) | DELIVER |
| A third party has to ship something for this to work | [dependency-register.md](../execution/dependency-register.md) | DESIGN |
| A model produces any part of the output | [eval-spec.md](../ai/eval-spec.md) and the rest of `templates/ai/` | AI overlay, from DEFINE |
| The business case has not been made anywhere else | [business-case.md](../planning/business-case.md) | PLANNING |
| More than one team has to change something | [program-charter.md](../planning/program-charter.md) | PLANNING |

## Sign-off

| Role | Name | Date | What they are signing |
|---|---|---|---|
| Product owner | | | The problem, the objectives, and the scope boundary |
| Engineering lead | | | Feasibility, the non-functional register, and the estimate |
| Design lead | | | Usability evidence and the accessibility position |
| Gate 2 approver | | | That Gate 2 in [os/STAGE-GATES.md](../../os/STAGE-GATES.md) is met |

<!-- The Gate 2 approver is a named person, and it is not the person who wrote this
     document, and it is not an agent. Verify and report; never sign. -->

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Section 0 is under 150 words and a reader who stops there is not misled
- [ ] "Who implements this" is answered, and if the answer is a model, the AI overlay is attached
- [ ] Background links to discovery evidence rather than restating it
- [ ] Every objective has metric, baseline, and target, and no target is still ILLUSTRATIVE
- [ ] Every must story carries an acceptance criteria ID
- [ ] Functional scope rows each trace to a story
- [ ] At least one guardrail metric is named, with an owner and an instrumented source
- [ ] Out of scope names the exclusions a reader would otherwise assume in
- [ ] Launch criteria are all checkable, each with an owner
- [ ] At least one kill criterion has a threshold, a check point, and a named caller
- [ ] All four risks carry an answer, counter-evidence, and a confidence level
- [ ] Every low-confidence risk and open question has an owner and a date
- [ ] Open questions number five or fewer, and the rest have been routed
- [ ] Every load-bearing assumption has a validate-by date
- [ ] The companion table has been read and the triggered rows opened
- [ ] [spec-review](../../skills/spec-review/SKILL.md) has run and no blocking finding is outstanding
- [ ] If the product contains an AI or machine-learning feature and a regulator applies to it, the regulated module template is in use as shipped
- [ ] The sign-off block names real people, and the Gate 2 approver did not write this document
