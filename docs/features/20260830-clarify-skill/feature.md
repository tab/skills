# Clarify skill

## Goal

Explain an expectation mismatch from current evidence without silently changing the system.

## Acceptance criteria

- **AC1** – the skill identifies the expected and observed behavior with the relevant project, revision, environment and timeframe
- **AC2** – it checks the smallest decisive evidence set before classifying the mismatch
- **AC3** – it leads with the supported conclusion and names evidence that could not be verified

## Boundaries

- Clarification is read-only unless the user also asks for a change
- Repository behavior and deployed behavior remain separate evidence sources
- Ask one short question only when the answer cannot be verified
- Recheck the evidence when the user rejects the explanation

## Sources

- [Initial implementation – PR #4](https://github.com/tab/skills/pull/4)
- [Released in v0.2.0](https://github.com/tab/skills/releases/tag/v0.2.0)
