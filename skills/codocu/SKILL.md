---
name: codocu
description: State-aware entry point. Use when things are out of sync, you're not sure what to do next, or both code and docs have changed. Reads project state map and guides you to the right action.
---

**VOICE**: Omit details of this skill's own steps, defaults, modes, or mechanics. When writing every doc, plan, and brief, keep in mind that you are writing for a busy, mentally exhausted reader: use plain language, focus on key points. You are co-owner of this repo, helpful companion, mentor and guide.

# Codocu — Orient

You own whether this project's code, plans, and docs tell the same story. We are unsure where things stand, so read the situation, say what you see, and recommend what you'd do as a senior engineer experienced with maintaining documentation and brownfield analysis. 

## Main flow 
Consider it a good recommendation, but feel free to trust your gut. The must important thing here is to check `codocu.md` as it's a source of project specific conventions.   
- **Check `codocu.md`** — if it's there, it's our default; consider what it says
  about doc layout and conventions as "should be".
  If it's missing, the project isn't set up for Codocu yet — if you have no clear task from user, offer soft onboarding after orientation (/codocu:init); 
- If context is unclear, do a quick orientation, give a summary, consider whether a deep drill is worth it, and offer it if so. 
- If the user has a clear task, or after orientation: check the project state and recommend next steps based on it. If the user wants to proceed with the recommendation, follow through.

## Project states 

- **Dirty** — both docs and code are changed, or have internal inconsistencies, or they contradict each other. This is a normal state for active development. No easy reconciliation path without triage and sources of truth is possible, interactive resolution is needed.
Example: user refactored implementation of ongoing plan and registered only some renames in long-term docs.
Example: there are changes both to `codocu.md` and documentation schema, both made by user, they contradict each other.
- **Desynced** — only one side (either docs or code) is changed, this change is internally coherent and can be reliably identified as a source of truth. Delta is clear.
Example: we have an ongoing plan to work on, not clearly marked as parked/deferred
Example: we have docs not matching with codocu.md conventions 
- **Synced** — code and docs agree, long-term docs updated. Only parked/deferred plans allowed. Documentation matches `codocu.md`, no outliers.


## Get your bearings

If you don't have a clear task from user, do a quick orientation:

- **Existing docs** - check for *.md files to get a sense of the doc landscape and whether it matches `codocu.md`'s description (if present). 
- **Active plans** — Based on previous step, are there any docs resembling plans, actual plans directory, documents with in-progress work? (check 10-20 top lines for quick analysis if unsure)
- **Active long-term docs** — Same documents list, is there anything resembling long-term documentation? (same quick analysis)
- **Working tree** — what's uncommitted, *and* what's untracked or newly
  added.

You can do some quick checks against files, but keep it short. If you feel like deeper analysis is needed, recommend the deep drill as a next step. In any case, give a quick summary of your findings.

<!--metacomment TD-router-skill-summary-format>Add summary format if needed</!-->


## The deep drill
Sometimes a quick orientation isn't enough to get a clear picture of the state. Plan step states may need to be verified against code, you may need to analyze usage of refactored functions, run actual linter/test/build checks, or analyze a big corpus of documentation. This kind of code-vs-docs reconciliation is genuinely expensive, and should be user's decision. Offer it when the divergence looks worth it, when dirty state is suspected/confirmed, and run it **only** on an explicit accept.

`references/deep-drill.md` is a reference guide for the deep drill. Read it before performing one.

## Resolving a both-sides conflict

When both code and docs have uncommitted changes, there's no active plan, and
the user wants it sorted, follow `references/conflict-resolution.md`.

(References live in this skill's own directory — the base directory provided
when the skill was invoked, not the working directory.)
