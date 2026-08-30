# Code Review Prompt

Review all current changes in this repository.

Read these files first:

- `AGENTS.md`
- `.github/CORE_REVIEW.md`
- `README.md`
- `CONTRIBUTING.md`

Then inspect staged, unstaged and untracked files.
For every changed skill, read its complete `SKILL.md` and every linked supporting file.

Check:

- User scope and unrelated changes
- Skill activation, boundaries, workflow and stopping conditions
- Safety, permissions and external side effects
- Shared Claude Code and Codex behavior
- Marketplace and plugin metadata consistency
- README skill list, installation and invocation examples
- Credentials, internal URLs, local paths and unrelated names
- Workflow action pins
- Markdown clarity and formatting

Run:

```bash
make test
make validate
git diff --check
```

Do not edit files, commit, push or publish.
Do not invent a problem when the evidence does not support one.
Do not report unrelated existing issues unless the change makes them worse.

Return findings first, ordered by severity.
For each finding, include:

- Severity
- Exact file and line
- Problem
- Impact
- Requested change

If there are no findings, say `No blocking findings`.
Then list the validation commands and results.
