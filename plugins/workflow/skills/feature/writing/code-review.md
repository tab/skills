# Code review

Read this when a code review starts, gets replies, is rechecked or starts again: it owns the rules of `code-review.md`.

Use `docs/features/YYYYMMDD-<slug>/code-review.md` for the current code review.
Do not use it for the plan gate or the PR review.
The PR review writes PR comments and no file, as [the PR report](../review/4-report.md#pr-review) says.

`code-review.md` is a short handoff between the primary and review agents during code reviews.
It stores the current target, round, findings, replies, rechecks, checked evidence and verdict.

The review agent produces and rewrites the file for a standard review.
For a code risk review, the primary agent owns the combined file and copies both independent result sets into it,
as [the risk review](../review/risk-review.md) says.
Before a review starts, the primary agent or reviewer that can write the file records its active round, target and resolved review
settings.
When it is read-only, the primary agent may save the complete returned content verbatim before adding any reply.
The primary agent adds a short `Reply` under each finding after making a fix or deciding the code should stay.
Only one agent updates the file at a time.

Keep current state instead of an appended conversation.
Do not turn the file into a chat transcript or implementation diary.
[The template](../templates/code-review.md) shows its shape. It is `templates/code-review.md` in the `feature` skill folder.

## Start a review

Record the active review before it starts.
The primary agent or external runner records it when the reviewer is read-only.
The reviewer records it when write access is limited to this file.

For a new standard review, replace the old file with the header of [the template](../templates/code-review.md).
Set `Status: in review`.
Set `Round: 1` for the first review of the gate, after a reopen of `feature` or `plan` or when the human asks to start again.
Otherwise set the next round number.

Record the reviewer, model and effort values used to start the review.
For a direct invocation, use the current review session values when available and `not reported` for values the host does not expose.
If the host reports a different runtime model, record that mismatch under `Checked` instead of adding another header field.

For a focused standard follow-up, preserve findings and replies, set `Status` to `in review` and increment `Round` before launch.
Do not change the finding text while recording the active round.

For a plan gate, the `feature` workflow records the active state in `plan.md` instead of creating this file.

## First review

The review agent creates or replaces the whole file for a new full code review.
When it is read-only, it returns the complete file content and the primary agent or external runner saves it verbatim.
It records the target, current round, findings, checked evidence and verdict.

Use the shape of [the template](../templates/code-review.md): the header, `Findings`, `Checked` and `Verdict`.

Use `CODE-1`, `CODE-2` and later IDs.
The plan gate returns its review directly and does not write this file.
Keep the target and resolved review settings from the active state in the completed file.

Use these file statuses:

- `in review` while the review has no verdict
- `changes needed` for `CHANGES NEEDED`
- `follow-ups` for `PASS WITH FOLLOW-UPS`
- `passed` for `PASS`
- `incomplete` for `INCOMPLETE`

Do not use finding states such as `fixed` or `resolved` as the file status.

When a started review stops or returns partial evidence, use `Status: incomplete` and `INCOMPLETE` as the verdict.
Record the reason under `Checked` and preserve existing findings and replies when a focused follow-up fails.
An incomplete review never passes the gate.

Use blocker, major or medium severities from [the finding contract](../review/3-findings.md#finding-contract).
Do not add minor or style-only findings.
For a risk review, apply the same status values to each source and derive the overall status only after both sources finish.

## Reply

The primary agent reads each finding, makes accepted changes and adds a short reply under it.
After a fix, it writes `Reply: Fixed by <short change and evidence>`.
When the code should stay, it writes `Reply: Kept because <short evidence>`.

The primary agent may set the finding status to `fixed`, `disputed`, `backlog` or `accepted risk`.
`backlog` must include the backlog ID.
`accepted risk` needs the human's decision.

Do not change the finding, severity, location or suggested fix while replying.

## Recheck

On a focused follow-up, the review agent reads the current file, replies and changed areas.
It checks only open finding IDs and regressions caused by their fixes.

In a risk review, each reviewer receives only findings, replies and related changes from its own source.
It does not read the combined handoff.
The primary agent copies the returned source result into the combined file and leaves the other source unchanged.

For a finding that stays open, add a short line: `Recheck: Still open because <current evidence>`.
Move closed findings to a compact `Resolved` section, one line each: `- CODE-1 – resolved: <short evidence>`.

Rewrite the whole file with the current state after every recheck.
Preserve the meaning of the primary agent's reply while its finding remains open.
Keep the active `Round` value when the review agent completes the pass.

## Start again

A new full review of the same gate replaces the file only when the user or primary agent asks to start again.
Deleting the file also starts again, but never delete it without clear user approval.

Do not review `code-review.md` as implementation code.
Check only that it matches the current review state.

## Follow-up passes

A [challenge pass](../review/challenge.md) adds this section after `## Verdict`.
The primary agent writes it after the triage.
The reviewer of the pass never edits this file.
[The template](../templates/code-review.md) shows the section.

- Each pass adds one entry with one line per finding
- The section never changes the verdict, status or finding IDs above it
- A focused follow-up or a later full review of the same gate keeps this section.
  The agent that rewrites the file copies it unchanged, and the primary agent restores it when a saved result omits it
