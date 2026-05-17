# Codocu Long-Term Documentation Style (Spec A) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give Codocu's long-term docs an enforceable WHAT-summary contract — correct the design-spec Principle, add the bounded WHAT-summary heuristic beside the existing WHY heuristic, and propagate it (in-voice, additively) into the skills that write and assess ActualDocs.

**Architecture:** This is prose/prompt engineering, not code. Deliverables are Markdown edits to the design spec and four skill files, plus a validation suite. "Tests" are runs of the existing subagent-scored dirty-repo harness (`testing/tools/state-guard.ps1`, separate-session scoring), extended with a WHAT-summary dimension, plus one disposable writer-side scenario. The instrument is built and baseline-run *before* the skill edits (test-first); the current skills are expected to fail the new WHAT-summary criteria.

**Tech Stack:** Markdown skill/spec files; PowerShell harness (`pwsh testing/tools/state-guard.ps1`); headless `claude --plugin-dir`; separate-session rubric scoring.

**Spec:** `docs/superpowers/specs/2026-05-17-codocu-longterm-doc-style-design.md`

> **Execution status (2026-05-17).** Tasks 1–3 and 5–8 are complete and verified inline (spec Principles split + ActualDoc WHAT/WHY/WHERE bound; in-voice WHAT-summary propagated into `fold`, `code-doc`, `codocu` orientation, `deep-drill.md`; validation instrument created). **Validation (Tasks 4 & 9) was NOT run** — by owner decision it is consolidated into a single combined Spec-A + Spec-B harness run after the Spec B plan is implemented; **Spec A behavior is unverified until then.** **Task 10 (commit) is not done** — Spec A edits sit uncommitted in the working tree; the single commit is deferred and taken together with Spec B per the combined-test decision (still gated on an explicit ask). Step checkboxes below are intentionally left unticked per this repo's standing dogfooding deviation (`:fold`/`:apply` verify by code + git, never by `[ ]`/`[x]`).

> **COMMIT POLICY — read before executing.** This repo's `CLAUDE.md` mandates: *"No intermediate commits. Make one commit per logical unit of work, at the end. Do not commit unless asked."* This **overrides** the writing-plans default of per-task commits. There are intentionally **no per-task commit steps** below. A single commit covering all of Spec A happens in the final task, **only when the user explicitly asks**. Do not `git commit` between tasks.

> **Fixture path convention.** The harness operates on an external anonymized fixture repo, referred to as `<target-repo>` (substitute the real path via the script's `-Repo` parameter). `<codocu-repo>` is this plugin checkout. These tokens are an established harness convention (see `testing/README.md`), not plan placeholders. `<scratch>` is a freshly-created throwaway directory for the writer-side scenario (Task 9), never the protected fixture.

> **Out of scope (do not do):** Spec B (`codocu.md` opinionated generation, router↔`:init` model, existing-docs stance); registering a `tuning.md` dial; editing `first_draft.md`; folding or re-touching the unfolded 2026-05-17 voice-redesign artifacts beyond the additive in-voice edits specified here. The current skill files are the post-voice-redesign baseline and must stay in-voice — every edit below is one positive clause, never a recited checklist.

---

## Reused in-voice constraint (applies to every skill edit)

Every skill edit in Tasks 5–8 must read as the senior-partner voice already in these files: a positive craftsmanship clause, no internal step numbers, no "per the skill", no recited numbered checklist in user-facing prose. The bound's *content* is the four-part anchor + drift test; its *expression in a skill* is prose a senior would say.

---

## Task 1: Spec — correct the Principles section

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md` (Principles section, the long-term-docs bullet)

- [ ] **Step 1: Replace the defective Principle bullet with two**

Find this exact line:

```
- Long-term docs answer: *why is it like that, where is it going?*, as well as provide lean summary, not a full retelling of what the code already says.
```

Replace with:

```
- **Long-term docs open with a coarse, drift-resistant *what*-summary** — an orientation map (purpose, system role, public contract, key external deps, direction) that lets a senior *or a non-technical reader* get their bearings without reading code. Bounded by an invariant, not a length: nothing an internal-only refactor would falsify belongs in it — that detail is the code's job.
- **Beyond the summary, docs answer *why* and *where to*** — rationale and direction the code can't state for itself. Never a full re-telling of what the code already says.
```

- [ ] **Step 2: Verify in context**

Read the Principles section (`docs/superpowers/specs/2026-05-14-codocu-design.md`, the `## Principles` block). Confirm: there are now six bullets; the four sound ones (code first-class, agents-over-bloat, fleeting plans, cross-linking) are untouched; the two new bullets read in the section's terse voice; no "lean summary, not a full retelling" phrasing remains. Fix inline if not.

---

## Task 2: Spec — add the ActualDoc WHAT-summary bound

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md` (Artifacts › Long-term › ActualDoc)

- [ ] **Step 1: Replace the Answers/WHY lines with the bounded three-part block**

In the `**ActualDoc**` entry, find these exact two list items:

```
- Answers: in short, what is this? why is it like that? where is it going?
- **What belongs here (not in code):** A decision, constraint, or design choice must be documented in ActualDoc if any of the following is true: (1) the reason is non-obvious from reading the code; (2) an alternative was considered and rejected; (3) an external constraint (regulatory, performance, organizational) drove the design; (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself.
```

Replace with:

```
- Answers, in three bounded parts: a **WHAT-summary**, then **WHY**, then a one-line **WHERE**.
- **The WHAT-summary (opens every ActualDoc).** A coarse orientation map of *what* the entity is, bounded by an invariant — not a word count.
  - **Names at most:** (1) the entity's purpose — what it is and the job it does; (2) its place in the system — what it talks to or depends on at the boundary; (3) its public contract — the capabilities/surface it offers consumers; (4) its direction — one line on where it's heading.
  - **Governing test (drift invariant):** if an internal-only refactor that leaves the public surface unchanged would falsify a sentence, that sentence is too detailed — cut it; the code is its home. A correct WHAT-summary stays correct as long as purpose and public contract are unchanged.
  - **Audience:** must read for a senior getting their bearings *and* a non-technical stakeholder — no per-function, per-field, algorithmic, or control-flow detail; no code unless a snippet *is* the contract.
- **WHY — what belongs here (not in code):** A decision, constraint, or design choice must be documented in ActualDoc if any of the following is true: (1) the reason is non-obvious from reading the code; (2) an alternative was considered and rejected; (3) an external constraint (regulatory, performance, organizational) drove the design; (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself.
- **WHERE:** one line on direction — where this entity is heading.
```

- [ ] **Step 2: Verify the WHY heuristic survived verbatim and the block is consistent**

Read the `**ActualDoc**` entry. Confirm: the four numbered WHY conditions are byte-identical to the original (only the label changed to "WHY — what belongs here"); the WHAT-summary's four-part anchor + drift test + audience match the spec's Design §2 exactly; nothing in the Artifacts section now contradicts the corrected Principles (Task 1). Fix inline if not.

---

## Task 3: Build the validation instrument (test-first)

Create the scoring instrument *before* editing any skill, so the post-edit behavior can be measured and the current skills can be shown to fail the new criteria.

**Files:**
- Create: `testing/2026-05-17-longterm-doc-style/setup.md`
- Create: `testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md`

- [ ] **Step 1: Create the suite setup file**

Create `testing/2026-05-17-longterm-doc-style/setup.md` with this exact content:

```markdown
# Long-term doc style (Spec A) — test setup

Delta from the base methodology in
`testing/2026-05-16-dirty-repo-exploration/setup.md`. The assessor-side run
reuses that suite's fixture, `testing/tools/state-guard.ps1` snapshot/verify
harness, verbatim read-only prompt, locked (a)/(b)-skip decision, and the
no-self-grading rule (score in a separate session) **unchanged**.

## What this suite verifies

Spec A's WHAT-summary contract, in two parts:

- **Assessor side (read-only, reuses the 2026-05-16 fixture):** when
  orientation / deep-drill judge the fixture's docs, they assess them against
  the WHAT-summary bound — flagging docs that are *over* it (re-tell code
  internals; the fixture's OpenSpec proposal/design/tasks/spec are the
  canonical over-bound example) or *under* it (no coarse orientation map;
  scattered homebrew docs), citing the bound — without regressing any retained
  functional or voice criterion.
- **Writer side (disposable scratch, Task 9):** when `code-doc` writes/updates
  an ActualDoc, its opening WHAT-summary respects the bound (four-part anchor
  only; drift test passes; no per-function/field/algorithmic detail).

## Fixture, runbook, prerequisites (assessor side)

Identical to `2026-05-16-dirty-repo-exploration/setup.md` — fixture,
snapshot/verify, the verbatim read-only test prompt (§"Per-iteration runbook"
step 3), the locked decision that the pre-emptive prompt skips the (a)/(b)
ask. Reuse it as-is; do not modify the fixture.

## Scoring

Score from the transcript in a separate session against
`report-template-whatsummary.md` in this directory. Save filled reports as
`run<N>/result.md`, raw output as `run<N>/transcript.md`, and the delta from
this setup as `run<N>/setup-changes.md`, per `testing/README.md` conventions.
```

- [ ] **Step 2: Create the extended report template**

Create `testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md` with this exact content:

```markdown
# Test Report — Long-Term Doc Style (Spec A) — Run NN

- **Date:** YYYY-MM-DD
- **Plugin state:** <git-sha or tag>
- **Model:** Opus
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS | FAIL (if FAIL, restore run? yes/no)
- **Run type:** assessor (fixture) | writer (scratch)
- **Skill state under test:** <baseline / spec-only / full-propagation>

## Prompt used

> <exact prompt given>

## What the agent did

<3–6 lines>

## Functional score (retained — must not regress; assessor runs only)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty |  |  |
| Claimed-complete≠done caught | archetypes→strategy divergence surfaces |  |  |
| Read-only verify PASS | state-guard fingerprint unchanged |  |  |

## Voice non-regression (retained; all runs)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| No scaffolding leak | no internal step numbers, no "per the skill" / "I default to", no recited numbered checklist in user-facing prose |  |  |
| Reads as senior partner | added WHAT-summary prose reads as a colleague reasoning, not a script |  |  |

## WHAT-summary score (new)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Assessor: over-bound flagged | explicitly flags an over-bound doc (the fixture's OpenSpec specs re-tell code) and names the WHAT-summary bound as the reason — not a generic "docs are messy" |  |  |
| Assessor: under-bound flagged | explicitly flags a doc with no coarse orientation map as under the bound, citing the bound |  |  |
| Writer: anchor honored | produced/updated WHAT-summary names only purpose / place-in-system / public contract / direction |  |  |
| Writer: drift test passes | no sentence in the WHAT-summary would be falsified by an internal-only refactor (no per-function/field/algorithmic/control-flow detail; no code unless the snippet IS the contract) |  |  |

Concrete writer FAIL example: summary lists internal helpers or private field
names ("calls `_recompute_cache()`, stores `self._dirty`").
Concrete writer PASS example: "Auth module — verifies credentials for the API
layer; depends on the token store; exposes `login`/`logout`; moving to
refresh-token rotation next."

## Defects / observations

-

## Change for next run

-
```

---

## Task 4: Baseline run — confirm current skills fail the WHAT-summary criteria

Proves the instrument discriminates (test-first: the new criteria must fail before the change). Assessor side only — the writer side has nothing to baseline until the skill edits land.

**Files:**
- Create: `testing/2026-05-17-longterm-doc-style/run1/transcript.md`
- Create: `testing/2026-05-17-longterm-doc-style/run1/result.md`
- Create: `testing/2026-05-17-longterm-doc-style/run1/setup-changes.md`

- [ ] **Step 1: Snapshot the fixture (read-only)**

Run: `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
Expected: `Snapshot OK` (72 tracked, 22 untracked).

- [ ] **Step 2: Run current orientation headless**

Fresh session, cwd = `<target-repo>`: `claude --model opus --plugin-dir <codocu-repo>`.
Paste the verbatim read-only prompt from `testing/2026-05-16-dirty-repo-exploration/setup.md` §"Per-iteration runbook" step 3.
Capture full assistant output to `testing/2026-05-17-longterm-doc-style/run1/transcript.md`.
Write `run1/setup-changes.md` = "baseline: skills + spec unchanged (pre-Spec-A), plugin state <git-sha>; assessor run".

- [ ] **Step 3: Verify read-only**

Run: `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
Expected: `VERIFY PASS`. On `VERIFY FAIL`: record the defect, run `pwsh testing/tools/state-guard.ps1 restore -Repo <target-repo> -Execute`, treat the run as void and re-run after the cause is fixed.

- [ ] **Step 4: Score in a SEPARATE session (no self-grading)**

In a different session, score `run1/transcript.md` against `testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md`; save as `run1/result.md` (Run type: assessor; Skill state: baseline).
Expected: functional + voice criteria PASS; **WHAT-summary assessor criteria FAIL** (current skills have no WHAT bound, so the agent does not flag the OpenSpec specs as *over the WHAT-summary bound* nor name the bound — at most a generic "docs are messy"). If the WHAT-summary criteria do *not* fail, the instrument is too lenient — tighten the pass conditions in `report-template-whatsummary.md` (require the bound be named explicitly) and re-score before proceeding.

---

## Task 5: Propagate the bound into `skills/fold/SKILL.md`

**Files:**
- Modify: `skills/fold/SKILL.md` ("## Bring the docs along" section)

- [ ] **Step 1: Add the WHAT-summary clause ahead of the WHY paragraph**

Find this exact section:

```
## Bring the docs along

Update long-term docs only where the work genuinely warrants it. A decision
earns a doc line when the reason isn't obvious from the code, an alternative
was weighed and dropped, an external constraint forced it, or an absence was
deliberate. If none of that applies, the code already says it — leave the
docs alone. Small, clear updates: show the change, write it on approval.
Larger ones: show the diff and get an explicit yes first.
```

Replace with:

```
## Bring the docs along

When the work touches an area whose doc exists or is now warranted, that doc
opens with a coarse orientation map — what the thing is, its place in the
system, its public contract, where it's heading — and nothing an internal-only
refactor would falsify; that detail is the code's job. Keep that opening
honest as you go.

Update long-term docs only where the work genuinely warrants it. A decision
earns a doc line when the reason isn't obvious from the code, an alternative
was weighed and dropped, an external constraint forced it, or an absence was
deliberate. If none of that applies, the code already says it — leave the
docs alone. Small, clear updates: show the change, write it on approval.
Larger ones: show the diff and get an explicit yes first.
```

- [ ] **Step 2: Verify**

Read `skills/fold/SKILL.md`. Confirm: the WHY paragraph is unchanged; the new WHAT-summary paragraph is one in-voice clause (no numbered checklist, no internal step numbers, no "per the skill"); the unconditional-`Synced` and no-trust-checkboxes semantics elsewhere in the file are untouched. Fix inline if not.

---

## Task 6: Propagate the bound into `skills/code-doc/SKILL.md`

**Files:**
- Modify: `skills/code-doc/SKILL.md` ("## Small scope path" and "## Large / brownfield path")

- [ ] **Step 1: Add the WHAT-summary anchor to the small-scope WHY paragraph**

Find this exact paragraph:

```
Apply the ActualDoc WHY heuristic when deciding what to document: write to ActualDoc if (1) the reason is non-obvious from reading the code, (2) an alternative was considered and rejected, (3) an external constraint drove the design, or (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself — no doc update needed.
```

Replace with:

```
Any ActualDoc you write or update opens with a coarse orientation map — the area's purpose, its place in the system, its public contract, where it's heading — bounded so nothing an internal-only refactor would falsify lands in it; that detail is the code's job. On top of that, apply the ActualDoc WHY heuristic when deciding what rationale to document: write to ActualDoc if (1) the reason is non-obvious from reading the code, (2) an alternative was considered and rejected, (3) an external constraint drove the design, or (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself — no doc update needed.
```

- [ ] **Step 2: Add the WHAT-summary clause to the large/brownfield path**

Find this exact block:

```
Draft a **ProposalSummary** in-conversation:
- What to document (areas, modules)
- Which existing docs to update
- Which new docs to create

Ask for approval. Iterate until approved.
```

Replace with:

```
Draft a **ProposalSummary** in-conversation:
- What to document (areas, modules)
- Which existing docs to update
- Which new docs to create

Each doc opens with a coarse orientation map — purpose, place in the system,
public contract, direction — bounded so nothing an internal-only refactor
would falsify lands in it; the WHY heuristic governs what rationale earns a
line on top of that.

Ask for approval. Iterate until approved.
```

- [ ] **Step 3: Verify**

Read `skills/code-doc/SKILL.md`. Confirm: both edits present; the four WHY conditions are unchanged in the small path; the sync-state-line phrasing and flow elsewhere are untouched; both added clauses are in-voice (no recited numbered checklist in user-facing prose). Fix inline if not.

---

## Task 7: Propagate the bound into `skills/codocu/SKILL.md` (orientation brief)

**Files:**
- Modify: `skills/codocu/SKILL.md` (the orientation-brief bullet list)

- [ ] **Step 1: Extend the "what the docs and plans claim" bullet**

Find this exact bullet:

```
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete;
```

Replace with:

```
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete, and whether the long-term docs read as a coarse orientation map or
  drift over the bound (re-telling code internals) or under it (no orientation
  map at all);
```

- [ ] **Step 2: Verify**

Read `skills/codocu/SKILL.md`. Confirm: only that bullet changed; the read-only orientation guarantee, the deep-drill opt-in gate, the pre-emptive-prompt skip, and the generic (no OpenSpec-hardcoded) detection are all intact; the added clause is in-voice. Fix inline if not.

---

## Task 8: Propagate the bound into `skills/codocu/references/deep-drill.md`

**Files:**
- Modify: `skills/codocu/references/deep-drill.md` (§4 Anchors, anchor 1)

- [ ] **Step 1: Add doc-adequacy-against-the-bound to the changed-surface anchor**

Find this exact item:

```
1. **Changed-surface (always).** For each changed/new code module and each
   public API object it defines, reconcile it against any doc that references
   that module or identifier. This is the universal bound and works with zero
   plans.
```

Replace with:

```
1. **Changed-surface (always).** For each changed/new code module and each
   public API object it defines, reconcile it against any doc that references
   that module or identifier. This is the universal bound and works with zero
   plans. Also judge the doc itself against the WHAT-summary bound: a doc that
   re-tells code internals is over the bound; one with no coarse orientation
   map (purpose, place, public contract, direction) is under it — report
   either as a distinct divergence.
```

- [ ] **Step 2: Verify**

Read `skills/codocu/references/deep-drill.md`. Confirm: only anchor 1 changed; the read-only contract, the tier table, the cost-disclosure gate, and the deterministic field-rename check (§5) are untouched; no OpenSpec-specific hardcoding introduced. Fix inline if not.

---

## Task 9: Re-validate — assessor pass + writer-side scenario + suite summary

**Files:**
- Create: `testing/2026-05-17-longterm-doc-style/run2/transcript.md`
- Create: `testing/2026-05-17-longterm-doc-style/run2/result.md`
- Create: `testing/2026-05-17-longterm-doc-style/run2/setup-changes.md`
- Create: `testing/2026-05-17-longterm-doc-style/run3/transcript.md`
- Create: `testing/2026-05-17-longterm-doc-style/run3/result.md`
- Create: `testing/2026-05-17-longterm-doc-style/run3/setup-changes.md`
- Create: `testing/2026-05-17-longterm-doc-style/summary.md`

- [ ] **Step 1: Assessor re-run — snapshot**

Run: `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
Expected: `Snapshot OK` (72 tracked, 22 untracked).

- [ ] **Step 2: Assessor re-run — run + verify read-only**

Fresh session, cwd = `<target-repo>`: `claude --model opus --plugin-dir <codocu-repo>`. Paste the same verbatim read-only prompt as Task 4 Step 2. Capture to `run2/transcript.md`. Write `run2/setup-changes.md` = "full Spec-A propagation in place (Tasks 1–2 spec + Tasks 5–8 skills); assessor run".
Then run: `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
Expected: `VERIFY PASS`. On FAIL: record defect, `restore … -Execute`, fix the offending skill (the leak/over-eager write is the defect), re-run.

- [ ] **Step 3: Assessor re-run — score in a SEPARATE session**

Score `run2/transcript.md` against `report-template-whatsummary.md`; save as `run2/result.md` (Run type: assessor; Skill state: full-propagation).
Expected: **all functional criteria PASS (no regression vs Task 4 baseline)**, **voice non-regression PASS**, AND **WHAT-summary assessor criteria PASS** (over-bound flagged on the OpenSpec specs with the bound named; under-bound flagged on a map-less homebrew doc). If any functional/voice criterion regressed or a WHAT-summary criterion failed: revise the offending skill edit (Tasks 5–8) per `run2/result.md` "Change for next run" and repeat Steps 1–3 with a new run folder.

- [ ] **Step 4: Writer-side scenario — build the disposable scratch repo**

Create a throwaway directory `<scratch>` (outside `<target-repo>` and `<codocu-repo>`; e.g. a temp dir). Create exactly these files:

`<scratch>/codocu.md`:
```markdown
# Codocu

> Codocu sync state: Synced

## Docs structure

Module-level docs in `docs/actual/`. One file per module.
```

`<scratch>/src/auth.py`:
```python
"""Credential verification for the API layer."""

class TokenStore:
    def __init__(self):
        self._cache = {}

    def _recompute(self, user_id):
        self._cache[user_id] = compute_hash(user_id)

def login(username, password):
    """Public: verify credentials, return a session token."""
    return _issue_token(username)

def logout(token):
    """Public: invalidate a session token."""
    _revoke(token)
```

`<scratch>/docs/actual/auth.md` (intentionally stale + over-bound, so an update is warranted and the bound is testable):
```markdown
# auth

The auth module has a `TokenStore` class with a `_cache` dict and a
`_recompute(user_id)` method that calls `compute_hash`. `login(username,
password)` internally calls `_issue_token` and `logout(token)` calls
`_revoke`. The cache is a plain dict keyed by user id.
```

- [ ] **Step 5: Writer-side scenario — run `code-doc` headless**

Fresh session, cwd = `<scratch>`: `claude --model opus --plugin-dir <codocu-repo>`.
Prompt (paste verbatim):
> `/codocu:code-doc I renamed nothing public but refactored TokenStore internals; bring docs/actual/auth.md up to date with the code.`
Capture full assistant output (and the resulting `<scratch>/docs/actual/auth.md`) to `run3/transcript.md`. Write `run3/setup-changes.md` = "writer-side scenario in disposable <scratch>; full Spec-A propagation in place". No state-guard here (scratch is disposable, not the protected fixture).

- [ ] **Step 6: Writer-side scenario — score in a SEPARATE session**

Score `run3/transcript.md` (including the rewritten `auth.md`) against `report-template-whatsummary.md`; save as `run3/result.md` (Run type: writer; Skill state: full-propagation).
Expected: **Writer: anchor honored PASS** (the rewritten `auth.md` opens with purpose / place / public contract `login`/`logout` / direction only) and **Writer: drift test passes PASS** (no mention of `TokenStore`, `_cache`, `_recompute`, `_issue_token`, `_revoke`, or "dict keyed by user id" — all internal-only, exactly the detail an internal refactor falsifies). Voice non-regression PASS. If it fails, revise the `code-doc` edit (Task 6) per `run3/result.md` and repeat Steps 4–6. Delete `<scratch>` when done.

- [ ] **Step 7: No-regression / locked-constraint guard**

Manually inspect the final files and record PASS/FAIL with file:line evidence in `run2/result.md` under "Defects / observations":
1. `docs/superpowers/specs/2026-05-14-codocu-design.md` — the four WHY conditions are byte-identical to pre-Spec-A; six Principles; WHAT block matches spec §2.
2. `skills/codocu/SKILL.md` — read-only orientation writes nothing; deep-drill opt-in gate intact; pre-emptive-prompt skip intact; detection still generic (no OpenSpec hardcoding).
3. `skills/fold/SKILL.md` — unconditional `Synced` on successful fold + active-plans-still-Synced note + no-trust-checkboxes verification all intact.
4. `skills/code-doc/SKILL.md`, `skills/codocu/references/deep-drill.md` — only the specified clauses added; no flow/contract change; in-voice.
5. No `tuning.md`, `codocu.md`, `first_draft.md`, router/`:init`, or voice-redesign-artifact changes were made (Spec A scope boundary).
Any FAIL → fix the offending file and repeat the relevant validation steps.

- [ ] **Step 8: Write the suite scoreboard**

Create `testing/2026-05-17-longterm-doc-style/summary.md`: a status-log table (run, plugin state, run type, functional, voice, WHAT-summary, read-only, headline) across run1 (assessor baseline — WHAT-summary FAIL expected), run2 (assessor full-propagation), run3 (writer), plus a short narrative and any open findings. Follow the shape of `testing/2026-05-16-dirty-repo-exploration/summary.md`.

---

## Task 10: Final commit (ONLY when the user asks)

Per `CLAUDE.md`, this is the single commit for the whole Spec A logical unit. **Do not run this task until the user explicitly asks to commit.**

**Files:**
- (commit only; no new edits)

- [ ] **Step 1: Confirm scope, then commit once**

Stage exactly Spec A's deliverables: `docs/superpowers/specs/2026-05-17-codocu-longterm-doc-style-design.md` (already written), `docs/superpowers/specs/2026-05-14-codocu-design.md` (Tasks 1–2), `skills/fold/SKILL.md`, `skills/code-doc/SKILL.md`, `skills/codocu/SKILL.md`, `skills/codocu/references/deep-drill.md` (Tasks 5–8), `docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md` (this plan), and the new `testing/2026-05-17-longterm-doc-style/` suite. Do **not** stage unfolded voice-redesign artifacts or any Spec B / out-of-scope file. Commit with a message summarizing "Spec A: long-term doc-style — WHAT-summary principle + bound + in-voice skill propagation". Use the repo's commit trailer convention. Do not push unless asked. Suggest `/codocu:fold` afterward to archive this plan.

---

## Self-Review

**1. Spec coverage:**
- Principles correction (spec §Design 1) → Task 1 (verbatim before/after matches spec).
- ActualDoc WHAT-summary bound, WHY preserved verbatim (spec §Design 2) → Task 2.
- Skill propagation surface — fold / code-doc / codocu orientation brief / deep-drill, in-voice, additive, writers+assessors only (spec §Design 3) → Tasks 5, 6, 7, 8.
- Validation: reuse dirty-repo harness, subagent/separate-session, read-only contract, baseline-fails-first, WHAT-summary dimension added, writer + assessor sides, fuzzy-scoring concrete examples (spec §Validation) → Tasks 3, 4, 9.
- Own logical unit / own single commit / not conflated with voice artifacts; deep-drill edit deliberate & in Spec A's commit (spec §Validation) → Task 10 + COMMIT POLICY/Out-of-scope banners.
- Scope boundaries (no tuning dial / no project index / no codocu.md-router-init / no first_draft / no new lifecycle / not retro-mandate) → Out-of-scope banner + Task 9 Step 7 item 5.
- All covered; no gaps.

**2. Placeholder scan:** No "TBD/TODO/implement later/handle edge cases". `<target-repo>`/`<codocu-repo>` are documented harness conventions; `<scratch>` is explicitly defined as a freshly-created throwaway dir with exact file contents given. Every find/replace block and every scratch file is given verbatim. No "similar to Task N".

**3. Type/string consistency:** The WHY four-condition text is byte-identical in Task 2's "after", in fold/code-doc (left unchanged there), and asserted unchanged in Task 9 Step 7. The four-part WHAT anchor wording (purpose / place in system / public contract / direction) is consistent across Tasks 2, 5, 6, 7, 8 and the report template. Suite/dir/file names (`testing/2026-05-17-longterm-doc-style/`, `report-template-whatsummary.md`, `run1`/`run2`/`run3`) are consistent everywhere referenced. The writer-side FAIL tokens in Task 9 Step 6 (`TokenStore`, `_cache`, `_recompute`, `_issue_token`, `_revoke`) exactly match the scratch `src/auth.py` / `auth.md` contents in Step 4.
