import typing

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem

from util import perf_timer


class CustomRectsItem(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.path = QPainterPath()

    @perf_timer("CustomRectsItem.paint()")
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        if self.path.length():

            path = self.path

        else:
            path = QPainterPath()

            path.moveTo(0, 0)
            rand = np.random.rand(100) * 100
            for i in np.arange(100):
                path.lineTo(i, rand[i])

        painter.save()
        pen = QPen()
        pen.setCosmetic(True)
        pen.setColor(Qt.darkBlue)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.restore()