# Voice Pairs

> Source: Neph corpus (distilled offline, one-way). These are the one place a
> *before* is kept on purpose: voice is taught by contrast, so each pair shows
> the labelled prior version and the version that replaced it.

Literal before/after few-shot for tone and wording. The lesson is in the
rewrite, not in any rule — read them as examples to imitate, not signatures to
match.

### too-technical → business-oriented
Before: "A union is a row with an auto-increment integer id, and a link row maps each chat into at most one union. … Everything is cached in-memory on startup."
After:  "A union is a set of chats that share a user's stats across some features, primarily for the game layer."
Note: drop implementation trivia (auto-increment ids, link rows, in-memory cache) and lead with what the thing is *for* the reader.
Source: neph chat-unions.md §"How it works" (labelled prior version) + §opening (the offered definition)

### internal-symbol + response-shape → public-surface + business-terms
Before: "`UserApiConnector` returns `{user, capabilities, chats?}`. Each chat carries `capabilities`, `modules_enabled` (toggleable modules whose `is_enabled` is true), and `member_status` (hierarchy status int 0–3, or `null` …)."
After:  "The init user endpoint (`/api/init`) returns the user's bot-wide capabilities and a list of chats. Each chat contains its own list of chat-wide capabilities."
Note: name the stable public path, not the connector class; describe in business terms; don't reach into other systems' fields (module toggles, hierarchy status int).
Source: neph access.md §"Main UI guard"

### implies-wrongness → well-known concept (heading)
Before: "## Why it's like this"
After:  "## ADRs"
Note: "Why it's like this" implies the decisions were mistakes; "ADRs" is a known concept that carries the meaning neutrally.
Source: neph access.md §ADRs

## Not yet distilled

- `code-structure → business meaning`: "Aggregation hub for capability resolution"
  → "Access capability resolution service". Demoted from an active pair — the
  after is only marginally less mechanical than the before, so it doesn't teach
  the business-words move cleanly. Keep until the corpus offers a sharper rewrite.
- The current chat-unions "How it works" prose ("Most modules store data in a
  `user_id+chat_id` key…") is the accepted version but still leans technical — a
  candidate for a future business-oriented pair if the corpus grows a cleaner
  exemplar.
