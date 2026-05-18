---
name: fold
description: "Archive completed plans and sync any docs they touched. Also invokable as /codocu:sync. Run at the end of a feature or when you want to wrap up in-progress work."
---

# Codocu — Fold

A plan's work is done (or being set down for now) and the record needs to
catch up. Verify what shipped, bring the docs along, archive the plan. Also
reachable as `/codocu:sync`.

_You own this project's code/doc coherence — talk about the project and the next move, never about this skill's own steps, defaults, modes, or mechanics. Write every doc, plan, and brief for a busy reader: lead with the answer, say it once, cut anything that just restates the code._

Read `codocu.md` first — it defines this project's doc layout and fold
behavior, and it's authoritative. Whatever it says is the convention here;
there's no "standard" to compare it against.

## Which plan

Look at the plans directory.

- Nothing there → there's nothing to fold; say so and stop.
- One plan → name it, confirm it's the one to fold, proceed.
- Several → list them with their goals, ask which; offer to walk all of them.

## Verify it actually shipped

Don't trust the checkboxes. For each step the plan treats as done, confirm
the change is really in the code. On this project in particular, plans have
been executed without ticking boxes at all — so judge by code and git
history, not by `[ ]`/`[x]`. If something marked done isn't there, surface
it before going further — never paper over it:

> "The plan counts X as done but I don't see it in the code. Re-do it, drop
> it, or skip?"

## Unfinished work

For steps that aren't done, `codocu.md`'s fold settings say how this project
wants them handled — follow that. If it's silent, ask the user per item
rather than guessing. The usual moves: move them into the project's tech-debt
record, carve them into a fresh trimmed plan (same goal, only the remaining
steps), or note them in the archive and leave them. Whichever applies, the
mechanics are the project's convention from `codocu.md`, not a fixed recipe.

## Bring the docs along

Update long-term docs only where the work genuinely warrants it. When a doc
is touched or newly warranted, it follows the long-term doc standard: an
orientation map — what the area is, its place in the system, its public
contract, its direction — holding nothing an internal-only refactor would
change. A decision earns a line only when the reason isn't obvious from the
code, an alternative was weighed and dropped, an external constraint forced
it, or an absence was deliberate; otherwise the code already says it — leave
the docs alone. (Canonical statement: the codocu skill's
`references/doc-standard.md`.)

Small, clear updates: show the change, write it on approval. Larger ones:
show the diff and get an explicit yes first.

## Archive and mark state

Move the plan into the archive directory. Then set `codocu.md`'s state line:

```
> Codocu sync state: Synced
```

A finished fold means this plan's work is verified and the docs it touched
agree with the code. Other active plans describe intended future work — that
is still Synced, not a desync. (Code mid-implementation that contradicts the
docs is a different situation, surfaced by `/codocu` — not decided here.)

## Close out

Tell the user what landed: plan archived, docs updated, anything moved to
tech debt or split into a new plan, and anything the verification turned up.
