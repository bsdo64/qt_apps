import pandas as pd
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QPixmap

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsView, \
    QGraphicsScene, QGraphicsPathItem, QGraphicsSceneHoverEvent
from util import perf_timer


data_range = 10000
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

    @perf_timer("MyGraphicsItem.paint()")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = ...):
        painter.drawPath(self.path)

    def boundingRect(self):
        return QRectF(0, 0, 640, 480)


class MyGraphicsItem2(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.df = pd.read_pickle('../../bitmex_1m_2018.pkl')

        self.path = QPainterPath()
        for i in range(data_range):
            self.path.addRect(i / width, self.df['open'][i] / height,
                              10, self.df['open'][i] - self.df['close'][i])

    @perf_timer("MyGraphicsItem.paint()")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = ...):
        pen = QPen()
        pen.setCosmetic(True)
        pen.setColor(Qt.green)
        painter.setPen(pen)
        painter.drawPath(self.path)

    def boundingRect(self):
        return QRectF(0, 0, 640, 480)


df = pd.read_pickle('../../bitmex_1m_2018.pkl')

path = QPainterPath()
for i in range(data_range):
    path.addRect(i / width, df['open'][i] / height,
                 10, df['open'][i] - df['close'][i])

MyGraphicsItem3 = QGraphicsPathItem(path)
perf_timer("painter")(MyGraphicsItem3.paint)


class MyGraphicsItem4(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.setAcceptHoverEvents(True)

    @perf_timer("painter")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget= ...):
        painter.fillPath(path, Qt.green)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.setCursor(Qt.PointingHandCursor)

if __name__ == '__main__':
    app = QApplication([])

    win = MyWidget()  # 400 ms
    # win = MyWidget2() # 4187 ms
    # win = MyWidget3() # 722 ms
    # win = MyWidget4() # 6250 ms
    # win = MyWidget5() # ~ 400 ms

    win = QGraphicsView()
    scene = QGraphicsScene()
    # scene.addItem(MyGraphicsItem())
    # scene.addItem(MyGraphicsItem2())
    # scene.addItem(MyGraphicsItem3)
    scene.addItem(MyGraphicsItem4())
    win.setScene(scene) # 400 ms

    print('init success')
    win.resize(width, height)
    win.show()

    app.exec()