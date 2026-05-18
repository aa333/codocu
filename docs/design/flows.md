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

## Moves

- **`/codocu` — orient.** The state-aware entry point. Read-only: classify
  the state, give an orientation brief, recommend a sized next move. Branches
  to setup, deep drill, or conflict resolution only on an explicit user
  choice.
- **`/codocu:init` — set up.** Goes straight to the setup (onboarding)
  branch.
- **`/codocu:propose` — intent → plan.** A ProposalSummary in the
  conversation, iterated to approval, then a plan in `docs/plans/`.
- **`/codocu:apply` — work a plan.** Resume an existing plan; do the
  unchecked steps; suggest `fold` when done.
- **`/codocu:doc-code` — docs are the spec.** Write a plan to implement what
  the docs describe, then implement it.
- **`/codocu:code-doc` — code is the truth.** Bring docs up to date. Small,
  clear delta: update directly, no plan. Large or brownfield: proposal →
  plan.
- **`/codocu:fold` (alias `/codocu:sync`) — close out.** Verify what shipped
  against code and git history (never the checkboxes), bring the docs along,
  archive the plan, set `Synced`.

## Setup (onboarding)

Runs when the project is uninitialized and the user wants to proceed, on an
explicit `/codocu:init`, or to revise conventions. It classifies the repo,
asks the three intent questions that can't be derived from it (doc
granularity, what else to document, fold behavior for incomplete plans),
fills `codocu.md` from `templates/codocu.md`, and never overwrites an
existing `codocu.md`. The existing-docs stance is a rollout strategy only —
it never weakens the doc standard.

## Gates

The invariants every flow honors:

- Read-only orientation writes nothing — no `codocu.md`, plan, code, or
  docs. A prompt that pre-empts the setup choice makes orientation skip the
  offer and just do the read-only look.
- Setup writes `codocu.md` only on an explicit go-ahead; never clobbers an
  existing one.
- The deep drill is opt-in, read-only, and runs only on an explicit accept;
  its cost is disclosed first and it is tiered (inline / plan-gated /
  hand-off), so the user controls cost by construction.
- Conflict resolution (both sides changed, no active plan) is its own gated
  branch; if `codocu.md` is absent it stays read-only and does not create
  it.
- `fold` trusts code and git history, not `[ ]`/`[x]`.

The deep-drill, conflict-resolution, reconciliation-plan, and onboarding
procedures live as on-demand references in the `codocu` skill — loaded only
when that branch is actually taken.
