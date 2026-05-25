# B-core — Design

> Status: design approved in brainstorming 2026-05-23/24. Supersedes the rough
> B-core bullets in `2026-05-22-track-b-decomposition.md` and resolves the open
> threads in `2026-05-23-b-core-seeds.md`. Track B sub-project; B-extract is
> done, this is the next implementation target.

## What B-core is

`/codocu` is the single user-invokable skill at the heart of v0.2. It keeps a
repo's docs aligned with Codocu's principles — writing new docs, fixing existing
ones, relocating misplaced content, removing transcription. It carries the full
standard inline (principles, voice pairs, placement rules, smell catalog) and
composes a small repertoire of verbs to handle whatever the user asks for. It
does not plan code work, does not write code, and does not track a sync state
machine.

## The skill family

v0.2 ships three things, not eight:

- **`/codocu`** — B-core. The main entry point. Writer + compositional reviewer
  + orchestrator.
- **`/codocu:init`** — sibling skill. Scaffolds a fresh repo (folders,
  `codocu.md`, opinionated conventions for typed docs like tech-debt, ADRs,
  feature plans). Its own design is its own brainstorm — B-core delegates to it
  and never duplicates init logic.
- **`codocu-reviewer`** — atomic per-doc reviewer subagent. Sonnet-viable,
  bounded tools, narrow scope.

B-integrate (always-on awareness, post-implementation verification) is wiring
at `CLAUDE.md` / hooks, not a skill. B-cleanup is docs.

## What B-core loads

Full corpus pack — read at skill load:

- `docs/design/principles.md` — the three core beliefs.
- `docs/design/voice.md` — who the agent is, how it talks.
- `docs/design/doc-standard.md` — the rules for a good auxiliary doc.
- `docs/corpus/smell-catalog.md` — named anti-patterns with fixes.
- `docs/corpus/voice-pairs.md` — literal few-shot for voice (dense → plain).
- `docs/corpus/placement-rules.md` — where docs live and why.
- The target repo's `codocu.md` — always loaded, carries local conventions.

Heavy by Sonnet standards; pragmatic for now. Optimization (indices, RAG, lazy
load) waits for measurable context pressure.

## The primitives

The verbs B-core composes per user ask. SKILL.md teaches each verb's role; the
agent picks and orders them. Not a flowchart, a repertoire.

1. **Map doc graph.** Read TOC/structure when the task needs cross-doc context.
   `codocu.md` is ambient; the wider graph is not.
2. **Discover scope.** Identify task targets. User-named, change-inferred
   (VCS-assisted — `git status` / `git diff` / `git log` to find the changeset,
   then map changed code → docs that reference it via filenames and breadcrumbs),
   or task-scoped.
3. **Atomic review.** Launch `codocu-reviewer` against a single doc. Receive a
   structured report.
4. **Compositional review.** In-thread. Cross-doc duplications, dangling
   cross-refs, structural relations the atomic reviewer can't see. Default scope
   is affected docs + immediate neighbors.
5. **Place.** Decide where a doc lives — new doc, fold into existing, push down
   to a docstring, breadcrumb-only, or absorb-then-delete. Includes the
   breadcrumb decision (does this need one, and which code file carries it).
6. **Write/edit.** Compose or modify doc content. *Local refs* (other good docs
   in this repo — drawn on for voice cues, placement patterns, and conventions)
   come first; shipped corpus samples are the fallback when the repo has nothing
   to imitate. Apply principles + voice. After writing, run atomic review per
   the heuristic below.
7. **Delete/demote.** Subtractive moves — remove transcription, push notes down
   to docstrings, archive superseded.
8. **Verify-against-code.** Mechanical Grep/Read against current code state.
   Does the path still exist, does the symbol still exist, does the doc's
   factual claim still hold. Surfaces stale claims, doesn't speculate.
9. **Survey doc system.** Whole `docs/` tree as subject. For meta-asks like
   "let's switch doc systems, I need a plan." Produces structured findings about
   the doc system itself, which Write then turns into the plan doc.
10. **Init.** Recognize uninited repos (no `codocu.md`) and delegate to
    `/codocu:init`. Never inline init logic.
11. **Report.** Lead with the answer. Sections for findings, doc edits applied,
    required code-side edits (backlinks, breadcrumbs the user or a coding
    specialist must add), recommendations. No narration of machinery.

## Composing the canonical invocations

How the primitives line up against the four user asks the design must support.
Order is the agent's judgment, not a script.

- **"Check if these docs are good quality."**
  Discover scope → Atomic review → Compositional review (light) → Report.

- **"Plan a migration to a new doc system."**
  Survey doc system → Place + Write (the plan doc itself) → Report.

- **"Code changed, update docs."**
  Discover scope (VCS) → Verify-against-code → Atomic review → Place + Write/edit
  (or Delete/demote) → Report.

- **"Verify tech-debt records still match reality."**
  Discover scope → Verify-against-code → Report.

## The reviewer interface (`codocu-reviewer`)

- **Where it lives:** `agents/codocu-reviewer.md` at the plugin root. Frontmatter
  pins `model: sonnet`.
- **Loaded:** `principles.md` + `smell-catalog.md` only. Voice and placement
  rules stay out — those are writer tools; the reviewer's job is judge, not
  writer.
- **Tools:** Read, Glob, Grep — bounded. Enough to verify a referenced path or
  breadcrumb exists when judging a sentence. No project briefing.
- **Input:** a doc path and an optional free-form context line ("focus on
  placement," "general check"). No typed-doc hint — generic for v0.2.
- **Output:** structured markdown with known sections —

  ```
  ## Verdict
  good | needs-work | bad

  ## Hits
  ### <smell-name> — <location-in-doc>
  Why: …
  Fix: …
  ### [uncataloged] — <location-in-doc>
  Principle violated: <which one>
  Why: …
  Fix: …

  ## Notes
  <free-form caveats>
  ```

  Smell catalog is non-exhaustive by construction. The reviewer is told the
  catalog is the first thing to check, and is also instructed to flag clear
  quality issues outside the catalog as `[uncataloged]`, naming which principle
  is violated. Repeated `[uncataloged]` hits are candidates to promote into the
  catalog later.

- **B-core fans out** when multiple docs need review. Concurrency is
  orchestration, not a reviewer property.

## Heuristics

- **Post-write atomic review.** Run it after a new doc, a major edit, or several
  compounded small edits in the same pass. Skip for isolated trivial edits.
- **Compositional review scope.** Affected docs + immediate neighbors (docs
  cross-linked with the affected ones) by default. Widen by running Map doc
  graph first when the task scope is unclear.
- **VCS in Discover scope.** When the user's ask is change-driven, use
  `git status` / `git diff` / `git log` to define the changeset before mapping
  to docs.
- **Destructive actions narrate intent.** Before Delete/demote runs, B-core
  states what's about to go and why. Standard agent etiquette, not a Codocu
  invention; plan mode catches it formally, narration catches it informally.

## Runtime boundaries

These are real constraints on B-core's behavior at runtime — they belong in
SKILL.md so the agent knows them as part of its job.

- **Applies doc work and small code edits directly.** Inline docs (docstrings,
  comments) are part of B-core's scope. Small code edits adjacent to the doc
  work — `System doc:` breadcrumbs, fixing a stale reference in a comment, a
  one-line rename — are also fair game.
- **Surfaces anything larger.** When the doc work implies a substantive code
  change (new functions, refactors, behavior changes), B-core surfaces it in
  the Report. The test: if a reasonable reviewer would want a coding
  specialist's eyes on the change, surface it; if it's a small fix anyone could
  verify at a glance, apply it directly.
- **Does not run its own propose/approve loop.** Claude Code's plan mode handles
  that. In normal mode B-core writes directly; in plan mode the writes are
  staged behind ExitPlanMode like any other tool.

## v0.1 deltas — implementer orientation, not SKILL.md material

These are concepts v0.1 carried that v0.2 explicitly drops. Listed so the
implementer doesn't reintroduce them out of habit. **Do not seed any of this
vocabulary in SKILL.md** — telling the agent "you don't track sync state"
requires it to first know what sync state is, which costs context and invites
exactly the confusion the drop was meant to remove.

- **Sync-state machine gone.** v0.1's three-state machine (synced / desynced /
  dirty) and everything it drove (state routing, conflict resolution) are out.
  Binary inited (`codocu.md` exists) vs uninited.
- **Modes collapsed.** v0.1 framed "subtractive (cleanup bad docs)" vs
  "generative (new docs)" as detected modes. v0.2 treats actions as the same;
  what varies is reference availability — covered operationally in the
  Write/edit primitive, with no mode detection needed.

## Deferred and known gaps

- **Typed-doc rule packs.** Tech-debt, ADRs, feature plans, etc. have their own
  conventions. v0.2 ships generic; the init template carries typed-doc
  opinionation, and once a repo is inited those conventions propagate as local
  references the writer naturally picks up.
- **Semantic Verify-against-code.** v0.2 is mechanical only — path/symbol
  existence, breadcrumb integrity. The "does this claim still hold given how
  the code now behaves" half is reviewer-shaped but needs a different rule pack
  than the smell catalog. Lifted when the eval fixtures show the gap matters.
- **Init's own design.** Sketched as a sibling skill but not designed in this
  spec. Brainstormed separately when B-cleanup decides its scope.
- **Voice expansion.** `voice.md` is parked pending more before/after pairs;
  voice-pairs.md is the v0.2 working set.
- **Stale CLAUDE.md text.** The "Codocu sync state:" line in CLAUDE.md and
  `codocu.md` refers to the dropped state machine. On B-cleanup's docket.
- **Plugin-root path resolution.** Today the skill and reviewer read design and
  corpus files via paths relative to the working directory. That resolves
  correctly only when cwd is the plugin root — the `--plugin-dir` dogfood case.
  For real installation (plugin loaded from cache, user working in their own
  repo), the relative paths would look in the user's repo, not the plugin's.
  Three plausible fixes when this gets picked up: inline the content into
  SKILL.md and the agent body; bundle copies of design + corpus into
  `skills/codocu/` (matching the "skill loads from its own directory" rule in
  codocu.md) with a build step that syncs from source; or use a plugin-root
  variable if Claude Code exposes one. Pick at deployment time.

## Reader test

> Where would the intended reader — a contributor implementing B-core — get
> lost or bored?
>
> Risk: the "primitives, not flow" framing is abstract until the canonical
> invocation table shows the verbs composing. That table is the load-bearing
> example; if it goes, the spec reads as a list of definitions and the reader
> has to invent the composition pattern themselves. Kept and placed early after
> the primitives.
>
> Risk: the reviewer interface block is the densest part (frontmatter, tools,
> output format). A reader looking only for the skill design might skim past
> it. Acceptable — that block is for whoever implements the reviewer, and it
> earns its space by being where they'll land first.
