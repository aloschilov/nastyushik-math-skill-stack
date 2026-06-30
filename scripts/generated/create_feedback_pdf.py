from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import PageBreak
from pathlib import Path

out = Path('/mnt/data/obratnaya_svyaz_den1_dlya_rebenka.pdf')
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_path))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='TitleRu', fontName='DejaVuSans-Bold', fontSize=20, leading=24,
    alignment=TA_CENTER, textColor=colors.HexColor('#1f3a5f'), spaceAfter=8
))
styles.add(ParagraphStyle(
    name='SubTitleRu', fontName='DejaVuSans', fontSize=11, leading=15,
    alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=14
))
styles.add(ParagraphStyle(
    name='H2Ru', fontName='DejaVuSans-Bold', fontSize=14, leading=18,
    textColor=colors.HexColor('#1f3a5f'), spaceBefore=8, spaceAfter=6
))
styles.add(ParagraphStyle(
    name='BodyRu', fontName='DejaVuSans', fontSize=11, leading=16,
    alignment=TA_LEFT, spaceAfter=5
))
styles.add(ParagraphStyle(
    name='BodyBoldRu', fontName='DejaVuSans-Bold', fontSize=11, leading=16,
    alignment=TA_LEFT, spaceAfter=5
))
styles.add(ParagraphStyle(
    name='SmallRu', fontName='DejaVuSans', fontSize=9.5, leading=13,
    textColor=colors.HexColor('#555555')
))
styles.add(ParagraphStyle(
    name='CardTitle', fontName='DejaVuSans-Bold', fontSize=11, leading=14,
    textColor=colors.HexColor('#1f3a5f')
))
styles.add(ParagraphStyle(
    name='CardText', fontName='DejaVuSans', fontSize=10.5, leading=14
))


def P(text, style='BodyRu'):
    return Paragraph(text, styles[style])


def section_box(title, body_items, bg, border):
    parts = [P(title, 'CardTitle')]
    for item in body_items:
        parts.append(P(item, 'CardText'))
    tbl = Table([[parts]], colWidths=[170*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.8, border),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    return tbl


def footer(canvas: Canvas, doc):
    canvas.saveState()
    canvas.setFont('DejaVuSans', 8)
    canvas.setFillColor(colors.HexColor('#777777'))
    canvas.drawRightString(200*mm, 10*mm, f'День 1 - обратная связь | стр. {doc.page}')
    canvas.restoreState()

story = []
story.append(P('Обратная связь по Дню 1', 'TitleRu'))
story.append(P('Тема: десятичные дроби, обыкновенные дроби и первые действия с ними', 'SubTitleRu'))

story.append(section_box('Короткий итог', [
    'Ты хорошо продвинулся: базовые переводы дробей стали получаться увереннее.',
    'Главная цель следующего шага - не просто получить ответ, а записывать решение чисто и проверять, насколько ответ похож на правду.'
], colors.HexColor('#eef6ff'), colors.HexColor('#8ab6e6')))
story.append(Spacer(1, 8))

story.append(P('1. Что получилось хорошо', 'H2Ru'))
good_data = [
    [P('Навык', 'BodyBoldRu'), P('Оценка', 'BodyBoldRu')],
    [P('Простые десятичные дроби', 'CardText'), P('0,5; 0,25; 0,75; 0,2; 0,4; 0,6; 0,8 переведены правильно.', 'CardText')],
    [P('Важные дроби из контрольной', 'CardText'), P('2,0625 = 33/16, 6,72 = 168/25, 6,4 = 32/5 - это большой плюс.', 'CardText')],
    [P('Задача на движение', 'CardText'), P('Исправлено верно: при догоняющем движении надо брать разность скоростей. Ответ 20 минут.', 'CardText')],
    [P('Порядок действий', 'CardText'), P('В большом выражении порядок действий выбран правильно: скобка, потом умножение, потом сложение.', 'CardText')],
]
good_tbl = Table(good_data, colWidths=[48*mm, 122*mm], repeatRows=1)
good_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceeff')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#c7d8e8')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(good_tbl)
story.append(Spacer(1, 8))

story.append(P('2. Что надо поправить', 'H2Ru'))
story.append(section_box('Главные ошибки дня', [
    '<b>0,625</b> надо доводить до конца: 0,625 = 625/1000 = 5/8, а не 25/40.',
    '<b>0,375</b> надо доводить до конца: 0,375 = 375/1000 = 3/8, а не 15/40.',
    'Если дробь можно сократить еще, ответ пока не закончен.',
    'В больших выражениях лучше держать дробь, например 69/8, а не сразу переходить к длинной десятичной записи.'
], colors.HexColor('#fff6e5'), colors.HexColor('#e0b45c')))
story.append(Spacer(1, 8))

story.append(P('3. Правило на завтра', 'H2Ru'))
story.append(section_box('Перед каждым ответом делай 3 проверки', [
    '1) Все десятичные дроби переведены правильно?',
    '2) Дробь сокращена до конца?',
    '3) Ответ по размеру похож на правду? Например, 6,72 : 6,4 должно быть чуть больше 1, а не 10.'
], colors.HexColor('#f0fbef'), colors.HexColor('#8ac486')))

story.append(PageBreak())
story.append(P('Личная карта навыков после Дня 1', 'TitleRu'))
story.append(P('Отметь галочкой, если получается без подсказки', 'SubTitleRu'))

skills = [
    ['Навык', 'Статус', 'Что делать дальше'],
    ['0,5; 0,25; 0,75; 0,2; 0,4; 0,6; 0,8', 'Хорошо', 'Повторять коротко, чтобы не забыть.'],
    ['0,025 = 1/40', 'Хорошо', 'Оставить в ежедневной разминке.'],
    ['2,0625 = 33/16', 'Хорошо', 'Использовать в примере из КР №2.'],
    ['0,625 = 5/8', 'Нужно закрепить', 'Решить 3-4 похожих примера.'],
    ['0,375 = 3/8', 'Нужно закрепить', 'Решить 3-4 похожих примера.'],
    ['Деление дробей', 'Нужно тренировать', 'Деление заменять умножением на обратную дробь.'],
    ['Сокращение перед умножением', 'Нужно тренировать', 'Сначала сокращай, потом умножай.'],
    ['Задачи на движение', 'Стало лучше', 'Запомнить: догоняет - разность скоростей.'],
]
skill_tbl = Table([[P(c, 'BodyBoldRu') for c in skills[0]]] + [[P(c, 'CardText') for c in row] for row in skills[1:]], colWidths=[68*mm, 37*mm, 65*mm], repeatRows=1)
skill_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceeff')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#c7d8e8')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(skill_tbl)
story.append(Spacer(1, 10))

story.append(P('Мини-цель на День 2', 'H2Ru'))
story.append(section_box('Если это получится, день засчитан', [
    'Без подсказок решить цепочку:',
    '2,0625 * 4/25 = 33/100',
    '6,72 : 6,4 = 21/20',
    '33/100 + 21/20 = 69/50',
    '6 1/4 * 69/50 = 69/8',
    '6 3/4 + 69/8 = 123/8 = 15,375'
], colors.HexColor('#eef6ff'), colors.HexColor('#8ab6e6')))
story.append(Spacer(1, 8))

story.append(P('Фраза на сегодня', 'H2Ru'))
story.append(P('Ошибки в дробях - это нормально. Важно не угадывать ответ, а проверять каждый шаг. Сегодня стало лучше: продолжай в том же направлении.', 'BodyRu'))


doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
