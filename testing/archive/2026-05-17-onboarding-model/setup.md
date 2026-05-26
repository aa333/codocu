# Onboarding model (Spec B) — test setup

Delta from `testing/2026-05-16-dirty-repo-exploration/setup.md`. Same
`testing/tools/state-guard.ps1` harness, same no-self-grading rule (score in a
separate session). Validated **together with Spec A** in one combined run
(see `testing/2026-05-17-longterm-doc-style/setup.md`).

## What this suite verifies

- **Bare repo (writer-side, disposable `<scratch>`):** onboarding asks only
  the three convention-core questions, then proposes a complete opinionated
  `codocu.md` (sync marker seeded `TBD`); one confirmation; no
  repo-conditional noise.
- **Brownfield-compatible (`<scratch>` with sample docs):** convention core +
  existing-docs stance asked; the one-line stance note recorded; defaults
  pre-filled from the detected layout.
- **Incompatible/dirty (reuse the read-only dirty fixture):** **no
  interview** — routes to `/codocu:propose`; the state-guard fingerprint is
  unchanged (no onboarding write without an explicit go-ahead — the locked
  read-only constraint).
- **Voice non-regression:** onboarding prose reads in-voice (no scaffolding
  leak, no recited checklist).

## Scoring

Separate session, against `report-template-onboarding.md`. Save as
`run<N>/result.md` with `run<N>/transcript.md` + `run<N>/setup-changes.md`,
per `testing/README.md`.
