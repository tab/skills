# Humanify skill

## Goal

Make prose, Markdown and code comments clear and natural without changing their meaning, facts or certainty.

## Acceptance criteria

- **AC1** – the result keeps the original meaning and level of certainty
- **AC2** – filler, repetition, vague claims and mechanical wording are removed when this improves the text
- **AC3** – Markdown, links, code, commands, technical terms and machine-read fields remain valid

## Boundaries

- Do not add unsupported detail, fake opinions, stories or mistakes
- Preserve exact quotes, commands, paths, URLs and required templates
- Match the reader, format and surrounding style

## Sources

- [Initial implementation – PR #3](https://github.com/tab/skills/pull/3)
- [Released in v0.2.0](https://github.com/tab/skills/releases/tag/v0.2.0)
