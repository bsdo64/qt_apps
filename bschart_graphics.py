from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTranslator, QObject
from PyQt5.QtGui import QColor, QPainterPath
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QStyleOptionGraphicsItem


class AxisItem(QGraphicsItem):
    def __init__(self, scene, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.moveBy(-scene.width() / 2, -scene.height() / 2)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None):
        path = QPainterPath()
        path.moveTo(-4, 0)
        path.lineTo(-4, 233)
        path.moveTo(93, 0)
        path.lineTo(93, 233)
        path.moveTo(190, 0)
        path.lineTo(190, 233)
        path.moveTo(287, 0)
        path.lineTo(287, 233)
        path.moveTo(384, 0)
        path.lineTo(384, 233)

        painter.setPen(QColor('#363c4e'))
        painter.drawPath(path)


class GraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        scene = QGraphicsScene(self)
        scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(QObject.tr(self, 'Graph'))

        self.setBackgroundBrush(QColor('#131722'))

        axis = AxisItem(scene)
        scene.addItem(axis)


if __name__ == '__main__':
    app = QApplication([])

    win = GraphWidget()
    win.show()
    app.exec_()
