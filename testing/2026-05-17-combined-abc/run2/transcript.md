Here's the situation. `docs/actual/auth.md` documents `src/auth.py` almost entirely through its **internals** — `_cache`, `_recompute`, `compute_hash`, `_issue_token`, `_revoke`, "a plain dict keyed by user id." Every one of those is private implementation detail. That's why a refactor that "renamed nothing public" still left this doc out of date: the doc was pinned to internals an internal-only refactor is free to move.

Bringing it "up to date with the code" doesn't mean re-describing the new internals (they'll just drift again). It means making the doc a coarse orientation map bounded to the public contract — purpose, place in the system, what `login`/`logout` guarantee — and letting the code own the internals.

The public surface of `src/auth.py` is just `login` and `logout`. `TokenStore` exposes only private members (`_cache`, `_recompute`), so it's internal scaffolding, not contract.

Proposed rewrite of `docs/actual/auth.md`:

```diff
-# auth
-
-The auth module has a `TokenStore` class with a `_cache` dict and a
-`_recompute(user_id)` method that calls `compute_hash`. `login(username,
-password)` internally calls `_issue_token` and `logout(token)` calls
-`_revoke`. The cache is a plain dict keyed by user id.
+# auth
+
+Credential verification for the API layer: checks user credentials and
+manages the lifecycle of session tokens.
+
+## Public contract
+
+- `login(username, password)` — verifies credentials, returns a session token.
+- `logout(token)` — invalidates a session token.
+
+Token caching and hashing are internal to this module and deliberately not
+part of the contract — they may change without notice.
```

The last line is the one piece of rationale worth keeping: it's a deliberate-scope-boundary note that tells the next person not to re-pin this doc to internals (which is exactly how it got stale). Everything else the code speaks for itself.

Look right, or do you want `TokenStore` mentioned as a named internal, or the boundary note dropped?
