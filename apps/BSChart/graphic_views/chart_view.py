from sys import platform

import pandas

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsView

from data.model import Model
from graphic_scenes.candlestick import CandleStickItem
from graphic_scenes.chart_scene import ChartScene
from util.fn import attach_timer
from util.thread import Thread


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setBackgroundBrush(QColor('#1B1D27'))
        # self.setViewport(QOpenGLWidget())
        # self.setRenderHint(QPainter.Antialiasing)
        # self.setFrameStyle(QFrame.NoFrame)

        self.thread = Thread()
        w = self.thread.make_worker(self.open_file, '../../bitmex_1m_2018.pkl')
        w.sig.finished.connect(self.set_scene)
        self.thread.start(w)

        self.open_file_finished = False

    def open_file(self, file_name):
        self.model = Model(pandas.read_pickle(file_name), self)


    def set_scene(self):
        print('call set_scene')
        self.chart_item = CandleStickItem(self.model)

        scene = ChartScene()
        scene.addItem(self.chart_item)

        self.setScene(scene)
        self.chart_item.update()
        self.open_file_finished = True

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # print(self.scene().itemAt(self.mapToScene(event.pos()), QTransform()))
        print(self.mapToScene(event.pos()))
        print(event.pos())
        super().mouseMoveEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent):

        super().resizeEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        """ ChartView's wheel event handler

        Handle mouse wheel event.
        This method must handle :
            1. Change range of model by y-axis
            2. Change translate of model by x-axis

        Parameters
        ----------
        event : QtGui.QWheelEvent
            QGraphicsView's wheel event.

        """
        if self.open_file_finished:
            if platform == "darwin":
                delta_x = event.pixelDelta().x()
                delta_y = event.pixelDelta().y()
            else:
                delta_x = event.angleDelta().x()
                delta_y = event.angleDelta().y()

            self.model.add_range(delta_y)
            self.chart_item.update()

        super().wheelEvent(event)


attach_timer(ChartView)
