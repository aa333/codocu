# testing/

Long-term test reports for the Codocu plugin. Each test suite is a dated
directory; shared harness lives in `tools/`.

## Layout

```
testing/
  tools/
    state-guard.ps1       # snapshot / verify / restore a dirty fixture repo (read-only by default)
    report-template.md    # current scoring rubric (7-criterion weighted)
  <date>-<suite-name>/
    setup.md              # base methodology, fixture, runbook, scoring
    summary.md            # cross-run scoreboard + narrative + open findings
    run<N>/
      setup-changes.md    # what differed from setup.md for this run
      result.md           # filled rubric + defects + next-iteration change
      transcript.md       # verbatim assistant output
      session.txt         # headless run session id
      turn<K>.json         # raw headless-run result objects
```

## Suites

- [`2026-05-16-dirty-repo-exploration/`](2026-05-16-dirty-repo-exploration/summary.md)
  — does bare `/codocu` correctly orient (read-only) in a dirty, uninitialized
  repo, and gate the deep code-vs-docs drill behind explicit acceptance?
  3 runs; the cost-aware drill redesign landed in run 3.

## Conventions

- **Anonymized.** The fixture is a synthetic, pseudonymized project; the target
  working copy is referred to as `<target-repo>` and the plugin checkout as
  `<codocu-repo>`. No real project names or absolute personal paths.
- **Read-only by contract.** Runs must not mutate the fixture; `state-guard.ps1
  verify` is the gate. `state-guard.ps1` stores its snapshot in a gitignored
  `.snapshot/` next to itself (`testing/**/.snapshot/`) — local-only,
  regenerate with `snapshot -Repo <path>`.
- **No self-grading.** Transcripts are scored in a separate session against the
  rubric in `tools/report-template.md`.
