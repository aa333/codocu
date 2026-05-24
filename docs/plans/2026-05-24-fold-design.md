# Fold — Design

> Status: design approved in brainstorming 2026-05-24; revised twice the same
> day. First revision dropped the per-plan subagent after smoke-testing
> showed it couldn't see cross-plan context. Second revision dropped the
> 7-step procedural flow after side-by-side testing showed naked Claude
> produced equivalent output at one-third the cost. Current shape: a
> ~25-line skill that loads conventions and frames the task, then trusts
> the model. Standalone sub-project; supersedes the v0.1 `fold`/`sync`
> skills in `docs/archive/skills_v1/`. The B-review bullet in
> `2026-05-22-track-b-decomposition.md` is treated as done by B-core
> (the `codocu-reviewer` subagent covers it).

## What fold is

`/codocu:fold` tidies up the record. It walks open plans, surfaces what's
done and can be archived, identifies what shipped that may need long-term
docs, and processes the inbox.

The skill itself is small — frontmatter, voice anchor, a load-first
instruction, a short list of conventions, and a closing line that says
"land it on the user's ask." No procedural flow. Naked Claude with the
conventions loaded does the work; the skill's job is to frame the task
and ensure the conventions are present.

It is a sibling to `/codocu`, not a child. The two skills compose: fold
hands shipped change sets to `/codocu`'s Place primitive; `/codocu`
decides whether docs are warranted and where they go. Neither needs to
swallow the other.

## The skill family

- **`/codocu:fold`** — the new user-invokable skill. `skills/fold/SKILL.md`.
  Frontmatter `name: fold`; invocation prefix `/codocu:` from the plugin
  namespace.

No subagent. No fold-specific verifier. No agent file.

No `/codocu:sync` alias. v0.1 had `sync` as an alias for `fold`; v0.2
dropped the sync-state vocabulary in B-core, and a single verb keeps the
surface clean.

## What fold loads

The target repo's `codocu.md` only (always — it carries archive layout,
inbox location, and local conventions).

Fold does not load principles, voice, or the corpus. Writing is delegated
to `/codocu`, which loads its own pack at that point. Verification is
mechanical and uses tools (Glob/Read/Grep/Bash) rather than loaded knowledge.

## The conventions fold carries

These live in `skills/fold/SKILL.md`. They're the load-bearing differentiators
between fold and an un-skilled invocation:

- **Don't trust checkboxes alone.** A plan claims done; the truth is code,
  git history, and any results notes the plan or its companion files carry.
- **Design and implementation plans archive together.** They're a pair.
- **Don't archive a plan whose validation work is documented as deferred.**
  Check the plan's status block and any sibling `testing/` or `results.md`
  files.
- **For shipped work, ask `/codocu` what needs doc treatment.** Hand it the
  shipped change set; `/codocu`'s Place primitive applies the warrantedness
  gate and decides. Fold doesn't pre-filter — it doesn't have principles or
  doc-standard loaded.
- **Inbox drafts** (`docs/inbox/*.md` not ending in `.defer.md`) get
  absorbed into evergreen docs via `/codocu`.

## Dependency: a Place warrantedness gate

Fold's "ask `/codocu` what needs doc treatment" convention relies on
`/codocu`'s Place primitive being able to return `no doc needed` for
trivial / code-explanatory changes. Place as written today has five outcomes
(new doc, fold into existing, push down to docstring, breadcrumb-only,
absorb-then-delete) and no "nothing needed" option.

This design requires one additive edit to `skills/codocu/SKILL.md`: add a
leading **doc-warrantedness gate** as Place's first sub-decision. One
paragraph, before the five options:

> First, decide whether documentation is warranted at all. If the change is
> trivial or carried by self-explanatory code (a rename, a small refactor, a
> bug fix the code already explains), the answer is *no doc needed* — return
> that and stop. Apply this gate to every Place call.

This is sibling work to fold itself, not part of fold, but both ship
together.

## Why the procedural flow went away

The first design carried a 7-step flow (survey → verify → decide → survey-for-docs
→ archive → inbox → report). The second smoke test ran fold side-by-side
with a naked Claude invocation against the same set of plans. Naked
Claude produced equivalent classification at one-third the cost. The
one place fold genuinely caught something naked Claude missed —
conservative bias on a plan whose validation was documented as deferred —
came down to a single rule, not the whole flow.

So the procedural ceremony got cut. The differentiating rules are now in
the skill's conventions list; everything else lives in the model's
defaults.

## Why no subagent

(Kept for posterity — this was discovered before the procedural strip-down.)

The first design used a per-plan `fold-verifier` subagent. Smoke testing
found two structural problems:

1. **Cross-plan context is essential.** Plans relate to each other —
   supersession, design/impl pairs, decomposition parent → sub-projects.
   A subagent seeing one plan at a time can't classify by lineage; it
   can only verify in a vacuum.
2. **Scale was bad.** One subagent per plan means N model calls for N plans.
   Most plans (outlines, decompositions, designs, seeds) classify cheaply by
   header alone. The `codocu-reviewer` subagent in B-core earns its keep
   because each doc review needs the smell catalog loaded with real isolation
   value. Plan verification has neither benefit.

The subagent was removed in revision 1; revision 2 removed the procedural
flow that had survived its loss.

## v0.1 deltas — implementer orientation, not SKILL.md material

Concepts v0.1 carried that v0.2 explicitly drops. Listed so the implementer
doesn't reintroduce them out of habit. **Do not seed any of this vocabulary
in SKILL.md.**

- **`Codocu sync state:` line.** v0.1 fold ended by writing `Synced` to
  `codocu.md`. The state machine is gone; the line goes with it. Stale
  references in `codocu.md` and `CLAUDE.md` are on B-cleanup's docket.
- **`sync` alias.** Dropped.
- **"Standard to compare against."** v0.1 fold said "codocu.md is
  authoritative — there's no standard to compare against." v0.2 has a
  standard (the doc-standard + corpus); `/codocu` enforces it. Fold
  composes with that, doesn't override it.

## Deferred and known gaps

- **Plan-format expectations.** Fold reads plans as they're written today —
  free-form markdown with a `> Status` block on top. If a stricter format
  appears later, fold can lean on it.
- **Semantic verification.** Fold checks mechanical evidence — did the
  artifact land, does the symbol exist, did git record the rename. The
  deeper "the doc says X but the code now behaves like Y" question is
  `/codocu`'s Verify-against-code primitive (mechanical-only in v0.2).
- **Scale beyond ~100 plans.** Not handled; not tested. The lighter shape
  scales as well as the model itself does at classifying markdown headers.
  If a real repo hits the wall, the next lever is a marker convention
  (e.g., `Status: candidate-for-fold` on plans the user thinks are done).
  Wait for the gap to show up.

## Reader test

> Where would the intended reader — a contributor implementing fold or
> revisiting the design later — get lost or bored?
>
> Risk: a reader expects the skill body to be longer because most skills
> are. The "What fold is" section explicitly calls out that the body is
> small by design and explains why.
>
> Risk: the Place warrantedness gate looks like sibling work but is a hard
> dependency. Called out in its own section.
>
> Risk: a reader might wonder where the 7-step flow went, or the subagent.
> Both have explicit sections explaining the cut. Saves the next reader
> re-litigating decisions that are already settled.
