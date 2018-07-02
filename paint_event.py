from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QThread, pyqtSignal, QLineF, QPoint
from PyQt5.QtGui import QPen, QPainter, QBrush, QColor, QPainterPath, QCursor
from PyQt5.QtWidgets import QApplication, QGraphicsView, QMainWindow, QHBoxLayout, QPushButton, QWidget, QGraphicsScene, \
    QGraphicsItem, QSizePolicy, QStyleOptionButton, QStyle

import pyqtgraph

class Plot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(460, 240)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.pos = QPoint()
        self.moving = QPoint()
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, ev: QtGui.QPaintEvent):

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(Qt.black)
        pen.setWidth(4)
        p.setPen(pen)
        r = self.rect().adjusted(10, 10, -10, -10)
        p.drawRoundedRect(r, 20, 10)

        p.save()
        r.adjust(2, 2, -2, -2)
        p.setViewport(r)
        r.moveTo(0, -r.height()//2)
        p.setWindow(r)
        self.draw_chart(p, r)
        p.restore()

    def draw_chart(self, p, r):
        p.setPen(Qt.red)
        p.drawLine(0, 0, r.width(), 0)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        self.pos = ev.pos()

        self.update()
        # super().mouseReleaseEvent(ev)

    def wheelEvent(self, ev: QtGui.QWheelEvent):

        self.moving += ev.angleDelta()
        self.update()

        # super().wheelEvent(ev)


class OpeningData(QThread):
    finished = pyqtSignal(object)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        import pandas as pd

        df = pd.read_pickle('bitmex_1m_2018.pkl')

        df['timestamp'] = df['timestamp'].astype('datetime64[ns]')

        self.finished.emit(df)


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setup_ui()

        self.my_thread = OpeningData(self)
        self.my_thread.finished.connect(self.opening_finished)

    def setup_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton()
        button.setText('import')
        button.setMaximumSize(100, 100)

        self.layout.addWidget(Plot(self))
        self.layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        if self.my_thread.isRunning():
            print("thread running wait....")
            return

        self.my_thread.start()

    def opening_finished(self, data):
        print(data.dtypes)


if __name__ == '__main__':
    app = QApplication([])

    win = Window()
    win.show()

    app.exec_()