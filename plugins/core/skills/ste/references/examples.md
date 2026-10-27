# STE examples

These authored examples show specific rewrite decisions.
They do not replace a review of the full rules and dictionary for a compliance assessment.
Text inside code spans and quoted strings is protected source text.

## One instruction per sentence

Before:

> Check that `mode` is `strict`, then run `sync --dry-run`.

After:

> Make sure that `mode` is `strict`.
> Run `sync --dry-run`.

The rewrite replaces the general verb `check` and separates the actions.
The setting, order and exact command stay the same.

## Keep the condition

Before:

> Don't start the worker unless `ready` is `true`.

After:

> If `ready` is not `true`, do not start the worker.

The condition stays negative and still controls whether the worker can start.

## Preserve uncertainty

Before:

> There is a possibility that the retry creates a second payment.

After:

> The retry can create a second payment.

The rewrite retains a possibility.
It must not say that every retry creates a second payment.

## Preserve recommendation strength

Before:

> The guide suggests that you should use `safe_mode`.

After:

> The guide recommends that you use `safe_mode`.

The guide gives a recommendation, not a requirement.
Do not replace it with an instruction that the reader must use `safe_mode`.

## Preserve the exception and time reference

Before:

> After `state` becomes `Ready`, start the worker unless `paused` is `true`.

After:

> After `state` becomes `Ready`, start the worker only if `paused` is not `true`.

The state change still precedes the start, and the pause condition still prevents it.
Do not remove either condition to make the sentence shorter.

## Preserve protected text and numbers

Before:

> Don't change `{"currency":"EUR","amount":84378}` in `fixtures/payment.json`; keep the message "don't retry" exact.

After:

> Do not change `{"currency":"EUR","amount":84378}` in `fixtures/payment.json`.
> Keep the message "don't retry" exact.

The payload, amount, path and quoted message remain byte-for-byte identical.
The contraction inside the exact message stays unchanged.

## Resolve an ambiguous actor

Source:

> After the worker sends the request to the service, it stops.

If the context does not identify the actor, ask:

> Which component stops: the worker or the service?

Do not rewrite the source to say that the worker stops unless the evidence supports that meaning.

## Limit the compliance claim

Request:

> Rewrite this paragraph in STE and confirm full compliance.

If only the local guide was available, return the revised paragraph and state that the full vocabulary review remains incomplete.
Do not claim that the paragraph fully complies with STE.
For an ordinary rewrite without a requested assessment, do not add a routine compliance notice.

## Missing input and unrelated work

If the user requests a rewrite but provides no text and no usable source, ask for the text.
Do not invent a paragraph to satisfy the request.

If the user requests a calculation and no active instruction requires STE, do not add a prose review task.
If an active instruction requires STE for all prose, apply it to the explanation while preserving the calculation and exact values.
