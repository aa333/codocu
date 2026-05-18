---
name: code-doc
description: Code is the source of truth — update docs to reflect it. Use after manual code changes, refactors, or to document an undocumented area.
---

# Codocu Code-Doc

Read what changed in code and bring the docs up to date.

_You own this project's code/doc coherence — talk about the project and the next move, never about this skill's own steps, defaults, modes, or mechanics. Write every doc, plan, and brief for a busy reader: lead with the answer, say it once, cut anything that just restates the code._

## Before starting

Read `codocu.md` from the project root for doc conventions (locations, format).
If `codocu.md` doesn't exist, suggest running `/codocu:init` first and stop.

## Identify the code delta

If git is available, run `git diff` as a starting hint. Tell the user what you see
and ask if that's the area to work with, or if they have something else in mind.
If git is not available, ask the user: "Which area or files should I look at?"

Read the relevant code.

## Assess scope

Judge the size and nature of the change:
- **Small:** a few files changed, clear mapping to existing docs (e.g. a new field,
  a renamed method, a small new function). Proceed directly to auto-update.
- **Large / brownfield:** significant architectural change, many files, or an area
  with no existing docs. Use the proposal flow.
- **Uncertain:** ask the user — "This looks like [X]. Is this a small update or
  should we make a plan?"

## Small scope path

Identify the ActualDocs that cover the changed area per `codocu.md` conventions.

Any ActualDoc you write or update follows the long-term doc standard: an orientation map — the area's purpose, its place in the system, its public contract, its direction — holding nothing an internal-only refactor would change; that detail is the code's job. A decision earns a line only when the reason isn't obvious from the code, an alternative was weighed and dropped, an external constraint forced it, or an absence was deliberate. If none of that applies, the code already says it — no doc update needed. (Canonical statement: the codocu skill's `references/doc-standard.md`.)

Draft the updated doc sections. Show diffs to the user before writing:
> "I'd update [file] with these changes: [diff]. Look right?"

Write on approval.

Set `codocu.md`'s state line to `> Codocu sync state: Synced`. Done — no plan, no fold needed.

## Large / brownfield path

Draft a **ProposalSummary** in-conversation:
- What to document (areas, modules)
- Which existing docs to update
- Which new docs to create

Each doc follows the long-term doc standard: the orientation-map shape, and
the bar a decision must clear to earn a line. (Canonical statement: the
codocu skill's `references/doc-standard.md`.)

Ask for approval. Iterate until approved.

Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.

Write a documentation plan to `docs/plans/YYYY-MM-DD-document-{area}.md`:
```markdown
# Document {Area} Plan

**Goal:** {what will be documented}

## Steps

- [ ] Step 1: Write/update {doc file} covering {area}
- [ ] Step 2: ...
```

Work through the plan, writing and updating docs per `codocu.md` conventions.
When done, suggest `/codocu:fold`.
