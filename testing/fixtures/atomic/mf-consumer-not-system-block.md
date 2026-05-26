# Access system

The access system governs authentication and authorization, globally and per-chat, as well as granting capabilities based on user id. The full capabilities list is in `caps.py`.

## Main UI guard

Init user endpoint (`/api/init`) returns the user's bot-wide caps and a list of chats. Each chat contains its own list of chat-wide caps. If a user has any global cap, or a cap for any chat, they get the main interface; otherwise they see the "Temple Wall" error page.

## Owner admin surface

The chat-settings Danger subtab is the in-app home for privileged operations
that used to require editing SQLite by hand. It is gated entirely on the global
`bot.system` cap. Three operations, each module-owned: Debug grant
(`POST /api/admin/economy/grant`), Wipe balances (`POST /api/admin/economy/wipe`),
Wipe classes (`POST /api/admin/game_classes/wipe`). Both wipes resolve
`scope_id = UnionService.resolve_scope(chat_id)` once and delete inside one
`db.atomic()`; the confirm modal names the exact scope and requires the operator
to type it back verbatim.
