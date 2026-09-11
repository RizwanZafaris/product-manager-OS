---
name: design-review
description: Run a design critique prep, a Gate 3 design review, a live-build design check before Gate 4, or an accessibility, content, localisation, or deceptive-design pass, one evaluator at a time, against the objectives written in the design brief. Use when a screen or flow is heading to Gate 3, a shipped build needs checking against its design before Gate 4, a critique room needs a structured pass before it fills with opinions, or a flow touches consent, cancellation, subscription, or a jurisdiction with an accessibility or dark-pattern regulator. Takes the design brief, the screens or build under review, and the worksheet or checklist the mode calls for; returns a severity-ranked findings table routed to the design review record, the risk register, or the tech-debt register, and never a sign-off.
---

# Design Review: one evaluator, against written objectives, never a verdict

A design review meeting that opens with "what do people think" produces a vote on taste, because nothing in the room states what the screen was supposed to do before anyone reacts to how it looks. This skill will not run without an objective to check against, and it will not let its own output pass as more than it is: whichever worksheet or checklist it walks, it walks alone, and a single evaluator catches a documented minority of what is actually wrong. The discipline of reporting findings without rewriting or ruling is the same discipline [spec-review](../spec-review/SKILL.md) holds for written requirements; this skill holds it for the screen.

## Files this skill drives

- Pulls objectives from, and never edits: [design-brief.md](../../templates/definition/design-brief.md), sections 1 and 4
- Runs, as one evaluator, whichever worksheet the mode calls for: [heuristic-evaluation.md](../../frameworks/design/heuristic-evaluation.md) (general pass or cognitive walkthrough), [design-critique.md](../../frameworks/design/design-critique.md) (critique prep), [content-microcopy-audit.md](../../frameworks/design/content-microcopy-audit.md) (content pass), [choice-symmetry-audit.md](../../frameworks/design/choice-symmetry-audit.md) (deceptive-design pass)
- Walks, in full, for an accessibility pass or before any Gate 3 or Gate 4 mode: [accessibility-checklist.md](../../templates/architecture/accessibility-checklist.md), including its scope-and-sample block in section 1 and its suppressions-and-accepted-exceptions table in section 10
- Walks, for a localisation pass: [localisation-rtl-checklist.md](../../templates/architecture/localisation-rtl-checklist.md)
- Checks strings against: [ux-writing-guide.md](../../templates/definition/ux-writing-guide.md), when the product has written one
- Reads, never invents: [ui-state-inventory.md](../../templates/definition/ui-state-inventory.md) for the state list every mode walks against, [component-spec.md](../../templates/architecture/component-spec.md) for a shared component's specification, and `products/<name>/DESIGN.md` (from [design-md.md](../../templates/architecture/design-md.md)) for the tokens and rules a Gate 3 or live-build review checks the screen against
- Routes every finding, by severity, into exactly one of: [design-review-record.md](../../templates/architecture/design-review-record.md) (the review itself, and the evidence Gate 3 and Gate 4 read), [risk-register.md](../../templates/execution/risk-register.md) (a finding that threatens the product, not only the screen), [tech-debt-register.md](../../templates/execution/tech-debt-register.md) (a known, accepted gap carried forward)
- Method behind the worksheets and the checklist: [usability-heuristics.md](../../knowledge/design/usability-heuristics.md), [accessibility-and-inclusive-design.md](../../knowledge/design/accessibility-and-inclusive-design.md), [accessibility-regulation.md](../../knowledge/design/accessibility-regulation.md), [deceptive-design.md](../../knowledge/design/deceptive-design.md)
- Feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md) and [Gate 4: acceptance criteria met](../../os/STAGE-GATES.md); evidence classes and quote limits per [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md)

## When to use

- A critique room is about to fill and needs objectives pasted in before the first comment, per [design-critique.md](../../frameworks/design/design-critique.md)
- A screen, flow, or prototype is heading to Gate 3 and needs a structured pass with a shared vocabulary in place of a pile of individual reactions
- A build just shipped into BUILD and needs checking against the design brief and the accessibility checklist's evidence column before Gate 4 reads it
- A flow carries new or changed user-facing text, a right-to-left locale, or a consent, cancellation, downgrade, or subscription step, and has not had its own pass yet
- A product ships into a jurisdiction carrying an accessibility regulator (the European Accessibility Act, Section 508, EN 301 549) or a dark-pattern regulator (the EU Digital Services Act, California's CCPA regulations, the FTC), and nobody has stamped which rules apply

**Skip it when:** nothing concrete exists yet to walk. A blank page or a single static mock has no flow for a heuristic to be checked against and no string set for a content audit; the design brief itself is the right tool for that moment. Skip the worksheet modes, not the accessibility or choice-symmetry modes, once a moderated usability round on the same flow has already produced real task-success data this iteration; running an inspection on top of it without saying so blurs a documented finding into a guess.

## Inputs

The design brief, for the objectives in sections 1 and 4; reviewing a screen against no written objective returns a taste opinion wearing this skill's name. The screens, flow, prototype, or live build under review, at a fidelity the mode can actually assess: a sketch supports a heuristic pass, not an accessibility pass that needs rendered contrast and real focus order. The mode, named by whoever is asking, or inferred from what exists (a live build implies the Gate 4 mode; a consent or cancellation flow implies the deceptive-design mode); ask when more than one mode plausibly fits and say which was chosen and why. For an accessibility pass: the conformance target copied from [nfr.md](../../templates/definition/nfr.md) section 5, not picked here. For a deceptive-design pass: every jurisdiction the flow ships into, because a rule that applies in California does not apply in a market with no equivalent. This skill runs with no model at all, as a checklist a person walks by hand; a model running it is one more evaluator, not a panel, and reports itself as exactly that.

## Workflow

### 1. Classify the request into a mode

Pick exactly one: critique prep, Gate 3 review, live-build review for Gate 4, accessibility pass, content pass, localisation pass, or deceptive-design pass. A Gate 3 review runs several of the others inside it, named below; the other modes run standalone, on request, between gates. State the mode chosen, in the output, before anything else.

### 2. Pull objectives, never invent them

Copy the problem statement and the success table from [design-brief.md](../../templates/definition/design-brief.md) sections 1 and 4 verbatim, not from memory of the meeting where they were discussed. No written brief exists: stop and say so, rather than reviewing against an objective this skill supplied itself.

### 3. Run the matching worksheet, and label it what it is

For critique prep, a general or task-based pass, or a content pass, open the matching worksheet ([design-critique.md](../../frameworks/design/design-critique.md), [heuristic-evaluation.md](../../frameworks/design/heuristic-evaluation.md), [content-microcopy-audit.md](../../frameworks/design/content-microcopy-audit.md)) and run it exactly once, as a single evaluator. Label the output **"one evaluator, unvalidated"** and carry the caveat with it: a lone evaluator working alone catches only 20 to 51 percent of the usability problems actually present (Nielsen and Molich, 1990, research evidence, via [usability-heuristics.md](../../knowledge/design/usability-heuristics.md)), and any two evaluators looking at the same screen agree on only 5 to 65 percent of what they separately find (Hertzum and Jacobsen, 2001, research evidence, same source). Neither number moves because the evaluator is careful, experienced, or a model; it is a documented property of the method. State in the output how many more independent evaluators a real panel needs (3 to 5, per the worksheet) before the findings list is reported as anything more than a first, cheap filter.

### 4. Walk the accessibility checklist in full, and refuse to certify

For an accessibility pass, or inside a Gate 3 or Gate 4 review, walk every component table in [accessibility-checklist.md](../../templates/architecture/accessibility-checklist.md) that the inventory in section 2 marks present. Complete the scope-and-sample block in section 1 before any table: the structured-plus-random sample names real pages and real states, including error, timeout, and third-party embedded content, not only the happy path. Report an automated checker's result with the ruleset it was actually configured to run, never as a blanket pass; a green automated scan and a browser overlay plug-in are both evidence of what that specific tool checked, not of conformance, because automated tools miss a majority of accessibility problems a blind user actually encounters on the page (Power, Freire, Petrie, and Swallow, CHI 2012, research evidence) and no independent evidence supports an overlay product's claim to make a site fully conformant on its own (FTC consent order against accessiBe, April 2025, one million US dollars, regulatory precedent, as of 2026-09-10, confirm with counsel). This skill never writes the word "conformant," "compliant," or "certified" about a product; it writes which checks passed, which failed, which are marked incomplete or needs-review (both of which are mandatory manual rows, never silent CI passes), and walks the suppressions-and-accepted-exceptions table in section 10, confirming every suppression carries an approver who did not author the component, an expiry date, and a linked risk-register row. Never cite the Accessible Perceptual Contrast Algorithm (APCA) or WCAG 3.0 as the basis for a pass or fail: WCAG 3.0 is a W3C Working Draft, not yet a Recommendation, and the conformance target this checklist inherits from the NFR is WCAG 2.2.

### 5. Run the localisation and content passes where the flow touches them

For a localisation pass, or a right-to-left locale anywhere in scope, walk [localisation-rtl-checklist.md](../../templates/architecture/localisation-rtl-checklist.md). For any flow carrying new or changed user-facing text, run the content pass (step 3) against [ux-writing-guide.md](../../templates/definition/ux-writing-guide.md) where one exists, layering its glossary and banned-word list on top of the worksheet's house list.

### 6. Run the choice-symmetry grid and stamp jurisdiction rows

For a deceptive-design pass, or any flow with a consent, cancellation, downgrade, or subscription step inside a Gate 3 review, run [choice-symmetry-audit.md](../../frameworks/design/choice-symmetry-audit.md): the path to the more privacy-protective or less committing option must not be longer, harder, or slower than the path to the opposite choice, and a binary choice needs a real decline, not a deferral dressed as one (Cal. Code Regs. tit. 11, section 7004(a)(2), standard, confirm with counsel). Findings are judged by effect, not by the designer's intent (CPPA Enforcement Advisory 2024-02, regulatory precedent). For every applicable jurisdiction, add a row naming the rule, the date it was read **as of**, and the words **"confirm with counsel"**; a jurisdiction row with neither is not a finding, it is an assumption with a due date nobody set.

### 7. Route every finding by severity, and stop

Score every finding on the 1 to 4 severity scale the worksheets already share with [usability-test-plan.md](../../templates/discovery/usability-test-plan.md) section 6. Route each one to exactly one place: an open item still being designed or built goes to [design-review-record.md](../../templates/architecture/design-review-record.md); a finding that threatens the product beyond this screen (a regulatory exposure, a security-adjacent pattern, a metric at risk) goes to [risk-register.md](../../templates/execution/risk-register.md); a known gap the team is knowingly carrying goes to [tech-debt-register.md](../../templates/execution/tech-debt-register.md), tagged by its debt type. Do not also decide whether the design passes. This skill's job ends at the routed table; the design review record names who signs next.

## Output format

1. **Mode declared**: which of the seven this run is, and why, when more than one fit.
2. **Evaluator statement**: "one evaluator, unvalidated" for any worksheet mode, with the 20 to 51 percent and 5 to 65 percent caveats stated in full, not abbreviated to a single figure; omitted only for the accessibility checklist and the choice-symmetry grid, which are walked against named criteria rather than scored by inspection.
3. **Findings table**: | # | Mode / worksheet | Location (screen, state, or string) | Finding | Severity (1 to 4) | Evidence | Routed to (design review record / risk register / tech-debt register) | Owner | Fix by |
4. **Accessibility addendum**, when run: the scope-and-sample block as completed, the ruleset actually configured, and the suppressions table with every approver, expiry, and risk-register link.
5. **Jurisdiction table**, when a deceptive-design pass ran: | Jurisdiction | Rule | Result | As of | "Confirm with counsel" |
6. A closing line naming what this review is not: not a sign-off, not a conformance certificate, not a substitute for the panel size the worksheet calls for.

## Failure modes this skill guards against

- **One evaluator's pass reported as the review.** A single pass catches 20 to 51 percent of what is actually wrong, and two evaluators agree on as little as 5 percent of what they separately find; reporting it as "reviewed" rather than "one evaluator, unvalidated" lets a Gate 3 or Gate 4 sign-off rest on a number nobody can reproduce.
- **A green automated scan presented as accessibility evidence.** Automated tools find a real but partial share of problems and miss most of what a blind user actually hits; reporting the scan's result without naming its configured ruleset turns a partial check into an unearned certificate.
- **An accessibility overlay or widget claimed to make the product compliant.** The FTC's 2025 order against accessiBe bars exactly this claim without evidence; this skill treats an overlay's own marketing the same way it treats any vendor claim, cite-only, never as the finding itself.
- **APCA or WCAG 3.0 cited as the compliance basis.** WCAG 3.0 is still a draft, not a Recommendation, and APCA is not the contrast model the conformance target in the NFR names; either one, cited as a pass or fail, is a standard that does not yet exist being used to close a gate that does.
- **A taste opinion wearing a finding's severity and location columns.** This skill reports what violates a written objective or a named rule; it never issues a go, a no-go, or a "feels off," which belongs to the design review record's named human signer.
- **A jurisdiction row with no as-of date and no counsel flag.** Dark-pattern and accessibility law is read and enforced by its effect on the consumer, not by the designer's intent, and a rule read once in 2026 without a re-check trigger is a rule nobody will notice has moved.
- **A suppression with no expiry or an approver who is also the author.** An accepted exception that never expires, or that was accepted by the person who built the thing it excuses, is a gap wearing a sign-off.
- **A finding that leaves the room and lands nowhere.** A severity score with no routed register row is a finding that existed for one meeting and then stopped existing; every row above ends in exactly one of three named destinations.

## Exit gate

This skill produces evidence for a gate; it does not close one. For a Gate 3 mode, the routed findings table and the completed accessibility addendum are the inputs [design-review-record.md](../../templates/architecture/design-review-record.md) carries into [Gate 3](../../os/STAGE-GATES.md), where a named architect, product owner, or security reviewer signs, never this skill. For a Gate 4 mode, the live-build findings confirm the shipped build still matches the design brief and that every accessibility evidence cell the checklist promised is filled, feeding the acceptance agent's own check at [Gate 4](../../os/STAGE-GATES.md). A review with an open severity finding and no register row is not done; a review that reports "one evaluator, unvalidated" honestly is done, because the caveat, not a false completeness, is the accurate report of what one evaluator, one time, can actually tell a gate.
