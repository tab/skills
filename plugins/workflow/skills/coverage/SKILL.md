---
name: coverage
description: >
  Raise test coverage to tiers by testability class and widen end-to-end scenarios under hermetic rules.
  Use after the last build step of a feature or when asked to raise coverage.
  Do not use to change production code or to chase a line that only a seam would reach.
---

# Coverage

Raise the coverage of each package to the floor of its tier.
Add end-to-end scenarios where the built artifact makes them cheap to drive.
Only tests change. Production code stays as it is.

## Classify

Put each package in one tier by how testable its code is:

| Tier   | Code                                                         | Floor per package |
|--------|--------------------------------------------------------------|-------------------|
| hard   | terminal, UI and other code that needs a device or a display | 90%               |
| medium | code where one focused test per branch is hard to write      | 95%               |
| easy   | code whose dependencies are mocked                           | 100%              |

- The floor applies per package, on the platform CI runs
- When a package mixes classes, the class of most of its code decides. On a tie, the lower floor wins
- The primary agent may name the tier of a package in the brief. The brief wins

## Measure

1. Use the coverage command the brief names. Otherwise find it in the project's instructions, build file or CI
2. Measure each package on the current tree and record the number as before
3. Name the uncovered blocks of each package at `file:line`

## Raise

Add tests block by block until each package reaches its floor.
Keep every command package-scoped.
Run the end-to-end suite or a tree-wide command only when the brief assigns it, or once at the end of a run without a brief.

Keep every test hermetic:

- A test creates nothing outside its own temporary directory, beyond what the code under test creates by design
- A test does not depend on the host: its user, home directory, network, installed tools or running processes

Rules:

- Never change production code to reach a line
- Never skip a test for a known bug. Leave the test out and report the bug for the backlog
- A platform-conditional test uses the project's existing skip pattern and says why
- Report a line left uncovered with its reason

Typical reasons for an uncovered line:

- Code that needs a device or a display
- An operating system error path that only a seam could reach
- A branch that only resource exhaustion reaches
- A branch that runs on another platform only
- A defensive branch that cannot be reached

## End-to-end

- Add a scenario when it is easy or not so hard to drive from the built artifact
- Skip a hard scenario with its reason, such as a terminal UI or a network dependency
- Keep the suite's own rules for ports and parallelism
- Wait on the output of the artifact, never on a sleep

## Report

Measure each package again with the same command. The new number fills the After column.

Return this report and omit empty sections:

```markdown
## QA coverage

Brief wrong: <what is wrong and the evidence>

| Package   | Tier   | Floor | Before | After |
|-----------|--------|-------|--------|-------|
| <package> | <tier> | <n>%  | <n>%   | <n>%  |

Uncovered:

- `<file:line>` – <reason>

Bugs found:

- <trigger – impact – the test left out>

End-to-end:

- Added: <scenario>
- Skipped: <scenario – reason>

Checks:

- `<command>` – <last lines>

Notes:

- <remark that does not block>

Files touched:

- <path>
```
