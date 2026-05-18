# Tuning Registry — DEFERRED (parked 2026-05-17)

Parked, not adopted. The dial-registry idea is sound — developer-time
behavioral knobs with a defined path from a setting to the skill text that
expresses it — but this execution is not. The handles are opaque, there is
no operable flow for how an edit here propagates into the skills, and in use
it was unworkable ("no idea how to work with it"). It also added exactly the
meta-indirection layer the clarity principle (`CLAUDE.md` §First principle)
exists to remove.

Revisit with a real design — see the `docs/todo.md` entry. The original
content is preserved below verbatim.

---

# Codocu — Behavioral Tuning Registry

Developer-facing. **Not read at runtime.** The skill prose is the source of
truth for behavior; this file is the map: every behavioral dial, its current
setting, and exactly where in the skill text that setting is expressed.

**The one rule:** retuning always goes through *edit here → propagate*.
Change the setting in this file, then run `/codocu:doc-code` on this repo to
carry the change into the skill-text locations listed for that dial. An
ad-hoc skill edit that skips this file silently desyncs the registry.

## Dials

### Voice intensity
How strongly the skills carry the senior-partner voice vs. plain procedure.
- **Setting:** Senior-partner (full).
- **Expressed in:** every `skills/*/SKILL.md` — the opening framing lines and
  the in-skill house rule ("Operate as the engineer who owns this project's
  code/doc coherence…"); most concentrated in `skills/codocu/SKILL.md` and
  `skills/fold/SKILL.md`.
- **Devalue:** flatten the opening framing toward neutral procedure; keep the
  house rule regardless — scaffolding leak is never desirable.

### Recommendation assertiveness
Whether orientation recommends a sized path or just reports options.
- **Setting:** Recommends (a sized path, then asks for the go-ahead).
- **Expressed in:** `skills/codocu/SKILL.md`, the "Recommend, don't
  enumerate" section.
- **Devalue:** soften "say what you'd do" toward "lay out the options"; do
  not revert to an opaque unranked menu — that was the original defect.

### Reconciliation-plan-shape weighting
How prominently orientation reaches for the tiered reconciliation plan.
- **Setting:** Default — recommended only for a genuinely dirty/multi-area
  repo; direct fix for a simple desync.
- **Expressed in:** `skills/codocu/SKILL.md` ("Recommend, don't enumerate",
  the dirty/multi-area bullet) and
  `skills/codocu/references/reconciliation-plan.md` (the adapt-don't-recite +
  not-for-simple-cases clause).
- **Strengthen:** widen the trigger toward multi-area-ish repos.
- **Devalue:** narrow the trigger to only the worst tangles.
- **Remove:** delete the dirty/multi-area bullet's reference pointer in
  `skills/codocu/SKILL.md` and delete
  `skills/codocu/references/reconciliation-plan.md`; orientation then
  recommends only per-area direct fixes.

### Existing-docs stance authority
Whether the onboarding existing-docs stance may weaken the WHAT-summary bound
for a project, or is purely a rollout strategy.
- **Setting:** Option 1 — rollout-only (the stance controls scope/timing
  only; the WHAT-summary bound stays invariant; onboarding never offers to
  soften or disable it).
- **Expressed in:** `skills/codocu/references/onboarding.md` §6 — the final
  "The standard itself stays invariant under every stance" paragraph.
- **Strengthen (Option 2 — softenable):** rewrite §6's final paragraph so the
  stance may, when chosen, dial the WHAT-summary bound down/off for the
  project's legacy docs, recorded in `codocu.md`'s existing-docs note.
- **Devalue / remove:** not applicable — Option 1 is the floor; there is no
  setting weaker than rollout-only.

### Reader economy
How hard the skills push every doc/plan/brief to read well for a busy reader
(lead with the answer, say it once, no bloat) vs. leaving prose quality to
chance. Orthogonal to the WHAT-summary bound — that governs scope; this
governs the read.
- **Setting:** On — internalized in the shared house-rule voice; live
  orientation/deep-drill flags reader-economy defects in existing docs as a
  finding distinct from the scope finding; one holistic reader-experience row
  (assessor + writer) in the test rubric.
- **Expressed in:** the shared `_Operate as the engineer…_` house-rule line in
  every `skills/*/SKILL.md` that carries it (`codocu`, `fold`, `propose`,
  `code-doc`, `doc-code`, `apply`); `skills/propose/SKILL.md` and
  `skills/doc-code/SKILL.md` (plan-for-a-reviewer clause);
  `skills/code-doc/SKILL.md` (small + brownfield paths) and
  `skills/fold/SKILL.md` ("Bring the docs along"); `skills/codocu/SKILL.md`
  orientation brief and `skills/codocu/references/deep-drill.md` anchor 1
  (live finding); `testing/2026-05-17-longterm-doc-style/
  report-template-whatsummary.md` (Reader-experience row).
- **Strengthen:** sharpen the house-rule clause toward an explicit cut-test;
  widen the live orientation finding.
- **Devalue:** soften the live finding to writer-side only; keep the
  house-rule clause regardless — internalized economy is never undesirable.
- **Remove:** drop the house-rule clause and the rubric row; orientation then
  judges only the WHAT-summary scope bound.

## Adding a dial
When a new behavioral knob emerges, add a section here with: setting,
expressed-in locations, and the strengthen/devalue/remove directions — then
propagate.
