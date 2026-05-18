# Codocu

> Codocu sync state: Synced
> Documentation state: evergreen design docs are authoritative and live in
> `docs/design/`; active dated specs/plans in `docs/plans/`, superseded ones
> archived in `docs/archive/`.

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

- `docs/design/` — the four authoritative aspect specs, each short and
  single-purpose: [`principles`](docs/design/principles.md) (what Codocu
  believes), [`voice`](docs/design/voice.md) (who the agent is),
  [`flows`](docs/design/flows.md) (states, moves, gates),
  [`doc-standard`](docs/design/doc-standard.md) (what a long-term doc is).
  Read the relevant one before changing skill semantics.
- `CLAUDE.md` §First principle — the dev-facing constitution; the same idea
  as `principles.md`, for the contributor at work.

**Roadmap**

- `docs/todo.md` — the single home for all roadmap, TODO, and tech-debt
  (V1 / V2 / Meta sections). Remove an entry when it ships.

**Active specs & plans**

- `docs/plans/` — dated working specs and implementation plans for in-flight
  work (`YYYY-MM-DD-{topic}.md`), the same location the Codocu skills
  (`propose`, `apply`, `code-doc`, `doc-code`) read and write. Empty between
  cycles.

**History**

- `docs/archive/` — superseded dated specs/plans, kept as history, not
  deleted (e.g. specs rebuilt into the evergreen `docs/design/`). This repo
  is built *with* superpowers skills and not yet fully self-hosted on Codocu;
  adopting `docs/plans/` above is the first step of the "Rewrite `codocu.md`
  using Codocu" Meta item in `docs/todo.md`.

**Provenance & evidence**

- `docs/first_draft.md` — the original origin brain-dump, kept for
  provenance.
- `testing/` — long-term test reports (deliberately outside `docs/` — test
  evidence, not documentation); suites are dated directories.
