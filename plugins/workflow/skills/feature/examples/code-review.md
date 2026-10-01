# Code review

Mode: standard
Gate: code
Status: passed
Round: 2
Target: 4f2c9e1..9b7d3a0
Reviewer: code-reviewer
Model: not reported
Effort: high

## Resolved

- CODE-1 – resolved: a used token no longer opens the form. `TestUsedTokenRejected` fails when the used check is removed
- CODE-2 – resolved: kept as it was. The old tokens are deleted at deploy, as `feature.md` decides, so no grace period is needed

## Checked

- AC1 to AC4 in `feature.md` against the diff
- `auth/reset_token` tests, three runs, all pass
- The expired page shows for an old, a used and a replaced token
- The deploy script deletes the tokens issued before the release

## Verdict

PASS
