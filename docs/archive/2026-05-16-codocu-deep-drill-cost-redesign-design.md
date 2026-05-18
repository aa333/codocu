# Codocu Deep-Drill Cost Redesign — Design Spec

**Status:** approved (design); implementation pending
**Date:** 2026-05-16
**Amends:** `2026-05-14-codocu-design.md` — Case 4 (`/codocu` orient) read-only
orientation and its deep drill. Aligns with and extends *Git as Advisory
Signal*. Does not change States, Artifacts, or the other commands.

---

## Problem

The bare `/codocu` read-only orientation is cheap (~$0.55). The **accepted
deep drill** is not: in the iter-02 dirty-orientation test it cost **$5.83 /
467 s**, ~4.9M cache-read tokens, by fanning out into unbounded parallel
sub-audits that re-read whole files and re-derived git/plan state per audit.
Quality was good (12/13) but cost is unacceptable for the value.

Root cause is not prompt size or cache hit rate (caching was already working).
It is **token volume**: unbounded sub-audit fan-out, whole-file re-reads
instead of scoped diffs, and re-derivation of state the cheap orientation pass
already computed.

## Goals

- Cut accepted-drill cost materially while holding orientation-level quality.
- **Preserve and sharpen the priority capability:** detecting when a plan or
  spec marks work complete but the code diverged (the
  archetypes→strategy-class / claimed-complete≠done class of finding).
- Make drill spend **user-controlled by construction**, not an automatic
  expensive shot.
- Generalize beyond the neph fixture's shape (do not over-fit to repos that
  have explicit plans + checkbox specs).

## Non-goals (scope boundary)

In scope: keeping docs ↔ code coherent, smart bookkeeping/archival, and
producing a triaged drill *plan*. **Out of scope:** global analysis of huge
repositories — that requires an outside harness; Codocu detects this and hands
off rather than attempting it. Also out of scope here: slimming the other
Codocu skills, building the external harness, and cross-repo-shape eval
fixtures (logged, not built).

---

## Design

### 1. Progressive-disclosure structure

```
skills/codocu/
  SKILL.md                      # lean entry, always loaded
  references/
    deep-drill.md               # loaded ONLY when the user accepts the drill
    conflict-resolution.md      # loaded ONLY when resolving a Case-4 conflict
```

`SKILL.md` keeps read signals, read-only orientation (classify state, per-side
divergence, **offer drill → stop**), present-findings, triage, and two explicit
trigger lines:

> "Read `references/deep-drill.md` **only when** the user accepts the offered
> deep drill."
> "Read `references/conflict-resolution.md` **only when** resolving a
> both-sides conflict (Case 4)."

`conflict-resolution.md` is the existing Case-4 resolution-plan machinery moved
**verbatim** (relocation, not rewrite). The split itself saves little token
cost; its purpose is to let a precise, cheaper drill protocol exist without
inflating the always-loaded entry. Savings come from §4.

Path-resolution mechanism (how `SKILL.md` references `references/` under
plugin-cache loading) is an implementation detail for the plan, not this spec.

### 2. Layered change detection — git is a helper, not a crutch

Change detection uses three signals, git is only one:

1. **VCS diff** (git now; other SCM pluggable later) — fast path when the repo
   is tracked.
2. **Filesystem signal** — untracked/new files; mtimes vs the `codocu.md` sync
   marker or doc mtimes.
3. **Doc-corpus scan** — VCS-independent: discover docs by location/content,
   reconcile documented claims against code identifiers.

Rationale is also quality, not only portability: iter-01 scored 10/13 because
the diverged refactor was **untracked**, and git-list-only reasoning skipped
it. Reducing git reliance buys back that quality.

### 3. Two anchors (anti-over-fit)

- **Changed-surface anchor — universal bound.** The set of changed/new code
  modules and the public API objects they define. Always present; this is the
  real cost bound, even with zero plans. Each changed module/identifier is
  reconciled against any doc that references it.
- **Completion-claim anchor — sharpening when present.** *On top of* the
  changed-surface anchor, if any plan/spec/prose asserts completion (`[x]`
  **or** "done/complete/shipped/archived"), add scoped checking per
  claimed-complete unit. This catches falsely-finished plans (the priority
  metric) but is an enhancement, not the foundation.

Active plans are in scope. **Archived plans are default-excluded**; revisiting
them is opt-in "deep bookkeeping" and, even then, windowed/capped (e.g.
archived within 30 days, or N most recent) — never "all hundreds" in a mature
repo.

### 4. Drill protocol (`references/deep-drill.md`)

a. **Consume the orientation brief** already in context; do not re-derive
   git/plan/doc state. (If invoked cold without prior orientation, run one
   compact bounded inventory first — no whole-file reads.)

b. **Cheap complexity assessment.** From cheap commands only
   (`git diff --stat` / `status` / file & line counts; filesystem fallback
   when no VCS), classify the drill into a tier (table below).

c. **Disclose cost/size to the user** before doing expensive work, in plain
   terms (changed code files, changed doc files, diff lines, # active plans).

d. **Tier behavior:**
   - **Inline:** run the scoped-diff drill directly and report.
   - **Plan-gated:** produce a **triaged drill plan** (triage order in §5),
     present it inline per §6; do not execute the heavy audit unprompted.
   - **Hand-off:** decline; emit a triage skeleton at most; recommend an
     external harness.

e. **Deterministic public-API field-rename check.** For any changed file that
   defines a returned/serialized API object, enumerate added/removed/renamed
   public fields from the diff and cross-check each against long-term docs;
   report renamed public surface as a distinct divergence. This is a
   checklist, not free-form drilling — it closes the standing ProfileData
   `status*` rubric miss cheaply.

Scoping rules throughout: read **diffs**, not whole files; scope to the
changed surface / claimed unit, not the repo; no recursive whole-repo reads;
code execution is **not** default (only a single named, bounded validation
command when a behavioral claim cannot be judged from the diff, and it must be
noted as a read-only nuance).

### 5. Triage priority (formalized)

1. VCS changes + active plans (current work; sync-critical)
2. README / context files (`CLAUDE.md`, `AGENTS.md`, etc.)
3. Long-term docs modified < 1 month old
4. Archived plans — deep bookkeeping, opt-in, windowed (lowest)

### 6. Read-only resolution (resolves artifact-vs-read-only conflict)

The drill **never writes**. For plan-gated repos it **presents the triaged
drill plan inline in the response**. Persisting it to `docs/plans/`
(`YYYY-MM-DD-drill.md`, Codocu plan format) is a **separate, explicitly-gated
step requiring an initialized project** — consistent with Codocu's existing
"offer, don't perform; init to persist" stance. Once persisted, the plan is an
ordinary Codocu plan: `/codocu:apply` executes it at any pace, findings are
marked per item, `/codocu:fold` archives it. This keeps the test harness's
read-only verification intact.

### 7. `codocu.md` configuration additions

The complexity-tier thresholds are project-tunable via natural-language
`codocu.md` config (agent-interpreted, consistent with existing fold/tech-debt
config style). The v0 defaults below apply when `codocu.md` is silent or
absent.

**v0 thresholds (provisional — calibrate against iter-03; configurable):**

| Tier | Trigger | Behavior |
|---|---|---|
| Inline | ≤10 changed code files **and** ≤500 changed lines **and** ≤1 completion-claiming plan | scoped diff drill, report |
| Plan-gated | anything above inline | cost notice + triaged drill plan, inline |
| Hand-off | >150 changed files **or** >10k changed lines **or** no VCS + hundreds of source files to cold-scan | decline + triage skeleton + recommend external harness |

Calibration anchor (one datapoint, stated honestly): neph (~94 changed files,
multi-plan) is "plan-gated", and one-shotting it cost $5.83 — which is exactly
why it must be plan-gated, not one-shot.

---

## Validation

Per decision (2026-05-16): **fresh baseline**, accept the behavior change.

- **Reworked, de-leaked turn-2 prompt** (replaces the over-steering iter-02
  prompt; the leak was already logged in TODO):
  > "Yes — perform that deeper drill-down now. Still READ-ONLY: do not modify
  > or create any file (including codocu.md), do not run codocu:init. When
  > you've reported, stop."
  A barer "Yes, do the drill." variant is run as a worst-case sub-run.

- **New rubric** (replaces the 13-pt one for iter-03+). Point weights are
  deliberately deferred to the iter-03 report template, not specified here;
  the criteria below are authoritative, the weighting is a test-setup detail:
  - Repo state correctly classified (Dirty) — retained.
  - **Complexity assessment correct** — tier matches the fixture's true size.
  - **Cost disclosed** — user is told size/cost before heavy work.
  - **Sound triaged plan** — correct triage order, scoped targets, no
    whole-repo sweep, archived plans not pulled in by default.
  - **Claimed-complete≠done still caught** — the archetypes→strategy
    divergence surfaces in the triaged plan (priority metric, retained).
  - **Public-API field-rename caught** — ProfileData `status*` (closes the
    standing miss).
  - **Read-only verify PASS** — state-guard fingerprint unchanged; nothing
    written.

- iter-02's $5.83 is a **one-shot anti-pattern reference, not a like-for-like
  target**. iter-03 is a fresh baseline; same dirty neph fixture + snapshot/
  verify harness. Artifacts: `testing/transcripts/iter-03.md`,
  `testing/report-iter-03.md`, status-log row, git tag `test-iter-03` in
  codocu.

---

## Out of scope / logged gaps

- **Cross-repo-shape eval coverage.** The rubric only scores the neph fixture
  (explicit plans + checkbox specs). Generalization to plan-less / scattered-
  docs / no-VCS repos is unverified; building those fixtures is logged in TODO,
  not done here.
- Other-skill slimming; external-harness build; non-git SCM adapters — future.

## Open items / risks

- Threshold numbers are first-draft; iter-03 may move them. They are
  intentionally configurable so a wrong default is not a redesign.
- "Completion claim" prose detection ("done/shipped") is fuzzier than `[x]`;
  the protocol must treat it as a weaker signal, not authoritative.
- Plan-gated behavior depends on the user reading the inline plan; if they
  paste a barer accept, the drill must still disclose cost and present the
  plan rather than silently executing.
