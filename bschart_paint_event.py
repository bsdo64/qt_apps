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
        option = QStyleOptionButton()
        option.initFrom(self)

        #background
        p.fillRect(0, 0, self.width(), self.height(), QColor('#131722'))

        #x-grid
        path = QPainterPath()
        x = self.moving.x()
        y = self.moving.y()
        path.moveTo(x + -4, 0 + y)
        path.lineTo(x + -4, 233 + + y)
        path.moveTo(x + 93, 0 + y)
        path.lineTo(x + 93, 233 + + y)
        path.moveTo(x + 190, 0 + y)
        path.lineTo(x + 190, 233 + + y)
        path.moveTo(x + 287, 0 + y)
        path.lineTo(x + 287, 233 + + y)
        path.moveTo(x + 384, 0 + y)
        path.lineTo(x + 384, 233 + + y)

        p.setPen(QColor('#363c4e'))
        p.drawPath(path)

        #y-grid
        path = QPainterPath()
        path.moveTo(x + 0, 2 + y)
        path.lineTo(x + 440, 2 + y)
        path.moveTo(x + 0, 40 + y)
        path.lineTo(x + 440, 40 + y)
        path.moveTo(x + 0, 77 + y)
        path.lineTo(x + 440, 77 + y)
        path.moveTo(x + 0, 114 + y)
        path.lineTo(x + 440, 114 + y)
        path.moveTo(x + 0, 152 + y)
        path.lineTo(x + 440, 152 + y)
        path.moveTo(x + 0, 189 + y)
        path.lineTo(x + 440, 189 + y)
        path.moveTo(x + 0, 226 + y)
        path.lineTo(x + 440, 226 + y)
        p.setPen(QColor('#363c4e'))
        p.drawPath(path)

        # candle
        p.fillRect(44, 40, 1, 0, QColor('#336854'))
        p.fillRect(34, 35, 1, 9, QColor('#336854'))
        p.fillRect(24, 12, 1, 37, QColor('#336854'))
        p.fillRect(15, 44, 1, 28, QColor('#336854'))
        p.fillRect(5, 68, 1, 23, QColor('#336854'))
        p.fillRect(-5, 12, 1, 102, QColor('#336854'))

        p.fillRect(41, 40, 7, 1, QColor('#53b987'))
        p.fillRect(31, 40, 7, 1, QColor('#53b987'))
        p.fillRect(21, 40, 7, 5, QColor('#53b987'))
        p.fillRect(12, 44, 7, 29, QColor('#53b987'))
        p.fillRect(2, 72, 7, 15, QColor('#53b987'))
        p.fillRect(-8, 86, 7, 29, QColor('#53b987'))

        if option.state & QStyle.State_MouseOver:
            self.setCursor(Qt.PointingHandCursor)
            # print(self.width(), self.height())

        #price
        path = QPainterPath()
        path.moveTo(0, 40)
        path.lineTo(440, 40)
        pen = p.pen()
        pen.setStyle(Qt.DashDotLine)
        pen.setColor(QColor("#53b987"))
        p.setPen(pen)
        p.drawPath(path)

        #mouse
        path = QPainterPath()
        path.moveTo(0, self.pos.y())
        path.lineTo(self.width(), self.pos.y())
        path.moveTo(self.pos.x(), 0)
        path.lineTo(self.pos.x(), self.height())
        p.setPen(Qt.red)
        p.drawPath(path)

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