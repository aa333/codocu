# Documentation work — working brief

> **Load this first** each session. It's the live orientation for the docs-and-methodology work running on Neph. Other files here are the substantive material; this is the narrative thread.

## Goals (in priority order, durable)

0. Ship apps quickly and reliably while keeping the docs supportable.
1. Build **Codocu** — a plugin/skill for documentation maintenance and processing — to help goal 0.
2. Build a set of well-written, **meta-narrated** docs from a real case (Neph), to feed back into Codocu's training. Not synthetic.
3. Improve and standardize Neph's own documentation. Originally yoked to goal 2; the yoke is heavier than expected (see "Workflow lessons").
4. Run LLM experiments on Neph to see what sticks and what doesn't — possibly skipping hand-writing of 2 and 3 if a flow lands.
5. Learn LLM skills and prompting in the process.

## Where we are (as of 2026-05-20)

- **Goal 1 (Codocu):** strongest gains so far. `methodology.md` is a usable spec for the skill — principles, tier model, breadcrumb mechanic, meta-narration framing, voice notes, elevation pass, naming-vs-enumerating distinction.
- **Goal 2 (corpus):** one strong sample (`docs/systems/access.md`, with deliberate anti-pattern blocks and METADOCU labels — the calibration exemplar). One half-sample (`docs/systems/chat-unions.md`, rewritten this session — Claude's prose with human edits; needs a human METADOCU pass to be corpus-grade).
- **Goal 3 (Neph docs):** 1.5 systems rewritten of 6 originally planned. The original phased plan is closed (archived under `_archive/`); next moves are principles-driven, one doc at a time, with explicit stop conditions.
- **Goal 4 (experiments):** this session produced material data — see "Workflow lessons". The experiment is doing what it's supposed to.
- **Goal 5 (learning):** passively accumulating through goal 4.

## Workflow lessons (durable — read these every session)

These belong in the brief because they're *how-we-work* observations, not doc-content principles. The doc-content principles live in `methodology.md`.

- **Rigid procedure suppresses critical thought.** A checklist-driven rewrite produces compliance prose and misses structural calls (tier-down, deletion, convention propagation). Procedures *do* catch mechanical mishaps in review — so we lifted them out of methodology into `review-checklist.md`, framed explicitly as a post-write reviewer's tool, not a writing recipe.
- **Principles + exemplars + license to think.** This is the writing mode that works. Principles set the bar, exemplars show the shape, explicit "stop and ask" license preserves judgment.
- **METADOCU labels teach you HOW to choose, not WHAT to include.** When reading a meta-narrated doc as a writing exemplar, treat each label as the author's chain-of-thought about placement (tier choice, naming, deletion). Do not copy the labeled instance itself unless the label says "this is the model." Anti-pattern blocks are labeled negative on purpose; they teach by contrast and must not be replicated. Without this framing, a mixed exemplar confuses; with it, the mix is *more* useful than clean prose alone.
- **Contradictions are questions, not sentences to smooth.** When fixing one part of a doc creates a hole elsewhere (this session: `bot.unions` cap superseded "owner-only" without anyone updating the limitations line), the hole is a question for the reviewer, not a non-statement to write into the gap. Surface; don't smooth.
- **The good METADOCU label is a short pointed instance-property note**, not a paraphrased rule. ~15 words, attached to a concrete property of *this* example. `access.md` has the calibration set.
- **Voice needs a corpus**, not a principle. CLAUDE.md's AGENT VOICE paragraph is a directive; without examples it produces dense compliance prose. Voice exemplar pairs grow in `methodology.md` § Voice as we encounter more.

## Current approach

- **Methodology drives writing**, review checklist catches what writing skipped.
- **One doc at a time**, with a clear stop condition: if the result isn't materially better than chat-unions.md was, stop and reassess rather than continue grinding through the remaining docs.
- **METADOCU pass by the human** on Claude's drafts. Highest meta-value per minute of human time.
- **Voice corpus grows incrementally** in `methodology.md`.
- **Plan = brief.** No phased plan with checkboxes. The "Next" section below carries the live plan and gets edited each session.

## Next

1. **Human reviews these new artifacts** (this brief, `methodology.md`, `review-checklist.md`) and edits / pushes back.
2. **Human does the METADOCU pass on `chat-unions.md`** — the corpus needs the labels to be training-grade.
3. **Phase 2 commit decision** still open. Working tree has uncommitted Phase 2 work (`docs/systems/chat-unions.md`, `src/modules/union/scope.py`) plus 13 unrelated `ruff format` reformats from drift. Three options discussed earlier (separate chore commit / reset the unrelated reformats / one combined commit); human paused for review.
4. **Pick the next doc to attempt under the new approach.** Candidates: `api-surface.md` (heaviest, most informative experiment), `game-classes.md` (medium), `db-migrations.md` / `dev-tunnel.md` (smaller, lower-risk first run).
5. **After that doc:** decide whether to continue with the remaining docs, redirect energy to Codocu directly (goal 1), or stop and let the corpus stay at what it is.

## Files in this folder (docs-methodology work only)

- `working-brief.md` — this file. Load-first.
- `methodology.md` — the doc-content principles. Drives writing.
- `review-checklist.md` — mechanical checks for post-write review.

