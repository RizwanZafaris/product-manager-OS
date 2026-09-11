---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["templates/architecture/design-review-record.md", "templates/definition/ux-writing-guide.md", "templates/architecture/localisation-rtl-checklist.md"]
method: "knowledge/design/content-design-and-forms.md"
aliases: ["Content and Microcopy Audit", "content-microcopy-audit"]
---
# Content and microcopy audit

Based on the content design guidance published by the Government Digital Service on GOV.UK (ongoing) and the error message and confirmation dialog research summarized by the Nielsen Norman Group. Explained here in this repository's own words.

## What it is for

A content and microcopy audit walks every user facing string on a screen, in every state that screen can be in, against a fixed set of yes or no rules: does the string say what happened, does it say how to fix it, does it avoid a closed list of banned words, does it avoid blaming the user, is a confirmation step used only where the action is serious or irreversible, does the term match the product's own glossary, does the string fit the channel it ships on, and is it formatted for the reader's locale. [GOV.UK's content design guidance](https://www.gov.uk/guidance/content-design/what-is-content-design) starts from the same premise: content exists to meet a user need, not to fill a screen, and it stays accountable to a house style rather than to whoever wrote it last. The audit turns that premise into a pass or fail per string instead of a feeling that the copy "reads fine." It closes the DESIGN stage gap where a screen has been reviewed for layout and never for what it actually tells the person using it.

## Run it when

- Before Gate 3, on every screen and flow in the release that carries new or changed user facing text.
- After a copy pass that touched error, empty, loading, or confirmation states, because these are the states most likely to carry the banned words the audit checks for.
- Before a string set goes to translation, because the audit is cheaper to run once on the source language and once on each target language than to discover a translated blame word in production.

**Skip it when:** fewer than five strings changed since the last audit on this screen, and none of the changed strings sit in an error, confirmation, empty, SMS, or USSD state. Log the exception and the reason in the design review record; do not silently skip a screen because the change looked small, because a one-word edit to an error message is exactly the kind of change that reintroduces a banned word, and this skip rule exists to catch low-risk default-state edits, not the states most likely to carry one.

## Inputs you need first

- The product's design brief, in particular [section 6, Deliverables](../../templates/definition/design-brief.md#6-deliverables): the screens, flows, and fidelity levels this audit inventories against.
- The product's writing guide, for its glossary of approved terms and its own banned word list, layered on top of the house list below.
- The channel plan for each string: in-app screen, push notification, email, SMS, or USSD, because the channel sets the character limit and the encoding.
- The confirmation inventory from the design brief or the ADRs: which actions the product already treats as serious or irreversible.

## The worksheet

### 1. Inventory every string by screen and state

List every string the screen shows, once per state that screen can be in. Take the state list straight from [ui-state-inventory.md](../../templates/definition/ui-state-inventory.md) rather than maintaining a second one: it is the single owner of which states a screen or component must render (for example default, loading, empty, error, success, confirmation), and every screen named in the design brief's [section 6 deliverables table](../../templates/definition/design-brief.md#6-deliverables) gets one inventory row here per state the inventory lists for it. A screen with five states and three strings per state is fifteen inventory rows, not three.

| String ID | Screen (design brief deliverable) | State | Channel | Current text | Owner |
|---|---|---|---|---|---|
| | | | | | |

### 2. Per string, run the rule check

For every row from step 1, answer each rule yes or no. A string that cannot honestly be marked yes is a fail on that rule, whatever the deadline says.

| Rule | What it checks | Pass means |
|---|---|---|
| States what happened | The string names the event, not a code or a generic label | "The date must be in the past", not "Error 0x004" |
| States how to fix | The string tells the reader the next action | "Enter a National Insurance number in the correct format" |
| No banned word | The string avoids the list below | Neither the house list nor the product's own list is present |
| No blame | The string does not accuse the reader of an error they did not knowingly make | No "you forgot", no implied fault for a system failure |
| Confirmation gated correctly | A confirmation step appears only for a serious or irreversible action, and the reversible ones offer undo instead | See the confirmation rule below |
| Terminology matches the glossary | The term used matches the product's writing guide glossary, not a synonym | "Freeze", never "lock" and "freeze" for the same action |
| Fits the channel limit | The string fits inside the character budget computed for its channel and encoding | See the channel arithmetic below |
| Expansion headroom | The layout or channel budget leaves the stated headroom percentage for translation growth | See the headroom convention below |
| Locale formatting via CLDR | Dates, numbers, and currency are formatted from the reader's locale data, never hard coded to one locale | A date renders as the reader's locale expects, not as the source locale wrote it |

**No banned word, the house list.** Adapted under the Open Government Licence v3.0 from the [GOV.UK Design System's error message guidance](https://design-system.service.gov.uk/components/error-message/) (evidence class: platform convention). Do not use:

- technical jargon such as "form post error", "unspecified error", or an internal error code shown as-is
- "forbidden", "illegal", "you forgot", or "prohibited"
- "please", because it implies the action is optional
- "sorry", because it does not help the reader fix the problem
- "valid" or "invalid", because they add nothing to the message
- humorous or informal language such as "oops"

Layer the product's own banned word list from its writing guide on top of this one; the two lists are checked together as a single yes or no per string. Jakob Nielsen, ["Error Message Guidelines"](https://www.nngroup.com/articles/error-message-guidelines/) (Nielsen Norman Group, 2001; evidence class: practitioner heuristic), recommends a positive, specific, non-blaming tone as what makes an error message actually get read and acted on.

**Confirmation gated correctly.** Per Jakob Nielsen, ["Confirmation Dialogs Can Prevent User Errors (If Not Overused)"](https://www.nngroup.com/articles/confirmation-dialog/) (Nielsen Norman Group, 2018; evidence class: practitioner heuristic), a confirmation step earns its place only when the consequence is serious or hard to reverse; on routine or frequent actions it becomes a habitual click-through and stops preventing anything. Mark this rule pass when a confirmation appears on an action the design brief or an ADR has named serious or irreversible, and mark it pass when a reversible action skips confirmation in favor of an undo affordance instead. Mark it fail in both directions: a missing confirmation on an irreversible action, and a confirmation dialog defending a reversible one.

**Channel arithmetic, character limit.** Compute the limit per script and encoding, never assume the Latin-script limit applies everywhere:

- GSM-7 encoding (Latin scripts the standard covers): 160 characters in a single SMS, 153 characters per segment once the message is split across segments (the segment headers cost 7 characters each).
- UCS-2 encoding (scripts GSM-7 does not cover, including Urdu and Arabic): 70 characters in a single SMS, 67 characters per segment.
- USSD: 182 characters per page in GSM-7 is the theoretical ceiling (standard-derived, 3GPP TS 23.038 and TS 23.090: 182 GSM-7 characters packed into a 160-octet payload), roughly 80 characters in UCS-2; most operator gateways enforce a lower figure in practice, commonly 160. Design to 160 as the safe default and confirm the actual figure with the gateway contract before relying on anything closer to the theoretical maximum (evidence class: vendor claim, confirm per integration).

A string that needs more than one segment to send is a fail on this rule unless the flow is explicitly designed as a multi-page message, because a silent truncation at the encoding boundary is how half an error message ships.

**Expansion headroom convention.** Reserve headroom against the source-language character count before the layout or the channel budget is locked: a stated convention is 30 percent for most Western European target languages (evidence class: practitioner heuristic; confirm per target language, because some target languages contract rather than expand). For non-Latin, UCS-2 target languages such as Urdu and Arabic, the 30 percent figure is not validated and script density does not scale linearly with source character count; use it only as a rough pre-translation estimate, and re-check the actual measured length of the drafted translation before signing off, never the multiplied estimate alone. Mark the rule fail when the layout has no room to grow, whatever the source-language string currently measures.

**Locale formatting via CLDR.** Dates, numbers, currency, and list separators are drawn from [Unicode CLDR](https://cldr.unicode.org/) locale data for the reader's locale rather than hard coded to the string's source locale (evidence class: standard). A date field that always renders day-month-year is a fail on this rule for any reader whose locale expects month-day-year, even if the string itself passes every other rule.

### 3. Score it

Pass rate per rule, over the inventory from step 1:

```
pass rate (rule) = passing strings applicable to that rule / applicable strings for that rule
```

A rule is not applicable to a string when the rule cannot fail for that string's channel or state; for example the SMS channel limit rule does not apply to an in-app modal string. A row still marked open (not yet reviewed against a rule) is excluded from that rule's denominator too, for every rule, until it is reviewed; an open row is neither a pass nor a fail and counting it as applicable inflates or deflates the rate depending on which way you round it. Compute one pass rate per rule, not one blended score for the screen, because a screen that is perfect on banned words and failing on channel limit needs a different fix than the reverse.

Alongside the pass rates, keep a fail list: every row that failed at least one rule, which rule it failed, the fix, and an owner.

| String ID | Rule failed | Fix | Owner | Due |
|---|---|---|---|---|
| | | | | |

## Reading the result

A rule with a pass rate near 100 percent across every screen means the writing guide is doing its job and the audit is mostly confirming, not catching. A rule that fails repeatedly on one screen, rather than scattered across many, usually means that screen's copy was written before the glossary existed or before the channel was decided, not that the writer is careless. Read the fail list by rule before reading it by screen: three screens failing "no banned word" on the same phrase is one fix to the source string, not three separate reviews. Bring the pass rates and the fail list to the design review record; a screen with an open fail row on the confirmation rule or the channel limit rule is not ready for Gate 3, because both of those failures ship as either a destructive action with no warning or a message the reader never receives in full.

## ILLUSTRATIVE example

Invented, for a card freeze flow in a fictional wallet product, a different invented product from the worked Sahulat example elsewhere in this repository. Four strings audited across two states, in-app and SMS, English source with an Urdu translation queued.

| String ID | Screen | State | Channel | Current text | States what happened | States how to fix | No banned word | No blame | Confirmation gated correctly | Terminology matches glossary | Fits channel limit | Expansion headroom | Locale CLDR | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | Freeze card | confirmation | in-app | "Are you sure you want to freeze this card?" | fail | fail | pass | pass | fail (freezing is reversible in this product; a confirmation dialog defending a reversible action fails this rule, and this string carries no undo at all) | fail (glossary uses "pause", not "freeze") | pass | pass | n/a | fail |
| F2 | Freeze card | error | in-app | "Sorry, invalid card number. Please try again." | fail | fail | fail ("sorry", "invalid", "please") | fail (implies the reader is at fault for a lookup failure) | n/a | pass | pass | pass | n/a | fail |
| F3 | Freeze card | success | SMS | "Card ending 4471 paused. Unpause any time in the app." | pass | pass | pass | pass | n/a | pass | pass, 53 characters, GSM-7 single segment | 53 x 1.3 = 68.9, a rough pre-translation sanity check against the 70-character UCS-2 budget; the 30 percent figure is a Western European convention applied here only as a coarse estimate, not a validated ratio for Urdu | n/a | pass |
| F4 | Freeze card | success (Urdu) | SMS | Urdu equivalent of F3, drafted, not yet reviewed | open | open | open | open | n/a | open | fail, UCS-2 at 70-character limit and the draft runs to 74 characters | n/a | open | fail |

Pass rate on "states what happened": 1 of 3 applicable strings (F4 excluded as unreviewed), 33 percent. Pass rate on "no banned word": 2 of 3 applicable strings (F4 excluded as unreviewed), 67 percent. F3's headroom figure only borrows the 30 percent convention as a coarse pre-translation estimate; the actual gate is F4, checked directly against the queued Urdu translation's own channel and encoding once it exists. Applying a Western European expansion ratio by multiplication is a rough heuristic for any non-Latin, UCS-2 target language, not a substitute for measuring the drafted translation, which is exactly why F4 fails on its own measured length rather than being waved through on the F3 estimate.

Fail list, in the step 3 format:

| String ID | Rule failed | Fix | Owner | Due |
|---|---|---|---|---|
| F1 | States what happened | Name the action's effect instead of asking a bare yes-or-no question | glossary owner | before Gate 3 |
| F1 | States how to fix | N/A once the confirmation dialog is dropped in favor of undo; if any string remains, it must name the next action | glossary owner | before Gate 3 |
| F1 | Confirmation gated correctly | Drop the confirmation dialog; freezing is reversible, so ship "Card frozen" immediately with an undo affordance instead | glossary owner | before Gate 3 |
| F1 | Terminology matches glossary | Swap "freeze" for "pause" everywhere on this screen, or change the glossary and rewrite everywhere else it diverges | glossary owner | before Gate 3 |
| F2 | States what happened | Name the specific problem with the card number, not a generic "invalid" | content owner | before Gate 3 |
| F2 | States how to fix | Tell the reader the correct format or the next action | content owner | before Gate 3 |
| F2 | No banned word | Rewrite past "sorry", "invalid", and "please" using the house list | content owner | before Gate 3 |
| F2 | No blame | Rewrite so the string does not imply the reader is at fault for a lookup failure | content owner | before Gate 3 |
| F4 | Fits channel limit | Cut to fit the 70-character UCS-2 single-segment budget, then re-run every rule on the shipped translation | localisation lead | before Gate 3 |

## The trap

Auditing the English strings and shipping the translations unaudited. A screen that passes every rule in its source language still ships a blame word, a broken confirmation gate, or a truncated SMS in a target language nobody re-checked, because a translation is not a pass-through of an already-audited string, it is a new string that happens to carry the same meaning. Run step 2 again on every shipped translation, not only on the source language draft; F4 in the example above is exactly this trap caught before it shipped rather than after.

## Feeds

- [Design review record](../../templates/architecture/design-review-record.md): the fail list and pass rates are the evidence line for any screen under review
- [UX writing guide](../../templates/definition/ux-writing-guide.md): the product's own banned word list and glossary that this audit checks strings against
- [Localisation and RTL checklist](../../templates/architecture/localisation-rtl-checklist.md): the expansion headroom and CLDR formatting rows carry forward into the localisation sign-off
- DESIGN, feeding [Gate 3: Architecture and risks reviewed](../../os/STAGE-GATES.md)
- Method background: [Content design and forms](../../knowledge/design/content-design-and-forms.md)
- Worked fill: [Sahulat content and microcopy audit example](../../examples/sahulat-content-microcopy-audit.md)
