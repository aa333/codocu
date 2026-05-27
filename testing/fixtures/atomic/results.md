# Atomic review fixture run — 2026-05-24

## Environment caveat

The codocu plugin was not loaded as a plugin in the session that ran these
fixtures (the active plugin was superpowers). The runs below are **simulations**:
a general-purpose subagent was given the codocu-reviewer prompt inline and
pointed at each fixture file. This validates the *prompt content*, not the
plugin's harness registration.

Real verification happens in a fresh session launched with:
```
claude --plugin-dir C:/repos/codocu
```
There, `/reload-plugins` will register the codocu skill and the codocu-reviewer
subagent, and the Task tool will accept `subagent_type: codocu-reviewer`.

## Smoke test results (3 fixtures of 15)

| Fixture | Kind | Expected | Result | Pass |
|---|---|---|---|---|
| mf-stray-todo | must-flag | flag `stray-todo-in-longterm-doc` | flagged correctly | ✓ |
| mf-summary-restates-signature | must-flag | flag `summary-restates-signature` | flagged correctly | ✓ |
| mnf-system-doc-opening | must-NOT-flag | no hits | flagged `doc-far-from-anchor` + 2 uncataloged | ✗ |

## Diagnosis of the failure

The reviewer over-applied `doc-far-from-anchor` to a markdown opening paragraph.
The catalog's trigger for that smell is "descriptions of many *symbols* are
gathered into one block (a class docstring, a banner) instead of sitting on
each symbol" — a code-level smell. The reviewer stretched the trigger to fit a
narrative paragraph that talks about Caps and AccessService at a system level,
which is exactly the system-doc opening that the corpus calls out as correct.

Two uncataloged hits also pushed too hard:
- "Main UI guard" heading vs body — defensible but not a principle violation.
- ADR rationale strength — stylistic preference, not a principle violation.

Root cause: the original `How to review` step 3 said *"check whether the doc
carries an instance"* — too permissive. The reviewer interpreted the smells
loosely.

## Fix applied

`agents/codocu-reviewer.md` updated with a tightened step 3 and a new
**Conservative bias** clause:

- Step 3 now requires the doc to match the trigger *as written*, and notes
  most smells are scoped (some are code-level, not markdown narrative).
- Conservative bias clause: "A false positive on good content erodes trust
  faster than a missed bad smell. When the doc looks fine, return `good`."

## Recommended next steps for the user

Run the full eval pass in a `--plugin-dir`-loaded session:

1. Launch `claude --plugin-dir C:/repos/codocu` in a fresh terminal.
2. Run `/reload-plugins` — expect 1 plugin, 1 skill (codocu), 7+ agents
   (the existing 6 plus codocu-reviewer).
3. Invoke the reviewer on each of the 15 fixture files in
   `testing/fixtures-run-2026-05-24/`. Either via `/codocu` (which would
   route to atomic review), or directly via the Task tool with
   `subagent_type: codocu-reviewer`.
4. Tabulate pass/fail per fixture. Target ≥80% pass.
5. If the must-NOT-flag side still shows false positives after the
   conservative-bias adjustment, the next lever is sharper trigger language
   in the smell catalog itself (e.g., add a `Scope:` line to each smell
   distinguishing code-level vs markdown-level).

## Fixtures staged but not yet run

In `testing/fixtures-run-2026-05-24/`:

Must-flag:
- mf-consumer-not-system-block.md — expect `consumer-not-system`
- mf-stray-todo.md — ran, PASS
- mf-unmaintainable-aggregation.md — expect `unmaintainable-aggregation-list`
- mf-summary-restates-signature.py — ran, PASS

Must-NOT-flag:
- mnf-system-doc-opening.md — ran, FAIL (fix applied to agent)
- mnf-file-link-with-backlink.md
- mnf-adr-as-business-rationale.md
- mnf-single-class-module-title.py

Eight fixtures staged. The remaining seven of the design's 15 (other consumer-not-system, doc-far-from-anchor, the remaining positives) can be added by following the same pattern: copy the Input block from `docs/corpus/eval-fixtures.md`, wrap in a stub host doc matching the Context line.

---

# Fold smoke test — 2026-05-24

## Environment caveat

Same as the codocu-reviewer run above: the codocu plugin was not loaded in the
session that ran this test. The fold-verifier run below is a **simulation**: a
general-purpose subagent was given the verifier prompt inline and pointed at
the target plan. This validates the *prompt content*, not the plugin's harness
registration.

Real verification — including end-to-end `/codocu:fold` invocations, the
delegation handoff at step 4, and inbox processing at step 6 — requires a
fresh session launched with `claude --plugin-dir C:/repos/codocu`. Those
remain on the user.

## Verifier in isolation (Task 5, Step 1)

Target: `docs/plans/2026-05-22-track-b-extract.md`. Documented as done at
commit `91d5b97`.

Result: `Overall: partial`. The verifier produced a well-formed structured
report with conservative-bias correctly applied to the process-directive step
(Step 1 → `unverifiable`), grounded shipped verdicts for the corpus-extraction
steps (Steps 2–5, with file paths and line-number evidence), and **caught a
real discrepancy on Step 6**: the plan's scope guard says principle and
doc-standard files must not be touched during extraction, but commit `91d5b97`
modifies `docs/design/principles.md`, `doc-standard.md`. The
plan's status header does not declare this deviation.

The prediction in the implementation plan was `foldable`. The verifier's
`partial` is the better answer. This is the verifier doing its job —
surfacing a real discrepancy rather than rubber-stamping. The implementer
(planning) missed what the verifier caught.

Pass on all four design criteria:

- Structured output emitted in the exact schema.
- Tools used appropriately (Read for the plan, Grep for evidence, Bash for
  `git show --stat`).
- Conservative bias fired on the abstract step.
- The Summary lines on shipped steps were business-words, not step text
  restated (e.g., "All five Neph source files are cited by name across the
  four assets, evidencing a full walk of the corpus").

## End-to-end fold flow (Task 5, Steps 2–4)

Not run. Requires the plugin to be loaded so `/codocu:fold` resolves and
`Task(subagent_type: fold-verifier)` is accepted. To run:

1. Launch `claude --plugin-dir C:/repos/codocu` in a fresh terminal.
2. `/reload-plugins` — expect 2 skills (`codocu`, `fold`) and 2 plugin
   agents (`codocu-reviewer`, `fold-verifier`).
3. Invoke `/codocu:fold` in plan mode first to see step 1 / 2 / 3 behavior
   without applying changes. Verify it fans out the verifier in parallel
   (one Task call per plan, all in one message), aggregates verdicts, and
   asks the user about partials rather than auto-archiving.
4. Then invoke `/codocu:fold` in normal mode and walk through step 4
   (delegation to `/codocu`), step 5 (archive), step 6 (inbox), step 7
   (report). Verify the delegation actually reads `skills/codocu/SKILL.md`
   mid-flow rather than guessing at Place.

## Open gaps from smoke test

- End-to-end behavior (steps 2–7 of fold's flow) is unvalidated. The verifier
  prompt is in good shape; the orchestrator skill and the delegation handoff
  are unverified.
- The verifier's `partial` finding on track-b-extract surfaces a real
  question the user may want to resolve before folding that plan: were the
  principle/doc-standard edits in `91d5b97` deliberately bundled with the
  extraction (in which case the scope guard is stale), or was the guard
  violated (in which case it merits a follow-up note)? Not fold's call —
  the user decides.

## Design revision after this run (2026-05-24)

This first smoke test surfaced two structural problems with the
per-plan-subagent shape:

1. **Cross-plan context missing.** A verifier seeing one plan at a time
   can't recognize that `b-core-design.md` pairs with
   `b-core-implementation.md`, or that `b-core-seeds.md` is superseded by
   the design — both essential for deciding what to archive.
2. **Scale.** One subagent per plan means N model calls for N plans, even
   when most plans (outlines, decompositions, designs, seeds) can be
   classified by header alone without verification.

Fold's design was revised the same day:

- `agents/fold-verifier.md` deleted.
- Fold now runs entirely in the main thread.
- Step 1 of the flow pre-classifies every plan by header into one of six
  categories (outline, decomposition, design, brainstorm/seeds,
  superseded, implementation). Only implementation plans fall into
  step 2 (mechanical verification).
- The track-b-extract verification result above stands — the conservative
  bias and grounding logic transfer one-for-one into the in-thread version.

The next smoke test will run against the revised design.

## Second design revision — strip-down (2026-05-24)

Side-by-side test: invoking the (first-revision) fold skill vs. naked Claude
against the same plan set. Naked Claude produced equivalent classification at
one-third the cost. The one place fold caught something naked Claude missed
was the conservative-bias call on b-core-implementation (validation
documented as deferred; archive would be premature). That came down to a
single rule, not the whole 7-step flow.

So the procedural ceremony was cut:

- `skills/fold/SKILL.md` reduced from ~60 lines to ~25 — frontmatter, voice
  anchor, load-first instruction, a short conventions list, and a closing
  "land it on the user's ask" line. No flow, no classification categories,
  no procedural gates.
- `docs/plans/2026-05-24-fold-implementation.md` deleted — implementation
  is "edit two files," no plan needed.
- Design doc rewritten to reflect the lighter shape and to record *why* the
  earlier shapes were cut (subagent removal in revision 1, procedural-flow
  removal in revision 2).
- `skills/codocu/SKILL.md` Place warrantedness-gate edit stands; the
  conventions list in fold's SKILL.md depends on it.

The next smoke test runs against the lighter skill.

## Lighter-skill smoke test — 2026-05-24

Ran `/codocu:fold` end-to-end against the live `docs/plans/` set (eight plans).
Skill loaded `codocu.md`, classified each plan against code and shipped commits,
correctly held the b-core pair and fold-design itself on outstanding validation,
held the v0.2 outline and track-b decomposition as parents of open work, and
surfaced the scope-guard discrepancy on track-b-extract for owner decision before
archive. Owner approved archive of track-a-methodology, track-b-extract, and
b-core-seeds; deferred the b-core pair. This session also serves as fold's own
end-to-end validation — closing the deferred smoke test.
