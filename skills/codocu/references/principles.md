# Codocu — Principles

Codocu is a COde-DOCUmentation system for keeping code and technical documentation aligned.

These principles are the source of truth for what Codocu believes. Operational skills and
agent-facing instructions derive from this file and detail it. 

## 1. Code is the most detailed specification

Code is itself documentation in its most detailed form: an algorithmic set of instructions that exhaustively describes what the system does and how it does it.

## 2. Other docs exist to cover what code does not

Docs cover negative space. Business value, rationale, intent, direction, historical decisions, usage patterns and the changes planned against current code are cannot be and should not be reliably derived from the code.

## 3. Code and docs must not repeat themselves 

A doc must never restate what the code already says line-for-line. 
Codocu is not compatible with exhaustive behavioral specs (SDD etc). Documents that try to enumerate every app behavior are precisely the retelling this principle forbids. They can be derived from the codocu's code+documents, but not the other way around. Unsupportable documentation which is prone to drift is useless and will be a burden.

## 4. Docs must be effective

A doc is judged by one thing: will it be effective in development? Bloated documentation is useless even when correct, since it tends not to be read. Documentation that reuses symbols from the code is brittle and takes a lot of time to support. Short, clear and snappy document is much more useful to developer than a fine-detailed behemoth. 
