# Core Review

Read `AGENTS.md` before reviewing a change.
Review the full affected skill and its supporting files, not only the changed lines.
Use [the code review prompt](CODE_REVIEW_PROMT.md) to run this review with an agent.

## Scope

- Confirm the change matches the request
- Separate blockers from optional follow-up work
- Ignore unrelated existing issues unless the change makes them worse
- Check staged, unstaged and untracked files

## Skill quality

- The folder name matches the frontmatter `name`
- The description explains the goal and activation conditions
- Similar but unsupported requests have a clear boundary when needed
- Instructions define the expected input, workflow, output and stopping conditions
- The skill does not invent missing facts or permissions
- Supporting files are linked and loaded only when needed
- Scripts have a clear benefit and were tested
- Examples clarify real behavior and do not encode local-only assumptions

## Claude Code and Codex

- One shared `SKILL.md` works on both hosts
- Shared instructions do not depend on one host's tool names or configuration paths
- Host-specific metadata stays in the matching metadata file
- Missing capabilities have a clear fallback or an honest stopping condition
- Invocation examples match the installed plugin layout

## Package consistency

- Marketplace name remains `skills`
- Plugin name remains `tab`
- Both plugin manifests use the same version and package metadata
- The version bump matches the change type
- README and manifest descriptions make the same promise
- Marketplace entries point to `./plugins/tab`
- New skills appear in the README in alphabetical order
- Only marketplace installation is documented
- Third-party workflow actions use full commit SHAs

## Safety

- No secrets, credentials, internal URLs or user-specific paths are present
- No unrelated brand, company or environment details are present
- Read-only skills do not modify files or external systems
- Destructive or externally visible actions require clear user approval
- Commands do not hide side effects or depend on undocumented setup

## Validation

- `make test` passes
- `make validate` passes
- `git diff --check` passes
- Meaningful behavior changes have representative activation and output checks
- Documentation links, commands and paths are valid

## Findings

Use these severities:

- **Blocker** – unsafe, invalid or incompatible change that must not be released
- **Major** – behavior, activation or maintenance defect that should be fixed before release
- **Minor** – small clear issue that is safe to fix now

For each finding, include the severity, exact file and line, impact and requested change.
Do not report a style preference unless it breaks repository rules or makes the behavior unclear.
If there are no findings, say `No blocking findings` and list the checks that passed.
