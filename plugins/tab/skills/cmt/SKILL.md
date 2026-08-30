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
git log --no-merges --format="%s" -30
```

- If anything is staged, describe only the staged changes
- If nothing is staged, inspect `git diff --stat`, `git diff` and the untracked files needed to understand the change
- If there are no changes, say so in one line and stop
- If the directory is not in a Git worktree, say that the skill needs to run inside one and stop
- State whether the message covers staged or unstaged changes

For a large diff, start with the stat, find the main change and then read the relevant parts of the full diff.

## Read the repository style

Read the subjects from the `git log` above.
Ignore any `Revert`, `fixup!` or `squash!` subject, since Git wrote it rather than the author.

- **Scope** – when the subjects are consistently scoped, always emit a scope; when they are mixed or scopeless, use a scope only when one component clearly owns the change
- **Case** – capitalize the description when the subjects capitalize it, and keep it lowercase when they do not
- **Vocabulary** – reuse the types and scope names the log already uses instead of inventing new ones
- **Wording** – follow the phrasing and length of the existing subjects

Fall back to a lowercase scope and a lowercase description when the repository has no history.

## Draft the message

Use this title shape:

```text
<type>[optional scope][!]: <description>
```

- Choose `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `style` or `revert` from the intent of the change, not from the files it touches
- Use the scope and case the log shows
- Aim for 50 characters in the title and never pass 72
- Describe the main change, not the symptom or the mechanics of the fix
- Use an imperative description with no trailing period
- Add `!` and a `BREAKING CHANGE:` footer when the change breaks compatibility

If the diff mixes unrelated concerns, propose separate commit messages instead of dropping the scope or widening the description.

Pick the shortest of the three shapes below that still carries the change.
The examples capitalize the description, but the log decides the case.

A title alone covers a small self-contained change, such as a version bump or a typo fix:

```text
chore(release): Bump version to 0.4.0
```

A prose body records the reason, constraint or behavior behind one change:

```text
fix(log): Fix lifecycle logs

Route the shutdown messages to debug so an info-level run no longer
prints them on every exit
```

A bullet body lists several related changes that belong in one commit:

```text
fix(log): Fix lifecycle logs

- Route the shutdown messages to debug so an info-level run stays quiet
- Close the done channel after the Sentry flush
- Drop the duplicate stop line from the relay
```

Separate the body from the title with one blank line and wrap prose near 72 characters.
Do not invent ticket references, test plans or AI attribution.

## Return the result

Put each message in its own copy-ready code block, then give the command in a second block.
Never run the command.

- Title only – one `git commit -m` argument
- Title and body – `git commit -F-` with a quoted heredoc, so blank lines and bullets survive
- Never stack `-m "title" -m "body"`, since each `-m` starts its own paragraph and mangles a bullet list

In Claude Code, prefix the command with `!` so the user can run it from the prompt:

```text
!git commit -m "chore(release): Bump version to 0.4.0"
```

```text
!git commit -F- <<'EOF'
fix(log): Fix lifecycle logs

- Route the shutdown messages to debug so an info-level run stays quiet
- Close the done channel after the Sentry flush
EOF
```

On other hosts, show the command without the `!`.
