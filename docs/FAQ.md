# Product Manager OS: FAQ

The sixteen questions a skeptical PM actually asks, answered without a pitch. Where the honest answer is a weakness, it is written as a weakness, because a FAQ that only lists strengths is a brochure with question marks in it. Last reviewed 2026-09-03.

Adjacent files: [PHILOSOPHY.md](PHILOSOPHY.md) argues the beliefs behind these answers, [COMPARISON.md](COMPARISON.md) puts the repository next to its alternatives, [ARCHITECTURE.md](ARCHITECTURE.md) maps the tree, and [../GLOSSARY.md](../GLOSSARY.md) defines the vocabulary used below.

---

## What it is

**1. What is this, in one paragraph, without the word "OS"?**

A set of markdown files that runs a product from first evidence to sunset: six stage gates with checklists a human signs, a template for every artifact those gates ask for, a knowledge layer explaining why each method exists and how it misleads, worksheets that run the methods, and optional prompt layers so a model can drive any of it. It is a document system with AI attached, in that order.

The shortest honest description is a library plus a discipline. The library is the templates, cards, and worksheets. The discipline is that a stage does not open until the previous gate passes on evidence, and that the size of the document is chosen before the document is opened.

**2. Do I need AI to use it?**

No, and this is load bearing rather than a hedge. Method one of the four in [README.md](../README.md) uses no model: clone, copy a template, fill it in any editor, work the gate checklist by hand. No document under `knowledge/`, `frameworks/`, `templates/`, or `os/` needs an AI layer to be readable or fillable, and the direction of dependency runs downward: a skill requires its template, a template does not require its skill.

**What is actually proved, and what is not.** `harness/` is fully deletable and a gate proves it, which is the run recorded in `harness/README.md`. The document layers are a weaker claim than this file used to make. Delete `skills/`, `agents/`, `system/`, and `routing/` and the remaining documents still take a product from Gate 1 to Gate 6, because every template's guidance is prose and its `Skill:` header is a pointer rather than a requirement. The same deletion breaks the structural lint gate in the hundreds, because those pointers are markdown links and links are what the gate checks. So the load-bearing sentence is this one: you can run the whole loop without a model, and you cannot delete a content layer and keep a green gate. Delete `templates/` instead and the AI layers have nothing left to produce, which tells you which half is the product.

**3. Why not just ask a model for a PRD?**

Because you will get one, and it will be fluent. A model with no evidence produces a confident document at the same reading quality as a grounded one, and that is worse than a thin document: the thin one fails the reading test and gets sent back, the fluent one survives to the gate and gets signed. What this repository adds to the same model is input discipline and shape. The [Conductor](../os/CONDUCTOR.md) asks before it writes and parks weak answers visibly, the never-invent rule in [AGENTS.md](../AGENTS.md) forbids originating a fact, a name, a number, or a citation, and the [PRD template](../templates/definition/prd.md) demands sections a model will not think to ask for, including kill criteria and one counter-fact per risk.

**When asking directly is the right call:** you need one document, you already hold the evidence in your head, and nobody downstream will have to reconstruct why. That is a real and common situation, and pretending it needs a six-gate loop would be selling.

**4. Isn't this waterfall with extra steps?**

It has the shape and not the mechanics, and three differences decide it. The loop returns: Gate 6 verifies outcomes and feeds DISCOVER again, so the terminal state is learning rather than handover. The weight is chosen per decision rather than per project, so a flag-reversible change costs an hour at ticket weight while a quarter-scale bet earns a full PRD, and both answer the same gate questions in different numbers of words. And the gates test evidence rather than completion: Gate 1 asks whether anyone seriously argued the case for no-go, which is not a question a phase review has ever asked.

**Where the critique lands:** if you run every decision at PRD weight, you have built waterfall out of these parts. [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md) exists to stop that, and the tell that it is happening is a decision log with no entries at "decide and log" weight.

**5. Won't the gates just become theater?**

Often, yes, and the tell sits in your own gate folder: if every gate passed on attempt one, it is already theater. The design defenses are that the gate names a person with standing to stop the stage, which is a different person from the one running it, that each gate carries a written skip-risk warning so waving it through means waving through something specific, and that failed attempts are filed rather than deleted.

**The rule that does the most work:** if nobody at the gate can name the evidence that would have produced a NO-GO, cancel the meeting and spend the hour on the weakest checklist line, because you were about to manufacture consent you already had.

## Trust and provenance

**6. Is this AI-generated?**

It was written with Claude Code by a working payments CPO, every non-merge commit carries a trailer saying so, and hiding that would be the exact defect this repository claims to guard against. What it means in practice matters more than the label: the structure, the beliefs, the skip conditions, and the failure modes come from the maintainer's own product and payments work, while the model did drafting, consistency, and volume.

**How to check the claim rather than take it:** read the commit history. The trailers name the tool on every commit that is not a merge, the messages show what was rewritten and when, and the [changelog](../CHANGELOG.md) records which release studied which prior art before writing. A repository hiding its authorship would have no reason to keep any of that legible.

**What to audit hardest:** anything a model is good at producing and bad at grounding. Claims about the field, numbers, and attributions. If you find a fabricated one, that is a real bug worth an issue, because the never-invent rule applies to this repository as much as to a product run inside it.

**7. Why should I trust a solo maintainer?**

Do not trust the maintainer, check the mechanisms, because that is the only claim one person can honestly make at this scale. Three are checkable in a minute. Every prompt is a file you read before you run it, so there is no hidden instruction. `python3 lint.py --os` fails on broken links, missing template headers, banned characters, drifted pinned files, and secret-shaped strings, so consistency is enforced by a script rather than by attention. And the versioning promise is specific: inside a major version, field names and paths do not move under you, and each breaking change is named in [CHANGELOG.md](../CHANGELOG.md) with its migration. That promise was overstated once and the correction is in the README's versioning section rather than buried: a minor version can add sections that today's checks then expect, so an older filled document keeps working and can still fall short of the current gate.

**What one maintainer cannot give you** is a community that finds bugs faster than you do, or a support address with a person behind it. [COMPARISON.md](COMPARISON.md) names the systems that have both.

**8. What happens when you stop maintaining it?**

Two answers, one promised and one structural. The promise: if maintenance stops, an ARCHIVED notice with a date goes at the top of the README, rather than the repository sitting there looking alive. The structure: on the manual path this is markdown under MIT with no build step, no dependencies, and nothing to call, so an abandoned copy keeps working exactly as well as the day you cloned it. The scripts age no faster: the quality gate, the graph tool, and the runner are Python standard library only, and the single third-party dependency anywhere in the tree is the MCP SDK that the optional desktop adapter needs. What can rot out from under you is the runtime path, because it calls a gateway whose API is not yours to freeze. See [../SECURITY.md](../SECURITY.md) for the two paths.

**The two things that decay anyway.** Regulated citations go stale, and the gate is built to fail on the date rather than hide it. And [COMPARISON.md](COMPARISON.md) ages, which is why it carries a comparison date and a re-check procedure. Forking is the intended succession plan, not a fallback.

**9. How do I know anything in here is true?**

You do not, and the tooling is documented to make exactly one claim: green means the tree is consistent, not that any document in it is true. It prints `ok` and a check count, and everywhere that green is described, in [README.md](../README.md), in `harness/README.md`, and in the gate's own header comment, it is described as structural and nothing more. What is checkable is provenance. Every method names an originator and a year in this repository's own words rather than in copied text, so a wrong restatement can be caught against the source. Every worked number is labeled invented and attached to a fictional product. And six literal metric strings from the maintainer's own past drafts are blocked tree-wide, so a number nobody could source cannot quietly return.

**What to do with a claim you doubt:** treat it the way the tree treats any class-five belief. Write it into your own assumptions register with your name and a validate-by date, act on it if the cost of being wrong is small, and go and check the primary source before it reaches a gate. A sentence in a repository is an argument, not evidence, and that includes the sentences in this file.

## Fit and adoption

**10. How is this different from a Notion template pack?**

A pack answers what a document looks like. This answers the three questions that arrive first: which document this decision deserves, why the method behind it exists and where it lies, and how you will know the filled version is any good. Concretely, the [RICE worksheet](../frameworks/prioritization/rice-scoring-sheet.md) makes you declare one reach unit before scoring, because drift between filers and reports lets a bookkeeping accident decide the ranking, and the [card](../knowledge/rice-prioritization.md) explains why near scores are ties rather than ranks. A blank scoring table carries neither.

**Where the pack wins:** comments, mentions, permissions, and a wiki your stakeholders already open. That is not a small win, and if inconsistency across teams is your actual problem, a pack may fix more of it than this will.

**11. My company already has its own PRD template. Now what?**

Keep it. The field names in it are what your reviewers know how to read, and swapping vocabulary costs more goodwill than it buys. Take the three things in-house templates almost never carry: the [weight tree](../os/WHICH-DOCUMENT.md), so a two-day change stops buying a twelve-section spec; kill criteria, because every system surveyed for the 0.5.1 release could start work and none could stop it; and the gate checklists, run against your own artifacts, since a checklist tests a filled document regardless of whose template produced it.

**The failure mode when a team takes only the gates:** the checklist gets run against a template that has no field for half its lines, so those lines are marked unknown every time and the team learns to ignore the unknown column. If you adopt a gate line, add the field it tests to your own template in the same week, or drop that line on purpose and write down why.

**12. Does it work for a two-person startup, or for something that is not software?**

At two people, run it light and be honest that the gates are cheap versions of themselves. Gate 1's real content is five customer conversations and a written cost of inaction, which is worth a morning at any size. Six full gates start paying when more than two functions must agree, or when being wrong costs a quarter, so below that bar take the templates and skip the ceremony.

**For non-software work,** the loop, the gates, and the discovery and planning material transfer; the definition and architecture templates mostly do not. The honest limit is that this tree was built for software and payments products and has not been proven anywhere else.

**13. How does this fit with Jira, Linear, or Confluence?**

Beside them, not against them. The tracker owns the present, which is what is in flight this week and who has it; this tree owns the record, which is what was decided, on what evidence, and by whom. Those are different half-lives, and the common mistake is asking one tool to do both: a tracker ticket cannot carry a rationale anyone will find in a year, and a document cannot track a sprint without going stale by Wednesday.

**The practical seam:** paste acceptance criteria from the [template](../templates/definition/acceptance-criteria.md) into the ticket, link the ticket back to the decision-log entry number, and never copy a rationale into two places. When they disagree, the record wins on why and the tracker wins on what is happening now.

**14. Do I have to use all of it, and what can I delete?**

No, and most of it. The intended first hour is [os/OPERATING-LOOP.md](../os/OPERATING-LOOP.md), [os/WHICH-DOCUMENT.md](../os/WHICH-DOCUMENT.md), and one template. Two kinds of deletion, and they are not the same:

- **Deletions the gate supports.** `harness/` only. Remove it and `python3 lint.py --os`, `python3 tools/check_manifest.py`, and the graph check all still pass, which is the run recorded in `harness/README.md`.
- **Deletions that keep the documents and cost you the gate.** `learn/`, `examples/`, `routing/`, `agents/`, `skills/`, `system/`, `modules/regulated/` when no supervisor governs your product, and any domain or knowledge card outside your market. Nothing depends upward on these, so every remaining template still fills and every gate still runs by hand. They are also link targets, so the lint gate then reports the links that no longer resolve, in the hundreds for the four AI layers. Fine if you never run the gate; a fork that wants a green gate has to remove the pointers too.

Keep `os/` and the templates you actually use, because the gates reference them by path.

**The one deletion that quietly costs you** is `frameworks/`, because the methods it runs are the ones people otherwise perform from memory, and a scoring argument reconstructed from memory three weeks later is unauditable. If space is the concern, keep the four worksheets your gates actually consume and delete the other fifty-four.

**Inside a document, deleting is the instruction rather than a liberty.** An empty heading reads as an unanswered question and teaches every future reader to skim, which is how the one real answer three sections below it gets missed.

## Practical

**15. Which model should I use, and what will it cost?**

Any capable chat model runs the boot prompt, free tiers included, which is why [system/BOOT-PROMPT.md](../system/BOOT-PROMPT.md) assumes no file access and asks you to paste files by exact path. In an agent CLI, the skills and templates load themselves. The cost lever is the tier doctrine in [routing/README.md](../routing/README.md): extraction and reformatting on a cheap tier, drafting on a coding tier, judgment on a frontier tier.

**The rule behind it:** pay for reasoning where a wrong answer propagates through a gate, and pay nothing extra where the work is rearrangement, because a frontier model reformatting a table is waste and a cheap model critiquing a gate is worse than not asking.

**16. Who owns my data and my output?**

You do, on both counts. There is no telemetry, no account, and no hosted service, and nothing here calls out on its own. One component makes a network call and only when you run it: `harness/runner.py` posts to the gateway URL you put in your own environment, sending the prompt it assembled plus the input you passed it, and reading its credential from an environment variable it never writes down. The desktop adapter speaks over standard input and output, listens on no port, and places no model call. Whatever you paste into a model goes wherever that vendor's terms say it goes, which is between you and them, and if your product data cannot leave your environment then method one uses no model at all. Filled artifacts live in `products/<name>/`, which is gitignored and never shipped here, so your work cannot collide with an update or be committed into this tree by accident. See [../SECURITY.md](../SECURITY.md).

**The license is MIT** ([../LICENSE](../LICENSE)): fork it, rename it, put your company's field names in it, strip what you disagree with. The one thing worth preserving in a fork is the attribution line on each card and worksheet, because that is what lets the next reader check a method against its source rather than against your restatement of it.

---

## Reporting a problem, or contributing

Open an issue or a pull request, and read [../CONTRIBUTING.md](../CONTRIBUTING.md) first, since it names what gets accepted. Two contributions are worth more than the rest: a failure mode you have personally watched happen, with the tell that revealed it, and a skip condition for a method the tree currently teaches without one. Both are things a maintainer cannot invent honestly, and both make the tree smaller rather than larger. Run `python3 -m unittest test_lint` and `python3 lint.py --os` before you push.
