# Contributing

## Workflow

1. Create `feature/<name>` or `fix/<name>` from `master`
2. Make one focused change
3. Run `make test` and `make validate`
4. Open a pull request
5. Wait for `checks.yaml` and complete the code review
6. Merge the pull request and confirm the `master` checks pass
7. Create a `v<version>` release when the change should be released

## Add or change a skill

1. Put the skill in `plugins/tab/skills/<skill-name>/`
2. Keep `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` in `plugins/tab/`
3. Use a lowercase hyphenated `name` and a short specific `description` in `SKILL.md`
4. Keep the main workflow in `SKILL.md` and move detailed conditional guidance to `references/`
5. Add `agents/openai.yaml` when Codex UI metadata helps users find the skill
6. Bump the version in both plugin manifests when any skill changes

Do not include credentials, internal URLs or environment-specific paths.

## Check locally

```bash
make test
make validate
```

Review changes with [the core review guide](.github/CORE_REVIEW.md).
Use [the code review prompt](.github/CODE_REVIEW_PROMT.md) when an agent runs the review.

## Check the landing page

Install dependencies and build the site:

```bash
make docs:install
make docs
```

Run a local preview with Astro:

```bash
make docs:dev
```

Or run the production image with Docker Compose:

```bash
make docs:up
```

Open `http://localhost:8080/skills/` for the Docker preview.
Use `make docs:down` to stop it.

## Release checklist

- Review the full diff
- Bump the plugin version when a skill changes
- Run `make test`
- Run `make validate`
- Install `tab@skills` and test each changed skill in a new session
