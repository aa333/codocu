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
