# Codocu Skill Voice & Constriction Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Codocu skills read and behave as a senior engineer who owns code/doc coherence — eliminating scaffolding leak and defensive over-compliance — while preserving every locked safety/cost guarantee.

**Architecture:** This is prose/prompt engineering, not code. Deliverables are Markdown skill files plus one new on-demand reference and one developer-time tuning registry. "Tests" are runs of the existing subagent-scored dirty-repo harness (`testing/tools/state-guard.ps1` + a separate-session rubric), extended with a voice/partnership dimension. The highest-risk skill (`codocu` orientation) is rewritten and harness-validated *before* the cheaper changes roll out suite-wide (the staging gate).

**Tech Stack:** Markdown skill files (`skills/<name>/SKILL.md`); PowerShell harness (`pwsh testing/tools/state-guard.ps1`); headless `claude --plugin-dir`; separate-session rubric scoring.

**Spec:** `docs/superpowers/specs/2026-05-17-codocu-skill-voice-redesign-design.md`

> **COMMIT POLICY — read before executing.** This repo's `CLAUDE.md` mandates: *"No intermediate commits. Make one commit per logical unit of work, at the end. Do not commit unless asked."* This **overrides** the writing-plans default of per-task commits. There are intentionally **no per-task commit steps** below. A single commit (covering the already-applied sync-state hotfix + this entire redesign) happens in the final task, **only when the user explicitly asks**. Do not `git commit` between tasks.

> **Fixture path convention.** The harness operates on an external anonymized fixture repo, referred to as `<target-repo>` (the engineer substitutes their real path via the script's `-Repo` parameter). `<codocu-repo>` is this plugin checkout. These two tokens are an established harness convention (see `testing/README.md`), not plan placeholders.

> **Out of scope (do not do):** strengthening the §5 field-rename check; the bare-assent behavioral cliff; folding the now-complete `2026-05-16-codocu-deep-drill-cost-redesign.md` plan (bookkeeping tracked in `docs/todo.md`). The sync-state hotfix (`fold` Step 5 + `init` TBD seed) is already applied — Task 9 (fold rewrite) must preserve its semantics.

---

## Reused house rule (used verbatim in several tasks)

This exact line is the in-skill voice/anti-leak standard. Where a task says "insert the house rule," insert **this exact text** (it is repeated in each task so tasks can be executed out of order):

```
_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

---

## Task 1: Build the validation instrument (test-first)

Create the scoring instrument *before* changing any skill, so the rewritten orientation can be measured against it. This is the failing-test analog: the current skills are expected to fail the new voice criteria.

**Files:**
- Create: `testing/2026-05-17-skill-voice-redesign/setup.md`
- Create: `testing/2026-05-17-skill-voice-redesign/report-template-voice.md`

- [ ] **Step 1: Create the suite setup file**

Create `testing/2026-05-17-skill-voice-redesign/setup.md` with this exact content:

```markdown
# Skill voice & constriction redesign — test setup

Delta from the base methodology in
`testing/2026-05-16-dirty-repo-exploration/setup.md`. Same fixture, same
`testing/tools/state-guard.ps1` snapshot/verify harness, same read-only
contract, same no-self-grading rule (score in a separate session).

## What this suite verifies

That the rewritten skills (a) keep every functional behavior the
2026-05-16 suite scored, and (b) read and behave as a senior partner:
no scaffolding leak, a sized recommendation instead of an opaque menu,
hard constraints honored without defensive narration, and no
over-application of the reconciliation-plan shape to a simple desync.

## Fixture, runbook, prerequisites

Identical to `2026-05-16-dirty-repo-exploration/setup.md` (fixture,
snapshot/verify, the verbatim read-only test prompt, the locked decision
that the pre-emptive prompt skips the (a)/(b) ask). Reuse it as-is.

## Scoring

Score from the transcript in a separate session against
`report-template-voice.md` in this directory (the 7 functional criteria
from `testing/tools/report-template.md` plus the voice/partnership
criteria). Save filled reports as `run<N>/result.md`.
```

- [ ] **Step 2: Create the extended report template**

Create `testing/2026-05-17-skill-voice-redesign/report-template-voice.md` with this exact content:

```markdown
# Test Report — Skill Voice Redesign — Run NN

- **Date:** YYYY-MM-DD
- **Plugin state:** <git-sha or tag>
- **Model:** Opus
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS | FAIL (if FAIL, restore run? yes/no)
- **Skill state under test:** <e.g. orientation-rewritten / full-rollout>

## Prompt used

> <exact prompt given>

## What the agent did

<3–6 lines>

## Functional score (retained — must not regress)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty |  |  |
| Claimed-complete≠done caught | archetypes→strategy divergence surfaces |  |  |
| Read-only verify PASS | state-guard fingerprint unchanged |  |  |

## Voice / partnership score (new)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| No scaffolding leak | no internal step numbers, no "per the skill" / "I default to", no internal mode names, no defaults re-declaration, no "standard vs non-standard structure" editorializing |  |  |
| Sized recommendation | recommends a specific path with reasoning, sized to findings — NOT an opaque unranked option-dump |  |  |
| Constraints honored, not narrated | stays read-only / opt-in-drill without defensively announcing compliance ("I'll do none of these unasked") |  |  |
| Reads as senior partner | tone is a colleague reasoning, not a script reciter |  |  |
| Over-fit guard | on a simple one-sided desync, recommends the direct fix; does NOT over-apply the reconciliation-plan shape |  |  |

## Defects / observations

-

## Change for next run

-
```

---

## Task 2: Baseline run — confirm current skills fail the voice criteria

Proves the instrument discriminates (test-first: the test must fail before the change).

**Files:**
- Create: `testing/2026-05-17-skill-voice-redesign/run1/transcript.md`
- Create: `testing/2026-05-17-skill-voice-redesign/run1/result.md`
- Create: `testing/2026-05-17-skill-voice-redesign/run1/setup-changes.md`

- [ ] **Step 1: Snapshot the fixture (read-only)**

Run: `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
Expected: `Snapshot OK` (72 tracked, 22 untracked).

- [ ] **Step 2: Run current orientation headless**

In a fresh session, cwd = `<target-repo>`:
`claude --model opus --plugin-dir <codocu-repo>`
Paste the verbatim read-only prompt from `2026-05-16-dirty-repo-exploration/setup.md` §"Per-iteration runbook" step 3.
Capture full assistant output to `testing/2026-05-17-skill-voice-redesign/run1/transcript.md`. Record `setup-changes.md` = "baseline: skills unchanged (pre-redesign), plugin state <git-sha>".

- [ ] **Step 3: Verify read-only**

Run: `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
Expected: `VERIFY PASS`. On `VERIFY FAIL`, record the defect and run `pwsh testing/tools/state-guard.ps1 restore -Repo <target-repo> -Execute`.

- [ ] **Step 4: Score in a SEPARATE session (no self-grading)**

In a different session, score `run1/transcript.md` against `testing/2026-05-17-skill-voice-redesign/report-template-voice.md`; save as `run1/result.md`.
Expected: functional criteria PASS; **voice criteria FAIL** (current orientation dumps opaque options + leaks scaffolding). If voice criteria do *not* fail, the instrument is too lenient — tighten the pass conditions in `report-template-voice.md` and re-score before proceeding.

---

## Task 3: Deep-rewrite `skills/codocu/SKILL.md` (orientation, in voice)

**Files:**
- Modify (full replace): `skills/codocu/SKILL.md`

- [ ] **Step 1: Replace the entire file with this exact content**

```markdown
---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads signals and guides you to the right action.
---

# Codocu — Orient

You own whether this project's code, plans, and docs tell the same story.
Someone's unsure where things stand. Read the situation, say what you see, and
recommend what you'd do — the way a senior who knows this codebase would.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._

## Get your bearings

Quick signals, not a full scan:

- **`codocu.md`** — if it's there, it's authoritative; follow what it says
  about doc layout and conventions without measuring it against any default.
  If it's missing, the project isn't set up for Codocu yet. Normally you'd
  offer either a read-only look or `/codocu:init` first — but if the request
  already rules out creating files or running init, skip the offer and just
  do the read-only look; that's what was asked.
- **Active plans** — anything in the plans directory in progress?
- **Working tree** — what's uncommitted, *and* what's untracked or newly
  added. Git alone misses untracked refactors, so look past it.

## Read-only orientation

When the ask is analysis-only — or `codocu.md` is absent and a read-only look
is what's wanted — give a clear read and a recommended path. You leave every
change to the user so they stay in control: nothing written, no `codocu.md`,
no plan, no code, no docs.

Work out which it is, and say why:

- **Dirty** — both sides moved, or they contradict each other.
- **Desynced** — one side moved; the other is internally coherent.
- **Synced** — code and docs agree. Plans describing future work are still
  Synced; future work isn't a desync.

Then give a tight orientation brief (keep it in your reply — a deeper drill
reuses it instead of re-deriving):

- **changed surface** — modified / added / deleted code and the key renames
  (old→new), from git *and* untracked files;
- **what the docs and plans claim** — homebrew docs, any spec/proposal
  formats present, and plan/"done" status; call out anything that marks work
  complete;
- **where the two disagree** — area by area.

## Recommend, don't enumerate

Don't hand back a menu of opaque options. Say what you'd do and why, sized to
what you actually found:

- **Simple one-sided desync** (docs lag code or vice-versa, the other side
  coherent): recommend the direct fix — `/codocu:code-doc` or
  `/codocu:doc-code` for that area — plainly.
- **Active plan with matching in-progress code:** normal mid-feature state.
  Recommend continuing it with `/codocu:apply`.
- **Genuinely dirty and multi-area** (several areas diverge, sources of truth
  unclear): a senior doesn't fix that ad hoc — they triage first. Recommend a
  tiered reconciliation: establish the source of truth per area, then take one
  area at a time — make it internally coherent, then bring its code and docs
  together — and repeat. For the concrete shape, read
  `references/reconciliation-plan.md` and fit it to this repo; it's a shape,
  not a script, and it's overkill for anything simpler than a real
  multi-area mess.
- **Worth a deeper look but expensive:** offer the deep drill (below). Offer
  it; don't run it.

Whatever you land on, the next move is the user's — say what you'd do, then
let them choose. If the project isn't initialized, note that `/codocu:init`
is what persists state and unlocks the resolution flows, so it's usually the
first step before anything else can stick.

## The deep drill — offer, don't perform

A file-level code-vs-docs reconciliation is genuinely expensive. Offer it
when the divergence looks worth it, and say plainly that it's read-only and
can be sizable. Run it **only** on an explicit accept — then read
`references/deep-drill.md` and follow it. That gate is a real cost decision
and it stays the user's to make.

## Resolving a both-sides conflict

When both code and docs have uncommitted changes, there's no active plan, and
the user wants it sorted (or says it's a mess), that's a Case-4 conflict.
Read `references/conflict-resolution.md` and follow it — only when actually
resolving such a conflict.

(References live in this skill's own directory — the base directory provided
when the skill was invoked, not the working directory.)
```

- [ ] **Step 2: Verify the locked constraints survived**

Read the file back and confirm all are present (positively framed is fine; the *guarantee* must be intact):
- read-only orientation writes nothing (no `codocu.md`/plan/code/docs);
- pre-emptive prompt → skip the (a)/(b) ask, orient directly;
- deep drill only on explicit accept; called "expensive"/"sizable"; `references/deep-drill.md` gated on accept;
- `references/conflict-resolution.md` gated on actual Case-4 resolution;
- no OpenSpec-specific terms hardcoded ("any spec/proposal formats present" is generic).
Expected: all present. If any is missing, fix inline before continuing.

---

## Task 4: Create `skills/codocu/references/reconciliation-plan.md`

**Files:**
- Create: `skills/codocu/references/reconciliation-plan.md`

- [ ] **Step 1: Create the file with this exact content**

```markdown
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
```

---

## Task 5: Staging gate — validate the rewritten orientation

The spec's load-bearing gate: orientation must pass voice criteria (and not regress functional) *before* the suite-wide rollout.

**Files:**
- Create: `testing/2026-05-17-skill-voice-redesign/run2/transcript.md`
- Create: `testing/2026-05-17-skill-voice-redesign/run2/result.md`
- Create: `testing/2026-05-17-skill-voice-redesign/run2/setup-changes.md`

- [ ] **Step 1: Snapshot**

Run: `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
Expected: `Snapshot OK` (72 tracked, 22 untracked).

- [ ] **Step 2: Run rewritten orientation headless**

Fresh session, cwd = `<target-repo>`: `claude --model opus --plugin-dir <codocu-repo>`. Paste the same verbatim read-only prompt as Task 2. Capture to `run2/transcript.md`. Record `run2/setup-changes.md` = "orientation rewritten (Task 3) + reconciliation-plan reference added (Task 4); fold/linear skills NOT yet changed".

- [ ] **Step 3: Verify read-only**

Run: `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
Expected: `VERIFY PASS`. On FAIL: record defect, `restore -Repo <target-repo> -Execute`, and treat the run as a defect to fix in Task 3 before re-running.

- [ ] **Step 4: Score in a SEPARATE session**

Score `run2/transcript.md` against `report-template-voice.md`; save as `run2/result.md`.
Expected: **all functional criteria PASS (no regression vs Task 2 baseline)** AND **all voice criteria PASS**.

- [ ] **Step 5: Gate decision**

If any functional criterion regressed or any voice criterion failed: revise `skills/codocu/SKILL.md` (Task 3) / `reconciliation-plan.md` (Task 4) per the `result.md` "Change for next run", and repeat Steps 1–4 (new run folder `run3`, etc.). **Do not start Task 6 until this run is a clean pass.**

---

## Task 6: Light-touch — `skills/propose/SKILL.md`

Apply the anti-leak + positive-framing standard. Exact edits only.

**Files:**
- Modify: `skills/propose/SKILL.md`

- [ ] **Step 1: Insert the house rule**

Find:
```
# Codocu Propose

Turn a new intent into an approved plan, ready to implement.
```
Replace with:
```
# Codocu Propose

Turn a new intent into an approved plan, ready to implement.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

- [ ] **Step 2: De-mechanize the sync-marker instruction**

Find:
```
Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`. `/codocu:fold` will restore this to `Synced` when the plan is archived.
```
Replace with:
```
Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.
```

- [ ] **Step 3: Reframe the CAPS prohibitions positively**

Find: `Check these signals quickly — do NOT do a full project scan:`
Replace with: `A couple of quick signals — no full project scan:`

Find: `Draft a **ProposalSummary** in the conversation — do NOT write it to disk:`
Replace with: `Draft a **ProposalSummary** in the conversation — it stays in the conversation, not on disk:`

- [ ] **Step 4: Verify**

Read the file back. Confirm: no `do NOT`/CAPS prohibitions remain; no "find the line… replace it" mechanic; house rule present; flow and the user-facing quoted prompts unchanged otherwise.

---

## Task 7: Light-touch — `skills/apply/SKILL.md`

**Files:**
- Modify: `skills/apply/SKILL.md`

- [ ] **Step 1: Insert the house rule**

Find:
```
# Codocu Apply

Pick up where a plan left off.
```
Replace with:
```
# Codocu Apply

Pick up where a plan left off.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

- [ ] **Step 2: De-mechanize the sync-marker instruction**

Find:
```
Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`. `/codocu:fold` will restore this to `Synced` when the plan is archived.
```
Replace with:
```
Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.
```

- [ ] **Step 3: Reframe the prohibition**

Find:
```
to the next. If a step cannot be completed, stop and report to the user — do not
  skip to the next plan.
```
Replace with:
```
to the next. If a step can't be completed, stop and report rather than skipping ahead.
```

- [ ] **Step 4: Verify**

Read back. Confirm: house rule present; sync-marker mechanic gone; no `do not`/CAPS prohibition; flow unchanged otherwise.

---

## Task 8: Light-touch — `skills/doc-code/SKILL.md`

**Files:**
- Modify: `skills/doc-code/SKILL.md`

- [ ] **Step 1: Insert the house rule**

Find:
```
# Codocu Doc-Code

The docs are the proposal. Write a plan and implement it.
```
Replace with:
```
# Codocu Doc-Code

The docs are the proposal. Write a plan and implement it.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

- [ ] **Step 2: De-mechanize the sync-marker instruction**

Find:
```
Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`. `/codocu:fold` will restore this to `Synced` when the plan is archived.
```
Replace with:
```
Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.
```

- [ ] **Step 3: Verify**

Read back. Confirm house rule present, sync-marker mechanic gone, flow unchanged otherwise.

---

## Task 9: Light-touch — `skills/code-doc/SKILL.md`

**Files:**
- Modify: `skills/code-doc/SKILL.md`

- [ ] **Step 1: Insert the house rule**

Find:
```
# Codocu Code-Doc

Read what changed in code and bring the docs up to date.
```
Replace with:
```
# Codocu Code-Doc

Read what changed in code and bring the docs up to date.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

- [ ] **Step 2: De-mechanize the small-path sync-marker instruction**

Find:
```
Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Synced`. Done — no plan, no fold needed.
```
Replace with:
```
Set `codocu.md`'s state line to `> Codocu sync state: Synced`. Done — no plan, no fold needed.
```

- [ ] **Step 3: De-mechanize the large-path sync-marker instruction**

Find:
```
Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`. `/codocu:fold` will restore this to `Synced` when the plan is archived.
```
Replace with:
```
Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.
```

- [ ] **Step 4: Verify**

Read back. Confirm house rule present, both sync-marker mechanics gone, flow unchanged otherwise.

---

## Task 10: Light-touch — `skills/init/SKILL.md`

`init` is genuinely procedural; keep its numbered authoring structure (it does not get narrated when the house rule is honored). Only add the house rule and confirm the hotfixed `TBD` seed is intact.

**Files:**
- Modify: `skills/init/SKILL.md`

- [ ] **Step 1: Insert the house rule**

Find:
```
# Codocu Init

Set up Codocu in the current project.
```
Replace with:
```
# Codocu Init

Set up Codocu in the current project.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._
```

- [ ] **Step 2: Confirm the hotfix is intact**

Read the file. Confirm the seeded block still contains `   > Codocu sync state: TBD` (NOT `Synced`). If it says `Synced`, change it back to `TBD` — that is the already-applied hotfix and must not regress.

---

## Task 11: Deep-rewrite `skills/fold/SKILL.md` (in voice, preserving the hotfix semantics)

This supersedes the hotfixed file. The replacement **must keep** the corrected sync-state semantics (unconditional `Synced` on a successful fold; active plans are still Synced) and the no-trust-checkboxes verification.

**Files:**
- Modify (full replace): `skills/fold/SKILL.md`

- [ ] **Step 1: Replace the entire file with this exact content**

```markdown
---
name: fold
description: "Archive completed plans and sync any docs they touched. Also invokable as /codocu:sync. Run at the end of a feature or when you want to wrap up in-progress work."
---

# Codocu — Fold

A plan's work is done (or being set down for now) and the record needs to
catch up. Verify what shipped, bring the docs along, archive the plan. Also
reachable as `/codocu:sync`.

_Operate as the engineer who owns this project's code/doc coherence. Talk about the project and what you'd do next — never about this skill's own steps, defaults, modes, or mechanics._

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

Update long-term docs only where the work genuinely warrants it. A decision
earns a doc line when the reason isn't obvious from the code, an alternative
was weighed and dropped, an external constraint forced it, or an absence was
deliberate. If none of that applies, the code already says it — leave the
docs alone. Small, clear updates: show the change, write it on approval.
Larger ones: show the diff and get an explicit yes first.

## Archive and mark state

Move the plan into the archive directory. Then set `codocu.md`'s state line:

\`\`\`
> Codocu sync state: Synced
\`\`\`

A finished fold means this plan's work is verified and the docs it touched
agree with the code. Other active plans describe intended future work — that
is still Synced, not a desync. (Code mid-implementation that contradicts the
docs is a different situation, surfaced by `/codocu` — not decided here.)

## Close out

Tell the user what landed: plan archived, docs updated, anything moved to
tech debt or split into a new plan, and anything the verification turned up.
```

Note: in Step 1 the inner fenced block shown as `\`\`\`` must be written as a literal triple-backtick fence in the actual file (it is escaped here only so this plan's own code block doesn't terminate early).

- [ ] **Step 2: Verify the hotfix semantics and constraints survived**

Read back. Confirm: state line is set **unconditionally** to `Synced` on a successful fold (no "if plans remain, leave unchanged" branch); the "active plans are still Synced" legibility note is present; no-trust-checkboxes verification is present; no internal step-number references; no "standard vs non-standard structure" editorializing.

---

## Task 12: Author `docs/tuning.md` (developer-time knob registry)

**Files:**
- Create: `docs/tuning.md`

- [ ] **Step 1: Create the file with this exact content**

```markdown
# Codocu — Behavioral Tuning Registry

Developer-facing. **Not read at runtime.** The skill prose is the source of
truth for behavior; this file is the map: every behavioral dial, its current
setting, and exactly where in the skill text that setting is expressed.

**The one rule:** retuning always goes through *edit here → propagate*.
Change the setting in this file, then run `/codocu:doc-code` on this repo to
carry the change into the skill-text locations listed for that dial. An
ad-hoc skill edit that skips this file silently desyncs the registry.

## Dials

### Voice intensity
How strongly the skills carry the senior-partner voice vs. plain procedure.
- **Setting:** Senior-partner (full).
- **Expressed in:** every `skills/*/SKILL.md` — the opening framing lines and
  the in-skill house rule ("Operate as the engineer who owns this project's
  code/doc coherence…"); most concentrated in `skills/codocu/SKILL.md` and
  `skills/fold/SKILL.md`.
- **Devalue:** flatten the opening framing toward neutral procedure; keep the
  house rule regardless — scaffolding leak is never desirable.

### Recommendation assertiveness
Whether orientation recommends a sized path or just reports options.
- **Setting:** Recommends (a sized path, then asks for the go-ahead).
- **Expressed in:** `skills/codocu/SKILL.md`, the "Recommend, don't
  enumerate" section.
- **Devalue:** soften "say what you'd do" toward "lay out the options"; do
  not revert to an opaque unranked menu — that was the original defect.

### Reconciliation-plan-shape weighting
How prominently orientation reaches for the tiered reconciliation plan.
- **Setting:** Default — recommended only for a genuinely dirty/multi-area
  repo; direct fix for a simple desync.
- **Expressed in:** `skills/codocu/SKILL.md` ("Recommend, don't enumerate",
  the dirty/multi-area bullet) and
  `skills/codocu/references/reconciliation-plan.md` (the adapt-don't-recite +
  not-for-simple-cases clause).
- **Strengthen:** widen the trigger toward multi-area-ish repos.
- **Devalue:** narrow the trigger to only the worst tangles.
- **Remove:** delete the dirty/multi-area bullet's reference pointer in
  `skills/codocu/SKILL.md` and delete
  `skills/codocu/references/reconciliation-plan.md`; orientation then
  recommends only per-area direct fixes.

## Adding a dial
When a new behavioral knob emerges, add a section here with: setting,
expressed-in locations, and the strengthen/devalue/remove directions — then
propagate.
```

---

## Task 13: Re-validate after rollout + locked-constraint guard

**Files:**
- Create: `testing/2026-05-17-skill-voice-redesign/run<N>/transcript.md` (next free N)
- Create: `testing/2026-05-17-skill-voice-redesign/run<N>/result.md`
- Create: `testing/2026-05-17-skill-voice-redesign/run<N>/setup-changes.md`
- Create: `testing/2026-05-17-skill-voice-redesign/summary.md`

- [ ] **Step 1: Snapshot**

Run: `pwsh testing/tools/state-guard.ps1 snapshot -Repo <target-repo>`
Expected: `Snapshot OK` (72 tracked, 22 untracked).

- [ ] **Step 2: Run headless with the full rollout in place**

Fresh session, cwd = `<target-repo>`: `claude --model opus --plugin-dir <codocu-repo>`. Same verbatim read-only prompt as Task 2. Capture to the new `run<N>/transcript.md`. `setup-changes.md` = "full rollout: orientation + fold deep-rewritten, 5 linear skills light-touched, tuning.md authored".

- [ ] **Step 3: Verify read-only**

Run: `pwsh testing/tools/state-guard.ps1 verify -Repo <target-repo>`
Expected: `VERIFY PASS`. On FAIL: record defect, `restore … -Execute`, fix the offending skill, re-run.

- [ ] **Step 4: Score in a SEPARATE session**

Score against `report-template-voice.md`; save as `run<N>/result.md`.
Expected: all functional criteria PASS (no regression) AND all voice criteria PASS.

- [ ] **Step 5: Run the locked-constraint guard checklist**

Manually inspect the final skill files and confirm each — record PASS/FAIL with the file:line evidence in `run<N>/result.md` under "Defects / observations":
1. `skills/codocu/SKILL.md` — read-only orientation still writes nothing (no codocu.md/plan/code/docs).
2. `skills/codocu/SKILL.md` — deep drill only on explicit accept; still called expensive/sizable; `references/deep-drill.md` gated on accept.
3. `skills/codocu/SKILL.md` — pre-emptive prompt still skips the (a)/(b) ask.
4. `skills/codocu/SKILL.md` + `references/reconciliation-plan.md` — no OpenSpec-specific hardcoding; detection generic.
5. `skills/fold/SKILL.md` — unconditional `Synced` on successful fold; active-plans-still-Synced note present.
6. `references/conflict-resolution.md` + `references/deep-drill.md` — unchanged (not in scope; confirm no accidental edits).
Any FAIL → fix the offending file and repeat Steps 1–5.

- [ ] **Step 6: Write the suite scoreboard**

Create `testing/2026-05-17-skill-voice-redesign/summary.md`: a status-log table (run, plugin state, functional score, voice score, read-only, headline) across run1 (baseline FAIL-voice), run2 (orientation gate), run<N> (full rollout), plus a short narrative and any open findings. Follow the shape of `testing/2026-05-16-dirty-repo-exploration/summary.md`.

---

## Task 14: Final commit (ONLY when the user asks)

Per `CLAUDE.md`, this is the single commit for the whole logical unit: the already-applied sync-state hotfix + this entire redesign. **Do not run this task until the user explicitly asks to commit.**

**Files:**
- Modify: `docs/todo.md` (close the feedback item)

- [ ] **Step 1: Update the TODO**

In `docs/todo.md`, under `## V1 todos`, find:
```
**Usage feedback**
see feedback-transcript.md
```
Replace with:
```
**Usage feedback** — addressed
Sync-state hotfix applied (`fold` unconditional Synced, `init` seeds TBD);
skill voice/constriction redesign implemented and harness-validated. See
`docs/superpowers/specs/2026-05-17-codocu-skill-voice-redesign-design.md` and
`testing/2026-05-17-skill-voice-redesign/summary.md`.
```

- [ ] **Step 2: Confirm scope with the user, then commit once**

Stage the skill changes, the new reference, `docs/tuning.md`, the spec, this plan, the new testing suite, and the `docs/todo.md` edit. Commit with a message summarizing "sync-state hotfix + skill voice/constriction redesign". Tag per the testing convention (`test-iter-NN` / next free N) if the user wants the score to map to an exact plugin state. Use the repo's commit trailer convention. Do not push unless asked.

---

## Self-Review

**1. Spec coverage:**
- Voice model — persona/anti-leak/constraints-as-standards/layered-recommendation → Tasks 3, 4, 6–12 (house rule + rewrites + tuning).
- Staged change surface (light-touch linear; deep rewrite codocu+fold; new reference) → Tasks 3,4,6–11.
- Sequencing (orientation rewritten + validated before suite-wide rollout) → Tasks 3→5 gate→6+.
- `tuning.md` knob registry, not runtime-read, retune workflow, one rule → Task 12.
- Locked constraints preserved → Task 3 Step 2, Task 11 Step 2, Task 13 Step 5.
- Validation: reuse harness, add voice dimension, subagent/separate-session scoring, baseline-fails-first → Tasks 1,2,5,13.
- Over-fit guard (in-prose + scored) → Task 4 content + voice rubric row (Task 1) + Task 13.
- All covered; no gaps.

**2. Placeholder scan:** No "TBD/TODO/handle edge cases". `<target-repo>`/`<codocu-repo>`/`run<N>` are documented harness conventions, not placeholders. All file content given verbatim. The fold Step 1 escaped-fence note is explicit, not a placeholder.

**3. Type/string consistency:** The house-rule string is byte-identical across Tasks 3, 6–12. The sync-marker replacement phrasing is identical across Tasks 6–9. `report-template-voice.md`, `skills/codocu/references/reconciliation-plan.md`, `docs/tuning.md` names are consistent everywhere referenced. The fold rewrite's state-line semantics match the applied hotfix and the spec.

---
