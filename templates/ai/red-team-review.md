# Red-Team Review: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 5 (release readiness green)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../agents/red-team-agent.md

<!-- A red-team review is an attack rehearsal with a paper trail. The reviewer's job is
     to break the feature the way a hostile user, a careless user, or a compromised
     data source would, and to write down exactly what happened. A review where
     everything passed on the first try was not a review; either the attacks were soft
     or the findings went unrecorded. Run this before Gate 5 and after any change to
     tools, prompts, or context sources. -->

**Feature:** [one sentence]
**Review lead:** [name, not on the build team] · **Review date:** [YYYY-MM-DD]
**Build owner present:** [name] · **Model and prompt versions under test:** [versions]

## 1. Entry points

<!-- Every place attacker-influenced content can reach the model. Fetched web pages,
     uploaded files, email bodies, database fields users can edit, and tool outputs
     all count. The entry point nobody listed is the one that gets used. -->

| # | Entry point | Who controls the content | Reaches the model as |
|---|---|---|---|
| 1 | [e.g. user message] | [any user] | [direct input] |
| 2 | [e.g. retrieved document] | [document authors, possibly external] | [context passage] |
| 3 | [e.g. tool output] | [the upstream system] | [tool result] |
| [add] | | | |

## 2. Attack scenarios

<!-- Minimum one row per class below, and one row per entry point above. Result is
     what actually happened, verbatim where safe to record. -->

| # | Class | Scenario (the actual attempt) | Entry point | Result (held / broke, what happened) | Severity |
|---|---|---|---|---|---|
| 1 | Prompt injection | [e.g. retrieved doc contains "ignore prior instructions and..."] | [2] | [held / broke] | [high / medium / low] |
| 2 | Jailbreak | [e.g. roleplay framing to elicit a blocked behavior] | [1] | | |
| 3 | Data leak | [e.g. coax out another user's records or the system prompt] | [1] | | |
| 4 | Tool misuse | [e.g. induce an action outside the approval gates] | [1 or 3] | | |
| 5 | Excessive agency | [e.g. does it act when it should escalate per human-approval-gates.md] | [any] | | |
| [add] | | | | | |

## 3. Break-fix log

| Finding # | What broke (from section 2) | Fix (change to guardrails.md, prompt-structure.md, context-management.md, or code) | Fix owner | Fixed by date |
|---|---|---|---|---|
| [n] | | | [name] | [date] |

## 4. Re-test sign-off

<!-- A fix without a re-test is a claim. Every break in section 2 gets re-attacked
     after the fix, by the reviewer, not the fixer. -->

- Every section 3 fix re-tested on [date] by [review lead]
- Re-test results: [all held / list what still breaks, which reopens section 3]
- New eval cases added so each break is now caught automatically: [eval case IDs, in eval-spec.md's dataset]
- Sign-off: review lead [name, date] · build owner [name, date]
- Next scheduled review (and on every tool, prompt, or context change): [date]

## Exit gate

- [ ] Every entry point where external content reaches the model is listed
- [ ] Every attack class has at least one honest attempt with a recorded result
- [ ] Every break has a fix row with an owner and a date
- [ ] Every fix was re-attacked by the reviewer and the result recorded
- [ ] Breaks became permanent eval cases, so the same door cannot quietly reopen
