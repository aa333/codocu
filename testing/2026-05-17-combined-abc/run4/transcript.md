## Orientation

**Repo:** brownfield, compatible docs — and tiny. One module, two docs, nothing committed yet.

**Changed surface (all untracked):**
- `src/app.py` — `Queue` (`push`/`pop`) + `run_worker(queue)`; a tiny in-process task queue.
- `docs/overview.md` — what it is + the *why* (chose an in-process list over Redis deliberately). Good orientation-shaped doc.
- `docs/api-notes.md` — restates the three public signatures and their behavior.

**Sync state:** code and docs **agree** — `pop()` on an empty list does raise `IndexError`, `run_worker` does drain and return a count. Everything is just uncommitted/untracked, internally coherent. Not dirty, not desynced.

**One caveat:** `docs/api-notes.md` drifts slightly *over* the bound — it re-narrates signatures the docstrings already carry. `overview.md` is the keeper (it explains intent a reader can't get from the code). Not incompatible enough to need migration — a Tailor stance handles it.

No `CLAUDE.md`/`AGENTS.md` at root, so there's nothing to de-duplicate into a single pointer.

## Defaults applied (as requested)

| Question | Default taken |
|---|---|
| ActualDoc granularity | Module-level, decompose on demand |
| What else to document | Tech-debt catchall on (`docs/tech-debt-todo.md`, `TD-XXXX`) |
| Fold for incomplete plans | Ask each time |
| Existing-docs stance | **Tailor** (no migration; standard applies to new/touched docs only) |

## One-line stance note

> **Existing-docs stance: Tailor** — `codocu.md` points at `docs/` (`overview.md`, `api-notes.md`) as-is; the going-forward doc standard applies to new or touched docs only; legacy docs are left as accepted friction (no migration).

## Proposed `codocu.md` (complete — not written)

```markdown
# Codocu

> Codocu sync state: TBD

<!-- Filled by Codocu onboarding (/codocu:init, or the onboarding branch of
/codocu). Defines this project's documentation conventions; read at the start
of every /codocu invocation. Edit freely. -->

## Docs structure

Long-term docs live in `docs/` (flat layout, kept as-is):

- `docs/overview.md` — what the service is and *why* it's built this way.
- `docs/api-notes.md` — public-surface notes.

Going forward: **one ActualDoc per module**, decomposed only when a module
grows enough to warrant it. New or touched docs follow the project's
going-forward doc standard — the WHAT-summary bound enforced by
`/codocu:code-doc` and `/codocu:fold`: orient the reader and explain *why*;
don't re-narrate code they can read.

Existing-docs stance: **Tailor** — point at `docs/` as-is; the standard
applies to new/touched docs only; `overview.md` and `api-notes.md` are left
as accepted friction (no migration). Revisit for convergence later if wanted.

## What else to document

Tech-debt / TODO catchall: `docs/tech-debt-todo.md`. Each entry gets a
`TD-XXXX` code, cross-linked from code with `# TODO TD-XXXX` comments.
Nothing else beyond ActualDocs unless added here later.

## Fold settings

Incomplete plan items at fold time: **ask each time** — move to tech-debt or
carve a trimmed follow-up plan, decided per item, not by a blanket rule.

## Additional notes

(yours)
```

Per your instruction, **nothing was written** — no `codocu.md`, no docs, no code. This is analysis/proposal only.

When you want to proceed, the next step is the explicit go-ahead to write this `codocu.md` (the only thing onboarding persists). After that, `docs/api-notes.md` would naturally come to standard the next time that area is touched — no migration needed under the Tailor stance.
