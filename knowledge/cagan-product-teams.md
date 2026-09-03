# Empowered Product Teams

Based on the ideas in Inspired (2017) and Empowered (2020) by Marty Cagan.

## The essence

Most software teams are feature teams: they receive a roadmap of outputs decided elsewhere and their job is to ship it. Cagan's argument is that this arrangement wastes the most expensive thing a company buys, the judgment of the people closest to the technology and the customer. An empowered team is handed a problem to solve and an outcome to move, and it is trusted to find the solution itself.

The discipline that makes this more than a slogan is risk-first work. Before a team commits engineering time, it tests four risks in whatever order they are scariest:

1. **Value risk.** Will anyone choose this, pay for it, or switch to it?
2. **Usability risk.** Can the intended user figure out how to get the value?
3. **Feasibility risk.** Can we build it with the time, skills, and technology we have?
4. **Business viability risk.** Does it work for the rest of the business: legal, finance, sales, compliance, brand?

Prototypes, not products, are the instrument for testing the first two. The product manager owns value and viability personally; design and engineering own usability and feasibility. A team that cannot name who owns which risk is not empowered, whatever the org chart says.

The measure of the team changes accordingly: outcomes over output. Shipping the feature is the beginning of the test, not the end of the work.

The mechanism is where the option to change the solution is held. In a feature team the solution is fixed upstream, so every discovery made during build is a deviation to be argued for, and the cost of arguing is high enough that most teams ship the thing they were given while privately knowing better. In an empowered team the solution is the team's variable, so a discovery in week two is a decision rather than a negotiation. That is the entire economic argument: not that engineers have better ideas, but that information arriving late is only useful to whoever holds the option to act on it.

The four risks are a claim about sequencing, and the ordering rule does the work. Test whichever risk would kill the idea most cheaply, first. Most teams instinctively test feasibility first, because it is the risk they know how to investigate and the one that feels technical, and feasibility is very often the least dangerous of the four: it usually resolves to yes, given time. Value and viability are the ones that end projects, and they are the ones a spike does not touch. A team that has spent three weeks proving something can be built has bought information about the risk it was least likely to lose to.

Prototype rather than product is a statement about cost of being wrong. A prototype exists to be discarded, which is what makes it honest: the team that has already built the real thing will find reasons the evidence against it is unrepresentative. That is not weakness of character, it is the sunk cost that the method is designed to avoid incurring.

## Where it came from

Cagan's material comes from operating roles at companies including Hewlett-Packard, Netscape, and eBay, and from twenty years of Silicon Valley Product Group's practice observing how strong product companies differ from ordinary ones. Inspired was first published in 2008 and substantially rewritten in 2017; Empowered followed in 2020, and the difference between them tells you what changed in the industry.

Inspired described how good product teams work. Empowered was written against something specific: the wave of agile transformations that had installed the ceremonies of empowerment on top of feature-factory reporting lines, producing squads that were renamed teams still receiving a list. That is why the second book spends most of its length on leadership behavior rather than team practice, and it is the reason the trap section of this card is about accountability rather than about method.

## What the model assumes

1. **Leadership can supply real context.** Empowerment without a strategy is not autonomy, it is abandonment: teams optimize locally, pick differing problems, and the portfolio incoherence gets blamed on the teams. The prerequisite for handing over the solution is having decided the problem, which means an actual product strategy exists.
2. **The product manager has earned deep knowledge.** Cagan's version of the role assumes genuine expertise in the customer, the data, the business constraints, and the industry. A person without it cannot own value and viability, and the team will correctly route around them.
3. **Engineers engage with the problem, not just the ticket.** Feasibility ownership and the best solution ideas both depend on engineers who know what the customer is trying to do. Where engineering is organized as an order-taking function, the model has no one to hold two of its four risks.
4. **The company can survive its own ideas being killed.** The method's output is frequently a decision not to build something a senior person wanted. An organization in which that is career-limiting will get discovery theater instead, and the theater is more expensive than no discovery at all.

## When to use it

- When deciding how to structure teams and what to hand them: problems and outcomes, or tickets.
- When a discovery document or PRD is being written by someone who has not talked to a customer, as a prompt to ask which of the four risks has actually been tested.
- When objectives are being set, to keep key results pointed at outcomes the team can own rather than features it can merely ship.

**Skip it when:** the team really is delivering a decision made and funded elsewhere that nobody in the room can change. That situation is real in agencies, in regulated remediation programs, and under a signed contract. Naming it honestly serves the team better than running empowered-team rituals over a feature order.

## A worked case, ILLUSTRATIVE

Thornbury is an invented field-service tool for appliance repair companies, and every number is made up. Sales escalated a request for offline mode, attached to two deals, and the engineering lead's first instinct was a spike: could the app work with an intermittent connection and reconcile afterwards. That spike was estimated at three weeks.

Ordering the risks by which would kill the idea most cheaply changed the plan. Value risk went first, at a cost of four days: eleven existing accounts were asked where and how often technicians lost connectivity, using their own dispatch records rather than their impressions. Two accounts had a real and constant problem, both operating in rural territories. Seven had lost connectivity in the last month in one specific place, which was the basement of a single large customer's building. Two had no instances at all.

Then viability, at a cost of one conversation. Offline work meant customer contact details and job notes cached on a technician's phone, which put the feature inside the company's data-retention commitments and required a remote wipe path before it could ship to anyone. That constraint added more to the build than the synchronization logic did, and nobody had priced it.

Feasibility, the risk the team had wanted to test first, turned out to be the least interesting: the synchronization was ordinary work. The decision that emerged was neither yes nor no. Two accounts got a narrow queue-and-retry behavior for the job-completion step only, which is where a lost connection cost a technician a second visit, and the general offline mode was declined in writing with the retention finding attached, which is what made the declination stick when the request returned two quarters later.

The teaching point is the order, not the answer. Testing feasibility first would have consumed three weeks and produced a yes, which would have been read as a green light, and the retention constraint would have arrived in the release-readiness review as a surprise. The risks were not equally scary, and the team's instinct about which one to test was inverted.

## The trap: the label without the accountability

The failure mode is adopting the vocabulary and skipping the trade. Teams get renamed squads, PMs get retitled product owners of empowerment, and the roadmap of committed features arrives exactly as before. Empowerment is a two-sided contract: leadership gives the team the problem and the context, and the team accepts accountability for the outcome, including the uncomfortable part where a shipped feature that moved nothing counts as a miss. A team that has the autonomy but not the accountability is a hobby. A team that has the accountability but not the autonomy is a scapegoat. If you cannot point to the outcome a team owns and the last solution idea it killed with evidence, you have the label.

The diagnostic worth running is a two-question audit, asked of the team rather than of its leadership. What outcome are you accountable for this quarter, and what solution idea have you killed with evidence in the last six months? Two clear answers mean the contract is real. An outcome with no killed idea means the team is deciding nothing, whatever it is called. A killed idea with no outcome means a team enjoying autonomy nobody will hold it to, which is pleasant and produces coherent products only by luck.

## Other ways it fails, and the tell for each

- **Autonomy without strategy.** Teams are handed outcomes with no shared diagnosis, so three teams optimize three metrics that fight. The tell: two teams could both hit their numbers while the company's position worsens, and nobody owns the conflict.
- **The product manager as backlog administrator.** The title is present and the knowledge is not, so value and viability are unowned and the team fills the gap with stakeholder requests. The tell: the PM cannot answer a data question about their own product without asking an analyst.
- **The prototype as a demo.** It is built to persuade rather than to test, shown to internal audiences, and produces enthusiasm instead of evidence. The tell: nobody can say what result would have counted as a failure.
- **Outcome ownership without instrumentation.** A team is told to own activation and cannot measure it weekly. The tell: the outcome number arrives monthly from another team, which makes accountability an accusation rather than a tool.
- **Viability discovered last.** Legal, finance, support, and compliance meet the idea at the release-readiness review. The tell: launches that slip in the final week for reasons nobody technical could have prevented, repeatedly.
- **Empowerment as a shield.** The team refuses a legitimate constraint, a contract commitment or a regulatory rule, on the grounds that it owns the solution. The tell: the phrase "we are empowered" appearing in a conversation about a rule the company does not control.
- **The four risks as a checklist.** All four get a paragraph in the document, none gets a test, and the ordering rule is ignored because a list has no order. The tell: risk sections of uniform length and uniform confidence.
- **Trio without an engineer.** Design and product run discovery, engineering joins at handoff, and feasibility surfaces as a redesign. The tell: the phrase "we did not know that was expensive" in a retrospective.

## How it lies

The model is normative and its evidence base is observational. It describes how the strongest product companies work, drawn from the strongest product companies, which means the causal direction is not established by the material itself: companies that are winning can afford to hand teams problems, and being able to afford it may be a consequence of success as much as a cause. That does not make the advice wrong, and it does mean a struggling organization cannot adopt the described end state by decree. The honest reading is that this is a description of a destination with very little about the route.

Its second distortion is that empowerment is presented as a binary and lived as a gradient. Real teams hold discretion over some decisions and none over others, and the useful question is never whether a team is empowered but which decisions it actually holds. Writing that list down for a specific team is more useful than the label in either direction, and it is what the [RACI worksheet](../frameworks/execution/raci.md) exists to make explicit.

The third is a matter of emphasis. Because the model puts the solution inside the team, it can quietly imply that anything handed down is illegitimate. Plenty of committed work is genuinely fixed by contracts, regulators, and platform commitments, and the professional response is to name it as such rather than to run discovery rituals over a decision nobody in the room can change. The skip line above is that response, and it is not a concession.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| The team can name the outcome it is accountable for this quarter | The team can name the features it committed to this quarter |
| A solution idea was killed with evidence in the last six months | Every idea entering discovery has shipped |
| Risks tested in order of which would kill the idea most cheaply | Risks documented in the order the four appear in the book |
| Viability consulted during discovery, by name | Viability consulted at the release-readiness review |
| Prototypes built to be discarded, with a stated failing condition | Prototypes built to be shown, and then shipped because they exist |
| An engineer in the discovery conversations | An engineer briefed after the design is agreed |
| The decision rights of this specific team written down | The word empowered in the team's charter |

## Where it sits in the loop

- Stage: it is not a stage. This card describes how the loop is staffed and who decides, so it applies at DISCOVER, DEFINE, and DESIGN alike.
- Upstream: a real [product strategy](../templates/planning/product-strategy.md) and [vision](../templates/planning/vision.md), without which the handover of solution authority becomes abandonment.
- Downstream: the [opportunity assessment](../templates/discovery/opportunity-assessment.md) and [discovery document](../templates/discovery/discovery-document.md) record which risk was tested and how, the [PRD](../templates/definition/prd.md) records what the tests settled, and [OKRs](../templates/planning/okrs.md) carry the outcome the team accepts.
- On trial at [Gate 1: problem worth solving](../os/STAGE-GATES.md), which asks which of the four risks has actually been tested rather than discussed.
- Supported by the [stakeholder map](../templates/execution/stakeholder-map.md) and [RACI](../frameworks/execution/raci.md), which turn the word empowered into a list of decisions with names on them.

## What it is not for

- **Contract and agency work.** Where scope is the deliverable and someone else owns the outcome, the model has nothing to give and its rituals cost real time.
- **Regulated remediation.** A supervisory finding with a deadline is not a problem space. Run it as a program, and reserve empowerment for the work where the solution is genuinely open.
- **Deciding what the company should do.** The model allocates authority; it does not generate strategy. A leadership team that adopts it hoping to be relieved of choosing has misread it.
- **Very small startups.** With three people and a founder who is the product manager, the distinction between feature team and empowered team has no referent. The four risks still apply.
- **Platform teams with committed interfaces.** When other teams depend on a published contract, discretion over the solution is genuinely limited, and the honest framing is a service with consumers rather than a problem to solve.

## Variants worth knowing

- **The product operating model**, Cagan's later synthesis in Transformed (2024): the same principles restated as an organizational change program, which is the route the earlier books left out.
- **The product trio**, shared with Teresa Torres's practice: product, design, and engineering deciding together. Torres supplies the weekly mechanics that make the trio a habit rather than a diagram; see [continuous discovery](torres-continuous-discovery.md).
- **The scrum product owner**, worth understanding precisely because it is not this. The role as commonly implemented owns a backlog inside a delivery process, which is the arrangement Cagan's material is arguing against, and conflating the two titles is the most common way an organization believes it has adopted the model.
- **The single-threaded leader**, from Amazon's practice: one senior owner with a dedicated team and no competing responsibility. A different answer to the same problem, trading the trio's shared judgment for unambiguous accountability.
- **Named-squad models**, of which the widely copied Spotify description is the best known, and which its own authors have since disowned as a snapshot rather than a template. Useful as a cautionary example of adopting structure without the decision rights underneath it.

## Used by

- [Discovery document](../templates/discovery/discovery-document.md)
- [PRD](../templates/definition/prd.md)
- [One-pager](../templates/definition/one-pager.md)
- [OKRs](../templates/planning/okrs.md)
- [Vision](../templates/planning/vision.md)
- [Opportunity assessment](../templates/discovery/opportunity-assessment.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [Assumption mapping](../frameworks/discovery/assumption-mapping.md), sorts the four risks into what to test first
- [RACI](../frameworks/execution/raci.md), for writing down which decisions this team actually holds
- [Decision doors](../frameworks/prioritization/decision-doors.md), the reversibility test that says how much evidence a decision earns
- [OKRs](okrs.md), the card on the outcome half of the two-sided contract
