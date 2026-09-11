---
layer: templates
stage: DESIGN
gate: 3
feeds: ["templates/execution/decision-log.md", "templates/execution/risk-register.md", "templates/execution/tech-debt-register.md"]
method: "knowledge/design/pm-design-collaboration.md"
aliases: ["Design Review Record", "design-review-record", "Design QA Sign-off"]
---
# Design Review Record: [feature or product name]

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); the live-build section is completed in BUILD and checked at Gate 4
Listed as a Gate 3 and Gate 4 input in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); not yet a checklist line of its own there (held for the owner)
Knowledge: [PM and design collaboration](../../knowledge/design/pm-design-collaboration.md)
Skill: [design-review](../../skills/design-review/SKILL.md)

> **Delete any section you do not need.** A one-screen change still fills sections 1, 3 and 6; the rest apply only as far as the product's own scope reaches. Never leave a heading standing over white space, and never delete section 7: a Gate 3 approval with no Gate 4 walk is a promise nobody checked.

<!-- One file, two gates. NN/g treats a design critique and a design review as
     two distinct meetings: a critique gathers feedback against agreed
     objectives, a review evaluates a design and can end in a go decision
     (Gibbons, 2016). This file is the review half, and the only place in this
     repository that decision gets signed. It runs twice against the same
     artifact: once at Gate 3, on the evidence a static or clickable design
     can produce, and once at Gate 4, on the release candidate a static
     review cannot see. Sections 1 to 6 and 8 to 9's Gate 3 row are filled
     once, at Gate 3, and are not reopened when the build starts. Section 7
     and the Gate 4 row of section 9 stay blank until BUILD, then get walked
     against the running candidate, following the accessibility checklist's
     own split between a design-time table and a build-time evidence column.
     A design critique's outcome log (frameworks/design/design-critique.md)
     is evidence this record can cite; it is never a substitute for the
     decision in section 6, because a critique produces feedback and this
     file produces a go. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. What was reviewed

<!-- Name the artifact precisely enough that a later reader can tell whether
     they are looking at the thing this record approved. Paste the
     objectives from the design brief section 4 verbatim, the way
     frameworks/design/design-critique.md section 1 does; an objective
     re-derived from memory in the room is not the objective that was
     agreed. -->

| Field | Value |
|---|---|
| Artifact reviewed | [prototype, build, or live feature; link] |
| Fidelity and version id | [paper / clickable / coded; version id, so a finding is attributable to a specific state of the design] |
| Screens or flows in scope | [list] |
| Objectives, pasted from [design brief](../../templates/definition/design-brief.md) section 4 | [verbatim, not paraphrased] |
| Design questions this review must answer | [two or three] |

## 2. Evidence on the table

<!-- Every evidence type below is either linked to a run instance or marked
     "not run because <reason>"; a blank cell is a gap nobody named. A
     heuristic evaluation and a usability test answer different questions
     (see frameworks/design/heuristic-evaluation.md "The trap"): an
     inspection method shows where a screen predictably breaks a general
     principle, never whether real users complete a real task, and section 3
     carries that distinction forward as an evidence-class column rather
     than collapsing it here. -->

| Evidence type | Run | Link, or "not run because <reason>" | Date |
|---|---|---|---|
| Heuristic evaluation, general pass | | [frameworks/design/heuristic-evaluation.md](../../frameworks/design/heuristic-evaluation.md) section 3-4, or reason | |
| Heuristic evaluation, task-based variant (cognitive walkthrough) | | [frameworks/design/heuristic-evaluation.md](../../frameworks/design/heuristic-evaluation.md) section 5, or reason | |
| Usability-test results | | [usability test plan](../../templates/discovery/usability-test-plan.md) section 7, or reason | |
| Content and microcopy audit | | [frameworks/design/content-microcopy-audit.md](../../frameworks/design/content-microcopy-audit.md), or reason | |
| Accessibility checklist, with its scope-and-sample block | | [accessibility checklist](../../templates/architecture/accessibility-checklist.md) section 1, or reason | |
| Localisation and RTL checklist | | [localisation and RTL checklist](../../templates/architecture/localisation-rtl-checklist.md), or reason | |
| Choice-symmetry audit | | `frameworks/design/choice-symmetry-audit.md` (vocabulary: [Deceptive Design](../../knowledge/design/deceptive-design.md)), only for a flow with a changed consent, cancellation, upgrade or downgrade path; otherwise "not applicable, no such path in scope" | |
| Design-system audit | | [frameworks/design/design-system-audit.md](../../frameworks/design/design-system-audit.md), or reason | |
| Component spec(s) | | [component-spec.md](component-spec.md) copies for every shared component this review touches, or "none, no shared component in scope" | |
| UI state inventory | | [ui-state-inventory.md](../definition/ui-state-inventory.md), or reason | |
| Product DESIGN.md | | `products/<name>/DESIGN.md`, or "none yet, first design review for this product" | |

## 3. Findings, consolidated

<!-- One row per distinct finding, deduplicated across every evidence type in
     section 2, not one row per method. Evidence class is "inspection"
     (heuristic evaluation, cognitive walkthrough, content audit,
     accessibility or localisation checklist read without a participant) or
     "user" (usability test, a participant's own session). Severity reuses
     the SAME 1 to 4 scale as usability-test-plan.md section 6 (4 blocker, 3
     major, 2 minor, 1 cosmetic), so an inspection finding and a user finding
     sit on one severity axis. An inspection-only review cannot close a
     severity 3 or 4 finding: a single evaluator finds 20 to 51 percent of
     the usability problems actually present (Nielsen and Molich, 1990,
     cited in frameworks/design/heuristic-evaluation.md section 6), so a
     severity 3 or 4 row whose evidence class is inspection stays "open,
     routed to usability test" in the status column, never "closed," until a
     user session confirms the fix or the absence of the problem. -->

| Id | Finding | Source | Evidence class (inspection / user) | Severity (1 to 4) | Screen or element | Status |
|---|---|---|---|---|---|---|
| *F-1* | *"Pending Review" status label gives no next action (ILLUSTRATIVE)* | *heuristic evaluation, general pass* | *inspection* | *3* | *status banner* | *open, routed to usability test: inspection cannot close a severity 3 finding* |
| F-2 | | | | | | |

## 4. Design-system fit and deviations

<!-- Reused components are named with the version or token tier they came
     from, not just a component name; a token is cited by name and tier
     (for example color.text.critical, tier semantic), never by a raw value,
     the same rule section 5 applies to handoff. A deviation is deliberate
     when a person chose it and can say why: log it as a row in the
     [decision log](../../templates/execution/decision-log.md), not here,
     and reference the row id. A deviation nobody chose, a component built
     or styled outside the system without a decision behind it, is a bug:
     route it to the backlog and name the tracking id. -->

| Component or pattern | Version or token tier used | Deviation from the design system | Deliberate (decision log row id) or accidental (bug id) |
|---|---|---|---|
| | | | |

## 5. Handoff to engineering

<!-- Maudet, Leiva, Beaudouin-Lafon and Mackay (CSCW 2017, cited from the
     abstract only) name three ways a handoff breaks down: a detail omitted
     from the spec that the designer knew and never wrote down, an edge case
     ignored because the design only ever showed the happy path, and a
     technical limit disregarded because the design was never checked
     against what the platform can actually do. This section is those three
     checked as questions, plus the token and asset mechanics a design
     review record is the one place to confirm before BUILD starts. -->

- [ ] No detail omitted: every state a component can be in in this scope (empty, loading, error, success, and any product-specific state) has its own spec, not left to the engineer's inference
- [ ] No edge case ignored: the design was checked against inputs the happy path never shows (a name that does not fit, a zero, a very long value, a missing value), not only the sample data in the mock
- [ ] No technical limit disregarded: the design was checked against what the platform actually renders (real fonts, real network latency, real API response shapes), not assumed from the mock's static state
- [ ] Tokens are used by name and tier, never a raw value; an engineer inspecting the handoff sees token names, not hex codes or raw pixel values
- [ ] Variant matrix is complete for every combination this scope ships (size, state, and density, as applicable), with no cell left for the engineer to guess
- [ ] Open overrides (any place engineering must diverge from the system on this screen) are listed with an owner
- [ ] Assets and SVG exports are checked: correct format, correct scale set, optimized, and named to match the spec
- [ ] A change log has been kept since handoff, so a finding in section 3 raised after the spec was cut is traceable to what changed and when

## 6. Gate 3 decision

<!-- One decision, one paragraph, made once the evidence in sections 2
     through 5 is on the table. A condition is a specific, checkable change
     with an owner and a date, never "polish the details." Dissent is
     recorded rather than smoothed over: a reviewer who disagreed and was
     overruled is named, with their reason, so the decision's actual margin
     is visible to whoever reads this later. -->

**Decision:** APPROVE / APPROVE WITH CONDITIONS / RETURN, because: [one paragraph]

| Condition (if APPROVE WITH CONDITIONS) | Owner | Date due |
|---|---|---|
| | | |

**Dissent:** [name, reason, and whether it was noted or overruled; or "none recorded"]

## 7. Live-build review, completed in BUILD for Gate 4

<!-- Everything above this section can be answered from a design file.
     Nothing here can: a screenshot is not the evidence, the running release
     candidate is. Walk the release candidate itself, on real devices and
     real locales, the way accessibility-checklist.md's evidence column is
     filled at Gate 4, not the way section 1 to 6 were filled from a static
     artifact. The person who walks this section is not the person who
     implemented it, the same separation the accessibility checklist
     requires of its own walker. -->

| Field | Value |
|---|---|
| Release-candidate version | |
| Environment | [staging / production-mirrored / device farm] |
| Devices tested | |
| Locales tested | |
| Walker (not the implementer) | |

- [ ] The brief's primary task (section 1) was walked end to end on the release candidate itself, not narrated from a screenshot
- [ ] Every state listed in [ui-state-inventory.md](../definition/ui-state-inventory.md) was walked on the release candidate, not only the happy-path state; section 5's variant matrix is checked against the same list, never a second one
- [ ] Contrast was measured per state with the tool named in [accessibility checklist](../../templates/architecture/accessibility-checklist.md) section 1 (WCAG 1.4.3 and 1.4.11; evidence class: standard)
- [ ] Content reflows at 320 CSS px wide without two-dimensional scrolling (WCAG 2.2, 1.4.10 Reflow; evidence class: standard)
- [ ] Targets meet the size minimum for the level, cited by the named authority (WCAG 2.2, 2.5.8, or the platform convention actually followed, named)
- [ ] Motion was walked, and the reduced-motion state was walked as its own pass, not assumed to follow from the motion pass
- [ ] Colour scheme (light and dark) was walked, if in scope; "not in scope" is written here explicitly if it is not
- [ ] RTL was walked, including overlays and portal-rendered menus, dialogs and toasts, per [internationalisation and RTL](../../knowledge/design/internationalisation-and-rtl.md): a base-page pass tells you nothing about whether the overlay layer inherited direction
- [ ] The choice-symmetry result is attached, or this row reads "not applicable, no consent, cancellation, upgrade or downgrade path changed in this scope"
- [ ] The walker named above is not the implementer of what they walked

## 8. Routed onward

<!-- Every open item from sections 3, 4 and 7 lands exactly once here, with
     the register that owns it going forward. A tech-debt row names its
     Fowler quadrant (deliberate-prudent, deliberate-reckless,
     inadvertent-prudent or inadvertent-reckless, per
     frameworks/assessment/tech-debt-assessment.md step 2), because the
     quadrant, not the debt alone, decides what else has to change besides
     the code. -->

| Item | Routed to | Row id or reference | Debt type (if tech debt) | Owner | Date |
|---|---|---|---|---|---|
| | [risk register](../../templates/execution/risk-register.md) / [tech-debt register](../../templates/execution/tech-debt-register.md) / backlog / [decision log](../../templates/execution/decision-log.md) | | | | |

## 9. Sign-off

<!-- Two separate sign-off blocks for two separate events. The Gate 3 block
     closes DESIGN on the evidence in sections 1 to 6. The Gate 4 block
     closes the live-build walk in section 7, and is left blank until BUILD
     produces a release candidate to walk. -->

**Gate 3 sign-off**

| Sign-off | Name | Date |
|---|---|---|
| Design lead | | |
| Product owner | | |
| Engineering lead | | |

**Gate 4 sign-off (live build)**

| Sign-off | Name | Date |
|---|---|---|
| Walker (section 7) | | |
| Design owner, not the implementer | | |
| Product owner | | |
| QA | | |

## How this record fails while looking complete

Every box in section 2 ticked "run," and every linked evidence file is a heuristic pass, never a usability test: the record reads as thorough because every row has a link, and every one of those links is inspection, which the trap in [heuristic-evaluation.md](../../frameworks/design/heuristic-evaluation.md) names directly, trained judgment standing in for evidence that real people completed a real task. The second failure sits at the seam between the two gates: section 6 says APPROVE, section 7 stays blank because BUILD has not shipped a candidate yet, and the record gets filed as done. A Gate 3 approval is a decision about a design, not about a product; the file is not the one signed record this template promises until section 7 has been walked and section 9's Gate 4 block carries a walker's name distinct from whoever implemented the screen.

## Exit gate (feeds Gate 3: architecture and risks reviewed)

- [ ] Section 1's objectives are pasted verbatim from the design brief, not re-derived
- [ ] Every evidence type in section 2 is linked to a run instance or marked "not run because <reason>"
- [ ] Every finding in section 3 has an evidence class, and no severity 3 or 4 finding with evidence class "inspection" is marked closed
- [ ] Every deviation in section 4 is marked deliberate with a decision-log row id, or accidental with a bug id
- [ ] Every box in section 5 is checked, not assumed
- [ ] Section 6 names one decision, with every condition owned and dated, and dissent recorded or explicitly noted as none
- [ ] Section 8 has routed every open item from sections 3, 4 and 7 exactly once
- [ ] Signed by [name], [date]

### Gate 4 boxes (live build, checked at delivery)

- [ ] Section 7's release-candidate identification is filled, not left as the design-time placeholder
- [ ] Every box in section 7 is checked against the running candidate, not the design file
- [ ] The walker named in section 7 is not the implementer
- [ ] Signed by [name], [date] in section 9's Gate 4 block
