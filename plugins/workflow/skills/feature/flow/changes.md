# Changes

Read this before you change an approved file, or when a change lands after a phase passed: what may change and what reopens.

## Reopen affected work

A semantic change invalidates the affected result even when its earlier review passed.
Before the PR opens:

- A semantic change to `feature.md` reopens `feature` and every downstream phase
- A semantic change to the steps or `Done when` reopens `plan` and affected downstream phases
- A code change after code review reopens `code review` and affected downstream phases

After the PR opens, nothing reopens in the files.
A fix is a normal commit pushed to the PR, and CI and any PR reviewer run on the new head.

When work reopens, reset its durable state:

| Earliest phase | Status        | Current step                                  | Gates reset   |
|----------------|---------------|-----------------------------------------------|---------------|
| `feature`      | `draft`       | update and approve the feature contract       | plan and code |
| `plan`         | `draft`       | update, review and approve the plan           | plan and code |
| `code review`  | `in progress` | run required checks and the current code gate | code          |

Also:

1. Clear approval for the affected phase and downstream phases
2. Reset each affected gate checkbox and verdict to `not run`
3. Clear any pending external action from the earlier report
4. Treat an existing `code-review.md` result as stale until the next full review replaces it
5. Run the required checks, review and human approval again.
   The primary agent reruns a reopened code gate without asking, as [the stretch](approvals.md#run-the-build-and-the-code-gate-as-one-stretch) says

An editorial change that does not alter meaning does not reopen a phase.
Record an important semantic correction in the matching contract, assumption or decision instead of leaving it only in chat.

## After approval

- `feature.md` is frozen once the human approves it
- Only the human changes it, or the primary agent proposes a change and the human approves it.
  The contract then returns to approval, as [Reopen affected work](#reopen-affected-work) says
- No agent polishes `feature.md` after approval
- In `plan.md`, the primary agent updates only the state: `Status`, `Phase`, `Current step`, `Blockers`, step checkboxes and gate lines
- Adding, removing or changing a step needs the human's approval.
  In the code gate, the primary agent may add a step to fix an accepted in-scope gate finding without it
- Delegated roles read both files and never edit them. The `architect` drafts them only before approval
- A better idea during the build goes to the backlog or to the human, never into the spec
- History lives in Git, not in the files
