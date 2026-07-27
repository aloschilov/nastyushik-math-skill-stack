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

CHILD_FEEDBACK = OUT / "feedback_child/obratnaya_svyaz_den42_Nastyushik.pdf"
PARENT_FEEDBACK = OUT / "feedback_parent/obratnaya_svyaz_den42_dlya_roditelya.pdf"
TASKS = OUT / "tasks/den43_zadaniya_Nastyushik.pdf"
ANSWERS = OUT / "answers/den43_otvety_i_akcenty.pdf"

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
        spaceBefore=5,
        spaceAfter=4,
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
        leading=13.8,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=9.75,
        leading=12.8,
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
        p("Настюшик, обратная связь по Дню 42", "TitleRu"),
        callout(
            "Ты хорошо вошла в тему многочленов: простые похожие слагаемые собираются, неравенства с минусом стали намного увереннее, углы считаются спокойно.",
            "#FFF7E6",
        ),
        p("Что получилось хорошо", "H1Ru"),
    ]
    bullets(
        story,
        [
            "В неравенствах -2x >= 10 и -0,5x < 3 ты уже переворачиваешь знак и получаешь полный ответ.",
            "Коэффициент у -xy исправлен: это -1.",
            "0,5x * 8x^2 и (3a)^2 теперь доведены до правильного стандартного вида.",
            "Простые многочлены 3x + 2x, 7a - 4a, 5x + 3 - 2x + 1 собраны верно.",
            "Смежные углы через 180° и вертикальные углы через равенство ты применяешь правильно.",
        ],
    )
    story.append(p("Что надо поправить", "H1Ru"))
    bullets(
        story,
        [
            "В многочлене нельзя складывать разные буквы: 7m и 2n не похожие. Похожими будут 7m и 2m, а n остаётся отдельно.",
            "Степень нельзя менять при сложении: 7a^2 + 2a^2 = 9a^2, не 9a^3.",
            "Когда объясняешь геометрию словами, лучше писать коротко: вертикальные углы равны, смежные в сумме дают 180°.",
        ],
    )
    story.append(p("Куда идём дальше", "H1Ru"))
    story.append(
        callout(
            "Следующий день - сложение и вычитание многочленов. Главная новая ловушка: если перед скобкой минус, знаки внутри скобки меняются.",
            "#EDF7ED",
        )
    )
    doc(CHILD_FEEDBACK, "Обратная связь День 42").build(story, onFirstPage=footer, onLaterPages=footer)


def parent_feedback() -> None:
    story = [
        p("День 42. Обратная связь для родителя", "TitleRu"),
        callout(
            "Общий вывод: можно переходить к сложению и вычитанию многочленов, но в каждом дне держать контроль подобности слагаемых.",
            "#FFF7E6",
        ),
        p("Наблюдения по работе", "H1Ru"),
    ]
    bullets(
        story,
        [
            "Ошибки Дня 41 почти все закрылись: знак в неравенстве при делении на отрицательное число поменян, -xy распознано как коэффициент -1.",
            "Стандартный вид одночлена заметно лучше: 0,5x * 8x^2 = 4x^3, (3a)^2 = 9a^2.",
            "Приведение подобных в простых случаях получается.",
            "Слабое место: похожесть слагаемых определяется не только числом, но и буквенной частью. m и n складывать нельзя.",
            "В 7a^2 - 5a + 2a^2 + a появилась типовая ошибка: при сложении a^2 и a^2 степень не растёт.",
            "Геометрия со смежными и вертикальными углами идёт хорошо; нужна лишь аккуратность формулировок.",
        ],
    )
    story.append(p("Рекомендация на День 43", "H1Ru"))
    bullets(
        story,
        [
            "Одно видео: Блок 7 из independent_math_course_materials_v2.md, 'Сложение и вычитание многочленов'.",
            "Не давать вторую лекцию по геометрии в этот же день: геометрию оставить короткой практикой.",
            "В заданиях обязательно отделить случаи с плюсом перед скобкой и с минусом перед скобкой.",
            "Проверять не только ответ, но и строку раскрытия скобок: именно там видно, меняются ли знаки.",
        ],
    )
    doc(PARENT_FEEDBACK, "Обратная связь День 42 для родителя").build(story, onFirstPage=footer, onLaterPages=footer)


def tasks() -> None:
    story = [
        p("День 43. Сложение и вычитание многочленов", "TitleRu"),
        p("Для Настюшика. Время: 45-55 минут. Без калькулятора.", "SubRu"),
        callout_markup(
            "Обязательная лекция дня: Блок 7 из independent_math_course_materials_v2.md - Сложение и вычитание многочленов. "
            "Ссылка: <a href=\"https://interneturok.ru/h/biblioteka/algebra/7-klass/slozhenie-i-vichitanie-mnogochlenov-tipovie-zadachi/1\">InternetUrok: сложение и вычитание многочленов</a>\n"
            "Смотреть только эту лекцию. Геометрию сегодня делаем по короткой памятке ниже, без второго видео.",
            "#EDF7ED",
        ),
        p("Блок 1. Разминка: похожие или не похожие", "H1Ru"),
    ]
    story.append(callout("Похожие слагаемые имеют одинаковую буквенную часть: 3x и -x похожие, а x и x^2 не похожие."))
    add_items(
        story,
        [
            "Можно ли сложить 7m и 2m? Если да, сложи.",
            "Можно ли сложить 7m и 2n? Если да, сложи; если нет, напиши 'нельзя'.",
            "Собери: 4x^2 + 2x^2 =",
            "Собери: 7a^2 - 5a + 2a^2 + a =",
            "Собери: 10m - 4n - 3m + n =",
        ],
    )

    story.append(p("Блок 2. Если перед скобкой плюс", "H1Ru"))
    story.append(callout("Если перед скобкой плюс, скобки можно убрать без изменения знаков."))
    add_items(
        story,
        [
            "(2x + 3) + (4x + 5) =",
            "(7a - 2) + (3a + 8) =",
            "(4a^2 + 3a) + (2a^2 - a) =",
            "(3p + 2q) + (5p - q) =",
        ],
    )

    story.append(p("Блок 3. Если перед скобкой минус", "H1Ru"))
    story.append(callout("Если перед скобкой минус, все знаки внутри этой скобки меняются."))
    add_items(
        story,
        [
            "(5m + 1) - (2m + 4) =",
            "(9x - 6) - (3x - 2) =",
            "(8x^2 - 5x) - (3x^2 + 2x) =",
            "(6m - 4n) - (2m - 7n) =",
        ],
    )

    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_items(
        story,
        [
            "Реши неравенство полностью: -3x <= 12.",
            "Раскрой скобки: -4(x - 2) =",
            "Реши уравнение: 1,5x = 9. Не забудь строку деления.",
            "Проверь при x = 3: 2(x + 4) и 2x + 8. Равны или не равны?",
        ],
    )

    story.append(p("Блок 5. Геометрия: углы", "H1Ru"))
    story.append(callout("Смежные углы в сумме дают 180°. Вертикальные углы равны."))
    add_items(
        story,
        [
            "Один из смежных углов равен 65°. Найди второй.",
            "Один из смежных углов равен 118°. Найди второй.",
            "Один из вертикальных углов равен 35°. Найди второй вертикальный.",
            "При пересечении двух прямых один угол равен 75°. Найди остальные три угла.",
        ],
    )
    story.append(p("Вопрос в конце: в каких номерах минус перед скобкой заставил поменять знаки?", "TaskRu"))
    doc(TASKS, "День 43 задания").build(story, onFirstPage=footer, onLaterPages=footer)


def answers() -> None:
    story = [
        p("День 43. Ответы и акценты для проверки", "TitleRu"),
        callout(
            "Главный акцент: сначала раскрыть скобки, затем собрать только подобные слагаемые. При вычитании многочлена меняются все знаки внутри второй скобки.",
            "#FFF7E6",
        ),
        p("Блок 1. Разминка", "H1Ru"),
    ]
    add_items(
        story,
        [
            "7m и 2m похожие: 9m.",
            "7m и 2n не похожие, складывать нельзя.",
            "4x^2 + 2x^2 = 6x^2.",
            "7a^2 - 5a + 2a^2 + a = 9a^2 - 4a.",
            "10m - 4n - 3m + n = 7m - 3n.",
        ],
    )

    story.append(p("Блок 2. Плюс перед скобкой", "H1Ru"))
    add_items(
        story,
        [
            "(2x + 3) + (4x + 5) = 6x + 8.",
            "(7a - 2) + (3a + 8) = 10a + 6.",
            "(4a^2 + 3a) + (2a^2 - a) = 6a^2 + 2a.",
            "(3p + 2q) + (5p - q) = 8p + q.",
        ],
    )

    story.append(p("Блок 3. Минус перед скобкой", "H1Ru"))
    add_items(
        story,
        [
            "(5m + 1) - (2m + 4) = 5m + 1 - 2m - 4 = 3m - 3.",
            "(9x - 6) - (3x - 2) = 9x - 6 - 3x + 2 = 6x - 4.",
            "(8x^2 - 5x) - (3x^2 + 2x) = 8x^2 - 5x - 3x^2 - 2x = 5x^2 - 7x.",
            "(6m - 4n) - (2m - 7n) = 6m - 4n - 2m + 7n = 4m + 3n.",
        ],
    )

    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_items(
        story,
        [
            "-3x <= 12 -> x >= -4. Знак поменялся.",
            "-4(x - 2) = -4x + 8.",
            "1,5x = 9 -> x = 9 : 1,5 = 6.",
            "При x = 3: 2 * 7 = 14, а 6 + 8 = 14. Равны.",
        ],
    )

    story.append(p("Блок 5. Геометрия", "H1Ru"))
    add_items(
        story,
        [
            "180° - 65° = 115°.",
            "180° - 118° = 62°.",
            "Вертикальный угол тоже 35°.",
            "Остальные углы: 105°, 75°, 105°.",
        ],
    )
    story.append(p("Что считать успехом", "H1Ru"))
    bullets(
        story,
        [
            "В вычитании многочлена у всех членов второй скобки поменялись знаки.",
            "m не складывается с n, x не складывается с x^2.",
            "При сложении a^2 + a^2 степень осталась a^2.",
            "В неравенстве с отрицательным коэффициентом знак ответа перевёрнут.",
            "В геометрии смежные углы проверены суммой 180°.",
        ],
    )
    doc(ANSWERS, "День 43 ответы").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        path.parent.mkdir(parents=True, exist_ok=True)
    child_feedback()
    parent_feedback()
    tasks()
    answers()
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        print(path)
