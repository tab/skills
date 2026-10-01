# 1. Prepare

Start every review here: resolve the review and its evidence, keep the evidence bounded and find the files to read next.

The gate reviewer reads this file from the path in its brief.
The `feature` skill reads it for a review-only request.

Review one feature gate or one assigned risk review perspective without changing code, feature contracts, plans, PRs or external
systems.
The one exception is a PR review, which posts its result as PR comments.
For a standard code gate, produce only the current review state for `code-review.md`.

Use the feature contract as the scope source, the plan's steps and `Done when` as the implementation and proof source and current
repository evidence as the reality check.

## Resolve the review and its evidence

Identify the requested gate:

- **Plan** – after the feature contract and plan are ready and before implementation
- **Code** – after implementation and local checks and before the PR

A request to review the PR follows [the PR review](2-check.md#pr-review).

Resolve `docs/features/YYYYMMDD-<slug>/feature.md` and `plan.md` from the request, branch, PR or nearby repository context.
Ask one short question only when more than one feature is plausible and the target cannot be verified.

For a standard code gate, read [the code review rules](../writing/code-review.md) before reviewing.
Use `code-review.md` in the same feature folder.

When the caller assigns a risk review perspective, use [the risk review rules](risk-review.md).
Review only the assigned `general` or named risk perspective and do not inspect the other reviewer's result.
For a code risk review, use the target, feature artifacts and evidence boundary provided by the caller.
Do not read the combined `code-review.md` file during the first review or a focused recheck.

Read the repository instructions and the smallest current evidence set needed for the gate.
Do not review from a chat summary when the source artifacts are available.

When the caller provides reviewer, model and effort values used to start the review, keep them in the review handoff.
For a direct invocation without those values, use the current review session values when the host exposes them and record
`not reported` for anything the host does not expose.
Do not start another reviewer or change the active session to fill these fields.

Return `INCOMPLETE` when a required artifact, diff, PR head or check result cannot be inspected.
Name the missing evidence and do not turn a partial review into a pass.

## Keep evidence bounded

Start with the feature artifacts, the changed-file list and focused diff hunks.
Open a full file only when a hunk lacks the context needed to judge behavior.
Do not reread a file after its relevant section is available.

Do not inspect prior branches, unrelated documentation or broad repository history unless the approved contract depends on them.
Current repository evidence replaces old session context unless the request needs a past decision that is not stored in the artifacts.

Treat an exact command and result recorded in the current plan as check evidence.
Rerun it only when the result is missing, stale, doubtful or needed to resolve a concrete finding.

## What to read next

Read the files that match the review:

- **Plan gate** – [the plan gate](2-check.md#plan-gate), [findings and verdicts](3-findings.md) and
  [its result](4-report.md#plan-gate)
- **Code gate** – [the code gate](2-check.md#code-gate), [findings and verdicts](3-findings.md),
  [the code review rules](../writing/code-review.md) and [its result](4-report.md#code-gate)
- **Focused follow-up** – [verdict and convergence](3-findings.md#verdict-and-convergence) and, for a code gate,
  [the recheck rules](../writing/code-review.md#recheck)
- **Risk review perspective** – [the risk review](risk-review.md) and [its result](4-report.md#risk-review),
  on top of the gate's files
- **PR review** – [the PR review](2-check.md#pr-review), [findings and verdicts](3-findings.md) and
  [its result](4-report.md#pr-review)
- **Challenge pass** – [the challenge pass](challenge.md)
- **Review settings** – [the settings](settings.md) and [their defaults](settings.json),
  read by the agent that starts a review
