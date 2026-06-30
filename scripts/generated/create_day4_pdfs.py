from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from pathlib import Path

OUT = Path('/mnt/data')
font_reg = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
font_bold = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', font_reg))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', font_bold))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRu', parent=styles['Title'], fontName='NotoSans-Bold', fontSize=18, leading=23, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name='H1Ru', parent=styles['Heading1'], fontName='NotoSans-Bold', fontSize=14, leading=18, spaceBefore=8, spaceAfter=6, textColor=HexColor('#1f4e79')))
styles.add(ParagraphStyle(name='H2Ru', parent=styles['Heading2'], fontName='NotoSans-Bold', fontSize=12, leading=16, spaceBefore=6, spaceAfter=4, textColor=HexColor('#333333')))
styles.add(ParagraphStyle(name='BodyRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=10.5, leading=15, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=9.2, leading=13, spaceAfter=3))
styles.add(ParagraphStyle(name='BoxRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=10.5, leading=15, leftIndent=8, rightIndent=8, spaceAfter=6))
styles.add(ParagraphStyle(name='TaskRu', parent=styles['BodyText'], fontName='NotoSans', fontSize=11, leading=17, spaceAfter=5))


def p(txt, style='BodyRu'):
    return Paragraph(txt, styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSans', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(15*mm, 10*mm, 'Настюшик - математика')
    canvas.drawRightString(195*mm, 10*mm, f'стр. {doc.page}')
    canvas.restoreState()

def make_doc(filename, title):
    return SimpleDocTemplate(str(OUT/filename), pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=14*mm, bottomMargin=16*mm, title=title)

def bullet(items):
    story=[]
    for item in items:
        story.append(p('• ' + item, 'BodyRu'))
    return story

def box(text, bg='#eef7ff'):
    t=Table([[p(text, 'BoxRu')]], colWidths=[170*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor(bg)),('BOX',(0,0),(-1,-1),0.6,HexColor('#8bb7d9')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t

# PDF 1 Feedback Day 3
story=[]
story.append(p('Настюшик, итоги Дня 3', 'TitleRu'))
story.append(box('Ты заметно продвинулась: дробное выражение из контрольной теперь получается почти целиком, а задачу на движение ты уже решила правильно. Следующий шаг - научиться решать текстовые задачи с частями и процентами, потому что срок близко: 26 мая.', '#fff7e6'))
story.append(p('Что получилось хорошо', 'H1Ru'))
story += bullet([
    'Десятичные дроби вида 0,875, 0,125, 0,375, 0,625 ты уже переводишь намного увереннее: 0,875 = 7/8, 0,125 = 1/8, 0,375 = 3/8, 0,625 = 5/8.',
    'Деление 6,72 : 6,4 стало получаться правильно: 168/25 : 32/5 = 21/20 = 1,05.',
    'Произведение 2,0625 · 4/25 ты довела до 33/100 = 0,33.',
    'Большое выражение в конце получилось правильно: 15,375.',
    'Задача на движение решена правильно: догоняет - значит берём разность скоростей, 150 - 90 = 60, потом 1200 : 60 = 20 минут.'
])
story.append(p('Что ещё надо подтянуть', 'H1Ru'))
story += bullet([
    'Иногда в середине решения появляется неправильный промежуточный ответ, а потом ты исправляешь его ниже. Это хорошо, что ты исправляешь, но нужно стремиться к одной чистой цепочке.',
    'Смешанные числа лучше записывать аккуратно: 69/8 = 8 5/8 = 8,625. Не теряй целую часть.',
    'Когда складываешь десятичные дроби, следи за запятой: 6,75 + 8,625 = 15,375.',
    'Перед длинным примером полезно сначала прикинуть: если ответ должен быть около 15, а получился 13 или 6, значит нужно искать ошибку.'
])
story.append(p('Оценка навыков после Дня 3', 'H1Ru'))
data = [
    [p('<b>Навык</b>','SmallRu'), p('<b>Оценка</b>','SmallRu'), p('<b>Комментарий</b>','SmallRu')],
    [p('Перевод десятичных дробей','SmallRu'), p('хорошо','SmallRu'), p('Основные дроби уже узнаёшь. Нужно удержать 0,875 = 7/8 и 0,625 = 5/8.','SmallRu')],
    [p('Умножение и деление дробей','SmallRu'), p('хорошо, но нужна чистота','SmallRu'), p('Сокращения есть. Теперь важно не путать деление и умножение на обратную дробь.','SmallRu')],
    [p('Длинное выражение','SmallRu'), p('почти готово','SmallRu'), p('Ответ получен правильно. Нужна более короткая и аккуратная запись.','SmallRu')],
    [p('Текстовые задачи на движение','SmallRu'), p('хорошо','SmallRu'), p('Правильно выбрала разность скоростей для догоняющего велосипедиста.','SmallRu')],
    [p('Готовность идти дальше','SmallRu'), p('да, с повторением','SmallRu'), p('Из-за срока 26 мая пора переходить к текстовым задачам, но дроби оставить в ежедневной разминке.','SmallRu')],
]
t=Table(data, colWidths=[45*mm, 35*mm, 90*mm])
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.grey),('BACKGROUND',(0,0),(-1,0),HexColor('#d9ead3')),('VALIGN',(0,0),(-1,-1),'TOP'),('FONTNAME',(0,0),(-1,-1),'NotoSans'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story.append(t)
story.append(Spacer(1,6))
story.append(p('Задача на завтра', 'H1Ru'))
story.append(box('Завтра тренируем не только вычисления, а текстовые задачи: время, части от целого, проценты и один большой пример на дроби для повторения. Главное правило: сначала короткая схема, потом действия.', '#edf7ed'))
story.append(p('Настюшик, ты уже можешь идти дальше. Просто не бросаем дроби: каждый день 10 минут разминки, и они перестанут мешать новым темам.', 'BodyRu'))
make_doc('obratnaya_svyaz_den3_Nastyushik.pdf', 'Обратная связь День 3').build(story, onFirstPage=header_footer, onLaterPages=header_footer)

# PDF 2 Day4 tasks
story=[]
story.append(p('День 4. Текстовые задачи + повторение дробей', 'TitleRu'))
story.append(box('Настюшик, сегодня задача - перейти от чистых дробей к задачам со смыслом. Сначала пишем схему, потом считаем. Срок близко, поэтому работаем аккуратно и без лишних примеров.', '#fff7e6'))
story.append(p('Правила на сегодня', 'H1Ru'))
story += bullet([
    'Одна строка - одно действие.',
    'В текстовой задаче сначала переведи время, граммы, проценты или части в удобный вид.',
    'Если есть проценты: 50% = 1/2, 25% = 1/4, 20% = 1/5, 15% = 15/100.',
    'Если получился странный ответ, сначала сделай прикидку.'
])
story.append(p('Блок 1. Разминка на дроби', 'H1Ru'))
for i, ex in enumerate(['0,875 = ?', '0,625 = ?', '6,72 : 6,4 = ?', '2,0625 · 4/25 = ?', '25/4 · 69/50 = ?', '6 3/4 + 69/8 = ?'],1):
    story.append(p(f'{i}) {ex}', 'TaskRu'))
story.append(p('Блок 2. Время на уроки', 'H1Ru'))
story.append(p('Тане надо приготовить уроки за 1 ч 45 мин. На математику она потратила 1/3 всего времени, на русский язык - 0,2 всего времени, а историю учила 49 минут. Успела ли Таня? Запиши решение по действиям.', 'TaskRu'))
story.append(p('Блок 3. Найди число по его части', 'H1Ru'))
story.append(p('Найдите 7/24 числа, если 5/16 этого числа равны 15.', 'TaskRu'))
story.append(p('Блок 4. Проценты: вся книга', 'H1Ru'))
story.append(p('В сборнике три повести. Первая занимает 60 страниц, что составляет 50% всей книги. Сколько всего страниц в книге?', 'TaskRu'))
story.append(p('Блок 5. Проценты: второе и третье число', 'H1Ru'))
story.append(p('Первое число равно 48 и составляет 15% второго числа. Третье число составляет 13/20 второго. Найдите второе и третье числа.', 'TaskRu'))
story.append(p('Блок 6. Задача про витамины', 'H1Ru'))
story.append(p('В 100 г чёрной смородины содержится 250 мг витамина C. Суточная доза для одного взрослого - 70 мг. В одной упаковке 10 таблеток по 0,025 г витамина C. Семья из 3 человек заготовила 5 кг смородины. Зима длится 90 дней. Какое наименьшее число упаковок витаминов нужно купить?', 'TaskRu'))
story.append(box('Подсказка: 1 г = 1000 мг. Значит 0,025 г = 25 мг. В конце число упаковок округляем вверх.', '#eef7ff'))
story.append(p('Блок 7. Мини-проверка без подсказок', 'H1Ru'))
for i, ex in enumerate(['0,2 от 105 минут = ?', '1/3 от 105 минут = ?', '15% от числа x - это 48. Как найти x?', 'Если 6,72 : 6,4 получилось 10,5, почему это точно ошибка?'],1):
    story.append(p(f'{i}) {ex}', 'TaskRu'))
make_doc('den4_zadaniya_Nastyushik.pdf', 'День 4 задания').build(story, onFirstPage=header_footer, onLaterPages=header_footer)

# PDF 3 Day4 answers
story=[]
story.append(p('День 4. Ответы и акценты для проверки', 'TitleRu'))
story.append(box('Проверяем не только ответ. Главный критерий: есть схема, единицы измерения, аккуратная цепочка действий и финальный ответ словами.', '#fff7e6'))
story.append(p('Блок 1. Разминка', 'H1Ru'))
answers1 = [
    '0,875 = 875/1000 = 7/8.',
    '0,625 = 625/1000 = 5/8.',
    '6,72 : 6,4 = 168/25 : 32/5 = 168/25 · 5/32 = 21/20 = 1,05.',
    '2,0625 · 4/25 = 33/16 · 4/25 = 33/100 = 0,33.',
    '25/4 · 69/50 = 69/8 = 8,625.',
    '6 3/4 + 69/8 = 27/4 + 69/8 = 54/8 + 69/8 = 123/8 = 15 3/8 = 15,375.'
]
story += bullet(answers1)
story.append(p('Блок 2. Время на уроки', 'H1Ru'))
story += bullet([
    '1 ч 45 мин = 105 мин.',
    'Математика: 1/3 · 105 = 35 мин.',
    'Русский: 0,2 · 105 = 1/5 · 105 = 21 мин.',
    'Всего: 35 + 21 + 49 = 105 мин.',
    'Ответ: Таня успела ровно за 1 ч 45 мин.'
])
story.append(box('Акцент: если получилось меньше или больше 105, проверить перевод 0,2 = 1/5 и 1 ч 45 мин = 105 мин.', '#edf7ed'))
story.append(p('Блок 3. Найди число по его части', 'H1Ru'))
story += bullet([
    'Пусть число равно x.',
    '5/16 от x равны 15: x · 5/16 = 15.',
    'x = 15 : 5/16 = 15 · 16/5 = 48.',
    '7/24 от 48: 48 · 7/24 = 2 · 7 = 14.',
    'Ответ: 14.'
])
story.append(p('Блок 4. Проценты: вся книга', 'H1Ru'))
story += bullet([
    '50% = 1/2.',
    'Если 60 страниц - половина книги, то вся книга: 60 · 2 = 120 страниц.',
    'Ответ: 120 страниц.'
])
story.append(p('Блок 5. Проценты: второе и третье число', 'H1Ru'))
story += bullet([
    '48 - это 15% второго числа.',
    '15% = 15/100 = 3/20.',
    'Второе число: 48 : 3/20 = 48 · 20/3 = 320.',
    'Третье число: 13/20 · 320 = 13 · 16 = 208.',
    'Ответ: второе число 320, третье число 208.'
])
story.append(p('Блок 6. Витамины', 'H1Ru'))
story += bullet([
    '5 кг = 5000 г.',
    'В 100 г - 250 мг, значит в 5000 г: 5000 : 100 · 250 = 50 · 250 = 12500 мг.',
    'Семье нужно за зиму: 70 · 3 · 90 = 18900 мг.',
    'Не хватает: 18900 - 12500 = 6400 мг.',
    '1 таблетка: 0,025 г = 25 мг.',
    '1 упаковка: 10 · 25 = 250 мг.',
    '6400 : 250 = 25,6, значит нужно округлить вверх.',
    'Ответ: 26 упаковок.'
])
story.append(box('Акценты проверки: 0,025 г обязательно перевести в 25 мг; 25,6 упаковки нельзя округлять до 25, потому что 25 упаковок не хватит.', '#edf7ed'))
story.append(p('Блок 7. Мини-проверка', 'H1Ru'))
story += bullet([
    '0,2 от 105 = 21.',
    '1/3 от 105 = 35.',
    'Если 15% от x - это 48, то x = 48 : 15/100 = 320.',
    '6,72 : 6,4 должно быть чуть больше 1, потому что 6,72 чуть больше 6,4. Ответ 10,5 невозможен.'
])
story.append(p('Что считать успехом Дня 4', 'H1Ru'))
story += bullet([
    'Настюшик сама переводит 1 ч 45 мин в 105 мин.',
    'Понимает 0,2 как 1/5.',
    'Умеет находить целое по части: 48 : 15/100.',
    'В задаче про витамины не путает граммы и миллиграммы.',
    'В конце пишет ответ словами.'
])
make_doc('den4_otvety_i_akcenty.pdf', 'День 4 ответы').build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print('created')
