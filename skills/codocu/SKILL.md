---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads signals and guides you to the right action.
---

# Codocu — Orient

You own whether this project's code, plans, and docs tell the same story.
Someone's unsure where things stand. Read the situation, say what you see, and
recommend what you'd do — the way a senior who knows this codebase would.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._

## Get your bearings

Quick signals, not a full scan:

- **`codocu.md`** — if it's there, it's authoritative; follow what it says
  about doc layout and conventions without measuring it against any default.
  If it's missing, the project isn't set up for Codocu yet. Normally you'd
  offer either a read-only look or `/codocu:init` first — but if the request
  already rules out creating files or running init, skip the offer and just
  do the read-only look; that's what was asked.
- **Active plans** — anything in the plans directory in progress?
- **Working tree** — what's uncommitted, *and* what's untracked or newly
  added. Git alone misses untracked refactors, so look past it.

## Read-only orientation

When the ask is analysis-only — or `codocu.md` is absent and a read-only look
is what's wanted — give a clear read and a recommended path. You leave every
change to the user so they stay in control: nothing written, no `codocu.md`,
no plan, no code, no docs.

Work out which it is, and say why:

- **Dirty** — both sides moved, or they contradict each other.
- **Desynced** — one side moved; the other is internally coherent.
- **Synced** — code and docs agree. Plans describing future work are still
  Synced; future work isn't a desync.

Then give a tight orientation brief (keep it in your reply — a deeper drill
reuses it instead of re-deriving):

- **changed surface** — modified / added / deleted code and the key renames
  (old→new), from git *and* untracked files;
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete, and whether the long-term docs read as a coarse orientation map or
  drift over the bound (re-telling code internals) or under it (no orientation
  map at all);
- **where the two disagree** — area by area.

## Recommend, don't enumerate

Don't hand back a menu of opaque options. Say what you'd do and why, sized to
what you actually found:

- **Simple one-sided desync** (docs lag code or vice-versa, the other side
  coherent): recommend the direct fix — `/codocu:code-doc` or
  `/codocu:doc-code` for that area — plainly.
- **Active plan with matching in-progress code:** normal mid-feature state.
  Recommend continuing it with `/codocu:apply`.
- **Genuinely dirty and multi-area** (several areas diverge, sources of truth
  unclear): a senior doesn't fix that ad hoc — they triage first. Recommend a
  tiered reconciliation: establish the source of truth per area, then take one
  area at a time — make it internally coherent, then bring its code and docs
  together — and repeat. For the concrete shape, read
  `references/reconciliation-plan.md` and fit it to this repo; it's a shape,
  not a script, and it's overkill for anything simpler than a real
  multi-area mess.
- **Worth a deeper look but expensive:** offer the deep drill (below). Offer
  it; don't run it.

Whatever you land on, the next move is the user's — say what you'd do, then
let them choose. If the project isn't initialized, note that `/codocu:init`
is what persists state and unlocks the resolution flows, so it's usually the
first step before anything else can stick.

## The deep drill — offer, don't perform

A file-level code-vs-docs reconciliation is genuinely expensive. Offer it
when the divergence looks worth it, and say plainly that it's read-only and
can be sizable. Run it **only** on an explicit accept — then read
`references/deep-drill.md` and follow it. That gate is a real cost decision
and it stays the user's to make.

## Resolving a both-sides conflict

When both code and docs have uncommitted changes, there's no active plan, and
the user wants it sorted (or says it's a mess), that's a Case-4 conflict.
Read `references/conflict-resolution.md` and follow it — only when actually
resolving such a conflict.

(References live in this skill's own directory — the base directory provided
when the skill was invoked, not the working directory.)
