#!/usr/bin/env bash
# PreToolUse hook for Claude Code and Codex.
# Deny `git commit` from a tool call, so the commit stays with the user.
# --no-gpg-sign is how the user opts in to an unsigned commit, so it is allowed.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

payload="$(cat)"

# Claude Code sends a shell string, Codex an argv array.
# The array is read twice: one element per line catches `bash -lc "git commit"`,
# and the flat line catches a direct `git commit` call.
lines="$(printf '%s' "$payload" | jq -r '
  .tool_input // {} | (.command // .cmd // empty) as $c
  | if ($c | type) == "array" then ($c | map(tostring) | join("\n"))
    elif ($c | type) == "string" then $c
    else "" end
' 2>/dev/null)"

flat="$(printf '%s' "$payload" | jq -r '
  .tool_input // {} | (.command // .cmd // empty) as $c
  | if ($c | type) == "array" then ($c | map(tostring) | join(" "))
    elif ($c | type) == "string" then $c
    else "" end
' 2>/dev/null)"

[ -z "$lines" ] && exit 0

case "$lines" in *--no-gpg-sign*) exit 0 ;; esac

# Drop heredoc bodies, so a document that only shows a git commit line is not a match.
# The line opening the heredoc is kept, since it may be the real invocation.
strip_heredocs() {
  awk '
    BEGIN { q = sprintf("%c", 39); delim = "" }
    delim != "" {
      t = $0
      sub(/^[ \t]+/, "", t); sub(/[ \t]+$/, "", t)
      if (t == delim) delim = ""
      next
    }
    {
      if (match($0, /<<-?[ \t]*/)) {
        rest = substr($0, RSTART + RLENGTH)
        gsub(q, "", rest); gsub(/"/, "", rest)
        if (match(rest, /^[A-Za-z_][A-Za-z0-9_]*/)) delim = substr(rest, RSTART, RLENGTH)
      }
      print
    }
  '
}

# `git commit` at a command position, allowing global flags such as -C <dir> or -c k=v
COMMIT='(^|[;&|({])[[:space:]]*git[[:space:]]+((-[cC][[:space:]]+[^[:space:]]+|--[a-z-]+(=[^[:space:]]+)?)[[:space:]]+)*commit([[:space:]]|$)'

is_commit() {
  printf '%s\n' "$1" | strip_heredocs | grep -qE "$COMMIT"
}

if is_commit "$lines" || is_commit "$flat"; then
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Do not run git commit. The commit belongs to the user: stage the files, then give them the git commit command to run. If the user has allowed an unsigned commit this time, re-run with --no-gpg-sign."}}
JSON
  exit 0
fi

exit 0
