---
layer: templates
stage: BUILD
gate: 4
feeds: []
method: ""
aliases: ["Change Request", "change-request"]
---
# Change Request: CR-[n], [short name]

Stage: BUILD and DELIVER, after Gate 2 signed a baseline; feeds [Gate 4: acceptance criteria met](../../os/STAGE-GATES.md), which checks that every scope change since Gate 2 is logged with a decider
Knowledge: [estimation sheet](../../frameworks/execution/estimation-sheet.md)
Skill: [decision-memo](../../skills/decision-memo/SKILL.md)

> **Delete any section you do not need.** A change inside one sprint, one team, and one feature flag is a ticket plus a decision log line, per [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md). This form is for changes to what Gate 2 signed: scope, a committed date, budget, or a non-functional target. Never leave a heading standing over white space.

<!-- One change to a signed baseline: what it is, what it does to scope, schedule,
     cost, and risk, and who approves it. The rule that carries the document: the
     baseline changes after approval, never before. A PRD edited to match a change
     nobody approved is how a quarter becomes two without anyone deciding it should.

     Neighbours: the decision memo (../planning/decision-memo.md) is for a decision
     with no baseline behind it; the decision log (decision-log.md) records the
     outcome of this request; the PRD and acceptance criteria are re-baselined in
     section 7 once approval is recorded.

     Fill first: the change and its trigger in section 1, the impact table in
     section 3, and the approvers in section 6. -->

**Requested by:** [name] · **CR owner:** [name] · **Raised:** [YYYY-MM-DD] · **Decision needed by:** [YYYY-MM-DD] · **Status:** Proposed / Assessed / Approved / Rejected / Withdrawn

## 1. The change

- **From:** [the baseline as signed, in one sentence]
- **To:** [the proposed state, in one sentence]
- **Baseline reference:** [PRD version, charter date, acceptance criteria IDs affected]
- **Trigger:** [what surfaced this: a build-time discovery, a customer commitment, a regulatory change, an estimate that was wrong. Name the source.]
- **Why now, and what happens if it waits:** [one or two sentences]

## 2. Options

<!-- Reject is a legal outcome and often the right one. Defer is a legal outcome
     with a named release. A request assessed with only "accept" as the option was
     a notification, not a request. -->

| Option | What it means | Impact in one line |
|---|---|---|
| Accept as proposed | | |
| Accept reduced: [the smaller version] | | |
| Defer to [release or quarter] | | |
| Reject | | |

## 3. Impact assessment

<!-- Schedule and cost deltas carry a range from the estimation sheet; a single
     number is an opinion with a decimal point. "Assessed by" is the person who
     did the arithmetic, not the person who asked for the change. -->

| Dimension | Baseline | After the change | Delta | Range (low / high) | Assessed by |
|---|---|---|---|---|---|
| Scope (stories, acceptance criteria) | | | | | |
| Schedule (milestones, Gate 4 date) | | | | | |
| Cost (build, run) | | | | | |
| Quality and non-functional targets | | | | | |
| Risk (new or changed register rows) | | | | | |
| Dependencies (other teams, needed-by dates) | | | | | |
| Compliance (regulated overlay, if it applies) | | | | | |

## 4. What we give up

[The explicit trade: what leaves scope, what slips, or what is descoped to pay for this. A change that costs nothing has not been assessed.]

## 5. Recommendation

- **Option:** [from section 2], because [two sentences].
- **Conditions:** [what must be true, with an owner and date each, or "none"].

## 6. Approvals

<!-- Approvers are the accountable names for the affected decision areas in the
     stakeholder map or the program charter, not whoever is in the room. The sponsor
     signs whenever money or a committed date moves. -->

| Role | Name | Decision (approve / approve with conditions / reject) | Conditions | Date |
|---|---|---|---|---|
| Accountable for scope changes | | | | |
| Engineering lead | | | | |
| Sponsor (when budget or a committed date moves) | | | | |
| Regulatory owner (regulated products only) | | | | |

## 7. After approval

<!-- Done in this order, within a week of the approval date. Until this list is
     complete the baseline is ambiguous and both versions will be quoted. -->

- [ ] Decision log entry D-[n] created, naming this CR number
- [ ] PRD or one-pager version bumped, with the change noted in its change history
- [ ] Acceptance criteria added, changed, or retired by ID
- [ ] Roadmap row and capacity plan updated
- [ ] Risk and dependency register rows updated
- [ ] Status report carries the new baseline from the next issue
- [ ] Teams affected told, by [channel] on [date]

---

## Exit gate (feeds Gate 4: acceptance criteria met)

Done when every box is honestly ticked. The approved request travels with its decision log entry to [Gate 4](../../os/STAGE-GATES.md), which asks that every scope change since Gate 2 has a decider.

- [ ] The change is stated as from and to, with the baseline version it changes
- [ ] Reject and defer were assessed as options, not listed for form
- [ ] Every impact row carries a delta with a range and the name that assessed it
- [ ] What we give up is written
- [ ] Approvers are the accountable names from the RACI; the sponsor signed if money or a date moved
- [ ] The decision log entry exists and names this CR
- [ ] Baseline documents were updated after approval, not before
- [ ] Signed by the CR owner, [name], [date]
