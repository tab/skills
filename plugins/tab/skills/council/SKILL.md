---
name: council
description: >
  Stress-test an engineering decision with five independent advisors, anonymous peer review and a final verdict.
  Use for architecture choices, design documents, technical specifications, pull requests and expensive trade-offs.
  Do not use for simple factual questions or mechanical tasks.
---

# Council

Run an engineering decision through five independent perspectives.
Let the advisors challenge the decision, review each other anonymously and then produce one clear verdict.

When the user explicitly invokes this skill, they authorize subagents for this council session.
This does not authorize external writes or other actions outside the request.

## When to use it

Use the council when:

- Several approaches could work
- A wrong decision would be expensive
- The artifact needs a strong independent review
- The user asks to pressure-test or stress-test a decision

Answer directly when the task has one clear answer or is only a mechanical change.

## The five advisors

### 1. Contrarian

Assume the decision has a serious flaw.
Look for edge cases, race conditions, partial failures, security gaps, data loss and production failure modes.

### 2. First-principles thinker

Ask what problem must actually be solved.
Challenge assumptions, abstractions and boundaries that may create unnecessary complexity.

### 3. Systems thinker

Check coupling, blast radius, scale, data growth and second-order effects.
Identify what the decision enables or blocks later.

### 4. Outsider

Read the artifact with no assumed context.
Find unclear terms, hidden assumptions, surprising interfaces and missing information.

### 5. Pragmatist

Find the simplest safe path that can be built and maintained.
Check testing, migration, rollback, operational cost and the first useful delivery step.

## Workflow

### 1. Gather the artifact once

Resolve the input before starting the advisors:

- For a pull request, read its description, changed files and diff through an available read-only source
- For a local document, read the document and the nearby files needed to understand it
- For working-tree changes, inspect the relevant diff and recent history
- For a question, use the question and the available repository context

If the input is unclear, ask one short question.

### 2. Build one evidence pack

Give every advisor the same neutral context:

- The decision or question
- The artifact
- Relevant repository guidance, code, tests and related decisions
- Known constraints and important numbers
- Missing evidence or unavailable sources
- What is at stake

Do not add an opinion to the evidence pack.
Do not make each advisor fetch the same artifact again.

### 3. Run five advisors

Use the host's available subagent or delegation feature.
Run the five advisors in parallel when supported.

Give each advisor one perspective, the shared evidence pack and these instructions:

```text
Respond only from your assigned perspective.
Be direct and specific.
Do not try to balance all views because the other advisors cover them.
Call out serious flaws or major benefits clearly.
Cite file, line or section references for artifact-specific claims.
Keep the response between 150 and 350 words.
```

If delegation is unavailable, run the five perspectives in the current conversation and say that the fallback was used.

### 4. Run anonymous peer review

Shuffle the five responses and label them `Response A` to `Response E` without revealing the advisor names.

Run five reviewers in parallel when supported.
Each reviewer receives all five responses and answers:

1. Which response is strongest and why?
2. Which response has the biggest blind spot?
3. What did all five responses miss?

Keep each review under 200 words.
If delegation is unavailable, do the same review in the current conversation.

### 5. Produce the verdict

Weigh the advisor responses and peer reviews.
The strongest reasoning may outweigh the majority view.
Say why when the verdict follows a minority position.

Return:

```markdown
## Council Verdict: [topic]

### Where the Council Agrees

[High-confidence points supported by several advisors]

### Where the Council Clashes

[Real disagreements and the reason for them]

### Blind Spots the Council Caught

[Important issues found during peer review]

### Recommendation

[One clear decision with the main reason]

### First Step

[One concrete next action]
```

Keep the verdict in the conversation unless the user asks to save it.
Do not create a report file by default.

## Rules

- Keep every advisor grounded in the same artifact and evidence
- Preserve anonymous peer review
- Do not use the council for trivial questions
- Do not hide important disagreement to make the verdict look unanimous
- State evidence limits instead of filling gaps with assumptions
