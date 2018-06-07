import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QLineF
from PyQt5.QtGui import QFont, QPainterPath, QPen, QBrush, QSurfaceFormat, QPainter
from PyQt5.QtOpenGL import QGLFormat, QGL, QGLWidget
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsView, QOpenGLWidget, QGridLayout

import pyqtgraph

class MyView(QGraphicsView):
    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        point = event.angleDelta()
        sc = point.y() / 10000
        self.scale(1 + sc, 1 + sc)


class MyScene(QGraphicsScene):
    def __init__(self, x, y, w, h):
        QGraphicsScene.__init__(self, x, y, w, h)

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        grid_size = 25

        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)

        lines = []

        for x in range(left, int(rect.right()), grid_size):
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))

        for y in range(top, int(rect.bottom()), grid_size):
            lines.append(QLineF(rect.left(), y, rect.right(), y))

        # print(len(lines))

        painter.drawLines(lines)


def make_candlestick(scene, n):
    width = 50
    gap = 10

    scene.addRect(QRectF((width+gap) * n, n, 100, 200), QPen(Qt.transparent), QBrush(Qt.green))


def make_path(scene, n):
    path2 = QPainterPath()
    path2.moveTo(50, -10)
    path2.lineTo(50 + n, 220 + n)

    scene.addPath(path2, QPen(Qt.black))


if __name__ == '__main__':
    app = QApplication([])

    fmt = QSurfaceFormat()
    fmt.setSamples(10)
    QSurfaceFormat.setDefaultFormat(fmt)

    scene = MyScene(0., 0., 600., 400.)

    path = QPainterPath()
    path.moveTo(0, 0)
    path.lineTo(50, 110)

    path2 = QPainterPath()
    path2.moveTo(50, -10)
    path2.lineTo(50, 220)

    scene.addPath(path2, QPen(Qt.black))
    scene.addRect(QRectF(0, 0, 100, 200), QPen(Qt.transparent), QBrush(Qt.green))

    scene.addRect(QRectF(200, 0, 100, 200), QPen(Qt.transparent), QBrush(Qt.red))
    scene.addPath(path, QPen(Qt.black), QBrush(Qt.green))
    scene.addText("I Love Qt Programming", QFont("Times", 22, QFont.Bold))

    view = MyView(scene)
    view.setViewport(QOpenGLWidget())
    view.setRenderHints(QPainter.HighQualityAntialiasing)
    view.show()

    layout = QGridLayout()

    app.exec()
