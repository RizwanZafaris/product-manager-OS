---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: "knowledge/crossing-the-chasm.md"
aliases: ["GTM Plan", "gtm-plan"]
---
# GTM Plan: [product name]

**Stage:** DELIVER (this file feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [Crossing the Chasm](../../knowledge/crossing-the-chasm.md)
**Skill:** [gtm-launch-planner](../../skills/gtm-launch-planner/SKILL.md)

<!-- The release checklist proves the product can ship. This file answers the question
     that checklist never asks: who meets it first, and why them.

     The structure follows Geoffrey Moore's Crossing the Chasm argument, restated in
     this repository's own words: early buyers and mainstream buyers purchase for
     different reasons, so a launch aimed at "the market" is aimed at nobody. Win one
     narrowly described cohort completely, then widen from the proof. The positioning
     skeleton in section 2 is Moore's as well, adapted; its power is that every blank
     must be filled with something checkable.

     Two disciplines this file enforces. One metric, not a dashboard: a launch judged
     by five numbers is judged by whichever one moved. And the stop condition is
     written now, because nobody reasons well mid-launch. -->

**Owner:** [name] · **Launch window:** [period, not a promise] · **Last updated:** [YYYY-MM-DD]
**Release readiness doc:** [filled copy of release-readiness.md](../delivery/release-readiness.md) · **Discovery doc:** [this product's Gate 1 evidence]

## 1. First cohort: the beachhead

<!-- Small enough to name and reach. "Evidence" means an artifact: a list you hold, a
     community you already stand in, a signed pilot agreement. "We will post about it"
     is a hope with a verb. The italic row shows a completed entry. A cohort named by
     title alone, such as "enterprise admins," is not a beachhead; the tell is that
     nobody on the team could hand over today's list of who it means. -->

| Cohort (who, precisely) | Size | Channel that reaches them | Evidence the channel reaches them | Owner |
|---|---|---|---|---|
| | [count] | | [artifact, linked or filed] | |
| *ops leads at the 9 design-partner firms (ILLUSTRATIVE)* | *9 firms, ~20 people* | *direct email from the pilot thread* | *pilot agreement + active email thread, filed in discovery/* | *[name]* |

## 2. Positioning against the named alternative

<!-- The alternative is what the cohort does today, which is usually a spreadsheet,
     an intern, or nothing, not the competitor on your slide. If the "unlike" line
     names no specific alternative, the competition has not been studied and this
     section is returned for rework, not polished. A positioning skeleton filled with
     adjectives the team likes, not words the cohort actually uses, is decoration;
     the red flag is an "ours" line nobody could verify by watching one demo. -->

- **For** [the cohort in section 1]
- **who** [the struggle, stated in words a cohort member has actually used]
- **[product name] is a** [category the buyer already has a mental shelf for]
- **that** [the one capability that removes the consequence they eat today]
- **unlike** [the named alternative they use now, including "a spreadsheet" or "doing nothing"]
- **ours** [the difference a skeptical buyer can verify in one demo]

## 3. Launch sequence

<!-- Phases advance on conditions, not on the calendar. An exit condition is evidence
     a reader could check, and each phase's comms are drafted before its entry, which
     is what Gate 5's comms line will ask about. A phase that exits "when it feels
     ready" instead of on the stated condition never actually gates anything; the
     tell is a phase 2 that started before phase 1's evidence existed. -->

| Phase | Cohort added | Entry condition | Exit condition (evidence, not a date) | Comms that go out | Owner |
|---|---|---|---|---|---|
| 1 | | Gate 5 signed | | | |
| 2 | | Phase 1 exit met | | | |
| 3 | | Phase 2 exit met | | | |

## 4. The one metric that says the launch worked

<!-- Exactly one. It should feed the Gate 1 success signal or an input metric on the
     north star tree, so the launch is scored in the product's own currency, not in
     launch-day applause. Impressions and coverage are activity, not adoption. A
     metric borrowed from the marketing dashboard because the number is already
     flowing is a bad answer here; the tell is a target with no owner on the product
     side who would act if it missed. -->

| Metric | Source system | Baseline | Target | Review date |
|---|---|---|---|---|
| | | | | |

## 5. Stop condition

<!-- Decided before launch, while everyone is still calm. The rollback this triggers
     is the one Gate 5 rehearsed in pre-production, not a new plan invented live. A
     stop condition written as "if things go badly" is not a threshold, it is a
     mood, and moods get argued down mid-launch; the tell is a number nobody agreed
     to before day one. -->

| What pauses rollout | Threshold | Who calls it | What happens next |
|---|---|---|---|
| | [number, with unit and period] | [name, reachable during launch] | [pause / rollback per the readiness doc, plus who is told] |

## How this launch fails

<!-- The first row is the expensive one, because launching to everyone is the
     default and it removes the only chance to learn cheaply. A failure-mode table
     copied verbatim from the last launch, with no row edited for this cohort, is
     never actually read again; the tell is a "rule that stops it" column with no
     name attached to who enforces it. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Everyone at once | One announcement to the whole base on day one, no cohort | Seed a named first cohort, read the signal, then widen |
| No first cohort | Segments described, but everybody goes live together anyway | Name the cohort, its size, and how feedback is captured |
| Success is the launch | The measure is that it shipped, or day-one traffic | Success is a retained behaviour some weeks later, per cohort |
| Support briefed last | Reps and agents get the material the day customers do | Brief support and sales before launch, and record the sign-off |
| No rollback for the message | Reaction is bad, and the copy stays up while a meeting is arranged | Agree the swap trigger and the alternate wording in advance |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. A gate signed by the plan's own author
     is not a check, it is a rubber stamp; the tell is a signature with no
     evidence attached to a single box above it. -->


This plan is fit to launch on when:

- [ ] The first cohort is described precisely enough that a member list could be assembled this week
- [ ] The channel carries evidence, an artifact a reader can open, not an intention
- [ ] The positioning names a real alternative, and every blank in section 2 is filled with something checkable
- [ ] Every phase exits on a condition, and each phase's comms exist before its entry
- [ ] Exactly one launch metric is named, with baseline, target, source system, and review date
- [ ] The stop condition names a threshold and a caller, and triggers the rollback Gate 5 actually rehearsed

Signed: [name], [role], [YYYY-MM-DD]
