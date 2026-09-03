# Path: Foundations

Audience: you are new to product management, or you have done the job by instinct and want one structured pass through the basics. No prior artifact experience assumed.
Fictional product: **Streakline**, a mobile habit tracker. Everything about it is invented, including its users; that is the point. Prefix invented evidence with "invented:" so the habit of labeling survives into real work.
Time: one step is an evening. Rushing two steps into one produces two half-filled templates, and the tutor will say so.

Before step 1: create `learn/products/streakline/`, copy the ledger below into `PROGRESS.md` there, and read the workspace rules in [products/README.md](products/README.md). Check boxes in your copy, never in this file.

## Ledger (copy into learn/products/streakline/PROGRESS.md)

- [ ] Step 1: the loop, and problems over features
- [ ] Step 2: discovery, on paper
- [ ] Step 3: the job to be done
- [ ] Step 4: definition at the right weight
- [ ] Step 5: prioritization without theater
- [ ] Step 6: the metric that means value
- [ ] Capstone: Gate 1, scored

## The standing brief

Every step draws on one invented situation, so your artifacts accumulate instead of restarting each evening. Copy this block into your PROGRESS.md and treat it as the only fact base you start with; anything else a step needs, you invent and label.

Invented: Streakline is eleven months old, 4,300 monthly active users, no revenue, four engineers and one designer. Day-30 retention sits at 11 percent. Of accounts created last quarter, 63 percent created exactly one habit and never opened the app again after their first week. Support is a shared inbox taking roughly forty messages a month, most of them about reminder timing. The team's stated plan for next quarter is "social features". Nobody has interviewed a user who quit.

Those are your baselines wherever a step asks for one, labeled invented every time. The label matters more than the number: an unlabeled practice figure that gets quoted back at you as a fact has taught you the one habit this layer exists to prevent.

## Step 1: the loop, and problems over features

**Read:** [Empowered product teams](../knowledge/cagan-product-teams.md). Notice the trap: the label without the accountability.
**Study:** [the operating loop](../os/OPERATING-LOOP.md), then skim [the six gates](../os/STAGE-GATES.md). You are learning the map, not filling anything yet.
**Do:** write two paragraphs in your PROGRESS.md. First: Streakline described as a feature list. Second: Streakline described as a problem some specific person has. Make the two deliberately different, then note which one the loop's Gate 1 could actually test.
**Done when:** the second paragraph names a person-shaped user, a circumstance, and a cost of the problem staying unsolved, and you can say which gate would catch the first paragraph's weakness.

**Why this comes first.** Everything downstream inherits the framing you open with, and the two framings differ in one property that matters more than elegance: failure behavior. "We shipped social features" stays true whether or not a single user's life changed, so it generates no information. A problem statement can be killed by one honest interview, which is precisely why it is worth writing. You are learning to prefer the claim that can lose.

**What good looks like.** Weak: "Streakline helps people build better habits." That survives any evidence, so it carries none. Strong: "Invented: a nurse on rotating nights sets a 7am meditation reminder, is asleep at 7am half the month, swipes the notification away without practicing, and quits in week two rather than keep a streak she knows is fake." Who, when, what they did, what it cost. That is the shape Gate 1's cost-of-inaction line demands, three steps before you meet it.

**Pass criteria.** Three checks before you tick the box. Delete every product name from paragraph two and it still describes a person in trouble. The cost line names who personally eats the cost, not the company. And you can point at the specific line in [the gates](../os/STAGE-GATES.md) that paragraph one would fail, by name.

**The trap, and its tell.** The solution smuggled into the problem. The tell is grammatical: your problem sentence contains a noun that exists only inside your product, like "streak freeze" or "reminder cadence". If deleting Streakline from the world would make the sentence unreadable, you wrote a feature list in problem clothing.

**Time.** Sixty to ninety minutes, most of it on the second paragraph. That ratio is correct.

## Step 2: discovery, on paper

**Read:** [Continuous discovery](../knowledge/torres-continuous-discovery.md). The trap here, a stale tree, is the one this exercise simulates away.
**Run:** [the Mom Test interview guide](../frameworks/discovery/mom-test-interview-guide.md) against an imagined quitter from the brief. Write the questions before you write the answers you wish you had, because inventing evidence backwards from a conclusion is the one practice habit that transfers badly.
**Study:** [the discovery document](../templates/discovery/discovery-document.md), guidance comments included; the worked micro-example at the bottom is your quality bar.
**Do:** fill the whole discovery document for Streakline. Invent the trigger, the target user, and at least three evidence rows, each labeled invented, each with the shape real evidence would have: a type, a source ID, a date.
**Done when:** every exit-gate checkbox at the bottom of your filled copy can be honestly ticked, including the falsifiable hypothesis with a baseline and a target, and a kill signal you wrote while still neutral.

**Why now.** The hypothesis you write here is the only thing that makes step 6's metric mean anything; a north star chosen before a hypothesis is a picture hung before the wall exists. Write the kill signal now, while you are neutral, because once you have spent an evening on the one-pager in step 4 you will set it where it can never fire and you will not notice yourself doing it.

**The rubric.** A 2: three evidence rows sitting on three different rungs of the ladder in [the bank format](../skills/conductor/questions/README.md), each with a source ID a reader could theoretically open, and a hypothesis of the form "invented: day-30 retention is 11 percent today; reminder rescheduling moves it to 18 percent by March". A 1: three rows that are all interview claims wearing different labels, or a target with no baseline beside it. A 0: a hypothesis no observation could contradict.

**The trap, and its tell.** Three rows that are secretly one belief. The tell: all three share a date, or reading them in any order tells you nothing new. Real corpora disagree with themselves somewhere. If your invented evidence is perfectly consistent, you invented a conclusion and dressed it three ways.

**Time.** Ninety minutes to two hours. The longest step in the path, and the one that repays a redo most.

## Step 3: the job to be done

**Read:** [Jobs to be done](../knowledge/jobs-to-be-done.md). The competition for Streakline is not other habit apps; work out what it actually is before you write.
**Run:** [the JTBD job map](../frameworks/discovery/jtbd-job-map.md) and stop at the map before you touch the template; the filled map in [the Ledgerline example](../examples/ledgerline-jtbd-job-map.md) shows the altitude to write at.
**Study:** [problem framing](../templates/discovery/problem-framing.md).
**Do:** fill the problem framing for Streakline. State the job in circumstance-motivation-outcome form, name what users hire today instead (a paper calendar, a phone alarm, nothing), and write the cost of inaction as a number with a unit and a period, labeled invented.
**Done when:** a stranger reading only your job statement could list Streakline's three real competitors, and none of them is an app.

**Why now.** Steps 4 through 6 all inherit this one sentence: Kano classifies candidates against the job, the roadmap orders work by how much of the job it completes, and the north star measures whether the job got done. Getting the job wrong here costs an hour. Discovering it wrong at step 6 costs three artifacts, which is the whole argument for putting it this early.

**What good looks like.** Weak: "helping users track habits", a feature in gerund form that competes only with other trackers. Strong: "invented: when I have decided to change something about myself and do not trust my own follow-through, I want proof I am the kind of person who does it, so I keep going on the days I do not feel like it." That version's competitors are a paper wall calendar, a friend who asks on Sundays, and quietly giving up, and none of them has a store listing.

**Pass criteria.** A 2: an observable circumstance, one motivation, one outcome, and three named competitors of which at least one is not buying anything. A 1: the right form with a circumstance so general it fits any adult with a resolution. A 0: a competitor list made of apps, which means the job was never found.

**The trap, and its tell.** Progress inflated into identity until the statement fits everything. The tell: swap Streakline for a running app or a language app and the sentence stays true. When that happens the circumstance is missing, and a job without a circumstance is a slogan.

**Time.** Sixty minutes, and expect to rewrite the job sentence four times. The rewriting is the work, not friction before it.

## Step 4: definition at the right weight

**Read:** [the Kano model](../knowledge/kano-model.md), and the weight logic in [WHICH-DOCUMENT](../os/WHICH-DOCUMENT.md). Delighters decay into basics; your feature list should show you know that.
**Run:** [the Kano survey](../frameworks/discovery/kano-survey.md) on your five candidates, functional and dysfunctional question per feature, before classifying anything by instinct. The classification you feel is usually the one you were hoping for.
**Study:** [the one-pager](../templates/definition/one-pager.md). Notice what it refuses to include, and the promotion rule to a full PRD.
**Do:** fill the one-pager for Streakline's first release. Then list five candidate features in PROGRESS.md and classify each as basic, performance, or delighter, with one line of reasoning each. At least two candidates must not make the release.
**Done when:** the one-pager carries exactly one metric plus a guardrail, a not-doing list with your two cut features on it, and your Kano reasoning would survive a "says who" per line.

**Why now.** This is the first step where you say no in writing, and the weight question arrives with it. Streakline gets a one-pager rather than a PRD because the decision is reversible inside a two-week release by four engineers, and [WHICH-DOCUMENT](../os/WHICH-DOCUMENT.md) routes reversible low-stakes work to the lightest artifact that can carry it. Be able to say that sentence about your own choice, because a PM who cannot defend a document's weight will default to the heaviest one available and call it thoroughness.

**The rubric.** A 2: the guardrail names something the metric could break if the team pushed it stupidly, such as invented notifications per user per day held at three or fewer while completion rate climbs. A 1: a guardrail that is a second goal in disguise, pointing the same way as the metric, so nothing can ever trip it. A 0: no guardrail, or a not-doing list full of things nobody proposed, which is a decoy rather than a decision.

**Worked micro-example.** Invented classifications worth arguing with: reminder rescheduling is a basic, because a tracker that fires at a time you cannot act is broken rather than merely plain; weekly progress email is performance, because more of it is better up to a point and then it is spam; the shareable year-in-habits card is a delighter this year and will be table stakes in two, which is the decay the card warns about. Cut the card and one more, and write the cut reasons next to them, because a not-doing list without reasons gets quietly undone by the next person who reads it.

**The trap, and its tell.** Everything classified as a delighter, because delighters are more fun to argue for. The tell is the absence test: a feature whose absence would generate no complaint is not a basic, and if you cannot name one candidate whose absence would produce a support message tomorrow, you have not found the basics at all.

**Time.** Two hours: one for the survey design and classification, one for the one-pager.

## Step 5: prioritization without theater

**Read:** [RICE prioritization](../knowledge/rice-prioritization.md). The trap is false precision; you are about to manufacture some on purpose so you can catch yourself doing it.
**Run:** [the RICE scoring sheet](../frameworks/prioritization/rice-scoring-sheet.md) for the arithmetic and the tie rule, then [Now, Next, Later](../frameworks/prioritization/now-next-later.md) to place the survivors. The sheet owns the mechanics; this step owns whether you were honest while filling it.
**Study:** [the roadmap](../templates/planning/roadmap.md), preamble first.
**Do:** score your five features from step 4 with RICE, all inputs invented and labeled. Then build a Now, Next, Later roadmap for Streakline. Somewhere, two scores must land close together; resolve that tie in the open with judgment, and write one line saying the scores were a tie and why you ordered them as you did.
**Done when:** the roadmap reads as expectations rather than commitments, and your tie-break line proves you treated near scores as buckets, not rankings.

**Why now.** You have five candidates and room for two, so this is the first artifact in the path that costs somebody something. The tie is engineered into the exercise deliberately, because ties are where prioritization actually happens: wide gaps decide themselves, and a PM who has only ever ordered obvious lists has never prioritized anything.

**Worked micro-example.** Invented: reminder rescheduling, reach 2,600 quitters per quarter, impact 2, confidence 0.8, effort 2, score 2,080. Streak repair, reach 2,600, impact 1, confidence 0.8, effort 1, score 2,080. Identical, and the honest sentence reads: these tie, rescheduling goes first because the support inbox says timing is what people write in about, and repair without correct timing only prettifies a broken loop. That sentence is the deliverable. The number was the excuse to have the argument.

**Pass criteria.** A 2: five scored rows with the arithmetic column filled, one declared reach unit used throughout, a Now list that fits your invented capacity, and a tie-break line naming the judgment rather than the number. A 1: correct arithmetic with a roadmap that reads as a delivery promise with dates. A 0: an order you had before you scored, reverse-engineered.

**The trap, and its tell.** Confidence used as a thumb on the scale. The tell is a pattern rather than a single row: every item you already wanted scored 0.8, everything a colleague proposed scored 0.5, and the evidence behind both is the same invented inbox. Fill the confidence column before you look at the resulting order, then leave it alone.

**Time.** Ninety minutes. Fifteen of those go to the tie-break line, which is the part the tutor grades hardest.

## Step 6: the metric that means value

**Read:** [North star metric](../knowledge/north-star-metric.md). A habit tracker is a vanity-metric minefield: opens and streaks are easy to move and mean nothing. Find the metric that means a user's life changed.
**Run:** [the north star input tree](../frameworks/metrics/north-star-input-tree.md) so your three inputs are derived rather than brainstormed, with the filled tree in [the Ledgerline example](../examples/ledgerline-north-star-tree.md) as the decomposition bar.
**Study:** [the metrics review](../templates/operate/metrics-review.md), so you see where the metric eventually gets judged.
**Do:** in PROGRESS.md, define Streakline's north star metric and three input metrics a team could move, with an invented baseline for each. Write one sentence per input on how it could be gamed, because it can.
**Done when:** your north star measures delivered user value rather than app activity, each input has an owner-shaped team attached, and every gaming sentence names a real mechanism.

**Why now.** This closes the loop opened at step 2: the hypothesis said what should change, the metric is how anyone would know. Written last, it also catches an earlier error cheaply, because a north star you cannot trace back to your job statement means one of the two is wrong, and you find out now instead of after a quarter of building.

**What good looks like.** Weak: daily active users, which rises when a notification bug fires twice. Also weak: average streak length, which rises fastest among users whose habit is trivial enough never to miss. Strong: invented weekly count of users completing a self-declared habit on four or more days, baseline 640 of 4,300, target 900. It moves only when somebody did the thing they set out to do, which is the value the product claims to deliver.

**Pass criteria.** A 2: a north star with an invented baseline and target, three inputs each carrying an owning team and a named gaming mechanism, and one written sentence linking the metric back to the job statement from step 3. A 1: a defensible north star whose inputs are the same measurement sliced three ways, which gives a team nothing to divide up. A 0: an activity metric, however well decorated.

**The trap, and its tell.** The metric that moves while nobody benefits. The tell is a sentence test you can run on any candidate: write "this number went up and no user's life changed" and see how plausible it sounds. For app opens it is trivial. For four-day completions it takes real contortion, and that difficulty is the quality you are selecting for.

**Time.** Ninety minutes including the gaming sentences, which are fast to write and the quickest way to disqualify a weak candidate.

## Capstone: Gate 1, scored

Run the tutor ([skills/tutor/SKILL.md](skills/tutor/SKILL.md)) against your filled Streakline discovery set. The tutor drills you from the DISCOVER bank ([the questions](../skills/conductor/questions/discover.md)), pushes once per weak answer, shows model answers, and scores every Gate 1 line.

**Done when:** every Gate 1 exit-gate line scores 2. A 1 anywhere means one targeted redo, card first; a 0 means the step that produced it gets rerun. Without an AI runtime, self-interview from the bank file and grade yourself against the Accept-when lines, which is harsher and works.

**Where each gate line comes from.** Gate 1 in [STAGE-GATES.md](../os/STAGE-GATES.md) has eight lines and every one traces to a step you already did: the single-sentence problem statement to step 1, the five cited conversations and the personas marked as assumptions to step 2, the cost of inaction to step 3, the argued no-go case to step 2's kill signal, the Gate 6 success signal to step 6. Read that mapping before the session, because if a line has no artifact behind it the failure happened at the step, and rerunning the gate will not manufacture one.

**Pass criteria for the session itself.** A 2 across all eight lines, every score landed in PROGRESS.md with the weakest area named, and the redos done as fresh attempts rather than edits to the old file. A session with no 1 and no 0 anywhere in it is not a triumph, it is a signal to check whether you handed over the artifact or a summary of it.

**The trap, and its tell.** Arguing with the tutor. The tell is that your reply to a critique opens by explaining what you meant. An artifact that needs your voice in the room to pass fails the moment the room is a stranger reading it six months later. Fix the artifact, resubmit, say nothing.

**Time.** One session of sixty to ninety minutes, plus the redos it names. Budget a second evening. A capstone that passes clean on a first pass through this path usually means the tutor was handed a thin artifact and graded it generously.

## When you are ready to leave this path

Not when the boxes are ticked. Three signals, and the first is the one that counts: you can look at a request from someone else, "add social features", and say in one sentence which artifact it belongs in, what evidence it is missing, and which gate would stop it. Second, you have caught yourself writing a naked number in something real, at work or elsewhere, and fixed it before anyone asked. Third, at least one Done-when line in this path failed on your first attempt and you rewrote rather than argued, because a path completed without a single redo taught you the vocabulary and not the discipline.

Next path when you want more: [Transitioning](path-transitioning.md) if you are changing roles, [Senior sharpening](path-senior.md) once you have run a real product through a few gates.
