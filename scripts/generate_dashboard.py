#!/usr/bin/env python3
"""Generate the GitHub Pages capability dashboard.

The dashboard is intentionally static: it reads the checked-in subject
capability matrices and artifact manifest, then writes docs/index.html with
GitHub links to the large LFS-backed artifacts.
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
CAPABILITY_MATRICES = {
    "algebra": REPO_ROOT / "data" / "capability_matrices" / "algebra.csv",
    "geometry": REPO_ROOT / "data" / "capability_matrices" / "geometry.csv",
    "probability_statistics": (
        REPO_ROOT
        / "data"
        / "capability_matrices"
        / "probability_statistics.csv"
    ),
}
ARTIFACT_MANIFEST = REPO_ROOT / "data" / "artifacts_manifest.csv"
CURRICULUM_PATH = REPO_ROOT / "data" / "curriculum" / "advanced_grade7.csv"
SUMMARY_FILE = REPO_ROOT / "artifacts" / "SUMMARY.json"
OUTPUT_FILE = REPO_ROOT / "docs" / "index.html"
GITHUB_BLOB_BASE = (
    "https://github.com/aloschilov/nastyushik-math-skill-stack/blob/master"
)
TARGET_CONTROL = "artifacts/source_uploads/pdfs/Экзамен по математике Настюшик.pdf"
FULL_ARCHIVE = "artifacts/nastyushik_repo_artifacts_full.zip"
SESSION_PROMPTS = "prompts/session-prompts.md"
ADVANCED_PROGRAM = "asserts/FRP_matematika_7-9_uglublennyi_uroven_2025.pdf"
GRADE7_TARGET_CONTROLS = [
    ("asserts/Algebra_demoversii_7_klass.pdf", "Алгебра, 7 класс"),
    ("asserts/Geometriya_demoversii_7_klass.pdf", "Геометрия, 7 класс"),
    (
        "asserts/Teoriya_veroyatnosti_i_statistika_demoversii_7_klass.pdf",
        "Вероятность и статистика, 7 класс",
    ),
]

DOMAIN_LABELS = {
    "algebra": "Алгебра",
    "geometry": "Геометрия",
    "probability_statistics": "Вероятность и статистика",
}

DOMAIN_DESCRIPTIONS = {
    "algebra": "Углублённый маршрут: функции, тождества, многочлены, делимость и системы.",
    "geometry": "Углублённый маршрут: доказательства, треугольники, окружность и построения.",
    "probability_statistics": "Углублённый маршрут: данные, изменчивость, графы, логика и вероятность.",
}


STATUS_LABELS = {
    "PASS": "Закреплено",
    "WATCH": "Наблюдаем",
    "TRAIN": "Тренируем",
    "NEW": "Новое",
}

STATUS_CLASS = {
    "PASS": "status-pass",
    "WATCH": "status-watch",
    "TRAIN": "status-train",
    "NEW": "status-new",
}

CAPABILITY_LABELS = {
    "signed_arithmetic": "Отрицательные числа",
    "rational_number_line_module": "Рациональные числа, прямая и модуль",
    "ratios_proportions_percent": "Отношения, пропорции и проценты",
    "like_terms_integer": "Подобные слагаемые: целые",
    "like_terms_decimal": "Подобные слагаемые: десятичные",
    "parentheses_positive": "Скобки с положительным коэффициентом",
    "parentheses_negative": "Скобки с минусом",
    "factor_common_monomial": "Вынесение общего множителя",
    "binomial_multiplication": "Умножение двучленов",
    "powers_monomials": "Степени и одночлены",
    "polynomial_structure_operations": "Структура и операции с многочленами",
    "square_of_sum": "Квадрат суммы",
    "identity_proof": "Доказательство тождеств",
    "reasoning_generalization": "Обобщение и доказательство",
    "factorization_special_products": "Разложение и формулы сокращённого умножения",
    "coordinate_intervals_distance": "Промежутки и расстояние на прямой",
    "function_concept_graph_analysis": "Понятие функции и чтение графиков",
    "linear_function_abs_piecewise": "Линейная функция, модуль и кусочные графики",
    "divisibility_primes_criteria": "Делимость, простые числа и признаки",
    "gcd_lcm_euclid": "НОД, НОК и алгоритм Евклида",
    "remainders_arithmetic": "Деление и арифметика остатков",
    "absolute_value_equations": "Линейные уравнения с модулем",
    "linear_systems": "Системы линейных уравнений",
    "geometry_basic_objects": "Точка, прямая, отрезок и луч",
    "geometry_axiomatic_language": "Определение, аксиома, теорема и доказательство",
    "geometry_angle_measurement": "Измерение углов",
    "geometry_adjacent_vertical_angles": "Смежные и вертикальные углы",
    "geometry_polygons_symmetry": "Ломаные, многоугольники и симметрия",
    "geometry_triangle_elements": "Элементы треугольника",
    "geometry_congruence_isosceles": "Равенство треугольников и равнобедренный треугольник",
    "geometry_parallel_lines": "Параллельные прямые",
    "geometry_polygon_angle_sums": "Суммы внутренних и внешних углов",
    "geometry_right_triangles": "Прямоугольные треугольники",
    "geometry_triangle_inequalities": "Геометрические неравенства",
    "geometry_circle_tangents": "Окружность, хорды и касательные",
    "geometry_loci": "Геометрические места точек",
    "geometry_compass_straightedge": "Построения циркулем и линейкой",
    "data_tables_diagrams": "Таблицы и диаграммы",
    "statistical_measures": "Среднее, медиана и размах",
    "advanced_statistical_measures": "Квартили и среднее гармоническое",
    "random_variability_grouping": "Случайная изменчивость и группировка",
    "random_experiment_outcomes": "Случайный эксперимент и исходы",
    "relative_frequency": "Абсолютная и относительная частота",
    "classical_probability": "Классическая вероятность",
    "graph_models": "Графы и пути",
    "graph_path_enumeration": "Перебор путей в ориентированном графе",
    "logic_statements": "Высказывания и доказательство от противного",
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
    "rational_number_line_module": [],
    "ratios_proportions_percent": [],
    "like_terms_integer": [4, 5, 6, 59, 60],
    "like_terms_decimal": [33, 34],
    "parentheses_positive": [10, 13, 36],
    "parentheses_negative": [12, 15, 37],
    "factor_common_monomial": [54, 55, 56, 57, 58],
    "binomial_multiplication": [58, 59, 60, 61, 62, 63, 64],
    "powers_monomials": [40, 41, 42],
    "polynomial_structure_operations": [58, 59, 60, 61],
    "square_of_sum": [62, 63, 64, 65, 66],
    "identity_proof": [62, 63, 64, 65, 66],
    "reasoning_generalization": [64, 65, 66],
    "factorization_special_products": [54, 55, 62, 63, 64, 65, 66],
    "coordinate_intervals_distance": [],
    "function_concept_graph_analysis": [],
    "linear_function_abs_piecewise": [],
    "divisibility_primes_criteria": [],
    "gcd_lcm_euclid": [],
    "remainders_arithmetic": [],
    "absolute_value_equations": [],
    "linear_systems": [],
    "geometry_basic_objects": [40, 41],
    "geometry_axiomatic_language": [65, 66],
    "geometry_angle_measurement": [46, 47, 48, 49, 50],
    "geometry_adjacent_vertical_angles": [46, 47, 48, 49, 50, 60, 61, 64, 65, 66],
    "geometry_polygons_symmetry": [],
    "geometry_triangle_elements": [],
    "geometry_congruence_isosceles": [],
    "geometry_parallel_lines": [],
    "geometry_polygon_angle_sums": [],
    "geometry_right_triangles": [],
    "geometry_triangle_inequalities": [],
    "geometry_circle_tangents": [],
    "geometry_loci": [],
    "geometry_compass_straightedge": [],
    "data_tables_diagrams": [],
    "statistical_measures": [],
    "advanced_statistical_measures": [],
    "random_variability_grouping": [],
    "random_experiment_outcomes": [],
    "relative_frequency": [],
    "classical_probability": [],
    "graph_models": [],
    "graph_path_enumeration": [],
    "logic_statements": [],
    "equations_one_root": [10, 12, 20, 38],
    "equations_fraction_decimal_answers": [11, 14, 31],
    "special_equations": [16, 18, 23],
    "simple_inequalities": [31, 32, 36, 56, 57, 58],
    "negative_multiplier_inequalities": [32, 37, 39, 56, 57, 58],
    "substitution_check": [12, 20, 38],
    "word_problems_table": [12, 20, 23],
    "variable_meaning": [12, 20, 23, 60, 61],
    "mixed_transfer": [36, 38, 39, 56, 57, 58],
}

CAPABILITY_SOURCE_HINTS = {
    "signed_arithmetic": ["-15 - 8", "1-12-10", "2)(- 5)", "1-446"],
    "rational_number_line_module": [],
    "ratios_proportions_percent": [],
    "like_terms_integer": ["7х - 9х", "X=46"],
    "like_terms_decimal": ["12,5 х", "1,4 х", "1,20"],
    "parentheses_positive": ["Блок 1.", "Длок 1."],
    "parentheses_negative": ["Блак", "Длок"],
    "factor_common_monomial": ["Днек", "Длок", "Блок 2.", "Блак 1.-5"],
    "binomial_multiplication": ["1 х-х = x2", "3|3+5m+ 2m +10|= m2 + 7m +10", "Блак 1-", "1 2 152 + 0+5"],
    "powers_monomials": ["1 х-х = x2", "1)(2 х) (22) = 4х2"],
    "polynomial_structure_operations": ["1 х-х = x2", "3|3+5m+ 2m +10|= m2 + 7m +10"],
    "square_of_sum": ["1)a. a + a. b", "14x+4х = 8 х", "1)(2 х) (22) = 4х2", "Бижк 1.-2"],
    "identity_proof": ["Бижк 1.-2"],
    "reasoning_generalization": ["Бижк 1.-2"],
    "factorization_special_products": ["Бижк 1.-2"],
    "coordinate_intervals_distance": [],
    "function_concept_graph_analysis": [],
    "linear_function_abs_piecewise": [],
    "divisibility_primes_criteria": [],
    "gcd_lcm_euclid": [],
    "remainders_arithmetic": [],
    "absolute_value_equations": [],
    "linear_systems": [],
    "geometry_basic_objects": [],
    "geometry_axiomatic_language": ["Бижк 1.-2"],
    "geometry_angle_measurement": ["Бижк 1.-2"],
    "geometry_adjacent_vertical_angles": ["Бижк 1.-2"],
    "geometry_polygons_symmetry": [],
    "geometry_triangle_elements": [],
    "geometry_congruence_isosceles": [],
    "geometry_parallel_lines": [],
    "geometry_polygon_angle_sums": [],
    "geometry_right_triangles": [],
    "geometry_triangle_inequalities": [],
    "geometry_circle_tangents": [],
    "geometry_loci": [],
    "geometry_compass_straightedge": [],
    "data_tables_diagrams": [],
    "statistical_measures": [],
    "advanced_statistical_measures": [],
    "random_variability_grouping": [],
    "random_experiment_outcomes": [],
    "relative_frequency": [],
    "classical_probability": [],
    "graph_models": [],
    "graph_path_enumeration": [],
    "logic_statements": [],
    "equations_one_root": ["X=46", "2)(- 5)", "5.pdf"],
    "equations_fraction_decimal_answers": ["12,5 х", "1,20", "1,4 х"],
    "special_equations": ["Экзамен по математике"],
    "simple_inequalities": ["округлить", "Экзамен по математике", "Блак 1.-5"],
    "negative_multiplier_inequalities": ["Экзамен по математике", "Блок", "Блак 1.-5"],
    "substitution_check": ["Экзамен по математике", "X=46"],
    "word_problems_table": ["Пусть Х", "Экзамен по математике"],
    "variable_meaning": ["Пусть Х", "Экзамен по математике", "3|3+5m+ 2m +10|= m2 + 7m +10", "Блак 1-"],
    "mixed_transfer": ["Экзамен по математике", "Блок", "Длок", "Блак 1.-5"],
}

FOCUS_ORDER = [
    "square_of_sum",
    "identity_proof",
    "reasoning_generalization",
    "geometry_adjacent_vertical_angles",
    "geometry_axiomatic_language",
    "data_tables_diagrams",
    "binomial_multiplication",
    "negative_multiplier_inequalities",
    "simple_inequalities",
    "factor_common_monomial",
    "mixed_transfer",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_capabilities() -> list[dict[str, str]]:
    capabilities: list[dict[str, str]] = []
    for domain, path in CAPABILITY_MATRICES.items():
        for row in read_csv(path):
            item = dict(row)
            item["domain"] = domain
            capabilities.append(item)
    return capabilities


def read_curriculum() -> list[dict[str, str]]:
    return read_csv(CURRICULUM_PATH)


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
    return f'<span class="status {cls}">{esc(label)}</span>'


def render_capability_rows(
    capabilities: list[dict[str, str]],
    day_index: dict[int, dict[str, list[dict[str, str]]]],
    source: list[dict[str, str]],
) -> str:
    rows: list[str] = []
    for cap in capabilities:
        key = cap["capability"]
        domain = cap["domain"]
        title = CAPABILITY_LABELS.get(key, key)
        search_text = " ".join(
            [
                DOMAIN_LABELS[domain],
                title,
                cap["evidence"],
                cap["next_gate"],
            ]
        ).lower()
        rows.append(
            "<tr "
            f'data-status="{esc(cap["status"])}" '
            f'data-domain="{esc(domain)}" '
            f'data-search="{esc(search_text)}">'
            f"<th scope=\"row\">{esc(title)}</th>"
            f"<td data-label=\"Направление\">{domain_badge(domain)}</td>"
            f"<td data-label=\"Статус\">{status_badge(cap['status'])}</td>"
            f"<td data-label=\"Уровень\">{level_bar(cap['level'])}</td>"
            f"<td data-label=\"Что уже видно\">{esc(cap['evidence'])}</td>"
            f"<td data-label=\"Следующий шаг\">{esc(cap['next_gate'])}</td>"
            f"<td data-label=\"Материалы\">{capability_artifacts(key, day_index, source)}</td>"
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
    for day in sorted(day_index, reverse=True):
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


def render_latest_bundle(
    latest_day: int,
    day_index: dict[int, dict[str, list[dict[str, str]]]],
) -> str:
    if not latest_day:
        return '<span class="muted">Комплекты ещё не добавлены</span>'
    labels = {
        "tasks": "Задания ребёнку",
        "answers": "Ответы родителю",
        "feedback_child": "Обратная связь ребёнку",
        "feedback_parent": "Обратная связь родителю",
    }
    links: list[str] = []
    for kind in ["tasks", "answers", "feedback_child", "feedback_parent"]:
        bundle_day = latest_day if kind in {"tasks", "answers"} else latest_day - 1
        bundle = day_index.get(bundle_day, {})
        for item in bundle.get(kind, [])[:1]:
            links.append(link(item["final_path"], labels[kind]))
    return (
        f'<div class="latest-number">День {latest_day}</div>'
        '<div class="latest-copy"><strong>Комплект готов к выдаче</strong>'
        '<span>Начните с задания; ответы и обратная связь находятся рядом.</span></div>'
        f'<div class="latest-links">{" ".join(links)}</div>'
    )


def render_focus(capabilities: list[dict[str, str]]) -> str:
    by_key = {cap["capability"]: cap for cap in capabilities}
    cards: list[str] = []
    for key in FOCUS_ORDER:
        cap = by_key.get(key)
        if not cap or cap["status"] == "PASS":
            continue
        title = CAPABILITY_LABELS.get(key, key)
        cards.append(
            '<article class="focus-item">'
            f'<div><h3>{esc(title)}</h3>{status_badge(cap["status"])}</div>'
            f'{domain_badge(cap["domain"])}'
            f'<p>{esc(cap["evidence"])}</p>'
            f'<strong>Дальше: {esc(cap["next_gate"])}</strong>'
            '</article>'
        )
    return "\n".join(cards) or '<p class="muted">Срочных зон тренировки нет.</p>'


def domain_badge(domain: str) -> str:
    return (
        f'<span class="domain-tag domain-{esc(domain)}">'
        f"{esc(DOMAIN_LABELS[domain])}</span>"
    )


def render_domain_overview(capabilities: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for domain in CAPABILITY_MATRICES:
        domain_caps = [cap for cap in capabilities if cap["domain"] == domain]
        counts = defaultdict(int)
        for cap in domain_caps:
            counts[cap["status"]] += 1
        count_text = (
            f'{counts["PASS"]} закреплено · {counts["WATCH"]} наблюдаем · '
            f'{counts["TRAIN"]} тренируем · {counts["NEW"]} новых'
        )
        cards.append(
            f'<article class="domain-item domain-border-{esc(domain)}">'
            f'<div><h3>{esc(DOMAIN_LABELS[domain])}</h3>'
            f'<strong>{len(domain_caps)} навыков</strong></div>'
            f'<p>{esc(DOMAIN_DESCRIPTIONS[domain])}</p>'
            f'<span>{esc(count_text)}</span>'
            '</article>'
        )
    return "\n".join(cards)


def render_matrix_links() -> str:
    return ", ".join(
        link(
            str(path.relative_to(REPO_ROOT)),
            DOMAIN_LABELS[domain],
        )
        for domain, path in CAPABILITY_MATRICES.items()
    )


def render_grade7_targets() -> str:
    return " ".join(
        link(path, label)
        for path, label in GRADE7_TARGET_CONTROLS
    )


def render_curriculum(curriculum: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for domain in CAPABILITY_MATRICES:
        units = [row for row in curriculum if row["domain"] == domain]
        hours = sum(int(row["hours"]) for row in units)
        unit_rows = "".join(
            "<li>"
            f'<span><b>{esc(row["sequence"])}</b> {esc(row["unit"])}</span>'
            f'<strong>{esc(row["hours"])} ч</strong>'
            "</li>"
            for row in units
        )
        cards.append(
            f'<article class="curriculum-item domain-border-{esc(domain)}">'
            f'<div><h3>{esc(DOMAIN_LABELS[domain])}</h3>'
            f"<strong>{hours} ч</strong></div>"
            f'<ol class="curriculum-list">{unit_rows}</ol>'
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
    latest_day: int,
) -> str:
    status_counts = defaultdict(int)
    for cap in capabilities:
        status_counts[cap["status"]] += 1
    cards = [
        (status_counts["PASS"], "закреплено"),
        (status_counts["WATCH"], "под наблюдением"),
        (status_counts["TRAIN"], "тренируем сейчас"),
        (status_counts["NEW"], "ещё не диагностировано"),
        (f"День {latest_day}" if latest_day else "-", "последний комплект"),
    ]
    return "\n".join(
        '<div class="stat">'
        f"<strong>{esc(value)}</strong><span>{esc(label)}</span>"
        "</div>"
        for value, label in cards
    )


def render_html() -> str:
    capabilities = read_capabilities()
    curriculum = read_curriculum()
    artifacts, _by_path = read_artifacts()
    summary = read_summary()
    day_index = build_day_index(artifacts)
    source = build_source_index(artifacts)
    latest_day = max(day_index, default=0)

    pass_count = sum(1 for cap in capabilities if cap["status"] == "PASS")
    watch_count = sum(1 for cap in capabilities if cap["status"] == "WATCH")
    train_count = sum(1 for cap in capabilities if cap["status"] == "TRAIN")
    new_count = sum(1 for cap in capabilities if cap["status"] == "NEW")
    domain_counts = defaultdict(int)
    for cap in capabilities:
        domain_counts[cap["domain"]] += 1

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
      --bg: #f5f7fa;
      --panel: #ffffff;
      --ink: #1c2331;
      --muted: #667085;
      --line: #d9dee8;
      --soft: #eef2f7;
      --blue: #2563eb;
      --green: #14804a;
      --amber: #b76e00;
      --red: #bd2b2b;
      --violet: #6d4aff;
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
      font-size: 36px;
      line-height: 1.12;
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
    .day-links a,
    .target-links a {{
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
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-top: 18px;
    }}
    .stat {{
      min-height: 92px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}
    .stat strong {{ display: block; font-size: 28px; line-height: 1; }}
    .stat span {{ display: block; margin-top: 8px; font-weight: 650; }}
    .latest-panel {{
      display: grid;
      grid-template-columns: auto minmax(220px, 1fr) minmax(300px, auto);
      gap: 18px;
      align-items: center;
      padding: 18px;
      border: 1px solid #b8c9e8;
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      background: var(--panel);
    }}
    .latest-number {{
      color: var(--blue);
      font-size: 24px;
      font-weight: 750;
      white-space: nowrap;
    }}
    .latest-copy strong, .latest-copy span {{ display: block; }}
    .latest-copy span {{ margin-top: 3px; color: var(--muted); }}
    .latest-links {{ display: flex; flex-wrap: wrap; gap: 7px; justify-content: flex-end; }}
    .latest-links a {{
      display: inline-flex;
      min-height: 34px;
      align-items: center;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: #26364f;
      font-size: 13px;
    }}
    .section-heading {{ margin: 0 0 10px; }}
    .section-heading h2 {{ margin: 0; font-size: 22px; }}
    .section-heading p {{ margin: 4px 0 0; color: var(--muted); }}
    .domain-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}
    .domain-item {{
      padding: 14px;
      border: 1px solid var(--line);
      border-left-width: 5px;
      border-radius: 8px;
      background: var(--panel);
    }}
    .domain-item > div {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
    }}
    .domain-item h3 {{ margin: 0; font-size: 18px; }}
    .domain-item p {{ margin: 8px 0; color: #344054; }}
    .domain-item span {{ color: var(--muted); font-size: 13px; }}
    .domain-border-algebra {{ border-left-color: var(--blue); }}
    .domain-border-geometry {{ border-left-color: var(--green); }}
    .domain-border-probability_statistics {{ border-left-color: var(--violet); }}
    .target-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .program-panel {{
      padding: 16px;
      border: 1px solid #b8c9e8;
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      background: var(--panel);
    }}
    .program-panel > div {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .program-panel p {{ margin: 8px 0 12px; color: #344054; }}
    .curriculum-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }}
    .curriculum-item {{
      padding: 14px;
      border: 1px solid var(--line);
      border-left-width: 5px;
      border-radius: 8px;
      background: var(--panel);
    }}
    .curriculum-item > div {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 10px;
    }}
    .curriculum-item h3 {{ margin: 0; font-size: 17px; }}
    .curriculum-list {{ margin: 10px 0 0; padding: 0; list-style: none; }}
    .curriculum-list li {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      padding: 7px 0;
      border-top: 1px solid var(--line);
      font-size: 13px;
    }}
    .curriculum-list li b {{
      display: inline-block;
      width: 20px;
      color: var(--muted);
    }}
    .curriculum-list li strong {{ white-space: nowrap; color: var(--muted); }}
    .focus-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}
    .focus-item {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}
    .focus-item > div {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }}
    .focus-item h3 {{ margin: 0; font-size: 16px; }}
    .focus-item p {{ margin: 10px 0; color: #344054; }}
    .focus-item > strong {{ display: block; font-size: 13px; color: var(--muted); }}
    .domain-tag {{
      display: inline-flex;
      width: fit-content;
      margin-top: 8px;
      padding: 3px 7px;
      border-radius: 5px;
      font-size: 12px;
      font-weight: 700;
    }}
    .domain-algebra {{ color: #174ea6; background: #eaf1ff; }}
    .domain-geometry {{ color: #146c43; background: #e8f6ef; }}
    .domain-probability_statistics {{ color: #6540a4; background: #f1ebff; }}
    .toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }}
    .toolbar h2, section h2 {{ margin: 0; font-size: 22px; letter-spacing: 0; }}
    .filters {{
      display: flex;
      align-items: flex-end;
      justify-content: flex-end;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .filter-group {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}
    .filter-group-label {{
      width: 100%;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }}
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
    }}
    table {{ width: 100%; border-collapse: collapse; min-width: 1180px; }}
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
      min-width: 92px;
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
    details.archive {{
      border-top: 1px solid var(--line);
      padding-top: 14px;
    }}
    details.archive > summary {{
      width: fit-content;
      color: var(--ink);
      font-size: 18px;
      font-weight: 700;
      cursor: pointer;
    }}
    details.archive[open] > summary {{ margin-bottom: 12px; }}
    mjx-container {{ max-width: 100%; }}
    mjx-container[display="true"] {{ overflow-x: auto; overflow-y: hidden; }}
    @media (max-width: 880px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .stats {{ grid-template-columns: repeat(2, minmax(130px, 1fr)); }}
      .quick-links {{ width: 100%; }}
      .latest-panel {{ grid-template-columns: 1fr; gap: 10px; }}
      .latest-links {{ justify-content: flex-start; }}
      .domain-grid {{ grid-template-columns: 1fr; }}
      .curriculum-grid {{ grid-template-columns: 1fr; }}
      .focus-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 700px) {{
      h1 {{ font-size: 30px; }}
      .table-wrap {{ overflow: visible; border: 0; background: transparent; }}
      table, tbody, tr, th, td {{ display: block; width: 100%; }}
      table {{ min-width: 0; }}
      thead {{ display: none; }}
      tbody tr {{
        margin-bottom: 10px;
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
      }}
      tbody tr[hidden] {{ display: none; }}
      tbody th {{ width: auto; padding: 14px; background: var(--soft); }}
      tbody td {{
        display: grid;
        grid-template-columns: 108px minmax(0, 1fr);
        gap: 10px;
        padding: 11px 14px;
      }}
      tbody td::before {{
        content: attr(data-label);
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
      }}
      .source-table tbody td:first-child::before {{ content: "Тип"; }}
      .source-table tbody td:nth-child(2)::before {{ content: "Файл"; }}
      .source-table tbody td:nth-child(3)::before {{ content: "Размер"; }}
      .source-table tbody td:nth-child(4)::before {{ content: "SHA-256"; }}
    }}
  </style>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['\\\\(', '\\\\)']],
        displayMath: [['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="topline">
        <div>
          <h1>Математика Настюшика</h1>
          <p class="subtitle">
            Здесь видно, что уже закреплено, что сейчас требует внимания
            и какой комплект выдавать следующим.
          </p>
        </div>
        <nav class="quick-links" aria-label="Ключевые артефакты">
          <a href="#targets">Углублённый маршрут</a>
          {link(TARGET_CONTROL, "Контрольная 6 класса")}
          {link(SESSION_PROMPTS, "Шаблоны запросов")}
          {link(FULL_ARCHIVE, "Скачать весь архив")}
        </nav>
      </div>
      <div class="stats">
        {render_stats(capabilities, artifacts, summary, latest_day)}
      </div>
    </div>
  </header>

  <main>
    <section aria-labelledby="latest-title">
      <div class="section-heading">
        <h2 id="latest-title">Что выдавать сейчас</h2>
      </div>
      <div class="latest-panel">
        {render_latest_bundle(latest_day, day_index)}
      </div>
    </section>

    <section aria-labelledby="focus-title">
      <div class="section-heading">
        <h2 id="focus-title">Сейчас в фокусе</h2>
        <p>Навыки, которые определяют ближайшие задания.</p>
      </div>
      <div class="focus-grid">
        {render_focus(capabilities)}
      </div>
    </section>

    <section aria-labelledby="domains-title">
      <div class="section-heading">
        <h2 id="domains-title">Направления</h2>
        <p>Один математический маршрут, три независимые линии наблюдения.</p>
      </div>
      <div class="domain-grid">
        {render_domain_overview(capabilities)}
      </div>
    </section>

    <section id="targets" aria-labelledby="targets-title">
      <div class="section-heading">
        <h2 id="targets-title">Углублённая программа 7 класса</h2>
        <p>Основной маршрут: \\(272\\) часа в год и пропорция основных дней \\(4:3:1\\).</p>
      </div>
      <div class="program-panel">
        <div>
          <strong>Федеральная рабочая программа, углублённый уровень</strong>
          {link(ADVANCED_PROGRAM, "Открыть программу")}
        </div>
        <p>
          Базовые контрольные остаются нижним диагностическим порогом.
          Верхнюю цель задают curriculum gates, доказательство и перенос.
        </p>
        <div class="target-links">
          {render_grade7_targets()}
        </div>
      </div>
      <div class="curriculum-grid">
        {render_curriculum(curriculum)}
      </div>
    </section>

    <section>
      <div class="toolbar">
        <h2>Все навыки</h2>
        <div class="filters">
          <input id="search" type="search" placeholder="Найти навык или наблюдение">
          <div class="filter-group" aria-label="Фильтр по направлению">
            <span class="filter-group-label">Направление</span>
            <button data-domain-filter="ALL" class="active">Все</button>
            <button data-domain-filter="algebra">Алгебра: {domain_counts["algebra"]}</button>
            <button data-domain-filter="geometry">Геометрия: {domain_counts["geometry"]}</button>
            <button data-domain-filter="probability_statistics">Вероятность и статистика: {domain_counts["probability_statistics"]}</button>
          </div>
          <div class="filter-group" aria-label="Фильтр по статусу">
            <span class="filter-group-label">Статус</span>
            <button data-status-filter="ALL" class="active">Все</button>
            <button data-status-filter="PASS">Закреплено: {pass_count}</button>
            <button data-status-filter="WATCH">Наблюдаем: {watch_count}</button>
            <button data-status-filter="TRAIN">Тренируем: {train_count}</button>
            <button data-status-filter="NEW">Новое: {new_count}</button>
          </div>
        </div>
      </div>
      <div class="table-wrap">
        <table aria-label="Capability matrix">
          <thead>
            <tr>
              <th>Навык</th>
              <th>Направление</th>
              <th>Статус</th>
              <th>Уровень</th>
              <th>Что уже видно</th>
              <th>Следующий шаг</th>
              <th>Материалы</th>
            </tr>
          </thead>
          <tbody id="capability-body">
            {render_capability_rows(capabilities, day_index, source)}
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <details class="archive">
        <summary>Архив дневных комплектов</summary>
        <div class="day-grid">
          {render_day_cards(day_index)}
        </div>
      </details>
    </section>

    <section class="source-table">
      <details class="archive">
        <summary>Исходные работы и контрольные</summary>
        <div class="table-wrap">
          <table aria-label="Исходные работы">
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
      </details>
    </section>

    <footer>
      Предметные матрицы: {render_matrix_links()}.
      Curriculum: {link("data/curriculum/advanced_grade7.csv", "углублённый 7 класс")}.
      Артефакты: {link("data/artifacts_manifest.csv", "data/artifacts_manifest.csv")}.
    </footer>
  </main>

  <script>
    const search = document.getElementById('search');
    const statusButtons = Array.from(document.querySelectorAll('[data-status-filter]'));
    const domainButtons = Array.from(document.querySelectorAll('[data-domain-filter]'));
    const rows = Array.from(document.querySelectorAll('#capability-body tr'));
    let statusFilter = 'ALL';
    let domainFilter = 'ALL';

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      rows.forEach((row) => {{
        const statusOk = statusFilter === 'ALL' || row.dataset.status === statusFilter;
        const domainOk = domainFilter === 'ALL' || row.dataset.domain === domainFilter;
        const queryOk = !query || row.dataset.search.includes(query);
        row.hidden = !(statusOk && domainOk && queryOk);
      }});
    }}

    search.addEventListener('input', applyFilters);
    statusButtons.forEach((button) => {{
      button.addEventListener('click', () => {{
        statusFilter = button.dataset.statusFilter;
        statusButtons.forEach((b) => b.classList.toggle('active', b === button));
        applyFilters();
      }});
    }});
    domainButtons.forEach((button) => {{
      button.addEventListener('click', () => {{
        domainFilter = button.dataset.domainFilter;
        domainButtons.forEach((b) => b.classList.toggle('active', b === button));
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
