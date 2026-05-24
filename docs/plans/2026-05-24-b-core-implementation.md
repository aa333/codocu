# B-core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build the v0.2 B-core skill (`/codocu`) and the `codocu-reviewer` subagent per the design spec, validate against the eval fixtures, and smoke-test the four canonical invocations on Codocu's own repo.

**Architecture:** One user-invokable skill (`skills/codocu/SKILL.md`) carrying the full corpus pack; one plugin-level subagent (`agents/codocu-reviewer.md`) for atomic per-doc review with a constrained rule pack (principles + smell catalog only). B-core composes 11 primitives per the user's ask; the reviewer is the only subagent it launches.

**Tech Stack:** Claude Code plugin (skills as markdown with frontmatter; agents as markdown with frontmatter); no runtime code. Validation runs through the existing eval fixtures in `docs/corpus/eval-fixtures.md`.

**Source spec:** `docs/plans/2026-05-24-b-core-design.md`.

**Commit policy:** Per project CLAUDE.md, commits are manual by the owner. Do not commit between tasks. The user will commit when the implementation is reviewed and stable.

---

## File Structure

- **Create:** `skills/codocu/SKILL.md` — the main skill body. Single file; full corpus pack loaded by instruction (the agent reads design + corpus assets at invocation via Read tool).
- **Create:** `agents/codocu-reviewer.md` — the atomic per-doc reviewer subagent. Frontmatter pins `model: sonnet`; body carries the structured output schema and the cataloged/uncataloged framing.
- **Modify:** `.claude-plugin/plugin.json` — description currently reflects v0.1 ("propose, implement, and fold changes through an explicit lifecycle"); rewrite for v0.2's doc-first framing.

Files referenced (not modified by this plan):
- `docs/design/principles.md`, `voice.md`, `doc-standard.md` — loaded by the skill at invocation.
- `docs/corpus/{principles,smell-catalog,voice-pairs,placement-rules,eval-fixtures}.md` — loaded by skill/agent at invocation; fixtures used for verification.

---

## Task 1: Plugin scaffold and metadata

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Create: `skills/codocu/` (directory)

- [x] **Step 1: Update `plugin.json` description to v0.2 framing**

The current description is v0.1: *"Keep code, plans, and docs coherent. Propose, implement, and fold changes through an explicit lifecycle."* Rewrite as:

```json
{
  "name": "codocu",
  "description": "Keep code and documentation coherent. A doc-first quality keeper that writes, reviews, and maintains the docs that complement your code.",
  "version": "0.2.0",
  "license": "MIT",
  "keywords": ["docs", "documentation", "quality", "workflow"]
}
```

Reason for change: "propose, implement, fold" was the v0.1 lifecycle vocabulary; v0.2 drops it. "doc-first quality keeper" matches the language in the v0.2 plan. Keywords trimmed to drop "spec" and "sync" (no longer central concepts).

- [x] **Step 2: Create the skill directory**

```
mkdir -p skills/codocu
```

Verify directory exists with `ls skills/`.

---

## Task 2: Write SKILL.md scaffold (frontmatter, anchor, loading)

**Files:**
- Create: `skills/codocu/SKILL.md`

- [x] **Step 1: Write SKILL.md frontmatter**

```markdown
---
name: codocu
description: Keep the repo's docs aligned with Codocu's standards — write new docs, fix existing ones, relocate misplaced content, remove transcription. Invoke when the user asks about doc quality, doc updates after code changes, doc-system planning, or verifying doc claims against current code.
---
```

The `name` matches the directory and is the `/codocu` invocation suffix per CLAUDE.md. The `description` states *when* to use the skill (per the project's skill-authoring conventions).

- [x] **Step 2: Add the voice anchor block**

Add immediately after the frontmatter (the verbatim house rule from `docs/design/voice.md`):

```markdown
> You own this project's code/doc coherence. Talk about the project and the next
> move — never about your own steps, defaults, modes, or mechanics. Write every
> doc, plan, and brief for a busy, tired reader: lead with the answer, say it
> once, cut anything that just restates the code.
```

Do not paraphrase this block. It is the persona contract for any Codocu skill.

- [x] **Step 3: Add the loading section**

```markdown
## On invocation, load

Before doing anything else, read these from the plugin's repo:

- `docs/design/principles.md` — the three core beliefs.
- `docs/design/doc-standard.md` — the rules for a good auxiliary doc.
- `docs/design/voice.md` — voice and tone (you've already absorbed the anchor above; this is the full spec).
- `docs/corpus/placement-rules.md` — where docs live and why.
- `docs/corpus/voice-pairs.md` — before/after examples for voice (dense → plain).
- `docs/corpus/smell-catalog.md` — named anti-patterns with fixes.

Then read the target repo's `codocu.md` if it exists. It carries the project's local conventions and overrides defaults.

If `codocu.md` does not exist, the repo is uninited. Stop and delegate to `/codocu:init` (see the Init primitive below).
```

- [x] **Step 4: Verify the file loads as a valid skill**

```
claude --plugin-dir . /reload-plugins
```

Expected output: should report 1 skill loaded (`codocu`). If the skill doesn't load, frontmatter is malformed — check name and description fields.

---

## Task 3: Write SKILL.md — the 11 primitives

**Files:**
- Modify: `skills/codocu/SKILL.md`

Add a new section `## Primitives` after the loading section. Each primitive gets a short subsection following this template — heading, one-line purpose, key constraints, and any relevant references.

- [x] **Step 1: Write the section preamble**

```markdown
## Primitives

These are the verbs you compose to do the user's task. They are not a flow — read the user's ask, choose which primitives the task needs, and order them by judgment. The four canonical invocations below show typical compositions; they are examples, not scripts.

Do not narrate the primitives back to the user. The user does not need to hear "running atomic review"; they need to hear what you found.
```

- [x] **Step 2: Write the `Map doc graph` primitive**

```markdown
### Map doc graph

Read the doc TOC and structure when the task needs cross-doc context. `codocu.md` is ambient — already loaded — so this primitive is about the wider graph: which docs exist, how they're cross-linked, what folders carry what kinds of doc.

Skip when the task scope is narrow (a named doc, a specific section). Use when the task scope is unclear or the work obviously touches multiple docs.
```

- [x] **Step 3: Write the `Discover scope` primitive**

```markdown
### Discover scope

Identify which docs the task touches. Three sources:

- **User-named.** The user pointed at one or more docs. Use as-is.
- **Change-inferred.** The task is change-driven ("code changed, update docs"). Run `git status` / `git diff` / `git log` to find the changeset, then map changed code files → docs that reference them (Grep for filenames and `System doc:` breadcrumbs back).
- **Task-scoped.** The task names a system or area but no specific docs ("the tech-debt records," "the access system"). Resolve via `codocu.md` and the doc graph.
```

- [x] **Step 4: Write the `Atomic review` primitive**

```markdown
### Atomic review

Launch the `codocu-reviewer` subagent against a single doc. The reviewer applies the smell catalog + principles and returns a structured report (verdict + hits + notes).

When multiple docs need review, launch reviewers concurrently — one Task call per doc, all in the same message. Each reviewer gets a clean context.

Read the reviewer's report and weigh it. The verdict (`good` / `needs-work` / `bad`) is the headline; the hits carry the actionable detail. Treat `[uncataloged]` hits as serious — the reviewer is grounding them by principle, not gut feel.
```

- [x] **Step 5: Write the `Compositional review` primitive**

```markdown
### Compositional review

Done in your own context, not delegated. Look for cross-doc issues:

- **Duplications.** The same fact stated in two docs; one is authoritative, the other is drift waiting to happen.
- **Dangling refs.** A doc points at another doc that moved or was deleted; a code file has a `System doc:` breadcrumb pointing nowhere.
- **Missing docs implied by the changes.** A new system without a doc; a fold that left a stray block unowned. (When you find one, route it through Place.)

Default scope is affected docs + immediate neighbors (docs cross-linked with the affected ones). Widen by running Map doc graph first when the task scope is unclear.
```

- [x] **Step 6: Write the `Place` primitive**

```markdown
### Place

Decide where a doc lives. Five options per `placement-rules.md`:

- **New doc.** A subsystem, flow, or convention with no single anchor needs its own system doc under `docs/`.
- **Fold into existing.** The content is about an existing documented system; absorb it into that system's doc.
- **Push down to docstring.** The content is about a single symbol or module — its docstring is the right home.
- **Breadcrumb-only.** The doc already exists; this code file just needs a `System doc:` breadcrumb pointing at it.
- **Absorb-then-delete.** The content is real but the doc carrying it shouldn't exist; move what stays, delete the rest.

Decide whether a breadcrumb is needed and which code file carries it. Surface required breadcrumb edits in the Report — you do not write code.
```

- [x] **Step 7: Write the `Write/edit` primitive**

```markdown
### Write/edit

Compose or modify doc content. References come in priority order:

1. **Local refs first.** Other good docs in this repo — drawn on for voice cues, placement patterns, and conventions the project already lives by.
2. **Shipped corpus samples.** When the repo has nothing to imitate, fall back to `placement-rules.md` and `voice-pairs.md`.

Apply principles (always) + voice (always) + placement (always). After writing, run atomic review on the result per the post-write heuristic.

You never write code. When a Place decision implies a code-side edit (breadcrumb, backlink), put it in the Report's code-edit list and stop there.
```

- [x] **Step 8: Write the `Delete/demote` primitive**

```markdown
### Delete/demote

Subtractive moves:

- Remove transcription — content that restates what the code already says.
- Push notes down to docstrings — content that belongs closer to its anchor.
- Archive superseded — dated specs that have been folded; move to `docs/archive/`.

Narrate intent before the destructive action: "I'm about to delete §3 of access.md and fold its rationale into chat-unions.md — the section is about a consumer, not the access system." Plan mode formalizes this gate; narration informalizes it.
```

- [x] **Step 9: Write the `Verify-against-code` primitive**

```markdown
### Verify-against-code

Mechanical Grep/Read against current code state. Does the path the doc names still exist? Does the symbol still exist? Does the doc's factual claim about code structure still hold?

Surface stale claims; do not speculate about *why* code drifted or whether the doc should now say something different — that's a Write/edit decision and may not need to happen at all.

v0.2 is mechanical only. Semantic verification (does the *behavior* the doc claims still match the code?) is out of scope.
```

- [x] **Step 10: Write the `Survey doc system` primitive**

```markdown
### Survey doc system

For meta-asks like "let's switch to a new doc system, I need a plan." Take the whole `docs/` tree as subject. Produce structured findings:

- What kinds of docs exist; how they're organized.
- What's working; what's not (stale, duplicated, misplaced, missing).
- What the user's proposed change would touch and why.

This primitive produces findings, not a plan doc. To produce a plan doc, hand the findings to Place + Write — the plan is itself a doc that needs to be placed and written.
```

- [x] **Step 11: Write the `Init` primitive**

```markdown
### Init

If `codocu.md` does not exist in the target repo, delegate to `/codocu:init`. Do not run init logic inline.

When the user invokes `/codocu` on an uninited repo, recommend running init first: "This repo isn't inited for Codocu yet. I'd run `/codocu:init` to scaffold the conventions, then come back to your ask. OK to do that now?"
```

- [x] **Step 12: Write the `Report` primitive**

```markdown
### Report

End with a report. Lead with the answer. Sections, in this order, omitting any that are empty:

- **What I found / did.** One or two sentences. The headline.
- **Doc edits applied.** Bulleted list of paths touched and what changed.
- **Required code-side edits.** Bulleted list of code files that need breadcrumbs, backlinks, or other edits to keep the docs whole. The user or a coding specialist applies these.
- **Recommendations.** Anything that needs the user's call — a doc that should be split, a system that should get its own doc, a record that should move.

Do not narrate machinery. Do not enumerate the primitives you ran. The user wants the result and what's next.
```

- [x] **Step 13: Verify the primitives section reads cleanly**

Re-read the full Primitives section. Check:
- Each primitive has exactly one job (per the spec).
- No vocabulary about v0.1 concepts (sync state, modes) appears anywhere.
- The voice matches `voice.md` — no narrating machinery, no menus.

If any primitive's body sounds like a procedure or a checklist back at the user, rewrite for voice.

---

## Task 4: Write SKILL.md — composition examples, heuristics, runtime boundaries

**Files:**
- Modify: `skills/codocu/SKILL.md`

- [x] **Step 1: Add the composition examples section**

```markdown
## Composing the primitives — typical patterns

These are illustrative, not prescriptive. Read the user's ask first, then choose.

**"Check if these docs are good quality."**
Discover scope → Atomic review (fan out per doc) → Compositional review (light, immediate neighbors only) → Report.

**"Let's switch to a new doc system, I need a plan."**
Survey doc system → Place + Write (the plan doc itself goes under `docs/plans/`) → Report.

**"Code changed, update docs."**
Discover scope (VCS-assisted) → Verify-against-code → Atomic review → Place + Write/edit (or Delete/demote if a section no longer applies) → Report (with required code-side edits like breadcrumbs).

**"Verify tech-debt records still match reality."**
Discover scope (the tech-debt doc) → Verify-against-code → Report (per-entry status).
```

- [x] **Step 2: Add the heuristics section**

```markdown
## Heuristics

- **Post-write atomic review.** Run it after a new doc, a major edit, or several compounded small edits in the same pass. Skip for isolated trivial edits (a typo, a single line).
- **Compositional review scope.** Affected docs + immediate neighbors by default. Widen by running Map doc graph first when the task scope is unclear.
- **VCS in Discover scope.** When the user's ask is change-driven, use `git status` / `git diff` / `git log` to define the changeset before mapping to docs.
- **Destructive actions narrate intent.** Before Delete/demote, state what's about to go and why. Plan mode catches it formally; narration catches it informally.
```

- [x] **Step 3: Add the runtime boundaries section**

```markdown
## Runtime boundaries

- **Do not write code.** When Place implies a breadcrumb or a code-side edit, surface the required edits in the Report. A coding specialist or the user applies them.
- **Do not run a propose/approve loop.** Claude Code's plan mode handles that. In normal mode write directly; in plan mode the writes are staged behind ExitPlanMode like any other tool.
```

Do not add a section like "What this skill does not know about." Per the design spec's implementer note: introducing vocabulary just to negate it is an anti-pattern. The skill simply doesn't carry v0.1 concepts (sync state, modes); it doesn't need to be told not to carry them.

- [x] **Step 4: Reload and verify the skill loads with the new content**

```
claude --plugin-dir . /reload-plugins
```

Expected: 1 skill loaded. Open SKILL.md, scan it end-to-end. Should be one coherent document — frontmatter, voice anchor, loading, primitives, composition, heuristics, runtime boundaries.

---

## Task 5: Write the `codocu-reviewer` subagent

**Files:**
- Create: `agents/codocu-reviewer.md`

- [x] **Step 1: Create the `agents/` directory if it doesn't exist**

```
mkdir -p agents
```

- [x] **Step 2: Write the agent frontmatter**

```markdown
---
name: codocu-reviewer
description: Atomic per-doc reviewer. Reads one doc and reports against the smell catalog and Codocu's principles. Use when reviewing the quality of a specific doc, never for cross-doc or compositional checks.
model: sonnet
tools: Read, Glob, Grep
---
```

`model: sonnet` per the corpus design — the catalog was extracted to be Sonnet-viable. Tools are bounded: read-only verification of references; no writes.

- [x] **Step 3: Write the agent's loading instructions**

```markdown
You are an atomic doc reviewer. You judge one doc against the standard. Compositional checks (cross-doc duplication, missing docs, dangling refs across the graph) are out of scope — those live in the main thread, not here.

## On invocation, load

Before reading the target doc:

- `docs/design/principles.md` from the plugin repo — the three core beliefs that define "good."
- `docs/corpus/smell-catalog.md` from the plugin repo — named patterns to check first.

Do not load `voice.md`, `voice-pairs.md`, or `placement-rules.md`. Those are writer tools; your job is judge, not writer.
```

- [x] **Step 4: Write the agent's review process**

```markdown
## How to review

1. Read the target doc.
2. Read the optional context line you were given (e.g., "focus on placement", "general check"). If none, treat as general.
3. Walk the smell catalog. For each smell, check whether the doc carries an instance. If yes, log a hit with the smell name, location, and the catalog's fix advice.
4. Walk the doc once more for clear quality issues outside the catalog. For each, log a hit marked `[uncataloged]`, name which principle is violated, and propose a fix in your own words. Do not speculate — if you can't name a principle violation, do not flag.
5. If a smell hit relies on a fact you can verify (a backlink target exists, a referenced path is real), use Read/Glob/Grep to check. Bounded checks only — do not browse the repo.
6. Produce the verdict and the structured report.
```

- [x] **Step 5: Write the output schema**

In the agent file, add a `## Output schema` section. Inside it, show the structure as plain text (no nested code fence — the agent file is markdown and an embedded fence reads as a block, not a literal template). Use four-backtick fences if you want it boxed; the simpler approach is plain text:

```
Output schema (write your output exactly in this shape; omit empty sections):

## Verdict
good | needs-work | bad

## Hits
### <smell-name> — <location-in-doc>
Why: <one sentence>
Fix: <one or two sentences>

### [uncataloged] — <location-in-doc>
Principle violated: <which one>
Why: <one sentence>
Fix: <one or two sentences>

## Notes
<free-form caveats — for example, "I couldn't reach a verdict on §3 because the referenced backlink target was missing from the repo">
```

Then add the verdict guide directly below:

```
Verdict guide:
- good — no hits; doc reads well against the standard.
- needs-work — one or more cataloged or uncataloged hits, but the doc's frame is right; targeted fixes will resolve.
- bad — multiple hits or a structural issue (wrong placement entirely, mass transcription); the doc needs to be redone, not patched.
```

- [x] **Step 6: Write the catalog framing**

```markdown
## Catalog is non-exhaustive

The smell catalog is a starting list — the named patterns we know how to fix. It is not the limit of what counts as bad. For any clear quality issue you see outside the catalog, mark it `[uncataloged]` and name which principle it violates.

Repeated `[uncataloged]` hits across reviews are how the catalog grows. Be specific about the principle so they're useful evidence later.
```

- [x] **Step 7: Reload and verify the agent loads**

```
claude --plugin-dir . /reload-plugins
```

Expected: reload reports 1 plugin, 1 skill, and 1+ agent loaded (the codocu-reviewer plus any others already in the plugin).

---

## Task 6: Run the atomic-review eval fixtures

**Files:**
- Read: `docs/corpus/eval-fixtures.md` for fixture content
- Test target: the `codocu-reviewer` subagent

The fixtures are the test suite. Each must-flag fixture has an expected smell name; each must-NOT-flag fixture must not be flagged. Compare actual reviewer output to expected.

- [x] **Step 1: Set up a temporary test doc for each must-flag fixture**

For each must-flag fixture, create a minimal markdown file containing the fixture's "Input" block, with a short context header so the reviewer has the same framing the corpus describes. Example for the first fixture:

```bash
mkdir -p testing/fixtures-run-2026-05-24
```

Then for `consumer-not-system / must-flag (block)`, create `testing/fixtures-run-2026-05-24/consumer-not-system-block.md`:

```markdown
# Access system

(stub system doc for fixture testing)

## Owner admin surface

The chat-settings Danger subtab is the in-app home for privileged operations
that used to require editing SQLite by hand. It is gated entirely on the global
`bot.system` cap … Three operations, each module-owned: Debug grant
(`POST /api/admin/economy/grant` …), Wipe balances (`POST /api/admin/economy/wipe`),
Wipe classes (`POST /api/admin/game_classes/wipe`). Both wipes resolve
`scope_id = UnionService.resolve_scope(chat_id)` once and delete inside one
`db.atomic()`; the confirm modal names the exact scope and requires the operator
to type it back verbatim …
```

Repeat for the remaining must-flag fixtures (5 more). Use the fixture's `Context:` line to decide what minimal scaffolding the test doc needs.

- [x] **Step 2: Invoke the reviewer against each must-flag fixture**

For each fixture file, launch the reviewer via the Task tool with `subagent_type: codocu-reviewer` (or via `/codocu` in atomic-review mode targeting the file). Pass the fixture file's path as input.

Expected output for `consumer-not-system / must-flag (block)`: the reviewer produces a hit named `consumer-not-system` referencing the "Owner admin surface" section, with a `needs-work` or `bad` verdict.

Repeat for each must-flag fixture. Tabulate pass/fail:

| Fixture | Expected smell | Reviewer flagged? | Pass |
|---|---|---|---|
| consumer-not-system / must-flag (block) | consumer-not-system | ? | ? |
| consumer-not-system / must-flag (ADR) | consumer-not-system | ? | ? |
| stray-todo-in-longterm-doc / must-flag | stray-todo-in-longterm-doc | ? | ? |
| unmaintainable-aggregation-list / must-flag | unmaintainable-aggregation-list | ? | ? |
| doc-far-from-anchor / must-flag | doc-far-from-anchor | ? | ? |
| summary-restates-signature / must-flag | summary-restates-signature | ? | ? |

- [x] **Step 3: Set up and invoke must-NOT-flag fixtures**

Same process: create a test file per fixture, invoke the reviewer, expect **no hits** for the smell that fixture exists to defend against. The reviewer may legitimately flag *other* things — that's fine — but it must not produce a hit that would describe the positive case as bad.

Fixtures to run (9 in total):
- system-doc-opening
- file-link-with-backlink
- name-public-surface
- adr-as-business-rationale
- single-class-module-title
- dev-usage-near-code-one-place
- document-the-negative-space
- docstring-by-nuance-not-appearance (trivial → none)
- docstring-by-nuance-not-appearance (trivial-looking → documented)

For each: pass if no hit asserts the fixture's correct content is wrong.

- [x] **Step 4: Diagnose failures and refine**

If any must-flag fixture didn't produce the expected smell:
- Re-read the smell entry in `smell-catalog.md` — is the trigger clear?
- Re-read the reviewer's instructions — does it walk the catalog or does it shortcut?
- The reviewer's instructions are in `agents/codocu-reviewer.md`. Adjust phrasing if the agent is skipping smells; do not over-fit (don't list every smell by name in the instructions).

If any must-NOT-flag fixture produced a false hit:
- The reviewer is being too aggressive. Re-read the relevant smell's trigger and tighten the agent's walking-the-catalog instructions (or move toward a more conservative "if uncertain, do not flag" stance).

After changes, reload (`/reload-plugins`) and re-run the affected fixtures.

- [x] **Step 5: Record a pass-rate baseline**

Write the results to `testing/fixtures-run-2026-05-24/results.md`:

```markdown
# Atomic review fixture run — 2026-05-24

## Must-flag (6 fixtures)
- consumer-not-system / block: PASS / FAIL
- consumer-not-system / ADR: PASS / FAIL
- stray-todo-in-longterm-doc: PASS / FAIL
- unmaintainable-aggregation-list: PASS / FAIL
- doc-far-from-anchor: PASS / FAIL
- summary-restates-signature: PASS / FAIL

## Must-NOT-flag (9 fixtures)
- system-doc-opening: PASS / FAIL
- file-link-with-backlink: PASS / FAIL
- ...

## Failures and follow-ups
<notes on what didn't pass and why>
```

Target: ≥80% pass on first run is a reasonable bar for v0.2 (the catalog is small, the model is bounded). Below that, the agent or the catalog needs work. Above that, ship and iterate.

---

## Task 7: Run the writer eval fixtures

**Files:**
- Read: `docs/corpus/eval-fixtures.md` for the must-produce fixtures
- Test target: the `/codocu` skill in write mode

Two must-produce fixtures exist:
- `too-technical → business-oriented`
- `internal-symbol+response-shape → public-surface`

Each gives a "before" block and an expected "after." The writer should produce something functionally equivalent to the after — drops implementation trivia, business-first, public surface named.

- [x] **Step 1: Set up the "before" docs**

For each must-produce fixture, create a test doc containing the before-text in the context the fixture describes. For `too-technical → business-oriented`, create `testing/fixtures-run-2026-05-24/writer-too-technical-before.md`:

```markdown
# Chat unions

(stub system doc for fixture testing)

## How it works

A union is a row with an auto-increment integer id, and a link row maps each chat into at most one union. … Everything is cached in-memory on startup.
```

- [x] **Step 2: Invoke /codocu to rewrite the "How it works" section**

Through Claude Code with the plugin loaded: invoke `/codocu` with a request like *"Rewrite the 'How it works' section of `testing/fixtures-run-2026-05-24/writer-too-technical-before.md` to match Codocu's voice."*

Expected output: the agent produces a rewrite that leads with what a union *is* (business), drops the trivia (row, auto-increment id, in-memory cache). Approximation target from the fixture:

> A union is a set of chats that share a user's stats across some features, primarily for the game layer.

Pass if the rewrite (a) leads with what a union is, (b) does not name the row/cache implementation. Exact wording doesn't matter.

- [x] **Step 3: Repeat for `internal-symbol+response-shape → public-surface`**

Before:

```
`UserApiConnector` returns `{user, capabilities, chats?}`. Each chat carries `capabilities`, `modules_enabled` …, and `member_status` (hierarchy status int 0–3, or null).
```

Expected approximation:

> The init user endpoint (`/api/init`) returns the user's bot-wide caps and a list of chats; each chat contains its own chat-wide caps.

Pass if the rewrite (a) names the public endpoint path, (b) drops `UserApiConnector` and the response-shape detail, (c) does not list every chat field.

- [x] **Step 4: Record writer-fixture results**

Append to `testing/fixtures-run-2026-05-24/results.md`:

```markdown
## Must-produce (2 fixtures)
- too-technical → business-oriented: PASS / FAIL — <one-line summary of what the writer produced and whether it lands>
- internal-symbol+response-shape → public-surface: PASS / FAIL — <same>
```

If failures: the writer is likely missing voice cues. Check that SKILL.md's loading instructions include `voice-pairs.md` and that the post-write atomic review heuristic triggered (a writer fixture that fails atomic review on its output is a useful signal to refine on).

---

## Task 8: Integration smoke test — the four canonical invocations

**Files:**
- Test target: `/codocu` end-to-end against the Codocu repo itself

Run each canonical invocation against this repo (the plugin's own repo, which has real docs). Check that the agent's behavior matches the spec's composition examples without devolving into mechanical narration.

- [x] **Step 1: Case 1 — "Check if these docs are good quality."**

Invocation: `/codocu check the quality of docs/design/principles.md and docs/design/voice.md`

Expected behavior:
- Loads codocu.md and the corpus pack (silently).
- Discovers scope (the two named docs).
- Launches the codocu-reviewer subagent against each, concurrently.
- Optionally does a light compositional check (these two docs cross-reference each other).
- Reports findings — verdict per doc, hits in plain language, no narration of the primitives.

Pass criteria: the agent produces a usable report; does not narrate "running atomic review"; calls out specific issues if any exist (or says cleanly that the docs are in good shape).

- [x] **Step 2: Case 2 — "Plan a migration."**

Invocation: `/codocu I'm thinking about renaming docs/corpus to docs/resources. Plan the migration.`

Expected behavior:
- Surveys the doc system (the agent should grep for references to `docs/corpus`, find all of them).
- Decides where the migration plan lives (likely `docs/plans/2026-05-24-corpus-rename.md` per the project convention).
- Writes the plan doc — listing affected files, the rename steps, what needs to update in SKILL.md/agent loading paths.
- Reports.

Pass criteria: produces a real migration plan doc (not a verbal summary in chat); plan lands in `docs/plans/`; lists references to update (including the skill and agent files this plan itself just created).

- [x] **Step 3: Case 3 — "Code changed, update docs."**

Invocation: `/codocu the last commit changed plugin.json and added skills/codocu/SKILL.md. Update any affected docs.`

Expected behavior:
- VCS-assisted scope discovery (`git diff HEAD~1 HEAD` or `git show HEAD`).
- Identifies docs that reference plugin.json or the skills layout (codocu.md, the v0.2 plan).
- Verifies-against-code (does codocu.md still describe the layout correctly?).
- Edits or notes that codocu.md may need an update reflecting the new skill.
- Reports.

Pass criteria: the agent reaches for git, doesn't ask the user "what changed?"; identifies at least codocu.md as a candidate; produces a coherent update or recommendation.

- [x] **Step 4: Case 4 — "Verify tech-debt records still match reality."**

Invocation: `/codocu verify the tech-debt records in docs/todo.md are still accurate.`

Expected behavior:
- Reads `docs/todo.md`.
- For each entry, Grep/Read against the current codebase to check whether the claim still holds (a referenced module exists, a noted limitation is still present).
- Reports per-entry status: still accurate / appears resolved / unverifiable.

Pass criteria: the agent does mechanical verification (uses Grep/Read), not speculation; produces a per-entry list; does not invent claims about entries it can't verify.

- [x] **Step 5: Capture observations**

Append to `testing/fixtures-run-2026-05-24/results.md`:

```markdown
## Integration smoke test (the four canonical invocations)

### Case 1 — check quality
<one paragraph: what the agent did, what was good, what was off>

### Case 2 — plan migration
<same>

### Case 3 — code changed update docs
<same>

### Case 4 — verify tech-debt records
<same>

## Open gaps after smoke test
<bullets — anything that surfaced as broken, awkward, or missing>
```

Gaps that surface here feed into the next iteration. The bar for v0.2 is "the canonical invocations produce something useful and don't embarrassingly miss" — not perfection.

---

## Self-Review Checklist (run after implementation)

After all tasks complete, before declaring done:

1. **Spec coverage.** Open `docs/plans/2026-05-24-b-core-design.md`. For each primitive, point to its section in SKILL.md. For the reviewer interface block, point to `agents/codocu-reviewer.md`. For the runtime boundaries, point to the corresponding SKILL.md section.

2. **No v0.1 vocabulary in artifacts.** Grep SKILL.md and the agent for "sync state", "synced", "desynced", "dirty", "subtractive", "generative", "propose", "doc-code", "apply" (as v0.1 skill names). None should appear in skill or agent content.

3. **Voice check.** Skim SKILL.md and the agent. Look for narration-of-machinery: step numbers in user-facing output, "per the skill", mode names, "I will now". Cut them.

4. **Reader test (per the codocu.md gate).** Where would a contributor reading SKILL.md for the first time get lost or bored? Name and fix.

5. **Eval pass rate.** Atomic review ≥80% on first pass; writer fixtures both pass on judgment grounds; integration smoke test produces useful behavior across all four cases.

---

## Handoff

When all tasks complete and self-review passes, leave the artifacts in place and stop. The user will review, run their own tests, and commit when ready. Do not commit.

Surface to the user:
- Where the artifacts live (`skills/codocu/SKILL.md`, `agents/codocu-reviewer.md`, `.claude-plugin/plugin.json`).
- The eval results doc (`testing/fixtures-run-2026-05-24/results.md`).
- Any gaps from the smoke test that were not fixed in this pass.
