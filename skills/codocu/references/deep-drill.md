# Codocu — Deep Drill (read-only, cost-aware)

Loaded by `/codocu` **only when the user has accepted the offered deep drill**.
This is the expensive path. It stays **read-only**: write nothing — no file,
no `codocu.md`, no plan on disk. You may *present* a plan in your reply; you do
not save it.

## 0. Reuse, don't re-derive

Use the **orientation brief** already in this conversation (changed-surface +
rename map, docs/plans completion claims, per-area disagreements). Do not
re-run the full inventory. If invoked without a prior orientation, run one
compact bounded pass first (`git status`, list `docs/plans/`, list docs) —
counts and paths only, no whole-file reads.

## 1. Detect changes with more than git

Git is one signal, not the only one:
- **git** (when tracked): `git diff --stat`, `git status` — fast path.
- **filesystem**: untracked / new files; file mtimes vs the `codocu.md` sync
  marker or doc mtimes — catches untracked refactors git-list reasoning misses.
- **docs**: discover docs by location/content (not a hardcoded path); note
  which reference changed code identifiers.

## 2. Assess complexity (cheap) and classify the tier

From cheap signals only (counts and `--stat`, no file reads), compute:
- changed code files (tracked-modified + untracked-new),
- changed doc files,
- total changed lines (diff insertions + deletions; estimate for untracked),
- number of plans/specs that **claim completion** (active only — see §4).

Classify (defaults; a project may override these in `codocu.md` under
"Deep drill settings"):

| Tier | Trigger | What you do |
|---|---|---|
| **Inline** | ≤10 changed code files **and** ≤500 changed lines **and** ≤1 completion-claiming plan | §5 scoped drill directly, then §7 report |
| **Plan-gated** | anything above Inline | §3 disclose, then produce a triaged drill plan (§6) and present it — do **not** run the heavy audit unprompted |
| **Hand-off** | >150 changed files **or** >10k changed lines **or** no VCS and hundreds of source files to cold-scan | decline; present a short triage skeleton only; recommend an external/whole-repo harness — out of Codocu's scope |

## 3. Disclose cost before heavy work

Before doing anything expensive, tell the user the size in plain terms:
> "This drill covers ~N changed code files / ~M doc files / ~L diff lines and
> K completion-claiming plans — a <tier> drill. <what that means for cost>."

## 4. Anchors (what to actually check)

Two anchors, strongest bound first:

1. **Changed-surface (always).** For each changed/new code module and each
   public API object it defines, reconcile it against any doc that references
   that module or identifier. This is the universal bound and works with zero
   plans. Also judge the doc itself against the WHAT-summary bound: a doc that
   re-tells code internals is over the bound; one with no coarse orientation
   map (purpose, place, public contract, direction) is under it — report
   either as a distinct divergence.
2. **Completion-claim (when present — a sharpening).** *On top of* the
   changed-surface, for each **active** plan/spec/prose that asserts
   completion (`[x]` **or** "done/complete/shipped/archived"), check whether
   the code actually delivers what it marks complete. Treat prose "done" as a
   weaker signal than a checkbox, not authoritative.

**Archived plans are excluded by default.** Revisiting them is opt-in "deep
bookkeeping" and, even then, windowed (e.g. archived within 30 days or the N
most recent) — never all of them.

## 5. Scoped checking rules

- Read **diffs**, not whole files: `git diff -- <path>`; for new/untracked
  files, a bounded read of just that file.
- Scope to the changed surface / claimed unit, not the repo. No recursive
  whole-repo reads. One bounded follow-up read is allowed only when a concrete
  divergence requires it.
- **Do not execute code by default.** Only when a behavioral claim cannot be
  judged from the diff, run a single named, bounded validation command — and
  report that you did (read-only nuance).
- **Deterministic public-API field-rename check:** for any changed file
  defining a returned/serialized API object, enumerate added / removed /
  renamed public fields from the diff and cross-check each against long-term
  docs. Report renamed public surface as a distinct divergence.

## 6. The triaged drill plan (Plan-gated only)

Present (do not save) a plan in Codocu plan format. Order items by triage
priority:

1. VCS changes + active plans (current work; sync-critical)
2. README / context files (`CLAUDE.md`, `AGENTS.md`, etc.)
3. Long-term docs modified < 1 month old
4. Archived plans — opt-in deep bookkeeping, windowed (lowest)

```markdown
# Drill Plan (proposed — not saved)

**Goal:** Verify code vs docs/plans coherence; surface claimed-complete≠done.

## Steps
- [ ] [tier 1 area]: check <scoped paths / claimed unit> — read diffs only
- [ ] [tier 2 area]: ...
```

Each item names its scoped target so it can be executed independently and at
any pace by `/codocu:apply` or any agent.

## 7. Report and stop

Report per checked unit: claimed vs actual, with an explicit "doc says X /
code says Y" line for every renamed/diverged identifier, and a verdict on
whether each completion-claiming unit is genuinely complete. For Plan-gated,
the deliverable is the triaged plan + cost disclosure; offer to persist it via
`/codocu:init` + an explicit go-ahead (persisting is a separate, gated step —
the drill itself never writes). Stop. Still read-only.
