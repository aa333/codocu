# CLAUDE.md

Codocu (COde-as-a-DOCUment) is a Claude Code plugin — an LLM-agent workflow kit
that keeps code, plans, and docs coherent. This file governs how to work **on
this repo** (developing the plugin itself), not how the plugin behaves at
runtime.

## First principle

Clarity is the point of this project, not a finish applied to it. Every
artifact it produces or carries — skills, docs, plans, specs, scripts, and
messages to the user — is judged by whether its intended reader arrives at
understanding, not by whether it is complete or defensible. Accuracy is
necessary but it is not the target; understanding is. When the two conflict,
cut for understanding.

These are defects here, not style: encyclopedic terms, defensive
over-qualification, restating what the code already says, the answer buried
under preamble. Clarity comes from re-deriving the idea in plain words —
never from compressing or laundering someone else's dense prose, including
through Codocu itself.

**The gate.** Every spec and plan carries one line in its self-review:
*"Reader test: where would the intended reader get lost or bored? — named
and fixed."* Manual validation of any prose change checks the same. A
principle with no forced moment of checking decays; this is that moment.

## Where things live

- **Skills:** `skills/<name>/SKILL.md`, one directory per skill. The `name`
  frontmatter equals the directory name and is the `/codocu:<name>` invocation
  suffix.
- **Plugin manifest:** `.claude-plugin/plugin.json`. Its `name` is the namespace
  prefix.
- **Templates** copied verbatim by skills: `templates/`.
- **Roadmap / TODO:** `docs/todo.md` — all roadmap, TODO, and tech-debt
  entries go here.
- **Design:** `skills/codocu/references/` — the authoritative aspect specs
  ([`principles`](skills/codocu/references/principles.md),
  [`voice`](skills/codocu/references/voice.md),
  [`doc-standard`](skills/codocu/references/doc-standard.md)). Read the
  relevant one before changing skill semantics. These live inside the codocu
  skill so they're reachable at install time; they're also the contributor
  source of truth. The superseded dated specs/plans are kept as history in
  `docs/archive/`. `docs/design/build-skill/` holds deferred Track C notes
  (not loaded at runtime).

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

Manual commits by owner

## Documentation

`codocu.md` is a must read.
This repository should follow Codocu's rules and spirit in documentation.


## Local testing

- The `codocu:` namespace requires installation. Test via
  `claude --plugin-dir <repo path>`, then `/reload-plugins` after edits.
- Never copy `skills/` into a project to "test" it — that produces
  unnamespaced, colliding skills.
