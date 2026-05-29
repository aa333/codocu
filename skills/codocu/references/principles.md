# Codocu — Principles

Codocu keeps code and its documentation in sync. These four beliefs are the
source of everything else here; the skills and reviewers just apply them.

## 1. Code is the most detailed spec

The code already says exactly what the system does, step by step. Nothing
describes behavior more precisely than the code itself.

## 2. Docs cover what code can't

A doc earns its place by holding what you can't read off the code: why the thing
exists, what was decided and rejected, how it's meant to be used, where it's
headed. Code can't tell you any of that.

## 3. Don't repeat what the code already says

If a sentence just restates what the code plainly shows, cut it. Re-told code
drifts the moment the code changes, and a reader gets it faster from the source.
This is why Codocu doesn't do exhaustive behavioral specs — they're all
repetition, and they rot.

## 4. A doc is only worth it if it gets read

Judge a doc by whether it actually helps someone working. A short, clear doc
beats a thorough one nobody opens. Long docs go unread; docs that quote code
symbols rot and cost time to maintain. Keep it short and plain.
