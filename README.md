# <img src="plugins/tab/assets/toolbox.svg" alt="" width="28">&nbsp;Agent Tools

Usable workflows for Claude Code and Codex

[tab.github.io/skills](https://tab.github.io/skills/)

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

## Skills

| Skill      | Description                                                            |
|------------|------------------------------------------------------------------------|
| `clarify`  | Explain expectation mismatches with current evidence                   |
| `cmt`      | Draft a Conventional Commit message for the current Git changes        |
| `council`  | Stress-test an engineering decision with five independent perspectives |
| `humanify` | Make prose, Markdown and code comments clear and natural               |

Use:

- `/cmt` in Claude Code
- `$cmt` in Codex

If `/cmt` conflicts with another command, use `/tab:cmt` in Claude Code.

## Repository layout

```text
.
├── .agents/plugins/              # Codex marketplace
├── .claude-plugin/               # Claude Code marketplace
├── .github/                      # CI workflows and review guides
├── AGENTS.md                     # Repository instructions for agents
├── docs/                         # Astro landing page
└── plugins/tab/
    ├── .codex-plugin/
    ├── .claude-plugin/
    └── skills/                    # Shared skill source
```

Claude Code and Codex use the same `SKILL.md` for each skill.
Host-specific metadata stays in the matching manifest or `agents/openai.yaml`.

## Developer notes

- Add new skills under `plugins/tab/skills/`
- Keep both plugin manifests on the same version
- Run `make test` to test installation with Claude Code and Codex
- Run `make validate` to validate the repository and plugin manifests
- Run `make docs:install` once and `make docs` to build the landing page
- Run `make docs:dev` for Astro or `make docs:up` for Docker preview

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checks.

## License

Distributed under the MIT License. See `LICENSE` for more information.
