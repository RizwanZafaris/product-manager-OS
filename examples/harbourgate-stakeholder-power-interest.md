# Harbourgate Stakeholder Power-Interest Grid

Fills [frameworks/execution/stakeholder-power-interest.md](../frameworks/execution/stakeholder-power-interest.md).

Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, chosen to reconcile with the [Harbourgate journey](harbourgate-journey.md) and its [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Ife Adeyemi, Product Manager · **Date:** 2026-06-25 · **Status:** Scored before Gate 5 planning · **Product:** Harbourgate checkout modernisation

## What it is for

This grid sorts the people who can affect Harbourgate's payment migration by power and interest, using behaviour in the prior 30 days. It answers where Ife Adeyemi's engagement time goes before the phased cutover plan is used.

Power and interest use the 1 to 5 instrument defined by the worksheet. A score of 3 is high. The grid produces six people in manage closely, one more than the reading allows, so Tomasz Wierzbicki co-owns the Noor Haddad and Hamid Qureshi relationships.

This is a different instrument from the stakeholder map's H/M/L ratings dated 2026-10-14. The reconciliation is recorded in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), note 8. This grid does not translate its 1 to 5 scores into those later H/M/L ratings.

## Run it when

- Before the Harbourgate cutover plan is agreed, on 2026-06-25.
- Before Gate 5, because the plan changes how web, app and kiosk payments move to Kestrel.
- Before the first kiosk cohort, because Lena Baptiste owns store operations across 61 shops and the store window must be understood before execution.
- After a decision stalls, or when a person with power has not seen the evidence behind a cohort, rollback or reconciliation decision.
- Again before later gates, because power and interest can change as the migration moves from design into live store operations.

**Skip it when:** the initiative has one sponsor, one team and one month. Harbourgate does not meet that condition: it has web, app and kiosk surfaces, three provider integrations, finance reconciliation, PCI DSS scope and store operations dependencies.

## Inputs you need first

- The candidate list from the journey cast: people who can sign, stop, fund or operate the work.
- Decision areas from the [RACI worksheet](../frameworks/execution/raci.md), including scope, budget, cohort go or no-go, abort during a window, reconciliation sign-off, PCI scope, the store cohort schedule and contract termination.
- The current concerns evidenced in the [Harbourgate journey](harbourgate-journey.md), rather than inferred from titles.
- The current cutover assumptions from [harbourgate-journey.md](harbourgate-journey.md): 61 shops, the 06:00 to 07:30 local store window, per-shop rollback and the phased provider cohorts.
- The supplementary scoring record, HC42, in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md).

## The worksheet

### Step 1: score

Power and interest are scored from behaviour in the prior 30 days, as recorded on 2026-06-25. Power is 1 to 5, where 1 means no influence on this work and 5 means the person can stop it and move its budget. Interest is 1 to 5, where 1 means unaware and 5 means an outcome of their own rides on it.

| Stakeholder (role) | Power | Evidence for the power score | Interest | Evidence for the interest score | Quadrant | Stance (sponsor / neutral / skeptic / opponent) |
|---|---:|---|---:|---|---|---|
| Tomasz Wierzbicki, Engineering Lead and cutover lead | 4 | Has authority to abort; co-decided D-021 on 2026-06-18 and owns the cutover design | 5 | Co-owned the change from the failed one-weekend shape to phased cohorts and the legacy drain | Manage closely | sponsor |
| Bea Lindqvist, Senior Engineer, payments | 2 | Owns Quay reconciliation, the integrations register and the dashboard, but does not hold the release veto | 5 | Owns the reconciliation and corrective actions after HG-INC-14 | Keep informed | sponsor |
| Noor Haddad, QA Lead | 4 | Holds the QA signature and facilitated the failure and postmortem work | 4 | Facilitated the postmortem on 2026-06-17 and is responsible for evidence that failure scenarios are exercised | Manage closely | neutral |
| Priya Raman, Head of Finance Operations | 4 | Owns daily close and reconciliation sign-off | 5 | Co-decided D-021 and owns the finance consequences of settlement and straddle errors | Manage closely | skeptic |
| Rohan Iyer, CFO, sponsor and budget owner | 5 | Can move the budget and accept a material business risk | 3 | Sponsor attention is required for the accepted single-provider risk and the release decision, but his day-to-day interest is lower than the delivery owners' | Manage closely | sponsor |
| Saoirse Whelan, Fraud and Risk Lead | 2 | Can change fraud rules and raise a security or fraud finding, but does not own cutover approval | 4 | Her team identified the double authorisations on 2026-05-19 and owns the decline event stream dependency | Keep informed | neutral |
| Hamid Qureshi, Information Security Lead and PCI DSS owner | 4 | Owns the PCI DSS scope decision and security review | 4 | Reviewed the SFTP separation, scope and security findings during the migration work | Manage closely | skeptic |
| Lena Baptiste, Head of Store Operations | 4 | Controls store operations across 61 shops and their kiosks, and can prevent a store cohort from running | 2 | The kiosks are an operational dependency, but the migration was not her daily focus until the store window was introduced | Keep satisfied | skeptic |
| Callum Fraser, Support Lead | 2 | Controls support and on-call briefings, but cannot approve a cohort | 3 | Needs the support behaviour and fallback explained before customer-facing change | Keep informed | neutral |
| Grace Mbeki, Data Engineering Lead | 2 | Owns reporting's dependency on the legacy table shape, but does not control cutover | 3 | Needs to track Quay's continued writing of the legacy table shape and the later DEP-4 migration | Keep informed | neutral |
| Anneliese Vogt, Legal Counsel and Data Protection Officer | 4 | Owns compliance sign-off and provider termination notices | 3 | Must review the provider contracts, data retention and termination path, but is not in the daily delivery loop | Manage closely | neutral |
| Ines Castellanos, Design Lead | 1 | Owns the deferred guest checkout redesign, which is out of scope for this migration | 2 | The migration changes no new customer-facing surface and does not require her daily attention | Monitor | neutral |

**Quadrant arithmetic:**

- Manage closely: Tomasz Wierzbicki + Noor Haddad + Priya Raman + Rohan Iyer + Hamid Qureshi + Anneliese Vogt = 6.
- Keep satisfied: Lena Baptiste = 1.
- Keep informed: Bea Lindqvist + Saoirse Whelan + Callum Fraser + Grace Mbeki = 4.
- Monitor: Ines Castellanos = 1.
- Total scored: 6 + 1 + 4 + 1 = 12.

Quadrant rule applied: power or interest of 3, 4 or 5 is high.

### Step 2: the four modes

| Quadrant | Mode | What they get | Cadence floor | Relationship owner |
|---|---|---|---|---|
| High power, high interest | Manage closely | Co-ownership of decisions, early drafts, direct access to the cutover evidence and reconciliation results | Every two weeks, plus before every gate | Ife Adeyemi, with Tomasz Wierzbicki co-owning the Noor Haddad and Hamid Qureshi relationships |
| High power, low interest | Keep satisfied | One-page summaries, no surprises, the single operational ask needed from store operations | Monthly, plus before any gate they sign or any store cohort | Ife Adeyemi |
| Low power, high interest | Keep informed | Working sessions, previews, evidence from the payment path and credit for findings | Weekly channel update | Ife Adeyemi, with Bea Lindqvist owning the operational detail |
| Low power, low interest | Monitor | The launch or change note, with no request for recurring meeting time | At launch or when the out-of-scope boundary changes | Ife Adeyemi |

The manage-closely relationship load is not left with Ife Adeyemi alone. Tomasz Wierzbicki co-owns Noor Haddad and Hamid Qureshi because the count is 6, while the reading says more than 5 means the PM is broadcasting rather than managing.

### Step 3: the engagement plan

These rows cover every person in the top two quadrants and every skeptic. The Lena Baptiste row is the row carried into section 3 of the stakeholder map.

| Stakeholder | Quadrant | What they need to hear, in their terms | What you need from them | Who engages | By when | Movement target |
|---|---|---|---|---|---|---|
| Priya Raman | Manage closely | The phased cohorts preserve daily close, the straddle set is classified, and reconciliation remains within the £50 per provider per day tolerance with 0 lines on count once the straddle set is classified | Reconciliation sign-off and a clear stop decision if finance cannot close | Ife Adeyemi | 2026-07-08, Gate 5 attempt 2 | skeptic to neutral before Gate 5 |
| Hamid Qureshi | Manage closely | The migration reduces PCI DSS scope from 7 systems at entry toward 3 after sunset, while the SFTP separation and retention controls address the known findings | Security review, PCI scope evidence and confirmation that the production drop cannot be read from pre-production | Tomasz Wierzbicki, co-owned with Ife Adeyemi | 2026-06-30 for the PCI scope review, then before each cohort | skeptic to neutral before the first kiosk cohort |
| Noor Haddad | Manage closely | A failure scenario is evidence only when it is exercised, and the rollback and reconciliation checks have named observers and results | QA signature on rehearsal evidence and confirmation that the failure scenarios are exercised | Tomasz Wierzbicki, co-owned with Ife Adeyemi | 2026-06-27, rehearsal 2, and before Gate 5 | neutral to sponsor |
| Rohan Iyer | Manage closely | The single-provider decision is explicit, the Kestrel outage risk is accepted by name, and the cutover can stop without an unapproved budget or contract surprise | Sponsor decision on the accepted risk and the release or sunset consequence when required | Ife Adeyemi | Before the provider leaves and at the Gate 5 decision | sponsor maintained |
| Anneliese Vogt | Manage closely | The contract, retention and provider termination obligations are visible in the plan, including the legacy path and its data | Compliance sign-off and confirmation of the legal route for provider termination | Ife Adeyemi | Before the relevant gate and before provider notices | neutral maintained |
| Tomasz Wierzbicki | Manage closely | The plan has a reversible cohort shape, a tested abort path and explicit co-ownership for the relationships that exceed the reading's five-person limit | Cutover ownership, abort authority and co-ownership of Noor Haddad and Hamid Qureshi | Ife Adeyemi | 2026-07-08, when cutover plan v2 is approved | sponsor maintained |
| Lena Baptiste | Keep satisfied | Store operations gets a 06:00 to 07:30 local window, before the earliest shop opens at 08:00, with per-shop rollback and the kiosk fallback if a call fails | Agreement to the store window and the operating plan for each shop cohort | Ife Adeyemi | By 2026-07-31, before the first kiosk cohort | skeptic to neutral before the first kiosk cohort |

## Reading the result

Six people land in manage closely:

`1 Tomasz Wierzbicki + 1 Noor Haddad + 1 Priya Raman + 1 Rohan Iyer + 1 Hamid Qureshi + 1 Anneliese Vogt = 6`

The reading allows no more than 5 before the PM is broadcasting:

`6 - 5 = 1 person over the reading`

Tomasz Wierzbicki therefore co-owns two relationships, Noor Haddad and Hamid Qureshi. The PM retains the decision context, while Tomasz carries the engineering, QA and security working relationships that need direct technical access.

Lena Baptiste is alone in keep satisfied:

`1 person in keep satisfied = Lena Baptiste`

Her row is deliberately operational rather than generic. The ask is the 06:00 to 07:30 local store window, before the earliest shop opens at 08:00, with per-shop rollback. It is due by 2026-07-31, before the first kiosk cohort.

The low-power, high-interest quadrant has four people:

`4 people = Bea Lindqvist + Saoirse Whelan + Callum Fraser + Grace Mbeki`

They are the evidence base and the early-warning system. Their information is needed weekly even though they do not hold the cutover veto.

This grid must not be merged with the stakeholder map's later H/M/L instrument. The grid is a 1 to 5 scoring instrument from 2026-06-25. The stakeholder map uses H/M/L ratings dated 2026-10-14. The reconciliation note in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md) records that difference: Lena Baptiste was the only person in the high-power, low-interest position at Gate 2 (2026-04-07) and in this 2026-06-25 grid, but her interest had moved to M by the 2026-10-14 stakeholder-map review, once her cadence settled into a standing weekly report by the third store cohort (2026-08-17).

## ILLUSTRATIVE example

This Harbourgate example applies the grid to the day cutover plan v2 was drafted and Lena Baptiste was first walked through the store window. The scores are behaviour-based, not title-based:

- Tomasz Wierzbicki has power because he can abort and interest because he co-owns the phased cutover.
- Priya Raman has power through finance close and interest because reconciliation determines whether the migration can proceed.
- Hamid Qureshi has power through PCI DSS and security review, with skeptic stance because the controls must be evidenced.
- Lena Baptiste has power over the 61 shops and kiosks, but lower current interest, so she receives a concise operational plan rather than daily delivery detail.
- Bea Lindqvist and Saoirse Whelan are kept informed because their evidence can identify payment, fraud and reconciliation problems before a cohort advances.

The engagement plan is the useful output, not the labels alone. It turns the six-person manage-closely overload into named co-ownership and gives the store-operations relationship a specific window, rollback behaviour and date.

## The trap

The trap in this Harbourgate reading is scoring by title or by the person who speaks most often. A title-only grid would either under-score Hamid Qureshi, whose security decision can stop the migration, or over-score Lena Baptiste as highly interested simply because 61 shops are affected.

The evidence column prevents both errors. Power means power over this work, including abort authority, finance sign-off, PCI scope and store cohort control. Interest means observed attention to the current migration, not the importance of the person's job.

The second trap is treating the 2026-06-25 scores as permanent. The stakeholder map's H/M/L ratings are from 2026-10-14 and use a different instrument. This grid is retained as the earlier decision record, while the later map is reconciled rather than overwritten.

## Feeds

- [Stakeholder map](../templates/execution/stakeholder-map.md), section 1 for the scores and section 3 for the Lena Baptiste engagement row.
- [RACI chart](../frameworks/execution/raci.md), where high-power stakeholders without an A or C cell are findings for both sheets.
- [Risk register](../templates/execution/risk-register.md), for sponsor drift and an unengaged veto-holder.
- [Program charter](../templates/planning/program-charter.md), governance context if the initiative shape changes.
- Gate 2 in [os/STAGE-GATES.md](../os/STAGE-GATES.md), with the grid re-scored before later gates.
- Method background: [High Output Management](../knowledge/high-output-management.md), the leverage argument behind spending engagement time where it moves the outcome.
- Data source: [harbourgate-journey.md](harbourgate-journey.md).
- Supplementary scoring source: [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), HC42 and reconciliation note 8.

**Exit gate walk:** Ife Adeyemi, Product Manager, signed this grid on 2026-06-25. Six people are in manage closely, Tomasz Wierzbicki co-owns the Noor Haddad and Hamid Qureshi relationships, Lena Baptiste is alone in keep satisfied, and her 06:00 window, per-shop rollback and 2026-07-31 engagement row is ready to carry into the stakeholder map.
