import pandas

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtGui import QRadialGradient, QGradient, QPen, QPainterPath, QTransform
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsItem, \
    QStyleOptionGraphicsItem, QWidget, QGraphicsRectItem


class MyItem(QGraphicsItem):
    def __init__(self, data, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.num = 1
        self.data = data
        self.path = QPainterPath()
        self.setZValue(0)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = ...):
        close = self.data['close'].reset_index()['close']
        close = close - close.min()
        close_max = close.max()
        close_min = close.min()

        for i in range(close.size - 1):
            self.path.moveTo(i, close[i])
            self.path.lineTo(i+1, close[i+1])

        painter.setPen(QPen(Qt.white))
        painter.drawRect(0, 0, close.size, close_max - close_min)

        painter.setPen(QPen(Qt.yellow))
        painter.drawPath(self.path)

        painter.setPen(QPen(Qt.red))
        painter.drawEllipse(self.boundingRect())

    def boundingRect(self):
        close = self.data['close'].reset_index()['close']
        close_max = close.max()
        close_min = close.min()

        return QRectF(0, 0, close.size, close_max - close_min)


class MyScene(QGraphicsScene):
    def __init__(self, data, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.data = data
        self.rec = QGraphicsRectItem()
        self.setBackgroundBrush(Qt.blue)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        # self.rec.moveBy()
        self.rec.setRect(event.scenePos().x(), event.scenePos().y(), 10, 10)
        print("Rect : ", self.rec.rect())
        print(event.scenePos())
        item = self.itemAt(event.scenePos(), QTransform())

        if item and isinstance(item, MyItem):
            print('haha')
            print(self.rec.collidesWithPath(item.path))
        #     print(item.contains(event.scenePos()))

        super().mouseMoveEvent(event)


class MyView(QGraphicsView):
    def __init__(self, data, parent=None):
        QGraphicsView.__init__(self, parent)
        self.data = data
        self.setMouseTracking(True)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        print("pixel / Data : {}".format(self.width() / len(self.data)))
        self.setFixedWidth(self.width() + event.angleDelta().y())


if __name__ == '__main__':
    df = pandas.read_pickle('bitmex_1m_2018.pkl')
    data = df[-100:]

    app = QApplication([])
    scene = MyScene(data)
    view = MyView(data)
    view.setScene(scene)
    view.show()

    scene.addLine(0, 0, 10, 10, QPen(Qt.white))
    rec = QGraphicsRectItem(0, 0, 1, 1)
    scene.addItem(rec)
    scene.rec = rec

    scene.addRect(scene.sceneRect(), QPen(Qt.white))
    scene.addItem(MyItem(data))

    app.exec_()
