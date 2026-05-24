# Codocu

**COde-as-a-DOCUmentation** — a Claude Code plugin that keeps a project's
documentation aligned with its code.

**Core bet:** well-written code is already the most detailed spec a project
will ever have. Auxiliary docs (everything outside code) carry what code
structurally can't — why a thing exists, what's coming, the cross-file
picture. They never reword what the code already says.

Codocu is a doc-first quality keeper for that auxiliary layer: it writes new
docs, fixes existing ones, places them where they belong, and verifies their
claims against current code.

## Who it's for

IT-first builders: solo developers, small technical teams, and technical
founders who want to ship maintainable software without drowning in doc
overhead. Codocu operates at the single-project level. Out of scope:
system-of-systems architecture, cross-team API contracts, stakeholder PRDs.

## What it does

Three skills, composed by the agent per the user's ask:

| Skill | Use |
|---|---|
| `/codocu` | The main skill. Writes, reviews, places, and verifies docs against the project's conventions. Use for any doc work — checking quality, updating after code changes, planning a doc-system change, verifying tech-debt records still match reality. |
| `/codocu:fold` | Close out completed plans. Verifies what shipped against code and git history, archives the plan, folds any `docs/inbox/` drafts. |
| `/codocu:init` | Scaffold `codocu.md` (the project's doc conventions file) and wire it into `CLAUDE.md` so every session loads it. Run once per project. |

`codocu.md` is a free-form natural-language file at the project root. It
defines where docs live, how breadcrumbs are written, and any project-specific
conventions. Edit it freely.

## Install & use

Marketplace publishing is planned. For now, install in development mode:

```
claude --plugin-dir <path to this repo>
```

Then in your project:

```
/codocu:init
```

After pulling new changes to this repo, run `/reload-plugins`.

Do **not** copy the `skills/` folder into a project — see
[CONTRIBUTING.md](CONTRIBUTING.md) for why.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and testing.

## Prior art

Codocu builds on established ideas rather than claiming to invent
code-centric documentation: **Living Documentation** (Martraire, 2019),
**literate programming** (Codocu draws the inverted lesson — code stands
alone, prose supplements), and **BDD/executable specs** (composable; tests
are the machine-verifiable layer). Codocu's divergence: code is a co-equal
source of truth, and auxiliary docs are deliberately scoped to what code
can't carry.

## License

MIT.
