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

## Step 1: what the seat actually owns

**Read:** [Empowered product teams](../knowledge/cagan-product-teams.md), then [High Output Management](../knowledge/high-output-management.md). Between them: the PM owns problems and risk, and output is now the team's output, not yours. Melissa Perri's Escaping the Build Trap (see [the library](library.md)) is the long version of why this transition fails when it stays output-shaped.
**Study:** [WHICH-DOCUMENT](../os/WHICH-DOCUMENT.md), the weight tree. Your old role had one artifact form; this seat has a dozen, and choosing the weight is the first real decision.
**Do:** in PROGRESS.md, write a two-column mapping: five artifacts from your current role on the left, the nearest PM artifact from this repository on the right, with one line each on what changes in the translation.
**Done when:** at least one row honestly says "nothing maps; this is new", because pretending everything transfers is the first trap of the transition.

## Step 2: evidence, the unit of the job

**Read:** the Mom Test entry in the [knowledge index](../knowledge/INDEX.md): past behavior over opinions, always. Then the evidence ladder in [the bank format](../skills/conductor/questions/README.md).
**Study:** [the evidence note](../templates/discovery/evidence-note.md).
**Do:** write three evidence notes for Restow: one from an invented support-ticket export, one from an invented customer interview, one from an invented analytics query. Each gets a claim, a load-bearing detail, a source ID, a date, and a confidence label; place each on the evidence ladder.
**Done when:** the three notes sit on three different ladder rungs and you can say, per note, what the Conductor's challenge grammar would attack first.

## Step 3: research you can defend

**Read:** [Continuous discovery](../knowledge/torres-continuous-discovery.md).
**Study:** [the user research plan](../templates/discovery/user-research-plan.md).
**Do:** fill the plan for one Restow research question: why do customers abandon a started return? Write the screener, five interview questions that ask about past behavior only, and the synthesis themes you expect to be wrong about.
**Done when:** none of your five questions can be answered with a compliment, and the plan names the decision the research will inform.

## Step 4: the PRD, written backwards

**Read:** [Amazon PR/FAQ](../knowledge/amazon-pr-faq.md). Working backwards is the antidote to the builder's instinct of starting from the system you already see in your head.
**Study:** [the PRD](../templates/definition/prd.md), delete-unused-sections rule first.
**Do:** write the internal FAQ's three hardest questions for Restow in PROGRESS.md, answer them, and then fill the PRD. Scope one release: label printing and pickup scheduling in, instant refunds out, with the why written down.
**Done when:** the PRD's out-of-scope section is as convincing as its scope, every success metric has an invented baseline and target, and nothing in it describes implementation your old self would have reached for.

## Step 5: acceptance criteria and edges, your unfair advantage

**Read:** the premortem entry in the [knowledge index](../knowledge/INDEX.md); you are about to run one in miniature against your own spec.
**Study:** [acceptance criteria](../templates/definition/acceptance-criteria.md) and [edge cases](../templates/delivery/edge-cases.md).
**Do:** write given-when-then criteria for the return-label flow, then the edge-case table: the damaged item, the return window expiring mid-flow, the order paid with a gift card, the customer with no printer. Your technical instincts are an advantage here; spend them on behavior, not architecture.
**Done when:** every edge case has an expected behavior rather than "handle gracefully", and at least three criteria are negative cases, because the flow that only works when everything works does not work.

## Step 6: stakeholders and decisions, the political ledger

**Read:** [High Output Management](../knowledge/high-output-management.md) again, the leverage lens this time: meetings and decisions are your new codebase.
**Study:** [the stakeholder map](../templates/execution/stakeholder-map.md) and [the decision log](../templates/execution/decision-log.md).
**Do:** map Restow's six invented stakeholders (operations lead, warehouse manager, finance controller, support lead, engineering lead, legal counsel) with interest, influence, and concerns. Then write two decision-log entries: one decision that went your way, one that did not and that you are recording honestly anyway.
**Done when:** the map contains at least one stakeholder whose interests genuinely conflict with the product's, and the lost decision reads as a record, not a grievance.

## Step 7: outcomes over output

**Read:** [OKRs](../knowledge/okrs.md). The trap, key results that are tasks, is precisely the transition trap: a builder's KR says "ship the portal", a PM's says what changes because it shipped.
**Study:** [the OKR template](../templates/planning/okrs.md).
**Do:** write one objective and three key results for Restow's first quarter live. Every KR gets an invented baseline, a target, and a source system. Then rewrite your own first instinct: take the most task-shaped KR you drafted and turn it into an outcome.
**Done when:** no key result contains a verb of building, and each one would still be scoreable if the team shipped nothing.

## Capstone: Gate 2, scored

Run the tutor ([skills/tutor/SKILL.md](skills/tutor/SKILL.md)) over your Restow definition set. The tutor drills from the DEFINE bank ([the questions](../skills/conductor/questions/define.md)), critiques the PRD against its exit gate line by line, pushes once per weak answer, and scores.

**Done when:** every Gate 2 line scores 2, including the weight question: be ready to defend why Restow got a PRD and not a one-pager, or concede the point and cut it down, which is also a pass. Pencil users: self-grade against the bank's Accept-when lines.

Next: [Senior sharpening](path-senior.md) once you have shipped something real through a gate, or the [library](library.md) for the long versions of what transferred least comfortably.
