import os

from PyQt5 import uic
from PyQt5.QtCore import QFile, QIODevice, QMetaObject, Qt, pyqtSlot
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QMessageBox


def load_ui_file(parent):
    abspath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "textfinder.ui")
    return uic.loadUi(abspath, parent)


def load_text_file():
    return open('input.txt').read()


class TextFinder(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        form_widget = load_ui_file(self)

        self.ui_find_button = self.findChild(QPushButton, name='findButton')
        self.ui_text_edit = self.findChild(QTextEdit, name='textEdit')
        self.ui_line_edit = self.findChild(QLineEdit, name='lineEdit')

        QMetaObject.connectSlotsByName(self)

        self.ui_text_edit.setText(load_text_file())

        layout = QVBoxLayout()
        layout.addWidget(form_widget)
        self.setLayout(layout)

        self.setWindowTitle("Text Finder")

    def on_findButton_clicked(self):

        search_string = self.ui_line_edit.text()
        document = self.ui_text_edit.document()

        self.found = False

        document.undo()

        if not search_string:
            QMessageBox.information(self, "Empty Search Field", 'Please enter a word')

        else:
            highlight_cursor = QTextCursor(document)
            cursor = QTextCursor(document)

            cursor.beginEditBlock()

            plain_format = QTextCharFormat(highlight_cursor.charFormat())
            color_format = plain_format
            color_format.setForeground(Qt.red)

            while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
                highlight_cursor = document.find(search_string, highlight_cursor, QTextDocument.FindWholeWords)

                if not highlight_cursor.isNull():
                    self.found = True
                    highlight_cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
                    highlight_cursor.mergeCharFormat(color_format)

            cursor.endEditBlock()

            if not self.found:
                QMessageBox.information(self, "Word not found", "Sorry, the word coannot be found")

if __name__ == '__main__':

    app = QApplication([])

    textFinder = TextFinder()
    textFinder.show()

    app.exec()

