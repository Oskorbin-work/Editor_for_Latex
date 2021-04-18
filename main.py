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

# -----------------------------------------------------------
# Other library
# -----------------------------------------------------------
import sys # Initiate project into operating system
from distutils.spawn import find_executable
import sqlite3


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
        s = "fsds"
        f = str(self.f_label.textCursor().selectedText())
        if (f == "PDF"):
            self.f_label.setToolTip(s)
        else:
            self.f_label.setToolTip(str(self.f_label.textCursor().selectedText()))

    def main_text_field(self):  # place to tex-file;
        self.f_label = QTextEdit(self)
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
        print("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf")
        self.main_window_view_pdf_val.load(
            QUrl("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))
        self.ver_box = QVBoxLayout()
        self.ver_box.addWidget(self.main_window_view_pdf_val)
        self.ver_frame.setLayout(self.ver_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if find_executable('latex'):
        ex = Main_windows()
    else:
        ex = Error_latex()
    sys.exit(app.exec_())