"""
Ворд:
1) Что если в таблице удалена ячейка в строке? В этом случае, нужно вывести ошибку про нарушение структуры таблицы.
2) Формулы. Библиотека питона их не видит. Для него формула -- пустота. Но если в ячейке есть обычный текст, то он
его отлично видит и отобразит его так же как в ячейке, но без формулы.
3) Рисунки. Тоже самое, что и с формулами.
3.1)Таблица внутри ячейки. Тоже что и формулы.
4) Слияние/объеденние ячеек работает без багов
5) Полужирный , курсив, нижнее подчеркивание, Нижний/вверхний индекс -- есть и работает стабильно.
6) Границы. Поддерживается только одна толщина и отображаются везде, кроме тех случаев, когда речь про
 объеденные ячейки.
7) Ширина ячейки. Тут есть проблемы. Латех не правильно отображает сантиметры , а ворд не очень корректно выдает
данные по ширине. К примеру, если в ячейке (в ворде) есть формула или же картинка, то ширина картинки/формулы
не учитывается. Видимо, ворд подставляет размер картинки во время внутренной работы, а в XML хранит размер без
учета формул/картинки.
Баг 7 пункта: Как оказалось, если ширина ячейки не указана (ворде можно такое сделать), то вызывается ошибка. Позже
исправить.
8) Выравнение. Если речь про то, что текст может быть слева/справа/по-центру, то проблем нету. Однако, если речь про
то что текст можеть быть сверху/внизу/центру, то тут уже проблемы. Как оказалось, метод, которым я это делаю,
имеет проблемы с том, что если в одной строке в одной ячейке  указано, что текст сверху, а в другой ячейке текст внизу,
то так не может быть. Каждая ячейка наследует поведение прошлой ячейки. Поэтому, если впервой ячейке текст сверху, то
все ячейки одной строки будут иметь текст с сверху. Кроме того, библиотека для работы с вордом не корректно отображает
выравнивание текст. Поэтому было решено, что весь текст в таблицах будет по центру. Но если он находиться справа или
слева, то это будет учтено. Если же сверху/внизу, то это не будет учтено и текст будет по середение высоты ячейки.
9) Распределение текста в ячейке. multirow пока-что сопротивляется, но думаю все будет с ним.
10) Фон/цвет ячеек. Как я понял это не нужно. А раз не нужно -- не делаеться.
11) Шрифт текста. Я когда-то изучал латех, то выявил, что латех не очень имеет дружбу с шрифтами ворда. В теории, я могу
вывести шрифт ворда, но сформировать его в латехе.... Сложно и как по мне не имеет смысла. Поэтому, таблицы наследуют
тот же шрифт, что используется в тех-документе.
12) Размер текста. В теории возможно, но в латехе странные функции по изменению размера.
13) В ворде можно поставить двойное зачеркивание текста. В латехе не нашел команды. Нужно ли?
14) Размер шрифта. Все было бы хорошо, если бы не одно НО. Если размер шрифта таблички совпадает с размером шрифта по
документу, то я не могу узнать его узнать -- функция выведет None, а не размер кегля. Узнать размер общий шрифт докумен-
та не очень-то и можно. Решил так. Если размер кегля совпадает с размером документа в ворде, то значит кегль таблицы
в латехе наследуется от общей настройки в  команде \documentclass[a4paper,12pt]{article}. В противном случае, размер
кегля таблицы будет корректироваться командой \small. Тоесть, если кегль документа 14pt, то табличка будет 12pt.
После синтаксиса таблицы, будет выводиться \normalsize.
Как я понял, кегль внутри таблички должен быть одинаковым. К тому же, если изменять размер каждого слова, то текст
начинает не очень адекватно выводиться и может вывестись весь в одну строку.
15) Табуляция в таблицах. Решено было пропустить.
16) Междустрочный интервал. Наследуется от латеха.
17) Специальные символы латеха обрабатываются

Что еще нужно сделать:
1) Специальная команда в начале tex-файл, что выводит необходимые команды в начале предложения. После begin{document}
должна оставаться. Также без этого не должны работать генератор. +
2) Подключение ворд-документа.Подключать можно где угодно, но команда должна занимать одну строку. +
3) Вывод ячеек в любой части латеха. Просто как текст. +
4) Разработка несколько режимов генератора:
-- Вывод таблицы как можно больше похоже на оригинал. Ха-ха. Original +
-- Вывод таблицы, где Текст без форматирования. Only_Text +
-- Вывод таблицы, где вместо текста команды для каждой ячейки. Only_Cells +
5) Внедрение генератора в основную таблицу. +
"""
"""
Примечание:
1) Работа с ворд документами.
    1.1) Найти нужную таблицу +/- Корректный способ?
    1.2) Анализ каждой ячейки. Для удобства, описывается только первая табличка
        1.2.1) Каждого слова!+
            1.2.1.1) Стиль (Жирный, обычный, курсив) +
            1.2.1.2) Подчеркивание +
            1.2.1.4) Цвет шрифта
            1.2.1.5) Двойное зачеркивание
            1.2.1.6) Цвет выделения
            1.2.1.7) Расположение текста:
Сверху-слева, сверху-центр, сверху-справа, Справа-справа, внизу-справа, внизу-центр, внизу-слева,слева-слева,центе-центр
            1.2.1.8) Направление текста
            1.2.1.9) Размер шрифта.
            1.2.1.10) Нижний индекс и вверхний индекс.
3) Получить таблицу. +
7) Разработка команды, через которую можно обратиться к ворду/екселю. Функция будет прописываться в латех-файле. +
8) Научиться искать эту команду в латех-файле.+
9) Получать таблицу по этой команде.+
10) Генерация начинаеться. Выход на финишнюю прямую.
11) Создать копию документа.
12) В копии заменить эту команду на команду, что умеет преобразывать CSV в таблицу латеха.
13) И так делать пока не закончятся команды.
14) Конвертация латеха в пдф.
15) Решаем баги, что могут быть. Надеюсь, их не будет. +/-
"""

import os
import docx
import re
import data.XML.work_with_XML as XML

class Generation_latex_word:
    def search_docx_file(self, name_address=None, name_table=None, command_status = "Original"):  # Search file-docx
        # Проверка на то что пользователь не указал данные.
        if name_address == None:
            return ("Не вказана назва файлу!")
        if name_table == None:
            return "Не вказана назва таблиці!"
        # Чтобы в классе проще работать
        self.name_address = name_address
        self.name_table = name_table
        # Проверяем, что файл вообще существует
        if os.path.isfile(self.name_address):
            self.doc = docx.Document(self.name_address)
            self.properties = self.doc.core_properties  # Сами еще не решили зачем это надо
            return self.search_docx_tables(command_status)  # Запускаем поиск таблицы
        else:  # На случай, если файл не нашелся.
            return "Файл не знайдено"

    def search_docx_tables(self,command_status):
        i = 0  # Определеяет номер необходимой таблицы.
        find_table = False  # Маркер нахождения таблицы
        for tables in self.doc.tables:  # Находим таблицу
            if find_table == True:  # Нашли таблицу!
                    break
            if tables.rows[0].cells[0].text == self.name_table:  # Ищем
                return self.Assembly_shop(i,command_status)
            else:
                i += 1
        if find_table == False:  # Если таблица не нашлась
            return "Таблиця не знайдена"

    def align_multirow(self, row, column):
        try:
            a = (self.name_table.cell(row, column).width / 914400.0) * 2.54
            a = round(a*0.9,1)
        except Exception:
            a = 1.0
        string = "\\parbox{" + str(a) + "cm" + "}{"
        a_aligment = str(self.name_table.cell(row, column).paragraphs[0].alignment)
        if a_aligment == "RIGHT (2)":
            string += " \\raggedleft "
            return string
        elif a_aligment == "CENTER (1)":
            string += " \\centering "
            return string
        elif a_aligment == "LEFT (4)":
            string += " \\raggedright "
            return string
        elif a_aligment == "JUSTIFY (3)":
            return string
        else:
            return string
    def every_row(self,command_status):
        map_table = [[0] * len(self.name_table.columns) for i in range(len(self.name_table.rows))]
        for row in range(len(self.name_table.rows)):
            if row == 0: pass
            else:
                string = ''
                column = 0
                map_table_hline = [""] * len(self.name_table.columns)
                while column < len(self.name_table.columns):
                    f = 1
                    c = 0
                    if column == 0:
                        border_left = "|"
                    else:
                        border_left = ""
                    border_right = ""
                    if (map_table[row][column] == 0):
                        k = 0

                        #print(str(row + 1) + " " + str(column+1))
                        self.merge_cells_word(row,column)
                        if row < (len(self.name_table.rows) - 1) and column < (len(self.name_table.columns) - 1)\
                                and self.merge_cells_word(row,column) == self.merge_cells_word(row + 1, column)\
                                and self.merge_cells_word(row,column) == self.merge_cells_word(row, column+1):
                            #----------------------
                            while (k + column) < (len(self.name_table.columns) - 1):
                                if self.merge_cells_word(row, k + column) == self.merge_cells_word(row,k + column + 1):
                                    f += 1
                                else:
                                    break
                                k += 1
                            border_right = "|"
                            map_table_hline[column+f-1] = "|"
                            string += "\\multicolumn{" + str(f) +"}{" + border_left + self.paragraphs_alignment_cell(row,column) + border_right +"}{"
                            c += 1
                            row_merge = 1
                            while (row_merge + row) < len(self.name_table.rows):
                                if self.merge_cells_word(row, column) == self.merge_cells_word(row_merge + row, column):
                                    k = 0
                                    while (k + column) < (column+f-1):
                                        map_table[row_merge + row][k + column] = 2
                                        k += 1
                                    map_table[row_merge + row][k + column] = 2 # Last column to merge_cell
                                    c += 1
                                else:
                                    break
                                row_merge += 1
                            if (column+f == len(self.name_table.columns)):
                                string += "\multirow{" + str(c) + "}{*}{" + self.align_multirow(row, column)+ self.return_cells(row, column,command_status) + "}}}"
                            else:
                                string += "\multirow{" + str(c) + "}{*}{" + self.align_multirow(row, column) + self.return_cells(row, column,command_status) + "}}}" + "&"
                            #-----------------------
                        elif row < (len(self.name_table.rows) - 1) \
                                and self.merge_cells_word(row,column) == \
                                self.merge_cells_word(row + 1, column):
                            map_table[row][column] = 1
                            map_table[row + 1][column] = 1
                            c += 1
                            row_merge = 1
                            border_right = "|"
                            map_table_hline[column + f-1] = "|"
                            string += "\\multicolumn{" + str(1) + "}{" + border_left + self.paragraphs_alignment_cell(row,column) + border_right + "}{"
                            while row_merge + row < len(self.name_table.rows):
                                if self.merge_cells_word(row, column) == self.merge_cells_word(row_merge + row, column):
                                    map_table[row_merge + row][column] = 1
                                    c += 1
                                else:
                                    break
                                row_merge += 1
                                map_table_hline[column+f-1] = "|"
                            if ((column + f) == len(self.name_table.columns)):
                                string += "\\multirow{" + str(c) + "}{*}{" + self.align_multirow(row, column)+ \
                                          self.return_cells(row,column,command_status) + "}}}"
                            elif (column == 0):
                                string += "\\multirow{" + str(c) + "}{*}{" + self.align_multirow(row, column)+ \
                                          self.return_cells(row,column,command_status) + "}}}" + "&"
                            else:
                                string += "\\multirow{" + str(c) + "}{*}{" + self.align_multirow(row, column)+ self.return_cells(row,column,command_status) + "}}}" + "&"
                        else:
                            while (k + column) < (len(self.name_table.columns) - 1):
                                if self.merge_cells_word(row, k + column) == self.merge_cells_word(row,
                                                                                                   k + column + 1):
                                    f += 1
                                else:
                                    break
                                k += 1
                            #|-----------|
                            #|           |
                            #|-----------|
                            if column + f == len(self.name_table.columns): # Last cell in row
                                ampersand = ""
                            else:
                                ampersand = "&"
                            border_right = "|"
                            map_table_hline[column + f-1] = "|"
                            string += "\\multicolumn{" + str(f) + "}{"+ border_left +self.paragraphs_alignment_cell(row,column) + border_right+"}{" + \
                                          self.return_cells(row,column,command_status) + "}" + ampersand
                    else:
                        # map-table == 1
                        if column + f == len(self.name_table.columns):  # Last cell in row
                            ampersand = ""
                        else:
                            ampersand = "&"
                        if column + f == len(self.name_table.columns):  # Last cell in row
                            border_right = "|"
                            map_table_hline[column + f-1] = "|"
                        elif column + f != len(self.name_table.columns) and self.merge_cells_word(row,column) != self.merge_cells_word(row,column+1):
                            border_right = "|"
                            map_table_hline[column + f-1] = "|"
                        if (map_table == 1):
                            string += "\\multicolumn{" + str(f) + "}{" + border_left + self.paragraphs_alignment_cell(row,column) + border_right + "}{" + "}" + ampersand
                        else:
                            string += "\\multicolumn{" + str(f) + "}{" + border_left + "c" + border_right + "}{" + "}" + ampersand
                    column = column + f
                self.list_new_table.append(string + "\\\\")
                hhline = "\\hhline{"
                for column_hline in range(len(self.name_table.columns)):
                    if row == (len(self.name_table.rows) - 1):
                        hhline += "-"
                    elif map_table[row+1][column_hline] == 0:
                        hhline += "-"
                    elif column_hline == 0:
                        hhline += "|~" + map_table_hline[column_hline]
                    else:
                        hhline += "~" + map_table_hline[column_hline]
                hhline += "}"
                self.list_new_table.append(hhline)


class Generation_latex(Generation_latex_word):

    def __init__(self):
        self.doc = ""
        self.name_address = ""
        self.name_table = ""
        self.list_start_file = list()
        self.list_new_table = list()
        self.list_docx_file = list()

    def merge_cells_word(self, row, column):  #
        try:
            return str(self.name_table.cell(row, column)._tc.top) + str(self.name_table.cell(row, column)._tc.bottom) + \
                   str(self.name_table.cell(row, column)._tc.left) + str(self.name_table.cell(row, column)._tc.right)
        except Exception:

            return str(self.name_table.cell(row, column)._tc.top) + "0707" + \
               str(self.name_table.cell(row, column)._tc.left) + str(self.name_table.cell(row, column)._tc.right)

    def paragraphs_alignment_cell(self,row,column):
        try:
            a = (self.name_table.cell(row, column).width / 914400.0) * 2.54
            a = round(a*0.9,1)
        except Exception:
            a = 1.0
        a_aligment = str(self.name_table.cell(row, column).paragraphs[0].alignment)
        if a_aligment == "RIGHT (2)":
            return (">{\\raggedleft\\arraybackslash}m{" + str(a) + "cm" + "}")
        elif a_aligment == "CENTER (1)":
            return (">{\\centering\\arraybackslash}m{" + str(a) + "cm" + "}")
        elif a_aligment == "LEFT (4)":
            return(">{\\raggedright\\arraybackslash}m{" + str(a) + "cm" + "}")
        elif a_aligment == "JUSTIFY (3)":
            return ("m{" + str(a) + "cm" + "}")
        else:
            return (">{\\raggedright\\arraybackslash}m{" + str(a) + "cm" + "}")

    def run_bold(self,string_r,status):
        if status == "True":
            return "\\textbf{" + string_r +"}"
        else:
            return string_r

    def run_italic(self,string_r,status):
        if status == "True":
            return "\\textit{" + string_r +"}"
        else:
            return string_r

    def run_underline(self,string_r,status):
        if status == "True":
            return "\\underline{" + string_r +"}"
        else:
            return string_r

    def run_font_strike(self,string_r,status):
        if status == "True":
            return "\\sout{" + string_r +"}"
        else:
            return string_r

    def run_font_subscript(self,string_r,status):
        if status == "True":
            return "True"
        else:
            return "False"

    def run_font_superscript(self,string_r,status):
        if status == "True":
            return "True"
        else:
            return "False"

    def table_font_size(self):
        try:
            status_size = str(self.name_table.cell(1, 0).paragraphs[0].runs[0].font.size)
        except Exception:
            status_size = "None"
        if status_size == "None":
            return "False"
        else:
            return "True"

    def special_symbols(self, string):
        mas_a = ['\\','#','$','%','^', '&', '_', '{","}','~']
        mas_b = ['\\textbackslash ','\\# ','\\$ ','\\% ','\\textasciicircum ', '\\& ', '\\_ ', '\\{ ","\\} ','\\textasciitilde ']
        for i in range(len(mas_a)):
            string = string.replace(mas_a[i],mas_b[i])
        return string

    def return_cells(self,row,column,command_status):
        # Ширина каждой ячейки
        string_p = ""
        string_r = ""
        for paragraph in self.name_table.cell(row, column).paragraphs:
            string_r = ""
            for run in paragraph.runs:
                string_rr = run.text
                string_rr = self.special_symbols(string_rr)
                math_first = ""
                math_formula = ""
                math_last = ""
                if self.run_font_subscript(string_rr, str(run.font.subscript)) == "True":
                    math_first = "$"
                    math_formula = "_{"
                    math_last = "}$"
                if self.run_font_subscript(string_rr, str(run.font.superscript)) == "True":
                    math_first = "$"
                    math_formula = "^{"
                    math_last = "}$"
                if string_rr != (" " or ". ") and command_status == "Original":
                    string_rr = self.run_bold(string_rr, str(run.bold))
                    string_rr = self.run_italic(string_rr, str(run.italic))
                if command_status == "Original":
                    string_rr = self.run_underline(string_rr, str(run.underline))
                    string_rr = self.run_font_strike(string_rr, str(run.font.strike))
                string_r += math_first + math_formula + string_rr + math_last
            string_p += string_r
            if command_status == "Original":
                string_p += "\\pol "
        if command_status == "Original":
            string_p = string_p[0:-5]
        string_p += ""
        if command_status == "Original" or command_status == "Only_Text":
            return string_p
        elif command_status == "Only_Cells":
            a = " Cell(" + self.name_table.cell(0, 0).text + "," + str(row) + "," + str(column) + ") "
            return a
        else:
            return  self.name_table.cell(row, column).text


    def commands_to_generation(self, status):
        if status == "True":
            self.list_start_file.append("\\usepackage{multirow} % Об'єднання через рядки")
            self.list_start_file.append("\\usepackage{hhline} % Міжрядкова лінія")
            self.list_start_file.append("\\usepackage{array} % Вирівнювання")
            self.list_start_file.append("\\usepackage[normalem]{ulem} % Закреслення тексту")
            self.list_start_file.append("\\newcommand{\pol} % Для переносів")
            self.list_start_file.append("{")
            self.list_start_file.append(" ")
            self.list_start_file.append(" ")
            self.list_start_file.append("}")
        else:
            self.list_start_file.append("%CommandsGenerationlatexpython")

    def first_part_table(self):  #
        if self.table_font_size() == "True": self.list_new_table.append("\\small")
        self.list_new_table.append("\\begin{tabular}" + "{" + "c" * len(self.name_table.columns) + "}")
        self.list_new_table.append("    \\hline")

    def Assembly_shop(self, number_table, command_status):  # Сборочный цех. Тут собирается уже latex - таблица
        self.name_table = self.doc.tables[number_table]
        try:
            for row in range(len(self.name_table.rows)):
                for column in range(len(self.name_table.columns)):
                    self.merge_cells_word(row, column)
        except (IndexError, AttributeError):
            return "Таблиця має не правильну структуру"
        self.first_part_table()
        self.every_row(command_status)
        self.list_new_table.append("\\end{tabular}")
        if self.table_font_size() == "True":
            self.list_new_table.append("\\normalsize")
        return self.list_new_table
    def find_parameter_to_command_to_latex_file(self, structure_command):  # разбивает команду Generationlatexpython на параметры
        status_parameters = "False"
        names_parameters = ["Original", "Insert_Original", "Only_Text", "Only_Cells"]
        # №1 параметр. Адрес ворда
        name_address = re.search(r'(?<=\{)([\s\S]+?)(?=\,)', structure_command)
        # №2 параметр. Имя таблицы
        name_table = re.search(r'(?<=\,)([\s\S]+?)(?=\})', structure_command)
        # Определяет формат текущего документа для дальнейшего распределения документа по классу: Ексель или Ворд.
        name_address_data = re.search(r'[^.]+$', name_address.group(0))
        for name in names_parameters:
            name = r'(?<=\{)(' + name + r')(?=\})'
            try:
                command_status = re.search(name, structure_command)
                command_status = command_status.group(0)
                break
            except AttributeError:
                command_status = "Original"
        self.list_new_table.append('%Generationlatexpython_Disable{'+name_address.group(0) + "," + name_table.group(0) + "}{" + command_status + "}")
        if name_address_data.group(0) == "docx":
            return self.search_docx_file(name_address.group(0), name_table.group(0),command_status)
        else:
            return "Формат документа може бути тільки docx"

    def find_parameter_to_command_to_IncludeDocx(self, structure_command):

        name_address = re.search(r'(?<=\{)([\s\S]+?)(?=\})', structure_command)
        if os.path.isfile(name_address.group(0)):
            name_address_data = re.search(r'[^.]+$', name_address.group(0))
            if name_address_data.group(0) == "docx":
                self.list_docx_file.append(name_address.group(0))
                return structure_command
            else:
                return structure_command + " Формат документа може бути тільки docx"  # Придумать чет по-лучше.
        elif name_address.group(0) == "Назва_файлу":
            return structure_command
        else:
            return structure_command + " Такого файлу не існує"

    def return_many_cells(self, structure_command):
        my = "True"
        table_string = ""
        try:
            string = re.search(r'Cell\s*\([^(),]+,\d+,\d+\)', structure_command).group(0)
            print(string)
        except AttributeError:
            return structure_command + "Attribute_error"
        while my == "True":
            #print(string)
            name_table = re.search(r'(?<=\()([\s\S]+?)(?=,)', string).group(0)
            #print(name_table)
            row = re.search(r'(?<=,)([\s\S]+?)(?=,)', string).group(0)
            #print(row)
            column = re.search(r'(?<=,)([\s\S]+?)(?=\))', string).group(0)
            column = re.search(r'(?<=,)([\s\S]+?)', column).group(0)
            #print(row + "|" + column)
            #print(column)
            a = "Cell_disable(" + name_table + "," + row + "," + column + ") - "
            table_string = a + " Впишіть назву документа за допомогою команди %IncludeDocx{Назва_файлу}"
            for docx_file in self.list_docx_file:
                #Находим файл
                if os.path.isfile(docx_file):
                    doc = docx.Document(docx_file)
                else:
                    table_string = a + " Впишіть назву документа за допомогою команди %IncludeDocx{Назва_файлу}"
                #Находим табличку
                i = 0  # Определеяет номер необходимой таблицы.
                find_table = False  # Маркер нахождения таблицы
                for tables in doc.tables:  # Находим таблицу
                    if find_table == True:  # Нашли таблицу!
                        break
                    if (tables.cell(0,0).text == name_table):  # Ищем
                        find_table = True
                        if row.isdigit() and column.isdigit() and isinstance(row,float) == False and isinstance(column,float)== False:
                            if int(row) < len(tables.rows) and int(row) >= 0 and int(column) < len(
                                    tables.columns) and int(column) >= 0:
                                table_string = self.special_symbols(tables.cell(int(row), int(column)).text)
                            else:
                                table_string = a + "Координати комірки вказані не вірно"
                        else:
                            table_string = a + "Координати комірки може бути тількі цілочисленними цифрами та вище нуля "
                    else:
                        i += 1
                if find_table == False:  # Если таблица не нашлась
                    table_string = a + "Таблиця ( " + name_table+ ")не знайдена по адресу (" + str (docx_file) + ") не знайдена"
                    table_string = self.special_symbols(table_string)

            structure_command = structure_command.replace(string,table_string)
            if str(re.search(r'Cell\s*\([^(),]+,\d+,\d+\)',structure_command)) == "None":
                my = "False"
            else:
                string = re.search(r'Cell\s*\([^(),]+,\d+,\d+\)', structure_command).group(0)
        return structure_command

    def find_command_to_latex_file(self, name_address_tex_file,status_run):  # Поиск команды.
        find_begin_document = "True"
        status_generation = "False"
        if os.path.isfile(name_address_tex_file):
            with open(name_address_tex_file, 'r+', encoding='utf-8') as file:
                for line in file:
                    if re.search(r'\\begin{document}',line):  # Маркер того, что начался основной документ.
                        find_begin_document = "False"
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.append(line)
                    elif re.search(r'Cell\s*\([^(),]+,\d+,\d+\)',line):
                        #print(line)
                        line = self.return_many_cells(line)
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.append(line)
                    elif re.search(r'%IncludeDocx\s*{([\s\S]+?)}', line): # Составлення списку docx-file
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)

                        self.list_start_file.append(self.find_parameter_to_command_to_IncludeDocx(line))
                    elif re.search(r'%CommandsGenerationlatexpython',line):  # Добавление команд для генератора.
                        self.commands_to_generation(find_begin_document)
                        find_begin_document = "False"
                        status_generation = "True"
                    elif (re.search(r'%Generationlatexpython\s*{[^(),]+,[^(),]+}{[^(),]+}', line))\
                            and status_generation == "True":  # Находим непосредственно команду для генерации таблиц.
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.extend(self.find_parameter_to_command_to_latex_file(line))
                        self.list_new_table.clear()
                    else:  # Если это строка без специальных команд
                        line = re.sub("^\s+|\n|\r|\s+$", '', line)
                        self.list_start_file.append(line)
            if (status_run == "enable"):
                file_name = XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex"
            elif status_run == "test":
                file_name = "test_table.tex"
            else:
                file_name = XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + '_enable' + ".tex"
            print(file_name)
            MyFile = open(file_name, 'w',  encoding='utf-8')
            self.list_start_file = map(lambda x: x + '\n', self.list_start_file)
            MyFile.writelines(self.list_start_file)
            MyFile.close()
        else:
            print("Файлу нема!")


if __name__ == '__main__':
    app = Generation_latex()
    app.find_command_to_latex_file('test.tex', "test")