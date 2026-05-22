# Documentation methodology — Neph

> The doc-content principles that drive how we write system documentation in Neph. Read cold before touching any doc.
>
> **Where this fits:** This is the writing-side companion to `review-checklist.md` (post-write mechanical checks). Both are read-first for any doc work. The narrative orientation lives in `working-brief.md`.
>


## The principle
One sentence carries all of it:

> **Documentation lives as close to its anchor as the concept's scope allows, and may name code in inverse proportion to its distance from that code.**

Placement and naming-license are the *same* axis, not two rules. The load-bearing half is the second: **drift is not a discipline failure — drift is naming code from too far away.** Every "don't" below is one instance of that single violation. Hold onto that and the rest is derivable.

CODOCU v0.2 TODO REMARK: 
```
This principle needs work
Naturally, review-checklist and working brief are also affected
- Summarizations, business-level explanations - benefit from it, it's much more context-enriching to reframe how modules work using business domain terms, not code concepts. Also helps with doc stability against code refactorings.
- System ADRs - not working. ADRs must be able to address the specific code entities while reasoning about several code files, so they are hard to land into code file.

> **Documentation lives as close to its anchor as possible, and should avoid referencing concepts that may change independently of the documentation** ?
Documentation of specific scope should avoid addressing entities of lower abstraction?

If some concept is described in the documentation, agent (Human/AI) that makes changes to that concept must see a link to be able to load that documentation into context (mention, backlink, breadcrumb).
When agent is preparing the change for the system, he must be naturally aware of the documenation related to that system.

API/contract changes vs implementation changes 
Method docstring - can we name other methods there? Or only their contracts? 
See scenarios
- Method A docstring references Method B contract (it formats string). Method B is used in A
    - When B contract is refactored, A must be updated (tests, direct references) - docs will be in context, will be updated
    -  

Documentation examples: 
 - method explanation and quirks - method docstring, can name methods and variables, and methods that 
 - module's extension and tuning examples - module docstring, can name classes, methods, variables, submodules, storage concepts, etc of this module  
 - business-level system summary - auxillary system document. No code entities allowed
```


## The four tiers

| Tier | Anchor | Home | May name | Neph touchstone |
|---|---|---|---|---|
| **Symbol** | one symbol / line | docstring or inline comment | *anything* — it moves with the code | the hack note beside a constant; `resolve_scope`'s contract in its own docstring |
| **Module** | one module / file | `module.py` / `__init__.py` / file header | symbols *in this module only* | "union owns scope resolution; downstream modules register `ScopeMigrator`s" → `union/module.py` header |
| **System** | *no single anchor* — a flow, a subsystem's reason to exist, deliberate non-goals, a convention, an in-flight cross-system refactor | `docs/systems/<x>.md` | systems, flows, decisions; **public-interface names verbatim in prose** (routes, bot commands, cap tokens); internal symbols by *location*, never by *transcription* | `chat-unions.md`; `access.md` (calibration exemplar with anti-patterns labeled) |
| **Outside** | the whole repo, for non-builders | generated artifact (wiki / API ref) | *anything* — regenerated, can't drift | API reference, route listing, command index — CI step, never hand-written |

A **convention** is a no-single-anchor concept → System tier (its own thin doc, or folded into the system it governs). An **in-flight intersystem refactor** spans many anchors → also System tier, but one that dies when the refactor lands — which is exactly what `docs/plans/` already is. *A plan is a system doc with a TTL.*

## The anti-drift gear: the back-reference breadcrumb

A doc that points at code rots silently — nobody editing the code ever sees the doc. Flip the arrow: a one-line breadcrumb lives *in the load-bearing file*, pointing out at the doc. Enforcement is **proximity to the edit**, not a compiler — the person changing the logic sees the pointer in their working context and is reminded the negative-space doc exists.

Canonical line (host syntax adds whatever prefix it needs — `#` in Python, `//` in TS, none inside a docstring):

    System doc: docs/systems/chat-unions.md

Grep-friendly: `rg "System doc:"` enumerates every breadcrumb in the repo.

Rules that fall out:

- Every System-tier doc has **≥1 inbound breadcrumb**, ideally from the load-bearing file (the concept's **center of gravity**: shared mechanism > canonical exemplar > orientation layer).
- A handful (1–5) across genuinely related anchor files is fine and *reinforces* the link — the smell isn't count, it's **scaling**. If a convention wants a breadcrumb in every file that uses it (a dozen, growing with the codebase), it should become a mechanism or a lint, and the doc keeps only the *why*.
- "I can't find one place for the breadcrumb" is still a design smell — same scaling logic applies.
- The rare residue — a convention that lands nowhere *and* lints nowhere — gets a **named, deliberate entry in the project-wide guide** (CLAUDE.md), flagged as the explicit exception.
- A System doc with *no possible* inbound breadcrumb is either Outside-tier (so: generate it) or fiction (so: it describes something the code doesn't do).
- The breadcrumb names the doc; the doc names the *location*. Never the reverse, never both transcribing each other.

## What a System doc is *for* (the negative space)

Code shows *what*. A System doc carries only what code structurally cannot:

1. **Why the subsystem exists** — the force that made it necessary.
2. **Roads not taken** and why — the `ADRs` section (see below).
3. **Deliberate non-goals and accepted sharp edges** — so a reader can tell an *intentional* smell from a bug.
4. **The cross-module flow** no single file owns.
5. **Conventions and agreements** no type system enforces.
6. **In-flight intersystem refactors** — the direction of travel, so a mid-refactor repo doesn't read as incoherent.
7. **The tuning-knob map** — how to change and tune module behavior, extend the system, work around quirks.

The hard boundary, stated as a non-goal of the method itself: **a System doc is not a behavioral spec.** No enumerated inputs/outputs, cases, or step-by-step behavior — that is code's job, and duplicating it is the SDD/BDD sync tax we refuse to pay.

The field test, run before writing *any* system-doc sentence:

> **"Could this sentence be a test assertion?"** If yes → push it down a tier or delete it.

That one test catches the transcription anti-pattern *before* it is written. It is the cheapest check in the whole method — use it constantly.

## Tier elevation — the second pass

Procedure-driven rewriting catches transcription but misses structure. After a first rewrite pass, do one explicit **elevation pass**: for each block in the doc, ask:

- Could this be one tier down (into a docstring, module header, file comment)?
- Could it be Outside tier (an enumeration that belongs in generated reference)?
- Could it be deleted entirely (carried by code, not negative space)?

If yes to any, do it. The default is "keep where it is" — but only after this question has been asked and answered. This is the step the original procedure didn't have; its absence produces compliance prose that obeys the local rules and misses the structural calls.

## ADRs — the standard name for "roads not taken"

The block that documents alternatives and reasoning is named **ADRs** (architectural decision records). Not "Why it's like this" — that phrasing implies wrongness or defensiveness, and it doesn't carry the well-known ADR concept that helps non-builders parse the block at a glance.

Each ADR entry is one or two sentences of *decision + reasoning*. Reasoning is the reason the entry exists; without it, the entry is a fact code already carries.

## Naming public surfaces vs. enumerating them

System docs **may name public-interface surfaces verbatim** in prose: HTTP routes, bot commands, CLI flags, cap tokens, env vars. The test: *would an external caller care if this name changed?* Yes → contract, name it. No → implementation, point at location.

But there's a second distinction:

- **Naming a surface for context** (in a sentence about *why* or *flow*): System tier, fine. *"Admin operations gate on `bot.unions`."*
- **Enumerating surfaces as a list** (here are all the routes, here are all the commands): **Outside tier**. That's API reference; it belongs in a generated artifact that can't drift. A bulleted list of all commands with their gates is enumeration even if each name is "allowed verbatim."

The trap: "public names allowed verbatim" reads as license to keep enumerations. It isn't. The license is for *prose use*, not *reference structure*.

## `#METADOCU` — doc about the doc

The single channel that is *not* doc-about-code. Its only job: turn Neph into **labelled training data** for the Codocu skill. It narrates the placement decision itself — *which tier was chosen and why, which rule fired, what was deliberately not done* — colocated with the example so lesson and instance can't drift apart.

It is **fixture-only**: written in Neph *because Neph is the reference corpus*, never in a downstream repo, excluded from the generated Outside tier by construction. Writing it anywhere but the fixture is the one way to misuse it. Its content is never about the system — only about the doc.

### How to read a meta-narrated doc as a writing exemplar

**METADOCU labels teach you HOW to choose, not WHAT to include.** Each label is the author's chain-of-thought about a placement decision (tier choice, naming, deletion, anti-pattern marking). When mimicking the exemplar to write a new doc:

- Read labels as instructions about *placement reasoning*.
- Do not copy the labeled instance itself unless the label explicitly says "this is the model."
- Anti-pattern blocks are labeled negative on purpose; they teach by contrast and must not be replicated.

Without this framing, a mixed exemplar (good content + labeled anti-patterns) confuses. With it, the mixed exemplar is *more* useful than clean prose alone, because the placement reasoning is exposed inline.

### What a good label looks like

Short, pointed, specific to *this* instance. ~15 words. Attached to a concrete property: *"acceptable use of file link, expected to be reasonably stable, easy to address when refactored, has backlink."* Not *"Protocol blocks are a transcription trap, here's the rule"* — that's a paraphrased rule, not a label.

Calibration set: `docs/systems/access.md`. Look there for the shape.

## When fixing one place creates a hole elsewhere

When a change to one part of a doc invalidates another part (a sentence that depended on the old state), the invalidated sentence is **a question**, not a sentence to rewrite into a non-statement. Surface the contradiction to the reviewer.

Example: tightening "owner-only operations" to "gated on `bot.unions` cap" elsewhere in the doc invalidates a "no delegation" limitation that meant "ownership lock, not capability lock." Smoothing it into "no delegation below that cap" loses the original meaning *and* the contradiction signal. The right move is to flag: *"this limitation no longer makes sense given the cap change — should it be removed or rephrased?"*

This isn't a content principle, it's a working principle. It belongs here because the failure mode (silent smoothing) is what suppresses it; making it explicit gives the writer permission to stop.

## Voice

Write for a busy, mentally exhausted reader. Direct subjects, concrete consequences, soft pointers (*"see X"*) over hard transcription. The corpus grows here — start with one pair, add more as we rewrite.

### Pair 1 — soften mechanism into reader-facing consequence

**Dense / compliance-prose:**

> Per-real-chat presence (the chats module's membership table) stays keyed by raw `chat_id` and does **not** register a migrator. Unions share *gameplay* state, not physical presence.

**Preferable:**

> Actual presence of user in any chat (see chats module membership tracking) is always based on real chat_id, and not affected by this chat's union status.

The shift: a concrete subject ("actual presence of user"), softer pointer ("see X" instead of naming the table), consequence stated in terms the reader cares about ("not affected by union status") rather than the mechanism ("does not register a migrator").

The principle is also in `CLAUDE.md` (§ AGENT VOICE); this corpus grows it from one pair to many over time.

## DO / DON'T

**DO**

- Place by anchor scope: one symbol → docstring; one module → module/file header; no single anchor → `docs/systems/`.
- Name code in inverse proportion to distance: docstrings may name anything; system docs name systems/flows/decisions and point at *locations*.
- **Public-interface names may appear verbatim in prose** — but not in enumerations. Enumerations are Outside tier.
- Put one breadcrumb at the concept's center of gravity (mechanism > exemplar > orientation layer).
- In system docs write only the negative space (the seven kinds above).
- Run the test-assertion test before every system-doc sentence.
- Run the elevation pass after every first draft.
- Treat a plan, and an in-flight refactor, as a system doc with a death date.
- Surface contradictions; do not smooth them.

**DON'T**

- Don't transcribe **internal** code in system docs — service methods, classes, fields, internal modules, enumerated behavior.
- Don't let a doc point at code without code pointing back.
- Don't scatter a breadcrumb across every instance of a convention.
- Don't write behavioral spec / SDD / BDD into a system doc.
- Don't hand-maintain the Outside tier — generate it.
- Don't leave a system doc with zero inbound breadcrumbs.
- Don't write `#METADOCU` anywhere but the fixture.
- Don't smooth a contradiction into a non-statement. Surface it.
- Don't paraphrase rules as METADOCU labels. Labels are pointed instance-properties, not lectures.
