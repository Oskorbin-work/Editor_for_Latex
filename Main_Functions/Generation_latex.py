"""
1) Работа с ворд документами.
2) Работа с эксель документами.
3) Получить таблицу.
4) Понять какой это формат.
5) Если это CSV, то попытаться его отобразить через встроеннный в латехе плюшку.
6) Если же нет, то думать как его превратить в CSV или же в другой поддерживаемый формат латех. Делать 5 пункт.
7) Разработка команды, через которую можно обратиться к ворду/екселю. Функция будет прописываться в латех-файле.
8) Научиться искать эту команду в латех-файле.
9) Получать таблицу по этой команде.
10) Генерация начинаеться. Выход на финишнюю прямую.
11) Создать копию документа.
12) В копии заменить эту команду на команду, что умеет преобразывать CSV в таблицу латеха.
13) И так делать пока не закончятся команды.
14) Конвертация латеха в пдф.
15) Решаем баги, что могут быть. Надеюсь, их не будет.
"""
import os
import docx


class Generation_latex():

    def __init__(self):
        self.doc = ""

    def search_docx_file(self, name_address): # Search file-docx
        if os.path.isfile(name_address):
            self.doc = docx.Document(name_address)
            self.properties = self.doc.core_properties
            self.search_docx_tables()
        else:
            print("O, no!")

    def search_docx_tables(self):
        pass

if __name__ == '__main__':
    app = Generation_latex()
    app.search_docx_file('D:\Учеба\Диплом\Editor_for_Latex\Main_Functions\demo.docx')
