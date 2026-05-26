# Captcha

Challenges new users with simple question. On success shows a little greeting, 
on time out user is kicked and can re-attempt by joining again. 

## Flow
#METADOCU: direct offense: renameable non-public code symbols, cannot be used in aux long term doc 
A `new_chat_members` event arrives at `app.py`, which calls
`CaptchaModule.handle_join`. The connector then asks four questions, in
order, and the first "yes" short-circuits the rest:

1. **Is the new user a bot?** Welcome it, no challenge.
2. **Did someone else add them?** Skip.
3. **Is the user already known in this chat?** Skip. 
4. **Is the join event stale?** If the event is older than
   `CAPTCHA_OUTDATED_TIMEOUT` (45 seconds), the timer can't be enforced
   fairly — the user may already have given up or moved on. Post the
   "outdated" notice and skip.

#METADOCU: direct offense: renameable non-public code symbols, cannot be used in aux long term doc
Otherwise, the connector picks a random question from `strings.QUESTIONS`,
posts it as a reply to the join event, registers an active challenge with
the service, and watches the challenge in a one-second sleep loop until it
ends.

#METADOCU: renameable non-public code symbols in aux longterm doc
While a challenge is open, the global intercept in `app.py` routes that
user's messages to `verify_answer` instead of `ChatsService.touch` — so
their answer never registers as activity, and unrelated messages don't
slip through the gate. See [[modules]] for the intercept's full rationale.

#METADOCU: this is definitely ADR, should be in ADR section; When making a fixture, ensure example has minimal skeleton structure so ADR section exists
#METADOCU: small solution, but inflated text. Gist of this is really small
#METADOCU: also that gist is already documented inline in code, must've been a duplicate. Note that it'd be hard to explain that through fixture mechanic, may need heuristics update
## The kick: ban + unban + a deliberate sleep

A failed or timed-out challenge bans the user, sleeps 1 second, then
unbans with `only_if_banned=True`. The kick = ban + unban dance is so the
user can re-join (a ban without unban is permanent); the sleep is the
non-obvious part.

Telegram's API processes ban and unban as separate writes, and an
immediate unban can race the ban. When it loses, the unban observes "not
banned yet" and silently no-ops because of `only_if_banned`; the ban then
commits and stays. The 1-second gap is large enough to keep this from
happening in practice. If the kick ever stops working — users staying
banned — this is where to look first.

We chose kick-and-unban over restricting permissions because restriction
leaves a half-state in the chat (a member who can't talk) and needs
explicit cleanup. A fresh join is the natural retry.

## Known-user gating
#METADOCU: good one because shows connection between 2 modules, but still not a valid text. Simple example: 'Captcha module remembers users who passed the captcha and posted at least 3 messages in a local cache'
#METADOCU: `The module declares the dependency in depends_on, and
MODULE_CLASSES in app.py orders chats first.` - this is a very detectable code-repetition case. Reviewer didnt catch it at all, it seems.
The `chats` module records membership after a user sends
`MESSAGES_TO_BE_KNOWN` (currently 3) messages in a chat. Captcha skips any
joiner who is already known there, so someone who left and rejoined isn't
re-challenged. This couples captcha to chats: both modules must be loaded
and `chats` must have its cache populated before captcha can answer
correctly. The module declares the dependency in `depends_on`, and
`MODULE_CLASSES` in `app.py` orders `chats` first.


## Abort on leave
#METADOCU: same, if we do a summary, we should do it without using code constants.
#METADOCU: correct example would be "If the user leaves the chat while challenge is open, challenge is aborted and removed". This example is refactor-resistant. Also note if we rewrite file with this level of brevity, the whole summary of module will take just 1-2 paragraphs.   
If the user leaves the chat while their challenge is open, the connector's
`left_chat_member` handler marks the challenge `ABORTED`. The sleep loop
exits on the next tick and cleans up without attempting to ban a user who
is already gone.

## Configuration
#METADOCU: this notion is good, captcha.challenge_time is a public (user-changeable) parameter.
- `captcha.challenge_time` (config.json) — seconds the user has to answer.
  Passed in at module init and bound to each challenge created.
#METADOCU: last refactoring removed this constant, instantly making docs stale. dev skill was used;  
`CAPTCHA_OUTDATED_TIMEOUT` in `types.py` is an in-code constant; tune it
there.

## ADRs
#METADOCU: this was a product of init run. Init run should not be in assumption that it could produce any kind of historical shit up. Unless it fuckin (pardon my language) analyses the git history and changes and past conversations and archived plans, and we neither can nor want that.
### Sleep loop over scheduled task
Each in-flight challenge runs as `await asyncio.sleep(1)` ticking down a
counter. Considered: a scheduler with timeouts. Rejected because the state
is small (a list of active challenges), the bot has no persistence layer
for it, and a restart-cancels-the-challenge semantic is acceptable —
losing a challenge to a restart is no worse than the user retrying their
join.

### Intercept in the dispatcher, not via handler order
While a challenge is open, the dispatcher in `app.py` short-circuits
normal routing for that user. We do this in the dispatcher rather than
relying on handler registration order because the underlying library
(`pyTelegramBotAPI`) has no priority concept — handlers fire in
registration order, first match wins, and that's the wrong shape for "a
challenge overrides everything else." See [[modules]] for the broader
discussion of this crosscut.
