# Track B — Decomposition & Design

> Status: design approved in brainstorming 2026-05-22. Five sub-projects, each
> getting its own implementation plan. Supersedes the rough Track B bullets in
> `2026-05-22-v0.2-plan.md`.

**What Track B is:** reposition Codocu from owning spec→plan→code to a
**doc-first quality keeper** that delegates planning and coding to specialist
skills, and rebuild the v0.1 eight-skill set as one flexible base skill plus a
small number of focused, derived assets.

## The corpus changes the shape

A real labelled corpus exists in the reference repo Neph
(`C:/repos/bots/neph` — `docs/systems/access.md` is the calibration exemplar,
`chat-unions.md` a half-sample, `src/core/caps.py` an in-code docstring
example; the breadcrumb mechanic `System doc: <path>` is dogfooded in 7 files).
`#METADOCU` labels annotate placement decisions, positive and negative.

**Hard constraint:** METADOCU is fixture-only. It teaches *how to choose*, the
labeled instance is not to be copied, and it must never ship into a user's repo.
So the corpus is **distilled one-way, offline, into committed skill assets** —
never read at runtime, never pasted as-is. The raw corpus stays in Neph; assets
cite it via provenance lines.

### The corpus distills into FOUR assets

1. **Smell checklist** (from negative labels) — named, matchable signatures with
   remediation, `Smell / Trigger / Why / Fix`. The runtime model sees the
   *signature and fix*, never the bad instance (prevents reproducing the
   anti-pattern). ~8–12 entries; Sonnet-viable. → feeds the reviewer and the
   writer's diagnostic mode.
2. **Voice before/after pairs** — literal few-shot (dense/technical → plain/
   business). The one place few-shot beats rules. → feeds the writing skill;
   partially unparks `voice.md`.
3. **Placement decision-rules** — each a rule + one *non-imitable* illustration +
   the reasoning (voice wants imitation; placement wants reasoning — different
   encodings). → feeds the writing skill and the skeletal fresh-repo templates.
4. **Eval fixture set** — every METADOCU label is a ready-made eval case
   (negative = "must flag," before/after = "must produce ≈this," positive =
   "must not flag"). Evals are the one place the raw labeled instances belong
   (graders, not exemplars). → regression check for assets 1–3.

**Pipeline decision:** manual extraction now (corpus is n≈1.5; a generator would
overfit), written so a script *could* reproduce it later (stable structure,
provenance lines). Keep a "not-yet-distilled" gaps note so the corpus→asset link
doesn't rot. Never runtime.

## The five sub-projects

- **B-extract (foundational, first). ✅ Done 2026-05-23 (`91d5b97`).** Hand-distilled
  the Neph corpus into the four assets (+ a notes file) in `docs/corpus/`. Feeds
  every other sub-project; its assets are the source the reviewer and writer
  derive from rather than invent.
- **B-core — the base `/codocu` skill.** One flexible, principles-based skill;
  flows become optional reference overlays. Reworks the always-on orientation
  requirement (orient only when the task needs fresh state). **Two modes of one
  skill:** existing-bad-docs is reviewer-led and *subtractive* (delete
  transcription, relocate consumer-docs, run the elevation pass); fresh-repo is
  template-led and *generative* (skeletal templates seed shape + section
  semantics, never fleshed content). Delegates planning/coding to specialists;
  removes `propose`/`doc-code`/`apply`. Consumes assets 2 and 3.
- **B-review — reviewer subagents.** Strict, Sonnet-viable, launched by the main
  agent to check docs. Rules are the smell checklist (asset 1), not invented.
  Includes `fold`/`sync` as the strict reviewer/archiver and the rehomed
  elevation pass.
- **B-integrate — always-on awareness & guards.** `codocu.md` loaded via
  `CLAUDE.md`; verify standards after a specialist implements (hooks or clauses);
  rules for composing with outside skills.
- **B-cleanup — docs.** README rewrite (stale v0.1), `codocu.md` update, archive
  `flows.md` + a small sync-flow doc, finish `voice.md`, decide on `init`. Fresh-
  repo templates are skeletal, drawn from asset 3. Trails the others.

## Sequencing

B-extract → B-core / B-review (both consume B-extract; B-review is the most
Track-A/extract-ready) → B-integrate → B-cleanup. The eval set (asset 4) threads
through as the regression check for B-core and B-review.

## Guardrail (n≈1.5)

Don't over-engineer against a tiny corpus. Build the manual assets, run them
against the *next* Neph doc as an eval, and only invest in a generator, runtime
retrieval, or richer machinery if the manual assets measurably fail.
