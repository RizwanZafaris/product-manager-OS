# Harbourgate RACI: legacy sunset execution

Fills [frameworks/execution/raci.md](../frameworks/execution/raci.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen so that this chart reconciles with the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md). See the [examples index](README.md).

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-10-16 · **Status:** Sunset execution · **Product:** Harbourgate legacy checkout

## What it is for

This chart assigns execution ownership for the legacy sunset. It runs the decommission steps in the sunset plan rather than restating the stakeholder map's eight decision areas.

The accountable person is one named person per deliverable. Responsible people do the work, consulted people can change the work before completion, and informed people are told after completion. The chart covers shutdown of the legacy payment path, the two provider integrations, the contractor's wrapper, the refund tail, the reporting dependency and the post-sunset learning recorded in D-025.

## Run it when

- Preparing the legacy shutdown scheduled for 2026-12-15
- Moving the legacy path through its drain, contract closure and deletion steps
- Reviewing the sunset plan in the OPERATE stage
- Confirming that the work has an owner before the peak change freeze from 2026-11-13 to 2026-12-04
- Checking the remaining work after the last legacy order on 2026-09-07

**Skip it when:** the work is a single-person task with no handoff or blocking dependency. The sunset is not that shape because finance, engineering, security, legal and data engineering each own a part of the execution.

## Inputs you need first

- The [Harbourgate journey](harbourgate-journey.md), especially N52, N53, N58, DEP-4, DEP-7, DEP-8, BR-009, D-023, D-024 and D-025
- The [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), especially HC43 and the TD-2, TD-4 and TD-5 rows
- The sunset plan's decommission steps, including I-5 to I-8
- The stakeholder map's named people and overlapping decision ownership
- The dependency register status for DEP-4 and DEP-7
- The retention schedule for wrapper log deletion by 2027-01-15

## The worksheet

### Step 1: the chart

| Decision area or deliverable | R: does the work (one or more) | A: answers for it (exactly one name) | C: asked before, and can change it (at most three) | I: told after | Forum and cadence where A decides |
|---|---|---|---|---|---|
| Close out the Marlowe and Tidewater billing relationship through contract end | Bea Lindqvist, Priya Raman | Priya Raman | Tomasz Wierzbicki, Rohan Iyer | Ife Adeyemi, Callum Fraser, Anneliese Vogt | Sunset execution review, before the 2026-12-15 contract end |
| Disconnect I-5 to I-8 and revoke legacy credentials | Bea Lindqvist, Hamid Qureshi | Bea Lindqvist | Anneliese Vogt, Tomasz Wierzbicki | Ife Adeyemi, Priya Raman, Rohan Iyer, Dani Ferreira | Decommission runbook review, before each disablement |
| Tear down legacy infrastructure to zero running cost, N53 | Bea Lindqvist, Tomasz Wierzbicki | Tomasz Wierzbicki | Priya Raman, Hamid Qureshi | Ife Adeyemi, Rohan Iyer, Grace Mbeki | Engineering sunset review, before the shutdown and after teardown |
| Narrow monitoring and remove provider-specific alerts | Bea Lindqvist | Bea Lindqvist | Priya Raman, Grace Mbeki, Callum Fraser | Ife Adeyemi, Tomasz Wierzbicki, Hamid Qureshi | Operations dashboard review, before shutdown and after the first post-sunset check |
| Close Marlowe and Tidewater contracts, retaining portal access to 2027-06-15 under N52 | Anneliese Vogt | Rohan Iyer | Priya Raman | Ife Adeyemi, Tomasz Wierzbicki, Hamid Qureshi, Dani Ferreira | Commercial close review, before contract termination |
| Complete the PCI DSS scope re-assessment, DEP-7 | Hamid Qureshi, external assessor | Hamid Qureshi | Anneliese Vogt, Bea Lindqvist | Ife Adeyemi, Rohan Iyer, Priya Raman | Security and compliance review, after the sunset |
| Delete wrapper log files and legacy credentials by 2027-01-15, N58 | Bea Lindqvist, Hamid Qureshi | Hamid Qureshi | Anneliese Vogt, Tomasz Wierzbicki | Ife Adeyemi, Priya Raman, Rohan Iyer | Retention closure review, before deletion and after evidence is filed |
| Run the BR-009 refund tail through the provider portals within 5 working days | Priya Raman, finance operations | Priya Raman | Anneliese Vogt, Bea Lindqvist, Callum Fraser | Ife Adeyemi, Rohan Iyer, Tomasz Wierzbicki | Finance operations review, from 2026-11-16 through portal wind-down |
| Move reporting off the legacy table shape under DEP-4 | Grace Mbeki, Bea Lindqvist | Grace Mbeki | Priya Raman, Tomasz Wierzbicki | Ife Adeyemi, Rohan Iyer, Hamid Qureshi | Data migration review, before DEP-4 completion |
| Complete the post-sunset check and file D-025 | Ife Adeyemi, Tomasz Wierzbicki, Priya Raman, Hamid Qureshi | Ife Adeyemi | Rohan Iyer, Anneliese Vogt, Grace Mbeki | Harbourgate sunset stakeholders | Post-sunset review, on the D-025 target date |

Letter rules applied here:

- Each row has at least one R.
- Each row has exactly one named A.
- Each C is a person who can change the deliverable before completion.
- Each I is told after completion and has no approval vote.
- The chart does not create a new decision area. It translates the sunset plan into executable deliverables.

### Step 2: the checks

| Check | Rule | Fail signal | Fix | Result |
|---|---|---|---|---|
| One A per row | Exactly one name | Zero, two names or a team name | The sponsor and the named owner resolve the row before work starts | Pass: 10 rows have one named A |
| A is a person | A name, never a committee | A team, function or committee is named | Name the person who answers for the outcome | Pass: every A is a named person |
| C load | At most three per row | More than three consultees, or a C cannot change the work | Move non-blocking recipients to I | Pass: no row has more than three C's |
| A load | No person is A on more than the stated cap, HC43 | One person is A on more than 3 rows | Delegate the deliverable or accept the bottleneck explicitly | Pass: maximum A load is 2, below the cap of 3 |
| R exists | At least one R per row | An A has nobody doing the work | Assign a named Responsible person or delete the row | Pass: every row has one or more R's |
| Forum exists | Every A has a calendar slot where they decide | The forum is "as needed" | Add the deliverable to the named sunset, finance, security, data or operations review | Pass: every row names a decision forum |
| Signed | Every A has agreed to their row in writing | Silence is treated as consent | Ask the A to confirm the row and record the confirmation | Pass: the chart is accepted by each named A for the sunset execution review |

A-load arithmetic:

| Accountable person | Rows | Arithmetic | Load |
|---|---|---|---|
| Priya Raman | Stop billing, BR-009 refund tail | 1 + 1 | 2 |
| Bea Lindqvist | Disconnect integrations, narrow monitoring | 1 + 1 | 2 |
| Tomasz Wierzbicki | Infrastructure teardown | 1 | 1 |
| Rohan Iyer | Contract closure | 1 | 1 |
| Hamid Qureshi | PCI DSS re-assessment, log deletion | 1 + 1 | 2 |
| Grace Mbeki | Reporting migration | 1 | 1 |
| Ife Adeyemi | Post-sunset check and D-025 | 1 | 1 |
| **Total** | **10 rows** | **2 + 2 + 1 + 1 + 2 + 1 + 1** | **10** |

Cap check:

**Maximum A load = 2**

**2 < 3, the HC43 cap, so the A-load check passes.**

No row fails two or more checks, and no more than a quarter of the 10 rows fails. The chart can therefore proceed with the sunset plan's execution.

## Reading the result

The A column has a distributed load. Priya Raman, Bea Lindqvist and Hamid Qureshi each answer for two rows. No person exceeds the cap of 3 in HC43.

The overlap with the stakeholder map is deliberate:

- Rohan Iyer remains Accountable for contract termination.
- Hamid Qureshi remains Accountable for PCI scope.
- Priya Raman remains Accountable for finance operations, including the refund tail.
- Grace Mbeki remains Accountable for DEP-4.
- Ife Adeyemi remains Accountable for the post-sunset check and D-025.

The chart also separates adjacent responsibilities. Bea Lindqvist owns the technical disablement and monitoring changes, while Tomasz Wierzbicki answers for the infrastructure teardown. Hamid Qureshi answers for evidence that the security and retention obligations are complete. Anneliese Vogt is consulted on contractual and legal effects, but Rohan Iyer is the single Accountable person for contract termination.

The table-shape removal remains outside the legacy path shutdown. DEP-4 is an execution row because reporting must move off the legacy shape, while the old table shape itself remains scheduled for removal on 2027-03-31 under ADR-0002.

The refund tail remains active after shutdown. BR-009 applies from 2026-11-16, and portal access continues to 2027-06-15 under N52. This is why the refund row and contract row are separate.

## ILLUSTRATIVE example

This Harbourgate RACI is an ILLUSTRATIVE example of A-load arithmetic under a stated cap. The 10 rows distribute across 7 accountable people: Priya Raman 1 + 1 = 2, Bea Lindqvist 1 + 1 = 2, Tomasz Wierzbicki 1, Rohan Iyer 1, Hamid Qureshi 1 + 1 = 2, Grace Mbeki 1, Ife Adeyemi 1, summing to **2 + 2 + 1 + 1 + 2 + 1 + 1 = 10**, matching the 10 rows.

The cap check reads the same arithmetic the other way: the maximum A load is 2 (Priya Raman, Bea Lindqvist and Hamid Qureshi each carry two rows), and HC43 sets the cap at 3, so **2 < 3** and the chart passes without delegating further or escalating a bottleneck.

- If a fourth row had gone to Hamid Qureshi, his load would be 3, still at the cap but requiring the sponsor to accept the bottleneck explicitly under the A-load check.
- A fifth row on any already-loaded person would put that person's load at 4, over the cap of 3, forcing a delegation decision before the chart could pass.

## The trap

The tempting chart would copy the stakeholder map's eight decision areas and call that execution ownership. That would hide the actual work: disabling I-5 to I-8, revoking credentials, deleting wrapper logs, narrowing monitoring and keeping the refund path alive.

A second trap is making Hamid Qureshi Accountable for every security-adjacent task. He owns the PCI DSS scope re-assessment and the retention evidence, but Bea Lindqvist does the integration disablement and Tomasz Wierzbicki answers for infrastructure teardown. The split keeps the A load below HC43 and leaves a Responsible person on every row.

A third trap is treating the contract end as the end of the customer obligation. Marlowe and Tidewater terminate on 2026-12-15, but BR-009, portal access to 2027-06-15 and the post-sunset check remain in the operating plan.

The signed check exists because a chart drafted by the PM alone is not agreement. Each A must accept the row before the sunset execution review treats the assignment as real.

## Feeds

- [Harbourgate journey](harbourgate-journey.md): N52, N53, N58, DEP-4, DEP-7, DEP-8, BR-009, D-023, D-024 and D-025
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md): HC43, plus TD-2, TD-4 and TD-5
- [frameworks/execution/raci.md](../frameworks/execution/raci.md): the blank worksheet and responsibility-charting rules
- The stakeholder map: named people and overlapping decision ownership
- The sunset plan: decommission sequence, refund tail, contract closure and post-sunset work
- The decision log: D-024 establishes the sunset and D-025 establishes the post-sunset learning
- The dependency register: DEP-4 and DEP-7 remain visible until their evidence is complete

**Exit-gate walk, signed:** Ife Adeyemi, Product Manager, 2026-10-16. One A per row, named forums, Responsible coverage, and the HC43 A-load cap are checked. Each accountable owner is named for written agreement in the sunset execution review.
