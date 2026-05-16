# CLAUDE.md

Codocu (COde-as-a-DOCUment) is a Claude Code plugin — an LLM-agent workflow kit
that keeps code, plans, and docs coherent. This file governs how to work **on
this repo** (developing the plugin itself), not how the plugin behaves at
runtime.

## Where things live

- **Skills:** `skills/<name>/SKILL.md`, one directory per skill. The `name`
  frontmatter equals the directory name and is the `/codocu:<name>` invocation
  suffix.
- **Plugin manifest:** `.claude-plugin/plugin.json`. Its `name` is the namespace
  prefix.
- **Templates** copied verbatim by skills: `templates/`.
- **Roadmap / TODO:** `docs/todo.md` — all roadmap, TODO, and tech-debt
  entries go here.
- **Design spec:** `docs/superpowers/specs/2026-05-14-codocu-design.md` — the
  authoritative description of intended behavior. Read it before changing skill
  semantics. This path is transitional: these spec/plan files are fleeting
  scaffolding and will be migrated into Codocu's own docs structure as the
  plugin dogfoods itself (see the "Meta" item in `docs/todo.md`).

## Skill-authoring conventions

- `name` matches the directory and is the invocation suffix.
- `description` states *when* to use the skill (the trigger), not just what it
  does.
- Reference sibling skills as `/codocu:<name>`.
- Skills that change sync state must update the `> Codocu sync state:` line in
  the target project's `codocu.md` per the rules in the design spec.
- Keep instructions imperative and step-numbered; many small steps over a few
  large ones.

## Commit policy

No intermediate commits. Make one commit per logical unit of work, at the end.
Do not commit unless asked.

## Local testing

- The `codocu:` namespace requires installation. Test via
  `claude --plugin-dir <repo path>`, then `/reload-plugins` after edits.
- Never copy `skills/` into a project to "test" it — that produces
  unnamespaced, colliding skills.
- There is no marketplace config yet (`marketplace.json` is a pending
  `docs/todo.md` item). Do not document or suggest a marketplace install path
  until it exists.
