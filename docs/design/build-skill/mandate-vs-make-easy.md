# Mandate vs make-easy

Skills sit on a spectrum from *mandate* (numbered steps, structured-question
gates, "always do X before Y") to *make-easy* (a frame and a short list of
conventions, then let the model land it). Both shapes exist for good
reasons. Picking the wrong one costs 3x without making the output 3x better.

## When to mandate

A heavy procedural shape is right when:

- **The procedure is genuinely non-obvious** and the model wouldn't infer it
  from defaults. Specialized domain logic, multi-step state machines with
  hidden invariants, sequenced operations where one step's output is
  another's input in non-obvious ways.
- **Skipping a step has high cost.** Data loss, broken state, irreversible
  action. The skill is acting as a safety harness as much as a guide.
- **Multiple users need consistent output across runs.** A team relying on
  the skill expects step 3's report to always have section X. Procedural
  rigidity buys that consistency.

## When to make-easy

A light shape is right when:

- **The model already does ~80% of the work correctly from defaults.** What
  it misses is a small number of project-specific conventions or
  edge-case judgments.
- **The user's ask varies and a rigid flow would over-fit.** Some
  invocations want the full sweep; others want a partial answer. A
  procedure forces the same shape on both.
- **The cost of ceremony exceeds the cost of occasional miss.** Forcing the
  model through five gates when one prompt would have produced the same
  answer wastes both tokens and user attention.

## The 3x cost test

A skill is failing when invoking it produces output a naked-model run would
have produced for one-third the cost. Run the same prompt both ways
occasionally. If the skill's version isn't materially better — different
conclusions, caught issues the naked run missed, structured outputs the
naked run couldn't replicate — strip ceremony until the difference shows up.

Fold went through two strips in one day on exactly this signal: the first
strip removed a subagent that gave no isolation value; the second removed a
7-step flow whose value was matched by a naked invocation at one-third the
cost.

## Direction of change

Go *toward* light by default. **Make-easy first; mandate only after
make-easy fails repeatedly on the same edge case.** A skill that started
heavy and stripped down catches its over-engineering; a skill that started
light and added rules only when needed catches its under-engineering.

The conversion test going *toward* light:

> What would a naked model do with these conventions loaded?

- *"The right thing"* → cut the procedure entirely; ship just the conventions.
- *"Almost the right thing, missing X"* → keep just X. Don't keep the
  procedure that contained X.
- *"Something subtly wrong"* → keep the procedure, but identify the smallest
  piece that fixed the wrong, and consider whether that piece could live as
  a convention instead.

The conversion test going *toward* heavy:

> Has the same edge case bitten in real use multiple times, and does the
> current convention list fail to catch it?

If yes, escalate to a procedure step. If no, add or refine a convention.
