# Codocu — What a long-term doc is

The single statement of the long-term doc standard. Read it when you're
about to write or judge a long-term doc.

A long-term doc is an **orientation map**, not a retelling of the code. It
covers four things and stops:

- **Purpose** — what this area is for.
- **Place** — where it sits in the system, what it talks to.
- **Public contract** — what callers can rely on.
- **Direction** — where it's heading, and any deliberate non-goals.

Nothing an internal-only refactor would change belongs in it — that detail
is the code's job, and the code is always the truth. So a doc fails this
two ways:

- **Too much detail** — it re-tells the code's internals; it rots the first
  time someone refactors without touching it.
- **No orientation map** — a new reader still can't place the area; the doc
  exists but doesn't do its one job.

When judging existing docs, each failure is a divergence in its own right.
One exception: a `docs/inbox/` draft is raw pre-standard input awaiting a
fold, not a divergence to flag. Bringing it to this standard *is* the fold;
holding it to the standard beforehand mistakes the input for the output.

## When a decision earns a line

Most of the "why" is already in the code. A decision earns a sentence in
the doc only when one of these holds:

- the reason isn't obvious from reading the code,
- an alternative was weighed and dropped,
- an external constraint forced it, or
- an absence was deliberate — something a reader would expect, left out on
  purpose.

If none hold, the code already says it — write nothing.
