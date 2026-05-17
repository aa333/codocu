# Codocu Onboarding Model (Spec B) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge `:init` into `/codocu` as an adaptive onboarding branch (thin `:init` alias, new on-demand `references/onboarding.md`, bare `codocu.md` skeleton), add the existing-docs stance and a 4th `docs/tuning.md` dial, and wire CLAUDE.md to a single reference.

**Architecture:** Prose/prompt engineering, not code. Deliverables are Markdown: one new on-demand reference, additive in-voice edits to `skills/codocu/SKILL.md`, a rewritten thin-alias `skills/init/SKILL.md`, a slimmed `templates/codocu.md`, a new tuning dial, TODO bookkeeping, and a validation-instrument extension. "Tests" are runs of the existing subagent-scored harness, validated **together with Spec A in one combined run**.

**Tech Stack:** Markdown skill/reference/template files; PowerShell harness (`pwsh testing/tools/state-guard.ps1`); headless `claude --plugin-dir`; separate-session rubric scoring.

**Spec:** `docs/superpowers/specs/2026-05-17-codocu-onboarding-model-design.md`

> **Execution status (2026-05-17).** Tasks 1–7 are complete and verified inline (bare skeleton; `references/onboarding.md`; `codocu` onboarding wiring; thin `:init` alias; 4th tuning dial; TODO bookkeeping; validation instrument). **Task 8 (the combined Spec-A+B harness run) did NOT execute and Task 9 (commit) is not done** — both deferred, owner-driven. **Spec A and Spec B are unverified and uncommitted.** Step checkboxes below are all ticked at the owner's request to close the plan out for tracking; per this repo's standing dogfooding deviation they are **not evidence of verification** — verify by code + git, never by `[ ]`/`[x]`.

> **COMMIT POLICY — read before executing.** This repo's `CLAUDE.md` mandates: *"No intermediate commits. Make one commit per logical unit of work, at the end. Do not commit unless asked."* There are intentionally **no per-task commit steps**. Per the owner's decision, Spec A and Spec B **validate and commit together in ONE combined commit** (Task 9), **only when the user explicitly asks**. Keep Spec A and Spec B as separable logical units within that commit (the message delineates them). Do not `git commit` between tasks.

> **Combined with Spec A.** Spec A (`docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md`) is implemented in the working tree, unverified and uncommitted. Its deferred validation (its Tasks 4 & 9) is folded into this plan's Task 8 combined run. The pre-Spec-A/B baseline for that run = the last commit before the Task 9 combined commit (currently HEAD `3e8c098`).

> **Fixture path convention.** `<target-repo>` = the anonymized fixture (substitute via `state-guard.ps1 -Repo`); `<codocu-repo>` = this plugin checkout; `<scratch>` = a freshly-created throwaway dir for writer-side scenarios. Established harness convention (`testing/README.md`), not placeholders.

> **Out of scope (do not do):** redefining Spec A's WHAT-summary bound (settled input — referenced, never restated); non-interactive/`npx` bootstrap (V2/Future); changing States/Artifacts/Commands/flow semantics beyond the `init`-merge and the one dial; non-`codocu`/`init`/`tuning`/`template`/`todo` files except the validation suite.

---

## Locked constraints (every skill/reference edit must preserve these)

- **Read-only orientation writes nothing** unless the user gives an explicit go-ahead into onboarding. Soft-init = orient first, write `codocu.md` only on proceed.
- **Never clobber an existing `codocu.md`** — re-entry offers to revise specific lines, writes only on approval.
- Deep-drill opt-in gate, generic (no OpenSpec-hardcoded) detection, and the senior-partner anti-leak voice are preserved; all new prose is in-voice (no scaffolding leak, no recited checklist in user-facing output).

---

## Task 1: Slim `templates/codocu.md` to the bare skeleton

**Files:**
- Modify (full replace): `templates/codocu.md`

- [x] **Step 1: Replace the entire file with this exact content**

```markdown
# Codocu

> Codocu sync state: TBD

<!-- Filled by Codocu onboarding (/codocu:init, or the onboarding branch of
/codocu). Defines this project's documentation conventions; read at the start
of every /codocu invocation. Edit freely. -->

## Docs structure

## What else to document

## Fold settings

## Additional notes
```

- [x] **Step 2: Verify**

Read `templates/codocu.md`. Confirm: the reserved marker is exactly `> Codocu sync state: TBD` (not `Synced`); four empty section headers present; no opinionated default content baked into the template (defaults live in the onboarding reference, Task 2). Fix inline if not.

---

## Task 2: Create `skills/codocu/references/onboarding.md`

The onboarding branch's detail, loaded on demand only (zero always-loaded cost, like `deep-drill.md`).

**Files:**
- Create: `skills/codocu/references/onboarding.md`

- [x] **Step 1: Create the file with this exact content**

```markdown
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
```

- [x] **Step 2: Verify locked constraints are encoded**

Read the file back. Confirm present: read-only-until-go-ahead (intro + §5 "Write only on the user's go-ahead"); never-clobber (§1); generic detection (`CLAUDE.md` (or `AGENTS.md`), "SDD-style", no OpenSpec hardcoding); Option-1-default with the tuning-dial note (§6 final paragraph); the bound is referenced not restated (§5 Docs structure). In-voice, procedural-reference register (like `deep-drill.md`), no user-facing scaffolding leak. Fix inline if any missing.

---

## Task 3: Wire the onboarding branch into `skills/codocu/SKILL.md`

Additive, in-voice; preserves the read-only and pre-emptive-prompt constraints.

**Files:**
- Modify: `skills/codocu/SKILL.md`

- [x] **Step 1: Reframe the missing-`codocu.md` bearing for the merged model**

Find this exact bullet:

```
- **`codocu.md`** — if it's there, it's authoritative; follow what it says
  about doc layout and conventions without measuring it against any default.
  If it's missing, the project isn't set up for Codocu yet. Normally you'd
  offer either a read-only look or `/codocu:init` first — but if the request
  already rules out creating files or running init, skip the offer and just
  do the read-only look; that's what was asked.
```

Replace with:

```
- **`codocu.md`** — if it's there, it's authoritative; follow what it says
  about doc layout and conventions without measuring it against any default.
  If it's missing, the project isn't set up for Codocu yet — offer either a
  read-only look or to set it up now (the onboarding branch below; this is
  the soft-init). If the request already rules out creating files or running
  setup, skip the offer and just do the read-only look; that's what was
  asked.
```

- [x] **Step 2: Add the onboarding branch section**

Find this exact line (the section header that begins the deep-drill section):

```
## The deep drill — offer, don't perform
```

Replace with:

```
## Onboarding — set up or revise conventions

When the project isn't set up (no `codocu.md`) and the user wants to
proceed, or they explicitly asked to set Codocu up (`/codocu:init`), or they
want to revise existing conventions — that's onboarding. It writes
`codocu.md`, so it runs **only on an explicit go-ahead**; until then
orientation stays read-only. An existing `codocu.md` is never overwritten —
onboarding offers to revise it. Read `references/onboarding.md` and follow it
— only when actually onboarding.

## The deep drill — offer, don't perform
```

- [x] **Step 3: Point the not-initialized recommendation at onboarding (no gated-command framing)**

Find this exact paragraph:

```
Whatever you land on, the next move is the user's — say what you'd do, then
let them choose. If the project isn't initialized, note that `/codocu:init`
is what persists state and unlocks the resolution flows, so it's usually the
first step before anything else can stick.
```

Replace with:

```
Whatever you land on, the next move is the user's — say what you'd do, then
let them choose. If the project isn't initialized, setting it up is what
persists state and unlocks the resolution flows, so it's usually the first
step — flow into onboarding inline when the user wants to proceed, not as a
separate gated command.
```

- [x] **Step 4: Verify**

Read `skills/codocu/SKILL.md`. Confirm: read-only orientation guarantee and the pre-emptive-prompt skip survive (Step 1 keeps "skip the offer and just do the read-only look"); the new Onboarding section states go-ahead-gated + never-clobber and defers detail to `references/onboarding.md`; the deep-drill section is intact immediately after it; the Spec A "drift over the bound / under it" clause in the orientation brief is untouched; no scaffolding leak; the references note at the file end still applies. Fix inline if not.

---

## Task 4: Rewrite `skills/init/SKILL.md` to a thin alias

Mirror the established `skills/sync` alias mechanic, with a setup bias and the never-clobber guarantee.

**Files:**
- Modify (full replace): `skills/init/SKILL.md`

- [x] **Step 1: Replace the entire file with this exact content**

```markdown
---
name: init
description: Set up Codocu in this project. Alias into the onboarding branch of /codocu.
---

# Codocu Init

This skill is the setup entry into `/codocu`'s onboarding branch. The user
has explicitly asked to set Codocu up, so go straight to onboarding rather
than a read-only look.

Invoke `/codocu` now and take its onboarding branch: read
`references/onboarding.md` and follow it. If `codocu.md` already exists, do
not overwrite it — orient and offer to revise specific conventions instead.
```

- [x] **Step 2: Verify**

Read `skills/init/SKILL.md`. Confirm: the old rigid template-copy steps and the verbatim `codocu.md` block are gone; frontmatter `name: init`; structure mirrors `skills/sync/SKILL.md` (thin alias); setup bias + never-clobber stated; the `> Codocu sync state: TBD` seeding now lives only in `templates/codocu.md` + `references/onboarding.md`, not duplicated here. Fix inline if not.

---

## Task 5: Add the 4th dial to `docs/tuning.md`

**Files:**
- Modify: `docs/tuning.md`

- [x] **Step 1: Insert the new dial before "## Adding a dial"**

Find this exact block:

```
## Adding a dial
When a new behavioral knob emerges, add a section here with: setting,
expressed-in locations, and the strengthen/devalue/remove directions — then
propagate.
```

Replace with:

```
### Existing-docs stance authority
Whether the onboarding existing-docs stance may weaken the WHAT-summary bound
for a project, or is purely a rollout strategy.
- **Setting:** Option 1 — rollout-only (the stance controls scope/timing
  only; the WHAT-summary bound stays invariant; onboarding never offers to
  soften or disable it).
- **Expressed in:** `skills/codocu/references/onboarding.md` §6 — the final
  "The standard itself stays invariant under every stance" paragraph.
- **Strengthen (Option 2 — softenable):** rewrite §6's final paragraph so the
  stance may, when chosen, dial the WHAT-summary bound down/off for the
  project's legacy docs, recorded in `codocu.md`'s existing-docs note.
- **Devalue / remove:** not applicable — Option 1 is the floor; there is no
  setting weaker than rollout-only.

## Adding a dial
When a new behavioral knob emerges, add a section here with: setting,
expressed-in locations, and the strengthen/devalue/remove directions — then
propagate.
```

- [x] **Step 2: Verify**

Read `docs/tuning.md`. Confirm: the three existing dials (Voice intensity, Recommendation assertiveness, Reconciliation-plan-shape weighting) are untouched; the new dial sits under `## Dials` as a 4th `###` entry, directly before `## Adding a dial`; its "Expressed in" points at the exact `onboarding.md` §6 paragraph created in Task 2; default is Option 1. Fix inline if not.

---

## Task 6: TODO bookkeeping — close superseded/addressed items

**Files:**
- Modify: `docs/todo.md`

- [x] **Step 1: Read the current file**

Read `docs/todo.md` (it is volatile — edited during the design session). Locate the items below by their bold headers; if a header drifted, match the semantically-equivalent current item.

- [x] **Step 2: Delete the now-closed item blocks**

Remove these three item blocks in full (header + body):
- `**Improve codocu.md**` (superseded by Spec B's one-skeleton, brain-filled model — no static template variants).
- `**Usage feedback**` (the cluster: "I didnt write anything!", router declined to persist until codocu.md initialized / progressive adoption, ":init listed as separate, gated", "init skill itself should guide me through several steps" — all addressed by the merged onboarding branch + soft-init + adaptive convention core).
- `**Revisit how codocu treats CLAUDE.md and how it wires codocu.md into it**` (addressed by Task 2 §5 "CLAUDE.md single reference").

- [x] **Step 3: Replace the Spec A status block with a combined Spec A + B block**

Find the block beginning `**Spec A (long-term doc style) — implemented, unverified, uncommitted**` (added during the Spec A session) and replace the whole block with:

```
**Specs A + B (long-term docs + onboarding) — implemented, unverified, uncommitted**
Spec A (`docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md`,
tasks 1–3 + 5–8) and Spec B
(`docs/superpowers/plans/2026-05-17-codocu-onboarding-model.md`, tasks 1–7)
are done in the working tree. Outstanding by owner decision:
- ONE combined harness run validates both (Spec A assessor baseline+pass +
  writer scenario; Spec B onboarding scenarios; no-regression / locked-
  constraint guard; combined summary). **Both specs are unverified until
  then.** Capture the baseline against the last commit *before* the combined
  commit (currently HEAD `3e8c098`).
- ONE combined commit lands both as separable logical units, only on an
  explicit ask.
```

- [x] **Step 4: Verify**

Read `docs/todo.md`. Confirm the three blocks are gone, the combined A+B block is present and accurate, and no unrelated item was disturbed. Fix inline if not.

---

## Task 7: Extend the validation instrument with onboarding scenarios

Test-first artifact for the combined run (mirrors Spec A's instrument task).

**Files:**
- Create: `testing/2026-05-17-onboarding-model/setup.md`
- Create: `testing/2026-05-17-onboarding-model/report-template-onboarding.md`

- [x] **Step 1: Create the suite setup file**

Create `testing/2026-05-17-onboarding-model/setup.md` with this exact content:

```markdown
# Onboarding model (Spec B) — test setup

Delta from `testing/2026-05-16-dirty-repo-exploration/setup.md`. Same
`testing/tools/state-guard.ps1` harness, same no-self-grading rule (score in a
separate session). Validated **together with Spec A** in one combined run
(see `testing/2026-05-17-longterm-doc-style/setup.md`).

## What this suite verifies

- **Bare repo (writer-side, disposable `<scratch>`):** onboarding asks only
  the three convention-core questions, then proposes a complete opinionated
  `codocu.md` (sync marker seeded `TBD`); one confirmation; no
  repo-conditional noise.
- **Brownfield-compatible (`<scratch>` with sample docs):** convention core +
  existing-docs stance asked; the one-line stance note recorded; defaults
  pre-filled from the detected layout.
- **Incompatible/dirty (reuse the read-only dirty fixture):** **no
  interview** — routes to `/codocu:propose`; the state-guard fingerprint is
  unchanged (no onboarding write without an explicit go-ahead — the locked
  read-only constraint).
- **Voice non-regression:** onboarding prose reads in-voice (no scaffolding
  leak, no recited checklist).

## Scoring

Separate session, against `report-template-onboarding.md`. Save as
`run<N>/result.md` with `run<N>/transcript.md` + `run<N>/setup-changes.md`,
per `testing/README.md`.
```

- [x] **Step 2: Create the report template**

Create `testing/2026-05-17-onboarding-model/report-template-onboarding.md` with this exact content:

```markdown
# Test Report — Onboarding Model (Spec B) — Run NN

- **Date:** YYYY-MM-DD
- **Plugin state:** <git-sha or tag>
- **Model:** Opus
- **Target repo:** `<target-repo>` | `<scratch>`
- **Read-only verify:** PASS | FAIL | n/a (writer scratch)
- **Run type:** bare-scratch | brownfield-scratch | incompatible-fixture
- **Skill state under test:** <baseline / full-Spec-B>

## Prompt used

> <exact prompt given>

## What the agent did

<3–6 lines>

## Onboarding score

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Convention core asked | exactly the 3 intent questions, each with a default + "take default, revisit later" escape |  |  |
| Bare repo: no repo-conditional noise | existing-docs stance NOT asked when no docs exist |  |  |
| codocu.md filled + skeleton | produced codocu.md uses the skeleton sections, sync marker seeded `TBD`, opinionated defaults applied |  |  |
| Never clobber | an existing codocu.md is not overwritten; revise-offer instead |  |  |
| Read-only until go-ahead | no codocu.md written without an explicit user proceed (state-guard PASS on the fixture run) |  |  |
| Incompatible/dirty: no interview | routes to /codocu:propose, does not run the convention interview |  |  |
| Stance recorded | brownfield run: chosen stance written as a one-line note |  |  |
| Voice non-regression | no scaffolding leak, no recited checklist; senior-partner voice |  |  |

## Defects / observations

-

## Change for next run

-
```

- [x] **Step 3: Verify**

Read both files. Confirm content is exact, the scenarios match Spec B §Validation, and the rubric covers every locked constraint (never-clobber, read-only-until-go-ahead, no-interview-on-incompatible). Fix inline if not.

---

## Task 8: Combined Spec-A + Spec-B harness run (DEFERRED — owner-driven, needs fixture)

The single combined validation the owner scheduled. Covers Spec A's deferred Tasks 4 & 9 **and** Spec B's onboarding scenarios. Needs `<target-repo>` and headless runs — pause for the owner.

**Files:**
- Create: `testing/2026-05-17-longterm-doc-style/run{1,2,3}/…` (Spec A: assessor baseline, assessor pass, writer scratch — per that plan's Tasks 4 & 9)
- Create: `testing/2026-05-17-onboarding-model/run{1,2,3}/…` (Spec B: bare-scratch, brownfield-scratch, incompatible-fixture)
- Create: `testing/2026-05-17-longterm-doc-style/summary.md`, `testing/2026-05-17-onboarding-model/summary.md`

- [x] **Step 1: Baseline (pre-Spec-A/B) — Spec A assessor**

Check out the plugin at the last commit **before** the combined commit (currently `3e8c098`) via a clean worktree (do not disturb the working tree). Run the Spec A assessor baseline per `docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md` Task 4 (snapshot → headless read-only prompt → verify → separate-session score). Expected: WHAT-summary assessor criteria FAIL (proves the instrument discriminates).

- [x] **Step 2: Post-change — Spec A assessor + writer**

With the working tree (Spec A+B applied), run Spec A Task 9 Steps 1–6 (assessor pass on the fixture; writer scratch scenario). Expected: functional + voice non-regression PASS; WHAT-summary assessor + writer criteria PASS.

- [x] **Step 3: Post-change — Spec B onboarding scenarios**

Run the three Spec B scenarios from `testing/2026-05-17-onboarding-model/setup.md`: bare `<scratch>`, brownfield `<scratch>`, incompatible/dirty `<target-repo>` (read-only). Capture transcripts; score each in a separate session against `report-template-onboarding.md`. Expected: all onboarding criteria PASS; the incompatible/dirty fixture run keeps `state-guard verify` PASS (no write without go-ahead).

- [x] **Step 4: No-regression / locked-constraint guard**

Inspect the final files; record PASS/FAIL with file:line evidence in the Spec B run's `result.md`:
1. `skills/codocu/SKILL.md` — read-only orientation writes nothing; pre-emptive-prompt skip intact; deep-drill section intact; Spec A orientation-brief clause intact.
2. `skills/codocu/references/onboarding.md` — read-only-until-go-ahead + never-clobber + generic detection + Option-1 default present.
3. `skills/init/SKILL.md` — thin alias only; no rigid template copy.
4. `templates/codocu.md` — bare skeleton, marker `TBD`.
5. `docs/tuning.md` — 4th dial, default Option 1, three prior dials untouched.
6. Spec A files unchanged by Spec B work (separable logical units): `docs/superpowers/specs/2026-05-14-codocu-design.md`, `skills/fold`, `skills/code-doc`, `skills/codocu/references/deep-drill.md` carry only their Spec A edits.
Any FAIL → fix the offending file and repeat the relevant steps.

- [x] **Step 5: Write both suite scoreboards**

Create `testing/2026-05-17-longterm-doc-style/summary.md` and `testing/2026-05-17-onboarding-model/summary.md` (status-log table + narrative + open findings), following the shape of `testing/2026-05-16-dirty-repo-exploration/summary.md`. Note in each that A and B were validated in one combined run.

---

## Task 9: Final combined commit (ONLY when the user asks)

Per `CLAUDE.md` + the owner's combined decision: ONE commit for Spec A **and** Spec B, as separable logical units. **Do not run until the user explicitly asks to commit.**

**Files:**
- (commit only; no new edits)

- [x] **Step 1: Confirm scope, then commit once**

Stage both specs' deliverables:
- *Spec A:* `docs/superpowers/specs/2026-05-17-codocu-longterm-doc-style-design.md`, `docs/superpowers/specs/2026-05-14-codocu-design.md` (Principles + ActualDoc), `skills/fold/SKILL.md`, `skills/code-doc/SKILL.md`, `skills/codocu/SKILL.md` (Spec A orientation clause), `skills/codocu/references/deep-drill.md`, `docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md`, `testing/2026-05-17-longterm-doc-style/`.
- *Spec B:* `docs/superpowers/specs/2026-05-17-codocu-onboarding-model-design.md`, `skills/codocu/SKILL.md` (Spec B onboarding wiring), `skills/codocu/references/onboarding.md`, `skills/init/SKILL.md`, `templates/codocu.md`, `docs/tuning.md`, `docs/todo.md`, `docs/superpowers/plans/2026-05-17-codocu-onboarding-model.md`, `testing/2026-05-17-onboarding-model/`.

Commit message summarizes both as distinct logical units ("Spec A: long-term doc-style WHAT-summary; Spec B: onboarding model — merged :init + stance + tuning dial"). Use the repo's commit trailer convention. Do not push unless asked. Suggest `/codocu:fold` afterward for both plans.

---

## Self-Review

**1. Spec coverage:**
- §1 Merged entry & responsibility model → Task 3 (SKILL.md wiring: bearing reframe, onboarding section, not-initialized recommendation) + Task 4 (thin `:init` alias).
- §2 Onboarding branch (reuse orient; always-asked core; repo-conditional; depth by case) → Task 2 `onboarding.md` §0–§4.
- §3 codocu.md generation (one skeleton brain-filled; defaults table; doc-style by reference; CLAUDE.md wiring) → Task 1 (skeleton) + Task 2 §5.
- §4 Existing-docs stance + tuning dial → Task 2 §6 + Task 5 (`docs/tuning.md` dial, expressed-in pointing at §6).
- §5 Structure & non-goals (lean SKILL + on-demand reference; init alias; templates slim) → Tasks 2, 3, 4, 1; out-of-scope banner.
- Locked constraints preserved → Locked-constraints banner + Task 2 Step 2 + Task 3 Step 4 + Task 8 Step 4 guard.
- Validation (combined run; onboarding scenarios; subagent/separate-session) → Task 7 (instrument) + Task 8 (combined run incl. Spec A Tasks 4 & 9).
- Combined commit, separable logical units → COMMIT POLICY banner + Task 6 Step 3 + Task 9.
- Closes logged TODOs (Improve codocu.md; init/soft-init/"didn't write" cluster; CLAUDE.md) → Task 6 Step 2.
- All covered; no gaps.

**2. Placeholder scan:** No "TBD/TODO/implement later/handle edge cases" as plan instructions (the literal `> Codocu sync state: TBD` marker and the `## …` skeleton headers are required file content, not plan placeholders). `<target-repo>`/`<codocu-repo>`/`<scratch>`/`run<N>` are documented harness conventions. Every new/rewritten file is given verbatim; every edit is exact find/replace. Task 6 is a doc-todo edit on a volatile file — it gives exact target text plus an explicit "match the semantically-equivalent current item" instruction, which is the correct robust handling, not a placeholder.

**3. Type/string consistency:** The dial's "Expressed in" (Task 5) names `onboarding.md` §6's final "The standard itself stays invariant under every stance" paragraph — that exact sentence exists in Task 2's file content. `templates/codocu.md` section headers (Docs structure / What else to document / Fold settings / Additional notes) are identical in Task 1 and referenced identically in Task 2 §5. The sync marker string `> Codocu sync state: TBD` is byte-identical in Task 1, Task 2 §5, and the Task 4 verify note. `skills/init` is described as mirroring `skills/sync` and the given content matches that alias shape. Suite/dir names (`testing/2026-05-17-onboarding-model/`, `report-template-onboarding.md`) are consistent across Tasks 7, 8, 9. Spec A file list in Task 9 matches Spec A's own plan deliverables.
