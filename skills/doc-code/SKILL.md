---
name: doc-code
description: Docs describe the desired state — implement them in code. Use when you have already written or edited docs and want to implement what they describe.
---

# Codocu Doc-Code

The docs are the proposal. Write a plan and implement it.

## Before starting

Read `codocu.md` from the project root. If `codocu.md` doesn't exist, suggest
running `/codocu:init` first and stop.

Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`. `/codocu:fold` will restore this to `Synced` when the plan is archived.

## Identify the docs delta

Ask the user which docs they changed or are treating as the spec, if they haven't
already said. If git is available, check `git diff` for changed `.md` files and
offer those as candidates — but the user decides. If git is not available, ask
the user: "Which docs are you working with?"

Read the identified docs.

## Write the plan

No ProposalSummary step — the docs are the proposal.

Write a plan to `docs/plans/YYYY-MM-DD-{topic}.md` describing the code changes
needed to implement what the docs describe.

Plan format:
```markdown
# {Topic} Plan

**Goal:** {what the docs are specifying}

**Source docs:** {list of doc files being implemented}

## Steps

- [ ] Step 1: ...
```

Show the plan to the user and ask if it looks right before proceeding.
Iterate if needed.

## Implement

Work through the plan steps in order, checking each off as it completes.
When all steps are done, suggest `/codocu:fold`.
