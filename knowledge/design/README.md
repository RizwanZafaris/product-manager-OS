---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Design Index", "Experience Design Index"]
---
# Experience Design Index

Experience design is the craft of making a product understandable, usable, accessible and honest once a person is actually looking at a screen. This layer holds the cards a PM reads to commission that work, question it and judge the result, without doing the designer's job. Roles answers WHO in [knowledge/roles/README.md](../roles/README.md) and domains answers WHERE in [knowledge/domains/README.md](../domains/README.md); this layer answers HOW a screen, a flow or a piece of copy should behave once it is built.

**"Design" here is never the DESIGN stage.** [os/OPERATING-LOOP.md](../../os/OPERATING-LOOP.md) runs a product through six stages, DESIGN among them, gated at Gate 3 in [os/STAGE-GATES.md](../../os/STAGE-GATES.md). Experience design work happens across all six stages, from a definition-stage acceptance criterion to a delivery-stage choice-symmetry check, and none of the cards below stand in for that gate.

## What this layer answers

A card here does not teach visual craft. It teaches a product person to read a design decision, commission the work with a clear brief, and tell a genuine usability problem from a stylistic preference, so a review lands on substance instead of taste.

- What does a named heuristic or a cited law actually claim, and where does it stop being true
- What must a product decide before a designer can start, and what belongs to the designer alone
- Which obligations are legal, which are convention, and which authority stands behind each number
- How is a usability claim measured, and what does a claim with no baseline actually prove
- Where does a critique end and a decision-rights dispute begin, and who owns that decision

## The cards

| Card | Pick it when | Essence |
|---|---|---|
| [Usability Heuristics](usability-heuristics.md) | You are inspecting a screen or flow before it reaches user testing | Nielsen's ten heuristics, Shneiderman's eight golden rules and the ISO 9241-110 principles, cross-walked, with the evidence on how much a single inspector actually finds |
| [Interaction Design Principles](interaction-design-principles.md) | You are writing acceptance criteria or a design brief and "intuitive" is not testable | Norman's vocabulary, discoverability, affordance, signifier, mapping, feedback, constraints, turned into observable pass or fail criteria |
| [UX Laws Evidence Ledger](ux-laws-evidence.md) | Someone cites Fitts, Hick, "seven plus or minus two" or another named law as if it settles the argument | A ledger that grades each law's origin, what it actually claims and its strongest counter-evidence, so a heuristic stops passing as a proof |
| [Accessibility and Inclusive Design](accessibility-and-inclusive-design.md) | You are filling an accessibility checklist or planning research with disabled participants | WCAG 2.2 practice and the testing evidence on what conformance checking actually finds, and why an accessible component library does not make a composed flow conform |
| [Accessibility Regulation](accessibility-regulation.md) | You are setting a conformance target in an NFR or a compliance-impact assessment | A dated obligation map across the EU, US, UK, UAE and Pakistan, each row carrying a verification status and a review trigger; not legal advice |
| [Internationalisation and RTL](internationalisation-and-rtl.md) | The product ships in Arabic, Persian, Urdu or another right-to-left or bidirectional market | Direction, mirroring, digit sets and bidi isolation, and the questions a PM must ask before trusting a translated screenshot |
| [Content Design](content-design-and-forms.md) | You are writing microcopy, an error message, an empty state or a form's validation behaviour | GOV.UK content-design rules and form patterns for error timing, disclosure and system states, in a PM's own words rather than a stylesheet |
| [Deceptive Design](deceptive-design.md) | A growth or retention flow narrows a choice, or release readiness needs a choice-symmetry pass | Dark-pattern taxonomy read against the DSA, CCPA and FTC enforcement record, judged by effect rather than intent; not legal advice |
| [Visual Foundations](visual-foundations.md) | You are reviewing contrast, type, spacing, targets, motion or colour without becoming the designer | Every visual number tagged by the authority behind it, so a standard, a platform convention and a heuristic are never confused for one another |
| [UX Measurement](ux-measurement.md) | A usability test plan needs a scorecard, or a launch readout claims a usability number | SUS, UMUX-LITE and HEART at the task, test and product level, and why one satisfaction score with no baseline proves nothing |
| [PM and Design Collaboration](pm-design-collaboration.md) | You are running a critique or a review, handing off a spec, or a decision-rights dispute has reached the triad | Critique against review, structured handoff, and where design debt gets tracked instead of argued about forever |
| [Design Systems and Tokens](design-systems-and-tokens.md) | You are commissioning a component spec, a DESIGN.md, or a design-system audit | A design system as a second product with its own users, backlog and release cadence; tokens as the contract that keeps a name meaning the same thing in the design tool and the shipped code |
| [Component-Driven Development](component-driven-development.md) | You are writing a UI state inventory or reviewing a component spec | Why a rendered, named story is the acceptance surface, not a screenshot or a live click-through, and how a component's state list stays owned in one place |
| [UI Dependency Licensing](ui-dependency-licensing.md) | You are choosing a UI library or component, or filling the dependency register's licence column | Which licence questions actually have teeth, read from the project's own licence file rather than a README; not legal advice |
| [AI Interaction Patterns](ai-interaction-patterns.md) | You are writing the AI interaction spec for a feature with a model behind it | The recurring user-facing decisions inside an AI feature, generation disclosure, stop behaviour, citations, ratings, memory, read as a case study rather than a specification |

## What this layer does not hold

No component specs, no token values, no palettes of any kind including hex values, no grids, no Figma kits, no logos or other brand assets, no taste rules and no contrast calculator. This layer explains what a number means and which authority stands behind it; a design system that ships actual values is a different kind of artifact, built once a template proves the layer's advice insufficient on its own, per the graduation rule below.

## Sources and licences

- This repository is MIT licensed.
- Text under a source the register at [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md) classes "Adapt with notice" may be adapted into a card (today: OGL v3, CC0, public domain, CC BY 4.0, MIT, Apache 2.0, the W3C Software and Document License, and EU reuse under Commission Decision 2011/833/EU), and every such occurrence carries the notice its licence requires, as set out in that source's register row: for MIT and Apache 2.0, the copyright and licence notice; for Apache 2.0 and CC BY 4.0, a statement that the text was changed; for OGL v3, its attribution statement and a link to the licence; for the W3C Software and Document License and EU reuse, the attribution string the register specifies.
- Everything else is paraphrased in this repository's own words, or cited with at most one quote under fifteen words with the source named. One exception: a worksheet that administers a published questionnaire quotes the items verbatim with the source named, because a paraphrased item is a different instrument (the UX scorecard's single-ease and UMUX-LITE items).
- The complete source-and-licence register, including the seventeen repositories studied while building this layer, lives in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md).
- A card's own Reading section names each source's reuse class; check the register before adapting anything from a card into your own material.

## Graduation rule

This layer grows the way [knowledge/README.md](../README.md) grows: a card lands when a template in this repository starts depending on it, not before. Each card above lands with the template that depends on it. A future addition that only catalogs a method with nothing here yet depending on it stays a line in this table's own future change set, not a new file.
