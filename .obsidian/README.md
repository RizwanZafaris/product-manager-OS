# Committed vault config

This directory is an [Obsidian](https://obsidian.md) vault configuration, checked into the repository on purpose. Open the repository root as a vault and the graph view arrives already colored by layer, with the stage hubs in [os/maps/README.md](../os/maps/README.md) as its centers.

Three files, core only.

| File | What it sets |
|---|---|
| `app.json` | Editor and link defaults: wikilinks written as vault-root paths, links updated on rename, readable line length on |
| `appearance.json` | Base font size and the light default; no custom CSS theme |
| `graph.json` | The graph view, including the eight color groups below |

## The color groups

Each group is a search query over one layer of the tree, so a node's color tells you which layer it belongs to before you read its name. The layer stack itself is defined in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md), section 1.3.

| Query | Layer | Color |
|---|---|---|
| `path:os/` | The loop, the gates, and the stage hubs | Blue |
| `path:knowledge/` | Why a method exists and how it misleads | Purple |
| `path:frameworks/` | The worksheets you actually fill in | Teal |
| `path:templates/` | The artifact each stage owes its gate | Amber |
| `path:skills/` | Procedures a model or a person follows end to end | Green |
| `path:agents/` | Role instruction files and the team table | Red |
| `path:modules/` | The regulated overlay, hash-pinned and never edited | Magenta |
| `path:learn/` | Study paths, the library, and the tutor | Cyan |

Colors are stored the way Obsidian stores them, as one integer per group. Edit them in the app rather than by hand if you want different ones.

## What this is not

No community plugin is configured, required, or referenced. There is no folder-note plugin, no dataview, no templater: everything here is core Obsidian, so the vault opens clean on a fresh install with nothing to trust and nothing to install.

Nothing in the repository depends on this directory. Delete it and the content is unchanged: every map note and every template is plain markdown with relative links, and the wikilinks that feed the graph are additive on top. The two link forms are explained in [os/maps/README.md](../os/maps/README.md).

If you already use Obsidian and keep your own settings, this directory will collide with them for this vault only. Copy the color groups out of `graph.json` into your own graph settings and delete the rest if you prefer.
