# Codocu — Deep Drill (cost-aware state analysis)

Loaded by `/codocu` **only when the user has accepted the offered deep drill**.
This is the expensive path. Result of this procedure is the report of code/doc sync state with overall analysis and per-area report.

## 0. Reuse, don't re-derive

Use the **orientation brief** already in this conversation (changed-surface +
rename map, docs/plans completion claims, per-area disagreements). 
If invoked without a prior orientation, run one compact bounded pass first (`git status`, list `docs/plans/`, list docs) — counts and paths only, no whole-file reads.

## 1. Detect changes with more than git

Git is a good tool, but not the only one:
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
| **Inline** | ≤10 changed code files **and** ≤500 changed lines **and** ≤1 completion-claiming plan | §5 scoped drill directly, then report |
| **Plan-gated** | anything above Inline | produce a triaged drill plan and present it — do **not** run the heavy audit unprompted |
| **Hand-off** | >150 changed files **or** >10k changed lines **or** no VCS and hundreds of source files to cold-scan | Explicitly state that costs may be prohibitive. If agreed upon, build a plan of further deeper analysis, using iterative approach - pick axis to break analysis to phases (layers, systems, modules, areas, whatever makes sense), prepare higher order plan with those phases, each phase producing separate deep-analysis plan to persist the long process. There's no definitive guide for this step yet |

## 3. Anchors (what to actually check)

Two anchors, strongest bound first:

1. **Changed-surface (always).** For each changed/new code module and each
   public API object it defines, reconcile it against any doc that references
   that module or identifier. This works with zero plans. Also judge each doc
   against the doc standard (`references/doc-standard.md`): too much detail
   (re-telling the code) or no orientation map is a divergence in its own
   right, and so is a doc a busy developer would give up on. Report each
   separately — don't fold them into the code-vs-doc finding.
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
  report that you did.
- **Deterministic public-API field-rename check:** for any changed file
  defining a returned/serialized API object, enumerate added / removed /
  renamed public fields from the diff and cross-check each against long-term
  docs. Report renamed public surface as a distinct divergence.

## 6. The triaged drill plan (Plan-gated only)

Present a plan in Codocu plan format. Order items by triage priority:

1. VCS changes + active plans (current work; sync-critical)
2. README / context files (`CLAUDE.md`, `AGENTS.md`, etc.)
3. Long-term docs modified < 1 month old
4. Archived plans — opt-in deep bookkeeping, windowed (lowest)

```markdown
# Drill Plan

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
`/codocu:init` + an explicit go-ahead 