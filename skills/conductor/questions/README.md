# Question Banks: format and rules

One bank per stage, six banks. Each bank is the normative question set the Conductor runs for that stage, in ID order, under the contract in [../../../os/CONDUCTOR.md](../../../os/CONDUCTOR.md). Banks are data for the interviewer, not prose for the user: the Conductor renders each entry into the four-part question anatomy at ask time, drafting the lettered options from the product's own context unless the entry fixes them.

## Entry format

Every question is one entry with exactly these fields:

```
### <STAGE>-<n>: <handle, three words or fewer>

Ask: <the question, one interrogative sentence, asked as written>
Wrong costs: <one line: the downstream damage of a bad answer here>
Evidence class: <minimum class from the ladder below>
Cross-examine when: <the answer pattern that fires a push> Move: <the grammar move to apply>.
Accept when: <the test an answer must pass, checkable in one read>
Lands in: <workspace-relative path plus section> and STATE.md accepted answers
```

Optional fields, used where they earn their place:

- `Options:` fixed lettered options, only when the choice set is stable across products (stakes, weights, persist-pivot-sunset). Everywhere else options are drafted at runtime and must differ in consequence.
- `Applies:` the knowledge card or skill the question operationalizes, linked, because the Conductor names the framework it is applying and why, every time it applies one.
- `Follow-up on strength:` the harder question a strong answer earns immediately.

## Bank file structure

Each bank opens with a header block: the stage, the gate it feeds, the working skills and agents the Conductor hands off to, and the overlays that can attach. Each bank closes with two sections:

1. **Forced pair.** The two highest-stakes questions for the escape hatch in [../../../os/CONDUCTOR.md](../../../os/CONDUCTOR.md). When a user says "advance anyway", these are forced first, in the order listed.
2. **Gate rendering.** A table mapping every checklist line of the stage's gate in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md) to the bank IDs whose accepted answers evidence it. This is the exit-gate test: a gate line with no accepted, landed answer behind it is marked unknown, and an unknown blocks exactly as a fail does.

## The evidence ladder

Strongest first. Every `Evidence class` field names its minimum from this list.

1. **Observed behavior**: something a user did, with a date and a place it is recorded.
2. **Artifact**: a document, dataset, ticket, or export a reader could open.
3. **Named commitment**: a person with standing said yes in writing.
4. **Interview claim**: a real person said it, cited by source and date.
5. **Team belief**: goes to the assumptions register, never into a template as fact.

## Rules

- IDs are stable. `Next question` in STATE.md points at an ID; renumbering breaks every resumed journey. New questions append, they do not insert.
- The `Ask` sentence is asked as written. The Conductor may add product context around it, never soften it.
- One entry, one question. An entry that needs "and" in its Ask line is two entries.
- `Lands in` paths are workspace-relative per [../../../os/PRODUCT-WORKSPACE.md](../../../os/PRODUCT-WORKSPACE.md): the filled copy, never the blank under `templates/`.
- A bank edit is a repo change: run `python3 lint.py --os` and check the gate-rendering table still covers every checklist line.
