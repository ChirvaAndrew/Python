from tkinter import *
from tkinter.ttk import Combobox, Radiobutton
import urllib.request
from tkinter.ttk import Notebook, Frame
import xml.dom.minidom
import datetime
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt

#Создание окна
window = Tk()
window.title("Конвертер валют")
window.geometry("1920x1080")

#Возвращает текущее время
def nowp(a):#Аргументы: 0 - Дата/Месяц/Год; 1 - Дата; 2 - Месяц; 3 - Год
    current_date = datetime.datetime.now()
    if a == 0:
        return current_date.strftime('%d/%m/%Y')
    if a == 1:
        return current_date.strftime('%d')
    if a == 2:
        return current_date.strftime('%m')
    if a == 3:
        return current_date.strftime('%Y')

def sevenyears(s): #Возвращает Текущий год минус s лет
    current_date = datetime.datetime.now()
    day = current_date.strftime('%Y')
    return str(int(day) - s)

def sevendays(s): #Возвращает дату начала и конца текущей недели в формате День.Месяц.Год - День.Месяц.Год
    current_date = datetime.datetime.now()
    day = current_date.strftime('%m.%d.%y')
    dt = datetime.datetime.strptime(day, '%m.%d.%y')
    start = dt - datetime.timedelta(days = dt.weekday()) - datetime.timedelta(days=s)#Начало недели
    end = start + datetime.timedelta(days = 6) #Конец недели
    start = start.strftime('%d.%m.%Y') #Форматирование
    end = end.strftime('%d.%m.%Y')
    return str(start + " - " + end)

def sevenkvart(s): #Возвращает номер квартала + год (Текущая дата - s месяцев)
    current_date = datetime.datetime.now()
    day = current_date.strftime('%m')
    year = current_date.strftime('%Y')
    day = int(day) - s
    while day <= 0: #Отработка случая с переходом в предыдущий год
        day = 12 + day
        year = str(int(year) - 1)
    if day == 1 or day == 2 or day == 3:
        return "I квартал " + year
    if day == 4 or day == 5 or day == 6:
        return "II квартал " + year
    if day == 7 or day == 8 or day == 9:
        return "III квартал " + year
    if day == 10 or day == 11 or day == 12:
        return "IV квартал " + year

def sevenmounth(s): #Возвращает str с названием месяца + год (Текущий месяц - s месяцев)
    current_date = datetime.datetime.now()
    day = current_date.strftime('%m')
    year = current_date.strftime('%Y')
    day = int(day) - s
    while day <= 0: #Отработка случая с переходом в предыдущий год
        day = 12 + day
        year = str(int(year) - 1)
    if day == 1:
        return "Январь " + year
    if day == 2:
        return "Февраль " + year
    if day == 3:
        return "Март " + year
    if day == 4:
        return "Апрель " + year
    if day == 5:
        return "Май " + year
    if day == 6:
        return "Июнь " + year
    if day == 7:
        return "Июль " + year
    if day == 8:
        return "Август " + year
    if day == 9:
        return "Сентябрь " + year
    if day == 10:
        return "Октябрь " + year
    if day == 11:
        return "Ноябрь " + year
    if day == 12:
        return "Декабрь " + year


link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + nowp(0) #Ссылка на сегодняшние котировки

response = urllib.request.urlopen(link)
ValName = ["Российский рубль"] #Список с названиями валют
ValNom = ["1.0"] #Список с номиналами валют
ValValue = ["1.0"] #Список с курсом валют
dom = xml.dom.minidom.parse(response) #Получение DOM структуры файла #Знать бы что такое DOM
dom.normalize()
nodeArray = dom.getElementsByTagName("Valute") #Получение элементов с тегом
for node in nodeArray:
    childList = node.childNodes #Получение дочерних элементов
    for child in childList:
        if (child.nodeName == "Name"):
            ValName.append(child.childNodes[0].nodeValue) #Добавление информации в списки ВАЖНО: Списки ассоциируются между друг другом только по индексу. Нельзя менять порядок только в одном списке, только во всех одновременно!
        if(child.nodeName == "Nominal"):
            ValNom.append(child.childNodes[0].nodeValue)
        if (child.nodeName == "Value"):
            ValValue.append(child.childNodes[0].nodeValue)
        #print(child.nodeName)
        #print(child.childNodes[0].nodeValue) #Получение значения

for i in range (len(ValValue)): #, -> .
    ValValue[i] = ValValue[i].replace(',','.') #Замена запятых на точки в курсах

"""
Здесь начинается первая вкладка
"""
tab_control = Notebook(window)
tab1 = Frame(tab_control)#Первая вкладка
tab_control.add(tab1, text = "Калькулятор валют")

combobox1 = Combobox(tab1) #Поле выбора первой валюты
combobox1["values"] = (ValName)
combobox1.current(0)
combobox1.grid(row = 0, column = 0, pady = 10)

combobox2 = Combobox(tab1) #Поле выбора второй валюты
combobox2["values"] = (ValName)
combobox2.current(0)
combobox2.grid(row = 2, column = 0)

entry1 = Entry(tab1, show = "") #Поле ввода числа
entry1.grid(row = 0, column = 1, pady = 10, padx = 20)


res = 0.0#Переменная в которой хранится результат вычисления
def ClickMe_click(): #Реакция по нажатии кнопки
    a = 0.0 #Переменная в которой хранится введённое значение
    global res
    a = float(entry1.get())
    valute1 = 0.0 #Переменная в которой хранится курс первой валюты к рублю
    valute2 = 0.0 #Переменная в которой хранится курс второй валюты к рублю
    for i in range(len(ValName)):
        if combobox1.get() == ValName[i]: #Ищем совпадение названия выбранной валюты и перебираемых названий валют
            valute1 = float(ValValue[i]) / float(ValNom[i]) #Нашли название, значит по тому-же индексу и курс, запоминаем его.
            break

    for i in range(len(ValName)):#Тоже самое для второй валюты
        if combobox2.get() == ValName[i]:
            valute2 = float(ValValue[i]) / float(ValNom[i])
            break

    res = (a * valute1) / valute2 #Вычисление соотношения курсов валют (Ответа)
    resultShow.configure(text = res) #Вывод результата

ClickMe = Button(tab1, text = "Конвертировать", command = ClickMe_click)
ClickMe.grid(row = 0, column = 2, pady = 10, padx = 10)

resultShow = Label(tab1, text = 0)
resultShow.grid(row = 1, column = 1, pady = 0, padx = 1)
"""
Здесь заканчивается первая вкладка
"""








"""
Здесь начинается вторая вкладка
"""

tab2 = Frame(tab_control)
tab_control.add(tab2, text="Динамика курса")


"""
Первый столбик
"""
combobox3Title = Label(tab2, text = "Валюта") # Здесь выбирается требуемая валюта
combobox3Title.grid(row = 0, column = 0, pady = 0, padx = 0)
combobox3 = Combobox(tab2)
combobox3["values"] = (ValName) # Значения берём из уже готового списка названий
combobox3.current(0)
combobox3.grid(row = 1, column = 0, pady = 0)

allVal = [] # Здесь хранятся числа для графика (сама стоимость валюты)
allDate = [] # Здесь хранятся подписи для графика (Даты)


def GraphVal(link): # Оно записывает значение стоимости валюты по передаваемой ссылке, а так же дату
    response = urllib.request.urlopen(link)
    global allVal
    global allDate
    flag = 0 # Показывает была ли найдена нужная валюта
    dom = xml.dom.minidom.parse(response)  # Получение DOM структуры файла #Знать бы что такое DOM
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Valute")  # Получение элементов с тегом
    for node in nodeArray:
        childList = node.childNodes  # Получение дочерних элементов
        for child in childList:
            if (child.nodeName == "Name"):
                if combobox3.get() == child.childNodes[0].nodeValue: #Сверяем названия валюты
                    flag = 1 #Ура, нашли
                else:
                    flag = 0 #Эх,не нашли
            if (child.nodeName == "Value"):
                if flag == 1: #Если мы нашли нужное название и сейчас находимся на позиции, то добавляем в список и значение и дату
                    allVal.append(child.childNodes[0].nodeValue)
                    allDate.append(link[-10::].replace("/",".")) #Дату достаём из передаваемой ссылки





def GraphThingy():#Создаёт нужные ссылки в зависимости от выбранного периода. Срабатывает после нажатии на кнопку
    global allVal
    global allDate
    allDate.clear() #Очищаем предыдущие результаты
    allVal.clear()
    if (radio_state.get() == 4): #Выбран год
        for i in range(1,10): #Содаём ссылки для всех одноциферных месяцев
            link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + nowp(1) + "/0" + str(i) + "/" + comboboxY.get()
            GraphVal(link) #Отправляем ссылку
        for i in range(10,13): #Содаём ссылки для всех двухзначных месяцев
            link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + nowp(1) + "/" + str(i) + "/" + comboboxY.get()
            GraphVal(link)
    if (radio_state.get() == 3):#Выбран квартал
        if(comboboxC.get()[0:3]) == "I к": #Колхоз, но сверяем начала названия, где есть римские цифры
            for i in range(1,4): #Ссылки на 1 и 15 число первых трех месяцев года, дальше по аналогично
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=15/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)

        if (comboboxC.get()[0:3]) == "II ":
            for i in range(4, 7):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=15/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
        if (comboboxC.get()[0:3]) == "III":
            for i in range(7, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=15/0" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
        if (comboboxC.get()[0:3]) == "IV ":
            for i in range(10, 13):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=15/" + str(i) + "/" + comboboxC.get()[-4:]
                GraphVal(link)
    if (radio_state.get() == 2): #Выбран месяц
        if comboboxM.get()[:-5] == "Январь": #Отрезаем год от названия, сверяем месяц
            for i in range(1,10): #Ссылки для одноциферных дней
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/01/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10,32):#Ссылки для двухзначных дней
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/01/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Февраль":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/02/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 29):#Не забываем про количество дней в каждом месяце!
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/02/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Март":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/03/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/03/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Апрель":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/04/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 31):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/04/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Май":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/05/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/05/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Июнь":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/06/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 31):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/06/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Июль":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/07/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/07/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Август":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/08/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/08/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Сентябрь":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/09/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 31):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/09/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Октябрь":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/10/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/10/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Ноябрь":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/11/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 31):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/11/" + comboboxM.get()[-4:]
                GraphVal(link)
        if comboboxM.get()[:-5] == "Декабрь":
            for i in range(1, 10):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/12/" + comboboxM.get()[-4:]
                GraphVal(link)
            for i in range(10, 32):
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/12/" + comboboxM.get()[-4:]
                GraphVal(link)
    if (radio_state.get() == 1):#Выбрана неделя, ох беда
        #print(comboboxW.get().replace(" - ", "",).replace(".", "/"))
        ran = comboboxW.get().replace(" - ", "/",).replace(".", "/") #Переводим дату в формат ДД/ММ/ГГДД/ММ/ГГ
        start = ran[:10:] #Начало недели
        end = ran[-10:] #Конец недели
        if start[3:5:] == end [3:5:]: #Если эта неделя находится в границах одной недели, то всё хорошо.
            dif = 7 #Нам нужны 7 дней после начала недели
        else:
            dif = abs(int(end[:2:]) - 7) #О нет, неделя в разных месяцах, dif - количество дней от этой недели в первом месяце
        for i in range(int(start[:2:]),int(start[:2:]) + dif): #Делаем ссылки для начала недели
            if i <= 9: #Число меньше 10, нужно добавить '0' в ссылку
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/" + start[3:5:] + "/" + start[-4:]
                GraphVal(link)
            else:
                link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(i) + "/" + start[3:5:] + "/" + start[-4:]
                GraphVal(link)
        for i in range(1, 7 - dif + 1): #Делаем ссылки для конца недели (Неделя не может залазить на другой месяц, и при этом заканчиватся на 10+ числа, исключение не требуется)
            link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=0" + str(i) + "/" + end[3:5:] + "/" + end[-4:]
            GraphVal(link)
    GraphSpawn() #отправили все ссылки, надеемся, что все результатаы записались, время создавать график


GraphBut = Button(tab2, text = "Построить график", command = GraphThingy) #Кнопка для запуска
GraphBut.grid(row = 5, column = 0, pady = 10, padx = 10)



"""
Третий столбик
"""
days = [] #Список дней для недели
mounths = [] #Список дней для месяца
kvarts = [] #Список кварталов
years = [] #Список годов

yearTitle = Label(tab2, text = "Выбор периода") #Надпись
yearTitle.grid(row = 0, column = 3, pady = 0, padx = 40)

comboboxW = Combobox(tab2) #Создание выпадающего списка с неделями
#comboboxW.grid(row = 1, column = 3, pady = 0)

comboboxM = Combobox(tab2) #Создание выпадающего списка с месяцами
comboboxM["values"] = (mounths)
#comboboxM.grid(row = 2, column = 3, pady = 0)

comboboxC = Combobox(tab2) #Создание выпадающего списка с кварталами
comboboxC["values"] = (kvarts)
#comboboxC.grid(row = 3, column = 3, pady = 0)

comboboxY = Combobox(tab2) #Создание выпадающего списка с годами
#comboboxY.grid(row = 4, column = 3, pady = 0)




"""
Второй столбик
"""

 #Заполняем все выпадающие списки
for i in range(0, 28, 7):
    days.append(sevendays(i))
for i in range(4):
    mounths.append(sevenmounth(i))
for i in range(0,12,3):
    kvarts.append(sevenkvart(i))
for i in range(4):
    years.append(sevenyears(i))



def Week(): #Выбрано поле с неделями, остальное убираем
    comboboxW["values"] = (days)
    comboboxW.grid(row = 1, column = 3, pady = 0)
    comboboxC.grid_remove()
    comboboxM.grid_remove()
    comboboxY.grid_remove()

def Mounth():#Выбрано поле с месяцами, остальное убираем

    comboboxM["values"] = (mounths)
    comboboxW.grid_remove()
    comboboxC.grid_remove()
    comboboxM.grid(row = 2, column = 3, pady = 0)
    comboboxY.grid_remove()

def Kvart(): #Выбрано поле с кварталами, остальное убираем

    comboboxC["values"] = (kvarts)
    comboboxW.grid_remove()
    comboboxC.grid(row = 3, column = 3, pady = 0)
    comboboxM.grid_remove()
    comboboxY.grid_remove()
def Year(): #Выбрано поле с годами, остальное убираем
    comboboxY["values"] = (years)
    comboboxW.grid_remove()
    comboboxC.grid_remove()
    comboboxM.grid_remove()
    comboboxY.grid(row = 4, column = 3, pady = 0)



Periodtitle = Label(tab2, text = "Период")#надпись
Periodtitle.grid(row = 0, column = 1, pady = 0, padx = 40)

radio_state = IntVar() #Штука в которой нужно выбирать переодичность (точки в кружочках)
radio_state.set(4)

radiobutton1 = Radiobutton(tab2, text = "Неделя",value = 1,variable = radio_state, command = Week)
radiobutton1.grid(row = 1, column = 1)
radiobutton2 = Radiobutton(tab2, text = "Месяц",value = 2,variable = radio_state, command = Mounth)
radiobutton2.grid(row = 2, column = 1)
radiobutton3 = Radiobutton(tab2, text = "Квартал",value = 3,variable = radio_state, command = Kvart)
radiobutton3.grid(row = 3, column = 1)
radiobutton4 = Radiobutton(tab2, text = "Год",value = 4,variable = radio_state, command = Year)
radiobutton4.grid(row = 4, column = 1)


def GraphSpawn(): #Рисует график
    global allDate
    global allVal
    if combobox3 == "Российский рубль": #Как рисовать график рубля от рубля? Никак не будем.
        for i in range(len(allVal)):
            allVal[i] = float(1.0)
    else:
        for i in range(len(allVal)):
            allVal[i] = float(allVal[i].replace(",", ".")) #Заменяем запятые в списке с значениями на точки
    matplotlib.use('TkAgg')
    fig = plt.figure()
    if radio_state.get() == 4: #делает красиво если выбран год
        allDate.clear()
        allDate = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]
    if radio_state.get() == 2: #делает красиво если выбран месяц
        allDate.clear()
        for i in range(len(allVal)):
            allDate.append(i)
    if radio_state.get() == 1: #делает красиво если выбрана неделя
        for i in range(len(allVal)):
            allDate[i] = allDate[i][:5:]
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master = tab2) #Штуки для графика, не знаю точно как оно работает
    plot_wiget = canvas.get_tk_widget()
    fig.clear()
    plt.plot(allDate, allVal) #x и y - списки значений абсциссы и ординаты #Запихиваем значения и смотрим рисунок
    plt.grid()
    plot_wiget.grid(row = 10, column = 10)

"""
Здесь заканчивается вторая вкладка
"""







tab_control.pack(expand = True, fill = BOTH)
window.mainloop() #отсюда запускается картинка