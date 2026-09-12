# Conventional Commit skill

## Goal

Draft a Conventional Commit message that matches the current changes and the repository's recent style without creating the commit.

## Acceptance criteria

- **AC1** – staged changes take priority, with unstaged and relevant untracked files used only when nothing is staged
- **AC2** – recent non-merge subjects provide the scope, case and vocabulary for the message
- **AC3** – the result contains a copy-ready message and host-appropriate command but never stages or commits changes

## Boundaries

- The title aims for 50 characters and never exceeds 72 characters
- Unrelated changes produce separate proposed messages
- Ticket references, test plans and AI attribution are not invented

## Sources

- [Initial implementation – PR #1](https://github.com/tab/skills/pull/1)
- [Current behavior refinement – PR #6](https://github.com/tab/skills/pull/6)
- [Released in v0.5.0](https://github.com/tab/skills/releases/tag/v0.5.0)
