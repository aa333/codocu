# Codocu TODO

## 0.2.0 todos

**TD-router-skill-summary-format**
Check if router skill format template is needed when given summary

**Manually touch all skill texts**
- [v] codocu
- [ ] apply
- [ ] code-doc
- [ ] doc-code ?
- [ ] apply
- [ ] fold / sync
- [v] init
- [ ] propose

**consider interaction with other planning/coding agents**
We already allow other agents to write own plans in the inbox folder.
Consider reframing codocu as doc-first agent, delegate plans and coding to others. doc-code sync is good in theory but it wont replace dev specialists. We need a way to compose skills.
Proposal
- make codocu.md an enforced read through CLAUDE - short yet strong doc on how to write documentation (done)
- use specialist skills, superpowers, openspec or whatever to make plans and implement them
- verify codocu standards are applied using hooks (?) or claude.md clauses after implementations
- fold as needed, process inbox during fold
- propose/doc-code/apply stays for now, but less prominent - other tools do spec->plan->code better 

##  Future

**`marketplace.json` and/or npx script for install/distribution testing**
No `.claude-plugin/marketplace.json` exists, so the plugin can only be loaded via `--plugin-dir`. Add a local marketplace manifest so the full `/plugin marketplace add` → `/plugin install codocu@<marketplace>` flow can be tested before publishing.

**Behavioral tuning mechanism — re-design needed**
`docs/tuning.md` (dial registry: voice intensity, reader economy, etc.) was
parked 2026-05-17 — see
`docs/archive/2026-05-17-tuning-registry-deferred.md`. The idea
(developer-time behavioral dials with a defined propagate-to-skills flow) is
worth keeping, but needs a real design: legible handles and a strict,
operable docs→skills(code) generation flow. Until then the skill prose is
the sole source of truth for behavior.

**`/codocu:status` — overview and housekeeping**
Diagnostic: show state of all plans (active, stalled, nearly complete), surface obvious desyncs, suggest next action. Possible home for an auto-fold prompt.

**`:fold` auto-trigger decision**
Currently `:fold` is suggested at end of flows that produced a plan, never forced. Revisit whether to auto-trigger it or tie to a commit hook during plugin stabilization.

**`codocu.md` drift detection**
If the user renames folders, `codocu.md` paths go stale. No mechanism defined. Candidate: a `codocu:init --check` validation step or a `:status` sub-check.

**Proposal Summary persistence**
Proposal Summary is intentionally ephemeral across all flows. Two situations may warrant persisting it — assess during real use:
- *Large brownfield `:code-doc`:* the analysis may be worth keeping as a Plan preamble or a separate artifact (assess during first real brownfield use).
- *Long pre-Plan session:* if a session grows long before a Plan is written (extended scope back-and-forth), consider auto-writing it to disk once a conversation-length threshold is crossed. Most proposals resolve to a Plan within a short session, so this is speculative.

**Richer git tooling**
Current git advisory is binary (md-only / code-only / both). Real git tooling can read diff content, commit messages, and affected modules to make more accurate suggestions and avoid false positives from trivial changes.

**Sync detection optimization**
Current sync detection is agent judgment only. Future options: git-based signals, `@synced-with` code comment markers, structured doc frontmatter. Only pursue if judgment proves insufficient in practice.

**Specialist skill integration**
Skills like `/specialist`, `/superpower`, `/goal` should be aware of Codocu conventions — not do Codocu's job, but follow basic requirements around doc format/placement and cross-linking, since they can (and should!) bring the system into a desynced state just like a human can.

**`npx codocu` install script + NPM publishing**
Installation script that bootstraps `codocu.md` and injects skill instructions for the target agent (Claude Code, etc.). Requires stable v1 plugin first.

**Non-Claude-Code integrations**
Artifact spec and command semantics are integration-agnostic. JetBrains plugin, VS Code extension, or CLI wrapper are post-v1 possibilities.

---

## Meta

**Rewrite `codocu.md` using Codocu**
Once the plugin is stable, eat the own cooking: high-level documentation + principles = long-term docs, skills and agent-specific commands = code. The project itself becomes the best demo of the methodology.

**Plans are executed without ticking step checkboxes**
Codocu dogfoods itself, but its own plans have been executed leaving every step
`- [ ]` even after the work shipped and was committed (e.g. the two plans folded
2026-05-16). `:fold` / `:apply` on this repo must verify deliverables against
code + git history, never trust `[ ]`/`[x]` state. Decide: adopt checkbox
discipline going forward, or document this as an accepted dogfooding deviation
in the spec.
