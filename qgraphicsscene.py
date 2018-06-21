from PyQt5.QtCore import Qt
from PyQt5.QtGui import QRadialGradient, QGradient, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView


if __name__ == '__main__':
    app = QApplication([])
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    view.show()

    scene.setBackgroundBrush(Qt.blue)

    gradient = QRadialGradient(0, 0, 10)
    gradient.setSpread(QGradient.RepeatSpread)

    scene.addLine(0,0, 10, 10, QPen(Qt.white))

    app.exec_()