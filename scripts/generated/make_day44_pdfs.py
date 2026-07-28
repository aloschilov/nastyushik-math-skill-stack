from __future__ import annotations

import hashlib
import html
import re
import subprocess
import tempfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/generated"

CHILD_FEEDBACK = OUT / "feedback_child/obratnaya_svyaz_den43_Nastyushik.pdf"
PARENT_FEEDBACK = OUT / "feedback_parent/obratnaya_svyaz_den43_dlya_roditelya.pdf"
TASKS = OUT / "tasks/den44_zadaniya_Nastyushik.pdf"
ANSWERS = OUT / "answers/den44_otvety_i_akcenty.pdf"
FORMULA_DPI = 180
FORMULA_RE = re.compile(r"\\\((.+?)\\\)")
RAW_LATEX_RE = re.compile(
    r"\\\(|\\\)|\\\[|\\\]|\\(?:le|ge|Rightarrow|cdot|circ|ldots)|[A-Za-z]\^[0-9]"
)
FORMULA_TMP = tempfile.TemporaryDirectory(prefix="day44_formula_render_")
FORMULA_CACHE: dict[tuple[str, float], tuple[Path, float, float]] = {}

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

pdfmetrics.registerFont(TTFont("TaskFont", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("TaskFont-Bold", FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleRu", parent=styles["Title"], fontName="TaskFont-Bold", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="SubRu", parent=styles["BodyText"], fontName="TaskFont", fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=10))
styles.add(ParagraphStyle(name="H1Ru", parent=styles["Heading1"], fontName="TaskFont-Bold", fontSize=13, leading=16, spaceBefore=5, spaceAfter=4, textColor=colors.HexColor("#1F4E79")))
styles.add(ParagraphStyle(name="BodyRu", parent=styles["BodyText"], fontName="TaskFont", fontSize=9.75, leading=13.2, spaceAfter=4))
styles.add(ParagraphStyle(name="TaskRu", parent=styles["BodyText"], fontName="TaskFont", fontSize=10.05, leading=13.6, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutRu", parent=styles["BodyText"], fontName="TaskFont", fontSize=9.65, leading=12.6, leftIndent=5, rightIndent=5, spaceBefore=4, spaceAfter=6))


def render_formula(formula: str, font_size: float) -> tuple[Path, float, float]:
    key = (formula, font_size)
    if key in FORMULA_CACHE:
        return FORMULA_CACHE[key]

    digest = hashlib.sha256(f"{font_size}:{formula}".encode("utf-8")).hexdigest()[:16]
    work_dir = Path(FORMULA_TMP.name) / digest
    work_dir.mkdir(parents=True, exist_ok=True)
    tex_path = work_dir / "formula.tex"
    png_path = work_dir / "formula.png"
    tex_path.write_text(
        "\n".join(
            [
                r"\documentclass{article}",
                r"\usepackage[utf8]{inputenc}",
                r"\usepackage[T1]{fontenc}",
                r"\usepackage{amsmath,amssymb}",
                r"\pagestyle{empty}",
                r"\begin{document}",
                rf"\fontsize{{{font_size}}}{{{font_size * 1.2}}}\selectfont",
                f"${formula}$",
                r"\end{document}",
            ]
        ),
        encoding="utf-8",
    )
    subprocess.run(
        ["latex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=work_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    subprocess.run(
        [
            "dvipng",
            "-D",
            str(FORMULA_DPI),
            "-T",
            "tight",
            "-bg",
            "Transparent",
            "-o",
            png_path.name,
            "formula.dvi",
        ],
        cwd=work_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    width_px, height_px = ImageReader(str(png_path)).getSize()
    rendered = (png_path, width_px * 72 / FORMULA_DPI, height_px * 72 / FORMULA_DPI)
    FORMULA_CACHE[key] = rendered
    return rendered


def formulas_to_images(text: str, style: str, *, escape_text: bool) -> str:
    font_size = styles[style].fontSize
    chunks: list[str] = []
    pos = 0
    for match in FORMULA_RE.finditer(text):
        prefix = text[pos : match.start()]
        chunks.append(html.escape(prefix) if escape_text else prefix)
        png_path, width, height = render_formula(match.group(1), font_size)
        src = html.escape(str(png_path), quote=True)
        chunks.append(f'<img src="{src}" width="{width:.2f}" height="{height:.2f}" valign="middle"/>')
        pos = match.end()
    suffix = text[pos:]
    chunks.append(html.escape(suffix) if escape_text else suffix)
    return "".join(chunks).replace("\n", "<br/>")


def p(text: str, style: str = "BodyRu") -> Paragraph:
    return Paragraph(formulas_to_images(text, style, escape_text=True), styles[style])


def p_markup(markup: str, style: str = "BodyRu") -> Paragraph:
    return Paragraph(formulas_to_images(markup, style, escape_text=False), styles[style])


def doc(path: Path, title: str) -> SimpleDocTemplate:
    return SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title=title,
    )


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("TaskFont", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(16 * mm, 9 * mm, "Настюшик - математика, 7 класс")
    canvas.drawRightString(194 * mm, 9 * mm, f"стр. {document.page}")
    canvas.restoreState()


def callout(text: str, background: str = "#EEF7FF") -> Table:
    table = Table([[p(text, "CalloutRu")]], colWidths=[178 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(background)),
        ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#B7CEE8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def callout_markup(markup: str, background: str = "#EEF7FF") -> Table:
    table = Table([[p_markup(markup, "CalloutRu")]], colWidths=[178 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(background)),
        ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#B7CEE8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def bullets(story: list, items: list[str]) -> None:
    for item in items:
        story.append(p("- " + item))


def add_items(story: list, items: list[str]) -> None:
    for i, item in enumerate(items, 1):
        story.append(p(f"{i}) {item}", "TaskRu"))


def child_feedback() -> None:
    story = [
        p("Настюшик, обратная связь по Дню 43", "TitleRu"),
        callout("Ты очень хорошо справилась со сложением и вычитанием многочленов: почти везде видно правильное раскрытие скобок и сбор похожих слагаемых.", "#FFF7E6"),
        p("Что получилось хорошо", "H1Ru"),
    ]
    bullets(story, [
        r"Ты правильно отличила похожие слагаемые: \(7m\) и \(2m\) можно сложить, а \(7m\) и \(2n\) нельзя.",
        r"При плюсе перед скобкой знаки сохранены, ответы \(6x + 8\), \(10a + 6\), \(6a^2 + 2a\), \(8p + q\) верные.",
        "В вычитании многочленов ты в основном поменяла знаки внутри второй скобки: это главный шаг темы.",
        r"Уравнение \(1{,}5x = 9\) решено с делением, проверка тождества при \(x = 3\) сделана аккуратно.",
        "Геометрия с углами стала сильной: смежные и вертикальные углы считаются уверенно.",
    ])
    story.append(p("Что надо поправить", "H1Ru"))
    bullets(story, [
        r"В примере \((6m - 4n) - (2m - 7n)\) после раскрытия получается \(-4n + 7n = +3n\). Ответ: \(4m + 3n\).",
        r"В неравенстве \(-3x \le 12\) нужен один итоговый ответ: \(x \ge -4\). Не надо записывать несколько отдельных вариантов.",
        r"Когда меняешь знак неравенства, полезно сразу писать строку деления: \(x \ge 12 : (-3)\), \(x \ge -4\).",
    ])
    story.append(p("Куда идём дальше", "H1Ru"))
    story.append(callout("Следующий день без нового видео: смешанная тренировка. Цель - сделать многочлены, уравнения и неравенства в одном листе без подсказки типа.", "#EDF7ED"))
    doc(CHILD_FEEDBACK, "Обратная связь День 43").build(story, onFirstPage=footer, onLaterPages=footer)


def parent_feedback() -> None:
    story = [
        p("День 43. Обратная связь для родителя", "TitleRu"),
        callout("Общий вывод: Блок 7 можно считать в основном пройденным. На День 44 лучше дать смешанный день без нового видео.", "#FFF7E6"),
        p("Наблюдения по работе", "H1Ru"),
    ]
    bullets(story, [
        r"Подобные слагаемые распознаются лучше: \(m\) не смешивается с \(n\), \(x^2\) не смешивается с \(x\).",
        "Сложение многочленов с плюсом перед скобкой выполнено уверенно.",
        r"Вычитание многочленов в большинстве случаев выполнено правильно, но осталась точечная ошибка в сумме \(-4n + 7n\).",
        "Неравенство с отрицательным коэффициентом снова стало хрупким: правило смены знака известно, но итоговый ответ записан не как одно условие.",
        "Геометрия со смежными и вертикальными углами идёт хорошо, отдельного геометрического видео на следующий день не требуется.",
    ])
    story.append(p("Рекомендация на День 44", "H1Ru"))
    bullets(story, [
        "Нового видео не давать: по independent_math_course_materials_v2.md это Неделя 2, День 3 - смешанный день без видео.",
        "В начале листа дать мини-конспект: минус перед скобкой меняет все знаки, деление неравенства на отрицательное число переворачивает знак.",
        "Проверять два места: строку раскрытия скобок и финальный ответ в неравенстве.",
        "Геометрию оставить коротким блоком на поддержание, без усложнения.",
    ])
    doc(PARENT_FEEDBACK, "Обратная связь День 43 для родителя").build(story, onFirstPage=footer, onLaterPages=footer)


def tasks() -> None:
    story = [
        p("День 44. Смешанный день: многочлены и неравенства", "TitleRu"),
        p("Для Настюшика. Время: 45-55 минут. Без калькулятора.", "SubRu"),
        callout_markup(
            "Нового видео сегодня нет: это смешанный день по Неделе 2 из independent_math_course_materials_v2.md. "
            "Если перед стартом хочется 5 минут повторить тему, можно открыть ту же лекцию: "
            "<a href=\"https://interneturok.ru/h/biblioteka/algebra/7-klass/slozhenie-i-vichitanie-mnogochlenov-tipovie-zadachi/1\">InternetUrok: сложение и вычитание многочленов</a>\n"
            "Главная памятка: минус перед скобкой меняет все знаки; при делении неравенства на отрицательное число знак переворачивается.",
            "#EDF7ED",
        ),
        p("Блок 1. Исправляем одну ловушку", "H1Ru"),
    ]
    story.append(callout(r"Проверь знак у \(n\): \(-4n + 7n = +3n\)."))
    add_items(story, [
        r"\((6m - 4n) - (2m - 7n) =\)",
        r"\((5a - 3b) - (2a - 6b) =\)",
        r"\((8x - 2y) - (3x - 5y) =\)",
        r"\((4p + q) - (p - 2q) =\)",
    ])

    story.append(p("Блок 2. Многочлены без подсказки", "H1Ru"))
    add_items(story, [
        r"\((3x + 5) + (2x - 9) =\)",
        r"\((7a - 4) - (2a + 6) =\)",
        r"\(4x^2 + 3x - 2x^2 + 5x =\)",
        r"\((9m - 4n) + (2m + n) =\)",
        r"\((6a^2 - a) - (2a^2 - 5a) =\)",
        r"\((10p + 3q) - (4p + 8q) =\)",
    ])

    story.append(p("Блок 3. Неравенства: один полный ответ", "H1Ru"))
    story.append(callout(r"Записывай одну строку ответа: например, \(-3x \le 12 \Rightarrow x \ge -4\)."))
    add_items(story, [
        r"\(-2x \le 8\)",
        r"\(-5x > 15\)",
        r"\(-0{,}5x \ge 3\)",
        r"\(-4(x - 1) < 12\)",
    ])

    story.append(p("Блок 4. Уравнения и тождества", "H1Ru"))
    add_items(story, [
        r"\(2{,}5x = 15\). Не забудь строку деления.",
        r"\(3(x - 2) = 12\).",
        r"Раскрой скобки: \(-3(a - 4) =\)",
        r"Проверь при \(x = 2\): \(5(x - 1)\) и \(5x - 5\). Равны или не равны?",
    ])

    story.append(p("Блок 5. Геометрия на поддержание", "H1Ru"))
    add_items(story, [
        r"Один из смежных углов равен \(48^\circ\). Найди второй.",
        r"Один из вертикальных углов равен \(82^\circ\). Найди второй вертикальный.",
        r"При пересечении двух прямых один угол равен \(120^\circ\). Найди остальные три угла.",
    ])
    story.append(p("Вопрос в конце: где сегодня чаще всего приходилось менять знак?", "TaskRu"))
    doc(TASKS, "День 44 задания").build(story, onFirstPage=footer, onLaterPages=footer)


def answers() -> None:
    story = [
        p("День 44. Ответы и акценты для проверки", "TitleRu"),
        callout("Главный акцент: в вычитании многочленов меняются все знаки второй скобки; в неравенствах нужен один финальный ответ.", "#FFF7E6"),
        p("Блок 1. Ловушка со знаком", "H1Ru"),
    ]
    add_items(story, [
        r"\(6m - 4n - 2m + 7n = 4m + 3n\).",
        r"\(5a - 3b - 2a + 6b = 3a + 3b\).",
        r"\(8x - 2y - 3x + 5y = 5x + 3y\).",
        r"\(4p + q - p + 2q = 3p + 3q\).",
    ])
    story.append(p("Блок 2. Многочлены", "H1Ru"))
    add_items(story, [
        r"\(5x - 4\).",
        r"\(5a - 10\).",
        r"\(2x^2 + 8x\).",
        r"\(11m - 3n\).",
        r"\(4a^2 + 4a\).",
        r"\(6p - 5q\).",
    ])
    story.append(p("Блок 3. Неравенства", "H1Ru"))
    add_items(story, [
        r"\(-2x \le 8 \Rightarrow x \ge -4\).",
        r"\(-5x > 15 \Rightarrow x < -3\).",
        r"\(-0{,}5x \ge 3 \Rightarrow x \le -6\).",
        r"\(-4(x - 1) < 12 \Rightarrow -4x + 4 < 12 \Rightarrow -4x < 8 \Rightarrow x > -2\).",
    ])
    story.append(p("Блок 4. Уравнения и тождества", "H1Ru"))
    add_items(story, [
        r"\(2{,}5x = 15 \Rightarrow x = 15 : 2{,}5 = 6\).",
        r"\(3(x - 2) = 12 \Rightarrow x - 2 = 4 \Rightarrow x = 6\).",
        r"\(-3(a - 4) = -3a + 12\).",
        r"При \(x = 2\): \(5 \cdot 1 = 5\), а \(10 - 5 = 5\). Равны.",
    ])
    story.append(p("Блок 5. Геометрия", "H1Ru"))
    add_items(story, [
        r"\(180^\circ - 48^\circ = 132^\circ\).",
        r"Вертикальный угол тоже \(82^\circ\).",
        r"Остальные углы: \(60^\circ\), \(120^\circ\), \(60^\circ\).",
    ])
    story.append(p("Что считать успехом", "H1Ru"))
    bullets(story, [
        r"В блоке 1 все ответы с плюсом у второй буквы там, где было \(-\ldots + \ldots\).",
        r"В каждом неравенстве есть один ответ вида \(x \ge \ldots\), \(x < \ldots\), \(x \le \ldots\), \(x > \ldots\).",
        "В уравнениях есть строка деления или аккуратный переход после скобок.",
        r"Геометрия проверена правилом \(180^\circ\) или равенством вертикальных углов.",
    ])
    doc(ANSWERS, "День 44 ответы").build(story, onFirstPage=footer, onLaterPages=footer)


def assert_rendered_formulas(paths: list[Path]) -> None:
    for path in paths:
        result = subprocess.run(
            ["pdftotext", str(path), "-"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        match = RAW_LATEX_RE.search(result.stdout)
        if match:
            raise AssertionError(f"raw LaTeX marker remains in {path}: {match.group(0)!r}")


if __name__ == "__main__":
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        path.parent.mkdir(parents=True, exist_ok=True)
    child_feedback()
    parent_feedback()
    tasks()
    answers()
    assert_rendered_formulas([CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS])
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        print(path)
