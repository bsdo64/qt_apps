import pandas
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainterPath, QTransform, QPen

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPathItem
from numpy import random

df = pandas.read_pickle('bitmex_1m_2018.pkl')
data = df[-200:]
close = data['close'].reset_index()['close']
close = close.max() - close
close_max = close.max()
close_min = close.min()

close2 = close - 4
close2_max = close2.max()
close2_min = close2.min()


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.scene().itemAt(self.mapToScene(event.pos()), QTransform()):
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().mouseMoveEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        plot: QGraphicsPathItem = self.scene().items()[0]
        trans = QTransform()
        trans.scale(self.width() / len(data), self.height() / (close_max - close_min))
        plot.setTransform(trans)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # print(event.pixelDelta())
        plot: QGraphicsPathItem = self.scene().items()[0]
        trans = plot.transform()

        trans.translate(event.pixelDelta().x(), 0)
        plot.setTransform(trans)

    def update_last_plot(self):
        global close_max

        plots = self.scene().items()

        for plot in plots:
            plot: QGraphicsPathItem = plot
            path = plot.path()
            last_element = path.elementAt(path.elementCount() - 1)
            path.setElementPositionAt(path.elementCount() - 1, last_element.x, last_element.y + 1)

            plot.setPath(path)

            close_max = close_max + 1
            trans = QTransform()
            trans.scale(self.width() / len(data), self.height() / (close_max - close_min))
            plot.setTransform(trans)


if __name__ == '__main__':

    path = QPainterPath()
    for i in range(close.size - 1):
        path.moveTo(i, close[i])
        path.lineTo(i + 1, close[i + 1])

    path2 = QPainterPath()
    for i in range(close2.size - 1):
        path2.moveTo(i, close2[i])
        path2.lineTo(i + 1, close2[i + 1])

    app = QApplication([])

    view = MyView()

    scene = QGraphicsScene()
    path_item = QGraphicsPathItem(path)

    pen = QPen(Qt.darkGray)
    pen.setCosmetic(True)
    path_item.setPen(pen)

    scene.addItem(path_item)

    path_item = QGraphicsPathItem(path2)

    pen = QPen(Qt.darkGray)
    pen.setCosmetic(True)
    path_item.setPen(pen)

    scene.addItem(path_item)

    timer = QTimer()
    timer.timeout.connect(view.update_last_plot)
    timer.start(1000)
    view.setScene(scene)

    view.show()

    app.exec_()