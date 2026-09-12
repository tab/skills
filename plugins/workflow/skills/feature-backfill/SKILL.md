---
name: feature-backfill
description: >
  Reconstruct missing feature artifacts from past repository work and current implementation evidence.
  Use when the user wants to restore docs/features from merged PRs, commits, releases or a bounded area of project history.
  Do not use for new feature planning, general changelogs or activity reports.
---

# Feature Backfill

Restore useful feature context from repository history without turning every PR into a document or inventing missing intent.

Read [the reconstruction guide](references/reconstruction.md) before grouping candidates, choosing dates or writing artifacts.

## Choose the mode

Use discovery mode when the user asks what can be restored, requests a broad backfill or has not clearly asked to create files.

In discovery mode, inspect evidence and return candidates without changing the repository.

Use backfill mode when the user explicitly asks to restore, create or save feature artifacts for named sources or selected candidates.

That request authorizes the matching local documentation changes only.
It does not authorize code changes, commits, pushes, PR changes or other external writes.

## Resolve the source scope

Identify the repository, its default branch and one outer scope:

- Named PRs, commits or releases
- A date range
- A repository area or feature name
- A continuation cursor from an earlier discovery batch

Read repository instructions and existing `docs/features/` artifacts first.

When the user gives no useful bound, inspect only the most recent source window from the reconstruction guide.
Never scan the complete history in one run.

If the required history or hosting evidence is unavailable, name the missing source and stop rather than guessing.

## Collect current and historical evidence

Use available read-only repository and hosting sources.

For each possible outcome, inspect the smallest useful set of:

- Merged PR metadata, diffs and relevant resolved review decisions
- Commits on the default branch
- Accepted issues or design records linked from the change
- Releases that identify the delivered behavior
- Current code, tests and documentation in the affected area
- Existing feature artifacts that may already cover the outcome

Treat PR descriptions, commit messages and release notes as claims to verify.
Do not copy their wording into artifacts when code, tests or accepted decisions provide clearer evidence.

## Build candidates

Group sources by one coherent user-visible or developer-visible outcome using the reconstruction guide.

Do not create candidates for:

- Dependency updates, formatting or mechanical cleanup
- CI or tooling maintenance with no durable developer contract
- Refactors with no lasting behavior or decision
- Reverted, replaced or materially drifted behavior that cannot be reconciled to current truth
- Work whose goal or boundary remains speculative

For a specific unambiguous source requested for backfill, continue directly when the feature boundary and evidence are clear.

For a batch, return at most five candidates before writing:

```markdown
### <Candidate title>

Delivery date: <YYYYMMDD or unresolved>
Outcome: <One clear result>
Sources: <PRs, commits, releases and current paths>
Artifact: <Create, update, skip or needs decision>
Reason: <One evidence-backed sentence>
```

End discovery output with the continuation cursor or `End of scope`.

Ask the user only about candidates whose boundary, value or conflict cannot be resolved from evidence.

## Reconstruct the artifacts

For each requested or selected candidate:

1. Recheck existing artifacts using the duplicate rules
2. Choose the historical delivery date and a short lowercase hyphenated slug
3. Create or update `docs/features/YYYYMMDD-<slug>/feature.md`
4. Create or update `plan.md` in the same folder
5. Reconcile both documents with current code, tests and documentation
6. Use the `humanify` skill without changing evidence, meaning or certainty
7. Read the result once as a first-time contributor

An existing matching artifact keeps its folder name and date.
Update it in place when new evidence changes current truth.
Skip it when it already covers the outcome and sources.

### `feature.md`

Start a small feature with `Goal`, atomic acceptance criteria and `Sources`.
Add `Context`, `Scope`, `Assumptions`, `Contracts` or `Decisions` only when they contain source-backed information that a contributor
cannot learn quickly from the current implementation.

Do not fill a template for completeness.
Omit generic context that could describe many projects or features.
Do not turn common sense into historical rationale.
When the current skill, code or documentation already explains a behavior well, link to it and record only the non-obvious boundary
or decision.

Keep `Sources` short and ordered from the main historical change or decision to final delivery evidence.
Do not repeat current implementation links that belong in `plan.md`.
Keep only the release that proves the complete current outcome was delivered unless an earlier release explains a durable boundary.
Use stable links or repository-relative paths.
Do not include review conversations, an activity timeline or a copied PR description.

### `plan.md`

Add `Reconstruction: After implementation, from the feature sources and current files` below `Current step`.
Do not add the live `Phase` field.

Name the actual files, components or operational mechanisms that implement each acceptance criterion.
Describe available verification evidence and important gaps.
Include rollout or rollback only when the sources support it and it still helps current maintenance.

Do not repeat PR, merge or release history already covered by `feature.md` and the lifecycle status.
Verification should name what current checks cover and any specific behavior they do not test.
Use checked Markdown tasks for the delivered implementation items reconstructed from evidence.

Set `Current step` to `Complete`.
Use `merged` only when default-branch integration is verified.
Use `released` only when a release containing the outcome is verified.
Otherwise use `implemented` and state which lifecycle evidence is missing.

Do not restate acceptance criteria as generic delivered steps.
Do not write imagined rejected options, planned steps, tests, rollout or rationale.

## Reconcile drift

Check later changes to the affected behavior before finishing.

- Include later sources when they refine the same feature and allow one current contract
- Update the documents to match current surviving behavior
- Stop when the original outcome was replaced, removed or split and no clear current boundary remains

Do not create a historical-looking artifact that a contributor could mistake for the current contract.

If the `humanify` skill is unavailable, make the same focused prose pass directly and state that the fallback was used.

## Report the result

For every created, updated or skipped candidate, report:

- Artifact path or matched existing path
- Delivery date and its evidence
- Main sources used
- Important evidence gap or `None`

Keep discovery notes and review history out of the saved artifacts.

## Safety and stopping rules

- Preserve unrelated working-tree changes
- Use read-only external sources unless the user separately approves a write
- Do not fetch, rewrite history or change branches when available read-only evidence is enough
- Do not commit, push, open or change a PR, merge or release without explicit approval
- Stop when evidence cannot support the goal, feature boundary, delivery date or current relevance
