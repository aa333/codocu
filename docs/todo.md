# Codocu TODO


## V1 todos

**Improve codocu.md**
Iterate on template clarity. Add 2-3 template options, allow choosing during init with a short summary. Store with skill as files, just copy.

**`:fold` is a no-op when no Plan exists**
When `:code-doc` handles a small delta (auto-updates docs, no plan created), `:fold` has nothing to fold. Make this explicit in the `:fold` skill instructions to avoid user confusion.

**`:fold` test suite check**
Before archiving a plan, `:fold` should verify the test suite passes. If tests fail, block archiving and report which steps may be incomplete. Exact behavior on failure (warn-only vs. hard block) configurable in `codocu.md`. Implement and test against a real project before finalizing policy.

**`marketplace.json` and/or npx script for install/distribution testing**
No `.claude-plugin/marketplace.json` exists, so the plugin can only be loaded via `--plugin-dir`. Add a local marketplace manifest so the full `/plugin marketplace add` → `/plugin install codocu@<marketplace>` flow can be tested before publishing.

**Usage feedback**
see feedback-transcript.md

**Revisit how codocu treats CLAUDE.md and how it wires codocu.md into it**
CLAUDE.md right now reiterates a lot of paths which are already defined in codocu, and we have to edit them in 2 places. Let's just encourage a single reference from CLAUDE.md

**Strengthen the public-API field-rename check (deep-drill.md §5)**
The ProfileData `status_label`→`member_status_str` / `status`→`member_status`
rename was missed in iter-01, iter-02, AND iter-03 — the §5 deterministic
check was added specifically to close this and still did not fire. The
changed-surface anchor reconciles modules but isn't enumerating renamed public
fields from diffs in practice. Next iteration: make §5 a hard, explicit
per-changed-API-object field enumeration step with a worked example, not a
prose instruction.

**Bare-assent behavioral cliff in the plan-gated drill**
iter-03 worst-case ("Yes, do the drill.") correctly disclosed cost + presented
the triaged plan but **withheld even the cheap changed-surface findings** —
the claimed-complete≠done divergence appeared only as an unexecuted plan step.
The slightly richer MAIN prompt ("perform that deeper drill-down now") DID
surface it. So there's a cliff: minimal assent loses the priority finding.
Consider revising deep-drill.md so the always-bound, already-cheap
changed-surface reconciliation is reported even on bare assent, gating only the
heavier per-tier audit behind a second go-ahead. Retest both prompts.

**Reconcile the deep-drill plan with the reorganized `testing/` layout, then fold it**
`docs/superpowers/plans/2026-05-16-codocu-deep-drill-cost-redesign.md` is
substantively implemented in `skills/codocu/` (lean `SKILL.md` +
`references/deep-drill.md` + `references/conflict-resolution.md`, plus the
template and spec edits). Outstanding:
- Task 6 references stale paths (`testing/neph-state-guard.ps1`,
  `testing/report-template.md`, `testing/report-iter-03.md`,
  `testing/transcripts/iter-03.*`, `testing/session-test-dirty-orientation-01.md`).
  The harness was reorganized to `testing/tools/state-guard.ps1` +
  `testing/tools/report-template.md`, and the iter-03-equivalent runs now live
  under `testing/2026-05-16-dirty-repo-exploration/` (run1–3 + worstcase,
  `summary.md`). Update Task 6's paths to the new layout / `testing/README.md`
  conventions and confirm the suite covers Task 6's intent.
- Then do Task 7 (single commit + `test-iter-03` tag) and `/codocu:fold` the plan.
- The new `testing/tools/`, `testing/README.md`, and
  `testing/2026-05-16-dirty-repo-exploration/` are untracked and need committing;
  the old `testing/` paths show as deletions until the rename is staged.
---

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
