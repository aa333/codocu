# Access system

Access system governs authentication and authorization — globally and per-chat.

## ADRs

- Owner gets all caps. The owner provider iterates and assigns all possible
  capabilities to the owner; a deliberate decision, with no foreseeable reason
  against it at the time.
- Caps are strings. Json-serializable and easy to parse by human eye, for a
  better client debug experience.
