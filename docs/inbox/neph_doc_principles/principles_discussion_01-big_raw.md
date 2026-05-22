 
❯ /superpowers:brainstorming I'd like to revisit approach to documentation. I   
want to use this repo as a ref, but consider docs here to be in a disarray.     
My general docs approach:                                                       
  - code is a first-class spec, it shows API, it shows behaviors. Its a         
document                                                                        
  - auxillary documentation is required to show what code doesnt reflect -      
system existence motivation, development direction,  intentional hacks and      
workarounds, how to extend and use the system, how to use APIs, as well as a    
short human-oriented summary. Conventions and agreements too.                   
                                                                                
My basic scenarios for auxillary documentation:                                 
  - Get into code made by someone else (AI or coworker) - works only if they    
respect doc principles                                                          
  - Recall how system works after not working with for a while                  
  - Get a new person/agent into context quickly                                 
  - Understand how to extend and modify the system, how to use it, where are    
tuning knobs, what conventions to respect                                       
  - Understand why it's made like it's made, whether hacks and smells are       
intentional and why                                                             
  - Understand how this system is planned to change, especially when long       
intersystem refactoring is ongoing.                                             
                                                                                
Basically all the negative space, invisible from code, should be in auxillary   
docs                                                                            
                                                                                
I should note that I do not want documentation in a form of a full behavioral   
spec, SDD or BDD. Not my cup of tea, requires a lot of back and forth sync      
especially if people work with code directly (I do).                            
One more scenario which is also important and often considered main for docs -  
outside standalone documentation. Wiki, API reference, high-level outline for   
non-programmers, etc. I should underline that I consider it a product of the    
code+local docs. It can be generated and re-generated based on repository       
contents, and can be delegated to CI/CD step.                                   
                                                                                
The main question right now is where and how to store aux docs. 2 main          
candidates are docstrings and set of md files.                                  
- Docstrings and module/file wide comments are nice in-place pieces, no need to 
 cross-reference, easy to keep updated, easy to immediately see. However, not   
every concept can be cleanly landed on some code place                          
- separate md files are good when docs are reasoning about whole flows and      
systems, or about concepts which cannot be landed exactly on specific file. But 
 it's a pain to support: easy to forget when editing relevant systems, you      
cannot and shouldnt have specific code concepts there or docs will be brittle,  
there are no alternatives to concepts of "imports" and "type safety" in those   
to tie them formally to code. Agents also have a hard time to support them      
without adding exact code function names and basically repeating the code.      
                                                                                
What are your thoughts about this?                                              

● I'm using the brainstorming skill to work through this with you. Let me start
  by exploring how documentation is currently set up here, so my thinking is
  grounded in what you actually have rather than abstractions.

  Searched for 4 patterns, read 5 files (ctrl+o to expand)

● This is clearly part of a larger documentation methodology you've been
  developing. Let me check what's already been established in the codocu
  project's memory — I don't want to re-litigate decisions you've already made.

  Read 5 files (ctrl+o to expand)

● I've got the full picture now — and the important context is that this isn't a
   fresh question. You've been building Codocu as a whole methodology (the "code
   is the most detailed spec; docs supplement, never translate" bet,
  clarity-first, the Synced/Desynced/Dirty lifecycle), and Neph is its reference
   fixture. So the docstrings-vs-md question isn't a Neph housekeeping problem —
   it's an unresolved seam in the methodology itself, and Neph's "disarray" is
  the symptom that's surfacing it.

  Let me reflect the tension back the way I see it, because I think there's a
  reframe hiding in your own framing:

  You've set it up as docstrings vs md files, but the real axis isn't the medium
   — it's how far the concept can travel from its code anchor. A function
  contract has exactly one home. "Why this whole subsystem exists" has none. The
   two ends of that gradient want different media; the middle is where it gets
  argued.

  And the maintainability problem you named for md files — drift, forgetting,
  agents parroting code — has one root cause: the reference points the wrong 
  way. A doc that points at code rots silently, because nobody editing the code
  is looking at the doc. Flip it: a one-line breadcrumb in the load-bearing file
   pointing out to the system doc is seen on every edit. That back-reference is
  the "import-like tie" you said md files lack — except its enforcement isn't a
  compiler, it's proximity to the edit. Your access.md is the cautionary case:
  it names EconomyService.grant, exact endpoints, field names — that's the drift
   surface. chat-unions.md mostly names systems and decisions and points at file
   locations — that one will age well. The discipline that falls out: the 
  further a doc sits from code, the less it's allowed to name code.

  That reframe is what I'd build the design around. But before I propose
  approaches, I need to know what you actually want to walk away with — it
  changes the whole shape of this.

● User answered Claude's questions:
  ⎿  · What's the deliverable here — what should exist when we're done? → End 
     goal is to refine approach of codocu (skill/plugin for documentation 
     support). Immediate goal of this session is to figure out methodology 
     approach so I can rewrite docs and leave metacomments around docs to feed 
     to the skill  later (see access.md for example). So a list of things to do 
     and not do, recommendations and next steps

● Your answer sharpens this: the deliverable is a methodology stance — do/don't,
   recommendations, next steps — that you'll then apply by rewriting Neph's docs
   and seeding #METACODOCU markers for the skill to learn from later. So this
  session's product is the rule, with Neph as the worked example, not the reorg
  itself.

  Here are three ways the methodology could go. They differ on one axis: how 
  much you starve the md layer to feed the in-code layer.

  Approach 1 — Anchor-maximalist (starve the md layer).
  Every concept that can land on a symbol or file must live there as a
  docstring/header. docs/systems/ shrinks to only true multi-system narrative.
  Module docstrings carry "what this owns / why this shape."
  - Pro: drift surface minimized — docs move with code, agents update them while
   editing. Purest "code is the spec." Lowest sync burden (your stated allergy).
  - Con: the cross-cutting "why" fragments across dozens of docstrings.
  Onboarding and "recall after months" suffer — there's no single narrative to
  read. In-flight intersystem refactors still have no home.

  Approach 2 — Curated systems layer, disciplined (keep docs/systems/, fix its 
  failure modes).
  One file per system stays. Two hard disciplines bolted on: (a) system docs
  name systems/flows/decisions, never symbols — point at code locations, never
  transcribe; (b) every system doc has a mandatory back-reference breadcrumb in
  its load-bearing file. A small set of cross-cutting docs absorbs conventions
  and in-flight refactors.
  - Pro: preserves the readable bird's-eye view. Back-reference flips the drift
  asymmetry. Evolution of what you already have, not a rewrite.
  - Con: the disciplines are a pile of conventions to remember; needs a
  fold/orientation check to stay honest. The "what counts as a system" boundary
  is judgment each time.

  Approach 3 — Scope-keyed gradient (the synthesis — my recommendation).
  Stop treating it as "in-place vs md." One placement rule keyed to how far the 
  concept travels from its anchor, with a single through-line: a doc may name 
  code in inverse proportion to its distance from that code.
  - Symbol-anchored (contract, invariant, local hack, the knob beside the
  constant) → docstring/inline. May name anything — it moves with the code.
  - Module-anchored (what this module owns, internal layering, why this shape) →
   module/file header. May name things in this module only.
  - No single anchor (cross-module flow, subsystem-existence rationale,
  deliberate non-goals, conventions, in-flight refactor) → docs/systems/<x>.md.
  Names systems and decisions; points at code locations; never transcribes.
  Mandatory back-reference breadcrumb in each load-bearing file.
  - Outside docs (wiki, API ref, non-programmer outline) → generated from the
  above, CI step, never hand-maintained.
  - Pro: one mental model covers all four of your scenarios; the anti-drift rule
   is derived from the gradient, not bolted on; the gradient's violations are
  your "don't" list; it houses the negative-space cases (conventions, refactors)
   that 1 and 2 leave homeless.
  - Con: it's a principle to internalize, not a rote checklist; enforcing the
  back-reference at fold-time is still a next-step to design.

  My recommendation is 3. It's the only one that turns your own reframe into the
   operating rule, and it yields the exact do/don't+next-steps artifact you
  asked for as a consequence of one principle rather than a pile of conventions
  you'll forget the way access.md already drifted. Approach 2 is just 3 with the
   unifying idea left implicit — which is precisely why it'll erode.

  Before I build the design around one of these:

● User answered Claude's questions:
  ⎿  · Which direction should the methodology take? → Approach 3 — scope-keyed 
     gradient (Recommended)

● Approach 3 it is. Let me present the design in pieces and check each before
  moving on. Here's the spine.

  ---
  Section 1 — The principle

  One sentence carries the whole methodology:

  ▎ Documentation lives as close to its anchor as the concept's scope allows, 
  ▎ and may name code in inverse proportion to its distance from that code.

  Two claims folded together. The first — scope decides placement — you already
  half-believe. The second is the load-bearing half, and it's what makes the
  first safe: distance decides naming license.

  A docstring may say raises KeyError when union_id is absent, because if that
  line is renamed or moved, the docstring is renamed or moved in the same edit —
   they can't separate. A system doc may not say that, because nothing forces
  the two to move together. So the system doc says "resolution fails closed when
   a chat isn't in a union" and points at the file. Same fact, different
  vocabulary, because the distance is different.

  The reframe this locks in: drift is not a discipline failure. Drift is naming 
  code from too far away. Every "don't" in your final list will be an instance
  of this one violation.

  ---
  Section 2 — The four tiers

  Tier: Symbol
  Anchor: one symbol / line
  Home: docstring or inline comment
  May name: anything — it moves with the code
  Neph example: the hack comment beside a constant; resolve_scope's contract in
    its own docstring
  ────────────────────────────────────────
  Tier: Module
  Anchor: one module / file
  Home: module.py / __init__.py / file header
  May name: symbols in this module only
  Neph example: "union owns scope resolution; downstream modules register
    ScopeMigrators" → union/module.py header
  ────────────────────────────────────────
  Tier: System
  Anchor: no single anchor — a flow, a subsystem's reason to exist, deliberate
    non-goals, a convention, an in-flight cross-system refactor
  Home: docs/systems/<x>.md
  May name: systems, flows, decisions; code by location, never by transcription
  Neph example: chat-unions.md (good — names the ScopeMigrator concept, points
  at
     scope.py); access.md (cautionary — transcribes EconomyService.grant, exact
    endpoints, field names: that is the  drift surface)
  ────────────────────────────────────────
  Tier: Outside
  Anchor: the whole repo, for non-builders
  Home: generated artifact (wiki / API ref)
  May name: anything — regenerated, so it can't drift
  Neph example: CI step, downstream of the three above; never hand-written

  And the boundary you keep snagging on — "this convention, this in-flight 
  refactor, belongs to no system" — dissolves here. A convention is, by
  definition, a no-single-anchor concept → it's a System-tier doc (a thin one:
  docs/systems/conventions.md, or folded into the system it governs). An
  in-flight intersystem refactor spans many anchors → also System-tier, but one
  expected to be deleted when the refactor lands. Which is precisely what
  docs/plans/ already is. A plan is just a system-tier doc with a death date.
  Your existing structure already encodes the gradient; it just never said so.

  ---
  Does this spine hold for you before I build the anti-drift mechanism and the
  negative-space taxonomy on top of it?

✻ Worked for 4m 19s

※ recap: We're designing a documentation methodology for Codocu: a scope-keyed gradient where docs sit near their anchor and name code less the farther away they are. You approved the principle and four-tier model. Next: I present the anti-drift mechanism and negative-space taxonomy for your review. (disable recaps in /config)

❯ Sounds solid. Nothing really to add here, good summary                        

● (No todo tool here — I'll keep tracking inline.) Continuing.

  ---
  Section 3 — The anti-drift mechanism: the back-reference breadcrumb

  The gradient tells you where a doc goes. It doesn't, by itself, stop a
  System-tier doc from rotting — because the person editing scope.py still has
  no reason to look at chat-unions.md. The mechanism that closes this is one
  move: flip the reference direction.

  A doc that points at code rots silently — nobody editing the code sees the
  doc. So you put a breadcrumb in the code, in the load-bearing file, pointing
  out at the doc:

  # System: docs/systems/chat-unions.md — scope resolution, migrator contract, 
  merge semantics.
  # Editing scope flow here? That doc owns the "why" and the cross-module 
  picture.

  This is the "import-like tie" you said md files structurally lack. It isn't a
  compiler tie — it's something better for this purpose: enforcement by 
  proximity to the edit. The agent or human touching the load-bearing logic sees
   the pointer in their working context and is reminded the negative-space doc
  exists and may need reconciling. No memory, no discipline, no external
  checklist — the reminder is physically in the path of the change.

  Rules that fall out:
  - Every System-tier doc MUST have ≥1 back-reference, placed in its single most
   load-bearing file (the one you can't refactor the system without touching).
  One good breadcrumb beats five weak ones — put it where the edit must land.
  - The breadcrumb names the doc; the doc names the location. Never the reverse.
   The code says "see this doc"; the doc says "this lives around scope.py."
  Neither transcribes the other.
  - A System-tier doc with no possible back-reference is a smell — it usually
  means it's either Outside-tier (generated) or fiction (describes something the
   code doesn't do).
  - Fold/orientation can later check this mechanically: "every docs/systems/*.md
   has ≥1 inbound breadcrumb; every breadcrumb resolves to a real doc." That's
  the one enforced gate — consistent with how Codocu already treats the sync
  marker. (Designing that check is a next-step, not this session.)

  ---
  Section 4 — What a System doc is for (the negative-space taxonomy)

  The gradient says System docs carry "no-single-anchor" knowledge. That's a
  shape, not a content list. Here's the content list — the negative space, the
  stuff genuinely invisible from code:

  1. Why this subsystem exists at all — the motivating pressure. Code shows
  what; it can never show the force that made what necessary.
  2. Roads not taken — the alternative designs weighed and rejected, and why.
  (Your chat-unions.md "Why it's like this" bullets are the gold standard here.)
  3. Deliberate non-goals & accepted sharp edges — "the loser build is dropped,
  we accept this for v1 because…". A reader must be able to tell an intentional
  smell from a bug. This is one of your stated core scenarios and code cannot
  express it.
  4. The flow across modules — the sequence no single file owns (join →
  migrators → atomic → post_commit).
  5. Conventions & agreements — the rules a contributor must respect that no
  type system enforces.
  6. In-flight intersystem refactors — the direction of travel, so a
  mid-refactor repo isn't read as incoherent. (System-tier doc with a death date
   = lives in docs/plans/.)
  7. The tuning-knob map — where the dials are and what moving them costs,
  conceptually. Not the values (those are code); the map.

  And the hard boundary, stated as a non-goal of the methodology itself, because
   you've been explicit about it:

  ▎ A System doc is not a behavioral spec. It does not enumerate inputs/outputs,
  ▎  cases, or step-by-step behavior. That is code's job, and duplicating it is 
  ▎ the SDD/BDD sync tax you're refusing to pay. If a sentence in a System doc 
  ▎ could be a test assertion, it's in the wrong tier — push it down to a 
  ▎ docstring or delete it.

  That single test — "could this sentence be a test assertion?" — is the
  cheapest field-check for the whole gradient. It catches access.md-style
  transcription before it's written.

  ---
  These two sections are the working core — the breadcrumb is the gear, the
  taxonomy is what rides on it. Do they hold before I cover the #METACODOCU role
   and distil the final do/don't + next-steps list?

✻ Sautéed for 41s

※ recap: We're designing Codocu's documentation methodology (the scope-keyed gradient: docs sit near their anchor, name code by distance, back-referenced from code). I've presented Sections 1-4 and you approved 1-2. Next: your call on Sections 3-4, then I cover `#METACODOCU` and the final do/don't list. (disable recaps in /config)

❯ yes, a little remark. Some convention files (e.g. we always work with Grids   
  like this: ... because of ....) can be related to hundreds of files, and it'd 
   be weird to have each one to refer to conventions.md. How would you work     
  around that?                                                                  

● Good catch — that's a real hole in the breadcrumb rule as I stated it. "Tag
  the most load-bearing file" works for a system (there's a scope.py you can't
  refactor around). A convention like "we always build Grids like this,
  because…" is true of a hundred files and load-bearing in none of them. Tagging
   all hundred is absurd — and worse, it's access.md-style drift by repetition:
  a hundred copies of a pointer that all rot together.

  The fix is to restate what the breadcrumb rule actually optimizes. It was
  never "tag every place the concept is true." It's "put the pointer where 
  someone will be standing when they're about to need or violate this."
  Truth-extent ≠ breadcrumb-extent. For a diffuse convention, that locus is one
  of three, in priority order:

  1. The shared mechanism it's embodied in. "We always build Grids like this"
  almost always means there's a Grid component / makeGrid() / a base. The
  breadcrumb goes there — and now the tie is literally the import graph. Every
  one of the hundred files already imports the mechanism; you've got one
  breadcrumb and a hundred consumers bound by real import edges. This is the
  exact structural tie you said md files lack — you don't add it to the files,
  you let the language's own dependency graph carry it.
  2. The canonical exemplar, if there's no shared mechanism. Conventions
  propagate by copy — people write the 101st Grid by copying a Grid that already
   exists. Tag the blessed one ("this is the reference Grid pattern →
  conventions.md#grids"). The "most load-bearing file" for a convention is the
  instance the others imitate.
  3. The orientation layer — CLAUDE.md / the conventions index itself — when
  it's so diffuse it has neither (naming style, error-handling philosophy). The
  reader "getting into the codebase" is reading the orientation layer by 
  definition; that's where the breadcrumb is already satisfied. The convention
  doc doesn't need an inbound pointer from code because its reader never arrives
   via code.

  And the part I like most: "I can't find one place to put this breadcrumb" is a
   design smell, not a doc problem. A convention with no shared mechanism and no
   exemplar is usually a convention that wants to be a mechanism — a helper, a
  base component, a lint rule — so it stops living in prose at all. The
  breadcrumb question doubles as a detector: when placement is hard, the honest
  move is often to dissolve the convention into code that enforces it, and let
  the doc keep only the why. That's the "code is the spec" bet applied
  recursively.

  So Section 3 gains one clause: the breadcrumb attaches to the concept's center
   of gravity — its shared mechanism, else its exemplar, else the orientation 
  layer — never to every instance; and if no center of gravity exists, that's a 
  signal to codify the convention, not to scatter pointers.

  Does that resolve the Grids case the way you'd want it before I move to
  #METACODOCU and the final list?

✻ Cooked for 39s

❯ Not quite, there are still conventions which cannot be easily landed to one   
  place, and neither easily formally linted, but i guess it's going to be very  
  rare occasion, deserving an explicit workaround in project-wide guide doc.    
  Fair points overall, we can work with that. Let's move on                     

● Fair — fold that in: the orientation-layer tier (3) is also the explicit 
  escape hatch. The rare convention that lands nowhere and lints nowhere gets a
  named, deliberate entry in the project-wide guide, flagged as "this is the
  exception, here's why it can't be anchored." Rare by design, called out as
  such, never silent. Moving on.

  ---
  Section 5 — The role of #METACODOCU

  Everything above is doc-about-code. #METACODOCU is the one channel that is
  doc-about-the-doc — and in this methodology it has exactly one job: it's how
  you turn Neph into labelled training data for the skill.

  When you rewrite a Neph doc to the gradient, the placement decision you made
  is invisible in the result — the reader just sees a well-placed sentence. The
  skill can't learn the rule from the outcome alone; it needs the outcome with 
  the reasoning attached at the point it was applied. That's the marker:

  #METACODOCU This block stays System-tier (not pushed to a docstring) because
  the
  flow spans union → migrators → economy and lands on no single file. Note it
  names
  the ScopeMigrator *concept* and points at scope.py — it does not transcribe
  it.

  So the content of a #METACODOCU is never about the system. It narrates which 
  tier was chosen and why, which rule fired, what was deliberately not done.
  It's you, thinking out loud about the gradient, colocated with the example so
  the lesson and the instance can't drift apart (the proximity principle,
  applied recursively to teaching).

  Its lifecycle is the sharp part: #METACODOCU is fixture-only. It lives in Neph
   because Neph is the reference corpus. It is never written in a real
  downstream repo, and it is excluded from the generated Outside tier by
  construction. It's scaffolding for the skill's eyes, stripped before the
  building is shown. Treating it as normal doc content is the one way to misuse
  it.

  ---
  Section 6 — The deliverable: do / don't / next steps

  DO
  - Place by anchor scope: one symbol → docstring; one module → module/file
  header; no single anchor → docs/systems/.
  - Name code in inverse proportion to distance: docstrings may name anything;
  system docs name systems, flows, decisions — and point at locations.
  - Put one back-reference breadcrumb at the concept's center of gravity: shared
   mechanism (import-tie) > canonical exemplar > orientation layer.
  - In system docs write only the negative space: why it exists, roads not
  taken, deliberate non-goals and accepted sharp edges, cross-module flow,
  conventions, in-flight refactors, the tuning-knob map.
  - Run the test before writing any system-doc sentence: "could this be a test 
  assertion?" If yes → push it down a tier or delete it.
  - Treat a plan as a system-tier doc with a death date; treat an in-flight
  refactor the same.
  - When a convention has a clear center of gravity, prefer to codify it into a 
  mechanism or lint and let the doc keep only the why.

  DON'T
  - Don't transcribe code in system docs — symbol names, signatures, endpoints,
  field names, enumerated behavior. (The access.md anti-pattern; it is the drift
   surface.)
  - Don't let a doc point at code without code pointing back.
  - Don't scatter a breadcrumb across every instance of a convention — center of
   gravity, not every site.
  - Don't write behavioral spec / SDD / BDD into a system doc.
  - Don't hand-maintain the Outside tier — generate it, or it becomes a third
  drift surface.
  - Don't leave a system doc with zero inbound breadcrumbs — it's either
  Outside-tier or fiction.
  - Don't write #METACODOCU in anything but the fixture.

  NEXT STEPS (post-session, yours to drive)
  1. Rewrite docs/systems/ to the gradient. access.md is the first surgery:
  strip transcription → locations + why, add a breadcrumb in its load-bearing
  file. chat-unions.md is the reference exemplar — it mostly conforms; add its
  breadcrumb.
  2. Seed #METACODOCU at each placement decision in the rewritten Neph docs —
  the labelled corpus for the skill.
  3. Add the "can't-land / can't-lint convention" escape-hatch section to the
  project-wide guide.
  4. (Later, not now) Design the single enforced gate: every docs/systems/*.md
  has ≥1 resolving inbound breadcrumb; flag system-doc sentences shaped like
  test assertions. Same enforcement philosophy as Codocu's sync marker.
  5. Fold the settled rule into Codocu's references/doc-standard.md.

  ---
  That's the complete methodology. If this holds, I'll write it to a spec doc
  and commit it. One placement question before I do: this is a dated methodology
   artifact destined to fold into Codocu's doc-standard — by your own gradient
  that's a plan with a death date. Shall I write it to
  docs/plans/2026-05-19-doc-gradient-methodology.md (consistent with codocu.md's
   structure), rather than the generic docs/superpowers/specs/ path?

✻ Sautéed for 58s
※ recap: We're designing a documentation methodology for Codocu (the scope-keyed gradient: docs placed by anchor distance, named in inverse proportion to that distance). The full design is approved; next action is writing it to a spec doc, pending your call on whether to save it at docs/plans/2026-05-19-doc-gradient-methodology.md.