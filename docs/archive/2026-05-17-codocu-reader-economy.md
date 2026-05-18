# Codocu Reader Economy ("Apply Varya's prompt") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode a reader-economy value across Codocu — one Principle, one `docs/tuning.md` dial, in-voice propagation into the skills that write/judge docs, plans, and briefs, and one holistic test-rubric row — so every artifact reads for a busy reader without becoming a cage.

**Architecture:** Prose/prompt engineering, not code. Deliverables are additive Markdown edits to the design spec, `docs/tuning.md`, six skill files, one reference, and the existing combined test rubric. "Tests" are the deferred combined Spec-A+B+C harness run, scored separate-session against the extended rubric. The instrument (rubric row) is extended **before** the skill edits (test-first); current skills are expected to fail the new Reader-experience criteria.

**Tech Stack:** Markdown skill/spec files; PowerShell harness (`pwsh testing/tools/state-guard.ps1`); headless `claude --plugin-dir`; separate-session rubric scoring.

**Spec:** `docs/superpowers/specs/2026-05-17-codocu-reader-economy-design.md`

---

> **COMMIT POLICY — read before executing.** This repo's `CLAUDE.md` mandates: *"No intermediate commits. Make one commit per logical unit of work, at the end. Do not commit unless asked."* This **overrides** the writing-plans default of per-task commits. There are intentionally **no per-task commit steps** below. A single commit covering this whole unit happens in the final task, **only when the user explicitly asks**. Do not `git commit` between tasks.

> **IN-VOICE / CONTAMINATION CONSTRAINT (applies to every skill edit).** Every edit must read as the senior-partner voice already in these files: one positive craftsmanship clause, no internal step numbers, no "per the skill", no recited numbered checklist in user-facing prose. It must be **Codocu's register, not the brainstorming/superpowers register**. `docs/superpowers/**` is throwaway scaffolding for this session. The exact replacement strings below are deterministic and good enough to ship; the owner takes a separate tone pass afterward — do not over-polish or add a self-consistency gate.

> **VALIDATION IS DEFERRED & COMBINED.** Per `docs/todo.md`, ONE combined harness run validates Spec A + Spec B + this unit (third additive dimension), taken on an explicit owner ask. This plan **builds the instrument** (Task 3) and **records the combined-run expectation** (Task 5); it does **not** run `claude` headless inline. Spec A's plan established this same deferred posture.

> **Out of scope (do not do):** any checkable readability bound / length cap / writer-side gate; a self-consistency invariant on skill prose; retro-cleanup of Codocu's own meta-docs; `templates/codocu.md`, `skills/init/SKILL.md`, `skills/sync/SKILL.md` edits (relays/standard-referenced — they inherit); re-touching Spec A/B unfolded artifacts beyond the additive clause here; pulling Spec A/B forward; any commit before the final task.

> **Dogfooding caveat.** Per this repo's standing deviation, plan-step checkboxes are tracking only, never evidence of verification. Verify deliverables by reading the files + git, not by `[ ]`/`[x]`.

---

## Task 1: Spec — add the reader-economy Principle

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md` (`## Principles`)

- [ ] **Step 1: Insert the seventh Principle bullet**

Find this exact two-line block (the last two Principles):

```
- **Beyond the summary, docs answer *why* and *where to*** — rationale and direction the code can't state for itself. Never a full re-telling of what the code already says.
- Code and docs cross-link so that editing one nudges the agent toward updating the other.
```

Replace with (inserts one bullet between them):

```
- **Beyond the summary, docs answer *why* and *where to*** — rationale and direction the code can't state for itself. Never a full re-telling of what the code already says.
- **Every doc, plan, and brief is written for a perpetually busy reader** — human or agent; attention is the scarcest resource. Lead with the answer, say each thing once, cut whatever restates the code or earns no decision. Orthogonal to the WHAT-summary bound: that governs *what content belongs*; this governs *whether it reads without exhausting the reader*. The defect is wasted attention, never length itself.
- Code and docs cross-link so that editing one nudges the agent toward updating the other.
```

- [ ] **Step 2: Verify in context**

Read the `## Principles` block. Confirm: seven bullets now; the original six (code-first-class, agents-over-bloat, fleeting plans, WHAT-summary, beyond-summary-why/where, cross-link) are untouched; the new bullet is terse and in the section's voice; it explicitly states orthogonality to the WHAT-summary bound. Fix inline if not.

---

## Task 2: Spec — register the fifth `docs/tuning.md` dial

**Files:**
- Modify: `docs/tuning.md` (insert a dial before `## Adding a dial`)

- [ ] **Step 1: Insert the "Reader economy" dial**

Find this exact block (end of the "Existing-docs stance authority" dial + the next heading):

```
- **Devalue / remove:** not applicable — Option 1 is the floor; there is no
  setting weaker than rollout-only.

## Adding a dial
```

Replace with:

```
- **Devalue / remove:** not applicable — Option 1 is the floor; there is no
  setting weaker than rollout-only.

### Reader economy
How hard the skills push every doc/plan/brief to read well for a busy reader
(lead with the answer, say it once, no bloat) vs. leaving prose quality to
chance. Orthogonal to the WHAT-summary bound — that governs scope; this
governs the read.
- **Setting:** On — internalized in the shared house-rule voice; live
  orientation/deep-drill flags reader-economy defects in existing docs as a
  finding distinct from the scope finding; one holistic reader-experience row
  (assessor + writer) in the test rubric.
- **Expressed in:** the shared `_Operate as the engineer…_` house-rule line in
  every `skills/*/SKILL.md` that carries it (`codocu`, `fold`, `propose`,
  `code-doc`, `doc-code`, `apply`); `skills/propose/SKILL.md` and
  `skills/doc-code/SKILL.md` (plan-for-a-reviewer clause);
  `skills/code-doc/SKILL.md` (small + brownfield paths) and
  `skills/fold/SKILL.md` ("Bring the docs along"); `skills/codocu/SKILL.md`
  orientation brief and `skills/codocu/references/deep-drill.md` anchor 1
  (live finding); `testing/2026-05-17-longterm-doc-style/
  report-template-whatsummary.md` (Reader-experience row).
- **Strengthen:** sharpen the house-rule clause toward an explicit cut-test;
  widen the live orientation finding.
- **Devalue:** soften the live finding to writer-side only; keep the
  house-rule clause regardless — internalized economy is never undesirable.
- **Remove:** drop the house-rule clause and the rubric row; orientation then
  judges only the WHAT-summary scope bound.

## Adding a dial
```

- [ ] **Step 2: Verify**

Read `docs/tuning.md`. Confirm: five dials now; the four originals are untouched; the new dial follows the existing setting / expressed-in / strengthen / devalue / remove format; the expressed-in list matches every surface edited in Task 4 (no more, no less). Fix inline if not.

---

## Task 3: Extend the validation instrument (test-first, before any skill edit)

Extend the existing combined rubric **before** editing skills, so the post-edit behavior is measurable and current skills can be shown to fail the new criteria.

**Files:**
- Modify: `testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md`

- [ ] **Step 1: Add the Reader-experience section**

Find this exact block (the WHAT-summary concrete examples + the next heading):

```
Concrete writer FAIL example: summary lists internal helpers or private field
names ("calls `_recompute_cache()`, stores `self._dirty`").
Concrete writer PASS example: "Auth module — verifies credentials for the API
layer; depends on the token store; exposes `login`/`logout`; moving to
refresh-token rotation next."

## Defects / observations
```

Replace with:

```
Concrete writer FAIL example: summary lists internal helpers or private field
names ("calls `_recompute_cache()`, stores `self._dirty`").
Concrete writer PASS example: "Auth module — verifies credentials for the API
layer; depends on the token store; exposes `login`/`logout`; moving to
refresh-token rotation next."

## Reader-experience score (new — Spec C; orthogonal to WHAT-summary)

Holistic, scored separate-session. NOT a writer gate — an observation, like
the WHAT-summary assessor rows. Reader economy is a different axis than scope:
an in-bound doc can still be an exhausting read.

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Assessor: bad read flagged | flags an existing doc a busy developer would abandon — redundancy, duplication, padding, answer buried — as a finding **distinct from** the WHAT-summary scope finding, not collapsed into a generic "docs are messy" |  |  |
| Writer: reads answer-first | a doc/plan/brief the agent produced leads with the answer, says each thing once, no padding a busy reader would resent |  |  |
| Voice non-regression | the added reader-economy clauses read in-voice — no scaffolding leak, no recited checklist (reuses the voice rubric) |  |  |

Concrete assessor FAIL example: "the docs are messy and out of sync" (generic;
no reader-economy axis named). Concrete assessor PASS example: "beyond scope,
`auth.md` explains the token flow in three places and buries the one fact
you'd come here for — a busy dev would bail." Concrete writer FAIL example: a
brief that restates every step before answering. Concrete writer PASS example:
a close-out that states the outcome first, then the detail, once.

## Defects / observations
```

- [ ] **Step 2: Verify**

Read the rubric file. Confirm: the retained Functional / Voice / WHAT-summary blocks are byte-unchanged; the new Reader-experience section sits between the WHAT-summary examples and `## Defects / observations`; it carries concrete assessor + writer pass/fail exemplars; it explicitly states it is not a writer gate and is orthogonal to scope. Fix inline if not.

---

## Task 4: Propagate the value in-voice into the skills

Additive, one positive craftsmanship clause per edit. Codocu register only.

- [ ] **Step 1: Shared house-rule line — all six skills that carry it**

In **each** of these files, find this exact line (identical in all six):

```
_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

Replace with:

```
_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics. Write every doc, plan, and brief for a perpetually busy reader — lead with the answer, say each thing once, cut whatever restates the code; they should come away "I get it," not "what a mess."_
```

Apply to all of:
- `skills/codocu/SKILL.md`
- `skills/fold/SKILL.md`
- `skills/propose/SKILL.md`
- `skills/code-doc/SKILL.md`
- `skills/doc-code/SKILL.md`
- `skills/apply/SKILL.md`

(Do **not** edit `skills/init/SKILL.md` or `skills/sync/SKILL.md` — relays, no house-rule line; they inherit through `/codocu` and `/codocu:fold`.)

- [ ] **Step 2: Verify Step 1**

Grep the six files for `perpetually busy reader`: exactly one hit per file, inside the existing italic house-rule block. Confirm `init`/`sync` have zero hits. Confirm no file's other content changed. Fix inline if not.

- [ ] **Step 3: `skills/propose/SKILL.md` — plan-for-a-reviewer clause**

Find this exact block:

```
Steps should be concrete and granular. Each step should be completable in one
focused action. Prefer too many small steps over too few large ones.
```

Replace with:

```
Steps should be concrete and granular. Each step should be completable in one
focused action. Prefer too many small steps over too few large ones. Write the
plan for a busy reviewer — a plan no one will read doesn't get reviewed: goal
and steps stated plainly, no padding, no restating the obvious.
```

- [ ] **Step 4: `skills/doc-code/SKILL.md` — plan-for-a-reviewer clause**

Find this exact block:

```
Write a plan to `docs/plans/YYYY-MM-DD-{topic}.md` describing the code changes
needed to implement what the docs describe.
```

Replace with:

```
Write a plan to `docs/plans/YYYY-MM-DD-{topic}.md` describing the code changes
needed to implement what the docs describe. Write it for a busy reviewer — an
obtuse plan goes unreviewed: goal and steps stated plainly, no padding.
```

- [ ] **Step 5: `skills/code-doc/SKILL.md` — small-scope path companion clause**

Find this exact sentence fragment:

```
bounded so nothing an internal-only refactor would falsify lands in it; that detail is the code's job. On top of that, apply the ActualDoc WHY heuristic
```

Replace with:

```
bounded so nothing an internal-only refactor would falsify lands in it; that detail is the code's job. Separately from scope, whatever you write reads for a busy person — lead with the answer, say it once, no padding; staying in scope is not the same as being worth reading. On top of that, apply the ActualDoc WHY heuristic
```

- [ ] **Step 6: `skills/code-doc/SKILL.md` — brownfield path companion clause**

Find this exact block:

```
Each doc opens with a coarse orientation map — purpose, place in the system,
public contract, direction — bounded so nothing an internal-only refactor
would falsify lands in it; the WHY heuristic governs what rationale earns a
line on top of that.
```

Replace with:

```
Each doc opens with a coarse orientation map — purpose, place in the system,
public contract, direction — bounded so nothing an internal-only refactor
would falsify lands in it; the WHY heuristic governs what rationale earns a
line on top of that. Separately, every doc reads for a busy person — lead with
the answer, say it once, no padding.
```

- [ ] **Step 7: `skills/fold/SKILL.md` — "Bring the docs along" clause**

Find this exact sentence:

```
refactor would falsify; that detail is the code's job. Keep that opening
honest as you go.
```

Replace with:

```
refactor would falsify; that detail is the code's job. Keep that opening
honest as you go — and readable: a doc a busy person abandons half-read has
failed, however accurate.
```

- [ ] **Step 8: `skills/codocu/SKILL.md` — orientation brief bullet**

Find this exact bullet:

```
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete, and whether the long-term docs read as a coarse orientation map or
  drift over the bound (re-telling code internals) or under it (no orientation
  map at all);
```

Replace with:

```
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete, whether the long-term docs read as a coarse orientation map or
  drift over the bound (re-telling code internals) or under it (no orientation
  map at all), and — a separate axis — whether they're a kind read or
  something a busy developer would abandon: redundant, duplicated, the answer
  buried;
```

- [ ] **Step 9: `skills/codocu/references/deep-drill.md` — anchor 1**

Find this exact block:

```
   plans. Also judge the doc itself against the WHAT-summary bound: a doc that
   re-tells code internals is over the bound; one with no coarse orientation
   map (purpose, place, public contract, direction) is under it — report
   either as a distinct divergence.
```

Replace with:

```
   plans. Also judge the doc itself against the WHAT-summary bound: a doc that
   re-tells code internals is over the bound; one with no coarse orientation
   map (purpose, place, public contract, direction) is under it — report
   either as a distinct divergence. Separately from scope, judge the read: a
   doc a busy developer would abandon — redundant, duplicated, the answer
   buried — is its own distinct divergence, not folded into the scope finding.
```

- [ ] **Step 10: Verify all of Task 4**

Read each modified file around its edit. Confirm for every edit: it is one positive in-voice clause (no step numbers, no "per the skill", no recited checklist); sibling semantics are untouched (`code-doc` WHY four-conditions and sync-state lines; `fold` unconditional-Synced + no-trust-checkboxes; `codocu` read-only orientation + deep-drill gate; `deep-drill` read-only contract + tier table + field-rename check); reader-economy is presented as a **distinct axis** from the WHAT-summary scope bound everywhere, never merged into it. Fix inline if not.

---

## Task 5: Record the combined-run validation hook + locked-constraint guard

No inline `claude` run — validation is the deferred combined Spec-A+B+C run. This task records what that run must additionally check and guards the locked constraints.

**Files:**
- Modify: `docs/todo.md` (the combined-run block)

- [ ] **Step 1: Note the third validation dimension on the combined run**

Read `docs/todo.md`. In the "Specs A + B" block (the bullet beginning "ONE combined harness run validates both"), extend it so the combined run also scores the Reader-experience dimension from `report-template-whatsummary.md`: baseline (last commit before the combined commit) must show current skills neither flag reader-economy defects in the fixture docs nor produce reader-economical output; post-propagation run must show both, with voice non-regression. Rename the block from "Specs A + B" to "Specs A + B + C (reader economy)" and add this unit's spec/plan paths next to A's and B's. Keep the existing A/B text intact; this is an additive edit in the file's existing terse style.

- [ ] **Step 2: Tick the `docs/todo.md` "Apply Varya's prompt" line as planned**

Find the line `**Apply Varya's prompt**` under `## V1 todos`. Replace it with `**Apply Varya's prompt** — spec + plan written (`docs/superpowers/specs/2026-05-17-codocu-reader-economy-design.md`, `docs/superpowers/plans/2026-05-17-codocu-reader-economy.md`); implemented in-tree, unverified/uncommitted, folded into the combined A+B+C run + separable commit.` Keep it terse, matching surrounding entries.

- [ ] **Step 3: No-regression / locked-constraint guard**

Manually inspect the final files; record PASS/FAIL with file:line evidence (in this plan's Self-Review note or a scratch note — not committed):
1. `2026-05-14-codocu-design.md` — seven Principles; the six originals byte-unchanged; new bullet states orthogonality.
2. `docs/tuning.md` — five dials; four originals byte-unchanged; expressed-in list exactly matches Task 4's surfaces.
3. Six skill house-rule lines identical and each carrying exactly one appended reader-economy clause; `init`/`sync` untouched.
4. `code-doc`/`fold`/`codocu`/`deep-drill` sibling semantics (WHY conditions, unconditional-Synced, no-trust-checkboxes, read-only orientation, deep-drill gate, tier table, field-rename check) all intact.
5. No edits to `templates/codocu.md`, Spec A/B unfolded artifacts, or any file outside this plan's scope.
Any FAIL → fix the offending file and re-verify.

---

## Task 6: Final commit (ONLY when the user explicitly asks)

Per `CLAUDE.md`, this is the single commit for the whole "Apply Varya's prompt" logical unit, separable from the Spec A and Spec B units. **Do not run this task until the user explicitly asks to commit.**

**Files:**
- (commit only; no new edits)

- [ ] **Step 1: Confirm scope, then commit once**

Stage exactly this unit's deliverables: `docs/superpowers/specs/2026-05-17-codocu-reader-economy-design.md`, `docs/superpowers/plans/2026-05-17-codocu-reader-economy.md`, `docs/superpowers/specs/2026-05-14-codocu-design.md` (Task 1), `docs/tuning.md` (Task 2), `testing/2026-05-17-longterm-doc-style/report-template-whatsummary.md` (Task 3), `skills/codocu/SKILL.md`, `skills/fold/SKILL.md`, `skills/propose/SKILL.md`, `skills/code-doc/SKILL.md`, `skills/doc-code/SKILL.md`, `skills/apply/SKILL.md`, `skills/codocu/references/deep-drill.md` (Task 4), `docs/todo.md` (Task 5). Do **not** stage Spec A/B unfolded artifacts or any out-of-scope file. Commit with a message summarizing "Reader economy ('Apply Varya's prompt'): Principle + tuning dial + in-voice skill propagation + rubric row". Use the repo's commit trailer convention (`Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`). Do not push unless asked. Suggest `/codocu:fold` afterward to archive this plan.

---

## Self-Review

**1. Spec coverage:**
- Anchor / Principle (spec §Design 1) → Task 1.
- Fifth `docs/tuning.md` dial (spec §Design 2, decision 3) → Task 2.
- Test-rubric row, test-first, holistic, not a writer gate (spec §Validation, decision 2B/4) → Task 3.
- In-voice propagation surface — shared house-rule line + propose/doc-code + code-doc/fold + codocu/deep-drill (spec §Design 3, decisions 1, 2A, 5) → Task 4 (steps 1–9), distinctness-from-scope asserted in Step 10.
- Deferred combined validation, separable logical unit, contamination guard (spec §Validation, §Open items) → Task 5 + COMMIT/VALIDATION/IN-VOICE banners + Task 6.
- Scope boundaries / non-goals (spec §Design 5) → Out-of-scope banner + Task 5 Step 3 item 5.
- All covered; no gaps.

**2. Placeholder scan:** No "TBD/TODO/implement later". Every find/replace block is given verbatim from the on-disk files read this session. `<target-repo>`/`<git-sha>` inside the rubric block are pre-existing documented harness conventions, not new placeholders. No "similar to Task N".

**3. Type/string consistency:** The house-rule replacement string is byte-identical across all six Task 4 Step 1 files (verified identical in source). The phrase "Separately from scope" / "Separately" and "a busy person/developer would abandon" recur consistently across code-doc, fold, codocu, deep-drill. The dial's "Expressed in" list (Task 2) names exactly the surfaces edited in Task 4 — six house-rule files + propose + doc-code + code-doc + fold + codocu + deep-drill + the rubric — no more, no less. Principle count (6→7) and dial count (4→5) are stated consistently in Tasks 1, 2 and their verifies and Task 5 Step 3.
