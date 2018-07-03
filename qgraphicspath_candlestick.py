import pandas
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPainterPath, QTransform, QPen, QBrush, QPainter

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPathItem, QGraphicsItem, \
    QStyleOptionGraphicsItem, QWidget
from numpy import random

df = pandas.read_pickle('bitmex_1m_2018.pkl')
data = df[-200:]
data = data.reset_index()
close = data['close']
close = close.max() - close
close_max = close.max()
close_min = close.min()


class MyItem(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = None):

        print(option.levelOfDetailFromTransform(painter.worldTransform()))

        painter.save()
        pen = QPen(Qt.red)
        pen.setWidth(0)
        painter.setPen(pen)
        brush = pen.brush()
        for i in range(200 - 1):
            height = data['high'][i] - data['low'][i]
            painter.fillRect(QRectF(i * 3, data['high'][i] - data['high'].min(), 1, height), brush)
        painter.restore()

    def boundingRect(self):
        return QRectF(0, 0, len(data) * 3, data['high'].max() - data['low'].min())


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # print(self.mapToScene(event.pos()))
        # print(self.scene().itemAt(self.mapToScene(event.pos()), QTransform()))

        if self.scene().itemAt(self.mapToScene(event.pos()), QTransform()):
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        print("pixel / Data : {}".format(self.width() / len(data)))
    #
    def resizeEvent(self, event: QtGui.QResizeEvent):
        plot: QGraphicsPathItem = self.scene().items()[0]
        trans = QTransform()
        trans.scale(self.width() / len(data) / 3, self.height() / (data['high'].max() - data['low'].min()))
        plot.setTransform(trans)


if __name__ == '__main__':
    #
    # path = QPainterPath()
    # for i in range(close.size - 1):
    #     path.moveTo(i, close[i])
    #     path.lineTo(i + 1, close[i + 1])

    app = QApplication([])

    view = MyView()

    scene = QGraphicsScene()
    # path_item = QGraphicsPathItem(path)

    # pen = QPen(Qt.darkGray)
    # pen.setCosmetic(True)
    # path_item.setPen(pen)
    #
    # scene.addItem(path_item)
    scene.addItem(MyItem())

    view.setScene(scene)
    view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    view.show()

    app.exec_()