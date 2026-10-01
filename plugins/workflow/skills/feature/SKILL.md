---
name: feature
description: >
  Plan, build and review a tracked software feature with a clear contract, current plan and controlled scope.
  Use when the user wants to start, save, build or resume feature work that needs durable project context,
  or asks for a review of a feature plan or code gate or of its PR.
  Do not use for routine edits that need no lasting feature record.
---

# Feature

Guide a feature from an approved idea to release while keeping the human-readable contract and current plan in the repository.

Use `docs/features/YYYYMMDD-<slug>/feature.md` for what and why.
Use `docs/features/YYYYMMDD-<slug>/plan.md` for the steps, the done checks and current progress.
Use `docs/features/YYYYMMDD-<slug>/code-review.md` for the current code review handoff.

When the request is only to review a feature gate, read [the first review step](review/1-prepare.md) and follow it.
Run no phase and change no artifact except what the review files allow.
Otherwise read the writing rules before creating or materially rewriting either document:
[style](writing/style.md), [the folder](writing/folder.md), [`feature.md`](writing/feature.md) and [`plan.md`](writing/plan.md).
Read the flow rules before starting or resuming tracked feature work: [status](flow/status.md), [approvals](flow/approvals.md),
[changes](flow/changes.md) and the phase files, from [`1-feature.md`](flow/1-feature.md) to [`5-pr-review.md`](flow/5-pr-review.md).

## Roles

- The primary agent leads: it discusses, plans and decides
- It implements and fixes the feature itself or through the team
- One or two review agents independently review the plan and code, while CI and any PR reviewer check the PR
- The human owns scope and plan approval, a dispute the agents leave open, accepted risks, merge and release decisions

The shared skill instructions stay neutral between Claude Code and Codex.
The linked review config holds the default reviewer, model and effort.
The user, primary agent or an external runner starts each agent handoff.

Read the team rules before delegating a draft, a step or a pass: [rules](team/rules.md), [briefs](team/briefs.md)
and [steps](team/steps.md).

## Configure review handoffs

Read [the review settings](review/settings.md) and
[the bundled defaults](review/settings.json) before starting an independent review.
Resolve the linked script path from this `SKILL.md`, then run
[the review config resolver](scripts/resolve-review-agent.py) with the repository root and requested gate.

Use its JSON result as the reviewer, model and effort for the requested gate.
Do not infer or merge these values when the resolver is available.
Apply them only to a new review agent or session.
Never change the model or effort of the active development session.
Never describe the review values as the active development configuration.

Project overrides are optional and belong only in `.codex/feature-review.json` or `.claude/feature-review.json` at the
repository root.
Do not read a user-level or parent-directory override.
Do not create or change a project override unless the user asks.
If the resolver cannot run, follow the linked settings directly and report that fallback.

Read [the risk review rules](review/risk-review.md) when a risk needs a risk review or the human requests another
perspective.

Use the `humanify` skill for artifact cleanup when it is available.
Otherwise make the same focused prose pass directly and state that the fallback was used.

## Start or resume

Read the repository instructions, current code, nearby tests, documentation and existing feature artifacts before asking questions.

Resolve:

- The user-visible or developer-visible goal
- Current behavior and the reason for change
- In-scope and out-of-scope work
- Testable acceptance criteria
- Assumptions that affect the solution
- Contracts or compatibility boundaries
- Decisions already made and open questions that block planning

Ask only about material choices that cannot be verified.
Do not turn brainstorming into an approved contract until the user asks to start, plan or save the feature.

Use an existing matching feature folder instead of creating a duplicate.
When a new folder is needed, prefix a short lowercase hyphenated slug with the creation date in `YYYYMMDD` format.
Keep that original dated folder name when the feature is resumed or changed.
Historical reconstruction uses the separate `feature-backfill` workflow and its verified delivery date.

Store the active phase in `plan.md` and follow the continuation, invalidation and blocker rules of the `flow/` files.
If an active plan has no `Phase`, infer the earliest unfinished phase from current evidence and add it before continuing.
Do not treat an old status, verdict or chat message as fresh approval.
Complete one phase per response by default, return its short report and stop at its boundary.
Plan approval is the exception: the build and the code gate run as [one stretch](flow/approvals.md#run-the-build-and-the-code-gate-as-one-stretch).

## Choose the smallest workflow

Classify the change before creating documents:

- **Routine** – local low-risk work with no new behavior, contract or durable decision
- **Standard** – a user-visible change, several implementation steps or a choice future work must understand
- **Large or high-risk** – a standard feature with migration, security, data, compatibility or architecture risk

Routine work may use only the PR and release note unless the user asks for feature artifacts.
Standard work uses both feature documents.
Large or high-risk work uses both documents and adds an ADR only when a real long-lived decision needs separate treatment.

Use standard review unless the linked risk review rules identify a material risk or the human requests a risk review.
A risk review adds one named risk perspective to the plan and code gates.
It never adds another PR reviewer.

## FEATURE phase

Create or refactor `feature.md` from [the contract rules](writing/feature.md).
The primary agent may ask the `architect` for a draft and stays the author of what goes to the human.
For new tracked work, create the small `plan.md` header with `Phase: feature`, the current step and gates.
Keep each fact in one place and link to it elsewhere.

Before feature approval:

1. Remove unresolved questions that can be answered from current evidence
2. Ask the user to approve material scope or trade-offs that remain
3. Run the focused prose pass on `feature.md` without changing its meaning, facts or certainty
4. Set the plan status to `ready for approval` and name feature approval as the current step
5. Return the `FEATURE` phase report and wait for explicit approval

Do not write a detailed implementation plan before the feature contract is approved.
Do not enter `PLAN` while the goal, scope, required behavior or important contract is unclear.

## PLAN phase

After feature approval, set `Phase: plan`, change the status to `draft` and create or refactor the full `plan.md`.
The primary agent may ask the `architect` for a draft and stays the author of what goes to the human.

Before implementation:

1. Map the steps and `Done when` to the approved acceptance criteria
2. Run the focused prose pass on both documents without changing their meaning, facts or certainty
3. Set the plan status to `ready for plan review`
4. Choose standard review or a risk review and name the risk perspective when a risk review applies
5. Resolve the review-only configuration for each required review process
6. Record the active mode and perspective, then start the required independent plan review or reviews
7. Record `INCOMPLETE` and stop when any required review cannot finish or required evidence is missing
8. Resolve accepted findings and update the documents to current truth
9. Run the focused prose pass on changed text and return to plan review whenever any change affects semantic content
10. Record the combined plan verdict in `plan.md` and check the gate only when it passes
11. Set the plan status to `ready for approval` and name plan approval as the current step
12. Return the `PLAN` phase report and wait for explicit user approval

Semantic content includes the goal, why, scope, behavior, assumptions, contracts, decisions, steps and `Done when`.

Do not start while a blocker or major plan finding remains open.
Do not start without explicit user approval of the final reviewed plan.

## BUILD phase

After plan approval, set `Phase: build`, set the plan status to `in progress` and name one current step.

Implement only the approved scope.
Run [the step loop](team/steps.md), or implement directly when the host cannot delegate.
Commit each accepted step as a checkpoint, as [the commit rules](team/steps.md#commits) say.
After the last step, run the passes the step loop lists.
Update the plan state in place as the truth changes, as [the freeze rules](flow/changes.md#after-approval) allow.
Do not append a progress diary, review transcript or chat summary.

Map implementation and tests back to acceptance criteria.
If implementation proves the contract wrong or incomplete, stop and propose the change to the human before continuing.
After the planned work and available checks finish, enter `CODE REVIEW` in the same run, with no `BUILD` report.

## Control discoveries

Classify work found during implementation:

- **Required and in scope** – include it, and ask the human before adding or changing a plan step, except for a code gate fix
- **Useful but not required** – add or update a backlog item and continue the feature
- **Required prerequisite outside the current scope** – mark the plan `blocked`, record the exact resume point and handle the
  prerequisite as a separate feature
- **Not useful** – leave it out and do not grow the documents

Use the `backlog` skill when it is available.
Otherwise make the same compact update in `docs/features/backlog.md`.

A separate prerequisite must not silently expand the original feature.
Its completion returns control to the saved current step and verification state in the original plan.

## Review handoffs

Use the independent review agent at two gates:

1. Plan review before implementation
2. Code review after local verification and before opening the PR

`plan.md` tracks only these two.
The PR review runs on the PR and writes no file, as the `PR REVIEW` phase says.

Read [the first review step](review/1-prepare.md) and
[the code review rules](writing/code-review.md) before a code gate.
The brief of a gate reviewer carries the absolute path of `review/1-prepare.md`, resolved from this skill's own folder,
installed or local, so a reviewer in any working directory can read it.
That file links the rest of `review/` and `writing/code-review.md`.
When its file-reading tool is denied outside the project, the reviewer reads that file and the files it links with the shell.
The brief also gives each check command and its latest result, because a read-only reviewer may not be able to run it.
Resolve the review-only configuration before every gate and focused follow-up.
Use the linked risk review rules to select and run a risk review for plan and code gates.

**Claude Code only.** When the resolved reviewer is `claude` and the host ships the `code-reviewer` agent, start
`workflow:code-reviewer` with the resolved model and a brief that names the gate and the path of `review/1-prepare.md`.
Pass the resolved model on every start of the reviewer, a retry or a focused follow-up included.
The agent's effort is fixed in its definition, so compare it with the resolved effort.
At or above the resolved effort, run the review and record the agent's effort in the gate record's `Effort` field as the effort used.
Below it, or when the host cannot rank the two values, report both and let the human start the review.
After it returns and before you save its result, confirm that `git status` and `git diff` show the same as before it ran,
apart from the untracked output of a named check.

Record the active review before starting it.
Set the matching gate in `plan.md` to `in review`.
For the code gate, follow the linked handoff rules to record the round, target and review settings used in `code-review.md`.
For a focused follow-up, preserve the current findings and replies while marking the next round `in review`.

For a standard code gate, the review agent produces the current result for `code-review.md`.
Let it write the file only when the host can limit its write access to that handoff.
When the reviewer is read-only, require the complete file content and save it verbatim before processing findings.
The primary agent must not edit that review content during the handoff.

For a code risk review, both reviewers return independent source results and the primary agent owns the combined
`code-review.md` file.
Copy each result without changing its finding content and derive the verdict through the linked risk review rules.
Do not let either risk reviewer overwrite the combined file.

Keep the review process attached until it returns its verdict and handoff.
Do not start a background reviewer that will be stopped when the current turn or process exits.
When the host cannot keep it alive, return the resolved configuration and an exact command for the human or external runner.
When a started review or required risk review perspective stops or returns partial evidence, record `INCOMPLETE` with the
reason and keep the gate unchecked.
Do not treat findings from a partial review as a complete verdict.

Read every finding, make accepted fixes and add a short `Reply` with what changed or why the code should stay.
Commit each accepted fix as a checkpoint, as [the commit rules](team/steps.md#commits) say.
Do not change the reviewer's finding text, severity, location or suggested fix.
Hand the file and changed areas back to the review agent for a focused recheck.
Only one agent updates the file at a time.

For standard review, the review agent rewrites the whole file after each round and keeps stable finding IDs.
For a risk review, the primary agent replaces only the returned perspective in the combined file and keeps both sources visible.
Start the same gate again only when the user or primary agent asks.

Keep each gate unchecked while its latest verdict is `CHANGES NEEDED` or `INCOMPLETE`.
Check it after `PASS`, or after every medium finding from `PASS WITH FOLLOW-UPS` has a recorded disposition.
A later full review replaces the verdict and may reopen the gate.

`Current step` ends at the PR. The files never record the merge or the release.

The primary agent fixes every finding it accepts, of any severity, inside the approved scope.
It may add a plan step for such a fix without the human's approval.
A fix that changes `feature.md` or the scope is a contract change and goes to the human.
Minor or low-value disagreement does not start another review round.
After the primary disputes a finding of any severity with evidence, allow one focused recheck.
If the reviewer keeps it open without answering that evidence or adding material evidence, stop the agent loop.
Keep the gate open and ask the human to choose the next action.
A request to continue until the agents agree does not authorize more unchanged rounds.

## CODE REVIEW phase

After the build, set `Phase: code review` in the same run and run the code gate through the review handoff above.
Stop and ask the human only for a reason [the stretch](flow/approvals.md#run-the-build-and-the-code-gate-as-one-stretch) lists.
Before the PR opens, every code change after a review reopens this gate and needs a current verdict.

When the code gate passes, set the plan status to `implemented`, name PR preparation as the current step and return the
`CODE REVIEW` phase report.
Stop before entering `PR REVIEW` or performing any external action.

## PR REVIEW phase

After code review approval, set `Phase: pr review`.
Approval to enter this phase covers two local actions: the close-out checkpoint and the history rewrite.
It does not approve a branch other than the rewrite's backup branch, a push or PR action, or any other commit.

1. Close out the artifacts before the push. [The freeze rules](flow/changes.md#after-approval) say what may change
2. Confirm every acceptance criterion has implementation or verification evidence
3. Run the focused prose pass and read both documents once as a first-time contributor
4. Keep `Status: implemented` and name the PR as `Current step`. This is the last update of the files
5. Resolve the source branch from the approved plan, the current branch and project conventions.
   Ask the human when it cannot be resolved safely, and before creating or switching the source branch
6. Commit the close-out as a checkpoint
7. Rewrite the unpushed history into a few atomic commits and hand over the signing, as
   [the rewrite rules](flow/5-pr-review.md#rewrite-the-history) say
8. Ask separately for the push and the PR
9. CI and any PR reviewer run on the PR. They write PR comments, never a file
10. Fix an accepted finding with a new unsigned commit after the human's approval, and push it to the PR
11. The phase ends when the human approves the merge

The primary agent may ask the `technical-writer` for the PR title and body.
The human still approves each action.
Name only the next eligible action in the phase report and stop after performing it.
Nobody edits `feature.md`, `plan.md` or `code-review.md` after the PR opens.

## RELEASE phase

The human's merge approval enters this phase. No file records it.
Perform only the approved merge.
Request separate approval for a release or another rollout action.
Never infer merge or release from passing tests.
Change no file.

## Safety and boundaries

- Plan approval covers the checkpoint commits of the build and of the code gate fixes
- Entering `PR REVIEW` covers the close-out checkpoint and the history rewrite
- Never sign a commit, rewrite a pushed commit or delete the backup branch of a rewrite
- Do not create or switch a branch, apart from the backup branch of a rewrite,
  make any other commit, push, open or change a PR, merge, release or write to an external system
  without user approval
- Do not change code when the user asked only to discuss, plan or review
- During a code review, the review agent may change only `code-review.md`, or nothing when it is read-only.
  A PR reviewer changes no file
- Preserve unrelated working-tree changes and current project conventions
- If an independent agent is unavailable, say which review gate could not be independent and let the human choose whether to continue
