# Doc rewrite — review checklist

> **Use after the rewrite is drafted, not as a writing recipe.** The principles in `methodology.md` drive how the doc gets written; these checks catch the mechanical things principles trust the writer to remember.
>
> If you find yourself reaching for this file *during* a first draft, stop. The compliance-prose failure mode lives here. Write to principles first; verify with this second.

## The checks

1. **Read** the doc and the code it describes.
2. **Mark** every sentence that fails the test-assertion test (transcribed symbols, signatures, endpoints, field names, enumerated behavior).
3. **Rewrite** each marked sentence: keep the *why / flow / decision*, replace the transcription with a pointer to the code *location*.
4. **Fill the negative space**: confirm the seven kinds of System-doc content are actually present; add what code can't say where it's missing.
5. **Breadcrumb**: place one at the subject's center of gravity (mechanism > exemplar > orientation).
6. **Seed `#METADOCU`** at non-obvious placement decisions. Labels are pointed instance-properties (~15 words), not paraphrased rules.
7. **Elevation pass:** for each block, ask — could this be one tier down? Outside tier? deleted? Default is keep, but only after the question.
8. **Verify (the gate):**
   - No internal-symbol transcription remains.
   - Public-interface names appear in prose, not in enumerations (enumerations belong in Outside tier).
   - The block that documents alternatives is named **ADRs**.
   - The breadcrumb resolves both ways: file → doc and doc → file.
   - The doc reads coherently to someone cold.
   - Nothing that belongs in a docstring is sitting in the system doc.
   - Any contradictions surfaced (not smoothed).
9. **Code gate** (when `src/` was touched): `uv run ruff check src/` + `uv run ruff format src/` both clean.

## When to use

- Post-write self-review by author.
- Post-write review by reviewer.
- Spot-audit of a doc rewritten under an older version of the methodology.

## When NOT to use

- During first draft. Procedure during writing suppresses structural thought. (We learned this the hard way; see `working-brief.md` § Workflow lessons.)
