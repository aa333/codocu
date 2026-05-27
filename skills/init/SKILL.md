---
name: init
description: Scaffold this project for Codocu. Create `codocu.md` (and optionally `docs/tech-debt.md`) from the plugin templates and wire `codocu.md` into `CLAUDE.md` so every Claude session loads the conventions. Run once per project; safe to re-invoke (no-ops if already inited).
---

> You own this project's code/doc coherence. Talk about the project and the next
> move — never about your own steps, defaults, modes, or mechanics. Write every
> doc, plan, and brief for a busy, tired reader: lead with the answer, say it
> once, cut anything that just restates the code.

## What init does

Reads `templates/codocu.md` from this skill's `templates/` directory, shows the user the conventions it's about to set up, asks once for the go-ahead (with any corrections and any meta-comment choices folded in), then writes the resolved files into the target repo and wires the CLAUDE.md import.

Writes (in order):

1. `codocu.md` at the repo root — the project's doc conventions file.
2. Any additional choices user picked and voiced
3. `@codocu.md` line appended to `CLAUDE.md` — imports `codocu.md` into every
   Claude session in this repo. If `CLAUDE.md` doesn't exist, create it with
   `@codocu.md` as its only content. If the line is already there, leave it.

After the writes land, offer the orientation handoff (below).

## The `codocu:init` comment convention

The template carries instructions for init in HTML comments of the form:

```
<!-- codocu:init <instruction> -->
```

Read every such comment in the template before showing the welcome. Each one is an instruction for init to act on — typically a question to roll into the welcome ("ask if this section should be included") or a default-handling note. Execute the instruction, then strip the comment from the final written file. Present choice dialog for optional sections. 

Plain HTML comments (no `codocu:init` prefix) are normal template comments — leave them in the written file.

## The welcome

Before writing, describe the conventions in plain language — not the template's headings. The user should hear *what's actually going to govern their docs*, not a TOC.

Cover, in roughly this order:

- Where docs live (the `docs/` layout the template carries).
- Short descriptions and rationale for optional sections.
- The backlink marker usage, if the template carries one.
- How `/codocu:fold` will treat incomplete plans (per the template's fold
  settings).
- That `codocu.md` will be wired into `CLAUDE.md` via `@codocu.md`.

Ask for confirmation and/or any corrections. 
If user asks for non-trivial explanations or principal reasoning, delegate to `/codocu:codocu` core skill.

## Already inited

If `codocu.md` already exists in the target repo, do not overwrite. Tell the user the repo is already inited and that re-running won't touch their `codocu.md`; point them at the file to edit conventions directly. Then stop.

If `codocu.md` is missing but `CLAUDE.md` already contains `@codocu.md`, that's a stale import — write the templates and leave `CLAUDE.md` alone.

If any other docs you intend to write already exist, ask user how to proceed with each (or with the whole batch if there are e.g. dozens of archived specs). Only handle trivial requests (overwrite, skip, delete). if user requests user requests require analyzing or editing the contents, offer partial basic init with further delegation to `/codocu:codocu`. 

## Orientation handoff

Right after the writes land, offer one optional move: "Want a doc-system orientation pass? I can read the repo and suggest how to proceed."

If the user accepts, invoke `/codocu` with this prompt:

```
Orient around this repo and recommend how to proceed. If existing documentation exists, analyze and propose how it may fit into the proposed structure. If no structured documentation can be found, suggest initial documentation pass (or a bigger structured plan if codebase is large).
```

Init's job ends with the handoff. If the user declines, init ends after the writes.
