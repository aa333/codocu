# Codocu — Doc Standard (design)

Why a long-term doc in a Codocu project is shaped the way it is. The
operational rule the agent loads at runtime is the `codocu` skill's
`references/doc-standard.md`; this is the reasoning behind it.

## The bet

[Code is the source of truth](principles.md). So a long-term doc earns its
keep only by *orienting* a reader to an area — not by re-describing code
that will change underneath it. A doc that re-tells the code rots the first
time someone refactors without touching it. A doc with no orientation map
fails its one job: a new reader still can't place the area. Both are real
divergences, not matters of style.

## The shape

A long-term doc is an orientation map: **purpose, place, public contract,
direction** — and nothing an internal-only refactor would change. A decision
earns a sentence only when the reason isn't obvious from the code, an
alternative was weighed and dropped, an external constraint forced it, or an
absence was deliberate; otherwise the code already says it. The operational
checklist is the runtime reference and is not restated here.

## Reader economy applies

Scope is not enough. A doc the reader abandons has failed, however accurate;
the [voice](voice.md) house rule and the first principle govern the read.

## Where it lives

- **This file** — the design rationale (the why).
- **`skills/codocu/references/doc-standard.md`** — the operational rule
  `code-doc`, `fold`, and the deep drill apply (the what-to-do). `code-doc`
  and `fold` carry a short synced statement of it because a skill loads
  references only from its own directory.
