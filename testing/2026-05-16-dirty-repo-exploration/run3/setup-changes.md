# Run 3 — setup changes (delta from `../setup.md`)

iter-03. First run of the **cost-aware Plan-gated drill redesign** and the
**new rubric**.

## Plugin state under test

Codocu @ `master` + uncommitted working-tree changes (a restructured `/codocu`
skill); **not** tagged — git is user-driven.

## Rubric change (new this run)

Runs 1–2 used a 13-point operational checklist. Run 3 introduces the
**7-criterion weighted rubric, total 17 points**, now in
`testing/tools/report-template.md`. Weighting rationale: "claimed-complete ≠
done" is the stated product priority (weight 4); the read-only/safety gates
and the cost-aware drill behaviors are the core of this redesign (weight 2–3
each); state classification is table-stakes (1); the public-API field-rename
criterion is real but secondary and lowest-frequency (weight 2). Scores are
**not** comparable across the 13-pt → 17-pt rubric boundary.

## Run design

### MAIN — two turns, single session (`--session-id` then `--resume`)

- **Turn 1** — de-leaked orientation prompt (the runbook step-3 prompt;
  pre-empts the (a)/(b) ask). Verbatim in `transcript.md`.
- **Turn 2** — accept the offered drill, **barer than run 2** (no leading
  hints about what to verify):
  > Yes — perform that deeper drill-down now. Still READ-ONLY: do not modify
  > or create any file (including codocu.md), do not run codocu:init. When
  > you've reported, stop.

### Worst-case sub-run — separate fresh session (new UUID, **not** resumed)

- **Turn 1:** same as MAIN Turn 1 (verbatim).
- **Turn 2** (barest possible accept):
  > Yes, do the drill.

Recorded as a separate observation; **NOT folded into the score**.

## Headless invocation

`--output-format json`, `--permission-mode bypassPermissions`, fresh UUID per
session. MAIN = two turns same session (`--session-id` then `--resume`);
worst-case = separate fresh session, no resume.

## Runbook deviation

The target repo's Claude auto-memory was deliberately **NOT** cleared this
iteration; MAIN runs may have been informed by prior-iteration memory of this
fixture. Noted for reproducibility — does not change scoring (divergence
findings are evidenced in-transcript regardless), but the claimed-complete
catch's reproducibility is partially confounded by retained memory.

## Read-only

Both MAIN turns were genuinely **execution-free** ("no code executed, no
whole-repo scan"). Unlike run 2 (T2 executed code; state-guard blind to
gitignored caches), run 3's `verify` PASS reflects a true no-side-effect pass;
**no caveat required**.

## Scoring

Score the combined MAIN two-turn transcript (T1+T2) against the new
7-criterion rubric in an isolated context. The worst-case sub-run is a
separate observation, not scored.

## Cost

- MAIN turn 1: $0.500 / 86.9 s
- MAIN turn 2: $0.562 / 150.5 s
- **MAIN combined ≈ $1.062 / 237.4 s** (vs run 2's ≈ $6.38)
- Worst-case turn 1: $0.438 / 93.0 s; turn 2: $0.278 / 73.9 s; combined ≈ $0.716
