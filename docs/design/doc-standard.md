# Codocu — Doc Standard

The rules for writing a good doc — auxiliary or internal (see the Dictionary
below). Every rule grows from a single principle: [code is exhaustive about
what is; docs cover the negative space](principles.md). Read this before
writing or judging any doc.

## Dictionary

- **Auxiliary** — docs outside code files (`.md` system docs, plans).
- **Internal** — docs inside code files (docstrings, comments).
- **Long-term** — docs that outlive feature work and survive small refactors.
  System docs, module docstrings.
- **Short-term** — docs that are only valid during a feature development
  session. Once the work lands, their content is absorbed into long-term
  docs and the short-term file is deleted.
- **Delta** — a proposed change to the code. Usually short-term, but can
  persist as a TODO or tech-debt record.
- **ADR** — Architecture Decision Record. A note of why a decision was made,
  including the alternatives considered.

## 1. A doc lives close to what it describes

Put a doc as near to its subject as the subject's scope allows. Four homes,
by scope:

- **Symbol** — one symbol or line → its docstring or an inline comment.
- **Module** — one module → the module or file header.
- **System** — a subsystem, flow, or convention with no single anchor → a
  system doc under `docs/`.
- **Outside** — the whole repo, for outside readers → a generated artifact
  (API reference, command index), never hand-written. Hand-written reference
  drifts the moment the code moves.

### Breadcrumbs

A doc that points out at code rots silently — the person changing the code
never sees the doc, so they never know to update it. Flip the arrow: leave
a one-line breadcrumb in the load-bearing code file pointing back at the
doc. The next editor sees it in their working context and remembers the doc
exists.

Use one consistent, greppable marker so a single search lists every breadcrumb
in the repo. The exact form is a project choice — record it in `codocu.md`.

Place the breadcrumb where someone working on this concept is most likely
to land — the shared mechanism, the canonical implementation, the entry
point. A handful of breadcrumbs across genuinely related files reinforces
the link and is fine. A breadcrumb in *every* file that touches a convention
is a smell: that convention wants to become a mechanism or a lint rule, and
the doc should then reference that mechanism, carrying only the *why*.

## 2. Say only what code can't

An auxiliary doc earns its space by carrying what code structurally cannot.
The kinds of content that qualify. Here are some (not exhausting) examples:

- why the subsystem exists — the force that made it necessary;
- decisions taken and rejected, with reasons (ADRs);
- deliberate non-goals and accepted rough edges, so a reader can tell an
  intentional smell from a bug;
- cross-module flow no single file owns;
- conventions and agreements no type system enforces;
- in-flight refactors and direction of travel, so a half-migrated repo
  doesn't read as broken;
- the configuration surface — env vars, flags, constants, the ways the
  system is meant to be tuned and extended.

The field test, run before every sentence:

> Could this sentence be a test assertion?

If yes, it describes behavior — the code's job. Push it down to a docstring
or delete it. An aux doc is not a behavioral spec; enumerating inputs,
outputs, and cases is work the code already does, in more detail, without
drifting.

### Naming public surfaces is fine

A doc may name a public surface in a sentence — a route, a command, a flag
— when it makes a point about why or how. It may not turn into a list of
all the routes or all the commands. That's reference material, and
reference material belongs in the Outside home, generated.

## 3. Name code only when it won't drift out from under the doc

The rule is co-change:

> Name a specific code symbol only if it changes *together* with the doc,
> or a breadcrumb guarantees the doc is in front of whoever changes that
> symbol.

That single test settles the cases:

- An ADR sitting in `docs/` *may* name specific code, even though it's far
  from that code — because the decision is about that code, and the
  breadcrumb keeps them in sync.
- A business summary *may* refuse to name code even when it sits right next
  to it — being close doesn't oblige it to transcribe. The stable business
  word reads better and survives refactors (rule 5).

## 4. Summaries describe meaning, not symbols

A short summary — a docstring especially — describes the *meaning* it
governs, not the exact symbols underneath it. The test:

> If a variable or type here were renamed without changing behavior, would
> this summary still read true?

If no, it's transcribing, not summarizing. Rewrite it to the meaning.

- Not: "System objects list is `Set<string>`." Transcribes the type;
  drifts the moment someone refactors it.
- Better: "System objects are stored in a set to drop duplicate ingests."
  States the meaning; survives the rename.

Short summaries are wanted, not discouraged. Code is hard to read without
them. The rule is not "write fewer" — it's "write them at the level of
meaning."

## 5. Prefer business words over code words

When the same thing can be named in business terms or in code terms, use
the business term. It reads better for the next person, and it survives
refactors — the business concept outlives whatever implementation
currently serves it.