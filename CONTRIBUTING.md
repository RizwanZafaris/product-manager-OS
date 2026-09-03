# Contributing

Issues and pull requests are welcome. The maintainer merges everything personally, so small and specific beats large and sweeping.

## What makes a contribution mergeable

- **Templates**: a new template needs a real problem statement in the PR description, fill-in fields with in-template guidance, and an exit gate at the bottom. Follow the voice of the existing files.
- **Knowledge cards**: framework essence in your own words with a named attribution line. Book text is never reproduced here; one quote under 15 words with attribution is the ceiling.
- **Skills and agents**: follow the two-field frontmatter convention in `skills/`. A skill that needs a specific vendor or paid tool to work will not be merged.
- **Claims**: any factual claim carries a public source. Unsourced numbers are removed on sight.
- **Failure modes and skip conditions**: worth more than the rest, because neither can be invented honestly. A failure mode is mergeable when it arrives with the tell that reveals it, since a named defect nobody can detect is trivia. A skip condition is mergeable when it tests the situation rather than your appetite: "the list is under five items and the first two are obvious" is checkable by someone else in the room, and "we do not have time" is a schedule.
- **Disproving a gap claim**: the four claims in [docs/COMPARISON.md](docs/COMPARISON.md) are written to be falsifiable, each with what would disprove it. An issue that disproves one is a good issue, and the correct response is to narrow the claim rather than defend it.

Before arguing that a rule here is wrong, read the counter-argument already written against it in [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md). Nine beliefs are stated there with the strongest case against each, so the PRs that land tend to be the ones that beat a counter-argument rather than the ones that rediscover it.

## Stability policy

Template field names and file paths are stable within a major version. Renames and removals happen only at a major version bump, with the old path noted in the changelog.

## What will not be merged

Portfolio and case-study templates, course content, tool integrations that require accounts, paid tiers, and anything reproducing licensed material. See `docs/ARCHITECTURE.md` for scope.
