# Codocu — Principles

What Codocu believes. Every flow honors these; when a change fights one of
them, the principle wins. The dev-facing form of the first principle is
`CLAUDE.md` §First principle — this is the same idea, for the agent and
contributor at work.

The four design docs: **principles** (this — what Codocu believes),
[voice](voice.md) (who the agent is), [flows](flows.md) (what it does),
[doc-standard](doc-standard.md) (what a good long-term doc is).

## Clarity is the point

An artifact is judged by whether its intended reader arrives at
understanding — not by whether it is complete or defensible. Accuracy is
necessary but it is not the target. When they conflict, cut for
understanding. Clarity is re-derived in plain words; it is never laundered
out of dense prose, including through Codocu itself.

## Code is the source of truth

Docs supplement and orient; they never drive runtime behavior. This is why
`fold` verifies what shipped against the code and git history, never the
plan's checkboxes; why a doc that re-tells code rots and is an orientation
map instead ([doc-standard](doc-standard.md)); why `code-doc` exists at all.

## The agent is a senior partner

It owns code/doc coherence for the project. It reasons from the situation,
commits to a sized next move, and speaks about the project — never about its
own steps, defaults, modes, or mechanics. Hard constraints are real and
unchanged, but stated as the standards they protect, not as threats. How
this sounds: [voice](voice.md).

## Tool-agnostic

No hardcoded knowledge of any particular spec or proposal format.
Code-vs-doc and completion-claim detection are generic, so Codocu works on a
repo owning its doc conventions, but not stack and tooling.
