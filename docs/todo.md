# Codocu TODO

Roadmap and TODO
Active in-flight work lives in `docs/plans/`, not here.

## 0.2.0
Docs quality of v0.1 is not sufficient. Flows were deemed rigid and redundant.
Active outline: [`docs/plans/2026-05-22-v0.2-plan.md`](plans/2026-05-22-v0.2-plan.md).

**bobatler run produced a lot of inflated bloated documentation**
Need to update skill to ensure document-less greenfield setup does not tempt the agent to restate code and come up with trivial bloated documentation. Test harness required, in progress

**improve initial orientation of core skill**
- search entrypoints
- follow imports, track depth and files amount
- do not read the whole codebase at once, especially if it's big. If it's more than 20 files, ask user if they want a plan and phases for documentation pass


## Backlog

**TD-init-not-offering-inlines**
It's a lot of work, but init on a brownfield should offer inline docs (docstrings, module comments) as well after documentation. If there are >10 files, offer to create a plan for processing them  

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

**TD-eval-identifier-counts**
Eval metrics used to count how many fixture identifiers (functions, classes,
upper-case constants) each produced doc mentioned — the transcription-density
signal. Parked 2026-05-26 because doing it across both Python and TypeScript
fixtures cleanly requires real ASTs for each language (the original Python-only
version used `ast`, but extending to TS by regex is unreliable, and a per-language
AST per fixture is enough scope to deserve its own design pass). Revive once
the fixture roster is stable enough to justify the language-specific tooling
investment.
