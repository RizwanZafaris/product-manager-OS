# Agent Architecture: Ledgerline customer add-on

Fills [templates/ai/agent-architecture.md](../templates/ai/agent-architecture.md). Everything here is invented: Ledgerline is a fictional software company, the customer add-on is fictional, the people and identifiers are fictional, and every model, prompt, threshold and finding is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and [coverage sheet](ledgerline-coverage-sheet.md). See the [examples index](README.md).

**System:** The Ledgerline customer add-on extracts receipt fields and matches them to the customer's own policy so a filer receives a confidence-flagged draft, while the filer and reviewer remain accountable for submission and approval. **Architecture owner:** Priya Nair · **Document date:** 2026-11-04

The customer overlay reuses internal evidence only where a written reason says it transfers, per D1. LEDGERLINE-S2 transfers the receipt-to-draft flow to customer accounts, and LEDGERLINE-S3 transfers confidence flags to the customer reviewer. The customer policy excerpt replaces Ledgerline's policy in `copilot-policy-match` v4, and the customer policy is treated as quoted data in v5, per [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md), LC17.

## 1. Agent roster

| Agent | Purpose (one sentence) | Model tier (see routing note below) | Tools allowed (exhaustive list) | Data access (systems, scope) | Can it write or only read? |
|---|---|---|---|---|---|
| extraction agent | Extracts receipt fields and a confidence value for each extracted field. | extraction tier | Receipt image or forwarded receipt content read; extraction response return | The current receipt input for the current customer account only, with no access to another account, account policy, billing, entitlement, mappings or submission state | read only; returns a scoped result to the orchestrator |
| policy-match agent | Matches the extracted fields to a policy line from the current customer account and returns a confidence value for the suggested category. | drafting tier | Extracted-field result read; current account policy excerpt read; policy-match response return | The current receipt's extracted fields and the current customer account's retrieved policy excerpt only, with no access to another account, account policy, billing, entitlement, mappings or submission state | read only; returns a scoped suggestion to the orchestrator |

Both agents use the model pinned as `docmodel-2026-09-30`, per LC16. The extraction prompt is `copilot-extract` at v7 on this Gate 3 date, with v8 current after the RT-07 fix (abstain on non-English amount/date) lands on 2026-11-06, per LC17. The policy-match prompt is `copilot-policy-match` at v4 on this Gate 3 date, with v5 current after the customer policy text is wrapped as quoted data on 2026-11-06, per LC17. An extracted field or suggested category under 0.80 model confidence is flagged to the reviewer, per LC22.

Neither agent can submit a report, activate an add-on, bill an account, change a category mapping, or read another account's policy. The agents do not decide entitlement. The entitlement check moved into the deterministic orchestrator after RT-06, so a draft cannot be produced for an account without the add-on active.

## 2. Least-access check

For each agent above:

### Extraction agent

- Tool it has but did not need in the last review period: none
- Broadest single permission, and why it cannot be narrower: read the current receipt input, because extraction cannot run without the receipt content; the permission is limited to the current account and current receipt
- What the worst plausible misuse of its access looks like: it could expose or misread information contained in the current receipt, but it cannot access another account, policy, mapping, entitlement, billing or submission action
- Reviewed by Priya Nair and Nadia Rahimi on 2026-11-04, next review 2027-02-04

### Policy-match agent

- Tool it has but did not need in the last review period: none
- Broadest single permission, and why it cannot be narrower: read the current account's policy excerpt and the current receipt's extracted fields, because the match requires both sources; the permission excludes the full policy corpus, other accounts and all write actions
- What the worst plausible misuse of its access looks like: an instruction planted in the current account's policy could attempt to redirect the match, but policy text is treated as quoted data and the agent cannot change mappings or submit a report
- Reviewed by Priya Nair and Nadia Rahimi on 2026-11-04, next review 2027-02-04

The least-access review is recorded in LC30 of [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md).

## 3. Orchestration pattern

- Pattern: fixed pipeline
- Who decides the next step: deterministic code
- Where the plan lives and whether a human can inspect it mid-run: the fixed pipeline definition in the application code, yes
- Concurrency: no parallel agents; the pipeline serializes entitlement, extraction, policy matching and draft assembly, and deterministic code serializes all conflicting writes
- Failure of one agent: halts the run for that receipt; the filer receives a blank, flagged draft rather than an unreviewed suggestion
- For handoffs, shared state, and termination rules, fill multi-agent-workflow.md; this document owns who exists and what they may touch, that one owns how they cooperate

The orchestrator checks entitlement before either agent runs. It then passes the current receipt to the extraction agent, passes the extraction result and the current account's policy excerpt to the policy-match agent, and assembles a draft for human review. RT-06 found that the forwarded-email path could skip entitlement and produce drafts for accounts without the add-on active. The entitlement check was moved into the orchestrator, and the path was re-attacked and held, per LC28.

## 4. Boundaries with humans

- Actions requiring approval before execution: the filer submits the report; the finance reviewer confirms flagged fields; a finance admin confirms any category mapping correction, which is logged and is not fed back into the agents in v1; the account admin confirms the add-on charge before activation. These actions are mirrored in the human approval gates document. No auto-submit path exists, as required by the PRD.
- Rails that bound every agent in the roster: the filled guardrails document for the Ledgerline customer add-on, including the no-auto-submit line, account isolation, confidence flagging, prompt rollback and the cost caps. The relevant customer-tenancy red-team findings are RT-03, RT-05 and RT-06 in [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): coaxing another account's policy line held, an auto-submit request held because no submit tool exists, and the forwarded-email entitlement bypass was fixed and held on re-test.
- How a human stops the whole system now: the application kill switch in section 4 of the guardrails document stops the fixed pipeline and prevents new agent runs; the on-call engineer owns the stop action and the prior prompt version is redeployable in 15 minutes, per LC29

The agents cannot activate or bill an account. Entitlement and charge computation remain outside the agents. ADR-007 states that the add-on entitlement and charge are computed from the billing system's seat count, not from a product-side counter. The agents have no billing or activation tool.

## Model routing note

Do not hard-wire one model into every agent. The roster's tier column maps each agent to a routing tier: extraction-grade work runs on the cheap tier, drafting on the coding tier, judgment calls on the reasoning tier. The tier doctrine, the config format, and the fallback recipe live in [routing README](../routing/README.md) and [routing config](../routing/omniroute.config.json); the extraction agent uses the extraction tier and the policy-match agent uses the drafting tier.

## Exit gate

- [x] Every agent has an exhaustive tool list; "and other tools as needed" appears nowhere
- [x] The least-access check is filled per agent with a reviewer and dates
- [x] Write access is scoped and justified everywhere it appears
- [x] Every irreversible action routes through a gate in the human approval gates document
- [x] Each agent names a routing tier, and the tier exists in the routing config

Signed at Gate 3, 2026-11-04: Priya Nair, engineering lead; Nadia Rahimi, application security lead.
