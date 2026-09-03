---
layer: knowledge
stage: OPERATE
gate: 6
feeds: ["templates/execution/stakeholder-map.md", "templates/execution/decision-log.md", "templates/operate/metrics-review.md"]
method: ""
aliases: ["High Output Management", "high-output-management"]
---
# High Output Management

Based on the ideas in High Output Management by Andrew Grove (1983).

## The essence

Grove's foundational move is to define a manager's output as the output of their own team plus the output of the neighboring teams they influence. Nothing the manager does personally counts except through that lens. Writing the memo, running the meeting, making the decision: these are activities, and activities only matter multiplied by their effect on team output. Grove treats that multiplier as the central quantity of the job, and it sorts all managerial work into three piles: high-multiplier activities (training, clear delegation, timely decisions, information that unblocks many people at once), low-multiplier activities, and negative ones, where a manager's involvement makes the team produce less: meddling, waffling on decisions, or spreading anxiety.

Two practical instruments follow. Delegation is calibrated to task-relevant maturity: how experienced this person is at this specific task, not how senior they are in general. Low maturity gets structure and frequent checkpoints; high maturity gets objectives and monitoring; misreading the maturity in either direction reads as micromanagement or abandonment. And meetings are defended as the medium in which managerial work happens, provided each has a named type and purpose: the one-on-one for the subordinate's agenda, the staff meeting for peer decisions, the operational review for teaching across levels.

The mechanism that makes the leverage idea more than a slogan is timing. Grove's argument is that the same managerial act has wildly different value depending on when in a process it lands, because the cost of correcting a problem rises as work moves downstream. The decision made before a team commits three weeks and the identical decision made after it are not the same decision. That is why he treats information gathering as most of the job and why he insists on indicators that give warning rather than confirmation: the whole point is to move interventions earlier, where they are cheap.

The second load-bearing idea is that management is a production process with a limiting step, and that the limiting step should be scheduled first. In a product organization the limiting step is usually a scarce human judgment, an architect, a compliance reviewer, a single person who understands a legacy system, and everything else should be arranged around that person's availability rather than around the calendar's convenience. Teams that do not identify their limiting step discover it anyway, as a queue.

Grove also pairs every indicator with its opposite, which is the most transferable habit in the book. A count of items produced is paired with a measure of their quality; a measure of speed is paired with a measure of rework. Single indicators invite the obvious distortion, and the pairing removes the incentive without requiring anyone to be virtuous.

## Where it came from

Grove was a chemical engineer running semiconductor manufacturing, and the book is a deliberate translation of production concepts into managerial and knowledge work. The famous opening runs a breakfast counter as a factory in order to introduce process, assembly, and test steps, inventory, the limiting step, and variability, and every later chapter reuses that vocabulary. Its unusual concreteness comes from that lineage, and so do its blind spots.

Manufacturing supplies an unambiguous output, so the frame is strongest where output is countable and weakest where the valuable work is judgment about what to produce at all. That is the reason for this card's skip line: reaching for a production frame in an argument about which product to build imports a metaphor whose central term, output, is exactly the thing under dispute.

## What the frame assumes

1. **Team output is attributable.** The definition requires that you can see what the team produced and connect it to a manager's acts. In operational work this holds; in a research or early-discovery team, output over a quarter may honestly be one decision, and the frame will underrate the manager who caused it.
2. **The manager's leverage runs mostly through their own organization.** Grove includes neighboring teams under influence, and in matrixed product organizations that neighboring share is now most of the job. The arithmetic still works and the reporting line no longer marks its boundary.
3. **A repeatable process exists to instrument.** Indicators, paired indicators, and the limiting step all presume something recurring enough to measure. One-off programs have no steady state to observe.
4. **Information flows through meetings.** Written asynchronous communication existed in 1983 and was slow. A modern equivalent has to include the document, the channel, and the recorded decision, and the underlying claim survives the substitution: the medium is where managerial work actually happens, so an unnamed, purposeless medium is where it is wasted.

## When to use it

- When mapping stakeholders and choosing cadences: the meeting type should match the decision the relationship needs to produce, not the calendar habit.
- When a decision log shows the same decision reopened three times, as the diagnostic: a wobbled decision has negative effect on everyone downstream of it.
- When reviewing metrics for a team or a product operation, to pair every activity indicator with an output indicator so effort is never graded as its own result.

**Skip it when:** the question in front of you is about the product rather than the operation. This frame diagnoses how a team spends its time and says nothing about whether what the team is building is right. Reaching for it in a prioritization argument produces activity advice for a strategy problem.

## A worked case, ILLUSTRATIVE

A group product manager at an invented company oversees three teams, and every figure here is made up. Two of her weeks are worth comparing, because they contained the same number of hours and produced very different amounts.

In the first week she reviewed every ticket in the release candidate, roughly thirty of them, at about six hours total, and attended four reviews she had no decision to make in. In the second she ran a two-hour working session for nine engineers and analysts on how to write an acceptance criterion that a tester could actually verify, then spent two hours writing down which specification decisions the teams could make without her.

Take the crude arithmetic of the session. Nine people, each losing roughly twenty minutes a week to clarification threads that a verifiable criterion would have prevented, is around three hours a week returned to the group against six hours spent preparing and running it, so the payback lands inside a month and continues after that. The ticket review returned a handful of caught defects and stopped returning anything the moment she stopped doing it, which is the signature of an activity with no multiplier: it produces value strictly in proportion to the manager's own hours.

Now the negative case, which is the more useful half. The same quarter contained a specification decision that she reopened three times over five weeks. Two teams had already built against the first version, so the rework cost several days of work across five people, and the standing cost was worse: for five weeks nobody could commit to an interface, so a third team's estimate was fiction. Total time she personally spent on that decision was under three hours, which is exactly why it is easy to miss. Managerial acts scale by the number of people downstream of them, and that arithmetic runs in both directions.

There is a cheap fix for the wobble that the arithmetic points at directly. The decision cost so little of her time and so much of everyone else's because nothing recorded that it had been made; each new objection arrived as if to an open question. A dated line in a decision log, naming what was decided and what was rejected, converts the third reopening from a discussion into a change request with a cost attached.

The uncomfortable observation is that the first week looked far more responsible than the second. A ticket review is visible, effortful, and easy to describe to a manager's own manager; two hours of teaching and two hours of writing down delegation boundaries look like a light week.

## The trap: busyness mistaken for impact

The definition cuts both ways, and the trap is measuring the manager's inputs because they are so much easier to see. A full calendar, fast email replies, presence in every review: all activity, all potentially multiplied by zero. A manager can be visibly exhausted while their team's output falls, because the activities chosen were low-multiplier or negative, and a manager can look idle for a week while a training course they ran quietly raises a whole team's output for a year. Organizations that promote on visible busyness select for exactly the wrong behavior. The corrective question is Grove's own frame turned on yourself: name the team output that changed because of what you did this week. If the honest answer is a list of meetings attended, the week was expensive.

The reason the trap persists is that busyness is legible and leverage is not. A calendar can be shown to a skeptical executive; a decision made early enough that nothing went wrong leaves no evidence at all. Managers respond rationally to what their organization can see, so the fix is partly personal and mostly structural: a written record of decisions with their dates, which turns timely deciding into something visible, and a review that asks what the team can now do that it could not do a quarter ago.

## Other ways it fails, and the tell for each

- **The one-on-one converted into a status meeting.** The manager arrives with an agenda and leaves with an update, so the meeting's actual purpose, surfacing the problems the manager cannot see, never happens. The tell: the manager talks more than the other person, and nothing ever surprises them.
- **Task-relevant maturity read from seniority.** A capable senior hire is left alone on a task they have never done in this context, and it reads as trust until it fails. The tell: a strong performer missing badly on their first attempt at something specific, followed by a conversation about ownership rather than about onboarding.
- **Activity indicators with no output pair.** Velocity, tickets closed, interviews run, all reported alone. The tell: a dashboard where every metric can be improved by working faster and none can be worsened by working badly.
- **The manager as the queue.** Every cross-team question routes through one person, who is now the limiting step they were supposed to be managing. The tell: the team's throughput visibly tracks the manager's calendar.
- **Monitoring that curdles into meddling.** Checkpoints appropriate for low maturity are kept after maturity rises, which the frame counts as negative leverage. The tell: reviews that no longer change anything and are still required.
- **Meetings with no named type.** A single recurring meeting is asked to serve as one-on-one, staff decision forum, and information broadcast, so it does the easiest of the three. The tell: a standing meeting whose purpose nobody can state in one sentence.
- **Delegation without the decision boundary.** Work is handed over and the decisions inside it are not, so the person must return for approval at every fork. The tell: a delegated task generating more manager time than it saved.
- **Information hoarded by accident.** A manager holds context that would unblock several people and shares it only when asked, because sharing it feels like broadcasting. The tell: teams solving the same puzzle in parallel, each unaware that the answer already exists one level up.
- **The reorganization as a leverage move.** Structure is changed because it is the largest visible act available, and the actual limiting step is untouched. The tell: a second reorganization within a year, with the same queue behind it.
- **Leverage used as an excuse.** Detail work is refused on principle by a manager who has stopped knowing how the product works. The tell: the manager cannot describe the last three defects their team fixed, and calls that delegation.

## How it lies

The frame's central quantity cannot be measured, which makes it easy to use retrospectively as a justification for whatever a manager already did. Leverage is estimated, not observed; the arithmetic in the worked case above is a story with numbers attached, and its purpose is to make a comparison thinkable rather than to compute a result. Any use of the model that ends in a claim of high leverage without naming the specific output that changed has produced a compliment rather than an analysis.

The book also assumes a particular organization: co-located, synchronous, hierarchical, and manufacturing-adjacent. Product organizations today are matrixed, partly remote, and often written-first. Three of its instruments transfer intact, which are the leverage question, task-relevant maturity, and paired indicators, and two need translation, which are the meeting taxonomy and the assumption that influence follows the reporting line. Adopting the untranslated version produces a manager with an excellent meeting structure and no reach into the teams that actually gate their work.

The translation is worth doing explicitly rather than by feel. Write down, for your own role, which decisions each recurring forum exists to produce and which are made in writing instead; the exercise usually retires one meeting and reveals one decision that no forum currently owns.

Its last distortion is a matter of scope, and this is the one product managers get wrong most often. The frame is silent about whether the work is worth doing. A team whose output doubles while building the wrong thing has doubled the rate at which it produces waste, and nothing in the model will notice. Pair it with something that judges direction, which in this repository means the strategy and the outcome the team owns.

The cheapest weekly instrument in the whole frame is one written line: what could my team do at the end of this week that it could not do at the start. A month of blank answers is a diagnosis.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| The manager can name the team output that changed because of their week | The manager can name what they attended and produced personally |
| Decisions made once, recorded with a date, and left alone | Decisions revisited whenever a stakeholder asks again |
| Checkpoints set from experience with this specific task | Checkpoints set from job title, then never adjusted |
| Every activity indicator published beside an output or quality pair | A dashboard of throughput metrics with no counterweight |
| Each recurring meeting has one named type and one purpose | One recurring meeting doing the work of three |
| Delegation hands over the decisions inside the task, in writing | Delegation hands over the task and keeps the decisions |
| The limiting step identified and scheduled first | The scarce reviewer booked last, and the queue described as a people problem |

## Where it sits in the loop

- Stage: it spans the loop as an operating discipline rather than a stage, and it is heaviest in OPERATE, where cadence and indicators are set.
- Upstream: the [stakeholder map](../templates/execution/stakeholder-map.md) says which relationships must produce decisions, which is what sets the meeting types and their cadence.
- Downstream: the [decision log](../templates/execution/decision-log.md) makes timely deciding visible, the [metrics review](../templates/operate/metrics-review.md) carries the paired indicators, and the [first 90 days](../templates/planning/first-90-days.md) plan is largely an application of this frame to a new manager's own leverage.
- Related gates: [Gate 5: release readiness green](../os/STAGE-GATES.md) is where an unidentified limiting step usually announces itself, in the form of a review nobody scheduled.
- Companion worksheet: [RACI](../frameworks/execution/raci.md) for accountability, and [stakeholder power and interest](../frameworks/execution/stakeholder-power-interest.md) for where a manager's attention earns most.

## What it is not for

- **Product decisions.** Repeated because it is the most common misuse: this frame optimizes how a team works and says nothing about what it should build.
- **Appraising individuals.** Team output is a joint product, and using it to rank people re-creates every distortion that Grove's separation of measurement from compensation was designed to avoid. See the [OKR card](okrs.md) for the same argument in metric form.
- **Research and long-horizon work.** Where a quarter's honest output is one insight, indicators measure noise and the leverage question has no observable denominator.
- **Organizational design.** The frame assumes a structure and helps you work inside it. Deciding what the structure should be is a different question with different literature.
- **Remote-first communication design.** The meeting taxonomy needs rebuilding for asynchronous work, and the book will not do that for you.

## Variants worth knowing

- **Situational leadership**, from Paul Hersey and Ken Blanchard: the ancestor of task-relevant maturity, with a fuller treatment of how supervision style should change as competence and commitment change independently.
- **Radical Candor**, Kim Scott's framing of caring personally while challenging directly: the feedback half of managerial leverage, which Grove treats briefly and which is where most of the practical difficulty lives.
- **Drucker's knowledge worker**, the earlier tradition Grove is arguing within: output defined by contribution rather than by activity, and the origin of the management-by-objectives lineage that became OKRs.
- **The manager readme**, a modern practice of publishing your own operating preferences and decision boundaries. Crude, and it does more for delegation clarity than most cadence changes.
- **Written-first operating models**, of which Amazon's narrative memo culture is the best-known example: substituting documents for meetings as the medium of managerial work, which is the translation Grove's meeting chapter needs today.

## Used by

- [Stakeholder map](../templates/execution/stakeholder-map.md)
- [Decision log](../templates/execution/decision-log.md)
- [Metrics review](../templates/operate/metrics-review.md)
- [First 90 days](../templates/planning/first-90-days.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [RACI](../frameworks/execution/raci.md), puts one accountable name on each decision
- [Stakeholder power and interest](../frameworks/execution/stakeholder-power-interest.md), for choosing where managerial attention earns the most
- [Five whys and fishbone](../frameworks/execution/five-whys-fishbone.md), for the recurring operational failure that a cadence change will not fix
- [OKRs](okrs.md), the card that carries Grove's other contribution and his rule about keeping measurement away from pay
