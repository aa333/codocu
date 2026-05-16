# Codocu

> Codocu sync state: Synced
> Documentation state: specs empty, most of knowledge lives in superpowers spec dir, see todo

## Docs structure

This repo *is* the plugin, so its "code" and "docs" map onto plugin assets:

- **Code:** `skills/<name>/SKILL.md` (skills), `templates/` (copied verbatim by
  skills), `.claude-plugin/plugin.json` (manifest).
- **Long-term docs:** `docs/**` — evergreen documentation. Skill-level docs for historical, motivational explanation and other additional context, as well as general principles
The original origin brain-dump is preserved at `docs/first_draft.md` for provenance.
- **Roadmap / TODO:** `docs/todo.md` — record **all** roadmap, TODO, and tech-debt entries here (V1 / V2 / Meta sections). Remove entries on implementation.
- **Test reports:** Long-term test reports live in `testing/`. Suites are dated directories.
- **Legacy superpowers plans** - this repo periodically works with superpowers skills. Specs from `docs/superpowers/specs` are to be refactored into codocu-style documentation for 