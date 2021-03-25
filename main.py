from PyQt5 import QtWebEngineWidgets

import data.XML.work_with_XML as XML
from PyQt5.QtWidgets import *
from PyQt5.QtGui  import QFont, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import  *
from PyQt5.QtWebEngineWidgets import *
import qpageview
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os.path
from os import path
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bar()
        self.osnova()
        self.osnova_2()

    def osnova_2(self):
        self.setWindowTitle(XML.get_attr_XML('name-title'))
        self.showMaximized()

    def bar(self):

        exitAction = QAction( 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)


    def osnova(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)

        f_label = QTextEdit()

        form_lay = QFormLayout()
        form_lay.addRow(f_label)
        form_frame.setLayout(form_lay)

        ver_frame = QFrame()
        ver_frame.setFrameShape(QFrame.StyledPanel)

        v =  QWebEngineView()
        v.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        v.load(QUrl("file:///alife.pdf"))
        v.load(QUrl("file:///pdf.js/web/compressed.tracemonkey-pldi-09.pdf"))
        ver_box = QVBoxLayout()
        ver_box.addWidget(v)
        ver_box.setContentsMargins(10, 10, 10, 10)
        ver_frame.setLayout(ver_box)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(form_frame)
        splitter.addWidget(ver_frame)
        splitter.setSizes([200, 220])
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(splitter)
        self.setCentralWidget(splitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())