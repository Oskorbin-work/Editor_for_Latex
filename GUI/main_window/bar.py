# -----------------------------------------------------------
# Codes other files project
# -----------------------------------------------------------
from PyQt5.QtCore import QUrl

import data.XML.work_with_XML as XML  # Work with XML-file
import Main_Functions.Generation_latex as latex
# -----------------------------------------------------------
# PyQt 5.Initiate structure Main window and GUI
# -----------------------------------------------------------
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
# -----------------------------------------------------------
# Other library
# -----------------------------------------------------------
import os  # To files Address


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
        self.run_latex_to_pdf_button_bar_disable()

    def bar_category_fileMenu(self):  # structure category "File menu". Initiate into main.py!
        #fileMenu = self.menubar.addMenu('&File')
        fileMenu = self.menubar.addMenu(XML.get_attr_XML('file'))
        run = self.menubar.addMenu(XML.get_attr_XML('run'))
        fileMenu.addAction(self.newAction)
        run.addAction(self.RunAction)
        run.addAction(self.RunAction_disable)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exitAction)

    # -----------------------------------------------------------
    # Buttons bar menu category "File"
    def new_button_bar(self):  # Button -- create new file.tex
        self.newAction = QAction(XML.get_attr_XML('file-new'), self)
        self.newAction.setShortcut(XML.get_hot_keyboard_XML('file-new'))
        self.newAction.triggered.connect(self.new_file)

    def open_button_bar(self):  # Button -- open file.tex
        self.openAction = QAction(XML.get_attr_XML('file-open'), self)
        self.openAction.setShortcut(XML.get_hot_keyboard_XML('file-open'))
        self.openAction.triggered.connect(self.open_file)

    def save_button_bar(self):  # Button -- save current file.tex
        self.saveAction = QAction(XML.get_attr_XML('file-save'), self)
        self.saveAction.setShortcut(XML.get_hot_keyboard_XML('file-save'))
        self.saveAction.triggered.connect(self.save_file)

    def save_as_button_bar(self):  # Button -- save current file.tex where the user wants
        self.saveAsAction = QAction(XML.get_attr_XML('file-save-as'), self)
        self.saveAsAction.setShortcut(XML.get_hot_keyboard_XML('file-save-as'))
        self.saveAsAction.triggered.connect(self.save_file_as)

    def run_latex_to_pdf_button_bar(self):  # Button -- convert current file.tex to file.pdf: tex to pdf
        self.RunAction = QAction(XML.get_attr_XML('run-enable'), self)
        self.RunAction.setShortcut(XML.get_hot_keyboard_XML('run-enable'))
        self.RunAction.triggered.connect(self.run_compile)

    def run_latex_to_pdf_button_bar_disable(self):  # Button -- convert current file.tex to file.pdf: tex to pdf
        self.RunAction_disable = QAction(XML.get_attr_XML('run-disable'), self)
        self.RunAction_disable.setShortcut(XML.get_hot_keyboard_XML('run-disable'))
        self.RunAction_disable.triggered.connect(self.run_compile_disable)

    def exit_button_bar(self):  # Button -- exit program
        self.exitAction = QAction(XML.get_attr_XML('file-exit'), self)
        self.exitAction.setShortcut(XML.get_hot_keyboard_XML('file-exit'))
        self.exitAction.triggered.connect(self.close)

    # -----------------------------------------------------------
    # Functional buttons bar menu category "File"
    def new_file(self):  # create new file.tex
        self.save_file()
        self.f_label.setPlainText("")
        XML.change_val_XML('osnova', 'tec-name-file', "")

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

        if os.path.isfile(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex"):
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", 'w',
                  encoding='utf-8') as f:
                my_text = self.f_label.toPlainText()
                f.write(my_text)
        else:
            self.save_file_as()

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
        app = latex.Generation_latex()
        self.save_file()
        app.find_command_to_latex_file(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex","enable")
        #print("cmd /c pdflatex -file-line-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
        os.chdir(XML.get_osnova_XML('tec-address') + '/')
        with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", encoding='utf-8') as f:
            self.f_label.setPlainText(f.read())
        os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
        os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
        #self.open_file()
        self.main_window_view_pdf_val.load( QUrl("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))

    def run_compile_disable(self):  # convert current file.tex to file.pdf: tex to pdf
        app = latex.Generation_latex()
        self.save_file()
        app.find_command_to_latex_file(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex","disable")
        #print("cmd /c pdflatex -file-line-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
        os.chdir(XML.get_osnova_XML('tec-address') + '/')

        os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file')+'_test' + ".tex")
        os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file')+'_test' + ".tex")
        #self.open_file()
        self.main_window_view_pdf_val.load( QUrl("file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') +'_test'+ ".pdf"))

    # The program is closed by the built-in function

    # -----------------------------------------------------------
