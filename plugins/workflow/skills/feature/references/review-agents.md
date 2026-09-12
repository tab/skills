# Review agent configuration

Use this guide only when the `feature` workflow starts an independent plan, code, PR or focused follow-up review.

## Boundary

The configuration applies only to a new review agent or session.
It must not change the active development session or a host's normal project settings.

The bundled defaults are in [review-agents.json](review-agents.json).
Codex is the default reviewer, but the user may choose another configured reviewer.

## Resolve the configuration

Run the linked resolver from the `feature` skill:

```bash
python3 <skill-dir>/scripts/resolve-review-agent.py --project-root <repository-root> --gate <gate>
```

Add `--reviewer <name>` only when the user chooses a reviewer other than the bundled default.
Use the returned `reviewer`, `model` and `effort` without guessing from the gate name or active session.
These values describe the new review process, not the active development process.

Review values use this precedence:

1. Use the reviewer named by the user, or `default.reviewer` when none is named
2. Start with the matching complete gate in `default`
3. Apply the matching gate override for the selected reviewer when present
4. Apply the matching project override at the repository root
5. Return the final review-only configuration

The returned `sources` list shows the applied layers in the same order.

Use these project override paths:

- Codex – `.codex/feature-review.json`
- Claude Code – `.claude/feature-review.json`

Do not read an override from a user directory, parent directory or native host settings file.
Do not create or edit an override unless the user asks.

Use the `follow-up` gate only to recheck open finding IDs and their fix diff.
Use the original `plan`, `code` or `pr` gate for a new full review.

If the selected handoff cannot apply the resolved model and effort, report both values and let the human start the review.
Do not run the review in the active development context as a fallback.

## Project override format

A project file may override one field, one gate or every gate.
The folder selects the review host, so the file does not repeat the host name.
An override never changes the selected reviewer.

```json
{
  "version": 1,
  "gates": {
    "code": {
      "model": "gpt-5.6-sol",
      "effort": "high"
    },
    "pr": {
      "effort": "low"
    }
  }
}
```

Accept only a JSON object with `version: 1` and a `gates` object.
Gate names are `plan`, `code`, `pr` and `follow-up`.
Each gate may contain a non-empty string `model`, `effort` or both.

Treat invalid JSON, an unsupported version, an unknown key or an empty value as a configuration error.
Report the exact file and problem before starting the review.
