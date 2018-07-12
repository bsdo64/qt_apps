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
        self.model: Model = model

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):

        painter.save()
        # painter.setRenderHint(painter.Antialiasing)

        pen = QPen()
        pen.setCosmetic(True)
        painter.setPen(pen)

        path = QPainterPath()
        model_data = self.model.data()
        for i, row in model_data.iterrows():
            path.addRect(row['time_axis'], row['open'], 1, row['close'] - row['open'])

        painter.fillPath(path, Qt.green)
        painter.drawRect(QRectF(model_data['time_axis'].min(),
                                model_data['open'].min(),
                                len(model_data),
                                model_data['open'].max() - model_data['close'].min()))
        painter.restore()

    def boundingRect(self):
        model_data = self.model.data()
        rect = QRectF(model_data['time_axis'].min(),
                      model_data['open'].min(),
                      len(model_data),
                      model_data['open'].max() - model_data['close'].min())

        return rect


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setTransformationAnchor(self.NoAnchor)
        # self.setRenderHint(QPainter.Antialiasing)
        # self.setFrameStyle(QFrame.NoFrame)

        self.model = Model(pandas.read_pickle('../../bitmex_1m_2018.pkl'), self)

        pen = QPen(Qt.red)
        pen.setCosmetic(True)
        scene = ChartScene()
        self.candlestick = CandleStickItem(self.model)
        scene.addItem(self.candlestick)
        # self.scene_rect = SceneRectItem()
        # scene.addItem(self.scene_rect)
        # scene.addItem(CustomRectsItem())
        # self.scene_rect = scene.addRect(scene.sceneRect(), pen)
        self.setScene(scene)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # print(self.scene().itemAt(self.mapToScene(event.pos()), QTransform()))
        print(self.mapToScene(event.pos()))
        print(event.pos())
        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # print(event.angleDelta())

        # scale by mouse point
        # self.setTransformationAnchor(QGraphicsView.NoAnchor)
        # self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        # old_pos = self.mapToScene(event.pos())
        # self.scale(1 + event.angleDelta().y() / 1000, 1)
        # new_pos = self.mapToScene(event.pos())
        # delta = new_pos - old_pos
        # print(delta)
        # self.translate(delta.x(), delta.y())
        self.model.add_range(event.pixelDelta().y())
        self.candlestick.update()

