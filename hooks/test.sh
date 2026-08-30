#!/usr/bin/env bash
# Check that block-git-commit.sh denies real commits and lets everything else through.
set -uo pipefail

hook="$(cd "$(dirname "$0")" && pwd)/block-git-commit.sh"
failures=0

check() {
  local expected="$1" name="$2" payload="$3" actual="allow"
  printf '%s' "$payload" | "$hook" | grep -q '"deny"' && actual="deny"
  if [ "$actual" = "$expected" ]; then
    printf 'ok    %-24s %s\n' "$expected" "$name"
  else
    printf 'FAIL  %-24s %s (got %s)\n' "$expected" "$name" "$actual"
    failures=$((failures + 1))
  fi
}

# Claude Code sends the command as a shell string
check deny "claude plain" '{"tool_name":"Bash","tool_input":{"command":"git commit -m \"x\""}}'
check deny "claude chained" '{"tool_name":"Bash","tool_input":{"command":"git add . && git commit -m \"x\""}}'
check deny "claude sequenced" '{"tool_name":"Bash","tool_input":{"command":"cd /tmp; git commit --amend"}}'
check deny "claude -C dir" '{"tool_name":"Bash","tool_input":{"command":"git -C /tmp/repo commit -m x"}}'
check deny "claude -c key=value" '{"tool_name":"Bash","tool_input":{"command":"git -c user.name=x commit -m x"}}'
check deny "claude heredoc message" '{"tool_name":"Bash","tool_input":{"command":"git commit -F- <<EOF\nfix: x\nEOF"}}'

# Codex sends the command as an argv array
check deny "codex bash -lc" '{"tool_name":"shell","tool_input":{"command":["bash","-lc","git commit -m x"]}}'
check deny "codex bash -lc chained" '{"tool_name":"shell","tool_input":{"command":["bash","-lc","git add . && git commit -m x"]}}'
check deny "codex direct argv" '{"tool_name":"shell","tool_input":{"command":["git","commit","-m","x"]}}'

# The opt-in for an unsigned commit
check allow "claude unsigned" '{"tool_name":"Bash","tool_input":{"command":"git commit --no-gpg-sign -m x"}}'
check allow "codex unsigned" '{"tool_name":"shell","tool_input":{"command":["bash","-lc","git commit --no-gpg-sign -m x"]}}'

# Reading, searching and writing about commits
check allow "git status" '{"tool_name":"Bash","tool_input":{"command":"git status --short"}}'
check allow "git log --grep" '{"tool_name":"Bash","tool_input":{"command":"git log --grep=commit --format=%s"}}'
check allow "git push" '{"tool_name":"Bash","tool_input":{"command":"git push origin HEAD"}}'
check allow "commit message file" '{"tool_name":"Bash","tool_input":{"command":"cat .git/COMMIT_EDITMSG"}}'
check allow "grep for the phrase" '{"tool_name":"Bash","tool_input":{"command":"grep -r \"git commit\" docs/"}}'
check allow "echo the phrase" '{"tool_name":"Bash","tool_input":{"command":"echo \"run git commit yourself\""}}'
check allow "quoted doc heredoc" '{"tool_name":"Bash","tool_input":{"command":"cat > x.md <<'\''EOF'\''\nRun git commit here\nEOF"}}'
check allow "bare doc heredoc" '{"tool_name":"Bash","tool_input":{"command":"cat > x.md <<EOF\nRun git commit here\nEOF"}}'
check allow "codex doc heredoc" '{"tool_name":"shell","tool_input":{"command":["bash","-lc","cat > x.md <<EOF\nRun git commit here\nEOF"]}}'

# Payloads with no shell command
check allow "empty command" '{"tool_name":"Bash","tool_input":{"command":""}}'
check allow "other tool" '{"tool_name":"Read","tool_input":{"file_path":"/x"}}'
check allow "not json" 'not json at all'

if [ "$failures" -gt 0 ]; then
  echo "$failures hook checks failed"
  exit 1
fi
echo "Hook checks passed"
