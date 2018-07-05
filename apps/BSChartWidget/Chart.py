import pandas
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QFile, QDataStream, QIODevice
from PyQt5.QtGui import QPen, QColor, QMouseEvent, QPainter, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, \
    QGraphicsItem, QStyleOptionGraphicsItem
from sys import platform
from util import perf_timer


class ChartItem(QGraphicsItem):
    def __init__(self, path, trans, data, parent=None):
        QGraphicsItem.__init__(self, parent)

        self.path:  QPainterPath = path
        self.trans: ChartTransform = trans
        self.data:  pandas.DataFrame = data

    @perf_timer("Timer: PlotItem::paint() ")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):

        painter.save()

        pen = QPen(Qt.white)
        pen.setCosmetic(True)

        df = self.data[-self.trans.d_range:]
        y_ratio = 1.5
        trans = painter.transform()
        trans.translate(-620 * y_ratio, 300 * y_ratio)
        trans.scale(1, y_ratio)

        painter.setTransform(trans)
        painter.setPen(pen)
        painter.drawPath(self.path)

        painter.restore()

    def boundingRect(self):
        view = self.scene().views()[0]

        rect = view.rect()
        return QRectF(rect.x(), rect.y(),
                      rect.width(), rect.height())

#
# class ChartScene(QGraphicsScene):
#     def __init__(self, parent=None):
#         QGraphicsScene.__init__(self, parent)
#

class ChartTransform:
    def __init__(self):
        # start point (inverted index of data)
        self.d_start = 0
        # data range
        self.d_range = 100
        # data range per pixel (d_range / pixel)
        self.x_marker_size: float = None
        self.y_marker_size: float = None
        self.gap: float = None
        self.width = 5
        self.view_width = 640
        self.view_height = 480


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('#131722'))
        self.setMinimumSize(640, 480)
        self.setFrameStyle(self.NoFrame)

        self.trans = ChartTransform()
        self.data: pandas.DataFrame = None
        self.path = None

    @perf_timer("ChartView.init_data()")
    def init_data(self, data: pandas.DataFrame):
        self.data = data
        self.add_plot()

    def add_plot(self):
        file = QFile('sample.dat')
        path = QPainterPath()

        flip = -1
        height = self.height()
        width = self.width()

        margin_max = self.data['close'].max() + 10
        margin_min = self.data['close'].min() - 10
        gap = margin_max - margin_min
        count = float(width / len(self.data))
        count_v = float(height / gap)

        self.data['x'] = np.arange(len(self.data)) * count
        self.data['y'] = (self.data['close'] - margin_min) * count_v * flip + height

        if not file.exists():

            path.moveTo(self.data['x'][0], self.data['y'][0])
            for i in np.arange(len(self.data) - 1):
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
        plot_item = ChartItem(path, self.trans, self.data)
        self.scene().addItem(plot_item)

    @perf_timer("ChartView.mouseMoveEvent()", False)
    def mouseMoveEvent(self, event: QMouseEvent):
        print()
        print(event.pos())
        print(self.mapToScene(event.pos()))

        super().mouseMoveEvent(event)

    @perf_timer("ChartView.wheelEvent()")
    def wheelEvent(self, event: QtGui.QWheelEvent):
        delta_x = 0
        delta_y = 0

        if platform == "linux" or platform == "linux2":
            delta_x = event.angleDelta().x()
            delta_y = event.angleDelta().y()
        elif platform == "darwin":
            delta_x = event.pixelDelta().x()
            delta_y = event.pixelDelta().y()
        elif platform == "win32":
            delta_x = event.angleDelta().x()
            delta_y = event.angleDelta().y()

        self.trans.d_start += delta_x
        self.trans.d_range += delta_y

        # plot: QGraphicsItem = self.scene().items()[0]
        # trans = plot.transform()
        # trans.translate(delta_x, 0)
        # # trans.scale(1 + delta_y / 1000, 1 + delta_y / 1000)
        # plot.setTransform(trans)
        #
        # print(trans.dx(), trans.dy())

        for item in self.scene().items():
            item.update()

        super().wheelEvent(event)

    @perf_timer("ChartView.resizeEvent()")
    def resizeEvent(self, event: QtGui.QResizeEvent):

        self.setSceneRect(0, 0,
                          self.width(), self.height())

        self.trans.view_width = self.width()
        self.trans.view_height = self.height()

        super().resizeEvent(event)


class Chart:
    def __init__(self, data):
        self.data = data
        self.main_view = ChartView()
        self.main_view.setScene(QGraphicsScene())
        self.main_view.resize(640, 480)

        self.main_view.init_data(data)

    def show(self):
        # self.main_view.setViewport(QOpenGLWidget())
        self.main_view.setRenderHint(QPainter.Antialiasing)
        self.main_view.show()
