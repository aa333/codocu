---
name: fold
description: "Archive completed plans and sync any docs they touched. Also invokable as /codocu:sync. Run at the end of a feature or when you want to wrap up in-progress work."
---

# Codocu Fold

Wrap up one or more plans: verify completion, update docs, archive.

Also invokable as `/codocu:sync` — same behavior.

## Before starting

Read `codocu.md` from the project root, especially the **Fold settings** section.

## Select a plan

List all `.md` files in `docs/plans/`.

- **None:** tell the user there's nothing to fold. Done.
- **One found:** confirm with the user: "Found `{filename}`. Fold this plan?" Proceed on confirmation.
- **Multiple:** list them with their goals. Ask which to fold.
  Offer: "Go through all plans one by one?"

## Per-plan process

### 1. Sanity check

Read the plan's steps. For each step marked done (`- [x]`), briefly verify the
corresponding change actually exists in code. If a checked step appears not to be
implemented, flag it:
> "Step N is marked done but I can't find the corresponding change. Want to
> re-implement it, uncheck it, or skip?"

Do not fail silently. Surface every discrepancy before proceeding.

### 2. Handle incomplete steps

If there are unchecked steps (`- [ ]`):

Read the **Fold settings** in `codocu.md` for the configured default. Apply it
unless the user overrides. Options:

- **Move to tech debt:** append each incomplete step to `docs/tech-debt-todo.md`
  as a `TD-XXXX` item. Scan the file for the highest existing `TD-NNNN` number
  and increment by 1. If no items exist yet, start at `TD-0001`.
- **Create new plan:** write a new `docs/plans/YYYY-MM-DD-{topic}-continued.md`
  with this format:
  ```markdown
  # {Original topic} (continued)

  **Goal:** {copy the Goal from the original plan}

  **Context:** Remaining work from {original plan filename} — deprioritized during fold.

  ## Steps

  - [ ] {remaining incomplete steps from the original plan}
  ```
- **Ask:** present the options and let the user choose per item.
- **Skip:** note the incomplete items in the archive but take no action.

If codocu.md has no fold settings, default to **Ask**.

### 3. Update docs

Check whether the work covered by this plan requires ActualDoc updates per
`codocu.md` conventions. Apply the ActualDoc WHY heuristic: a decision must be documented if (1) the reason is non-obvious from reading the code, (2) an alternative was considered and rejected, (3) an external constraint drove the design, or (4) the absence of something was a deliberate choice. If none apply, the code speaks for itself — skip.

- **Small or obvious update:** draft the change, show it to the user, write on approval.
- **Larger update:** show a diff and ask for explicit approval before writing.

### 4. Archive

Move the plan file from `docs/plans/` to `docs/archive/`.

### 5. Update sync state marker

After archiving, check whether `docs/plans/` is now empty.

- **If empty:** Update the `codocu.md` status line to:
  ```
  > Codocu sync state: Synced
  ```
- **If plans still remain:** Leave the marker unchanged. The project is not fully
  synced until all plans are folded.

### 6. Report

Tell the user:
- Plan archived to `docs/archive/`
- Any docs updated
- Any tech debt items added or new plans created
- Any discrepancies found in the sanity check
