# B-extract — Corpus Distillation — Spec

> Status: ✅ executed 2026-05-23, committed in `91d5b97`. Sub-project of Track B
> (see `2026-05-22-track-b-decomposition.md`).
>
> **Execution outcome.** Five files in `docs/corpus/`: `smell-catalog.md` (6
> smells; `leaks-changeable-implementation` kept as a deliberate un-graded entry),
> `voice-pairs.md` (3 pairs), `placement-rules.md` (9 rules), `eval-fixtures.md`
> (6 must-flag · 3 must-produce · 9 must-NOT-flag), plus `improvement-notes.md`
> (scope-guard parking lot, now empty). Deviations from this spec, all recorded in
> the assets' `Not yet distilled` sections: fixtures gained a per-fixture
> `Context:` line (cold review showed placement is unjudgeable without the host
> doc); `missing-is-definition`, `untracked-impl-limitation`, and the
> `code-structure` voice pair were demoted as too thin or unverifiable. Validated
> by four cold-reader passes, one per asset.

**Goal:** Hand-distill the Neph labelled corpus into four committed assets in
`docs/corpus/` that the v0.2 reviewer and writer skills derive from. One-way,
offline, manual. The raw `#METADOCU` corpus stays in Neph; the assets cite it.

## Sources

**System docs** (auxiliary-doc labels — placement, ADRs, system-doc voice):
- `C:/repos/bots/neph/docs/systems/access.md` — calibration exemplar (richest labels).
- `C:/repos/bots/neph/docs/systems/chat-unions.md` — training-grade (the working-brief's "needs a human pass" note is stale).

**Code files** (internal-doc labels — docstrings, comments, banners, breadcrumbs;
the main source for the summaries-describe-meaning rule):
- `C:/repos/bots/neph/src/core/caps.py` — docstring before/after; in-code METADOCU; breadcrumb.
- `C:/repos/bots/neph/src/core/access_service.py` — banner-vs-class-docstring placement; bad-vs-good class summary (code-name → business terms); "what it does *not* do"; trivial-code-needs-no-docstring; docstring leaking changeable implementation (smell).
- `C:/repos/bots/neph/src/core/bot_module.py` — trivial-looking method that still warrants a docstring; bad docstring (`"…or None"` duplicates the code declaration) vs good.

## Output — four files in `docs/corpus/`, structured markdown with stable IDs (approach B)

Each file opens with a `Source: Neph corpus` line and ends with a
`## Not yet distilled` section for skipped/ambiguous/needs-human-pass items.

**`smell-catalog.md`** — one block per smell; signature + fix only, **never the
bad instance** (anti-pattern-leakage guard). Dedupe to ~8–12 entries.

```
### consumer-not-system
- Trigger: a block/ADR describes something that *uses* this system, not the system itself.
- Why: it's about a consumer; it doesn't change how this system works.
- Fix: move to the consumer's doc or a new UI/route doc.
- Source: neph access.md §"Owner admin surface", §ADRs
```

**`voice-pairs.md`** — literal before/after few-shot.

```
### too-technical → business-oriented
Before: "A union is a row with an auto-increment integer id..."
After:  "A union is a set of chats that share a user's stats..."
Source: neph chat-unions.md §"How it works"
```

**`placement-rules.md`** — rule + one **non-imitable** illustration + reasoning.

```
### file-link-with-backlink
Rule: a doc may name a code file when it's stable and carries a backlink.
Illustration (do not copy): access.md links `caps.py` for the full cap list; caps.py has a `System doc:` breadcrumb back.
Reasoning: co-change is guaranteed by the breadcrumb, so the reference is safe.
```

**`eval-fixtures.md`** — each fixture names the smell/pair id it exercises. This
is the one file that **does** hold the raw labeled instances (graders, not
exemplars). Covers must-flag (from negative labels), must-NOT-flag (from
positive labels), and must-produce-≈this (from before/after pairs).

```
### fixture: consumer-not-system / must-flag
Input: <the "Owner admin surface" block from access.md>
Expect: reviewer flags `consumer-not-system`.
```

## Process

1. **Inline, full-context** (not a subagent) — judgment-heavy classification.
2. Walk each source; read every `#METADOCU` label and the code breadcrumbs.
3. Classify and route each label:
   - **negative** → `smell-catalog.md` entry (signature + fix) **and** a must-flag `eval-fixtures.md` fixture holding the instance.
   - **positive structural** → `placement-rules.md` entry **and** a must-NOT-flag fixture.
   - **voice before/after** → `voice-pairs.md` entry **and** a must-produce fixture.
4. Dedupe smells (~8–12). Add a provenance line to every entry.
5. Fill each file's `## Not yet distilled` section.
6. **Scope guard:** principle/doc-standard improvement ideas that surface go to a
   notes list only — *not* applied to `principles.md`/`doc-standard.md` here.

## Invariants

- Bad instances appear **only** in `eval-fixtures.md`, never in the other three.
- No `#METADOCU` token is copied into any asset (the labels are fixtures; assets
  carry distilled signatures/rules/pairs, not the labels themselves).
- Every asset entry has a `Source:` provenance line.

## Done when

- The four files exist in `docs/corpus/` with the formats above.
- Every negative label became a smell entry or a `Not yet distilled` line; every
  before/after became a voice pair; fixtures cover must-flag and must-NOT-flag.
- A reader cold to Neph can use `smell-catalog.md` without seeing the corpus.

## Out of scope (later sub-projects)

- Projecting these assets into skill reference dirs → B-core / B-review.
- Running the eval fixtures (needs the skills) → B-review / B-core.
- Automating regeneration from new sources → `TD-corpus-enrichment-skill`.
