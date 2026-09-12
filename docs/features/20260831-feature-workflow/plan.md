# Feature workflow plan

Feature: [feature.md](feature.md)

Status: implemented

Phase: code review

Current step: wait for approval to prepare commits; version changes remain deferred

## Approach

Add three focused skills instead of one large orchestrator.

Keep the artifact rules with the `feature` skill, the gate contract with `feature-review` and backlog state management with `backlog`.

Package feature lifecycle skills in `workflow`, daily shared skills in `core` and optional `council` review in `thinking`.
Use `humanify` when it is available and keep the same focused prose pass as a fallback.

Use this repository change as the first feature that follows the new document structure.

Finish the PR flow by making artifact closeout, branch preparation, commit, push, PR creation and final handoff ordering explicit.
Keep the final review result and allowed plan state updates local until the verdict passes.
Allow their final handoff commit to preserve the verdict with a fresh CI result.

Add one human guide beside the `feature` skill.
Keep the root README short and link to the guide instead of copying the workflow.

## Steps

- [x] Add the feature contract and plan structure – AC1
- [x] Add `feature` with human approval, `humanify` and scope interruption rules – AC1, AC2, AC3 and AC7
- [x] Add `feature-review` with plan, code and PR gates – AC4 and AC5
- [x] Add `backlog` with stable IDs and closed decisions – AC3
- [x] Split the repository into `core`, `workflow` and `thinking` plugins, add distinct visual metadata and avoid a hard
      cross-plugin dependency – AC6 and AC8
- [x] Use compact `YYYYMMDD` feature folders and Markdown tasks in plans – AC1
- [x] Replace the backlog table with prioritized Markdown tasks – AC3
- [x] Run skill, marketplace, documentation and diff checks – AC1 through AC8
- [x] Add review-only defaults, a deterministic resolver and project override rules without changing development sessions – AC9
- [x] Verify the config schema, skill behavior, marketplace packages and repository diff – AC9
- [x] Add the `code-review.md` format and reset rules to a `feature-review` reference – AC10
- [x] Make `feature-review` create the file for code and PR reviews, preserve replies during focused follow-ups and replace it
      when a new full review starts – AC10
- [x] Make `feature` guide the primary agent to read findings, add short replies and hand the file back for a recheck – AC10
- [x] Add visible plan, code and PR gate verdicts and define when a checkbox opens or closes – AC10
- [x] Test the review file through an independent code review and focused follow-up – AC10
- [x] Use high effort for full reviews and medium effort for focused follow-ups – AC9
- [x] Move the complete default reviewer profile into `default` and keep other reviewers as overrides – AC9
- [x] Keep review processes alive until completion and support a verbatim handoff from read-only reviewers – AC10
- [x] Map each review verdict to one valid file status – AC10
- [x] Record active review state before each gate starts and mark it incomplete when it cannot finish – AC11
- [x] Check each candidate finding before it enters the review handoff – AC11
- [x] Stop a repeated blocker or major disagreement for a human decision – AC11
- [x] Add standard and stress review mode selection with clear risk triggers and perspective selection – AC12
- [x] Add independent general and named risk perspectives with one shared baseline for plan and code gates – AC12
- [x] Add source-scoped stable IDs and a primary-owned combined result for stress reviews – AC12
- [x] Keep incomplete state and focused rechecks separate for each required perspective – AC12
- [x] Combine both results without voting or separate synthesis and verification agents – AC12
- [x] Forward-test a split verdict, missing perspective, disputed-major stop and stress PR request before rerunning repository
      checks – AC12
- [x] Add the six staged phases and one-phase continuation rules – AC13
- [x] Add focused invalidation rules for scope, plan, code and PR changes – AC13
- [x] Add short chat phase reports without another durable artifact – AC13
- [x] Require a named external action before bare continuation authorizes it – AC6 and AC13
- [x] Clear stale approvals, verdicts and pending actions when work reopens – AC13
- [x] Keep blockers durable and prevent phase advance until they are cleared – AC13
- [x] Reset status and the current step for each reopened phase – AC13
- [x] Define legacy phase inference and keep reconstructed history outside live phase state – AC13
- [x] Forward-test phase advance, correction, reopening and external-action cases – AC13
- [x] Close local artifacts before branch, commit, push and PR actions and request each action separately – AC14
- [x] Keep PR review handoff changes and allowed plan state updates local until the verdict passes – AC15
- [x] Allow the final handoff and verified plan state updates to preserve the PR verdict and require final CI – AC16
- [x] Align `feature/SKILL.md`, `feature/references/phases.md` and the `feature-review` handoff with the final PR sequence – AC14,
      AC15 and AC16
- [x] Add `plugins/workflow/skills/feature/README.md` with the Mermaid pipeline, artifacts, human checkpoints, review modes,
      triggers, verdicts and stop rules – AC17
- [x] Keep the root README focused and add only a short link to the feature guide – AC17
- [x] Forward-test artifact closeout, source-branch resolution, separate branch, commit, push and PR approvals, PR review on the
      pushed head, the final handoff commit and push, final CI and merge approval – AC14 through AC16
- [x] Forward-test review mode triggers, the unsupported stress PR request and the expected phase, checkpoint and stop-rule paths
      in the human guide – AC17
- [x] Run skill, marketplace, documentation and whitespace checks – AC14 through AC17
- [x] Check review start, passing verdict, final handoff, release entry and mixed plan changes against the narrow state
      exception – AC15 and AC16

## Gates

- [x] Plan review – PASS (stress: general + human control)
- [x] Code review – PASS (prior stress baseline plus focused PR state exception check)
- [ ] PR review – not run

## Verification

- `feature`, `feature-review` and `backlog` contain the approved workflow boundaries
- Direct, indirect, incomplete-input, non-match and blocking-prerequisite cases were checked
- The PR gate returns `INCOMPLETE` when the PR head, full diff or CI evidence is unavailable
- Provider choice stays outside the shared skill instructions
- Review model and effort apply only to independent review sessions
- Project overrides use `.codex/feature-review.json` or `.claude/feature-review.json` and no user-level file
- Codex and Claude overrides resolve from the local files in the skills and Fuku projects
- `workflow` installs and exposes all four lifecycle skills without `core`
- Each Codex plugin manifest points to its own icon and accent color
- The focused prose fallback keeps feature artifacts usable when `humanify` is unavailable
- Every feature folder uses `YYYYMMDD-<slug>` and every plan tracks implementation with Markdown tasks
- The backlog keeps High, Medium and Low tasks in order and preserves rejected decisions at the bottom
- The Fuku test kept Codex read-only, saved its returned review verbatim and changed only feature artifacts
- An active plan, code or PR review is visible before its verdict returns
- A stopped or partial review is `INCOMPLETE` and cannot look like a clean result
- A finding is not published without a reachable trigger, concrete impact and a reviewed plan or change that causes, worsens or
  misses required behavior
- A blocker or major that stays open without an evidence-based answer after one focused recheck stops for a human decision
- Standard review still starts one reviewer and does not pay the stress review cost
- Stress plan and code reviews keep general and named risk findings independent until both return
- An active plan review shows its target, mode and source-specific status, round, reviewer, model and effort
- The primary records the named perspective selected from the highest-impact risk before both reviews start
- General and risk findings use separate stable ID namespaces and keep an immutable source
- The primary owns the combined result and each reviewer rechecks only its own open IDs
- One verified blocker or major keeps a stress gate open and a missing required perspective makes it `INCOMPLETE`
- Stress review does not add a second PR reviewer or separate synthesis and verification agents
- A stress PR request requires a human choice and is not silently downgraded
- Stress code reviewers use the caller-provided baseline and do not read the combined handoff
- Each tracked feature has one durable phase in `plan.md`
- `LGTM`, `continue` and `next` advance exactly one recorded phase while a named phase wins
- Phase transitions require a complete phase, passed checks and gates and a ready report
- A named phase can enter only the next eligible phase and cannot bypass a prerequisite
- Questions and informational corrections do not advance the workflow
- Semantic feature, plan, code and PR changes reopen only the affected phase and downstream work
- Reopening clears affected approvals, verdicts, checkboxes and pending actions
- Reopening also resets status and the current step to the affected phase
- A blocker keeps a durable reason and resume point and prevents phase advance until cleared
- A chat report shows the phase result, checks, human input and exact next action without creating another artifact
- Phase approval never authorizes an external action
- Bare `continue` authorizes one named external action without changing phase only when the prior report requested it
- Merge and release need separate approval
- Legacy live plans choose the earliest unfinished phase and ambiguous evidence moves to the earlier phase
- `Reconstruction:` identifies a historical backfill that has no live phase
- PR preparation closes artifacts and resolves the intended source branch before commit, push or PR actions
- Each branch, commit, push and PR action has its own approval and exact next step
- PR review uses the pushed head after required CI while the handoff and allowed plan state updates remain local
- A final head change limited to the handoff and allowed plan state updates keeps the PR verdict but still waits for required CI
- The exception covers only verified lifecycle fields and review gate state in the same feature's plan
- Any change outside the exception, including mixed state and semantic plan edits, reopens the PR gate
- The independent PR state exception check passed direct, indirect, missing-CI, routine-edit and mixed-plan-change cases
- The focused check traced review start, PASS, final handoff, final CI and release entry without a review loop
- The focused check simulated instructions and did not run a live PR review or replace the prior full branch review
- Mermaid CLI `11.17.0` rendered the guide's chart and the visual preview showed every phase and review loop
- An independent five-case behavior pass checked direct, indirect, incomplete, non-match and edge requests – PASS
- The human guide matches the implemented phase, review mode, trigger, verdict and convergence contracts
- The root README links to the guide without copying its detailed flow
- `make test` – passed
- `make validate` – passed
- `make docs` – passed
- `git diff --check` – passed

## Rollout and rollback

Release the skills after the implementation commit, separate version bump and PR review.

Projects opt in by invoking a skill and adding their first feature artifact or backlog entry.

Rollback removes the new skills and their documentation without changing existing project code or artifacts.
