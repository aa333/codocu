# Access system

The access system governs authentication and authorization, globally and per-chat, as well as granting capabilities based on user id.

## UI availability

The main UI is gated by the init endpoint's cap check. Some game-data tabs (dashboard, journal, shop) are visible only when caps allow.

#TODO move to tech debt: Some game-data tabs (dashboard, journal, shop)
additionally require `member_status >= Known`. This is remains of an old
approach and should be guarded by either a catchall game cap or specific caps.
