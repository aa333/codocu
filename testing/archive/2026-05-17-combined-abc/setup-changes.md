# Combined Spec A + B + C run — setup-changes (delta from base methodology)

Base: `testing/2026-05-16-dirty-repo-exploration/setup.md` +
`testing/2026-05-17-longterm-doc-style/setup.md` (Spec A) +
`testing/2026-05-17-onboarding-model/setup.md` (Spec B). Spec C adds the
Reader-experience dimension already merged into
`testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md`.

**LOCAL / UNCOMMITTED.** The target is a real, non-anonymized repo. Per the
`testing/README.md` anonymization convention, none of this suite's artifacts
(transcripts, results, this file) may be committed as-is. Referred to as
`<target-repo>` in-body; concrete local path: `../bots/neph` (do not commit).

## Plugin state under test

Codocu @ `master` (HEAD `86b14c7`) **+ uncommitted working-tree edits for
Spec A, Spec B, and Spec C** (the combined unit). Post-change run only — no
separate pre-edit baseline this pass (the test-first baseline against
`86b14c7` remains the owner's deferred decision per `docs/todo.md`). Precedent:
`2026-05-16-dirty-repo-exploration/run3` likewise tested "master + uncommitted
working-tree changes".

## Deltas from base methodology

1. **Target repo non-anonymized + initialized.** `<target-repo>` has a
   `codocu.md` (Codocu-initialized) and OpenSpec + homebrew docs. The
   2026-05-16 fixture was anonymized and **uninitialized**. Consequence:
   orientation treats `codocu.md` as authoritative; the (a)/(b) ask path
   differs from the uninitialized fixture. Recorded, not scored against the
   uninitialized assumption.
2. **Spec B "incompatible/dirty, no-interview" sub-check = n/a.** That check
   presumes an *uninitialized* incompatible repo routing to `/codocu:propose`.
   `<target-repo>` is initialized, so the sub-check is not faithfully
   exercisable here; the scoring subagent marks it n/a with this reason.
3. **Onboarding scenarios run single-turn.** Onboarding is inherently
   interactive (asks the 3 convention-core questions and waits). Headless
   `claude -p` is single-turn, so R3/R4 prompts instruct: "take the default
   for every question, show the complete proposed `codocu.md`, do **not**
   write any file." This preserves the read-only contract and still exercises
   the scored behaviors (exactly-3 questions, skeleton + `TBD` seed, no
   repo-conditional noise, never-clobber, voice).
4. **Headless execution.** `claude -p --model opus --plugin-dir <codocu-repo>
   --dangerously-skip-permissions`, cwd = the run's target. Read-only safety
   on `<target-repo>` is enforced by `state-guard.ps1` snapshot (before) →
   verify (after) → restore -Execute (on FAIL), exactly as prior runs. Writer
   (R2) and onboarding (R3/R4) targets are disposable scratch dirs — no
   state-guard, deleted after capture.

## Runs in this combined pass

| Run | Scenario | Target | Read-only gate | Scored against |
|---|---|---|---|---|
| R1 | Assessor (Spec A + C) | `<target-repo>` (dirty, initialized) | state-guard snapshot/verify | `tools/report-template.md` + `report-template-whatsummary.md` (assessor + Reader-experience-assessor) |
| R2 | Writer (Spec A + C) | disposable `<scratch-w>` | n/a (disposable) | `report-template-whatsummary.md` (writer + Reader-experience-writer) |
| R3 | Onboarding bare (Spec B) | disposable `<scratch-bare>` | n/a (disposable) | `report-template-onboarding.md` + voice |
| R4 | Onboarding brownfield (Spec B) | disposable `<scratch-bf>` | n/a (disposable) | `report-template-onboarding.md` + voice |

## Scoring

Separate session, transcript-only fresh subagents (no design rationale in
their prompt) — the sanctioned no-self-grading mechanism. Results in
`run<N>/result.md`; combined scoreboard in `summary.md`. All local/uncommitted.
