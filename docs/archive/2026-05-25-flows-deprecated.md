// deprecate?
# Codocu — Flows

What Codocu does: the states it reasons about, the moves between them, and
the gates that bound them. Operational detail lives in the skills; this is
the map.

## States

Orientation diagnoses one of three:

- **Synced** — code and docs agree. A plan describing *future* work is still
  Synced; future work is not a desync.
- **Desynced** — one side moved; the other is internally coherent.
- **Dirty** — both sides moved, or they contradict.

The persisted marker is a single line in `codocu.md`:
`> Codocu sync state: TBD | Synced | Dirty`. Setup seeds `TBD` (real state
unknown until first assessed). `propose`, `apply`, `doc-code`, and a large
`code-doc` set `Dirty` for the duration of the work; `fold` sets `Synced` on
a successful fold; a small `code-doc` sets `Synced` directly. "Desynced" is
an orientation diagnosis, not a marker any flow writes.

A non-empty `docs/inbox/` is not a fourth state. It holds long-term docs
other agents produced in their own tone, not yet processed — an outstanding
*folding obligation*, surfaced by orient and cleared by `fold`.

## Moves

- **`/codocu` — orient.** The state-aware entry point. Classify
  the state, give an orientation brief, recommend a sized next move. 
- **`/codocu:init` — set up.** Goes straight to the setup (onboarding)
  branch.
- **`/codocu:propose` — intent → plan.** A proposal summary in the
  conversation, iterated to approval, then a plan in `docs/plans/`.
- **`/codocu:apply` — work a plan.** Resume an existing plan; do the
  unchecked steps; suggest `fold` when done.
- **`/codocu:doc-code` — docs are the spec.** Write a plan to implement what
  the docs describe, then implement it.
- **`/codocu:code-doc` — code is the truth.** Bring docs up to date. Small,
  clear delta: update directly, no plan. Large or brownfield: proposal →
  plan.
- **`/codocu:fold` (alias `/codocu:sync`) — close out.** Verify what shipped
  against code and git history (never the checkboxes), fold any
  `docs/inbox/` drafts into the evergreen docs, bring the docs along,
  archive the plan, set `Synced`.

## Setup (onboarding)

Runs when the project is uninitialized and the user wants to proceed, on an
explicit `/codocu:init`, or to revise conventions. It classifies the repo,
asks the three intent questions that can't be derived from it (doc
granularity, what else to document, fold behavior for incomplete plans),
fills `codocu.md` from `templates/codocu.md`, and never overwrites an
existing `codocu.md`. The existing-docs stance is a rollout strategy only —
it never weakens the doc standard.



The deep-drill, conflict-resolution, reconciliation-plan, and onboarding
procedures live as on-demand references in the `codocu` skill — loaded only
when that branch is actually taken.
