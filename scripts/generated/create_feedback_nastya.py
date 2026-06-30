from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

out = '/mnt/data/obratnaya_svyaz_den1_Nastyushik.pdf'
font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', font))
pdfmetrics.registerFont(TTFont('DejaVuBold', font_bold))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRu', fontName='DejaVuBold', fontSize=20, leading=24, alignment=1, textColor=colors.HexColor('#243b53'), spaceAfter=8))
styles.add(ParagraphStyle(name='SubTitleRu', fontName='DejaVu', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#52616b'), spaceAfter=14))
styles.add(ParagraphStyle(name='H1Ru', fontName='DejaVuBold', fontSize=14, leading=18, textColor=colors.HexColor('#1f3a5f'), spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name='BodyRu', fontName='DejaVu', fontSize=10.5, leading=15, textColor=colors.HexColor('#1b1b1b'), spaceAfter=5))
styles.add(ParagraphStyle(name='SmallRu', fontName='DejaVu', fontSize=9.5, leading=13, textColor=colors.HexColor('#333333')))
styles.add(ParagraphStyle(name='GoodRu', fontName='DejaVuBold', fontSize=11, leading=15, textColor=colors.HexColor('#1b6b3a'), spaceAfter=5))
styles.add(ParagraphStyle(name='FocusRu', fontName='DejaVuBold', fontSize=11, leading=15, textColor=colors.HexColor('#9a4d00'), spaceAfter=5))
styles.add(ParagraphStyle(name='FormulaRu', fontName='DejaVu', fontSize=10.5, leading=14, leftIndent=8, textColor=colors.HexColor('#202124'), backColor=colors.HexColor('#f4f7fb'), borderPadding=5, spaceAfter=5))


def P(txt, style='BodyRu'):
    return Paragraph(txt, styles[style])

def bullet(txt):
    return Paragraph('• ' + txt, styles['BodyRu'])

story = []
story.append(P('Настюшик, обратная связь по Дню 1', 'TitleRu'))
story.append(P('Тема: десятичные дроби, обыкновенные дроби, сокращение и первое большое выражение.', 'SubTitleRu'))

story.append(P('Главный итог', 'H1Ru'))
story.append(P('Настюшик, ты хорошо продвинулась. Самое важное: ты уже научилась переводить многие десятичные дроби в обыкновенные и начала правильно использовать это в большом примере. Это именно тот навык, который нужен для задач с дробями.', 'BodyRu'))

story.append(P('Что получилось особенно хорошо', 'H1Ru'))
for t in [
    'Быстро и правильно переведены простые дроби: 0,5 = 1/2, 0,25 = 1/4, 0,75 = 3/4, 0,2 = 1/5.',
    'Верно получились важные дроби для контрольной: 2,0625 = 33/16, 6,72 = 168/25, 6,4 = 32/5.',
    'Ты правильно поняла задачу на догоняющего велосипедиста: скорости надо вычитать, а не складывать.',
    'В большом выражении ты соблюдала порядок действий: сначала скобка, потом умножение, потом прибавление.'
]:
    story.append(bullet(t))

story.append(Spacer(1, 4*mm))
story.append(P('Оценка навыков после Дня 1', 'H1Ru'))
data = [
    [P('Навык', 'SmallRu'), P('Оценка', 'SmallRu'), P('Комментарий', 'SmallRu')],
    [P('Простые десятичные дроби', 'SmallRu'), P('уверенно', 'GoodRu'), P('0,5; 0,25; 0,75; 0,2; 0,4; 0,6; 0,8 получаются хорошо.', 'SmallRu')],
    [P('Дроби с тысячными', 'SmallRu'), P('надо закрепить', 'FocusRu'), P('0,625 и 0,375 нужно сокращать до конца: 5/8 и 3/8.', 'SmallRu')],
    [P('Сокращение дробей', 'SmallRu'), P('средне+', 'SmallRu'), P('Идея понятна, но иногда остановка происходит раньше полной несократимой дроби.', 'SmallRu')],
    [P('Действия с дробями', 'SmallRu'), P('следующая цель', 'FocusRu'), P('Нужно тренировать умножение, деление и сокращение перед умножением.', 'SmallRu')],
    [P('Текстовые задачи', 'SmallRu'), P('улучшение', 'GoodRu'), P('В задаче на движение уже выбрана правильная модель: догоняет - значит разность скоростей.', 'SmallRu')],
]
t = Table(data, colWidths=[45*mm, 32*mm, 95*mm])
t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), 'DejaVu'),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8f0fe')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1f3a5f')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#c9d6e2')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)

story.append(P('Две ошибки, которые надо исправить', 'H1Ru'))
story.append(P('1) 0,625 надо довести до конца:', 'BodyRu'))
story.append(P('0,625 = 625/1000 = 5/8', 'FormulaRu'))
story.append(P('2) 0,375 тоже надо довести до конца:', 'BodyRu'))
story.append(P('0,375 = 375/1000 = 3/8', 'FormulaRu'))
story.append(P('Правило: если дробь можно сократить еще - сокращаем. Ответ должен быть несократимой дробью.', 'BodyRu'))

story.append(P('Отдельная похвала за большой пример', 'H1Ru'))
story.append(P('В большом выражении ты дошла до правильного ответа. Это сильный результат, потому что пример длинный и в нем есть десятичные дроби, смешанные числа, умножение, деление и скобки.', 'BodyRu'))
story.append(P('Правильная цепочка:', 'BodyRu'))
story.append(P('2,0625 · 4/25 = 33/100 = 0,33<br/>6,72 : 6,4 = 21/20 = 1,05<br/>0,33 + 1,05 = 1,38<br/>6 1/4 · 1,38 = 8,625<br/>6 3/4 + 8,625 = 15,375', 'FormulaRu'))

story.append(PageBreak())
story.append(P('На что обращать внимание дальше', 'H1Ru'))
for t in [
    'Перед умножением дробей сначала ищи, что можно сократить крест-накрест.',
    'При делении дробей обязательно меняй деление на умножение на обратную дробь.',
    'После ответа проверяй размер: например, 6,72 : 6,4 должно быть чуть больше 1, а не 10.',
    'В задачах на движение сначала решай, скорости складываются или вычитаются.'
]:
    story.append(bullet(t))

story.append(P('Твой личный чек-лист перед сдачей работы', 'H1Ru'))
for t in [
    'Я сократила дробь до конца?',
    'Я не потеряла ноль в десятичной дроби?',
    'Я правильно заменила деление на умножение?',
    'Я проверила, примерно какого размера должен быть ответ?',
    'Я написала ответ словами, если это задача?'
]:
    story.append(bullet(t))

story.append(P('Короткая цель на День 2', 'H1Ru'))
story.append(P('Настюшик, твоя цель на следующий день - не просто переводить дроби, а уверенно выполнять действия с ними: умножать, делить, сокращать и проверять размер ответа.', 'BodyRu'))
story.append(P('Мини-цель: без подсказок решить цепочку', 'BodyRu'))
story.append(P('2,0625 · 4/25 = 33/100<br/>6,72 : 6,4 = 21/20<br/>33/100 + 21/20 = 69/50<br/>6 1/4 · 69/50 = 69/8<br/>6 3/4 + 69/8 = 123/8 = 15,375', 'FormulaRu'))

story.append(P('Финальное сообщение', 'H1Ru'))
story.append(P('Настюшик, ты молодец: у тебя уже есть понимание, осталось натренировать аккуратность и сокращение. Главное сейчас - писать чисто, не спешить и проверять каждый шаг.', 'BodyRu'))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DejaVu', 8)
    canvas.setFillColor(colors.HexColor('#6b7280'))
    canvas.drawRightString(A4[0]-18*mm, 10*mm, f'Страница {doc.page}')
    canvas.restoreState()

doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
