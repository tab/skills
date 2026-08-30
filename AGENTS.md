# Repository Instructions

## Purpose

This repository packages reusable skills for Claude Code and Codex.
Each skill has one shared source under `plugins/tab/skills/<skill-name>/`.

## Before changing files

- Read `README.md`, `CONTRIBUTING.md` and the full affected skill
- Read every supporting file linked from the affected `SKILL.md`
- Check the current working tree and preserve unrelated changes
- Keep the change limited to the requested skill, metadata or documentation
- Verify current official requirements when changing skill or plugin formats

## Skill authoring

- Use a lowercase hyphenated folder name that matches the frontmatter `name`
- Keep `name` and `description` in the `SKILL.md` frontmatter
- Say what the skill does and when it should activate in the description
- Add a boundary when a similar request should not activate the skill
- Keep the main workflow, important decisions and safety rules in `SKILL.md`
- Move detailed conditional guidance to `references/` only when it reduces the main file
- Add scripts only when deterministic code is safer or easier to maintain than instructions
- Link every supporting file from `SKILL.md` and explain when to use it
- Assume the agent already knows common engineering practices
- Do not add filler, repeated instructions or speculative edge cases

## Shared compatibility

- Keep shared skill instructions neutral between Claude Code and Codex
- Do not hard-code host tool names when a capability can be described in neutral terms
- Keep host-specific metadata in plugin manifests or `agents/openai.yaml`
- Keep commands, paths and examples valid for the host where they are shown
- Preserve graceful fallback behavior when a capability is not available on one host
- Do not maintain separate Claude Code and Codex copies of the same `SKILL.md`

## Scope and safety

- Do not treat a skill invocation as permission for unrelated changes or external writes
- Require clear user approval before destructive or externally visible actions
- Keep read-only review and diagnosis separate from implementation
- Do not include secrets, credentials, internal URLs, user-specific paths or environment-only assumptions
- Do not add unrelated brands or company names
- Keep required repository URLs and automation identifiers unchanged
- Use relative paths inside skills and plugin packages

## Metadata and documentation

- Keep marketplace name `skills` and plugin name `tab` unless the user requests a rename
- Keep both plugin manifests on the same version
- Keep names, descriptions, author, license and keywords aligned across manifests
- Keep the README description aligned with the plugin metadata
- List skills alphabetically in `README.md`
- Document only marketplace installation
- Pin third-party workflow actions to full commit SHAs and keep the version in a comment
- Update `README.md` when installation, invocation or repository layout changes
- Update the README and landing page when the skill list changes

## Validation

- Run `make test` after changing skills, manifests or marketplace files
- Run `make validate` after changing skills, manifests or marketplace files
- Run `make docs` after changing the landing page
- Test representative requests after a meaningful skill behavior change
- Check direct activation, indirect activation, incomplete input, non-matching input and one important edge case
- Run `git diff --check` before handing off the change
- Review staged, unstaged and untracked files before declaring the work complete
- Use `feature/<name>` for new skills and `fix/<name>` for fixes
- Do not commit, push or publish unless the user asks

## Writing

- Keep one sentence on each source line when practical
- Avoid formal, promotional or AI-generated wording
- Preserve exact commands, paths, URLs, code and quotes
- Use the en dash `–` when prose needs a dash
- Do not add terminal punctuation to list items
- Align Markdown table pipes and separator columns

Use [the core review guide](.github/CORE_REVIEW.md) for the release review gate.
