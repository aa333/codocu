# Codocu — Dirty State Conflict Resolution

Loaded by `/codocu` only when resolving a both-sides conflict: both
code and docs have uncommitted changes and there is no active plan in
`docs/plans/`, or the user says "things are a mess". Repository is in Dirty state.

If `codocu.md` exists, set its state line to `> Codocu sync state: Dirty`.

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
