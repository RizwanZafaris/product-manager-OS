---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["User Research Plan", "user-research-plan"]
---
# User Research Plan: [study short name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Knowledge index, Mom Test entry](../../knowledge/INDEX.md)
Skill: [research-agent](../../agents/research-agent.md) for fielding, [feedback-synthesis](../../skills/feedback-synthesis/SKILL.md) for section 6

<!-- Plan the study before you talk to anyone, and keep the notes in the same file
     so evidence never separates from method. This template holds four things: the
     questions you need answered, the method and screener, the interview script,
     and one notes block per session plus a synthesis section.

     The interviewing rules here are based on the ideas in The Mom Test by Rob
     Fitzpatrick, restated in this repo's own words: ask about the person's past
     behavior and current workarounds, never about whether they like your idea;
     compliments and hypothetical enthusiasm are noise; commitments of time,
     money, or reputation are signal. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Planned / Fielding / Synthesized

## 1. Research questions

<!-- What the TEAM needs to learn, not what you will ask the participant. Three to
     five. Each one should be answerable by evidence a session can produce. -->

| # | Research question | Why it matters to the decision at hand |
|---|---|---|
| RQ1 | | |
| RQ2 | | |
| RQ3 | | |

## 2. Method

<!-- The method follows the question, not the calendar. Say what it cannot
     tell you as well as what it can: an interview cannot measure frequency,
     and a survey cannot explain why. -->


- **Method:** [semi-structured interviews / contextual observation / diary study / survey / usability session]
- **Why this method answers the RQs:** [one or two sentences]
- **Sessions planned:** [count; five to eight interviews per segment is a workable floor for pattern-finding]
- **Session length:** [minutes] · **Recording:** [yes or no, and where consent is captured]
- **Incentive:** [what, if anything, participants receive]

## 3. Screener

<!-- Who qualifies. Screen on behavior, not attitude: "filed an expense report in
     the last 30 days" screens better than "cares about expenses". -->

| Criterion | Include if | Exclude if |
|---|---|---|
| [behavior in the last N days] | | |
| [role or segment] | | |
| [tool or context in use] | | |

**Recruiting source:** [where participants come from, and who books them]

## 4. Interview script

<!-- Openers, then behavior questions, then the deep dive. Never pitch. If you
     catch yourself explaining the product idea, the session has stopped
     producing evidence. -->

**Opening (2 minutes):** [introduce yourself, confirm consent to record, state that there are no wrong answers and you are studying the problem, not testing them]

**Warm-up:**
1. Walk me through the last time you [target activity]. Start from what triggered it.
2. What did you do right before and right after?

**Behavior and pain:**
3. Where did that go slower or worse than you wanted?
4. What have you already tried to fix or route around it? What did that cost you?
5. When it went wrong, what did it affect downstream?

**Prioritization:**
6. Of everything we discussed, what would you fix first? Why that one?

**Commitment probe (signal, not sale):**
7. If a fix for [the pain they named] existed, what would you be willing to do next: try a rough version, introduce us to a colleague, put time on a calendar?

**Close:** [thank them; ask who else you should talk to]

## 5. Session notes

<!-- Duplicate this block once per session. Keep raw observation separate from
     your interpretation: the observation column is what happened; the
     interpretation column is what you think it means. Future readers must be able
     to disagree with your interpretation while trusting your observation. -->

### Session [ID: INT-001]

- **Date:** [YYYY-MM-DD] · **Participant:** [code, not name, if notes are shared] · **Segment:** [segment]
- **Screener criteria met:** [list]

| Timestamp | Observation (what was said or done) | Interpretation (what it might mean) | RQ touched |
|---|---|---|---|
| | | | |

**Strongest moment of the session:** [one sentence]
**Commitments made, if any:** [time, intro, follow-up; or "none"]

## 6. Synthesis themes

<!-- Fill after at least five sessions. A theme needs three or more independent
     sessions behind it. Two mentions is a coincidence to watch, not a theme. -->

| Theme | Sessions supporting it (IDs) | Contradicting sessions (IDs) | Confidence (high / medium / low) | So what: implication for the product decision |
|---|---|---|---|---|
| | | | | |

**Surprises:** [what the team believed before the study that the sessions contradicted]

**Answers to the research questions:**

| RQ | Answer as evidenced | Open remainder |
|---|---|---|
| RQ1 | | |

---

## How this plan fails

<!-- Research is the cheapest place to get a confident wrong answer, because
     every failure below still produces findings, and findings get quoted. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Recruiting people who already like you | The screener quietly selects current, happy, engaged users | Screen for the population the question is about, and cap prior usage |
| Leading questions | "How much would this help you?", about a feature you want to build | Two people review the guide for leading wording before it is used |
| Sample size by convenience | A number chosen from recruiter availability, justified afterwards | Set it from the method: per segment, or until sessions stop producing new themes |
| No analysis plan | The guide is written, transcripts arrive, themes are invented while reading | Write how findings will be coded and how they map to the decision, before fielding |
| Run to justify a decision | The conclusion arrives with the brief | Ask the requester in writing what result would change the plan. If none, do not run it |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- The field that stops research being theatre is the last one. Delete once
     real content exists. -->

| Field | Filled |
|---|---|
| *Decision this informs* | *Whether to build in-app correction before launch, or ship extraction alone* |
| *What result would change the plan* | *If fewer than a third of reps hit a wrong extraction in two weeks of real use, correction waits* |
| *Population* | *Field reps who file at least four expenses a month, excluding pilot participants and anyone in the design partner programme* |
| *Method and its limits* | *Diary study over two weeks. It can tell us frequency and what people did next. It cannot tell us why they chose not to correct, which needs follow-up interviews* |
| *Sample* | *Twelve, or until three consecutive diaries produce no new theme* |
| *Analysis plan, written before fielding* | *Code each entry for: extraction correct, incorrect and corrected, incorrect and submitted anyway. Themes map to the decision above and nowhere else* |
| *Consent and incentive* | *Written consent covering data use, retention of eight weeks, and withdrawal at any point. Incentive stated up front and not contingent on completing* |

*The second row is the one most plans omit. A stakeholder who cannot say what result would change the plan is asking for a document, not a study.*

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


- [ ] Every research question maps to a live decision, not curiosity
- [ ] Screener screens on behavior, not attitude
- [ ] Script contains no pitch and no "would you use" questions
- [ ] At least five sessions completed and noted in this file
- [ ] Every theme cites three or more supporting session IDs and lists contradictions
- [ ] Each RQ has an evidenced answer or an explicit open remainder
