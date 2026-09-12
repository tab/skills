# Code review handoff

Use `docs/features/YYYYMMDD-<slug>/code-review.md` for the current code or PR review.
Do not use it for the plan gate.

The file is shared by the primary and review agents, but only one agent updates it at a time.
Keep current state instead of an appended conversation.

## Start a review

Record the active review before it starts.
The primary agent or external runner records it when the reviewer is read-only.
The reviewer records it when write access is limited to this file.

For a new standard review, replace the old file with:

```markdown
# Code review

Mode: standard
Gate: <code or pr>
Status: in review
Round: 1
Target: <exact diff range, working tree or PR head>
Reviewer: <resolved reviewer>
Model: <resolved model>
Effort: <resolved effort>
```

Record the reviewer, model and effort values used to start the review.
For a direct invocation, use the current review session values when available and `not reported` for values the host does not expose.
If the host reports a different runtime model, record that mismatch under `Checked` instead of adding another header field.

For a focused standard follow-up, preserve findings and replies, set `Status` to `in review` and increment `Round` before launch.
Do not change the finding text while recording the active round.

For a plan gate, the `feature` workflow records the active state in `plan.md` instead of creating this file.

## PR handoff boundary

Create and update the PR review handoff locally while reviewing the pushed PR head.
The `Target` remains the implementation head that the reviewer checked.
Do not change it to a later commit that contains only the allowed handoff changes below.

The pushed head remains reviewable when local changes are limited to this handoff and workflow state in the same feature's `plan.md`:

- `Status`, `Phase` and `Current step` values that record the current lifecycle or next eligible action
- Review gate checkboxes and verdicts that record the current review result or `in review` state

Inspect the actual diff before applying this exception.
A state update must follow verified events and existing approvals.
It cannot change scope, decisions, implementation tasks, verification, findings or approval requirements.
A mixed `plan.md` diff with any such change is outside the exception.
For any other unpushed implementation or artifact change, return `INCOMPLETE` because the PR head is not the current release candidate.

After a PR verdict passes, the primary agent records the result in `plan.md` and may request separate approval to commit and push
the final handoff plus those allowed state updates.
That head change does not need another PR review, but required CI must pass on the final head before merge approval.
Any change outside this exception reopens the PR gate.
Later allowed state updates may stay local until the next approved commit, and any later push needs final CI before merge.
The reviewer never edits `plan.md`, commits or pushes the handoff.

## Stress code review

The primary agent owns `code-review.md` during a stress code review.
Both reviewers are read-only for this file and return only their assigned perspective result.
They receive the target, artifacts and evidence boundary from the caller and do not read this combined file.

Start with:

```markdown
# Code review

Mode: stress
Gate: code
Status: in review
Target: <exact diff range or working tree>
General status: in review
General round: 1
General reviewer: <resolved reviewer>
General model: <resolved model>
General effort: <resolved effort>
Risk perspective: <named perspective>
Risk status: in review
Risk round: 1
Risk reviewer: <resolved reviewer>
Risk model: <resolved model>
Risk effort: <resolved effort>
```

Each reviewer returns its source, findings, checked evidence and verdict.
The primary agent copies each finding without changing its content and keeps checked evidence under `General` and the named risk
perspective.

Use `CODE-G1`, `CODE-G2` and later IDs for general findings.
Use `CODE-R1`, `CODE-R2` and later IDs for risk findings.
Every finding includes `Source: general` or `Source: <risk perspective>`.

Update each source status when its result returns.
Keep the overall status `in review` while either result is still running.
After both return, map the combined verdict to the overall file status through the main skill rules.
If either result is incomplete, set the overall status to `incomplete` and keep any returned findings and evidence.

For a focused stress follow-up, change only the matching source status to `in review` and increment only its round.
Keep the other source result unchanged.

## First review

The review agent creates or replaces the whole file for a new full code or PR review.
When it is read-only, it returns the complete file content and the primary agent or external runner saves it verbatim.
It records the target, current round, findings, checked evidence and verdict.

Use this shape:

```markdown
# Code review

Mode: standard
Gate: <code or pr>
Status: changes needed
Round: 1
Target: <exact diff range, working tree or PR head>
Reviewer: <resolved reviewer>
Model: <resolved model>
Effort: <resolved effort>

## Findings

### CODE-1 – <short title>

Severity: major
Status: open
Location: `<path:line>`

Finding: <problem and impact>

Suggested fix: <smallest useful change>

## Checked

- <artifact, diff or check result>

## Verdict

CHANGES NEEDED
```

Use `CODE-1`, `CODE-2` or matching `PR-1`, `PR-2` IDs.
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

Use blocker, major or medium severities from the main skill.
Do not add minor or style-only findings.
For stress review, apply the same status values to each source and derive the overall status only after both sources finish.

## Reply

The primary agent reads each finding, makes accepted changes and adds a short reply:

```markdown
Reply: Fixed by <short change and evidence>
```

When it should stay:

```markdown
Reply: Kept because <short evidence>
```

The primary agent may set the finding status to `fixed`, `disputed`, `backlog` or `accepted risk`.
`backlog` must include the backlog ID.
`accepted risk` needs the human's decision.

Do not change the finding, severity, location or suggested fix while replying.

## Recheck

On a focused follow-up, the review agent reads the current file, replies and changed areas.
It checks only open finding IDs and regressions caused by their fixes.

In stress review, each reviewer receives only findings, replies and related changes from its own source.
It does not read the combined handoff.
The primary agent copies the returned source result into the combined file and leaves the other source unchanged.

For a finding that stays open, add a short recheck:

```markdown
Recheck: Still open because <current evidence>
```

Move closed findings to a compact section:

```markdown
## Resolved

- CODE-1 – resolved: <short evidence>
```

Rewrite the whole file with the current state after every recheck.
Preserve the meaning of the primary agent's reply while its finding remains open.
Keep the active `Round` value when the review agent completes the pass.

## Start again

A PR review replaces the previous code review, uses standard mode and starts with `PR-NNN` IDs.
A new full review of the same gate replaces the file only when the user or primary agent asks to start again.
Deleting the file also starts again, but never delete it without clear user approval.

Do not review `code-review.md` as implementation code.
Check only that it matches the current review state.
