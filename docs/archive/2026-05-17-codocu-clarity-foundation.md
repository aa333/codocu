# Codocu Clarity Foundation — Plan

**Goal:** Make clarity the project's enforced foundation, then bring the
skill surface and the project's own specs into compliance — zero behavioral
change.

**Spec:** `docs/superpowers/specs/2026-05-17-codocu-clarity-foundation-design.md`

**Commit policy:** per `CLAUDE.md` — no intermediate commits; one commit at
the end, only when the owner asks.

## Movement I — Constitution

- [x] I.1 `CLAUDE.md` §First principle (#1, above conventions): principle +
  reconstruct-don't-launder corollary + the enforced reader-test gate.
- [x] I.2 Park `docs/tuning.md` →
  `docs/superpowers/archive/2026-05-17-tuning-registry-deferred.md`
  (deferral header + original verbatim); remove `docs/tuning.md`.
- [x] I.3 `docs/todo.md` — V2/Future entry: behavioral tuning mechanism
  needs a real design.
- [x] I.4 Persist this spec + plan.
- [x] I.5 Owner reviews the persisted spec/plan + `CLAUDE.md` principle
  before Movement II.

## Movement II — Consolidation (after I.5 approval)

- [x] II.1 Create `skills/codocu/references/doc-standard.md` — orientation-map
  shape + WHY heuristic, defined once, plain words, no invented jargon.
- [x] II.2 Collapse the shared house-rule line to two plain sentences; apply
  verbatim across `codocu`, `fold`, `propose`, `code-doc`, `doc-code`,
  `apply`.
- [x] II.3 Strip the inline reader-economy restatements (`code-doc` ×2,
  `fold`, `doc-code`, `propose`, `deep-drill`, `codocu` brief) — keep only
  flow-local specifics.
- [x] II.4 Point the doc-shape sites at `doc-standard.md` (`code-doc`
  small+brownfield, `fold` "Bring the docs along", `deep-drill` §4 anchor 1,
  `codocu` orientation-brief bullet) + the on-demand load step.
- [x] II.5 De-mechanize `conflict-resolution.md`; preserve "if `codocu.md`
  absent: don't create, stay read-only, note `/codocu:init`".
- [x] II.6 Manual validation per spec §Validation 1–5.
- [x] II.7 Owner reviews before Movement III.

## Movement III — Re-foundation (after II.7 approval)

- [x] III.1 `docs/design/principles.md` — runtime-facing; what Codocu
  believes (rebuilt from understanding, not laundered).
- [x] III.2 `docs/design/voice.md` — senior-partner persona, anti-leak, the
  reader/Feynman standard.
- [x] III.3 `docs/design/flows.md` — states, moves, gates; onboarding folds
  in.
- [x] III.4 `docs/design/doc-standard.md` — evergreen; the consolidation
  reference (II.1) derives from / points to this.
- [x] III.5 Archive the six dated specs/plans to
  `docs/superpowers/archive/`; update `CLAUDE.md`'s "Design spec" pointer to
  `docs/design/`; reconcile the stale A+B+C `docs/todo.md` entry with the
  owner.

## Self-review

- **Spec coverage:** Movement I → I.1–I.4; II → II.1–II.6; III → III.1–III.5;
  validation → II.6 + spec §Validation. No gaps.
- **No placeholders;** `docs/design/` paths and file names match the spec.
- **Reader test: where would the intended reader get lost or bored? —** The
  three-movement split risks reading as process for its own sake; mitigated
  by a one-line what/why per task and explicit review pauses (I.5, II.7) so
  the owner never reviews more than one movement at a time. No dense terms;
  the gate line is concrete, not abstract. — named and fixed.
