# B-core — seeds for a fresh brainstorm

> Not a spec — three threads to pick up when B-core gets its own session.
> Context: Track B (`2026-05-22-track-b-decomposition.md`); B-extract is done,
> its assets live in `docs/corpus/`.

- **Drop the repo-state classification.** v0.1 tracked synced / desynced / dirty
  and routed off it. v0.2 tracks only **inited** (`codocu.md` exists) vs
  **uninited**. The three-state machine and everything it drove (routing,
  conflict-resolution) goes away with the removed flows.

- **Question the generative/subtractive split.** The decomposition frames B-core
  as two modes — subtractive for existing bad docs, generative for fresh repos.
  Before building that, decide whether the division is real or whether one rule
  covers it: *enough local references exist → use them; if not → fall back to the
  shipped samples.* The "mode" may just be a reference-availability check, not a
  repo condition the skill has to detect and name.

- **Stub a parallel reviewer.** B-core's doc-checking leans on the B-review
  reviewer, which isn't built. Ship at least a simple stub reviewer subagent
  (runs in parallel, rules = the smell catalog) that B-review expands later —
  enough to wire the interface now.
