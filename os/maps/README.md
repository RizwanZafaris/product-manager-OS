---
layer: os
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Maps of content"]
---
# Maps of content

Six notes, one per stage of the loop in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Each one answers a single question: for this stage, what does the repository actually hold? The templates the stage owns, the worksheets its methods come from, the skills that drive it, the agents that lead it, and the gate it ends at with what that gate demands.

| Map | Stage | Gate it ends at |
|---|---|---|
| [discover.md](discover.md) | DISCOVER | Gate 1: problem worth solving |
| [define.md](define.md) | DEFINE | Gate 2: requirements signed off |
| [design.md](design.md) | DESIGN | Gate 3: architecture and risks reviewed |
| [build.md](build.md) | BUILD | Gate 4: acceptance criteria met |
| [deliver.md](deliver.md) | DELIVER | Gate 5: release readiness green |
| [operate.md](operate.md) | OPERATE | Gate 6: outcomes verified |

## Why these exist

The tree has more than two hundred files and they cross-reference each other densely, which is correct for reading and useless in a graph view. Opened in a vault with no hubs, this repository is a hairball: every node connects to several others, no cluster has a center, and the picture tells you nothing you did not already know.

A map of content fixes that with a cheap structural move borrowed from personal-knowledge-management practice, where the term comes from Nick Milo's Linking Your Thinking work (from 2017 onward). One note per stage becomes the center its cluster fans out from. The graph then shows six clusters, the layers colored inside them, and the loop's shape as edges between the hubs. Reading the file works too: a map note is a usable index of one stage even with the graph turned off.

## The two link forms, and why both

Each map carries the same set of pointers twice.

| Form | Where it sits | Who it is for |
|---|---|---|
| Relative markdown, for example `../../templates/definition/prd.md` | In the prose and the tables | Anyone reading on a code host, in an editor, or on disk. This is the load-bearing form, and lint resolves every one |
| Wikilinks, for example a double-bracketed vault path | In the closing graph-links section only | The Obsidian graph, which draws edges from wikilinks |

Wikilinks are additive. A code host renders them as literal brackets, so nothing a reader needs to click is ever wikilink-only. Vault paths inside them are repo-root relative and carry the `.md` extension, which resolves both in Obsidian and for a lint check that treats the target as a path.

## Maintenance

These notes are curated by hand. They are not generated, and no script keeps them in step with the tree.

- **When you add a template, worksheet, skill, or agent**, add it to the stage map that owns it, in both link forms. A file the maps never name is invisible in the graph view.
- **When you move or rename a file**, fix both forms. A stale wikilink shows up in Obsidian as an unresolved node and in the gate as a failed link check.
- **Keep the stage set at six.** The maps mirror the loop; if the loop ever changes shape, [OPERATING-LOOP.md](../OPERATING-LOOP.md) changes first and these follow.
- **Keep them thin.** A map note points; it never explains a method. The reasoning lives in [knowledge/README.md](../../knowledge/README.md), the procedure in [frameworks/README.md](../../frameworks/README.md), and the artifact in [templates/README.md](../../templates/README.md).
- **Curation, not coverage.** If a stage borrows a worksheet from another layer, name it where it is actually used rather than listing every file that could conceivably apply. A hub that lists everything is the hairball again, indented.

The vault settings that give the graph its colors are committed at [.obsidian/README.md](../../.obsidian/README.md). Deleting that directory changes nothing here: these six notes are plain markdown and read fine without it.
