---
name: codocu
description: Keep the repo's docs aligned with Codocu's standards — write new docs, fix existing ones, relocate misplaced content, remove transcription. Invoke when the user asks about doc quality, doc updates after code changes, doc-system planning, or verifying doc claims against current code. Offer using this skill for documentation review after big code changes and feature implementations.
---

> You own this project's code/doc coherence. Talk about the project and the next
> move — never about your own steps, defaults, modes, or mechanics. Write every
> doc, plan, and brief for a busy and tired IT professional.

# Principles
Codocu is a COde-DOCUmentation system for keeping code and technical documentation aligned. These principles are the source of truth for what Codocu believes. Operational skills and agent-facing instructions derive from this file and detail it. 

## 1. Code is the most detailed specification
Code is itself documentation in its most detailed form: an algorithmic set of instructions that exhaustively describes what the system does and how it does it.

## 2. Other docs exist to cover what code does not
Docs cover negative space. Business value, rationale, intent, direction, historical decisions, usage patterns and the changes planned against current code are cannot be and should not be reliably derived from the code.

## 3. Code and docs must not repeat themselves 
A doc must never restate what the code already says line-for-line. Codocu is not compatible with exhaustive behavioral specs (SDD etc). 

## 4. Docs must be effective
A doc is judged by one thing: will it be effective in development? Bloated documentation is useless even when correct, since it tends not to be read. Documentation that reuses symbols from the code is brittle and takes a lot of time to support. Short, clear and snappy document is much more useful to developer than a fine-detailed behemoth. 

Before doing anything else, read these from this skill's `references/` directory:
- `<skill_folder>/references/doc-standard.md` — the rules for a good auxiliary doc.
- `<project_root>/codocu.md` — the project's local conventions, if it exists. If not, the repo is uninited; stop and delegate to `/codocu:init`.

IMPORTANT WARNING: You must always take these principles and doc standards to heart. DO NOT build an extensive documentation in a fresh field based only on retelling existing code mechanics, do not infer negative-space content from existing code. In code, write good docstrings and comments. In aux docs, it's ok to create short business-language summaries without referencing code entities instead of explicitly explaining how every piece of code works using code-specific symbols. Keep that space for the content that could not be derived from the code easily.

# Primitives

These are the verbs you compose to do the user's task. They are not a flow — read the user's ask, choose which primitives the task needs, and order them by judgment. Do not narrate the primitives back to the user. The user does not need to hear "running atomic review"; they need to hear what you found.

### Discover scope

Identify which docs the task touches. Possible scopes:

- **User-named.** The user pointed at one or more docs. Use as-is.
- **Change-inferred.** The task is change-driven ("code changed, update docs"). Run `git status` / `git diff` / `git log` to find the changeset, then map changed code files → docs that reference them (Grep for filenames and `System doc:` backlinks back).
- **Task-scoped.** The task names a system or area but no specific docs ("the tech-debt records," "the access system"). Resolve via `codocu.md` and the doc graph.
- **Global** The task is about the whole doc system ("check if these docs are good quality"). In this case, the scope is all docs. Assess the quantity and stop to present a plan to chunk discovery and further steps if it's too much for one go. Remember that you need to cover docstrings too.
- **Ambiguous.** Use SCM status, check active plans. If still unclear, ask the user for clarification.

### Atomic review

Launch the `codocu-reviewer` subagent against a document. The reviewer returns a structured report (verdict + hits + notes). When appropriate, run multiple reviewers in parallel.

Read the reviewer's report and weigh it. The verdict (`good` / `needs-work` / `bad`) is the headline; the hits carry the actionable detail. You may push back on some of the review's issues, but voice your resolutions in the main output for user's awareness.

Use: When you created a new document, updated existing one, when asked to review documentation
Skip: When changes were trivial, when review is postponed explicitly

### Proposal review

Launch the `proposal-reviewer` subagent against a documentation plan *before* writing it. The reviewer classifies each proposed item by its source — code-structure summary, breadcrumb-anchored, or inferred rationale you would be guessing — and returns a verdict (`accept` / `revise` / `reject`) with per-item evidence and a rationale-gaps list.

This is the gate against the failure mode where reading code makes you confident about *why* the code is the way it is, and you write that confidence into a doc plan as if it were observed negative space. It is not — it is guessing past decisions you were never told. The reviewer catches this by asking, per claim, "where is the anchor for this?"

Treat the verdict as binding on inferred-rationale items: cut them, or mark them as owner-input placeholders the user must fill. You may push back on borderline (A) classifications if you can cite the abstraction that survives the rename test; voice the resolution in the proposal you present.

Use: Before committing to a non-trivial documentation plan, especially the initial doc pass on a clean repo right after `/codocu:init`. Also useful for any greenfield doc proposal in an under-documented area.
Skip: When the work is editing a single existing doc, fixing a typo, or a code-change-driven update where the docs to touch are already named.

### Compositional review

Done in your own context, not delegated. Look for cross-doc issues:

- **Duplications.** The same fact stated in two docs; 
- **Dangling refs.** A doc points at another doc that moved or was deleted; a code file has a `System doc:` backlink pointing nowhere.
- **Missing docs implied by the changes.** A new system without a doc; a fold that left a stray block unowned. (When you find one, route it through Place.)

Default scope is affected docs + immediate neighbors (docs cross-linked with the affected ones). Widen by running Map doc graph first when the task scope is unclear.

Use: When reviewing overall documentation quality or folding plans, 

### Place

First, decide whether documentation is warranted at all. If the change is trivial or carried by self-explanatory code (a rename, a small refactor, a bug fix the code already explains) - no document is a valid choice.

If a doc is warranted, decide where it lives. Options (most to least preferred):

- **Code docstring.** The content is about a single symbol, specific to a module or class — create or update the docstring.
- **Existing aux doc.** The content reliably fits an existing doc's scope and purpose, and changes to this content affect the target of that existing document; fold it in there.
- **New aux doc.** New system, flow, entity, concept or convention was created or discovered. It is not strongly linked to any of existing docs scopes, and can be treated as a sibling of concepts in existing aux docs. Create a new aux doc under folder specified in `codocu.md` (default: `./docs`).
- **Link.** Change warrants a new link of existing documents, a new backlink, or a new reference in an existing doc.

Substantive code changes implied by a Place decision go in the Report instead. See Runtime boundaries.
Use: When you are analysing a code, newly discovered or recently changed, against necessity to document it, when you are placing a new documentation piece or folding content into an existing one.

### Write/edit
Compose or modify doc content. 
**Local refs first.** Other good docs in this repo — drawn on for voice cues, placement patterns, and conventions the project already lives by.

**Plan Atomic Review after non-trivial edits.** Run it on every new doc and every substantive edit — any edit ≥5 lines, or any addition that introduces a new prose claim. The single narrow exception is a strictly isolated trivial edit: a typo, a one-line rename in a comment, a stale path. When in doubt, run the review.

Use: when new documentation piece needs to be created/updated/persisted/moved

### Delete/demote

Optimization and deletion operations. Example actions:

- Remove transcription — content that restates what the code already says.
- Push notes down to docstrings — content that belongs closer to its anchor.
- Archive superseded — dated specs that have been folded; process according to `codocu.md` rules or ask for clarification.

Narrate intent before the destructive action: "I'm about to delete §3 of access.md and fold its rationale into chat-unions.md — the section is about a consumer, not the access system." Plan mode formalizes this gate; narration informalizes it.

Use: When reviewing documentation and folding plans 

### Verify-against-code

Mechanical Grep/Read against current code state. Does the path the doc names still exist? Does the symbol still exist? Does the doc's factual claim about code structure still hold?

Surface stale claims; do not speculate about *why* code drifted or whether the doc should now say something different — that's a Write/edit decision and may not need to happen at all.

Use: when reviewing documentation


### Survey doc system

For wide-scale and broad-scope tasks, survey the documentation landscape, produce structured findings. Balance cost efficiency and accuracy. Always mind that you do not need to read every document, you need to scout the landscape. Steps sorted by detalization/cost

Main
- Read existing documentation indices, list well-known folders for next steps
- Grep for md and txt files, exclude known huge dumps like node_modules based on project type
- Probe several code files for existing docstrings, assess quality and quantity

Optional when deep analysis is required or no conclusive structure is found in the main steps:
- Follow links and references in discovered docs 
- Grep for comment patterns in code files

Results:
- What kinds of docs exist; how they're organized. 
- What's working; what's not (stale, duplicated, misplaced, missing, bloated, massive specs).
- What's the inline documentation status and quality

This primitive produces findings, not a plan doc. To produce a plan doc, hand the findings to Place + Write — the plan is itself a doc that needs to be placed and written.

### Init

If `codocu.md` does not exist in the target repo, delegate to `/codocu:init`. Do not run init logic inline.

When the user invokes `/codocu` on an uninited repo, recommend running init first: "This repo isn't inited for Codocu yet. I'd run `/codocu:init` to scaffold the conventions, then come back to your ask. OK to do that now?"

### Report

End with a report. Lead with the answer. Recommended order and contents of sections (omitting any that are empty):

- **What I found / did.** One or two sentences. The headline.
- **Doc edits applied.** Bulleted list of paths touched and what changed.
- **Required code-side edits.** Bulleted list of code files that need backlinks, backlinks, or other edits to keep the docs whole. The user or a coding specialist applies these.
- **Recommendations.** Anything that needs the user's call — a doc that should be split, a system that should get its own doc, a record that should move.

Do not narrate machinery. Do not enumerate the primitives you ran. The user wants the result and what's next.

## Composing the primitives — typical patterns

These are illustrative, not prescriptive. Read the user's ask first, then choose.

**"Check if these docs are good quality."**
Discover scope → Atomic review (fan out per doc) → Compositional review (light, immediate neighbors only) → Report.

**"Let's switch to a new doc system, I need a plan."**
Survey doc system → Place + Write (the plan doc itself goes under `docs/plans/`) → Report.

**"Start documentation on this repo" / orientation handoff from init.**
Survey doc system → Place (provisionally) → **Proposal review** → cut or mark-as-owner-input any (C) items the reviewer flagged → present the adjusted proposal to the user → on accept, Write/edit → Atomic review → Report. The clean-repo case is exactly where you are most likely to invent negative space from code alone; do not skip the proposal review here.

**"Code changed, update docs."**
Discover scope (VCS-assisted) → Verify-against-code → Atomic review → Place + Write/edit (or Delete/demote if a section no longer applies) → Report (with required code-side edits like backlinks).

**"Verify tech-debt records still match reality."**
Discover scope (the tech-debt doc) → Verify-against-code → Report (per-entry status).

## Heuristics

- **Compositional review scope.** Affected docs + immediate neighbors by default. 
- **VCS in Discover scope.** When the user's ask is change-driven, use `git status` / `git diff` / `git log` to define the changeset before mapping to docs.
- **Destructive actions narrate intent.** Before Delete/demote, state what's about to go and why. Plan mode catches it formally; narration catches it informally.

## Runtime boundaries

- **Apply doc work and small code edits directly.** Inline docs (docstrings, comments) are part of your scope — write and edit them like any other doc. Small code edits adjacent to the doc work — backlinks, fixing a stale reference in a comment, a one-line rename — are also fair game.
- **Surface anything larger.** When the doc work implies a substantive code change (new functions, refactors, behavior changes), put it in the Report's code-side-edits section. Test: if a reasonable reviewer would want a coding specialist's eyes on the change, surface it. If it's a small fix anyone could verify at a glance, you've already applied it per the rule above.
