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
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/generated"

CHILD_FEEDBACK = OUT / "feedback_child/obratnaya_svyaz_den41_Nastyushik.pdf"
PARENT_FEEDBACK = OUT / "feedback_parent/obratnaya_svyaz_den41_dlya_roditelya.pdf"
TASKS = OUT / "tasks/den42_zadaniya_Nastyushik.pdf"
ANSWERS = OUT / "answers/den42_otvety_i_akcenty.pdf"

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
        spaceBefore=7,
        spaceAfter=5,
        textColor=colors.HexColor("#1F4E79"),
    )
)
styles.add(
    ParagraphStyle(
        name="BodyRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=9.75,
        leading=13.3,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="TaskRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=10.1,
        leading=14.7,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=9.75,
        leading=13.3,
        leftIndent=5,
        rightIndent=5,
        spaceBefore=4,
        spaceAfter=6,
    )
)


def p(text: str, style: str = "BodyRu") -> Paragraph:
    escaped = html.escape(text).replace("\n", "<br/>")
    return Paragraph(escaped, styles[style])


def p_markup(markup: str, style: str = "BodyRu") -> Paragraph:
    return Paragraph(markup.replace("\n", "<br/>"), styles[style])


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


def callout_markup(markup: str, background: str = "#EEF7FF") -> Table:
    table = Table([[p_markup(markup, "CalloutRu")]], colWidths=[178 * mm])
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


def bullets(story: list, items: list[str]) -> None:
    for item in items:
        story.append(p("- " + item))


def add_items(story: list, items: list[str]) -> None:
    for i, item in enumerate(items, 1):
        story.append(p(f"{i}) {item}", "TaskRu"))


def child_feedback() -> None:
    story = [
        p("Настюшик, обратная связь по Дню 41", "TitleRu"),
        callout(
            "Ты хорошо продолжила 7 класс: тождества исправила, углы решила уверенно, а одночлены в целом уже начинают собираться.",
            "#FFF7E6",
        ),
        p("Что получилось хорошо", "H1Ru"),
    ]
    bullets(
        story,
        [
            "В тождествах ты уже увидела, что 5(x + 1) и 5x + 1 не равны: при x = 2 получается 15 и 11.",
            "Раскрытие скобок и уравнение 4x = 18 решены аккуратно, последний шаг есть: x = 18 : 4 = 4,5.",
            "В одночленах хорошо получились примеры -3ab * 2a = -6a^2b и 4xy * (-2y) = -8xy^2.",
            "Геометрия с углами очень неплохая: вершину O держишь в середине названия, задачи 40° + 30° и 90° - 35° решены верно.",
        ],
    )
    story.append(p("Что надо поправить", "H1Ru"))
    bullets(
        story,
        [
            "В неравенствах нельзя останавливаться на проверке одного числа. Нужен полный ответ: например, -2x >= 10 -> x <= -5.",
            "В одночлене -xy коэффициент равен -1. Минус без числа - это не 'нет коэффициента'.",
            "В примере 0,5x * 8x^2 числа перемножаются один раз: 0,5 * 8 = 4, поэтому ответ 4x^3, не 32x^3.",
            "Если записала (3a)^2 = 3a * 3a, надо сделать ещё один шаг: 3a * 3a = 9a^2.",
        ],
    )
    story.append(p("Куда идём дальше", "H1Ru"))
    story.append(
        callout(
            "Следующий день - многочлены. Это просто сумма одночленов: 3x^2 + 5x - 7. Главная задача - собирать только похожие части.",
            "#EDF7ED",
        )
    )
    doc(CHILD_FEEDBACK, "Обратная связь День 41").build(story, onFirstPage=footer, onLaterPages=footer)


def parent_feedback() -> None:
    story = [
        p("День 41. Обратная связь для родителя", "TitleRu"),
        callout(
            "Общий вывод: переход к многочленам уместен, но в разминке нужно удержать неравенства и стандартный вид одночлена.",
            "#FFF7E6",
        ),
        p("Наблюдения по работе", "H1Ru"),
    ]
    bullets(
        story,
        [
            "Ложное тождество из Дня 40 исправлено: 5(x + 1) и 5x + 1 различены правильно.",
            "Неравенства снова решались через подстановку отдельных чисел, без записи полного множества решений.",
            "Коэффициенты в одночленах в целом поняты, но -xy записано как 'нету', а нужно -1.",
            "Стандартный вид в большинстве произведений получается. Ошибка в 0,5x * 8x^2: лишний множитель 8.",
            "Степень одночлена (3a)^2 пока не доведена до 9a^2.",
            "Углы и задачи на сумму/разность углов выполнены хорошо.",
        ],
    )
    story.append(p("Рекомендация на День 42", "H1Ru"))
    bullets(
        story,
        [
            "Одно видео: Блок 6 из independent_math_course_materials_v2.md, 'Многочлены'.",
            "Разминка: 2 неравенства и 3 одночлена, чтобы закрыть конкретные ошибки.",
            "Новая тема: стандартный вид многочлена и сбор подобных слагаемых.",
            "Геометрия: смежные и вертикальные углы как мини-конспект без второго видео.",
        ],
    )
    doc(PARENT_FEEDBACK, "Обратная связь День 41 для родителя").build(story, onFirstPage=footer, onLaterPages=footer)


def tasks() -> None:
    story = [
        p("День 42. Многочлены + смежные углы", "TitleRu"),
        p("Для Настюшика. Время: 45-55 минут. Без калькулятора.", "SubRu"),
        callout_markup(
            "Обязательная лекция дня: Блок 6 из independent_math_course_materials_v2.md - Многочлены. "
            "Ссылка: <a href=\"https://interneturok.ru/h/biblioteka/algebra/7-klass/privedenie-mnogochlenov-k-standartnomu-vidu-tipovie-zadachi/1\">InternetUrok: многочлены, стандартный вид</a>\n"
            "Смотреть только эту лекцию: до примеров про подобные слагаемые. Геометрию сегодня делаем по мини-конспекту ниже, без второго видео.",
            "#EDF7ED",
        ),
        p("Блок 1. Разминка: закрыть вчерашние ловушки", "H1Ru"),
    ]
    add_items(
        story,
        [
            "Реши неравенство полностью: -2x >= 10.",
            "Реши неравенство полностью: -0,5x < 3.",
            "Запиши коэффициент одночлена: -xy.",
            "Приведи к стандартному виду: 0,5x * 8x^2 =",
            "Доведи до конца: (3a)^2 = 3a * 3a =",
        ],
    )

    story.append(p("Блок 2. Многочлен: найди части", "H1Ru"))
    story.append(callout("Многочлен - это сумма одночленов. В 3x^2 + 5x - 7 три части: 3x^2, 5x, -7."))
    story.append(p("Раздели многочлен на части и подчеркни подобные.", "BodyRu"))
    add_items(
        story,
        [
            "3x + 2x + 5",
            "4a^2 - 3a + 2a^2",
            "7m - 6 + 2m + 10",
            "3x + 2y - x + 5y",
        ],
    )

    story.append(p("Блок 3. Собери подобные слагаемые", "H1Ru"))
    add_items(
        story,
        [
            "3x + 2x =",
            "7a - 4a =",
            "5x + 3 - 2x + 1 =",
            "8m - 6 + 2m + 10 =",
            "4x^2 + 3x + 2x^2 =",
            "7a^2 - 5a + 2a^2 + a =",
            "3x + 2y - x + 5y =",
            "10m - 4n - 3m + n =",
        ],
    )

    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_items(
        story,
        [
            "Приведи к стандартному виду: -3ab * 2a =",
            "Раскрой скобки: -2(x - 6) =",
            "Реши уравнение: 2,5x = 10. Не забудь строку деления.",
            "Проверь при x = 2: 4(x - 1) и 4x - 4. Равны или не равны?",
        ],
    )

    story.append(p("Блок 5. Геометрия: смежные и вертикальные углы", "H1Ru"))
    story.append(callout("Смежные углы вместе дают 180°. Вертикальные углы равны."))
    add_items(
        story,
        [
            "Один из смежных углов равен 50°. Найди второй.",
            "Один из смежных углов равен 125°. Найди второй.",
            "Один из вертикальных углов равен 70°. Найди второй вертикальный.",
            "При пересечении двух прямых один угол равен 40°. Найди остальные три угла.",
        ],
    )
    story.append(p("Вопрос в конце", "H1Ru"))
    story.append(p("Где было легче: собирать похожие слагаемые или считать углы? Что было самым хитрым?", "TaskRu"))
    doc(TASKS, "День 42 задания").build(story, onFirstPage=footer, onLaterPages=footer)


def answers() -> None:
    story = [
        p("День 42. Ответы и акценты для проверки", "TitleRu"),
        callout(
            "Главный акцент: многочлены собираются только по подобным слагаемым. x^2 нельзя складывать с x, а x нельзя складывать с числом.",
            "#FFF7E6",
        ),
        p("Блок 1. Разминка", "H1Ru"),
    ]
    add_items(
        story,
        [
            "-2x >= 10 -> x <= -5. Знак поменялся.",
            "-0,5x < 3 -> x > -6. Знак поменялся.",
            "-xy: коэффициент -1.",
            "0,5x * 8x^2 = 4x^3.",
            "(3a)^2 = 3a * 3a = 9a^2.",
        ],
    )

    story.append(p("Блок 2. Части многочлена", "H1Ru"))
    add_items(
        story,
        [
            "3x, 2x, 5. Подобные: 3x и 2x.",
            "4a^2, -3a, 2a^2. Подобные: 4a^2 и 2a^2.",
            "7m, -6, 2m, 10. Подобные: 7m и 2m; -6 и 10.",
            "3x, 2y, -x, 5y. Подобные: 3x и -x; 2y и 5y.",
        ],
    )

    story.append(p("Блок 3. Подобные слагаемые", "H1Ru"))
    add_items(
        story,
        [
            "5x.",
            "3a.",
            "3x + 4.",
            "10m + 4.",
            "6x^2 + 3x.",
            "9a^2 - 4a.",
            "2x + 7y.",
            "7m - 3n.",
        ],
    )

    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_items(
        story,
        [
            "-3ab * 2a = -6a^2b.",
            "-2(x - 6) = -2x + 12.",
            "2,5x = 10 -> x = 10 : 2,5 = 4.",
            "При x = 2: 4 * 1 = 4, а 8 - 4 = 4. Равны.",
        ],
    )

    story.append(p("Блок 5. Геометрия", "H1Ru"))
    add_items(
        story,
        [
            "180° - 50° = 130°.",
            "180° - 125° = 55°.",
            "Вертикальный угол тоже 70°.",
            "Остальные углы: 140°, 40°, 140°.",
        ],
    )
    story.append(p("Что считать успехом", "H1Ru"))
    bullets(
        story,
        [
            "В неравенствах есть полный ответ x <= ... или x > ...",
            "Коэффициент -1 в -xy записан явно.",
            "В многочленах не складываются разные типы: x^2, x и числа.",
            "В смежных углах используется сумма 180°.",
            "В вертикальных углах используется равенство углов.",
        ],
    )
    doc(ANSWERS, "День 42 ответы").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        path.parent.mkdir(parents=True, exist_ok=True)
    child_feedback()
    parent_feedback()
    tasks()
    answers()
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        print(path)
