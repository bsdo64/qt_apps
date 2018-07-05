import pandas
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QPointF, QFile, QDataStream, QIODevice
from PyQt5.QtGui import QPen, QColor, QMouseEvent, QBrush, QTransform, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QOpenGLWidget, QGraphicsPathItem

from util import perf_timer

# class ChartItem(QGraphicsPathItem):
#     def __init__(self, parent=None):
#         QGraphicsPathItem.__init__(self, parent)

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
        self.tick_range = 3
        self.x_marker_size: float = None
        self.y_marker_size: float = None
        self.gap: float = None
        self.width = 5


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setMouseTracking(True)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('#131722'))
        self.setMinimumSize(400, 400)
        self.setFrameStyle(self.NoFrame)

        self.data: pandas.DataFrame = None
        self.trans = ChartTransform()
        self.path = None

    @perf_timer("ChartView.init_data()")
    def init_data(self, data: pandas.DataFrame):
        self.data = data
        self.make_path()

    def make_path(self):
        file = QFile('sample.dat')
        path = QPainterPath()

        series = self.data['close'] - self.data['close'].min()

        print(series)
        if file.exists():
            file.open(QIODevice.ReadOnly)
            file_in = QDataStream(file)
            file_in >> path
            file.close()
        else:

            for i in range(len(self.data) - 1):
                path.moveTo(QPointF(i, series[i]))
                path.lineTo(QPointF(i+1, series[i+1]))

            file.open(QIODevice.WriteOnly)
            out = QDataStream(file)
            out << path
            file.close()

        self.path = path
        plot = QGraphicsPathItem(path)
        pen = QPen(Qt.gray)
        pen.setCosmetic(True)
        plot.setPen(pen)
        self.scene().addItem(plot)

    @perf_timer("ChartView.mouseMoveEvent()", False)
    def mouseMoveEvent(self, event: QMouseEvent):
        print()
        print(event.pos())
        print(self.mapToScene(event.pos()))

        super().mouseMoveEvent(event)

    @perf_timer("ChartView.wheelEvent()")
    def wheelEvent(self, event: QtGui.QWheelEvent):
        delta_x = event.pixelDelta().x()

        delta_y = event.pixelDelta().y()

        self.trans.d_start += delta_x
        self.trans.d_range += delta_y

        print(self.trans.d_start, self.trans.d_range)

        super().wheelEvent(event)

    @perf_timer("ChartView.resizeEvent()")
    def resizeEvent(self, event: QtGui.QResizeEvent):

        self.setSceneRect(0, 0,
                          self.width(), self.height())

        # plot: QGraphicsPathItem = self.scene().items()[0]
        # trans = QTransform()
        # trans.scale(self.width() / (len(self.data) + 1),
        #             self.height() / (self.data['close'].max() - self.data['close'].min() + 1))
        # plot.setTransform(trans)

        super().resizeEvent(event)


class Chart:
    def __init__(self, data):
        self.data = data
        self.main_view = ChartView()
        self.main_view.setScene(QGraphicsScene())
        self.main_view.resize(640, 480)

        self.main_view.init_data(data)

    def show(self):
        self.main_view.setViewport(QOpenGLWidget())
        self.main_view.setRenderHint(QPainter.Antialiasing)
        self.main_view.show()
