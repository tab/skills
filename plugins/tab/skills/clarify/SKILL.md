---
name: clarify
description: >
  Investigate confusion or expectation mismatches with current evidence.
  Use when the user does not understand, expected different behavior or says something seems wrong.
---

# Clarify

Explain what actually happens and determine whether the mismatch is a misunderstanding,
stale context, unclear documentation, configuration or a real issue.

Clarification is a diagnostic task.
Do not change code, configuration, documentation or external systems unless the user also asks for that change.

## Establish the mismatch

Identify:

- The exact question or confusing point
- What the user expected
- What they observed or what the artifact says
- The relevant project, revision, environment and timeframe

Infer these from the visible context when possible.
Do not ask the user for facts that can be checked from available sources.

## Check current evidence

Inspect the smallest useful source set before explaining:

- Current code, tests and configuration
- Project documentation and applicable instructions
- Tasks, comments, contracts or decision records when they define expected behavior
- Runtime evidence when the question is about deployed behavior and such evidence is available

Use applicable read-only sources for external evidence.
Keep repository behavior and deployed behavior separate.
Confirm the project and revision so similar systems or old versions are not mixed together.

If a decisive source is unavailable, name it and say what remains uncertain.
Ask one short question only when the answer cannot be verified.

## Assess the result

Choose the best supported result:

- **Misunderstanding or recall gap** – current behavior matches its supported contract
- **Context or version mismatch** – the expectation belongs to another project, revision or environment
- **Documentation issue** – implementation and documentation disagree or the explanation is unclear
- **Configuration issue** – the expected capability exists but current settings change its behavior
- **Real issue** – evidence shows a bug, design problem or missing capability
- **Unresolved** – available evidence cannot distinguish the cases

Do not assume that the user is wrong or that the system is broken.
Treat the user's expectation as a hypothesis and verify both sides.

## Explain clearly

Lead with the conclusion, then give only the evidence needed to understand it.

- State the expected and actual behavior in concrete terms
- Explain why they differ and cite exact paths, lines, links, revisions or settings when available
- Say why the difference matters and give one small example when it helps
- Use short B1 English and avoid blame, filler and a long tutorial
- Say `I could not verify ...` when evidence is missing instead of guessing

Use `Expected`, `Actual`, `Why` and `Assessment` labels only when they make the answer easier to scan.
A short direct paragraph is better for a simple case.

## Respect task boundaries

- If the user asked only for an explanation, stop after the evidence-backed assessment
- If a real issue is confirmed, state its likely scope and impact without implementing a fix automatically
- If the user also asked for a fix, continue through the applicable development workflow and reuse the evidence
- Use root-cause analysis only when the causal chain matters to the question
- Do not save a learning, memory or backlog item unless the user explicitly asks

If the user rejects the explanation, re-read the affected evidence and correct the assessment.
Do not defend the earlier conclusion as a premise.
