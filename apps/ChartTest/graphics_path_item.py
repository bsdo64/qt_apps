import pandas as pd
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPainterPath

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsPathItem, QGraphicsView, QGraphicsScene
from util import perf_timer


data_range = 100000
width = 640
height = 480

class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    @perf_timer("MyWidget.paintEvent()")
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)

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

    @perf_timer("MyWidget2.paintEvent()")
    def paintEvent(self, ev: QtGui.QPaintEvent):
        painter = QPainter(self)

        rects = []

        for i in range(data_range):
            rects.append(QRectF(self.df['x'][i], self.df['y'][i], self.df['width'][i], self.df['height'][i]))

        painter.drawRects(rects)



class MyPathItem(QGraphicsPathItem):
    def __init__(self, parent=None):
        QGraphicsPathItem.__init__(self, parent)



if __name__ == '__main__':
    app = QApplication([])

    view = QGraphicsView()
    view.resize(640, 480)
    scene = QGraphicsScene()

    view.setScene(scene)
    view.show()

    app.exec()