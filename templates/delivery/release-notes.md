---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Release Notes", "release-notes"]
---
# Release Notes: [product or feature name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md)
Knowledge: [Knowledge index, SCR entry](../../knowledge/INDEX.md)
Skill: [release-manager-agent](../../agents/release-manager-agent.md)

> **Delete any section you do not need.** A ticket-weight change gets the customer block and one support line; a PRD-weight launch fills all three audiences. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- Release notes are the record of what changed, written three times for three
     readers who need different things: customers need what is new and what they
     must do; internal teams need why it shipped and what to watch; support needs
     what will break and what to say. One set of facts, three cuts. The timing and
     channels of who hears when belong to launch-comms-plan.md; the messages that
     go out in-app, by email, or on the status page belong to customer-comms.md;
     this file is what they all quote from. Fill section 1 first, then the
     customer block, then the support block; the internal block can wait until the
     other two agree. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Release facts

<!-- Copy from the filled release-readiness.md; never retype. If a fact here
     disagrees with the readiness document, the readiness document wins. -->

| Field | Value |
|---|---|
| Release | [version or milestone] |
| Ship date and time | [YYYY-MM-DD, time, timezone] |
| Rollout shape | [all at once / staged: cohorts and dates / behind a flag] |
| Readiness decision | [GO / GO WITH CONDITIONS, link to the filled release-readiness.md] |
| Scope cuts since sign-off | [list, or "none"] |
| Rollback trigger and owner | [condition, name; copied from release-readiness.md section 4] |

## 2. Customer notes

<!-- Written for the person who uses the product, in their words, no internal
     names. Lead with what they can now do. "Improved performance" says nothing;
     "the receipt upload no longer times out on files over [size]" says something.
     Anything taken away gets its own line; hiding a removal under "improvements"
     is how a launch earns its first angry ticket. -->

**What is new**

- [capability, one line, in the customer's terms]

**What changed**

| Before | Now | What you need to do |
|---|---|---|
| | | [nothing / a specific action] |

**What was removed or deprecated:** [feature, date it stops working, replacement; or "nothing"]

**Known limitations in this release:** [the customer-visible subset of section 4, in plain words]

## 3. Internal notes

<!-- For sales, success, leadership, and neighbouring teams. Why this shipped,
     what it is expected to move, and what would tell us it is not working. -->

- Problem this release addresses: [one sentence, traced to the PRD or one-pager]
- Metric it is expected to move: [metric, from the analytics instrumentation spec, with the dashboard link]
- Watch for in the first [n] days: [signal, threshold, owner]
- Flags and configuration: [flag names, default state, who may flip them]
- Not in this release, and when: [deferred items with the roadmap reference]

## 4. Support notes

<!-- The block support reads at 9 a.m. on launch day. Known issues are copied from
     the readiness document's table, then translated: a stack trace is not a
     symptom. The italic row is an invented example on the expense copilot. -->

| # | Symptom the customer will report | Cause | Workaround or answer | Escalate to | Fix date |
|---|---|---|---|---|---|
| | | | | | |
| *1* | *"my mileage claim shows the wrong currency"* | *rate table refreshes nightly, not at submit time* | *resubmit after the next refresh; macro EXP-CUR* | *payments on-call* | *[date]* |

**Expected questions, with the agreed answer:** [three to five, taken from the hardest questions in launch-comms-plan.md section 4]
**Escalation path for this release:** [name, channel, hours]
**Where the runbook lives:** [link to the filled support-runbook.md]

## 5. Breaking changes and deprecations

<!-- Anything that changes an API, an export format, an integration contract, or a
     workflow a customer has automated around. One row each, with the migration
     path and the date the old behavior stops. Cross-check against
     ../architecture/api-contract.md and ../architecture/integrations.md. -->

| Change | Who it affects | Migration path | Old behavior ends | Notice sent (date, channel) |
|---|---|---|---|---|
| | | | | |

## 6. Distribution

<!-- Where a note goes decides who reads it. Support reads it before the
     customer does, or the first person to explain the change to a customer
     is guessing. -->


| Audience | Where it is published | Owner | Approved by | Published (date) |
|---|---|---|---|---|
| Customers | [changelog, help center, in-app] | | | |
| Internal | [wiki, channel, email] | | | |
| Support | [knowledge base, macro set] | | | |

## 7. How release notes fail

<!-- These notes are read by people who do not work here, which is what makes
     the first two rows expensive: internal language is invisible to the
     person who wrote it and opaque to everyone else. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Internal language leaks out | A line describing a service, a queue or a refactor | Every line says what a user can now do, see, or stop seeing |
| Changes nobody can act on | "Improved internal error handling" | If a reader cannot tell whether it affects them, it does not belong here |
| Vague bug fixes | "Fixed an issue with exports" | Name the symptom and the situation, so the person who reported it recognises it |
| Removals go unmentioned | Only additions appear, and something quietly stopped working | A required section for anything removed, deprecated, or changed by default |
| Written after the release | Users meet the change before the note explaining it exists | The draft is done before the release, and the gate above checks that |
| No owner, so they stop | A gap of several releases, then an apology | A named owner, and a missing note is a missed deliverable rather than an oversight |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- The same release written twice. The first is what gets published when
     notes are drafted from the commit log; the second is what the rules above
     ask for. Delete once real content exists. -->

*As written from the changelog:*

> *Refactored the extraction pipeline for improved throughput. Updated error handling. Various bug fixes and performance improvements. Deprecated the legacy import endpoint.*

*As published:*

> **New.** *Photograph a receipt and the merchant, date and total fill in for you. Available on iOS and Android, one currency to start.*
>
> **Fixed.** *Expenses submitted between midnight and 1am were dated to the previous day. If you corrected a date manually in the last month, it is now correct on new submissions.*
>
> **Changing on 30 September.** *The old bulk import link stops working. If you upload a spreadsheet each month, switch to the new import screen before then. Nothing you have already uploaded is affected.*

The third block is the one the first version buried in a single word. A removal that a reader does not notice is the change most likely to generate a support ticket, and it is the one most often written for the team rather than the customer.

## Exit gate (feeds Gate 5: release readiness green)

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


The customer and support blocks satisfy the comms rows of [release-readiness.md](release-readiness.md) section 6 and the comms checkbox at [Gate 5](../../os/STAGE-GATES.md).

- [ ] Section 1 matches the filled release-readiness.md line for line
- [ ] Every customer-facing line names a capability or a change, not an adjective
- [ ] Every removal or deprecation has an end date and a migration path
- [ ] Every known issue in the readiness document appears in section 4 as a symptom with a workaround
- [ ] Support has read section 4 before any customer copy is published
- [ ] Each audience row in section 6 has a named approver
- [ ] Signed by [name], [date]
