#!/usr/bin/env python3
"""Build daily math PDFs from Markdown with Pandoc and XeLaTeX.

Each source Markdown file must live under artifacts/generated/source/dayNN/
and contain a small YAML front matter block with an output path, for example:

---
title: "День 44. Задания"
output: "artifacts/generated/tasks/den44_zadaniya_Nastyushik.pdf"
---

The script renders formulas natively via XeLaTeX and fails if raw LaTeX markers
survive in the final PDF text layer.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "artifacts" / "generated" / "source"
TEMPLATE = ROOT / "templates" / "day-material.tex"
MANIFEST = ROOT / "data" / "artifacts_manifest.csv"
PREVIEW_ROOT = ROOT / "tmp" / "pdfs" / "rendered_check"
RAW_LATEX_RE = re.compile(
    r"\\\(|\\\)|\\\[|\\\]|\\(?:le|ge|Rightarrow|cdot|circ|ldots)|[A-Za-z]\^[0-9]"
)


@dataclass(frozen=True)
class SourceDoc:
    source: Path
    output: Path


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required tool is missing: {name}")


def parse_front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path}: missing YAML front matter")

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise SystemExit(f"{path}: unsupported front matter line: {line!r}")
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        values[key.strip()] = value
    return values


def source_docs_for_day(day: int) -> list[SourceDoc]:
    day_dir = SOURCE_ROOT / f"day{day}"
    if not day_dir.is_dir():
        raise SystemExit(f"Source directory not found: {day_dir}")
    docs = []
    for source in sorted(day_dir.glob("*.md")):
        metadata = parse_front_matter(source)
        raw_output = metadata.get("output")
        if not raw_output:
            raise SystemExit(f"{source}: front matter must define output")
        output = (ROOT / raw_output).resolve()
        try:
            output.relative_to(ROOT)
        except ValueError as exc:
            raise SystemExit(f"{source}: output must stay inside repo") from exc
        docs.append(SourceDoc(source=source, output=output))
    if not docs:
        raise SystemExit(f"No Markdown sources found in {day_dir}")
    return docs


def build_pdf(doc: SourceDoc) -> None:
    doc.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "pandoc",
        str(doc.source),
        "--standalone",
        "--from",
        "markdown+tex_math_single_backslash+fenced_divs",
        "--template",
        str(TEMPLATE),
        "--pdf-engine=xelatex",
        "--output",
        str(doc.output),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def assert_rendered_formulas(paths: list[Path]) -> None:
    failed = False
    for path in paths:
        text = pdf_text(path)
        match = RAW_LATEX_RE.search(text)
        if match:
            print(
                f"FAIL raw LaTeX marker remains in {path.relative_to(ROOT)}: "
                f"{match.group(0)!r}",
                file=sys.stderr,
            )
            failed = True
        else:
            print(f"OK no raw LaTeX markers: {path.relative_to(ROOT)}")
    if failed:
        raise SystemExit(1)


def assert_pdf_has_pages(paths: list[Path]) -> None:
    for path in paths:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
        if not match or int(match.group(1)) < 1:
            raise SystemExit(f"{path}: PDF has no pages")
        print(f"OK pages={match.group(1)}: {path.relative_to(ROOT)}")


def render_previews(paths: list[Path]) -> None:
    PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    for path in paths:
        prefix = PREVIEW_ROOT / path.stem
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", str(path), str(prefix)],
            cwd=ROOT,
            check=True,
        )
        print(f"Rendered preview: {prefix.name}-*.png")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_category(path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if parts[:3] == ("artifacts", "generated", "tasks"):
        return "generated/tasks"
    if parts[:3] == ("artifacts", "generated", "answers"):
        return "generated/answers"
    if parts[:3] == ("artifacts", "generated", "feedback_child"):
        return "generated/feedback_child"
    if parts[:3] == ("artifacts", "generated", "feedback_parent"):
        return "generated/feedback_parent"
    if parts[:3] == ("artifacts", "generated", "source"):
        return "generated/source"
    return None


def manifest_archive_path(path: Path, category: str) -> str:
    rel = path.relative_to(ROOT)
    if category.startswith("generated/"):
        return rel.relative_to("artifacts").as_posix()
    return rel.as_posix()


def manifest_row(path: Path) -> dict[str, str]:
    category = manifest_category(path)
    if category is None:
        raise SystemExit(f"No manifest category rule for {path}")
    return {
        "category": category,
        "archive_path": manifest_archive_path(path, category),
        "original_path": path.name,
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
    }


def update_manifest(paths: list[Path]) -> None:
    fields = ["category", "archive_path", "original_path", "bytes", "sha256"]
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    updates: dict[str, dict[str, str]] = {}
    for path in paths:
        row = manifest_row(path)
        updates[row["archive_path"]] = row
    seen: set[str] = set()
    next_rows: list[dict[str, str]] = []
    for row in rows:
        archive_path = row["archive_path"]
        if archive_path in updates:
            next_rows.append(updates[archive_path])
            seen.add(archive_path)
        else:
            next_rows.append(row)
    for archive_path in sorted(set(updates) - seen):
        next_rows.append(updates[archive_path])

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(next_rows)
    print(f"Updated manifest: {MANIFEST.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", type=int, required=True, help="day number to build")
    parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="update data/artifacts_manifest.csv for sources and outputs",
    )
    parser.add_argument(
        "--render-preview",
        action="store_true",
        help="render PNG previews to tmp/pdfs/rendered_check for visual QA",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for tool in ["pandoc", "xelatex", "pdftotext", "pdfinfo"]:
        require_tool(tool)
    if args.render_preview:
        require_tool("pdftoppm")

    docs = source_docs_for_day(args.day)
    for doc in docs:
        print(f"Building {doc.output.relative_to(ROOT)} from {doc.source.relative_to(ROOT)}")
        build_pdf(doc)

    outputs = [doc.output for doc in docs]
    assert_pdf_has_pages(outputs)
    assert_rendered_formulas(outputs)

    if args.render_preview:
        render_previews(outputs)

    if args.update_manifest:
        update_manifest([doc.source for doc in docs] + outputs)


if __name__ == "__main__":
    main()
