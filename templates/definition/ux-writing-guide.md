---
layer: templates
stage: DEFINE
gate: 2
feeds: ["templates/definition/acceptance-criteria.md", "templates/delivery/release-notes.md", "templates/architecture/localisation-rtl-checklist.md"]
method: "knowledge/design/content-design-and-forms.md"
aliases: ["UX Writing Guide", "ux-writing-guide"]
---
# UX Writing Guide: [product or feature name]

Stage: DEFINE, feeds [Gate 2: requirements signed off](../../os/STAGE-GATES.md); written with the design brief and kept current through OPERATE
Knowledge: [Content design and forms](../../knowledge/design/content-design-and-forms.md)
Skill: [drafting-agent](../../agents/drafting-agent.md) for the first draft; [spec-review](../../skills/spec-review/SKILL.md) checks every screen against it before Gate 2

> **Delete any section you do not need.** A ticket-weight change reuses the product's existing guide unchanged; a new product fills every section once, then this file stops changing shape and only grows rows. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md). Never leave a heading standing over white space.

<!-- The standard every string in the product is audited against, so that
     "error message" is not reinvented, differently, by every squad that writes
     one. It sits next to the design brief (../definition/design-brief.md), not
     inside it, because voice and message patterns outlive any one feature and a
     brief is scoped to one.

     Neighbours: the design brief owns the problem and the users this guide writes
     for; the content design and forms knowledge card
     (../../knowledge/design/content-design-and-forms.md) owns the method behind
     sections 2 and 3; the accessibility checklist
     (../architecture/accessibility-checklist.md) owns the WCAG evidence that
     section 8 promises; the localisation and RTL checklist
     (../architecture/localisation-rtl-checklist.md) owns the structural walk that
     section 7 promises; acceptance criteria
     (../definition/acceptance-criteria.md) turn the message patterns in section 3
     into testable pass-or-fail lines; release notes
     (../delivery/release-notes.md) reuse this guide's voice for the audience
     that reads them.

     Fill first: section 1, so the rest of the guide is written for a named
     reader instead of an imagined one, then section 2, because sections 3
     through 8 are that voice applied to specific situations, not new decisions. -->

**Product owner:** [name] · **Content design lead:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Agreed / Superseded
**Links:** [design brief](design-brief.md) · [personas](../discovery/personas.md) · [accessibility checklist](../architecture/accessibility-checklist.md) · [localisation and RTL checklist](../architecture/localisation-rtl-checklist.md)

## 1. Who we write for

<!-- A voice written for "all users" is written for none of them. Reading
     context changes the sentence: a support agent skims a queue, a first-time
     user reads every word, a returning user reads nothing until something is
     wrong. -->

| Persona (link) | What they are trying to do | Reading context | Channel (in-product, email, push, SMS, support script) |
|---|---|---|---|
| [ILLUSTRATIVE] first-time applicant | Complete a form they have never seen before, under time pressure | Full attention, first pass; will not return to re-read | in-product |
| | | | |

## 2. Voice principles

<!-- At most 4. Each one is a real choice the product has made, stated so
     specifically that its opposite is also a coherent voice a competitor could
     choose. "Be clear" is not a principle, it is the job description; a
     principle says how this product resolves clear against something else it
     could have chosen instead. This template never reproduces a vendor voice
     guide: write these in the product's own words, and cite this card's
     Reading section, never the vendor's own text, as the source of the method. -->

| Principle | Do (product's own words) | Don't (product's own words) |
|---|---|---|
| [ILLUSTRATIVE] Plain over formal | "You can cancel any time." | "Cancellation may be effected at the customer's discretion." |
| | | |
| | | |
| | | |

## 3. Message patterns

<!-- Each row is a decision, not a template to fill mechanically: the
     knowledge card explains why the evidence points this way and when a
     product's own research overrides it. -->

### 3.1 Error

Say what happened and how to fix it, in plain, positive language, next to the field it belongs to (standard; GOV.UK Design System, error-message component). Never use an error message for something the user cannot fix, such as ineligibility or a service outage; send them to a page that explains the problem and what to do next instead (standard; same source). Avoid technical jargon and words that blame the user, "forbidden," "illegal," "you forgot"; avoid "please," because it implies a choice, and "sorry," because it does not help fix the problem (standard; same source).

| Situation | Message pattern | Example (ILLUSTRATIVE) |
|---|---|---|
| Field left empty | An instruction: "Enter [what is missing]" | "Enter your date of birth" |
| Field fails a format rule | A description naming the rule | "Postcode must be a real UK postcode" |
| The user cannot fix the problem (ineligibility, outage) | Route to an explanation page, not an inline error | [OPEN: link the problem page this product uses] |

### 3.2 Empty

State what would normally be here, then give a direct path into the task that would fill it (standard; Carbon Design System, empty-states pattern; Nielsen Norman Group, "Designing Empty States in Complex Applications"). Distinguish a first-use empty state from the result of a user's own filter or search, from an error state; each needs a different sentence, because "nothing here yet" and "nothing matches" are not the same fact.

### 3.3 Success

Confirm what happened, in the past tense, without inviting a second look for reassurance the action already succeeded.

### 3.4 Confirmation

Use a confirmation step only before an action with serious consequences, destroying work, an irreversible charge, or anything that cannot be undone (standard; Nielsen Norman Group, "Confirmation Dialogs Can Prevent User Errors, If Not Overused"). Prefer undo to confirmation wherever the action can be reversed after the fact. A generic "Are you sure?" on a reversible action trains people to click through it, which removes the protection on the one action later that actually needed it.

### 3.5 Notification, by persistence

State how long a message stays on screen as a product decision, not a default (standard; Carbon Design System, notification pattern): an inline notification stays until the user dismisses it or the underlying state resolves; a toast without an action can clear itself; a toast or banner carrying an action stays until the user acts or dismisses it. Use a page-level banner sparingly. There is evidence people miss banners placed outside the content they are reading, so information belonging to the current task goes in the main content, not a banner above it (standard; GOV.UK Design System, notification-banner component).

| Message type | Persistence | This product's rule |
|---|---|---|
| Inline (next to a field or row) | Until dismissed or resolved | |
| Toast, no action | Can clear on its own | |
| Toast or banner with an action | Until acted on or dismissed | |

### 3.6 Form validation timing

State this product's decision once here, and link it from every form so no screen re-derives it. Validating inline, field by field, rather than only on submit, measured higher task success and fewer errors, plus 31% higher satisfaction, 42% shorter completion time and 47% fewer eye fixations, in a small usability study across six form variants (research evidence, one study; Wroblewski, "Inline Validation in Web Forms," tested with Etre). Treat the finding as a reason to default to inline validation, not as a number this product can cite as its own; a product that validates differently should say why and where.

**This product's decision:** [OPEN: inline per field / on submit / hybrid, owner, date]

## 4. Banned and preferred words

<!-- Seeded from the GOV.UK Design System error-message component (adapt under
     licence: Open Government Licence v3.0, Crown copyright; this section
     contains public sector information adapted from the GOV.UK Design System
     under the Open Government Licence v3.0, https://design-system.service.gov.uk/components/error-message/).
     Add product-specific rows below the seed; never delete a seed row, only
     add "unless" exceptions this product has actually decided. -->

| Banned | Why | Prefer instead |
|---|---|---|
| forbidden, illegal, prohibited | Blames the user for a system decision | State what to do instead |
| you forgot | Assumes carelessness the product cannot know | "Enter [field]" |
| please | Implies the action is optional | Remove it; state the instruction plainly |
| sorry | Does not help the user fix the problem | Remove it; lead with the fix |
| valid, invalid | Adds nothing a specific rule does not already say | Name the actual rule broken |
| error 0x0000000643, unspecified error, and other technical codes | Meaningless to the reader | Plain-English description of what happened |
| [ILLUSTRATIVE product addition] utilize | Longer than the plain word, no added meaning | use |
| | | |

## 5. Terminology glossary

<!-- One term, one meaning, used the same way on every screen, in every
     message, and in support scripts. A second term for the same concept is a
     silent bug: a user who has learned one word does not recognise the
     other. -->

| Term | Meaning in this product | Never use instead |
|---|---|---|
| [ILLUSTRATIVE] Workspace | The account-level container a user's projects live in | Team, Organisation, Hub |
| | | |

## 6. Numbers, money, dates and time

<!-- Never hand-encode a locale's number, date or currency format. Read it
     from the platform's Unicode CLDR-backed formatting library (ICU or
     equivalent) at run time (standard; Unicode CLDR project,
     https://cldr.unicode.org/index); a hand-built table drifts out of date
     the day CLDR next publishes and silently mis-formats a market this
     product has not tested. The localisation and RTL checklist
     (../architecture/localisation-rtl-checklist.md) carries the structural
     walk this rule feeds. -->

| Element | Rule | Evidence class |
|---|---|---|
| Decimal and thousands separators | Read from CLDR per locale; never assume comma-decimal or period-decimal | standard (Unicode CLDR) |
| Calendar | Read from CLDR per locale; never assume Gregorian | standard (Unicode CLDR) |
| Currency display | Read symbol, placement and rounding from CLDR per locale | standard (Unicode CLDR) |
| Date order and separators | Read from CLDR per locale; never assume day-month-year | standard (Unicode CLDR) |
| Relative time ("2 hours ago") | [OPEN: this product's cutoff before switching to an absolute date, owner] | product decision |

## 7. Languages and scripts

<!-- This section names the operating facts; the walk that proves them lives
     in the localisation and RTL checklist
     (../architecture/localisation-rtl-checklist.md). -->

| Field | Value |
|---|---|
| Source language this guide is written in | [language] |
| Translation workflow | [translation memory tool, vendor, or in-house process] |
| Reviewer per shipped language | [name or role, one per language; a reviewer who is not the translator] |
| Channel encoding budgets (SMS segment length, push character limit, email subject limit) | [OPEN: per channel, owner] |

## 8. Accessible copy

<!-- The evidence column and the walk itself belong to the accessibility
     checklist (../architecture/accessibility-checklist.md); this section
     states the content-level rules that checklist verifies. -->

- Link text makes sense read on its own, out of the sentence around it; never "click here" or "read more" with no named destination.
- Every image that carries meaning has alternative text stating that meaning; a decorative image is marked so a screen reader skips it.
- No instruction is given by colour or position alone ("the button on the right," "the red one"); pair it with a name or a label a screen reader also announces.
- Every input has a visible label; a placeholder is never the only label, because it disappears the moment the user starts typing.

## 9. Change log

| Date | Change | Owner |
|---|---|---|
| [ILLUSTRATIVE] YYYY-MM-DD | Guide created | [name] |
| | | |

---

## How this guide fails while looking complete

A voice-principles table filled with adjectives no competitor would ever disagree with, "friendly," "clear," "helpful," is not a decision; it is decoration, and a writer under deadline learns nothing from it that they did not already believe. The tell is a message-pattern section that restates the seed rows without a single product-specific "this product's decision" line filled in: a guide that never commits to inline-versus-submit validation, a banner persistence rule, or a reading-context table has not yet been used on a real screen. The other failure is silent drift: a glossary term that a new feature quietly renames without updating this file, so two words now mean the same thing in different parts of the product and support cannot tell users which one to trust.

## Exit gate (feeds Gate 2: requirements signed off)

Done when every box is honestly ticked. The agreed guide travels with the [design brief](design-brief.md) to [Gate 2](../../os/STAGE-GATES.md), and its message patterns become the standard [spec-review](../../skills/spec-review/SKILL.md) checks every new screen against.

- [ ] Section 1 names a real reading context per persona, not "all users"
- [ ] At most 4 voice principles, each with a do and a don't in the product's own words, none copied from a vendor voice guide
- [ ] Every message pattern in section 3 that this product ships has its own "this product's decision" line filled in, not left on the seed default
- [ ] The banned and preferred words table keeps every seed row and its Open Government Licence attribution intact
- [ ] Every glossary term has exactly one meaning and at least one "never use instead" entry
- [ ] Section 6 points to CLDR at run time; no hand-encoded locale table appears in this file
- [ ] Section 7 names a reviewer for every shipped language
- [ ] Section 8's rules are checked against the accessibility checklist's evidence, not asserted here alone
- [ ] Signed by the product owner and the content design lead, [names], [date]
