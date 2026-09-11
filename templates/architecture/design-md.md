---
layer: templates
stage: DESIGN
gate: 3
feeds: ["templates/architecture/component-spec.md", "templates/architecture/design-review-record.md", "templates/architecture/accessibility-checklist.md"]
method: "knowledge/design/design-systems-and-tokens.md"
aliases: ["DESIGN.md Template", "design-md"]
---
# DESIGN.md: [product or feature name]

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); the filled copy lives at `products/<name>/DESIGN.md`, the workspace root beside STATE.md, not inside a stage subfolder
Knowledge: [Design systems and tokens](../../knowledge/design/design-systems-and-tokens.md)
Skill: [drafting-agent](../../agents/drafting-agent.md) for the first draft; [architect-agent](../../agents/architect-agent.md) for the token and component tiers; [design-review](../../skills/design-review/SKILL.md) for the record this file feeds

> **Delete any section you do not need, and say so.** A missing fundamental is accepted here: a product with no dark theme deletes the theme row from section 1 and says why, rather than inventing one. Never leave a heading standing over white space. Weight follows [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- One file an agent can read before touching a pixel or a component prop, and
     a human can read in one sitting. The convention is Google Stitch's original
     DESIGN.md specification; this template's section schema is adapted, with
     credit and the MIT notice reproduced at the foot of this file, from
     VoltAgent/awesome-design-md (commit 8147538). None of the 74 brand
     DESIGN.md files that repository links are a source for this template: they
     describe named products' trade dress under a licence their own list does
     not extend to, and nothing here paraphrases or quotes any of them.

     Neighbours: the design brief (../definition/design-brief.md) sets the
     constraints this file has to honor, including which design system it
     draws from; the accessibility checklist
     (accessibility-checklist.md) owns every accessibility claim in detail,
     and section 4 links it rather than restating its tables; a shared
     component gets its own file in component-spec.md, and this file's
     components table links out to it rather than duplicating its state
     definitions; the design review record (design-review-record.md) is
     where the Gate 3 go decision on this file is signed.

     Fill first: section 1's tokens, because sections 2, 6 and 7 all reference
     them by name. A components table with no token vocabulary behind it is a
     screenshot with captions. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Platforms in scope:** [web, native iOS, native Android, kiosk, email, other] · **Design system this extends:** [named system, or "none: this product defines its own"]

## 1. Tokens

<!-- Three tiers, after Penpot's own design-system implementation and its MCP
     best-practice guide (paraphrased with attribution, MPL-2.0; Penpot docs,
     penpot/penpot@37dab75): global tokens hold raw values (a hex, a pixel
     count); semantic tokens name a role and are the only tier a component may
     reference (surface, text, border, action); component tokens are local
     overrides for one component's variant. A component that references a
     global token directly has skipped a tier, and that is a finding for
     section 9, not a style choice.

     Colors: name by role, not by hue, and pair every foreground colour with
     the background it is measured against. Contrast is measured, not
     assumed; the ratio column is empty until a contrast tool has run, per
     WCAG 2.2 success criterion 1.4.3 (or 1.4.6 where the product commits to
     the enhanced level), see the Understanding page cited in section 10.

     Type scale: the numbers-and-money row is mandatory wherever the product
     shows a quantity or a currency amount, because a number rendered in the
     body font invites the eye to compare digits that are not aligned. Set a
     tabular-figure token so digits share one width, and state the currency
     format (symbol position, thousands separator, decimal places) and how a
     negative value is shown; colour alone must never be the only signal for
     negative, per WCAG 1.4.1.

     Every row's provenance is one of: extracted from shipped code, taken from
     a Figma or Penpot file, agreed in a workshop, or invented for this draft
     and pending a source. "Invented, pending a source" is a valid, honest
     value; a blank cell is not. -->

The full set below may be lifted into the front matter of the filled copy at `products/<name>/DESIGN.md`, for any tool that reads tokens from front matter rather than from a fenced block.

```yaml
colors:
  brand-primary:
    value: "[hex]"
    role: "primary action"
    on_color: "text-on-primary"
    provenance: "[extracted / design file / workshop / invented, pending a source]"
  surface-default:
    value: "[hex]"
    role: "page background"
    on_color: "text-default"
    provenance: "[source]"
  text-default:
    value: "[hex]"
    role: "body text"
    on_color: "n/a"
    provenance: "[source]"
  semantic-success:
    value: "[hex]"
    role: "positive status, confirmations"
    on_color: "text-on-success"
    provenance: "[source]"
  semantic-danger:
    value: "[hex]"
    role: "errors, destructive actions, negative amounts"
    on_color: "text-on-danger"
    provenance: "[source]"
type:
  base_unit_px: "[value]"
  scale_ratio: "[value, or a named step list]"
spacing:
  base_unit_px: "[value]"
radius:
  scale: ["[token: value]"]
elevation:
  levels: ["[token: description, for example flat / hairline border / soft shadow]"]
```

### Colors

| Role | Token | Value | Paired on-colour token | Measured contrast ratio | Provenance |
|---|---|---|---|---|---|
| *Primary action* | *action-primary* | *#0B5FFF (ILLUSTRATIVE)* | *text-on-primary, #FFFFFF* | *4.6:1, measured with the tool named in the accessibility checklist section 1* | *design file* |
| | | | | | |

### Type scale

<!-- One row is not optional: numbers and money. Add every other size the
     product actually uses; do not pre-populate a generic scale the product
     does not have. -->

| Token | Size | Weight | Line height | Letter spacing | Use | Provenance |
|---|---|---|---|---|---|---|
| *body-numeric (ILLUSTRATIVE)* | *16px* | *regular* | *24px* | *0* | *tabular figures; every quantity and currency cell; negative values carry a leading sign and the danger colour, never colour alone* | *invented, pending a source* |
| | | | | | | |

### Spacing, radius and elevation

| Token category | Base unit or scale | Where it applies | Provenance |
|---|---|---|---|
| Spacing | | | |
| Radius | | | |
| Elevation | | | |

## 2. Components

<!-- One row per component, and one state matrix column per state the
     component actually has: default, hover, focus, active or pressed,
     disabled, loading, empty, error. In practice these states are documented
     unevenly, and error, empty and loading are the ones most often skipped;
     do not leave a state cell blank. Enumerate it, mark it "not applicable"
     with a reason, or move it to section 9 as a Known Gap with an owner.

     A component used by more than one surface gets its own file in
     component-spec.md and this row becomes a pointer to it, not a second
     copy of its states. -->

| Component | States enumerated | Tokens referenced | Component spec | Known gap |
|---|---|---|---|---|
| *Payment outcome panel (ILLUSTRATIVE)* | *default, loading, success, error, empty (no attempt yet)* | *semantic-success, semantic-danger, action-primary* | *[component-spec.md](component-spec.md), if one exists for this component* | *none logged* |
| | | | | |

## 3. Content and voice

<!-- This section links the writing guide; it does not restate it. If the
     product has no dedicated writing guide yet, say so as a Known Gap in
     section 9 rather than drafting voice rules inline here. -->

Writing guide: [Content design and forms](../../knowledge/design/content-design-and-forms.md)

| Rule | Reason | Example (ILLUSTRATIVE) |
|---|---|---|
| Error messages name what went wrong and the next step, never only a code | A code with no next step turns a support ticket into the fix | *"That card was declined. Try another card or contact your bank." not "Error 402."* |
| | | |

## 4. Accessibility

<!-- Full detail lives in the accessibility checklist; this section is the
     tokens-and-targets summary a designer checks before that walk starts,
     never a second copy of it. State which conformance level and which
     target-size success criterion govern this product (WCAG 2.2 2.5.5,
     enhanced, or 2.5.8, minimum) so a designer is not left guessing which
     number to hit. A tall button is not evidence of the enhanced level on
     its own: the claim has to name the success criterion and the measured
     value, not the pixel height alone. -->

**Conformance target:** [copied from nfr.md section 5, not chosen here] · **Target-size authority:** [WCAG 2.2 2.5.5 Enhanced / 2.5.8 Minimum, and why]

| Foreground token | Background token | Context | Measured ratio | Passes target level |
|---|---|---|---|---|
| *text-on-primary (ILLUSTRATIVE)* | *action-primary* | *primary button label* | *4.6:1* | *yes, AA* |
| | | | | |

Full walk: [accessibility-checklist.md](accessibility-checklist.md).

## 5. Responsive and platform

<!-- One row per platform in scope. A kiosk or TV surface needs a viewing
     distance and the target-size and type-scale delta that follows from it;
     a native app needs the platform's own gesture and safe-area rules; email
     needs the token subset a mail client can actually render. -->

| Platform | Breakpoint or viewing context | Token or scale delta from section 1 | Provenance |
|---|---|---|---|
| *Kiosk (ILLUSTRATIVE)* | *arm's length, approximately 40cm* | *type scale one step larger; target size uses the enhanced authority, not the minimum* | *workshop* |
| | | | |

## 6. Do and do not

<!-- Every rule states its reason. A rule with no reason is a preference
     dressed as a standard, and an agent following it cannot judge when an
     exception is safe. -->

| Do | Do not | Reason |
|---|---|---|
| *Reserve the danger token for errors and destructive actions (ILLUSTRATIVE)* | *Do not use the danger token for a neutral warning* | *A colour that means two things loses the one signal it was scarce enough to carry* |
| | | |

## 7. Agent guide

<!-- After VoltAgent/awesome-design-md's own Iteration Guide idea (adapted
     with attribution and the MIT notice below; not from any of its 74 brand
     files). The steering value is the closed vocabulary and the explicit
     rules, not adjectives: an agent that can only choose from named tokens
     cannot invent a hex value by accident. -->

- Reference tokens by name from section 1 only. A raw hex, pixel or colour value inline in code or copy is a defect, not a style choice.
- Change one component at a time, and open a design review record for it per [design-review-record.md](design-review-record.md).
- Add a new variant as a separate row in section 2's states matrix; do not overload an existing state to mean something new.
- A gap in this file (see section 9) is a stop, not licence to invent a value.
- Lint: [tool and command, or "none configured"].

## 8. Design-to-code contract

<!-- After the W3C Design Tokens Community Group format module (adapted with
     notice, W3C Software and Document License) and Penpot's own token
     implementation (paraphrased with attribution, MPL-2.0; Penpot docs,
     penpot/penpot@37dab75). A token name is a public interface between
     design and code in the same way a field name is a public interface
     between two services: renaming one without a deprecation window breaks
     whatever referenced the old name silently. -->

| Question | Answer |
|---|---|
| Token tiers | global (raw values) then semantic (role names, the only tier components reference) then component (local overrides) |
| Exchange format | [DTCG JSON, after the W3C Design Tokens Community Group format module](https://www.designtokens.org/TR/2025.10/format/) / [proprietary export, name it] |
| What a round trip loses | [state it: an unsupported token type dropped silently, a hidden theme left out of export, a resolved value that loses its token reference] |
| Token rename policy | A rename ships the new name alongside the old for [deprecation window], with an owner named here: [name] |
| Theme and set model | [how many themes, how sets combine, which is the default] |
| Source of truth | [design tool / code repository] · **Sync direction:** [design to code / code to design / both, and who resolves a conflict] |
| Plugin or agent permission scopes | [content, library, user or comment read and write, downloads, clipboard; a write scope implies the matching read] |

## 9. Known gaps

<!-- What this file has never specified, so an agent or a designer does not
     have to guess and does not get to invent. Every row needs an owner; a
     gap with no owner just moves the guessing to whoever reads this file
     next. -->

| Gap | Why it is open | Owner | Needed by |
|---|---|---|---|
| [OPEN: state size not specified for the data table component] | [reason] | [name] | [date] |
| | | | |

## 10. Provenance

<!-- Every value in sections 1 through 8 traces to one of these rows, or to
     "invented, pending a source" recorded next to the value itself. This
     table is where a skeptic checks whether "extracted from shipped code"
     means a script ran against production CSS, or means a person looked at
     a screenshot. -->

| Source | What it covers | Evidence class | Link or reference |
|---|---|---|---|
| | | [standard / platform convention / practitioner heuristic / research evidence / vendor claim / adage] | |
| WCAG 2.2 Understanding: Contrast (Minimum) | contrast ratios cited in section 4 | standard | [w3c.github.io/wcag/understanding/contrast-minimum](https://w3c.github.io/wcag/understanding/contrast-minimum.html) |
| W3C Design Tokens Community Group format module | exchange format named in section 8 | standard (W3C Community Group report, 2025.10) | [designtokens.org/TR/2025.10/format](https://www.designtokens.org/TR/2025.10/format/) |

## 11. Owner and sign-off

| Role | Name | Confirms |
|---|---|---|
| Product owner | | Sections 1 to 6 match the design brief's constraints |
| Design lead | | Tokens and components are implementation-ready, not exploratory |
| Engineering counterpart | | Section 8's contract is workable as written |
| Accessibility owner | | Section 4 is complete or every gap is logged in section 9 |

## Exit gate (feeds Gate 3: architecture and risks reviewed)

<!-- The criteria below come from the same study that produced this
     template's schema: the difference between a DESIGN.md that steers an
     agent and one that is a screenshot with captions is these things,
     not visual polish. -->

- [ ] Every value in section 1 is a named token with a role, not a raw value with no name
- [ ] Section 2's states matrix has no blank cell: every state is enumerated, marked not applicable with a reason, or moved to section 9
- [ ] Sections 1 through 8 are internally consistent: no component in section 2 or rule in section 6 references a token that is not in section 1
- [ ] Section 5 gives implementation-ready responsive and platform rules, not a single desktop assumption
- [ ] Section 4 gives implementation-ready accessibility rules and links, never restates, the accessibility checklist
- [ ] Every row in section 9 has an owner and a needed-by date
- [ ] Every value traces to section 10, or is marked invented and pending a source
- [ ] Signed by [name], [date]

---

This template's section schema is adapted, with attribution, from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (commit 8147538), MIT License, Copyright (c) 2026 VoltAgent. That repository credits the DESIGN.md convention itself to Google Stitch's original DESIGN.md specification. No content from the 74 brand DESIGN.md files that repository links was read into, adapted for, or paraphrased into this template.
