# Test Report — Orientation (Dirty) — Run 2 (iter-02)

- **Date:** 2026-05-16
- **Plugin version / tag:** untagged — codocu @ `99e8495` + uncommitted `SKILL.md`
- **Model:** Opus (`claude-opus-4-7`)
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS — git-visible fingerprint unchanged, `permission_denials: []` both turns. Caveat: Turn 2 *executed* code; the state-guard is blind to gitignored `__pycache__`/`.pytest_cache` side effects (tracked + untracked source genuinely preserved).
- **Rubric:** 13-point operational checklist (unchanged from run 1)

> Two-turn single-session run (Turn 1 = verbatim hardened run-1 prompt;
> Turn 2 = user accepts the offered drill). Scored from the combined transcript
> in an isolated context (no self-grading). Rubric is the reference, unchanged
> from run 1.

## Prompt used

**Turn 1** (verbatim, hardened run-1 prompt):
> /codocu Analyze the current state of this repository - code vs plans vs docs - and report what you find. INITIAL ANALYSIS ONLY: do not modify or create any file (including codocu.md), do not run codocu:init, do not create a plan. When you've reported, stop.

**Turn 2** (verbatim, accept the offered drill):
> Yes - perform that deeper drill-down now. Read the actual code diffs and the plan/spec files, and verify whether work that any plan or spec marks as complete is genuinely reflected in the code. Report the full code-vs-spec divergence. Still READ-ONLY: do not modify or create any file (including codocu.md), do not run codocu:init, do not create a plan. When you've reported, stop.

## What the agent did

Turn 1: noted `codocu.md` missing, wrote nothing, classified the repo **"Dirty
— mid-refactor"**, inventoried the `classes`→`game_classes` rename and `src/core`
split with file:line stale-doc references, summarized OpenSpec + homebrew docs,
mapped a specific spec claim (single `archetypes.py`) to the shipped
`archetypes/` package, then offered — but did not perform — the deeper drill and
stopped ("nothing written"). Turn 2 (user accepted): spawned parallel
sub-audits, read diffs/specs, and reported that the OpenSpec `[x]` checkboxes
are false against the working tree — reproducing a live `TypeError` in
eligibility, a JSON-500, spec-divergent class windows, and a test suite that
does not collect. It identified the dict→strategy-class data-model abandonment
fully, but never named the ProfileData `status*` API renames.

## Score

| Metric | Max | Got | Note |
|---|---|---|---|
| Repo state = Dirty | 1 | 1 | T1: "Verdict: **Dirty — mid-refactor**" — explicit. |
| Dirty spots detected | 6 | 5 | archetypes→strategy **2/2** (T2: "no `ClassId` enum / `ClassDef` / `CLASSES` tuple — the spec's data model was abandoned for an ABC-per-class design"; T1: `archetypes.py` now an `archetypes/` package — full semantic data-model change); classes→game_classes **2/2** (T1: "Old `src/modules/classes/` deleted (9 files); new untracked `src/modules/game_classes/`"); core modules **1/1** (`module.py`→`bot_module.py`, `access.py`→`access_service.py`+`cap_provider.py`, stale refs CLAUDE.md:57 / design.md:6 / design.md:7); ProfileData `status*` **0/1** — NOT EVIDENCED. |
| Docs state — openspec | 1 | 1 | T1: "OpenSpec changes (active, not archived): `classes-system` … `settings-debug-dangerous-actions`". |
| Docs state — homebrew | 1 | 1 | T1: "`CLAUDE.md` modules table and `docs/systems/chat-unions.md`"; "`docs/tech-debt.md`". |
| Docs analyzed & mapped to code | 1 | 1 | T1: "`classes-system` tasks describe a single `archetypes.py` (2.1/3.1) while code ships an `archetypes/` package — tasks are checked off but the written granularity diverged." Specific spec claim → specific code divergence. |
| Deep drill offered, not performed | 3 | 3 | Scored on T1 restraint only: "Deeper drill-down … I can do this read-only on request"; "Stopping here as requested — nothing written." T2 performs on explicit accept = intended UX, not a violation. |
| **Total** | **13** | **12** | |

## Defects / observations

- **Claimed-complete ≠ done: CAUGHT (decisively) — the run-1 defect is
  resolved by the accepted drill.** T2 headline: "the two OpenSpec changes are
  marked essentially complete, but the untracked `game_classes` refactor … broke
  the entire test suite — so a large set of `[x]` checkboxes are false against
  the current working tree." Live-verified: "`TypeError: Cleric.eligible()
  missing 1 required positional argument`" (vs 5.2/5.3/7.3/8.2/8.3 all `[x]`);
  "`TypeError: Object of type KarmaData is not JSON serializable`"; "the entire
  classes test suite does not collect … `uv run pytest` runs **zero** tests";
  spec-divergent class-window table; bottom line "not safe to archive."
- **ProfileData `status*` rename: STILL MISSED (0/1).** No mention of
  `status_label`→`member_status_str` or `status`→`member_status` on the
  ProfileData API object vs long-term docs. T2 touches `profile/service.py`/
  `KarmaData` only. This is the sole remaining rubric miss, unchanged from
  run 1.
- **run 1 → run 2 delta: 10/13 → 12/13 (+2),** entirely on the archetypes
  line (0/2 → 2/2). All other lines stable; ProfileData miss persists.
- **Read-only nuance.** T1 wrote nothing. T2 honored no-write/no-init but
  *executed* code; `verify` PASS but is blind to gitignored caches. Fixture
  preserved for the next iteration.
- **Cost as a design signal.** T2 = **$5.83 / 467 s** via parallel sub-audits
  (~4.9M cache-read tokens); combined ≈ $6.38. Concrete evidence the deep
  doc-vs-code drill is expensive and must remain explicitly opt-in / never
  default — the offered-not-performed gate at orientation is doing real work.

## Skill change for next iteration

- **Add an explicit public-API-surface field-rename check.** The agent read
  modified source (found `KarmaData`/`PlayerData`, the JSON-500 in
  `profile/service.py`) yet never surfaced the ProfileData
  `status_label`→`member_status_str` / `status`→`member_status` rename vs
  long-term docs. Instruct: when a returned/serialized API object appears in a
  diff, enumerate its renamed/added/removed public fields and cross-check each
  against long-term docs, reporting renamed public attributes as a distinct
  dirty spot — not only chasing crash sites.
- **Require a docs↔code field-level reconciliation table in drill output.** T2
  produced a spec-vs-code window table for class ranges; extend that discipline
  to identifier/field names (a "doc says X / code says Y" table for renamed
  public modules/services/object fields) so intra-file rename divergences are
  reported alongside structural moves rather than lost among runtime-bug
  findings. (Generic — not an openspec-specific flow.)
