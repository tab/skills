---
name: humanify
description: >-
  Rewrite or review prose, Markdown and code comments so they are clear, natural, specific and right for the reader.
  Use when asked to humanize text, reduce AI-style wording, improve tone, improve readability or reflow Markdown lines and tables without changing the meaning.
---

# Humanify

Make the writing sound like it came from someone who understands the subject and the reader.
Keep the author's meaning, facts and level of formality.
Do not add fake opinions, stories, mistakes or filler to make text seem human.

## Read the context

- Identify the reader, purpose and format before rewriting
- Read nearby text, repository guidance and the established style when available
- Preserve facts, commitments, technical terms, links, examples and required structure
- Do not make an unverified claim stronger or more specific
- Check a fact against its source when one exists, such as code, config or a workflow file
- Fix a stale fact when its source proves it wrong, and say which fact changed
- Improve the wording without changing the message, policy or product behavior

## Make the writing clear and natural

- Keep statements short, direct and natural
- Split a sentence that chains clauses with "which", "while" or "so that"
- Lead with the point, action or question
- Prefer practical language over formal language
- Prefer the simple verb when it says the same thing: "checks" over "performs a check", "can" over "is able to", "to" over "in order to"
- Use concrete nouns and verbs that describe what happens
- Name the file, function, command or value instead of describing it
- Prefer concrete examples over abstract explanations when they help
- Name the exact missing detail instead of saying only that something is unclear
- Use bullets only when there are several concrete points
- Keep a list item to a fragment or one sentence, and put extra detail in a second sentence
- Add only the reason or context the reader needs to understand or act
- Remove generic framing, repetition, inflated claims, jargon and stock transitions that add no meaning
- State a rule as a statement, not as a question or a "note that" aside
- Vary sentence shape when the draft has a mechanical rhythm, but do not force informal wording or quirks
- Use contractions, fragments or questions only when they fit the reader and surrounding text
- Follow local rules for punctuation, capitalization and heading style
- Match the format: concise for UI and comments, explanatory for docs and conversational only when someone is speaking

Read [common tells](references/tells.md) when the draft needs a close AI-style wording check.
Read [voice and format](references/voice.md) when the format needs more specific guidance.

## Preserve the format

- Keep Markdown structure, links, code fences, tables, frontmatter and machine-read fields valid unless asked to change them
- Keep quotes, code, commands, paths and URLs exact
- For code comments, explain intent, constraints or behavior that is not clear from the code
- Do not make code comments more conversational than the surrounding codebase
- Prefer precise technical terms over smoother but less accurate wording
- Keep examples and commands runnable

## Lay out Markdown

- When asked only to reflow, change the layout and nothing else
- Break a line only between sentences, never inside one, unless the repository enforces a line length
- Pack sentences to about 135 characters per line, and keep a paragraph or list item of up to 150 characters on one line
- Follow the layout the document already uses, such as one sentence per line or a width of 120 or 160
- Align every table so the pipes line up in each row, including the separator row
- Leave code blocks, headings, frontmatter, blockquotes and badge lines as they are, and change a table only to align it

When asked to rewrite a Markdown file, run [the reflow script](scripts/reflow.py) once its wording is final:

```bash
python3 <skill-dir>/scripts/reflow.py --width 135 <file.md>
```

It rewrites the file in place and skips a file when the result would change more than whitespace.
Set `--width` to the document's width, or `0` to put each sentence on its own line.
Review the diff afterwards, and break the lines by hand when Python 3 is not available.
Do not run it in a review-only request.

## Check the result

- The revision says the same true thing at the same level of certainty
- Each sentence is useful, specific and easy for the reader to scan
- The tone fits the surrounding text
- Formatting, terminology and technical details remain intact
- With whitespace collapsed, the result differs from the original only in wording, or in a fact that was wrong
- Every table renders with aligned pipes
- No line ends inside a sentence
