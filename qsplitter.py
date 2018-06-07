from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSplitter, QListWidget, QTreeWidget, QTextEdit, QMainWindow

if __name__ == '__main__':
    app = QApplication([])

    win = QMainWindow()

    splitter = QSplitter()
    list = QListWidget()
    tree = QTreeWidget()
    text = QTextEdit()

    splitter.setOrientation(Qt.Vertical)
    splitter.addWidget(list)
    splitter.addWidget(tree)
    splitter.addWidget(text)

    win.setCentralWidget(splitter)
    win.show()

    app.exec()
