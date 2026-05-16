# Run 1 — setup changes (delta from `../setup.md`)

Baseline run. iter-01.

## Plugin state under test

Codocu @ `99e8495` + uncommitted `M skills/codocu/SKILL.md` (working tree;
**not** tagged — git is user-driven).

### Skill version under test (iter-01 baseline)

`skills/codocu/SKILL.md` changed this session:

- On missing `codocu.md`, **asks**: (a) read-only orientation now, or (b) run
  `/codocu:init` first — instead of bailing with "suggest init and stop".
- Added a **Read-only orientation** section (write nothing; characterize state
  + per-side divergence; offer but do not perform the deep drill).
- Case 4 sync-marker write guarded with "if `codocu.md` exists".

## Run design

- **Single turn.** Per the locked decision the test prompt pre-empts the
  (a)/(b) ask, so the expected behavior is read-only orientation directly with
  no turn 2 (no pending question by design).
- Prompt: the verbatim runbook step-3 prompt (see `../setup.md`).
- Headless invocation: `claude --model opus --plugin-dir <codocu-repo>
  --permission-mode bypassPermissions --session-id <uuid> --output-format json -p`.

## Scoring rubric

13-point operational checklist (runs 1–2 era). See `../setup.md`.

## Runbook deviations

None. Snapshot/verify per the standard runbook; `verify` PASS.

## Cost

$0.358 / 78.6 s (single response, `num_turns`=6 internal).
