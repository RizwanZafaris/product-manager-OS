---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/planning/growth-plan.md", "templates/operate/experiment-brief.md", "frameworks/metrics/north-star-input-tree.md"]
method: "knowledge/INDEX.md"
aliases: ["Growth Loops", "growth-loops"]
---
# Growth Loops

Based on the ideas of Brian Balfour and Casey Winters, from the Reforge growth essays and programs (2018 onward). Explained here in this repository's own words.

## What it is for

A funnel is linear: people enter at the top, some come out the bottom, and tomorrow you must refill it. A loop is closed: the output of one cycle (a new user, a piece of content, a data point) becomes the input of the next, so the product does some of its own acquisition. This worksheet draws the loop as a table, measures each step, and computes the reinvestment factor, which is how many new users one user generates per cycle. It answers whether the product grows itself at all, how fast, and which step to push. The decision it improves is where growth effort compounds versus where it merely adds.

## Run it when

- The growth plan needs a mechanism and the product has a natural spillover: teammates, managers, shared documents, public output
- Acquisition spend is rising while new users per dollar fall
- The growth agent is diagnosing why a cohort-based rollout stalled
- Deciding between a referral feature and a top-of-funnel campaign

**Skip it when:** no path exists from one user's use to the next user's arrival without a salesperson. Drawing a loop for a single-player internal tool produces a circle with a hopeful arrow; use the [AARRR funnel](aarrr-funnel.md).

## Inputs you need first

- Stage events from the [AARRR funnel](aarrr-funnel.md), especially the activation and referral events
- A [cohort table](cohort-retention.md) to read the cycle time from
- The rates for each loop step, per cohort, from the analytics spec
- Cost per cycle, if the loop consumes money (credits, inference, human review)

## The worksheet

### Step 1: draw the loop

The last row's output must be the first row's input. If it is not, you have drawn a funnel.

| Step | Input (what enters) | Action (who does what) | Output (what comes out) | Output feeds step | Rate r (output / input) | Users generated per action (g) |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | 1 | | |

### Step 2: loop math

| Quantity | Symbol | Formula | Value | How measured |
|---|---|---|---|---|
| Starting cohort | N0 | activated users from external acquisition per period | | |
| Reinvestment factor | k | r1 x r2 x ... x rn x g | | product of the step rates, per cohort |
| Cycle time | t | | | median days from a user's activation to the activation of a user they generated |
| Users from one cycle | N1 | N0 x k | | |
| Long-run amplification (k under 1) | A | 1 / (1 minus k) | | total users per externally acquired user, over many cycles |
| Cycles per quarter | c | 90 / t | | |
| Users in a quarter | | N0 x (1 + k + k^2 + ... + k^c) | | |

Rules: k at or above 1 means the loop grows without external input, which is rare and should be re-measured before anyone repeats it in a board deck. k under 1 is still valuable; it multiplies every externally acquired user by A. k and t matter together: k of 0.5 with a one-week cycle beats k of 0.8 with a two-month cycle over a quarter. Recompute k per cohort, because it decays as the loop reaches people with less fit.

### Step 3: loop or funnel

| Question | Loop | Funnel |
|---|---|---|
| Does one cycle's output re-enter without new spend? | yes | no |
| Can k be measured from instrumented events? | yes | not yet |
| Is t shorter than the planning period? | yes | no |
| Are activation and retention leaks already fixed? | yes | fix those first |

Decision rule: model growth as a loop only when all four answers are in the loop column. Otherwise run the funnel and fix its leaks; a loop multiplies whatever enters it, waste included.

## Reading the result

The step to push is the one with the lowest rate that the team can actually influence; a rate near its ceiling (nearly every submitter's manager already sees the prompt) has no headroom. Compare k across cohorts: a falling k is the loop saturating, and projecting the first cohort's k across the company is the most common way a growth model lies. A long t with a decent k argues for shortening the cycle (earlier prompt, faster invite) before raising any rate. If A is close to 1, the loop is decoration and the honest plan is a funnel.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot. The loop is the manager loop: a submitter's copilot-drafted report reaches a manager, the manager enables the copilot for the whole team, the team's new submitters repeat the cycle.

| Step | Input | Action | Output | Rate | g |
|---|---|---|---|---|---|
| 1 | Activated submitter | Submits a copilot draft; manager sees the "enable for your team" prompt | Manager who saw the prompt | 0.9 | |
| 2 | Manager who saw the prompt | Enables the copilot for the team | Team enabled | 0.18 | 6.5 invites |
| 3 | Invited employee | Activates (first matched draft submitted) | Activated submitter, back to step 1 | 0.45 | |

k = 0.9 x 0.18 x 6.5 x 0.45 = 0.474. Cycle time t = 24 days, so about 3.75 cycles per quarter. Amplification A = 1 / (1 minus 0.474) = 1.9.

Worked cycle from a rollout wave of N0 = 1,000: cycle 1 adds 474, cycle 2 adds 225, cycle 3 adds 106, cycle 4 adds 50, so about 1,855 activated submitters by quarter end, approaching 1,900 in the limit. The weakest controllable step is the manager enable rate at 0.18. Raising it to 0.28 gives k = 0.74 and A = 3.8; the same wave would approach 3,800 users. That step, not more invite email, is the growth bet.

## The trap

The first-cohort k. The rollout wave was the enthusiasts: managers who asked for the copilot, teams with heavy travel. Their enable rate was 0.18; the general population's turned out lower, and a plan built on the wave-1 loop promised a company-wide number that the loop could not deliver. Recompute k for every cohort and plot it; a loop whose k falls with each cohort is a loop that is finishing, and the plan should say so before the board deck does.

## Feeds

- [Growth plan](../../templates/planning/growth-plan.md), section 3 (the loop behind the metric) and section 4 (the step to push as the cheapest experiment)
- [Experiment brief](../../templates/operate/experiment-brief.md), one per step pushed
- [North star input tree](north-star-input-tree.md): the weakest step rate is a candidate input
- The [growth agent](../../agents/growth-agent.md) runs this diagnosis
- OPERATE stage, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: [AARRR entry in the knowledge index](../../knowledge/INDEX.md), the funnel this worksheet compares against
