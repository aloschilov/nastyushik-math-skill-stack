from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', FONT))
pdfmetrics.registerFont(TTFont('DejaVuBold', FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleRU', fontName='DejaVuBold', fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name='SubTitleRU', fontName='DejaVu', fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=12))
styles.add(ParagraphStyle(name='H1RU', fontName='DejaVuBold', fontSize=13, leading=16, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='H2RU', fontName='DejaVuBold', fontSize=11, leading=14, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyRU', fontName='DejaVu', fontSize=10, leading=14, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallRU', fontName='DejaVu', fontSize=8.8, leading=12, spaceAfter=4))
styles.add(ParagraphStyle(name='TaskRU', fontName='DejaVu', fontSize=10.5, leading=16, spaceAfter=3))
styles.add(ParagraphStyle(name='AnswerRU', fontName='DejaVu', fontSize=10, leading=14, spaceAfter=3))
styles.add(ParagraphStyle(name='AccentRU', fontName='DejaVuBold', fontSize=10, leading=14, textColor=colors.HexColor('#8A1F11'), spaceAfter=4))

line = '<font color="#999999">__________________________________________________________________</font>'


def p(txt, style='BodyRU'):
    return Paragraph(txt, styles[style])

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('DejaVu', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0]/2, 10*mm, f"{doc.page}")
    canvas.restoreState()


def build_tasks(path):
    doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    story=[]
    story.append(p('День 1. Дроби и десятичные дроби', 'TitleRU'))
    story.append(p('Рабочий лист для самостоятельного решения. Без калькулятора. Время: 35-45 минут.', 'SubTitleRU'))
    story.append(p('<b>Правила работы:</b> каждую десятичную дробь сначала переведи в обыкновенную; каждую дробь сокращай; каждое действие пиши отдельной строкой. Если ответ получился неожиданно большим, проверь порядок величины.', 'BodyRU'))

    story.append(p('Блок 1. Быстрый перевод дробей', 'H1RU'))
    story.append(p('Заполни пропуски. Сокращай дроби до несократимого вида.', 'BodyRU'))
    items = ['0,5 =', '0,25 =', '0,75 =', '0,2 =', '0,4 =', '0,6 =', '0,8 =', '0,025 =', '0,625 =', '0,375 =']
    data=[]
    for i in range(0,len(items),2):
        data.append([f'{i+1}) {items[i]}', '________________', f'{i+2}) {items[i+1]}', '________________'])
    tbl=Table(data, colWidths=[32*mm,45*mm,32*mm,45*mm])
    tbl.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'DejaVu'),('FONTSIZE',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(tbl)

    story.append(p('Блок 2. Десятичные дроби в обыкновенные', 'H1RU'))
    story.append(p('Формат: 6,72 = 672/100 = 168/25.', 'SmallRU'))
    decs=['0,35','0,65','0,625','0,375','2,0625','6,72','6,4','0,025']
    for i,d in enumerate(decs,1):
        story.append(p(f'{i}) {d} = {line}', 'TaskRU'))

    story.append(p('Блок 3. Сокращение дробей', 'H1RU'))
    fracs=['18/33','36/60','14/24','36/90','28/70','48/84','(25 · 39)/(35 · 13)','(7 · 12)/(30 · 21)']
    for i,f in enumerate(fracs,1):
        story.append(p(f'{i}) {f} = {line}', 'TaskRU'))

    story.append(p('Блок 4. Сравнение', 'H1RU'))
    story.append(p('Поставь знак &lt;, &gt; или =. Рядом напиши короткое объяснение: привёл к общему знаменателю или перевёл десятичную дробь.', 'BodyRU'))
    comps=['3/7 ___ 0,4','5/7 ___ 0,7','5/6 ___ 8/9','1/12 ___ 3/20']
    for i,c in enumerate(comps,1):
        story.append(p(f'{i}) {c}. Объяснение: {line}', 'TaskRU'))

    story.append(PageBreak())
    story.append(p('Блок 5. Мостик к контрольной №2', 'H1RU'))
    story.append(p('Решай по строкам. Не смешивай несколько действий в одной строке.', 'BodyRU'))
    bridge = [
        '1) 2,0625 · 4/25 =',
        '2) 6,72 : 6,4 =',
        '3) 2,0625 · 4/25 + 6,72 : 6,4 =',
        '4) 6 1/4 · (2,0625 · 4/25 + 6,72 : 6,4) =',
        '5) 6 3/4 + 6 1/4 · (2,0625 · 4/25 + 6,72 : 6,4) ='
    ]
    for b in bridge:
        story.append(p(b, 'TaskRU'))
        story.append(p(line, 'TaskRU'))
        story.append(p(line, 'TaskRU'))

    story.append(p('Блок 6. Мини-проверка на движение', 'H1RU'))
    story.append(p('Из двух посёлков в одном направлении выехали два велосипедиста. Скорость первого 90 м/мин, это 3/5 скорости второго. Расстояние между посёлками 1200 м. Через сколько минут второй догонит первого?', 'BodyRU'))
    story.append(p('1) Скорость второго: ' + line, 'TaskRU'))
    story.append(p('2) Скорость сближения: ' + line, 'TaskRU'))
    story.append(p('3) Время: ' + line, 'TaskRU'))
    story.append(p('Ответ: ' + line, 'TaskRU'))

    story.append(p('Самопроверка перед сдачей', 'H1RU'))
    checks=[
        'В десятичной дроби я посчитал количество знаков после запятой.',
        'Все дроби сокращены.',
        'Деление дробей заменено умножением на обратную дробь.',
        'В задаче на движение я проверил: скорости надо складывать или вычитать.',
        'Финальный ответ похож по размеру на ожидаемый.'
    ]
    for c in checks:
        story.append(p('□ ' + c, 'BodyRU'))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def build_answers(path):
    doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    story=[]
    story.append(p('День 1. Ответы и акценты для проверки', 'TitleRU'))
    story.append(p('Для взрослого. Проверять не только ответ, но и способ записи.', 'SubTitleRU'))

    story.append(p('Главная цель проверки', 'H1RU'))
    story.append(p('Не добиваться скорости любой ценой. Сегодня проверяем три навыка: 1) десятичная дробь -> обыкновенная; 2) сокращение; 3) порядок действий в выражении. Если ребёнок получил ответ, но запись грязная или пропущены переходы, это считать неполным решением.', 'BodyRU'))

    story.append(p('Блок 1. Быстрый перевод дробей', 'H1RU'))
    ans1=[('0,5','1/2'),('0,25','1/4'),('0,75','3/4'),('0,2','1/5'),('0,4','2/5'),('0,6','3/5'),('0,8','4/5'),('0,025','1/40'),('0,625','5/8'),('0,375','3/8')]
    data=[[a,b] for a,b in ans1]
    tbl=Table(data, colWidths=[45*mm,45*mm])
    tbl.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'DejaVu'),('FONTSIZE',(0,0),(-1,-1),10),('GRID',(0,0),(-1,-1),0.25,colors.lightgrey),('BACKGROUND',(0,0),(-1,0),colors.whitesmoke)]))
    story.append(tbl)
    story.append(Spacer(1,5))
    story.append(p('<b>Акцент:</b> 0,025 = 25/1000 = 1/40. Здесь часто ошибаются с количеством нулей.', 'AccentRU'))

    story.append(p('Блок 2. Десятичные дроби в обыкновенные', 'H1RU'))
    ans2=[
        '0,35 = 35/100 = 7/20',
        '0,65 = 65/100 = 13/20',
        '0,625 = 625/1000 = 5/8',
        '0,375 = 375/1000 = 3/8',
        '2,0625 = 20625/10000 = 33/16 = 2 1/16',
        '6,72 = 672/100 = 168/25 = 6 18/25',
        '6,4 = 64/10 = 32/5 = 6 2/5',
        '0,025 = 25/1000 = 1/40'
    ]
    for a in ans2: story.append(p(a, 'AnswerRU'))
    story.append(p('<b>Акцент:</b> если ребёнок пишет 6,72 = 672/10, это ключевая ошибка дня. Нужно возвращать к правилу: две цифры после запятой - знаменатель 100.', 'AccentRU'))

    story.append(p('Блок 3. Сокращение дробей', 'H1RU'))
    ans3=['18/33 = 6/11','36/60 = 3/5','14/24 = 7/12','36/90 = 2/5','28/70 = 2/5','48/84 = 4/7','(25 · 39)/(35 · 13) = 15/7 = 2 1/7','(7 · 12)/(30 · 21) = 2/15']
    for a in ans3: story.append(p(a, 'AnswerRU'))
    story.append(p('<b>Акцент:</b> в произведениях сокращать до умножения больших чисел. Это уменьшает ошибки.', 'AccentRU'))

    story.append(p('Блок 4. Сравнение', 'H1RU'))
    ans4=['3/7 > 0,4, потому что 3/7 ≈ 0,428...','5/7 > 0,7, потому что 5/7 ≈ 0,714...','5/6 < 8/9, потому что 15/18 < 16/18','1/12 < 3/20, потому что 5/60 < 9/60']
    for a in ans4: story.append(p(a, 'AnswerRU'))
    story.append(p('<b>Акцент:</b> разрешить любой корректный способ сравнения: общий знаменатель, десятичное приближение или перекрёстное умножение.', 'AccentRU'))

    story.append(PageBreak())
    story.append(p('Блок 5. Мостик к контрольной №2', 'H1RU'))
    story.append(p('Ожидаемая чистая запись:', 'BodyRU'))
    steps=[
        '2,0625 · 4/25 = 33/16 · 4/25 = 33/100.',
        '6,72 : 6,4 = 168/25 : 32/5 = 168/25 · 5/32 = 21/20.',
        '33/100 + 21/20 = 33/100 + 105/100 = 138/100 = 69/50.',
        '6 1/4 · 69/50 = 25/4 · 69/50 = 69/8.',
        '6 3/4 + 69/8 = 27/4 + 69/8 = 54/8 + 69/8 = 123/8 = 15 3/8 = 15,375.'
    ]
    for s in steps: story.append(p(s, 'AnswerRU'))
    story.append(p('<b>Акцент:</b> 6,72 : 6,4 должно быть чуть больше 1, а не около 10. Приучать к быстрой оценке: 6,72 и 6,4 почти равны.', 'AccentRU'))
    story.append(p('<b>Акцент:</b> если ребёнок получает большие дроби вроде 27079/2500, не ругать за арифметику сразу, а вернуть к более раннему месту: были ли десятичные дроби сокращены до удобных 33/16, 168/25, 32/5?', 'AccentRU'))

    story.append(p('Блок 6. Движение', 'H1RU'))
    movement=[
        '90 м/мин - это 3/5 скорости второго, значит скорость второго: 90 : 3/5 = 90 · 5/3 = 150 м/мин.',
        'Едут в одном направлении, второй догоняет первого, поэтому скорость сближения: 150 - 90 = 60 м/мин.',
        'Время: 1200 : 60 = 20 минут.',
        'Ответ: через 20 минут.'
    ]
    for s in movement: story.append(p(s, 'AnswerRU'))
    story.append(p('<b>Акцент:</b> главная ошибка - сложить скорости и получить 5 минут. В одном направлении при догонянии скорости вычитаются.', 'AccentRU'))

    story.append(p('Как оценить результат дня', 'H1RU'))
    story.append(p('Хорошо: не меньше 80% ответов верные, десятичные дроби переведены с правильным количеством нулей, в выражении порядок действий сохранён.', 'BodyRU'))
    story.append(p('Нужно повторить день: если путает 6,72 = 672/10, не умеет сокращать 0,625 и 0,375, или в делении дробей не заменяет деление умножением на обратную.', 'BodyRU'))
    story.append(p('Следующий шаг: только после уверенного выполнения этого листа переходить к отдельной тренировке деления дробей и затем к полному выражению КР №2 №1.', 'BodyRU'))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

if __name__ == '__main__':
    build_tasks('/mnt/data/den1_zadaniya_drobi.pdf')
    build_answers('/mnt/data/den1_otvety_i_akcenty.pdf')
