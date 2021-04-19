# -----------------------------------------------------------
# Codes other files project
# -----------------------------------------------------------
from GUI.main_window.bar import * # Initiate bar-structure

# -----------------------------------------------------------
# PyQt 5.Initiate structure Main window and GUI
# -----------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWebEngineWidgets
from PyQt5.Qt import QSyntaxHighlighter, QRegularExpression
# -----------------------------------------------------------
# Other library
# -----------------------------------------------------------
import sys # Initiate project into operating system
from distutils.spawn import find_executable
import sqlite3


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.regexp_by_format = dict()

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.blue)
        self.regexp_by_format[r'\\[^()({|[|}|\]|\s)]+'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkCyan)
        self.regexp_by_format[r'\[[^()[^\\]}]+[^\\]\]'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkGreen)
        self.regexp_by_format[r'{[^()}]+}'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.gray)
        self.regexp_by_format[r'[^\\]%.*'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkMagenta)
        self.regexp_by_format[r'(%CommandsGenerationlatexpython|%Generationlatexpython_Disable|%IncludeDocx|Cell' \
                              r'|Cell_disable|%CommandsGenerationlatexpython)|%Generationlatexpython' \
                              r''] = char_format


    def highlightBlock(self, text):
        for regexp, char_format in self.regexp_by_format.items():
            expression = QRegularExpression(regexp)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


class Error_latex(QMainWindow, Bar):
    def __init__(self):
        super(Error_latex, self).__init__()
        self.error_install_latex()

    def error_install_latex(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Встановить Дистрибутив  Latex!")
        #self.msg.setInformativeText("Більше інформації!")
        self.msg.setWindowTitle("Помилка!")
        self.msg.setDetailedText("Посилання на дистрибутив Texlive: \n https://tug.org/texlive/")
        self.msg.exec_()


# Initiate Main window
class Main_windows(QMainWindow, Bar):

    def __init__(self):
        super().__init__()
        self.bar_category_fileMenu()  # Initiate Bar category fileMenu
        # -----------------------------------------------------------
        # Initiate structure Main window
        self.main_structure()
        self.main_text_field()
        self.main_window_view_pdf()
        self.main_window_splitter()
        self.main_window_parameter()
        # -----------------------------------------------------------

    def main_window_parameter(self):  # place to main setting "view window"
        self.setWindowTitle(XML.get_attr_XML('name-title'))
        self.showMaximized()

    def on_select(self):
        try:
            s = ""
            f = str(self.f_label.textCursor().selectedText())
            conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '\\'+'identifier.sqlite')
            cur = conn.cursor()
            cur.execute("select * from name_commands where name = '%s';"% f)
            conn.commit()
            ones = cur.fetchall()
            self.f_label.setToolTip("")
            for one in ones:
                if f == str(one[1]):
                    s += "<div>" + "<b>Назва команди:</b> <br>" + str(one[1]) + "</div>"
                    cur.execute("select des_text from table_description where id ='%s';" % one[0])
                    des = cur.fetchone()
                    if str(des[0]) != "None":
                        s += "<div>" + "<b>Опис:</b> <br>" + str(des[0]) + "</div>"
                    cur.execute("select param from table_parameter where id ='%s';" % one[0])
                    des = cur.fetchone()
                    if str(des[0]) != "None":
                        s += "<div>" + "<b>Параметри:</b> <br>" + str(des[0]) + "</div>"
                    cur.execute("select example_text from table_example where id ='%s';" % one[0])
                    des = cur.fetchone()
                    if str(des[0]) != "None":
                        s += "<div>" + "<b>Приклад:</b> <br>" + str(des[0]) + "</div>"
                    self.f_label.setToolTip(s)
                    break
            conn.close()
        except sqlite3.Error as E:
            self.f_label.setToolTip("В базі даних помилка!" + str(E))

    def main_text_field(self):  # place to tex-file;
        self.f_label = QTextEdit(self)
        self.f_label.setFontPointSize(10)
        self.f_label.selectionChanged.connect(self.on_select)
        # open tex-file when open program
        if XML.get_osnova_XML('tec-address') != "" and XML.get_osnova_XML('tec-name-file') != "":
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex",
                      encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())
    # Initiate text_place into main_structure()

        self.form_lay = QFormLayout()
        self.form_lay.addRow(self.f_label)
        self.form_frame.setLayout(self.form_lay)
        highlighter = MyHighlighter(self.f_label.document())

    def main_window_splitter(self):
        """
        split the window into two;
        Left is place to tex-file;
        Right is place to view.
        """
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.form_frame)
        self.splitter.addWidget(self.ver_frame)
        self.splitter.setSizes([200, 220])
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.splitter)
        self.setCentralWidget(self.splitter)

    def main_structure(self): # Initiate structure
        self.form_frame = QFrame()
        self.form_frame.setFrameShape(QFrame.StyledPanel)
        self.ver_frame = QFrame()
        self.ver_frame.setFrameShape(QFrame.StyledPanel)

    def main_window_view_pdf(self): # View pdf into main window
        self.main_window_view_pdf_val = QWebEngineView()
        self.main_window_view_pdf_val.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,
                                                              True)
        self.main_window_view_pdf_val.load(
            QUrl("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))
        self.ver_box = QVBoxLayout()
        self.ver_box.addWidget(self.main_window_view_pdf_val)
        self.ver_frame.setLayout(self.ver_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if find_executable('latex'):
        ex = Main_windows()
        a = MyHighlighter(ex.f_label.document())
    else:
        ex = Error_latex()
    sys.exit(app.exec_())