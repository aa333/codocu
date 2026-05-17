# No-regression / locked-constraint guard — combined A+B+C

Artifact inspection (not transcript grading). file:line evidence. All PASS.

## Spec A locked constraints
- **A1 — design spec.** Seven Principles `2026-05-14-codocu-design.md:28-34`
  (original six intact, reader-economy bullet added at `:33`). WHY four
  conditions byte-identical to pre-Spec-A: `:77` (verbatim "(1) the reason is
  non-obvious … (4) the absence of something was a deliberate choice. If none
  apply, the code speaks for itself."). WHAT-summary block `:72-77` untouched
  by this unit (only a Principle bullet was inserted). PASS.
- **A2 — `codocu/SKILL.md`.** Only the shared house-rule line + the
  orientation-brief bullet were edited; read-only orientation, deep-drill
  opt-in gate, pre-emptive-prompt skip, and generic (non-OpenSpec-hardcoded)
  detection are untouched. Empirically corroborated by R1: `state-guard verify`
  = VERIFY PASS (nothing written) and detection was generic (found the
  governing plan + rename without OpenSpec hardcoding). PASS.
- **A3 — `fold/SKILL.md`.** No-trust-checkboxes intact (`fold/SKILL.md:28`
  "Don't trust the checkboxes", `:30` "judge by code and git"); unconditional
  `> Codocu sync state: Synced` intact (`:67`). The "Bring the docs along"
  edit did not touch the verify/archive sections. PASS.
- **A4 — `code-doc` + `deep-drill`.** WHY four conditions present once,
  unchanged (`code-doc/SKILL.md:39`); deep-drill anchor 1 only extended
  (Task 4 Step 10 verification). No flow/contract change. PASS.

## Spec B locked constraints
- **B1 — never-clobber.** `skills/codocu/references/onboarding.md:17` "If
  `codocu.md` already exists it is authoritative. Do not overwrite it." —
  intact; onboarding.md received zero edits in this unit. PASS.
- **B2 — read-only until explicit go-ahead.** `onboarding.md:6` "the only
  place `codocu.md` gets written, and only on an explicit go-ahead." —
  intact. PASS.
- (B behavioral checks — exactly-3 questions, skeleton+`TBD`, no
  repo-conditional noise — are scored from R3/R4 transcripts by the scoring
  subagent, not here.)

## Spec C locked constraints
- Covered by Task 5 Step 3 (all PASS): 7 Principles; `docs/tuning.md` 5 dials
  (4 originals byte-unchanged); 6 house-rule lines each carrying exactly one
  appended reader-economy clause (`init`/`sync` untouched); sibling semantics
  intact; no out-of-scope edits (`git status` cross-checked vs session start).

**Verdict: PASS — no locked constraint regressed by the combined A+B+C edits.**
