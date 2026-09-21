# Voice and format

The right voice fits the reader and the surrounding text.
Use these defaults only when local guidance or existing copy does not set a stronger style.

## Product and UI copy

- Name the action, result or constraint instead of the feature category
- Use words the reader sees in the interface when that makes an instruction easier to follow
- Keep it brief
- Use a fragment when the interface gives it enough context
- Do not promise an outcome the product cannot guarantee

## Documentation and Markdown

- Put the answer or outcome before background information
- Order a document from the top down, so the reader meets the entry point first and each section builds on the one before it
- Keep one main idea per sentence
- Explain an unfamiliar term when the reader needs it to act
- Drop what is irrelevant, obvious by default or only nice to know, and keep the rule, the fact, the number and the name
- Use headings and lists only when they make a real structure easier to scan
- Use a table for facts that share the same columns and prose for rules
- Keep commands, code, paths and names exact
- Explain important preconditions and effects of a command

### Length

Aim for the shortest text that still answers the reader's question, so 80 lines that do the job need no padding.
Treat these sizes as upper bounds and judge them by what the document holds, since a diagram or code example can take about 50 lines on its own:

| Content                                                  | Upper bound              |
|----------------------------------------------------------|--------------------------|
| Prose only                                               | 150–200 lines            |
| Prose with diagrams or code examples                     | 400–500 lines            |
| Several domains, each with its own diagrams and examples | 150–200 lines per domain |

The counts assume packed lines, so a document with one sentence per line runs longer.
Suggest a split when a document grows well past these sizes, and leave the decision to the author.

### Repository docs

- A package README answers four questions: why it exists and where its boundary is, how it works, how a consumer uses it, what to keep true when changing it
- Add a diagram only where the flow branches or crosses a boundary, never for a straight line
- Leave file tables, method signatures and test lists out of an internal package README, since the code is the reference for those
- A top-level architecture doc is the map: the main parts, how they connect, the entry point and one section per feature or area
- A feature section names the packages that implement it, the interfaces it exposes and where it is wired, and leaves the details to the package READMEs

## Code comments

- Explain why the code exists, which constraint it protects or which behavior is not obvious
- Match the repository's comment format and level of detail
- Use plain direct wording
- Do not repeat the implementation

## Messages and reports

- Start with the answer, decision, finding or requested action
- Be direct about uncertainty and verification
- Do not make an unverified result sound certain
- Keep courtesy natural and proportionate
- Remove generic praise, scripted openings and summaries that repeat the message
