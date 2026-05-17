# Combined Spec A + B + C — run summary (2026-05-17)

**LOCAL / UNCOMMITTED** (real non-anon target — see `setup-changes.md`).
Plugin: master `86b14c7` + uncommitted A+B+C working tree. Post-change only
(no pre-edit baseline this pass — owner-deferred). All scoring done
separate-session by fresh transcript-only subagents (no self-grading).

## Scoreboard

| Run | Scenario | Read-only | Functional | WHAT/Reader (writer) | WHAT/Reader (assessor) | Voice | Verdict |
|---|---|---|---|---|---|---|---|
| R1 | Assessor, dirty neph | **PASS** (×2) | PASS (Dirty, claimed≠done, triage; rename PARTIAL) | — | **FAIL/PARTIAL** (bound never invoked) | PASS | Orientation strong; **assessor reader/WHAT not demonstrated** |
| R2 | Writer, scratch (code-doc) | n/a | n/a | **PASS** (anchor + drift + answer-first) | — | PASS | Clean pass (proposal; file approval-gated) |
| R3 | Onboarding bare | PASS (proposal-only) | PASS (3-core, no noise, TBD) | — | — | PASS | Pass |
| R4 | Onboarding brownfield | PASS (proposal-only) | PASS (stance + note, TBD) | — | — | PASS | Pass |
| Guard | Locked constraints A+B+C | — | PASS (`guard.md`) | — | — | PASS | No regression |

## Narrative

- **Writer side (Spec A WHAT-summary + Spec C reader-economy): PASS.** R2's
  proposed `auth.md` rewrite is a refactor-proof, answer-first orientation map
  naming only purpose/place/`login`+`logout`/direction — zero internal names —
  in senior voice.
- **Onboarding (Spec B) + voice/reader non-regression: PASS.** Bare suppresses
  docs-stance noise; brownfield handles + records the stance; both proposal-
  only, `TBD`-seeded, senior voice.
- **Assessor side (Spec A + C live finding): NOT demonstrated.** In R1 the
  agent did excellent orientation/triage but **never invoked the WHAT-summary
  bound or a reader-economy critique** on the target's docs. The over-bound
  and bad-read rows FAIL; under-bound PARTIAL.
- **Read-only contract held** (state-guard VERIFY PASS before *and* after the
  battery). **Locked constraints intact** (`guard.md`, file:line evidence).

## Open findings / threats to validity

1. **Assessor reader/WHAT gap is the headline — but confounded.** Three
   plausible causes, not disambiguated by this pass:
   (a) the propagation genuinely doesn't fire in live orientation;
   (b) the target offered no clean in-bound-but-bad-read doc — its authored
   docs are mostly empty `docs/actual/` scaffold + legacy OpenSpec, which the
   agent treated as *divergence/staleness* (correct) rather than a WHAT/reader
   critique; the canonical over-bound example (the anonymized fixture's
   OpenSpec specs) wasn't framed as such here;
   (c) no baseline, so we cannot say whether this regressed or never fired.
   The agent also never *stated* "no in-bound docs to assess," so it didn't
   reason about the dimension at all — mild evidence for (a).
2. **No test-first baseline.** The instrument-discriminates check (current
   skills FAIL the new criteria pre-edit) was not run — owner-deferred.
3. **Writer scored from the proposal, not a written file** (code-doc approval
   gate + single-turn headless). On-disk `auth.md` stayed drifted.
4. **Spec B "incompatible/dirty no-interview" sub-check unexercised** (target
   is initialized) — n/a, by recorded delta.

## Recommended next steps (owner's call)

1. **Targeted assessor re-run** against a repo (or scratch) that contains an
   explicit in-bound-but-bad-read doc (redundant/padded/buried-answer) AND a
   clean over-bound doc, with a **pre-edit baseline** (`86b14c7` via throwaway
   worktree) — this disambiguates cause (a) vs (b)/(c). Until then the
   assessor-side reader-economy claim is **unverified**, writer-side is
   **verified-pass**.
2. If (a) is confirmed: sharpen the `codocu` orientation-brief + `deep-drill`
   anchor clauses (the tuning dial's "Strengthen" direction) so the live
   finding actually fires, then re-run.
3. Treat onboarding + writer + voice + read-only + locked-constraints as
   **green** for this combined unit.
