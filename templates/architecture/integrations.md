# Integrations Register: `<initiative or system name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [architect agent](../../agents/architect-agent.md)

<!-- Every line that crosses a system boundary gets a row here and a detail block
     below. Integrations fail differently from code: the counterparty changes
     something, and your first notice is an incident. The two columns teams skip,
     failure behavior and owner, are the two an incident commander needs at 3 a.m. -->

**Scope:** `<which system's integrations this register covers>`
**Register owner:** `<name>` · **Date:** `<YYYY-MM-DD>` · **Status:** Draft / In review / Approved

## 1. Register

<!-- Direction is from our system's point of view: outbound (we call them), inbound
     (they call us), or bidirectional. SLA is the counterparty's committed number,
     with its source; a remembered number from a sales call is not an SLA. -->

| # | Counterparty system | Direction | Protocol | Auth | Counterparty SLA (and source) | Owner (ours) | Failure behavior (one clause) |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

## 2. Detail block, one per row

<!-- Copy this block once per register row. -->

### Integration `<row #>`: `<counterparty name>`

- Purpose: `<what crosses this boundary and why the product needs it>`
- Data exchanged: `<payload summary, and the PII class it carries per the data model>`
- Environments: `<sandbox available? production credentials held by whom?>`
- Failure behavior, expanded: `<what our system does when the counterparty is down,
  slow, or returning errors: queue and retry / degrade / block the user flow>`
- Backoff and retry policy: `<schedule, cap, and idempotency mechanism>`
- Monitoring: `<the alert that fires when this integration degrades, and who receives it>`
- Counterparty contact: `<named human or support channel, with response SLA>`
- Contract or DPA reference: `<document and clause, or "none" plus a risk register row>`
- Change notice: `<how the counterparty announces breaking changes, and who on our side watches>`

## 3. Failure drill

<!-- Before Gate 3, answer for the register as a whole. -->

- If every outbound integration failed at once, the user could still: `<what degrades gracefully>`
- The integration whose failure hurts most is `<row #>` because `<reason>`; its mitigation is `<link to risk register row>`.

## Exit gate

- [ ] Every boundary line in the solution architecture one-pager has a register row
- [ ] Every row has a named owner on our side
- [ ] Every SLA cites its source document, not a recollection
- [ ] Every detail block states failure behavior a user would recognize
- [ ] Retry policies name their idempotency mechanism
- [ ] Every integration with no contract or DPA reference has a risk register row
- [ ] The worst-single-failure answer in section 3 is written and its mitigation linked
