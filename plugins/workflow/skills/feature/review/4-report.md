# 4. Report

Read this before you return a review result: where the result of each review goes.

## Plan gate

For a plan gate, return the findings and verdict directly.
A direct review does not edit `plan.md`; say that the primary agent or human must record the returned verdict under the matching gate.
[The plan rules](../writing/plan.md#gates) show the gate line.

Lead with findings ordered by severity.
If there are no findings, say `No blocking findings`.

For a risk review perspective, put `Source: <assigned perspective>` before the findings.

Then return:

```markdown
Verdict: <PASS | PASS WITH FOLLOW-UPS | CHANGES NEEDED | INCOMPLETE>

Evidence checked:

- <Artifact, diff and check result>

Disposition needed:

- <Medium finding ID or none>
```

Keep the plan response short enough for the primary agent and human to act on without another summary.

## Code gate

At the start of a standard code gate, initialize the active review state from [the code review rules](../writing/code-review.md)
when write access is limited to that file.
For a read-only reviewer, the primary agent or external runner owns this start state.

For a standard code gate, create or replace `code-review.md` using the code review rules when the host can limit write access to
that file.
On a focused follow-up, rewrite the whole file with its current open and resolved state.
Do not append a review transcript.

When a standard review runs read-only, return the complete file content directly so the primary agent or external runner can save
it verbatim.
Once the unchanged content is saved, the recorded verdict applies and the review does not need to run again.
A read-only handoff is `INCOMPLETE` when its content cannot be saved unchanged.

After a standard code review, return one short message with the path and verdict.

## Risk review

For a plan or code risk review, return only the assigned perspective result.
The primary agent owns the combined result and final verdict.
Do not write or replace the combined `code-review.md` file.

## PR review

A PR review saves nothing. Its comments on the PR are its result.
A request to review the PR approves its comments. It approves no other write.

- Post each finding as a PR comment at its file and line, with a `PR-1`, `PR-2` ID
- Post the verdict as one PR comment
- Never write a file, commit or push
