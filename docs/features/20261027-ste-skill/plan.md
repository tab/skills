# Simplified Technical English skill plan

Feature: [feature.md](feature.md)

Status: implemented

Phase: pr review

Current step: open the STE skill pull request from `feature/ste` to `master`

## Done when

- **AC1** – Explicit requests and active instructions select STE, while unrelated requests do not require it
- **AC2** – The entry point links local Markdown rules and examples, and every reference resolves inside the skill
- **AC3** – Representative rewrites preserve technical meaning, uncertainty, numbers, exact quotes, code, paths and required formats
- **AC4** – A partial vocabulary review or missing authoritative reference does not produce a full compliance claim
- The skill contains no HTML, external web links, full standard, copied dictionary or source metadata
- Direct, inherited, non-matching, incomplete-input and preservation scenarios have recorded results
- `make test`, `make validate` and `git diff --check` pass for the intended feature tree.
  Use a clean temporary copy when unrelated ignored files prevent validation of the working checkout

## Steps

- [x] 1. Implement the skill with a focused workflow, local rules and examples
- [x] 2. Verify activation, meaning preservation and compliance limits with representative requests
- [x] 3. Verify the complete skill package against the repository checks

## Gates

- [x] Plan review – PASS
- [x] Code review – PASS
