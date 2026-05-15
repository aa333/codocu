# Post-Research Spec & TODO Updates — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply seven actionable improvements to the design spec and TODO surfaced by the code-as-spec prior art research and critique session.

**Architecture:** Pure documentation edits to two files — `docs/superpowers/specs/2026-05-14-codocu-design.md` and `TODO.md`. No code changes. Tasks are independent and can be applied in any order, but are sequenced spec-first, then TODO.

**Tech Stack:** Markdown, git.

---

## Files

- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md` (Tasks 1–5)
- Modify: `TODO.md` (Tasks 6–7)

---

### Task 1: Spec — Add Target User & Scope section

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md`

- [ ] **Step 1: Insert new section after "What It Is"**

After the closing `---` of the "What It Is" section (after line 13), insert:

```markdown
## Target User & Scope

**Target user:** IT-first builders — solo developers, small technical teams, and technical entrepreneurs who want to ship maintainable software without drowning in process or doc overhead.

**Scope:** Codocu operates at the single-project TRD level. Its area of responsibility is keeping a project's WHAT WAS / WHAT IS / WHAT WILL BE / WHY documented and coherent with its code.

**Out of scope:** System-of-systems architecture, cross-team API contracts, OpenAPI specs, stakeholder PRDs, and infrastructure specifications. These may reference or be referenced by Codocu docs, but Codocu does not manage them.

---
```

- [ ] **Step 2: Review the section in context**

Read the top of the spec and confirm the new section reads naturally between "What It Is" and "Principles." Check that "WHAT WAS / WHAT IS / WHAT WILL BE / WHY" matches the language used elsewhere in the file.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-codocu-design.md
git commit -m "docs: add target user and scope section to design spec"
```

---

### Task 2: Spec — Add Literature Acknowledgements section

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md`

- [ ] **Step 1: Insert new section at the end of the spec (after Folder Structure)**

Append to the end of `docs/superpowers/specs/2026-05-14-codocu-design.md`:

```markdown

---

## Prior Art & Influences

Codocu builds on established ideas — it does not claim to invent code-centric documentation:

- **Literate Programming (Knuth, 1984):** The original attempt to unify code and prose. Codocu draws the opposite lesson: prose woven into code is too high-friction; instead, code stands alone and prose *supplements* it.
- **Living Documentation (Cyrille Martraire, 2019):** The closest intellectual predecessor. Martraire's argument that documentation should evolve at the same pace as code, using the system itself as the primary knowledge source, directly informs Codocu's ActualDoc model.
- **BDD / Executable Specifications (Cucumber, SpecFlow, ~2006–present):** Treats tests as the living spec. Codocu is composable with BDD/TDD — tests are the machine-verifiable layer of the code-as-spec, not a competing approach.
- **OpenSpec (2024):** Direct workflow inspiration. Codocu adopts OpenSpec's propose→apply→archive lifecycle and reduces friction when switching between the two. Core divergence: OpenSpec treats code as a side-effect of specs; Codocu treats code as a co-equal source of truth.
- **Spec-Driven Development (SDD, 2024–2025):** The broader category Codocu belongs to, now represented by Kiro (AWS), GitHub Spec Kit, BMAD, and others. Codocu's differentiator is lightweight bidirectional sync for small teams, not enterprise-grade structured artifact management.
```

- [ ] **Step 2: Review**

Read the section and confirm all citations are accurate and the framing ("draws the opposite lesson," "composable," "direct workflow inspiration") matches the project's actual position on each.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-codocu-design.md
git commit -m "docs: add prior art and influences section to design spec"
```

---

### Task 3: Spec — Add ActualDocs WHY heuristic

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md`

- [ ] **Step 1: Locate the ActualDoc artifact description**

Find the ActualDoc entry under `## Artifacts > Long-term`. It currently reads:

```markdown
**ActualDoc**
- Evergreen project documentation. Might be per-module, might be per-slice or per-system, or even hybrid - users define that in codocu.md. 
- Default location: `docs/actual/entityA.md`. Decomposable to `docs/actual/entityA/` for large modules.
- Answers: in short, what is this? why is it like that? where is it going?
```

- [ ] **Step 2: Add the WHY heuristic**

Replace the ActualDoc block with:

```markdown
**ActualDoc**
- Evergreen project documentation. Might be per-module, might be per-slice or per-system, or even hybrid - users define that in codocu.md.
- Default location: `docs/actual/entityA.md`. Decomposable to `docs/actual/entityA/` for large modules.
- Answers: in short, what is this? why is it like that? where is it going?
- **What belongs here (not in code):** A decision, constraint, or design choice must be documented in ActualDoc if any of the following is true: (1) the reason is non-obvious from reading the code; (2) an alternative was considered and rejected; (3) an external constraint (regulatory, performance, organizational) drove the design; (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself.
```

- [ ] **Step 3: Review**

Read the full Artifacts section and confirm the heuristic is clear, not redundant with surrounding text, and doesn't contradict the "code is first-class" principle (it should reinforce it by defining exactly when docs are needed).

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-codocu-design.md
git commit -m "docs: add ActualDoc WHY heuristic to artifacts section"
```

---

### Task 4: Spec — Design the Sync State Marker (promote to V1)

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md`

- [ ] **Step 1: Add Sync State Marker subsection under Meta-doc**

Find `## Meta-doc: \`codocu.md\`` section. After the paragraph "The agent reads `codocu.md` at the start of every invocation...", insert:

```markdown
### Sync state marker

The first non-heading line of `codocu.md` is a reserved sync state marker:

```
> Codocu sync state: Synced
```

Valid values: `Synced`, `Desynced`, `Dirty`. Every command that changes sync state updates this line before finishing. This gives any new session an instant orientation without replaying git history or re-probing code.

**Update rules:**
- `:propose` / `:doc-code` / `:apply`: set to `Dirty` at start, `Synced` at successful fold.
- `:code-doc` (small delta): set to `Synced` on completion.
- `:code-doc` (large/brownfield): set to `Dirty` at plan creation, `Synced` at successful fold.
- `:fold`: set to `Synced` on completion.
- Bare `/codocu`: set to `Dirty` at start of resolution, `Synced` at successful fold.
- No command ever sets `Desynced` automatically — this value is set by the agent when it detects one side changed while the other is internally coherent, during state assessment at session start.
```

- [ ] **Step 2: Confirm the template already has the marker**

Open `templates/codocu.md`. Verify it already has `> Codocu sync state: Synced` as its second line. If not, add it.

- [ ] **Step 3: Review the update rules**

Re-read the States section (`Synced / Desynced / Dirty`) and confirm the update rules in the new subsection are consistent with those definitions. Pay attention to the `Desynced` rule — it should only be set by active assessment, never automatically.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-codocu-design.md templates/codocu.md
git commit -m "docs: design sync state marker, promote to V1"
```

---

### Task 5: Spec — Rename FOOBAR, reframe as nominal orientation flow

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-codocu-design.md`

- [ ] **Step 1: Find all FOOBAR references**

Search the spec for "FOOBAR". There are two: in the Commands table and in the Flows section header ("Case 4 — FOOBAR").

- [ ] **Step 2: Update the Commands table entry**

Change:

```markdown
| `/codocu` | Case 4 | FOOBAR / "I don't know what state I'm in." Read signals, ask per-area source-of-truth questions, produce a resolution plan before touching anything. |
```

To:

```markdown
| `/codocu` | Case 4 | **Orient** — nominal flow for dirty or unknown state. Read git signals and existing artifacts, show what changed on each side, ask per-area source-of-truth questions, produce a resolution plan before touching anything. Expected during active development; not a failure state. |
```

- [ ] **Step 3: Update the Flow section header and description**

Change:

```markdown
### Case 4 — FOOBAR (`/codocu`)
```

To:

```markdown
### Case 4 — Orient (`/codocu`)
```

- [ ] **Step 4: Review**

Read Cases 1–4 in sequence and confirm Case 4 now reads as a peer flow, not an exceptional one. Check that no other "FOOBAR" or failure-adjacent language remains.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-codocu-design.md
git commit -m "docs: rename FOOBAR to Orient, reframe as nominal dirty-state flow"
```

---

### Task 6: TODO — Promote sync state marker, add TDD hook item

**Files:**
- Modify: `TODO.md`

- [ ] **Step 1: Remove sync state marker from V1 todos (it's now in the spec)**

Find in `TODO.md`:

```markdown
**Sync state marker in `codocu.md`**
A short status line at the top of `codocu.md` showing current sync state (Synced / Desynced / Dirty) and a one-liner summary. Updated by commands as they run. Useful for quick orientation in a new session.
```

Delete this block entirely — it is now designed in the spec (Task 4) and will be implemented with the skills.

- [ ] **Step 2: Add TDD/test hook for :fold as a V1 item**

In the `## V1 todos` section, add after the `:fold` no-op item:

```markdown
**`:fold` test suite check**
Before archiving a plan, `:fold` should verify the test suite passes. If tests fail, block archiving and report which steps may be incomplete. Exact behavior on failure (warn-only vs. hard block) configurable in `codocu.md`. Implement and test against a real project before finalizing policy.
```

- [ ] **Step 3: Add ProposalSummary threshold item to V2/Future**

In the `## V2 / Future` section, add:

```markdown
**ProposalSummary persistence threshold**
ProposalSummary is intentionally ephemeral. If a session grows long before a Plan is written (e.g., extended back-and-forth on scope), consider writing it to disk automatically once a conversation length threshold is crossed. Assess during real use — most proposals resolve to a Plan within a short session.
```

- [ ] **Step 4: Review TODO structure**

Read the full TODO and confirm: V1 todos are actionable for the current implementation phase, V2/Future items are genuine deferments, and nothing in V1 duplicates what's now in the spec.

- [ ] **Step 5: Commit**

```bash
git add TODO.md
git commit -m "docs: update TODO — fold test hook to V1, proposal threshold to V2, sync marker removed (now in spec)"
```

---

### Task 7: TODO — Rename FOOBAR reference in TODO if present

**Files:**
- Modify: `TODO.md`

- [ ] **Step 1: Search for FOOBAR in TODO.md**

Scan TODO.md for any mention of "FOOBAR". If none exists, skip to Step 3.

- [ ] **Step 2: If found, update to "Orient"**

Replace any instance of "FOOBAR" with "Orient" or "orient" to match the spec rename from Task 5.

- [ ] **Step 3: Commit (only if changes were made)**

```bash
git add TODO.md
git commit -m "docs: update FOOBAR references to Orient in TODO"
```

---

## Self-Review

**Spec coverage check:**
- ✅ Target user & scope → Task 1
- ✅ Literature acknowledgements → Task 2
- ✅ ActualDocs WHY heuristic → Task 3
- ✅ Sync state marker design (V1) → Task 4
- ✅ FOOBAR rename → Task 5
- ✅ TDD/test hook for :fold → Task 6
- ✅ ProposalSummary threshold → Task 6
- ✅ FOOBAR in TODO → Task 7

**Placeholder scan:** No TBDs, no "implement later," no vague steps. Every step shows the exact text to insert or change.

**Consistency check:** "Orient" replaces "FOOBAR" in both the spec (Task 5) and TODO (Task 7). Sync state marker update rules in Task 4 align with State definitions in the spec. ActualDoc heuristic in Task 3 uses four numbered conditions — concrete enough to apply without judgment.
