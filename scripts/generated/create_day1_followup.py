from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

out = '/mnt/data/posle_dnya1_zadaniya_dlya_rebenka.pdf'
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', font_path))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', bold_path))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRu', parent=styles['Title'], fontName='DejaVu-Bold', fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name='H1Ru', parent=styles['Heading1'], fontName='DejaVu-Bold', fontSize=13, leading=16, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='H2Ru', parent=styles['Heading2'], fontName='DejaVu-Bold', fontSize=11.5, leading=14, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyRu', parent=styles['BodyText'], fontName='DejaVu', fontSize=10.5, leading=14, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallRu', parent=styles['BodyText'], fontName='DejaVu', fontSize=9.2, leading=12, spaceAfter=3))
styles.add(ParagraphStyle(name='TaskRu', parent=styles['BodyText'], fontName='DejaVu', fontSize=10.5, leading=15, spaceAfter=4))
styles.add(ParagraphStyle(name='FormulaRu', parent=styles['BodyText'], fontName='DejaVu', fontSize=11, leading=15, leftIndent=8, spaceAfter=4))


def P(text, style='BodyRu'):
    return Paragraph(text, styles[style])

story = []
story.append(P('Работа после Дня 1: дроби и действия с ними', 'TitleRu'))
story.append(P('Цель: исправить две типичные ошибки и научиться решать кусок выражения из контрольной без путаницы.', 'BodyRu'))

# rules box
rules = [
    [P('<b>Правила на сегодня</b>', 'BodyRu')],
    [P('1. Без калькулятора. 2. Каждую десятичную дробь сначала переводи в обыкновенную. 3. Сокращай до конца. 4. После деления проверяй: ответ должен быть разумного размера.', 'SmallRu')]
]
t = Table(rules, colWidths=[170*mm])
t.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(t)
story.append(Spacer(1, 6))

story.append(P('Блок 1. Исправь ошибки первого дня', 'H1Ru'))
story.append(P('Запиши через дробь со знаменателем 1000 или 100, затем сократи до конца.', 'BodyRu'))
items = [
    '1) 0,625 =', '2) 0,375 =', '3) 0,875 =', '4) 0,125 =', '5) 1,625 =', '6) 2,375 ='
]
rows=[]
for i in range(0,len(items),2):
    rows.append([P(items[i] + ' ________________________________', 'TaskRu'), P(items[i+1] + ' ________________________________', 'TaskRu')])
t=Table(rows, colWidths=[85*mm,85*mm], rowHeights=[15*mm]*3)
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(t)

story.append(P('Блок 2. Переведи в дроби и выполни действие', 'H1Ru'))
story.append(P('Сначала сделай перевод, потом считай. Десятичные дроби столбиком не делить.', 'BodyRu'))
items = [
    '1) 0,625 · 4/5 =', '2) 0,375 · 8/3 =', '3) 2,0625 · 4/25 =',
    '4) 6,72 : 6,4 =', '5) 0,025 · 40 =', '6) 1,25 : 0,5 ='
]
for item in items:
    story.append(P(item, 'TaskRu'))
    story.append(Spacer(1, 8))

story.append(P('Блок 3. Сокращай перед умножением', 'H1Ru'))
story.append(P('Сокращай крест-накрест до умножения. Не перемножай сразу большие числа.', 'BodyRu'))
items = [
    '1) 33/16 · 4/25 =', '2) 168/25 · 5/32 =', '3) 25/4 · 69/50 =',
    '4) 15/8 · 16/5 =', '5) 7/20 · 100/14 =', '6) 27/40 · 80/9 ='
]
for item in items:
    story.append(P(item, 'TaskRu'))
    story.append(Spacer(1, 7))

story.append(PageBreak())
story.append(P('Блок 4. Деление дробей', 'H1Ru'))
story.append(P('Перед каждым примером вспомни правило: чтобы разделить на дробь, умножаю на обратную.', 'BodyRu'))
items = [
    '1) 3/4 : 1/2 =', '2) 5/8 : 5/4 =', '3) 7/10 : 0,7 =',
    '4) 6,72 : 6,4 =', '5) 1,25 : 0,25 =', '6) 2,4 : 0,6 ='
]
for item in items:
    story.append(P(item, 'TaskRu'))
    story.append(Spacer(1, 9))

story.append(P('Блок 5. Собери выражение из контрольной по частям', 'H1Ru'))
story.append(P('Решай строго по шагам. Каждый шаг на новой строке.', 'BodyRu'))
items = [
    '1) 2,0625 · 4/25 =',
    '2) 6,72 : 6,4 =',
    '3) 2,0625 · 4/25 + 6,72 : 6,4 =',
    '4) 6 1/4 · (2,0625 · 4/25 + 6,72 : 6,4) =',
    '5) 6 3/4 + 6 1/4 · (2,0625 · 4/25 + 6,72 : 6,4) ='
]
for item in items:
    story.append(P(item, 'TaskRu'))
    story.append(Spacer(1, 12))

story.append(P('Блок 6. Проверка смысла ответа', 'H1Ru'))
story.append(P('Сначала напиши словами: ответ меньше 1, около 1, больше 1 или намного больше 1. Потом считай.', 'BodyRu'))
items = [
    '1) 6,72 : 6,4', '2) 0,25 · 0,4', '3) 2,0625 · 4/25',
    '4) 15 : 0,5', '5) 0,625 · 8', '6) 1200 : 60'
]
for item in items:
    story.append(P(item + '  → сначала оценка: ____________________  ответ: ____________________', 'TaskRu'))

story.append(PageBreak())
story.append(P('Блок 7. Задача на движение: не перепутай скорости', 'H1Ru'))
story.append(P('Из двух посёлков в одном направлении выехали два велосипедиста. Скорость первого велосипедиста 90 м/мин, что составляет 3/5 скорости второго. Через сколько времени второй велосипедист догонит первого, если расстояние между посёлками 1200 м?', 'BodyRu'))
story.append(Spacer(1, 4))
story.append(P('1) Найди скорость второго велосипедиста:', 'TaskRu'))
story.append(Spacer(1, 16))
story.append(P('2) Найди скорость сближения. Подчеркни правильный вариант:', 'TaskRu'))
story.append(P('едут навстречу - складываем скорости; &nbsp;&nbsp; догоняет - вычитаем скорости', 'FormulaRu'))
story.append(Spacer(1, 16))
story.append(P('3) Найди время:', 'TaskRu'))
story.append(Spacer(1, 16))
story.append(P('Ответ: __________________________________________________________', 'TaskRu'))

story.append(Spacer(1, 10))
final_box = [
    [P('<b>Мини-проверка в конце</b>', 'BodyRu')],
    [P('Если без подсказки получились эти четыре результата, день засчитан:', 'SmallRu')],
    [P('2,0625 · 4/25 = 33/100; 6,72 : 6,4 = 21/20; 25/4 · 69/50 = 69/8; задача на движение = 20 мин.', 'SmallRu')]
]
t = Table(final_box, colWidths=[170*mm])
t.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(t)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DejaVu', 8)
    canvas.drawRightString(A4[0]-18*mm, 10*mm, f'Страница {doc.page}')
    canvas.restoreState()

pdf = SimpleDocTemplate(out, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
pdf.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
