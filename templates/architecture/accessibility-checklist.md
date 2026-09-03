---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Accessibility Checklist", "accessibility-checklist"]
---
# Accessibility Checklist: [product or feature name]

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); the evidence column is completed in BUILD and checked at Gate 4
Knowledge: [Knowledge index](../../knowledge/INDEX.md); the standard itself is [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
Skill: [acceptance-agent](../../agents/acceptance-agent.md)

> **Delete any section you do not need.** Delete the component tables for components the feature does not contain, and say so; keep every table for a component it does. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- The conformance level the product commits to is set once, in
     ../definition/nfr.md section 5, and this checklist inherits it; do not pick
     a different level here. Design intent lives in ../definition/design-brief.md;
     test levels and who runs them in ../delivery/testing-strategy.md. This file
     is the walk: component by component, against the WCAG guideline families,
     with evidence a skeptic could open. Families are cited by guideline number
     (1.1, 2.4, 3.3 and so on) because they are stable across WCAG versions;
     look up the exact success criteria for your level at the link above. A
     checked box with an empty evidence cell is a claim, not a check. Fill
     section 1 and the component inventory first; then walk one table at a time
     with a keyboard, a screen reader, and the contrast tool named in section 1. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Scope and tools

| Field | Value |
|---|---|
| Conformance target | [version and level, copied from nfr.md section 5] |
| Surfaces in scope | [web, native, email, PDF output] |
| Assistive technology tested with | [screen reader and browser pairs, magnifier, switch, voice control] |
| Automated checker | [tool, version; it finds a share of issues, never all of them] |
| Contrast tool | [tool] |
| Who walks the checklist | [name; not the author of the component] |

## 2. Component inventory

| Component type | Instances in this feature (screens or ids) | Table |
|---|---|---|
| Forms and inputs | | 3 |
| Controls: buttons, links, menus | | 4 |
| Page structure and navigation | | 5 |
| Images, icons, charts | | 6 |
| Tables and data grids | | 7 |
| Dialogs, overlays, toasts | | 8 |
| Media and motion | | 9 |

## 3. Forms and inputs

<!-- Families: 1.3 Adaptable, 2.4 Navigable, 3.3 Input Assistance, 4.1
     Compatible. Evidence is a screen reader recording, a checker report, or a
     dated test note; "looks fine" is not evidence. Result is pass, fail, or
     "N/A because". -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Every input has a visible label programmatically associated with it | 1.3, 3.3 | screen reader announces the label with the field | | | |
| Required fields and formats are stated before an error occurs | 3.3 | read the form without submitting | | | |
| Errors are identified in text, next to the field, and announced | 3.3, 4.1 | submit an invalid form with a screen reader running | | | |
| Submissions with legal or financial effect can be reviewed or reversed | 3.3 | walk the submit path | | | |
| Input purpose is exposed where a field collects personal data | 1.3 | inspect the field attributes | | | |
| Information entered earlier in the flow is not demanded again | 3.3 | walk a multi-step flow | | | |

## 4. Controls: buttons, links, menus

<!-- Families: 2.1 Keyboard Accessible, 2.4 Navigable, 2.5 Input Modalities,
     4.1 Compatible. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Every control is reachable and operable by keyboard alone, with no trap | 2.1 | tab through the whole flow; escape from every widget | | | |
| Focus is visible and not hidden behind sticky elements | 2.4 | tab with a sticky header or footer present | | | |
| Focus order follows the reading order | 2.4 | tab and compare with the visual order | | | |
| The accessible name contains the visible label | 2.5, 4.1 | inspect the name; try voice control by label | | | |
| Link text makes sense out of context | 2.4 | list all links with a screen reader | | | |
| Targets meet the size minimum for the level, and dragging has a non-drag alternative | 2.5 | measure; operate with a pointer only | | | |
| Name, role, and state are exposed for custom controls | 4.1 | inspect the accessibility tree | | | |

## 5. Page structure and navigation

<!-- Families: 1.3 Adaptable, 1.4 Distinguishable, 2.4 Navigable, 3.1 Readable,
     3.2 Predictable. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Headings form an outline; landmarks mark regions | 1.3, 2.4 | headings and landmarks list in a screen reader | | | |
| The page title states the page and the product | 2.4 | read the title | | | |
| A skip mechanism bypasses repeated blocks | 2.4 | first tab stop | | | |
| Language of the page, and of any foreign passages, is set | 3.1 | inspect attributes | | | |
| Navigation and help sit in consistent places across screens | 3.2 | compare screens | | | |
| Content reflows at high zoom without horizontal scrolling or loss | 1.4 | zoom to the level's reflow point | | | |
| Nothing changes context on focus or on input alone | 3.2 | tab and type through selects and fields | | | |

## 6. Images, icons, charts

<!-- Families: 1.1 Text Alternatives, 1.4 Distinguishable. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Informative images have text alternatives that carry the meaning; decorative ones are hidden | 1.1 | screen reader pass | | | |
| Charts have a text or table equivalent of the data | 1.1 | find the equivalent without the chart | | | |
| Color is never the only carrier of meaning | 1.4 | view in grayscale | | | |
| Text and essential non-text contrast meet the ratio for the level | 1.4 | contrast tool on every state | | | |
| No images of text where real text would do | 1.4 | inspect | | | |

## 7. Tables and data grids

<!-- Families: 1.3 Adaptable, 2.1 Keyboard Accessible, 4.1 Compatible. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Header cells are marked and associated with data cells | 1.3 | navigate cells with a screen reader | | | |
| Sort and filter controls are keyboard operable and announce their state | 2.1, 4.1 | operate by keyboard | | | |
| Grids keep their meaning when linearized | 1.3 | read with styles off | | | |

## 8. Dialogs, overlays, toasts

<!-- Families: 1.4 Distinguishable, 2.1 Keyboard Accessible, 2.4 Navigable,
     4.1 Compatible. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Focus moves into the dialog on open and returns on close | 2.4 | keyboard walk | | | |
| The background is inert while the dialog is open | 2.1 | try to tab out | | | |
| Status messages are announced without stealing focus | 4.1 | trigger a toast with a screen reader running | | | |
| Content shown on hover or focus can be dismissed and does not obscure the trigger | 1.4 | hover, then press escape | | | |

## 9. Media and motion

<!-- Families: 1.2 Time-based Media, 2.2 Enough Time, 2.3 Seizures and Physical
     Reactions. -->

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Video has captions; audio has a transcript; audio description is present where the level requires it | 1.2 | play with sound off | | | |
| Moving, blinking, or auto-updating content can be paused, stopped, or hidden | 2.2 | find the control | | | |
| Nothing flashes above the threshold the standard sets | 2.3 | inspect animations | | | |
| Time limits can be extended or turned off | 2.2 | trigger the timeout | | | |

## 10. Findings routed onward

| Finding | Check | Severity | Routed to (backlog item, risk register row) | Owner | Fix by |
|---|---|---|---|---|---|
| | | | | | |

## Exit gate (feeds Gate 3: architecture and risks reviewed)

Filled tables are the audit artifact [nfr.md](../definition/nfr.md) section 5 names; open failures become rows in [risk-register.md](../execution/risk-register.md), and the evidence column is what the acceptance agent verifies at [Gate 4](../../os/STAGE-GATES.md).

- [ ] The conformance target is copied from the NFR, not chosen here
- [ ] Every component type in the inventory has its table walked, or is deleted with a reason
- [ ] Every row has a result, and every pass has evidence a reviewer could open
- [ ] Every fail has a row in section 10 with an owner and a date
- [ ] The walk used a keyboard, a screen reader, and a contrast tool, named in section 1
- [ ] The walker is not the author of the component
- [ ] Signed by [name], [date]
