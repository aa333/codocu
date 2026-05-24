# Codocu

<!-- codocu:init init skill to execute and strip all meta comments starting with `codocu:init` -->

<!-- Created by /codocu:init. Defines this project's documentation conventions, loaded through CLAUDE.md. 
Edit freely. -->

## Docs structure

- **docs/systems/** — the long-term docs home. One file per system, edited
  in place, never date-stamped. This is where durable knowledge lives.
- **docs/plans/** — fleeting working plans. Deleted or folded into a
  system doc on completion.
- **docs/archive/** — folded plans, kept for history. Fold target; never
  hand-edited.


## Tech Debt

- **docs/tech-debt.md** — Compact list of known issues, deferred work, and explicitly suboptimal choices. Add freely; remove on fix.
Format: `**<TD-short-id>**: <what is wrong> - <optional: reason for not fixing || solution draft>`
<!--codocu:init This is an optional feature, init skill shall ask user if it needs to be included in final codocu.md -->

## Agent guidelines

Agents/skills that come with their dedicated opinionated plan/doc/spec structures must keep documents related to planning and immediate implementation in docs/plans. Plans must contain actual completion status per each step. 

## Fold settings

Ask per each incomplete plan: archive as is, extract incomplete parts, leave

## Additional notes

<!-- You can set project-specific rules — API conventions, security postures, deprecation
policies, anything else that doesn't fit above. -->
