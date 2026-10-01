# Folder

Read this when you create or resume a feature folder: it names the folder and says where each document starts.

## Naming

Use `docs/features/YYYYMMDD-<slug>/`.
For new work, the date is when the feature folder is first created.
For backfilled work, the date is the verified historical delivery date.
The slug is a short lowercase hyphenated name.
For example, use `docs/features/20260831-password-reset/`.

Keep the original folder name when the feature is resumed or changed.
Do not replace its date with the resume, merge or release date.
Add [`code-review.md`](code-review.md) only when the first code review starts.

## Templates and example

Start each document from its template:

- [`feature.md`](../templates/feature.md)
- [`plan.md`](../templates/plan.md)
- [`code-review.md`](../templates/code-review.md)

[The example](../examples/feature.md) shows one small feature in all three files, with
[its plan](../examples/plan.md) and [its code review](../examples/code-review.md).
