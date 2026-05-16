# Codocu — Reconciliation Plan (a shape, not a script)

Read this only when orientation found a **genuinely dirty, multi-area** repo
and you're recommending how to climb out of it. For a simple one-sided
desync, don't use this — recommend the direct `/codocu:code-doc` or
`/codocu:doc-code` fix instead. This is a shape to fit to the project in
front of you, not a checklist to recite: adapt the areas, order, and depth
to what's actually there, and drop anything that doesn't apply.

The senior approach to a messy tree: don't fix it ad hoc. Triage, then take
it one area at a time.

**Triage and set the source of truth.** Break the divergence into areas — by
module, system, or feature, whatever the project's natural seams are. For
each area, establish which side is authoritative right now: the code, the
docs, or neither-yet (needs a decision). Get the user's call where it's
genuinely ambiguous; don't invent a truth.

**Per area, repeat:**
- Make the area internally coherent first. Before syncing code to docs, fix
  what's wrong *within* each side: code errors, contradictory or stale doc
  passages, broken formatting, dead references. An incoherent side can't be
  a sync target.
- Then bring code and docs together for that area, in the direction triage
  decided.
- Move to the next area. Earlier areas stay fixed — you're not re-opening
  them.

Order areas by what's most load-bearing or most diverged first, unless the
user has a reason to sequence differently.

**Persisting it.** If the project is initialized, this becomes an ordinary
Codocu plan in the plans directory — then `/codocu:apply` works it at any
pace and `/codocu:fold` closes it, like any other plan. If it isn't
initialized, say so: `/codocu:init` first, since nothing persists without
it. Presenting the shape is read-only; writing it down is a separate,
deliberate step the user asks for.
