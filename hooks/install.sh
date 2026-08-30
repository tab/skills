#!/usr/bin/env bash
# Install the block-git-commit hook for Claude Code, Codex or both.
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
source_script="$root/block-git-commit.sh"
stamp="$(date +%Y%m%d%H%M%S)"

usage() {
  cat <<'USAGE'
Usage: hooks/install.sh [--claude] [--codex]

Installs block-git-commit.sh and registers it as a PreToolUse hook.
Both hosts are installed when no option is given.
USAGE
}

targets=""
while [ $# -gt 0 ]; do
  case "$1" in
    --claude) targets="$targets claude" ;;
    --codex) targets="$targets codex" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done
[ -z "$targets" ] && targets="claude codex"

command -v jq >/dev/null 2>&1 || { echo "jq is required" >&2; exit 1; }
[ -f "$source_script" ] || { echo "missing $source_script" >&2; exit 1; }

backup() {
  cp "$1" "$1.bak.$stamp"
  echo "  backed up $1.bak.$stamp"
}

install_claude() {
  local dir="$HOME/.claude/hooks"
  local settings="$HOME/.claude/settings.json"
  local current='{}'
  local add
  # $HOME stays literal, so the same settings.json works on every machine
  # shellcheck disable=SC2016
  local hook_command='"$HOME/.claude/hooks/block-git-commit.sh"'

  mkdir -p "$dir"
  install -m 755 "$source_script" "$dir/block-git-commit.sh"
  echo "Claude Code: installed $dir/block-git-commit.sh"

  if [ -s "$settings" ]; then
    if ! jq -e . "$settings" >/dev/null 2>&1; then
      echo "  $settings is not valid JSON, register the hook manually" >&2
      return 1
    fi
    if jq -e '[.. | strings | select(test("block-git-commit"))] | length > 0' "$settings" >/dev/null; then
      echo "  already registered in $settings"
      return 0
    fi
    backup "$settings"
    current="$(cat "$settings")"
  fi

  add="$(jq --arg command "$hook_command" '.hooks.PreToolUse[].hooks[].command = $command' \
    "$root/claude/settings.snippet.json")"
  printf '%s' "$current" | jq --argjson add "$add" '
    .hooks = (reduce ($add.hooks | to_entries[]) as $event
      ((.hooks // {}); .[$event.key] = ((.[$event.key] // []) + $event.value)))
  ' > "$settings.tmp"
  mv "$settings.tmp" "$settings"
  echo "  registered in $settings"
}

install_codex() {
  local dir="$HOME/.codex/hooks"
  local config="$HOME/.codex/config.toml"
  local hook_command="$dir/block-git-commit.sh"

  mkdir -p "$dir"
  install -m 755 "$source_script" "$dir/block-git-commit.sh"
  echo "Codex: installed $dir/block-git-commit.sh"

  if [ -s "$config" ]; then
    if grep -q 'block-git-commit' "$config"; then
      echo "  already registered in $config"
      return 0
    fi
    backup "$config"
    printf '\n' >> "$config"
  fi

  sed "s|__HOOK_COMMAND__|$hook_command|" "$root/codex/config.snippet.toml" >> "$config"
  echo "  registered in $config"
  echo "  open Codex once and trust the hook when prompted"
}

for target in $targets; do
  case "$target" in
    claude) install_claude ;;
    codex) install_codex ;;
  esac
done
