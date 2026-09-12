# Conventional Commit skill plan

Feature: [feature.md](feature.md)

Status: released

Current step: complete

Reconstruction: After implementation, from the feature sources and current files

## Implementation

- [x] [`SKILL.md`](../../../plugins/core/skills/cmt/SKILL.md) reads Git status, diff and history
  then returns the message and command – AC1, AC2 and AC3
- [x] [`agents/openai.yaml`](../../../plugins/core/skills/cmt/agents/openai.yaml) provides Codex discovery metadata

## Verification

- `make test` checks marketplace installation and `make validate` checks skill and plugin metadata
- No automated test checks the generated commit message
