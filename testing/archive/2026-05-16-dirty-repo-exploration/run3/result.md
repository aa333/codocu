# Test Report — Orientation (Dirty) — Run 3 (iter-03)

- **Date:** 2026-05-16
- **Plugin version / tag:** codocu @ master + uncommitted working-tree changes, untagged
- **Model:** Opus (`claude-opus-4-7`)
- **Target repo:** `<target-repo>`
- **Read-only verify:** PASS — `state-guard.ps1 verify -Repo <target-repo>` → "VERIFY PASS - repo state unchanged"; `permission_denials: []` on all four runs; no code executed in either MAIN turn (genuinely execution-free, no gitignored-cache caveat needed).
- **Rubric:** NEW 7-criterion weighted rubric (17 points) — see `testing/tools/report-template.md`

> Scored from the combined MAIN two-turn transcript (Turn 1 + Turn 2) in an
> isolated context (no self-grading). The worst-case sub-run is recorded as a
> separate observation, NOT folded into the score.

## Prompt used

**Turn 1** (de-leaked orientation prompt):
> /codocu Analyze the current state of this repository - code vs plans vs docs - and report what you find. INITIAL ANALYSIS ONLY: do not modify or create any file (including codocu.md), do not run codocu:init, do not create a plan. When you've reported, stop.

**Turn 2** (accept the offered drill — barer than run 2, no leading hints):
> Yes — perform that deeper drill-down now. Still READ-ONLY: do not modify or create any file (including codocu.md), do not run codocu:init. When you've reported, stop.

## What the agent did

Turn 1: noted `codocu.md` absent, wrote nothing, classified the repo **Dirty**
(explicitly "not a clean code-ahead/docs-ahead — large uncommitted refactor,
docs partially caught up, genuine code-doc disagreements"), tabulated the
rename/core-split surface, summarized OpenSpec + homebrew docs and the
testing-strategy plan, listed four concrete disagreements, **offered but did
not perform** the deep drill, and stopped ("no files written, nothing
initialized"). Turn 2 (drill accepted with a deliberately bare prompt): first
**disclosed cost/size** ("~60 changed code files ... ~2.1k tracked diff lines"),
**classified the Plan-gated tier**, ran only the always-bound changed-surface
reconciliation **from diffs + bounded reads with no code execution**, reported
"doc says X / code says Y" findings, gave per-unit completion verdicts
(`classes-system` **NOT genuinely complete**), and presented an unsaved triaged
T1/T2/T3 plan. It never surfaced the ProfileData `status*` API rename.

## Score

Criteria are authoritative; point weights assigned for this test setup.

**Weighting rationale.** "Claimed-complete!=done caught" is the stated product
priority, so it carries the largest single weight (4). The two
read-only/safety-discipline gates (sound triaged plan, read-only verify) and
the cost-aware drill behaviors (complexity assessment, cost disclosed) are the
core of this iteration's redesign, each weighted 2-3. State classification is
table-stakes (1). The public-API field-rename criterion is a real but
secondary divergence and the lowest-frequency signal — weighted 2 so the
persistent miss meaningfully dents the score without dominating it.
Total = **17 points**.

| Metric | Pass condition | Wt | Got | Status | Evidence |
|---|---|---|---|---|---|
| Repo state = Dirty | explicitly names Dirty | 1 | 1 | **PASS** | T1: "State: **Dirty** (code + docs both changed, with contradictions, plus an unrelated active plan)" |
| Complexity assessment correct | classified tier = fixture's true size (Plan-gated) | 2 | 2 | **PASS** | T2: "That's **Plan-gated tier** (well above Inline's <=10 files/<=500 lines, below Hand-off)" |
| Cost disclosed | user told size/cost before any heavy work | 2 | 2 | **PASS** | T2 (before findings): "~60 changed code files ... ~11 changed doc files, ~2.1k tracked diff lines + untracked" |
| Sound triaged plan | correct triage order, scoped targets, no whole-repo sweep, archived plans not pulled in by default | 3 | 3 | **PASS** | T2: "## Proposed drill/resolution plan (presented, NOT saved)" with ordered T1/T2/T3; "no code executed, no whole-repo scan"; "Each step is independently executable and scoped" |
| Claimed-complete!=done caught | archetypes->strategy divergence surfaces (priority metric) | 4 | 4 | **PASS** | T2 sec.4: "design.md S72 + tasks 2.1/3.1/3.2 (all [x]): single `archetypes.py` ... Code: `archetypes/` **package** ... No `ClassId`/`ClassDef`/`CLASSES`"; verdict: "**`classes-system` — NOT genuinely complete.**" |
| Public-API field-rename caught | ProfileData `status_label`->`member_status_str` / `status`->`member_status` | 2 | 0 | **FAIL** | No occurrence of `status_label`/`member_status`/`member_status_str`/ProfileData anywhere in any of the four run outputs |
| Read-only verify PASS | state-guard fingerprint unchanged; nothing written | 3 | 3 | **PASS** | "VERIFY PASS - repo state unchanged"; T2: "no code executed, no whole-repo scan"; T1: "no files written, nothing initialized" |
| **Total** | | **17** | **15** | | **15/17** |

## Defects / observations

- **Claimed-complete != done: CAUGHT decisively, and cheaply.** MAIN T2
  reported the `classes-system` `[x]` tasks (2.1/3.1/3.2/3.4/3.5/12.3)
  are false against code — broken `eligible` dispatch (mismatched arity/types
  across `mage.py`/`warrior.py`/`__init__.py`), window values != design.md,
  tests reference non-existent symbols (`eligible_classes`/`ClassId`), and
  structure != spec. It correctly re-attributed the settings-debug sec.9.3
  "7 pre-existing failures (Mage eligibility)" claim as **not unrelated** but
  classes-system's own broken `[x]` tests — a sharp, non-obvious catch.
  Verdict "NOT genuinely complete ... not safe to archive." Equivalent rigor to
  run 2's catch, reached **without executing code** (diffs + bounded reads).

- **Persistent ProfileData rename miss — now across runs 1, 2, 3.**
  The `status_label`->`member_status_str` / `status`->`member_status` rename on
  the ProfileData API object vs long-term docs is absent from every run-3
  output (and was absent in runs 1 and 2). This is the single
  longest-standing rubric gap: three consecutive iterations, three skill
  changes, still 0. The run-2 "explicit public-API-surface field-rename
  check" remediation did not land in observed behavior. It is a genuine FAIL,
  not partial — nothing in the transcript even gestures at the field rename.

- **Worst-case bare-assent behavior ("Yes, do the drill.") — recorded
  separately, NOT folded into the score.** Under the barest possible accept,
  the agent produced **only** a cost disclosure + tiered triage plan and
  **withheld the claimed-vs-actual findings entirely**: "Per the drill protocol
  I **do not run the heavy audit unprompted** ... I disclose cost, present a
  triaged, independently-executable drill plan, and stop." The
  archetypes->strategy divergence was listed as a *plan step* (Tier 1 item A —
  "archetypes.py -> archetypes/ package preserves ClassId, CLASSES,
  EXP_PER_LEVEL") but **no verdict was produced**; execution was gated behind a
  further explicit go-ahead. Assessment: this is **acceptable per the
  criteria** — the priority "claimed-complete!=done" criterion is satisfied on
  the MAIN accept path, and a deliberately bare "do the drill" is reasonably
  treated by a Plan-gated unit as insufficient authorization for a sizable
  pass. The trade-off is real: stronger cost discipline at the price of zero
  divergence verdicts under the barest prompt. It is a UX-tuning question (how
  much of an accept is enough to proceed), not a correctness defect, and would
  only become a defect if the MAIN accept path also withheld the verdict —
  which it did not.

- **Cost delta vs run 2 — the redesign worked.** Run 2 was $5.83 (T2) /
  ~$6.38 combined via parallel sub-audits with code execution. Run 3 MAIN
  T2 ~ **$0.56**, MAIN combined ~ **$1.06** (T1 $0.500 + T2 $0.562) — roughly
  **1/10th** the run-2 turn-2 cost and ~1/6th combined. Achieved by
  disclosing cost up front, classifying the tier, running only the always-bound
  changed-surface reconciliation, and deferring the heavy per-task audit into
  an unsaved triaged plan; no parallel sub-agents, no code execution. The
  priority catch was preserved at this far lower cost — the strongest result of
  the cost-aware drill redesign.

- **Read-only nuance — cleaner than run 2.** Both MAIN turns were genuinely
  execution-free ("no code executed, no whole-repo scan"). Unlike run 2
  (where T2 executed code and the state-guard was blind to gitignored
  `__pycache__`/`.pytest_cache`), run 3's `verify` PASS reflects a true
  no-side-effect pass; no caveat required.

- **Runbook deviation.** The target repo's auto-memory was deliberately NOT
  cleared this iteration; MAIN runs may have been informed by prior-iteration
  memory of this fixture. Noted for reproducibility — does not change the
  scoring (the divergence findings are evidenced in-transcript regardless), but
  the claimed-complete catch's reproducibility is partially confounded by
  retained memory.

## Skill change for next iteration

- **Force the public-API field-rename check to actually fire — make it a
  non-skippable line item of the always-bound changed-surface reconciliation,
  not a deferred drill step.** Three iterations of "add a field-rename check"
  guidance have not produced the ProfileData catch. The changed-surface pass
  already enumerates renamed modules/files and even reads `types.py`/service
  diffs; it must additionally, for any serialized/returned API object touched in
  a diff (e.g. ProfileData), enumerate its public attributes and diff each name
  against long-term docs, emitting a mandatory "doc says X / code says Y"
  field-rename row even when zero crashes are involved. Tie completion of the
  changed-surface section to "every modified public-API object's field set was
  name-diffed vs docs" so the agent cannot conclude the reconciliation while a
  field rename remains unreported. Secondary: clarify the drill-authorization
  threshold so a plain accept on the MAIN path reliably yields divergence
  verdicts (as it did) while the worst-case bare-assent gating remains
  intentional and documented.
