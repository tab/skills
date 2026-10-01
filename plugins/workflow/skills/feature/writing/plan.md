# Plan

Read this before you write or update `plan.md`: its steps, statuses, phase and gates.

`plan.md` answers which steps reach the goal, how we know it is done and where work resumes.

## Steps

- Write each step in one line
- Give a complex step two or three sub-bullets, never more
- Leave out the approach, file lists, proofs and acceptance criterion text.
  The brief of a delegated step names its files, as [the brief rules](../team/briefs.md) say
- Add `Blockers` only while a blocker stops the work, and remove it when the blocker clears
- Add `Rollout and rollback` only when release risk or staged rollout makes it useful

## Status and phase

Use one of these statuses:

- `draft`
- `ready for plan review`
- `ready for approval`
- `in progress`
- `blocked`
- `implemented`
- `stopped`

For active feature work, use one phase from [the durable state rules](../flow/status.md).

The files stop at the PR.
The last update comes before the push: `Status: implemented`, the code gate passed and `Current step` names the PR.
Nobody edits `feature.md` or `plan.md` after the PR opens. Keep `Done when` useful for later maintenance.
Historical plans may use `complete` as their `Current step`.
Use Markdown tasks for implementation steps.
Mark a task `[x]` when its work and required checks are complete.

## Gates

Keep the latest verdict beside each gate.
Use `<gate> – in review` while its reviewer is running.
Leave `CHANGES NEEDED` and `INCOMPLETE` unchecked.
Check `PASS`, or `PASS WITH FOLLOW-UPS` after each medium finding has a recorded disposition.
Reopen the checkbox when a later full review does not pass.
`plan.md` tracks two gates: plan review and code review.
The PR review runs on the PR itself and writes PR comments, never a file.

While a standard plan review runs, use:

```markdown
- [ ] Plan review – in review
  - Mode: standard
  - Target: <exact feature and plan revision>
  - Status: in review
  - Round: 1
  - Reviewer: <resolved reviewer>
  - Model: <resolved model>
  - Effort: <resolved effort>
```

While a risk review of the plan runs, use:

```markdown
- [ ] Plan review – in review
  - Mode: risk review
  - Target: <exact feature and plan revision>
  - General: in review, round 1, <reviewer>, <model>, <effort>
  - Risk perspective: <named perspective>
  - Risk: in review, round 1, <reviewer>, <model>, <effort>
```

Update the source status while the review runs.
After the gate returns its combined verdict, remove the active details and keep the short gate line.
