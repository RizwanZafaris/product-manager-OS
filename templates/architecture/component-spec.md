---
layer: templates
stage: DESIGN
gate: 3
feeds: ["templates/architecture/design-review-record.md", "templates/execution/risk-register.md", "templates/delivery/testing-strategy.md"]
method: "knowledge/design/design-systems-and-tokens.md"
aliases: ["Component Spec", "component-spec"]
---
# Component Spec: `<component name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); the evidence column is re-checked at Gate 4
Knowledge: [Design systems and tokens](../../knowledge/design/design-systems-and-tokens.md)
Skill: [design-review](../../skills/design-review/SKILL.md)

> **Delete any section you do not need.** A component with no library heritage still fills sections 1 through 6 and 10; skip section 8 only by writing "no known gaps imported, because <reason>", never by deleting the heading. Never leave a heading standing over white space. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- Write one of these only for a component two or more surfaces share; a
     one-screen composition belongs in the design brief and the design review
     record, not here (WHICH-DOCUMENT.md). The section order below follows
     Nathan Curtis's content architecture for component documentation:
     introduction, examples, design reference, code reference, in that order,
     because engineers return to this page five or ten times a day and
     designers less often (Curtis, "Documenting Components," EightShapes).
     Anatomy and the variant matrix are drafted with the engineer who will
     build the component, not handed down from design alone: Curtis's
     companion piece on crafting a component API argues that anatomy,
     properties and layout diverge quietly between a Figma file and a code
     file unless a team aligns the three together before coding starts
     ("Crafting Component API, Together," EightShapes). Storybook's own
     documentation model treats each state in section 4 as a first-class,
     independently viewable story rather than a screenshot in a design file,
     which is why the state table asks what is rendered and what is
     announced, not what it looks like (Storybook, "Automatic documentation
     and Storybook"). Comparing how shadcn/ui, Material UI and Chakra UI
     document their own components turns up the same four-part anatomy,
     variant table and states table, which is why this file uses them rather
     than inventing a fifth shape. Penpot's design-system documentation adds
     the two sections a component library usually skips: known gaps and an
     ownership and status line, because a spec that only shows the happy
     path teaches a team to trust a page that is quietly out of date.

     This file is the spec, not the source of truth for values: token
     values, hex codes, and pixel measurements live in the design system
     itself; this file names which tokens a component consumes, by tier and
     name, never by value, the same rule the design review record's handoff
     section enforces. Accessibility and localisation evidence live in their
     own checklists; section 7 links them and adds only what a shared
     component needs beyond a single screen's walk: a responsibility split
     and an evidence-status column, because a shared component's
     accessibility often belongs partly to a library nobody on this team
     wrote. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Surfaces that share this component:** [list two or more; a component used by only one surface does not need this file]

## 1. Purpose, use when, do not use when

<!-- One or two sentences of purpose, then two short lists. "Use when" and "do
     not use when" are the sentence a designer or engineer reads before
     reaching for this component instead of building something new; a
     component with no "do not use when" line invites misuse by every team
     that never read the rest of the page. Name the nearest look-alike
     component this one is not, and why. -->

**Purpose:** [what problem this component solves, in one or two sentences]

| Use when | Do not use when |
|---|---|
| [ILLUSTRATIVE: confirming a destructive action the user chose] | [ILLUSTRATIVE: the action is reversible; use an inline toast with undo instead] |
| | |

**Nearest look-alike, and why this is not it:** [ILLUSTRATIVE: a Popover; a Dialog traps focus and blocks the rest of the page, a Popover does not]

## 2. Anatomy

<!-- The element hierarchy as a text composition tree, drafted with the
     engineer, not derived from a screenshot after the fact (Curtis,
     "Crafting Component API, Together"). Name every subcomponent that would
     need its own entry in section 3 if it grows its own variants. Mark
     which nodes are required, which are optional slots, and which accept
     arbitrary composed content. -->

```
<Component name> (required)
  <Trigger> (required, or omitted if programmatically opened)
  <Content>
    <Header>
      <Title> (required)
      <Description> (optional)
    <Body> (slot: accepts arbitrary composed content)
    <Footer>
      <Action> (slot: zero or more)
```

**Subcomponents that carry their own variants (get their own row in section 3, or their own spec if the list grows past two or three):** [list]

## 3. Variant matrix

<!-- The full cross product first, so the count is honest, then the pruned
     set that actually ships, with a reason for every combination that was
     cut. A matrix with no pruning step is either trivially small or hiding
     combinations nobody tested. Compound combinations (two dimensions that
     interact, such as a size that is not available in a given appearance)
     get their own row rather than a footnote. -->

**Dimensions:** appearance × size × intent

| Dimension | Values | Count |
|---|---|---|
| Appearance | [ILLUSTRATIVE: solid, outline, ghost] | 3 |
| Size | [ILLUSTRATIVE: small, medium, large] | 3 |
| Intent | [ILLUSTRATIVE: default, primary, destructive, disabled] | 4 |

**Full cross product:** 3 × 3 × 4 = 36 combinations

**Defaults:** appearance = [value], size = [value], intent = [value]

**Compound combinations and prunes:**

| Combination | Ships? | Reason if pruned |
|---|---|---|
| *ghost × destructive (ILLUSTRATIVE)* | *No* | *A destructive ghost button reads as a low-priority link; destructive intent ships only in solid and outline* |
| | | |

**Pruned set that ships:** `<n>` of 36 combinations, listed in full in [design system component catalog / Storybook link]

## 4. States

<!-- One row per state. Every row names the element the state lives on (the
     trigger, the whole component, a child), the ARIA state or role it sets,
     what an assistive-technology user hears, and the keyboard behavior that
     produces or follows from it. States are composed from these rows, never
     hardcoded as a separate "disabled variant" prop that duplicates what the
     state table already owns (Storybook documents each state as its own
     story for the same reason: a state is a fact about the component's
     condition, not a design choice re-made per variant). Delete a row only
     if the component genuinely cannot enter that state, and say why in the
     Notes column. -->

| State | Element that carries it | ARIA state or role | What is announced | Keyboard behavior | Notes |
|---|---|---|---|---|---|
| Default | | | | | |
| Hover | | | | pointer only; no keyboard equivalent | |
| Focus-visible | | | | receives focus on Tab; visible focus ring | |
| Pressed | | | | activates on Enter/Space while focused | |
| Selected | | `aria-selected` or `aria-checked` | | | |
| Disabled | | `aria-disabled` or `disabled` | announced as unavailable, still discoverable, or removed from the tab order (state which) | not focusable, or focusable and inert (state which) | |
| Read-only | | `aria-readonly` | | focusable, not editable | |
| Loading | | `aria-busy` | progress is announced without stealing focus | | |
| Error | | `aria-invalid`, `aria-describedby` pointing at the message | error text is announced with the field | | |
| Empty | | | | | |

## 5. Keyboard decisions

<!-- Decisions, not a restatement of the states table: how the component is
     activated, whether moving focus also changes selection (selection
     follows focus) or requires a separate confirming key, and where focus
     lands on open and returns to on close. These are product and design
     calls with real behavioral consequences, not implementation detail, so
     they are signed here rather than left to whoever writes the code. -->

| Decision | Choice | Reason |
|---|---|---|
| Activation mode | [click / Enter / Space / any] | |
| Selection follows focus | [yes, moving focus selects / no, a separate key confirms] | |
| Focus on open | [first item / trigger remains / named element] | |
| Focus on close | [returns to trigger / moves to named element] | |
| Escape behavior | [closes and returns focus / no-op / named] | |

**Signed by:** Product [name], Design [name]

## 6. Tokens consumed

<!-- Token name and tier, never a value: a raw hex code or pixel number in
     this table is the handoff bug the design review record's section 5
     already checks for. Tier is global, semantic, or component, following
     the same three-tier hierarchy the design-system knowledge card uses; a
     component-tier token is local to this component and safe to change
     without a wider review, a semantic-tier token is not. -->

| Token name | Tier (global / semantic / component) | Used for |
|---|---|---|
| `color.border.default` | semantic | default border, all appearances |
| `color.bg.critical` | semantic | solid appearance, destructive intent |
| `radius.md` | global | corner radius, all sizes |
| `component.button.paddingInline.md` | component | horizontal padding, medium size |

## 7. Accessibility and localisation

<!-- Link the accessibility checklist's table for this component type and the
     localisation and RTL checklist; never restate a check either file
     already owns. What this section adds, beyond a single screen's walk, is
     who is responsible for each obligation on a shared component (a
     component partly built on a third-party library, where some
     accessibility behavior is inherited rather than authored here) and how
     confident the evidence for each obligation actually is. "Assessed from
     source" means someone read the library's code or docs and judged it
     correct without running an assistive-technology test; it is weaker than
     "tested" and stronger than a guess, and it should not be presented as
     equivalent to "tested" at Gate 4. -->

**Accessibility checklist table for this component type:** [link to the relevant table in [accessibility-checklist.md](accessibility-checklist.md), e.g. "section 4, Controls: buttons, links, menus"]
**Localisation and RTL checklist:** [link to [localisation-rtl-checklist.md](localisation-rtl-checklist.md)]

| Obligation | Responsibility (library / shared / our code) | Evidence status (tested / assessed from source / flagged) | Note |
|---|---|---|---|
| *Keyboard trap avoidance on open (ILLUSTRATIVE)* | *library* | *assessed from source* | *not run against our own assistive-technology pairing yet; route to accessibility checklist section 8 when tested* |
| | | | |

## 8. Known gaps

<!-- Gaps the underlying library or an earlier build already discloses, not
     gaps this team is inventing here for the first time (a newly found gap
     goes straight to the accessibility checklist or the risk register, not
     into this list as if it were pre-existing). Every gap gets a
     risk-register row id; a known gap with no row id is a known gap nobody
     is tracking. -->

| Gap | Source (library changelog, prior audit, vendor doc) | Risk-register row id | Owner |
|---|---|---|---|
| | | [risk-register.md](../execution/risk-register.md) row `<id>` | |

## 9. Do and do not

<!-- Pairs, each with a reason. A "do not" with no reason reads as taste and
     gets argued with; a "do not" with a reason is a rule someone can check
     their own case against. -->

| Do | Do not | Reason |
|---|---|---|
| *Use one primary-intent instance per view (ILLUSTRATIVE)* | *Use two primary-intent instances in the same view* | *Two competing primary actions make the user guess which one the product actually wants* |
| | | |

## 10. Ownership and status

<!-- Ownership is how this component enters the codebase, which decides who
     pulls upstream fixes and how a breaking change in the upstream library
     reaches this product. Status follows a Trial / Stable / Deprecated
     lifecycle; a Deprecated row without a replacement and a removal date is
     a component nobody can safely stop using. Link the design-system
     card's governance guidance rather than restating it here. -->

| Field | Value |
|---|---|
| Ownership model | [copied-in code / installed dependency, pinned to a version / CSS-only classes over a shared primitive] |
| Who pulls upstream fixes | [name or team] |
| Status | [Trial / Stable / Deprecated] |
| If Deprecated: replacement | |
| If Deprecated: removal date | |

Governance for how a status change or a deprecation is decided lives in [Design systems and tokens](../../knowledge/design/design-systems-and-tokens.md); this table records the current state, not the process that sets it.

## 11. Open questions

| Question | Owner | Needed by | Blocks (section) |
|---|---|---|---|
| | | | |

---

## How this spec fails while looking complete

The variant matrix lists every combination that ships and section 4's state table has a row for all ten states, so the page reads as exhaustive, while every "Evidence status" cell in section 7 says "assessed from source": nobody has actually run a screen reader against this component, and a reviewer skimming filled tables sees completeness where there is only description. The second way this fails sits between sections 2 and 6: the anatomy tree was drafted from the Figma file alone, without the engineer who will build it, so the names in section 2 (`CardActionsArea`) and the token names in section 6 quietly diverge from what the code will actually call them; the spec looks signed off while design and code have never been reconciled, which is the exact failure Curtis's companion article on component API names as the reason to draft anatomy together rather than in sequence.

## Exit gate (feeds Gate 3: architecture and risks reviewed)

- [ ] Section 1's "do not use when" names a real look-alike component, not a strawman
- [ ] The anatomy in section 2 matches the code, confirmed by the engineer who built it, not assumed from the design file
- [ ] The variant matrix shows the full cross product and every pruned combination has a reason
- [ ] Every state in section 4 has a row; any deleted row says why the component cannot enter that state
- [ ] Keyboard decisions are signed by both product and design
- [ ] Every token in section 6 is named by tier, with no raw value anywhere in this file
- [ ] Section 7 links the accessibility and localisation checklists rather than restating their checks, and every obligation has a responsibility and an evidence status
- [ ] Every known gap in section 8 has a risk-register row id
- [ ] Section 10's status is Trial, Stable, or Deprecated, and a Deprecated row names a replacement and a removal date
- [ ] Signed by [name], [date], design
- [ ] Signed by [name], [date], engineering
