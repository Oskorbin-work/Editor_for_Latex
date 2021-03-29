import data.XML.work_with_XML as XML
from PyQt5 import QtWidgets
import os, os.path
from PyQt5.QtWidgets import *


#  In class "Bar" -- menuBar in main program
class Bar:
    def __init__(self):  # Initiate menuBar
        self.menubar = self.menuBar()
        self.new_button_bar()
        self.open_button_bar()
        self.save_button_bar()
        self.save_as_button_bar()
        self.run_latex_to_pdf_button_bar()
        self.exit_button_bar()

    def bar_category_fileMenu(self):  # structure category "File menu"
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.RunAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exitAction)

    # ************************************************************
    # Buttons bar menu category "File"
    def new_button_bar(self):  # Button -- create new file.tex
        self.newAction = QAction('New', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.triggered.connect(self.new_file)

    def open_button_bar(self):  # Button -- open file.tex
        self.openAction = QAction('Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.open_file)

    def save_button_bar(self):  # Button -- save current file.tex
        self.saveAction = QAction('Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.save_file)

    def save_as_button_bar(self):  # Button -- save current file.tex where the user wants
        self.saveAsAction = QAction('Save as', self)
        self.saveAsAction.setShortcut('Alt+S')
        self.saveAsAction.triggered.connect(self.save_file_as)

    def run_latex_to_pdf_button_bar(self):  # Button -- convert current file.tex to file.pdf: tex to pdf
        self.RunAction = QAction('Run', self)
        self.RunAction.setShortcut('Ctrl+R')
        self.RunAction.triggered.connect(self.run_compile)

    def exit_button_bar(self):  # Button -- exit program
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    # ************************************************************
    # Functional buttons bar menu category "File"
    def new_file(self):  # create new file.tex
        self.f_label.setPlainText("")

    def open_file(self):  # open file.tex
        file, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", XML.get_osnova_XML('tec-address'),
                                                         "Tex files (*.tex)")
        if not file:
            return
        else:
            XML.change_val_XML('osnova', 'tec-address', os.path.split(file[0])[0])
            XML.change_val_XML('osnova', 'tec-name-file', os.path.splitext(os.path.basename(file[0]))[0])
            with open(file[0], encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())

    def save_file(self):  # save current file.tex
        with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", 'w',
                  encoding='utf-8') as f:
            my_text = self.f_label.toPlainText()
            f.write(my_text)

    def save_file_as(self):  # save current file.tex where the user wants
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save file as", XML.get_osnova_XML('tec-address'),
                                                     "Tex files (*.tex)")
        if file[0] == "":
            return
        else:
            XML.change_val_XML('osnova', 'tec-address', os.path.split(file[0])[0])
            XML.change_val_XML('osnova', 'tec-name-file', os.path.splitext(os.path.basename(file[0]))[0])
            with open(file[0], 'w', encoding='utf-8') as f:
                my_text = self.f_label.toPlainText()
                f.write(my_text)

    def run_compile(self):  # convert current file.tex to file.pdf: tex to pdf
        self.save_file()
        print("cmd /c pdflatex " + XML.get_osnova_XML('tec-name-file') + ".tex")
        os.chdir(XML.get_osnova_XML('tec-address') + '/')
        os.system("cmd /c pdflatex " + XML.get_osnova_XML('tec-name-file') + ".tex")
        self.v.reload()

    # The program is closed by the built-in function

    # ************************************************************
