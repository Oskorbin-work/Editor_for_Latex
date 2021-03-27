import data.XML.work_with_XML as XML
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
import os.path
import os
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

        saveAsAction = QAction('Save as', self)
        saveAsAction.setShortcut('Alt+S')
        saveAsAction.triggered.connect(self.save_file_as)

        RunAction = QAction('Run', self)
        RunAction.setShortcut('Ctrl+R')
        RunAction.triggered.connect(self.run_compile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(RunAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(exitAction)

    def osnova(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_lay = QFormLayout()
        form_lay.addRow(self.f_label)
        if XML.get_osnova_XML('tec-address') != "" and XML.get_osnova_XML('tec-name-file') != "":
            with open(XML.get_osnova_XML('tec-address') +"/" + XML.get_osnova_XML('tec-name-file') + ".tex", encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())

        form_frame.setLayout(form_lay)

        ver_frame = QFrame()
        ver_frame.setFrameShape(QFrame.StyledPanel)

        self.v = QWebEngineView()
        self.v.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.v.load(QUrl("file:///"+XML.get_osnova_XML('tec-address') +"/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))
        ver_box = QVBoxLayout()
        ver_box.addWidget(self.v)
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
        with open(XML.get_osnova_XML('tec-address') +"/" + XML.get_osnova_XML('tec-name-file') + ".tex", 'w', encoding='utf-8') as f:
            my_text = self.f_label.toPlainText()
            f.write(my_text)

    def save_file_as(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self,"Save file as",XML.get_osnova_XML('tec-address'),"Tex files (*.tex)")
        print(file)#Взять название нового файла.
        if file[0] == "":
            return
        else:
            XML.change_val_XML('osnova', 'tec-address', os.path.split(file[0])[0])
            XML.change_val_XML('osnova', 'tec-name-file', os.path.splitext(os.path.basename(file[0]))[0])
            with open(file[0], 'w', encoding='utf-8') as f:
                my_text = self.f_label.toPlainText()
                f.write(my_text)

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Open file",XML.get_osnova_XML('tec-address'),"Tex files (*.tex)")
        if not file:
             return
        else:
            XML.change_val_XML('osnova', 'tec-address', os.path.split(file[0])[0])
            XML.change_val_XML('osnova', 'tec-name-file', os.path.splitext(os.path.basename(file[0]))[0])
            with open(file[0], encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())

    def new_file(self):

        self.f_label.setPlainText("")

    def run_compile(self):
        print("cmd /c pdflatex " + XML.get_osnova_XML('tec-name-file') + ".tex")
        os.chdir(XML.get_osnova_XML('tec-address') + '/')
        os.system("cmd /c pdflatex " + XML.get_osnova_XML('tec-name-file') + ".tex" )
        self.v.reload()


#Разбить на классы. В "Bar" будет строка управления
class Bar(Window):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())