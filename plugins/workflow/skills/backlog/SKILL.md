---
name: backlog
description: >
  Capture and maintain deferred project work with stable decisions in docs/features/backlog.md.
  Use when the user wants to add, triage, complete, reject or revisit an idea or an out-of-scope follow-up.
  Do not use to implement the item or replace an external issue tracker the user chose for the project.
---

# Backlog

Keep one compact project backlog at `docs/features/backlog.md`.

The backlog protects the active feature from useful but non-blocking work and preserves decisions that should not be discussed again
without new evidence.

## Inspect before changing

Read repository instructions, the existing backlog and the source feature, issue or review when one is named.

Search for an existing item with the same outcome before adding another one.
Update the existing item when the new request is a duplicate, a status change or stronger evidence for the same decision.

Do not create or edit the backlog when the user only asks to discuss an idea and has not asked to save, defer, triage or decide it.

## File contract

Create this structure when `docs/features/backlog.md` does not exist:

```markdown
# Backlog

## High

- [ ] **BL-001 – <One clear outcome>**
  - Why: <Why this matters or why it was deferred>
  - Added: <YYYYMMDD>

## Medium

- [ ] **BL-002 – <One clear outcome>**
  - Why: <Why this matters or why it was deferred>
  - Added: <YYYYMMDD>

## Low

- [ ] **BL-003 – <One clear outcome>**
  - Why: <Why this matters or why it was deferred>
  - Added: <YYYYMMDD>
```

Use the next unused `BL-NNN` ID and never reuse an ID.
Write the creation date once as `Added: YYYYMMDD` and do not update it when the item moves.
Add `Source: <link>` as another nested bullet only when a useful source exists.
Resolve a source link relative to `docs/features/backlog.md`.
For a feature source, use a target such as `20260831-example/feature.md`, not
`docs/features/20260831-example/feature.md`.

Use priority sections in this order:

- `High` – valuable next work or a material risk that should be handled soon
- `Medium` – useful work with no near-term urgency and the default when no stronger priority is supported
- `Low` – optional work, an early idea or work waiting on a condition

Priority is not severity.
A blocker required by the active feature does not belong in the backlog.

Use these states:

- An unchecked task under a priority section is `Open`
- Add `Status: Doing` only after work starts and keep it under its priority
- Move a completed item to `Done` and mark it `[x]`
- Move a rejected item to `Won't implement` and record `Status: Won't do` or `Status: Won't fix`

Keep `Done` after `Low` and keep `Won't implement` at the bottom.
Omit empty sections.
Within a priority, put `Doing` first, then prerequisites before dependent work and preserve the remaining order.

Write `Item` as one concrete outcome, not a copied chat message.
Write one short reason under it, not a discussion history.

## Decide where work belongs

- Keep required in-scope work in the active feature plan
- Put useful non-blocking out-of-scope work in the backlog and continue the active feature
- Treat a required prerequisite as a separate feature and mark the original plan blocked with an exact resume point
- Leave speculative or no-value ideas out unless the user explicitly wants to preserve them

Do not hide a feature blocker in the backlog.

## Triage and closed decisions

Only mark an item `Won't do` or `Won't fix` from the user's decision or an existing authoritative decision.
Include the reason so another agent does not reopen the same debate later.

When a closed item is raised again:

1. Show its ID, status and reason
2. Check whether the new request contains evidence or constraints that change the decision
3. Keep it closed when nothing material changed
4. Reopen it as `Open` only with the user's approval or a clearly superseding project decision

Mark an item `Doing` only when work has started and move it to `Done` only when its outcome is complete.
Do not infer completion from a merged related change unless it delivers the item.

## Boundaries

- Do not implement backlog items as part of this skill
- Do not create external issues, comments or tickets without explicit approval
- Do not delete closed items because their decisions remain useful project context
- Keep review conversations, estimates and progress logs out of the backlog

After an update, report the changed ID, status and one-line outcome.
