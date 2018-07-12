from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene


class ChartScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

    def sceneRectChanged(self, rect: QtCore.QRectF):
        pass
