# Long-term doc style (Spec A) — test setup

Delta from the base methodology in
`testing/2026-05-16-dirty-repo-exploration/setup.md`. The assessor-side run
reuses that suite's fixture, `testing/tools/state-guard.ps1` snapshot/verify
harness, verbatim read-only prompt, locked (a)/(b)-skip decision, and the
no-self-grading rule (score in a separate session) **unchanged**.

## What this suite verifies

Spec A's WHAT-summary contract, in two parts:

- **Assessor side (read-only, reuses the 2026-05-16 fixture):** when
  orientation / deep-drill judge the fixture's docs, they assess them against
  the WHAT-summary bound — flagging docs that are *over* it (re-tell code
  internals; the fixture's OpenSpec proposal/design/tasks/spec are the
  canonical over-bound example) or *under* it (no coarse orientation map;
  scattered homebrew docs), citing the bound — without regressing any retained
  functional or voice criterion.
- **Writer side (disposable scratch, Task 9):** when `code-doc` writes/updates
  an ActualDoc, its opening WHAT-summary respects the bound (four-part anchor
  only; drift test passes; no per-function/field/algorithmic detail).

## Fixture, runbook, prerequisites (assessor side)

Identical to `2026-05-16-dirty-repo-exploration/setup.md` — fixture,
snapshot/verify, the verbatim read-only test prompt (§"Per-iteration runbook"
step 3), the locked decision that the pre-emptive prompt skips the (a)/(b)
ask. Reuse it as-is; do not modify the fixture.

## Scoring

Score from the transcript in a separate session against
`report-template-whatsummary.md` in this directory. Save filled reports as
`run<N>/result.md`, raw output as `run<N>/transcript.md`, and the delta from
this setup as `run<N>/setup-changes.md`, per `testing/README.md` conventions.
