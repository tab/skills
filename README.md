# Skills

Reusable workflows for Claude Code and Codex

## Install

Claude Code:

```bash
claude plugin marketplace add tab/skills
claude plugin install tab@skills
```

Codex:

```bash
codex plugin marketplace add tab/skills
codex plugin add tab@skills
```

Start a new session after installation.

## Repository layout

```text
.
├── .agents/plugins/              # Codex marketplace
├── .claude-plugin/               # Claude Code marketplace
├── .github/                      # Validation workflow and review guides
├── AGENTS.md                     # Repository instructions for agents
└── plugins/tab/
    ├── .codex-plugin/
    └── .claude-plugin/
```

Claude Code and Codex use the same `SKILL.md` for each skill.
Host-specific metadata stays in the matching manifest or `agents/openai.yaml`.

## Developer notes

- Add new skills under `plugins/tab/skills/`
- Keep both plugin manifests on the same version
- Run `make test` to test installation with Claude Code and Codex
- Run `make validate` to validate the repository and plugin manifests

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checks.
Licensed under the [MIT License](LICENSE).
