---
layer: knowledge
stage: DESIGN
gate: 3
feeds: ["frameworks/design/heuristic-evaluation.md", "templates/discovery/usability-test-plan.md", "templates/architecture/design-review-record.md"]
method: ""
aliases: ["Usability Heuristics", "usability-heuristics"]
---
# Usability Heuristics

Based on Jakob Nielsen and Rolf Molich's inspection method for experience design (heuristic evaluation, Nielsen and Molich, ACM CHI 1990; revised by Nielsen, 1994; heuristic names and examples updated 2020, reviewed January 2024) and Ben Shneiderman's Eight Golden Rules of Interface Design (original list 1985, per Shneiderman's own page; current wording from Designing the User Interface, 6th edition, Pearson, 2016, section 3.3.4). Explained here in this repository's own words.

## The essence

Heuristic evaluation and its relatives are inspection methods: a small number of evaluators walk a design against a fixed list of general principles, with no participant recruited, and write down where the design breaks each one. The appeal is cost. A round can run in a day against a paper sketch, a clickable prototype or a shipped screen, and it catches the class of problem that is predictable in advance, an unreadable error message, a dead-end flow with no way back, a control that looks disabled when it is not, before anyone has to schedule five participants and a moderator.

Two named lists dominate practice, and this card credits both. Nielsen's ten heuristics are, in Nielsen's own words, "broad rules of thumb and not specific usability guidelines": general enough to apply to almost any interface, and for exactly that reason unable to say anything about whether one specific screen serves one specific task. Shneiderman's eight golden rules cover much the same ground, first drafted in 1985 and revised across six editions of his textbook since; the two lists overlap partly because they drew on shared HCI practice, and, by Shneiderman's own account, because Nielsen, Jeff Johnson and others went on to expand and vary the golden rules themselves. Where the two lists overlap, that overlap is a sign that both are naming the same handful of general ideas, not independent confirmation that the ideas are correct; where they diverge, the difference is usually a matter of grouping rather than disagreement. The crosswalk below places both against a third reference, the interaction principles in ISO 9241-110:2020, to show where all three name the same idea under three different labels, and where one list catches something the other two leave out.

None of the three is a substitute for watching a real person attempt a real task. What an inspection buys is speed and a shared vocabulary for the predictable problems; what it does not buy is evidence that the specific people who will use this specific product can actually get their specific job done, which is what the evidence and trap sections below are about.

## Where it came from

Jakob Nielsen and Rolf Molich published the original heuristic evaluation method at CHI 1990, working from their own practice of reviewing interfaces. That first list, arrived at by reflection on the authors' own experience rather than by data, held up reasonably in use but was not derived from evidence of which principles actually predicted problems in the field.

Nielsen answered that gap in 1994: a factor analysis of 249 usability problems (research evidence, Nielsen 1994) collected across earlier studies produced the ten-heuristic set used today, chosen for its explanatory power against that problem set rather than for breadth of coverage on paper. Nielsen Norman Group refreshed the heuristics' names, explanations and examples in 2020 and reviewed the article again in January 2024; by Nielsen's own account on the current page, the ten heuristics themselves have not changed since 1994.

Shneiderman's rules come from inside human-computer interaction research rather than industrial inspection practice, stating the guidance experienced practitioners had converged on. First drafted in 1985, the list has been revised across six editions of Designing the User Interface since, Shneiderman's own page noting that each edition produces some changes; rule 2 is one example, moving from the original edition's shortcuts-for-frequent-users framing to the broader "Seek universal usability" of the current wording. The wording used in this card throughout is the current one, from section 3.3.4 of the sixth edition, 2016. Shneiderman states plainly that the eight rules require validation and tuning for a specific application domain rather than being applied as they stand, which this card treats as a scope limit on the whole list, not a stylistic disclaimer to be skimmed past.

## When to use it

- Inspecting a prototype or a shipped screen before it goes into a moderated usability round, to catch the predictable, generic problems a real participant would otherwise burn a session on.
- Reviewing a competitor's product, or an acquired codebase's interface, where no research budget exists yet and a structured first pass still beats an unstructured one.
- Running a design critique (see [PM and Design Collaboration](pm-design-collaboration.md)) that needs a shared vocabulary in place of a pile of individual taste opinions.
- Re-checking a flow after a fix, as a cheap first filter before a second moderated round is committed to the same screen.

**Skip it when:** a moderated usability round on this exact flow has already run this iteration and produced real task-success data; running an inspection afterward adds a violation count beside evidence that already exists, and the two are easy to blur into one number that overstates how much is actually known. Skip it too when nothing concrete exists yet to walk: a single static mock or a blank page has no flow for a heuristic to be checked against, and the earlier-stage tools in [Interaction Design Principles](interaction-design-principles.md) or the [design brief](../../templates/definition/design-brief.md) fit that moment better.

## Nielsen's ten heuristics

Credited to Jakob Nielsen, per his own stated condition for reuse: [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/), Nielsen Norman Group. The ten names below are Nielsen's; the one-line gloss after each is this repository's own, not NN/g's description, example or tip, which the source page reserves for print or online reproduction under a separate permission this repository does not hold.

1. **Visibility of system status.** The interface keeps the user current on what state it is in and what its last action just did.
2. **Match between the system and the real world.** Words, order and icons follow the user's own language and mental model, not internal engineering terms.
3. **User control and freedom.** Every path in has a marked way out: undo, cancel, back, none of them buried.
4. **Consistency and standards.** The same word or control means the same thing everywhere in the product, and follows the conventions a user already carries in from elsewhere.
5. **Error prevention.** A likely mistake is designed out, or confirmed before it takes effect, rather than only explained afterward.
6. **Recognition rather than recall.** Information the user needs to act sits visible on the screen instead of living only in their memory.
7. **Flexibility and efficiency of use.** The same path serves a first-time user, while a frequent one gets a shortcut through it.
8. **Aesthetic and minimalist design.** Every element earns its place; nothing on the screen competes with what the user actually needs there.
9. **Help users recognize, diagnose, and recover from errors.** An error message says what happened, in plain language, and points at the fix.
10. **Help and documentation.** Findable, task-focused help exists for the cases the interface cannot make self-evident on its own.

## Shneiderman's eight golden rules

Attributed to Ben Shneiderman; names restated here in this repository's own words from [The Eight Golden Rules of Interface Design](https://www.cs.umd.edu/~ben/goldenrules.html).

1. **Strive for consistency.** The same term, layout and action apply to the same kind of task throughout the product.
2. **Seek universal usability.** Design for the actual range of users and contexts that will show up, novice through expert, including people relying on assistive technology.
3. **Offer informative feedback.** Every action gets a response sized to how significant that action is.
4. **Design dialogs to yield closure.** A sequence of steps has a clear beginning, middle and a satisfying end that tells the user the task is actually done.
5. **Prevent errors.** The interface is designed so a likely mistake either cannot be made, or is caught before it causes damage.
6. **Permit easy reversal of actions.** Actions can be undone, which frees a user to explore without fearing an unrecoverable mistake.
7. **Keep users in control.** The user initiates and directs the action; the system responds, rather than surprising the user with a change nobody asked for.
8. **Reduce short-term memory load.** Displays stay simple, related information is consolidated, and the user gets enough time to learn an action sequence.

Shneiderman is explicit that the eight rules need validation and tuning before they are applied to a specific domain; they are a starting checklist, not a finished one, in exactly the same way Nielsen's ten are rules of thumb rather than guidelines. One caution travels with rule 8 specifically: Shneiderman's own explanation still invokes Miller's 1956 figure of about seven items, plus or minus two, for how many chunks working memory holds (practitioner heuristic, as Shneiderman uses it). The stronger and more current evidence puts the practical limit closer to four (research evidence, Cowan); see the correction and its sourcing in [UX Laws Evidence Ledger](ux-laws-evidence.md) before citing Miller's seven-plus-or-minus-two figure as if it settled the question.

## Crosswalk against ISO 9241-110:2020

ISO 9241-110:2020, Ergonomics of human-system interaction, Part 110: Interaction principles, is read here at catalogue level only: the 32-page standard itself was not purchased or read, so what follows lists the standard's seven principle names against Nielsen's and Shneiderman's items and is a vocabulary crosswalk, not a compliance mapping. The standard explicitly excludes aesthetics, marketing and corporate identity from its scope. Its 2006 predecessor edition covered similar ground under the title "Dialogue principles"; the 2020 edition renamed the set "Interaction principles," folded a prior "individualisation" principle into controllability, and added user engagement as a new seventh principle.

| ISO 9241-110:2020 principle | Closest Nielsen heuristics | Closest Shneiderman rule |
|---|---|---|
| Suitability for the user's tasks | Match between the system and the real world; Flexibility and efficiency of use | Seek universal usability |
| Self-descriptiveness | Visibility of system status; Recognition rather than recall | Offer informative feedback |
| Conformity with user expectations | Consistency and standards; Match between the system and the real world | Strive for consistency |
| Learnability | Recognition rather than recall; Help and documentation | Reduce short-term memory load |
| Controllability | User control and freedom; Flexibility and efficiency of use | Permit easy reversal of actions; Keep users in control |
| Use error robustness | Error prevention; Help users recognize, diagnose, and recover from errors | Prevent errors |
| User engagement | No clean match; ISO's own scope note excludes aesthetics, marketing and corporate identity, and user engagement was added only in the 2020 edition | No clean match; the golden rules predate this principle and stop at usability, not engagement |

This table is this repository's own vocabulary mapping across three lists that were written for overlapping purposes, not evidence that the ideas are correct; a row where only one list has an entry is not a gap in that list, it is a reminder that no one of the three is complete on its own, and a row where all three have an entry says only that three authors used similar language for a similar idea, not that the idea has been independently confirmed.

## The task-based variant: cognitive walkthrough

Where an inspection against Nielsen's or Shneiderman's list asks whether a screen honors a set of general principles, the cognitive walkthrough asks a narrower, task-based question: at each step of one specific task, would a new user correctly guess the next action, notice that it was available, and understand the feedback it produced. The original method is Lewis, Polson, Wharton and Rieman (1990), cited here by title and year only, not fetched; a later streamlined form is Spencer (2000), cited here by title and year only, not fetched. Neither this card nor the worksheet describes what either paper's method actually contains; the runnable procedure and when to reach for one variant over the other are the worksheet's own construction, in the [Heuristic Evaluation](../../frameworks/design/heuristic-evaluation.md) worksheet's variant section.

## The evidence

Nielsen and Molich's four original experiments (CHI 1990, read here at OpenAlex abstract level; the ACM Digital Library paper itself was not fetched) found that individual evaluators working alone caught only 20 to 51 percent of the usability problems actually present in the interfaces they reviewed (research evidence, Nielsen and Molich 1990, abstract level). Aggregating the independent findings of three to five evaluators (research evidence, same source) did rather well by comparison, even though each of those evaluators individually missed most of the problems on their own. That gap between one evaluator and a small pool is the entire empirical basis for running heuristic evaluation as a panel rather than a solo pass, carried into the worksheet's own scoring.

A later synthesis, Hertzum and Jacobsen's review of the evaluator effect across 11 studies of heuristic evaluation, cognitive walkthrough and think-aloud testing (research evidence, Hertzum and Jacobsen 2001, abstract level), found that average agreement between any two evaluators looking at the same system, on which problems actually exist there, ranged from 5 to 65 percent. The effect held for novice and expert evaluators alike, and for severe problems as well as cosmetic ones; no one method proved consistently more reliable than the others. Two careful people inspecting the same screen will often produce substantially different problem lists, and that instability, not a flaw in any single evaluator, is a documented property of the method itself.

## The trap: inspection is not user evidence

A heuristic pass substitutes trained judgment for a data-gathering method such as an interview or a moderated usability test, and the evidence above shows exactly how much that substitution costs: one person, however careful, is one evaluator, and the numbers say one evaluator catches a minority of what is actually there. Running the pass again with the same one person the next morning does not fix this; it is the same evaluator finding roughly the same subset a second time.

This applies just as directly to a language model asked to list heuristic violations against a screenshot or a mockup, and it is no longer untested ground: the studies behind the 20-to-51-percent and evaluator-agreement numbers above all predate language models, but Duan et al. (CHI 2024, research evidence) built a GPT-4 heuristic-evaluation plugin, ran it against 51 UI mockups under three guideline sets including Nielsen's ten, and compared its output with human experts. GPT-4's feedback was useful for catching subtle errors, improving text and reasoning about UI semantics on a design's first pass, but its usefulness fell away across iterations as the design improved, the opposite of what a human panel is asked to do at Gate 3. Treat a single AI-run heuristic sweep as one more single-evaluator opinion to be pooled with others, exactly as the panel-size evidence recommends, useful earliest in a design's life and least where it matters most, on a design that has already been through a round of fixes.

## How it lies: a violation count is not a usability score

A heuristic evaluation produces a list of violations, each assigned a severity under NN/g's standard procedure. That list is genuinely useful for prioritizing fixes, and genuinely dangerous the moment it gets treated as a measurement. Two failure modes recur. First, a tidy scorecard, "twelve violations, down from twenty last release," looks like a trend line and is not one: a violation count is an artifact of how many screens got reviewed, how experienced the reviewer was that day, and how finely the heuristics were applied, none of which stays constant release over release, so the two numbers are not measuring the same thing twice.

Second, and more consequential, a violation count never stands in for whether a real user, attempting a real task, actually succeeds. That is what the task-success and happiness rows of the [HEART metrics](../../frameworks/metrics/heart-metrics.md) worksheet measure, not this card's method. A screen can clear a heuristic review with zero violations recorded and still fail its own task-success number, because a heuristic list catches generic, predictable problems and has nothing to say about the one thing specific to this task, this copy, this particular user's mental model, that only a person attempting the task will ever surface. A heuristic pass earns the right to say a screen has no obvious, predictable problems left; it never earns the right to say the screen works.

## Where it sits in the loop

- Stage: DESIGN, on the way to [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md#gate-3-architecture-and-risks-reviewed). The gate's own checklist is written at the system and integration level; this card's method operates one layer down, on the screens and flows that architecture carries, and its findings are what a screen-level design review brings to that gate rather than a line item the gate checklist states itself.
- Upstream: a concrete flow to inspect, coming out of the [design brief](../../templates/definition/design-brief.md) and acceptance criteria written in DEFINE; an inspection with nothing built yet has nothing to walk.
- Runs as: the [Heuristic Evaluation](../../frameworks/design/heuristic-evaluation.md) worksheet, which scores a pass against both named lists and offers the task-based variant above.
- Feeds: findings land in the [Design Review Record](../../templates/architecture/design-review-record.md), the signed artifact a heuristic pass answers to at Gate 3, and inform what a subsequent round of the [Usability Test Plan](../../templates/discovery/usability-test-plan.md) needs to probe with real participants rather than re-check by inspection.

## Used by

- [Heuristic Evaluation](../../frameworks/design/heuristic-evaluation.md), the runnable worksheet that scores a pass against both named lists and carries the cognitive-walkthrough variant.
- [Usability Test Plan](../../templates/discovery/usability-test-plan.md), which a heuristic pass's findings help scope before a moderated round is booked.
- [Design Review Record](../../templates/architecture/design-review-record.md), the signed record a heuristic pass's findings feed at Gate 3.

## Reading

Reuse classes below are registered in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md); this card follows that register.

- [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/), Jakob Nielsen, Nielsen Norman Group, 1994, last reviewed January 2024. All rights reserved; the page grants explicit permission to reuse the heuristics with credit to Jakob Nielsen and a link to the page, and reserves reproduction of its descriptions, tips and posters. Reuse class: cite only, per the NN/g register row; the one-line glosses above are this repository's own wording, not NN/g's, and the heuristic names and the credit-and-link permission are what is taken from the source itself.
- [Heuristic evaluation of user interfaces](https://api.openalex.org/works/doi:10.1145/97243.97281), Jakob Nielsen and Rolf Molich, ACM CHI 1990, DOI 10.1145/97243.97281. ACM copyright; read here at OpenAlex abstract level, the ACM Digital Library page itself was not fetched. Reuse class: cite only, paraphrase the finding.
- [How to Conduct a Heuristic Evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/), Kate Moran and Kelley Gordon, Nielsen Norman Group, 2023. All rights reserved. Reuse class: cite only; the runnable procedure this source describes is paraphrased with attribution in [Heuristic Evaluation](../../frameworks/design/heuristic-evaluation.md), not reproduced here.
- [The Eight Golden Rules of Interface Design](https://www.cs.umd.edu/~ben/goldenrules.html), Ben Shneiderman, from Designing the User Interface, 6th edition, Pearson, 2016, section 3.3.4. All rights reserved. Reuse class: paraphrase with attribution, rule names restated in this repository's own words.
- [ISO 9241-110:2020](https://www.iso.org/standard/75258.html), Ergonomics of human-system interaction, Part 110: Interaction principles, ISO, edition 2, May 2020. ISO copyright, a purchased standard; read at catalogue level only. Reuse class: cite only, principle names may be listed, the standard's text and recommendations are not reproduced.
- [The evaluator effect: a chilling fact about usability evaluation methods](https://forskning.ruc.dk/en/publications/the-evaluator-effect-a-chilling-fact-about-usability-evaluation-m), Morten Hertzum and Niels Ebbe Jacobsen, International Journal of Human-Computer Interaction, 2001. Publisher copyright (Taylor and Francis); read at abstract level. Reuse class: cite only, paraphrase the finding.
- [Generating Automatic Feedback on UI Mockups with Large Language Models](https://dl.acm.org/doi/10.1145/3613904.3642782), Peitong Duan, Jeremy Warner, Yang Li and Bjoern Hartmann, ACM CHI 2024, DOI 10.1145/3613904.3642782. ACM copyright; read here at the arXiv preprint and abstract level (arXiv:2403.13139), the ACM Digital Library version of record was not fetched. Reuse class: cite only, paraphrase the finding, by analogy with the register's existing ACM-venue rows. **Not yet added as its own row in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md)**: add it there before citing this source again.
- Lewis, C., Polson, P., Wharton, C., and Rieman, J. (1990), "Testing a walkthrough methodology for theory-based design of walk-up-and-use interfaces." Cited by title and year only, not fetched, no DOI on file. Reuse class: link only.
- Spencer, R. (2000), "The streamlined cognitive walkthrough method." Cited by title and year only, not fetched, no DOI on file. Reuse class: link only.
