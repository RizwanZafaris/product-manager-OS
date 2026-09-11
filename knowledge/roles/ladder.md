---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["The PM Ladder", "ladder"]
---
# The PM Ladder: Associate PM to CPO

Eight rungs, one fork. Each rung below states what the role owns, what it alone decides, the documents it produces and consumes, what success looks like, the classic way the rung fails, and how the job bends by company stage. The shape draws on Marty Cagan's writing on product roles and product leadership, Melissa Perri's treatment of the product career path, and Lenny Rachitsky's published surveys of how companies actually level PMs; sources are listed at the end.

**The names are directional.** Real ladders differ: some companies fold Principal into Senior, some run Lead PM instead of Group PM, some stop at VP. Until verbatim company ladders are collected and cited here, use these rungs to locate scope, not to argue titles. What separates rungs is scope and the cost of the decisions trusted to you, not tenure.

**The fork.** After Senior PM the ladder splits. The IC track deepens judgment (Principal PM); the management track converts judgment into other people's output (Group PM and up). The fork is a real choice with different success measures, and companies that treat management as the only continuation lose their best product thinkers or, worse, promote them into managing badly.

## 1. Associate Product Manager

- **Owns:** a feature area inside someone else's product area, with a named supervising PM. The training rung: real users, real scope, bounded blast radius.
- **Decides:** ordering within the feature backlog, acceptance of individual stories against written criteria, which user questions to chase first.
- **Documents out:** [evidence notes](../../templates/discovery/evidence-note.md), [acceptance criteria](../../templates/definition/acceptance-criteria.md), [user stories](../../templates/definition/user-stories.md), [interview notes](../../templates/discovery/interview-notes.md), meeting-ready summaries of research.
- **Documents in:** the parent area's [PRD](../../templates/definition/prd.md) and [user research plan](../../templates/discovery/user-research-plan.md); the team's [OKRs](../../templates/planning/okrs.md).
- **Recurring workflows:** [user interview](../../skills/user-interview/SKILL.md) runs the sessions this rung turns into evidence notes. [Story writer](../../skills/story-writer/SKILL.md) decomposes the supervising PM's PRD into the stories this rung accepts against.
- **Filled examples at this level:** [sahulat-acceptance-criteria.md](../../examples/sahulat-acceptance-criteria.md), the written bar an APM accepts stories against, one story at a time; [sahulat-interview-notes.md](../../examples/sahulat-interview-notes.md), the raw session record this rung turns into evidence, not a summary written after the fact; [sahulat-interview-guide.md](../../examples/sahulat-interview-guide.md), a script an APM runs without leading the witness; [sahulat-mom-test-interview-guide.md](../../examples/sahulat-mom-test-interview-guide.md), the same discipline applied to a specific anti-leading technique this rung is drilled on.
- **Success looks like:** small things shipped predictably, interviews run without leading the witness, and unknowns written down as unknowns instead of guessed at.
- **Classic failure mode:** mistaking activity for judgment. The APM who produces the most tickets, decks, and status updates while never once changing a decision with evidence is practicing the wrong craft.
- **Stage variance:** startups rarely carry APMs honestly; there is no supervision capacity, so the title usually means underpaid PM. See [stage-shift.md](stage-shift.md).

## 2. Product Manager

- **Owns:** a product area end to end through the operating loop, DISCOVER to OPERATE, including the four risks named in [empowered product teams](../cagan-product-teams.md): value and viability personally, usability and feasibility with design and engineering.
- **Decides:** what enters and leaves scope for a release, priority within the area, the weight of document each piece of work deserves per [WHICH-DOCUMENT](../../os/WHICH-DOCUMENT.md), and the go or no-go recommendation at each gate.
- **Documents out:** [discovery documents](../../templates/discovery/discovery-document.md), [PRDs](../../templates/definition/prd.md) or [one-pagers](../../templates/definition/one-pager.md), [metrics reviews](../../templates/operate/metrics-review.md), the area's slice of the [roadmap](../../templates/planning/roadmap.md).
- **Documents in:** product strategy and [vision](../../templates/planning/vision.md), company OKRs, research and [feedback synthesis](../../skills/feedback-synthesis/SKILL.md) output, architecture decisions that constrain the area.
- **Recurring workflows:** the [conductor](../../skills/conductor/SKILL.md) runs the six-stage loop as an interview, this rung's own terrain. [Write PRD](../../skills/write-prd/SKILL.md) sizes and drafts the requirements stack the area needs. [Product review](../../skills/product-review/SKILL.md) is the weekly ritual that keeps the area's work visible before it reaches a gate.
- **Filled examples at this level:** [expense-copilot-discovery.md](../../examples/expense-copilot-discovery.md), a full DISCOVER pass an area PM runs end to end; [expense-copilot-prd.md](../../examples/expense-copilot-prd.md), the requirements document this rung owns and signs for its area; [ledgerline-metrics-review.md](../../examples/ledgerline-metrics-review.md), the outcome check that tells this rung whether the hypothesis held; [sahulat-opportunity-scoring.md](../../examples/sahulat-opportunity-scoring.md), the priority call within the area this rung decides alone.
- **Success looks like:** outcomes moved, not features shipped. Two or three releases where the metric named in the discovery document actually went where the hypothesis said, and one bet killed early with evidence.
- **Classic failure mode:** becoming a backlog administrator: collecting requests, sequencing them, and calling the sequence a strategy. The feature factory runs on exactly this rung.
- **Stage variance:** at a seed startup this title often covers the whole product and half of marketing; at an enterprise it may cover one screen of one workflow.

## 3. Senior Product Manager

- **Owns:** the hardest or most consequential product area, and increasingly the tradeoffs that cross team boundaries: sequencing against another team's dependency, spending political capital at a gate.
- **Decides:** cross-team tradeoffs within the line, when to escalate versus absorb, which fights are worth having, and how thin a document can safely be. Trusted to run a gate without an audience.
- **Documents out:** everything a PM produces, plus [risk registers](../../templates/execution/risk-register.md) and [dependency registers](../../templates/execution/dependency-register.md) that other teams actually consult, [decision memos](../../templates/planning/decision-memo.md) for the fights not worth absorbing, and [roadmap](../../templates/planning/roadmap.md) positions defended in writing.
- **Documents in:** strategy at company altitude, board context when it leaks, other teams' PRDs for collision checks.
- **Recurring workflows:** [program premortem](../../skills/program-premortem/SKILL.md) runs before a cutover or Gate 3, checking the twelve failure modes this rung is trusted to catch early. [Escalation](../../skills/escalation/SKILL.md) turns a stuck decision into a one-page brief when absorbing the fight would cost more than raising it.
- **Filled examples at this level:** [harbourgate-risk-register.md](../../examples/harbourgate-risk-register.md), the register other teams actually consult because a Senior PM keeps it honest; [harbourgate-dependency-register.md](../../examples/harbourgate-dependency-register.md), the cross-team collision map this rung is trusted to keep current; [sahulat-decision-log.md](../../examples/sahulat-decision-log.md), the named-decider record that survives a gate audit; [harbourgate-premortem-worksheet.md](../../examples/harbourgate-premortem-worksheet.md), the failure-mode pass this rung runs before a cutover it is trusted to own.
- **Success looks like:** being handed ambiguity and returning structure. Patterns this person invents (a sharper gate checklist, a better interview script) show up in other teams' work uncredited.
- **Classic failure mode:** the hero PM. Personally excellent, scales nothing, hoards the hard problems, and leaves a team that cannot run a discovery cycle without them. The rung exists to teach the opposite lesson before the fork.
- **Stage variance:** this is the most inflated title on the ladder; at small companies it is often the second PM hired, whatever their scope.

## 4. Principal Product Manager (IC track)

- **Owns:** problems no single team owns: a cross-cutting platform migration, a pricing model change that touches every area, the bet that redefines a product line. No reports; influence is the whole toolkit.
- **Decides:** product direction on questions where reversal is expensive and evidence is thin, jointly with senior engineering; when a one-way-door decision needs an [ADR](../../templates/architecture/adr.md) and a wider room.
- **Documents out:** [strategy notes](../../templates/planning/product-strategy.md), system-level PRDs, [system design](../../templates/architecture/system-design.md) contributions, [ADRs](../../templates/architecture/adr.md) for the one-way-door calls, and [decision memos](../../templates/planning/decision-memo.md), the written positions that settle arguments other people were having.
- **Documents in:** effectively everything; the job is reading across boundaries that others read within.
- **Recurring workflows:** [decision memo](../../skills/decision-memo/SKILL.md) writes the one-way-door call this rung is trusted with, priced and recommended in one read. [Strategy critic](../../skills/strategy-critic/SKILL.md) stress-tests a strategy draft before it reaches a room this person cannot personally staff.
- **Filled examples at this level:** [harbourgate-adr.md](../../examples/harbourgate-adr.md), the one-way-door architecture call this rung writes jointly with senior engineering; [harbourgate-system-design.md](../../examples/harbourgate-system-design.md), a system-level contribution that crosses every team's boundary at once; [ledgerline-strategy-kernel.md](../../examples/ledgerline-strategy-kernel.md), the strategy note that reads across areas nobody else is positioned to read across; [ledgerline-decision-memo.md](../../examples/ledgerline-decision-memo.md), the written position that settles an argument other people were having.
- **Success looks like:** force multiplication. Decisions across several teams get better because this person wrote three pages nobody else could have written. Measured in outcomes of work they influenced, not work they ran.
- **Classic failure mode:** the roving architect: opinions on everything, accountability for nothing. A Principal PM with no named outcome in the current [OKRs](../okrs.md) has drifted into commentary.
- **Stage variance:** the rung barely exists below a few hundred people; a startup needing a Principal PM usually needs a VP who still ships.

## 5. Group Product Manager (management track)

- **Owns:** a group of two to five PMs and their combined outcomes, usually while still carrying one product area personally. The player-coach rung, and the first rung where [High Output Management](../high-output-management.md) applies literally: your output is now the team's output.
- **Decides:** which PM gets which problem, whether a gate submission from the group is honest, when to intervene in a team's work versus let a recoverable mistake teach.
- **Documents out:** the group's [roadmap](../../templates/planning/roadmap.md) and [OKRs](../../templates/planning/okrs.md), gate sign-offs on the gate forms filed under the product workspace per [STAGE-GATES](../../os/STAGE-GATES.md), the [decision log](../../templates/execution/decision-log.md) entries that name a decider for every scope change the next gate will ask about, the [hiring scorecard](../../templates/execution/hiring-scorecard.md) for every seat the group fills, and coaching and evaluation notes (which live in your company's people system, not in this repo).
- **Documents in:** every PRD, discovery document, and metrics review the group produces; read them as a coach reads film.
- **Recurring workflows:** [OKR critic](../../skills/okr-critic/SKILL.md) reviews the group's OKR set before it cascades, catching key results that are really tasks in disguise. [Product review](../../skills/product-review/SKILL.md) is the ritual this rung runs for the group instead of personally producing the work.
- **Filled examples at this level:** [ledgerline-okrs.md](../../examples/ledgerline-okrs.md), the group's OKR set this rung defends before it cascades to individual PMs; [sahulat-hiring-scorecard.md](../../examples/sahulat-hiring-scorecard.md), the scorecard filled for every seat the group fills, a coaching artifact no IC rung owns; [ledgerline-status-report.md](../../examples/ledgerline-status-report.md), the rollup that replaces this rung personally producing the work; [harbourgate-raci.md](../../examples/harbourgate-raci.md), the who-decides map a player-coach uses to hand a problem to the right PM.
- **Success looks like:** PMs who visibly level up, and group outcomes that no longer route through you. The test: take two weeks off and count what stalled.
- **Classic failure mode:** the player who never coaches. Keeps doing the PM job for the group because doing is faster than teaching, reviews documents by rewriting them, and produces a team of stenographers.
- **Stage variance:** at scale-ups this rung appears suddenly and is staffed by whoever was senior when the music stopped; treat the title as directional and check whether coaching actually happens.

## 6. Director of Product

- **Owns:** a product line, several groups or teams, and the PM practice inside the line: who gets hired, what good looks like, which rituals are mandatory.
- **Decides:** the hiring bar, allocation of PMs across problems, roadmap conflicts between groups, and what escalates upward versus dies at their desk.
- **Documents out:** [product-line strategy](../../templates/planning/product-strategy.md), [quarterly business reviews](../../templates/operate/qbr-board-update.md) upward, headcount cases costed in the [capacity plan](../../templates/planning/capacity-plan.md), the line's [stakeholder map](../../templates/execution/stakeholder-map.md).
- **Documents in:** group roadmaps and metrics reviews, finance and sales context, the strategy from above that the line must serve.
- **Recurring workflows:** [PM hiring](../../skills/pm-hiring/SKILL.md) runs the loop that sets the hiring bar this rung owns. [Roadmap builder](../../skills/roadmap-builder/SKILL.md) turns the line's backlog and strategy into the sequenced plan a QBR can defend.
- **Filled examples at this level:** [harbourgate-stakeholder-map.md](../../examples/harbourgate-stakeholder-map.md), the line's stakeholder map this rung keeps current across several groups; [harbourgate-product-operating-model-assessment.md](../../examples/harbourgate-product-operating-model-assessment.md), the operating-model assessment this rung uses to set what is mandatory across groups the Director owns; [example-program-charter.md](../../examples/example-program-charter.md), the line-level charter that sets what is mandatory across groups the Director owns; [harbourgate-operational-readiness-review.md](../../examples/harbourgate-operational-readiness-review.md), the readiness standard this rung holds constant whether or not they are in the room.
- **Success looks like:** the line's outcomes plus bench strength: two people ready for every key seat, and gates that hold to the same standard whether or not the Director is in the room.
- **Classic failure mode:** the status-report router. Aggregates updates upward and pressure downward, adds no judgment in either direction, and calls the traffic management leadership.
- **Stage variance:** at a startup, Director of Product frequently has zero reports; the title marks salary band, not the job described here.

## 7. VP of Product

- **Owns:** the product organization itself: its strategy, its operating model, its leaders. Per Cagan's framing of product leadership, the job reduces to two duties done personally: coaching the leaders below and owning a strategy worth executing.
- **Decides:** the product strategy and its sequencing, the portfolio shape, the organization design, which markets and bets get starved to feed the ones that matter.
- **Documents out:** the [product strategy](../../templates/planning/product-strategy.md) and [vision](../../templates/planning/vision.md), the portfolio-level [roadmap](../../templates/planning/roadmap.md), board materials in the [QBR / board update](../../templates/operate/qbr-board-update.md) format, fed by the monthly [exec update](../../templates/planning/exec-update.md) that rolls up into it, the operating rules the organization runs on (in this repo's terms: which gates are law).
- **Documents in:** everything at summary altitude, plus raw signal deliberately sampled: real interviews, real support tickets, real metrics reviews. A VP who consumes only summaries is flying on instruments someone else calibrated.
- **Recurring workflows:** [write vision and strategy](../../skills/write-vision-strategy/SKILL.md) drafts the strategy this rung owns personally, handed to strategy-critic for the attack pass. [Stakeholder update](../../skills/stakeholder-update/SKILL.md) writes the board or exec update that puts the decisions needed on the first page.
- **Filled examples at this level:** [ledgerline-gtm-plan.md](../../examples/ledgerline-gtm-plan.md), a launch plan for one add-on to six design partners this rung sets across markets and channels; [ledgerline-north-star-tree.md](../../examples/ledgerline-north-star-tree.md), the metric tree the organization's strategy answers to; [ledgerline-qbr-board-update.md](../../examples/ledgerline-qbr-board-update.md), the board-format update this rung owns personally rather than rolling up from a Director; [harbourgate-product-operating-model-assessment.md](../../examples/harbourgate-product-operating-model-assessment.md), the operating-rules check that sets which gates are law across the organization.
- **Success looks like:** a strategy that survives contact with three quarters of reality, and Directors who could each run product somewhere smaller tomorrow.
- **Classic failure mode:** administration without direction. The calendar fills with reviews, the strategy document ages, and the organization mistakes cadence for progress. The second form: losing customer contact entirely and defending the strategy from memory.
- **Stage variance:** at a startup the VP still writes PRDs; at an enterprise the VP who still writes PRDs is the bottleneck.

## 8. Chief Product Officer

- **Owns:** product across the company: the portfolio, the product P&L conversation, the leveling and craft standards every rung below runs on, and product's seat in company strategy.
- **Decides:** portfolio allocation across lines, build versus buy versus partner at company scale, the tradeoff between this year's number and the product that earns the years after, and who leads product in each division.
- **Documents out:** company [product strategy](../../templates/planning/product-strategy.md), [board updates](../../templates/operate/qbr-board-update.md), the investment theses in the [business case](../../templates/planning/business-case.md) that open or close whole product lines.
- **Documents in:** every line's strategy and quarterly review, plus the same deliberately sampled raw signal the VP needs, at higher cost and higher necessity.
- **Recurring workflows:** [strategy critic](../../skills/strategy-critic/SKILL.md) attacks company strategy before it reaches the board, the same pass a VP's strategy gets, at higher cost when it is wrong. [Market sizing](../../skills/market-sizing/SKILL.md) sizes the bets big enough to open or close a product line.
- **Filled examples at this level:** [ledgerline-business-case.md](../../examples/ledgerline-business-case.md), the investment thesis that funded v1 on internal time savings alone and opens or closes a whole product line; [sahulat-market-sizing.md](../../examples/sahulat-market-sizing.md), the sizing pass behind a bet large enough to reach the board; [ledgerline-swot-tows.md](../../examples/ledgerline-swot-tows.md), the company-strategy stress test this rung defends before the board sees it; [ledgerline-build-buy-partner.md](../../examples/ledgerline-build-buy-partner.md), the build-versus-buy-versus-partner read at company scale.
- **Success looks like:** product is the reason the company wins its market, and the board treats product judgment as a company asset rather than a department. Perri's test is the sharp one: a real CPO changes what the company decides, not just what it builds.
- **Classic failure mode:** the renamed VP. Same scope, grander title, no seat at the decisions that shape the portfolio. The second form: going fully native to the board's altitude and becoming a very senior stranger to the product.
- **Stage variance:** below a few hundred people the title is almost always aspirational branding; ask what the person decides that a VP would not.

## Sources

- Marty Cagan, Inspired (2017) and Empowered (2020), with the SVPG essays on product roles: the four-risk vocabulary the IC rungs carry, and the reduction of product leadership to coaching plus strategy. See the [empowered product teams](../cagan-product-teams.md) card.
- Melissa Perri, Escaping the Build Trap (2018): the career-path chapter whose APM-to-CPO arc these rungs broadly follow, and the CPO-changes-decisions test.
- Lenny Rachitsky's newsletter surveys of PM career ladders: the observation that scope separates rungs while tenure merely correlates, and that the IC fork is real at strong companies.
- Andrew Grove, High Output Management (1983), via [the card in this repo](../high-output-management.md): the success measure for every management rung.
