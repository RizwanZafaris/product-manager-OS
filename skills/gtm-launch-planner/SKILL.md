---
name: gtm-launch-planner
description: Tier a launch, choose the first cohort, build the channel plan, and draft the comms and readiness lines so Gate 5 finds them already written. Use when a customer-facing release is coming and the GTM plan or the comms table is empty, when PM and PMM disagree on how big the launch is, when a release takes something away or changes what customers pay, or when a failed launch needs a second attempt. Takes the positioning, the success signal, the release scope and window, and the channel evidence; returns the tier decision, the filled GTM plan, the channel plan by funnel stage, the comms plan, and the readiness rows.
---

# GTM Launch Planner: tier it, pick the cohort, write the stop rule first

Launches fail in two mirror-image ways. Every release is treated as the big one, so none of them is, and the comms are drafted the night before. Or a release that changes what customers pay ships as a changelog line, and support hears about it from customers. Both get judged afterwards by applause. This skill sets the tier by rule, names a cohort you can list, and writes the one metric and the stop condition before anyone is excited.

## Files this skill drives

- [../../templates/planning/gtm-plan.md](../../templates/planning/gtm-plan.md), every section
- [../../templates/delivery/launch-comms-plan.md](../../templates/delivery/launch-comms-plan.md), for a tier that needs more than the readiness doc's comms table
- [../../templates/delivery/release-readiness.md](../../templates/delivery/release-readiness.md), section 6 and the rollback trigger in section 4
- [../../templates/delivery/sales-enablement-one-pager.md](../../templates/delivery/sales-enablement-one-pager.md), [../../templates/delivery/customer-comms.md](../../templates/delivery/customer-comms.md), and [../../templates/delivery/release-notes.md](../../templates/delivery/release-notes.md), the audience artifacts a tier calls for
- Read first: [../../templates/planning/positioning.md](../../templates/planning/positioning.md), which the positioning skeleton is cut from
- Worksheets: [../../frameworks/strategy/positioning-canvas.md](../../frameworks/strategy/positioning-canvas.md) (Dunford, Obviously Awesome, 2019), [../../frameworks/metrics/aarrr-funnel.md](../../frameworks/metrics/aarrr-funnel.md) (McClure, 2007)
- Method background: [../../knowledge/crossing-the-chasm.md](../../knowledge/crossing-the-chasm.md) (Moore, 1991), [../../knowledge/roles/pmm-boundary.md](../../knowledge/roles/pmm-boundary.md)
- Hands the packet to [../../skills/launch-readiness/SKILL.md](../../skills/launch-readiness/SKILL.md) for the Gate 5 verdict

## When to use

- A customer-facing release is scheduled and the GTM plan does not exist, or its comms table is empty
- PM and PMM disagree on whether this is a big launch
- The release takes something away, changes permissions, or changes what customers pay
- A launch missed its metric and is being rerun
- Early enough that each phase's comms can be drafted before that phase's entry, which is what Gate 5 checks

## Inputs

The positioning document; if none exists, run [../../skills/competitive-intel/SKILL.md](../../skills/competitive-intel/SKILL.md) first rather than inventing a category in launch week. The Gate 1 success signal and the north star tree, for the one launch metric. Release scope and the target window from the readiness doc. Evidence of a reachable first cohort: a pilot list, a community you already stand in, a signed agreement. The channels available, with the artifact that proves each one reaches the cohort. Support and sales capacity. Whether pricing changes (route through [../../skills/pricing-packaging/SKILL.md](../../skills/pricing-packaging/SKILL.md)) and whether a regulator is in scope (route through [../../skills/reg-gap-check/SKILL.md](../../skills/reg-gap-check/SKILL.md)).

Ask for what is missing: what changes for existing users, anything taken away included; who can say no-go during the launch; and where the baseline for the launch metric is computed.

## Workflow

### 1. Set the tier by rule

Three tiers, decided by what the release changes, not by how proud the team is. Tier 1: it changes how a customer buys, pays, or works day to day, or it opens a new segment; it gets the full comms plan, a phased rollout, sales enablement, and customer comms. Tier 2: a visible improvement for existing users; it gets release notes, a support briefing, an in-app notice, and one or two phases. Tier 3: invisible or internal; a changelog line and a support note. Two overrides: anything taken away or any price change is at least Tier 2 with customer comms and a notice period; any regulated disclosure is Tier 1 regardless of size. The tier names the templates that get filled, so the argument about size ends here.

### 2. Name the beachhead

One cohort, small enough to name and reach, with the channel that reaches it and an artifact proving it, per section 1 of the GTM plan. Decision rule: if a member list could not be assembled this week, the cohort is a segment wearing a cohort's clothes. Widen from proof, one cohort per phase.

### 3. Cut the positioning skeleton

Fill section 2 of the GTM plan from the positioning document in canvas order: for whom, who struggles with what, the category the buyer already has a shelf for, the one capability, unlike the named alternative, verified how. The "unlike" line names what the cohort does today, a spreadsheet included. If it names no alternative, the section goes back for rework.

### 4. Plan the channels against the funnel

For each stage of the AARRR funnel (acquisition, activation, retention, referral, revenue) name the channel or mechanism, the event that marks the stage in the analytics platform, the leak you expect, and an owner. A launch channel is a hypothesis about acquisition and activation; the event is how you learn whether the hypothesis held. Channels with no event behind them are cut.

### 5. Sequence, metric, stop

Phases advance on exit conditions a reader could check, never on dates, and each phase's comms are drafted before its entry. One launch metric, with the baseline from the metrics review or the analytics platform, the target from the OKR sheet or marked [OPEN: owner], the source system, and a review date. The stop condition names a threshold, a caller reachable during launch, and the rollback the readiness doc actually rehearsed.

### 6. Write the comms and the readiness rows

Launch facts written once in the comms plan, every message derived from them. Audience rows with an action, an owner, and a sign-off. A T-minus timeline with support briefed before any external message. The rollback holding statement drafted now. The sales one-pager, customer comms, and release notes cut from the same facts. Then the readiness doc's section 6 rows and the rollback trigger, and the packet goes to launch readiness for the verdict.

## Output format

1. Tier decision: the tier, the rule that set it, the override that applied if any, the template list it triggers
2. GTM plan sections 1 to 5: beachhead table, positioning skeleton, phase table, the one metric row, the stop condition row
3. Channel plan: | Funnel stage | Channel | Event that marks it | Expected leak | Owner |
4. Comms plan sections 1 to 5, the audience artifacts drafted, and the readiness doc rows
5. The handoff line to launch readiness, with what is still [OPEN: owner]

## Failure modes this skill guards against

- Every release a Tier 1 launch, or none of them
- A cohort called "the market"
- A category invented in launch week because positioning was never done
- A launch judged by impressions and coverage instead of the one metric
- A stop condition decided after the metric fell
- Comms drafted the night before, and support learning the release from customers
- Something taken away silently
- A price change hidden inside a feature launch
- A launch date presented as a promise instead of a window
- Five launch metrics, so the launch is judged by whichever one moved

## Exit gate

The plan feeds Gate 5 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) through the readiness doc. Do not report it done until the GTM plan's and the comms plan's exit gates pass, every phase has its comms drafted before its entry, and launch readiness has the packet.
