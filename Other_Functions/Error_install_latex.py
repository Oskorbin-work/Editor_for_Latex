# -----------------------------------------------------------
# Codes other files project
# -----------------------------------------------------------
from GUI.main_window.bar import * # Initiate bar-structure
from main import QMainWindow
# -----------------------------------------------------------
# PyQt 5.Initiate structure Main window and GUI
# -----------------------------------------------------------
from PyQt5.QtWidgets import *


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