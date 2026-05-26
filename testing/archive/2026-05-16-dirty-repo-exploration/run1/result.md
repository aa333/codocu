# Test Report — Orientation (Dirty) — Run 1 (iter-01)

- **Date:** 2026-05-16
- **Plugin version / tag:** untagged — codocu @ `99e8495` + uncommitted `SKILL.md`
- **Model:** Opus (`claude-opus-4-7`)
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS
- **Rubric:** 13-point operational checklist (runs 1–2 era)

> Scored in an isolated subagent context from the transcript text only (no
> self-grading). Rubric is the reference; no golden transcript.

## Prompt used

> /codocu Analyze the current state of this repository - code vs plans vs docs - and report what you find. INITIAL ANALYSIS ONLY: do not modify any file, do not run codocu:init, do not create a plan. When you've reported, stop.

(Note: the runbook prompt was hardened post-run to also say "do not modify or
create any file (including codocu.md)" — see the locked decision in
`../setup.md`. The behavior scored here already conforms to that hardened
intent.)

## What the agent did

Correctly skipped the (a)/(b) ask (the prompt pre-empts it — locked decision)
and went straight to read-only orientation. It noted `codocu.md` is missing,
classified the repo as **Dirty** but coherent, and tabulated the code-side
rename refactor (~72 files: `classes`→`game_classes` plus core module renames).
It summarized the docs/specs side (CLAUDE.md table, OpenSpec `classes-system`
and `settings-debug-dangerous-actions`, homebrew `docs/systems/chat-unions.md`
and `docs/tech-debt.md`), listed plans, offered a deeper drill-down without
performing it, and stopped as instructed. It did **not** identify the
`archetypes.py` dict→strategy-class semantic change or the ProfileData `status*`
API renames.

## Score

| Metric | Max | Got | Note |
|---|---|---|---|
| Repo state = Dirty | 1 | 1 | "Classification: **Dirty** (but coherent, not contradictory)" — explicit. |
| Dirty spots detected | 6 | 3 | archetypes→strategy 0/2 (only "+ new `archetypes/`" as a new folder; dict→strategy-class semantic change NOT identified — not even partial); classes→game_classes 2/2 ("`src/modules/classes/` (9 files) → `src/modules/game_classes/`"); core modules 1/1 (`module.py`→`bot_module.py`, `access.py`→`access_service.py`, new `cap_provider.py`); ProfileData renames 0/1 (NOT EVIDENCED — no mention of `status_label`/`member_status_str`/`status`/`member_status`/ProfileData). |
| Docs state — openspec | 1 | 1 | "OpenSpec `classes-system` …", "OpenSpec `settings-debug-dangerous-actions` …". |
| Docs state — homebrew | 1 | 1 | "`docs/systems/chat-unions.md`, `docs/tech-debt.md` — modified." |
| Docs analyzed & mapped to code | 1 | 1 | "`CLAUDE.md` — module table already updated `classes` → `game_classes` (docs match the code rename)." — ties a doc claim to a code divergence. |
| Deep drill offered, not performed | 3 | 3 | "Available next steps (not performed)" / "Deeper drill-down — full doc-vs-code diff per area"; "Stopping here as requested." Offered, explicitly not performed. |
| **Total** | **13** | **10** | |

## Defects / observations

- **Missed the archetypes dict→strategy-class semantic change (−2).** The agent
  saw `archetypes/` only as a new folder and listed it as a next-step drill
  target. It never identified that a single dict in `archetypes.py` was
  refactored into strategy classes, nor diffed it against the active plan. Per
  the rubric this earns 0, not partial.
- **Missed the ProfileData `status*` API renames (−1).** No mention anywhere of
  `status_label`→`member_status_str` or `status`→`member_status`, nor of the
  ProfileData API object diverging from long-term docs. The deepest divergence,
  entirely absent.
- **Correct read-only behavior and stop discipline.** Wrote nothing, verify
  PASS, explicitly offered but did not perform the deep drill, stopped on
  request. Strong on structure, coherence framing, and surface-level
  rename/file-move inventory.
- **Pattern of the misses:** both gaps are semantic, content-level divergences
  (a refactor's *nature*, an API field rename) rather than path/file-move facts.
  The agent reasoned from `git status` file lists and the CLAUDE.md table, not
  from reading diff content of changed source files — structural moves caught,
  intra-file API/semantic changes not.

## Skill change for next iteration

- **Add a content-diff pass for changed/new source files, not just a
  path/file-status inventory.** The orientation step should, for a bounded
  sample of modified and new code files, inspect the actual diff (or read new
  files) to detect intra-file semantic changes — a data structure replaced by
  classes, or renamed public attributes/fields — and not stop at "new
  folder/file exists."
- **Make the docs-vs-code mapping bidirectional and field-level.** Beyond
  confirming the CLAUDE.md table matches a folder rename, the skill should
  cross-check long-term docs against specific API/identifier names in code
  (e.g. ProfileData fields) and call out renamed/diverged public API surface as
  a distinct "dirty spot," so deep-semantic divergences appear in the initial
  orientation rather than being deferred to the (un-performed) drill.
