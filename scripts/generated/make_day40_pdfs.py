from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
TASKS_PATH = ROOT / "artifacts/generated/tasks/den40_zadaniya_Nastyushik.pdf"
ANSWERS_PATH = ROOT / "artifacts/generated/answers/den40_otvety_i_akcenty.pdf"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

pdfmetrics.registerFont(TTFont("TaskFont", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("TaskFont-Bold", FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleRu",
        parent=styles["Title"],
        fontName="TaskFont-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="SubRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="H1Ru",
        parent=styles["Heading1"],
        fontName="TaskFont-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=6,
        spaceAfter=5,
        textColor=colors.HexColor("#1F4E79"),
    )
)
styles.add(
    ParagraphStyle(
        name="BodyRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=9.8,
        leading=13.5,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=8.8,
        leading=12,
        spaceAfter=3,
        textColor=colors.HexColor("#444444"),
    )
)
styles.add(
    ParagraphStyle(
        name="TaskRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=10.2,
        leading=15,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=10,
        leading=14,
        leftIndent=5,
        rightIndent=5,
        spaceBefore=4,
        spaceAfter=6,
    )
)


def p(text: str, style: str = "BodyRu") -> Paragraph:
    escaped = html.escape(text).replace("\n", "<br/>")
    return Paragraph(escaped, styles[style])


def doc(path: Path, title: str) -> SimpleDocTemplate:
    return SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
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
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(background)),
                ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#B7CEE8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def add_tasks(story: list, tasks: list[str]) -> None:
    for i, task in enumerate(tasks, 1):
        story.append(p(f"{i}) {task}", "TaskRu"))


def add_answers(story: list, answers: list[str]) -> None:
    for i, answer in enumerate(answers, 1):
        story.append(p(f"{i}) {answer}", "TaskRu"))


def build_tasks() -> None:
    story = []
    story.append(p("День 40. Первый вход в алгебру и геометрию 7 класса", "TitleRu"))
    story.append(p("Для Настюшика. Время: 45-55 минут. Без калькулятора.", "SubRu"))
    story.append(
        callout(
            "Сегодня начинаем 7 класс мягко: в алгебре - тождества и степени, "
            "в геометрии - точка, прямая, отрезок, луч. Старые навыки не бросаем: "
            "знаки, скобки и последний шаг в уравнении остаются в разминке.",
            "#FFF7E6",
        )
    )

    story.append(p("Что посмотреть перед заданием", "H1Ru"))
    story.append(
        callout(
            "Обязательная лекция дня: Блок 3 из independent_math_course_materials_v2.md - "
            "Тождества: выражения могут выглядеть по-разному. Ссылка: "
            "https://interneturok.ru/h/biblioteka/algebra/7-klass/tozhdestva/1\n"
            "Смотреть только эту лекцию: до первого понятного разобранного примера про равные выражения. "
            "Потом сразу делать Блоки 2-3. Степени и геометрию сегодня берём из мини-конспекта в этом листе, без второго видео.",
            "#EDF7ED",
        )
    )

    story.append(p("Правила дня", "H1Ru"))
    for item in [
        "В уравнениях обязательно пиши последний шаг: 2x = 8, значит x = 8 : 2 = 4.",
        "В неравенствах при делении на отрицательное число знак переворачивается.",
        "В геометрии важны подписи: точка A, прямая AB, отрезок CD, луч OA.",
        "В задачах на отрезки сначала сделай маленький рисунок.",
    ]:
        story.append(p("- " + item))

    story.append(p("Блок 1. Разминка: удержать старые навыки", "H1Ru"))
    add_tasks(
        story,
        [
            "7 - 12 + 5 =",
            "12,5x - 1,2x - 0,8x =",
            "-2(x + 4) =",
            "3(2x - 5) - 4(x - 4) =",
            "0,5x = 3. Реши уравнение и запиши строку деления.",
            "-3x >= 12. Реши неравенство и не забудь про знак.",
        ],
    )

    story.append(p("Блок 2. Алгебра 7 класса: тождества", "H1Ru"))
    story.append(
        callout(
            "Тождество - это равенство, которое верно при любом значении буквы. "
            "Например, 2(x + 3) и 2x + 6 дают одинаковый результат при любом x.",
        )
    )
    story.append(p("Проверь подстановкой x = 2, равны ли выражения. Напиши: равны / не равны.", "BodyRu"))
    add_tasks(
        story,
        [
            "3(x + 1) и 3x + 3",
            "4(x - 2) и 4x - 8",
            "5(x + 1) и 5x + 1",
            "-2(x - 5) и -2x + 10",
            "0,5(x + 8) и 0,5x + 4",
        ],
    )

    story.append(p("Блок 3. Раскрой скобки и приведи подобные", "H1Ru"))
    add_tasks(
        story,
        [
            "2(a + 5) =",
            "3(b - 4) =",
            "-2(x + 6) =",
            "-5(y - 3) =",
            "0,5(m + 8) =",
            "4(x - 2) + 3x =",
        ],
    )

    story.append(p("Блок 4. Алгебра 7 класса: степени", "H1Ru"))
    story.append(
        callout(
            "Степень - это короткая запись умножения: 2^3 = 2 * 2 * 2. "
            "В скобках минус тоже повторяется: (-3)^2 = (-3) * (-3).",
        )
    )
    story.append(p("Запиши как произведение.", "BodyRu"))
    add_tasks(story, ["5^2", "4^3", "a^3", "x^5"])
    story.append(p("Запиши степенью или вычисли.", "BodyRu"))
    add_tasks(
        story,
        [
            "7 * 7 =",
            "2 * 2 * 2 * 2 =",
            "m * m * m =",
            "2^4 =",
            "(-2)^3 =",
            "(-3)^2 =",
        ],
    )

    story.append(p("Блок 5. Геометрия 7 класса: точки, прямые, отрезки, лучи", "H1Ru"))
    story.append(
        callout(
            "Отрезок имеет два конца. Луч имеет начало. Прямая идет бесконечно в обе стороны.",
        )
    )
    story.append(p("Сделай рисунки в тетради и подпиши точки.", "BodyRu"))
    add_tasks(
        story,
        [
            "Поставь точки A и B. Проведи прямую AB.",
            "Поставь точки C и D. Нарисуй отрезок CD.",
            "Поставь точку O. Нарисуй луч OA.",
            "На одной прямой отметь точки A, B, C так, чтобы B была между A и C.",
            "Нарисуй два отрезка, которые пересекаются в точке M.",
        ],
    )

    story.append(p("Блок 6. Геометрия: задачи на длины отрезков", "H1Ru"))
    story.append(p("Перед каждым решением нарисуй схему.", "BodyRu"))
    add_tasks(
        story,
        [
            "Точка B лежит между A и C. AB = 4 см, BC = 7 см. Найди AC.",
            "Точка M лежит между K и P. KP = 15 см, KM = 6 см. Найди MP.",
            "Отрезок AB = 12 см. Точка C - середина AB. Найди AC и CB.",
        ],
    )

    story.append(p("Вопрос в конце", "H1Ru"))
    story.append(p("Что сегодня было легче: тождества, степени или геометрические рисунки? Где запуталась?", "TaskRu"))

    doc(TASKS_PATH, "День 40 задания").build(story, onFirstPage=footer, onLaterPages=footer)


def build_answers() -> None:
    story = []
    story.append(p("День 40. Ответы и акценты для проверки", "TitleRu"))
    story.append(
        callout(
            "Это первый день семиклассного контура. Проверяем не скорость, а язык записи: "
            "в алгебре - равенство выражений и степени, в геометрии - правильные названия и рисунки.",
            "#FFF7E6",
        )
    )

    story.append(p("Блок 1. Разминка", "H1Ru"))
    add_answers(
        story,
        [
            "0.",
            "10,5x.",
            "-2x - 8.",
            "6x - 15 - 4x + 16 = 2x + 1.",
            "x = 3 : 0,5 = 6.",
            "x <= -4, потому что делим на -3 и знак переворачивается.",
        ],
    )

    story.append(p("Блок 2. Тождества", "H1Ru"))
    add_answers(
        story,
        [
            "Равны. При x = 2: 3 * 3 = 9 и 3 * 2 + 3 = 9.",
            "Равны. При x = 2: 4 * 0 = 0 и 8 - 8 = 0.",
            "Не равны. При x = 2: 5 * 3 = 15, а 5 * 2 + 1 = 11.",
            "Равны. При x = 2: -2 * (-3) = 6, а -4 + 10 = 6.",
            "Равны. При x = 2: 0,5 * 10 = 5, а 1 + 4 = 5.",
        ],
    )
    story.append(
        callout(
            "Акцент: подстановка одного числа помогает заметить ошибку, но настоящее тождество "
            "доказываем раскрытием скобок и приведением подобных.",
        )
    )

    story.append(p("Блок 3. Скобки и подобные", "H1Ru"))
    add_answers(
        story,
        [
            "2a + 10.",
            "3b - 12.",
            "-2x - 12.",
            "-5y + 15.",
            "0,5m + 4.",
            "4x - 8 + 3x = 7x - 8.",
        ],
    )

    story.append(p("Блок 4. Степени", "H1Ru"))
    story.append(p("Записать как произведение:", "BodyRu"))
    add_answers(
        story,
        [
            "5^2 = 5 * 5.",
            "4^3 = 4 * 4 * 4.",
            "a^3 = a * a * a.",
            "x^5 = x * x * x * x * x.",
        ],
    )
    story.append(p("Записать степенью или вычислить:", "BodyRu"))
    add_answers(
        story,
        [
            "7 * 7 = 7^2.",
            "2 * 2 * 2 * 2 = 2^4.",
            "m * m * m = m^3.",
            "2^4 = 16.",
            "(-2)^3 = -8.",
            "(-3)^2 = 9.",
        ],
    )
    story.append(
        callout(
            "Акцент: (-3)^2 положительное, потому что минус умножается на минус. "
            "Но -3^2 без скобок обычно читается как -(3^2) = -9; эту тонкость можно только обозначить, не перегружая.",
        )
    )

    story.append(p("Блок 5. Геометрические рисунки", "H1Ru"))
    for item in [
        "Прямая AB должна проходить через точки A и B и продолжаться в обе стороны.",
        "Отрезок CD должен иметь два конца: C и D.",
        "Луч OA начинается в O и проходит через A.",
        "Если B между A и C, порядок на прямой: A - B - C или C - B - A.",
        "У пересекающихся отрезков точка M должна быть общей точкой.",
    ]:
        story.append(p("- " + item))

    story.append(p("Блок 6. Длины отрезков", "H1Ru"))
    add_answers(
        story,
        [
            "AC = AB + BC = 4 + 7 = 11 см.",
            "MP = KP - KM = 15 - 6 = 9 см.",
            "AC = CB = 12 : 2 = 6 см.",
        ],
    )

    story.append(p("Что считать успехом дня", "H1Ru"))
    for item in [
        "В уравнении 0,5x = 3 есть строка x = 3 : 0,5.",
        "В неравенстве -3x >= 12 знак поменялся.",
        "В тождествах Настюшик не просто угадывает, а делает подстановку x = 2.",
        "В степенях понимает, что показатель говорит, сколько раз повторяется множитель.",
        "В геометрии подписывает точки и перед задачей на длину рисует схему.",
    ]:
        story.append(p("- " + item))

    story.append(p("Следующий акцент", "H1Ru"))
    story.append(
        p(
            "Если День 40 идет спокойно, дальше можно дать одночлены и продолжить геометрию углами. "
            "Если путаются степени или подписи фигур, следующий день лучше сделать повтором: 6 заданий на степени и 6 рисунков.",
            "BodyRu",
        )
    )

    doc(ANSWERS_PATH, "День 40 ответы").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ANSWERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    build_tasks()
    build_answers()
    print(TASKS_PATH)
    print(ANSWERS_PATH)
