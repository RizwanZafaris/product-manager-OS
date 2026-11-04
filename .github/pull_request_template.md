## What this changes

<!-- One or two sentences. Name the files and the stage or gate they touch. -->

## Why

<!-- The real problem this solves. For a new template, framework, skill or knowledge card, the situation a working PM is in when they reach for it. Link the issue if there is one. -->

## Evidence and sources

<!-- Every factual claim carries a public source. Unsourced numbers are removed on sight. Write "none" if the change makes no factual claim. -->

## Checklist

- [ ] `python3 tools/ci_gate.py` passes locally, and I have pasted its last line below
- [ ] New or changed templates keep their Stage, Knowledge and Skill header and end at an exit gate
- [ ] New or moved files are in the graph: `python3 tools/graph.py` was rerun, and `docs/GRAPH.md` was not hand-edited
- [ ] No reproduced book text; at most one quote under 15 words, attributed
- [ ] Nothing under `modules/regulated/` was edited
- [ ] If this changes a template field name or a file path that other files link to, the CHANGELOG names the migration

```text
paste the last line of tools/ci_gate.py here
```
