# Smell Catalog

> Source: Neph corpus (distilled offline, one-way). Provenance lines cite the
> raw `#METADOCU`-labelled instances; the instances themselves live only in
> `eval-fixtures.md`.

Named, matchable signatures of bad documentation. Each entry gives the trigger,
why it's wrong, and the fix — **never the bad instance** (seeing the
anti-pattern invites reproducing it). To grade a reviewer against a real
instance, use the matching fixture in `eval-fixtures.md`.

### consumer-not-system
- Trigger: a block or ADR in a system doc describes a feature that *uses* this system rather than the system itself.
- Why: it documents a consumer, so it doesn't change how this system works; it drifts here and buries the system's real shape under unrelated detail (often reiterating code concepts as it goes).
- Fix: move it to the consumer's own doc, or open a new doc for that slice (e.g. a UI / admin-routes doc). Keep in the system doc only the part that changes how this system works.
- Source: neph access.md §"Owner admin surface", §ADRs (admin-surface ADR)

### stray-todo-in-longterm-doc
- Trigger: a long-term doc carries an inline `#TODO` / fix-later note about future work.
- Why: a long-term doc records what is and why; a fleeting task buried in its prose is invisible to whoever tracks work and rots unowned.
- Fix: move it to the tech-debt / TODO record; if the doc must mention it, leave a one-line pointer with a stable backlink.
- Source: neph access.md §"UI availability"

### unmaintainable-aggregation-list
- Trigger: a doc aggregates per-component behavior into one list, but nothing links each source component back to the list.
- Why: the list reads well as an overview, yet an editor changing one component has no way to know it exists, so it silently goes stale.
- Fix: add a backlink (breadcrumb) from each source to the list and re-check those backlinks during routine review — or drop the list if the breadcrumbs can't be maintained.
- Source: neph chat-unions.md §"Merge semantics for known modules"

### doc-far-from-anchor
- Trigger: descriptions of many symbols are gathered into one block (a class docstring, a banner) instead of sitting on each symbol.
- Why: it places each note further from its anchor than needed and forfeits the IDE's per-symbol docstring preview, so the reader doesn't meet the right note at the right symbol.
- Fix: attach a short docstring / comment to each symbol it describes; keep a shared block only for what genuinely spans all of them.
- Source: neph caps.py §Cap

### leaks-changeable-implementation
- Trigger: a docstring states an implementation detail (caching, DB access, call count) that this layer doesn't own and that can change.
- Why: it drifts when the implementation changes, it may already be wrong for some paths, and it usually sits where the people who could act on it never look.
- Fix: drop it, or move it to the layer that owns the detail (e.g. the abstract method its implementers must read), where it is both true and seen.
- Source: neph access_service.py §AccessService.resolve_user_chat_caps
- No current fixture: grading this needs the provider/caching code to show the detail belongs to a lower layer and will drift.

### summary-restates-signature
- Trigger: a summary repeats what the declaration already states — a return type, an "…or None", a parameter list.
- Why: it duplicates the code line-for-line, adding length without meaning, and drifts the moment the signature changes.
- Fix: cut the restated part; describe the meaning, or phrase the condition in plain words ("…if it has any").
- Source: neph bot_module.py §BotModule.help

### enumerates-code-shape
- Trigger: a doc lists files or directories in the system and what each one is for — a `tree`-shaped table with file → role.
- Why: it transcribes a directory listing the reader can produce with `ls` or their IDE. A rename or reorg silently invalidates the table, and no breadcrumb sits in the renamed file to point at the doc.
- Fix: drop the listing. If the convention itself is the point, state it in one sentence and let the reader confirm by looking. If one specific file is load-bearing, name it once where it matters, with rationale.
- Source: 002 run, T2 `docs/systems/bot-architecture.md` §Modules

### narrates-sequential-code
- Trigger: a doc walks through a function's body as numbered steps that mirror the code's actual order ("first X, then Y, then Z").
- Why: it's a second copy of the function in prose; reordering or merging branches silently falsifies the doc, and reading the function is faster than reading the paraphrase.
- Fix: keep only the *why* of the ordering — what would break if the steps swapped. Cut the step-by-step recap.
- Source: 002 run, T2 `docs/systems/bot-architecture.md` §Assembly (three-phase startup); T1 `docs/architecture.md` numbered `main()` walkthrough.

### enum-recap
- Trigger: a doc enumerates the variants of an enum, status field, or return type that the code already defines.
- Why: the enum is the authoritative list; restating it creates a second source of truth that drifts the moment a variant is added, removed, or renamed.
- Fix: name the enum once and let the reader follow it back. If one variant carries rationale the code can't, describe that variant's reason — not the whole list as a recap.
- Source: 002 run, T2 `docs/systems/captcha-gate.md` §"How a join lands" (PASSED/FAILED/SKIPPED/ABORTED list).

### behavior-assertion-as-prose
- Trigger: a sentence describes what a function does in a form that could be a test assertion ("X flips Y to false", "X returns N if Z").
- Why: it is the kind of behavior the code already proves; in a doc it is a second copy of the implicit test, and it drifts the moment behavior changes. The field test from `doc-standard.md` §2 ("could this sentence be a test assertion?") names this directly.
- Fix: apply the field test. If yes, push the sentence down to a docstring on the function — or delete it. Keep only the *why* the behavior is the way it is.
- Source: 002 run, T2 `docs/systems/chats-presence.md` ("`left_chat_member` flips `in_chat` to false"); `docs/systems/owner-commands.md` (various callback-effect sentences).

## Not yet distilled

- `untracked-impl-limitation` (a "known limitations" entry that re-describes
  implementation and duplicates a tech-debt record with no stable backlink) was
  pulled as a smell: it can't be graded without the linked tech-debt file to
  confirm the duplication and the missing backlink. Re-add once a self-contained
  example exists.
- `missing-is-definition` (a doc explaining what a thing *does* but never what
  it *is*) was pulled as a smell: the rule is unsettled — a good "does X and Y"
  summary is sometimes enough — and the corpus has no clean example. Revisit
  with better examples before re-adding.
- The "Owner admin surface" block also *reiterates code concepts* (endpoint
  signatures, `db.atomic()`, `scope_id` resolution). Folded into
  `consumer-not-system` rather than split into a separate transcription smell;
  revisit if a non-consumer transcription instance shows up.
- chat-unions.md notes that joining a union is destructive for game classes and
  "UI should better represent that" (an in-flight rough edge). Unlabelled;
  reads as intentional negative-space, not a smell. Left out.
