# Codocu — Principles

Codocu is a COde-and-DOCUmentation system for keeping code and technical documentation aligned.

These principles are the source of truth for what Codocu believes. Operational skills and
agent-facing instructions derive from this file. When a derived rule and a
principle conflict, the principle wins. When two principles conflict, the
order below decides.

## 1. Clarity is the point

A doc is judged by one thing: does its reader come away understanding. Bloated documentation 
is useless even when correct. Accuracy serves understanding; when the two fight, cut for understanding.

## 2. Code is exhaustive about what is; docs cover the negative space

Code is itself documentation, in its most detailed form: an algorithmic set
of instructions that exhaustively describes what the system does. Docs
cover what code can't: business value, rationale, intent, direction, and the changes
planned against current code.


## 3. Code and docs must not repeat themselves 

A doc must never restate what the code already says line-for-line. 
Higher-level summaries that orient the reader are fine; mirror documentation 
that drifts the moment the code moves is not.

Codocu is not compatible with exhaustive behavioral specs (SDD etc). Documents that try to
enumerate every app behavior are precisely the retelling this principle forbids. 
Unsupportable documentation which is prone to drift is useless and will be a burden.



