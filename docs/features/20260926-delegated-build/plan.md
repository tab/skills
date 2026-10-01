# Delegated delivery team plan

Feature: [feature.md](feature.md)

Status: implemented

Phase: pr review

Current step: Open the PR from `feature/delegated-build` to `master`

## Done when

- Every acceptance criterion in `feature.md` holds
- `make test`, `make validate` and `make docs` pass
- Real agents pass the probes in steps 5, 8 and 15

## Steps

- [x] 1. Add the five role agents
- [x] 2. Write the team guide and link it from the `feature` skill
- [x] 3. Add the `coverage` skill
- [x] 4. Add the adversarial review and update the README
- [x] 5. Probe the agents in a scratch project and fix what they miss
- [x] 6. Merge `feature-review` into `feature`
  - Move the review rules and the review handoff into `feature/references/`
  - Give a reviewer the full path to the review rules in its brief
  - Remove the skill and every mention of it
- [x] 7. Add templates and a worked example to the `feature` skill
  - Freeze `feature.md` after approval; the lead edits only the state in `plan.md`
  - Drop the `Commits` section from the plan template; commits follow the `cmt` skill
- [x] 8. Probe the merged skill: a Claude gate, a Codex gate, a PR gate and an `architect` draft
- [x] 9. Stop the files at the PR
  - Remove the PR gate from the plan, the PR handoff exception and the `merged` and `released` statuses
  - Keep a short PR review section for a reviewer that comments on the PR
- [x] 10. Split the references into single-purpose files under `artifacts/`, `phases/`, `team/` and `review/`
  - Split `team/roles.md` into roles, the phase map and reports
  - Move the review defaults to `review/config.json` and update the two paths that read it
  - Probe that a gate still finds its rules from `review/guide.md`
- [x] 11. Restructure the skill so the tree reads without documentation
  - Move `references/` up into `writing/`, `flow/`, `team/` and `review/`, numbered where order matters
  - Probe that a gate still finds its rules from `review/1-prepare.md`
- [x] 12. Answer CODE-1: reword AC2 and have the lead check that a `code-reviewer` run changed no file
- [x] 13. Make the code review loop autonomous
  - Plan approval leads into the code gate with no BUILD stop, and covers the fix steps and commits of in-scope findings
  - A disputed finding of any severity gets one rebuttal and one recheck, then goes to the human
  - The human also decides a contract change, a blocker, an incomplete review, an accepted risk and a gate open after round 3
  - Update `SKILL.md`, `README.md`, `flow/approvals.md`, `flow/3-build.md`, `flow/4-code-review.md`, `flow/changes.md`,
    `review/3-findings.md`, `writing/code-review.md`, `team/rules.md` and `team/steps.md`
- [x] 14. Move the Codex review defaults to the current models
  - `gpt-6.1-sol` for plan and code at high effort and for the PR at medium, `gpt-6-luna` at high for a follow-up
- [x] 15. Add checkpoint commits and the history rewrite before the PR
  - The lead commits each accepted step and gate fix with `--no-gpg-sign`, and plan approval covers them
  - In PR REVIEW, after the close-out, the lead rewrites the unpushed history into a few atomic commits, checks each one
    in a temporary worktree, keeps a backup branch and gives the human the command that signs every commit on the branch
  - Update `SKILL.md`, `README.md`, `flow/approvals.md`, `flow/3-build.md`, `flow/5-pr-review.md` and `team/steps.md`
    in the `feature` skill, the root `README.md` and `hooks/README.md`
  - Probe it in a scratch repository: unsigned checkpoints for a step and a gate fix, a rewrite of only unpushed commits,
    the backup branch, the `Done when` checks on each rewritten commit and the command that signs the whole branch

## Gates

- [x] Plan review – PASS, round 2, 2026-10-01
- [x] Code review – PASS, round 1, 2026-10-01
