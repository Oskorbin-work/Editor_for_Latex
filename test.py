# from PyQt5.Qt import QSyntaxHighlighter, QTextCharFormat, QFont, Qt, QRegularExpression, QApplication, QTextEdit
from PyQt5.Qt import *
import PyQt5


class MyHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setForeground(Qt.darkMagenta)

        expression = QRegularExpression(r"small")
        it = expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


if __name__ == '__main__':
    print(PyQt5.__file__)
    app = QApplication([])

    mw = QTextEdit()

    a = MyHighlighter(mw.document())

    mw.show()

    app.exec()