# Build-skill notes — inputs, structures, and lessons from hand-building B-core

> **Status:** Notes for a future `/build` skill (Track C, deferred). Marked for
> Codocu processing — eventual home is wherever Track C's spec lands. This file
> aggregates what was learned hand-writing v0.2's B-core (`/codocu` skill +
> `codocu-reviewer` agent) on 2026-05-23/24, so a generator can later replay
> the same shape from the same inputs without re-deriving everything.
>
> Includes synthesized content from non-git-controlled memory files
> (`~/.claude/projects/C--repos-codocu/memory/`) so the file is self-contained.

## What `/build` would eventually do

Take a set of structured inputs (principles, voice spec, doc standard, corpus
assets, tuning notes) and produce skill texts targeting different IDEs / LLM
harnesses (Claude Code, Codex, etc.). v0.2 hand-wrote one such projection for
Claude Code; that artifact is the calibration exemplar a generator must match.

## Source inputs used (the v0.2 hand-build)

In load order — the order the hand-build read them, and the order a generator
should consume them. The aspect specs and most of the corpus now live under
`skills/codocu/references/` so they're reachable at install time; only
`eval-fixtures.md` stayed in `docs/corpus/` (graders, not runtime input):

1. **`skills/codocu/references/principles.md`** — three core beliefs: clarity
   is the point; code is exhaustive about what is, docs cover the negative
   space; code and docs must not repeat themselves. Top of the truth hierarchy.
2. **`skills/codocu/references/doc-standard.md`** — the rules for a good
   auxiliary doc; dictionary of doc kinds; the four placement homes (symbol /
   module / system / outside); backlink mechanic.
3. **`skills/codocu/references/smell-catalog.md`** — 10 named smells, each
   with Trigger / Why / Fix. Sources cited to Neph.
4. **`skills/codocu/references/placement-rules.md`** — 9 placement rules with
   one non-imitable illustration + reasoning each.
5. **`docs/corpus/eval-fixtures.md`** — graders, not exemplars. The only
   asset that carries raw labelled instances. Three kinds: must-flag,
   must-NOT-flag, must-produce.
6. **`CLAUDE.md`** — repo-level conventions for working on Codocu itself.
7. **`codocu.md`** — repo-level doc structure declaration (where things
   live, the backlink marker the project uses, etc.). Always loaded at
   skill invocation in v0.2.

## Skill meta-structure (SKILL.md)

The B-core SKILL.md follows this shape, top-to-bottom. Order is load-bearing
— the voice anchor must reach the model before any operational instructions.

```
---
name: <invocation-suffix>          # = directory name = /codocu:<name>
description: <when to use>          # not "what it does" — when to invoke
---

## On invocation, load
- <design docs paths>
- <corpus asset paths>
- target repo's codocu.md

## Primitives
<short preamble: "verbs you compose, not a flow; do not narrate primitives back to user">

### <Primitive 1>
<1-3 paragraphs: what it does, when, key constraints, references>
...

## Composing the primitives — typical patterns
<one composition per canonical invocation; illustrative not prescriptive>

## Heuristics
<bulleted list of judgment-line rules: when to do X vs not>

## Runtime boundaries
<bulleted list of what the agent applies directly vs surfaces>
```

**Section-by-section discipline:**

- **Frontmatter `description`** describes *when* the user should invoke
  (the trigger), not what the skill does. This is the matcher signal for
  routing.
- **Loading section** lists explicit paths; the agent runs Read on each at
  invocation. No magic, no `${PLUGIN_DIR}` (until the harness supports it —
  see Open Questions).
- **Primitives** are verbs. Each has one job. The preamble explicitly tells
  the agent the list is a repertoire, not a flow. No state machine framing.
- **Composition examples** are *illustrative*, one per canonical use case;
  the agent is told to choose by judgment.
- **Heuristics** are judgment-line rules ("post-write atomic review for new
  docs or compounded edits; skip for trivial isolated edits"). They give
  the agent a test, not a script.
- **Runtime boundaries** carry only constraints active *at runtime* — what
  the agent does or does not apply when invoked. Architectural deltas vs
  earlier versions (e.g. "v0.1 had X, dropped") go in the implementer-facing
  spec, NEVER in SKILL.md.

## Agent meta-structure (subagent .md files)

For the reviewer subagent (`agents/codocu-reviewer.md`):

```
---
name: <agent-name>
description: <when the main agent should launch this>
model: <sonnet | haiku | opus>     # match the budget to the role
tools: <comma-separated list>      # narrow to what the agent must do
---

<one-paragraph role statement; what this agent IS NOT also>

## On invocation, load
<minimal subset of corpus needed for this agent's job — NOT the full pack>

## How to review (or "How to <verb>" for non-review agents)
<numbered process steps>

## Output schema
<exact shape, omit-empty rule, verdict guide if applicable>

## <Any anti-bias clauses>
<e.g. catalog non-exhaustive framing, conservative bias>
```

**Discipline:**

- **Model frontmatter** is chosen per the agent's competence requirement.
  Reviewer = sonnet because the corpus was distilled to be Sonnet-viable.
- **Tools** are bounded by what the agent needs. Reviewer gets Read/Glob/Grep
  for bounded reference verification — never Write/Edit (the reviewer never
  produces; it judges).
- **Loading is minimal.** Reviewer loads only `principles.md` and
  `smell-catalog.md` — NOT voice/placement (those are writer tools, not
  judge tools). The main skill loads everything; the subagent's pack is a
  deliberate subset.
- **Output schema** is explicit, including a verdict-guide rubric. The
  schema is text — markdown sections, not JSON — so it stays readable
  while still being structured enough for the caller to parse.
- **Anti-bias clauses** matter. See the conservative-bias lesson below.

## Writing principles applied during the hand-build

These shaped how each section was phrased. A generator must enforce them.

1. **Clarity over completeness.** "A doc the reader gives up on has failed,
   however accurate it is." Sections were cut aggressively when they
   restated something the reader already had.
2. **Lead with the answer.** Each section's first sentence carries the
   payload. Preamble is for orientation, not throat-clearing.
3. **No narration of machinery.** Skills never tell the user "running
   primitive X" or "step 3 of 7." The agent acts; the user sees results.
4. **Recommend; don't hand over a menu.** When the skill faces a choice
   point, it commits to a default and explains the trade — not "here are
   the options, pick."
5. **Constraints stated as standards, not threats.** "Apply doc work
   directly" — not "do not skip applying doc work."
6. **Local refs first, corpus samples fallback.** The skill privileges
   the target repo's own conventions; shipped samples are only the
   fallback when the repo has nothing to imitate.

## Anti-patterns (caught in this build — must not regress)

### Don't seed vocabulary just to negate it

The skill's SKILL.md should never say "this skill does not know about X" /
"does not track Y" when X / Y is a concept the agent otherwise has zero
context about. The negation has to first introduce X, and once introduced
it's loaded and may bleed into behavior.

Caught: B-core's draft included "does not track sync state" and "does not
detect subtractive vs generative modes" — vocabulary that existed only as
v0.1 → v0.2 deltas. Removed from SKILL.md; kept in the spec in a section
clearly marked **"v0.1 deltas — implementer orientation, not SKILL.md
material."**

**Test:** if removing the negation would make the agent behave differently,
keep it. If the agent would never have done X anyway because it doesn't
know X exists, drop the negation — it's pure overhead.

(Source: `feedback-no-negative-vocabulary-in-skills` memory.)

### Don't over-restrict skill authority

When designing skill boundaries, do not pick the maximally-conservative
interpretation by reflex. Restrictions should prevent real harm (changes
the user can't easily reverse, work outside the skill's competence) — not
enforce an abstract clean separation between domains.

Caught: B-core's first draft said "does not write code." Forced punting
one-line backlink additions and inline-doc edits to "a coding specialist,"
adding friction every time. Corrected to: applies doc work + small adjacent
code edits directly; substantive code-behavior changes still surface in the
Report. Test the agent applies at runtime: "if a reasonable reviewer would
want a coding specialist's eyes on the change, surface it; if it's a small
fix anyone could verify at a glance, apply it."

**Inline docs (docstrings, comments) live in code files but are doc work.**
A skill that does doc work owns inline docs by default.

(Source: `feedback-skill-authority-not-over-restricted` memory.)

### Reviewer subagents need explicit conservative bias

Caught 2026-05-24 smoke test: reviewer correctly flagged must-flag fixtures
but stretched `doc-far-from-anchor` (a code-level smell about symbols
aggregated in a docstring) onto a markdown opening paragraph the corpus
calls out as correct. Reviewer subagents trend aggressive without explicit
anti-aggression instructions.

**Fix baked into the agent:** Step 3 of "How to review" now requires the
doc to match the trigger *as written* (not superficial resemblance), and
notes that most smells are scoped. Plus a "Conservative bias" clause:
*"A false positive on good content erodes trust faster than a missed bad
smell. When the doc looks fine against the trigger, return `good` with no
hits."*

(Source: `b-core-design` memory — Reviewer conservative-bias clause.)

## Mode collapse: actions are the same; references availability is the axis

v0.1 framed B-core as two modes: subtractive (clean up bad docs) vs
generative (write new docs). v0.2 collapsed this: the actions are identical
either way — read what's there, decide what to keep / move / delete / write,
apply per the standard. What varies is **whether good local references
exist** (other docs in this repo) — if yes, the writer imitates them; if
no, falls back to shipped corpus samples.

A generator must NOT reintroduce mode-detection logic. The reference-
availability check is operational, internal to the Write/edit primitive,
not a runtime classification the skill carries.

(Source: `b-core-design` memory.)

## Primitives, not flow

The skill teaches a **repertoire of verbs** the agent composes per task,
not a fixed sequence. Each primitive has one job; the agent picks and
orders. Composition examples are illustrative.

v0.2's primitives (the verbs B-core's SKILL.md teaches):

1. Map doc graph
2. Discover scope
3. Atomic review (delegates to reviewer subagent)
4. Compositional review (in main thread)
5. Place
6. Write/edit
7. Delete/demote
8. Verify-against-code
9. Survey doc system
10. Init (delegates to sibling skill)
11. Report

Parse-intent is the dispatcher (not a verb). Init delegates to a sibling
skill (not inline). Atomic review delegates to a subagent; compositional
review stays in main thread (the split is by review *kind*, not by
always/sometimes).

(Source: `b-core-design` memory.)

## Lessons from the smoke test (input for the generator's evals)

Even with a tight design, the first prompt drafts had real misses. The
generator's eval harness needs to catch these:

- **Trigger language must be exact.** Reviewer with permissive "check
  whether the doc carries an instance" generalized smells too liberally.
  Fix: "Match the trigger *as written*; when in doubt, do not flag."
- **Conservative bias must be explicit.** Without "false positives erode
  trust," reviewers default to aggressive.
- **Smell catalog is non-exhaustive but principle-grounded.** Uncataloged
  hits must name which principle is violated; can't be gut-feel.

The eval fixtures in `docs/corpus/eval-fixtures.md` are the regression
suite. Every must-flag fixture must produce its expected smell; every
must-NOT-flag fixture must not flag the named correct content; every
must-produce fixture's writer output must drop trivia and lead with the
business shape.

## Open questions for `/build` (deferred)

- **Plugin-root path resolution.** The hand-build assumes `cwd = plugin
  root` (the `--plugin-dir` dogfood path). For real installation, the
  skill's loading instructions need to resolve plugin-root paths. Three
  candidate fixes: inline content into SKILL.md; bundle copies into
  `skills/codocu/`; use a `${PLUGIN_DIR}` variable if the harness exposes
  one. A generator should pick its strategy and bake it in.
- **Multi-IDE / multi-LLM projections.** The hand-build targets Claude
  Code. Other harnesses (Codex, etc.) have different conventions for
  skill packaging, subagent invocation, frontmatter shape, tool naming.
  The generator needs a per-target template layer.
- **Typed-doc rule packs.** Tech-debt, ADRs, feature plans, etc. have
  their own conventions. v0.2 ships generic; the init template carries
  typed-doc opinionation. The generator should accept per-doc-type rule
  packs as an optional input layer.
- **Tuning doc.** A separate file capturing per-target tuning (model
  defaults, tool budgets, eval pass thresholds) — does not exist yet;
  the generator's spec should call out its shape.

## Provenance — where this file's content came from

- Conversation 2026-05-23/24 (brainstorming → spec → plan → execute cycle).
  The dated spec and implementation plan
  (`docs/plans/2026-05-24-b-core-*.md`) and the matching smoke-test results
  folder have since been folded; their content lives in the surviving
  artifacts and in this file.
- Surviving hand-built artifacts: `skills/codocu/SKILL.md`,
  `agents/codocu-reviewer.md`.
- Memory files (non-git-controlled, synthesized inline above):
  - `b-core-design.md` — architecture decisions, reviewer conservative-bias.
  - `feedback-no-negative-vocabulary-in-skills.md` — anti-pattern.
  - `feedback-skill-authority-not-over-restricted.md` — anti-pattern.
  - `codocu-v02-core-and-plan.md` — v0.2 reframe.
  - `codocu-metadocu-corpus.md` — corpus design.
