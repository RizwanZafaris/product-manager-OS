---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Core banking", "core banking systems", "retail banking", "core-banking"]
---
# Core banking

The core banking system is the ledger of record for every retail and SME deposit account: every other screen, app, and report is a client reading from it or writing to it. The distinctive fact is that most work here is not green field. It is modernising, replacing, or wrapping a system that has run for decades, and the industry's canonical failure stories are cutovers, not feature bugs. A core migration is executed in a single weekend and becomes a one way door the moment the old system is switched off. The second distinctive fact is double entry: every posting is a debit and a credit, so a change that looks like "add a field" actually touches reconciliation, interest accrual, statementing, and regulatory reporting at once, and a reconciliation break that would be a bug ticket anywhere else is a regulatory event here. The third is that the deposits sitting in that ledger are not the bank's money. The bank is a fiduciary custodian of somebody else's cash, and the safety net behind that fact, deposit insurance, a licensing regime, a resolution plan, shapes what the product may do before a single feature is designed.

## Questions a PM must ask

1. Is this a green field core or a migration off an existing one, and if it is a migration, what is the rehearsed cutover and rollback plan? An unrehearsed rollback is a plan on paper, not a control.
2. During a dual running period, which system is the single source of truth for a balance? Two cores can each believe they are authoritative, and the customer sees whichever one answers first.
3. Does this feature write to the general ledger, or only read from a downstream replica? A ledger write carries reconciliation and audit consequences a read never does.
4. What happens to interest accrual, standing instructions, and direct debits during the cutover window? Silence here is how standing payments get dropped without anyone deciding to drop them.
5. Which deposit insurance scheme covers this account type, up to what limit, and does the customer facing copy state it accurately? Misstating coverage is its own compliance failure, independent of whether the product works.
6. What is the reconciliation process between the ledger and every downstream system, statementing, card processing, the mobile app's cached balance, and how fast is a break actually caught?
7. Who can see or override a customer's transaction history, and what does the audit trail capture when a teller or an operations user makes that override?
8. What does degraded mode look like when the core is unreachable? Payroll and cash withdrawal have no acceptable downtime, so the offline path is a requirement, not a nicety.

## Gatekeepers

- **The banking supervisor.** The specific regulator varies by charter and geography (a joint prudential and conduct regulator in the UK, the State Bank of Pakistan for Pakistani banks), but every one issued the licence this product runs under and can compel an independent review after an incident.
- **The deposit insurer.** Cares less about your roadmap than about whether the core can produce an accurate, current list of insured depositors within days of a failure. A migration that cannot answer that question mid cutover is a resolution readiness gap, not only an IT risk.
- **Internal audit and the migration steering committee.** Owns the cutover go or no go decision and asks for a rehearsed rollback with a measured time, not a described one.
- **The AML and financial crime function, the MLRO.** Opening a deposit account is a regulated customer due diligence act under FATF Recommendations and the bank's own anti money laundering programme; a faster onboarding flow that quietly waters down verification is a finding waiting to happen.
- **Resolution and recovery planning teams.** Recovery and resolution regimes, Dodd-Frank Title I style living wills in the US and the equivalent UK and EU resolution frameworks, want assurance that the ledger and payment rails keep working, or fail predictably, if the bank itself is put into resolution.
- **National payment scheme operators.** The domestic instant or bulk payment rail the core connects to, Pakistan's Raast, run by the State Bank of Pakistan, is a clear non-US example, certifies message format compliance and can suspend a participant that breaks it.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Core system availability | Whether customers can transact | A definition that excludes batch windows or "planned maintenance" hides real customer facing downtime |
| End of day batch completion time | Back office health | A batch that finishes late but before branch open looks fine while it compresses every downstream reconciliation window |
| Reconciliation break count and aging | Ledger integrity | A shrinking count can mean breaks are being written off rather than investigated |
| Straight through processing rate on payments | Payment efficiency | Improves by routing exception prone payment types to a separate, unmeasured queue |
| Account opening turnaround time | Onboarding friction | Gamed by pre-qualifying easy applicants or excluding cases pending manual review from the clock |
| Deposit attrition or runoff rate | Franchise health | Aggregated across the book, it hides concentration; a handful of large uninsured depositors leaving looks identical to broad, harmless churn |
| Migration data reconciliation match rate | Cutover readiness | A high match rate on record count says nothing about whether the mismatched few are the highest value accounts |
| Failed or returned payment rate | Payment quality | Falls when acceptance criteria tighten and marginal payments are rejected upfront, moving the failure onto the customer's other bank |
| Cost to serve per account | Unit economics | Improves by pushing low balance customers to self service or closing "unprofitable" accounts, which is a fair access question, not only a cost one |
| Time to detect a ledger discrepancy | Control effectiveness | The median hides the tail, and the one discrepancy that takes weeks to surface is the one that mattered |

## Reading

- **TSB Bank's 2018 core migration.** The move to a new platform locked customers out of banking for weeks and drew a joint fine from the FCA and PRA (verify the exact date and amount before relying). Read it as the reference case for what an unrehearsed cutover actually costs.
- **The Basel III liquidity and capital framework.** Its liquidity coverage and funding stability tools shape what a deposit product is allowed to promise from a treasury standpoint, independent of what the app says.
- **Deposit insurance regimes.** The FDIC in the US is the best documented model; Silicon Valley Bank's collapse in March 2023 is the modern case study in how quickly uninsured deposits can run once a digital channel makes exit frictionless.
- **The UK's ring fencing regime**, under the Financial Services (Banking Reform) Act 2013, separates retail deposit taking from investment banking activity, which bounds what a shared core can actually be used for.
- **State Bank of Pakistan's prudential regulation and the Raast instant payment system**, rolled out in phases from 2021 (verify exact phase dates before relying), as a non-US example of a central bank operating the rail a retail core connects to directly.
- **A note on model driven monitoring:** where transaction monitoring for AML uses a machine learning model rather than fixed rules, treat that as the AI in finance case in [modules/regulated/README.md](../../modules/regulated/README.md) rather than inventing a separate acceptance bar here.

**Conductor overlay:** this domain sharpens DESIGN-1 (the rejected alternative, since migrate versus wrap is the design decision that defines the whole programme), DESIGN-2 (integrations, because every downstream reader of the ledger needs an owner and a failure behavior before cutover), DELIVER-1 (the rollback, which for a core migration is rehearsed or it does not exist), and OPERATE-4 (cost to run, where reconciliation load and break aging are the operational numbers that matter).

**Templates this bends:** [migration-cutover-plan](../../templates/delivery/migration-cutover-plan.md) (the rollback rehearsal is the acceptance criterion, not the plan document itself), [data-model](../../templates/architecture/data-model.md) (account and ledger classes carry retention and reconciliation ownership per class), [release-readiness](../../templates/delivery/release-readiness.md) (a cutover go or no go line replaces the generic launch line), and [sla-slo-definition](../../templates/delivery/sla-slo-definition.md) (uptime has to be defined against batch and real time posting separately, or it measures nothing).
