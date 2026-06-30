from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT

FONT_REG = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', FONT_REG))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', FONT_BOLD))

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='TitleRu', parent=styles['Title'], fontName='NotoSans-Bold', fontSize=18, leading=22,
    alignment=TA_CENTER, spaceAfter=8
))
styles.add(ParagraphStyle(
    name='SubRu', parent=styles['Normal'], fontName='NotoSans', fontSize=10.5, leading=14,
    alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceAfter=8
))
styles.add(ParagraphStyle(
    name='H1Ru', parent=styles['Heading1'], fontName='NotoSans-Bold', fontSize=13, leading=16,
    spaceBefore=8, spaceAfter=6, textColor=colors.HexColor('#1f2937')
))
styles.add(ParagraphStyle(
    name='H2Ru', parent=styles['Heading2'], fontName='NotoSans-Bold', fontSize=11.5, leading=14,
    spaceBefore=6, spaceAfter=4, textColor=colors.HexColor('#1f2937')
))
styles.add(ParagraphStyle(
    name='BodyRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=10.2, leading=14,
    spaceAfter=4
))
styles.add(ParagraphStyle(
    name='SmallRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=9, leading=12,
    textColor=colors.HexColor('#444444'), spaceAfter=3
))
styles.add(ParagraphStyle(
    name='BoxRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=10, leading=14,
    leftIndent=4, rightIndent=4, spaceBefore=2, spaceAfter=2
))
styles.add(ParagraphStyle(
    name='FormulaRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=11, leading=15,
    spaceAfter=3
))

def p(text, style='BodyRu'):
    return Paragraph(text.replace('\n', '<br/>'), styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSans', 8)
    canvas.setFillColor(colors.HexColor('#777777'))
    canvas.drawString(MARGIN, 10*mm, 'День 2: действия с дробями')
    canvas.drawRightString(PAGE_W-MARGIN, 10*mm, f'стр. {doc.page}')
    canvas.restoreState()

def box(story, lines, title=None):
    data = []
    if title:
        data.append([Paragraph(title, styles['H2Ru'])])
    data.append([Paragraph('<br/>'.join(lines), styles['BoxRu'])])
    t = Table(data, colWidths=[PAGE_W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 5))

def numbered_items(items, col_widths=None, font_size=10.5):
    data = []
    for i, item in enumerate(items, 1):
        data.append([Paragraph(f'{i})', styles['BodyRu']), Paragraph(item, styles['FormulaRu'])])
    if col_widths is None:
        col_widths = [10*mm, PAGE_W - 2*MARGIN - 10*mm]
    t = Table(data, colWidths=col_widths, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    return t

def two_col_items(items):
    left = items[: (len(items)+1)//2]
    right = items[(len(items)+1)//2:]
    maxn = max(len(left), len(right))
    data=[]
    for r in range(maxn):
        row=[]
        for part, offset in [(left,0),(right,len(left))]:
            if r < len(part):
                row += [Paragraph(f'{r+1+offset})', styles['BodyRu']), Paragraph(part[r], styles['FormulaRu'])]
            else:
                row += ['', '']
        data.append(row)
    t=Table(data, colWidths=[8*mm, 77*mm, 8*mm, 77*mm], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),2),
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    return t

# ---------------- TASKS ----------------
tasks=[]
tasks.append(p('День 2. Действия с дробями', 'TitleRu'))
tasks.append(p('Фокус: перевод десятичных дробей, умножение и деление дробей, сокращение перед умножением, контроль размера ответа.', 'SubRu'))
box(tasks, [
    'Правило 1. Десятичную дробь сначала переведи в обыкновенную.',
    'Правило 2. При умножении дробей сначала сокращай крест-накрест.',
    'Правило 3. При делении на дробь умножай на обратную.',
    'Правило 4. После ответа проверь размер: должен ли ответ быть около 1, меньше 1 или больше 1?'
], 'Перед началом')

tasks.append(p('Блок 1. Исправление ошибок дня 1', 'H1Ru'))
tasks.append(p('Переведи в обыкновенные дроби и сократи до конца.', 'BodyRu'))
tasks.append(two_col_items(['0,625 =', '0,375 =', '0,875 =', '0,125 =', '1,625 =', '2,375 =']))

tasks.append(p('Блок 2. Перевод в дроби перед действием', 'H1Ru'))
tasks.append(p('Сначала переведи десятичные дроби в обыкновенные. Потом выполни действие. Столбиком не считать.', 'BodyRu'))
tasks.append(two_col_items(['0,625 · 4/5 =', '0,375 · 8/3 =', '2,0625 · 4/25 =', '6,72 : 6,4 =', '0,025 · 40 =', '1,25 : 0,5 =']))

tasks.append(p('Блок 3. Сокращение перед умножением', 'H1Ru'))
tasks.append(p('Реши с обязательным сокращением до умножения.', 'BodyRu'))
tasks.append(two_col_items(['33/16 · 4/25 =', '168/25 · 5/32 =', '25/4 · 69/50 =', '15/8 · 16/5 =', '7/20 · 100/14 =', '27/40 · 80/9 =']))

tasks.append(PageBreak())
tasks.append(p('Блок 4. Деление дробей', 'H1Ru'))
tasks.append(p('Перед каждым примером проговори: «Чтобы разделить на дробь, умножаю на обратную».', 'BodyRu'))
tasks.append(two_col_items(['3/4 : 1/2 =', '5/8 : 5/4 =', '7/10 : 0,7 =', '6,72 : 6,4 =', '1,25 : 0,25 =', '2,4 : 0,6 =']))

tasks.append(p('Блок 5. Мини-выражения как в КР №2', 'H1Ru'))
tasks.append(p('Решай по действиям. Каждое действие - на отдельной строке.', 'BodyRu'))
tasks.append(numbered_items([
    '2,0625 · 4/25 + 6,72 : 6,4 =',
    '6 1/4 · 1,38 =',
    '6 3/4 + 8,625 =',
    '6 3/4 + 6 1/4 · 1,38 ='
]))

tasks.append(p('Блок 6. Контроль смысла ответа', 'H1Ru'))
tasks.append(p('Сначала без точного решения напиши: «меньше 1», «около 1», «больше 1» или «намного больше 1». Потом можешь посчитать.', 'BodyRu'))
tasks.append(two_col_items(['6,72 : 6,4', '0,25 · 0,4', '2,0625 · 4/25', '15 : 0,5', '0,625 · 8', '1200 : 60']))

box(tasks, [
    'Минимум на сегодня: Блок 1 весь; Блок 2 №3-6; Блок 3 №1-3; Блок 5 весь.',
    'День засчитан, если без подсказок получаются: 33/100, 21/20, 69/8, 123/8.'
], 'Критерий успеха')

# ---------------- ANSWERS ----------------
answers=[]
answers.append(p('День 2. Ответы и акценты для проверки', 'TitleRu'))
answers.append(p('Проверяйте не только ответ, но и цепочку: перевод дробей, сокращение, порядок действий, контроль размера.', 'SubRu'))
box(answers, [
    'Главные ошибки, за которыми следить:',
    '1) 0,625 = 5/8, а не 25/40.',
    '2) 0,375 = 3/8, а не 15/40.',
    '3) 6,72 : 6,4 должно быть чуть больше 1, а не 10 и не 0,1.',
    '4) В примерах с умножением сначала сокращаем, потом перемножаем.'
], 'Акценты')

answers.append(p('Блок 1. Ответы', 'H1Ru'))
answers.append(two_col_items(['0,625 = 625/1000 = 5/8', '0,375 = 375/1000 = 3/8', '0,875 = 875/1000 = 7/8', '0,125 = 125/1000 = 1/8', '1,625 = 1 625/1000 = 1 5/8 = 13/8', '2,375 = 2 375/1000 = 2 3/8 = 19/8']))

answers.append(p('Блок 2. Ответы', 'H1Ru'))
answers.append(numbered_items([
    '0,625 · 4/5 = 5/8 · 4/5 = 1/2',
    '0,375 · 8/3 = 3/8 · 8/3 = 1',
    '2,0625 · 4/25 = 33/16 · 4/25 = 33/100 = 0,33',
    '6,72 : 6,4 = 168/25 : 32/5 = 168/25 · 5/32 = 21/20 = 1,05',
    '0,025 · 40 = 1/40 · 40 = 1',
    '1,25 : 0,5 = 5/4 : 1/2 = 5/4 · 2 = 5/2 = 2,5'
]))

answers.append(p('Блок 3. Ответы', 'H1Ru'))
answers.append(numbered_items([
    '33/16 · 4/25 = 33/100',
    '168/25 · 5/32 = 21/20',
    '25/4 · 69/50 = 69/8 = 8,625',
    '15/8 · 16/5 = 6',
    '7/20 · 100/14 = 5/2 = 2,5',
    '27/40 · 80/9 = 6'
]))

answers.append(PageBreak())
answers.append(p('Блок 4. Ответы', 'H1Ru'))
answers.append(numbered_items([
    '3/4 : 1/2 = 3/4 · 2 = 3/2 = 1,5',
    '5/8 : 5/4 = 5/8 · 4/5 = 1/2',
    '7/10 : 0,7 = 7/10 : 7/10 = 1',
    '6,72 : 6,4 = 21/20 = 1,05',
    '1,25 : 0,25 = 5/4 : 1/4 = 5',
    '2,4 : 0,6 = 24/10 : 6/10 = 4'
]))

answers.append(p('Блок 5. Ответы', 'H1Ru'))
answers.append(numbered_items([
    '2,0625 · 4/25 + 6,72 : 6,4 = 33/100 + 21/20 = 33/100 + 105/100 = 138/100 = 69/50 = 1,38',
    '6 1/4 · 1,38 = 25/4 · 69/50 = 69/8 = 8,625',
    '6 3/4 + 8,625 = 27/4 + 69/8 = 54/8 + 69/8 = 123/8 = 15,375',
    '6 3/4 + 6 1/4 · 1,38 = 27/4 + 69/8 = 123/8 = 15,375'
]))

answers.append(p('Блок 6. Оценка размера ответа', 'H1Ru'))
answers.append(numbered_items([
    '6,72 : 6,4 - чуть больше 1. Точный ответ: 1,05.',
    '0,25 · 0,4 - меньше 1. Точный ответ: 0,1.',
    '2,0625 · 4/25 - меньше 1. Точный ответ: 0,33.',
    '15 : 0,5 - намного больше 1. Точный ответ: 30.',
    '0,625 · 8 - больше 1. Точный ответ: 5.',
    '1200 : 60 - намного больше 1. Точный ответ: 20.'
]))

box(answers, [
    'Ставьте плюс за чистую запись, даже если ответ не сразу получился.',
    'Если ребёнок получил 6,72 : 6,4 = 10,5, остановить и спросить: «6,72 во сколько раз больше 6,4?». Ответ должен быть около 1.',
    'Если ребёнок перемножает большие числа, напомнить: сначала сокращение крест-накрест.'
], 'Как проверять')


def build(path, story):
    doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN, topMargin=13*mm, bottomMargin=17*mm)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

build('/mnt/data/den2_zadaniya_drobi.pdf', tasks)
build('/mnt/data/den2_otvety_i_akcenty.pdf', answers)
print('[OK] PDFs written')
