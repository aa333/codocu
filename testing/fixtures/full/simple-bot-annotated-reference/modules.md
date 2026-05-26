# Modules

The bot is organized as modules — self-contained units that each own one
slice of behavior (the join challenge, presence tracking, `/help`, ops
commands). A module owns its own data, its own business logic, and the
Telegram handlers it registers. The base class is in `src/core/module.py`;
the active modules and their load order live in `MODULE_CLASSES` in
`src/app.py`.

## Lifecycle

Loading happens in two phases. First, every module is instantiated and
registered in the DI container. Then, in a second pass, each module's
`init()` runs.

The two phases exist because modules reach into each other — captcha asks
the chats module whether a user is already known, the help module asks the
module list for everyone's help text. If init ran as part of construction,
the first module to wake up would find nothing else registered yet. By
splitting the phases, every module's `init()` can assume the full registry
is populated.

The price is a global DI container (`src/core/di.py`): a stringly-keyed
lookup by type. We accept it because the alternative — threading every
dependency through constructors in the right order — turns every reorder
of `MODULE_CLASSES` into a refactor.

## Anatomy of a module

Most modules follow the same internal split:

- **`module.py`** — the `Module` subclass. Owns lifecycle, exposes the
  `help()` and `debug()` surfaces, holds references to its service and
  connector.
- **`service.py`** — business logic and in-memory state. Knows nothing
  about Telegram. Unit-testable on its own.
- **`bot_connector.py`** — registers handlers, translates between Telegram
  types and the service. The only layer that imports from `telebot`.
- **`strings.py`** — user-facing strings (Russian).
- **`types.py` / `models.py`** — dataclasses, enums, peewee models.

A module without persistent state skips `models.py`; a module that doesn't
talk to Telegram (none currently, but the shape is open) would skip
`bot_connector.py`.

## Module metadata

The class-level attributes on `Module` carry conventions the type system
can't:

- `name` — the id used in DI lookups and the `/help` picker callback data.
  Stable; treat it as a public-ish surface.
- `str_name` — the label shown in the `/help` menu.
- `is_system` — owner-only modules are hidden from non-owners in `/help`.
- `depends_on` — declarative, **not enforced**. Order is actually set by
  `MODULE_CLASSES` in `app.py`. The tuple documents intent for humans;
  with four modules a real dependency resolver isn't worth the code.
- `models` — peewee model classes. `app.py` flattens these into a single
  `db.create_tables` call at startup.

## The captcha intercept

One thing breaks the "each module owns its handlers" model. While a
captcha challenge is open for a user, `app.py` intercepts that user's
messages before normal routing happens and sends them to
`CaptchaModule.verify_answer` instead. This is the *only* place message
flow is rewritten globally; if message routing ever looks confused, that's
the first place to look.

The intercept lives in `app.py` rather than as a handler-priority trick
because pyTelegramBotAPI runs handlers in registration order with no
notion of priority — short-circuiting in the dispatcher is the cleanest
expression of "this user is mid-challenge, nothing else applies."

## ADRs

### `depends_on` documents, doesn't enforce
With four modules, the load order is obvious from the list in `app.py` and
a human can verify it. A real dependency resolver would carry its own bugs
and add ceremony to every module. If the module count grows past, say, a
dozen, this decision is worth revisiting.

### Telegram bot stays a singleton in DI
The `AsyncTeleBot` is registered as the singleton `AsyncTeleBot` type.
Modules pull it via `di.get(AsyncTeleBot)` to register handlers during
`init()`. We do not pass the bot to constructors because handler
registration is an init-time concern.
