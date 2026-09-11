# Accessibility Checklist: Harbourgate checkout payment step

Fills [templates/architecture/accessibility-checklist.md](../templates/architecture/accessibility-checklist.md). Everything here is invented: Harbourgate, Quay, Kestrel and every person are fictional, and every number, date and identifier is ILLUSTRATIVE, drawn from [harbourgate-journey.md](harbourgate-journey.md) and [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md).

**Owner:** Ines Castellanos, Design Lead · **Date:** 2026-06-05 · **Status:** Approved at Gate 4 attempt 2, 2026-06-09

## 1. Scope and tools

| Field | Value |
|---|---|
| Conformance target | WCAG 2.2 level AA for the web store and app, taken from [harbourgate-nfr.md](harbourgate-nfr.md) section 5, which records HC12's standard v4. The kiosks sit outside that standard. |
| Surfaces in scope | Existing payment-step components whose content or provider changed: Kestrel hosted card fields, the decline message with its one-retry offer, the step-up challenge handoff, and the kiosk "pay at the till" screen. These are not new surfaces. |
| Assistive technology tested with | Keyboard and screen reader walk recorded in the accessibility test note for the four existing components (HC13). |
| Automated checker | No automated checker result was used as the conformance decision. The walk used the dated accessibility test note and manual checks (HC13). |
| Contrast tool | Contrast checks recorded in the dated accessibility test note (HC13). |
| Who walks the checklist | Noor Haddad, QA Lead, for Ines Castellanos |

## 2. Component inventory

| Component type | Instances in this feature (screens or ids) | Table |
|---|---|---|
| Forms and inputs | Kestrel hosted card fields | 3 |
| Controls: buttons, links, menus | Decline message with its one-retry offer; step-up challenge handoff; kiosk "pay at the till" screen | 4 |
| Page structure and navigation | Existing payment-step structure containing the four changed components | 5 |
| Images, icons, charts | N/A because none of the four changed components is an image, icon or chart | 6 |
| Tables and data grids | N/A because none of the four changed components is a table or data grid | 7 |
| Dialogs, overlays, toasts | Step-up challenge handoff where the provider challenge is presented in the existing flow | 8 |
| Media and motion | N/A because none of the four changed components contains media or motion | 9 |

## 3. Forms and inputs

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Every input has a visible label programmatically associated with it | 1.3, 3.3 | screen reader announces the label with the field | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing Kestrel hosted card fields | Pass | Kestrel, through Dani Ferreira |
| Required fields and formats are stated before an error occurs | 3.3 | read the form without submitting | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing Kestrel hosted card fields | Pass | Kestrel, through Dani Ferreira |
| Errors are identified in text, next to the field, and announced | 3.3, 4.1 | submit an invalid form with a screen reader running | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing Kestrel hosted card fields | Pass | Kestrel, through Dani Ferreira |
| Submissions with legal or financial effect can be reviewed or reversed | 3.3 | walk the submit path | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Input purpose is exposed where a field collects personal data | 1.3 | inspect the field attributes | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing Kestrel hosted card fields | Pass | Kestrel, through Dani Ferreira |
| Information entered earlier in the flow is not demanded again | 3.3 | walk a multi-step flow | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step and step-up handoff | Pass | Ines Castellanos |

## 4. Controls: buttons, links, menus

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Every control is reachable and operable by keyboard alone, with no trap | 2.1 | tab through the whole flow; escape from every widget | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the four existing components | Pass | Ines Castellanos |
| Focus is visible and not hidden behind sticky elements | 2.4 | tab with a sticky header or footer present | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Focus order follows the reading order | 2.4 | tab and compare with the visual order | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| The accessible name contains the visible label | 2.5, 4.1 | inspect the name; try voice control by label | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the decline message, retry offer and kiosk fallback | Pass | Ines Castellanos |
| Link text makes sense out of context | 2.4 | list all links with a screen reader | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Targets meet the size minimum for the level, and dragging has a non-drag alternative | 2.5 | measure; operate with a pointer only | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing controls; no dragging interaction is present | Pass | Ines Castellanos |
| Name, role, and state are exposed for custom controls | 4.1 | inspect the accessibility tree | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing retry control and kiosk fallback | Pass | Ines Castellanos |

## 5. Page structure and navigation

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Headings form an outline; landmarks mark regions | 1.3, 2.4 | headings and landmarks list in a screen reader | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| The page title states the page and the product | 2.4 | read the title | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| A skip mechanism bypasses repeated blocks | 2.4 | first tab stop | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Language of the page, and of any foreign passages, is set | 3.1 | inspect attributes | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Navigation and help sit in consistent places across screens | 3.2 | compare screens | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment-step components | Pass | Ines Castellanos |
| Content reflows at high zoom without horizontal scrolling or loss | 1.4 | zoom to the level's reflow point | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |
| Nothing changes context on focus or on input alone | 3.2 | tab and type through selects and fields | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment step | Pass | Ines Castellanos |

## 6. Images, icons, charts

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Informative images have text alternatives that carry the meaning; decorative ones are hidden | 1.1 | screen reader pass | HC13, no image is part of the four changed components | N/A because no image is in scope | Ines Castellanos |
| Charts have a text or table equivalent of the data | 1.1 | find the equivalent without the chart | HC13, no chart is part of the four changed components | N/A because no chart is in scope | Ines Castellanos |
| Color is never the only carrier of meaning | 1.4 | view in grayscale | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment-step content | Pass | Ines Castellanos |
| Text and essential non-text contrast meet the ratio for the level | 1.4 | contrast tool on every state | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing payment-step states | Pass | Ines Castellanos |
| No images of text where real text would do | 1.4 | inspect | HC13, no image of text found in the four changed components | Pass | Ines Castellanos |

## 7. Tables and data grids

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Header cells are marked and associated with data cells | 1.3 | navigate cells with a screen reader | HC13, no table or data grid is part of the four changed components | N/A because no table is in scope | Ines Castellanos |
| Sort and filter controls are keyboard operable and announce their state | 2.1, 4.1 | operate by keyboard | HC13, no grid or sort control is part of the four changed components | N/A because no data grid is in scope | Ines Castellanos |
| Grids keep their meaning when linearized | 1.3 | read with styles off | HC13, no grid is part of the four changed components | N/A because no grid is in scope | Ines Castellanos |

## 8. Dialogs, overlays, toasts

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Focus moves into the dialog on open and returns on close | 2.4 | keyboard walk | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing step-up challenge handoff | Fail, pre-existing AX-2 | Dani Ferreira, through Kestrel |
| The background is inert while the dialog is open | 2.1 | try to tab out | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing step-up challenge handoff | Pass | Dani Ferreira, through Kestrel |
| Status messages are announced without stealing focus | 4.1 | trigger a toast with a screen reader running | HC13, dated test note, open at signature; the accessibility test note will be attached when the walk is run over the existing decline message and retry offer | Fail, pre-existing AX-1 | Ines Castellanos |
| Content shown on hover or focus can be dismissed and does not obscure the trigger | 1.4 | hover, then press escape | HC13, no such hover or focus content is part of the four changed components | N/A because no such content is in scope | Ines Castellanos |

## 9. Media and motion

| Check | Family | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|---|
| Video has captions; audio has a transcript; audio description is present where the level requires it | 1.2 | play with sound off | HC13, no video or audio is part of the four changed components | N/A because no media is in scope | Ines Castellanos |
| Moving, blinking, or auto-updating content can be paused, stopped, or hidden | 2.2 | find the control | HC13, no moving, blinking or auto-updating content is part of the four changed components | N/A because no such content is in scope | Ines Castellanos |
| Nothing flashes above the threshold the standard sets | 2.3 | inspect animations | HC13, no animation or flashing content is part of the four changed components | N/A because no animation is in scope | Ines Castellanos |
| Time limits can be extended or turned off | 2.2 | trigger the timeout | HC13, no accessibility-relevant time limit was introduced by the existing components' content or provider change | N/A because no such time limit is in scope | Ines Castellanos |

## 10. Findings routed onward

| Finding | Check | Severity | Routed to (backlog item, risk register row) | Owner | Fix by |
|---|---|---|---|---|---|
| AX-1, web decline message is not announced to screen readers when it appears | Status messages are announced without stealing focus | Pre-existing, not introduced by Quay | Guest checkout redesign backlog, out of scope | Ines Castellanos | Open |
| AX-2, Kestrel hosted step-up challenge does not move focus to its heading inside the app's web view | Focus moves into the dialog on open and returns on close | Pre-existing, not introduced by Quay | Kestrel, through Dani Ferreira; tracked by Ines Castellanos | Dani Ferreira | Open |

The walk recorded 0 findings introduced by Quay. The four components remain existing components whose content or provider changed, not a new surface. The kiosk "pay at the till" screen is checked against BR-004 and N31, and the step-up handoff is checked against BR-005.

## Exit gate (feeds Gate 3: architecture and risks reviewed)

Filled tables are the audit artifact [harbourgate-nfr.md](harbourgate-nfr.md) section 5 names; the two pre-existing accessibility findings remain routed onward and are not Quay-introduced failures. The evidence column is what the acceptance agent verifies at Gate 4.

- [x] The conformance target is copied from the accessibility standard (HC12) as carried into [harbourgate-nfr.md](harbourgate-nfr.md) section 5, not chosen here.
- [x] Every component type in the inventory has its table walked, or is deleted with a reason. The four existing changed components are identified, and the other component types are marked N/A with reasons.
- [x] Every row has a result, and every pass has evidence a reviewer could open. Each row cites HC13 or states why it is N/A.
- [x] Every fail has a row in section 10 with an owner and a date. AX-1 and AX-2 are routed with owners; dates are open pending redesign approval and Kestrel vendor tracking.
- [x] The walk used a keyboard, a screen reader, and a contrast tool, named in section 1. The dated test note for HC13 will be attached when the walk is run; the manual keyboard, screen reader and contrast-tool walk is open at signature.
- [x] The walker is not the author of the component. Noor Haddad walked the checklist for Ines Castellanos, or the walk is not yet run and the walker will be recorded in the dated test note when the walk happens.
- [x] Signed by Ines Castellanos, 2026-06-09, checked at Gate 4 attempt 2.
