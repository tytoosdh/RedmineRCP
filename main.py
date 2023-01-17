import tkinter
from datetime import date
import configparser
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showerror

from redminelib import Redmine
import json
from unidecode import unidecode

import tkinter as tk
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

from tkcalendar import Calendar
from datetime import date
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *  # Additional Import

### DEFINICJE WSZYTKICH FUNKCJI
# menu


def aboutapp():  # POPUP z informacją o programie
    showinfo("About", "Redmine - Rejestracja Czasu Pracy \n Wersja: 0.9.2 \n Autor: Daniel Hopej, 2022")


def openconfig():  # otwiera notatnik z konfiguracją
    subprocess.Popen(["notepad", 'redmine.config'])


def select_issue(e):  #
    projektString = projects_combo.get()
    projektArray = projektString.split(' ')
    projektId = int(projektArray[0])
    if type(projektId) == int:
        listaZadan = issuesList(conn, projektId)
        listaAktywnosci = activityList(conn, projektId)
    else:
        listaZadan = ['-']
    issue_combo.config(values=listaZadan)
    listaAkt_combo.config(values=listaAktywnosci)
    issue_combo.current(0)
    listaAkt_combo.current(2)
    label_project["text"] = projektId
    projId.set(projektId)
    aktywnosc = listaAkt_combo.get()
    aktywnowscArray = aktywnosc.split(' ')
    aktywnoscId = int(aktywnowscArray[0])
    label_activity["text"] = aktywnoscId
    print(projektId)


def get_issue_id(e):
    issueString = issue_combo.get()
    issueArray = issueString.split(' ')
    issueId = int(issueArray[0])
    label_issue["text"] = issueId
    issId.set(issueId)


def get_hour(e):
    hours = hour_combo.get()
    label_hour["text"] = hours


def get_min(e):
    minutes = min_combo.get()
    label_minutes["text"] = minutes


def get_miesiac(e):
    miesiac = mies_combo.get()
    label_miesiac["text"] = miesiac


def get_wykon(e):
    wykon = listaWyk_combo.get()
    label_wykon["text"] = wykon


def get_activity(e):
    aktywnosc = listaAkt_combo.get()
    aktywnowscArray = aktywnosc.split(' ')
    aktywnoscId = int(aktywnowscArray[0])
    label_activity["text"] = aktywnoscId


def getValue():

    # TODO: pobieranie wartości z faktycznych pól a nie etykiet testowych
    #zadanieId = issId.get()
    zadanieId = str(label_issue.cget("text"))
    print("ZadanieID: " + zadanieId)
    data = cal.get_date()
    godzin = hour_combo.get()
    minut = min_combo.get()
    opis_wyk_lista = label_wykon.cget("text")
    opis_wyk = opis.get()

    if opis_wyk_lista != '-':
        opis_wyk = opis_wyk_lista + " " + opis_wyk
    else:
        opis_wyk = opis_wyk

    czasW = godzin + "h" + minut +"m"
    wpis = zadanieId + " - " + data + " - " + godzin + "h - " + minut + "min " + opis_wyk
    miesDoRoz = mies_combo.get()
    print(wpis)
    label_test.config(text=wpis)
    activity = label_activity.cget("text")
    dodajWpis = addTimeEntry(conn, zadanieId, data, opis_wyk, czasW, miesDoRoz, activity)
    if dodajWpis == True:
        popup_OK()
    else:
        popup_ERROR()


def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())


def popup_OK():
    showinfo("Info", "Wpis dodany poprawnie!")


def popup_ERROR():
    showerror("Błąd", "Coś poszło nie tak!! Sprawdź poprawność wprowadzonych danych")


def print_sel(e):
    data_wybrana = cal.get_date()
    print(data_wybrana)
    timeEntryTable(conn, tabelaFrame, getCurrentUserId(conn), data_wybrana)


def redmineConnect():
    try:
        # pobranie konfiguracji z pliku redmine.config
        config = configparser.ConfigParser()
        config.read('redmine.config')
        host = config['redmine']['host']
        api_key = config['redmine']['api_key']
        if api_key != '':
            redmine_conn = Redmine(f'{host}', requests={'verify': False}, key=f'{api_key}')
        else:
            showerror("Brak API KEY", "Brak klucza API, sprawdź plik redmine.config!")
        return redmine_conn
        pass
    except:
        showerror("Błąd połączenia", "Błąd połaczenia do Redmine!")


def projectsList(rmconn):
    projectList = ["-"]
    for project in rmconn.project.all():
        #print(str(project.id) + " - " + project.name)
        projectList.append(str(project.id) + " - " + project.name)
    return projectList


def issuesList(rmconn, project):
    issueList = ["-"]
    issueId = ''
    issueName = ''
    project = rmconn.project.get(f'{project}')
    for issue in project.issues:
        issueId = str(issue.internal_id)
        issueName = str(issue)
        #tekst = issueString.split(" ")
        #print(issue)
        #issueList.append(issue)
        issueList.append(issueId + " - " + issueName)
    return issueList


def issueName(rmconn, project, issueid):
    issueName = ''
    project = rmconn.project.get(f'{project}')
    for issue in project.issues:
        # print(issue.internal_id)
        # print(issueid)
        # print(int(issue.internal_id) == int(issueid))
        if int(issue.internal_id) == int(issueid):
            issueName = str(issue)
            print(issueName)
    return issueName

def convert_tuple_to_list(tup):
    brand_new_list = []
    for element in tup:
        brand_new_list.append(element)
    return brand_new_list


def activityList(rmconn, project):
    activityList = []
    project = rmconn.project.get(f'{project}', include=['time_entry_activities'])
    list = convert_tuple_to_list(project)
    # print(list)
    list2 = convert_tuple_to_list(list[10])
    list3 = convert_tuple_to_list(list2[1])
    print(list3)
    print(json.dumps(list3))

    for entry in list3:
        activityList.append(str(entry['id']) + " - " + str(entry['name']))

    print(activityList)
    return activityList

def hourTime():
    hourList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return hourList


def minTime():
    minList = [0, 15, 30, 45]
    return minList



# def pobierz_slownik():
#     config = configparser.ConfigParser()
#     config.read('redmine.config')
#     slownik = config['slownik']['opis_wykonania']
#     slownik_wykonania = slownik.split("#")
#     print(slownik_wykonania)


def miesiacDoRozliczen():
    config = configparser.ConfigParser()
    config.read('redmine.config')
    slownik = config['slownik']['miesiac_do_rozliczen']
    slownik_miesiac = slownik.split("#")
    print(slownik_miesiac)
    return slownik_miesiac


def opis_wykonania():
    opis_wykonania = ['']
    config = configparser.ConfigParser()
    config.read('redmine.config', encoding="utf-8")
    slownik = config['slownik']['opis_wykonania']
    opis_wykonania = slownik.split("#")

    print(str(opis_wykonania))
    return opis_wykonania


def getCurrentUserId(conn):
    user = conn.user.get('current')
    userId = user.id
    print(userId)
    return userId


def addTimeEntry(conn, issueId, dataW, komentarz, czasW, miesDoRoz, activity):
    try:
        new_time_entry = conn.time_entry.new()
        new_time_entry.issue_id = issueId
        new_time_entry.spent_on = dataW
        new_time_entry.comments = komentarz
        new_time_entry.hours = czasW
        new_time_entry.custom_fields = [{'id': 33, 'value': f'{miesDoRoz}'}] # miesiąc do rozliczenia
        new_time_entry.activity_id = activity
        new_time_entry.save()
        print("OK - wpis dodany")
        return True
        pass
    except:
        return False


def getDayTimeEntry(conn, userid, data):
    suma = 0
    time_entries = conn.time_entry.filter(user_id=userid, from_date=data, to_date=data)
    for time_entry in time_entries:
        print(time_entry.project)
        print(time_entry.comments)
        print(time_entry.hours)
        suma = suma + time_entry.hours

        #print(time_entries)
        print(suma)

        time = suma
        hours = int(time)
        minutes = (time * 60) % 60.
        seconds = (time * 3600) % 60.
        print("%d:%02d" % (hours, minutes))
        #pass
        #return suma


def convertTime(time):
    hours = int(time)
    minutes = (time * 60) % 60.
    seconds = (time * 3600) % 60.
    time_conv = "%d:%02d" % (hours, minutes)
    return time_conv

def timeEntryTable(conn, ws, userid, data):

    for widget in ws.winfo_children():
        widget.destroy()

    list = ttk.Treeview(ws)

    list['columns'] = ('Projekt', 'Zadanie', 'Opis działania', 'Czas')

    list.column("#0", width=0, stretch=NO)
    list.column("Projekt", anchor=W, width=250)
    list.column("Zadanie", anchor=W, width=250)
    list.column("Opis działania", anchor=W, width=300)
    list.column("Czas", anchor=E, width=50)

    list.heading("#0", text="", anchor=CENTER)
    list.heading("Projekt", text="Projekt", anchor=CENTER)
    list.heading("Zadanie", text="Zadanie", anchor=CENTER)
    list.heading("Opis działania", text="Opis działania", anchor=CENTER)
    list.heading("Czas", text="Czas", anchor=W)

    suma = 0
    iid = 0
    time_entries = conn.time_entry.filter(user_id=userid, from_date=data, to_date=data)
    for time_entry in time_entries:
        project = time_entry.project
        projectid = project.id
        issue = time_entry.issue
        issue_name = issueName(conn, projectid, issue)
        comments = time_entry.comments
        hours = time_entry.hours
        list.insert(parent='', index='end', iid=iid, text='',
                values=(project, issue_name, comments, convertTime(hours)))
        suma = suma + time_entry.hours
        iid = iid + 1

    list.insert(parent='', index='end', iid=iid, text='',
                values=('-', '-', 'Suma', convertTime(suma)))

    list.pack()
### KONIEC DEFINICJI FUNKCJI

# połączenie do Redmine
conn = redmineConnect()

# utworzenie okna Tk i przypisanie ikony
root = Tk()
root.iconbitmap('redmine_ico.ico')

# zainicjowanie menu
menubar = Menu(root)
# definicja menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Otwórz plik konfiguracji", command=openconfig)
filemenu.add_separator()
filemenu.add_command(label="Zamknij", command=root.quit)
menubar.add_cascade(label="Plik", menu=filemenu)
####
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="O programie...", command=aboutapp)
menubar.add_cascade(label="Pomoc", menu=helpmenu)

# TODO: popracować nad interfejsem

frame_up = LabelFrame(root, text='Rejestracja działania', padx=5, pady=5, relief=RAISED)
frame_down = LabelFrame(root, text='Wykonane działania', padx=5, pady=5, relief=RAISED)
frame_footer = LabelFrame(root, text='Testowa', padx=5, pady=5)

frame_up.pack(side=TOP)
frame_down.pack(side=TOP)
frame_footer.pack(side=BOTTOM)

frame_up_left = Frame(frame_up, padx=5, pady=5, border=TRUE, borderwidth=2)
frame_up_right = Frame(frame_up, padx=5, pady=5)
frame_up_left.pack(side=LEFT)
separator = ttk.Separator(frame_up, orient='vertical')
separator.pack(fill='y')
frame_up_right.pack(side=RIGHT)

calendarFrame = Frame(frame_up_left, padx=5, pady=5)
calendarFrame.pack(side=TOP)

valuesFrame = Frame(frame_footer)
#valuesFrame.pack(side=BOTTOM)
valuesFrame.pack_forget()

projectFrame = Frame(frame_up_right)
projectFrame.pack(side=TOP)

issueFrame = Frame(frame_up_right)
issueFrame.pack(side=TOP)

timeFrame = Frame(frame_up_right)
timeFrame.pack(side=TOP)

dzialanieFrame = Frame(frame_up_right)
dzialanieFrame.pack(side=TOP)

dzialanie2Frame = Frame(frame_up_right)
dzialanie2Frame.pack(side=TOP)

dzialanie2Frame = Frame(frame_up_right)
dzialanie2Frame.pack(side=TOP)

aktywnoscFrame = Frame(frame_up_right)
aktywnoscFrame.pack(side=TOP)

tabelaFrame = Frame(frame_down)
tabelaFrame.pack(side=TOP)

root.title('Redmine - Rejestracja Czasu Pracy (v. 0.9.2)')
root.geometry("900x520")
root.resizable(False, False)

projects = projectsList(conn)
print(projects[0])



#Calendar
today = date.today()

today_day = today.day
today_month = today.month
today_year = today.year
cal = Calendar(calendarFrame, selectmode='day',
               year=today_year, month=today_month,
               day=today_day, date_pattern='y-mm-dd', locale="pl_PL")

cal.pack(side=TOP, pady=10)
cal.bind("<<CalendarSelected>>", print_sel)

timeEntryTable(conn, tabelaFrame, getCurrentUserId(conn), today)

# pole daty
#date = Label(root, text="")
#date.pack(pady=20)

# Add Button and Label
#Button(root, text="Get Date",
#       command=grad_date).pack(pady=20)

#Create a drop box - projekty
Label(projectFrame, text="Projekt   ").pack(side=LEFT)
projects_combo = ttk.Combobox(projectFrame, value=projects, width="300")
projects_combo.current(0)
projects_combo.pack(side=LEFT, pady=5)
# bind the combobox
projects_combo.bind("<<ComboboxSelected>>", select_issue)

#Second drop box - zadania
Label(issueFrame, text="Zadanie ").pack(side=LEFT)
issue_combo = ttk.Combobox(issueFrame, value=[], width="300")
#issue_combo.current(0)
issue_combo.pack(side=LEFT, pady=5)
issue_combo.bind("<<ComboboxSelected>>", get_issue_id)

# lista godzin
Label(timeFrame, text="Godziny").pack(side=LEFT)
listaGodzin = hourTime()
hour_combo = ttk.Combobox(timeFrame, value=listaGodzin, width=20, justify=LEFT)
hour_combo.set(listaGodzin[0])
hour_combo.pack(side=LEFT, pady=5)
hour_combo.bind("<<ComboboxSelected>>", get_hour)
# lista minut
Label(timeFrame, text="Minuty").pack(side=LEFT)
listaMinut = minTime()
min_combo = ttk.Combobox(timeFrame, value=listaMinut, width=20, justify=LEFT)
min_combo.set(listaMinut[0])
min_combo.pack(side=LEFT, pady=5)
min_combo.bind("<<ComboboxSelected>>", get_min)

#miesiac do rozliczen
Label(timeFrame, text="Miesiąc do rozliczeń").pack(side=LEFT)
listaMiesiac = miesiacDoRozliczen()
mies_combo = ttk.Combobox(timeFrame, value=listaMiesiac, width=60)
mies_combo.set(listaMiesiac[0])
mies_combo.pack(side=LEFT, pady=5)
mies_combo.bind("<<ComboboxSelected>>", get_miesiac)

#opis działania z listy
Label(dzialanieFrame, text="Wykonanie z listy").pack(side=LEFT)
listaWykonania = opis_wykonania()
listaWyk_combo = ttk.Combobox(dzialanieFrame, value=listaWykonania, width=100)
listaWyk_combo.set(listaWykonania[0])
listaWyk_combo.pack(side=LEFT, pady=5)
listaWyk_combo.bind("<<ComboboxSelected>>", get_wykon)

# opis działania
Label(dzialanie2Frame, text="i/lub dodatkowy opis").pack(side=LEFT)
opis = StringVar()
entry = Entry(dzialanie2Frame, textvariable=opis, width=100).pack(side=LEFT, pady=5)

#opis activity
Label(aktywnoscFrame, text="Aktywność").pack(side=LEFT)
listaAktywnosci = opis_wykonania()
listaAkt_combo = ttk.Combobox(aktywnoscFrame, value=[], width=100)
#listaAkt_combo.set(listaWykonania[0])
listaAkt_combo.pack(side=LEFT, pady=5)
listaAkt_combo.bind("<<ComboboxSelected>>", get_activity)

Button(frame_up_right, text="Dodaj wpis",
       command=getValue).pack(pady=5)

#timeEntryTable(conn, tabelaFrame, getCurrentUserId(conn), '2022-09-20')

#dolna belka z wartościami wybranymi
#values_frame = Frame(root, borderwidth=2)

projId = StringVar()
Label(valuesFrame, textvariable=projId).pack(side=LEFT, pady=10)
projId.set("projectid")

issId = StringVar()
Label(valuesFrame, textvariable=issId).pack(side=LEFT, pady=10)
issId.set("issueid")

label_userId = Label(valuesFrame, text=getCurrentUserId(conn))
label_userId.pack(side=LEFT, pady=10)
label_project = Label(valuesFrame, text="")
label_project.pack(side=LEFT, pady=10)
label_issue = Label(valuesFrame, text="")
label_issue.pack(side=LEFT, pady=10)
label_hour = Label(valuesFrame, text="0")
label_hour.pack(side=LEFT, pady=10)
label_minutes = Label(valuesFrame, text="0")
label_minutes.pack(side=LEFT, pady=10)
label_miesiac = Label(valuesFrame, text=mies_combo.get())
label_miesiac.pack(side=LEFT, pady=10)
label_wykon = Label(valuesFrame, text=listaWyk_combo.get())
label_wykon.pack(side=LEFT, pady=10)
label_activity = Label(valuesFrame, text=listaWyk_combo.get())
label_activity.pack(side=LEFT, pady=10)

label_test = Label(valuesFrame, text="Etykieta testowa0")
label_test.pack(side=LEFT, pady=10)

root.config(menu=menubar)
root.mainloop()