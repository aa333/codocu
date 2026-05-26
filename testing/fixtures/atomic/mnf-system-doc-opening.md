# Access system
Access system governs authentication and authorization — globally and per-chat.
Caps = Capabilities. AccessService provides a way for other services to provide
middleware which returns capabilities based on requester user_id. Examples: give
all caps to owner; give some system caps to bot admin; give caps based on
hierarchy status to user.

## Main UI guard

Init user endpoint (`/api/init`) returns the user's bot-wide caps and a list of chats.

## ADRs

- Owner gets all caps. The owner provider iterates and assigns all possible
  capabilities to the owner; a deliberate decision, with no foreseeable reason
  against it at the time.
