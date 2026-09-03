---
layer: knowledge
stage: DISCOVER
gate: 1
feeds: ["templates/discovery/discovery-document.md", "templates/definition/brd.md", "templates/definition/prd.md"]
method: ""
aliases: ["Amazon PR/FAQ", "amazon-pr-faq"]
---
# Amazon PR/FAQ

Based on Amazon's working backwards practice as described by Colin Bryar and Bill Carr in Working Backwards (2021).

## The essence

Before Amazon builds a product, someone writes the press release announcing it, dated for launch day, one page, in plain customer language: the customer, the problem, how the product solves it, why the customer should care. Attached is the FAQ, several pages of the hardest questions anyone inside or outside the company could ask, answered honestly: what it costs, what it depends on, what could kill it, what the skeptical customer says, what the skeptical CFO says.

The mechanism is deliberate inversion. Most products are built forward, from a capability the company has toward a customer it hopes exists. Working backwards starts at the moment of customer value and refuses to proceed until that moment is vivid and worth the trip. If the press release is boring, the product will be boring; it is vastly cheaper to learn that in a document review than in a launch. Drafts go through many revisions, and killing the idea at PR/FAQ stage is a success of the process, not a failure of the author.

The FAQ is where the intellectual honesty lives. The press release sells; the FAQ confesses. A PR/FAQ with a glowing PR and a thin FAQ has done half its job, the cheap half.

A second mechanism is doing quiet work: the choice of prose over slides. A bullet can hide a missing causal link, because the reader supplies the connective tissue themselves and assumes the author had it. A sentence cannot. Writing "customers will switch because their current process fails at month-end" forces the author to notice they do not know that, whereas a slide reading "pain: month-end" survives review untouched. The narrative form is a defect detector for arguments, which is why the format resists being reformatted into something more scannable.

The third is the constraint of length. One page for the press release means the value claim must survive compression to a few sentences a customer would recognize, and compression is where vagueness dies. Most initiatives that cannot produce a good press release fail at exactly this step: the value is real but distributed across four different beneficiaries, none of whom would read the announcement and feel anything. That is a genuine finding about the initiative, arriving in week one rather than after launch.

## Where it came from

The practice grew out of a specific decision at Amazon in the mid-2000s to ban presentation slides from senior meetings in favor of narrative memos, and to start product proposals from the customer announcement rather than from the company's capabilities. Bryar and Carr, who worked there through that period, describe both the format and the ritual around it, and the ritual is the part usually left behind: the meeting opens with the room reading the document in silence, so discussion begins from a common understanding rather than from a presenter's framing.

Two features of the company explain why the tool worked there. Amazon ran many bets and was willing to kill them, which made a document that ends an initiative a normal outcome rather than a career event. And it had an unusual appetite for long-horizon, reversible experiments, so the discipline of stating what would have to be true was answering a question the leadership actually wanted answered. Both conditions are worth checking before importing the format, because they determine whether the FAQ can afford to be honest.

## What the document assumes

1. **The decision is still open.** Everything here is designed to test an idea. Applied after commitment, the same format is an unusually persuasive internal advertisement, which is the trap below.
2. **The document will actually be read.** Prose only outperforms slides if people read the prose. Without the silent reading ritual or an equivalent, reviewers skim, comment on style, and the format's advantage evaporates while its cost remains.
3. **There is a nameable customer and an expressible benefit.** Some real work has neither, and forcing a press release out of it produces fiction that a team then has to live with.
4. **Killing is survivable.** An organization where the author of a killed document loses standing will produce documents that cannot be killed. The failure will look like unusually good writing.

## When to use it

- At discovery stage, before a line of the PRD exists, as the sharpest test of whether the problem and its resolution can be stated in customer language at all.
- When writing the business case: the FAQ's hard questions are the same questions the BRD's sponsor will ask, and it is better to meet them on paper first.
- When a large initiative feels vaguely justified, as a kill test: if six revisions cannot produce an exciting press release, the initiative is the problem.

**Skip it when:** nothing customer-facing changes. A platform migration, an internal tool, or a debt paydown has no press release that is not fiction, and writing one anyway teaches the team to produce marketing copy for engineering work. A system design document and a decision record do that job.

## A worked case, ILLUSTRATIVE

Kestrel is an invented parcel-locker service for apartment buildings, and every number is made up. The press release wrote itself: your deliveries are waiting in a locker in your own lobby, no missed slots, no notes from couriers, collect them when you get home. It was vivid, short, and everyone liked it.

The FAQ contained one question that changed the outcome. What happens when the lockers are full? Answering it honestly required arithmetic nobody had done. A representative building has sixty apartments; ordinary weeks average about one and a half parcels per apartment; the locker bank the team had specified held forty-eight compartments with same-day collection by most residents. In the four weeks around the winter peak, the average roughly doubles, and collection slows because people travel. The lockers overflow for the several weeks of the year when parcel delivery matters most to residents and to couriers, which is precisely when the promise in the press release is being tested by everyone.

That answer could not be softened without becoming false, and it forced a decision rather than an edit. Three options were written into the FAQ: larger banks, which broke the lobby footprint and the unit economics; overflow into a concierge process, which meant the product was actually a staff workflow tool with lockers attached; or a narrower promise about small parcels only, which was honest and much less exciting as a press release.

The company chose the second option and shipped something real. The point of the case is what the document cost and what it saved. Writing it took two people about a week, and the arithmetic that changed the product was one paragraph inside it. The same discovery in a pilot would have arrived in December, in the buildings the company most wanted as references, and the press release would already have been published.

Notice too that the killing question was not exotic. It was the first thing a resident would ask, and the reason nobody had asked it internally is that internal conversations had been about lockers, suppliers, and installation, all of which are questions about the build. Working backwards is mostly a device for spending an hour inside the customer's sequence of questions rather than the company's.

Note also which section carried the value. The press release was excellent and told nobody anything they did not already believe. Everything decision-relevant was in the FAQ, in a question a critic would have asked in the first minute, which is why the FAQ is the half worth rehearsing before review.

## The trap: selling a decision already made

The instrument assumes the decision is still open. Write the PR/FAQ after the initiative has a budget line, an assigned team, and an executive sponsor's name on it, and the document inverts into marketing collateral for an internal audience: the press release gets polished, the FAQ's hard questions get softened into setups for reassuring answers, and review becomes a table read. The tell is the FAQ. A genuine one contains at least one question the authors cannot yet answer well and says so; a laundering one answers everything smoothly. If no PR/FAQ in your organization has ever killed the idea it described, the tool is being used as a ribbon, and the working backwards is theater performed after working forwards finished.

A second tell is the authorship. When the document is written by the person whose promotion depends on the initiative proceeding, and reviewed by people who have already told their own managers it is happening, the FAQ's honesty has no institutional support. The cheap counter is to assign the hardest three questions to someone who does not benefit from the answer, whether that is a red-team reviewer, a skeptical peer, or the finance partner who will price it, and to print their answers unedited.

## Other ways it fails, and the tell for each

- **A press release written for an internal audience.** It contains capability language, project names, and integration lists, because the real audience is a funding committee. The tell: a customer would not understand the headline, and no customer benefit appears before the third sentence.
- **The comfortable FAQ.** Ten questions, each with a satisfying answer, none of which the author had to research. The tell: no answer in the document contains the words "we do not yet know" or an owner and a date for finding out.
- **The invented customer quote.** A fictional testimonial is written to make the release feel real, then gets cited in later documents as a customer view. The tell: a quotation with no interview behind it and no label saying so.
- **The PR/FAQ used as a specification.** The team skips the PRD because the document reads complete, and engineering builds from a narrative with no acceptance criteria. The tell: an open question in the FAQ appearing as a defect in the build.
- **Format without ritual.** The document is circulated in advance, nobody reads it, and the meeting becomes a presentation of the document, which is the slide deck with extra steps. The tell: the first ten minutes of review are the author summarizing.
- **Availability left vague.** No date, no geography, no segment, so the document commits to nothing and cannot be wrong. The tell: the word "eventually", or a launch scope that widens quietly between drafts.
- **One revision.** The value comes from iterating a document toward truth, and a single draft approved in the first review has skipped the mechanism entirely. The tell: version one is the version that shipped.
- **The FAQ that answers only external questions.** Pricing, availability, and how it works are covered; what it costs us, what it depends on, and what would make us stop are not. The tell: no question in the document could embarrass the team if a competitor read it.
- **Written for work with no customer.** A migration or a debt paydown gets a press release because the process requires one, and the team learns to write marketing copy about infrastructure. The tell: the release announces an internal capability as though users had asked for it.

## How it lies

The format is rhetorical, and rhetoric is a skill unevenly distributed. A strong writer can produce a compelling PR/FAQ for a mediocre idea, and a weak writer can fail to sell a good one, so the instrument systematically favors initiatives owned by good writers. There is no citation apparatus in the format, which compounds the problem: a sentence asserting that customers abandon the current process reads exactly like a sentence reporting that eleven of them said so. In this repository the correction is external, which is why the [PR/FAQ template](../templates/definition/prfaq.md) requires evidence references and the discovery document carries the counts.

It also lies by optimizing for a moment. A press release describes launch day, so the document's attention naturally lands on first impressions and away from the second year: the support burden, the migration of existing customers, the operational routine, the slow decay of an unowned integration. Many initiatives are excellent on launch day and expensive forever after, and this format is structurally blind to that shape unless the FAQ is deliberately asked to price it.

The practical counter is one extra FAQ question, asked every time: what does this cost us in the second year, when the launch team has moved on and nobody owns it. It is the question most likely to change a decision and the one least likely to be volunteered.

The last distortion is selection. Working backwards from an announcement biases a portfolio toward things that can be announced. Reliability work, latency, developer productivity, and the removal of accumulated friction have no press release and are frequently the highest-value work available. An organization that funds only what produces a good PR/FAQ will drift toward the announceable, and that drift is invisible because every funded item passed a rigorous review.

One rehearsal is worth more than three revisions of the press release: read the FAQ aloud to someone who wants the initiative stopped, and keep the questions they ask.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| A press release a customer could read and recognize as their own problem | A press release naming systems, teams, and integrations |
| An FAQ containing at least one unresolved question, with an owner and a date | An FAQ where every answer is reassuring |
| The hardest questions answered by someone who does not benefit from the answer | The hardest questions answered by the author, gently |
| Several revisions, with the change in claim visible between them | One draft, approved at the first review |
| Review opens with the room reading in silence | Review opens with the author presenting |
| A dated, scoped availability statement | Availability described as eventually, for everyone |
| Some documents in the organization's history killed the idea they described | Every document ever written has proceeded to build |

## Where it sits in the loop

- Stage: DISCOVER into DEFINE. It is a gate document, written before the PRD and often instead of one when the answer turns out to be no.
- Upstream: evidence from [discovery](../templates/discovery/discovery-document.md) and a stated job or problem, so the press release's claim rests on something countable.
- Downstream: the [PR/FAQ template](../templates/definition/prfaq.md) holds the artifact, the [business case](../templates/planning/business-case.md) takes the FAQ's cost and dependency answers, and the [PRD](../templates/definition/prd.md) turns the surviving promise into acceptance criteria.
- On trial at [Gate 1: problem worth solving](../os/STAGE-GATES.md), which is the gate this document was built to inform, and where a comfortable FAQ should fail rather than pass.
- Reviewed adversarially by the [red-team agent](../agents/red-team-agent.md), whose job is the three questions the author would rather not answer.

## What it is not for

- **Work with no customer-facing change.** Named in the skip line, and the most common misuse. Use a decision record and a system design document.
- **Technical design.** The document says what will be true for the customer, not how. An architecture decision belongs in an [ADR](../templates/architecture/adr.md).
- **Sizing and financial approval.** The FAQ answers cost questions qualitatively. The numbers belong in the business case, where they can be challenged as numbers.
- **Incremental improvement.** A change too small to announce does not need a press release to justify it, and writing one trains the team to inflate.
- **Regulated launches where the binding constraint is a rule.** A vivid narrative does not survive a precondition nobody can waive; run the gap check first and let the document describe what is actually permitted.

## Variants worth knowing

- **The six-page narrative memo**, Amazon's general-purpose document for a decision that is not a product launch. Same prose discipline and same silent reading, without pretending there is an announcement.
- **The one-pager**, this repository's lighter form, for an idea that has not earned a full document yet. It carries the problem and the proposed bet without the launch fiction.
- **The future press release in a design sprint**, from the Knapp tradition: the same inversion compressed into an hour as a framing exercise rather than a decision document. Cheap, and it produces alignment rather than evidence.
- **FAQ-only**, an underused variant for internal or platform decisions where the press release would be fiction but the hard questions are exactly what is missing. Keep the confessional half, drop the sales half.
- **The premortem**, from Gary Klein, as a complement rather than a variant: assume the launch failed and write down why. It reliably surfaces the questions a friendly FAQ omits, which is why the two are usually run together.

## Used by

- [Discovery document](../templates/discovery/discovery-document.md)
- [BRD](../templates/definition/brd.md)
- [PRD](../templates/definition/prd.md)
- [PR/FAQ](../templates/definition/prfaq.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [Decision doors](../frameworks/prioritization/decision-doors.md), the reversibility test that decides how much document the decision earns
- [Premortem worksheet](../frameworks/execution/premortem-worksheet.md), for the failure questions a friendly FAQ leaves out
- [Reg gap check](../skills/reg-gap-check/SKILL.md), before writing a launch narrative in a regulated domain
- [Crossing the Chasm](crossing-the-chasm.md), the card on who the announcement is actually addressed to
