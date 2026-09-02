# The OS: the loop in miniature

Six files. Together they answer the four questions that come before any template opens: what the stages are and what each gate demands, how much document this decision deserves, where the filled copies live, and how the interview runs if you want one.

One product runs through six stages, and each stage ends at a gate that must pass before the next one opens.

```
DISCOVER -> [Gate 1] -> DEFINE -> [Gate 2] -> DESIGN -> [Gate 3]
        -> BUILD    -> [Gate 4] -> DELIVER -> [Gate 5] -> OPERATE -> [Gate 6] -> loop
```

Gates are documents, not ceremonies. A gate passes when its checklist is filled in on evidence and signed by a named human, and a gate that cannot fail is a ceremony wearing a checklist. Gate 6 does not end the product; it decides whether the next pass through DISCOVER is a deepening, a pivot, or a sunset.

## The six files

| File | What it holds |
|---|---|
| [OPERATING-LOOP.md](OPERATING-LOOP.md) | The six stages, with entry, work, and exit for each; the three overlays (planning, AI, regulated); the six rules of the loop |
| [STAGE-GATES.md](STAGE-GATES.md) | The six gate checklists as fill-in forms, each with sign-off lines and a stated skip risk |
| [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md) | Three questions (stakes, audience, reversibility) that pick one of five artifact weights, plus a table for the documents that attach to a trigger rather than to a weight |
| [PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md) | The `products/<name>/` folder convention: where filled artifacts accumulate as the product's memory, and where STATE.md sits in the layout |
| [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md) | One fictional product taken through all six gates, naming every template used at each step |
| [CONDUCTOR.md](CONDUCTOR.md) | The normative interview protocol: the seven-rule contract, the challenge grammar, the gate procedure, the escape hatch, the resume rules |

## Read order for a first-timer

1. **[OPERATING-LOOP.md](OPERATING-LOOP.md).** Fifteen minutes, and everything else in the repository is downstream of it.
2. **[WHICH-DOCUMENT.md](WHICH-DOCUMENT.md).** Read it before you copy any template, or you will default to the heaviest artifact and then resent it.
3. **[STAGE-GATES.md](STAGE-GATES.md).** Skim your current stage's gate now rather than the day before you need it; the checklist is the specification for the work.
4. **[HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md).** The walkthrough that makes the first three concrete, with a filled counterpart in [examples/](../examples/README.md).
5. **[PRODUCT-WORKSPACE.md](PRODUCT-WORKSPACE.md).** Read it when you are about to write your first real artifact and need somewhere to put it.
6. **[CONDUCTOR.md](CONDUCTOR.md).** Read it only if you want the interview, or if you are debugging a runtime that is running one. Nothing above depends on it: every template here works with a pencil.

Then pick a template from [templates/](../templates/README.md) and take the filled copy to its gate.
