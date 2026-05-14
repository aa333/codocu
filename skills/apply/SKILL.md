---
name: apply
description: Resume or apply an existing plan. Use when returning to an interrupted session or when a plan was written manually.
---

# Codocu Apply

Pick up where a plan left off.

## Before starting

Read `codocu.md` from the project root. If `codocu.md` doesn't exist, suggest running `/codocu:init` first and stop.

## Find the plan

List all `.md` files in `docs/plans/`.

- **None found:** tell the user there are no active plans. Suggest `/codocu:propose`
  to start something new.
- **One found:** confirm with the user: "Found `{filename}`. Apply this plan?"
  Proceed on confirmation.
- **Multiple found:** list them with their goals (read the **Goal:** line from each).
  Ask which to apply. Offer: "Apply all in sequence?" as an option.
  When applying multiple plans in sequence: complete each plan fully before moving
  to the next. If a step cannot be completed, stop and report to the user — do not
  skip to the next plan.

## Apply the plan

Read the plan file. Find the first unchecked step (`- [ ]`).

If all steps are already checked: tell the user the plan looks complete and
suggest `/codocu:fold` to archive it.

Otherwise: work through the unchecked steps in order, checking each off as it
completes. Show the user each step before executing so they can redirect.

When all steps are checked: tell the user the plan is complete.
Suggest `/codocu:fold`.
