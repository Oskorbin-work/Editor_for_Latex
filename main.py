import data.XML.work_with_XML as XML
from PyQt5.QtWidgets import *
import sys
class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle(XML.get_attr_XML('name-title'))

        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("Hello, World!")
        layout.addWidget(label, 0, 0)

app = QApplication(sys.argv)

screen = Window()
screen.showMaximized()

sys.exit(app.exec_())