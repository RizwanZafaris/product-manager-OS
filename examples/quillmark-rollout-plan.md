# Rollout Plan: Quillmark Auto-Nudge payment reminders

Fills [templates/delivery/rollout-plan.md](../templates/delivery/rollout-plan.md). Everything here is invented for this standalone example: Quillmark is a fictional invoicing product sold per account to small agencies and studios, Auto-Nudge is its fictional automatic payment-reminder feature, the people are fictional, and every number, name and date is ILLUSTRATIVE, not drawn from any real company. There is no external Quillmark journey or data sheet. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**What ships:** Auto-Nudge emails an account's client when one of the account's invoices falls overdue, at 3, 10 and 21 days after the due date, and stops the moment the invoice is paid or voided. It is on by default for every eligible account once that account enters the flag, with a one-click opt-out. Reminders apply only to invoices that fall overdue after the account entered the flag, so no client is reminded about an invoice that was overdue before the account was told.

**Owner:** Dara Whitlock, Product Manager, Payments squad · **Flag owner:** Tobias Rinne, Engineering Lead, Payments squad · **Release:** 2026.10 "Auto-Nudge"
**Ramp starts:** 2026-10-12 · **GA target:** 2026-12-01 · **Thresholds agreed on:** 2026-10-07, before stage 0
**Release readiness:** the workspace's own `release-readiness.md`, Gate 5 held 2026-10-09, GO WITH CONDITIONS, before stage 0 · **Comms plan:** the workspace's own `launch-comms-plan.md`
**Last updated:** 2026-11-18 · **Status:** at stage 2 since 2026-11-09, after one halt and rollback in stage 1 (stage log, rows 3 and 4)

## 1. The flag

| Flag key | Type (release / experiment / ops / permission) | What it gates | Ramp unit (user / account / tenant / region) | Default if the flag service is unreachable | Flag owner | Created | Retirement date | Debt register row |
|---|---|---|---|---|---|---|---|---|
| `auto-nudge-release` | release | The reminder scheduler and the Auto-Nudge settings panel | account | off: no reminders are scheduled. An unsent reminder costs the account a day; a wrong one costs it a client | Tobias Rinne | 2026-09-21 | 2027-02-16 | Row 9 of the workspace's `tech-debt-register.md`, which fills [templates/execution/tech-debt-register.md](../templates/execution/tech-debt-register.md) |
| `auto-nudge-holdout` | experiment | Assigns the holdout in section 5; holdout accounts get no reminders and no settings panel | account | treated as holdout: no reminders | Oskar Lind, Product Analyst | 2026-10-05 | 2027-02-16 | Row 10 of the same register |
| `auto-nudge-kill` | ops | Stops the reminder sender queue for every account at once | global | not engaged, because the release flag's fail-closed default already stops scheduling | Femi Adeyemi, Site Reliability Engineer | 2026-09-21 | None: a permanent ops control, listed in the workspace's operational readiness review and reviewed each quarter there | None, for the reason in section 7 |

- Cohort assignment is sticky by: a hash of the account ID, salted per flag, so an account entering at stage 2 stays on at stage 3 and the holdout never overlaps a ramp stage
- Clients that cache flag values: web 5 minutes, iOS and Android 60 minutes, for the settings panel only. The sender runs server-side and reads the flags every 60 seconds, so client caches do not slow the kill switch; they only mean the mobile settings panel can show Auto-Nudge as on for up to an hour after a kill, and support is told so in their briefing

## 2. Ramp stages

Eligible accounts: 9,600 on the Studio and Agency plans after the exclusions below (ILLUSTRATIVE). The 480-account holdout is drawn from non-beta accounts on 2026-10-09, before any ramp stage, so no ramp stage can draw from it.

| Stage | Cohort (who, by rule) | Exposure (share or count of the ramp unit) | Minimum dwell | Exit criterion to advance | Advance decided by |
|---|---|---|---|---|---|
| 0. Internal | Quillmark's own billing account and 11 staff workspaces, three of them seeded with test clients whose mailboxes the team controls | 12 accounts | 7 days | Zero confirmed G1 cases across every send; defects AN-31 (reminder on a voided invoice) and AN-34 (wrong currency in the subject line) closed. G2 to G4 are not readable at this volume and are not used | Dara Whitlock |
| 1. Beta | The 400 accounts that opted into the beta from the in-app notice, list in the beta program sheet | 400 accounts, 4 percent of eligible | 14 days; after a halt, G1 must reach its minimum volume again from the resume before the stage can exit | G1 and G2 inside threshold at minimum volume; G3 inside threshold for one full week | Dara Whitlock |
| 2. Ramp | Random and sticky, beta accounts included, holdout excluded | 15 percent of eligible, 1,440 accounts | 10 days | G1 to G4 inside threshold at minimum volume | Dara Whitlock |
| 3. Ramp | As stage 2 | 50 percent of eligible, 4,800 accounts | 10 days | G1 to G4 inside threshold at minimum volume; the holdout sample-size rerun in section 5 closed | Dara Whitlock |
| 4. GA | Every eligible account, minus the holdout | 9,120 accounts, 100 percent of eligible less the 480 held out | n/a | The holdout is read on 2027-01-26 and the result goes to the post-launch review | Dara Whitlock |

- Units excluded from every stage, and why: accounts created less than 30 days ago, which have no invoice history to judge a reminder against; and the 6 accounts whose custom contract requires written notice before any new outbound email goes to their clients. Those 6 get the written notice in December and join after the holdout ends
- Pause rule: no stage advances on a Friday or on the last two business days of a month, because agencies issue most of their invoices at month end and a defect found then is found by their clients

## 3. Guardrail metrics and halt thresholds

| # | Guardrail | Definition and source (dashboard or query) | Baseline (value, measured from where, on what dates) | Halt threshold (a number) | Minimum volume before it is read | Reading window | Stages it applies to | Halt called by (and backup) |
|---|---|---|---|---|---|---|---|---|
| G1 | Reminders sent on an invoice that was already paid or voided at send time | Sender audit log joined to invoice status at send time, query `an_wrong_state_sends` on the Auto-Nudge dashboard | 0.6 per 10,000 manual reminders, measured from manual-reminder logs 2026-07-01 to 2026-09-30 | Above 3 per 10,000 sends in the stage to date | 2,000 sends | Daily, stage to date | 0 to 4 | Mei Tanaka, QA Lead (backup: payments on-call primary) |
| G2 | Spam complaints on reminder emails | Email provider feedback-loop reports, split by flag state | 0.02 percent of delivered invoice emails, measured from provider reports 2026-07-01 to 2026-09-30. Replaced at the end of stage 1 by the reminders' own rate, 0.03 percent; see the note below | Above 0.08 percent of delivered over 24 hours | 5,000 delivered | 24 hours | 1 to 4 | Femi Adeyemi (backup: Tobias Rinne) |
| G3 | Support contacts tagged auto-nudge, per 1,000 accounts on the flag, per week | Helpdesk tag report, weekly | 2.1 invoice-email contacts per 1,000 accounts per week, measured from the helpdesk tag report for Q3 2026 | Above 6 | 300 accounts on the flag for a full week | 7 days | 1 to 4 | Hana Sato, Support Lead (backup: support shift lead) |
| G4 | Accounts that switch Auto-Nudge off within 7 days of entering the flag | Settings event `auto_nudge_disabled`, product analytics, by entry date | None measured; the nearest comparable is 9 percent of accounts switching off the late-fee setting within 7 days in 2025, from the same analytics | Above 20 percent | 200 accounts past their day 7 | 7 days, by entry cohort | 2 to 4. Not stage 1: beta accounts chose the feature, so their switch-off rate says little about accounts that did not | Dara Whitlock (backup: Oskar Lind) |

- Where the readings live: the Auto-Nudge dashboard in the workspace's observability spec, every tile split by flag state, with the not-yet-on accounts shown beside the on accounts for the same hours
- SLO this rollout spends error budget against: none. The sender is asynchronous and has no user-facing latency; the email provider's delivery rate is watched on the same dashboard but is not this rollout's guardrail, because a provider outage is not caused by the flag
- G2 baseline note: the baseline agreed on 2026-10-07 was invoice emails, not reminders, which clients were expected to report as spam more often. Gate 5 made replacing it a condition before stage 2, owned by Femi Adeyemi. Closed 2026-11-06: stage 1's reminders measured 0.03 percent over 6,560 delivered, and the 0.08 percent threshold was kept, with a stage-log row recording that it was reviewed and not moved

## 4. Kill switch and rollback trigger

Section 4 of the workspace's `release-readiness.md` points here rather than restating this trigger.

- Kill switch: `auto-nudge-kill` · turns off: the reminder sender queue for every account · leaves running: invoice sending, manual reminders, payment links, and the settings panel
- Tested on: staging, 2026-10-08, by Femi Adeyemi · decision to effect: 3 minutes, being the 60-second flag poll plus the in-flight batch of up to 500 messages finishing. Run again in production on 2026-10-14 against the stage 0 accounts: 2 minutes
- Rollback trigger, any one of these, agreed in advance: G1 above 3 per 10,000 sends at minimum volume, confirmed by a second reader · G2 above 0.08 percent for two consecutive 24-hour windows · any warning from the email provider about the shared sending domain's reputation · any guardrail breaching its halt threshold for two consecutive reading windows
- May pull the switch without asking anyone: the payments on-call rota, primary and secondary; Femi Adeyemi; Tobias Rinne · Tells, within 15 minutes: Dara Whitlock, Hana Sato, and Lucia Ferreira, the comms owner
- What a flag-off does not undo, and what happens to each: reminders already handed to the email provider, including the in-flight batch, are sent and cannot be recalled, so support holds an approved "please disregard" correction email it can send per account; reminder history on each invoice stays, because those reminders were sent; account settings are kept, so turning Auto-Nudge back on resumes each schedule, and a reminder whose day passed while it was off is skipped, not sent late in a burst

## 5. Holdout

- Holdout: 5 percent of eligible accounts, 480 accounts, assigned by the sticky hash on 2026-10-09, excluding beta accounts and the 6 contract-notice accounts
- Measures: share of invoices paid within 15 days of their due date, the PRD's success metric, as defined in the workspace's metrics dictionary. Baseline 61 percent across eligible accounts, measured from invoice records for Q3 2026
- Sample size and duration: 480 accounts for 8 weeks after GA, about 4,800 invoices falling due, sized in the workspace's experiment brief section 4 to detect a 3 percentage point change. [OPEN: that calculation treats each invoice as independent, but invoices from one account move together, so clustering by account will widen the interval. Oskar Lind reruns it with account-level clustering by 2026-11-20. If the holdout must grow, it grows before stage 3, drawn from accounts not yet on the flag, because after stage 3 there are not enough unexposed accounts left to draw from]
- Ends on: 2027-01-26, then the holdout accounts receive Auto-Nudge and `auto-nudge-holdout` is retired
- Exception rule: only Ana Pellegrini, Head of Customer Success, may release an account from the holdout; every released account leaves the analysis; after 10 releases the holdout result is declared unreadable in the post-launch review instead of being reported
- Result goes to: the workspace's post-launch review, which fills [templates/operate/post-launch-review.md](../templates/operate/post-launch-review.md)

## 6. Who hears at each stage

- Stage 0 and 1: support briefed on 2026-10-09 with the known-issues table and the mobile-cache caveat; each beta account's admin told by email and in-app notice what changes, which invoices it applies to, and how to switch it off
- Each ramp stage: account admins entering the flag get the same notice on the day they enter; support's daily note carries the current exposure, so a ticket can be matched to flag state from the account ID
- GA: the comms plan's section 3 sequence, starting T-0 on 2026-12-01, with the help-centre article and changelog entry
- On a halt or rollback: the comms plan's pre-written holding statement, approved by Dara Whitlock and sent by Lucia Ferreira

## 7. Flag retirement

- Retirement date: 2027-02-16, three weeks after the holdout ends, which is later than GA
- Retirement owner: Tobias Rinne · Register rows: 9 and 10 of the workspace's tech-debt register, interest 2 team-days per quarter while both flags live, from the doubled test paths on the scheduler
- Done when: both flags deleted from the flag service · the off-path scheduler code deleted, change ID to be recorded on the day · the off-path tests deleted · the flag-state split removed from the Auto-Nudge dashboard
- If the date passes with either flag still in code: the row moves to section 5 of the register, accepted debt, with Tobias Rinne's signature and a new date, or the flag comes out that week
- The kill switch has no register row because it is not debt: it is a permanent control with a named owner, and it is reviewed each quarter in the operational readiness review rather than retired

## 8. Stage log

| Date and time | Moved from, to | Guardrail readings at the move (G1 to G4) | Minimum volume met? | Decided by | Notes |
|---|---|---|---|---|---|
| 2026-10-12 09:30 | none, to stage 0 | None yet | n/a | Dara Whitlock | First sends scheduled for the seeded test clients |
| 2026-10-14 16:00 | none, kill-switch drill at stage 0 | G1: 0 confirmed in 210 sends | No, and not needed for a drill | Femi Adeyemi | `auto-nudge-kill` pulled and released in production; sending stopped 2 minutes after the decision |
| 2026-10-19 10:00 | 0, to 1 | G1: 0 confirmed in 620 sends. G2 to G4 not used at stage 0 | G1 no (620 of 2,000); the stage 0 exit criterion is zero cases across every send, which was met | Dara Whitlock | AN-31 and AN-34 closed 2026-10-16 |
| 2026-10-26 11:20 | 1, halted at 1, then rolled back | G1: 3 confirmed in 2,600 sends, 11.5 per 10,000 | Yes | Mei Tanaka called the halt; Tobias Rinne, as second reader, confirmed the rollback trigger; on-call pulled `auto-nudge-kill` at 11:34 | Card payments through the payment link were marked paid by a webhook arriving up to 10 minutes later, and the sender checked status only when the batch was built. Support sent the correction email to the 3 affected accounts the same day |
| 2026-10-28 15:00 | rolled back, resumed at 1 | G1 count restarted from this row | n/a | Tobias Rinne and Mei Tanaka | Fix AN-52: the sender rechecks status immediately before each send and skips any invoice with a payment pending. Kill switch released; reminders whose day fell in the 51 hours off were skipped, as section 4 says |
| 2026-11-06 17:00 | none, threshold review | G2: 0.03 percent of 6,560 delivered over stage 1 | Yes | Femi Adeyemi | Reminder baseline replaces the invoice-email baseline; the 0.08 percent threshold is kept, not moved |
| 2026-11-09 10:00 | 1, to 2 | G1: 0 confirmed in 4,100 sends since the fix. G2: 0.03 percent, 24 hours inside threshold. G3: 5.0 per 1,000 accounts, 2 contacts from 400 accounts, for the week to 2026-11-06. G4 not used at stage 1 | Yes for G1, G2, G3 | Dara Whitlock | Stage 1 ran 21 days in all; earliest stage 3 move is 2026-11-19 |

## 9. How a rollout fails while looking controlled

The template's failure table, with the third column saying what this plan does about each.

| Failure | The tell | What this plan does |
|---|---|---|
| Thresholds set after the first reading | The "thresholds agreed on" date is later than the stage 0 start | Agreed 2026-10-07, stage 0 began 2026-10-12. The only later threshold event, the G2 review, has its own log row and kept the number |
| Ramp by calendar | Stage log moves every Monday, with "green" and no numbers | Every advance row carries values; stage 1 ran 21 days, not 14, because of the halt and rollback |
| Ramp unit wrong for the product | A per-user percentage on a product sold per account | Ramp unit is the account; percentages count accounts |
| Guardrail read at noise volume | A stage cleared or halted on a few dozen events | The 2026-10-19 row says G1 was below minimum volume and names the exit criterion used instead |
| Everyone can halt, so nobody does | The halt column says "on-call" | One name and one backup per guardrail; the halt on 2026-10-26 was called by the named reader, and the rollback needed a second reader, who confirmed it in 14 minutes |
| Kill switch that only works on the web | Tested in a browser while mobile caches for an hour | The switch acts in the server-side sender; the mobile settings-panel lag is in support's briefing |
| Holdout dissolved one favour at a time | Units released on request until the holdout is too small | One named releaser and a cap of 10, after which the result is declared unreadable |
| The flag that never retires | A release flag past its date, with no register row | Rows 9 and 10 opened with the flags; retirement date 2027-02-16 |

## Exit gate

This plan is ready for Gate 5 when:

- [x] Every flag row names a type, a ramp unit, a default for flag-service failure, one flag owner, a retirement date, and a debt-register row number, or, for a permanent ops flag, the review where it is listed instead (the kill switch is listed in the operational readiness review; section 7 says why it is not debt)
- [x] Section 3 is dated before stage 0, and every guardrail has a sourced baseline, a numeric halt threshold, a minimum volume, and one named halt caller with a backup (G4's baseline is a stated comparable, not a measurement of this feature)
- [x] Every ramp stage has a cohort rule, an exposure, a minimum dwell, an exit criterion, and the name of whoever advances it
- [x] The kill switch was executed in a named environment on a dated day, with the decision-to-effect time recorded, including client caches (staging 2026-10-08, 3 minutes; production 2026-10-14, 2 minutes)
- [x] The "does not undo" line is answered for every side effect the feature has
- [x] Section 5 has a holdout with size, duration, end date and exception rule, or a written reason there is none (the sample-size rerun is open, with an owner and a date before stage 3)
- [x] Section 4 of release-readiness.md points at section 4 of this file instead of restating a trigger
- [x] The stage log has a row for every move made so far, each with numbers

Signed: Dara Whitlock, Product Manager, Payments squad, 2026-10-09
