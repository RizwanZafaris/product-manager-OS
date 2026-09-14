# Risk Register: Expense Copilot

Fills [templates/execution/risk-register.md](../templates/execution/risk-register.md). Part of the [Ledgerline Expense Copilot journey](expense-copilot-journey.md): the internal v1 Ledgerline's own finance team commissioned for Ledgerline's own filers, from the understood problem to a development-ready handoff at Gate 3. Everything here is invented and ILLUSTRATIVE, drawn from that journey's data sheet and from [ledgerline-journey.md](ledgerline-journey.md)'s data sheet; no figure is a target to copy. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), reviewed weekly through DELIVER
Knowledge: [Cagan on the four risks](../knowledge/cagan-product-teams.md)
Skill: [program-premortem](../skills/program-premortem/SKILL.md)

**Initiative:** Expense Copilot (Ledgerline internal v1) · **Register owner:** Maya Chen, Product Manager · **Review cadence:** weekly, `<day and meeting>` (neither data sheet fixes a day or a standing meeting; this chain closes at Gate 3 on 2026-09-11, before DELIVER's weekly cadence begins)
**Last reviewed:** 2026-09-08 · **Premortem run:** 2026-09-08

## 1. Scoring

Neither data sheet assigns a numeric likelihood or impact to RV-1 to RV-4. [expense-copilot-journey.md](expense-copilot-journey.md)'s Risks table carries only an id, a description, an owner, an opened date and a status at Gate 3, and [ledgerline-journey.md](ledgerline-journey.md) adds nothing to those four beyond the two citations that table already names: N2 behind RV-4, and the row 7 open item on [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md) that RV-1 echoes. The scores in section 2 apply the template's own fixed scale, likelihood and impact each 1 to 3 so a score runs 1 to 9, six or above needing an active mitigation with a date rather than a watching brief, to what the two sheets say about each risk. No number in this section stands in for a sheet figure; each is this register reading the template's scale onto a sourced description, with the reasoning shown so it can be checked rather than taken on faith.

### The premortem

Run 2026-09-08 (V14), the same day [expense-copilot-journey.md](expense-copilot-journey.md) records the dependency register drafted (V13), using [frameworks/execution/premortem-worksheet.md](../frameworks/execution/premortem-worksheet.md)'s method. The room was this chain's own named cast: Maya Chen, Priya Nair and Daniel Okafor, plus the legal lead by role. The worksheet also asks for one outsider who will not do the work; neither data sheet names one for this session, so this register does not claim one attended. Shown briefly, as the worksheet structures it:

**Step 1, the failure headline.** Date of failure: launch plus one quarter, one of the worksheet's own two suggested framings, measured from go-live on 2026-10-12. Headline, past tense: it is launch plus one quarter, and finance reviewers stopped trusting the copilot's drafts after extraction on crumpled or foreign-language receipts kept coming back wrong.

**Step 2, causes.** Four causes, each already the seed of a register row below, so every "already on the register?" answer is no: this premortem is what put them there.

| # | Cause (past tense) | Category |
|---|---|---|
| 1 | Extraction on a crumpled or foreign-language receipt came back wrong often enough that reviewers stopped trusting drafts | feasibility |
| 2 | The model vendor's training-data and retention terms stayed unresolved past Gate 3 | security |
| 3 | Receipts kept accumulating before a retention and deletion schedule was signed | security |
| 4 | One model call per receipt (ADR-0001) raised cost or latency once monthly volume outgrew the internal baseline | viability |

The worksheet's own table also asks each cause's author's role; neither data sheet names who raised which cause in this session, so that column is left out here rather than assigned by guess.

**Step 3, votes.** The worksheet scores each cause as likelihood votes plus twice its unrecoverable votes. Neither data sheet records this session's vote tally, so this register does not invent one. What the session produced instead, and what section 2 below carries, is each cause's likelihood and impact on the template's own fixed 1-to-3 scale, which is the judgment the votes exist to produce.

**Step 4, mitigations.** Every cause scoring 3 or more became a register row with a named owner, shown in section 2. Per D-6 ([expense-copilot-journey.md](expense-copilot-journey.md) decision log), the AI overlay's own guardrails, eval spec and red-team review are deferred to the PRD's existing Gate 5 launch criteria rather than duplicated at Gate 3, so cause 1's mitigation below points to that Gate 5 checkpoint rather than restating overlay content this chain has already decided not to hold twice.

**Step 5, the sentence.** "It is launch plus one quarter, and the initiative failed. The most likely cause, given the table above, was cause 1: extraction on a crumpled or foreign-language receipt came back wrong often enough that reviewers stopped trusting drafts." Cause 1 carries the session's highest score (RV-1, section 2) and, unlike RV-2 and RV-3, has no dependency register row driving it to closure: [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md) tracks a vendor clause and a retention schedule, nothing that tracks extraction quality itself. Its only checkpoint is the eval spec threshold at Gate 5, and D-4 already records that threshold as ILLUSTRATIVE, not finance-agreed. RV-2 and RV-3 close when DEPV-1 and DEPV-2 deliver; RV-1 closes only once someone writes a number nobody has agreed to yet.

## 2. The register

| # | Risk (event, not a vague noun) | Category | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| RV-1 | Extraction quality on crumpled or foreign-language receipts is unproven | feasibility | 2 | 3 | 6 | mitigate | The eval spec's threshold on the labeled receipt set, due before Gate 5 (2026-10-09, N16); the threshold itself is ILLUSTRATIVE, not finance-agreed, per D-4. Trigger: any eval run scoring below the threshold, or Gate 5 arriving with no finance-agreed number in its place | Priya Nair | before Gate 5 (2026-10-09, N16) |
| RV-2 | The model vendor's training-data and retention terms are unresolved | security | 2 | 3 | 6 | mitigate | DEPV-1 delivering (vendor clause forbidding training on Ledgerline data), due before Gate 5; see [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md). Trigger: DEPV-1 still open as Gate 5 approaches | the legal lead | before Gate 5 (2026-10-09, N16) |
| RV-3 | Receipts accumulate before a retention and deletion schedule is signed | security | 2 | 2 | 4 | mitigate | DEPV-2 delivering (receipt image retention and deletion schedule), due before Gate 5, per the PRD's Launch criteria; see [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md). Trigger: DEPV-2 still open as Gate 5 approaches, or receipts continuing to accumulate with no schedule signed | the legal lead | before Gate 5 (2026-10-09, N16) |
| RV-4 | One model call per receipt (ADR-0001) raises cost or latency if monthly volume outgrows the internal baseline | viability | 2 | 2 | 4 | mitigate | Watch monthly and annual receipt volume against the basis the quoted rate assumes: about 40,000 receipts a year (N9), the same figure N10 derives from N2's 9,600 reports a year at 4.2 receipts each. DEPV-3, contracting rather than merely quoting the per-receipt price, is the mitigation meant to pre-empt this before volume outgrows that basis; see [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md). Trigger: monthly volume trending above the N2 baseline with DEPV-3 still open | Priya Nair | 2026-11-09, the first internal metrics review ([ledgerline-journey.md](ledgerline-journey.md) N17, N25) |

RV-2 and RV-3 both score under security because both trace to the same underlying fact: receipts carry personal data, per the PRD's Launch criteria and V10's provisional PII flag on the Receipt and LineItem entities. RV-2 is the exposure on the model vendor's side of that data; RV-3 is the exposure on Ledgerline's own side, before its retention and deletion schedule is signed. RV-1 is scored feasibility because it asks whether the extraction mechanism itself works, prior to any question of value or cost; RV-4 is scored viability because it asks whether the mechanism stays affordable once its one-call-per-receipt design (ADR-0001) meets real volume.

Two rows score 6 and two score 4; none scores lower, and none scores higher. A four-row register from one hour-long session has a narrow range by construction, not because every risk here is actually the same size: RV-1 and RV-2 threaten the product's core mechanism and its ability to launch at all, while RV-3 and RV-4 are real but more remediable once their dependencies land.

## 3. Accepted risks

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| | | | | |

Empty. No risk on either data sheet carries an accept response at Gate 3: RV-1 to RV-4 are all open with a mitigate response in section 2, each tied to a dependency or a Gate 5 checkpoint rather than a named person choosing to live with it. This section stays empty because nothing has been accepted yet, not because a signature was skipped.

## 4. Closed risks

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| | | |

Empty. All four rows are open at Gate 3 (2026-09-11) per the data sheet's own status column, and this chain closes at Gate 3, before any of RV-1 to RV-4 has had a chance to resolve. [ledgerline-journey.md](ledgerline-journey.md) N9 shows DEPV-3's underlying condition still true after go-live (the rate still quoted, not contracted), which would keep RV-4 open too were this register reopened on that later date; N20 shows DEPV-4 delivered on time, but DEPV-4 is a dependency register row, not one of RV-1 to RV-4, so its delivery closes nothing in this section directly.

## 5. How this register fails

| Failure mode | What it looks like here | The rule that stops it |
|---|---|---|
| No owner | Never happened here: RV-1 and RV-4 name Priya Nair, RV-2 and RV-3 name the legal lead, in section 2 | Orphans go to the top of the review, not the bottom |
| Scored once, never revisited | This is the live version of that risk for a three-day-old register: RV-1 to RV-4 have been scored exactly once, at the 2026-09-08 premortem, and Gate 3 on 2026-09-11 reads them without re-scoring | Re-score at every review; DELIVER's weekly cadence is where a second score becomes possible, and this register is not old enough yet to have skipped one |
| Mitigation restates the risk | Never happened here: each mitigation in section 2 names a dependency register row or a Gate 5 checkpoint, not a restatement of the risk itself | A mitigation names an action, an owner and a date, or it is not one |
| Everything is medium | Two rows score 6, two score 4; not a flat list, though the range is narrow for the reason given under section 2 | Force a spread. A four-row register from one session has less room to spread than a year-long one, and this table says so rather than pretending the two scores mean more separation than they do |
| Closed risks deleted | Not applicable: nothing has closed yet to delete | Closed rows are archived in section 4, not removed, once any exist |
| The register replaces escalation | RV-1 is the live version of this concern: it scores 6, its only checkpoint (the eval spec threshold) is explicitly ILLUSTRATIVE and not finance-agreed per D-4, and no one has been told about that gap beyond this register and the decision log | Naming the gap here is not the same as raising it; Priya Nair, as owner, is the one accountable for putting a real number in front of Daniel Okafor before Gate 5, not for this row alone to stand in for that conversation |

This chain has no separate security-architecture checklist: Priya Nair signs Gate 3's security-reviewer line herself, per V16, a fact about the team's size the journey names rather than smooths over. RV-2's and RV-3's security-flavoured findings come from this premortem and from the dependency register alone, not from a checklist that does not exist for this build.

## Exit gate

- [x] Every risk is written as an event that could happen, not a topic heading: RV-1 to RV-4 in section 2, each an event (extraction failing, terms staying unresolved, receipts accumulating, cost or latency rising), none a bare noun like "extraction risk."
- [x] Every open risk has a score, an owner, and a review date in the future: RV-1 to RV-4 in section 2, each dated after the 2026-09-08 last-reviewed date.
- [x] Every score of 6 or higher has an active mitigation with a trigger, not "monitor": RV-1 and RV-2, both scored 6, each carry a named mitigation and trigger in section 2.
- [x] Every accepted risk is signed by name in section 3: vacuously true. No risk carries an accept response by Gate 3, so section 3 holds no row to sign; see its own note above.
- [x] Findings from the security architecture checklist and dependency register appear here: no security architecture checklist exists for this build (see section 5's closing note); DEPV-1 and DEPV-2 from [expense-copilot-dependency-register.md](expense-copilot-dependency-register.md) appear as RV-2's and RV-3's mitigations in section 2.
- [x] A premortem has been run before Gate 3, and its findings are rows above: 2026-09-08, before Gate 3 on 2026-09-11; walked briefly above, producing RV-1 to RV-4 directly.
- [x] The example row has been deleted: section 2 holds only RV-1 to RV-4.

Reviewed and current as of 2026-09-08: Maya Chen, Product Manager and register owner, ahead of Gate 3 on 2026-09-11. Open: RV-1 to RV-4, all carried into Gate 3 as open with a mitigate response; none closes inside this chain, which ends at that gate.
