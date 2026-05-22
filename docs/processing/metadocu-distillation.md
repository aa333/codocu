# Distilling METADOCU-labelled sources into the corpus

How to turn a sibling repo's `#METADOCU`-labelled documentation into the
committed assets under [`docs/corpus/`](../corpus/). This is the method, not a
log of any one run — Neph is the worked example throughout, but the process is
meant to work on the next labelled repo too.

## When to run this

Run it when a labelled source appears or changes: a sibling repo carries
`#METADOCU` annotations on its docs and code, and you want those judgements
reflected in the corpus the reviewer and writer skills derive from.

It is **offline and one-way.** It never runs at a user's request, never reads
the raw corpus at runtime, and produces nothing that ships into a user repo.
Today it is done by hand; it is structured so a skill could later do it (see
[boundaries](#boundaries-and-future)).

## The core constraint

A `#METADOCU` label is a *teaching signal about a placement choice*, not text to
reuse. The labelled instance shows how someone decided where a piece of
documentation belongs — and often shows a bad instance on purpose. So two things
must hold for every asset you produce:

- **No label token is ever copied.** Assets carry the distilled signature, rule,
  or before/after pair — not the `#METADOCU` annotation itself.
- **The raw source stays in the sibling repo.** Each asset entry instead cites
  it with a `Source:` line, so the judgement is traceable without dragging the
  corpus along.

A bad instance reproduced into a runtime asset teaches the model to reproduce
the anti-pattern. That is the failure this whole process is built to avoid.

## The method

1. **Locate the labelled material.** Walk the source repo for `#METADOCU`
   labels and the code breadcrumbs that pair with them. A label sits next to the
   doc or code it judges; read both.
2. **Classify each label** by the lesson it carries:
   - a **negative** judgement ("this is wrong, and why") → a smell;
   - a **positive structural** judgement ("this placement is correct") → a
     placement rule;
   - a **voice before/after** ("this phrasing replaced that one") → a voice pair.
   Some labels carry more than one lesson. Route by the *dominant* one and note
   the rest; don't split one label into three thin entries.
3. **Route to the matching asset, and always mint a paired fixture.** Every
   routed label becomes both an entry in its asset *and* a grader in
   [`eval-fixtures.md`](../corpus/eval-fixtures.md): a must-flag fixture for a
   smell, a must-NOT-flag for a placement rule, a must-produce for a voice pair.
   The asset teaches; the fixture proves the teaching took.
4. **Dedupe.** Several labels often point at one underlying smell. Collapse them;
   a catalog of near-duplicates is harder to match against than a tight one.

The asset formats themselves live in `docs/corpus/` — follow what's already
there rather than restating it here.

## Invariants

These hold for every asset, every time:

- **No `#METADOCU` token appears in any asset.**
- **Bad instances live only in `eval-fixtures.md`.** The smell catalog and
  placement rules carry signatures and reasoning, never the anti-pattern.
  (Voice pairs are the one exception: a "before" is the contrast that teaches, so
  it belongs there.)
- **Every asset entry carries a `Source:` line.**
- **Every fixture carries a `Context:` line** — see below.

## Validation: the cold-reader test

Distillation is judgement-heavy, so verify it the way you'd verify any
judgement: hand each finished asset to a reader who has none of your context.

Run a fresh agent **per asset**, give it *only that one file*, and have it grade
every entry YES / SOMEWHAT / NO on whether the rule and its justification are
understandable cold. Anything below YES is a self-containment failure to fix.

Two findings from doing this matter enough to plan around:

- **Fixtures must be fully self-contained.** A placement judgement is judged
  against its *host document* — the same ADR is right in one doc and wrong in
  another. An instance pulled out of context is unjudgeable. So every fixture
  needs a `Context:` line naming where it lived and what that document is about.
- **Separate genuine defects from context-starvation.** The smell catalog,
  voice pairs, and placement rules are consumed *alongside* `principles.md` and
  `doc-standard.md`, so they may lean on shared vocabulary ("breadcrumb",
  "negative-space", "ADR"). A cold reader will flag those terms as unclear —
  that's an artifact of starving it, not a defect. Fixtures get no such
  allowance; they travel alone.

## Judgement calls

- **Demote, don't ship weak.** When an entry is too thin to teach, can't be
  graded without code the fixture doesn't include, or rests on a rule you're not
  yet sure of, move it to that asset's `## Not yet distilled` section with the
  reason. Faithfulness to a label is not the same as teaching value — a real
  label can still make a poor asset.
- **Park principle ideas, don't apply them.** Distilling surfaces ideas for
  improving `principles.md` or `doc-standard.md`. Collect them in a notes file;
  changing the design docs mid-distillation mixes two jobs and corrupts both.
  Triage the notes later, on purpose.

## Boundaries and future

Keep it manual while the corpus is tiny. A generator calibrated on one or two
sources overfits to them; build the assets by hand, then run them against the
*next* labelled source as a live test before investing in automation.

This doc is the foundation for that automation — `TD-corpus-enrichment-skill`
in [`docs/todo.md`](../todo.md), which would regenerate the assets from new or
updated labelled sources. The structure here (stable steps, invariants,
provenance lines, a validation pass) is what makes that skill possible to
specify later.
