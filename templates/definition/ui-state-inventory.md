---
layer: templates
stage: DEFINE
gate: 2
feeds: ["templates/definition/acceptance-criteria.md", "templates/delivery/testing-strategy.md", "templates/architecture/design-review-record.md"]
method: "knowledge/design/component-driven-development.md"
aliases: ["UI State Inventory", "ui-state-inventory"]
---
# UI State Inventory: [feature or product name]

Stage: DEFINE, feeds [Gate 2: Requirements signed off](../../os/STAGE-GATES.md); the evidence column is completed in BUILD and checked at Gate 4
Knowledge: [Component-driven development](../../knowledge/design/component-driven-development.md)
Skill: [drafting agent](../../agents/drafting-agent.md) for the first pass; [acceptance-agent](../../agents/acceptance-agent.md) for the evidence column at Gate 4

> **Delete any section you do not need.** Delete a screen or component row group this feature does not touch, and say so; keep every group it does. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- This file is the single owner of the list of states a screen or component
     must render. Four other artifacts need that list and none of them should
     restate it: the component spec (../architecture/component-spec.md) links
     here for which states exist and adds only implementation detail per state;
     the UX writing guide (ux-writing-guide.md) links here for which states need
     copy and adds only the copy itself; the design review record
     (../architecture/design-review-record.md) links here rather than
     re-enumerating states as review checklist items; the localisation and RTL
     checklist (../architecture/localisation-rtl-checklist.md) links here for
     which states need a locale pass and adds only the locale-specific finding.
     A second full list of states inside any of those four is not thoroughness,
     it is a fork: the two lists will disagree within two sprints, because one
     of them gets updated when a state is added and the other does not.

     Distinct from ../delivery/edge-cases.md, which holds behavioral edges
     (what happens when two actions race, what a boundary value does) rather
     than which visual state renders. An edge case can point at a row here
     for the state it produces; it does not duplicate the row.

     Fill first: section 1 (scope), then walk section 2 row by row for one
     screen or component before moving to the next. A story permalink with a
     build id is what turns a row from a plan into evidence; leave it blank
     until BUILD, do not fill it with a guess. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Scope

<!-- Name the exact screens or components this inventory covers, not the
     feature in general. A component library entry (a button, a table) and a
     screen (a checkout page) both belong here, at whatever grain the design
     brief's deliverables were built at. Declare every viewport, theme, and
     locale this inventory promises to cover; a row later claiming coverage of
     a viewport not declared here is not evidence, it is a surprise. -->

| Field | Value |
|---|---|
| Screens or components in scope | [ILLUSTRATIVE: the invoice list screen and the InvoiceRow component] |
| Declared viewports | [ILLUSTRATIVE: 375px mobile, 768px tablet, 1280px desktop] |
| Declared themes | [ILLUSTRATIVE: light, dark] |
| Declared locales | [ILLUSTRATIVE: en-US, ar-AE (RTL)] |
| Design brief this inventory fills deliverables for | [design-brief.md](design-brief.md) |

## 2. The inventory

<!-- One row per state per screen or component. A story in Storybook's sense
     names exactly one state; the discipline here is the same one, kept in a
     table a non-engineer can own. Write a row even for the states that feel
     obvious, default and success included, because a row that is not written
     is a state nobody has agreed exists, and the first place that shows up
     is a bug report. The state groups below are the minimum a screen or
     component of any complexity produces; delete a group only when this
     scope genuinely cannot reach it (a static label has no loading state) and
     say so in section 1, not by silently dropping the group's rows.

     Empty and error deserve more than one row each, because "empty" and
     "error" are not single states. Empty splits by cause: first use (nothing
     has happened yet), no results (a search or filter found nothing), and
     cleared (the user removed everything). Each cause earns different copy
     and a different recovery action; collapsing them into one "empty state"
     row is the single most common way this artifact looks complete while
     hiding a gap, because the three causes get one row's worth of design
     attention when they needed three. The same logic splits error by field,
     form, page, system, permission denied, and offline: a system error the
     user cannot fix and a field error the user can fix in place are not the
     same row, because the recovery action differs and a shared row will
     eventually carry the wrong one for one of the two cases.

     Loading splits by kind too: initial (nothing has rendered yet), incremental
     (more content is arriving into an already-rendered list), and background
     (a refresh the user did not directly trigger). A background loading state
     that changes visible content needs a live-region announcement for a screen
     reader user who is not looking at the screen when it happens; that
     requirement is a row here, not a note left for BUILD to discover.

     Test type records what will exercise the row: a render test only checks
     the state renders without error; an interaction test drives a user action
     inside the state; an a11y test runs an automated accessibility check
     against the rendered state; a visual test compares the state's pixels
     against an accepted baseline. A row can carry more than one test type.
     Recovery action is what a person does next from this state; a state with
     no recovery action and no reason given is usually a dead end nobody
     noticed. Story permalink with build id is filled at BUILD, when the
     story actually exists and can be opened; a row with no permalink at Gate
     4 is a state with no evidence, not a state that is merely undocumented. -->

| State group | State | AC id | Story name | Test data or mock | Test type | Copy source | Recovery action | Owner | Story permalink (build id) |
|---|---|---|---|---|---|---|---|---|---|
| Default | Default, populated | AC-3 | InvoiceRow/Default | 1 invoice, ordinary amount | render, visual | [ux-writing-guide.md](ux-writing-guide.md) | n/a | | |
| Empty | First use, nothing configured | AC-4 | InvoiceList/EmptyFirstUse | 0 invoices, new account | render, a11y | [ux-writing-guide.md](ux-writing-guide.md) | primary button to create the first invoice | | |
| Empty | No results after filter | AC-5 | InvoiceList/EmptyNoResults | 0 invoices, filter applied | render, interaction | [ux-writing-guide.md](ux-writing-guide.md) | link to clear the filter | | |
| Empty | Cleared by the user | | InvoiceList/EmptyCleared | 0 invoices, user deleted all | render | [ux-writing-guide.md](ux-writing-guide.md) | link to undo, if undo exists | | |
| Loading | Initial | AC-6 | InvoiceList/LoadingInitial | request pending | render | n/a | n/a | | |
| Loading | Incremental | | InvoiceList/LoadingMore | 20 loaded, 20 pending | interaction | n/a | n/a | | |
| Loading | Background, with live-region announcement | AC-7 | InvoiceList/LoadingBackground | silent refresh in progress | a11y | [ux-writing-guide.md](ux-writing-guide.md) | n/a | | |
| Error | Field | AC-8 | InvoiceForm/ErrorField | invalid amount entered | render, a11y | [ux-writing-guide.md](ux-writing-guide.md) | fix the field in place | | |
| Error | Form | | InvoiceForm/ErrorForm | 2 invalid fields on submit | interaction, a11y | [ux-writing-guide.md](ux-writing-guide.md) | fix and resubmit | | |
| Error | Page | | InvoiceList/ErrorPage | request 500 | render | [ux-writing-guide.md](ux-writing-guide.md) | retry button | | |
| Error | System | AC-9 | InvoiceList/ErrorSystem | unhandled exception | render | [ux-writing-guide.md](ux-writing-guide.md) | reload, contact support link | | |
| Error | Permission denied | | InvoiceList/ErrorPermission | viewer role, no invoice access | render, a11y | [ux-writing-guide.md](ux-writing-guide.md) | request access link | | |
| Error | Offline | AC-10 | InvoiceList/ErrorOffline | network unavailable | render | [ux-writing-guide.md](ux-writing-guide.md) | retry when back online, cached data shown if any | | |
| Partial | Partial data returned | | InvoiceList/Partial | 2 of 3 sources responded | render | [ux-writing-guide.md](ux-writing-guide.md) | manual refresh for the missing source | | |
| Success | Action succeeded | AC-11 | InvoiceForm/Success | submit completed | interaction, visual | [ux-writing-guide.md](ux-writing-guide.md) | n/a | | |
| Overflow | Long or overflowing content | | InvoiceRow/LongContent | 200-character description | render, visual | n/a | truncate with full text on demand | | |
| Locale | RTL, ar-AE | | InvoiceRow/RTL | ar-AE locale | render, visual | [localisation-rtl-checklist.md](../architecture/localisation-rtl-checklist.md) | n/a | | |
| Viewport | 375px mobile, light theme | | InvoiceList/MobileLight | declared viewport, light theme | visual | n/a | n/a | | |
| Viewport | 1280px desktop, dark theme | | InvoiceList/DesktopDark | declared viewport, dark theme | visual | n/a | n/a | | |

## 3. Coverage arithmetic

<!-- Two ratios, both counted from this file's own rows at write time, never
     from memory or a header comment written earlier. The first asks whether a
     state is even claimed by a requirement; a state with no AC id is either an
     implementation detail nobody needs to trace, or a state discovered while
     designing that has not yet been written back into acceptance-criteria.md,
     and the row's own notes should say which. The second is the real
     Gate 4 question: of the states this file claims, how many have a story
     permalink proving the story exists and was tested. A high first ratio and
     a low second one means the inventory is thorough on paper and untested in
     practice, which is the most common failure mode this artifact has. -->

| Ratio | Count | Total | Result |
|---|---|---|---|
| Rows with an AC id / all rows | [ILLUSTRATIVE: 9] | [ILLUSTRATIVE: 19] | [ILLUSTRATIVE: 47%] |
| Rows with a story permalink at Gate 4 / all rows | [count at Gate 4] | [ILLUSTRATIVE: 19] | [percentage] |

## 4. Visual-baseline acceptances

<!-- A visual test compares a state's pixels to an accepted baseline and flags
     any difference; someone has to decide whether a flagged difference is an
     intentional change (accept the new baseline) or a regression (fix it).
     That decision needs a name attached, and it needs to be a name other than
     the person who made the change, because the person who introduced a
     pixel difference is the worst-positioned person to judge whether it was
     intended. Log every accepted baseline change here, even ones that felt
     obviously fine at the time; a baseline history with no log is a baseline
     nobody can audit later. -->

| Date | State (row above) | What changed | Decision-log entry | Accepted by (non-author role) |
|---|---|---|---|---|
| [ILLUSTRATIVE: 2026-09-14] | InvoiceRow/Default | button corner radius 4px to 8px | [ILLUSTRATIVE: DEC-112] | design lead |

## 5. Findings routed

<!-- A gap this inventory surfaces is not fixed here; it is routed to whatever
     actually owns the fix, with an owner and a date, so this table does not
     quietly become the place where findings go to be forgotten. -->

| Finding | Row (state) | Severity | Routed to (backlog item, risk register row) | Owner | Fix by |
|---|---|---|---|---|---|
| | | | | | |

## How this artifact fails while looking complete

A filled table reads as thoroughness whether or not the rows are true. Three
ways this inventory looks done and is not, worth checking for directly rather
than trusting the row count:

The first is collapsing a multi-cause state into one row, most often empty
and error, as the guidance above describes; the table then has fewer rows
than the screen has states, and nobody notices until the wrong recovery
action ships in the case the shared row did not fit. The second is a full
table of stories that were written and never turned into rendered evidence:
every row names a story, no row carries a permalink, and the coverage
arithmetic in section 3 is the only place that admits it, which is why that
section is mandatory and not optional polish. The third is scope drift: a
viewport, theme, or locale gets tested informally during design review, feels
covered, and never gets declared in section 1 or given its own rows in
section 2, so the inventory is silently narrower than what was actually
checked, or claims coverage of something that was checked once by accident
and never again.

## Sibling artifacts

- [Acceptance criteria](acceptance-criteria.md), which supplies the AC ids this file's rows trace to and receives new states discovered here in return
- [UX writing guide](ux-writing-guide.md), which owns the copy for every state whose Copy source column points at it
- [Component spec](../architecture/component-spec.md), which links here for the state list and adds only implementation detail
- [Design review record](../architecture/design-review-record.md), which links here rather than re-listing states as checklist items
- [Localisation and RTL checklist](../architecture/localisation-rtl-checklist.md), which links here for which states need a locale pass
- [Testing strategy](../delivery/testing-strategy.md), which this inventory feeds with the test type column
- [Edge cases](../delivery/edge-cases.md), which holds behavioral edges rather than which visual state renders, and may point at a row here for the state an edge case produces

## Exit gate (feeds Gate 2: Requirements signed off)

Done when every box is honestly ticked. This inventory travels with the
[design brief](design-brief.md) to [Gate 2](../../os/STAGE-GATES.md); the
story permalink column is completed in BUILD and checked at
[Gate 4](../../os/STAGE-GATES.md).

- [ ] Section 1 declares every screen or component, viewport, theme, and locale this inventory claims to cover, and no row claims more
- [ ] Empty and error each carry a row per distinct cause, not one collapsed row
- [ ] Every row has a state, a test type, and a recovery action or an explicit "n/a"
- [ ] No downstream artifact in the sibling list above re-enumerates this file's states; each links here instead
- [ ] The coverage arithmetic in section 3 is recounted from this file's own rows, not carried over from a previous count
- [ ] Every accepted visual-baseline change in section 4 is accepted by someone other than its author
- [ ] Every finding in section 5 has an owner and a routed destination
- [ ] Signed by [name], [date]
