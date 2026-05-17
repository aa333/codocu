# Codocu Deep-Drill Cost Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the `/codocu` router skill so the accepted deep drill is cost-aware, plan-gated, and read-only — cutting the $5.83 one-shot drill while keeping the claimed-complete≠done catch.

**Architecture:** Progressive-disclosure split of `skills/codocu/SKILL.md` into a lean entry plus two on-demand reference files (`deep-drill.md`, `conflict-resolution.md`). The drill protocol reuses the cheap orientation brief, detects change with git + filesystem + docs (git non-exclusive), classifies a complexity tier, discloses cost, and for sizable repos presents (never writes) a triaged drill plan. Validated by the existing dirty-`neph` fixture methodology (iter-03), not unit tests — this is a prompt/skill-authoring change.

**Tech Stack:** Claude Code plugin skills (Markdown only), PowerShell state-guard harness (`testing/neph-state-guard.ps1`), rubric scoring in a separate session.

**Commit policy (overrides writing-plans' frequent-commits default):** CLAUDE.md mandates *no intermediate commits* — one commit per logical unit at the end, and only when the user asks. Do **not** commit per task. Task 7 is the single, user-gated commit/tag step.

---

## File Structure

- **Create** `skills/codocu/references/conflict-resolution.md` — Case-4 resolution machinery, moved verbatim from `SKILL.md` with a context header. Loaded only when resolving a both-sides conflict.
- **Create** `skills/codocu/references/deep-drill.md` — the cost-aware read-only drill protocol. Loaded only when the user accepts the drill.
- **Modify** `skills/codocu/SKILL.md` — slim to lean entry: read signals, read-only orientation (now emits a reusable brief + offer/stop), present findings, triage, two reference trigger lines. Case-4 body removed (relocated).
- **Modify** `templates/codocu.md` — add optional "Deep drill settings" section so projects can tune tier thresholds.
- **Modify** `testing/report-template.md` — replace the old 13-pt rubric with the new criteria.
- **Test artifacts (Task 6)** — `testing/transcripts/iter-03.md`, `testing/report-iter-03.md`, status-log row, codocu git tag `test-iter-03`.

---

### Task 1: Create `references/conflict-resolution.md` (verbatim relocation)

**Files:**
- Create: `skills/codocu/references/conflict-resolution.md`

- [ ] **Step 1: Create the file with this exact content**

````markdown
# Codocu — Case 4 Conflict Resolution

Loaded by `/codocu` only when resolving a both-sides conflict (Case 4): both
code and docs have uncommitted changes and there is no active plan in
`docs/plans/`, or the user says "things are a mess".

If `codocu.md` exists, update its sync state marker: find the line beginning
with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`.
If it does not exist, skip this (you are in read-only orientation) — do not
create the file; note that `/codocu:init` is required to persist sync state.

Walk through the conflicts area by area:
> "In [area], the docs say [X] and the code does [Y]. Which is the intended truth?"

Record the user's answers. Once all areas are resolved, write a resolution plan:

```markdown
# Resolution Plan

**Goal:** Bring code and docs into sync

## Steps

- [ ] [area 1]: update [code/docs] to match [docs/code]
- [ ] [area 2]: ...
```

Save to `docs/plans/YYYY-MM-DD-resolution.md`.

Implement per plan. Suggest `/codocu:fold` when done.
````

- [ ] **Step 2: Verify the file matches the original Case-4 logic**

Read `skills/codocu/references/conflict-resolution.md` and confirm the sync-marker rule, the per-area question, the resolution-plan template, and the save path are byte-identical to the current `SKILL.md` "Case 4" section (only the header paragraph is new). No behavior changed — relocation only.

---

### Task 2: Create `references/deep-drill.md` (the cost-aware protocol)

**Files:**
- Create: `skills/codocu/references/deep-drill.md`

- [ ] **Step 1: Create the file with this exact content**

````markdown
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
   plans.
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
````

- [ ] **Step 2: Verify against the spec**

Read `skills/codocu/references/deep-drill.md` and confirm every spec §4 element is present: orientation-brief reuse (§0), git-non-exclusive detection (§1), tier table with the v0 thresholds (§2), cost disclosure (§3), two-anchor model + archived-default-excluded (§4), scoped-diff/no-default-exec/API-rename check (§5), triaged plan with triage order (§6), never-writes/persist-gated (§7). List any missing element and add it.

---

### Task 3: Slim `skills/codocu/SKILL.md` to the lean entry

**Files:**
- Modify: `skills/codocu/SKILL.md` (full rewrite — replace entire file)

- [ ] **Step 1: Replace the entire file with this exact content**

````markdown
---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads signals and guides you to the right action.
---

# Codocu Router

Figure out where things stand and what to do next.

## Read signals

Gather these quickly — no full project scan:

1. **`codocu.md`**: does it exist?
   - **Exists** → continue with the steps below.
   - **Missing** → the project is uninitialized. Ask the user which they want,
     and do nothing else until they answer:
     > "No `codocu.md` here — this project isn't initialized. I can either
     > **(a)** run a read-only orientation now (inspect git + docs, report
     > what I find, suggest next steps — writes nothing), or **(b)** run
     > `/codocu:init` first to set up `codocu.md`, then orient. Which?"
     - **(a)** → follow "Read-only orientation" below.
     - **(b)** → stop; tell the user to run `/codocu:init`.

2. **Active plans**: list files in `docs/plans/` — any in progress?

3. **Git** (if available): `git status` — what files have uncommitted changes?
   - Only `.md` files → hint: docs are ahead, consider `:doc-code`
   - Only code files → hint: code is ahead, consider `:code-doc`
   - Both → check active plans first (see conflict section below)

## Read-only orientation

Enter this mode when the user asks for analysis only, or when `codocu.md` is
absent and the user chose option (a) above. In this mode you **write nothing**
— no `codocu.md`, no sync marker, no plan, no code, no docs.

1. Gather the signals above. Use more than git: also note untracked/new files
   and modified docs, since git alone misses untracked refactors.
2. State which it is, with reasoning:
   - **Dirty** — both code and docs/plans changed or contradict each other.
   - **Desynced** — one side changed, the other is internally coherent.
   - **Synced** — code and docs agree (pending future-work plans stay Synced).
3. Produce a compact **orientation brief** (keep it in your reply; a later
   deep drill reuses this instead of re-deriving):
   - **changed-surface**: modified / added / deleted code, key renames
     (old→new path/identifier map), from git *and* untracked files;
   - **docs/plans claims**: homebrew docs, openspec changes, and plan
     checkbox / "done" status — flag any unit that marks work complete;
   - **disagreements**: area by area, where the two sides diverge.
4. Offer — but do **not** perform — a deeper drill-down, and the next actions
   (`/codocu:init` to persist state and enable resolution, or a targeted
   resolution flow). State that the drill is read-only and may be sizable.
5. Stop. Do not write anything or begin resolution until the user explicitly
   asks and the project is initialized.

**If the user accepts the deep drill:** read
`skills/codocu/references/deep-drill.md` and follow it. Do this **only** on
explicit accept — it is the expensive path.

## Present findings

Tell the user what you found. Be concise:
> "Here's what I see: [uncommitted code changes in X, Y] and [active plan: Z].
> What would you like to do?"

If signals point clearly to one action (e.g. only code changed, no active
plans), suggest it directly and ask for confirmation.

If there is an active plan and uncommitted code changes, that is normal
mid-feature state — suggest `/codocu:apply` to continue the plan rather than
entering conflict resolution.

## Case 4 — both sides changed (conflict)

If both code and docs have uncommitted changes AND there is no active plan in
`docs/plans/` (or the user says "things are a mess"), this is a conflict that
needs resolution. Read `skills/codocu/references/conflict-resolution.md` and
follow it. Do this **only** when actually resolving such a conflict.

## No conflicts — triage

If no conflicts but user isn't sure what to do:

- Active plan + uncommitted code changes → suggest `/codocu:apply` to continue
  the plan (this is normal mid-feature state, not a conflict)
- Active plan exists → suggest `/codocu:apply` to continue it
- No active plan, project is clean → suggest `/codocu:propose` for something new
- No git → ask: "What changed recently? Docs, code, or both?"
````

- [ ] **Step 2: Verify the slimming is faithful**

Read `skills/codocu/SKILL.md` and confirm: read signals + the (a)/(b) ask are unchanged; read-only orientation now has the brief (step 3) and the accept→`references/deep-drill.md` trigger; the Case-4 section is now a trigger to `references/conflict-resolution.md` (no inline resolution machinery); triage section unchanged. Confirm no behavior was lost — only relocated and the brief added.

---

### Task 4: Add optional drill settings to the codocu.md template

**Files:**
- Modify: `templates/codocu.md`

- [ ] **Step 1: Insert a new section before `## Additional notes`**

Find:

```markdown
## Additional notes

Add any project-specific conventions here. The agent reads this file at the start
of every /codocu invocation.
```

Replace with:

```markdown
## Deep drill settings (optional)

Controls when `/codocu`'s deep drill runs inline vs. produces a triaged plan
vs. hands off. Defaults (used if this section is absent):
- Inline: ≤10 changed code files and ≤500 changed lines and ≤1
  completion-claiming plan.
- Plan-gated: anything larger — disclose cost, present a triaged drill plan,
  don't auto-run the heavy audit.
- Hand-off: >150 changed files or >10k changed lines — out of scope; recommend
  an external harness.
Archived plans are excluded from the drill unless you explicitly ask for
"deep bookkeeping". Tune the numbers here in plain language; the agent
interprets them.

## Additional notes

Add any project-specific conventions here. The agent reads this file at the start
of every /codocu invocation.
```

- [ ] **Step 2: Verify**

Read `templates/codocu.md`; confirm the new section is present, the defaults match `references/deep-drill.md` §2 exactly, and `## Additional notes` is intact below it.

---

### Task 5: Replace the test rubric in the report template

**Files:**
- Modify: `testing/report-template.md`

- [ ] **Step 1: Replace the `## Score` table**

Find the block from `## Score` through the line `| **Total** | **13** |  |  |` and replace the whole block with:

```markdown
## Score

Criteria are authoritative; point weights are a test-setup detail — assign
weights when filling iter-NN.

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty |  |  |
| Complexity assessment correct | classified tier matches the fixture's true size (neph = Plan-gated) |  |  |
| Cost disclosed | user told size/cost before any heavy work |  |  |
| Sound triaged plan | correct triage order, scoped targets, no whole-repo sweep, archived plans not pulled in by default |  |  |
| Claimed-complete≠done caught | archetypes→strategy divergence surfaces (priority metric) |  |  |
| Public-API field-rename caught | ProfileData `status_label`→`member_status_str` / `status`→`member_status` |  |  |
| Read-only verify PASS | state-guard fingerprint unchanged; nothing written |  |  |
```

- [ ] **Step 2: Verify**

Read `testing/report-template.md`; confirm the old 6-row/13-pt table is gone, the 7 new criteria are present, and the surrounding template sections (header, Prompt used, What the agent did, Defects, Skill change) are untouched.

---

### Task 6: Run iter-03 (integration test — the real validation)

This is the project's test methodology, not unit tests. Read-only on `neph`; the interactive fresh-session run is **user-driven** per the runbook — be explicit about that boundary, do not fake it.

**Files:**
- Produce: `testing/transcripts/iter-03.md`, `testing/report-iter-03.md`

- [ ] **Step 1: Snapshot the fixture (agent runs — read-only on neph)**

Run: `powershell C:\repos\codocu\testing\neph-state-guard.ps1 snapshot`
Expected: `Snapshot OK` (72 tracked, 22 untracked). If counts differ, stop and report — the fixture drifted.

- [ ] **Step 2: Clear neph auto-memory (isolation)**

Delete the contents of `C:\Users\arzgi\.claude\projects\C--repos-bots-neph\memory\` so the tested agent can't read memory a prior iteration wrote. Confirm empty.

- [ ] **Step 3: Hand the user the exact run block (user executes — agent cannot drive an interactive `claude` session faithfully)**

Tell the user to run, from `C:\repos\bots\neph`:
`claude --model opus --plugin-dir C:\repos\codocu`

Turn 1 (verbatim — the hardened iter-01/02 prompt):
> /codocu Analyze the current state of this repository - code vs plans vs docs - and report what you find. INITIAL ANALYSIS ONLY: do not modify or create any file (including codocu.md), do not run codocu:init, do not create a plan. When you've reported, stop.

Turn 2 (verbatim — the new de-leaked prompt from the spec):
> Yes — perform that deeper drill-down now. Still READ-ONLY: do not modify or create any file (including codocu.md), do not run codocu:init. When you've reported, stop.

Worst-case sub-run (separate fresh session, same Turn 1, then this barer Turn 2):
> Yes, do the drill.

Ask the user to paste the full assistant output of each run into `testing/transcripts/iter-03.md`, then exit the session.

- [ ] **Step 4: Verify read-only (agent runs after the user's run)**

Run: `powershell C:\repos\codocu\testing\neph-state-guard.ps1 verify`
- `VERIFY PASS` → valid run.
- `VERIFY FAIL` → record the defect in `testing/report-iter-03.md`, then run `powershell C:\repos\codocu\testing\neph-state-guard.ps1 restore -Execute` to recover the fixture.

- [ ] **Step 5: Score in a separate session (no self-grading)**

Copy `testing/report-template.md` to `testing/report-iter-03.md` and fill it from the transcript **in a different session or by hand** — do not grade your own run. Add a status-log row to `testing/session-test-dirty-orientation-01.md` (Iter 03, tag `test-iter-03`, score, read-only, key observations: cost vs the $5.83 anti-pattern reference, did the triaged plan still surface archetypes→strategy and the ProfileData rename).

---

### Task 7: Single commit + tag (only if the user asks)

CLAUDE.md: no intermediate commits; one commit per logical unit at the end; do not commit unless asked. The user drives git/tagging per the test methodology.

**Files:**
- Modify: git history (only on explicit user request)

- [ ] **Step 1: Ask whether to commit**

Ask the user: commit the skill restructure + spec + plan + TODO + template/report changes as one logical unit now, and tag `test-iter-03` in the codocu repo? Proceed only on an explicit yes.

- [ ] **Step 2: If yes, commit on a branch and tag**

If on `master`, create a branch first. Stage the changed files (`skills/codocu/`, `docs/superpowers/specs/`, `docs/superpowers/plans/`, `TODO.md`, `templates/codocu.md`, `testing/report-template.md`, iter-03 artifacts) and make one commit. Then `git tag test-iter-03`. End the commit message with the required `Co-Authored-By` trailer.

---

## Self-Review

**1. Spec coverage:**
- Progressive-disclosure split (spec §1) → Tasks 1, 2, 3. ✓
- Git non-exclusive detection (§2) → Task 2 §1 + Task 3 orientation step 1. ✓
- Two-anchor model, archived-default-excluded (§3/§4) → Task 2 §4. ✓
- Drill protocol assess→disclose→tier + API-rename check (§4) → Task 2 §2/§3/§5. ✓
- Read-only never-writes / inline-plan / persist-gated (§6) → Task 2 §0/§7. ✓
- Triage priority (§5) → Task 2 §6. ✓
- Configurable thresholds (§7) → Task 2 §2 + Task 4. ✓
- Validation: de-leaked prompt, new rubric, fresh baseline (Validation) → Task 5, Task 6. ✓
- Out-of-scope/logged gaps → already in TODO.md (done pre-plan). ✓
No spec requirement is without a task.

**2. Placeholder scan:** Full file contents are embedded in Tasks 1–3; exact find/replace blocks in Tasks 4–5; exact commands and verbatim prompts in Task 6. The `[area]` / `[tier N area]` tokens inside the embedded skill markdown are intentional skill template literals (the agent fills them at runtime), not plan placeholders. No "TBD/TODO/similar to Task N".

**3. Type consistency:** Path `skills/codocu/references/deep-drill.md` and `skills/codocu/references/conflict-resolution.md` are referenced identically in the SKILL.md triggers (Task 3) and created at those exact paths (Tasks 1–2). Tier names (Inline / Plan-gated / Hand-off) and threshold numbers are identical between `references/deep-drill.md` §2 (Task 2) and `templates/codocu.md` (Task 4). Rubric criteria in Task 5 match the spec Validation list.

No issues found.

---

## Notes / risks carried from the spec

- Threshold numbers are provisional; iter-03 may move them — they live in one place (`deep-drill.md` §2, mirrored in the template) so a wrong default is a one-line edit, not a redesign.
- Path-resolution for `references/` under plugin-cache loading is unverified; Task 3 step 2 / Task 6 are where a wrong relative path would surface. If the agent can't resolve `skills/codocu/references/...`, fall back to the loader's injected skill base dir convention during execution.
- Task 6's fresh-session run is human-in-the-loop by methodology design; the agent does the read-only snapshot/verify and prepares everything else.
