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

## Adding a dial
When a new behavioral knob emerges, add a section here with: setting,
expressed-in locations, and the strengthen/devalue/remove directions — then
propagate.
