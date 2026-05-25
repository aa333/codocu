---
name: eval-base-vs-skill
description: Run a cell, score a cell, or kick off a pass for the base-vs-skill eval suite. Invoke when working on the eval suite under testing/2026-05-25-base-vs-skill/ — running tiers against fixtures, computing metrics, calling the Claude-as-judge, or opening the manual scorecard.
---

> You are the operator for Codocu's base-vs-skill eval suite. Methodology
> lives in `testing/2026-05-25-base-vs-skill/SETUP.md` — defer to it on what
> the tiers contain, what the rubric measures, and where outputs land. This
> skill is the playbook.

## Vocabulary

- **Cell** — one (fixture, tier) pair. Produces one set of outputs.
- **Pass** — a sweep over multiple cells under a single dated directory.
- **Tier** — T0 through T4. See SETUP for definitions.
- **Fixture** — frozen code under `testing/fixtures/<name>/`.

## Prerequisites

Before running anything, verify in this order:

1. `testing/2026-05-25-base-vs-skill/SETUP.md` exists. If not, the suite hasn't
   been initialized. Stop.
2. The fixture exists at `testing/fixtures/<fixture>/`. If not, the user is
   running a cell the suite hasn't defined yet. Confirm intent before
   proceeding.
3. For tiers T1–T3: the relevant base files exist under
   `skills/codocu/references/` (`principles.md`, `doc-standard.md`,
   `smell-catalog.md`). If a referenced base file is missing, stop and tell
   the user — the suite's premise is broken.
4. For T4 only: the plugin is loadable via `claude --plugin-dir <codocu-repo>`.
   If the user isn't already running with the plugin loaded, T4 is a manual
   step (see T4 below).

## Invocation forms

The skill handles three operator verbs.

### `run <fixture> <tier>`

Run one cell. Produces a `produced/` directory of `.md` files, a
`prompt.md`, and a `transcript.md`.

Procedure:

1. Determine the pass directory. If the user hasn't named one, use the most
   recent `pass-N/` under `testing/2026-05-25-base-vs-skill/`. Create
   `pass-1/` if none exists.
2. Create the cell directory: `<pass>/<fixture>/<tier>/`.
3. Build the **prompt** for the tier:
   - **T0** prompt:
     > Below is a code fixture under `testing/fixtures/<fixture>/`. Write
     > auxiliary docs for this code as if you were documenting it for new
     > engineers joining the project. Put them under
     > `<pass>/<fixture>/T0/produced/`. Use whatever structure and tone you
     > judge best.
   - **T1** prompt = T0 prompt **prepended** with the literal text of
     `skills/codocu/references/principles.md`, headed with
     "Project conventions to follow:".
   - **T2** prompt = T1 prompt + doc-standard.md appended after principles.
   - **T3** prompt = T2 prompt + smell-catalog.md appended after doc-standard.
4. Save the assembled prompt to `<pass>/<fixture>/<tier>/prompt.md`.
5. **Dispatch a subagent** with the assembled prompt as its instruction. The
   subagent has Write access only under the cell's `produced/` directory; no
   skill scaffolding is loaded. Use the Agent tool with `subagent_type:
   general-purpose`. Capture its full output to `transcript.md`.
6. After the subagent returns, verify `produced/` is non-empty. If empty,
   note in `transcript.md` and stop — do not score.

**T4 is different.** It exercises the real plugin flow:
   - Tell the user: "T4 requires running `claude --plugin-dir <codocu-repo>`
     against the fixture working copy. I'll prepare the fixture working copy
     at `<pass>/<fixture>/T4/working/`; you launch a session there and run
     `/codocu:init` then `/codocu`, asking it to document the code under
     `docs/`."
   - Copy the fixture to `working/`. After the user reports the T4 session
     complete, copy `working/docs/` to `<pass>/<fixture>/T4/produced/` and
     `working/codocu.md` if present.
   - Save the user's reported session transcript (or a pointer to it) as
     `transcript.md`.

### `score <fixture> <tier>`

Score one already-produced cell. Runs metrics + judge; opens the manual
scorecard template.

Procedure:

1. Resolve the cell directory the same way `run` does.
2. Verify `<cell>/produced/` exists and is non-empty.
3. **Metrics:** invoke
   ```
   py testing/tools/metrics.py \
       --fixture testing/fixtures/<fixture> \
       --produced <cell>/produced \
       --out <cell>/metrics.json
   ```
4. **Judge:** dispatch a fresh subagent (Agent tool, `subagent_type:
   general-purpose`) with:
   - The full text of `skills/codocu/references/principles.md` and
     `skills/codocu/references/doc-standard.md`
   - The full content of every `.md` under `<cell>/produced/`
   - Instruction:
     > Score these produced docs against the principles and doc-standard
     > above. For each criterion below, give a 1–5 score with a one-sentence
     > justification: (1) Principle adherence; (2) Refactor resistance;
     > (3) Bloat; (4) Voice. Then list specific sentences from the docs
     > that restate code (line refs welcome). Then close with a one-paragraph
     > overall verdict. Markdown output.
   - The judge has no transcript, no rubric file, no other tier's output.
5. Save the judge's response to `<cell>/judge-score.md`.
6. **Manual:** write a `manual-score.md` scaffold to the cell directory if
   none exists, with the rubric criteria from SETUP and blank entries for
   the operator to fill in. Don't fill scores yourself — that's the human's
   job.

### `pass <date>`

Start a new pass that sweeps all defined cells. Create
`testing/2026-05-25-base-vs-skill/pass-<date>/`, then run each defined
(fixture, tier) in order. Phase 1 = egregor-cut × T0..T4. Phase 2 adds
bobatler-cut.

This form is deferred to Phase 3. For now, run cells individually.

## Bare invocation

If invoked with no arguments, show:
- The current state: which passes exist, which cells under each are scored.
- A short menu: which cell to run, which to score, which to rerun.

Use `find testing/2026-05-25-base-vs-skill/pass-*/ -mindepth 3 -maxdepth 3
-type d` to enumerate cells; presence of `metrics.json`, `judge-score.md`,
and `manual-score.md` indicates scored.

## What you do not do

- Do not modify fixtures. Fixtures are frozen by design.
- Do not modify the base materials under `skills/codocu/references/`. The
  whole point of the suite is to test those as-is.
- Do not synthesize manual scores. Always leave the manual scorecard blank;
  the human fills it.
- Do not invoke the Codocu skill (`/codocu`, `/codocu:init`) during a T0–T3
  cell run. Those tiers are explicitly "no skill scaffolding."
- Do not commit. Repo policy is manual commits by owner.

## Subagent dispatch — key details

When dispatching the run subagent for T0–T3:

- `subagent_type: general-purpose`
- The prompt is the full assembled tier prompt — including base materials
  if applicable.
- Tell the subagent its working directory is the cell's `produced/`
  directory, and it should only write under there.
- Do not pass any Codocu skill, CLAUDE.md, or this skill into its context.
  The subagent must be cold.
