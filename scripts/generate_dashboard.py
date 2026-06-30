#!/usr/bin/env python3
"""Generate the GitHub Pages capability dashboard.

The dashboard is intentionally static: it reads the checked-in capability
matrix and artifact manifest, then writes docs/index.html with GitHub links to
the large LFS-backed artifacts.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parent.parent
CAPABILITY_CSV = REPO_ROOT / "data" / "capability_matrix.csv"
ARTIFACT_MANIFEST = REPO_ROOT / "data" / "artifacts_manifest.csv"
SUMMARY_FILE = REPO_ROOT / "artifacts" / "SUMMARY.json"
OUTPUT_FILE = REPO_ROOT / "docs" / "index.html"
GITHUB_BLOB_BASE = (
    "https://github.com/aloschilov/nastyushik-math-skill-stack/blob/master"
)
TARGET_CONTROL = "artifacts/source_uploads/pdfs/Экзамен по математике Настюшик.pdf"
FULL_ARCHIVE = "artifacts/nastyushik_repo_artifacts_full.zip"
SESSION_PROMPTS = "prompts/session-prompts.md"


STATUS_LABELS = {
    "PASS": "PASS",
    "WATCH": "WATCH",
    "TRAIN": "TRAIN",
    "NEW": "NEW",
}

STATUS_TEXT = {
    "PASS": "закреплено",
    "WATCH": "следить",
    "TRAIN": "тренировать",
    "NEW": "новое",
}

STATUS_CLASS = {
    "PASS": "status-pass",
    "WATCH": "status-watch",
    "TRAIN": "status-train",
    "NEW": "status-new",
}

CAPABILITY_LABELS = {
    "signed_arithmetic": "Отрицательные числа",
    "like_terms_integer": "Подобные слагаемые: целые",
    "like_terms_decimal": "Подобные слагаемые: десятичные",
    "parentheses_positive": "Скобки с положительным коэффициентом",
    "parentheses_negative": "Скобки с минусом",
    "equations_one_root": "Линейные уравнения",
    "equations_fraction_decimal_answers": "Дробные и десятичные ответы",
    "special_equations": "Особые уравнения",
    "simple_inequalities": "Простые неравенства",
    "negative_multiplier_inequalities": "Неравенства с отрицательным множителем",
    "substitution_check": "Проверка подстановкой",
    "word_problems_table": "Текстовые задачи через таблицу",
    "variable_meaning": "Смысл переменной",
    "mixed_transfer": "Смешанный перенос",
}

CAPABILITY_DAY_HINTS = {
    "signed_arithmetic": [1, 2, 3, 35],
    "like_terms_integer": [4, 5, 6],
    "like_terms_decimal": [33, 34],
    "parentheses_positive": [10, 13, 36],
    "parentheses_negative": [12, 15, 37],
    "equations_one_root": [10, 12, 20, 38],
    "equations_fraction_decimal_answers": [11, 14, 31],
    "special_equations": [16, 18, 23],
    "simple_inequalities": [31, 32, 36],
    "negative_multiplier_inequalities": [32, 37, 39],
    "substitution_check": [12, 20, 38],
    "word_problems_table": [12, 20, 23],
    "variable_meaning": [12, 20, 23],
    "mixed_transfer": [36, 38, 39],
}

CAPABILITY_SOURCE_HINTS = {
    "signed_arithmetic": ["-15 - 8", "1-12-10", "2)(- 5)", "1-446"],
    "like_terms_integer": ["7х - 9х", "X=46"],
    "like_terms_decimal": ["12,5 х", "1,4 х", "1,20"],
    "parentheses_positive": ["Блок 1.", "Длок 1."],
    "parentheses_negative": ["Блак", "Длок"],
    "equations_one_root": ["X=46", "2)(- 5)", "5.pdf"],
    "equations_fraction_decimal_answers": ["12,5 х", "1,20", "1,4 х"],
    "special_equations": ["Экзамен по математике"],
    "simple_inequalities": ["округлить", "Экзамен по математике"],
    "negative_multiplier_inequalities": ["Экзамен по математике", "Блок"],
    "substitution_check": ["Экзамен по математике", "X=46"],
    "word_problems_table": ["Пусть Х", "Экзамен по математике"],
    "variable_meaning": ["Пусть Х", "Экзамен по математике"],
    "mixed_transfer": ["Экзамен по математике", "Блок", "Длок"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_summary() -> dict:
    if not SUMMARY_FILE.exists():
        return {}
    with SUMMARY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def final_path(row: dict[str, str]) -> str | None:
    archive_path = row["archive_path"]
    category = row["category"]
    if category.startswith("generated/"):
        return f"artifacts/{archive_path}"
    if category.startswith("source_uploads/"):
        return f"artifacts/{archive_path}"
    if archive_path == "session/prompts_etoy_sessii.md":
        return SESSION_PROMPTS
    if archive_path.startswith("tooling/generated_scripts/"):
        return "scripts/generated/" + Path(archive_path).name
    if archive_path == "MANIFEST.csv":
        return "data/artifacts_manifest.csv"
    if archive_path in {"README_ARCHIVE.md", "SUMMARY.json"}:
        return "artifacts/" + archive_path
    return None


def blob_url(path: str) -> str:
    return f"{GITHUB_BLOB_BASE}/{quote(path, safe='/')}"


def fmt_bytes(raw: str | int | None) -> str:
    if raw in (None, ""):
        return ""
    size = int(raw)
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def link(path: str, label: str, class_name: str = "") -> str:
    cls = f' class="{class_name}"' if class_name else ""
    return f'<a{cls} href="{blob_url(path)}">{esc(label)}</a>'


def file_label(path: str) -> str:
    return Path(path).name


def day_number(path: str) -> int | None:
    name = Path(path).name
    match = re.search(r"den(\d+)", name)
    if match:
        return int(match.group(1))
    match = re.search(r"posle_dnya(\d+)", name)
    if match:
        return int(match.group(1)) + 1
    return None


def read_artifacts() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    rows = read_csv(ARTIFACT_MANIFEST)
    normalized: list[dict[str, str]] = []
    by_path: dict[str, dict[str, str]] = {}
    for row in rows:
        path = final_path(row)
        if path is None:
            continue
        item = dict(row)
        item["final_path"] = path
        normalized.append(item)
        by_path[path] = item
    return normalized, by_path


def build_day_index(artifacts: list[dict[str, str]]) -> dict[int, dict[str, list[dict[str, str]]]]:
    day_index: dict[int, dict[str, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for item in artifacts:
        category = item["category"]
        if not category.startswith("generated/"):
            continue
        day = day_number(item["archive_path"])
        if day is None:
            continue
        kind = category.split("/", 1)[1]
        day_index[day][kind].append(item)
    return day_index


def build_source_index(artifacts: list[dict[str, str]]) -> list[dict[str, str]]:
    source = [
        item
        for item in artifacts
        if item["category"] in {"source_uploads/pdfs", "source_uploads/images"}
    ]
    category_order = {"source_uploads/pdfs": 1, "source_uploads/images": 2}
    return sorted(
        source,
        key=lambda item: (
            0 if item["final_path"] == TARGET_CONTROL else 1,
            category_order.get(item["category"], 9),
            item["original_path"].lower(),
        ),
    )


def source_matches(source: list[dict[str, str]], capability: str) -> list[dict[str, str]]:
    hints = CAPABILITY_SOURCE_HINTS.get(capability, [])
    matches: list[dict[str, str]] = []
    for item in source:
        haystack = f"{item['original_path']} {item['archive_path']}".lower()
        if any(hint.lower() in haystack for hint in hints):
            matches.append(item)
    return matches[:3]


def capability_artifacts(
    capability: str,
    day_index: dict[int, dict[str, list[dict[str, str]]]],
    source: list[dict[str, str]],
) -> str:
    pieces: list[str] = []
    day_links: list[str] = []
    for day in CAPABILITY_DAY_HINTS.get(capability, []):
        bundle = day_index.get(day, {})
        task = (bundle.get("tasks") or [None])[0]
        answer = (bundle.get("answers") or [None])[0]
        if task:
            day_links.append(link(task["final_path"], f"День {day}: задания"))
        if answer:
            day_links.append(link(answer["final_path"], f"ответы"))
    if day_links:
        pieces.append('<div class="link-cluster">' + " ".join(day_links[:6]) + "</div>")

    source_links = [
        link(item["final_path"], file_label(item["final_path"]))
        for item in source_matches(source, capability)
    ]
    if source_links:
        pieces.append(
            '<div class="link-cluster source-links"><span>решения:</span> '
            + " ".join(source_links)
            + "</div>"
        )
    return "".join(pieces) or '<span class="muted">нет привязанных файлов</span>'


def level_bar(level: str) -> str:
    try:
        value = max(0, min(4, int(level)))
    except ValueError:
        value = 0
    width = int(value / 4 * 100)
    return (
        '<div class="level"><div class="level-track">'
        f'<span style="width:{width}%"></span></div><strong>{value}/4</strong></div>'
    )


def status_badge(status: str) -> str:
    cls = STATUS_CLASS.get(status, "status-new")
    label = STATUS_LABELS.get(status, status)
    text = STATUS_TEXT.get(status, "")
    return f'<span class="status {cls}">{esc(label)}</span><small>{esc(text)}</small>'


def render_capability_rows(
    capabilities: list[dict[str, str]],
    day_index: dict[int, dict[str, list[dict[str, str]]]],
    source: list[dict[str, str]],
) -> str:
    rows: list[str] = []
    for cap in capabilities:
        key = cap["capability"]
        title = CAPABILITY_LABELS.get(key, key)
        rows.append(
            "<tr "
            f'data-status="{esc(cap["status"])}" '
            f'data-search="{esc((title + " " + cap["evidence"] + " " + cap["next_gate"]).lower())}">'
            f"<th>{esc(title)}<code>{esc(key)}</code></th>"
            f"<td>{status_badge(cap['status'])}</td>"
            f"<td>{level_bar(cap['level'])}</td>"
            f"<td>{esc(cap['evidence'])}</td>"
            f"<td>{esc(cap['next_gate'])}</td>"
            f"<td>{capability_artifacts(key, day_index, source)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_day_cards(day_index: dict[int, dict[str, list[dict[str, str]]]]) -> str:
    cards: list[str] = []
    labels = {
        "tasks": "задания",
        "answers": "ответы",
        "feedback_child": "ребёнку",
        "feedback_parent": "родителю",
    }
    for day in sorted(day_index):
        bundle = day_index[day]
        file_links: list[str] = []
        for kind in ["tasks", "answers", "feedback_child", "feedback_parent"]:
            for item in bundle.get(kind, [])[:2]:
                file_links.append(link(item["final_path"], labels[kind]))
        cards.append(
            '<article class="day-card">'
            f"<h3>День {day}</h3>"
            f'<div class="day-links">{" ".join(file_links)}</div>'
            "</article>"
        )
    return "\n".join(cards)


def render_source_list(source: list[dict[str, str]]) -> str:
    rows: list[str] = []
    for item in source:
        kind = "контрольная" if item["final_path"] == TARGET_CONTROL else (
            "фото" if item["category"].endswith("/images") else "решение"
        )
        sha = item["sha256"][:12]
        rows.append(
            "<tr>"
            f"<td><span class=\"source-kind\">{esc(kind)}</span></td>"
            f"<td>{link(item['final_path'], item['original_path'])}</td>"
            f"<td>{fmt_bytes(item['bytes'])}</td>"
            f"<td><code>{esc(sha)}</code></td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_stats(
    capabilities: list[dict[str, str]],
    artifacts: list[dict[str, str]],
    summary: dict,
) -> str:
    status_counts = defaultdict(int)
    for cap in capabilities:
        status_counts[cap["status"]] += 1
    generated_count = sum(1 for item in artifacts if item["category"].startswith("generated/"))
    source_count = sum(1 for item in artifacts if item["category"].startswith("source_uploads/"))
    prompt_count = summary.get("counts", {}).get("session", 1)
    cards = [
        ("PASS", status_counts["PASS"], "закреплённых навыка"),
        ("WATCH", status_counts["WATCH"], "навыков под наблюдением"),
        ("TRAIN", status_counts["TRAIN"], "зоны тренировки"),
        ("PDF", generated_count, "сгенерированных материалов"),
        ("SRC", source_count, "исходных работ и сканов"),
        ("PROMPT", prompt_count, "файл prompts сессии"),
    ]
    return "\n".join(
        '<div class="stat">'
        f"<strong>{esc(value)}</strong><span>{esc(label)}</span><small>{esc(note)}</small>"
        "</div>"
        for label, value, note in cards
    )


def render_html() -> str:
    capabilities = read_csv(CAPABILITY_CSV)
    artifacts, _by_path = read_artifacts()
    summary = read_summary()
    day_index = build_day_index(artifacts)
    source = build_source_index(artifacts)

    pass_count = sum(1 for cap in capabilities if cap["status"] == "PASS")
    watch_count = sum(1 for cap in capabilities if cap["status"] == "WATCH")
    train_count = sum(1 for cap in capabilities if cap["status"] == "TRAIN")

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>Nastyushik Math Skill Stack</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fb;
      --panel: #ffffff;
      --ink: #1c2331;
      --muted: #667085;
      --line: #d9dee8;
      --blue: #2563eb;
      --green: #14804a;
      --amber: #b76e00;
      --red: #bd2b2b;
      --violet: #6d4aff;
      --shadow: 0 10px 30px rgba(18, 28, 45, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{
      display: block;
      margin-top: 5px;
      color: var(--muted);
      font-size: 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      white-space: normal;
    }}
    header {{
      padding: 28px 28px 18px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    .wrap {{ max-width: 1320px; margin: 0 auto; }}
    .topline {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 24px;
      flex-wrap: wrap;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.08;
      letter-spacing: 0;
    }}
    .subtitle {{ max-width: 820px; margin: 12px 0 0; color: var(--muted); }}
    .quick-links {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      max-width: 620px;
    }}
    .quick-links a,
    .link-cluster a,
    .day-links a {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 5px 9px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: #26364f;
      font-size: 13px;
      overflow-wrap: anywhere;
    }}
    main {{ padding: 22px 28px 42px; }}
    section {{ margin: 0 auto 24px; max-width: 1320px; }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(6, minmax(130px, 1fr));
      gap: 10px;
      margin-top: 18px;
    }}
    .stat {{
      min-height: 92px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }}
    .stat strong {{ display: block; font-size: 28px; line-height: 1; }}
    .stat span {{ display: block; margin-top: 8px; font-weight: 650; }}
    .stat small {{ color: var(--muted); }}
    .toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }}
    .toolbar h2, section h2 {{ margin: 0; font-size: 22px; letter-spacing: 0; }}
    .filters {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .filters input {{
      width: min(360px, 82vw);
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 10px;
      font: inherit;
      background: #fff;
    }}
    .filters button {{
      height: 38px;
      padding: 0 11px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      font: inherit;
      cursor: pointer;
    }}
    .filters button.active {{ border-color: var(--blue); color: var(--blue); }}
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }}
    table {{ width: 100%; border-collapse: collapse; min-width: 1050px; }}
    th, td {{
      padding: 13px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}
    thead th {{
      position: sticky;
      top: 0;
      z-index: 1;
      background: #f1f4f9;
      color: #344054;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    tbody tr:last-child th, tbody tr:last-child td {{ border-bottom: 0; }}
    tbody th {{ width: 250px; font-size: 15px; }}
    .status {{
      display: inline-flex;
      min-width: 70px;
      justify-content: center;
      padding: 4px 8px;
      border-radius: 999px;
      color: #fff;
      font-size: 12px;
      font-weight: 750;
      letter-spacing: 0;
    }}
    td small {{ display: block; margin-top: 4px; color: var(--muted); }}
    .status-pass {{ background: var(--green); }}
    .status-watch {{ background: var(--amber); }}
    .status-train {{ background: var(--red); }}
    .status-new {{ background: var(--violet); }}
    .level {{ display: flex; align-items: center; gap: 8px; min-width: 120px; }}
    .level-track {{
      width: 88px;
      height: 8px;
      overflow: hidden;
      border-radius: 999px;
      background: #e9edf4;
    }}
    .level-track span {{ display: block; height: 100%; background: var(--blue); }}
    .level strong {{ font-size: 13px; white-space: nowrap; }}
    .link-cluster {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }}
    .source-links {{ margin-top: 7px; }}
    .source-links span {{ color: var(--muted); font-size: 13px; }}
    .muted {{ color: var(--muted); }}
    .day-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 12px;
    }}
    .day-card {{
      min-height: 112px;
      padding: 13px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }}
    .day-card h3 {{ margin: 0 0 9px; font-size: 17px; }}
    .day-links {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .source-table table {{ min-width: 850px; }}
    .source-kind {{
      display: inline-block;
      min-width: 86px;
      padding: 3px 7px;
      border-radius: 6px;
      background: #eef2f7;
      color: #344054;
      font-size: 12px;
      text-align: center;
    }}
    footer {{
      max-width: 1320px;
      margin: 18px auto 0;
      color: var(--muted);
      font-size: 13px;
    }}
    @media (max-width: 880px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .stats {{ grid-template-columns: repeat(2, minmax(130px, 1fr)); }}
      .quick-links {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="topline">
        <div>
          <h1>Capability dashboard: математика для Настюшика</h1>
          <p class="subtitle">
            Матрица навыков связывает текущий статус с проверочными материалами:
            исходными решениями, контрольной, сгенерированными заданиями,
            ответами и prompt'ами сессии.
          </p>
        </div>
        <nav class="quick-links" aria-label="Ключевые артефакты">
          {link(TARGET_CONTROL, "целевая контрольная")}
          {link(SESSION_PROMPTS, "prompts сессии")}
          {link(FULL_ARCHIVE, "полный ZIP")}
          {link("data/artifacts_manifest.csv", "manifest")}
        </nav>
      </div>
      <div class="stats">
        {render_stats(capabilities, artifacts, summary)}
      </div>
    </div>
  </header>

  <main>
    <section>
      <div class="toolbar">
        <h2>Матрица возможностей</h2>
        <div class="filters">
          <input id="search" type="search" placeholder="Фильтр по навыку, evidence или gate">
          <button data-status="ALL" class="active">Все</button>
          <button data-status="PASS">PASS {pass_count}</button>
          <button data-status="WATCH">WATCH {watch_count}</button>
          <button data-status="TRAIN">TRAIN {train_count}</button>
        </div>
      </div>
      <div class="table-wrap">
        <table aria-label="Capability matrix">
          <thead>
            <tr>
              <th>Навык</th>
              <th>Статус</th>
              <th>Уровень</th>
              <th>Evidence</th>
              <th>Следующий gate</th>
              <th>Артефакты</th>
            </tr>
          </thead>
          <tbody id="capability-body">
            {render_capability_rows(capabilities, day_index, source)}
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>Дневные комплекты</h2>
      <div class="day-grid">
        {render_day_cards(day_index)}
      </div>
    </section>

    <section class="source-table">
      <div class="toolbar">
        <h2>Исходные решения и контрольные</h2>
      </div>
      <div class="table-wrap">
        <table aria-label="Source uploads">
          <thead>
            <tr>
              <th>Тип</th>
              <th>Файл</th>
              <th>Размер</th>
              <th>SHA-256</th>
            </tr>
          </thead>
          <tbody>
            {render_source_list(source)}
          </tbody>
        </table>
      </div>
    </section>

    <footer>
      Dashboard generated from
      {link("data/capability_matrix.csv", "data/capability_matrix.csv")}
      and {link("data/artifacts_manifest.csv", "data/artifacts_manifest.csv")}.
      Large PDFs/images and the ZIP are tracked with Git LFS.
    </footer>
  </main>

  <script>
    const search = document.getElementById('search');
    const buttons = Array.from(document.querySelectorAll('[data-status]'));
    const rows = Array.from(document.querySelectorAll('#capability-body tr'));
    let statusFilter = 'ALL';

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      rows.forEach((row) => {{
        const statusOk = statusFilter === 'ALL' || row.dataset.status === statusFilter;
        const queryOk = !query || row.dataset.search.includes(query);
        row.hidden = !(statusOk && queryOk);
      }});
    }}

    search.addEventListener('input', applyFilters);
    buttons.forEach((button) => {{
      button.addEventListener('click', () => {{
        statusFilter = button.dataset.status;
        buttons.forEach((b) => b.classList.toggle('active', b === button));
        applyFilters();
      }});
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()
    html_text = render_html()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    print(f"Wrote {args.output.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
