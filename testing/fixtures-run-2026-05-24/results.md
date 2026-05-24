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
