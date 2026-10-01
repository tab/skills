# Password reset links expire plan

Feature: [feature.md](feature.md)

Status: implemented

Phase: code review

Current step: prepare the PR

## Done when

- Every acceptance criterion in `feature.md` holds
- The unit and integration tests pass
- A link opened after 31 minutes shows the expired page in a manual check

## Steps

- [x] 1. Store the creation time and a used flag with each token
- [x] 2. Reject expired, used and replaced tokens
  - Check the age and the used flag in the token lookup, the one place every caller goes through
  - A new request deletes the user's older tokens
- [x] 3. Show the expired page with a "Send a new link" button
- [x] 4. Delete the tokens issued before the release

## Gates

- [x] Plan review – PASS, round 1, 2026-08-31
- [x] Code review – PASS, round 2, 2026-09-03
