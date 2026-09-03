# New-user session script: golden path and recovery path

Stage: ALL STAGES, run once before any release is tagged
Knowledge: [readiness criteria](criteria.json)
Skill: none. This is a script for a person observing another person

<!-- This file closes EXT-USER in external-gates.json, which requires four
     things: informed consent, observed task outcome, accessibility feedback,
     and issue disposition. It supplies the script and the record; the one
     thing it cannot supply is a participant who did not build this. -->

## Who the participant must be

Someone who did not build this repository. A product manager is ideal but not
required; anyone comfortable with a terminal and a text editor can do it.

They must not be coached during the tasks. That is the entire value of the
exercise: if the participant needs to be told what to do, the documentation
did not work, and that is the finding.

Budget 45 minutes: 5 for consent, 20 for the golden path, 15 for recovery, 5
for the closing questions.

## Before you start

Read this aloud and get an explicit yes. Do not paraphrase it into something
warmer; a participant who does not understand what is recorded has not
consented.

> I am asking you to try a tool I did not design for you specifically, and to
> tell me where it confuses you. I will write down what you did, where you got
> stuck, and what you said about it. I will not record audio or video unless
> you say yes to that separately, and you can say no and still take part.
>
> Nothing you type is sent to any external service. Everything stays on this
> machine.
>
> I am testing the tool, not you. If something is confusing, that is a defect
> I need to find. Getting stuck is the most useful thing you can do.
>
> You can stop at any point, for any reason, without explaining. If you want
> your notes deleted afterwards, say so and I will delete them.
>
> Do you agree to take part?

Record: consent given, by whom, on what date, and whether recording was
separately agreed. Consent that is assumed rather than given does not close
this gate.

## Observer rules

- Do not help. Not even a hint, and not even when it is painful to watch.
- If they are stuck for more than three minutes, say only: *"What are you
  trying to do right now?"* Write the answer down. Then let them continue.
- Write down what they do, not what you think they meant.
- Write their words in quotation marks. Paraphrase drifts.
- Do not defend the tool. If they say it is confusing, the answer is "thank
  you", not an explanation.

## Task 1: the golden path

Give them the repository and this sentence, and nothing else:

> "Set up a workspace for a new product called `acme-payouts`, install the
> discovery document, and check that it is valid."

Start the clock.

**What success looks like** (do not read this to them):

```bash
python3 tools/init_product.py acme-payouts
python3 tools/init_product.py acme-payouts --add templates/discovery/discovery-document.md
python3 tools/init_product.py acme-payouts --check
```

Record for each step: did they find it unaided, from which document, and how
long it took.

| Observation | Record |
|---|---|
| Where did they look first? | |
| Did they find the command without help? | yes / no |
| Time to a created workspace | |
| Time to an installed and validated document | |
| Any command they tried that did not exist | |
| Any error message they could not act on | |
| Exact words when stuck (quote) | |

**The question that matters most:** after `--check` passes, ask *"what do you
think just got checked?"* If they cannot say, the output is reassuring rather
than informative, and that is a P2 finding.

## Task 2: the recovery path

Break it in front of them, so they know it was deliberate and not their fault.
Say: *"I am going to break something on purpose. See if you can work out what
happened and fix it."*

Then run this, with them watching:

```bash
echo "See [the personas](../../templates/discovery/personas.md)" \
  >> products/acme-payouts/discovery/discovery-document.md
```

Give them: *"Something is now wrong with that workspace. Find out what, and
fix it."*

**What success looks like:** they run `--check` or `lint.py --workspace`, read
that a link does not resolve, work out that the depth is wrong, and correct it
to `../../../templates/discovery/personas.md`.

Verified before this script shipped: `--check` reports the file and line, and
the three-dot-segment correction clears it. `--relink` deliberately does
**not** fix this one, and that is correct behaviour rather than a gap: relink
repoints links that already resolve at a workspace copy, and it leaves a link
that resolves nowhere exactly as written rather than inventing a target. If
the participant reaches for `--relink` and it reports "0 links repointed",
watch what they do next. That moment is the most informative part of the task.

| Observation | Record |
|---|---|
| Did they think to re-run a check at all? | yes / no |
| Did the error message tell them which file and line? | yes / no |
| Could they tell what to do from the message alone? | yes / no |
| Did they try `--relink`, and what did they do when it changed nothing? | |
| Time to recovery, or gave up at | |
| Exact words on reading the error (quote) | |

Known cosmetic defect they may notice: the `--check` message currently reads
"link relative link X does not resolve. does not resolve." If they comment on
it, record it; it is already filed and does not need rediscovering.

A participant who cannot recover from a broken link using only the tool's own
output has found a P1: the system detects the problem and does not explain it.

## Task 3: accessibility

Ask directly. Do not infer.

| Question | Response |
|---|---|
| Was any output hard to read? Size, contrast, colour, density | |
| Did anything rely on colour alone to tell you something? | |
| If you use a screen reader, magnifier, or high-contrast mode: did anything break? | |
| Were the tables readable at your terminal width? | |
| Was any wording unclear, jargon-heavy, or condescending? | |
| Anything that made you feel stupid rather than informed? | |

The last row is not padding. Documentation that shames the reader gets
abandoned, and abandonment is the failure mode that never shows up in a test.

## Closing questions

1. What would you tell a colleague this tool is for?
2. What did you expect to happen that did not?
3. What is the single thing you would change first?
4. Would you use this again next week? Why, or why not?

Question 1 is the real test of the README. If their answer does not match what
the project claims to be, the positioning is wrong regardless of how the
tasks went.

## The record

```
Participant           : (name or initials, as they prefer)
Relationship to work  : (must be: did not build this)
Consent given         : yes / no      Date:
Recording agreed      : yes / no / not requested
Observer              :
Commit under test     : ba286db0121e613f5c1a6a6d3bdfa3cc6bee2c27
Date of session       :

Golden path           : completed unaided / completed with prompting / not completed
Time to complete      :
Recovery path         : completed unaided / completed with prompting / not completed
Time to recover       :

Accessibility issues  : (list, or "none reported")
Verbatim quotes       : (at least three)

Findings raised       :
  P0/P1 (blocking)    :
  P2/P3 (non-blocking):

Disposition per finding: fixed / accepted with reason / deferred to task ID
Participant asked for deletion of notes: yes / no
```

Every finding needs a disposition. "Noted" is not a disposition; the gate asks
what happened to each issue, and an issue with no decision against it is an
issue nobody owns.
