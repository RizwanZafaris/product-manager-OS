# Edge-Case Register: [product or feature name]

**Stage:** BUILD into DELIVER (feeds [Gate 4: acceptance criteria met](../../os/STAGE-GATES.md), rechecked at Gate 5)
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- The happy path is what the team builds by instinct. This register is where the
     product earns its keep. One rule governs the whole file: no case is left
     "to be decided". Every row either states the expected behavior, or it escalates
     to a named person with a date. A register full of question marks is a bug
     tracker waiting to happen. -->

**Owner:** [name] · **Status:** Draft / Complete · **Date:** [YYYY-MM-DD]

## 1. Hunting list

<!-- Walk each category against your feature before declaring the register done.
     Check the box when the category has been considered, even if it produced zero
     rows. An unchecked box means nobody looked. -->

- [ ] Empty, null, and missing values
- [ ] Boundary values (zero, one, maximum, one past maximum)
- [ ] Duplicates, retries, and double submission
- [ ] Concurrency (two users, two tabs, two devices)
- [ ] Permissions and roles (wrong user, expired session, revoked access)
- [ ] Time (timezones, daylight saving, leap days, clock skew)
- [ ] Localization and encoding (long names, non-Latin scripts, emoji, RTL text)
- [ ] Network failure, timeout, and partial failure mid-transaction
- [ ] Malicious input (injection, oversized payloads, unexpected content types)
- [ ] Volume (the 10x day, the empty account, the account with years of history)
- [ ] For AI features: refusal, escalation, and never-invent behavior (see [guardrails](../ai/guardrails.md) and [red-team review](../ai/red-team-review.md))

## 2. Register

<!-- Linked test ID is mandatory once the case is agreed. A case without a test is an
     intention. The italic row shows a completed entry. -->

| ID | Case | Trigger | Expected behavior | Linked test ID | Status |
|---|---|---|---|---|---|
| EC-1 | | | | | Open / Agreed / Tested |
| EC-2 | | | | | |
| *EC-0* | *user submits the same form twice* | *double click on submit* | *second request is idempotent, one record created, user sees one confirmation* | *T-1042* | *Tested* |

## 3. Escalations

<!-- The only legal alternative to an expected behavior. If a case needs a product
     decision, it goes here with a name and a date, and it comes back as a row above. -->

| ID | Case needing a decision | Decider | Decide by | Resolved as |
|---|---|---|---|---|
| | | [name] | [YYYY-MM-DD] | |

## Exit gate

This document passes when:

- [ ] Every hunting-list category is checked, meaning someone actually looked
- [ ] Every register row has an expected behavior, none say "to be decided"
- [ ] Every Agreed or Tested row links a real test ID
- [ ] Every escalation has a named decider and a date, and none is overdue
- [ ] The register was reviewed against the [failure scenarios](failure-scenarios.md) for overlap

Signed: [name], [role], [YYYY-MM-DD]
