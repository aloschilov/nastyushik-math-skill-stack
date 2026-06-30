from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

out = '/mnt/data/den2_dlya_rebenka_po_itogam_dnya1.pdf'
font = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
bold = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', font))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', bold))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRu', fontName='NotoSans-Bold', fontSize=18, leading=22, alignment=1, spaceAfter=8))
styles.add(ParagraphStyle(name='H1Ru', fontName='NotoSans-Bold', fontSize=13, leading=16, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name='BodyRu', fontName='NotoSans', fontSize=10.5, leading=14, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallRu', fontName='NotoSans', fontSize=9, leading=12, textColor=colors.HexColor('#333333')))
styles.add(ParagraphStyle(name='TaskRu', fontName='NotoSans', fontSize=11, leading=16, leftIndent=4, spaceAfter=3))
styles.add(ParagraphStyle(name='BoxRu', fontName='NotoSans-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#222222')))

doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm)
story = []

story.append(Paragraph('День 2. Действия с дробями', styles['TitleRu']))
story.append(Paragraph('Задания по результатам первого дня', styles['BodyRu']))

checks = [
    ['Что важно сегодня', '1) сокращать дроби до конца; 2) делить дроби через обратную; 3) перед вычислением десятичные дроби переводить в обыкновенные; 4) проверять, похож ли ответ на правду.'],
    ['Как писать', 'Каждое действие - с новой строки. Сначала сокращение, потом умножение. Без калькулятора.']
]
t = Table([[Paragraph(a, styles['BoxRu']), Paragraph(b, styles['SmallRu'])] for a,b in checks], colWidths=[42*mm, 116*mm])
t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.8,colors.black),('INNERGRID',(0,0),(-1,-1),0.4,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#eeeeee')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(t)
story.append(Spacer(1, 6))

sections = [
('Блок 1. Исправь ошибки первого дня', [
'1) 0,625 =', '2) 0,375 =', '3) 0,875 =', '4) 0,125 =', '5) 1,625 =', '6) 2,375 ='
], 'Записывай так: 0,625 = 625/1000 = ...'),
('Блок 2. Сначала переведи в дроби, потом посчитай', [
'1) 0,625 * 4/5', '2) 0,375 * 8/3', '3) 2,0625 * 4/25', '4) 6,72 : 6,4', '5) 0,025 * 40', '6) 1,25 : 0,5'
], 'Не считай столбиком. Сначала сделай обыкновенные дроби.'),
('Блок 3. Сократи перед умножением', [
'1) 33/16 * 4/25', '2) 168/25 * 5/32', '3) 25/4 * 69/50', '4) 15/8 * 16/5', '5) 7/20 * 100/14', '6) 27/40 * 80/9'
], 'Сначала сокращай крест-накрест, потом умножай.'),
('Блок 4. Деление дробей', [
'1) 3/4 : 1/2', '2) 5/8 : 5/4', '3) 7/10 : 0,7', '4) 6,72 : 6,4', '5) 1,25 : 0,25', '6) 2,4 : 0,6'
], 'Правило: разделить на дробь - значит умножить на обратную.'),
('Блок 5. Собери выражение из контрольной по частям', [
'1) 2,0625 * 4/25 + 6,72 : 6,4', '2) 6 1/4 * 1,38', '3) 6 3/4 + 8,625', '4) 6 3/4 + 6 1/4 * 1,38'
], 'Порядок действий: скобка, умножение, сложение.'),
('Блок 6. Проверь смысл ответа', [
'Перед точным решением напиши: меньше 1, около 1, больше 1 или намного больше 1.', '1) 6,72 : 6,4', '2) 0,25 * 0,4', '3) 2,0625 * 4/25', '4) 15 : 0,5', '5) 0,625 * 8', '6) 1200 : 60'
], 'Если ответ сильно не похож на ожидаемый размер, ищи ошибку.')
]

for idx,(title,tasks,note) in enumerate(sections):
    story.append(Paragraph(title, styles['H1Ru']))
    story.append(Paragraph(note, styles['SmallRu']))
    for task in tasks:
        story.append(Paragraph(task, styles['TaskRu']))
    if idx in (2,4):
        story.append(PageBreak())
    else:
        story.append(Spacer(1, 5))

story.append(Paragraph('Мини-цель дня', styles['H1Ru']))
story.append(Paragraph('В конце занятия без подсказок решить: 2,0625 * 4/25; 6,72 : 6,4; 25/4 * 69/50; 6 3/4 + 69/8.', styles['BodyRu']))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSans', 8)
    canvas.drawString(16*mm, 8*mm, f'День 2 - задания для ребёнка, стр. {doc.page}')
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
