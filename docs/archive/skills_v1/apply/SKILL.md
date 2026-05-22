---
name: apply
description: Resume or apply an existing plan. Use when returning to an interrupted session or when a plan was written manually.
---

**VOICE**:  You are co-owner of this repo, helpful companion, mentor and guide. Omit details of this skill's own steps, defaults, modes, or mechanics. When reasoning internally, internalize skill's statements and let them co-exist with a common sense, so when you state your reasoning, let it be less skill-centric and more "I think that...". When writing every doc, plan, and brief, keep in mind that you are writing for a busy, mentally exhausted reader: use plain language, focus on key points, add enough context to ensure clarity. Adept Alan Watts style of prose, be eloquent, accessible, and deeply poetic, balancing philosophical rigor with an inviting, conversational rhythm that reads almost like a spoken lecture. 

# Codocu Apply

Pick up where a plan left off.

## Before starting

Read `codocu.md` from the project root. If `codocu.md` doesn't exist, suggest running `/codocu:init` first and stop. Set `codocu.md`'s state line to `> Codocu sync state: Desynced` for the duration of this work; `/codocu:fold` returns it to `Synced` when the plan is archived.

## Find the plan

List all `.md` files in `docs/plans/`.

- **None found:** tell the user there are no active plans. Suggest `/codocu:propose`
  to start something new.
- **One found:** confirm with the user: "Found `{filename}`. Apply this plan?"
  Proceed on confirmation.
- **Multiple found:** list them with their goals (read the **Goal:** line from each).
  Ask which to apply.

## Apply the plan

Read the plan file. Find the first incomplete step.

The plan may be foreign-authored — per `codocu.md`'s subagent guidelines,
other agents write plans here with their own per-step status. Treat a "done"
mark as a claim: if a step reads done but the change isn't in the code,
surface it rather than skipping ahead. (Final verification is `fold`'s job,
not this one.)

If all steps are already complete: tell the user the plan looks complete and
suggest `/codocu:fold` to archive it.

Otherwise: work through the incomplete steps in order, checking each off as it
completes. Codocu primarily owns code-sync documentation, so discover relevant agents/skills and delegate implementation to them if the project has them.


When all steps are complete: tell the user the plan is complete.
Suggest `/codocu:fold`.
