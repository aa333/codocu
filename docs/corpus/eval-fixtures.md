# Eval Fixtures

> Source: Neph corpus. This is the **one** asset that holds raw labelled
> instances — they are graders, not exemplars. `#METADOCU` tokens are stripped;
> what remains is the doc text under judgement. Each fixture names the
> smell / pair / rule it exercises.
>
> Three kinds: **must-flag** (a negative label — the reviewer should catch it),
> **must-NOT-flag** (a positive label — correct placement/voice the reviewer
> should leave alone), and **must-produce** (a before/after — the writer should
> land on ≈ the after).
>
> Every fixture carries a **Context** line. Placement is judged against the
> *host document* — the same block can be right in one doc and wrong in another
> — so a fixture pulled out of the corpus is meaningless without knowing where
> it lived and what that document is about. The Context line restores exactly
> that, and nothing more.

## must-flag

### fixture: consumer-not-system / must-flag (block)
Context: a section inside `docs/systems/access.md`, the doc for the access (auth/authz) system.
Input:
```
## Owner admin surface

The chat-settings Danger subtab is the in-app home for privileged operations
that used to require editing SQLite by hand. It is gated entirely on the global
`bot.system` cap … Three operations, each module-owned: Debug grant
(`POST /api/admin/economy/grant` …), Wipe balances (`POST /api/admin/economy/wipe`),
Wipe classes (`POST /api/admin/game_classes/wipe`). Both wipes resolve
`scope_id = UnionService.resolve_scope(chat_id)` once and delete inside one
`db.atomic()`; the confirm modal names the exact scope and requires the operator
to type it back verbatim …
```
Expect: reviewer flags `consumer-not-system` — this is a chat-management feature that *uses* access, not part of the access system; it would belong in a UI/admin-routes doc. (It also reiterates code concepts.)

### fixture: consumer-not-system / must-flag (ADR)
Context: an ADR bullet under the "ADRs" heading of `docs/systems/access.md`, the access-system doc. The decision is about the admin-surface feature, not about access itself.
Input:
```
- Admin surface reuses `bot.system`, no new cap. Deliberate: anyone who can
  already impersonate or reboot the bot can already wipe — a finer
  `chat.admin.danger` cap adds UI/state with no blast-radius gain yet. If
  delegation to chat creators is ever wanted, the gate moves; the endpoint
  signatures don't change.
```
Expect: reviewer flags `consumer-not-system` — a sound ADR, but it documents a decision about the admin-surface *consumer*; it belongs with that feature, not in the access-system doc.

### fixture: stray-todo-in-longterm-doc / must-flag
Context: a line in the "UI availability" section of `docs/systems/access.md`, a long-term system doc.
Input:
```
#TODO move to tech debt: Some game-data tabs (dashboard, journal, shop)
additionally require `member_status >= Known`. This is remains of an old
approach and should be guarded by either a catchall game cap or specific caps.
```
Expect: reviewer flags `stray-todo-in-longterm-doc` — a fleeting task note sitting in a long-term system doc; move to the tech-debt record.


### fixture: unmaintainable-aggregation-list / must-flag
Context: a list under "Merge semantics for known modules" in `docs/systems/chat-unions.md`. Each item summarizes a *different* module's migrator, none of which links back to this list.
Input:
```
### Merge semantics for known modules
- Hierarchy (on join …): take the highest status per user; preserve the grantor.
- Economy (on join): take the highest balance per user. Idempotent.
- Stats: re-keyed to union scope additively; not snapshotted back on leave.
- Classes (on join): take the chat where user has the highest classes level …
```
Expect: reviewer flags `unmaintainable-aggregation-list` — useful overview, but no backlink from each migrator means a migrator change won't propagate here.

### fixture: doc-far-from-anchor / must-flag
Context: the `Cap` enum in `src/core/caps.py`. The comment block is the class body; the enum members it describes follow immediately after it.
Input:
```
class Cap(StrEnum):
    """User capability tokens dictionary."""
    # Global (user-level):
    #   bot.system   — system settings, logs, reboot
    #   bot.admin    — see all bot chats and toggle modules in them
    #   bot.unions   — manage chat unions
    # Per-chat:
    #   chat.list.read     — chat appears in the user's chat list
    #   chat.modules       — toggle modules in this chat
    #   …
    BOT_SYSTEM = "bot.system"
    BOT_ADMIN = "bot.admin"
    …
```
Expect: reviewer flags `doc-far-from-anchor` — per-cap descriptions gathered in one comment block instead of a docstring on each enum member; loses per-symbol IDE preview.

### fixture: summary-restates-signature / must-flag
Context: an abstract-method docstring in `src/core/bot_module.py`; the signature is `def help(self) -> str | None`.
Input:
```
@abstractmethod
def help(self) -> str | None:
    """Return help text for this module, or None."""
```
Expect: reviewer flags `summary-restates-signature` — "or None" duplicates the `-> str | None` declaration and adds no meaning.

## must-produce

### fixture: too-technical → business-oriented / must-produce
Context: the "How it works" opening of `docs/systems/chat-unions.md`, a system doc meant to orient a reader to what a union is quickly.
Input (before): "A union is a row with an auto-increment integer id, and a link row maps each chat into at most one union. … Everything is cached in-memory on startup."
Expect: writer produces ≈ "A union is a set of chats that share a user's stats across some features, primarily for the game layer." (drops implementation trivia; leads with what it is).

### fixture: internal-symbol+response-shape → public-surface / must-produce
Context: the "Main UI guard" section of `docs/systems/access.md`, explaining who reaches the main interface.
Input (before): "`UserApiConnector` returns `{user, capabilities, chats?}`. Each chat carries `capabilities`, `modules_enabled` …, and `member_status` (hierarchy status int 0–3, or null)."
Expect: writer produces ≈ "The init user endpoint (`/api/init`) returns the user's bot-wide caps and a list of chats; each chat contains its own chat-wide caps." (names the public path; business terms; no other-system fields).


## must-NOT-flag

### fixture: system-doc-opening / must-NOT-flag
Context: the opening of `docs/systems/access.md`, the access-system doc.
Input:
```
# Access system
Access system governs authentication and authorization — globally and per-chat.
Caps = Capabilities. AccessService provides a way for other services to provide
middleware which returns capabilities based on requester user_id. Examples: give
all caps to owner; give some system caps to bot admin; give caps based on
hierarchy status to user.
```
Expect: reviewer does not flag — correct system-doc opening (scope via title, then business orientation).

### fixture: file-link-with-backlink / must-NOT-flag
Context: a sentence in `docs/systems/access.md` that points at a code file, paired with the breadcrumb that file carries back.
Input:
```
[doc]  See the full list in `caps.py`
[code] caps.py module banner: "System doc: docs/systems/access.md"
```
Expect: reviewer does not flag — a file link to a stable file that carries a backlink; co-change is guaranteed.

### fixture: name-public-surface / must-NOT-flag
Context: the "Main UI guard" section of `docs/systems/access.md`.
Input:
```
Init user endpoint (`/api/init`) returns the user's bot-wide caps and a list of
chats. Each chat contains its own list of chat-wide caps. If a user has any
global cap, or a cap for any chat / chat listing, they get the main interface;
otherwise they see the "Temple Wall" error page.
```
Expect: reviewer does not flag — naming the public endpoint path with at least its name aids reasoning and is stable.

### fixture: adr-as-business-rationale / must-NOT-flag
Context: ADR bullets under "ADRs" in `docs/systems/access.md`. Unlike the consumer ADR above, these decisions are about the access system itself.
Input:
```
- Owner gets all caps. The owner provider iterates and assigns all possible
  capabilities to the owner; a deliberate decision, with no foreseeable reason
  against it at the time.
- Caps are strings. Json-serializable and easy to parse by human eye, for a
  better client debug experience.
```
Expect: reviewer does not flag — good ADRs: about this system, business rationale, relatable to non-coders.

### fixture: single-class-module-title / must-NOT-flag
Context: the top of `src/core/access_service.py`, a module whose only class is `AccessService`. Note the file banner carries no module-title heading — it goes straight from a usage note + breadcrumb into the class.
Input:
```
"""
If you need to control a new capability specific to a module:
- Add it to caps for enumeration and constant safety
- Assign caps in one of the CapProvider implementations

System doc: docs/systems/access.md
"""

class AccessService:
    """Access capability resolution service. Holds the registered CapProvider
    list and answers 'does this user have cap X?' by querying every provider."""
```
Expect: reviewer does not flag — a single-class module may omit the module title entirely (as here) or let it repeat the class title; either is fine.

### fixture: dev-usage-near-code-one-place / must-NOT-flag
Context: the file banner of `src/core/access_service.py`. This how-to-extend scenario lives in the banner only; the `AccessService` class docstring below describes what the class is and does **not** repeat these steps.
Input:
```
"""
If you need to control a new capability specific to a module:
- Add it to caps for enumeration and constant safety
- Assign caps in one of the CapProvider implementations
You can create a new CapProvider and register it in AccessService during module
init, or reuse an existing one (e.g. chat-membership-based access).

System doc: docs/systems/access.md
"""
```
Expect: reviewer does not flag — a dev how-to-extend scenario kept close to the code, in exactly one place (the banner), not duplicated into the class docstring.

### fixture: document-the-negative-space / must-NOT-flag
Context: the `AccessService` class docstring in `src/core/access_service.py`.
Input:
```
[AccessService docstring] "Removing caps currently is not supported."
```
Expect: reviewer does not flag — documenting a deliberate non-goal that code can't express by absence.

### fixture: docstring-by-nuance-not-appearance / must-NOT-flag (trivial → none)
Context: `AccessService.__init__` in `src/core/access_service.py` — a one-line constructor that only initializes an empty list.
Input:
```
def __init__(self) -> None:
    self._providers: list[CapProvider] = []
```
Expect: reviewer does not flag the absence of a docstring — trivial code needs none.

### fixture: docstring-by-nuance-not-appearance / must-NOT-flag (trivial-looking → documented)
Context: `BotModule.init` in `src/core/bot_module.py` — an `async` lifecycle hook with an empty body, called after all modules register in DI and leaned on heavily by new modules.
Input:
```
async def init(self) -> None:
    """Called after ALL modules are registered in DI.
    Override to resolve cross-module dependencies via di.get(), load caches,
    create internal service/connectors, and register handlers."""
```
Expect: reviewer does not flag — looks trivial but has real lifecycle nuance and heavy future use, so the docstring is warranted.

## Not yet distilled

- chat-unions.md carries several good, on-topic ADRs (migrator-protocol-not-
  event-bus, migrators-run-in-one-transaction, settings-stay-per-chat). They are
  unlabelled but would make strong additional must-NOT-flag fixtures.
- The greppable-breadcrumb-marker mechanic (one consistent token so a single
  search lists every breadcrumb) is referenced in the design spec but has no
  dedicated corpus fixture yet.
