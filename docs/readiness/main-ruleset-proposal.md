# Main branch ruleset proposal

Stage: ALL STAGES, applies before any merge into `main`
Knowledge: [external gates](external-gates.json), EXT-CI and EXT-TEAM
Skill: none. This is a proposal for the repository administrator, not a procedure for a runtime

<!-- P0 item 7 of the release contract asked for a ruleset built from the
     check names the hosted workflow actually reports, with maintainer
     approval requested before anything administrative changes. This file is
     that request. Nothing here is applied by any tool in the tree; the
     administrator applies it, or declines it, by hand. -->

## What was observed

Measured on 2026-09-09 against commit `df466083117cfe0d8131df92d54609295367b31d`,
the head of `main` at the time:

| Fact | Observed value | How it was observed |
|---|---|---|
| Branch protection on `main` | none (`Branch not protected`, HTTP 404) | `gh api repos/RizwanZafaris/product-manager-OS/branches/main/protection` |
| Repository rulesets | 0 | `gh api repos/RizwanZafaris/product-manager-OS/rulesets` |
| Hosted workflow | `lint` (`.github/workflows/lint.yml`), on `push` and `pull_request` | the workflow file |
| Job names the workflow reports | `gate (3.11)`, `gate (3.13)`, `deletable-harness` | `gh run view 34254784876 --json jobs` |
| Status of those jobs on `main` | `gate (3.11)` failure, `gate (3.13)` failure, `deletable-harness` success | same run |
| Why the gate jobs fail | one criterion, CI-6: the exact-tree review record is stale | the run log, `readiness-local ... failing: 1 criteria` |

The job names matter because a required status check is matched by name. A
ruleset that names a job the workflow does not report blocks every merge
forever, and one that names nothing blocks none.

## The proposal

One ruleset, targeting the default branch, enforced (not evaluate-only).

| Rule | Setting | Why this and not stricter |
|---|---|---|
| Require a pull request before merging | on, 0 required approving reviews | The maintainer merges alone. Requiring a review from a second GitHub account would either block every merge or invite self-approval from a second account, which is worse than none. The independent-review mechanism this repository actually uses is the exact-tree record behind CI-6, and that is enforced by the status check below, not by a GitHub approval |
| Dismiss stale approvals on push | on | Costs nothing at 0 required reviews and is correct if reviews are ever required later |
| Require status checks to pass | `gate (3.11)`, `gate (3.13)`, `deletable-harness` | These are the three names the workflow reports. All three, because the Python matrix exists to catch interpreter-specific assertions (see the comment in `lint.yml`), and a merge that is green on one interpreter and unmeasured on the other is not green |
| Require branches to be up to date before merging | on | The review record binds to a tree digest. Merging a branch that was green against an older `main` produces a merge tree nobody measured, which is the CI-6 failure mode by another route |
| Block force pushes | on | The release contract forbids history rewriting on `main`; this makes the rule mechanical |
| Restrict deletions | on | Same |
| Require linear history | off | Merge commits are the current practice (PR #13 through #19 are all merge commits) and the changelog's ancestry checks assume them. Turning this on would change the merge record retroactively |
| Require signed commits | off | Not currently practised; turning it on would block the maintainer's own commits until signing is set up. Worth revisiting once EXT-RELEASE asks for a signed tag |
| Bypass list | empty | An administrator bypass is exactly the "admin bypass as a workaround for red checks" the release contract names as forbidden. If a bypass is ever needed, the honest move is to disable the ruleset visibly, merge, and re-enable it, so the audit log shows the decision |

## What this does and does not do

It does: make an unmeasured merge impossible, and make a red `main` impossible
to reach through the pull-request path.

It does not: substitute for EXT-TEAM. A required status check proves the tree
was measured; it does not prove a second person read it. EXT-TEAM stays
required, with its own evidence, exactly as `external-gates.json` says.

It also does not fix the current red. Applying this ruleset today would block
every merge until CI-6 is closed, because `gate (3.11)` and `gate (3.13)` are
failing on `main`. The order is therefore: close CI-6 through the review-record
path first, confirm both gate jobs green on that exact commit, then apply.

## How the administrator applies it

The payload below matches the table. It is given so the administrator can
read what is being asked before running anything; it has not been run by any
agent, and no agent has the authority to run it under the release contract.

```bash
gh api --method POST repos/RizwanZafaris/product-manager-OS/rulesets \
  --input - <<'JSON'
{
  "name": "main: measured merges only",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "bypass_actors": [],
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_review_thread_resolution": false}},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": true,
      "required_status_checks": [
        {"context": "gate (3.11)"},
        {"context": "gate (3.13)"},
        {"context": "deletable-harness"}]}}
  ]
}
JSON
```

Verify afterwards with `gh api repos/RizwanZafaris/product-manager-OS/rulesets`
(expect one entry) and by opening a throwaway pull request from a branch with a
deliberately failing test: the merge button must be unavailable.

## Decision record

| Field | Value |
|---|---|
| Proposed by | the agent lead, 2026-09-09, from the observations above |
| Decision | Approved and applied by the repository administrator as proposed. GitHub filled in one default the payload did not set: `require_extra_approval_for_unattributed_changes: true` on the pull-request rule |
| Applied on | 2026-09-12, after `main` went green at `29bba38` (hosted run 34645522548): ruleset id 22968065, "main: measured merges only", enforcement active, no bypass actors; `gh api repos/RizwanZafaris/product-manager-OS/rulesets` returns that one entry |
