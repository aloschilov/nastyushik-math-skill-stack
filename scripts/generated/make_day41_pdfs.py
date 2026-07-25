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

CHILD_FEEDBACK = OUT / "feedback_child/obratnaya_svyaz_den40_Nastyushik.pdf"
PARENT_FEEDBACK = OUT / "feedback_parent/obratnaya_svyaz_den40_dlya_roditelya.pdf"
TASKS = OUT / "tasks/den41_zadaniya_Nastyushik.pdf"
ANSWERS = OUT / "answers/den41_otvety_i_akcenty.pdf"

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
        fontSize=9.8,
        leading=13.4,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="TaskRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=10.15,
        leading=14.8,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutRu",
        parent=styles["BodyText"],
        fontName="TaskFont",
        fontSize=9.8,
        leading=13.4,
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


def bullets(story: list, items: list[str]) -> None:
    for item in items:
        story.append(p("- " + item))


def add_tasks(story: list, items: list[str]) -> None:
    for i, item in enumerate(items, 1):
        story.append(p(f"{i}) {item}", "TaskRu"))


def child_feedback() -> None:
    story = [
        p("Настюшик, обратная связь по Дню 40", "TitleRu"),
        callout(
            "Ты очень хорошо вошла в темы 7 класса. Видно, что скобки, степени и первые геометрические рисунки тебе уже не страшны.",
            "#FFF7E6",
        ),
        p("Что получилось особенно хорошо", "H1Ru"),
    ]
    bullets(
        story,
        [
            "Разминка была сильная: отрицательные числа, десятичные коэффициенты и раскрытие скобок решены аккуратно.",
            "В уравнении 0,5x = 3 ты записала важный последний шаг: x = 3 : 0,5 = 6.",
            "Скобки раскрываешь уверенно: 4(x - 2) + 3x = 7x - 8, а минус перед скобкой тоже держится.",
            "Степени поняла хорошо: (-2)^3 = -8, а (-3)^2 = 9.",
            "В задачах на отрезки есть схемы, единицы измерения и ответы словами.",
        ],
    )
    story.append(p("Что надо поправить", "H1Ru"))
    bullets(
        story,
        [
            "В неравенстве -3x >= 12 нужно не только проверить числа, а записать полный ответ: x <= -4.",
            "В тождествах важно уметь сказать 'не равны'. Например, 5(x + 1) и 5x + 1 при x = 2 дают 15 и 11, значит это не тождество.",
            "В геометрии рисунок - это половина решения. Вторая половина - правильно назвать: прямая AB, отрезок CD, луч OA.",
        ],
    )
    story.append(p("Куда идём дальше", "H1Ru"))
    story.append(
        callout(
            "Следующий день - одночлены. Это продолжение степеней: будем находить коэффициент и приводить выражения вроде 2x * 4x к виду 8x^2.",
            "#EDF7ED",
        )
    )
    doc(CHILD_FEEDBACK, "Обратная связь День 40").build(story, onFirstPage=footer, onLaterPages=footer)


def parent_feedback() -> None:
    story = [
        p("День 40. Обратная связь для родителя", "TitleRu"),
        callout(
            "Общий вывод: старт 7 класса можно продолжать. База по скобкам и степеням достаточная для перехода к одночленам, но тождества и неравенства нужно держать короткой разминкой.",
            "#FFF7E6",
        ),
        p("Наблюдения по работе", "H1Ru"),
    ]
    bullets(
        story,
        [
            "Разминка: 7 - 12 + 5, 12,5x - 1,2x - 0,8x, раскрытие скобок и уравнение с 0,5x выполнены хорошо.",
            "Неравенство -3x >= 12 проверялось подстановкой, но не доведено до полного ответа x <= -4.",
            "В тождествах 1, 2, 4, 5 логика подстановки верная. В номере 3 ошибка: 5(x + 1) и 5x + 1 не равны.",
            "Степени решены уверенно, включая отрицательное основание в скобках.",
            "Геометрия: схемы на отрезки хорошие, единицы измерения записаны. Нужно закреплять словесные названия объектов.",
        ],
    )
    story.append(p("Что проверить в следующем дне", "H1Ru"))
    bullets(
        story,
        [
            "Одночлен: ребёнок отличает коэффициент от буквенной части.",
            "Стандартный вид: числа перемножены отдельно, буквы и степени собраны отдельно.",
            "Неравенства: ответ записан как условие, а не только проверка чисел.",
            "Тождества: если при подстановке получились разные числа, обязательно написано 'не равны'.",
            "Геометрия: в рисунке угла вершина стоит посередине в названии, например угол AOB.",
        ],
    )
    story.append(p("Рекомендация на День 41", "H1Ru"))
    story.append(
        p(
            "Дать ровно одну лекцию: Блок 5 из independent_math_course_materials_v2.md, 'Одночлены'. "
            "Геометрию сегодня вести по мини-конспекту в листе, без второго видео.",
            "BodyRu",
        )
    )
    doc(PARENT_FEEDBACK, "Обратная связь День 40 для родителя").build(story, onFirstPage=footer, onLaterPages=footer)


def tasks() -> None:
    story = [
        p("День 41. Одночлены + углы", "TitleRu"),
        p("Для Настюшика. Время: 45-55 минут. Без калькулятора.", "SubRu"),
        callout(
            "Обязательная лекция дня: Блок 5 из independent_math_course_materials_v2.md - Одночлены. "
            "Ссылка: https://interneturok.ru/h/biblioteka/algebra/7-klass/ponyatie-odnochlena-standartniy-vid-odnochlena/1\n"
            "Смотреть только эту лекцию: до примеров про коэффициент и стандартный вид одночлена. Геометрию сегодня делаем по мини-конспекту ниже, без второго видео.",
            "#EDF7ED",
        ),
        p("Блок 1. Разминка: две ловушки Дня 40", "H1Ru"),
    ]
    add_tasks(
        story,
        [
            "Проверь при x = 2: 5(x + 1) и 5x + 1. Равны или не равны?",
            "Проверь при x = 2: 3(x - 4) и 3x - 12. Равны или не равны?",
            "Реши неравенство: -2x >= 10.",
            "Реши неравенство: -0,5x < 3.",
        ],
    )
    story.append(p("Блок 2. Одночлен: коэффициент и буквенная часть", "H1Ru"))
    story.append(callout("Одночлен - это произведение чисел, букв и степеней. В 7x^2y коэффициент 7, буквенная часть x^2y."))
    story.append(p("Подчеркни коэффициент и отдельно выпиши буквенную часть.", "BodyRu"))
    add_tasks(story, ["5x", "-3a^2", "0,8mn", "-xy", "4x^2y"])

    story.append(p("Блок 3. Приведи одночлен к стандартному виду", "H1Ru"))
    story.append(p("Сначала перемножь числа, потом собери одинаковые буквы.", "BodyRu"))
    add_tasks(
        story,
        [
            "2x * 4x =",
            "3a * 5a^2 =",
            "-2m * 6m =",
            "0,5x * 8x^2 =",
            "-3ab * 2a =",
            "4xy * (-2y) =",
        ],
    )
    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_tasks(
        story,
        [
            "Раскрой скобки: -3(x + 5) =",
            "Реши уравнение: 4x = 18. Не забудь строку деления.",
            "Запиши как произведение: (3a)^2.",
            "Вычисли: (-4)^2.",
        ],
    )

    story.append(p("Блок 5. Геометрия: угол", "H1Ru"))
    story.append(callout("Угол состоит из двух лучей с общим началом. В названии угла вершина всегда посередине: угол AOB, вершина O."))
    add_tasks(
        story,
        [
            "Нарисуй угол AOB. Подпиши вершину.",
            "Нарисуй острый угол.",
            "Нарисуй прямой угол.",
            "Если угол AOB = 40°, угол BOC = 30°, а луч OB внутри угла AOC, найди угол AOC.",
            "Если угол AOC = 90°, угол AOB = 35°, а луч OB внутри угла AOC, найди угол BOC.",
        ],
    )
    story.append(p("Вопрос в конце", "H1Ru"))
    story.append(p("Что было понятнее: коэффициент одночлена или название угла? Где запуталась?", "TaskRu"))
    doc(TASKS, "День 41 задания").build(story, onFirstPage=footer, onLaterPages=footer)


def answers() -> None:
    story = [
        p("День 41. Ответы и акценты для проверки", "TitleRu"),
        callout(
            "Главный акцент: одночлен приводится к стандартному виду через два шага - числа отдельно, буквенная часть отдельно. Неравенства по-прежнему должны заканчиваться ответом в виде условия.",
            "#FFF7E6",
        ),
        p("Блок 1. Разминка", "H1Ru"),
    ]
    add_tasks(
        story,
        [
            "При x = 2: 5 * 3 = 15, а 5 * 2 + 1 = 11. Не равны.",
            "При x = 2: 3 * (-2) = -6, а 6 - 12 = -6. Равны.",
            "-2x >= 10 -> x <= -5. Знак поменялся.",
            "-0,5x < 3 -> x > -6. Знак поменялся.",
        ],
    )
    story.append(p("Блок 2. Коэффициент и буквенная часть", "H1Ru"))
    add_tasks(
        story,
        [
            "5x: коэффициент 5, буквенная часть x.",
            "-3a^2: коэффициент -3, буквенная часть a^2.",
            "0,8mn: коэффициент 0,8, буквенная часть mn.",
            "-xy: коэффициент -1, буквенная часть xy.",
            "4x^2y: коэффициент 4, буквенная часть x^2y.",
        ],
    )
    story.append(p("Блок 3. Стандартный вид", "H1Ru"))
    add_tasks(
        story,
        [
            "2x * 4x = 8x^2.",
            "3a * 5a^2 = 15a^3.",
            "-2m * 6m = -12m^2.",
            "0,5x * 8x^2 = 4x^3.",
            "-3ab * 2a = -6a^2b.",
            "4xy * (-2y) = -8xy^2.",
        ],
    )
    story.append(p("Блок 4. Мини-смешанный блок", "H1Ru"))
    add_tasks(
        story,
        [
            "-3(x + 5) = -3x - 15.",
            "4x = 18 -> x = 18 : 4 = 4,5.",
            "(3a)^2 = 3a * 3a.",
            "(-4)^2 = 16.",
        ],
    )
    story.append(p("Блок 5. Геометрия", "H1Ru"))
    add_tasks(
        story,
        [
            "Должны быть два луча OA и OB с общей вершиной O.",
            "Острый угол меньше 90°.",
            "Прямой угол равен 90°.",
            "AOC = AOB + BOC = 40° + 30° = 70°.",
            "BOC = AOC - AOB = 90° - 35° = 55°.",
        ],
    )
    story.append(p("Что считать успехом", "H1Ru"))
    bullets(
        story,
        [
            "В заданиях с одночленами коэффициент указан вместе со знаком.",
            "В -xy коэффициент записан как -1, а не как 0 или пусто.",
            "В произведениях степеней буквы собраны: x * x^2 = x^3.",
            "В неравенствах с отрицательным множителем знак перевернут.",
            "В угле AOB вершина O стоит посередине.",
        ],
    )
    doc(ANSWERS, "День 41 ответы").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        path.parent.mkdir(parents=True, exist_ok=True)
    child_feedback()
    parent_feedback()
    tasks()
    answers()
    for path in [CHILD_FEEDBACK, PARENT_FEEDBACK, TASKS, ANSWERS]:
        print(path)
