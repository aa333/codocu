# testing/

Eval evidence for the Codocu plugin. Test reports, fixtures, and the tooling
that produces them. Not documentation about Codocu — that lives under
`docs/` and `skills/codocu/references/`.

## Layout

```
testing/
  fixtures/
    full/      whole-project fixtures used by the base-vs-skill suite
    atomic/    single-file fixtures used by the codocu-reviewer evals
  runs/        eval suites; current is 002-base-vs-skill-inplace
  tools/       shared scripts (metrics.py, state-guard.ps1)
  archive/     superseded suites, kept as history
```

Suite directories use `NNN-name` numeric IDs so ordering is obvious without
parsing dates. Passes inside a suite are `pass-1`, `pass-2`, …

## Current suite

[`runs/002-base-vs-skill-inplace/`](runs/002-base-vs-skill-inplace/SETUP.md)
asks whether Codocu's bloat and code-repetition failures live in the base
material (principles + doc-standard) or in the skill scaffolding on top of
it. Three tiers — no Codocu, base materials only, full plugin — run against
each fixture. See its `SETUP.md` for the rubric, tier definitions, and
per-cell flow.

`runs/001-base-vs-skill/` is frozen historical data from the first pass.
Don't add to it; new cells go in 002.

## Running an eval

The operator skill is [`.claude/skills/eval-base-vs-skill/`](../.claude/skills/eval-base-vs-skill/SKILL.md)
(project-local; not shipped in the plugin manifest). Invoke via
`/eval-base-vs-skill <verb> <fixture> <tier>`:

- `run` — copies the fixture to `<cell>/working/`, dispatches a cold
  subagent into it, captures the transcript. For T2 the user runs the
  plugin manually inside `working/` instead.
- `score` — runs `tools/metrics.py` and a Claude-as-judge subagent against
  the working copy, opens a blank manual scorecard for the human.
- `pass` — sweeps every (fixture, tier) cell. Deferred to phase 2.

Output for one cell:

```
pass-N/<fixture>/<tier>/
  prompt.md         exact prompt given to the run agent
  transcript.md     verbatim agent output
  working/          fixture copy after the agent edited it — the artifact
  metrics.json      automated counts
  judge-score.md    Claude-as-judge verdict
  manual-score.md   human rubric (METADOCU section only if the fixture has a -reference/ companion)
```

To extract "what the agent wrote", diff `working/` against the frozen
fixture at `fixtures/full/<fixture>/`.

## Conventions

- **Frozen fixtures.** Both halves of a `full/` pair are committed in their
  final form. If a fixture is wrong, create a new one at a new name; never
  edit in place. Same rule applies to `atomic/`.
- **Anonymized values.** Identifiers stay real; channel handles, tokens, DB
  paths, and similar values are placeholders.
- **No self-grading.** The run agent never sees the rubric. Scoring happens
  in separate sessions per the suite's `SETUP.md`.
- **`-reference/` companions are scorer-only.** Never show them to the run
  agent.
