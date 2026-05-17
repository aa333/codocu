# Test Report — Long-Term Doc Style (Spec A) — Run NN

- **Date:** YYYY-MM-DD
- **Plugin state:** <git-sha or tag>
- **Model:** Opus
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS | FAIL (if FAIL, restore run? yes/no)
- **Run type:** assessor (fixture) | writer (scratch)
- **Skill state under test:** <baseline / spec-only / full-propagation>

## Prompt used

> <exact prompt given>

## What the agent did

<3–6 lines>

## Functional score (retained — must not regress; assessor runs only)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty |  |  |
| Claimed-complete≠done caught | archetypes→strategy divergence surfaces |  |  |
| Read-only verify PASS | state-guard fingerprint unchanged |  |  |

## Voice non-regression (retained; all runs)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| No scaffolding leak | no internal step numbers, no "per the skill" / "I default to", no recited numbered checklist in user-facing prose |  |  |
| Reads as senior partner | added WHAT-summary prose reads as a colleague reasoning, not a script |  |  |

## WHAT-summary score (new)

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Assessor: over-bound flagged | explicitly flags an over-bound doc (the fixture's OpenSpec specs re-tell code) and names the WHAT-summary bound as the reason — not a generic "docs are messy" |  |  |
| Assessor: under-bound flagged | explicitly flags a doc with no coarse orientation map as under the bound, citing the bound |  |  |
| Writer: anchor honored | produced/updated WHAT-summary names only purpose / place-in-system / public contract / direction |  |  |
| Writer: drift test passes | no sentence in the WHAT-summary would be falsified by an internal-only refactor (no per-function/field/algorithmic/control-flow detail; no code unless the snippet IS the contract) |  |  |

Concrete writer FAIL example: summary lists internal helpers or private field
names ("calls `_recompute_cache()`, stores `self._dirty`").
Concrete writer PASS example: "Auth module — verifies credentials for the API
layer; depends on the token store; exposes `login`/`logout`; moving to
refresh-token rotation next."

## Reader-experience score (new — Spec C; orthogonal to WHAT-summary)

Holistic, scored separate-session. NOT a writer gate — an observation, like
the WHAT-summary assessor rows. Reader economy is a different axis than scope:
an in-bound doc can still be an exhausting read.

| Metric | Pass condition | Got | Note |
|---|---|---|---|
| Assessor: bad read flagged | flags an existing doc a busy developer would abandon — redundancy, duplication, padding, answer buried — as a finding **distinct from** the WHAT-summary scope finding, not collapsed into a generic "docs are messy" |  |  |
| Writer: reads answer-first | a doc/plan/brief the agent produced leads with the answer, says each thing once, no padding a busy reader would resent |  |  |
| Voice non-regression | the added reader-economy clauses read in-voice — no scaffolding leak, no recited checklist (reuses the voice rubric) |  |  |

Concrete assessor FAIL example: "the docs are messy and out of sync" (generic;
no reader-economy axis named). Concrete assessor PASS example: "beyond scope,
`auth.md` explains the token flow in three places and buries the one fact
you'd come here for — a busy dev would bail." Concrete writer FAIL example: a
brief that restates every step before answering. Concrete writer PASS example:
a close-out that states the outcome first, then the detail, once.

## Defects / observations

-

## Change for next run

-
