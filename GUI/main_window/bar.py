# -----------------------------------------------------------
# Codes other files project
# -----------------------------------------------------------

import data.XML.work_with_XML as XML  # Work with XML-file
import Main_Functions.Generation_latex as latex
# -----------------------------------------------------------
# PyQt 5.Initiate structure Main window and GUI
# -----------------------------------------------------------
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel,QAction,QMessageBox,QMainWindow
# -----------------------------------------------------------
# Few libraries
# -----------------------------------------------------------
import os  # To files Address


#  In class "Bar" -- menuBar in main program
class Bar:
    def __init__(self):  # Initiate menuBar
        self.wcLabel = QLabel(f"Error")
        self.menubar = self.menuBar()
        self.new_button_bar()
        self.open_button_bar()
        self.save_button_bar()
        self.save_as_button_bar()
        self.run_latex_to_pdf_button_bar()
        self.exit_button_bar()
        self.run_latex_to_pdf_button_bar_disable()
        self.help_button()

    def createStatusBar(self,Ready):
        # Adding a temporary message
        self.statusbar.addWidget(self.wcLabel)
        self.statusbar.removeWidget(self.wcLabel)
        if Ready == True:
            ready_to_work = " || " +"Очікую команди..." + " || "
        else:
            ready_to_work = " || " + "Обробляю команду..." + " || "
        if XML.get_osnova_XML('tec-address') != "" and XML.get_osnova_XML('tec-name-file') != "":
            self.wcLabel = QLabel(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file')
                                  + ".tex" + ready_to_work)
            self.statusbar.addWidget(self.wcLabel)
        else:
            self.wcLabel = QLabel("Зараз без адреси!" + ready_to_work)
            self.statusbar.addWidget(self.wcLabel)

    # structure category "File menu".
    # Initiate into main.py!
    def bar_category_fileMenu(self):
        #fileMenu = self.menubar.addMenu('&File')
        fileMenu = self.menubar.addMenu(XML.get_attr_XML('file'))
        run = self.menubar.addMenu(XML.get_attr_XML('run'))
        help = self.menubar.addMenu(XML.get_attr_XML('help'))

        # add action to "Файл"
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exitAction)

        # add action to "Запуск"
        run.addAction(self.RunAction)

        run.addAction(self.RunAction_disable)
        # add action to "Допомога"
        help.addAction(self.help)

    # -----------------------------------------------------------
    # Buttons bar menu category "Файл"
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

    def exit_button_bar(self):  # Button -- exit program
        self.exitAction = QAction(XML.get_attr_XML('file-exit'), self)
        self.exitAction.setShortcut(XML.get_hot_keyboard_XML('file-exit'))
        self.exitAction.triggered.connect(self.exit_program)

    # -----------------------------------------------------------
    # Buttons bar menu category "Запуск"

    # Button -- # convert current file.tex to file.pdf: tex to pdf.
    # "Запустити-с заміною команд"

    def run_latex_to_pdf_button_bar(self):
        self.RunAction = QAction(XML.get_attr_XML('run-enable'), self)
        self.RunAction.setShortcut(XML.get_hot_keyboard_XML('run-enable'))
        self.RunAction.triggered.connect(self.run_compile)

    # Button -- # convert current file.tex to file.pdf: tex to pdf.
    # "Запустити-без заміни заміною команд"
    def run_latex_to_pdf_button_bar_disable(self):
        self.RunAction_disable = QAction(XML.get_attr_XML('run-disable'), self)
        self.RunAction_disable.setShortcut(XML.get_hot_keyboard_XML('run-disable'))
        self.RunAction_disable.triggered.connect(self.run_compile_disable)

    # -----------------------------------------------------------
    # Buttons bar menu category "Допомога"

    # Button -- # guide to latex
    def help_button(self):
        self.help = QAction(XML.get_attr_XML('help-help'), self)
        self.help.setShortcut(XML.get_hot_keyboard_XML('help'))
        self.help.triggered.connect(self.help_pdf)

    # -----------------------------------------------------------
    # Functional buttons bar menu category "Файл"
    def new_file(self):  # create new file.tex
        self.createStatusBar(True)
        status = QMessageBox.question(self,"Новий файл", "Ви хочете створити новий файл?", QMessageBox.Yes,
                                      QMessageBox.No)
        if status == QMessageBox.Yes:
            self.save_file()
            self.f_label.setPlainText("")
            XML.change_val_XML('osnova', 'tec-name-file', "")
            self.createStatusBar(True)


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
        self.createStatusBar(True)

    def save_file(self):  # save current file.tex
        if os.path.isfile(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex"):
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", 'w',
                  encoding='utf-8') as f:
                my_text = self.f_label.toPlainText()
                f.write(my_text)
            self.createStatusBar(True)
        else:
            self.createStatusBar(True)
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
        self.createStatusBar(True)
    # Button -- # exit program
    def exit_program(self):
        status = QMessageBox.question(self,"Вихід із програми", "Ви хочете вийти із програми?", QMessageBox.Yes,
                                      QMessageBox.No)
        if status == QMessageBox.Yes:
            self.close()
    # -----------------------------------------------------------
    # Functional buttons bar menu category "Запуск"

    # convert current file.tex to file.pdf: tex to pdf. "Запустити-з заміною команд"
    def run_compile(self):
        self.createStatusBar(False)
        status = QMessageBox.question(self,"Запуск з заміною команд","Ви хочете конвертувати файл tex в pdf?",QMessageBox.Yes,QMessageBox.No)
        if status == QMessageBox.Yes:
            app = latex.Generation_latex()
            self.save_file()
            app.find_command_to_latex_file(
                XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", "enable")
            # print("cmd /c pdflatex -file-line-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
            os.chdir(XML.get_osnova_XML('tec-address') + '/')
            with open(XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex",
                      encoding='utf-8') as f:
                self.f_label.setPlainText(f.read())
            os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
            os.system("cmd /c pdflatex -file-line-error -halt-on-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
            # self.open_file()
            self.main_window_view_pdf_val.load(QUrl(
                "file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".pdf"))
        self.createStatusBar(True)

    # convert current file.tex to file.pdf: tex to pdf. "Запустити-без заміни заміною команд"
    def run_compile_disable(self):
        self.createStatusBar(False)
        status = QMessageBox.question(self,"Запуск без заміни команд","Ви хочете конвертувати файл tex в pdf?",QMessageBox.Yes,QMessageBox.No)
        if status == QMessageBox.Yes:
            app = latex.Generation_latex()
            self.save_file()
            app.find_command_to_latex_file(
                XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML('tec-name-file') + ".tex", "disable")
            # print("cmd /c pdflatex -file-line-error " + XML.get_osnova_XML('tec-name-file') + ".tex")
            os.chdir(XML.get_osnova_XML('tec-address') + '/')
            os.system("cmd /c pdflatex -file-line-error -halt-on-error -jobname " + XML.get_osnova_XML(
                    'tec-name-file') + " " + XML.get_osnova_XML(
                'tec-name-file') + '_enable' + ".tex")
            os.system("cmd /c pdflatex -file-line-error -halt-on-error -jobname " + XML.get_osnova_XML(
                    'tec-name-file') + " " + XML.get_osnova_XML(
                'tec-name-file') + '_enable' + ".tex")
            # self.open_file()
            self.main_window_view_pdf_val.load(QUrl(
                "file:///" + XML.get_osnova_XML('tec-address') + "/" + XML.get_osnova_XML(
                    'tec-name-file') + ".pdf"))
        self.createStatusBar(True)

    # -----------------------------------------------------------
    # Functional buttons bar menu category "Допомога"
    def help_pdf(self):
        adress = str(os.path.dirname(os.path.abspath(__file__)))
        adress = adress.replace('\\', '/')
        self.main_window_view_pdf_val.load(QUrl("file:///" + adress + "/ukr.pdf"))

    # The program is closed by the built-in function
    # -----------------------------------------------------------