# Challenge pass

Read this when the human asks for a challenge pass: after the code gate passes, a second model tries to break the change.

Run this pass only after the code gate passed and only when the human asks.
It never replaces the gate and never changes the gate's verdict.
It never runs on the plan gate or the PR review.

Target and reviewer:

- The target is the feature's merge-base range at the head the gate passed: `<merge base>..<passed head>`
- The reviewer is independent of the author and of the gate reviewer's context
- It may be a reviewer of another host through the resolved review configuration, or any reviewer the human names
- The reviewer is read-only and returns its result to the primary agent

The prompt asks for the strongest reasons this change should not ship.
It names:

- The high-value areas of the change
- The maintainer's decisions, quoted from `Decisions` and `Out` in `feature.md`
- The disposition of every earlier finding in `code-review.md`, with the instruction not to report those again

The reviewer returns structured findings and a verdict:

```json
{
  "verdict": "needs-attention",
  "findings": [
    {
      "severity": "high",
      "title": "<short title>",
      "location": { "file": "<path>", "lines": "<start>-<end>" },
      "body": "<trigger, impact and evidence>",
      "confidence": 0.8,
      "recommendation": "<smallest fix>"
    }
  ]
}
```

- `verdict` is `approve` or `needs-attention`
- `severity` is `critical`, `high`, `medium` or `low`
- `confidence` runs from 0 to 1
- These findings take no gate ID and never enter the gate's `Findings`

Triage each finding:

- Brief `qa` with its triage job
- Where the host cannot delegate, the primary agent triages it with the same four answers
- The four answers are the trigger, the impact, the state at the merge base and the smallest fix
- "Present at the merge base" is proven from the base revision, never asserted

Act on each disposition:

- For `FIX NOW`, the primary agent proposes a new plan step and the human approves it.
  Its code change reopens the code gate, as the `feature` skill says
- `BACKLOG` becomes a backlog item with `Why`, `Boundary` and `Source` through the `backlog` skill
- `DROP` is recorded with its evidence

The primary agent records every disposition under `Follow-up passes` in `code-review.md`, as
[the code review rules](../writing/code-review.md#follow-up-passes) show.
Stop after one pass unless the human asks for another.
A second pass lists every earlier disposition in its prompt, so no finding returns without new evidence.
