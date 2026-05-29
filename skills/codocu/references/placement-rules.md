# Placement Rules

> Source: Neph corpus (distilled offline, one-way). Each rule carries one
> illustration marked *do not copy* — placement is taught by reasoning, not
> imitation, so the illustration points at the corpus instead of reproducing it.

Each entry: a rule, one illustration you shouldn't copy, and the reasoning.

### system-doc-opening
Rule: open a system doc by setting scope with the title, then a short
business-domain orientation and the few facts readers reach for most — not a
feature inventory.
Illustration (do not copy) — a one-screen opening, scope then orientation:
```
# Access system
Handles authentication and authorization, globally and per-chat, and grants
capabilities by user id. The full capability list is in `caps.py`.
```
Reasoning: the title already fixes scope. What the reader needs next is
orientation and the handful of facts they'll use often — the things code can't
hand them quickly.
Source: neph access.md §opening

### file-link-with-backlink
Rule: a doc may name a code file when the file is stable, easy to relocate on a
refactor, and carries a backlink to the doc.
Illustration (do not copy): access.md links `caps.py` for the full cap list, and
`caps.py` carries a backlink to access.md.
Reasoning: the backlink puts the doc in front of whoever changes the file, so
the two stay in sync and the reference can't rot in silence.
Source: neph access.md §opening + caps.py module banner

### name-public-surface
Rule: a doc may name a public surface — a route, an endpoint path, a command —
since these are more stable than filenames. Give at least the name so the reader
can reason about it.
Illustration (do not copy): the main-UI guard names the `/api/init` endpoint
when explaining who reaches the interface.
Reasoning: public surfaces change less often than internal symbols and are
addressable, so naming one helps without inviting drift. Don't let it grow into
a full route list — that's generated reference.
Source: neph access.md §"Main UI guard"

### decision-in-system-doc
Rule: a decision belongs in the system doc when it's about this system and reads
as a plain rationale a non-coder could follow — what was chosen, what was turned
down, and why. Use whatever heading the project already uses for these; don't
impose a fixed format.
Illustration (do not copy): the "owner gets all capabilities" decision is
recorded as a plain-language choice about who can do what.
Reasoning: a decision is negative space the code can't hold. Told in plain
terms, it survives refactors and stays readable to the people who need it.
Source: neph access.md §ADRs

### fold-only-system-changing-parts
Rule: when folding a feature plan into a system doc, keep only the parts that
change how *this* system works; route the rest elsewhere.
Illustration (do not copy) — folding a "new capability for module X" plan into
the access doc:
```
keep here:  "a provider can now grant capabilities from hierarchy status"
            (changes how access resolves)
route out:  module X's own UI and usage    → module X's doc
            how to register a new provider  → docstring on the provider base
```
Reasoning: a system doc is about this system. Consumer detail and dev how-tos
belong nearer their own anchors — other systems' docs, or docstrings.
Source: neph access.md §"Known limitations" (scope note)

### single-class-module-title
Rule: for a single-class module, the file or banner title may repeat the class
name or be left off entirely.
Illustration (do not copy): access_service.py carries its usage banner and lets
the `AccessService` class title stand for the module.
Reasoning: with one class, a separate module title just echoes the class name,
and the rule against repetition makes that echo optional.
Source: neph access_service.py §module banner

### dev-usage-near-code-one-place
Rule: a "how to use or extend this" note for developers belongs close to the
code — in the module banner or the class docstring — in exactly one of the two,
never both.
Illustration (do not copy): access_service.py puts the "adding a new
Cap/CapProvider" steps in the file banner, where someone extending the system
will land.
Reasoning: it's orientation the code can't give, it's most useful next to the
code, and duplicating it across banner and docstring guarantees the two drift
apart.
Source: neph access_service.py §module banner

### document-the-negative-space
Rule: state what a component deliberately does *not* do when that absence is a
real, surprising boundary.
Illustration (do not copy): the AccessService docstring notes that removing caps
isn't supported.
Reasoning: a non-goal can't be read off code that simply lacks the feature.
Saying it out loud separates "intentionally absent" from "missing / bug".
Source: neph access_service.py §AccessService docstring

### docstring-by-nuance-not-appearance
Rule: decide a docstring by whether the code carries nuance, not by how simple
it looks. Trivial code needs none; trivial-*looking* code with real nuance or
heavy future use warrants one.
Illustration (do not copy): `AccessService.__init__` gets no docstring;
`BotModule.init` looks trivial but gets one because it has lifecycle nuances and
new modules lean on it.
Reasoning: a docstring on obvious code is noise; withholding one from
deceptively-nuanced code leaves the next author to rediscover the nuance.
Source: neph access_service.py §AccessService.__init__ + bot_module.py
§BotModule.init

## Not yet distilled

- The access.md scope note (what may and may not live in this doc) is partly
  captured by `fold-only-system-changing-parts`. Its other halves — "system
  growth direction is fine here" and "guides to adding caps go in the Python
  files" — reinforce existing rules (negative space, doc-lives-close) and didn't
  get their own entries.
