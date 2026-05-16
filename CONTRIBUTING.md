# Contributing to Codocu

Codocu is a Claude Code plugin. Skills live in `skills/`, one directory per
skill.

## Repo layout

```
.claude-plugin/plugin.json   # plugin manifest; "name" is the namespace prefix
skills/<name>/SKILL.md        # one skill per directory
templates/                    # files copied verbatim by skills (e.g. codocu.md seed)
docs/                         # long-term docs, roadmap (todo.md), plans (transitional — see CLAUDE.md)
```

## Local development & testing

The `codocu:` namespace only exists when the plugin is *installed*. Point Claude
Code at this repo:

```
claude --plugin-dir <path to this repo>
```

Skills are then invokable as `/codocu:init`, `/codocu:propose`, and so on. After
editing a `SKILL.md`, run `/reload-plugins` to pick up the change.

**Do not copy `skills/` into a test project.** Loose `SKILL.md` folders become
unnamespaced project skills (`/init`, not `/codocu:init`) and will collide with
the real plugin. Always test via `--plugin-dir`.

To test against a real project, run the `--plugin-dir` command from that
project's directory so the skills operate on its files.

## Adding or editing a skill

Create `skills/<name>/SKILL.md`:

```markdown
---
name: <name>            # must match the directory name
description: <when to use this skill — action-oriented, names the trigger>
---

# Codocu <Name>

<concise, step-numbered imperative instructions>
```

Conventions:

- `name` matches the directory; together they form the `/codocu:<name>`
  invocation.
- `description` states *when* to reach for the skill, not just what it does — it
  is the trigger text.
- Reference sibling skills by their namespaced form, e.g. suggest
  `/codocu:fold` at the end of a flow that produced a plan.
- Skills that change sync state must update the `> Codocu sync state:` line in
  the target project's `codocu.md` per the rules in the design spec.
- Keep instructions tight and step-numbered. Prefer many small steps over a few
  large ones.

## Roadmap

See [docs/todo.md](docs/todo.md) for V1 and V2 items.
