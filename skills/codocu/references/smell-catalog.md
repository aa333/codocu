# Smell Catalog

> Source: Neph corpus (distilled offline, one-way). The source lines cite the
> raw `#METADOCU`-labelled instances; the instances themselves live only in
> `eval-fixtures.md`.

Named patterns of bad documentation — the detail behind the atomic reviewer's
checklist. Each entry gives the trigger, why it's bad, and the fix, but **never
the bad example** (seeing the anti-pattern invites copying it). To grade a
reviewer against a real instance, use the matching fixture in `eval-fixtures.md`.

### invented-why
- Trigger: a doc states a rationale, intent, decision, or non-goal with nothing
  in the code or comments to back it — the author guessing why the code is the
  way it is.
- Why: rationale is negative space. It can't be read off the code, so deriving
  it from the code is a guess dressed up as fact. A wrong "why" is worse than no
  "why".
- Fix: cut it, or mark it as something the owner needs to confirm. Keep only a
  why that's anchored in a comment, a commit, or what the user actually told you.

### consumer-not-system
- Trigger: a block in a system doc describes a feature that *uses* this system
  rather than the system itself.
- Why: it documents a consumer, so it doesn't change how this system works. It
  drifts here and buries the system's real shape under unrelated detail.
- Fix: move it to the consumer's own doc, or start a new doc for that slice.
  Keep only the part that changes how this system works.
- Source: neph access.md §"Owner admin surface", §ADRs

### stray-todo-in-longterm-doc
- Trigger: a long-term doc carries an inline `#TODO` / fix-later note about
  future work.
- Why: a long-term doc records what is and why. A fleeting task buried in its
  prose is invisible to whoever tracks work, and it rots unowned.
- Fix: move it to the tech-debt / TODO record. If the doc must mention it, leave
  a one-line pointer with a stable backlink.
- Source: neph access.md §"UI availability"

### unmaintainable-aggregation-list
- Trigger: a doc gathers per-component behavior into one list, but nothing links
  each source component back to the list.
- Why: the list reads well, but an editor changing one component has no way to
  know it exists, so it silently goes stale.
- Fix: add a backlink from each source to the list, and re-check those backlinks
  in routine review — or drop the list if the backlinks can't be kept up.
- Source: neph chat-unions.md §"Merge semantics for known modules"

### doc-far-from-anchor
- Trigger: notes about many symbols are gathered into one block (a class
  docstring, a banner) instead of sitting on each symbol.
- Why: each note ends up further from its symbol than it needs to be, and you
  lose the IDE's per-symbol docstring preview — so the reader doesn't meet the
  right note at the right place.
- Fix: attach a short docstring or comment to each symbol. Keep a shared block
  only for what genuinely spans all of them.
- Source: neph caps.py §Cap

### leaks-changeable-implementation
- Trigger: a docstring states an implementation detail (caching, DB access, call
  count) that this layer doesn't own and that can change.
- Why: it drifts when the implementation changes, it may already be wrong for
  some paths, and it usually sits where the people who could fix it never look.
- Fix: drop it, or move it to the layer that owns the detail (e.g. the abstract
  method its implementers must read), where it's both true and seen.
- Source: neph access_service.py §AccessService.resolve_user_chat_caps
- No current fixture: grading this needs the provider/caching code to show the
  detail belongs to a lower layer and will drift.

### summary-restates-signature
- Trigger: a summary repeats what the declaration already states — a return
  type, an "…or None", a parameter list.
- Why: it duplicates the code line-for-line, adding length without meaning, and
  drifts the moment the signature changes.
- Fix: cut the restated part. Describe the meaning, or phrase the condition in
  plain words ("…if it has any").
- Source: neph bot_module.py §BotModule.help

### enumerates-code-shape
- Trigger: a doc lists the files or directories in a system and what each is for
  — a `tree`-shaped table of file → role.
- Why: it transcribes a listing the reader can get from `ls` or their IDE. A
  rename or reorg silently invalidates the table, and no backlink in the renamed
  file points at the doc.
- Fix: drop the listing. If the convention itself is the point, state it in one
  sentence and let the reader confirm by looking. If one file is load-bearing,
  name it once where it matters, with the reason.
- Source: 002 run, T2 `docs/systems/bot-architecture.md` §Modules

### narrates-sequential-code
- Trigger: a doc walks a function's body as numbered steps that mirror the
  code's order ("first X, then Y, then Z").
- Why: it's a second copy of the function in prose. Reordering or merging
  branches silently falsifies it, and reading the function is faster than the
  paraphrase.
- Fix: keep only the *why* of the ordering — what would break if the steps
  swapped. Cut the step-by-step recap.
- Source: 002 run, T2 `docs/systems/bot-architecture.md` §Assembly; T1
  `docs/architecture.md` numbered `main()` walkthrough.

### enum-recap
- Trigger: a doc lists the variants of an enum, status field, or return type
  that the code already defines.
- Why: the enum is the real list. Restating it makes a second source of truth
  that drifts the moment a variant is added, removed, or renamed.
- Fix: name the enum once and let the reader follow it back. If one variant
  carries a reason the code can't, describe that one — not the whole list.
- Source: 002 run, T2 `docs/systems/captcha-gate.md` §"How a join lands".

### behavior-assertion-as-prose
- Trigger: a sentence describes what a function does in a form you could write as
  a test ("X flips Y to false", "X returns N if Z").
- Why: it's behavior the code already proves — a second copy of the implicit
  test — and it drifts the moment behavior changes.
- Fix: if it reads like a test assertion, push it down to a docstring on the
  function, or delete it. Keep only *why* the behavior is the way it is.
- Source: 002 run, T2 `docs/systems/chats-presence.md`;
  `docs/systems/owner-commands.md`.

## Not yet distilled

- `untracked-impl-limitation` (a "known limitations" entry that re-describes the
  implementation and duplicates a tech-debt record with no stable backlink) was
  pulled: it can't be graded without the linked tech-debt file to confirm the
  duplication and the missing backlink. Re-add once a self-contained example
  exists.
- `missing-is-definition` (a doc that explains what a thing *does* but never what
  it *is*) was pulled: the rule is unsettled — a good "does X and Y" summary is
  sometimes enough — and the corpus has no clean example. Revisit with better
  examples.
- The "Owner admin surface" block also re-tells code concepts (endpoint
  signatures, `db.atomic()`, `scope_id` resolution). Folded into
  `consumer-not-system` rather than split into its own transcription smell;
  revisit if a non-consumer instance shows up.
- chat-unions.md notes that joining a union is destructive for game classes and
  "UI should better represent that" (an in-flight rough edge). Unlabelled; reads
  as intentional negative space, not a smell. Left out.
