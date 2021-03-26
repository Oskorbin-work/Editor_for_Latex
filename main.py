import data.XML.work_with_XML as XML
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
import os.path
from PyQt5 import QtWebEngineWidgets
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.f_label = QTextEdit(self)
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

        newAction = QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new_file)

        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.open_file)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save_file)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

    def osnova(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_lay = QFormLayout()
        form_lay.addRow(self.f_label)
        form_frame.setLayout(form_lay)

        ver_frame = QFrame()
        ver_frame.setFrameShape(QFrame.StyledPanel)

        v = QWebEngineView()
        v.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        v.load(QUrl("file:///alife.pdf"))
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

    def save_file(self):
        with open('test.tex', 'w', encoding='utf-8') as f:
            my_text = self.f_label.toPlainText()
            f.write(my_text)

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileNames(self,'Open file','./','Tex files (*.tex)')
        if not file:
             return
        else:
            with open(file[0], encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())

    def new_file(self):
        self.f_label.setPlainText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())