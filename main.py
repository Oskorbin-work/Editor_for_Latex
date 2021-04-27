# -----------------------------------------------------------
# Codes other files project
# -----------------------------------------------------------
from GUI.main_window.bar import * # Initiate bar-structure
from Main_Functions.Mylighterliter import * # Initiate Highlight text
from Other_Functions.Error_install_latex import * #If latex-dist not installed
# -----------------------------------------------------------
# PyQt 5.Initiate structure Main window and GUI
# -----------------------------------------------------------
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
#from PyQt5.QtGui import * $$$$$
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWebEngineWidgets
# -----------------------------------------------------------
# Other library
# -----------------------------------------------------------
import sys # Initiate project into operating system
from distutils.spawn import find_executable # find latex-dist
import sqlite3 # Database to Tooltip


# Initiate Main window
class Main_windows(QMainWindow, Bar):

    def __init__(self):
        super().__init__()
        self.statusbar = self.statusBar()
        self.bar_category_fileMenu()  # Initiate Bar category fileMenu
        self.createStatusBar(True)
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

    # find tip in database
    def on_select(self):
        try:
            s = "" # to add command in ToolTip
            f = str(self.f_label.textCursor().selectedText()) # Get Selected Text
            # Connect database
            conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '\\'+'identifier.sqlite')
            cur = conn.cursor()
            # get all command from database
            cur.execute("select * from name_commands where name = '%s';"% f)
            conn.commit()
            ones = cur.fetchall()
            # if not find command
            self.f_label.setToolTip("")
            # Find command
            for one in ones:

                # If select text is command
                if f == str(one[1]):
                    # Add name command to Tool
                    s += "<div>" + "<b>Назва команди:</b> <br>" + str(one[1]) + "</div>"
                    # Find description command
                    cur.execute("select des_text from table_description where id ='%s';" % one[0])
                    des = cur.fetchone()

                    if str(des[0]) != "None":
                        # Add description command to Tool
                        s += "<div>" + "<b>Опис:</b> <br>" + str(des[0]) + "</div>"
                    # Find parameter command
                    cur.execute("select param from table_parameter where id ='%s';" % one[0])
                    des = cur.fetchone()

                    if str(des[0]) != "None":
                        # Add parameter command to Tool
                        s += "<div>" + "<b>Параметри:</b> <br>" + str(des[0]) + "</div>"
                    # Find example command
                    cur.execute("select example_text from table_example where id ='%s';" % one[0])
                    des = cur.fetchone()

                    if str(des[0]) != "None":
                        # Add example command to Tool
                        s += "<div>" + "<b>Приклад:</b> <br>" + str(des[0]) + "</div>"
                    # Output Tip
                    self.f_label.setToolTip(s)
                    break
            conn.close()
        # If error in database
        except sqlite3.Error as E:
            self.f_label.setToolTip("В базі даних помилка!" + str(E))

    def main_text_field(self):  # place to tex-file;
        self.f_label = QTextEdit(self)
        self.f_label.setFontPointSize(10)
        self.f_label.selectionChanged.connect(self.on_select)
        # open tex-file when open program
        if os.path.isfile (XML.get_osnova_XML('tec-address')+"/"+XML.get_osnova_XML('tec-name-file') + ".tex"):
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", "r",
                      encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())
    # Initiate text_place into main_structure()

        self.form_lay = QFormLayout()
        self.form_lay.addRow(self.f_label)
        self.form_frame.setLayout(self.form_lay)
        # Initiate highlighter text
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