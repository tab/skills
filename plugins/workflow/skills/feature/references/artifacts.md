# Feature artifacts

These documents are for humans and agents.
Write them for a contributor who knows the project but did not join the original discussion.

## Shared rules

- Keep current truth, not a history of the conversation
- Use short concrete language and define a term before relying on it
- Keep one behavior in each acceptance criterion
- State important assumptions instead of hiding them inside implementation steps
- Describe contracts precisely enough to implement and test
- Keep explicit out-of-scope items that prevent likely scope drift
- Remove unused sections instead of filling them with `None` or generic text
- Refactor unclear text in place instead of appending corrections
- Put deferred ideas in the backlog, current code review state in `code-review.md` and older history in Git or the PR
- Prefer links over copied requirements, decisions or evidence

## Feature folder

Use `docs/features/YYYYMMDD-<slug>/`.
For new work, the date is when the feature folder is first created.
For backfilled work, the date is the verified historical delivery date.
The slug is a short lowercase hyphenated name.
For example, use `docs/features/20260831-password-reset/`.

Keep the original folder name when the feature is resumed or changed.
Do not replace its date with the resume, merge or release date.
Add `code-review.md` only when the first code or PR review starts.

## `feature.md`

`feature.md` answers what should change, why it matters and where the boundary is.

Use the smallest useful set of these sections:

```markdown
# <Feature title>

## Goal

<One clear outcome>

## Context

<Current behavior, problem and why the change matters>

## Scope

### In

- <Required outcome>

### Out

- <Explicit boundary that prevents likely scope drift>

## Expected behavior

### Main flow

1. <Observable step>

### Acceptance criteria

- **AC1** – <One testable behavior>

## Assumptions

- <Decision-shaping fact that has been checked or must remain visible>

## Contracts

<API, data, compatibility, security or operational rules needed to implement the feature>

## Decisions

- <Durable choice and short reason>

## Open questions

- <Only a question that still blocks scope or implementation>
```

Do not add `Contracts`, `Decisions` or `Open questions` when they add no useful information.
Resolve an open question into the relevant section or remove it.

## `plan.md`

`plan.md` answers how the feature will be implemented, how it will be proved and where work should resume.

```markdown
# <Feature title> plan

Feature: feature.md

Status: draft

Phase: feature

Current step: <one active or next step>

## Approach

<Smallest implementation shape and important affected areas>

## Steps

- [ ] <Implementable step> – AC1

## Verification

- <Check and expected proof>

## Gates

- [ ] Plan review – not run
- [ ] Code review – not run
- [ ] PR review – not run

## Rollout and rollback

<Only when release risk or staged rollout makes this useful>

## Blockers

- <Blocking feature or decision and the exact resume point>
```

Use one of these statuses:

- `draft`
- `ready for plan review`
- `ready for approval`
- `in progress`
- `blocked`
- `implemented`
- `merged`
- `released`
- `stopped`

For active feature work, use one phase from [the phase guide](phases.md):

- `feature`
- `plan`
- `build`
- `code review`
- `pr review`
- `release`

The phase is the work that is active or waiting for approval.
The `feature-backfill` workflow uses `Reconstruction:` and omits `Phase` because a historical plan did not run through the live
phases.
An existing active plan adds it when the `feature` workflow next resumes that work.

Remove `Blockers` when no blocker exists.
After a verified release, set `Current step` to `complete` and keep the final verification plan useful for later maintenance.
Historical plans may use `complete` with their verified lifecycle status.
Use Markdown tasks for implementation steps.
Mark a task `[x]` when its work and required checks are complete.
Add an unchecked task when new in-scope work is discovered and update the feature contract first when it changes scope or behavior.

Keep the latest verdict beside each gate.
Use `<gate> – in review` while its reviewer is running.
Leave `CHANGES NEEDED` and `INCOMPLETE` unchecked.
Check `PASS`, or `PASS WITH FOLLOW-UPS` after each medium finding has a recorded disposition.
Reopen the checkbox when a later full review does not pass.
During PR review, lifecycle fields and review gate state may change under the narrow exception in the `feature-review` handoff.
This exception does not cover changes to the approach, tasks or verification.

While a standard plan review runs, use:

```markdown
- [ ] Plan review – in review
  - Mode: standard
  - Target: <exact feature and plan revision>
  - Status: in review
  - Round: 1
  - Reviewer: <resolved reviewer>
  - Model: <resolved model>
  - Effort: <resolved effort>
```

While a stress plan review runs, use:

```markdown
- [ ] Plan review – in review
  - Mode: stress
  - Target: <exact feature and plan revision>
  - General: in review, round 1, <reviewer>, <model>, <effort>
  - Risk perspective: <named perspective>
  - Risk: in review, round 1, <reviewer>, <model>, <effort>
```

Update the source status while the review runs.
After the gate returns its combined verdict, remove the active details and keep the short gate line.

## `code-review.md`

`code-review.md` is a short handoff between the primary and review agents during code and PR reviews.
It stores the current target, round, findings, replies, rechecks, checked evidence and verdict.

The review agent produces and rewrites the file for a standard review.
For a stress code review, the primary agent owns the combined file and copies both independent result sets into it.
Before a review starts, the primary agent or reviewer that can write the file records its active round, target and resolved review
settings.
When it is read-only, the primary agent may save the complete returned content verbatim before adding any reply.
The primary agent adds a short `Reply` under each finding after making a fix or deciding the code should stay.
Only one agent updates the file at a time.

Do not turn the file into a chat transcript or implementation diary.
The `feature-review` skill owns its exact format, reset rules and finding states.

## Quality check

Before a plan review, use the `humanify` skill on both documents when it is available.
Otherwise make the same focused prose pass directly and state that the fallback was used.
Do not change facts, scope, contracts or certainty.
Run the same pass on text changed while resolving review findings.
Return to plan review when that cleanup changes meaning.

Before the final PR review, run the focused prose pass after the implementation closeout so the reviewer sees the final wording.

Then read the documents once in this order:

1. Goal and context
2. Scope and assumptions
3. Expected behavior and contracts
4. Decisions
5. Approach, steps and verification

The reader should not need chat history to explain the goal, implement the main flow or know what is outside the feature.
If the documents repeat the same rule, keep the clearest source and link to it from the other document.
