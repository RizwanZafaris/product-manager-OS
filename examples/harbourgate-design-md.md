# DESIGN.md: Harbourgate checkout and payment surfaces

Fills [templates/architecture/design-md.md](../templates/architecture/design-md.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Quay is its fictional payment service, Kestrel is a fictional payment provider, every person is fictional, and every value, size and token here is ILLUSTRATIVE, consistent with the [Harbourgate journey](harbourgate-journey.md) data sheet, never to be quoted as a benchmark or copied as a target. See the [examples index](README.md).

**Owner:** Ines Castellanos, Design Lead · **Date:** 2026-04-08 · **Status:** Approved at Gate 3 (accepted 2026-04-10); amended 2026-07-06, kiosk target-size authority confirmed in section 5 before the first store cohort; annotated 2026-06-05, the accessibility walk of section 4
**Platforms in scope:** web, native iOS, native Android, kiosk · **Design system this extends:** none for the payment surfaces: this product defines its own, a token layer over the existing checkout, app and kiosk components (see section 1, note on scope)

## 1. Tokens

These tokens govern the checkout step Quay touches: card entry (Kestrel hosted fields), the decline message and its one-retry offer, the step-up challenge handoff, and the kiosk "pay at the till" fallback. They are new because the product has no shared token vocabulary to inherit, and they are deliberately narrow: no token here restyles the product's own brand colours or its product-page type scale. Note on scope, and it is a Known Gap (section 9): this file is a new artifact of Gate 3, drafted 2026-04-08 from the design standard of record, Harbourgate digital accessibility standard v4 (HC12), which sets WCAG 2.2 level AA for the web store and the app; the hex values below are recorded as invented, pending a source, because no brand DESIGN.md or extracted code dump was available at drafting time, and Ines Castellanos confirmed the surface and text values against the existing checkout and app components on 2026-04-08.

```yaml
colors:
  brand-primary:
    value: "#0B5FFF"
    role: "primary action"
    on_color: "text-on-primary"
    provenance: "invented, pending a source (confirmed against existing components by Ines Castellanos 2026-04-08)"
  surface-default:
    value: "#FFFFFF"
    role: "page background"
    on_color: "text-default"
    provenance: "invented, pending a source"
  text-default:
    value: "#111111"
    role: "body text"
    on_color: "n/a"
    provenance: "invented, pending a source"
  semantic-success:
    value: "#0F7D4A"
    role: "positive status, confirmations"
    on_color: "text-on-success"
    provenance: "invented, pending a source"
  semantic-danger:
    value: "#B3261C"
    role: "errors, destructive actions, negative amounts"
    on_color: "text-on-danger"
    provenance: "invented, pending a source"
type:
  base_unit_px: "16"
  scale_ratio: "1.25 (Major Third)"
spacing:
  base_unit_px: "4"
radius:
  scale: ["radius-sm: 4px", "radius-md: 8px", "radius-full: 9999px"]
elevation:
  levels: ["flat", "hairline-border: 1px outline", "soft-shadow: 0 2px 8px rgba(0,0,0,0.08)"]
```

### Colors

| Role | Token | Value | Paired on-colour token | Measured contrast ratio | Provenance |
|---|---|---|---|---|---|
| Page background | surface-default | #FFFFFF (ILLUSTRATIVE) | text-default, #111111 | 17.8:1 (ILLUSTRATIVE, measured with the tool named in the accessibility-checklist section 1) | invented, pending a source |
| Body text | text-default | #111111 (ILLUSTRATIVE) | n/a | 17.8:1 against surface-default (ILLUSTRATIVE) | invented, pending a source |
| Primary action | action-primary | #0B5FFF (ILLUSTRATIVE) | text-on-primary, #FFFFFF | 4.6:1 (ILLUSTRATIVE, measured against action-primary) | invented, pending a source |
| Positive status | semantic-success | #0F7D4A (ILLUSTRATIVE) | text-on-success, #FFFFFF | 5.1:1 (ILLUSTRATIVE, measured against semantic-success) | invented, pending a source |
| Errors and negative | semantic-danger | #B3261C (ILLUSTRATIVE) | text-on-danger, #FFFFFF | 5.6:1 (ILLUSTRATIVE, measured against semantic-danger) | invented, pending a source |
| Kiosk fallback background | kiosk-fallback-surface (ILLUSTRATIVE) | #111111 | text-on-kiosk-fallback, #FFFFFF | 17.8:1 (ILLUSTRATIVE, measured against kiosk-fallback-surface) | invented, pending a source |

### Type scale

The numbers-and-money row is mandatory here: the checkout shows order total, amount due, and any refund amount, and the kiosk shows the same figures at 40 cm.

| Token | Size | Weight | Line height | Letter spacing | Use | Provenance |
|---|---|---|---|---|---|---|
| body-numeric (ILLUSTRATIVE) | 16px | regular | 24px | 0 | tabular figures; every quantity and currency cell; negative values carry a leading sign and the danger colour, never colour alone | invented, pending a source |
| body-default (ILLUSTRATIVE) | 16px | regular | 24px | 0 | all body copy in the payment step | invented, pending a source |
| heading-payment (ILLUSTRATIVE) | 20px | semibold | 28px | 0 | the checkout step's own heading ("Pay for your order") | invented, pending a source |
| kiosk-body-default (ILLUSTRATIVE) | 20px | regular | 28px | 0 | all body copy on the kiosk, one step up from body-default (see section 5) | workshop, kiosk viewing distance |
| kiosk-heading-payment (ILLUSTRATIVE) | 25px | semibold | 34px | 0 | the kiosk's own heading | workshop |

### Spacing, radius and elevation

| Token category | Base unit or scale | Where it applies | Provenance |
|---|---|---|---|
| Spacing | 4px base; steps 4, 8, 12, 16, 24, 32 | gutters and rhythm inside the checkout step only; the surrounding product page keeps its own spacing, which these tokens do not restyle | invented, pending a source |
| Radius | radius-sm 4px (inputs), radius-md 8px (cards and panels), radius-full (kiosk fallback pill) | all components in section 2 | invented, pending a source |
| Elevation | flat (most content); hairline-border (input focus and error outlines); soft-shadow (the decline panel and the kiosk fallback panel only) | components in section 2; no token here adds shadow to a component the product did not already float | invented, pending a source |

## 2. Components

The four components below are exactly the four walked in the 2026-06-05 accessibility walk (HC13), and each is an existing product component whose content or provider changed, never a new surface (reconciliation note 7 of [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md): "shoppers saw no visible change"). No payment component in this checkout is shared across more than one surface, so none has its own component-spec.md yet; a shared component's second surface is a Known Gap (section 9, DESIGN-G5).

| Component | States enumerated | Tokens referenced | Component spec | Known gap |
|---|---|---|---|---|
| Kestrel hosted card fields (web and app) | default, focus, filled-valid, filled-invalid (a declined card that will not be resubmitted automatically per AC-5), error (a vendor-side load failure), empty (fields not yet mounted). Loading, disabled and pressed not applicable: vendor-owned markup does not expose or document them, which is the finding AX-2 tracks | radius-sm, semantic-danger, surface-default, text-default | none; pointer only (DESIGN-G5 if shared) | vendor-owned internals outside Harbourgate control, tracked as AX-2 |
| Decline message with one-retry offer | default (declined, showing reason class per AC-4), offer-visible (the different-method retry, never the same card again, BR-001), empty (no attempt yet), loading (payment in flight, the retry control absent so nothing submits by accident), error (a step-up or retry that itself failed) | semantic-danger, text-on-danger, action-primary, radius-md | none; pointer only (DESIGN-G5 if shared) | none logged |
| Step-up challenge handoff (web and app) | default (about to hand off), in-challenge (vendor-owned, focus not returned per AX-2), success, error (challenge failed, AC-11: the order is not marked paid). Disabled not applicable: the challenge is only reached when BR-005 requires it; empty not applicable: no state precedes entry; loading is vendor-owned | action-primary, surface-default, text-default | none; pointer only (DESIGN-G5 if shared) | in-challenge focus behaviour is vendor-owned, AX-2 |
| Kiosk "pay at the till" fallback panel | shown (default), timed-out (BR-004: shown within 10 s, basket held 30 min per N31), empty (no basket, not reachable on a kiosk). Hover and focus not applicable: the surface is touch and PIN pad, not pointer or keyboard. Disabled not applicable: no user action is offered, only a message | kiosk-fallback-surface, text-on-kiosk-fallback, radius-full | none; pointer only (DESIGN-G5 if shared) | none logged |

## 3. Content and voice

Writing guide: [Content design and forms](../knowledge/design/content-design-and-forms.md). The product has no dedicated payment-copy guide of its own; the rules below are the payment-step subset of that guide's methods, and a broader writing guide is a Known Gap (section 9, DESIGN-G3).

| Rule | Reason | Example (ILLUSTRATIVE) |
|---|---|---|
| Error messages name what went wrong and the next step, never only a code | A code with no next step turns a support ticket into the fix; AC-4 gives the reason class, so the copy has something true to name | "That card was declined. Try another card or pay at the till." rather than "Error 402" |
| Never promise the money moved when it might not yet, because a missed status webhook is exercised failure scenario FS-5 | A confident "paid" on an order still in flight becomes a support ticket and a duplicate attempt | "We are confirming your payment. Do not try again yet." rather than "Payment successful" |
| The kiosk fallback tells the customer what to do physically, not just what went wrong, because the surface is arm's length with no keyboard to type a reason | An associate or customer standing at a till needs the next physical action, since BR-004 holds the basket for 30 minutes | "Payment did not complete. Take this basket to the till; the shop will hold it for 30 minutes." rather than "Payment unavailable" |
| Refund and negative amounts are always shown with a sign and a reason, never by colour alone | WCAG 1.4.1: colour alone is not a signal; and the order history must not need a legend to read a minus | "Refunded -£64.00, item returned" rather than a green or red number |

## 4. Accessibility

**Conformance target:** WCAG 2.2 level AA for web and app (HC12, Harbourgate digital accessibility standard v4, the conformance claim the NFR carries; not chosen here) · **Target-size authority:** WCAG 2.2 success criterion 2.5.8, Minimum (44px), governs web and app as the AA level's target-size criterion; the kiosk, which sits outside that standard's platform scope, commits to the enhanced criterion 2.5.5 (48px) by its own policy (section 5), because an arm's-length, standing surface with a 10 s SLO (N32) has no second pass at a mis-tap.

| Foreground token | Background token | Context | Measured ratio | Passes target level |
|---|---|---|---|---|
| text-on-primary (ILLUSTRATIVE) | action-primary | primary button label on web and app | 4.6:1 | yes, AA |
| text-on-danger (ILLUSTRATIVE) | semantic-danger | decline message text | 5.6:1 | yes, AA |
| text-on-success (ILLUSTRATIVE) | semantic-success | confirmation text | 5.1:1 | yes, AA |
| text-on-kiosk-fallback (ILLUSTRATIVE) | kiosk-fallback-surface | kiosk "pay at the till" panel | 17.8:1 | yes, enhanced (kiosk policy) |

Annotation, 2026-06-05: the accessibility walk (HC13, run by Noor Haddad for Ines Castellanos) covered the four section 2 components and found 0 accessibility issues introduced by Quay, with 2 pre-existing findings carried, not introduced by this design (AX-1, the web decline message is not announced to screen readers when it appears; AX-2, Kestrel's hosted step-up challenge does not move focus to its heading inside the app's web view). Both are logged in section 9 and routed, not silently carried; neither contradicts the "shoppers saw no visible change" reading the release carries.

Full walk: [harbourgate-accessibility-checklist.md](harbourgate-accessibility-checklist.md).

## 5. Responsive and platform

| Platform | Breakpoint or viewing context | Token or scale delta from section 1 | Provenance |
|---|---|---|---|
| Web | desktop-first, content reflows down to a 360px-wide phone; a hosted-fields iframe can be narrower than the page, so fields use fluid width inside their container, never a fixed px width | type: body-default and body-numeric unchanged; no kiosk delta | workshop |
| Native iOS and Android | the app's own viewport, no browser chrome to account for | as web; type unchanged; the hosted-fields surface is an app web view and its focus behaviour is AX-2 | workshop |
| Kiosk | standing, arm's length, approximately 40 cm to a fixed PIN-pad surface, one kiosk per shop across 61 shops (N1, N2) | type scale one step up (kiosk-body-default 20px, kiosk-heading-payment 25px); target size commits to the enhanced authority, 48px minimum, not the AA minimum (see section 4's target-size authority row) | workshop |

## 6. Do and do not

| Do | Do not | Reason |
|---|---|---|
| Reference only section 1's token names in a component or a rule | Do not put a raw hex, px or pt inline in a component's spec or a review's note | A value with no name cannot be checked against its pair, its contrast, or a rename (section 8) |
| Reserve semantic-danger for declines, failed retries, negative amounts and destructive actions (N35's blocked close shows danger as a status) | Do not use semantic-danger for a neutral warning or for a decline message's mere presence | A colour that means two things loses the one signal it was scarce enough to carry |
| Keep every quantity and currency cell on body-numeric (tabular figures), on the kiosk too | Do not set a price in the product page's proportional body font | Digits that do not share a width invite the eye to compare numbers that are not aligned; the kiosk's 40 cm distance makes the error easier to make, not harder to see |
| Announce the decline message and step-up challenge to assistive tech when they appear, and put focus on the new message when it arrives | Do not hand off to the step-up challenge without stating what it is for | AX-1 and AX-2 are pre-existing defects here, not design intent; silently relying on the vendor's web view is what let AX-2 reach a shipped flow |

## 7. Agent guide

- Reference tokens by name from section 1 only. A raw hex, pixel or pt value inline in code or copy is a defect, not a style choice.
- Change one component at a time, and open a design review record for it per [harbourgate-design-review-record.md](harbourgate-design-review-record.md).
- Add a new variant as a separate row in section 2's states matrix; do not overload an existing state to mean something new.
- A gap in this file (section 9) is a stop, not a licence to invent a value.
- Lint: none configured.

## 8. Design-to-code contract

| Question | Answer |
|---|---|
| Token tiers | global (raw values) then semantic (role names, the only tier components reference) then component (local overrides); the four section 2 components reference semantic tokens only |
| Exchange format | DTCG JSON, after the W3C Design Tokens Community Group format module |
| What a round trip loses | kiosk-* tokens are a separate set and must be exported explicitly or they drop silently; a vendor-owned internal value inside Kestrel hosted fields has no token at all and a round trip cannot carry it |
| Token rename policy | a rename ships the new name alongside the old for one sprint (two weeks) with a migration note, owner named here: Ines Castellanos |
| Theme and set model | one default set; kiosk-* is a platform set applied only on the kiosk surface; no dark theme exists yet, so the theme row is deleted with reason, see section 1's note on scope |
| Source of truth | design tool (Penpot), then code (the repo's token module) · **Sync direction:** design to code, and Ines Castellanos resolves a conflict |
| Plugin or agent permission scopes | content read and write, comment read, library read only; no download or clipboard write |

## 9. Known gaps

| Gap | Why it is open | Owner | Needed by |
|---|---|---|---|
| DESIGN-G1: no dark theme exists, so section 1 has no theme row | The product does not ship a dark theme, so it was deleted with reason rather than invented | Ines Castellanos | revisit if and when the product commits to a dark theme; no date |
| DESIGN-G2: the kiosk sits outside Harbourgate digital accessibility standard v4 (HC12), so the enhanced 2.5.5 target-size commitment here is product policy, not standard policy | The standard's platform scope is web and app; the kiosk needs its own clause before it can inherit the standard's conformance claim | Ines Castellanos | 2026-07-06, before the first store cohort (Gate 5 attempt 3, 2026-07-29) |
| DESIGN-G3: no product-wide writing guide; section 3's rules are the payment-step subset of the content-design method, not a payment style guide | A guide beyond the payment step would overlap the product's existing copy without a decision on who owns the whole | Ines Castellanos | 2026-10-16, next design review cycle (annotation) |
| DESIGN-G4: AX-1 and AX-2 (see section 4) are pre-existing defects, not introduced by Quay, and are still open | Both belong to surfaces that existed before Quay: AX-1's decline message predates the payment step and is routed to the deferred guest checkout redesign Ines Castellanos already owns as a Known Gap; AX-2's step-up focus behaviour is vendor-owned inside the app web view and is routed to Dani Ferreira (Kestrel merchant success manager, I-1), tracked here by Ines Castellanos | Ines Castellanos | 2027-06-15 (N52), the provider-portal wind-down date, by which AX-2's vendor path is either fixed or the step-up surface changes |
| DESIGN-G5: no component-spec.md exists yet for any payment component, because none is currently shared across surfaces | A component shared across web, app and kiosk needs its own spec file; if one is shared this file's section 2 row becomes a pointer to it, not a second copy of its states | Ines Castellanos | if and when a payment component crosses to a second surface; no date |

## 10. Provenance

| Source | What it covers | Evidence class | Link or reference |
|---|---|---|---|
| Harbourgate digital accessibility standard v4 (HC12) | the WCAG 2.2 level AA conformance claim for web and app in section 4 | vendor claim (an internal standard of record) | design standard v4, held by Ines Castellanos |
| Kestrel master services agreement and Kestrel merchant success contact (Dani Ferreira) | the Kestrel hosted fields component in section 2 and the AX-2 vendor routing in section 9 | vendor claim | Kestrel MSA, held by Anneliese Vogt; I-1 |
| Harbourgate journey data sheet, rows N1, N31, N32, N52 | the kiosk's 61-shop, 40 cm, 10 s, 30 min and wind-down context in sections 1, 3, 5 and 9 | research evidence, in the fiction, measured or target | [harbourgate-journey.md](harbourgate-journey.md) |
| Accessibility walk, 2026-06-05 (HC13, findings AX-1 and AX-2) | section 4's annotation and section 9's DESIGN-G4 | research evidence, in the fiction, measured | [harbourgate-accessibility-checklist.md](harbourgate-accessibility-checklist.md) |
| WCAG 2.2 Understanding: Contrast (Minimum), and success criteria 1.4.1, 2.5.5 and 2.5.8 | every contrast ratio and target-size claim in sections 3, 4 and 5 | standard | [w3c.github.io/wcag/understanding/contrast-minimum](https://w3c.github.io/wcag/understanding/contrast-minimum.html) |
| W3C Design Tokens Community Group format module | the exchange format named in section 8 | standard (community group draft) | [designtokens.org/tr/drafts/format](https://www.designtokens.org/tr/drafts/format/) |

## 11. Owner and sign-off

| Role | Name | Confirms |
|---|---|---|
| Product owner | Ife Adeyemi | Sections 1 to 6 match the design brief's constraints |
| Design lead | Ines Castellanos | Tokens and components are implementation-ready, not exploratory |
| Engineering counterpart | Tomasz Wierzbicki | Section 8's contract is workable as written |
| Accessibility owner | Ines Castellanos | Section 4 is complete or every gap is logged in section 9 |

## Exit gate (feeds Gate 3: architecture and risks reviewed)

- [x] Every value in section 1 is a named token with a role, not a raw value with no name
- [x] Section 2's states matrix has no blank cell: every state is enumerated, marked not applicable with a reason, or moved to section 9
- [x] Sections 1 through 8 are internally consistent: no component in section 2 or rule in section 6 references a token that is not in section 1
- [x] Section 5 gives implementation-ready responsive and platform rules, not a single desktop assumption
- [x] Section 4 gives implementation-ready accessibility rules and links, never restates, the accessibility checklist
- [x] Every row in section 9 has an owner and a needed-by date (DESIGN-G1 and DESIGN-G5 carry a conditional "if and when" rather than a calendar date, which is honest for a gap with no known trigger; every other row has a date)
- [x] Every value traces to section 10, or is marked invented and pending a source (every token in section 1 is so marked)
- [x] Signed by Ines Castellanos, 2026-04-08
