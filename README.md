# Codocu

**COde-as-a-DOCUment** — an LLM-agent workflow kit that keeps code, short-term
plans, and long-term documentation coherent through an explicit lifecycle.
Delivered as a Claude Code plugin.

**Core bet:** well-written code is already the most detailed spec possible.
Documentation supplements it — it does not translate it. The differentiator is
lightweight, bidirectional sync between code and docs.

## Who it's for

IT-first builders: solo developers, small technical teams, and technical
founders who want to ship maintainable software without drowning in process or
doc overhead.

Codocu operates at the single-project level. Its job is keeping a project's
*what was / what is / what will be / why* coherent with its code.

**Out of scope:** system-of-systems architecture, cross-team API contracts,
stakeholder PRDs, infrastructure specs. Codocu docs may reference these, but
Codocu does not manage them.

## How it works

Codocu tracks the project as being in one of three states:

| State | Meaning |
|---|---|
| **Synced** | Code and long-term docs represent the same reality. Active plans may exist (planned future work is not a desync). Tests pass. |
| **Desynced** | One side changed; the other is internally coherent. Directional sync is possible once a source of truth is chosen. |
| **Dirty** | Both sides in motion or contradictory. Iterative resolution with the user. Normal during active development. |

The state lives on the first line of `codocu.md` (a free-form meta-doc at the
project root, created by `:init`) so any new session orients instantly.

You drive the lifecycle with these commands:

| Command | What it does |
|---|---|
| `/codocu:init` | Create `codocu.md` with sensible defaults. Safe to re-run. |
| `/codocu:propose` | Fresh intent → proposal → plan → implement → fold. |
| `/codocu:doc-code` | Docs describe the desired state → plan → implement in code. |
| `/codocu:code-doc` | Code is the truth → update docs (auto for small deltas). |
| `/codocu:apply` | Resume an existing or hand-written plan. |
| `/codocu:fold` | Verify and archive completed plans (alias: `:sync`). |
| `/codocu` | Orient — read signals, show what changed, produce a resolution plan. The nominal entry point when unsure. |

`codocu.md` is free-form natural language: it defines doc locations, fold
behavior, and any project-specific conventions. The agent reads it at the start
of every invocation. It is not itself subject to sync tracking.

## Install & use

There is no marketplace listing yet. Install the plugin in development mode by
pointing Claude Code at this repo:

```
claude --plugin-dir <path to this repo>
```

Then run `/codocu:init` in your project to get started. After pulling new
changes, run `/reload-plugins`.

Do **not** copy the `skills/` folder into a project — see
[CONTRIBUTING.md](CONTRIBUTING.md) for why. Marketplace publishing is planned
(see [docs/todo.md](docs/todo.md)).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and testing.

## Prior art

Codocu builds on established ideas rather than claiming to invent code-centric
documentation: **OpenSpec** (direct workflow ancestor — propose → apply →
archive), **Living Documentation** (Martraire, 2019), **literate programming**
(Codocu draws the inverted lesson — code stands alone, prose supplements), and
**BDD/executable specs** (composable; tests are the machine-verifiable layer).
Codocu's divergence: code is a co-equal source of truth, not a side effect of
specs.

## License

MIT.
