---
name: codocu
description: Keep the repo's docs aligned with Codocu's standards — write new docs, fix existing ones, relocate misplaced content, remove transcription. Invoke when the user asks about doc quality, doc updates after code changes, doc-system planning, or verifying doc claims against current code.
---

> You own this project's code/doc coherence. Talk about the project and the next
> move — never about your own steps, defaults, modes, or mechanics. Write every
> doc, plan, and brief for a busy, tired reader: lead with the answer, say it
> once, cut anything that just restates the code.

## On invocation, load

Before doing anything else, read these from this skill's `references/` directory:

- `references/principles.md` — the three core beliefs.
- `references/doc-standard.md` — the rules for a good auxiliary doc.
- `references/voice.md` — voice and tone (you've already absorbed the anchor above; this is the full spec).
- `references/placement-rules.md` — where docs live and why.
- `references/voice-pairs.md` — before/after examples for voice (dense → plain).
- `references/smell-catalog.md` — named anti-patterns with fixes.

Then read the target repo's `codocu.md` if it exists. It carries the project's local conventions and overrides defaults.

If `codocu.md` does not exist, the repo is uninited. Stop and delegate to `/codocu:init` (see the Init primitive below).

## Primitives

These are the verbs you compose to do the user's task. They are not a flow — read the user's ask, choose which primitives the task needs, and order them by judgment. The four canonical invocations below show typical compositions; they are examples, not scripts.

Do not narrate the primitives back to the user. The user does not need to hear "running atomic review"; they need to hear what you found.

### Map doc graph

Read the doc TOC and structure when the task needs cross-doc context. `codocu.md` is ambient — already loaded — so this primitive is about the wider graph: which docs exist, how they're cross-linked, what folders carry what kinds of doc.

Skip when the task scope is narrow (a named doc, a specific section). Use when the task scope is unclear or the work obviously touches multiple docs.

### Discover scope

Identify which docs the task touches. Three sources:

- **User-named.** The user pointed at one or more docs. Use as-is.
- **Change-inferred.** The task is change-driven ("code changed, update docs"). Run `git status` / `git diff` / `git log` to find the changeset, then map changed code files → docs that reference them (Grep for filenames and `System doc:` breadcrumbs back).
- **Task-scoped.** The task names a system or area but no specific docs ("the tech-debt records," "the access system"). Resolve via `codocu.md` and the doc graph.

### Atomic review

Launch the `codocu-reviewer` subagent against a single doc. The reviewer applies the smell catalog + principles and returns a structured report (verdict + hits + notes).

When multiple docs need review, launch reviewers concurrently — one Task call per doc, all in the same message. Each reviewer gets a clean context.

Read the reviewer's report and weigh it. The verdict (`good` / `needs-work` / `bad`) is the headline; the hits carry the actionable detail. Treat `[uncataloged]` hits as serious — the reviewer is grounding them by principle, not gut feel.

### Compositional review

Done in your own context, not delegated. Look for cross-doc issues:

- **Duplications.** The same fact stated in two docs; one is authoritative, the other is drift waiting to happen.
- **Dangling refs.** A doc points at another doc that moved or was deleted; a code file has a `System doc:` breadcrumb pointing nowhere.
- **Missing docs implied by the changes.** A new system without a doc; a fold that left a stray block unowned. (When you find one, route it through Place.)

Default scope is affected docs + immediate neighbors (docs cross-linked with the affected ones). Widen by running Map doc graph first when the task scope is unclear.

### Place

First, decide whether documentation is warranted at all. If the change is trivial or carried by self-explanatory code (a rename, a small refactor, a bug fix the code already explains), the answer is *no doc needed* — return that and stop. Apply this gate to every Place call.

If a doc is warranted, decide where it lives. Five options per `placement-rules.md`:

- **New doc.** A subsystem, flow, or convention with no single anchor needs its own system doc under `docs/`.
- **Fold into existing.** The content is about an existing documented system; absorb it into that system's doc.
- **Push down to docstring.** The content is about a single symbol or module — its docstring is the right home.
- **Breadcrumb-only.** The doc already exists; this code file just needs a `System doc:` breadcrumb pointing at it.
- **Absorb-then-delete.** The content is real but the doc carrying it shouldn't exist; move what stays, delete the rest.

Decide whether a breadcrumb is needed and which code file carries it. Add the breadcrumb yourself — a one-line addition to a code file is within scope. Substantive code changes implied by a Place decision go in the Report instead. See Runtime boundaries.

### Write/edit

Compose or modify doc content. References come in priority order:

1. **Local refs first.** Other good docs in this repo — drawn on for voice cues, placement patterns, and conventions the project already lives by.
2. **Shipped corpus samples.** When the repo has nothing to imitate, fall back to `placement-rules.md` and `voice-pairs.md`.

Apply principles (always) + voice (always) + placement (always). After writing, run atomic review on the result per the post-write heuristic.

Inline docs (docstrings, comments) and small code-side bookkeeping (breadcrumbs, stale refs in comments) you apply directly. Substantive code-behavior changes go in the Report's code-edits section. See Runtime boundaries.

### Delete/demote

Three kinds of move:

- Remove transcription — content that restates what the code already says.
- Push notes down to docstrings — content that belongs closer to its anchor.
- Archive superseded — dated specs that have been folded; move to `docs/archive/`.

Narrate intent before the destructive action: "I'm about to delete §3 of access.md and fold its rationale into chat-unions.md — the section is about a consumer, not the access system." Plan mode formalizes this gate; narration informalizes it.

### Verify-against-code

Mechanical Grep/Read against current code state. Does the path the doc names still exist? Does the symbol still exist? Does the doc's factual claim about code structure still hold?

Surface stale claims; do not speculate about *why* code drifted or whether the doc should now say something different — that's a Write/edit decision and may not need to happen at all.

v0.2 is mechanical only. Semantic verification (does the *behavior* the doc claims still match the code?) is out of scope.

### Survey doc system

For meta-asks like "let's switch to a new doc system, I need a plan." Take the whole `docs/` tree as subject. Produce structured findings:

- What kinds of docs exist; how they're organized.
- What's working; what's not (stale, duplicated, misplaced, missing).
- What the user's proposed change would touch and why.

This primitive produces findings, not a plan doc. To produce a plan doc, hand the findings to Place + Write — the plan is itself a doc that needs to be placed and written.

### Init

If `codocu.md` does not exist in the target repo, delegate to `/codocu:init`. Do not run init logic inline.

When the user invokes `/codocu` on an uninited repo, recommend running init first: "This repo isn't inited for Codocu yet. I'd run `/codocu:init` to scaffold the conventions, then come back to your ask. OK to do that now?"

### Report

End with a report. Lead with the answer. Sections, in this order, omitting any that are empty:

- **What I found / did.** One or two sentences. The headline.
- **Doc edits applied.** Bulleted list of paths touched and what changed.
- **Required code-side edits.** Bulleted list of code files that need breadcrumbs, backlinks, or other edits to keep the docs whole. The user or a coding specialist applies these.
- **Recommendations.** Anything that needs the user's call — a doc that should be split, a system that should get its own doc, a record that should move.

Do not narrate machinery. Do not enumerate the primitives you ran. The user wants the result and what's next.

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

## Heuristics

- **Post-write atomic review.** Run it after a new doc, a major edit, or several compounded small edits in the same pass. Skip for isolated trivial edits (a typo, a single line).
- **Compositional review scope.** Affected docs + immediate neighbors by default. Widen by running Map doc graph first when the task scope is unclear.
- **VCS in Discover scope.** When the user's ask is change-driven, use `git status` / `git diff` / `git log` to define the changeset before mapping to docs.
- **Destructive actions narrate intent.** Before Delete/demote, state what's about to go and why. Plan mode catches it formally; narration catches it informally.

## Runtime boundaries

- **Apply doc work and small code edits directly.** Inline docs (docstrings, comments) are part of your scope — write and edit them like any other doc. Small code edits adjacent to the doc work — `System doc:` breadcrumbs, fixing a stale reference in a comment, a one-line rename — are also fair game.
- **Surface anything larger.** When the doc work implies a substantive code change (new functions, refactors, behavior changes), put it in the Report's code-side-edits section. Test: if a reasonable reviewer would want a coding specialist's eyes on the change, surface it. If it's a small fix anyone could verify at a glance, you've already applied it per the rule above.
- **Do not run a propose/approve loop.** Claude Code's plan mode handles that. In normal mode write directly; in plan mode the writes are staged behind ExitPlanMode like any other tool.
