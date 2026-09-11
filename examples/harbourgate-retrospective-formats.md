# Harbourgate Retrospective Formats: after the last drain

Fills [frameworks/execution/retrospective-formats.md](../frameworks/execution/retrospective-formats.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen so that this artifact reconciles with the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Noor Haddad, QA Lead · **Date:** 2026-09-17 · **Status:** Retrospective complete; actions committed before 2026-10-22 · **Facilitator:** Noor Haddad · **Product:** Harbourgate checkout

## What it is for

This retrospective turns the R9 drain into changes to how the payments squad works next. R9 closed on 2026-09-15 after the last drain, so the squad reviewed the delivery period rather than reopening the migration decision.

The decision improved by this retrospective is what the squad will verify, plan and read differently before the next retrospective on 2026-10-22.

The session used the 4Ls format, in this repository's own words.

## Run it when

- The R9 drain has closed, with R9 closed on 2026-09-15 after the last drain.
- The previous action table can be reviewed first.
- The squad can separate facts from feelings and actions.
- A facilitator who is not the team's manager is available. Noor Haddad facilitated.
- The next retrospective is scheduled for 2026-10-22.

The last retrospective's actions were complete, so this retrospective was not skipped.

## Inputs you need first

- The previous action table, A1 to A6, with a status per row.
- The cycle facts: the last drain closed R9, and the squad has a remaining on-call share of 0.4 FTE in N54.
- The open risk R11, which remains open with a weekly kiosk-use report per shop.
- The payments squad composition: 5 engineers, 1 QA lead and 1 PM, from N63.
- The next retrospective date, 2026-10-22, from HC44.
- A facilitator and speaking order: Noor Haddad facilitated, and Tomasz Wierzbicki spoke and voted last.

### Previous action table

| ID | Previous action | Owner | Due | Verification | Status at this retrospective |
|---|---|---|---|---|---|
| A1 | Dual-path reconciliation with a classified straddle set | Bea Lindqvist | 2026-07-03 | Rehearsal 2 passed AC-8 | Done |
| A2 | Separate SFTP drop per environment, with pre-production credentials unable to read the production drop | Hamid Qureshi | 2026-06-26 | Failed read attempt on 2026-06-26 | Done |
| A3 | Settlement-file-absent page at 07:45 | Bea Lindqvist | 2026-07-09 | N72 and the live page of 2026-07-10 | Done |
| A4 | Production ingestion job exits non-zero on “no file” | Bea Lindqvist | 2026-06-26 | Verified in CI | Done |
| A5 | Abort checklist gains “disable every pre-production schedule” | Tomasz Wierzbicki | 2026-06-19 | Verified at the rehearsal 2 abort drill | Done |
| A6 | Dependency at “requested” for more than 4 weeks is escalated automatically at the weekly review | Ife Adeyemi | 2026-06-19 | Verified by the register's review log | Done |

Completion rate arithmetic:

`actions done / actions committed = 6 / 6 = 100%`

The previous action table was therefore complete before this retrospective began.

## The worksheet

### Step 1: choose the format

| Format | The question it asks | Fits when | Does not fit when | Time |
|---|---|---|---|---|
| Start, stop, continue | Which habits change? | A stable team making incremental improvements | A big event needs processing; it also yields the same list every cycle on autopilot | 45 minutes |
| **4Ls, selected** | **What did we take from this?** | **After a launch or a hard cycle; a new team; learning matters more than habits this time** | **A specific failure needs causes: use five whys and fishbone** | **60 minutes** |
| Sailboat, wind, anchors, rocks, island | What pushes us, what drags, what could sink us, where are we going? | Goal ambiguity or unspoken risk; cross-team work | A team of three; a team that dislikes metaphor | 60 minutes |
| Timeline | What actually happened, and when? | Memories disagree; a long cycle; after an incident or a missed gate | A short cycle everyone remembers the same way | 90 minutes |

**Choice:** 4Ls. The postmortem had already reviewed HG-INC-14 and A1 to A6. This session needed to capture what the squad carried forward from the drain, not repeat the incident analysis.

### 4Ls capture

| 4L | Squad observation | Resulting implication |
|---|---|---|
| Liked | R9 closed on 2026-09-15 after the last drain, and all 6 of 6 postmortem actions were done | Keep explicit verification and named owners |
| Learned | A rehearsal verify step must count settlement and refund tails still in flight, rather than treating the provider shift as the end of the work | Add the count to the rehearsal method |
| Lacked | The Q4 capacity plan did not yet show the release of N54's 0.4 FTE on-call share | Book the release explicitly in the Q4 capacity plan |
| Longed for | A named squad reader for the weekly kiosk-use report behind R11 | Assign a reader so the report has an accountable audience |

### Step 2: facilitation rules

| Rule | How it was applied |
|---|---|
| Read Kerth's prime directive aloud, paraphrased: everyone did the best job they could with what they knew | Noor Haddad opened with the conditions-based, no-blame framing |
| Review the last action table first, row by row | A1 to A6 were reviewed first; 6 of 6 were done |
| Silent writing before any discussion | Each squad member wrote 4Ls notes before discussion |
| Facts, then feelings, then actions, in that order | The group reviewed R9 and A1 to A6, discussed the 4Ls observations, then committed three actions |
| Three dot votes per person; the top three items get actions, the rest are logged | HC44 records 21 dot votes. The top three items received 7, 5 and 4 votes. The remaining votes were calculated as `21 - (7 + 5 + 4) = 5` and were logged rather than turned into additional actions |
| The manager speaks last and votes last | Tomasz Wierzbicki spoke and voted last |
| No names in problem statements; roles and conditions only | The 4Ls observations name conditions, reports and capacity; the action table names one owner per action |
| Timebox held by the facilitator, not the manager | Noor Haddad held the 60-minute 4Ls session |

### Dot-vote result

| Item selected for action | Votes | Decision |
|---|---:|---|
| Add a rehearsal verify step that counts settlement and refund tails still in flight | 7 | Action 1 |
| Book N54's 0.4 FTE release into the Q4 capacity plan | 5 | Action 2 |
| Name a squad reader for the weekly kiosk-use report behind R11 | 4 | Action 3 |
| Other observations | `21 - (7 + 5 + 4) = 5` | Logged, no additional action |

### Step 3: the actions table

| # | Action, a change to how we work, verifiable | Owner, one name | Due, before the next retro | How we will know it happened | Status at next retro |
|---|---|---|---|---|---|
| 1 | Add a rehearsal verify step that counts settlement and refund tails still in flight | Tomasz Wierzbicki | Before 2026-10-22 | The rehearsal checklist contains the verify step, and a reviewer can see the settlement-tail and refund-tail counts recorded in the rehearsal evidence | To verify |
| 2 | Book the release of N54's 0.4 FTE on-call share into the Q4 capacity plan | Ife Adeyemi | 2026-10-16 | The Q4 capacity plan records the 0.4 FTE release as a dated capacity change, with the resulting plan reviewed by the squad | To verify |
| 3 | Name a squad reader for the weekly kiosk-use report behind R11 | Bea Lindqvist | Before 2026-10-22 | The weekly kiosk-use report names Bea Lindqvist or another named squad member as reader, and the report has a recorded review before the next retrospective | To verify |

The new action count is three, which is within the maximum of three.

The previous completion rate was:

`6 done / 6 committed = 100%`

The new actions have not yet reached their due point on 2026-09-17, so no completion rate is claimed for them.

## Reading the result

R9 closed after the last drain, and the previous action table was complete. The retrospective therefore moved from incident correction to operating discipline.

The strongest item was the rehearsal verify step, with 7 of 21 dot votes. This keeps the learning from R9 visible in future rehearsal evidence rather than relying on the assumption that a provider shift ends when traffic reaches 100%.

The second item was capacity visibility. N54 records 0.4 FTE consumed by the legacy path, and the action makes its release explicit in the Q4 capacity plan rather than leaving the capacity change implicit.

The third item keeps R11 visible. R11 remains open, and the weekly kiosk-use report per shop needs a named squad reader. The report is therefore treated as an operating input, not as an unowned output.

The arithmetic for the vote record is:

`7 + 5 + 4 = 16 top-three votes`

`21 - 16 = 5 other votes`

Five votes went to other observations and were logged; no additional action was committed because the worksheet caps new actions at three.

## ILLUSTRATIVE example

This Harbourgate retrospective is an ILLUSTRATIVE example of a 4Ls session after the last drain. The previous actions A1 to A6 were reviewed first and all 6 were done. The session then used 21 dot votes to select three actions, with the top three receiving 7, 5 and 4 votes.

The actions are deliberately verifiable:

- The rehearsal action is checked in the rehearsal checklist and evidence.
- The capacity action is checked in the Q4 capacity plan.
- The R11 action is checked in the weekly kiosk-use report.

## The trap

The trap here would be celebrating R9's closure and treating the drain as finished without checking what remains in flight. The rehearsal action prevents that by requiring settlement and refund tails to be counted explicitly.

A second trap would be treating N54's 0.4 FTE as a permanent background load. The capacity action makes the planned release visible in the Q4 capacity plan.

A third trap would be producing the R11 report without giving the squad a reader. The named-reader action makes the report's use verifiable.

The retrospective avoids the trap by reviewing A1 to A6 first, showing the arithmetic aloud, limiting the new list to three actions and assigning one named owner to each.

## Feeds

- [harbourgate-journey.md](harbourgate-journey.md): R9, R11, N54, N63 and A1 to A6.
- [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md): HC44, including the 4Ls format, facilitator, speaking order, vote count and next retrospective date.
- The next retrospective on 2026-10-22: verify all three action done-tests.
- The Q4 capacity plan: record the release of N54's 0.4 FTE share.
- The weekly kiosk-use report behind R11: record the named squad reader.

**Exit-gate walk:** Noor Haddad, facilitator, confirms that A1 to A6 were reviewed first, the completion arithmetic was `6 / 6 = 100%`, the three new actions have one named owner each, and the actions are due before the 2026-10-22 retrospective. **Signed:** Noor Haddad · **Date:** 2026-09-17
