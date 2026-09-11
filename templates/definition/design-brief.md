---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/jobs-to-be-done.md"
aliases: ["Design Brief", "design-brief"]
---
# Design Brief: [feature or product name]

Stage: DEFINE, feeds [Gate 2: requirements signed off](../../os/STAGE-GATES.md); written alongside the PRD, before design work starts
Knowledge: [Jobs to be done](../../knowledge/jobs-to-be-done.md)
Skill: [drafting agent](../../agents/drafting-agent.md) for the first draft; [user-interview](../../skills/user-interview/SKILL.md) for the evidence behind section 2

> **Delete any section you do not need.** A one-squad feature fits on one page; sections 6 and 7 are the two that must survive any cut, because a brief with no deliverables and no review dates is a mood. Weight follows [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md). Never leave a heading standing over white space.

<!-- The agreement between product and design on the problem, the users, the
     constraints, and what done looks like, before any pixels. It prevents the
     review where the designer hears the real constraint for the first time and the
     PM sees the real user for the first time.

     Neighbours: the PRD (prd.md) owns requirements and success metrics, and this
     brief links them rather than restating them; the user research plan
     (../discovery/user-research-plan.md) owns the research; the design sprint
     runbook in the frameworks layer is one way to run the week this brief opens;
     the accessibility checklist (../architecture/accessibility-checklist.md) owns
     the WCAG evidence that section 3 promises.

     Fill first: the problem in section 1, the users and their jobs in section 2,
     and the constraints in section 3. -->

**Product owner:** [name] · **Design lead:** [name] · **Engineering counterpart:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Agreed / Superseded
**Links:** [PRD](prd.md) · [problem framing](../discovery/problem-framing.md) · [personas](../discovery/personas.md)

## 1. The problem

[Two to four sentences copied from the problem framing, not restated: who is stuck, at what moment, and what progress they are trying to make. State the evidence weight behind it. If a solution guess already exists, write it on its own line, label it a guess, and check it against the [assumptions register](assumptions-register.md): a guess with no confidence, validation method, and validate-by date there is a solution smuggled in as a problem, however it reads on the page.]

## 2. Users

<!-- One primary user, named precisely, with the job they are hiring the product
     for and what they do today instead. Secondary users get a row each. A brief
     for "all users" designs for none of them. -->

| User (persona link) | Primary or secondary | Job to be done | Current workaround | What better means, in their words | Evidence |
|---|---|---|---|---|---|
| | primary | | | | |
| | secondary | | | | |

## 3. Constraints

<!-- Hard constraints cannot move without the named source's signature. Label
     honestly: a team that calls every preference hard loses the word when it needs
     it. Accessibility is a row on every brief, never a later phase. -->

| Constraint | Type (platform / design system / accessibility / localization / legal / brand / technical / time) | Hard or soft | Source |
|---|---|---|---|
| Uses the design system's components unless a gap is logged | design system | | |
| Design system and version in use: [name and version, pointed at `products/<name>/DESIGN.md`]; gaps against it are logged in that file's Known gaps section, not here | design system | | [DESIGN.md](../architecture/design-md.md) |
| Meets [WCAG level] with evidence in the accessibility checklist; the level itself is copied from [nfr.md](nfr.md) section 5, not chosen here | accessibility | hard | |
| Locales and text direction: [languages in scope; LTR / RTL / bidirectional] | localization | | |
| Reduced motion is honoured per the platform preference | accessibility | | |
| Supported breakpoints: [named widths or device classes] | platform | | |
| Conventions kept rather than deliberately broken: a familiar pattern used because users already know it, per the Jakob's Law row of [ux-laws-evidence.md](../../knowledge/design/ux-laws-evidence.md); a deliberate break is named and defended here, not discovered in critique | design system | | |
| Where complexity lives when it cannot be removed: pushed to the system rather than the user, per the Tesler's Law row of [ux-laws-evidence.md](../../knowledge/design/ux-laws-evidence.md) | technical | | |
| Third-party UI components carry licence clearance recorded in the [dependency register](../execution/dependency-register.md) before use | legal | hard | |
| | | | |

## 4. Success

<!-- Metrics are the PRD's, by reference. The brief adds how the design is tested
     before launch, because a design tested only in production is a bet with users
     as the stake. -->

| Outcome | Metric (PRD reference) | Target (ILLUSTRATIVE until agreed) | Pre-launch test (usability test, prototype study, experiment) | Test date |
|---|---|---|---|---|
| | | | [usability-test-plan.md](../discovery/usability-test-plan.md) copy | |

## 5. Out of scope

| Excluded | Why | Where it went (backlog / never / another brief) |
|---|---|---|
| | | |

## 6. Deliverables

<!-- Fidelity matches the decision the deliverable informs. A high-fidelity mock
     to settle a flow question is a week spent on the wrong variable. The
     states a screen or component must render belong in
     [ui-state-inventory.md](ui-state-inventory.md), listed once there and
     referenced by every deliverable that depends on it, rather than
     restated per deliverable. -->

| Deliverable | Fidelity (sketch / wireframe / prototype / final) | Decision it informs | Due | Reviewers (roles) |
|---|---|---|---|---|
| [ui-state-inventory.md](ui-state-inventory.md) copy | n/a, a state list | Which states exist before any screen is designed against them | | |
| | | | | |

## 7. Review dates

<!-- Critique is a scheduled event, not a hallway. Two reviews minimum: problem and
     direction first, solution second. Input needed by is the date after which the
     review proceeds without it. -->

| Review | Date | Attendees (roles) | Decision expected | Input needed by |
|---|---|---|---|---|
| Problem and direction | | | | |
| Critique, run per [design-critique.md](../../frameworks/design/design-critique.md) | | | Improves the work; grants no approval | |
| Solution | | | | |
| Handoff to engineering | | | | |

## 8. Open questions

| Question | Owner | Needed by | Blocks (section or deliverable) |
|---|---|---|---|
| | | | |

---

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The agreed brief travels with the [PRD](prd.md) to [Gate 2](../../os/STAGE-GATES.md), and its deliverables become the design inputs to the DESIGN stage.

- [ ] The problem is stated without a solution, and any solution guess is labeled as one
- [ ] The primary user has a job, a workaround, and evidence; "all users" appears nowhere
- [ ] Every constraint is labeled hard or soft with a source
- [ ] Success metrics reference the PRD, and a pre-launch test is named with a date
- [ ] Out of scope is written with reasons
- [ ] Every deliverable names the decision it informs, a due date, and reviewers
- [ ] Review dates are on calendars, with attendees confirmed
- [ ] The accessibility row names the level and where its evidence will live
- [ ] Signed by the product owner and the design lead, [names], [date]
