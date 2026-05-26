## Orientation

**Repo:** `C:\repos\_codocu_scratch\bare` — **bare/minimal**, not yet set up for Codocu.

- **Code:** one untracked file, `src/main.py` (a trivial Python `greet`/`main`). No commits yet.
- **Docs:** none. No `docs/`, no `codocu.md`, no `CLAUDE.md`/`AGENTS.md`.
- **State:** Synced by default — nothing to reconcile, nothing to migrate.

Because this is a bare repo, onboarding only needs the three convention-core questions. You asked to **take every default** and **not write anything**, so below is the complete `codocu.md` exactly as it *would* be written — no file created, no questions asked. Defaults applied:

| Question | Default chosen |
|---|---|
| Long-term docs granularity | Module-level under `docs/actual/`, decompose on demand |
| What else to document | Tech-debt/TODO catchall on — `docs/tech-debt-todo.md`, `TD-XXXX` codes |
| Fold behavior for incomplete plans | Ask each time |

No existing-docs stance (no docs exist). No `CLAUDE.md` pointer change (none present). One tailoring: TODO cross-link comments use Python syntax (`# TODO TD-XXXX`) since the project is Python.

---

## Proposed `codocu.md` (not written)

```markdown
# Codocu

> Codocu sync state: TBD

<!-- Filled by Codocu onboarding (/codocu:init, or the onboarding branch of
/codocu). Defines this project's documentation conventions; read at the start
of every /codocu invocation. Edit freely. -->

## Docs structure

Long-term docs live under `docs/actual/`, one document per module, mirroring
the code layout. Start coarse: a module gets a single long-term doc; decompose
into system- or feature-level docs on demand, only when a module grows enough
that one doc stops being a useful orientation map.

Long-term docs are an orientation layer that *supplements* the code — they
explain what a module is for and how its pieces fit, not a line-by-line
re-telling. They follow the project's going-forward doc standard (the
WHAT-summary bound defined by the design spec / `/codocu:code-doc` /
`/codocu:fold`); that bound is authoritative and is not restated here.

## What else to document

Tech-debt and deferred work are tracked in `docs/tech-debt-todo.md`. Each
item gets a stable `TD-XXXX` code. Inline code TODOs that defer real work
reference their entry — Python: `# TODO TD-XXXX: <short note>` — so the
catchall and the code stay cross-linked.

## Fold settings

When folding a plan that still has incomplete items, ask each time how to
handle the remainder (move to tech-debt, carve a trimmed follow-up plan, or
something else). No automatic disposition.

## Additional notes

(Left for you.)
```

---

Nothing was written. To make this real, the next step is to run `/codocu:init` (or `/codocu`) without the analysis-only constraint and approve — that writes this `codocu.md` and unlocks the resolution flows. From a bare repo, the natural follow-on is `/codocu:propose` to start the first feature with docs and code tracked together.
