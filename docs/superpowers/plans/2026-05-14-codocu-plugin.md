# Codocu Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code plugin that implements the Codocu workflow — propose→implement→fold across four entry cases, seven commands.

**Architecture:** Each command is a standalone `SKILL.md` file. All skills read `codocu.md` from the project root for per-project conventions. No runtime dependencies — pure markdown instructions interpreted by the LLM agent.

**Tech Stack:** Claude Code plugin format (`SKILL.md` with YAML frontmatter), Markdown

**Spec:** `docs/superpowers/specs/2026-05-14-codocu-design.md`

---

## File Map

| File | Purpose |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `templates/codocu.md` | Default template seeded by `:init` |
| `skills/init/SKILL.md` | `/codocu:init` |
| `skills/propose/SKILL.md` | `/codocu:propose` — case 1 |
| `skills/doc-code/SKILL.md` | `/codocu:doc-code` — case 2 |
| `skills/code-doc/SKILL.md` | `/codocu:code-doc` — case 3 |
| `skills/apply/SKILL.md` | `/codocu:apply` |
| `skills/fold/SKILL.md` | `/codocu:fold` (alias: `:sync`) |
| `skills/codocu/SKILL.md` | `/codocu` bare router — case 4 |

---

## Task 1: Plugin scaffold

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `templates/` directory
- Create: `skills/` directory

- [ ] **Step 1: Create plugin manifest**

```json
// .claude-plugin/plugin.json
{
  "name": "codocu",
  "description": "Keep code, plans, and docs coherent. Propose, implement, and fold changes through an explicit lifecycle.",
  "version": "0.1.0",
  "license": "MIT",
  "keywords": ["docs", "plans", "workflow", "sync", "spec"]
}
```

- [ ] **Step 2: Create directory structure**

```
mkdir -p skills/init skills/propose skills/doc-code skills/code-doc
mkdir -p skills/apply skills/fold skills/codocu templates
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/
git commit -m "feat: add plugin manifest"
```

---

## Task 2: Default `codocu.md` template

**Files:**
- Create: `templates/codocu.md`

- [ ] **Step 1: Write the default template**

```markdown
// templates/codocu.md
# Codocu

> Codocu sync state: Synced

## Docs structure

Module-level docs in `docs/actual/`. One file per module by default; decompose to
`docs/actual/module/` when a module needs more than one doc file.

Modules, slices, or system-level groupings are all valid — organize however matches
the project's natural boundaries.

## Fold settings

When folding incomplete plans, ask the user what to do with unfinished items:
- Move to `docs/tech-debt-todo.md`
- Extract into a new trimmed plan
- Skip (leave incomplete, revisit later)

## Tech debt (optional)

Track tech debt in `docs/tech-debt-todo.md` using `TD-XXXX` codes.
Cross-link from inline code `TODO`s: `// TODO TD-0012 fix rate limiting`.
Items are removed on completion.

To disable tech debt tracking entirely, delete this section.

## Additional notes

Add any project-specific conventions here. The agent reads this file at the start
of every /codocu invocation.
```

- [ ] **Step 2: Commit**

```bash
git add templates/codocu.md
git commit -m "feat: add default codocu.md template"
```

---

## Task 3: `/codocu:init` skill

**Files:**
- Create: `skills/init/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/init/SKILL.md
---
name: init
description: Initialize Codocu in a project by creating codocu.md with sensible defaults. Run once per project.
---

# Codocu Init

Set up Codocu in the current project.

## Steps

1. **Check for existing codocu.md.** If `codocu.md` exists at the project root, stop
   and tell the user. Do NOT overwrite it. Suggest they edit it directly or delete it
   to re-run init.

2. **Create `codocu.md`** at the project root with this exact content:

   ```markdown
   # Codocu

   > Codocu sync state: Synced

   ## Docs structure

   Module-level docs in `docs/actual/`. One file per module by default; decompose to
   `docs/actual/module/` when a module needs more than one doc file.

   Modules, slices, or system-level groupings are all valid — organize however matches
   the project's natural boundaries.

   ## Fold settings

   When folding incomplete plans, ask the user what to do with unfinished items:
   - Move to `docs/tech-debt-todo.md`
   - Extract into a new trimmed plan
   - Skip (leave incomplete, revisit later)

   ## Tech debt (optional)

   Track tech debt in `docs/tech-debt-todo.md` using `TD-XXXX` codes.
   Cross-link from inline code `TODO`s: `// TODO TD-0012 fix rate limiting`.
   Items are removed on completion.

   To disable tech debt tracking entirely, delete this section.

   ## Additional notes

   Add any project-specific conventions here. The agent reads this file at the start
   of every /codocu invocation.
   ```

3. **Check if `docs/` exists.** If not, offer to create the default folder structure:
   ```
   docs/actual/     # evergreen module docs
   docs/plans/      # active short-term plans
   docs/archive/    # completed plans
   ```
   Ask the user before creating — they may have a different structure in mind.

4. **Tell the user:**
   - `codocu.md` was created at the project root
   - Sections to customize: docs structure, fold settings, tech debt strategy
   - All paths in `codocu.md` are configurable — the agent reads it on every invocation
   - Run `/codocu:propose` to start a new feature, or `/codocu` if unsure where to begin
```

- [ ] **Step 2: Manual test scenario**

In a fresh empty directory:
1. Run `/codocu:init`
2. Verify `codocu.md` was created with the default template content
3. Run `/codocu:init` again — verify it stops and does NOT overwrite
4. Verify the agent offers to create `docs/` subdirectories

- [ ] **Step 3: Commit**

```bash
git add skills/init/SKILL.md
git commit -m "feat: add :init skill"
```

---

## Task 4: `/codocu:propose` skill (case 1)

**Files:**
- Create: `skills/propose/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/propose/SKILL.md
---
name: propose
description: Start a new feature or change from intent. Creates a plan after proposal approval. Use when you know what you want to build and the project is (roughly) in sync.
---

# Codocu Propose

Turn a new intent into an approved plan, ready to implement.

## Before starting

Read `codocu.md` from the project root. If it doesn't exist, suggest running
`/codocu:init` first and stop.

## Dirty state warning

Check these signals quickly — do NOT do a full project scan:
- `git status` if git is available: any uncommitted changes?
- `docs/plans/`: any active plan files?

If either signal is positive, warn the user:
> "There are [uncommitted changes / active plans] — you may want to resolve those
> first with `/codocu` or `/codocu:fold`. Continue anyway?"

Do not block. If the user confirms, proceed.

## Proposal

Ask the user what they want to build or change, if they haven't already said.
Draft a **ProposalSummary** in the conversation — do NOT write it to disk:

- **Scope:** what is changing (modules, APIs, data, etc.)
- **Affected areas:** files or systems likely to be touched
- **Risks or open questions:** anything that could go wrong or needs a decision

Present it and ask: "Does this look right? Anything to add or change?"
Iterate until the user approves.

## Write the plan

Once approved, write the plan to `docs/plans/YYYY-MM-DD-{topic}.md`
where `{topic}` is a short kebab-case summary of the intent (e.g. `user-createdat`).

Plan format:
```markdown
# {Topic} Plan

**Goal:** {one sentence from the proposal}

**Context:** {relevant background, 2-4 sentences}

## Steps

- [ ] Step 1: ...
- [ ] Step 2: ...
```

Steps should be concrete and granular. Each step should be completable in one
focused action. Prefer too many small steps over too few large ones.

## After writing

Tell the user where the plan was written. Ask:
> "Ready to start implementing? I can work through the plan now, or you can
> pick it up later with `/codocu:apply`."

If they want to start: begin implementing the plan steps in order, checking each
off (`- [x]`) as it completes.
When all steps are done, suggest `/codocu:fold`.
```

- [ ] **Step 2: Manual test scenario**

In a repo with a clean `codocu.md`:
1. Run `/codocu:propose` and say "add a user profile page"
2. Verify the agent drafts a ProposalSummary in-conversation (scope, affected areas, risks)
3. Approve it
4. Verify a plan file appears at `docs/plans/YYYY-MM-DD-user-profile-page.md` with checkable steps
5. Decline to start implementing — verify agent stops cleanly

In a repo with uncommitted changes:
1. Run `/codocu:propose`
2. Verify the dirty warning appears but does not block

- [ ] **Step 3: Commit**

```bash
git add skills/propose/SKILL.md
git commit -m "feat: add :propose skill"
```

---

## Task 5: `/codocu:doc-code` skill (case 2)

**Files:**
- Create: `skills/doc-code/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/doc-code/SKILL.md
---
name: doc-code
description: Docs describe the desired state — implement them in code. Use when you have already written or edited docs and want to implement what they describe.
---

# Codocu Doc-Code

The docs are the proposal. Write a plan and implement it.

## Before starting

Read `codocu.md` from the project root.

## Identify the docs delta

Ask the user which docs they changed or are treating as the spec, if they haven't
already said. If git is available, check `git diff` for changed `.md` files and
offer those as candidates — but the user decides.

Read the identified docs.

## Write the plan

No ProposalSummary step — the docs are the proposal.

Write a plan to `docs/plans/YYYY-MM-DD-{topic}.md` describing the code changes
needed to implement what the docs describe.

Plan format (same as `:propose`):
```markdown
# {Topic} Plan

**Goal:** {what the docs are specifying}

**Source docs:** {list of doc files being implemented}

## Steps

- [ ] Step 1: ...
```

Show the plan to the user and ask if it looks right before proceeding.
Iterate if needed.

## Implement

Work through the plan steps in order, checking each off as it completes.
When all steps are done, suggest `/codocu:fold`.
```

- [ ] **Step 2: Manual test scenario**

1. Manually edit `docs/actual/user.md` to add a section describing a new `role` field
2. Run `/codocu:doc-code`
3. Verify the agent identifies `user.md` as the changed doc (or accepts your answer)
4. Verify a plan is written covering the code changes needed
5. Verify the plan skips the ProposalSummary step

- [ ] **Step 3: Commit**

```bash
git add skills/doc-code/SKILL.md
git commit -m "feat: add :doc-code skill"
```

---

## Task 6: `/codocu:code-doc` skill (case 3)

**Files:**
- Create: `skills/code-doc/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/code-doc/SKILL.md
---
name: code-doc
description: Code is the source of truth — update docs to reflect it. Use after manual code changes, refactors, or to document an undocumented area.
---

# Codocu Code-Doc

Read what changed in code and bring the docs up to date.

## Before starting

Read `codocu.md` from the project root for doc conventions (locations, format).

## Identify the code delta

If git is available, run `git diff` as a starting hint. Tell the user what you see
and ask if that's the area to work with, or if they have something else in mind.
If git is not available, ask the user: "Which area or files should I look at?"

Read the relevant code.

## Assess scope

Judge the size and nature of the change:
- **Small:** a few files changed, clear mapping to existing docs (e.g. a new field,
  a renamed method, a small new function). Proceed directly to auto-update.
- **Large / brownfield:** significant architectural change, many files, or an area
  with no existing docs. Use the proposal flow.
- **Uncertain:** ask the user — "This looks like [X]. Is this a small update or
  should we make a plan?"

## Small scope path

Identify the ActualDocs that cover the changed area per `codocu.md` conventions.
Draft the updated doc sections. Show diffs to the user before writing:
> "I'd update [file] with these changes: [diff]. Look right?"

Write on approval. Done — no plan, no fold needed.

## Large / brownfield path

Draft a **ProposalSummary** in-conversation:
- What to document (areas, modules)
- Which existing docs to update
- Which new docs to create

Ask for approval. Iterate until approved.

Write a documentation plan to `docs/plans/YYYY-MM-DD-document-{area}.md`:
```markdown
# Document {Area} Plan

**Goal:** {what will be documented}

## Steps

- [ ] Step 1: Write/update {doc file} covering {area}
- [ ] Step 2: ...
```

Work through the plan, writing and updating docs per `codocu.md` conventions.
When done, suggest `/codocu:fold`.
```

- [ ] **Step 2: Manual test scenario**

Small scope:
1. Make a one-line change to a code file (add a field)
2. Run `/codocu:code-doc`
3. Verify agent identifies the change, judges it as small, and shows a doc diff
4. Approve — verify the doc is updated with no plan file created

Large / brownfield:
1. Run `/codocu:code-doc` and say "document the entire auth module"
2. Verify agent produces a ProposalSummary and asks for approval
3. Approve — verify a plan file is written before any docs are touched

- [ ] **Step 3: Commit**

```bash
git add skills/code-doc/SKILL.md
git commit -m "feat: add :code-doc skill"
```

---

## Task 7: `/codocu:apply` skill

**Files:**
- Create: `skills/apply/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/apply/SKILL.md
---
name: apply
description: Resume or apply an existing plan. Use when returning to an interrupted session or when a plan was written manually.
---

# Codocu Apply

Pick up where a plan left off.

## Before starting

Read `codocu.md` from the project root.

## Find the plan

List all `.md` files in `docs/plans/`.

- **None found:** tell the user there are no active plans. Suggest `/codocu:propose`
  to start something new.
- **One found:** confirm with the user: "Found `{filename}`. Apply this plan?"
  Proceed on confirmation.
- **Multiple found:** list them with their goals (read the **Goal:** line from each).
  Ask which to apply. Offer: "Apply all in sequence?" as an option.

## Apply the plan

Read the plan file. Find the first unchecked step (`- [ ]`).

If all steps are already checked: tell the user the plan looks complete and
suggest `/codocu:fold` to archive it.

Otherwise: work through the unchecked steps in order, checking each off as it
completes. Show the user each step before executing so they can redirect.

When all steps are checked: tell the user the plan is complete.
Suggest `/codocu:fold`.
```

- [ ] **Step 2: Manual test scenario**

1. Create a plan at `docs/plans/2026-05-14-test.md` with 3 steps, first 2 checked
2. Run `/codocu:apply`
3. Verify agent reads the plan, identifies step 3 as the first unchecked step, and starts there
4. Verify it does NOT re-do the already-checked steps

With no plans:
1. Remove all files from `docs/plans/`
2. Run `/codocu:apply`
3. Verify agent says no active plans and suggests `:propose`

- [ ] **Step 3: Commit**

```bash
git add skills/apply/SKILL.md
git commit -m "feat: add :apply skill"
```

---

## Task 8: `/codocu:fold` skill

**Files:**
- Create: `skills/fold/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/fold/SKILL.md
---
name: fold
description: "Archive completed plans and sync any docs they touched. Also invokable as /codocu:sync. Run at the end of a feature or when you want to wrap up in-progress work."
---

# Codocu Fold

Wrap up one or more plans: verify completion, update docs, archive.

Also invokable as `/codocu:sync` — same behavior.

## Before starting

Read `codocu.md` from the project root, especially the **Fold settings** section.

## Select a plan

List all `.md` files in `docs/plans/`.

- **None:** tell the user there's nothing to fold. Done.
- **One:** fold it.
- **Multiple:** list them with their goals. Ask which to fold.
  Offer: "Go through all plans one by one?"

## Per-plan process

### 1. Sanity check

Read the plan's steps. For each step marked done (`- [x]`), briefly verify the
corresponding change actually exists in code. If a checked step appears not to be
implemented, flag it:
> "Step N is marked done but I can't find the corresponding change. Want to
> re-implement it, uncheck it, or skip?"

Do not fail silently. Surface every discrepancy before proceeding.

### 2. Handle incomplete steps

If there are unchecked steps (`- [ ]`):

Read the **Fold settings** in `codocu.md` for the configured default. Apply it
unless the user overrides. Options:

- **Move to tech debt:** append each incomplete step to `docs/tech-debt-todo.md`
  as a `TD-XXXX` item. Scan the file for the highest existing `TD-NNNN` number
  and increment by 1. If no items exist yet, start at `TD-0001`.
- **Create new plan:** write a new `docs/plans/YYYY-MM-DD-{topic}-continued.md`
  containing only the incomplete steps.
- **Ask:** present the options and let the user choose per item.
- **Skip:** note the incomplete items in the archive but take no action.

If codocu.md has no fold settings, default to **Ask**.

### 3. Update docs

Check whether the work covered by this plan requires ActualDoc updates per
`codocu.md` conventions.

- **Small or obvious update:** draft the change, show it to the user, write on approval.
- **Larger update:** show a diff and ask for explicit approval before writing.

### 4. Update sync state marker

Update the `codocu.md` status line to reflect that the project is now synced:

Find the line starting with `> Codocu sync state:` and replace it with:
```
> Codocu sync state: Synced
```

### 5. Archive

Move the plan file from `docs/plans/` to `docs/archive/`.

### 6. Report

Tell the user:
- Plan archived to `docs/archive/`
- Any docs updated
- Any tech debt items added or new plans created
- Any discrepancies found in the sanity check
```

- [ ] **Step 2: Manual test scenario**

Completed plan:
1. Create `docs/plans/2026-05-14-test.md` with all steps checked
2. Run `/codocu:fold`
3. Verify agent does sanity check, updates relevant docs, moves file to `docs/archive/`

Incomplete plan:
1. Create a plan with 3 steps, only 2 checked
2. Set codocu.md fold settings to "ask"
3. Run `/codocu:fold`
4. Verify agent flags incomplete step and asks what to do
5. Choose "move to tech debt" — verify `docs/tech-debt-todo.md` is updated

Multiple plans:
1. Create two plan files
2. Run `/codocu:fold`
3. Verify agent lists both and asks which to fold

- [ ] **Step 3: Commit**

```bash
git add skills/fold/SKILL.md
git commit -m "feat: add :fold skill"
```

---

## Task 9: `/codocu` bare router skill (case 4)

**Files:**
- Create: `skills/codocu/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
// skills/codocu/SKILL.md
---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads signals and guides you to the right action.
---

# Codocu Router

Figure out where things stand and what to do next.

## Read signals

Gather these quickly — no full project scan:

1. **Git** (if available): `git status` — what files have uncommitted changes?
   - Only `.md` files → hint: docs are ahead, consider `:doc-code`
   - Only code files → hint: code is ahead, consider `:code-doc`
   - Both → conflict, need resolution

2. **Active plans**: list files in `docs/plans/` — any in progress?

3. **`codocu.md`**: does it exist? If not, suggest `/codocu:init` and stop.

## Present findings

Tell the user what you found. Be concise:
> "Here's what I see: [uncommitted code changes in X, Y] and [active plan: Z].
> What would you like to do?"

If signals point clearly to one action (e.g. only code changed, no active plans),
suggest it directly and ask for confirmation.

## Case 4 — both sides changed (conflict)

If both code and docs have uncommitted changes, or the user says "things are a mess":

Walk through the conflicts area by area:
> "In [area], the docs say [X] and the code does [Y]. Which is the intended truth?"

Record the user's answers. Once all areas are resolved, write a resolution plan:

```markdown
# Resolution Plan

**Goal:** Bring code and docs into sync

## Steps

- [ ] [area 1]: update [code/docs] to match [docs/code]
- [ ] [area 2]: ...
```

Save to `docs/plans/YYYY-MM-DD-resolution.md`.

Implement per plan. Suggest `/codocu:fold` when done.

## No conflicts — triage

If no conflicts but user isn't sure what to do:

- Active plan exists → suggest `/codocu:apply` to continue it
- No active plan, project is clean → suggest `/codocu:propose` for something new
- No git → ask: "What changed recently? Docs, code, or both?"
```

- [ ] **Step 2: Manual test scenario**

Both changed:
1. Edit a `.md` doc file and a code file, leave both uncommitted
2. Run `/codocu`
3. Verify agent reads git status, identifies the conflict, and asks which side wins
4. Resolve each area — verify a resolution plan is written before any changes are made

Clean state:
1. Commit all changes, no active plans
2. Run `/codocu`
3. Verify agent suggests `:propose` as the natural next step

No git:
1. Simulate no git (or run in a non-git directory)
2. Run `/codocu`
3. Verify agent asks the user what changed rather than erroring

- [ ] **Step 3: Commit**

```bash
git add skills/codocu/SKILL.md
git commit -m "feat: add bare /codocu router skill"
```

---

## Task 10: Smoke test — end-to-end forward flow

Verify the full case 1 flow works together before shipping.

- [ ] **Step 1: Set up a test project**

Create a fresh directory with a minimal codebase (a few files, nothing complex).
Run `/codocu:init` and verify `codocu.md` is created.

- [ ] **Step 2: Run a full propose→implement→fold cycle**

1. `/codocu:propose` — "Add a `createdAt` field to the user record"
2. Approve the ProposalSummary
3. Verify plan is written at `docs/plans/`
4. Let the agent implement the plan steps
5. `/codocu:fold` — verify sanity check, doc update, and archive

- [ ] **Step 3: Verify the backward flow**

1. Manually edit a code file (add a comment field)
2. `/codocu:code-doc` — verify small scope auto-update, no plan created

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "feat: codocu plugin v0.1.0 complete"
```
