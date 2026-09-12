# Feature workflow

## Goal

Add a small shared workflow that helps a human and two agents plan, build and review a software feature without losing scope or reasoning.

The workflow must reduce repeated manual coordination while keeping the human in control of scope, merge and release decisions.

## Context

The current process works, but its useful context often stays in chat sessions.

This makes progress hard to track, lets deferred work interrupt active work and gives a new reviewer too little context about
earlier decisions.

The feature documents must remain useful to contributors who did not join the original discussion.

## Scope

### In

- A `feature` skill for planning, implementation progress and scope control
- A `feature-review` skill for independent plan, code and PR reviews
- A `backlog` skill for deferred, completed and rejected follow-up work
- A `workflow` plugin for the feature lifecycle skills
- A small `core` plugin for daily shared skills and a `thinking` plugin for optional deep review
- One feature contract and one Markdown task plan under `docs/features/YYYYMMDD-<slug>/`
- Shared instructions that work in Claude Code and Codex
- Clear review severities, verdicts and stopping rules
- Review-only model and effort defaults with optional project overrides
- A current `code-review.md` handoff for code and PR review rounds
- Visible active review state with the selected target, reviewer, model and effort
- A finding check that rejects unreachable, unsupported or out-of-scope claims before they enter the handoff
- A human handoff when a blocker or major finding repeats without new evidence
- An optional two-perspective stress review for risky plan and code gates
- A staged feature flow with one visible phase and human pause at each boundary
- A deterministic PR preparation order with separate approval for each repository or external action
- A final PR review handoff that can be saved without reopening the same review forever
- A human-facing feature skill README with a Mermaid flow and clear review mode triggers
- README and landing page updates for the new skills

### Out

- A workflow orchestrator or background service
- Automatic branch creation, commits, pushes, PR changes, merges or releases
- Provider-specific commands or model names inside shared `SKILL.md` instructions
- Changing the model or effort of a normal development session
- User-level review configuration
- Migration of existing projects to the new structure
- ADRs for routine implementation choices
- Append-only review logs or chat transcripts stored in feature documents
- An always-on reviewer panel, stress PR review or separate synthesis and verification agents
- A separate phase report artifact or silent multi-phase advance

## Expected behavior

### Main flow

1. The primary agent completes the `FEATURE` phase, presents the feature contract and waits
2. After approval, the primary agent completes the `PLAN` phase with an independent review and waits
3. After approval, the primary agent completes the `BUILD` phase and waits
4. The primary agent runs the `CODE REVIEW` phase and resolves accepted findings
5. The primary agent closes the artifacts, prepares the branch through separate approvals and reviews the current PR head and CI
   result
6. The human decides when to enter the `RELEASE` phase and perform each external action

A standard gate uses one general reviewer.
A stress gate adds one independent named risk perspective and keeps both sources visible without voting.
Each phase returns one short chat report and stops before the next phase by default.

### Acceptance criteria

- **AC1** – each standard feature keeps one current contract and one Markdown task plan under a compact dated folder
- **AC2** – implementation starts only after independent plan review and explicit human approval
- **AC3** – optional work moves to the backlog while a separate prerequisite records an exact resume point
- **AC4** – independent plan, code and PR reviews use evidence-backed findings with stable IDs
- **AC5** – blocker and major findings block a gate, medium findings need a disposition and minor findings do not create loops
- **AC6** – all workflow skills remain agent-neutral and require approval for external or destructive actions
- **AC7** – `humanify` improves artifacts without changing facts, scope, contracts or certainty
- **AC8** – `workflow` remains usable without `core` and applies the same prose checks when `humanify` is unavailable
- **AC9** – review model and effort defaults apply only to independent review work and may be overridden per project
- **AC10** – code and PR review rounds use one short current-state file that both agents update in turns
- **AC11** – each review shows its active state, checks findings before publishing and stops repeated blocker or major disagreement
- **AC12** – risky plan and code gates may add one independent named perspective without changing the standard review path
- **AC13** – the workflow records `FEATURE`, `PLAN`, `BUILD`, `CODE REVIEW`, `PR REVIEW` and `RELEASE` phases and advances one
  phase only after a clear human instruction
- **AC14** – PR preparation closes local artifacts and prepares the source branch before separate commit, push and PR actions
- **AC15** – the PR reviewer checks a pushed head with required CI while the handoff and allowed plan state updates stay local
- **AC16** – a final head change limited to `code-review.md` and allowed plan state updates keeps the PR verdict but still needs
  required CI before merge
- **AC17** – a first-time contributor can use the feature skill README to understand the phases, human checkpoints, artifacts,
  review modes, triggers and stop rules without reading `SKILL.md`

## Assumptions

- Feature documents are committed with the project and reviewed like code
- The primary and review roles may use any compatible agents
- The user, primary agent or an external runner starts each review gate in the first version
- Small routine changes may use only a PR and release note when no durable contract or decision is needed
- Git and PR history keep review discussion while feature documents keep current truth
- Two independent review contexts are enough for the first stress review version
- Phase reports stay in chat while `plan.md` stores the durable phase and current step

## Contracts

### Feature artifacts

```text
docs/features/
├── backlog.md
└── YYYYMMDD-<slug>/
    ├── code-review.md
    ├── feature.md
    └── plan.md
```

`feature.md` explains what should change, why it matters and what is outside the feature.

`plan.md` explains how to implement and verify that contract and shows the current progress state.

`code-review.md` holds the current code or PR review round.
It uses stable finding IDs, short replies and rechecks instead of a chat transcript.
In standard mode, the reviewer replaces the file for a new full review and rewrites it to current state on each follow-up.
A read-only standard reviewer returns the complete file and the primary agent saves it without editing the review.
In stress mode, the primary agent owns the file and copies both independent results without changing their findings.

### Review gates

The review agent returns `PASS`, `PASS WITH FOLLOW-UPS`, `CHANGES NEEDED` or `INCOMPLETE`.

A gate needs another implementation round only when it has a blocker or major finding.

Each medium finding must be fixed, added to the backlog, accepted as a known risk or rejected with evidence before handoff.

Each plan shows the latest verdict for its plan, code and PR gates.
A gate stays unchecked while its verdict is `CHANGES NEEDED` or `INCOMPLETE` and becomes checked only when its current review passes.
A later full review replaces the old verdict and may reopen the gate.

The plan gate shows `in review` while its required reviewer or reviewers are running.
While active, it records the target, mode and each required source's status, round, reviewer, model and effort.
After the review, the primary removes these temporary details and keeps the short verdict.
Code and PR reviews record `in review`, the target and the resolved review settings in `code-review.md` before they start.
A stopped or partial review becomes `INCOMPLETE` and cannot pass the gate.

The plan gate returns its findings directly because the primary agent updates the documents before human approval.
Code and PR gates keep their current findings, replies and rechecks in `code-review.md`.

Before publishing a finding, the reviewer confirms that its trigger can happen, its impact is concrete, the reviewed plan or change
caused it, worsened it or missed required behavior and the suggested fix matches the impact.
The reviewer does not turn missing evidence, unrelated existing work or a low-value preference into a finding.

After the primary disputes a blocker or major with evidence, the reviewer gets one focused recheck.
If the reviewer keeps it open without answering that evidence or adding material evidence, the agent loop stops.
The gate stays open until the human chooses the next action.

### Review modes

Standard review uses one general reviewer and remains the default.

Stress review applies only to plan and code gates.
It runs one general review and one independent review with a named risk perspective.
The reviewers do not see each other's findings before they return.

When the human asks for a stress PR review, the workflow does not silently run a standard review.
It asks the human to choose a standard PR review or a stress code review on the PR diff followed by the standard PR gate.

Use stress review when the human requests it or the feature has a material security, privacy, authorization, data migration,
data-loss, public API, compatibility, concurrency, distributed behavior or cross-cutting risk.
After a review stops on a disputed blocker or major, only the human may request a new stress review.

Before launch, the primary agent names one perspective for the risk with the greatest possible release impact.
When several risks have similar impact or the choice is unclear, the human selects the perspective.
The selected perspective stays fixed for that gate and is recorded in its active state.

Both reviewers receive the same target, feature artifacts and evidence boundary without the other reviewer's findings.
Stress code reviewers receive this baseline from the caller and do not inspect the combined `code-review.md` during their first
review or focused recheck.
General findings use IDs such as `PLAN-G1` and `CODE-G1`.
Risk findings use IDs such as `PLAN-R1` and `CODE-R1`.
Each finding keeps an immutable `Source` value.

The primary agent owns the combined result and copies both returned result sets into it without changing their findings.
Each reviewer rechecks only its own open IDs, replies and related changes.
The primary agent derives the gate verdict from the most severe open result after both required reviews finish.
The workflow does not use reviewer votes.
If either required review cannot finish, the stress gate is `INCOMPLETE`.

### Review agent configuration

Bundled defaults choose the review agent, model and effort for plan, code, PR and focused follow-up reviews.

Projects may override model and effort for the selected review host in `.codex/feature-review.json` or
`.claude/feature-review.json`.

The workflow reads these files only when it starts an independent review.
It does not change `.codex/config.toml`, `.claude/settings.json` or the active development session.

### Human guide

`plugins/workflow/skills/feature/README.md` explains the workflow for humans and contributors.
It includes a Mermaid chart for the full pipeline and a compact comparison of standard, stress and focused follow-up reviews.
It links to detailed configuration guidance instead of copying model defaults that may change.
The root README stays focused and links to this guide without copying its details.

### Feature phases

`plan.md` stores one current phase: `feature`, `plan`, `build`, `code review`, `pr review` or `release`.

The primary agent handles one phase per response by default.
At a phase boundary, it updates `plan.md`, returns a short result, checks and next-action report and stops.

The current phase must be complete before the workflow can enter the next phase.
Its required checks and gates must pass and its report must say that it is ready for approval.
An active review, failed check or blocker keeps the current phase.

At a ready phase boundary, `LGTM`, `continue` or `next` approves the result and enters only the next eligible phase.
An explicit phase name requests that phase but can enter only the next eligible phase after its prerequisites pass.
Phase approval and selection never authorize an external action.

A question or informational correction keeps the current phase.
A semantic change to `feature.md` reopens `FEATURE` and all downstream work.
A semantic plan or verification change reopens `PLAN` and affected downstream work.
A code change after review reopens `CODE REVIEW`.
A PR head or CI change reopens `PR REVIEW`, except for the allowed handoff changes defined below, which still require final CI.

Reopening sets the earliest affected phase, clears stale approvals and pending actions and resets affected gate verdicts and
checkboxes.
It also resets `Status` and `Current step` to values defined for that phase.
The changed work needs fresh review and approval.

A blocker sets the plan status to `blocked` and records its reason and exact resume point.
The workflow cannot advance until the blocker is cleared.

An external action needs its own approval.
The prior report must name one exact action under `To continue` before bare `continue` can authorize it.
That use of `continue` performs only the named action and does not also change the phase.
An explicit action request may authorize the same eligible action without this prompt.
Merge and release always need separate approvals.

PR REVIEW completes local artifact closeout before it asks for branch, commit, push or PR actions.
It verifies the intended source branch and asks the human when the branch cannot be inferred safely.
It then requests one eligible action at a time: create or switch the source branch when needed, commit local changes, push the
source branch and open or update the PR.
Branch and commit changes are local repository actions while push and PR changes are external actions.
Each action needs its own approval.

The PR reviewer checks the pushed PR head after required CI finishes.
Changes to `code-review.md` and allowed state updates in the same feature's `plan.md` stay local during review and focused follow-ups.
Allowed plan updates record current `Status`, `Phase`, `Current step` and review gate checkboxes or verdicts.
They follow verified events and existing approvals without changing scope, decisions, implementation tasks, verification or
approval requirements.
The workflow checks the actual diff and rejects mixed state and semantic changes from this exception.
After the PR verdict passes, the workflow records the gate result in the plan and may request a commit and push of the final
handoff and allowed plan state updates.
That head change does not reopen PR REVIEW, but required CI on the final head must pass before merge approval.
Any change outside the exception reopens PR REVIEW and needs a current verdict.
Later allowed state updates, including entry into `release`, may stay local until the next approved commit.
Any later push still requires final CI before merge.

### Backlog

Deferred work uses stable `BL-NNN` IDs in `docs/features/backlog.md`.

Open tasks are grouped under `High`, `Medium` and `Low` in that order.

Completed tasks move to `Done`.

Rejected tasks move to `Won't implement` and keep their `Won't do` or `Won't fix` reason.

The backlog stores the current decision and reason, not a discussion log.

## Decisions

- Keep `feature.md` and `plan.md` separate because they answer different reader questions
- Keep code and PR review handoffs in `code-review.md` so their current state is visible to the human and both agents
- Let only one agent update `code-review.md` at a time and rewrite current state instead of appending a conversation
- Map every review verdict to one valid file status and keep finding states separate
- Show the latest verdict beside each plan, code and PR gate checkbox and reopen the checkbox when a new review does not pass
- Prefix each new feature folder with its compact `YYYYMMDD` creation date so directory order shows feature chronology
- Use the verified historical delivery date when a feature is backfilled
- Keep the original dated folder name when a feature is resumed or changed
- Track plan steps as Markdown tasks and mark them complete when their work and checks are done
- Store current truth in documents and use Git and PRs for history
- Use one project backlog file for the first version to keep capture and triage cheap
- Group backlog tasks by priority and keep rejected decisions at the bottom
- Keep agent roles neutral in shared skills and configure providers outside the skills
- Keep review model and effort in a linked config file instead of `SKILL.md`
- Use high effort for full reviews and medium effort for focused follow-ups
- Resolve review values from the complete default gate, selected reviewer override and project override in that order
- Allow only project review overrides and do not use user-level review config
- Treat reviewer convergence as a severity and disposition problem, not full agreement between agents
- Keep daily shared skills in `core`, feature lifecycle skills in `workflow` and optional deep review in `thinking`
- Give each plugin a distinct icon and accent color within one shared visual style
- Keep cross-plugin helpers optional and define an equivalent local fallback
- Keep a started review attached until it returns a verdict and use a verbatim handoff for a read-only standard reviewer
- Record active review state before launch and keep stopped or partial reviews incomplete
- Check each finding against its trigger, impact, change scope and suggested fix before publishing it
- Stop a repeated blocker or major disagreement and give the decision to the human
- Keep one reviewer as the default and add only one named risk perspective for a stress review
- Use stress review for plan and code gates, not the final PR gate
- Ask the human how to continue when they request an unsupported stress PR review
- Let the primary agent combine both results without a separate synthesis or verification agent
- Give both stress reviewers the same baseline and keep their initial findings independent
- Use general and risk ID namespaces so findings and rechecks cannot collide
- Let each reviewer recheck only findings from its own perspective
- Keep stress code reviewers independent from the combined handoff
- Keep one durable phase in `plan.md` and short phase reports in chat
- Advance one phase per clear human instruction and reopen only affected downstream work
- Name an external action before a bare continuation can authorize it
- Clear stale approvals, verdicts and pending actions when a semantic change reopens work
- Reset status and the current step when work reopens and use `Reconstruction:` to identify historical backfills
- Complete PR artifact closeout and source-branch resolution before requesting commit, push or PR actions
- Keep PR review handoff edits and allowed plan state updates local until the verdict passes
- Preserve the PR verdict for the final handoff and verified plan state updates while still requiring final CI
- Check the diff before allowing plan state updates so scope, tasks, verification and approval rules still receive review
- Keep detailed workflow guidance beside the `feature` skill and only a short link in the root README
