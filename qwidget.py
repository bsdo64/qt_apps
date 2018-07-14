from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

from util import perf_timer


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    @perf_timer('paint')
    def paintEvent(self, a0: QtGui.QPaintEvent):
        widget_painter = QPainter(self)

        pixmap = QPixmap()
        widget_painter.drawPixmap(0, 0, pixmap)

if __name__ == '__main__':
    app = QApplication([])

    widget = MyWidget()

    widget.show()

    app.exec_()