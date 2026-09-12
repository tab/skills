# <img src="plugins/core/assets/toolbox.svg" alt="" width="28">&nbsp;Agent Tools

Usable workflows for Claude Code and Codex

[tab.github.io/skills](https://tab.github.io/skills/)

## Install

Claude Code:

```bash
claude plugin marketplace add tab/skills

claude plugin install core@skills
claude plugin install thinking@skills
claude plugin install workflow@skills
```

Codex:

```bash
codex plugin marketplace add tab/skills

codex plugin add core@skills
codex plugin add thinking@skills
codex plugin add workflow@skills
```

Start a new session after installation.

`core` and `workflow` cover daily feature work.
`thinking` adds the optional `council` workflow for important decisions.

## Skills

| Skill              | Plugin     | Description                                                            |
|--------------------|------------|------------------------------------------------------------------------|
| `clarify`          | `core`     | Explain expectation mismatches with current evidence                   |
| `cmt`              | `core`     | Draft a Conventional Commit message for the current Git changes        |
| `humanify`         | `core`     | Make prose, Markdown and code comments clear and natural               |
| `council`          | `thinking` | Stress-test an engineering decision with five independent perspectives |
| `backlog`          | `workflow` | Track deferred work and preserve closed decisions                      |
| `feature`          | `workflow` | Plan and deliver a feature with clear scope and durable context        |
| `feature-backfill` | `workflow` | Restore feature artifacts from repository history                      |
| `feature-review`   | `workflow` | Review a feature plan, implementation or PR against its contract       |

Use:

- `/cmt` in Claude Code
- `$cmt` in Codex

If `/cmt` conflicts with another command, use `/core:cmt` in Claude Code.

## Feature workflow

The `feature` skill runs six visible phases with human checkpoints and independent plan, code and PR reviews.
See [the feature workflow guide](plugins/workflow/skills/feature/README.md) for the pipeline, artifacts, review modes and settings.

## Hooks

`hooks/` holds optional `PreToolUse` hooks.
Install them manually:

```bash
hooks/install.sh
```

`block-git-commit` denies `git commit` from a tool call, so the commit stays with the user.
See [hooks/README.md](hooks/README.md).

## Repository layout

```text
.
├── .agents/plugins/              # Codex marketplace
├── .claude-plugin/               # Claude Code marketplace
├── .github/                      # CI workflows and review guides
├── AGENTS.md                     # Repository instructions for agents
├── docs/
│   ├── features/
│   │   ├── backlog.md            # Prioritized deferred work and closed decisions
│   │   └── YYYYMMDD-<slug>/
│   │       ├── code-review.md     # Current code or PR review handoff, created when needed
│   │       ├── feature.md        # Goal, scope and behavior
│   │       └── plan.md           # Markdown tasks, checks and current progress
│   └── src/                      # Astro landing page source
├── hooks/                        # Optional hooks, installed manually
└── plugins/
    ├── core/
    │   ├── .claude-plugin/
    │   ├── .codex-plugin/
    │   └── skills/                # Daily shared skills
    ├── thinking/
    │   ├── .claude-plugin/
    │   ├── .codex-plugin/
    │   └── skills/                # Optional decision workflows
    └── workflow/
        ├── .claude-plugin/
        ├── .codex-plugin/
        └── skills/                # Feature lifecycle skills
```

Claude Code and Codex use the same `SKILL.md` for each skill.
Host-specific metadata stays in the matching manifest or `agents/openai.yaml`.

## Developer notes

- Add new skills under `plugins/<plugin-name>/skills/`
- Keep every plugin manifest on the same repository release version
- Run `make test` to test installation with Claude Code and Codex
- Run `make validate` to validate the repository and plugin manifests
- Run `make hooks:test` to check the optional hooks
- Run `make docs:install` once and `make docs` to build the landing page
- Run `make docs:dev` for Astro or `make docs:up` for Docker preview

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checks.

## License

Distributed under the MIT License. See `LICENSE` for more information.
