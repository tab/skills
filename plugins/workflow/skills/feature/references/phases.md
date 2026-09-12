# Feature phases

Use this guide to keep feature work visible and let the human check each result before the next phase starts.

## Durable state

Active feature work uses one of these `Phase` values in `plan.md`:

- `feature`
- `plan`
- `build`
- `code review`
- `pr review`
- `release`

Store the phase that is active or waiting for approval.
Keep `Current step` specific enough to resume without chat history.

New tracked work starts with:

```markdown
Status: draft

Phase: feature

Current step: define and approve the feature contract
```

A backfilled historical plan uses a `Reconstruction:` field and does not use `Phase` because it did not run through this live
workflow.
When new work changes that feature, remove `Reconstruction:` and reopen `feature`.

An existing live plan without `Phase` gets one when the `feature` workflow next resumes it.
Choose the earliest unfinished phase in this order:

1. Use `feature` when the feature contract is incomplete or the plan has no complete approach, tasks and verification
2. Use `plan` when its current plan gate or final human approval cannot be verified
3. Use `build` when approved implementation work or required local checks remain
4. Use `code review` when the current code gate has not passed
5. Use `pr review` when the current PR gate has not passed or the change is not merged
6. Use `release` when merge is verified and release or rollout work remains

When evidence conflicts, choose the earlier phase and name the evidence that must be confirmed.
Do not treat an old status, verdict or chat message as fresh approval.

## Work one phase at a time

Complete one phase per response by default.
At the phase boundary, update `plan.md`, return one short report and stop.

Use this report and omit empty sections:

```markdown
## <Phase>

Status: <ready, blocked or complete>

Flow: <completed, current and remaining phases>

Result:

- <What is now true>

Checks:

- <Check and result>

Needs you:

- <Decision or manual check>

To continue:

- <One exact next phase or action>
```

Keep detailed evidence in the artifacts, code or review handoff.
Do not store phase reports as a new file or append them to `plan.md`.

Optional progress updates may announce phase entry, a material result or a blocker.
Do not report every command.

## Advance safely

Enter the next phase only when the current phase is complete, its required checks and gates pass and its report says it is ready.
An active or incomplete review, failed check or blocker keeps the current phase.

At a ready phase boundary:

- `LGTM`, `continue` or `next` approves the result and enters only the next eligible phase
- An explicit phase name requests that phase but can enter only the next eligible phase after its prerequisites pass
- A question or informational correction keeps the current phase
- A named repository or external action authorizes only that eligible action

Phase approval and selection do not authorize a gated repository or external action.
Do not skip an unfinished phase because the human named a later phase.

When the report names one exact gated action under `To continue`, bare `continue` authorizes only that action.
It does not also change the phase.
This exact action prompt takes precedence over the phase meaning of `continue`.

Ask for separate approval before each later gated action.
For example, switching a branch, committing, pushing, opening a PR, merging and publishing a release are separate actions.

## Reopen affected work

A semantic change invalidates the affected result even when its earlier review passed.

- A semantic change to `feature.md` reopens `feature` and every downstream phase
- A semantic plan or verification change reopens `plan` and affected downstream phases
- A code change after code review reopens `code review` and affected downstream phases
- A PR head or CI change after PR review reopens `pr review` and affected downstream phases, except for the allowed handoff
  changes defined below, which still require final CI

When work reopens, reset its durable state:

| Earliest phase | Status        | Current step                                   | Gates reset                 |
|----------------|---------------|------------------------------------------------|-----------------------------|
| `feature`      | `draft`       | update and approve the feature contract        | plan, code and PR           |
| `plan`         | `draft`       | update, review and approve the plan            | plan, code and PR           |
| `code review`  | `in progress` | run required checks and the current code gate  | code and PR                 |
| `pr review`    | `implemented` | run required CI and the current PR gate        | PR                          |

Also:

1. Clear approval for the affected phase and downstream phases
2. Reset each affected gate checkbox and verdict to `not run`
3. Clear any pending external action from the earlier report
4. Treat an existing `code-review.md` result as stale until the next full review replaces it
5. Run the required checks, review and human approval again

An editorial change that does not alter meaning does not reopen a phase.
Record an important semantic correction in the matching contract, assumption or decision instead of leaving it only in chat.

## Keep blockers durable

When a blocker stops the phase, set `Status: blocked` and record:

- The blocker and why it prevents progress
- The exact `Current step` to resume
- The required decision, evidence or prerequisite

Do not advance on a later continuation until the blocker is cleared.
If a separate prerequisite feature is needed, keep the original phase and resume point in this plan.

## Phase contract

### FEATURE

- Inspect current behavior, repository context and existing artifacts
- Define the goal, scope, expected behavior, acceptance criteria, assumptions and important contracts
- Run the focused prose pass on `feature.md`
- Set `Status: ready for approval` and wait for feature approval

### PLAN

- Write the approach, implementation tasks and verification against the approved feature contract
- Run the focused prose pass on both documents
- Complete the independent plan review and resolve accepted findings
- Set `Status: ready for approval` and wait for plan approval

### BUILD

- Set `Status: in progress` and implement only the approved scope
- Keep the current step, tasks, assumptions and decisions accurate
- Run available automated checks and record any required manual check
- Stop for a contract change, blocker or separate prerequisite

### CODE REVIEW

- Review the complete feature diff against the approved artifacts
- Use standard or stress review and resolve accepted findings through the review handoff
- Reopen the gate after every code change until its current verdict passes
- Set `Status: implemented` only after the code gate passes

### PR REVIEW

- Close out feature artifacts before branch, commit, push or PR actions
- Resolve the intended source branch, then ask separately before branch, commit, push and PR actions in that order
- Review the pushed PR head after required CI while the handoff and allowed plan state updates stay local
- Allow only `code-review.md` and current `Status`, `Phase`, `Current step` or review gate state in the same feature's `plan.md`
- Check the actual diff using the `feature-review` handoff rules, including the exclusion of mixed state and semantic changes
- After a passing verdict, record the PR gate result in the plan and ask separately to commit and push the allowed handoff changes
- Keep the verdict after that head change, but require final CI before merge approval
- Reopen the gate for any change outside this exception and repeat commit, push, CI and review
- Later allowed state updates may stay local until the next approved commit, and any later push requires final CI before merge
- After final CI passes, wait for human approval to enter `release`

### RELEASE

- After PR review approval, enter this phase and ask separately for merge approval
- Perform only the approved merge action
- Verify the merge before setting `Status: merged`
- Ask separately before publishing a release or starting another rollout action
- Verify the release before setting `Status: released` and `Current step: complete`
