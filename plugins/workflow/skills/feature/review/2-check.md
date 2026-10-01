# 2. Check

Read this at a plan gate, a code gate or a PR review: what each one checks.

## Plan gate

Read the feature contract once as a first-time contributor before following its links.

Check in this order:

1. `feature.md` has Goal, Why, Scope, How it works, Acceptance criteria and Decisions.
   `plan.md` has Done when, Steps and Gates. Check an optional section only when it is present
2. The goal and the why are clear
3. In-scope and out-of-scope work are explicit
4. Assumptions, when present, are supported or visibly marked
5. How it works, the acceptance criteria and any contracts are implementable and testable
6. The steps cover every acceptance criterion
7. `Done when`, and `Rollout and rollback` when present, match the actual risk

Check relevant current code and project conventions for feasibility claims.
Do not demand implementation detail that the repository can resolve safely during coding.

## Code gate

Review the complete feature diff and relevant tests against the approved artifacts.
Do not treat `code-review.md` as implementation code in that diff.

Check:

- Every acceptance criterion is implemented or has clear proof
- Behavior, contracts and compatibility match `feature.md`
- The implementation follows `How it works` and the plan's steps, or records a valid current decision
- Error paths, partial failures and important edge cases are handled
- Tests would fail for the important regression they claim to cover
- Documentation changed when the public or contributor-facing behavior changed
- Unrelated work did not enter the feature

Run or inspect proportionate automated checks when available.
Passing checks do not override a concrete behavioral defect.

## PR review

Run this when the human asks for a review of the pushed PR.

A PR review runs on the pushed PR, not in the files. It is not a gate in `plan.md`.
CI runs there, and so does any reviewer the project adds.

- Review the pushed PR head: its complete diff against the base branch and its CI result
- Use the finding contract, the severities and the verdicts of [findings and verdicts](3-findings.md)
- Return `INCOMPLETE` when the head or its CI result cannot be inspected

Focus on integration and release readiness:

- Blocker or major regressions not caught earlier
- Drift between final code, feature contract and plan
- Missing required tests, documentation, migration, rollout or rollback work
- Failed, skipped or unavailable required checks
- Accidental commits or out-of-scope changes

Do not restart the code review from style preferences.
Do not repeat a finding closed in `code-review.md` unless new evidence changes it.
A fix is a normal commit pushed to the PR.
On the new head, check the open IDs, the fix diff and its CI result, as a focused follow-up does.
