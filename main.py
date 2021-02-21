import data.XML.work_with_XML as XML
from PyQt5.QtWidgets import *
import sys
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        textEdit = QTextEdit()

        exitAction = QAction( 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle(XML.get_attr_XML('name-title'))

        layout.setSpacing(10)
        layout.addWidget(textEdit)

        self.setLayout(layout)

        self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())