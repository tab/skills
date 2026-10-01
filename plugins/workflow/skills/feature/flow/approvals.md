# Approvals

Read this at each phase boundary: it keeps feature work visible and lets the human check each result before the next phase starts.

## Work one phase at a time

Complete one phase per response by default.
At the phase boundary, update `plan.md` while no PR is open, return one short report and stop.

Use this report and omit empty sections:

```markdown
## <Phase>

Status: <ready, blocked or complete>

Flow: <completed, current and remaining phases>

Result:

- <What is now true>

Checks:

- <Check and result>

Needs you:

- <Decision or manual check>

To continue:

- <One exact next phase or action>
```

Keep detailed evidence in the artifacts, code or review handoff.
Do not store phase reports as a new file or append them to `plan.md`.

Optional progress updates may announce phase entry, a material result or a blocker.
Do not report every command.

## Run the build and the code gate as one stretch

Plan approval covers the build and the code gate as one stretch, and the one-phase rule above applies at every other boundary.
After the last passes of the build and the `Done when` checks, set `Phase: code review` and start the code gate in the same run.
Return no `BUILD` report and ask for no build approval.
The next phase report comes when the code gate passes or when the stretch stops.

The step loop keeps its own [stopping rules](../team/rules.md#stopping-rules).
In the code gate, the primary agent settles findings as [the findings rules](../review/3-findings.md#verdict-and-convergence) say.
It stops and asks the human only for:

- A dispute that one rebuttal and one recheck leave open
- A contract change, which is a change to `feature.md` or the approved scope
- A blocker that sets `Status: blocked`, or a separate prerequisite
- An `INCOMPLETE` review
- An accepted risk
- A code gate that still does not pass after round 3.
  A new full review of the gate restarts the count at round 1 only after a reopen of `feature` or `plan`, or when the human asks for it

A code change after the gate passes reopens it, and the primary agent reruns it under these rules without asking.

## Advance safely

Enter the next phase only when the current phase is complete, its required checks and gates pass and its report says it is ready.
The build enters the code gate without a report, as [the stretch](#run-the-build-and-the-code-gate-as-one-stretch) says.
An active or incomplete review, failed check or blocker keeps the current phase.

At a ready phase boundary:

- `LGTM`, `continue` or `next` approves the result and enters only the next eligible phase
- An explicit phase name requests that phase but can enter only the next eligible phase after its prerequisites pass
- A question or informational correction keeps the current phase
- A named repository or external action authorizes only that eligible action

Phase approval and selection do not authorize a gated repository or external action.
Two approvals are the exception, and each covers only local actions:

- Plan approval covers the [checkpoint commits](../team/steps.md#commits) of the build and of the code gate fixes
- Entering `PR REVIEW` covers the close-out checkpoint and [the history rewrite](5-pr-review.md#rewrite-the-history)

Every branch action other than the rewrite's backup branch, and every push and PR action, still needs its own approval.
Do not skip an unfinished phase because the human named a later phase.

When the report names one exact gated action under `To continue`, bare `continue` authorizes only that action.
It does not also change the phase.
This exact action prompt takes precedence over the phase meaning of `continue`.

Ask for separate approval before each later gated action.
For example, switching a branch, making a commit neither exception covers, pushing, opening a PR, merging and publishing
a release are separate actions.
