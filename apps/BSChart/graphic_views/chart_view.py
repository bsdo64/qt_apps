from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QTransform
from PyQt5.QtWidgets import QGraphicsView, QSizePolicy

from graphic_items import SceneRectItem, CustomRectsItem
from graphic_scenes.chart_scene import ChartScene


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        # self.setRenderHint(QPainter.Antialiasing)
        # self.setFrameStyle(QFrame.NoFrame)

        pen = QPen()
        pen.setCosmetic(True)

        scene = ChartScene()
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
        # super().wheelEvent(event)
        # print(event.angleDelta())
