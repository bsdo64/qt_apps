from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout


class RightSide(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(0, 0, 300, 100)

        pal = self.palette()

        pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)


class Chart(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(0, 0, 300, 100)

        pal = self.palette()

        pal.setColor(QPalette.Background, Qt.red)
        self.setAutoFillBackground(True)
        self.setPalette(pal)


if __name__ == '__main__':
    app = QApplication([])

    chart_win = QMainWindow()

    layout_widget = QWidget()
    layout = QGridLayout()
    layout.addWidget(Chart())
    layout.addWidget(RightSide())
    layout_widget.setLayout(layout)

    chart_win.setCentralWidget(layout_widget)
    chart_win.show()

    app.exec()
