# Plan — Teach the skills the inbox + subagent conventions

> Status: complete (steps 1–8 done; live-harness validation run by hand by
> the owner and concluded)
> Source of truth: `codocu.md` (doc → code). This plan implements two
> conventions already written there; do not re-decide them, implement them.

## Why

`codocu.md` now tells *foreign* agents two things: drop long-term docs in
`docs/inbox/` (raw, their own tone, uncommitted until marked), and put plans
in `docs/plans/` with real per-step status. None of the eight skills know
either rule — `fold` never looks at `docs/inbox/`, `orient` never signals it,
and the seeded template wouldn't carry the convention to a new project. The
gap is total but narrow: `fold` is the real work; everything else is a signal
line, a wording pass, or a seed.

This plan does **not** touch the broader 0.2.0 "doc-first, delegate
plan/code" reframe in `docs/todo.md` — that's a roadmap question, not this
sync.

## The two conventions (restated only as acceptance criteria)

1. **Inbox intake.** `docs/inbox/` holds long-term docs other agents
   produced, not yet processed. Between fleeting and long-term. Not committed
   unless explicitly marked for deferred processing. Codocu folds them into
   evergreen docs under the doc-standard and voice, then clears them.
2. **Subagent guidelines.** Foreign agents with their own plan/spec
   structure: planning + immediate-implementation docs → `docs/plans/`, with
   actual completion status per step; long-term docs → `docs/inbox/`, marked
   for Codocu folding.

## Steps

Spec leads (CLAUDE.md: read/update the design spec before changing skill
semantics). Each step carries its own status; `fold` will verify by code, not
by these boxes.

### 1. `docs/design/flows.md` — add the inbox to the map  `[x]`

- Under **States** or a short new note: a non-empty `docs/inbox/` is
  unprocessed long-term input — a folding obligation, not a desync of its
  own.
- Under **Moves**: extend the `/codocu:fold` line — it also ingests
  `docs/inbox/` drafts, not just plans.
- Under **Moves**: extend `/codocu` (orient) — a non-empty inbox is a
  bearings signal that recommends `fold`.
- Under **Gates**: inbox contents stay uncommitted unless explicitly marked
  for deferred processing; fold is what clears them.
- Acceptance: a reader of `flows.md` alone learns inbox exists, who fills it,
  and which move drains it — without opening a skill.

### 2. `skills/fold/SKILL.md` — ingest the inbox  `[x]`

This is the substantive change.

- Add a step (after "Which plan", before/with "Bring the docs along"): check
  `docs/inbox/`. If non-empty, each file is a foreign-authored long-term
  draft to fold into the project's evergreen docs under the long-term
  doc-standard and Codocu voice — not pasted in, re-derived in plain words.
- Honor the "marked for deferred processing" marker: a draft so marked is
  left in place and reported, not folded this pass.
- After folding a draft, remove it from `docs/inbox/` (the directory persists
  via `.gitkeep`; the drafts do not).
- `fold` with no plan but a non-empty inbox is still real work — the existing
  "nothing to fold, stop" line must not short-circuit when inbox has content.
- Acceptance: running `fold` on a repo with an inbox draft and no plan folds
  the draft into the right evergreen doc, clears it, and the close-out report
  names what was folded.

### 3. `skills/codocu/SKILL.md` — orient sees the inbox  `[x]`

- "Get your bearings": add `docs/inbox/` to the quick signals — non-empty
  inbox = unprocessed long-term docs from other agents.
- "Read-only orientation" brief: count a non-empty inbox under "what the docs
  and plans claim".
- "Recommend, don't enumerate": non-empty inbox (no other divergence) →
  recommend `/codocu:fold` plainly, same shape as the one-sided-desync
  recommendation.
- Acceptance: orienting a repo whose only change is an inbox draft yields
  "Desynced / fold" — not "Synced".

### 4. `skills/apply`, `skills/propose`, `skills/doc-code` — foreign plans  `[x]`

(Done: `apply` got the foreign-plan sentence. `propose` and `doc-code`
already write to `docs/plans/` with per-step `- [ ]` steps — they conform;
editing them would duplicate the convention and add noise, so left as-is.)

Light wording only — these already read/write `docs/plans/`.

- `apply`: one sentence that a plan in `docs/plans/` may be foreign-authored;
  trust its per-step status as a claim, still verify by code (consistent with
  `fold`'s existing stance).
- `propose` / `doc-code`: confirm they state plans land in `docs/plans/` with
  per-step status; add the half-sentence only if absent. Do not restate the
  convention — point to `codocu.md`.
- Acceptance: no skill contradicts the subagent guideline; none duplicates
  its full text.

### 5. `templates/codocu.md` + `skills/codocu/references/onboarding.md` — seed it  `[x]`

- `templates/codocu.md`: add an `## Subagent guidelines` section and a
  `docs/inbox/` line under "Docs structure" so a freshly onboarded project
  carries the convention. Keep it template-terse (placeholders, not this
  repo's prose).
- `onboarding.md`: where it enumerates the structure it seeds, include
  `docs/inbox/` and the subagent section so onboarding actually writes them.
- Acceptance: a dry run of onboarding into a scratch dir produces a
  `codocu.md` containing both the inbox line and a subagent-guidelines
  section.

### 6. `.gitignore` — keep inbox drafts uncommitted by default  `[x]`

- Ignore `docs/inbox/*` except `.gitkeep` and any file explicitly marked for
  deferred processing (use a name/marker convention decided in step 2 and
  stated in `flows.md`).
- Acceptance: a stray inbox draft does not show up in `git status`; a
  deferred-marked one does.

### 7. doc-standard boundary — one line, only if it helps  `[x]`

(Done in the operational `skills/codocu/references/doc-standard.md` only —
that's the file consulted while judging a doc, so that's where the confusion
lived. `docs/design/doc-standard.md` is the why-rationale, not a literal
copy; it never implied inbox drafts must meet the standard, so editing it
would be noise. The plan's "two copies stay identical" wording was
imprecise — they're a design/operational pair by construction.)

- Check `docs/design/doc-standard.md` and its mirror
  `skills/codocu/references/doc-standard.md`. If a reader could confuse an
  inbox draft with a finished long-term doc, add one sentence: inbox drafts
  are pre-standard inputs; folding is what brings them to standard. If the
  distinction is already obvious, add nothing (reader-test discipline).
- Acceptance: the two doc-standard copies stay identical, and neither now
  reads as if inbox drafts must already meet the standard.

### 8. Self-review + validation  `[x]`

(Static validation done: gitignore behavior tested — `sample.md` ignored,
`keep.defer.md` not; no skill duplicates the convention, all defer to
`codocu.md`; reader test run, no buried/bored spots left. Live
`claude --plugin-dir` + `/reload-plugins` harness pass run by hand by the
owner and concluded.)

- Reader test: where would the intended reader (whoever runs `/codocu:apply`
  on this, and an end user reading the changed skills) get lost or bored? —
  named and fixed.
- Manual: `claude --plugin-dir <repo>`, `/reload-plugins`; create
  `docs/inbox/sample.md`, run `/codocu:fold`, confirm it folds and clears;
  run `/codocu` with only an inbox draft, confirm it reports Desynced→fold.
- Confirm no skill duplicates the convention text; all defer to `codocu.md`.

## Out of scope

The 0.2.0 doc-first reframe, fold-time test-suite gate, pre-commit hook
verification, `marketplace.json` — tracked in `docs/todo.md`, not here.
