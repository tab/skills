# Humanify skill plan

Feature: [feature.md](feature.md)

Status: released

Current step: complete

Reconstruction: After implementation, from the feature sources and current files

## Implementation

- [x] [`SKILL.md`](../../../plugins/core/skills/humanify/SKILL.md) holds the meaning, evidence and format boundaries – AC1 and AC3
- [x] [`references/tells.md`](../../../plugins/core/skills/humanify/references/tells.md) identifies wording patterns to check – AC2
- [x] [`references/voice.md`](../../../plugins/core/skills/humanify/references/voice.md) adapts the result to its reader and format – AC3
- [x] [`agents/openai.yaml`](../../../plugins/core/skills/humanify/agents/openai.yaml) provides Codex discovery metadata

## Verification

- `make test` checks marketplace installation and `make validate` checks skill and plugin metadata
- No automated test checks meaning preservation or rewrite quality
