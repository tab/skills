---
name: feature-review
description: >
  Independently review a tracked feature at its plan, code or PR gate against its contract and current evidence.
  Use when the user asks for a feature plan review, implementation review or final PR review.
  Do not use to implement fixes or to report minor style preferences.
---

# Feature Review

Review one feature gate or one assigned stress perspective without changing code, feature contracts, plans, PRs or external systems.
For a standard code or PR gate, produce only the current review state for `code-review.md`.

Use the feature contract as the scope source, the plan as the implementation and verification source and current repository evidence
as the reality check.

## Resolve the gate and evidence

Identify the requested gate:

- **Plan** – after the feature contract and plan are ready and before implementation
- **Code** – after implementation and local checks and before the PR
- **PR** – on the current PR head after CI and accepted fixes

Resolve `docs/features/YYYYMMDD-<slug>/feature.md` and `plan.md` from the request, branch, PR or nearby repository context.
Ask one short question only when more than one feature is plausible and the target cannot be verified.

For a standard code or PR gate, read [the code review handoff](references/code-review.md) before reviewing.
Use `code-review.md` in the same feature folder.

When the caller assigns a stress perspective, use the stress rules below.
Stress review applies only to plan and code gates.
Review only the assigned `general` or named risk perspective and do not inspect the other reviewer's result.
For a stress code review, use the target, feature artifacts and evidence boundary provided by the caller.
Do not read the combined `code-review.md` file during the first review or a focused recheck.
If the user asks for a stress PR review, explain the boundary and ask them to choose a standard PR review or a stress code review
on the PR diff followed by the standard PR gate.
Do not silently downgrade the request or start an extra PR reviewer.

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

## Plan gate

Read the feature contract once as a first-time contributor before following its links.

Check in this order:

1. The goal and current problem are clear
2. In-scope and out-of-scope work are explicit
3. Assumptions are supported or visibly marked
4. Expected behavior and contracts are implementable and testable
5. The approach and steps cover every acceptance criterion
6. Verification, rollout and rollback match the actual risk

Check relevant current code and project conventions for feasibility claims.
Do not demand implementation detail that the repository can resolve safely during coding.

## Code gate

Review the complete feature diff and relevant tests against the approved artifacts.
Do not treat `code-review.md` as implementation code in that diff.

Check:

- Every acceptance criterion is implemented or has clear proof
- Behavior, contracts and compatibility match `feature.md`
- The implementation follows the planned approach or records a valid current decision
- Error paths, partial failures and important edge cases are handled
- Tests would fail for the important regression they claim to cover
- Documentation changed when the public or contributor-facing behavior changed
- Unrelated work did not enter the feature

Run or inspect proportionate automated checks when available.
Passing checks do not override a concrete behavioral defect.

## PR gate

Resolve the current PR head and review its complete diff, checks and unresolved relevant findings.
Do not treat `code-review.md` as implementation code in that diff.
Use the pushed PR head as the review target.
Inspect local changes and apply only the linked handoff's exception for `code-review.md` and workflow state in the same feature's
`plan.md`.
Return `INCOMPLETE` for an unpushed implementation or artifact change outside that exception.

Focus on integration and release readiness:

- Blocker or major regressions not caught earlier
- Drift between final code, feature contract and plan
- Missing required tests, documentation, migration, rollout or rollback work
- Failed, skipped or unavailable required checks
- Accidental commits or out-of-scope changes

Do not restart the code review from style preferences.
Do not repeat a closed finding unless new evidence changes it.
Do not commit or push the completed handoff.
The primary agent owns the separate final handoff actions and final CI check after a passing verdict.

## Check a finding before publishing it

Try to disprove every candidate finding against the current evidence:

1. Confirm that the trigger can happen under the reviewed contract or implementation
2. Name a concrete impact that a user, caller or maintainer would notice
3. Confirm that the reviewed plan or change causes it, worsens it or misses required behavior
4. Confirm that the suggested fix addresses the cause and matches the impact

Do not publish the finding until each check passes.
Do not report an unrelated existing issue unless the current change makes it reachable or worse.
When required evidence is missing, return `INCOMPLETE` instead of raising the finding's severity.
Returning no findings is valid when the reviewed evidence supports the feature.

## Finding contract

Report only findings with concrete impact:

- **Blocker** – unsafe, destructive, invalid or impossible to release safely
- **Major** – required behavior is wrong or missing, a likely serious defect exists or a key contract or proof is absent
- **Medium** – a contained real issue that needs a clear disposition before handoff

Do not report minor, low-value, optional or style-only findings unless the user explicitly asks for them.
If a low-value idea is still useful, suggest one backlog item after the verdict without presenting it as a finding.

Use stable IDs within a feature:

- `PLAN-1`, `PLAN-2` for the plan gate
- `CODE-1`, `CODE-2` for the code gate
- `PR-1`, `PR-2` for the PR gate

For a general stress perspective, use IDs such as `PLAN-G1` and `CODE-G1`.
For a named risk perspective, use IDs such as `PLAN-R1` and `CODE-R1`.
Add the assigned `Source` to every stress finding.

For each finding include severity, ID, exact file and line or section, evidence, impact and suggested fix.
Do not inflate severity to keep a review loop open.

## Verdict and convergence

Return one verdict:

- `CHANGES NEEDED` – at least one blocker or major finding remains open
- `PASS WITH FOLLOW-UPS` – no blocker or major remains, but medium findings still need a disposition
- `PASS` – the evidence is complete and no blocker, major or undisposed medium remains
- `INCOMPLETE` – required evidence could not be reviewed

A medium finding does not require agreement between agents.
The primary agent may fix a clear in-scope medium finding without another approval step.
The human decides when the finding is disputed, changes approved scope or contracts or needs accepted risk.
An out-of-scope medium may move to the backlog under the active feature workflow.
Keep a fixed finding's status in `code-review.md` and code evidence.
Update feature artifacts only when the finding changes their current contract, assumptions, decisions or plan.
Use the backlog only for deferred work.

On another round, review only changed areas and open finding IDs plus any regression caused by the fixes.
Read each `Reply`, keep IDs stable and record a short `Recheck` when a finding stays open.
Move closed findings to the compact `Resolved` section.
Do not reopen an unchanged resolved finding without new evidence.

Do not repeat target discovery, reread unchanged artifacts, run a broad repository search or rerun the full check suite on a
focused follow-up.
Start from the open IDs and the fix diff, then make another read or check only when it can change an ID's disposition.

Stop the gate loop as soon as no blocker or major remains.
Minor or low-value disagreement never starts another round.
After the primary disputes a blocker or major with evidence, allow one focused recheck.
If the reviewer keeps the finding open without answering that evidence or adding material evidence, stop the agent loop.
Keep the verdict `CHANGES NEEDED` and ask the human to choose the next action.
A request to continue until the agents agree does not authorize more unchanged rounds.

## Save the result

For a plan gate, return the findings and verdict directly.
A direct review does not edit `plan.md`; say that the primary agent or human must record the returned verdict under the matching gate.

At the start of a standard code or PR gate, initialize the active review state from the linked handoff when write access is limited
to that file.
For a read-only reviewer, the primary agent or external runner owns this start state.

For a standard code or PR gate, create or replace `code-review.md` using the linked handoff when the host can limit write access to
that file.
On a focused follow-up, rewrite the whole file with its current open and resolved state.
Do not append a review transcript.

For a stress plan or code review, return only the assigned perspective result.
The primary agent owns the combined result and final verdict.
Do not write or replace the combined `code-review.md` file.

When a standard review runs read-only, return the complete file content directly so the primary agent or external runner can save
it verbatim.
Once the unchanged content is saved, the recorded verdict applies and the review does not need to run again.
A read-only handoff is `INCOMPLETE` when its content cannot be saved unchanged.

After a standard code or PR review, return one short message with the path and verdict.

## Plan review output

Lead with findings ordered by severity.
If there are no findings, say `No blocking findings`.

For a stress perspective, put `Source: <assigned perspective>` before the findings.

Then return:

```markdown
Verdict: <PASS | PASS WITH FOLLOW-UPS | CHANGES NEEDED | INCOMPLETE>

Evidence checked:

- <Artifact, diff and check result>

Disposition needed:

- <Medium finding ID or none>
```

Keep the plan response short enough for the primary agent and human to act on without another summary.
