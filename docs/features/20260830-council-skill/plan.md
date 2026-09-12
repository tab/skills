# Council skill plan

Feature: [feature.md](feature.md)

Status: released

Current step: complete

Reconstruction: After implementation, from the feature sources and current files

## Implementation

- [x] [`SKILL.md`](../../../plugins/thinking/skills/council/SKILL.md) defines the evidence pack, five roles
  anonymous review, fallback and verdict – AC1, AC2 and AC3
- [x] [`agents/openai.yaml`](../../../plugins/thinking/skills/council/agents/openai.yaml) provides Codex discovery metadata

## Verification

- `make test` checks marketplace installation and `make validate` checks skill and plugin metadata
- No automated test checks the advisor, peer review and verdict flow
