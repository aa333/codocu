---
name: propose
description: Start a new feature or change from intent. Creates a plan after proposal approval. Use when you know what you want to build and the project is (roughly) in sync.
---

# Codocu Propose

Turn a new intent into an approved plan, ready to implement.

_You own this project's code/doc coherence — talk about the project and the next move, never about this skill's own steps, defaults, modes, or mechanics. Write every doc, plan, and brief for a busy reader: lead with the answer, say it once, cut anything that just restates the code._

## Before starting

Read `codocu.md` from the project root. If it doesn't exist, suggest running
`/codocu:init` first and stop.

Set `codocu.md`'s state line to `> Codocu sync state: Dirty` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.

## Dirty state warning

A couple of quick signals — no full project scan:
- `git status` if git is available: any uncommitted changes?
- `docs/plans/`: any active plan files?

If either signal is positive, warn the user:
> "There are [uncommitted changes / active plans] — you may want to resolve those
> first. If there's an active plan, `/codocu:apply` can resume it. Otherwise
> `/codocu` can help you sort out the state. Continue anyway?"

Do not block. If the user confirms, proceed.

## Proposal

Ask the user what they want to build or change, if they haven't already said.
Draft a **ProposalSummary** in the conversation — it stays in the conversation, not on disk:

- **Scope:** what is changing (modules, APIs, data, etc.)
- **Affected areas:** files or systems likely to be touched
- **Risks or open questions:** anything that could go wrong or needs a decision

Present it and ask: "Does this look right? Anything to add or change?"
Iterate until the user approves.

## Write the plan

Once approved, write the plan to `docs/plans/YYYY-MM-DD-{topic}.md`
where `{topic}` is a short kebab-case summary of the intent (e.g. `user-createdat`).

Plan format:
```markdown
# {Topic} Plan

**Goal:** {one sentence from the proposal}

**Context:** {relevant background, 2-4 sentences}

## Steps

- [ ] Step 1: ...
- [ ] Step 2: ...
```

Steps should be concrete and granular. Each step should be completable in one
focused action. Prefer too many small steps over too few large ones.

## After writing

Tell the user where the plan was written. Ask:
> "Ready to start implementing? I can work through the plan now, or you can
> pick it up later with `/codocu:apply`."

If they want to start: begin implementing the plan steps in order, checking each
off (`- [x]`) as it completes.
When all steps are done, suggest `/codocu:fold`.
