---
layer: knowledge
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/user-research-plan.md", "templates/discovery/discovery-document.md", "templates/discovery/journey-map.md"]
method: ""
aliases: ["Continuous Discovery", "torres-continuous-discovery"]
---
# Continuous Discovery

Based on the ideas in Continuous Discovery Habits by Teresa Torres (2021).

## The essence

Traditional research happens in phases: a study is commissioned, weeks pass, a report lands, and by then the decisions it was meant to inform have been made on instinct. Torres replaces the phase with a habit. The product trio (product manager, designer, engineer) talks to customers every week, in small touchpoints, as a standing part of how the team works rather than an event someone schedules when things go wrong.

The structural tool is the opportunity solution tree. At the root sits the outcome the team is driving. Beneath it branch opportunities: needs, pain points, and desires heard directly from customers, phrased in the customer's terms, not the team's. Beneath each opportunity hang candidate solutions, and beneath solutions hang the assumption tests that would tell you cheaply whether a solution deserves to live. The tree does three jobs at once: it forces solutions to trace back to a heard customer need, it makes the team compare opportunities against each other instead of falling for the most recent interview, and it turns "what should we build?" into the smaller, answerable question "which assumption should we test this week?"

The weekly cadence is the point. One interview a week beats twelve interviews once a year, because the twelve arrive after the decision and the one arrives before it.

The mechanism is decision latency, not research volume. A team's quality of judgment is bounded by how long it takes to get evidence about a question, because any question whose answer takes six weeks will be settled by opinion in week one. Shrinking that interval changes which questions are worth asking: when a customer conversation is four days away, "we do not know" becomes a workable answer in a planning meeting rather than an embarrassment. That is the whole return on the habit, and it explains why a small continuous sample beats a large periodic one despite being worse research by every statistical measure.

The trio is the second mechanism, and it is about transmission rather than headcount. Research findings normally have to be sold: a report is written, circulated, and argued with by people who were not in the room and who reasonably discount a summary. When the engineer heard the customer struggle directly, the finding needs no advocate, and the design constraint arrives at the person who would otherwise have discovered it two months later as a rework. Discovery done by one person on behalf of a team pays the transmission cost in full every time.

The tree's quieter contribution is that it makes comparison possible. Without it, discovery produces a queue of findings and the team acts on the most recent one, because recency is the only ordering a queue has. With opportunities laid out beside each other under one outcome, the question becomes which of these to serve, which is answerable, rather than whether to serve this one, which is not.

## Where it came from

The book codifies a coaching practice, and it is a reaction to two things product teams tried in the years before it. The first was research as a service, where a dedicated research function ran studies for teams, which produced good research and slow decisions, because the study's timeline was set by the function's queue rather than by the team's question. The second was dual-track agile, described by Desiree Sy and popularized by Marty Cagan and Jeff Patton, which put discovery and delivery in parallel streams and left unspecified how discovery actually gets done week to week.

Continuous discovery is the answer to that unspecified part, which is why so much of the book is about mechanics: recruiting, interview snapshots, the trio's calendar. Read against that history, the tree is less a diagram than an argument that a team can hold its own research questions rather than outsourcing them, and the weekly cadence is the smallest commitment that keeps the questions the team's own.

## What the habit assumes

1. **Users are reachable weekly.** Not merely existent. A habit built on a recruiting channel that produces one conversation a month is a broken promise that discredits the practice, which is what the skip line below protects against.
2. **The trio can act on what it hears.** Discovery informs decisions; if the decisions are made elsewhere, the interviews become a ritual that produces well-informed people with no authority. This assumption is the same one the [empowered teams card](cagan-product-teams.md) makes explicit.
3. **Small samples are fit for purpose.** The output is direction, not magnitude. One conversation a week can tell you that a struggle exists and roughly what shape it has, and it cannot tell you how many people have it or what they would pay. Teams that ask the weekly interview for a number get one anyway, which is the source of most of this method's misuse.
4. **The outcome at the root is stable.** The tree hangs from one outcome, so a team whose target changes every month cannot accumulate anything. Branches from the old root do not transfer, and the tree becomes a record of the organization's mind changing rather than of the market.

## When to use it

- When planning research: the research plan template asks for a cadence, and this is the argument for making it weekly rather than phase-gated.
- When a discovery document's evidence section is thin, as the mechanism for filling it: recruit continuously, interview weekly, snapshot each conversation.
- When solution debates loop without resolution, to redraw the argument as a tree and locate exactly where the disagreement lives: outcome, opportunity, solution, or assumption.

**Skip it when:** there are no reachable users this quarter, which is the real situation for a pre-launch product in a closed domain, a market you have no access to, or a build under an embargo. Weekly contact you cannot get is not a habit, it is a missed commitment that erodes the rest of the practice. Say so, name the proxy evidence you will use instead, and put a date on when real contact starts.

## A worked case, ILLUSTRATIVE

Wickham is an invented tool for small architecture practices to track drawing revisions. All details are made up. The outcome at the root of the tree was to reduce the share of projects where the site team builds from a superseded drawing. The team had been about to build a notification system, on the strength of one memorable conversation with their largest customer.

Six weekly interviews later the tree looked different. Five of the six described the same struggle, which was not a notification problem: revisions arrived by email attachment, and the site foreman worked from a printed set in a van, so the failure happened at the moment of printing rather than at the moment of sending. Two people mentioned notifications, one of whom was the original large customer. The tree's shape made that ratio visible, where a chronological list of findings had made the loud interview look like the finding.

The assumption test was small on purpose. The team spent two days sending a stamped, dated cover sheet by hand to four practices and asking a week later which sets the foremen had actually printed. Three of the four had adopted it and one had not, for a reason that turned out to matter more than the whole notification idea: that practice's drawings were issued by a consultant outside the tool, so no cover sheet existed to stamp.

The fourth practice also shows why an assumption test is worth more than an argument about the same question. Nobody in the team had proposed "some drawings are issued outside our tool" as a risk, because it was not a disagreement anyone held; it was a gap in what everyone assumed. Cheap contact with reality finds those, and no amount of internal debate does, because a debate can only explore positions somebody already occupies.

Two days of work redirected roughly six weeks of build. That ratio is the argument for the assumption test layer of the tree, and the fourth practice is the argument for the interviews. A notification feature would have shipped on time, worked correctly, and left the printing failure entirely in place, and the retrospective would have concluded that customers did not adopt the notifications.

## The trap: a stale tree

The tree is a living index of what the team currently believes, and it earns that status only while interviews keep feeding it. The failure mode is the kickoff tree: built in a workshop, admired, exported to a slide, and never touched again. A stale tree is worse than no tree, because it wears the costume of evidence. Solutions keep pointing at opportunities nobody has heard a customer voice in months, and the diagram lends them a legitimacy they no longer own. The test is mechanical: if you cannot say which branch changed after last week's interviews, you do not have a discovery practice, you have a picture of one.

Staleness is usually a recruiting failure rather than a discipline failure, which matters because the two have different fixes. Teams do not stop interviewing because they stopped caring; they stop because each conversation costs a week of chasing, and the cost lands on the person with the fullest calendar. The durable fix is structural: an automated recruiting channel inside the product, a standing slot on the calendar that requires no negotiation, and a default participant list that does not depend on one relationship manager's goodwill. A habit that survives only while one person pushes it is a personal virtue, not a practice.

## Other ways it fails, and the tell for each

- **Interviews with no decision attached.** The team talks to customers weekly and learns things, and nothing in the plan changes for a quarter. The tell: ask what the last interview changed and get a summary rather than a decision. Discovery that informs no decision is a hobby with a good reputation.
- **The trio in name only.** The engineer is invited and never comes, so the transmission benefit disappears and the findings go back to being a report. The tell: interview attendance is one person, and design constraints keep arriving late in build.
- **The friendly sample.** The same three enthusiastic customers absorb most of the touchpoints, because they always say yes. The tell: participant names repeat across the last two months, and no interview has produced an uncomfortable result.
- **Opportunities that are solutions in disguise.** Branches read "needs a dashboard" or "wants bulk upload", which are your ideas quoting a customer. The tell: the opportunity names an interface. A real opportunity survives the deletion of every product in the category.
- **Findings without snapshots.** Conversations happen and leave no artifact, so the evidence exists only in the memory of whoever attended, and the tree is fed from recollection. The tell: no interview record older than a month is retrievable.
- **The tree that only grows.** Branches are added and never pruned or merged, so after two quarters it is a hundred nodes and nobody can compare anything. The tell: the diagram no longer fits on a screen, which is a signal about the team's willingness to decide, not about the market's complexity.
- **Assumption tests scoped like projects.** The test that would settle a question is estimated at three weeks, so it never runs and the team builds instead. The tell: no test in the last month cost less than a sprint. The layer exists to be cheap; if it is not cheap, it is not a test.
- **Synthesis deferred until it is impossible.** Twenty interviews accumulate unread because synthesis is scheduled for when there is time. The tell: a folder of recordings and a tree that stopped growing three weeks before the interviews did.
- **One interview treated as a mandate.** A single vivid conversation, usually with the biggest customer, becomes the plan, and the tree is drawn afterwards to justify it. The tell: a branch supported by one participant carrying more roadmap weight than a branch supported by five.
- **Continuous discovery on a delivery-only team.** Interviews run weekly and the roadmap is set elsewhere. The tell: the team's findings are shared upward as recommendations, and the word recommendation is doing a lot of work.

## How it lies

The instrument's honest limitation is sampling. Weekly interviews select for people who are willing to speak with you weekly, which is a population skewed toward the engaged, the articulate, and the already-loyal. The struggles of the indifferent, the churned, and the people who evaluated you and walked away are systematically underrepresented, and those are precisely the people who define the ceiling of the market. A practice run for a year on a friendly panel will keep discovering refinements to what the product already does.

It also lies through tidiness. A tree is a hierarchy, hierarchies imply that each child belongs to exactly one parent, and real opportunities are entangled: the same struggle feeds two outcomes, and the same solution serves three opportunities badly. The diagram's cleanliness is a drawing convention that readers mistake for a finding, and the usual symptom is a debate about where a node belongs, which is a debate about the drawing rather than about the customer.

The practical answer to both is to record what a branch rests on: how many people, which segments, and when. A tree annotated that way is honest about its own thin spots, and the thin spots are where next week's conversation should go.

The third distortion is that qualitative evidence has no magnitude. Five of six people mentioning something establishes that the struggle is common in that sample and nothing about its frequency in the market, its cost, or anyone's willingness to pay to remove it. Continuous discovery is a direction-finder that must be paired with counting: a survey, an instrumented funnel, or opportunity scoring. Teams that skip the pairing produce confident qualitative claims with numbers attached later by inference, which is the most persuasive kind of wrong.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| You can name the branch that changed after last week's interview | You can name how many interviews were held |
| Recruiting is automated and needs no chasing | Recruiting is one person's weekly favor to the team |
| Opportunities phrased so they survive your product's deletion | Opportunities phrased as features customers asked for |
| Assumption tests that cost days and settle something | Assumption tests scoped as builds, so the build happens instead |
| Two of the three trio roles in most conversations | One person interviewing and reporting back |
| Participants who churned, declined, or chose a competitor appear in the sample | A stable panel of enthusiasts who always say yes |
| The tree pruned and merged as it grows | The tree only ever added to, now a hundred nodes wide |

## Where it sits in the loop

- Stage: DISCOVER, continuously, and it is the only stage in the loop that never stops while the others run.
- Upstream: an outcome to hang the root from, usually an input metric from the [north star input tree](../frameworks/metrics/north-star-input-tree.md), and a job statement from [jobs to be done](jobs-to-be-done.md) to keep opportunities at the right altitude.
- Downstream: the [opportunity solution tree](../templates/discovery/opportunity-solution-tree.md) holds the structure, [discovery synthesis](../templates/discovery/discovery-synthesis.md) turns a run of conversations into claims, and the [discovery document](../templates/discovery/discovery-document.md) cites the evidence with counts.
- On trial at [Gate 1: problem worth solving](../os/STAGE-GATES.md), which asks how many people said this and when, and at [Gate 6: outcomes verified](../os/STAGE-GATES.md), where the assumption that survived the test is checked against the shipped result.
- Sustained by the [feedback program](../templates/operate/feedback-program.md), which owns the recruiting channel the habit depends on.

## What it is not for

- **Sizing or pricing.** No sample of this size supports a magnitude claim. Pair it with a survey or instrumentation, and treat any number produced by weekly interviews as a hypothesis about a number.
- **Usability verification.** Talking about a struggle and watching someone attempt a task are different instruments. A usability test has a script, a task, and an observation protocol.
- **Mandated or maintenance work.** The requirement is settled, and the interview slots are worth more spent on an open question.
- **Replacing analytics.** Interviews explain why a funnel leaks and cannot tell you that it leaks, or by how much. Teams that adopt continuous discovery and let instrumentation rot end up with rich stories about a product they can no longer measure.
- **Markets you cannot reach.** Named in the skip line and worth repeating, because the usual response is to interview whoever is available instead, which produces evidence about the wrong population and carries the authority of real research.

## Variants worth knowing

- **Dual-track agile**, from Desiree Sy and later Marty Cagan and Jeff Patton: discovery and delivery running in parallel with the same team. The ancestor of this practice, and useful vocabulary for explaining to a delivery-focused organization why discovery is not a phase.
- **Research operations with a standing panel**, common in larger companies: a recruited, consented pool with scheduling handled centrally. Solves the recruiting failure that kills most habits, at the cost of a panel that drifts toward professional participants.
- **The assumption test ladder**, a discipline within the method: for any assumption, list the cheapest possible test first, then the next, and only descend when the cheap one is genuinely inconclusive. Most teams start three rungs too low.
- **Opportunity sizing**, Torres's own extension: attach rough magnitude to opportunities before comparing them, which repairs the magnitude gap without pretending the interviews supplied it.
- **Story-based interviewing**, shared with the jobs tradition: ask about the last time it happened rather than about needs in general. The single highest-yield change to a weekly touchpoint, and the reason the [Mom Test guide](../frameworks/discovery/mom-test-interview-guide.md) sits beside this card.

## Used by

- [User research plan](../templates/discovery/user-research-plan.md)
- [Discovery document](../templates/discovery/discovery-document.md)
- [Journey map](../templates/discovery/journey-map.md)
- [Discovery synthesis](../templates/discovery/discovery-synthesis.md)
- [Opportunity solution tree](../templates/discovery/opportunity-solution-tree.md)
- [Feedback program](../templates/operate/feedback-program.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [Opportunity scoring](../frameworks/discovery/opportunity-scoring.md), ranks the outcomes the tree branches into
- [Mom Test interview guide](../frameworks/discovery/mom-test-interview-guide.md), runs the weekly touchpoint without pitching
- [Assumption mapping](../frameworks/discovery/assumption-mapping.md), sorts which assumption under a solution is worth this week's test
- [Empathy map](../frameworks/discovery/empathy-map.md), for turning a single conversation into something the trio can compare
