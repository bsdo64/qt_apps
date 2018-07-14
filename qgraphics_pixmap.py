from PyQt5 import QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QStyleOptionGraphicsItem, QWidget

from util import perf_timer


class MyPixmapItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)

    @perf_timer("paint")
    def paint(self, painter: QtGui.QPainter,
              option: QStyleOptionGraphicsItem,
              widget: QWidget):

        painter.drawRect(100, 100, 100, 100)

    def boundingRect(self):
        return QRectF(100, 100, 100, 100)


if __name__ == '__main__':
    app = QApplication([])

    view = QGraphicsView()
    scene = QGraphicsScene()
    scene.addItem(MyPixmapItem())
    view.setScene(scene)
    view.show()

    app.exec_()