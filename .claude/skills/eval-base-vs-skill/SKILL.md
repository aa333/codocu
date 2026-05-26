---
name: eval-base-vs-skill
description: Run a cell, score a cell, or kick off a pass for the base-vs-skill eval suite. Invoke when working on the eval suite under testing/runs/002-base-vs-skill-inplace/ — running tiers against any fixture under testing/fixtures/full/, computing metrics, calling the Claude-as-judge, or opening the manual scorecard.
---

> You are the operator for Codocu's base-vs-skill eval suite. Methodology
> lives in `testing/runs/002-base-vs-skill-inplace/SETUP.md` — defer to
> it on what the tiers contain, which fixtures are defined, what the
> rubric measures, and where outputs land. This skill is the playbook.

001 (`testing/runs/001-base-vs-skill/`) is frozen historical material; do
not run new cells there. If the user asks about 001, they're asking about
that frozen data, not asking you to add to it.

## Vocabulary

- **Cell** — one (fixture, tier) pair. Produces one set of outputs.
- **Pass** — a sweep over multiple cells under a single numbered directory.
- **Tier** — T0, T1, or T2. See SETUP for definitions.
- **Fixture** — frozen code at `testing/fixtures/full/<name>/`. An
  annotated fixture also has a `testing/fixtures/full/<name>-reference/`
  sibling (scorer-only). Defined fixtures so far:
  - `simple-bot-annotated` (Python; has `-reference/` companion)
  - `obsidian-spotiplay` (TypeScript; no companion)
- **Working copy** — `<cell>/working/`, a per-cell mutable copy of the
  fixture. The run agent edits here in place. After the run, the working
  copy *is* the artifact.

## Prerequisites

Before running anything, verify in this order:

1. `testing/runs/002-base-vs-skill-inplace/SETUP.md` exists. If not, the
   suite hasn't been initialized. Stop.
2. The fixture the user named exists at `testing/fixtures/full/<fixture>/`.
   If not, either the user mistyped or the fixture hasn't been set up
   yet. Confirm intent before proceeding.
3. For tier T1: the relevant base files exist under
   `skills/codocu/references/` (`principles.md`, `doc-standard.md`). If
   either is missing, stop and tell the user — the suite's premise is
   broken.
4. For T2 only: the plugin is loadable via `claude --plugin-dir <codocu-repo>`.
   T2 is a manual user-driven step (see T2 below).

## Invocation forms

The skill handles three operator verbs.

### `run <fixture> <tier>`

Run one cell. After this, `<cell>/working/` contains the fixture
post-agent, plus `prompt.md` and `transcript.md` at the cell root.

Procedure:

1. Determine the pass directory. If the user hasn't named one, use the
   most recent `pass-N/` under `testing/runs/002-base-vs-skill-inplace/`.
   Create `pass-1/` if none exists.
2. Create the cell directory: `<pass>/<fixture>/<tier>/`.
3. Copy the fixture verbatim into `<cell>/working/`:
   ```
   cp -r testing/fixtures/full/<fixture>/ <cell>/working/
   ```
4. Build the **prompt** for the tier:
   - **T0** prompt:
     > You are documenting an existing project. The fixture is in your
     > current working directory, `<cell-relative-path>/working/`. Read
     > the code, then write the documentation a new engineer joining
     > the project would actually use.
     >
     > You may write auxiliary docs (`.md` files under `docs/`) **and**
     > edit code files in place (docstrings, comments). Pick whichever
     > home fits each piece of doc best. Do not change non-doc code —
     > no renames, no logic edits.
     >
     > Use whatever structure and tone you judge best.
   - **T1** prompt = T0 prompt **prepended** with the literal text of
     `skills/codocu/references/principles.md` followed by `doc-standard.md`,
     under the heading "Project conventions to follow:".
5. Save the assembled prompt to `<cell>/prompt.md`.
6. **Dispatch a subagent** with the assembled prompt as its instruction.
   Use the Agent tool with `subagent_type: general-purpose`. Tell the
   subagent its working directory is `<cell>/working/` and it may edit
   anything there. Do not pass any Codocu skill, CLAUDE.md, or this
   skill into its context. The subagent must be cold. Capture its full
   output to `transcript.md`.
7. After the subagent returns, verify `<cell>/working/` has new files or
   meaningful diffs vs the fixture. If nothing changed, note in
   `transcript.md` and stop — do not score.

**T2 is different.** It exercises the real plugin flow:
   - Tell the user: "T2 requires running `claude --plugin-dir <codocu-repo>`
     against the fixture working copy. I'll prepare the working copy at
     `<cell>/working/`; you launch a session there and run `/codocu:init`
     then `/codocu`, asking it to document the code. Tell me when done."
   - Copy the fixture into `working/` as for T0/T1.
   - After the user reports T2 complete, `working/` already holds the
     full output (aux docs + any inline edits + `codocu.md`/`CLAUDE.md`).
     No additional collection step.
   - Save the user's reported session transcript (or a pointer to it) as
     `transcript.md`. Save the prompt-equivalent (a short note: "T2 ran
     via plugin install; no operator prompt assembled") as `prompt.md`.

### `score <fixture> <tier>`

Score one already-run cell. Runs metrics + judge; opens the manual
scorecard template.

Procedure:

1. Resolve the cell directory the same way `run` does.
2. Verify `<cell>/working/` exists and has meaningful diffs vs the fixture.
3. **Metrics:** invoke
   ```
   py testing/tools/metrics.py \
       --fixture testing/fixtures/full/<fixture> \
       --working <cell>/working \
       --out <cell>/metrics.json
   ```
   This counts aux-doc words, inline-doc words added per code file, the
   `home_split` ratio, and flags `code_touched` if any non-doc code line
   changed.
4. **Judge:** dispatch a fresh subagent (Agent tool, `subagent_type:
   general-purpose`) with:
   - The full text of `skills/codocu/references/principles.md` and
     `skills/codocu/references/doc-standard.md`.
   - The full content of every `.md` file under `<cell>/working/` that
     does not exist in the fixture (these are the agent's new aux docs;
     include `codocu.md` and `CLAUDE.md` for T2).
   - The **inline-doc diff** for each code file the agent touched: the
     fixture's original docstrings/comments alongside the new ones,
     clearly labelled. Use a unified diff or before/after blocks; the
     judge only needs the doc surface, not the rest of the code.
   - Instruction:
     > Score the agent's documentation output against the principles and
     > doc-standard above. The output spans two surfaces — auxiliary
     > `.md` files and inline edits to code-file docstrings/comments —
     > and they are graded together. A run that put the right content
     > in a docstring instead of an aux doc should score *higher*, not
     > lower.
     >
     > For each criterion below give a 1–5 score with a one-sentence
     > justification:
     > (1) Principle adherence — does each sentence say something code can't?
     > (2) Refactor resistance — would this survive a rename, extract, or inline?
     > (3) Bloat — judged against a minimum-viable mental version of the same doc set.
     > (4) Voice — busy-tired-reader, or reference material?
     >
     > Then list specific sentences from the docs (aux or inline) that
     > restate code, with file references. Close with a one-paragraph
     > overall verdict. Markdown output.
   - The judge has no transcript, no rubric file, no other tier's output.
5. Save the judge's response to `<cell>/judge-score.md`.
6. **Manual:** write a `manual-score.md` scaffold to the cell directory
   if none exists, with the five rubric criteria from SETUP and blank
   entries for the operator to fill in. **METADOCU agreement is
   optional** — include it only if a sibling `-reference/` directory
   exists next to the fixture. When present, point the section at that
   path as the ground-truth source. When absent, omit the section
   entirely; the five criteria stand alone. Don't fill scores yourself
   — that's the human's job.

### `pass <id>`

Start a new pass that sweeps every (fixture, tier) defined in SETUP.
Create `testing/runs/002-base-vs-skill-inplace/pass-<id>/`, then run each
cell in order. With the current fixture roster that is 6 cells:
`simple-bot-annotated × T0..T2` then `obsidian-spotiplay × T0..T2`.

This form is deferred to Phase 2. For now, run cells individually.

## Bare invocation

If invoked with no arguments, show:
- The current state: which passes exist under
  `testing/runs/002-base-vs-skill-inplace/`, which cells under each are
  scored.
- A short menu: which cell to run, which to score, which to rerun.

Use `find testing/runs/002-base-vs-skill-inplace/pass-*/ -mindepth 2
-maxdepth 2 -type d` to enumerate cells; presence of `metrics.json`,
`judge-score.md`, and `manual-score.md` indicates scored.

## What you do not do

- Do not modify any fixture or its `-reference/` companion. All fixtures
  are frozen by design.
- Do not modify the base materials under `skills/codocu/references/`.
  The whole point of the suite is to test those as-is.
- Do not modify 001 (`testing/runs/001-base-vs-skill/`). That run is
  frozen historical data.
- Do not synthesize manual scores. Always leave the manual scorecard
  blank; the human fills it.
- Do not invoke the Codocu skill (`/codocu`, `/codocu:init`) during a
  T0–T1 cell run. Those tiers are explicitly "no skill scaffolding."
- Do not show the agent any `testing/fixtures/full/<fixture>-reference/`
  directory. Those are scorer material.
- Do not commit. Repo policy is manual commits by owner.

## Subagent dispatch — key details

When dispatching the run subagent for T0–T1:

- `subagent_type: general-purpose`
- The prompt is the full assembled tier prompt — including base
  materials if applicable.
- Tell the subagent its working directory is `<cell>/working/` and it
  may edit anything there (aux docs **and** inline docstrings/comments),
  but must not change non-doc code.
- Do not pass any Codocu skill, CLAUDE.md, or this skill into its
  context. The subagent must be cold.
