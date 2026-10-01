# Style

Read this before writing or rewriting a feature document: it holds the shared writing rules and the quality check.

These documents are for humans and agents.
Write them for a contributor who knows the project but did not join the original discussion.

## Shared rules

- Keep current truth, not a history of the conversation
- Use short concrete language and define a term before relying on it
- Keep one behavior in each acceptance criterion
- State important assumptions instead of hiding them inside implementation steps
- Describe contracts precisely enough to implement and test
- Keep explicit out-of-scope items that prevent likely scope drift
- Remove unused sections instead of filling them with `None` or generic text
- Refactor unclear text in place instead of appending corrections
- Put deferred ideas in the backlog, current code review state in [`code-review.md`](code-review.md)
  and older history in Git or the PR
- Prefer links over copied requirements, decisions or evidence

## Quality check

Before a plan review, use the `humanify` skill on both documents when it is available.
Otherwise make the same focused prose pass directly and state that the fallback was used.
Do not change facts, scope, contracts or certainty.
Run the same pass on text changed while resolving review findings.
Return to plan review when that cleanup changes meaning.

Before the push, run the focused prose pass after the implementation closeout so the PR shows the final wording.
A change to `feature.md` still needs the human's approval.

Then read the documents once in this order:

1. Goal and why
2. Scope and assumptions
3. How it works, acceptance criteria and contracts
4. Decisions
5. Done when and steps

The reader should not need chat history to explain the goal, implement the main flow or know what is outside the feature.
If the documents repeat the same rule, keep the clearest source and link to it from the other document.
