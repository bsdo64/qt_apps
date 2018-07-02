import pandas

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtGui import QRadialGradient, QGradient, QPen, QPainterPath, QTransform, QPainter
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
        self.bounding_rect = QGraphicsRectItem()
        self.setBackgroundBrush(Qt.blue)

        self.addItem(self.bounding_rect)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print()
        print("rec pos : ", self.rec.pos())
        print("rec rect : ", self.rec.rect())
        print("Scene rect : ", self.sceneRect())
        print("ItemBounding rect : ", self.itemsBoundingRect())
        item = self.itemAt(event.scenePos(), QTransform())

        if item and isinstance(item, MyItem):
            print()Z
            print('haha')
            print(self.rec.pos())
            print(self.rec.scenePos())
            print(self.rec.collidesWithPath(item.path))
            print(item.contains(event.scenePos()))

        super().mouseMoveEvent(event)

    def print_bound(self, rect):
        self.bounding_rect.setPen(QPen(Qt.green))
        self.bounding_rect.setRect(rect.x() + 5, rect.y() + 5,
                          rect.width() - 10, rect.height() - 10)


class MyView(QGraphicsView):
    def __init__(self, data, parent=None):
        QGraphicsView.__init__(self, parent)
        self.data = data
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        print("pixel / Data : {}".format(self.width() / len(self.data)))

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.scene().setSceneRect(self.rect().x(), self.rect().y(),
                          self.rect().width(), self.rect().height())

        self.scene().print_bound(self.rect())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        rec: QGraphicsRectItem = self.scene().rec
        rec.setPos(self.mapToScene(event.pos()))

        super().mouseMoveEvent(event)


if __name__ == '__main__':
    df = pandas.read_pickle('bitmex_1m_2018.pkl')
    data = df[-100:]

    app = QApplication([])
    scene = MyScene(data)
    view = MyView(data)
    view.setScene(scene)
    view.show()

    scene.addLine(0, 0, 10, 10, QPen(Qt.white))
    rec = QGraphicsRectItem(-2, -2, 4, 4)
    rec.setPen(Qt.red)
    scene.rec = rec
    scene.addItem(rec)

    scene.addItem(MyItem(data))

    app.exec_()
