# Steps

Read this during the build: the loop for each step, what the lead verifies, the commits and what runs after the last step.

## The step loop

1. Brief a `developer` with the step and the model
2. Read its report and compare the files it touched with the step's files
3. Brief a `code-reviewer` with the model, the step, the developer's report, the lint,
   and the checks with their timeout and repeat count.
   Name the step's own changes by path from the developer's report, new files included.
   The step's diff starts at the last checkpoint
4. On `CHANGES NEEDED`, send the numbered required changes back to the same `developer`
5. On `ACCEPT`, verify the claims that decide the verdict, then tick the step and move `Current step`
6. Commit the step as a checkpoint, as [the commit rules](#commits) below say. The commit stays local

A step gets at most two `code-reviewer` rounds.
The second round covers only the first round's required changes and the regressions their fixes caused.
A new item in round two names the fix that caused it.

Before you tick a step, check:

- The evidence lists every named check in every repeat, and each one passed
- Every new test that matters killed its mutant, or the evidence says why no mutant could run
- The changed files match the step's files, or the developer's report says why the step needed each other file
- The step's changes meet the acceptance criterion. Read them yourself
- A check whose evidence looks doubtful passes when you rerun it
- `git status` and `git diff` show the same as before the `code-reviewer` ran, apart from the untracked output of a named check.
  Its rules forbid a shell write, but nothing blocks one

When the `code-reviewer` named the exact edit and it is a few lines, you may apply the required change yourself.
Anything larger returns to the `developer`.
The `code-reviewer` confirms that change in its recheck, like any other fix.

## Commits

The primary agent commits each accepted step and each accepted gate fix as a checkpoint:

- Commit after you tick the step or record the fix, so the checkpoint holds the plan state lines of that moment
- Commit with `git commit --no-gpg-sign`. The primary agent never signs
- Write a short title in the project's convention, using the `cmt` skill when it is available.
  That skill only drafts the message, and this rule makes the commit
- Plan approval covers these local commits

In `PR REVIEW`, [the history rewrite](../flow/5-pr-review.md#rewrite-the-history) groups the checkpoints into a few atomic
commits before the push.

## After the last step

Each of these runs as a step with its own `code-reviewer` round:

1. `qa` runs the coverage pass. The `coverage` skill defines the tiers and the measurement
2. The `technical-writer` brings the docs to the code
3. The primary agent runs the checks in the plan's `Done when`

Then set `Phase: code review` and start the code gate in the same run, as [the stretch](../flow/approvals.md#run-the-build-and-the-code-gate-as-one-stretch) says.

In `CODE REVIEW`, when the human asks, [the challenge pass](../review/challenge.md) follows a passing gate.
Brief `qa` to triage each of its findings.
For `FIX NOW`, the primary agent proposes a step and the human approves it.
`BACKLOG` becomes a backlog item and `DROP` is recorded with its evidence.
[The code review rules](../writing/code-review.md) define where each disposition lands in `code-review.md`.
