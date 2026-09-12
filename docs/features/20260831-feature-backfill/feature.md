# Feature backfill

## Goal

Rebuild missing feature documents from repository history and current code without guessing intent or documenting every repository event.

## Context

Useful context is spread across PRs, commits, releases and current implementation files.
These sources must be grouped and checked before they can describe one current feature.

## Scope

### In

- Bounded discovery from Git history, PRs, releases and current implementation
- Candidate grouping by one delivered outcome
- Historical dates, duplicate checks and concise sources
- A reconstructed contract and observed implementation plan
- A focused `humanify` and first-time-reader pass

### Out

- An unbounded full-history scan
- One feature artifact per PR or commit
- Changelogs, activity reports or guessed rationale
- Implementation changes, commits, pushes or other external writes

## Expected behavior

### Main flow

1. The user provides past work or a repository area
2. The agent checks a bounded source window, current implementation and existing artifacts
3. The agent groups strong candidates and previews a batch before writing
4. The user selects candidates or resolves an unclear boundary
5. The agent reconstructs both documents from verified evidence
6. The agent runs `humanify` and a first-time-reader check without changing facts or certainty

### Human checkpoints

- Select backfill candidates when a batch contains several useful outcomes
- Decide ambiguous boundaries, material drift or accepted evidence gaps
- Decide when the skill change is ready to merge and release

### Acceptance criteria

- **AC1** – discovery accepts named sources or a repository area and returns a bounded batch with a continuation cursor
- **AC2** – sources are grouped by one coherent outcome while routine, weak or independent work stays separate
- **AC3** – current implementation and existing artifacts are checked before writing
- **AC4** – the folder date and lifecycle status use verified delivery and release evidence
- **AC5** – `feature.md` keeps only source-backed context, non-obvious boundaries and concise sources
- **AC6** – `plan.md` names the observed files or mechanisms and does not pretend to be the original plan
- **AC7** – the skill remains agent-neutral and requires explicit approval before local or external writes

## Decisions

- Keep backfill separate from new feature planning because its evidence and date rules are different
- Reconstruct coherent outcomes rather than repository activity records
- Use the historical delivery date so feature folders sort by when work landed
- Preview small batches and skip uncertain candidates instead of creating speculative artifacts
