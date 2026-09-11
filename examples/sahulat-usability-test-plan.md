# Usability Test Plan: Sahulat Bill Pay, menu script v0.3

Fills [templates/discovery/usability-test-plan.md](../templates/discovery/usability-test-plan.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the Sahulat journey and its coverage sheet extension, not from any real wallet, market or regulator. See the [examples index](README.md).

This is a DESIGN-stage rerun of a DISCOVER template: the round tests a prototype, not a problem, and its findings feed the [Gate 3](../os/STAGE-GATES.md) packet rather than Gate 1. See [the Sahulat journey](sahulat-journey.md) for the fourteen-artifact story this round sits inside, and [the coverage sheet](sahulat-coverage-sheet.md), row `sahulat-usability-test-plan.md` in its artifact map, for where this file's reported numbers (CN10 to CN12) and identifiers (TK-1 to TK-5, UF-1 to UF-4) are sourced.

**Owner:** Hira Baig · **Date:** 2026-04-13 · **Status:** Reported, 2026-04-14

## 1. What is being tested

| Field | Value |
|---|---|
| Artifact | Menu script v0.3, the paper USSD card deck for Sahulat bill pay; not a build, since BUILD had not opened |
| Fidelity and version | Paper. Menu script v0.3, one card per USSD screen; the facilitator swaps cards to simulate navigation and removes one mid-task to simulate a dropped session |
| Design questions this round must answer | Does a customer read the bill reference correctly off the paper bill and key it without confusing it with the consumer number printed beside it. Does an agent complete a same-visit cash-in-and-pay without a facilitator prompt. Does the dropped-session design (ADR-2's two-phase state machine, shown here as a removed card) lead a participant to redial blind rather than wait for a status message |
| Out of scope this round | Coded latency, real BillBridge posting, the smartphone app flow (SAHULAT-S10), and the Mehran Water bill, which was still in scope for Rel-1 at this date and had not yet failed its reference-validation test (the failure, N58, and the drop decision, D5, land on 2026-05-19 and 2026-05-21, after this round) |
| Environment | In person, a room at the Lahore agent-operations office; facilitator Hira Baig runs the cards, Usman Javed times and takes notes; participants' own phones for the SMS confirmation step, everything else paper |

## 2. Participants

| Segment | Count | Screener criteria (behavior in the last n days) | Source | Codes |
|---|---|---|---|---|
| Customer | 5 | Paid a household electricity or gas bill in person in the last 60 days; owns or regularly uses a Sahulat wallet; none were in INT-001 to INT-008, so this round is a fresh sample rather than the discovery panel re-asked | Recruited through the agent network, screened by Tariq Sohail's team | UC-01 to UC-05 |
| Agent | 5 | Active Sahulat agent, at least one cash-in transaction in the last 7 days | Recruited by Tariq Sohail from the Lahore pilot pool | UA-01 to UA-05 |

Session logistics follow N61: customers 45 minutes, agents 30 minutes at the counter, incentive PKR 500 mobile airtime, the same terms the pass-1 research plan used.

## 3. Tasks

| Task id | Scenario read to the participant | Starting point | Success is | Max time | Data to capture |
|---|---|---|---|---|---|
| TK-1 | "Here is your Ravi Power electricity bill. Use this card deck to look up what is owed and when it is due." | Home-screen card, logged in | The reference number from the bill, not the consumer number printed beside it, is the one entered on the lookup card, and the amount and due date card is reached | 3 minutes (target under this per CN11) | completion, errors (reference confused with consumer number), assists, time, path |
| TK-2 | "You just cashed in. Pay this bill from what is now in your wallet." | Amount and due date card shown, a staged balance card already in hand | The payment-confirmation card is reached and the participant states, unprompted, what proof they now hold | No stated max; time recorded | completion, errors, assists, time, path |
| TK-3 (agents) | "A customer wants to cash in and pay this same bill in one visit. Walk me through it as you would at your counter." | Agent home card, customer's bill reference on hand | The agent reaches the same-visit cash-in-and-pay confirmation card without asking the facilitator what to do next | No stated max; time recorded | completion, errors, assists, time, path |
| TK-4 | "Partway through paying, your screen goes blank." (facilitator removes the confirmation card) "What do you do now?" | Mid-payment card, then the removed card | The participant states what they would do next; a stated intent to redial immediately, or to wait for an SMS, both count as a completed task, since the design question is which one they choose, not whether one is wrong | No stated max; time recorded | completion, stated intent (redial vs wait), assists |
| TK-5 | "Your neighbour asks if you actually paid. Show me what you would show them." | After TK-2's payment-confirmation card | The participant identifies the SMS reference, or names it as what they would find, as the proof | No stated max; time recorded | completion, assists |

## 4. Success criteria

Targets are CN11, agreed by Hira Baig and Zainab Qureshi on 2026-04-10, three days before the round.

| Measure | Definition | Target agreed before the round | Why this target |
|---|---|---|---|
| Task completion, unassisted | share of participants reaching the success state without help, per task per segment | at least 4 of 5 | A same-visit cash-in-and-pay that needs a facilitator's help at the counter does not survive a real queue; 4 of 5 leaves room for one genuinely hard case without masking a design fault |
| Errors per task | wrong paths, recovered or not | at most 1 assist per task | Matches the completion bar; more than one assisted recovery on the same task across five participants is a pattern, not a fluke |
| Assists | facilitator interventions needed | at most 1 per task | As above |
| Time on task | median, against the max in section 3 | TK-1 under 3 minutes | TK-1 is the only task with a stated max, since it is the one Falak Telecom's gateway also times (N66, 180-second session ceiling); the others were left open deliberately, to see where time actually went rather than test against a guessed number |
| Satisfaction | post-task rating, 1 to 5, "how easy was that", asked after every task | median at least 4 | Matches the bar the pass-1 research plan's forces block implied for a flow replacing a trip and a fee |

## 5. Script

- Intro (2 minutes): who we are; we are testing the paper cards, not you; think aloud; there are no wrong answers; you can stop at any time; consent to record confirmed (notes only, no audio, since the cards are the artifact)
- Think-aloud reminder: "keep telling me what you expect to happen"
- Facilitator may: repeat the scenario, ask "what would you do next", ask "what did you expect", swap the next card once the participant states where they are pointing or reaching
- Facilitator may not: explain what a card means, answer "is this right", name which card comes next, react to success or failure
- After each task: "on a scale of 1 to 5, how easy was that", then "what was hardest about that"
- Debrief (5 minutes): what would you change first; anything you avoided; thanks and incentive

## 6. Severity scale

Unchanged from the template; the same scale the pass-1 research and interview artifacts use, so a severity number means the same thing across every Sahulat round.

| Level | Definition | Example | Action |
|---|---|---|---|
| 4, blocker | participant cannot complete the task; no recovery | a card path with no route back to the lookup screen | fix before any release; row in the risk register |
| 3, major | completes with an assist or a serious detour; likely to cause errors in real use | the reference number confused with the consumer number, so a customer looks up the wrong bill without noticing | fix before release |
| 2, minor | hesitation or a recoverable wrong turn; task still completes | pausing before finding the amount-due card, then finding it | fix in the next iteration |
| 1, cosmetic | noticed, no effect on completion | wording on a card felt formal | backlog |

## 7. Findings

Findings are CN12's results read against section 6's scale; see the coverage sheet's identifier table for UF-1 to UF-4 in full. Neither the findings below nor the CN12 results show an agent keying a customer's payment: at this round the flow was customer-initiated throughout, and the post-launch review (2026-08-21) is where an agent keying the payment on the customer's behalf first appears, recorded there as unpredicted rather than designed for. No finding shows a paper-slip request either; the post-launch review records it as unpredicted (N60).

| Id | Task | Participants affected (codes) | What happened | Severity | Evidence (clip time or quote) | Recommended change | Owner |
|---|---|---|---|---|---|---|---|
| UF-1 | TK-1 | UC-02, UC-04 | Two of five customers entered the consumer number printed beside the reference on the bill, not the reference itself, and the lookup card returned no match; neither reached the amount-and-due-date card until the facilitator repeated the scenario and pointed them back to the bill | 3, major | Facilitator note, session UC-02, 09:40; session UC-04, 10:55: both participants pointed to the same printed line and needed the scenario repeated before trying the reference number instead | Restyle the lookup card and the paper-bill callout so the reference is visually distinct from the consumer number; carries into the coded lookup screen, not just the card | Zainab Qureshi |
| UF-2 | TK-4 | UC-01, UC-02, UC-03, UC-05 | Four of five customers said they would wait briefly for a status SMS and, when none arrived, blind-redial; one said they would wait for an SMS, with no redial stated | 3, major | Facilitator note, session UC-01, 11:20: "I'd give it a few minutes for the message, then call the number again, see what happens." Session UC-05, 14:05, same stated intent | Blind redial after a short wait for a status message that does not come; this finding is the case AC-7 and AC-8 answer | Zainab Qureshi |
| UF-3 | TK-3 | UA-01, UA-03 | Two of five agents paused mid-flow, unsure whether the customer's cash-in credit was already spendable or still pending, before continuing on their own | 2, minor | Facilitator note, session UA-01, 15:30: "Is that money in already, or do I wait?" | Add an explicit "credit available" state to the same-visit card before the pay step; this is the case AC-5 answers | Zainab Qureshi |

UF-4 is retired: no round-2 finding on a paper slip. The paper-slip expectation first appears after launch, recorded as unpredicted in the post-launch review (N60); see [the coverage sheet](sahulat-coverage-sheet.md).

## 8. Results against criteria

| Measure | Target | Result | Met |
|---|---|---|---|
| Task completion, unassisted, TK-1 (customer) | at least 4 of 5 | 3 of 5 | no |
| Task completion, unassisted, TK-1 (agent) | at least 4 of 5 | 5 of 5 | yes |
| Task completion, unassisted, TK-2 (pay from staged balance, customer) | at least 4 of 5 | 4 of 5 | yes |
| Task completion, unassisted, TK-3 (same-visit cash-in and pay, agent) | at least 4 of 5 | 4 of 5 | yes |
| Task completion, TK-4 (stated intent, customer) | at least 4 of 5 stating wait-then-redial | 4 of 5 | yes against the target, but UF-2 flags the same behavior below: waiting then blind-redialing still risks a duplicate, the gap AC-7 and AC-8 exist to close |
| Task completion, unassisted, TK-5 (find the proof, customer) | at least 4 of 5 | 5 of 5 | yes |
| Time on task, TK-1 median | under 3 minutes | 2.5 minutes | yes |
| Satisfaction, median across tasks | at least 4 | 4 | yes |

**Decision:** Fix findings rated severity 3 and above (UF-1, UF-2) before BUILD opens, and retest the fixed lookup card and the dropped-session flow in BUILD with Mariam Gill as verifier. Findings rated severity 2 (UF-3) go to the backlog for the next iteration rather than blocking Gate 3. No finding reached severity 4, so no new risk-register row was opened; UF-2 is treated as confirming R2 and ADR-2 rather than raising a new risk. Decided by Hira Baig, 2026-04-14.

## Exit gate (feeds Gate 1: problem worth solving)

This round reruns the template inside DESIGN, so its findings feed the [Gate 3](../os/STAGE-GATES.md) packet, not Gate 1; the template's own exit-gate line is answered against that reuse below, per the header note in [the template](../templates/discovery/usability-test-plan.md). In DESIGN and BUILD, blockers become rows in [risk-register.md](../templates/execution/risk-register.md) and unmet criteria block [acceptance-criteria.md](../templates/definition/acceptance-criteria.md) at [Gate 4](../os/STAGE-GATES.md).

- [x] Every task is a scenario in the participant's words with an observable success state. TK-1 to TK-5 in section 3 each name the card or the stated intent that counts as success
- [x] Every success measure has a target agreed before the first session. Section 4's five measures carry the CN11 targets Hira Baig and Zainab Qureshi agreed on 2026-04-10, three days ahead of the round
- [x] The script forbids explaining the interface, and the facilitator followed it. Section 5's "may not" line held; every assist logged in section 7 is a card swap or a repeated scenario, never an explanation of what a card meant
- [x] Every finding names affected participant codes, a severity against the scale, and checkable evidence. UF-1 to UF-3 in section 7 each carry codes, a severity, and a facilitator-note timestamp or quote; UF-4 is retired
- [x] Results are recorded against every target, and the decision is signed by name. Section 8 carries every target from section 4 against its result; section 8's decision line is signed
- [x] Signed by Hira Baig, 2026-04-14

This round's findings, and the fix-and-retest decision above, are the DESIGN-stage input the [Gate 3](../os/STAGE-GATES.md) packet on 2026-04-15 carries alongside the premortem risks R1 to R6 and ADR-1 to ADR-3; Gate 3 was ACCEPTED that date per the Sahulat journey timeline. The retest itself, run in BUILD with Mariam Gill against the fixed lookup card, is not a file in this example set: Open, the coverage sheet's DISCOVER-pass-2 files pick the thread back up on the agent-keyed flow, but no BUILD-stage retest artifact exists in this example.
