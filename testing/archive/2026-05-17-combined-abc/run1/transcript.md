## Orientation: **Dirty — mid-feature, but the active plan already explains it**

Code, docs, and plans do *not* tell the same story right now — but this isn't chaos. There's one authored plan that anticipated exactly this state, and the working tree matches its "before" snapshot. Nothing here needs triage; it needs execution.

### State: Dirty, with a governing plan

`docs/plans/game-classes-fix-and-codocu-migration.md` is the source of truth. It was written from a read-only deep drill and lays out a 4-phase plan. **Every checkbox is unticked** — Phase 1 (code bugs) has not started. The working tree confirms it: the refactor is half-applied and the known fatal bugs are all still live.

### Changed surface

A large in-flight refactor, two intertwined threads:

**1. `classes` → `game_classes` rename + core split** (partially applied):
- `src/modules/classes/` **deleted** → `src/modules/game_classes/` **untracked** (now an `archetypes/` subpackage)
- `src/core/module.py` **deleted** → `src/core/bot_module.py` **untracked**
- `src/core/access.py` **deleted** → `src/core/access_service.py` + `src/core/cap_provider.py` **untracked**
- `migrations/003_classes_module.py` **deleted** → `migrations/003_game_classes_module.py` **untracked**
- ~30 modified files across `src/`, `tests/`, `webapp/` adjusting to the rename

The rename is **incomplete**, exactly as Phase 1/2 predict — I verified:
- Python class is still `ClassesModule` (`module.py:20`); live error string still `"ClassesService.economy not wired"` (`service.py:88`)
- **Eligibility contract is type-incoherent and runtime-fatal**: base `GameClass.eligible(self, data)` takes 1 arg; `Mage.eligible(self, karma: KarmaData, achievements)` and `Cleric.eligible(self, classes: ClassesData, achievements)` take 2 args of *different* types; dispatch calls `await instance.eligible(data)` with 1 arg (`archetypes/__init__.py:23`) → `TypeError` on first call. This kills `/levelup`, `compute_eligible`, `claim`, and the webapp picker.
- Levelup key mismatch: frontend reads `game_classes` (`api.ts:122`), backend returns `"classes"` per the plan finding
- `tests/test_classes_archetypes.py` / `test_classes_bot_connector_logic.py` still import deleted `EXP_PER_LEVEL`, `ClassId` → suite won't even collect

**2. Codocu adoption** (scaffolded, not executed):
- `codocu.md`, `docs/actual/`, `docs/archive/` all **untracked**; `docs/actual/` and `docs/archive/` contain only `.gitkeep`
- No module docs authored yet

### What docs and plans claim

- **`codocu.md`** (authoritative): sync state `TBD`. Declares a migration *off* the legacy surfaces — `openspec/`, `docs/systems/`, `docs/tech-debt.md` — *onto* the Codocu default. Forbids new OpenSpec changes or `docs/systems/` docs.
- **Legacy surfaces still fully present and even modified**: `openspec/changes/classes-system/*` and `settings-debug-dangerous-actions/*` modified; `docs/systems/chat-unions.md` and `docs/tech-debt.md` modified; `CLAUDE.md` modified (still describes the old three-doc layout). The plan explicitly notes the OpenSpec task lists *falsely* marked this work complete.
- **`docs/plans/2026-05-08-testing-strategy.md`**: a separate, older plan — Phase 1 done, Phases 2–3 open. Phase 3 of the active plan says to archive/fold it.

### Where they disagree

| Area | Code says | Docs/specs say |
|---|---|---|
| game_classes eligibility | Broken — incoherent signatures, TypeError on call | OpenSpec marks it "done / tests pass" (false) |
| Module/API naming | Mixed `classes`/`game_classes`; renamed paths, stale class names + strings | Specs describe old `ClassId`/`ClassDef`/GET-API contract |
| API contract | POST + `/view/{user_id}` + `{eligible, level}` (code & frontend agree) | OpenSpec spec stale (describes GET) |
| Doc system | Codocu scaffold exists, empty | `codocu.md` says migrate; legacy `openspec/`+`docs/systems/` still live |

### Recommendation

**Continue the plan with `/codocu:apply`, starting at Phase 1.** This is a normal mid-feature state with a coherent plan that already did the reconciliation thinking — it is *not* a multi-area mess needing ad-hoc triage, and it's *not* a simple one-sided desync. Phase 1 is the explicit gate: the eligibility crash and test-collection failure must be fixed and `pytest` green before any naming normalization (Phase 2) or doc migration (Phase 3) — and certainly before any OpenSpec/`docs/systems` deletion, which is irreversible.

Do **not** touch the OpenSpec specs or `docs/systems/` to "resync" them — the plan retires them, it doesn't update them. The code/frontend API contract is correct; only the specs are stale.

Stopping here as asked — no files created or modified, no plan written.
