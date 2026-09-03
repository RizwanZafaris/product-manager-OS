# Product Manager OS: Philosophy

This file states what the repository believes, and it is written to be argued with. Nine beliefs follow. Each one gets the strongest counter-argument I could build against it, taken seriously rather than staged, and then the mechanism in the tree that makes the belief operational. A belief with no mechanism behind it is a mood, and a mood cannot fail a gate.

Read this when you want to know why a template is shaped the way it is. Read [ARCHITECTURE.md](ARCHITECTURE.md) when you want to know where things live, and [COMPARISON.md](COMPARISON.md) when you want to know what else you could use instead.

---

## 1. Evidence beats opinion, and the real enemy is unlabeled opinion

Every artifact here asks where a claim came from. The [evidence note](../templates/discovery/evidence-note.md) wants a verbatim quote, a source, and two dates. The [personas template](../templates/discovery/personas.md) marks itself an assumption below five cited interviews. Gate 1 refuses a cost of inaction without the calculation shown. The point is not that opinion is worthless: the point is that a document mixes measured facts and confident guesses at the same font size, and six weeks later nobody can tell which was which.

**The counter-argument.** Great products are built by people with taste who moved before the evidence existed. Evidence-first cultures ship the thing the data could justify, which is the thing the last competitor already shipped. Worse, evidence theater is real: five interviews with the five friendliest customers is a ritual, not a fact, and demanding citations can be a way for the timid to stall the bold.

**What the tree actually does about it.** It does not ban opinion, it ranks it. The five-class evidence ladder in [os/CONDUCTOR.md](../os/CONDUCTOR.md) runs from observed behavior down to team belief, and class five is a filing instruction rather than a defeat: the belief goes to the [assumptions register](../templates/definition/assumptions-register.md) with an owner and a validate-by date, then the work proceeds. A founder's hunch is a legal input. A founder's hunch wearing the costume of a measured result is not.

**The failure mode, and its tell.** Evidence laundering: a number enters as an estimate in a spreadsheet cell, gets copied into a deck, then returns in a PRD with no source. The tell is a number with no unit, no period, and no owner, which is exactly the pattern the challenge grammar routes to the assumptions register. If you can ask "per what, measured when, by whom" and nobody in the room can answer, you are reading laundry.

**What good looks like.** Restow, a fictional returns portal, writes "38 of 61 returns in March were re-shipped to the wrong address, per the ops export dated 2026-04-02". The anti-pattern says "address errors are a major driver of returns cost", which cannot be checked, cannot be falsified, and cannot be sized.

---

## 2. A gate that cannot fail is a ceremony

Six stages, six gates, each a form with checkboxes and a signature line, in [os/STAGE-GATES.md](../os/STAGE-GATES.md). A gate passes when the form is complete and a named human signs it, and a failed gate is a normal outcome that gets recorded with owners and re-run. No agent ticks a box here, ever, because the box is an assertion about the world and a model has no standing to assert it.

**The counter-argument.** Stage gates are the artifact of the era product management spent a decade escaping. They add latency, they reward the person who can fill a form over the person who can ship, and in most organizations they degrade within two quarters into a meeting where everyone nods because stopping the project would be socially expensive. A gate nobody has ever failed is worse than no gate: it launders risk while consuming calendar.

**What the tree actually does about it.** Three defenses. The gate has to name a person with standing to stop the stage, which is a different question from who runs it. The weight of the document going into the gate is chosen first, by [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md), so a flag-reversible sprint change never buys a twelve-section spec; the gate asks the same questions of a one-pager, in fewer words, not in fewer answers. And every gate carries a written skip-risk warning, so the person waving it through is waving through something specific.

**The failure mode, and its tell.** The rubber stamp. The tell is an attempt count that never exceeds one. If your `products/<name>/gates/` folder holds six gate forms and every one passed on attempt one, the gate is not measuring anything; the honest reading is that the checklist was written to match the artifact rather than the artifact to the checklist.

**Micro-example.** Restow ran Gate 1 twice. Attempt one failed on two lines: the cost of inaction had no calculation behind it, and no case for no-go had been argued. Attempt two, nine days later, carried an ops export and a written no-go case that lost on one number. The nine days were the cheapest nine days in the project, because the alternative was discovering the same gap at Gate 5 with a launch date attached.

**The decision rule.** If nobody in the room can name what evidence would have produced a NO-GO, do not hold the gate, because you are about to spend an hour manufacturing consent you already had. Cancel it, log the decision, and put the hour into the weakest line on the checklist.

---

## 3. Documents are decisions, not artifacts

A document here exists to record a decision and its rationale at the moment the decision was cheap to argue about. That is why [decision-log.md](../templates/execution/decision-log.md) numbers entries, why [adr.md](../templates/architecture/adr.md) supersedes rather than edits, and why the PRD carries kill criteria: the conditions under which the team stops, each with a threshold, a check point, and the person allowed to call it.

**The counter-argument.** Documents rot. Code is the only truth, the tracker is the only schedule, and a PRD is out of date the week after Gate 2. Teams that write more end up maintaining a parallel fiction, and the maintenance tax falls on the PM, who is the least able to pay it. The honest version of this argument is strong: most PRDs are read once, by three people, in the week they are written.

**What the tree actually does about it.** It separates the two genres that the word "document" hides. A decision record is append-only and never needs updating, because it is a statement about a moment: on this date, with these options and this evidence, we chose this, and here is who dissented. A specification is a living statement about the present, and it does rot, which is why the tree keeps specifications thin and pushes durable content into records. Reversing an ADR writes a second ADR and leaves the first standing, because the reversal's value is in the pair.

**The failure mode, and its tell.** The zombie spec. The tell is a document whose last edit predates the last three shipped changes, still linked from the tracker as the source of truth. When you find one, do not update it: cut it to the decisions it records, mark the rest superseded, and let the tracker own the present.

**The decision rule.** If a sentence will be equally true in a year, it belongs in a record; if it describes what is currently intended, it belongs in a thin specification that someone owns. Sentences that cannot pass either test are the ones to cut, because they are the reason people stop reading the document that contains the two that matter.

**Micro-example.** Meterly, fictional API usage metering, chose per-request counting over per-connection in ADR 004 with three consequences listed. Eleven months later, per-connection wins on a customer with long-lived streams. ADR 011 supersedes 004. The team that kept both can answer the board question "did we know this could happen"; the team that edited 004 in place cannot, and will spend the meeting reconstructing a memory.

---

## 4. The model should interrogate, not ghostwrite

Say "start" and you meet an interviewer, not a drafting service. The [Conductor](../os/CONDUCTOR.md) asks one question at a time, names what a wrong answer costs, offers a recommended default so agreeing costs you one word, cross-examines a weak answer at most twice, and then parks it visibly instead of accepting it quietly. It writes only what you have said.

**The counter-argument.** Ghostwriting is the actual time saver, and pretending otherwise is precious. A PM with a first draft in four minutes edits it into something good in an hour; a PM being interviewed for that hour has a blank page and a headache. Interviewing is also patronizing to the expert: a director with a decade in payments does not need a model asking whether the problem is real.

**What the tree actually does about it.** It concedes most of the ground and holds one line. Drafting is fine where the content is a rearrangement of things you already established, which is why skills like [write-prd](../skills/write-prd/SKILL.md) and [story-writer](../skills/story-writer/SKILL.md) draft freely from filled inputs. The line is the input side: a model may not originate a fact, a name, a number, a citation, or a quote. That single rule is what separates acceleration from contamination, because a fluent draft with invented specifics is the most expensive document in this system: it passes the reading test that a thin draft would have failed, and it survives to the gate.

**The failure mode, and its tell.** Fluency mistaken for grounding. The tell is a paragraph you enjoy reading that you cannot trace to a source, usually carrying a suspiciously round number or an unattributed "studies show". The [smart skip](../os/CONDUCTOR.md) rule cuts the other way too: a question the loaded context already answers is skipped with the source cited, so the interview is short where you were prepared and long only where you were not.

**The decision rule.** Interrogate before Gate 2 and after Gate 6, because those are the two moments where a wrong input propagates furthest; draft freely in between, because by then the facts are on the record and the work is arrangement.

---

## 5. The smallest sufficient document wins

Weight is chosen before a template opens, by three questions: stakes, audience, reversibility. The five weights run from a ten-minute decision-log entry to a BRD, PRD, and FRD stack. Every template is a superset, and the instruction to delete is stated in [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md) and repeated inside the four templates where the pull to fill every field is strongest.

**The counter-argument.** Superset templates are safer. The section you deleted is the risk you did not consider, and juniors do not know which sections carry weight, so telling them to cut is telling them to cut the parts they least understand. Standardized full documents are also easier to review across a portfolio, because every reviewer knows where to look.

**What the tree actually does about it.** It makes cutting a recorded act rather than a private one. Upgrading a weight is normal, downgrading is a decision, and both get one line in the decision log naming the weight and why, because that line is what tells the next person where a gap came from. It also refuses to let lightness buy silence at the gate: Gate 2 asks a one-pager the same questions it asks a PRD.

**The failure mode, and its tell.** The form nobody trims. The tell is a section heading standing over white space, or over the phrase "N/A" with no reason after it. An empty section reads as an unanswered question and teaches every future reader to skim, which is how a real answer three sections down gets missed.

**The decision rule.** When two weights are both defensible, take the lighter one and write one line naming the choice, because the lighter document gets read and the line is what tells the next person where the gap came from. Upgrading later is normal; discovering that nobody read the heavy version is not recoverable.

**Micro-example.** Streakline, a fictional habit tracker, spent six days on a full PRD for a reminder-time picker that one engineer shipped behind a flag in three days. The weight tree would have said ticket, with acceptance criteria attached, in under an hour. The cost was not the six days; it was that the next real quarter-scale bet got the same six days, because the team had learned that PRDs cost six days.

---

## 6. Every method must publish its own off switch

Each knowledge card and each worksheet carries a line beginning **Skip it when**, naming the situation where running the method costs a week and returns nothing. RICE gets skipped when the list is under five items. A method that never names its own uselessness is being sold, not taught.

**The counter-argument.** Giving people permission to skip is giving them permission to skip everything, and the methods most worth running are the ones that feel least necessary in the moment. The premortem is skipped by exactly the teams that need it. If you hand a stressed PM an off switch, they will find that every method qualifies.

**What the tree actually does about it.** It writes the skip condition as a test on the situation, not on your appetite. "The list is under five items and the first two are obvious" is checkable by someone else in the room. "We do not have time" is not a skip condition, it is a schedule. The gate is the backstop: skipping a method is allowed, skipping the gate line the method was going to evidence is not, so you either produce the evidence another way or you carry it as a named unknown.

**Micro-example.** Streakline's team skipped the premortem before its second launch, on the reasoning that the first launch had gone fine. The failure that arrived, a notification job firing in the user's server timezone rather than their own, was the sort of thing a premortem surfaces in twenty minutes. The skip condition for a premortem is a change with no new integration, no new data path, and no new audience; that launch had a new data path, so the skip was never legal under the method's own line.

**The failure mode, and its tell.** Ritual application. The tell is a scoring sheet whose ranking nobody disputed, which usually means the sheet documented a decision already made. When that happens twice on the same team, the sheet has become a compliance artifact and its output has stopped changing anyone's plan.

---

## 7. Attribution is load bearing, not politeness

Every card and worksheet names its originator and year, in this repository's own words, and links the method to the templates it feeds. Where there is no single originator, the file says so instead of inventing a founder: TAM, SAM, and SOM, RACI, and the risk matrix all state their honest lineage.

**The counter-argument.** Nobody reads citations in a working document, attribution adds a maintenance surface, and the courtesy shades into cargo cult: invoking a famous name to end an argument is worse than having no name at all, because the name is doing the work that reasoning should do.

**What the tree actually does about it.** Attribution is a check, not a credential. Knowing that RICE came out of a 2016 blog post at one company tells you the sample it was built from and therefore where it transfers; knowing a method has no named origin tells you to trust it only as far as your own experience carries it. The rule that makes this honest is the one against copying source text: the reasoning is restated here, so if the restatement is wrong you can go and find that out.

**Micro-example.** Two methods on the shelf both promise to rank a backlog. One names a person, a company, and a year, which tells you it was built on one company's subscription business and that its reach unit assumes repeat usage. The other names nobody. On Meterly's usage-metered product the first method's assumptions are checkable and one of them fails, which is useful; nothing about the second can be checked at all, which is not.

**The failure mode, and its tell.** The unfalsifiable framework. The tell is a method with no stated origin, no stated failure mode, and no situation where it does not apply. Anything that explains every outcome after the fact predicts none of them in advance, and the cost of noticing that is one line of provenance.

---

## 8. The system must survive its own AI

Method one of four uses no model at all. Nothing in `knowledge/`, `frameworks/`, or `templates/` depends on any AI layer existing, the boot prompt assumes no file access, and the gates are checklists a human works through with a pencil. Graceful degradation is stated as structural, not aspirational.

**The counter-argument.** Designing for the free tier costs the frontier. Every mechanism that must also work on paper is a mechanism that cannot use tool calls, retrieval, or evaluation loops, so the pencil path drags the whole system down to the capability of its weakest runtime. And the hedge is self-defeating: if the AI layer is genuinely good, insisting it is optional signals that its author does not believe in it.

**What the tree actually does about it.** It splits the layers so degradation is partial rather than total. Losing the model costs you the interview, the drafting, and the routing; it does not cost you the format, the gates, or the record, because those are files. The dependency direction enforces it: skills cite templates, templates never cite skills as a requirement. The practical test is a fork with `skills/`, `agents/`, `system/`, and `routing/` deleted, which still runs a product from Gate 1 to Gate 6.

**The decision rule.** Before adding any mechanism, ask what remains of it with the model switched off. If the answer is nothing, it belongs in `skills/` or `agents/`; if the answer is a file someone can fill in by hand, it belongs in `templates/` or `frameworks/`. That single question is what has kept the pencil path real through five versions.

**The failure mode, and its tell.** Silent capability drift. The tell is a template whose instructions only make sense if a model is reading them, which is how a document system quietly becomes a prompt library. If a section cannot be completed by a human with the same inputs, it belongs in `skills/`.

---

## 9. Rot must be visible, including this repository's own

Citations in the regulated overlay carry verification dates, and an as-of date past the staleness window fails the gate rather than looking maintained. The changelog carries a known-gaps list, because a release note that only lists wins is marketing. If maintenance stops, an ARCHIVED notice with a date goes at the top of the README instead of the repository quietly decaying.

**The counter-argument.** Loud staleness is a way of shipping your maintenance debt to the user. A gate that fails on a date, rather than on a fact, cries wolf: the citation may be perfectly current, the calendar simply moved, and a team that gets red-lined for the calendar learns to disable the check. That is a worse outcome than a slightly stale document.

**What the tree actually does about it.** It scopes the date check to the material where the calendar genuinely changes the answer, which is the regulated overlay, and it keeps the failure cheap to clear: re-verify, restate the date, move on. Everywhere else the honesty mechanism is disclosure rather than enforcement, which is why the version policy promises that field names and paths do not move under you inside a major version, and why the gate's own output says green means the tree is consistent, not that anything in it is true.

**The last belief, and it is about this file.** A system that publishes its beliefs invites the counter-evidence that a system quietly holding them never receives. If one of the nine above is wrong, the fastest way to find out is that it is written down where you can point at it. Disagreements belong in an issue, and the ones that land change the file.

---

## Where these beliefs are enforced

| Belief | Enforced by |
|---|---|
| 1. Evidence over unlabeled opinion | Evidence ladder in [os/CONDUCTOR.md](../os/CONDUCTOR.md), [evidence-note.md](../templates/discovery/evidence-note.md), Gate 1 |
| 2. Gates that can fail | [os/STAGE-GATES.md](../os/STAGE-GATES.md), sign-off lines, skip-risk warnings, gate attempts on file |
| 3. Documents as decisions | [decision-log.md](../templates/execution/decision-log.md), [adr.md](../templates/architecture/adr.md), PRD kill criteria |
| 4. Interrogate before drafting | [os/CONDUCTOR.md](../os/CONDUCTOR.md), the never-invent rule in [AGENTS.md](../AGENTS.md) |
| 5. Smallest sufficient document | [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md), the delete-unused-sections rule |
| 6. Published off switches | The Skip it when line in every [knowledge](../knowledge/README.md) card and [framework](../frameworks/README.md) worksheet |
| 7. Attribution as a check | Named originator and year in every card and worksheet |
| 8. Survives its own AI | Method one in [README.md](../README.md), downward-only dependencies |
| 9. Visible rot | Staleness failure in [lint.py](../lint.py), known gaps in [CHANGELOG.md](../CHANGELOG.md) |
