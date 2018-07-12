import typing

import pandas

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QSizePolicy, QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from data.model import Model
from graphic_items import SceneRectItem, CustomRectsItem
from graphic_scenes.chart_scene import ChartScene


class CandleStickItem(QGraphicsItem):
    def __init__(self, model, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.model = model

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        data = self.model.series[-100:]

        painter.save()
        painter.setRenderHint(painter.Antialiasing)
        pen = QPen()
        pen.setCosmetic(True)

        painter.setPen(pen)
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(100, 100)

        painter.drawPath(path)
        painter.restore()

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        # self.setRenderHint(QPainter.Antialiasing)
        # self.setFrameStyle(QFrame.NoFrame)

        self.model = Model(pandas.read_pickle('../../bitmex_1m_2018.pkl'))

        scene = ChartScene()
        scene.addItem(CandleStickItem(self.model))
        scene.addItem(SceneRectItem())
        scene.addItem(CustomRectsItem())
        self.setScene(scene)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # print(self.scene().itemAt(self.mapToScene(event.pos()), QTransform()))
        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # print(event.angleDelta())

        # scale by mouse point
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        # self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        old_pos = self.mapToScene(event.pos())
        self.scale(1 + event.angleDelta().y() / 1000, 1)
        new_pos = self.mapToScene(event.pos())
        delta = new_pos - old_pos
        # print(delta)
        # self.translate(delta.x(), delta.y())
        super().wheelEvent(event)

