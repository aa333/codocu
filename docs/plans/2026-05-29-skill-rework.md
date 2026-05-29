# Skill rework — plain voice, faster reviewers

## Why

The skills work, but two things grate: the prose is dense and over-qualified, and
the reviewers are slow because each one loads three reference files before it looks
at a single doc. The dense voice starts in `principles.md` and `doc-standard.md` and
spreads from there into the SKILL and the reviewers. So we fix the language at the
source, split the one slow reviewer into a fast single-file one and a slower
multi-file one, and replace the ten-primitive scheme with a short plain workflow.

Hard rule throughout: every plain rewrite is written by hand. Nothing gets run
through Codocu or any other compressor — that is the one move the project forbids.

## Work

### 1. Language layer

- [x] **principles.md** — keep all four ideas, rewrite plain. One short principle per
  breath. Drop the over-qualification and the "not compatible with SDD" aside.
- [x] **doc-standard.md** — keep the four rules (live close to the subject; backlink
  when you name code; say only what code can't; plain summaries that survive a
  rename). Cut the Dictionary to the two or three terms actually used. Plain
  good/bad examples.
- [x] **voice.md** — keep, tighten, and add one hand-written before/after pair as the
  teaching example. Add a blunt line about being brief and leading with the answer.
- [x] **voice-pairs.md** — delete. Its job moves into the one pair in voice.md.

### 2. Reviewers

- [x] **codocu-reviewer (atomic)** — make it snappy. Inline a compact smell checklist
  in the agent prompt so it stops loading principles + doc-standard + smell-catalog.
  One file in, terse verdict + hits out. Remove the one-level cross-file peeking —
  that belongs to the cross-reviewer now.
- [x] **cross-reviewer (new)** — the slower, multi-file one. Duplication across docs,
  dangling refs and backlinks, missing docs, claims that no longer match code. It
  follows the doc graph. Absorbs the old "compositional review" that used to run in
  the main thread.
- [x] **proposal-reviewer** — delete. Its one real guard ("don't document a why nobody
  told you") survives as a line in the workflow and a smell in the atomic checklist.

### 3. SKILL workflow

- [x] Replace the ten primitives, the composition catalog, the heuristics, and the
  runtime-boundaries section in `codocu/SKILL.md` with one screen of plain prose:
  find what's affected → decide if it's worth a doc and where it lives → write it
  plain → check it (atomic reviewer after a real edit, cross-reviewer when the work
  spans several docs) → report, leading with the answer.
- [x] Keep two one-liners: uninited repo delegates to `/codocu:init`; apply docs and
  small code edits directly, surface bigger code changes.
- [x] Trim the SKILL header — a two-line essence plus the pointer to principles.md,
  not the full four principles inlined again.

### 4. Remaining rewrites (plainer, same substance)

- [x] **smell-catalog.md** — same patterns, plainer wording. Add the "invented-why"
  smell carried over from the deleted proposal-reviewer.
- [x] **placement-rules.md** — plainer. Drop the ADR ceremony; decisions stay as plain
  negative-space content with format left to each project.
- [x] **init/SKILL.md, fold/SKILL.md** — only the shared top blockquote gets the
  plain-voice treatment; the logic is untouched.

## Out of scope

`codocu.md` (root and template), init/fold logic, and the `docs/` layout stay as they
are.

## Reader test

Where would a contributor reworking these skills get lost or bored? — The risk is
this plan reads as a flat checklist with no sense of why the order matters. Fixed by
leading with the diagnosis (dense voice spreads from the language layer) so the
language-first ordering reads as deliberate, not arbitrary.
