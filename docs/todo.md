# Codocu TODO

Roadmap, TODO, and tech-debt records. Format per `codocu.md` §Roadmap:
`**TD-short-id**` header, then a short summary of what is wrong / what to do.
Active in-flight work lives in `docs/plans/`, not here.

## 0.2.0

**TD-router-skill-summary-format**
Check if the router skill needs a format template when handed a summary.

**TD-doc-first-reframe**
Consider reframing Codocu as a doc-first agent that delegates planning and
coding to specialist skills, rather than owning the full spec→plan→code loop.
`doc-code` sync is sound in theory but won't replace dev specialists; we need
a way to compose skills. Direction:
- `codocu.md` enforced-read via CLAUDE.md — short, strong doc-writing rules (done)
- use specialist skills (superpowers, openspec, etc.) to make/implement plans
- verify Codocu standards post-implementation via hooks or CLAUDE.md clauses
- fold as needed; process inbox during fold
- keep `propose`/`doc-code`/`apply` but less prominent — other tools do
  spec→plan→code better

## Future

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
