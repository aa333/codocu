# Codocu — Doc Standard

How to write a good doc. Every rule comes straight from the
[principles](principles.md).

Two kinds of doc:

- **Auxiliary** — a doc outside the code: a `.md` system doc or a plan.
- **Internal** — a doc inside the code: a docstring or comment.

## 1. Keep a doc close to what it describes

Put a doc as near its subject as the subject's scope allows:

- One symbol or line → its docstring or an inline comment.
- One module → the module or file header.
- A system, flow, or convention with no single home → a system doc under `docs/`.

The test: who reads this, and where would they look for it? Someone editing a
function should meet its quirks in the docstring, right there. Someone new to a
system should find a short overview in its system doc, then drill into
docstrings. Someone reviewing the architecture should find decisions and
direction in the aux docs.

Good: "how to add a submodule" in the parent module's header or its aux doc.
Good: a function's quirks in that function's docstring.
Bad: a full class schema explained in a system doc.
Bad: one property explained in a system doc instead of on the property.

Some docs belong outside Codocu entirely — public API references, business docs.
Fine to point the user there; just don't try to own them here.

## 2. If a doc names code, leave a backlink in the code

A doc that points at a code file rots in silence: whoever changes the file never
sees the doc, so they never update it. Leave a one-line backlink in the code
file pointing back at the doc. The next person to touch that code sees it and
remembers the doc exists.

Use one consistent, greppable marker so a single search lists every backlink.
The exact wording is a project choice — it's recorded in `codocu.md`. Put the
backlink where someone working on this thing will actually land: the main
mechanism, the entry point, the canonical implementation.

Good: a system's aux doc is linked from that system's entry file, which carries
a backlink to the doc.
Bad: a system's aux doc is linked from no code at all.
Bad: a doc about basic conventions is backlinked from dozens of files.

## 3. Say only what code can't

An aux doc earns its space by carrying what code structurally can't. For example:

- why the thing exists and what made it necessary;
- decisions taken and rejected, and the reasons;
- deliberate non-goals and accepted rough edges, so a reader can tell an
  intentional smell from a bug;
- conventions no type system enforces;
- in-flight refactors and where things are headed, so a half-migrated repo
  doesn't read as broken;
- the knobs — env vars, flags, constants, the ways the system is meant to be
  tuned and extended.

Naming a code entity outside its source is fine when the entity is genuinely
public and stable — an API route, a user command, an editable flag. Public
surfaces change rarely, so a sparing reference to one won't rot.

## 4. Plain summaries are fine — if they'd survive a rename

A summary describes what something *means*, not the exact symbols under it. The
test:

> If a variable or type here were renamed, with no change in behavior, would this
> summary still read true?

If no, you're transcribing, not summarizing — rewrite it to the meaning. A
higher-level summary of how a system behaves is welcome; it's what gets someone
oriented fast. An occasional filename as an anchor is fine; a full directory
listing is not.

Good: "Objects are kept in a set so duplicate ingests drop out." — states the
meaning, survives the rename.
Bad: "Objects are stored in `SystemObjects`, typed `Set<string>`." — transcribes
the code, breaks on rename.
