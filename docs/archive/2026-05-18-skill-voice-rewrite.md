# Plan: Skill voice & efficiency rewrite

**Status:** near-complete — core work committed, final polish + fold pending.

## Goal

Rewrite every skill's prose for the Codocu voice
and trim mechanical bloat, without changing skill semantics. This plan exists
because the work was tracked as a loose checklist in `docs/todo.md` with every
box unticked even though it had shipped — a live instance of the
checkbox-drift problem. Status below is verified against git, not against the
old boxes.

## Steps

Core rewrite — all committed in `50f2f51` ("Rewrite codocu skills to change
voice and improve efficiency"); line counts are that commit's diff:

- [x] `skills/codocu/SKILL.md` — rewritten (~128 lines), onboarding branch reworked
- [x] `skills/init/SKILL.md` — rewritten (~121 lines), `onboarding.md` reference merged in and removed
- [x] `skills/fold/SKILL.md` — rewritten (~34 lines)
- [x] `skills/apply/SKILL.md` — rewritten (~28 lines)
- [x] `skills/code-doc/SKILL.md` — rewritten (~13 lines)
- [x] `skills/doc-code/SKILL.md` — rewritten (~10 lines)
- [x] `skills/propose/SKILL.md` — rewritten (~9 lines)
- [x] Supporting docs realigned: `flows.md`, `principles.md`, `codocu.md`,
      `CLAUDE.md`, `templates/codocu.md`, codocu skill references
      (`conflict-resolution`, `deep-drill`, `doc-standard`,
      `reconciliation-plan`); dead `skills/sync/SKILL.md` and
      `references/onboarding.md` removed

Open:

- [x] Final polish pass — uncommitted working-tree tweaks
      (`docs/design/voice.md` +4 lines; 7 skills, 1–2 lines each). Review and
      commit as the close of this cycle.
- [x] `:fold` this plan once the polish is committed; set `codocu.md` sync
      state honestly (it currently claims "Synced" while this cycle is open).

## Notes

- **Checkbox discipline adopted.** `codocu.md` §Subagent guidelines already
  requires plans to carry real per-step status; this plan enforces it and
  supersedes the open "plans executed without ticking checkboxes" question in
  `docs/todo.md` Meta. Going forward, `:apply`/`:fold` verify deliverables
  against code + git, and steps are ticked as they land.

Reader test: the intended reader is a future me at `:fold` time. Risk of
boredom is the per-skill list reading like a changelog — kept to one line
each with the git anchor so it can be confirmed at a glance, not re-read.
