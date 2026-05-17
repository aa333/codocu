# Codocu TODO


## V1 todos

**Spec A (long-term doc style) — implemented, unverified, uncommitted**
`docs/superpowers/plans/2026-05-17-codocu-longterm-doc-style.md` tasks 1–3 + 5–8
are done in the working tree: spec Principles split + ActualDoc WHAT/WHY/WHERE
bound (`docs/superpowers/specs/2026-05-14-codocu-design.md`); in-voice
WHAT-summary propagated into `fold`, `code-doc`, `codocu` orientation, and
`skills/codocu/references/deep-drill.md`; `testing/2026-05-17-longterm-doc-style/`
instrument created. Outstanding by owner decision:
- Validation (plan Tasks 4 & 9) is consolidated into ONE combined Spec-A +
  Spec-B harness run, after the Spec B plan is implemented. **Spec A behavior is
  unverified until then.** Capture the baseline against the last commit *before*
  the combined Spec-A/B commit.
- Plan Task 10 (single commit) deferred; Spec A edits are uncommitted and will
  be committed together with Spec B per the combined-test decision.
- Spec B (Codocu onboarding model — router↔`:init`, `codocu.md` opinionated
  generation, existing-docs stance) is the next brainstorming cycle; it builds
  on Spec A's principle + heuristic. See
  `docs/superpowers/specs/2026-05-17-codocu-longterm-doc-style-design.md`
  ("Relation to other specs").

**Improve codocu.md**
Iterate on template clarity. Add 2-3 template options, allow choosing during init with a short summary. Store with skill as files, just copy.

**`:fold` is a no-op when no Plan exists**
When `:code-doc` handles a small delta (auto-updates docs, no plan created), `:fold` has nothing to fold. Make this explicit in the `:fold` skill instructions to avoid user confusion.

**`:fold` test suite check**
Before archiving a plan, `:fold` should verify the test suite passes. If tests fail, block archiving and report which steps may be incomplete. Exact behavior on failure (warn-only vs. hard block) configurable in `codocu.md`. Implement and test against a real project before finalizing policy.

**`marketplace.json` and/or npx script for install/distribution testing**
No `.claude-plugin/marketplace.json` exists, so the plugin can only be loaded via `--plugin-dir`. Add a local marketplace manifest so the full `/plugin marketplace add` → `/plugin install codocu@<marketplace>` flow can be tested before publishing.

**Usage feedback**
- Still a little bit rough on the edges around "I didnt write anything!" in the proposal stage. Should be giving "this is a quick proposal, take a quick look, discuss and I'll make a plan" 
```
The drill itself wrote nothing — no files, no codocu.md, no plan on disk. To persist this plan and wire Codocu around your existing OpenSpec + docs/systems/docs/plans/tech-debt.md layout, the next step is /codocu:init — but that's a separate, explicitly-gated action. Say the word and I'll walk it; otherwise this stands as your read.
```
- codocu analysis router declined saving a plan until codocu.md is initialized. I'd rather allow users to get progressive adoption.
- codocu: init listed as separate, gated - as a user, I've no idea what that means. We need simpler terms and we need router to be able to soft-init codocu.
- and init skill itself should guide me throug several steps, like long-term documentation level (module/system/whatever), do I need techdebt, how do I want to fold incomplete plans. I think that's better than template. In this case skill can ask questions and propose variants based on existing docs and repo state, but sensible defaults should lean towards codocu principles  

**Revisit how codocu treats CLAUDE.md and how it wires codocu.md into it**
CLAUDE.md right now reiterates a lot of paths which are already defined in codocu, and we have to edit them in 2 places. Let's just encourage a single reference from CLAUDE.md

**Apply Varya's prompt**


## V2 / Future

**`/codocu:status` — overview and housekeeping**
Read-only diagnostic: show state of all plans (active, stalled, nearly complete), surface obvious desyncs, suggest next action. Possible home for an auto-fold prompt.

**`:fold` auto-trigger decision**
Currently `:fold` is suggested at end of flows that produced a plan, never forced. Revisit whether to auto-trigger it or tie to a commit hook during plugin stabilization.

**`codocu.md` drift detection**
If the user renames folders, `codocu.md` paths go stale. No mechanism defined. Candidate: a `codocu:init --check` validation step or a `:status` sub-check.

**ProposalSummary persistence for large brownfield `:code-doc`**
ProposalSummary is ephemeral across all flows. For large brownfield documentation efforts the analysis may be worth keeping — as a Plan preamble or a separate artifact. Assess during first real brownfield use.

**ProposalSummary persistence threshold**
ProposalSummary is intentionally ephemeral. If a session grows long before a Plan is written (e.g., extended back-and-forth on scope), consider writing it to disk automatically once a conversation length threshold is crossed. Assess during real use — most proposals resolve to a Plan within a short session.

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
