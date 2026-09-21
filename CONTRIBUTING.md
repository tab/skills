# Contributing

## Workflow

1. Create `feature/<name>` or `fix/<name>` from `master`
2. Make one focused change
3. Run `make test` and `make validate`
4. Open a pull request
5. Wait for `checks.yaml` and complete the code review
6. Merge the pull request and confirm the `master` checks pass
7. Create a `<plugin>-v<version>` release for each changed plugin when the change should be released

## Add or change a skill

Choose the smallest matching plugin:

- `core` – daily skills or shared capabilities used by other plugins
- `workflow` – feature planning, delivery, review and backlog skills
- `thinking` – optional deep analysis for important engineering decisions

Do not put a skill in `core` only because it is useful.

1. Put the skill in `plugins/<plugin-name>/skills/<skill-name>/`
2. Keep `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` in the selected plugin
3. Use a lowercase hyphenated `name` and a short specific `description` in `SKILL.md`
4. Keep the main workflow in `SKILL.md` and move detailed conditional guidance to `references/`
5. Add `agents/openai.yaml` when Codex UI metadata helps users find the skill
6. Bump the plugin version in both of its manifests when an installed skill changes

Do not include credentials, internal URLs or environment-specific paths.

## Check locally

```bash
make test
make validate
```

Run `make hooks:test` when changing `hooks/`.

Review changes with [the core review guide](.github/CORE_REVIEW.md).
Use [the code review prompt](.github/CODE_REVIEW_PROMT.md) when an agent runs the review.

## Test an unreleased skill

Run the host from the target project and load the skill from this checkout.
Replace `<skills-repo>`, `<project>` and `<profile>` before running the examples.

Claude Code loads a local plugin for one session:

```bash
cd <project>
claude \
  --plugin-dir <skills-repo>/plugins/core \
  --plugin-dir <skills-repo>/plugins/workflow \
  --add-dir <skills-repo>
```

Pass every plugin needed by the test with its own `--plugin-dir`.
Keep `--add-dir <skills-repo>` so the session can read references linked from each `SKILL.md`.

Codex can load one changed skill directly without replacing an installed marketplace plugin:

```bash
cd <project>
codex \
  --profile <profile> \
  --model <model> \
  -c 'model_reasoning_effort="medium"' \
  --add-dir <skills-repo> \
  -c 'skills.config=[{path="<skills-repo>/plugins/workflow/skills/feature-review/SKILL.md",enabled=true}]'
```

For a non-interactive test, put the shared options before `exec` and add `--ephemeral` after it.
Use the smallest review model and reasoning effort that match the gate risk.
This direct skill setup tests behavior, while `make test` and `make validate` test plugin packaging and metadata.

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

## Versioning

Each plugin carries its own version in both of its manifests and follows [semantic versioning](https://semver.org/):

- **Major** – an incompatible change, such as removing or renaming a skill
- **Minor** – a new skill or a new feature
- **Patch** – a fix or another change that keeps current behavior

Bump only the plugins the change touches, in their own commit, separate from the change it releases.
A release tag names one plugin and its version, such as `core-v1.1.0`.
A change that does not affect what users install or run, such as contributor documentation or CI, needs no bump.

## Release checklist

- Review the full diff
- Bump each changed plugin to match the change type
- Run `make test`
- Run `make validate`
- Install each changed plugin from the `skills` marketplace and test its changed skills in a new session
