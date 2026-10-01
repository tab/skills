# Briefs

Read this before you brief a role: how a step is written for delegation and what every brief names.

## A step written for delegation

A step in `plan.md` follows [the plan rules](../writing/plan.md): one line, and two or three sub-bullets for a complex step.
The plan names no files, criterion or proof.
The brief of a delegated step names them, so a `developer` can take it alone:

- **Files** – every file the step may change, its tests included
- **Acceptance criterion** – the criterion the step delivers
- **Proof** – the check or observation that shows the criterion holds

For example:

```markdown
- [ ] 2. Reject expired, used and replaced tokens
  - Check the age and the used flag in the token lookup
  - A new request deletes the user's older tokens
```

## The brief

Each role body lists what its brief names. Every brief names:

- The feature folder, and for a delegated session, the role body to follow
- The model, and the effort where the host lets it
- The step or the job, its files and its acceptance criterion
- The checks, each with its timeout, and the repeat count for the `code-reviewer`.
  The count is 1 by default, and more for a test that depends on timing or concurrency
- The files other agents own at the same time, which this agent must not touch
- The command that touches the whole tree when this agent owns it
- On a second round, the numbered required changes and the fix diff

Name files, diffs and commands. Do not restate facts from memory.
Each role body defines its report, so the brief points to it and does not restate it.

For example, a `developer` brief:

```markdown
Role: `developer`. Follow your role body and return its report.
Model: `<model>`.
Feature folder: `docs/features/<folder>/`. Read `feature.md` and step 2 of `plan.md`.
Step 2 – AC3. Files you may change: `<path>`, `<path>`.
Checks: `<package test command>`, 300 s timeout each.
Files another agent owns: `<path>`.
Tree-wide commands: none.
```
