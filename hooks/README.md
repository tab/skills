# Hooks

Optional hooks for Claude Code and Codex.

## block-git-commit

Denies `git commit` from an agent tool call, so the commit stays with the user.
It matters most when commits are signed, since the agent cannot reach the signing key.

The hook matches `git commit` at a command position, so `git add . && git commit` is caught along with a plain call.
It also matches the `git -C <dir>` and `git -c <key>=<value>` forms.
Nothing else is blocked: `git status`, `git log`, `git push`, a `grep` for the phrase and a command that writes a `git commit` line into a document all run as usual.
A command that carries `--no-gpg-sign` runs too, for the times an unsigned commit is allowed.

## Install

```bash
hooks/install.sh            # Claude Code and Codex
hooks/install.sh --claude
hooks/install.sh --codex
```

The script needs `jq`.
It copies `block-git-commit.sh` into the host hook directory, registers it as a `PreToolUse` hook and backs up every file it edits.
Running it again when the hook is already registered changes nothing.
Start a new session afterwards.

Codex reviews a new hook before it runs, so open Codex once and trust the hook when prompted.

## Install without the script

Copy `block-git-commit.sh` to a path that will not move and make it executable.
Merge the matching snippet and replace `__HOOK_COMMAND__` with the path to the copy.

- Claude Code – merge [`claude/settings.snippet.json`](claude/settings.snippet.json) into `~/.claude/settings.json`
- Codex – append [`codex/config.snippet.toml`](codex/config.snippet.toml) to `~/.codex/config.toml`

## Uninstall

Remove the hook entry from `~/.claude/settings.json` or `~/.codex/config.toml`, then delete the copied script.

## Test

```bash
make hooks:test
```

`test.sh` sends both host payload shapes through the hook and checks each decision.
Add a case when changing what the hook matches.
