# Simplified Technical English skill

## Goal

Provide a shared `ste` skill for English prose that must follow ASD-STE100 Simplified Technical English, Issue 9.

## Why

General readability rules do not define the controlled vocabulary and sentence rules of STE.
Agents need consistent guidance for replies, documents, comments and other English prose.

## Scope

In:

- A `ste` skill in the `core` plugin with a writing and review workflow
- Local Markdown references with concise rules and examples

Out:

- HTML content and external web links
- Stored copies of the full standard, dictionary or source metadata

## How it works

1. Identify the reader, purpose and prose to create or revise
2. Read the applicable local rules and examples
3. Write or revise the prose using STE
4. Review the result before returning or saving it

## Acceptance criteria

- **AC1** – The skill applies when STE is requested or required by active instructions
- **AC2** – `SKILL.md` links local rules and examples in `references/`
- **AC3** – The result preserves facts, uncertainty, technical meaning, exact source text and required formats
- **AC4** – The skill permits a full compliance claim only after a review of the applicable rules and vocabulary

## Decisions

- Use one shared skill for Claude Code and Codex to prevent different writing rules between hosts

## Details

[STE skill](../../../plugins/core/skills/ste/SKILL.md)
