from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import time
import os
import psycopg2
from psycopg2 import Error
# from main import *

conn = None
cursor = None

try:
    f = open('query.txt')
    init_query = [line.strip() for line in f]
    query = '\n'.join(init_query)
    f.close()
except Exception as e:
    mb.showerror("Ошибка", "Не удалось загрузить скрипт для инициализации базы данных")
    exit(1)
try:
    f = open('key.txt')
    root_login, root_password = [line.strip() for line in f]
    f.close()
except Exception as e:
    mb.showerror("Ошибка", "Не удалось загрузить данные для подключения к базе данных")
    exit(1)

character_head_format = '{: <16}|{: <4}|{: <6}|{: <13}|{: <13}|{: <23}'
character_sep = '{:-<16}+{:-<4}+{:-<6}+{:-<13}+{:-<13}+{:-<23}'.format('', '', '', '', '', '')
ascendancy_head_format = '{: <13}|{: <23}|{: <16}|{: <16}|{: <11}'
ascendancy_sep = '{:-<13}+{:-<23}+{:-<16}+{:-<16}+{:-<11}'

##################################################################################################
def sql_base_class_search(base_class: str):
    cursor.execute("select * from base_class_search('{base_class}');".format(base_class=base_class))
    result = cursor.fetchall()
    return result


def sql_base_class_search_all(base_class: str):
    cursor.execute("select * from base_class_search_all('{base_class}');".format(base_class=base_class))
    result = cursor.fetchall()
    return result


def sql_main_skill_search(main_skill: str):
    cursor.execute("select * from main_skill_search('{main_skill}');".format(main_skill=main_skill))
    result = cursor.fetchall()
    return result


def sql_main_skill_search_all(main_skill: str):
    cursor.execute("select * from main_skill_search_all('{main_skill}');".format(main_skill=main_skill))
    result = cursor.fetchall()
    return result


def sql_show_all():
    cursor.execute("select * from show_all();")
    result = cursor.fetchall()
    return result


def sql_show_ascendancy_table():
    cursor.execute("select * from show_ascendancy_table();")
    result = cursor.fetchall()
    return result


def sql_show_character_table():
    cursor.execute("select * from show_character_table();")
    result = cursor.fetchall()
    return result


def sql_add_ascendancy(ascendancy_id: int, ascendancy: str, base_class: str, specialization: str):
    cursor.execute("call add_ascendancy({ascendancy_id}, '{ascendancy}', '{base_class}', '{specialization}');".format(
        ascendancy_id=ascendancy_id, ascendancy=ascendancy, base_class=base_class, specialization=specialization
    ))


def sql_add_character(name: str, lvl: int, life: int, energy_shield: int, ascendancy_id: int, main_skill: str):
    cursor.execute("call add_character('{name}', {lvl}, {life}, {energy_shield}, {ascendancy_id}, '{main_skill}');".format(
        name=name, lvl=lvl, life=life, energy_shield=energy_shield, ascendancy_id=ascendancy_id, main_skill=main_skill
    ))


def sql_delete_ascendancy(ascendancy_id: int):
    cursor.execute("call delete_ascendancy({ascendancy_id});".format(ascendancy_id=ascendancy_id))


def sql_delete_character(name: str):
    cursor.execute("call delete_character('{name}');".format(name=name))


def sql_delete_by_skill(main_skill: str):
    cursor.execute("call delete_by_skill('{main_skill}');".format(main_skill=main_skill))


def sql_delete_by_base_class(base_class: str):
    cursor.execute("call delete_by_base_class('{base_class}');".format(base_class=base_class))


def sql_delete_ascendancy_table():
    cursor.execute("call delete_ascendancy_table();")


def sql_delete_character_table():
    cursor.execute("call delete_character_table();")


def sql_update_ascendancy_table(ascendancy_id: int, ascendancy: str, base_class: str, specialization: str):
    cursor.execute("call update_ascendancy_table({ascendancy_id}, '{ascendancy}', '{base_class}', '{specialization}');".format(
        ascendancy_id=ascendancy_id, ascendancy=ascendancy, base_class=base_class, specialization=specialization
    ))


def sql_update_character_table(name: str, lvl: int, life: int, energy_shield: int, ascendancy_id: int, main_skill: str):
    cursor.execute("call update_character_table('{name}', {lvl}, {life}, {energy_shield}, {ascendancy_id}, '{main_skill}');".format(
        name=name, lvl=lvl, life=life, energy_shield=energy_shield, ascendancy_id=ascendancy_id, main_skill=main_skill
    ))


def sql_init_database(cursor, db_name: str, user: str, query):
    cursor.execute(query)
    # print('grant all privileges on all tables in schema public to {0};'.format(user))
    # cursor.execute('grant all privileges on all tables in schema public to {0};'.format(user))


def sql_create_database(user: str, password: str, db_name: str, query):
    conn = psycopg2.connect(user=root_login, password=root_password, host='localhost')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("select f_create_db('{0}', '{1}');".format(db_name, user))
    cursor.close()
    conn.close()
    # conn = psycopg2.connect(user=root_login, password=root_password, host='localhost', dbname=db_name)
    # conn.autocommit = True
    # cursor = conn.cursor()
    # sql_init_database(cursor, db_name, user, query)
    # cursor.close()
    # conn.close()
    conn = psycopg2.connect(user=user, password=password, host='localhost', dbname=db_name)
    conn.autocommit = True
    cursor = conn.cursor()
    sql_init_database(cursor, db_name, user, query)
    return conn, cursor


def sql_delete_database(db_name: str):
    conn = psycopg2.connect(user=root_login, password=root_password, host='localhost')
    conn.autocommit = True
    cursor = conn.cursor()
    # cursor.execute('drop database if exists {0};'.format(db_name))
    cursor.execute("select f_delete_db('{0}')".format(db_name))
    cursor.close()
    conn.close()
##################################################################################################


def create_database():
    # global cursor, conn
    # if cursor is not None:
    #     cursor.close()
    #     cursor = None
    # if conn is not None:
    #     conn.close()
    #     conn = None
    window = Toplevel()
    window.title('Создать базу данных')
    window.resizable(False, False)
    login_label = Label(window, text='login')
    login = Entry(window)
    login.delete(0, END)
    login_label.grid(row=0, column=0)
    login.grid(row=1, column=0)
    password_label = Label(window, text='password')
    password = Entry(window)
    password.delete(0, END)
    password_label.grid(row=0, column=1)
    password.grid(row=1, column=1)
    db_name_label = Label(window, text='Название базы данных')
    db_name = Entry(window)
    db_name.delete(0, END)
    db_name_label.grid(row=0, column=2)
    db_name.grid(row=1, column=2)

    def function():
        try:
            global cursor, conn
            if cursor is not None:
                cursor.close()
                cursor = None
            if conn is not None:
                conn.close()
                conn = None
            conn, cursor = sql_create_database(user=login.get(), password=password.get(), db_name=db_name.get(), query=query)
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except EXCEPTION:
            mb.showerror("Ошибка", "Не удалось подключиться")
            return

    button = Button(window, text='Создать', command=function)
    button.grid(row=2, column=0, columnspan=3)


def delete_database():
    global cursor, conn
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
    window = Toplevel()
    window.title('Удаление базы данных')
    window.resizable(False, False)
    label = Label(window, text='Введите название базы данных')
    label.grid(row=0, column=0)
    db_name = Entry(window)
    db_name.delete(0, END)
    db_name.grid(row=1, column=0)

    def function():
        global conn, cursor
        try:
            if cursor is not None:
                cursor.close()
                cursor = None
            if conn is not None:
                conn.close()
                conn = None
            sql_delete_database(db_name=db_name.get())
        except Error as e:
            cursor = conn = None
            mb.showerror("Ошибка", e.args[0])
            return
        except EXCEPTION as e:
            cursor = conn = None
            mb.showerror("Ошибка", "Не удалось подключиться")
            return
        conn = None
        cursor = None
        # print(conn, cursor)

    button = Button(window, text='Удалить', command=function)
    button.grid(row=2, column=0)


def show_character_table():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    result = sql_show_character_table()
    character_table.delete(0.0, END)
    # print(len(character_head_format.format('Name', 'Lvl', 'Life', 'EnergyShield', 'AscendancyId', 'Main Skill')))
    character_table.insert(0.0, character_head_format.format('Name', 'Lvl', 'Life', 'EnergyShield', 'AscendancyId', 'Main Skill'))
    character_table.insert(END, character_sep)
    for line in result:
        character_table.insert(END, character_head_format.format(*line))
    character_table.insert(END, character_sep)


def show_ascendancy_table():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    result = sql_show_ascendancy_table()
    ascendancy_table.delete(0.0, END)
    # print(len(ascendancy_head_format.format('AscendancyId', 'Ascendancy', 'Base Class', 'Specialization', 'Popularity')))
    ascendancy_table.insert(0.0, ascendancy_head_format.format('AscendancyId', 'Ascendancy', 'Base Class', 'Specialization', 'Popularity'))
    ascendancy_table.insert(END, ascendancy_sep.format('', '', '', '', ''))
    for line in result:
        ascendancy_table.insert(END, ascendancy_head_format.format(*line))
    ascendancy_table.insert(END, ascendancy_sep.format('', '', '', '', ''))


def clear_character_table():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    sql_delete_character_table()
    show_character_table()
    show_ascendancy_table()


def clear_ascendancy_table():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    sql_delete_ascendancy_table()
    show_character_table()
    show_ascendancy_table()


def add_character():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Добавить персонажа')
    window.resizable(False, False)
    name_label = Label(window, text='Name', width=15)
    name = Entry(window)
    name.delete(0, END)
    name_label.grid(row=0, column=0)
    name.grid(row=1, column=0)
    Label(window, text='Lvl').grid(row=0, column=1)
    lvl = Entry(window)
    lvl.delete(0, END)
    lvl.grid(row=1, column=1)
    Label(window, text='Life').grid(row=0, column=2)
    life = Entry(window, width=5)
    life.delete(0, END)
    life.grid(row=1, column=2)
    Label(window, text='ES', width=5).grid(row=0, column=3)
    es = Entry(window, width=5)
    es.delete(0, END)
    es.grid(row=1, column=3)
    Label(window, text='AscendancyId').grid(row=0, column=4)
    ascendancyId = Entry(window)
    ascendancyId.delete(0, END)
    ascendancyId.grid(row=1, column=4)
    Label(window, text='Main Skill').grid(row=0, column=5)
    main_skill = Entry(window, width=15)
    main_skill.delete(0, END)
    main_skill.grid(row=1, column=5)

    def function():
        try:
            sql_add_character(name.get(), lvl.get(), life.get(), es.get(), ascendancyId.get(), main_skill.get())
            show_character_table()
            show_ascendancy_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Добавить', command=function)
    button.grid(row=2, column=0, columnspan=5)


def add_ascendancy():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Добавить восхождение')
    window.resizable(False, False)
    Label(window, text='AscendancyId').grid(row=0, column=0)
    ascendancyId = Entry(window)
    ascendancyId.delete(0, END)
    ascendancyId.grid(row=1, column=0)
    Label(window, text='Ascendancy').grid(row=0, column=1)
    ascendancy = Entry(window)
    ascendancy.delete(0, END)
    ascendancy.grid(row=1, column=1)
    Label(window, text='Base Class').grid(row=0, column=2)
    base_class = Entry(window)
    base_class.delete(0, END)
    base_class.grid(row=1, column=2)
    Label(window, text='Specialization').grid(row=0, column=3)
    specialization = Entry(window)
    specialization.delete(0, END)
    specialization.grid(row=1, column=3)

    def function():
        try:
            sql_add_ascendancy(ascendancyId.get(), ascendancy.get(), base_class.get(), specialization.get())
            show_character_table()
            show_ascendancy_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
        return

    button = Button(window, text='Добавить', command=function)
    button.grid(row=3, column=0, columnspan=4)


def search_by_main_skill():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Поиск по main skill')
    Label(window, text='Main skill').grid(row=0, column=0)
    main_skill = Entry(window)
    main_skill.delete(0, END)
    main_skill.grid(row=1, column=0)

    def function():
        try:
            result = sql_main_skill_search(main_skill.get())
            character_table.delete(0.0, END)
            character_table.insert(0.0,
                                   character_head_format.format('Name', 'Lvl', 'Life', 'EnergyShield', 'AscendancyId',
                                                                'Main Skill'))
            character_table.insert(END, character_sep)
            for line in result:
                character_table.insert(END, character_head_format.format(*line))
            character_table.insert(END, character_sep)
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Найти', command=function)
    button.grid(row=2, column=0, columnspan=5)


def search_by_base_class():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Поиск по base skill')
    Label(window, text='Base class').grid(row=0, column=0)
    base_class = Entry(window)
    base_class.delete(0, END)
    base_class.grid(row=1, column=0)

    def function():
        try:
            result = sql_base_class_search(base_class.get())
            ascendancy_table.delete(0.0, END)
            ascendancy_table.insert(0.0, ascendancy_head_format.format('AscendancyId', 'Ascendancy', 'Base Class',
                                                                       'Specialization', 'Popularity'))
            ascendancy_table.insert(END, ascendancy_sep.format('', '', '', '', ''))
            for line in result:
                ascendancy_table.insert(END, ascendancy_head_format.format(*line))
            ascendancy_table.insert(END, ascendancy_sep.format('', '', '', '', ''))
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Найти', command=function)
    button.grid(row=2, column=0, columnspan=5)


def update_character():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Изменить персонажа\nЧтобы оставить поле неизменным\nоставьте его пустым для текстовых полей\nили введите -1 для численных')
    window.resizable(False, False)
    name_label = Label(window, text='Name', width=15)
    name = Entry(window)
    name.delete(0, END)
    name_label.grid(row=0, column=0)
    name.grid(row=1, column=0)
    Label(window, text='Lvl').grid(row=0, column=1)
    lvl = Entry(window)
    lvl.delete(0, END)
    lvl.insert(END, '-1')
    lvl.grid(row=1, column=1)
    Label(window, text='Life').grid(row=0, column=2)
    life = Entry(window, width=5)
    life.delete(0, END)
    life.insert(END, '-1')
    life.grid(row=1, column=2)
    Label(window, text='ES', width=5).grid(row=0, column=3)
    es = Entry(window, width=5)
    es.delete(0, END)
    es.insert(END, '-1')
    es.grid(row=1, column=3)
    Label(window, text='AscendancyId').grid(row=0, column=4)
    ascendancyId = Entry(window)
    ascendancyId.delete(0, END)
    ascendancyId.insert(END, '-1')
    ascendancyId.grid(row=1, column=4)
    Label(window, text='Main Skill').grid(row=0, column=5)
    main_skill = Entry(window, width=15)
    main_skill.delete(0, END)
    main_skill.grid(row=1, column=5)

    def function():
        try:
            sql_update_character_table(name.get(), lvl.get(), life.get(), es.get(), ascendancyId.get(), main_skill.get())
            show_character_table()
            show_ascendancy_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Изменить', command=function)
    button.grid(row=2, column=0, columnspan=5)


def update_ascendancy():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Изменить восхождение\nЧтобы оставить поле неизменным\nоставьте его пустым для текстовых полей\nили введите -1 для численных')
    window.resizable(False, False)
    Label(window, text='AscendancyId').grid(row=0, column=0)
    ascendancyId = Entry(window)
    ascendancyId.delete(0, END)
    ascendancyId.grid(row=1, column=0)
    Label(window, text='Ascendancy').grid(row=0, column=1)
    ascendancy = Entry(window)
    ascendancy.delete(0, END)
    ascendancy.grid(row=1, column=1)
    Label(window, text='Base Class').grid(row=0, column=2)
    base_class = Entry(window)
    base_class.delete(0, END)
    base_class.grid(row=1, column=2)
    Label(window, text='Specialization').grid(row=0, column=3)
    specialization = Entry(window)
    specialization.delete(0, END)
    specialization.grid(row=1, column=3)

    def function():
        try:
            sql_update_ascendancy_table(ascendancyId.get(), ascendancy.get(), base_class.get(), specialization.get())
            # show_character_table()
            show_ascendancy_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
        return

    button = Button(window, text='Изменить', command=function)
    button.grid(row=3, column=0, columnspan=4)


def delete_character_be_main_skill():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Удалить по main skill')
    Label(window, text='Main skill').grid(row=0, column=0)
    main_skill = Entry(window)
    main_skill.delete(0, END)
    main_skill.grid(row=1, column=0)

    def function():
        try:
            sql_delete_by_skill(main_skill.get())
            show_character_table()
            show_ascendancy_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Удалить', command=function)
    button.grid(row=2, column=0, columnspan=5)


def delete_ascendancy_by_base_class():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Удаление по base skill')
    Label(window, text='Base class').grid(row=0, column=0)
    base_class = Entry(window)
    base_class.delete(0, END)
    base_class.grid(row=1, column=0)

    def function():
        try:
            sql_delete_by_base_class(base_class.get())
            show_character_table()
            show_character_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Удалить', command=function)
    button.grid(row=2, column=0, columnspan=5)


def delete_character():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Удалить персонажа')
    window.resizable(False, False)
    Label(window, text='Имя персонажа').grid(row=0, column=0)
    name = Entry(window)
    name.delete(0, END)
    name.grid(row=1, column=0)

    def function():
        try:
            sql_delete_character(name.get())
            show_character_table()
            show_character_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Удалить', command=function)
    button.grid(row=2, column=0)


def delete_ascendancy():
    global conn, cursor
    if conn is None or cursor is None:
        mb.showerror("Ошибка", "База данных не выбрана")
        return
    window = Toplevel()
    window.title('Удалить восхождение')
    window.resizable(False, False)
    Label(window, text='AscendancyId').grid(row=0, column=1)
    ascendancyId = Entry(window)
    ascendancyId.delete(0, END)
    ascendancyId.grid(row=0, column=1)

    def function():
        try:
            sql_delete_ascendancy(ascendancyId.get())
            show_character_table()
            show_character_table()
        except Error as e:
            mb.showerror("Ошибка", e.args[0])
            return
        except Exception as e:
            mb.showerror("Ошибка", "Ошибка")
            return

    button = Button(window, text='Удалить', command=function)
    button.grid(row=2, column=0)


root = Tk()
root.title('POE statistics')
root.resizable(False, False)
main_menu = Menu(root)
root.config(menu=main_menu)

database_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Действия в базой данных', menu=database_menu)
database_menu.add_command(label='Создать базу данных', command=create_database)
database_menu.add_command(label='Удалить дазу данных', command=delete_database)

character_database_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Персонажи', menu=character_database_menu)
character_database_menu.add_command(label='Очистить таблицу', command=clear_character_table)
character_database_menu.add_command(label='Добавить персонажа', command=add_character)
character_database_menu.add_command(label='Поиск по main skill', command=search_by_main_skill)
character_database_menu.add_command(label='Изменить запись', command=update_character)
character_database_menu.add_command(label='Удалить запись по main skill', command=delete_character_be_main_skill)
character_database_menu.add_command(label='Удалить персонажа', command=delete_character)
character_database_menu.add_command(label='Показать таблицу', command=show_character_table)

ascendancy_database_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Восхождения', menu=ascendancy_database_menu)
ascendancy_database_menu.add_command(label='Очистить таблицу', command=clear_ascendancy_table)
ascendancy_database_menu.add_command(label='Добавить восхождение', command=add_ascendancy)
ascendancy_database_menu.add_command(label='Поиск по base class', command=search_by_base_class)
ascendancy_database_menu.add_command(label='Изменить запись', command=update_ascendancy)
ascendancy_database_menu.add_command(label='Удалить запись по base class', command=delete_ascendancy_by_base_class)
ascendancy_database_menu.add_command(label='Удалить восхождение', command=delete_ascendancy)
ascendancy_database_menu.add_command(label='Показать таблицу', command=show_ascendancy_table)

character_frame = Frame(root)
character_table_name = Label(text='Персонажи')
character_table_name.grid(row=0, column=0)
character_frame.grid(row=1, column=0)
character_table = Text(character_frame, width=80, height=20, wrap=WORD)
character_table.pack(side=LEFT)
character_scroll = Scrollbar(character_frame, command=character_table.yview)
character_scroll.pack(side=LEFT, fill=Y)
character_table.config(yscrollcommand=character_scroll.set)

ascendancy_frame = Frame(root)
ascendancy_table_name = Label(text='Восхождения')
ascendancy_table_name.grid(row=0, column=1)
ascendancy_frame.grid(row=1, column=1)
ascendancy_table = Text(ascendancy_frame, width=83, height=20, wrap=WORD)
ascendancy_table.pack(side=LEFT)
ascendancy_scroll = Scrollbar(ascendancy_frame, command=ascendancy_table.yview)
ascendancy_scroll.pack(side=LEFT, fill=Y)
ascendancy_table.config(yscrollcommand=ascendancy_scroll.set)

root.mainloop()


