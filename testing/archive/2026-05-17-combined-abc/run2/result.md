# R2 — Writer (Spec A + C) code-doc on scratch — scored separate-session (subagent, transcript-only)

- Run type: writer | Target: disposable `<scratch-w>` | Read-only verify: n/a
- Skill state: master `86b14c7` + uncommitted A+B+C

## What the agent did

Diagnosed `docs/actual/auth.md` was pinned to private internals (`_cache`,
`_recompute`, `compute_hash`, `_issue_token`, `_revoke`, "dict keyed by user
id"), which is why an internal-only refactor left it stale. Identified the
public surface as only `login`/`logout`. Presented a proposed diff rewriting
the doc to a coarse orientation map (purpose / place / public contract /
explicit scope-boundary note) and asked approval before writing.
`auth.after.md` UNCHANGED — approval-gated single-turn headless (expected; not
penalized). Scored from the proposed rewrite in the transcript.

| Metric | Got | Note |
|---|---|---|
| Writer: anchor honored | PASS | Proposed summary = purpose + place + `login`/`logout` contract + direction; no internals in WHAT body |
| Writer: drift test passes | PASS | No `TokenStore`/`_cache`/`_recompute`/`_issue_token`/`_revoke`/"dict keyed by user id" in proposed summary; explicit "may change without notice" boundary line |
| Reader-exp: answer-first | PASS | Leads with one-line purpose, tight contract, single boundary sentence; each fact once, no padding |
| Voice non-regression | PASS | Senior-colleague explanation of *why* stale; no checklist recital, no scaffolding leak |

## Headline

Clean PASS on all four — refactor-proof, answer-first orientation map in
senior voice. Only caveat: file unchanged (expected, approval-gated); on-disk
doc remains drifted, only the proposal is evaluable.
