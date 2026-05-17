# Codocu Design Spec

**Status:** approved  
**Date:** 2026-05-14

---

## What It Is

Codocu (COde-as-a-DOCUment) is an LLM agent workflow kit that keeps code, short-term plans, and long-term documentation coherent through an explicit lifecycle. Its core bet: well-written code is already the most detailed spec possible. Docs supplement it — they don't translate it.

Delivered as a Claude Code plugin (skills/commands), with the methodology spec as the design artifact. Other integrations (JetBrains, etc.) are future scope.

---

## Target User & Scope

**Target user:** IT-first builders — solo developers, small technical teams, and technical entrepreneurs who want to ship maintainable software without drowning in process or doc overhead.

**Scope:** Codocu operates at the single-project TRD level. Its area of responsibility is keeping a project's WHAT WAS / WHAT IS / WHAT WILL BE / WHY documented and coherent with its code.

**Out of scope:** System-of-systems architecture, cross-team API contracts, OpenAPI specs, stakeholder PRDs, and infrastructure specifications. These may reference or be referenced by Codocu docs, but Codocu does not manage them.

---

## Principles

- Code is first-class documentation. Compilation, unit tests, and integration tests are the machine-verifiable layer of that spec.
- LLM agents and experienced developers work better with focused, well-structured code than with bloated narrative docs. Both are agents — treat them accordingly.
- Detailed natural-language plans (TRDs) are fleeting. They live only as long as the work is active, then get folded into the permanent record.
- **Long-term docs open with a coarse, drift-resistant *what*-summary** — an orientation map (purpose, system role, public contract, key external deps, direction) that lets a senior *or a non-technical reader* get their bearings without reading code. Bounded by an invariant, not a length: nothing an internal-only refactor would falsify belongs in it — that detail is the code's job.
- **Beyond the summary, docs answer *why* and *where to*** — rationale and direction the code can't state for itself. Never a full re-telling of what the code already says.
- **Every doc, plan, and brief is written for a perpetually busy reader** — human or agent; attention is the scarcest resource. Lead with the answer, say each thing once, cut whatever restates the code or earns no decision. Orthogonal to the WHAT-summary bound: that governs *what content belongs*; this governs *whether it reads without exhausting the reader*. The defect is wasted attention, never length itself.
- Code and docs cross-link so that editing one nudges the agent toward updating the other.

---

## States

| State | Meaning |
|---|---|
| **Synced** | Code and long-term docs represent the same reality. Active plans may exist (future work is not a desync). Tests pass. |
| **Desynced** | One side changed, the other is internally coherent. Directional sync is possible once source of truth is established. |
| **Dirty** | Both sides in motion or contradictory. Iterative resolution with user input required. Normal during active development. |

**On plans and sync state:** if a plan states that feature X should be built and feature X is not yet in code, that is *Synced* — the plan accurately describes intended future work. Desync means the description of reality is wrong, not that work is incomplete.

---

## Artifacts

### Short-term (fixed structure — not configurable)

**ProposalSummary**
- Ephemeral. Lives in-conversation only; never written to disk unless explicitly asked.
- Contains: scope, affected areas, risks.
- Produced by `:propose`. Consumed when the Plan is written.
- `:doc-code` skips ProposalSummary entirely — the docs are the proposal.

**Plan**
- Written to `docs/plans/YYYY-MM-DD-topic.md`.
- Contains: context, goals, checkable implementation steps (`- [ ] step`).
- Created after ProposalSummary approval (or directly in `:doc-code`).
- Steps are checked off during implementation. `:fold` uses checkbox state + code probing to verify completion.
- Archived by `:fold` when complete.

### Long-term (conventions defined in `codocu.md`)

**ActualDoc**
- Evergreen project documentation. Might be per-module, might be per-slice or per-system, or even hybrid - users define that in codocu.md.
- Default location: `docs/actual/entityA.md`. Decomposable to `docs/actual/entityA/` for large modules.
- Answers, in three bounded parts: a **WHAT-summary**, then **WHY**, then a one-line **WHERE**.
- **The WHAT-summary (opens every ActualDoc).** A coarse orientation map of *what* the entity is, bounded by an invariant — not a word count.
  - **Names at most:** (1) the entity's purpose — what it is and the job it does; (2) its place in the system — what it talks to or depends on at the boundary; (3) its public contract — the capabilities/surface it offers consumers; (4) its direction — one line on where it's heading.
  - **Governing test (drift invariant):** if an internal-only refactor that leaves the public surface unchanged would falsify a sentence, that sentence is too detailed — cut it; the code is its home. A correct WHAT-summary stays correct as long as purpose and public contract are unchanged.
  - **Audience:** must read for a senior getting their bearings *and* a non-technical stakeholder — no per-function, per-field, algorithmic, or control-flow detail; no code unless a snippet *is* the contract.
- **WHY — what belongs here (not in code):** A decision, constraint, or design choice must be documented in ActualDoc if any of the following is true: (1) the reason is non-obvious from reading the code; (2) an alternative was considered and rejected; (3) an external constraint (regulatory, performance, organizational) drove the design; (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself.
- **WHERE:** one line on direction — where this entity is heading.

**ArchivedPlan**
- Completed plans moved to `docs/archive/`.
- Historical record. Not synced or maintained.

**(Optional) TechDebtRecord**
- Default: single catchall `docs/tech-debt-todo.md` with `TD-XXXX` codes.
- Codes are cross-linked with inline code `TODO`s so edits surface the record.
- Entirely specified by codocu.md. Example of advanced documentation flow. Tech debt documentation can be omitted entirely, stored in entity files, stored in code, routed to `docs/actual/improvements/`, this is just an example.

---

## Meta-doc: `codocu.md`

Free-form markdown at the project root. Pre-seeded by `/codocu:init` with opinionated defaults. User edits freely.

Defines for *this project*:
- Long-term doc locations and format expectations
- `:fold` behavior for incomplete plans (move to tech-debt, create new plan, always ask, skip, etc.)
- Additional flows, e.g. tech-debt records strategy (catchall file / per-module / in-code / etc)
- Any project-specific conventions the agent should follow

The agent reads `codocu.md` at the start of every invocation. `codocu.md` is **not subject to sync tracking** — it defines the rules, it doesn't follow them.

### Sync state marker

The first non-heading line of `codocu.md` is a reserved sync state marker:

```
> Codocu sync state: Synced
```

Valid values: `Synced`, `Desynced`, `Dirty`. `:init` seeds `TBD` in a fresh project (its real state is unknown until first assessed); the first command that establishes state replaces it. Every command that changes sync state updates this line before finishing. This gives any new session an instant orientation without replaying git history or re-probing code.

**Update rules:**
- `:propose` / `:doc-code` / `:apply`: set to `Dirty` at start, `Synced` at successful fold.
- `:code-doc` (small delta): set to `Synced` on completion.
- `:code-doc` (large/brownfield): set to `Dirty` at plan creation, `Synced` at successful fold.
- `:fold`: set to `Synced` on completion.
- Bare `/codocu`: set to `Dirty` at start of resolution, `Synced` at successful fold.
- No command ever sets `Desynced` automatically — this value is set by the agent when it detects one side changed while the other is internally coherent, during state assessment at session start.

Example fold config section (natural language — agent interprets):
```
## Fold settings
When folding incomplete plans, move unfinished items into tech-debt-todo.md by default. Always ask before archiving a plan with more than 3 incomplete steps.
```

---

## Commands

| Command | Entry case | Description |
|---|---|---|
| `/codocu:init` | — | Create `codocu.md` with defaults. Safe to re-run (won't overwrite). |
| `/codocu:propose` | Case 1 | Fresh intent → ProposalSummary → Plan → code → fold. Fast dirty-warn if uncommitted changes or active plans exist. |
| `/codocu:doc-code` | Case 2 | Docs describe desired state → Plan → implement in code → fold. ProposalSummary skipped. |
| `/codocu:code-doc` | Case 3 | Code is truth → update docs. Small delta: auto-update, no plan. Large / brownfield: ProposalSummary → Plan → write docs → fold. |
| `/codocu:apply` | — | Resume an existing plan (interrupted session, manually written plan). If multiple active plans: ask user which, offer "apply all in sequence". |
| `/codocu:fold` (alias: `/codocu:sync`) | — | Archive completed plans. Suggest (not auto-trigger) at end of any flow that produced a plan. |
| `/codocu` | Case 4 | **Orient** — nominal flow for dirty or unknown state. Read git signals and existing artifacts, show what changed on each side, ask per-area source-of-truth questions, produce a resolution plan before touching anything. Expected during active development; not a failure state. |

---

## Flows
Each step in general allows iterations and corrections

### Case 1 — Fresh intent (`/codocu:propose`)

```
user intent
  → [warn if dirty] 
  → ProposalSummary (ephemeral, user approves)
  → Plan written to docs/plans/
  → implement (code + plan steps checked off)
  → [fold suggested]
```

### Case 2 — Docs-first (`/codocu:doc-code`)

```
docs delta (already written)
  → Plan written (docs are the proposal, no ProposalSummary)
  → implement in code
  → [fold suggested]
```

### Case 3 — Code-first (`/codocu:code-doc`)

```
code delta
  → assess scope (agent judgment: files changed, doc coverage, area familiarity. In case of uncertainty - user consultation)
    → small: auto-update ActualDocs. Done. No fold needed.
    → large/brownfield: ProposalSummary (user approves) → doc Plan → write docs → [fold suggested]
```

### Case 4 — Orient (`/codocu`)

```
read signals (git hint if available, active plans, codocu.md)
  → show what changed on each side
  → ask user: which side wins per area?
  → resolution Plan
  → implement (code and/or docs per resolution)
  → [fold suggested]
```

---

## `:fold` in detail

`:fold` is a smart wrap-up command, not a simple archiver.

**Plan selection:** if one plan is active, fold it. If multiple: ask user which, offer "go through all plans."

**Per-plan process:**
1. **Sanity check** — read plan steps; probe code to verify claimed-done steps (`- [x]`) are actually implemented. Flag any that aren't.
2. **Completed plans** — confirm docs are updated (auto for small changes, diff+approve for large), then archive to `docs/archive/`.
3. **Incomplete plans** — offer to refactor: archive the original, produce a trimmed plan with only remaining work. Default behavior per `codocu.md` fold settings (move incomplete to tech-debt, create new plan, always ask).

**When it runs:** suggested by the agent at the end of any flow that produced a plan. Never auto-triggered. A future `/codocu:status` housekeeping command may incorporate a fold suggestion.

---

## Git as Advisory Signal

Git is a hint and a helper tool, not a direct router. When available:

| git diff shows | Suggestion |
|---|---|
| Only `.md` files uncommitted | Suggest `:doc-code` |
| Only code files uncommitted | Suggest `:code-doc` |
| Both changed | Suggest bare `/codocu` |
| Nothing | Suggest `:propose` (or `:apply` if active plan exists) |

No git in project → agent asks. User's explicit command always takes priority over any git-based suggestion.

---

## Folder Structure (defaults)

```
docs/
  actual/          # evergreen module docs
  plans/           # active short-term plans
  archive/         # completed plans
  tech-debt-todo.md # example of additional file
codocu.md          # meta-doc
```

All paths configurable via `codocu.md`.

---

## Prior Art & Influences

Codocu builds on established ideas — it does not claim to invent code-centric documentation:

- **Literate Programming (Knuth, 1984):** The original attempt to unify code and prose. Codocu draws the opposite lesson: prose woven into code is too high-friction; instead, code stands alone and prose *supplements* it.
- **Living Documentation (Cyrille Martraire, 2019):** The closest intellectual predecessor. Martraire's argument that documentation should evolve at the same pace as code, using the system itself as the primary knowledge source, directly informs Codocu's ActualDoc model.
- **BDD / Executable Specifications (Cucumber, SpecFlow, ~2006–present):** Treats tests as the living spec. Codocu is composable with BDD/TDD — tests are the machine-verifiable layer of the code-as-spec, not a competing approach.
- **OpenSpec (2024):** Direct workflow inspiration. Codocu adopts OpenSpec's propose→apply→archive lifecycle and reduces friction when switching between the two. Core divergence: OpenSpec treats code as a side-effect of specs; Codocu treats code as a co-equal source of truth.
- **Spec-Driven Development (SDD, 2024–2025):** The broader category Codocu belongs to, now represented by Kiro (AWS), GitHub Spec Kit, BMAD, and others. Codocu's differentiator is lightweight bidirectional sync for small teams, not enterprise-grade structured artifact management.
