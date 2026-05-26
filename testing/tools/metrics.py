"""metrics.py — per-doc + aggregated metrics for an eval cell.

Usage:
    py testing/tools/metrics.py \\
        --fixture testing/fixtures/full/simple-bot-annotated \\
        --working testing/runs/002-base-vs-skill-inplace/pass-1/simple-bot-annotated/T0/working \\
        [--out metrics.json]

Compares `--working` against `--fixture` and reports both surfaces of doc
output: new aux `.md` files written under working/ and inline doc-line
additions to code files.

Per aux .md (new under working/, did not exist in fixture):
    word_count, sentence_count, avg_sentence_length,
    code_block_count, code_block_lines.

Per code file (working has a counterpart in fixture):
    fixture_doc_words, working_doc_words, inline_doc_words_added,
    code_touched (any non-doc line differs).

Aggregated:
    total_aux_words (sum across new .md files — 1:1 comparable to 001's
        total_words for back-diff against pass-1)
    total_inline_words (sum of inline_doc_words_added across code files)
    total_doc_words (aux + inline)
    home_split (inline / total — the routing signal 001 couldn't see)
    code_touched_any (boolean — flags any non-doc code edits)
    fixture_module_count, words_per_module (total_doc_words / module_count)

Identifier-mention density is parked — see TD-eval-identifier-counts in
docs/todo.md. Reviving needs real Python and TypeScript ASTs.

Doc-line classification is heuristic. Python: lines inside triple-quoted
strings or starting with `#`. TS/JS: lines inside `/* */` blocks or
starting with `//`. Imperfect at edge cases (triple-quoted data strings,
`//` inside string literals) but adequate for the fixtures in this suite.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")
WORD_SPLIT = re.compile(r"\b\w+\b")
CODE_FENCE = re.compile(r"^```", re.MULTILINE)

CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
TS_FAMILY = {".ts", ".tsx", ".js", ".jsx"}


@dataclass
class DocMetrics:
    path: str
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    code_block_count: int
    code_block_lines: int


@dataclass
class CodeFileMetrics:
    path: str
    fixture_doc_words: int
    working_doc_words: int
    inline_doc_words_added: int
    code_touched: bool


@dataclass
class CellMetrics:
    fixture: str
    working_dir: str
    fixture_module_count: int
    aux_docs: list[DocMetrics]
    code_files: list[CodeFileMetrics]
    total_aux_words: int
    total_inline_words: int
    total_doc_words: int
    home_split: float
    code_touched_any: bool
    words_per_module: float


def count_fixture_code_files(fixture_root: Path) -> int:
    """Count non-trivial code files under fixture_root.

    Counts files with extensions in CODE_EXTENSIONS. Skips empty `__init__.py`
    so an idiomatic Python package layout doesn't inflate the denominator.
    """
    count = 0
    for path in fixture_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in CODE_EXTENSIONS:
            continue
        if path.name == "__init__.py":
            try:
                if not path.read_text(encoding="utf-8").strip():
                    continue
            except OSError:
                continue
        count += 1
    return count


def _classify_python_lines(text: str) -> list[bool]:
    """Mark each line True if it is a doc line (inside triple-quotes or `#` comment)."""
    lines = text.splitlines()
    result: list[bool] = []
    in_triple = False
    triple_kind: str | None = None
    for line in lines:
        if in_triple:
            result.append(True)
            if triple_kind and triple_kind in line:
                in_triple = False
                triple_kind = None
            continue
        # Find earliest triple-quote on this line.
        kind_at: tuple[str, int] | None = None
        for k in ('"""', "'''"):
            i = line.find(k)
            if i != -1 and (kind_at is None or i < kind_at[1]):
                kind_at = (k, i)
        if kind_at:
            k, idx = kind_at
            rest = line[idx + 3:]
            if k in rest:
                result.append(True)  # opens and closes on the same line
            else:
                in_triple = True
                triple_kind = k
                result.append(True)
            continue
        result.append(line.lstrip().startswith("#"))
    return result


def _classify_ts_lines(text: str) -> list[bool]:
    """Mark each line True if it is a doc line (inside `/* */` or `//` comment)."""
    lines = text.splitlines()
    result: list[bool] = []
    in_block = False
    for line in lines:
        if in_block:
            result.append(True)
            if "*/" in line:
                in_block = False
            continue
        i = line.find("/*")
        if i != -1:
            rest = line[i + 2:]
            if "*/" in rest:
                result.append(True)
            else:
                in_block = True
                result.append(True)
            continue
        result.append(line.lstrip().startswith("//"))
    return result


def _classify_lines(text: str, ext: str) -> list[bool]:
    if ext == ".py":
        return _classify_python_lines(text)
    if ext in TS_FAMILY:
        return _classify_ts_lines(text)
    return [False] * len(text.splitlines())


def doc_words_in_text(text: str, ext: str) -> int:
    classes = _classify_lines(text, ext)
    lines = text.splitlines()
    return sum(len(WORD_SPLIT.findall(line)) for line, is_doc in zip(lines, classes) if is_doc)


def code_only_text(text: str, ext: str) -> str:
    classes = _classify_lines(text, ext)
    lines = text.splitlines()
    return "\n".join(line.rstrip() for line, is_doc in zip(lines, classes) if not is_doc)


def score_doc(doc_path: Path) -> DocMetrics:
    text = doc_path.read_text(encoding="utf-8")

    fences = [m.start() for m in CODE_FENCE.finditer(text)]
    code_block_count = len(fences) // 2
    code_block_lines = 0
    prose_parts: list[str] = []
    if fences:
        i = 0
        last_end = 0
        while i + 1 < len(fences):
            start = fences[i]
            end = fences[i + 1]
            prose_parts.append(text[last_end:start])
            block = text[start:end]
            code_block_lines += block.count("\n") - 1
            last_end = end + len("```")
            i += 2
        prose_parts.append(text[last_end:])
        prose = "".join(prose_parts)
    else:
        prose = text

    words = WORD_SPLIT.findall(prose)
    word_count = len(words)
    sentences = [s for s in SENT_SPLIT.split(prose) if s.strip()]
    sentence_count = len(sentences)
    avg_sent_len = (word_count / sentence_count) if sentence_count else 0.0

    return DocMetrics(
        path=str(doc_path),
        word_count=word_count,
        sentence_count=sentence_count,
        avg_sentence_length=round(avg_sent_len, 2),
        code_block_count=code_block_count,
        code_block_lines=code_block_lines,
    )


def compare_code_file(fixture_path: Path, working_path: Path) -> CodeFileMetrics | None:
    ext = working_path.suffix
    if ext not in CODE_EXTENSIONS:
        return None
    try:
        working_text = working_path.read_text(encoding="utf-8")
    except OSError:
        return None
    fixture_text = ""
    if fixture_path.exists():
        try:
            fixture_text = fixture_path.read_text(encoding="utf-8")
        except OSError:
            fixture_text = ""

    fixture_doc_words = doc_words_in_text(fixture_text, ext) if fixture_text else 0
    working_doc_words = doc_words_in_text(working_text, ext)
    added = max(0, working_doc_words - fixture_doc_words)

    fixture_code = code_only_text(fixture_text, ext) if fixture_text else ""
    working_code = code_only_text(working_text, ext)
    touched = fixture_code != working_code

    return CodeFileMetrics(
        path=str(working_path),
        fixture_doc_words=fixture_doc_words,
        working_doc_words=working_doc_words,
        inline_doc_words_added=added,
        code_touched=touched,
    )


def find_new_md_files(fixture_root: Path, working_root: Path) -> list[Path]:
    """Return .md files under working/ that don't have a counterpart in fixture/."""
    new_files: list[Path] = []
    for md in working_root.rglob("*.md"):
        rel = md.relative_to(working_root)
        if not (fixture_root / rel).exists():
            new_files.append(md)
    return new_files


def iter_code_pairs(fixture_root: Path, working_root: Path) -> Iterable[tuple[Path, Path]]:
    for wf in working_root.rglob("*"):
        if not wf.is_file():
            continue
        if wf.suffix not in CODE_EXTENSIONS:
            continue
        rel = wf.relative_to(working_root)
        yield fixture_root / rel, wf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", required=True, help="Path to frozen fixture root")
    ap.add_argument("--working", required=True, help="Path to <cell>/working/ — the post-agent copy")
    ap.add_argument("--out", help="Optional output JSON path. Default: stdout.")
    args = ap.parse_args()

    fixture_root = Path(args.fixture).resolve()
    working_root = Path(args.working).resolve()

    if not fixture_root.is_dir():
        raise SystemExit(f"fixture not found: {fixture_root}")
    if not working_root.is_dir():
        raise SystemExit(f"working not found: {working_root}")

    module_count = count_fixture_code_files(fixture_root)

    aux_docs = [score_doc(p) for p in sorted(find_new_md_files(fixture_root, working_root))]
    code_metrics: list[CodeFileMetrics] = []
    for ff, wf in iter_code_pairs(fixture_root, working_root):
        m = compare_code_file(ff, wf)
        if m is not None:
            code_metrics.append(m)

    total_aux = sum(d.word_count for d in aux_docs)
    total_inline = sum(c.inline_doc_words_added for c in code_metrics)
    total = total_aux + total_inline
    home_split = (total_inline / total) if total else 0.0
    touched_any = any(c.code_touched for c in code_metrics)
    words_per_module = (total / module_count) if module_count else 0.0

    cell = CellMetrics(
        fixture=str(fixture_root),
        working_dir=str(working_root),
        fixture_module_count=module_count,
        aux_docs=aux_docs,
        code_files=code_metrics,
        total_aux_words=total_aux,
        total_inline_words=total_inline,
        total_doc_words=total,
        home_split=round(home_split, 4),
        code_touched_any=touched_any,
        words_per_module=round(words_per_module, 2),
    )

    out = json.dumps(asdict(cell), indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
