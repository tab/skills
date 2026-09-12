# Reconstruction guide

Use this guide to keep backfilled feature artifacts bounded, evidence-backed and consistent across agents.

## Evidence order

Prefer sources in this order:

1. Current code, tests and public or contributor-facing documentation
2. Merged diffs and commits confirmed on the default branch
3. Accepted issues, design records and resolved review decisions
4. Release membership and release notes
5. PR descriptions and commit messages

A lower source may explain intent, but it cannot override contradictory implementation evidence without a later accepted decision.

Record an assumption only when evidence supports it and future maintenance needs it to remain visible.
Stop when a decision-shaping claim depends only on plausible wording or inference.

## Discovery windows

Apply the user's sources, date range or repository area as the outer scope.

Within that scope, inspect at most:

- 30 merged PRs ordered from newest to oldest
- 100 first-parent commits ordered from newest to oldest when merged PR metadata is unavailable

Return at most five strong candidates per batch.

Use the oldest inspected merge date and PR number as the PR cursor.
Use the oldest inspected commit hash as the commit cursor.

Continue strictly before that cursor in the next batch.
Do not rescan newer sources or silently expand the outer scope.

## Feature identity

A feature is one coherent outcome, not one repository event.

Group sources only when the outcome needs them together and at least one strong signal connects them:

- The same accepted issue, design record or explicit feature identifier
- An explicit prerequisite or follow-up chain required for the outcome
- One shared behavior or contract introduced across the sources

File overlap, similar wording, the same author or nearby dates are only search hints.

Split sources when either part:

- Has a useful outcome by itself
- Can ship, roll back or be removed independently
- Exists for a different reason
- Belongs to a separate compatibility or operational contract

## Duplicate matching

Check in this order:

1. An existing artifact names one of the same source PRs, commits or releases
2. An existing artifact describes the same outcome and current behavior
3. A similar title or slug suggests a candidate to inspect

Update the existing artifact when the first or second match is true and new evidence changes current truth.
Skip it when the evidence and current truth are already covered.
Create a new folder only when no existing artifact matches.

Never change an existing matching folder date because later evidence was found.

## Delivery date

The folder date is when the coherent outcome first became usable on the default branch.

Use:

1. The merge date of the last required PR
2. The date of the last required implementing commit on the default branch when no PR exists
3. The release date only when it is the only reliable anchor and the release uniquely identifies the outcome

Do not use the first development commit, PR creation date, optional follow-up date or backfill date.

## Artifact mapping

Map evidence into artifacts without copying it:

| Evidence                      | Artifact destination                              |
|-------------------------------|---------------------------------------------------|
| Verified problem and goal     | `feature.md` Goal and source-backed Context       |
| Delivered behavior            | `feature.md` acceptance criteria                  |
| Compatibility boundary        | `feature.md` Scope or Contracts                   |
| Accepted durable rationale    | `feature.md` Decisions                            |
| Historical change or decision | `feature.md` Sources                              |
| Final delivery evidence       | `feature.md` Sources                              |
| Current implementation        | `plan.md` files, components and observed behavior |
| Tests and verified checks     | `plan.md` Verification                            |
| Verified release operation    | `plan.md` Rollout and rollback                    |

Use atomic acceptance criteria and map implementation steps to them.
Omit a conditional section when evidence does not support useful content.

## Final quality gate

Before saving, confirm:

- A first-time contributor can explain the goal, boundary and current behavior without opening every source
- Every material statement has direct evidence or is marked as an assumption
- No context paragraph relies only on generic engineering advice or common sense
- No section mainly repeats a current skill, source document or another artifact
- Sources do not repeat current implementation links from the plan
- The plan describes observed implementation rather than imagined original intent
- Each implementation item names an actual file, component or operational mechanism
- Verification names current coverage and specific gaps without repeating delivery history
- Sources are concise and stable
- Current code does not contradict the artifact
- Existing feature artifacts do not already cover the outcome
- The folder date follows the delivery rule
- A focused `humanify` pass removed repetition and unclear wording without changing evidence or certainty

When any check fails materially, keep the candidate in discovery output and do not create the artifact.
