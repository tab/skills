# Rules

Read this when the primary agent delegates to roles: the roles, what no role may do, the stopping rules and how to read a report.

The primary agent leads the team: it briefs, verifies, decides and commits.
It keeps its effort for judgment.
Every commit has passed an independent check.

## Roles

Each role's body is its agent file in the plugin folder, named below.

- `architect` – `agents/architect.md`
  - Edits `feature.md` and `plan.md`
  - Runs the survey the writing rules ask for
  - Returns a draft and its open questions, as the `Architect report`
- `developer` – `agents/developer.md`
  - Edits the step's files
  - Runs the package checks, with a timeout
  - Returns the diff, check tails and what was left out, as the `Developer report`
- `code-reviewer` – `agents/code-reviewer.md`
  - Edits nothing
  - Runs repeated checks and mutation checks
  - Returns `ACCEPT` or `CHANGES NEEDED` at `file:line`, as `Code review – step <n>, round <1 or 2>`,
    or the gate result of the `review/` files
- `qa` – `agents/qa.md`
  - Edits test files
  - Runs the reproduction, the merge-base run and coverage
  - Returns a disposition as `QA triage – <finding ID>`, or a coverage delta as `QA coverage`
- `technical-writer` – `agents/technical-writer.md`
  - Edits docs, READMEs and the site
  - Runs the docs build and the link check
  - Returns the changed files, or a PR title and body, as the `Technical writer report`

Also:

- A name is a job, never a level
- The brief sets the model, and the effort where the host lets it
- The primary agent may delegate the `architect` drafts and names the model in the brief.
  A draft helps only a session that runs on a smaller model than the agent
- The `architect` drafts and never approves. The plan gate and the human keep approval

On a host with custom agents, the roles are the plugin agents `workflow:<name>`.
A project specialises a role by shipping an agent with the same name. Prefer that agent when it exists.
On a host without them, the role's body is `agents/<name>.md` in the plugin folder when the host ships it.
The primary agent gives that body to a delegated session.
Otherwise it runs the role's checklist from the role list itself.
It says in its phase report which one it did.

## What no role may do

- No role stages, commits, pushes, opens a PR, merges or releases
- Only the primary agent commits

## Stopping rules

Enforce these rules whenever a round, a dispute or a blocked agent could loop.
Each role follows its own rules inside its body.

- In the step loop, after round two with an item open, stop. Ask the human to accept, run one more round or move the item to the backlog
- Treat a verdict without its evidence lines as `INCOMPLETE`. Ask the `code-reviewer` once, then treat the step as unchecked
- Reject a finding that contradicts a line of `feature.md` under Scope or Decisions, and quote that line
- In the step loop, give a dispute with the `code-reviewer` one rebuttal with evidence. Then the human decides
- The code gate stops only as [the stretch](../flow/approvals.md#run-the-build-and-the-code-gate-as-one-stretch) says
- Give a `developer` that returns `BLOCKED` one new brief. Then the human decides
- Settle a question in a report from the artifacts, or take it to the human, before the next brief.
  A design choice the step left open never arrives as code
- Add the known bug a report names to the backlog. No test is skipped to hide it, and its test goes away
- Accept a line the coverage pass leaves uncovered when the report gives its reason. No production change exists to reach it
- Give one agent at a time the commands that touch the whole tree: the full build, the end-to-end suite and the formatter.
  Every other agent runs package-scoped commands
- Run two `developer` agents at once only when you have checked that their steps touch disjoint files.
  Name those files in each brief. Each agent works in its own worktree. Bring each result back into the branch yourself
- An agent that hits its turn limit returns its partial work. Resume it or re-brief it
- After an agent dies, read the status and the diff. Keep or reset only the edits of that agent.
  Accepted steps stay in their checkpoints. The next brief says what was kept
- Keep no number that drifts in the records, such as a commit count

## Reports

Each role returns the report its body defines, as the role list names.

- Read `Brief wrong` first. Fix the brief and start the role again.
  When the step itself contradicts `feature.md`, the fix belongs in the plan or the contract and reopens phases
  as [the reopen rules](../flow/changes.md#reopen-affected-work) say
- Check the files touched against what the role may edit
