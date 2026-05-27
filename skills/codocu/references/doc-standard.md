# Codocu — Doc Standard

The rules for writing a good doc — auxiliary or internal (see the Dictionary below). Every rule grows from the [principles](principles.md).

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

Out of Codocu scope, but a fair target to mentally place some docs or offer the user as a solution
- **Outside** — External sources, business-oriented documentation engines, public documentation (e.g. API reference). Might be generated from code+technical documentation

Good test: Who's the consumer of this documentation piece and where can they most reliably find it?
- Working agent/coder who needs to know about system quirk/todo/debt should stumble upon relevant info organically while editing code
- Working agent who edits code should find the backlink and update documentation if needed
- Onboarding/Returning coder will look for short summaries at system aux docs, and then for docstrings of code entities 
- Architecture reviewer will look for decisions and future plans in aux docs

Good: "How to create a new submodule" section placed in parent module's docstring or in aux doc dedicated to parent module
Good: Function quirks and usage patterns placed in function docstring
Good: Property explanation placed in its docstring 
Bad: Full class schema presented and explained in aux system doc 
Bad: Property explained in aux system doc
Bad: Design decision related to several functions placed in one of these function's docstrings
 
## 2. Code references in aux docs must be complemented with backlinks in code

Doc that points out at code entities will rot silently — the person changing the code never sees the doc, so they never know to update it. Place one-line backlink in the load-bearing code file pointing back at the doc. The next editor sees it in their working context and remembers the doc exists.

Use one consistent, greppable marker so a single search lists every backlink in the repo. The exact form is a project choice — record it in `codocu.md`. Place the backlink where someone working on this concept is most likely to land — the shared mechanism, the canonical implementation of documented system, the entry module point.

Good: Aux doc related to a global page is referenced in that page's main tsx file
Bad: Aux doc related to a system is not referenced in any of that system's files
Bad: Aux doc about basic conventions is referenced in a ton of files

## 3. Say only what code can't

An auxiliary doc earns its space by carrying what code structurally cannot. Here are some (not exhausting) examples:

- why the subsystem exists, what made it necessary;
- decisions taken and rejected, with reasons (ADRs);
- deliberate non-goals and accepted rough edges, so a reader can tell an
  intentional smell from a bug;
- conventions and agreements no type system enforces;
- in-flight refactors and direction of travel, so a half-migrated repo
  doesn't read as broken;
- the configuration surface — what are editable env vars, flags, constants, the ways the
  system is meant to be tuned and extended.

Note: Explicitly naming code entities outside their source is ok as long as they are truly accessible for someone other than developer. An api route, a user command, an editable config flag. Public surfaces get changed less frequently so they might be sparringly used


## 4. Short summaries are allowed as long as they use business language and do not contain code entity names

A short summary — describes the *meaning* it governs, not the exact symbols underneath it. 
The test:

> If a variable or type here were renamed without changing behavior, would
> this summary still read true?
If no, it's transcribing, not summarizing. Rewrite it to the meaning. 

Summaries of system structure and behaviors are welcomed when they are made on a higher abstraction level. They are not specifications, they bring value of quick onboarding into complex code. Occasional filenames for anchoring references are acceptable; full directory listings are not.

Good: "System objects are stored in a set to drop duplicate ingests." - States the meaning; survives the rename. 
Bad: "System objects list `SystemObjects` is typed as `Set<string>`." Transcribes the code, fragile



