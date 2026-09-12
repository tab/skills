---
name: feature
description: >
  Plan, implement and continue a tracked software feature with a clear contract, current plan and controlled scope.
  Use when the user wants to start, save, build or resume feature work that needs durable project context.
  Do not use for review-only requests or routine edits that need no lasting feature record.
---

# Feature

Guide a feature from an approved idea to release while keeping the human-readable contract and current plan in the repository.

Use `docs/features/YYYYMMDD-<slug>/feature.md` for what and why.
Use `docs/features/YYYYMMDD-<slug>/plan.md` for how, proof and current progress.
Use `docs/features/YYYYMMDD-<slug>/code-review.md` for the current code or PR review handoff.

Read [the artifact guide](references/artifacts.md) before creating or materially rewriting either document.
Read [the phase guide](references/phases.md) before starting or resuming tracked feature work.

## Roles

- The primary agent discusses, plans, implements and fixes the feature
- One or two review agents independently review the plan and code, while one review agent checks the PR
- The human owns scope and plan approval, disputed medium findings, merge and release decisions

The shared skill instructions stay neutral between Claude Code and Codex.
The linked review config holds the default reviewer, model and effort.
The user, primary agent or an external runner starts each agent handoff.

## Configure review handoffs

Read [the review agent guide](references/review-agents.md) and
[the bundled defaults](references/review-agents.json) before starting an independent review.
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
If the resolver cannot run, follow the linked guide directly and report that fallback.

Read [the review perspective guide](references/review-perspectives.md) when a risk needs stress review or the human requests
another perspective.

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

Store the active phase in `plan.md` and follow the phase guide's continuation, invalidation and blocker rules.
If an active plan has no `Phase`, infer the earliest unfinished phase from current evidence and add it before continuing.
Do not treat an old status, verdict or chat message as fresh approval.
Complete one phase per response by default, return its short report and stop at its boundary.

## Choose the smallest workflow

Classify the change before creating documents:

- **Routine** – local low-risk work with no new behavior, contract or durable decision
- **Standard** – a user-visible change, several implementation steps or a choice future work must understand
- **Large or high-risk** – a standard feature with migration, security, data, compatibility or architecture risk

Routine work may use only the PR and release note unless the user asks for feature artifacts.
Standard work uses both feature documents.
Large or high-risk work uses both documents and adds an ADR only when a real long-lived decision needs separate treatment.

Use standard review unless the linked perspective guide identifies a material risk or the human requests stress review.
Stress review adds one named risk perspective to the plan and code gates.
It never adds another PR reviewer.

## FEATURE phase

Create or refactor `feature.md` from the artifact guide.
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

Before implementation:

1. Map the approach, steps and verification to the approved acceptance criteria
2. Run the focused prose pass on both documents without changing their meaning, facts or certainty
3. Set the plan status to `ready for plan review`
4. Choose standard or stress review and name the risk perspective when stress review applies
5. Resolve the review-only configuration for each required review process
6. Record the active mode and perspective, then start the required independent plan review or reviews
7. Record `INCOMPLETE` and stop when any required review cannot finish or required evidence is missing
8. Resolve accepted findings and update the documents to current truth
9. Run the focused prose pass on changed text and return to plan review whenever any change affects semantic content
10. Record the combined plan verdict in `plan.md` and check the gate only when it passes
11. Set the plan status to `ready for approval` and name plan approval as the current step
12. Return the `PLAN` phase report and wait for explicit user approval

Semantic content includes the goal, context, scope, behavior, assumptions, contracts, decisions, approach, steps and verification.

Do not start while a blocker or major plan finding remains open.
Do not start without explicit user approval of the final reviewed plan.

## BUILD phase

After plan approval, set `Phase: build`, set the plan status to `in progress` and name one current step.

Implement only the approved scope.
Update the existing status, current step, assumptions and decisions in place as the truth changes.
Do not append a progress diary, review transcript or chat summary.

Map implementation and tests back to acceptance criteria.
If implementation proves the contract wrong or incomplete, stop and update the contract before continuing.
After the planned work and available checks finish, return the `BUILD` phase report and stop before code review.

## Control discoveries

Classify work found during implementation:

- **Required and in scope** – include it and update the plan when needed
- **Useful but not required** – add or update a backlog item and continue the feature
- **Required prerequisite outside the current scope** – mark the plan `blocked`, record the exact resume point and handle the
  prerequisite as a separate feature
- **Not useful** – leave it out and do not grow the documents

Use the `backlog` skill when it is available.
Otherwise make the same compact update in `docs/features/backlog.md`.

A separate prerequisite must not silently expand the original feature.
Its completion returns control to the saved current step and verification state in the original plan.

## Review handoffs

Use the independent review agent at three gates:

1. Plan review before implementation
2. Code review after local verification and before opening the PR
3. PR review on the current PR head after CI and accepted fixes

Read the `feature-review` skill and its linked code review handoff before starting a code or PR gate.
Resolve the review-only configuration before every gate and focused follow-up.
Use the linked perspective guide to select and run stress review for plan and code gates.

Record the active review before starting it.
Set the matching gate in `plan.md` to `in review`.
For code and PR gates, follow the linked handoff rules to record the round, target and resolved review settings in `code-review.md`.
For the PR gate, use the linked handoff's narrow exception for lifecycle and gate state updates in `plan.md`.
For a focused follow-up, preserve the current findings and replies while marking the next round `in review`.

For a standard code or PR gate, the review agent produces the current result for `code-review.md`.
Let it write the file only when the host can limit its write access to that handoff.
When the reviewer is read-only, require the complete file content and save it verbatim before processing findings.
The primary agent must not edit that review content during the handoff.

For a stress code gate, both reviewers return independent source results and the primary agent owns the combined
`code-review.md` file.
Copy each result without changing its finding content and derive the verdict through the linked perspective guide.
Do not let either stress reviewer overwrite the combined file.

Keep the review process attached until it returns its verdict and handoff.
Do not start a background reviewer that will be stopped when the current turn or process exits.
When the host cannot keep it alive, return the resolved configuration and an exact command for the human or external runner.
When a started review or required stress perspective stops or returns partial evidence, record `INCOMPLETE` with the reason and
keep the gate unchecked.
Do not treat findings from a partial review as a complete verdict.

Read every finding, make accepted fixes and add a short `Reply` with what changed or why the code should stay.
Do not change the reviewer's finding text, severity, location or suggested fix.
Hand the file and changed areas back to the review agent for a focused recheck.
Only one agent updates the file at a time.

For standard review, the review agent rewrites the whole file after each round and keeps stable finding IDs.
For stress review, the primary agent replaces only the returned perspective in the combined file and keeps both sources visible.
A new PR review replaces the earlier code review.
Start the same gate again only when the user or primary agent asks.

Keep each gate unchecked while its latest verdict is `CHANGES NEEDED` or `INCOMPLETE`.
Check it after `PASS`, or after every medium finding from `PASS WITH FOLLOW-UPS` has a recorded disposition.
A later full review replaces the verdict and may reopen the gate.

Do not set `Current step` to `complete` while a required review, merge or release step remains.

The primary agent fixes accepted blocker, major and clear in-scope medium findings.
The human chooses the disposition of disputed medium findings.
Minor or low-value disagreement does not start another review round.
After the primary disputes a blocker or major with evidence, allow one focused recheck.
If the reviewer keeps it open without answering that evidence or adding material evidence, stop the agent loop.
Keep the gate open and ask the human to choose the next action.
A request to continue until the agents agree does not authorize more unchanged rounds.

## CODE REVIEW phase

After build approval, set `Phase: code review` and run the code gate through the review handoff above.
Every code change after a review reopens this gate and needs a current verdict.

When the code gate passes, set the plan status to `implemented`, name PR preparation as the current step and return the
`CODE REVIEW` phase report.
Stop before entering `PR REVIEW` or performing any external action.

## PR REVIEW phase

After code review approval, set `Phase: pr review`.
Do not treat approval to enter this phase as approval for a branch, commit, push or PR action.

Before requesting any of those actions, close out the documents:

- Make contracts and assumptions match the implementation
- Record material deviations as current decisions
- Remove stale questions and temporary notes
- Confirm every acceptance criterion has implementation or verification evidence
- Run the focused prose pass to remove repetition and unclear or AI-style wording without changing meaning
- Read both documents once as a first-time contributor

Then confirm the intended source branch from the approved plan, current branch and project conventions.
Ask the human when it cannot be resolved safely.

Prepare the PR in this order and request separate approval for each action that is needed:

1. Create or switch to the intended source branch
2. Commit the closed-out implementation and artifacts
3. Push the source branch
4. Open or update the PR

Name only the next eligible action in the phase report and stop after performing it.
Branch and commit actions are local repository changes.
Push and PR actions change an external system.

Wait for required CI, then run the standard PR gate on the pushed PR head.
Keep `code-review.md` and allowed `plan.md` state updates local while the review and focused follow-ups run.
The exception covers only `Status`, `Phase`, `Current step` and review gate checkboxes or verdicts that record current workflow state.
It does not cover changes to scope, decisions, implementation tasks, verification or approval requirements.
Inspect the actual diff before applying the exception, as defined in the `feature-review` handoff.
Do not include other unpushed implementation or artifact changes in the review evidence.

When an accepted fix changes implementation or artifacts outside this exception, request separate commit and push approvals,
wait for required CI and reopen the PR gate on the new head.
Any change outside the exception invalidates the earlier PR verdict.

After the PR gate passes, record its result in `plan.md` and check the complete diff against the reviewed head.
The final handoff may contain `code-review.md` and only the allowed state updates in `plan.md`.
Request separate approval to commit that handoff, then request separate approval to push it.
This handoff head change keeps the PR verdict and does not start another review round.
Do not rewrite the recorded review target to the handoff commit.
Wait for required CI on the final head.
If the diff includes any other change, reopen the PR gate instead.

After final CI passes, name PR review approval as the current step, return the `PR REVIEW` phase report and stop.
Later allowed state updates, including entry into `release`, keep the verdict and may stay local until the next approved commit.
Any later push still needs required CI on its final head before merge.
Do not request merge approval until the human approves this phase and the workflow enters `RELEASE`.

## RELEASE phase

After PR review approval, set `Phase: release`.
Request approval for merge and perform only that external action.
Verify the merge before setting the plan status to `merged`.

Request separate approval for a release or another rollout action.
Set the plan status to `released` and `Current step` to `complete` only after the release is verified.

Set status to `implemented`, `merged` and `released` only when each event has happened.
Never infer merge or release from passing tests.

## Safety and boundaries

- Do not create or switch a branch, commit, push, open or change a PR, merge, release or write to an external system without user
  approval
- Do not change code when the user asked only to discuss, plan or review
- During a code or PR review, the review agent may change only `code-review.md`, or nothing when it is read-only
- Preserve unrelated working-tree changes and current project conventions
- If an independent agent is unavailable, say which review gate could not be independent and let the human choose whether to continue
