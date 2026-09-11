---
layer: knowledge
stage: DEFINE
gate: 2
feeds: ["templates/definition/ui-state-inventory.md", "templates/architecture/component-spec.md", "templates/delivery/testing-strategy.md"]
method: ""
aliases: ["Component-Driven Development", "component-driven-development"]
---
# Component-Driven Development

Based on the component-driven development practice for experience design as documented by the Storybook project (storybookjs/storybook, commit 4431a2f, MIT, including its Autodocs documentation at storybook.js.org), the practice's name and its bottom-up build order as set out at componentdriven.org, and the term "frontend workshop" that Storybook's own docs credit to Brad Frost. Frost's separate design-system governance process (bradfrost.com), co-credited there to Inayaili de Leon Persson's earlier work at Canonical, is drawn on below for who signs off a component change. Explained here in this repository's own words.

## The essence

A frontend workshop is a place to build a user interface away from the running application: an isolated environment where one component renders on its own, free of the app's routing, data layer and business logic. Storybook's docs credit the term to Brad Frost, and componentdriven.org names the resulting practice and its order of work: build small, presentational components first, compose them into larger composites, then pages, and only then wire the page to real data. The isolation is the whole value: a component that renders correctly with no network, no auth and no sibling state is a component whose behavior you can actually pin down, because nothing else in the system can be silently making it work.

The unit that isolation produces is a story: one named, rendered state of one component. A component with a default look, a disabled look, an empty look, an error look and a long-text look has five stories, and that list is a complete, reviewable inventory of what the component can look like. This is the fact this card exists to state plainly: a story is not a developer convenience, it is the acceptance surface. Before component-driven development, the object a PM signed off was a screenshot or a live click-through, neither of which named its own states or stayed reachable after the review meeting. A story is addressable (it has a name and, once published, a URL), it is enumerable (a component's story list is the state inventory), and it renders the same way for a reviewer as it does for the developer who wrote it.

## Where it came from

Frost's Atomic Design work supplied the underlying build order (atoms into molecules into organisms into pages) that "bottom up" describes; componentdriven.org names the practice and gives it a home independent of any one tool. Storybook grew alongside that thinking as the most widely used implementation: a tool that renders one component at a time in its own workshop and turns each rendered state into a story a browser can load directly. The practice does not require Storybook specifically. It requires an isolated rendering environment, a name for each state that environment can reach, and a way to publish that environment so a reviewer can open it without a local build.

The governance half of this card, who may accept a change to a shared component, traces to a second and separate line of Frost's writing: his design-system governance process. That process describes a product team reaching a design system team when a component does not fit their need, the two teams agreeing whether the work is a one-off ("snowflake") or belongs in the shared system, and, when it belongs in the system, the work going through a joint review, testing and a named product-team sign-off before it releases. The relevant fact for this card is narrower than the whole process: the person accepting a shared component's new or changed appearance is not the person who built it, and the acceptance is a recorded step, not a private judgment call.

## When to use it

- Turning a design brief's states into a reviewable list before code review starts, so the [UI state inventory](../../templates/definition/ui-state-inventory.md) has a named target for every state a component must reach.
- Writing an acceptance criterion for anything with a visible interface, so the criterion can be phrased as a state a reviewer will actually open, not as a paragraph of intent.
- Reviewing a built component without reading its code: a published story, pinned to a build, is something a PM, a designer or an accessibility reviewer can open directly.
- Deciding what a [component spec](../../templates/architecture/component-spec.md) must declare before a component is treated as shared and reusable rather than a one-off.

**Skip it when:** the work is a throwaway prototype that will be discarded after one review, the interface has no components meant to be reused, or the deliverable is a single marketing page with no interactive states. Building an isolated workshop and a story per state costs real time, and that cost is paid back only when a component will be looked at, changed or reused more than once. Skip it too when nothing has been designed yet: a state inventory needs states to enumerate, and the [design brief](../../templates/definition/design-brief.md) is where those states first get named.

## A story is a named rendered state

A story renders one specific set of inputs and nothing else. Its name is the state it captures: default, disabled, empty, loading, error, long or overflowing content, and so on. Two things follow from this that a PM can rely on without reading a line of code. First, the component's full list of stories is its state inventory, so "which states must exist" is a decision a PM can write down in the design brief and later check against the sidebar of story names, state by state. Second, because Storybook's own documentation builds an autogenerated component page directly from the same stories and their inputs, the same list that a developer writes for testing becomes the human-readable specification a reviewer reads, with no second document to keep in sync. Autodocs is a convenience for keeping the spec current, not a review mechanism in its own right: the spec is only as complete as the state inventory that drives it, and an inventory with a gap in it produces documentation with the same gap.

## Args are GIVEN, play steps are WHEN, assertions are THEN

A story's starting inputs set up a precondition. An interaction script, run against that story, drives one or more user actions. An assertion at the end checks one observable outcome. That is the same shape as the GIVEN, WHEN, THEN structure already used in this repository's [acceptance criteria](../../templates/definition/acceptance-criteria.md): the story's inputs are the GIVEN, the interaction steps are the WHEN, and the assertions are the THEN. Storybook groups a sequence of interaction steps under human-readable labels shown in a dedicated panel, and that label is exactly where an acceptance-criterion ID belongs: a step labeled with the criterion it verifies turns "QA says it passes" into a labeled, reproducible step a reviewer can watch run.

Every criterion phrased this way names a role and an accessible label, never an implementation detail: "the button named Submit," "the field labeled Email," never a CSS class or an internal test hook. This is not a style preference borrowed loosely from testing practice; it follows the query order Storybook's own testing documentation recommends, which finds elements by accessible role and label first and falls back to an internal test identifier only as a last resort, "the way a real person would" find them. A criterion written this way is doubly useful: it reads the same to a PM checking acceptance and to an assistive-technology user checking that the control has a real name, so the acceptance criterion and an accessibility check are, for that one control, the same sentence.

## Four test types, and what each costs to maintain

A story is tool-agnostic. Storybook, Chromatic or any equivalent workshop and publishing tool can run these four kinds of check against it; this repository names no vendor and never requires a commercial service to complete a review.

- **Render.** The story loads without throwing. This is nearly free, it runs automatically for every story that exists, and it catches nothing beyond an outright crash. Every story gets this for the cost of writing the story.
- **Interaction.** A scripted sequence of user actions runs against the story and asserts an outcome, the WHEN and THEN pair above. This is the most expensive type to keep current, because a script written against today's markup can break on a harmless refactor tomorrow. Reserve it for stateful behavior tied to a specific acceptance criterion, not for every story a component has; a component's static, non-interactive states are proven by the render and visual checks instead.
- **Accessibility.** An automated ruleset runs against the rendered DOM and reports violations, passes and items it cannot decide on its own. This check finds a share of accessibility problems, never all of them, and its default ruleset and severity are configuration choices someone has to set deliberately to match whatever conformance target the product actually committed to; a default left unexamined is not the same as a target chosen. A per-component mode that silently skips a check produces no visible failure and no visible record either, so any component left in that mode is accessibility debt that belongs in a findings list, not in silence.
- **Visual.** A rendered story's pixels are compared against a saved baseline, and a person accepts the new pixels as the baseline or fixes an unintended change. This is the cheapest type to keep running once it exists, and the one place in this list where a human judgment call is unavoidable: accepting a new baseline is a product decision that a specific change was intended, not a maintenance chore to wave through.

None of the four proves that a real user, moving through the actual product, ever reaches the state being checked. That is what the trap below is about.

## What counts as evidence

A component acceptance review runs on a published build, and four rules keep that review honest.

A story permalink is evidence only paired with a build or commit identifier. A link to "the story" with no build attached can point at a version that no longer exists by the time anyone reads the link, so a reviewer who cites a story as evidence names the build it was opened on.

A status shown in a sidebar, a badge or a check mark is a claim until a person opens the story behind it and looks. This is the same rule this repository applies everywhere else evidence is claimed: a green indicator is somebody's assertion, not a substitute for the reviewer's own look.

A visual-baseline acceptance needs two things to count: a decision-log or change-request entry recording that the new appearance was intended, and a named role that is not the component's author doing the accepting. This follows directly from Frost's governance process, where a component change reaching the shared system goes through a joint review and a distinct sign-off step rather than resting on the word of whoever built it. An author accepting their own visual change is not a review; it is a note to self.

A list of stories an agent curated, or a set a change-detection tool flagged as new or modified, is a starting point for a review and never the review's scope. Storybook's own documentation is explicit that such a curated list is "not a comprehensive list" and that change detection can produce false positives. A reviewer who stops at the flagged subset has reviewed the tool's guess at what changed, not the change itself; the full state inventory is the scope, and the flagged list is only where to look first.

## States are composed, not propped

A state a user can see is made of everything visibly different about the screen in that state, not one internal flag a developer happened to name it after. A loading state is not a boolean; it is usually a spinner, a disabled submit control, and a status announcement together, and each of those three pieces can be present, absent or wrong independently of the others. Writing a criterion or a story name against "isLoading: true" describes the code, not the interface, and it can pass while the actual composed state on screen is broken: the spinner shows, but the button underneath it is still clickable, or the control is disabled but nothing tells an assistive-technology user why. A state's definition is what a person looking at (or listening to) the rendered screen would report seeing, and that is also why the query order in the GIVEN, WHEN, THEN section above matters here too: the state is proven by what is visible and reachable, not by what a prop was set to.

## The trap: a green workshop, a broken journey

An isolated workshop's whole value, no interference from the app's routing, data or business logic, is also its blind spot. A story renders a component with mocked args standing in for real data, real permissions and real network conditions, so every one of the four test types above can pass while the same component fails the moment it sits inside the actual page, behind the actual authentication state, receiving actual data from a service that can be slow, empty or wrong in ways no mock anticipated. Storybook's own documentation names the fix as an order of operations, not an alternative method: build and test components first, then composites, then pages, and only full end-to-end tests on the real stack can tell you the journey between pages still works. Accepting every state in the workshop is a necessary step toward accepting a feature; it is never a substitute for walking the actual journey a user will take, and a reviewer who treats a fully green workshop as proof that the journey works has mistaken a component-level result for a system-level one.

## How it lies

Two things in this practice look like more coverage than they are. The first is a deliberately silent accessibility mode some tooling offers, distinct from an outright "off" mode: a component set to that mode produces no failure in the pipeline and, from the outside, looks identical to a component that was checked and passed. A pipeline that is all green can be all green because everything was checked and everything is fine, or because a portion of it was quietly told not to check at all, and nothing in a green build distinguishes the two without someone going and looking at each component's mode. The second is an "incomplete" or "needs manual confirmation" result from an automated accessibility pass, which is not a pass: an automated check that cannot decide is reporting exactly the boundary of what automation can verify, and treating an unreviewed "incomplete" item as though it were a pass moves a real open question into the blind spot where nobody owns it.

## Where it sits in the loop

- Stage: DEFINE, on the way to [Gate 2: requirements signed off](../../os/STAGE-GATES.md#gate-2-requirements-signed-off). The states a component must reach are named at DEFINE time, alongside the acceptance criteria they carry, not invented later once a developer is already mid-build.
- Upstream: the states a screen or flow needs come out of the [design brief](../../templates/definition/design-brief.md) and the [acceptance criteria](../../templates/definition/acceptance-criteria.md) written in DEFINE; a story with no named state behind it is a developer's guess at what mattered.
- Downstream: the [UI state inventory](../../templates/definition/ui-state-inventory.md) is where each component's required states are listed and later matched to a story permalink at a build. The [component spec](../../templates/architecture/component-spec.md) is where a shared, reusable component declares its variants and states as a reviewable contract, at DESIGN. The [testing strategy](../../templates/delivery/testing-strategy.md) is where the four test types above get an owner, a blocking rule and a place in the release gate, at DELIVER feeding [Gate 5: release readiness green](../../os/STAGE-GATES.md#gate-5-release-readiness-green).
- Reviewed by: the [acceptance agent](../../agents/acceptance-agent.md), which turns acceptance criteria into test cases and checks that Gate 4 evidence actually exists rather than assuming a pass.

## Used by

- [UI state inventory](../../templates/definition/ui-state-inventory.md), which lists the named states this card defines and later carries the story permalink each one resolves to.
- [Component spec](../../templates/architecture/component-spec.md), where a shared component's variant and state contract is declared for reuse.
- [Testing strategy](../../templates/delivery/testing-strategy.md), which assigns an owner and a blocking rule to each of the four test types above.

## Reading

Reuse classes below are registered in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md); this card follows that register.

- [storybookjs/storybook](https://github.com/storybookjs/storybook), commit 4431a2f. MIT. Reuse class: paraphrase with attribution. Source for stories as named rendered states, the GIVEN, WHEN, THEN mapping and interaction step labels, the four test types and their default rulesets and modes, published-build review, and the "not a comprehensive list" and change-detection caveats.
- [Automatic documentation and Storybook (Autodocs)](https://storybook.js.org/docs/writing-docs/autodocs), part of the same repository and licence above. Reuse class: paraphrase with attribution. Source for autodocs building a documentation page from the same stories and inputs that define a component's states.
- [componentdriven.org](https://www.componentdriven.org/), the site that names the component-driven development practice and its bottom-up build order. No licence verified for this card. Reuse class: cite only; named here by title, not adapted or quoted.
- [A Design System Governance Process](https://bradfrost.com/blog/post/a-design-system-governance-process/), Brad Frost, credited there to earlier work by Inayaili de Leon Persson at Canonical. All rights reserved, no licence found on the page. Reuse class: paraphrase with attribution. Source for the joint review and named, non-author sign-off a shared component change goes through before release.
