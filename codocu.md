# Codocu

## Docs structure

This repo *is* the plugin, so "code" and "docs" map onto plugin assets. **Code
is the source of truth**; docs orient, they never drive runtime behavior.

**Code — the plugin itself**

- `skills/<name>/SKILL.md` — one directory per skill; `name` = directory name
  = the `/codocu:<name>` invocation suffix. Skill-only references live beside
  it (a skill loads references from its own directory only).
- `templates/` — files copied verbatim by skills (e.g. `templates/codocu.md`,
  seeded into a target project at onboarding).
- `.claude-plugin/plugin.json` — manifest; its `name` is the namespace prefix.

**Evergreen docs — the orientation map**

- `docs/design/` — the authoritative aspect specs, each short and
  single-purpose: [`principles`](docs/design/principles.md) (what Codocu
  believes), [`voice`](docs/design/voice.md) (who the agent is and how it
  talks), [`doc-standard`](docs/design/doc-standard.md) (the rules for a good
  auxiliary doc). Read the relevant one before changing skill semantics. (The
  old `flows` spec is being reworked in v0.2 — flow overlays become optional
  helpers, not a standing authority.)
- `CLAUDE.md` §First principle — the dev-facing constitution; the same idea
  as `principles.md`, for the contributor at work.
- `docs/inbox/` - long-term docs not yet processed by codocu (e.g. produced by other agents with their preferred context level and tone). These are in-between fleeting and long-term, and should not be committed unless marked explicitly for deferred processing.

**Roadmap**

- `docs/todo.md` — the single home for all roadmap, TODO, and tech-debt records
format: 
```
## version
### item title
Item description, 1-2 paragraphs, short
```

**Active specs & plans**

- `docs/plans/` — dated working specs and implementation plans for in-flight
  work (`YYYY-MM-DD-{topic}.md`), the location Codocu skills read and write.
  (The v0.1 skill set is being reworked in v0.2 — see
  `docs/plans/2026-05-22-v0.2-plan.md`.) Empty between cycles.

**History**

- `docs/archive/` — superseded dated specs/plans, kept as history, not
  deleted (e.g. specs rebuilt into the evergreen `docs/design/`). 

**Provenance & evidence**

- `docs/first_draft.md` — the original origin brain-dump, kept for
  provenance.
- `testing/` — long-term test reports (deliberately outside `docs/` — test
  evidence, not documentation); suites are dated directories.

Note that even though skill files are considered "code" in this repo, we do not leave inline documentation in them (except required by claude), as it will create noise and confusion in consumer agents. No breadcrumbs, no pointers.

## Subagent guidelines

Agents/skills that come with their dedicated opinionated plan/doc/spec structures must keep documents related to planning and immediate implementation in docs/plans. Plans must contain actual completion status per each step. Long-term documents are to be kept in docs/inbox, and cleanly marked for codocu's processing and folding.