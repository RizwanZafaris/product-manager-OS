# Interview Guide: Sahulat Bill Pay

Fills [templates/discovery/interview-guide.md](../templates/discovery/interview-guide.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, the fourteen research sessions and every quoted line in this guide's design notes are fiction, and the session-length totals in section 2 carry an ILLUSTRATIVE label back to the data sheet; the per-block minute allocations below are this guide's own scheduling, not listed there. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-01-28 (v2; first piloted 2026-01-26) · **Last updated:** 2026-08-28 · **Status:** In use; v1 on INT-001 and INT-002, v2 on INT-003 to INT-014 · **Research plan:** [sahulat-user-research-plan.md](sahulat-user-research-plan.md), sections 2 and 4 · **Guide version:** v2 · **Data sheet:** [sahulat-journey.md](sahulat-journey.md)

## 1. Research questions this guide serves

| RQ | Question the team needs answered | Blocks that serve it |
|---|---|---|
| RQ1 | How households pay utility bills today, and what each payment costs in time, money and surcharge | Block A, Block B, Block C, Block E, customer track |
| RQ2 | What happens to money between a cash-in and the moment it leaves the wallet, and what decides the timing | Block A, Block B, Block D, customer track |
| RQ3 | What an agent does today when a customer asks about a bill, and what it costs the agent | Block A, Block B, Block C, Block D, Block E, agent track |
| RQ4 | Where USSD sessions fail from the customer's side, and what the customer does next | Block B, Block D, customer and agent tracks |

## 2. Session logistics

- Length: 45 minutes for the eight customer sessions, C-01 to C-08 (ILLUSTRATIVE, N61, decided) · 30 minutes for the six agent sessions, A-01 to A-06, at the agent's own counter (ILLUSTRATIVE, N61, decided)
- Format: in person. Customers are met at home or nearby; agents are interviewed in context at the counter, between customers, per the [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md), which treats the agent as a persona and a channel in its own right, not a stand-in for the wallet holder
- Roles: lead interviewer Hira Baig, note-taker Usman Javed; the lead never takes notes
- Consent and recording: verbal consent is asked before notes begin, including consent to record audio on the interviewer's phone; a participant code (C-01 to C-08, A-01 to A-06) replaces the name from the first line. Open: Amna Rasheed owns the long-term archive for consent slips and audio; working copies sit on the research shared drive under the session id
- Incentive: PKR 500 mobile airtime per session (ILLUSTRATIVE, N61, decided)

## 3. Opening (2 minutes customers, 1 minute agents)

Customer track: "Hi, I'm Hira, I work on the Sahulat wallet, and this is Usman. I'd like to understand how your household handles the electricity and gas bills today, not anything we're building. There are no wrong answers, and I'll mostly ask about things that actually happened. With your permission we'll also record the audio on my phone, and Usman takes notes; we'll use a code, not your name, in anything written down. If you ask what we're building, I'll happily tell you at the end; first I want to understand how this works for you today. About forty-five minutes, is that alright?"

Agent track: "Hi, I'm Hira from Sahulat's product team, this is Usman. I want to understand what happens when a customer asks you about a bill, not anything we're building. There are no wrong answers, and I'll mostly ask about things that actually happened. With your permission we'll also record the audio on my phone, and Usman takes notes; we'll use a code, not your name, in anything written down. If you ask what we're building, I'll happily tell you at the end; first I want to understand how this works for you today. About thirty minutes, and if a customer comes in, we stop and wait."

## 4. Question blocks

### Block A: context (RQ: RQ1, RQ2, RQ3; 5 minutes customers, 3 minutes agents)

| Question | Probes | Listening for |
|---|---|---|
| [Customer] Tell me about the bills your household pays every month, electricity, gas, water, anything else, and who usually deals with them. | How often does each one come due? Who else in the house is involved? | frequency, actors, which bills (feeds N22) |
| [Agent] Tell me about a normal day at your counter, where Sahulat cash-in and cash-out sit against everything else you sell. | How many Sahulat customers on a normal day? What do most of them come in for? | frequency, counter routine, where a bill question would land |

### Block B: the last time (RQ: RQ1, RQ2, RQ3, RQ4; 12 minutes customers, 8 minutes agents)

| Question | Probes | Listening for |
|---|---|---|
| [Customer] Walk me through the last time you paid an electricity or gas bill, from when you knew it was due to when it was actually paid. | What did you do right before? What happened after? Show me the bill if you have it. | the real sequence, the trip, the fee (feeds N18 to N20) |
| [Customer] Where did that go slower or worse than you wanted? | What did you do about it? What did that cost you, time, money, standing? | pain with a cost attached |
| [Customer] The last time money sat in your Sahulat wallet for more than two days, what was it for? | What made you leave it there instead of cashing out? What happened to it in the end? | RQ2, the v2 replacement question, see section 7 |
| [Customer] Tell me about the last time a Sahulat session on your phone or the short code stopped in the middle. What happened next? | Did you know whether the money had moved? What did you do, wait, dial again, go to the agent? | RQ4, dropped-session behavior |
| [Agent] Tell me about the last time a customer's Sahulat session stopped in the middle at your counter. What happened next? | Did the customer know whether the money had moved? What did you tell them to do? | RQ4, dropped-session behavior from the agent's side |
| [Agent] Tell me about the last time a customer asked you about paying a bill. | What did you tell them? Where did you send them? What did you get out of it? | RQ3, the referral pattern and the fee it carries |

### Block C: workarounds and tools (RQ: RQ1, RQ3; 8 minutes customers, 5 minutes agents)

| Question | Probes | Listening for |
|---|---|---|
| [Customer] What have you tried to make paying bills easier, or to avoid the trip? | Did you pay for anything, a bill shop, a relative's help? Who set it up? | spend, effort, ownership (feeds N63) |
| [Customer] What did you stop using to pay a bill, and why? | What was the moment you gave up on it? | switching evidence |
| [Agent] What do you already do for a customer who cannot get to the bill shop or the bank branch? | Where do you send them? What does that shop charge? | informal bill-paying already happening at the counter (feeds N21) |

### Block D: forces (RQ: RQ2, RQ3, RQ4; 10 minutes customers, 6 minutes agents)

| Question | Probes | Listening for |
|---|---|---|
| [Customer] When you last thought about changing how you pay a bill, what got in the way? | What would have had to be true first? Who else had a say? | anxiety, habit |
| [Customer] What would make it worth the hassle of changing how you pay? | Has anything come close? | pull |
| [Agent] When you last thought about doing a customer's bill yourself instead of sending them across the road, what stopped you? | What would have had to be true first? Who else had a say? | RQ3, push and anxiety on the agent's side |
| [Agent] When a bill payment for a customer you referred goes wrong, a wrong reference, a late posting, what happens next? | Who does the customer blame? What do you do about it? | RQ3, agent exposure to a failed payment |

### Block E: priority and commitment (RQ: RQ1, RQ3; 5 minutes customers, 5 minutes agents)

| Question | Probes | Listening for |
|---|---|---|
| [Customer] Of everything we talked about, what would you fix first about paying bills, and why that one? | What would you do with the time or money back? | ranked pain |
| [Customer] If a fix for the trip and the fee you just described existed, what would you do next: try it with your next real bill, introduce us to a neighbour, put a visit on the calendar? | When? | commitment, not a compliment |
| [Agent] What did you earn from the last customer you sent to the bill shop? | Was that typical? What is the most and least you have made off a referral? | RQ3, referral economics, past behavior only |

## 5. Question rules

| Never ask | Because | Ask instead |
|---|---|---|
| "Would you keep money in the wallet if you could pay bills?" | hypothetical enthusiasm is free; this is the exact question v1 asked before it was cut, see section 7 | "The last time money sat in your wallet for more than two days, what was it for?" |
| "Do you think a bill-pay feature would help people like you?" | it leads the witness | "When did paying a bill last cost you more than the bill itself, in a trip, a fee, or a surcharge? What happened?" |
| "How much would you pay to skip the trip to the bill shop?" | nobody prices a trip in the abstract | "What do you spend on this today, including the fare and the shop's fee?" |
| Anything that names Sahulat's bill-pay plans before the close | the session stops producing evidence the moment the idea is on the table | park it for the close |

## 6. Close (3 minutes customers, 2 minutes agents)

- Thank them; ask who else is worth talking to, an introduction on the spot if one is offered
- Ask for the artifacts they mentioned: the bill itself if not already shown, a bill-shop receipt, any message from Falak Telecom about a dropped session
- Only now, if asked, describe the idea in one sentence: "we're looking at whether you could pay a Ravi Power or Chenab Gas bill straight from the wallet." Record the reaction as a compliment, not evidence
- Confirm follow-up: what they agreed to and by when, including whether Usman may observe them at the agent counter the next time a bill is paid; goes to interview-notes.md section 5

## 7. Pilot and revision log

| Version | Date | What changed | Why (session id) |
|---|---|---|---|
| v1 | 2026-01-19 | First draft, built from the research plan's RQ1 to RQ4; v1's Block D closed with "Would you keep money in the wallet if you could pay bills?" | drafted from the research plan, not yet tested |
| v1, piloted | 2026-01-26 | Piloted unchanged on the first two sessions | INT-001, INT-002 |
| v2 | 2026-01-28 | Cut "Would you keep money in the wallet if you could pay bills?" from Block D. Both pilot participants answered yes within a second and had no story behind the answer, which section 5's own rule says is not evidence. Replaced it in Block B with "the last time money sat in your wallet for more than two days, what was it for?", a past-event question with the same research aim. This is the question every session from INT-003 onward actually ran | INT-001, INT-002 |

**Retrospective note, added 2026-08-28.** The cut question was the hypothesis wearing a question mark: it asked customers to imagine keeping a balance rather than to report a time they had. Its replacement is where the evidence split. INT-003 answered it with a salary that stays in the wallet for days, filed as E5 and built into the persona Kamran; INT-004 answered it at 19:00 with no recall of money ever sitting two days, just after the E2 line at 18:35. Both are honest and both are in the record; deciding which household was more common was the research plan's job at synthesis, not this guide's, and it is the judgment DESIGN later got wrong when it scored the balance-keeper risk low. The guide's job ends at collecting both lines cleanly: the leading v1 wording would have returned confident yeses from all eight customers and told the team nothing.

Block B's dropped-session question, present from v1 onward, was never revised; it produced E4 in INT-007 unchanged and fed directly into the acceptance criteria the [mobile money and wallets card](../knowledge/domains/mobile-money-wallets.md) asks every USSD payment to answer, what happens when a session times out mid-transaction. That question became AC-7, AC-8 and AC-10. The [payments acquiring card](../knowledge/domains/payments-acquiring.md)'s question, what happens when a payment is approved by the network but fulfilment fails afterward, is a different failure mode; it fed AC-9, not this question.

This guide's Block D asked an agent what stopped them from performing a customer's bill payment themselves, but no session produced an answer; what commission an agent would expect for doing so was not asked. That remaining gap is recorded as open in the research plan's RQ3 answer, owner Hira Baig, next DISCOVER pass, and it is part of why the agent-assisted bill pay the post-launch review measured (N45) came as unpredicted, even with Block D's question on record.

The agent track's Block D forces question is part of v2, matching theme T3: agents refer customers to a bill shop rather than pay on their behalf. INT-004's parked line at 26:10, not liking money she cannot see, together with the folder of paper bills the notes' section 7 records, foreshadowed the paper-slip demand the post-launch review recorded (N60, 5 of 6 pilot agent debriefs); this guide carried no proof-of-payment question in v2, a gap interview-notes.md section 7 records for INT-004 and that this revision does not close.

## Exit gate (feeds Gate 1: problem worth solving)

Sessions run with this guide are recorded in sahulat-interview-notes.md and synthesized in sahulat-user-research-plan.md section 6, toward [Gate 1](../os/STAGE-GATES.md).

- [x] Every block serves a named research question, and every research question has a block
- [x] No question asks about the idea, the future, or a price; every question asks about a specific past event or its cost
- [x] The commitment probe is present and sits last
- [x] The guide was piloted and the revision log has at least one row
- [x] Time budgets sum to the session length, including the close: customers 2 + 5 + 12 + 8 + 10 + 5 + 3 = 45 minutes; agents 1 + 3 + 8 + 5 + 6 + 5 + 2 = 30 minutes, matching N61
- [x] Signed by Hira Baig, 2026-01-28
