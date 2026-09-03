# Mom Test interview guide

Based on the ideas of Rob Fitzpatrick, from The Mom Test (2013). Explained here in this repository's own words.

## What it is for

An interview produces evidence only when it asks questions politeness cannot answer. The Mom Test's rules make that possible: talk about the customer's life, not your idea; ask about specific things that already happened, not opinions about the future; listen more than you talk. This guide turns the rules into a rewrite table for your questions, a 30-minute script skeleton, and a note sheet that keeps facts, compliments, and commitments apart. It improves one decision: whether the problem is real, frequent, and costly enough to carry to Gate 1.

## Run it when

- The problem statement in [problem framing](../../templates/discovery/problem-framing.md) rests on team belief and you are about to recruit.
- A sales request or an executive hunch needs its pain confirmed by the people who feel it.
- A draft script needs a pre-flight check before the first session burns a participant.

**Skip it when:** the question is "how many" rather than "whether and why". Eight interviews cannot size a segment or rank twelve outcomes; that is survey work through [survey design](../../templates/discovery/survey-design.md).

## Inputs you need first

- Research questions from [user research plan](../../templates/discovery/user-research-plan.md) section 1, and a screener on behavior (filed a report in the last 30 days) from section 3.
- The assumptions the interviews could bust, with IDs from the [assumptions register](../../templates/definition/assumptions-register.md).
- The commitments you would accept as signal, decided before the session; participant codes, never names.

## The worksheet

### 1. Question rules

<!-- Run every draft question through the rules; rewrite the ones that fail. -->

| Rule | The tell that you broke it |
|---|---|
| R1 Their life, not your idea | The question names your product or contains "would" |
| R2 Specifics in the past, not generics or the future | "Usually", "typically", "would you ever" |
| R3 Talk less; let silence do the follow-up | Your share of the transcript is above a third |
| R4 Never pitch | You said "so what we are thinking is" |
| R5 Ask what they tried and what it cost | No workaround in the notes |
| R6 Push a compliment back to a fact | The note says "loved it" with no date |
| R7 Close with a commitment ask sized to the pain | The close is "we will be in touch" |

| Draft question | Breaks | Rewrite |
|---|---|---|
| "Would you use a copilot that files expenses for you?" | R1, R2 | "Walk me through the last report you filed. What took longest?" |
| [your question] | [R1 to R7] | [rewrite] |

### 2. Script skeleton, 30 minutes

| Minute | Block | What you ask | What you write down |
|---|---|---|---|
| 0 to 2 | Open | Consent to record; "I am studying the problem, not testing you"; no product description | Code, segment, screener criteria met |
| 2 to 8 | The last time | "Tell me about the last time you [did the job]. Start from what triggered it." | Trigger, steps, tools, elapsed time, date |
| 8 to 16 | Pain and workaround | "Where did it go slower or worse than you wanted? What have you tried? What did that cost?" | Each workaround and its cost in time, money, or standing |
| 16 to 22 | Stakes | "When it went wrong, who noticed? What happened downstream?" | Who else feels it; how often; the number attached |
| 22 to 27 | Commitment probe | "If [the pain they named] went away, what would you do next: try a rough version, introduce us to [role], put 30 minutes on a calendar?" | The commitment or the polite refusal, verbatim |
| 27 to 30 | Close | "Who else should I talk to?" | Referrals; anything said after the recorder stopped |

### 3. Note sheet

<!-- Three columns kept apart during the session. A fact is a specific past event with a
     date, a number, a tool, or a role attached. A compliment is praise or hypothetical
     enthusiasm: "definitely", "love", "cool". A commitment costs the participant something
     today: time (a booked follow-up), reputation (an introduction), or money (a pilot, a
     budget line, a purchase order). -->

| Session | Facts (count, best one) | Compliments (count) | Commitments (what, from whom) | Assumption IDs touched |
|---|---|---|---|---|
| INT-001 | | | | |

**Decision rule:** a session counts toward a theme when it yields at least two dated facts. Compliments score zero, whatever the mood in the room. Commitments are the strongest evidence the method produces.

## Reading the result

After five to eight sessions per segment, tally the sheet. Facts converging across three or more independent sessions make a theme; carry it into the research plan's section 6 with the session IDs. One commitment beyond politeness outweighs ten compliments; two from different organizations say the pain is worth a one-pager. Sessions that produced only compliments mean the pain is not real or the questions were leading; reread the transcripts against the rules before recruiting anyone else. Facts without commitments mean the pain exists and is tolerable: log it and move on.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Seven sessions with field sales and consulting staff who filed a report in the last 30 days. Five produced dated facts about the same event: reports filed in one sitting on the last weekend of the quarter, 30 to 40 minutes each, at least one receipt missing per report, one participant repaid 160 dollars out of pocket after a rejected line. Compliments ("an AI for this would be amazing") were logged as zero. Commitments: a regional sales manager booked a follow-up with the finance operations lead; a consultant offered a redacted export of a quarter's reports. Two fact-rich themes and two commitments across two firms: the problem framing moves to Gate 1 with seven sessions cited.

## The trap

The interviewer hears a commitment that is not there. A participant says "we would definitely buy this" and the sheet records a commitment because it sounded like one. It is a compliment with a future tense. A commitment has a date, a named role, or a dollar figure, and it costs the participant something today. The second form of the failure is the pitch leak: in minute four you "give some context" about the copilot, and the remaining 26 minutes are feedback on your idea. Both are cured by the same habit: after every session, ask which lines in the notes a skeptic could verify.

## Feeds

- [User research plan](../../templates/discovery/user-research-plan.md): section 4 (interview script) and section 5 (session notes)
- [Interview guide](../../templates/discovery/interview-guide.md) and [interview notes](../../templates/discovery/interview-notes.md): the per-study fills of the script and the note sheet
- [Evidence note](../../templates/discovery/evidence-note.md): each fact or commitment becomes a claim with an evidence class
- DISCOVER, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- Method background: [knowledge index, Mom Test entry](../../knowledge/INDEX.md); [jobs to be done](../../knowledge/jobs-to-be-done.md) for the switch-interview variant
