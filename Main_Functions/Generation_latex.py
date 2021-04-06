"""
Ворд:
Что не получилось:
1) Что если в таблице удалена ячейка в строке? В этом случае, увы, ничего сделать невозможно. С точки зрения библиотеки,
    отсутсвие ячейки означает, что береться ячейка со следуйщей строки. Что в свою очередь делает неправильную
    структуру таблицы, а данные отображаются не в своих ячейках. Вывод:
        для корректного переноса таблицы, нужно чтобы структура таблицы была прямоугольна. Даже, если нужно, чтобы
        ячейки не было, то, просто, нужно в нее вписать такое "Абракадавра 1" и в латехе, не будет отображаться
        левая граница
2) Формулы. Много читал по их переносу. Библиотека не поддерживает ее. Можно через XML, но это сложно.
 Кроме того, преоброзовать формулу из ворда в латех -- задача требующих познаний в математике (с точки зрения как строя-
 тся формулы и т.д. Чую тут много тонкостей ) и большой обьем труда. Боюсь, что полноценная конвертация ворда в латех
 -- это уже полноценная тема для диплома.  А у меня кроме этого, есть еще функции. Поэтому, оставлю на последок, если
 будет время.
 Костыль-решение: в ворде можно преоброзвать формулу в латех-форму. Возможно, пользователь должен конвертировать так
 форумулу, после чего, скопировать ее в ячейку и до нее написать "Абракадавра 2". Я же одену ее в форму для формул
 в латехе и выведу в латех. Но это уже в самом конце разработки.

"""
"""
Примечание:
-Сделать проверку на docx файл
1) Работа с ворд документами.
    1.1) Найти нужную таблицу +/- Корректный способ?
    1.2) Анализ каждой ячейки. Для удобства, описывается только первая табличка
        1.2.1) Каждого слова!
            1.2.1.1) Стиль (Жирный, обычный, курсив)
            1.2.1.2) Подчеркивание
            1.2.1.3) Капсом ли написано
            1.2.1.4) Цвет шрифта
            1.2.1.5) Двойное зачеркивание
            1.2.1.6) Цвет выделения
            1.2.1.7) Расположение текста:
Сверху-слева, сверху-центр, сверху-справа, Справа-справа, внизу-справа, внизу-центр, внизу-слева,слева-слева,центе-центр
            1.2.1.8) Направление текста
            1.2.1.9) Размер шрифта.
            1.2.1.10) Нижний индекс и вверхний индекс.
2) Работа с эксель документами.
3) Получить таблицу. 
4) Понять какой это формат.
5) Если это CSV, то попытаться его отобразить через встроеннный в латехе плюшку.
6) Если же нет, то думать как его превратить в CSV или же в другой поддерживаемый формат латех. Делать 5 пункт.
7) Разработка команды, через которую можно обратиться к ворду/екселю. Функция будет прописываться в латех-файле. +
8) Научиться искать эту команду в латех-файле.+
9) Получать таблицу по этой команде.+
10) Генерация начинаеться. Выход на финишнюю прямую.
11) Создать копию документа.
12) В копии заменить эту команду на команду, что умеет преобразывать CSV в таблицу латеха.
13) И так делать пока не закончятся команды.
14) Конвертация латеха в пдф.
15) Решаем баги, что могут быть. Надеюсь, их не будет.
"""
import os
import docx
import re
import sys


class Generation_latex_excel():
    pass

class Generation_latex_word():
    def search_docx_file(self, name_address=None, name_table=None):  # Search file-docx
        # Проверка на то что пользователь не указал данные.
        if name_address == None: return "Не вказана назва файлу!"
        if name_table == None: return "Не вказана назва таблиці!"
        # Чтобы в классе проще работать
        self.name_address = name_address
        self.name_table = name_table
        # Проверяем, что файл вообще существует
        if os.path.isfile(self.name_address):
            self.doc = docx.Document(self.name_address)
            self.properties = self.doc.core_properties  # Сами еще не решили зачем это надо
            return self.search_docx_tables()  # Запускаем поиск таблицы
        else:  # На случай, если файл не нашелся.
            return "Файл не знайдено"

    def search_docx_tables(self):
        # Позор родины
        i = 0  # Определеяет номер необходимой таблицы.
        find_table = False  # Маркер нахождения таблицы
        for tables in self.doc.tables:  # Находим таблицу
            if find_table == True:  # Нашли таблицу!
                break
            if (tables.rows[0].cells[0].text == self.name_table):  # Ищем
                return self.Assembly_shop(i)
            else:
                i += 1
        if find_table == False:  # Если таблица не нашлась
            return "Таблиця не знайдена"

class Generation_latex(Generation_latex_word,Generation_latex_excel):

    def __init__(self):
        self.doc = ""
        self.name_address = ""
        self.name_table = ""
        self.list_start_file = list()
        self.list_new_table = list()

    def merge_cells(self, c):
       pass
       #self.test_list_1 = list()

        #self.test_list_2 = list()

    def every_row(self):
        c = self.name_table.cell(0, 1)
        print(str(c._tc.top)+ str(c._tc.bottom)+ str(c._tc.left)+ str(c._tc.right))
        for i in range(len(self.name_table.rows)):
            if i == 0:
                pass
            else:
                string = self.name_table.cell(i,0).text
                for j in range(len(self.name_table.columns)):
                        self.merge_cells(self.name_table.cell(i,j).text)
                        f = -1
                        k = j
                        while k < len(self.name_table.columns):
                            r_1 = str(self.name_table.cell(i, j) ._tc.top)+ str(self.name_table.cell(i, j) ._tc.bottom)+ str(self.name_table.cell(i, j) ._tc.left)+ str(self.name_table.cell(i, j) ._tc.right)
                            r_2 = str(self.name_table.cell(i, k) ._tc.top)+ str(self.name_table.cell(i, k) ._tc.bottom)+ str(self.name_table.cell(i, k) ._tc.left)+ str(self.name_table.cell(i, k) ._tc.right)
                            print(f)
                            if r_1 == r_2:
                                f=f+1
                                k+=1
                            else:
                                break
                        if(f==0):
                            string = string+"&" + self.name_table.cell(i,j).text
                        else:
                            string = string+"&" + "\\multirow{" +str(f)+"}{c}{"+ self.name_table.cell(i,j).text + "}"

                self.list_new_table.append(string + "\\\\")
                self.list_new_table.append(" \\hline")
        #print("1)")
        #print(self.name_table.row_cells(5))
        #print("2)")
        #print(self.name_table.row_cells(1))
        #print("3)")
        #print(self.name_table.row_cells(2))


    def Assembly_shop(self, number_table): # Сборочный цех. Тут собирается уже latex - таблица
        self.name_table = self.doc.tables[number_table]
        self.list_new_table.append("\\begin{longtable}"  + "{|" + "c|"*len(self.name_table.columns) +"}")
        self.list_new_table.append("    \\multicolumn{"+ str(len(self.name_table.columns)) +"}{r}{Продовження на наступній сторінці\\ldots}\\\\")
        self.list_new_table.append("    \\endfoot")
        self.list_new_table.append("    \\endlastfoot")
        self.list_new_table.append("    \\hline")
        self.every_row()
        self.list_new_table.append("\\end{longtable}")
        return self.list_new_table
        #return name_table.rows[0].cells[0].text
        #print(self.doc.tables[0].rows[0].cells[0].paragraphs[0].runs[0].bold)

    def find_parameter_to_command_to_latex_file(self, structure_command): # разбивает команду на параметры
        # Баг: Что если параметров будет не правильное количество?
        # №1 параметр. Адрес ворда
        # Баг: Если в название папки или файла будет запятая, то это сломает абсолютно все. Исправить бы
        name_address = re.search(r'(?<=\{)([\s\S]+?)(?=\,)', structure_command)
        #print(name_address.group(0))
        # №2 параметр. Имя таблицы
        name_table = re.search(r'(?<=\,)([\s\S]+?)(?=\})', structure_command)
        #print(name_table.group(0))
        #Определяет формат текущего документа для дальнейшего распределения документа по классу: Ексель или Ворд.
        name_address_data=re.search(r'[^.]+$', name_address.group(0))
        if name_address_data.group(0) == "docx":
            return self.search_docx_file(name_address.group(0),name_table.group(0))
        elif name_address_data.group(0) == "xlsx":
            pass # реализация обработки xls-документов
        else:
            return "Формат документа може бути тільки docx чи xls"

    def find_command_to_latex_file(self,name_address_tex_file): # Поиск команды.
        if os.path.isfile(name_address_tex_file):
            with open(name_address_tex_file, 'r+',encoding='utf-8') as file:
                for line in file:
                    if (re.search(r'%Generationlatexpython{([\s\S]+?),([\s\S]+?)}', line)) is None:
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.append(line)
                        #print(line)
                    else:
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.extend (self.find_parameter_to_command_to_latex_file(line))
                        #print(self.list_start_file[-1])
                        #print(line)
                        self.list_new_table.clear()
            MyFile = open('test_table.tex', 'w')
            self.list_start_file = map(lambda x: x + '\n', self.list_start_file)
            MyFile.writelines(self.list_start_file)
            MyFile.close()
                        #line = "%Generationlatexpython{D:\Учеба\Диплом\Editor_for_Latex\Main_Functions\demo.docx,Таблица 3}"
            #print('\n'.join(self.list_start_file))
        else:
            print("Файлу нема!")



if __name__ == '__main__':
    app = Generation_latex()
    app.find_command_to_latex_file('test.tex')

    #app.search_docx_file('D:\Учеба\Диплом\Editor_for_Latex\Main_Functions\demo.docx', "Таблица 1")
