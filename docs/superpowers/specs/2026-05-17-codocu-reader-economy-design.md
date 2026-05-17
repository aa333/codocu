# Codocu Reader Economy — Design Spec ("Apply Varya's prompt")

**Status:** approved (design); implementation pending
**Date:** 2026-05-17
**Amends:** `2026-05-14-codocu-design.md` — adds one Principle (reader economy)
and registers a fifth `docs/tuning.md` dial. Does not change States,
Commands, Artifacts schemas, or flow semantics.
**Relation to other specs:** Third separable logical unit after **Spec A**
(`2026-05-17-codocu-longterm-doc-style-design.md`, the WHAT-summary scope
bound) and **Spec B** (`2026-05-17-codocu-onboarding-model-design.md`). Builds
on A's bound as an *orthogonal companion* and on the implemented-but-unfolded
voice redesign; the current skill files are the in-voice baseline. Validated by
the **same combined harness run** already mandated for A+B in `docs/todo.md`
(third additive dimension, not a forked suite).

---

## Problem

Codocu can keep a doc *in scope* (the WHAT-summary bound) and still leave it an
exhausting read — redundant, duplicated, padded, the load-bearing sentence
buried. Scope and reader experience are different axes; only the first has any
teeth today. The dirty-repo testing already established that soft prose
guidelines do not land in agent behavior unless they are rooted, registered,
and propagated. Nothing currently makes Codocu *value* a kind read — for docs,
for plans (an obtuse plan goes unreviewed), or for its own orientation briefs.
Attention is the scarcest resource for every reader Codocu writes for, human or
agent.

---

## Decisions (locked in brainstorming)

1. **Scope of reach.** The value governs full ActualDocs (not just the WHAT
   opening), WHY/WHERE prose, plans, *and* the agent's own reader-facing
   replies (orientation briefs, proposals, close-outs). Going-forward
   disposition — **no retro-cleanup** of Codocu's own meta-docs this session
   (a later restructure handles that).
2. **Enforcement — both dials.** (A) Live orientation/deep-drill flags
   reader-economy defects in a project's *existing* docs, as a finding beside
   the existing scope finding (user-visible, colleague-phrased). (B) One
   holistic reader-experience row in the separate-session test rubric so the
   testing session can observe it. Writer-side internalized voice is in scope
   regardless of A/B.
3. **Encoding — full layered (Approach 1).** Spec Principle → `docs/tuning.md`
   dial → in-voice skill propagation → test rubric row. The repo's own rule:
   a behavioral knob unregistered in `tuning.md` silently desyncs.
4. **Not a cage.** Expressed as one positive craftsmanship clause in the voice
   layer — never a numbered checklist, length cap, or per-artifact pass/fail
   gate the writer must clear. The rubric row is a holistic separate-session
   observation, like the WHAT-summary assessor rows — not a writer gate. It
   sharpens an instinct; it never overrides a user who asks for exhaustive
   detail. *Rejected:* a checkable readability bound (the cage the owner
   excluded); a self-consistency invariant (owner reserves the tone pass).
5. **Orthogonal to the WHAT-summary bound, not merged.** Scope = *what content
   belongs*; reader economy = *whether it reads without exhausting the
   reader*. The Principle states this explicitly so the agent never reads
   "I stayed in scope" as "this reads well".

---

## Design

### The anchor

The value, in Codocu's own register (the source phrasing for the Principle and
the in-voice clauses; final wording is the owner's tone pass):

> Every doc, plan, and brief is written for a perpetually busy reader whose
> attention is the scarcest resource in the project — human or agent. They
> should come away saying "thanks, I get it," not abandon it halfway through
> "what a mess." Lead with the answer; say each thing once, in one place; cut
> anything that restates the code or earns no decision. Length is never the
> target — wasted reader attention is the defect.

### 1. Principle addition (`2026-05-14-codocu-design.md` › Principles)

Add one bullet after the two WHAT/WHY bullets (six Principles become seven),
terse, in the section's voice — substance, owner sets final wording:

> - **Every doc, plan, and brief is written for a perpetually busy reader** —
>   human or agent; attention is the scarcest resource. Lead with the answer,
>   say each thing once, cut whatever restates the code or earns no decision.
>   Orthogonal to the WHAT-summary bound: that governs *what content belongs*;
>   this governs *whether it reads without exhausting the reader*. The defect
>   is wasted attention, never length itself.

### 2. Register the `docs/tuning.md` dial (fifth dial)

Add a "Reader economy" dial in the existing dial format — setting,
expressed-in locations (every surface in §3), strengthen/devalue/remove
directions. Setting: **On** — internalized in the shared house-rule voice;
live orientation/deep-drill flags reader-economy defects; one holistic
assessor + writer row in the test rubric. Devalue floor: keep the house-rule
clause regardless (internalized economy is never undesirable); soften only the
live finding. The dial's existence is what satisfies decision 3's
"unregistered = silent desync" rule.

### 3. Skill propagation surface (in-voice, additive)

Additive edits to the current in-voice baseline — one positive craftsmanship
clause each, never a recited checklist; Codocu register, not the brainstorming
register.

- **Shared house-rule line in every `skills/*/SKILL.md`** — append a compact
  reader-economy clause to the existing `_Operate as the engineer…_` line.
  Single most-leveraged edit; rides every flow; `apply`/`init`/`sync` inherit
  it. This is the "in its nature" mechanism.
- **`skills/propose/SKILL.md` (plan format) + `skills/doc-code/SKILL.md`
  ("Write the plan")** — the plan is written for a busy reviewer; an obtuse
  plan goes unreviewed.
- **`skills/code-doc/SKILL.md` (small + brownfield paths) +
  `skills/fold/SKILL.md` ("Bring the docs along")** — a reader-economy
  companion clause beside the existing WHAT-summary clause (kept distinct, not
  merged — decision 5).
- **`skills/codocu/SKILL.md` orientation brief bullet +
  `skills/codocu/references/deep-drill.md` anchor 1** — extend the existing
  scope-drift finding so it also flags reader-economy defects in *existing*
  docs (dial A — the user-visible live finding).

Deliberate non-edits (parity, not oversight): `templates/codocu.md` untouched
— a standard is referenced, not restated in per-project conventions (same
treatment the WHAT bound gets, onboarding §5); `apply`/`init`/`sync` get no
targeted edit (inherit via the shared line / delegation); no new test suite;
Spec A/B unfolded working-tree artifacts not re-touched beyond this additive
clause.

### 4. Prior-art grounding

Consistent with the prior art the 2026-05-14 spec cites: **Living
Documentation (Martraire)** — docs are the navigational layer over the code,
worthless if the navigator won't read them; the **agents-over-bloat**
Principle already in the spec extends naturally from "focused code over
bloated docs" to "focused docs over bloated docs". This Principle names the
reader the others assume.

### 5. Scope boundaries / non-goals

- No checkable readability bound, length cap, or writer-side gate (the cage
  the owner excluded).
- No self-consistency invariant on the skill prose (owner reserves the tone
  pass).
- No retro-cleanup of Codocu's own meta-docs; no new States/Artifacts/Commands
  /flow semantics; no `codocu.md`/template change.
- Not a forked validation suite — third additive dimension on the combined
  Spec-A+B harness run.

---

## Validation

Rides the combined run `docs/todo.md` already mandates for A+B — a **third
additive dimension**, not a separate suite. Test-first holds: a baseline must
show the current skills neither flag reader-economy defects in the fixture's
docs nor produce reader-economical output (instrument discriminates); the
post-edit run shows they do. Reuse the locked conventions — dirty-repo
harness, dated suite dir, **subagent-scored in a separate session, never
self-graded**, read-only fixture contract.

Add one holistic **Reader experience** row to
`testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md`:

- **Assessor side:** orientation/deep-drill flags an existing doc a busy
  developer would abandon — redundancy, duplication, buried answer — *distinct
  from* the WHAT-summary scope finding, not collapsed into "docs are messy".
- **Writer side:** a doc/plan/brief Codocu produces reads answer-first, says
  each thing once, no padding — judged holistically, with concrete
  pass/fail exemplars in the rubric so scoring is repeatable, not
  impressionistic.
- **Voice non-regression:** the added clauses read in-voice — no scaffolding
  leak, no recited checklist (reuses the existing voice rubric).

---

## Open items / risks

- Reader economy is fuzzy and judgment-bearing — fuzzier than the WHAT drift
  test. Mitigation: the rubric must carry concrete over/under exemplars, like
  the voice and WHAT-summary dimensions.
- This is its own separable logical unit ("Apply Varya's prompt" in
  `docs/todo.md`), layered on the uncommitted Spec A/B working tree. Validated
  by the same combined run; commit grouping is deferred to the owner's
  explicit ask (per `CLAUDE.md`). The implementation plan must not pull A/B
  forward or re-touch their files beyond this additive clause, keeping the
  units separable.
- Contamination guard: every permanent edit is in Codocu's senior-partner
  register; `docs/superpowers/**` is throwaway scaffolding for this session
  only.
