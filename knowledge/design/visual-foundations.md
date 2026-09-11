---
layer: knowledge
stage: DESIGN
gate: 3
feeds: ["templates/architecture/design-review-record.md", "templates/architecture/accessibility-checklist.md", "templates/definition/nfr.md"]
method: ""
aliases: ["Visual Foundations", "visual-foundations"]
---
# Visual Foundations

Grounded in WCAG 2.2 and the W3C's own status notes on WCAG 3.0, in platform conventions published by Apple, Google Material and the UK Government Digital Service, in practitioner heuristics from the Nielsen Norman Group and the Baymard Institute, and in the research literature on contrast derivation, print size and colour vision (Legge and Bigelow, 2011; Birch, 2012; Piepenbrock et al., 2013). Explained here in this repository's own words, with every number kept next to the authority that stands behind it.

## The essence

A product manager reviewing a screen hears four sentences wearing the same grammar. "Text needs 4.5 to 1 contrast" is a legal minimum. "Buttons sit on an 8 point grid" is a practitioner's habit. "Animations run 100 to 500 milliseconds" is a rule of thumb from usability testing. "Body text reads best at 50 to 75 characters" is an institute's field observation with no published method behind it. All four arrive in the same confident tone, and treating them as if they carried the same weight is the single most common failure in experience design review: a team ships a screen that fails a real legal threshold while proudly quoting a heuristic nobody measured, because nobody in the room asked which kind of sentence they were looking at.

This card exists to let a PM ask that question fast. Every number below carries an evidence class:

| Evidence class | What it means | Example |
|---|---|---|
| Standard | A normative WCAG success criterion, with its conformance level (A, AA or AAA) named | 1.4.3 Contrast (Minimum), AA |
| Platform convention | A figure a major platform or design system has adopted and documented, without controlled research behind that specific figure | Apple's 44 by 44 pt control size |
| Practitioner heuristic | A range a practice publishes from observation, with a stated rationale that is not a controlled study | NN/g's 100 to 500 millisecond animation range |
| Research evidence | A peer reviewed or peer reviewable finding, cited to the study itself rather than a summary of it | Legge and Bigelow's angular print size range |
| Vendor claim | A figure published by the party who stands to benefit from its adoption; useful as a design aid, never as a conformance basis | APCA's Lc contrast thresholds |
| Aesthetic convention | A proportion chosen for how it looks, carrying no readability claim at all | A golden ratio type scale |

A standard passing does not mean a screen is legible, and a heuristic failing does not mean a screen is broken. The two facts sit on different axes: legal exposure runs through the standard column alone, and craft quality runs through all six. Confusing the columns produces both of the repository's most common design-review failures: a team that treats a heuristic as a blocker it is not, and a team that treats a standard as a suggestion it is not.

## Where it came from

These numbers never had one author. The W3C's Accessibility Guidelines Working Group standardises a small set of testable thresholds through public review and eventual normative publication, which is why WCAG numbers carry legal weight in the jurisdictions that reference them and why they change slowly. Platform vendors, Apple and Google chief among them, publish their own conventions for their own ecosystems: fast to update, binding only within that platform, and rarely defended with a citation because the vendor is also the implementer. Practitioner firms such as the Nielsen Norman Group and the Baymard Institute sit between the two: they publish observational guidance from usability testing and field research because controlled academic studies are too slow for a product team's decision cadence, and they say so, which is more honest than it sounds. Academic vision science, Legge and Bigelow on print size, Birch on colour vision deficiency prevalence, moves slower still and almost never reaches a product team directly; it arrives secondhand, filtered through whichever practitioner article cited it, which is exactly why this card cites the primary study by name wherever one exists rather than the article that mentioned it.

WCAG's own contrast threshold is worth reading once as a case study in how a standard actually gets its number, because most PMs assume 4.5 to 1 was measured as an optimum and it was not. The derivation starts from a 3 to 1 minimum contrast published in ISO 9241-3 and ANSI/HFES 100-1988 for people with normal vision, then multiplies by roughly 1.5 because someone with 20/40 acuity carries about 1.5 times the contrast-sensitivity loss of normal vision, following Arditi and Faye's work on low-vision reading. The same multiplier logic produces roughly 7 to 1 for 20/80 acuity, which is why 1.4.6, the AAA-level enhanced contrast criterion, lands there. The number is a normative threshold built from a chain of derivations, not a measured readability optimum, which is why passing it is necessary and not sufficient.

## When to use it

- Reviewing a screen, a flow or a design brief before Gate 3, when a number is being quoted as a requirement and nobody has said which authority stands behind it.
- Filling section 5 of [nfr.md](../../templates/definition/nfr.md) or walking the [accessibility checklist](../../templates/architecture/accessibility-checklist.md), where a conformance target has to be named precisely rather than asserted as "accessible."
- Settling a disagreement between a PM and a design lead about whether a number is negotiable: a standard is not a design lead's call to waive alone, and a heuristic is not a PM's call to mandate alone.
- Writing the constraints section of a design brief, so "uses the design system" is not the only accessibility-adjacent line in the document.

**Skip it when:** the product already has an adopted design system whose own documentation states these values for this product. Read that document first; this card explains the authorities behind any design system's choices, and it is not a substitute for the system a team has actually agreed to run. It is also the wrong tool for choosing a brand palette, a typeface, an illustration style or any other decision that is taste rather than legibility; those decisions belong to the named designer, in full, and this card says so directly in the trap below.

## Contrast

The number a PM quotes most often, and the one most often quoted for the wrong level.

| Rule | Authority | Level | Evidence class | Source |
|---|---|---|---|---|
| Text contrast at least 4.5 to 1; large-scale text (roughly 18pt regular or 14pt bold and larger) at least 3 to 1 | WCAG 2.2, 1.4.3 Contrast (Minimum) | AA | Standard | W3C, Understanding SC 1.4.3 |
| Non-text contrast at least 3 to 1 for UI component boundaries and states, focus indicators, and graphic parts needed to understand content such as chart marks; inactive controls and unmodified browser defaults are exempt | WCAG 2.2, 1.4.11 Non-text Contrast | AA | Standard | W3C, Understanding SC 1.4.11 |
| Colour is never the only means of conveying information, indicating an action, prompting a response or distinguishing an element | WCAG 2.2, 1.4.1 Use of Color | A | Standard | W3C, Understanding SC 1.4.1 |
| Grade difference of 40 or more between two colours meets AA large text, 50 or more meets AA text (or AAA large text), 70 or more meets AAA | USWDS colour token naming ("the magic number") | Maps to the standard above | Platform convention | U.S. General Services Administration |

W3C's own worked examples for 1.4.1 are a red error label and a chart whose series are told apart only by colour, both common in product screens and both easy to miss because they look like normal styling rather than a violation. A checked contrast box with no measured value beside it is a claim, not a check: the accessibility checklist's own instruction to walk every state with a contrast tool exists because a component that passes in its default state routinely fails on hover, on a disabled state or on a coloured background variant nobody measured.

One caution worth stating plainly: 4.5 to 1 is a threshold, not a readability optimum. A pair of colours can clear it and still be hard to read, particularly a thin font weight, a small size, or a near-black pair where the ratio math behaves counterintuitively (see the next section). Passing is a floor a team must clear, not a ceiling that proves a screen is legible.

## WCAG 2 and APCA

Status as of 2026-09-10. This is not legal advice; confirm any conformance decision with counsel before it reaches a contract or a compliance filing. Re-check trigger: any new WCAG 3.0 Working Draft, since the contrast algorithm itself is explicitly unsettled.

The WCAG 3.0 Working Draft states outright that "the contrast algorithm used in WCAG 3 is yet to be determined." Its own glossary marks the contrast-ratio test Exploratory and the text-contrast requirement Developing, with a placeholder standing in for the measure. The draft's own status section calls citing it as anything other than a work in progress inappropriate, so nothing in this card, and nothing a team ships, should treat WCAG 3 contrast language as settled.

The Accessible Perceptual Contrast Algorithm, published by Myndex Research's Andrew Somers, is the best-known challenger. Its author's technical critique of the WCAG 2 ratio is specific and worth taking seriously: the ratio is not perceptually uniform, it overstates contrast for dark colour pairs so a 4.5 to 1 pair near black can still be hard to read, it treats foreground and background symmetrically when perception does not, and it ignores font size and weight entirely. That is a credible critique from the person with the largest stake in its being believed, which is not the same as a settled finding. The Accessibility Guidelines Working Group's own contrast subgroup has said APCA needs extensive peer review from other colour-contrast researchers before adoption; APCA's author answers that peer review was never in his charter and lists reviews he considers sufficient. APCA has been in public beta since February 2021, was pulled from the July 2023 WCAG 3 draft for lack of working-group support, and as of April 2026 was still not the algorithm WCAG 3 names. APCA's own author has agreed publicly that nobody should drop WCAG 2 conformance on the strength of a draft.

The legal-risk rule this repository follows: conform to WCAG 2.x, because the accessibility laws that reference a standard reference WCAG 2.x, not WCAG 3 and not APCA. APCA may be used as a secondary design aid inside a team's own process, never as the conformance basis a gate signs against. Two further restrictions apply if a team wants to use it at all: APCA's code and documentation are copyrighted and marked all rights reserved, and the name "APCA" may describe only a correctly implemented, maintained and up to date implementation, so this repository never vendors APCA code and never names a check "APCA." Apple's Human Interface Guidelines describe both WCAG and APCA as widely used ways to measure contrast, which is a platform's editorial choice of words, not a standardisation event; Apple's own Accessibility Inspector tool checks WCAG AA values, 4.5 to 1 for text up to 17pt and 3 to 1 at 18pt or bold, which is the more reliable signal of what actually gets enforced.

APCA's author publishes his own thresholds on a lightness-contrast scale running roughly Lc 0 to 106: Lc 90 preferred for body text at 14px weight 400 or larger, Lc 75 as a minimum for that same body text, Lc 60 for other readable text (24px regular or 16px bold), Lc 45 for headlines (36px regular or 24px bold), and Lc 15 sitting near invisibility. These are the vendor's own author guidance, not a standard, and belong in a design system's internal notes at most, never in a conformance statement.

## Colour vision deficiency

Inherited red-green colour vision deficiency affects roughly 8 percent of men of European descent and about 0.4 percent of women, per the Birch (2012) population survey, and 4 to 6.5 percent of men in Chinese and Japanese populations, the same paper's figure for those populations. This is research evidence, and the number is population-dependent: 8 percent of men is the European Caucasian figure specifically, not a global constant, and a product shipping into a market this repository's domain cards cover, South Asia, MENA, East Asia, should not quote the 8 percent line without naming which population it describes.

The US National Eye Institute states roughly 1 in 12 men have some form of colour vision deficiency, red-green being by far the most common type and blue-yellow considerably rarer, and notes CVD can also be acquired later in life through cataract, diabetes or certain medicines rather than only inherited. This is a public-domain federal source and the safer figure to quote when a product's actual user population is unknown.

The practical consequence for review is the 1.4.1 and 1.4.11 rules already stated above: colour never carries meaning alone, and any UI element or chart mark that needs to be understood clears 3 to 1 non-text contrast against its neighbours. A grayscale pass, viewing the screen with colour removed entirely, is the fastest first check for whether information was hiding in hue alone.

## Type

| Rule | Authority | Level | Evidence class | Source |
|---|---|---|---|---|
| Text spacing must not lose content when line height is set to 1.5x font size, paragraph spacing to 2x, letter spacing to 0.12x, word spacing to 0.16x | WCAG 2.2, 1.4.12 Text Spacing | AA | Standard | W3C, Understanding SC 1.4.12 |
| Blocks of text carry user-selectable colours, a width no more than 80 characters (40 for CJK), no justification, line spacing at least 1.5, paragraph spacing at least 1.5x the line spacing, and resize to 200 percent without horizontal scrolling | WCAG 2.2, 1.4.8 Visual Presentation | AAA | Standard | W3C, Understanding SC 1.4.8 |
| Body text reads best at roughly 50 to 75 characters per line; a practical target is a max-width near 70ch | Baymard Institute | | Practitioner heuristic | Baymard, "Readability: The Optimal Line Length" |
| The fluent print-size range, where reading speed is maximal, spans about a factor of ten in angular x-height, roughly 0.2 to 2 degrees; at a 40cm reading distance that is x-heights of about 1.4mm (4pt) to 14mm (40pt) | Vision science literature | | Research evidence | Legge and Bigelow, 2011, Journal of Vision |
| GOV.UK's type scale runs 19px body text (24px large body, 16px small body) on larger screens, each with a line height in a 5px multiple, and 16px small body text below its 640px tablet breakpoint | GOV.UK Design System | | Platform convention | Government Digital Service |

1.4.8's 80-character measure and its 1.5 line-spacing rule are AAA, not AA, and this is the single most common misquote a PM will hear: a checklist that states "lines under 80 characters" as if it were required for AA conformance is quoting an AAA criterion as a floor. Say the level every time.

1.4.12 tests something different from default styling: it is a robustness check. A component still has to work, with nothing lost or overlapping, when a user's own accessibility settings inflate spacing well beyond whatever the design specified. A design that only ever looks right at its own default spacing values has not been tested against 1.4.12 regardless of how generous those defaults look.

Legge and Bigelow's evidence is about angular size, the size of the letter relative to the eye, not a fixed pixel count, which means a fixed px minimum for body text is always a convention layered on top of an assumption about viewing distance and typeface; the same physical size reads differently held at arm's length than at a desk. Baymard's 50 to 75 character range is a practitioner heuristic from e-commerce usability testing with an unpublished method, reporting user fatigue past roughly 100 characters per line; treat it as a strong starting point, not a measured law. A separate strand of screen-reading research (Dyson and Haselgrove, 2001) tested 25, 55 and 100 characters per line and points toward a speed-versus-comprehension trade-off rather than one universal optimum; confirm the paper's own numbers before quoting a specific figure from it, since only a secondary summary was available when this card was written.

**A numbers-and-money row.** This repository's own study of design-system documentation across a large sample of fintech and product interfaces found a recurring, unstandardised but consistent pattern worth carrying into any product handling money: money cells set in tabular figures so digits align in a column, a stated and consistent currency-placement rule, and negative values marked by more than colour alone, a leading minus sign or parentheses alongside any red, never red by itself. That last point is 1.4.1 applied to a specific and easy-to-miss case: a negative balance shown only in red fails the same rule a chart series shown only in red does. This is a practitioner convention drawn from how live design systems actually document their number typography, not a standard, and it belongs in a design brief's constraints section for any product with a ledger, a balance or a transaction list.

Modular type scales built from a fixed ratio, the golden ratio 1.618 being the most cited, are an aesthetic convention popularised for the web in 2011. They produce a pleasing, consistent proportion and carry no readability evidence behind any particular ratio; treat a modular scale as a design decision to review for consistency, never as a claim about legibility.

## Spacing, grids and breakpoints

| Rule | Authority | Level | Evidence class | Source |
|---|---|---|---|---|
| Content reflows without two-dimensional scrolling at 320 CSS px wide (equivalent to 1280px at 400 percent zoom), or 256 CSS px tall for vertical-scrolling content; maps, data tables, games and toolbars are excepted | WCAG 2.2, 1.4.10 Reflow | AA | Standard | W3C, Understanding SC 1.4.10 |
| All spacing, padding and margin values are multiples of 8, often paired with a 4pt baseline grid for text | The 8-point grid | | Practitioner heuristic | Widely documented practitioner convention |
| Window size classes: compact under 600dp, medium 600 to 839dp, expanded 840 to 1199dp, large 1200 to 1599dp, extra-large 1600dp and up | Material 3 | | Platform convention | Google Material Design |
| Tablet breakpoint at 640px | GOV.UK Design System | | Platform convention | Government Digital Service |

1.4.10 is the only layout width in this section backed by a standard, and it is worth stating precisely because it is often paraphrased loosely: the requirement is reflow, not a specific breakpoint, and it is tested by checking that nothing needs to scroll in two directions at once at that width. Everything else here, the 8-point grid, Material's window classes, GOV.UK's 640px, is a convention chosen by a specific practice or platform for consistency and fewer decisions, not a figure with user-performance research behind the specific number. The 8-point grid's own stated benefit is that it takes seven of every eight possible spacing values out of a design conversation, which is a real and useful discipline, but it is a discipline, not a finding. A spec that blends numbers from two systems, an 8-point spacing scale next to a 640px breakpoint borrowed from a different design system's own internal logic, is not wrong, but a reviewer should be able to see which authority each number came from and that they were not assumed to be the same authority.

## Targets

| Rule | Authority | Level | Evidence class | Source |
|---|---|---|---|---|
| Pointer targets at least 24 by 24 CSS px, or spaced so a 24px circle centred on an undersized target touches no other target; inline, equivalent, user-agent and essential targets are excepted | WCAG 2.2, 2.5.8 Target Size (Minimum) | AA | Standard | W3C, Understanding SC 2.5.8 |
| Default control size 44 by 44 pt on iOS and iPadOS (minimum 28 by 28 pt); other Apple platforms vary: macOS 28x28 and 20x20, tvOS 66x66 and 56x56, visionOS 60x60 and 28x28, watchOS 44x44 and 28x28 | Apple Human Interface Guidelines | | Platform convention | Apple |
| Commonly documented minimum touch target of 48dp | Material Design | | Platform convention | Google Material Design; not independently re-verified against a fetched source in this pass, confirm against the current Material touch-target page before citing a specific number in a spec |

These three numbers conflict, on purpose, because they come from three different authorities answering slightly different questions: WCAG's 24px is a minimum accessibility floor across any web content, Apple's 44pt is a platform's own default control size tuned to its own displays and its own point unit, and Material's commonly cited 48dp follows the same logic for Android's density-independent pixel unit. Record which authority a spec is actually committing to, name it in the design review record, and do not average the three or treat them as interchangeable; a component sized to clear WCAG's 24px floor is not automatically sized to Apple's or Material's own platform convention, and a native app built to a platform's convention should say so rather than quoting WCAG's number as if it were the platform's own rule.

## Motion

| Rule | Authority | Level | Evidence class | Source |
|---|---|---|---|---|
| Most UI animations run 100 to 500 milliseconds depending on complexity and travel distance; simple feedback such as a toggle sits near 100ms, modal-scale changes near 200 to 300ms; pick the shortest duration that does not feel jarring | Nielsen Norman Group | | Practitioner heuristic | NN/g, "Executing UX Animations" |
| Interaction-triggered motion (parallax and scroll-linked motion named specifically) can be turned off unless essential | WCAG 2.2, 2.3.3 Animation from Interactions | AAA | Standard | W3C, Understanding SC 2.3.3 |
| `prefers-reduced-motion` CSS media feature, values `no-preference` and `reduce`, Baseline widely available since January 2020 | CSS Media Queries | | Standard (implemented, not a WCAG success criterion) | MDN |

2.3.3 is AAA, not AA, and this matters because it is tempting to treat a reduced-motion commitment as optional simply because the underlying success criterion sits at the AAA level. The vestibular harm the criterion exists to prevent is real regardless of which conformance level a product commits to, and this card recommends honouring `prefers-reduced-motion` as a baseline practice independent of the conformance target, because the CSS mechanism to do so is now a Baseline, widely supported web feature with essentially no implementation cost.

Material 3's own duration tokens, short, medium, long and extra-long bands running from roughly 50ms to 1000ms, are marked by Google itself as no longer maintained, superseded by a spring-based motion system; do not cite the token table as current Material guidance. IBM Carbon's motion system distinguishes productive motion, which serves a task, from expressive motion, reserved for occasional important moments, and its documentation says every motion should have a static or reduced alternative available, which is a useful framing independent of which specific duration numbers a team adopts.

One number was deliberately left out of this card. Early justifications for reduced-motion support cited counts of people affected by vestibular disorders, and a commonly repeated figure for adults over 40 traces to a 2009 population study. Neither figure was verified against its primary source in the research pass behind this card, both are secondary citations at best, and this card would rather state plainly that vestibular harm from motion is a documented, real phenomenon than repeat an unverified number to make that point sound more urgent than the underlying standard already makes it.

## Colour scheme and dark mode

Whether a product supports light mode, dark mode or both is a non-functional requirement, not a visual-design footnote; record it in [nfr.md](../../templates/definition/nfr.md) section 5 alongside the conformance level it sits beside, rather than leaving it to whoever builds the theme last.

Nielsen Norman Group's review of the literature finds that for people with normal or corrected vision, light mode, positive polarity, produces better visual acuity and proofreading performance, citing Piepenbrock et al. (2013) in Ergonomics; the advantage grows as font size shrinks, even though the same participants reported no perceived difference between modes. Some people with cataracts may read better in dark mode. A link between long-term light-mode reading and myopia has been reported, but the study behind it had seven participants; that is evidence to note, not evidence to build a policy on, and this card names the sample size specifically so nobody downstream repeats the claim without it.

The practical framing this card recommends: treat dark mode as a user preference and an accessibility option for the people it genuinely helps, not as an accessibility improvement in general. Evidence favours light mode for reading performance overall, particularly at small sizes, which cuts against the common assumption that dark mode is simply the more accessible default.

Where a team does build a dark theme, Material's own convention is worth knowing even though it is a legacy (Material 2) page: use a dark surface near #121212 rather than pure black, keep enough headroom that white text on the base surface clears roughly 15.8 to 1 so elevated, lighter surfaces still pass the 4.5 to 1 text-contrast standard, desaturate primary colours because saturated colours both fail contrast more easily and visually vibrate against a dark background, and express elevation through lighter surfaces rather than through shadow alone, since shadows read poorly on a dark ground. This is a platform convention, not a standard, and every colour pair a dark theme produces still needs its own measured contrast check rather than inheriting the light theme's passing grade.

## Icons and hierarchy

Nielsen Norman Group's icon research is blunt: very few icons are universally recognised without a label, home, print and the magnifying glass for search being close to the exceptions, and understanding almost any other icon depends on prior experience the viewer may not have. The practical rule: an icon needs a visible text label, not a tooltip that appears only on hover, unless the icon is one of the small set that has become genuinely universal.

Visual hierarchy, the ordering that guides a viewer's eye to what matters most first, comes from three levers according to the same source: colour and contrast, scale, and grouping. None of the three carries a numeric rule; hierarchy is judged by whether a viewer can name the primary action on a screen within a few seconds, not by measuring against a formula. That squint-test framing belongs in a design review record alongside the measured numbers this card otherwise insists on, because hierarchy is real and reviewable even where it resists a table.

## Charts

Colour rules for data visualisation follow directly from the standards already stated above, applied to marks instead of text: a chart series told apart only by hue fails 1.4.1, and any chart element needed to understand the data clears 1.4.11's 3 to 1 non-text contrast. Two further, non-standard rules from the data-visualisation literature (Wilke, *Fundamentals of Data Visualization*) are worth carrying into any review: avoid rainbow colour scales for continuous data, because a rainbow scale emphasises arbitrary bands of the range rather than the underlying quantity, and design categorical palettes for colour vision deficiency using eight colour-vision-safe categories, the palette commonly credited to Okabe and Ito (2008) and named in Wilke's own chapter on the subject. This card deliberately does not reproduce the palette's hex values here; a design system that adopts it should cite the palette by name and pull the actual values from a source built to host them, not from a knowledge card.

Chartability, a workbook of testable data-visualisation accessibility heuristics built around the POUR principles (Perceivable, Operable, Understandable, Robust) plus three further criteria the authors call Compromising, Assistive and Flexible, offers quick and full audit modes and is worth pointing a team toward directly; its text is licensed CC BY-SA, so this card paraphrases its structure rather than reproducing its heuristics, and any future worksheet built from it needs its own attribution rather than a copy of Chartability's own wording.

A chart-specific accessibility floor worth stating plainly: every chart needs a text or table equivalent of the underlying data, not only a well-contrasted image of it, because a chart with perfect contrast and a CVD-safe palette is still inaccessible to anyone using a screen reader if the numbers behind it exist nowhere but inside the rendered graphic.

## The trap: the PM becomes the designer

This card's numbers are seductive precisely because they are numbers, and a PM under deadline pressure will reach for a table like the ones above and start specifying pixel values, easing curves and palette choices directly into a ticket. That is the trap. Every number in this card exists so a PM can ask a sharper question of the person who owns the answer, never so the PM can supply the answer instead. "This contrast pair measures 3.8 to 1 against a 4.5 to 1 target, what's the fix" is a PM doing the job. "Make it darker, maybe like #333" is a PM doing the design lead's job worse than the design lead would, while still holding the design lead accountable for the result.

The tell is where the sentence points. A question aimed at a standard, a convention or a measured value ("does this clear 4.5 to 1," "which target-size authority are we following," "what's our reduced-motion behaviour") belongs to the PM and this card equips it directly. A sentence that supplies a hex value, a specific easing curve, a spacing number chosen by eye, or any answer to "which one looks better" belongs to the named designer alone, every time, regardless of how confidently this card's tables let a PM produce the same shape of sentence. A PM who has internalised every table above and still asks only the first kind of question has used this card correctly; a PM who starts handing back colour values has not, no matter how well-sourced those values happen to be.

## How it lies

The most common distortion this card guards against is level conflation: quoting an AAA criterion, 1.4.8's 80-character measure or 2.3.3's animation opt-out, as if it were required at AA, which is the level most conformance targets actually name. The fix is mechanical: say the level every time a WCAG number is quoted, and never let a checklist item stand without one.

The second distortion is treating a threshold as an optimum. WCAG's 4.5 to 1 is derived from an accessibility floor for a defined population, not measured as the point where reading is easiest; a pair that clears it can still be hard to read at a thin weight or a small size, and a team that stops asking questions the moment a number passes has confused compliance with quality.

The third is authority laundering: a vendor claim (APCA's Lc thresholds) or a practitioner heuristic (Baymard's 50 to 75 characters) gets repeated often enough, and confidently enough, that a team starts treating it as if it carried a standard's legal weight. It does not, and repetition is not promotion between evidence classes.

The fourth is universalising population-specific research. Birch's 8 percent colour-vision-deficiency figure is the European Caucasian figure specifically; a product's actual population may see 4 to 6.5 percent, may see something else again, and stating "8 percent of users" without naming the population is a claim this card's own sourcing does not support.

The fifth is the platform-blend failure already named under targets and breakpoints: taking a number from one platform's convention and applying it inside a spec that is actually following a different platform or the web standard, without saying so. Each number in this card belongs to an authority; carrying the number without carrying the authority is how a spec quietly stops being reviewable.

## Where it sits in the loop

- Stage: DESIGN, feeding [Gate 3: Architecture and risks reviewed](../../os/STAGE-GATES.md), the gate that closes DESIGN and opens BUILD.
- Upstream: the design brief's constraints section, where a product first names its design system, conformance target and dark-mode commitment, and [nfr.md](../../templates/definition/nfr.md) section 5, where the conformance level itself is set once and inherited everywhere else.
- Downstream: the [accessibility checklist](../../templates/architecture/accessibility-checklist.md) walks WCAG's guideline families component by component with an evidence column, and cross-links here rather than re-explaining where a number came from; the [design review record](../../templates/architecture/design-review-record.md) is where a specific screen's measured values and the authority each one follows get written down for the gate.
- On trial at [Gate 3](../../os/STAGE-GATES.md): the gate as it stands today is architecture and risk only, and carries no design-specific line yet; until it does, a design review record's findings route through the risk register the same way any other unresolved finding does.

## Used by

- [Accessibility checklist](../../templates/architecture/accessibility-checklist.md)
- [NFR template](../../templates/definition/nfr.md)
- [Design review record](../../templates/architecture/design-review-record.md)

## Reading

- Understanding SC 1.4.3 Contrast (Minimum), W3C WAI. Reuse class: paraphrase with attribution under the W3C Document License. https://w3c.github.io/wcag/understanding/contrast-minimum.html
- Understanding SC 1.4.11 Non-text Contrast, W3C WAI. Reuse class: paraphrase with attribution under the W3C Document License. https://w3c.github.io/wcag/understanding/non-text-contrast.html
- Understanding SC 1.4.1 Use of Color, W3C WAI. Reuse class: paraphrase with attribution under the W3C Document License. https://w3c.github.io/wcag/understanding/use-of-color.html
- Understanding SC 1.4.8 Visual Presentation (AAA), W3C WAI. Reuse class: paraphrase with attribution; always labelled AAA. https://w3c.github.io/wcag/understanding/visual-presentation.html
- Understanding SC 1.4.12 Text Spacing, W3C WAI. Reuse class: paraphrase with attribution. https://w3c.github.io/wcag/understanding/text-spacing.html
- Understanding SC 1.4.10 Reflow, W3C WAI. Reuse class: paraphrase with attribution. https://w3c.github.io/wcag/understanding/reflow.html
- Understanding SC 2.5.8 Target Size (Minimum), W3C WAI. Reuse class: paraphrase with attribution. https://w3c.github.io/wcag/understanding/target-size-minimum.html
- Understanding SC 2.3.3 Animation from Interactions (AAA), W3C WAI. Reuse class: paraphrase with attribution; always labelled AAA. https://w3c.github.io/wcag/understanding/animation-from-interactions.html
- Contrast Research: APCA Peer Reviews and Defining a Visual Contrast Guideline, W3C GitHub, opened by APCA author A. Somers. Reuse class: cite only. https://github.com/w3c/wcag3/issues/29
- WCAG3 Contrast as of April 2026, Adrian Roselli. Reuse class: cite only. https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html
- WCAG 3 is not ready yet, Eric Eggert. Reuse class: cite only. https://yatil.net/blog/wcag-3-is-not-ready-yet
- Worldwide prevalence of red-green color deficiency, Birch (2012), Optica/PubMed abstract. Reuse class: cite only; the figures themselves are facts and may be restated with attribution. https://pubmed.ncbi.nlm.nih.gov/22472762/
- Color Blindness, US National Eye Institute. Reuse class: public domain federal work, adapt with attribution. https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness
- Readability: The Optimal Line Length, Baymard Institute (Edward Scott, 2022). Reuse class: cite only. https://baymard.com/blog/line-length-readability
- GOV.UK Design System: Type scale, Government Digital Service. Reuse class: adapt under licence (MIT, Crown copyright notice). https://design-system.service.gov.uk/styles/type-scale/
- Material Design 3: Breakpoints (window size classes), Google. Reuse class: adapt under licence (CC BY 4.0 or Apache 2.0, with attribution). https://m3.material.io/foundations/layout/applying-layout/window-size-classes
- Executing UX Animations: Duration and Motion Characteristics, Nielsen Norman Group (Aurora Harley). Reuse class: cite only. https://www.nngroup.com/articles/animation-duration/
- prefers-reduced-motion, MDN. Reuse class: paraphrase with attribution (CC BY-SA 2.5 prose); avoid verbatim copying. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Dark Mode vs. Light Mode: Which Is Better?, Nielsen Norman Group (Raluca Budiu, 2020), reviewing Piepenbrock et al. (2013), Ergonomics. Reuse class: cite only; the primary study is cited separately for evidence claims. https://www.nngroup.com/articles/dark-mode/
- Icon Usability, Nielsen Norman Group (Harley, 2014). Reuse class: cite only. https://www.nngroup.com/articles/icon-usability/
- Fundamentals of Data Visualization, chapter 19, Claus O. Wilke (O'Reilly, 2019, free web edition). Reuse class: cite only; the Okabe and Ito palette is a fact attributable to Okabe and Ito directly. https://clauswilke.com/dataviz/color-pitfalls.html
- Chartability, Frank Elavsky and Fizz Studio (EuroVis 2022 paper with Bennett and Moritz). Reuse class: paraphrase only, never adapt verbatim (CC BY-SA 3.0, ShareAlike). https://chartability.fizz.studio/
- Apple Human Interface Guidelines: Accessibility. Reuse class: cite only. https://developer.apple.com/design/human-interface-guidelines/accessibility
- VoltAgent/awesome-design-md, commit 8147538. Reuse class: adapt the section schema with the MIT notice; brand-specific file content is cite-only and was not carried into this card.
