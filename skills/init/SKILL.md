---
name: init
description: Scaffold this project for Codocu. Create `codocu.md` and `docs/tech-debt.md` from the plugin templates and wire `codocu.md` into `CLAUDE.md` so every Claude session loads the conventions. Run once per project; safe to re-invoke (no-ops if already inited).
---

> You own this project's code/doc coherence. Talk about the project and the next
> move — never about your own steps, defaults, modes, or mechanics. Write every
> doc, plan, and brief for a busy, tired reader: lead with the answer, say it
> once, cut anything that just restates the code.

## What init does

Reads `templates/codocu.md` and `templates/tech-debt.md` from the plugin repo, shows the user the conventions it's about to set up, asks once for the go-ahead (with any corrections they want folded in), then makes three writes in the target repo:

1. `codocu.md` at the repo root — the project's doc conventions file, free-form, edited by the user from here on.
2. `docs/tech-debt.md` — single catchall for deferred items, with the entry format already in place.
3. `@codocu.md` line appended to `CLAUDE.md` — imports `codocu.md` into every Claude session in this repo. If `CLAUDE.md` doesn't exist, create it with `@codocu.md` as its only content. If the line is already there, leave it.

## The welcome

Before writing, describe the conventions in plain language — not the template's headings. The user should hear *what's actually going to govern their docs*, not a TOC.

Cover, in roughly this order:

- Where docs live (the `docs/` layout the template carries, including the inbox).
- The tech-debt catchall and its entry format.
- The breadcrumb marker the template picks as default.
- How `/codocu:fold` will treat archives and the inbox.
- That `codocu.md` will be wired into `CLAUDE.md` via `@codocu.md` so every session sees it.

Then list the writes (the three above) and ask once: OK to proceed, or any corrections first?

If the user names corrections — different folder names, a different breadcrumb form, drop a section, swap the tech-debt format — apply them to the in-memory templates before writing. Don't bargain or ask follow-ups; take what they said and proceed.

## Already inited

If `codocu.md` already exists in the target repo, do not overwrite. Tell the user the repo is already inited and that re-running won't touch their `codocu.md`; point them at the file to edit conventions directly. Then stop.

If `codocu.md` is missing but `CLAUDE.md` already contains `@codocu.md`, that's a stale import — write the templates and leave `CLAUDE.md` alone.

If `docs/tech-debt.md` already exists, leave it alone too — the user has started using it.
