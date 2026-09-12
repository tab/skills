# Feature backfill plan

Feature: [feature.md](feature.md)

Status: implemented

Current step: open the PR when the user is ready

## Approach

Keep bounded discovery and write approval in `SKILL.md`.
Keep grouping, duplicate and date rules in one reconstruction reference.

## Steps

- [x] Add bounded discovery, grouping, duplicate and date rules – AC1, AC2, AC3 and AC4
- [x] Reconstruct short source-backed contracts and observed implementation plans – AC5 and AC6
- [x] Preserve agent-neutral approval and write boundaries – AC7
- [x] Test the skill on repository history and run package validation – AC1, AC2, AC3, AC4, AC5, AC6 and AC7
- [x] Run an independent code review and close out both artifacts – AC5 through AC7

## Gates

- [x] Plan review – PASS before gate tracking was added
- [x] Code review – PASS before the `code-review.md` handoff was added
- [ ] PR review – not run

## Verification

- One complete small-repository pilot returned a bounded candidate batch before files were written
- The pilot grouped related refinements and kept independent features separate
- Four selected artifacts use verified delivery dates and lifecycle statuses
- The skill validator, `make test`, `make validate`, `make docs` and whitespace checks pass
- No automated test covers candidate grouping or historical date selection

## Rollout and rollback

Include the skill in the pending workflow release after the separate version bump.

Rollback removes the skill and its listing without changing any feature artifacts already reviewed and accepted by the user.
