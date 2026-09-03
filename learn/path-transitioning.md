# Path: Transitioning

Audience: you ship, design, analyze, deliver, or support software for a living, and you are moving into a PM seat. This path does not teach you the domain you already know; it teaches you the artifacts and the evidence discipline, and it spends your existing craft where it transfers.
Fictional product: **Restow**, a self-service returns portal for an online furniture retailer. Invented end to end; label invented evidence "invented:" throughout.
Prerequisite: none of Foundations is required, but skim [path-foundations.md](path-foundations.md) step 1 if the six-stage loop is new to you.

Before step 1: create `learn/products/restow/`, copy the ledger below into `PROGRESS.md` there, per [products/README.md](products/README.md).

## Ledger (copy into learn/products/restow/PROGRESS.md)

- [ ] Step 1: what the seat actually owns
- [ ] Step 2: evidence, the unit of the job
- [ ] Step 3: research you can defend
- [ ] Step 4: the PRD, written backwards
- [ ] Step 5: acceptance criteria and edges, your unfair advantage
- [ ] Step 6: stakeholders and decisions, the political ledger
- [ ] Step 7: outcomes over output
- [ ] Capstone: Gate 2, scored

## The standing brief

One invented situation carries all seven steps, so each artifact can cite the last instead of restarting. Copy this block into your PROGRESS.md.

Invented: the retailer ships about 18,000 orders a month and roughly 8 percent come back, so around 1,400 returns a month. Today a customer emails support, waits, and gets a pickup slot by reply; median time from request to scheduled pickup is six days, and eleven agents handle 2,900 return emails a month. Of the returns customers start by email, 31 percent are never completed. The warehouse rejects one arrival in twelve for missing paperwork and re-books the collection at the retailer's cost, roughly 55 euros per truck visit. Finance refuses to discuss instant refunds. Legal owns a 30-day statutory return window that cannot move.

Every number above is invented and stays labeled. The discipline is the point, because the difference between a PM and a very senior builder is mostly what they are willing to put their name next to.

## Step 1: what the seat actually owns

**Read:** [Empowered product teams](../knowledge/cagan-product-teams.md), then [High Output Management](../knowledge/high-output-management.md). Between them: the PM owns problems and risk, and output is now the team's output, not yours. Melissa Perri's Escaping the Build Trap (see [the library](library.md)) is the long version of why this transition fails when it stays output-shaped.
**Run:** [RACI](../frameworks/execution/raci.md) over the Restow release, then read [triad decision rights](../knowledge/roles/triad-decision-rights.md) and find the rows where you handed yourself a decision the triad says you share.
**Study:** [WHICH-DOCUMENT](../os/WHICH-DOCUMENT.md), the weight tree. Your old role had one artifact form; this seat has a dozen, and choosing the weight is the first real decision.
**Do:** in PROGRESS.md, write a two-column mapping: five artifacts from your current role on the left, the nearest PM artifact from this repository on the right, with one line each on what changes in the translation.
**Done when:** at least one row honestly says "nothing maps; this is new", because pretending everything transfers is the first trap of the transition.

**Why this comes first.** The failure mode of a new PM is rarely bad judgment. It is correct judgment aimed at the wrong object: you keep optimizing whatever your last role was measured on. Writing down what the seat owns, before you write anything else, gives you a document to check an instinct against on the day one fires.

**What good looks like.** Weak row: "tech design doc maps to PRD", true and useless. Strong row: "tech design doc maps to the PRD, but the audience inverts, because a design doc persuades people who can read the code while a PRD persuades a sponsor who will never open it, so the burden shifts from correctness to consequence." Weak from support: "macros map to release notes." Strong: "macros map to [customer comms](../templates/delivery/customer-comms.md), and the new question is who signs them, because a macro was mine and a comms plan is legal's."

**Pass criteria.** A 2: five rows, at least one honest "nothing maps", and every translation line naming what changes rather than what stays, such as the audience, the burden of proof, or who signs. A 1: five plausible rows whose translation lines describe the artifact instead of the shift. A 0: a mapping that would let you keep working exactly as you worked last month.

**The trap, and its tell.** Everything maps. The tell is that your five rows read as five reassurances. The honest missing row is usually identical across backgrounds: no previous seat ever required you to write down a reason to say no-go about your own project and then defend it to the person who wanted it.

**Time.** Sixty minutes. If it takes twenty, you wrote the reassuring version.

## Step 2: evidence, the unit of the job

**Read:** the Mom Test entry in the [knowledge index](../knowledge/README.md): past behavior over opinions, always. Then the evidence ladder in [the bank format](../skills/conductor/questions/README.md).
**Run:** [assumption mapping](../frameworks/discovery/assumption-mapping.md) over the standing brief, so you can see which of those invented numbers are evidence and which are beliefs wearing decimal points.
**Study:** [the evidence note](../templates/discovery/evidence-note.md).
**Do:** write three evidence notes for Restow: one from an invented support-ticket export, one from an invented customer interview, one from an invented analytics query. Each gets a claim, a load-bearing detail, a source ID, a date, and a confidence label; place each on the evidence ladder.
**Done when:** the three notes sit on three different ladder rungs and you can say, per note, what the Conductor's challenge grammar would attack first.

**Why now.** Evidence is the unit of account in this seat, the way a passing test or a shipped screen was in your last one. Do it before the research plan, because a plan written by someone who has not yet felt the difference between rung two and rung four will collect the wrong material politely and on schedule.

**Pass criteria.** A 2: the ticket note reads "invented: 412 of 2,900 return emails in March asked when the truck is coming, export RET-EXP-2026-03, pulled 2026-04-02, artifact, single-source", and its load-bearing detail is a count with a period and a place. A 1: the same note without the export ID, or with a claim the detail does not actually support. A 0: "customers are frustrated by slow pickups", a conclusion with no rung at all.

**The trap, and its tell.** The analytics note that is an opinion with a chart attached. The tell: your claim contains a word the query cannot return. A query returns counts of events, so it can say 31 percent of started returns logged no label event within seven days; it cannot say customers gave up, because giving up is not a column. Write what the data says, then what you infer, in two sentences, labeled differently.

**Time.** Seventy-five minutes, twenty-five per note. The third gets fast, which is the skill arriving.

## Step 3: research you can defend

**Read:** [Continuous discovery](../knowledge/torres-continuous-discovery.md).
**Run:** [the Mom Test interview guide](../frameworks/discovery/mom-test-interview-guide.md) and draft your questions there before they enter the plan; the guide catches the two or three that are pitches with question marks.
**Study:** [the user research plan](../templates/discovery/user-research-plan.md).
**Do:** fill the plan for one Restow research question: why do customers abandon a started return? Write the screener, five interview questions that ask about past behavior only, and the synthesis themes you expect to be wrong about.
**Done when:** none of your five questions can be answered with a compliment, and the plan names the decision the research will inform.

**Why now.** The plan is where old reflexes show most, because engineers and designers both tend to research solutions and call it discovery. The named decision at the top is the control: if you cannot say which decision changes depending on the answer, the research is a hobby with a calendar invite.

**What good looks like.** Weak question: "would a self-service portal have helped?" It invites agreement and costs the interviewee nothing. Strong: "walk me through the last item you sent back, from the moment you decided to the moment it left your hallway, and name every place you had to wait for somebody." Also strong, and uncomfortable: "what did you do with the piece you decided not to return?" That one finds the real workaround, because a sofa nobody returned went into a spare room, onto a resale site, or into a skip, and each of those is a different product.

**Pass criteria.** A 2: five past-behavior questions, a screener criterion drawn from the problem rather than from your product, and one named decision the findings will change. A 1: good questions with no decision named, which produces a report nobody acts on. A 0: any question answerable with a compliment.

**The trap, and its tell.** The screener that selects for people who agree with you. The tell: every criterion is a behavior your product would cause rather than one the problem causes. "Has used a returns portal before" recruits your fan club; "has started a return and not completed it in the last quarter" recruits the 31 percent you need.

**Time.** Ninety minutes. The five questions take longer than the plan around them, correctly.

## Step 4: the PRD, written backwards

**Read:** [Amazon PR/FAQ](../knowledge/amazon-pr-faq.md). Working backwards is the antidote to the builder's instinct of starting from the system you already see in your head.
**Run:** [impact mapping](../frameworks/prioritization/impact-mapping.md) from the goal through the actors to the behavior changes, so every scope item has a behavior above it, then compare your shape against the filled [expense copilot PRD](../examples/expense-copilot-prd.md).
**Study:** [the PRD](../templates/definition/prd.md), delete-unused-sections rule first.
**Do:** write the internal FAQ's three hardest questions for Restow in PROGRESS.md, answer them, and then fill the PRD. Scope one release: label printing and pickup scheduling in, instant refunds out, with the why written down.
**Done when:** the PRD's out-of-scope section is as convincing as its scope, every success metric has an invented baseline and target, and nothing in it describes implementation your old self would have reached for.

**Why now.** You have evidence and a research plan, which is exactly enough to write a document that commits other people's time. The hard-FAQ step comes first because the questions you least want to answer are the ones a sponsor asks in minute four, and answering them on paper while nobody is watching is the cheapest rehearsal available.

**Worked micro-example.** Three hard questions worth stealing: what happens to the customer with no printer, given the brief says nothing about it; why is a portal cheaper than three more agents, as a number with a period; and what does finance lose if instant refunds stay out for a year. The third tests whether your out-of-scope line is a decision or an avoidance. A convincing answer reads "invented: instant refunds shift roughly 210,000 euros of float per quarter, finance has not agreed to carry it, so this release ships refund-on-scan and revisits after two quarters of scan-accuracy data".

**Pass criteria.** A 2: every scope item traces up to a behavior change on the impact map, every success metric carries an invented baseline and target, and the out-of-scope section names what each exclusion costs and who agreed to pay it. A 1: complete scope with an out-of-scope list carrying no reasons. A 0: a functional requirement that specifies a mechanism.

**The trap, and its tell.** Architecture leaking into requirements. The tell for a former engineer is the word queue or webhook inside a functional requirement; for a former designer, a named component inside an acceptance criterion; for a former analyst, a metric definition that presumes one event schema. State the behavior the system owes and let [solution architecture](../templates/architecture/solution-architecture.md) own the how.

**Time.** Two to three hours, the longest step here. Split it: FAQ one evening, PRD the next.

## Step 5: acceptance criteria and edges, your unfair advantage

**Read:** the premortem entry in the [knowledge index](../knowledge/README.md); you are about to run one in miniature against your own spec.
**Run:** [the premortem worksheet](../frameworks/execution/premortem-worksheet.md) against the release you just scoped, then convert only the failures a criterion could have caught; the rest belong in the risk register at step 6's altitude.
**Study:** [acceptance criteria](../templates/definition/acceptance-criteria.md) and [edge cases](../templates/delivery/edge-cases.md).
**Do:** write given-when-then criteria for the return-label flow, then the edge-case table: the damaged item, the return window expiring mid-flow, the order paid with a gift card, the customer with no printer. Your technical instincts are an advantage here; spend them on behavior, not architecture.
**Done when:** every edge case has an expected behavior rather than "handle gracefully", and at least three criteria are negative cases, because the flow that only works when everything works does not work.

**Why now.** This is the step your old craft wins outright, and it is worth knowing why: you already think in states and failures, and most PMs do not. The risk is spending that talent one layer too low, writing a test plan when the team needed a decision about what the product owes a customer whose window expires while a pickup is pending.

**What good looks like.** Weak: "given an expired return window, the request is handled gracefully." Nobody can fail that. Strong: "given a return whose 30-day window expires after a pickup is booked but before collection, when the truck arrives, then the collection proceeds and the refund is honoured at the original price, because the retailer chose the slot and not the customer." That criterion decides something, names who eats the cost, and can be failed by a build.

**Pass criteria.** A 2: at least three negative criteria, every edge case carrying an expected behavior that names who absorbs the cost, and every policy question routed out with an owner rather than answered by you. A 1: complete criteria that all describe the happy path in different words. A 0: any expected-behavior cell that a build could not fail.

**The trap, and its tell.** Edge cases that are unwritten policy. The tell: the expected-behavior cell contains a rule you invented on the spot, such as refunding a damaged item at half value. Half of what, decided by whom? Route it out as a question for finance or legal and mark the row open with an owner. A spec that quietly legislates gets overruled after launch, in public.

**Time.** Two hours. The four named edge cases take thirty minutes; the fifth one you find yourself takes the rest, and is the reason for the step.

## Step 6: stakeholders and decisions, the political ledger

**Read:** [High Output Management](../knowledge/high-output-management.md) again, the leverage lens this time: meetings and decisions are your new codebase.
**Run:** [power and interest mapping](../frameworks/execution/stakeholder-power-interest.md) on the six stakeholders before you fill the template, because grid position rather than job title decides how often each one hears from you.
**Study:** [the stakeholder map](../templates/execution/stakeholder-map.md) and [the decision log](../templates/execution/decision-log.md).
**Do:** map Restow's six invented stakeholders (operations lead, warehouse manager, finance controller, support lead, engineering lead, legal counsel) with interest, influence, and concerns. Then write two decision-log entries: one decision that went your way, one that did not and that you are recording honestly anyway.
**Done when:** the map contains at least one stakeholder whose interests genuinely conflict with the product's, and the lost decision reads as a record, not a grievance.

**Why now.** You now hold a PRD and a set of criteria, which means you hold something other people can lose because of. The map is not a courtesy exercise; it tells you which of the six can stop the release and therefore has to be persuaded before the meeting rather than during it.

**What good looks like.** The conflict most learners miss is the warehouse manager, whose invented bonus rides on dock throughput while a self-service portal raises arrival volume and leaves the paperwork-rejection rate untouched. His interests are not aligned with yours, and no amount of shared vision fixes that; a scan-on-arrival requirement in the release does, or an explicit deferral logged with his name on it. Then contrast the two log entries: "finance declined instant refunds, deciding factor was quarter-end float exposure, revisit trigger is two quarters of scan accuracy above the agreed bar, decided by the finance controller on an invented date" is a record. "Finance blocked us" is a grievance, and it will read as one to whoever finds the log after you have moved on.

**Pass criteria.** A 2: six stakeholders with what each is measured on, one genuine conflict, and two log entries each carrying the decision, the deciding factor, the decider, and the date. A 1: a complete map whose concerns column restates job titles. A 0: a lost-decision entry that assigns blame instead of recording a reason.

**The trap, and its tell.** The map where everyone is supportive. The tell: every concerns cell paraphrases "wants it to go well". Ask instead what each person is measured on and whether your release moves that number the wrong way. If nobody's number moves the wrong way, the release is probably too small to matter.

**Time.** Ninety minutes, and the two log entries take longer than the map of six.

## Step 7: outcomes over output

**Read:** [OKRs](../knowledge/okrs.md). The trap, key results that are tasks, is precisely the transition trap: a builder's KR says "ship the portal", a PM's says what changes because it shipped.
**Run:** [the north star input tree](../frameworks/metrics/north-star-input-tree.md) and take your key results from the input layer, because a KR invented straight out of an objective is usually a task in a costume.
**Study:** [the OKR template](../templates/planning/okrs.md).
**Do:** write one objective and three key results for Restow's first quarter live. Every KR gets an invented baseline, a target, and a source system. Then rewrite your own first instinct: take the most task-shaped KR you drafted and turn it into an outcome.
**Done when:** no key result contains a verb of building, and each one would still be scoreable if the team shipped nothing.

**Why last.** A key result is only honest once scope is fixed: written before step 4 it is a wish, written after it is a claim you can be held to. Keep both versions of the rewrite in PROGRESS.md, side by side, because the gap between them is the transition itself and it is worth being able to see later.

**Worked micro-example.** Task-shaped: "launch the returns portal to all customers by end of quarter." Outcome-shaped: "invented: median request-to-scheduled-pickup falls from six days to under two, measured in the returns database, on returns created in the quarter." Notice what the rewrite removes: the same work, none of the credit for merely doing it. The second version is scoreable if the team ships nothing, and it scores badly, which is the property that makes it a key result.

**Pass criteria.** A 2: three key results with baseline, target, and source system, none scoreable by shipping alone, and both versions of the rewrite kept side by side. A 1: outcome-shaped results with no baselines, which makes every target a wish. A 0: any key result containing a verb of building.

**The trap, and its tell.** The metric that is adoption in disguise. The tell: your KR moves when people use the thing, not when their situation improves. Portal sessions is a task with a number attached. Paperwork rejection at the dock, falling from one arrival in twelve to one in thirty, is an outcome, and it happens to be the number that buys you the warehouse manager from step 6.

**Time.** Seventy-five minutes including the rewrite. Do the rewrite the same evening, while the first instinct still feels defensible.

## Capstone: Gate 2, scored

Run the tutor ([skills/tutor/SKILL.md](skills/tutor/SKILL.md)) over your Restow definition set. The tutor drills from the DEFINE bank ([the questions](../skills/conductor/questions/define.md)), critiques the PRD against its exit gate line by line, pushes once per weak answer, and scores.

**Done when:** every Gate 2 line scores 2, including the weight question: be ready to defend why Restow got a PRD and not a one-pager, or concede the point and cut it down, which is also a pass. Pencil users: self-grade against the bank's Accept-when lines.

**Where each gate line comes from.** Gate 2 in [STAGE-GATES.md](../os/STAGE-GATES.md) traces objectives back to the Gate 1 problem, demands criteria that can fail, numeric non-functional targets or a named owner with a date, a populated [assumptions register](../templates/definition/assumptions-register.md), a written out-of-scope the sponsor has read, and a signature on the business case itself. Two of those this path does not build for you, deliberately: fill the register from your step 2 assumption map before the session, and for the sponsor line name the invented human who would sign, because "the sponsor" is a role and the gate wants a person.

**Pass criteria for the session itself.** A 2 on every Gate 2 line; the assumptions register filled from your step 2 map before the session rather than during it; an invented human named on the sponsor line; and the weight question answered on stakes, audience, and reversibility, whichever way you landed. A 1 anywhere sends the step that produced the artifact back as a fresh attempt, not an edit to the file the tutor already read. A session in which nothing scored below 2 earns one check before you believe it: reopen the out-of-scope section and ask whether the sponsor who wanted those items would accept the reasons as written. That is the line readers of this path most often pass by agreeing with themselves, because the exclusions were argued inside their own head and never against anybody who wanted them.

**The trap, and its tell.** Defending the PRD's weight with effort. The tell: your answer describes how much work the document was. Stakes, audience, and reversibility decide weight, and the honest concession, that a reversible two-team release wanted a one-pager plus criteria, scores the same 2 as a successful defense. Conceding on the right axis is the skill being tested.

**Time.** One session of ninety minutes. Expect step 5's criteria to score highest and the assumptions register to score lowest, because it is the artifact no previous role ever asked you to keep.

Next: [Senior sharpening](path-senior.md) once you have shipped something real through a gate, or the [library](library.md) for the long versions of what transferred least comfortably.
