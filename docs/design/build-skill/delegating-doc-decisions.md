# Delegating doc decisions

A skill that ends in "ask `/codocu` what to do with this" needs to be
explicit about *what kinds of input* it's handing over. The word "this" is
where things break — a skill that thinks "this" means one kind of content,
when `/codocu` could legitimately receive another kind, will silently drop
half the work.

## The shipped-work / plan-content split

A plan that ships work and archives carries two distinct kinds of content
that may earn long-term docs. Confusing them produces the wrong fix.

**Shipped work.** The artifacts the plan produced — code files, doc files,
config changes. Whether these earn long-term docs runs through `/codocu`'s
Place primitive (with its doc-warrantedness gate): trivial /
code-explanatory changes don't (rename, small refactor, bug fix the code
already explains); substantive new behavior usually does (new module →
docstring or system doc; new architectural pattern → ADR).

**Plan content.** The reasoning, decisions, and rationale captured inside
the plan itself — ADRs, design constraints, why we chose X over Y, what was
rehomed to where. This is *independent* of what the plan shipped. A plan
that says "we built a 25-line skill because we tested heavier shapes and the
main thread matched them at 1/3 cost" carries an ADR even if the shipped
work was trivial.

Both flow through `/codocu`'s Place primitive. But forgetting either kind
produces a real loss:

- Forget *shipped-work* doc-warrantedness → architectural artifacts ship
  without their orientation docs.
- Forget *plan-content* extraction → ADRs and design rationale get buried in
  the archive, forcing future readers to dig.

A fold operation has to surface both.

## Surface, don't extract

Heavy auto-extraction is the wrong fix. Most plan content doesn't need
elevation — most ADRs are about decisions specific to one plan and don't
generalize; most shipped work is already its own documentation. Auto-running
extraction on every plan produces noise.

Light surfacing is the right fix. The skill names what's load-bearing in the
candidate plans — "plan X carries the why-no-subagent rationale," "plan Y's
shipped work touched the auth module, which has no doc" — and lets the user
flag what to elevate.

This is the [[mandate-vs-make-easy]] rule applied to a delegation boundary:
make it easy to do the right thing (the candidates are named, the placement
hand-off is one prompt away), but don't mandate it.

## Hand-off hygiene

When the skill says "hand this to `/codocu`," it should:

- **Name the kind of input.** "Here's the shipped change set" vs "here's the
  plan's content" vs "here's both, treat them separately." Don't assume
  `/codocu` will infer which is which.
- **Not pre-filter.** The skill doing the delegation typically lacks
  principles and doc-standard. Filtering before handing over is guessing —
  and the guess will sometimes drop something `/codocu` would have kept.
- **Be one-shot when possible.** A delegation that requires three rounds of
  "now look at this, now look at that" is friction. Aggregate first, hand
  off once, return when done.
