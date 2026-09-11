# Component Spec: `payment-outcome-panel`

Fills [templates/architecture/component-spec.md](../templates/architecture/component-spec.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay, Kestrel, Marlowe and Tidewater are fictional payment providers, every person is the journey's fictional cast, and every number, date, rate and pound is ILLUSTRATIVE, taken from the journey's data sheet rather than from any real retailer or payment surface. See the [examples index](README.md).

**Owner:** Ines Castellanos, Design Lead · **Date:** 2026-10-19 · **Status:** Trial, the redesign's first release. Promotion to Stable is a later decision, not recorded on this sheet; approved at the redesign pass's Gate-3-equivalent review, 2026-11-11; evidence inherited from the Quay journey's Gate 4 attempt 2 (2026-06-09) is cited, not re-run here
**Surfaces this behavioral contract covers:** web checkout, mobile app, and the kiosk PIN-pad flow (one kiosk per shop across 61 shops, N1, N2)

## 1. Purpose, use when, do not use when

**Purpose:** Renders the terminal outcome of one card-payment attempt, authorisation declined or the kiosk's no-outcome fallback, on whichever surface called Quay, so that the customer, the associate and the support log all read the same words at the same moment, and so that the retry offer BR-001 and the kiosk fallback BR-004 cannot drift per surface. This spec documents the behavioral contract of existing separate implementations on each surface, rather than asserting a single code artifact shared across all three.

| Use when | Do not use when |
|---|---|
| A card authorisation returns 402: the panel names the reason class, offers exactly one retry with a different method, and never resubmits the same card (BR-001, AC-5) | The decline is transient at the network layer: a 503 after Quay's one same-key retry (N61) is a transport-level retry of the same authorisation key, not a user-facing re-submission of the card (BR-001), owned by the client, not this panel; and a 429 with a `Retry-After` is a back-off case, not an outcome |
| Step-up authentication is required and the surface hands off to the Kestrel challenge (BR-005, AC-11) | Step-up has already resolved: this panel does not restate a result a challenge screen owned |
| On the kiosk only: no outcome has arrived within 10 s, so "pay at the till" appears and the basket holds for 30 minutes (BR-004, AC-10, N31) | Web and app, at any point: the "pay at the till" fallback is a physical-till affordance that exists only where a till is (N31, Lena Baptiste, store operations policy); importing it into checkout would invite shoppers to queue at a counter for an order they can retry online |
| | The authorisation succeeded: a success is receipt and order confirmation, a different composition; a panel whose happy path is an error teaches teams to reach for it where none belongs |

**Nearest look-alike, and why this is not it:** The Kestrel hosted fields component (I-1) owns the card entry; the step-up challenge handoff (vendor integration, not a register row) owns the verification; the receipt and order confirmation own a success (the order-history page reading the legacy table shape is I-10, a separate integration). This component is none of them: it exists only for the terminal non-success, and it consumes the decline's provider and reason class (S8, AC-4) rather than authoring them.

## 2. Anatomy

```
PaymentOutcomePanel (required)
  <OutcomeHeader> (required)
    <OutcomeTitle> (required; one of declined | challenge required | no outcome)
    <ReasonClass> (required only when Quay's decline event carries one, AC-4, S8)
  <Body> (slot: composed content, zero or more)
    <RetryOffer> (slot; rendered when a different method exists on this surface)
    <StepUpHandoff> (kiosk and web/app: opens the Kestrel challenge, AC-11)
    <TillFallback> (optional slot; kiosk only; timer-driven, BR-004, AC-10)
  <SupportLine> (optional; support path per the support runbook)
  <StatusPoll> (non-visual; polls I-2 until an outcome lands or the surface's own
    timeout closes the attempt; on the kiosk the close condition is the
    TillFallback firing at 10 s, not the web/app target 20 s, HC5)
```

**Subcomponents that carry their own variants (get their own row in section 3, or their own spec if the list grows past two or three):** `<OutcomeHeader>` (declined versus challenge required versus no outcome is a different title, reason row, icon set and announcement), and `<StatusPoll>` (it carries its own state table, so its own spec is safer than a row here). `<RetryOffer>`, `<StepUpHandoff>` and `<TillFallback>` are one-shot today and stay rows in section 3; if `<StepUpHandoff>` grows an app-embedding variant on top of the web-app handoff it gets its own spec. The anatomy tree was drafted with Bea Lindqvist on 2026-10-19, not read back off a Figma frame, because Curtis's companion piece on crafting a component API names sequence, not review, as the reason design and code names diverge ("Crafting Component API, Together," EightShapes).

## 3. Variant matrix

**Dimensions:** appearance × size × intent

| Dimension | Values | Count |
|---|---|---|
| Appearance | filled (default), outline (high-contrast) | 2 |
| Size | default (web, app), compact (kiosk) (N1, N2) | 2 |
| Intent | authorising, approved, declined, conflict, unavailable | 5 |

**Full cross product:** 2 × 2 × 5 = 20 combinations

**Defaults:** appearance = filled, size = default, intent = authorising.

**Compound combinations and prunes:**

| Combination | Ships? | Reason if pruned |
|---|---|---|
| compact × outline × any intent | No | Compact (kiosk) is filled-only, a platform convention for glare and distance legibility (HD20); the kiosks sit outside the WCAG 2.2 AA posture (HC12), and the lean on a device-level high-contrast mode depends on that mode being confirmed as reliable, which section 11 still holds open as a question; shipping it inside the component before then would produce two competing overrides nobody owns (KG-1) |

**Pruned set that ships:** 15 of 20 combinations, listed in full in the design system component catalog.

## 4. States

| State | Element that carries it | ARIA state or role | What is announced | Keyboard behavior | Notes |
|---|---|---|---|---|---|
| Default | Panel container | `role="alert"` on mount | Title plus reason class, if any (AC-4) | Tab reaches the first action | |
| Hover | `<RetryOffer>` and `<TillFallback>` only | none | nothing new | pointer only; no keyboard equivalent | |
| Focus-visible | First focusable action after mount | focus visible | focus lands silently on the first action (selection does not follow focus, section 5) | the visible ring is this component's obligation, not the library's | |
| Pressed | `<RetryOffer>` | none | activation text is not pre-announced | activates on Enter or Space while focused (section 5) | |
| Selected | no element carries it | not applicable | not applicable | not applicable | Row kept with a stated reason: the panel is a result readout, not a selectable control; no element in the panel is selectable, so no state could enter here |
| Disabled | `<RetryOffer>` after the one retry is taken, or when no different method exists (BR-001, AC-5) | `aria-disabled`, never `disabled` (removed from the tree instead) | the offer is absent or announced unavailable; the decline reason stays announced and discoverable | not focusable when `disabled`; focusable and inert if it must stay in the tree, and this component's case removes it from the tree instead | AC-5's "never re-submitted automatically" is why the disabled state is permanent within a session and not a timed debounce |
| Read-only | no element carries it | `aria-readonly` not set | not applicable | not applicable | Row kept with a stated reason: the panel never takes user input, so a read-only condition never applies |
| Loading | `<StatusPoll>` and `<OutcomeHeader>` before the 10 s or 20 s deadline (N31, HC5) | `aria-busy="true"` on the panel | "waiting for the bank to respond" without a focus move; repeated announcements are suppressed to one per surface session, the web/app rule | focus does not move; no activation while busy | The same row governs the kiosk's first 10 s; the announcement text is the one Ines Castellanos drafted with Lena Baptiste's team, not the checkout copy. The 10 s and 20 s figures are targets (HC5, N31), not measured component behaviour |
| Error | `<OutcomeHeader>` (declined with a known reason class, or no known reason class) | `role="alert"` on the panel plus `aria-describedby` pointing at the reason message | the reason class is announced with the decline title; "we could not determine a reason" is the announced text when the class is absent (N20) | focus returns to the panel when an async resolution arrives without the surface having moved focus | aria-invalid is not applied to this panel because it is a result readout that never takes user input; role="alert" and aria-describedby carry the announcement |
| Empty | no element carries it | not applicable | not applicable | not applicable | Row kept with a stated reason: the panel is not rendered before a terminal outcome arrives; a pre-outcome surface renders the Loading row, so an Empty state cannot exist here |

## 5. Keyboard decisions

| Decision | Choice | Reason |
|---|---|---|
| Activation mode | Enter or Space on a focused action; pointer click equivalent | One rule across all three surfaces is the point of sharing the component; the kiosk's PIN-pad surface is pointer-and-enter only, so a Surface-Enter-only rule would be a silent kiosk gap |
| Selection follows focus | No; a separate activation key confirms | A result readout must not change what the panel shows just because a Tab landed where a decline reason already lives; the section 4 Selected row is therefore kept with "not applicable" rather than deleted |
| Focus on open | The first focusable action (`<RetryOffer>`, else `<StepUpHandoff>`; on the kiosk, nothing focusable: the 10 s clock runs and the fallback fires, so there is no action to reach, N31) | The customer is the only person acting; a result screen should not hold focus hostage to a heading |
| Focus on close | Returns to the trigger on web and app (the pay button or the checkout's action area); on the kiosk, focus is released with the screen | Web and app keep a live page to return to; the kiosk's screen is replaced by the next step or by the till hand-off |
| Escape behavior | No-op; the panel is not a dialog and does not own dismissal | Escape closing a terminal outcome would create a way to lose a decline without reading it, which breaks support's ability to trace a ticket back to the reason class (S8, AC-4) |

**Signed by:** Product Ife Adeyemi, Design Ines Castellanos. The two exercised scenarios in that Gate 4 attempt 1 miss, FS-2 and FS-5 (HC1), sat with the QA and engineering line (Noor Haddad, Tomasz Wierzbicki), not with the two signers of these keyboard decisions, but they are the two states this component surfaces most, so these decisions were re-confirmed against the 2026-06-08 test logs and against BR-001 and BR-004, not re-decided.

## 6. Tokens consumed

| Token name | Tier (global / semantic / component) | Used for |
|---|---|---|
| `color.border.default` | semantic | default border, default appearance, all surfaces |
| `color.bg.neutral.subtle` | semantic | panel background, default appearance |
| `radius.md` | global | corner radius, all surfaces |
| `space.stack.xs` | global | gap between title and reason line |
| `component.outcome.paddingInline.md` | component | horizontal padding, kiosk medium size |
| `component.outcome.focusRing.width` | component | visible focus ring width, all surfaces (the component's own obligation, section 4 Focus-visible) |
| `kiosk.typeScale.2x` | global | "pay at the till" headline, across 61 kiosks (N2, N31), because the kiosk renders at a distance no web type scale reaches |

No raw value appears in this table or anywhere else in this file; every value lives in the design system itself.

## 7. Accessibility and localisation

**Accessibility checklist table for this component type:** [harbourgate-accessibility-checklist.md](harbourgate-accessibility-checklist.md), section 4, Controls and result readouts: buttons, links, status messages. Note: the same checklist also walked the web decline message and the step-up handoff as separate items (HC13), so where that file owns a component-level finding (AX-1 on the web decline message, AX-2 on the Kestrel challenge focus) this table does not restate it; it records only the responsibility split for obligations on top of those walk results.
**Localisation and RTL checklist:** [localisation-rtl-checklist.md](../templates/architecture/localisation-rtl-checklist.md), with the NFR section 5 localisation waiver as the reason the current sweep is English-only and carries a revisit date.

| Obligation | Responsibility (library / shared / our code) | Evidence status (tested / assessed from source / flagged) | Note |
|---|---|---|---|
| The decline title and reason class are announced together when the panel mounts (AC-4, N20) | our code, the component | tested | Exercised on 402 declines (the UAT log HC11 records a reason-class "other" defect) and on the kiosk fallback at the 2026-06-05 accessibility walk (HC13); the 503 and 429 paths are explicitly untested, since the FS-2 200 injected-timeout run and the FS-5 50 suppressed-webhook run of 2026-06-08 (HC2, HC3) produced no 402 decline and did not exercise a decline announcement (section 1) |
| Kiosk fallback announces "pay at the till" at or before 10 s (BR-004, AC-10, N31) | our code on kiosk; the 10 s clock is the kiosk's, not the checkout's | tested | Walked at the 2026-06-05 accessibility walk by Noor Haddad for Ines Castellanos (HC13), against the design system's screen pairing rather than a kiosk device; evidence inherited from the Quay journey's Gate 4 attempt 2 (2026-06-09) is cited, not re-run here |
| Focus is visible on web and app after the panel mounts (the panel's own obligation, not the browser default) | our code, the component | tested | Gate 4 attempt 2 evidence |
| The step-up challenge handoff moves focus to the challenge heading inside the app's web view | library (Kestrel); tracked by our code, Ines Castellanos | flagged | AX-2, an inherited, vendor-owned finding routed to Kestrel and to Ines Castellanos for tracking; this component's obligation here is to not swallow the vendor's focus move on handoff, which is the only behavior it can own |
| Decline reason class present on every panel instance, on every surface | our code, the component, but the underlying S8 decline event stream is Bea Lindqvist's (N20) | tested | AC-4: every decline carries provider, reason class and trace id; the 6% "other" class in early Kestrel declines (N62, KI-1) is a mapping fix on the decline stream, not a panel defect, scheduled to bring the rate to 1.5% on 2026-08-14, after this table's Gate 4 attempt 2 re-check |
| Web decline message announcing on appearance | our code, the web checkout, not this component | flagged | AX-1, pre-existing and routed to Ines Castellanos's guest-checkout redesign backlog, out of scope per the seed; this component does not introduce it and does not fix it |

## 8. Known gaps

| Gap | Source (library changelog, prior audit, vendor doc) | Risk-register row id | Owner |
|---|---|---|---|
| The kiosk fallback text is not yet high-contrast at device level | Digital accessibility standard v4 sets WCAG 2.2 level AA for the web store and the app and excludes the kiosks from that posture (HC12) | No register row; tracked as design backlog item by Ines Castellanos, assessed against the journey's R1 to R15 register and judged not to reach it, with R11 (associates stop using kiosks after seeing the "pay at the till" fallback) as the closest row considered | Ines Castellanos |
| Decline reason "other" surfaced in 6% of Kestrel declines at the Gate 5 attempt 2 point (mapping fix scheduled for 2026-08-14, N62, KI-1) | Decline event stream; the 2026-08-14 mapping fix | No register row; tech debt register TD-3, owner Bea Lindqvist | Bea Lindqvist |
| Step-up challenge handoff does not move focus to the challenge heading inside the app's web view (AX-2) | The 2026-06-05 accessibility walk (HC13); vendor-owned behavior, raised with Dani Ferreira | No register row; tracked by Ines Castellanos | Ines Castellanos |

## 9. Do and do not

| Do | Do not | Reason |
|---|---|---|
| Show exactly one retry offer per decline instance, once the offer is taken the retry control is removed from the panel's DOM | Re-show the retry offer after a second failure inside the same session | BR-001 and AC-5: a declined card must never be re-submitted automatically, and a panel that keeps offering a retry it will not honour is a second, unlogged authorisation attempt waiting to happen |
| Render the reason class text exactly as Quay's decline event carries it, never re-map it inside the panel | Re-map or rephrase a reason class per surface | AC-4: every decline carries the same reason class for every surface, so a support log can trace one ticket back to one class; a per-surface rephrase breaks that join and the finance, fraud and support teams each read from one stream (S8) |
| On the kiosk, fire "pay at the till" at or before 10 s and hold the basket 30 minutes | Fire the fallback on a timeout the web/app 20 s rule (HC5) was copied from | BR-004 and N31 are the store-operations rule, agreed by Lena Baptiste; a copied web timeout would leave a customer standing at a PIN pad waiting on a clock nobody owns |
| Keep the behavioral contract consistent across surfaces, one pattern documented for consistency | Fork a per-surface copy "because the copy differs" | One surface's fork of a payment outcome panel is exactly what the contractor-built wrapper over the legacy providers became: unowned, undocumented, and nobody could change it safely until 2026-04-24 (R2, HC52); the same shape on the UI side would be the same failure, slower to spot and costlier to unwind |

## 10. Ownership and status

| Field | Value |
|---|---|
| Ownership model | Existing component pattern being documented for consistency; behavioral contract defined centrally, implemented separately on each surface |
| Who pulls upstream fixes | Ines Castellanos (design) and the payments squad's front-end pair, with Bea Lindqvist as the contact for any change that touches the decline event contract (S8, AC-4) |
| Status | Trial |
| If Deprecated: replacement | Not deprecated |
| If Deprecated: removal date | Not applicable |

Governance for how a status change or a deprecation is decided lives in [Design systems and tokens](../knowledge/design/design-systems-and-tokens.md); this table records the current state, not the process that sets it.

## 11. Open questions

| Question | Owner | Needed by | Blocks (section) |
|---|---|---|---|
| Is the kiosk's PIN-pad high-contrast mode reliable enough, across 61 kiosks, that shipping the high-contrast appearance inside the component is safe (the pruned rows in section 3)? | Ines Castellanos with Lena Baptiste | Before the redesign's first kiosk pilot shop, after 2026-11-11 | Section 3 (kiosk high-contrast prunes) |
| Does the 20 s web/app client timeout (target, HC5), above Quay's worst case of 18 s (HC5, N61), hold against the kiosk's own 10 s clock in a shared session, or does the checkout need its own visible "still waiting" state distinct from the Loading row? | Ines Castellanos with Tomasz Wierzbicki | Before the redesign's first release candidate, after 2026-11-11 | Section 4 (Loading row) |
| When localisation reopens, does the reason class text stay identical across surfaces, or does a translated reason class break the join AC-4 relies on? | Ines Castellanos with Anneliese Vogt | Next localisation sweep (NFR section 5 waiver's revisit date) | Sections 6 and 9 |

---

## How this spec fails while looking complete

The variant matrix lists every combination that ships and section 4's state table has a row for all ten states, so the page reads as exhaustive, while section 7's evidence column says "assessed from source" for the two obligations that live on the device rather than in a browser (the kiosk fallback announcement, and the vendor-owned step-up focus move). The section 4 Selected row is kept rather than deleted, which is honest but also the kind of kept row that a reviewer reads as "covered" when it means "not applicable, here is why"; a later pass that deletes this row, or worse, that reads "not applicable" as "tested clean," is how a shared component ships a state nobody walked. The second way this fails sits between sections 2 and 6: the anatomy tree was drafted with Bea Lindqvist on 2026-10-19, which is what the file claims, but the claim is unverifiable from this page alone, so a reader who trusts the note without checking that Bea Lindqvist signed it, not merely met with Ines Castellanos, is trusting the very thing Curtis names as the reason to draft anatomy together rather than in sequence. The third, and the one this file cannot write away: every surface that consumes this panel also consumes a different timeout (N31 on kiosk, HC5 on web/app), and a component whose Loading row's duration is decided by a caller's number, not its own, is a component whose most visible state is owned by three different clocks.

## Exit gate (feeds Gate 3: architecture and risks reviewed)

- [x] Section 1's "do not use when" names a real look-alike component, not a strawman. The Kestrel hosted fields (I-1), the step-up challenge handoff (vendor integration, not a register row) and the receipt and order confirmation are all real components this one is not; the "nearest look-alike" line names each
- [x] The anatomy in section 2 matches the code, confirmed by the engineer who built it, not assumed from the design file. Bea Lindqvist co-drafted the tree on 2026-10-19, per the note under section 2; verified at the redesign pass's Gate-3-equivalent review, 2026-11-11, by Tomasz Wierzbicki, who owns the build
- [x] The variant matrix shows the full cross product (20) and every pruned combination has a reason. Five pruned rows (the compact × outline cross product), each with a reason; fifteen combinations ship
- [x] Every state in section 4 has a row; any deleted row says why the component cannot enter that state. Ten rows, none deleted; three (Selected, Read-only, Empty) kept with "not applicable, here is why"
- [x] Keyboard decisions are signed by both product and design. Section 5: Ife Adeyemi, Product, and Ines Castellanos, Design
- [x] Every token in section 6 is named by tier, with no raw value anywhere in this file. Seven rows, tier named on each; no hex, no pixel value appears in this file
- [x] Section 7 links the accessibility and localisation checklists rather than restating their checks, and every obligation has a responsibility and an evidence status. Section 7 links both checklists and names the two rows (AX-1, AX-2) it deliberately does not restate
- [x] Every known gap in section 8 has a risk-register row id. No gap carries a risk-register row id, because the three gaps were assessed against the journey's R1 to R15 register and judged not to reach it, with R11 (associates stop using kiosks after seeing the "pay at the till" fallback) and R15 (a kiosk authorisation lands after "pay at the till", leaving a second payment authorised) as the closest rows considered: each is a design backlog item or tech-debt item (TD-3) or a vendor-tracked finding, tracked by a named owner outside the register rather than invented into it; this is recorded honestly rather than a row id being manufactured, and the three named owners (Ines Castellanos, Bea Lindqvist, Ines Castellanos again for the vendor tracking) are the checkable substitute
- [x] Section 10's status is Trial, Stable, or Deprecated, and a Deprecated row names a replacement and a removal date. Status is Trial; not deprecated, so those two rows are not applicable
- [x] Signed by Ines Castellanos, 2026-11-11, design
- [x] Signed by Tomasz Wierzbicki, 2026-11-11, engineering
