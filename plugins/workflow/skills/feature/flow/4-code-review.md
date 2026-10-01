# 4. Code review

Read this when you enter the `CODE REVIEW` phase: what it must finish and who works in it.

## Must finish

- Review the complete feature diff against the approved artifacts
- Use standard review or a risk review and resolve accepted findings through the review handoff
- Settle findings without the human, and stop only for a reason [the stretch](approvals.md#run-the-build-and-the-code-gate-as-one-stretch) lists
- Reopen the gate after every code change until its current verdict passes
- Set `Status: implemented` only after the code gate passes

## Who works

- Roles: the gate reviewer; `qa` after a challenge pass
- Primary agent: runs the gate, fixes accepted findings, proposes a step for each `FIX NOW`
