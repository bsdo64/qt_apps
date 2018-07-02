import pandas

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtGui import QRadialGradient, QGradient, QPen, QPainterPath, QTransform, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsItem, \
    QStyleOptionGraphicsItem, QWidget, QGraphicsRectItem


class MyItem(QGraphicsItem):
    def __init__(self, data, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.num = 1
        self.data = data
        self.path = QPainterPath()
        self.trans = QTransform()
        self.cached = False
        self.printed = False
        self.setZValue(0)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget = ...):
        close = self.data['close'].reset_index()['close']
        close = close - close.min()
        close_max = close.max()
        close_min = close.min()

        if not self.cached:
            for i in range(close.size - 1):
                self.path.moveTo(i, close[i])
                self.path.lineTo(i+1, close[i+1])

            self.cached = True

        pen = QPen(Qt.white)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRect(0, 0, close.size, close_max - close_min)

        pen.setColor(Qt.yellow)
        painter.setPen(pen)
        painter.drawPath(self.path)

        if not self.printed:
            rec_item = self.scene().addPath(self.path, QPen(Qt.red))
            rec_item.setZValue(-10)
            self.printed = True

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
        self.plot: MyItem(data) = None
        self.bounding_rect = QGraphicsRectItem()
        self.setBackgroundBrush(QColor('#14161f'))

        self.addItem(self.bounding_rect)
        self.printed = False

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print()

        print("rec rect : ", self.rec.rect())
        print("Scene rect : ", self.sceneRect())
        print("ItemBounding rect : ", self.itemsBoundingRect())
        print("transform : ", self.plot.transform().m11(), ", ", self.plot.transform().m22())
        item = self.itemAt(event.scenePos(), self.plot.transform())

        if item and isinstance(item, MyItem):
            print()
            print('collides path : ', self.rec.collidesWithPath(item.path))
            print('collides item : ', self.rec.collidesWithItem(item))



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
        scene: MyScene = self.scene()
        scene.setSceneRect(self.rect().x(), self.rect().y(),
                          self.rect().width(), self.rect().height())

        scene.print_bound(self.rect())

        plot: QGraphicsItem = scene.plot
        trans = QTransform()
        close = plot.data['close'].reset_index()['close']
        close = close - close.min()
        close_max = close.max()
        close_min = close.min()
        trans.scale(self.width() / len(close),
                    self.height() / (close_max - close_min))
        plot.trans = trans
        plot.setTransform(trans)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        rec: QGraphicsRectItem = self.scene().rec
        rec.setRect(event.pos().x() - 5, event.pos().y() - 5, 10, 10)

        super().mouseMoveEvent(event)


if __name__ == '__main__':
    df = pandas.read_pickle('bitmex_1m_2018.pkl')
    data = df[-5000:]

    app = QApplication([])
    scene = MyScene(data)
    view = MyView(data)
    view.setScene(scene)

    rec = QGraphicsRectItem(-2, -2, 4, 4)
    rec.setPen(Qt.white)
    scene.rec = rec
    scene.addItem(rec)

    plot = MyItem(data)
    scene.addItem(plot)
    scene.plot = plot

    view.show()

    app.exec_()
