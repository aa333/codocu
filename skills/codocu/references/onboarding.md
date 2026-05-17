# Codocu — Onboarding (the /codocu setup branch)

Loaded by `/codocu` **only when the onboarding branch is taken** — the user
asked to set Codocu up, or an uninitialized repo is being adopted and the
user wants to proceed. Until then orientation stays read-only; this branch is
the only place `codocu.md` gets written, and only on an explicit go-ahead.

## 0. Reuse orientation, don't re-derive

Use the bearings orientation already took (codocu.md present? docs? plans?
working tree). Don't re-scan. If invoked cold (via `/codocu:init`), take one
bounded look first — counts and paths only — enough to classify the repo and
propose good defaults.

## 1. Never clobber

If `codocu.md` already exists it is authoritative. Do not overwrite it.
Orient, then offer to revise specific conventions — the same questions below,
pre-filled from the current file — and write only the lines the user
approves.

## 2. Classify the repo (cheap)

From the reused bearings, place the repo:

- **Bare / minimal** — little or no code, no docs worth migrating.
- **Brownfield, compatible docs** — docs exist and roughly fit a
  supplements-the-code shape.
- **Incompatible docs** — docs re-tell the code in full (SDD-style) or are
  scattered/contradictory.
- **Dirty** — code and docs both in motion / contradictory.

## 3. The always-asked convention core

Ask these three regardless of repo state — they are intent, not derivable
from any repo. Each carries a codocu-leaning default and an explicit "take
the default, revisit later" escape, so adoption is never blocked on a
decision:

1. **ActualDoc granularity** — module / system / feature / hybrid.
   Default: module-level, decompose on demand.
2. **What else to document** — a tech-debt/TODO catchall (`TD-XXXX`
   cross-linked from inline code TODOs) / nothing beyond ActualDocs / "I'll
   note other conventions myself". Default: tech-debt catchall on. (This
   choice only — not an open-ended artifact-design session.)
3. **Fold behavior for incomplete plans** — move to tech-debt / carve a
   trimmed new plan / ask each time. Default: ask each time.

In a bare/minimal repo, ask only these three, propose the complete filled
`codocu.md` (§5), get one confirmation, and you're done.

## 4. Repo-conditional questions

Only when the signal exists:

- **Existing-docs stance** — only if docs exist (§6).
- **Dirty / incompatible** — do not interview. Surface what orientation
  found and the migration size, and route to `/codocu:propose` -> plan;
  `codocu.md` is written as part of that plan, not here.

## 5. Fill `codocu.md` from the skeleton

Start from `templates/codocu.md` (the bare skeleton: the reserved
`> Codocu sync state: TBD` marker plus empty sections). Fill, in voice, from
the answers — opinionated, lean, supplements-the-code (Living-Documentation
shaped, not SDD):

- **Docs structure** <- granularity answer. Default: module-level
  `docs/actual/`, decompose on demand. State that long-term docs follow the
  project's going-forward doc standard — **reference** the WHAT-summary bound
  (the design spec / `code-doc` / `fold`); do not restate it here.
  `codocu.md` carries conventions, not the bound's definition.
- **What else to document** <- Q2. Default: `docs/tech-debt-todo.md`,
  `TD-XXXX` codes cross-linked from inline `// TODO TD-XXXX` comments.
- **Fold settings** <- Q3. Default: ask per incomplete item.
- **Existing-docs note** <- stance (§6), written **only if docs exist**.
- Leave **Additional notes** for the user.

Seed the sync-state marker `TBD` (real state is unknown until first
assessed). Write only on the user's go-ahead.

### CLAUDE.md single reference

If a `CLAUDE.md` (or `AGENTS.md`) duplicates doc paths/conventions that now
live in `codocu.md`, offer — don't do it automatically, never clobber — to
replace those with a single pointer to `codocu.md`, so conventions live in
one place.

## 6. Existing-docs stance (only if docs exist)

Ask the user's stance toward the existing docs. The stance is a **rollout
strategy**; it does not change the doc standard:

- **Tailor** — `codocu.md` points at the existing layout/locations as-is;
  the going-forward standard applies to new/touched docs only; legacy docs
  are left as they are (accepted friction). No migration.
- **In-between** — same, with intent to converge: as areas are touched via
  normal `/codocu:code-doc` / `/codocu:fold`, their docs are brought to the
  standard. Gradual.
- **Full-migrate** — bring existing docs to the standard now. Size it with
  the same judgment `/codocu:code-doc` uses (files, doc coverage, area
  familiarity; ask the user when unsure). Anything past a trivial touch goes
  through `/codocu:propose` -> plan, executed and folded like any plan — not
  done inline here.

Record the chosen stance as a one-line note in `codocu.md` (stance + pointer
to legacy locations). Bare repo: this section never runs.

The standard itself stays invariant under every stance. A plugin-level
developer dial — *Existing-docs stance authority* in `docs/tuning.md` — can
change that; by default it does not, and this branch never offers to weaken
the standard.

## 7. Close out

Tell the user what landed: `codocu.md` written (or the specific revised
lines), the conventions chosen, any CLAUDE.md pointer change, and — for an
incompatible/dirty repo — that the next step is `/codocu:propose` for the
migration plan. Then stop.
