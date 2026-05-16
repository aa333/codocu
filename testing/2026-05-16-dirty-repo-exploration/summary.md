# Dirty-repo exploration — cross-run summary

Suite goal and methodology: see [`setup.md`](setup.md). This file is the
running scoreboard and narrative across runs. Date: 2026-05-16.

## Status log

| Run | Plugin state | Score | Read-only | Headline |
|---|---|---|---|---|
| [1](run1/result.md) | `99e8495` + dirty `SKILL.md` | **10/13** | PASS | Correct read-only + stop. Lost 3 pts on semantic divergences: archetypes dict→strategy-class (0/2), ProfileData `status*` rename (0/1) — agent inventoried path/file moves but never read diff content. |
| [2](run2/result.md) | `99e8495` + dirty `SKILL.md` | **12/13** | PASS | Two-turn (T1 offered-not-performed; T2 accepted drill). **Claimed-complete ≠ done caught decisively** (reproduced a live `TypeError`, suite doesn't collect, OpenSpec `[x]` false). +2 vs run 1 (archetypes 0/2→2/2). T2 cost ≈ $5.83 — strong "deep drill must be opt-in" signal. Sole miss: ProfileData `status*` (0/1). |
| [3](run3/result.md) | `master` + dirty working tree (NEW 7-criterion rubric, weighted) | **15/17** | PASS | MAIN two-turn (de-leaked T1; bare-accept T2). Claimed-complete ≠ done caught **with no code execution** at **≈ $1.06 combined vs run 2's ≈ $6.38** — the cost-aware Plan-gated drill redesign worked. Cost disclosed + tier classified + unsaved triaged plan, archived OpenSpec excluded. Sole miss: persistent ProfileData `status*` rename (0/2). Worst-case "Yes, do the drill." withheld verdicts behind a further go-ahead (recorded separately, not scored). |

## The arc

- **Run 1** established the baseline: orientation, state classification, and
  stop-discipline are solid; the gaps are *semantic* divergences (a refactor's
  nature, an API field rename) that need diff-content reading, not just
  `git status` file lists.
- **Run 2** added the accepted-drill turn and resolved the priority gap:
  claimed-complete ≠ done is caught decisively. But the drill was expensive
  (parallel sub-audits, code execution, ≈ $5.83 turn 2) — concrete evidence
  the deep drill must be explicitly opt-in and never default.
- **Run 3** redesigned the drill to be cost-aware (disclose cost, classify a
  complexity tier, run only the always-bound changed-surface reconciliation
  from diffs + bounded reads, defer the heavy per-task audit into an unsaved
  triaged plan). It preserved the priority catch at **≈ 1/6th the combined
  cost** and with **no code execution** — the strongest result of the suite.

## Persistent open finding

The **`ProfileData` public-API field rename** (`status_label` →
`member_status_str`, `status` → `member_status` vs long-term docs) was missed
in **run 1, run 2, and run 3** — three consecutive iterations, three skill
changes, still 0. The single longest-standing rubric gap. Each iteration's
remediation ("add a field-rename check") did not land in observed behavior.
Run 3's next-iteration change makes it a **non-skippable line item of the
always-bound changed-surface reconciliation** (mandatory "doc says X / code
says Y" field-rename row even with zero crashes), tying section completion to
"every modified public-API object's field set was name-diffed vs docs". See
each run's `result.md` for evidence and `setup-changes.md` for the skill
change carried into the next run.

## Cost trajectory (Plan-gated tier, this fixture)

| Run | Turn 2 | Combined | How |
|---|---|---|---|
| 2 | ≈ $5.83 | ≈ $6.38 | parallel sub-audits + code execution |
| 3 (MAIN) | ≈ $0.56 | ≈ $1.06 | diffs + bounded reads, no sub-agents, no execution |

The cost-aware redesign cut the priority-finding cost by roughly an order of
magnitude on turn 2 while keeping the catch. This is the suite's load-bearing
design signal: the offered-not-performed gate plus tiered, deferred audit is
doing real work.

## Worst-case behavioral cliff (run 3, recorded — not scored)

Under the barest possible accept ("Yes, do the drill."), run 3 disclosed cost
+ presented the triaged plan but **withheld the claimed-vs-actual verdicts**,
gating them behind a further explicit go-ahead. The slightly richer MAIN
accept did surface them. Assessed as acceptable (the priority criterion is
satisfied on the MAIN path) but a real UX-tuning question — how much of an
accept is enough to proceed. Tracked in `TODO.md`.
