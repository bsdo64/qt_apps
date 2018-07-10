from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QGraphicsView, QWidget, QGraphicsScene


class ChartScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)


class ChartView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setViewportMargins(0, 0, 0, 0)
        self.resize(640, 480)

        scene = ChartScene()
        scene.addRect(0, 0, 100, 100)
        scene.addRect(100, 100, 100, 100)
        scene.addRect(500, 500, 100, 100)
        scene.addRect(640, 480, 100, 100)
        self.setScene(scene)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        print(event.angleDelta())


if __name__ == '__main__':
    app = QApplication([])
    view = ChartView()
    view.show()
    app.exec_()