# R3 + R4 — Onboarding (Spec B) scratch — scored separate-session (subagent, transcript-only)

Covers run3 (bare-scratch) and run4 (brownfield-scratch). Single-turn
"take defaults, propose-don't-write" adaptation. Skill state: master `86b14c7`
+ uncommitted A+B+C.

## What the agent did

**R3 (bare):** identified bare/minimal (one untracked `src/main.py`, no docs,
no `codocu.md`); only the 3 convention-core questions; defaults table;
complete proposed `codocu.md` seeded `> Codocu sync state: TBD`; explicitly no
existing-docs stance (no docs); nothing written.
**R4 (brownfield):** classified brownfield/compatible (two homebrew docs +
`src/app.py`); 3 core defaults + existing-docs stance (Tailor) with a one-line
stance note; complete proposed `codocu.md` seeded `TBD`; flagged
`api-notes.md` slightly over the bound but not migration-worthy; nothing
written.

### R3 (bare)
| Metric | Got | Note |
|---|---|---|
| Convention core | PASS | Exactly the 3 intent questions w/ defaults; no interactive interrogation |
| Bare: no repo-conditional noise | PASS | "No existing-docs stance (no docs exist)" — stance not raised |
| Brownfield: stance handled | n/a | bare scenario |
| codocu.md skeleton + TBD | PASS | Skeleton sections; `TBD` seeded |
| Read-only until go-ahead | PASS | Nothing written; proposal only |
| Never clobber | n/a | no pre-existing codocu.md |
| Incompatible/dirty: no interview | n/a | not exercised (initialized-target delta) |
| Reader-exp + Voice | PASS | Answer-first, terse, senior voice, no scaffolding leak |

### R4 (brownfield)
| Metric | Got | Note |
|---|---|---|
| Convention core | PASS | 3 core + stance as derived 4th row; not extra interrogation |
| Bare: no repo-conditional noise | n/a | brownfield scenario |
| Brownfield: stance handled | PASS | Tailor stance + explicit one-line stance note |
| codocu.md skeleton + TBD | PASS | Skeleton present; `TBD` seeded |
| Read-only until go-ahead | PASS | Nothing written |
| Never clobber | n/a | no pre-existing codocu.md |
| Incompatible/dirty: no interview | n/a | not exercised |
| Reader-exp + Voice | PASS | Answer-first, diagnostic, concise, senior voice |

## Headline

Post-change onboarding behaves correctly in both repo classes — bare
suppresses docs-stance noise, brownfield handles + notes the stance — proposal-
only read-only, no voice/reader regression.
