# Codocu Skill Voice & Constriction Redesign — Design Spec

**Status:** approved (design); implementation pending
**Date:** 2026-05-17
**Amends:** `2026-05-14-codocu-design.md` — changes *how the skills express
themselves* (voice, framing, recommendation behavior). Does not change States,
Artifacts, Commands, or any flow semantics. Builds on the now-complete
`2026-05-16-codocu-deep-drill-cost-redesign-design.md` (current state is the
baseline).

---

## Problem

Usage feedback (`feedback-transcript.md`) shows the skills work correctly but
talk like a junior executor reciting a script, not a senior partner. Two
distinct failures:

1. **Scaffolding leak.** The agent narrates its own machinery to the user:
   internal step numbers ("exactly fold's Step 3"), "per the skill I default
   to Ask", internal mode names, defaults re-declaration, and cross-skill
   editorializing ("the standard `docs/plans/` directory … this repo uses a
   non-standard structure" — an `init`-flavored opinion bleeding into `fold`,
   which should treat `codocu.md` as authoritative without commentary).
2. **Defensive over-compliance.** Heavy prohibition-framed guardrails
   ("write nothing", "Stop", "do none of these unasked") trained a hedging,
   permission-seeking persona that will not commit to a recommendation. In the
   bare `/codocu` orientation a fresh user is handed three opaque formal
   options with no recommendation and an explicit refusal to act.

Root cause: the skills are authored as defensive, step-numbered procedures the
agent recites and visibly complies with, instead of internalized expertise it
acts from. The constriction language is *load-bearing for cost and safety* in
the deep-drill / read-only path (locked decisions) — so the fix must preserve
those guarantees while removing the persona damage they caused.

A separate, already-applied hotfix corrected the critical sync-state-semantics
defect (see *Prior context*); it is not part of this redesign.

## Goals

- The skills read and behave as a senior engineer who owns code/doc coherence
  for the project — a partner that reasons, commits to a recommendation, and
  speaks about the user's project, not about Codocu's internal flow.
- Eliminate scaffolding leak and defensive over-compliance across the suite.
- Replace orientation's opaque option-dump with a sized recommendation,
  including a generalizable tiered-reconciliation approach for dirty repos.
- Preserve every locked safety/cost constraint verbatim in guarantee; change
  only their framing.
- Give the Codocu developer a single control point for behavioral emphasis.
- Generalize, not over-fit to the feedback transcript.

## Non-goals

- Changing States, Artifacts, Commands, or flow semantics.
- Re-litigating locked decisions: deep-drill stays opt-in and expensive;
  read-only orientation writes nothing; no OpenSpec-specific hardcoding;
  drill cost stays user-controlled by construction.
- The two independent deep-drill follow-on todos (strengthen the §5 field-
  rename check; the bare-assent behavioral cliff) — out of scope here.
- A runtime-loaded voice/config artifact (rejected: cost-sensitive project;
  skills must stay self-contained/portable).

## Prior context (already done, not part of implementation)

- **Sync-state hotfix applied.** `skills/fold/SKILL.md` Step 5 now sets
  `Synced` unconditionally on a successful fold (matching the spec it
  implements and the router) with one tight legibility sentence;
  `skills/init/SKILL.md` now seeds `> Codocu sync state: TBD` (matching the
  design spec and `templates/codocu.md`). This corrected the
  "stays Synced … but isn't fully synced until folded" self-contradiction.
- **Deep-drill cost-redesign considered complete.** Its design deliverables
  are implemented and validated (current files + `testing/2026-05-16-dirty-
  repo-exploration/`). Closing it is bookkeeping (fold its plan); its two
  logged follow-on todos remain independent and untouched by this work.

---

## Design

### 1. The voice model

Four elements, authored into the skill prose:

**a. Operating persona.** Running any Codocu skill, the agent is a senior
engineer who owns code/doc coherence for this project — a partner, not a
procedure executor. It reasons from expertise, commits to a recommendation,
and speaks about the user's project, never about its own machinery.

**b. Anti-leak rule (global).** An explicit standard: never narrate your own
mechanism. No internal step numbers, no "per the skill" / "I default to", no
internal mode names, no defaults re-declaration, no cross-skill editorializing
about "standard vs non-standard structure". A skill treats `codocu.md` as
authoritative with zero commentary on whether it deviates from any default.
User-facing output discusses findings, recommendations, and the project only.

**c. Constraints as professional standards, not threats (global).** Every
locked safety/cost constraint stays intact in guarantee but is reframed from
prohibition to the value it serves, stated once, positively. Example:
read-only orientation's "you write nothing / Stop / do none of these unasked"
becomes *"Orientation gives you a clear read and a recommended path; it
deliberately leaves the writing to you so you stay in control."* Same
invariant, expressed as a craftsmanship norm — honored without defensively
announcing compliance or sliding into permission-seeking. This positive
framing of an unchanged hard line is the core behavioral lever.

**d. Layered recommendation (orientation).** Orientation stops dumping opaque
menus. It orients, then recommends the path it would take and why, sized to
context, and asks for the go-ahead.

- The **tiered-reconciliation principle** is authored into orientation's
  voice as how a senior reasons about a dirty repo: triage and establish the
  source of truth per area → [repeat] pick an area, make it internally
  coherent (fix code errors, doc inconsistencies, formatting/spelling) →
  sync the code and doc parts for that area → repeat.
- A named lightweight **reconciliation-plan shape** lives as an *on-demand*
  reference (same loading mechanism as `deep-drill.md`/
  `conflict-resolution.md` — zero always-loaded cost). Orientation
  instantiates it against the actual repo state **only when the repo is
  genuinely dirty/multi-area**. It carries an explicit clause: *adapt to the
  project, do not recite; for a simple one-sided desync, recommend the direct
  fix instead*. This clause is the over-fit guard — the principle
  generalizes; the shape is one tool a senior reaches for, never the only
  answer and never for simple cases.

### 2. Staged change surface

The work splits into two *categories* of change. Their execution order is
deliberately not "1 then 2" — see *Sequencing*.

**Light-touch — global, cheap (anti-leak + constraint-reframing).**
Targeted edits to the linear skills carrying leak/threat language:
`propose`, `apply`, `doc-code`, `code-doc`, `init`. `sync` is a pure alias —
unchanged. No structural rewrite; each skill keeps its flow, only leak
patterns and prohibition-framed guardrails are rewritten to positive
standards. This alone resolves the "per the skill I default to", "do none of
these unasked", and "standard vs non-standard structure" classes in these
skills.

**Deep rewrite — targeted (in-voice).**
Full in-voice rewrite of `skills/codocu/SKILL.md` (orientation) and
`skills/fold/SKILL.md` — the two skills the feedback most indicts. The
rewrite *embodies* the global anti-leak + positive-framing standard, so these
two are not separately light-touch-edited. Add
`skills/codocu/references/reconciliation-plan.md` (the named, adapt-don't-
recite shape; loaded on demand). All locked gates in these skills are
preserved verbatim in guarantee, only reframed in voice. Linear skills stay
light-touch-only unless review shows residual executor-voice.

**Sequencing (execution order).**
1. Deep-rewrite `skills/codocu/SKILL.md` (orientation) + add the
   reconciliation-plan reference.
2. Validate orientation through the harness (the staging gate: confirm the
   voice fix on the highest-pain skill before broad rollout).
3. On pass, apply the light-touch pattern across the linear skills and
   deep-rewrite `skills/fold/SKILL.md`.
4. Author `tuning.md`; re-validate; run the locked-constraint guard.

### 3. `tuning.md` — developer-time knob registry

A new evergreen doc about the plugin's own behavior. Proposed location
`docs/tuning.md`.

- **Not runtime-read.** Skill prose stays the source of truth; `tuning.md`
  is the map. This is consistent with Codocu's own bet (docs supplement and
  map; they do not drive behavior at runtime).
- **Contents.** Each behavioral dial — *voice intensity*, *recommendation
  assertiveness*, *reconciliation-plan-shape weighting* (strengthen /
  default / devalue / remove) — with its current setting and the exact
  skill-text location(s) expressing it.
- **Retune workflow** (documented in the file): edit the dial in
  `tuning.md` → run Codocu (`doc-code` on this repo) to propagate the change
  into the named skill-text locations. Retuning is a deliberate
  edit-then-propagate step, not a live dial. The registry is extensible:
  new dials are added as new behavioral knobs emerge.

### 4. Locked constraints preserved (explicit)

The rewrite must not weaken any of these; only their framing changes:

- Deep drill is opt-in and only performed on explicit accept; it is the
  expensive path; cost stays user-controlled by construction.
- Read-only orientation writes nothing — no `codocu.md`, no plan, no code,
  no docs.
- A prompt that pre-empts the missing-`codocu.md` choice (forbids creating
  `codocu.md`/`:init`) makes the agent skip the ask and orient directly.
- No OpenSpec-specific flow or forced per-plan validation; code-vs-spec /
  completion-claim detection stays generic.

---

## Validation

Reuse the existing dirty-repo harness — `testing/2026-05-16-dirty-repo-
exploration/` layout, `testing/tools/state-guard.ps1`, **subagent-scored,
never self-graded** (locked testing convention). Add a voice/partnership
dimension to the existing report template, scored alongside (not replacing)
the retained functional rubric:

Retained functional criteria: repo state correctly classified; claimed-
complete≠done still caught; read-only verify PASS (state-guard fingerprint
unchanged).

New voice/partnership criteria:
- No scaffolding leak (no step numbers, "per the skill", mode names, defaults
  re-declaration, standard-vs-non-standard editorializing).
- Sized recommendation made, not an opaque option-dump.
- Hard constraints honored without defensively narrating compliance.
- Reads as a senior partner, not a script reciter.
- **Over-fit guard:** on a simple one-sided desync, orientation recommends
  the direct fix and does *not* over-apply the reconciliation-plan shape.

Run the rewritten orientation through the harness before the suite-wide
light-touch rollout. Artifacts follow the existing `testing/README.md`
conventions (dated suite dir, run subfolders, `summary.md`, subagent
scoring).

The locked-constraint guard is a pre-rollout checklist asserting the
reframing did not weaken any constraint in *§4*; the state-guard fingerprint
already proves "writes nothing" for orientation runs.

## Out of scope / logged gaps

- Strengthening the §5 public-API field-rename check; the bare-assent
  behavioral cliff in the plan-gated drill — independent logged todos.
- Folding the now-complete deep-drill plan and committing the reorganized
  `testing/` layout — bookkeeping tracked in `docs/todo.md`, not this spec.
- Cross-repo-shape eval coverage — the harness still only scores the neph
  fixture; voice generalization to other repo shapes is unverified (logged).

## Open items / risks

- Voice/partnership scoring is fuzzier than functional pass/fail; the
  subagent rubric must give concrete leak/recommendation examples so scoring
  is repeatable, not impressionistic.
- `tuning.md` only stays accurate if retuning always goes through the
  edit-then-propagate workflow; an ad-hoc skill edit that bypasses it
  desyncs the registry. The registry itself names this as its one rule.
- Light-touch skills risk residual executor-voice; the review step must
  catch and escalate them to a full in-voice rewrite.
- Reframing a hard constraint positively could, if done carelessly, read as
  *optional*. The §4 list plus the locked-constraint guard exist to prevent
  guarantee drift while voice changes.
