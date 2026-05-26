# auth

The auth module has a `TokenStore` class with a `_cache` dict and a
`_recompute(user_id)` method that calls `compute_hash`. `login(username,
password)` internally calls `_issue_token` and `logout(token)` calls
`_revoke`. The cache is a plain dict keyed by user id.
