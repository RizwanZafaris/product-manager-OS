# Information Architecture: Tillwick Payroll, Settings and admin area

Fills [templates/architecture/information-architecture.md](../templates/architecture/information-architecture.md). Everything here is invented for this standalone example: Tillwick Payroll is a fictional payroll product for small employers, Tillwick its fictional maker, and every participant count, ticket count, percentage, name and date is ILLUSTRATIVE, not drawn from any real company, study or customer. There is no journey or data sheet behind it. See the [examples index](README.md).

**Area in scope:** the Settings and admin area of the Tillwick Payroll web app: every page an employer's admin uses to configure payroll rather than run it
**Owner:** Marisol Achterberg, Product Manager, Settings · **Design lead:** Felix Oduya · **Research lead:** Rhiannon Okafor
**Date:** 2026-10-28 · **Status:** Approved at Gate 3 with one waiver (task T6, section 4) · **Tree version tested:** settings-tree-v3 (round 1), settings-tree-v3.1 (round 2, task T3 only)

Why this exists: Settings grew from 19 pages at launch to 64 over five years (ILLUSTRATIVE), each added under whichever team built the feature. "Where do I change..." became the largest support ticket category, with 1,840 tickets in the six months to 2026-07-31 (ILLUSTRATIVE).

## 1. Top tasks the structure must serve

| Task id | Task, in the user's words | Who does it | Evidence of frequency (count, window) | Source |
|---|---|---|---|---|
| T1 | "We're moving from every two weeks to twice a month, where do I change that?" | Owner or office manager | 312 tickets, Feb to Jul 2026 | Support tag `where-is` |
| T2 | "Wages should come out of our new business account" | Owner | 268 tickets | Support tag `where-is` |
| T3 | "An employee gave me new details for where their wages go" | Office manager | 241 tickets | Support tag `where-is` |
| T4 | "I hired someone who works in another state, how do I set up withholding there?" | Owner, bookkeeper | 187 tickets | Support tag `where-is` |
| T5 | "My bookkeeper needs last year's forms for each employee" | Bookkeeper | 98 tickets | Support tag `where-is` |
| T6 | "I want wage totals to show up in our accounting software automatically" | Bookkeeper | 76 tickets | Support tag `where-is` |
| T7 | "Let my office manager run payroll without seeing what everyone earns" | Owner | 71 tickets | Support tag `where-is` |
| T8 | "Change how many vacation days new staff earn" | Office manager | 53 tickets | Support tag `where-is` |

The eight tasks account for 1,306 of the 1,840 `where-is` tickets (71%, ILLUSTRATIVE). Settings search logs for the 90 days to 2026-07-31, 6,210 queries (ILLUSTRATIVE), rank the same eight among the top eleven query clusters.

## 2. Content inventory

Inventory produced from: the front-end router's route list, exported 2026-08-04, joined to 90 days of page views · Items: 71 (64 pages, 7 standalone dialogs) · Keep 38 · Merge 17 · Move 9 · Rewrite 4 · Remove 3 (all ILLUSTRATIVE)

Eight of the 71 rows are shown. The full inventory lives in `settings-inventory-2026-08.csv` in the product workspace, not tracked in this repository.

| Item | Type | Current location | Owner | Usage (count, window) | Decision | Reason |
|---|---|---|---|---|---|---|
| Pay schedule | Page | Payroll setup > Schedule | Dana Whitcombe, Pay team | 2,940 views, 90 days | Move | To Pay. Section 3a pairs it with pay types, not with funding |
| Funding account | Page | Payroll setup > Funding | Arjun Szabo, Money movement | 2,310 views | Move | To Banking. Only 5 of 18 participants grouped it with the pay schedule |
| Employee bank details | Setting on the employee record | People > employee > Payment | Lena Marchetti, People team | 4,120 views | Keep | Stays on the employee record; a cross-link was added after T3 failed (section 4) |
| State tax accounts | Page | Compliance > Registrations | Oskar Lindqvist, Tax team | 1,870 views | Move | To Taxes, beside year-end forms |
| Year-end forms | Page | Reports > Tax documents | Oskar Lindqvist, Tax team | 1,020 views | Move | To Taxes. 13 of 18 participants grouped it with tax registrations |
| Legacy pay periods | Page | Payroll setup > Advanced | Dana Whitcombe, Pay team | 41 views | Remove | Superseded by the pay schedule in 2023; every view came from an old bookmark, so it gets a redirect |
| Leave policies, Holiday calendar | Two pages | Leave > Policies; Leave > Holidays | Lena Marchetti, People team | 1,460 and 610 views | Merge | One Time off page with two sections; 16 of 18 grouped the two together |
| Connected apps | Page | Company profile > Integrations | Wei Ling Tan, Partnerships | 890 views | Rewrite | Relabelled after T6 failed (sections 4 and 6) |

## 3. Mental model evidence

### 3a. Open card sort

Participants: 18 current customers (12 owners or office managers, 6 bookkeepers) · Cards: 40 · Unmoderated, online · Dates: 2026-08-11 to 2026-08-18 (all ILLUSTRATIVE)

| Card pair | Grouped together (k of n) | Pairwise agreement | What the proposed structure does | Reading |
|---|---|---|---|---|
| Pay schedule + Pay types | 14 of 18 | 78% | Together, under Pay | Keep together |
| Payroll funding account + Pay schedule | 5 of 18 | 28% | Apart: funding moves to Banking | The old tree had them together under Payroll setup; participants did not |
| Payroll funding account + Employee bank details | 12 of 18 | 67% | Apart | Participants group by the word "bank", which predicted the T3 failure before the tree test ran |
| Tax registrations + Year-end forms | 13 of 18 | 72% | Together, under Taxes | The old tree split them across Compliance and Reports |
| Admin users + Employee profile fields | 11 of 18 | 61% | Together, under People and access | Participants see both as "people"; see the label collision in section 8 |
| Accounting sync + Payroll funding account | 7 of 18 | 39% | Apart | Weak signal either way, so tested as T6 |
| Time off policies + Holiday calendar | 16 of 18 | 89% | Together, under Time off | Keep together |

A participant names several groups, so the counts below do not sum to 18.

| Word participants used for a group | Participants who used it (k of n) |
|---|---|
| Taxes, Tax | 15 of 18 |
| Time off | 13 of 18 |
| Pay, Paying people | 12 of 18 |
| Bank, Banking | 11 of 18 |
| Company | 10 of 18 |
| Team | 9 of 18 |
| Permissions, Access | 7 of 18 |
| Accounting | 6 of 18 |
| Integrations, Apps | 4 of 18 |
| Leave (the old label) | 2 of 18 |
| Compliance (the old label) | 1 of 18 |

### 3b. Closed card sort

Participants: 24 (16 owners or office managers, 8 bookkeepers; not the open-sort participants: yes) · Categories tested: Company, Pay, Taxes, Banking, People and access, Time off, and People (the employee records reached from the global rail) · Contested below: 60%, written 2026-08-20; the sort ran 2026-08-25 to 2026-09-01 (all ILLUSTRATIVE)

| Card | Most chosen category | Placement agreement (k of n) | Second choice (k) | Intended category | Verdict |
|---|---|---|---|---|---|
| Pay schedule | Pay | 21 of 24 (88%) | Banking (2) | Pay | Holds |
| Pay types | Pay | 19 of 24 (79%) | Company (3) | Pay | Holds |
| Payroll funding account | Banking | 18 of 24 (75%) | Pay (5) | Banking | Holds |
| Employee bank details | People | 11 of 24 (46%) | Banking (9) | People | Contested |
| Tax registrations | Taxes | 22 of 24 (92%) | Company (2) | Taxes | Holds |
| Year-end forms | Taxes | 17 of 24 (71%) | Company (4) | Taxes | Holds |
| Admins and permissions | People and access | 20 of 24 (83%) | People (3) | People and access | Holds |
| Accounting sync | Banking | 9 of 24 (38%) | Company (8) | Company | Contested, and the most chosen category is not the intended one |
| Time off policies | Time off | 23 of 24 (96%) | People (1) | Time off | Holds |
| Company address | Company | 19 of 24 (79%) | Taxes (4) | Company | Holds |

Cards meeting the threshold: 34 of 40 (85%). Contested cards and what happens to each: employee bank details stays on the employee record with a cross-link from Banking, tested as T3; accounting sync stays under Company, tested as T6; the other four (benefits provider, wage deduction orders, insurance policy, company documents) carry their decisions in the inventory file.

## 4. Tree test

Participants: 40 per task (28 customers, 12 non-customers who run payroll at firms under 50 staff), recruited through the in-app research panel and an external panel · Tree version: settings-tree-v3, holding the global rail's five items, all of Settings, and People down to the employee record's sections · Dates: 2026-09-14 to 2026-09-20 (all ILLUSTRATIVE)
Pass rule, written 2026-09-08: success at least 70% and directness at least 60%. A pass whose interval's lower bound sits below 55% is marked "on the line" and watched after launch.
Baseline: the live tree, settings-tree-v2, tested on the same eight tasks with 40 different participants, 2026-09-02 to 2026-09-06.

Paths below leave out the leading "Settings >" on Settings nodes; People paths start at the global rail. Task texts were checked against their destinations' labels before the run. T5's first draft said "year-end forms", which is the destination's label, and was rewritten on 2026-09-09.

| Task id | Task text as shown | Correct destination(s) | Success (k of n) | 95% interval | Directness (k of n) | First click correct (k of n) | Most common wrong destination (k) | Baseline success (k of n) | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| T1 | "From next month your staff get their wages twice a month instead of every two weeks. Where would you set that up?" | Pay > Pay schedule | 34 of 40 (85%) | 71% to 93% | 30 of 40 (75%) | 36 of 40 (90%) | Banking > Payroll funding account (3) | 26 of 40 (65%) | Pass |
| T2 | "You moved the company's money to a new account and want wages drawn from there. Where would you go?" | Banking > Payroll funding account | 30 of 40 (75%) | 60% to 86% | 26 of 40 (65%) | 30 of 40 (75%) | Pay > Pay schedule (6) | 16 of 40 (40%) | Pass |
| T3 | "One of your employees gave you new details for where their wages should go. Where would you enter them?" | People > employee record > Payment details | 20 of 40 (50%) | 35% to 65% | 24 of 40 (60%) | 22 of 40 (55%) | Banking > Payroll funding account (14) | 18 of 40 (45%) | Fail |
| T4 | "You hired your first employee who works in another state. Where would you set things up so the right amounts are withheld there?" | Taxes > Tax registrations | 32 of 40 (80%) | 65% to 90% | 28 of 40 (70%) | 34 of 40 (85%) | Company > Business details (4) | 24 of 40 (60%) | Pass |
| T5 | "Your bookkeeper asks for the documents each employee needs to file their personal return for last year. Where would you find them?" | Taxes > Year-end forms | 28 of 40 (70%) | 54% to 82% | 24 of 40 (60%) | 32 of 40 (80%) | Company > Documents (6) | 20 of 40 (50%) | Pass, on the line |
| T6 | "You want wage totals to appear in your bookkeeping software without retyping them. Where would you set that up?" | Company > Connected apps | 24 of 40 (60%) | 45% to 74% | 20 of 40 (50%) | 26 of 40 (65%) | Banking > Payroll funding account (12) | 12 of 40 (30%) | Fail |
| T7 | "Your new office manager should be able to run payroll but not see what anyone earns. Where would you arrange that?" | People and access > Admins and permissions | 34 of 40 (85%) | 71% to 93% | 28 of 40 (70%) | 36 of 40 (90%) | People > employee record (4) | 22 of 40 (55%) | Pass |
| T8 | "New staff should earn more vacation days each month. Where would you change that?" | Time off > Policies | 35 of 40 (88%) | 73% to 95% | 32 of 40 (80%) | 38 of 40 (95%) | People > employee record (2) | 28 of 40 (70%) | Pass |

The interval arithmetic, shown for the two rows a decision rests on (adjusted Wald, z = 1.96):

- T3: p' = (20 + 1.92) / (40 + 3.84) = 21.92 / 43.84 = 0.500; margin = 1.96 x sqrt(0.500 x 0.500 / 43.84) = 1.96 x 0.0755 = 0.148; interval 35% to 65%. Directness passes at 24 of 40 only because 14 participants went straight to Banking, which is a wrong answer reached directly. Success fails, so the task fails.
- T5: p' = (28 + 1.92) / 43.84 = 29.92 / 43.84 = 0.682; margin = 1.96 x sqrt(0.682 x 0.318 / 43.84) = 1.96 x 0.0703 = 0.138; interval 54% to 82%. The point estimate meets the rule and the lower bound is below 55%, so the pass is on the line.

Pooled across the eight tasks, for the headline only: the new tree found 237 of 320 (74%) against the live tree's 166 of 320 (52%) (ILLUSTRATIVE). Every decision below is made per task, because pooling hides which branch fails.

Decisions on every task that did not pass:

| Task id | Decision (restructure / relabel / cross-link / accept) | Re-test date and result | Approver if accepted |
|---|---|---|---|
| T3 | Cross-link: add "Employee bank details" under Banking, leading to the employee list. The setting itself stays on the employee record | 2026-10-12 to 2026-10-16, tree v3.1, 40 new participants: 30 of 40 (75%), 60% to 86%; directness 26 of 40 (65%). Pass. 11 of the 30 succeeded through the Banking cross-link, which was listed as a correct destination before the run because on screen it lands on the same page | Not needed |
| T6 | Relabel "Connected apps" to "Accounting and apps", keep it under Company, add a contextual link from Banking | [OPEN: round 2 for T6 has not run; Rhiannon Okafor, research lead, owns it, due 2026-11-12] | Waiver: Gate 3 proceeds with T6 open, approved by Marisol Achterberg, product owner, 2026-10-28, because the page's URL carries no category (section 7), so moving it after the re-test changes no inbound link |
| T5 | Accept as a pass on the line. Watch after launch: the share of Year-end forms sessions that begin from search, monthly from January 2027 | Not re-tested | Marisol Achterberg, 2026-10-28 |

## 5. Navigation model

| Navigation type | Where it appears | What it holds | Entry rule |
|---|---|---|---|
| Global | Left rail, every page | Home, Run payroll, People, Reports, Settings | A destination admins reach weekly or more. Settings is the one exception, by its size |
| Local | Settings, left column | Company, Pay, Taxes, Banking, People and access, Time off | One row per closed-sort category. A seventh needs a card-sort result, not a request |
| Contextual (links inside content or errors) | Payroll-run errors, empty states | "Funding account not verified" links to Banking > Payroll funding account | Every blocking error names where its fix lives and links there |
| Utility (account, help) | Top right | Help, Account, Sign out | Not product content |
| Search | Top of Settings | Every page title, every field label, the synonyms in section 6 | Indexed nightly from the route list |

Maximum depth: 3 levels (Settings > category > page; employee records are reached from People and are not counted) · Maximum items in one level: 9 (Pay) · Consistency rule: the local list sits in the same place, in the same order, on every Settings page

| Task id | Path to the destination | Steps | Second route (search term, contextual link) |
|---|---|---|---|
| T1 | Settings > Pay > Pay schedule | 3 | Search "pay frequency", "biweekly" |
| T2 | Settings > Banking > Payroll funding account | 3 | Contextual link from the payroll-run funding error |
| T3 | People > employee record > Payment details | 3 | Settings > Banking > Employee bank details (cross-link) |
| T4 | Settings > Taxes > Tax registrations | 3 | Prompt on the new-hire form when the work state has no registration |
| T5 | Settings > Taxes > Year-end forms | 3 | Reports > Year-end forms, a link to the same page |
| T6 | Settings > Company > Accounting and apps | 3 | Link from Banking; search "accounting", "ledger", "sync" |
| T7 | Settings > People and access > Admins and permissions | 3 | Search "permissions", "roles" |
| T8 | Settings > Time off > Policies | 3 | Search "PTO", "vacation" |

## 6. Labels and the words users used

| Node | Proposed label | Words users used (source, count) | Old label | Decision and reason |
|---|---|---|---|---|
| Category | Pay | "Pay", "Paying people" (open sort, 12 of 18) | Payroll setup | Participants group by what is being paid, and "Payroll setup" also held funding, which section 3a split off |
| Category | Taxes | "Taxes", "Tax" (open sort, 15 of 18); "tax" in 1,120 search queries in 90 days | Compliance | "Compliance" was used by 1 of 18 participants |
| Category | Banking | "Bank", "Banking" (open sort, 11 of 18) | Funding, inside Payroll setup | Users' word |
| Category | Time off | "Time off" (open sort, 13 of 18); "PTO" 410 and "vacation" 260 search queries in 90 days | Leave | "Leave" was used by 2 of 18. PTO and vacation become search synonyms |
| Category | People and access | "Team" (9 of 18); "Permissions", "Access" (7 of 18) | Users | "Team" was the more common word and was not used, because the global rail already says "People" for the directory and a third name would split the concept further; see section 8 |
| Page | Accounting and apps | "Accounting" (6 of 18); "Integrations", "Apps" (4 of 18) | Connected apps | Relabelled after T6 failed; the re-test is open |
| Page | Year-end forms | "tax forms" (380 search queries in 90 days) | Tax documents | The forms' legal names stay on the page itself; the navigation label uses the plain term |

Search synonyms: "biweekly", "pay frequency" and "pay day" map to Pay schedule
Search synonyms: "PTO", "vacation" and "holiday allowance" map to Time off > Policies
Search synonyms: "direct deposit" and "employee bank" map to Banking > Employee bank details
Search synonyms: "ledger", "accounting" and "sync" map to Accounting and apps

(All search counts ILLUSTRATIVE.)

## 7. URLs and deep links

| Node type | URL pattern | Example | Stable part | Changes when relabelled? |
|---|---|---|---|---|
| Settings page | `/settings/{page-key}` | `/settings/pay-schedule` | The page key, set once at this restructure. The category is shown in the breadcrumb and kept out of the path, so moving a page between categories changes no URL | No |
| Employee record section | `/people/{employee-id}/{section-key}` | `/people/e_48213/payment` | Employee id and section key | No |

The old tree put category labels in its paths, which is why every row below exists. This restructure is the last time a key follows a label.

Inbound links counted: help articles 212, support macros 31, email templates 9, mobile app deep links 4, partner integrations 0 (ILLUSTRATIVE), updated by Joanna Pell, support content lead, before 2026-12-01, a week ahead of the 2026-12-08 launch
Deep link without permission: the page title, the line "Only payroll admins can change this", and the names of the account's payroll admins. The URL stays as it was, so the person can forward it to an admin.

| Old URL | New URL | Redirect status code | Kept until |
|---|---|---|---|
| `/settings/payroll-setup/schedule` | `/settings/pay-schedule` | 308 | 2027-12-08 |
| `/settings/payroll-setup/funding` | `/settings/funding-account` | 308 | 2027-12-08 |
| `/settings/payroll-setup/advanced` | `/settings/pay-schedule` | 308 | 2027-12-08 |
| `/settings/compliance/registrations` | `/settings/tax-registrations` | 308 | 2027-12-08 |
| `/reports/tax-documents` | `/settings/year-end-forms` | 308 | 2027-12-08 |
| `/settings/leave/policies` | `/settings/time-off` | 308 | 2027-12-08 |
| `/settings/company-profile/integrations` | `/settings/accounting-apps` | 308 | 2027-12-08 |
| `/settings/users` | `/settings/admins` | 308 | 2027-12-08 |

## 8. Risks and open questions

| Risk or question | Owner | Due | Register row |
|---|---|---|---|
| "People" in the global rail and "People and access" in Settings may read as one place: T7's most common wrong destination was People > employee record (4 of 40), where participants looked for permissions | Felix Oduya, design lead | 2026-11-12, checked in the T6 re-test round | R-31 |
| The 212 help articles carry screenshots and written paths that redirects do not fix | Joanna Pell, support content lead | 2026-12-01 | R-32 |
| No tree test measures habit. Existing admins who learned the old tree may slow down even where new users speed up | Marisol Achterberg | Weekly for eight weeks from 2026-12-08: attempts on redirected paths, and `where-is` tickets by task | R-33 |
| [OPEN: T6 round 2 result; Rhiannon Okafor, research lead, owns it, due 2026-11-12] | Rhiannon Okafor | 2026-11-12 | R-34 |

## 9. How this file passes while the structure is wrong

Read before the Gate 3 review. Three rows of the template's table applied here; the others were checked and did not.

| Failure | The tell | What happened here |
|---|---|---|
| Leading tree-test tasks | A task's text contains its destination's label | T5's first draft said "year-end forms". Rewritten on 2026-09-09, before the run |
| Search as the fix for a failed task | "They can search for it" written against a failed row | Proposed for T6 in the review on 2026-09-24 and refused. T6 stays a fail with a relabel and a re-test; its synonyms are a second route, recorded separately in section 6 |
| Moving a habituated audience without a transition | Existing users' tickets rise after launch while new users do fine | Not testable before launch, so it is risk R-33 with a weekly reading, and the redirects are kept for a year |

## Exit gate

- [x] Every top task in section 1 cites a source of evidence, not a meeting (support tag counts, with search logs as a cross-check)
- [x] The inventory states its total, how it was produced, and a decision for every item (71 items from the route list; the full file is named in section 2)
- [x] Every card-sort and tree-test percentage is written as k of n, and the agreement formula used is named (pairwise and placement agreement, adjusted Wald intervals)
- [x] The closed sort's contested threshold and the tree test's pass rule each carry a date earlier than the run they judge (2026-08-20 before 2026-08-25; 2026-09-08 before 2026-09-14)
- [x] Every tree-test task names its correct destination, is phrased without that destination's label, and reports success with its interval, directness and first click
- [x] Every task that did not pass has a decision, and every accepted fail names its approver (T3 passed on re-test; T6 is waived by Marisol Achterberg with its re-test open; T5 is accepted on the line)
- [x] Every top task has a path with a step count and a second route
- [x] Every new or changed label cites the words users used, with a count and a source
- [x] Every URL that changes has a redirect row with a keep-until date, and the deep-link-without-permission behaviour is written
- [x] The design review record cites section 4's results, and the accessibility checklist cites section 5 for navigation consistency and multiple ways (both in the product workspace, not tracked in this repository)

Signed: Marisol Achterberg, Product Manager, Settings, 2026-10-28
