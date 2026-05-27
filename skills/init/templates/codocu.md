# Codocu
<!-- Created by /codocu:init. Defines this project's documentation conventions, loaded through CLAUDE.md. 
Edit freely. -->

## Docs structure

- **docs/systems/** — the long-term docs home. One file per system, edited
  in place, never date-stamped. This is where durable knowledge lives.
- **docs/plans/** — fleeting working plans. Deleted or folded into a
  system doc on completion.
- **docs/archive/** — folded plans, kept for history. Fold target; never
  hand-edited.

## Backlinks
Use `Auxillary doc: <root_relative_path>` in code files to mark documents that might be affected with changes in this area.  

## Tech Debt
<!--codocu:init This is an optional section. Default: included -->
- **docs/tech-debt.md** — Compact list of known issues, deferred technical work, and explicitly suboptimal choices. Offer to add new entries when appropriate (e.g. solution was implemented suboptimally for now), write after confirmation or on direct request; remove on fix. String ID is more conflict-resistant than numeric.
Format: `**<TD-short-id>**: <what is wrong> - <optional: reason || solution draft>`
If record has a single responsible place in code, leave a backlink in code format of `TODO <TD-short-id>: <short summary>`
<!--codocu:init empty file is created during init -->

## TODO List
<!--codocu:init This is an optional section. Default: included -->
- **docs/todo.md** — Compact list of things to work on next, features and bugfixes. Offer to add new entries when appropriate (e.g. incomplete plan is folding and dangling part needs to be extracted), write after confirmation or on direct request; remove when implemented. String ID is more conflict-resistant than numeric.
Format:
```
# <Version> / <Backlog>
## <TD-short-id> 
<what needs to be done>
```
<!--codocu:init file with empty # Backlog is created during init -->

## Agent guidelines

When editing code which contains a backlink to a document, make sure to check if it was affected and mark it for user to update with codocu.

Agents/skills that come with their dedicated opinionated plan/doc/spec structures must keep documents related to planning and immediate implementation in docs/plans. Plans must contain actual completion status per each step and this status must be updated immeditely after work is done.

## Fold settings

Ask per each incomplete plan: archive as is, extract incomplete parts, leave

## Additional notes

<!-- You can set project-specific documentation rules here — API conventions, security postures, deprecation
policies, anything else that doesn't fit above. -->
