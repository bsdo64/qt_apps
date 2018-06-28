import time

import numpy as np
import pandas as pd

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, QRectF
from PyQt5.QtGui import QColor, QPainterPath, QPen, QTransform
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QStyleOptionGraphicsItem, \
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, \
    QGraphicsSceneWheelEvent
from scipy.linalg import norm


class AxisItem(QGraphicsItem):
    def __init__(self, data: pd.DataFrame, parent=None):
        QGraphicsItem.__init__(self, parent)
        # self.setAcceptHoverEvents(True)
        self.data = data
        self.max = data['close'].max()
        self.min = data['close'].min()
        self.length = data['close'].size
        self.setZValue(1)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):
        view = self.scene().views()[0]
        height = view.height()
        width = view.width()

        count = float(width / self.length)

        s = time.perf_counter()
        painter.save()
        path = QPainterPath()
        for i in np.arange(self.length):
            path.moveTo(count * i, 0)
            path.lineTo(count * i, height)

        painter.setPen(QColor('#363c4e'))
        painter.drawPath(path)
        painter.restore()
        print("Timer:AxisItem() : ", (time.perf_counter() - s)*1000)

    def boundingRect(self):
        view = self.scene().views()[0]
        rect = view.rect()

        return QRectF(int(rect.x()), int(rect.y()),
                      int(rect.width()), int(rect.height()))


class PlotItem(QGraphicsItem):
    def __init__(self, data: pd.DataFrame, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.setAcceptHoverEvents(True)
        self.data = data
        self.max = data['close'].max()
        self.min = data['close'].min()
        self.length = data['close'].size
        self.mouse_over = False
        self.cached = False
        self.path = None
        self.delta = 0
        self.setZValue(2)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):
        flip = -1
        view = self.scene().views()[0]
        height = view.height()
        width = view.width()

        margin_max = self.max + 10
        margin_min = self.min - 10
        gap = margin_max - margin_min
        count = float(width / self.length)
        count_v = float(height / gap)

        s = time.perf_counter()
        painter.save()
        self.data['x'] = np.arange(self.length) * count + self.delta
        self.data['y'] = (self.data['close'] - margin_min) * count_v * flip + height

        path = self.path
        if path is None and self.cached is False:
            path = QPainterPath()
            for i in np.arange(self.length - 1):
                path.moveTo(self.data['x'][i], self.data['y'][i])
                path.lineTo(self.data['x'][i+1], self.data['y'][i+1])

            self.path = path
            self.cached = True

        path.translate(self.delta, 0)
        # path = QPainterPath()
        # for i in np.arange(self.length - 1):
        #     path.moveTo(self.data['x'][i], self.data['y'][i])
        #     path.lineTo(self.data['x'][i+1], self.data['y'][i+1])

        print("Timer:PlotItem() : ", (time.perf_counter() - s) * 1000)

        pen = QPen(Qt.white)
        if self.mouse_over:
            pen.setWidth(2)
            view.setCursor(Qt.PointingHandCursor)
        else:
            view.setCursor(Qt.ArrowCursor)

        painter.setPen(pen)
        painter.drawPath(path)
        painter.restore()

    def boundingRect(self):
        view = self.scene().views()[0]

        rect = view.rect()
        return QRectF(int(rect.x()), int(rect.y()),
                      int(rect.width()), int(rect.height()))

    def hoverMoveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        self.mouse_over = False
        pos = self.mapToScene(event.pos())

        print()
        print("Scene Pos : ", pos)

        data = self.data
        dist = (pos.x() - data['x']) ** 2 + (pos.y() - data['y']) ** 2

        min_pos_idx = dist.idxmin()
        self.update()
        if 1 < min_pos_idx < dist.size - 1:
            min_pos = (data['x'][min_pos_idx], data['y'][min_pos_idx])
            min_pos_minus = (data['x'][min_pos_idx + 1], data['y'][min_pos_idx + 1])
            min_pos_plus = (data['x'][min_pos_idx - 1], data['y'][min_pos_idx - 1])

            a2 = (min_pos[0] - min_pos_minus[0], min_pos[1] - min_pos_minus[1])
            a3 = (pos.x() - min_pos_minus[0], pos.y() - min_pos_minus[1])

            b2 = (min_pos[0] - min_pos_plus[0], min_pos[1] - min_pos_plus[1])
            b3 = (pos.x() - min_pos_plus[0], pos.y() - min_pos_plus[1])

            print("dot : ", np.dot(a3, b3))
            if np.dot(a3, b3) < 1000:

                # 2D distance = abs(np.cross(p2 - p1, p3 - p1) / norm(p2 - p1))
                min_dist1 = abs(np.cross(a2, a3) / norm(a2))
                min_dist2 = abs(np.cross(b2, b3) / norm(b2))

                min_dist = min(min_dist1, min_dist2)
                print("min_dist : ", min_dist)
                if min_dist < 2:
                    self.mouse_over = True
                    self.update()

        super().hoverMoveEvent(event)

    def wheelEvent(self, event: 'QGraphicsSceneWheelEvent'):

        self.delta = event.delta()
        self.update()

        super().wheelEvent(event)


class GraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):

        super().mouseMoveEvent(event)


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('#131722'))
        self.setMinimumSize(400, 400)
        self.setWindowTitle(QObject.tr(self, 'Graph'))
        self.setFrameStyle(self.NoFrame)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        print()
        print("View Rect : ", self.rect())
        self.setSceneRect(self.rect().x(), self.rect().y(),
                          self.rect().width(), self.rect().height())
        print("Scene Rect : ", self.sceneRect())

        super().resizeEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        super().mouseMoveEvent(event)


if __name__ == '__main__':
    app = QApplication([])

    data = pd.read_pickle('bitmex_1m_2018.pkl')
    data = data[-2160:].reset_index()

    plot_data = data

    win = QWidget()
    hlayout = QHBoxLayout()

    view = GraphView()
    scene = GraphScene()
    view.setScene(scene)
    axis = AxisItem(data)
    plot = PlotItem(data)
    view.scene().addItem(axis)
    view.scene().addItem(plot)

    button1 = QPushButton('move left')
    button2 = QPushButton('move right')
    button3 = QPushButton('zoom in')
    button4 = QPushButton('zoom out')

    vlayout = QVBoxLayout()
    group = QWidget()
    group.setLayout(vlayout)
    vlayout.addWidget(button1)
    vlayout.addWidget(button2)
    vlayout.addWidget(button3)
    vlayout.addWidget(button4)

    hlayout.addWidget(view)
    hlayout.addWidget(group)

    win.setLayout(hlayout)
    win.show()

    app.exec_()
