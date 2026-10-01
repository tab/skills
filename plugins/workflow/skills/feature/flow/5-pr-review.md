# 5. PR review

Read this when you enter the `PR REVIEW` phase: what it must finish, who works in it, how the history is rewritten and what the
release after it may do.

## Must finish

- Close out the artifacts before the push, within [the freeze rules](changes.md#after-approval).
  A change to `feature.md` needs the human's approval
- This is the last update of the files: `Status: implemented`, the code gate passed and `Current step` names the PR
- The primary agent may ask the `technical-writer` to draft the PR title and body
- Resolve the intended source branch, and ask before creating or switching the source branch
- Commit the close-out as a checkpoint, as [the commit rules](../team/steps.md#commits) say
- [Rewrite the history](#rewrite-the-history), then [hand over the signing](#hand-over-the-signing)
- Ask separately before the push and the PR
- CI and any PR reviewer run on the PR. They write PR comments, never a file
- Fix an accepted finding with a new unsigned commit after the human's approval and push it to the PR.
  No file changes, and no new review of the files
- The phase ends when the human approves the merge

## Rewrite the history

Entering `PR REVIEW` covers two local actions without another approval: the close-out checkpoint and this rewrite.
Every branch action other than the backup branch, and every push and PR action, still needs its own approval.

1. Start from a clean working tree, so the reset sweeps in no uncommitted file. Ignored files do not count.
   When it is not clean, stop and ask the human. Never stash, commit or discard a change the feature did not make.
   Fetch, then take as the base the upstream head of the branch when it has been pushed, otherwise the merge base with the
   target branch. Stop and ask the human when the upstream head is not an ancestor of `HEAD`.
   Never rewrite a pushed commit. When a merge from the target branch sits after the base, stop and ask the human
2. Keep the old history on the backup branch `backup/<branch>-before-rewrite`.
   When that name exists, add a numeric suffix
3. Group the commits after the base into a few atomic commits by purpose.
   Put each file in one commit where it can be, and order the commits so each one stands on its own
4. Write each message in the project's convention, drafted with the `cmt` skill when it is available.
   A breaking change says so in the message the way the convention does
5. Rebuild the history with a mixed reset to the base, then stage each group and commit it with `git commit --no-gpg-sign`
6. Check each new commit with the runnable `Done when` checks in a temporary worktree from `git worktree add --detach <dir> <commit>`.
   Remove the worktree afterwards
7. Check that the final tree equals the backup: `git diff <backup> HEAD` is empty
8. When a commit fails its checks, regroup.
   When no grouping passes, restore the backup with `git reset --hard <backup>`, safe because the tree started clean,
   and report why

The rewrite leaves the final tree unchanged, so it does not reopen the code gate.
The human deletes the backup branch after the merge. No agent deletes it.

## Hand over the signing

The primary agent never signs.
Its phase report shows the new log and gives the human two commands with `<base>` filled in:

- `git rebase --exec 'git commit --amend --no-edit -S' <base>` – signs every commit after the base
- `git log --format='%h %G? %s' <base>..HEAD` – each line should show `G`, or `U` for a key you have not marked as trusted

Then it asks for the push.
After the PR opens, a fix is a new unsigned commit.
The signing command then takes the pushed head as its base, so only the new commits change.

## Who works

- Roles: the `technical-writer` drafts the PR title and body
- Primary agent: closes out the artifacts, commits the close-out and rewrites the history

## Release

- Perform only the approved merge action
- Ask separately before publishing a release or starting another rollout action
- Change no file
