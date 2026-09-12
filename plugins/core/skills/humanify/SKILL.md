---
name: humanify
description: >-
  Rewrite or review prose, Markdown and code comments so they are clear, natural, specific and right for the reader.
  Use when asked to humanize text, reduce AI-style wording, improve tone or improve readability without changing the meaning.
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
- Improve the wording without changing the message, policy or product behavior

## Make the writing clear and natural

- Keep statements short, direct and natural
- Lead with the point, action or question
- Prefer practical language over formal language
- Use concrete nouns and verbs that describe what happens
- Prefer concrete examples over abstract explanations when they help
- Name the exact missing detail instead of saying only that something is unclear
- Use bullets only when there are several concrete points
- Add only the reason or context the reader needs to understand or act
- Remove generic framing, repetition, inflated claims, jargon and stock transitions that add no meaning
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

## Check the result

- The revision says the same true thing at the same level of certainty
- Each sentence is useful, specific and easy for the reader to scan
- The tone fits the surrounding text
- Formatting, terminology and technical details remain intact
