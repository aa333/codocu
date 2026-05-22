# Codocu TODO

Roadmap and TODO
Active in-flight work lives in `docs/plans/`, not here.

## 0.2.0
Docs quality of v0.1 is not sufficient. Flows were deemed rigid and redundant.
Active outline: [`docs/plans/2026-05-22-v0.2-plan.md`](plans/2026-05-22-v0.2-plan.md).

- Skills for reviewer subagents. Strict, rigid flows, at least Sonnet-viable, launched by main agent to verify doc standards against simple rules.


## Backlog

**TD-corpus-enrichment-skill**
A skill that expands/enriches the `docs/corpus/` assets (smell catalog, voice
pairs, placement rules, eval fixtures) from new or updated METADOCU-narrated
sources. The v0.2 B-extract pass distills the corpus by hand; this automates the
later regeneration. Ties to the "scriptable later" pipeline note in
`docs/plans/2026-05-22-track-b-decomposition.md` and overlaps Track C.

**TD-router-skill-summary-format**
Check if the router skill needs a format template when handed a summary.

**TD-autoconstruct-skill-prompts**
Centralized voice control and replace, for example. Overlaps a lot with TD-tuning-redesign

**TD-marketplace-manifest**
No `.claude-plugin/marketplace.json` exists, so the plugin can only be loaded
via `--plugin-dir`. Add a local marketplace manifest so the full
`/plugin marketplace add` → `/plugin install codocu@<marketplace>` flow can be
tested before publishing.

**TD-tuning-redesign**
`docs/tuning.md` (dial registry: voice intensity, reader economy, etc.) was
parked 2026-05-17 — see `docs/archive/2026-05-17-tuning-registry-deferred.md`.
The idea (developer-time behavioral dials with a defined propagate-to-skills
flow) is worth keeping, but needs a real design: legible handles and a strict,
operable docs→skills(code) generation flow. Until then the skill prose is the
sole source of truth for behavior.

**TD-status-skill**
`/codocu:status` — diagnostic that shows the state of all plans (active,
stalled, nearly complete), surfaces obvious desyncs, and suggests the next
action. Possible home for an auto-fold prompt.

**TD-fold-autotrigger**
`:fold` is currently suggested at the end of flows that produced a plan, never
forced. Revisit whether to auto-trigger it or tie it to a commit hook during
plugin stabilization.

**TD-codocu-drift-detection**
If the user renames folders, `codocu.md` paths go stale. No mechanism defined.
Candidate: a `codocu:init --check` validation step or a `:status` sub-check.

**TD-richer-git-tooling**
Current git advisory is binary (md-only / code-only / both). Real git tooling
can read diff content, commit messages, and affected modules to make more
accurate suggestions and avoid false positives from trivial changes.

**TD-sync-detection-opt**
Sync detection is agent judgment only. Future options: git-based signals,
`@synced-with` code comment markers, structured doc frontmatter. Pursue only
if judgment proves insufficient in practice.

**TD-specialist-skill-integration**
Skills like `/specialist`, `/superpower`, `/goal` should be aware of Codocu
conventions — not do Codocu's job, but follow basic doc format/placement and
cross-linking rules, since they can bring the system into a desynced state
just like a human can.

**TD-npx-install-script**
`npx codocu` install script + NPM publishing. Bootstraps `codocu.md` and
injects skill instructions for the target agent (Claude Code, etc.). Requires
a stable v1 plugin first.

**TD-non-cc-integrations**
Artifact spec and command semantics are integration-agnostic. JetBrains
plugin, VS Code extension, or CLI wrapper are post-v1 possibilities.
