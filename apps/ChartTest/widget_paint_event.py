import pandas as pd
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QPixmap

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsView, \
    QGraphicsScene
from util import perf_timer


data_range = 100000
width = 640
height = 480


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    @perf_timer("MyWidget.paintEvent()") # 600 ms
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        pen.setCosmetic(True)
        painter.setPen(pen)

        for i in range(data_range):
            painter.drawRect(QRectF(i / data_range * width,
                                    i / data_range * height,
                                    (i + 10) / width,
                                    (i + 10) / height)
                             )


class MyWidget2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.df = pd.DataFrame({
            'x': np.arange(0, data_range) / data_range * width,
            'y': np.arange(0, data_range) / data_range * height,
            'width': np.arange(0, data_range) / data_range * width,
            'height': np.arange(0, data_range) / data_range * height,
        })

    @perf_timer("MyWidget2.paintEvent()")  # 6000 ms
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        pen.setCosmetic(True)
        painter.setPen(pen)

        rects = []

        for i in range(data_range):
            rects.append(QRectF(self.df['x'][i], self.df['y'][i], self.df['width'][i], self.df['height'][i]))

        painter.drawRects(rects)


class MyWidget3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    @perf_timer("MyWidget.paintEvent()") # 1600 ms
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        pen.setCosmetic(True)
        painter.setPen(pen)

        for i in range(data_range):
            painter.fillRect(QRectF(i / data_range * width,
                                    i / data_range * height,
                                    (i + 10) / width,
                                    (i + 10) / height),
                             Qt.green
                             )


class MyWidget4(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.df = pd.DataFrame({
            'x': np.arange(0, data_range) / data_range * width,
            'y': np.arange(0, data_range) / data_range * height,
            'width': np.arange(0, data_range) / data_range * width,
            'height': np.arange(0, data_range) / data_range * height,
        })

        self.path = QPainterPath()
        for i in range(data_range):
            self.path.moveTo(self.df['x'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i] + self.df['height'][i])
            self.path.lineTo(self.df['x'][i], self.df['y'][i])

    @perf_timer("MyWidget.paintEvent()") # 48000 ms
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        pen.setCosmetic(True)
        painter.setPen(pen)

        painter.fillPath(self.path, Qt.red)


class MyWidget5(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.df = pd.DataFrame({
            'x': np.arange(0, data_range) / data_range * width,
            'y': np.arange(0, data_range) / data_range * height,
            'width': np.arange(0, data_range) / data_range * width,
            'height': np.arange(0, data_range) / data_range * height,
        })

        self.path = QPainterPath()
        for i in range(data_range):
            self.path.moveTo(self.df['x'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i] + self.df['height'][i])
            self.path.lineTo(self.df['x'][i], self.df['y'][i])

    @perf_timer("MyWidget.paintEvent()") # 700 ms
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        pen.setCosmetic(True)
        painter.setPen(pen)

        painter.drawPath(self.path)


class MyGraphicsItem(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.df = pd.DataFrame({
            'x': np.arange(0, data_range) / data_range * width,
            'y': np.arange(0, data_range) / data_range * height,
            'width': np.arange(0, data_range) / data_range * width,
            'height': np.arange(0, data_range) / data_range * height,
        })

        self.path = QPainterPath()
        for i in range(data_range):
            self.path.moveTo(self.df['x'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i])
            self.path.lineTo(self.df['x'][i] + self.df['width'][i], self.df['y'][i] + self.df['height'][i])
            self.path.lineTo(self.df['x'][i], self.df['y'][i])

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = ...):
        painter.drawPath(self.path)

    def boundingRect(self):
        return self.shape().boundingRect()


if __name__ == '__main__':
    app = QApplication([])

    # win = MyWidget()  # 600 ms
    # win = MyWidget2() # 6000 ms
    # win = MyWidget3() # 1600 ms
    # win = MyWidget4() # 48000 ms
    # win = MyWidget5() # 700 ms

    win = QGraphicsView()
    scene = QGraphicsScene()
    win.setScene(QGraphicsScene())
    print('init success')
    win.resize(width, height)
    win.show()

    app.exec()