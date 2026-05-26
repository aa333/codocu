# Reference docs — scorer only

The agent under test never sees this directory.

Contents:
- `captcha.md` — human-written long-term doc for the captcha system, with
  `#METADOCU:` annotations encoding specific verdicts (renameable symbols,
  transcription, ADR misplacement, code duplication, etc.). The scorer's
  METADOCU-agreement check asks: of the failure modes these annotations
  flag, how many does the agent's produced doc reproduce, avoid, or
  introduce new?
- `modules.md` — human-written cross-module doc. No annotations; included
  because `captcha.md` cross-references it (`[[modules]]`), so the scorer
  has the full reference context.

Paths in the reference (`src/core/module.py`, `src/app.py`, `MODULE_CLASSES`)
match the fixture's layout exactly. Scoring compares failure *patterns*,
not identifier strings — but identifiers stay aligned so reading both
side-by-side is unambiguous.
