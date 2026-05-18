# Codocu Clarity Foundation — Design

**Status:** approved (design); implementation in progress
**Date:** 2026-05-17
**Follows:** `2026-05-17-codocu-skill-voice-redesign-design.md` — same goal;
that change had no enforcement and decayed within three specs.

## Problem

The skills work, but they read like an encyclopedia, not a colleague. The
voice redesign fixed this once; three later specs (longterm-doc-style,
onboarding-model, reader-economy) re-bloated the same shared sentences
because nothing forced anyone to keep them clear. Plans and specs themselves
became unreviewable — the owner's actual complaint: *"I wouldn't talk like
that to my juniors; they just won't get it."*

Root cause: clarity was treated as a feature some specs add, not a
constraint every spec must pass. A one-time cleanup with no recurring gate
decays — measured, in this repo.

## Principle

Stated canonically in `CLAUDE.md` §First principle (the dev constitution).
In one line: an artifact is judged by whether its intended reader
understands, not by whether it is complete or defensible; clarity is
re-derived in plain words, never laundered from dense prose. This spec does
not restate it — it rolls it out.

## The work — three movements

Each is independently complete and committable; sequenced so the foundation
precedes anything built on it. The owner reviews between movements.

**I. Constitution.** `CLAUDE.md` §First principle, above all conventions,
with the reconstruct-don't-launder corollary and the enforced reader-test
gate (every spec/plan self-review; manual prose validation). `docs/tuning.md`
parked — its meta-indirection is the disease, not the cure; its one useful
function (where each behavior lives) moves to the aspect specs. This spec +
plan persisted.

**II. Consolidation.** Bring the live skill surface into compliance: a new
on-demand `skills/codocu/references/doc-standard.md` (the doc-shape rule,
defined once, plainly); collapse the 6× house-rule blob to two plain
sentences; strip the duplicate clusters (reader-economy restated ~9×,
orientation-map jargon ~5×, WHY heuristic 2×); de-mechanize
`conflict-resolution.md`. Surface: the 6 `SKILL.md` files + the 4
references.

**III. Re-foundation.** Replace the dated `docs/superpowers/specs|plans/*`
pile with four evergreen aspect specs in `docs/design/`, each rebuilt from
understanding (never laundered through Codocu): `principles.md` (what Codocu
believes — the runtime-facing home of the principle), `voice.md` (who the
agent is), `flows.md` (states + moves + gates; onboarding folds in here),
`doc-standard.md` (what a long-term doc is). The six dated specs/plans move
to `docs/superpowers/archive/`.

## Not changing

States, Artifacts, Commands, flows, and every locked safety/cost constraint:
read-only orientation writes nothing; deep-drill opt-in/expensive/gated;
pre-emptive prompt skips the ask; no tool-specific hardcoding; `fold`
unconditional `Synced` + active-plans-still-Synced; `conflict-resolution`
Case-4 + don't-create-`codocu.md`-if-missing; `reconciliation-plan`
adapt-don't-recite. Only wording and file organization change.

## Validation — fully manual (owner's choice; no harness)

1. **Meaning-preservation table:** every behavioral cue in the old prose →
   its new home. An unmapped cue is a blocking defect.
2. **Locked-constraint guard:** read the final files; each constraint above
   present in guarantee.
3. **Jargon/leak sweep:** the banned tokens ("the bound", "over/under it",
   "a separate axis", "a kind read", "per the skill", internal step
   numbers) — count zero.
4. **Reader test** (the gate, applied to this work): where would the reader
   get lost or bored — named and fixed.
5. **Before/after word count** on the house rule + the worst sentences —
   evidence the bloat dropped.

## Known stale state (owner reconciles at review)

`docs/todo.md` lists Specs A+B+C as "unverified, uncommitted, pending ONE
combined harness run". They are in fact committed (HEAD); that entry is
stale. This work cleans their output, and the owner chose manual validation,
which discharges the prose/voice dimension of that pending obligation.

## Deferred

`docs/tuning.md` parked — real re-design needed (`docs/todo.md`). The
2026-05-14 design spec is archived in Movement III, not polished now.
