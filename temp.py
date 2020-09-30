#Подключение модулей
from tkinter import *
from tkinter.ttk import Combobox 
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


#Объявление класса главного фрейма
class Main(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db #подключение созданной БД
        self.init_main()
       
    def init_main(self):
        #создание виджетов и фремов для их упаковки
        f_top = Frame(root) 
        f_bot = Frame(root)
        
        self.b_change_tov = Button(f_top, text="Измение товара", width=20, height=2, command=self.change_tov)
        b_change_shop = Button(f_top, text="Добавить магазин", width=20, height=2, command=self.change_shop)
        b_calculation = Button(f_bot, text="Расчет", width=20, height=2, command=self.calculation)
        
        #размещение виджетов
        f_top.pack()
        f_bot.pack()
        self.b_change_tov.pack(side=LEFT, pady=30)
        b_change_shop.pack(side=LEFT)
        b_calculation.pack(side=LEFT)
        
        self.db.create_table_tov() #создание таблицы товаров
        self.db.create_table_shop() #создание таблицы магазинов
        self.db.create_table_calculation() #создание таблицы поступлений
        
    #функция вызова класса(нового окна) изменения товаров
    def change_tov(self):
        Main_change_tov()
        
    #функция вызова класса(нового окна) добавления магазинов
    def change_shop(self):
        Main_change_shop()
    
    #функция вызова класса(нового окна) добавления приходов и произведения расчетов
    def calculation(self):
        self.db.cursorObj.execute('''SELECT count(*) from tov''')
        if str(self.db.cursorObj.fetchone()[0]) != '0':
            Main_calculation()
        else:
            messagebox.showerror('Ошибка', 'Введите данные в таблицу товаров и магазинов')
        
  
      
#Объявление класса окна изменения товара    
class Main_change_tov(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db #подключение созданной БД
        self.init_main_change_tov()
      
    def init_main_change_tov(self):
        #задание параметров окна
        self.title("Изменение товара")
        self.geometry("580x480+300+100")
    
        #создание виджетов и фремов для их упаковки
        t_bot = Frame(self)
        t_top = Frame(self)
        f_top = Frame(t_bot) 
        f_mid = Frame(t_bot)
        f_bot = Frame(t_bot)
        
        l_tov = Label(f_top, text="Новый товар")
        l_cost = Label(f_top, text="Цена")
        self.e_tov = Entry(f_mid, width=10)
        self.e_costs = Entry(f_mid, width=10) 
        b_invite = Button(f_bot, text="Добавить", width=20, height=2, command=self.invite)
        b_delite = Button(f_bot, text="Удалить", width=20, height=2, command=self.delite)
        self.tree = ttk.Treeview(t_top, columns=('ID', 'name', 'costs'), height=15, show='headings')
        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('name', width=265, anchor=CENTER)
        self.tree.column('costs', width=150, anchor=CENTER)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Наименование')
        self.tree.heading('costs', text='Цена')
    
        scroll = ttk.Scrollbar(t_top, orient="vertical", command=self.tree.yview)
        #размещение виджетов
        t_top.pack()
        self.tree.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scroll.set)
        
        t_bot.pack(pady=20)
        f_top.pack(side=LEFT)
        f_mid.pack(side=LEFT, padx=20)
        f_bot.pack(side=LEFT, padx=40)
        l_tov.pack()
        l_cost.pack(pady=5)
        self.e_tov.pack()
        self.e_costs.pack(pady=5)
        b_invite.pack()
        b_delite.pack()
        
        #фиксация на фрейме дочернего окна
        self.grab_set()
        self.focus_set()
        
        self.print_table() #функция начального отображения таблицы товаров
    
    #функция добавления элемента в таблицу
    def invite(self):
        '''И проверки существования'''
        self.db.cursorObj.execute('''SELECT count(*) FROM tov WHERE name =?''', (self.e_tov.get(),))
        if str(self.db.cursorObj.fetchone()[0]) != '0':
            messagebox.showerror('Ошибка', 'Данный товар уже существует')
        elif self.e_tov.get() == '':
            messagebox.showerror('Ошибка', 'Введите название товара')
        elif is_number(self.e_costs.get()):
            self.db.insert_table_tov(self.e_tov.get(), self.e_costs.get()) #заполнение таблицы SQL
            self.print_table()
            self.e_tov.delete(0, END)
            self.e_costs.delete(0, END)
        else:
            messagebox.showerror('Ошибка', 'В поле "цена" ведено не число')

    #функция удаления элемента в таблицу        
    def delite(self):
        for selection_item in self.tree.selection():
            self.db.cursorObj.execute('''DELETE FROM tov WHERE ID =?''', (self.tree.set(selection_item, '#1'),)) #удаляем все выделенные элементы в виджете tree
        self.db.conn.commit()
        self.print_table()
            
    #функция начального отображения таблицы товаров    
    def print_table(self):
        self.db.cursorObj.execute('''SELECT * FROM tov''')
        [self.tree.delete(i) for i in self.tree.get_children()] #удаление всей таблицы из виджета
        [self.tree.insert('', 'end', values=row) for row in self.db.cursorObj.fetchall()] #заполнение обновленными данными 
            

#Объявление класса окна добавления магазина
class Main_change_shop(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db #подключение созданной БД 
        self.init_main_change_shop()    
        
    def init_main_change_shop(self):
        #задание параметров окна
        self.title("Добавление/удаление магазина")
        self.geometry("400x460+400+150")
    
        #создание виджетов и фремов для их упаковки
        f_top = Frame(self) 
        f_bot = Frame(self) 
    
        self.l_shop = Label(f_top, text="Укажите магазин")
        self.e_shop = Entry(f_top, width=20)
        b_invite = Button(self, text="Добавить", width=20, height=2, command=self.invite)
        b_delite = Button(self, text="Удалить", width=20, height=2, command=self.delite)
        self.tree = ttk.Treeview(f_bot, columns=('ID', 'shop'), height=15, show='headings')
        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('shop', width=265, anchor=CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('shop', text='Магазин')
        
        scroll = ttk.Scrollbar(f_bot, orient="vertical", command=self.tree.yview)
        
        #размещение виджетов
        f_bot.pack()
        self.tree.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scroll.set)
        
        f_top.pack(pady=10)
        self.l_shop.pack(side=LEFT)
        self.e_shop.pack(side=LEFT)
        b_invite.pack()
        b_delite.pack()
    
        #фиксация на фрейме дочернего окна
        self.grab_set()
        self.focus_set()
        
        self.print_table() #функция начального отображения таблицы магазинов
    
    #функция добавления элемента в таблицу    
    def invite(self):
        self.db.cursorObj.execute('''SELECT count(*) FROM shop WHERE name =?''', (self.e_shop.get(),))
        if str(self.db.cursorObj.fetchone()[0]) != '0':
            messagebox.showerror('Ошибка', 'Данный магазин уже существует')
        elif self.e_shop.get() == '':
            messagebox.showerror('Ошибка', 'Введите название магазина')
        else:
            self.db.insert_table_shop(self.e_shop.get()) #заполнение таблицы SQL
            self.print_table()
            self.e_shop.delete(0, END)

    #функция удаления элемента в таблицу
    def delite(self):
        for selection_item in self.tree.selection():
            self.db.cursorObj.execute('''DELETE FROM shop WHERE ID =?''', (self.tree.set(selection_item, '#1'),)) #удаляем все выделенные элементы в виджете tree
        self.db.conn.commit()
        self.print_table()
        
    #функция начального отображения таблицы магазинов     
    def print_table(self):
        self.db.cursorObj.execute('''SELECT * FROM shop''')
        [self.tree.delete(i) for i in self.tree.get_children()] #удаление всей таблицы из виджета
        [self.tree.insert('', 'end', values=row) for row in self.db.cursorObj.fetchall()] #заполнение обновленными данными
  
    
#Объявление класса окна вычислений   
class Main_calculation(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db #подключение созданной БД
        self.init_main_calculation()   
     
    def init_main_calculation(self):
        #задание параметров окна
        self.title("Расчет")
        self.geometry("800x630+250+50")
        
        #создание виджетов и фремов для их упаковки 
        t_mid = Frame(self)
        f_mid = Frame(self)
        f_top = Frame(self) 
        f_bot = Frame(self)   
    
        l_shop = Label(f_mid, text="Выберите магазин")
        l_name = Label(f_top, text="Товар")
        l_count = Label(f_top, text="Колличество")
        l_inv_del = Label(f_top, text="Поступление/Возврат")
        l_calculation = Label(self)
        self.l_result = Label(self)
        self.e_count = Entry(f_bot, width=23)
        self.combo_name = Combobox(f_bot, state='readonly')
        self.combo_inv_del = Combobox(f_bot, state='readonly')
        self.combo_inv_del['values'] = ("Поступление", "Возврат")  
        self.combo_inv_del.current(0)
        self.combo_shop = Combobox(f_mid, state='readonly')
        b_invite = Button(self, text="Добавить", width=20, height=2, command=self.invite)
        b_delite = Button(self, text="Удалить", width=20, height=2, command=self.delite)
        b_change = Button(self, text="Очистить таблицу", width=20, height=2, command=self.change)
        b_calculation = Button(self, text="Расчет", width=20, height=2, command=self.calculation)
        self.tree = ttk.Treeview(t_mid, columns=('ID', 'name', 'costs', 'inv_del', 'summ'), height=15, show='headings')
        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('name', width=265, anchor=CENTER)
        self.tree.column('costs', width=150, anchor=CENTER)
        self.tree.column('inv_del', width=150, anchor=CENTER)
        self.tree.column('summ', width=150, anchor=CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Наименование')
        self.tree.heading('costs', text='Кол-во')
        self.tree.heading('inv_del', text='Поступление/Возврат')
        self.tree.heading('summ', text='Сумма')
        
        scroll = ttk.Scrollbar(t_mid, orient="vertical", command=self.tree.yview)
    
        #размещение виджетов
        f_mid.pack(pady=20)
        l_shop.pack(side=LEFT)
        self.combo_shop.pack(side=LEFT, padx=5)
        t_mid.pack()
        self.tree.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scroll.set)
        b_calculation.pack(pady=3)
        self.l_result.pack()
        l_calculation.pack()
        f_top.pack(side=LEFT, padx=20)
        f_bot.pack(side=LEFT)
        l_name.pack(pady=2)
        l_count.pack(pady=2)
        l_inv_del.pack(pady=2)
        self.combo_name.pack(pady=2)
        self.e_count.pack(pady=2)
        self.combo_inv_del.pack(pady=2)
        b_invite.pack()
        b_delite.pack()
        b_change.pack()
        
        self.combo_shop.bind("<<ComboboxSelected>>", lambda _: self.print_table()) #создание действия виджета Combobox
        
        #фиксация на фрейме дочернего окна
        self.grab_set()
        self.focus_set()

        #извлечение данных из таблицы магазинов в комбобокс
        self.db.cursorObj.execute('''SELECT name FROM shop''')
        self.combo_shop['values'] = self.db.cursorObj.fetchall()
        self.combo_shop.current(0)
        
        #извлечение данных из таблицы товаров в комбобокс
        self.db.cursorObj.execute('''SELECT name FROM tov''')
        self.combo_name['values'] = self.db.cursorObj.fetchall()
        
        self.print_table() #функция начального отображения таблицы поступлений
    
    #функция добавления элемента в таблицу
    def invite(self):
        '''Сделать так, чтобы id сдвигалось в зависимости от того, что удалили'''
        if is_number(self.e_count.get()):
            self.db.insert_table_calculation(self.combo_name.get(), self.e_count.get(), self.combo_inv_del.get(), self.combo_shop.get()) #заполнение таблицы SQL
            self.print_table()
            self.e_count.delete(0, END)
        else:
            messagebox.showerror('Ошибка', 'В поле "количество" ведено не число')
            
    #функция удаления элемента из таблици       
    def delite(self):
        for selection_item in self.tree.selection():
            self.db.cursorObj.execute('''DELETE FROM calculation WHERE ID =?''', (self.tree.set(selection_item, '#1'),)) #удаляем все выделенные элементы в виджете tree
        self.db.conn.commit()
        self.print_table()
    
    #функция начального отображения таблицы магазинов
    def print_table(self):
        self.db.cursorObj.execute('''SELECT ID, name, costs, inv_del, summ FROM calculation WHERE shop=?''', (self.combo_shop.get(),))
        [self.tree.delete(i) for i in self.tree.get_children()] #удаление всей таблицы из виджета
        [self.tree.insert('', 'end', values=row) for row in self.db.cursorObj.fetchall()] #заполнение обновленными данными
        
    def change(self):
        res = messagebox.askyesno('Предупреждение', 'Вы действительно хотите очистить таблицу?')
        if res:
            self.db.cursorObj.execute('''DELETE FROM calculation''')
            self.db.conn.commit()
            self.print_table()
            
    #функция подсчета денег    
    def calculation(self):
        self.db.cursorObj.execute('''SELECT ifnull((SELECT SUM(summ) FROM calculation where inv_del = "Поступление"), 0)
        - ifnull((SELECT SUM(summ) FROM calculation where inv_del = "Возврат"), 0)''')
        self.l_result['text'] = self.db.cursorObj.fetchone()      
 
       
#Объявление класса баз данных и таблиц 
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.cursorObj = self.conn.cursor() #подключение к БД для выполнения запросов
        self.conn.commit()
    
    #создание таблицы магазинов    
    def create_table_shop(self):
        self.cursorObj.execute(
            '''CREATE TABLE IF NOT EXISTS shop(id integer PRIMARY KEY, name text)''')
        self.conn.commit()
    
    #создание таблицы товаров     
    def create_table_tov(self):
        self.cursorObj.execute(
            '''CREATE TABLE IF NOT EXISTS tov(id integer PRIMARY KEY, name text, costs real)''')
        self.conn.commit()
    
    #создание таблицы поступлений  
    def create_table_calculation(self):
        self.cursorObj.execute(
            '''CREATE TABLE IF NOT EXISTS calculation(id integer PRIMARY KEY, name text, costs real, inv_del text, summ real, shop text)''')
        self.conn.commit()
        
    #заполнение таблицы магазинов
    def insert_table_shop(self, name):
        self.cursorObj.execute('''INSERT INTO shop(name) VALUES (?)''',
                       (name,))
        self.conn.commit()
    
    #заполнение таблицы товаров
    def insert_table_tov(self, name, costs):
        self.cursorObj.execute('''INSERT INTO tov(name, costs) VALUES (?, ?)''',
                       (name, costs))
        self.conn.commit()
    
    #заполнение таблицы поступлений    
    def insert_table_calculation(self, name, costs, inv_del, shop):
        self.cursorObj.execute('''INSERT INTO calculation(name, costs, inv_del, summ, shop) 
                        VALUES (?, ?, ?, (SELECT costs * ? FROM tov WHERE name = ?), ?)''',
                        (name, costs, inv_del, costs, name, shop))
        self.conn.commit()    


if __name__ == "__main__":       
    db = DB() #создание объекта БД
    
    #создание главного окна программы
    root = Tk()
    first_block = Main(root)
    root.title("Главный экран")
    root.geometry("350x250+400+200")
    root.mainloop()
