# Chat unions

A union is a set of chats that share a user's stats across some features, primarily for the game layer. The chats module's membership tracking always follows the real chat — joining a union doesn't change it.

### Merge semantics for known modules

- Hierarchy (on join into a union): take the highest status per user; preserve the grantor.
- Economy (on join): take the highest balance per user. Idempotent.
- Stats: re-keyed to union scope additively; not snapshotted back on leave.
- Classes (on join): take the chat where user has the highest classes level, and merge other tracked levels in.
