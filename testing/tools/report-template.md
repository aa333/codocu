# Test Report — Orientation (Dirty) — Iteration NN

- **Date:** YYYY-MM-DD
- **Plugin version / tag:** vX.Y.Z @ <git-sha or test-iter-NN>
- **Model:** Opus
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS | FAIL (if FAIL, restore run? yes/no)

## Prompt used

> <exact prompt given to bare `/codocu`>

## What the agent did

<3–6 lines: did it ask analyze-vs-init? what did it report? where did it stop?>

## Score

Criteria are authoritative; point weights are a test-setup detail — assign
weights when filling iter-NN.

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty |  |  |
| Complexity assessment correct | classified tier matches the fixture's true size (this fixture = Plan-gated) |  |  |
| Cost disclosed | user told size/cost before any heavy work |  |  |
| Sound triaged plan | correct triage order, scoped targets, no whole-repo sweep, archived plans not pulled in by default |  |  |
| Claimed-complete≠done caught | archetypes→strategy divergence surfaces (priority metric) |  |  |
| Public-API field-rename caught | ProfileData `status_label`→`member_status_str` / `status`→`member_status` |  |  |
| Read-only verify PASS | state-guard fingerprint unchanged; nothing written |  |  |

## Defects / observations

-

## Skill change for next iteration

-
