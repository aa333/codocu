---
name: init
description: Initialize Codocu in a project by creating codocu.md with sensible defaults. Run once per project.
---

# Codocu Init

Set up Codocu in the current project.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._

## Steps

1. **Check for existing codocu.md.** If `codocu.md` exists at the project root, stop
   and tell the user. Do NOT overwrite it. Suggest they edit it directly or delete it
   to re-run init.

2. **Create `codocu.md`** at the project root with this exact content:

   ```markdown
   # Codocu

   > Codocu sync state: TBD

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
