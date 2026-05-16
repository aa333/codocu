# Run 2 — setup changes (delta from `../setup.md`)

iter-02. Clarifying run — **not** a new suite and **no rubric change**. Same
fixture, snapshot/verify harness, per-iteration runbook, and 13-point rubric
as run 1.

## Plugin state under test

Codocu @ `99e8495` + uncommitted `M skills/codocu/SKILL.md` (unchanged from
run 1; **not** tagged — git is user-driven).

## Run design — two turns, single session

`--session-id` then `--resume` (same session across both turns).

- **Turn 1 — verbatim run-1 prompt** (the locked/hardened runbook step-3
  prompt). Expected: read-only orientation that *offers but does not perform*
  the deep drill — scored exactly as run 1 (also a reproducibility datapoint
  against run 1's 10/13).
- **Turn 2 — accept the offered drill** (resume the same session, paste
  verbatim):
  > Yes - perform that deeper drill-down now. Read the actual code diffs and
  > the plan/spec files, and verify whether work that any plan or spec marks
  > as complete is genuinely reflected in the code. Report the full
  > code-vs-spec divergence. Still READ-ONLY: do not modify or create any file
  > (including codocu.md), do not run codocu:init, do not create a plan. When
  > you've reported, stop.

## Why this run

Run 1 trusted the OpenSpec `classes-system` change at face value ("61/61
complete, just unarchived") when the developer's refactor had diverged from
it — the spec is *not* fulfilled by the code. This run does **not** hard-code
an OpenSpec flow or force per-plan validation; it tests whether, once the user
accepts the drill orientation already offered, the agent reads diffs and
discovers (a) `classes-system` claimed-complete ≠ actually-done, plus the
spots run 1 missed: (b) archetypes dict→strategy-class, (c) ProfileData
`status*` renames.

## Scoring

Unchanged 13-point rubric. Score the **combined turn1+turn2 transcript**. Turn
1 still earns "deep drill offered, not performed (3)" by restraining at
orientation (the accept path in turn 2 is *not* a violation — it is the
intended UX); the 6 dirty-spot points are now attainable via the turn-2 drill.
Added observation: did the performed drill flag the `classes-system`
61/61-but-not-actually-done divergence?

## Read-only caveat

Turn 2 **executed code** to confirm bugs (live `TypeError`, JSON-500 repro).
It modified no tracked/untracked source and `verify` PASSed, but the
state-guard fingerprint only covers git-visible state; `__pycache__` /
`.pytest_cache` are gitignored, so execution caches are invisible to `verify`.
The *fixture* (tracked + untracked source) is genuinely preserved; "read-only"
here includes *running* code with gitignored side effects the harness cannot
detect. Flagged for the deep-analysis design discussion.

## Runbook deviations

None. Auto-memory cleared between iterations per the standard runbook.

## Cost

Turn 1 $0.546 / 104.9 s; **turn 2 $5.832 / 467.2 s** (turn 2 spawned parallel
sub-audits — ~4.9M cache-read tokens, 61k output). Combined ≈ **$6.38**.
