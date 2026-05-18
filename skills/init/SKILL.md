---
name: init
description: Set up Codocu in this project. Alias into the onboarding branch of /codocu.
---

**VOICE**: Omit details of this skill's own steps, defaults, modes, or mechanics. When reasoning internally, internalize skill's statements and let them co-exist with a common sense, so when you state your reasoning, let it be less skill-centric and more "I think that...". When writing every doc, plan, and brief, keep in mind that you are writing for a busy, mentally exhausted reader: use plain language, focus on key points, add enough context to ensure clarity. Adept Feynman style of prose, be clear, conscise, simple. You are co-owner of this repo, helpful companion, mentor and guide.


# Codocu Init

User asked to set Codocu up, or an uninitialized repo is being adopted and the
user wants to proceed. 

## 1. Check `codocu.md` and orientation

If `codocu.md` already exists, consider it authoritative. Do not overwrite it.
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

1. **Long-term documents granularity** — module / system / feature / hybrid.
   Default: module-level, decompose on demand.
2. **What else to document** — some options to offer, each one on/off
- a tech-debt catchall file (`TD-short-issue-id`)
- a todo list
- user's own conventions
3. **Fold behavior for incomplete plans** — move to tech-debt / carve a
   trimmed new plan / ask each time. Default: ask each time.

In a bare/minimal repo, ask only these three, propose the complete filled
`codocu.md`, get confirmation, and you're done.

## 4. Repo-conditional questions

Only when the signal exists:

- **Existing-docs stance** — only if docs exist (§6).
- **Dirty / incompatible** — do not interview. Surface what orientation
  found and the migration size, and route to `/codocu:propose` -> plan;
  `codocu.md` is written as part of that reconciliation plan, not here.

## 5. Fill `codocu.md` from the skeleton

Start from `templates/codocu.md` (the bare skeleton: the reserved
`> Codocu sync state: TBD` marker plus empty sections). Fill, in voice, from
the answers — opinionated, lean, supplements-the-code (Living-Documentation
shaped, not SDD):

- **Docs structure** <- granularity answer. Default: module-level
  `docs/actual/`, decompose on demand. State that long-term docs follow the
  project's going-forward doc standard — point to where it's defined (the
  codocu skill's `references/doc-standard.md`); don't restate it in
  `codocu.md`, which carries conventions, not the standard's definition.
  Include a `docs/inbox/` line: the intake where other agents drop long-term
  docs for Codocu to fold (`/codocu:fold`).
- **What else to document** <- Q2. Default: `docs/tech-debt-todo.md`,
  `TD-XXXX` codes cross-linked from inline `// TODO TD-XXXX` comments.
- **Fold settings** <- Q3. Default: ask per incomplete item.
- **Subagent guidelines** <- the template default, kept as-is. It's a stable
  Codocu convention, not interview-derived; don't expand it per project.
- **Existing-docs note** <- stance (§6), written **only if docs exist**.
- Leave **Additional notes** for the user.

Seed the sync-state marker `TBD` (real state is unknown until first
assessed). Write only on the user's go-ahead.

Then make the inbox convention functional, not just documented: create
`docs/inbox/.gitkeep` in the target project and — if it has git — add a
`.gitignore` rule ignoring `docs/inbox/*` except `.gitkeep` and `*.defer.md`.

### CLAUDE.md reference

Insert a strong incentive to consult with `codocu.md` regarding documentation conventions in `CLAUDE.md` (or `AGENTS.md`) 

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
