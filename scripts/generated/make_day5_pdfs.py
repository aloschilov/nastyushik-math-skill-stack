from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

FONT_REG = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', FONT_REG))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRus', parent=styles['Title'], fontName='NotoSans-Bold', fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name='H1Rus', parent=styles['Heading1'], fontName='NotoSans-Bold', fontSize=14, leading=18, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='H2Rus', parent=styles['Heading2'], fontName='NotoSans-Bold', fontSize=12, leading=15, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyRus', parent=styles['BodyText'], fontName='NotoSans', fontSize=10.5, leading=14, spaceAfter=4))
styles.add(ParagraphStyle(name='SmallRus', parent=styles['BodyText'], fontName='NotoSans', fontSize=9.2, leading=12, spaceAfter=3))
styles.add(ParagraphStyle(name='Callout', parent=styles['BodyText'], fontName='NotoSans-Bold', fontSize=10.5, leading=14, backColor=colors.HexColor('#F0F6FF'), borderColor=colors.HexColor('#C9DFFF'), borderWidth=0.5, borderPadding=6, spaceBefore=5, spaceAfter=6))
styles.add(ParagraphStyle(name='Task', parent=styles['BodyText'], fontName='NotoSans', fontSize=11, leading=18, spaceAfter=2))
styles.add(ParagraphStyle(name='Answer', parent=styles['BodyText'], fontName='NotoSans', fontSize=10, leading=14, spaceAfter=3))

MARGIN = 15*mm

def doc(path, title=None):
    return SimpleDocTemplate(path, pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN, topMargin=14*mm, bottomMargin=14*mm, title=title)

def P(txt, style='BodyRus'):
    return Paragraph(txt, styles[style])

def bullet(items, style='BodyRus'):
    story=[]
    for it in items:
        story.append(P('• ' + it, style))
    return story

def make_feedback():
    path='/mnt/data/obratnaya_svyaz_den4_Nastyushik.pdf'
    story=[]
    story.append(P('Настюшик, обратная связь по Дню 4', 'TitleRus'))
    story.append(P('Сегодня ты хорошо показала, что можешь решать не только вычисления, но и текстовые задачи. Это важный шаг: теперь дроби начинают работать внутри настоящих задач.', 'Callout'))
    story.append(P('Что получилось особенно хорошо', 'H1Rus'))
    story += bullet([
        'Дробная разминка стала устойчивой: 0,875 = 7/8, 0,625 = 5/8, 6,72 : 6,4 = 1,05.',
        'Задача про уроки решена правильно: 1 ч 45 мин = 105 мин; математика 35 мин, русский 21 мин, история 49 мин; всего 105 мин, значит Таня успела.',
        'Задачи "найти число по его части" стали получаться: если 5/16 числа равны 15, всё число равно 48, а 7/24 от него равно 14.',
        'Проценты в простой задаче тоже получились: если 60 страниц - это 50%, вся книга - 120 страниц.',
        'Большая задача про витамин C решена правильно до ответа 26 упаковок. Это очень сильный результат для текстовой задачи с единицами измерения.'
    ])
    story.append(P('Что надо закрепить', 'H1Rus'))
    story += bullet([
        'В задачах с процентами всегда сначала писать: что является 100%.',
        'В задачах "часть от числа" и "число по части" не путать два действия: часть от числа - умножаем, число по части - делим.',
        'В длинных задачах держать единицы измерения: г, мг, дни, человек, упаковки. Единицы помогают не потеряться.',
        'Ответ в конце должен быть не просто числом, а фразой: "26 упаковок", "120 страниц", "Таня успела".'
    ])
    story.append(P('Оценка навыков после Дня 4', 'H1Rus'))
    data = [
        [P('Навык','SmallRus'), P('Уровень','SmallRus'), P('Комментарий','SmallRus')],
        [P('Действия с дробями','SmallRus'), P('хорошо','SmallRus'), P('Ключевые вычисления из КР №2 уже получаются.', 'SmallRus')],
        [P('Текстовые задачи на части','SmallRus'), P('хорошо','SmallRus'), P('Задачи про уроки и витамин C решены верно.', 'SmallRus')],
        [P('Проценты','SmallRus'), P('начало хорошее','SmallRus'), P('Нужно больше задач на "что такое 100%".', 'SmallRus')],
        [P('Самопроверка','SmallRus'), P('становится лучше','SmallRus'), P('Хорошо объяснила, почему 6,72 : 6,4 не может быть 10,5.', 'SmallRus')],
    ]
    t=Table(data, colWidths=[42*mm,32*mm,91*mm])
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'NotoSans'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF2FF')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#B8C7D9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)
    ]))
    story.append(t)
    story.append(P('Куда идём дальше', 'H1Rus'))
    story.append(P('Срок близко, поэтому дальше мы не застреваем на одной теме. На следующем занятии идём в проценты и задачи "часть - целое", а дроби оставляем короткой разминкой.', 'BodyRus'))
    story.append(P('Цель следующего дня: научиться быстро выбирать действие: найти часть от числа, найти всё число по части или найти процент.', 'Callout'))
    doc(path, 'Обратная связь День 4').build(story)
    return path

def make_tasks():
    path='/mnt/data/den5_zadaniya_Nastyushik.pdf'
    story=[]
    story.append(P('День 5. Проценты и части от целого', 'TitleRus'))
    story.append(P('Настюшик, сегодня цель такая: быстро понять, что в задаче является целым, что является частью, и какое действие выбрать. Пиши аккуратно: одна строка - одно действие.', 'Callout'))
    story.append(P('Блок 1. Разминка по дробям', 'H1Rus'))
    for i, task in enumerate(['0,875 = ?', '0,625 = ?', '6,72 : 6,4 = ?', '2,0625 · 4/25 = ?', '25/4 · 69/50 = ?', '6 3/4 + 69/8 = ?'],1):
        story.append(P(f'{i}) {task}', 'Task'))
    story.append(P('Блок 2. Найди часть от числа', 'H1Rus'))
    story.append(P('Подсказка: если нужно найти часть от числа - умножаем.', 'SmallRus'))
    for i, task in enumerate(['Найди 3/5 от 40.', 'Найди 7/24 от 48.', 'Найди 13/20 от 320.', 'Найди 15% от 200.', 'Найди 35% от 80.'],1):
        story.append(P(f'{i}) {task}', 'Task'))
    story.append(P('Блок 3. Найди всё число по его части', 'H1Rus'))
    story.append(P('Подсказка: если часть известна, а нужно всё число - делим на эту часть.', 'SmallRus'))
    for i, task in enumerate(['5/16 числа равны 15. Найди число.', '60 страниц составляют 50% всей книги. Сколько страниц в книге?', '48 составляет 15% второго числа. Найди второе число.', '35 минут составляют 1/3 всего времени. Сколько всего минут?', '21 минута составляет 0,2 всего времени. Сколько всего минут?'],1):
        story.append(P(f'{i}) {task}', 'Task'))
    story.append(PageBreak())
    story.append(P('Блок 4. Проценты: что такое 100%?', 'H1Rus'))
    story.append(P('Перед решением напиши: "100% - это ..."', 'SmallRus'))
    for i, task in enumerate(['В книге 120 страниц. Первая повесть занимает 60 страниц. Сколько это процентов?', 'В классе 25 учеников, 5 из них отсутствуют. Сколько процентов учеников отсутствуют?', 'Число 48 составляет 15% числа x. Найди x.', 'В сплаве 300 г, из них 60 г олова. Сколько процентов олова в сплаве?'],1):
        story.append(P(f'{i}) {task}', 'Task'))
    story.append(P('Блок 5. Текстовые задачи', 'H1Rus'))
    tasks=[
        'Таня должна закончить уроки за 1 ч 45 мин. На математику ушла 1/3 всего времени, на русский - 0,2 всего времени, на историю - 49 мин. Успела ли Таня?',
        'В сборнике три повести. Первая занимает 60 страниц, что составляет 50% всей книги. Сколько всего страниц в книге?',
        'Первое число равно 48 и составляет 15% второго числа. Третье число составляет 13/20 второго. Найди второе и третье числа.',
        'В 100 г смородины 250 мг витамина C. Семья заготовила 5 кг смородины. Сколько мг витамина C в заготовленной смородине?'
    ]
    for i, task in enumerate(tasks,1):
        story.append(P(f'{i}) {task}', 'Task'))
    story.append(P('Блок 6. Самопроверка', 'H1Rus'))
    for i, task in enumerate(['Если нужно найти 15% от числа, это умножение или деление?', 'Если 15% числа равны 48, это умножение или деление?', 'Почему 0,2 всего времени - это 1/5 всего времени?', 'Что значит округлить 25,6 упаковки в большую сторону?'],1):
        story.append(P(f'{i}) {task}', 'Task'))
    doc(path,'День 5 задания').build(story)
    return path

def make_answers():
    path='/mnt/data/den5_otvety_i_akcenty.pdf'
    story=[]
    story.append(P('День 5. Ответы и акценты для проверки', 'TitleRus'))
    story.append(P('Главная проверка дня: Настюшик должна не только получить ответ, но и выбрать правильную модель: часть от числа, всё число по части или процент.', 'Callout'))
    story.append(P('Блок 1. Разминка', 'H1Rus'))
    answers=['0,875 = 7/8','0,625 = 5/8','6,72 : 6,4 = 168/25 : 32/5 = 21/20 = 1,05','2,0625 · 4/25 = 33/16 · 4/25 = 33/100 = 0,33','25/4 · 69/50 = 69/8 = 8,625','6 3/4 + 69/8 = 54/8 + 69/8 = 123/8 = 15,375']
    for i,a in enumerate(answers,1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Блок 2. Найди часть от числа', 'H1Rus'))
    for i,a in enumerate(['40 · 3/5 = 24','48 · 7/24 = 14','320 · 13/20 = 208','200 · 15/100 = 30','80 · 35/100 = 28'],1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Блок 3. Найди всё число по части', 'H1Rus'))
    for i,a in enumerate(['15 : 5/16 = 48','60 : 0,5 = 120 страниц','48 : 0,15 = 320','35 : 1/3 = 105 минут','21 : 0,2 = 105 минут'],1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Акцент: если известна часть и надо найти целое, делим на дробь или процент.', 'Callout'))
    story.append(PageBreak())
    story.append(P('Блок 4. Проценты', 'H1Rus'))
    for i,a in enumerate(['100% - 120 страниц. 60/120 = 1/2 = 50%.','100% - 25 учеников. 5/25 = 1/5 = 20%.','48 = 15% от x. x = 48 : 0,15 = 320.','100% - 300 г. 60/300 = 1/5 = 20%.'],1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Блок 5. Текстовые задачи', 'H1Rus'))
    ans5=[
        '1 ч 45 мин = 105 мин. Математика: 105 · 1/3 = 35. Русский: 105 · 0,2 = 21. Всего: 35 + 21 + 49 = 105. Ответ: успела ровно.',
        '60 страниц - это 50%, значит вся книга: 60 : 0,5 = 120 страниц.',
        'Второе число: 48 : 0,15 = 320. Третье: 320 · 13/20 = 208.',
        '5 кг = 5000 г. В 100 г - 250 мг, значит в 5000 г: 5000 : 100 · 250 = 12500 мг.'
    ]
    for i,a in enumerate(ans5,1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Блок 6. Самопроверка', 'H1Rus'))
    ans6=['Найти 15% от числа - умножение на 15/100 или 0,15.','Если 15% числа равны 48, нужно делить: 48 : 0,15.','0,2 = 2/10 = 1/5.','25,6 упаковки нельзя купить как 25 упаковок: не хватит. Округляем вверх до 26.']
    for i,a in enumerate(ans6,1): story.append(P(f'{i}) {a}', 'Answer'))
    story.append(P('Что считать ошибкой', 'H1Rus'))
    story += bullet([
        'Записала правильное число, но не указала единицы измерения в текстовой задаче.',
        'Перепутала действия: вместо деления на 0,15 умножила на 0,15.',
        'Не написала, что является 100% в задаче на проценты.',
        'Округлила 25,6 упаковки вниз до 25.'
    ], 'SmallRus')
    doc(path,'День 5 ответы').build(story)
    return path

if __name__=='__main__':
    for f in [make_feedback(), make_tasks(), make_answers()]:
        print(f)
