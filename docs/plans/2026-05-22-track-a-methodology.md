# Track A — Methodology Re-founding — Implementation Plan

> **For the worker:** This is documentation work, not code. There is no test
> suite. Each task's gate is the `CLAUDE.md` **reader test** ("where would the
> intended reader get lost or bored? — named and fixed") plus the named
> methodology check. Steps use `- [ ]` for completion tracking. **Do not
> commit** — commits are the owner's, done manually at the end of the unit.

**Goal:** Re-found Codocu's design docs on the new core — *"Code is the spec;
aux docs are the complement"* — in plain English, written as clean injectable
units (single source of truth for the future `/build` pipeline).

**Approach:** Rewrite `principles.md`, `doc-standard.md`, and `voice.md`; align
`codocu.md` and `CLAUDE.md`. The Neph methodology (`docs/inbox/neph_doc_principles/`)
and the archived v1 reference (`docs/archive/skills_v1/codocu/references/doc-standard.md`)
are the source material to distill — not to paste. Re-derive in plain words;
never launder dense prose through.

**Outline this implements:** `docs/plans/2026-05-22-v0.2-plan.md` (Track A + B7).

## Status (2026-05-22) — owner-reviewed and revised

Drafted inline, then revised by the owner. Final outcome:

- **A1 — `principles.md`** ✅ landed (owner-revised): three principles —
  *Clarity is the point* / *Code is exhaustive about what is; docs cover the
  negative space* / *Code and docs must not repeat themselves*. Priority
  ordering added; "spec" dropped for "exhaustive about what is". Tool-agnostic
  moved out to `README.md` (a manifesto claim, not a how-to-write rule).
- **A2 — "auxiliary docs" term** ✅ landed as a **Dictionary** in
  `doc-standard.md` (Auxiliary / Internal / Long-term / Short-term / Delta / ADR).
- **A3 — `doc-standard.md`** ✅ landed (owner-revised): Dictionary + five rules.
- **A4 — Neph edges & mechanics** ◑ resolved by descoping. Kept: the co-change
  rule and the "an ADR may name code" clause. Rehomed out of the base docs:
  the **elevation pass** → reviewer-subagent todo; **`#METADOCU`** → separate
  learning skill + Neph metadocu-pass todo; the **"roads not taken" ADR detail**
  → fresh-repo doc templates.
- **A5 — summaries rule** ✅ landed as rule 4 (meaning, not symbols).
- **B7 — `voice.md`** ⏸ parked, pending the METADOCU / learning-skill work.
- Alignment (`codocu.md`, `CLAUDE.md`) ✅ landed.

Reader-test gate = owner's cold read (done). Files: `docs/design/principles.md`,
`docs/design/doc-standard.md`, `codocu.md`, `CLAUDE.md`. (`voice.md` untouched.)

---

## File map

- `docs/design/principles.md` — Modify: 3 core beliefs, persona removed, flow framing dropped.
- `docs/design/voice.md` — Modify: plain-English rewrite, receives the persona.
- `docs/design/doc-standard.md` — Modify: becomes the single injectable rules doc (rules + resolved edges + folded mechanics).
- `codocu.md` — Modify: "auxiliary docs" vocabulary, design-doc list, drop the archived-reference pointer.
- `CLAUDE.md` — Modify: align §First principle wording and the design-doc list with the new core.
- `docs/plans/2026-05-22-v0.2-plan.md` — Modify: check off Track A items as done.

---

## Task 1: Rewrite `principles.md` on the new core

**Files:**
- Modify: `docs/design/principles.md`
- Modify: `docs/design/voice.md` (persona lands here; full rewrite is Task 5)

- [ ] **Step 1: Write the three beliefs.** Replace the four current principles with three, plain English:
  - *Clarity is the point* — the reader has to come away understanding; accuracy serves that, never the reverse.
  - *Code is the spec; aux docs are the complement* — use this core verbatim as the anchor: "Code is a first-class spec — it precisely describes how the product works *right now* (the complete spec). Auxiliary docs carry what code can't: why it's built this way, where it's headed, the changes planned as deltas, the cross-file picture. An aux doc never re-states what the code already spells out."
  - *Tool-agnostic* — no built-in knowledge of any spec/proposal format; works on whatever conventions a repo owns.
- [ ] **Step 2: Move the persona out.** Cut the "The agent is a senior partner" principle and paste its substance into `voice.md` (don't lose it — Task 5 reworks it there).
- [ ] **Step 3: Drop flow framing.** Remove the "every flow honors these" framing and any reference to the rigid flow model. Update the design-doc cross-reference list to `principles / voice / doc-standard` (flows.md is slated for archive in Track B — do not list it as a current peer; a one-line "flow overlays are optional, see Track B" note is fine).
- [ ] **Step 4: Reader-test gate.** Read it cold as a tired reader. Name the one spot where attention drops; fix it. Confirm no sentence just restates what the code/other docs already say.
- [ ] **Step 5:** Mark this task complete.

## Task 2: Establish "auxiliary docs" as a first-class term

**Files:**
- Modify: `docs/design/principles.md` (the core belief already introduces it)
- Modify: `codocu.md` (vocabulary used in structure description)

- [ ] **Step 1: Write the definition once, where it's load-bearing.** In `principles.md`'s core belief, define it crisply: *auxiliary docs = everything outside code (the `.md` files, etc.); they carry why / direction / deltas / the cross-file picture, and never reword the code.* Both long-term docs and plans are auxiliary.
- [ ] **Step 2: Use the term consistently.** In `codocu.md`, replace ad-hoc phrasings ("docs", "long-term docs") with "auxiliary docs" where the new term is meant, so the vocabulary is single-sourced. Do not redefine it in `codocu.md` — point at the principle.
- [ ] **Step 3: Reader-test gate.** Confirm a newcomer meets the term once, clearly defined, and never a second conflicting definition.
- [ ] **Step 4:** Mark this task complete.

## Task 3: Rewrite `doc-standard.md` as the single injectable rules doc

This collapses the old split (design rationale here / operational rule in the
skill reference). With design docs as the single source of truth, `doc-standard.md`
becomes the one injectable unit the future skill projects from.

**Files:**
- Modify: `docs/design/doc-standard.md`
- Source to distill: `docs/inbox/neph_doc_principles/methodology.md`, `review-checklist.md`; `docs/archive/skills_v1/codocu/references/doc-standard.md`

- [ ] **Step 1: Open with the core link.** One short paragraph: every rule below grows from the core ("code is the spec; aux docs complement it"); the rules are how that core is honored when writing.
- [ ] **Step 2: Write the rules, each plain and standalone:**
  - *A doc is tied to what it describes* — placement by anchor scope (one symbol → docstring; one module → module/file header; a system/flow → a system doc; the whole repo → generated). Plus the breadcrumb: a doc that points at code gets a back-pointer in the load-bearing file, so the next editor sees it.
  - *Reference discipline* — name a concept only if it co-changes with the doc **or** a backlink guarantees the doc loads when it changes. Distance no longer governs naming; co-change + reachability does.
  - *Summaries survive meaning-preserving refactors* — a summary describes the meaning it governs, not the exact symbols; a rename leaves it true. (Detailed in Task 4.)
  - *Prefer business words over code words* — when both name the same thing, the business handle is richer and more refactor-stable.
  - *Say only what code can't* — the negative space: why the subsystem exists, roads not taken (ADRs), deliberate non-goals, the cross-module flow, conventions no type system enforces, in-flight refactors. Run the field test before each sentence: *"Could this be a test assertion?"* If yes → push down a tier or delete.
- [ ] **Step 3: Resolve the two flagged edges** (the methodology's "CODOCU v0.2 TODO REMARK"):
  - *ADRs may name specific code* — justified because the decision is *about* that code; the backlink keeps them co-changing.
  - *Business summaries may refuse code names even when close* — proximity does not license code-naming; the stable business handle wins.
  - State both as the *reference-discipline rule firing*, not as exceptions to a distance rule.
- [ ] **Step 4: Fold in the mechanics**, distilled (not pasted) from the Neph methodology: the tier model, the breadcrumb line convention (`System doc: <path>`, grep-friendly), and `#METADOCU` as **fixture-only** (training labels written only in the reference corpus, never downstream). Keep these operational and short.
- [ ] **Step 5: Elevation pass.** For each block, ask: could this be one tier down, generated (Outside tier), or deleted? Default keep — but only after asking.
- [ ] **Step 6: Reader-test gate.** Read cold; name the spot a tired reader stalls; fix. Confirm no internal-symbol transcription crept into the doc's own prose.
- [ ] **Step 7:** Mark this task complete.

## Task 4: Make the docstring / code-summary standard concrete (A5)

**Files:**
- Modify: `docs/design/doc-standard.md` (a focused subsection under the summaries rule)

- [ ] **Step 1: State what a good code summary names vs. avoids.** Names: the meaning/contract it governs, stable public surfaces. Avoids: transcribing exact symbol names that a meaning-preserving refactor would rename, and restating mechanics the code shows.
- [ ] **Step 2: Add one do/don't pair** (concrete, from the todo's own example): not *"this thing is a StrEnum"* (transcribes the type, drifts on refactor) but *"an enum chosen for constant safety and discoverability"* (states the meaning, survives the rename).
- [ ] **Step 3: Make the refactor-resistance test explicit:** *"If a variable/type here were renamed without changing behavior, would this summary still read true?"* If no, it's transcribing — rewrite to the meaning.
- [ ] **Step 4: Reader-test gate.** Confirm the rule is usable by someone writing a docstring right now, not just admirable.
- [ ] **Step 5:** Mark this task complete.

## Task 5: Rewrite `voice.md` in plain English (B7, pulled forward)

**Files:**
- Modify: `docs/design/voice.md`

- [ ] **Step 1: Plain-English rewrite.** Keep the persona (senior co-owner, mentor, partner — not a procedure executor) and the house rule (talk about the project and the next move, never the skill's own mechanics; write for a busy, tired reader; lead with the answer, say it once, cut what restates the code). Strip dense phrasing.
- [ ] **Step 2: Absorb the persona moved from `principles.md`** (Task 1, Step 2) so it lives here cleanly, not duplicated.
- [ ] **Step 3: Resolve the open TODOs in the file** — either seed one concrete voice example pair (dense vs. preferable, like the methodology's Pair 1) or mark the multishot-seeding work explicitly as a Track B/C dependency. Don't leave a bare "TODO: this isnt enough".
- [ ] **Step 4: Write as an injectable unit** — self-contained, no dependence on flow framing or deleted skills.
- [ ] **Step 5: Reader-test gate.** Read cold; fix the stall point.
- [ ] **Step 6:** Mark this task complete.

## Task 6: Consistency + cross-reference pass

**Files:**
- Modify: `codocu.md`, `CLAUDE.md`
- Modify: `docs/plans/2026-05-22-v0.2-plan.md`

- [ ] **Step 1: Align `CLAUDE.md`.** Update §First principle and the "Design" list so the wording matches the new core and the `principles / voice / doc-standard` set. Don't list `flows.md` as a current authority (archived in Track B).
- [ ] **Step 2: Align `codocu.md`.** Fix the design-doc description, drop the dead pointer to `skills/codocu/references/doc-standard.md` (the split is gone), and remove references to the deleted `propose`/`apply`/`doc-code` skills in the structure section (or mark them as Track B removals, consistent with the outline).
- [ ] **Step 3: Vocabulary sweep.** Confirm "auxiliary docs", the core sentence, and the rule names read the same across `principles.md`, `doc-standard.md`, `voice.md`, `codocu.md`, `CLAUDE.md`. A term defined one way in one file and another way elsewhere is a defect — fix it.
- [ ] **Step 4: Check off Track A** in `docs/plans/2026-05-22-v0.2-plan.md` (A1–A5 + B7) with a one-line status each.
- [ ] **Step 5: Final reader-test gate** across all changed docs, read in the order a newcomer would: principles → voice → doc-standard. Name the one weakest transition; fix it.
- [ ] **Step 6:** Mark this task complete. Hand back to owner for review and commit.

---

## Self-review (against the outline)

- **A1** → Task 1. **A2** → Task 2. **A3** → Task 3. **A4** → Task 3 (Steps 3–4).
  **A5** → Task 4. **B7** → Task 5. Cross-cutting "injectable units" → enforced
  per task; "single source of truth" → Task 3 collapses the rationale/operational split.
- No code placeholders (no code in this plan by design). The target prose for the
  core, the rules, and the docstring example is stated concretely, not deferred.
- Vocabulary consistency is its own task (Task 6, Step 3), since drift across five
  files is the most likely defect.
