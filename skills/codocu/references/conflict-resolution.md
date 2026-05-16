# Codocu — Case 4 Conflict Resolution

Loaded by `/codocu` only when resolving a both-sides conflict (Case 4): both
code and docs have uncommitted changes and there is no active plan in
`docs/plans/`, or the user says "things are a mess".

If `codocu.md` exists, update its sync state marker: find the line beginning
with `> Codocu sync state:` and replace it with `> Codocu sync state: Dirty`.
If it does not exist, skip this (you are in read-only orientation) — do not
create the file; note that `/codocu:init` is required to persist sync state.

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
