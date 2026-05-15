---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads signals and guides you to the right action.
---

# Codocu Router

Figure out where things stand and what to do next.

## Read signals

Gather these quickly — no full project scan:

1. **`codocu.md`**: does it exist? If not, suggest `/codocu:init` and stop.

2. **Active plans**: list files in `docs/plans/` — any in progress?

3. **Git** (if available): `git status` — what files have uncommitted changes?
   - Only `.md` files → hint: docs are ahead, consider `:doc-code`
   - Only code files → hint: code is ahead, consider `:code-doc`
   - Both → check active plans first (see conflict section below)

## Present findings

Tell the user what you found. Be concise:
> "Here's what I see: [uncommitted code changes in X, Y] and [active plan: Z].
> What would you like to do?"

If signals point clearly to one action (e.g. only code changed, no active plans),
suggest it directly and ask for confirmation.

If there is an active plan and uncommitted code changes, that is normal mid-feature
state — suggest `/codocu:apply` to continue the plan rather than entering conflict
resolution.

## Case 4 — both sides changed (conflict)

If both code and docs have uncommitted changes AND there is no active plan in `docs/plans/`, this is a conflict that needs resolution. Or if the user says "things are a mess":

Update the sync state marker in `codocu.md`: find the line beginning with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`.

Walk through the conflicts area by area:
> "In [area], the docs say [X] and the code does [Y]. Which is the intended truth?"

Record the user's answers. Once all areas are resolved, write a resolution plan:

```markdown
# Resolution Plan

**Goal:** Bring code and docs into sync

## Steps

- [ ] [area 1]: update [code/docs] to match [docs/code]
- [ ] [area 2]: ...
```

Save to `docs/plans/YYYY-MM-DD-resolution.md`.

Implement per plan. Suggest `/codocu:fold` when done.

## No conflicts — triage

If no conflicts but user isn't sure what to do:

- Active plan + uncommitted code changes → suggest `/codocu:apply` to continue the plan (this is normal mid-feature state, not a conflict)
- Active plan exists → suggest `/codocu:apply` to continue it
- No active plan, project is clean → suggest `/codocu:propose` for something new
- No git → ask: "What changed recently? Docs, code, or both?"
