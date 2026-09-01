# The PM Ladder: Associate PM to CPO

Eight rungs, one fork. Each rung below states what the role owns, what it alone decides, the documents it produces and consumes, what success looks like, the classic way the rung fails, and how the job bends by company stage. The shape draws on Marty Cagan's writing on product roles and product leadership, Melissa Perri's treatment of the product career path, and Lenny Rachitsky's published surveys of how companies actually level PMs; sources are listed at the end.

**The names are directional.** Real ladders differ: some companies fold Principal into Senior, some run Lead PM instead of Group PM, some stop at VP. Until verbatim company ladders are collected and cited here, use these rungs to locate scope, not to argue titles. What separates rungs is scope and the cost of the decisions trusted to you, not tenure.

**The fork.** After Senior PM the ladder splits. The IC track deepens judgment (Principal PM); the management track converts judgment into other people's output (Group PM and up). The fork is a real choice with different success measures, and companies that treat management as the only continuation lose their best product thinkers or, worse, promote them into managing badly.

## 1. Associate Product Manager

- **Owns:** a feature area inside someone else's product area, with a named supervising PM. The training rung: real users, real scope, bounded blast radius.
- **Decides:** ordering within the feature backlog, acceptance of individual stories against written criteria, which user questions to chase first.
- **Documents out:** [evidence notes](../../templates/discovery/evidence-note.md), [acceptance criteria](../../templates/definition/acceptance-criteria.md), user stories, meeting-ready summaries of research.
- **Documents in:** the parent area's [PRD](../../templates/definition/prd.md) and [user research plan](../../templates/discovery/user-research-plan.md); the team's [OKRs](../../templates/planning/okrs.md).
- **Success looks like:** small things shipped predictably, interviews run without leading the witness, and unknowns written down as unknowns instead of guessed at.
- **Classic failure mode:** mistaking activity for judgment. The APM who produces the most tickets, decks, and status updates while never once changing a decision with evidence is practicing the wrong craft.
- **Stage variance:** startups rarely carry APMs honestly; there is no supervision capacity, so the title usually means underpaid PM. See [stage-shift.md](stage-shift.md).

## 2. Product Manager

- **Owns:** a product area end to end through the operating loop, DISCOVER to OPERATE, including the four risks named in [empowered product teams](../cagan-product-teams.md): value and viability personally, usability and feasibility with design and engineering.
- **Decides:** what enters and leaves scope for a release, priority within the area, the weight of document each piece of work deserves per [WHICH-DOCUMENT](../../os/WHICH-DOCUMENT.md), and the go or no-go recommendation at each gate.
- **Documents out:** [discovery documents](../../templates/discovery/discovery-document.md), [PRDs](../../templates/definition/prd.md) or [one-pagers](../../templates/definition/one-pager.md), [metrics reviews](../../templates/operate/metrics-review.md), the area's slice of the [roadmap](../../templates/planning/roadmap.md).
- **Documents in:** product strategy and [vision](../../templates/planning/vision.md), company OKRs, research and [feedback synthesis](../../skills/feedback-synthesis/SKILL.md) output, architecture decisions that constrain the area.
- **Success looks like:** outcomes moved, not features shipped. Two or three releases where the metric named in the discovery document actually went where the hypothesis said, and one bet killed early with evidence.
- **Classic failure mode:** becoming a backlog administrator: collecting requests, sequencing them, and calling the sequence a strategy. The feature factory runs on exactly this rung.
- **Stage variance:** at a seed startup this title often covers the whole product and half of marketing; at an enterprise it may cover one screen of one workflow.

## 3. Senior Product Manager

- **Owns:** the hardest or most consequential product area, and increasingly the tradeoffs that cross team boundaries: sequencing against another team's dependency, spending political capital at a gate.
- **Decides:** cross-team tradeoffs within the line, when to escalate versus absorb, which fights are worth having, and how thin a document can safely be. Trusted to run a gate without an audience.
- **Documents out:** everything a PM produces, plus [risk registers](../../templates/execution/risk-register.md) and [dependency registers](../../templates/execution/dependency-register.md) that other teams actually consult, and roadmap positions defended in writing.
- **Documents in:** strategy at company altitude, board context when it leaks, other teams' PRDs for collision checks.
- **Success looks like:** being handed ambiguity and returning structure. Patterns this person invents (a sharper gate checklist, a better interview script) show up in other teams' work uncredited.
- **Classic failure mode:** the hero PM. Personally excellent, scales nothing, hoards the hard problems, and leaves a team that cannot run a discovery cycle without them. The rung exists to teach the opposite lesson before the fork.
- **Stage variance:** this is the most inflated title on the ladder; at small companies it is often the second PM hired, whatever their scope.

## 4. Principal Product Manager (IC track)

- **Owns:** problems no single team owns: a cross-cutting platform migration, a pricing model change that touches every area, the bet that redefines a product line. No reports; influence is the whole toolkit.
- **Decides:** product direction on questions where reversal is expensive and evidence is thin, jointly with senior engineering; when a one-way-door decision needs an [ADR](../../templates/architecture/adr.md) and a wider room.
- **Documents out:** strategy notes, system-level PRDs, [system design](../../templates/architecture/system-design.md) contributions, written positions that settle arguments other people were having.
- **Documents in:** effectively everything; the job is reading across boundaries that others read within.
- **Success looks like:** force multiplication. Decisions across several teams get better because this person wrote three pages nobody else could have written. Measured in outcomes of work they influenced, not work they ran.
- **Classic failure mode:** the roving architect: opinions on everything, accountability for nothing. A Principal PM with no named outcome in the current [OKRs](../okrs.md) has drifted into commentary.
- **Stage variance:** the rung barely exists below a few hundred people; a startup needing a Principal PM usually needs a VP who still ships.

## 5. Group Product Manager (management track)

- **Owns:** a group of two to five PMs and their combined outcomes, usually while still carrying one product area personally. The player-coach rung, and the first rung where [High Output Management](../high-output-management.md) applies literally: your output is now the team's output.
- **Decides:** which PM gets which problem, whether a gate submission from the group is honest, when to intervene in a team's work versus let a recoverable mistake teach.
- **Documents out:** the group's roadmap and OKRs, gate sign-offs, coaching and evaluation notes (which live in your company's people system, not in this repo).
- **Documents in:** every PRD, discovery document, and metrics review the group produces; read them as a coach reads film.
- **Success looks like:** PMs who visibly level up, and group outcomes that no longer route through you. The test: take two weeks off and count what stalled.
- **Classic failure mode:** the player who never coaches. Keeps doing the PM job for the group because doing is faster than teaching, reviews documents by rewriting them, and produces a team of stenographers.
- **Stage variance:** at scale-ups this rung appears suddenly and is staffed by whoever was senior when the music stopped; treat the title as directional and check whether coaching actually happens.

## 6. Director of Product

- **Owns:** a product line, several groups or teams, and the PM practice inside the line: who gets hired, what good looks like, which rituals are mandatory.
- **Decides:** the hiring bar, allocation of PMs across problems, roadmap conflicts between groups, and what escalates upward versus dies at their desk.
- **Documents out:** product-line strategy, quarterly business reviews upward, headcount cases, the line's [stakeholder map](../../templates/execution/stakeholder-map.md).
- **Documents in:** group roadmaps and metrics reviews, finance and sales context, the strategy from above that the line must serve.
- **Success looks like:** the line's outcomes plus bench strength: two people ready for every key seat, and gates that hold to the same standard whether or not the Director is in the room.
- **Classic failure mode:** the status-report router. Aggregates updates upward and pressure downward, adds no judgment in either direction, and calls the traffic management leadership.
- **Stage variance:** at a startup, Director of Product frequently has zero reports; the title marks salary band, not the job described here.

## 7. VP of Product

- **Owns:** the product organization itself: its strategy, its operating model, its leaders. Per Cagan's framing of product leadership, the job reduces to two duties done personally: coaching the leaders below and owning a strategy worth executing.
- **Decides:** the product strategy and its sequencing, the portfolio shape, the organization design, which markets and bets get starved to feed the ones that matter.
- **Documents out:** the [product strategy and vision](../../templates/planning/vision.md), portfolio-level roadmap, board materials, the operating rules the organization runs on (in this repo's terms: which gates are law).
- **Documents in:** everything at summary altitude, plus raw signal deliberately sampled: real interviews, real support tickets, real metrics reviews. A VP who consumes only summaries is flying on instruments someone else calibrated.
- **Success looks like:** a strategy that survives contact with three quarters of reality, and Directors who could each run product somewhere smaller tomorrow.
- **Classic failure mode:** administration without direction. The calendar fills with reviews, the strategy document ages, and the organization mistakes cadence for progress. The second form: losing customer contact entirely and defending the strategy from memory.
- **Stage variance:** at a startup the VP still writes PRDs; at an enterprise the VP who still writes PRDs is the bottleneck.

## 8. Chief Product Officer

- **Owns:** product across the company: the portfolio, the product P&L conversation, the leveling and craft standards every rung below runs on, and product's seat in company strategy.
- **Decides:** portfolio allocation across lines, build versus buy versus partner at company scale, the tradeoff between this year's number and the product that earns the years after, and who leads product in each division.
- **Documents out:** company product strategy, board updates, the investment theses that open or close whole product lines.
- **Documents in:** every line's strategy and quarterly review, plus the same deliberately sampled raw signal the VP needs, at higher cost and higher necessity.
- **Success looks like:** product is the reason the company wins its market, and the board treats product judgment as a company asset rather than a department. Perri's test is the sharp one: a real CPO changes what the company decides, not just what it builds.
- **Classic failure mode:** the renamed VP. Same scope, grander title, no seat at the decisions that shape the portfolio. The second form: going fully native to the board's altitude and becoming a very senior stranger to the product.
- **Stage variance:** below a few hundred people the title is almost always aspirational branding; ask what the person decides that a VP would not.

## Sources

- Marty Cagan, Inspired (2017) and Empowered (2020), with the SVPG essays on product roles: the four-risk vocabulary the IC rungs carry, and the reduction of product leadership to coaching plus strategy. See the [empowered product teams](../cagan-product-teams.md) card.
- Melissa Perri, Escaping the Build Trap (2018): the career-path chapter whose APM-to-CPO arc these rungs broadly follow, and the CPO-changes-decisions test.
- Lenny Rachitsky's newsletter surveys of PM career ladders: the observation that scope separates rungs while tenure merely correlates, and that the IC fork is real at strong companies.
- Andrew Grove, High Output Management (1983), via [the card in this repo](../high-output-management.md): the success measure for every management rung.
