# Codocu Long-Term Documentation Style — Design Spec (Spec A)

**Status:** approved (design); implementation pending
**Date:** 2026-05-17
**Amends:** `2026-05-14-codocu-design.md` — corrects one Principle and adds the
ActualDoc WHAT-summary bound to Artifacts. Does not change States, Commands, or
flow semantics.
**Relation to other specs:** This is **Spec A** of a two-spec effort on
long-term documentation. **Spec B** (Codocu onboarding model — router↔`:init`
responsibilities, `codocu.md` opinionated generation, the existing-docs stance)
is a separate, later cycle that builds on the principle and heuristic defined
here. Builds on the now-implemented (but unfolded)
`2026-05-17-codocu-skill-voice-redesign-design.md`; the current skill files are
its post-redesign, in-voice baseline.

---

## Problem

Codocu has no enforceable definition of *what a good ActualDoc contains*. The
2026-05-14 spec's Principle on long-term docs buries the most user-valuable
function — the summary of works — as a grudging aside (*"as well as provide
lean summary, not a full retelling"*). Consequences:

- The summary-of-works has no teeth: nothing tells an agent how much summary is
  enough, or what makes it too much. The ActualDoc WHY heuristic governs
  *rationale*; there is no parallel governing the *WHAT*.
- The dirty-repo testing established that soft prose guidelines do not land in
  agent behavior (the ProfileData rename missed three iterations until it
  became a non-skippable line item). A vague "keep the summary lean"
  instruction will be ignored the same way.
- The summary reiterates code, which appears to contradict Codocu's core bet
  ("code is the most detailed spec; docs don't translate it"). The
  contradiction is unresolved, so the exception reads as a loophole rather than
  a principle.

This spec resolves the tension, gives the summary an enforceable bound, and
lands it in the skills that write and assess docs.

---

## Decisions (locked in brainstorming)

1. **Drift posture — coarse, drift-resistant map.** The WHAT-summary is a
   deliberately abstract orientation map at the project's chosen ActualDoc
   granularity (module / slice / system — whatever `codocu.md` conventions
   pick; the bound is granularity-agnostic). It is bounded so ordinary
   (internal-only) code change does not invalidate it; only
   public-surface/structural change does — exactly what `code-doc`/`fold`
   already catch. Non-technical readers are served *by* the coarseness; any
   richer non-technical treatment is a per-project dial deferred to Spec B.
   *Rejected:* a maintained fold-time narrative (the SDD burden Codocu
   differentiates against) and a two-artifact split (unnecessary structure).
2. **Bound form — drift-test invariant + granularity anchor.** A positive
   inclusion list plus a negative governing test, not a length cap. Pairs with
   the existing WHY four-condition heuristic and a one-line WHERE.
3. **Placement — per-ActualDoc opening only.** Each ActualDoc opens with its
   bounded WHAT-summary. No project-level aggregated index in Spec A; that is a
   `codocu.md` dial in Spec B.
4. **Behavioral reach — spec + principles + skill propagation; no `tuning.md`
   dial.** The contract must land in the doc-writing and doc-assessing skills
   to change behavior. No "WHAT-summary strictness" dial is registered now (a
   logged future candidate). No `codocu.md`/router/`:init` changes (Spec B).

---

## Design

### 1. Principles correction (`2026-05-14-codocu-design.md` › Principles)

Review finding: of the five Principles, only the long-term-docs one is
defective. The Principles on code-as-first-class, agents-over-bloat, fleeting
plans, and cross-linking are sound and unchanged.

Replace the current bullet:

> Long-term docs answer: *why is it like that, where is it going?*, as well as
> provide lean summary, not a full retelling of what the code already says.

with two first-class Principles (terse, matching the section's voice):

> - **Long-term docs open with a coarse, drift-resistant *what*-summary** — an
>   orientation map (purpose, system role, public contract, key external deps,
>   direction) that lets a senior *or a non-technical reader* get their
>   bearings without reading code. Bounded by an invariant, not a length:
>   nothing an internal-only refactor would falsify belongs in it — that detail
>   is the code's job.
> - **Beyond the summary, docs answer *why* and *where to*** — rationale and
>   direction the code can't state for itself. Never a full re-telling of what
>   the code already says.

Net: five Principles become six.

### 2. The ActualDoc WHAT-summary bound (`2026-05-14-codocu-design.md` › Artifacts › ActualDoc)

In the ActualDoc entry, sharpen the existing line *"Answers: in short, what is
this? why is it like that? where is it going?"* to point at three bounded
parts, and add — directly beside the existing WHY four-condition heuristic —
this block:

> **The WHAT-summary (opens every ActualDoc).** A coarse orientation map of
> *what* the entity is, bounded by an invariant — not a word count.
>
> - **Names at most:** (1) the entity's purpose — what it is and the job it
>   does; (2) its place in the system — what it talks to or depends on at the
>   boundary; (3) its public contract — the capabilities/surface it offers
>   consumers; (4) its direction — one line on where it's heading.
> - **Governing test (drift invariant):** if an internal-only refactor that
>   leaves the public surface unchanged would falsify a sentence, that sentence
>   is too detailed — cut it; the code is its home. A correct WHAT-summary
>   stays correct as long as purpose and public contract are unchanged.
> - **Audience:** must read for a senior getting their bearings *and* a
>   non-technical stakeholder — no per-function, per-field, algorithmic, or
>   control-flow detail; no code unless a snippet *is* the contract.
>
> **WHY** (the existing four-condition heuristic, unchanged) and a one-line
> **WHERE** complete the doc.

The drift invariant is load-bearing: it makes the summary self-policing rather
than a maintenance tax, and it is phrased as a concrete cut-test an agent can
apply — the lesson from the ProfileData miss.

### 3. Skill propagation surface

The 2026-05-17 voice redesign is implemented in the working tree
(unmarked/unfolded; that bookkeeping is handled separately). The current skill
files are therefore the post-redesign, in-voice baseline. Spec A's propagation
is **additive edits to the current files**, authored in the established
senior-partner voice — the WHAT bound is one positive craftsmanship clause,
never a recited numbered checklist (it extends the voice work, it does not undo
it).

Propagation surface — ActualDoc *writers* and *assessors* only:

- **`skills/fold/SKILL.md` › "## Bring the docs along"** — add the WHAT-summary
  bound beside the existing WHY-heuristic sentence: a folded ActualDoc opens
  with a bounded WHAT-summary; the drift invariant decides what stays out.
- **`skills/code-doc/SKILL.md` › "## Small scope path" and "## Large /
  brownfield path"** — the WHAT bound governs what an auto-update writes and
  what a documentation plan specifies.
- **`skills/codocu/SKILL.md` orientation brief +
  `skills/codocu/references/deep-drill.md`** — when judging doc adequacy,
  assess the WHAT-summary against the bound alongside the WHY heuristic: a doc
  that re-tells code internals is *over* the bound; a doc with no orientation
  map is *under* it.

Excluded: `propose`, `apply`, `doc-code` — they produce plans/code, not
ActualDocs.

### 4. Prior-art grounding (why these opinions)

The decisions are consistent with the prior art the 2026-05-14 spec already
cites:

- **Living Documentation (Martraire):** docs evolve with code and the system
  is the primary knowledge source — the coarse map is the
  contextual/navigational layer over that source, not a re-survey of it.
- **SDD differentiation:** the drift invariant is precisely the mechanism that
  keeps the summary from degrading into the enterprise SDD maintained-narrative
  Codocu positions against.
- **Literate Programming (rejected lesson):** prose stays out of code; the map
  lives in the doc, and the existing cross-link Principle is the lightweight
  bridge — not woven prose.

### 5. Scope boundaries / non-goals

- No `tuning.md` dial (logged as a future candidate, not registered now).
- No project-level aggregated index — per-doc opening only; aggregation is a
  Spec B `codocu.md` dial.
- No `codocu.md`, router, or `:init` changes; no existing-docs-stance handling
  — all Spec B.
- No `first_draft.md` edit — it is `status: incoherent` scaffolding slated for
  migration; the authoritative principle lives in the design spec.
- No new States/Artifacts/Commands/flow semantics — Spec A refines ActualDoc
  *content* only.
- Not a retro-doc mandate — the contract governs docs written or touched going
  forward; bulk migration of existing docs is Spec B's existing-docs-stance
  concern.

---

## Validation

Spec A is its **own logical unit**: its own implementation plan, its own
harness run, its own single commit — not conflated with the unfolded
voice-redesign artifacts. The `deep-drill.md` edit is deliberate and committed
with Spec A (it was out of scope for the voice work; touching it here is
intentional, separate, and after that work).

Reuse the dirty-repo harness conventions (`testing/tools/state-guard.ps1`,
dated suite dir, run subfolders, `summary.md`, **subagent-scored in a separate
session, never self-graded** — locked testing convention; read-only fixture
contract preserved). Add a WHAT-summary dimension to the report template,
scored alongside the retained functional + voice criteria:

- **Writer side:** when `code-doc`/`fold` write or update an ActualDoc, the
  opening WHAT-summary respects the bound — granularity anchor honored
  (purpose/role/contract/deps/direction only), drift test passes (no sentence
  an internal-only refactor would falsify), no per-function/field/algorithmic
  detail.
- **Assessor side:** when orientation/`deep-drill` judge doc adequacy, they
  flag a doc that is *over* the bound (re-tells code internals) or *under* it
  (no orientation map), citing the bound.
- **Voice non-regression:** the added clauses read in-voice — no scaffolding
  leak, no recited checklist (reuses the existing voice rubric).

WHAT-summary scoring is fuzzy (like voice); the subagent rubric must give
concrete over/under examples so scoring is repeatable, not impressionistic.

---

## Open items / risks

- The bound is judgment-bearing ("public contract", "internal-only refactor").
  For most module code the public surface is clear; for scripts/configs/prose
  projects (Codocu itself) it is fuzzier. The drift test still applies (would
  an internal-only change falsify it?), but the rubric must include a
  non-code-module example.
- Spec A intentionally ships before Spec B, so the WHAT bound is honored by
  skills before `codocu.md` can tune it. Acceptable — the bound is the
  principled default; Spec B only adds per-project adjustment. Stated so the
  implementation plan does not pull Spec B forward.
- The voice-redesign plan is unfolded; Spec A's commit must not absorb or
  re-touch its files beyond the additive propagation here, to keep the two
  logical units separable for that later bookkeeping.
