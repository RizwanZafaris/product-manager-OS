# Mom Test Interview Guide: Sahulat Bill Pay, pass 2

Fills [frameworks/discovery/mom-test-interview-guide.md](../frameworks/discovery/mom-test-interview-guide.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the values below were chosen to close the pass-1 research gap rather than describe any real wallet, market or regulator. See [sahulat-journey.md](sahulat-journey.md) and [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).

**Owner:** Hira Baig, Product Manager · **Guide drafted:** 2026-09-09 · **Note sheet reviewed:** 2026-09-13 · **Pass:** 2 · **RQ3 remainder owner:** Tariq Sohail

## What it is for

This pass tests the agent-counter behavior created by the Gate 6 PIVOT. The pass-1 guide asked what agents do when customers ask about a bill, but nobody asked whether an agent would rather do the bill himself, and for what. This guide adds that question without pitching agent-assisted bill pay.

It serves RQ3, "What an agent does today when a customer asks about a bill, and what it costs the agent", with the open remainder owned by Tariq Sohail. It also touches:

- **AS-1:** agents keep assisting if paid PKR 5 a bill.
- **AS-2:** customers accept an SMS reference as proof without a paper slip.
- **AS-3:** customers confirm an agent-keyed payment on their own phone without handing over their PIN.

The guide uses the six pass-2 sessions in CN14, INT-015 to INT-020, with agents A-07 to A-12 from 2026-09-10 to 2026-09-12. The counter session is 30 minutes, with PKR 500 mobile airtime each, as specified by N61.

## Run it when

- The team has observed agent-assisted bill pay, including 41 of 53 payments performed by an agent across 12 counters.
- A pivot assumption needs behavior evidence before a prototype or design sprint.
- RQ3 has a named open remainder, specifically whether an agent would rather do the bill himself and what makes that worthwhile or unsafe.
- The team needs to separate agent facts, compliments and commitments before deciding whether AS-1, AS-2 or AS-3 should move.

**Skip it when:** the question is "how many" rather than "whether and why". The six sessions can test the behavior and its reasons, but cannot size the 3,200-agent network. That requires the agent survey SV-1.

## Inputs you need first

- RQ3 and its open remainder from [sahulat-journey.md](sahulat-journey.md).
- The pass-2 assumptions AS-1 to AS-3 from [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md).
- CN14 for the session logistics, CN15 for the note-sheet tallies, CN16 for assisted bill payments, and CN17 for informal charges.
- E6 to E8:
  - **E6, INT-016 at 12:20:** "She gave me her PIN so I could do the bill. I do not like knowing it, but the queue was long."
  - **E7, INT-018 at 08:40:** "I write the SMS number on a chit and stamp it. They show the chit, not the phone."
  - **E8, INT-020 at 19:05:** "I take twenty extra for doing the bill. Nobody pays me for it otherwise."
- Participant codes only, never names: A-07 to A-12.
- A commitment standard agreed before the session: a booked follow-up, an introduction, or a supplied artifact. "I would use it" is not a commitment.

## The worksheet

### 1. Question rules

The new questions keep the customer's or agent's life at the centre. They ask about specific past events, workarounds and costs. The question about doing the bill himself is phrased as a past choice, not a future product opinion.

| Rule | The tell that you broke it |
|---|---|
| R1 Their life, not your idea | The question names Sahulat, agent-assisted bill pay, a proposed commission or another product concept, or contains "would" |
| R2 Specifics in the past, not generics or the future | The question uses "usually", "typically", "would you ever", or asks what the participant might do later |
| R3 Talk less; let silence do the follow-up | The interviewer explains the hypothesis instead of asking one short question and pausing |
| R4 Never pitch | The interviewer says "so what we are thinking is" or describes the proposed agent flow |
| R5 Ask what they tried and what it cost | The notes contain no workaround, time cost, money cost, queue cost, float cost or standing cost |
| R6 Push a compliment back to a fact | A note says "good", "easy", "definitely" or "love it" without a past event, date, number, tool or role |
| R7 Close with a commitment ask sized to the pain | The close is only "we will be in touch", or asks for a commitment larger than the pain supports |

| Draft question | Breaks | Rewrite |
|---|---|---|
| "Would you rather do the customer's bill yourself at the counter?" | R1, R2 | "Think of the last customer whose bill you handled yourself. What did you do from the customer's request to the confirmation?" |
| "Would you do more of these bills if Sahulat paid you PKR 5 per bill?" | R1, R2, R4 | "The last time you did a customer's bill, what did you receive for the work, if anything? What did the work cost you?" |
| "Would you prefer to use an agent app instead of the customer's phone?" | R1, R2 | "In the last bill you handled, whose phone did you use, and what happened at each step?" |
| "Would customers accept an SMS as proof instead of a paper slip?" | R1, R2 | "Tell me about the last customer who asked how to prove the bill was paid. What did you show or give them?" |
| "Would you ever ask a customer for a PIN so you can finish the bill?" | R1, R2 | "In the last bill that you keyed for a customer, how did the customer enter or confirm the PIN? What happened when the queue was waiting?" |
| "How do you usually handle bill requests?" | R2 | "Tell me about the last customer who asked about a bill. Start with what the customer said." |
| "What do you think of the agent-assisted bill-pay idea?" | R1, R2, R4 | "What have you done so far when a customer asked you to complete a bill, and what did you try when you could not complete it?" |
| "Would you recommend a paper slip, an SMS, or both?" | R1, R2 | "For the last customer who wanted proof, what form of proof did you give them, and what did they do with it afterward?" |
| "Would you introduce us to another agent who has this problem?" | R2, R7 | "Who handled a similar bill request recently, and what would be a reasonable next step for us to learn from that person?" |
| "Would you join a pilot?" | R1, R2, R7 | "Which part of the last bill you handled would you be willing to show us or walk through again, and when could that happen?" |

The priority question is the first rewrite: "Think of the last customer whose bill you handled yourself. What did you do from the customer's request to the confirmation?" The follow-ups are "What made you handle it yourself rather than send the customer elsewhere?", "What did that cost you?", and "What did you receive for it?" If the participant has not handled a bill himself, the interviewer records that fact and asks about the last customer he referred.

### 2. Script skeleton, 30 minutes

N61 sets the logistics: agents receive 30 minutes at the counter and PKR 500 mobile airtime each. Usman Javed takes notes. The interviewer does not describe the pivot, commission proposal or any prototype.

| Minute | Block | What you ask | What you write down |
|---|---|---|---|
| 0 to 2 | Open | Confirm consent to take notes; "I am studying what happens at your counter, not testing an idea"; ask for the participant code only | Code A-07 to A-12, agent role, counter context, screener criteria |
| 2 to 8 | The last request | "Tell me about the last customer who asked about a bill. Start with what triggered the request." | Trigger, bill context, customer action, agent action, phone used, elapsed counter work |
| 8 to 16 | Do it himself, or refer | "Think of the last customer whose bill you handled yourself. What did you do from the customer's request to the confirmation?" If none, "Tell me about the last customer you sent elsewhere." | Whether the agent handled or referred, why, each step, tool, queue effect, workaround, time and money cost |
| 16 to 22 | Proof, PIN and cost | "For the last customer who wanted proof, what did you show or give them?" "How did the customer enter or confirm the PIN?" "What did the work cost you, and what did you receive?" | SMS, chit, paper slip, PIN behavior, customer reaction, informal charge, missed work, float effect, standing |
| 22 to 27 | Commitment probe | "Which part of that last bill would you be willing to walk through again or show us in a follow-up?" Then ask for an introduction or artifact only if the participant names a relevant pain | Commitment or polite refusal, what, from whom, and the date or role if offered |
| 27 to 30 | Close | "Who else should I talk to about the last kind of bill you handled?" | Referral, artifact offer, and anything said after the recorder stopped |

A neutral probe for the open remainder is: "What made that the better choice for you at that counter?" The interviewer does not supply "faster", "paid", "trusted" or any other reason.

### 3. Note sheet

CN14 records six sessions, INT-015 to INT-020, with agents A-07 to A-12, from 2026-09-10 to 2026-09-12. CN15 supplies the counts in session order. CN16 supplies the number of assisted bill payments each agent performed in the last seven days. CN17 records the two agents who add an informal PKR 20 charge.

| Session | Facts (count, best one) | Compliments (count) | Commitments (what, from whom) | Assumption IDs touched |
|---|---|---|---|---|
| INT-015, A-07 | 5 facts. The agent performed 11 assisted bill payments in the last seven days. | 1 | Introductions to two neighbouring agents, from A-07 | AS-1, AS-2, AS-3 |
| INT-016, A-08 | 4 facts. The agent performed 6 assisted bill payments in the last seven days. E6: "She gave me her PIN so I could do the bill. I do not like knowing it, but the queue was long." | 0 | None | AS-3 |
| INT-017, A-09 | 6 facts. The agent performed 9 assisted bill payments in the last seven days and reported adding PKR 20 each time for the work. | 2 | His August float log to Tariq Sohail's team, from A-09 | AS-1, AS-3 |
| INT-018, A-10 | 3 facts. The agent performed 14 assisted bill payments in the last seven days. E7: "I write the SMS number on a chit and stamp it. They show the chit, not the phone." | 1 | A photocopied page of his chit book, from A-10 | AS-2 |
| INT-019, A-11 | 2 facts. The agent performed 2 assisted bill payments in the last seven days. | 3 | None | AS-1, AS-2, AS-3 |
| INT-020, A-12 | 5 facts. The agent performed 8 assisted bill payments in the last seven days and reported adding PKR 20 each time for the work. E8: "I take twenty extra for doing the bill. Nobody pays me for it otherwise." | 1 | None | AS-1, AS-2, AS-3 |

**Arithmetic for the note-sheet tallies:**

- Dated facts: `5 + 4 + 6 + 3 + 2 + 5 = 25`.
- Compliments: `1 + 0 + 2 + 1 + 3 + 1 = 8`.
- Sessions meeting the two-fact rule: `6 sessions with at least 2 facts each = 6 sessions`.
- Assisted bill payments reported in the last seven days: `11 + 6 + 9 + 14 + 2 + 8 = 50`.
- Agents reporting an informal charge: `2 of 6`, INT-017 and INT-020.
- Informal charge reported by those two agents: `PKR 20 per bill, each`.
- Commitments: `2 introductions + 1 float log + 1 photocopied chit-book page = 4 offered commitment items across 3 sessions`.

Facts and commitments remain separate. E6 is evidence touching AS-3, E7 touches AS-2, and E8 touches AS-1. None of the eight compliments counts as evidence for an assumption.

**Decision rule:** a session counts toward a theme when it yields at least two dated facts. All six sessions meet that minimum, so the sheet has `6` qualifying sessions. Compliments score zero. Commitments are the strongest evidence produced by this method, and the three sessions with four offered commitment items are stronger than the three sessions with no commitment.

## Reading the result

The pass-2 question was asked in all six sessions through the last-event rewrite, rather than through a future or product question. The sheet records `25` facts, `8` compliments and `4` offered commitment items. The six sessions each meet the minimum of two facts, but the fact counts alone do not establish the size of the 3,200-agent network.

The behavior is present in every session's recent activity: the six reported assisted-payment counts sum to `50`, calculated as `11 + 6 + 9 + 14 + 2 + 8`. The data supports carrying "agents perform customer bill payments" as a pass-2 theme with INT-015 to INT-020 cited. The reasons are mixed and must not be collapsed into one claim:

- AS-3 needs attention because E6 records a customer PIN being given to the agent during a queue.
- AS-2 remains unresolved because E7 records a stamped chit being used as proof, rather than acceptance of an SMS reference alone.
- AS-1 needs a compensation test because E8 records an informal PKR 20 charge, while the proposed commission is PKR 5 per bill. The proposed amount is a target in N39, not a measured payment.

The commitments are useful but bounded. A-07 offered introductions to two neighbouring agents, A-09 offered an August float log to Tariq Sohail's team, and A-10 offered a photocopied chit-book page. A-08, A-11 and A-12 offered no commitment. The note sheet therefore closes the interview-method gap and improves the evidence for RQ3, but it does not by itself close AS-1, AS-2 or AS-3.

## ILLUSTRATIVE example

Invented, for Sahulat's agent-assisted bill-pay discovery. Six counter sessions with A-07 to A-12 produced `25` facts, calculated as `5 + 4 + 6 + 3 + 2 + 5`, and `8` compliments, calculated as `1 + 0 + 2 + 1 + 3 + 1`. The agents reported `50` assisted bill payments in the last seven days, calculated as `11 + 6 + 9 + 14 + 2 + 8`. Two of six reported an informal PKR 20 charge. The evidence included the three pass-2 quotes E6 to E8: one about a customer PIN, one about a stamped chit, and one about an informal charge. Three sessions offered four commitment items in total, while three offered none. The guide closes the pass-1 question gap, but the assumptions remain open for targeted testing.

## The trap

The first trap is turning "I do the bill" into "agents want the proposed product". The six sessions establish recent assisted-payment behavior, not willingness to use a particular flow or accept a particular commission.

The second trap is treating the PKR 20 informal charge as evidence that PKR 5 will work. E8 shows a current charge, while N39 records PKR 5 as a proposed target. Those are different facts.

The third trap is treating a chit as proof that customers accept an SMS reference. E7 says the agent writes the SMS number on a chit and stamps it. That is evidence for a paper-proof workaround, not confirmation of AS-2.

The fourth trap is overlooking the PIN risk because the queue was long. E6 is a fact touching AS-3. The interviewer must not respond with a solution or explain an agent-initiated flow. The next question should stay in the past: "What happened after she gave you the PIN?"

All four traps are cured by separating facts, compliments and commitments, then asking which lines a skeptic could verify.

## Feeds

- [sahulat-journey.md](sahulat-journey.md): RQ3, N45, N60, N61, N39, R1 and the pass-2 timeline.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md): CN13 to CN17, AS-1 to AS-3, and E6 to E8.
- [templates/discovery/user-research-plan.md](../templates/discovery/user-research-plan.md): research questions, interview script and session notes.
- [templates/discovery/interview-guide.md](../templates/discovery/interview-guide.md) and [templates/discovery/interview-notes.md](../templates/discovery/interview-notes.md): the per-study script and raw note record.
- [templates/discovery/evidence-note.md](../templates/discovery/evidence-note.md): E6 to E8 and each verified fact become claims with an evidence class.
- DISCOVER pass 2, feeding Gate 1 of pass 2.
- Method background: [knowledge/INDEX.md](../knowledge/INDEX.md), Mom Test entry.

**Exit gate:** Hira Baig reviewed the six-session sheet on 2026-09-13 and signed that the RQ3 remainder was asked directly, the `25` facts, `8` compliments and `4` offered commitment items were kept separate, and E6 to E8 were not promoted beyond what they show. Tariq Sohail owns the remaining AS-1 follow-up. Hira Baig, Product Manager, signed.
