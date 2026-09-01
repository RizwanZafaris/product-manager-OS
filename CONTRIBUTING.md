# Contributing

Issues and pull requests are welcome. The maintainer merges everything personally, so small and specific beats large and sweeping.

## What makes a contribution mergeable

- **Templates**: a new template needs a real problem statement in the PR description, fill-in fields with in-template guidance, and an exit gate at the bottom. Follow the voice of the existing files.
- **Knowledge cards**: framework essence in your own words with a named attribution line. Book text is never reproduced here; one quote under 15 words with attribution is the ceiling.
- **Skills and agents**: follow the two-field frontmatter convention in `skills/`. A skill that needs a specific vendor or paid tool to work will not be merged.
- **Claims**: any factual claim carries a public source. Unsourced numbers are removed on sight.

## Stability policy

Template field names and file paths are stable within a major version. Renames and removals happen only at a major version bump, with the old path noted in the changelog.

## What will not be merged

Portfolio and case-study templates, course content, tool integrations that require accounts, paid tiers, and anything reproducing licensed material. See `docs/ARCHITECTURE.md` for scope.
