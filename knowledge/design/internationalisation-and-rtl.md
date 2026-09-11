---
layer: knowledge
stage: DESIGN
gate: 3
feeds: ["templates/architecture/localisation-rtl-checklist.md", "templates/definition/ux-writing-guide.md", "templates/delivery/edge-cases.md"]
method: ""
aliases: ["Internationalisation and RTL", "internationalisation-and-rtl", "RTL"]
---
# Internationalisation and Right to Left

This is an experience design card, about how a screen behaves for a right to left or multi script reader, not about the DESIGN stage this card feeds at Gate 3. Named attribution: the W3C Internationalization Activity (Richard Ishida, "Structural markup and right to left text in HTML"), the W3C Arabic Layout Task Force ("Arabic and Persian Layout Requirements", editor's draft), and the Unicode Consortium (UAX 9, cited only, and the CLDR project).

## The essence

Internationalisation is not translation. Translation swaps the words; internationalisation is the set of structural decisions, where direction lives, how numbers and dates format, which script renders, that have to be right before translation can even be tested. Get the structure wrong and a perfect translation still breaks, because the page reorders itself around the words instead of the words sitting correctly inside a page built for them.

The single fact worth carrying into every review: direction is a document level property, not a paint job. Right to left is not "left to right, flipped." Arabic, Persian and Urdu script joins letters, uses its own digit conventions in several markets, and reorders numbers and mixed language phrases by a real algorithm, not by mirroring a screenshot. A PM who treats RTL as a CSS toggle applied at the end will ship a page that looks correct in a static review and breaks the moment a real name, a real invoice number or a real date meets real user data.

## Where it came from

The W3C's Internationalization Activity has published implementation guidance on bidirectional text and markup since the early 2000s, written by engineers who worked the actual browser bug reports. Its Arabic Layout Task Force, part of the Internationalization Interest Group, later documented the layout requirements Arabic script imposes that Latin typography has no equivalent for, an editor's draft still being refined toward a formal Working Group Note. Both sit on top of the Unicode Consortium's Bidirectional Algorithm (UAX 9), the low level rule set that decides, character by character, which way a mixed direction line of text actually reads, and the Unicode Common Locale Data Repository (CLDR), the dataset every major platform's internationalisation library reads for how a given locale actually formats a number, a date or a currency amount.

## When to use it

- The product is launching or expanding into an Arabic, Persian, Urdu, Hebrew or other right to left market, or already serves one and has never had a structural RTL review.
- The product carries user generated or transactional content that mixes scripts and directions in the same string: a name, a reference number, an amount, a link, inside a sentence written the other way.
- A design system or component library is being adopted or built, and its overlay, dialog and menu behaviour under `dir="rtl"` has never been checked.

**Skip it when:** the product is single market, left to right only, with no dated expansion plan. Keep one habit anyway at no real cost, `dir="auto"` on free text fields, because it costs nothing today and removes one whole class of retrofit later.

## Direction is a document property, not a paint job

Set `dir="rtl"` on the `html` element for a right to left page, and set it there once. The W3C's own rule: never set base direction with CSS, and below the `html` tag only touch `dir` on the rare structural element whose own direction genuinely differs from the page. A stylesheet toggle that "flips" a layout with `direction: rtl` in CSS is solving the wrong layer of the problem; it can win a screenshot review and still leave every browser default, every form control and every assistive technology signal pointing the wrong way.

Three attributes carry the rest of the load:

- `dir="auto"` on inputs and on any block of inserted or user supplied text, so the browser reads the first strongly directional character and sets that element's direction from the content rather than from an assumption. This matters most exactly where a translator never touches the string: a support ticket, a comment thread, a chat message.
- `dirname` on a form field, so the direction the user actually typed in travels to the server with the rest of the form data, instead of being silently lost.
- Logical properties, `start` and `end`, in place of `left` and `right`, on margins, padding, alignment and anything else positional. A codebase written in logical properties flips for free when direction changes; a codebase written in physical properties needs every value re-audited by hand.

## The moment scripts actually meet: bidi isolation

Real screens mix directions inside a single sentence far more than a translated mock-up suggests: a bill reference, an IBAN, a URL, a person's name in Latin script, or a currency amount, sitting inside an Arabic or Urdu sentence. The Unicode Bidirectional Algorithm reorders text automatically, and since Unicode 6.3 it has offered directional isolate characters built for exactly this: wrapping an embedded opposite direction string so it renders correctly without letting its direction leak out and reorder the words around it (standard, Unicode UAX 9). HTML exposes the same idea through the `bdi` element and through `dir="auto"` on the wrapping block, so a forum thread mixing Urdu and English posts, or a single post mixing both, renders each piece in its own direction without corrupting the other.

The PM relevant instinct: any token that is not being translated, an ID, a reference number, a URL, a code, an amount, is a candidate for isolation the moment it can appear inside a right to left sentence. Skipping this is invisible in a design mock built from placeholder Latin text and painfully visible the first time a real Arabic sentence contains a real invoice number.

## Where RTL bugs actually hide: overlays and portals

A study of three actively maintained, MIT licensed component libraries (shadcn/ui at commit 3ba91b1, MUI Material UI at commit 5ce5a0f, Chakra UI at commit 67abe9f; paraphrased here, not quoted) found a shared foundation and then real differences in how far each goes. All three set direction the same way, with `dir` on `html` or a parent element. From there they diverge: shadcn and Chakra replace physical CSS utilities with logical `start` and `end` ones; MUI instead keeps physical CSS and flips it with a dedicated stylis RTL plugin (`@mui/stylis-plugin-rtl`), rewriting `left`/`right` at build time rather than authoring logical properties by hand. Only shadcn and MUI warn about the same portal failure, and both frame it more narrowly than "portals lose direction": content rendered through a portal, a dialog, a popover, a tooltip, a toast, a dropdown menu, escapes any `dir` set below the document root (MUI's own example sets `dir="rtl"` on a `Box` sub-element, not on `html`), and a headless library often reads direction from a JavaScript provider rather than the DOM, so an overlay can end up wrong even when `html` itself carries `dir` correctly. Chakra's RTL documentation carries no equivalent warning. Only shadcn documents flipping directional icons (`rtl:rotate-180`) and rewriting motion curves for RTL (`slide-in-from-right` becomes `slide-in-from-end`); MUI's guide instead covers the stylis plugin and its `/* @noflip */` escape hatch, and Chakra's guide covers neither. Chakra's own distinguishing feature is a locale aware `LocaleProvider`, for components whose behaviour, not only their layout, has to change with direction, such as which arrow key advances a slider.

For a product shipping into an Arabic, Urdu or Persian market, this is the concrete acceptance test a spec should name explicitly: every overlay surface, every dialog, every toast, every menu, every tooltip, gets its own RTL check, because the base page passing tells you nothing about whether the overlay layer did.

## What mirrors and what does not

Paraphrased here with attribution, from Google's Material Design guidance on bidirectionality; its content licence was not confirmed for this repository, so this is a paraphrase only, with no reproduced imagery. The general shape mirrors: page layout, the order of primary navigation, and icons whose meaning depends on reading direction, a "next" chevron, a back arrow, a non-media progress indicator implying an order to read in (a step tracker, a loading bar tied to reading order, not a media scrubber, see below). The general shape does not mirror: numbers and their internal digit order, text left in another, untranslated direction such as a URL or a piece of code, icons tied to a real world referent rather than reading direction, a clock face, a refresh icon (clockwise) or a history icon (counterclockwise), circular time is not mirrored even though linear time is, a picture of a physical object such as a keyboard, media playback controls and the media progress bar, which follow the direction of the tape rather than the direction of time, and the search icon, whose handle placement follows handedness rather than reading direction. Treat this as a starting checklist, not a law: it is platform convention rather than a technical requirement, and the right call for a specific icon in a specific product is worth testing with a native reader rather than assumed from the list.

## Digits are not determined by the language

Arabic script markets use three separate digit families, and W3C's Arabic Layout Task Force is explicit that the common shorthand for them is unreliable. European numerals (0123456789, the same shapes used in English) are one family. Arabic-Indic numerals (٠١٢٣٤٥٦٧٨٩) are a second, historically associated with Mashriq countries such as Egypt, Saudi Arabia and Iraq. Extended Arabic-Indic numerals, also called Eastern Arabic-Indic numerals (۰۱۲۳۴۵۶۷۸۹), are a third, associated with Iran and Afghanistan. The term "Eastern Arabic numerals" on its own is genuinely ambiguous in practice, used inconsistently for either of the last two sets, and alreq recommends avoiding it; ask a vendor or a translator which Unicode range they mean rather than trusting that label alone (standard, W3C alreq).

The two non-European digit families also carry different Unicode bidirectional categories from each other, Arabic-Indic digits are category AN, Extended Arabic-Indic and European digits are both category EN, which is why the same number can reorder differently depending on which digit set a market actually uses, a detail that only shows up with real numbers in a real sentence, never in a static mock.

Do not guess a market's default digit set from its language code; check it, and let a user override it. A locale by locale default is exactly what the platform's own internationalisation library already knows: this table is a directly checked sample against CLDR 48 data through ICU 78.2 (standard; Unicode CLDR), not a bundled data extract, since this repository has not verified the CLDR data licence for redistribution and does not reproduce a full locale table here.

| Locale | Default digit set |
|---|---|
| ar-SA, ar-EG | Arabic-Indic |
| ar, ar-AE, ar-MA | European (Latin) |
| ur, ur-PK | European (Latin) |
| fa-IR | Extended Arabic-Indic |

Note the trap inside the table itself: `ar` alone, and Gulf Arabic in the UAE, default to the same European digits an English speaking designer already expects, while Egypt and Saudi Arabia do not, and Urdu markets default to European digits too even though the script itself is right to left. There is no shortcut that reads the digit set off the language name.

## Script matters as much as direction: Nasta'liq for Urdu

Direction is only half the typography question. Nasta'liq remains the preferred calligraphic style for Urdu in Pakistan and for Persian in Iran, distinct from the Naskh style that has become the default form of most digital Arabic typography (standard, W3C alreq). A font stack chosen only for Arabic-script coverage in general can render Urdu technically but in a style Urdu readers experience as foreign or low quality. This has three concrete consequences for a spec: font fallback has to be tested with actual Urdu text, not assumed from an Arabic sample; Nasta'liq's characteristic diagonal flow needs materially more line height than a Naskh-style font at the same point size, so a layout tuned against Arabic line height will clip or crowd Urdu text; and diacritical marks, where used, need vertical space the layout has to reserve rather than discover in production.

## Calendars and currency: never a hand rolled table

Calendar, date and currency formatting vary by locale in ways too numerous and too easily wrong to encode by hand, comma or period as the decimal separator, thousands grouping, which calendar a date is expressed in. The checked sample above already shows one concrete case: fa-IR defaults to the Solar Hijri calendar, not Gregorian, alongside its Extended Arabic-Indic digits (standard, checked against CLDR 48 via ICU 78.2). The same alreq source documents a separator split for European digits specifically: with European digits, Western Arabic-speaking regions such as Morocco use a period for thousands and a comma for decimals, and Eastern Arabic-speaking regions use the reverse (standard, W3C alreq; ar-MA checked against CLDR 48 via ICU 78.2). alreq does not extend this split to Arabic-Indic numerals; it says those use their own dedicated separators, U+066B ARABIC DECIMAL SEPARATOR and U+066C ARABIC THOUSANDS SEPARATOR, regardless of Western or Eastern region. Checked directly against CLDR 48 through ICU 78.2, ar-SA and ar-EG format 1234567.89 as ١٬٢٣٤٬٥٦٧٫٨٩ using those Arabic separators, ar-AE as 1,234,567.89, and ar-MA as 1.234.567,89, so applying the period-thousands, comma-decimal rule to ar-SA or ar-EG is exactly the mistake the digit-set table above already warns against: those two locales default to Arabic-Indic digits, not European ones. The instruction this card gives is not a table to memorise, it is a rule: read this from CLDR or from the platform's ICU backed formatting library at run time, never encode a currency or date format by hand, and never assume Gregorian.

## Budget for length and content you have not measured yet

A layout designed and pixel checked only against English strings has been tested against one of the more compact ways many of these ideas can be expressed, not against the string that will actually ship in Arabic, Persian or Urdu. Two habits catch this before a translator does: budget generously for the string that runs longest, then verify with real translated copy rather than filler text, since Arabic script glyphs join and change width in ways placeholder Latin text cannot simulate; and pseudo-localise before a real translation exists, a testing technique that programmatically transforms strings, lengthening them, wrapping them in accent marks or bracket characters, sometimes reversing them, to surface hardcoded strings, truncation, and layout assumptions early, without waiting on an actual translation pass.

## Two constraints worth asking about before they surprise you

Two questions belong on every internationalisation review and are easy to miss because they sit outside the UI layer entirely.

First, channel encoding. Any product that sends transactional content over SMS or a similarly narrow channel needs to ask its messaging vendor, explicitly, how the character encoding for this script changes the per message budget. Latin text usually fits the GSM-7 alphabet, the compact 7-bit encoding SMS defaults to; Arabic-script text, along with most other non-Latin scripts, falls back to UCS-2, a 16-bit encoding that fits far fewer characters into a single segment and a single concatenated message. Ask the vendor for its documented single-segment and concatenated-message character budgets for both encodings, for the specific script in question; do not carry over an assumption from an English language message, and this card gives no specific character counts, since those belong to the vendor's own documentation, not to a general claim here.

Second, screen reader voice switching. The `lang` attribute, on `html` and on any nested element whose language differs from its parent, is what lets assistive technology switch pronunciation engine and pick correct hyphenation rules; it is a separate signal from `dir`, which only controls layout, and both belong on the same element when a page or a block genuinely changes language. This card makes no claim about the quality of Urdu text to speech specifically; that has not been researched here, and a product depending on it should test with the actual assistive technology its users run rather than assume the `lang` attribute alone settles the question.

## Questions a PM must ask

- Is `dir` set once, on `html`, and inherited from there, or is a stylesheet faking direction somewhere in the codebase?
- Does every overlay, dialog, toast, dropdown menu and tooltip in the design system carry correct direction on its own, or only the base page that was screenshotted for review?
- Where does user entered or third party text sit inside a sentence written the other way, and has bidi isolation actually been applied there?
- Which digit set does this specific locale default to, and can a user change it?
- Which script and typeface renders this language, and has font fallback been tested with real text in that language, not a Latin placeholder?
- Which calendar does this locale expect, and where in the product is Gregorian still hardcoded?
- Has the string catalog been checked for concatenated fragments that assume English word order and English pluralisation?
- Has this screen been pseudo-localised, so a longer, accented, direction-shifted string has actually rendered in it, not only a translated one?
- If this ships over SMS or another narrow channel, has the vendor confirmed what this script does to the per message character budget?
- Does every text bearing element carry a correct `lang` attribute, so assistive technology pronounces it correctly?

## The trap: translate at the end

The trap has a name teams say out loud: "we will translate before launch." It treats internationalisation as a coat of paint applied once the English design is finished and locked, and it fails for a structural reason, not a scheduling one. Direction is architectural: `dir` belongs on `html` and threads through the render layer, and retrofitting a shipped codebase from physical to logical positioning touches every component that ever hardcoded left or right. Length assumptions get baked into layouts that were only ever measured against English strings, so a late pass discovers truncation, overlap and clipped diacritics everywhere at once instead of catching one component at a time during design. Worst of all, the string catalog itself is often unusable by the time anyone looks: a sentence assembled from fragments, "You have " plus a count plus " new messages", assumes an English word order and an English two-way plural rule that a language with different grammar, different agreement, or more plural forms cannot simply be dropped into.

The tell that a team is in this trap: the roadmap carries a single late card labelled "RTL support" or "translate strings," with no earlier card for markup and logical properties, no earlier review of the string catalog's grammar, and no time budgeted for a native reader to check real, not placeholder, content before ship.

## How it lies

The honest weakness sits in what a review checks because it is cheap to check. A document level `dir` attribute and a mirrored layout are the necessary first move, and they are also the easiest part of this whole area to verify: take one screenshot of a translated page, in a right to left layout, and confirm it looks correct. A review that stops there is checking the frame, not the content, and the defects that actually reach users hide in exactly the parts a static screenshot never exercises: content a user typed rather than a translator, a Latin order number or IBAN sitting inside an Arabic sentence, a number rendered in the locale's real default digit set rather than the designer's test data, and an overlay, dialog or third party embed that only appears on interaction and was never part of the reviewed screen at all. An RTL screenshot review can pass cleanly while every one of those still breaks in production, because it tested a static frame built from clean data, not the live data the product actually carries.

## Where it sits in the loop

- Stage: DESIGN, feeding [Gate 3: Architecture and risks reviewed](../../os/STAGE-GATES.md), which closes DESIGN and feeds BUILD.
- Upstream: which markets and which scripts matter is a DISCOVER and DEFINE question, set by [personas](../../templates/discovery/personas.md) and by market sizing work in the [frameworks layer](../../frameworks/strategy/market-sizing.md); this card starts once a right to left or multi script market is already on the table.
- Downstream: [the localisation and RTL checklist](../../templates/architecture/localisation-rtl-checklist.md) turns every section above into a walkable pass, [the UX writing guide](../../templates/definition/ux-writing-guide.md) is the standard every string is audited against, including the concatenation trap described above, and [edge cases](../../templates/delivery/edge-cases.md) is where mixed direction content, live user data and portal overlays belong as named hunting list entries, never left implicit.
- On trial at Gate 3 alongside the rest of the architecture review; a product shipping into a right to left market with no named RTL entry in its risk register is exactly the kind of gap that gate exists to catch.

## Used by

- [Localisation and RTL checklist](../../templates/architecture/localisation-rtl-checklist.md)
- [UX writing guide](../../templates/definition/ux-writing-guide.md)
- [Edge cases](../../templates/delivery/edge-cases.md)
- [Experience Design Index](README.md)

## Reading

- [Structural markup and right to left text in HTML](https://www.w3.org/International/questions/qa-html-dir), Richard Ishida, W3C Internationalization Activity. Reuse class: paraphrase with attribution. Its rules about setting base direction on the html element and never in CSS are stated as fact and restated here in this card's own words.
- [Arabic and Persian Layout Requirements](https://w3c.github.io/alreq/), W3C Arabic Layout Task Force, editor's draft. Reuse class: paraphrase with attribution; its digit set terminology may be quoted directly, which this card does for the family names only.
- [UAX 9: Unicode Bidirectional Algorithm](https://www.unicode.org/reports/tr9/), Unicode Consortium. Reuse class: cite only, under the Unicode Terms of Use; no text reproduced beyond the standard's own defined terms.
- [Unicode CLDR Project](https://cldr.unicode.org/index), Unicode Consortium. Reuse class: cite only for the project itself; the locale table above is a directly checked sample against CLDR 48 through ICU 78.2, not a bundled extract, because this repository has not separately verified the CLDR data licence for redistribution.
- [Bidirectionality](https://m2.material.io/design/usability/bidirectionality.html), Google, Material Design 2. Reuse class: paraphrase with attribution only; the guideline prose's licence was not confirmed for this repository, and its do and don't imagery is not reproduced here.
- shadcn/ui at commit 3ba91b1, MIT licence; MUI Material UI at commit 5ce5a0f, MIT licence; Chakra UI at commit 67abe9f, MIT licence. Reuse class: paraphrase with attribution; a repository study of how three actively maintained, permissively licensed component libraries implement direction and where each documents portal content failing to inherit it.

See also [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md) for the full source and licence register this card's Reading section draws its reuse classes from.
