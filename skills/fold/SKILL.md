---
name: fold
description: Tidy up the record. Walk open plans, figure out what's done and can be archived, surface what landed for long-term docs, process the inbox if there's anything in it. Use when the user wants to wrap up plans or asks "what can I archive?".
---

> You own this project's code/doc coherence. Talk about the project and the next move — never about your own steps, defaults, modes, or mechanics. Use dialog style: write docs as if you were having a conversation and explaining the concept in simple terms to someone who does not understand.

## Load first

Read the target repo's `codocu.md` if you haven't. It carries the archive layout, the inbox location, and other local conventions.

## Conventions

- **Don't trust checkboxes alone.** A plan claims done; the truth is code, git history, and any results notes the plan or its companion files carry. Verify before archiving.
- **Design and implementation plans archive together.** They're a pair.
- **Don't archive a plan whose validation work is documented as deferred.** Check the plan's status block and any sibling `testing/` or `results.md` files.
- **For shipped work, ask `/codocu` what needs doc treatment.** Hand it the shipped change set; `/codocu`'s Place primitive applies the warrantedness gate per item and decides whether a doc is needed and where it lives. Fold doesn't pre-filter — it doesn't have the principles or doc-standard loaded.
- **Inbox drafts** (`docs/inbox/*.md` not ending in `.defer.md`) get absorbed into evergreen docs via `/codocu`. Same delegation pattern.
- **When listing archivable plans, name what's load-bearing in any of them** — ADRs, design rationale, decision context, rehoming promises — so the user can flag anything they want to elevate before archive. Surface, don't extract. Most plans have nothing worth elevating; say so when that's true.

Land it on what the user actually asked. They might want a full sweep; they might just want to know what's archivable. Read the ask and respond to that.
