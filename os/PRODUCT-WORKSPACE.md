# The Product Workspace

Templates are blanks. A product is the filled copies of them, accumulated over a year, and that pile is the only memory the next PM will have. This file defines where the pile lives and what it is called, so that "what did we decide about refunds" is a file path rather than an archaeology project.

The convention is a folder. That is the whole mechanism, and it is deliberate: the answer to a memory problem in a document system is a place to put documents, not a database.

## The layout

One folder per product, named for the product, holding one subfolder per stage of the loop:

```
products/
└── ledgerline/
    ├── README.md              what this product is, one paragraph, plus the current stage and gate
    ├── discovery/             filled copies of templates/discovery/
    ├── definition/            filled copies of templates/definition/
    ├── architecture/          filled copies of templates/architecture/
    ├── execution/             decision log, risk register, stakeholder map, dependency register
    ├── delivery/              filled copies of templates/delivery/
    ├── operate/               filled copies of templates/operate/
    ├── planning/              this product's roadmap and OKR copies
    └── gates/                 one file per gate attempt, copied from os/STAGE-GATES.md
```

Where the folder sits is your choice. Three arrangements work, and only the third needs a rule:

1. **Its own repository**, with this one cloned alongside as reference. The cleanest option for a team.
2. **Inside your product's existing repository**, next to the code the documents describe.
3. **Inside a clone of this repository.** Allowed, and the reason `products/` is the reserved name: nothing in this repository will ever ship a directory by that name, so your work cannot collide with an update. Add `products/` to `.gitignore` if the contents are private and the clone is not.

## The four rules that make it memory rather than storage

1. **Filled copies, never edits to the originals.** Copy the template out, fill the copy. `templates/` stays blank so the next product starts clean. This is the same rule the agent files state and the reason for it is the same.
2. **Keep the file name of the template you copied.** A filled PRD is `definition/prd.md`, not `PRD_v3_final_FINAL.md`. Versions are the file's history, not its name. When one product genuinely needs two of something, the suffix names the thing, not the version: `architecture/adr-004-precompute-explanations.md`.
3. **Three files never get archived, whatever the stage.** The decision log, the risk register, and the assumptions register run the length of the product. Everything else is written at a stage and read afterward; these three are written continuously and are the first things a new owner reads.
4. **Gate attempts are kept, including the failures.** `gates/gate-2-attempt-1.md` is more useful than `gates/gate-2.md`, because the attempt that was returned records what the team did not know at the time. A gate history with no failures in it is either a very lucky product or a rewritten one.

## The product README is the index

One paragraph on what the product is, then a short table: current stage, last gate passed and when, next gate and what it is waiting on, and the owner. Update it at each gate, which is six edits a year, not a maintenance burden.

This is what an AI runtime reads first when you point it at a product. It is also what a new PM reads first, which is the same requirement.

## What this convention is deliberately not

It is not a knowledge graph, an index service, or a database. Those were considered and rejected for the first version, because a document system whose memory needs software has stopped working with a pencil, and because the failure mode of index infrastructure is a stale index that lies with confidence. A folder cannot go stale in a way that hides from you.

It is also not a replacement for the canon layer. `knowledge/` holds methods that are true across products, with named attribution. `products/<name>/` holds what happened to one product. The two never merge: a lesson from one product graduates into the canon only when it stops being about that product, and it arrives with an attribution like everything else in that directory.

## How the loop uses it

[OPERATING-LOOP.md](OPERATING-LOOP.md) says which template a stage produces. This file says where it lands. [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md) walks one product through all six stages and every artifact it names ends up in one of the folders above. [WHICH-DOCUMENT.md](WHICH-DOCUMENT.md) decides how heavy each of those artifacts should be before you copy it out.
