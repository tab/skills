# Backlog

## High

- [ ] **BL-001 – Add a portable `code-review` skill to a new `review` plugin**
  - Why: Replace the narrow local `gh-review` flow with diff and PR review plus optional approval-gated publishing
  - Added: 20260901

## Medium

- [ ] **BL-002 – Add a short agent-neutral `gap` skill to the `review` plugin**
  - Why: Remove existing paths, collectors and review-pipeline coupling before reuse
  - Added: 20260901

- [ ] **BL-003 – Add a short agent-neutral `tldr` skill to the `review` plugin**
  - Why: Remove GAP and current pipeline coupling while keeping the output useful for first-time readers
  - Added: 20260901

## Low

- [ ] **BL-004 – Add a compact portable `root-cause-analysis` skill to the `thinking` plugin**
  - Why: Keep the evidence gate for important decisions without the current collector assumptions
  - Added: 20260901

- [ ] **BL-005 – Add portable `adr-review` and `spec-review` skills to the `review` plugin**
  - Why: Build them after BL-001 – BL-004 so they can reuse small shared workflows instead of copying the local stack
  - Added: 20260901
