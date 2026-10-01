# Risk review

Read this when a plan or code gate needs more than the standard general review: a second reviewer focused on one named risk.

Do not use it for the PR review.

When the human asks for a PR risk review, explain that the mode applies only to plan and code gates, before the PR opens.
The PR review stays standard.
Do not silently downgrade the request or start an extra PR reviewer.

## Choose the mode

Use `standard` review by default.
It starts one general reviewer.

Use a risk review when the human requests it or one named risk could cause a blocker or major issue:

- Security, privacy or authorization
- Data migration, corruption or loss
- Public API or compatibility
- Concurrency or distributed behavior
- Cross-cutting integration

After a review stops on a disputed finding, only the human may start a new risk review.
Do not use a risk review only because a change is large or unfamiliar.

## Select one risk perspective

The primary agent names one perspective for the risk with the greatest possible release impact.
When several risks have similar impact or the choice is unclear, ask the human to select one.

Keep the perspective narrow enough to guide a review.
For example, use `authorization boundaries`, `migration rollback`, `API compatibility`, `concurrency safety` or
`cross-service failure handling`.

Record the selected perspective before launch and keep it fixed for that gate.
A risk review has exactly two perspectives: `general` and the named risk perspective.

## Start independent reviews

Give both reviewers the same target, feature artifacts and evidence boundary.
Tell each reviewer its perspective and do not give it the other reviewer's findings.
For a code risk review, pass this baseline directly to each reviewer.
Do not ask either reviewer to read the combined `code-review.md` file.

Run both reviews at the same time when the host supports it.
Otherwise run them separately and keep the second review independent from the first result.

Resolve review-only settings for each review process.
Use the same selected reviewer by default.
Use another configured reviewer only when the human selects it.

For a plan gate, use:

- `Plan review – in review (risk review: general + <risk perspective>)`

For a code gate, use the active-state format of [the code risk review](#code-risk-review).
Risk reviewers do not write the combined handoff directly.

If either required review cannot start or finish, keep any returned evidence and make the combined verdict `INCOMPLETE`.
Do not replace the missing perspective with the active development session.

## Keep sources separate

General findings use IDs such as `PLAN-G1` and `CODE-G1`.
Risk findings use IDs such as `PLAN-R1` and `CODE-R1`.

Every risk review finding includes an immutable `Source` value:

```markdown
Source: general
```

or:

```markdown
Source: <risk perspective>
```

The primary agent owns the combined result.
Copy each returned finding without changing its ID, source, severity, evidence, impact or suggested fix.
Keep duplicate findings until disposition and use replies to link them when one fix addresses both.

Do not ask another agent to synthesize or verify the results.
Each reviewer verifies its own findings through [the finding checks](3-findings.md#check-a-finding-before-publishing-it).
Do not use reviewer votes or drop a unique finding because the other reviewer passed.

Derive the combined verdict in this order:

1. `INCOMPLETE` when either required review is incomplete
2. `CHANGES NEEDED` when any blocker or major remains open
3. `PASS WITH FOLLOW-UPS` when only medium findings need disposition
4. `PASS` when both reviews pass and no finding needs disposition

For a plan gate, return both result sets under their perspective names followed by one combined verdict.
For a code gate, save both result sets in the primary-owned `code-review.md` handoff.

## Recheck one perspective

Send each reviewer only its own open IDs, replies and related changes.
Do not ask it to read the combined handoff.
Do not rerun a perspective that has no open finding.

The reviewer keeps its source-specific IDs and returns only its updated source result.
The primary agent copies that result into the combined handoff and recalculates the combined verdict.

Apply the normal convergence rule to each perspective.
When a disputed finding of any severity repeats without answering the reply or adding material evidence, stop and ask the human.

## Code risk review

The primary agent owns `code-review.md` during a code risk review.
Both reviewers are read-only for this file and return only their assigned perspective result.
They receive the target, artifacts and evidence boundary from the caller and do not read this combined file.

Start with:

```markdown
# Code review

Mode: risk review
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

Update each source status when its result returns.
Keep the overall status `in review` while either result is still running.
After both return, map the combined verdict to the overall file status through
[the file statuses](../writing/code-review.md#first-review).
If either result is incomplete, set the overall status to `incomplete` and keep any returned findings and evidence.

For a focused risk review follow-up, change only the matching source status to `in review` and increment only its round.
Keep the other source result unchanged.
