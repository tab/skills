---
name: cmt
description: >-
  Draft a Conventional Commit message for the current Git changes.
  Use when asked to write, draft or generate a commit message.
  Return the message and command, but never run git commit.
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git branch *) Bash(git rev-parse *) Read
---

# cmt

Draft a commit message that follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.
Match the style in the repository's recent Git history.
Never run `git commit`.

An optional hint may set the type, scope or intent.
Follow it when it matches the changes.

## Read the changes

Run:

```bash
git status --short
git diff --cached --stat
git diff --cached
git log --pretty=format:"%s" -30
```

- If anything is staged, describe only the staged changes
- If nothing is staged, inspect `git diff --stat`, `git diff` and the untracked files needed to understand the change
- If there are no changes, say so in one line and stop
- If the directory is not in a Git worktree, say that the skill needs to run inside one and stop
- State whether the message covers staged or unstaged changes
- Use recent subjects to learn the repository's type, scope, case and wording style
- If the repository has no history, use the defaults below

For a large diff, start with the stat, find the main change and then read the relevant parts of the full diff.

## Draft the message

Use this title shape:

```text
<type>[optional scope][!]: <description>
```

- Choose `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `style` or `revert` by intent
- Use a lowercase scope when one clear component owns the change or recent history uses that scope
- Leave the scope out when no useful scope fits
- Follow the repository's case style and use lowercase when no style is established
- Keep the full title at 60 characters or fewer
- Keep the description clear and specific, not vague or generic
- Use the main change, not the symptom or the fix at the description
- Use an imperative description with no trailing period
- Add `!` and a `BREAKING CHANGE:` footer when the change breaks compatibility

If the diff mixes unrelated concerns, propose separate commit messages.

Add a body only when it explains a reason, constraint or behavior that is not clear from the title.
Keep it short, separate it from the title with one blank line and wrap prose near 60 characters.
Do not invent ticket references, test plans or AI attribution.

## Return the result

Put each proposed message in its own copy-ready code block.
Then provide a command the user can run, but do not run it.

- For a title-only message, use one `git commit -m` argument
- For a message with a body, use `git commit -F-` with a quoted heredoc
- Keep the command in a separate code block
