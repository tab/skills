# 3. Build

Read this when you enter the `BUILD` phase: what it must finish and who works in it.

## Must finish

- Set `Status: in progress` and implement only the approved scope
- Run [the step loop](../team/steps.md), or implement directly
- Commit accepted work as [the commit rules](../team/steps.md#commits) say
- Keep the plan state accurate. Change no step and no line of `feature.md` without the human's approval
- Run available automated checks and record any required manual check
- Stop for a contract change, blocker or separate prerequisite
- After the last passes and the `Done when` checks, start the code gate in the same run, as [the stretch](approvals.md#run-the-build-and-the-code-gate-as-one-stretch) says

## Who works

- Roles: `developer`, `code-reviewer`, `qa`, `technical-writer`
- Primary agent: runs the step loop, commits each accepted step as a checkpoint
