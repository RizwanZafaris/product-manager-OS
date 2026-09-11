---
layer: templates
stage: DESIGN
gate: 3
feeds: ["templates/delivery/edge-cases.md", "templates/delivery/testing-strategy.md", "templates/architecture/design-review-record.md"]
method: "knowledge/design/internationalisation-and-rtl.md"
aliases: ["Localisation and RTL Checklist", "localisation-rtl-checklist", "RTL Checklist"]
---
# Localisation and RTL Checklist: [product or feature name]

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); the evidence column is completed in BUILD and checked at Gate 4
Knowledge: [Internationalisation and RTL](../../knowledge/design/internationalisation-and-rtl.md); the underlying standards are [Structural markup and right to left text in HTML](https://www.w3.org/International/questions/qa-html-dir) and the [W3C Arabic and Persian Layout Requirements](https://w3c.github.io/alreq/)
Skill: [acceptance-agent](../../agents/acceptance-agent.md)

> **Delete any section you do not need.** Delete the direction tables for directions the product does not ship into, and say so; keep every table for a market it does serve. This checklist expands the single localisation row in [edge-cases.md](../delivery/edge-cases.md): that row flags that localisation is in scope, this file is the walk, and the result is also what [testing-strategy.md](../delivery/testing-strategy.md) points to for localisation test coverage and what the [design review record](design-review-record.md) checks off at Gate 3. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- Direction is a document level property, not a paint job: dir belongs on
     html and is inherited from there, never faked with a CSS transform. This
     file is the walk, market by market and surface by surface, against that
     rule and the ones next to it: bidi isolation of untranslated tokens inside
     a reordered sentence, overlay and portal content that does not inherit dir
     from its ancestor, the digit family and calendar a locale actually
     defaults to, and script and typeface, not only direction. A checked box
     with an empty evidence cell is a claim, not a check. Fill section 1,
     including the market and surface inventory, first; then walk sections 2
     through 9 one table at a time with dir="rtl" set on html, real translated
     or pseudo-localised text, and the native reader named for that language. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Scope

<!-- Family: what is in scope and who walks it. A market, surface or language
     left off these tables is one nobody is testing, whatever the code
     actually supports. Fill this section first; every later table refers
     back to it, and every language needs its own named reviewer, not one
     generic native reader standing in for all of them. -->

| Field | Value |
|---|---|
| Markets and scripts in scope | [e.g. ar-SA, ar-AE, ur-PK, fa-IR; note which are RTL and which are LTR but multi script] |
| Surfaces in scope | [web, native, email, PDF output, SMS] |
| Base direction mechanism | [confirm dir is set once on html per locale, not toggled with CSS] |
| Pseudo-localisation tool | [tool; used before real translation exists to surface truncation and hardcoded strings] |
| Real translated copy source | [where the actual translated strings for this walk came from; filler text does not count] |

**Reviewers by language:** each language in scope gets its own named native reader; the designer alone cannot sign off a script they do not read.

| Language or script | Reviewer (name) | Not the author or translator? |
|---|---|---|
| | | |
| | | |

| Market or locale | Direction | Digit family (do not assume) | Calendar | Surfaces affected | Section |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

## 2. Direction and markup

<!-- Family: document level direction and the overlay layer that does not
     automatically inherit it. Evidence is the rendered markup or the
     browser's accessibility tree, not a screenshot; "the layout looks
     mirrored" is not evidence that dir is set correctly. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| `dir` is set once, on `html`, per locale, and inherited from there | inspect the rendered markup; confirm no stylesheet fakes direction with a CSS transform | | | |
| `lang` is set on `html` and on any nested element whose language differs from its parent | inspect the rendered markup | | | |
| Layout, spacing and alignment are written with logical properties (`start`/`end`), not physical ones (`left`/`right`) | inspect the stylesheet or design tokens for hardcoded physical values | | | |
| `dir="auto"` is set on free text inputs and on blocks of inserted or user supplied text | inspect the input markup | | | |
| `dirname` is set on form fields, so the direction the user typed in travels to the server | inspect the form markup and the submitted payload | | | |
| Every dialog, toast, tooltip and popover carries correct direction on its own, checked independently of the base page (content mounted through a portal does not inherit `dir` from its ancestor the way ordinary page content does) | open each one with the locale's direction set; do not infer from the base page | | | |
| Any third party embed (payment widget, map, chat widget) either inherits direction correctly or is confirmed as an accepted exception | inspect the embed with the locale's direction set | | | |

## 3. Mixed-direction strings

<!-- Family: the moment scripts actually meet. This is invisible in a mock
     built from placeholder Latin text and only visible with a real
     untranslated token inside a real sentence written the other way. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| Every untranslated token that can appear inside a reordered sentence (name, reference number, IBAN, URL, code, amount) is wrapped for bidi isolation, with `bdi` or `dir="auto"` on its container | render a real sentence in the target script containing one of these tokens; confirm it does not reorder the surrounding words | | | |
| A Latin order number or reference sitting inside an Arabic, Urdu or Persian sentence reads left to right in place, without corrupting sentence order | same test, read by the language's named reviewer | | | |
| A URL or code snippet inside translated body text is isolated and remains readable | same test with a URL in the string | | | |

## 4. Mirroring and its exceptions

<!-- Family: mirroring is a visual rule with real exceptions, and it is not
     limited to the base page. Getting it wrong reads as "broken", getting the
     exceptions wrong reads as "broken in a way a native speaker notices
     first". -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| Directional icons (next, back, progress) mirror with direction; non-directional icons (clock, refresh, real world objects) do not | view the screen in both directions side by side | | | |
| Every dropdown menu opens on the correct side for the direction, and its items read in the correct direction | open each menu with the locale's direction set | | | |
| Keyboard and gesture interaction that depends on direction (which arrow key advances a slider, which side a swipe dismisses) is correct for the locale, not only the visual layout | operate the control by keyboard or gesture | | | |

## 5. Numbers, dates, calendars and currency

<!-- Family: digits are not determined by the language, and calendars are
     never a hand rolled table. Read from CLDR or the platform's ICU backed
     formatting library at run time; never encode a currency or date format by
     hand, and never assume Gregorian or European digits from the language
     code alone. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| The digit family rendered matches the locale's actual default (European, Arabic-Indic, or Extended Arabic-Indic), not assumed from the language code | render a real number in the target locale; confirm against the platform's locale data, not a guess | | | |
| A user can override the digit family where the locale supports more than one convention | find the setting | | | |
| The calendar rendered matches the locale's default (for example Solar Hijri for fa-IR), not hardcoded Gregorian | render a real date in the target locale | | | |
| Thousands and decimal separators match the locale (Western vs Eastern Arabic-speaking regions differ) | render a formatted amount in the target locale | | | |
| No date, number or currency format is hand rolled outside the platform's locale formatting library | inspect the formatting code path | | | |

## 6. Type

<!-- Family: script matters as much as direction, and layouts pixel checked
     only against English strings have not been tested against the script
     that will actually ship. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| The typeface renders the target script correctly, tested with real text in that language, not a Latin placeholder or a related script's sample | render real text in the target script and font stack | | | |
| Urdu text renders in a Nasta'liq style, not defaulted to a Naskh-style Arabic font, where the market expects it | render real Urdu text and compare with the language's named reviewer's expectation | | | |
| Line height is generous enough for the script's diagonal flow or diacritical marks, not tuned only against a different script's line height | render a full paragraph and check for clipping or crowding | | | |

## 7. Text expansion and channel budgets

<!-- Family: two constraints that live outside a single screenshot and are
     easy to miss for exactly that reason: how much room a string needs once
     it is real, and what a narrow channel will actually deliver. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| Layout leaves room for the target language's real expansion or contraction (German and Russian commonly run 20 to 35 percent longer than English, Arabic can run shorter), with no clipped buttons, labels or navigation items | render the real translated strings, not English length assumptions, and check every affected screen | | | |
| Fixed width containers wrap or truncate with an affordance instead of silently overflowing when a real translated string runs longer than the English source | resize or render at the container's actual constraint with real copy | | | |
| The string catalog has been checked for concatenated fragments that assume English word order or English two-way pluralisation | inspect the string catalog for concatenation and confirm each fragment is a complete, independently translatable sentence | | | |
| Where content ships over SMS or another narrow channel, the messaging vendor has confirmed the per message character budget for this script | get the vendor's own documented number for the script in question, not an assumption carried over from English | | | |

## 8. Screen-reader language switching

<!-- Family: pronunciation, not just visible text. A `lang` attribute that
     looks correct in markup has not been tested until a screen reader has
     actually switched languages on it. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| When content on a page switches language mid-flow (an embedded quote, a brand name, a code value in Latin script inside RTL body text), the nested `lang` attribute correctly changes the screen reader's pronunciation language | test with a real screen reader in the target language, not assumed from the `lang` attribute alone | | | |
| Screen reader pronunciation of ordinary translated content has been tested with the actual assistive technology the product's users run | test with a real screen reader in the target language | | | |

## 9. Pseudo-localisation and native-speaker review

<!-- Family: two passes, in order, and neither substitutes for the other.
     Pseudo-localisation finds truncation and hardcoded strings before real
     translation exists; the native-speaker pass finds everything pseudo-loc
     cannot, because it is not actually the target language. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| The layout has been pseudo-localised (lengthened, accented, direction shifted) to surface truncation and hardcoded strings before real translation exists | run the pseudo-localisation pass and review every screen it touches | | | |
| The layout has been re-verified with the real translated copy, not only filler or pseudo-localised text | render the real translated strings | | | |
| Every table above has been walked by the language's own named reviewer from section 1, not the author of the component or the translator | check the reviewer named against the evidence recorded in each table | | | |

## 10. Findings routed

| Finding | Check | Severity | Routed to (backlog item, risk register row) | Owner | Fix by |
|---|---|---|---|---|---|
| | | | | | |

## Exit gate (feeds Gate 3: architecture and risks reviewed)

Filled tables are the localisation audit artifact this checklist produces; open failures become rows in [risk-register.md](../execution/risk-register.md), and the evidence column is what the acceptance agent verifies at [Gate 4](../../os/STAGE-GATES.md). The [edge cases](../delivery/edge-cases.md) hunting list keeps mixed direction content, live user data and portal overlays named explicitly rather than left implicit; this checklist is where that row gets walked, and [testing-strategy.md](../delivery/testing-strategy.md) is where the resulting localisation test coverage gets scheduled.

- [ ] Every market or locale in scope has its direction, digit family and calendar recorded, not assumed from the language code
- [ ] `dir` is confirmed set once on `html`, per locale, with no CSS faking direction
- [ ] Every overlay surface (dialog, toast, tooltip, dropdown menu) has been checked independently of the base page
- [ ] Every untranslated token that can sit inside a reordered sentence has been checked for bidi isolation with real mixed content
- [ ] The layout has been pseudo-localised and separately re-verified with real translated copy, not filler text
- [ ] Every row has a result, and every pass has evidence a reviewer could open
- [ ] Every fail has a row in section 10 with an owner and a date
- [ ] Every language in scope has its own named reviewer, not the author of the component or the translator, and that reviewer's language matches the table they signed

**Sign-off**

| Role | Name | Date |
|---|---|---|
| Designer (whole checklist) | [name] | [YYYY-MM-DD] |
| Language reviewer | [name, language] | [YYYY-MM-DD] |
| Language reviewer | [name, language] | [YYYY-MM-DD] |

Add one row per language reviewer named in section 1; every language in scope needs a signature here before Status moves to Approved.
