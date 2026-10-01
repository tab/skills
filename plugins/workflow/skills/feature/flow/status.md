# Status

Read this before you start or resume tracked feature work: it says what `plan.md` records and how a blocker stops the work.

## Durable state

Active feature work uses one of these `Phase` values in `plan.md`:

- `feature`
- `plan`
- `build`
- `code review`
- `pr review`

Store the phase that is active or waiting for approval.
`RELEASE` holds only the human's merge and release actions, so no plan records it.
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

1. Use `feature` when the feature contract is incomplete or the plan has no complete steps and `Done when`
2. Use `plan` when its current plan gate or final human approval cannot be verified
3. Use `build` when approved implementation work or required local checks remain
4. Use `code review` when the current code gate has not passed
5. Use `pr review` when the code gate passed and `Status` is `implemented`. The PR, its CI and the merge live outside the files

When evidence conflicts, choose the earlier phase and name the evidence that must be confirmed.
Do not treat an old status, verdict or chat message as fresh approval.

## Keep blockers durable

When a blocker stops the phase, set `Status: blocked` and record:

- The blocker and why it prevents progress
- The exact `Current step` to resume
- The required decision, evidence or prerequisite

Do not advance on a later continuation until the blocker is cleared.
If a separate prerequisite feature is needed, keep the original phase and resume point in this plan.
