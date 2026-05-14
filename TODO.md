# Codocu TODO

---

## Before implementation

**Research: code-as-spec prior art**
Gather existing materials, articles, and frameworks around code as a living specification. Use findings to stress-test the design and fill any gaps before building.

---

## V1 implementation notes

**Sync state marker in `codocu.md`**
A short status line at the top of `codocu.md` showing current sync state (Synced / Desynced / Dirty) and a one-liner summary. Updated by commands as they run. Useful for quick orientation in a new session.

**`:fold` is a no-op when no Plan exists**
When `:code-doc` handles a small delta (auto-updates docs, no plan created), `:fold` has nothing to fold. Make this explicit in the `:fold` skill instructions to avoid user confusion.

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

**Richer git tooling**
Current git advisory is binary (md-only / code-only / both). Real git tooling can read diff content, commit messages, and affected modules to make more accurate suggestions and avoid false positives from trivial changes.

**Sync detection optimization**
Current sync detection is agent judgment only. Future options: git-based signals, `@synced-with` code comment markers, structured doc frontmatter. Only pursue if judgment proves insufficient in practice.

**Specialist skill integration**
Skills like `/specialist`, `/superpower`, `/goal` should be aware of Codocu conventions — not do Codocu's job, but follow basic requirements around doc format/placement and cross-linking, since they can bring the system into a desynced state just like a human can.

**`npx codocu` install script + NPM publishing**
Installation script that bootstraps `codocu.md` and injects skill instructions for the target agent (Claude Code, etc.). Requires stable v1 plugin first.

**Non-Claude-Code integrations**
Artifact spec and command semantics are integration-agnostic. JetBrains plugin, VS Code extension, or CLI wrapper are post-v1 possibilities.

---

## Meta

**Rewrite `codocu.md` using Codocu**
Once the plugin is stable, eat the own cooking: high-level documentation + principles = long-term docs, skills and agent-specific commands = code. The project itself becomes the best demo of the methodology.
