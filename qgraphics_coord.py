from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QTransform, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem

import pyqtgraph

class View(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(Qt.yellow)
        self.setScene(self.scene)

        center_rect = QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(center_rect)

        rect = QGraphicsRectItem(0, 0, 100, 100)
        rect.setPos(-100, -100)
        self.scene.addItem(rect)

        rect2 = QGraphicsRectItem(0, 0, 100, 100)
        self.scene.addItem(rect2)

        text = self.scene.addText("Hello WOrld")

        # self.scene.addLine(QLineF(0, 10, -20, -20), QPen(Qt.black))

        rect2.moveBy(50, 50)
        rect2.setRotation(50)
        rect2.moveBy(-50, -50)

        print(self.scene.width(), self.scene.height())

        self.resize(400, 400)



if __name__ == '__main__':
    app = QApplication([])

    view = View()
    view.show()

    app.exec_()