from GUI.main_window.bar import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
from PyQt5 import QtWebEngineWidgets


class Window(QMainWindow, Bar):
    def __init__(self):
        super().__init__()
        self.bar_category_fileMenu()
        self.main_text_field()
        self.view_pdf()
        self.main_structure()
        self.main_window_splitter()
        self.structure_main_windows()
        self.main_windows_parameter()

    def main_windows_parameter(self):
        self.setWindowTitle(XML.get_attr_XML('name-title'))
        self.showMaximized()

    def main_text_field(self):
        self.f_label = QTextEdit(self)
        if XML.get_osnova_XML('tec-address') != "" and XML.get_osnova_XML('tec-name-file') != "":
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex",
                      encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())

    def view_pdf(self):
        self.v = QWebEngineView()
        self.v.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.v.load(
            QUrl("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))

    def main_window_splitter(self):
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.form_frame)
        self.splitter.addWidget(self.ver_frame)
        self.splitter.setSizes([200, 220])

    def main_structure(self):
        self.form_frame = QFrame()
        self.form_frame.setFrameShape(QFrame.StyledPanel)
        form_lay = QFormLayout()
        form_lay.addRow(self.f_label)

        self.form_frame.setLayout(form_lay)

        self.ver_frame = QFrame()
        self.ver_frame.setFrameShape(QFrame.StyledPanel)

        ver_box = QVBoxLayout()
        ver_box.addWidget(self.v)
        self.ver_frame.setLayout(ver_box)

    def structure_main_windows(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.splitter)
        self.setCentralWidget(self.splitter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())