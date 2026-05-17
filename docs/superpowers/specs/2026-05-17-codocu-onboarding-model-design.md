# Codocu Onboarding Model — Design Spec (Spec B)

**Status:** approved (design); implementation pending
**Date:** 2026-05-17
**Amends:** `2026-05-14-codocu-design.md` — merges `:init` into the `/codocu`
router as an onboarding branch, replaces the rigid template-copy with an
adaptive guided flow, and adds one `docs/tuning.md` dial. Does not change
States, Artifacts, or flow semantics beyond this merge.
**Relation to other specs:** This is **Spec B** of the two-spec long-term
documentation effort. **Spec A**
(`2026-05-17-codocu-longterm-doc-style-design.md`) is a **settled input**: its
WHAT-summary principle and bound are referenced here, not re-opened. Builds on
the implemented (but unfolded) `2026-05-17-codocu-skill-voice-redesign` — the
current skill files are the in-voice baseline. Per the owner's decision, Spec B
validates and commits **together with Spec A** in one combined run.

---

## Problem

`:init` is a rigid template-copy disjoint from `/codocu` (the state-aware
brain). Logged friction: "init listed as separate, gated — as a user I've no
idea what that means"; the router declined to persist work until `codocu.md`
existed; "I didn't write anything!" confusion; the template can't adapt to
repo state; `CLAUDE.md` duplicates paths already in `codocu.md`. There is no
clean responsibility split between "tell me where I stand" and "set me up",
and no explicit handling of a project's stance toward its existing docs.

---

## Decisions (locked in brainstorming)

1. **One brain (merge).** `/codocu` is the single state-aware entry point and
   gains an onboarding branch. `:init` becomes a thin alias into that branch
   with a setup bias (mirroring `:sync`→`:fold`). No separate rigid init flow.
2. **Adaptive depth + always-asked convention core.** A small fixed set of
   intent questions is always asked (even in a bare repo); repo-conditional
   questions are asked only when the signal exists.
3. **Existing-docs stance = rollout strategy (Option 1, default).** Spec A's
   WHAT-summary bound is invariant; the stance controls scope/timing only.
   Sizable migration → propose→plan.
4. **One new `docs/tuning.md` developer dial** can flip the plugin to Option 2
   (stance may soften/disable the bound) — consciously closing Spec A's
   deferral. Default is Option 1.

---

## Design

### 1. Merged entry & responsibility model

`/codocu` remains the single responsibility owner. The standalone
`skills/init/SKILL.md` rigid flow is dissolved; `/codocu:init` is a **thin
alias** that enters `/codocu` with an onboarding bias (the established
`skills/sync`→`fold` alias mechanic — the command stays discoverable).

- **Bare `/codocu`** → orient first; *offer* onboarding if uninitialized and
  it's the sensible next step.
- **`/codocu:init`** → same brain, explicit "set me up" → enter the onboarding
  branch directly (still orients enough to propose good defaults).
- **Soft-init** — an uninitialized repo the user wants to proceed on flows
  *inline* into onboarding; no separate gated command, no jargon.
- **Already-initialized repo** — onboarding never clobbers an existing
  `codocu.md`; re-entering = orient + *offer to revise* specific conventions
  (same questions, pre-filled from the current file), writing only on
  approval. This preserves the old init "don't overwrite" safety, reframed.

**Five use cases, one brain:**

| Case | Path |
|---|---|
| 1 — bare/minimal | onboarding: ask the convention core, propose full opinionated `codocu.md`, one confirm |
| 2 — brownfield, compatible docs | orient → onboarding: core + existing-docs stance; converge as areas are touched |
| 3 — incompatible docs (SDD-reiterating/scattered) | orient → assess migration size → **no interview**; route to propose→plan |
| 4 — dirty brownfield | orient (existing dirty-state handling) → resolution/recon plan; onboarding persists conventions as prerequisite |
| 5 — bare `:init`, unknown repo | alias enters onboarding; bounded orient self-classifies into 1–4, proceeds or hands off |

### 2. The onboarding branch (adaptive depth)

The branch **reuses orientation's bearings** (codocu.md present? docs? plans?
dirty?) and never re-derives what orient already found (same reuse discipline
as `deep-drill.md` §0).

**Always-asked convention core** — intent, not derivable from any repo; asked
even in a bare repo. Each offers a codocu-leaning default *and* an explicit
"take the default, revisit later" escape so adoption is never blocked:

1. **ActualDoc granularity** — module / system / feature / hybrid. Default:
   module-level, decompose on demand.
2. **What else to document** — tech-debt/TODO catchall (`TD-XXXX` model) /
   nothing beyond ActualDocs / note other conventions in Additional notes.
   Default: tech-debt catchall on. (Bounded to this choice — not an open-ended
   artifact designer.)
3. **Fold behavior for incomplete plans** — move to tech-debt / trimmed new
   plan / ask each time. Default: ask each time.

**Repo-conditional questions** (adaptive — only when the signal exists):
existing-docs stance (only if orient found existing docs — §4); dirty
handling / migration sizing (only if dirty or incompatible).

**Depth by case:**
- **Bare/trivial (1, 5-easy):** ask the three core questions, propose the
  complete filled `codocu.md`, one confirmation, done. No repo-conditional
  noise.
- **Brownfield-compatible (2):** core + existing-docs stance, every default
  pre-filled from what orient saw (detected layout → proposed granularity).
- **Incompatible / dirty (3, 4):** **no interview.** Surface the migration
  assessment / dirty read and route to propose→plan; `codocu.md` is written
  *as part of* that plan.

The branch speaks in the senior-partner voice — proposes, does not
interrogate; the "take the default" escape is always on the table.

### 3. codocu.md generation

**One skeleton, brain-filled.** The logged "add 2-3 template options, store as
files, just copy" TODO line is **superseded** by this model. Onboarding holds
one minimal skeleton and fills it from the answers, in-voice — no static
variant files.

- `templates/codocu.md` is slimmed to the **bare skeleton**: the reserved
  sync-state marker seeded `> Codocu sync state: TBD` (unchanged convention —
  real state unknown until first assessed), plus empty Docs-structure,
  What-else-to-document, Fold-settings, and Additional-notes sections.
- The fill logic and opinionated defaults live in the onboarding reference
  (§5), derived from Spec A + the cited prior art — lean, Living-Documentation
  style, deliberately *not* SDD-heavy:

| codocu.md section | Filled from | Default |
|---|---|---|
| Docs structure | core Q1 | module-level `docs/actual/`, decompose on demand; the **WHAT-summary bound named (by reference to Spec A) as the going-forward doc standard** |
| What else to document | core Q2 | tech-debt catchall `docs/tech-debt-todo.md`, `TD-XXXX` cross-links |
| Fold settings | core Q3 | ask per incomplete item |
| Existing-docs note | repo-conditional stance | written **only if docs exist** (§4) |

The doc-style line **references** Spec A's bound; it does not restate it —
`codocu.md` stays the conventions file; the bound stays defined in the design
spec/skills (no duplication).

**CLAUDE.md wiring (in scope).** When onboarding detects a `CLAUDE.md`
duplicating doc paths/conventions already in `codocu.md`, it *offers* to
replace those with a single pointer to `codocu.md` — an offer, never
automatic, never clobbering. Closes the logged "CLAUDE.md reiterates paths"
friction.

### 4. Existing-docs stance + the tuning dial

**Three stances (Option 1 / default semantics — Spec A's bound invariant):**
- **Tailor** — `codocu.md` points at the existing doc layout/locations as-is;
  the bound applies only to new/touched docs; legacy docs left non-conforming
  (the accepted "friction"). No migration.
- **In-between** — same, with explicit intent to converge: as areas are
  touched via normal `code-doc`/`fold`, their docs are brought to the bound.
  Gradual, no big-bang.
- **Full-migrate** — bring existing docs to the bound now, via **propose→plan**
  when sizable (executed and folded like any plan).

**Sizing the migration.** Reuse `code-doc`'s existing small/large judgment
(agent judgment on files changed, doc coverage, area familiarity; consult the
user on uncertainty) — one consistent sizing heuristic across the plugin.
Anything past a trivial touch → propose→plan.

**Stance → codocu.md.** Only when docs exist, onboarding writes a one-line
existing-docs note (chosen stance + pointer to legacy locations). Bare repo:
nothing written, question never asked.

**The tuning dial (new — 4th in `docs/tuning.md`).** After Voice intensity /
Recommendation assertiveness / Reconciliation-plan-shape weighting:

- **Name:** *Existing-docs stance authority.*
- **Setting (default): Option 1 — rollout-only.** Onboarding presents the
  stance purely as scope/timing; it never offers to soften or disable the
  bound; Spec A's bound is invariant.
- **Setting: Option 2 — softenable.** Onboarding additionally may offer the
  stance to dial the WHAT-summary bound down/off for the project's legacy
  docs (recorded in `codocu.md`'s existing-docs note when chosen).
- **Expressed in:** the existing-docs-stance prose of the onboarding branch
  (the new onboarding reference / `skills/codocu/SKILL.md`).
- **Retune:** edit the dial → `/codocu:doc-code` on this repo to propagate
  into the skill text (the registry's one rule), with strengthen/devalue/
  remove directions per the registry's "Adding a dial" convention.

This is the registry's first post-voice-redesign dial; it consciously closes
Spec A's deferral. Guardrail: default is Option 1; Option 2 is a deliberate
developer dial flip, propagated, never silent.

### 5. Structure & non-goals

**Where the logic lives** (established lean-SKILL + on-demand-reference
pattern):
- `skills/codocu/SKILL.md` gets a short onboarding-branch entry point.
- A **new on-demand reference `skills/codocu/references/onboarding.md`** holds
  the detail (always-asked core, adaptive depth, codocu.md fill logic +
  defaults, stance). Loaded only when the branch is taken — zero
  always-loaded cost, like `deep-drill.md` / `conflict-resolution.md` /
  `reconciliation-plan.md`. The `SKILL.md` entry pointer stays tiny.
- `skills/init/SKILL.md` is **rewritten to a thin alias** into that branch
  with a setup bias (mirrors `skills/sync`).
- `templates/codocu.md` is slimmed to the bare skeleton.

**Non-goals / out of scope:**
- **Interactive-only.** Non-interactive / `npx codocu` bootstrap stays
  V2/Future (logged) — not designed here.
- No change to States / Artifacts / Commands / flow semantics beyond the
  `init`-merge and the one tuning dial. `/codocu:init` stays a valid command
  (alias).
- Spec A's WHAT-summary bound is a settled input; `codocu.md` references it,
  this spec does not redefine it.
- No bulk retro-doc rewrite implied by adopting Codocu — the existing-docs
  stance governs that.

---

## Locked constraints preserved (explicit)

- **Read-only orientation still writes nothing by default.** Onboarding
  *writes* `codocu.md`; that write is gated behind an explicit user
  go-ahead/approval, exactly as the deep drill is gated. Soft-init must not
  violate the locked "read-only orientation writes nothing" guarantee — orient
  first, write only when the user proceeds into onboarding.
- **Never clobber an existing `codocu.md`** — re-entry offers to revise,
  writes only on approval.
- Deep-drill opt-in gate, generic (no OpenSpec-hardcoded) detection, and the
  senior-partner anti-leak voice are all preserved; new prose is in-voice.

## Validation

Folded into the **combined Spec-A + Spec-B harness run** (after this plan).
Reuse `testing/` conventions (`state-guard.ps1`, dated suite dir, run
subfolders, `summary.md`, **subagent-scored in a separate session, never
self-graded**). Spec B adds onboarding scenarios:

- **Bare repo (writer-side, disposable scratch):** onboarding asks the three
  core questions and produces a complete opinionated `codocu.md`; sync marker
  seeded `TBD`; one confirmation.
- **Brownfield-compatible (scratch):** existing-docs stance asked and the
  one-line note recorded; defaults pre-filled from detected layout.
- **Incompatible/dirty (reuse the dirty fixture, read-only):** **no
  interview** — routes to propose→plan; the locked read-only orientation
  fingerprint is unchanged (state-guard PASS) because no onboarding write
  happens without an explicit proceed.
- **Voice non-regression:** the onboarding prose reads in-voice (no
  scaffolding leak, no recited checklist).

Spec B is its own logical unit but commits **together with Spec A** per the
owner's combined-test/commit decision.

## Open items / risks

- Adding onboarding to the cost-sensitive single brain risks bloat — mitigated
  by the on-demand reference; the `SKILL.md` entry pointer must stay minimal
  and the review step must catch leak/bloat.
- "What else to document" is open-ended by nature; it is deliberately bounded
  to the three choices in core Q2 to avoid becoming an artifact designer.
- Option 2 lets a project run with Spec A's bound disabled; the
  default-Option-1 + deliberate-propagated-dial-flip guardrail prevents silent
  divergence, but a project on Option 2 is two doc philosophies coexisting —
  acceptable and intended for SDD-mandated brownfield, flagged here so it is a
  conscious choice.
- The combined Spec-A+B commit means the two specs' deliverables land
  together; the implementation plan must keep them as separable logical units
  within that single commit for clean history/folding.
