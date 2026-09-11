---
layer: knowledge
stage: DESIGN
gate: 3
feeds: ["templates/execution/dependency-register.md", "frameworks/design/design-system-audit.md", "frameworks/strategy/build-buy-partner.md"]
method: ""
aliases: ["UI Dependency Licensing", "ui-dependency-licensing"]
---
# UI Dependency Licensing

Based on the licence files of usablica/intro.js (commit e5517e6), wasabeef/awesome-android-ui (commit 312f9be), open-webui/open-webui (commit 0a7c158), and akiraux/Akira (commit a70cc8f), read alongside the GNU Affero General Public License v3.0 text and the Elastic UI and Penpot rows already registered in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md). Explained here in this repository's own words. This card is not legal advice, and no ruling in it should be treated as one.

## The essence

Choosing a UI library or a component is an experience design decision the moment a licence attaches to it, because the terms decide what your product is allowed to become, not just what it looks like. A product manager who treats the licence field as a formality signed by whoever set up the repository is the same manager who discovers, a release later, that the tour library wired into forty screens cannot be shipped closed source without either paying a vendor or rewriting all forty. The point of this card is not to answer whether a given library is safe to use. It is to teach a product manager which questions the licence text actually raises, so the ones with real teeth reach legal before code, budget, or a launch date makes the honest answer expensive to hear.

The habit this card asks for is small and specific: read the licence file the project itself ships, in the exact version and the exact path you plan to ship, and write down what it actually says before writing down what a README or a sales page says it means. Everything below is a worked demonstration of that habit against real, dated repositories, not a ruling on any of them.

## Where it came from

This card was built by studying licence files directly, the way [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md) instructs every design-layer source to be read: the file itself, never a shields.io badge or a README's summary of it. Four repositories carry the specific lessons. usablica/intro.js, an onboarding-tour library, was read for its dual-licensing structure. wasabeef/awesome-android-ui, a curated catalogue of Android UI libraries, was read for what a permissively licensed list actually covers. open-webui/open-webui, a self-hostable AI chat interface, was read for a branding clause layered on top of a permissive core. akiraux/Akira, an early-stage open source design tool, was read for a licence claim its own repository does not support. Two more sources already in this repository's register round out the classes these four do not cover on their own: Penpot (MPL-2.0, a file-level copyleft) and Elastic UI (SSPL or Elastic License 2.0, source-available rather than open source).

## When to use it

- A UI library, component kit, icon set, or onboarding-tour tool is proposed for the build, and nobody on the team has read its licence file yet.
- A design-system audit finds a component whose upstream project changed its licence, its major version, or its branding terms since it was first adopted.
- A team wants to fork, white-label, or self-host an open source product and is not sure whether the result can be sold, rebranded, or kept closed.
- [Build, buy, partner, or wait](../../frameworks/strategy/build-buy-partner.md) is being scored for a component, and the control and exit-cost criteria need the licence's actual obligations rather than a guess.
- A curated "awesome" list or a marketplace page is the only evidence anyone has gathered for a dependency's terms.

**Skip it when:** the dependency is already logged on the [dependency register](../../templates/execution/dependency-register.md) with a licence read from its own licence file, at the version actually shipping, and no major upgrade or deployment change has happened since. Re-reading a licence that has not moved is process for its own sake; the trigger below names exactly when to come back.

## Licence classes, plainly stated

None of this is a legal definition. It is the shape of what each class asks of a product team, so a name in a dependency scan reads as a real question rather than a colour on a badge.

- **Permissive** (MIT, BSD, Apache 2.0). Use, modify, and redistribute almost freely, including inside closed-source and commercial products, as long as the copyright notice and licence text travel with any substantial copy. This is the largest class in this repository's own register: shadcn/ui, Chakra UI, Material UI, daisyUI, Semantic UI, GitHub Primer, and the code (not always the docs) behind GOV.UK and USWDS all fall here.
- **File-level copyleft** (Mozilla Public License 2.0). A file you modify and distribute stays under MPL, but MPL allows combining that file with differently licensed code into a larger work, so an unmodified MPL dependency sitting beside your own MIT-licensed code does not pull your code under MPL. Penpot is this register's example, already recorded as paraphrase-with-attribution, never adapt its file text verbatim.
- **Strong copyleft** (GPL-3.0 and similar). A work that incorporates GPL code, rather than merely calling it as a separate program, becomes a combined work that must itself be distributed under the GPL if you distribute it at all. Akira, below, is this register's example, and it is recorded as never adapted or reused for exactly this reason.
- **Network copyleft** (AGPL-3.0). Everything GPL requires, plus one extension: modifying the program and then letting users interact with it over a network can trigger the same source-sharing obligation that GPL only triggers on distribution. intro.js, below, ships under this class by default.
- **Source-available** (SSPL v1, Elastic License 2.0, and similar). The code sits in a public repository and reads like an open licence, but the licence is not OSI-approved open source: it typically restricts offering the software as a hosted service. Elastic UI is dual-licensed this way and is recorded in this repository's register as never reused, because both licences carry terms this repository will not take on for adapted or paraphrased text.
- **Dual or commercial.** A project offers the copyleft terms for free and a separate paid licence that removes the copyleft obligation. intro.js again: AGPL or a purchased commercial licence, and the two are not equivalent in what they cost you.

## The intro.js case: two framings of the same clause

intro.js's own license.md states the licence as AGPL-3.0 or a paid commercial licence, with one stated carve-out: versions before v2.0.0 need no commercial licence at all, meaning the terms themselves changed at a named major version. Inside the same repository, the example/bootstrap/v3 subdirectory carries its own separate MIT licence, unrelated to the library it demonstrates. Two lessons follow directly, and neither depends on which side of the AGPL question your company lands on. First, a single "the project is licensed X" line is never the whole story once a project's history spans a licence change; the version you actually pin matters as much as the project name. Second, a licence can vary by path inside one repository, so "we use intro.js" is not yet a complete sentence.

The README and the licence file also frame the same clause differently, and the gap between the two framings is the more consequential lesson. intro.js's own license.md says a commercial project "would need" a commercial licence. That is the vendor's sales framing. The AGPL's own text permits commercial use outright, provided its source-sharing obligations are met; buying the commercial licence is what a team chooses when meeting those obligations costs more than the purchase price, not a requirement the AGPL itself imposes. Reading the vendor's summary in place of the licence text is how a team either overpays for a licence it did not need, or underestimates one it did.

The AGPL's own extension over GPL, its section 13, applies to a modified version of the program that users interact with remotely over a network. A UI library is not run on a server the way a backend service is; it is JavaScript delivered to and executed inside a user's own browser. Whether that delivery counts as the network interaction section 13 was written for, and whether an unmodified copy of the library even reaches section 13 at all, is precisely the kind of question this card hands to counsel rather than answers. Framing it as settled either way, in either direction, is the mistake this card exists to prevent.

## A list's licence is not its entries' licence

wasabeef/awesome-android-ui is itself MIT licensed: the categories, the entry names, and the short descriptions that make up the list can be paraphrased or adapted with the MIT notice kept, exactly as the list's own copyright permits. None of that extends to what the list links to. Its more than three hundred entries carry their own licences, the large majority permissive (Apache 2.0, MIT, BSD-2, ISC) but including at least two under GPL-3.0 and several with no licence found at all. A team that reads "the list is MIT" and treats every library it links as cleared has confused the wrapper for the contents. Every entry needs its own licence read, at the version actually pulled in, exactly like any other dependency.

## Branding clauses: a second axis of restriction

open-webui/open-webui's licence is not one thing across its history. Code committed before commit a76068d is MIT. Code between a76068d and 60d84a3 is BSD-3-Clause. Code after 60d84a3 carries the project's own Open WebUI License, which layers a fourth clause onto a BSD-3-Clause base: the project's branding, meaning its name, logo, and other visual or textual identifiers, must stay visible and unaltered in any deployment or distribution. That clause names exactly three exceptions: no more than 50 end users inside any rolling 30-day window, prior written permission from the project, or a paid enterprise licence. A fork or a self-hosted deployment that removes or replaces the branding outside those three exceptions is a material breach of the licence, whatever the rest of the code's history says. A team that forks from a commit before 60d84a3 keeps BSD-3-Clause and escapes the branding clause entirely, at the cost of every feature the project has added since. Contributing changes back upstream carries a separate obligation again: the project's contributor agreement grants it a perpetual right to relicense that contribution commercially on its own terms.

The number 50 above is not a benchmark this card is asserting; it is the literal threshold written into the licence's own fourth clause, current to the commit read (0a7c158, read 2026-09-10). A licence-derived number like this one is a fact about the text, not a claim requiring separate evidence the way a usability statistic would, but it is exactly the kind of term a live user count can quietly cross without anyone on the product side noticing, which is why the trap below treats a branding threshold as a recheck trigger rather than a one-time fact.

## Source-available is not open source: Elastic UI

Elastic UI defaults to a dual licence of SSPL v1 or Elastic License 2.0, neither of which is an OSI-approved open source licence, even though the code sits in a public GitHub repository with a permissive-looking README. Source-available licences of this kind typically restrict offering the software itself as a competing hosted service, among other terms. This repository's own design-layer register already excludes Elastic UI from any reuse for exactly this reason: a public repository is evidence that the code is visible, never evidence that its licence permits what a permissive or even a standard copyleft licence would. The two questions, "can I read this code" and "what does its licence let me do with it," have different answers here, and a component scan that only checks whether a repository is public will miss the difference every time.

## Read the licence file, not the README

akiraux/Akira's README states its licence as "GNU GPLv3 / Creative Commons BY-SA." Its repository's own COPYING file contains the complete GPLv3 text and nothing else; no Creative Commons text exists anywhere in the tree. The README's claim is simply not supported by the document that actually grants rights. This is the cleanest example in this card of the discipline every other section depends on: the operative document is the file named COPYING, LICENSE, LICENSE_NOTICE, or the equivalent the project itself ships, or for a hosted service its published terms page, never a summary line written for humans skimming a repository page. A mismatch like Akira's is not rare enough to assume away.

## Four options once the terms are known

Once a dependency's actual licence, version, and path are read, a product team has four moves, and choosing among them is a product decision, not an engineering default.

- **Comply.** Meet the licence's stated obligations, whether that is keeping a notice, sharing modifications, or sharing the whole combined work's source, and confirm with legal that the obligation as read is one the product can actually meet.
- **Buy.** Purchase the commercial or enterprise licence a dual-licensed project offers, when meeting the free tier's obligations costs the business more than the purchase does.
- **Choose a permissive alternative.** Swap in a component under a licence class the product can use freely, before the dependency is wired into markup, data flows, or a design system's own token contracts, since unwinding it afterward costs far more than the swap would have.
- **Build.** Write the component internally when none of the above clears at an acceptable cost, feeding the same [build-buy-partner](../../frameworks/strategy/build-buy-partner.md) worksheet this card's licence read is meant to supply real numbers to.

The cost of switching later is not hypothetical. A tour library like intro.js is wired directly into markup, step by step, screen by screen; discovering a licence problem after that wiring is done means paying twice, once for the original build and again for the rebuild.

## Questions for legal

This card hands legal a list of questions, never a conclusion. None of the following has a settled answer here.

- Given our actual deployment shape (server-rendered page, single-page app, embedded widget, or something else), does shipping this library's JavaScript to a user's browser count as the kind of network interaction AGPL section 13 addresses?
- Are we shipping the library unmodified, or have we changed its source, and does that change the answer?
- Does our product and this dependency form a single combined work under the licence's own terms, or can the two be treated as merely aggregated, separately licensed programs?
- Which exact commit and which exact path inside the repository are we shipping, and does a carve-out (a pre-major-version exemption, a separately licensed subdirectory) apply to that specific path?
- If we take the vendor's commercial or enterprise licence instead, what precisely does it cover: which repositories, which versions, how many seats, deployments, or end users?
- If a branding or attribution clause applies, does our current or projected user count cross its stated threshold, and on what cadence should we recheck a number that can move without a code change?
- If contributing a fix upstream requires signing a contributor agreement, what rights does that agreement grant the project over our contribution, and are we comfortable granting them?
- What event should trigger a re-read of this dependency's licence: a major version bump, a fork, a new deployment shape, a user count crossing a stated threshold, or something else specific to this component?

## The trap: the licence checked once at selection and never on major upgrade

A licence read at intake and logged once reads like a closed question, and treating it as permanently closed is the trap. It is not permanently closed, because the terms themselves can move without the dependency's name changing at all. intro.js's obligations differ before and after v2.0.0. Open WebUI's licence differs across three separate commit ranges within its own history, and its branding clause depends on a live user count that can cross the stated threshold on its own, with no code change and no new commit to prompt a re-check. A dependency register entry that says "MIT, cleared" and is never revisited is a snapshot mistaken for a fact. The fix this card asks for is not more frequent auditing in general; it is a named recheck trigger attached to the specific things that actually move a licence's terms for that dependency: a major version upgrade, a fork, a change in how the product is deployed or distributed, or, where a licence names one, a user-count threshold. [Dependency Register](../../templates/execution/dependency-register.md) is where that trigger gets written down and owned, not carried in anyone's memory of what was true at intake.

## How it lies: a licence badge read instead of the licence file

The most convincing failure mode in this whole card is Akira's: a README states a licence with confidence, a badge on a repository page implies one, and neither is the document that actually grants any rights. A reader who stops at the badge walks away believing something the project's own COPYING file does not say. The same failure appears in softer form in intro.js's license.md, whose own prose tells a commercial team it "would need" a paid licence, a sales framing that reads as settled fact unless the AGPL's actual text is read beside it. A licence badge, a README summary, or a vendor's own explanation of its licence is marketing or communication written for humans skimming quickly. It is never the operative document, and treating it as one is how a team ships a licence violation, or pays for a licence it never needed, while believing the question was already answered.

## Where it sits in the loop

- Stage: DESIGN, at the point a UI library, component kit, or design-system dependency first enters the build; revisited at BUILD when the actual version is pinned, and again at every event named by the trap's recheck trigger.
- Upstream: [Build, buy, partner, or wait](../../frameworks/strategy/build-buy-partner.md) already scores a component's control and exit cost generically; this card supplies the licence-specific facts that scoring needs rather than a guess.
- Downstream: the dependency's licence class, its stated obligations, and its recheck trigger are logged on the [Dependency Register](../../templates/execution/dependency-register.md); [Design system audit](../../frameworks/design/design-system-audit.md) checks, on its own cadence, whether an adopted component's cleared terms still hold as the design system and its dependencies both keep moving.
- On trial at: [Gate 3: Architecture and risks reviewed](../../os/STAGE-GATES.md#gate-3-architecture-and-risks-reviewed), through the dependency register's own checklist line that every integration names its owner and its terms; and again, informally, at any later major upgrade this card's trap names as a recheck trigger.

## Used by

- [Dependency Register](../../templates/execution/dependency-register.md), where a dependency's licence class, obligations, and recheck trigger are logged and owned on a weekly cadence.
- [Design system audit](../../frameworks/design/design-system-audit.md), which checks an adopted component's licence terms against what was cleared at intake as the design system evolves.
- [Build, buy, partner, or wait](../../frameworks/strategy/build-buy-partner.md), whose control and exit-cost criteria this card supplies real licence facts to, in place of a guess.

## Reading

Reuse classes below are registered in [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md); this card follows that register. Read 2026-09-10.

- [usablica/intro.js](https://github.com/usablica/intro.js), commit e5517e6. Dual-licensed: AGPL-3.0 or a paid commercial licence for the project as a whole from v2.0.0 onward; versions before v2.0.0 need no commercial licence; the example/bootstrap/v3 subdirectory carries its own separate MIT licence. Reuse class: cite only; never adapt or paraphrase the licensed prose or code.
- [wasabeef/awesome-android-ui](https://github.com/wasabeef/awesome-android-ui), commit 312f9be. MIT for the list's own text; the more than three hundred libraries it links keep their own licences, including at least two under GPL-3.0 and several with no licence found. Reuse class: cite only.
- [open-webui/open-webui](https://github.com/open-webui/open-webui), commit 0a7c158. Split by history: commits before a76068d are MIT, a76068d through 60d84a3 are BSD-3-Clause, and the current Open WebUI License layers a branding clause onto a BSD-3-Clause base for everything after. Reuse class: paraphrase only, no branding element carried over, no claim of endorsement by the project.
- [akiraux/Akira](https://github.com/akiraux/Akira), commit a70cc8f. GPL-3.0, per the repository's own COPYING file; the README's separate claim of a Creative Commons BY-SA licence has no supporting text anywhere in the tree. Reuse class: never; nothing is adapted from this repository, and it is cited here only as the licence-hygiene lesson its own README and COPYING files disagree.
- [elastic/eui](https://github.com/elastic/eui). Dual licence, SSPL v1 or Elastic License 2.0, source-available rather than an OSI-approved open source licence. Reuse class: never; excluded from the design layer entirely, per this repository's own register.
- [penpot/penpot](https://github.com/penpot/penpot), commit 37dab75, cited here as this card's file-level copyleft example. MPL-2.0 at the repository root. Reuse class: paraphrase with attribution; never adapt file text verbatim.
- [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html), Free Software Foundation. Not a design-layer study source; linked here directly for its own canonical text rather than paraphrased, since the licence's own terms permit copying its text verbatim but never altered. Reuse class: link only.
