---
name: spec-review
description: Read any written spec, PRD, BRD, FRD, NFR, one-pager, business rules register, acceptance criteria, or epic and story text, and report every place the prose cannot be tested: unquantified adjectives, requirements that cannot fail, rows with no owner, dates that should be a day rather than a quarter. Use when a document is heading to a stage gate, when a draft reads clean to the person who wrote it, when the same ambiguous phrase keeps getting relitigated during BUILD, or when write-prd calls this check before Gate 2. Reports findings and never rewrites, the discipline validation-agent also holds. Takes the drafted document; returns a severity-ranked findings table with the exact phrase and the rewrite question for the author.
---

# Spec Review: requirements as testable prose

Every exit gate in this operating system checks that a field is filled. Nothing, until this skill, checked that what got written in the field could be tested. A requirement that reads well and cannot fail passes Gate 2 clean and fails at the first engineering question, the first QA run, or the first meeting where two people discover they meant different things by fast. This skill runs fourteen checks against the sentence itself and reports what it finds in a table; it never rewrites the draft, the same discipline [validation-agent](../../agents/validation-agent.md) holds for structure elsewhere in this repository.

## Files this skill drives

- Runs against a document already drafted, and edits none of them: [prd.md](../../templates/definition/prd.md), [brd.md](../../templates/definition/brd.md), [frd.md](../../templates/definition/frd.md), [nfr.md](../../templates/definition/nfr.md), [one-pager.md](../../templates/definition/one-pager.md), [business-rules.md](../../templates/definition/business-rules.md), [acceptance-criteria.md](../../templates/definition/acceptance-criteria.md), and epic or story text out of [story-writer](../story-writer/SKILL.md)
- Blocking findings hold whichever stage gate the document is heading to in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); [write-prd](../write-prd/SKILL.md) runs this check before every Gate 2 submission, and any other skill in this repository may call it before its own gate the same way
- Method background: the discipline of checking requirements prose the way tests check code is borrowed from GitHub's spec-kit project, adapted below as the fourteen checks, in this repository's own words

## When to use

- A PRD, BRD, FRD, NFR, one-pager, business rules register, or acceptance criteria draft exists and is heading to a stage gate
- A draft reads clean to the person who wrote it, which is exactly when a second pass earns its cost
- The same ambiguous phrase keeps getting relitigated during BUILD, months after DEFINE closed and nobody remembers deciding it
- Epic or story text is about to leave backlog refinement and become a sprint commitment

## Inputs

The drafted document, at whatever weight it was written, and the document type it claims to be, because a PRD read as an NFR misses half the checks below. Confirm first that the file is a filled draft and not a blank template copied out of `templates/`; run against a blank and every check fires at once, which tells the author nothing they did not already know. Ask for these when missing: the stage gate it is heading to, from [os/STAGE-GATES.md](../../os/STAGE-GATES.md); and whether the author wants every finding or blocking findings only, since a first pass takes everything and a re-check before signing takes blocking only. This skill never supplies the missing number or the missing owner itself, only the question that gets it out of the author.

## The fourteen checks

1. **Unquantified adjectives.** Flags fast, intuitive, seamless, robust, scalable, secure, and their cousins wherever no number or threshold sits next to them; an engineer can satisfy an adjective however is easiest, and a tester can never fail it. Before: "Receipt capture must be fast." After: "Receipt capture returns a verdict within 2 seconds (ILLUSTRATIVE) at p95."
2. **Requirements that cannot fail.** For every requirement, asks what observation would prove it false; no answer means it passes by definition and the gate that checked it learned nothing. Before: "The system will support reconciliation." After: "GIVEN a report with an unmatched line, WHEN the rep submits it, THEN the report is blocked and the line is named."
3. **Passive requirements with no actor.** Flags "it will be validated," "the data will be checked," anywhere the sentence has no subject; at build time nobody owns the check, so it gets skipped. Before: "Receipts will be validated for legibility." After: "The legibility service validates each photo on capture."
4. **"Should"/"may" where "must"/"will not" is meant, and the reverse.** A "should" that means unconditional becomes optional the first time a sprint runs short; a "must" that is really a preference nobody agreed to enforce turns into a quiet fight the first time it gets relaxed. Before: "The app should queue receipts offline." After: "The app must queue receipts offline; no connectivity will not block capture."
5. **Rows with no owner, or an owner that is a team name.** An owner cell needs a person who answers a message, not "Engineering" or "the team," because a team cannot be asked why a row is late. Before: "Owner: Platform team." After: "Owner: [name], platform lead."
6. **Dates that are quarters where a decision needs a day.** Read date cells only; this repository numbers its open questions Q1 to Q5 and those are row IDs, not quarters. A quarter in a date cell lets a decision, a kill check, or a validation slide for thirteen weeks with nobody able to say it is late. Before: "Validate by: Q3." After: "Validate by: [YYYY-MM-DD]."
7. **Numbers with no unit, no baseline, or no source.** Every number in an objective or metric row needs where it starts, what it is measured in, and where it came from, or it cannot show a lift and gets quoted back as fact at the next meeting. Before: "Approval time drops to 4 hours." After: "Approval time drops from a [n]-hour baseline (source: [link], [date]) to 4 hours at p50."
8. **Acceptance criteria that restate the requirement instead of testing it.** A THEN line that repeats the requirement's own words plus "correctly" checks nothing, because it passes by the same definition that let the requirement pass. Before: "THEN the upload works correctly." After: "THEN the app shows an accept or retake verdict before the submit control activates."
9. **An objective and a metric that measure different things.** The metric column must move because the objective's outcome happened, not because of something else entirely, or the team can hit the number while the objective stays false. Before: "Objective: reps stop batching at month end. Metric: app store rating." After: "Metric: share of receipts captured within 1 hour of the expense (ILLUSTRATIVE)."
10. **A scope table row that appears nowhere in the stories.** Every functional-scope row must trace to a story; a capability with no story behind it shipped because it was easy to build, not because anyone asked for it. Before: "F4: Export to CSV. Story served: (blank)." After: "F4: Export to CSV. Story served: US7, or the row is removed."
11. **An exclusion missing from the out-of-scope table that the reader will assume is in.** Checks every capability a reasonable reader would assume follows from what is in scope; the ones left unnamed are the ones an implementer, human or agent, will attempt. Before: the out-of-scope table has no row for multi-currency, in a feature that captures receipts across regions. After: "Excluded: multi-currency conversion. Why: single-currency pilot only; revisit after Gate 6."
12. **A kill criterion with no threshold or no named caller.** Every kill row needs a metric or date, a threshold, a check point, and a person who calls it; "if it is not working" supplies none of the four. Before: "We will stop if adoption disappoints." After: "K1: if week-4 capture rate is below [n]% (ILLUSTRATIVE) by [date], [name] decides at the next review."
13. **An assumption with no validate-by date.** A confidence label with no date sits untested indefinitely, because nothing on the calendar forces the question back open. Before: "AS-004: Finance accepts one approval threshold. Confidence: low." After: "AS-004: Finance accepts one approval threshold. Confidence: low. Validate by: [date]. Validation: [method]."
14. **Terms used with two meanings in the same document, or a load-bearing term used more than three times and never defined.** The remedy is a definition stated once at first use, not a glossary section; none of the templates this skill audits has one. "Approved" meaning a manager's click in one section and a passed fraud check in another lets two readers silently disagree. Before: "approved" used both ways, never distinguished. After: one definition stated once, then "manager-approved" and "fraud-cleared" used consistently.

## Workflow

1. Identify the document type and, from it, which checks apply: checks 1 through 9 and 13 to 14 apply everywhere; checks 10 and 11 need a scope table and a story or out-of-scope table both present; check 12 needs a kill criteria section.
2. Read the whole document once for meaning, then again line by line, applying each check to every requirement, row, criterion, and term defined or implied.
3. For every hit, quote the exact phrase, or name the exact missing row, plus the check it fails and its location by section and row.
4. Assign severity: blocking, would fail the stage gate as written; should fix, weakens the document but the gate would still pass; or note, worth the author's attention and nothing more. Write one rewrite question per finding, never the rewrite.
5. Return the findings table, blocking first, then should fix, then note. Do not tell the author the document is ready; that word belongs to the human who signs the gate.

## Output format

| # | Severity (blocking / should fix / note) | Location (section, row) | Quoted phrase | Check | Rewrite question for the author |
|---|---|---|---|---|---|

Blocking findings hold the gate: a document with an open blocking finding does not go to its signer. Should-fix findings travel with the document and get a named owner if the author disagrees they block. A note is a suggestion; nothing holds on it.

## Exit gate

Do not call the review done while a blocking finding is open. This skill's table is evidence for a gate, never the gate itself: [os/STAGE-GATES.md](../../os/STAGE-GATES.md) still names a human who reads the document and signs it. A clean spec-review is not a gate pass; it is the condition that makes a gate pass worth trusting.
