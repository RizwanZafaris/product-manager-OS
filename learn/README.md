# Learn: the study layer

The rest of this repository assumes you are running a real product. This layer assumes you are not, yet. It teaches the OS the only way a document system can be taught: by making you fill it in, on products that are safely fictional, with a tutor that critiques your work the way the Conductor would cross-examine it.

Learning mode depends downward only: on [knowledge/](../knowledge/README.md), on [templates/](../templates/README.md), on the loop files in [os/](../os/OPERATING-LOOP.md), and on the Conductor's question banks, all read-only. Nothing outside `learn/` knows this layer exists. Delete the folder and the OS loses nothing but the curriculum.

## Pick your path

| Path | You are | Steps | Fictional product | Capstone gate |
|---|---|---|---|---|
| [Foundations](path-foundations.md) | New to product management, or want one structured pass through the basics | 6 + capstone | Streakline, a mobile habit tracker | Gate 1: problem worth solving |
| [Transitioning](path-transitioning.md) | Moving into a PM seat from engineering, design, data, delivery, or support | 7 + capstone | Restow, a returns portal for a furniture retailer | Gate 2: requirements signed off |
| [Senior sharpening](path-senior.md) | A practicing PM or Director sharpening strategy, GTM, growth, and the honest ending | 6 + capstone | Meterly, usage metering for a developer API platform | Gate 6: outcomes verified, learn or sunset |

Paths are sequences, not menus: each step builds on the artifacts of the last, because that is how the loop itself works. A step you can already pass is still worth the hour; write the exercise anyway and let the tutor find out.

## How a step works

Every step in every path has the same four parts:

1. **Read** one knowledge card. The card is the why; it names the originator and the trap.
2. **Study** one template or OS file. Read the guidance comments, not just the fields; the comments are where the repo argues with you.
3. **Do** the exercise: fill the template, or a named section of it, for the path's fictional product. Invented evidence is allowed and must be labeled invented; what is graded is whether it has the right shape and class, not whether it is true.
4. **Done when** names the checkable test. It mirrors the template's own exit gate. An unchecked box is a reason to redo the exercise, not a formality.

## The checkbox ledger

Each path opens with a ledger block: one markdown checkbox per step. Copy that block into `learn/products/<product>/PROGRESS.md` and check boxes there, never in the path file itself. Paths stay blank for the same reason templates stay blank: the next learner starts clean. The convention is defined in [products/README.md](products/README.md).

## Tutor mode

Say "teach me", "quiz me", or "tutor" and the runtime loads [skills/tutor/SKILL.md](skills/tutor/SKILL.md). The tutor reuses the Conductor's question machinery in a teaching posture: it asks from the real stage banks, judges your answer against the real evidence ladder, pushes once with the challenge grammar, then shows a model answer and scores you. It critiques filled exercises line by line against the template's exit gate, citing the knowledge card behind each critique. It never touches a real product workspace.

No AI runtime, no problem: every path works with a pencil. Self-interview from the bank files, grade yourself against the Done-when lines, and use the [library](library.md) when a card is not enough.

## What this layer is not

- Not a course. There is no video, no certificate, no cohort. The curriculum is the repo's own files in a deliberate order.
- Not a source of evidence. Nothing produced in `learn/products/` may ever be cited in a real workspace; practice artifacts are labeled practice and stay here.
- Not a second canon. When a path disagrees with a knowledge card or an OS file, the card or the OS file wins; fix the path.

## Where things are

- [library.md](library.md): the books and podcasts behind the cards, attributed, in this repo's own words.
- [products/README.md](products/README.md): the practice workspace convention.
- [skills/tutor/SKILL.md](skills/tutor/SKILL.md): the tutor, and the exact scoring scale.
- [../os/CONDUCTOR.md](../os/CONDUCTOR.md): the interrogation the tutor is training you to survive.
