import random

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainterPath, QPen, QBrush
from PyQt5.QtOpenGL import QGLFormat, QGL, QGLWidget
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsView, QOpenGLWidget

import pyqtgraph

class MyView(QGraphicsView):
    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        point = event.angleDelta()
        sc = point.y() / 10000
        self.scale(1 + sc, 1 + sc)


def make_candlestick(scene, n):
    width = 50
    gap = 10

    scene.addRect(QRectF((width+gap) * n, n, 100, 200), QPen(Qt.transparent), QBrush(Qt.green))


def make_path(scene, n):
    path2 = QPainterPath()
    path2.moveTo(50, -10)
    path2.lineTo(50+ n, 220 + n)

    scene.addPath(path2, QPen(Qt.black))

if __name__ == '__main__':
    app = QApplication([])
    scene = QGraphicsScene()

    path = QPainterPath()
    path.moveTo(0, 0)
    path.lineTo(50, 110)

    path2 = QPainterPath()
    path2.moveTo(50, -10)
    path2.lineTo(50, 220)

    for i in range(2000):
        make_candlestick(scene, random.randint(0, 10))

    scene.addPath(path2, QPen(Qt.black))
    scene.addRect(QRectF(0,0,100,200), QPen(Qt.transparent), QBrush(Qt.green))

    scene.addRect(QRectF(200, 0, 100, 200), QPen(Qt.transparent), QBrush(Qt.red))
    scene.addPath(path, QPen(Qt.black), QBrush(Qt.green))
    scene.addText("I Love Qt Programming", QFont("Times", 22, QFont.Bold))

    view = MyView(scene)
    view.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
    view.show()

    app.exec()