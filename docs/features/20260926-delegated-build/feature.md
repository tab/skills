# Delegated delivery team

## Goal

Let one lead agent deliver a feature through a small team of agents.
The lead plans, briefs, checks and commits. The team writes, reviews and tests.
Every commit passes an independent review.

## Why

Today one agent does everything in one session.
On a long feature it loses track, changes more than asked and reviews its own work.
Reviews repeat without new evidence, and nothing stops the loop.

## Scope

In:

- Five role agents: `architect`, `developer`, `code-reviewer`, `qa`, `technical-writer`
- A team guide: who does what, how to brief a role and when to stop
- A `coverage` skill that raises test coverage after the build
- An adversarial review that tries to break the change after the code gate
- One `feature` skill: the `feature-review` skill merges into it
- Templates and a worked example for `feature.md`, `plan.md` and `code-review.md`
- Rules that freeze `feature.md` after approval and let the lead change only the state in `plan.md`
- The files stop at the PR. The PR review runs on GitHub and changes no file
- A skill layout that reads without documentation: `templates/`, `examples/`, `writing/`, `flow/`, `team/`, `review/`.
  A number in a file name means order. No number means it applies at any point
- Checkpoint commits during the build and the code gate, rewritten into a few atomic commits before the PR

Out:

- A script that runs a plan without a human
- An agent that commits, pushes, opens a PR, merges or releases
- A change to the review resolver. The bundled defaults get only the current Codex models, and moving them changes only their path

## How it works

1. The lead writes the contract and the plan. The human approves each one
2. For each plan step, a `developer` makes the change and a `code-reviewer` checks it
3. At most two review rounds per step. Then the human decides
4. The lead commits each accepted step and each gate fix as an unsigned checkpoint. Plan approval covers these local commits
5. After the last step, `qa` raises coverage and the `technical-writer` updates the docs
6. The code gate reviews the whole change. The agents settle its findings among themselves. An adversarial pass may follow
7. Before the push, the lead rewrites the unpushed history into a few atomic commits and keeps a backup branch.
   The human signs them, reviews the log and approves the push and the PR. CI and any PR reviewer run on GitHub, read-only
8. A fix after the PR review is a normal commit. Nobody edits `feature.md` or `plan.md` after the PR opens

## Acceptance criteria

- **AC1** – The plugin ships the five role agents
- **AC2** – The `code-reviewer` has no edit tools, and its rules forbid writing tracked files through the shell
- **AC3** – The team guide says which role works in which phase, what a brief holds and when to stop
- **AC4** – A reviewer rejects a test that cannot fail and a finding that contradicts a recorded decision
- **AC5** – After two review rounds the lead stops and asks the human
- **AC6** – The `coverage` skill sets floors: 90% for hard code, 95% for medium, 100% for easy
- **AC7** – `qa` sorts each adversarial finding into fix now, backlog or drop, with evidence from the base branch
- **AC8** – A Claude gate runs in the `code-reviewer` agent with the resolved model
- **AC9** – The `feature-review` skill is gone. Its rules live in the `feature` skill, and a reviewer can reach them from any project
- **AC10** – The `feature` skill has templates and a complete example
- **AC11** – No agent edits `feature.md` after approval. The lead edits only the state lines in `plan.md`
- **AC12** – `plan.md` tracks two gates, plan review and code review. No rule writes a file after the PR opens
- **AC13** – Each file has one purpose and a name that says it. A reviewer starts at `review/1-prepare.md` and never reads `flow/` or `team/`
- **AC14** – `make test` and `make validate` pass
- **AC15** – After plan approval, the lead runs the build and the code gate without stopping.
  It asks the human only about a disagreement that one rebuttal and one recheck leave open, a contract change, a blocker,
  an incomplete review, an accepted risk or a gate still open after round 3
- **AC16** – The lead commits each accepted step and gate fix as an unsigned checkpoint.
  Before the push, it rewrites only unpushed history into a few atomic commits, each passing the `Done when` checks on its own,
  keeps a backup branch and gives the human the command that signs every commit on the branch

## Decisions

- A role name is a job, not a seniority level. The brief sets the model
- Only the lead commits, with the `cmt` skill: a short title, and a short body only when needed
- Checkpoint commits record each step. The rewrite before the PR groups them into a few atomic commits, each file in one commit where it can be
- Agents commit with `--no-gpg-sign`. Only the human signs every commit on the branch, after the rewrite and before the push
- A better idea during the build goes to the backlog or to the human. It never rewrites the spec
- The shared text names no host model, project or language. The agents are a Claude Code extra
- The review settings files keep their names, so existing projects keep working
- Removing `feature-review` is a breaking change. The next release is a major version

## Details

The rules live in the plugin, not here:

- Roles and briefs: `plugins/workflow/agents/`
- Team rules, briefs and steps: `plugins/workflow/skills/feature/team/`
- Coverage tiers: `plugins/workflow/skills/coverage/SKILL.md`
