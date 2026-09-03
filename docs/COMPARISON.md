# Product Manager OS: honest comparison

**Comparison date: 2026-09-03.** Everything below was read from the public repositories, documentation sites, and product pages of the systems named, on that date, by one person. No controlled trial was run: nobody built the same feature four times with four toolchains and measured the outcome, and you should discount every claim here by that fact. Categories in this space move in weeks, so treat this file as a dated snapshot and re-read the primary sources before you make a purchasing or adoption decision.

Two things are deliberately absent. Star counts, download counts, and community size are not in the table, because they measure attention rather than capability, and quoting them ages this file badly. And there is no scoring column, because a total would let a reader skip the only part of a comparison that is worth reading: the row where the other system wins.

## The table

| System | Category | What it owns | What it does better than this repo | Where this repo is the better tool |
|---|---|---|---|---|
| [spec-kit](https://github.com/github/spec-kit) | Spec-driven development toolkit | Turning a written specification into working code through a fixed command sequence | Shipping code. It installs as a CLI, injects its command set into your coding agent, holds project-wide principles in one governing file, and decomposes a spec into implementable tasks. Nothing here does that. | Everything before the spec exists, and everything after the code ships: discovery evidence, weight choice, business case, launch readiness, outcome verification at Gate 6 |
| [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Agentic build method | A planning phase then an IDE build cycle, run by named agent personas that hand work to each other | The build loop, in depth. Sharded plans become story files with the context an implementing agent needs, and the developer and reviewer roles are genuinely separate runtime agents. Its expansion packs also carry the method outside software. | Judgment layers it does not attempt: why a method exists, when it lies, the gate a human signs, the regulated overlay, and the pencil path for anyone with no agent runtime |
| ChatPRD | Hosted commercial AI PM product | Drafting and coaching a PM through product documents in a browser, with a company behind it | Being usable in five minutes by someone who does not open a terminal. Hosted collaboration, a maintained product roadmap, mobile access, and a coaching tone that is genuinely good for a first-time PM. There is a support address to email. | Inspectability and ownership. Every prompt here is a file you can read, diff, fork, and pin to a version; nothing here calls out on its own, and the one component that makes a network call is an optional runner you point at a gateway you chose; and the artifacts are yours in plain markdown with no subscription attached |
| PM template packs (Notion, Confluence, and paid bundles) | Template libraries | A pretty, immediately usable set of blank documents inside the tool your company already uses | Adoption friction and collaboration. Comments, mentions, permissions, and a wiki your stakeholders already log into. Visual polish beats plain markdown for an executive audience. | Linkage and judgment. A pack gives you blanks; this gives you which blank, why the method behind it exists, where it misleads, when to skip it, and a gate that tests the filled result |

## Pick by your binding constraint

Feature lists do not decide this; the thing currently stopping you does. Read down the left column until one row is uncomfortably accurate.

| What is actually blocking you | Reach for | Because |
|---|---|---|
| Nobody will sign, or a launch keeps getting surprised late | This repository | The scarce artifact is a gate with a named person who can fail it, and none of the others has one |
| The problem is agreed and code is not appearing | spec-kit or BMAD | Both instrument implementation, and this repository deliberately stops at the spec |
| Documents get written and nobody reads or comments on them | A pack in your wiki, or a hosted product | The constraint is where the document lives, and markdown in a clone loses that fight |
| Documents exist, are read, and are confidently wrong | This repository | The fixes are evidence classes, skip lines, and a gate that tests a filled document, which is the layer the others do not carry |
| A supervisor or auditor can ask for the file | This repository, regulated overlay on | It is the only one in the list that ships a regulatory overlay with its own review gate |

## spec-kit

spec-kit is the strongest thing in this list at the job it chose, and the job it chose is downstream of almost everything in this repository. Its sequence runs from a governing principles file through specify, clarify, plan, tasks, and implement, which means its unit of success is running software. This repository's unit of success is a signed decision, and those are different products even though both use the word "spec".

**Pick spec-kit when** the problem is already understood, a human has decided it is worth building, and the remaining risk is implementation, because that is exactly the interval it instruments. **Pick this repository when** the expensive risk is upstream: whether the problem is real, what the thing should be, what it costs to be wrong, and who signs.

**The weakness it exposes here.** This repository has no installer and generates no code. `git clone` and copy a file is the whole install story, which is fine for a document system and thin next to a tool that injects a command set into your agent for you. If you want the loop and the code generation, run both: take a filled [PRD](../templates/definition/prd.md) and [acceptance criteria](../templates/definition/acceptance-criteria.md) from here into spec-kit's specify step. Those two artifacts are a better spec-kit input than a fresh prompt, because they carry the evidence and the kill criteria that a prompt cannot.

## BMAD-METHOD

BMAD is the most ambitious agentic method in the list, and its central insight is one this repository borrows in spirit: put the plan in files that an agent can carry into a build session, rather than in a chat window that compacts away. Its planning phase produces a PRD and an architecture, its build cycle turns those into story files, and its roles are separate agents rather than sections of one prompt.

**Pick BMAD when** the team's bottleneck is throughput of implemented stories and you are willing to run an agent-driven pipeline end to end. **Pick this repository when** the bottleneck is a decision nobody will sign, a stakeholder who will be surprised at launch, or a regulator who will ask for the file.

**The weakness it exposes here.** BMAD's agents actually do the work; this repository's [agents](../agents/README.md) are instruction files that shape how a model behaves inside a document task, which is a smaller claim. BMAD also has a community that finds its bugs, and this repository has a lint gate and one maintainer. Run both when the work is greenfield software: use Gate 1 and Gate 2 here to decide what earns a build slot, then hand the signed PRD to BMAD's planning phase rather than starting from a brief.

## ChatPRD

This is the only commercial hosted product in the comparison, and the honest headline is that a funded team maintaining a polished tool beats a repository maintained by one person on several axes that matter in real adoption: onboarding, reliability, collaboration, and the fact that a colleague who has never used a terminal can be productive in it today.

**Pick ChatPRD when** the people who must write documents are not going to clone a repository, and you would rather have adoption than inspectability. That is a defensible trade and it is often the right one. **Pick this repository when** any of three conditions holds: you need to know exactly what prompt produced a document, because a reviewer or a regulator will ask; you need your prompts pinned to a version so a vendor update cannot change your output mid-quarter; or your product data cannot go to a third party.

**The weakness it exposes here.** No hosted collaboration, no comments, no permissions, no mobile, no support address. There is also no coaching layer for a first-time PM beyond [learn/](../learn/README.md), which is a curriculum rather than a companion. If a PM needs someone to explain what a PRD is while they write it, a hosted coach is a kinder answer than a repository.

## PM template packs

Template packs are the incumbent and they are not going away, because their distribution model is right: they live where the work already lives. The gap is not aesthetic. A pack hands you a hundred blanks with no answer to the questions that arrive first, which are which of these does this decision deserve, why does this method exist, and how will I know the filled version is any good.

**Pick a pack when** the org's real problem is that documents are inconsistent across teams and a shared shape would fix most of it. **Pick this repository when** the problem is that filled documents are confidently wrong, because the fixes for that are the parts a pack does not carry: an evidence ladder, a [skip line](../frameworks/README.md) on every method, a [weight tree](../os/WHICH-DOCUMENT.md), and a gate a named human signs.

**The weakness it exposes here.** Plain markdown in a git repository is a worse reading experience for a stakeholder than a well-built wiki page, and the volume here is genuinely intimidating: a first-time visitor sees a catalog of templates and dozens of worksheets and reasonably concludes this is heavier than it is. The intended entry is three files, [os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md), [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md), and one template, and the rest is a library you visit when a specific question arrives. If that is not obvious from the front door, that is a defect here, not a misreading by the visitor.

## Running two of these together

The category talks as though these are rival purchases. In practice the pairs below are the common and correct configuration, because the systems own different halves of one job. What matters in a handoff is what you strip: hand a code generator your business case and you have spent context on something it cannot use, and hand an agentic build loop a PRD with no numeric constraints and it will cheerfully ship past them.

| Take from here | Hand it to | What it becomes there | Strip before handing over |
|---|---|---|---|
| Filled [PRD](../templates/definition/prd.md) plus [acceptance criteria](../templates/definition/acceptance-criteria.md) | spec-kit's specify step | The spec the command sequence plans and implements against | The business case, comms plan, and GTM sections. Keep the kill criteria: a stop rule is the one piece of judgment a generator will never propose |
| The signed Gate 2 packet | BMAD's planning phase | Its PRD and architecture inputs, before sharding into stories | The discovery narrative. Keep the four risks and every [NFR](../templates/definition/nfr.md) number, because numeric constraints are the first thing lost when a plan is sharded into stories |
| A ChatPRD or in-house draft | This repository's Gate 2 checklist | A tested document rather than a written one | Nothing. Run it as written and read the unknown column: hosted drafts most often lack kill criteria, counter-evidence per risk, and a validate-by date on any assumption |
| A pack's filled template | The [gate](../os/STAGE-GATES.md) for its stage | Evidence of what the pack's shape does not ask for | Nothing. Each gate line you cannot evidence is a field your template is missing, and that list is the cheapest audit in this file |

## Where this repository loses, in one place

Scattering weaknesses through the prose above would be a way of hiding them. Here they are together, each marked fixable or structural, because a reader deciding today needs to know which ones a later release could remove.

- **No installer, no command set.** `git clone` and copy a file is the whole install story. Fixable, and low value: an installer would not change what the tree is.
- **No code generation, ever.** Out of scope by design, which means for a solo builder shipping a side project this is the wrong tool on its own. Structural.
- **No hosted collaboration.** No comments, no mentions, no permissions, no mobile. Structural for a git repository, and the reason a wiki keeps winning the stakeholder-review step.
- **One maintainer.** No community finding bugs in parallel, no support address. Structural until adoption changes it, and mitigated only by the lint gate and the small size of the surface.
- **Volume at the front door.** A visitor sees a large catalog and reasonably concludes this is heavier than it is, when the intended entry is three files. Fixable, and currently a defect here rather than a misreading by the visitor.
- **No outcome evidence.** Nobody has shown that this, or anything in its category, produces better products. Structural for the category, and the reason the claims in this file stay at the level of what is recoverable later.
- **The AI layers are optional to use and not optional to keep.** A fork can run the whole loop with no model, and a fork that deletes `skills/`, `agents/`, `system/`, or `routing/` breaks the link gate in the hundreds, because every template points up at the procedure that drives it. Fixable, at the price of a tree that cross-references less well, which is why it has not been fixed.
- **Unproven outside software and payments.** The loop and gates plausibly transfer; the definition and architecture templates carry assumptions from those two worlds. An honest limit, not a fixable one.

## Three teams choosing, worked

Every number and product below is invented, and each scenario ends with the rule that actually decided it. The three products are the ones the rest of the tree already uses, so a reader who has worked a [learn path](../learn/README.md) or read [PHILOSOPHY.md](PHILOSOPHY.md) meets the same fictional teams here rather than three new ones.

**Ledgerline, a fictional expense copilot, eleven people, one regulated market.** Two engineers, a designer, and a compliance officer who can stop a launch. They picked this repository plus spec-kit: the gates because a supervisor can ask for the file, and spec-kit because the build risk is real and they had nobody to spare for it. **The deciding rule:** when a named person outside product can stop your launch, you need the artifact that answers them before you need the tool that writes code faster.

**Streakline, a fictional habit tracker, in its two-founder year before the first engineering hires, no regulator.** They took the weight tree, four templates, and Gate 1, and skipped the rest. Running six full gates across two people would have meant one person signing their own work, which is the definition of theater. **The deciding rule:** below three functions, take the templates and skip the ceremony, because a gate needs two people to mean anything. By the month-eleven state the [foundations path](../learn/path-foundations.md) picks Streakline up in, with five people and a retention problem, the answer has changed and Gate 6 has become the one worth running.

**Meterly, a fictional API metering product inside a larger company, thirty people across four functions.** They already had a company PRD template that reviewers knew, and a Confluence space nobody was leaving. They kept both, added kill criteria to their own template, and ran these gate checklists against their own artifacts. **The deciding rule:** when adoption is the binding constraint, port the mechanisms into the tooling people already open, because a better template nobody opens loses to a worse one they do.

## Adjacent systems, named but not scored

Three more systems informed the design and are deliberately absent from the table: BuildBetter's product-os, which owns discovery; deanpeters' Product-Manager-Skills, a prompt and skill collection; and the vendor product-management plugins that ship with agent runtimes. They are not scored for one honest reason: each either sits inside a category already represented by a scored row, or I have not used it long enough on real work to judge it, and a scored row built on a skim would be the exact failure this file is written against. The teardown that produced this repository's four gap claims covered all of them, and it is recorded in [ARCHITECTURE.md](ARCHITECTURE.md) and the 0.5.1 entry of [CHANGELOG.md](../CHANGELOG.md).

## What no comparison in this category can tell you

- **Nobody has measured outcomes.** There is no study showing that any product operating system, this one included, produces better products. What these systems demonstrably change is whether a decision is recoverable six months later, which is worth having and is not the same claim.
- **Fit dominates features.** A two-person startup with no regulator and one engineer will get more from a pack and a habit than from a six-gate loop, and saying otherwise would be selling. The gates start paying when more than two functions must agree, or when being wrong costs a quarter.
- **The categories overlap on purpose.** These four are not four answers to one question. Roughly: this repository decides and records, spec-kit and BMAD build, ChatPRD drafts, packs standardize. The common failure is buying the second one for the first one's problem, then concluding the category does not work.

## The four gap claims, as falsifiable statements

This repository justifies itself with four claims about the field. Each is written below in a form that can be checked and therefore disproved, with what would disprove it, because a gap claim nobody can test is marketing wearing a table's clothes.

1. **No surveyed system chains discovery through post-launch verification in one tree.** Disproved by any system that ships both an evidence-cited discovery artifact and an outcome-verification artifact that references it. Adding a discovery layer to a build-focused system would do it.
2. **No surveyed system ships a regulatory overlay.** Disproved by a shipped template that asks for a regulatory precondition register and blocks a gate on it, rather than by a prompt that mentions compliance.
3. **No surveyed system carries a canon knowledge layer with named attribution and stated failure modes.** Disproved by a method library where each entry names an originator and the situation in which the method misleads. Attribution alone does not do it; the failure mode is the load-bearing half.
4. **No surveyed system runs a whole-tree consistency gate.** Disproved by any repository whose CI fails on a broken internal link or a missing required header across all of its own documents.

If you can disprove one, that is a genuinely useful issue to open, and the honest response is to narrow the claim in this file rather than to argue.

## How to evaluate any of these in one afternoon

Do not compare feature lists, because every system in this category writes its own list to win. Instead take one decision you have already made and regret, ideally one where the postmortem found something knowable in advance. Reconstruct the inputs you had at the time, then run that decision through each candidate for an hour.

Score each on one question: would this have surfaced the thing you missed, before you spent the money? A tool that would have caught it is worth its overhead on your real work; a tool that produces a handsomer version of the document you already wrote is not, however good the document looks. Two hours of that is worth more than a week of comparison reading, this file included.

## How to re-check this table

Read the four primary sources again, note the date, and rewrite any row where the capability changed. Two specific things to watch, because they are the rows most likely to flip: whether the build-focused systems add an upstream discovery or evidence layer, which would take a real bite out of the middle column here, and whether the hosted products add exportable, inspectable prompts, which would remove this repository's clearest structural advantage. If either happens, this file should say so in the same release it happens in, and [CHANGELOG.md](../CHANGELOG.md) should carry the line.

Related reading: [PHILOSOPHY.md](PHILOSOPHY.md) for the beliefs that produced these trade-offs, [FAQ.md](FAQ.md) for the skeptical questions this comparison usually provokes, and [ARCHITECTURE.md](ARCHITECTURE.md) for the layer map the middle column keeps referring to.
