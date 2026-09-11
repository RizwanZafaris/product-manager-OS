# Harbourgate Five Whys and Fishbone: HG-INC-14

Fills [frameworks/execution/five-whys-fishbone.md](../frameworks/execution/five-whys-fishbone.md). Everything here is invented: Harbourgate, its people and systems are fictional, and every number, date, amount, rate and identifier is ILLUSTRATIVE, taken from the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Noor Haddad, QA Lead and facilitator · **Date:** 2026-06-17 · **Incident:** HG-INC-14 · **Stage:** DELIVER event review, feeding OPERATE

## What it is for

This worksheet separates the observed effect from causes that can be changed. It follows the HG-INC-14 chain from the enabled pre-production ingestion job, through the shared SFTP drop and the missing Marlowe sandbox settlement files, to the unclassified straddle and the finding that was below the register threshold and sent to the unscheduled backlog.

The review was conducted out loud on 2026-06-17. No person is named in a cause cell.

The effect was:

- The Marlowe settlement file was deleted at 07:00 on 2026-06-15.
- Finance's daily close completed at 12:40 instead of 07:00, a delay of 5 h 40 min.
- Arithmetic: 12:40 minus 07:00 = 5 h 40 min.
- The late close covered 5,190 settlement lines and £332,000.

Evidence: N41 and N42 in [harbourgate-journey.md](harbourgate-journey.md).

## Run it when

This worksheet was run because:

- HG-INC-14 had several true contributing conditions, not one disputed cause.
- The original finding F2 was scored 4, below the register threshold of 6, and routed to backlog item HG-812 rather than to the risk register.
- The team needed to distinguish changeable system conditions from the rehearsal crew's load and the Monday settlement timing.
- The output had to feed the incident postmortem and corrective actions A1 to A6.

The review rule was agreed before starting: no names in any cause cell.

## Inputs you need first

| Input | Used here | Evidence |
|---|---|---|
| Effect stated as an observation | File deleted at 07:00; close 5 h 40 min late | N41, N42 |
| Timeline from logs and chat | Rehearsal 1 was aborted at 9 h 10 min on 2026-06-13; the incident occurred on 2026-06-15 | N37, N41 |
| People who were there and an independent facilitator | Out-loud review facilitated by Noor Haddad on 2026-06-17 | HC38 |
| Relevant dependency status | DEP-2 had no committed delivery date and was closed on 2026-07-03 after ADR-0004 removed the need | DEP-2 |
| Finding and register rule | F2 scored 4; the register threshold is 6; F2 was routed to HG-812 and became R14 after the incident | F2, R14, N68 |
| Corrective actions | A1 to A6, each tied to a cause and verification method | A1 to A6 |

## The worksheet

### Five whys

| Level | Why did it happen? (one cause, stated as a checkable fact) | Evidence (log, document, quote) | Can we change this? | If yes, the change |
|---|---|---|---|---|
| Effect | The Marlowe settlement file was deleted at 07:00 on 2026-06-15, and finance close finished 5 h 40 min late at 12:40. Arithmetic: 12:40 minus 07:00 = 5 h 40 min. | N41 and N42; 5,190 settlement lines and £332,000 were reconciled late | Yes | Prevent non-production jobs from reading the production drop, and detect an absent file by 07:45 |
| Why 1 | An enabled pre-production ingestion job read the production settlement file and deleted it after a successful read. | HG-INC-14 incident record; F2; rehearsal 1 used pre-production on production-shaped data | Yes | A4: make production ingestion exit non-zero on “no file”, and A5: disable every pre-production schedule during an abort |
| Why 2 | Pre-production and production shared the same SFTP drop, so the pre-production job had access to a live settlement file. | F2; R14; I-6; A2 | Yes | A2: separate the SFTP drop per environment and prevent pre-production credentials from reading the production drop |
| Why 3 | The rehearsal needed a settlement file, but DEP-2, Marlowe sandbox settlement files, had never been committed. Two true answers were recorded: the missing sandbox left production-shaped files as the available fixture, and the shared drop allowed that fixture to be consumed by pre-production. | DEP-2: “never committed”; N37; F2; HC38 | Yes | A2 removes the shared access path. ADR-0004 and A1 provide dual-path reconciliation fixtures and a classified straddle set |
| Why 4 | The settlement process had no classification for lines authorised on one path and settled after a provider shift, so the rehearsal could not determine which path should reconcile the lines. | N36; R9; ADR-0004; A1; N37 records 1,529 of 1,742 Marlowe lines unmatched | Yes | A1: reconcile both paths from one ledger, matching on either reference, with a classified straddle set |
| Why 5 | F2 was scored 4, below the register threshold of 6, and was sent to the unscheduled backlog HG-812. The process had no trigger to escalate a below-threshold finding or a dependency that remained requested for more than 4 weeks. | F2; N68; R14; DEP-2; A6 | Yes | A6: automatically escalate a dependency at “requested” for more than 4 weeks at the weekly review, and route the shared-drop control into the corrective-action path |

The chain contains two true answers at Why 3. They are both retained rather than selecting the more convenient branch.

### Fishbone

| Branch | Contributing cause (a condition that had to be true) | Evidence | Changeable? | Weight (1 to 3) |
|---|---|---|---|---|
| Process | The abort checklist did not require disabling every pre-production schedule. | N37; A5 | Yes | 3 |
| Process | DEP-2 remained requested without automatic escalation after more than 4 weeks. | DEP-2; A6; HC38 | Yes | 2 |
| People | The rehearsal crew aborted after 9 h 10 min against a planned 6 h. | N37; HC38 | No | 1 |
| Tooling | Pre-production and production used a shared SFTP drop. | F2; R14; I-6; A2 | Yes | 3 |
| Data | No separate data cause was identified. The settlement file was valid and available; the failure was in access, handling and classification. | N37; N42 | Not separately scored | Not scored |
| Design | The ingestion job deleted the file on read. | HG-INC-14; A4 | Yes | 3 |
| Design | The reconciliation design had no classified straddle set for authorisations and settlements crossing the provider shift. | N36; R9; ADR-0004; A1 | Yes | 2 |
| Environment | Monday's Marlowe file carried weekend settlements, increasing the consequence of a missed or consumed file. | N33; HC38 | No | 1 |
| Measurement | No alert paged when the expected settlement file was absent after 06:30. The file was detected at 08:10 by a finance analyst. | N33, N34, N41, A3 | Yes | 2 |

#### Weight arithmetic

- Weight 3 causes: tooling 1 + process 1 + design 1 = 3 causes.
- Weight 3 corrective actions: A2 + A5 + A4 = 3 actions.
- Weight 2 causes: process 1 + design 1 + measurement 1 = 3 causes.
- Weight 2 corrective actions: A6 + A1 + A3 = 3 actions.
- Weight 1 causes: environment 1 + people 1 = 2 recorded causes, 0 actions.
- Total scored causes: 3 + 3 + 2 = 8.
- The data row is not separately scored because the review found no independent data cause.

#### Cause to action mapping

| Cause weight | Cause | Corrective action | Owner | Due date | Verification |
|---|---|---|---|---|---|
| 3 | Shared SFTP drop | A2, separate SFTP drop per environment | Hamid Qureshi | 2026-06-26 | Failed read attempt on 2026-06-26 |
| 3 | Ingestion job deletes the file on read | A4, production ingestion exits non-zero on “no file” | Bea Lindqvist | 2026-06-26 | CI verification |
| 3 | Abort checklist leaves pre-production schedules enabled | A5, add “disable every pre-production schedule” | Tomasz Wierzbicki | 2026-06-19 | Rehearsal 2 abort drill |
| 2 | No straddle classification | A1, dual-path reconciliation with a classified straddle set | Bea Lindqvist | 2026-07-03 | Rehearsal 2 passing AC-8 |
| 2 | No missing-file alert | A3, settlement-file-absent page at 07:45 | Bea Lindqvist | 2026-07-09 | N72 and live page on 2026-07-10 |
| 2 | DEP-2 remained requested without escalation | A6, escalate a dependency at “requested” for more than 4 weeks | Ife Adeyemi | 2026-06-19 | Register review log |

### The root cause test

**Candidate:** findings below the register threshold going to an unscheduled backlog, represented by F2.

| Test | Result | Evidence |
|---|---|---|
| Is it something the team can change? | Pass. The finding-routing and dependency-escalation policy can be changed. | A6; N68 |
| Would changing it have prevented this instance? | Pass. Escalating F2 or DEP-2 before rehearsal 1 would have forced a decision on the shared drop or the missing sandbox. | F2; DEP-2; N37 |
| Would changing it prevent the class of failure, not just this case? | Pass. A threshold and escalation rule applies to future environment, dependency and operational findings, not only to HG-INC-14. | A6; R14 |
| Is it stated without a person's name? | Pass. The candidate names a process condition and F2, not a person. | F2 |

**Result:** F2 is the root-cause candidate. The candidate is not “human error”, “the vendor” or “the rehearsal crew”. Those descriptions stop the analysis before the changeable policy and system conditions.

## Reading the result

The five whys reaches a changeable policy and process condition at Why 5. It also records two true answers at Why 3:

1. DEP-2 never committed, leaving production-shaped settlement files as the available fixture.
2. The shared drop allowed the pre-production job to consume that fixture.

The fishbone shows why one fix would not have been sufficient:

- The weight-3 causes were necessary conditions for the incident path and map to A2, A4 and A5.
- The weight-2 causes increased the likelihood or impact and map to A1, A3 and A6.
- The environment and people causes were recorded at weight 1 and not actioned.
- Arithmetic: 3 weight-3 causes + 3 weight-2 causes + 2 weight-1 causes = 8 scored causes.

The result explains both impacts:

- File impact: a pre-production job could read and delete the production file at 07:00.
- Close impact: no missing-file page fired by 07:45, and the straddle set had no classification. Finance detected the issue at 08:10, and the close completed at 12:40.
- Arithmetic: 12:40 minus 07:00 = 5 h 40 min.
- Impact volume: 5,190 settlement lines and £332,000 were reconciled late.

The findings below threshold were not harmless. F2 scored 4 while the register threshold was 6, so it went to HG-812 rather than receiving a scheduled control. After HG-INC-14, it became R14 and was scored 9.

## ILLUSTRATIVE example

This is the Harbourgate incident example. Harbourgate, its people, companies, systems and figures are fictional and ILLUSTRATIVE.

The effect was the Marlowe settlement file deleted at 07:00 on 2026-06-15 and the finance close completing 5 h 40 min late. The chain showed an enabled pre-production job, a shared SFTP drop, no committed DEP-2 sandbox files, and no classified straddle set. The fishbone then separated the causes:

- Weight 3: shared SFTP drop, delete-on-read ingestion design and incomplete abort checklist.
- Weight 2: no straddle classification, no missing-file alert and no dependency escalation.
- Weight 1: Monday's weekend-carrying file and the crew reaching the abort after 9 h 10 min.

The arithmetic was:

- 3 weight-3 causes + 3 weight-2 causes + 2 weight-1 causes = 8 scored causes.
- 12:40 minus 07:00 = 5 h 40 min.
- 1,529 unmatched Marlowe lines out of 1,742 lines were recorded in rehearsal 1.
- 5,190 settlement lines and £332,000 were reconciled late.

The corrective actions were A1 to A6, with A2, A4 and A5 addressing the weight-3 causes, and A1, A3 and A6 addressing the weight-2 causes.

## The trap

The convenient chain would stop at “the rehearsal job consumed a production file” or “the crew did not disable the schedule”. That would omit the shared drop, the missing DEP-2 sandbox, the missing straddle classification and the routing rule that allowed F2 to remain unscheduled.

The review therefore keeps both true answers at Why 3 and records the weight-1 causes without actioning them. The crew's elapsed time and Monday's settlement timing explain contribution and impact, but they are not changeable root causes.

## Feeds

- [harbourgate-journey.md](harbourgate-journey.md): N33, N36, N37, N41, N42, F2, DEP-2, A1 to A6 and R14.
- [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md): HC38, the recorded five-whys and fishbone weights.
- [frameworks/execution/five-whys-fishbone.md](../frameworks/execution/five-whys-fishbone.md): the blank worksheet and method guidance.
- Incident postmortem section 3: contributing causes, using the systems-language causes recorded here.
- Incident postmortem section 5: corrective actions A1 to A6, with owners, due dates and verification methods.
- Risk register: F2 became R14 after HG-INC-14 because the incident showed a higher score.
- Gate 5 attempt 1: the reconciliation line failed at rehearsal 1 on 2026-06-13, and the gate outcome was NO-GO on 2026-06-16.
