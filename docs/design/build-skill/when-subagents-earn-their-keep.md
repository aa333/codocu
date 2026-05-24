# When subagents earn their keep

Subagents add real cost — fresh model invocation, context loading, no shared
memory with the main thread. They earn that cost only when they offer
something the main thread can't get for free.

Two patterns from v0.2 development illustrate when the math works and when
it doesn't.

## The codocu-reviewer subagent (worth it)

Atomic per-doc reviewer. Loads the smell catalog plus principles, applies
them against one doc, returns a structured report. Three things justify the
cost:

- **Specialized knowledge to load.** The smell catalog is ~50 lines of named
  anti-patterns with triggers. Loading it once per review — rather than
  carrying it in the main thread's context for every conversation — keeps
  the main skill light.
- **Real isolation value.** One doc's findings shouldn't pollute another's
  review. A smell hit in doc A shouldn't bias the model's read of doc B.
- **Fan-out is natural.** When reviewing N docs, N reviewers run in parallel
  from a single dispatch message. The work parallelizes cleanly.

## The fold-verifier subagent (not worth it; removed)

Per-plan verifier. Failed all three tests:

- **No specialized knowledge to load.** Plan verification is mechanical —
  `git log`, `Grep`, file existence checks. The instructions are short and
  main-thread-suitable; loading them per plan is overhead, not architecture.
- **No isolation value.** Plans don't pollute each other's verification.
  There's no risk in running them together; the main thread holds the
  evidence already.
- **Cross-plan context is required.** Plans relate to each other —
  supersession, design/impl pairs, decomposition parents. A subagent that
  sees one plan at a time literally cannot do the work right. Naked main
  thread reading the whole tree was strictly better than a fan-out of
  isolated verifiers.

## The test before adding a subagent

> What does it know that the main thread doesn't, and what does isolation
> protect?

If both answers are "nothing," it's overhead, not architecture. Ship the
work in the main thread with a convention list instead.

Common false positives:

- *"It does verification, that feels atomic"* — atomicity is necessary, not
  sufficient. Verification still needs to know whether evidence is missing
  is missing because it's not there or because the wrong place was checked,
  which is a cross-call question.
- *"It scales by parallel fan-out"* — only true when N is high and each call
  is independent. If most candidates classify trivially in the main thread
  without spawning anything, parallel fan-out is a non-feature.
