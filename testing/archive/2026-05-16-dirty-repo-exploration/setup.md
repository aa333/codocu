# Dirty-repo exploration — test setup

Base methodology for the dirty-repo orientation suite. Each run records only
its delta from this file in its own `run<N>/setup-changes.md`; results go in
`run<N>/result.md`; the verbatim agent output in `run<N>/transcript.md`.

## Goal

Verify the bare `/codocu` catch-all correctly orients in a **dirty,
uninitialized** repository — read-only, without touching the fixture — and
that it *offers but does not perform* the deeper code-vs-docs drill until the
user accepts.

## Target repo

The fixture is a separate working copy referred to here as `<target-repo>`
(an anonymized stand-in; substitute your own path via the state-guard
`-Repo` parameter). The plugin under test is this Codocu repo, loaded via
`claude --plugin-dir <codocu-repo>`.

## Fixture

A real-world-shaped mid-refactor working tree. Repo state: **Dirty**, no
`codocu.md` (uninitialized — exercises the uninitialized path).

- **2 plans exist:**
  - testing-strategy — synced; partially done, checkmarks align with code.
  - classes system — dirty; plan in OpenSpec format (proposal, design, tasks,
    spec). Partially done, then the developer refactored the code away from it.
- **Dirty spots (the scored divergences):**
  - a single dict in `archetypes.py` was refactored by the dev into strategy
    classes (an `archetypes/` package) — diverges from the active plan **(2 pts)**
  - some renames were synced back to the plan (`classes` → `game_classes`) **(2 pts)**
  - core folders/modules changed — diverge from long-term docs **(1 pt)**
  - `status_label` → `member_status_str`, `status` → `member_status` renames in
    the `ProfileData` API object — diverge from long-term docs **(1 pt)**
- Docs are in disarray — partially homebrew, partially OpenSpec (just started,
  one feature, not per-module).
- Some changes are git-tracked, some are not.

### Verified fixture state (snapshot point-in-time)

- **no `codocu.md`** → exercises the uninitialized path.
- **72 tracked changes**, **22 untracked files** (per `state-guard.ps1 snapshot`).
- Strategy-class refactor present as untracked:
  `src/modules/game_classes/archetypes/{cleric,mage,rogue,warlock,warrior,game_class,types}.py`.
- Renames (deleted tracked + new untracked): `classes` → `game_classes`,
  `src/core/access.py` → `access_service.py`, `core/module.py` → `bot_module.py`,
  new `core/cap_provider.py`, `migrations/003_classes_module.py` →
  `003_game_classes_module.py`.
- OpenSpec changes modified: `classes-system`, `settings-debug-dangerous-actions`.
- homebrew docs modified: `docs/systems/chat-unions.md`, `docs/tech-debt.md`,
  `CLAUDE.md`.

## Desired result

Bare `/codocu` analyzes the repo and reports state + divergence, **read-only**,
and stops — offering a deeper drill but not performing it.

## Locked decision

This scenario does **not** exercise the skill's (a) read-only-now / (b)
run-`/codocu:init`-first ask path. The test prompt pre-emptively forbids
creating `codocu.md` / running `codocu:init`, so the correct behavior is to
**skip the ask** and go straight to read-only orientation. Proceeding
read-only = correct; stopping to ask (a)/(b) = wrong for this prompt. The
skill's general ask-first behavior is out of scope here and is **not** a
scored item.

## Prerequisites

- **Versioning + run + compare:** versioning = git tag `test-iter-NN` in the
  Codocu repo (git is user-driven; tags/commits are the version mechanism);
  run = `claude --plugin-dir <codocu-repo>`; compare = rubric scoring in a
  **separate** session (no golden transcript — the rubric is the reference).
- **State-preservation harness:** `testing/tools/state-guard.ps1`
  (`snapshot` / `verify` / `restore [-Execute]`, `-Repo <target-repo>`
  required). snapshot captures tracked changes via `git stash create`
  (working tree untouched) + backs up untracked files; `verify` PASS confirms
  read-only; `restore` is dry-run by default, destructive recovery gated
  behind `-Execute`. The snapshot is stored local-only in a gitignored
  `.snapshot/` next to the script — regenerate with `snapshot`.
- **Report template:** `testing/tools/report-template.md`.

## One-time setup

1. `testing/**/.snapshot/` is gitignored (it holds a regenerated copy of the
   target repo's untracked code).
2. Baseline the plugin: commit skill state + `git tag test-iter-01` in Codocu.
3. Each run folder collects its own raw outputs.

## Per-iteration runbook

1. **Snapshot** (read-only on the target):
   `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
   → expect `Snapshot OK` (72 tracked, 22 untracked).
2. **Fresh session**, Opus, cwd = target repo so `/codocu` inspects it:
   `cd <target-repo>` then
   `claude --model opus --plugin-dir <codocu-repo>`
   (fresh process picks up skill edits; no `/reload-plugins` needed).
3. **Test prompt** (paste verbatim, read-only / analysis-only):
   > `/codocu Analyze the current state of this repository - code vs plans vs`
   > `docs - and report what you find. INITIAL ANALYSIS ONLY: do not modify or`
   > `create any file (including codocu.md), do not run codocu:init, do not`
   > `create a plan. When you've reported, stop.`
   Expected (per the locked decision): the prompt **pre-emptively precludes
   creating `codocu.md`**, so the skill does **not** prompt (a)/(b) — it
   performs read-only orientation directly, reports, and stops. An agent that
   stops to ask (a)/(b) here is **wrong** for this prompt.
4. **Capture** the full assistant output to `run<N>/transcript.md`. Exit.
5. **Verify read-only:**
   `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
   - `VERIFY PASS` → valid run.
   - `VERIFY FAIL` → record defect, then
     `... state-guard.ps1 restore -Repo <target-repo> -Execute` to recover.
6. **Isolation:** between iterations, clear the target repo's Claude
   auto-memory (the `…/projects/<target-repo>/memory/` directory) so the next
   iteration doesn't read memory a prior tested agent may have written.
   (Deviations from this are recorded per-run.)

## Scoring (separate session — no self-grading)

Score from the transcript in a different session or by hand; fill
`testing/tools/report-template.md` → save as `run<N>/result.md`.

**Rubric evolution.** Runs 1–2 used a 13-point operational checklist; run 3
introduced the current **7-criterion weighted rubric (17 points)** in
`report-template.md`. Each `run<N>/result.md` records which rubric that run
was scored against, so scores are only comparable within a rubric era.

13-point checklist (runs 1–2):

| Item | Pts | Pass condition |
|---|---|---|
| State = Dirty | 1 | explicitly names Dirty |
| Dirty spots | 6 | archetypes→strategy classes (2), classes→game_classes rename (2), core modules vs docs (1), ProfileData `status*` renames (1) |
| Docs: openspec detected | 1 | identifies `openspec/changes/...` |
| Docs: homebrew detected | 1 | identifies `docs/systems`, `docs/tech-debt`, etc. |
| Docs mapped to code | 1 | ties a doc claim to a specific code divergence |
| Deep drill offered, not performed | 3 | offers full doc-vs-code diff but stops |

7-criterion weighted rubric (run 3+): see `testing/tools/report-template.md`.

## Iteration rules

- Change prompts / skills, retest. Repeat across iterations.
- Preserve the target repo's exact dirty state with `state-guard.ps1`
  (snapshot before, verify after, restore on misbehavior). Do **not**
  `git stash` or use worktrees — the uncommitted/untracked changes **are** the
  fixture; both would discard or omit them.
- Versioning: each iteration's skill changes are committed + tagged
  (`test-iter-NN`) in the Codocu repo so a score maps to an exact plugin state.

## Per-run artifacts

- `run<N>/setup-changes.md` — what differed from this base setup for run N
  (skill/prompt/design deltas, runbook deviations).
- `run<N>/transcript.md` — verbatim assistant output.
- `run<N>/result.md` — filled rubric + defects + next-iteration skill change.
- `run<N>/session.txt`, `run<N>/turn<K>.json` — raw headless-run artifacts.
- git tag `test-iter-NN` in Codocu.
