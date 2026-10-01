# 3. Findings

Read this before you publish a finding or a verdict at any review: the checks, the finding contract and when the loop stops.

## Check a finding before publishing it

Try to disprove every candidate finding against the current evidence:

1. Confirm that the trigger can happen under the reviewed contract or implementation
2. Name a concrete impact that a user, caller or maintainer would notice
3. Confirm that the reviewed plan or change causes it, worsens it or misses required behavior
4. Confirm that the suggested fix addresses the cause and matches the impact

Do not publish the finding until each check passes.
Do not report an unrelated existing issue unless the current change makes it reachable or worse.
When required evidence is missing, return `INCOMPLETE` instead of raising the finding's severity.
Returning no findings is valid when the reviewed evidence supports the feature.

## Finding contract

Report only findings with concrete impact:

- **Blocker** – unsafe, destructive, invalid or impossible to release safely
- **Major** – required behavior is wrong or missing, a likely serious defect exists or a key contract or proof is absent
- **Medium** – a contained real issue that needs a clear disposition before handoff

Do not report minor, low-value, optional or style-only findings unless the user explicitly asks for them.
If a low-value idea is still useful, suggest one backlog item after the verdict without presenting it as a finding.

Use stable IDs within a feature:

- `PLAN-1`, `PLAN-2` for the plan gate
- `CODE-1`, `CODE-2` for the code gate
- `PR-1`, `PR-2` for a PR review comment

A risk review finding uses the IDs and the `Source` line of [the risk review](risk-review.md#keep-sources-separate).

For each finding include severity, ID, exact file and line or section, evidence, impact and suggested fix.
Do not inflate severity to keep a review loop open.

## Verdict and convergence

Return one verdict:

- `CHANGES NEEDED` – at least one blocker or major finding remains open
- `PASS WITH FOLLOW-UPS` – no blocker or major remains, but medium findings still need a disposition
- `PASS` – the evidence is complete and no blocker, major or undisposed medium remains
- `INCOMPLETE` – required evidence could not be reviewed

The primary agent fixes every finding it accepts, of any severity, inside the approved scope without another approval step.
It gives each medium a disposition itself: fix, backlog when out of scope, or dispute.
The human decides a dispute the recheck leaves open, a change to approved scope or contracts and an accepted risk.
Keep a fixed finding's status in `code-review.md` and code evidence.
Propose the change to the human when a finding changes the contract, assumptions, decisions or scope.
Use the backlog only for deferred work.

On another round, review only changed areas and open finding IDs plus any regression caused by the fixes.
Read each `Reply`, keep IDs stable and record a short `Recheck` when a finding stays open.
Move closed findings to the compact `Resolved` section.
Do not reopen an unchanged resolved finding without new evidence.

Do not repeat target discovery, reread unchanged artifacts, run a broad repository search or rerun the full check suite on a
focused follow-up.
Start from the open IDs and the fix diff, then make another read or check only when it can change an ID's disposition.

Stop the gate loop as soon as no blocker or major remains and no disputed finding waits for its recheck.
Minor or low-value disagreement never starts another round.
After the primary disputes a finding of any severity with evidence, allow one focused recheck.
If the reviewer keeps the finding open without answering that evidence or adding material evidence, stop the agent loop.
Keep the verdict and the gate open and ask the human to choose the next action.
A request to continue until the agents agree does not authorize more unchanged rounds.
