import time

import numpy as np
import pandas as pd

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, QRectF, QDataStream, QFile, QIODevice
from PyQt5.QtGui import QColor, QPainterPath, QPen, QTransform
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QStyleOptionGraphicsItem, \
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, \
    QGraphicsSceneWheelEvent, QOpenGLWidget
from scipy.linalg import norm


def perf_timer(argument, debug=True):
    def real_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                s = time.perf_counter()
                result = fn(*args, **kwargs)
                print("{} : ".format(argument), (time.perf_counter() - s) * 1000)
            else:
                result = fn(*args, **kwargs)

            return result
        return wrapper
    return real_decorator


class AxisItem(QGraphicsItem):
    def __init__(self, data: pd.DataFrame, parent=None):
        QGraphicsItem.__init__(self, parent)
        # self.setAcceptHoverEvents(True)
        self.data = data
        self.max = data['close'].max()
        self.min = data['close'].min()
        self.length = data['close'].size
        self.cached = True
        self.path = None

        self.data_range_x_pix_min = 75
        self.data_range_x_pix_max = 150
        self.data_range_x_pix = 100
        self.setZValue(1)

    @perf_timer("Timer: AxisItem::paint()")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):
        view = self.scene().views()[0]
        height = view.height()
        width = view.width()

        painter.save()
        pen = QPen(QColor('#363c4e'))
        pen.setCosmetic(True)
        path = QPainterPath()
        for i in range(int(width / self.data_range_x_pix)):
            path.moveTo(width - i * self.data_range_x_pix, 0)
            path.lineTo(width - i * self.data_range_x_pix, height)

        painter.setPen(pen)
        painter.drawPath(path)
        painter.restore()

    # @perf_timer("Timer: AxisItem::boudningRect()")
    def boundingRect(self):
        view = self.scene().views()[0]
        rect = view.rect()

        return QRectF(rect.x(), rect.y(),
                      rect.width(), rect.height())

    # @perf_timer("Timer: AxisItem::wheelEvent()")
    def wheelEvent(self, event: 'QGraphicsSceneWheelEvent'):
        if self.data_range_x_pix_min > self.data_range_x_pix > 0:
            self.data_range_x_pix = self.data_range_x_pix_max
        elif self.data_range_x_pix_max <= self.data_range_x_pix:
            self.data_range_x_pix = self.data_range_x_pix_min
        elif self.data_range_x_pix_min <= self.data_range_x_pix < self.data_range_x_pix_max:
            pass
        else:
            self.data_range_x_pix = self.data_range_x_pix_min - 1


class PlotItem(QGraphicsItem):
    @perf_timer("Timer: PlotItem.__init__() : ")
    def __init__(self, data: pd.DataFrame, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.setAcceptHoverEvents(True)
        self.data = data
        self.max = data['close'].max()
        self.min = data['close'].min()
        self.length = data['close'].size
        self.mouse_over = False
        self.cached = False
        self.path = QPainterPath()
        self.data_range_x_pix = 0
        self.setZValue(2)

        self.create_path()

    def create_path(self):
        file = QFile('file.dat')
        path = QPainterPath()

        flip = -1
        height = view.height()
        width = view.width()

        margin_max = self.max + 10
        margin_min = self.min - 10
        gap = margin_max - margin_min
        count = float(width / self.length)
        count_v = float(height / gap)

        self.data['x'] = np.arange(self.length) * count
        self.data['y'] = (self.data['close'] - margin_min) * count_v * flip + height

        if not file.exists():

            for i in np.arange(self.length - 1):
                path.moveTo(self.data['x'][i], self.data['y'][i])
                path.lineTo(self.data['x'][i + 1], self.data['y'][i + 1])

            file.open(QIODevice.WriteOnly)
            out = QDataStream(file)
            out << path
            file.close()

        else:
            file.open(QIODevice.ReadOnly)
            file_in = QDataStream(file)
            file_in >> path
            file.close()

        self.path = path

    @perf_timer("Timer: PlotItem::paint() ")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):

        view = self.scene().views()[0]
        painter.save()

        pen = QPen(Qt.white)
        pen.setCosmetic(True)
        if self.mouse_over:
            view.setCursor(Qt.PointingHandCursor)
        else:
            view.setCursor(Qt.ArrowCursor)

        painter.setPen(pen)
        transform = QTransform()
        transform.scale(1 + self.data_range_x_pix / 1000, 1)
        painter.setTransform(transform)
        painter.drawPath(self.path)

        painter.restore()

    def boundingRect(self):
        view = self.scene().views()[0]

        rect = view.rect()
        return QRectF(rect.x(), rect.y(),
                      rect.width(), rect.height())

    @perf_timer("Timer: PlotItem::hoverMoveEvent() ")
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

            print("mouse distance : ", np.dot(a3, b3))
            if np.dot(a3, b3) < 1000:

                # 2D distance = abs(np.cross(p2 - p1, p3 - p1) / norm(p2 - p1))
                min_dist1 = abs(np.cross(a2, a3) / norm(a2))
                min_dist2 = abs(np.cross(b2, b3) / norm(b2))

                min_dist = min(min_dist1, min_dist2)
                print("min distance dist : ", min_dist)
                if min_dist < 2:
                    self.mouse_over = True
                    self.update()

        super().hoverMoveEvent(event)


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

    def wheelEvent(self, event: QtGui.QWheelEvent):

        items = self.items()
        plot: PlotItem = items[0]
        axis: AxisItem = items[1]

        axis.data_range_x_pix += event.pixelDelta().x()
        axis.update()

        plot.data_range_x_pix += event.pixelDelta().x()
        plot.update()

        super().wheelEvent(event)


if __name__ == '__main__':
    app = QApplication([])

    data = pd.read_pickle('bitmex_1m_2018.pkl')

    plot_data = data

    win = QWidget()
    hlayout = QHBoxLayout()

    view = GraphView()
    view.setViewport(QOpenGLWidget())
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
