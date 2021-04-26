# -----------------------------------------------------------
# PyQt 5. Include QSyntaxHighlighter
# -----------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.Qt import QSyntaxHighlighter, QRegularExpression


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        # Dictionary of special expressions
        self.regexp_by_format = dict()

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.blue)
        self.regexp_by_format[r'\\[^()({|[|}|\]|\s)]+'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.gray)
        self.regexp_by_format[r'[^\\]%.*'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.gray)
        self.regexp_by_format[r'^%.*'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkCyan)
        self.regexp_by_format[r'\[[^()[^}]+\]'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkGreen)
        self.regexp_by_format[r'{[^()}]+}'] = char_format

        char_format = QTextCharFormat()
        char_format.setForeground(Qt.darkMagenta)
        self.regexp_by_format[r'(%CommandsGenerationlatexpython|%Generationlatexpython_Disable|%IncludeDocx|Cell\s*(?=\()' \
                              r'|Cell_disable\s*(?=\()|%CommandsGenerationlatexpython)|%Generationlatexpython'\
                              r''] = char_format

    def highlightBlock(self, text):
        for regexp, char_format in self.regexp_by_format.items():
            expression = QRegularExpression(regexp)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)
