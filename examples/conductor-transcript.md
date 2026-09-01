# Conductor Transcript: Renewal Radar

A condensed transcript of the Conductor (the interviewing skill at [../skills/conductor/SKILL.md](../skills/conductor/SKILL.md)) running one fictional product through the end of DISCOVER and the start of DEFINE. The product, the company, the people, and every number are invented for illustration; nothing here is evidence about any real product. See the [examples index](README.md).

Watch for five mechanics: one question at a time with lettered options that differ in consequence, the challenge grammar catching a vague answer with the two-push cap stated up front, every accepted answer landing in STATE.md before the next question fires, a stage advance refused with the gate checklist rendered as the reason, and the resume protocol at the start of the second session.

The product: Renewal Radar, a weekly digest that flags accounts at renewal risk, proposed at Harwick Systems (fictional, about 500 employees). The PM is Sana Iqbal. The workspace is `products/renewal-radar/`.

---

## Session 1: DISCOVER, 2026-08-20

**Conductor:** Question DISCOVER-1. Who exactly has this problem? Getting this wrong costs the whole run: every later answer inherits the person we name here. Recommended: (a), because a checkable name is the strongest thing you can put under a product, and you have interview notes on file. Options:

- a) I can name one person, at one company, and the consequence they personally eat. Implies: the answer enters at interview-claim class or better, and the personas build on someone real.
- b) I can describe a segment but not name a person. Implies: the answer enters the assumptions register, not the discovery document, and Gate 1 will see it there.
- c) I am not sure the problem holder is who we assumed. Implies: we pause the bank and plan interviews before anything else is asked.

**Sana:** Mid-market customer success teams. Every CSM we talk to is desperate for earlier churn signals.

**Conductor:** That is a category, and "every CSM" is the pattern this bank names as a banned opener, so it triggers the standard pushback rather than acceptance. Push 1 of 2; after the second push the answer is accepted as offered or parked, your call either way. Name one title, at one company, and the consequence that person personally eats when the signal comes late.

**Sana:** Dana Okonkwo, senior CSM at Fernwood Software, runs a book of about 60 accounts. When one churns without warning she sits in the Monday escalation explaining why the first signal was the cancellation email. She has rebuilt a spreadsheet tracker for this three times this year; she showed it to us in the interview on 2026-07-18.

**Conductor:** Accepted, at interview claim with a cited source and date, and the spreadsheet raises it further: an artifact of the workaround is a stronger evidence class than the sentence about it. Attach the export to the discovery folder and DISCOVER-2 is half answered already. Landing this before the next question:

```
## Accepted answers
| DISCOVER-1 | who has this problem | Dana Okonkwo, senior CSM, Fernwood Software: eats the Monday churn escalation | Interview claim (2026-07-18) + workaround artifact | discovery/problem-framing.md, "Who feels it and how often" |

## Evidence ledger
| E4 | The workaround is manual and failing | "I have rebuilt that tracker three times this year and it still missed the Corvale renewal." | Interview notes, D. Okonkwo, filed discovery/research-notes.md | 2026-07-18 | 2026-08-20 | single-source |
```

*(Questions DISCOVER-2 through DISCOVER-4 ran the same way and are omitted: the workaround behavior, its cost per month with the calculation shown, and the cost of doing nothing, all landed in the discovery set. STATE.md shows Next question: DISCOVER-5.)*

**Sana:** We have enough. Let's move to DEFINE, the sponsor wants requirements by Friday.

**Conductor:** The gate decides advancement, not either of us, so here is Gate 1 rendered against the workspace as it stands:

| Gate 1 line | Status | Evidence |
|---|---|---|
| Problem statement is one sentence, stated the same way by everyone | pass | discovery/problem-framing.md, restated identically in the interview notes |
| Five or more real user conversations, cited by source | FAIL | three cited: Okonkwo plus two reviewers, filed in discovery/research-notes.md |
| Personas on fewer than five interviews marked as assumptions | FAIL | personas.md presents two personas as findings, no assumption label |
| Cost of inaction written down, calculation shown | pass | DISCOVER-3 and DISCOVER-4, landed in problem-framing.md |
| A no-go case seriously argued | unknown | nothing in the workspace argues it; DISCOVER-6 not yet asked |
| Gate 6 success signal named now | unknown | DISCOVER-7 not yet asked |
| Go or no-go recorded with rationale | unknown | gate not yet run |

Refused: two lines fail and three are unknown, and an unknown blocks exactly as a fail does. This render is filed as `gates/gate-1-attempt-1.md`, because a refused attempt is a record, not an embarrassment. Your options:

- a) Schedule two more interviews this week and re-render after. Implies: Friday slips, and the gate gets what it actually asks for.
- b) Mark both personas as assumptions and answer DISCOVER-6 and DISCOVER-7 now. Implies: three lines move today; the five-conversation line still fails until the interviews exist, so the gate still cannot pass this week.
- c) Say "advance anyway". Implies: I first force the two highest-stakes unanswered questions, and if you still insist, the skip lands in STATE.md and the risk register naming what was skipped and what it risks, in the gate's own words about products that die of no market need.

Recommended: (b) then (a), because they stack, and (b) costs you twenty minutes now.

**Sana:** (b).

**Conductor:** DISCOVER-6, then. What would make the honest answer no-go? I need a disconfirming condition someone could observe, not reassurance.

**Sana:** If we pull the last two quarters of churned accounts and the signals Radar would surface were not visible earlier than the cancellation, the product cannot work. Ade in data can run that this week.

**Conductor:** Accepted: an observable condition with a named owner. That is also the cheapest test in the whole plan, so it goes to the top of the discovery actions. DISCOVER-7 next, and then I will re-render the gate so today's position is honest in the file.

```
## Journal
| 2026-08-20 | claude-code | DISCOVER-1, -6, -7; gate 1 rendered and refused (attempt 1) | problem-framing.md, personas.md, research-notes.md, gates/gate-1-attempt-1.md |
```

---

## Session 2: into DEFINE, 2026-08-31

**Conductor:** Resuming. I read the product README, STATE.md, and `gates/gate-1-attempt-2.md`, and spot-checked two accepted answers against the artifacts their Landed in column names; both match. Since last session the workspace shows six cited interviews, the churned-account lookback done (signals were visible early in most churned accounts, so the no-go condition did not trigger), and Gate 1 attempt 2 with every line passing, signed by Sana Iqbal and the sponsor on 2026-08-28. Stage is DEFINE. Before any template opens, the three questions that pick the artifact weight.

DEFINE-1. Stakes: what does being wrong here cost, an afternoon, a sprint, a quarter, or a license? Recommended: (b), because the discovery evidence points at one squad and one integration. Options:

- a) An afternoon: reversible, no build. Implies: the honest output is a decision-log entry and no document, and this interview ends there.
- b) A sprint or two. Implies: light weight, likely a one-pager.
- c) A quarter or more, several functions. Implies: full PRD, sponsor signature at Gate 2.
- d) Contracts, funding, or a regulator in scope. Implies: the full BRD, PRD, FRD stack.

**Sana:** (b). One squad, maybe six weeks.

**Conductor:** DEFINE-2, audience, is skipped: `products/renewal-radar/README.md` already names the consuming audience as the CS squad plus the sponsor, and the stakeholder map agrees. Marked accepted with that source; you would have seen a question here otherwise. DEFINE-3. Reversibility: can this be turned off in a day with a flag, or does it set data models or external contracts that outlive the team?

**Sana:** Flag-reversible. It reads from the warehouse; it writes nothing back.

**Conductor:** Then the tree lands on a one-pager with acceptance criteria attached, not the PRD your Friday deadline assumed: no sponsor signature is required before Gate 2 at this weight, and a heavier document would spend a week saying what one page can. That weight choice is itself a decision, so it goes to the decision log with this rationale. Next question after it lands: DEFINE-4, which Gate 1 problem statement each objective traces to.

```
## Position
Stage: DEFINE
Gate attempts: gate 1: attempt 1 refused 2026-08-20; attempt 2 passed and signed 2026-08-28
Next question: DEFINE-4
Overlays active: AI: no. Regulated: no. Decided at: 2026-08-31, decision log entry D-014

## Accepted answers (this session)
| DEFINE-1 | stakes | a sprint or two, one squad | named commitment (owner's call, logged) | definition/one-pager.md, header |
| DEFINE-2 | audience | CS squad + sponsor | accepted by smart skip, source: README.md + stakeholder-map.md | definition/one-pager.md, "Audience" |
| DEFINE-3 | reversibility | flag-reversible, read-only on the warehouse | named commitment | definition/one-pager.md, "Scope" |
```

---

## What this transcript is built to show

The refusal is the product. A runtime that advances on three interviews and unlabeled personas produces a beautiful PRD about a problem nobody verified, and the gate in [os/STAGE-GATES.md](../os/STAGE-GATES.md) exists precisely because that failure is cheap here and expensive later. The cross-examination is not skepticism about Sana, it is the standard applied to every answer: the bank named the evidence class, the first answer missed it, and two pushes later the file holds a name, a date, and a checkable artifact instead of "every CSM". And the weight decision at DEFINE, one page instead of the assumed PRD, is [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md) doing what it was written to do: sometimes the honest output is smaller than the one that was asked for.
