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
